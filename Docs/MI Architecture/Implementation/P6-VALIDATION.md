# Phase 6: Validation — Lossless Traceability Verification

**Phase**: P6
**Depends on**: P1-P5 (all implementation complete)
**Output**: 6 Python files in `Musical_Intelligence/validation/`
**Gate**: G6 — Traceability matrix covers 100% of Type 1-4 doc information

---

## Overview

This phase ensures that ZERO information was lost during the documentation-to-code conversion.
Three layers of verification:

```
Layer 1: STRUCTURAL — Do all expected files, classes, methods exist?
Layer 2: VALUE      — Do all constants, indices, coefficients match docs?
Layer 3: SEMANTIC   — Are citations, brain regions, falsification criteria preserved?
```

---

## Validation Architecture

### `validation/__init__.py`

**Purpose**: Package init, re-exports all validation functions.

---

### `validation/structural_check.py`

**Purpose**: Verify that every expected code artifact exists.

**Primary Docs**:
- `Docs/MI Architecture/MI-Doc/MI-DOC-ARCHITECTURE.md` — 395-file inventory
- `Docs/C³/Models/00-INDEX.md` — 96 model roster
- `Docs/C³/Mechanisms/00-INDEX.md` — 10 mechanism roster
- `Docs/C³/Units/00-INDEX.md` — 9 unit roster

**Related Docs**:
- `Docs/R³/Registry/DimensionMap.md` — 11 groups
- `Docs/H³/Registry/HorizonCatalog.md` — 32 horizons
- `Docs/L³/Groups/00-INDEX.md` — 8 semantic groups

**Depends On**: All P1-P5 code.

**Exports**: `run_structural_check() → StructuralReport`

**Key Constraints**:
- Must verify existence of:
  - 14 contract files (8 dataclasses + 5 ABCs + 1 init)
  - 11 R³ spectral groups (each with group.py)
  - 24 H³ morph functions (across 5 category files)
  - 32 H³ horizon entries in constants
  - 3 H³ law implementations
  - 10 mechanism classes
  - 9 unit classes
  - 96 model classes
  - 5 pathway definitions
  - 6 circuit definitions
  - 26 brain region entries
  - 4 neurochemical definitions
  - 8 semantic groups
  - 9 unit adapters
  - 96 vocabulary terms
- Report: list of missing items, list of extra items, coverage percentage

**Verification Checklist**:
- [ ] Detects all 96 model classes
- [ ] Detects all 10 mechanism classes
- [ ] Reports 100% structural coverage
- [ ] Identifies any unexpected extra files

---

### `validation/value_check.py`

**Purpose**: Verify that constants and values in code match documentation.

**Primary Docs**:
- `Docs/R³/Registry/FeatureCatalog.md` — 128 feature names and indices
- `Docs/R³/Registry/DimensionMap.md` — group boundaries
- `Docs/H³/Registry/HorizonCatalog.md` — HORIZON_MS values
- `Docs/H³/Registry/MorphCatalog.md` — MORPH_NAMES, formulas
- `Docs/H³/Registry/LawCatalog.md` — law definitions
- All 96 model docs (Sections 4, 5, 6)

**Related Docs**:
- `Docs/Beta/DISCREPANCY-REGISTRY.md` — known discrepancies to account for

**Depends On**: All P1-P5 code, ability to import and inspect model classes.

**Exports**: `run_value_check() → ValueReport`

**Key Constraints**:
- For each R³ group: verify GROUP_NAME, OUTPUT_DIM, INDEX_RANGE, feature_names
- For H³: verify HORIZON_MS[32], MORPH_NAMES[24], LAW_NAMES[3]
- For each model (96 total):
  - `NAME` matches doc header
  - `FULL_NAME` matches doc Section 1 title
  - `UNIT` matches unit code
  - `TIER` matches doc tier
  - `OUTPUT_DIM` matches doc Section 6 total
  - `len(LAYERS)` matches doc E/M/P/F count
  - `sum(layer.dim for layer in LAYERS) == OUTPUT_DIM`
  - `len(dimension_names) == OUTPUT_DIM`
  - `len(h3_demand)` matches doc Section 5 tuple count
  - `MECHANISM_NAMES` matches doc mechanism list
- Report: per-model pass/fail, per-field mismatch details

**Verification Checklist**:
- [ ] Checks all 96 models
- [ ] Checks all R³ group boundaries
- [ ] Checks all H³ constants
- [ ] Reports exact mismatch details (expected vs actual)
- [ ] Accounts for known discrepancies from DISCREPANCY-REGISTRY

---

### `validation/cross_reference.py`

**Purpose**: Verify cross-layer integrity (R³↔H³↔C³↔L³ references are consistent).

**Primary Docs**:
- `Docs/C³/Matrices/R3-Usage.md` — which models use which R³ features
- `Docs/C³/Matrices/H3-Demand.md` — aggregated H³ demands per unit
- `Docs/C³/Matrices/Mechanism-Map.md` — mechanism-model assignments
- `Docs/MI Architecture/MI-Doc/MI-DOC-ARCHITECTURE.md` §6 — cross-layer references

**Related Docs**:
- `Docs/R³/Mappings/` — per-unit R³ usage maps
- `Docs/H³/Demand/` — per-unit H³ demand tables

**Depends On**: All P1-P5 code.

**Exports**: `run_cross_reference_check() → CrossRefReport`

