# UDP F-Layer — Forecast (3D)

**Layer**: Forecast (F)
**Indices**: [7:10]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:reward_expectation | [0, 1] | Predicted reward for next event. Anticipatory reward signal based on current uncertainty level and reward pathway strength. Maps to caudate anticipatory dopamine (Salimpoor 2011: r=0.71 chill anticipation). Formula: sigma(0.40*pleasure_index + 0.30*periodicity_trend + 0.30*coupling_skew). |
| 8 | F1:uncertainty_resolution | [0, 1] | Predicted uncertainty resolution. Will the next event reduce uncertainty (confirming the model)? High when uncertainty is high but predictions are improving. Gold 2019: IC × entropy interaction — learning progress is rewarding. |
| 9 | F2:pleasure_anticipation | [0, 1] | Anticipatory affective state (1-3s ahead). Combined forward prediction of pleasure from reward expectation and uncertainty trajectory. Maps to caudate-NAcc anticipatory circuit. Decay: τ=3s (Mencke 2019). |

---

## Design Rationale

1. **Reward Expectation (F0)**: Anticipatory reward prediction from current pleasure level and periodicity trend. The caudate generates anticipatory dopamine proportional to expected reward.

2. **Uncertainty Resolution (F1)**: Predicts whether the next event will reduce uncertainty. In atonal contexts, correct predictions (confirmation) resolve uncertainty — which is intrinsically rewarding.

3. **Pleasure Anticipation (F2)**: 1-3s forward affective prediction combining reward expectation and uncertainty trajectory. The temporal dynamics follow a τ=3s decay (Mencke 2019).

All outputs are sigmoid-bounded to [0, 1] with coefficient sums ≤ 1.0.

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 41 | 8 | M0 (value) | L0 | Coupling at 500ms |
| 1 | 41 | 16 | M1 (mean) | L0 | Mean coupling over bar |
| 2 | 41 | 16 | M20 (entropy) | L0 | Coupling entropy |
| 3 | 41 | 16 | M6 (skew) | L0 | Coupling skew (reward asymmetry) |

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | E0:uncertainty_level | Uncertainty for resolution prediction |
| E-layer | E3:pleasure_index | Current pleasure for anticipation |
| P-layer | P0:reward_mode | Mode for pathway prediction |
| R³ [41] | x_l5l7 | Coupling for reward computation |
| H³ | 4 tuples (see above) | Bar-level coupling features |
