# ICEM F-Layer — Forecast (2D)

**Model**: ICEM (Information Content Emotion Model)
**Layer**: F (Forecast)
**Dimensions**: 2D [11:13]
**Scope**: external

---

## Dimensions

| Index | Name | Formula | Range |
|-------|------|---------|-------|
| 11 | F0:arousal_change_1_3s | σ(0.50×E1 + 0.30×onset_mean_500ms + 0.20×pitch_sal_mean_1s) | [0,1] |
| 12 | F1:valence_shift_2_5s | σ(0.40×E2 + 0.30×tonal_stab_mean_1s + 0.30×key_clarity_mean_500ms) | [0,1] |

## H³ Demands Consumed (4)

| Key | Feature | Purpose |
|-----|---------|---------|
| (11,8,1,0) | onset_strength 500ms mean memory | Sustained event context |
| (39,16,1,2) | pitch_salience 1s mean bidi | Sustained arousal context |
| (60,16,1,0) | tonal_stability 1s mean memory | Reused — valence pathway context |
| (51,8,1,0) | key_clarity 500ms mean memory | Sustained tonal grounding |

## Scientific Basis

- **Salimpoor 2011**: dopamine release in caudate during anticipation, NAc during peak pleasure (PET/fMRI, N=8).
- **Gold 2019**: pleasure depends on joint uncertainty and surprise (p<0.001).

## Implementation

File: `Musical_Intelligence/brain/functions/f2/mechanisms/icem/forecast.py`
