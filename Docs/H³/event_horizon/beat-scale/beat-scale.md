# Beat Scale — H₁₂-H₁₆ (525-1000ms)

**Windows**: H₁₂, H₁₃, H₁₄, H₁₅, H₁₆
**Duration Range**: 525-1000ms
**Neural Basis**: Basal ganglia, cerebellum, hippocampal replay
**Cognitive Function**: Rhythm perception, groove, interval timing

---

## Overview

The Beat Scale is the heart of rhythm perception, spanning from tension-prediction cycles through beat anticipation, hippocampal replay, groove experience, and interval timing. This scale contains the most mechanisms and represents the sweet spot for human rhythm perception (60-120 BPM).

---

## Windows in This Scale

| Window | Duration | Tempo | Primary Use |
|--------|----------|-------|-------------|
| [H₁₂](beat-h12-525ms.md) | 525ms | 114 BPM | ITPRA tension-prediction |
| [H₁₃](beat-h13-600ms.md) | 600ms | 100 BPM | Beat anticipation |
| [H₁₄](beat-h14-730ms.md) | 730ms | 82 BPM | Hippocampal replay |
| [H₁₅](beat-h15-800ms.md) | 800ms | 75 BPM | Groove sweet spot |
| [H₁₆](beat-h16-1000ms.md) | 1000ms | 60 BPM | Delta/interval timing |

---

## Neuroscience Foundation

| Paper | Year | Finding |
|-------|------|---------|
| Huron | 2006 | ITPRA model of expectation |
| Salimpoor et al. | 2013 | Caudate for anticipation |
| Fujioka et al. | 2012 | β peaks -140ms before beat |
| Bonetti et al. | 2024 | 730ms hippocampal prediction lead |
| Janata et al. | 2012 | 800ms optimal for groove |
| Merchant et al. | 2013 | Cerebellar interval timing |

---

## HC⁰ Mechanisms Using This Scale

| Mechanism | Windows | Dimensions |
|-----------|---------|------------|
| **CPD** | H₁₂, H₁₅ | tension_level, prediction_confidence, reaction_intensity |
| **PTM** | H₁₃ | All 8 dimensions |
| **HRM** | H₁₄ | All 8 dimensions |
| **GRV** | H₁₅ | movement_urge, body_specificity, groove_pleasure |
| **OSC** | H₁₆ | delta_phase, delta_amplitude |
| **ITM** | H₁₆ | All 8 dimensions |
| **AED** | H₁₆ | arousal_level, valence_state, autonomic_coupling |

---

## Musical Relevance

- **Harmonic tension**: ITPRA cycles at H₁₂
- **March/dance rhythms**: Beat anticipation at H₁₃
- **Melodic expectation**: Hippocampal prediction at H₁₄
- **Dance music**: Groove sweet spot at H₁₅
- **Phrase boundaries**: Delta oscillation at H₁₆

---

## Implementation

```python
BEAT_SCALE = {
    'windows': [12, 13, 14, 15, 16],
    'range_ms': (525, 1000),
    'tempo_bpm': (60, 114),
    'brain_regions': ['Caudate', 'OFC', 'Putamen', 'SMA', 'Hippocampus', 'Cerebellum'],
    'validated': True  # All windows literature-validated
}
```

---

**Implementation**: `Pipeline/D0/h0/event_horizon/beat_scale.py`
