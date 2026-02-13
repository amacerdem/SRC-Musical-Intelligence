# R3 Feature Quality Tier System

**Phase**: 3C -- Standards Documentation
**Source**: R3-V2-DESIGN.md Section 2 (all 128 feature specs), R3-CROSSREF.md Section 5

---

## 1. Tier Definitions

| Tier | Label | Description | Example |
|:----:|-------|-------------|---------|
| **P** | Proxy | Simple mathematical approximation with weak or no psychoacoustic validity. Formula does not implement the named concept. | roughness[0]: `var/mean` instead of Plomp-Levelt critical band model |
| **A** | Approximate | Reasonable approximation with known, documented limitations. Captures the correct perceptual dimension but deviates quantitatively from the reference method. | mel-based chroma[49:60]: correct pitch class concept, limited by mel frequency resolution below 200 Hz |
| **S** | Standard | Proper implementation following a published algorithm. Deviation from reference is small and well-characterized. | MFCC[94:106]: DCT of log-mel is the standard definition; no approximation involved |
| **R** | Reference | Gold-standard implementation matching published benchmark results within accepted tolerances. | (None currently in R3; target for Phase 6 upgrades) |

---

## 2. Quality Tier Assessment -- All 128 Features

### Group A: Consonance [0:7]

| Idx | Feature | Tier | Rationale | Phase 6 Target |
|:---:|---------|:----:|-----------|:--------------:|
| 0 | roughness | P | `var/mean` proxy, not Plomp-Levelt critical band roughness | S |
| 1 | sethares_dissonance | P | Adjacent mel bin diff, not pairwise `d(fi,fj,ai,aj)` | S |
| 2 | helmholtz_kang | P | Lag-1 autocorrelation only; true harmonicity requires multi-lag | A |
| 3 | stumpf_fusion | P | Low-frequency energy ratio; identical to warmth[12]; not Parncutt subharmonic matching | S |
| 4 | sensory_pleasantness | P | Arbitrary-weight combination of [1] and [3]; both are proxies themselves | A |
| 5 | inharmonicity | P | Simply `1 - [2]`; derived, not independent | A |
| 6 | harmonic_deviation | P | `0.5*[1] + 0.5*(1-[2])`; derived combination | A |

### Group B: Energy [7:12]

| Idx | Feature | Tier | Rationale | Phase 6 Target |
|:---:|---------|:----:|-----------|:--------------:|
| 7 | amplitude | A | RMS of log-mel (double compression bug) | S |
| 8 | velocity_A | A | First derivative with sigmoid normalization; loses physical scale | A |
| 9 | acceleration_A | A | Second derivative with sigmoid; same scaling issue | A |
| 10 | loudness | P | Stevens law on log-mel = double compression | S |
| 11 | onset_strength | S | HWR spectral flux; well-validated (Weineck 2022) | S |

### Group C: Timbre [12:21]

| Idx | Feature | Tier | Rationale | Phase 6 Target |
|:---:|---------|:----:|-----------|:--------------:|
| 12 | warmth | A | Low-frequency ratio; valid concept but identical to [3] | A |
| 13 | sharpness | A | High-frequency ratio; not DIN 45692 (see K[122] for Zwicker) | A |
| 14 | tonalness | A | Peak/sum ratio; reasonable proxy for Terhardt tonalness | A |
| 15 | clarity | A | Spectral centroid (misnamed as clarity, not C80) | A |
| 16 | spectral_smoothness | P | Complement of [1] (`1 - sethares`); not independent | A |
| 17 | spectral_autocorrelation | P | Duplicate of [2] (identical lag-1 autocorrelation) | A |
| 18 | tristimulus1 | A | Mel-band proxy of Pollard-Jansson (partial-based original) | A |
| 19 | tristimulus2 | A | Same mel-band proxy | A |
| 20 | tristimulus3 | A | Same mel-band proxy | A |

### Group D: Change [21:25]

| Idx | Feature | Tier | Rationale | Phase 6 Target |
|:---:|---------|:----:|-----------|:--------------:|
| 21 | spectral_flux | S | L2 frame diff, standard MIR computation | S |
| 22 | distribution_entropy | S | Shannon entropy of spectral distribution; correct formula | S |
| 23 | distribution_flatness | S | Wiener entropy (geo/arith mean); MPEG-7 compatible | S |
| 24 | distribution_concentration | P | Bug: uniform and concentrated both yield 1.0 | S |

