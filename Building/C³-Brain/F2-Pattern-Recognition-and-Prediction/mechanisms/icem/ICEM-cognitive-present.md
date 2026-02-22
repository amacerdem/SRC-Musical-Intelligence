# ICEM P-Layer — Cognitive Present (2D)

**Model**: ICEM (Information Content Emotion Model)
**Layer**: P (Present)
**Dimensions**: 2D [9:11]
**Scope**: hybrid

---

## Dimensions

| Index | Name | Formula | Range |
|-------|------|---------|-------|
| 9 | P0:surprise_signal | σ(0.35×M0 + 0.25×E0 + 0.20×spectral_flux_entropy + 0.20×loudness_100ms) | [0,1] |
| 10 | P1:emotional_evaluation | σ(0.30×M2 + 0.25×M1 + 0.25×key_clarity_100ms + 0.20×tonal_stab_500ms) | [0,1] |

## H³ Demands Consumed (4)

| Key | Feature | Purpose |
|-----|---------|---------|
| (21,3,13,2) | spectral_flux 100ms entropy bidi | Reused from E-layer — distributional surprise |
| (10,3,0,2) | loudness 100ms value bidi | Perceptual intensity for salience |
| (51,3,0,2) | key_clarity 100ms value bidi | Tonal grounding for evaluation |
| (60,8,0,0) | tonal_stability 500ms value memory | Structural stability context |

## Scientific Basis

- **Cheung 2019**: amygdala/hippocampus process uncertainty × surprise jointly (β_amyg=-0.140, p=0.004).
- **Gold 2019**: inverted-U for IC on liking — moderate IC maximizes pleasure (p<0.001).

## Implementation

File: `Musical_Intelligence/brain/functions/f2/mechanisms/icem/cognitive_present.py`
