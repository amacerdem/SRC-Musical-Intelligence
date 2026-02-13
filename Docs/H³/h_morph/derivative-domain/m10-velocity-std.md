# M₁₀: velocity_std (σ_δ) — Velocity Variability

**Index**: 10
**Domain**: Derivative
**Symbol**: σ_δ
**Formula**: `σ_δ = std(δ_i)`
**Range**: [0, ∞)

---

## Overview

Standard deviation of velocity values across the window. High σ_δ indicates erratic changes; low σ_δ indicates consistent change rate.

---

## Computation

```python
def compute_velocity_std(signal: np.ndarray, dt: float) -> float:
    """Compute M₁₀: velocity variability."""
    velocity = np.gradient(signal, dt)
    return np.std(velocity)
```

---

## Relationship to M₁₉ (stability)

```
M₁₉ (stability) = 1 / (1 + σ_δ²)

High velocity_std → Low stability
Low velocity_std → High stability
```

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | constant | Nearly constant velocity | < 0.125 |
| 1 | very_consistent | Very low variability | < 0.25 |
| 2 | consistent | Low variability | < 0.375 |
| 3 | moderate | Some variability | < 0.5 |
| 4 | variable | Noticeable variability | < 0.625 |
| 5 | erratic | High variability | < 0.75 |
| 6 | volatile | Very high variability | < 0.875 |
| 7 | chaotic | Extreme variability | ≥ 0.875 |

---

## Musical Interpretation

- Low σ_δ: Smooth crescendo, steady portamento
- High σ_δ: Tremolo, rapid alternation, unstable expression
- "How consistently is the signal changing?"

---

**Implementation**: `Pipeline/D0/h0/h_morph/derivative_domain/m10_velocity_std.py`
