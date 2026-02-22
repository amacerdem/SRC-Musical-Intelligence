# plasticity_magnitude -- Appraisal Belief (TSCP)

**Category**: Appraisal (observe-only)
**Owner**: TSCP (SPU-beta2)

---

## Definition

"Auditory cortex reorganized by training." Observes the degree of cortical reorganization induced by musical training. High plasticity magnitude means the auditory cortex has substantially reorganized its frequency tuning curves and spectral representations in response to long-term instrument training. This is the bridge between training exposure and enhanced timbre recognition.

---

## Observation Formula

```
# From TSCP E-layer + M-layer:
plasticity_magnitude = 0.60 * f03_plasticity_magnitude + 0.40 * enhancement_function

# f03 = sigma(0.50 * f01 * timbre_change_std)
#   f01 = trained timbre response (spectral envelope match)
#   timbre_change_std = H3[(24, 8, 3, 0)]  -- timbre_change std 300ms fwd
#   Plasticity triggered by novel timbre patterns interacting with trained response

# enhancement_function = f01 * f02
#   f01 = trained timbre response
#   f02 = timbre specificity (selectivity index)
#   Enhancement selectivity -- ratio of trained to untrained response
```

No prediction -- observe-only appraisal. The value serves as an expertise marker consumed by ESME and downstream learning models.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| TSCP E2 | f03_plasticity_magnitude [2] | Degree of cortical reorganization |
| TSCP M0 | enhancement_function [3] | Enhancement selectivity (f01 * f02) |
| TSCP E0 | f01_trained_timbre_response [0] | Trained instrument response baseline |
| TSCP E1 | f02_timbre_specificity [1] | Trained vs untrained selectivity |
| H3 | (24, 8, 3, 0) | Timbre change std at 300ms -- plasticity trigger |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| ESME | Plasticity magnitude feeds expertise-dependent MMN enhancement |
| F1 Sensory | Cortical plasticity modulates sensory processing efficiency |
| Precision engine | Higher plasticity = more precise timbre predictions |

---

## Scientific Foundation

- **Pantev et al. 2001**: Enhancement magnitude correlates with training duration -- age-of-inception r=-0.634, p=.026 (MEG, N=17)
- **Leipold et al. 2021**: Robust musicianship effects on structural + functional connectivity replicable across AP/non-AP (fMRI+DWI, N=153)
- **Olszewska et al. 2021**: Longitudinal training changes in motor-auditory networks; arcuate fasciculus predicts learning -- predisposition + plasticity dual model
- **Whiteford et al. 2025**: Plasticity locus must be cortical, not brainstem (N>260, d=-0.064, BF=0.13 for null)

## Implementation

File: `Musical_Intelligence/brain/functions/f8/beliefs/plasticity_magnitude.py` (Phase 5)
