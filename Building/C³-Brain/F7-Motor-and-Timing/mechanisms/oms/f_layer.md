# OMS — Forecast

**Model**: Oscillatory Motor Synchronization
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: β
**Layer**: F — Forecast
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 7 | sync_prediction | Next-beat synchronization prediction. Extrapolates synchronization quality from dynamics coupling trend, predictive timing stability, and current sync_quality at bar level (H16). When trend is positive and stability is high, confident synchronization continuation is predicted. Formula: σ(0.40 × dynamics_trend + 0.30 × predict_stability + 0.30 × sync_quality). |
| 8 | ensemble_cohesion | Ensemble cohesion prediction. Predicted orchestral balance from perceptual-crossband coupling mean and periodicity at H16 (1000ms). High mean + periodic balance → cohesive ensemble predicted. Formula: σ(0.50 × x_l5l7_mean + 0.50 × balance_periodicity). |
| 9 | groove_engagement | Groove-driven motor engagement prediction. Predicted motor engagement from amplitude smoothness and interpersonal sync signal (f03) at bar level. Smooth ensemble dynamics with strong interpersonal coordination predict sustained groove-driven engagement. Formula: σ(0.40 × amp_smoothness + 0.30 × f03 + 0.30 × motor_locking). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 41 | 16 | M1 (mean) | L0 | Mean orchestral balance |
| 1 | 41 | 16 | M14 (periodicity) | L2 | Balance regularity |
| 2 | 33 | 16 | M18 (trend) | L0 | Dynamics coupling trajectory |
| 3 | 25 | 16 | M19 (stability) | L0 | Predictive timing stability |
| 4 | 7 | 16 | M15 (smoothness) | L0 | Ensemble smoothness |

---

## Computation

The F-layer generates predictions about upcoming oscillatory motor synchronization:

1. **Sync prediction** (idx 7): Extrapolates synchronization from dynamics trend, predictive stability, and current sync quality. Positive trend + high stability + high current sync = high confidence in synchronization continuation.

2. **Ensemble cohesion** (idx 8): Predicts orchestral balance cohesion from mean cross-modal coupling and periodicity at bar level. Strong, periodic orchestral balance predicts ensemble cohesion.

3. **Groove engagement** (idx 9): Predicts motor engagement from amplitude smoothness and interpersonal synchronization. Smooth dynamics with strong social coordination predict sustained groove-driven engagement. Maps to the reward-motor pathway (ARU cross-unit).

All outputs are sigmoid-bounded to [0, 1] with coefficient sums ≤ 1.0.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f03_interpersonal_sync | Interpersonal signal for groove engagement |
| M-layer | sync_quality | Current sync for extrapolation |
| P-layer | motor_locking | Motor lock state for groove prediction |
| R³ [7] | amplitude | Smoothness for ensemble quality |
| R³ [25] | x_l0l5 | Stability for predictive timing |
| R³ [33] | x_l4l5 | Trend for dynamics coupling trajectory |
| R³ [41] | x_l5l7 | Mean and periodicity for orchestral balance |
| H³ | 5 tuples (see above) | Bar-level features at H16 (1000ms) |
