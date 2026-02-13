# L³ Registry — Index

**Scope**: Canonical reference tables for the L³ semantic interpretation layer.

---

## Files

| File | Description |
|------|-------------|
| [DimensionCatalog.md](DimensionCatalog.md) | All 104 dimensions: global index, group, local index, name, range, formula, citation |
| [GroupMap.md](GroupMap.md) | 8 semantic groups: index range, dimensionality, phase, dependencies, code file |
| [NamingConventions.md](NamingConventions.md) | Dimension naming rules: Greek letters, snake_case, range conventions |

## Quick Reference

| Group | Symbol | Range | Dim | Phase | Stateful |
|-------|:------:|:-----:|:---:|:-----:|:--------:|
| Computation | α | [0:6] | 6 | 1 | No |
| Neuroscience | β | [6:20] | 14 | 1 | No |
| Psychology | γ | [20:33] | 13 | 1 | No |
| Validation | δ | [33:45] | 12 | 1 | No |
| Learning | ε | [45:64] | 19 | 1b | **Yes** |
| Polarity | ζ | [64:76] | 12 | 2 | No |
| Vocabulary | η | [76:88] | 12 | 2 | No |
| Narrative | θ | [88:104] | 16 | 2 | No |
| **Total** | | [0:104] | **104** | | |

---

**Code**: `mi_beta/core/types.py` (L3Output, SemanticGroupOutput)
**Parent**: [../00-INDEX.md](../00-INDEX.md)
