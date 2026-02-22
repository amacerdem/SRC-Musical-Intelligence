# CDMR — Extraction

**Model**: Context-Dependent Mismatch Response
**Unit**: NDU
**Function**: F8 Learning & Plasticity
**Tier**: β
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_mismatch_amplitude | Deviance response magnitude. Basic mismatch detection signal from spectral flux and onset strength at 25ms gamma timescale. σ(0.35 * flux_25ms + 0.35 * onset_25ms). Crespo-Bojorque 2018: consonance MMN in both musicians and non-musicians (172-250ms), p=0.007 (non-mus), p=0.001 (mus). Wagner 2018: MMN for major third deviant -0.34uV +/- 0.32, p=0.003. |
| 1 | f02_context_modulation | Context-dependent enhancement. Melodic context complexity that modulates mismatch responses, driven by pitch change dynamics at 100ms and 1s horizons. σ(0.35 * pitch_change_100ms + 0.35 * mean_pitch_change_1s). Crespo-Bojorque 2018: musicians show consonance MMN > dissonance MMN, right-lateralized F(1,15)=4.95, p<0.05. Dissonance condition latency >> consonance: F(1,15)=155.03, p<0.001. |
| 2 | f03_subadditivity_index | Integration vs summation measure. Response to combined deviants less than sum of individual responses, indicating integrated processing. σ(0.35 * binding_100ms + 0.35 * binding_variability_100ms). Rupp/Hansen 2022: musicians > non-musicians in subadditivity for combined melodic deviants (MEG). |
| 3 | f04_expertise_effect | Expertise-context interaction. Difference between complex and simple context mismatch responses scaled by expertise. clamp((f01_complex - f01_simple) * expertise_indicator, -1, 1). Rupp/Hansen 2022: no group difference in classic oddball, but musicians > non-musicians in complex melodic paradigm. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 0 | M0 (value) | L2 (bidi) | Instantaneous deviance at 25ms |
| 1 | 10 | 3 | M2 (std) | L2 (bidi) | Deviance variability at 100ms |
| 2 | 11 | 0 | M0 (value) | L2 (bidi) | Onset deviance at 25ms |
| 3 | 11 | 3 | M8 (velocity) | L0 (fwd) | Onset velocity at 100ms |
| 4 | 23 | 3 | M0 (value) | L2 (bidi) | Pitch deviance at 100ms |
| 5 | 23 | 16 | M1 (mean) | L2 (bidi) | Mean pitch change over 1s |
| 6 | 41 | 3 | M0 (value) | L2 (bidi) | Binding strength at 100ms |
| 7 | 41 | 3 | M2 (std) | L2 (bidi) | Binding variability at 100ms |

---

## Computation

The E-layer extracts four explicit features characterizing context-dependent mismatch responses:

1. **Mismatch amplitude** (f01): Driven by spectral flux and onset strength at 25ms gamma timescale. This captures the basic deviance detection signal — how much the current frame deviates from expectations. Present in both musicians and non-musicians for simple contexts. Maps to bilateral auditory cortex A1/STG (Rupp 2022: MEG; Wagner 2018: BESA dipole source reconstruction).

2. **Context modulation** (f02): Driven by pitch change complexity at 100ms and 1s horizons. Captures how melodic context richness modulates the mismatch response. Complex melodic contexts (high pitch variability, rich melodic structure) amplify mismatch detection selectively in experts. Maps to anterior auditory cortex (Rupp 2022: pitch contour tracking gradient).

3. **Subadditivity index** (f03): Driven by cross-feature binding strength and variability at 100ms from x_l5l6 interactions. Subadditivity (combined < sum of individual) indicates integrated rather than additive processing of multiple deviant features. Higher values reflect more expert-like integration. Maps to fronto-central cortex (Crespo-Bojorque 2018: Fz electrode).

4. **Expertise effect** (f04): Interaction term capturing the context-dependent expertise advantage. Zero in simple oddball contexts, positive in complex melodic contexts for musicians. Computed as the product of f01 and f02, scaled by an expertise indicator. Maps to right IFG (Koelsch: ERAN generators).

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [10] | spectral_flux | Frame-level deviance magnitude for mismatch detection |
| R³ [11] | onset_strength | Onset deviation for rhythmic deviance detection |
| R³ [23] | pitch_change | Melodic context complexity for context modulation |
| R³ [41:49] | x_l5l6 | Perceptual-shape coupling for subadditivity computation |
| H³ | 8 tuples (see above) | Multi-scale deviance, context, and binding dynamics |
