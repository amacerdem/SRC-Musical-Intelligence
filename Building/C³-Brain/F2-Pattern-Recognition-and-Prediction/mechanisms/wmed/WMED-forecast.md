# WMED F-Layer — Forecast (4D)

**Layer**: Forecast (F)
**Indices**: [7:11]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:next_beat_pred | [0, 1] | Motor system beat timing prediction. Extrapolates next beat from current entrainment and beat periodicity trend. Maps to SMA/BG anticipatory timing circuit (Ross & Balasubramaniam 2022). |
| 8 | F1:tapping_accuracy_pred | [0, 1] | Predicted tapping performance. Combines WM contribution and timing stability to forecast upcoming reproduction accuracy. High WM + stable timing predicts accurate reproduction. |
| 9 | F2:wm_interference_pred | [0, 1] | Predicted WM interference with entrainment. Forecasts whether cognitive load will disrupt automatic entrainment in the next window. Maps to the dual-route independence (Noboa 2025: no interaction term). |
| 10 | F3:paradox_strength_pred | [0, 1] | Predicted entrainment paradox intensity. Forecasts whether the entrainment→tapping inverse relationship will strengthen. High when entrainment is trending upward while accuracy trends downward. Aparicio-Terres 2025: tempo modulates entrainment (1.65>2.85 Hz). |

---

## Design Rationale

1. **Next Beat Prediction (F0)**: Forward timing prediction from current entrainment and periodicity trajectory. The automatic pathway generates motor predictions whether or not they improve accuracy.

2. **Tapping Accuracy Prediction (F1)**: Performance forecast from the controlled WM pathway. High WM engagement predicts maintained accuracy despite entrainment paradox.

3. **WM Interference Prediction (F2)**: Forecasts whether the two independent routes will conflict. Despite route independence (Noboa 2025), individual-level interference patterns may emerge.

4. **Paradox Strength Prediction (F3)**: Forecasts the entrainment-accuracy inverse relationship. When entrainment is strengthening, the paradox predicts decreased accuracy.

All outputs are sigmoid-bounded to [0, 1].

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 41 | 8 | M0 (value) | L0 | WM coupling at 500ms |
| 1 | 41 | 16 | M1 (mean) | L0 | Mean WM coupling at bar |
| 2 | 41 | 16 | M20 (entropy) | L0 | WM coupling entropy |
| 3 | 21 | 3 | M0 (value) | L2 | Spectral change (timing PE) |
| 4 | 21 | 16 | M2 (std) | L0 | Timing variability at bar |
| 5 | 21 | 16 | M19 (stability) | L0 | Timing stability at bar |

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | E0:entrainment_strength | Entrainment for paradox prediction |
| E-layer | E1:wm_contribution | WM for accuracy prediction |
| E-layer | E2:tapping_accuracy | Current accuracy for trajectory |
| P-layer | P2:paradox_strength | Current paradox for prediction |
| R³ [21] | spectral_change | Timing PE and stability |
| R³ [41] | x_l5l7 | WM coupling proxy |
| H³ | 6 tuples (see above) | WM and timing features |
