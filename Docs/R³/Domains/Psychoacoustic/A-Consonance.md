# Group A: Consonance [0:7] -- 7D

## Overview
- **Domain**: Psychoacoustic
- **Code**: `mi_beta/ear/r3/psychoacoustic/consonance.py`
- **Status**: EXISTING
- **Quality Tier**: Proxy (most features are spectral statistic proxies, not true psychoacoustic models)
- **Pipeline Stage**: 1 (parallel, mel-only)
- **Class**: `ConsonanceGroup(BaseSpectralGroup)`

## Feature Table

| Index | Feature Name | Formula | Normalization | Cost | Psychoacoustic Basis | Quality |
|-------|-------------|---------|---------------|------|---------------------|---------|
| 0 | roughness | `sigmoid(mel_high.var() / mel.mean() - 0.5)` | sigmoid | <0.1 ms | Plomp-Levelt 1965 critical band beating | Proxy |
| 1 | sethares_dissonance | `mean(\|mel[k] - mel[k+1]\|) / max` | max-norm (frame) | <0.1 ms | Sethares 1993 timbre-dependent dissonance | Proxy |
| 2 | helmholtz_kang | `corr(mel[k], mel[k+1])` lag-1 spectral autocorrelation | clamp(0,1) | <0.1 ms | Terhardt 1979 periodicity detection | Proxy (lag-1 only) |
| 3 | stumpf_fusion | `mel[:N//4].sum() / mel.sum()` | ratio [0,1] | <0.1 ms | Stumpf tonal fusion | Proxy (=warmth[12]) |
| 4 | sensory_pleasantness | `0.6 * (1 - [1]) + 0.4 * [3]` | linear [0,1] | <0.1 ms | Harrison & Pearce 2020 | Derived |
| 5 | inharmonicity | `1 - [2]` | complement [0,1] | <0.01 ms | Deviation from harmonic series | Derived |
| 6 | harmonic_deviation | `0.5 * [1] + 0.5 * (1 - [2])` | linear [0,1] | <0.01 ms | Spectral irregularity | Derived |

## Computation Pipeline

- **Input**: mel (B, 128, T) -- log-mel spectrogram
- **Dependencies**: None
- **Output**: (B, T, 7) -- all values in [0,1]
- **Estimated cost**: <0.1 ms/frame total (7 simple mel statistics)
- **Warm-up**: None (all features are instantaneous)

### Detailed Computation Flow

```
mel (B, 128, T) -> transpose -> mel_t (B, T, 128)
  |
  +-- spectral_mean = mel_t.mean(dim=-1)
  |
  +-- [0] roughness:
  |     high_bins = mel_t[..., 64:]
  |     roughness = sigmoid(high_bins.var() / spectral_mean - 0.5)
  |
  +-- [1] sethares_dissonance:
  |     diff = torch.diff(mel_t, dim=-1)
  |     sethares = diff.abs().mean() / max
  |
  +-- [2] helmholtz_kang:
  |     centered = mel_t - mel_t.mean()
  |     normalized = centered / centered.norm()
  |     autocorr = (normalized[:-1] * normalized[1:]).sum()
  |     helmholtz = autocorr.clamp(0, 1)
  |
  +-- [3] stumpf_fusion:
  |     low_bins = mel_t[..., :32]  (N//4 = 32)
  |     stumpf = low_bins.sum() / total_energy
  |
  +-- [4] sensory_pleasantness = 0.6 * (1 - [1]) + 0.4 * [3]
  +-- [5] inharmonicity = 1.0 - [2]
  +-- [6] harmonic_deviation = 0.5 * [1] + 0.5 * (1 - [2])
  |
  cat([0..6]) -> (B, T, 7) -> clamp(0, 1)
```

## PyTorch Implementation Notes

- **Key operations**: `torch.var`, `torch.diff`, `torch.abs`, `torch.mean`,
  `torch.sigmoid`, element-wise multiply, `torch.norm`, `torch.clamp`
- **Pre-computed matrices**: None
- **Warm-up requirements**: None
- **Helper function**: `_spectral_autocorrelation(mel_t)` computes lag-1
  autocorrelation used by both [2] helmholtz_kang and propagated to [5],[6]

