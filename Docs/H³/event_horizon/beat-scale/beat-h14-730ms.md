# H₁₄: 730ms — Hippocampal Replay Prediction

**Window Index**: 14
**Duration**: 730ms (~82 BPM)
**Scale**: Beat
**Neural Basis**: Hippocampal sequence replay
**Status**: Literature-validated

---

## Overview

H₁₄ captures the hippocampal replay mechanism — the brain's ability to "preview" upcoming musical events approximately 730ms before they occur. This enables melodic expectation and surprise detection.

---

## Neural Basis

| Region | Function | Evidence |
|--------|----------|----------|
| Hippocampus CA1 | Sequence replay | Diba & Buzsáki 2007 |
| Hippocampus CA3 | Pattern completion | Foster & Wilson 2006 |
| Entorhinal cortex | Temporal context | Bonetti et al. 2024 |

---

## HC⁰ Mechanisms Using This Window

| Mechanism | Dimensions | Function |
|-----------|------------|----------|
| **HRM** | All 8 dimensions | Hippocampal Replay Mechanism |

**HRM Dimensions:**
- replay_strength, compression_ratio
- sequence_accuracy, pattern_match
- prediction_lead, confidence
- novelty_detection, expectation_error

**Key Finding:** Replay occurs at 10-20x temporal compression, enabling the 730ms prediction window.

---

## Scientific Evidence

| Paper | Year | Finding |
|-------|------|---------|
| Bonetti et al. | 2024 | 730ms prediction lead in music listening |
| Diba & Buzsáki | 2007 | 10-20x temporal compression in replay |
| Foster & Wilson | 2006 | Forward and reverse replay |

---

## Musical Relevance

- Melodic expectation (predicting next note)
- Familiar song recognition
- Surprise detection
- Musical memory retrieval

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | unpredicted | No expectation | < 0.125 |
| 1 | vague | Weak prediction | < 0.25 |
| 2 | uncertain | Low confidence | < 0.375 |
| 3 | guessing | Moderate prediction | < 0.5 |
| 4 | expecting | Normal anticipation | < 0.625 |
| 5 | predicting | Good accuracy | < 0.75 |
| 6 | knowing | High confidence | < 0.875 |
| 7 | certain | Perfect prediction | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/beat_scale/h14.py`
