# H3 Contracts -- Interface Specifications

**Version**: 2.0.0
**Updated**: 2026-02-13
**Code path**: `mi_beta/ear/h3/` (5 files)

---

## Purpose

The Contracts directory documents each class and function in the H3 code as a formal interface specification. These are the "API contracts" that the H3 engine exposes to the rest of the MI system. Each document describes the public interface, input/output contracts, execution semantics, edge cases, and design rationale for a single code unit.

---

## Files

| Document | Code File | Class/Function | Lines |
|----------|-----------|---------------|:-----:|
| [H3Extractor.md](H3Extractor.md) | `__init__.py` | `H3Extractor` | 135 |
| [DemandTree.md](DemandTree.md) | `demand.py` | `DemandTree` | 44 |
| [EventHorizon.md](EventHorizon.md) | `horizon.py` | `EventHorizon` | 39 |
| [MorphComputer.md](MorphComputer.md) | `morph.py` | `MorphComputer` | 268 |
| [AttentionKernel.md](AttentionKernel.md) | `attention.py` | `compute_attention_weights()` | 43 |

---

## Dependency Graph

```
H3Extractor
  |--- DemandTree           (demand routing)
  |--- EventHorizon         (horizon lookup)
  |--- MorphComputer        (morph dispatch)
  |--- compute_attention_weights  (decay kernel)

DemandTree -------> constants (N_HORIZONS, N_MORPHS, N_LAWS)
EventHorizon -----> constants (HORIZON_FRAMES, HORIZON_MS, N_HORIZONS)
MorphComputer ----> constants (N_MORPHS, MORPH_SCALE)
compute_attention_weights -> constants (ATTENTION_DECAY)
```

---

## Cross-References

| Related Document | Location |
|-----------------|----------|
| H3 Architecture | [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) |
| H3DemandSpec | [../../C3/Contracts/H3DemandSpec.md](../../C3/Contracts/H3DemandSpec.md) |
| Registry | [../Registry/](../Registry/) |
| Morphology Catalog | [../Morphology/](../Morphology/) |
| Law Specifications | [../Laws/](../Laws/) |
| Band Specifications | [../Bands/](../Bands/) |
| Code | `mi_beta/ear/h3/` |
