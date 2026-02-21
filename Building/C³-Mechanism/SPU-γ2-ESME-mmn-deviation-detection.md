# MMN Deviation Detection (Pitch / Rhythm / Timbre)

**Source**: SPU-γ2-ESME (Expertise-Specific MMN Enhancement)
**Unit**: SPU (Spectral Processing Unit)
**Tier**: γ (Speculative)
**Score**: 7/10 — Temporal deviation with domain specificity

---

## Scientific Basis

- MMN (Mismatch Negativity) literature: Naatanen, Tervaniemi
- Expertise-dependent enhancement: singers (pitch), drummers (rhythm)

## Mechanism

Pre-attentive deviance detection via temporal deviation from running mean.
Three parallel channels (pitch, rhythm, timbre) with expertise-dependent gain.

### Formulas

```
Pitch MMN:
  pitch_dev = |H³(23, H3, M8, L0) - H³(2, H3, M1, L2)|
  f01 = σ(0.40·pitch_dev + 0.30·helmholtz_diff + 0.30·onset_val)

Rhythm MMN:
  onset_dev = |H³(11, H3, M0, L0)|
  f02 = σ(0.40·onset_dev + 0.30·spec_change_vel + 0.30·x_l4l5_val)

Timbre MMN:
  timbre_dev = H³(24, H8, M3, L0)  # timbre_change std
  f03 = σ(0.40·timbre_dev + 0.30·tristimulus_deviation)

Expertise enhancement:
  f04 = σ(α · max(f01, f02, f03))    α = trainable

Unified MMN-expertise:
  mmn = sqrt(f04 · max(f01, f02, f03))    # geometric mean
```

### Core Principle

Deviation = |current_value - running_mean|

This is the computational substrate of MMN: the brain maintains a running model
of recent stimuli and fires when a deviation exceeds threshold.

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| pitch_change_vel | H³(23, H3, M8, L0) | Pitch velocity at 100ms |
| helmholtz_val/mean | H³(2, H0/H3, M0/M1, L2) | Consonance instant vs mean |
| onset_val | H³(11, H3, M0, L0) | Onset strength |
| timbre_change_std | H³(24, H8, M3, L0) | Timbre variability at 300ms |
| tristimulus | H³ tristimulus values | Harmonic energy distribution |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| pitch_mmn | [0, 1] | Pitch deviance magnitude |
| rhythm_mmn | [0, 1] | Rhythm deviance magnitude |
| timbre_mmn | [0, 1] | Timbre deviance magnitude |
| expertise_factor | [0, 1] | Domain-specific enhancement |
| mmn_unified | [0, 1] | Geometric mean of expertise × max MMN |

## Why 7/10

- Deviation from running mean is a real computational mechanism
- Three parallel channels with max-pooling and geometric mean
- Expertise enhancement adds trainable gain
- But running mean comes from H³ (not internally maintained state)
- α parameter needs calibration
