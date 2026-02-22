# SSPS — Extraction

**Model**: Saddle-Shaped Preference Surface
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: γ
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_ic_value | Current information content (surprise) level. Captures the degree of temporal surprise in the acoustic signal from fast IC at 75ms and IC velocity at 500ms. f01 = sigma(0.35 * ic_75ms + 0.30 * ic_velocity_500ms). Cheung 2019: IC (information content) forms one axis of the saddle-shaped preference surface. |
| 1 | f02_entropy_value | Current entropy (uncertainty) level. Combines concentration entropy, roughness variability, and context variability to estimate the listener's current uncertainty state. f02 = sigma(0.35 * concentration_entropy_1s + 0.35 * roughness_std_1s + 0.30 * context_variability_500ms). Cheung 2019: entropy forms the second axis of the saddle surface. |
| 2 | f03_saddle_position | Position on the saddle-shaped preference surface. Computed from the IC x entropy interaction via two optimal zones: zone1 = f02 * (1 - f01) (high entropy + low IC), zone2 = (1 - f02) * 4*f01*(1-f01) (low entropy + medium IC). f03 = sigma(0.35 * max(zone1, zone2) + 0.30 * coupling_entropy_1s). Cheung 2019: interaction beta = -0.124, p = 0.000246. |
| 3 | f04_peak_proximity | Proximity to an optimal preference zone peak. Measures how close the current IC x entropy combination is to one of the two pleasure peaks on the saddle surface. f04 = sigma(0.35 * f03 + 0.30 * pleasantness_smoothness_1s). Gold 2023: R^2 = 0.496 for full saddle model; VS shows RPE-like surprise x liking pattern. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 21 | 2 | M0 (value) | L0 (fwd) | IC at 75ms (fast surprise) |
| 1 | 21 | 8 | M8 (velocity) | L0 (fwd) | IC velocity at 500ms |
| 2 | 21 | 16 | M20 (entropy) | L2 (bidi) | IC entropy over 1s |
| 3 | 24 | 8 | M2 (std) | L2 (bidi) | Concentration std at 500ms |
| 4 | 24 | 16 | M20 (entropy) | L2 (bidi) | Concentration entropy at 1s |
| 5 | 0 | 8 | M1 (mean) | L2 (bidi) | Mean roughness at 500ms |
| 6 | 0 | 16 | M2 (std) | L2 (bidi) | Roughness variability at 1s |
| 7 | 4 | 8 | M1 (mean) | L2 (bidi) | Mean pleasantness at 500ms |
| 8 | 4 | 16 | M15 (smoothness) | L0 (fwd) | Pleasantness smoothness at 1s |
| 9 | 8 | 16 | M1 (mean) | L2 (bidi) | Mean loudness at 1s |
| 10 | 33 | 8 | M1 (mean) | L2 (bidi) | IC-perceptual coupling at 500ms |
| 11 | 33 | 16 | M20 (entropy) | L2 (bidi) | Coupling entropy at 1s |
| 12 | 25 | 8 | M2 (std) | L2 (bidi) | Context variability at 500ms |
| 13 | 25 | 16 | M1 (mean) | L2 (bidi) | Mean context at 1s |

---

## Computation

The E-layer extracts four explicit features that characterize the listener's position on the saddle-shaped preference surface. The key insight is that musical preference is not a simple inverted-U of complexity -- it follows a saddle-shaped surface in IC x entropy space with two distinct optimal zones (Cheung 2019).

All features use sigmoid activation with coefficient sums equal to 1.0 (saturation rule).

1. **f01** (IC value): Captures the current level of information content (surprise) by combining fast IC at 75ms (immediate surprise detection) with IC velocity at 500ms (rate of surprise change). This forms the x-axis of the saddle surface.

2. **f02** (entropy value): Estimates the current level of uncertainty by integrating three signals: concentration entropy at 1s (spectral uncertainty), roughness variability at 1s (harmonic complexity), and context variability at 500ms (environmental unpredictability). This forms the y-axis of the saddle surface.

3. **f03** (saddle position): Computes the position on the preference surface via the IC x entropy interaction. Two optimal zones are computed:
   - **Zone 1**: High entropy * low IC = predictable events in uncertain contexts (Mencke 2019)
   - **Zone 2**: Low entropy * quadratic IC = moderate surprise in stable contexts (Berlyne 1971)
   The saddle value is max(zone1, zone2), combined with coupling entropy to assess the interaction strength.

4. **f04** (peak proximity): Measures proximity to the nearest optimal zone peak. Combines the saddle position with pleasantness smoothness, which tracks how smoothly hedonic quality varies (smooth variation near peaks, jagged variation in the saddle trough).

H3 tuples span H2 (75ms) through H16 (1s), using a mix of L0 (forward) and L2 (bidirectional) laws. The fast IC features (H2, L0) capture immediate surprise, while entropy features require longer windows (H16, L2) for stable uncertainty estimation.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R3[0] roughness | Harmonic complexity | Entropy axis: roughness variability contributes to uncertainty estimation |
| R3[4] sensory_pleasantness | Hedonic quality | Liking proxy for peak proximity computation |
| R3[8] loudness | Perceptual salience | Attention weight for preference evaluation |
| R3[21] spectral_change | Temporal surprise (IC proxy) | Primary information content signal |
| R3[24] concentration_change | Spectral complexity (entropy proxy) | Primary uncertainty signal |
| R3[25] x_l0l5[0] | Context integration | Context variability for entropy estimation |
| R3[33:41] x_l4l5 | IC-perceptual coupling | Saddle surface interaction features |
| H3 (14 tuples) | Multi-scale temporal morphology | IC/entropy dynamics at 75ms-1s |
| IUCP (intra-unit) | Inverted-U preference | SSPS refines IUCP's inverted-U with saddle topology |
