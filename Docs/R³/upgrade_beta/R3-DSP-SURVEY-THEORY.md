# R³ DSP Survey — Theory & Local Literature
## Phase 3A-2 (Chat R2): Psychoacoustic & Computational Music Theory Feature Inventory

**Date:** 2026-02-13
**Scope:** Literature/r3/ (121 markdown files from 58 PDFs) + mi_beta/ear/r3/ (5 groups, 49D)
**Output:** Candidate feature inventory for R³ expansion (49D → 128–256D)

---

## 1. Executive Summary

**Files scanned:** 121 markdown files across 5 subdirectories:
- `psychoacoustics/` — 11 files (Plomp-Levelt, Sethares, Helmholtz, JI, neural correlates)
- `dsp-and-ml/` — 4 files (CNN genre classification, spectral contrast, modulation, microtonal AMT)
- `spectral-music/` — 7 files (Anderson, Grisey, Fineberg, spectral composition theory)
- `computational-music-theory/` — 65 files (Tymoczko, Neo-Riemannian, Balzano, Lewin, Hook)
- `music-theory-analysis/` — 34 files (consonance models, geometry, neurodynamics, affect)

**Candidate features found:** 67 distinct measurable features
**Category distribution:**

| Category | Count | Mel-Derivable | Needs Chroma | Needs Raw Audio |
|----------|-------|---------------|--------------|-----------------|
| A: Consonance (revision) | 12 | 4 | 5 | 3 |
| B: Energy (revision) | 4 | 4 | 0 | 0 |
| C: Timbre (revision) | 8 | 6 | 0 | 2 |
| D: Change (revision) | 5 | 5 | 0 | 0 |
| F: Pitch (NEW) | 10 | 3 | 6 | 1 |
| G: Rhythm (NEW) | 7 | 5 | 0 | 2 |
| H: Harmony (NEW) | 12 | 0 | 12 | 0 |
| I: Information (NEW) | 9 | 4 | 3 | 2 |
| **Total** | **67** | **31** | **26** | **10** |

**Key finding:** The current 49D R³ has ~15–20 effective independent dimensions due to extensive cross-group redundancy. The literature supports expansion to 128D+ with psychoacoustically grounded features, particularly in Pitch (F), Harmony (H), and Information (I) groups which are entirely absent.

---

## 2. Current R³ Critique (Literature-Based)

### 2.1 Group A: Consonance [0:7] — 7D

**Code:** `mi_beta/ear/r3/psychoacoustic/consonance.py`

| Index | Name | Method | Fidelity | Issues |
|-------|------|--------|----------|--------|
| 0 | roughness | `sigmoid(spectral_variance / spectral_mean)` | **LOW** | Not Plomp-Levelt. Uses bulk spectral variance as proxy. Real roughness requires pairwise partial comparison within critical bands (Plomp & Levelt 1965; Pressnitzer & McAdams 2000). Register-dependent critical bandwidth not modeled. |
| 1 | sethares_dissonance | Mean abs difference of adjacent mel bins, max-normalized | **LOW** | Not Sethares (1993). Sethares model computes pairwise dissonance between ALL partial pairs weighted by amplitudes. This is spectral irregularity (Krimphoff 1994), not dissonance. |
| 2 | helmholtz_kang | Lag-1 spectral autocorrelation | **LOW-MODERATE** | Captures harmonic regularity but only at lag-1. Real harmonicity requires multi-lag autocorrelation or template matching (Terhardt 1979). |
| 3 | stumpf_fusion | Low-quarter energy ratio | **LOW** | Stumpf fusion is about perceptual merging of simultaneous tones into one percept (CDC-2). Energy ratio in low mel bins is unrelated. **Identical to warmth [12].** |
| 4 | sensory_pleasantness | `0.6*(1-[1]) + 0.4*[3]` | **LOW** | Derived feature. Linear combination with arbitrary weights. Real pleasantness models (Harrison & Pearce 2020) combine roughness, harmonicity, and familiarity. |
| 5 | inharmonicity | `1 - helmholtz_kang [2]` | **DERIVED** | Complement of [2]. Not an independent feature. |
| 6 | harmonic_deviation | `0.5*[1] + 0.5*(1-[2])` | **DERIVED** | Linear combination. Not independent. |

**Literature verdict:** The entire Consonance group uses **proxy features** that do not implement any established consonance model (Plomp-Levelt, Sethares, Vassilakis, Parncutt, Stolzenburg). No critical band analysis, no partial extraction, no pairwise interaction computation. The naming (Helmholtz, Sethares, Stumpf) is misleading.

**Effective independent dimensions:** ~3 (roughness proxy, spectral autocorrelation, low-freq energy ratio). Features [4-6] are linear combinations; [3] duplicates [12].

**Sources:** Literature/r3/psychoacoustics/Consonance&Dissonance_Part1.md, Part2.md; Pressnitzer_2000_ContMusRev.md; music-theory-analysis/harmony_perception_by_periodicity_detection.md

### 2.2 Group B: Energy [7:12] — 5D

**Code:** `mi_beta/ear/r3/dsp/energy.py`

| Index | Name | Method | Fidelity | Issues |
|-------|------|--------|----------|--------|
| 7 | amplitude | RMS of mel bins, max-normalized | **MODERATE** | RMS on log-mel creates double-compression. Should apply to linear spectrogram. |
| 8 | velocity_A | `sigmoid(d(amplitude)/dt * 5)` | **LOW-MODERATE** | Arbitrary gain factor 5.0. Sigmoid centers at 0.5. Frame-rate dependent. |
| 9 | acceleration_A | `sigmoid(d²(amplitude)/dt² * 5)` | **LOW** | Same issues as velocity. Boundary frames always = sigmoid(0) = 0.5. |
| 10 | loudness | `amplitude^0.3` (Stevens) | **LOW** | Stevens' law applied to log-mel RMS = double compression. Should apply to linear power. ISO 532-1/2 (Zwicker/Moore-Glasberg) are proper loudness models. |
| 11 | onset_strength | HWR spectral flux (L1, positive-only) | **MODERATE** | Standard onset detection function (Bello 2005). Most faithful feature in this group. Validated as strongest neural synchronization driver (Weineck et al. 2022). |

**Literature verdict:** The amplitude/loudness computation has a systematic domain error: Stevens' power law is applied to log-mel values instead of linear power. The derivative chain (amplitude → velocity → acceleration) is conceptually sound but sigmoid normalization obscures physical meaning.

**Effective independent dimensions:** ~3 (amplitude, velocity, onset_strength).

**Sources:** Literature/r3/psychoacoustics/elife-neural_Part1.md (spectral flux validation)

### 2.3 Group C: Timbre [12:21] — 9D

**Code:** `mi_beta/ear/r3/dsp/timbre.py`

