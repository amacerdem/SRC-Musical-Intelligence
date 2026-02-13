# L³ Groups — Master Index

**Version**: 2.1.0
**Total Dimensions**: 104D (variable + variable + 13 + 12 + 19 + 12 + 12 + 16)
**Groups**: 8 (alpha through theta)
**Code**: `mi_beta/language/groups/`
**Updated**: 2026-02-13

---

## Cross-Group Comparison

| Group | Symbol | Level | Dim | Phase | Stateful | Dependencies | Output Range | Question | Code File |
|-------|:------:|:-----:|:---:|:-----:|:--------:|--------------|:------------:|----------|-----------|
| Alpha | α | 1 | var | 1 | No | BrainOutput | [0,1] | HOW computed? | `alpha.py` (98 lines) |
| Beta | β | 2 | var | 1 | No | BrainOutput, ModelRegistry | [0,1] | WHERE in brain? | `beta.py` (123 lines) |
| Gamma | γ | 3 | 13 | 1 | No | BrainOutput | [0,1] | WHAT subjectively? | `gamma.py` (134 lines) |
| Delta | δ | 4 | 12 | 1 | No | BrainOutput | [0,1] | HOW to test? | `delta.py` (112 lines) |
| Epsilon | ε | 5 | 19 | 1b | **Yes** | BrainOutput | [0,1] | HOW learn? | `epsilon.py` (336 lines) |
| Zeta | ζ | 6 | 12 | 2 | No | BrainOutput, ε | **[-1,+1]** | WHICH direction? | `zeta.py` (145 lines) |
| Eta | η | 7 | 12 | 2 | No | ζ | [0,1] | WHAT word? | `eta.py` (176 lines) |
| Theta | θ | 8 | 16 | 2 | No | BrainOutput, ε, ζ | [0,1] | HOW describe? | `theta.py` (155 lines) |

---

## Computation Phases

### Phase 1 — Independent Groups (α, β, γ, δ)

Read **only** BrainOutput. Stateless. Can execute in parallel.

- **α** (variable D): Per-unit attribution + certainty + bipolar activation
- **β** (variable D): Per-brain-region activation from ModelRegistry
- **γ** (13D): Psychology — reward, ITPRA, aesthetics, emotion, chills
- **δ** (12D): Validation — physiological, neural, behavioral, temporal

### Phase 1b — Stateful Independent (ε)

Reads only BrainOutput but maintains internal state (EMA, Markov, Welford, ring buffer). Must execute after Phase 1 conceptually but before Phase 2 consumers.

- **ε** (19D): Learning dynamics — surprise, PE, precision, information, ITPRA, reward

### Phase 2 — Dependent Groups (ζ, η, θ)

Require outputs from earlier groups. Must execute in dependency order.

- **ζ** (12D): Reads BrainOutput + ε → bipolar polarity axes
- **η** (12D): Reads ζ → 64-gradation vocabulary quantization
- **θ** (16D): Reads BrainOutput + ε + ζ → narrative sentence structure

```
brain_output ─────────┬──→ α (var D)
                      ├──→ β (var D)          Phase 1: Independent
                      ├──→ γ (13D)            (read only BrainOutput)
                      ├──→ δ (12D)
                      ├──→ ε (19D) ──┬──→ ζ (12D) ──→ η (12D)
                      │     STATEFUL │                     Phase 2: Dependent
                      │              └──────┬──────────→ θ (16D)
                      └─────────────────────┘
```

---

## Design Principles

1. **Zero learned parameters** — every dimension is a deterministic formula
2. **Every dimension is citable** — at least one peer-reviewed source
3. **Graceful degradation** — `_safe_get_dim()` returns 0.5 for missing Brain dims
4. **Single stateful group** — only ε maintains state; reset between audio files
5. **Bipolar exception** — only ζ outputs [-1,+1]; all others output [0,1]

---

## File Listing

| File | Description |
|------|-------------|
| [Independent/00-INDEX.md](Independent/00-INDEX.md) | Phase 1 overview |
| [Independent/Alpha.md](Independent/Alpha.md) | α Computation Semantics (variable D) |
| [Independent/Beta.md](Independent/Beta.md) | β Neuroscience Semantics (variable D) |
| [Independent/Gamma.md](Independent/Gamma.md) | γ Psychology Semantics (13D) |
| [Independent/Delta.md](Independent/Delta.md) | δ Validation Semantics (12D) |
| [Independent/Epsilon.md](Independent/Epsilon.md) | ε Learning Dynamics (19D, STATEFUL) |
| [Dependent/00-INDEX.md](Dependent/00-INDEX.md) | Phase 2 overview |
| [Dependent/Zeta.md](Dependent/Zeta.md) | ζ Polarity (12D, [-1,+1]) |
| [Dependent/Eta.md](Dependent/Eta.md) | η Vocabulary (12D, 64-gradation) |
| [Dependent/Theta.md](Dependent/Theta.md) | θ Narrative (16D) |

---

## Parent / See Also

- **Parent**: [L³ 00-INDEX.md](../00-INDEX.md)
- **Epistemology**: [Epistemology/00-INDEX.md](../Epistemology/00-INDEX.md) — theoretical framework
- **Registry**: [Registry/DimensionCatalog.md](../Registry/DimensionCatalog.md) — global dimension indices
- **Pipeline**: [Pipeline/DependencyDAG.md](../Pipeline/DependencyDAG.md) — execution ordering
- **Code**: `mi_beta/language/groups/` (8 files, ~1,279 total lines)
