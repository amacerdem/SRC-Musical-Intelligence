# M₆: skew (γ₁) — Skewness

**Index**: 6
**Domain**: Value
**Symbol**: γ₁
**Formula**: `γ₁ = E[(x - μ)³] / σ³`
**Range**: (-∞, ∞), typical [-2, 2]

---

## Overview

Measures asymmetry of the signal distribution within the window.

- γ₁ = 0: Symmetric distribution
- γ₁ > 0: Right-skewed (more low values, long right tail)
- γ₁ < 0: Left-skewed (more high values, long left tail)

---

## Computation

```python
def compute_skew(signal: np.ndarray) -> float:
    """Compute M₆: skewness."""
    return scipy.stats.skew(signal)
```

---

## Visual Interpretation

```
LEFT-SKEWED (γ₁ < 0)      SYMMETRIC (γ₁ = 0)      RIGHT-SKEWED (γ₁ > 0)
       ╭───╮                   ╭───╮                      ╭───╮
      ╱     ╲                 ╱     ╲                   ╱     ╲
    ╭╯       ╲              ╱       ╲                 ╱       ╰╮
   ╱          ╰─────      ╱         ╲              ─────╯      ╲
More high values       Balanced                More low values
```

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | left_heavy | Strong left skew | < -0.75 |
| 1 | left_leaning | Moderate left skew | < -0.375 |
| 2 | slight_left | Slight left skew | < -0.125 |
| 3 | symmetric_low | Nearly symmetric | < 0.125 |
| 4 | symmetric_high | Nearly symmetric | < 0.375 |
| 5 | slight_right | Slight right skew | < 0.625 |
| 6 | right_leaning | Moderate right skew | < 0.875 |
| 7 | right_heavy | Strong right skew | ≥ 0.875 |

---

## Musical Interpretation

- γ₁ > 0: Mostly quiet with occasional loud peaks
- γ₁ < 0: Mostly loud with occasional quiet moments
- γ₁ ≈ 0: Balanced dynamic distribution

---

**Implementation**: `Pipeline/D0/h0/h_morph/value_domain/m6_skew.py`
