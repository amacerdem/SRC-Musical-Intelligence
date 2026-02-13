# L³ Vocabulary — Axis Definitions

**Scope**: Detailed specification of the 12 polarity axes, their source formulas, subcategories, and vocabulary terms.
**Version**: 2.1.0
**Updated**: 2026-02-13
**Code**: `mi_beta/language/groups/zeta.py` (polarity), `mi_beta/language/groups/eta.py` (vocabulary)

---

## Overview

The 12 polarity axes originate in the ζ (zeta) group, which maps Brain and epsilon outputs to bipolar [-1, +1] signals. The η (eta) group then quantizes each axis into 64 gradations and assigns vocabulary terms. This document defines all 12 axes with their complete metadata.

The axes are organized into three subcategories:
- **Reward Axes** (6): Core affective and motivational dimensions
- **Learning Axes** (3): Information-theoretic dimensions from epsilon
- **Aesthetic Axes** (3): Higher-order aesthetic experience dimensions

---

## Reward Axes (6 axes, indices 0-5)

Derived from Brain [0,1] signals via the `2x - 1` transform.

### Axis 0: Valence

| Property | Value |
|----------|-------|
| **ζ index** | 0 |
| **η index** | 0 |
| **Name** | valence |
| **Negative pole** | sad |
| **Positive pole** | joyful |
| **Source formula** | `2 * Brain.valence - 1` |
| **Subcategory** | Reward |
| **Primary citation** | Russell 1980 (Circumplex Model of Affect) |
| **Band terms** | devastating, melancholic, wistful, subdued, neutral, content, happy, euphoric |

### Axis 1: Arousal

| Property | Value |
|----------|-------|
| **ζ index** | 1 |
| **η index** | 1 |
| **Name** | arousal |
| **Negative pole** | calm |
| **Positive pole** | excited |
| **Source formula** | `2 * Brain.arousal - 1` |
| **Subcategory** | Reward |
| **Primary citation** | Yang 2025 |
| **Band terms** | comatose, lethargic, drowsy, calm, neutral, alert, energized, explosive |

### Axis 2: Tension

| Property | Value |
|----------|-------|
| **ζ index** | 2 |
| **η index** | 2 |
| **Name** | tension |
| **Negative pole** | relaxed |
| **Positive pole** | tense |
| **Source formula** | `2 * Brain.tension - 1` |
| **Subcategory** | Reward |
| **Primary citation** | Huron 2006 (ITPRA) |
| **Band terms** | dissolved, slack, easy, mild, neutral, taut, strained, crushing |

### Axis 3: Power

| Property | Value |
|----------|-------|
| **ζ index** | 3 |
| **η index** | 3 |
| **Name** | power |
| **Negative pole** | delicate |
| **Positive pole** | powerful |
| **Source formula** | `2 * Brain.arousal - 1` (proxy) |
| **Subcategory** | Reward |
| **Primary citation** | Osgood 1957 (Semantic Differential Theory) |
| **Band terms** | whisper, fragile, gentle, moderate, neutral, strong, forceful, overwhelming |

**Note**: Power currently uses arousal as a proxy when `ans_composite` is unavailable.

### Axis 4: Wanting

| Property | Value |
|----------|-------|
| **ζ index** | 4 |
| **η index** | 4 |
| **Name** | wanting |
| **Negative pole** | satiated |
| **Positive pole** | craving |
| **Source formula** | `2 * Brain.wanting - 1` |
| **Subcategory** | Reward |
| **Primary citation** | Berridge 2003 (Incentive Salience) |
| **Band terms** | fulfilled, content, settled, mild, neutral, interested, eager, desperate |

### Axis 5: Liking

