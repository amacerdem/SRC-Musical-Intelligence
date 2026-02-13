# H3 Pipeline Documentation Index

> Version 2.0.0 | Updated 2026-02-13

## Purpose

This directory documents the H3 execution pipeline: how temporal demand flows from C3 model declarations through sparse computation to produce the features that feed the Brain. These documents cover the runtime architecture, not the mathematical design of horizons and morphs (see [H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) for design rationale).

## File Listing

| File | Description |
|------|-------------|
| [00-INDEX.md](00-INDEX.md) | This file. Master index for the Pipeline directory. |
| [ExecutionModel.md](ExecutionModel.md) | End-to-end execution flow from demand collection through result packing. ASCII pipeline diagram, pseudocode for each phase, tensor shapes, and complexity analysis. |
| [SparsityStrategy.md](SparsityStrategy.md) | Why and how H3 achieves sparse computation. Occupancy analysis, DemandTree structure, memory savings, and per-unit/per-tier sparsity breakdowns. |
| [Performance.md](Performance.md) | Performance characteristics and optimization strategies. Per-horizon cost model, cost-by-band table, GPU strategy, memory footprint estimates, and batching considerations. |
| [WarmUp.md](WarmUp.md) | Horizon-dependent warm-up behavior. Per-law warm-up patterns, warm-up durations by band, musical implications, and recommendations for C3 model consumers. |

## Cross-References

### Contracts Directory

The [Contracts/](../Contracts/) directory specifies the formal interfaces that the pipeline implements:

- Demand specification format (H3DemandSpec 4-tuples)
- H3Output structure and access patterns
- Per-mechanism horizon assignments

### Design Documents

- [H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) -- Design rationale for the 32-horizon, 24-morph, 3-law address space
- [H3-HORIZON-TABLE.md](../H3-HORIZON-TABLE.md) -- Complete horizon parameter table (frame counts, durations, bands)
- [H3-MORPH-CATALOG.md](../H3-MORPH-CATALOG.md) -- All 24 morph functions with mathematical definitions

### Code

- `mi_beta/ear/h3/` -- Implementation (5 files: `__init__.py`, `attention.py`, `demand.py`, `horizon.py`, `morph.py`)
