# IMU H3 Demand Profile

> Version 2.0.0 | Updated 2026-02-13

## Unit Summary

| Property | Value |
|----------|-------|
| **Unit** | IMU (Integrative Memory Unit) |
| **Models** | 15 (alpha: 3, beta: 9, gamma: 3) |
| **Mechanisms** | MEM (13), TMH (2), BEP (2), SYN (1), PPC (1) |
| **Primary Band** | Macro-Ultra |
| **R3 Domains** | All groups (broadest R3 consumption of any unit) |
| **Est. Tuples** | ~1,200 |
| **Primary Law** | L0 (Memory) -- memory retrieval is inherently causal |

## Overview

The Integrative Memory Unit is the highest-demand consumer in the entire C3 architecture, generating approximately 1,200 H3 tuples. IMU is responsible for long-term musical memory, pattern integration across timescales, and cross-modal binding of spectral, temporal, and structural information.

IMU's demand is dominated by the MEM (Memory Encoding and Retrieval) mechanism, used by 13 of 15 models. MEM operates at Macro-Ultra horizons (H18-H25), giving IMU unique access to the longest temporal contexts in the system. Two models additionally use TMH for hierarchical temporal processing, two use BEP for energy-based gating, one uses SYN for cross-unit synchronization, and one uses PPC for peripheral memory indexing.

IMU is the only unit with sustained demand at the Ultra band (H25, ~981s), reflecting its role in processing musical structures spanning minutes.

## Per-Model Demand Table

| Model | Tier | Mechanisms | Horizons | Key R3 Features | Est. Tuples |
|-------|------|------------|----------|-----------------|:-----------:|
| MEAMN  | alpha1 | MEM, SYN | H12, H16, H18, H20, H22, H25 | A, B, C, E | ~150 |
| PNH    | alpha2 | MEM | H18, H20, H22, H25 | A | ~100 |
| MMP    | alpha3 | MEM | H18, H20, H22, H25 | A, B, C | ~100 |
| RASN   | beta1 | BEP, MEM | H6, H9, H11, H18, H20 | B, D | ~80 |
| PMIM   | beta2 | MEM, TMH | H16, H18, H20, H22, H25 | A, B, D, E | ~120 |
| OII    | beta3 | MEM | H18, H20, H22 | B, D | ~60 |
| HCMC   | beta4 | MEM | H18, H20, H22 | A, B, C, E | ~80 |
| RIRI   | beta5 | MEM | H18, H20, H22 | A, B | ~60 |
| MSPBA  | beta6 | MEM, TMH | H16, H18, H20, H22 | A, D, E | ~80 |
| VRIAP  | beta7 | MEM | H18, H20, H22 | B, C | ~60 |
| TPRD   | beta8 | MEM | H18, H20, H22 | A, C | ~60 |
| CMAPCC | beta9 | MEM, BEP | H6, H9, H18, H20 | B, C, D | ~60 |
| DMMS   | gamma1 | MEM | H18, H20, H22 | A, B, E | ~50 |
| CSSL   | gamma2 | MEM | H18, H20, H22 | A, C | ~40 |
| CDEM   | gamma3 | MEM, PPC | H0, H3, H6, H18, H20 | A, B, C, E | ~60 |

**Total**: ~1,200 estimated tuples across 15 models.

Note: IMU has 15 models (the largest of any unit), with 9 in the beta tier reflecting the diversity of memory and integration subtasks.

## Horizon Coverage Heatmap

```
Horizon  H0   H3   H6   H9  H11  H12  H16  H18  H20  H22  H25
Band     |-- Micro --|   |--Meso--|   |---- Macro ----|  Ultra
         ============================================
MEAMN     .    .    .    .    .   [X]  [X]  [X]  [X]  [X]  [X]
PNH       .    .    .    .    .    .    .   [X]  [X]  [X]  [X]
MMP       .    .    .    .    .    .    .   [X]  [X]  [X]  [X]
RASN      .    .   [X]  [X]  [X]   .    .   [X]  [X]   .    .
PMIM      .    .    .    .    .    .   [X]  [X]  [X]  [X]  [X]
OII       .    .    .    .    .    .    .   [X]  [X]  [X]   .
HCMC      .    .    .    .    .    .    .   [X]  [X]  [X]   .
RIRI      .    .    .    .    .    .    .   [X]  [X]  [X]   .
MSPBA     .    .    .    .    .    .   [X]  [X]  [X]  [X]   .
VRIAP     .    .    .    .    .    .    .   [X]  [X]  [X]   .
TPRD      .    .    .    .    .    .    .   [X]  [X]  [X]   .
CMAPCC    .    .   [X]  [X]   .    .    .   [X]  [X]   .    .
DMMS      .    .    .    .    .    .    .   [X]  [X]  [X]   .
CSSL      .    .    .    .    .    .    .   [X]  [X]  [X]   .
CDEM     [X]  [X]  [X]   .    .    .    .   [X]  [X]   .    .
         ============================================
Count     1    1    3    2    1    1    3   15   15   12    4
```