| Property | Value |
|----------|-------|
| **ζ index** | 5 |
| **η index** | 5 |
| **Name** | liking |
| **Negative pole** | displeasure |
| **Positive pole** | satisfaction |
| **Source formula** | `2 * Brain.liking - 1` |
| **Subcategory** | Reward |
| **Primary citation** | Berridge 2003 (Hedonic Pleasure) |
| **Band terms** | aversive, unpleasant, bland, indifferent, neutral, pleasant, delightful, ecstatic |

---

## Learning Axes (3 axes, indices 6-7 and 10)

Derived from epsilon (ε) output signals via the `2x - 1` transform. When `epsilon_output` is None, these axes default to 0 (neutral polarity).

### Axis 6: Novelty

| Property | Value |
|----------|-------|
| **ζ index** | 6 |
| **η index** | 6 |
| **Name** | novelty |
| **Negative pole** | familiar |
| **Positive pole** | novel |
| **Source formula** | `2 * ε.surprise - 1` (epsilon[0]) |
| **Subcategory** | Learning |
| **Primary citation** | Berlyne 1971 (Aesthetics and Psychobiology) |
| **Band terms** | habitual, routine, known, expected, neutral, fresh, surprising, shocking |

### Axis 7: Complexity

| Property | Value |
|----------|-------|
| **ζ index** | 7 |
| **η index** | 7 |
| **Name** | complexity |
| **Negative pole** | simple |
| **Positive pole** | complex |
| **Source formula** | `2 * ε.entropy - 1` (epsilon[1]) |
| **Subcategory** | Learning |
| **Primary citation** | Berlyne 1971 (Aesthetics and Psychobiology) |
| **Band terms** | trivial, basic, clear, moderate, neutral, elaborate, intricate, labyrinthine |

### Axis 10: Stability

| Property | Value |
|----------|-------|
| **ζ index** | 10 |
| **η index** | 10 |
| **Name** | stability |
| **Negative pole** | chaotic |
| **Positive pole** | stable |
| **Source formula** | `2 * ε.precision_long - 1` (epsilon[6]) |
| **Subcategory** | Learning |
| **Primary citation** | Friston 2010 (Free Energy Principle) |
| **Band terms** | turbulent, erratic, unsteady, wavering, neutral, steady, anchored, immovable |

---

## Aesthetic Axes (3 axes, indices 8-9 and 11)

Derived from Brain signals, some via multiplicative interaction terms.

### Axis 8: Beauty

| Property | Value |
|----------|-------|
| **ζ index** | 8 |
| **η index** | 8 |
| **Name** | beauty |
| **Negative pole** | discordant |
| **Positive pole** | harmonious |
| **Source formula** | `2 * Brain.beauty - 1` |
| **Subcategory** | Aesthetic |
| **Primary citation** | Blood & Zatorre 2001 |
| **Band terms** | harsh, grating, rough, plain, neutral, pleasing, beautiful, sublime |

### Axis 9: Groove

| Property | Value |
|----------|-------|
| **ζ index** | 9 |
| **η index** | 9 |
| **Name** | groove |
| **Negative pole** | rigid |
| **Positive pole** | flowing |
| **Source formula** | `2 * (Brain.arousal * Brain.harmonic_context) - 1` |
| **Subcategory** | Aesthetic |
| **Primary citation** | Janata 2012 |
| **Band terms** | mechanical, stiff, stilted, measured, neutral, swinging, grooving, transcendent |

**Note**: Groove is a multiplicative interaction between arousal and harmonic context, capturing the sense of rhythmic flow that emerges when energy and harmonic structure align.

### Axis 11: Engagement

| Property | Value |
|----------|-------|
| **ζ index** | 11 |
| **η index** | 11 |
| **Name** | engagement |
| **Negative pole** | detached |
| **Positive pole** | absorbed |
| **Source formula** | `2 * (Brain.pleasure * Brain.arousal) - 1` |
| **Subcategory** | Aesthetic |
| **Primary citation** | Csikszentmihalyi 1990 (Flow) |
| **Band terms** | oblivious, indifferent, distracted, aware, neutral, attentive, immersed, entranced |

