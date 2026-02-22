# ASAP — Extraction

**Model**: Action Simulation for Auditory Prediction
**Unit**: MPU-β1
**Function**: F7 Motor & Timing
**Tier**: β (Bridging)
**Layer**: E — Extraction
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f10_beat_prediction | Temporal "when" prediction via motor simulation. f10 = σ(0.40 * beat_periodicity_1s + 0.35 * onset_periodicity_1s). The motor system predicts beat timing rather than content, relying on spectral_flux periodicity at 1s (beat regularity) and onset_strength periodicity at 1s (onset regularity). Patel & Iversen 2014: ASAP hypothesis — beat perception requires continuous motor-auditory interaction via dorsal pathway. Range [0, 1]. |
| 1 | f11_motor_simulation | Continuous action simulation strength. f11 = σ(0.40 * onset_100ms + 0.35 * coupling_100ms). Captures the ongoing motor system simulation of upcoming beats at fast timescales. Ross & Balasubramaniam 2022: motor simulation generates temporal predictions; TMS to parietal/premotor impairs beat but not interval timing. Range [0, 1]. |
| 2 | f12_dorsal_stream | Parietal dorsal auditory-motor pathway activity. f12 = σ(0.35 * dorsal_periodicity_1s + 0.35 * dorsal_velocity_100ms + 0.30 * f10 * f11). Bidirectional coupling through the dorsal pathway — motor prediction feeds forward, auditory error corrects back. Ross et al. 2018: cTBS to posterior parietal cortex impairs beat-based but NOT interval timing (double dissociation). Range [0, 1]. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 3 | M0 (value) | L0 (fwd) | Onset at 100ms — fast beat detection |
| 1 | 10 | 16 | M14 (periodicity) | L0 (fwd) | Beat periodicity 1s — rhythmic regularity |
| 2 | 11 | 16 | M14 (periodicity) | L0 (fwd) | Onset periodicity 1s — onset regularity |
| 3 | 25 | 3 | M0 (value) | L0 (fwd) | Motor-auditory coupling 100ms — fast simulation |
| 4 | 33 | 3 | M8 (velocity) | L0 (fwd) | Dorsal stream velocity 100ms — pathway speed |
| 5 | 33 | 16 | M14 (periodicity) | L0 (fwd) | Dorsal periodicity 1s — pathway regularity |

---

## Computation

The E-layer extracts three explicit features capturing the core components of action simulation for auditory prediction.

**f10 (beat_prediction)** is the temporal "when" prediction signal. It combines beat periodicity at 1s (how regular onsets are at the beat timescale) and onset periodicity at 1s (how regular onset events are). Both features pass through sigmoid activation. This reflects the ASAP hypothesis that beat perception is fundamentally a temporal prediction — the motor system predicts "when" not "what."

**f11 (motor_simulation)** captures the continuous action simulation at fast timescales. It combines onset value at 100ms (immediate onset detection) with motor-auditory coupling at 100ms (current coupling state). This fast-scale feature reflects the ongoing motor simulation process that generates temporal predictions.

**f12 (dorsal_stream)** models the parietal dorsal auditory-motor pathway. It integrates dorsal stream periodicity at 1s (sustained pathway activity), dorsal velocity at 100ms (pathway responsiveness), and the interaction of f10 and f11 (beat prediction gated by simulation strength). The interaction term captures the bidirectional coupling: motor prediction (f11) modulates beat prediction (f10) through the dorsal pathway.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³[10] spectral_flux | Beat onset detection | "When" prediction requires onset timing |
| R³[11] onset_strength | Beat event strength | Temporal prediction anchor |
| R³[25] x_l0l5[0] | Motor-auditory coupling | Action simulation signal |
| R³[33] x_l4l5[0] | Dorsal stream activity | Parietal pathway for beat prediction |
| H³ (6 tuples) | Multi-scale temporal dynamics | Fast (100ms) to beat-level (1s) prediction |