### Current Code Analysis

The existing implementation in `consonance.py` defines `ConsonanceGroup` with:
- `GROUP_NAME = "consonance"`, `OUTPUT_DIM = 7`, `INDEX_RANGE = (0, 7)`
- `compute(mel)` method processes mel (B, N_MELS, T)
- Roughness uses `high_bins = mel_t[..., N//2:]` (top half) with
  `var / mean.clamp(min=1e-8)` then `sigmoid(x - 0.5)`
- Note: Design doc says `mel.var(dim=1) / mel.mean(dim=1)` but code uses
  high-bins-only variance, which is a more targeted roughness proxy
- Sethares uses `torch.diff` + `abs().mean()` with batch-level max-norm
- Helmholtz uses the `_spectral_autocorrelation()` helper (lag-1 only)
- Stumpf uses bottom-quarter ratio `mel[:N//4].sum() / total`
- Pleasantness, inharmonicity, harmonic_deviation are linear combinations

## Phase 6 Notes

### Known Issues

1. **Duplicate [3] = [12]**: `stumpf_fusion` and `warmth` (C group) use
   identical formula: `mel[:, :N//4, :].sum() / mel.sum()`. This is a
   cross-group redundancy reducing effective dimensionality.

2. **Complement duplicate [16] = 1 - [1]**: `spectral_smoothness` (C group)
   is `1 - sethares_dissonance`. Not independent information.

3. **Identical duplicate [17] = [2]**: `spectral_autocorrelation` (C group)
   computes the exact same lag-1 autocorrelation as `helmholtz_kang`.

4. **Derived features [4],[5],[6]**: All three are linear combinations of
   [1],[2],[3]. They add zero independent information.

5. **Effective dimensionality**: ~3 independent dimensions out of 7 nominal.
   Features [0],[1],[2] are the only truly independent computations.

### Phase 6 Revision Plan

| Index | Current | Phase 6 Target | Change |
|-------|---------|----------------|--------|
| 0 | Spectral variance proxy | Real Plomp-Levelt roughness (pairwise ERB beating) | Formula upgrade |
| 1 | Adjacent bin diff proxy | Real Sethares pairwise dissonance d(fi,fj,ai,aj) | Formula upgrade |
| 2 | Lag-1 autocorrelation | Multi-lag autocorrelation max(R(tau)/R(0)) | Formula upgrade |
| 3 | Low-quarter energy ratio | Real Parncutt subharmonic matching | Formula replacement |
| 4 | 0.6*(1-[1]) + 0.4*[3] | Literature-calibrated weights or new feature | Recalibrate |
| 5 | 1 - [2] | Spectral peak deviation from harmonic template | Independent feature |
| 6 | 0.5*[1] + 0.5*(1-[2]) | Spectral irregularity (Jensen 1999) | Independent feature |

### Phase 6 Priority: HIGH
Group A's effective dimensionality of ~3 makes it a critical revision target.
The Plomp-Levelt and Sethares upgrades require spectral peak detection within
ERB bands, which is achievable from mel but computationally more expensive.

## References

### Primary Papers
- Plomp, R. & Levelt, W. J. M. (1965). Tonal consonance and critical bandwidth. JASA 38(4), 548-560.
- Sethares, W. A. (1993). Local consonance and the relationship between timbre and scale. JASA 94(3), 1218-1228.
- Terhardt, E. (1979). Calculating virtual pitch. Hearing Research 1(2), 155-182.
- Harrison, P. M. C. & Pearce, M. T. (2020). Simultaneous consonance in music perception and composition. Psychological Review 127(2), 216-244.
- Parncutt, R. (1989). Harmony: A Psychoacoustical Approach. Springer.
- Jensen, K. (1999). Timbre Models of Musical Sounds. PhD thesis, University of Copenhagen.

### Toolkit Implementations
- `essentia.Dissonance` -- Plomp-Levelt roughness model (requires spectral peaks)
- `essentia.Inharmonicity` -- harmonic deviation from raw audio
- `librosa.feature.spectral_flatness` -- related spectral statistics
