# SSPS — Forecast

**Model**: Saddle-Shaped Preference Surface
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: γ
**Layer**: F — Forecast
**Dimensions**: 1D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 5 | optimal_zone_pred | Predicted movement toward an optimal zone on the saddle surface. Forecasts whether upcoming acoustic events will move the listener closer to or further from a preference peak. optimal_zone_pred = sigma(0.5 * f04_peak_proximity + 0.5 * saddle_value). Combines current peak proximity with the raw saddle interaction value to predict future preference trajectory. Gold 2023: VS shows RPE-like surprise x liking interaction consistent with predictive preference evaluation. |

---

## H3 Demands

The F-layer does not read additional H3 tuples beyond those consumed by the E-layer. It reuses the E-layer's saddle_value intermediate and the f04 output.

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| — | — | — | — | — | No additional H3 demands (reuses E-layer outputs) |

---

## Computation

The F-layer produces a single forward-looking prediction about the listener's trajectory on the preference surface. It combines:

- **f04_peak_proximity** (50% weight): Current proximity to an optimal zone peak -- the starting point for the prediction.
- **saddle_value** (50% weight): The raw IC x entropy interaction value (max of zone1, zone2) -- captures the underlying preference topology independent of smoothness modulation.

```
optimal_zone_pred = sigma(0.5 * f04 + 0.5 * saddle_value)
```

The prediction leverages the temporal dynamics built into the E-layer's H3 features. Because the E-layer reads IC velocity (H8, M8) and entropy trends (H16, M20), the saddle_value already encodes directional information about where the music is heading in IC x entropy space. The F-layer surfaces this directional signal as an explicit prediction.

High values indicate the music is predicted to move toward (or remain at) an optimal zone peak. Low values indicate predicted movement toward the saddle trough (the preference minimum between the two peaks). This prediction supports the preference assessment window (tau = 2.0s) by providing anticipatory information for downstream models.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f04 | Peak proximity | Current position baseline for prediction |
| E-layer saddle_value | Raw IC x entropy interaction | Directional preference topology signal |
| IMU (cross-unit) | Learning target | SSPS.optimal_zone_pred feeds IMU learning as optimal complexity target |
| DAED (intra-unit) | DA anticipation | Predicted peak approach drives anticipatory dopamine |
| Precision engine | pi_pred | Prediction confidence feeds precision weighting |
