# vividness_trajectory — Anticipation Belief (MEAMN)

**Category**: Anticipation (prediction)
**Owner**: MEAMN (IMU-α1)

---

## Definition

"Memory will become vivid within 2-5 seconds." Forward prediction from MEAMN F-layer. Predicts the trajectory of memory recall quality over the next 2-5 seconds: will the currently forming autobiographical memory sharpen into a vivid, detailed re-experience, or will it fade before fully consolidating? Uses the hippocampal retrieval trajectory over the H20 (5s) consolidation window.

---

## Observation Formula

```
# From MEAMN F-layer:
vividness_trajectory = MEAMN.mem_vividness_fc[F0]  # index [8]

# Formula: sigma(hippocampal retrieval trajectory over H20)
# Based on:
#   H3 (7, 20, 4, 0): amplitude max H20 L0 — peak energy over 5s
#   MEAMN E0: f01_retrieval — current retrieval strength
#   MEAMN P0: memory_state — current memory activation
```

Anticipation beliefs are forward-looking predictions that generate PE when the predicted vividness trajectory mismatches the observed vividness evolution. High vividness_trajectory predicts that the listener is about to enter a vivid memory state.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| MEAMN F0 | mem_vividness_fc [8] | Vividness prediction (2-5s ahead) |
| MEAMN E0 | f01_retrieval [0] | Current retrieval state (upstream input) |
| MEAMN P0 | memory_state [5] | Current memory activation (upstream input) |
| H³ | (7, 20, 4, 0) amplitude max H20 L0 | Peak energy over 5s |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| Precision engine | pi_pred estimation — high vividness_trajectory increases prediction confidence for autobiographical_retrieval |
| F5 Emotion | Emotional preparation: if vividness is predicted to increase, affective systems prepare for stronger emotional re-experiencing |
| F6 Reward | PE from vividness prediction mismatches feeds reward (surprising vividness = positive reward) |

---

## Scientific Foundation

- **Janata 2009**: Imagery vividness strong vs weak autobiographical (t(9)=5.784, p<0.0003); hippocampal activation trajectory predicts memory quality (fMRI 3T, N=13)
- **Janata et al. 2007**: MEAMs emerge over seconds — retrieval trajectory is predictable from initial activation (behavioral, N~300)
- **Tulving 2002**: Episodic memory requires coherent feature binding over time — vividness builds through progressive consolidation (review)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/meamn_relay.py`
