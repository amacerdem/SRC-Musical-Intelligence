# Salience Circuit -- Attention & Novelty

**Circuit ID**: `salience`
**Function**: Auditory attention capture, salience detection, novelty/deviance processing, arousal gating
**Pooled Effect Range**: d = 0.55 -- 0.60

---

## Overview

The salience circuit models how the brain detects, prioritizes, and responds to unexpected or attention-demanding auditory events. It encompasses two complementary processes: bottom-up salience detection (sudden onsets, spectral deviance, interaural differences) and top-down novelty evaluation (mismatch negativity, statistical learning violations, prediction error correction).

Two units share this circuit. ASU handles salience detection and attention capture -- the fast, involuntary "what is that?" response to acoustically prominent events. NDU handles novelty detection and expectation violation -- the slower, more cognitive "that was unexpected" response driven by comparison against learned statistical models of auditory regularities.

---

## Mechanisms

| Mechanism | Full Name | Horizons | Output | Role |
|-----------|-----------|----------|--------|------|
| **ASA** | Auditory Scene Analysis | H3, H6, H9 | 30D | Stream segregation, attention gating, salience weighting |

**Direct mechanism output**: 30D (ASA only)

ASA is the single mechanism directly assigned to the salience circuit. It operates at fast timescales (23.2 ms -- 350 ms) where grouping and segregation cues operate: onset synchrony, harmonicity, spatial proximity, and spectral continuity.

However, both ASU and NDU combine ASA with mechanisms from other circuits:
- **ASU** uses BEP (from sensorimotor) + ASA: beat-level entrainment informs salience assessment.
- **NDU** uses PPC (from perceptual) + ASA: pitch processing feeds deviance detection.

---

## Units

| Unit | Full Name | Circuit Role | Pooled d | Dependency |
|------|-----------|-------------|----------|------------|
| **ASU** | Auditory Salience Unit | Primary (attention) | 0.60 | Independent (Phase 2) |
| **NDU** | Novelty Detection Unit | Primary (novelty) | 0.55 | Independent (Phase 2) |

- **ASU** (9 models, 94D): Detects and prioritizes salient auditory events -- sudden onsets, spectral deviance, interaural differences, and bottom-up attention capture. Uses BEP + ASA mechanisms.
- **NDU** (9 models, 94D): Detects deviations from expected auditory patterns -- mismatch negativity (MMN), spectral deviance, statistical learning violations, and error correction. Uses PPC + ASA mechanisms.

---

## Key Brain Regions

| Region | Abbreviation | Function in Circuit |
|--------|-------------|-------------------|
| Anterior Insula | aINS | Salience detection, interoceptive awareness, arousal gating |
| Dorsal Anterior Cingulate Cortex | dACC | Conflict monitoring, surprise signaling, error detection |
| Temporo-Parietal Junction | TPJ | Attention reorienting to salient events |
| Inferior Frontal Gyrus | IFG | Deviance detection, mismatch response generation |
| Bilateral Temporal Cortex | bTC | Auditory change detection, MMN generation |
| Right Frontal Cortex | rFC | Involuntary attention capture, novelty P3a |

---

## Information Flow

```
Audio Signal
    |
    v
[R3/H3 Features]
    |
    +---> [ASA: H3 micro-segregation] --> [ASA: H6 stream formation] --> [ASA: H9 object tracking]
    |           |                                |                              |
    |           v                                v                              v
    |     [Primitive grouping]          [Schema-based grouping]        [Salience map]
    |                                                                          |
    +--- [BEP: beat coupling] --+---> ASU Model Stack (94D) <-----------------+
    |                           |           |
    +--- [PPC: pitch chain] ----+---> NDU Model Stack (94D) <-----------------+
                                            |
                                            v
                                    [Attention / Novelty Signals]
                                            |
                                +-----------+-----------+
                                |                       |
                                v                       v
                    [Feeds into ARU               [Feeds into PCU
                     via arousal gating]           via prediction error]
```

1. ASA decomposes acoustic input into perceptual streams at gamma-to-beat timescales.
2. ASU combines ASA with BEP (beat entrainment) to assess salience within rhythmic context.
3. NDU combines ASA with PPC (pitch processing) to detect pitch-based deviations from expectations.
4. Both units output attention and novelty signals that gate downstream processing.

---

## Models by Tier

### Alpha (k >= 10, >90% confidence)

