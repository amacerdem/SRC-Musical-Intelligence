# SSRI — Extraction

**Model**: Social Synchrony Reward Integration
**Unit**: RPU-β4
**Function**: F6 Reward & Motivation
**Tier**: β (Bridging)
**Layer**: E — Extraction
**Dimensions**: 5D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_synchrony_reward | Reward from interpersonal synchrony. f01 = σ(0.25 * onset_periodicity_500ms + 0.15 * mean_pleasantness_1s + 0.15 * coupling_trend_1s). Captures how coordinated timing and shared hedonic experience generate mesolimbic reward. Kokal et al. 2011: joint drumming activates caudate with synchrony quality. Range [0, 1]. |
| 1 | f02_social_bonding_index | Social bonding strength proxy. f02 = σ(0.25 * coupling_mean_5s + 0.20 * f01 + 0.15 * loudness_trend_5s + 0.15 * mean_warmth_1s). Slow-building index reflecting cumulative interpersonal connection through shared musical experience. Ni et al. 2024: social bonding increases prefrontal neural synchronization (d = 0.85). Range [0, 1]. |
| 2 | f03_group_flow_state | Group flow / collective absorption. f03 = σ(0.25 * f01 + 0.15 * mean_amplitude_500ms + 0.15 * spectral_entropy_500ms). Models the shared state of absorbed coordination where individual boundaries blur. Williamson & Bonshor 2019: brass band group music produces flow and cognitive engagement. Range [0, 1]. |
| 3 | f04_entrainment_quality | Temporal entrainment precision. f04 = σ(0.30 * onset_periodicity_500ms + 0.25 * beat_periodicity_125ms + 0.25 * onset_100ms + 0.20 * energy_velocity_500ms). Measures how precisely co-performers align in temporal structure. Wohltjen et al. 2023: beat entrainment ability is stable individual difference (d = 1.37). Range [0, 1]. |
| 4 | f05_collective_pleasure | Shared hedonic experience. f05 = σ(0.25 * mean_pleasantness_500ms + 0.20 * f03 + 0.15 * f02). Integrates group flow and social bonding into a collective pleasure estimate that exceeds individual hedonic responses. Range [0, 1]. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 3 | M0 (value) | L2 (bidi) | Onset at 100ms alpha — micro-timing alignment |
| 1 | 10 | 4 | M14 (periodicity) | L2 (bidi) | Beat periodicity 125ms — rhythmic entrainment |
| 2 | 10 | 8 | M14 (periodicity) | L2 (bidi) | Onset periodicity 500ms — phrase-level coordination |
| 3 | 7 | 8 | M1 (mean) | L2 (bidi) | Mean amplitude 500ms — shared dynamic envelope |
| 4 | 4 | 8 | M1 (mean) | L2 (bidi) | Mean pleasantness 500ms — shared hedonic quality |
| 5 | 4 | 16 | M1 (mean) | L2 (bidi) | Mean pleasantness 1s — sustained positive affect |
| 6 | 22 | 8 | M8 (velocity) | L0 (fwd) | Energy velocity 500ms — dynamic coordination tracking |
| 7 | 12 | 16 | M1 (mean) | L2 (bidi) | Mean warmth 1s — timbral blending quality |
| 8 | 21 | 8 | M20 (entropy) | L2 (bidi) | Spectral entropy 500ms — structural coordination demand |
| 9 | 25 | 16 | M18 (trend) | L2 (bidi) | Coupling trend 1s — consonance-energy interaction trajectory |
| 10 | 25 | 20 | M1 (mean) | L0 (fwd) | Coupling mean 5s LTI — sustained emotional synchrony |
| 11 | 8 | 20 | M18 (trend) | L0 (fwd) | Loudness trend 5s LTI — long-range dynamic trajectory |

---

## Computation

The E-layer extracts five explicit features capturing the reward-relevant dimensions of social musical interaction.

**f01 (synchrony_reward)** is the core reward signal from interpersonal coordination. It combines onset periodicity at 500ms (how regularly onsets occur, indexing beat-level coordination), mean pleasantness at 1s (hedonic quality of the shared stimulus), and coupling trend at 1s (whether consonance-energy interaction is strengthening). All pass through sigmoid activation.

**f02 (social_bonding_index)** accumulates over longer timescales (5s LTI coupling mean, 5s loudness trend) and depends on f01, reflecting that bonding builds on synchrony reward. Mean warmth at 1s contributes timbral blend quality.

**f03 (group_flow_state)** combines f01 with beat-level dynamics (mean amplitude 500ms, spectral entropy 500ms) to capture collective absorption during coordinated performance.

**f04 (entrainment_quality)** is the most temporally precise feature, drawing on fast-scale onset alignment (100ms, 125ms periodicity) and medium-scale periodicity (500ms). Energy velocity adds dynamic coordination tracking.

**f05 (collective_pleasure)** integrates f02 and f03 with mean pleasantness 500ms, providing a summary hedonic signal that reflects the social amplification of individual pleasure.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³[10] spectral_flux | Onset synchrony quality | Temporal alignment between performers |
| R³[7] amplitude | Shared dynamic envelope | Joint crescendo/decrescendo tracking |
| R³[4] sensory_pleasantness | Hedonic quality of shared stimulus | Shared positive affect |
| R³[8] loudness | Perceptual intensity matching | Loudness alignment across performers |
| R³[12] warmth | Timbral blending quality | Warmth similarity indexes blend quality |
| R³[22] energy_change | Dynamic coordination tracking | Shared energy trajectory matching |
| R³[21] spectral_change | Structural coordination demand | Simultaneous change indexes synchrony challenge |
| R³[25] x_l0l5[0] | Foundation-perceptual coupling | Consonance-energy interaction for group processing |
| H³ (12 tuples) | Multi-scale temporal dynamics | Fast (100-125ms) to long-range (5s) coordination tracking |
