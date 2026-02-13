# H₁₃: 600ms — Predictive Timing Model (Beat Anticipation)

**Window Index**: 13
**Duration**: 600ms (100 BPM)
**Scale**: Beat
**Neural Basis**: BG beta anticipation (-140ms to beat)
**Status**: Literature-validated

---

## Overview

H₁₃ captures the Predictive Timing Model (PTM) — the neural mechanism for beat anticipation. Beta power in the basal ganglia peaks approximately 140ms before expected beats, demonstrating predictive rather than reactive timing.

---

## Neural Basis

| Region | Function | Evidence |
|--------|----------|----------|
| Putamen | Beat timing | Grahn & Rowe 2009 |
| SMA | Motor preparation | Merchant et al. 2015 |
| preSMA | Temporal prediction | Fujioka et al. 2012 |

---

## HC⁰ Mechanisms Using This Window

| Mechanism | Dimensions | Function |
|-----------|------------|----------|
| **PTM** | All 8 dimensions | Predictive Timing Model |

**PTM Dimensions:**
- beat_phase, meter_hierarchy
- anticipation_strength, beta_peak_timing
- synchronization_error, adaptive_correction
- confidence_level, next_beat_prediction

---

## Scientific Evidence

| Paper | Year | Finding |
|-------|------|---------|
| Fujioka et al. | 2012 | β peaks -140ms before expected beat |
| Grahn & Rowe | 2009 | BG essential for beat-based timing |
| Merchant et al. | 2015 | SMA for interval production |

---

## Musical Relevance

- Beat perception at common tempi (100 BPM)
- March and dance rhythms
- Metric strength perception
- Conductor synchronization

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | arrhythmic | No beat sense | < 0.125 |
| 1 | irregular | Weak timing | < 0.25 |
| 2 | unsteady | Fluctuating | < 0.375 |
| 3 | approximate | Rough beat | < 0.5 |
| 4 | steady | Normal timing | < 0.625 |
| 5 | precise | Good accuracy | < 0.75 |
| 6 | locked | High precision | < 0.875 |
| 7 | metronomic | Perfect timing | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/beat_scale/h13.py`
