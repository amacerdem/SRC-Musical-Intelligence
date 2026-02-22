# oscillatory_signature — Appraisal Belief (SPH, F2)

**Type**: Appraisal (observe-only)
**Mechanism**: SPH (Relay, Depth 0)
**Function**: F2 Pattern Recognition & Prediction

---

## Definition

"The current oscillatory state reflects match vs mismatch processing."

---

## Observation Formula

```
observe = 0.40 * M2:gamma_power[6]
        + 0.30 * M3:alpha_beta_power[7]
        + 0.30 * E3:feedforward_feedback[3]
```

## Source Dimensions

| Weight | SPH Dim | Name | Rationale |
|--------|---------|------|-----------|
| 0.40 | [6] | M2:gamma_power | Match oscillatory signature |
| 0.30 | [7] | M3:alpha_beta_power | Mismatch oscillatory signature |
| 0.30 | [3] | E3:feedforward_feedback | Information flow direction |

## No Predict/Update Cycle

As an Appraisal belief, oscillatory_signature is observe-only.

## Scientific Foundation

- **Bonetti 2024**: gamma M>N, alpha-beta N>M; feedforward vs feedback
- **Golesorkhi 2021**: core-periphery hierarchy with distinct timescales

## Implementation

File: `Musical_Intelligence/brain/functions/f2/beliefs/sph/oscillatory_signature.py`
