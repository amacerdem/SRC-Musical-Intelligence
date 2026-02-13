# C3 Neural Circuits -- Index

**Total**: 6 functional circuits spanning 9 cognitive units and 10 mechanisms
**Version**: 2.0.0
**Date**: 2026-02-13

---

## Overview

Circuits are functional neural pathways that group units and mechanisms by their cognitive role in music processing. Each circuit represents a distinct aspect of the brain's response to music -- from low-level spectral analysis through temporal structure, memory, attention, and reward. Units and mechanisms may participate in multiple circuits through shared mechanism assignments.

The architecture defines two circuit registries:

- **`CIRCUIT_NAMES`** (6 circuits): The full conceptual set including imagery.
- **`CIRCUITS`** (5 circuits): The operational set used for cross-unit pathway routing (excludes imagery, which is emergent rather than structural).

---

## Circuit Summary

| Circuit | Description | Mechanisms | Units | Key Brain Regions |
|---------|-------------|-----------|-------|-------------------|
| [**Mesolimbic**](Mesolimbic.md) | Reward & Pleasure | AED, CPD, C0P | ARU, RPU | NAcc, VTA, Amygdala, vmPFC, OFC |
| [**Perceptual**](Perceptual.md) | Hearing & Pattern | PPC, TPC | SPU | Heschl's Gyrus, PT, PP, IC |
| [**Sensorimotor**](Sensorimotor.md) | Rhythm & Movement | BEP, TMH | STU, MPU | SMA, PMC, Cerebellum, BG |
| [**Mnemonic**](Mnemonic.md) | Memory & Familiarity | MEM, SYN | IMU, PCU | Hippocampus, mPFC, IFG, dlPFC |
| [**Salience**](Salience.md) | Attention & Novelty | ASA | ASU, NDU | aInsula, dACC, TPJ, IFG |
| [**Imagery**](Imagery.md) | Simulation & Prediction | (PPC, TPC, MEM)* | PCU* | AC, IFG, STS, Hipp |

*Imagery reuses mechanisms from perceptual and mnemonic circuits; PCU is the primary unit.

---

## Unit-to-Circuit Assignments

| Unit | Primary Circuit | Pooled d | Models | Output |
|------|----------------|----------|--------|--------|
| SPU | perceptual | 0.84 | 9 | 99D |
| STU | sensorimotor | 0.67 | 14 | 148D |
| IMU | mnemonic | 0.53 | 15 | 159D |
| ARU | mesolimbic | 0.83 | 10 | 120D |
| ASU | salience | 0.60 | 9 | 94D |
| NDU | salience | 0.55 | 9 | 94D |
| MPU | sensorimotor | 0.62 | 10 | 104D |
| PCU | mnemonic | 0.58 | 9 | 94D |
| RPU | mesolimbic | 0.70 | 9 | 94D |

---

## Mechanism-to-Circuit Assignments

| Mechanism | Full Name | Circuit | Output | Horizons |
|-----------|-----------|---------|--------|----------|
| AED | Affective Entrainment Dynamics | mesolimbic | 30D | H6, H16 |
| CPD | Chills & Peak Detection | mesolimbic | 30D | H9, H16, H18 |
| C0P | Cognitive Projection | mesolimbic | 30D | H18, H19, H20 |
| PPC | Pitch Processing Chain | perceptual | 30D | H0, H3, H6 |
| TPC | Timbre Processing Chain | perceptual | 30D | H6, H12, H16 |
| BEP | Beat Entrainment Processing | sensorimotor | 30D | H6, H9, H11 |
| TMH | Temporal Memory Hierarchy | sensorimotor | 30D | H16, H18, H20, H22 |
| MEM | Memory Encoding / Retrieval | mnemonic | 30D | H18, H20, H22, H25 |
| SYN | Syntactic Processing | mnemonic | 30D | H12, H16, H18 |
| ASA | Auditory Scene Analysis | salience | 30D | H3, H6, H9 |

---

## Cross-Circuit Mechanism Sharing

