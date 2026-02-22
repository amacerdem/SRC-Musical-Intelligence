# TPRD T-Layer — Extraction (3D)

**Layer**: Tonotopic (T)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | T0:tonotopic | [0, 1] | Tonotopic encoding strength (primary/medial HG). sigma(0.35*roughness_h10*(1-tonalness) + 0.35*entropy_h6*amplitude). High roughness + low tonalness = spectral (not pitch) encoding. Briley 2013: primary HG tuned to spectral content. |
| 1 | T1:pitch | [0, 1] | Pitch representation strength (nonprimary/lateral HG). sigma(0.40*tonalness_mean*autocorr_period + 0.30*tonalness_h0*autocorr). High pitch salience + periodicity = F0 extraction. Briley 2013: anterolateral HG extracts pitch chroma. |
| 2 | T2:dissociation | [0, 1] | Representation dissociation degree. sigma(0.30*|T0-T1| + 0.25*inharm_h10 + 0.25*entropy). Divergence between tonotopic and pitch streams. Basinski 2025: inharmonicity -> P3a attentional capture. |

---

## Design Rationale

Three features modeling the medial-lateral dissociation in Heschl's gyrus (Briley et al. 2013):

1. **Tonotopic (T0)**: Roughness at chord level (H10) gated by (1-tonalness) captures spectral processing in primary/medial HG. When tonalness is high (clear pitch), tonotopic encoding diminishes. Entropy*amplitude adds spectral complexity weighted by energy.

2. **Pitch (T1)**: Tonalness mean at brainstem level (H3) times harmonic periodicity captures F0 extraction in nonprimary/lateral HG. Instant tonalness*autocorrelation provides fine temporal resolution. The 0.40/0.30 weighting prioritizes temporal context over instantaneous features.

3. **Dissociation (T2)**: Absolute difference between T0 and T1 captures the degree of stream separation. Inharmonicity (Basinski 2025: P3a p=0.010) and spectral entropy add independent dissociation signals. When tonotopic and pitch streams agree, T2 is low; when they diverge, T2 is high.

---

## H3 Dependencies (T-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 10, 0, 2) | roughness value H10 L2 | Tonotopic beating at chord level |
| (14, 0, 0, 2) | tonalness value H0 L2 | Immediate pitch salience |
| (14, 3, 1, 2) | tonalness mean H3 L2 | Brainstem pitch salience mean |
| (17, 3, 14, 2) | spectral_auto period H3 L2 | Harmonic periodicity at brainstem |
| (5, 10, 0, 2) | inharmonicity value H10 L2 | Tonotopy-pitch conflict |
| (22, 6, 0, 0) | entropy value H6 L0 | Spectral complexity at beat level |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| 0 | roughness | T0: tonotopic beating proxy |
| 5 | inharmonicity | T2: spectral-pitch misalignment |
| 7 | velocity_A | T0: amplitude/energy weighting |
| 14 | tonalness | T0/T1: pitch clarity |
| 17 | spectral_autocorrelation | T1: harmonic periodicity |
| 22 | entropy | T2: spectral complexity |

---

## Scientific Foundation

- **Briley 2013**: Pure-tone responses in medial HG (tonotopic); IRN pitch chroma in anterolateral HG; F(1,28)=29.865, p<0.001
- **Basinski 2025**: Inharmonicity -> P3a attentional capture (est=-1.37, p=0.0007)
- **Norman-Haignere 2013**: Pitch-sensitive regions respond to resolved harmonics in anterior auditory cortex

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/tprd/extraction.py`
