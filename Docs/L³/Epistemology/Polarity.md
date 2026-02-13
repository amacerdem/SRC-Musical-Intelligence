# L³ Epistemology — Polarity

**Level**: 6 (ζ)
**Question**: WHICH direction?
**Audience**: Semanticists, psychometricians
**Version**: 2.1.0
**Updated**: 2026-02-13

---

## Overview

The Polarity group transforms unipolar [0,1] signals into bipolar [-1,+1] axes. This is not a trivial rescaling — it reflects a deep fact about how humans represent meaning. People do not think "arousal = 0.3." They think "calm rather than excited." Polarity provides the directional structure that makes semantic interpretation natural.

Zeta produces 12 bipolar dimensions grouped into Reward (6), Learning (3), and Aesthetic (3) axes.

---

## Theoretical Foundation

### Semantic Differential Theory (Osgood et al. 1957)

Osgood's semantic differential is one of the most replicated findings in psychology. When people rate the meaning of *any* concept — a word, an image, a sound — their ratings organize along bipolar scales. "Good-bad," "strong-weak," "active-passive." This is not a researcher-imposed structure; it emerges from factor analysis of thousands of ratings across cultures and languages.

Osgood identified three universal factors:
- **Evaluation** (E): good-bad, pleasant-unpleasant
- **Potency** (P): strong-weak, large-small
- **Activity** (A): active-passive, fast-slow

The **EPA framework** is the direct precursor to ζ's bipolar axes. L³ extends it from 3 generic factors to 12 music-specific axes, preserving the bipolar structure.

### Circumplex Model of Affect (Russell 1980)

Russell demonstrated that emotional experience can be mapped onto a circular space defined by two bipolar axes: **valence** (pleasant-unpleasant) and **arousal** (activated-deactivated). This circumplex model has been validated in music emotion research (Eerola & Vuoskoski 2011) and forms the core of ζ's emotion axes (ζ0, ζ1).

---

## The 12 Bipolar Axes

### Reward Axes (6)

| Local | Name | Neg Pole | Pos Pole | Source | Citation |
|:-----:|------|----------|----------|--------|----------|
| ζ0 | `valence` | sad | joyful | f03_valence | Russell 1980 |
| ζ1 | `arousal` | calm | excited | 2*arousal - 1 | Yang 2025 |
| ζ2 | `tension` | relaxed | tense | 2*tension - 1 | Huron 2006 |
| ζ3 | `power` | delicate | powerful | 2*ans_composite - 1 | Osgood 1957 |
| ζ4 | `wanting` | satiated | craving | 2*wanting - 1 | Berridge 2003 |
| ζ5 | `liking` | displeasure | satisfaction | 2*liking - 1 | Berridge 2003 |

### Learning Axes (3)

| Local | Name | Neg Pole | Pos Pole | Source | Citation |
|:-----:|------|----------|----------|--------|----------|
| ζ6 | `novelty` | familiar | novel | 2*ε[0] - 1 | Berlyne 1971 |
| ζ7 | `complexity` | simple | complex | 2*ε[1] - 1 | Berlyne 1971 |
| ζ10 | `stability` | chaotic | stable | 2*ε[6] - 1 | Friston 2010 |

### Aesthetic Axes (3)

| Local | Name | Neg Pole | Pos Pole | Source | Citation |
|:-----:|------|----------|----------|--------|----------|
| ζ8 | `beauty` | discordant | harmonious | 2*beauty - 1 | Blood & Zatorre 2001 |
| ζ9 | `groove` | rigid | flowing | 2*(harm_ctx*arousal) - 1 | Janata 2012 |
| ζ11 | `engagement` | detached | absorbed | 2*(pleasure*arousal) - 1 | Csikszentmihalyi 1990 |

---

## Transformation Design

### Unipolar to Bipolar

The transformation from [0,1] unipolar to [-1,+1] bipolar is:

```
ζ[i] = 2 * source[i] - 1
```

For sources already in [-1,+1] (e.g., f03_valence), no transformation is needed.

This maps:
- Source = 0.0 → ζ = -1.0 (negative pole)
- Source = 0.5 → ζ = 0.0 (neutral)
- Source = 1.0 → ζ = +1.0 (positive pole)

### Why Bipolar Matters

Three reasons:

1. **Cognitive naturalness**: Humans spontaneously organize experience in terms of opposites (Osgood 1957). "Calm vs excited" is more intuitive than "arousal = 0.3."

2. **Semantic completeness**: A unipolar scale cannot represent the *absence* of a quality as distinct from its opposite. Low arousal is not just "less excited" — it is "calm," a qualitatively different state. Bipolar encoding captures this.

3. **Downstream utility**: ζ feeds into η (Vocabulary) and θ (Narrative). Both require knowing not just the magnitude but the *direction* of a dimension to select appropriate words and sentence structures.

---

## Dependency: ζ reads ε

ζ is the first dependent group (Phase 2a). Six of its 12 axes derive from upstream groups:
- ζ0-ζ5 derive from γ (Psychology) and β (Neuroscience) signals
- ζ6, ζ7, ζ10 derive from ε (Learning) outputs: surprise, entropy, precision
- ζ8, ζ9, ζ11 derive from combinations of γ and ε signals

This dependency is why ζ cannot compute in Phase 1 — it needs ε's stateful learning dynamics to provide the novelty, complexity, and stability signals.

---

## Key Citations

- Osgood, C.E., Suci, G.J., & Tannenbaum, P.H. (1957). *The Measurement of Meaning*. University of Illinois Press.
- Russell, J.A. (1980). A circumplex model of affect. *JPSP*, 39(6), 1161-1178.
- Berridge, K.C. (2003). Pleasures of the brain. *Brain and Cognition*, 52(1), 106-128.
- Berlyne, D.E. (1971). *Aesthetics and Psychobiology*. Appleton-Century-Crofts.
- Friston, K. (2010). The free-energy principle. *Nature Reviews Neuroscience*, 11(2), 127-138.
- Huron, D. (2006). *Sweet Anticipation*. MIT Press.
- Blood, A.J. & Zatorre, R.J. (2001). Intensely pleasurable responses to music. *PNAS*, 98(20), 11818-11823.
- Janata, P. et al. (2012). Sensorimotor coupling in music and the psychology of the groove. *JEPHPP*, 38(1), 54-72.
- Csikszentmihalyi, M. (1990). *Flow: The Psychology of Optimal Experience*. Harper & Row.

---

**Parent**: [00-INDEX.md](00-INDEX.md)
**See also**: [Groups/Dependent/Zeta.md](../Groups/Dependent/Zeta.md) for implementation details | [Registry/DimensionCatalog.md](../Registry/DimensionCatalog.md) for dimension metadata | [Vocabulary/AxisDefinitions.md](../Vocabulary/AxisDefinitions.md) for axis pole terms
