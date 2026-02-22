# period_lock_strength -- Appraisal Belief (PEOM)

**Category**: Appraisal (observe-only)
**Owner**: PEOM (MPU-alpha1)

---

## Definition

"Beat-entrainment neurons maximally coupled." Observes the current strength of period-locked neural activity in the sensorimotor circuit. High values indicate that SMA, putamen, and premotor cortex neurons are tightly synchronized to the auditory beat period -- the motor system is maximally entrained and ready for precisely timed movement.

---

## Observation Formula

```
# Direct read from PEOM P-layer:
period_lock_strength = PEOM.period_lock_strength[P0]  # index [7]

# Computed from: beat periodicity + onset periodicity + coupling
# Reflects current neural phase-locking value (PLV) proxy
```

No prediction -- observe-only appraisal. The value is directly consumed by period_entrainment Core belief's observe() and by the F3 attention system.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| PEOM P0 | period_lock_strength [7] | Primary neural period-lock state |
| H3 | (10, 16, 14, 2) | Beat periodicity at 1s (contributes to P0) |
| H3 | (11, 16, 14, 2) | Onset periodicity at 1s (contributes to P0) |
| H3 | (25, 16, 14, 2) | Motor-auditory coupling periodicity at 1s |

---

## Kernel Usage

The period_lock_strength appraisal serves two purposes:

1. **Core belief input**: period_entrainment observe() reads it as 30% weight
2. **Cross-function feed**: F3 attention reads it to modulate beat-related salience

```python
# period_entrainment observe():
# PEOM motor = 0.50*period_lock + 0.30*kinematic + 0.20*beat_pred
```

---

## Scientific Foundation

- **Grahn & Brett 2007**: Putamen Z=5.67, SMA Z=5.03 for beat-inducing rhythms (fMRI, N=27)
- **Fujioka et al. 2012**: Beta oscillations in SMA modulated by rhythmic stimulus frequency (MEG, N=12)
- **Tierney & Kraus 2013**: Beat synchronization linked to neural response consistency, r=0.37 (EEG ABR, N=124)
- **Thaut et al. 2009b**: Distinct cortico-cerebellar activations in rhythmic synchronization (fMRI, N=12)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/peom_relay.py`
