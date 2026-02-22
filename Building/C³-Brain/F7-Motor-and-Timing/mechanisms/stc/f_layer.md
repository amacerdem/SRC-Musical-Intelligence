# STC — Forecast

**Model**: Singing Training Connectivity
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: F — Forecast
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 8 | connectivity_pred | Connectivity change prediction. Forecasts the expected insula-sensorimotor connectivity state at the next time step by combining current interoceptive coupling (f28) with interoceptive periodicity at 1s. connectivity_pred = sigma(0.5 * f28 + 0.5 * interoceptive_period_1s). The periodicity signal provides the oscillatory regularity that supports forward prediction of connectivity dynamics. |
| 9 | respiratory_pred | Respiratory control prediction. Forecasts the expected respiratory integration state by combining current respiratory integration (f29) with respiratory periodicity at 1s. respiratory_pred = sigma(0.5 * f29 + 0.5 * respiratory_period_1s). Breath-phrase coupling regularity at the 1s scale enables prediction of upcoming respiratory states. |
| 10 | vocal_pred | Vocal production prediction. Forecasts the expected speech sensorimotor state by combining current speech sensorimotor activation (f30) with vocal warmth at 100ms. vocal_pred = sigma(0.5 * f30 + 0.5 * vocal_warmth_100ms). The fast warmth signal captures the immediate vocal timbre trajectory for short-term prediction. Zarate 2010: involuntary pitch correction implies automatic predictive vocal control. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 33 | 16 | M14 (periodicity) | L2 (bidi) | Interoceptive period 1s (shared with E-layer) |
| 1 | 25 | 16 | M14 (periodicity) | L2 (bidi) | Respiratory period 1s (shared with E-layer) |
| 2 | 12 | 3 | M0 (value) | L2 (bidi) | Vocal warmth 100ms (shared with E-layer) |

---

## Computation

The F-layer generates three forward predictions about the interoceptive-motor integration state, enabling the C3 belief system to form expectations about upcoming connectivity, respiratory control, and vocal motor engagement.

1. **connectivity_pred**: Predicts next-step insula-sensorimotor connectivity by averaging current interoceptive coupling (f28) with the interoceptive periodicity signal at 1s. The periodicity captures the cyclic nature of interoceptive monitoring, providing a natural basis for forecasting. This prediction is supported by Zamorano 2023's evidence that singing training creates lasting (resting-state) connectivity patterns that persist beyond active singing.

2. **respiratory_pred**: Predicts next-step respiratory integration by averaging current respiratory integration (f29) with respiratory periodicity at 1s. Breathing follows inherently periodic patterns that are coupled with musical phrases, making periodicity at the 1s scale a strong predictor of upcoming respiratory states. Tsunada 2024's finding of tonic vocal suppression (predictive component) supports the existence of forward respiratory prediction mechanisms.

3. **vocal_pred**: Predicts next-step speech sensorimotor activation by averaging current activation (f30) with the fast vocal warmth signal at 100ms. Unlike the other predictions which use slow periodicity (1s), vocal_pred uses the fast warmth signal because vocal articulation operates at a faster timescale than breathing or interoceptive monitoring. Zarate 2010 showed that singers automatically correct pitch deviations, implying a predictive vocal control loop that this dimension captures.

F-layer H3 demands are shared with the E-layer (interoceptive and respiratory periodicity at H16, vocal warmth at H3), requiring no additional tuples.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f28 | Interoceptive coupling | Base signal for connectivity prediction |
| E-layer f29 | Respiratory integration | Base signal for respiratory prediction |
| E-layer f30 | Speech sensorimotor | Base signal for vocal prediction |
| H3 (33, 16, M14, L2) | Interoceptive period 1s | Periodicity basis for connectivity_pred |
| H3 (25, 16, M14, L2) | Respiratory period 1s | Periodicity basis for respiratory_pred |
| H3 (12, 3, M0, L2) | Vocal warmth 100ms | Fast timbre signal for vocal_pred |
