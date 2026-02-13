# M₇: kurtosis (γ₂) — Excess Kurtosis

**Index**: 7
**Domain**: Value
**Symbol**: γ₂
**Formula**: `γ₂ = E[(x - μ)⁴] / σ⁴ - 3`
**Range**: [-2, ∞), typical [-1, 5]

---

## Overview

Measures "tailedness" of the signal distribution (excess kurtosis, normalized so normal = 0).

- γ₂ = 0: Normal distribution (mesokurtic)
- γ₂ > 0: Heavy tails, peaked center (leptokurtic)
- γ₂ < 0: Light tails, flat (platykurtic)

---

## Computation

```python
def compute_kurtosis(signal: np.ndarray) -> float:
    """Compute M₇: excess kurtosis."""
    return scipy.stats.kurtosis(signal)  # fisher=True gives excess
```

---

## Visual Interpretation

```
PLATYKURTIC (γ₂ < 0)     MESOKURTIC (γ₂ = 0)    LEPTOKURTIC (γ₂ > 0)
    ╭─────────╮              ╭───╮                    ╭╮
   ╱           ╲            ╱     ╲                  ╱  ╲
  ╱             ╲          ╱       ╲                ╱    ╲
─╯               ╰─      ╱         ╲             ─╯      ╰─
Flat/uniform          Normal-like           Peaked with outliers
```

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | flat | Very uniform | < -0.5 |
| 1 | platykurtic | Light tails | < 0 |
| 2 | sub_normal | Below normal | < 0.5 |
| 3 | normal | Normal-like | < 1.0 |
| 4 | super_normal | Above normal | < 2.0 |
| 5 | leptokurtic | Heavy tails | < 4.0 |
| 6 | peaked | Very peaked | < 6.0 |
| 7 | extreme | Extreme outliers | ≥ 6.0 |

---

## Musical Interpretation

- γ₂ > 0: Mostly stable with occasional extreme events (sforzandi, accents)
- γ₂ < 0: Spread evenly across range (scales, arpeggios)
- γ₂ ≈ 0: Normal-like distribution of values

---

**Implementation**: `Pipeline/D0/h0/h_morph/value_domain/m7_kurtosis.py`
