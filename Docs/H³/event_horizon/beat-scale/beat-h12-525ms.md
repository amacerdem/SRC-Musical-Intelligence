# H₁₂: 525ms — CPD Tension-Prediction (ITPRA T-P)

**Window Index**: 12
**Duration**: 525ms (~114 BPM)
**Scale**: Beat
**Neural Basis**: Striatal prediction, cortical tension tracking
**Status**: Literature-validated

---

## Overview

H₁₂ captures the Tension (T) and Prediction (P) stages of the ITPRA model. This window tracks harmonic tension and prediction confidence during the anticipation phase before musical resolution.

---

## Neural Basis

| Region | Function | Evidence |
|--------|----------|----------|
| Caudate | Prediction coding | Salimpoor et al. 2013 |
| OFC | Valuation | Cheung et al. 2019 |
| ACC | Tension monitoring | Huron 2006 |

---

## HC⁰ Mechanisms Using This Window

| Mechanism | Dimensions | Function |
|-----------|------------|----------|
| **CPD** | tension_level, prediction_confidence, peak_buildup | ITPRA Tension-Prediction |

**ITPRA Model:**
```
I (Imagination) → T (Tension) → P (Prediction) → R (Reaction) → A (Appraisal)
                      ↑
                   H₁₂ captures T-P
```

---

## Scientific Evidence

| Paper | Year | Finding |
|-------|------|---------|
| Huron | 2006 | ITPRA model of musical expectation |
| Salimpoor et al. | 2013 | Caudate encodes anticipation value |
| Cheung et al. | 2019 | Surprise + uncertainty → pleasure |

---

## Musical Relevance

- Harmonic tension perception
- Melodic expectation building
- Climax anticipation
- Suspense in music

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | resolved | No tension | < 0.125 |
| 1 | stable | Minimal anticipation | < 0.25 |
| 2 | emerging | Building slightly | < 0.375 |
| 3 | moderate | Growing tension | < 0.5 |
| 4 | tense | Normal anticipation | < 0.625 |
| 5 | mounting | Strong buildup | < 0.75 |
| 6 | critical | High tension | < 0.875 |
| 7 | climactic | Peak anticipation | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/beat_scale/h12.py`
