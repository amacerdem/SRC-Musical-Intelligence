# Backward Mode (L₁) — Present → Future

**Index**: 1
**Symbol**: L_B
**Direction**: Present → Future
**Causality**: Anti-causal
**Real-time Compatible**: No (requires lookahead)

---

## Overview

Backward mode focuses attention on the future following the current moment. Information from after the current time contributes to feature computation. This mode requires lookahead buffering.

---

## Mask Function

```python
def backward_mask(delta_t: float) -> float:
    """Compute mask for backward mode."""
    return 1.0 if delta_t >= 0 else 0.0
```

---

## Attention Formula

```
A_backward(Δt) = exp(-3|Δt|/H) × mask_backward(Δt)

For Δt < 0 (past): A = 0              (no past information)
For Δt ≥ 0 (future): A = exp(-3Δt/H)  (exponential decay into future)
```

---

## Attention Profile

```
         ▲ Attention
         │
    1.0 ─┤─╮
         │ │
         │ │╲
         │ │ ╲
         │ │  ╲
     0 ──┼─┴────────►
       Now  +H      Time

    Past is blocked, future is weighted
```

---

## Time Window

```
For window H at current time t:

Backward mode: [t, t + H]

Only samples from the next H seconds are used.
Requires H seconds of lookahead buffer.
```

---

## Neuroscience Basis

Backward attention relates to:
- **Expectation**: Anticipated events ahead
- **Goal-directed processing**: Preparing for upcoming events
- **Predictive coding**: Forward models project into future
- **Offline processing**: Post-hoc analysis can use "future"

---

## Musical Interpretation

- "What is coming that I'm preparing for?"
- Captures anticipation and upcoming events
- Used in offline analysis where full piece is available

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | immediate | Very near future | < 0.125 |
| 1 | short_future | Short horizon | < 0.25 |
| 2 | moderate_future | Moderate horizon | < 0.375 |
| 3 | standard_future | Normal lookahead | < 0.5 |
| 4 | extended_future | Extended lookahead | < 0.625 |
| 5 | long_future | Long horizon | < 0.75 |
| 6 | deep_future | Deep lookahead | < 0.875 |
| 7 | full_future | Complete future | ≥ 0.875 |

---

## Implementation Note

Backward mode requires pre-buffering the future portion of the signal before computing features at the current time.

---

**Implementation**: `Pipeline/D0/h0/h_law/backward.py`
