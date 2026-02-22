# error_propagation — Appraisal Belief (SPH, F2)

**Type**: Appraisal (observe-only)
**Mechanism**: SPH (Relay, Depth 0)
**Function**: F2 Pattern Recognition & Prediction

---

## Definition

"Prediction error is propagating through the hierarchy."

---

## Observation Formula

```
observe = 0.40 * E1:alpha_beta_error[1]
        + 0.30 * P1:prediction_error[9]
        + 0.30 * M3:alpha_beta_power[7]
```

## Source Dimensions

| Weight | SPH Dim | Name | Rationale |
|--------|---------|------|-----------|
| 0.40 | [1] | E1:alpha_beta_error | Alpha-beta error activation |
| 0.30 | [9] | P1:prediction_error | Memory-level error signal |
| 0.30 | [7] | M3:alpha_beta_power | Oscillatory error signature |

## No Predict/Update Cycle

As an Appraisal belief, error_propagation is observe-only.

## Scientific Foundation

- **Carbajal & Malmierca 2018**: SSA + MMN = deviance detection, propagating IC→MGB→AC
- **Fong 2020**: MMN prediction error propagates upward through hierarchy

## Implementation

File: `Musical_Intelligence/brain/functions/f2/beliefs/sph/error_propagation.py`
