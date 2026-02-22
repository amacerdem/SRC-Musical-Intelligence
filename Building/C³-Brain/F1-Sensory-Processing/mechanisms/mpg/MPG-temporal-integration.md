# MPG M-Layer — Temporal Integration (3D)

**Layer**: Memory (M)
**Indices**: [4:7]
**Scope**: internal

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|------------------|
| 4 | M0:activity_x | [0, 1] | Cortical gradient: α(0.7)×E0 + β(0.3)×E1 |
| 5 | M1:posterior_activity | [0, 1] | Onset encoding. σ(0.40×onset + 0.30×flux + 0.30×amplitude) |
| 6 | M2:anterior_activity | [0, 1] | Contour strength. σ(0.35×sharpness_vel + 0.35×pitch_height + 0.30×E2) |

---

## Cortical Gradient Function

```
Activity(x) = α·Onset(x=0,t)·exp(-x/λ_post) + β·Σ(Notes)·Contour·(1-exp(-x/λ_ant))

Parameters:
  α = 0.7 (posterior weighting)
  β = 0.3 (anterior weighting)
```

M0 is the weighted combination of posterior (E0) and anterior (E1) E-layer outputs.
M1 and M2 represent the separated posterior/anterior activation components.

---

## H³ Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (11, 0, 0, 2) | onset_strength instant | M1: onset |
| (21, 0, 0, 2) | spectral_flux instant | M1: flux |
| (13, 4, 8, 0) | sharpness velocity ~125ms | M2: pitch movement |
| (37, 3, 0, 2) | pitch_height ~100ms | M2: register |

---

## Scientific Foundation

- **Patterson 2002**: Activity moves anterolaterally from HG (pitch) to STG/PP (melody)
- **Norman-Haignere 2013**: Pitch-sensitive regions in anterior nonprimary AC
- **Briley 2013**: Spatial displacement of complex vs simple pitch sources

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/mpg/temporal_integration.py`
