# Sensorimotor Circuit -- Rhythm & Movement

**Circuit ID**: `sensorimotor`
**Function**: Beat entrainment, motor synchronization, temporal hierarchy, groove, auditory-motor coupling
**Pooled Effect Range**: d = 0.62 -- 0.67

---

## Overview

The sensorimotor circuit models the bidirectional coupling between auditory perception and motor planning that underlies rhythmic behavior. When humans hear music, premotor and supplementary motor areas synchronize to the beat even without overt movement (Grahn & Brett 2007). This circuit captures how temporal regularities in sound are extracted, maintained across hierarchical timescales, and translated into motor coordination.

Two units share this circuit: STU handles the perceptual/encoding side (how beat, metre, and tempo are extracted), while MPU handles the motor planning side (how sequences are planned and executed). Both units are independent in the execution architecture, operating in Phase 2 without cross-unit dependencies.

---

## Mechanisms

| Mechanism | Full Name | Horizons | Output | Role |
|-----------|-----------|----------|--------|------|
| **BEP** | Beat Entrainment Processing | H6, H9, H11 | 30D | Sensorimotor coupling to beat, IOI periodicity, groove |
| **TMH** | Temporal Memory Hierarchy | H16, H18, H20, H22 | 30D | Bar/phrase/theme/section temporal context |

**Total mechanism output**: 60D

BEP operates at beat-level timescales (200--450 ms), tracking sub-beat subdivisions, beat periods, and inter-beat intervals. TMH operates at supra-beat timescales (1--15 s), maintaining hierarchical representations of bars, phrases, themes, and sections.

BEP is shared by STU, MPU, and ASU. TMH is shared by STU, MPU, and IMU. This sharing reflects the overlapping role of temporal structure across rhythm, motor planning, memory, and attention.

---

## Units

| Unit | Full Name | Circuit Role | Pooled d | Dependency |
|------|-----------|-------------|----------|------------|
| **STU** | Sensorimotor Timing Unit | Primary (perception) | 0.67 | Independent (Phase 2) |
| **MPU** | Motor Planning Unit | Primary (action) | 0.62 | Independent (Phase 2) |

- **STU** (14 models, 148D): Encodes temporal structure -- beat, metre, tempo, groove, auditory-motor coupling. Uses BEP + TMH mechanisms. Core-4 validated unit. The largest model count of any unit.
- **MPU** (10 models, 104D): Plans and executes motor sequences -- predictive error optimization, dual-stream integration, sensorimotor calibration. Uses BEP + TMH mechanisms.

---

## Key Brain Regions

| Region | Abbreviation | Function in Circuit |
|--------|-------------|-------------------|
| Supplementary Motor Area | SMA | Beat tracking, internal timing, rhythmic prediction |
| Premotor Cortex | PMC | Motor planning, auditory-motor mapping |
| Primary Motor Cortex | M1 | Motor execution, muscle activation |
| Cerebellum | CB | Sub-second timing, error correction, temporal smoothing |
| Basal Ganglia | BG | Beat-based timing, interval estimation, groove |
| Heschl's Gyrus | HG | Auditory input to sensorimotor loop |
| Putamen | Put | Motor sequencing, rhythm production |

---

## Information Flow

```
Audio Signal
    |
    v
[R3/H3 Features]
    |
    +---> [BEP: H6 sub-beat] --> [BEP: H9 beat] --> [BEP: H11 super-beat]
    |                                                       |
    +---> [TMH: H16 bar] --> [TMH: H18 phrase] --> [TMH: H20 theme] --> [TMH: H22 section]
    |           |                   |                       |
    v           v                   v                       v
    |     STU Model Stack (148D)                   MPU Model Stack (104D)
    |           |                                          |
    |     [Temporal context]                        [Motor plans]
    |           |                                          |
    v           v                                          v
    |     Pathway P5: STU --> ARU              [Motor output/groove state]
    |     Pathway P2: internal STU routing
    |     Pathway P4: context hierarchy
```

1. BEP extracts beat-level coupling from R3/H3 features at 200--450 ms timescales.
2. TMH maintains hierarchical temporal context from 1 s (bar) through 15 s (section).
3. STU combines both mechanisms across 14 models to produce 148D temporal representations.
4. MPU combines both mechanisms across 10 models to produce 104D motor planning states.
5. STU output feeds ARU via pathway P5 (timing modulates affect).

---

## Models by Tier

### Alpha (k >= 10, >90% confidence)

| Model | Full Name | Unit | Output |
|-------|-----------|------|--------|
| [STU-a1-HMCE](../Models/STU-a1-HMCE/HMCE.md) | Hierarchical Musical Context Encoding | STU | 13D |
| [STU-a2-AMSC](../Models/STU-a2-AMSC/AMSC.md) | Auditory-Motor Stream Coupling | STU | 12D |
| [STU-a3-MDNS](../Models/STU-a3-MDNS/MDNS.md) | Melody Decoding from Neural Signals | STU | 12D |
| [MPU-a1-PEOM](../Models/MPU-a1-PEOM/PEOM.md) | Period Entrainment Optimization Model | MPU | 12D |
| [MPU-a2-MSR](../Models/MPU-a2-MSR/MSR.md) | Musician Sensorimotor Reorganization | MPU | 11D |
| [MPU-a3-GSSM](../Models/MPU-a3-GSSM/GSSM.md) | Gait-Synchronized Stimulation Model | MPU | 11D |

