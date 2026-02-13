# M₂: std (σ) — Standard Deviation

**Index**: 2
**Domain**: Value
**Symbol**: σ
**Formula**: `σ = √[(1/n) × Σ(x_i - μ)²]`
**Range**: [0, ∞)

---

## Overview

Measures the spread/variability of the signal around the mean. Low σ indicates a stable signal; high σ indicates a variable signal.

---

## Computation

```python
def compute_std(signal: np.ndarray) -> float:
    """Compute M₂: standard deviation."""
    return np.std(signal)
```

---

## Related Parameters

| Parameter | Relationship |
|-----------|--------------|
| M₅ (range) | Extreme-to-extreme span |
| M₁₉ (stability) | Inverse of velocity variance |
| M₂₀ (entropy) | Information-theoretic variability |

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | static | Nearly constant | < 0.125 |
| 1 | very_stable | Very low variation | < 0.25 |
| 2 | stable | Low variation | < 0.375 |
| 3 | moderate | Some variation | < 0.5 |
| 4 | variable | Noticeable variation | < 0.625 |
| 5 | dynamic | Significant variation | < 0.75 |
| 6 | very_dynamic | High variation | < 0.875 |
| 7 | extreme | Maximum variation | ≥ 0.875 |

---

## Musical Interpretation

- Low σ: Sustained note, stable pitch
- High σ: Rapid changes, arpeggio, texture change
- "How consistent is this signal within the window?"

---

**Implementation**: `Pipeline/D0/h0/h_morph/value_domain/m2_std.py`
