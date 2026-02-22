# NSCP — Cognitive Present

**Model**: Neural Synchrony Commercial Prediction
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 6 | coherence_level | Beat-entrainment cross-layer coherence level. Tracks the instantaneous state of neural coherence across spectral feature layers, serving as a real-time ISC proxy. Driven by short-timescale cross-layer coupling and onset values. Leeuwis 2021: ISC strongest at frontocentral and temporal electrodes during beat-driven passages. Hasson 2004: intersubject correlation is content-driven and reliable at moment-to-moment timescales. |
| 7 | groove_response | Beat-entrainment groove/motor response level. Tracks the current motor engagement state reflecting population-level rhythmic entrainment. Combines short-timescale onset tracking with loudness entropy for dynamic modulation. Spiech 2022: pupil drift rate indexes groove perception moment-by-moment. Sarasso 2019: consonance enhances motor inhibition engagement in real time. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 0 | M0 (value) | L2 (bidi) | Instantaneous onset 25ms for groove present state |
| 1 | 10 | 3 | M0 (value) | L2 (bidi) | Onset at 100ms for groove present state |
| 2 | 25 | 0 | M0 (value) | L2 (bidi) | Coherence at 25ms for coherence present state |
| 3 | 25 | 3 | M0 (value) | L2 (bidi) | Coherence at 100ms for coherence present state |
| 4 | 10 | 1 | M1 (mean) | L2 (bidi) | Mean onset 50ms for groove smoothing |
| 5 | 25 | 1 | M1 (mean) | L2 (bidi) | Mean coherence 50ms for coherence smoothing |

---

## Computation

The P-layer captures the instantaneous state of neural synchrony and motor groove at the cognitive present:

1. **Coherence Level (dim 6)**: Represents the real-time cross-layer coherence state. Uses the shortest H³ horizons (25ms instantaneous, 50ms mean, 100ms value) of the cross-layer coupling signal (x_l0l5). This captures moment-to-moment fluctuations in how synchronized the auditory feature space is -- a real-time proxy for what ISC measures across subjects. High coherence indicates that spectral features are well-organized in the present moment.

2. **Groove Response (dim 7)**: Represents the instantaneous motor entrainment level. Uses short-timescale onset tracking (25ms, 50ms, 100ms) to capture beat-by-beat rhythmic engagement. This is the population-level "groove" response -- the shared motor engagement that Spiech 2022 linked to pupil drift rate. High groove response indicates strong rhythmic entrainment at the current moment.

The P-layer uses the shortest available H³ horizons (25ms-100ms, value and mean morphologies) to ground the cognitive present, distinguishing it from the 1s integration windows of the M-layer and the predictive horizons of the F-layer.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [10] | spectral_flux | Onset tracking for groove present state |
| R³ [25:33] | x_l0l5 | Cross-layer coupling for coherence present state |
| H³ | 6 tuples (see above) | Short-timescale (25ms-100ms) present-moment features |
