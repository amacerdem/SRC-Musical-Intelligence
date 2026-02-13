# L³ Vocabulary — Gradation System

**Scope**: Design rationale and quantization mechanics for the 64-level gradation system.
**Version**: 2.1.0
**Updated**: 2026-02-13
**Code**: `mi_beta/language/groups/eta.py`

---

## Overview

The η (eta) group quantizes each of the 12 ζ (zeta) polarity axes from continuous [-1, +1] bipolar signals into 64 discrete gradation levels. This document explains why 64 gradations were chosen, how the quantization works, and the scientific basis for the design.

---

## Why 64 Gradations?

The number 64 satisfies three constraints simultaneously:

### 1. Below the Just Noticeable Difference (JND)

**Weber's Law** (Weber 1834) states that the smallest detectable difference between two stimuli is proportional to the stimulus magnitude. **Stevens' Power Law** (Stevens 1957) generalizes this to power-law relationships between physical intensity and perceived magnitude.

For musical emotion perception, continuous emotional rating studies (Schubert 2004) place the JND at approximately **3%** of the scale range. The 64-gradation system produces a step size of:

```
Step size = 1 / 64 = 1.5625%
Ratio    = step / JND = 1.5625% / 3.0% ≈ 0.52
```

At roughly half the JND, every adjacent pair of gradations represents a perceptually distinguishable difference. No perceptible information is lost during quantization.

### 2. Powers of Two (Bit Budget)

64 = 2^6, so each axis requires exactly **6 bits** of storage:

```
Bits per axis:    log2(64) = 6
Total bits:       6 x 12 axes = 72
Total states:     64^12 = 2^72 ≈ 4.7 x 10^21
```

72 bits provides an astronomically large state space -- far exceeding what is needed to distinguish any musically relevant semantic configuration.

### 3. 8 x 8 Band Structure

64 = 8 bands x 8 gradations per band. This two-level structure enables both coarse-grained and fine-grained description:

- **Bands** (8 per axis): Map to human-readable vocabulary terms. Band 0 = extreme negative, band 7 = extreme positive. Band 4 = neutral crossover.
- **Gradations within bands** (8 per band): Provide fine-grained distinctions within each term's semantic region. A listener described as "happy" (band 6) can be at gradation 48 (just barely happy) or gradation 55 (strongly happy).

---

## Quantization Pipeline

The full quantization chain from ζ polarity to η output:

```
ζ polarity [-1, +1]
    │
    ▼
normalized = (polarity + 1.0) * 0.5          # [-1,+1] → [0,1]
    │
    ▼
gradation = round(normalized * 63)             # [0,1] → {0..63}
    │
    ▼
band = gradation // 8                          # {0..63} → {0..7}
    │
    ▼
output = gradation / 63                        # {0..63} → [0,1]
```

### Step-by-Step Example

Given ζ valence = +0.7 (joyful direction):

```
normalized = (0.7 + 1.0) * 0.5 = 0.85
gradation  = round(0.85 * 63) = round(53.55) = 54
band       = 54 // 8 = 6                       → term: "happy"
output     = 54 / 63 = 0.857                   → tensor value
```

---

## Code Implementation

### Constants

```python
N_GRADATIONS: int = 64
N_BANDS: int = 8
GRADATIONS_PER_BAND: int = N_GRADATIONS // N_BANDS  # 8
```

### polarity_to_gradation()

Converts polarity values to integer gradation indices:

```python
def polarity_to_gradation(value: Tensor) -> Tensor:
    """Convert polarity [-1, +1] to gradation index [0, 63]."""
    normalized = (value + 1.0) * 0.5
    return (normalized * (N_GRADATIONS - 1)).round().long().clamp(0, N_GRADATIONS - 1)
```

### gradation_to_band()

Converts gradation indices to band indices:

```python
def gradation_to_band(grad_idx: Tensor) -> Tensor:
    """Convert gradation index [0, 63] to band index [0, 7]."""
    return (grad_idx // GRADATIONS_PER_BAND).clamp(0, N_BANDS - 1)
```