| Index | Name | Method | Fidelity | Issues |
|-------|------|--------|----------|--------|
| 12 | warmth | Bottom-quarter energy ratio | **LOW** | **= stumpf_fusion [3]** (identical formula) |
| 13 | sharpness | Top-quarter energy ratio | **LOW** | DIN 45692 sharpness requires Bark-scale with Zwicker weighting `g(z)`. This is just a high-freq ratio. |
| 14 | tonalness | `max(mel) / sum(mel)` | **LOW** | Single-peak dominance measure. Real tonalness (Terhardt 1979, Aures 1985) compares harmonic peaks to noise floor in critical bands. |
| 15 | clarity | Spectral centroid / N | **MODERATE** | Standard MIR brightness feature. Mislabeled as "clarity" (which means C80 early-to-late energy ratio in acoustics). |
| 16 | spectral_smoothness | `1 - spectral_irregularity` | **LOW-MODERATE** | **= 1 - sethares_dissonance [1]** (complement). Krimphoff/Jensen irregularity approximation. |
| 17 | spectral_autocorrelation | Lag-1 autocorrelation | **DUPLICATE** | **= helmholtz_kang [2]** (identical computation) |
| 18 | tristimulus1 | Bottom-third energy ratio | **LOW** | Pollard-Jansson tristimulus needs partials, not mel-band thirds. Overlaps with warmth [12]. |
| 19 | tristimulus2 | Middle-third energy ratio | **LOW** | Same caveat. |
| 20 | tristimulus3 | Top-third energy ratio | **LOW** | Same caveat. |

**Literature verdict:** Major redundancy issues. Three cross-group duplicates. Tristimulus implementation approximates a partial-based concept with mel-band ratios. Spectral centroid (labeled "clarity") is the only standard, well-validated feature.

**Effective independent dimensions:** ~4 (centroid, low/mid/high energy ratios — but these are constrained to sum to 1.0).

**Sources:** Literature/r3/dsp-and-ml/Music_type_classification_by_spectral_contrast_fea.md

### 2.4 Group D: Change [21:25] — 4D

**Code:** `mi_beta/ear/r3/dsp/change.py`

| Index | Name | Method | Fidelity | Issues |
|-------|------|--------|----------|--------|
| 21 | spectral_flux | L2 full-spectrum flux, max-normalized | **MODERATE** | Standard MIR feature. Full (not half-wave rectified) unlike [11]. |
| 22 | distribution_entropy | Shannon entropy / log(N) | **MODERATE** | Principled normalization. Computed on log-mel probabilities (biases toward uniformity). |
| 23 | distribution_flatness | Wiener entropy (geometric/arithmetic mean) | **MODERATE** | Standard MPEG-7 descriptor. Highly correlated with [22]. |
| 24 | distribution_concentration | HHI * N | **LOW** | **Normalization bug:** HHI*N maps both uniform AND concentrated spectra to 1.0. Effective discrimination destroyed. |

**Literature verdict:** This group is critically thin (4D) for a "change" category. Three features (entropy, flatness, concentration) measure the same spectral uniformity property. The concentration feature has a normalization bug. Spectral flux is the only temporal change feature.

**Effective independent dimensions:** ~2 (spectral flux, spectral uniformity).

**Sources:** Literature/r3/psychoacoustics/elife-neural_Part1.md

### 2.5 Group E: Interactions [25:49] — 24D

**Code:** `mi_beta/ear/r3/cross_domain/interactions.py`

**Architecture issue:** Independently recomputes proxy features from mel instead of using Groups A-D outputs. Two proxy mismatches: (1) roughness_proxy omits `/spectral_mean` divisor; (2) helmholtz_proxy uses `max/sum` (= tonalness) instead of spectral autocorrelation.

**Feature structure:** 24 element-wise products organized as:
- x_l0l5 [25:33]: Energy × Consonance (8D)
- x_l4l5 [33:41]: Change × Consonance (8D)
- x_l5l7 [41:49]: Consonance × Timbre (8D)

**Literature verdict:** The interaction concept (capturing "simultaneous presence") is valid for psychoacoustic research. However, since base features have high redundancy, the 24 interaction terms inherit and multiply that redundancy. Product of two [0,1] values biases heavily toward zero.

**Effective independent dimensions:** ~8–10 (due to base feature redundancy propagation).

### 2.6 Overall Redundancy Map

| Feature A | Feature B | Relationship |
|-----------|-----------|-------------|
| stumpf_fusion [3] | warmth [12] | **Identical** (low-quarter energy ratio) |
| sethares_dissonance [1] | spectral_smoothness [16] | **Complement** (smoothness = 1 - sethares) |
| helmholtz_kang [2] | spectral_autocorrelation [17] | **Identical** (lag-1 autocorrelation) |
| helmholtz_kang [2] | inharmonicity [5] | **Complement** (inharmonicity = 1 - helmholtz) |
| sensory_pleasantness [4] | combo of [1],[3] | **Derived** (linear combination) |
| harmonic_deviation [6] | combo of [1],[2] | **Derived** (linear combination) |
| entropy [22] | flatness [23] | **Highly correlated** (both measure spectral uniformity) |
| flatness [23] | concentration [24] | **Highly correlated** (both measure peakiness) |
| warmth [12] | tristimulus1 [18] | **Nearly identical** (quarter vs. third boundary) |

**Total effective independent dimensions: ~15–20 out of nominal 49D**

---

## 3. Revision Proposals for Existing Groups (A–E)

### 3.1 Group A: Consonance → Proper Psychoacoustic Models

**Current:** 7D of proxy features (3 independent)
**Proposed:** 10–12D of literature-grounded consonance features

| # | Feature | Method | Source |
|---|---------|--------|--------|
| A.0 | plomp_levelt_roughness | Pairwise partial roughness within critical bands: `R = Σ_{i,j} A_i * A_j * g(Δf_{ij} / CB(f_{center}))` where g is the Plomp-Levelt curve (max at ~25% of CB). Requires spectral peak detection. | Plomp & Levelt (1965); Pressnitzer_2000_ContMusRev.md |
| A.1 | vassilakis_roughness | 3-factor model: `R = 0.5 * (A_i*A_j)^0.1 * (2*A_min/(A_i+A_j))^3.11 * [exp(-3.5*s*Δf) - exp(-5.75*s*Δf)]` where s = 0.24/(0.0207*f_center + 18.96) | Vassilakis (2005); Consonance&Dissonance_Part2.md |
| A.2 | sethares_dissonance | Timbre-dependent dissonance: sum pairwise `d(fi,fj,ai,aj) = ai*aj * [exp(-b1*s*|fi-fj|) - exp(-b2*s*|fi-fj|)]` with s = d_max/(s1*f_min + s2) | Sethares (1993); Consonance&Dissonance_Part2.md |
| A.3 | harmonicity_autocorr | Multi-lag spectral autocorrelation: `H = max_{τ>0} Σ_k S(k)*S(k+τ) / (||S|| * ||S_shifted||)` | Terhardt (1979); harmony_perception_by_periodicity_detection.md |
| A.4 | harmonic_distance | Tenney HD: `HD = log2(a*b)` for frequency ratio a:b (rational approximation via Stern-Brocot tree with JND ~1% tolerance) | Fundamental_Principles_of_Just_Intonatio_Part2.md |
| A.5 | harmonic_intersection | Tenney intersection: `I = (a+b-1)/(a*b)` — differentiates otonal from utonal | Fundamental_Principles_of_Just_Intonatio_Part2.md |
| A.6 | tonal_fusion | Degree to which aggregate matches single harmonic series template (subharmonic matching, Parncutt 1989) | simultaneous_consonance_in_music_perception_and_composition.md |
| A.7 | critical_band_ratio | Frequency separation / critical bandwidth at center frequency. Key parameter for roughness computation. `CB(f) = 24.7 * (4.37*f/1000 + 1)` Hz (ERB) | Pressnitzer_2000_ContMusRev.md; Greenwood (1961) |
| A.8 | spectral_centroid | Weighted mean frequency: `SC = Σ(f_k * M_k) / Σ(M_k)` (replaces misnamed "clarity" [15]) | Standard MIR; Music_type_classification_by_spectral_contrast_fea.md |
| A.9 | spectral_irregularity | Jensen (1999): `IRR = Σ_k (A_k - (A_{k-1}+A_k+A_{k+1})/3)² / Σ A_k²` | Krimphoff et al. (1994) |
| ÖNERİ: A.10 | combination_tone_strength | First-order: `f_diff = f1-f2`; higher orders from cochlear nonlinearity. Measures non-linear distortion products. | Pressnitzer_2000_ContMusRev.md |
| ÖNERİ: A.11 | coincident_harmonics_count | Count matching partials between two complex tones within audible range (Benade) | ji_primer_ed3.md |

