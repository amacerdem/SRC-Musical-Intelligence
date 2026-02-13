# M₁₂: acceleration_mean (μ_δ²) — Mean Acceleration

**Index**: 12
**Domain**: Derivative
**Symbol**: μ_δ²
**Formula**: `μ_δ² = mean(d²x/dt²)`
**Range**: (-∞, ∞)

---

## Overview

Average acceleration over the entire window. Indicates whether the signal's rate of change is generally increasing or decreasing across the window.

---

## Computation

```python
def compute_acceleration_mean(signal: np.ndarray, dt: float) -> float:
    """Compute M₁₂: mean acceleration."""
    velocity = np.gradient(signal, dt)
    acceleration = np.gradient(velocity, dt)
    return np.mean(acceleration)
```

---

## Difference from M₁₁ (acceleration)

| Aspect | M₁₁ (acceleration) | M₁₂ (acceleration_mean) |
|--------|-------------------|------------------------|
| Weighting | Attention-weighted | Unweighted |
| Scope | Current moment | Entire window |
| Use case | Instantaneous | Overall curvature |

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | decelerating_strongly | Strong overall decel | < -0.75 |
| 1 | decelerating | Clear deceleration | < -0.375 |
| 2 | slowing_slightly | Mild deceleration | < -0.125 |
| 3 | linear_low | Nearly linear | < 0.125 |
| 4 | linear_high | Nearly linear | < 0.375 |
| 5 | accelerating_slightly | Mild acceleration | < 0.625 |
| 6 | accelerating | Clear acceleration | < 0.875 |
| 7 | accelerating_strongly | Strong overall accel | ≥ 0.875 |

---

## Musical Interpretation

- μ_δ² > 0: Generally convex shape (accelerating changes)
- μ_δ² < 0: Generally concave shape (decelerating changes)
- μ_δ² ≈ 0: Linear overall trajectory

---

**Implementation**: `Pipeline/D0/h0/h_morph/derivative_domain/m12_acceleration_mean.py`
