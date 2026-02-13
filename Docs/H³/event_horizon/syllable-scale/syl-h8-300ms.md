# H₈: 300ms — TIH Meso Scale

**Window Index**: 8
**Duration**: 300ms (~3.3 Hz)
**Scale**: Syllable
**Neural Basis**: Belt auditory cortex integration
**Status**: Literature-validated

---

## Overview

H₈ captures the meso (note-level) scale of the Temporal Integration Hierarchy. This window integrates individual notes into melodic contours and enables tracking of pitch sequences.

---

## Neural Basis

| Region | Function | Evidence |
|--------|----------|----------|
| Belt | Spectrotemporal integration | Hickok & Poeppel 2007 |
| Parabelt | Pattern recognition | Rauschecker & Scott 2009 |
| STG | Melody tracking | Various |

---

## HC⁰ Mechanisms Using This Window

| Mechanism | Dimensions | Function |
|-----------|------------|----------|
| **TIH** | meso_level parameters | Note-level integration |

**TIH Meso Functions:**
- Melodic contour tracking
- Note-to-note transitions
- Local pitch pattern recognition
- Articulation perception

---

## Scientific Evidence

| Paper | Year | Finding |
|-------|------|---------|
| Hickok & Poeppel | 2007 | Dual-stream model for auditory processing |
| Rauschecker & Scott | 2009 | Ventral stream for "what" processing |

---

## Musical Relevance

- Melody perception
- Note grouping
- Articulation (legato vs staccato)
- Ornament integration

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | isolated | No melodic connection | < 0.125 |
| 1 | sparse | Minimal continuity | < 0.25 |
| 2 | sketchy | Weak contour | < 0.375 |
| 3 | outlined | Partial melody | < 0.5 |
| 4 | melodic | Normal contour | < 0.625 |
| 5 | flowing | Clear line | < 0.75 |
| 6 | shaped | Strong contour | < 0.875 |
| 7 | sculpted | Perfect melodic shape | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/syllable_scale/h8.py`
