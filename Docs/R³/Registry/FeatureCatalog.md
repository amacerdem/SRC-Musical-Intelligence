# R3 Feature Catalog -- Complete 128D Reference

**Version**: 2.0.0
**Source**: R3-V2-DESIGN.md Section 2, R3-CROSSREF.md Section 4
**Updated**: 2026-02-13

---

## Overview

This document provides the definitive catalog of all 128 features in the R3 v2 spectral vector. Each entry includes the feature index, name, group, domain, dimensionality, psychoacoustic basis, quality tier, and status.

### Quality Tier Definitions

| Tier | Label | Definition |
|:----:|-------|-----------|
| P | **Proxy** | Simplified approximation of the target psychoacoustic concept. Does not implement the canonical algorithm. |
| A | **Approximate** | Implements a reasonable approximation of the target concept, with known accuracy limitations (e.g., mel-based chroma vs. CQT chroma). |
| S | **Standard** | Implements a well-established MIR algorithm (e.g., MFCC, spectral contrast, nPVI). |
| R | **Reference** | Implements the canonical psychoacoustic model (e.g., DIN 45692 Zwicker sharpness). |

### Status Definitions

| Status | Meaning |
|--------|---------|
| Existing | Present in R3 v1 (indices [0:49]), formula unchanged |
| New | Added in R3 v2 (indices [49:128]) |
| Revised | Formula planned for revision in Phase 6 |

---

## Complete Feature Catalog

### Group A: Consonance [0:7] -- 7D

| Index | Feature Name | Group | Domain | Dim | Psychoacoustic Basis | Tier | Status |
|:-----:|-------------|:-----:|--------|:---:|---------------------|:----:|--------|
| 0 | roughness | A | Psychoacoustic | 1 | Plomp-Levelt 1965 critical band beating | P | Existing |
| 1 | sethares_dissonance | A | Psychoacoustic | 1 | Sethares 1993 timbre-dependent dissonance | P | Existing |
| 2 | helmholtz_kang | A | Psychoacoustic | 1 | Terhardt 1979 periodicity detection (lag-1 only) | P | Existing |
| 3 | stumpf_fusion | A | Psychoacoustic | 1 | Stumpf tonal fusion (identical to [12] warmth) | P | Existing |
| 4 | sensory_pleasantness | A | Psychoacoustic | 1 | Harrison & Pearce 2020 consonance (arbitrary weights) | P | Existing |
| 5 | inharmonicity | A | Psychoacoustic | 1 | Harmonic series deviation (derived: 1 - [2]) | P | Existing |
| 6 | harmonic_deviation | A | Psychoacoustic | 1 | Spectral irregularity (derived: 0.5*[1] + 0.5*(1-[2])) | P | Existing |

**Phase 6 notes**: Effective independent dimensions ~3. [3] == [12] duplication. [4-6] are derived features. [0] to become real Plomp-Levelt, [1] real Sethares pairwise, [3] real Parncutt subharmonic matching.

---

### Group B: Energy [7:12] -- 5D

| Index | Feature Name | Group | Domain | Dim | Psychoacoustic Basis | Tier | Status |
|:-----:|-------------|:-----:|--------|:---:|---------------------|:----:|--------|
| 7 | amplitude | B | Spectral | 1 | RMS energy (double compression on log-mel) | P | Existing |
| 8 | velocity_A | B | Spectral | 1 | Energy change rate (1st derivative, sigmoid norm) | S | Existing |
| 9 | acceleration_A | B | Spectral | 1 | Energy buildup curvature (2nd derivative, sigmoid norm) | S | Existing |
| 10 | loudness | B | Spectral | 1 | Stevens' power law sone (BUG: double compression) | P | Existing |
| 11 | onset_strength | B | Spectral | 1 | HWR spectral flux (Weineck 2022 neural sync driver) | S | Existing |

