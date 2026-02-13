# H3 Demand Documentation Index

> Version 2.0.0 | Updated 2026-02-13

## Overview

Each C3 unit places temporal demand on the H3 horizon system through its constituent models and mechanisms. This documentation suite captures those demands per unit, organized by model tier, mechanism assignment, horizon coverage, and R3 feature consumption.

The H3 demand tuple format is `(r3_idx, horizon, morph, law)`, drawn from a theoretical space of 2,304 combinations. In practice, the ~5,210 tuples documented here represent the active subset consumed by the 96 models across all 9 units.

## Grand Total Summary

| Unit | Models | Mechanisms | Primary Band | Est. Tuples | Largest Consumer |
|------|:------:|------------|:------------:|:-----------:|:----------------:|
| SPU  |   9    | PPC, TPC   | Micro-Macro  |    ~450     | TPC at H6-H16    |
| STU  |  14    | BEP, TMH, TPC | All bands |    ~900     | TMH at H16-H22   |
| IMU  |  15    | MEM, TMH, BEP, SYN, PPC | Macro-Ultra | ~1,200 | MEM at H18-H25 |
| ASU  |   9    | ASA        | Micro-Meso   |    ~360     | ASA at H3-H9     |
| NDU  |   9    | ASA, PPC, TMH, MEM | All bands |  ~400     | ASA at H3-H6     |
| MPU  |  10    | BEP        | Micro-Meso   |    ~500     | BEP at H6-H11    |
| PCU  |  10    | PPC, TPC, MEM, AED, C0P, ASA | All bands | ~500 | C0P at H18-H20 |
| ARU  |  10    | AED, CPD, C0P, ASA, MEM | Micro-Macro | ~500 | AED at H6+H16 |
| RPU  |  10    | AED, CPD, C0P, TMH, MEM, BEP, ASA | All bands | ~400 | CPD at H9+H16 |
| **Total** | **96** | **10** | | **~5,210** | |

### R3 v2 Expansion Projection

With the R3 v2 feature set (groups F through K), per-unit demand expands significantly:

- **v1 demand**: ~5,210 tuples (groups A-E, 49 features)
- **v2 additional**: ~3,400 tuples (groups F-K, projected features)
- **Combined total**: ~8,610 tuples

The largest v2 beneficiaries are STU (G:Rhythm group) and IMU (I:Information group).

## Per-Unit Documentation

| File | Unit | Description |
|------|------|-------------|
| [SPU-H3-DEMAND.md](SPU-H3-DEMAND.md) | SPU | Spectral Processing Unit -- PPC/TPC across Micro-Macro |
| [STU-H3-DEMAND.md](STU-H3-DEMAND.md) | STU | Sensorimotor Timing Unit -- BEP/TMH/TPC across all bands |
| [IMU-H3-DEMAND.md](IMU-H3-DEMAND.md) | IMU | Integrative Memory Unit -- MEM-dominant, Macro-Ultra |
| [ASU-H3-DEMAND.md](ASU-H3-DEMAND.md) | ASU | Auditory Salience Unit -- ASA-only, Micro-Meso |
| [NDU-H3-DEMAND.md](NDU-H3-DEMAND.md) | NDU | Novelty Detection Unit -- ASA-dominant with PPC/TMH/MEM outliers, all bands |
| [MPU-H3-DEMAND.md](MPU-H3-DEMAND.md) | MPU | Motor Planning Unit -- BEP-only, Micro-Meso |
| [PCU-H3-DEMAND.md](PCU-H3-DEMAND.md) | PCU | Predictive Coding Unit -- 6 mechanisms, most diverse, all bands |
| [ARU-H3-DEMAND.md](ARU-H3-DEMAND.md) | ARU | Affective Resonance Unit -- AED-dominant, pathway-dependent, Micro-Macro |
| [RPU-H3-DEMAND.md](RPU-H3-DEMAND.md) | RPU | Reward Processing Unit -- 7 mechanisms, most diverse set, all bands |

## Cross-References

- **H3 Architecture**: [H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md)
- **Horizon Bands**: [Bands/](../Bands/)
- **Morph Definitions**: [Morphology/](../Morphology/)
- **Law Specifications**: [Laws/](../Laws/)
- **H3 Demand Matrix**: [Contracts/](../Contracts/)
- **R3 Mappings**: [../../R3/](../../R3/)
- **C3 Model Docs**: [../../C3/Models/](../../C3/Models/)

## Mechanism-to-Horizon Reference

For quick lookup, each mechanism's horizon assignments:

| Mechanism | Horizons | Band Range |
|-----------|----------|------------|
| PPC | H0, H3, H6 | Micro |
| TPC | H6, H12, H16 | Micro-Macro |
| BEP | H6, H9, H11 | Micro-Meso |
| ASA | H3, H6, H9 | Micro-Meso |
| TMH | H16, H18, H20, H22 | Macro |
| MEM | H18, H20, H22, H25 | Macro-Ultra |
| SYN | H12, H16, H18 | Meso-Macro |
| AED | H6, H16 | Micro+Macro |
| CPD | H9, H16, H18 | Meso-Macro |
| C0P | H18, H19, H20 | Macro |

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial per-unit demand documentation suite |
