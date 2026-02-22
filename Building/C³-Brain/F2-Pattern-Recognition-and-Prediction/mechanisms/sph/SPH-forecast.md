# SPH F-Layer — Forecast (3D)

**Model**: SPH (Spatiotemporal Prediction Hierarchy)
**Layer**: F (Forecast)
**Dimensions**: 3D [11:14]
**Scope**: external

---

## Dimensions

| Index | Name | Formula | Range |
|-------|------|---------|-------|
| 11 | F0:next_tone_pred_350ms | σ(0.40×E0 + 0.30×consonance_mean_1s + 0.30×pitch_height_vel_500ms) | [0,1] |
| 12 | F1:sequence_completion_2s | σ(0.40×tonal_stab_mean_1s + 0.30×spectral_auto_mean_1s + 0.30×chroma_mean_1s) | [0,1] |
| 13 | F2:decision_evaluation | σ(0.50×E2 + 0.50×tonal_stab_mean_1s) | [0,1] |

## H³ Demands Consumed (5, all reused from E)

| Key | Feature | Purpose |
|-----|---------|---------|
| (4,16,1,0) | sensory_pleasantness 1s mean memory | Long-range consonance context (reused) |
| (17,16,1,0) | spectral_autocorrelation 1s mean memory | Sustained feedforward context (reused) |
| (25,16,1,0) | chroma_C 1s mean memory | Long-range tonal context |
| (37,8,8,0) | pitch_height 500ms velocity memory | Melodic contour prediction |
| (60,16,1,0) | tonal_stability 1s mean memory | Long-range hierarchy template (reused) |

## Scientific Basis

- **Bonetti 2024**: Heschl→Hippocampus retrieval for next tone. Final tone reshapes hierarchy — cingulate assumes top position.
- **Rimmele 2021**: delta oscillations underpin phrase-level chunking.

## Implementation

File: `Musical_Intelligence/brain/functions/f2/mechanisms/sph/forecast.py`
