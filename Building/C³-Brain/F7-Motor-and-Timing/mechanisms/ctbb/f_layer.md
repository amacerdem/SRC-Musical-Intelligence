# CTBB — Forecast

**Model**: Cerebellar Theta-Burst Balance
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: F — Forecast
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 8 | timing_pred | Timing enhancement prediction. Forecasts the expected cerebellar timing precision at the next time step by combining current cerebellar timing (f25) with coupling stability at 1s. timing_pred = sigma(0.5 * f25 + 0.5 * coupling_stability_1s). Relies on the stability of the cerebellar timing circuit to extrapolate forward. |
| 9 | balance_pred | Postural control prediction. Forecasts the expected balance state by combining current postural control (f27) with coupling periodicity at 1s. balance_pred = sigma(0.5 * f27 + 0.5 * coupling_period_1s). Periodicity provides the oscillatory regularity that supports prediction. |
| 10 | modulation_pred | M1 modulation prediction. Forecasts the expected motor cortex excitability modulation. Extrapolates the current M1 modulation state (f26) forward. Note: CBI null (Sansare 2025) suggests this prediction carries higher uncertainty than timing_pred and balance_pred. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 16 | M19 (stability) | L0 (fwd) | Coupling stability 1s (shared with E-layer) |
| 1 | 25 | 16 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 1s (shared with E-layer) |

---

## Computation

The F-layer generates three forward predictions about the cerebellar motor timing state, enabling the C3 belief system to form expectations about upcoming motor precision, balance, and cortical modulation.

1. **timing_pred**: Predicts next-step cerebellar timing precision by averaging current cerebellar timing (f25) with the long-term coupling stability signal. Stability at 1s captures the slow-varying reliability of the cerebellar timing circuit, making it a natural basis for prediction. This is the highest-confidence prediction, supported by Sansare 2025's sustained iTBS effects (>= 30 min).

2. **balance_pred**: Predicts next-step postural control by averaging current postural control (f27) with coupling periodicity at 1s. The periodicity signal captures oscillatory regularities in the cerebellar-M1 coupling that support balance prediction. Sansare 2025's POST1-6 time series shows relatively stable postural improvement within the 30-min window.

3. **modulation_pred**: Predicts next-step M1 modulation state. This prediction carries the highest uncertainty due to the CBI null result (Sansare 2025, eta-sq = 0.045 n.s.), which indicates the direct cerebellar-M1 pathway may not be the primary mediator. Alternative circuits (cerebellar-prefrontal, cerebellar-vestibular) may contribute but are not modeled here.

F-layer H3 demands are shared with the E-layer (coupling stability and periodicity at H16), requiring no additional tuples.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f25 | Cerebellar timing | Base signal for timing prediction |
| E-layer f26 | M1 modulation | Base signal for modulation prediction |
| E-layer f27 | Postural control | Base signal for balance prediction |
| H3 (25, 16, M19, L0) | Coupling stability 1s | Stability basis for timing_pred |
| H3 (25, 16, M14, L2) | Coupling periodicity 1s | Periodicity basis for balance_pred |
