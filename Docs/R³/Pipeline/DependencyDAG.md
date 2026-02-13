# Pipeline: Dependency DAG

**Purpose**: Documents the dependency graph between R3 spectral groups, the resulting stage ordering, and the GPU parallelization strategy.

---

## 1. Current State (v1): No Dependency Awareness

In the current implementation, `R3Extractor.extract()` iterates sequentially over all groups, passing the same `mel` tensor to each:

```python
# Current code (mi_beta/ear/r3/__init__.py):
def extract(self, mel: Tensor) -> R3Output:
    parts = []
    names: List[str] = []
    for group in self.groups:
        feat = group.compute(mel)  # (B, T, group_dim)
        parts.append(feat)
        names.extend(group.feature_names)
    features = torch.cat(parts, dim=-1)  # (B, T, total_dim)
    return R3Output(features=features, feature_names=tuple(names))
```

**Implication**: Group E (Interactions) currently computes its own proxy features instead of referencing the actual A-D outputs. This introduces proxy mismatch (documented in R3-V2-DESIGN.md Section 4).

---

## 2. Phase 6 Dependency DAG (v2, 128D)

### 2.1 Group-Level DAG

```
                      ┌────────────────────────────────────────────┐
                      │             mel (B, 128, T)                 │
                      └──┬──┬──┬──┬──┬──┬──────────────────────────┘
                         │  │  │  │  │  │
   Stage 1 (parallel):  v  v  v  v  v  v  v
                        [A][B][C][D][F][J][K]
                         │  │  │  │  │  │  │
                         │  │  │  │  │  │  │
   Stage 2 (parallel):  │  │  │  │  │  │  │
                         └──┴──┴──┤  │  │  │
                            ┌─────┘  │  │  │
                            v     ┌──┘  │  │
                           [E]    │     │  │
                           (A,B,  v     │  │
                            C,D) [G]    │  │
                                 (B[11])│  │
                                     ┌──┘  │
                                     v     │
                                    [H]    │
                                    (F     │
                                   chroma) │
                                     │     │
   Stage 3:                          │     │
                            ┌────────┤     │
                            v        v     │
                           [I]             │
                           (F chroma,      │
                            G onset,       │
                            H key)         │
                                           │
   Concat:  torch.cat([A,B,C,D,E,F,G,H,I,J,K], dim=-1) -> (B, T, 128)
```

### 2.2 Stage Assignment Table

| Stage | Groups | Dependencies | Can Run In Parallel |
|:-----:|--------|-------------|:---:|
| 1 | A(7D), B(5D), C(9D), D(4D), F(16D), J(20D), K(14D) | mel only | Yes (7 streams) |
| 2 | E(24D), G(10D), H(12D) | E needs A,B,C,D; G needs B[11]; H needs F chroma | Yes (3 streams) |
| 3 | I(7D) | F chroma, G onset, H key | No (single group) |
| - | Concat | All groups | - |

### 2.3 Why These Dependencies Exist

**F must compute before H and I (chroma dependency)**:

Group F computes a 12-dimensional chroma vector from the mel spectrogram using Gaussian soft-assignment:

```python
mel_linear = mel.exp()
chroma = torch.matmul(self.mel_to_chroma.T, mel_linear)  # (B, 12, T)
chroma = chroma / chroma.sum(dim=1, keepdim=True).clamp(min=1e-8)
```

This chroma output is consumed by:
- **H** (Harmony & Tonality): Key detection via Krumhansl-Schmuckler correlation against 24 key profiles. Tonnetz projection via 12x6 pre-computed matrix. Voice-leading distance, harmonic change, diatonicity -- all require the pitch class distribution.
- **I** (Information & Surprise): Melodic entropy (chroma transition probabilities), harmonic entropy (KL divergence from running average chroma), tonal ambiguity (softmax entropy of key correlations).

Without F's chroma, H and I would need to independently recompute it, wasting computation and risking inconsistency.

**G needs B[11] onset_strength**:

