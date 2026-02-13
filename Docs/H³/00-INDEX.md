# H3 Temporal Architecture -- Master Index

**Version**: 2.0.0
**Dimensions**: 294,912D theoretical (128 R3 features x 32 horizons x 24 morphs x 3 laws)
**Actual usage**: Sparse (~8,600 tuples = ~2.9% occupancy across 96 models)
**Status**: Phase 4 — modular architecture designed, population in progress
**Updated**: 2026-02-13

---

## Overview

H3 (Temporal Morphology Layer) transforms R3 spectral features into temporal morphological descriptors at multiple time horizons. Each H3 demand is a 4-tuple:

```
(r3_idx, horizon, morph, law)
```

**Pipeline position**: Audio --> Cochlea (128-mel) --> R3 (128D) --> **H3 (sparse)** --> Brain (C3 models)

**Input**: R3 feature tensor `(B, T, 128)` at 172.27 Hz frame rate
**Output**: Sparse dict `{(r3_idx, horizon, morph, law): tensor(B, T)}` with values in `[0, 1]`

**Design principle**: Demand-driven sparse computation. Each C3 model declares only the H3 tuples it needs (~12-150 per model). The H3 engine lazily computes only demanded tuples, keeping computation tractable despite the vast theoretical space.

---

## Three-Axis Space

### 32 Horizons (temporal scales)

| Band | Horizons | Duration | Frames | Musical Meaning | Primary Mechanisms |
|------|----------|----------|--------|-----------------|-------------------|
| **Micro** | H0-H7 | 5.8ms - 250ms | 1-43 | Onset, attack, transient, short note | PPC, ASA |
| **Meso** | H8-H15 | 300ms - 800ms | 52-138 | Beat period, quarter note, motif | BEP, TPC, SYN |
| **Macro** | H16-H23 | 1s - 25s | 172-4307 | Measure, section, passage | TMH, MEM, C0P, AED, CPD |
| **Ultra** | H24-H31 | 36s - 981s | 6202-169K | Movement, piece, full work | MEM (sparse) |

### 24 Morphs (statistical descriptors)

| Category | Morphs | Count | Description |
|----------|--------|:-----:|-------------|
| **Distribution** | M0-M7 | 8 | value, mean, std, median, max, range, skewness, kurtosis |
| **Dynamics** | M8-M13, M15, M18, M21 | 9 | velocity, acceleration, smoothness, trend, zero_crossings |
| **Rhythm** | M14, M17, M22 | 3 | periodicity, shape_period, peaks |
| **Information** | M20 | 1 | Shannon entropy |
| **Symmetry** | M16, M19, M23 | 3 | curvature, stability, symmetry |

### 3 Laws (temporal perspective)

| Law | Name | Direction | Kernel | Primary Users |
|-----|------|-----------|--------|---------------|
| L0 | Memory | Past --> Now | Causal exp decay | IMU, STU, MPU |
| L1 | Prediction | Now --> Future | Anticipatory forward | NDU, MPU, PCU |
| L2 | Integration | Past <--> Future | Bidirectional symmetric | SPU, ASU, ARU |

---

## Architecture Summary

| Aspect | Value |
|--------|-------|
| R3 feature count | 128 (49 v1 + 79 v2) |
| Horizon count | 32 (H0-H31, 4 bands) |
| Morph count | 24 (M0-M23, 5 categories) |
| Law count | 3 (L0-L2) |
| Theoretical space | 128 x 32 x 24 x 3 = 294,912 |
| Estimated actual tuples | ~8,600 (~2.9% occupancy) |
| Attention kernel | A(dt) = exp(-3\|dt\|/H) |
| Frame rate | 172.27 Hz (5.8 ms/frame) |
| Code path | `mi_beta/ear/h3/` |
| Constants | `mi_beta/core/constants.py` (HORIZON_MS, MORPH_NAMES, LAW_NAMES) |

---

## Directory Structure

