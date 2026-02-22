# OII F-Layer — Forecast (2D)

**Layer**: Future Predictions (F)
**Indices**: [8:10]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 8 | F0:integration_pred | [0, 1] | Integration mode prediction (1-2s ahead). sigma(0.25 * struct_expect + 0.20 * fusion_h18). |w| sum = 0.45. Structural expectation trajectory — projects whether the brain will shift toward integration mode based on upcoming harmonic closure and binding trends. Bruzzone et al. 2022: theta/alpha integration patterns track cognitive state across time (MEG N=66). |
| 9 | F1:segregation_pred | [0, 1] | Segregation mode prediction (0.5-1s ahead). sigma(0.20 * entropy_h14 + 0.20 * onset_velocity_h14). |w| sum = 0.40. Projects whether upcoming input will demand local gamma processing based on entropy and onset trajectories. Samiee et al. 2022: cross-frequency PAC dynamics shift with stimulus properties (MEG N=16). |

---

## Design Rationale

1. **Integration Prediction (F0)**: Forecasts the upcoming integration state 1-2s ahead based on structural expectation trajectory and binding quality trends. Uses H18 (2s phrase window) because integration operates at the phrase level — theta oscillations bind information across the full harmonic arc. When structural expectations point toward cadential resolution (high binding trend), integration mode is predicted. Uses stumpf fusion at H18 as the binding trajectory indicator.

2. **Segregation Prediction (F1)**: Forecasts the upcoming segregation demand 0.5-1s ahead based on entropy and onset velocity trajectories. Uses H14 (700ms progression window) matching the faster timescale of gamma-band processing. When entropy is increasing (more complex local structure) and onset velocity is high (many transient events), the model predicts the brain will shift toward segregation mode. This shorter horizon reflects that gamma transitions are faster than theta transitions.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 18, 1, 0) | stumpf_fusion mean H18 L0 | Phrase-level binding stability for integration forecast |
| (22, 14, 1, 0) | entropy mean H14 L0 | Average complexity trajectory for segregation forecast |
| (11, 14, 8, 0) | onset_strength velocity H14 L0 | Mode switch rate trajectory for segregation forecast |
| (21, 18, 1, 0) | spectral_flux mean H18 L0 | Average transition rate for integration forecast |
| (15, 18, 3, 0) | spectral_centroid std H18 L0 | Frequency balance variability for mode prediction |
| (0, 24, 1, 0) | roughness mean H24 L0 | Average dissonance over 36s episodic chunk |
| (7, 16, 8, 0) | amplitude velocity H16 L0 | Energy change rate for switch prediction |
| (7, 20, 4, 0) | amplitude max H20 L0 | Peak energy over 5s consolidation |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | F1: gamma demand trajectory |
| [3] | stumpf_fusion | F0: binding quality trajectory |
| [7] | amplitude | F0+F1: energy trajectory for mode prediction |
| [15] | spectral_centroid | F0: frequency balance for integration prediction |
| [22] | entropy | F1: complexity trajectory for segregation forecast |

---

## Scientific Foundation

- **Bruzzone et al. 2022**: DTI + MEG N=66/67, theta/alpha integration patterns track cognitive state; DTI structural degree p=0.007 confirms long-range white matter supports integration mode
- **Samiee et al. 2022**: MEG N=16, cross-frequency PAC dynamics (delta-beta) shift with stimulus properties; directed connectivity shows bottom-up delta and top-down beta
- **Cabral et al. 2022**: Computational model, metastable oscillatory modes — frequency, duration, scale controlled by coupling parameters; predicts mode transitions
- **Ding et al. 2025**: EEG N=31, 6 Hz boundary for theta-alpha transition; entrainment rate determines oscillatory mode

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/oii/forecast.py`
