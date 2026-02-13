# H3 Validation -- Acceptance and Benchmarking Index

> Version 2.0.0 | Updated 2026-02-13

## Overview

The Validation directory defines acceptance criteria for H3 outputs and benchmark plans for performance and accuracy testing. These documents translate the quality standards defined in [Standards/](../Standards/) into concrete, testable requirements that will be executed during Phase 5 (code implementation) and Phase 6 (formula revision).

**AcceptanceCriteria** specifies pass/fail tests for every morph, law, horizon, and attention kernel property. **BenchmarkPlan** defines the performance and accuracy benchmarks, including synthetic test signals, golden reference computation, regression thresholds, and latency/memory targets.

## File Listing

| File | Description |
|------|-------------|
| [00-INDEX.md](00-INDEX.md) | This file. Master index for the Validation directory. |
| [AcceptanceCriteria.md](AcceptanceCriteria.md) | Per-morph/horizon acceptance criteria. Output range tests, per-morph synthetic input tests, law symmetry tests, horizon scaling tests, attention kernel verification, and performance thresholds. |
| [BenchmarkPlan.md](BenchmarkPlan.md) | Performance and accuracy benchmarks. Synthetic test corpus, golden reference generation, regression test suite, latency targets, and memory footprint validation. |

## Cross-References

| Related Document | Location |
|-----------------|----------|
| Quality tier framework | [../Standards/MorphQualityTiers.md](../Standards/MorphQualityTiers.md) |
| Temporal resolution standards | [../Standards/TemporalResolutionStandards.md](../Standards/TemporalResolutionStandards.md) |
| Performance characteristics | [../Pipeline/Performance.md](../Pipeline/Performance.md) |
| H3Extractor contract | [../Contracts/H3Extractor.md](../Contracts/H3Extractor.md) |
| MorphComputer contract | [../Contracts/MorphComputer.md](../Contracts/MorphComputer.md) |
| DemandTree contract | [../Contracts/DemandTree.md](../Contracts/DemandTree.md) |
| H3 master index | [../00-INDEX.md](../00-INDEX.md) |
| H3 code | `mi_beta/ear/h3/` |

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial validation index (Phase 4H) |
