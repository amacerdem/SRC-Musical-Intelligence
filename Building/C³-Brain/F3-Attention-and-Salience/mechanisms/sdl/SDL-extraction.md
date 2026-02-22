# SDL E-Layer — Extraction (3D)

**Layer**: Extraction (E)
**Indices**: [0:3]
**Scope**: internal
**Activation**: mixed (tanh for lateralization, sigmoid for clustering/oscillation)
**Model**: ASU-gamma3, Salience-Dependent Lateralization (9D, gamma-tier 50-70%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:dynamic_lateral | [-1, 1] | Dynamic lateralization index. f25 = tanh(0.35*centroid_value - 0.30*flux_value). Spectral features drive rightward (+) lateralization; temporal features drive leftward (-). Zatorre 2022: AST model — spectral processing right-lateralized, temporal processing left-lateralized. |
| 1 | E1:local_clustering | [0, 1] | Degradation compensation clustering. f26 = sigma(0.35*loudness_entropy_1s + 0.35*ts_entropy_100ms). When signal quality degrades, both hemispheres recruit local networks. Albouy 2020: double dissociation — spectral/temporal degradation drives bilateral compensation. |
| 2 | E2:hemispheric_osc | [0, 1] | Task-dependent hemispheric oscillation. f27 = sigma(0.35*conn_velocity_1250ms + 0.30*ts_periodicity_1s). Connectivity velocity at 1250ms captures slow hemispheric shifts; periodicity captures sustained lateralized processing. Jin 2024: eta2p=0.526 for task-dependent lateralization. |

---

## Design Rationale

1. **Dynamic Lateral (E0)**: The core lateralization signal — uses tanh activation for signed output [-1, 1] where positive = right hemisphere (spectral processing) and negative = left hemisphere (temporal processing). The subtraction centroid - flux captures the Zatorre AST principle: spectral centroid indexes spectral complexity (rightward), spectral flux indexes temporal change (leftward).

2. **Local Clustering (E1)**: When processing is challenged (high entropy = degraded signal), both hemispheres increase local clustering to compensate. Uses loudness entropy at 1s (macro degradation) and cross-stream entropy at 100ms (micro degradation). Based on Albouy 2020 double dissociation showing bilateral recruitment under degradation.

3. **Hemispheric Oscillation (E2)**: Task demands shift lateralization over time. Connectivity velocity at 1250ms captures slow network reconfigurations; periodicity at 1s captures sustained oscillatory lateralization patterns. Jin 2024 showed large effect sizes (eta2p=0.526) for task-dependent lateralization shifts.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (15, 3, 0, 2) | spectral_centroid value H3 L2 | Centroid at 100ms — spectral complexity (rightward) |
| (10, 3, 0, 2) | spectral_flux value H3 L2 | Flux at 100ms — temporal change (leftward) |
| (8, 16, 20, 2) | loudness entropy H16 L2 | Loudness entropy at 1s — macro degradation |
| (37, 3, 20, 2) | x_l4l5 entropy H3 L2 | Cross-stream entropy at 100ms — micro degradation |
| (25, 17, 8, 0) | x_l0l5 velocity H17 L0 | Connectivity velocity at 1250ms — slow hemispheric shift |
| (37, 16, 17, 2) | x_l4l5 periodicity H16 L2 | Cross-stream periodicity at 1s — sustained lateralization |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [8] | loudness | E1: perceptual loudness entropy for degradation |
| [10] | spectral_flux | E0: temporal change rate (leftward driver) |
| [15] | spectral_centroid | E0: spectral complexity (rightward driver) |
| [25:33] | x_l0l5 | E2: motor-auditory connectivity velocity |
| [37:45] | x_l4l5 | E1+E2: cross-stream entropy and periodicity |

---

## Scientific Foundation

- **Zatorre 2022**: Auditory Scene Typicality (AST) model — spectral right, temporal left lateralization
- **Albouy 2020**: Double dissociation — spectral degradation increases right activation, temporal degradation increases left (fMRI, N=40)
- **Jin 2024**: Task-dependent lateralization with large effect size (eta2p=0.526, EEG, N=32)
- **Haiduk 2024**: chi2=41.4 for salience-dependent lateralization shifts

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/sdl/extraction.py` (pending)
