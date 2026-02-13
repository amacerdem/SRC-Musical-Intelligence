# Alpha-Beta Scale — H₂-H₄ (75-125ms)

**Windows**: H₂, H₃, H₄
**Duration Range**: 75-125ms
**Frequency Range**: 8-13 Hz
**Neural Basis**: Alpha (α) and Theta-low (θ) oscillations
**Cognitive Function**: Attention gating, motor-auditory prediction

---

## Overview

The Alpha-Beta Scale bridges the fast gamma processing with slower theta rhythms. This range is crucial for attention allocation, efference copy computation, and theta-gamma coupling that organizes working memory.

---

## Windows in This Scale

| Window | Duration | Neural Basis | Primary Use |
|--------|----------|--------------|-------------|
| [H₂](ab-h2-75ms.md) | 75ms | Efference copy | Motor → auditory prediction |
| [H₃](ab-h3-100ms.md) | 100ms | α oscillation | Attention gating |
| [H₄](ab-h4-125ms.md) | 125ms | θ low (8Hz) | Working memory anchor |

---

## Neuroscience Foundation

| Paper | Year | Finding |
|-------|------|---------|
| Eliades & Wang | 2024 | 75ms motor-auditory delay |
| Jensen & Mazaheri | 2010 | α inhibits task-irrelevant regions |
| Klimesch et al. | 2007 | α power inversely related to attention |
| Lisman & Jensen | 2013 | θ organizes γ bursts |
| Canolty et al. | 2006 | θ-γ PAC in human cortex |

---

## HC⁰ Mechanisms Using This Scale

| Mechanism | Windows | Dimensions |
|-----------|---------|------------|
| **EFC** | H₂ | All 8 dimensions |
| **OSC** | H₃, H₄ | alpha_power, alpha_suppression, theta_phase |
| **ATT** | H₃ | All 8 dimensions |
| **NPL** | H₃ | All 8 dimensions |
| **BND** | H₃ | cross_modal |
| **TGC** | H₄ | modulation_index, preferred_phase, phase_reset |
| **TIH** | H₃ | belt_window, belt_coherence |

---

## Musical Relevance

- **Musician self-monitoring**: 75ms efference copy window
- **Selective attention**: α suppression for melody vs accompaniment
- **Beat anticipation**: θ-based prediction at fast tempi
- **Memory encoding**: θ phase for melodic chunking

---

## Implementation

```python
ALPHA_BETA_SCALE = {
    'windows': [2, 3, 4],
    'range_ms': (75, 125),
    'frequency_hz': (8, 13),
    'brain_regions': ['Cerebellum', 'STS', 'Parietal', 'FEF', 'Hippocampus', 'mPFC'],
    'validated': True  # All windows literature-validated
}
```

---

**Implementation**: `Pipeline/D0/h0/event_horizon/alpha_beta_scale.py`