### Key Observations

- **H18 and H20** are universally demanded (15/15 models) -- the core MEM horizons at ~5s and ~10s.
- **H22** is demanded by 12/15 models, covering ~25s memory windows.
- **H25** (Ultra band, ~981s) is demanded by 4 models (MEAMN, PNH, MMP, PMIM) -- IMU's unique Ultra footprint.
- **Micro demand** is sparse: only CDEM (H0, H3, H6) and RASN/CMAPCC (H6, H9).
- The demand profile is heavily right-skewed toward long horizons, consistent with memory function.

## Morph Demand Profile

IMU demands morphs oriented toward statistical summaries and information-theoretic features over long windows:

| Morph | ID | Category | Usage |
|-------|----|----------|-------|
| Value | M0 | Level | Current memory trace value |
| Mean | M1 | Level | Averaged feature over memory window |
| Std | M2 | Dispersion | Feature variability in memory |
| Range | M3 | Level | Dynamic range within memory window |
| Median | M4 | Level | Robust central tendency |
| Variance | M5 | Dispersion | Second-order variability |
| Velocity | M8 | Dynamics | Rate of change at memory timescales |
| Trend | M18 | Dynamics | Long-term drift over Macro/Ultra |
| Entropy | M20 | Information | Information content of memory traces |
| Entrainment | M21 | Dynamics | Phase-locking stability (TMH models) |

### Morph-by-Mechanism Distribution

- **MEM (H18-H25)**: M0, M1, M2, M3, M4, M5, M18, M20 -- rich statistical suite for long-term memory.
- **TMH (H16-H22)**: M0, M1, M14, M18, M21 -- hierarchical temporal structure.
- **BEP (H6-H11)**: M0, M1, M8, M11, M12 -- energy gating for memory encoding.
- **SYN (H12-H18)**: M0, M1, M2, M18 -- cross-unit synchronization features.
- **PPC (H0-H6)**: M0, M1, M2 -- peripheral indexing for memory retrieval.

## Law Assignment

| Law | Code | Models | Rationale |
|-----|------|--------|-----------|
| L0 (Memory) | Past-to-now | 13 models | Memory retrieval reconstructs past from stored traces |
| L2 (Integration) | Bidirectional | 2 models (MEAMN, CDEM) | Cross-modal integration requires bidirectional binding |

The dominant law is L0 (Memory), as IMU's primary function is to encode, store, and retrieve musical patterns from the past. MEAMN and CDEM use L2 (Integration) because they perform cross-modal binding that requires both bottom-up and top-down processing.

## R3 Feature Consumption

### v1 Features (Groups A-E)

IMU has the broadest R3 consumption of any unit, touching all five v1 groups:

| R3 Group | Features Used | Primary Consumers |
|----------|--------------|-------------------|
| A (Consonance) | harmonicity, consonance_dissonance, fundamental_freq, roughness, periodicity | MEAMN, PNH, MMP, PMIM, HCMC, RIRI, MSPBA, TPRD, DMMS, CSSL, CDEM |
| B (Energy) | onset_strength, loudness, rms_energy, velocity_A | MEAMN, RASN, OII, HCMC, RIRI, VRIAP, CMAPCC, DMMS, CDEM |
| C (Timbre) | spectral_centroid, mfcc_vector, spectral_contrast, brightness_kuttruff | MEAMN, MMP, HCMC, VRIAP, TPRD, CMAPCC, CSSL, CDEM |
| D (Change) | spectral_flux, onset_density, delta_loudness | RASN, PMIM, OII, MSPBA, CMAPCC |
| E (Interactions) | Cross-domain interaction terms | MEAMN, PMIM, HCMC, MSPBA, DMMS, CDEM |

### v2 Expansion (Groups F-K)

