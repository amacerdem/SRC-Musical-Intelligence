# R3 Validation Documentation

**Scope**: Experimental benchmarks, acceptance criteria, and quality gates for R3 v2 (128D).
**Phase**: 3C -- Documentation Layer
**Status**: Active

---

## Contents

| File | Description | Key Content |
|------|-------------|-------------|
| [BenchmarkPlan.md](BenchmarkPlan.md) | Experimental benchmark plan for 6 critical features | Datasets, baselines, metrics, success thresholds, fallback plans, timeline |
| [AcceptanceCriteria.md](AcceptanceCriteria.md) | Per-group quality gates for R3 v2 acceptance | Output shape, value range, NaN/Inf checks, performance budgets, regression tests |

---

## Relationship to Other Documentation

| Related Doc | Relationship |
|-------------|--------------|
| `R3-V2-DESIGN.md` Section 7 | Source: validation plan and 6 benchmark tests |
| `R3-CROSSREF.md` Section 7.2 | Source: features requiring experimental validation |
| `Standards/QualityTiers.md` | Quality tier assignments reference benchmark outcomes |
| `Standards/ComplianceMatrix.md` | Standard compliance claims depend on validation results |
| `Migration/V1-to-V2.md` | Migration proceeds only after acceptance criteria are met |

---

## Validation Strategy Overview

R3 v2 validation operates at three levels:

1. **Structural validation** (AcceptanceCriteria.md): Every group must produce correct output
   shapes, value ranges, and pass NaN/Inf checks. This is a hard gate -- no exceptions.

2. **Performance validation** (AcceptanceCriteria.md): Each group must compute within its
   per-frame time budget. The total pipeline must maintain real-time capability (< 5.8 ms/frame
   on GPU batch, per R3-V2-DESIGN.md Section 1.5).

3. **Quality validation** (BenchmarkPlan.md): Six features identified in R3-CROSSREF.md Section 7.2
   require correlation or accuracy benchmarks against established reference methods. These are
   the features where mel-domain approximation risk is highest.

---

## Benchmark Priority Matrix

| Priority | Feature | Group | Blocking? |
|:--------:|---------|:-----:|:---------:|
| Critical | mel-chroma [49:60] | F | Yes -- H, I groups depend on chroma quality |
| High | syncopation_index [68] | G | Partial -- groove and metricality depend on it |
| Medium | inharmonicity_index [64] | F | No -- independent feature |
| Medium | melodic_entropy [87] | I | No -- but IDyOM data prep required |
| Medium | harmonic_entropy [88] | I | No -- Billboard dataset required |
| Low | groove_index [71] | G | No -- behavioral data limited |

---

## Revision History

| Date | Change |
|------|--------|
| 2026-02-13 | Initial creation (Phase 3C) |
