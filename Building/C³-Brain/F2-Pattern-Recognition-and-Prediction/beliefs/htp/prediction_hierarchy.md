# prediction_hierarchy — Core Belief (HTP, F2)

**Type**: Core (full Bayesian PE cycle)
**Mechanism**: HTP (Relay, Depth 0)
**Function**: F2 Pattern Recognition & Prediction
**τ**: 0.4

---

## Definition

"Abstract/mid/low-level patterns are predictable ahead."

---

## Observation Formula

```
observe = 0.40 * E0:high_level_lead[0]
        + 0.30 * E1:mid_level_lead[1]
        + 0.30 * E2:low_level_lead[2]
```

## Prediction Formula

```
predict = τ × prev + (1-τ) × 0.5
        + 0.05 × tonal_stability_trend
        + 0.03 × onset_periodicity
        + 0.02 × abstract_future
```

## Source Dimensions

| Weight | HTP Dim | Name | Rationale |
|--------|---------|------|-----------|
| 0.40 | [0] | E0:high_level_lead | Abstract prediction — strongest indicator |
| 0.30 | [1] | E1:mid_level_lead | Perceptual prediction |
| 0.30 | [2] | E2:low_level_lead | Sensory prediction |

## Scientific Foundation

- **de Vries & Wurm 2023**: ηp²=0.49 for hierarchical prediction timing
- **Golesorkhi 2021**: Core-periphery hierarchy η²=0.86

## Implementation

File: `Musical_Intelligence/brain/functions/f2/beliefs/htp/prediction_hierarchy.py`
