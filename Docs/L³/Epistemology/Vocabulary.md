# L³ Epistemology — Vocabulary

**Level**: 7 (η)
**Question**: WHAT word describes this?
**Audience**: Linguists, lay users, interface designers
**Version**: 2.1.0
**Updated**: 2026-02-13

---

## Overview

The Vocabulary group bridges the gap between continuous numerical signals and discrete human language. Where ζ provides bipolar direction (e.g., "calm vs excited"), η answers: at exactly what gradation along that axis are we, and what word best describes it?

Eta produces 12 dimensions, one per ζ axis, each quantized to 64 discrete levels.

---

## Theoretical Foundation

### Prototype Theory (Rosch 1975)

Rosch demonstrated that cognitive categories are not defined by necessary and sufficient conditions (the classical view) but by **prototypes** — central, best examples of a category. A robin is a more prototypical bird than a penguin. "Joyful" is a more prototypical example of high-valence emotion than "content."

η's vocabulary system applies prototype theory to musical semantics. Each of the 64 gradations per axis corresponds to a region of semantic space, and the label assigned to that region is the prototype for that gradation level. The listener does not need to understand the numerical value — they receive the word that best represents it.

### Semantic Field Theory (Trier 1931, Lyons 1977)

Trier proposed that words do not carry meaning in isolation but form **semantic fields** — interconnected networks where each word's meaning is partly defined by its neighbors. "Joyful," "happy," "content," and "serene" form a field along the positive valence axis. The boundaries between them are not sharp — they grade into each other.

η respects this by providing 64 gradations rather than a small number of coarse categories. The gradation system preserves the continuous nature of the underlying signal while mapping it to discrete labels drawn from coherent semantic fields.

### Psychophysics of Perception (Weber 1834, Stevens 1957)

Weber's Law states that the smallest detectable difference (Just Noticeable Difference, or JND) between two stimuli is proportional to the stimulus magnitude. Stevens (1957) generalized this to power law relationships between physical intensity and perceived magnitude.

For musical emotion perception, the JND is approximately **3%** of the scale range (Schubert 2004, based on continuous emotional rating studies). This sets a fundamental constraint on η's quantization: step sizes must be smaller than the JND to ensure that every adjacent pair of gradations represents a perceptually distinguishable difference.

---

## The 64-Gradation System

### Design Parameters

```
Gradations per axis:    64 (= 8 bands x 8 sub-gradations)
Step size:              1/64 = 1.5625%
JND threshold:          ~3%
Ratio (step/JND):       ~0.52 (well below 1.0)
Bits per axis:          6 (log2(64) = 6)
Total bits (12 axes):   72
```

### Why 64?

The number 64 is not arbitrary. It satisfies three constraints simultaneously:

1. **Below JND**: At 1/64 = 1.56%, the step size is roughly half the JND (~3%). This ensures that every gradation step is **perceptually meaningful** — no two adjacent levels are indistinguishable.

2. **Powers of 2**: 64 = 2^6, making the system naturally binary. Each axis requires exactly 6 bits, enabling efficient digital representation.

3. **8 x 8 structure**: 64 = 8 bands x 8 sub-gradations. The 8 bands provide coarse-grained categories (e.g., "very calm," "calm," "slightly calm," "neutral," "slightly excited," "excited," "very excited," "extremely excited"). The 8 sub-gradations provide fine-grained distinctions within each band.

### Quantization Formula

For each axis i:

```
η[i] = round((ζ[i] + 1) / 2 * 63) / 63
```

This maps ζ's [-1,+1] bipolar range to η's [0,1] quantized range in three steps:
1. Shift from [-1,+1] to [0,1]: `(ζ + 1) / 2`
2. Quantize to 64 levels: `round(... * 63)`
3. Normalize back to [0,1]: `/ 63`

---

## Natural Language Grounding

### From Numbers to Words

The quantization enables a lookup table: each of the 64 levels per axis maps to a specific term. With 12 axes, the complete vocabulary consists of 12 x 8 = 96 terms (at the band level) or 12 x 64 = 768 terms (at the sub-gradation level).

