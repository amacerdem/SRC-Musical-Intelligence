# GSSM — Extraction

**Model**: Gait-Synchronized Stimulation Model
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: E — Extraction
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f07_phase_synchronization | Gait-stimulation phase locking. Measures how well stimulation is synchronized to the gait cycle phase. σ(0.40 * step_periodicity_1s + 0.30 * coupling_periodicity_1s). Yamashita 2025: gait-synchronized tACS to M1 phase-locked to heel strike; swing time CV eta_p² = 0.825. |
| 1 | f08_cv_reduction | Stride variability decrease. Tracks the reduction in coefficient of variation of stride time under dual-site stimulation. σ(0.40 * f07 + 0.30 * coupling_periodicity_100ms). Yamashita 2025: stride time CV reduced from 4.51 to 2.80 (d = -1.10, p = 0.014). |
| 2 | f09_balance_improvement | Mini-BESTest score increase. Interaction of phase synchronization and CV reduction producing balance improvement. σ(0.35 * f07 * f08). Yamashita 2025: Mini-BESTest d = 1.05, p = 0.025; CV-balance correlation r = 0.62, p = 0.012. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 3 | M0 (value) | L2 (bidi) | Onset at 100ms — step detection |
| 1 | 10 | 3 | M14 (periodicity) | L2 (bidi) | Step periodicity 100ms — gait rhythm |
| 2 | 10 | 16 | M14 (periodicity) | L2 (bidi) | Step periodicity 1s — stride cycle |
| 3 | 11 | 3 | M0 (value) | L2 (bidi) | Step onset 100ms — heel strike |
| 4 | 11 | 8 | M14 (periodicity) | L2 (bidi) | Gait periodicity 500ms — half-stride |
| 5 | 25 | 3 | M0 (value) | L2 (bidi) | SMA-M1 coupling 100ms — dual-site sync |
| 6 | 25 | 3 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 100ms — phase lock |

---

## Computation

The E-layer implements the core gait-synchronized stimulation mechanism from Yamashita et al. (2025). Three features compute:

1. **Phase synchronization** (f07): Driven by step periodicity at 1s and SMA-M1 coupling periodicity at 1s. Tracks the phase alignment between auditory/stimulation rhythm and the gait cycle. Phase_Lock = cos(phi_gait - phi_stim) approaching 1.0 for perfect synchronization. Yamashita 2025 used individualized stimulation frequency phase-locked to heel strike via pressure sensors.

2. **CV reduction** (f08): Driven by phase synchronization (f07) and coupling periodicity at 100ms. Tracks the stride time variability decrease produced by dual-site stimulation. Yamashita 2025: stride time CV condition x time F(1,14) = 6.27, p = 0.025, eta_p² = 0.309. Real stimulation d = -1.10 vs sham d = 0.24 (n.s.).

3. **Balance improvement** (f09): Interaction term combining f07 and f08. Captures the compound therapeutic effect where gait synchronization plus variability reduction together improve balance. Yamashita 2025: Mini-BESTest d = 1.05; CV-balance correlation r = 0.62 demonstrates the variability-balance coupling.

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [10] | spectral_flux | Step onset detection for gait phase marker |
| R³ [11] | onset_strength | Step event strength for phase locking |
| R³ [25:33] | x_l0l5 | SMA-M1 coupling for dual-site synchronization proxy |
| H³ | 7 tuples (see above) | Multi-scale step periodicity and coupling dynamics |
