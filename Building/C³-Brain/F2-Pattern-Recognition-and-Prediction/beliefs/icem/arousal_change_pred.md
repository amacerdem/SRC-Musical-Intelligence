# arousal_change_pred — Anticipation Belief (ICEM, F2)

**Type**: Anticipation (forward prediction)
**Mechanism**: ICEM (Relay, Depth 0)
**Function**: F2 Pattern Recognition & Prediction

---

## Definition

"Arousal will change in the near future (~1.3s)."

---

## Observation Formula

```
observe = F0:arousal_change_1_3s[11] (1.0)
```

## Source Dimensions

| Weight | ICEM Dim | Name | Rationale |
|--------|----------|------|-----------|
| 1.0 | [11] | F0:arousal_change_1_3s | Direct forecast layer output |

## Scientific Foundation

- **Salimpoor 2011**: dopamine release in caudate during anticipation of musical peaks (PET, N=8)
- **Egermann 2013**: IC peaks predict upcoming SCR responses

## Implementation

File: `Musical_Intelligence/brain/functions/f2/beliefs/icem/arousal_change_pred.py`
