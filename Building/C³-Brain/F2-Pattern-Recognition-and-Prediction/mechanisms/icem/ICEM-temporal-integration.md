# ICEM M-Layer — Temporal Integration (5D)

**Model**: ICEM (Information Content Emotion Model)
**Layer**: M (Memory)
**Dimensions**: 5D [4:9]
**Scope**: internal

---

## Dimensions

| Index | Name | Formula | Range |
|-------|------|---------|-------|
| 4 | M0:ic_value | σ(0.40×E0 + 0.25×pitch_class_entropy + 0.20×spectral_flux_std + 0.15×tonal_stab_entropy_1s) | [0,1] |
| 5 | M1:arousal_pred | σ(0.50×E0 + 0.50×E1) | [0,1] |
| 6 | M2:valence_pred | σ(0.50×(1−E0) + 0.50×E2) | [0,1] |
| 7 | M3:scr_pred | σ(0.50×E1 + 0.50×E3) | [0,1] |
| 8 | M4:hr_pred | σ(0.40×(1−E0) + 0.30×E2 + 0.30×consonance_std_500ms) | [0,1] |

## H³ Demands Consumed (4)

| Key | Feature | Purpose |
|-----|---------|---------|
| (21,3,2,2) | spectral_flux 100ms std bidi | IC magnitude variability |
| (4,8,2,0) | sensory_pleasantness 500ms std memory | Consonance stability for HR |
| (38,3,0,2) | pitch_class_entropy 100ms value bidi | Melodic unpredictability |
| (60,16,13,0) | tonal_stability 1s entropy memory | Structural uncertainty |

## Scientific Basis

- **Egermann 2013**: Linear IC-to-emotion mappings — Arousal = α·IC + β, Valence = -γ·IC + δ, SCR = ε·IC + ζ, HR = -η·IC + θ (all p<0.001).
- **Cheung 2019**: IC × entropy interaction β=-0.124, p<0.001; uncertainty modulates surprise-to-pleasure mapping.

## Implementation

File: `Musical_Intelligence/brain/functions/f2/mechanisms/icem/temporal_integration.py`
