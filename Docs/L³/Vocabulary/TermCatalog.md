# L³ Vocabulary — Term Catalog

**Scope**: Complete catalog of the 96 vocabulary terms (12 axes x 8 bands) used by the η (eta) group.
**Version**: 2.1.0
**Updated**: 2026-02-13
**Source of truth**: `mi_beta/language/groups/eta.py`, constant `AXIS_TERMS`

---

## Band-to-Gradation Mapping

Each axis spans 64 gradations (indices 0-63), divided into 8 bands of 8 gradations each:

| Band | Gradation Range | Polarity Region | Normalized Range |
|:----:|:---------------:|-----------------|:----------------:|
| 0 | 0-7 | Extreme negative | 0.000 - 0.111 |
| 1 | 8-15 | Strong negative | 0.127 - 0.238 |
| 2 | 16-23 | Moderate negative | 0.254 - 0.365 |
| 3 | 24-31 | Mild negative | 0.381 - 0.492 |
| 4 | 32-39 | Mild positive | 0.508 - 0.619 |
| 5 | 40-47 | Moderate positive | 0.635 - 0.746 |
| 6 | 48-55 | Strong positive | 0.762 - 0.873 |
| 7 | 56-63 | Extreme positive | 0.889 - 1.000 |

Bands 0-3 correspond to the ζ negative pole; bands 5-7 correspond to the ζ positive pole. Band 4 is the neutral crossover region.

---

## Per-Axis Term Tables

### Axis 0: Valence (sad <--> joyful)

| Band | Gradations | Term | Polarity Region |
|:----:|:----------:|------|-----------------|
| 0 | 0-7 | devastating | Extreme negative |
| 1 | 8-15 | melancholic | Strong negative |
| 2 | 16-23 | wistful | Moderate negative |
| 3 | 24-31 | subdued | Mild negative |
| 4 | 32-39 | neutral | Mild positive |
| 5 | 40-47 | content | Moderate positive |
| 6 | 48-55 | happy | Strong positive |
| 7 | 56-63 | euphoric | Extreme positive |

### Axis 1: Arousal (calm <--> excited)

| Band | Gradations | Term | Polarity Region |
|:----:|:----------:|------|-----------------|
| 0 | 0-7 | comatose | Extreme negative |
| 1 | 8-15 | lethargic | Strong negative |
| 2 | 16-23 | drowsy | Moderate negative |
| 3 | 24-31 | calm | Mild negative |
| 4 | 32-39 | neutral | Mild positive |
| 5 | 40-47 | alert | Moderate positive |
| 6 | 48-55 | energized | Strong positive |
| 7 | 56-63 | explosive | Extreme positive |

### Axis 2: Tension (relaxed <--> tense)

| Band | Gradations | Term | Polarity Region |
|:----:|:----------:|------|-----------------|
| 0 | 0-7 | dissolved | Extreme negative |
| 1 | 8-15 | slack | Strong negative |
| 2 | 16-23 | easy | Moderate negative |
| 3 | 24-31 | mild | Mild negative |
| 4 | 32-39 | neutral | Mild positive |
| 5 | 40-47 | taut | Moderate positive |
| 6 | 48-55 | strained | Strong positive |
| 7 | 56-63 | crushing | Extreme positive |

### Axis 3: Power (delicate <--> powerful)

| Band | Gradations | Term | Polarity Region |
|:----:|:----------:|------|-----------------|
| 0 | 0-7 | whisper | Extreme negative |
| 1 | 8-15 | fragile | Strong negative |
| 2 | 16-23 | gentle | Moderate negative |
| 3 | 24-31 | moderate | Mild negative |
| 4 | 32-39 | neutral | Mild positive |
| 5 | 40-47 | strong | Moderate positive |
| 6 | 48-55 | forceful | Strong positive |
| 7 | 56-63 | overwhelming | Extreme positive |

### Axis 4: Wanting (satiated <--> craving)

| Band | Gradations | Term | Polarity Region |
|:----:|:----------:|------|-----------------|
| 0 | 0-7 | fulfilled | Extreme negative |
| 1 | 8-15 | content | Strong negative |
| 2 | 16-23 | settled | Moderate negative |
| 3 | 24-31 | mild | Mild negative |
| 4 | 32-39 | neutral | Mild positive |
| 5 | 40-47 | interested | Moderate positive |
| 6 | 48-55 | eager | Strong positive |
| 7 | 56-63 | desperate | Extreme positive |

### Axis 5: Liking (displeasure <--> satisfaction)

| Band | Gradations | Term | Polarity Region |
|:----:|:----------:|------|-----------------|
| 0 | 0-7 | aversive | Extreme negative |
| 1 | 8-15 | unpleasant | Strong negative |
| 2 | 16-23 | bland | Moderate negative |
| 3 | 24-31 | indifferent | Mild negative |
| 4 | 32-39 | neutral | Mild positive |
| 5 | 40-47 | pleasant | Moderate positive |
| 6 | 48-55 | delightful | Strong positive |
| 7 | 56-63 | ecstatic | Extreme positive |

### Axis 6: Novelty (familiar <--> novel)

| Band | Gradations | Term | Polarity Region |
|:----:|:----------:|------|-----------------|
| 0 | 0-7 | habitual | Extreme negative |
| 1 | 8-15 | routine | Strong negative |
| 2 | 16-23 | known | Moderate negative |
| 3 | 24-31 | expected | Mild negative |
| 4 | 32-39 | neutral | Mild positive |
| 5 | 40-47 | fresh | Moderate positive |
| 6 | 48-55 | surprising | Strong positive |
| 7 | 56-63 | shocking | Extreme positive |

