# H₅: 150ms — Theta Mid (Interpolated)

**Window Index**: 5
**Duration**: 150ms (~6.7 Hz)
**Scale**: Theta
**Neural Basis**: Mid-theta transition
**Status**: Interpolated

---

## Overview

H₅ is an interpolated window between theta low (125ms) and affective entrainment (200ms). It provides smooth coverage for sub-beat processing and transitional temporal features.

---

## Interpolation Rationale

```
H₄ (125ms) ←──── H₅ (150ms) ────→ H₆ (200ms)
   8 Hz             6.7 Hz            5 Hz
   TGC anchor       Transition       Emotion sync
```

---

## Function

- Bridge between theta-gamma coupling and emotion synchronization
- Sub-beat tracking (faster than beat, slower than note)
- Transitional processing between cognitive and affective

---

## Musical Relevance

- Sub-divisions of beat
- Ornament perception
- Grace note timing
- Rhythmic embellishment

---

## Usage

While no dedicated mechanism uses H₅ exclusively, it contributes to smooth temporal gradients in:
- TIH (Temporal Integration Hierarchy) interpolation
- Cross-window averaging for HR⁰ mechanisms

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | empty | No transitional signal | < 0.125 |
| 1 | trace | Minimal activity | < 0.25 |
| 2 | sparse | Low coverage | < 0.375 |
| 3 | partial | Some signal | < 0.5 |
| 4 | present | Normal interpolation | < 0.625 |
| 5 | dense | Good coverage | < 0.75 |
| 6 | rich | Strong transitional | < 0.875 |
| 7 | complete | Full spectrum | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/theta_scale/h5.py`
