# SPH P-Layer — Cognitive Present (3D)

**Model**: SPH (Spatiotemporal Prediction Hierarchy)
**Layer**: P (Present)
**Dimensions**: 3D [8:11]
**Scope**: hybrid

---

## Dimensions

| Index | Name | Formula | Range |
|-------|------|---------|-------|
| 8 | P0:memory_match | σ(0.40×M0 + 0.30×M2 + 0.30×pitch_sal_100ms) | [0,1] |
| 9 | P1:prediction_error | σ(0.40×M1 + 0.30×M3 + 0.30×entropy_vel_125ms) | [0,1] |
| 10 | P2:deviation_detection | σ(0.35×spectral_flux_100ms + 0.25×onset_100ms + 0.20×amplitude_100ms + 0.20×pitch_height_100ms) | [0,1] |

## H³ Demands Consumed (6, 1 reused from E)

| Key | Feature | Purpose |
|-----|---------|---------|
| (7,3,0,2) | amplitude 100ms value bidi | Deviation detection |
| (11,3,0,2) | onset_strength 100ms value bidi | Deviation onset |
| (21,3,0,2) | spectral_flux 100ms value bidi | Spectral deviation (reused) |
| (22,4,8,0) | distribution_entropy 125ms velocity memory | Distributional change rate |
| (37,3,0,2) | pitch_height 100ms value bidi | Pitch deviation |
| (39,3,0,2) | pitch_salience 100ms value bidi | Pitch clarity for match |

## Scientific Basis

- **Bonetti 2024**: hippocampus memory match/mismatch comparison. Prediction error strongest at the tone introducing variation.
- **Carbajal & Malmierca 2018**: prediction error propagates IC→MGB→AC.

## Implementation

File: `Musical_Intelligence/brain/functions/f2/mechanisms/sph/cognitive_present.py`
