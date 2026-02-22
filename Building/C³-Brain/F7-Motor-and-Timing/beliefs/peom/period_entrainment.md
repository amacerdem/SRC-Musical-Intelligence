# period_entrainment -- Core Belief (PEOM)

**Category**: Core (full Bayesian PE)
**tau**: 0.65
**Owner**: PEOM (MPU-alpha1)
**Multi-Scale**: 6 horizons, T_char = 600ms

---

## Definition

"Motor period converged to auditory period." Tracks how tightly the internal motor period has locked to the external auditory rhythm. High values indicate the motor system has entrained its oscillation period to the sound's inter-onset interval -- the listener is temporally synchronized. This is the foundational timing belief: period locking (not phase locking) provides a continuous time reference that optimizes downstream velocity and acceleration profiles.

---

## Multi-Scale Horizons

```
H5(46ms)  H7(250ms)  H10(400ms)  H13(600ms)
H18(2s)   H21(8s)
```

T_char = 600ms reflects the characteristic timescale of motor period entrainment (~100 BPM). Short horizons (H5, H7) capture sub-beat motor adjustments; H10-H13 are the primary beat-period scales where dP/dt = alpha * (T - P(t)) converges; H18-H21 capture phrase-level and section-level period stability.

---

## Observation Formula

```
# R3 base:
value = 0.35*tempo_estimate + 0.25*beat_strength
        + 0.25*pulse_clarity + 0.15*regularity

# HMCE blend: 0.70*R3 + 0.30*HMCE_context
#   HMCE = 0.40*A1 + 0.35*STG + 0.25*MTG

# PEOM motor: 0.50*period_lock + 0.30*kinematic + 0.20*beat_pred

# Precision: regularity * onset * amplitude / (H3_std + eps)
```

Relay components: PEOM.period_lock_strength[P0] + PEOM.kinematic_smoothness[P1] + PEOM.next_beat_pred[F0].

---

## Prediction Formula

```
predict = Linear(tau * prev + w_trend * M18 + w_period * M14 + w_ctx * beliefs_{t-1})
```

Standard Bayesian PE cycle with gain = pi_obs / (pi_obs + pi_pred).

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| PEOM E0 | f01_period_entrainment [0] | Primary period lock state |
| PEOM P0 | period_lock_strength [7] | Neural period-lock activity |
| PEOM F0 | next_beat_pred_T [9] | Next beat prediction |
| PEOM M0 | motor_period [3] | Entrained motor period |
| R3 [7] | amplitude | Beat strength proxy |
| R3 [10] | spectral_flux (onset_strength) | Onset component |
| R3 [11] | onset_strength | Beat event detection |
| H3 | (10, 16, 14, 2) | Beat periodicity at 1s |
| H3 | (11, 16, 14, 2) | Onset periodicity at 1s |

---

## Scientific Foundation

- **Thaut et al. 2015**: Period locking (not phase) defines entrainment; CTR optimizes velocity/acceleration (Review)
- **Thaut et al. 1998b**: Motor period entrains to auditory period even during subliminal 2% tempo changes (Behavioral, N=12)
- **Grahn & Brett 2007**: Putamen Z=5.67, SMA Z=5.03 respond specifically to beat (fMRI, N=27)
- **Yamashita et al. 2025**: CV reduction d=-1.10 with gait-synchronized stimulation (RCT, N=16)
- **Tierney & Kraus 2013**: Beat sync ability linked to neural response consistency, r=0.37 (EEG ABR, N=124)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/peom_relay.py`
