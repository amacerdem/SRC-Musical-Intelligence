# arousal_scaling — Appraisal Belief (ICEM, F2)

**Type**: Appraisal (observe-only)
**Mechanism**: ICEM (Relay, Depth 0)
**Function**: F2 Pattern Recognition & Prediction

---

## Definition

"The current IC level is producing arousal scaling."

---

## Observation Formula

```
observe = 0.40 * E1:arousal_response[1]
        + 0.30 * M1:arousal_pred[5]
        + 0.30 * P0:surprise_signal[9]
```

## Source Dimensions

| Weight | ICEM Dim | Name | Rationale |
|--------|----------|------|-----------|
| 0.40 | [1] | E1:arousal_response | Physiological activation from IC |
| 0.30 | [5] | M1:arousal_pred | Mathematical arousal prediction |
| 0.30 | [9] | P0:surprise_signal | Present-moment surprise signal |

## Scientific Foundation

- **Egermann 2013**: IC → arousal↑ (Arousal = α·IC + β, p<0.001)
- **Salimpoor 2011**: anticipatory arousal → caudate dopamine release

## Implementation

File: `Musical_Intelligence/brain/functions/f2/beliefs/icem/arousal_scaling.py`
