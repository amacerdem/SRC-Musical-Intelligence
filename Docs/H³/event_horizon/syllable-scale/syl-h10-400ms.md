# H₁₀: 400ms — Syllable Integration (Interpolated)

**Window Index**: 10
**Duration**: 400ms (2.5 Hz)
**Scale**: Syllable
**Neural Basis**: Association cortex
**Status**: Interpolated

---

## Overview

H₁₀ is an interpolated window between stream segregation (350ms) and motor synchronization (500ms). It provides coverage for extended syllable processing and short motif recognition.

---

## Interpolation Rationale

```
H₉ (350ms) ←──── H₁₀ (400ms) ────→ H₁₁ (500ms)
   ASA             Extended          Motor sync
   Streaming       syllable          C⁰ projection
```

---

## HC⁰ Mechanisms Using This Window

| Mechanism | Dimensions | Function |
|-----------|------------|----------|
| **TIH** | association_window, association_coherence | Association cortex integration |

---

## Function

- Bridge between streaming and motor synchronization
- Extended syllable processing
- Phrase fragment perception
- Two-note pattern recognition

---

## Musical Relevance

- Two-note phrases
- Call-response patterns at note level
- Short motif recognition
- Interval perception

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | atomic | Individual notes only | < 0.125 |
| 1 | paired | Minimal pairing | < 0.25 |
| 2 | linked | Weak connection | < 0.375 |
| 3 | associated | Moderate linking | < 0.5 |
| 4 | connected | Normal association | < 0.625 |
| 5 | bound | Strong pairing | < 0.75 |
| 6 | unified | High integration | < 0.875 |
| 7 | fused | Perfect binding | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/syllable_scale/h10.py`