### 3.2 Group B: Energy → Perceptual Loudness

**Current:** 5D (3 independent)
**Proposed:** 7D with proper loudness model

| # | Feature | Method | Source |
|---|---------|--------|--------|
| B.0 | rms_amplitude | RMS on **linear** spectrogram (not log-mel) | Standard |
| B.1 | velocity | `d(rms)/dt` with proper frame-rate normalization (no sigmoid) | Standard |
| B.2 | acceleration | `d²(rms)/dt²` | Standard |
| B.3 | zwicker_loudness | ISO 532-1: specific loudness per Bark band → total loudness in sone. Requires linear spectrum. | ISO 532-1; Pressnitzer_2000_ContMusRev.md |
| B.4 | onset_strength | HWR spectral flux (validated by Weineck et al. 2022 as strongest neural correlate) | elife-neural_Part1.md |
| B.5 | dynamic_range | `max(rms) - min(rms)` over sliding window, normalized | Standard MIR |
| ÖNERİ: B.6 | masking_pattern | Asymmetric excitation pattern on basilar membrane; affects perceived energy balance | Pressnitzer_2000_ContMusRev.md |

### 3.3 Group C: Timbre → Deduplicated + Extended

**Current:** 9D (4 independent due to duplicates)
**Proposed:** 10D with proper deduplication

| # | Feature | Method | Source |
|---|---------|--------|--------|
| C.0 | spectral_centroid | (moved from clarity [15], properly named) | Standard |
| C.1 | spectral_spread | Second central moment of spectrum: `σ² = Σ(f_k - SC)² * M_k / Σ M_k` | Standard MIR |
| C.2 | spectral_skewness | Third central moment (asymmetry of spectral shape) | Standard MIR |
| C.3 | spectral_kurtosis | Fourth central moment (peakedness) | Standard MIR |
| C.4 | spectral_rolloff | Frequency below which 85% of spectral energy is concentrated | Standard MIR; dsp-and-ml/ papers |
| C.5 | spectral_contrast | Octave-band peak-valley difference (Jiang 2002). 6D: 6 octave sub-bands. | Music_type_classification_by_spectral_contrast_fea.md |
| C.6 | zwicker_sharpness | DIN 45692: `S = 0.11 * ∫ N'(z)*g(z)*z dz / ∫ N'(z) dz` with weighting function g(z) on Bark scale | Zwicker; Pressnitzer_2000_ContMusRev.md |
| C.7 | warmth | Low-frequency energy ratio (below ~500 Hz mel bands) | Alluri & Toiviainen (2010) |
| C.8 | tristimulus_proper | If partial extraction available: T1=a1/Σ, T2=(a2+a3+a4)/Σ, T3=Σ_{k≥5}/Σ. Otherwise: mel-band approximation with clear caveat. | Pollard & Jansson (1982) |
| ÖNERİ: C.9 | inharmonicity_score | Deviation of peak frequencies from nearest harmonic series: `INH = Σ |f_k - k*f_0| / (k*f_0)` | Standard; Stanford-Spectral.md |

### 3.4 Group D: Change → Expanded Temporal Features

**Current:** 4D (2 independent)
**Proposed:** 8D covering multiple temporal scales

| # | Feature | Method | Source |
|---|---------|--------|--------|
| D.0 | spectral_flux_l2 | L2 full-spectrum flux (current [21]) | Standard |
| D.1 | spectral_flux_hwr | HWR positive-only flux (= onset_strength, but grouped here for temporal analysis) | Weineck et al. (2022) |
| D.2 | spectral_entropy | Shannon entropy of mel probability distribution, normalized by log(N) | Standard |
| D.3 | spectral_flatness | Wiener entropy: `exp(mean(log(p))) / mean(p)` | MPEG-7 |
| D.4 | novelty_function | Self-similarity matrix diagonal derivative (Foote 2000) | Standard MIR |
| D.5 | temporal_centroid | Center of mass of energy envelope within analysis window | Standard |
| ÖNERİ: D.6 | modulation_spectrum | AM envelope rate in 4–16 Hz band (speech/music temporal modulation) | Automatic_Music_Genre_Classification_Based_on_Modu.md |
| ÖNERİ: D.7 | spectral_change_rate | Rate of spectral centroid movement (Hz/s) | Anderson_provisional_history_spectral.md |

### 3.5 Group E: Interactions → Principled Redesign

**Current:** 24D of recomputed products with proxy mismatches
**Proposed:** Redesign pending final group structure. Options:

1. **Curated cross-group products** (current approach, fixed): Use actual Group A-D outputs instead of independent proxies. Fix roughness and helmholtz proxy mismatches.
2. **Learned interactions** (ÖNERİ): Replace fixed products with a small learned MLP that discovers relevant cross-group relationships.
3. **Psychoacoustically motivated interactions** only: e.g., roughness × loudness (masking interaction), harmonicity × spectral flux (harmonic surprise), brightness × roughness (Sethares timbre-dependent dissonance).

---

## 4. New Group Proposals (F–I)

### 4.1 Group F: Pitch (NEW — 12–16D)

**Justification:** R³ currently has NO pitch representation. 96 C³ models in SPU, PCU, and IMU rely heavily on pitch features. All 7 R³ gap logs mention missing pitch-related dimensions.