### Group E: Interactions [25:49]

| Idx | Feature | Tier | Rationale | Phase 6 Target |
|:---:|---------|:----:|-----------|:--------------:|
| 25-32 | x_l0l5 (B x A, 8D) | P | Uses independent proxy, not actual A/B output | A |
| 33-40 | x_l4l5 (D x A, 8D) | P | Same proxy mismatch issue | A |
| 41-48 | x_l5l7 (A x C, 8D) | P | Same proxy mismatch issue | A |

### Group F: Pitch & Chroma [49:65] (NEW)

| Idx | Feature | Tier | Rationale | Phase 6 Target |
|:---:|---------|:----:|-----------|:--------------:|
| 49-60 | chroma_C..chroma_B (12D) | A | Mel-to-chroma Gaussian soft-assignment; limited below 200 Hz | A |
| 61 | pitch_height | A | Weighted mean log-frequency; Weber-Fechner law | A |
| 62 | pitch_class_entropy | S | Shannon entropy of chroma; correct formula | S |
| 63 | pitch_salience | A | Peak-to-median ratio; proxy for Parncutt virtual pitch salience | A |
| 64 | inharmonicity_index | A | Mel peak harmonic template matching (K=8); mel resolution limits accuracy | A |

### Group G: Rhythm & Groove [65:75] (NEW)

| Idx | Feature | Tier | Rationale | Phase 6 Target |
|:---:|---------|:----:|-----------|:--------------:|
| 65 | tempo_estimate | A | Onset autocorrelation; standard approach but mel-onset-based | A |
| 66 | beat_strength | A | Autocorrelation peak value at tempo lag | A |
| 67 | pulse_clarity | A | Peak/median ratio of autocorrelation; sigmoid normalization | A |
| 68 | syncopation_index | A | LHL model from mel onsets; requires benchmark validation | A |
| 69 | metricality_index | A | Multi-scale autocorrelation subdivision counting | A |
| 70 | isochrony_nPVI | A | nPVI from onset IOI; standard linguistics metric adapted | A |
| 71 | groove_index | A | Composite: syncopation x bass x clarity; needs behavioral validation | A |
| 72 | event_density | S | Onset count in sliding window; straightforward computation | S |
| 73 | tempo_stability | A | CV inverse of local tempo estimates | A |
| 74 | rhythmic_regularity | A | 1 - normalized IOI histogram entropy | A |

### Group H: Harmony & Tonality [75:87] (NEW)

| Idx | Feature | Tier | Rationale | Phase 6 Target |
|:---:|---------|:----:|-----------|:--------------:|
| 75 | key_clarity | A | Krumhansl-Schmuckler on mel-chroma; quality depends on chroma accuracy | A |
| 76-81 | tonnetz (6D) | S | Harte 2006 formula on chroma; mathematically exact given chroma input | S |
| 82 | voice_leading_distance | S | L1 distance between consecutive chroma vectors; exact computation | S |
| 83 | harmonic_change | S | Cosine distance between consecutive chroma; standard HCDF | S |
| 84 | tonal_stability | A | Composite: key_clarity x (1 - harmonic_change_rate) | A |
| 85 | diatonicity | A | Active pitch class count mapping; Tymoczko macroharmony proxy | A |
| 86 | syntactic_irregularity | A | KL divergence from key template; Lerdahl tension proxy | A |

### Group I: Information & Surprise [87:94] (NEW)

| Idx | Feature | Tier | Rationale | Phase 6 Target |
|:---:|---------|:----:|-----------|:--------------:|
| 87 | melodic_entropy | A | Chroma transition entropy; IDyOM approximation (needs benchmark) | A |
| 88 | harmonic_entropy | A | Chroma KL divergence from EMA; chord surprise proxy | A |
| 89 | rhythmic_information_content | A | IOI histogram log-probability; Shannon IC from mel onsets | A |
| 90 | spectral_surprise | A | Mel KL divergence from EMA; Friston prediction error proxy | A |
| 91 | information_rate | A | Frame-pair mutual information approximation | A |
| 92 | predictive_entropy | A | Gaussian entropy of prediction residual variance | A |
| 93 | tonal_ambiguity | A | Softmax entropy of 24 key correlations | A |

