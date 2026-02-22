# episodic_boundary — Appraisal Belief (HCMC)

**Category**: Appraisal (observe-only)
**Owner**: HCMC (IMU-b4)

---

## Definition

"Phrase ended, new one began." Detects event boundaries -- moments where the hippocampus closes one episodic segment and opens another. High values indicate a major structural boundary (phrase end, section change). Combines spectral flux (change magnitude) with entropy (unpredictability) as confirmatory signals for boundary detection.

---

## Observation Formula

```
# Direct read from HCMC P-layer:
episodic_boundary = HCMC.segmentation_state[P1]  # index [6]

# Formula (in mechanism): sigma(0.40 * flux * flux_mean_1s
#                              + 0.30 * entropy * flux
#                              + 0.30 * onset_str * flux)
# Spectral flux is the primary boundary trigger; entropy and onset
# strength provide confirmatory signals.
```

No prediction -- observe-only appraisal. The value is directly consumed by the salience mixer for boundary detection and the familiarity computation for segment structure.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| HCMC P1 | segmentation_state [6] | Primary episodic boundary signal |
| HCMC E1 | episodic_seg [1] | E-layer segmentation computation |
| R3 [21] | spectral_flux | Primary boundary trigger |
| R3 [22] | entropy | Pattern unpredictability at boundary |
| R3 [11] | onset_strength | Event boundary marker |
| H3 | (21, 16, 1, 2) | spectral_flux mean H16 L2 -- segmentation rate at 1s |
| H3 | (21, 16, 3, 2) | spectral_flux std H16 L2 -- flux variability at 1s |

---

## Kernel Usage

The episodic_boundary appraisal feeds the salience mixer and familiarity:

```python
# Phase 1 in scheduler:
# salience_relay += w_boundary * hcmc_relay['segmentation_state']
# familiarity segment tracking uses boundary for reset
```

This creates boundary-driven salience peaks: musical structure transitions (phrase ends, key changes, section boundaries) generate salience spikes that drive attention and encoding.

---

## Scientific Foundation

- **Zacks et al. 2007**: Event segmentation theory -- boundaries trigger hippocampal encoding (behavioral + fMRI)
- **Sridharan et al. 2007**: Salience network activates at musical event boundaries (fMRI)
- **Fernandez-Rubio et al. 2022**: Tonal sequence recognition activates hippocampus + cingulate (MEG, N=71, MCS p<0.001)
- **Billig et al. 2022**: Hippocampal auditory processing via EC-DG-CA3-CA1 trisynaptic pathway (review)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/hcmc/` (pending)