| # | Feature | Computation | Mel Derivability | Source |
|---|---------|-------------|-----------------|--------|
| F.0 | chroma_vector (12D) | 12-bin pitch class profile from mel spectrogram. Method: fold mel bands into 12 chroma bins using mel-to-pitch mapping. | **Dolaylı** — mel-based chroma is coarser than CQT-based but feasible | Krumhansl (1990); Balzano (1980) |
| F.1 | pitch_height | Weighted mean log-frequency from mel spectrogram: `PH = Σ(log(f_k) * M_k) / Σ M_k` | **Doğrudan** | Tymoczko; Standard MIR |
| F.2 | pitch_salience | Spectral peak prominence: ratio of peak energy to surrounding spectral noise floor | **Doğrudan** — from mel peaks | Parncutt (2019); elife-neural_Part2.md |
| F.3 | virtual_pitch_salience | Harmonic template matching: for each candidate f0, check if harmonic series `{f0, 2f0, 3f0...}` matches spectral peaks | **Dolaylı** — requires harmonic template matching on mel | Parncutt (1989); mp3604_05_parncutt_406430.md |
| F.4 | pitch_class_entropy | Shannon entropy of chroma distribution: `H = -Σ p_c * log(p_c)` | **Dolaylı** — via chroma | Standard |
| ÖNERİ: F.5 | vibrato_rate | AM modulation frequency of spectral peaks (4–8 Hz typical) | **Doğrudan** — from temporal envelope modulation | Intonation_of_Harmonic_Intervals_Adaptab.md |
| ÖNERİ: F.6 | vibrato_extent | AM modulation depth (semitones of frequency deviation) | **Doğrudan** | Same |
| ÖNERİ: F.7 | pitch_register | Octave band of dominant pitch activity (low/mid/high) | **Doğrudan** — from mel spectral envelope | Standard |

**Dimensionality:** 12 (chroma) + 1 (height) + 1 (salience) + 1 (virtual pitch) + 1 (PC entropy) = **16D** base. Vibrato adds 2D optional = **18D max**.

### 4.2 Group G: Rhythm (NEW — 8–12D)

**Justification:** R³ has onset_strength but no tempo, beat, or metrical features. STU (14 models) and MPU (10 models) critically need rhythm features.

| # | Feature | Computation | Mel Derivability | Source |
|---|---------|-------------|-----------------|--------|
| G.0 | tempo_estimate | Autocorrelation of onset strength → dominant period → BPM | **Doğrudan** — from onset function autocorrelation | Standard MIR |
| G.1 | beat_strength | Peak value of onset function autocorrelation at estimated tempo period | **Doğrudan** | Standard |
| G.2 | pulse_clarity | Ratio of autocorrelation peak to noise floor (how clear is the beat?) | **Doğrudan** | Standard |
| G.3 | metrical_level | Number of hierarchically nested pulse levels detected (1=no meter, 4=strong meter) | **Doğrudan** — multi-scale autocorrelation | thinking_about_musical_time.md (Morris) |
| ÖNERİ: G.4 | syncopation_index | Degree of off-beat accent relative to metrical grid (Witek et al. 2014) | **Dolaylı** — needs beat tracking + accent detection | Not in local literature — **Chat R3 web search needed** |
| ÖNERİ: G.5 | groove_factor | Relationship between tempo stability and microtiming deviations | **Dolaylı** — needs beat tracking | Not in local literature — **Chat R3 web search needed** |
| G.6 | event_density | Number of onsets per second (from onset detection) | **Doğrudan** | Standard |
| ÖNERİ: G.7 | rhythmic_entropy | Entropy of inter-onset-interval distribution | **Doğrudan** — from onset times | Standard |

**Dimensionality:** 8D base + 4D optional = **12D max**.

### 4.3 Group H: Harmony (NEW — 12–18D)

**Justification:** Harmony is the most requested missing category across all gap logs. PCU (9 gaps), IMU (13 gaps), and ASU (8 gaps) all cite harmony features. Computational music theory literature (Tymoczko, Neo-Riemannian) provides rich computational frameworks.

| # | Feature | Computation | Mel Derivability | Source |
|---|---------|-------------|-----------------|--------|
| H.0 | key_clarity | Krumhansl-Schmuckler key-finding: max correlation of chroma profile with 24 major/minor probe-tone templates | **Dolaylı** — via chroma | Krumhansl (1990); perception_of_affect_in_unfamiliar_musical_chords.md |
| H.1 | key_mode | Index of best-fit key template (0–23 for 12 major + 12 minor) — encoded as 2D (key × mode) | **Dolaylı** — via chroma | Same |
| H.2 | chord_template_match (12D) | Correlation of chroma vector with 24 major+minor chord templates. Top-1 as scalar or full 24D correlation profile compressed to 12D | **Dolaylı** — via chroma | Parncutt (2019); fluidharmony.md |
| H.3 | voice_leading_distance | `d_VL = min_σ Σ|a_i - b_σ(i)|` between successive chord chroma vectors | **Dolaylı** — via chroma comparison | Tymoczko; Geometry_of_Music_Part2.md |
| H.4 | tonnetz_coordinates (6D) | Harte (2006) 6D Tonnetz from chroma: `[Σ c_k sin(kπ/2), Σ c_k cos(kπ/2), ...]` for intervals of fifth, major third, minor third | **Dolaylı** — via chroma → 6D projection | Balzano (1980); the_tonnetz_at_first_sight.md |
| H.5 | harmonic_change | Frame-to-frame chroma cosine distance: `1 - cos(chroma_t, chroma_{t-1})` | **Dolaylı** — via chroma | Standard |
| H.6 | diatonicity | Tymoczko Mh: count of distinct PCs in window / 12. Low = diatonic, high = chromatic. | **Dolaylı** — via chroma | Tymoczko.md |
| H.7 | harmonic_tension | Lerdahl (2001) hierarchical tension model: surface + prolongational + inheritance | **Dolaylı** — via chord detection + key context | Not in local literature — **Chat R3 web search needed** |
| ÖNERİ: H.8 | pc_dft_coefficients (6D) | DFT magnitude of 12-bin chroma: T(1)..T(6) encoding interval-class content. T(5)=diatonicity, T(3)=triadicity, T(1)=chromaticity | **Dolaylı** — via chroma | fluidharmony_defining.md (Bernardes 2022) |
| ÖNERİ: H.9 | tonal_stability | Inverse of harmonic change rate + key clarity. High = stable tonal center. | **Dolaylı** — via key + chroma | Standard |
| ÖNERİ: H.10 | root_motion_fifths | Circle-of-fifths distance of successive chord roots: `(7*Δroot) mod 12` | **Dolaylı** — via chord root detection | Balzano (1980) |
| ÖNERİ: H.11 | mode_locking_stability | Neural oscillator coupling stability for detected intervals: `ε^((k+m-2)/2)` for Farey ratio k:m | **Dolaylı** — via pitch detection | Large et al. (2016); a_neurodynamic_account.md |

**Dimensionality:** 12 base (key, chord, VL, tonnetz, change, diatonicity) + 6D optional = **18D max**.

### 4.4 Group I: Information (NEW — 8–12D)

**Justification:** NDU (novelty detection, 9 models) and PCU (predictive coding, 10 models) critically need information-theoretic features. Shannon entropy is already in D group but limited to spectral domain.

