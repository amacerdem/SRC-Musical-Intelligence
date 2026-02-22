# NSCP — Forecast

**Model**: Neural Synchrony Commercial Prediction
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: F — Forecast
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 8 | synchrony_pred | Neural synchrony prediction. Forecasts upcoming ISC levels by combining current neural synchrony with coherence periodicity trend. synchrony_pred = σ(0.5 * f22 + 0.5 * coherence_period_1s). Leeuwis 2021: ISC stability over time (early R² = 0.404 vs late R² = 0.393) supports temporal prediction of synchrony. |
| 9 | popularity_pred | Commercial success prediction. Forecasts upcoming popularity trajectory by combining current commercial prediction with binding periodicity. popularity_pred = σ(0.5 * f23 + 0.5 * binding_period_1s). Leeuwis 2021: combined model achieves R² = 0.619 for predicting streams from neural data. |
| 10 | catchiness_pred | Catchiness trajectory prediction. Forecasts whether the motor entrainment response will be sustained by combining current catchiness with onset periodicity. catchiness_pred = σ(0.5 * f24 + 0.5 * onset_period_1s). Spiech 2022: groove perception has stable temporal dynamics indexed by pupil drift rate. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 16 | M14 (periodicity) | L2 (bidi) | Coherence periodicity 1s for synchrony prediction |
| 1 | 33 | 16 | M14 (periodicity) | L2 (bidi) | Binding periodicity 1s for popularity prediction |
| 2 | 10 | 16 | M14 (periodicity) | L2 (bidi) | Onset periodicity 1s for catchiness prediction |
| 3 | 25 | 4 | M14 (periodicity) | L2 (bidi) | Coherence periodicity 125ms for short-term trend |
| 4 | 10 | 4 | M2 (std) | L2 (bidi) | Onset variability 125ms for catchiness stability |

---

## Computation

The F-layer generates three forward-looking predictions for the neural synchrony commercial pathway:

1. **Synchrony Prediction (dim 8)**: Forecasts the trajectory of inter-subject correlation. Combines the current ISC estimate (f22) with the 1s coherence periodicity to predict whether neural synchrony will be maintained. Regular coherence periodicity with high current synchrony predicts sustained ISC. Leeuwis 2021 showed ISC is temporally stable, supporting this predictive approach.

2. **Popularity Prediction (dim 9)**: Forecasts commercial success trajectory. Combines the current commercial prediction (f23) with binding periodicity at 1s to project whether the popularity-driving features will persist. Stable binding periodicity indicates sustained multi-feature coherence -- the acoustic signature that predicts continued listener engagement.

3. **Catchiness Prediction (dim 10)**: Forecasts the groove/motor entrainment trajectory. Combines current catchiness (f24) with onset periodicity at 1s to predict whether the rhythmic entrainment response will continue. Beat-regular passages with sustained catchiness predict extended motor engagement, which drives repeated listening and commercial success.

All F-layer dimensions combine E-layer features (current state) with 1s-horizon periodicity features (temporal regularity), consistent with the ISC prediction paradigm where temporal consistency predicts population-level response.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer [0] | f22_neural_synchrony | Current ISC for synchrony prediction |
| E-layer [1] | f23_commercial_prediction | Current popularity for popularity prediction |
| E-layer [2] | f24_catchiness_index | Current catchiness for catchiness prediction |
| R³ [10] | spectral_flux | Onset periodicity and variability for catchiness prediction |
| R³ [25:33] | x_l0l5 | Coherence periodicity for synchrony prediction |
| R³ [33:41] | x_l4l5 | Binding periodicity for popularity prediction |
| H³ | 5 tuples (see above) | Forward-looking periodicity and variability features |
