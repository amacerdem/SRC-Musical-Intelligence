# driving_signal — Anticipation Belief (AAC)

**Category**: Anticipation (prediction)
**Owner**: AAC (F5)

---

## Definition

"Fast tempo driving ANS arousal." Predicts that current fast tempo will increase autonomic arousal. Tempo is a primary driver of physiological responses to music — fast rhythmic patterns directly elevate heart rate, respiration rate, and skin conductance through sensorimotor coupling, independently of emotional content. This belief captures the motor-autonomic pathway: beat clarity at 350ms (individual onset detection) and 1s (bar-level periodicity) forecast ANS elevation over the next 1-2 seconds.

---

## Observation Formula

```
# From AAC P-layer:
driving_signal = AAC.driving_signal[P1]  # index [10]

# Formula: sigma(0.50 * periodicity_H9 + 0.30 * periodicity_H16 + 0.20 * tempo_signal)
# Based on:
#   H3 (10, 9, 14, 2): spectral_flux periodicity H9 L2 — beat clarity at 350ms
#   H3 (10, 16, 14, 2): spectral_flux periodicity H16 L2 — bar-level periodicity at 1s
#   tempo_signal: derived from H3 periodicity features
```

Anticipation beliefs are forward-looking predictions that generate PE when the predicted tempo-arousal coupling mismatches the observed autonomic response. High driving_signal predicts that the listener's ANS will elevate due to rhythmic entrainment.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| AAC P1 | driving_signal [10] | Tempo-driven ANS prediction |
| H3 | (10, 9, 14, 2) spectral_flux periodicity H9 L2 | Beat clarity at 350ms |
| H3 | (10, 16, 14, 2) spectral_flux periodicity H16 L2 | Bar-level periodicity at 1s |
| AAC F0 | scr_pred_1s [12] | SCR prediction 1s ahead (validation) |
| AAC F1 | hr_pred_2s [13] | HR prediction 2s ahead (validation) |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F7 Motor | Tempo anticipation — motor system prepares for rhythmic engagement based on predicted tempo-arousal coupling |
| F6 Reward | Arousal-reward coupling — predicted ANS elevation feeds anticipatory reward (groove/urge-to-move) |
| Precision engine | pi_pred estimation — high driving_signal increases prediction confidence for emotional_arousal |
| F3 Attention | Rhythmic attention allocation — fast tempo predictions sharpen temporal attention windows |

---

## Scientific Foundation

- **Janata 2012**: Sensorimotor coupling — respiratory entrainment to musical beat; breathing rate increases with tempo independently of emotion (JEPG)
- **Gomez & Danuser 2007**: Tempo drives RespR (r=0.42 arousal factor) independently of valence; fast tempo = higher ANS baseline (multi-ANS, N=48)
- **Salimpoor et al. 2011**: Anticipatory dopamine in caudate 15-30s before peak; ANS composite d=0.71 — autonomic preparation precedes conscious experience (PET, N=8)
- **Laeng 2016**: Pupil dilation onset 200-500ms BEFORE subjective report — ANS preparation precedes awareness (N=24, r=0.56)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/aac_relay.py`
