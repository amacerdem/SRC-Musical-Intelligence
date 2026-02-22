# catchiness_pred — Anticipation Belief (NSCP)

**Category**: Anticipation (prediction)
**Owner**: NSCP (MPU-gamma1)

---

## Definition

"Music will synchronize listeners -> popular." Predicts whether the current musical passage will produce population-level neural synchrony sufficient to drive commercial success. High catchiness prediction indicates the music possesses acoustic features (beat regularity, onset periodicity, harmonic consonance) that reliably entrain listeners' brains across a population.

---

## Observation Formula

```
# From NSCP F-layer:
catchiness_pred = NSCP.catchiness_pred[F2]  # index [10]

# Formula: sigma(0.5 * f24_catchiness_index + 0.5 * onset_period_1s)
# where f24 = sigma(0.35 * f22_neural_synchrony + 0.35 * onset_period_1s + 0.30 * loudness_entropy)
# onset_period_1s = H3 (10, 16, 14, 2) -- spectral_flux periodicity at 1s
```

Anticipation beliefs are forward-looking predictions. catchiness_pred generates PE when predicted catchiness mismatches observed neural synchrony levels.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| NSCP F2 | catchiness_pred [10] | Catchiness trajectory prediction |
| NSCP E2 | f24_catchiness_index [2] | Population motor response index |
| H3 | (10, 16, 14, 2) | Onset periodicity at 1s |
| H3 | (8, 3, 20, 2) | Loudness entropy at 100ms |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F6 Reward | PE from catchiness prediction feeds reward signal |
| neural_synchrony (Core) | Feeds predict() for ISC anticipation |
| Precision engine | pi_pred estimation via prediction accuracy |

---

## Scientific Foundation

- **Leeuwis 2021**: ISC predicts streaming success; R2=0.404 early, R2=0.619 combined (EEG, N=30)
- **Spiech 2022**: Pupil drift rate indexes groove; inverted-U for syncopation (pupillometry, N=30)
- **Berns 2010**: NAcc activity predicts future song sales (fMRI, N=27)

## Implementation

File: `Musical_Intelligence/brain/functions/f9/mechanisms/nscp.py`
