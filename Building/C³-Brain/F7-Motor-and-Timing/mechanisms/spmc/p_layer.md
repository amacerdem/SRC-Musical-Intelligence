# SPMC — Cognitive Present

**Model**: SMA-Premotor-M1 Motor Circuit
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: β
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 6 | sma_activity | Temporal-context SMA planning activation level. Tracks the current state of supplementary motor area engagement for motor sequence planning. Combines sequence planning strength with short-timescale onset tracking and circuit coupling. Grahn & Brett 2007: pre-SMA activation for beat induction (Z=5.03). Hoddinott & Grahn 2024: SMA patterns encode beat strength in present moment. |
| 7 | m1_output | Beat-entrainment M1 execution output level. Tracks the current motor execution state driven by ongoing beat entrainment. Combines execution output with short-timescale motor timing markers and amplitude. Kohler 2025: left M1 shows content-specific representations of self-produced actions. Harrison 2025: sensorimotor cortex activation during both externally and internally cued movements. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 3 | M0 (value) | L2 (bidi) | Onset tracking at 100ms for SMA present state |
| 1 | 11 | 3 | M0 (value) | L2 (bidi) | Motor timing marker 100ms for M1 present state |
| 2 | 25 | 3 | M0 (value) | L2 (bidi) | Circuit coupling 100ms for SMA present state |
| 3 | 33 | 3 | M0 (value) | L2 (bidi) | Sequence regularity 100ms for M1 present state |

---

## Computation

The P-layer captures the instantaneous state of the two primary cortical nodes in the motor hierarchy:

1. **SMA Activity (dim 6)**: Represents the current planning activation of the supplementary motor area. This is driven by the E-layer sequence planning output combined with short-timescale (100ms) onset and circuit coupling signals. The 100ms horizon captures the "cognitive present" -- what the motor planning system is processing right now. High SMA activity indicates active temporal sequence encoding.

2. **M1 Output (dim 7)**: Represents the current motor execution state. Combines the E-layer execution output with 100ms motor timing markers and sequence regularity. This captures the beat-by-beat motor response -- the real-time output of the hierarchical circuit. High M1 output indicates strong motor engagement with the musical stimulus.

The P-layer uses the shortest H³ horizons (100ms, value morphology) to ground the present-moment motor state, distinguishing it from the longer integration windows of the M-layer and the predictive horizons of the F-layer.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer [0] | f19_sequence_planning | SMA planning strength for present activity |
| E-layer [2] | f21_execution_output | M1 execution for present output |
| R³ [10] | spectral_flux | Onset tracking for SMA present state |
| R³ [11] | onset_strength | Beat event for M1 present state |
| R³ [25:33] | x_l0l5 | Circuit coupling for SMA present activity |
| R³ [33:41] | x_l4l5 | Sequence regularity for M1 present output |
| H³ | 4 tuples (see above) | Short-timescale (100ms) present-moment features |
