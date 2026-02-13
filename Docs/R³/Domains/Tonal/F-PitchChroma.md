# Group F: Pitch & Chroma [49:65] -- 16D

## Overview
- **Domain**: Tonal
- **Code**: `mi_beta/ear/r3/domains/tonal/pitch_chroma.py`
- **Status**: NEW (Phase 3)
- **Quality Tier**: Approximate (chroma from mel; not CQT-based) / Standard (pitch_height, entropy)
- **Pipeline Stage**: 1 (parallel, mel-only)
- **Class**: `PitchChromaGroup(BaseSpectralGroup)`

## Feature Table

| Index | Feature Name | Formula | Normalization | Cost | Psychoacoustic Basis | Quality |
|-------|-------------|---------|---------------|------|---------------------|---------|
| 49 | chroma_C | mel->freq->PC fold, pitch class 0 | L1-norm (sum=1) | ~0.5 ms (all) | Octave equivalence (Shepard 1964) | Approximate |
| 50 | chroma_Db | pitch class 1 | L1-norm | (shared) | " | Approximate |
| 51 | chroma_D | pitch class 2 | L1-norm | (shared) | " | Approximate |
| 52 | chroma_Eb | pitch class 3 | L1-norm | (shared) | " | Approximate |
| 53 | chroma_E | pitch class 4 | L1-norm | (shared) | " | Approximate |
| 54 | chroma_F | pitch class 5 | L1-norm | (shared) | " | Approximate |
| 55 | chroma_Gb | pitch class 6 | L1-norm | (shared) | " | Approximate |
| 56 | chroma_G | pitch class 7 | L1-norm | (shared) | " | Approximate |
| 57 | chroma_Ab | pitch class 8 | L1-norm | (shared) | " | Approximate |
| 58 | chroma_A | pitch class 9 | L1-norm | (shared) | " | Approximate |
| 59 | chroma_Bb | pitch class 10 | L1-norm | (shared) | " | Approximate |
| 60 | chroma_B | pitch class 11 | L1-norm | (shared) | " | Approximate |
| 61 | pitch_height | `sum(log2(f_k) * mel_k) / sum(mel_k)` | min-max [log2(20), log2(22050)] | <0.1 ms | Weber-Fechner perceived pitch | Standard |
| 62 | pitch_class_entropy | `-sum(chroma * log(chroma)) / log(12)` | /log(12) -> [0,1] | <0.1 ms | Pitch distribution uniformity | Standard |
| 63 | pitch_salience | `(peak - median) / (peak + median)` | natural [0,1] | <0.1 ms | Parncutt 1989 virtual pitch (proxy) | Approximate |
| 64 | inharmonicity_index | Spectral peak deviation from harmonic template | clamp(0,1) | ~1.0 ms | Harmonic series deviation | Approximate |

## Computation Pipeline

