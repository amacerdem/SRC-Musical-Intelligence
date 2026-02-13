# M₁₆: curvature (κ) — Geometric Curvature

**Index**: 16
**Domain**: Shape
**Symbol**: κ (kappa)
**Formula**: `κ = |d²x/dt²| / (1 + (dx/dt)²)^1.5`
**Range**: [0, ∞)

---

## Overview

Measures the geometric curvature of the signal trajectory — how sharply the signal bends at each point. High curvature indicates sharp turns; low curvature indicates straight-line motion.

---

## Computation

```python
def compute_curvature(signal: np.ndarray, dt: float) -> float:
    """Compute M₁₆: mean geometric curvature."""
    velocity = np.gradient(signal, dt)
    acceleration = np.gradient(velocity, dt)
    curvature = np.abs(acceleration) / (1 + velocity**2)**1.5
    return np.mean(curvature)
```

---

## Geometric Interpretation

```
LOW CURVATURE              HIGH CURVATURE
────────────────           ╭──────╮
Straight line              Sharp bend

κ = 0 for straight         κ → ∞ for sharp corners
```

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | straight | Nearly linear | < 0.125 |
| 1 | very_slight | Very gentle curve | < 0.25 |
| 2 | slight | Gentle curve | < 0.375 |
| 3 | moderate | Some curvature | < 0.5 |
| 4 | curved | Noticeable curve | < 0.625 |
| 5 | arced | Strong curve | < 0.75 |
| 6 | bent | Very curved | < 0.875 |
| 7 | sharp | Maximum curvature | ≥ 0.875 |

---

## Musical Interpretation

- Low κ: Straight melodic line, linear dynamics
- High κ: Phrase arcs, melodic turns, dynamic inflections
- Captures the "shape" of musical gestures

---

**Implementation**: `Pipeline/D0/h0/h_morph/shape_domain/m16_curvature.py`
