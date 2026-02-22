# detection_accuracy -- Appraisal Belief (SLEE)

**Category**: Appraisal (observe-only)
**Owner**: SLEE (NDU-beta3)

---

## Definition

"Detect statistical irregularities faster." Observes the current accuracy of irregularity detection -- how well the listener identifies deviations from the learned statistical distribution. High detection accuracy means the internal statistical model is well-calibrated and deviations are quickly and precisely identified. Musicians show significantly better detection accuracy than non-musicians (d=-1.09), reflecting their refined internal models.

---

## Observation Formula

```
# From SLEE E-layer + P-layer:
detection_accuracy = 0.60 * f02_detection_accuracy + 0.40 * expectation_formation

# f02 = sigma(0.35 * flux_std_100ms
#            + 0.35 * flux_mean_1s)
#   flux_std_100ms = H3[(10, 3, 2, 2)]  -- spectral_flux std at 100ms
#   flux_mean_1s = H3[(10, 16, 1, 2)]  -- spectral_flux mean over 1s
#   Irregularity identification rate based on spectral flux variability

# expectation_formation = current distribution model state
#   How well the expectation template has formed from exposure
```

No prediction -- observe-only appraisal. The value modulates precision weighting in downstream attention and prediction models.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SLEE E1 | f02_detection_accuracy [1] | Irregularity identification rate |
| SLEE P0 | expectation_formation [7] | Current distribution model state |
| H3 | (10, 3, 2, 2) | Spectral flux std at 100ms |
| H3 | (10, 16, 1, 2) | Spectral flux mean over 1s |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F3 Attention | Detection accuracy modulates precision weighting |
| statistical_model (Core) | f02 feeds the statistical model observation |
| ECT | Behavioral benefit measure despite compartmentalization cost |

---

## Scientific Foundation

- **Paraskevopoulos et al. 2022**: Musicians show superior accuracy in identification of multisensory statistical irregularities, Hedges' g=-1.09 (MEG+PTE, N=25)
- **Bridwell 2017**: r=0.65 correlation between pattern-related cortical sensitivity and MMN amplitude -- detection accuracy reflects internalized statistical model quality (EEG, N=13)
- **Fong et al. 2020**: MMN as prediction error under Bayesian framework -- detection accuracy is the behavioral manifestation of precision-weighted prediction error

## Implementation

File: `Musical_Intelligence/brain/functions/f8/mechanisms/slee/slee.py` (Phase 5)
