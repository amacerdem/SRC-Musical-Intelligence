# SDDP — Temporal Integration

**Model**: Sex-Dependent Developmental Plasticity
**Unit**: NDU
**Function**: F11 Development & Evolution
**Tier**: gamma
**Layer**: M — Temporal Integration
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 4 | prenatal_baseline | Baseline developmental state. Pitch-processing oscillation strength proxy computed from vocal periodicity at 100ms alpha timescale. sigma(0.50 * vocal_periodicity_100ms). Reflects the infant's pre-intervention auditory processing capacity. Range [0, 1]. |
| 5 | hormonal_state | Sex differentiation proxy. Derived from f01_sex_modulation (E-layer) as a continuous representation of sex-dependent hormonal influence on plasticity. Captures the hypothesized role of sex hormones in modulating the plasticity window timing or magnitude. Partanen 2022: eta^2=0.309. Range [0, 1]. |
| 6 | intervention_accum | Cumulative intervention exposure. Exponential moving average of vocal coupling at 1s beat timescale: mean_vocal_coupling_1s (H3 tuple 25,16,M1,L0). Tracks the accumulated effect of singing intervention over time, serving as a dosage proxy. Range [0, 1]. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 3 | M14 (periodicity) | L2 (bidi) | Vocal periodicity at 100ms alpha for prenatal baseline |
| 1 | 25 | 16 | M1 (mean) | L0 (fwd) | Mean vocal coupling over 1s for intervention accumulation |
| 2 | 13 | 3 | M0 (value) | L2 (bidi) | Pitch brightness at 100ms for baseline calibration |
| 3 | 13 | 4 | M17 (periodicity) | L2 (bidi) | Pitch periodicity at 125ms theta for developmental tracking |

---

## Computation

The M-layer integrates temporal dynamics of the sex-dependent developmental plasticity process across three dimensions:

1. **Prenatal baseline** (idx 4): Estimates the infant's starting auditory processing capacity before or at the onset of intervention. Computed from vocal periodicity at the 100ms alpha timescale, which captures how regularly the singing voice is produced. Higher periodicity indicates more structured vocal input that the developing auditory cortex can track. The sigmoid activation with 0.50 coefficient ensures bounded output.

2. **Hormonal state** (idx 5): A continuous proxy for sex-dependent hormonal modulation of plasticity. Directly derived from the E-layer f01_sex_modulation factor. This is the most speculative dimension in the model -- the hypothesis that sex hormones modulate plasticity window timing or magnitude remains untested. Jasinskyte & Guzulaitis 2025 provide indirect support showing males have stronger 40Hz ASSR gamma-band entrainment at baseline in mouse auditory cortex.

3. **Intervention accumulation** (idx 6): Tracks cumulative singing exposure using the mean vocal coupling signal over a 1-second beat timescale. This is the only L0 (forward-only) law tuple in SDDP's M-layer, reflecting that intervention dosage is inherently a forward-accumulating quantity. The EMA formulation allows the model to capture both recent and historical exposure effects.

The M-layer provides the developmental dynamics context that the P-layer uses for attention modulation and the F-layer uses for trajectory prediction.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [13] | brightness | Pitch brightness for baseline calibration |
| R3 [25] | x_l0l5[0] | Vocal coupling for periodicity and accumulation |
| H3 | 4 tuples (see above) | Multi-scale vocal periodicity and coupling dynamics |
| E-layer | f01_sex_modulation | Hormonal state derives from sex modulation factor |