### Axis 7: Complexity (simple <--> complex)

| Band | Gradations | Term | Polarity Region |
|:----:|:----------:|------|-----------------|
| 0 | 0-7 | trivial | Extreme negative |
| 1 | 8-15 | basic | Strong negative |
| 2 | 16-23 | clear | Moderate negative |
| 3 | 24-31 | moderate | Mild negative |
| 4 | 32-39 | neutral | Mild positive |
| 5 | 40-47 | elaborate | Moderate positive |
| 6 | 48-55 | intricate | Strong positive |
| 7 | 56-63 | labyrinthine | Extreme positive |

### Axis 8: Beauty (discordant <--> harmonious)

| Band | Gradations | Term | Polarity Region |
|:----:|:----------:|------|-----------------|
| 0 | 0-7 | harsh | Extreme negative |
| 1 | 8-15 | grating | Strong negative |
| 2 | 16-23 | rough | Moderate negative |
| 3 | 24-31 | plain | Mild negative |
| 4 | 32-39 | neutral | Mild positive |
| 5 | 40-47 | pleasing | Moderate positive |
| 6 | 48-55 | beautiful | Strong positive |
| 7 | 56-63 | sublime | Extreme positive |

### Axis 9: Groove (rigid <--> flowing)

| Band | Gradations | Term | Polarity Region |
|:----:|:----------:|------|-----------------|
| 0 | 0-7 | mechanical | Extreme negative |
| 1 | 8-15 | stiff | Strong negative |
| 2 | 16-23 | stilted | Moderate negative |
| 3 | 24-31 | measured | Mild negative |
| 4 | 32-39 | neutral | Mild positive |
| 5 | 40-47 | swinging | Moderate positive |
| 6 | 48-55 | grooving | Strong positive |
| 7 | 56-63 | transcendent | Extreme positive |

### Axis 10: Stability (chaotic <--> stable)

| Band | Gradations | Term | Polarity Region |
|:----:|:----------:|------|-----------------|
| 0 | 0-7 | turbulent | Extreme negative |
| 1 | 8-15 | erratic | Strong negative |
| 2 | 16-23 | unsteady | Moderate negative |
| 3 | 24-31 | wavering | Mild negative |
| 4 | 32-39 | neutral | Mild positive |
| 5 | 40-47 | steady | Moderate positive |
| 6 | 48-55 | anchored | Strong positive |
| 7 | 56-63 | immovable | Extreme positive |

### Axis 11: Engagement (detached <--> absorbed)

| Band | Gradations | Term | Polarity Region |
|:----:|:----------:|------|-----------------|
| 0 | 0-7 | oblivious | Extreme negative |
| 1 | 8-15 | indifferent | Strong negative |
| 2 | 16-23 | distracted | Moderate negative |
| 3 | 24-31 | aware | Mild negative |
| 4 | 32-39 | neutral | Mild positive |
| 5 | 40-47 | attentive | Moderate positive |
| 6 | 48-55 | immersed | Strong positive |
| 7 | 56-63 | entranced | Extreme positive |

---

## Master Summary Table

All 96 terms at a glance (rows = axes, columns = bands):

| Axis | Band 0 | Band 1 | Band 2 | Band 3 | Band 4 | Band 5 | Band 6 | Band 7 |
|------|--------|--------|--------|--------|--------|--------|--------|--------|
| **valence** | devastating | melancholic | wistful | subdued | neutral | content | happy | euphoric |
| **arousal** | comatose | lethargic | drowsy | calm | neutral | alert | energized | explosive |
| **tension** | dissolved | slack | easy | mild | neutral | taut | strained | crushing |
| **power** | whisper | fragile | gentle | moderate | neutral | strong | forceful | overwhelming |
| **wanting** | fulfilled | content | settled | mild | neutral | interested | eager | desperate |
| **liking** | aversive | unpleasant | bland | indifferent | neutral | pleasant | delightful | ecstatic |
| **novelty** | habitual | routine | known | expected | neutral | fresh | surprising | shocking |
| **complexity** | trivial | basic | clear | moderate | neutral | elaborate | intricate | labyrinthine |
| **beauty** | harsh | grating | rough | plain | neutral | pleasing | beautiful | sublime |
| **groove** | mechanical | stiff | stilted | measured | neutral | swinging | grooving | transcendent |
| **stability** | turbulent | erratic | unsteady | wavering | neutral | steady | anchored | immovable |
| **engagement** | oblivious | indifferent | distracted | aware | neutral | attentive | immersed | entranced |

---

## Term Statistics

- **Total unique terms**: 96 (12 axes x 8 bands)
- **Shared terms across axes**: "neutral" appears in all 12 axes at band 4; "mild" appears in tension (band 3) and wanting (band 3); "moderate" appears in power (band 3) and complexity (band 3); "content" appears in valence (band 5) and wanting (band 1); "indifferent" appears in liking (band 3) and engagement (band 1)
- **Band 4 universality**: Every axis uses the term "neutral" for band 4, the crossover region between negative and positive polarity

---

## Code Verification

The terms above are extracted verbatim from `mi_beta/language/groups/eta.py`, constant `AXIS_TERMS` (lines 39-88). Zero drift is enforced: any discrepancy between this document and the code is a documentation bug to be fixed in the document.

---

**Parent**: [00-INDEX.md](00-INDEX.md)
**See also**: [GradationSystem.md](GradationSystem.md) for quantization design | [AxisDefinitions.md](AxisDefinitions.md) for axis source formulas | [Groups/Dependent/Eta.md](../Groups/Dependent/Eta.md) for η implementation
