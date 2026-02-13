# H3 Standards -- Quality and Stability Index

> Version 2.0.0 | Updated 2026-02-13

## Overview

The Standards directory defines quality tiers for morph outputs and temporal resolution requirements for numerical stability. Together, these documents establish the expected accuracy and reliability of every H3 computation as a function of morph type, horizon band, and input characteristics.

**MorphQualityTiers** classifies each morph-band combination into Reliable, Marginal, or Unstable tiers based on expected numerical accuracy. **TemporalResolutionStandards** specifies the minimum window sizes (in frames) required for each morph to achieve each quality tier, along with numerical edge case documentation.

These standards feed directly into the [Validation/](../Validation/) acceptance criteria and are referenced during Phase 5 (code implementation) and Phase 6 (formula revision) to guide design decisions.

## File Listing

| File | Description |
|------|-------------|
| [00-INDEX.md](00-INDEX.md) | This file. Master index for the Standards directory. |
| [MorphQualityTiers.md](MorphQualityTiers.md) | Per-morph quality assessment framework. Tier definitions (Reliable/Marginal/Unstable), 24-morph x 4-band quality matrix, minimum window sizes, and MORPH_SCALE adequacy assessment. |
| [TemporalResolutionStandards.md](TemporalResolutionStandards.md) | Minimum window sizes and numerical stability requirements. Frame-to-duration conversion table, morph category minimums, horizon-morph compatibility matrix, and numerical edge case documentation. |

## Cross-References

| Related Document | Location |
|-----------------|----------|
| Morph catalog (formulas + scaling) | [../Registry/MorphCatalog.md](../Registry/MorphCatalog.md) |
| MORPH_SCALE calibration | [../Morphology/MorphScaling.md](../Morphology/MorphScaling.md) |
| Performance characteristics | [../Pipeline/Performance.md](../Pipeline/Performance.md) |
| Acceptance criteria | [../Validation/AcceptanceCriteria.md](../Validation/AcceptanceCriteria.md) |
| Benchmark plan | [../Validation/BenchmarkPlan.md](../Validation/BenchmarkPlan.md) |
| MorphComputer contract | [../Contracts/MorphComputer.md](../Contracts/MorphComputer.md) |
| H3 master index | [../00-INDEX.md](../00-INDEX.md) |
| MORPH_SCALE constants | `mi_beta/core/constants.py` |

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial standards index (Phase 4H) |
