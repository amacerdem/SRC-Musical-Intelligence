# H₁₆: 1000ms — Delta Oscillation / Interval Timing

**Window Index**: 16
**Duration**: 1000ms (1 Hz / 60 BPM)
**Scale**: Beat
**Neural Basis**: Delta (δ) oscillations, scalar timing
**Status**: Literature-validated

---

## Overview

H₁₆ captures delta oscillations (1 Hz) and the interval timing mechanism. This window represents phrase-level structure processing and serves as a fundamental reference for timing (Weber's law: σ = 0.15μ).

---

## Neural Basis

| Region | Function | Evidence |
|--------|----------|----------|
| Cerebellum | Interval timing | Teki et al. 2011 |
| BG | Duration encoding | Merchant et al. 2013 |
| SMA | Timing production | Gibbon et al. 1984 |

---

## HC⁰ Mechanisms Using This Window

| Mechanism | Dimensions | Function |
|-----------|------------|----------|
| **OSC** | delta_phase, delta_amplitude | Delta oscillation state |
| **ITM** | All 8 dimensions | Interval Timing Model |
| **AED** | arousal_level, valence_state, autonomic_coupling, affective_coherence, mood_state | Affective entrainment |

**ITM Dimensions:**
- interval_estimate, timing_variability
- scalar_coefficient, drift_rate
- comparison_result, reference_interval
- motor_preparation, execution_timing

**Weber's Law:**
```
σ = 0.15 × μ

where:
  σ = timing variability
  μ = interval duration
  0.15 = Weber fraction for timing
```

---

## Scientific Evidence

| Paper | Year | Finding |
|-------|------|---------|
| Merchant et al. | 2013 | Cerebellar interval timing |
| Gibbon et al. | 1984 | Scalar timing theory |
| Teki et al. | 2011 | BG vs cerebellum dissociation |

---

## Musical Relevance

- Phrase boundaries
- Breath points
- Slow tempo beats (60 BPM)
- Duration judgment

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | timeless | No duration sense | < 0.125 |
| 1 | vague | Imprecise timing | < 0.25 |
| 2 | approximate | Rough duration | < 0.375 |
| 3 | estimated | Moderate precision | < 0.5 |
| 4 | timed | Normal accuracy | < 0.625 |
| 5 | precise | Good timing | < 0.75 |
| 6 | exact | High precision | < 0.875 |
| 7 | calibrated | Perfect duration | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/beat_scale/h16.py`
