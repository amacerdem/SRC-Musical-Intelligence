# hierarchy_coherence — Appraisal Belief (HTP, F2)

**Type**: Appraisal (observe-only)
**Mechanism**: HTP (Relay, Depth 0)
**Function**: F2 Pattern Recognition & Prediction

---

## Definition

"The hierarchical prediction structure is coherent."

---

## Observation Formula

```
observe = 0.50 * E3:hierarchy_gradient[3]
        + 0.30 * P2:abstract_prediction[9]
        + 0.20 * P1:pitch_prediction[8]
```

## Source Dimensions

| Weight | HTP Dim | Name | Rationale |
|--------|---------|------|-----------|
| 0.50 | [3] | E3:hierarchy_gradient | Gradient strength — primary coherence indicator |
| 0.30 | [9] | P2:abstract_prediction | Abstract pattern match |
| 0.20 | [8] | P1:pitch_prediction | Mid-level template match |

## No Predict/Update Cycle

As an Appraisal belief, hierarchy_coherence is observe-only.

## Implementation

File: `Musical_Intelligence/brain/functions/f2/beliefs/htp/hierarchy_coherence.py`
