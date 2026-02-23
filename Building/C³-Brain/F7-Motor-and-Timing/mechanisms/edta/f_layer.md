# EDTA — Forecast

**Model**: Expertise-Dependent Tempo Accuracy
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: β
**Layer**: F — Forecast
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 7 | tempo_prediction | Predicted tempo trajectory. H³ trend-based next-beat expectation from pitch trend, bar-level periodicity, and meter state. Maps to anticipatory timing in the premotor/SMA circuit. Formula: σ(0.40 × pitch_trend + 0.30 × periodicity_bar + 0.30 × meter_state). |
| 8 | entrainment_expect | Entrainment confidence for next bar. Predicted motor-auditory entrainment quality from periodicity + smoothness at bar level (H16). High periodicity and smoothness signal that the motor system can confidently entrain to upcoming beat structure. Formula: σ(0.50 × smoothness + 0.50 × bar_periodicity). |
| 9 | accuracy_forecast | Predicted accuracy for upcoming tempo. Motor entrainment × expertise proxy. Combines f03 expertise effect, tempo prediction, and entrainment expectation. When all three signals are strong, high accuracy for the upcoming bar is predicted. Formula: σ(0.50 × f03 + 0.30 × tempo_prediction + 0.20 × entrainment_expect). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 21 | 16 | M14 (periodicity) | L2 | Bar-level rhythmic regularity |
| 1 | 21 | 16 | M15 (smoothness) | L2 | Motor smoothness proxy |
| 2 | 23 | 16 | M18 (trend) | L0 | Melodic tempo coupling trend |
| 3 | 24 | 16 | M19 (stability) | L0 | Timbral timing stability |
| 4 | 22 | 16 | M14 (periodicity) | L2 | Bar-level tempo periodicity |

---

## Computation

The F-layer generates predictions about upcoming tempo accuracy:

1. **Tempo prediction** (idx 7): Extrapolates tempo trajectory from pitch change trend, bar-level energy periodicity, and current meter state. When pitch trend is stable, periodicity is strong, and meter is clear, the system confidently predicts tempo continuation.

2. **Entrainment expectation** (idx 8): Predicts motor-auditory entrainment quality from spectral change smoothness and periodicity at bar level. Smooth, periodic patterns at H16 indicate that the motor system can maintain entrainment.

3. **Accuracy forecast** (idx 9): Combined prediction of upcoming tempo accuracy. Integrates expertise effect (f03), tempo prediction, and entrainment expectation. The highest accuracy forecasts occur when domain-specific expertise is activated AND tempo/entrainment predictions are confident.

All outputs are sigmoid-bounded to [0, 1] with coefficient sums ≤ 1.0.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f03_expertise_effect | Expertise modulation for accuracy forecast |
| P-layer | meter_state | Current metrical context for tempo prediction |
| R³ [21] | spectral_change | Periodicity and smoothness at bar level |
| R³ [22] | energy_change | Bar-level periodicity for entrainment |
| R³ [23] | pitch_change | Trend for melodic-tempo coupling |
| R³ [24] | timbre_change | Stability for timing assessment |
| H³ | 5 tuples (see above) | Bar-level features at H16 (1000ms) |
