# Pipeline: Performance

**Purpose**: Documents the frame-level computational budget, per-group cost estimates, real-time feasibility analysis, and optimization strategies.

---

## 1. Frame-Level Budget

The R3 pipeline operates at the mel spectrogram frame rate:

```
Sample rate:     44,100 Hz
Hop length:      256 samples
Frame rate:      44,100 / 256 = 172.27 Hz
Frame period:    1 / 172.27 = 5.805 ms
```

**Budget: 5.8 ms per frame** shared across all R3 groups. Any computation that exceeds this budget causes the pipeline to fall below real-time.

---

## 2. Per-Group Cost Estimates

Cost estimates from R3-V2-DESIGN.md Section 3.4, derived from operation analysis and benchmarking:

### 2.1 Detailed Cost Table

| Group | Dim | Computation Type | Est. ms/frame | Primary Operations |
|-------|:---:|-----------------|:---------:|-------------------|
| A: Consonance | 7D | mel statistics | 0.1 | var, mean, diff, corr, slice+sum (7 features) |
| B: Energy | 5D | mel statistics + diff | 0.1 | pow, sqrt, diff, sigmoid, relu+sum |
| C: Timbre | 9D | mel statistics | 0.1 | slice+sum (6x), centroid, max/sum, autocorr |
| D: Change | 4D | mel statistics + diff | 0.1 | L2 norm, entropy, flatness, HHI |
| E: Interactions | 24D | element-wise product | 0.1 | 24 multiply operations |
| F: Pitch & Chroma | 16D | matmul + statistics | 1.0 | 128x12 chroma matmul, argmax, peak/median |
| G: Rhythm & Groove | 10D | FFT autocorrelation | 0.8 | rfft+abs2+irfft, argmax, peak detect, IOI |
| H: Harmony & Tonality | 12D | correlation + projection | 1.0 | 24 key correlations (batch matmul), 12x6 tonnetz matmul, cosine similarity |
| I: Information & Surprise | 7D | KL + entropy + EMA | 0.8 | Running EMA updates, KL divergence, entropy (x3), histogram update |
| J: Timbre Extended | 20D | DCT + band sort | 0.5 | 128x13 DCT matmul, 7-band sort+quantile |
| K: Modulation & Psychoacoustic | 14D | sliding FFT + psychoacoustic | 0.5* | unfold+rfft per band, Bark rebinning, A-weighting, linear regression |

*K group amortized cost. See Section 2.2.

### 2.2 K Group Amortization

Group K computes a sliding-window FFT for modulation spectrum analysis:

```
Window size:  344 frames (~2.0s)
Hop size:     86 frames (~0.5s)
FFT size:     512 (zero-padded)
```

The full FFT computation runs every 86 frames, not every frame. Between FFT windows, the output is interpolated:

```
Full FFT cost:     ~3.0 ms (per-band unfold + rfft over 128 mel bins)
Amortization:      3.0 ms / 86 frames = ~0.035 ms/frame (FFT only)
Interpolation:     ~0.05 ms/frame (F.interpolate)
Psychoacoustic:    ~0.4 ms/frame (Zwicker sharpness, A-weighting, etc.)
Total amortized:   ~0.5 ms/frame
```

Peak cost occurs every 86th frame: ~3.0 ms. For real-time scheduling, this peak must still fit within the frame budget. However, since the pipeline has headroom on non-peak frames, the average performance is what matters for sustained throughput.

---

## 3. Total Estimated Cost

### 3.1 Sequential Execution (v1 current)

```
A(0.1) + B(0.1) + C(0.1) + D(0.1) + E(0.1)
= 0.5 ms/frame

Frame budget:  5.8 ms
Headroom:      5.8 / 0.5 = 11.6x real-time
```

The current v1 pipeline is extremely lightweight with abundant headroom.

### 3.2 Sequential Execution (v2 hypothetical)

```
A(0.1) + B(0.1) + C(0.1) + D(0.1) + E(0.1) +
F(1.0) + G(0.8) + H(1.0) + I(0.8) + J(0.5) + K(0.5)
= 5.1 ms/frame

Frame budget:  5.8 ms
Headroom:      5.8 / 5.1 = 1.14x real-time
```

Sequential execution of all 11 groups barely fits within the frame budget. This is why parallel execution is essential for v2.

