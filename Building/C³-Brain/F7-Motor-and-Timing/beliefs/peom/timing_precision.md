# timing_precision -- Appraisal Belief (PEOM)

**Category**: Appraisal (observe-only)
**Owner**: PEOM (MPU-alpha1)

---

## Definition

"Timing variance below self-paced baseline." Observes the degree to which motor timing variability has been reduced by auditory entrainment compared to self-paced conditions. High timing precision indicates that the entrained motor system achieves lower CV than unaided movement -- the hallmark of successful rhythmic auditory stimulation (RAS) in both healthy and clinical populations.

---

## Observation Formula

```
# From PEOM E-layer + M-layer:
timing_precision = 0.50*f03_variability_reduction + 0.50*cv_reduction

# f03 = sigma(0.35 * f01 * f02 + ...)
# cv_reduction = 1 - (CV_entrained / CV_self_paced)
# Range [0, 1]: 0 = no improvement, 1 = maximal CV reduction
```

No prediction -- observe-only appraisal. The value is a direct assessment of motor timing quality.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| PEOM E2 | f03_variability_reduction [2] | CV reduction function |
| PEOM M3 | cv_reduction [6] | Raw CV ratio metric |
| PEOM E0 | f01_period_entrainment [0] | Period lock contributes to f03 |
| PEOM E1 | f02_velocity_optimization [1] | Velocity smoothness contributes to f03 |

---

## Kernel Usage

The timing_precision appraisal feeds the precision engine for motor predictions:

```python
# Precision enrichment:
# Higher timing_precision -> higher pi_pred for motor Core beliefs
# pi_pred_motor *= 1 + 0.2 * timing_precision
```

---

## Scientific Foundation

- **Yamashita et al. 2025**: CV reduction from 4.51 to 2.80 with SMA+M1 gait-synchronized stimulation, d=-1.10, eta_p2=0.309 (RCT tDCS+tACS, N=16)
- **Thaut et al. 2015**: Period entrainment reduces motor variability across clinical populations (Review)
- **Repp 2005**: Sensorimotor synchronization: period correction mechanism reduces timing variability (Review)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/peom_relay.py`
