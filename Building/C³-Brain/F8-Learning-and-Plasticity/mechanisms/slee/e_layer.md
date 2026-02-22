# SLEE — Extraction

**Model**: Statistical Learning Expertise Enhancement
**Unit**: NDU
**Function**: F8 Learning & Plasticity
**Tier**: β
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_statistical_model | Internal distribution representation. Captures how strongly the statistical model of the auditory environment is built from loudness and amplitude entropy. f01 = σ(0.35 * loudness_mean_100ms + 0.35 * amplitude_entropy_100ms). Paraskevopoulos 2022: musicians show enhanced statistical learning accuracy (Hedges' g = -1.09). Carbajal & Malmierca 2018: predictive coding hierarchy from SSA to MMN to deviance detection. |
| 1 | f02_detection_accuracy | Irregularity identification rate. Measures the ability to detect statistical irregularities in the auditory stream from spectral flux variability and mean. f02 = σ(0.35 * flux_std_100ms + 0.35 * flux_mean_1s). Paraskevopoulos 2022: t(23) = -2.815, p < 0.05 for musician > non-musician detection accuracy. Bridwell 2017: 45% amplitude reduction for patterned vs random sequences. |
| 2 | f03_multisensory_integration | Cross-modal binding strength. Estimates the degree of multisensory integration from interaction feature binding at 100ms and 1s timescales. f03 = σ(0.35 * binding_100ms + 0.35 * mean_binding_1s). Paraskevopoulos 2022: IFG (area 47m left) is primary supramodal hub across 5/6 network states. Porfyri et al. 2025: multisensory training improves audiovisual incongruency detection (η² = 0.168). |
| 3 | f04_expertise_advantage | Expert enhancement index. Reflects the difference in detection accuracy between musicians and non-musicians. f04 = clamp(f02 * expertise_indicator, -1, 1). Paraskevopoulos 2022: d = -1.09 (large expertise effect); network compartmentalization: 192 edges (NM) vs 106 edges (M), p < 0.001 FDR. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 8 | 3 | M1 (mean) | L2 (bidi) | Mean loudness 100ms |
| 1 | 7 | 3 | M20 (entropy) | L2 (bidi) | Amplitude entropy 100ms |
| 2 | 10 | 3 | M2 (std) | L2 (bidi) | Spectral flux variability 100ms |
| 3 | 10 | 16 | M1 (mean) | L2 (bidi) | Mean spectral flux over 1s |
| 4 | 41 | 3 | M0 (value) | L2 (bidi) | Cross-modal binding 100ms |
| 5 | 41 | 16 | M1 (mean) | L2 (bidi) | Mean binding over 1s |
| 6 | 10 | 0 | M0 (value) | L2 (bidi) | Instantaneous irregularity 25ms |

---

## Computation

The E-layer extracts four explicit features that characterize statistical learning capacity and expertise-dependent enhancement. The key insight is that musical expertise enhances behavioral accuracy in identification of multisensory statistical irregularities, linked to compartmentalized network reorganization (Paraskevopoulos 2022).

All features use sigmoid activation with coefficient sums equal to 1.0 (saturation rule), except f04 which uses clamped scaling.

1. **f01** (statistical model): Estimates the internal distribution representation from mean loudness and amplitude entropy at 100ms. This captures the quality of the statistical model that the auditory system builds from repeated exposure, supported by Carbajal & Malmierca 2018's predictive coding hierarchy.

2. **f02** (detection accuracy): Estimates irregularity detection ability from spectral flux variability at 100ms and mean spectral flux over 1s. This reflects the core behavioral finding from Paraskevopoulos 2022 showing musicians' superior irregularity identification.

3. **f03** (multisensory integration): Estimates cross-modal binding from interaction features at 100ms and 1s. The IFG area 47m serves as the primary supramodal hub (Paraskevopoulos 2022), and multisensory training specifically improves audiovisual detection (Porfyri et al. 2025).

4. **f04** (expertise advantage): Scales detection accuracy by an expertise indicator. This dimension captures the large effect size (d = -1.09) between musician and non-musician statistical learning performance.

H³ tuples span H0 (25ms) through H16 (1s), primarily using L2 (bidirectional) laws for template-building statistical integration.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³[7] amplitude | Acoustic intensity | Amplitude entropy for statistical model estimation |
| R³[8] loudness | Perceptual loudness | Mean loudness for distribution model |
| R³[10] spectral_flux | Spectral change rate | Irregularity detection and variability |
| R³[41:49] x_l5l6 | Multi-feature coherence | Cross-modal binding proxy for multisensory integration |
| H³ (7 tuples) | Multi-scale temporal morphology | Loudness, entropy, flux, and binding dynamics at 25ms-1s |