| # | Feature | Computation | Mel Derivability | Source |
|---|---------|-------------|-----------------|--------|
| I.0 | spectral_surprise | KL divergence between current frame and running average: `D_KL(p_t || p̄)` | **Doğrudan** — from mel distributions | Standard |
| I.1 | chroma_surprise | KL divergence of current chroma from running chroma average | **Dolaylı** — via chroma | Standard |
| I.2 | self_information | `-log(p(frame_class))` where class from VQ codebook of spectral patterns | **Doğrudan** — requires offline codebook | Standard information theory |
| I.3 | predictive_entropy | Entropy of the conditional distribution `p(frame_t | frame_{t-1},...,frame_{t-k})` — measures uncertainty | **Doğrudan** — from frame statistics | Standard |
| I.4 | information_rate | `I(frame_t; frame_{t-1})` — mutual information between consecutive frames | **Doğrudan** — from mel distributions | Weineck et al. (2022) |
| I.5 | harmonic_surprisal | `-log(p(chord_t | chord_{t-1}))` — how unexpected is the current chord given the previous one? | **Dolaylı** — needs chord detection + transition matrix | ÖNERİ: based on IDyOM (Pearce 2005) — **Chat R3 needed** |
| ÖNERİ: I.6 | melodic_information_content | Weighted surprise of pitch events: `-log(p(pitch_t | context))` | **Dolaylı** — needs pitch tracking + statistical model | ÖNERİ: IDyOM framework |
| ÖNERİ: I.7 | spectral_complexity | Number of significant spectral peaks above noise floor per frame | **Doğrudan** — from mel peak detection | Standard |
| ÖNERİ: I.8 | tonal_ambiguity | Entropy of key template correlations: `H = -Σ p_key * log(p_key)` where p from softmax of key correlations | **Dolaylı** — via chroma + key profiles | Standard |

**Dimensionality:** 6 base + 3 optional = **9D max**.

---

## 5. Complete Candidate Feature Catalog

### Format: snake_case name | Category | R³ Group | Description | Psychoacoustic Basis | Computation | Range | Source | Current R³ | Mel Compatibility

---

### 5.1 Consonance Features

#### plomp_levelt_roughness
- **Kategori**: Consonance
- **Önerilen R³ Grubu**: A (revised)
- **Tanım**: Sum of pairwise roughness between all spectral partial pairs within critical bandwidth
- **Psikoakustik Temeli**: Plomp-Levelt (1965) critical band dissonance theory; beating between partials perceived as roughness at 20–300 Hz modulation rate
- **Hesaplama Yöntemi**: Detect spectral peaks → for each pair (fi, fj): R_ij = Ai * Aj * g(|fi-fj| / CB(f_center)) where g is Plomp-Levelt curve → sum all R_ij
- **Beklenen Aralık**: [0, 1] normalized by max possible roughness
- **Kaynak**: Literature/r3/psychoacoustics/Consonance&Dissonance_Part2.md — CDC-5 section; Pressnitzer_2000_ContMusRev.md — critical bandwidth section
- **Mevcut R³'te**: Kısmen (proxy: roughness [0] uses spectral variance instead)
- **Mel Uyumluluğu**: Dolaylı (needs spectral peak detection from mel, CB computation from center frequencies)

#### vassilakis_roughness
- **Kategori**: Consonance
- **Önerilen R³ Grubu**: A
- **Tanım**: Three-factor roughness model incorporating amplitude, frequency separation, and phase
- **Psikoakustik Temeli**: Vassilakis (2005) extension of Plomp-Levelt with amplitude weighting
- **Hesaplama Yöntemi**: `R = 0.5 * (Ai*Aj)^0.1 * (2*min(Ai,Aj)/(Ai+Aj))^3.11 * [exp(-3.5*s*Δf) - exp(-5.75*s*Δf)]` where s = 0.24/(0.0207*f_center + 18.96)
- **Beklenen Aralık**: [0, 1]
- **Kaynak**: Literature/r3/psychoacoustics/Consonance&Dissonance_Part2.md — Kameoka-Kuriyagawa section
- **Mevcut R³'te**: Yok
- **Mel Uyumluluğu**: Dolaylı (needs partial extraction)

#### sethares_dissonance_proper
- **Kategori**: Consonance
- **Önerilen R³ Grubu**: A
- **Tanım**: Timbre-dependent dissonance: total pairwise dissonance between all partials
- **Psikoakustik Temeli**: Sethares (1993) — dissonance depends on both frequency ratios AND timbral partial structure
- **Hesaplama Yöntemi**: Σ_{i≠j} a_i * a_j * [exp(-b1*s*|fi-fj|) - exp(-b2*s*|fi-fj|)] with s=d_max/(s1*min(fi,fj)+s2), b1=3.5, b2=5.75, d_max=0.24, s1=0.021, s2=19
- **Beklenen Aralık**: [0, 1]
- **Kaynak**: Literature/r3/psychoacoustics/Consonance&Dissonance_Part2.md
- **Mevcut R³'te**: Yok (sethares_dissonance [1] is misnamed spectral irregularity)
- **Mel Uyumluluğu**: Dolaylı (needs partial extraction)

#### harmonicity
- **Kategori**: Consonance
- **Önerilen R³ Grubu**: A
- **Tanım**: Degree to which spectral content matches a harmonic series template
- **Psikoakustik Temeli**: Periodicity detection in auditory brainstem; autocorrelation models (Licklider, Meddis & Hewitt)
- **Hesaplama Yöntemi**: Multi-lag autocorrelation of spectrum: `H = max_{τ>τ_min} R(τ) / R(0)` where R is autocorrelation
- **Beklenen Aralık**: [0, 1]
- **Kaynak**: Literature/r3/music-theory-analysis/harmony_perception_by_periodicity_detection.md; a_neurodynamic_account_of_musical_tonality.md
- **Mevcut R³'te**: Kısmen (helmholtz_kang [2] uses only lag-1)
- **Mel Uyumluluğu**: Dolaylı (multi-lag autocorrelation on mel spectrum feasible but coarser)

#### harmonic_distance
- **Kategori**: Consonance
- **Önerilen R³ Grubu**: A
- **Tanım**: Tenney harmonic distance — graduated consonance measure based on integer ratio complexity
- **Psikoakustik Temeli**: Simpler integer ratios are perceived as more consonant (Pythagoras through Helmholtz)
- **Hesaplama Yöntemi**: Detect interval ratio a:b via Stern-Brocot tree approximation (JND ~1%): `HD = log2(a*b)`
- **Beklenen Aralık**: [0, ~15] (unison=0, octave=1, fifth=2.58, tritone=~7)
- **Kaynak**: Literature/r3/psychoacoustics/Fundamental_Principles_of_Just_Intonatio_Part2.md — Tenney section
- **Mevcut R³'te**: Yok
- **Mel Uyumluluğu**: Dolaylı (needs pitch/interval detection)

#### tonal_fusion
- **Kategori**: Consonance
- **Önerilen R³ Grubu**: A
- **Tanım**: Perceptual merging of simultaneous tones into a single percept (Stumpf CDC-2)
- **Psikoakustik Temeli**: Stumpf's Tonverschmelzung; temporal autocorrelation coincidence at integer ratios
- **Hesaplama Yöntemi**: Subharmonic matching: count coinciding subharmonics weighted by harmonic number (Parncutt 1989)
- **Beklenen Aralık**: [0, 1]
- **Kaynak**: Literature/r3/music-theory-analysis/harmonic_fusion_and_pitch_affinity_is_there_a_direct_link.md
- **Mevcut R³'te**: Yok (stumpf_fusion [3] is misnamed low-freq energy ratio)
- **Mel Uyumluluğu**: Mümkün değil (needs fine temporal/spectral resolution beyond mel)

