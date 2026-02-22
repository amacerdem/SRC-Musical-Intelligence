# NSCP — Extraction

**Model**: Neural Synchrony Commercial Prediction
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: E — Extraction
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f22_neural_synchrony | Inter-subject correlation (ISC) proxy. Tracks population-level neural synchrony during music listening by combining cross-layer coherence periodicity with harmonic consonance. f22 = σ(0.40 * coherence_period_1s + 0.30 * consonance_100ms). Leeuwis 2021: neural synchrony predicts commercial success (R² = 0.404 early, R² = 0.619 combined). Hasson 2004: ISC in cortical responses during naturalistic stimuli is reliable and content-driven. |
| 1 | f23_commercial_prediction | Streaming popularity proxy. Predicts commercial success from neural synchrony combined with multi-feature temporal binding. f23 = σ(0.40 * f22 + 0.30 * binding_period_1s). Leeuwis 2021: 1% ISC increase corresponds to approximately 2.4M more Spotify streams. Berns 2010: NAcc activity during music listening predicts future song sales (r = 0.33). |
| 2 | f24_catchiness_index | Population motor response ("catchiness"). Tracks the shared groove/motor entrainment response that drives repeated listening. f24 = σ(0.35 * onset_period_1s + 0.30 * loudness_entropy). Spiech 2022: pupil drift rate indexes groove perception with inverted-U syncopation relationship (F(1,29) = 10.515, p = .003). Sarasso 2019: musical consonance enhances motor inhibition and aesthetic engagement (eta² = 0.685). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 16 | M14 (periodicity) | L2 (bidi) | Coherence periodicity 1s for ISC proxy |
| 1 | 3 | 3 | M0 (value) | L2 (bidi) | Consonance at 100ms for synchrony quality |
| 2 | 33 | 16 | M14 (periodicity) | L2 (bidi) | Binding periodicity 1s for commercial prediction |
| 3 | 10 | 16 | M14 (periodicity) | L2 (bidi) | Onset periodicity 1s for catchiness |
| 4 | 8 | 3 | M20 (entropy) | L2 (bidi) | Loudness entropy 100ms for engagement |

---

## Computation

The E-layer extracts three features that model the population-level neural synchrony pathway from shared brain response to commercial outcome:

1. **Neural Synchrony (f22)**: The primary ISC proxy. Combines two signals that drive inter-subject correlation: cross-layer coherence periodicity (how consistently the auditory feature space oscillates across time) and harmonic consonance (which Sarasso 2019 showed enhances population-level responses). The 1s coherence periodicity captures the temporal scale at which EEG ISC was measured in Leeuwis 2021.

2. **Commercial Prediction (f23)**: A second-order feature combining ISC magnitude with multi-feature binding periodicity. The binding periodicity (x_l4l5 at 1s) captures whether multiple perceptual features cohere over time -- songs with consistent multi-feature binding synchronize brains more reliably. This follows Leeuwis 2021's finding that ISC magnitude maps to streaming counts.

3. **Catchiness Index (f24)**: Models the population motor entrainment response. Onset periodicity captures beat regularity (the rhythmic foundation of "catchiness"), while loudness entropy captures dynamic unpredictability. The combination reflects Spiech 2022's inverted-U finding: moderate rhythmic complexity maximizes groove. High onset regularity with moderate dynamic variation yields peak catchiness.

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [3] | stumpf | Harmonic consonance for cross-subject consistency |
| R³ [7] | amplitude | Acoustic salience for attention capture |
| R³ [8] | loudness | Perceptual loudness for engagement driver |
| R³ [10] | spectral_flux | Musical events for ISC engagement markers |
| R³ [25:33] | x_l0l5 | Cross-layer coherence as neural sync proxy |
| R³ [33:41] | x_l4l5 | Multi-feature binding for ISC prediction |
| H³ | 5 tuples (see above) | Multi-scale temporal dynamics for synchrony computation |
