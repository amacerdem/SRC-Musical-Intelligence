# IUCP — Extraction

**Model**: Inverted-U Complexity Preference
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: β
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_ic_liking_curve | Inverted-U for information content (IC). σ(0.40 * ic_quadratic + 0.30 * mean_pleasantness_1s). ic_quadratic = 4.0 * mean_ic_1s * (1.0 - mean_ic_1s), peaks at 0.5. Gold 2019: IC quadratic β_quad = -0.09 (p < 0.001), R² = 26.3% (Study 1, N = 43); replicated β_quad = -0.18, R² = 41.6% (Study 2, N = 27). |
| 1 | f02_entropy_liking_curve | Inverted-U for entropy. σ(0.40 * entropy_quadratic + 0.30 * concentration_entropy_1s). entropy_quadratic = 4.0 * concentration_entropy_1s * (1.0 - concentration_entropy_1s). Gold 2019: entropy quadratic β_quad = -0.06 (p = 0.003), R² = 19.1% (Study 1); replicated β_quad = -0.25, R² = 34.9% (Study 2). |
| 2 | f03_ic_entropy_interaction | IC × Entropy interaction surface. σ(0.40 * f01 * f02 + 0.30 * coupling_entropy_1s). Captures saddle-shaped preference: high entropy shifts optimal IC downward. Gold 2019: partial η² = 0.07 (p = 0.06, marginal); confirmed in Cheung 2019 (p < 0.05) and Gold 2023b. |
| 3 | f04_optimal_complexity | Preferred complexity level. σ(0.50 * f03 + 0.25 * pleasantness_std_1s). Integrates interaction surface with hedonic variability to estimate listener's current optimal complexity zone. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 21 | 4 | M0 (value) | L2 (bidi) | IC at 125ms theta timescale |
| 1 | 21 | 8 | M20 (entropy) | L2 (bidi) | IC entropy at 500ms |
| 2 | 21 | 16 | M1 (mean) | L2 (bidi) | Mean IC over 1s — primary IC input for inverted-U |
| 3 | 24 | 4 | M0 (value) | L2 (bidi) | Concentration at 125ms |
| 4 | 24 | 8 | M2 (std) | L2 (bidi) | Concentration std at 500ms |
| 5 | 24 | 16 | M20 (entropy) | L2 (bidi) | Concentration entropy 1s — primary entropy input |
| 6 | 0 | 8 | M1 (mean) | L2 (bidi) | Mean roughness 500ms — harmonic complexity |
| 7 | 0 | 16 | M2 (std) | L2 (bidi) | Roughness variability 1s |
| 8 | 8 | 16 | M1 (mean) | L2 (bidi) | Mean loudness 1s — perceptual weighting |
| 9 | 4 | 16 | M1 (mean) | L2 (bidi) | Mean pleasantness 1s — hedonic baseline |
| 10 | 4 | 16 | M2 (std) | L2 (bidi) | Pleasantness variability 1s — hedonic fluctuation |
| 11 | 33 | 8 | M1 (mean) | L2 (bidi) | IC-perceptual coupling 500ms |
| 12 | 33 | 16 | M2 (std) | L2 (bidi) | Coupling variability 1s |
| 13 | 33 | 16 | M20 (entropy) | L2 (bidi) | Coupling entropy 1s — interaction uncertainty |

---

## Computation

The E-layer implements the Berlyne (1971) inverted-U complexity-preference function using Gold 2019's empirical parametrization. Two independent inverted-U curves are computed for IC and entropy, then combined via an interaction term.

1. **IC Liking Curve (f01)**: Uses the quadratic transform 4*x*(1-x) on mean IC over 1s, which peaks at 0.5 (medium complexity). The sigmoid-weighted combination with mean pleasantness provides hedonic context. Gold 2019 showed consistent negative quadratics across two independent samples.

2. **Entropy Liking Curve (f02)**: Same quadratic transform on concentration entropy. Medium uncertainty maximizes liking independently of IC. The entropy_quadratic captures the concave-down preference shape.

3. **IC × Entropy Interaction (f03)**: Product of f01 and f02, modulated by coupling entropy. Implements the saddle surface from Cheung 2019: high uncertainty shifts optimal IC downward (prefer predictable outcomes in uncertain contexts). Amygdala + hippocampus + STG reflect this interaction neurally.

4. **Optimal Complexity (f04)**: Integrates interaction surface with pleasantness variability. Pleasantness std provides a hedonic fluctuation signal indicating how dynamically the optimal zone is shifting. Feeds P-layer for real-time preference tracking.

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [0] | roughness | Harmonic complexity / dissonance level |
| R³ [4] | sensory_pleasantness | Hedonic signal for pleasantness baseline |
| R³ [8] | loudness | Structural salience / perceptual weight |
| R³ [21] | spectral_change | Information content (surprise level) |
| R³ [24] | concentration_change | Spectral uncertainty / timbral complexity |
| R³ [33:41] | x_l4l5 | IC × Entropy surface / preference computation |
| H³ | 14 tuples (see above) | Multi-scale temporal dynamics for complexity assessment |
| Gold 2019 | IC + entropy inverted-U | Primary behavioral evidence (N = 43 + 27) |
| Gold 2023b | VS + STG fMRI | Neural substrate for preference (N = 24) |
| Cheung 2019 | Saddle surface + amygdala/hippocampus | Interaction and neural evidence (N = 39 + 40) |
