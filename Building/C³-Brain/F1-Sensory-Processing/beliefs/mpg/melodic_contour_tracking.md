# melodic_contour_tracking — Appraisal Belief

**Category**: Appraisal (observe-only, no PE)
**Function**: F1 (Sensory Processing)
**Mechanism**: MPG (Melodic Processing Gradient)

---

## Definition

> "The current melodic contour is being tracked with this level of
> complexity and directional change."

## Observe Formula

```
observe = 0.45 × P1:contour_state
        + 0.30 × E2:contour_complexity
        + 0.25 × E1:sequence_anterior
```

| Source Dim | MPG Index | Weight | Rationale |
|-----------|-----------|--------|-----------|
| P1:contour_state | 8 | 0.45 | Primary relay output for contour tracking |
| E2:contour_complexity | 2 | 0.30 | Melodic complexity measure |
| E1:sequence_anterior | 1 | 0.25 | Anterior AC activation level |

Weights sum to 1.0.

---

## Dependency Chain

```
R³/H³ → MPG (Depth 0, Relay) → melodic_contour_tracking
```

No upstream mechanism dependency. MPG reads R³/H³ directly.

---

## Downstream Consumers

- Salience: MPG contour tracking contributes to attention allocation
- Reward: melodic complexity modulates aesthetic response
- Other beliefs: context for pitch_identity.predict()

## Implementation

File: `Musical_Intelligence/brain/functions/f1/beliefs/mpg/melodic_contour_tracking.py`