### Group J: Timbre Extended [94:114] (NEW)

| Idx | Feature | Tier | Rationale | Phase 6 Target |
|:---:|---------|:----:|-----------|:--------------:|
| 94-106 | mfcc_1..mfcc_13 (13D) | S | DCT-II of log-mel is the standard MFCC definition | S |
| 107-113 | spectral_contrast_1..7 (7D) | A | Mel-band peak/valley computation; Jiang 2002 adapted to mel bins | A |

### Group K: Modulation & Psychoacoustic [114:128] (NEW)

| Idx | Feature | Tier | Rationale | Phase 6 Target |
|:---:|---------|:----:|-----------|:--------------:|
| 114-119 | modulation_0.5Hz..16Hz (6D) | A | Per-band temporal FFT at target rates; Chi/Shamma cortical model approximation | A |
| 120 | modulation_centroid | S | Weighted mean of modulation energies; straightforward computation | S |
| 121 | modulation_bandwidth | S | Weighted std of modulation energies | S |
| 122 | sharpness_zwicker | A | Mel-to-Bark rebinning; DIN 45692 formula with Zwicker g(z) weighting | A |
| 123 | fluctuation_strength | A | Derived from modulation_4Hz; simplified Zwicker model | A |
| 124 | loudness_a_weighted | A | A-weighting on mel; not full ISO 226 phon calibration | A |
| 125 | alpha_ratio | A | Mel-band low/high ratio; eGeMAPS adapted | A |
| 126 | hammarberg_index | A | Mel-band peak ratio; eGeMAPS adapted | A |
| 127 | spectral_slope_0_500 | A | Linear regression on mel bins 0-18; eGeMAPS adapted | A |

---

## 3. Tier Distribution Summary

| Tier | Count | Percentage | Description |
|:----:|:-----:|:----------:|-------------|
| **P** (Proxy) | 21 | 16.4% | A[0-6], B[10], C[16-17], D[24], E[25-48] |
| **A** (Approximate) | 72 | 56.3% | B[7-9], C[12-15,18-20], F, G, H (partial), I, J (contrast), K |
| **S** (Standard) | 35 | 27.3% | B[11], D[21-23], F[62], G[72], H[76-83], J[94-106], K[120-121] |
| **R** (Reference) | 0 | 0.0% | None currently |

---

## 4. Phase 6 Upgrade Path: Proxy to Standard

Features currently at Proxy tier with planned Phase 6 upgrades to Standard:

| Feature | Current Tier | Phase 6 Change | Target Tier |
|---------|:----:|----------------|:----:|
| roughness[0] | P | Critical band pairwise comparison within ERB bands | S |
| sethares_dissonance[1] | P | Real Sethares timbre-dependent `d(fi,fj,ai,aj)` | S |
| stumpf_fusion[3] | P | Parncutt subharmonic matching | S |
| loudness[10] | P | `exp(log_mel).pow(0.3)` or full Zwicker ISO 532-1 | S |
| distribution_concentration[24] | P | Correct HHI formula: `(HHI - 1/N) / (1 - 1/N)` | S |
| E interactions[25:49] | P | Replace proxies with actual A-D group outputs | A |

---

## 5. Quality Assessment Methodology

Each feature is assessed on three axes:

1. **Algorithmic fidelity**: Does the formula implement the named psychoacoustic concept?
   - Reference algorithm identified from the literature citation in R3-V2-DESIGN.md
   - Deviation classified as: none (S/R), known quantitative (A), or qualitative (P)

2. **Domain correctness**: Is the computation performed in the correct signal domain?
   - Mel-domain computation where Hz-domain is required = tier penalty
   - Log-domain computation where linear is required = tier penalty (e.g., loudness[10])

3. **Independence**: Is the feature measuring a genuinely independent perceptual dimension?
   - Derived features (`1-x`, `0.5*a + 0.5*b`) receive P tier
   - Duplicate features ([3]=[12], [2]=[17]) flagged; the copy receives P tier

---

*Source: R3-V2-DESIGN.md Section 2 (feature specs), R3-CROSSREF.md Section 5 (revision decisions)*
