# PEOM — Temporal Integration

**Model**: Period Entrainment Optimization Model
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: M — Temporal Integration
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 3 | motor_period | Entrained motor period (normalized). Motor period P(t) converging to auditory period T via dP/dt = alpha * (T - P(t)), with tau = 4.0s integration window. Maps to SMA/putamen beat period locking. Grahn & Brett 2007: putamen Z=5.67. |
| 4 | velocity | Optimized velocity profile. Kinematic v(t) = dx/dt with reduced jerk under fixed period entrainment. Maps to premotor cortex (PMd) velocity planning. Thaut 2015: CTR optimizes velocity profiles. |
| 5 | acceleration | Optimized acceleration profile. Kinematic a(t) = d²x/dt² optimized by fixed period. Smooth acceleration follows from reduced jerk when period is stable. Maps to cerebellum motor timing error correction. |
| 6 | cv_reduction | Coefficient of variation reduction. 1 - (CV_entrained / CV_self_paced). Directly derived from f03 variability reduction. Yamashita 2025: d = -1.10, eta_p² = 0.309. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 7 | 16 | M1 (mean) | L2 (bidi) | Mean amplitude over 1s — motor drive baseline |
| 1 | 8 | 8 | M1 (mean) | L0 (fwd) | Mean loudness over 500ms — intensity integration |
| 2 | 21 | 4 | M8 (velocity) | L0 (fwd) | Tempo velocity at 125ms — period rate change |
| 3 | 21 | 16 | M1 (mean) | L0 (fwd) | Mean tempo change at 1s — drift tracking |

---

## Computation

The M-layer implements the mathematical model of period entrainment kinematics from Thaut et al. (2015). Four quantities are computed:

1. **Motor period** (idx 3): Tracks the entrained motor period using the primary equation dP/dt = tau^-1 * (T - P(t)) where tau = 4.0s. Integrates mean amplitude (1s) and loudness (500ms) as motor drive signals. Period converges to auditory target T.

2. **Velocity** (idx 4): Computes the optimized velocity profile v(t) = dx/dt. Under stable period locking, the velocity profile becomes smooth with reduced jerk. Uses tempo velocity at 125ms for fine-grained dynamics.

3. **Acceleration** (idx 5): Derives the optimized acceleration a(t) = d²x/dt² from the velocity profile. Smooth acceleration results from the fixed period providing a continuous time reference.

4. **CV reduction** (idx 6): Directly inherits from f03 (E-layer variability reduction). Represents the normalized decrease in coefficient of variation: 1 - (CV_entrained / CV_self_paced). Clinical validation: stride time CV drops from 4.51% to 2.80% with rhythmic cueing.

All outputs are sigmoid-bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01, f02, f03 | Period entrainment, velocity optimization, variability reduction feed mathematical integration |
| R³ [7] | amplitude | Motor drive signal for period tracking |
| R³ [8] | loudness | Perceptual intensity for motor drive |
| R³ [21] | spectral_change | Tempo dynamics for period rate change |
| H³ | 4 tuples (see above) | Multi-scale mean and velocity features for temporal integration |
