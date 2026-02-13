# Theta Scale — H₅-H₇ (150-250ms)

**Windows**: H₅, H₆, H₇
**Duration Range**: 150-250ms
**Frequency Range**: 4-6.7 Hz
**Neural Basis**: Theta (θ) oscillations
**Cognitive Function**: Beat tracking, emotional synchronization

---

## Overview

The Theta Scale spans the mid-theta range crucial for syllable-rate processing, emotional synchronization with music, and theta-gamma nesting for working memory. This scale bridges individual note perception with beat-level organization.

---

## Windows in This Scale

| Window | Duration | Status | Primary Use |
|--------|----------|--------|-------------|
| [H₅](theta-h5-150ms.md) | 150ms | Interpolated | Sub-beat tracking |
| [H₆](theta-h6-200ms.md) | 200ms | Validated | Affective entrainment |
| [H₇](theta-h7-250ms.md) | 250ms | Validated | Syllable segmentation |

---

## Neuroscience Foundation

| Paper | Year | Finding |
|-------|------|---------|
| Janata et al. | 2012 | 200ms lag for emotion tracking |
| Koelsch | 2014 | Amygdala responds within 200ms |
| Giraud & Poeppel | 2012 | θ aligns with syllable rate |
| Lisman & Jensen | 2013 | θ-γ code for 7±2 items |
| Howard et al. | 2003 | θ phase encodes serial position |

---

## HC⁰ Mechanisms Using This Scale

| Mechanism | Windows | Dimensions |
|-----------|---------|------------|
| **AED** | H₆ | emotional_sync, entrainment_strength, emotional_contagion |
| **TIH** | H₆ | parabelt_window, parabelt_coherence |
| **TGC** | H₇ | coupling_strength, nesting_depth, syllable_rate |
| **CPD** | H₇ | imagination_activation |

---

## Musical Relevance

- **Real-time emotional response**: 200ms emotion tracking lag
- **Lyric segmentation**: θ alignment with syllable boundaries
- **Beat grouping**: Compound meter perception
- **Ornament timing**: Grace notes and sub-beat detail

---

## Implementation

```python
THETA_SCALE = {
    'windows': [5, 6, 7],
    'range_ms': (150, 250),
    'frequency_hz': (4, 6.7),
    'brain_regions': ['Amygdala', 'vmPFC', 'STG', 'Hippocampus'],
    'validated': [False, True, True]  # H₅ interpolated
}
```

---

**Implementation**: `Pipeline/D0/h0/event_horizon/theta_scale.py`
