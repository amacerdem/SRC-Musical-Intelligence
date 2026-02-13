# Section Scale — H₂₁-H₂₄ (7.5-36s)

**Windows**: H₂₁, H₂₂, H₂₃, H₂₄
**Duration Range**: 7.5-36s
**Neural Basis**: Dorsolateral Striatum (DLS), habitual memory
**Cognitive Function**: Verse/chorus perception, procedural memory

---

## Overview

The Section Scale spans verse and chorus durations, where music's formal structure becomes perceivable. This range is associated with the Dorsolateral Striatum (DLS) and habitual/procedural memory — explaining why familiar songs become "automatic" with repeated listening.

---

## Windows in This Scale

| Window | Duration | Status | Primary Use |
|--------|----------|--------|-------------|
| [H₂₁](sec-h21-7500ms.md) | 7.5s | Interpolated | Short section |
| [H₂₂](sec-h22-15s.md) | 15s | Interpolated | Typical verse |
| [H₂₃](sec-h23-25s.md) | 25s | Interpolated | Extended section |
| [H₂₄](sec-h24-36s.md) | 36s | Validated | DLS habitual memory |

---

## Neuroscience Foundation

| Paper | Year | Finding |
|-------|------|---------|
| Hamid et al. | 2024 | DLS encodes short-term reward gradient |
| Mello et al. | 2015 | Striatal time gradient |
| Yin & Knowlton | 2006 | DLS for habitual behavior |

---

## HC⁰ Mechanisms Using This Scale

| Mechanism | Windows | Dimensions |
|-----------|---------|------------|
| **SGM** | H₂₄ | dls_value, dls_habit |

---

## HR⁰ Mechanisms Using This Scale

| Mechanism | Windows | Dimensions |
|-----------|---------|------------|
| **LTI** | H₂₃, H₂₄ | tempo_estimate, tempo_fluctuation |
| **XTI** | H₂₁ | cross_layer dimensions |

---

## Musical Relevance

- **Pre-chorus sections**: Short sections at H₂₁
- **Standard verse/chorus**: 16-bar sections at H₂₂
- **Development sections**: Extended sections at H₂₃
- **Groove habituation**: Automatic response formation at H₂₄

---

## Implementation

```python
SECTION_SCALE = {
    'windows': [21, 22, 23, 24],
    'range_ms': (7500, 36000),
    'brain_regions': ['DLS', 'Putamen', 'Caudate'],
    'striatal_gradient': 'DLS (habitual)',
    'validated': [False, False, False, True]  # Only H₂₄ validated
}
```

---

**Implementation**: `Pipeline/D0/h0/event_horizon/section_scale.py`
