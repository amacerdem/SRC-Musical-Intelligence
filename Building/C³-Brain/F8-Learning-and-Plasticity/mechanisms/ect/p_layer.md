# ECT — Cognitive Present

**Model**: Expertise Compartmentalization Trade-off
**Unit**: NDU
**Function**: F8 Learning & Plasticity
**Tier**: γ
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 7 | within_binding | Current within-network efficiency. Represents the instantaneous state of intra-network coupling, reflecting how efficiently specialized modules are operating right now. Derived from within-coupling at 100ms, coupling variability at 100ms, and pattern binding at 100ms. Papadaki et al. 2023: greater network strength and global efficiency in professionals correlate with task performance. |
| 8 | network_isolation | Current cross-network reduction. Represents the instantaneous degree of between-network isolation, reflecting how disconnected specialized modules are from each other right now. Derived from cross-network binding at 100ms, cross-network variability at 100ms, and inverted flexibility index. Moller et al. 2021: musicians show localized CT correlations only (not distributed); structural evidence for network isolation. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 33 | 3 | M0 (value) | L2 (bidi) | Pattern binding at 100ms for within-binding |
| 1 | 23 | 3 | M0 (value) | L2 (bidi) | Pitch specialization at 100ms |
| 2 | 23 | 16 | M1 (mean) | L2 (bidi) | Mean pitch specialization 1s |
| 3 | 8 | 3 | M0 (value) | L2 (bidi) | Attention allocation at 100ms |

---

## Computation

The P-layer captures the instantaneous state of the expertise compartmentalization trade-off, providing a snapshot of how the network is currently balancing specialization versus integration.

1. **within_binding**: Represents the current within-network efficiency by combining instantaneous within-coupling (H³: x_l0l5[0], H3, M0, L2), coupling variability (H³: x_l0l5[0], H3, M2, L2), and pattern binding (H³: x_l4l5[0], H3, M0, L2). Low variability with high coupling indicates efficient specialized processing. This dimension fluctuates with the complexity and familiarity of the current auditory input.

2. **network_isolation**: Represents the current between-network disconnection by combining instantaneous cross-network binding (H³: x_l5l6[0], H3, M0, L2), cross-network variability (H³: x_l5l6[0], H3, M2, L2), and inverted flexibility index (E-layer f04). High isolation means the specialized modules are operating independently with limited information sharing — the "cost" side of the trade-off visible in real time.

The P-layer provides the real-time balance that the F-layer uses to predict future transfer limitations and recovery capacity.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f04 | Flexibility index | Inverted for network isolation computation |
| R³[25:33] x_l0l5 | Intra-network coupling | Instantaneous within-binding measurement |
| R³[33:41] x_l4l5 | Pattern-feature binding | Current binding state |
| R³[41:49] x_l5l6 | Cross-network connectivity | Instantaneous isolation measurement |
| R³[8] loudness | Perceptual loudness | Attention allocation context |
| R³[23] pitch_change | Pitch dynamics | Specialization tracking |
| H³ (4 tuples) | Multi-scale temporal morphology | Pattern binding, pitch specialization, and attention at 100ms-1s |
