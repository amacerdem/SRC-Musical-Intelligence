# motor_preparation -- Appraisal Belief (HGSIC)

**Category**: Appraisal (observe-only)
**Owner**: HGSIC (STU-beta5)

---

## Definition

"Motor cortex preparing for movement at tempo." Observes the current state of premotor preparation for beat-aligned movement. High values indicate that the motor system is actively preparing to move -- premotor cortex has received the groove signal and is generating anticipatory motor plans at the current tempo. This occurs even during passive listening (covert motor entrainment) without overt movement.

---

## Observation Formula

```
# From HGSIC P-layer:
motor_preparation = HGSIC.motor_preparation[P1]  # index [6]

# motor_preparation = sigma(0.4*motor_entrainment + 0.3*f01_beat_gamma + 0.2*f02_meter)
# where motor_entrainment combines groove state with meter context
```

No prediction -- observe-only appraisal. The value represents current premotor readiness state.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| HGSIC P1 | motor_preparation [6] | Premotor preparation state |
| HGSIC E0 | f01_beat_gamma [0] | Beat-level input to motor prep |
| HGSIC E1 | f02_meter_integration [1] | Meter context for motor timing |
| HGSIC E2 | f03_motor_groove [2] | Groove-level motor drive |

---

## Kernel Usage

The motor_preparation appraisal feeds F9 social coordination:

```python
# F9 Social:
# Motor readiness enables synchronized interpersonal movement
# motor_preparation -> social_coordination context
```

---

## Scientific Foundation

- **Grahn & Brett 2007**: SMA Z=5.03, premotor PMd Z=5.30 activated by beat-inducing rhythms even without movement (fMRI, N=27)
- **Ross & Balasubramaniam 2022**: Sensorimotor simulation -- motor network engaged during perception without overt movement (Review)
- **Fujioka et al. 2012**: Beta oscillations in SMA reflect internalized timing, modulated by rhythmic stimulus (MEG, N=12)
- **Hoddinott & Grahn 2024**: C-Score model in SMA encodes continuous beat strength during passive listening (7T fMRI RSA, N=26)

## Implementation

File: `Musical_Intelligence/brain/functions/f7/mechanisms/hgsic/` (no dedicated relay -- H3-grounded)
