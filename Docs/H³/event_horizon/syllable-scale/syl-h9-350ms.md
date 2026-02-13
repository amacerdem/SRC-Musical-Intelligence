# H₉: 350ms — Auditory Stream Segregation

**Window Index**: 9
**Duration**: 350ms (~2.9 Hz)
**Scale**: Syllable
**Neural Basis**: A1 frequency selectivity, attention
**Status**: Literature-validated

---

## Overview

H₉ captures the critical period for auditory stream segregation — the "cocktail party effect." After ~350ms of exposure, the brain begins to separate simultaneous sound sources into distinct perceptual streams.

---

## Neural Basis

| Region | Function | Evidence |
|--------|----------|----------|
| A1 | Frequency selectivity | Snyder & Alain 2007 |
| Belt | Stream formation | Micheyl et al. 2007 |
| STS | Source attribution | Bregman 1990 |

---

## HC⁰ Mechanisms Using This Window

| Mechanism | Dimensions | Function |
|-----------|------------|----------|
| **ASA** | All 8 dimensions | Auditory Scene Analysis |

**ASA Dimensions:**
- stream_count, stream_coherence
- frequency_separation, temporal_continuity
- common_fate, spectral_segregation
- attention_capture, scene_complexity

---

## Scientific Evidence

| Paper | Year | Finding |
|-------|------|---------|
| Bregman | 1990 | Auditory Scene Analysis framework |
| Micheyl et al. | 2007 | 350ms stream buildup time |
| Snyder & Alain | 2007 | Neural correlates of streaming |

---

## Musical Relevance

- Following individual voices in counterpoint
- Bass line perception
- Instrumental texture analysis
- Melody-accompaniment segregation

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | fused | All sounds merged | < 0.125 |
| 1 | blended | Minimal separation | < 0.25 |
| 2 | emerging | Streams forming | < 0.375 |
| 3 | partial | Some segregation | < 0.5 |
| 4 | separated | Normal streaming | < 0.625 |
| 5 | distinct | Clear streams | < 0.75 |
| 6 | isolated | High segregation | < 0.875 |
| 7 | crystallized | Perfect separation | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/syllable_scale/h9.py`
