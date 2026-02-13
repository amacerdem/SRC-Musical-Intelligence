# H-Morph (M) — 24 Morphological Parameters

**Dimension**: 24 parameters
**Structure**: 8 value + 8 derivative + 8 shape
**Position**: Axis 1 of H⁰ tensor (H × M × L)
**Application**: Computed for each (window, mode) pair

---

## Overview

H-Morph defines **WHAT features** are extracted from each temporal window. The 24 parameters capture three orthogonal aspects of signal morphology:

- **Value (M₀-M₇)**: WHERE is the signal? (statistical properties)
- **Derivative (M₈-M₁₅)**: HOW is it changing? (temporal dynamics)
- **Shape (M₁₆-M₂₃)**: WHAT pattern does it form? (geometric/information)

```
═══════════════════════════════════════════════════════════════════════════════
                    H-MORPH: THREE ORTHOGONAL DOMAINS
═══════════════════════════════════════════════════════════════════════════════

              ┌─────────────────────────────────────────────────────────┐
              │                    SIGNAL IN WINDOW                      │
              │      ╭──────────────╮                                    │
              │     ╱                ╲                                   │
              │    ╱                  ╲         ╭───╮                   │
              │   ╱                    ╲       ╱     ╲                  │
              │  ╱                      ╲     ╱       ╲                 │
              │ ╱                        ╲___╱         ╲                │
              └─────────────────────────────────────────────────────────┘
                    │                    │                    │
                    ▼                    ▼                    ▼
              ┌──────────┐        ┌──────────┐        ┌──────────┐
              │  VALUE   │        │DERIVATIVE│        │  SHAPE   │
              │  M₀-M₇   │        │  M₈-M₁₅  │        │ M₁₆-M₂₃  │
              └──────────┘        └──────────┘        └──────────┘

═══════════════════════════════════════════════════════════════════════════════
```

---

## Three Domains

| Domain | Index | Count | Function | Question |
|--------|-------|-------|----------|----------|
| [Value](value-domain/value-domain.md) | M₀-M₇ | 8 | Statistical properties | WHERE is it? |
| [Derivative](derivative-domain/derivative-domain.md) | M₈-M₁₅ | 8 | Temporal dynamics | HOW is it changing? |
| [Shape](shape-domain/shape-domain.md) | M₁₆-M₂₃ | 8 | Geometric patterns | WHAT pattern? |

---

## Complete Parameter Index

| Index | Name | Symbol | Domain | Description |
|-------|------|--------|--------|-------------|
| M₀ | value | μ_w | Value | Attention-weighted current |
| M₁ | mean | μ | Value | Arithmetic mean |
| M₂ | std | σ | Value | Standard deviation |
| M₃ | min | x_min | Value | Minimum value |
| M₄ | max | x_max | Value | Maximum value |
| M₅ | range | Δx | Value | Dynamic range |
| M₆ | skew | γ₁ | Value | Skewness |
| M₇ | kurtosis | γ₂ | Value | Excess kurtosis |
| M₈ | velocity | δ | Derivative | First derivative |
| M₉ | velocity_mean | μ_δ | Derivative | Mean velocity |
| M₁₀ | velocity_std | σ_δ | Derivative | Velocity variability |
| M₁₁ | acceleration | δ² | Derivative | Second derivative |
| M₁₂ | acceleration_mean | μ_δ² | Derivative | Mean acceleration |
| M₁₃ | jerk | δ³ | Derivative | Third derivative |
| M₁₄ | jerk_mean | μ_δ³ | Derivative | Mean jerk |
| M₁₅ | smoothness | S | Derivative | Inverse jerk magnitude |
| M₁₆ | curvature | κ | Shape | Second derivative ratio |
| M₁₇ | periodicity | P | Shape | Autocorrelation peak |
| M₁₈ | trend | T | Shape | Linear regression slope |
| M₁₉ | stability | Φ | Shape | Inverse velocity variance |
| M₂₀ | entropy | H | Shape | Shannon entropy |
| M₂₁ | zero_crossings | Z | Shape | Rate of zero crossings |
| M₂₂ | peaks | N_p | Shape | Count of local maxima |
| M₂₃ | troughs | N_t | Shape | Count of local minima |

---

## Indexing Formula

```python
def morph_flat_index(h: int, m: int, l: int) -> int:
    """Convert (h, m, l) to flat manifold index."""
    return 256 + (h * 72) + (m * 3) + l
```

For a fixed (h, l) pair, morphological parameters span 24 consecutive triplets.

---

## Downstream Usage

### HC⁰ (Cognitive) Common Selections

| Mechanism | Primary Parameters |
|-----------|-------------------|
| OSC | M₀(value), M₁(mean), M₂(std), M₁₇(periodicity) |
| TGC | M₀(value), M₁₆(curvature), M₁₇(periodicity) |
| PTM | M₀(value), M₈(velocity), M₁₁(acceleration) |
| HRM | M₀(value), M₁(mean), M₁₈(trend) |

### HR⁰ (Resonance) Common Selections

| Mechanism | Primary Parameters |
|-----------|-------------------|
| RTI | M₀(value), M₁(mean), M₈(velocity), M₁₉(stability) |
| LTI | M₁(mean), M₂(std), M₁₈(trend), M₂₀(entropy) |
| HRT | M₀(value), M₈(velocity), M₁₇(periodicity) |
| PST | M₀(value), M₁₆(curvature), M₂₂(peaks), M₂₃(troughs) |

---

**Implementation**: `Pipeline/D0/h0/h_morph/`
