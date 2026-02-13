# M₁₃: jerk (δ³) — Third Derivative

**Index**: 13
**Domain**: Derivative
**Symbol**: δ³ (or d³x/dt³)
**Formula**: `δ³_i = d³x/dt³`
**Range**: (-∞, ∞)

---

## Overview

Instantaneous rate of change of acceleration — the "jerk" or "jolt." High jerk indicates abrupt changes in acceleration; low jerk indicates smooth dynamics.

---

## Computation

```python
def compute_jerk(signal: np.ndarray, dt: float, attention: np.ndarray) -> float:
    """Compute M₁₃: attention-weighted current jerk."""
    velocity = np.gradient(signal, dt)
    acceleration = np.gradient(velocity, dt)
    jerk = np.gradient(acceleration, dt)
    return np.sum(jerk * attention) / np.sum(attention)
```

---

## Jerk and Smoothness

```
High |jerk| → Abrupt, discontinuous changes
Low |jerk|  → Smooth, continuous changes

M₁₅ (smoothness) = -log(mean(jerk²))
```

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | sharp_negative | Strong negative jerk | < -0.75 |
| 1 | jerky_negative | Moderate negative | < -0.375 |
| 2 | bumpy_negative | Slight negative | < -0.125 |
| 3 | smooth_low | Nearly smooth | < 0.125 |
| 4 | smooth_high | Nearly smooth | < 0.375 |
| 5 | bumpy_positive | Slight positive | < 0.625 |
| 6 | jerky_positive | Moderate positive | < 0.875 |
| 7 | sharp_positive | Strong positive jerk | ≥ 0.875 |

---

## Musical Interpretation

- High |jerk|: Sforzando, accent, sudden attack
- Low |jerk|: Legato, smooth portamento, gradual dynamics
- Jerk is key to detecting "sharpness" of musical gestures

---

**Implementation**: `Pipeline/D0/h0/h_morph/derivative_domain/m13_jerk.py`
