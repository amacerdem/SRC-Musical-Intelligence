# NEWMD F-Layer — Forecast (2D)

**Layer**: Future Predictions (F)
**Indices**: [8:10]
**Scope**: exported (kernel relay)
**Activation**: sigmoid
**Model**: STU-γ2 (Neural Entrainment-Working Memory Dissociation, 10D, γ-tier <70%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 8 | F0:performance_pred | [0, 1] | Predicted task performance. f08 = sigma(0.35*f02 - 0.30*paradox + 0.25*f03). WM benefit minus entrainment cost plus flexibility contribution. Sares 2023: performance = WM(+) + entrainment(-) + flexibility(+). |
| 9 | F1:adaptation_pred | [0, 1] | Predicted tempo-change adaptation. f09 = sigma(0.40*stability_long + 0.30*f02). Combines long-range stability with WM capacity to predict how well the listener will adapt to upcoming tempo perturbations. |

---

## Design Rationale

1. **Performance Prediction (F0)**: The forward prediction of rhythmic performance. Combines the three routes discovered by Sares 2023: WM capacity (positive, +0.35), paradox magnitude (negative, -0.30), and flexibility (positive, +0.25). This mirrors the regression model: performance ~ beta_WM*WM + beta_entrain*entrainment + beta_flex*flexibility.

2. **Adaptation Prediction (F1)**: Predicts how well the listener will handle tempo changes. Uses long-range stability (H20, x_l4l5) combined with WM capacity. Musicians with higher WM and more stable long-range coupling adapt faster to tempo perturbations. This feeds F7 Motor for preparatory motor adjustments.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (33, 20, 19, 0) | x_l4l5[0] stability H20 L0 | Long-range coupling stability for adaptation prediction |
| (25, 20, 1, 0) | x_l0l5[0] mean H20 L0 | Long-range motor coupling mean — adaptation baseline |
| (25, 20, 22, 0) | x_l0l5[0] autocorrelation H20 L0 | Coupling temporal consistency — adaptation trend |

F-layer also reuses E+M outputs rather than reading many new H3 tuples:
- f02 (wm_capacity) from E-layer
- paradox (paradox_magnitude) from M-layer
- f03 (flexibility_cost) from E-layer

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:performance_pred | F6 Reward | PE from performance prediction vs actual |
| F0:performance_pred | Precision engine | pi_pred confidence for temporal beliefs |
| F1:adaptation_pred | F7 Motor | Motor preparation for tempo changes |
| F1:adaptation_pred | F8 Learning | Adaptation rate modulation |

---

## Scientific Foundation

- **Sares et al. 2023**: Performance ~ WM(+0.068) + entrainment(-0.060) + flexibility (N=48)
- **Noboa et al. 2025**: Exact replication with R²=0.316 — model generalizes across samples
- **Scartozzi et al. 2024**: Cross-validation of dual-route model (beta r=0.42, N=57)
- **Zanto et al. 2022**: Separable attention mechanisms predict adaptation (RCT, d=0.52)

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/newmd/forecast.py` (pending)
