# L³ Epistemology — Framework Index

**Version**: 2.1.0
**Updated**: 2026-02-13
**Scope**: Overview of the 8-level epistemological framework that structures L³'s 104 semantic dimensions.

---

## Purpose

The L³ semantic layer transforms the Brain's numerical output into **interpretable meaning**. But "meaning" is not monolithic — different audiences ask different questions about the same signal. A neuroscientist asks WHERE a response originates. A psychologist asks WHAT it feels like. An engineer asks HOW it was computed.

The 8-level epistemological framework organizes L³'s 104 dimensions into groups that each answer a fundamentally different question. This is not arbitrary taxonomy — it reflects how knowledge about musical experience is actually structured across scientific disciplines.

---

## The 8 Levels

| Level | Symbol | Group | Question | Audience | Dim | Key Theory | Key Citation |
|:-----:|:------:|-------|----------|----------|:---:|------------|-------------|
| 1 | α | Computation | HOW was this computed? | Engineers | 6 | Bayesian precision, attribution | Friston 2010 |
| 2 | β | Neuroscience | WHERE in the brain? | Neuroscientists | 14 | Mesolimbic pathway, RPE | Salimpoor 2011 |
| 3 | γ | Psychology | WHAT does it mean subjectively? | Psychologists | 13 | ITPRA, circumplex affect | Huron 2006 |
| 4 | δ | Validation | HOW to test empirically? | Experimenters | 12 | Physiological prediction | de Fleurian & Pearce 2021 |
| 5 | ε | Learning | HOW does the listener learn? | Info theorists | 19 | Free energy, statistical learning | Friston 2010, Pearce 2005 |
| 6 | ζ | Polarity | WHICH direction? | Semanticists | 12 | Semantic differential | Osgood 1957 |
| 7 | η | Vocabulary | WHAT word describes this? | Linguists | 12 | Prototype theory, JND | Rosch 1975, Weber 1834 |
| 8 | θ | Narrative | HOW to describe in language? | Narrative researchers | 16 | Musical narrative, cohesion | Almen 2008 |
| | | **Total** | | | **104** | | |

---

## Why 8 Levels?

The 8-level structure is not a convenience — it reflects fundamental epistemological distinctions:

1. **Computation (α)** grounds everything in traceable mathematics. Without attribution, the system is a black box.
2. **Neuroscience (β)** maps computation to biological substrate. The brain is the reference frame for musical reward.
3. **Psychology (γ)** translates neural activity into subjective experience. This is where reward becomes feeling.
4. **Validation (δ)** ensures scientific accountability. Every claim must be testable.
5. **Learning (ε)** adds temporal dynamics. Music is a process, not a snapshot — listeners learn over time.
6. **Polarity (ζ)** gives direction. Unipolar [0,1] signals become meaningful bipolar [-1,+1] axes.
7. **Vocabulary (η)** bridges continuous signals to discrete human language.
8. **Narrative (θ)** assembles words into sentences — the final step from number to description.

Each level depends on the previous levels in a principled way. Levels 1-4 are **independent** (read only Brain output). Level 5 is **stateful** (accumulates over time). Levels 6-8 are **dependent** (cascade through the chain).

---

## Design Rationale

### Separation of concerns
Each group answers exactly one epistemological question. No dimension serves two masters.

### Dependency ordering
Phase 1 groups (α-δ) can compute in parallel. Phase 1b (ε) must maintain state. Phase 2 groups (ζ-η-θ) cascade in strict order. This is not a design choice — it is entailed by what each level computes.

### Audience targeting
Each level is designed for a specific scientific community. A psychologist can read γ without understanding the neural details in β. An engineer can audit α without knowing the psychological literature.

### Falsifiability
Level δ exists solely to generate testable predictions. This makes L³ a scientific framework, not just an engineering convenience.

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

## Per-Level Documents

| Document | Level | Lines |
|----------|:-----:|:-----:|
| [Computation.md](Computation.md) | α (1) | ~100 |
| [Neuroscience.md](Neuroscience.md) | β (2) | ~150 |
| [Psychology.md](Psychology.md) | γ (3) | ~130 |
| [Validation.md](Validation.md) | δ (4) | ~120 |
| [Learning.md](Learning.md) | ε (5) | ~200 |
| [Polarity.md](Polarity.md) | ζ (6) | ~120 |
| [Vocabulary.md](Vocabulary.md) | η (7) | ~150 |
| [Narrative.md](Narrative.md) | θ (8) | ~150 |

---

## Cross-References

| Related Document | Location |
|-----------------|----------|
| Dimension Catalog (all 104D) | [Registry/DimensionCatalog.md](../Registry/DimensionCatalog.md) |
| Group Map (index ranges) | [Registry/GroupMap.md](../Registry/GroupMap.md) |
| Groups — Independent (α-ε) | [Groups/Independent/](../Groups/Independent/) |
| Groups — Dependent (ζ-θ) | [Groups/Dependent/](../Groups/Dependent/) |
| L³ Master Index | [00-INDEX.md](../00-INDEX.md) |
| L³ Changelog | [CHANGELOG.md](../CHANGELOG.md) |

---

**Parent**: [L³ 00-INDEX.md](../00-INDEX.md)
**See also**: [Registry/GroupMap.md](../Registry/GroupMap.md) for execution-level group details
