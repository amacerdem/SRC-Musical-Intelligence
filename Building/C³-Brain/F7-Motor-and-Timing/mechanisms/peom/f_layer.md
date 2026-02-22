# PEOM — Forecast

**Model**: Period Entrainment Optimization Model
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: F — Forecast
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 9 | next_beat_pred_T | Next beat onset prediction (T ahead). Predicts when the next beat will occur based on current period lock. σ(0.5 * f01 + 0.5 * beat_periodicity_1s). Thaut 1998b: motor period entrains even during subliminal tempo changes; Repp 2005: period correction as distinct predictive mechanism. |
| 10 | velocity_profile_pred | Velocity profile prediction 0.5T ahead. Predicts the upcoming velocity profile shape based on current coupling. σ(0.5 * f02 + 0.5 * coupling_periodicity_1s). Thaut 2015: CTR enables anticipatory velocity planning; Ross & Balasubramaniam 2022: motor simulation for prediction. |

---

## H³ Demands

No additional H³ demands beyond those already consumed by E and M layers. The F-layer reuses:
- beat_periodicity_1s from (10, 16, 14, 2)
- coupling_periodicity_1s from (25, 16, 14, 2)

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| — | — | — | — | — | No unique H³ demands; reuses E/M layer tuples |

---

## Computation

The F-layer generates predictions about upcoming motor states:

1. **Next beat prediction** (idx 9): Combines the current period entrainment level (f01) with the beat periodicity signal at 1s to predict the next beat onset. When entrainment is strong (f01 high) and periodicity is stable, the prediction confidence is high. This implements the anticipatory period correction mechanism from Repp (2005) and the predictive motor timing from Thaut (1998b). Equal weighting (0.5/0.5) reflects that both internal entrainment state and external periodicity contribute equally to beat prediction.

2. **Velocity profile prediction** (idx 10): Combines the current velocity optimization (f02) with coupling periodicity at 1s to predict the velocity profile half a period ahead. This enables anticipatory motor preparation — the motor system pre-shapes the velocity trajectory before the next beat arrives. Maps to the sensorimotor simulation framework (Ross & Balasubramaniam 2022) where covert motor imagery generates predictions.

Both outputs are sigmoid-bounded to [0, 1] and represent confidence in future-state predictions.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_period_entrainment | Entrainment level feeds beat prediction confidence |
| E-layer | f02_velocity_optimization | Velocity state feeds profile prediction |
| H³ (shared) | beat_periodicity_1s, coupling_periodicity_1s | Temporal periodicity signals for prediction generation |
