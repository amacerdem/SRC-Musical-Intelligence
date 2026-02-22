# consonance_valence_mapping — Appraisal Belief (CSG)

**Category**: Appraisal (observe-only)
**Owner**: CSG (ASU-a3)

---

## Definition

"Consonance directly predicts emotional valence." Observes the linear mapping from consonance to emotional valence. Consonant intervals are pleasant (positive valence); dissonant intervals are unpleasant (negative valence). This is a direct, pre-cognitive mapping — no learning required.

---

## Observation Formula

```
# Direct read from CSG E-layer:
consonance_valence_mapping = CSG.f09_consonance_valence[E2]   # index [2], [-1,1]

# Computation:
# tanh(0.50 * pleasantness_velocity + 0.50 * pleasantness_mean_1s)
#
# Linear consonance -> valence mapping
# Range [-1, 1]: negative = unpleasant, positive = pleasant
```

No prediction — observe-only appraisal. The value captures the direct hedonic quality of the consonance level, signed to reflect valence direction.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| CSG E2 | f09_consonance_valence [2] | Consonance-to-valence mapping, [-1,1] |
| R3 [3] | pleasant | Pleasantness driving valence |
| H3 | pleasant velocity H16 | Hedonic change rate |
| H3 | pleasant mean H16 | Sustained pleasantness |

---

## Kernel Usage

The consonance_valence_mapping appraisal provides a signed valence signal:

```python
# Phase 1 in scheduler:
consonance_valence = observe(csg_relay['consonance_valence'])
```

Unlike most beliefs which are [0,1], this belief uses [-1,1] range to capture bipolar valence. Positive values indicate pleasant (consonant) and negative values indicate unpleasant (dissonant). This feeds downstream to F5 Emotion for valence integration.

---

## Scientific Foundation

- **Bravo 2017**: Linear consonance-valence relationship (d=3.31)
- **Plomp & Levelt 1965**: Consonance-pleasantness foundation
- **Sethares 1993**: Roughness-based dissonance predicts unpleasantness

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/csg_relay.py`
