# M₉: velocity_mean (μ_δ) — Mean Velocity

**Index**: 9
**Domain**: Derivative
**Symbol**: μ_δ
**Formula**: `μ_δ = (1/n) × Σδ_i`
**Range**: (-∞, ∞)

---

## Overview

Average rate of change over the entire window. Indicates the overall trend direction regardless of local fluctuations.

---

## Computation

```python
def compute_velocity_mean(signal: np.ndarray, dt: float) -> float:
    """Compute M₉: mean velocity."""
    velocity = np.gradient(signal, dt)
    return np.mean(velocity)
```

---

## Difference from M₈ (velocity)

| Aspect | M₈ (velocity) | M₉ (velocity_mean) |
|--------|---------------|-------------------|
| Weighting | Attention-weighted | Unweighted |
| Scope | Current moment | Entire window |
| Use case | Instantaneous change | Overall trend |

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | strongly_descending | Strong downward trend | < -0.75 |
| 1 | descending | Clear descent | < -0.375 |
| 2 | slightly_descending | Mild descent | < -0.125 |
| 3 | flat_low | Nearly flat | < 0.125 |
| 4 | flat_high | Nearly flat | < 0.375 |
| 5 | slightly_ascending | Mild ascent | < 0.625 |
| 6 | ascending | Clear ascent | < 0.875 |
| 7 | strongly_ascending | Strong upward trend | ≥ 0.875 |

---

## Musical Interpretation

- μ_δ > 0: Overall ascending melodic line, building dynamics
- μ_δ < 0: Overall descending melodic line, receding dynamics
- μ_δ ≈ 0: Balanced or oscillating signal

---

**Implementation**: `Pipeline/D0/h0/h_morph/derivative_domain/m9_velocity_mean.py`
