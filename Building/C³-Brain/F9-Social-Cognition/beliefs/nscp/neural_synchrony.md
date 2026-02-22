# neural_synchrony — Core Belief (NSCP)

**Category**: Core (full Bayesian PE)
**tau**: 0.65
**Owner**: NSCP (MPU-gamma1)
**Multi-Scale**: single-scale in v1.0, T_char = 5s

---

## Definition

"Brain synchronized with other listeners." Tracks how strongly a listener's neural responses correlate with the population-level response to the same music. High values indicate the listener's brain is responding in lockstep with other listeners -- the hallmark of "catching" music that reliably synchronizes neural activity across individuals.

---

## Multi-Scale Horizons

Single-scale in v1.0 kernel. When activated (waves 3-5):

```
T_char = 5s (Macro band)
```

T_char = 5s reflects the characteristic timescale of inter-subject correlation accumulation. Population-level neural synchrony builds over seconds of shared listening as brains converge on common acoustic features.

---

## Observation Formula

```
# NSCP mechanism outputs:
value = 0.50 * f22_neural_synchrony + 0.30 * isc_magnitude + 0.20 * coherence_level

# f22 = sigma(0.40 * coherence_period_1s + 0.30 * consonance_100ms)
# isc_magnitude = f22 (raw ISC magnitude estimate)
# coherence_level = cross-layer coherence from x_l0l5 periodicity at 1s

# Precision: 1/(std(f22, isc_magnitude, coherence_level) + 0.1)
```

---

## Prediction Formula

```
predict = Linear(tau * prev + w_trend * M18 + w_period * M14 + w_ctx * beliefs_{t-1})
```

Standard Bayesian PE cycle with gain = pi_obs / (pi_obs + pi_pred).

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| NSCP E0 | f22_neural_synchrony [0] | Primary ISC proxy |
| NSCP M0 | isc_magnitude [3] | Raw ISC magnitude |
| NSCP P0 | coherence_level [6] | Cross-layer coherence level |
| H3 | (25, 16, 14, 2) | Coherence periodicity at 1s |
| H3 | (3, 3, 0, 2) | Consonance at 100ms |
| R3 [3] | stumpf | Harmonic consonance for cross-subject consistency |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F6 Reward | PE from neural synchrony feeds reward formula |
| F3 Attention | Population synchrony modulates salience weighting |
| Precision engine | pi_pred estimation from synchrony stability |

---

## Scientific Foundation

- **Leeuwis 2021**: Neural synchrony (ISC) during first listen predicts commercial success; R2=0.404 (EEG, N=30)
- **Hasson 2004**: Intersubject correlation in cortical responses during natural stimuli is reliable and content-driven (fMRI, N=5)
- **Berns 2010**: NAcc activity predicts future song sales; r=0.33 (fMRI, N=27)
- **Sarasso 2019**: Musical consonance enhances motor inhibition and aesthetic engagement; eta2=0.685 (EMG+ERP, N=36)

## Implementation

File: `Musical_Intelligence/brain/functions/f9/beliefs/neural_synchrony.py`