Units draw mechanisms from circuits other than their primary assignment:

| Unit | Primary Circuit | Mechanisms Used | Source Circuits |
|------|----------------|----------------|-----------------|
| SPU | perceptual | PPC + TPC | perceptual |
| STU | sensorimotor | BEP + TMH | sensorimotor |
| IMU | mnemonic | MEM + TMH | mnemonic + sensorimotor |
| ARU | mesolimbic | AED + CPD | mesolimbic |
| ASU | salience | BEP + ASA | sensorimotor + salience |
| NDU | salience | PPC + ASA | perceptual + salience |
| MPU | sensorimotor | BEP + TMH | sensorimotor |
| PCU | mnemonic | PPC + TPC + MEM | perceptual + mnemonic |
| RPU | mesolimbic | AED + CPD + C0P | mesolimbic |

---

## Circuit Interconnection Diagram

```
                        +-----------+
                        |  AUDIO IN |
                        +-----+-----+
                              |
                    +---------+---------+
                    |                   |
                    v                   v
            [R3 Spectral 49D]   [H3 Temporal 2304D]
                    |                   |
          +---------+-------------------+---------+
          |         |         |         |         |
          v         v         v         v         v
    +-----------+ +-----+ +-------+ +-------+ +-------+
    | PERCEPTUAL| |SENSO| |MNEMONIC| |SALIENCE| |MESO- |
    |           | |MOTOR| |        | |        | |LIMBIC |
    |  PPC TPC  | |BEP  | |MEM SYN| | ASA    | |AED CPD|
    |           | |TMH  | |        | |        | |C0P    |
    +-----+-----+ +--+--+ +---+---+ +---+----+ +---+---+
          |           |        |         |          |
          v           v        v         v          v
        [SPU]     [STU,MPU] [IMU,PCU] [ASU,NDU] [ARU,RPU]
          |           |        |         |          |
          |     P5    |   P3   |         |          |
          +---------->+--->----+-------->+--------->|
          |  P1                                     |
          +---------------------------------------->|
                                                    |
                                              [ARU + RPU]
                                           Dependent Units
                                            (Phase 4)
                                                    |
                                                    v
                                          [Affect / Reward Output]
```

### Pathway Routing (Phase 2 -> Phase 4)

| Pathway | Route | Signal |
|---------|-------|--------|
| P1 | SPU --> ARU | Spectral features modulate affect |
| P2 | Internal STU | HMCE --> AMSC within sensorimotor |
| P3 | IMU --> ARU | Memory/familiarity modulates affect |
| P4 | Internal STU | Context hierarchy within sensorimotor |
| P5 | STU --> ARU | Temporal structure modulates affect |

Independent units (SPU, STU, IMU, ASU, NDU, MPU, PCU) compute in Phase 2 without cross-unit dependencies. Their outputs are routed via pathways to dependent units (ARU, RPU) in Phase 4.

---

## Temporal Coverage

Each circuit operates at characteristic timescales:

```
        5.8ms    23ms    200ms   350ms   525ms    1s     2s     5s    15s    60s
          |       |       |       |       |       |      |      |      |      |
PERCEPT:  H0------H3------H6                                                    PPC
                          H6--------------H12-----H16                            TPC
SENSORI:                  H6------H9------H11                                    BEP
                                                  H16----H18----H20----H22       TMH
MNEMONIC:                                 H12-----H16----H18                     SYN
                                                         H18----H20----H22--H25  MEM
SALIENCE:         H3------H6------H9                                             ASA
MESOLIMB:                 H6                      H16----H18                     AED
                                  H9              H16----H18                     CPD
                                                         H18----H19----H20       C0P
```

---

## Cross-References

- **Models**: [Models Index](../Models/00-INDEX.md)
- **Mechanisms**: [Mechanisms](../Mechanisms/)
- **Units**: [Units](../Units/)
- **Tiers**: [Alpha](../Tiers/Alpha.md) | [Beta](../Tiers/Beta.md) | [Gamma](../Tiers/Gamma.md)
