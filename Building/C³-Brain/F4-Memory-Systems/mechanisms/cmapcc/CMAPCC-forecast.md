# CMAPCC F-Layer — Forecast (3D)

**Model**: Cross-Modal Action-Perception Common Code (IMU-β9)
**Unit**: IMU (Integrative Memory Unit)
**Layer**: Forecast (F)
**Indices**: [7:10]
**Scope**: internal
**Activation**: sigmoid
**Output Dim (total)**: 10D

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:transfer_pred | [0, 1] | Cross-modal transfer prediction (2-5s ahead). Will learning in one modality transfer to the other? Uses _predict_future() with common_code_strength and H20 (5s) window features. Based on consolidation trajectory of binding and sequence stability. Paraskevopoulos 2022: musicians show enhanced statistical learning transfer (g=-1.09, MEG+PTE, N=25). |
| 8 | F1:motor_seq_pred | [0, 1] | Motor sequence prediction (0.5-1s ahead). Right PMC -> action prediction. Uses _predict_future() with motor_entrainment from sensorimotor cross-circuit and H6 (200ms) beat-level window features. Predicts upcoming motor program activation based on onset and amplitude trajectories. Ross & Balasubramaniam 2022: premotor cortex enables beat-level action prediction. |
| 9 | F2:perceptual_seq_pred | [0, 1] | Perceptual sequence prediction (0.5-1s ahead). Right PMC -> auditory prediction. Uses _predict_future() with encoding_state from mnemonic circuit and H16 (1s) window features. Predicts upcoming perceptual sequence activation based on harmonic and onset trajectories. Di Liberto 2021: shared encoding between perceived and imagined melodies (EEG, N=21). |

---

## Design Rationale

1. **Transfer Prediction (F0)**: Projects whether cross-modal transfer will occur over the next 2-5 seconds. Uses the H20 (5s) consolidation window from H3, tracking the trajectory of common code strength. The prediction reflects that transfer requires time for hippocampal binding to consolidate the cross-modal representation. Supported by Paraskevopoulos 2022 showing that multisensory statistical learning drives broader connectivity changes over seconds-scale windows.

2. **Motor Sequence Prediction (F1)**: Projects the motor system's next action 0.5-1s ahead using beat-level (H6, 200ms) features. This short-horizon prediction enables anticipatory motor programming — the system predicts what the next motor action would be based on the ongoing rhythmic and onset pattern. Uses motor entrainment from the sensorimotor cross-circuit read. Ross & Balasubramaniam 2022 confirm that premotor cortex enables beat-level motor predictions through covert entrainment.

3. **Perceptual Sequence Prediction (F2)**: Projects the auditory system's expectation 0.5-1s ahead using bar-level (H16, 1s) features. This prediction enables anticipatory listening — the system predicts what pitch/harmonic event comes next based on the current melodic context. Uses encoding state from the mnemonic circuit. Supported by Di Liberto 2021 showing accurate melody decoding from both listening and imagery conditions, indicating that perceptual predictions share format with perceived sequences.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 20, 1, 0) | stumpf_fusion mean H20 L0 | Binding stability over 5s for transfer prediction |
| (5, 20, 19, 0) | periodicity stability H20 L0 | Sequence stability over 5s for transfer |
| (4, 24, 1, 0) | sensory_pleasantness mean H24 L0 | Long-term valence context for consolidation |
| (1, 24, 19, 0) | sethares_dissonance stability H24 L0 | Long-term interval stability for transfer |
| (7, 20, 18, 0) | amplitude trend H20 L0 | Intensity trajectory 5s for transfer context |
| (7, 6, 8, 0) | amplitude velocity H6 L0 | Action dynamics at beat for motor prediction |
| (10, 6, 0, 2) | onset_strength value H6 L2 | Beat-level onset for motor prediction |
| (11, 6, 0, 2) | spectral_flux value H6 L2 | Spectral change at beat for motor prediction |
| (11, 11, 1, 0) | spectral_flux mean H11 L0 | Mean flux at 500ms for perceptual prediction |
| (0, 20, 18, 0) | roughness trend H20 L0 | Dissonance trajectory for perceptual prediction |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | F2: dissonance trajectory for perceptual forecast |
| [3] | stumpf_fusion | F0: binding trajectory for transfer |
| [5] | periodicity | F0: sequence stability for transfer |
| [7] | amplitude | F0+F1: intensity trajectory and action dynamics |
| [10] | onset_strength | F1: motor event prediction |
| [11] | spectral_flux | F1+F2: spectral change for action and perception |

---

## Brain Regions

| Region | MNI Coordinates | Evidence | Function |
|--------|-----------------|----------|----------|
| Right IFG (BA44) | 44, 6, 26 | Direct (fMRI, Bianco 2016 Z=4.29, N=29) | Action prediction — dorsal stream output |
| Right IFG (BA45) | 44, 34, 2 | Direct (fMRI, Bianco 2016 Z=5.12, N=29) | Perceptual prediction — ventral stream output |
| Bilateral SPL (BA7) | 32, -78, 42 | Direct (fMRI, Bianco 2016 Z=4.66, N=29) | Visuomotor prediction — sensorimotor integration |
| SMA | 0, -6, 62 | Direct (fMRI, Bianco 2016; Lahav 2007) | Motor sequence prediction |

---

## Scientific Foundation

- **Paraskevopoulos et al. (2022)**: Musicians show increased compartmentalized connectivity during multisensory statistical learning (g=-1.09, MEG+PTE, N=25)
- **Ross & Balasubramaniam (2022)**: Motor networks causally involved in beat perception; TMS of premotor cortex disrupts beat timing (mini-review)
- **Di Liberto et al. (2021)**: Accurate melody decoding from listening and imagery; pitch decoding F(1,20)=142.3, p=1.5e-10 (EEG, N=21)
- **Porfyri et al. (2025)**: Multisensory training drives broader connectivity changes than unisensory (Group x Time: F(1,28)=4.635, p=0.042, eta-sq=0.168, EEG+GCA, N=30)
- **Takagi et al. (2025)**: Cross-modal generative models predict brain activity better than unimodal in IPS, precuneus, STS (fMRI, N=14)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/cmapcc/forecast.py`
