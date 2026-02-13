# Bidirectional Mode (L₂) — Past ↔ Future

**Index**: 2
**Symbol**: L_Bi
**Direction**: Past ↔ Future
**Causality**: Acausal
**Real-time Compatible**: No (requires lookahead)

---

## Overview

Bidirectional mode includes both past and future in the attention window, centered on the current moment. This provides the fullest temporal context but requires lookahead buffering.

---

## Mask Function

```python
def bidirectional_mask(delta_t: float) -> float:
    """Compute mask for bidirectional mode."""
    return 1.0  # No masking - use all data
```

---

## Attention Formula

```
A_bidirectional(Δt) = exp(-3|Δt|/H)

For all Δt: A = exp(-3|Δt|/H)  (exponential decay in both directions)
```

---

## Attention Profile

```
         ▲ Attention
         │
    1.0 ─┤   ╭─╮
         │  ╱   ╲
         │ ╱     ╲
         │╱       ╲
         ╱         ╲
     0 ──┴─────┬─────┴───►
        -H/2  Now  +H/2  Time

    Both past and future are weighted symmetrically
```

---

## Time Window

```
For window H at current time t:

Bidirectional mode: [t - H/2, t + H/2]

Half window before, half window after.
Requires H/2 seconds of lookahead buffer.
```

---

## Neuroscience Basis

Bidirectional attention relates to:
- **Context integration**: Understanding requires full context
- **Pattern recognition**: Patterns span both directions
- **Semantic processing**: Meaning emerges from context
- **Offline analysis**: Complete information available

---

## Musical Interpretation

- "What is the full context surrounding this moment?"
- Captures local patterns centered on the current time
- Ideal for understanding musical structure

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | narrow_context | Very narrow | < 0.125 |
| 1 | limited_context | Limited span | < 0.25 |
| 2 | moderate_context | Moderate span | < 0.375 |
| 3 | standard_context | Normal context | < 0.5 |
| 4 | broad_context | Broad span | < 0.625 |
| 5 | wide_context | Wide span | < 0.75 |
| 6 | expansive_context | Expansive span | < 0.875 |
| 7 | full_context | Complete context | ≥ 0.875 |

---

## Advantages Over Forward/Backward

| Aspect | Bidirectional Advantage |
|--------|------------------------|
| **Context** | Maximum information |
| **Symmetry** | Equal weight to both directions |
| **Pattern detection** | Best for local patterns |
| **Phase analysis** | Accurate phase estimation |

---

**Implementation**: `Pipeline/D0/h0/h_law/bidirectional.py`
