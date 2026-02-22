# salience_network_activation — Core Belief (CSG)

**Category**: Core (full Bayesian PE)
**tau**: 0.3
**Owner**: CSG (ASU-a3)
**Multi-Scale**: 6 horizons, T_char = 400ms

---

## Definition

"Saliency network (ACC/insula) activated." Tracks the graded salience response from consonance level. High dissonance triggers high ACC/anterior insula activation, reflecting the salience network's role in detecting acoustically significant events. This is a Core belief with full Bayesian prediction error cycling.

---

## Multi-Scale Horizons

```
H5(46ms)  H7(250ms)  H10(400ms)  H13(600ms)
H18(2s)   H21(8s)
```

T_char = 400ms reflects the characteristic timescale of salience detection. Short horizons (H5, H7) capture transient salience spikes from onset events; H10 is the primary salience scale; H13-H18 capture sustained salience from harmonic tension; H21 captures section-level salience adaptation.

---

## Observation Formula

```
# Direct read from CSG P-layer and E-layer:
observe = f(
    CSG.salience_network[P0]          # index [6], [0,1]
  + CSG.f07_salience_activation[E0]   # index [0]
)

# Graded salience response from consonance level
# High dissonance -> high ACC/AI activation
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
| CSG P0 | salience_network [6] | Primary salience state from consonance |
| CSG E0 | f07_salience_activation [0] | E-layer raw salience activation |
| R3 [0] | roughness | Dissonance level driving salience |
| R3 [3] | pleasant | Consonance level (inverted salience) |

---

## Kernel Usage

The salience_network_activation Core belief participates in the full Bayesian PE cycle:

```python
# Phase 2 in scheduler:
# Predict from prior + H3 trends
# Observe from CSG relay salience_network
# PE = observe - predict
# Update: gain = pi_obs / (pi_obs + pi_pred)
```

High prediction error when salience changes unexpectedly (e.g., sudden dissonance after consonant passage) drives belief updating and feeds downstream reward computation.

---

## Scientific Foundation

- **Bravo 2017**: Salience network activation from dissonance (d=5.16)
- **Sarasso 2019**: Consonance modulates ERP amplitudes (eta2p=0.685)
- **Salimpoor 2011**: ACC/insula activation during musical salience events (PET)

## Implementation

File: `Musical_Intelligence/brain/kernel/beliefs/salience_network_activation.py`
