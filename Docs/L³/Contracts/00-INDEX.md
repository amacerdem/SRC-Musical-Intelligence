# L³ Contracts — Index

Overview of the 5 interface contracts that govern L³ semantic interpretation.

## Contract Registry

| Contract | Code File | Key Method | Used By |
|----------|-----------|------------|---------|
| [BaseSemanticGroup](BaseSemanticGroup.md) | `mi_beta/contracts/base_semantic_group.py` | `compute()` | All 8 groups |
| [SemanticGroupOutput](SemanticGroupOutput.md) | `mi_beta/contracts/base_semantic_group.py` | `__post_init__()` | All groups |
| [BaseModelSemanticAdapter](BaseModelSemanticAdapter.md) | `mi_beta/language/adapters/_base_adapter.py` | `adapt()` | 9 unit adapters |
| [L3Orchestrator](L3Orchestrator.md) | `mi_beta/language/groups/__init__.py` | `compute()` | Brain pipeline |
| [EpsilonStateContract](EpsilonStateContract.md) | `mi_beta/language/groups/epsilon.py` | `reset()` | Epsilon only |

## Design Principles

1. **ABC-first**: All groups inherit from `BaseSemanticGroup`
2. **Validated output**: `SemanticGroupOutput.__post_init__()` enforces dimension count match
3. **Dependency injection**: Cross-group data passed via `**kwargs` (e.g., `epsilon_output=...`)
4. **Lazy state**: Only epsilon maintains state; all other groups are stateless
5. **Adapter pattern**: Per-unit adapters decouple unit outputs from semantic group inputs

---

**Parent**: [../00-INDEX.md](../00-INDEX.md)
