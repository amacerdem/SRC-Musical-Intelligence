# Structural Scale — H₂₅-H₂₈ (100-414s)

**Windows**: H₂₅, H₂₆, H₂₇, H₂₈
**Duration Range**: 100-414s (1.7-7 minutes)
**Neural Basis**: Dorsomedial Striatum (DMS), goal-directed cognition
**Cognitive Function**: Movement form, compositional structure

---

## Overview

The Structural Scale spans movement-level durations in classical music and complete song forms in popular music. This range is associated with the Dorsomedial Striatum (DMS) and goal-directed cognition — where listeners actively track musical narrative and compositional intent.

---

## Windows in This Scale

| Window | Duration | Status | Primary Use |
|--------|----------|--------|-------------|
| [H₂₅](str-h25-100s.md) | 100s | Interpolated | Movement introduction |
| [H₂₆](str-h26-200s.md) | 200s | Interpolated | Song-length form |
| [H₂₇](str-h27-300s.md) | 300s | Interpolated | Extended movement |
| [H₂₈](str-h28-414s.md) | 414s | Validated | DMS goal-directed |

---

## Neuroscience Foundation

| Paper | Year | Finding |
|-------|------|---------|
| Hamid et al. | 2024 | DMS encodes medium-term goals |
| Balleine & O'Doherty | 2010 | DMS for goal-directed action |
| Yin et al. | 2005 | DMS-DLS functional distinction |

---

## HC⁰ Mechanisms Using This Scale

| Mechanism | Windows | Dimensions |
|-----------|---------|------------|
| **SGM** | H₂₈ | dms_value, dms_goal |

---

## HR⁰ Mechanisms Using This Scale

| Mechanism | Windows | Dimensions |
|-----------|---------|------------|
| **GTI** | H₂₅ | global temporal integration |
| **FTO** | H₂₅, H₂₆ | form-temporal organization |

---

## Musical Relevance

- **Symphony introductions**: Movement-level at H₂₅
- **Pop song forms**: Complete verse-chorus-verse at H₂₆
- **Sonata expositions**: Classical form at H₂₇
- **Musical narrative**: Compositional intent tracking at H₂₈

---

## Implementation

```python
STRUCTURAL_SCALE = {
    'windows': [25, 26, 27, 28],
    'range_ms': (100000, 414000),
    'range_minutes': (1.7, 6.9),
    'brain_regions': ['DMS', 'Caudate', 'mPFC'],
    'striatal_gradient': 'DMS (goal-directed)',
    'validated': [False, False, False, True]  # Only H₂₈ validated
}
```

---

**Implementation**: `Pipeline/D0/h0/event_horizon/structural_scale.py`
