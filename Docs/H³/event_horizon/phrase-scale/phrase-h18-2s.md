# H₁₈: 2000ms — Short Phrase (Interpolated)

**Window Index**: 18
**Duration**: 2000ms (2s)
**Scale**: Phrase
**Neural Basis**: Working memory buffer
**Status**: Interpolated

---

## Overview

H₁₈ is an interpolated window within the phrase scale, capturing short phrase integration around the "psychological present" (~2-3s). This aligns with Pöppel's research on conscious temporal experience.

---

## Interpolation Rationale

```
H₁₇ (1250ms) ←──── H₁₈ (2s) ────→ H₁₉ (3s)
   TIH macro       Short phrase     Standard phrase
```

---

## HR⁰ Mechanisms Using This Window

| Mechanism | Windows | Function |
|-----------|---------|----------|
| **RTI** | H₁₈, H₁₉ | Real-Time Integration (2.5s center) |

**RTI Interpolation:**
```
RTI characteristic window = 2.5s
H₁₈ (2s) + H₁₉ (3s) → interpolated to 2.5s
```

---

## Musical Relevance

- Four-beat phrases (at moderate tempo)
- Question phrases
- Riff patterns
- Working memory capacity for notes

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | momentary | No phrase memory | < 0.125 |
| 1 | fleeting | Brief retention | < 0.25 |
| 2 | short | Limited buffer | < 0.375 |
| 3 | holding | Moderate memory | < 0.5 |
| 4 | retained | Normal buffer | < 0.625 |
| 5 | sustained | Good retention | < 0.75 |
| 6 | maintained | Strong memory | < 0.875 |
| 7 | present | Full consciousness | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/phrase_scale/h18.py`
