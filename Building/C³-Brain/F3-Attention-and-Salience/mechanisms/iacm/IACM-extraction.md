# IACM E-Layer — Extraction (3D)

**Layer**: Extraction (E)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:inharmonic_capture | [0, 1] | Inharmonic event detection. f04 = sigma(0.40*approx_entropy + 0.25*roughness_entropy). Inharmonic events produce larger P3a (Basinski 2025, d=-1.37). |
| 1 | E1:object_segregation | [0, 1] | Auditory scene complexity. f05 = sigma(0.35*scene_coupling_100ms + 0.25*periodicity_std). ORN-indexed auditory scene complexity (OR=16.44). |
| 2 | E2:precision_weighting | [0, 1] | Context-dependent prediction error weighting. f06 = sigma(0.40*periodicity_value + 0.30*tonalness_period_1s + 0.30*coupling_phase_resets). Context-dependent PE. Friston 2005: precision weighting in predictive coding. |

---

## Design Rationale

1. **Inharmonic Capture (E0)**: Detects inharmonic spectral events that capture involuntary attention. Uses approximate entropy (spectral unpredictability) and roughness entropy. Primary basis: Basinski 2025 showing P3a amplitude is significantly larger for inharmonic sounds (d=-1.37, N=35).

2. **Object Segregation (E1)**: Tracks auditory scene complexity via the Object-Related Negativity (ORN). Uses motor-auditory coupling at 100ms (scene-level binding) and periodicity variability. High values indicate the auditory system is segregating multiple concurrent sound objects.

3. **Precision Weighting (E2)**: Evaluates contextual stability to weight prediction errors appropriately. Combines tonalness periodicity at 1s (tonal stability), raw periodicity (regularity), and coupling phase resets (context disruption). Grounded in Friston's precision-weighted predictive coding framework.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (14, 0, 0, 2) | tonalness value H0 L2 | Instantaneous tonal quality 25ms |
| (14, 1, 1, 2) | tonalness mean H1 L2 | Mean tonalness 50ms |
| (14, 3, 0, 2) | tonalness value H3 L2 | Tonal quality at 100ms |
| (14, 4, 14, 2) | tonalness periodicity H4 L2 | Tonalness periodicity at 125ms |
| (14, 16, 14, 2) | tonalness periodicity H16 L2 | Tonalness periodicity at 1s |
| (16, 0, 0, 2) | spectral_flatness value H0 L2 | Instantaneous spectral flatness 25ms |
| (16, 3, 20, 2) | spectral_flatness entropy H3 L2 | Flatness entropy 100ms |
| (0, 3, 0, 2) | roughness value H3 L2 | Roughness level at 100ms |
| (0, 3, 20, 2) | roughness entropy H3 L2 | Roughness entropy 100ms |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | E0: roughness entropy for inharmonic detection |
| [5] | periodicity | E1: regularity for object segregation |
| [7] | amplitude | E1: energy for scene coupling |
| [14] | tonalness | E0+E2: tonal context for precision weighting |
| [16] | spectral_flatness | E0: spectral unpredictability |
| [25:33] | x_l0l5 | E1+E2: motor-auditory coupling |

---

## Scientific Foundation

- **Basinski 2025**: Inharmonic events produce larger P3a (d=-1.37, EEG, N=35)
- **Basinski 2025**: ORN object-related negativity (OR=16.44 for inharmonic sounds)
- **Friston 2005**: Precision-weighted prediction errors in predictive coding
- **Alain 2007**: ORN and auditory scene segregation mechanisms

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/iacm/extraction.py`
