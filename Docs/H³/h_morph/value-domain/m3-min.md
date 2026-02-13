# M₃: min (x_min) — Minimum Value

**Index**: 3
**Domain**: Value
**Symbol**: x_min
**Formula**: `x_min = min(x_i) for all i in window`
**Range**: [-∞, max(x)]

---

## Overview

The lowest value the signal reaches within the window. Captures the floor/nadir of the signal — useful for detecting rests, diminuendos, and phrase nadirs.

---

## Computation

```python
def compute_min(signal: np.ndarray) -> float:
    """Compute M₃: minimum value."""
    return np.min(signal)
```

---

## Related Parameters

| Parameter | Relationship |
|-----------|--------------|
| M₄ (max) | Opposite extreme |
| M₅ (range) | Combined: range = max - min |
| M₂₃ (troughs) | Count of local minima |

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | lowest | Absolute minimum | < 0.125 |
| 1 | very_low | Very low floor | < 0.25 |
| 2 | low | Low floor | < 0.375 |
| 3 | moderate_low | Below center | < 0.5 |
| 4 | moderate | Center range | < 0.625 |
| 5 | elevated | Above center | < 0.75 |
| 6 | high | High floor | < 0.875 |
| 7 | highest | Maximum floor | ≥ 0.875 |

---

## Musical Interpretation

- "What is the quietest/lowest point in this window?"
- Identifies softest moments, rest points
- Essential for dynamic range calculation

---

**Implementation**: `Pipeline/D0/h0/h_morph/value_domain/m3_min.py`
