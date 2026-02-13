# Gamma Scale — H₀-H₁ (25-50ms)

**Windows**: H₀, H₁
**Duration Range**: 25-50ms
**Frequency Range**: 20-40 Hz
**Neural Basis**: Gamma (γ) and Beta (β) oscillations
**Cognitive Function**: Feature binding, onset detection

---

## Overview

The Gamma Scale represents the fastest temporal resolution in the Event Horizon, corresponding to gamma and high-beta neural oscillations. These windows are critical for feature binding across frequency channels and precise onset detection.

---

## Windows in This Scale

| Window | Duration | Frequency | Neural Basis | Primary Use |
|--------|----------|-----------|--------------|-------------|
| [H₀](gamma-h0-25ms.md) | 25ms | 40 Hz | γ oscillation | Feature binding |
| [H₁](gamma-h1-50ms.md) | 50ms | 20 Hz | β oscillation | Motor preparation |

---

## Neuroscience Foundation

| Paper | Year | Finding |
|-------|------|---------|
| Giraud & Poeppel | 2012 | γ band critical for phonemic processing |
| Lakatos et al. | 2019 | γ oscillations gate sensory input |
| Buzsáki & Wang | 2012 | γ enables local computation |
| Engel & Fries | 2010 | β maintains current cognitive set |
| Arnal & Giraud | 2012 | β carries top-down predictions |

---

## HC⁰ Mechanisms Using This Scale

| Mechanism | Windows | Dimensions |
|-----------|---------|------------|
| **OSC** | H₀, H₁ | gamma_power, beta_power |
| **BND** | H₀, H₁ | binding_strength, gamma_coherence, temporal_window |
| **TGC** | H₀ | gamma_burst |
| **TIH** | H₁ | a1_window, a1_coherence |

---

## Musical Relevance

- **Note attack transients**: 25ms resolution for onset precision
- **Spectral fusion judgments**: Feature binding across harmonics
- **Motor-auditory synchronization**: 50ms preparation window
- **Instrument onset coordination**: Inter-onset timing

---

## Implementation

```python
GAMMA_SCALE = {
    'windows': [0, 1],
    'range_ms': (25, 50),
    'frequency_hz': (20, 40),
    'brain_regions': ['A1', 'Heschl\'s gyrus', 'SMA', 'PMC', 'thalamus'],
    'validated': True  # Both windows literature-validated
}
```

---

**Implementation**: `Pipeline/D0/h0/event_horizon/gamma_scale.py`
