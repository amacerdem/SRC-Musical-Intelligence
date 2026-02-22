# prediction_error -- Core Belief (SRP)

**Category**: Core (full Bayesian PE)
**tau**: 0.5
**Owner**: SRP (ARU-alpha1)
**Multi-Scale**: single-scale (terminal, v1.0 kernel)

---

## Definition

"Better/worse than expected (delta = R + gamma*V' - V)." Tracks the temporal difference reward prediction error -- the signed discrepancy between expected and received musical reward. This is the Schultz RPE signal: positive delta indicates "better than expected" (phasic DA burst, 14-30 Hz, <200ms), negative delta indicates "worse than expected" (DA dip below ~5 Hz baseline), and zero indicates "exactly as predicted."

Prediction error is the fastest F6 Core belief (tau=0.5), reflecting the rapid phasic nature of the DA RPE signal. It is the core computational variable driving learning: RPE updates prediction models so future similar events produce smaller errors.

**Important distinction**: F6.prediction_error is the reward PE (TD error), distinct from per-belief sensory PEs that each of the 36 Core Beliefs computes individually. The reward PE aggregates surprise across all functions.

---

## Multi-Scale Horizons

Single-scale in v1.0 kernel. Multi-scale extension deferred.

When activated (future):
```
T_char = 200ms (phasic burst duration)
Candidate horizons: H6(200ms)  H7(250ms)  H11(500ms)
```

RPE operates at the beat/note timescale, matching the ~50-110ms latency and <200ms duration of phasic DA bursts (Schultz 2016).

---

## Observation Formula

```
# Schultz TD error:
delta = R(t) + gamma * V(t+1) - V(t)
# where:
#   R(t) = instantaneous reward (from RewardAggregator)
#   gamma = temporal discount factor
#   V(t) = current value estimate
#   V(t+1) = next-step value estimate

# Two-component Schultz response:
# Component 1 (40-120ms): Unselective detection -- sensory intensity
# Component 2 (evolves): Value-coded RPE

# For music specifically (Cheung 2019):
# pleasure = nonlinear f(uncertainty, surprise)
# Peak pleasure at:
#   (1) Low uncertainty + High surprise = "I thought I knew, but WOW"
#   (2) High uncertainty + Low surprise = "I was confused, but it resolved"

# Range: [-1, +1]
# +1 = maximum positive surprise (better than expected)
# -1 = maximum negative surprise (worse than expected)
#  0 = exactly as predicted

# Precision: |delta| * prediction_confidence / (delta_variance + eps)
```

---

## Prediction Formula

```
predict = tau * prev + (1-tau) * baseline + trend + periodicity + context
```

Standard Bayesian PE cycle with gain = pi_obs / (pi_obs + pi_pred). Low tau (0.5) means PE decays quickly -- the phasic burst is brief and the system returns to baseline rapidly. The prediction baseline is zero (no expectation of surprise).

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SRP C5 | prediction_error [5] | Primary RPE signal |
| SRP C3 | vta_drive [3] | VTA->Striatum activation (DA source) |
| SRP T10 | prediction_match [10] | Huron P response (confirmation/violation) |
| RewardAggregator | all 36 PEs | Cross-function surprise aggregation |
| R3 [21] | spectral_flux | Acoustic-level surprise trigger |
| R3 [22] | distribution_entropy | Uncertainty context (Cheung 2019) |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| Output | Reward PE drives learning signal -- updates prediction models |
| RAM | VTA region activation (DA source) |
| F8 Learning | PE magnitude trend feeds statistical_model and expertise_enhancement |
| F4 Memory | Large PE events trigger enhanced episodic encoding (hippocampal) |

---

## Scientific Foundation

- **Schultz 1997, 2016**: Two-component phasic DA: unselective detection (40-120ms) + value-coded RPE (burst 14-30 Hz, <200ms)
- **Cheung 2019**: Pleasure = nonlinear f(uncertainty, surprise); 80,000 chords analyzed (ML+fMRI, N=39, d=3.8-8.53)
- **Gold 2019**: NAcc RPE-related activity; music = neurobiological reward for learning (fMRI+IDyOM, N=20)
- **Salimpoor 2013**: NAcc-STG connectivity predicts reward value of novel music (Science, N=19)
- **Koelsch, Vuust & Friston 2019**: Predictive processes and the peculiar case of music -- PE as core computation

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/srp_relay.py`
