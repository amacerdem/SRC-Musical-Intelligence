# Syllable Scale — H₈-H₁₁ (300-500ms)

**Windows**: H₈, H₉, H₁₀, H₁₁
**Duration Range**: 300-500ms
**Neural Basis**: Stream segregation, motor synchronization
**Cognitive Function**: Auditory scene analysis, motor coupling

---

## Overview

The Syllable Scale spans the critical range for auditory stream segregation (cocktail party effect) and motor synchronization to beats. This is where individual notes begin to form meaningful groupings and where spontaneous movement to music emerges.

---

## Windows in This Scale

| Window | Duration | Status | Primary Use |
|--------|----------|--------|-------------|
| [H₈](syl-h8-300ms.md) | 300ms | Validated | Note-level integration |
| [H₉](syl-h9-350ms.md) | 350ms | Validated | Stream segregation |
| [H₁₀](syl-h10-400ms.md) | 400ms | Interpolated | Extended syllable |
| [H₁₁](syl-h11-500ms.md) | 500ms | Validated | Motor synchronization |

---

## Neuroscience Foundation

| Paper | Year | Finding |
|-------|------|---------|
| Bregman | 1990 | Auditory Scene Analysis framework |
| Micheyl et al. | 2007 | 350ms stream buildup time |
| Snyder & Alain | 2007 | Neural correlates of streaming |
| Repp | 2005 | 500ms optimal for tapping |
| Grahn & Brett | 2007 | BG crucial for beat perception |

---

## HC⁰ Mechanisms Using This Scale

| Mechanism | Windows | Dimensions |
|-----------|---------|------------|
| **TIH** | H₈, H₁₀ | meso scale, association_window |
| **ASA** | H₉ | All 8 dimensions |
| **GRV** | H₁₁ | motor_coupling, beta_anticipation, syncopation_level |
| **C0P** | H₁₁ | All 8 dimensions |

---

## Musical Relevance

- **Melody perception**: Note grouping at H₈
- **Polyphonic voice separation**: Stream analysis at H₉
- **Toe-tapping, head-nodding**: Motor sync at H₁₁
- **Call-response patterns**: Short motif recognition

---

## Implementation

```python
SYLLABLE_SCALE = {
    'windows': [8, 9, 10, 11],
    'range_ms': (300, 500),
    'brain_regions': ['Belt', 'Parabelt', 'STG', 'STS', 'SMA', 'Putamen', 'Cerebellum'],
    'validated': [True, True, False, True]  # H₁₀ interpolated
}
```

---

**Implementation**: `Pipeline/D0/h0/event_horizon/syllable_scale.py`
