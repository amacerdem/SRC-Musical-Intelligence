# L³ Contracts — Index

**Scope**: Interface specifications for the L³ semantic interpretation layer. These contracts define the ABCs, output formats, orchestration protocol, and state management rules that all L³ components must follow.

---

## Files

| File | Description |
|------|-------------|
| [BaseSemanticGroup.md](BaseSemanticGroup.md) | ABC for all 8 semantic groups: class constants, abstract methods, validation |
| [SemanticGroupOutput.md](SemanticGroupOutput.md) | Output dataclass: fields, tensor shape convention, post-init validation |
| [BaseModelSemanticAdapter.md](BaseModelSemanticAdapter.md) | Per-unit adapter ABC: maps unit output dimensions to semantic group inputs |
| [L3Orchestrator.md](L3Orchestrator.md) | Group coordination: registration, phase execution, dependency ordering, reset |
| [EpsilonStateContract.md](EpsilonStateContract.md) | Stateful group state management: lifecycle, state components, memory budget |

---

## Quick Reference

| Contract | Code File | Key Method | Used By |
|----------|-----------|------------|---------|
| BaseSemanticGroup | `mi_beta/contracts/base_semantic_group.py` | `compute()`, `validate()` | All 8 groups (alpha through theta) |
| SemanticGroupOutput | `mi_beta/contracts/base_semantic_group.py` | `__post_init__()` | All groups (return type of `compute()`) |
| BaseModelSemanticAdapter | `mi_beta/language/adapters/_base_adapter.py` | `adapt()` | 9 unit adapters (SPU, STU, IMU, ASU, NDU, MPU, PCU, ARU, RPU) |
| L3Orchestrator | `mi_beta/language/groups/__init__.py` | `compute()`, `reset()` | Application code, pipeline entry point |
| EpsilonStateContract | `mi_beta/language/groups/epsilon.py` | `_init_state()`, `reset()` | EpsilonGroup only |

---

## Contract Relationships

```
BaseSemanticGroup (ABC)
    |
    +-- defines --> SemanticGroupOutput (return type)
    |
    +-- implemented by --> 8 groups (alpha..theta)
    |
    +-- coordinated by --> L3Orchestrator
                              |
                              +-- delegates reset --> EpsilonStateContract
                              |
                              +-- manages phase ordering

BaseModelSemanticAdapter (ABC)
    |
    +-- implemented by --> 9 unit adapters
    |
    +-- maps --> UnitOutput dimensions to semantic group inputs
```

---

## Cross-References

| Related Document | Path |
|-----------------|------|
| L³ master index | [../00-INDEX.md](../00-INDEX.md) |
| L³ architecture | [../L3-SEMANTIC-ARCHITECTURE.md](../L3-SEMANTIC-ARCHITECTURE.md) |
| Extension guide | [../EXTENSION-GUIDE.md](../EXTENSION-GUIDE.md) |
| Group specifications | [../Groups/00-INDEX.md](../Groups/00-INDEX.md) |
| Pipeline execution | [../Pipeline/ExecutionModel.md](../Pipeline/ExecutionModel.md) |

---

**Parent**: [../00-INDEX.md](../00-INDEX.md)
