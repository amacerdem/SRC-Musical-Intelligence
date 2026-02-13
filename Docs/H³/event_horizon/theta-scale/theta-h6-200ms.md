# H₆: 200ms — Affective Entrainment Sync

**Window Index**: 6
**Duration**: 200ms (5 Hz)
**Scale**: Theta
**Neural Basis**: Amygdala-auditory coupling
**Status**: Literature-validated

---

## Overview

H₆ captures the affective entrainment window — the ~200ms lag between musical events and emotional state updates. This window enables real-time emotional synchronization with music.

---

## Neural Basis

| Region | Function | Evidence |
|--------|----------|----------|
| Amygdala | Emotion processing | Koelsch 2014 |
| vmPFC | Valence computation | Juslin & Västfjäll 2008 |
| Auditory cortex | Music-emotion coupling | Janata et al. 2012 |

---

## HC⁰ Mechanisms Using This Window

| Mechanism | Dimensions | Function |
|-----------|------------|----------|
| **AED** | emotional_sync, entrainment_strength, emotional_contagion | Affective entrainment |
| **TIH** | parabelt_window, parabelt_coherence | Parabelt auditory integration |

---

## Scientific Evidence

| Paper | Year | Finding |
|-------|------|---------|
| Janata et al. | 2012 | 200ms lag for emotion tracking |
| Koelsch | 2014 | Amygdala responds within 200ms to music |
| Juslin & Västfjäll | 2008 | Multiple emotion mechanisms in music |

---

## Musical Relevance

- Real-time emotional response to music
- Tension-release tracking
- Expressive timing perception
- Emotional "chills" preparation

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | detached | No emotional sync | < 0.125 |
| 1 | distant | Minimal affect | < 0.25 |
| 2 | aware | Low entrainment | < 0.375 |
| 3 | responsive | Moderate sync | < 0.5 |
| 4 | engaged | Normal affect | < 0.625 |
| 5 | immersed | Strong entrainment | < 0.75 |
| 6 | moved | High emotion | < 0.875 |
| 7 | transported | Peak affect | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/theta_scale/h6.py`
