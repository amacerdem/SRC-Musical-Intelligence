# MPG E-Layer — Extraction (4D)

**Layer**: Extraction (E)
**Indices**: [0:4]
**Scope**: internal
**Activation**: sigmoid (coefficient saturation rule: |wi| ≤ 1.0)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|------------------|
| 0 | E0:onset_posterior | [0, 1] | Posterior AC dominance at onset. σ(0.40×onset_strength + 0.35×flux + 0.25×amplitude) |
| 1 | E1:sequence_anterior | [0, 1] | Anterior AC activation for contour. σ(0.35×sharpness_velocity + 0.35×pitch_height_trend + 0.30×pitch_height) |
| 2 | E2:contour_complexity | [0, 1] | Melodic complexity index. σ(0.35×pitch_height_trend + 0.35×sharpness_std + 0.30×pitch_salience_velocity) |
| 3 | E3:gradient_ratio | [0, 1] | Posterior/anterior ratio. E0/(E0+E1+ε) |

---

## H³ Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (11, 0, 0, 2) | onset_strength instant | E0: onset detection |
| (21, 3, 0, 2) | spectral_flux ~100ms | E0: spectral change |
| (7, 3, 0, 2) | amplitude ~100ms | E0: energy context |
| (13, 4, 8, 0) | sharpness velocity ~125ms | E1: pitch velocity |
| (37, 4, 18, 2) | pitch_height trend ~125ms | E1+E2: contour direction |
| (37, 3, 0, 2) | pitch_height ~100ms | E1: register context |
| (13, 3, 2, 2) | sharpness std ~100ms | E2: brightness variability |
| (39, 3, 8, 0) | pitch_salience velocity | E2: pitch presence dynamics |

---

## R³ Ontology Mapping

| Old v1 | New 97D | Change |
|--------|---------|--------|
| onset_strength [11] | onset_strength [11] | unchanged |
| spectral_flux [10] | spectral_flux [21] | Group B→D |
| amplitude [7] | amplitude [7] | unchanged |
| brightness [13] | sharpness [13] | renamed |
| pitch_change [23] | pitch_height [37] | dissolved → replacement |
| x_l4l5 [33] | pitch_salience [39] | dissolved → replacement |

---

## Scientific Foundation

- **Rupp 2022**: MEG (n=20) — posterior→anterior gradient for melodic contours
- **Patterson 2002**: fMRI — pitch in lateral HG, melody extends to STG/PP
- **Briley 2013**: EEG — IRN sources 7mm lateral/anterior to pure-tone

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/mpg/extraction.py`
