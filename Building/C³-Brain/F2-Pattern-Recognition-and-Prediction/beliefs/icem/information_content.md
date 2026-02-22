# information_content — Core Belief (ICEM, F2)

**Type**: Core (full Bayesian PE cycle)
**Mechanism**: ICEM (Relay, Depth 0)
**Function**: F2 Pattern Recognition & Prediction
**τ**: 0.35

---

## Definition

"The current event is unexpected (high information content)."

---

## Observation Formula

```
observe = 0.40 * E0:information_content[0]
        + 0.30 * M0:ic_value[4]
        + 0.30 * P0:surprise_signal[9]
```

## Prediction Formula

```
predict = τ × prev + (1-τ) × 0.5
        + 0.05 × spectral_flux_trend
        + 0.03 × entropy_velocity
        + 0.02 × prediction_hierarchy
```

## Source Dimensions

| Weight | ICEM Dim | Name | Rationale |
|--------|----------|------|-----------|
| 0.40 | [0] | E0:information_content | Raw IC proxy — primary surprise |
| 0.30 | [4] | M0:ic_value | Refined IC with melodic entropy |
| 0.30 | [9] | P0:surprise_signal | Present-moment IC assessment |

## Scientific Foundation

- **Egermann 2013**: IC peaks predict emotional responses (p<0.001, N=50)
- **Cheung 2019**: uncertainty × surprise → pleasure (R²=0.654)

## Implementation

File: `Musical_Intelligence/brain/functions/f2/beliefs/icem/information_content.py`
