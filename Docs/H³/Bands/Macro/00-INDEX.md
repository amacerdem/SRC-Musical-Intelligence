# Macro Band Index

**Band**: Macro
**Horizons**: H16-H23
**Duration**: 1,000ms - 25,000ms
**Frames**: 172-4,307
**Neural correlate**: Delta-theta oscillations (1-4 Hz)
**Updated**: 2026-02-13

---

## Overview

The Macro band is the most functionally important band for higher musical cognition. It covers measure-level through section-level timescales (1-25 seconds), where musical form, harmonic progressions, memory encoding, and predictive coding operate. This band contains the highest mechanism density by count (7 distinct mechanisms) and the largest number of estimated H3 tuples (~49% of total).

The macro band corresponds to the delta-theta oscillation range (1-4 Hz), associated with auditory cortex temporal receptive fields (Norman-Haignere 2022) and memory encoding (Golesorkhi 2021).

---

## Quick Reference

| Horizon | Duration | Frames | Musical Scale | Mechanisms | Units |
|---------|----------|:------:|---------------|------------|-------|
| H16 | 1,000ms | 172 | Measure @240BPM (4/4) | TMH, TPC, SYN, AED, CPD | ARU, STU, SPU, NDU, RPU |
| H17 | 1,500ms | 259 | Measure @160BPM | -- | IMU, STU |
| H18 | 2,000ms | 345 | Measure @120BPM | MEM, SYN, CPD, C0P | IMU, ARU, PCU, STU |
| H19 | 3,000ms | 517 | 2 measures @160BPM | C0P | PCU |
| H20 | 5,000ms | 861 | 4 measures @120BPM | TMH, MEM, C0P | IMU, PCU |
| H21 | 8,000ms | 1,378 | 8 bars @120BPM | -- | IMU |
| H22 | 15,000ms | 2,584 | Section (~16 bars) | TMH, MEM | IMU |
| H23 | 25,000ms | 4,307 | Extended section | -- | IMU |

---

## Key Mechanisms

- **TMH** (Temporal Memory Hierarchy): H16, H18, H20, H22 -- hierarchical temporal memory at section scales
- **MEM** (Memory Encoding/Retrieval): H18, H20, H22, H25 -- long-term memory formation spanning into ultra
- **C0P** (Comparative Processing): H18, H19, H20 -- section-level comparison and evaluation
- **SYN** (Syntactic Processing): H12, H16, H18 -- musical syntax at measure-to-section scale
- **AED** (Auditory Event Detection): H6, H16 -- macro-scale event detection (section boundaries)
- **CPD** (Change-Point Detection): H9, H16, H18 -- structural boundary detection
- **TPC** (Temporal Pattern Coding): H6, H12, H16 -- longest temporal pattern recognition

---

## Primary Unit Consumers

| Unit | Mechanisms Used | Horizon Range | Typical Tuple Count |
|------|----------------|:-------------:|:-------------------:|
| IMU | MEM, TMH | H18-H23 | ~1,200 |
| ARU | AED, CPD | H6+H16, H9+H16+H18 | ~500 |
| PCU | C0P | H18-H20 | ~300 |
| STU | TMH, SYN | H16-H18 | ~350 |
| NDU | TMH | H16 | ~100 |
| RPU | CPD, TMH | H16-H18 | ~200 |

---

## Morph Applicability

At macro timescales (172-4,307 frames), statistical summary morphs dominate:

- **Preferred**: M1 (mean), M2 (std), M18 (trend), M19 (stability), M20 (entropy)
- **Valid but less informative**: M8 (velocity), M9 (acceleration) -- instantaneous dynamics are less meaningful at section scale
- **Fully valid**: All 24 morphs compute without issues, but higher-order morphs may be noisy at H22-H23

---

## Sub-Documents

| File | Horizons | Description |
|------|----------|-------------|
| [H16-H17-Measure.md](H16-H17-Measure.md) | H16-H17 | Measure-level horizons |
| [H18-H23-Section.md](H18-H23-Section.md) | H18-H23 | Section-level horizons |

## Cross-References

| Document | Location |
|----------|----------|
| Band overview | [../00-INDEX.md](../00-INDEX.md) |
| Phrase (H12-H15) | [../Meso/H12-H15-Phrase.md](../Meso/H12-H15-Phrase.md) |
| Movement (H24-H28) | [../Ultra/H24-H28-Movement.md](../Ultra/H24-H28-Movement.md) |
| Horizon catalog | [../../Registry/HorizonCatalog.md](../../Registry/HorizonCatalog.md) |
