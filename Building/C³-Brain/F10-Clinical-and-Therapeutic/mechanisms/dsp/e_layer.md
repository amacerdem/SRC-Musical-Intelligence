# DSP — Extraction

**Model**: Developmental Singing Plasticity
**Unit**: NDU
**Function**: F10 Clinical & Therapeutic
**Tier**: beta
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_singing_quality | Vocal quality index. Composite of consonance and warmth at 100ms alpha timescale, gated by voice tonality (1 - spectral_flatness). sigma(0.35 * consonance_100ms + 0.35 * warmth_100ms). Partanen 2022: singing quality predicts outcomes better than quantity (eta^2=0.262, p=0.030). Scholkmann 2024: CMT singing drives StO2 increase 3.2+/-2.0% in auditory cortex (r_rb=1.00, p=0.002). |
| 1 | f02_attention_engagement | Infant attention capture. Combines instantaneous intensity at 25ms gamma with perceived loudness at 100ms and mean loudness over 500ms delta window. sigma(0.35 * loudness_100ms + 0.35 * mean_loudness_500ms). Scholkmann 2024: StO2 increase 2.4+/-1.1% in prefrontal cortex (r_rb=1.00, p=0.008) during CMT, reflecting attention engagement. |
| 2 | f03_plasticity_index | Neural maturation rate. Driven by melodic contour entropy at 125ms theta and vocal periodicity at 100ms alpha, capturing the richness of vocal stimulation that drives quality-dependent plasticity. sigma(0.35 * contour_entropy_125ms + 0.35 * vocal_periodicity_100ms). Partanen 2022: group x singing time interaction eta^2=0.262 — quality-dependent neural maturation. |
| 3 | f04_sex_modulation | Sex-dependent response modulation. Scales plasticity index by sex effect size from Partanen 2022. clamp(f03 * (1 + 0.309 * sex_indicator), 0, 1). Partanen 2022: sex x singing time interaction eta^2=0.309, p=0.017 — males show stronger MMR enhancement for vowel duration deviants (p=0.001). Scholkmann 2024: females show greater positive cerebrovascular response (tau_b=-0.514, p=0.034). |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 4 | 3 | M0 (value) | L2 (bidi) | Vocal consonance at 100ms alpha |
| 1 | 14 | 3 | M0 (value) | L2 (bidi) | Vocal warmth at 100ms alpha |
| 2 | 17 | 3 | M0 (value) | L2 (bidi) | Voice/noise tonality ratio at 100ms |
| 3 | 7 | 0 | M0 (value) | L2 (bidi) | Instantaneous vocal intensity at 25ms gamma |
| 4 | 8 | 3 | M0 (value) | L2 (bidi) | Perceived loudness at 100ms alpha |
| 5 | 8 | 8 | M1 (mean) | L2 (bidi) | Mean perceived loudness over 500ms delta |
| 6 | 23 | 4 | M20 (entropy) | L2 (bidi) | Melodic contour entropy at 125ms theta |
| 7 | 25 | 3 | M14 (periodicity) | L2 (bidi) | Vocal periodicity at 100ms alpha |

---

## Computation

The E-layer extracts four explicit features characterizing singing-driven developmental plasticity:

1. **Singing quality** (f01): Combines vocal consonance and warmth at the 100ms alpha timescale, with spectral flatness providing a voice-versus-noise quality gate. This captures the acoustic quality of parental singing that Partanen 2022 demonstrated to be the primary driver of auditory plasticity in preterm infants — quality of singing predicts outcomes better than quantity. Higher consonance and warmth indicate richer harmonic structure in the singing voice, which maps to stronger auditory cortex activation (Scholkmann 2024: bilateral AC StO2 increase).

2. **Attention engagement** (f02): Driven by perceived loudness at 100ms and its 500ms running mean, with instantaneous intensity at 25ms for onset capture. This reflects the infant's attentional response to parental singing — louder, more dynamically varied singing captures and sustains neonatal attention. Maps to prefrontal cortex activation (Scholkmann 2024: right PFC StO2 increase during CMT sessions).

3. **Plasticity index** (f03): Combines melodic contour entropy at 125ms theta timescale with vocal periodicity at 100ms alpha. Contour entropy measures the informational richness of the singing melody — high entropy indicates varied, complex melodic contours that provide richer stimulation. Vocal periodicity captures the regularity of the singing voice that enables statistical learning. Together they quantify the quality-dependent plasticity driver identified by Partanen 2022.

4. **Sex modulation** (f04): Multiplicative scaling of plasticity index by the sex-dependent effect size (eta^2=0.309). Males in the singing intervention group showed significantly stronger MMR enhancement than females for vowel duration deviants (Partanen 2022, p=0.001). At the cerebrovascular level, females showed a different pattern with greater positive StO2 response (Scholkmann 2024), suggesting sex differences may reflect distinct processing levels rather than a simple magnitude difference.

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [4] | consonance | Vocal harmonic quality for singing quality index |
| R3 [7] | amplitude | Instantaneous vocal intensity for attention capture |
| R3 [8] | loudness | Perceived intensity for attention engagement |
| R3 [14] | warmth | Vocal warmth for singing quality index |
| R3 [17] | spectral_flatness | Voice vs noise discrimination gate |
| R3 [23] | pitch_change | Melodic contour for entropy computation |
| R3 [25] | x_l0l5[0] | Vocal coupling for periodicity extraction |
| H3 | 8 tuples (see above) | Multi-scale vocal quality, attention, and plasticity dynamics |
