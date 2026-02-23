# PSH F-Layer — Forecast (3D)

**Layer**: Forecast (F)
**Indices**: [7:10]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:silencing_prediction | [0, 1] | Predicted silencing for next stimulus. Based on current prediction accuracy and high-level coupling trend. High when context is predictable and silencing has been effective — predicting continued silencing. de Vries 2023: high-level silencing at ~500ms post-stimulus with τ_high=0.2s. |
| 8 | F1:persistence_prediction | [0, 1] | Predicted low-level persistence for next window. Always high (low-level persists regardless) but modulated by amplitude and coupling trajectory. de Vries 2023: low-level persistence at ~110ms with τ_low=0.5s. |
| 9 | F2:next_prediction | [0, 1] | All-level prediction strength for next stimulus. Pre-stimulus prediction activation forecast based on consonance, periodicity, and coupling trajectory at bar level. High when the system can generate confident predictions for the upcoming event. |

---

## Design Rationale

1. **Silencing Prediction (F0)**: Forecasts whether the next stimulus will be silenced at high levels. When context is predictable (high consonance, periodicity), accurate predictions are likely → silencing predicted.

2. **Persistence Prediction (F1)**: Low-level persistence is always expected (model constraint) but amplitude and coupling trends modulate the magnitude of persistence.

3. **Next Prediction (F2)**: Forward prediction of pre-stimulus activation levels. When context is clear and coupling is strong, the system generates confident predictions → high pre-stimulus activity expected.

All outputs are sigmoid-bounded to [0, 1] with coefficient sums ≤ 1.0.

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 41 | 3 | M0 (value) | L0 | High-level coupling at 100ms |
| 1 | 41 | 8 | M0 (value) | L0 | High-level coupling at 500ms |
| 2 | 41 | 16 | M1 (mean) | L0 | Mean high-level coupling at bar |
| 3 | 41 | 16 | M20 (entropy) | L0 | High-level coupling entropy |
| 4 | 4 | 16 | M1 (mean) | L0 | Consonance mean at bar |
| 5 | 5 | 16 | M1 (mean) | L0 | Periodicity mean at bar |

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | E0:high_level_silencing | Current silencing for prediction |
| E-layer | E1:low_level_persistence | Persistence baseline |
| E-layer | E2:silencing_efficiency | Efficiency for continuation |
| P-layer | P0:prediction_state | Current prediction for extrapolation |
| R³ [4] | sensory_pleasantness | Consonance context |
| R³ [5] | periodicity | Periodicity context |
| R³ [41] | x_l5l7 | High-level coupling trajectory |
| H³ | 6 tuples (see above) | High-level and context features |
