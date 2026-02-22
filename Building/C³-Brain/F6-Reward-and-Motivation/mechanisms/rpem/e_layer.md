# RPEM — Extraction

**Model**: Reward Prediction Error in Music
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: α
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_surprise_signal | Information content (IC) / surprise signal. Tracks how surprising the current musical event is relative to predictions. σ(0.35 * spectral_entropy_125ms + 0.20 * spectral_change_100ms + 0.15 * concentration_100ms). Gold 2023: R STG reflects surprise magnitude (d = 1.22). |
| 1 | f02_liking_signal | Real-time reward valence / liking signal. Tracks the hedonic value of the current moment. σ(... + 0.35 * mean_pleasantness_1s + 0.25 * (1 - roughness_100ms)). Gold 2023: liking interacts with surprise to produce RPE crossover in VS. |
| 2 | f03_positive_rpe | Positive reward prediction error. Surprise x Liked produces VS activation — better-than-expected musical events. σ(0.50 * f01 * f02 + 0.20 * rpe_coupling_100ms). Gold 2023: VS shows increased BOLD for surprising liked stimuli (d = 1.07). |
| 3 | f04_negative_rpe | Negative reward prediction error. Surprise x Disliked produces VS deactivation — worse-than-expected events. σ(0.50 * f01 * (1 - f02) + 0.30 * roughness_velocity_100ms + 0.20 * prediction_entropy_1s). Gold 2023: VS shows decreased BOLD for surprising disliked stimuli. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 21 | 4 | M20 (entropy) | L0 (fwd) | Spectral entropy at 125ms — prediction uncertainty |
| 1 | 21 | 3 | M0 (value) | L2 (bidi) | Spectral change at 100ms — instantaneous surprise |
| 2 | 24 | 3 | M0 (value) | L2 (bidi) | Concentration change at 100ms — uncertainty signal |
| 3 | 4 | 16 | M1 (mean) | L2 (bidi) | Mean pleasantness over 1s — sustained liking |
| 4 | 0 | 3 | M0 (value) | L2 (bidi) | Roughness at 100ms — instantaneous dissonance |
| 5 | 0 | 3 | M8 (velocity) | L0 (fwd) | Roughness velocity at 100ms — tension rate for negative RPE |
| 6 | 33 | 3 | M0 (value) | L2 (bidi) | RPE coupling at 100ms — cross-domain RPE signal |
| 7 | 25 | 16 | M20 (entropy) | L2 (bidi) | Prediction entropy at 1s — model uncertainty |

---

## Computation

The E-layer implements the reward prediction error crossover pattern discovered by Gold et al. (2023). Two primary signals are extracted and then combined multiplicatively:

1. **Surprise Signal (f01)**: Quantifies information content (IC) — how unexpected the current musical event is. Uses spectral entropy (prediction uncertainty), spectral change (acoustic deviation), and concentration change (harmonic uncertainty). Fast timescales (100-125ms) capture event-level surprise.

2. **Liking Signal (f02)**: Quantifies real-time hedonic valence. Uses sustained pleasantness (1s) and instantaneous consonance (inverse roughness). This is the reward signal against which predictions are evaluated.

3. **Positive RPE (f03)**: The multiplicative interaction f01 * f02 implements the core RPE computation: surprise that is liked produces a positive prediction error. The RPE coupling feature (x_l4l5) provides the cross-domain context. Gold (2023) showed this pattern in VS with d = 1.07.

4. **Negative RPE (f04)**: The interaction f01 * (1 - f02) captures surprise that is disliked. Roughness velocity (rapidly increasing dissonance) and prediction entropy (high model uncertainty) amplify negative RPE. This produces VS deactivation.

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [0] | roughness | Harmonic tension for liking signal and negative RPE |
| R³ [4] | sensory_pleasantness | Hedonic valence for liking signal |
| R³ [8] | loudness | Salience encoding for attention capture |
| R³ [10] | spectral_flux | Musical deviation / event detection |
| R³ [21] | spectral_change | Spectral surprise (information content proxy) |
| R³ [24] | concentration_change | Concentration shift / uncertainty signal |
| R³ [25:33] | x_l0l5 | Prediction generation (Foundation x Perceptual) |
| R³ [33:41] | x_l4l5 | Surprise x context RPE computation (Derivatives x Perceptual) |
| H³ | 8 tuples (see above) | Multi-scale temporal dynamics for RPE computation |
