# ECT — Forecast

**Model**: Expertise Compartmentalization Trade-off
**Unit**: NDU
**Function**: F8 Learning & Plasticity
**Tier**: γ
**Layer**: F — Forecast
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 9 | transfer_limit | Cross-domain performance prediction. Predicts the degree to which compartmentalization will limit cross-domain transfer. transfer_limit = σ(0.50 * f02 + 0.50 * (1 - f04)). High between-reduction (f02) combined with low flexibility (1 - f04) predicts strong transfer limitation. Moller et al. 2021: musicians show behavioral cost in BCG (t(42.3) = 3.06, p = 0.004) — reduced cross-modal structural connectivity limits visual cue benefit. |
| 10 | efficiency_opt | Within-network speed prediction. Predicts the future processing efficiency within specialized modules based on current within-binding state and training history. Reflects the "gain" trajectory of compartmentalization — continued specialization should improve within-network processing speed. Papadaki et al. 2023: network strength and global efficiency correlate with task performance in aspiring professionals. |
| 11 | flexibility_recovery | Network reconfiguration capacity prediction. Predicts whether the system can recover flexibility through varied demands. Based on flexibility index (f04), task memory demand entropy, and current network isolation. Wu-Chung et al. 2025: baseline network flexibility determines whether music training produces cognitive benefit — suggesting flexibility can be a recoverable resource. Blasi et al. 2025: music/dance rehabilitation produces neuroplasticity in perception, memory, and motor areas, suggesting recovery is possible. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 7 | 3 | M0 (value) | L2 (bidi) | Task demand at 100ms for efficiency context |
| 1 | 13 | 3 | M0 (value) | L2 (bidi) | Tonal adaptation at 100ms for flexibility context |

---

## Computation

The F-layer generates three forward predictions about the trajectory of the compartmentalization trade-off, addressing the core speculative question: does expertise compartmentalization limit creative transfer?

1. **transfer_limit**: Combines between-network reduction (f02, weight 0.50) with inverted flexibility (1 - f04, weight 0.50) to predict cross-domain transfer limitations. This is the most directly testable prediction: musicians with high compartmentalization and low flexibility should show slower cross-domain transfer. Moller et al. 2021 provides the first behavioral evidence supporting this prediction (reduced BCG in musicians).

2. **efficiency_opt**: Predicts future within-network processing speed based on the P-layer within_binding state and M-layer training_history. This captures the "gain" side of the trade-off trajectory: continued specialization should yield increasing processing efficiency within the trained domain. Papadaki et al. 2023 supports this with evidence that network strength correlates with performance.

3. **flexibility_recovery**: Predicts whether the system can recover flexibility through varied task demands. Based on the E-layer flexibility index (f04), M-layer task memory (demand entropy), and P-layer network isolation. Wu-Chung et al. 2025's finding that baseline flexibility determines training benefit suggests flexibility is not permanently lost but can be modulated. Blasi et al. 2025's rehabilitation evidence further supports that neuroplasticity allows recovery.

These predictions remain speculative (gamma-tier): the structural observation is confirmed, but functional consequences are only partially tested (Moller BCG; Wu-Chung flexibility pilot). Full functional testing of transfer, task switching, and creativity trade-offs is a critical research priority.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f02 | Between-network reduction | Transfer limitation input |
| E-layer f04 | Flexibility index | Transfer limitation and recovery inputs |
| M-layer training_history | Specialization accumulation | Efficiency trajectory context |
| M-layer task_memory | Demand entropy | Flexibility recovery modulator |
| P-layer within_binding | Current efficiency state | Efficiency prediction base |
| P-layer network_isolation | Current isolation state | Recovery prediction context |
| R³[7] amplitude | Acoustic intensity | Task demand for efficiency context |
| R³[13] brightness | Tonal quality | Adaptation for flexibility context |
| H³ (2 tuples) | Multi-scale temporal morphology | Task demand and tonal adaptation at 100ms |
