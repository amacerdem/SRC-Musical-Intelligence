# spectral_complexity — Appraisal Belief (SDED, F1)

**Type**: Appraisal (observe-only)
**Mechanism**: SDED (Relay, Depth 0)
**Function**: F1 Sensory Processing

---

## Definition

"The spectral content is complex / has multiple dissonance sources."

---

## Observation Formula

```
observe = 0.40 * M0:detection_function[3]
        + 0.30 * P0:roughness_detection[4]
        + 0.30 * P1:deviation_detection[5]
```

**Range**: [0, 1] — weighted sum of [0,1] bounded SDED outputs.

---

## Source Dimensions

| Weight | SDED Dim | Name | Rationale |
|--------|----------|------|-----------|
| 0.40 | [3] | M0:detection_function | Overall detection strength — primary indicator |
| 0.30 | [4] | P0:roughness_detection | Roughness quality at sensory level |
| 0.30 | [5] | P1:deviation_detection | Change from context — novelty indicator |

---

## Design Rationale

Spectral complexity is high when:
- Detection function is strong (M0 > 0.5): clear dissonance signal
- Roughness quality is high (P0 > 0.5): spectral interference is well-defined
- Deviation is large (P1 > 0.3): roughness is changing, indicating multiple interacting sources

The 40/30/30 weighting emphasizes the integrated detection function while balancing raw roughness quality and contextual change.

---

## No Predict/Update Cycle

As an Appraisal belief, spectral_complexity is observe-only:
- No prior (tau), no baseline
- No Bayesian update
- No prediction error

It provides a moment-by-moment assessment of spectral dissonance complexity without maintaining temporal expectations.

---

## Scientific Foundation

- **Crespo-Bojorque 2018**: Universal early detection provides the neural substrate
- **Fishman 2001**: A1 phase-locked activity quantifies roughness complexity
- **Trulla 2018**: Recurrence patterns measure spectral interaction complexity

## Implementation

File: `Musical_Intelligence/brain/functions/f1/beliefs/sded/spectral_complexity.py`
