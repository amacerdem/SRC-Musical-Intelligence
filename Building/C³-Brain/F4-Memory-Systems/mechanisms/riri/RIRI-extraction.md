# RIRI E-Layer — Extraction (3D)

**Layer**: Extraction (E)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:multimodal_entrainment | [0, 1] | Multi-modal rhythmic entrainment. SMA + premotor convergent temporal input. f01 = sigma(0.35 * flux_val * onset_val * mean(beat_induction[0:10]) + 0.35 * x_l0l5_coupling + 0.30 * onset_periodicity). Thaut 2015: period entrainment drives motor optimization via reticulospinal pathways. |
| 1 | E1:sensorimotor_integration | [0, 1] | Cross-modal sensorimotor integration. Cerebellum + IPL prediction coupling. f02 = sigma(0.35 * loudness_mean * mean(motor_entrainment[20:30]) + 0.35 * x_l4l5_coupling + 0.30 * energy_periodicity). Harrison 2025: SMA + putamen + sensorimotor cortex activation during musical cues. |
| 2 | E2:enhanced_recovery | [0, 1] | Integration synergy (multi > uni). Hippocampus + mPFC session consolidation. f03 = sigma(0.30 * connectivity_mean + 0.30 * pleasantness_mean + 0.20 * f01 + 0.20 * f02). Blasi 2025: 20 RCTs (N=718) structural + functional neuroplasticity from music rehab. |

---

## Design Rationale

1. **Multi-modal Entrainment (E0)**: Tracks how strongly all modality channels (auditory RAS, visual VR, haptic robotics) lock to a common rhythmic clock. Uses spectral flux and onset strength at the beat level (H6, 200ms) combined with motor-auditory coupling (x_l0l5). Primary basis: Thaut 2015 period entrainment, Liang 2025 music+VR>VR alone for SMA/premotor activation.

2. **Sensorimotor Integration (E1)**: Measures cross-modal prediction coupling in the cerebellum and inferior parietal lobule. Loudness provides motor drive intensity, x_l4l5 captures derivative-consonance coupling (sensorimotor prediction), and energy periodicity reflects rhythmic regularity. Harrison 2025: cerebellum activated during internal cueing.

3. **Enhanced Recovery (E2)**: The integration synergy signal -- captures how multi-modal rehabilitation exceeds unimodal RAS. Combines connectivity coupling (x_l5l7 mean at H16) with sensory pleasantness, gated by the product of f01 and f02. The multiplicative dependency ensures all pathways must contribute. Blasi 2025: structural neuroplasticity from music-based rehabilitation.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 6, 0, 0) | spectral_flux value H6 L0 | Current onset detection at beat level |
| (10, 6, 17, 0) | spectral_flux peaks H6 L0 | Beat count per 200ms window |
| (11, 6, 0, 0) | onset_strength value H6 L0 | Event onset precision |
| (11, 6, 14, 2) | onset_strength periodicity H6 L2 | Rhythmic regularity at beat level |
| (25, 6, 0, 2) | x_l0l5[0] value H6 L2 | Entrainment coupling signal |
| (8, 11, 1, 0) | loudness mean H11 L0 | Mean loudness over motor window |
| (33, 11, 0, 2) | x_l4l5[0] value H11 L2 | Sensorimotor coupling signal |
| (33, 11, 17, 0) | x_l4l5[0] peaks H11 L0 | Sensorimotor peak events |
| (22, 11, 14, 2) | energy_change periodicity H11 L2 | Intensity regularity |
| (41, 16, 1, 0) | x_l5l7[0] mean H16 L0 | Mean connectivity coupling |
| (4, 16, 1, 0) | sensory_pleasantness mean H16 L0 | Sustained pleasantness |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [4] | sensory_pleasantness | E2: motor valence proxy |
| [7] | amplitude | E1: motor drive intensity |
| [8] | loudness | E1: perceptual intensity |
| [10] | spectral_flux | E0: onset detection trigger |
| [11] | onset_strength | E0: beat precision |
| [12] | warmth | E1: therapeutic comfort signal |
| [14] | tonalness | E2: melodic clarity |
| [21] | spectral_change | E1: adaptive challenge modulation |
| [22] | energy_change | E1: motor effort tracking |
| [23] | pitch_change | E1: melodic guidance signal |
| [25:33] | x_l0l5 | E0: auditory-motor coupling (RAS) |
| [33:41] | x_l4l5 | E1: sensorimotor integration |
| [41:49] | x_l5l7 | E2: connectivity coupling |

---

## Scientific Foundation

- **Thaut, McIntosh & Hoemberg 2015**: Period entrainment drives motor optimization via reticulospinal pathways (review)
- **Harrison et al. 2025**: SMA + putamen + sensorimotor cortex during musical cues in PD (fMRI)
- **Liang et al. 2025**: Music + VR > VR alone for SMA/premotor activation (fNIRS, N=26)
- **Blasi et al. 2025**: Structural + functional neuroplasticity from music/dance rehab (20 RCTs, N=718)
- **Huang & Qi 2025**: Music bypasses basal ganglia via auditory-motor networks in PD (review)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/riri/extraction.py`
