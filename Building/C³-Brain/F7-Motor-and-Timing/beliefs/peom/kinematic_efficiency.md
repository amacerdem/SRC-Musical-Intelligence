# kinematic_efficiency -- Core Belief (PEOM)

**Category**: Core (full Bayesian PE)
**tau**: 0.60
**Owner**: PEOM (MPU-alpha1)
**Multi-Scale**: 4 horizons, T_char = 500ms

---

## Definition

"Movement velocity smooth and optimized." Tracks the degree to which motor kinematics benefit from auditory period entrainment. High values indicate that velocity profiles are smooth (reduced jerk), acceleration is optimized, and the coefficient of variation (CV) of movement timing is reduced below self-paced baseline. A fixed auditory period provides the continuous time reference that enables this kinematic optimization.

---

## Multi-Scale Horizons

```
H5(46ms)  H7(250ms)  H10(400ms)  H13(600ms)
```

T_char = 500ms reflects the characteristic timescale of kinematic optimization. H5 captures micro-adjustments to velocity; H7-H10 are the primary movement planning scales; H13 captures movement sequence optimization across beats.

---

## Observation Formula

```
# From PEOM E-layer + M-layer:
value = 0.40*f02_velocity_optimization + 0.30*velocity + 0.30*kinematic_smoothness

# CV component: f03_variability_reduction (CV_ent < CV_sp)
# Kinematics: v(t) = dx/dt with reduced jerk under fixed period T

# Precision: 1/(std(velocity, smoothness, cv_reduction) + 0.1)
```

Relay components: PEOM.kinematic_smoothness[P1] + PEOM.velocity[M1] + PEOM.cv_reduction[M3].

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
| PEOM E1 | f02_velocity_optimization [1] | Kinematic smoothness via fixed period |
| PEOM E2 | f03_variability_reduction [2] | CV reduction metric |
| PEOM M1 | velocity [4] | Optimized velocity profile |
| PEOM M2 | acceleration [5] | Optimized acceleration profile |
| PEOM M3 | cv_reduction [6] | 1 - (CV_entrained / CV_self_paced) |
| PEOM P1 | kinematic_smoothness [8] | Jerk-reduction metric |
| H3 | (25, 16, 14, 2) | Motor-auditory coupling periodicity at 1s |
| H3 | (25, 3, 14, 2) | Motor-auditory coupling periodicity at 100ms |

---

## Scientific Foundation

- **Thaut et al. 2015**: Fixed period CTR optimizes velocity and acceleration profiles (Review)
- **Yamashita et al. 2025**: CV reduction from 4.51 to 2.80 with rhythmic stimulation, d=-1.10 (RCT, N=16)
- **Repp 2005**: Period correction vs phase correction as distinct mechanisms (Review)
- **Ross & Balasubramaniam 2022**: Sensorimotor simulation supports subsecond timing; motor network engaged during perception (Review)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/peom_relay.py`
