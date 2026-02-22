# TPRD P-Layer — Cognitive Present (2D)

**Model**: Tonotopy-Pitch Representation Dissociation (IMU-β8)
**Unit**: IMU (Integrative Memory Unit)
**Layer**: Cognitive Present (P)
**Indices**: [5:7]
**Scope**: internal
**Activation**: clamp [0, 1]
**Output Dim (total)**: 10D

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:tonotopic_state | [0, 1] | Current tonotopic activation state. tonotopic_state = (harmony.mean() * roughness), clamped to [0,1]. Represents the instantaneous level of tonotopic (frequency-map) processing in primary HG. Modulated by the harmonic context from the mnemonic circuit. Fishman 2001: A1/HG phase-locked activity correlates with dissonance. |
| 6 | P1:pitch_state | [0, 1] | Current pitch representation state. pitch_state = (pitch_sal.mean() * tonalness), clamped to [0,1]. Represents the instantaneous strength of pitch (F0) representation in nonprimary HG. Briley 2013: anterolateral HG encodes pitch chroma independent of resolvability. Norman-Haignere 2013: pitch regions driven by resolved harmonics. |

---

## Design Rationale

1. **Tonotopic State (P0)**: Provides a real-time readout of how strongly the tonotopic (spectral frequency) system is engaged. The product of harmonic context (from the mnemonic circuit harmony signal) and roughness captures the co-occurrence of spectral complexity and beating in the current frame. High roughness during rich harmonic contexts indicates heavy tonotopic map activation. This reflects the finding that A1/HG shows phase-locked oscillatory activity correlating with perceived dissonance (Fishman 2001).

2. **Pitch State (P1)**: Provides a real-time readout of pitch representation strength. The product of pitch salience (from the perceptual circuit) and tonalness (from R3) captures how clearly the fundamental frequency is being extracted. When both are high, the nonprimary HG is strongly engaged in pitch processing. This reflects the anterolateral HG pitch chroma encoding demonstrated by Briley 2013 and the resolved-harmonic preference shown by Norman-Haignere 2013.

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 10, 0, 2) | roughness value H10 L2 | Current tonotopic beating for tonotopic_state |
| (14, 0, 0, 2) | tonalness value H0 L2 | Immediate pitch salience for pitch_state |
| (14, 3, 1, 2) | tonalness mean H3 L2 | Brainstem pitch salience context |
| (3, 0, 0, 2) | stumpf_fusion value H0 L2 | Immediate fusion quality for pitch context |
| (22, 6, 0, 0) | entropy value H6 L0 | Spectral complexity at beat level |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | P0: tonotopic activation driver |
| [14] | tonalness | P1: pitch clarity for pitch_state |
| [22] | entropy | P0: spectral complexity context |

---

## Brain Regions

| Region | Coordinates (Talairach) | Evidence | Function |
|--------|-------------------------|----------|----------|
| Heschl's Gyrus (medial) | L: -41.9, -18.8, 15.8 / R: 44.2, -13.4, 13.4 | Direct (EEG, Briley 2013 N=8) | Tonotopic state — frequency-selective activation |
| Anterolateral HG | L: -49.1, -21.2, 17.2 / R: 42.9, -5.5, 17.6 | Direct (EEG, Briley 2013 N=8) | Pitch state — F0 extraction activation |
| Planum Temporale | ~+/-54, -28, 12 | Direct (intracranial, Fishman 2001 N=2 human) | Segregation gate — no phase-locked activity, functionally differentiated from HG |

---

## Scientific Foundation

- **Briley et al. (2013)**: Pure-tone responses centered on medial HG; pitch chroma on anterolateral HG (EEG, N=8); dipole difference: L p=0.024, R p=0.047
- **Fishman et al. (2001)**: Phase-locked activity in A1/HG correlates with dissonance; PT shows no phase-locking — functional differentiation (intracranial, 3 macaque + 2 human)
- **Norman-Haignere et al. (2013)**: Pitch-sensitive cortical regions respond primarily to resolved harmonics (fMRI, N=12)
- **Crespo-Bojorque et al. (2018)**: Consonant context changes elicit rapid MMN; dissonant context elicit late MMN only in musicians (EEG/ERP)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/tprd/cognitive_present.py`
