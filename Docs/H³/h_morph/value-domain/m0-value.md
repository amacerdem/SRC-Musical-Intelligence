# M₀: value (μ_w) — Attention-Weighted Current

**Index**: 0
**Domain**: Value
**Symbol**: μ_w
**Formula**: `μ_w = Σ(x_i × A_i) / Σ(A_i)`
**Range**: [min(x), max(x)]

---

## Overview

The attention-weighted current value of the signal. Unlike mean (M₁), this parameter emphasizes temporally relevant samples based on the H-Law attention mask.

---

## Computation

```python
def compute_value(signal: np.ndarray, attention: np.ndarray) -> float:
    """Compute M₀: attention-weighted current value."""
    return np.sum(signal * attention) / np.sum(attention)
```

---

## H-Law Interaction

| Mode | Emphasis | Interpretation |
|------|----------|----------------|
| **Forward** | Recent past | "Current state considering history" |
| **Backward** | Near future | "Predicted upcoming state" |
| **Bidirectional** | Centered | "Context-aware current" |

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | minimal | Extremely low | < 0.125 |
| 1 | very_low | Very low level | < 0.25 |
| 2 | low | Below average | < 0.375 |
| 3 | moderate_low | Slightly below | < 0.5 |
| 4 | moderate_high | Slightly above | < 0.625 |
| 5 | high | Above average | < 0.75 |
| 6 | very_high | Very high level | < 0.875 |
| 7 | maximal | Extremely high | ≥ 0.875 |

---

## Musical Interpretation

- "What is the effective pitch/loudness/brightness right now?"
- Captures current state with temporal smoothing
- Essential for real-time feature tracking

---

**Implementation**: `Pipeline/D0/h0/h_morph/value_domain/m0_value.py`
