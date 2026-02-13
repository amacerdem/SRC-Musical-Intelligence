# Meso Band Index

**Band**: Meso
**Horizons**: H8-H15
**Duration**: 300ms - 800ms
**Frames**: 52-138
**Neural correlate**: Beta-theta oscillations (4-30 Hz)
**Updated**: 2026-02-13

---

## Overview

The Meso band covers beat-period and phrase-level temporal horizons. This is the core timescale for musical rhythm perception, where beat entrainment, motor synchronization, and short-range temporal pattern recognition occur. All 24 morphs are reliable at meso timescales, making this the most statistically complete band.

The meso band corresponds to the neural beta-theta oscillation range (4-30 Hz), which drives sensorimotor synchronization and beat perception (Grahn & Brett 2007, Large & Palmer 2002).

---

## Quick Reference

| Horizon | Duration | Frames | Musical Scale | Mechanisms | Units |
|---------|----------|:------:|---------------|------------|-------|
| H8 | 300ms | 52 | Quarter @200BPM | -- | STU, MPU |
| H9 | 350ms | 60 | Quarter @171BPM | BEP, ASA, CPD | STU, MPU, ASU, NDU, ARU |
| H10 | 400ms | 69 | Quarter @150BPM | -- | STU, MPU |
| H11 | 450ms | 78 | Quarter @133BPM | BEP | STU, MPU |
| H12 | 525ms | 90 | Half @114BPM | TPC, SYN | SPU, STU |
| H13 | 600ms | 103 | Half @100BPM | -- | STU |
| H14 | 700ms | 121 | Half @86BPM | -- | STU |
| H15 | 800ms | 138 | Half @75BPM | -- | STU |

---

## Key Mechanisms

- **BEP** (Beat Entrainment Prediction): H6, H9, H11 -- core beat tracking domain
- **TPC** (Temporal Pattern Coding): H6, H12, H16 -- pattern recognition spanning micro-to-macro
- **SYN** (Syntactic Processing): Entry at H12 -- musical syntax begins at phrase level
- **ASA** (Auditory Scene Analysis): H3, H6, H9 -- stream segregation extending into beat timescale
- **CPD** (Change-Point Detection): H9, H16, H18 -- earliest structural boundary detection

---

## Primary Unit Consumers

| Unit | Mechanisms Used | Horizon Range | Typical Tuple Count |
|------|----------------|:-------------:|:-------------------:|
| STU | BEP, TPC | H6-H15 | ~350 |
| MPU | BEP | H6-H11 | ~250 |
| SPU | TPC | H6-H12 | ~150 |
| ASU | ASA | H6-H9 | ~120 |
| NDU | ASA | H6-H9 | ~120 |
| ARU | CPD | H9 | ~60 |

---

## Morph Applicability

All 24 morphs are valid at meso timescales (52-138 frames). Particularly relevant morphs:

- **M14** (periodicity): Directly measures rhythmic regularity within beat-period windows
- **M18** (trend): Detects accelerando/ritardando within phrase windows
- **M8** (velocity): Tracks dynamic changes at beat rate
- **M1** (mean): Stable average over beat-length windows

---

## Sub-Documents

| File | Horizons | Description |
|------|----------|-------------|
| [H8-H11-BeatPeriod.md](H8-H11-BeatPeriod.md) | H8-H11 | Beat period horizons |
| [H12-H15-Phrase.md](H12-H15-Phrase.md) | H12-H15 | Phrase-level horizons |

## Cross-References

| Document | Location |
|----------|----------|
| Band overview | [../00-INDEX.md](../00-INDEX.md) |
| Beat subdivision (H6-H7) | [../Micro/H6-H7-BeatSubdivision.md](../Micro/H6-H7-BeatSubdivision.md) |
| Measure (H16-H17) | [../Macro/H16-H17-Measure.md](../Macro/H16-H17-Measure.md) |
| Horizon catalog | [../../Registry/HorizonCatalog.md](../../Registry/HorizonCatalog.md) |
