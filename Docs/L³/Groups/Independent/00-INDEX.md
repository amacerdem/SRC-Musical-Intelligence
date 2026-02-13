# L³ Groups — Independent (Phase 1)

**Version**: 2.1.0
**Groups**: 5 (α, β, γ, δ, ε)
**Dimensions**: variable + variable + 13 + 12 + 19 = 44 + variable
**Phase**: 1 (α,β,γ,δ stateless) + 1b (ε stateful)
**Code**: `mi_beta/language/groups/{alpha,beta,gamma,delta,epsilon}.py`
**Updated**: 2026-02-13

---

## Overview

Phase 1 groups read **only** BrainOutput — they have no dependencies on other L³ groups. The first four (α, β, γ, δ) are stateless and can execute in any order or in parallel. Epsilon (ε) is also independent of other groups but is **stateful**: it maintains EMA accumulators, a Markov transition matrix, Welford statistics, and a ring buffer across frames.

All Phase 1 groups output tensors in the **[0,1]** range. Missing Brain dimensions default to 0.5 (neutral) via `_safe_get_dim()`.

---

## Group Summary

| Group | Symbol | Level | Dim | Stateful | Question | Code |
|-------|:------:|:-----:|:---:|:--------:|----------|------|
| Alpha | α | 1 | variable | No | HOW was this computed? | `alpha.py` (98 lines) |
| Beta | β | 2 | variable | No | WHERE in the brain? | `beta.py` (123 lines) |
| Gamma | γ | 3 | 13 | No | WHAT does it mean subjectively? | `gamma.py` (134 lines) |
| Delta | δ | 4 | 12 | No | HOW to test empirically? | `delta.py` (112 lines) |
| Epsilon | ε | 5 | 19 | **Yes** | HOW does the listener learn? | `epsilon.py` (336 lines) |

---

## File Listing

| File | Description |
|------|-------------|
| [Alpha.md](Alpha.md) | α Computation Semantics — per-unit attribution, certainty, bipolar |
| [Beta.md](Beta.md) | β Neuroscience Semantics — brain region activations, neurotransmitters, circuits |
| [Gamma.md](Gamma.md) | γ Psychology Semantics — reward, ITPRA, aesthetics, emotion, chills |
| [Delta.md](Delta.md) | δ Validation Semantics — physiological, neural, behavioral, temporal |
| [Epsilon.md](Epsilon.md) | ε Learning Dynamics — surprise, PE, precision, information, ITPRA, reward (STATEFUL) |

---

## Shared Patterns

All five groups share the following patterns:

1. **Inherit** `BaseSemanticGroup` (ABC with `LEVEL`, `GROUP_NAME`, `OUTPUT_DIM`, `compute()`)
2. **Return** `SemanticGroupOutput(group_name, level, tensor, dimension_names)`
3. **Clamp** output to [0,1] via `tensor.clamp(0, 1)`
4. **Use** `_safe_get_dim(brain_output, name, default=0.5)` for graceful missing-dim handling
5. **Accept** `brain_output: Any` as first argument to `compute()`

---

## Parent / See Also

- **Parent**: [Groups/00-INDEX.md](../00-INDEX.md)
- **Dependent groups**: [Dependent/00-INDEX.md](../Dependent/00-INDEX.md) — Phase 2
- **Epistemology**: [Epistemology/00-INDEX.md](../../Epistemology/00-INDEX.md) — Levels 1--5
- **Registry**: [Registry/DimensionCatalog.md](../../Registry/DimensionCatalog.md) — global indices
