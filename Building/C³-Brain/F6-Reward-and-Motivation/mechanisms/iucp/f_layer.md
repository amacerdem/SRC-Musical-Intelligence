# IUCP — Forecast

**Model**: Inverted-U Complexity Preference
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: β
**Layer**: F — Forecast
**Dimensions**: 1D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | optimal_zone_pred | Predicted preference zone. σ(0.5 * f04 + 0.5 * f03). Projects the listener's optimal complexity zone forward based on current interaction surface and optimal complexity estimate. High values predict music will remain in the preferred zone; low values predict drift away from optimal complexity. τ_decay = 2.0s (Gold 2019). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 33 | 16 | M20 (entropy) | L2 (bidi) | Coupling entropy 1s — via f03 interaction dynamics |
| 1 | 4 | 16 | M2 (std) | L2 (bidi) | Pleasantness variability 1s — via f04 hedonic flux |
| 2 | 21 | 16 | M1 (mean) | L2 (bidi) | Mean IC over 1s — via f01 -> f03 |
| 3 | 24 | 16 | M20 (entropy) | L2 (bidi) | Concentration entropy 1s — via f02 -> f03 |

---

## Computation

The F-layer forecasts whether the music will remain in the listener's preferred complexity zone. It combines:

1. **f04 (optimal complexity)**: The current estimate of where the listener's optimal zone lies, incorporating the interaction surface and hedonic variability.

2. **f03 (IC × entropy interaction)**: The interaction dynamics that shift the optimal zone. If the interaction is strong and complexity is near optimal, the prediction is high.

The τ_decay = 2.0s (Gold 2019) sets the relevant prediction horizon. This enables anticipatory reward modulation: DAED can scale anticipation dopamine based on predicted future preference. The signal is also relevant for IUCP's cross-unit pathway to IMU (complexity_target for learning).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer [2] | f03_ic_entropy_interaction | Interaction dynamics for zone prediction |
| E-layer [3] | f04_optimal_complexity | Current optimal zone estimate |
| R³ [21] | spectral_change | IC trajectory (via f01 -> f03) |
| R³ [24] | concentration_change | Entropy trajectory (via f02 -> f03) |
| R³ [4] | sensory_pleasantness | Hedonic variability (via f04) |
| R³ [33:41] | x_l4l5 | Coupling dynamics (via f03) |
| Gold 2019 | Inverted-U replicated across two studies | Predictable preference zones |
| Gold 2023b | VS anticipatory coding of preference | F(1,22) = 4.83, p = 0.039 |
| Cheung 2019 | NAcc reflects uncertainty (not surprise) | Anticipatory zone signal |
