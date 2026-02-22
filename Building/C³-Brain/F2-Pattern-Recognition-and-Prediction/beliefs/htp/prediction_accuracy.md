# prediction_accuracy — Core Belief (HTP, F2)

**Type**: Core (full Bayesian PE cycle)
**Mechanism**: HTP (Relay, Depth 0)
**Function**: F2 Pattern Recognition & Prediction
**τ**: 0.5

---

## Definition

"My prediction was correct/wrong (post-stimulus silencing)."

---

## Observation Formula

```
observe = 0.50 * P0:sensory_match[7]
        + 0.30 * P1:pitch_prediction[8]
        + 0.20 * E3:hierarchy_gradient[3]
```

## Prediction Formula

```
predict = τ × prev + (1-τ) × 0.5
        + 0.04 × sharpness_trend
        + 0.03 × spectral_flux_velocity
        + 0.02 × prediction_hierarchy
```

## Source Dimensions

| Weight | HTP Dim | Name | Rationale |
|--------|---------|------|-----------|
| 0.50 | [7] | P0:sensory_match | Low-level match — primary accuracy |
| 0.30 | [8] | P1:pitch_prediction | Mid-level match |
| 0.20 | [3] | E3:hierarchy_gradient | Gradient quality modulates accuracy |

## Scientific Foundation

- **de Vries & Wurm 2023**: High-level silenced post-stimulus when correct
- **Forseth 2020**: Dual prediction in HG (timing) + PT (content)

## Implementation

File: `Musical_Intelligence/brain/functions/f2/beliefs/htp/prediction_accuracy.py`