**Phase 6 notes**: [10] loudness double-compression bug (Stevens' law applied to log-mel instead of linear power). [7] same issue. Sigmoid normalization on [8],[9] loses physical meaning.

---

### Group C: Timbre [12:21] -- 9D

| Index | Feature Name | Group | Domain | Dim | Psychoacoustic Basis | Tier | Status |
|:-----:|-------------|:-----:|--------|:---:|---------------------|:----:|--------|
| 12 | warmth | C | Spectral | 1 | Low-frequency energy balance (identical to [3]) | P | Existing |
| 13 | sharpness | C | Spectral | 1 | High-frequency energy ratio (not DIN 45692) | P | Existing |
| 14 | tonalness | C | Spectral | 1 | Spectral peak dominance (Terhardt proxy) | P | Existing |
| 15 | clarity | C | Spectral | 1 | Spectral centroid / N (misnomer: not C80) | S | Existing |
| 16 | spectral_smoothness | C | Spectral | 1 | Spectral regularity (complement of [1]: 1 - sethares) | P | Existing |
| 17 | spectral_autocorrelation | C | Spectral | 1 | Lag-1 autocorrelation (identical to [2]) | P | Existing |
| 18 | tristimulus1 | C | Spectral | 1 | Fundamental strength (Pollard-Jansson 1982 mel proxy) | A | Existing |
| 19 | tristimulus2 | C | Spectral | 1 | Mid-harmonic energy (Pollard-Jansson mel proxy) | A | Existing |
| 20 | tristimulus3 | C | Spectral | 1 | High-harmonic energy (Pollard-Jansson mel proxy) | A | Existing |

**Phase 6 notes**: 3 duplications ([12]==[3], [16]==1-[1], [17]==[2]). Effective independent dimensions ~4. [16] to become spectral_spread, [17] to become spectral_kurtosis.

---

### Group D: Change [21:25] -- 4D

| Index | Feature Name | Group | Domain | Dim | Psychoacoustic Basis | Tier | Status |
|:-----:|-------------|:-----:|--------|:---:|---------------------|:----:|--------|
| 21 | spectral_flux | D | Temporal | 1 | L2 frame-to-frame spectral change | S | Existing |
| 22 | distribution_entropy | D | Temporal | 1 | Shannon entropy of spectral distribution | S | Existing |
| 23 | distribution_flatness | D | Temporal | 1 | Wiener entropy / MPEG-7 spectral flatness | S | Existing |
| 24 | distribution_concentration | D | Temporal | 1 | HHI-based concentration (BUG: normalization) | P | Existing |

**Phase 6 notes**: [24] normalization bug -- both uniform and concentrated distributions map to 1.0. Correct formula: `(HHI - 1/N) / (1 - 1/N)`. [22] and [23] are highly correlated (both measure spectral uniformity).

---

### Group E: Interactions [25:49] -- 24D

| Index | Feature Name | Group | Domain | Dim | Psychoacoustic Basis | Tier | Status |
|:-----:|-------------|:-----:|--------|:---:|---------------------|:----:|--------|
| 25 | x_l0l5_0 | E | CrossDomain | 1 | Energy x Consonance interaction (amp * roughness) | P | Existing |
| 26 | x_l0l5_1 | E | CrossDomain | 1 | Energy x Consonance interaction (amp * sethares) | P | Existing |
| 27 | x_l0l5_2 | E | CrossDomain | 1 | Energy x Consonance interaction | P | Existing |
| 28 | x_l0l5_3 | E | CrossDomain | 1 | Energy x Consonance interaction | P | Existing |
| 29 | x_l0l5_4 | E | CrossDomain | 1 | Energy x Consonance interaction | P | Existing |
| 30 | x_l0l5_5 | E | CrossDomain | 1 | Energy x Consonance interaction | P | Existing |
| 31 | x_l0l5_6 | E | CrossDomain | 1 | Energy x Consonance interaction | P | Existing |
| 32 | x_l0l5_7 | E | CrossDomain | 1 | Energy x Consonance interaction (vel * stumpf) | P | Existing |
| 33 | x_l4l5_0 | E | CrossDomain | 1 | Change x Consonance interaction (flux * roughness) | P | Existing |
| 34 | x_l4l5_1 | E | CrossDomain | 1 | Change x Consonance interaction | P | Existing |
| 35 | x_l4l5_2 | E | CrossDomain | 1 | Change x Consonance interaction | P | Existing |
| 36 | x_l4l5_3 | E | CrossDomain | 1 | Change x Consonance interaction | P | Existing |
| 37 | x_l4l5_4 | E | CrossDomain | 1 | Change x Consonance interaction | P | Existing |
| 38 | x_l4l5_5 | E | CrossDomain | 1 | Change x Consonance interaction | P | Existing |
| 39 | x_l4l5_6 | E | CrossDomain | 1 | Change x Consonance interaction | P | Existing |
| 40 | x_l4l5_7 | E | CrossDomain | 1 | Change x Consonance interaction (entropy * stumpf) | P | Existing |
| 41 | x_l5l7_0 | E | CrossDomain | 1 | Consonance x Timbre interaction (roughness * warmth) | P | Existing |
| 42 | x_l5l7_1 | E | CrossDomain | 1 | Consonance x Timbre interaction | P | Existing |
| 43 | x_l5l7_2 | E | CrossDomain | 1 | Consonance x Timbre interaction | P | Existing |
| 44 | x_l5l7_3 | E | CrossDomain | 1 | Consonance x Timbre interaction | P | Existing |
| 45 | x_l5l7_4 | E | CrossDomain | 1 | Consonance x Timbre interaction | P | Existing |
| 46 | x_l5l7_5 | E | CrossDomain | 1 | Consonance x Timbre interaction | P | Existing |
| 47 | x_l5l7_6 | E | CrossDomain | 1 | Consonance x Timbre interaction | P | Existing |
| 48 | x_l5l7_7 | E | CrossDomain | 1 | Consonance x Timbre interaction (stumpf * autocorr) | P | Existing |

**Phase 6 notes**: All 24 features use independent proxies instead of actual A-D outputs (proxy mismatch). Phase 6 Stage 1: replace proxies with real group outputs. Phase 6 Stage 2 (v2.1): add F-K cross-group interactions (+16D).

---

### Group F: Pitch & Chroma [49:65] -- 16D

| Index | Feature Name | Group | Domain | Dim | Psychoacoustic Basis | Tier | Status |
|:-----:|-------------|:-----:|--------|:---:|---------------------|:----:|--------|
| 49 | chroma_C | F | Tonal | 1 | Octave equivalence, pitch class 0 (Shepard 1964, Krumhansl 1990) | A | New |
| 50 | chroma_Db | F | Tonal | 1 | Octave equivalence, pitch class 1 | A | New |
| 51 | chroma_D | F | Tonal | 1 | Octave equivalence, pitch class 2 | A | New |
| 52 | chroma_Eb | F | Tonal | 1 | Octave equivalence, pitch class 3 | A | New |
| 53 | chroma_E | F | Tonal | 1 | Octave equivalence, pitch class 4 | A | New |
| 54 | chroma_F | F | Tonal | 1 | Octave equivalence, pitch class 5 | A | New |
| 55 | chroma_Gb | F | Tonal | 1 | Octave equivalence, pitch class 6 | A | New |
| 56 | chroma_G | F | Tonal | 1 | Octave equivalence, pitch class 7 | A | New |
| 57 | chroma_Ab | F | Tonal | 1 | Octave equivalence, pitch class 8 | A | New |
| 58 | chroma_A | F | Tonal | 1 | Octave equivalence, pitch class 9 | A | New |
| 59 | chroma_Bb | F | Tonal | 1 | Octave equivalence, pitch class 10 | A | New |
| 60 | chroma_B | F | Tonal | 1 | Octave equivalence, pitch class 11 | A | New |
| 61 | pitch_height | F | Tonal | 1 | Weber-Fechner law: perceived pitch ~ log(frequency) | S | New |
| 62 | pitch_class_entropy | F | Tonal | 1 | Pitch distribution uniformity (information theory) | S | New |
| 63 | pitch_salience | F | Tonal | 1 | Virtual pitch salience (Parncutt 1989 proxy) | A | New |
| 64 | inharmonicity_index | F | Tonal | 1 | Harmonic series deviation measurement | A | New |

**Implementation**: mel -> exp -> Gaussian soft-assignment chroma matrix (128x12) -> L1 norm. Chroma quality is approximate (mel-based, not CQT).

---

### Group G: Rhythm & Groove [65:75] -- 10D

| Index | Feature Name | Group | Domain | Dim | Psychoacoustic Basis | Tier | Status |
|:-----:|-------------|:-----:|--------|:---:|---------------------|:----:|--------|
| 65 | tempo_estimate | G | Temporal | 1 | Entrainment / preferred tempo (Fraisse 1982) | A | New |
| 66 | beat_strength | G | Temporal | 1 | Pulse perception strength | A | New |
| 67 | pulse_clarity | G | Temporal | 1 | Beat ambiguity (Witek 2014 groove link) | A | New |
| 68 | syncopation_index | G | Temporal | 1 | Metrical conflict (Longuet-Higgins & Lee 1984) | A | New |
| 69 | metricality_index | G | Temporal | 1 | Metrical hierarchy (Grahn & Brett 2007) | A | New |
| 70 | isochrony_nPVI | G | Temporal | 1 | Rhythmic regularity (Ravignani 2021, Grabe & Low 2002) | S | New |
| 71 | groove_index | G | Temporal | 1 | Sensorimotor coupling (Madison 2006, Janata 2012) | A | New |
| 72 | event_density | G | Temporal | 1 | Temporal event density | S | New |
| 73 | tempo_stability | G | Temporal | 1 | Temporal prediction reliability | S | New |
| 74 | rhythmic_regularity | G | Temporal | 1 | IOI distribution regularity (Spiech 2022 inverse) | S | New |

**Dependencies**: B[11] onset_strength. Pipeline stage 2.

---

### Group H: Harmony & Tonality [75:87] -- 12D

| Index | Feature Name | Group | Domain | Dim | Psychoacoustic Basis | Tier | Status |
|:-----:|-------------|:-----:|--------|:---:|---------------------|:----:|--------|
| 75 | key_clarity | H | Tonal | 1 | Tonal hierarchy (Krumhansl & Kessler 1982) | A | New |
| 76 | tonnetz_fifth_x | H | Tonal | 1 | Circle-of-fifths projection x (Harte 2006, Balzano 1980) | S | New |
| 77 | tonnetz_fifth_y | H | Tonal | 1 | Circle-of-fifths projection y | S | New |
| 78 | tonnetz_minor_x | H | Tonal | 1 | Minor-third tonal relation x | S | New |
| 79 | tonnetz_minor_y | H | Tonal | 1 | Minor-third tonal relation y | S | New |
| 80 | tonnetz_major_x | H | Tonal | 1 | Major-third tonal relation x | S | New |
| 81 | tonnetz_major_y | H | Tonal | 1 | Major-third tonal relation y | S | New |
| 82 | voice_leading_distance | H | Tonal | 1 | Voice-leading parsimony (Tymoczko) | S | New |
| 83 | harmonic_change | H | Tonal | 1 | Harmonic change detection function (HCDF) | S | New |
| 84 | tonal_stability | H | Tonal | 1 | Tonal center stability (composite of [75] and [83]) | A | New |
| 85 | diatonicity | H | Tonal | 1 | Macroharmony diatonic/chromatic measure (Tymoczko) | A | New |
| 86 | syntactic_irregularity | H | Tonal | 1 | Harmonic syntax violation (Lerdahl 2001 tension) | A | New |

**Dependencies**: F[49:61] chroma. Pipeline stage 2.

---

### Group I: Information & Surprise [87:94] -- 7D

| Index | Feature Name | Group | Domain | Dim | Psychoacoustic Basis | Tier | Status |
|:-----:|-------------|:-----:|--------|:---:|---------------------|:----:|--------|
| 87 | melodic_entropy | I | Information | 1 | Melodic prediction error (IDyOM approx., Pearce 2005) | A | New |
| 88 | harmonic_entropy | I | Information | 1 | Chord transition surprise (Gold 2019, chroma KL) | A | New |
| 89 | rhythmic_information_content | I | Information | 1 | Rhythmic surprise (Spiech 2022, Shannon IC) | A | New |
| 90 | spectral_surprise | I | Information | 1 | Spectral prediction error (Friston free energy) | A | New |
| 91 | information_rate | I | Information | 1 | Mutual information per frame (Weineck 2022 link) | S | New |
| 92 | predictive_entropy | I | Information | 1 | Conditional prediction uncertainty (predictive coding) | A | New |
| 93 | tonal_ambiguity | I | Information | 1 | Key profile correlation entropy | A | New |

**Dependencies**: F chroma, G onset, H key. Pipeline stage 3. All features use EMA running statistics with tau=2.0s and 344-frame warm-up ramp.

---

### Group J: Timbre Extended [94:114] -- 20D

| Index | Feature Name | Group | Domain | Dim | Psychoacoustic Basis | Tier | Status |
|:-----:|-------------|:-----:|--------|:---:|---------------------|:----:|--------|
| 94 | mfcc_1 | J | Spectral | 1 | Cepstral coefficient 1 (vocal tract proxy) | S | New |
| 95 | mfcc_2 | J | Spectral | 1 | Cepstral coefficient 2 | S | New |
| 96 | mfcc_3 | J | Spectral | 1 | Cepstral coefficient 3 | S | New |
| 97 | mfcc_4 | J | Spectral | 1 | Cepstral coefficient 4 | S | New |
| 98 | mfcc_5 | J | Spectral | 1 | Cepstral coefficient 5 | S | New |
| 99 | mfcc_6 | J | Spectral | 1 | Cepstral coefficient 6 | S | New |
| 100 | mfcc_7 | J | Spectral | 1 | Cepstral coefficient 7 | S | New |
| 101 | mfcc_8 | J | Spectral | 1 | Cepstral coefficient 8 | S | New |
| 102 | mfcc_9 | J | Spectral | 1 | Cepstral coefficient 9 | S | New |
| 103 | mfcc_10 | J | Spectral | 1 | Cepstral coefficient 10 | S | New |
| 104 | mfcc_11 | J | Spectral | 1 | Cepstral coefficient 11 | S | New |
| 105 | mfcc_12 | J | Spectral | 1 | Cepstral coefficient 12 | S | New |
| 106 | mfcc_13 | J | Spectral | 1 | Cepstral coefficient 13 | S | New |
| 107 | spectral_contrast_1 | J | Spectral | 1 | Octave sub-band 1 peak-valley (Jiang 2002) | S | New |
| 108 | spectral_contrast_2 | J | Spectral | 1 | Octave sub-band 2 peak-valley | S | New |
| 109 | spectral_contrast_3 | J | Spectral | 1 | Octave sub-band 3 peak-valley | S | New |
| 110 | spectral_contrast_4 | J | Spectral | 1 | Octave sub-band 4 peak-valley | S | New |
| 111 | spectral_contrast_5 | J | Spectral | 1 | Octave sub-band 5 peak-valley | S | New |
| 112 | spectral_contrast_6 | J | Spectral | 1 | Octave sub-band 6 peak-valley | S | New |
| 113 | spectral_contrast_7 | J | Spectral | 1 | Octave sub-band 7 residual peak-valley | S | New |

**Implementation**: MFCC via pre-computed DCT matrix (128x13). Spectral contrast via per-octave sort, top/bottom 20% quantile difference.

---

### Group K: Modulation & Psychoacoustic [114:128] -- 14D

| Index | Feature Name | Group | Domain | Dim | Psychoacoustic Basis | Tier | Status |
|:-----:|-------------|:-----:|--------|:---:|---------------------|:----:|--------|
| 114 | modulation_0_5Hz | K | Psychoacoustic | 1 | Cortical temporal modulation (Chi & Shamma 2005) | A | New |
| 115 | modulation_1Hz | K | Psychoacoustic | 1 | Phrase-level rhythmic modulation | A | New |
| 116 | modulation_2Hz | K | Psychoacoustic | 1 | Beat-rate modulation | A | New |
| 117 | modulation_4Hz | K | Psychoacoustic | 1 | Speech syllabic rate / strong beat | A | New |
| 118 | modulation_8Hz | K | Psychoacoustic | 1 | Rapid articulation / tremolo | A | New |
| 119 | modulation_16Hz | K | Psychoacoustic | 1 | Roughness boundary / vibrato upper limit | A | New |
| 120 | modulation_centroid | K | Psychoacoustic | 1 | Dominant modulation rate (weighted mean) | S | New |
| 121 | modulation_bandwidth | K | Psychoacoustic | 1 | Modulation rate diversity (weighted std) | S | New |
| 122 | sharpness_zwicker | K | Psychoacoustic | 1 | DIN 45692 perceptual sharpness (Zwicker & Fastl 1999) | R | New |
| 123 | fluctuation_strength | K | Psychoacoustic | 1 | ~4 Hz temporal fluctuation (Zwicker & Fastl 1999) | A | New |
| 124 | loudness_a_weighted | K | Psychoacoustic | 1 | ISO 226 frequency-weighted loudness | S | New |
| 125 | alpha_ratio | K | Psychoacoustic | 1 | Low/high energy ratio (eGeMAPS, Eyben 2015) | S | New |
| 126 | hammarberg_index | K | Psychoacoustic | 1 | Spectral tilt measure (eGeMAPS) | S | New |
| 127 | spectral_slope_0_500 | K | Psychoacoustic | 1 | Low-frequency spectral shape (eGeMAPS) | S | New |

**Implementation**: Modulation via sliding-window FFT (window=344 frames, hop=86, fft_size=512). Sharpness via mel-to-Bark rebinning + Zwicker weighting. 344-frame warm-up for modulation features.

---

## Summary Statistics

### By Status

| Status | Count | Percentage |
|--------|:-----:|:----------:|
| Existing (v1) | 49 | 38.3% |
| New (v2) | 79 | 61.7% |
| **Total** | **128** | **100%** |

### By Quality Tier

| Tier | Label | Count | Percentage |
|:----:|-------|:-----:|:----------:|
| P | Proxy | 36 | 28.1% |
| A | Approximate | 49 | 38.3% |
| S | Standard | 42 | 32.8% |
| R | Reference | 1 | 0.8% |
| **Total** | | **128** | **100%** |

### By Domain

| Domain | Count | Percentage |
|--------|:-----:|:----------:|
| Psychoacoustic | 21 | 16.4% |
| Spectral | 34 | 26.6% |
| Tonal | 28 | 21.9% |
| Temporal | 14 | 10.9% |
| Information | 7 | 5.5% |
| CrossDomain | 24 | 18.8% |
| **Total** | **128** | **100%** |

### By Group

| Group | Name | Dim | Existing | New |
|-------|------|:---:|:--------:|:---:|
| A | Consonance | 7 | 7 | 0 |
| B | Energy | 5 | 5 | 0 |
| C | Timbre | 9 | 9 | 0 |
| D | Change | 4 | 4 | 0 |
| E | Interactions | 24 | 24 | 0 |
| F | Pitch & Chroma | 16 | 0 | 16 |
| G | Rhythm & Groove | 10 | 0 | 10 |
| H | Harmony & Tonality | 12 | 0 | 12 |
| I | Information & Surprise | 7 | 0 | 7 |
| J | Timbre Extended | 20 | 0 | 20 |
| K | Modulation & Psychoacoustic | 14 | 0 | 14 |
| **Total** | | **128** | **49** | **79** |
