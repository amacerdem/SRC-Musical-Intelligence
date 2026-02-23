# PWUP F-Layer — Forecast (3D)

**Layer**: Forecast (F)
**Indices**: [7:10]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:precision_adjustment | [0, 1] | Predicted precision for next window. sigma(0.50*tonal_precision + 0.50*rhythmic_precision). Combined tonal + rhythmic precision predicts overall precision level for upcoming events. Harding 2025: vmPFC modulates surprise-related precision (F(1,39)=7.07). |
| 8 | F1:context_uncertainty | [0, 1] | Predicted uncertainty trajectory. Direct pass of E3 uncertainty_index. High uncertainty predicts continued PE attenuation. Cheung 2019: hippocampus tracks context uncertainty. |
| 9 | F2:response_attenuation | [0, 1] | Predicted PE response attenuation. sigma(0.50*weighted_error + 0.50*uncertainty_index). Combines current PE strength with uncertainty to predict how much PE will be attenuated in the next window. Mencke 2019: atonal PE attenuation pattern. |

---

## Design Rationale

1. **Precision Adjustment (F0)**: Predicts the overall precision level for upcoming processing. When both tonal and rhythmic precision are high, strong PE responses are predicted; when either is low, attenuation is predicted.

2. **Context Uncertainty (F1)**: Tracks the uncertainty trajectory — whether the context is becoming more or less predictable. High values predict continued PE attenuation.

3. **Response Attenuation (F2)**: Combines PE magnitude with uncertainty to predict the degree of PE attenuation in the next processing window. This forward signal prepares downstream models for the expected PE magnitude.

All outputs are sigmoid-bounded to [0, 1] with coefficient sums ≤ 1.0.

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 41 | 8 | M0 (value) | L0 | Cross-modal coupling at 500ms |
| 1 | 41 | 16 | M1 (mean) | L0 | Mean coupling over bar |
| 2 | 41 | 16 | M20 (entropy) | L0 | Coupling entropy at bar level |

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | E0:tonal_precision | Tonal precision for forecast |
| E-layer | E1:rhythmic_precision | Rhythmic precision for forecast |
| E-layer | E2:weighted_error | PE magnitude for attenuation prediction |
| E-layer | E3:uncertainty_index | Uncertainty for context trajectory |
| R³ [41] | x_l5l7 | Cross-modal coupling for precision |
| H³ | 3 tuples (see above) | Bar-level coupling features |
