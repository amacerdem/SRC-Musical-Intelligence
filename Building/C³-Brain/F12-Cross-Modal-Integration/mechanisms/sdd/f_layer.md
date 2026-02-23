# SDD — Forecast

**Model**: Supramodal Deviance Detection
**Unit**: NDU
**Function**: F12 Cross-Modal Integration
**Tier**: alpha
**Layer**: F — Forecast
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 9 | expectation_update | 300ms-ahead learning signal for statistical model updating. Captures how strongly the current deviance should modify the listener's statistical regularity model. Driven by present-moment deviance signal (P-layer) and spectral flux periodicity at 1s beat timescale -- periodic flux patterns indicate stable regularity that can be efficiently updated, while aperiodic flux requires more cautious updating. sigma(0.40 * deviance_signal + 0.30 * supramodal_ratio + 0.30 * flux_periodicity_1s). Fong 2020: MMN under predictive coding operates at 150-250ms latency with hierarchical prediction error propagation; the F-layer extends this to a 300ms forward prediction window for expectation revision. |
| 10 | attention_reorienting | 100-200ms frontal attention allocation prediction. Captures the anticipated attentional shift triggered by deviance detection -- how strongly the frontal network will reorient attention to the deviant stimulus. Driven by IFG state (P-layer) and multilink activation, reflecting that attention reorienting is proportional to both hub engagement and cross-modal binding breadth. sigma(0.40 * ifg_state + 0.30 * multilink_activation + 0.30 * deviance_signal). Kim 2021: IFG-LTDMI enhanced for syntactic irregularity F(2,36)=6.526; Porfyri 2025: left MFG/IFS/insula central nodes for multisensory-induced neuroplasticity. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 17 | 10 | 16 | M14 (periodicity) | L2 (bidi) | Flux periodicity at 1s beat |

---

## Computation

The F-layer generates two forward-looking predictions from the SDD processing cascade:

1. **Expectation update** (idx 9): The predicted revision to the listener's statistical regularity model. This is the key output for predictive coding -- when deviance is detected, the brain must decide how much to update its generative model vs treating the event as noise. The computation combines the present deviance signal (how strong is the current irregularity), the supramodal ratio (how cross-modal is the deviance -- cross-modal deviants demand stronger model updating), and flux periodicity at 1s (how regular is the spectral environment -- regular environments produce more confident predictions that require larger updates when violated). Fong 2020 reviewed MMN under predictive coding, establishing the 150-250ms latency for hierarchical prediction error; the F-layer extends this to a 300ms forecast horizon appropriate for the beat timescale.

2. **Attention reorienting** (idx 10): The predicted frontal attention shift. When deviance is detected by the supramodal mechanism, attentional resources are redirected from ongoing processing to the deviant event. The IFG state (from P-layer) indexes hub engagement -- stronger hub activation predicts stronger reorienting. Multilink activation captures the breadth of cross-modal involvement -- when deviance is detected supramodally (across modalities), attention reorienting is more forceful than when deviance is limited to a single channel. Kim 2021 dissociated IFG-LTDMI (syntactic irregularity) from STG-LTDMI (perceptual ambiguity), confirming that the IFG specifically drives frontal reorienting for structural violations.

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| P-layer | deviance_signal | Current deviance for expectation revision |
| P-layer | multilink_activation | Cross-modal binding for reorienting breadth |
| P-layer | ifg_state | Hub engagement for frontal reorienting |
| M-layer | supramodal_ratio | Temporal stability for update magnitude |
| R3 [10] | spectral_flux | Spectral regularity context for updating |
| H3 | 1 tuple (see above) | Flux periodicity at 1s beat |
