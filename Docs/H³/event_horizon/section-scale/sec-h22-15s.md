# H₂₂: 15s — Verse/Chorus (Interpolated)

**Window Index**: 22
**Duration**: 15000ms (15s)
**Scale**: Section
**Neural Basis**: Section-level memory
**Status**: Interpolated

---

## Overview

H₂₂ is an interpolated window capturing typical verse/chorus duration. This represents the fundamental building block of song-form structure in popular music.

---

## Interpolation Rationale

```
H₂₁ (7.5s) ←──── H₂₂ (15s) ────→ H₂₃ (25s)
   Short section   Verse/Chorus    Extended
```

---

## Function

- Typical verse length
- Chorus duration
- Section-level memory
- 16-bar sections at moderate tempo

---

## Musical Relevance

- Standard verse duration (16 bars at 120 BPM)
- Chorus sections
- Bridge sections (extended)
- Solo sections

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | formless | No section identity | < 0.125 |
| 1 | vague | Weak structure | < 0.25 |
| 2 | outlined | Emerging form | < 0.375 |
| 3 | partial | Moderate identity | < 0.5 |
| 4 | identified | Normal section | < 0.625 |
| 5 | characterized | Clear identity | < 0.75 |
| 6 | memorable | Strong section | < 0.875 |
| 7 | iconic | Perfect section | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/section_scale/h22.py`
