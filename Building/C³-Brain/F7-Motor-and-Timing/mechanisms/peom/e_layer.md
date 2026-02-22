# PEOM — Extraction

**Model**: Period Entrainment Optimization Model
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: E — Extraction
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_period_entrainment | Motor period lock to auditory period. Tracks how the motor system entrains to rhythmic input period (not phase). σ(0.40 * beat_periodicity_1s + 0.35 * onset_periodicity_1s). Thaut 2015: period locking defines entrainment; CTR optimizes velocity/acceleration. Thaut 1998b: motor period entrains even during subliminal 2% tempo changes. |
| 1 | f02_velocity_optimization | Kinematic smoothness via fixed period. Measures velocity profile optimization when period is locked. σ(0.35 * coupling_periodicity_1s). Thaut 2015: fixed period provides CTR that reduces jerk and smooths velocity. Ross & Balasubramaniam 2022: sensorimotor simulation supports subsecond beat timing. |
| 2 | f03_variability_reduction | CV reduction with rhythmic cueing. Interaction of entrainment and velocity optimization producing variability decrease. σ(0.35 * f01 * f02). Yamashita 2025: CV reduction d = -1.10 (large), stride time CV from 4.51 to 2.80. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 3 | M0 (value) | L2 (bidi) | Onset at 100ms alpha |
| 1 | 10 | 3 | M14 (periodicity) | L2 (bidi) | Beat periodicity at 100ms |
| 2 | 10 | 16 | M14 (periodicity) | L2 (bidi) | Beat periodicity at 1000ms |
| 3 | 11 | 3 | M0 (value) | L2 (bidi) | Onset strength at 100ms |
| 4 | 11 | 16 | M14 (periodicity) | L2 (bidi) | Onset periodicity at 1s |
| 5 | 7 | 3 | M0 (value) | L2 (bidi) | Beat amplitude at 100ms |
| 6 | 7 | 3 | M2 (std) | L2 (bidi) | Amplitude variability 100ms |
| 7 | 25 | 3 | M0 (value) | L2 (bidi) | Motor-auditory coupling 100ms |
| 8 | 25 | 3 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 100ms |

---

## Computation

The E-layer implements the core period entrainment mechanism from Thaut et al. (2015, 1998b). Three features compute:

1. **Period entrainment** (f01): Driven by beat periodicity and onset periodicity at 1s horizon. Tracks how motor period P(t) converges to auditory period T via dP/dt = alpha * (T - P(t)). Maps to SMA/putamen period locking (Grahn & Brett 2007: putamen Z=5.67, SMA Z=5.03).

2. **Velocity optimization** (f02): Driven by motor-auditory coupling periodicity at 1s. Fixed period provides a continuous time reference (CTR) that reduces jerk and produces smooth velocity profiles. Maps to premotor cortex velocity planning (PMd Z=5.30).

3. **Variability reduction** (f03): Interaction term combining f01 and f02. Captures the compound effect where period locking plus velocity optimization together produce lower coefficient of variation (CV). Yamashita 2025 provides direct clinical evidence: stride time CV reduced from 4.51 to 2.80 (d=-1.10).

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [7] | amplitude | Beat strength proxy for temporal intensity |
| R³ [10] | spectral_flux | Onset detection for beat marker |
| R³ [11] | onset_strength | Beat event detection for period tracking |
| R³ [25:33] | x_l0l5 | Motor-auditory coupling for continuous time reference |
| H³ | 9 tuples (see above) | Multi-scale beat/onset periodicity and coupling dynamics |
