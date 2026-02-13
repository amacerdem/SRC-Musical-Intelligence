# L³ Epistemology — Narrative

**Level**: 8 (θ)
**Question**: HOW to describe in language?
**Audience**: Narrative researchers, music analysts, interface designers
**Version**: 2.1.0
**Updated**: 2026-02-13

---

## Overview

The Narrative group is the final epistemological level — where numbers become sentences. θ assembles the semantic information from all upstream groups into a structured description of what is happening in the music at each frame. This is the output a human reader or downstream NLG system would consume.

Theta produces 16 dimensions organized as a **4-slot sentence structure**: Subject (4), Predicate (4), Modifier (4), and Connector (4).

---

## Theoretical Foundation

### Musical Narrative Theory (Almen 2008)

Almen argued that music, like literature, exhibits narrative structure — it has agents (themes, motifs), conflicts (tension, dissonance), and resolutions (cadences, returns). The key insight is that musical narrative is not metaphorical but structural: music genuinely organizes temporal experience into narrative patterns.

θ operationalizes this by treating each frame as a sentence in an ongoing narrative. The Subject identifies *who* is acting (which musical dimension dominates). The Predicate describes *what* is happening (rising, peaking, falling, stable). The Modifier qualifies *how* (intensity, certainty, novelty, speed). The Connector links this sentence to the previous one (continuing, contrasting, resolving, transitioning).

### Cohesion Theory (Halliday & Hasan 1976)

Halliday and Hasan's theory of textual cohesion describes how sentences link together into coherent discourse. They identified four primary cohesion mechanisms:
- **Conjunction**: additive ("and"), adversative ("but"), causal ("so"), temporal ("then")
- **Reference**: anaphoric ties to previous sentences
- **Substitution**: replacing elements with pro-forms
- **Lexical cohesion**: repetition and semantic field continuity

θ's Connector slot (θ12-θ15) implements a simplified version of conjunction: each frame's description is linked to the previous frame's description via one of four discourse relations (continuing, contrasting, resolving, transitioning).

### Classical Form (Caplin 1998)

Caplin's theory of classical form provides phrase-structural categories (presentation, continuation, cadential, standing on the dominant) that describe how musical phrases are constructed. θ's Predicate slot draws on this — "rising" corresponds to presentation/continuation, "peaking" to climax, "falling" to cadential function, and "stable" to prolongation.

---

## The 4-Slot Sentence Structure

### Slot 1: Subject (4D) — WHO is acting?

| Local | Name | Description | Source | Citation |
|:-----:|------|-------------|--------|----------|
| θ0 | `reward_salience` | Reward dominates the frame | γ reward dims | Salimpoor 2011 |
| θ1 | `tension_salience` | Tension dominates the frame | γ ITPRA dims | Huron 2006 |
| θ2 | `motion_salience` | Motion/arousal dominates | γ emotion dims | Yang 2025 |
| θ3 | `beauty_salience` | Beauty/aesthetics dominates | γ aesthetic dims | Blood & Zatorre 2001 |

**Selection mechanism**: Softmax competition with temperature = 3.0.

The four subject dimensions compete via softmax to determine which aspect of the musical experience is most salient at the current frame. Temperature = 3.0 produces a "soft" winner — typically one subject dominates but others retain non-zero activation. This reflects the phenomenological reality that musical moments are usually *about* one thing primarily (reward, tension, motion, or beauty) while other aspects contribute secondarily.

The softmax temperature was chosen to avoid winner-take-all (temperature → 0) while still producing interpretable dominance (temperature → infinity would make all subjects equal).

### Slot 2: Predicate (4D) — WHAT is happening?

| Local | Name | Description | Source | Citation |
|:-----:|------|-------------|--------|----------|
| θ4 | `rising` | Increasing trajectory | ε temporal dynamics (positive derivative) | Schubert 2004 |
| θ5 | `peaking` | At climax/apex | ε temporal dynamics (zero crossing after rise) | Sloboda 1991 |
| θ6 | `falling` | Decreasing trajectory | ε temporal dynamics (negative derivative) | Schubert 2004 |
| θ7 | `stable` | Holding steady | ε temporal dynamics (near-zero derivative) | Meyer 1956 |

The Predicate classifies the temporal dynamics of the dominant subject. It derives from ε's learning dynamics — specifically, the direction and rate of change of the relevant signals. A rising reward signal produces "rising." A tension signal at its peak produces "peaking." A beauty signal declining after a climax produces "falling."

This maps naturally to Caplin's (1998) phrase functions: presentation (rising), climax (peaking), cadential (falling), and prolongation (stable).

### Slot 3: Modifier (4D) — HOW is it happening?

