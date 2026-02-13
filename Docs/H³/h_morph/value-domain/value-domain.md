# Value Domain — M₀-M₇ (Statistical Properties)

**Index Range**: 0-7
**Parameters**: 8
**Question**: WHERE is the signal?
**Function**: Statistical description of signal level and distribution

---

## Overview

The Value domain captures the **static properties** of a signal within a temporal window — its level, spread, and distributional characteristics. These parameters answer "where is the signal?" without considering how it got there.

---

## Parameters

| Index | Name | Symbol | Formula | Description |
|-------|------|--------|---------|-------------|
| [M₀](m0-value.md) | value | μ_w | Σ(x_i × A_i) / Σ(A_i) | Attention-weighted current |
| [M₁](m1-mean.md) | mean | μ | (1/n) × Σx_i | Arithmetic mean |
| [M₂](m2-std.md) | std | σ | √[(1/n) × Σ(x_i - μ)²] | Standard deviation |
| [M₃](m3-min.md) | min | x_min | min(x_i) | Minimum value |
| [M₄](m4-max.md) | max | x_max | max(x_i) | Maximum value |
| [M₅](m5-range.md) | range | Δx | x_max - x_min | Dynamic range |
| [M₆](m6-skew.md) | skew | γ₁ | E[(x-μ)³]/σ³ | Distribution asymmetry |
| [M₇](m7-kurtosis.md) | kurtosis | γ₂ | E[(x-μ)⁴]/σ⁴ - 3 | Distribution tailedness |

---

## Relationships

```
                M₃ (min) ─────────────────────── M₄ (max)
                    │                               │
                    └───────── M₅ (range) ─────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                M₁ (mean)    M₂ (std)      M₀ (value)
                    │             │             │
                    └─────────────┼─────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                M₆ (skew)                  M₇ (kurtosis)
```

---

## Musical Interpretation

| Parameter | Low Value | High Value |
|-----------|-----------|------------|
| **value** | Current state is low | Current state is high |
| **mean** | Average is low in window | Average is high in window |
| **std** | Stable/consistent | Variable/dynamic |
| **min** | Floor is low | Floor is high |
| **max** | Ceiling is low | Ceiling is high |
| **range** | Narrow variation | Wide variation |
| **skew** | More high values | More low values |
| **kurtosis** | Uniform distribution | Peaked with outliers |

---

## Implementation

```python
def compute_value_domain(signal: np.ndarray, attention: np.ndarray) -> np.ndarray:
    """Compute Value domain parameters M₀-M₇."""
    weighted = signal * attention

    return np.array([
        np.sum(weighted) / np.sum(attention),  # M₀: value
        np.mean(signal),                        # M₁: mean
        np.std(signal),                         # M₂: std
        np.min(signal),                         # M₃: min
        np.max(signal),                         # M₄: max
        np.max(signal) - np.min(signal),        # M₅: range
        scipy.stats.skew(signal),               # M₆: skew
        scipy.stats.kurtosis(signal),           # M₇: kurtosis
    ])
```

---

**Implementation**: `Pipeline/D0/h0/h_morph/value_domain.py`
