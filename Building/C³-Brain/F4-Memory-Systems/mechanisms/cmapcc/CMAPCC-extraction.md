# CMAPCC E-Layer — Explicit Features (3D)

**Model**: Cross-Modal Action-Perception Common Code (IMU-β9)
**Unit**: IMU (Integrative Memory Unit)
**Layer**: Extraction (E)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid
**Output Dim (total)**: 10D

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:f01_common_code | [0, 1] | Unified perception-action representation. Right PMC convergence zone. f01 = sigma(0.30*x_l4l5.mean + 0.35*stumpf + 0.35*periodicity). Coefficient sum: 1.00. The x_l4l5 interaction (derivatives x consonance) captures temporal dynamics coupled with pitch identity — the perception-action bridge. Bianco 2016: rIFG BA44 Z=4.29 as dorsal (action) convergence; BA45 Z=5.12 as ventral (audio) convergence (fMRI, N=29 pianists). |
| 1 | E1:f02_cross_modal_binding | [0, 1] | Auditory-motor integration strength. Cross-modal transfer capacity. f02 = sigma(0.35*x_l5l7.mean + 0.35*x_l0l5.mean + 0.30*onset*loudness). Coefficient sum: 1.00. Combines timbre-consonance binding (x_l5l7), energy-consonance perception (x_l0l5), and action dynamics (onset x loudness). Moller 2021: left IFOF FA correlates with cross-modal gain (t=3.38, p<0.001, DTI, N=45). |
| 2 | E2:f03_seq_generalization | [0, 1] | Pattern transfer across modalities. Sequence abstraction in right PMC. f03 = sigma(0.50*f01*f02 + 0.25*seq_coherence + 0.25*retrieval). Coefficient sum: 1.00. The product f01*f02 ensures both common code and cross-modal binding must be active for generalization. Di Liberto 2021: accurate melody decoding from both listening and imagery (note-onset F(1,20)=80.6, p=1.9e-8, EEG, N=21). |

---

## Design Rationale

1. **Common Code (E0)**: Captures the unified neural representation that bridges perception and action in right premotor cortex. Uses x_l4l5 (derivatives x consonance interaction) as the primary common code signal — temporal dynamics coupled with pitch identity reflects the shared format for hearing and playing musical sequences. Stumpf fusion (binding coherence) and periodicity (pitch regularity) support sequence identity. Primary evidence: Bianco 2016 showing dual-stream (dorsal fronto-parietal + ventral fronto-temporal) convergence in rIFG.

2. **Cross-Modal Binding (E1)**: Tracks the strength of auditory-motor integration. Uses three cross-domain signals: x_l5l7 (consonance x timbre = instrument-specific identity across modalities), x_l0l5 (energy x consonance = salience-weighted harmonic sequence), and onset x loudness (action dynamics). Supported by Moller 2021 showing that IFOF white matter structure supports audiovisual integration, and Paraskevopoulos 2022 showing enhanced compartmentalized connectivity in musicians.

3. **Sequence Generalization (E2)**: Captures whether learned patterns transfer across modalities. The multiplicative f01*f02 term ensures both common code and cross-modal binding are prerequisites for generalization. Sequence coherence (stumpf x periodicity) and retrieval from the mnemonic circuit add context. Supported by Di Liberto 2021 showing shared neural encoding between perceived and imagined melodies, and Lahav 2007 showing that brief motor training creates perceptual-action representations.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 16, 1, 2) | stumpf_fusion mean H16 L2 | Binding coherence at 1s for common code |
| (4, 16, 0, 2) | sensory_pleasantness value H16 L2 | Current sequence valence |
| (5, 16, 1, 2) | periodicity mean H16 L2 | Pitch regularity at 1s for common code |
| (10, 6, 0, 2) | onset_strength value H6 L2 | Beat-level note onsets for action dynamics |
| (8, 6, 0, 2) | loudness value H6 L2 | Beat-level intensity for action dynamics |
| (0, 16, 0, 2) | roughness value H16 L2 | Current dissonance for sequence identity |
| (1, 16, 1, 2) | sethares_dissonance mean H16 L2 | Interval quality at 1s |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | E0: harmonic quality (inverse) |
| [1] | sethares_dissonance | E0: interval identity |
| [3] | stumpf_fusion | E0+E2: binding coherence |
| [4] | sensory_pleasantness | E0: sequence valence |
| [5] | periodicity | E0+E2: pitch regularity |
| [8] | loudness | E1: arousal / motor engagement |
| [10] | onset_strength | E1: event salience / note onset |
| [25:33] | x_l0l5 | E1: perceptual sequence binding (energy x consonance) |
| [33:41] | x_l4l5 | E0: common code basis (derivatives x consonance) |
| [41:49] | x_l5l7 | E1: cross-modal binding (consonance x timbre) |

---

## Brain Regions

| Region | MNI Coordinates | Evidence | Function |
|--------|-----------------|----------|----------|
| Right IFG (BA44) | 44, 6, 26 | Direct (fMRI, Bianco 2016 Z=4.29, N=29) | Dorsal (action-seed) convergence for harmonic structure |
| Right IFG (BA45) | 44, 34, 2 | Direct (fMRI, Bianco 2016 Z=5.12, N=29) | Ventral (audio-seed) convergence for harmonic perception |
| SMA | 0, -6, 62 | Direct (fMRI + resting-state FC, Bianco 2016; Lahav 2007) | Motor sequence programming — action side of common code |
| Left IFOF | -31, -68, 5 | Direct (DTI, Moller 2021 t=3.38, p<0.001, N=45) | White matter pathway for audiovisual integration |

---

## Scientific Foundation

- **Bianco et al. (2016)**: Dissociable dorsal (fronto-parietal) and ventral (fronto-temporal) networks converge on rIFG for harmonic prediction (fMRI + resting-state FC, N=29 pianists; BA44 Z=4.29, BA45 Z=5.12)
- **Lahav et al. (2007)**: Listening to trained melodies activates bilateral premotor, IFG, SMA — motor training creates perceptual-action code (fMRI, N=9)
- **Di Liberto et al. (2021)**: Accurate melody decoding from listening and imagery; note-onset F(1,20)=80.6, p=1.9e-8 (EEG, N=21)
- **Moller et al. (2021)**: Left IFOF FA correlates with audiovisual gain (t=3.38, p<0.001, DTI, N=45)
- **Paraskevopoulos et al. (2022)**: Musicians show compartmentalized intra-network connectivity during multisensory learning (g=-1.09, MEG+PTE, N=25)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/cmapcc/extraction.py`
