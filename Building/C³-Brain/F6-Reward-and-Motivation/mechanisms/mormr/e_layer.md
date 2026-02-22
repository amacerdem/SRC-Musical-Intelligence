# MORMR — Extraction

**Model**: mu-Opioid Receptor Music Reward
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: α
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_opioid_release | Endogenous opioid release proxy. Tracks mu-opioid receptor activation in reward regions during pleasurable music. σ(0.35 * mean_pleasantness_1s + 0.20 * (1 - mean_roughness_1s) + 0.15 * mean_warmth_500ms). Putkinen 2025: [11C]carfentanil binding increases in VS, OFC, amygdala during music (d = 4.8). |
| 1 | f02_chills_count | Chills frequency proxy. Tracks the likelihood and intensity of musical chills (frisson). σ(... + 0.20 * amplitude_500ms + 0.15 * beauty_coupling_500ms). Putkinen 2025: chills count correlates with NAcc BPND (r = -0.52, negative because more opioid release = less radiotracer). |
| 2 | f03_nacc_binding | NAcc opioid activity proxy. Tracks MOR binding specifically in the nucleus accumbens hedonic hotspot. σ(0.40 * f01 + 0.30 * pleasantness_velocity_1s). Putkinen 2025: NAcc shows strongest music-induced MOR activation. |
| 3 | f04_reward_sensitivity | Individual music reward sensitivity. Captures between-subject variance in opioid-mediated pleasure. σ(0.40 * f01 * f02 + 0.30 * beauty_entropy_1s). Putkinen 2025: baseline MOR tone modulates pleasure-BOLD coupling (d = 1.16). Mas-Herrero 2014: musical anhedonia dissociates from monetary reward. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 4 | 16 | M1 (mean) | L2 (bidi) | Mean pleasantness over 1s — primary hedonic signal |
| 1 | 0 | 16 | M1 (mean) | L2 (bidi) | Mean roughness over 1s — consonance context (inverted) |
| 2 | 12 | 8 | M1 (mean) | L2 (bidi) | Mean warmth at 500ms — timbral richness |
| 3 | 7 | 8 | M0 (value) | L2 (bidi) | Amplitude at 500ms — peak magnitude for chills |
| 4 | 41 | 8 | M0 (value) | L2 (bidi) | Beauty coupling at 500ms — aesthetic quality |
| 5 | 4 | 16 | M8 (velocity) | L0 (fwd) | Pleasantness velocity over 1s — hedonic change rate |
| 6 | 41 | 16 | M20 (entropy) | L2 (bidi) | Beauty entropy at 1s — aesthetic complexity |

---

## Computation

The E-layer models mu-opioid receptor activation during musical pleasure, based on Putkinen et al. (2025) PET evidence:

1. **Opioid Release (f01)**: Combines consonance quality (pleasantness, inverse roughness) with timbral warmth. Opioid release is driven by sustained hedonic quality rather than sudden events -- hence the 1s mean horizons. This reflects the slower pharmacokinetics of the opioid system compared to dopamine.

2. **Chills Count (f02)**: Combines peak intensity signals (loudness, amplitude) with aesthetic coupling. Chills are triggered by peak emotional moments with high aesthetic value. The beauty coupling feature (x_l5l7) captures the Perceptual x Crossband interaction that corresponds to "musical beauty."

3. **NAcc Binding (f03)**: A second-order feature combining opioid release with pleasantness velocity. The rate of change in pleasantness (velocity) captures the dynamic hedonic trajectory -- rising pleasantness predicts stronger NAcc activation.

4. **Reward Sensitivity (f04)**: The multiplicative interaction f01 * f02 captures individual differences: listeners who show both high opioid release AND frequent chills are the most reward-sensitive. Beauty entropy modulates this to capture complexity preference.

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [0] | roughness | Consonance quality (inverse) for pleasure |
| R³ [4] | sensory_pleasantness | Direct hedonic signal |
| R³ [7] | amplitude | Peak magnitude for chills intensity |
| R³ [8] | loudness | Pleasure intensity level |
| R³ [12] | warmth | Timbral richness for aesthetic quality |
| R³ [13] | brightness | Spectral character for timbre recognition |
| R³ [22] | energy_change | Dynamic modulation for expressive intensity |
| R³ [33:41] | x_l4l5 | Sustained pleasure (Derivatives x Perceptual) |
| R³ [41:49] | x_l5l7 | Pleasure-structure beauty (Perceptual x Crossband) |
| H³ | 7 tuples (see above) | Multi-scale temporal dynamics for opioid response |