### 5.2 Pitch Features

#### chroma_vector
- **Kategori**: Pitch
- **Önerilen R³ Grubu**: F
- **Tanım**: 12-bin pitch class profile representing energy distribution across chroma classes
- **Psikoakustik Temeli**: Octave equivalence; pitch class perception (Shepard 1964); statistical learning of tonal hierarchies (Krumhansl 1990)
- **Hesaplama Yöntemi**: Fold mel bands into 12 chroma bins: assign each mel band to nearest semitone class, sum energies per class
- **Beklenen Aralık**: [0, 1] per bin (L1-normalized)
- **Kaynak**: Literature/r3/computational-music-theory/Balzano-GroupTheoreticDescription12Fold-1980.md; music-theory-analysis/perception_of_affect_in_unfamiliar_musical_chords.md
- **Mevcut R³'te**: Yok
- **Mel Uyumluluğu**: Dolaylı (mel-based chroma feasible but coarser than CQT chroma)

#### pitch_height
- **Kategori**: Pitch
- **Önerilen R³ Grubu**: F
- **Tanım**: Average perceived pitch height — spectral centroid mapped to log-frequency
- **Psikoakustik Temeli**: Weber-Fechner law; perceived pitch ~ log(frequency)
- **Hesaplama Yöntemi**: `PH = Σ(log(f_k) * M_k) / Σ M_k` where f_k are mel band center frequencies
- **Beklenen Aralık**: [0, 1] normalized to audible range
- **Kaynak**: Literature/r3/music-theory-analysis/Smit et al. (2019); Himpel (2022)
- **Mevcut R³'te**: Yok
- **Mel Uyumluluğu**: Doğrudan

#### virtual_pitch_salience
- **Kategori**: Pitch
- **Önerilen R³ Grubu**: F
- **Tanım**: Salience of the missing fundamental — strength of perceived pitch from harmonic series without f0
- **Psikoakustik Temeli**: Harmonic pattern recognition; Parncutt (1989) model
- **Hesaplama Yöntemi**: For each candidate f0: match mel peaks against template {f0, 2f0, 3f0...}; salience = Σ matched peak energies / expected pattern energy
- **Beklenen Aralık**: [0, 1]
- **Kaynak**: Literature/r3/music-theory-analysis/mp3604_05_parncutt_406430.md
- **Mevcut R³'te**: Yok
- **Mel Uyumluluğu**: Dolaylı (harmonic template matching on mel — feasible with sufficient bands)

### 5.3 Harmony Features

#### key_clarity
- **Kategori**: Harmony
- **Önerilen R³ Grubu**: H
- **Tanım**: Strength of tonal center — max correlation of chroma with Krumhansl-Kessler key profiles
- **Psikoakustik Temeli**: Tonal hierarchy perception (Krumhansl & Kessler 1982)
- **Hesaplama Yöntemi**: Compute chroma vector → correlate with 24 key profiles (12 major, 12 minor) → max correlation value
- **Beklenen Aralık**: [0, 1]
- **Kaynak**: Literature/r3/computational-music-theory/Tymoczko.md — centricity component
- **Mevcut R³'te**: Yok
- **Mel Uyumluluğu**: Dolaylı (via chroma extraction)

#### tonnetz_coordinates
- **Kategori**: Harmony
- **Önerilen R³ Grubu**: H
- **Tanım**: 6D tonal space coordinates encoding fifths, major thirds, minor thirds relationships
- **Psikoakustik Temeli**: Psychoacoustic triadic perception; Krumhansl & Kessler (1982) empirical proximity matches Tonnetz geometry
- **Hesaplama Yöntemi**: Harte (2006): from chroma vector c, compute 6 coordinates as weighted circular projections at intervals of 7, 4, 3 semitones
- **Beklenen Aralık**: [-1, 1] per dimension
- **Kaynak**: Literature/r3/computational-music-theory/Balzano-GroupTheoreticDescription12Fold-1980.md; music-theory-analysis/the_tonnetz_at_first_sight.md
- **Mevcut R³'te**: Yok
- **Mel Uyumluluğu**: Dolaylı (via chroma → 6D projection)

#### voice_leading_distance
- **Kategori**: Harmony
- **Önerilen R³ Grubu**: H
- **Tanım**: Minimal total pitch displacement between successive chord voicings
- **Psikoakustik Temeli**: Perceived harmonic similarity correlates with voice-leading parsimony (Tymoczko)
- **Hesaplama Yöntemi**: `d_VL = min_σ Σ|a_i - b_σ(i)|` (L1 norm over optimal voice assignment). Approximate from chroma: use chroma vector L1 distance.
- **Beklenen Aralık**: [0, 12] semitones
- **Kaynak**: Literature/r3/computational-music-theory/Geometry_of_Music_Part2.md; Rus_Geometry.md; music-theory-analysis/geometry_of_music_perception.md
- **Mevcut R³'te**: Yok
- **Mel Uyumluluğu**: Dolaylı (approximate from chroma vector distance)

#### pc_dft_magnitudes
- **Kategori**: Harmony
- **Önerilen R³ Grubu**: H
- **Tanım**: DFT magnitude coefficients of chroma vector — encode interval-class content
- **Psikoakustik Temeli**: Captures harmonic properties: T(5)=diatonicity, T(3)=triadicity, T(1)=chromaticity
- **Hesaplama Yöntemi**: `T(k) = |Σ_{c=0}^{11} chroma(c) * exp(2πi*k*c/12)|` for k=1..6
- **Beklenen Aralık**: [0, ~1] (L2-normalized)
- **Kaynak**: Literature/r3/music-theory-analysis/fluidharmony_defining_an_equal-tempered.md (Bernardes et al. 2022)
- **Mevcut R³'te**: Yok
- **Mel Uyumluluğu**: Dolaylı (via chroma → DFT)

### 5.4 Information Features

#### spectral_surprise
- **Kategori**: Information
- **Önerilen R³ Grubu**: I
- **Tanım**: Frame-level unexpectedness — KL divergence between current and running average spectral distribution
- **Psikoakustik Temeli**: Prediction error / surprise signal; free energy principle (Friston); neural mismatch negativity
- **Hesaplama Yöntemi**: `D_KL(p_t || p̄) = Σ p_t(k) * log(p_t(k) / p̄(k))` where p̄ is exponentially decaying average
- **Beklenen Aralık**: [0, ∞) typically [0, 5]; normalize by max
- **Kaynak**: Based on elife-neural_Part1.md (prediction error framework); perception_of_affect_in_unfamiliar_musical_chords.md
- **Mevcut R³'te**: Yok
- **Mel Uyumluluğu**: Doğrudan

#### information_rate
- **Kategori**: Information
- **Önerilen R³ Grubu**: I
- **Tanım**: Mutual information between consecutive frames — how much new information per frame
- **Psikoakustik Temeli**: Spectral flux is strongest neural sync driver (Weineck 2022); information rate captures similar concept in bits
- **Hesaplama Yöntemi**: `I(X_t; X_{t-1}) = H(X_t) + H(X_{t-1}) - H(X_t, X_{t-1})`
- **Beklenen Aralık**: [0, H_max] bits
- **Kaynak**: Literature/r3/psychoacoustics/elife-neural_Part1.md
- **Mevcut R³'te**: Yok
- **Mel Uyumluluğu**: Doğrudan

