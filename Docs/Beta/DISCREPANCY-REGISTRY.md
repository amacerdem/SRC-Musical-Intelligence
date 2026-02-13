# Discrepancy Registry — Phase 6 Documentation & Code Validation

**Version**: 1.0.0
**Date**: 2026-02-13
**Scope**: 391 documentation files + 94 code implementations
**Purpose**: Exact specification for Phase 7 code changes

---

## Summary

| Category | Count | Action |
|----------|:-----:|--------|
| **EXPECTED** | 12 | Code intentionally behind docs — fix in Phase 7 |
| **DOC-BUG** | 7 | Documentation errors — **ALL FIXED in Phase 6** |
| **CODE-BUG** | 1 | Code inconsistency — fix in Phase 7 |

---

## EXPECTED Discrepancies (Fix in Phase 7)

These are intentional: docs describe v2 features not yet implemented in code.

| ID | Category | Scope | Description | Fix Phase |
|:--:|----------|:-----:|-------------|:---------:|
| E01 | h3_demand empty | 94 models | All models return `()` in code; docs (Section 5) have populated 4-tuples | 7B |
| E02 | gamma OUTPUT_DIM | ~26 models | Code=10, doc=9 for all gamma-tier models | 7B |
| E03 | ASU MECHANISM_NAMES | 9 models | Code=`("ASA",)`, doc=`("BEP","ASA")` | 7B |
| E04 | FULL_NAME mismatches | ~30+ models | Code `FULL_NAME` differs from doc Section 1 header | 7B |
| E05 | R3_DIM 49→128 | constants.py | Code=49, docs=128 (R³ v2 expansion) | 7C |
| E06 | R³ groups F-K | 6 groups | Exist in docs only, not yet in code | 7C |
| E07 | H3_TOTAL_DIM | constants.py | Code=2304, doc v2=294,912 (depends on R³ v2) | 7D |
| E08 | Model files missing | 2 models | CHPI.py, SSRI.py are doc-only (no code yet) | 7A |
| E09 | L³ adapter stubs | 9 adapters | All return raw tensor `{"tensor": unit_output.tensor}`; docs describe real semantic mapping | 7E |
| E10 | R³ naming mismatches | 6 features | Code names ≠ doc semantic labels: [5] periodicity→roughness_total, [7] amplitude→velocity_A, [8] loudness→velocity_D, [10] spectral_flux→onset_strength, [14] tonalness→brightness_kuttruff, [21] spectral_change→spectral_flux | 7C |
| E11 | dimension_names drift | ~20 models | Minor code↔doc dimension name differences | 7B |
| E12 | MORPH_SCALE TBD | constants.py | MorphScaling.md notes some (gain,bias) values as "TBD" pending calibration | 7D |

---

## DOC-BUG Items (ALL FIXED in Phase 6)

| ID | File | Issue | Fix Applied |
|:--:|------|-------|-------------|
| D01 | `Docs/C³/Units/00-INDEX.md` | PCU=9, RPU=9, Total=94 (wrong) | Updated to PCU=10, RPU=10, Total=96 |
| D02 | `Docs/C³/Units/PCU.md` | Model Count=9, missing CHPI from roster and doc links | Updated to 10, added CHPI β4 row + link |
| D03 | `Docs/C³/Units/RPU.md` | Model Count=9, missing SSRI from roster and doc links | Updated to 10, added SSRI β4 row + link |
| D04 | `Docs/C³/Models/00-INDEX.md` | PCU/RPU section headers say "(9 models)" | Updated both to "(10 models)" |
| D05 | `Docs/C³/00-INDEX.md` | MISSING — no root C³ index existed | Created: root index listing all 11 subdirectories |
| D06 | `Docs/C³/Tiers/00-INDEX.md` | MISSING — tier docs had no index | Created: lists Alpha(27), Beta(40), Gamma(29) = 96 |
| D07 | `Docs/C³/Matrices/00-INDEX.md` | MISSING — matrix docs had no index | Created: lists all 5 aggregate matrix files |

---

## CODE-BUG Items (Fix in Phase 7)

| ID | File | Issue | Fix Phase |
|:--:|------|-------|:---------:|
| C01 | `mi_beta/core/constants.py` | `CIRCUITS` (line ~210, 5 entries) vs `CIRCUIT_NAMES` (line ~112, 6 entries) — "imagery" missing from `CIRCUITS` | 7A |

**Note**: `Docs/C³/Circuits/00-INDEX.md` correctly documents this distinction: `CIRCUIT_NAMES` is the full conceptual set (6), `CIRCUITS` is the operational set for pathway routing (5, excludes imagery). Whether this is truly a bug or intentional design depends on Phase 7 architecture decisions.

---

## Validation Summary by Sub-Phase

| Sub-Phase | Scope | Result |
|:---------:|-------|--------|
| **6A** | Structural Inventory: 391 docs + all components | **PASS** — all expected files exist |
| **6C** | C³ Cross-References: units↔models↔mechanisms↔circuits | **7 DOC-BUGs found → ALL FIXED** |
| **6D** | R³ Internal Consistency: 128D, 11 groups, mappings | **PASS** — all checks pass |
| **6E** | H³ Internal Consistency: 32H × 24M × 3L, demands | **PASS** — all checks pass |
| **6F** | L³ Internal Consistency: 104D, 8 groups, 96 terms | **PASS** — all checks pass |
| **6G** | Cross-Layer Pipeline: R³→H³→C³→L³ | **PASS** — version refs consistent |
| **6H** | Index Integrity: 55 existing + 3 created = 58 total | **3 DOC-BUGs found → ALL FIXED** |

---

## Quality Gate Checklist

- [x] Structural inventory covers all 94 code models + 96 doc models + all components
- [x] C³ aggregate cross-references verified (Units, Mechanisms, Circuits, Pathways)
- [x] R³ feature groups A-K and dimension sums verified (49 v1, 128 v2)
- [x] H³ horizons(32), morphs(24), laws(3) verified
- [x] L³ vocabulary 96 terms across 12 axes verified
- [x] Cross-layer pipeline chain validated (R³→H³→C³→L³)
- [x] All 58 00-INDEX files verified complete (55 existing + 3 newly created)
- [x] DISCREPANCY-REGISTRY.md created (this file)
- [x] All 7 DOC-BUG items fixed — zero remaining doc errors

---

## Files Modified in Phase 6

| File | Change |
|------|--------|
| `Docs/C³/Units/00-INDEX.md` | PCU 9→10, RPU 9→10, Total 94→96 |
| `Docs/C³/Units/PCU.md` | Count 9→10, added CHPI to roster + docs |
| `Docs/C³/Units/RPU.md` | Count 9→10, added SSRI to roster + docs |
| `Docs/C³/Models/00-INDEX.md` | PCU/RPU headers "(9 models)"→"(10 models)" |
| `Docs/C³/00-INDEX.md` | **NEW** — root C³ index |
| `Docs/C³/Tiers/00-INDEX.md` | **NEW** — tier index |
| `Docs/C³/Matrices/00-INDEX.md` | **NEW** — matrices index |
| `Docs/Beta/DISCREPANCY-REGISTRY.md` | **NEW** — this file |
