# CSSL F-Layer — Forecast (3D)

**Layer**: Future Predictions (F)
**Indices**: [7:10]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:learning_trajectory | [0, 1] | Learning trajectory prediction (2-5s ahead). Template fidelity trend from H20 consolidation window. Predicts whether template matching is improving or degrading. Sensitive period study (2018): critical window for song template acquisition (~20-90 dph in zebra finch, d=0.61). |
| 8 | F1:binding_prediction | [0, 1] | Binding strength prediction (5-36s ahead). Hippocampal binding trajectory from H24. Predicts whether rhythm-melody binding will strengthen or weaken. Burchardt et al. 2025: all-shared binding r=0.94 (N=54). |
| 9 | F2:reserved | [0, 1] | Reserved for future expansion. Currently outputs zeros. |

---

## Design Rationale

1. **Learning Trajectory (F0)**: Predicts the direction of song learning over the next 2-5 seconds. Uses familiarity trend from the H20 window to extrapolate whether the listener is getting better at matching the template. During the sensitive period, this trajectory is steep (rapid learning); post-sensitive period, it flattens. This maps to the tutee's progressive convergence toward tutor song.

2. **Binding Prediction (F1)**: Predicts the strength of the all-shared binding over a longer 5-36s window. Uses retrieval dynamics from the H24 horizon. High binding prediction means the hippocampus is actively consolidating rhythm + melody into a unified song representation. This is the "will the song be learned?" prediction.

3. **Reserved (F2)**: Held for future expansion. Potential uses include sensitive-period gating signal or cross-species divergence index.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (22, 24, 19, 0) | entropy stability H24 L0 | Pattern stability over 36s for binding prediction |
| (12, 20, 1, 0) | warmth mean H20 L0 | Sustained voice warmth for learning trajectory |

F-layer primarily reuses E+M+P outputs rather than reading many new H3 tuples directly.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:learning_trajectory | F4 Memory (DMMS) | Sensitive period parallels — developmental scaffold depth |
| F1:binding_prediction | F4 Memory (MEAMN) | Song template binding feeds autobiographical memory |
| F2:reserved | -- | Future expansion |

---

## Scientific Foundation

- **Burchardt et al. 2025**: All-shared binding r=0.94 for tutor-tutee song element sequences (N=54, zebra finch)
- **Sensitive period study 2018**: Critical window for song template acquisition; d=0.61 (N=48)
- **Basal ganglia sequencing 2017**: Area X necessary for song learning, analogous to human striatum (lesion + neural, N=24)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/cssl/forecast.py`
