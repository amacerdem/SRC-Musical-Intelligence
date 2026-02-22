# VRIAP P-Layer — Cognitive Present (2D)

**Model**: VR-Integrated Analgesia Paradigm (IMU-β7)
**Unit**: IMU (Integrative Memory Unit)
**Layer**: Cognitive Present (P)
**Indices**: [5:7]
**Scope**: internal
**Activation**: clamp [0, 1]
**Output Dim (total)**: 10D

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:motor_pain_state | [0, 1] | Current motor-pain gating activation. Product of encoding state and engagement level: motor_pain_state = (encoding_state * f01_engagement), clamped to [0,1]. Tracks the real-time motor-pain interaction where active engagement gates nociceptive input. Liang 2025: VRMS enhances S1-motor connectivity (t=4.023, p=0.002). |
| 6 | P1:s1_connectivity | [0, 1] | S1 connectivity proxy (inverse = analgesic). Higher values indicate more pain gating (less S1 connectivity). s1_connectivity = pain_gate.mean(), clamped to [0,1]. Represents current state of primary somatosensory cortex connectivity reduction. Liang 2025: VRMS > VRAO for RS1 FC (t=4.023, p=0.002 FDR). |

---

## Design Rationale

1. **Motor-Pain State (P0)**: Captures the instantaneous motor-pain gating state. The product of encoding state (from the mnemonic circuit) and motor engagement (f01) creates a signal that is only active when both memory encoding is engaged AND the motor system is actively coupled with musical structure. This reflects the gate control mechanism: efference copies from active motor engagement suppress pain signal propagation through S1.

2. **S1 Connectivity (P1)**: Provides a running estimate of primary somatosensory cortex connectivity reduction. Higher values mean greater pain gating (i.e., less S1 connectivity to the pain matrix). This is directly derived from the pain gate signal (f02) averaged over the current window, representing the steady-state level of pain modulation at any given moment.

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (11, 16, 0, 2) | onset_strength value H16 L2 | Current motor cueing for motor-pain state |
| (10, 16, 0, 2) | loudness value H16 L2 | Current engagement intensity |
| (7, 16, 8, 0) | amplitude velocity H16 L0 | Energy change rate — tracks motor dynamics |
| (21, 16, 0, 2) | spectral_flux value H16 L2 | Current event salience |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [7] | amplitude | P0: energy dynamics for motor-pain interaction |
| [10] | loudness | P0: engagement intensity modulation |
| [11] | onset_strength | P0: motor cueing for active gating |
| [21] | spectral_flux | P0: event detection drives motor response |
| [25:33] | x_l0l5 | P0: motor-sensory binding strength |

---

## Brain Regions

| Region | Coordinates | Evidence | Function |
|--------|-------------|----------|----------|
| S1 | +/-42, -24, 54 | Direct (fNIRS, Liang 2025 N=50) | Pain signal propagation, connectivity reduction in active mode |
| PM&SMA | +/-44, 0, 48 | Direct (fNIRS, Liang 2025 N=50) | Efference copy generation for motor-pain gating |
| DLPFC | +/-42, 34, 28 | Direct (fNIRS, Liang 2025 N=50) | Cognitive control — VRMS enhances RDLPFC-S1/PM&SMA hetero-FC (p<0.05 FDR) |

---

## Scientific Foundation

- **Liang et al. (2025)**: VRMS > VRAO S1 FC (t=4.023, p=0.002 FDR, fNIRS, N=50); RDLPFC-S1/PM&SMA/M1 hetero-FC enhanced (p<0.05 FDR)
- **Liang et al. (2025)**: VRMS > VRMI bilateral M1 activation (RM1 z=-2.196, p=0.028; LM1 t=2.065, p=0.044)
- **Melzack & Wall (1965)**: Gate control theory — motor engagement generates non-nociceptive input that gates pain
- **Garza-Villarreal et al. (2017)**: Moderate pooled analgesic effects of music across chronic pain conditions (systematic review + meta-analysis)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/vriap/cognitive_present.py`