- **Input**: mel (B, 128, T) -- log-mel spectrogram
- **Dependencies**: None (H and I groups depend on this group's chroma output)
- **Output**: (B, T, 16) -- chroma [0,1] L1-normalized; others [0,1]
- **Estimated cost**: ~1.5 ms/frame total
- **Warm-up**: None

### Mel-to-Chroma Matrix Computation

The core of Group F is the pre-computed chroma mapping matrix M (128 x 12).

```
Algorithm:
1. Compute mel bin center frequencies:
   mel_min = 2595 * log10(1 + fmin/700)        # fmin = 0
   mel_max = 2595 * log10(1 + fmax/700)        # fmax = 22050
   mels = linspace(mel_min, mel_max, 128)
   f_center = 700 * (10^(mels/2595) - 1)       # (128,) Hz

2. Convert to MIDI pitch:
   midi = 69 + 12 * log2(f_center / 440)       # (128,)

3. Build Gaussian soft-assignment matrix:
   sigma = 0.5 semitone
   For each pitch class c in 0..11:
     dist = (midi % 12 - c + 6) % 12 - 6       # circular distance
     M[:, c] = exp(-0.5 * dist^2 / sigma^2)

4. Zero out unreliable bins:
   M[f_center < 20 Hz] = 0.0                   # below audible range

Result: M (128, 12) -- register_buffer("mel_to_chroma", M)
```

**Quality limitation**: Below ~200 Hz, mel bins span more than one semitone,
causing pitch class blurring. This is the primary error source for low-register
music. CQT-based chroma would resolve this but requires raw audio access.

### Detailed Computation Flow

```
mel (B, 128, T)
  |
  +-- mel_linear = exp(mel)                    # log-mel -> linear power
  |
  +-- Chroma (12D) [49:60]:
  |     chroma_raw = M.T @ mel_linear           # (B, 12, T) matmul
  |     chroma = chroma_raw / sum(chroma_raw)   # L1 normalize
  |     chroma = chroma.permute(0, 2, 1)        # (B, T, 12)
  |
  +-- Pitch Height [61]:
  |     weights = mel_linear.permute(0, 2, 1)   # (B, T, 128)
  |     ph = (log2_freqs * weights).sum(-1) / weights.sum(-1)
  |     ph_norm = (ph - log2(20)) / (log2(22050) - log2(20))
  |
  +-- Pitch Class Entropy [62]:
  |     H = -(chroma * log(chroma)).sum(-1) / log(12)
  |     # 0 = single PC dominant (strong tonality)
  |     # 1 = uniform (chromatic / atonal)
  |
  +-- Pitch Salience [63]:
  |     peak = mel.max(dim=1).values             # (B, T)
  |     noise = mel.median(dim=1).values         # (B, T)
  |     salience = (peak - noise) / (peak + noise + 1e-8)
  |
  +-- Inharmonicity Index [64]:
        f0_bin = mel_linear.argmax(dim=1)         # (B, T) dominant peak
        # Simplified proxy: high peak concentration = harmonic
        peak_val = mel_linear.max(dim=1).values
        total_val = mel_linear.sum(dim=1)
        inh = 1 - peak_val / total_val            # low ratio = inharmonic
  |
  cat([chroma, ph, pce, salience, inh]) -> (B, T, 16)
```

## PyTorch Implementation Notes

- **Key operations**: `torch.matmul` (128x12 chroma mapping), `torch.exp`,
  `torch.log`, `torch.argmax`, `torch.median`, `torch.max`
- **Pre-computed matrices**:
  - `mel_to_chroma` (128, 12): Gaussian soft-assignment matrix -- `register_buffer`
  - `log2_freqs` (128,): log2 of mel center frequencies -- `register_buffer`
- **Warm-up requirements**: None
- **Memory**: Chroma matrix 128x12 = 1,536 floats (6 KB). Negligible.

### Chroma Output for Downstream Groups

The chroma vector (B, T, 12) is the primary output consumed by:
- **Group H** (Harmony): key_clarity, tonnetz, voice-leading, harmonic change,
  diatonicity, syntactic irregularity
- **Group I** (Information): melodic_entropy, harmonic_entropy, tonal_ambiguity

In the Stage-aware R3Extractor, the chroma is passed via `group_outputs` dict:
```python
group_outputs['pitch_chroma'][:, :, :12]  # (B, T, 12) chroma vector
```

### Inharmonicity Implementation Note

The design document specifies a full harmonic template matching algorithm
(K=8 harmonics, gather from mel bins at f0, 2*f0, ..., 8*f0). The reference
implementation in R3-V2-DESIGN.md Section 6.1 uses a simplified proxy:
`1 - peak_val / total_val`. The full implementation should be considered for
Phase 6+ if the proxy proves insufficient for C3 model requirements.

## Phase 6 Notes

Group F is entirely new in R3 v2. No Phase 6 revision is planned.

### Experimental Validation Required

| Feature | Validation Test | Expected Quality |
|---------|----------------|-----------------|
| chroma [49:60] | Key detection accuracy vs librosa.chroma_cqt | >=85% (mel chroma) vs ~90% (CQT) |
| pitch_height [61] | Correlation with perceived pitch ratings | High (log-frequency is perceptually motivated) |
| pitch_class_entropy [62] | Tonal vs atonal classification | High (information-theoretic measure) |
| pitch_salience [63] | Correlation with essentia PitchSalience (raw audio) | Medium (mel peak != spectral peak) |
| inharmonicity_index [64] | Correlation with essentia Inharmonicity (raw audio) | Low-Medium (mel resolution limits harmonic analysis) |

## References

### Primary Papers
- Shepard, R. N. (1964). Circularity in judgments of relative pitch. JASA 36(12), 2346-2353.
- Krumhansl, C. L. (1990). Cognitive Foundations of Musical Pitch. Oxford University Press.
- Parncutt, R. (1989). Harmony: A Psychoacoustical Approach. Springer.
- Fujishima, T. (1999). Realtime chord recognition of musical sound. Proc. ICMC.
- Gomez, E. (2006). Tonal description of polyphonic audio for music content processing. INFORMS J. Computing 18(3).

### Toolkit Implementations
- `librosa.feature.chroma_stft` / `librosa.feature.chroma_cqt` -- chroma reference
- `essentia.HPCP` -- Harmonic Pitch Class Profile (high-quality chroma)
- `essentia.PitchSalience` -- spectral pitch salience
- `essentia.Inharmonicity` -- harmonic deviation from raw audio
