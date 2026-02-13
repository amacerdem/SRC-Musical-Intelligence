# H₁₇: 1250ms — TIH Macro Scale

**Window Index**: 17
**Duration**: 1250ms (1.25s)
**Scale**: Phrase
**Neural Basis**: Association cortex integration
**Status**: Literature-validated

---

## Overview

H₁₇ captures the macro level of the Temporal Integration Hierarchy — phrase boundary detection. This window integrates multiple beats into coherent musical phrases, marking the transition from rhythm to structure.

---

## Neural Basis

| Region | Function | Evidence |
|--------|----------|----------|
| dlPFC | Working memory integration | Various |
| Parietal | Spatial-temporal mapping | Various |
| Temporal association | Pattern recognition | Various |

---

## HC⁰ Mechanisms Using This Window

| Mechanism | Dimensions | Function |
|-----------|------------|----------|
| **TIH** | macro level parameters | Phrase boundary detection |

**TIH Macro Functions:**
- Phrase boundary detection
- Multi-note pattern integration
- Short-term memory consolidation
- Antecedent phrase recognition

---

## Musical Relevance

- Two-bar phrases
- Antecedent phrases
- Short melodic arcs
- Call phrases (before response)

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | continuous | No phrase sense | < 0.125 |
| 1 | flowing | Minimal boundary | < 0.25 |
| 2 | hinted | Weak phrasing | < 0.375 |
| 3 | suggested | Emerging boundary | < 0.5 |
| 4 | phrased | Normal structure | < 0.625 |
| 5 | articulated | Clear phrases | < 0.75 |
| 6 | punctuated | Strong boundaries | < 0.875 |
| 7 | segmented | Perfect phrasing | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/phrase_scale/h17.py`
