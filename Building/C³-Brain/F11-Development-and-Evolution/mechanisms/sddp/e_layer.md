# SDDP — Extraction

**Model**: Sex-Dependent Developmental Plasticity
**Unit**: NDU
**Function**: F11 Development & Evolution
**Tier**: gamma
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_sex_modulation | Sex-dependent plasticity rate. Multiplicative scaling factor: 1 + (eta^2 * sex_indicator), where eta^2=0.309 from Partanen 2022 sex x singing time interaction (p=0.017). Males: f01~1.31, Females: f01=1.0. Range [0, 2]. |
| 1 | f02_male_advantage | Male-specific enhancement magnitude. Difference score: (MMR_male - MMR_female) / (MMR_baseline + epsilon). Captures the relative male advantage in MMR amplitude enhancement from singing intervention. Partanen 2022: males show stronger MMR enhancement for vowel duration deviants (p=0.001). Range [-0.5, 0.5]. |
| 2 | f03_plasticity_window | Developmental timing match. Gaussian fit: exp(-(GA - 30)^2 / (2 * 2^2)), centered at 30 weeks gestational age with sigma=2 weeks. Captures the hypothesized optimal intervention window for auditory plasticity in preterm infants. Range [0, 1]. |
| 3 | f04_intervention_response | Sex-dependent intervention response. sigma(0.35 * loudness_100ms + 0.35 * mean_loudness_500ms) * f01. Combines perceived loudness at 100ms alpha and 500ms delta mean, scaled by sex modulation factor. Partanen 2022: group effect eta^2=0.229 (p=0.030). Range [0, 1]. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 4 | 3 | M0 (value) | L2 (bidi) | Vocal consonance at 100ms alpha |
| 1 | 4 | 16 | M1 (mean) | L2 (bidi) | Mean consonance over 1s beat |
| 2 | 7 | 0 | M0 (value) | L2 (bidi) | Instantaneous vocal intensity 25ms gamma |
| 3 | 7 | 3 | M1 (mean) | L2 (bidi) | Mean intensity 100ms alpha |
| 4 | 8 | 3 | M0 (value) | L2 (bidi) | Perceived loudness 100ms alpha |
| 5 | 8 | 8 | M1 (mean) | L2 (bidi) | Mean perceived loudness 500ms delta |
| 6 | 14 | 3 | M0 (value) | L2 (bidi) | Vocal warmth 100ms alpha |
| 7 | 17 | 3 | M0 (value) | L2 (bidi) | Voice/noise tonality ratio 100ms |

---

## Computation

The E-layer extracts four explicit features characterizing sex-dependent developmental plasticity from parental singing intervention:

1. **Sex modulation** (f01): A multiplicative scaling factor derived from the eta^2=0.309 sex x singing time interaction reported by Partanen 2022. For male infants the factor is ~1.31, for female infants 1.0. This captures the observation that males showed significantly stronger MMR enhancement from singing exposure during the preterm period. Note: Scholkmann 2024 found opposite-direction sex effects in cerebrovascular response (females positive, males negative StO2), suggesting the sex modulation may be measure-specific.

2. **Male advantage** (f02): A normalized difference score quantifying the relative male benefit. Computed as the ratio of male-female MMR difference to baseline MMR amplitude. This dimension is speculative (gamma-tier) given the small sample (n=21) and awaits independent replication.

3. **Plasticity window** (f03): A Gaussian function of gestational age centered at 30 weeks with sigma=2 weeks. Captures the hypothesized optimal developmental window for singing intervention. Edalati 2023 and Saadatmehr 2024 show that beat/meter processing capacity matures progressively, with hierarchical rhythm coding emerging after ~33 weeks GA.

4. **Intervention response** (f04): Loudness-driven intervention engagement scaled by the sex modulation factor. Uses H3 features at 100ms alpha and 500ms delta timescales to capture both immediate attention capture and sustained engagement. Coefficients sum to 0.70 before implicit 0.30 bias (saturation rule).

All sigmoid formulas use coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [4] | consonance | Vocal harmonic quality for singing quality assessment |
| R3 [7] | amplitude | Instantaneous vocal intensity for attention capture |
| R3 [8] | loudness | Perceived intensity for intervention response |
| R3 [14] | warmth | Vocal warmth for singing quality proxy |
| R3 [17] | spectral_flatness | Voice vs noise discrimination gate |
| H3 | 8 tuples (see above) | Multi-scale vocal quality and attention dynamics |
| DSP (NDU-beta1) | Empirical base | DSP provides the intervention evidence that SDDP's sex effects draw from |
