# CMAPCC P-Layer — Cognitive Present (2D)

**Model**: Cross-Modal Action-Perception Common Code (IMU-β9)
**Unit**: IMU (Integrative Memory Unit)
**Layer**: Cognitive Present (P)
**Indices**: [5:7]
**Scope**: internal
**Activation**: sigmoid / clamp [0, 1]
**Output Dim (total)**: 10D

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:pmc_activation | [0, 1] | Right premotor cortex activation level. Convergence of perception + action streams. pmc_activation = sigma(0.50*encoding_state.mean + 0.50*x_l4l5.mean). Coefficient sum: 1.00. Encoding state from the mnemonic circuit provides the perceptual component, while x_l4l5 (derivatives x consonance) provides the temporal-dynamics-coupled-with-pitch action component. Bianco 2016: rIFG BA44 Z=4.29 (action-seed, fMRI, N=29). Ross & Balasubramaniam 2022: motor networks causally involved in beat perception via covert entrainment. |
| 6 | P1:mirror_coupling | [0, 1] | Mirror neuron system engagement. Bidirectional perception-action mapping. mirror_coupling = sigma(0.50*pmc_activation*familiarity + 0.50*motor_entrainment). Coefficient sum: 1.00. The product pmc_activation*familiarity ensures mirror coupling requires both active PMC and stored representations. Motor entrainment from the sensorimotor cross-circuit provides real-time action coupling. Tanaka 2021: mu suppression d=0.72-0.86 during audiovisual perception (EEG, N=21). |

---

## Design Rationale

1. **PMC Activation (P0)**: Provides a real-time readout of right premotor cortex activation, the convergence zone where perception and action representations merge. The equal weighting of encoding state (perception side) and x_l4l5 interaction (action side) reflects the dual-stream architecture: both dorsal (fronto-parietal, action) and ventral (fronto-temporal, auditory) streams must contribute. Ross & Balasubramaniam 2022 confirm that motor networks are causally involved in beat perception through covert entrainment, meaning PMC activation occurs even during passive listening.

2. **Mirror Coupling (P1)**: Tracks the bidirectional mapping between perception and action. The multiplicative pmc_activation*familiarity term ensures mirror coupling is strongest when both the convergence zone is active AND the sequence is recognized from prior experience. Familiar sequences activate stronger mirror responses because stored motor programs can be matched to perceived patterns. Motor entrainment from the sensorimotor cross-circuit provides the real-time action component. Tanaka 2021 showed mu suppression (mirror neuron index) during audiovisual music performance with moderate-to-large effect sizes.

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 6, 0, 2) | onset_strength value H6 L2 | Beat-level note onsets for PMC action stream |
| (8, 6, 0, 2) | loudness value H6 L2 | Beat-level intensity for PMC action stream |
| (7, 6, 8, 0) | amplitude velocity H6 L0 | Action dynamics at beat level |
| (11, 6, 0, 2) | spectral_flux value H6 L2 | Spectral change at beat for event detection |
| (0, 16, 0, 2) | roughness value H16 L2 | Current harmonic quality for encoding context |
| (4, 16, 0, 2) | sensory_pleasantness value H16 L2 | Current valence for encoding modulation |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [7] | amplitude | P0: action dynamics via velocity |
| [8] | loudness | P0+P1: intensity for motor coupling |
| [10] | onset_strength | P0: event salience for action stream |
| [11] | spectral_flux | P0: spectral change for event detection |
| [33:41] | x_l4l5 | P0: common code basis (derivatives x consonance) |

---

## Brain Regions

| Region | MNI Coordinates | Evidence | Function |
|--------|-----------------|----------|----------|
| Right IFG (BA44) | 44, 6, 26 | Direct (fMRI, Bianco 2016 Z=4.29, N=29) | PMC activation — action-seed dorsal convergence |
| Right pSTG/STS | 48, -32, 0 | Direct (fMRI, Bianco 2016 Z=3.92, N=29) | Auditory encoding — spectrotemporal sequence representation |
| Frontal-central-parietal | EEG scalp | Direct (EEG, Tanaka 2021 d=0.72-0.86, N=21) | Mirror coupling — mu suppression during audiovisual music |
| SMA | 0, -6, 62 | Direct (fMRI, Bianco 2016; Lahav 2007) | Motor sequence — covert entrainment during listening |

---

## Scientific Foundation

- **Bianco et al. (2016)**: rIFG BA44 Z=4.29 (action-seed), pSTG Z=3.92 (perception-seed); dual-stream convergence for harmonic prediction (fMRI, N=29 pianists)
- **Tanaka (2021)**: Mu suppression at FC2 d=-0.72, Cz d=-0.78, CP1 d=-0.86, CP6 d=-0.72 (FDR p=0.027) during audiovisual opera (EEG, N=21)
- **Ross & Balasubramaniam (2022)**: Motor networks causally involved in beat perception via covert entrainment; TMS of parietal/premotor disrupts beat timing (mini-review)
- **Bigand et al. (2025)**: Disentangled neural signals for auditory tracking, motor control, and partner observation during dyadic dance (EEG + mTRF)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/cmapcc/cognitive_present.py`
