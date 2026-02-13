# M₁₅: smoothness (S) — Inverse Jerk Magnitude

**Index**: 15
**Domain**: Derivative
**Symbol**: S
**Formula**: `S = -log(∫|jerk|²dt) = -log(mean(δ³²))`
**Range**: (-∞, ∞), higher = smoother

---

## Overview

Measures the overall smoothness of the signal by computing the negative log of mean squared jerk. Higher values indicate smoother, more continuous motion; lower values indicate jerky, abrupt changes.

---

## Computation

```python
def compute_smoothness(signal: np.ndarray, dt: float) -> float:
    """Compute M₁₅: smoothness (inverse jerk magnitude)."""
    velocity = np.gradient(signal, dt)
    acceleration = np.gradient(velocity, dt)
    jerk = np.gradient(acceleration, dt)
    mean_jerk_squared = np.mean(jerk**2)
    return -np.log(mean_jerk_squared + 1e-10)  # Epsilon for stability
```

---

## Relationship to M₁₃ (jerk)

```
High |M₁₃|  →  Low M₁₅ (jerky)
Low |M₁₃|   →  High M₁₅ (smooth)
```

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | very_jerky | Extremely abrupt | < 0.125 |
| 1 | jerky | Very abrupt | < 0.25 |
| 2 | rough | Somewhat abrupt | < 0.375 |
| 3 | moderate | Some jerkiness | < 0.5 |
| 4 | fluid | Fairly smooth | < 0.625 |
| 5 | smooth | Quite smooth | < 0.75 |
| 6 | very_smooth | Very continuous | < 0.875 |
| 7 | silky | Extremely smooth | ≥ 0.875 |

---

## Musical Interpretation

- High smoothness: Legato passages, sustained notes, gentle dynamics
- Low smoothness: Percussive attacks, staccato, accents
- Key indicator of articulation style

---

**Implementation**: `Pipeline/D0/h0/h_morph/derivative_domain/m15_smoothness.py`
