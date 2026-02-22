# SPMC — Forecast

**Model**: SMA-Premotor-M1 Motor Circuit
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: β
**Layer**: F — Forecast
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 8 | sequence_pred | Sequence planning prediction. Forecasts upcoming SMA sequence encoding by combining current planning state with beat periodicity. sequence_pred = σ(0.5 * f19 + 0.5 * beat_period_1s). Grahn & Brett 2007: SMA encodes beat expectation in metric rhythms. Hoddinott & Grahn 2024: SMA beat-strength patterns are predictive. |
| 9 | execution_pred | Motor execution prediction. Forecasts upcoming M1 output by combining current execution with tempo variability and sequence stability. Okada 2022: cerebellar dentate neurons encode timing of next movement. Harrison 2025: CTC pathway provides predictive motor timing. |
| 10 | timing_pred | Timing precision prediction. Forecasts cerebellar timing accuracy by combining current timing precision with tempo variability and sequence stability. Okada 2022: 1/3 of dentate neurons are selectively active for synchronized vs reactive movements, encoding predictive timing. Thaut 2015: rhythmic entrainment via reticulospinal pathways enables anticipatory timing. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 16 | M14 (periodicity) | L2 (bidi) | Beat periodicity 1s for sequence prediction |
| 1 | 21 | 16 | M1 (mean) | L0 (fwd) | Mean tempo change 1s for execution prediction |
| 2 | 21 | 16 | M2 (std) | L0 (fwd) | Tempo variability 1s for timing prediction |
| 3 | 33 | 16 | M19 (stability) | L0 (fwd) | Sequence stability 1s for execution prediction |

---

## Computation

The F-layer generates three forward-looking predictions for the motor circuit:

1. **Sequence Prediction (dim 8)**: Forecasts upcoming SMA sequence encoding. Combines the current sequence planning state (f19) with the 1s beat periodicity to predict whether the SMA will continue encoding regular motor sequences. Strong beat periodicity with active planning yields high sequence predictions.

2. **Execution Prediction (dim 9)**: Forecasts upcoming M1 motor output. Uses current execution output combined with forward-looking tempo and stability features. Tempo mean and sequence stability at 1s horizon provide the predictive context -- stable tempo with consistent sequences predicts continued motor execution.

3. **Timing Prediction (dim 10)**: Forecasts cerebellar timing precision. Combines current timing precision with tempo variability (std) and sequence stability. Low tempo variability and high sequence stability predict maintained timing precision. This reflects the cerebellum's anticipatory timing function demonstrated by Okada 2022.

All F-layer dimensions use forward-looking (L0) H³ features at the 1s horizon and E-layer features as predictive context, consistent with the motor system's anticipatory planning role.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer [0] | f19_sequence_planning | Current planning state for sequence prediction |
| E-layer [2] | f21_execution_output | Current execution for execution prediction |
| M-layer [5] | timing_precision | Current timing for timing prediction |
| R³ [10] | spectral_flux | Beat periodicity for sequence prediction |
| R³ [21] | spectral_change | Tempo dynamics for execution and timing prediction |
| R³ [33:41] | x_l4l5 | Sequence stability for execution and timing prediction |
| H³ | 4 tuples (see above) | Forward-looking 1s horizon features |