| Local | Name | Description | Source | Citation |
|:-----:|------|-------------|--------|----------|
| θ8 | `intensity` | How strongly | Overall activation magnitude | Gabrielsson 2001 |
| θ9 | `certainty` | How confidently | ε precision (α4, ε5-6) | Friston 2010 |
| θ10 | `novelty` | How surprisingly | ε surprise (ε0) | Berlyne 1971 |
| θ11 | `speed` | How quickly | Rate of change magnitude | Fong 2020 |

Modifiers qualify the predicate. A "rising reward" can be intense or subtle, certain or tentative, novel or familiar, fast or slow. These four modifier dimensions provide the adverbial richness that distinguishes "gently building anticipation" from "explosively surging desire."

### Slot 4: Connector (4D) — HOW does this relate to what came before?

| Local | Name | Description | Discourse Relation | Citation |
|:-----:|------|-------------|-------------------|----------|
| θ12 | `continuing` | Same thread continues | Additive conjunction | Halliday & Hasan 1976 |
| θ13 | `contrasting` | Opposition to previous | Adversative conjunction | Almen 2008 |
| θ14 | `resolving` | Previous tension resolves | Causal conjunction | Huron 2006 |
| θ15 | `transitioning` | New section begins | Temporal conjunction | Caplin 1998 |

The Connector links the current frame's sentence to the previous frame's narrative. It derives from ζ's polarity signals — specifically, the change in polarity between consecutive frames:
- **Continuing** (θ12): polarity is stable — the narrative thread persists
- **Contrasting** (θ13): polarity reverses — the music does the opposite of what it was doing
- **Resolving** (θ14): tension drops — a dissonance or suspense resolves
- **Transitioning** (θ15): a new section begins — the narrative shifts to a new topic

---

## Narrative Assembly

A complete narrative frame combines all four slots into a structured description:

```
[Subject] + [Predicate] + [Modifier] + [Connector]
```

Example interpretations:

| Subject | Predicate | Modifier | Connector | Natural Language |
|---------|-----------|----------|-----------|-----------------|
| reward (0.8) | rising (0.7) | intense (0.9), certain (0.6) | continuing (0.8) | "Reward continues to rise intensely and confidently" |
| tension (0.9) | peaking (0.8) | novel (0.7), fast (0.6) | contrasting (0.7) | "But tension peaks suddenly and unexpectedly" |
| beauty (0.7) | falling (0.5) | subtle (0.3), slow (0.2) | resolving (0.9) | "As a result, beauty gently subsides" |

The actual NLG generation from these 16 dimensions is downstream of L³ — θ provides the structured semantic representation that a template-based or neural language generation system would consume.

---

## Dependencies

θ is the most dependent group (Phase 2c), reading from:
- **ε** (Learning): temporal dynamics for Predicate, surprise for Modifier novelty
- **ζ** (Polarity): direction changes for Connector derivation
- **γ** (Psychology, via θ's internal routing): reward/tension/motion/beauty for Subject

This makes θ the "culmination" of the L³ pipeline — it can only be computed after all upstream groups have produced their output.

---

## Key Citations

- Almen, B. (2008). *A Theory of Musical Narrative*. Indiana University Press.
- Halliday, M.A.K. & Hasan, R. (1976). *Cohesion in English*. Longman.
- Caplin, W.E. (1998). *Classical Form: A Theory of Formal Functions for the Instrumental Music of Haydn, Mozart, and Beethoven*. Oxford University Press.
- Schubert, E. (2004). Modeling perceived emotion with continuous musical features. *Music Perception*, 21(4), 561-585.
- Meyer, L.B. (1956). *Emotion and Meaning in Music*. University of Chicago Press.
- Gabrielsson, A. (2001). Emotions in strong experiences with music. In P.N. Juslin & J.A. Sloboda (Eds.), *Music and Emotion* (pp. 431-449). Oxford University Press.
- Sloboda, J.A. (1991). Music structure and emotional response. *Psychology of Music*, 19, 110-120.
- Friston, K. (2010). The free-energy principle. *Nature Reviews Neuroscience*, 11(2), 127-138.
- Berlyne, D.E. (1971). *Aesthetics and Psychobiology*. Appleton-Century-Crofts.

---

**Parent**: [00-INDEX.md](00-INDEX.md)
**See also**: [Groups/Dependent/Theta.md](../Groups/Dependent/Theta.md) for implementation details | [Registry/DimensionCatalog.md](../Registry/DimensionCatalog.md) for dimension metadata | [Vocabulary/TermCatalog.md](../Vocabulary/TermCatalog.md) for the vocabulary terms used in narrative generation
