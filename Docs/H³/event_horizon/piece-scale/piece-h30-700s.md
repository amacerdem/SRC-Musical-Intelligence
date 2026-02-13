# H₃₀: 700s — Medium Piece (Interpolated)

**Window Index**: 30
**Duration**: 700000ms (700s / 11.7 min)
**Scale**: Piece
**Neural Basis**: Extended narrative integration
**Status**: Interpolated

---

## Overview

H₃₀ is an interpolated window for medium piece integration. This captures symphony movements, extended jazz performances, and rock suites as complete narrative experiences.

---

## Interpolation Rationale

```
H₂₉ (500s) ←──── H₃₀ (700s) ────→ H₃₁ (981s)
   Short piece    Medium piece     VS narrative
```

---

## Function

- Medium piece integration
- Extended narrative tracking
- Multi-movement awareness (single movement complete)
- Album track sequences

---

## Musical Relevance

- Symphony movements
- Extended jazz performances
- Rock suites (e.g., "Bohemian Rhapsody")
- Progressive compositions

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | scattered | No narrative | < 0.125 |
| 1 | episodic | Weak connection | < 0.25 |
| 2 | linked | Emerging narrative | < 0.375 |
| 3 | flowing | Growing story | < 0.5 |
| 4 | narrative | Normal story | < 0.625 |
| 5 | compelling | Clear arc | < 0.75 |
| 6 | gripping | Strong narrative | < 0.875 |
| 7 | transcendent | Perfect story | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/piece_scale/h30.py`
