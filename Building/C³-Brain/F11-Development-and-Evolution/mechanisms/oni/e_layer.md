# ONI — Extraction

**Model**: Over-Normalization in Intervention
**Unit**: NDU
**Function**: F11 Development & Evolution
**Tier**: gamma
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_over_normalization | Enhancement beyond full-term baseline. Ratio index: MMR_intervention / (MMR_fullterm + epsilon). Values > 1.0 indicate over-normalization where intervention group exceeds full-term norms. Partanen 2022: singing intervention preterm infants showed larger oddball MMR than full-term controls (eta^2=0.229, p=0.030). Range [0, 2]. |
| 1 | f02_compensatory_response | Enhanced predictive processing magnitude. sigma(0.35 * spectral_change_100ms + 0.35 * coupling_mean_1s). Captures the hypothesized compensatory adaptation where preterm auditory cortex develops enhanced spectral prediction capacity through intervention. Blasi et al. 2025: music interventions produce compensatory neural changes that can exceed baseline. Range [0, 1]. |
| 2 | f03_attention_enhancement | Heightened deviance detection capacity. sigma(0.35 * brightness_100ms + 0.35 * tonal_entropy_100ms). Captures the alternative explanation that over-normalization reflects enhanced attentional orienting rather than true over-development. Scholkmann 2024: prefrontal StO2 +2.4% (p=0.008) during CMT. Range [0, 1]. |
| 3 | f04_intervention_ceiling | Response saturation point. 1 - exp(-dosage / tau_ceil), tau_ceil=4 weeks (hypothesized). Models the diminishing returns of continued intervention, predicting a ceiling effect at high dosages. Range [0, 1]. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 0 | M0 (value) | L2 (bidi) | Instantaneous spectral flux deviance at 25ms gamma |
| 1 | 10 | 3 | M2 (std) | L2 (bidi) | Deviance variability at 100ms alpha |
| 2 | 10 | 16 | M1 (mean) | L2 (bidi) | Mean deviance magnitude over 1s beat |
| 3 | 11 | 0 | M0 (value) | L2 (bidi) | Onset deviance at 25ms gamma |
| 4 | 11 | 3 | M0 (value) | L2 (bidi) | Onset strength at 100ms alpha |
| 5 | 13 | 3 | M0 (value) | L2 (bidi) | Tonal brightness at 100ms alpha |
| 6 | 13 | 3 | M20 (entropy) | L2 (bidi) | Tonal entropy at 100ms alpha |
| 7 | 21 | 3 | M0 (value) | L2 (bidi) | Spectral change at 100ms alpha |

---

## Computation

The E-layer extracts four explicit features characterizing the over-normalization phenomenon observed in musical intervention with preterm infants:

1. **Over-normalization index** (f01): The core finding -- a ratio comparing intervention-group MMR amplitude to full-term baseline. When this ratio exceeds 1.0, the preterm intervention group has surpassed full-term norms, which is the unexpected result reported by Partanen 2022. The E-layer proxies this from spectral flux deviance magnitude and onset strength, as these R3 features capture the acoustic deviance processing that MMR indexes neurally.

2. **Compensatory response** (f02): Models the enhanced predictive processing hypothesis. Uses spectral change at 100ms and dynamic-percept coupling mean over 1s to capture whether the intervention has driven the developing auditory cortex to build stronger internal models. Coefficients sum to 0.70 before implicit 0.30 bias (saturation rule).

3. **Attention enhancement** (f03): Models the alternative attentional explanation. Uses tonal brightness and tonal entropy at 100ms to capture heightened attentional orienting to acoustic features. Tervaniemi 2022 notes that MMR paradigm design affects whether responses reflect prediction or attention. The attention enhancement dimension allows the model to represent this alternative mechanism.

4. **Intervention ceiling** (f04): An exponential saturation function modeling the diminishing returns of continued intervention exposure. The hypothesized ceiling constant of 4 weeks reflects a speculative estimate of the dosage at which MMR enhancement plateaus.

All sigmoid formulas use coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [10] | spectral_flux | Deviance magnitude for MMR proxy |
| R3 [11] | onset_strength | Onset deviance for rhythmic processing |
| R3 [13] | brightness | Tonal quality for attention enhancement |
| R3 [21] | spectral_change | Spectral dynamics for compensatory response |
| H3 | 8 tuples (see above) | Multi-scale deviance, onset, tonal, and spectral dynamics |
| DSP (NDU-beta1) | Plasticity evidence | DSP provides empirical data that revealed the over-normalization effect |
| SDDP (NDU-gamma1) | Sex component | Sex-dependent modulation of the over-normalization effect |
