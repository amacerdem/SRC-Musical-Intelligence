# SDDP — Forecast

**Model**: Sex-Dependent Developmental Plasticity
**Unit**: NDU
**Function**: F11 Development & Evolution
**Tier**: gamma
**Layer**: F — Forecast
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 8 | mmr_development | Sex-specific MMR trajectory prediction. Estimates the developmental trajectory of mismatch response amplitude given accumulated intervention exposure and sex modulation. sigma(0.35 * intervention_accum + 0.35 * prenatal_baseline) * f01. Partanen 2022: singing group showed enhanced MMR; males showed stronger enhancement (eta^2=0.309). Range [0, 1]. |
| 9 | language_outcomes | Long-term speech-language development prediction. Estimates downstream language outcomes from current plasticity state, linking auditory MMR enhancement to speech-language development. sigma(0.35 * mmr_development + 0.35 * attention_modulation). Nayak et al. 2025 (via ONI references): rhythm impairment is a risk factor for speech-language disorders (OR=1.33, p<0.0001). Range [0, 1]. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 23 | 16 | M1 (mean) | L2 (bidi) | Mean pitch change over 1s for trajectory estimation |

---

## Computation

The F-layer generates two forward-looking predictions about developmental outcomes:

1. **MMR development** (idx 8): Predicts the sex-specific trajectory of mismatch response maturation. Combines the M-layer's intervention_accum (cumulative singing exposure) and prenatal_baseline (starting auditory capacity), scaled by the E-layer's sex modulation factor. This implements the core SDDP prediction: given equivalent intervention dosage, male infants are expected to show ~31% stronger MMR enhancement. The prediction is speculative (gamma-tier) and based on a single study with n=21.

2. **Language outcomes** (idx 9): Links current MMR development to long-term speech-language predictions. This is the most distal prediction in the model, grounded in the established relationship between early auditory plasticity (indexed by MMR) and subsequent language development. Yu et al. 2015 review MMN as an index of neural plasticity; Nayak et al. 2025 demonstrate that rhythm processing abilities predict speech-language disorder risk (OR=1.33). The sex-dependent component suggests that differential early plasticity rates could lead to sex-differentiated language developmental trajectories.

Both F-layer dimensions are maximally speculative and serve as testable hypotheses rather than confident predictions. They require longitudinal follow-up studies tracking preterm infants from intervention through language acquisition milestones.

All sigmoid formulas use coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| H3 | 1 tuple (see above) | Mean pitch change over 1s for trajectory context |
| E-layer | f01_sex_modulation | Sex-dependent scaling of MMR trajectory |
| M-layer | intervention_accum, prenatal_baseline | Cumulative exposure and starting state for trajectory |
| P-layer | attention_modulation | Current attentional engagement for language outcome prediction |
