# groove_quality -- Core Belief (HGSIC)

**Category**: Core (full Bayesian PE)
**tau**: 0.55
**Owner**: HGSIC (STU-beta5)
**Multi-Scale**: 4 horizons, T_char = 1s

---

## Definition

"Motor system should move at this groove level." Tracks the integrated groove state emerging from hierarchical beat x meter x motor coupling. High values indicate strong groove -- the compelling urge to move with the music. Groove is NOT a single signal but a multi-scale integration across the dorsal auditory-motor pathway: pSTG high-gamma tracks sound intensity (r=0.49), propagates to motor cortex with 110ms delay (r=0.70), and is modulated by metric structure. Groove follows an inverted-U curve with syncopation complexity.

---

## Multi-Scale Horizons

```
H7(250ms)  H10(400ms)  H13(600ms)  H16(1s)
```

T_char = 1s reflects the bar-level timescale where groove state integrates. H7 captures beat-level pulse; H10-H13 capture metric grouping; H16 is the primary groove integration scale where beat x meter x motor coupling produces the unified groove state.

---

## Observation Formula

```
# Hierarchical integration (HGSIC 3-level cascade):

# Level 1 -- Beat Induction (pSTG, H6=200ms):
f01_beat_gamma = sigma(0.49 * amp_val * loud_val * onset_val)
# 0.49 from Potes 2012 (pSTG high-gamma <-> intensity)

# Level 2 -- Meter Extraction (pSTG + Premotor, H11=500ms):
f02_meter_integration = sigma(0.51 * f01 * energy_periodicity)

# Level 3 -- Motor Groove (Motor cortex, H16=1000ms):
f03_motor_groove = sigma(0.70 * f01 * f02)
# 0.70 from Potes 2012 (auditory-motor coupling)

# Groove index: weighted hierarchical combination
groove_index = (1*f01 + 2*f02 + 3*f03) / 6

# Belief observe: 0.50*groove_index + 0.30*f03 + 0.20*coupling_strength
# Precision: coupling_strength * amplitude_smoothness / (H3_std + eps)
```

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
| HGSIC M0 | groove_index [3] | Integrated groove state |
| HGSIC E2 | f03_motor_groove [2] | Motor-level groove |
| HGSIC M1 | coupling_strength [4] | Auditory-motor coupling |
| HGSIC E0 | f01_beat_gamma [0] | Beat-level gamma tracking |
| HGSIC E1 | f02_meter_integration [1] | Meter-level integration |
| H3 | (7, 16, 15, 0) | Amplitude smoothness at 1s |
| H3 | (22, 11, 14, 2) | Energy change periodicity at 500ms |
| H3 | (7, 16, 18, 0) | Amplitude trend at 1s |

---

## Scientific Foundation

- **Potes et al. 2012**: pSTG high-gamma (70-170 Hz) tracks intensity r=0.49; auditory-motor coupling r=0.70 at 110ms (ECoG, N=8)
- **Grahn & Brett 2007**: Putamen Z=5.67, SMA Z=5.03 for beat-inducing rhythms (fMRI, N=27)
- **Spiech et al. 2022**: Groove follows inverted-U with syncopation, chi2(1)=14.643 (Pupillometry+behavioral, N=30)
- **Hoddinott & Grahn 2024**: C-Score model in SMA/putamen encodes continuous beat strength (7T fMRI RSA, N=26)
- **Large et al. 2023**: Optimal beat 0.5-8 Hz; dynamical systems groove model (Review)

## Implementation

File: `Musical_Intelligence/brain/functions/f7/mechanisms/hgsic/` (no dedicated relay -- H3-grounded)
