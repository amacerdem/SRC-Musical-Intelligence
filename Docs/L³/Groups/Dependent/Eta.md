# L³ Groups — Eta (Vocabulary)

**Version**: 2.1.0
**Symbol**: η
**Level**: 7
**Dimensions**: 12 (fixed)
**Phase**: 2 (Dependent, Stateless)
**Output Range**: [0, 1]
**Dependencies**: zeta_output
**Code**: `mi_beta/language/groups/eta.py` (176 lines)
**Updated**: 2026-02-13

---

## Overview

Eta answers the question: **WHAT word describes this?**

Eta quantizes the 12 continuous zeta polarity axes [-1, +1] into 64 discrete gradation levels, then provides human-readable vocabulary terms via the `get_terms()` method. The tensor output is the **normalized gradation index** (continuous [0, 1]), while the vocabulary lookup maps each gradation to one of 96 semantic terms (12 axes x 8 bands).

**Audience**: Linguists, lay users, natural language generation, music description systems.

---

## 64-Gradation System

| Parameter | Value | Rationale |
|-----------|:-----:|-----------|
| `N_GRADATIONS` | 64 | 6 bits per axis; total 72 bits for 12 axes |
| `N_BANDS` | 8 | 8 intensity bands per axis |
| `GRADATIONS_PER_BAND` | 8 | 64 / 8 = 8 gradations per band |
| Step size | ~1.56% | Finer than human JND (~3%), per Weber 1834 / Stevens 1957 |

### Quantization Pipeline

```
zeta [-1,+1] → normalize to [0,1] → scale to [0,63] → round → clamp → gradation index
```

---

## Constants

### AXIS_NAMES (12 axes)

```python
AXIS_NAMES = (
    "valence", "arousal", "tension", "power",
    "wanting", "liking", "novelty", "complexity",
    "beauty", "groove", "stability", "engagement",
)
```

One-to-one correspondence with zeta's 12 polarity axes.

### AXIS_TERMS (12 x 8 = 96 terms)

Each axis has 8 band terms, from most negative (band 0) to most positive (band 7):

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

## Dimension Table

| Local Index | Name | Range | Formula | Source Axis |
|:-----------:|------|:-----:|---------|:-----------:|
| 0 | `valence_vocab` | [0,1] | `round((ζ[0]+1)/2 * 63) / 63` | ζ valence |
| 1 | `arousal_vocab` | [0,1] | `round((ζ[1]+1)/2 * 63) / 63` | ζ arousal |
| 2 | `tension_vocab` | [0,1] | `round((ζ[2]+1)/2 * 63) / 63` | ζ tension |
| 3 | `power_vocab` | [0,1] | `round((ζ[3]+1)/2 * 63) / 63` | ζ power |
| 4 | `wanting_vocab` | [0,1] | `round((ζ[4]+1)/2 * 63) / 63` | ζ wanting |
| 5 | `liking_vocab` | [0,1] | `round((ζ[5]+1)/2 * 63) / 63` | ζ liking |
| 6 | `novelty_vocab` | [0,1] | `round((ζ[6]+1)/2 * 63) / 63` | ζ novelty |
| 7 | `complexity_vocab` | [0,1] | `round((ζ[7]+1)/2 * 63) / 63` | ζ complexity |
| 8 | `beauty_vocab` | [0,1] | `round((ζ[8]+1)/2 * 63) / 63` | ζ beauty |
| 9 | `groove_vocab` | [0,1] | `round((ζ[9]+1)/2 * 63) / 63` | ζ groove |
| 10 | `stability_vocab` | [0,1] | `round((ζ[10]+1)/2 * 63) / 63` | ζ stability |
| 11 | `engagement_vocab` | [0,1] | `round((ζ[11]+1)/2 * 63) / 63` | ζ engagement |

---

## Formulas

### polarity_to_gradation

```python
def polarity_to_gradation(value: Tensor) -> Tensor:
    """Convert polarity [-1, +1] to gradation index [0, 63]."""
    normalized = (value + 1.0) * 0.5        # [-1,+1] -> [0,1]
    return (normalized * 63).round().long().clamp(0, 63)
```

### gradation_to_band

```python
def gradation_to_band(grad_idx: Tensor) -> Tensor:
    """Convert gradation index [0, 63] to band index [0, 7]."""
    return (grad_idx // 8).clamp(0, 7)
```

### Tensor Output (compute)

```python
# From zeta_output (B, T, 12) in [-1, +1]:
normalized = (zeta_output + 1.0) * 0.5                     # [0, 1]
quantized = (normalized * 63).round().clamp(0, 63) / 63    # quantized [0, 1]
tensor = quantized                                           # (B, T, 12)
```

