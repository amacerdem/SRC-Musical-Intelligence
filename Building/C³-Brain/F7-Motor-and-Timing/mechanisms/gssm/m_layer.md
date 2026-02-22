# GSSM — Temporal Integration

**Model**: Gait-Synchronized Stimulation Model
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: M — Temporal Integration
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 3 | stride_cv | Coefficient of variation of stride time. Continuous estimate of stride-to-stride variability. CV = (SD / Mean) x 100, calculated from stride time intervals. Yamashita 2025: CV measured from 20 stride time steps using heel pressure sensors at 100 Hz. Real stim: 4.51 to 2.80; sham: minimal change. |
| 4 | sma_m1_coupling | SMA-M1 synchronization strength. Measures the dual-site coupling between supplementary motor area and primary motor cortex. Stronger coupling indicates more effective simultaneous stimulation. Yamashita 2025: tDCS (2mA) to SMA (Fz) + gait-synchronized tACS to M1 (1cm lat/post from Cz). |
| 5 | balance_score | Normalized Mini-BESTest score. Clinical balance assessment mapped to [0, 1]. Directly derived from f09 (E-layer). Yamashita 2025: Mini-BESTest d = 1.05; condition x time eta_p² = 0.309. |
| 6 | gait_stability | Overall gait pattern stability. Combined index of phase lock and variability reduction. σ(0.5 * f07 + 0.5 * f08). Represents the global quality of gait pattern under synchronized stimulation. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 7 | 3 | M0 (value) | L2 (bidi) | Step amplitude 100ms — stride force |
| 1 | 7 | 16 | M1 (mean) | L2 (bidi) | Mean amplitude 1s — gait energy baseline |
| 2 | 25 | 16 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 1s — stride-level SMA-M1 sync |

---

## Computation

The M-layer integrates E-layer features into continuous mathematical estimates of gait function:

1. **Stride CV** (idx 3): Tracks the coefficient of variation of stride time as a continuous estimate. Incorporates step amplitude at 100ms for instantaneous stride force and mean amplitude at 1s for the gait energy baseline. CV is normalized to [0, 1] where lower values indicate more regular gait. The clinical formula CV = (SD/Mean)*100 from Yamashita 2025 is mapped through sigmoid normalization.

2. **SMA-M1 coupling** (idx 4): Estimates the synchronization strength between SMA and M1 using coupling periodicity at 1s stride-level horizon. This represents the effectiveness of dual-site stimulation — higher coupling indicates the two motor areas are working in better synchrony. Maps to the tDCS+tACS protocol where SMA receives constant current while M1 receives gait-phase-locked alternating current.

3. **Balance score** (idx 5): Directly inherits from f09 (E-layer balance improvement). Normalized Mini-BESTest assessment capturing postural control, reactive balance, sensory orientation, and dynamic gait quality.

4. **Gait stability** (idx 6): Combined stability index: σ(0.5 * f07 + 0.5 * f08). Equal weighting of phase synchronization and CV reduction provides a global gait quality metric. Higher stability indicates the gait pattern has achieved the therapeutic target of synchronized, low-variability walking.

All outputs are sigmoid-bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f07, f08, f09 | Phase sync, CV reduction, balance feed mathematical integration |
| R³ [7] | amplitude | Step force signal for stride CV computation |
| R³ [25:33] | x_l0l5 | SMA-M1 coupling for dual-site synchronization |
| H³ | 3 tuples (see above) | Amplitude and coupling periodicity for temporal integration |
