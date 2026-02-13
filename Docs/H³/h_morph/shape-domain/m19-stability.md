# M₁₉: stability (Φ) — Inverse Velocity Variance

**Index**: 19
**Domain**: Shape
**Symbol**: Φ (Phi)
**Formula**: `Φ = 1 / (1 + σ_δ²)`
**Range**: (0, 1]

---

## Overview

Measures the stability of the signal by computing the inverse of velocity variance. High stability means the signal changes consistently; low stability means erratic, unpredictable changes.

---

## Computation

```python
def compute_stability(signal: np.ndarray, dt: float) -> float:
    """Compute M₁₉: stability (inverse velocity variance)."""
    velocity = np.gradient(signal, dt)
    velocity_var = np.var(velocity)
    return 1 / (1 + velocity_var)
```

---

## Relationship to M₁₀ (velocity_std)

```
Φ = 1 / (1 + σ_δ²)

When σ_δ = 0:  Φ = 1 (perfectly stable)
When σ_δ → ∞: Φ → 0 (completely unstable)
```

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | chaotic | Extremely unstable | < 0.125 |
| 1 | very_unstable | Very erratic | < 0.25 |
| 2 | unstable | Erratic changes | < 0.375 |
| 3 | fluctuating | Variable stability | < 0.5 |
| 4 | moderate | Somewhat stable | < 0.625 |
| 5 | stable | Fairly consistent | < 0.75 |
| 6 | very_stable | Very consistent | < 0.875 |
| 7 | rock_solid | Perfectly stable | ≥ 0.875 |

---

## Musical Interpretation

- High Φ: Sustained notes, steady dynamics, held pitch
- Low Φ: Tremolo, flutter, unstable vibrato
- Used by RTI and TKT mechanisms for tracking stability

---

**Implementation**: `Pipeline/D0/h0/h_morph/shape_domain/m19_stability.py`
