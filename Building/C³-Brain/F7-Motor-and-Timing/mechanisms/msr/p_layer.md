# MSR — Cognitive Present

**Model**: Musician Sensorimotor Reorganization
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: P — Cognitive Present
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 6 | bottom_up_precision | Current neural synchrony precision. Measures instantaneous bottom-up processing quality based on gamma-band coupling. Higher values indicate more precise sensory encoding. Grahn & Brett 2007: musicians activate PMC, cerebellum, SMA during all rhythms. Alpheis 2025: increased FC of dlPFC-putamen (t=4.46) in musician brains. |
| 7 | top_down_modulation | Current cortical inhibition level. Measures instantaneous top-down modulation strength. Higher values indicate stronger suppression of redundant neural responses. L. Zhang 2015: P2 suppression reflects efficient cortical gating. Liang 2025: music stimulation enhances PM-SMA, dlPFC, M1 connectivity. |
| 8 | training_level | Estimated expertise marker. Inferred training level from the PLV/P2 dissociation pattern. σ(0.5 * f04 + 0.5 * (1 - f05)). High PLV combined with low P2 indicates extensive training. L. Zhang 2015: musicians had 9.07 +/- 4.68 years training. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 16 | M21 (zero_crossings) | L2 (bidi) | Coupling phase resets 1s — synchrony stability |
| 1 | 10 | 3 | M0 (value) | L2 (bidi) | Onset at 100ms — bottom-up input |
| 2 | 10 | 3 | M14 (periodicity) | L2 (bidi) | Onset periodicity 100ms — processing regularity |

---

## Computation

The P-layer assesses the real-time state of sensorimotor reorganization at the current moment:

1. **Bottom-up precision** (idx 6): Evaluates instantaneous bottom-up processing quality from gamma-band coupling strength. Incorporates onset value and periodicity at 100ms to capture how precisely the sensory system is encoding the current stimulus. Higher precision in musicians reflects enhanced neural phase-locking (PLV) at 40-60 Hz.

2. **Top-down modulation** (idx 7): Evaluates instantaneous top-down inhibition from P2 suppression and coupling phase resets. Zero-crossings at 1s track disruptions in the inhibitory control — fewer resets indicate more stable top-down modulation. Reflects the ACC-mediated cortical gating that reduces P2 amplitude in trained listeners.

3. **Training level** (idx 8): Inferred expertise marker computed as σ(0.5 * f04 + 0.5 * (1 - f05)). High PLV (f04 high) combined with strong P2 suppression (f05 high, inverted) produces high training level. This provides a continuous [0, 1] estimate of sensorimotor reorganization degree that other models can consume as a training-dependent modulator.

All outputs are sigmoid-bounded to [0, 1] and represent instantaneous present-state assessments.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f04_high_freq_plv | PLV level feeds bottom-up precision and training estimation |
| E-layer | f05_p2_suppression | P2 suppression feeds top-down modulation and training estimation |
| R³ [10] | spectral_flux | Onset features for bottom-up precision assessment |
| R³ [25:33] | x_l0l5 | Coupling phase resets for top-down stability |
| H³ | 3 tuples (see above) | Coupling resets and onset periodicity for present-state evaluation |
