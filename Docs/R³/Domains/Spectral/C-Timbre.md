# Group C: Timbre [12:21] -- 9D

## Overview
- **Domain**: Spectral
- **Code**: `mi_beta/ear/r3/dsp/timbre.py`
- **Status**: EXISTING
- **Quality Tier**: Approximate (simple mel-band statistics; no perceptual weighting)
- **Pipeline Stage**: 1 (parallel, mel-only)
- **Class**: `TimbreGroup(BaseSpectralGroup)`

## Feature Table

| Index | Feature Name | Formula | Normalization | Cost | Psychoacoustic Basis | Quality |
|-------|-------------|---------|---------------|------|---------------------|---------|
| 12 | warmth | `mel[:, :N//4, :].sum() / mel.sum()` | ratio [0,1] | <0.1 ms | Low-frequency balance | Proxy (=[3]) |
| 13 | sharpness | `mel[:, 3*N//4:, :].sum() / mel.sum()` | ratio [0,1] | <0.1 ms | High-frequency weighting (not DIN 45692) | Proxy |
| 14 | tonalness | `mel.max(dim=1) / mel.sum(dim=1)` | ratio [0,1] | <0.1 ms | Terhardt peak dominance proxy | Proxy |
| 15 | clarity | `sum(k * mel[k]) / sum(mel[k]) / N` | /N -> [0,1] | <0.1 ms | Spectral centroid (misnomer: not C80) | Standard |
| 16 | spectral_smoothness | `1 - mean(\|mel[k]-mel[k+1]\|) / max` | complement [0,1] | <0.1 ms | Spectral envelope regularity | Derived (=1-[1]) |
| 17 | spectral_autocorrelation | `corr(mel[k], mel[k+1])` lag-1 | clamp(0,1) | <0.1 ms | Spectral periodicity | Duplicate (=[2]) |
| 18 | tristimulus1 | `mel[:, :N//3, :].sum() / mel.sum()` | ratio [0,1] | <0.1 ms | Fundamental strength (Pollard-Jansson 1982) | Proxy |
| 19 | tristimulus2 | `mel[:, N//3:2*N//3, :].sum() / mel.sum()` | ratio [0,1] | <0.1 ms | Mid-harmonic energy | Proxy |
| 20 | tristimulus3 | `mel[:, 2*N//3:, :].sum() / mel.sum()` | ratio [0,1] | <0.1 ms | High-harmonic energy | Proxy |

## Computation Pipeline

- **Input**: mel (B, 128, T) -- log-mel spectrogram
- **Dependencies**: None
- **Output**: (B, T, 9) -- all values in [0,1]
- **Estimated cost**: <0.1 ms/frame total
- **Warm-up**: None

### Detailed Computation Flow

```
mel (B, 128, T) -> transpose -> mel_t (B, T, 128)
  |
  +-- total_energy = mel_t.sum(dim=-1)
  |
  +-- [12] warmth = mel_t[:, :, :32].sum() / total_energy   (N//4 = 32)
  +-- [13] sharpness = mel_t[:, :, 96:].sum() / total_energy  (3*N//4 = 96)
  +-- [14] tonalness = mel_t.max() / total_energy
  +-- [15] clarity = (arange(128) * mel_t).sum() / total_energy / 128
  |
  +-- [16] spectral_smoothness:
  |     diff = torch.diff(mel_t, dim=-1).abs()
  |     irregularity = diff.mean() / max
  |     smoothness = 1.0 - irregularity
  |
  +-- [17] spectral_autocorrelation:
  |     centered = mel_t - mel_t.mean()
  |     normalized = centered / centered.norm()
  |     autocorr = (normalized[:-1] * normalized[1:]).sum().clamp(0, 1)
  |
  +-- [18] tristimulus1 = mel_t[:, :, :42].sum() / total_energy  (N//3 ~ 42)
  +-- [19] tristimulus2 = mel_t[:, :, 42:85].sum() / total_energy
  +-- [20] tristimulus3 = mel_t[:, :, 85:].sum() / total_energy
  |
  cat([12..20]) -> (B, T, 9) -> clamp(0, 1)
```

## PyTorch Implementation Notes

- **Key operations**: Slice + `torch.sum`, `torch.max`, `torch.mean`,
  `torch.diff`, `torch.abs`, `torch.arange` (for bin indices), `torch.norm`
- **Pre-computed matrices**: None
- **Warm-up requirements**: None
- **Code structure**: `TimbreGroup.compute(mel)` transposes to (B,T,N),
  computes total_energy once, then derives all 9 features

