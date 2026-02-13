# L³ Group Map

**Scope**: Index-range mapping, dimensionality, execution phase, and dependencies for all 8 semantic groups.

---

## Group Registry

| # | Symbol | Name | Index Range | Dim | Phase | Dependencies | Stateful | Code File |
|:-:|:------:|------|:----------:|:---:|:-----:|:-------------|:--------:|-----------|
| 1 | α | Computation | [0:6] | 6 | 1 | — | No | `mi_beta/language/groups/alpha.py` |
| 2 | β | Neuroscience | [6:20] | 14 | 1 | — | No | `mi_beta/language/groups/beta.py` |
| 3 | γ | Psychology | [20:33] | 13 | 1 | — | No | `mi_beta/language/groups/gamma.py` |
| 4 | δ | Validation | [33:45] | 12 | 1 | — | No | `mi_beta/language/groups/delta.py` |
| 5 | ε | Learning | [45:64] | 19 | 1b | — | **Yes** | `mi_beta/language/groups/epsilon.py` |
| 6 | ζ | Polarity | [64:76] | 12 | 2a | ε | No | `mi_beta/language/groups/zeta.py` |
| 7 | η | Vocabulary | [76:88] | 12 | 2b | ζ | No | `mi_beta/language/groups/eta.py` |
| 8 | θ | Narrative | [88:104] | 16 | 2c | ε, ζ | No | `mi_beta/language/groups/theta.py` |

**Total**: 6 + 14 + 13 + 12 + 19 + 12 + 12 + 16 = **104 dimensions**

---

## Phase Execution Order

```
Phase 1  (Independent):   α, β, γ, δ  — read only BrainOutput, no mutual dependencies
Phase 1b (Stateful):      ε            — read only BrainOutput, maintains internal state
Phase 2a (Dependent):     ζ            — reads ε output
Phase 2b (Dependent):     η            — reads ζ output
Phase 2c (Dependent):     θ            — reads ε + ζ output
```

## Output Ranges

| Range | Groups | Encoding |
|-------|--------|----------|
| `[0, 1]` | α, β, γ, δ, ε, η, θ | Unipolar sigmoid/clamp |
| `[-1, +1]` | ζ | Bipolar semantic axes |

## Variable Dimensionality (mi_beta)

In the mi_beta implementation, **α** and **β** have variable output dimensionality:

| Group | Doc Spec (mi v2) | mi_beta Behavior |
|-------|:----------------:|:----------------:|
| α | 6D (fixed) | N_active_units + 2 (auto-configured) |
| β | 14D (fixed) | N_unique_regions + 3 + 3 (auto-configured) |
| γ–θ | Fixed | Same as doc spec |

The L3Orchestrator (`mi_beta/language/groups/__init__.py`) computes `total_dim` dynamically:

```python
@property
def total_dim(self) -> int:
    return sum(g.OUTPUT_DIM for g in self.groups.values())
```

---

## Dependency Graph

```
BrainOutput ──┬──→ α (6D)      ┐
              ├──→ β (14D)     │ Phase 1
              ├──→ γ (13D)     │ (independent)
              ├──→ δ (12D)     ┘
              │
              ├──→ ε (19D) ─── Phase 1b (stateful)
              │        │
              │        ├──→ ζ (12D) ── Phase 2a
              │        │       │
              │        │       ├──→ η (12D) ── Phase 2b
              │        │       │
              │        └───┬───┘
              │            ↓
              └────────→ θ (16D) ── Phase 2c
```

---

**Parent**: [00-INDEX.md](00-INDEX.md)
**See also**: [DimensionCatalog.md](DimensionCatalog.md) for per-dimension detail
