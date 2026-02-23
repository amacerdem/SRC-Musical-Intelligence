# TMRM — Forecast

**Model**: Tempo Memory Reproduction Method
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: F — Forecast
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 7 | tempo_prediction | Predicted next-beat tempo stability. Extrapolates tempo trajectory from bar-level loudness periodicity and amplitude trend at H16 (1000ms). When periodicity is strong and intensity trend is stable, confident tempo continuation is predicted. Formula: σ(0.50 × loud_bar_period + 0.50 × amp_trend). |
| 8 | method_confidence | Confidence in current reproduction method. Combines loudness smoothness at H11 with loudness trend at H16. Smooth, trending loudness patterns signal reliable method-independent tempo encoding. Formula: σ(0.50 × loud_smooth + 0.50 × loud_trend). |
| 9 | reproduction_accuracy | Expected overall reproduction accuracy. Weighted combination of sensory advantage, optimal tempo, and expertise. Integrates all three E-layer signals to predict upcoming reproduction precision. Formula: σ(0.40 × f01 + 0.30 × f02 + 0.30 × f03). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 7 | 16 | M18 (trend) | L0 | Bar-level intensity trend |
| 1 | 8 | 16 | M14 (periodicity) | L0 | Bar-level periodicity |
| 2 | 8 | 16 | M18 (trend) | L0 | Loudness trajectory over bar |
| 3 | 21 | 16 | M8 (velocity) | L0 | Spectral change rate at bar level |
| 4 | 22 | 16 | M15 (smoothness) | L0 | Energy smoothness at bar level |

---

## Computation

The F-layer generates predictions about upcoming tempo reproduction:

1. **Tempo prediction** (idx 7): Extrapolates tempo stability from periodicity and trend at bar level. Strong loudness periodicity at H16 with positive amplitude trend predicts reliable tempo continuation.

2. **Method confidence** (idx 8): Predicts confidence in whichever reproduction method is dominant. Combines loudness smoothness (motor quality) with loudness trend (trajectory quality). Smooth, trending patterns indicate both methods can maintain accuracy.

3. **Reproduction accuracy** (idx 9): Overall accuracy forecast combining all three E-layer components with weights emphasizing the sensory advantage (0.40) over optimal tempo (0.30) and expertise (0.30). The highest accuracy forecasts occur near 120 BPM with strong sensory support and musical expertise.

All outputs are sigmoid-bounded to [0, 1] with coefficient sums ≤ 1.0.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01, f02, f03 | All three accuracy components for forecast |
| P-layer | sensory_state, motor_state | Current pathway states |
| R³ [7] | amplitude | Bar-level intensity trend |
| R³ [8] | loudness | Bar-level periodicity and trajectory |
| R³ [21] | spectral_change | Spectral dynamics at bar level |
| R³ [22] | energy_change | Energy smoothness at bar level |
| H³ | 5 tuples (see above) | Bar-level features at H16 (1000ms) |