### 3.3 Parallel Execution (v2 DAG)

```
Stage 1:  max(A=0.1, B=0.1, C=0.1, D=0.1, F=1.0, J=0.5, K=0.5*) = 1.0 ms
Stage 2:  max(E=0.1, G=0.8, H=1.0) = 1.0 ms
Stage 3:  I = 0.8 ms
Concat:   < 0.1 ms
───────────────────────
Total:    2.9 ms (peak)
          ~2.5 ms (amortized, K averaging)

Frame budget:  5.8 ms
Headroom:      5.8 / 2.5 = 2.3x real-time (amortized)
               5.8 / 2.9 = 2.0x real-time (peak)
```

---

## 4. Real-Time Feasibility

### 4.1 Headroom Summary

| Configuration | ms/frame | RT Headroom | Status |
|--------------|:--------:|:-----------:|--------|
| v1 sequential (49D) | 0.5 | 11.6x | Comfortable |
| v2 sequential (128D) | 5.1 | 1.14x | Marginal -- not recommended |
| v2 parallel (128D, amortized) | 2.5 | 2.3x | Feasible |
| v2 parallel (128D, peak) | 2.9 | 2.0x | Feasible with headroom |
| v2 parallel (128D, K peak frame) | 4.9* | 1.18x | Tight on K peak frames |

*K peak frame scenario: K uses 3.0ms instead of 0.5ms on every 86th frame. Stage 1 becomes max(3.0ms) instead of max(1.0ms), pushing total to 3.0+1.0+0.8+0.1 = 4.9ms.

### 4.2 Mitigation for K Peak Frames

Several strategies can handle the K-group burst:

1. **Asynchronous computation**: Compute K's FFT in a background CUDA stream; use the previous window's result until the new one is ready.
2. **Pipeline buffering**: Allow a 1-frame latency buffer to absorb burst computation.
3. **Batch-aligned FFT**: Schedule K's FFT computation to overlap with non-peak frames of other processing stages.

---

## 5. Cost Tiers

Features and groups can be classified by computational cost:

| Tier | Cost Range | Examples |
|------|-----------|----------|
| **Trivial** | < 0.01 ms | Complement (`1-x`), linear combination, index lookup |
| **Cheap** | 0.01 - 0.1 ms | Band energy ratios, spectral centroid, entropy, element-wise products |
| **Moderate** | 0.1 - 1.0 ms | Matrix multiply (128x12, 128x13), correlation (24 keys), autocorrelation (FFT), DCT, running statistics |
| **Expensive** | 1.0 - 3.0 ms | Sliding FFT (K modulation), harmonic template matching (F inharmonicity) |
| **Very Expensive** | > 3.0 ms | (None currently; CQT-based chroma would be ~5ms, rejected in R3-V2-DESIGN) |

### 5.1 Per-Feature Cost Classification

**Trivial (< 0.01 ms)**:
- `[4] sensory_pleasantness`: `0.6*(1-x) + 0.4*y`
- `[5] inharmonicity`: `1 - x`
- `[6] harmonic_deviation`: `0.5*x + 0.5*(1-y)`
- `[16] spectral_smoothness`: `1 - x`
- `[10] loudness`: `x^0.3`
- `[66] beat_strength`: `R.gather(tempo_lag)` (single lookup)
- `[123] fluctuation_strength`: Direct reference to `[117]`

**Cheap (0.01 - 0.1 ms)**:
- All band energy ratios: [3], [12], [13], [18-20], [125]
- Spectral centroid [15], tonalness [14]
- Entropy [22], flatness [23], concentration [24]
- Flux [21]
- All 24 interaction products [25-48]
- Pulse clarity [67], metricality [69]
- Event density [72], groove [71]
- Tonnetz projection [76-81] (6 dot products)
- Voice-leading distance [82], harmonic change [83]
- Tonal stability [84], diatonicity [85]
- Modulation centroid [120], bandwidth [121]
- A-weighted loudness [124], alpha ratio [125]
- Spectral slope [127]

