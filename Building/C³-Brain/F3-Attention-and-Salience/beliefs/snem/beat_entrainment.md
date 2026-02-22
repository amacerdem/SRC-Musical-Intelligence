# beat_entrainment — Core Belief (SNEM)

**Category**: Core (full Bayesian PE)
**τ**: 0.35
**Owner**: SNEM (ASU-α1)
**Multi-Scale**: 6 horizons, T_char = 400ms

---

## Definition

"Neural oscillations locked to beat frequency." Tracks how strongly internal oscillatory processes are entrained to the external beat. High values indicate tight phase-locking between neural rhythm and musical beat — the brain is "on the beat."

---

## Multi-Scale Horizons

```
H5(46ms)  H7(250ms)  H10(400ms)  H13(600ms)
H18(2s)   H21(8s)
```

T_char = 400ms reflects the characteristic timescale of beat perception (~120 BPM). Short horizons (H5, H7) capture sub-beat fluctuations; H10 is the primary beat scale; H13–H18 capture bar and phrase-level entrainment stability; H21 captures section-level entrainment persistence.

---

## Observation Formula

```
energy = 0.6 × amplitude + 0.4 × onset
h3_change = max(|vel_amp|, |vel_onset|, |vel_flux|)  # beat scale
            × 0.60 + phrase_scale × 0.40

# 4-signal mixing (with relays):
base = 0.25 × energy + 0.25 × h3_change + 0.15 × |PE_prev| + 0.35 × relay
value = 0.5 × base + 0.5 × max(all signals)   # peak preservation

# SNEM attention gate (multiplicative):
value *= 1 + 0.3 × selective_gain

# Precision: (0.5 × energy + 0.5 × h3_change) × 10, clamped [0.5, 10]
```

Relay components: SNEM.beat_locked[P0] + SNEM.entrainment_strength[P1] + SNEM.beat_onset_pred[F0] + SNEM.meter_position_pred[F1].

---

## Prediction Formula

```
predict = Linear(τ × prev + w_trend × M18 + w_period × M14 + w_ctx × beliefs_{t-1})
```

Standard Bayesian PE cycle with gain = π_obs / (π_obs + π_pred).

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SNEM P0 | beat_locked_activity [6] | Primary beat-lock state |
| SNEM P1 | entrainment_strength [7] | Phase-locking value |
| SNEM F0 | beat_onset_pred [9] | Next beat prediction |
| SNEM F1 | meter_position_pred [10] | Metric hierarchy position |
| R³ [7] | amplitude | Energy component |
| R³ [10] | spectral_flux (onset_strength) | Onset component |

---

## Scientific Foundation

- **Nozaradan 2012**: SS-EPs enhanced at beat/meter > acoustic envelope (N=9, p<0.0001)
- **Grahn & Brett 2007**: Beat perception recruits SMA + basal ganglia (fMRI, N=27)
- **Yang et al. 2025**: PLV=0.76 frontal-parietal at fast tempo (EEG, N=26)
- **Large & Palmer 2002**: Temporal regularity perception — oscillator-based beat tracking

## Implementation

File: `Musical_Intelligence/brain/kernel/beliefs/beat_entrainment.py`
