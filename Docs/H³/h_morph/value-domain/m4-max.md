# M₄: max (x_max) — Maximum Value

**Index**: 4
**Domain**: Value
**Symbol**: x_max
**Formula**: `x_max = max(x_i) for all i in window`
**Range**: [min(x), ∞)

---

## Overview

The highest value the signal reaches within the window. Captures the ceiling/peak of the signal — useful for climax detection and peak identification.

---

## Computation

```python
def compute_max(signal: np.ndarray) -> float:
    """Compute M₄: maximum value."""
    return np.max(signal)
```

---

## Related Parameters

| Parameter | Relationship |
|-----------|--------------|
| M₃ (min) | Opposite extreme |
| M₅ (range) | Combined: range = max - min |
| M₂₂ (peaks) | Count of local maxima |

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | lowest | Minimum ceiling | < 0.125 |
| 1 | very_low | Very low ceiling | < 0.25 |
| 2 | low | Low ceiling | < 0.375 |
| 3 | moderate | Center range | < 0.5 |
| 4 | moderate_high | Above center | < 0.625 |
| 5 | high | High ceiling | < 0.75 |
| 6 | very_high | Very high ceiling | < 0.875 |
| 7 | highest | Absolute maximum | ≥ 0.875 |

---

## Musical Interpretation

- "What is the loudest/highest point in this window?"
- Identifies climax moments, peak intensity
- Essential for dynamic range and contrast

---

**Implementation**: `Pipeline/D0/h0/h_morph/value_domain/m4_max.py`
