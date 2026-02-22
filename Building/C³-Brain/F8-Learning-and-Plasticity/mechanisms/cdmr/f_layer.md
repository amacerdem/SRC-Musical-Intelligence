# CDMR — Forecast

**Model**: Context-Dependent Mismatch Response
**Unit**: NDU
**Function**: F8 Learning & Plasticity
**Tier**: β
**Layer**: F — Forecast
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 9 | next_deviance | Attention allocation prediction. Predicts expected deviance at the next temporal step based on current deviance history, context state, and binding curvature trends. Drives pre-attentive resource allocation — higher predicted deviance increases vigilance for upcoming violations. Fong 2020: MMN as prediction error under predictive coding — the prediction itself. |
| 10 | context_continuation | Pattern expectation update. Predicts whether the current melodic context will continue, shift, or break. σ(0.50 * f02 + 0.50 * melodic_expectation). Combines current context modulation with accumulated melodic expectation. Maps to ERAN-like syntactic prediction in IFG (Koelsch: long-term music-syntactic regularities). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 15 | 41 | 16 | M16 (curvature) | L2 (bidi) | Binding curvature over 1s |

---

## Computation

The F-layer generates predictions about upcoming mismatch and context dynamics:

1. **Next deviance** (idx 9): Predicts the expected magnitude of deviance at upcoming time steps. Under the predictive coding framework (Fong 2020), this represents the top-down prediction that will be compared against incoming sensory input to generate the next mismatch response. Uses deviance history (M-layer), context state (P-layer), and binding curvature at 1s (H³) to extrapolate deviance trajectories. The curvature morph captures whether deviance patterns are accelerating, decelerating, or stable.

2. **Context continuation** (idx 10): Predicts whether the current melodic context will persist, enabling anticipatory modulation of mismatch sensitivity. Equal weighting of current context modulation (f02) and accumulated melodic expectation provides both immediate and historical context information. When both are high, the system predicts continued rich melodic context and maintains high sensitivity. When either drops, sensitivity prediction decreases accordingly. This prediction feeds forward to the next frame's mismatch computation.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f02_context_modulation | Current context for continuation prediction |
| M-layer | melodic_expectation | Accumulated context for continuation prediction |
| M-layer | deviance_history | Recent deviance for next-step prediction |
| P-layer | context_state | Current context richness for deviance forecasting |
| H³ | 1 tuple (see above) | Binding curvature for trend extrapolation |
