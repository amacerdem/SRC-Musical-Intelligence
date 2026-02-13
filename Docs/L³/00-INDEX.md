# L³ Semantic Architecture — Master Index

**Version**: 2.1.0
**Dimensions**: 104D total (8 semantic groups: α6 + β14 + γ13 + δ12 + ε19 + ζ12 + η12 + θ16)
**Status**: Phase 5 complete — 68 files, ~10,350 lines across 13 directories
**Updated**: 2026-02-13

---

## Overview

L³ (Lexical LOGOS Lattice) is MI's **semantic interpretation layer**. It answers the question: "What does this computation MEAN?"

The Brain (C³) produces a multi-dimensional output per frame across 96 cognitive models organized in 9 units. These are numbers. L³ provides **eight interpretation groups** (α through θ) that give the Brain output its scientific, psychological, and linguistic meaning.

**Pipeline position**: Audio → Cochlea (128-mel) → R³ (128D) → H³ (sparse) → **C³ Brain (1006D)** → **L³ (104D)** → MI-space

**Input**: BrainOutput tensor `(B, T, D)` where D depends on active units/models
**Output**: L3Output tensor `(B, T, 104)` with per-group semantic interpretation
**Properties**: Zero learned parameters. Every dimension has a formula and citation.

---

## 8-Level Epistemological Framework

| Level | Group | Question | Audience | Dim | Phase |
|:-----:|:-----:|----------|----------|:---:|:-----:|
| 1 | α Computation | HOW was this computed? | Engineers | 6 | 1 |
| 2 | β Neuroscience | WHERE in the brain? | Neuroscientists | 14 | 1 |
| 3 | γ Psychology | WHAT does it mean subjectively? | Psychologists | 13 | 1 |
| 4 | δ Validation | HOW to test empirically? | Experimenters | 12 | 1 |
| 5 | ε Learning | HOW does the listener learn? | Information theorists | 19 | 1b |
| 6 | ζ Polarity | WHICH direction? | Semanticists | 12 | 2 |
| 7 | η Vocabulary | WHAT word describes this? | Linguists, lay users | 12 | 2 |
| 8 | θ Narrative | HOW to describe in language? | Narrative researchers | 16 | 2 |
| | | **Total** | | **104** | |

---

## Computation Phases

```
brain_output ─────────┬──→ α (6D)
                      ├──→ β (14D)         Phase 1: Independent
                      ├──→ γ (13D)         (read only BrainOutput)
                      ├──→ δ (12D)
                      ├──→ ε (19D) ──┬──→ ζ (12D) ──┬──→ η (12D)
                      │     STATEFUL │               │         Phase 2: Dependent
                      │              └──────┬────────┘         (cascaded)
                      │                     ↓
                      └─────────────────→ θ (16D)
```

---

## Directory Structure

```
Docs/L³/
├── 00-INDEX.md                              ← You are here
├── L3-SEMANTIC-ARCHITECTURE.md              Definitive architecture document
├── CHANGELOG.md                             Version history
├── EXTENSION-GUIDE.md                       Developer extension guide
│
├── Registry/                                Canonical reference tables
│   ├── 00-INDEX.md
│   ├── DimensionCatalog.md                  All 104 dimensions with full metadata
│   ├── GroupMap.md                           8 groups: index range, dim, phase, deps
│   └── NamingConventions.md                 Dimension naming rules
│
├── Epistemology/                            8-level framework theory
│   ├── 00-INDEX.md                          Framework overview
│   ├── Computation.md                       Level 1 (α): HOW computed?
│   ├── Neuroscience.md                      Level 2 (β): WHERE in brain?
│   ├── Psychology.md                        Level 3 (γ): WHAT does it mean?
│   ├── Validation.md                        Level 4 (δ): HOW to test?
│   ├── Learning.md                          Level 5 (ε): HOW does listener learn?
│   ├── Polarity.md                          Level 6 (ζ): WHICH direction?
│   ├── Vocabulary.md                        Level 7 (η): WHAT word?
│   └── Narrative.md                         Level 8 (θ): HOW to describe?
│
├── Groups/                                  Per-group detailed specifications
│   ├── 00-INDEX.md                          Cross-group comparison
│   ├── Independent/                         Phase 1 groups (α, β, γ, δ, ε)
│   │   ├── 00-INDEX.md
│   │   ├── Alpha.md                         Computation (variable D)
│   │   ├── Beta.md                          Neuroscience (variable D)
│   │   ├── Gamma.md                         Psychology (13D)
│   │   ├── Delta.md                         Validation (12D)
│   │   └── Epsilon.md                       Learning (19D, STATEFUL)
│   └── Dependent/                           Phase 2 groups (ζ, η, θ)
│       ├── 00-INDEX.md
│       ├── Zeta.md                          Polarity (12D, [-1,+1])
│       ├── Eta.md                           Vocabulary (12D, 64-gradation)
│       └── Theta.md                         Narrative (16D)
│
├── Vocabulary/                              64-gradation linguistic system
│   ├── 00-INDEX.md
│   ├── TermCatalog.md                       96 terms (12 axes × 8 bands)
│   ├── GradationSystem.md                   64-level design + JND rationale
│   └── AxisDefinitions.md                   12 polarity axes with sources
│
├── Contracts/                               Interface specifications
│   ├── 00-INDEX.md
│   ├── BaseSemanticGroup.md                 ABC: LEVEL, GROUP_NAME, compute()
│   ├── SemanticGroupOutput.md               Output dataclass spec
│   ├── BaseModelSemanticAdapter.md          Per-unit adapter ABC
│   ├── L3Orchestrator.md                    Orchestrator dependency ordering
│   └── EpsilonStateContract.md              Stateful group reset protocol
│
├── Pipeline/                                Execution architecture
│   ├── 00-INDEX.md
│   ├── DependencyDAG.md                     Phase 1 → Phase 2 graph
│   ├── ExecutionModel.md                    Orchestrator sequence
│   ├── StateManagement.md                   Epsilon lifecycle
│   └── Performance.md                       Per-group compute cost
│
├── Adapters/                                Per-unit semantic mapping
│   ├── 00-INDEX.md                          Cross-unit adapter comparison
│   ├── SPU-L3-ADAPTER.md ... RPU-L3-ADAPTER.md (9 files)
│
├── Standards/
│   ├── 00-INDEX.md
│   ├── CitationQuality.md                   Per-dimension citation audit
│   └── PsychometricAlignment.md             Alignment with GEMS, SDT, circumplex
│
├── Validation/
│   ├── 00-INDEX.md
│   ├── AcceptanceCriteria.md                Per-group output validation
│   └── BenchmarkPlan.md                     Delta vs physiology, gamma vs ratings
│
├── Literature/
│   ├── 00-INDEX.md
│   └── L3-LITERATURE.md                     Per-dimension literature cross-ref
│
├── Migration/
│   ├── 00-INDEX.md
│   ├── V1-to-V2.md                          Per-model → unified Brain migration
│   └── DeprecatedFiles.md                   Archive inventory
│
└── Archive/                                 Deprecated files
    ├── 00-INDEX.md
    ├── L³-SRP-SEMANTIC-SPACE.md             v1.x SRP-only (DEPRECATED)
    ├── L³-AAC-SEMANTIC-SPACE.md             v1.x AAC-only (DEPRECATED)
    └── L³-VMM-SEMANTIC-SPACE.md             v1.x VMM-only (DEPRECATED)
```

