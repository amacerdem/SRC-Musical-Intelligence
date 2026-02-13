# Group B: Energy [7:12] -- 5D

## Overview
- **Domain**: Temporal
- **Code**: `mi_beta/ear/r3/dsp/energy.py`
- **Status**: EXISTING
- **Quality Tier**: Standard ([7],[8],[9],[11]) / Proxy ([10] -- double-compression bug)
- **Pipeline Stage**: 1 (parallel, mel-only)
- **Class**: `EnergyGroup(BaseSpectralGroup)`

## Feature Table

| Index | Feature Name | Formula | Normalization | Cost | Psychoacoustic Basis | Quality |
|-------|-------------|---------|---------------|------|---------------------|---------|
| 7 | amplitude | `mel.pow(2).mean(dim=1).sqrt()` | max-norm (batch) | <0.1 ms | RMS energy (double-compressed from log-mel) | Standard* |
| 8 | velocity_A | `sigmoid((amp[t] - amp[t-1]) * 5.0)` | sigmoid (gain=5) | <0.1 ms | Energy change rate (attack/decay) | Standard |
| 9 | acceleration_A | `sigmoid((vel[t] - vel[t-2]) * 5.0)` | sigmoid (gain=5) | <0.1 ms | Energy buildup curvature | Standard |
| 10 | loudness | `amplitude^0.3 / max` | max-norm | <0.01 ms | Stevens' law sone approximation | Proxy (BUG) |
| 11 | onset_strength | `relu(mel[t] - mel[t-1]).sum() / max` | max-norm | <0.1 ms | HWR spectral flux (Weineck 2022) | Reference |

*Note: amplitude is RMS of log-mel values, not linear power. See Phase 6 notes.

## Computation Pipeline

- **Input**: mel (B, 128, T) -- log-mel spectrogram
- **Dependencies**: None (B[11] is consumed by Group G and Group I)
- **Output**: (B, T, 5) -- all values in [0,1]
- **Estimated cost**: <0.1 ms/frame total
- **Warm-up**: None (velocity is zero at t=0; acceleration is zero at t=0,t=T-1)

### Detailed Computation Flow

```
mel (B, 128, T)
  |
  +-- [7] amplitude:
  |     amp = mel.pow(2).mean(dim=1).sqrt()       # (B, T) RMS per frame
  |     amp_norm = amp / amp.max()                 # batch-level max-norm
  |
  +-- [8] velocity_A:
  |     vel = amp_norm[t] - amp_norm[t-1]          # first difference
  |     vel_norm = sigmoid(vel * 5.0)              # sigmoid with gain=5
  |     (t=0 padded with zero)
  |
  +-- [9] acceleration_A:
  |     acc = vel[t] - vel[t-2]                    # second difference (stride 2)
  |     acc_norm = sigmoid(acc * 5.0)
  |     (t=0, t=T-1 padded with zero)
  |
  +-- [10] loudness:
  |     loud = amp.pow(0.3)                        # Stevens' law
  |     loud_norm = loud / loud.max()              # BUG: amp is from log-mel
  |
  +-- [11] onset_strength:
        flux = relu(mel[:,:,t] - mel[:,:,t-1])     # positive spectral flux
        onset = flux.sum(dim=1)                    # sum across mel bins
        onset_norm = onset / onset.max()           # batch-level max-norm
  |
  stack([7..11]) -> (B, T, 5) -> clamp(0, 1)
```

## PyTorch Implementation Notes

- **Key operations**: `torch.pow`, `torch.mean`, `torch.sqrt`, `torch.sigmoid`,
  `torch.relu`, `torch.sum`, `torch.clamp`
- **Pre-computed matrices**: None
- **Warm-up requirements**: None (edge frames padded with zeros)
- **Code structure**: `EnergyGroup.compute(mel)` computes amplitude first,
  then derives velocity, acceleration, and loudness from it. Onset strength
  is independent (directly from mel frame differences).

### Current Code Analysis

The existing `energy.py` implements `EnergyGroup` with:
- `GROUP_NAME = "energy"`, `OUTPUT_DIM = 5`, `INDEX_RANGE = (7, 12)`
- Amplitude: `mel.pow(2).mean(dim=1).sqrt()` -- RMS across 128 mel bins per frame
- Velocity: `amplitude_norm[:, 1:] - amplitude_norm[:, :-1]` with `sigmoid(x * 5.0)`
- Acceleration: `velocity[:, 2:] - velocity[:, :-2]` with `sigmoid(x * 5.0)`
  Note: uses raw velocity (before sigmoid), stride of 2
