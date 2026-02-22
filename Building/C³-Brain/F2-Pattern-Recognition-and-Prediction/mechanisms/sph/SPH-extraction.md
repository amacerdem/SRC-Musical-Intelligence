# SPH E-Layer — Extraction (4D)

**Model**: SPH (Spatiotemporal Prediction Hierarchy)
**Layer**: E (Extraction)
**Dimensions**: 4D [0:4]
**Scope**: internal

---

## Dimensions

| Index | Name | Formula | Range |
|-------|------|---------|-------|
| 0 | E0:gamma_match | σ(0.35×consonance_100ms + 0.30×spectral_auto_100ms + 0.20×consonance_mean_1s + 0.15×chroma_100ms) | [0,1] |
| 1 | E1:alpha_beta_error | σ(0.35×spectral_flux_100ms + 0.25×onset_25ms + 0.20×spectral_flux_std_100ms + 0.20×onset_period_100ms) | [0,1] |
| 2 | E2:hierarchy_position | σ(0.50×tonal_stab_100ms + 0.50×tonal_stab_mean_1s) | [0,1] |
| 3 | E3:feedforward_feedback | σ(0.50×spectral_auto_mean_1s − 0.50×tonal_stab_entropy_1s) | [0,1] |

## H³ Demands Consumed (12)

| Key | Feature | Purpose |
|-----|---------|---------|
| (4,3,0,2) | sensory_pleasantness 100ms value bidi | Consonance at 100ms |
| (4,16,1,0) | sensory_pleasantness 1s mean memory | Long-range consonance |
| (11,0,0,2) | onset_strength 25ms value bidi | Instant onset detection |
| (11,3,14,2) | onset_strength 100ms periodicity bidi | Rhythmic regularity |
| (17,3,0,2) | spectral_autocorrelation 100ms value bidi | Feedforward coupling |
| (17,16,1,0) | spectral_autocorrelation 1s mean memory | Sustained feedforward |
| (21,3,0,2) | spectral_flux 100ms value bidi | Spectral deviation |
| (21,3,2,2) | spectral_flux 100ms std bidi | Deviation variability |
| (25,3,0,2) | chroma_C 100ms value bidi | Tonal identity |
| (60,3,0,2) | tonal_stability 100ms value bidi | Hierarchy position |
| (60,16,1,0) | tonal_stability 1s mean memory | Long-range hierarchy |
| (60,16,13,0) | tonal_stability 1s entropy memory | Structural uncertainty |

## Scientific Basis

- **Bonetti 2024**: gamma > alpha-beta for memorised sequences; alpha-beta > gamma for varied. Feedforward Heschl→Hippocampus→Cingulate.
- **Golesorkhi 2021**: core-periphery hierarchy η²=0.86.
- **de Vries & Wurm 2023**: hierarchical prediction timing.

## Implementation

File: `Musical_Intelligence/brain/functions/f2/mechanisms/sph/extraction.py`
