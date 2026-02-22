# MAA E-Layer — Extraction (4D)

**Layer**: Extraction (E)
**Indices**: [0:4]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:f01_complexity_tolerance | [0, 1] | Ability to process atonal complexity. Entropy-based tolerance index. f01 = sigma(0.35 * consonance_entropy_1s + 0.35 * coupling_entropy_1s). Cheung 2019: uncertainty x surprise interaction predicts pleasure (R2_marginal=0.476); Gold 2019: inverted-U preference for intermediate predictive complexity (quadratic IC+entropy p<0.05). |
| 1 | E1:f02_familiarity_index | [0, 1] | Mere exposure / familiarity accumulation. f02 = sigma(0.40 * coupling_trend_1s + 0.30 * periodicity_mean_1s). Gold 2019: inverted-U persists across repetitions; Mencke 2019: exposure as third factor in appreciation (d=3.0 key clarity tonal vs atonal). |
| 2 | E2:f03_framing_effect | [0, 1] | Cognitive framing benefit from aesthetic context. f03 = sigma(0.40 * tonalness_mean_1s + 0.30 * change_mean_500ms). Huang 2016: artistic music activates mPFC secondary reward (p<0.05 FWE); Sarasso 2021: aesthetic attitude reorients attention to learning. |
| 3 | E3:f04_appreciation_composite | [0, 1] | Overall multifactorial appreciation index. f04 = sigma(0.35 * f01 * f02 + 0.35 * f03). Mencke 2019: Appreciation = f(Complexity x Tolerance x Framing x Exposure); Cheung 2019: saddle-shaped pleasure surface (R2=0.476). |

---

## Design Rationale

1. **Complexity Tolerance (E0)**: The core MAA extraction feature. Measures the listener's capacity to process atonal complexity without aversion. Uses consonance entropy at 1s and coupling entropy at 1s as dual indicators of harmonic unpredictability. High entropy in both domains indicates atonal contexts where appreciation depends on openness/tolerance. Primary basis: Cheung 2019 demonstrating that the uncertainty x surprise interaction predicts pleasure, and Gold 2019 showing inverted-U preference for intermediate complexity.

2. **Familiarity Index (E1)**: Tracks the mere exposure effect where repeated listening increases liking for complex music. Uses coupling trend at 1s (tracking whether the listener is building familiarity with the harmonic coupling patterns) and periodicity mean at 1s (detecting recurring structural patterns). Mencke 2019 identifies exposure as the third factor in the multifactorial appreciation model.

3. **Framing Effect (E2)**: Measures the cognitive framing benefit from aesthetic context. When listeners approach atonal music with an aesthetic attitude (as art rather than noise), appreciation increases. Uses tonalness mean at 1s (tonal context quality) and spectral change mean at 500ms (structural complexity requiring interpretation). Supported by Huang 2016 showing mPFC activation for artistic vs popular music and Sarasso 2021 theory of aesthetic reorientation.

4. **Appreciation Composite (E3)**: The multiplicative integration of the three factors. The interaction term (f01 * f02) captures the finding that complexity tolerance and familiarity must co-occur for appreciation to emerge. Framing contributes additively. This maps to the saddle-shaped pleasure surface from Cheung 2019 where low uncertainty + high surprise = maximal pleasure.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 16, 20, 0) | sensory_pleasantness entropy H16 L0 | Consonance entropy over 1s |
| (41, 16, 20, 0) | x_l5l7[0] entropy H16 L0 | Coupling entropy over 1s |
| (41, 16, 18, 0) | x_l5l7[0] trend H16 L0 | Coupling trend over 1s |
| (5, 16, 1, 0) | periodicity mean H16 L0 | Mean periodicity over 1s |
| (14, 16, 1, 0) | tonalness mean H16 L0 | Mean tonalness over 1s |
| (21, 8, 1, 0) | spectral_change mean H8 L0 | Mean spectral change over 500ms |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | Dissonance level (atonality indicator) |
| [4] | sensory_pleasantness | Consonance proxy (inverse of atonality) |
| [5] | periodicity | Tonal certainty / key clarity component |
| [14] | tonalness | Key clarity proxy / atonality index |
| [21] | spectral_change | Structural complexity for pattern detection |
| [41:49] | x_l5l7 (8D) | Complexity tolerance / appreciation pathway |

---

## Scientific Foundation

- **Mencke et al. 2019**: Key clarity tonal M=0.8 vs atonal M=0.5, d=3.0; pulse clarity d=2.0; openness, framing, exposure interact for appreciation (MIR corpus, N=100 excerpts)
- **Gold et al. 2019**: Inverted-U preference for intermediate predictive complexity; quadratic IC and entropy on liking (behavioral + IDyOM, N=43+27, p<0.05)
- **Cheung et al. 2019**: Uncertainty x surprise interaction predicts pleasure; amygdala/hippocampus beta=-0.14, AC beta=-0.18 (fMRI, N=39+40, R2_marginal=0.476)
- **Huang et al. 2016**: Artistic music activates mPFC (secondary reward) + ToM areas; popular music activates putamen (fMRI, N=18, p<0.05 FWE)
- **Sarasso et al. 2021**: Aesthetic emotions help tolerate predictive uncertainty; aesthetic attitude reorients attention to learning (theoretical)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/maa/extraction.py`
