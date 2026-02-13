# M₁₄: jerk_mean (μ_δ³) — Mean Jerk

**Index**: 14
**Domain**: Derivative
**Symbol**: μ_δ³
**Formula**: `μ_δ³ = mean(d³x/dt³)`
**Range**: (-∞, ∞)

---

## Overview

Average jerk over the entire window. Indicates the overall "jerkiness" tendency of the signal's evolution.

---

## Computation

```python
def compute_jerk_mean(signal: np.ndarray, dt: float) -> float:
    """Compute M₁₄: mean jerk."""
    velocity = np.gradient(signal, dt)
    acceleration = np.gradient(velocity, dt)
    jerk = np.gradient(acceleration, dt)
    return np.mean(jerk)
```

---

## Note on Interpretation

Mean jerk is often close to zero (positive and negative jerks cancel). The magnitude (via M₁₅ smoothness) is often more informative than the sign.

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | negative_bias | Strong negative jerk bias | < -0.75 |
| 1 | softening_trend | Moderate negative | < -0.375 |
| 2 | slight_softening | Mild negative | < -0.125 |
| 3 | balanced_low | Nearly balanced | < 0.125 |
| 4 | balanced_high | Nearly balanced | < 0.375 |
| 5 | slight_sharpening | Mild positive | < 0.625 |
| 6 | sharpening_trend | Moderate positive | < 0.875 |
| 7 | positive_bias | Strong positive jerk bias | ≥ 0.875 |

---

## Musical Interpretation

- Mean jerk bias can indicate overall gesture direction
- Positive bias: Attacks becoming sharper
- Negative bias: Attacks becoming softer
- Zero: Balanced gesture profile

---

**Implementation**: `Pipeline/D0/h0/h_morph/derivative_domain/m14_jerk_mean.py`
