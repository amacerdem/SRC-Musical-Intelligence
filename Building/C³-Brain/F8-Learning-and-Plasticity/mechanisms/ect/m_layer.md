# ECT — Temporal Integration

**Model**: Expertise Compartmentalization Trade-off
**Unit**: NDU
**Function**: F8 Learning & Plasticity
**Tier**: γ
**Layer**: M — Temporal Integration
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 4 | training_history | Specialization accumulation over time. Uses the pattern binding trend over 1s as a proxy for how specialization has developed. Increasing trend indicates deepening compartmentalization; stable or decreasing trend indicates plateau or broadening. Leipold et al. 2021 (N = 153): robust effects of musicianship on interhemispheric and intrahemispheric connectivity independent of absolute pitch, confirming graded expertise effects. |
| 5 | network_state | Recent network architecture state. Computes the efficiency delta as the difference between within-network efficiency and between-network reduction: network_state = σ(0.50 * f01 + 0.50 * (1 - f02)). Positive values indicate the network currently favors specialization; values near 0.5 indicate balance. Paraskevopoulos et al. 2022: musicians show a distinct network topology with more within-network and fewer between-network connections. |
| 6 | task_memory | Demand-driven network shaping. Tracks the processing demand entropy through EMA of amplitude entropy at 500ms. High demand entropy suggests varied task demands that may counteract compartmentalization; low entropy suggests stable demands that reinforce specialization. Olszewska et al. 2021: training-induced brain reorganization involves dynamic reconfiguration of neural connections. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 33 | 16 | M18 (trend) | L0 (fwd) | Pattern binding trend over 1s for training history |
| 1 | 7 | 8 | M20 (entropy) | L2 (bidi) | Demand entropy 500ms for task memory |

---

## Computation

The M-layer tracks three temporal dynamics of the compartmentalization process: how specialization accumulates, the current network architecture state, and how task demands shape the trade-off.

1. **training_history**: Uses the binding trend over 1s (H³ tuple: x_l4l5[0], H16, M18, L0) as a direct proxy for specialization accumulation. The forward-only law (L0) ensures causal tracking of how binding patterns evolve over time. This captures the graded nature of expertise effects confirmed across 153 participants by Leipold et al. 2021.

2. **network_state**: Combines within-efficiency (f01) with inverted between-reduction (1 - f02) through equal weighting. This produces a single scalar reflecting the current balance between specialization gains and integration costs. The sigmoid ensures the output stays in [0, 1], where high values indicate strong specialization dominance.

3. **task_memory**: Tracks the demand entropy at 500ms (H³ tuple: amplitude, H8, M20, L2) as a measure of how varied the processing demands have been. Complex, varied music creates high demand entropy which may counteract compartmentalization; simple, repetitive passages create low entropy which reinforces it.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f01 | Within-network efficiency | Input to network state computation |
| E-layer f02 | Between-network reduction | Inverted input to network state |
| R³[7] amplitude | Acoustic intensity | Demand entropy for task memory |
| R³[33:41] x_l4l5 | Pattern-feature binding | Binding trend for training history |
| H³ (2 tuples) | Multi-scale temporal morphology | Binding trend at 1s and demand entropy at 500ms |
