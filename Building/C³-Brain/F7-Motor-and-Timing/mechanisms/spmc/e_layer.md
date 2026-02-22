# SPMC — Extraction

**Model**: SMA-Premotor-M1 Motor Circuit
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: β
**Layer**: E — Extraction
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f19_sequence_planning | SMA temporal sequence encoding. Tracks how strongly the supplementary motor area encodes upcoming motor sequences from beat periodicity. f19 = σ(0.40 * beat_period_1s). Grahn & Brett 2007: SMA + putamen respond to beat in metric rhythms (F(2,38)=20.67, p<.001). Hoddinott & Grahn 2024: SMA multi-voxel patterns encode beat strength via RSA. |
| 1 | f20_motor_preparation | PMC action selection and motor preparation. Tracks premotor cortex readiness for upcoming motor actions based on circuit periodicity and tempo velocity. f20 = σ(0.30 * circuit_period_1s + 0.30 * tempo_velocity). Pierrieau 2025: beta oscillations (13-30 Hz) in motor cortex predict motor flexibility/action selection. Kohler 2025: PMC shows content-specific action representations. |
| 2 | f21_execution_output | M1 motor execution output. Tracks primary motor cortex execution level from the interaction of sequence planning and motor preparation, modulated by amplitude. f21 = σ(0.35 * f19 * f20 + 0.30 * mean_amplitude_1s). Kohler 2025: self-produced actions localized to left M1 via MVPA. Harrison 2025: sensorimotor cortex activated during musically-cued movements. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 3 | M0 (value) | L2 (bidi) | SMA onset tracking 100ms |
| 1 | 10 | 16 | M14 (periodicity) | L2 (bidi) | SMA beat periodicity 1s |
| 2 | 11 | 3 | M0 (value) | L2 (bidi) | Motor timing marker 100ms |
| 3 | 11 | 16 | M14 (periodicity) | L2 (bidi) | Onset periodicity 1s |
| 4 | 21 | 4 | M8 (velocity) | L0 (fwd) | Tempo velocity 125ms |
| 5 | 7 | 16 | M1 (mean) | L2 (bidi) | Mean motor output level 1s |

---

## Computation

The E-layer extracts the three core nodes of the SMA-Premotor-M1 hierarchical motor circuit:

1. **Sequence Planning (f19)**: Models SMA temporal sequence encoding -- the longest timescale in the hierarchy. Beat periodicity at 1s drives this feature, reflecting SMA's role in encoding temporal structure of motor sequences. Grahn & Brett 2007 showed SMA activation scales with metrical complexity.

2. **Motor Preparation (f20)**: Models PMC action selection at a medium timescale. Combines circuit periodicity (cross-layer coupling regularity) with tempo velocity (rate of tempo change). Pierrieau 2025 demonstrated beta oscillations in motor cortex predict action selection flexibility, not vigor.

3. **Execution Output (f21)**: Models M1 motor execution at the shortest timescale. The multiplicative interaction f19 * f20 captures the hierarchical flow -- execution depends on both planning and preparation being active. Mean amplitude modulates output strength. Kohler 2025 confirmed M1 encodes self-produced actions via MVPA.

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [7] | amplitude | Motor output strength for M1 execution level |
| R³ [10] | spectral_flux | Onset detection for SMA sequence markers |
| R³ [11] | onset_strength | Beat event for motor timing signal |
| R³ [21] | spectral_change | Tempo rate for SMA tempo encoding |
| R³ [25:33] | x_l0l5 | Hierarchical circuit coupling (SMA-PMC-M1) |
| H³ | 6 tuples (see above) | Multi-scale temporal dynamics for motor hierarchy |
