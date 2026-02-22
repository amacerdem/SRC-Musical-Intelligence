# valence_shift_pred — Anticipation Belief (ICEM, F2)

**Type**: Anticipation (forward prediction)
**Mechanism**: ICEM (Relay, Depth 0)
**Function**: F2 Pattern Recognition & Prediction

---

## Definition

"Valence will shift in the near future (~2.5s)."

---

## Observation Formula

```
observe = F1:valence_shift_2_5s[12] (1.0)
```

## Source Dimensions

| Weight | ICEM Dim | Name | Rationale |
|--------|----------|------|-----------|
| 1.0 | [12] | F1:valence_shift_2_5s | Direct forecast layer output |

## Scientific Foundation

- **Gold 2019**: pleasure depends on joint uncertainty and surprise (p<0.001)
- **Gold 2023**: VS reflects liked surprises during naturalistic music (fMRI, N=24)

## Implementation

File: `Musical_Intelligence/brain/functions/f2/beliefs/icem/valence_shift_pred.py`
