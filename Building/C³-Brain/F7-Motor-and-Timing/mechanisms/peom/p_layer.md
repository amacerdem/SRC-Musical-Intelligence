# PEOM — Cognitive Present

**Model**: Period Entrainment Optimization Model
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 7 | period_lock_strength | Current period-locked neural activity strength. Measures how strongly the motor system is currently locked to the auditory period. Combines entrainment quality with coupling stability. Fujioka 2012: beta oscillations in SMA modulated by rhythmic stimulus frequency. Nozaradan 2011: neural entrainment to beat frequencies. |
| 8 | kinematic_smoothness | Current jerk-reduction metric. Measures the instantaneous smoothness of the velocity profile under period entrainment. Higher values indicate smoother movement with less jerk. Thaut 2015: fixed period CTR reduces jerk; Ross & Balasubramaniam 2022: sensorimotor simulation optimizes subsecond timing. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 16 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 1s — lock stability |
| 1 | 25 | 16 | M21 (zero_crossings) | L2 (bidi) | Coupling phase resets 1s — lock disruptions |

---

## Computation

The P-layer computes the real-time state of the period entrainment system at the current moment:

1. **Period lock strength** (idx 7): Combines f01 (period entrainment) with coupling periodicity at 1s to assess how firmly the motor system is currently locked to the auditory period. Zero-crossings at 1s serve as a negative indicator — more phase resets indicate weaker lock. Maps to beta oscillation modulation in SMA (Fujioka 2012) and frequency-tagged neural entrainment (Nozaradan 2011).

2. **Kinematic smoothness** (idx 8): Combines the velocity profile (M-layer) with coupling stability. High smoothness indicates the motor system has achieved the jerk-minimized state predicted by the continuous time reference theory. Computed as σ(coupling_periodicity + 0.5 * velocity). Maps to cerebellar timing calibration (Thaut 2009b: distinct cortico-cerebellar activations in rhythmic synchronization).

Both outputs are sigmoid-bounded to [0, 1] and represent instantaneous present-state assessments.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_period_entrainment | Entrainment quality feeds lock strength |
| M-layer | velocity | Velocity smoothness feeds kinematic assessment |
| R³ [25:33] | x_l0l5 | Motor-auditory coupling for present-state lock evaluation |
| H³ | 2 tuples (see above) | Coupling periodicity and phase resets for lock assessment |
