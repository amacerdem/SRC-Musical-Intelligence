# Forward Mode (L₀) — Past → Present

**Index**: 0
**Symbol**: L_F
**Direction**: Past → Present
**Causality**: Causal
**Real-time Compatible**: Yes

---

## Overview

Forward mode focuses attention on the past leading up to the current moment. Only information from before the current time contributes to the feature computation. This mode is essential for real-time processing.

---

## Mask Function

```python
def forward_mask(delta_t: float) -> float:
    """Compute mask for forward mode."""
    return 1.0 if delta_t <= 0 else 0.0
```

---

## Attention Formula

```
A_forward(Δt) = exp(-3|Δt|/H) × mask_forward(Δt)

For Δt ≤ 0 (past): A = exp(3Δt/H)    (exponential decay into past)
For Δt > 0 (future): A = 0            (no future information)
```

---

## Attention Profile

```
         ▲ Attention
         │
    1.0 ─┤   ╭─
         │   │
         │  ╱│
         │ ╱ │
         │╱  │
     0 ──┴───┼────────►
        -H  Now       Time

    Past is weighted, future is blocked
```

---

## Time Window

```
For window H at current time t:

Forward mode: [t - H, t]

Only samples from the last H seconds are used.
```

---

## Neuroscience Basis

Forward attention aligns with:
- **Causal reasoning**: Causes precede effects
- **Memory retrieval**: We remember the past, not the future
- **Predictive processing**: Predictions based on history
- **Real-time processing**: No future information available

---

## Musical Interpretation

- "What has happened that led to this moment?"
- Captures cumulative effects (dynamics building, harmony unfolding)
- Essential for real-time music analysis and generation

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | recent | Very recent past only | < 0.125 |
| 1 | short_history | Short history | < 0.25 |
| 2 | moderate_history | Moderate history | < 0.375 |
| 3 | standard_history | Normal history | < 0.5 |
| 4 | extended_history | Extended history | < 0.625 |
| 5 | long_history | Long history | < 0.75 |
| 6 | deep_history | Deep history | < 0.875 |
| 7 | full_history | Complete history | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/h_law/forward.py`
