# trained_timbre_recognition -- Core Belief (TSCP)

**Category**: Core (full Bayesian PE)
**tau**: 0.90
**Owner**: TSCP (SPU-beta2)
**Multi-Scale**: single-scale (Ultra band), T_char = 60s

---

## Definition

"This is MY instrument." Tracks how strongly the listener recognizes the timbre of their trained instrument. High values indicate tight spectral template matching between the current sound and deeply learned instrument representations -- the auditory cortex responds preferentially to the trained timbre. This is one of the clearest demonstrations of experience-driven cortical reorganization in the auditory system.

---

## Multi-Scale Horizons

```
Single-scale in v1.0 kernel.
T_char = 60s (Ultra band -- timbre recognition is deeply learned)
```

When multi-scale is activated (implementation wave 3-5), timbre recognition will span Ultra horizons reflecting the minutes-to-hours timescale of instrument familiarity accumulation.

---

## Observation Formula

```
# TSCP mechanism outputs:
value = 0.40 * f01_trained_timbre_response
      + 0.30 * timbre_identity
      + 0.30 * recognition_quality

# f01 = sigma(0.35 * trist_balance + 0.35 * (1-inharm) * tonalness)
#   trist_balance = 1.0 - std(tristimulus[18:21])
#   Tristimulus energy balance is the harmonic envelope signature
#   of each instrument family

# timbre_identity = sigma(0.40 * trist_balance
#                       + 0.30 * (1-inharmonicity)
#                       + 0.30 * spectral_autocorrelation)
#   Feature binding coherence -- spectral envelope + tristimulus + temporal

# recognition_quality = spectral_envelope x instrument_identity
#   Template matching quality -- how well current timbre matches stored templates

# Precision: 1/(std(f01, timbre_identity, recognition_quality) + 0.1)
```

---

## Prediction Formula

```
predict = Linear(tau * prev + w_trend * M18 + w_period * M14 + w_ctx * beliefs_{t-1})
```

Standard Bayesian PE cycle with gain = pi_obs / (pi_obs + pi_pred). The very high tau=0.90 means the belief is extremely stable -- timbre recognition barely changes frame-to-frame, reflecting deeply learned cortical representations that took years to establish.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| TSCP E0 | f01_trained_timbre_response [0] | Trained instrument cortical enhancement |
| TSCP P0 | recognition_quality [4] | Template matching quality |
| TSCP P2 | timbre_identity [6] | Feature binding coherence |
| TSCP M0 | enhancement_function [3] | Enhancement selectivity (f01 * f02) |
| R3 [18:21] | tristimulus1-3 | Harmonic envelope signature |
| R3 [5] | inharmonicity | Instrument character |
| R3 [14] | tonalness | Harmonic-to-noise ratio |

---

## Scientific Foundation

- **Pantev et al. 2001**: Timbre-specific N1m enhancement -- double dissociation between violinists/trumpeters (MEG, N=17, F(1,15)=28.55, p=.00008)
- **Bellmann & Asano 2024**: ALE meta-analysis of timbre neuroimaging (k=18, N=338) -- 4 clusters in bilateral pSTG/HG/SMG + R anterior insula
- **Alluri et al. 2012**: Naturalistic fMRI (N=11) -- timbral brightness bilateral STG Z=8.13
- **Whiteford et al. 2025**: CONSTRAINT -- N>260, no subcortical musician enhancement (d=-0.064, BF=0.13 for null) -- plasticity must be cortical

## Implementation

File: `Musical_Intelligence/brain/functions/f8/beliefs/trained_timbre_recognition.py` (Phase 5)