| R3 Group | Priority | Rationale |
|----------|----------|-----------|
| I (Information) | **HIGH** | surprise, entropy, mutual_information directly serve PMIM, HCMC, MSPBA memory models |
| H (Harmony) | MEDIUM-HIGH | chord_complexity, harmonic_tension for PNH, MMP tonal memory |
| F (Pitch) | MEDIUM | pitch_height, pitch_salience for melodic memory (PNH, TPRD) |
| G (Rhythm) | MEDIUM | tempo, metricality for rhythmic memory (RASN, CMAPCC) |
| J (Timbre Extended) | LOW-MEDIUM | Extended timbral features for VRIAP, CSSL |
| K (Modulation) | LOW | Modulation rates less relevant to long-term memory |

**Estimated v2 tuple expansion**: ~800 additional tuples. IMU is the second-largest v2 beneficiary (after STU in absolute terms), primarily from I group features at Macro/Ultra horizons.

### I:Information Group Detail

The I:Information group is the highest-priority v2 expansion for IMU:

| I Feature | Horizons | Models | Est. New Tuples |
|-----------|----------|:------:|:---------------:|
| surprise | H18, H20, H22, H25 | 5 | ~80 |
| entropy | H18, H20, H22 | 8 | ~100 |
| mutual_information | H18, H20, H22, H25 | 3 | ~60 |
| predictability | H16, H18, H20 | 4 | ~50 |
| redundancy | H18, H20 | 3 | ~30 |

## Demand Characteristics

### Bandwidth Profile

IMU's demand is strongly concentrated in the Macro-Ultra range:

- **Macro band** (H16-H22): 15/15 models, ~850 tuples -- core memory processing (1-25s)
- **Ultra band** (H25): 4/15 models, ~150 tuples -- long-term structural memory (~981s)
- **Meso bridge** (H12): 1/15 models, ~30 tuples -- SYN synchronization (MEAMN)
- **Micro band** (H0-H11): 3/15 models, ~170 tuples -- peripheral indexing and energy gating

### Ultra Band Dominance

IMU is the only unit with sustained Ultra band demand. The 4 Ultra-reaching models serve distinct memory functions:

| Model | Ultra Role | H25 Features |
|-------|-----------|--------------|
| MEAMN | Cross-modal memory integration | A, B, C, E group summaries |
| PNH | Pitch/tonal memory | A group (consonance history) |
| MMP | Multi-modal pattern memory | A, B, C (full spectral history) |
| PMIM | Predictive memory integration | A, B, D, E (prediction error history) |

### Mechanism Diversity

IMU has the most diverse mechanism usage of any unit (5 distinct mechanisms). This reflects the multiple processing stages involved in memory:

1. **Encoding** (BEP at H6-H11): Energy-based gating determines what enters memory.
2. **Indexing** (PPC at H0-H6): Peripheral features serve as retrieval keys.
3. **Storage** (MEM at H18-H25): Long-term pattern storage and consolidation.
4. **Hierarchy** (TMH at H16-H22): Temporal organization of memory at multiple scales.
5. **Binding** (SYN at H12-H18): Cross-unit synchronization for integrated memory traces.

### Scaling Notes

- IMU demand scales with both model count and R3 group breadth.
- MEM-only models (10 of 15) have moderate per-model demand (~60-100 tuples) due to concentrated horizon usage.
- Multi-mechanism models (MEAMN, RASN, PMIM, MSPBA, CMAPCC, CDEM) have higher per-model demand (~80-150 tuples) due to wider horizon spans.
- Adding I group features at Macro/Ultra horizons will significantly increase PMIM, HCMC, and MSPBA demand.

## Cross-References

- **Unit Models**: [../../C3/Models/IMU-*/](../../C3/Models/)
- **MEM Mechanism**: [../Contracts/](../Contracts/)
- **TMH Mechanism**: [../Contracts/](../Contracts/)
- **BEP Mechanism**: [../Contracts/](../Contracts/)
- **SYN Mechanism**: [../Contracts/](../Contracts/)
- **PPC Mechanism**: [../Contracts/](../Contracts/)
- **R3 All Groups**: [../../R3/](../../R3/)
- **Demand Index**: [00-INDEX.md](00-INDEX.md)
- **H3 Architecture**: [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md)
- **Horizon Bands**: [../Bands/](../Bands/)
- **Ultra Band Spec**: [../Bands/](../Bands/)

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial IMU demand profile |