**Moderate (0.1 - 1.0 ms)**:
- Chroma computation [49-60]: 128x12 matmul
- Key clarity [75]: 24 correlations via batch matmul
- Syntactic irregularity [86]: KL divergence
- Melodic/harmonic entropy [87-88]: Running statistics + KL
- Spectral surprise [90]: 128D EMA + KL
- Information rate [91], predictive entropy [92]: Entropy x3
- MFCC [94-106]: 128x13 DCT matmul
- Spectral contrast [107-113]: 7-band sort + quantile
- Sharpness Zwicker [122]: 128x24 Bark matmul + weighted sum

**Expensive (1.0 - 3.0 ms)**:
- Modulation spectrum [114-119]: Sliding FFT (128 bands x 344 frame window). Peak cost ~3.0ms per evaluation, but amortized to ~0.035ms/frame due to hop=86.
- Inharmonicity index [64]: Harmonic template matching with peak detection.
- Tempo estimate [65]: FFT autocorrelation over full onset envelope.

---

## 6. Optimization Strategies

### 6.1 Pre-Computed Matrices

Several groups use pre-computed matrices stored as `register_buffer`:

| Matrix | Size | Group | Purpose |
|--------|:----:|:-----:|---------|
| `mel_to_chroma` | 128 x 12 | F | Mel-to-chroma Gaussian soft-assignment |
| `key_profiles` | 24 x 12 | H | Krumhansl-Kessler key templates |
| `tonnetz_matrix` | 12 x 6 | H | Harte 2006 tonnetz projection |
| `dct_matrix` | 128 x 13 | J | DCT-II for MFCC |
| `bark_matrix` | 128 x 24 | K | Mel-to-Bark rebinning |
| `a_weights` | 128 | K | A-weighting curve |
| `zwicker_g` | 24 | K | Sharpness weighting function |

Pre-computation moves the matrix construction cost to `__init__` time. At extraction time, only `torch.matmul` is needed.

### 6.2 Batch Processing

All computations are batched along the `B` dimension. A single `torch.matmul(M.T, mel)` processes all batch items simultaneously, exploiting GPU parallelism.

For temporal operations (autocorrelation, sliding FFT), batched FFT (`torch.fft.rfft` on the last dimension) processes all batch items in one call.

### 6.3 Shared Computation

Several features share intermediate results:

- **Autocorrelation R**: Shared between `[65] tempo_estimate`, `[66] beat_strength`, `[67] pulse_clarity`, `[69] metricality_index`.
- **Chroma**: Shared between F[49-60] and all H and I features that consume chroma.
- **Mel linear** (`mel.exp()`): Shared within F (chroma), K (sharpness, loudness).
- **Key correlations**: Shared between H[75] key_clarity and I[93] tonal_ambiguity.

Efficient implementations compute shared intermediates once and pass them to downstream features.

### 6.4 Amortized Computation

Group K's modulation spectrum is the primary example: full FFT every 86 frames with interpolation between evaluations. This pattern can be applied to other windowed computations:

- Tempo estimation (G): Autocorrelation over a 344-frame window could be amortized similarly.
- Running statistics (I): EMA updates are inherently incremental (O(1) per frame).

### 6.5 GPU Stream Scheduling

Phase 6 parallelization uses CUDA streams within each stage:

```python
# Proposed implementation pattern:
streams = [torch.cuda.Stream() for _ in stage_groups]
for stream, group in zip(streams, stage_groups):
    with torch.cuda.stream(stream):
        outputs[group.GROUP_NAME] = group.compute(mel)
torch.cuda.synchronize()
```

This allows independent groups to execute concurrently on the GPU, limited only by available SM (streaming multiprocessor) resources.

---

## 7. Benchmark Protocol

To validate the cost estimates, the following benchmark should be run:

```python
import torch
import time

mel = torch.randn(4, 128, 1000, device='cuda')  # 4 batches, ~5.8s audio

# Warm up
for _ in range(10):
    extractor.extract(mel)
torch.cuda.synchronize()

# Benchmark
N = 100
start = time.perf_counter()
for _ in range(N):
    extractor.extract(mel)
torch.cuda.synchronize()
end = time.perf_counter()

ms_per_call = (end - start) / N * 1000
ms_per_frame = ms_per_call / 1000  # 1000 frames
print(f"Per-frame: {ms_per_frame:.2f} ms  ({5.8/ms_per_frame:.1f}x RT)")
```

Expected results:
- v1 (49D): < 0.5 ms/frame (~11x RT)
- v2 (128D, parallel): < 2.5 ms/frame (~2.3x RT)
