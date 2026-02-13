# STU H3 Demand Profile

> Version 2.0.0 | Updated 2026-02-13

## Unit Summary

| Property | Value |
|----------|-------|
| **Unit** | STU (Sensorimotor Timing Unit) |
| **Models** | 14 (alpha: 3, beta: 7, gamma: 4) |
| **Mechanisms** | BEP (13 models), TMH (4 models), TPC (1 model) |
| **Primary Band** | All bands (Micro through Macro, some Ultra) |
| **R3 Domains** | B (Energy), D (Change) |
| **Est. Tuples** | ~900 |
| **Primary Law** | L0 (Memory) -- causal beat tracking from past to present |

## Overview

The Sensorimotor Timing Unit is responsible for beat extraction, pulse tracking, tempo estimation, and rhythmic structure analysis. It is the second-highest consumer of H3 tuples after IMU, reflecting the temporal complexity of rhythm perception.

STU's demand is dominated by BEP (Beat Extraction and Pulse tracking), which operates at Micro-Meso horizons (H6, H9, H11) and is used by 13 of 14 models. Four models additionally engage TMH (Temporal Memory Hierarchy) for Macro-band processing (H16-H22), and one model (MPFS) uses TPC for Meso-Macro integration.

The primary law is L0 (Memory): beat tracking is inherently causal, accumulating evidence from past onsets to infer current pulse position.

## Per-Model Demand Table

| Model | Tier | Mechanisms | Horizons | Key R3 Features | Est. Tuples |
|-------|------|------------|----------|-----------------|:-----------:|
| HMCE  | alpha1 | BEP, TMH | H6, H9, H11, H16, H18, H20 | B (onset_strength, loudness), D (spectral_flux) | ~120 |
| AMSC  | alpha2 | BEP | H6, H9, H11 | B, D | ~60 |
| MDNS  | alpha3 | BEP | H6, H9, H11 | A, B | ~50 |
| AMSS  | beta1 | BEP | H6, H9, H11 | B, C | ~50 |
| TPIO  | beta2 | BEP | H6, H9, H11 | C | ~40 |
| EDTA  | beta3 | BEP, TMH | H6, H9, H11, H16, H18 | B, D | ~80 |
| ETAM  | beta4 | BEP | H6, H9, H11 | B, D | ~50 |
| HGSIC | beta5 | BEP | H6, H9, H11 | B, D, E | ~50 |
| OMS   | beta6 | BEP | H6, H9, H11 | B, D | ~50 |
| TMRM  | gamma1 | BEP, TMH | H6, H9, H11, H16, H18, H20, H22 | B, D | ~80 |
| NEWMD | gamma2 | BEP | H6, H9, H11 | B, D | ~40 |
| MTNE  | gamma3 | BEP | H6, H9, H11 | B | ~30 |
| PTGMP | gamma4 | BEP | H6, H9, H11 | B | ~30 |
| MPFS  | gamma5 | BEP, TPC | H6, H9, H11, H12, H16 | B, D | ~50 |

**Total**: ~900 estimated tuples across 14 models (after removing duplicates from shared horizons).

Note: STU has 14 models rather than the standard 9, reflecting the complexity of sensorimotor timing. The beta tier has 7 models and gamma has 5 (including MPFS).

## Horizon Coverage Heatmap

```
Horizon  H0   H3   H6   H9  H11  H12  H16  H18  H20  H22  H25
Band     |-- Micro --|   |--Meso--|   |---- Macro ----|  Ultra
         ============================================
HMCE      .    .   [X]  [X]  [X]   .   [X]  [X]  [X]   .    .
AMSC      .    .   [X]  [X]  [X]   .    .    .    .    .    .
MDNS      .    .   [X]  [X]  [X]   .    .    .    .    .    .
AMSS      .    .   [X]  [X]  [X]   .    .    .    .    .    .
TPIO      .    .   [X]  [X]  [X]   .    .    .    .    .    .
EDTA      .    .   [X]  [X]  [X]   .   [X]  [X]   .    .    .
ETAM      .    .   [X]  [X]  [X]   .    .    .    .    .    .
HGSIC     .    .   [X]  [X]  [X]   .    .    .    .    .    .
OMS       .    .   [X]  [X]  [X]   .    .    .    .    .    .
TMRM      .    .   [X]  [X]  [X]   .   [X]  [X]  [X]  [X]   .
NEWMD     .    .   [X]  [X]  [X]   .    .    .    .    .    .
MTNE      .    .   [X]  [X]  [X]   .    .    .    .    .    .
PTGMP     .    .   [X]  [X]  [X]   .    .    .    .    .    .
MPFS      .    .   [X]  [X]  [X]  [X]  [X]   .    .    .    .
         ============================================
Count     0    0   14   14   14    1    3    3    2    1    0
```

### Key Observations

- **H6, H9, H11** are universally demanded (14/14 models) -- the BEP core horizons spanning ~46ms to ~250ms, covering the beat-rate range.
- **H16-H22** are demanded only by TMH-equipped models (HMCE, EDTA, TMRM) for tempo memory and metric hierarchy.
- **H12** is demanded only by MPFS through TPC for metrical pattern completion.
- **No Micro-early demand** (H0, H3): STU does not process sub-beat spectral transients.
- **No Ultra demand**: STU does not track rhythmic patterns beyond ~25s.

## Morph Demand Profile

STU demands a broad range of morphs reflecting the diversity of temporal statistics needed for beat tracking:

| Morph | ID | Category | Usage |
|-------|----|----------|-------|
| Value | M0 | Level | Instantaneous onset/energy values |
| Mean | M1 | Level | Average energy level over horizon |
| Std | M2 | Dispersion | Energy variability (pulse regularity) |
| Velocity | M8 | Dynamics | Onset rate of change |
| Acceleration | M9 | Dynamics | Onset acceleration (tempo change) |
| Jerk | M10 | Dynamics | Onset jerk (rhythmic surprise) |
| Peak | M11 | Dynamics | Local energy maxima (beat candidates) |
| Trough | M12 | Dynamics | Local energy minima (inter-beat intervals) |
| Flux | M13 | Dynamics | Energy flux (onset density) |
| Periodicity | M14 | Rhythm | Autocorrelation-based periodicity |
| Trend | M18 | Dynamics | Long-term energy drift |
| Entrainment | M21 | Dynamics | Phase-locking measure (TMH models) |

### Morph-by-Mechanism Distribution

- **BEP (H6-H11)**: M0, M1, M2, M8, M9, M10, M11, M12, M13, M14 -- full dynamics suite for beat extraction.
- **TMH (H16-H22)**: M0, M1, M2, M14, M18, M21 -- periodicity and entrainment at metric timescales.
- **TPC (H12-H16)**: M0, M1, M14, M18 -- pattern completion with periodicity features.

## Law Assignment

| Law | Code | Models | Rationale |
|-----|------|--------|-----------|
| L0 (Memory) | Past-to-now | 12 models | Beat tracking accumulates past onset evidence |
| L1 (Prediction) | Now-to-future | 2 models (HMCE, TMRM) | Tempo prediction for anticipatory timing |

Most STU models operate under L0 (Memory), as beat perception is fundamentally about accumulating evidence from past events. The two models with both BEP and TMH (HMCE, TMRM) additionally use L1 (Prediction) for tempo anticipation at Macro horizons.

## R3 Feature Consumption

### v1 Features (Groups A-E)

| R3 Group | Features Used | Primary Consumers |
|----------|--------------|-------------------|
| B (Energy) | onset_strength, loudness, velocity_A, velocity_D, rms_energy | All 14 models |
| D (Change) | spectral_flux, onset_density, delta_loudness, delta_rms | 10 models (all except MDNS, MTNE, PTGMP, TPIO) |
| A (Consonance) | periodicity, fundamental_freq | MDNS |
| C (Timbre) | spectral_centroid, spectral_flatness | AMSS, TPIO |
| E (Interactions) | Energy-timbre cross terms | HGSIC |

### v2 Expansion (Groups F-K)

| R3 Group | Priority | Rationale |
|----------|----------|-----------|
| G (Rhythm) | **VERY HIGH** | syncopation, metricality, tempo, beat_strength, groove -- 10/14 models benefit directly. STU is the single largest G group consumer across all units. |
| K (Modulation) | MEDIUM | beat-rate modulation (1-4Hz) for ETAM, OMS, TMRM -- amplitude modulation rates overlap with beat frequencies |
| F (Pitch) | LOW | pitch not primary for timing, minor utility for melodic rhythm |
| I (Information) | LOW | information-theoretic features less relevant to timing |

**Estimated v2 tuple expansion**: ~600 additional tuples, dominated by G group features across all BEP horizons (H6, H9, H11). This makes STU the unit with the largest absolute v2 expansion.

### G:Rhythm Group Detail

The G:Rhythm group is mission-critical for STU. Projected per-feature demand:

| G Feature | Horizons | Models | Est. New Tuples |
|-----------|----------|:------:|:---------------:|
| syncopation | H6, H9, H11, H16 | 10 | ~100 |
| metricality | H9, H11, H16 | 8 | ~80 |
| tempo | H9, H11, H12, H16 | 14 | ~140 |
| beat_strength | H6, H9, H11 | 14 | ~140 |
| groove | H9, H11, H16, H18 | 6 | ~60 |

## Demand Characteristics

### Bandwidth Profile

STU has the broadest band coverage of any unit, with demand spanning Micro through Macro:

- **Core band** (H6-H11): 14/14 models, ~600 tuples -- beat-rate processing (46ms-250ms)
- **Macro band** (H16-H22): 4/14 models, ~250 tuples -- metric hierarchy and tempo memory
- **Meso bridge** (H12): 1/14 models, ~50 tuples -- metrical pattern completion

### Mechanism Overlap

Four models use dual mechanisms, creating horizon overlap at shared boundaries:

| Model | Mechanism 1 | Mechanism 2 | Shared Horizon |
|-------|-------------|-------------|:--------------:|
| HMCE  | BEP | TMH | (none -- distinct ranges) |
| EDTA  | BEP | TMH | (none -- distinct ranges) |
| TMRM  | BEP | TMH | (none -- distinct ranges) |
| MPFS  | BEP | TPC | (none -- distinct ranges) |

There is no horizon overlap between BEP and TMH/TPC in any model, which means each horizon's demand is unambiguously assigned to one mechanism.

### Scaling Notes

- STU demand scales primarily with BEP model count and G group feature additions.
- TMH demand is relatively fixed (4 models, stable horizon set).
- The beta tier is the largest (7 models), creating significant BEP demand at H6/H9/H11.

## Cross-References

- **Unit Models**: [../../C3/Models/STU-*/](../../C3/Models/)
- **BEP Mechanism**: [../Contracts/](../Contracts/)
- **TMH Mechanism**: [../Contracts/](../Contracts/)
- **TPC Mechanism**: [../Contracts/](../Contracts/)
- **R3 B Group**: [../../R3/](../../R3/)
- **R3 D Group**: [../../R3/](../../R3/)
- **Demand Index**: [00-INDEX.md](00-INDEX.md)
- **H3 Architecture**: [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md)
- **Horizon Bands**: [../Bands/](../Bands/)

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial STU demand profile |
