# PUPF E-Layer — Extraction (2D)

**Layer**: Extraction (E)
**Indices**: [0:2]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:f07_prediction_err | [0, 1] | Surprise magnitude. \|observed - predicted\| / sigma_context. Cheung 2019: striatal RPE (d=3.8-8.53). Amygdala salience detection for unexpected harmonic events. f07 = sigma(S) where S = spectral_flux[21] normalized by context std. |
| 1 | E1:f08_uncertainty | [0, 1] | Entropy of expectation distribution. H = -sum(p(xi) log p(xi)) / log(n). Pearce 2005: IDyOM entropy correlates with expectation rating. f08 = sigma(H) where H derived from distribution_entropy[22] and H3 entropy morphs. |

---

## Design Rationale

1. **Prediction Error (E0)**: The primary PUPF extraction feature. Measures surprise magnitude as the normalized deviation between observed and predicted spectral events. Uses spectral_flux[21] as the frame-level surprise proxy, contextualized by H3 velocity morphs for dynamic scaling. Cheung 2019 fMRI showed striatal response to musical surprise with very large effect sizes (d=3.8-8.53), confirming this signal drives the mesolimbic reward pathway. This feeds SRP's RPE signal directly.

2. **Uncertainty (E1)**: Tracks the entropy of the listener's expectation distribution — how uncertain the brain is about what comes next. Uses distribution_entropy[22] as the spectral proxy for Shannon entropy, enriched by H3 entropy morphs at the 1s integration window. Pearce 2005 IDyOM framework validates that entropy of the internal model correlates with subjective expectation. This is the "H" axis of PUPF's Goldilocks function.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (21, 16, 20, 0) | spectral_flux entropy H16 L0 | 1s entropy of spectral change for H computation |
| (22, 16, 20, 0) | distribution_entropy entropy H16 L0 | 1s Shannon entropy integration |
| (21, 7, 8, 0) | spectral_flux velocity H7 L0 | Instantaneous surprise rate |
| (22, 7, 8, 0) | distribution_entropy velocity H7 L0 | Uncertainty change rate |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [21] | spectral_flux | E0: frame-to-frame surprise signal (S computation) |
| [22] | distribution_entropy | E1: Shannon entropy proxy (H computation) |
| [23] | distribution_flatness | E1: noise-level uncertainty context |
| [24] | distribution_concentration | E1: spectral focus for predictability |

---

## Scientific Foundation

- **Cheung et al. 2019**: Striatal response to musical surprise (fMRI 3T, N=39, d=3.8-8.53); H x S interaction drives amygdala, hippocampus, auditory cortex (d=3.8-4.16)
- **Pearce 2005**: IDyOM entropy correlates with expectation rating (computational model, melodic sequences)
- **Egermann et al. 2013**: High information content increases arousal, decreases valence (live concert + physiology, N=50, d=6.0)
- **Gold et al. 2019**: IC x entropy quadratic effects; intermediate complexity preferred (behavioral, N=43+27)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/pupf/extraction.py`