### get_terms()

Combines both functions to produce human-readable term lookups:

```python
def get_terms(self, zeta_output: Tensor) -> List[List[Dict[str, object]]]:
    grad_indices = polarity_to_gradation(zeta_output)  # [0, 63]
    band_indices = gradation_to_band(grad_indices)      # [0, 7]
    # For each axis and (batch, time) position:
    term = AXIS_TERMS[axis_name][band_index]
    # Returns: {"axis": name, "band_index": int, "term": str}
```

### Tensor Output (compute)

The `EtaGroup.compute()` method outputs the normalized gradation index as a continuous [0, 1] tensor:

```python
normalized = (zeta_output + 1.0) * 0.5                     # [0, 1]
quantized = (normalized * 63).round().clamp(0, 63) / 63    # quantized [0, 1]
tensor = quantized                                           # (B, T, 12)
```

When `zeta_output` is None, all dimensions default to 0.5 (gradation 32, band 4 = "neutral").

---

## Band Structure Detail

| Band | Gradation Range | Polarity Range | Semantic Region | Example (valence) |
|:----:|:---------------:|:--------------:|-----------------|-------------------|
| 0 | 0-7 | -1.000 to -0.778 | Extreme negative | devastating |
| 1 | 8-15 | -0.746 to -0.524 | Strong negative | melancholic |
| 2 | 16-23 | -0.492 to -0.270 | Moderate negative | wistful |
| 3 | 24-31 | -0.238 to -0.016 | Mild negative | subdued |
| 4 | 32-39 | +0.016 to +0.238 | Mild positive | neutral |
| 5 | 40-47 | +0.270 to +0.492 | Moderate positive | content |
| 6 | 48-55 | +0.524 to +0.746 | Strong positive | happy |
| 7 | 56-63 | +0.778 to +1.000 | Extreme positive | euphoric |

The polarity range values are derived from the inverse quantization: `polarity = 2 * (gradation / 63) - 1`.

---

## Scientific Basis

### Weber's Law (Weber 1834)

The just-noticeable difference (JND) between two stimuli is proportional to the magnitude of the stimulus. For perceptual continua relevant to musical experience, this ratio (the Weber fraction) is typically 2-5%. The 1.56% step size falls comfortably below this threshold.

### Stevens' Power Law (Stevens 1957)

Perceived magnitude follows a power function of stimulus intensity. This means that equal physical steps do not produce equal perceptual steps. However, because η quantizes polarity signals (which are already perceptually scaled by ζ), the uniform 64-step grid maps to approximately uniform perceptual steps.

### Prototype Theory (Rosch 1975)

Cognitive categories are organized around prototypes -- the best, most central examples. Each band term (e.g., "happy," "euphoric") serves as the prototype for its gradation region. The 8 gradations within each band represent varying distances from the prototype.

### Semantic Field Theory (Trier 1931, Lyons 1977)

Words derive meaning from their position within structured semantic fields. The 8 terms per axis form a coherent semantic field that spans the full polarity range. Adjacent terms grade into each other naturally (e.g., "content" grades into "happy" grades into "euphoric").

---

## Design Constraints

| Constraint | Requirement | How Met |
|-----------|-------------|---------|
| Perceptual fidelity | Step < JND (~3%) | 1/64 = 1.56% < 3% |
| Compact representation | Minimal bits per axis | 6 bits = 64 levels |
| Human readability | Named intensity bands | 8 bands with prototype terms |
| Computational efficiency | Power-of-2 quantization | 64 = 2^6 |
| Symmetric structure | Equal negative/positive coverage | 4 bands each side of neutral |
| Universal neutral | Consistent midpoint across axes | Band 4 = "neutral" for all 12 axes |

---

**Parent**: [00-INDEX.md](00-INDEX.md)
**See also**: [TermCatalog.md](TermCatalog.md) for the complete 96-term vocabulary | [AxisDefinitions.md](AxisDefinitions.md) for axis source formulas | [Epistemology/Vocabulary.md](../Epistemology/Vocabulary.md) for level 7 theory