The tensor output is the **normalized gradation index**: quantized to one of 64 levels, then divided by 63 to return to [0, 1]. This preserves differentiability while encoding the discrete step structure.

### Term Lookup (get_terms)

```python
def get_terms(self, zeta_output: Tensor) -> List[List[Dict[str, object]]]:
    grad_indices = polarity_to_gradation(zeta_output)  # [0, 63]
    band_indices = gradation_to_band(grad_indices)     # [0, 7]

    # For each axis, for each (batch, time) position:
    term = AXIS_TERMS[axis_name][band_index]
    # Returns: {"axis": name, "band_index": int, "term": str}
```

---

## Code Mapping

| Doc Concept | Code Variable | Location |
|-------------|---------------|----------|
| AXIS_NAMES | `AXIS_NAMES: Tuple[str, ...]` (12 entries) | eta.py:33-37 |
| AXIS_TERMS | `AXIS_TERMS: Dict[str, Tuple[str, ...]]` (12 keys, 8 terms each) | eta.py:39-88 |
| N_GRADATIONS | `N_GRADATIONS = 64` | eta.py:90 |
| N_BANDS | `N_BANDS = 8` | eta.py:91 |
| GRADATIONS_PER_BAND | `GRADATIONS_PER_BAND = 8` | eta.py:92 |
| polarity_to_gradation | `polarity_to_gradation(value)` | eta.py:95-98 |
| gradation_to_band | `gradation_to_band(grad_idx)` | eta.py:101-103 |
| Quantization | `(normalized * 63).round().clamp(0, 63) / 63` | eta.py:128-132 |
| Zeta fallback | `torch.full((B, T, 12), 0.5, ...)` when zeta_output is None | eta.py:134-139 |
| get_terms() | `get_terms(self, zeta_output)` | eta.py:148-175 |
| Dimension names | `[f"{name}_vocab" for name in AXIS_NAMES]` | eta.py:114 |
| OUTPUT_DIM | `OUTPUT_DIM = 12` (class constant) | eta.py:110 |

---

## Example

Given zeta output for a single frame:

```
valence = +0.7 (joyful direction)
arousal = -0.3 (calm direction)
tension = +0.1 (slightly tense)
```

Quantization:
```
valence: (0.7+1)/2 * 63 = 53.55 → round → 54 → band 54//8 = 6 → "happy"
arousal: (-0.3+1)/2 * 63 = 22.05 → round → 22 → band 22//8 = 2 → "drowsy"
tension: (0.1+1)/2 * 63 = 34.65 → round → 35 → band 35//8 = 4 → "neutral"
```

Tensor output: `[54/63, 22/63, 35/63, ...]` = `[0.857, 0.349, 0.556, ...]`

---

## Theoretical Basis

- **Prototype Theory** (Rosch 1975): Terms are prototypical labels for regions of the polarity space
- **Semantic Field Theory** (Trier 1931, Lyons 1977): Each axis's 8 terms form a coherent semantic field
- **JND Psychophysics** (Weber 1834, Stevens 1957): 64 gradations exceed human just-noticeable difference (~3%), ensuring no perceptible information loss

---

## Design Notes

- **64 levels = 6 bits**: Compact representation that exceeds perceptual resolution
- **96 total terms**: 12 axes x 8 bands, curated for musical experience description
- **Band 4 = neutral**: The middle band always has the term "neutral" across all axes
- **Symmetric structure**: Bands 0--3 are negative-pole terms, bands 4--7 are positive-pole terms
- **Tensor + terms**: Dual output format — tensor for computation, terms for human readability
- **Fallback**: When zeta_output is None, all dimensions default to 0.5 (gradation 32, band 4 = "neutral")

---

## Parent / See Also

- **Parent**: [Dependent/00-INDEX.md](00-INDEX.md)
- **Epistemology**: [Epistemology/Vocabulary.md](../../Epistemology/Vocabulary.md) — Level 7 theory
- **Registry**: [Registry/DimensionCatalog.md](../../Registry/DimensionCatalog.md) — global indices
- **Vocabulary**: [Vocabulary/TermCatalog.md](../../Vocabulary/TermCatalog.md) — complete 96-term catalog
- **Vocabulary**: [Vocabulary/GradationSystem.md](../../Vocabulary/GradationSystem.md) — 64-level design rationale
- **Vocabulary**: [Vocabulary/AxisDefinitions.md](../../Vocabulary/AxisDefinitions.md) — 12 axis definitions
- **Source**: [Dependent/Zeta.md](Zeta.md) — provides polarity input
- **Code**: `mi_beta/language/groups/eta.py`