Group G (Rhythm & Groove) computes tempo, beat strength, syncopation, and related features from the onset envelope. The onset strength signal is B's feature at index 11 (the 5th feature within group B):

```python
onset = group_outputs['energy'][:, :, 4]  # B[11] = onset_strength
```

The autocorrelation of onset strength yields tempo estimate, beat strength, and pulse clarity. Syncopation requires both onset peaks and the estimated tempo period.

**I needs F, G, and H outputs**:

Group I (Information & Surprise) operates on running statistics and information-theoretic measures that span multiple perceptual domains:
- `melodic_entropy` [87]: Uses F chroma transitions.
- `harmonic_entropy` [88]: Uses F chroma KL divergence.
- `rhythmic_information_content` [89]: Uses B[11] onset timing and G[65] tempo.
- `tonal_ambiguity` [93]: Uses H[75] key correlation distribution.
- `spectral_surprise` [90], `information_rate` [91], `predictive_entropy` [92]: Use mel directly but with running state.

---

## 3. Feature-Level Dependency Graph

```
mel ──┬── A[0:7] ──────────────────────────────────────── E[25:49]
      ├── B[7:12] ─┬── B[11] onset_strength ──── G[65:75] ── I[89]
      │             └── E[25:49]                              │
      ├── C[12:21] ──────────────────────────────── E[25:49]  │
      ├── D[21:25] ──────────────────────────────── E[25:49]  │
      ├── F[49:65] ─┬── chroma[49:61] ──┬── H[75:87] ─── I[87,88,93]
      │             │                    └── I[87,88]
      │             ├── pitch_height[61]
      │             ├── PC_entropy[62]
      │             ├── pitch_salience[63]
      │             └── inharmonicity[64]
      ├── J[94:114] (independent)
      └── K[114:128] ─── mod_4Hz[117] -> fluctuation[123]

                      I[87:94] <- F chroma + G onset + H key + mel
```

### 3.1 Critical Dependency Chains

**Longest chain** (determines minimum latency):

```
mel -> F (chroma) -> H (key clarity, tonnetz) -> I (tonal ambiguity)
       ~1.0ms        ~1.0ms                       ~0.5ms
                                                   ─────────
                                            Total: ~2.5ms minimum
```

**Parallel chains** (can overlap with the critical path):

```
mel -> A,B,C,D    (Stage 1, ~0.1ms each)
mel -> J           (Stage 1, ~0.5ms)
mel -> K           (Stage 1, ~0.5ms amortized)
B[11] -> G         (Stage 2, ~0.8ms)
A,B,C,D -> E       (Stage 2, ~0.1ms)
```

---

## 4. GPU Parallelization Strategy

### 4.1 Multi-Stream Execution

Each stage can exploit GPU parallelism by assigning groups to separate CUDA streams:

```
Stage 1 (7 CUDA streams):
    Stream 0: A (Consonance)       ████ 0.1ms
    Stream 1: B (Energy)           ████ 0.1ms
    Stream 2: C (Timbre)           ████ 0.1ms
    Stream 3: D (Change)           ████ 0.1ms
    Stream 4: F (Pitch & Chroma)   ██████████████████████ 1.0ms
    Stream 5: J (Timbre Extended)  ██████████ 0.5ms
    Stream 6: K (Modulation)       ██████████ 0.5ms*
              ────────────────────────────────────────────
    Stage 1 wall time: max(K) = ~3.0ms peak / ~0.5ms amortized

    * K performs sliding FFT every 86 frames; average cost ~0.5ms

Stage 2 (3 CUDA streams):
    Stream 0: E (Interactions)     ██ 0.1ms
    Stream 1: G (Rhythm & Groove)  ████████████████ 0.8ms
    Stream 2: H (Harmony)          ██████████████████████ 1.0ms
              ────────────────────────────────────────────
    Stage 2 wall time: max(H) = ~1.0ms

Stage 3 (1 CUDA stream):
    Stream 0: I (Information)      ████████████████ 0.8ms
              ────────────────────────────────────────────
    Stage 3 wall time: ~0.8ms

Concat: torch.cat (all parts) → <0.1ms
```

