# statistical_model -- Core Belief (SLEE)

**Category**: Core (full Bayesian PE)
**tau**: 0.88
**Owner**: SLEE (NDU-beta3)
**Multi-Scale**: single-scale (Macro band), T_char = 30s

---

## Definition

"Internalized statistical structure of this music." Tracks how well the listener has built an internal statistical model of the current musical stream -- the distribution of pitch intervals, rhythmic patterns, and spectral regularities. High values indicate a well-established internal model that accurately predicts upcoming events. This statistical learning is enhanced by musical expertise (d=-1.09, Paraskevopoulos 2022), with musicians showing faster and more accurate internalization of musical structure.

---

## Multi-Scale Horizons

```
Single-scale in v1.0 kernel.
T_char = 30s (Macro band -- statistical models build over tens of seconds)
```

When multi-scale is activated (implementation wave 3-5), statistical model building will span Macro horizons reflecting the seconds-to-minutes timescale of pattern extraction and distribution formation.

---

## Observation Formula

```
# SLEE mechanism outputs:
value = 0.40 * f01_statistical_model
      + 0.30 * exposure_model
      + 0.30 * pattern_memory

# f01 = sigma(0.35 * loudness_mean_100ms
#            + 0.35 * amplitude_entropy_100ms)
#   loudness_mean_100ms = H3[(8, 3, 1, 2)]  -- mean loudness at 100ms
#   amplitude_entropy_100ms = H3[(7, 3, 20, 2)]  -- amplitude entropy 100ms
#   Internal distribution representation -- how well the listener
#   has learned the acoustic regularities

# exposure_model = EMA of f01 over session timescale
#   Statistical model building -- accumulates over exposure

# pattern_memory = EMA of pitch_stability with tau=3s
#   Pattern accumulation -- how stable the learned patterns are

# Precision: 1/(std(f01, exposure_model, pattern_memory) + 0.1)
```

---

## Prediction Formula

```
predict = Linear(tau * prev + w_trend * M18 + w_period * M14 + w_ctx * beliefs_{t-1})
```

Standard Bayesian PE cycle with gain = pi_obs / (pi_obs + pi_pred). At tau=0.88, the statistical model has high inertia -- once built, it persists strongly. This reflects how statistical learning creates stable internal representations that resist frame-by-frame perturbation. However, tau=0.88 is the fastest of F8 Core beliefs, recognizing that statistical models do update within a listening session as new patterns are encountered.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SLEE E0 | f01_statistical_model [0] | Internal distribution representation |
| SLEE M0 | exposure_model [4] | Statistical model building via EMA |
| SLEE M1 | pattern_memory [5] | Pattern accumulation via EMA |
| H3 | (8, 3, 1, 2) | Loudness mean at 100ms |
| H3 | (7, 3, 20, 2) | Amplitude entropy at 100ms |
| R3 [24] | pitch_stability | Pitch regularity baseline |

---

## Scientific Foundation

- **Paraskevopoulos et al. 2022**: Musicians > non-musicians in multisensory statistical learning accuracy, Hedges' g=-1.09; t(23)=-2.815, p<0.05 (MEG+PTE, N=25)
- **Bridwell 2017**: Cortical sensitivity to guitar note patterns at 4Hz; 45% amplitude reduction for patterned vs random; MMN correlation r=0.65, p=0.015 (EEG, N=13)
- **Doelling & Poeppel 2015**: Musicians show enhanced cortical entrainment at all tempi (1-8 Hz); years of training correlate with PLV (MEG, N=34)
- **Carbajal & Malmierca 2018**: Predictive coding hierarchy -- SSA to MMN to deviance detection; repetition suppression vs prediction error decomposition

## Implementation

File: `Musical_Intelligence/brain/functions/f8/beliefs/statistical_model.py` (Phase 5)
