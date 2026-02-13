# R3 Migration Documentation

**Scope**: Migration guides and backward compatibility strategy for R3 v1 (49D) to v2 (128D).
**Phase**: 3C -- Documentation Layer
**Status**: Active

---

## Contents

| File | Description | Key Content |
|------|-------------|-------------|
| [V1-to-V2.md](V1-to-V2.md) | 49D to 128D migration guide | Code changes, 3-layer migration strategy, phase timeline, rollback plan |
| [BackwardCompatibility.md](BackwardCompatibility.md) | Backward compatibility guarantees | Index preservation, formula change strategy, model code migration, testing |

---

## Relationship to Other Documentation

| Related Doc | Relationship |
|-------------|--------------|
| `R3-V2-DESIGN.md` Section 5 | Source: 6 code change specifications |
| `R3-V2-DESIGN.md` Section 8 | Source: phase roadmap and timeline |
| `R3-CROSSREF.md` Section 7.3 | Source: 3-layer backward compatibility strategy |
| `mi_beta/core/constants.py` | Primary migration target: R3_DIM, group boundaries |
| `mi_beta/core/dimension_map.py` | Migration target: _R3_FEATURE_NAMES tuple |
| `mi_beta/contracts/feature_spec.py` | Migration target: index validation bounds |
| `Validation/AcceptanceCriteria.md` | Acceptance gates must pass before migration proceeds |

---

## Migration Philosophy

The R3 v1-to-v2 migration follows three principles:

1. **Additive, not destructive**: New features [49:128] are added; existing features [0:49]
   are preserved. No existing feature changes meaning, index, or formula until Phase 6.

2. **Documentation before code**: Phase 3 defines all indices and feature names in documentation.
   Code changes happen in Phase 6. This allows 96 C3 model docs to reference new features
   before any code is written.

3. **Layered rollback**: Each migration layer can be independently rolled back without
   affecting previous layers. Layer 1 (docs) is independent of Layer 2 (code), which is
   independent of Layer 3 (formula revision).

---

## Migration Timeline Summary

```
Phase 3B (COMPLETE)  -- R3-V2-DESIGN.md: architecture defined
Phase 3C (CURRENT)   -- Documentation: indices, features, standards
Phase 3E (NEXT)      -- 96 model docs: Section 4 updates with [49:128] refs
Phase 6.1            -- constants.py, dimension_map.py, feature_spec.py
Phase 6.2            -- 6 new BaseSpectralGroup subclasses (F-K)
Phase 6.3            -- R3Extractor stage-ordered compute
Phase 6.4            -- A-E formula fixes (bugs, duplications)
Phase 6.5            -- E group interaction proxy fix
Phase 6.6            -- Benchmark validation (6 tests)
Phase 6.7            -- Integration test + 96 model code updates
```

---

## Revision History

| Date | Change |
|------|--------|
| 2026-02-13 | Initial creation (Phase 3C) |
