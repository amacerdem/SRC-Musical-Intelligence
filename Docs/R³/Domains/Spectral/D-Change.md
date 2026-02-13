# Group D: Change [21:25] -- 4D

## Overview
- **Domain**: Spectral
- **Code**: `mi_beta/ear/r3/dsp/change.py`
- **Status**: EXISTING
- **Quality Tier**: Standard ([21],[22],[23]) / Proxy ([24] -- bugged normalization)
- **Pipeline Stage**: 1 (parallel, mel-only)
- **Class**: `ChangeGroup(BaseSpectralGroup)`

## Feature Table

| Index | Feature Name | Formula | Normalization | Cost | Psychoacoustic Basis | Quality |
|-------|-------------|---------|---------------|------|---------------------|---------|
| 21 | spectral_flux | `\|\|mel[:,t] - mel[:,t-1]\|\|_2 / max` | max-norm (batch) | <0.1 ms | Frame-to-frame spectral change | Standard |
| 22 | distribution_entropy | `-sum(p * log(p)) / log(128)` | /log(N) -> [0,1] | <0.1 ms | Shannon spectral uniformity | Standard |
| 23 | distribution_flatness | `exp(mean(log(p))) / mean(p)` | natural [0,1] | <0.1 ms | Wiener entropy / MPEG-7 flatness | Standard |
| 24 | distribution_concentration | `sum(p^2) * N` -> clamp(0,1) | BUG: clamp(0,1) | <0.1 ms | Herfindahl-Hirschman Index | Proxy (bugged) |

## Computation Pipeline

- **Input**: mel (B, 128, T) -- log-mel spectrogram
- **Dependencies**: None
- **Output**: (B, T, 4) -- all values in [0,1]
- **Estimated cost**: <0.1 ms/frame total
- **Warm-up**: None (spectral_flux is zero for frame 0; subsequent frames immediate)

### Detailed Computation Flow

```
mel (B, 128, T) -> transpose -> mel_t (B, T, 128)
  |
  +-- [21] spectral_flux:
  |     diff = mel_t[:, 1:] - mel_t[:, :-1]
  |     flux = diff.norm(dim=-1)                    # L2 norm
  |     flux_norm = flux / flux.max()                # max-normalize
  |     (frame 0 padded with zero)
  |
  +-- prob = mel_t / mel_t.sum(dim=-1)              # normalize to distribution
  |     prob = prob.clamp(min=1e-10)
  |
  +-- [22] distribution_entropy:
  |     H = -(prob * prob.log()).sum(dim=-1)
  |     entropy_norm = H / log(128)                  # max entropy = log(N)
  |
  +-- [23] distribution_flatness:
  |     log_mean = prob.log().mean(dim=-1)
  |     arith_mean = prob.mean(dim=-1)
  |     flatness = log_mean.exp() / arith_mean       # Wiener entropy
  |     flatness = flatness.clamp(0, 1)
  |
  +-- [24] distribution_concentration:
        HHI = prob.pow(2).sum(dim=-1)                # Herfindahl index
        concentration = HHI * N                       # BUG: scale by N
        concentration = concentration.clamp(0, 1)     # BUG: both extremes -> 1.0
  |
  cat([21..24]) -> (B, T, 4) -> clamp(0, 1)
```

## PyTorch Implementation Notes

- **Key operations**: `torch.norm` (L2), `torch.log`, `torch.exp`,
  `torch.pow(2)`, `torch.sum`, `torch.mean`
- **Pre-computed matrices**: None
- **Warm-up requirements**: spectral_flux [21] is zero at t=0 (no previous
  frame). All other features are instantaneous.
- **Probability normalization**: All distribution features ([22]-[24]) first
  convert mel to a probability distribution: `p = mel / sum(mel)`.
  Uses `clamp(min=1e-10)` to avoid log(0).

### Current Code Analysis

The existing `change.py` implements `ChangeGroup` with:
- `GROUP_NAME = "change"`, `OUTPUT_DIM = 4`, `INDEX_RANGE = (21, 25)`
- Flux uses `diff.norm(dim=-1)` (L2 norm) with frame-level max normalization
- Entropy uses softmax-style probability then `-p * p.log()` summed, divided
  by `log(N)` where N is the number of mel bins (128)
- Flatness implements Wiener entropy: `exp(mean(log(p))) / mean(p)`
- Concentration computes `p.pow(2).sum() * N` then clamps to [0,1]

## Phase 6 Notes

### Known Bugs

1. **[24] concentration normalization bug** (CRITICAL):
   - **Current formula**: `concentration = sum(p^2) * N`
   - **Uniform distribution**: each `p_k = 1/N`, so `sum(p^2) = N * (1/N)^2 = 1/N`,
     then `* N = 1.0` -- clamp gives 1.0
   - **Single peak**: one `p_k = 1.0`, so `sum(p^2) = 1`, then `* N = 128`,
     clamp gives 1.0
   - **Both extremes map to 1.0** -- the feature cannot distinguish uniform
     from concentrated spectra
   - **Correct formula**: `(HHI - 1/N) / (1 - 1/N)` maps to 0=uniform, 1=concentrated

### High Correlation

2. **[22] entropy and [23] flatness correlation**: Both measure spectral
   uniformity. Shannon entropy and Wiener entropy (geometric/arithmetic mean
   ratio) are highly correlated for smooth distributions. Empirical correlation
   is typically >0.9 for music signals.
   - This is a known redundancy but both are retained because:
     - Entropy is standard in information theory
     - Flatness is the MPEG-7 standard descriptor
     - Their behavior diverges for sparse/peaky spectra

### Phase 6 Revision Plan

| Index | Current | Phase 6 Target | Change |
|-------|---------|----------------|--------|
| 21 | spectral_flux (L2) | KEEP -- well-validated spectral change measure | No change |
| 22 | distribution_entropy | KEEP -- standard Shannon measure | No change |
| 23 | distribution_flatness | KEEP -- MPEG-7 standard, slight divergence from [22] | No change |
| 24 | distribution_concentration | Fix: `(HHI - 1/N) / (1 - 1/N)` | Formula fix |

### [24] Corrected Implementation

```python
# CURRENT (bugged):
concentration = prob.pow(2).sum(dim=-1, keepdim=True) * N
concentration = concentration.clamp(0, 1)

# FIXED (Phase 6):
HHI = prob.pow(2).sum(dim=-1, keepdim=True)
inv_N = 1.0 / N
concentration = (HHI - inv_N) / (1.0 - inv_N)
concentration = concentration.clamp(0, 1)
```

### Phase 6 Priority: HIGH (for [24] bug fix), LOW (for [22]-[23] correlation)

The [24] bug is one of two critical normalization errors in the existing R3
implementation (the other being [10] loudness double compression in Group B).

## References

### Primary Papers
- MPEG-7 Audio Standard (ISO/IEC 15938-4). Spectral flatness measure.
- Shannon, C. E. (1948). A mathematical theory of communication. Bell System Technical Journal.
- Herfindahl, O. C. (1950). Concentration in the U.S. Steel Industry. (economic concentration index adapted for spectral analysis)
- Weineck, K. et al. (2022). Neural correlates of spectral flux in music perception. NeuroImage.

### Toolkit Implementations
- `librosa.feature.spectral_flatness` -- Wiener entropy
- `librosa.onset.onset_strength` -- spectral flux variant
- `essentia.Flux` -- spectral flux
- `essentia.FlatnessDB` -- spectral flatness in dB
