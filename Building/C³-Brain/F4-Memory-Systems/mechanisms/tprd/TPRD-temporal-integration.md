# TPRD M-Layer — Temporal Integration (2D)

**Model**: Tonotopy-Pitch Representation Dissociation (IMU-β8)
**Unit**: IMU (Integrative Memory Unit)
**Layer**: Temporal Integration (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: arithmetic / sigmoid
**Output Dim (total)**: 10D

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:dissociation_idx | [0, 1] | Normalized dissociation index. Raw: (tonotopic - pitch) / (tonotopic + pitch + eps), where eps=1e-7. Remapped to [0,1]: dissociation_idx = (idx_raw + 1) / 2. Interpretation: 0.0 = pure pitch dominant (nonprimary HG), 0.5 = balanced, 1.0 = pure tonotopic dominant (primary HG). Captures the medial-lateral gradient from Briley 2013: medial HG tonotopic vs anterolateral HG pitch. |
| 4 | M1:spectral_pitch_r | [0, 1] | Spectral-to-pitch ratio. Coherence between perceptual and syntactic representations of pitch. Measures how well the physical spectral content aligns with the perceived pitch representation. Bidelman 2013: brainstem FFR-consonance r>=0.81, showing subcortical spectral-pitch correspondence. |

---

## Design Rationale

1. **Dissociation Index (M0)**: Provides a continuous measure of where along the medial-lateral gradient the current stimulus falls. The index is computed as the contrast ratio between tonotopic (f31) and pitch (f32) encoding strengths, remapped from [-1, 1] to [0, 1]. A value of 0.5 indicates balanced representation (both tonotopic and pitch systems equally active), while extreme values indicate dominance of one system. This operationalizes the core finding of Briley 2013: a smooth gradient from tonotopy (medial) to pitch (lateral/anterolateral) within Heschl's gyrus.

2. **Spectral-Pitch Ratio (M1)**: Quantifies the coherence between the spectral (physical) and pitch (perceptual) representations. When spectral content and perceived pitch are well-aligned (e.g., harmonic complex tones), the ratio is high. When they diverge (e.g., inharmonic tones, missing fundamental), the ratio drops. This is supported by Bidelman 2013 showing that subcortical pitch salience predicts perceptual consonance ratings (r>=0.81).

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 14, 1, 0) | roughness mean H14 L0 | Average tonotopic load over progression (700ms) |
| (5, 14, 1, 0) | inharmonicity mean H14 L0 | Average tonotopy-pitch conflict over progression |
| (3, 6, 1, 0) | stumpf_fusion mean H6 L0 | Beat-level fusion stability (200ms) |
| (14, 6, 1, 0) | tonalness mean H6 L0 | Beat-level pitch clarity (200ms) |
| (17, 6, 14, 0) | spectral_autocorrelation periodicity H6 L0 | Beat-level harmonic periodicity |
| (22, 14, 1, 0) | entropy mean H14 L0 | Average spectral complexity over progression |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | M0: tonotopic component for dissociation index |
| [5] | inharmonicity | M0: spectral-pitch conflict component |
| [14] | tonalness | M0+M1: pitch clarity for both dissociation and ratio |
| [17] | spectral_autocorrelation | M1: harmonic periodicity for spectral-pitch coherence |
| [22] | entropy | M0: spectral complexity modulates dissociation |

---

## Brain Regions

| Region | Coordinates (Talairach) | Evidence | Function |
|--------|-------------------------|----------|----------|
| Heschl's Gyrus (medial) | L: -41.9, -18.8, 15.8 / R: 44.2, -13.4, 13.4 | Direct (EEG, Briley 2013 N=8) | Tonotopic encoding for dissociation numerator |
| Anterolateral HG | L: -49.1, -21.2, 17.2 / R: 42.9, -5.5, 17.6 | Direct (EEG, Briley 2013 N=8) | Pitch encoding for dissociation denominator |
| Lateral HG | ~+/-52, -14, 4 | Direct (fMRI, Patterson 2002 N=6) | Temporal pitch processing, F0 extraction |

---

## Scientific Foundation

- **Briley et al. (2013)**: Medial-lateral gradient in HG: pure-tone on medial, pitch chroma on anterolateral (EEG, N=8-15); pitch chroma F(1,28)=29.865, p<0.001
- **Bidelman (2013)**: Brainstem FFR encodes consonance hierarchy; subcortical pitch salience predicts perceptual consonance (r>=0.81, review)
- **Tabas et al. (2019)**: POR latency up to 36ms longer for dissonant dyads; consonance processing in alHG (MEG, N=37)
- **Patterson et al. (2002)**: Lateral HG responds to temporal pitch cues (fMRI, N=6)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/tprd/temporal_integration.py`
