# H3 Migration -- Reference Index

> Version 2.0.0 | Updated 2026-02-13

## Overview

The Migration directory documents the transition path from H3 v1 (49 R3 features, groups A-E) to H3 v2 (128 R3 features, groups A-K). The migration is purely additive: the H3 engine code, horizon definitions, morph formulas, law kernels, and all existing DemandSpec tuples remain unchanged. The only changes occur at the C3 model level, where new 4-tuples referencing `r3_idx` values in [49:128] are appended to existing demand sets.

This directory provides the main migration guide (scope, steps, compatibility guarantees, risk assessment) and a detailed procedure for updating individual C3 model DemandSpec declarations with v2 tuples.

**Key numbers**:

| Metric | v1 | v2 | Change |
|--------|---:|---:|--------|
| R3 features | 49 | 128 | +79 (+161%) |
| Theoretical H3 space | 112,896 | 294,912 | +182,016 (+161%) |
| Actual H3 tuples | ~5,210 | ~8,610 | +3,400 (+65%) |
| H3 engine code changes | -- | -- | **None** |

## File Listing

| File | Description |
|------|-------------|
| [00-INDEX.md](00-INDEX.md) | This file. Master index for the Migration directory. |
| [V1-to-V2.md](V1-to-V2.md) | Main migration guide: what changes, what does not, step-by-step migration procedure, backward compatibility guarantee, risk assessment, and timeline. |
| [DemandSpec-Update.md](DemandSpec-Update.md) | Detailed procedure for updating C3 model DemandSpec tuples: 4-tuple format, per-group conventions, worked example, validation checklist, and adoption priority order. |

## Cross-References

| Related Document | Location |
|-----------------|----------|
| R3 v2 H3 impact analysis | [../Expansion/R3v2-H3-Impact.md](../Expansion/R3v2-H3-Impact.md) |
| Expansion group files (F-K) | [../Expansion/](../Expansion/) |
| Per-unit demand documentation | [../Demand/](../Demand/) |
| DemandAddressSpace registry | [../Registry/DemandAddressSpace.md](../Registry/DemandAddressSpace.md) |
| H3DemandSpec contract (C3) | [../../C3/Contracts/H3DemandSpec.md](../../C3/Contracts/H3DemandSpec.md) |
| R3 feature catalog | [../../R3/Registry/FeatureCatalog.md](../../R3/Registry/FeatureCatalog.md) |
| Acceptance criteria | [../Validation/AcceptanceCriteria.md](../Validation/AcceptanceCriteria.md) |
| Benchmark plan | [../Validation/BenchmarkPlan.md](../Validation/BenchmarkPlan.md) |
| H3 master index | [../00-INDEX.md](../00-INDEX.md) |

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial migration index (Phase 4H) |
