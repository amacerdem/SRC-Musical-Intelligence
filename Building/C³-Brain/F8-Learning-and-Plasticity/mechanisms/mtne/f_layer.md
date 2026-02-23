# MTNE — Forecast

**Model**: Music Training Neural Efficiency
**Unit**: STU
**Function**: F8 Learning & Plasticity
**Tier**: γ
**Layer**: F — Forecast
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 8 | efficiency_predict | Predicted efficiency for upcoming segment. Based on long-term autocorrelation of cross-domain coupling features at H20 (5000ms). σ(0.35 × x_l0l5_autocorr + 0.35 × x_l4l5_autocorr + 0.30 × efficiency_index). High autocorrelation = stable structural patterns → efficiency predicted to continue. |
| 9 | resource_forecast | Predicted neural resource demand. Based on energy entropy, acceleration, and hedonic trajectory at H14/H20. σ(0.40 × entropy_energy + 0.30 × energy_accel + 0.30 × pleasant_trend). Rising entropy + acceleration = increasing complexity → higher resource demand predicted. Positive hedonic trend may moderate resource cost. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 20 | M1 (mean) | L0 | Long-term cross-domain coupling mean |
| 1 | 25 | 20 | M22 (autocorr) | L0 | Section-level self-similarity |
| 2 | 33 | 20 | M1 (mean) | L0 | Long-term dynamics coupling mean |
| 3 | 33 | 20 | M22 (autocorr) | L0 | Long-range repetition detection |
| 4 | 0 | 20 | M1 (mean) | L0 | Long-term hedonic level |
| 5 | 0 | 20 | M18 (trend) | L0 | Hedonic trajectory |

---

## Computation

The F-layer generates predictions about upcoming neural efficiency:

1. **Efficiency prediction** (idx 8): Forecasts whether the current efficiency state will continue. High autocorrelation in cross-domain coupling (x_l0l5, x_l4l5) at section level (H20=5000ms) indicates stable structural patterns that predict continued efficiency. Combined with current efficiency index from M-layer. Coefficient sum: 0.35 + 0.35 + 0.30 = 1.0.

2. **Resource forecast** (idx 9): Predicts neural resource demand for upcoming segment. Energy entropy (unpredictability) and acceleration (rate of change change) drive resource demand upward. Hedonic trajectory (pleasant trend) provides a modulating context — positive hedonic experience may reduce perceived effort. Coefficient sum: 0.40 + 0.30 + 0.30 = 1.0.

All outputs are sigmoid-bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| M-layer | efficiency_index | Current efficiency for continuation prediction |
| E-layer | (indirect) | Via M-layer integration |
| H³ | 6 tuples (see above) | Long-term features at H20 |
| H³ (reused) | entropy_energy, energy_accel at H14 | Complexity features from E-layer |
