# HMCE — Extraction

**Model**: Hierarchical Musical Context Encoding
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: E — Extraction
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_short_context | Short-range context encoding (10-50 notes). Captures local melodic/harmonic patterns within a phrase. σ(0.40 * spectral_auto_periodicity_100ms + 0.35 * onset_periodicity_500ms + 0.25 * amplitude_std_100ms). Maps to Heschl's gyrus (HG) and primary auditory cortex. Bonetti 2024: HG drives feedforward hierarchy. |
| 1 | f02_medium_context | Medium-range context encoding (50-150 notes). Captures phrase-level structure and harmonic progression patterns. σ(0.40 * tonal_stability_mean_500ms + 0.35 * spectral_flux_trend_1s + 0.25 * f01). Maps to STG and planum temporale. Norman-Haignere 2022: temporal receptive fields increase posterior→anterior. |
| 2 | f03_long_context | Long-range context encoding (150-300+ notes). Captures section-level structure, key areas, and global form. σ(0.40 * tonal_stability_mean_1s + 0.35 * key_clarity_entropy_1s + 0.25 * f02). Maps to MTG and anterior temporal lobe. Rimmele 2021: phrase-level chunking at >1s timescales. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 17 | 3 | M14 (periodicity) | L0 | Spectral autocorrelation periodicity 100ms — local regularity |
| 1 | 17 | 3 | M2 (std) | L0 | Spectral autocorrelation variability 100ms — local change |
| 2 | 11 | 8 | M14 (periodicity) | L0 | Onset periodicity 500ms — phrase-level beat |
| 3 | 7 | 3 | M2 (std) | L0 | Amplitude variability 100ms — event detection |
| 4 | 60 | 8 | M1 (mean) | L0 | Mean tonal stability 500ms — harmonic context |
| 5 | 21 | 16 | M18 (trend) | L0 | Spectral flux trend 1s — structural change direction |
| 6 | 60 | 16 | M1 (mean) | L0 | Mean tonal stability 1s — long-range harmonic context |
| 7 | 51 | 16 | M13 (entropy) | L0 | Key clarity entropy 1s — structural uncertainty |

---

## Computation

The E-layer implements the hierarchical context encoding model (Bonetti 2024; Norman-Haignere 2022). Three context ranges are computed in increasing temporal scope:

1. **Short context** (f01): Driven by local spectral periodicity and onset regularity at 100-500ms. Captures note-to-note and motif-level patterns. Correlation with cortical distance r=0.99 (Norman-Haignere 2022) confirms hierarchical temporal receptive fields.

2. **Medium context** (f02): Extends to phrase-level (500ms-1s). Integrates tonal stability and spectral change trends. Depends on f01 (hierarchical buildup). Maps to secondary auditory areas (STG belt regions).

3. **Long context** (f03): Captures section and form-level structure (1s+). Integrates long-range tonal stability and key uncertainty. Depends on f02 (hierarchical continuation). Maps to anterior temporal lobe and association cortex.

All formulas use sigmoid activation with coefficient sums ≤ 1.0.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [7] | amplitude | Event detection for context boundaries |
| R³ [11] | onset_strength | Beat marker for phrase-level timing |
| R³ [17] | spectral_autocorrelation | Local regularity proxy |
| R³ [21] | spectral_flux | Structural change signal |
| R³ [51] | key_clarity | Tonal context strength |
| R³ [60] | tonal_stability | Harmonic context at multiple scales |
| H³ | 8 tuples (see above) | Multi-scale context features |
