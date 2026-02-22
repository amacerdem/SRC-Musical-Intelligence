# entrainment_quality — Appraisal Belief (SSRI)

**Category**: Appraisal (observe-only)
**Owner**: SSRI (RPU-beta4)

---

## Definition

"Timing alignment with partner tight." Observes the precision of temporal entrainment between co-performers or co-listeners. High entrainment quality indicates tight phase-locking of motor and neural responses across individuals -- beat onsets, dynamic changes, and gestural timing are precisely aligned. Entrainment quality is a stable individual difference (d=1.37, Wohltjen et al. 2023) and the primary driver of social synchrony reward.

---

## Observation Formula

```
# Direct read from SSRI E-layer:
entrainment_quality = SSRI.f04_entrainment_quality[E3]  # index [3]

# f04 = sigma(0.30 * onset_periodicity_500ms
#            + 0.25 * beat_periodicity_125ms
#            + 0.25 * onset_100ms
#            + 0.20 * energy_velocity_500ms)
```

No prediction -- observe-only appraisal. The value reflects temporal coordination precision at micro-timing (100-125ms) and beat (500ms) scales.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SSRI E3 | f04_entrainment_quality [3] | Temporal entrainment precision |
| H3 | (10, 8, 14, 2) | Onset periodicity at 500ms |
| H3 | (10, 4, 14, 2) | Beat periodicity at 125ms |
| H3 | (10, 3, 0, 2) | Onset value at 100ms |
| H3 | (22, 8, 8, 0) | Energy velocity at 500ms |

---

## Kernel Usage

Entrainment quality feeds motor precision and social reward amplification:

```python
# Phase 3 in scheduler:
# Entrainment quality modulates motor precision
motor_precision_boost = 0.2 * ssri_relay['entrainment_quality']
# Entrainment feeds social amplification ratio
sync_amplification = 1.0 + f01 * (ssri_relay['entrainment_quality'] + f02)
```

---

## Scientific Foundation

- **Wohltjen et al. 2023**: Beat entrainment ability is stable individual difference (d=1.37); predicts interpersonal attentional synchrony with storyteller (behavioral+pupillometry, N=198)
- **Bigand et al. 2025**: mTRF disentangles 4 parallel processes during dyadic dance; social coordination F(1,57)=249.75 (dual-EEG, N=70)
- **Novembre et al. 2012**: Neural entrainment during joint piano performance; motor simulation of partner (EEG)
- **Spiech et al. 2022**: Pupil drift rate indexes groove via inverted U with rhythmic complexity; noradrenergic arousal reflects precision-weighted prediction error (pupillometry, N=30)

## Implementation

File: `Musical_Intelligence/brain/functions/f9/mechanisms/ssri.py`