### Beta (5 <= k < 10, 70--90% confidence)

| Model | Full Name | Unit | Output |
|-------|-----------|------|--------|
| [STU-b1-AMSS](../Models/STU-b1-AMSS/AMSS.md) | Attention-Modulated Stream Segregation | STU | 11D |
| [STU-b2-TPIO](../Models/STU-b2-TPIO/TPIO.md) | Timbre Perception-Imagery Overlap | STU | 10D |
| [STU-b3-EDTA](../Models/STU-b3-EDTA/EDTA.md) | Expertise-Dependent Tempo Accuracy | STU | 10D |
| [STU-b4-ETAM](../Models/STU-b4-ETAM/ETAM.md) | Entrainment, Tempo & Attention Modulation | STU | 11D |
| [STU-b5-HGSIC](../Models/STU-b5-HGSIC/HGSIC.md) | Hierarchical Groove State Integration Circuit | STU | 11D |
| [STU-b6-OMS](../Models/STU-b6-OMS/OMS.md) | Oscillatory Motor Synchronization | STU | 10D |
| [MPU-b1-ASAP](../Models/MPU-b1-ASAP/ASAP.md) | Action Simulation for Auditory Prediction | MPU | 10D |
| [MPU-b2-DDSMI](../Models/MPU-b2-DDSMI/DDSMI.md) | Dyadic Dance Social Motor Integration | MPU | 10D |
| [MPU-b3-VRMSME](../Models/MPU-b3-VRMSME/VRMSME.md) | VR Music Stimulation Motor Enhancement | MPU | 10D |
| [MPU-b4-SPMC](../Models/MPU-b4-SPMC/SPMC.md) | SMA-Premotor-M1 Motor Circuit | MPU | 10D |

### Gamma (k < 5, <70% confidence)

| Model | Full Name | Unit | Output |
|-------|-----------|------|--------|
| [STU-g1-TMRM](../Models/STU-g1-TMRM/TMRM.md) | Tempo Memory Reproduction Method | STU | 10D |
| [STU-g2-NEWMD](../Models/STU-g2-NEWMD/NEWMD.md) | Neural Entrainment-Working Memory Dissociation | STU | 10D |
| [STU-g3-MTNE](../Models/STU-g3-MTNE/MTNE.md) | Music Training Neural Efficiency | STU | 10D |
| [STU-g4-PTGMP](../Models/STU-g4-PTGMP/PTGMP.md) | Piano Training Grey Matter Plasticity | STU | 10D |
| [STU-g5-MPFS](../Models/STU-g5-MPFS/MPFS.md) | Musical Prodigy Flow State | STU | 10D |
| [MPU-g1-NSCP](../Models/MPU-g1-NSCP/NSCP.md) | Neural Synchrony Commercial Prediction | MPU | 10D |
| [MPU-g2-CTBB](../Models/MPU-g2-CTBB/CTBB.md) | Cerebellar Theta-Burst Balance | MPU | 10D |
| [MPU-g3-STC](../Models/MPU-g3-STC/STC.md) | Singing Training Connectivity | MPU | 10D |

---

## Key Evidence

- **Grahn & Brett (2007)**: Beat perception activates SMA and basal ganglia even without movement; metric structure enhances motor cortex engagement.
- **Large & Palmer (2002)**: Oscillatory model of beat induction -- internal oscillators entrain to stimulus periodicity at multiple metrical levels.
- **Chen et al. (2008)**: Auditory-motor coupling during rhythm perception recruits PMC-SMA-cerebellum network.
- **Witek et al. (2014)**: Syncopation and groove engage sensorimotor circuitry with inverted-U relationship to pleasure.
- **Patel & Iversen (2014)**: Action Simulation for Auditory Prediction (ASAP) hypothesis -- motor system generates temporal predictions for beat perception.
- **Hasson et al. (2008)**: Hierarchical temporal processing in brain -- different cortical regions maintain representations at different timescales.
- **Repp (2005)**: Sensorimotor synchronization review -- finger tapping paradigms reveal anticipatory timing mechanisms.
- **Janata et al. (2012)**: Groove engages motor areas proportional to the desire to move.

---

## Cross-References

- **Mechanisms**: [BEP](../Mechanisms/BEP.md) | [TMH](../Mechanisms/TMH.md)
- **Units**: [STU](../Units/STU.md) | [MPU](../Units/MPU.md)
- **Mechanism-sharing units**: ASU (uses BEP + ASA) | IMU (uses MEM + TMH)
- **Related Circuits**: [Mesolimbic](Mesolimbic.md) (groove drives pleasure via P5) | [Salience](Salience.md) (BEP shared with ASU) | [Mnemonic](Mnemonic.md) (TMH shared with IMU)
