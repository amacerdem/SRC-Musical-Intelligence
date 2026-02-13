# H3 Expansion Documentation Index

> Version 2.0.0 | Updated 2026-02-13

## Overview

The R3 v2 expansion adds 79 new spectral features in groups F through K (indices [49:128]), extending the R3 feature tensor from 49D to 128D. This expansion directly impacts H3 temporal demand because the first element of every H3 4-tuple is `r3_idx` -- the index into the R3 tensor that the temporal morph operates on.

The theoretical H3 address space grows from 112,896 (49 x 32 x 24 x 3) to 294,912 (128 x 32 x 24 x 3), a 2.61x increase. However, actual demand grows far more modestly: from ~5,210 v1 tuples to ~8,610 combined tuples (~65% growth). This asymmetry reflects the selective nature of C3 model demands -- new features are consumed only where they serve specific perceptual computations, not uniformly across all horizons, morphs, and laws.

Critically, the H3 engine itself requires no code changes. Horizons, morphs, and laws are feature-agnostic temporal operations. The only changes occur at the C3 model level, where `H3DemandSpec` tuples are extended to reference `r3_idx` values in [49:128].

## Per-Group Impact Summary

| Group | Features | Indices | Temporal Priority | Key H3 Horizons | Est. New Tuples | Primary Consumers |
|-------|:--------:|---------|:-----------------:|:---------------:|:---------------:|-------------------|
| F: Pitch & Chroma | 16D | [49:65] | HIGH | H3-H16 (Micro-Macro) | ~800-1200 | SPU, IMU, PCU |
| G: Rhythm & Groove | 10D | [65:75] | HIGH | H12-H22 (Meso-Macro) | ~400-600 | STU, MPU |
| H: Harmony & Tonality | 12D | [75:87] | HIGH | H12-H22 (Meso-Macro) | ~500-800 | NDU, PCU, IMU |
| I: Information & Surprise | 7D | [87:94] | MEDIUM-HIGH | H6-H22 (Meso-Macro) | ~300-500 | PCU, RPU, IMU |
| J: Timbre Extended | 20D | [94:114] | MEDIUM | H6-H18 (Meso) | ~400-700 | SPU, ASU |
| K: Modulation & Psycho | 14D | [114:128] | MEDIUM | H16-H25 (Macro) | ~200-400 | STU, ARU |
| **Total** | **79D** | **[49:128]** | | | **~3,400** | |

## File Listing

| File | Description |
|------|-------------|
| [R3v2-H3-Impact.md](R3v2-H3-Impact.md) | Master impact analysis: space expansion, per-unit demand, horizon shifts, code impact |
| [F-PitchChroma-Temporal.md](F-PitchChroma-Temporal.md) | Group F [49:65]: 16D pitch and chroma temporal demand analysis |
| [G-RhythmGroove-Temporal.md](G-RhythmGroove-Temporal.md) | Group G [65:75]: 10D rhythm and groove temporal demand analysis |
| [H-HarmonyTonality-Temporal.md](H-HarmonyTonality-Temporal.md) | Group H [75:87]: 12D harmony and tonality temporal demand analysis |
| [I-InformationSurprise-Temporal.md](I-InformationSurprise-Temporal.md) | Group I [87:94]: 7D information and surprise temporal demand analysis |
| [J-TimbreExtended-Temporal.md](J-TimbreExtended-Temporal.md) | Group J [94:114]: 20D extended timbre temporal demand analysis |
| [K-ModulationPsychoacoustic-Temporal.md](K-ModulationPsychoacoustic-Temporal.md) | Group K [114:128]: 14D modulation and psychoacoustic temporal demand analysis |

## Cross-References

- **H3 Architecture**: [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md)
- **H3 Master Index**: [../00-INDEX.md](../00-INDEX.md)
- **Demand Documentation**: [../Demand/00-INDEX.md](../Demand/00-INDEX.md)
- **R3 Feature Catalog**: [../../R3/Registry/FeatureCatalog.md](../../R3/Registry/FeatureCatalog.md)
- **R3 Mappings**: [../../R3/Mappings/](../../R3/Mappings/)
- **Registry / DemandAddressSpace**: [../Registry/DemandAddressSpace.md](../Registry/DemandAddressSpace.md)
- **Horizon Catalog**: [../Registry/HorizonCatalog.md](../Registry/HorizonCatalog.md)
- **Migration Guide**: [../Migration/V1-to-V2.md](../Migration/V1-to-V2.md)

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial expansion documentation index (Phase 4G) |