### 4.2 Synchronization Points

```
                    Stage 1
                   /   |   \
    [A,B,C,D]  [F]   [J,K]
         |       |
         v       v
    ─── SYNC ─── SYNC ───  (barrier between Stage 1 and Stage 2)
         |       |      |
        [E]     [H]    [G]
         |       |      |
         v       v      v
    ─── SYNC ─── SYNC ── SYNC ──  (barrier between Stage 2 and Stage 3)
                |
               [I]
                |
                v
    ─── SYNC ──  (before concat)
                |
            torch.cat
```

Each SYNC is a `torch.cuda.synchronize()` or stream event wait, ensuring outputs from the previous stage are available.

---

## 5. Compute Order Table with Estimated Latencies

| Order | Group | Dim | Stage | Dependencies | Est. Latency | Notes |
|:-----:|-------|:---:|:-----:|-------------|:---:|-------|
| 1 | A: Consonance | 7D | 1 | mel | 0.1 ms | 7 simple mel statistics |
| 2 | B: Energy | 5D | 1 | mel | 0.1 ms | RMS, diff, sigmoid |
| 3 | C: Timbre | 9D | 1 | mel | 0.1 ms | Band ratios, centroid, autocorrelation |
| 4 | D: Change | 4D | 1 | mel | 0.1 ms | Flux, entropy, flatness |
| 5 | F: Pitch & Chroma | 16D | 1 | mel | 1.0 ms | 128x12 chroma matmul + peak analysis |
| 6 | J: Timbre Extended | 20D | 1 | mel | 0.5 ms | 128x13 DCT + 7-band contrast |
| 7 | K: Modulation | 14D | 1 | mel | 0.5 ms* | Sliding FFT (amortized) |
| 8 | E: Interactions | 24D | 2 | A,B,C,D | 0.1 ms | 24 element-wise multiplies |
| 9 | G: Rhythm & Groove | 10D | 2 | B[11] | 0.8 ms | FFT autocorrelation + peak detect |
| 10 | H: Harmony & Tonality | 12D | 2 | F chroma | 1.0 ms | 24 key correlations + tonnetz |
| 11 | I: Information | 7D | 3 | F,G,H,mel | 0.8 ms | Running statistics + KL divergence |

*K group cost is amortized: full sliding FFT runs every 86 frames (~0.5s). Peak cost is ~3.0ms but the average per-frame cost is ~0.5ms.

### 5.1 Sequential vs Parallel Totals

```
Sequential total:  0.1+0.1+0.1+0.1+1.0+0.5+0.5+0.1+0.8+1.0+0.8 = 5.1ms
Parallel total:    max(S1) + max(S2) + S3 + concat
                 = 1.0 + 1.0 + 0.8 + 0.1
                 = 2.9ms (peak)
                 = ~2.5ms (amortized, K averaging)

Frame budget:     5.8ms (at 172.27 Hz)
Headroom:         5.8 / 2.5 = 2.3x real-time
```

---

## 6. Current Code vs Phase 6 Comparison

| Aspect | Current (v1) | Phase 6 (v2) |
|--------|-------------|--------------|
| Groups | A-E (5 groups, 49D) | A-K (11 groups, 128D) |
| Execution | Sequential loop | 3-stage DAG with `compute_with_deps` |
| E group | Internal proxy computation | Receives real A-D outputs |
| G group | Does not exist | Receives B[11] onset_strength |
| H group | Does not exist | Receives F[49:61] chroma |
| I group | Does not exist | Receives F, G, H outputs |
| GPU parallelism | None (single thread) | Multi-stream per stage |
| Synchronization | Implicit (sequential) | Explicit barriers between stages |
| Dependency declaration | None | `STAGE_ORDER` dict + `compute_with_deps()` |
