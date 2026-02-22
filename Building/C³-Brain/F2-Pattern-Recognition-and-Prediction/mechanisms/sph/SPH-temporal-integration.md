# SPH M-Layer — Temporal Integration (4D)

**Model**: SPH (Spatiotemporal Prediction Hierarchy)
**Layer**: M (Memory)
**Dimensions**: 4D [4:8]
**Scope**: internal

---

## Dimensions

| Index | Name | Formula | Range |
|-------|------|---------|-------|
| 4 | M0:match_response | σ(0.40×E0 + 0.30×consonance_100ms + 0.30×tonal_stab_mean_500ms) | [0,1] |
| 5 | M1:varied_response | σ(0.40×E1 + 0.30×amplitude_std_100ms + 0.30×spectral_flux_std_100ms) | [0,1] |
| 6 | M2:gamma_power | σ(0.50×E0 + 0.50×sensory_pleasantness_R3) | [0,1] |
| 7 | M3:alpha_beta_power | σ(0.50×E1 + 0.50×(1 − sensory_pleasantness_R3)) | [0,1] |

## H³ Demands Consumed (4, 2 reused from E)

| Key | Feature | Purpose |
|-----|---------|---------|
| (4,3,0,2) | sensory_pleasantness 100ms value bidi | Memory match indicator (reused) |
| (7,3,2,2) | amplitude 100ms std bidi | Amplitude variability for mismatch |
| (21,3,2,2) | spectral_flux 100ms std bidi | Spectral change variability (reused) |
| (60,8,1,0) | tonal_stability 500ms mean memory | Mid-range structural context |

## R³ Direct Reads

| Index | Feature | Purpose |
|-------|---------|---------|
| [4] | sensory_pleasantness | Modulates gamma/alpha-beta balance |

## Scientific Basis

- **Bonetti 2024**: memorised → positive ~350ms (M0), varied → negative ~250ms (M1). Gamma power M>N (M2), alpha-beta power N>M (M3).

## Implementation

File: `Musical_Intelligence/brain/functions/f2/mechanisms/sph/temporal_integration.py`
