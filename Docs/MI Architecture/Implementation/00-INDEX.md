# Implementation Plan — Index

**Version**: 1.0.0
**Date**: 2026-02-14
**Scope**: 395 documentation files → ~297 code files (lossless conversion)
**Strategy**: Contracts-first, then bottom-up layer implementation
**Constraint**: Max ~1000 lines per code file

---

## Documents in This Directory

| File | Phase | Content | Est. Code Files |
|------|:-----:|---------|:---------------:|
| [MASTER-PLAN.md](MASTER-PLAN.md) | — | Architecture overview, phase sequencing, agent protocol, traceability rules | — |
| [P1-CONTRACTS.md](P1-CONTRACTS.md) | P1 | Frozen dataclasses + ABC base classes | 14 |
| [P2-EAR-R3.md](P2-EAR-R3.md) | P2 | R³ spectral features (128D, 11 groups, 3-stage DAG) | 62 |
| [P2-EAR-H3.md](P2-EAR-H3.md) | P2 | H³ temporal morphology (32H × 24M × 3L) | 38 |
| [P3-BRAIN.md](P3-BRAIN.md) | P3 | C³ cognitive models (96 models, 10 mechanisms, 9 units) | 156 |
| [P4-SEMANTICS.md](P4-SEMANTICS.md) | P4 | L³ semantic interpretation (104D, 8 groups) | 25 |
| [P5-PIPELINE.md](P5-PIPELINE.md) | P5 | End-to-end pipeline + cochlea | 6 |
| [P6-VALIDATION.md](P6-VALIDATION.md) | P6 | Lossless traceability verification | 6 |

---

## Phase Dependency Graph

```
P1 (Contracts)
 ├──→ P2 (Ear: R³ + H³)
 │     └──→ P3 (Brain: Mechanisms → Units → Models → Pathways)
 │           └──→ P4 (Semantics: Groups → Adapters → Orchestrator)
 │                 └──→ P5 (Pipeline: end-to-end)
 │                       └──→ P6 (Validation: lossless verification)
 └──→ P5 (Pipeline depends on P1 contracts directly too)
```

**Parallelizable**: P2-R3 and P2-H3 can run in parallel after P1 completes.

---

## Agent Protocol Summary

Every code file implementation MUST follow the **READ → ANALYZE → IMPLEMENT → VERIFY** cycle:

1. **READ**: Open and fully read the primary doc(s) listed for that file
2. **ANALYZE**: Cross-reference with related docs to understand dependencies
3. **IMPLEMENT**: Write code that captures ALL information from the docs
4. **VERIFY**: Run the verification checklist for that specific file

See [MASTER-PLAN.md §3](MASTER-PLAN.md) for the full agent protocol.

---

## Key Cross-References

| Layer Doc | Location |
|-----------|----------|
| MI Vision | `Docs/Vision/MI-VISION.md` |
| MI Doc Architecture | `Docs/MI Architecture/MI-Doc/MI-DOC-ARCHITECTURE.md` |
| Discrepancy Registry | `Docs/Beta/DISCREPANCY-REGISTRY.md` |
| R³ Architecture | `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md` |
| H³ Architecture | `Docs/H³/H3-TEMPORAL-ARCHITECTURE.md` |
| C³ Architecture | `Docs/C³/C3-ARCHITECTURE.md` |
| L³ Architecture | `Docs/L³/L3-SEMANTIC-ARCHITECTURE.md` |

---

## File Count Summary

| Category | Files | Lines Est. |
|----------|:-----:|:----------:|
| contracts/ | 14 | ~2,800 |
| ear/cochlea/ | 3 | ~400 |
| ear/r3/ | 62 | ~12,000 |
| ear/h3/ | 38 | ~5,500 |
| brain/ | 156 | ~45,000 |
| semantics/ | 25 | ~5,000 |
| pipeline/ | 3 | ~600 |
| validation/ | 6 | ~2,000 |
| **Total** | **~307** | **~73,300** |
