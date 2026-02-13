# Derivative Domain — M₈-M₁₅ (Temporal Dynamics)

**Index Range**: 8-15
**Parameters**: 8
**Question**: HOW is the signal changing?
**Function**: Temporal derivatives and smoothness characteristics

---

## Overview

The Derivative domain captures the **dynamic properties** of a signal — its rate of change, acceleration, and smoothness. These parameters answer "how is the signal evolving?" across time.

---

## Parameters

| Index | Name | Symbol | Formula | Description |
|-------|------|--------|---------|-------------|
| [M₈](m8-velocity.md) | velocity | δ | dx/dt | First derivative (current) |
| [M₉](m9-velocity-mean.md) | velocity_mean | μ_δ | mean(δ_i) | Average velocity |
| [M₁₀](m10-velocity-std.md) | velocity_std | σ_δ | std(δ_i) | Velocity variability |
| [M₁₁](m11-acceleration.md) | acceleration | δ² | d²x/dt² | Second derivative (current) |
| [M₁₂](m12-acceleration-mean.md) | acceleration_mean | μ_δ² | mean(δ²_i) | Average acceleration |
| [M₁₃](m13-jerk.md) | jerk | δ³ | d³x/dt³ | Third derivative (current) |
| [M₁₄](m14-jerk-mean.md) | jerk_mean | μ_δ³ | mean(δ³_i) | Average jerk |
| [M₁₅](m15-smoothness.md) | smoothness | S | -log(∫|jerk|²dt) | Inverse jerk magnitude |

---

## Derivative Hierarchy

```
Signal x(t)
    │
    ├─── M₈ (velocity) = dx/dt
    │        │
    │        ├── M₉ (velocity_mean)
    │        └── M₁₀ (velocity_std)
    │
    ├─── M₁₁ (acceleration) = d²x/dt²
    │        │
    │        └── M₁₂ (acceleration_mean)
    │
    └─── M₁₃ (jerk) = d³x/dt³
             │
             ├── M₁₄ (jerk_mean)
             └── M₁₅ (smoothness) = inverse
```

---

## Musical Interpretation

| Parameter | Low Value | High Value |
|-----------|-----------|------------|
| **velocity** | Stable/decreasing | Increasing rapidly |
| **velocity_mean** | Overall descending | Overall ascending |
| **velocity_std** | Consistent change rate | Erratic changes |
| **acceleration** | Slowing down | Speeding up |
| **acceleration_mean** | Overall deceleration | Overall acceleration |
| **jerk** | Smooth acceleration | Abrupt acc. changes |
| **jerk_mean** | Steady dynamics | Jerky dynamics |
| **smoothness** | Jerky/abrupt | Smooth/continuous |

---

## Musical Examples

| Gesture | velocity | acceleration | smoothness |
|---------|----------|--------------|------------|
| **Sustained note** | ~0 | ~0 | High |
| **Crescendo** | +constant | ~0 | High |
| **Attack transient** | +high | -high | Low |
| **Sforzando** | spike | spike | Very low |
| **Portamento** | moderate | low | High |

---

## Implementation

```python
def compute_derivative_domain(signal: np.ndarray, dt: float, attention: np.ndarray) -> np.ndarray:
    """Compute Derivative domain parameters M₈-M₁₅."""
    # Compute derivatives
    velocity = np.gradient(signal, dt)
    acceleration = np.gradient(velocity, dt)
    jerk = np.gradient(acceleration, dt)

    # Attention-weighted current values
    weights = attention / np.sum(attention)

    return np.array([
        np.sum(velocity * weights),       # M₈: velocity
        np.mean(velocity),                 # M₉: velocity_mean
        np.std(velocity),                  # M₁₀: velocity_std
        np.sum(acceleration * weights),   # M₁₁: acceleration
        np.mean(acceleration),             # M₁₂: acceleration_mean
        np.sum(jerk * weights),           # M₁₃: jerk
        np.mean(jerk),                     # M₁₄: jerk_mean
        -np.log(np.mean(jerk**2) + 1e-10), # M₁₅: smoothness
    ])
```

---

**Implementation**: `Pipeline/D0/h0/h_morph/derivative_domain.py`