```
Docs/H3/
|-- 00-INDEX.md                              <-- You are here
|-- H3-TEMPORAL-ARCHITECTURE.md              Definitive architecture document
|-- CHANGELOG.md                             Version history
|-- EXTENSION-GUIDE.md                       Developer extension guide
|
|-- Registry/                                Canonical reference tables
|   |-- 00-INDEX.md
|   |-- HorizonCatalog.md                    All 32 horizons with full metadata
|   |-- MorphCatalog.md                      All 24 morphs with formulas + MORPH_SCALE
|   |-- LawCatalog.md                        All 3 laws with kernel formulas
|   |-- DemandAddressSpace.md                4-tuple address system + sparsity analysis
|
|-- Bands/                                   Primary axis: temporal bands
|   |-- 00-INDEX.md                          Cross-band comparison
|   |-- Micro/                               H0-H7: Sensory (~6ms-250ms)
|   |   |-- 00-INDEX.md
|   |   |-- H0-H5-SubBeat.md
|   |   |-- H6-H7-BeatSubdivision.md
|   |-- Meso/                                H8-H15: Beat/phrase (~300ms-800ms)
|   |   |-- 00-INDEX.md
|   |   |-- H8-H11-BeatPeriod.md
|   |   |-- H12-H15-Phrase.md
|   |-- Macro/                               H16-H23: Section (~1s-25s)
|   |   |-- 00-INDEX.md
|   |   |-- H16-H17-Measure.md
|   |   |-- H18-H23-Section.md
|   |-- Ultra/                               H24-H31: Movement/piece (~36s-981s)
|       |-- 00-INDEX.md
|       |-- H24-H28-Movement.md
|       |-- H29-H31-Piece.md
|
|-- Morphology/                              Cross-cutting morph documentation
|   |-- 00-INDEX.md
|   |-- Distribution.md                      M0-M7
|   |-- Dynamics.md                          M8-M13, M15, M18, M21
|   |-- Rhythm.md                            M14, M17, M22
|   |-- Information.md                       M20
|   |-- Symmetry.md                          M16, M19, M23
|   |-- MorphScaling.md                      MORPH_SCALE calibration
|
|-- Laws/                                    Cross-cutting law documentation
|   |-- 00-INDEX.md
|   |-- L0-Memory.md
|   |-- L1-Prediction.md
|   |-- L2-Integration.md
|
|-- Contracts/                               Interface specifications
|   |-- 00-INDEX.md
|   |-- H3Extractor.md
|   |-- DemandTree.md
|   |-- EventHorizon.md
|   |-- MorphComputer.md
|   |-- AttentionKernel.md
|
|-- Pipeline/                                Execution architecture
|   |-- 00-INDEX.md
|   |-- ExecutionModel.md
|   |-- SparsityStrategy.md
|   |-- Performance.md
|   |-- WarmUp.md
|
|-- Demand/                                  Per-unit H3 demand
|   |-- 00-INDEX.md
|   |-- SPU-H3-DEMAND.md
|   |-- STU-H3-DEMAND.md
|   |-- IMU-H3-DEMAND.md
|   |-- ASU-H3-DEMAND.md
|   |-- NDU-H3-DEMAND.md
|   |-- MPU-H3-DEMAND.md
|   |-- PCU-H3-DEMAND.md
|   |-- ARU-H3-DEMAND.md
|   |-- RPU-H3-DEMAND.md
|
|-- Expansion/                               R3 v2 impact on H3
|   |-- 00-INDEX.md
|   |-- R3v2-H3-Impact.md
|   |-- F-PitchChroma-Temporal.md
|   |-- G-RhythmGroove-Temporal.md
|   |-- H-HarmonyTonality-Temporal.md
|   |-- I-InformationSurprise-Temporal.md
|   |-- J-TimbreExtended-Temporal.md
|   |-- K-ModulationPsychoacoustic-Temporal.md
|
|-- Standards/
|   |-- 00-INDEX.md
|   |-- MorphQualityTiers.md
|   |-- TemporalResolutionStandards.md
|
|-- Validation/
|   |-- 00-INDEX.md
|   |-- AcceptanceCriteria.md
|   |-- BenchmarkPlan.md
|
|-- Literature/
|   |-- 00-INDEX.md
|   |-- H3-LITERATURE.md
|
|-- Migration/
    |-- 00-INDEX.md
    |-- V1-to-V2.md
    |-- DemandSpec-Update.md
```

---

## Unit-Level Demand Summary

| Unit | Models | Mechanisms | Primary Band | Est. Tuples | Largest Consumer |
|------|:------:|-----------|:------------:|:-----------:|:----------------:|
| SPU | 9 | PPC, TPC | Micro-Macro | ~450 | TPC at H6-H16 |
| STU | 14 | BEP, TMH, TPC | All bands | ~900 | TMH at H16-H22 |
| IMU | 15 | MEM, TMH, BEP, SYN, PPC | Macro-Ultra | ~1,200 | MEM at H18-H25 |
| ASU | 9 | ASA | Micro-Meso | ~360 | ASA at H3-H9 |
| NDU | 9 | ASA, PPC, TMH, MEM | All bands | ~400 | ASA at H3-H6 |
| MPU | 10 | BEP | Micro-Meso | ~500 | BEP at H6-H11 |
| PCU | 10 | PPC, TPC, MEM, AED, C0P, ASA | All bands | ~500 | C0P at H18-H20 |
| ARU | 10 | AED, CPD, C0P, ASA, MEM | Micro-Macro | ~500 | AED at H6+H16 |
| RPU | 10 | AED, CPD, C0P, TMH, MEM, BEP, ASA | All bands | ~400 | CPD at H9+H16 |
| **Total** | **96** | **10** | | **~5,210** | |

**With R3 v2 expansion**: ~5,210 (v1) + ~3,400 (v2) = **~8,610 total estimated tuples**

---

## Key Documents

| Document | Purpose |
|----------|---------|
| [H3-TEMPORAL-ARCHITECTURE.md](H3-TEMPORAL-ARCHITECTURE.md) | Definitive architecture, design rationale, theory |
| [Registry/HorizonCatalog.md](Registry/HorizonCatalog.md) | All 32 horizons with complete metadata |
| [Registry/MorphCatalog.md](Registry/MorphCatalog.md) | All 24 morphs with formulas and scaling |
| [Expansion/R3v2-H3-Impact.md](Expansion/R3v2-H3-Impact.md) | R3 v2 expansion impact analysis |

## Cross-References

| Related Document | Location |
|-----------------|----------|
| H3DemandSpec contract | [C3/Contracts/H3DemandSpec.md](../C3/Contracts/H3DemandSpec.md) |
| H3 demand matrix | [C3/Matrices/H3-Demand.md](../C3/Matrices/H3-Demand.md) |
| R3 feature catalog | [R3/Registry/FeatureCatalog.md](../R3/Registry/FeatureCatalog.md) |
| Mechanism index | [C3/Mechanisms/00-INDEX.md](../C3/Mechanisms/00-INDEX.md) |
| H3 code | `mi_beta/ear/h3/` (5 files) |
| H3 constants | `mi_beta/core/constants.py` |
