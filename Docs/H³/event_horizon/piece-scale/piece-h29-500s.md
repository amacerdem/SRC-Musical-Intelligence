# H₂₉: 500s — Short Piece (Interpolated)

**Window Index**: 29
**Duration**: 500000ms (500s / 8.3 min)
**Scale**: Piece
**Neural Basis**: Early piece-level integration
**Status**: Interpolated

---

## Overview

H₂₉ is an interpolated window for short piece integration. This captures complete shorter works — pop songs, jazz standards, and shorter classical pieces — as unified wholes.

---

## Interpolation Rationale

```
H₂₈ (414s) ←──── H₂₉ (500s) ────→ H₃₀ (700s)
   DMS goal       Short piece      Medium piece
```

---

## HR⁰ Mechanisms Using This Window

| Mechanism | Windows | Function |
|-----------|---------|----------|
| **FTO** | H₂₉, H₃₀ | Extended Form-Temporal Organization |

---

## Musical Relevance

- Complete pop songs (extended versions)
- Short classical pieces (preludes, etudes)
- Jazz standards
- Single-movement works

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | incomplete | No work sense | < 0.125 |
| 1 | partial | Fragmentary | < 0.25 |
| 2 | emerging | Work forming | < 0.375 |
| 3 | building | Growing whole | < 0.5 |
| 4 | cohesive | Normal unity | < 0.625 |
| 5 | complete | Clear work | < 0.75 |
| 6 | unified | Strong whole | < 0.875 |
| 7 | masterwork | Perfect unity | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/piece_scale/h29.py`
