# M₈: velocity (δ) — First Derivative

**Index**: 8
**Domain**: Derivative
**Symbol**: δ (or dx/dt)
**Formula**: `δ_i = (x_{i+1} - x_{i-1}) / (2Δt)`
**Range**: (-∞, ∞)

---

## Overview

Instantaneous rate of change of the signal — the attention-weighted current velocity. Indicates whether the signal is currently increasing, decreasing, or stable.

---

## Computation

```python
def compute_velocity(signal: np.ndarray, dt: float, attention: np.ndarray) -> float:
    """Compute M₈: attention-weighted current velocity."""
    velocity = np.gradient(signal, dt)
    return np.sum(velocity * attention) / np.sum(attention)
```

---

## H-Law Interaction

| Mode | Emphasis | Interpretation |
|------|----------|----------------|
| **Forward** | Recent trend | "Current rate of change" |
| **Backward** | Future trend | "Predicted change direction" |
| **Bidirectional** | Centered | "Local slope at center" |

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | falling_fast | Rapid decrease | < -0.75 |
| 1 | falling | Moderate decrease | < -0.375 |
| 2 | declining | Slight decrease | < -0.125 |
| 3 | stable_low | Nearly stable | < 0.125 |
| 4 | stable_high | Nearly stable | < 0.375 |
| 5 | rising | Slight increase | < 0.625 |
| 6 | climbing | Moderate increase | < 0.875 |
| 7 | soaring | Rapid increase | ≥ 0.875 |

---

## Musical Interpretation

- δ > 0: Crescendo, ascending pitch, brightening timbre
- δ < 0: Decrescendo, descending pitch, darkening timbre
- δ ≈ 0: Sustained note, stable feature

---

**Implementation**: `Pipeline/D0/h0/h_morph/derivative_domain/m8_velocity.py`
