# H₇: 250ms — Theta Oscillation High

**Window Index**: 7
**Duration**: 250ms (4 Hz)
**Scale**: Theta
**Neural Basis**: Theta (θ) oscillations at syllable rate
**Status**: Literature-validated

---

## Overview

H₇ corresponds to high theta oscillations (4 Hz), aligning with the syllable rate in speech and the fundamental chunking rate for auditory working memory. This is where individual sounds become grouped into meaningful units.

---

## Neural Basis

| Region | Function | Evidence |
|--------|----------|----------|
| STG | Syllable processing | Giraud & Poeppel 2012 |
| Hippocampus | Sequence encoding | Lisman & Jensen 2013 |
| Frontal cortex | Working memory | Howard et al. 2003 |

---

## HC⁰ Mechanisms Using This Window

| Mechanism | Dimensions | Function |
|-----------|------------|----------|
| **TGC** | coupling_strength, nesting_depth, syllable_rate | Extended theta-gamma nesting |
| **CPD** | imagination_activation | ITPRA Imagination stage |

---

## Scientific Evidence

| Paper | Year | Finding |
|-------|------|---------|
| Giraud & Poeppel | 2012 | θ aligns with syllable rate (4-7 Hz) |
| Lisman & Jensen | 2013 | θ-γ code encodes 7±2 items |
| Howard et al. | 2003 | θ phase encodes serial position |

---

## Musical Relevance

- Lyric segmentation and comprehension
- Melodic phrase boundaries
- Beat grouping in compound meters
- Working memory for melodic sequences

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | fragmented | No grouping | < 0.125 |
| 1 | scattered | Weak chunking | < 0.25 |
| 2 | loose | Partial grouping | < 0.375 |
| 3 | forming | Moderate chunking | < 0.5 |
| 4 | grouped | Normal segmentation | < 0.625 |
| 5 | chunked | Strong grouping | < 0.75 |
| 6 | organized | Clear segments | < 0.875 |
| 7 | parsed | Perfect chunking | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/theta_scale/h7.py`
