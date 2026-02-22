# VRIAP E-Layer — Episodic Engagement (3D)

**Model**: VR-Integrated Analgesia Paradigm (IMU-β7)
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
| 0 | E0:f01_engagement | [0, 1] | Active motor engagement level. Premotor cortex + auditory-motor coupling. f01 = sigma(0.35*onset*x_l0l5.mean + 0.35*loudness*amp_vel + 0.30*mem_enc). Liang 2025: VRMS enhances bilateral PM&SMA FC vs VRAO (RPMSMA t=3.574, p=0.004 FDR, N=50). |
| 1 | E1:f02_pain_gate | [0, 1] | Pain gating signal (S1 connectivity reduction). S1 + insula pain matrix modulation. f02 = sigma(0.40*f01*mem_ret + 0.30*pleasantness + 0.30*(1-roughness)). Liang 2025: RS1 FC t=4.023, p=0.002 FDR (N=50). |
| 2 | E2:f03_multimodal | [0, 1] | Multi-modal binding strength. Hippocampal binding of auditory+visual+motor. f03 = sigma(0.35*stumpf*x_l5l7.mean + 0.35*mem_enc + 0.30*(1-entropy)). Bushnell 2013: mPFC/insula modulate pain through multi-modal cognitive control. |

---

## Design Rationale

1. **Active Motor Engagement (E0)**: Tracks how strongly the motor system engages with musical structure, producing efference copies that gate pain. Uses onset strength weighted by energy-consonance coupling (x_l0l5) and loudness modulated by amplitude velocity from H3. Primary basis: Liang 2025 showing VRMS-specific sensorimotor FC enhancement in PM&SMA.

2. **Pain Gating (E1)**: Models S1 connectivity reduction driven by motor engagement interacting with memory retrieval. Pleasant context (sensory_pleasantness) and low roughness create a safety signal that facilitates pain gating. Liang 2025: S1 FC significantly enhanced in VRMS condition (t=4.023, p=0.002).

3. **Multi-modal Binding (E2)**: Captures hippocampal integration of auditory, visual, and motor streams. Stumpf fusion weighted by timbre-consonance coupling (x_l5l7) provides binding coherence, while memory encoding and low entropy (predictable context) facilitate consolidation. Bushnell 2013: cognitive-emotional control of pain via multi-modal mPFC pathways.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (11, 16, 0, 2) | onset_strength value H16 L2 | Current motor cueing at 1s |
| (10, 16, 0, 2) | loudness value H16 L2 | Current engagement intensity |
| (7, 16, 8, 0) | amplitude velocity H16 L0 | Energy change rate at 1s — amp_vel signal |
| (4, 16, 0, 2) | sensory_pleasantness value H16 L2 | Current comfort level |
| (0, 16, 0, 2) | roughness value H16 L2 | Current dissonance (pain proxy, inverted) |
| (22, 16, 0, 2) | entropy value H16 L2 | Current unpredictability |
| (3, 16, 1, 2) | stumpf_fusion mean H16 L2 | Binding stability at 1s |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | E1: pain proxy (inverted for consonance/safety) |
| [3] | stumpf_fusion | E2: multi-modal binding coherence |
| [4] | sensory_pleasantness | E1: positive valence for pain reduction |
| [7] | amplitude | E0: engagement intensity baseline |
| [10] | loudness | E0: arousal correlate for immersion |
| [11] | onset_strength | E0: motor cueing signal |
| [22] | entropy | E2: predictability proxy (inverted) |
| [25:33] | x_l0l5 | E0: motor-sensory binding (energy x consonance) |
| [41:49] | x_l5l7 | E2: comfort-familiarity binding (consonance x timbre) |

---

## Brain Regions

| Region | Coordinates | Evidence | Function |
|--------|-------------|----------|----------|
| PM&SMA | +/-44, 0, 48 | Direct (fNIRS, Liang 2025 N=50) | Motor planning, efference copy generation |
| S1 | +/-42, -24, 54 | Direct (fNIRS, Liang 2025 N=50) | Pain signal propagation, connectivity reduced by active mode |
| Insula (Anterior) | +/-36, 16, 2 | Direct (fMRI, Putkinen 2025 N=30) | Pain awareness, interoceptive salience gating |
| Hippocampus | +/-20, -24, -12 | Inferred | Multi-modal binding, analgesic memory consolidation |

---

## Scientific Foundation

- **Liang et al. (2025)**: VRMS enhances bilateral PM&SMA FC vs VRAO (RPMSMA t=3.574, p=0.004; LPMSMA t=3.169, p=0.009 FDR, fNIRS, N=50)
- **Liang et al. (2025)**: RS1 FC enhancement in VRMS (t=4.023, p=0.002 FDR, N=50)
- **Putkinen et al. (2025)**: Pleasure-dependent BOLD in insula, ACC, SMA (cluster-level FWE p<0.05, fMRI, N=30)
- **Arican & Soyman (2025)**: Active task engagement > silence for analgesia (W=236.5, p=0.001, r_rb=0.491, N=123)
- **Bushnell et al. (2013)**: Cognitive and emotional control of pain via mPFC/insula pathways

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/vriap/extraction.py`
