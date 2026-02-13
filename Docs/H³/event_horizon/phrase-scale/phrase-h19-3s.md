# H₁₉: 3000ms — Phrase Center (Interpolated)

**Window Index**: 19
**Duration**: 3000ms (3s)
**Scale**: Phrase
**Neural Basis**: Extended working memory
**Status**: Interpolated

---

## Overview

H₁₉ is an interpolated window capturing standard phrase duration. This represents the typical length of a complete melodic idea — the "sentence" of musical expression.

---

## Interpolation Rationale

```
H₁₈ (2s) ←──── H₁₉ (3s) ────→ H₂₀ (5s)
   Short phrase   Standard       Extended
```

---

## HR⁰ Mechanisms Using This Window

| Mechanism | Windows | Function |
|-----------|---------|----------|
| **RTI** | H₁₈, H₁₉ | Real-Time Integration |

---

## Function

- Standard phrase processing
- Melodic arc tracking
- Harmonic progression integration
- Complete musical idea

---

## Musical Relevance

- Standard 4-bar phrases at moderate tempo (120 BPM)
- Complete melodic ideas
- Harmonic sequences (I-IV-V-I)
- Lyrical phrases

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | fragmented | No phrase coherence | < 0.125 |
| 1 | sketched | Minimal arc | < 0.25 |
| 2 | outlined | Weak shape | < 0.375 |
| 3 | forming | Emerging phrase | < 0.5 |
| 4 | shaped | Normal arc | < 0.625 |
| 5 | complete | Good phrase | < 0.75 |
| 6 | eloquent | Strong expression | < 0.875 |
| 7 | perfected | Ideal phrase | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/phrase_scale/h19.py`
