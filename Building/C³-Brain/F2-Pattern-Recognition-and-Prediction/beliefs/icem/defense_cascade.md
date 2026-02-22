# defense_cascade — Appraisal Belief (ICEM, F2)

**Type**: Appraisal (observe-only)
**Mechanism**: ICEM (Relay, Depth 0)
**Function**: F2 Pattern Recognition & Prediction

---

## Definition

"A defense cascade (orienting → threat appraisal) is active."

---

## Observation Formula

```
observe = 0.50 * E3:defense_cascade[3]
        + 0.30 * M3:scr_pred[7]
        + 0.20 * M4:hr_pred[8]
```

## Source Dimensions

| Weight | ICEM Dim | Name | Rationale |
|--------|----------|------|-----------|
| 0.50 | [3] | E3:defense_cascade | Threat appraisal activation |
| 0.30 | [7] | M3:scr_pred | SCR prediction (arousal + defense) |
| 0.20 | [8] | M4:hr_pred | HR prediction (deceleration) |

## Scientific Foundation

- **Egermann 2013**: subjective unexpected → SCR↑, HR↓, RespR↑ (defense cascade pattern, p<0.001)

## Implementation

File: `Musical_Intelligence/brain/functions/f2/beliefs/icem/defense_cascade.py`
