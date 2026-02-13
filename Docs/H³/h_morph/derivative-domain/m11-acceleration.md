# M₁₁: acceleration (δ²) — Second Derivative

**Index**: 11
**Domain**: Derivative
**Symbol**: δ² (or d²x/dt²)
**Formula**: `δ²_i = d²x/dt²`
**Range**: (-∞, ∞)

---

## Overview

Instantaneous rate of change of velocity — the attention-weighted current acceleration. Indicates whether changes are speeding up or slowing down.

---

## Computation

```python
def compute_acceleration(signal: np.ndarray, dt: float, attention: np.ndarray) -> float:
    """Compute M₁₁: attention-weighted current acceleration."""
    velocity = np.gradient(signal, dt)
    acceleration = np.gradient(velocity, dt)
    return np.sum(acceleration * attention) / np.sum(attention)
```

---

## Physical Analogy

```
Signal x(t)     = position
Velocity δ      = speed
Acceleration δ² = force/mass

Positive acceleration → speeding up
Negative acceleration → slowing down
```

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | braking_hard | Strong deceleration | < -0.75 |
| 1 | braking | Moderate deceleration | < -0.375 |
| 2 | slowing | Slight deceleration | < -0.125 |
| 3 | coasting_low | Nearly constant | < 0.125 |
| 4 | coasting_high | Nearly constant | < 0.375 |
| 5 | accelerating | Slight acceleration | < 0.625 |
| 6 | accelerating_fast | Moderate acceleration | < 0.875 |
| 7 | surging | Strong acceleration | ≥ 0.875 |

---

## Musical Interpretation

- δ² > 0: Crescendo intensifying, pitch glide accelerating
- δ² < 0: Crescendo reaching plateau, attack decay
- δ² ≈ 0: Linear change rate (constant velocity)

---

**Implementation**: `Pipeline/D0/h0/h_morph/derivative_domain/m11_acceleration.py`
