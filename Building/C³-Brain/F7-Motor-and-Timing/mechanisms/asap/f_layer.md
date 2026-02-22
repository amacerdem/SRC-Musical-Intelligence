# ASAP — Forecast

**Model**: Action Simulation for Auditory Prediction
**Unit**: MPU-β1
**Function**: F7 Motor & Timing
**Tier**: β (Bridging)
**Layer**: F — Forecast
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 9 | beat_when_pred_0.5s | Next beat "when" prediction. beat_when_pred = σ(0.5 * f10 + 0.5 * beat_periodicity_1s). Predicts the likelihood that a beat will occur at the motor-predicted time point ~0.5s ahead. Combines the current beat prediction state (f10) with the sustained beat periodicity signal. Higher values indicate confident temporal prediction. Large et al. 2023: dynamic oscillator models predict optimal beat perception near 2 Hz (~500ms). Range [0, 1]. |
| 10 | simulation_pred | Motor simulation continuation prediction. simulation_pred = σ(0.5 * f11 + 0.5 * coupling_period_1s). Predicts whether the motor simulation will maintain or strengthen in the near future. Combines current simulation strength (f11) with sustained motor-auditory coupling periodicity. Thaut et al. 2015: period entrainment drives motor optimization — simulation persists when coupling is periodic. Range [0, 1]. |

---

## H³ Demands

This layer does not introduce additional H³ demands. It reuses tuples from E-layer and M-layer:
- beat_periodicity_1s: H³ tuple (10, 16, M14, L0) from E-layer
- coupling_period_1s: H³ tuple (25, 16, M14, L0) from M-layer

---

## Computation

The F-layer generates two forward-looking predictions about the state of the action simulation system.

**beat_when_pred_0.5s** predicts the next beat event timing. It averages the current beat prediction (f10, which captures how well the motor system has locked onto the rhythm) with the sustained beat periodicity signal (from H³). The logic is that future beat prediction depends both on the current prediction state and on the regularity of the underlying rhythm: highly periodic rhythms with strong current prediction yield confident beat forecasts.

**simulation_pred** predicts the continuation of the motor simulation process itself. It averages current simulation strength (f11) with coupling periodicity at 1s. This captures whether the motor-auditory coupling will sustain: if the coupling signal is periodic (regular bidirectional exchange) and the simulation is currently strong, the simulation is predicted to continue. This is important for downstream consumers (PEOM, STU) that need to know whether motor-based temporal prediction will be available in the near future.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f10 | Beat prediction state | Current prediction strength anchors beat forecast |
| E-layer f11 | Motor simulation state | Current simulation anchors continuation prediction |
| H³ (10, 16, M14, L0) | Beat periodicity 1s | Rhythmic regularity supports beat prediction |
| H³ (25, 16, M14, L0) | Coupling periodicity 1s | Coupling regularity supports simulation prediction |
| Downstream: PEOM | Prediction for entrainment | PEOM uses beat_when_pred for period locking |
| Downstream: STU | Temporal prediction signal | STU receives beat timing predictions |
