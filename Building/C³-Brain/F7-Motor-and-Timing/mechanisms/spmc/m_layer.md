# SPMC — Temporal Integration

**Model**: SMA-Premotor-M1 Motor Circuit
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: β
**Layer**: M — Temporal Integration
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 3 | circuit_flow | SMA-to-PMC-to-M1 information flow index. Tracks the functional connectivity of the hierarchical motor circuit by combining sequence planning with execution output. circuit_flow = σ(0.5 * f19 + 0.5 * f21). Zatorre 2007: dorsal stream connects auditory cortex to PMC/SMA for sensorimotor transformations. Harrison 2025: both CTC and SPT pathways active during musically-cued movements. |
| 4 | hierarchy_index | Hierarchical motor organization level. Tracks the degree of top-down motor planning by combining SMA sequence encoding with PMC action selection. hierarchy_index = σ(0.5 * f19 + 0.5 * f20). Grahn & Brett 2007: SMA and putamen show hierarchical beat-metric responses. Hoddinott & Grahn 2024: RSA confirms beat-strength encoding in SMA. |
| 5 | timing_precision | Cerebellar timing precision. Tracks the accuracy of temporal predictions via cerebellar error correction, driven by beat periodicity. timing_precision = σ(0.5 * beat_period_1s). Okada 2022: cerebellar dentate nucleus correlates with timing of next movement and temporal error. Thaut 2015: mCBGT circuit provides rhythmic entrainment foundations. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 16 | M14 (periodicity) | L2 (bidi) | Beat periodicity for timing precision 1s |
| 1 | 25 | 8 | M14 (periodicity) | L2 (bidi) | Circuit periodicity 500ms |
| 2 | 25 | 16 | M14 (periodicity) | L2 (bidi) | Circuit periodicity 1s |
| 3 | 33 | 8 | M1 (mean) | L0 (fwd) | Mean pattern stability 500ms |
| 4 | 33 | 16 | M2 (std) | L0 (fwd) | Sequence variability 1s |
| 5 | 33 | 16 | M19 (stability) | L0 (fwd) | Sequence stability 1s |

---

## Computation

The M-layer computes three mathematical model outputs that characterize the motor circuit's temporal integration properties:

1. **Circuit Flow (dim 3)**: Measures the end-to-end information flow from SMA planning to M1 execution. By averaging the sequence planning and execution output from the E-layer, this captures whether the full hierarchical circuit is engaged. High circuit flow indicates intact SMA-PMC-M1 transmission.

2. **Hierarchy Index (dim 4)**: Quantifies the degree of top-down hierarchical motor organization. Combines the two upstream nodes (SMA sequence + PMC preparation) to measure whether motor planning is structured hierarchically rather than reactive. Grahn & Brett 2007 demonstrated that metric rhythms preferentially engage this hierarchy.

3. **Timing Precision (dim 5)**: Models cerebellar timing accuracy. Driven primarily by beat periodicity, this reflects the cerebellum's role in online timing correction. Okada 2022 showed cerebellar dentate neurons encode both upcoming timing and temporal error, providing the correction signal that refines motor output.

These M-layer dimensions integrate temporal information across the 500ms-1s range, combining E-layer features with longer-horizon H³ stability and periodicity morphologies.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer [0] | f19_sequence_planning | SMA planning for circuit flow and hierarchy |
| E-layer [1] | f20_motor_preparation | PMC preparation for hierarchy index |
| E-layer [2] | f21_execution_output | M1 execution for circuit flow |
| R³ [25:33] | x_l0l5 | Cross-layer coupling for circuit periodicity |
| R³ [33:41] | x_l4l5 | Sequence regularity for stability measures |
| H³ | 6 tuples (see above) | Multi-scale periodicity and stability |
