# episodic_encoding — Core Belief (HCMC)

**Category**: Core (full Bayesian PE)
**t**: 0.7
**Owner**: HCMC (IMU-b4)
**Multi-Scale**: 4 horizons, T_char = 4s

---

## Definition

"I am encoding this music pattern right now." Tracks the moment-by-moment hippocampal binding activation -- whether the brain is currently encoding the incoming musical features into a new episodic memory trace. High values indicate strong hippocampal CA3 autoassociative binding of the current musical input.

---

## Multi-Scale Horizons

```
H16(1s)  H18(2s)  H20(5s)  H21(8s)
```

T_char = 4s reflects the characteristic timescale of episodic encoding (longer than beat perception, shorter than autobiographical retrieval). H16 captures fast binding events; H18 covers the hippocampal binding window; H20 spans the consolidation horizon; H21 captures extended encoding episodes across phrases.

---

## Observation Formula

```
# HCMC binding state:
value = 0.40 * binding_state + 0.30 * fast_binding + 0.30 * segmentation_state

# Where:
# binding_state = HCMC P0 [5] -- current hippocampal binding activation
# fast_binding  = HCMC E0 [0] -- CA3 autoassociative binding of features
# segmentation_state = HCMC P1 [6] -- event boundary detection

# Precision: binding_state * novelty_signal / (H3_std + epsilon)
# Clamped [0.5, 10]
```

---

## Prediction Formula

```
predict = Linear(t * prev + w_trend * M18 + w_period * M14 + w_ctx * beliefs_{t-1})
```

Standard Bayesian PE cycle with gain = pi_obs / (pi_obs + pi_pred).

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| HCMC P0 | binding_state [5] | Primary hippocampal binding activation |
| HCMC P1 | segmentation_state [6] | Event boundary detection |
| HCMC E0 | fast_binding [0] | CA3 autoassociative fast binding |
| HCMC E1 | episodic_seg [1] | Episodic segmentation signal |
| HCMC E2 | cortical_storage [2] | Cortical consolidation (context) |
| R3 [3] | stumpf_fusion | Binding coherence proxy |
| R3 [21] | spectral_flux | Segmentation trigger |
| R3 [22] | entropy | Encoding difficulty |

---

## H3 Dependencies

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 16, 1, 2) | stumpf_fusion mean H16 L2 | Binding coherence at 1s |
| (21, 16, 1, 2) | spectral_flux mean H16 L2 | Current segmentation rate |
| (7, 20, 5, 0) | amplitude range H20 L0 | Energy dynamic range for binding |
| (5, 16, 1, 2) | harmonicity mean H16 L2 | Harmonic template at 1s |

---

## Scientific Foundation

- **Fernandez-Rubio et al. 2022**: Left hippocampus activated at 4th tone of memorized tonal sequences (MEG, N=71, MCS p<0.001)
- **Zacks et al. 2007**: Event segmentation theory -- boundaries trigger hippocampal encoding (behavioral + fMRI)
- **Sikka et al. 2015**: Age-related hippocampal-to-cortical shift for musical semantic memory (fMRI, N=40)
- **Rolls 2013**: CA3 autoassociative network for fast pattern binding (computational)
- **Cheung et al. 2019**: Hippocampal encoding of musical expectation uncertainty (fMRI, N=79, beta=-0.140, p=0.002)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/hcmc/` (pending)