---

## 6. Computability Assessment (Mel → Feature Difficulty Ranking)

### Tier 1: Directly from Mel Spectrogram (no preprocessing)
| Feature | Computation Cost | Notes |
|---------|-----------------|-------|
| spectral_centroid | <0.1 ms/frame | Weighted mean |
| spectral_spread/skewness/kurtosis | <0.1 ms/frame | Central moments |
| spectral_entropy | <0.1 ms/frame | Histogram + log |
| spectral_flatness | <0.1 ms/frame | Geometric/arithmetic mean |
| spectral_flux (L1, L2) | <0.1 ms/frame | Frame difference |
| onset_strength | <0.1 ms/frame | HWR spectral flux |
| rms_amplitude | <0.1 ms/frame | sqrt(mean(x²)) |
| pitch_height | <0.1 ms/frame | Weighted log-freq mean |
| spectral_surprise (KL) | <0.5 ms/frame | Running average + KL |
| event_density | <0.1 ms/frame | Onset count |
| warmth/sharpness | <0.1 ms/frame | Band energy ratios |
| spectral_contrast | <0.5 ms/frame | Octave-band peak-valley |

### Tier 2: Via Chroma Extraction (mel → chroma → feature)
| Feature | Computation Cost | Notes |
|---------|-----------------|-------|
| chroma_vector (12D) | ~1 ms/frame | Mel-to-chroma folding |
| key_clarity | ~2 ms/frame | Chroma × 24 key profiles |
| tonnetz_coordinates (6D) | ~1 ms/frame | Chroma → 6D projection |
| chord_template_match | ~2 ms/frame | Chroma × chord templates |
| voice_leading_distance | ~1 ms/frame | Chroma cosine distance |
| harmonic_change | ~1 ms/frame | Frame chroma distance |
| pc_dft_magnitudes (6D) | ~1 ms/frame | FFT of 12-point chroma |
| diatonicity | ~1 ms/frame | PC count in window |
| chroma_surprise | ~1 ms/frame | Chroma KL divergence |
| tonal_ambiguity | ~2 ms/frame | Entropy of key correlations |

### Tier 3: Requires Spectral Peak Detection (mel → peaks → feature)
| Feature | Computation Cost | Notes |
|---------|-----------------|-------|
| plomp_levelt_roughness | ~5 ms/frame | Peak detection + pairwise CB comparison |
| vassilakis_roughness | ~5 ms/frame | Same + 3-factor weighting |
| sethares_dissonance | ~5 ms/frame | All-pairs partial dissonance |
| harmonicity (multi-lag) | ~3 ms/frame | Multi-lag autocorrelation |
| harmonic_distance | ~5 ms/frame | Interval ratio detection + Stern-Brocot |
| virtual_pitch_salience | ~5 ms/frame | Harmonic template search |
| inharmonicity_score | ~3 ms/frame | Peak deviation from harmonic series |
| spectral_complexity | ~2 ms/frame | Peak counting above noise floor |

### Tier 4: Requires External Model or Raw Audio
| Feature | Requirement | Notes |
|---------|-------------|-------|
| zwicker_loudness | Linear spectrum (not mel) | ISO 532-1 requires Bark-band specific loudness |
| tonal_fusion | Fine temporal resolution | Needs autocorrelation on waveform |
| combination_tones | Cochlear nonlinearity model | Not available from mel |
| melodic_information_content | Statistical model (IDyOM) | Requires trained pitch prediction model |
| syncopation_index | Beat tracking + metrical model | Requires external meter analysis |
| groove_factor | Precise onset timing | Needs sub-frame timing accuracy |
| vibrato_rate/extent | AM/FM demodulation | Feasible from mel envelope modulation |

---

## 7. Literature Reference Matrix

| File | Category | Features Found |
|------|----------|---------------|
| **psychoacoustics/Consonance&Dissonance_Part1.md** | Consonance | 5 CDC taxonomy: melodic affinity, tonal fusion, clarity, functional consonance, roughness |
| **psychoacoustics/Consonance&Dissonance_Part2.md** | Consonance | Plomp-Levelt roughness curve, Kameoka-Kuriyagawa dissonance, Sethares timbre-dependent model, Vassilakis 3-factor roughness |
| **psychoacoustics/Fundamental_Principles_Part1.md** | Consonance/Pitch | Cents formula, JND (~3Hz/<500Hz), combination tones, periodic signature |
| **psychoacoustics/Fundamental_Principles_Part2.md** | Consonance | Harmonic distance HD=log2(ab), harmonic intersection I=(a+b-1)/(ab), tuneable interval criteria |
| **psychoacoustics/Fundamental_Principles_Part3.md** | — | Score excerpts only (no features) |
| **psychoacoustics/Pressnitzer_2000_ContMusRev.md** | Consonance/Timbre | Critical bandwidth, roughness vs CB ratio, auditory scene analysis, masking, emergent attributes |
| **psychoacoustics/elife-neural_Part1.md** | Change/Energy | Spectral flux as strongest neural synchronization driver; TRF/SRCoh methods; 1-2Hz beat preference |
| **psychoacoustics/elife-neural_Part2.md** | — | Methods details (EEG preprocessing) |
| **psychoacoustics/ji_primer_ed3.md** | Consonance | Benade's special relationships; coincident harmonics; periodicity pitch |
| **psychoacoustics/JI-Terry.md** | — | JI mathematics (Pythagorean/syntonic comma); lattice/torus geometry |
| **psychoacoustics/Intonation_of_Harmonic_Intervals.md** | Consonance/Change | 4-factor intonation model; beat frequency as tuning cue; jitter; categorical perception boundaries (~50 cents) |
| **dsp-and-ml/CNN_Genre_Classification.md** | Timbre | MFCC (13D), mel spectrogram, spectral centroid, spectral rolloff, zero-crossing rate |
| **dsp-and-ml/Modulation_Classification.md** | Change/Rhythm | Modulation spectrum (AM at 4-16Hz); rhythmic modulation features; temporal envelope |
| **dsp-and-ml/Spectral_Contrast.md** | Timbre | Spectral contrast (octave-band peak-valley, 6D); MFCC comparison; OSFC features |
| **dsp-and-ml/Benetos_Turkish_Microtonal.md** | Pitch | Shift-invariant spectrogram factorization; instrument-specific spectral templates; 20-cent resolution microtonal transcription |
| **spectral-music/Anderson.md** | Timbre/Change | Harmonic/non-harmonic spectra; ring modulation products; rate of spectral change; timbral fusion |
| **spectral-music/Fineberg_Basics.md** | Pitch/Timbre | Partial frequency tracking; spectral envelope; formant structure; spectral filtering; frequency-to-pitch mapping |
| **spectral-music/Stanford-Spectral.md** | Timbre/Harmony | Partial structure as compositional material; spectral brightness evolution; harmonic vs. inharmonic continuum |
| **spectral-music/Chung-spectral.md** | Timbre | MFCC, SSD, RH, MVD, TSSD, TRH, AIM features; texture features from log-frequency spectrogram |
| **computational-music-theory/Tymoczko.md** | Harmony | 5 components of tonality: conjunct motion, consonance, harmonic consistency, macroharmony, centricity |
| **computational-music-theory/Balzano-1980.md** | Harmony/Pitch | C3×C4 thirds-space coordinates; circle-of-fifths position; diatonic set connectivity; scale coherence; transpositional overlap |
| **computational-music-theory/Geometry_Part1-5.md** | Harmony | Voice-leading distance; chord space (orbifold); pitch-class space; transposition/inversion as distance-preserving; near-evenness |
| **computational-music-theory/Neo-Riemannian_Part1-5.md** | Harmony | Tonnetz coordinates; P/L/R operations; parsimony; hexatonic/octatonic system membership |
| **computational-music-theory/Lewin.md** | — | GIS framework (abstract); interval function int(x,y) (algebraic, not directly computable from audio) |
| **computational-music-theory/Julian Hook.md** | Harmony | Cross-type transformations; GIS homomorphism (framework, limited direct audio applicability) |
| **music-theory-analysis/harmony_perception_by_periodicity.md** | Consonance | Periodicity detection model; Stern-Brocot tree for ratio approximation; logarithmic periodicity for chords |
| **music-theory-analysis/a_neurodynamic_account.md** | Harmony | Mode-locking stability: ε^((k+m-2)/2); coupled oscillator model; Farey ratio table for all 12 intervals |
| **music-theory-analysis/simultaneous_consonance.md** | Consonance | Three-component model: roughness + harmonicity + familiarity; Harrison & Pearce (2020) `incon` R package |
| **music-theory-analysis/perception_of_affect.md** | Information/Harmony | Spectral entropy, roughness, harmonicity predict chord affect; Bohlen-Pierce scale learning |
| **music-theory-analysis/fluidharmony.md** | Harmony | DFT of pitch-class sets: T(1)..T(6) magnitudes and phases; tonal index; L2-normalized comparison |
| **music-theory-analysis/the_tonnetz_at_first_sight.md** | Harmony | Tonnetz as cognitive interface; hexagonal representation; pitch-class proximity |
| **music-theory-analysis/geometry_of_music_perception.md** | Harmony | Whitney stratified chord space; roughness/harmonicity as height functions; gradient vectors as tension/release |
| **music-theory-analysis/thinking_about_musical_time.md** | Rhythm | Hierarchical temporal nesting; multi-scale time strata; qualitative temporal categories |
| **music-theory-analysis/consonance_critical_review.md** | Consonance | Historical survey of consonance theories; 5 CDC framework validation |

