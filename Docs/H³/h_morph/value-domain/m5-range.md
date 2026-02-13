# M₅: range (Δx) — Dynamic Range

**Index**: 5
**Domain**: Value
**Symbol**: Δx
**Formula**: `Δx = x_max - x_min = M₄ - M₃`
**Range**: [0, ∞)

---

## Overview

The total span of the signal within the window. Measures extreme-to-extreme variation — the full dynamic or pitch range traversed.

---

## Computation

```python
def compute_range(signal: np.ndarray) -> float:
    """Compute M₅: dynamic range."""
    return np.max(signal) - np.min(signal)
```

---

## Difference from M₂ (std)

| Aspect | M₂ (std) | M₅ (range) |
|--------|----------|------------|
| Measure | Average deviation | Extreme span |
| Sensitivity | Distribution shape | Outliers |
| Robustness | Less sensitive to outliers | Sensitive to outliers |

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | minimal | Nearly no variation | < 0.125 |
| 1 | very_narrow | Very small range | < 0.25 |
| 2 | narrow | Small range | < 0.375 |
| 3 | moderate | Medium range | < 0.5 |
| 4 | wide | Above average range | < 0.625 |
| 5 | very_wide | Large range | < 0.75 |
| 6 | expansive | Very large range | < 0.875 |
| 7 | extreme | Maximum possible range | ≥ 0.875 |

---

## Musical Interpretation

- Small range: Single note, small interval, stable dynamics
- Large range: Wide melodic leap, arpeggio, dramatic dynamics
- "How much total variation exists in this window?"

---

**Implementation**: `Pipeline/D0/h0/h_morph/value_domain/m5_range.py`
