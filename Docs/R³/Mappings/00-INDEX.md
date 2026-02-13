# R3 Feature Mapping Index

> **Scope**: 96 models across 9 cognitive units
> **R3 Version**: v2 (128D, groups A-K)
> **Sources**: R3-DEMAND-MATRIX.md, R3-CROSSREF.md, R3-Usage.md
> **Created**: 2026-02-13

---

## Overview

Each mapping file documents how a cognitive unit consumes the R3 spectral
feature vector, covering both the current v1 layout [0:49] and the new v2
expansion [49:128].

## Unit Consumption Heatmap

```
              A:Cons   B:Ener   C:Timb   D:Chan   E:Inter  F:Pitch  G:Rhythm H:Harm   I:Info   J:TimbX  K:ModPsy
              (0-6)    (7-11)   (12-20)  (21-24)  (25-48)  (49-64)  (65-74)  (75-86)  (87-93)  (94-113) (114-127)
            +--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
   SPU (9)  | XXXXX  |   x    |  XXXX  |   x    |   x    |  XXXX  |   .    |   x    |   .    |   xx   |   x    |
   STU (14) |   x    |  XXXX  |   x    |  XXXX  |   xx   |   x    |  XXXX  |   .    |   x    |   x    |   xx   |
   IMU (15) |  XXX   |  XXX   |  XXX   |  XXX   |  XXX   |   XX   |   XX   |   XX   |  XXX   |   xx   |   x    |
   ASU (9)  |   xx   |  XXXX  |  XXXX  |   xx   |   xx   |   XX   |   XX   |   .    |   .    |   xx   |   x    |
   NDU (9)  |   x    |   xx   |   xx   |  XXXX  |  XXXX  |   x    |   .    |  XXX   |  XXX   |   x    |   x    |
   MPU (10) |   x    |  XXXX  |   x    |  XXXX  |   xx   |   .    |  XXXX  |   .    |   .    |   x    |   xx   |
   PCU (10) |  XXXX  |   xx   |  XXX   |   xx   |  XXXX  |   XX   |   .    |  XXX   |  XXXX  |   xx   |   x    |
   ARU (10) |  XXXX  |  XXX   |  XXX   |  XXX   |  XXX   |   x    |   x    |   x    |   X    |   xx   |   x    |
   RPU (10) |  XXX   |  XXX   |  XXX   |  XXX   |  XXX   |   .    |   X    |   xx   |  XXXX  |   xx   |   x    |
            +--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+

Legend:  XXXXX = dominant (>80%)    XXXX = primary (60-80%)
        XXX = substantial (40-60%) XX = moderate (20-40%)
        X = low but direct         x = minor / indirect
        . = no demand
```

## New Group Demand Summary (v2, [49:128])

| New Group | Direct (X) | Indirect (x) | Total | Primary Units |
|-----------|:---:|:---:|:---:|---|
| F: Pitch & Chroma (16D) [49:65] | 16 | 11 | 27 | SPU (7), IMU (3), PCU (2), ASU (2) |
| G: Rhythm & Groove (10D) [65:75] | 25 | 8 | 33 | STU (10), MPU (9), IMU (3), ASU (3) |
| H: Harmony & Tonality (12D) [75:87] | 12 | 10 | 22 | NDU (4), PCU (3), IMU (2), RPU (4) |
| I: Information & Surprise (7D) [87:94] | 22 | 10 | 32 | RPU (6), PCU (5), IMU (3), NDU (3) |
| J: Timbre Extended (20D) [94:114] | ~20 | ~30 | ~50 | SPU, IMU, ARU (potential) |
| K: Modulation & Psychoacoustic (14D) [114:128] | ~10 | ~20 | ~30 | STU, MPU, ASU (potential) |

## Dependency Strength by Unit

| Unit | Models | R3 Dependency | Justification |
|------|:------:|:-------------:|---|
| SPU | 9 | **Critical** | Core spectral processing; A, C, F groups are primary input |
| STU | 14 | **Critical** | Temporal/motor timing; B, D, G groups drive all models |
| IMU | 15 | **Important** | Broad memory encoding; reads all groups but via higher-level integration |
| ASU | 9 | **Critical** | Salience detection directly from B, C spectral features |
| NDU | 9 | **Critical** | Deviation detection driven by D, E, H, I features |
| MPU | 10 | **Critical** | Motor planning from B, D, G features |
| PCU | 10 | **Critical** | Prediction error from A, E, H, I features |
| ARU | 10 | **Important** | Pathway-mediated; R3 access via P1/P3/P5 cross-unit routes |
| RPU | 10 | **Important** | Reward computation from A, B, E, I; pathway-mediated |

## File Listing

| File | Unit | Models | Primary v1 | Primary v2 |
|------|------|:------:|------------|------------|
| [SPU-R3-MAP.md](SPU-R3-MAP.md) | Spectral Processing | 9 | A, C | F, H |
| [STU-R3-MAP.md](STU-R3-MAP.md) | Sensorimotor Timing | 14 | B, D | G |
| [IMU-R3-MAP.md](IMU-R3-MAP.md) | Integrative Memory | 15 | All | F, G, H, I |
| [ASU-R3-MAP.md](ASU-R3-MAP.md) | Auditory Salience | 9 | B, C | F, G |
| [NDU-R3-MAP.md](NDU-R3-MAP.md) | Novelty Detection | 9 | D, E | H, I |
| [MPU-R3-MAP.md](MPU-R3-MAP.md) | Motor Planning | 10 | B, D | G |
| [PCU-R3-MAP.md](PCU-R3-MAP.md) | Predictive Coding | 10 | A, C, E | H, I |
| [ARU-R3-MAP.md](ARU-R3-MAP.md) | Affective Resonance | 10 | All (pathways) | I (minimal direct) |
| [RPU-R3-MAP.md](RPU-R3-MAP.md) | Reward Processing | 10 | A, B, E | I |

---

## Cross-References

- R3 feature definitions: `Docs/R3/upgrade_beta/R3-CROSSREF.md` Section 4
- Current usage matrix: `Docs/C3/Matrices/R3-Usage.md`
- Bottom-up demand analysis: `Docs/R3/upgrade_beta/R3-DEMAND-MATRIX.md`
- Literature survey: `Docs/R3/Literature/R3-LITERATURE.md`
