# ICEM E-Layer — Extraction (4D)

**Model**: ICEM (Information Content Emotion Model)
**Layer**: E (Extraction)
**Dimensions**: 4D [0:4]
**Scope**: internal

---

## Dimensions

| Index | Name | Formula | Range |
|-------|------|---------|-------|
| 0 | E0:information_content | σ(0.35×spectral_flux_entropy + 0.35×spectral_flux_100ms + 0.30×entropy_vel_100ms) | [0,1] |
| 1 | E1:arousal_response | σ(0.40×E0 + 0.30×pitch_sal_vel + 0.30×onset_100ms) | [0,1] |
| 2 | E2:valence_response | σ(0.40×(1−E0) + 0.30×tonal_stab_mean_1s + 0.30×consonance_100ms) | [0,1] |
| 3 | E3:defense_cascade | σ(0.50×E0×E1 + 0.50×loudness_vel_1s) | [0,1] |

## H³ Demands Consumed (8)

| Key | Feature | Purpose |
|-----|---------|---------|
| (21,3,0,2) | spectral_flux 100ms value bidi | Raw spectral change for IC |
| (21,3,13,2) | spectral_flux 100ms entropy bidi | Distributional unpredictability |
| (22,3,8,0) | distribution_entropy 100ms velocity memory | Rate of distributional change |
| (11,3,0,2) | onset_strength 100ms value bidi | Event detection for arousal |
| (10,16,8,2) | loudness 1s velocity bidi | Defense cascade trigger |
| (4,3,0,2) | sensory_pleasantness 100ms value bidi | Consonance for valence |
| (39,4,8,0) | pitch_salience 125ms velocity memory | Mid-level arousal pathway |
| (60,16,1,0) | tonal_stability 1s mean memory | Valence context |

## Scientific Basis

- **Egermann 2013**: IC peaks (IDyOM) → arousal↑, valence↓, SCR↑, HR↓ (p<0.001, N=50 live concert).
- **Cheung 2019**: uncertainty × surprise interaction (R²=0.654, fMRI N=79).

## Implementation

File: `Musical_Intelligence/brain/functions/f2/mechanisms/icem/extraction.py`
