# L³ Groups — Dependent (Phase 2)

**Version**: 2.1.0
**Groups**: 3 (ζ, η, θ)
**Dimensions**: 12 + 12 + 16 = 40
**Phase**: 2 (Dependent, Stateless)
**Code**: `mi_beta/language/groups/{zeta,eta,theta}.py`
**Updated**: 2026-02-13

---

## Overview

Phase 2 groups have **dependency chains** — they require outputs from Phase 1 groups (specifically from epsilon) and/or from each other. All three are stateless but must execute in dependency order.

### Dependency Chain

```
epsilon (19D) ──┬──→ zeta (12D) ──→ eta (12D)
                │
                └──────┬──────────→ theta (16D)
                       │
zeta (12D) ────────────┘
```

- **ζ Zeta** reads: BrainOutput + epsilon_output
- **η Eta** reads: zeta_output (BrainOutput as fallback only)
- **θ Theta** reads: BrainOutput + epsilon_output + zeta_output

**Execution order**: ε must complete before ζ; ζ must complete before η; ε and ζ must complete before θ.

---

## Group Summary

| Group | Symbol | Level | Dim | Output Range | Dependencies | Question | Code |
|-------|:------:|:-----:|:---:|:------------:|--------------|----------|------|
| Zeta | ζ | 6 | 12 | **[-1, +1]** | BrainOutput, ε | WHICH direction? | `zeta.py` (145 lines) |
| Eta | η | 7 | 12 | [0, 1] | ζ | WHAT word? | `eta.py` (176 lines) |
| Theta | θ | 8 | 16 | [0, 1] | BrainOutput, ε, ζ | HOW describe? | `theta.py` (155 lines) |

---

## Key Characteristics

1. **Bipolar output**: Zeta is the only L³ group with [-1,+1] output range (all others are [0,1])
2. **Vocabulary quantization**: Eta converts continuous polarity to 64 discrete gradation levels
3. **Narrative structure**: Theta produces Subject/Predicate/Modifier/Connector sentence slots
4. **Graceful fallback**: All three handle missing dependency outputs by defaulting to neutral values (zero tensors or 0.5 fill)

---

## File Listing

| File | Description |
|------|-------------|
| [Zeta.md](Zeta.md) | ζ Polarity — 12 bipolar axes with named neg/pos poles |
| [Eta.md](Eta.md) | η Vocabulary — 64-gradation quantization, 96 semantic terms |
| [Theta.md](Theta.md) | θ Narrative — 16D sentence structure (Subject/Predicate/Modifier/Connector) |

---

## Parent / See Also

- **Parent**: [Groups/00-INDEX.md](../00-INDEX.md)
- **Independent groups**: [Independent/00-INDEX.md](../Independent/00-INDEX.md) — Phase 1
- **Epsilon (key dependency)**: [Independent/Epsilon.md](../Independent/Epsilon.md) — provides learning signals to ζ and θ
- **Epistemology**: [Epistemology/00-INDEX.md](../../Epistemology/00-INDEX.md) — Levels 6--8
- **Registry**: [Registry/DimensionCatalog.md](../../Registry/DimensionCatalog.md) — global indices
