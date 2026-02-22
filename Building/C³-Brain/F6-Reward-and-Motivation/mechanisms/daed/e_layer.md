# DAED — Extraction

**Model**: Dopamine Anticipation-Experience Dissociation
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: α
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_anticipatory_da | Caudate dopamine proxy. Tracks anticipatory DA release during build-up phases preceding peak moments. σ(0.35 * loudness_velocity_1s + 0.20 * spectral_uncertainty_125ms + 0.15 * roughness_velocity_500ms). Salimpoor 2011: caudate BP correlates with chills count (r = 0.71). |
| 1 | f02_consummatory_da | NAcc dopamine proxy. Tracks consummatory DA release at peak emotional moments. σ(0.35 * mean_pleasantness_1s + 0.15 * mean_loudness_1s). Salimpoor 2011: NAcc BP correlates with pleasure rating (r = 0.84). |
| 2 | f03_wanting_index | Anticipatory motivation. Combines anticipatory DA with coupling entropy to quantify approach motivation. σ(0.40 * f01 + 0.30 * coupling_entropy_1s). Maps to Berridge's incentive salience framework. |
| 3 | f04_liking_index | Consummatory pleasure. Combines consummatory DA with immediate pleasantness for hedonic evaluation. σ(0.50 * f02 + 0.20 * pleasantness_100ms). Maps to Berridge's hedonic "liking" component. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 8 | 16 | M8 (velocity) | L0 (fwd) | Loudness velocity over 1s — anticipatory DA ramp |
| 1 | 21 | 4 | M20 (entropy) | L0 (fwd) | Spectral uncertainty at 125ms — prediction uncertainty |
| 2 | 0 | 8 | M8 (velocity) | L0 (fwd) | Roughness velocity at 500ms — tension dynamics |
| 3 | 4 | 16 | M1 (mean) | L2 (bidi) | Mean pleasantness over 1s — consummatory pleasure |
| 4 | 8 | 16 | M1 (mean) | L2 (bidi) | Mean loudness over 1s — intensity baseline |
| 5 | 25 | 16 | M20 (entropy) | L2 (bidi) | Coupling entropy at 1s — wanting uncertainty |
| 6 | 4 | 3 | M0 (value) | L2 (bidi) | Pleasantness at 100ms — immediate hedonic signal |

---

## Computation

The E-layer implements the core dopaminergic dissociation from Salimpoor et al. (2011). Two parallel pathways compute:

1. **Anticipatory pathway** (f01, f03): Driven by loudness velocity (crescendo tracking), spectral uncertainty (prediction signal), and roughness velocity (tension dynamics). These features map onto caudate nucleus DA release that peaks 15-30s before emotional climax.

2. **Consummatory pathway** (f02, f04): Driven by mean pleasantness and loudness over longer windows (1s), reflecting the sustained hedonic evaluation at the moment of peak emotion. Maps onto NAcc DA release at the peak moment.

f03 (wanting) and f04 (liking) are second-order features that combine the primary DA signals with contextual features (coupling entropy, immediate pleasantness) to produce Berridge-framework wanting/liking indices.

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [0] | roughness | Tension level (inverse consonance) for anticipation |
| R³ [4] | sensory_pleasantness | Direct hedonic signal for consummation |
| R³ [7] | amplitude | Energy build-up tracking |
| R³ [8] | loudness | Perceptual loudness for intensity progression |
| R³ [10] | spectral_flux | Onset detection for peak approach |
| R³ [21] | spectral_change | Spectral dynamics for prediction uncertainty |
| R³ [22] | energy_change | Crescendo/decrescendo dynamics |
| R³ [25:33] | x_l0l5 | Foundation x Perceptual coupling for peak timing |
| H³ | 7 tuples (see above) | Multi-scale temporal dynamics for anticipation/consummation |
