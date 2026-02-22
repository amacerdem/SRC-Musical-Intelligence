# RASN F-Layer — Forecast (3D)

**Layer**: Future Predictions (F)
**Indices**: [8:11]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 8 | F0:movement_timing_pred | [0, 1] | Movement timing prediction (0.5-1s ahead). Motor cortex beat prediction trajectory. Uses beat_induction at H6 window for short-horizon temporal extrapolation. Grahn & Brett 2007: SMA predicts upcoming beat positions (fMRI N=27). |
| 9 | F1:neuroplastic_change_pred | [0, 1] | Neuroplastic change prediction (long-term). Hippocampal-cortical connectivity trajectory at H24 (36s). Extrapolates plasticity accumulation based on current entrainment quality and encoding strength. Blasi et al. 2025: structural neuroplasticity after >= 4 weeks (20 RCTs). |
| 10 | F2:gait_improvement_pred | [0, 1] | Gait improvement prediction (sessions ahead). Sensorimotor integration trajectory at H16 (1s). Projects motor recovery potential based on entrainment-motor coupling trends. Wang 2022: RAS improves gait velocity and stride (22 studies). |

---

## Design Rationale

1. **Movement Timing Prediction (F0)**: Forecasts upcoming beat positions based on current entrainment state and motor cortex prediction signals. Uses short-horizon (H6, 200ms) beat induction to project movement timing 0.5-1s ahead. This captures the SMA's role in beat prediction — anticipating the next beat before it arrives, which is fundamental to entrainment.

2. **Neuroplastic Change Prediction (F1)**: Projects long-term neuroplastic trajectory based on current plasticity indicators. Uses long-horizon (H24, 36s) retrieval dynamics to estimate the cumulative effect of ongoing rhythmic stimulation on neural reorganization. This captures the clinical evidence that >= 4 weeks of RAS produces measurable structural changes (hippocampal volume, white matter integrity).

3. **Gait Improvement Prediction (F2)**: Forecasts motor recovery potential based on sensorimotor integration trajectory. Uses medium-horizon (H16, 1s) motor entrainment signals to project expected gait parameter improvements. This connects the real-time entrainment quality to predicted clinical outcomes (velocity, stride length, cadence).

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 16, 0, 2) | sensory_pleasantness value H16 L2 | Current engagement for trajectory |
| (4, 20, 18, 0) | sensory_pleasantness trend H20 L0 | Engagement trajectory over 5s |
| (0, 16, 0, 2) | roughness value H16 L2 | Current dissonance for challenge level |
| (0, 20, 18, 0) | roughness trend H20 L0 | Dissonance trajectory over 5s |
| (10, 20, 1, 0) | spectral_flux mean H20 L0 | Average onset over 5s consolidation |
| (10, 24, 19, 0) | spectral_flux stability H24 L0 | Onset stability over 36s plasticity |
| (7, 20, 4, 0) | amplitude max H20 L0 | Peak energy over 5s |
| (7, 24, 3, 0) | amplitude std H24 L0 | Energy variability over 36s |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | F1: dissonance level for plasticity challenge |
| [4] | sensory_pleasantness | F1+F2: engagement level for prediction |
| [10] | spectral_flux | F0: onset trajectory for timing prediction |
| [7] | amplitude | F2: energy trajectory for gait prediction |

---

## Scientific Foundation

- **Grahn & Brett 2007**: fMRI N=27, SMA predicts beat positions (Z=5.03, FDR p<.05); putamen Z=5.67
- **Blasi et al. 2025**: Systematic review 20 RCTs N=718, structural neuroplasticity from rhythm interventions (hippocampal volume, WM integrity)
- **Wang 2022**: Meta-analysis, 22 studies — RAS improves walking function (gait velocity, stride length)
- **Zhao 2025**: Systematic review, 968+ patients — duration >= 4 weeks shows measurable changes
- **Thaut et al. 2015**: Rhythmic entrainment via reticulospinal pathways; beta oscillations modulated in SMA

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/rasn/forecast.py`
