# LDAC — Extraction

**Model**: Liking-Dependent Auditory Cortex
**Unit**: RPU-γ1
**Function**: F6 Reward & Motivation
**Tier**: γ (Integrative)
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_stg_liking_coupling | Right STG tracks moment-to-moment liking. f01 = σ(0.35 * pleasantness_100ms + 0.30 * mean_pleasantness_500ms). Continuous coupling between auditory cortex BOLD and hedonic evaluation, demonstrating that sensory processing is not passive but pleasure-modulated. Gold et al. 2023a: R STG covaries with normalized moment-to-moment liking (t(23) = 2.56, p = 0.018). Range [0, 1]. |
| 1 | f02_pleasure_gating | Pleasure gates sensory gain. f02 = σ(0.35 * f01 + 0.30 * loudness_100ms). Top-down reward-to-perception pathway where pleasure state modulates auditory cortex responsiveness. Liked music produces enhanced cortical response; disliked music reduces sensory gain. Martinez-Molina et al. 2016: R STG-NAcc functional connectivity modulated by musical reward sensitivity (PPI group effect p = 0.05). Range [0, 1]. |
| 2 | f03_ic_liking_interaction | Information Content x Liking interaction. f03 = σ(0.35 * ic_75ms * (1 - f01) + 0.30 * ic_entropy_1s). Captures the critical finding that high IC combined with disliking produces the lowest STG activation (maximal sensory suppression). The (1 - f01) term inverts liking so that low liking amplifies the IC contribution. Gold et al. 2023a: IC x liking interaction in R STG (t(23) = 2.92, p = 0.008); Cheung et al. 2019: replicated in harmonic domain as uncertainty x surprise in bilateral AC. Range [0, 1]. |
| 3 | f04_moment_to_moment | Continuous tracking signal. f04 = σ(0.40 * f01 + 0.30 * f02 + 0.30 * spectral_flux_100ms). Integrated real-time summary of STG modulation combining liking coupling, pleasure gating, and sensory deviation detection. Provides a frame-by-frame readout of the reward-modulated auditory processing state. Range [0, 1]. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 4 | 3 | M0 (value) | L2 (bidi) | Pleasantness at 100ms — fast hedonic tracking |
| 1 | 4 | 8 | M1 (mean) | L2 (bidi) | Mean pleasantness 500ms — smoothed liking signal |
| 2 | 4 | 16 | M2 (std) | L2 (bidi) | Pleasantness variability 1s — liking stability |
| 3 | 8 | 3 | M0 (value) | L2 (bidi) | Loudness at 100ms — sensory salience for gating |
| 4 | 8 | 16 | M1 (mean) | L2 (bidi) | Mean loudness over 1s — sustained arousal context |
| 5 | 21 | 2 | M0 (value) | L0 (fwd) | IC at 75ms — surprise detection for IC x liking |
| 6 | 21 | 8 | M8 (velocity) | L0 (fwd) | IC velocity at 500ms — rate of surprise change |
| 7 | 21 | 16 | M20 (entropy) | L2 (bidi) | IC entropy over 1s — predictability context |
| 8 | 10 | 3 | M0 (value) | L2 (bidi) | Spectral flux at 100ms — deviation detection |
| 9 | 10 | 8 | M2 (std) | L2 (bidi) | Flux variability 500ms — deviation consistency |
| 10 | 25 | 3 | M0 (value) | L2 (bidi) | Auditory gating at 100ms — cross-layer modulation |
| 11 | 25 | 16 | M20 (entropy) | L2 (bidi) | Gating entropy over 1s — modulation complexity |

---

## Computation

The E-layer extracts four explicit features capturing the pleasure-dependent modulation of auditory cortex processing.

**f01 (stg_liking_coupling)** is the core feature: continuous coupling between R STG activity and moment-to-moment liking. It combines fast pleasantness (100ms, weight 0.35) for immediate hedonic tracking with smoothed pleasantness (500ms mean, weight 0.30) for temporal stability. This reflects Gold et al. 2023a's finding that R STG BOLD continuously covaries with joystick liking ratings during naturalistic listening.

**f02 (pleasure_gating)** models the top-down reward-to-perception pathway. It takes f01 (weight 0.35) as the pleasure signal and loudness at 100ms (weight 0.30) as the sensory salience being gated. This implements Martinez-Molina et al. 2016's finding that R STG-NAcc functional connectivity is modulated by musical reward sensitivity, with anhedonia reducing the coupling.

**f03 (ic_liking_interaction)** captures the critical IC x liking interaction. The term ic_75ms * (1 - f01) implements the finding that high information content combined with low liking (disliking) produces maximal sensory suppression (lowest STG activity). IC entropy over 1s adds predictability context. This is the most distinctive LDAC feature, replicated across melodic (Gold 2023a) and harmonic (Cheung 2019) domains.

**f04 (moment_to_moment)** integrates all three preceding features with spectral flux at 100ms into a continuous tracking signal, providing a single frame-by-frame readout of reward-modulated auditory processing.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³[4] sensory_pleasantness | Hedonic quality | Moment-to-moment pleasure for STG coupling |
| R³[8] loudness | Sensory salience | Attention capture for pleasure gating |
| R³[10] spectral_flux | Musical deviation | Change detection for moment-to-moment tracking |
| R³[21] spectral_change | Information content (IC) | Surprise level for IC x liking interaction |
| R³[25] x_l0l5[0] | Auditory gating proxy | Cross-layer modulation of STG processing |
| H³ (12 tuples) | Multi-scale temporal dynamics | 75ms surprise to 1s entropy context |