- Loudness: `amplitude.pow(0.3)` with max-normalization
- Onset: `flux.clamp(min=0).sum(dim=1)` -- half-wave rectified spectral flux

### Onset Strength as Key Output

Feature [11] onset_strength is the most important output of Group B because:
1. It feeds Group G (Rhythm) for all tempo/beat/syncopation analysis
2. It feeds Group I (Information) for rhythmic_information_content
3. It is the strongest predictor of neural synchronization (Weineck 2022)

The onset formula (HWR spectral flux) is well-validated and does not require
Phase 6 revision.

## Phase 6 Notes

### Known Bugs

1. **[10] loudness -- Stevens' law double compression** (CRITICAL):
   - **The bug**: `amplitude` is computed from log-mel spectrogram.
     Log-mel values are already logarithmically compressed (dB-like scale).
     Applying Stevens' power law (`x^0.3`) on top of logarithmic values
     creates a double compression: `(log(power))^0.3` instead of the
     correct `power^0.3`.
   - **Effect**: Dynamic range is severely compressed. Quiet and loud passages
     become less distinguishable. The feature loses discriminative power at
     both extremes of the loudness range.
   - **Correct formula**: `loudness = exp(log_mel).pow(0.3)` -- first undo
     the log, then apply Stevens' law. Or use the full Zwicker ISO 532-1
     specific loudness model.
   - **Note**: K[124] `loudness_a_weighted` provides an alternative loudness
     measure with A-weighting that avoids this bug by applying weights to
     `exp(mel)` (linear domain).

2. **[7] amplitude -- double compression** (MODERATE):
   - RMS of log-mel values is not physically meaningful (RMS should be
     computed on linear power values). However, the max-normalization
     partially compensates, making this a relative measure. Less critical
     than the loudness bug.

3. **[8],[9] velocity/acceleration -- sigmoid normalization** (MINOR):
   - Sigmoid with gain=5 maps to approximately [-2.5, +2.5] in linear
     range before compression. This loses the absolute magnitude of
     energy changes. Physical interpretability is reduced.
   - Phase 6 alternative: min-max or percentile normalization.

### Phase 6 Revision Plan

| Index | Current | Phase 6 Target | Change |
|-------|---------|----------------|--------|
| 7 | amplitude = RMS(log_mel) | `exp(log_mel).pow(2).mean().sqrt()` or keep as relative | Formula fix |
| 8 | velocity = sigmoid(damp * 5) | Percentile normalization or adaptive gain | Normalization fix |
| 9 | acceleration = sigmoid(dvel * 5) | Same as velocity | Normalization fix |
| 10 | loudness = RMS(log_mel)^0.3 | `exp(log_mel).mean().pow(0.3)` or Zwicker ISO 532-1 | Formula fix (CRITICAL) |
| 11 | onset_strength = HWR flux | KEEP -- well-validated, no change needed | No change |

### Phase 6 Corrected Loudness

```python
# CURRENT (bugged):
amplitude = mel.pow(2).mean(dim=1).sqrt()
loudness = amplitude.pow(0.3) / max

# OPTION A (minimal fix):
mel_linear = mel.exp()  # log-mel -> linear power
loudness = mel_linear.mean(dim=1).pow(0.3)
loudness_norm = loudness / loudness.max()

# OPTION B (full Zwicker, higher cost):
# Requires Bark-band specific loudness computation
# See ISO 532-1 for the complete algorithm
```

### Phase 6 Priority: HIGH (for [10] loudness fix)
The loudness double compression is one of two critical normalization bugs
in the R3 implementation (the other being [24] concentration in Group D).

## References

### Primary Papers
- Stevens, S. S. (1957). On the psychophysical law. Psychological Review 64(3), 153-181.
- Zwicker, E. & Fastl, H. (1999). Psychoacoustics: Facts and Models. Springer.
- ISO 532-1:2017. Methods for calculating loudness -- Part 1: Zwicker method.
- Weineck, K. et al. (2022). Neural correlates of spectral flux in music perception. NeuroImage 261.
- Bello, J. P. et al. (2005). A tutorial on onset detection in music signals. IEEE Trans. Speech & Audio Processing 13(5).

### Toolkit Implementations
- `librosa.feature.rms` -- RMS energy
- `librosa.onset.onset_strength` -- spectral flux onset function
- `essentia.Loudness` -- EBU R128 loudness
- `essentia.OnsetDetection` -- multiple onset detection methods
