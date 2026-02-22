# midlevel_future — Anticipation Belief (HTP, F2)

**Type**: Anticipation (forward prediction)
**Mechanism**: HTP (Relay, Depth 0)
**Function**: F2 Pattern Recognition & Prediction

---

## Definition

"Upcoming mid-level features ~200ms ahead."

---

## Observation Formula

```
observe = F1:midlevel_future_200ms[11] (1.0)
```

## Downstream

- Feeds F7 Motor (period_entrainment.predict()) as context
- Feeds F3 Attention (attention_capture) mid-level expectation

## Scientific Foundation

- **de Vries & Wurm 2023**: View-dependent predictions ~200ms ahead
- **Norman-Haignere 2022**: Belt cortex 200-400ms integration

## Implementation

File: `Musical_Intelligence/brain/functions/f2/beliefs/htp/midlevel_future.py`
