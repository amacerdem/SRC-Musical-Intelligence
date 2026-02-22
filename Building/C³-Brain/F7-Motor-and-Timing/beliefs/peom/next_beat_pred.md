# next_beat_pred -- Anticipation Belief (PEOM)

**Category**: Anticipation (prediction)
**Owner**: PEOM (MPU-alpha1)

---

## Definition

"Next beat will arrive at expected time T." Predicts the timing of the next beat onset based on the entrained motor period. This is the motor system's temporal prediction: given that P(t) has converged to auditory period T, the next beat is expected at time t + T. Period entrainment makes this prediction more precise than phase-based estimates because the fixed period provides a continuous time reference.

---

## Observation Formula

```
# From PEOM F-layer:
next_beat_pred = PEOM.next_beat_pred_T[F0]  # index [9]

# Formula: sigma(0.5 * f01_period_entrainment + 0.5 * beat_periodicity_1s)
# where f01 = period entrainment state
# beat_periodicity_1s = H3 (10, 16, 14, 2)
```

Anticipation beliefs are forward-looking predictions that generate PE when the predicted beat timing mismatches the observed onset.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| PEOM F0 | next_beat_pred_T [9] | Next beat timing prediction |
| PEOM E0 | f01_period_entrainment [0] | Current entrainment state |
| H3 | (10, 16, 14, 2) | Beat periodicity at 1s |
| H3 | (11, 16, 14, 2) | Onset periodicity at 1s |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F3 Attention (SNEM) | Motor timing prediction for beat-aligned salience |
| F6 Reward | PE from temporal prediction feeds reward signal |
| Precision engine | pi_pred estimation via prediction accuracy history |
| F9 Social | Beat prediction for coordinated synchronization |

---

## Scientific Foundation

- **Thaut et al. 2015**: Period locking generates continuous time reference for temporal prediction (Review)
- **Thaut et al. 1998b**: Motor period entrains even during subliminal tempo changes, demonstrating predictive tracking (Behavioral, N=12)
- **Repp 2005**: Period correction mechanism generates anticipatory timing signals (Review)
- **Ross & Balasubramaniam 2022**: Motor simulation supports subsecond beat prediction without overt movement (Review)
- **Nozaradan et al. 2011**: Neural entrainment to beat generates temporal expectations at meter frequencies (EEG, N=14)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/peom_relay.py`
