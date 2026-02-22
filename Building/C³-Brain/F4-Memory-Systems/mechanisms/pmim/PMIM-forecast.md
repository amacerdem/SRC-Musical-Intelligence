# PMIM F-Layer — Forecast (3D)

**Layer**: Future Predictions (F)
**Indices**: [8:11]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 8 | F0:eran_forecast_fc | [0, 1] | ERAN prediction (1-2s ahead). Based on harmony trajectory + entropy trend at H18 (2s phrase window). Forecasts whether upcoming harmonic events will conform to or violate stored syntax rules. Koelsch 2014: hierarchical predictive coding for music syntax; brain predicts upcoming chords based on tonal context. |
| 9 | F1:mmn_forecast_fc | [0, 1] | MMN prediction (0.5-1s ahead). Based on pred_error trajectory + flux trend at H14 (700ms progression window). Forecasts whether upcoming sensory events will match established echoic regularities. Garrido et al. 2009: forward connections carry PE, backward connections carry predictions (DCM/fMRI N=16). |
| 10 | F2:model_update_fc | [0, 1] | Model refinement forecast (2-5s ahead). Based on structural_expect trajectory at H18 (2s phrase window). Predicts how much the internal model will need to be updated — large anticipated PE = high model_update_fc. Gold et al. 2023: R-STG and ventral striatum reflect pleasure of musical expectancies (fMRI N=24). |

---

## Design Rationale

1. **ERAN Forecast (F0)**: Projects the expected syntax violation signal 1-2s ahead based on the current harmonic trajectory and entropy trend. Uses H18 (2s phrase window) to capture the scope of harmonic planning. When harmony is trending toward a tonic resolution, ERAN forecast is low (expected). When harmony is trending toward an unusual key area, ERAN forecast increases. This implements the top-down prediction arm of hierarchical predictive coding.

2. **MMN Forecast (F1)**: Projects the expected deviance detection signal 0.5-1s ahead based on prediction error trajectory and flux trend. Uses H14 (700ms progression window) matching the MMN temporal scope. Rapid flux acceleration predicts upcoming deviant events. This shorter forecast window matches the echoic memory timescale.

3. **Model Update Forecast (F2)**: Projects how much the predictive model will need updating over the next 2-5s. Based on structural expectation trajectory — when structural expectations are being violated (cadence not resolving, key modulation occurring), the model predicts high updating demand. This drives proactive resource allocation for memory encoding.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 18, 18, 0) | roughness trend H18 L0 | Dissonance trajectory for ERAN forecast |
| (22, 18, 13, 0) | entropy entropy H18 L0 | Higher-order unpredictability for model update |
| (21, 14, 8, 0) | spectral_flux velocity H14 L0 | Change acceleration for MMN forecast |
| (4, 18, 19, 0) | sensory_pleasantness stability H18 L0 | Consonance stability for model update forecast |
| (14, 14, 18, 0) | tonalness trend H14 L0 | Tonal trajectory for ERAN forecast |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | F0: dissonance trajectory for syntax forecast |
| [14] | tonalness | F0: tonal trend for ERAN projection |
| [21] | spectral_flux | F1: change trend for MMN forecast |
| [22] | entropy | F2: unpredictability for model update forecast |

---

## Scientific Foundation

- **Koelsch 2014**: Review, hierarchical predictive coding for music syntax; brain generates top-down predictions of upcoming harmonic events
- **Garrido et al. 2009**: DCM/fMRI N=16, forward connections carry PE, backward connections carry predictions; hierarchical predictive coding explains MMN
- **Gold et al. 2023**: fMRI N=24, R-STG and ventral striatum reflect pleasure of musical expectancies during naturalistic listening; uncertainty x surprise interaction in VS
- **Harding et al. 2025**: fMRI N=41, PE processing modulated by neuromodulatory state; vmPFC involvement in prediction error weighting
- **Egermann et al. 2013**: Behavioral N=50, IDyOM-predicted expectation violations correlate with subjective unexpectedness and autonomic arousal

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/pmim/forecast.py`