| Model | Full Name | Unit | Output |
|-------|-----------|------|--------|
| [ASU-a1-SNEM](../Models/ASU-a1-SNEM/SNEM.md) | Selective Neural Entrainment Model | ASU | 12D |
| [ASU-a2-IACM](../Models/ASU-a2-IACM/IACM.md) | Inharmonicity-Attention Capture Model | ASU | 11D |
| [ASU-a3-CSG](../Models/ASU-a3-CSG/CSG.md) | Consonance-Salience Gradient | ASU | 12D |
| [NDU-a1-MPG](../Models/NDU-a1-MPG/MPG.md) | Melodic Processing Gradient | NDU | 12D |
| [NDU-a2-SDD](../Models/NDU-a2-SDD/SDD.md) | Supramodal Deviance Detection | NDU | 11D |
| [NDU-a3-EDNR](../Models/NDU-a3-EDNR/EDNR.md) | Expertise-Dependent Network Reorganization | NDU | 11D |

### Beta (5 <= k < 10, 70--90% confidence)

| Model | Full Name | Unit | Output |
|-------|-----------|------|--------|
| [ASU-b1-BARM](../Models/ASU-b1-BARM/BARM.md) | Beat Ability Regulatory Model | ASU | 10D |
| [ASU-b2-STANM](../Models/ASU-b2-STANM/STANM.md) | Spectrotemporal Attention Network Model | ASU | 10D |
| [ASU-b3-AACM](../Models/ASU-b3-AACM/AACM.md) | Aesthetic-Attention Coupling Model | ASU | 10D |
| [NDU-b1-DSP](../Models/NDU-b1-DSP/DSP.md) | Developmental Singing Plasticity | NDU | 10D |
| [NDU-b2-CDMR](../Models/NDU-b2-CDMR/CDMR.md) | Context-Dependent Mismatch Response | NDU | 10D |
| [NDU-b3-SLEE](../Models/NDU-b3-SLEE/SLEE.md) | Statistical Learning Expertise Enhancement | NDU | 10D |

### Gamma (k < 5, <70% confidence)

| Model | Full Name | Unit | Output |
|-------|-----------|------|--------|
| [ASU-g1-PWSM](../Models/ASU-g1-PWSM/PWSM.md) | Precision-Weighted Salience Model | ASU | 10D |
| [ASU-g2-DGTP](../Models/ASU-g2-DGTP/DGTP.md) | Domain-General Temporal Processing | ASU | 10D |
| [ASU-g3-SDL](../Models/ASU-g3-SDL/SDL.md) | Salience-Dependent Lateralization | ASU | 10D |
| [NDU-g1-SDDP](../Models/NDU-g1-SDDP/SDDP.md) | Sex-Dependent Developmental Plasticity | NDU | 10D |
| [NDU-g2-ONI](../Models/NDU-g2-ONI/ONI.md) | Over-Normalization in Intervention | NDU | 10D |
| [NDU-g3-ECT](../Models/NDU-g3-ECT/ECT.md) | Expertise Compartmentalization Trade-off | NDU | 10D |

---

## Key Evidence

- **Bregman (1990)**: Foundational theory of auditory scene analysis -- primitive (bottom-up) and schema-based (top-down) grouping processes.
- **Menon & Uddin (2010)**: Anterior insula and dACC form the core "salience network" that detects behaviorally relevant stimuli across modalities.
- **Naatanen et al. (2007)**: Mismatch negativity (MMN) as pre-attentive deviance detector -- auditory cortex generates prediction error signals for unexpected events.
- **Escera & Corral (2007)**: Auditory novelty processing recruits frontal attention networks; novel sounds produce P3a component reflecting involuntary attention shift.
- **Saarinen et al. (1992)**: MMN to abstract rule violations demonstrates that the auditory system extracts and stores regularities for comparison.
- **Koelsch et al. (2009)**: Musical expectation violations produce ERAN (early right anterior negativity) in IFG, analogous to linguistic surprise.
- **Parmentier (2014)**: Deviant sounds capture attention involuntarily, disrupting ongoing task performance -- evidence for automatic salience detection.

---

## Cross-References

- **Mechanisms**: [ASA](../Mechanisms/ASA.md)
- **Units**: [ASU](../Units/ASU.md) | [NDU](../Units/NDU.md)
- **Mechanism-sharing**: ASU shares BEP with sensorimotor circuit | NDU shares PPC with perceptual circuit
- **Related Circuits**: [Perceptual](Perceptual.md) (PPC feeds NDU deviance detection) | [Sensorimotor](Sensorimotor.md) (BEP feeds ASU beat-salience) | [Mesolimbic](Mesolimbic.md) (novelty/surprise drives reward prediction error)
