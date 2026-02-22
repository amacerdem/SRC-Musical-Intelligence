# sequence_match — Core Belief (SPH, F2)

**Type**: Core (full Bayesian PE cycle)
**Mechanism**: SPH (Relay, Depth 0)
**Function**: F2 Pattern Recognition & Prediction
**τ**: 0.45

---

## Definition

"The incoming sequence matches a memorised pattern."

---

## Observation Formula

```
observe = 0.40 * E0:gamma_match[0]
        + 0.30 * P0:memory_match[8]
        + 0.30 * M2:gamma_power[6]
```

## Prediction Formula

```
predict = τ × prev + (1-τ) × 0.5
        + 0.04 × tonal_stability_trend
        + 0.03 × pitch_salience_velocity
        + 0.02 × prediction_hierarchy
```

## Source Dimensions

| Weight | SPH Dim | Name | Rationale |
|--------|---------|------|-----------|
| 0.40 | [0] | E0:gamma_match | Gamma activation — primary match indicator |
| 0.30 | [8] | P0:memory_match | Memory-level match confirmation |
| 0.30 | [6] | M2:gamma_power | Oscillatory match signature |

## Scientific Foundation

- **Bonetti 2024**: memorised → positive ~350ms, gamma M>N
- **Fernandez-Rubio 2022**: tonal recognition engages hippocampus + cingulate

## Implementation

File: `Musical_Intelligence/brain/functions/f2/beliefs/sph/sequence_match.py`
