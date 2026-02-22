# RIRI P-Layer — Cognitive Present (2D)

**Layer**: Present Processing (P)
**Indices**: [5:7]
**Scope**: exported (kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:entrainment_state | [0, 1] | Current multi-modal entrainment quality. Combines beat induction with onset signal. sigma(0.50 * x_l0l5_val + 0.50 * flux_val * onset_val). Reflects the real-time "are all channels locked to the rhythm" signal. Thaut 2015: auditory rhythm primes motor system via reticulospinal pathways. |
| 6 | P1:motor_adaptation | [0, 1] | Current motor adaptation state. sigma(0.50 * x_l4l5_val + 0.50 * amplitude_velocity). Tracks how effectively the sensorimotor system is adjusting to the rhythmic input. Yamashita 2025: gait-synchronized M1+SMA stimulation reduces step variability. |

---

## Design Rationale

1. **Entrainment State (P0)**: The summary "present-moment" signal for multi-modal entrainment quality. This is the primary relay output that the kernel scheduler reads. It reflects whether the auditory RAS master clock has successfully entrained all rehabilitation modalities (visual, haptic). High entrainment state indicates effective phase-locking across channels.

2. **Motor Adaptation (P1)**: Tracks real-time sensorimotor adaptation -- how the motor system is responding to and adjusting with the rhythmic input. Uses sensorimotor coupling (x_l4l5) and amplitude velocity (rate of intensity change). High motor adaptation indicates the closed-loop rehabilitation system is effectively modulating difficulty.

---

## Kernel Relay Export

P-layer outputs are the primary relay exports for RIRI:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `entrainment_state` | P0 [5] | Beat entrainment belief: multi-modal component |
| `motor_adaptation` | P1 [6] | Motor belief: adaptation state |

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (25, 6, 0, 2) | x_l0l5[0] value H6 L2 | Entrainment coupling at beat level |
| (7, 11, 0, 2) | amplitude value H11 L2 | Current motor drive |
| (7, 11, 8, 0) | amplitude velocity H11 L0 | Intensity change rate |
| (33, 11, 0, 2) | x_l4l5[0] value H11 L2 | Sensorimotor coupling |

P-layer primarily aggregates E+M outputs with real-time H3 features.

---

## Brain Regions

| Region | MNI Coordinates | P-Layer Role |
|--------|-----------------|--------------|
| SMA | 0, -6, 62 | P0: multi-modal entrainment hub |
| Premotor Cortex | +/-44, 0, 48 | P0+P1: motor preparation |
| Cerebellum | +/-24, -64, -28 | P1: sensorimotor prediction error |
| Putamen | +/-24, 4, -2 | P0: basal ganglia timing |
| M1 | +/-36, -22, 54 | P1: motor execution |

---

## Scientific Foundation

- **Thaut, McIntosh & Hoemberg 2015**: Auditory rhythm primes motor system via reticulospinal pathways (review)
- **Harrison et al. 2025**: SMA + putamen activation during musically-cued movement (fMRI, PD+HC)
- **Yamashita et al. 2025**: Gait-synchronized M1+SMA tACS reduces step variability (pilot RCT, N=15)
- **Ross & Balasubramaniam 2022**: Sensorimotor simulation during rhythm perception (review)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/riri/cognitive_present.py`
