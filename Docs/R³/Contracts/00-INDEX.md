# R3 Contracts -- Index

**Scope**: Interface contracts governing the R3 spectral feature architecture.
**Status**: Current (v1, 49D) with Phase 6 planned changes (v2, 128D) annotated throughout.

---

## Contract Documents

| # | Document | Subject | Code Location |
|---|----------|---------|---------------|
| 1 | [BaseSpectralGroup.md](BaseSpectralGroup.md) | ABC for all spectral feature groups | `mi_beta/contracts/base_spectral_group.py` |
| 2 | [R3FeatureRegistry.md](R3FeatureRegistry.md) | Registry lifecycle: register, freeze, query | `mi_beta/ear/r3/_registry.py` |
| 3 | [R3FeatureSpec.md](R3FeatureSpec.md) | Per-feature registration dataclass | `mi_beta/contracts/feature_spec.py` |
| 4 | [R3Extractor.md](R3Extractor.md) | Orchestrator: discovery, registration, extraction | `mi_beta/ear/r3/__init__.py` |
| 5 | [ExtensionProtocol.md](ExtensionProtocol.md) | Extension system for adding new groups | `mi_beta/ear/r3/extensions/_template.py` |

---

## Contract Summary

The R3 spectral architecture is governed by five interlocking contracts:

```
BaseSpectralGroup (ABC)
        |
        | subclassed by
        v
[ConsonanceGroup, EnergyGroup, TimbreGroup, ChangeGroup, InteractionsGroup, ...]
        |
        | registered into
        v
R3FeatureRegistry
        |
        | freeze() produces
        v
R3FeatureMap  (frozen snapshot: total_dim + per-group R3GroupInfo)
        |
        | consumed by
        v
R3Extractor  (orchestrates compute, produces R3Output)
        |
        | validates with
        v
R3FeatureSpec  (per-feature index, name, group, citation)
```

### Key Invariants

1. **Contiguous indexing**: Every group occupies a half-open interval `[start, end)` with no gaps or overlaps. Assigned automatically by `R3FeatureRegistry.freeze()`.
2. **Dimension consistency**: `group.OUTPUT_DIM == end - start == len(group.feature_names)`.
3. **Output range**: All features target `[0, 1]` unless explicitly documented otherwise.
4. **Name uniqueness**: No two features across any groups may share a name.
5. **Immutability after freeze**: Once `freeze()` is called, no further groups may be registered.

### Current State vs Phase 6

| Aspect | Current (v1) | Phase 6 (v2) |
|--------|-------------|--------------|
| Total dimensions | 49D (groups A-E) | 128D (groups A-K) |
| Groups | 5 | 11 |
| Index assignment | Hardcoded `INDEX_RANGE` | Auto-assigned by registry |
| Feature spec validation | `0 <= index < 49` | `0 <= index < R3_DIM` (dynamic) |
| Compute ordering | Sequential, no dependencies | 3-stage DAG with dependency injection |
| Extension mechanism | Manual modification | Auto-discovery from `extensions/` |

---

## Related Documentation

- **Pipeline/**: Execution ordering, normalization, performance, state management
- **Registry/**: Feature name catalog and dimension map
- **Standards/**: Naming conventions, output format specifications
- **R3-V2-DESIGN.md**: Full architecture design document (Phase 3B)
