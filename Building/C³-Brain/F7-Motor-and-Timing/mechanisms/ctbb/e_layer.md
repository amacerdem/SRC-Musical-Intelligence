# CTBB — Extraction

**Model**: Cerebellar Theta-Burst Balance
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: E — Extraction
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f25_cerebellar_timing | Cerebellar timing enhancement from iTBS effect. Captures how strongly the cerebellar timing circuit is engaged, estimated from coupling stability and periodicity. f25 = sigma(0.40 * coupling_stability_1s). Sansare 2025: cerebellar iTBS reduces postural sway (eta-sq = 0.202, F = 9.600, p = .004). Okada 2022: cerebellar dentate contains 3 functional neuron types for rhythm prediction, timing control, and error detection. |
| 1 | f26_m1_modulation | Motor cortex excitability modulation via cerebellar-M1 pathway. Estimates the degree of M1 excitability change driven by cerebellar output, combining coupling periodicity and fast cerebellar signal. f26 = sigma(0.30 * coupling_period_1s + 0.30 * cerebellar_100ms). Sansare 2025: CBI null result (eta-sq = 0.045 n.s.) suggests alternative circuits may mediate the effect. Shi 2025: bilateral M1 iTBS enhances gait automaticity (F = 5.558, p = .026). |
| 2 | f27_postural_control | Balance improvement from cerebellar-M1 interaction. Integrates timing and modulation with balance variability and motor amplitude. f27 = sigma(0.35 * f25 * f26 + 0.35 * (1 - balance_var_1s) + 0.30 * mean_amplitude_1s). Sansare 2025: sway reduction sustained >= 30 min post-iTBS; Bonferroni POST1-6 all p < .05. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 16 | M19 (stability) | L0 (fwd) | Coupling stability 1s |
| 1 | 25 | 16 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 1s |
| 2 | 25 | 3 | M0 (value) | L2 (bidi) | Cerebellar coupling 100ms |
| 3 | 33 | 16 | M2 (std) | L0 (fwd) | Balance variability 1s |
| 4 | 7 | 16 | M1 (mean) | L2 (bidi) | Mean motor output 1s |

---

## Computation

The E-layer extracts three explicit features that characterize cerebellar timing enhancement and its downstream effects on motor cortex and postural control. The key insight is that cerebellar iTBS causally modulates motor timing precision through the cerebellar-M1 circuit (Sansare 2025, Okada 2022).

All features use sigmoid activation with coefficient sums equal to 1.0 (saturation rule).

1. **f25** (cerebellar timing): Estimates the cerebellar timing enhancement level from coupling stability at 1s. This captures the core iTBS effect on the cerebellum's timing function, supported by Sansare 2025's causal TMS evidence and Okada 2022's single-neuron recording showing three functional neuron types in the cerebellar dentate nucleus.

2. **f26** (M1 modulation): Estimates motor cortex excitability change by combining coupling periodicity at 1s with the fast cerebellar signal at 100ms. Note the CBI null result (Sansare 2025) suggests this pathway's contribution is uncertain; balance improvements may involve cerebellar-prefrontal or cerebellar-vestibular routes.

3. **f27** (postural control): Integrates the f25 x f26 interaction (timing x modulation) with inverted balance variability (lower variability = better control) and mean motor amplitude. The interaction term captures the synergy between cerebellar timing precision and M1 excitability for balance maintenance.

H3 tuples span H3 (100ms) through H16 (1s), using a mix of L0 (forward) and L2 (bidirectional) laws. The fast cerebellar signal (H3, L2) captures immediate timing, while stability and periodicity features require longer windows (H16) for reliable estimation.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R3[7] amplitude | Motor output level | Mean amplitude for postural control estimation |
| R3[10] spectral_flux | Timing dynamics | Cerebellar tempo tracking signal |
| R3[21] spectral_change | Timing rate change | Motor adjustment dynamics |
| R3[22] energy_change | Energy dynamics | Postural sway proxy |
| R3[25:33] x_l0l5 | Cerebellar-M1 modulation | Coupling stability and periodicity for timing |
| R3[33:41] x_l4l5 | Balance monitoring | Balance variability for postural control |
| H3 (5 tuples) | Multi-scale temporal morphology | Coupling and balance dynamics at 100ms-1s |
