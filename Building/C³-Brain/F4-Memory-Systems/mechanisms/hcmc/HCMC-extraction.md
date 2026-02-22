# HCMC E-Layer — Extraction (3D)

**Layer**: Extraction (E)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:fast_binding | [0, 1] | Hippocampal initial encoding. CA3 autoassociative binding of features. f19 = sigma(0.35 * x_l0l5.mean * stumpf_mean_1s + 0.35 * stumpf * stumpf_mean_1s + 0.30 * onset_str * loudness). Rolls 2013: CA3 autoassociative network for fast pattern binding. |
| 1 | E1:episodic_seg | [0, 1] | Event boundary detection. Hippocampal segmentation at spectral flux boundaries. f20 = sigma(0.40 * flux * flux_mean_1s + 0.30 * entropy * flux + 0.30 * onset_str * flux). Zacks et al. 2007: event boundaries trigger encoding. |
| 2 | E2:cortical_storage | [0, 1] | Long-term cortical pattern storage. mPFC + PCC consolidation via hippocampal replay. f21 = sigma(0.35 * x_l5l7.mean * harmonicity_mean_5s + 0.35 * harmonicity * tonalness_autocorr_5s + 0.30 * (1-entropy) * tonalness). Liu et al. 2024: hippocampal replay drives mPFC consolidation. |

---

## Design Rationale

1. **Fast Binding (E0)**: Tracks how strongly the hippocampus binds incoming auditory features into an episodic trace. Uses cross-domain interactions (x_l0l5 = Energy x Consonance) multiplied by tonal fusion (stumpf) at the 1s binding window. Primary basis: Rolls 2013 CA3 autoassociative binding, Cheung et al. 2019 hippocampal uncertainty encoding.

2. **Episodic Segmentation (E1)**: Detects event boundaries where musical structure changes, triggering new episodic segments in hippocampal memory. Spectral flux is the primary boundary trigger; entropy and onset strength provide confirmatory signals. Based on Zacks et al. 2007 event segmentation theory.

3. **Cortical Storage (E2)**: Measures the strength of long-term cortical consolidation from hippocampal traces into mPFC/PCC networks. Uses consonance-timbre interactions (x_l5l7) and harmonic stability as templates for durable cortical storage. Supported by Liu et al. 2024 replay-triggered hippocampal-cortical transfer.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 16, 1, 2) | stumpf_fusion mean H16 L2 | Binding coherence at 1s |
| (3, 16, 3, 2) | stumpf_fusion std H16 L2 | Binding variability at 1s |
| (21, 16, 1, 2) | spectral_flux mean H16 L2 | Current segmentation rate |
| (21, 16, 3, 2) | spectral_flux std H16 L2 | Flux variability at 1s |
| (11, 16, 1, 2) | onset_strength mean H16 L2 | Event density at 1s |
| (10, 16, 1, 2) | loudness mean H16 L2 | Encoding salience at 1s |
| (7, 16, 1, 2) | amplitude mean H16 L2 | Energy level at 1s |
| (5, 16, 1, 2) | harmonicity mean H16 L2 | Harmonic template at 1s |
| (5, 20, 1, 0) | harmonicity mean H20 L0 | Harmonic stability over 5s |
| (14, 16, 1, 2) | tonalness mean H16 L2 | Melodic content at 1s |
| (14, 20, 22, 0) | tonalness autocorrelation H20 L0 | Tonal repetition over 5s |
| (22, 16, 1, 2) | entropy mean H16 L2 | Current pattern complexity |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [3] | stumpf_fusion | E0: binding coherence proxy |
| [5] | harmonicity | E2: harmonic template match |
| [7] | amplitude | E0: encoding salience |
| [10] | loudness | E0: arousal correlate |
| [11] | onset_strength | E0+E1: event boundary marker |
| [14] | tonalness | E2: melodic encoding quality |
| [21] | spectral_flux | E1: segmentation trigger |
| [22] | entropy | E1+E2: encoding difficulty |
| [25:33] | x_l0l5 | E0: fast hippocampal binding |
| [41:49] | x_l5l7 | E2: cortical long-term template |

---

## Scientific Foundation

- **Rolls 2013**: CA3 autoassociative network for fast pattern binding (computational)
- **Zacks et al. 2007**: Event segmentation theory -- boundaries trigger hippocampal encoding (behavioral + fMRI)
- **Cheung et al. 2019**: Hippocampal encoding of musical expectation uncertainty (fMRI, N=79, beta=-0.140, p=0.002)
- **Liu et al. 2024**: Replay-triggered hippocampal-cortical transfer (EEG-fMRI, N=33)
- **Borderie et al. 2024**: Theta-gamma PAC for hippocampal auditory binding (SEEG, intracranial)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/hcmc/extraction.py`
