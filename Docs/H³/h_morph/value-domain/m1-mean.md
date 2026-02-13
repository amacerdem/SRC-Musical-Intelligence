# M₁: mean (μ) — Arithmetic Mean

**Index**: 1
**Domain**: Value
**Symbol**: μ
**Formula**: `μ = (1/n) × Σx_i`
**Range**: [min(x), max(x)]

---

## Overview

Simple arithmetic mean of all samples in the window. Unweighted — all samples contribute equally regardless of temporal position.

---

## Computation

```python
def compute_mean(signal: np.ndarray) -> float:
    """Compute M₁: arithmetic mean."""
    return np.mean(signal)
```

---

## Difference from M₀ (value)

| Aspect | M₀ (value) | M₁ (mean) |
|--------|------------|-----------|
| Weighting | Attention-weighted | Unweighted |
| Emphasis | Mode-relevant region | Entire window |
| Use case | Current state | Overall level |

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | very_low | Extremely low average | < 0.125 |
| 1 | low | Low average | < 0.25 |
| 2 | below_average | Below midpoint | < 0.375 |
| 3 | average_low | Slightly below center | < 0.5 |
| 4 | average_high | Slightly above center | < 0.625 |
| 5 | above_average | Above midpoint | < 0.75 |
| 6 | high | High average | < 0.875 |
| 7 | very_high | Extremely high average | ≥ 0.875 |

---

## Musical Interpretation

- "What is the average pitch/loudness/brightness over this period?"
- Captures overall register of a passage
- Baseline for comparison with current value (M₀)

---

**Implementation**: `Pipeline/D0/h0/h_morph/value_domain/m1_mean.py`
