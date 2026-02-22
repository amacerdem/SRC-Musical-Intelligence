# wanting -- Core Belief (SRP)

**Category**: Core (full Bayesian PE)
**tau**: 0.6
**Owner**: SRP (ARU-alpha1)
**Multi-Scale**: single-scale (terminal, v1.0 kernel)

---

## Definition

"I want more of this music (caudate DA)." Tracks incentive salience -- the dopamine-driven motivational "wanting" that ramps quasi-hyperbolically as expected reward approaches. This is Berridge's wanting signal: it represents approach motivation, not hedonic pleasure. Wanting can exist without liking (earworm you hate) and responds to anticipatory cues.

Wanting is the v1.0 kernel's backward-compatible `reward_valence` belief, now renamed and grounded in the SRP reward pathway. It is the terminal aggregator: its PE computation aggregates prediction errors from ALL 36 Core Beliefs across 8 Functions (F1-F5, F7-F9).

---

## Multi-Scale Horizons

Single-scale in v1.0 kernel. Multi-scale extension deferred.

When activated (future):
```
T_char = 15s (Salimpoor anticipatory window)
Candidate horizons: H22(15s)  H23(25s)  H24(36s)
```

The anticipatory ramp operates at section timescale (15-36s), matching the caudate DA ramp onset observed by Salimpoor 2011 and the quasi-hyperbolic proximity signal modeled by Howe 2013.

---

## Observation Formula

```
# Terminal aggregation -- no direct sensory observation:
observe() = zeros

# Actual wanting computed via RewardAggregator + SRP mechanism:
# Step 1: Aggregate PEs from all 36 Core Beliefs
reward = sum(salience * (1.5*surprise + 0.8*resolution + 0.5*exploration
             - 0.6*monotony) * fam_mod * da_gain)

# Step 2: SRP mechanism computes da_caudate ramp
# da_caudate ramps quasi-hyperbolically toward expected reward (Howe 2013)
# Scales with: proximity * expected_magnitude * prediction_confidence

# Step 3: Wanting from caudate DA
wanting = sigma(BETA_2 * da_caudate)   # BETA_2 = 0.71 (Salimpoor 2011)

# Precision: prediction_match stability * da_caudate_trend
#            Higher when predictions are consistent and ramp is building
```

---

## Prediction Formula

```
predict = tau * prev + (1-tau) * baseline + trend + periodicity + context
```

Standard Bayesian PE cycle with gain = pi_obs / (pi_obs + pi_pred). Because wanting is terminal (single-scale), prediction relies on temporal inertia (tau=0.6) and context from the wanting_ramp anticipation belief (DAED).

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SRP P6 | wanting [6] | Primary wanting state |
| SRP N0 | da_caudate [0] | Caudate DA ramp (anticipatory) |
| SRP C5 | prediction_error [5] | RPE modulates wanting |
| SRP T9 | tension [9] | Anticipatory arousal component |
| DAED | wanting_ramp | Ramp prediction feeds predict() |
| RewardAggregator | all 36 PEs | Terminal aggregation of cross-function PEs |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| Output | Final incentive salience -- behavioral "approach" motivation |
| RAM | Caudate nucleus region activation |
| F10 Clinical | Anhedonia marker (wanting absence in ~5% of population) |

---

## Scientific Foundation

- **Salimpoor 2011**: Caudate DA release during anticipation correlates with pleasure (PET, N=8, r=0.71)
- **Berridge & Robinson 2003**: Wanting is dissociable from liking -- DA-dependent incentive salience
- **Ferreri 2019**: Levodopa causally increases wanting (pharmacology, N=27, Z=2.44, P=0.015)
- **Mas-Herrero 2021**: Pre-experience NAcc activation predicts motivation (TMS+fMRI, N=17, R2=0.47)
- **Howe 2013**: DA ramps quasi-hyperbolically toward expected reward (in vivo rodent)
- **Mohebi et al. 2024**: Striatal gradient of reward time horizons (VS tau=981s, DMS tau=414s)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/srp_relay.py`
