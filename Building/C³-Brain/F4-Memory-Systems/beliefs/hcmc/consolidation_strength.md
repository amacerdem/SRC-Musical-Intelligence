# consolidation_strength — Appraisal Belief (HCMC)

**Category**: Appraisal (observe-only)
**Owner**: HCMC (IMU-b4)

---

## Definition

"Hippocampal to cortical transfer strength." Reflects the degree to which cortical networks (mPFC, PCC) are actively receiving consolidated traces from the hippocampus. High consolidation means active transfer from short-term hippocampal to long-term cortical storage. Uses consonance-timbre interactions (x_l5l7) and harmonic stability as templates for durable cortical storage.

---

## Observation Formula

```
# Direct read from HCMC P-layer:
consolidation_strength = HCMC.storage_state[P2]  # index [7]

# Formula (in mechanism): sigma(0.35 * x_l5l7.mean * harmonicity_mean_5s
#                              + 0.35 * harmonicity * tonalness_autocorr_5s
#                              + 0.30 * (1 - entropy) * tonalness)
# Cortical storage uses consonance-timbre interactions as the
# template signal for durable long-term memory consolidation.
```

No prediction -- observe-only appraisal. The value is directly consumed by the learning rate adjustment and indicates memory permanence.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| HCMC P2 | storage_state [7] | Primary cortical storage activation |
| HCMC E2 | cortical_storage [2] | E-layer consolidation computation |
| R3 [5] | harmonicity | Harmonic template match |
| R3 [14] | tonalness | Melodic encoding quality |
| R3 [22] | entropy | Encoding difficulty (inverse) |
| R3 [41:49] | x_l5l7 | Cortical long-term template |
| H3 | (5, 20, 1, 0) | harmonicity mean H20 L0 -- harmonic stability over 5s |
| H3 | (14, 20, 22, 0) | tonalness autocorrelation H20 L0 -- tonal repetition over 5s |
| H3 | (10, 24, 3, 0) | loudness std H24 L0 -- salience variability over 36s |

---

## Kernel Usage

The consolidation_strength appraisal feeds learning rate and memory permanence:

```python
# Phase 2a in scheduler:
# learning_rate *= 1 + w_consol * hcmc_relay['storage_state']
# High consolidation = stronger long-term encoding
```

This modulates how quickly and permanently musical patterns are stored: high consolidation strength indicates the hippocampal-to-cortical transfer pipeline is active, leading to durable memory traces in mPFC and PCC.

---

## Brain Regions

| Region | MNI Coordinates | Role |
|--------|-----------------|------|
| Hippocampus | +/-20, -24, -12 | Source: episodic trace origin |
| mPFC | 0, 52, 12 | Target: cortical storage |
| PCC / Cingulate | 0, -52, 26 | Target: episodic recollection |
| Entorhinal Cortex | +/-24, -12, -24 | Gateway: sensory input relay |

---

## Scientific Foundation

- **Sikka et al. 2015**: Age-related hippocampal-to-cortical shift for musical semantic memory (fMRI, N=40)
- **Liu et al. 2024**: Replay-triggered hippocampal-cortical transfer (EEG-fMRI, N=33)
- **Buzsaki 2015**: Sharp-wave ripples drive hippocampal-cortical transfer and forecast consolidation outcome (review)
- **Billig et al. 2022**: Hippocampal auditory processing via EC-DG-CA3-CA1 trisynaptic pathway (review)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/hcmc/` (pending)