---

## 8. Open Questions for Chat R3 (Web Research)

### 8.1 Computation Methods Needing Web Verification

1. **Mel-based chroma extraction accuracy:** How does mel-to-chroma folding compare to CQT-based chroma (librosa `chroma_cqt`) for key detection and chord recognition? What is the quality loss?

2. **Real-time Plomp-Levelt from mel:** Has anyone implemented Plomp-Levelt roughness from mel spectrogram (rather than linear FFT)? What resolution is needed?

3. **Tonnetz from chroma — Harte (2006) exact formulas:** The 6D Tonnetz projection from chroma is described in Harte's PhD thesis. What are the exact sine/cosine weights?

4. **IDyOM approximation:** Can IDyOM-style melodic/harmonic information content be approximated without the full IDyOM model? Any simplified versions?

### 8.2 Specific Feature Implementations Needed

5. **Syncopation index (Witek et al. 2014):** Exact algorithm for computing syncopation from onset pattern + metrical grid?

6. **Groove features (Madison 2006, Janata 2012):** How are groove features operationalized computationally?

7. **Lerdahl harmonic tension (2001):** Herremans (2017) computational implementation — what inputs does it need? Can it work from chroma?

8. **Spectral contrast (Jiang 2002):** librosa implementation details — octave band boundaries, peak/valley detection specifics?

### 8.3 Toolkit Comparisons

9. **librosa vs essentia feature sets:** Which features from each toolkit are most relevant for R³ expansion? What's their mel compatibility?

10. **openSMILE eGeMAPS features:** Which of the 88 eGeMAPS features overlap with or extend R³?

11. **CREPE/pYIN pitch accuracy from mel:** Can neural pitch estimators (CREPE) work from mel spectrogram input rather than raw audio?

### 8.4 Architecture Decisions

12. **Target dimensionality:** 128D, 192D, or 256D? What is the computational cost tradeoff at 172 Hz frame rate?

13. **Fixed vs. learned interactions:** Should Group E be replaced with a learned MLP? What are the training considerations?

14. **Backward compatibility:** If existing 49D indices change, what is the migration strategy for 96 C³ model documents?

### 8.5 Standards

15. **ISO 532-1/2:** Zwicker vs Moore-Glasberg loudness — which is more appropriate for music? Implementation availability?

16. **AES/ITU standards:** Which audio measurement standards (AES17, ITU-R BS.1770) provide features relevant to R³?

---

## Appendix A: Proposed Dimensionality Summary

| Group | Current D | Proposed D | Independent Gain |
|-------|-----------|------------|-----------------|
| A: Consonance | 7 | 10–12 | +7 (remove 4 redundant, add 10 new) |
| B: Energy | 5 | 7 | +2 |
| C: Timbre | 9 | 10 | +3 (remove 3 duplicates, add 6 new) |
| D: Change | 4 | 8 | +6 |
| E: Interactions | 24 | 16–24 | Redesign (fix proxies) |
| **F: Pitch** | **0** | **16–18** | **+16** (entirely new) |
| **G: Rhythm** | **0** | **8–12** | **+8** (entirely new) |
| **H: Harmony** | **0** | **12–18** | **+12** (entirely new) |
| **I: Information** | **0** | **8–12** | **+8** (entirely new) |
| **Total** | **49** | **95–141** | **+62 to +92 new independent D** |

**Recommended target: 128D** — achievable with conservative selections from each group, leaving room for Phase 3B design decisions.

---

## Appendix B: Cross-Reference with R³ Gap Logs

| Gap Log | Top Requested Category | Proposed Solution |
|---------|----------------------|-------------------|
| R3-GAP-LOG-IMU.md (13 gaps) | Pitch, Harmony, Information | Groups F, H, I |
| R3-GAP-LOG-ASU.md (8 gaps) | Salience, Surprise | Group I (spectral_surprise, information_rate) |
| R3-GAP-LOG-PCU.md (9 gaps) | Prediction, Harmony | Groups H, I (predictive_entropy, harmonic_surprisal) |
| R3-GAP-LOG-RPU.md (5 gaps) | Reward-related | Groups H (harmonic_tension), I (surprise) |
| R3-GAP-LOG-MPU.md (7 gaps) | Rhythm, Motor | Group G (tempo, beat, syncopation) |
| R3-GAP-LOG-NDU.md (5 gaps) | Novelty, Surprise | Group I (spectral_surprise, self_information) |
| R3-GAP-LOG-ARU.md (0 gaps) | — | Fully covered |

---

*Generated by Phase 3A-2 Chat R2 | 2026-02-13*
*Sources: 121 markdown files from Literature/r3/, 5 code files from mi_beta/ear/r3/*
