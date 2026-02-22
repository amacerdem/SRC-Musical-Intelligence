# TPRD T-Layer — Tonotopic-Pitch Features (3D)

**Model**: Tonotopy-Pitch Representation Dissociation (IMU-β8)
**Unit**: IMU (Integrative Memory Unit)
**Layer**: Extraction (T)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid
**Output Dim (total)**: 10D

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | T0:f31_tonotopic | [0, 1] | Tonotopic encoding strength (primary HG). f31 = sigma(0.35*roughness*(1-tonalness) + 0.35*entropy*amplitude). High roughness + low tonalness = spectral (not pitch) encoding dominance. Coefficient sum: 0.70. Briley 2013: pure-tone responses centered on medial HG (N=8, EEG). Fishman 2001: phase-locked oscillatory activity in A1/HG correlates with dissonance. |
| 1 | T1:f32_pitch | [0, 1] | Pitch representation strength (nonprimary HG). f32 = sigma(0.40*pitch_sal.mean() + 0.30*tonalness*spectral_autocorr). High pitch salience + high tonalness = strong F0 extraction. Coefficient sum: 0.70. Briley 2013: pitch chroma F(1,28)=29.865, p<0.001 in anterolateral HG. Norman-Haignere 2013: pitch regions respond primarily to resolved harmonics (fMRI, N=12). |
| 2 | T2:f33_dissoc | [0, 1] | Representation dissociation degree. f33 = sigma(0.30*abs(f31-f32) + 0.25*inharmonicity + 0.25*pred_error.mean()). Measures tonotopy-pitch divergence. Coefficient sum: 0.80. Basinski 2025: inharmonicity drives stronger P3a (p=0.010, N=30), supporting dissociation mechanism. |

---

## Design Rationale

1. **Tonotopic Encoding (T0)**: Tracks the strength of frequency-map (cochleotopic) processing in primary Heschl's gyrus. Uses roughness (spectral beating) modulated by inverse tonalness (when pitch clarity is low, processing is spectral rather than pitch-based) plus entropy weighted by amplitude (spectral complexity under energy). This reflects that primary HG encodes physical spectral content, not perceived pitch.

2. **Pitch Representation (T1)**: Tracks F0 extraction strength in nonprimary (anterolateral) HG. Uses pitch salience from the perceptual circuit and tonalness weighted by spectral autocorrelation (harmonic periodicity). When the signal has clear harmonic structure and strong pitch salience, pitch representation dominates. This matches the finding that anterolateral HG responds to pitch chroma independent of harmonic resolvability (Briley 2013).

3. **Representation Dissociation (T2)**: Quantifies the divergence between tonotopic and pitch representations. Uses the absolute difference between T0 and T1, inharmonicity (spectral-pitch misalignment from non-integer partials), and prediction error (harmonic expectation violation). When tonotopic and pitch systems disagree strongly, dissociation is high. Supported by Basinski 2025 showing inharmonicity drives attentional capture (P3a) through representational conflict.

---

## H3 Dependencies (T-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 10, 0, 2) | roughness value H10 L2 | Current tonotopic beating at chord level (400ms) |
| (5, 10, 0, 2) | inharmonicity value H10 L2 | Current tonotopy-pitch conflict at chord level |
| (3, 0, 0, 2) | stumpf_fusion value H0 L2 | Immediate pitch fusion (cochlear, 5.8ms) |
| (3, 3, 1, 2) | stumpf_fusion mean H3 L2 | Brainstem pitch fusion (23.2ms) |
| (14, 0, 0, 2) | tonalness value H0 L2 | Immediate pitch salience (cochlear) |
| (14, 3, 1, 2) | tonalness mean H3 L2 | Brainstem pitch salience (23.2ms) |
| (17, 3, 14, 2) | spectral_autocorrelation periodicity H3 L2 | Harmonic periodicity at brainstem level |
| (10, 10, 0, 2) | loudness value H10 L2 | Attention weight at chord level |
| (6, 10, 0, 2) | harmonic_deviation value H10 L2 | Harmonic template mismatch |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | T0: tonotopic beating proxy |
| [1] | sethares_dissonance | T2: spectral dissonance (tonotopic quality) |
| [3] | stumpf_fusion | T1: pitch fusion quality |
| [4] | sensory_pleasantness | T1+T2: consonance integration |
| [5] | inharmonicity | T2: tonotopy-pitch conflict signal |
| [6] | harmonic_deviation | T2: harmonic template error |
| [7] | amplitude | T0: overall signal energy |
| [10] | loudness | T0: attention weighting |
| [14] | tonalness | T0+T1: pitch clarity / F0 salience |
| [17] | spectral_autocorrelation | T1: harmonic periodicity for pitch extraction |
| [22] | entropy | T0: spectral complexity (tonotopic map load) |

---

## Brain Regions

| Region | Coordinates (Talairach) | Evidence | Function |
|--------|-------------------------|----------|----------|
| Heschl's Gyrus (medial) | L: -41.9, -18.8, 15.8 / R: 44.2, -13.4, 13.4 | Direct (EEG, Briley 2013 N=8) | Tonotopic encoding — primary auditory cortex, frequency-selective responses |
| Anterolateral HG (nonprimary) | L: -49.1, -21.2, 17.2 / R: 42.9, -5.5, 17.6 | Direct (EEG, Briley 2013 N=8) | Pitch chroma representation — IRN pitch independent of resolvability |
| R-STG | Lateral surface (ECoG) | Direct (ECoG, Foo 2016 N=8) | Dissonant-sensitive sites anterior; high-gamma tracks roughness |

---

## Scientific Foundation

- **Briley et al. (2013)**: Pure-tone responses on medial HG; pitch chroma F(1,28)=29.865, p<0.001 in anterolateral HG; dipole location difference L p=0.024, R p=0.047 (EEG, N=8-15)
- **Norman-Haignere et al. (2013)**: Pitch-sensitive regions respond primarily to resolved harmonics in anterior auditory cortex (fMRI, N=12)
- **Fishman et al. (2001)**: Phase-locked activity in A1/HG correlates with dissonance; PT shows no phase-locking (intracranial, N=3 macaque + 2 human)
- **Basinski et al. (2025)**: Inharmonic sounds generate stronger P3a (cluster p=0.010, 190-353ms) and object-related negativity (EEG, N=30)
- **Foo et al. (2016)**: High-gamma in STG tracks roughness; dissonant-sensitive sites anterior in R-STG (ECoG, N=8, p<0.001 FDR)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/tprd/extraction.py`