### Current Code Analysis

The existing `timbre.py` implements `TimbreGroup` with:
- `GROUP_NAME = "timbre"`, `OUTPUT_DIM = 9`, `INDEX_RANGE = (12, 21)`
- Band boundaries: `low_cutoff = N // 4`, `high_cutoff = 3 * N // 4`
- `total_energy = mel_t.sum(dim=-1, keepdim=True).clamp(min=1e-8)`
- `warmth` uses exact same formula as consonance.py `stumpf_fusion`
- `spectral_autocorrelation` uses identical lag-1 autocorrelation as
  consonance.py `_spectral_autocorrelation()`
- `spectral_smoothness` computes `1 - (irregularity / max)` which is the
  complement of sethares_dissonance's computation
- Tristimulus uses `N // 3` boundaries (42, 85 for N=128)

## Phase 6 Notes

### Known Issues

1. **Duplicate [12] = [3]**: `warmth` is identical to `stumpf_fusion` in Group A.
   Both compute `mel[:, :N//4, :].sum() / mel.sum()`. This is a birebir (exact)
   cross-group duplicate.

2. **Complement duplicate [16] = 1 - [1]**: `spectral_smoothness` computes
   `1 - (mean|diff| / max)`. This is the arithmetic complement of
   `sethares_dissonance`. Carries zero additional information.

3. **Identical duplicate [17] = [2]**: `spectral_autocorrelation` computes
   the exact same lag-1 autocorrelation as `helmholtz_kang`. Both use
   centered normalization + adjacent element-wise product + sum. The code
   in `timbre.py` lines 76-80 mirrors `_spectral_autocorrelation()` in
   `consonance.py` lines 93-109.

4. **Effective dimensionality**: ~4 independent features out of 9. After
   removing duplicates ([12],[16],[17]), warmth/tristimulus1/sharpness are
   partially correlated (all are band energy ratios).

### Phase 6 Revision Plan

| Index | Current | Phase 6 Target | Change |
|-------|---------|----------------|--------|
| 12 | warmth = low-quarter ratio | KEEP (warmth stays; [3] changes to real Parncutt) | No change |
| 13 | sharpness = high-quarter ratio | KEEP (K[122] provides real Zwicker sharpness) | No change |
| 14 | tonalness = max/sum ratio | KEEP (adequate as peak dominance proxy) | No change |
| 15 | clarity = spectral centroid/N | KEEP (rename in Phase 5 to spectral_centroid_norm) | Rename only |
| 16 | spectral_smoothness = 1-[1] | **spectral_spread** (2nd central moment of spectrum) | Formula replacement |
| 17 | spectral_autocorrelation = [2] | **spectral_kurtosis** (4th central moment) | Formula replacement |
| 18 | tristimulus1 | KEEP (mel-band proxy; adequate for spectral shape) | No change |
| 19 | tristimulus2 | KEEP | No change |
| 20 | tristimulus3 | KEEP | No change |

### Phase 6 New Formulas

**[16] spectral_spread** (2nd central moment):
```
centroid = sum(k * mel[k]) / sum(mel[k])
spread = sqrt(sum((k - centroid)^2 * mel[k]) / sum(mel[k])) / N
```

**[17] spectral_kurtosis** (4th central moment):
```
kurtosis = sum((k - centroid)^4 * mel[k]) / (sum(mel[k]) * spread^4) - 3
kurtosis_norm = sigmoid(kurtosis / 10)
```

### Phase 6 Priority: MEDIUM
Duplicate resolution is straightforward (formula swap). The replacement
features (spectral_spread, spectral_kurtosis) are well-established MIR
descriptors available in librosa and essentia.

## References

### Primary Papers
- Krimphoff, J. et al. (1994). Characterization of the timbre of complex sounds. JASA 95(5).
- Pollard, H. F. & Jansson, E. V. (1982). A tristimulus method for musical timbre. Acustica 51(3).
- Terhardt, E. (1979). Calculating virtual pitch. Hearing Research 1(2).
- Peeters, G. et al. (2011). The Timbre Toolbox: Audio descriptors of musical signals. JASA 130(5).

### Toolkit Implementations
- `librosa.feature.spectral_centroid` -- clarity reference
- `librosa.feature.spectral_bandwidth` -- spectral_spread equivalent
- `essentia.SpectralCentroidTime` -- spectral centroid
- `essentia.Tristimulus` -- partial-based tristimulus (requires peaks, not mel)
