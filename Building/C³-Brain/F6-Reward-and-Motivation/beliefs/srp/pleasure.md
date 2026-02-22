# pleasure -- Core Belief (SRP)

**Category**: Core (full Bayesian PE)
**tau**: 0.7
**Owner**: SRP (ARU-alpha1)
**Multi-Scale**: single-scale (terminal, v1.0 kernel)

---

## Definition

"My overall pleasure level is X." Tracks the aggregate hedonic state -- a composite of anticipatory wanting and consummatory liking that represents the listener's moment-to-moment subjective pleasure. This is not a single neurochemical signal but a psychological integration: P = 0.84*da_nacc + 0.71*da_caudate, combining both the "about to feel good" (caudate) and "feeling good now" (NAcc) components.

Pleasure has the highest tau among F6 Core beliefs (0.7), reflecting that subjective pleasure evolves slowly -- it does not spike and drop instantaneously but builds, peaks, and decays over seconds, with an afterglow period following peak moments.

---

## Multi-Scale Horizons

Single-scale in v1.0 kernel. Multi-scale extension deferred.

When activated (future):
```
T_char = 5s (broad pleasure envelope)
Candidate horizons: H18(2s)  H20(5s)  H21(8s)
```

Pleasure operates at a broader timescale than either wanting or liking individually, integrating anticipatory and consummatory components into a smooth envelope.

---

## Observation Formula

```
# Composite from SRP Salimpoor coefficients:
pleasure = clamp(BETA_1 * da_nacc + BETA_2 * da_caudate, 0, 1)
# where:
#   BETA_1 = 0.84 (Salimpoor 2011: NAcc-BP <-> pleasure, r=0.84)
#   BETA_2 = 0.71 (Salimpoor 2011: Caudate-BP <-> chills, r=0.71)
#   da_nacc  = ventral striatal DA phasic burst (consummation)
#   da_caudate = dorsal striatal DA ramp (anticipation)

# The composite captures the full temporal profile:
# - During anticipation: 0.71*da_caudate dominates (wanting component)
# - At peak moment: 0.84*da_nacc peaks (liking component)
# - Result: broad pleasure envelope spanning anticipation through consummation

# Precision: (wanting_precision + liking_precision) / 2
#            Inherits from both wanting and liking precision signals
```

---

## Prediction Formula

```
predict = tau * prev + (1-tau) * baseline + trend + periodicity + context
```

Standard Bayesian PE cycle with gain = pi_obs / (pi_obs + pi_pred). High tau (0.7) means pleasure is strongly persistent -- once established, it decays slowly, creating the hedonic afterglow observed in fMRI studies.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SRP P8 | pleasure [8] | Primary aggregate hedonic state |
| SRP N0 | da_caudate [0] | Anticipatory DA component (weight 0.71) |
| SRP N1 | da_nacc [1] | Consummatory DA component (weight 0.84) |
| SRP P6 | wanting [6] | Anticipatory wanting (modulates) |
| SRP P7 | liking [7] | Consummatory liking (modulates) |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| Output | Aggregate hedonic state for behavioral output and experience logging |
| RAM | Ventral striatum + OFC region activation |
| SRP T12 | Appraisal computation: appraisal = sigma(0.4*pleasure + 0.3*prediction_match + 0.3*opioid) |
| F10 Clinical | Therapeutic benefit monitoring -- pleasure trajectory correlates with engagement |

---

## Scientific Foundation

- **Salimpoor 2011**: Pleasure correlates with both caudate (r=0.71) and NAcc (r=0.84) DA release (PET, N=8)
- **Mas-Herrero 2021**: Pre-experience NAcc predicts motivation (R2=0.47), experience NAcc predicts pleasure (R2=0.44)
- **Ferreri 2019**: DA causally modulates BOTH wanting AND liking for music -- challenging strict dissociation for abstract rewards
- **Salimpoor 2013**: NAcc-STG connectivity predicts how much listeners would PAY for novel music (fMRI, N=19)
- **Blood & Zatorre 2001**: Ventral striatum, midbrain (VTA), OFC correlate linearly with chill intensity (PET, N=10)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/srp_relay.py`
