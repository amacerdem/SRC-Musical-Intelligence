# CMAPCC M-Layer — Temporal Integration (2D)

**Model**: Cross-Modal Action-Perception Common Code (IMU-β9)
**Unit**: IMU (Integrative Memory Unit)
**Layer**: Temporal Integration (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: arithmetic / sigmoid
**Output Dim (total)**: 10D

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:common_code_strength | [0, 1] | Overall common code activation. Balanced average of E-layer: common_code_strength = (f01 + f02 + f03) / 3. Provides a single scalar summary of the perception-action common code state. Equal weighting reflects that all three E-layer components (common code, cross-modal binding, sequence generalization) contribute equally to the unified representation. Bianco 2016: dual-stream convergence requires both dorsal and ventral activations. |
| 4 | M1:transfer_probability | [0, 1] | P(cross-modal transfer). transfer_prob = sigma(0.40*familiarity + 0.30*motor_coupling + 0.30*seq_coherence). Coefficient sum: 1.00. Familiarity is the strongest predictor (0.40) because cross-modal transfer requires a stored representation. Motor coupling (from beat-entrainment cross-circuit) and sequence coherence (stumpf x periodicity) provide the action and perception components. Lahav 2007: motor training creates action representations of sound. |

---

## Design Rationale

1. **Common Code Strength (M0)**: Aggregates the three E-layer signals into a unified measure of perception-action code activation. The arithmetic mean ensures balanced contribution — all three components must be active for a strong common code. This mirrors the theoretical requirement that common code formation requires simultaneous perceptual encoding (f01), cross-modal binding (f02), and successful generalization (f03). If any component is weak, overall strength drops proportionally.

2. **Transfer Probability (M1)**: Estimates the likelihood that learning in one modality (e.g., listening) will transfer to the other (e.g., performing). Familiarity receives the highest weight (0.40) because cross-modal transfer fundamentally requires a stored representation — you cannot transfer what has not been encoded. Motor coupling (0.30) from the sensorimotor cross-circuit read provides the action template, and sequence coherence (0.30) ensures the harmonic-temporal pattern is stable enough to transfer. This is supported by Lahav 2007 showing that brief piano training creates listening-based action representations.

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 20, 1, 0) | stumpf_fusion mean H20 L0 | Binding over 5s consolidation for transfer estimate |
| (5, 20, 19, 0) | periodicity stability H20 L0 | Sequence stability over 5s for coherence |
| (10, 11, 14, 0) | onset_strength periodicity H11 L0 | Onset regularity at 500ms for motor coupling |
| (8, 11, 8, 0) | loudness velocity H11 L0 | Intensity dynamics at 500ms for motor coupling |
| (10, 16, 1, 0) | onset_strength mean H16 L0 | Mean onset over 1s bar |
| (8, 16, 1, 0) | loudness mean H16 L0 | Mean intensity over bar |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [3] | stumpf_fusion | M1: sequence coherence component (binding) |
| [5] | periodicity | M1: sequence coherence component (regularity) |
| [8] | loudness | M1: motor coupling intensity |
| [10] | onset_strength | M1: motor coupling event rate |

---

## Brain Regions

| Region | MNI Coordinates | Evidence | Function |
|--------|-----------------|----------|----------|
| Bilateral STG | 60, -32, 8 | Direct (fMRI, Bianco 2016 R: Z=3.46) | Auditory encoding — perception side for transfer |
| SMA | 0, -6, 62 | Direct (fMRI, Bianco 2016; Lahav 2007) | Motor sequence programming — action side for transfer |
| Frontal-central-parietal | EEG scalp | Direct (EEG, Tanaka 2021 d=0.72-0.86) | Mirror neuron system — mu suppression indexes coupling |
| Bilateral SPL (BA7) | 32, -78, 42 | Direct (fMRI, Bianco 2016 Z=4.66) | Visuomotor transformation for musical action |

---

## Scientific Foundation

- **Lahav et al. (2007)**: Action representation of sound — brief motor training creates listening-based premotor activation (fMRI, N=9)
- **Tanaka (2021)**: Mu suppression at FC/Cz/CP during audiovisual opera — mirror neuron engagement requires multimodal input (EEG, N=21, d=0.72-0.86)
- **Bangert & Schlaug (2006)**: Musicians show enhanced grey matter in motor/auditory regions — structural basis for common code (VBM, N=26)
- **Olszewska et al. (2021)**: Musical training drives neuroplasticity in motor-auditory connectivity; arcuate fasciculus FA predicts learning success (review)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/cmapcc/temporal_integration.py`