---

## Code-to-Documentation Mapping

| Documentation | Code | Lines |
|--------------|------|:-----:|
| This index | `mi_beta/language/__init__.py` | 5 |
| L3Orchestrator | `mi_beta/language/groups/__init__.py` | 141 |
| Groups/Independent/Alpha.md | `mi_beta/language/groups/alpha.py` | 98 |
| Groups/Independent/Beta.md | `mi_beta/language/groups/beta.py` | 123 |
| Groups/Independent/Gamma.md | `mi_beta/language/groups/gamma.py` | 134 |
| Groups/Independent/Delta.md | `mi_beta/language/groups/delta.py` | 112 |
| Groups/Independent/Epsilon.md | `mi_beta/language/groups/epsilon.py` | 336 |
| Groups/Dependent/Zeta.md | `mi_beta/language/groups/zeta.py` | 145 |
| Groups/Dependent/Eta.md | `mi_beta/language/groups/eta.py` | 176 |
| Groups/Dependent/Theta.md | `mi_beta/language/groups/theta.py` | 155 |
| Contracts/BaseSemanticGroup.md | `mi_beta/contracts/base_semantic_group.py` | 169 |
| Contracts/BaseModelSemanticAdapter.md | `mi_beta/language/adapters/_base_adapter.py` | 14 |
| Adapters/{UNIT}-L3-ADAPTER.md (×9) | `mi_beta/language/adapters/{unit}_adapter.py` | ~12 each |

---

## Key Documents

| Document | Purpose |
|----------|---------|
| [L3-SEMANTIC-ARCHITECTURE.md](L3-SEMANTIC-ARCHITECTURE.md) | Definitive architecture, all 104 dimensions, formulas |
| [Registry/DimensionCatalog.md](Registry/DimensionCatalog.md) | Complete dimension inventory with metadata |
| [Registry/GroupMap.md](Registry/GroupMap.md) | Group index ranges and dependencies |
| [Epistemology/00-INDEX.md](Epistemology/00-INDEX.md) | 8-level epistemological framework |
| [Vocabulary/TermCatalog.md](Vocabulary/TermCatalog.md) | Complete 96-term vocabulary catalog |

## Cross-References

| Related Document | Location |
|-----------------|----------|
| C³ Brain architecture | [C³/C3-ARCHITECTURE.md](../C³/C3-ARCHITECTURE.md) |
| C³ output space | [C³/Matrices/Output-Space.md](../C³/Matrices/Output-Space.md) |
| R³ feature catalog | [R³/Registry/FeatureCatalog.md](../R³/Registry/FeatureCatalog.md) |
| H³ temporal architecture | [H³/00-INDEX.md](../H³/00-INDEX.md) |
| L³ code | `mi_beta/language/` (21 files) |
| L³ contract | `mi_beta/contracts/base_semantic_group.py` |
| L³ types | `mi_beta/core/types.py` (L3Output, SemanticGroupOutput) |
