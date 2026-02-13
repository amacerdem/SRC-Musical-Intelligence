# M₁₈: trend (T) — Linear Regression Slope

**Index**: 18
**Domain**: Shape
**Symbol**: T
**Formula**: `T = slope from linear regression fit`
**Range**: (-∞, ∞)

---

## Overview

The slope from fitting a linear regression line to the signal. Captures the overall directional tendency of the signal, independent of local fluctuations.

---

## Computation

```python
def compute_trend(signal: np.ndarray, dt: float) -> float:
    """Compute M₁₈: linear trend (regression slope)."""
    t = np.arange(len(signal)) * dt
    slope, _ = np.polyfit(t, signal, 1)
    return slope
```

---

## Difference from M₉ (velocity_mean)

| Aspect | M₉ (velocity_mean) | M₁₈ (trend) |
|--------|-------------------|-------------|
| Method | Mean of derivatives | Regression fit |
| Robustness | Sensitive to noise | More robust |
| Interpretation | Average local change | Overall direction |

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | strongly_falling | Strong downward trend | < -0.75 |
| 1 | falling | Clear downward | < -0.375 |
| 2 | slightly_falling | Mild downward | < -0.125 |
| 3 | flat_low | Nearly flat | < 0.125 |
| 4 | flat_high | Nearly flat | < 0.375 |
| 5 | slightly_rising | Mild upward | < 0.625 |
| 6 | rising | Clear upward | < 0.875 |
| 7 | strongly_rising | Strong upward trend | ≥ 0.875 |

---

## Musical Interpretation

- T > 0: Overall crescendo, ascending melody
- T < 0: Overall decrescendo, descending melody
- T ≈ 0: Stable or oscillating around a center
- Used by LTI and HRM mechanisms for pattern tracking

---

**Implementation**: `Pipeline/D0/h0/h_morph/shape_domain/m18_trend.py`
