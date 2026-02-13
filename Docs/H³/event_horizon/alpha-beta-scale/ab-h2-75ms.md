# H₂: 75ms — Efference Copy Window

**Window Index**: 2
**Duration**: 75ms
**Scale**: Alpha-Beta
**Neural Basis**: Cerebellar forward model, STS prediction
**Status**: Literature-validated

---

## Overview

H₂ captures the efference copy window — the ~75ms delay between motor command and predicted auditory consequence. This mechanism allows musicians to distinguish self-generated sounds from external sounds.

---

## Neural Basis

| Region | Function | Evidence |
|--------|----------|----------|
| Cerebellum | Forward model | Wolpert et al. 1998 |
| STS | Prediction comparison | Eliades & Wang 2024 |
| Auditory cortex | Expectation matching | Blakemore et al. 2001 |

---

## HC⁰ Mechanisms Using This Window

| Mechanism | Dimensions | Function |
|-----------|------------|----------|
| **EFC** | All 8 dimensions | Efference copy processing |

**EFC Dimensions:**
- motor_command, predicted_consequence
- actual_feedback, prediction_error
- suppression_gain, forward_model_update
- timing_precision, confidence

---

## Scientific Evidence

| Paper | Year | Finding |
|-------|------|---------|
| Eliades & Wang | 2024 | 75ms motor-auditory delay |
| Wolpert et al. | 1998 | Forward models in cerebellum |
| Blakemore et al. | 2001 | Self-tickle impossible due to prediction |

---

## Musical Relevance

- Musician's self-monitoring
- Ensemble timing adjustment
- Performance error detection
- Self vs. other sound discrimination

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | unmonitored | No self-tracking | < 0.125 |
| 1 | passive | Minimal monitoring | < 0.25 |
| 2 | aware | Low prediction | < 0.375 |
| 3 | tracking | Moderate forward model | < 0.5 |
| 4 | monitoring | Normal efference | < 0.625 |
| 5 | precise | Accurate prediction | < 0.75 |
| 6 | expert | High precision | < 0.875 |
| 7 | virtuoso | Perfect self-model | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/alpha_beta_scale/h2.py`
