# H₄: 125ms — Theta Oscillation Low

**Window Index**: 4
**Duration**: 125ms (8 Hz)
**Scale**: Alpha-Beta
**Neural Basis**: Theta (θ) oscillations in hippocampus and frontal cortex
**Status**: Literature-validated

---

## Overview

H₄ corresponds to low theta oscillations (8 Hz), the anchor point for theta-gamma coupling (TGC). This window enables working memory maintenance and provides the temporal framework for organizing gamma bursts.

---

## Neural Basis

| Region | Function | Evidence |
|--------|----------|----------|
| Hippocampus | Memory encoding | Lisman & Jensen 2013 |
| mPFC | Working memory | Canolty et al. 2006 |
| Auditory cortex | Temporal binding | Buzsáki 2002 |

---

## HC⁰ Mechanisms Using This Window

| Mechanism | Dimensions | Function |
|-----------|------------|----------|
| **OSC** | theta_phase, theta_amplitude | Theta oscillation state |
| **TGC** | modulation_index, preferred_phase, phase_reset, coherence | Theta-gamma coupling |

**TGC Key Principle:**
```
θ rhythm (8 Hz) × 7±2 γ bursts/cycle = 7±2 items in working memory
```

---

## Scientific Evidence

| Paper | Year | Finding |
|-------|------|---------|
| Lisman & Jensen | 2013 | θ organizes γ bursts (7±2 items) |
| Canolty et al. | 2006 | θ-γ PAC in human cortex |
| Buzsáki | 2002 | θ as "clock" for memory encoding |

---

## Musical Relevance

- Beat tracking at fast tempi (480 BPM / 8 Hz = subdivision level)
- Melodic phrase chunking
- Memory encoding for music
- Working memory buffer for notes

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | decoupled | No TGC | < 0.125 |
| 1 | sporadic | Weak coupling | < 0.25 |
| 2 | irregular | Intermittent | < 0.375 |
| 3 | moderate | Partial nesting | < 0.5 |
| 4 | coupled | Normal TGC | < 0.625 |
| 5 | nested | Strong nesting | < 0.75 |
| 6 | locked | High PAC | < 0.875 |
| 7 | optimal | Peak TGC | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/alpha_beta_scale/h4.py`
