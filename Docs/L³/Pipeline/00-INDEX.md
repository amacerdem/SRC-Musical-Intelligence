# L³ Pipeline — Index

**Version**: 2.1.0
**Scope**: Execution architecture of the L3Orchestrator
**Updated**: 2026-02-13

---

## Overview

The L³ Pipeline documents how the L3Orchestrator manages dependency-ordered computation across 8 semantic groups in 5 execution phases. The orchestrator reads a single `BrainOutput` tensor from C³ and produces a concatenated `L3Output` tensor of 104 dimensions (reference spec), accumulating results from alpha through theta.

Key architectural properties:
- **5 phases**: Phase 1 (4 independent groups), Phase 1b (1 stateful group), Phases 2a/2b/2c (3 dependent groups)
- **1 stateful group**: Only epsilon maintains state across frames; all others are pure functions
- **Variable output**: Alpha and beta auto-configure dimensionality from the active model set
- **Zero learned parameters**: Every dimension is a deterministic formula

---

## Documents

| Document | Purpose | Lines |
|----------|---------|:-----:|
| [DependencyDAG.md](DependencyDAG.md) | Phase dependency graph, data flow edges, parallelism | ~120 |
| [ExecutionModel.md](ExecutionModel.md) | Step-by-step orchestrator execution sequence | ~150 |
| [StateManagement.md](StateManagement.md) | Epsilon state lifecycle, reset protocol, memory | ~150 |
| [Performance.md](Performance.md) | Per-group compute cost and memory analysis | ~100 |

---

## Quick Reference

```
BrainOutput ──┬──> alpha (6D)   ┐
              ├──> beta  (14D)  │ Phase 1 (independent, parallelizable)
              ├──> gamma (13D)  │
              ├──> delta (12D)  ┘
              │
              ├──> epsilon (19D) ── Phase 1b (stateful)
              │        |
              │        +──> zeta (12D) ── Phase 2a
              │        |       |
              │        |       +──> eta (12D) ── Phase 2b
              │        |
              │        +───────+──> theta (16D) ── Phase 2c
              │                |
              └────────────────┘
```

**Total**: 104D (reference spec) = 6 + 14 + 13 + 12 + 19 + 12 + 12 + 16

---

## Cross-References

| Related Document | Path |
|-----------------|------|
| L3Orchestrator contract | [../Contracts/L3Orchestrator.md](../Contracts/L3Orchestrator.md) |
| EpsilonStateContract | [../Contracts/EpsilonStateContract.md](../Contracts/EpsilonStateContract.md) |
| Group specifications | [../Groups/00-INDEX.md](../Groups/00-INDEX.md) |
| Adapter overview | [../Adapters/00-INDEX.md](../Adapters/00-INDEX.md) |
| L³ master index | [../00-INDEX.md](../00-INDEX.md) |
| Orchestrator code | `mi_beta/language/groups/__init__.py` |

---

**Parent**: [../00-INDEX.md](../00-INDEX.md)
