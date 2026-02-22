# beat_onset_pred — Anticipation Belief (SNEM)

**Category**: Anticipation (prediction)
**Owner**: SNEM (ASU-α1)

---

## Definition

"Next beat will come at time X." Predicts the timing of the next beat onset approximately 0.5s ahead. This is the fundamental temporal prediction of entrainment: a periodic internal clock synchronized to external rhythm.

---

## Observation Formula

```
# From SNEM F-layer:
beat_onset_pred = SNEM.beat_onset_pred[F0]  # index [9]

# Formula: sigma(0.5 * f01_beat + 0.5 * beat_periodicity_1s)
# where f01_beat = SNEM E0:beat_entrainment
# beat_periodicity_1s = H³ (10, 16, 14, 2)
```

Anticipation beliefs are forward-looking predictions that generate PE when the predicted beat timing mismatches the observed onset.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SNEM F0 | beat_onset_pred [9] | Next beat prediction |
| SNEM E0 | beat_entrainment [0] | Current beat entrainment |
| H³ | (10, 16, 14, 2) | Beat periodicity at 1s |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F6 Reward | PE from temporal prediction feeds reward signal |
| F7 Motor | Motor preparation timing for beat-aligned movement |
| Precision engine | pi_pred estimation via prediction accuracy |

---

## Scientific Foundation

- **Large & Palmer 2002**: Temporal regularity perception — oscillator-based beat tracking generates predictions
- **Nozaradan 2011**: Neuronal entrainment generates temporal expectations
- **Saadatmehr et al.**: Even premature neonates show beat prediction

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/snem_relay.py`