**Key Constraints**:
- For each model's R3_INDICES: verify indices exist in R³ feature catalog (0-127)
- For each model's h3_demand tuples:
  - r3_idx exists in model's R3_INDICES (or is otherwise valid)
  - horizon in [0, 31]
  - morph in [0, 23]
  - law in [0, 2]
- For each model's MECHANISM_NAMES: verify mechanism class exists
- For each model's CROSS_UNIT_READS: verify target unit/model exists
- For each pathway: verify source and target models exist
- For L³ adapters: verify unit exists and output dimensions align
- Verify unit dependency graph is acyclic

**Verification Checklist**:
- [ ] All R3 indices valid (0-127)
- [ ] All H3 demand tuples valid
- [ ] All mechanism references resolve
- [ ] All cross-unit pathway references resolve
- [ ] Dependency graph is a DAG (no cycles)

---

### `validation/traceability.py`

**Purpose**: Generate the doc-to-code traceability matrix.

**Primary Docs**:
- `Docs/MI Architecture/Implementation/MASTER-PLAN.md` §4 — information taxonomy
- All 395 documentation files

**Depends On**: All P1-P5 code, `structural_check.py`, `value_check.py`, `cross_reference.py`.

**Exports**: `generate_traceability_matrix() → TraceabilityMatrix`

**Key Constraints**:
- For each doc file, identify what information it contains (Type 1-6 classification)
- For Type 1-4 information: map to exact code location (file:class:attribute or file:function)
- For Type 5: verify docstring exists
- For Type 6: mark as "docs-only" (no code required)
- Output: structured matrix with columns:
  - Doc file path
  - Information type (1-6)
  - Information item (e.g., "BCH.OUTPUT_DIM = 12")
  - Code location (e.g., "brain/units/spu/models/bch.py:BCH.OUTPUT_DIM")
  - Status: MAPPED / MISSING / DOCS_ONLY
- Coverage metric: `mapped_count / (mapped_count + missing_count) * 100`
- Target: 100% coverage for Type 1-4 information

**Verification Checklist**:
- [ ] Processes all 395 doc files
- [ ] Classifies each information item by type
- [ ] Maps Type 1-4 to code locations
- [ ] Reports coverage percentage
- [ ] Identifies any MISSING items

---

### `validation/report.py`

**Purpose**: Generate comprehensive lossless verification report.

**Primary Docs**:
- This file (P6-VALIDATION.md) — report format

**Depends On**: All other validation modules.

**Exports**: `generate_report() → str`

**Key Constraints**:
- Aggregates results from:
  - structural_check → StructuralReport
  - value_check → ValueReport
  - cross_reference → CrossRefReport
  - traceability → TraceabilityMatrix
- Report sections:
  1. Executive Summary (pass/fail, coverage %)
  2. Structural Inventory (expected vs actual counts)
  3. Value Verification (per-model results)
  4. Cross-Reference Integrity (all references valid?)
  5. Traceability Matrix (full mapping)
  6. Discrepancy Analysis (any remaining gaps?)
  7. Recommendations (what to fix)
- Output: markdown-formatted report

**Verification Checklist**:
- [ ] Report is valid markdown
- [ ] All 4 sub-reports included
- [ ] Executive summary has clear PASS/FAIL
- [ ] Traceability coverage percentage calculated

---

## Verification Gate G6

```python
from Musical_Intelligence.validation import (
    run_structural_check,
    run_value_check,
    run_cross_reference_check,
    generate_traceability_matrix,
    generate_report
)

# Run all checks
structural = run_structural_check()
values = run_value_check()
cross_ref = run_cross_reference_check()
traceability = generate_traceability_matrix()

# Generate report
report = generate_report()

# Verify coverage
assert structural.coverage == 100.0, f"Structural: {structural.coverage}%"
assert values.pass_rate == 100.0, f"Values: {values.pass_rate}%"
assert cross_ref.all_valid, f"Cross-ref failures: {cross_ref.failures}"
assert traceability.coverage >= 99.0, f"Traceability: {traceability.coverage}%"

print("G6 PASSED: Lossless verification complete")
print(f"  Structural coverage: {structural.coverage}%")
print(f"  Value match rate: {values.pass_rate}%")
print(f"  Cross-references valid: {cross_ref.all_valid}")
print(f"  Traceability coverage: {traceability.coverage}%")
```

---

## Final Project Metrics

After all 6 phases complete:

| Metric | Target | Source |
|--------|:------:|--------|
| Code files | ~297 | Package structure |
| Documentation files processed | 395 | MI-DOC-ARCHITECTURE.md |
| Type 1 (executable) coverage | 100% | traceability.py |
| Type 2 (metadata) coverage | 100% | traceability.py |
| Type 3 (constants) coverage | 100% | value_check.py |
| Type 4 (validation) coverage | 100% | structural_check.py |
| Type 5 (narrative) coverage | >90% | docstring check |
| Type 6 (process) coverage | N/A | docs-only |
| R³ dimensions | 128 | R3Extractor output |
| H³ sparse tuples | ~8,600 | DemandTree |
| C³ models | 96 | ModelRegistry |
| C³ output | 1,006D | BrainOrchestrator output |
| L³ dimensions | 104 | L3Orchestrator output |
| MI-space total | 1,366D | MIPipeline output |
| Max file length | ≤1000 lines | structural check |
