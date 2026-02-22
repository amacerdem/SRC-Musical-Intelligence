# prediction_match -- Appraisal Belief (SRP)

**Category**: Appraisal (observe-only)
**Owner**: SRP (ARU-alpha1)

---

## Definition

"Prediction confirmed (+1) / violated (-1)." Observes whether the musical event that just occurred matched or violated the brain's prediction. This is Huron's Prediction (P) response: a phasic signal at event boundaries that evaluates whether the predicted outcome was correct. +1 indicates full confirmation (V->I cadence arrived as expected), -1 indicates complete violation (deceptive cadence V->vi instead of V->I), and 0 indicates partial match or ambiguity.

Prediction match is phasic -- it fires at musical events (~130-250ms before to ~150ms after the event) and returns to zero between events. It is a binary-like judgment, not a graded signal.

---

## Observation Formula

```
# From SRP T-layer (Huron ITPRA):
prediction_match = SRP.prediction_match[T10]  # index [10]

# Range: [-1, +1]
# +1 = prediction fully confirmed
# -1 = prediction fully violated
#  0 = ambiguous / no strong prediction

# Computed from:
# match = tanh(predicted_chord_similarity - surprise_threshold)
# where predicted_chord_similarity compares the expected and actual harmonic event
# and surprise_threshold is adapted by the precision engine

# Kernel usage:
# - Feeds SRP.prediction_error via Schultz RPE computation
# - Feeds SRP.appraisal: sigma(0.4*pleasure + 0.3*prediction_match + 0.3*opioid)
# - Feeds precision engine: pi_pred estimation for reward predictions
```

No prediction -- observe-only appraisal.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SRP T10 | prediction_match [10] | Huron P response (confirmation/violation) |
| SRP C5 | prediction_error [5] | RPE that drives match evaluation |
| HTP | sensory_match | Sensory prediction match from predictive coding unit |
| BCH | consonance_signal | Harmonic prediction quality |

---

## Kernel Usage

The prediction_match appraisal serves three roles in the kernel:

1. **Reward PE computation**: Match/violation determines the sign and magnitude of prediction_error (TD error)
2. **Appraisal computation**: `appraisal = sigma(0.4*pleasure + 0.3*prediction_match + 0.3*opioid_proxy)` -- confirmation enhances positive appraisal
3. **Precision engine**: Match history feeds pi_pred estimation -- consistent matches increase prediction confidence

```python
# In scheduler Phase 5:
# prediction_match feeds both reward PE and conscious appraisal
appraisal = torch.sigmoid(0.4 * pleasure + 0.3 * prediction_match + 0.3 * opioid_proxy)
```

---

## Scientific Foundation

- **Huron 2006**: Prediction (P) response -- phasic evaluation of whether prediction was correct (Sweet Anticipation, MIT Press)
- **Cheung 2019**: Pleasure from low uncertainty + high surprise (prediction violated pleasantly) (fMRI, N=39, d=3.8-8.53)
- **Schultz 2016**: Two-component RPE -- unselective detection (40-120ms) + value-coded prediction match
- **Gold 2019**: Listeners learn to find preferred endings -- prediction match drives learning (fMRI+IDyOM, N=20)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/srp_relay.py`
