# tension -- Core Belief (SRP)

**Category**: Core (full Bayesian PE)
**tau**: 0.55
**Owner**: SRP (ARU-alpha1)
**Multi-Scale**: single-scale (terminal, v1.0 kernel)

---

## Definition

"Something about to happen, I'm tense." Tracks anticipatory arousal -- Huron's Tension (T) response that prepares the organism for an impending musical event. Tension is a negative-valence preparatory state: the autonomic nervous system activates (increased heart rate, skin conductance) as the brain detects signals of approaching significance. Tension is the "coiled spring" before the release.

Tension rises during dominant-7th holds, crescendos toward climax, and dramatic buildups. It drops sharply at resolution (tonic arrival, dynamic release). The tension-resolution arc is the fundamental engine of musical reward: without tension, there is nothing to resolve, and resolution without prior tension produces minimal pleasure.

---

## Multi-Scale Horizons

Single-scale in v1.0 kernel. Multi-scale extension deferred.

When activated (future):
```
T_char = 5s (phrase-level buildup)
Candidate horizons: H18(2s)  H19(3s)  H20(5s)  H22(15s)
```

Tension builds at phrase-to-section timescale, matching the Huron T response onset (seconds before the event) and the caudate DA ramp period.

---

## Observation Formula

```
# Tension from energy buildup + harmonic unresolvedness + uncertainty:
tension = sigma(0.5 * energy_buildup + 0.3 * harmonic_unresolved + 0.2 * uncertainty)
# where:
#   energy_buildup = R3[7] (amplitude) -> H3(H18, M8, L0) -- forward velocity (crescendo)
#   harmonic_unresolved = 1 - consonance_mean (high roughness, far from tonic)
#   uncertainty = R3[22] (distribution_entropy) -> H3(H18, M0, L2) -- spectral unpredictability

# Tension scales with uncertainty * significance (Cheung 2019):
# High uncertainty about what comes next + high significance of outcome = maximum tension

# For deceptive cadences: tension SPIKES further instead of releasing
# (V->vi instead of V->I: prediction violated, wanting extends, resolution delayed)

# Precision: energy_buildup_stability * (1 - consonance_variance)
```

---

## Prediction Formula

```
predict = tau * prev + (1-tau) * baseline + trend + periodicity + context
```

Standard Bayesian PE cycle with gain = pi_obs / (pi_obs + pi_pred). Moderate tau (0.55) reflects that tension builds over seconds but can drop rapidly at resolution -- faster than pleasure (0.7) but slower than prediction_error (0.5).

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SRP T9 | tension [9] | Primary anticipatory arousal state |
| SRP M13 | harmonic_tension [13] | Tonal distance from tonic (unresolvedness) |
| SRP M14 | dynamic_intensity [14] | Energy trajectory (crescendo/decrescendo) |
| SRP N0 | da_caudate [0] | Caudate DA ramp (wanting component of tension) |
| R3 [7] | amplitude | Energy level |
| R3 [22] | distribution_entropy | Uncertainty context |
| R3 [0:7] | consonance group | Harmonic unresolvedness (inverted) |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F3 Attention | Anticipatory arousal modulates salience allocation |
| SRP internal | Tension drives da_caudate ramp and wanting buildup |
| RAM | Caudate + amygdala region activation |
| Output | Tension trajectory for experiential logging |

---

## Scientific Foundation

- **Huron 2006**: Tension (T) response -- preparatory arousal preceding expected musical events (Sweet Anticipation, MIT Press)
- **Cheung 2019**: Tension scales with uncertainty; amygdala, hippocampus, auditory cortex encode uncertainty*surprise interaction (fMRI, N=39)
- **Salimpoor 2011**: Caudate DA ramps 2-30s before peak pleasure, correlating with anticipatory tension (PET, N=8)
- **Howe 2013**: Quasi-hyperbolic DA approach signal scales with proximity * magnitude (in vivo rodent)
- **Sloboda 1991**: Musical triggers of tension include appoggiaturas, held dominants, crescendos (survey, N=83)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/srp_relay.py`
