# social_prediction_error — Appraisal Belief (SSRI)

**Category**: Appraisal (observe-only)
**Owner**: SSRI (RPU-beta4)

---

## Definition

"Coordination better/worse than expected." Observes the mismatch between expected and actual interpersonal coordination quality. Positive social prediction error (SPE > 0) indicates better-than-expected coordination -- a "reward surge" from surprising synchrony. Negative SPE indicates coordination breakdown below expectation. SPE extends the individual reward prediction error framework (RPEM) to the interpersonal domain.

---

## Observation Formula

```
# Direct read from SSRI M-layer:
social_prediction_error = SSRI.social_prediction_error[M0]  # index [5]

# SPE = f04_entrainment_quality - E[coordination]
# Range: [-1, 1] (tanh bounded)
# Positive SPE -> "better than expected coordination" -> reward surge
# Negative SPE -> coordination breakdown -> reward suppression

# NAcc_social = NAcc_solo + gamma * max(SPE, 0)
```

No prediction -- observe-only appraisal. SPE is computed as the difference between actual entrainment quality and expected coordination from prior context.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SSRI M0 | social_prediction_error [5] | Social RPE value |
| SSRI E3 | f04_entrainment_quality [3] | Actual coordination quality |
| Context | beliefs_{t-1} | Expected coordination baseline |

---

## Kernel Usage

Social prediction error feeds the reward formula:

```python
# Phase 3 in scheduler:
# Positive SPE amplifies reward; negative SPE suppresses
social_reward_signal = max(ssri_relay['social_prediction_error'], 0)
# Feeds F6 via: surprise component in reward formula
```

---

## Scientific Foundation

- **Cheung et al. 2019**: Uncertainty x surprise interaction predicts musical pleasure; amygdala, hippocampus, auditory cortex; NAcc reflects uncertainty (fMRI, N=39+24)
- **Kokal et al. 2011**: Joint drumming activates caudate nucleus; reward increases with synchrony quality; prosocial commitment enhanced (fMRI, N=24)
- **Spiech et al. 2022**: Noradrenergic arousal reflects precision-weighted prediction error for groove (pupillometry, N=30)
- **Gold et al. 2019**: Intermediate predictive complexity maximizes musical pleasure; inverted-U; learning-reward model (behavioral, N=43+27)

## Implementation

File: `Musical_Intelligence/brain/functions/f9/mechanisms/ssri.py`
