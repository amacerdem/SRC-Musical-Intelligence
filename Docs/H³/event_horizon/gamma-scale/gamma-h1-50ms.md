# H₁: 50ms — Beta Oscillation

**Window Index**: 1
**Duration**: 50ms (20 Hz)
**Scale**: Gamma
**Neural Basis**: Beta (β) oscillations in motor and auditory cortex
**Status**: Literature-validated

---

## Overview

H₁ corresponds to beta oscillations (20 Hz), crucial for motor preparation, temporal prediction maintenance, and micro-timing analysis. This window bridges sensory processing with motor preparation.

---

## Neural Basis

| Region | Function | Evidence |
|--------|----------|----------|
| SMA | Motor preparation | Fujioka et al. 2012 |
| PMC | Premotor planning | Engel & Fries 2010 |
| A1 | Auditory prediction | Arnal & Giraud 2012 |
| Thalamus | Timing coordination | Various |

---

## HC⁰ Mechanisms Using This Window

| Mechanism | Dimensions | Function |
|-----------|------------|----------|
| **OSC** | beta_power | Motor-auditory oscillation |
| **BND** | temporal_window, object_formation, gestalt_strength | Temporal binding |
| **TIH** | a1_window, a1_coherence | Primary auditory integration |

---

## Scientific Evidence

| Paper | Year | Finding |
|-------|------|---------|
| Fujioka et al. | 2012 | β power decreases before expected beats |
| Engel & Fries | 2010 | β maintains current cognitive set |
| Arnal & Giraud | 2012 | β carries top-down predictions |

---

## Musical Relevance

- Motor-auditory synchronization
- Beat anticipation at fine scale
- Instrument onset coordination
- Micro-timing sensitivity

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | dormant | No motor prep | < 0.125 |
| 1 | awakening | Trace readiness | < 0.25 |
| 2 | preparing | Low anticipation | < 0.375 |
| 3 | ready | Moderate prep | < 0.5 |
| 4 | active | Normal readiness | < 0.625 |
| 5 | primed | High anticipation | < 0.75 |
| 6 | locked | Strong coupling | < 0.875 |
| 7 | synchronized | Peak beta sync | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/gamma_scale/h1.py`