The band-level terms are defined in [Vocabulary/TermCatalog.md](../Vocabulary/TermCatalog.md). Examples:

| Axis | Band 1 (-1.0) | Band 4 (~0.0) | Band 8 (+1.0) |
|------|---------------|----------------|----------------|
| valence | despairing | neutral | ecstatic |
| arousal | catatonic | neutral | frenzied |
| tension | serene | balanced | agonizing |
| wanting | satiated | indifferent | desperate |

### Why This Matters

Continuous signals are powerful for computation but opaque to humans. A user does not want to see "ζ_valence = 0.73." They want to see "joyful." η provides this translation while preserving the quantitative precision needed for downstream processing (θ Narrative).

---

## The 12 Dimensions

| Local | Name | Range | Quantization | Corresponding ζ Axis |
|:-----:|------|:-----:|-------------|---------------------|
| η0 | `valence_vocab` | [0, 1] | round((ζ0+1)/2 * 63) / 63 | valence |
| η1 | `arousal_vocab` | [0, 1] | round((ζ1+1)/2 * 63) / 63 | arousal |
| η2 | `tension_vocab` | [0, 1] | round((ζ2+1)/2 * 63) / 63 | tension |
| η3 | `power_vocab` | [0, 1] | round((ζ3+1)/2 * 63) / 63 | power |
| η4 | `wanting_vocab` | [0, 1] | round((ζ4+1)/2 * 63) / 63 | wanting |
| η5 | `liking_vocab` | [0, 1] | round((ζ5+1)/2 * 63) / 63 | liking |
| η6 | `novelty_vocab` | [0, 1] | round((ζ6+1)/2 * 63) / 63 | novelty |
| η7 | `complexity_vocab` | [0, 1] | round((ζ7+1)/2 * 63) / 63 | complexity |
| η8 | `beauty_vocab` | [0, 1] | round((ζ8+1)/2 * 63) / 63 | beauty |
| η9 | `groove_vocab` | [0, 1] | round((ζ9+1)/2 * 63) / 63 | groove |
| η10 | `stability_vocab` | [0, 1] | round((ζ10+1)/2 * 63) / 63 | stability |
| η11 | `engagement_vocab` | [0, 1] | round((ζ11+1)/2 * 63) / 63 | engagement |

---

## Information Content

Each axis carries 6 bits of information (log2(64) = 6). Across all 12 axes, the total vocabulary state space is:

```
Total states = 64^12 = 2^72 ≈ 4.7 × 10^21
Total bits   = 72
```

This is more than sufficient to distinguish any musically relevant semantic configuration. For comparison, the English language has roughly 10^5 common words — η's 72-bit space is astronomically larger.

---

## Key Citations

- Rosch, E. (1975). Cognitive representations of semantic categories. *Journal of Experimental Psychology: General*, 104(3), 192-233.
- Trier, J. (1931). *Der deutsche Wortschatz im Sinnbezirk des Verstandes*. Heidelberg: Winter.
- Lyons, J. (1977). *Semantics*. Cambridge University Press.
- Weber, E.H. (1834). *De Pulsu, Resorptione, Auditu et Tactu*. Leipzig.
- Stevens, S.S. (1957). On the psychophysical law. *Psychological Review*, 64(3), 153-181.
- Schubert, E. (2004). Modeling perceived emotion with continuous musical features. *Music Perception*, 21(4), 561-585.

---

**Parent**: [00-INDEX.md](00-INDEX.md)
**See also**: [Groups/Dependent/Eta.md](../Groups/Dependent/Eta.md) for implementation details | [Registry/DimensionCatalog.md](../Registry/DimensionCatalog.md) for dimension metadata | [Vocabulary/GradationSystem.md](../Vocabulary/GradationSystem.md) for full gradation design | [Vocabulary/TermCatalog.md](../Vocabulary/TermCatalog.md) for the 96-term vocabulary
