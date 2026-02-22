# PMIM M-Layer — Temporal Integration (2D)

**Layer**: Mathematical / Temporal Integration (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: sigmoid / clamp

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:hierarchical_pe | [0, 1] | Hierarchical prediction error. Precision-weighted combination of ERAN + MMN. hierarchical_pe = clamp(flux * (roughness + inharmonicity)/2 + entropy * (1 - stumpf_fusion), 0, 1). Cheung et al. 2019: uncertainty x surprise interaction predicts musical pleasure; amygdala/hippocampus beta=-0.140 (fMRI N=40, corrected p=0.002). |
| 4 | M1:model_precision | [0, 1] | Prediction model certainty. High precision = confident predictions. model_precision = sigma(stumpf_fusion * sensory_pleasantness * tonalness). Max argument = 1.0. Gold et al. 2019: inverted-U preference for intermediate predictive complexity; quadratic IC and entropy effects (N=70). |

---

## Design Rationale

1. **Hierarchical PE (M0)**: Combines the two prediction error streams into a single precision-weighted metric. The formula reflects hierarchical predictive coding: flux-driven deviance weighted by dissonance (low-level PE from MMN pathway) plus entropy-driven unpredictability weighted by lack of fusion (high-level PE from ERAN pathway). This implements the Bayesian brain principle where PE magnitude depends on both surprise AND precision of the violated prediction.

2. **Model Precision (M1)**: Quantifies how confident the current predictive model is. High stumpf fusion (tonal coherence), sensory pleasantness (consonance), and tonalness (harmonic-to-noise ratio) all indicate a well-formed prediction that should produce large PE when violated. This implements the precision term in predictive coding — the inverse uncertainty that weights PE in downstream processing.

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (22, 14, 1, 0) | entropy mean H14 L0 | Average complexity over progression (700ms) |
| (22, 18, 13, 0) | entropy entropy H18 L0 | Higher-order unpredictability over phrase (2s) |
| (3, 10, 0, 2) | stumpf_fusion value H10 L2 | Fusion state at chord level for precision |
| (3, 14, 14, 0) | stumpf_fusion periodicity H14 L0 | Cadential regularity proxy over progression |
| (4, 10, 0, 2) | sensory_pleasantness value H10 L2 | Current consonance for precision |
| (14, 10, 0, 2) | tonalness value H10 L2 | Harmonic purity for precision |
| (14, 14, 18, 0) | tonalness trend H14 L0 | Tonal trend over progression |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | M0: sensory dissonance for PE weighting |
| [3] | stumpf_fusion | M0+M1: tonal coherence (integration/precision) |
| [4] | sensory_pleasantness | M1: consonance for model precision |
| [5] | inharmonicity | M0: harmonic template deviation |
| [14] | tonalness | M1: harmonic-to-noise ratio for precision |
| [21] | spectral_flux | M0: change magnitude for hierarchical PE |
| [22] | entropy | M0: unpredictability for hierarchical PE |

---

## Scientific Foundation

- **Cheung et al. 2019**: fMRI N=40, uncertainty x surprise jointly predict musical pleasure; amygdala/hippocampus beta=-0.140 (corrected p=0.002); IDyOM model quantified 80,000 chord predictions
- **Gold et al. 2019**: Behavioral N=70, inverted-U preference for intermediate predictive complexity; quadratic IC and entropy effects on liking
- **Friston 2005**: Theoretical framework, precision-weighted prediction error in hierarchical generative models
- **Koelsch 2014**: Review, hierarchical predictive coding for music syntax processing in IFG

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/pmim/temporal_integration.py`
