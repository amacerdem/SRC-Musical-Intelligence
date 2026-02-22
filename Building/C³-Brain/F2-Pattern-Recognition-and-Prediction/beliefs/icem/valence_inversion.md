# valence_inversion — Appraisal Belief (ICEM, F2)

**Type**: Appraisal (observe-only)
**Mechanism**: ICEM (Relay, Depth 0)
**Function**: F2 Pattern Recognition & Prediction

---

## Definition

"High IC is inverting valence (unexpected → negative feeling)."

---

## Observation Formula

```
observe = 0.40 * E2:valence_response[2]
        + 0.30 * M2:valence_pred[6]
        + 0.30 * P1:emotional_evaluation[10]
```

## Source Dimensions

| Weight | ICEM Dim | Name | Rationale |
|--------|----------|------|-----------|
| 0.40 | [2] | E2:valence_response | Emotional valence change from IC |
| 0.30 | [6] | M2:valence_pred | Mathematical valence prediction |
| 0.30 | [10] | P1:emotional_evaluation | Present-moment valence assessment |

## Scientific Foundation

- **Egermann 2013**: IC → valence↓ (Valence = -γ·IC + δ, p<0.001)
- **Gold 2019**: inverted-U for IC on liking — moderate IC maximizes pleasure

## Implementation

File: `Musical_Intelligence/brain/functions/f2/beliefs/icem/valence_inversion.py`
