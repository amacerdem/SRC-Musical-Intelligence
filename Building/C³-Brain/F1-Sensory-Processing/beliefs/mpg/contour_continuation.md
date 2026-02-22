# contour_continuation — Anticipation Belief

**Category**: Anticipation (forward prediction, no PE)
**Function**: F1 (Sensory Processing)
**Mechanism**: MPG (Melodic Processing Gradient)

---

## Definition

> "The melodic contour will continue / a phrase boundary is approaching."

## Observe Formula

```
observe = 1.0 × F0:phrase_boundary_pred
```

| Source Dim | MPG Index | Weight | Rationale |
|-----------|-----------|--------|-----------|
| F0:phrase_boundary_pred | 9 | 1.0 | Direct F-layer forecast output |

Single-source anticipation — the MPG's phrase boundary prediction
is the forward-looking signal that feeds into Core beliefs' predict()
methods as context.

---

## Dependency Chain

```
R³/H³ → MPG (Depth 0, Relay) → contour_continuation
```

No upstream mechanism dependency. MPG reads R³/H³ directly.

---

## Downstream Consumers

- Core belief context: feeds into predict() methods of:
  - pitch_identity (PCCR): phrase boundaries affect chroma predictions
  - harmonic_stability (BCH): boundary approaching → stability drops
- Anticipation beliefs do NOT generate prediction errors.

## Implementation

File: `Musical_Intelligence/brain/functions/f1/beliefs/mpg/contour_continuation.py`
