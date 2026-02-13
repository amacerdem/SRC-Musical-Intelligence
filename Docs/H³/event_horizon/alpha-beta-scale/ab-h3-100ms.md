# H₃: 100ms — Alpha Oscillation

**Window Index**: 3
**Duration**: 100ms (10 Hz)
**Scale**: Alpha-Beta
**Neural Basis**: Alpha (α) oscillations in parietal and auditory cortex
**Status**: Literature-validated

---

## Overview

H₃ corresponds to alpha oscillations (10 Hz), the primary mechanism for attention gating. Alpha power inversely relates to attention — suppressed alpha indicates focused processing.

---

## Neural Basis

| Region | Function | Evidence |
|--------|----------|----------|
| Parietal | Attention control | Jensen & Mazaheri 2010 |
| FEF | Eye/attention direction | Klimesch et al. 2007 |
| A1 | Sensory gating | eLife 2019 |
| Thalamus | Attention relay | Various |

---

## HC⁰ Mechanisms Using This Window

| Mechanism | Dimensions | Function |
|-----------|------------|----------|
| **OSC** | alpha_power, alpha_suppression | Oscillatory state |
| **ATT** | All 8 dimensions | Attention mechanism |
| **NPL** | All 8 dimensions | Neural phase-locking |
| **BND** | cross_modal | Cross-modal binding |
| **TIH** | belt_window, belt_coherence | Belt auditory integration |

---

## Scientific Evidence

| Paper | Year | Finding |
|-------|------|---------|
| Jensen & Mazaheri | 2010 | α inhibits task-irrelevant regions |
| Klimesch et al. | 2007 | α power inversely related to attention |
| eLife | 2019 | α suppression gates beat perception |

---

## Musical Relevance

- Selective attention to melody vs accompaniment
- Rhythmic attention fluctuation
- Audio-visual integration for performance
- Focused listening states

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | unfocused | High alpha (distracted) | < 0.125 |
| 1 | diffuse | Scattered attention | < 0.25 |
| 2 | wandering | Low focus | < 0.375 |
| 3 | moderate | Partial attention | < 0.5 |
| 4 | attending | Normal focus | < 0.625 |
| 5 | focused | Good suppression | < 0.75 |
| 6 | absorbed | High focus | < 0.875 |
| 7 | entranced | Deep attention | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/alpha_beta_scale/h3.py`