**Note**: Engagement is a multiplicative interaction between pleasure and arousal, capturing the flow-like absorption that occurs when hedonic reward and activation coincide.

---

## Summary Table

| Idx | Axis | Neg Pole | Pos Pole | Source | Subcategory | Citation |
|:---:|------|:--------:|:--------:|--------|:-----------:|----------|
| 0 | valence | sad | joyful | Brain.valence | Reward | Russell 1980 |
| 1 | arousal | calm | excited | Brain.arousal | Reward | Yang 2025 |
| 2 | tension | relaxed | tense | Brain.tension | Reward | Huron 2006 |
| 3 | power | delicate | powerful | Brain.arousal (proxy) | Reward | Osgood 1957 |
| 4 | wanting | satiated | craving | Brain.wanting | Reward | Berridge 2003 |
| 5 | liking | displeasure | satisfaction | Brain.liking | Reward | Berridge 2003 |
| 6 | novelty | familiar | novel | ε.surprise | Learning | Berlyne 1971 |
| 7 | complexity | simple | complex | ε.entropy | Learning | Berlyne 1971 |
| 8 | beauty | discordant | harmonious | Brain.beauty | Aesthetic | Blood & Zatorre 2001 |
| 9 | groove | rigid | flowing | Brain.arousal * harmonic_context | Aesthetic | Janata 2012 |
| 10 | stability | chaotic | stable | ε.precision_long | Learning | Friston 2010 |
| 11 | engagement | detached | absorbed | Brain.pleasure * arousal | Aesthetic | Csikszentmihalyi 1990 |

---

## Tensor Ordering Note

The output tensor concatenation order in zeta.py interleaves learning and aesthetic axes:

```python
tensor = cat([
    valence, arousal, tension, power, wanting, liking,  # Reward (idx 0-5)
    novelty, complexity,                                 # Learning (idx 6-7)
    beauty, groove,                                      # Aesthetic (idx 8-9)
    stability,                                           # Learning (idx 10)
    engagement,                                          # Aesthetic (idx 11)
], dim=-1)
```

This means stability (Learning) is at index 10 between groove (Aesthetic, index 9) and engagement (Aesthetic, index 11), rather than being grouped contiguously with novelty and complexity. The ordering matches the `POLARITY_AXES` constant and is preserved through to η.

---

## Index Cross-Reference

| η Local Index | ζ Index | Axis Name | η Dimension Name | Global L³ Index |
|:-------------:|:-------:|-----------|:----------------:|:---------------:|
| 0 | 0 | valence | `valence_vocab` | 76 |
| 1 | 1 | arousal | `arousal_vocab` | 77 |
| 2 | 2 | tension | `tension_vocab` | 78 |
| 3 | 3 | power | `power_vocab` | 79 |
| 4 | 4 | wanting | `wanting_vocab` | 80 |
| 5 | 5 | liking | `liking_vocab` | 81 |
| 6 | 6 | novelty | `novelty_vocab` | 82 |
| 7 | 7 | complexity | `complexity_vocab` | 83 |
| 8 | 8 | beauty | `beauty_vocab` | 84 |
| 9 | 9 | groove | `groove_vocab` | 85 |
| 10 | 10 | stability | `stability_vocab` | 86 |
| 11 | 11 | engagement | `engagement_vocab` | 87 |

Global L³ indices 76-87 correspond to the η group (see [Registry/DimensionCatalog.md](../Registry/DimensionCatalog.md)).

---

**Parent**: [00-INDEX.md](00-INDEX.md)
**See also**: [TermCatalog.md](TermCatalog.md) for the complete 96-term vocabulary | [GradationSystem.md](GradationSystem.md) for quantization design | [Groups/Dependent/Zeta.md](../Groups/Dependent/Zeta.md) for ζ polarity source | [Groups/Dependent/Eta.md](../Groups/Dependent/Eta.md) for η implementation
