# H3 Temporal Architecture -- Changelog

All notable changes to the H3 documentation and architecture are recorded here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [2.0.0] -- 2026-02-13 (Phase 4)

### Added
- Modular documentation architecture (64 files, 12 directories)
- Registry: HorizonCatalog, MorphCatalog, LawCatalog, DemandAddressSpace
- Band documentation: Micro (H0-H7), Meso (H8-H15), Macro (H16-H23), Ultra (H24-H31)
- Morphology documentation: Distribution, Dynamics, Rhythm, Information, Symmetry, MorphScaling
- Laws documentation: L0 Memory, L1 Prediction, L2 Integration
- Contracts: H3Extractor, DemandTree, EventHorizon, MorphComputer, AttentionKernel
- Pipeline: ExecutionModel, SparsityStrategy, Performance, WarmUp
- Per-unit Demand docs (9 units: SPU, STU, IMU, ASU, NDU, MPU, PCU, ARU, RPU)
- Expansion: R3 v2 impact analysis + per-group temporal docs (F through K)
- Standards: MorphQualityTiers, TemporalResolutionStandards
- Validation: AcceptanceCriteria, BenchmarkPlan
- Literature: H3-LITERATURE.md
- Migration: V1-to-V2, DemandSpec-Update
- EXTENSION-GUIDE.md for developer onboarding

### Changed
- R3 feature range: [0:48] -> [0:127] (R3 v2 expansion)
- Theoretical space: 112,896 -> 294,912 (128 x 32 x 24 x 3)
- Estimated actual demand: ~5,200 -> ~8,600 tuples (~2.9% occupancy)
- Documentation structure: single monolithic file -> 64 modular files in 12 directories

### Removed
- Monolithic H3 documentation from Phase 1 (content migrated, not lost)

---

## [1.0.0] -- 2026-02-10 (Phase 1)

### Added
- 00-INDEX.md skeleton with H3 space overview
- 32 horizon definitions across 4 bands (Micro, Meso, Macro, Ultra)
- 24 morph definitions across 5 categories (Distribution, Dynamics, Rhythm, Information, Symmetry)
- 3 law definitions (Memory, Prediction, Integration)
- Three-axis space summary table
- Unit-level demand summary (9 units, 96 models)
- Cross-references to C3, R3, and code paths

### Notes
- Initial skeleton created during Phase 1 (C3 model revision)
- H3 space defined as 2304D (49 x 32 x 24 x 3) with sparse usage
- Based on 49 R3 v1 features; v2 expansion not yet incorporated
- Demand estimates derived from C3 model documentation review

---

## Version Summary

| Version | Date | R3 Features | Horizons | Morphs | Laws | Theoretical Space | Actual Tuples |
|---------|------|:-----------:|:--------:|:------:|:----:|:-----------------:|:-------------:|
| 1.0.0 | 2026-02-10 | 49 | 32 | 24 | 3 | 112,896 | ~5,200 |
| 2.0.0 | 2026-02-13 | 128 | 32 | 24 | 3 | 294,912 | ~8,600 |

---

## Roadmap

### [2.1.0] -- Phase 5 (planned)
- Populate all per-unit demand docs with exact tuple lists from code
- Reconcile R3 naming discrepancies (semantic vs. computational)
- Validate MORPH_SCALE calibration values against actual model training
- Fill in mechanism-to-horizon mappings from code audit

### [3.0.0] -- Phase 6+ (planned)
- Dynamic demand discovery from trained model weights
- Horizon pruning based on activation statistics
- Morph importance ranking per unit

---

**Code path**: `mi_beta/ear/h3/`
**Constants**: `mi_beta/core/constants.py`
**Parent index**: [00-INDEX.md](00-INDEX.md)
