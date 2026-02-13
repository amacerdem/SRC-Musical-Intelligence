# R3 Literature Cross-Reference -- 128 Features

> **Scope**: All 128 R3 v2 features with literature grounding
> **Sources**: R3-DSP-SURVEY-THEORY.md Section 7, R3-DSP-SURVEY-TOOLS.md Section 8
> **Created**: 2026-02-13

---

## Reading Guide

Each feature is listed with:
- **Index**: Position in the 128D R3 vector
- **Feature Name**: Canonical name from R3-CROSSREF.md Section 4
- **Primary Paper**: The foundational psychoacoustic or DSP reference
- **DSP Reference**: Implementation source (library API or algorithm)
- **Local File**: Path within `Literature/r3/` if available

---

## Group A: Consonance [0:7] -- 7D (EXISTING)

| Index | Feature Name | Primary Paper | DSP Reference | Local File |
|:-----:|-------------|--------------|---------------|------------|
| 0 | roughness | Plomp & Levelt (1965) "Tonal consonance and critical bandwidth" | `mi_beta/ear/r3/psychoacoustic/consonance.py` -- sigmoid(spectral_var/mean). PROXY: not true Plomp-Levelt pairwise roughness. | `psychoacoustics/Consonance&Dissonance_Part2.md` |
| 1 | sethares_dissonance | Sethares (1993) "Local consonance and the relationship between timbre and scale" | `mi_beta/ear/r3/psychoacoustic/consonance.py` -- mean abs adjacent mel diff. PROXY: not true Sethares pairwise dissonance. | `psychoacoustics/Consonance&Dissonance_Part2.md` |
| 2 | helmholtz_kang | Terhardt (1979) "Calculating virtual pitch"; Helmholtz (1863) | `mi_beta/ear/r3/psychoacoustic/consonance.py` -- lag-1 spectral autocorrelation | `music-theory-analysis/harmony_perception_by_periodicity_detection.md` |
| 3 | stumpf_fusion | Stumpf (1898) "Konsonanz und Dissonanz"; Parncutt (1989) | `mi_beta/ear/r3/psychoacoustic/consonance.py` -- low-quarter energy ratio. PROXY: identical to warmth [12]. | `music-theory-analysis/simultaneous_consonance_in_music_perception_and_composition.md` |
| 4 | sensory_pleasantness | Harrison & Pearce (2020) "Simultaneous consonance in music perception" | `mi_beta/ear/r3/psychoacoustic/consonance.py` -- 0.6*(1-[1]) + 0.4*[3]. Derived linear combination. | `music-theory-analysis/simultaneous_consonance_in_music_perception_and_composition.md` |
| 5 | inharmonicity | Terhardt (1979); Norman-Haignere (2013) | `mi_beta/ear/r3/psychoacoustic/consonance.py` -- 1 - helmholtz_kang [2]. Complement of [2]. | `music-theory-analysis/harmony_perception_by_periodicity_detection.md` |
| 6 | harmonic_deviation | Krimphoff et al. (1994) spectral irregularity | `mi_beta/ear/r3/psychoacoustic/consonance.py` -- 0.5*[1] + 0.5*(1-[2]). Derived. | -- |

---

## Group B: Energy [7:12] -- 5D (EXISTING)

| Index | Feature Name | Primary Paper | DSP Reference | Local File |
|:-----:|-------------|--------------|---------------|------------|
| 7 | amplitude | Standard DSP (RMS) | `mi_beta/ear/r3/dsp/energy.py` -- RMS of mel bins, max-normalized | -- |
| 8 | velocity_A | Standard (energy derivative) | `mi_beta/ear/r3/dsp/energy.py` -- sigmoid(d(amp)/dt * 5) | -- |
| 9 | acceleration_A | Standard (energy 2nd derivative) | `mi_beta/ear/r3/dsp/energy.py` -- sigmoid(d2(amp)/dt2 * 5) | -- |
| 10 | loudness | Stevens (1957) "On the psychophysical law" | `mi_beta/ear/r3/dsp/energy.py` -- amplitude^0.3. BUG: double compression on log-mel. | `psychoacoustics/Pressnitzer_2000_ContMusRev.md` |
| 11 | onset_strength | Bello et al. (2005) "A tutorial on onset detection"; Weineck et al. (2022) | `mi_beta/ear/r3/dsp/energy.py` -- HWR spectral flux. Most validated feature. | `psychoacoustics/elife-neural_Part1.md` |

---

## Group C: Timbre [12:21] -- 9D (EXISTING)

| Index | Feature Name | Primary Paper | DSP Reference | Local File |
|:-----:|-------------|--------------|---------------|------------|
| 12 | warmth | Alluri & Toiviainen (2010) | `mi_beta/ear/r3/dsp/timbre.py` -- low-quarter energy ratio. NOTE: identical to [3]. | -- |
| 13 | sharpness | DIN 45692 (Zwicker sharpness, conceptual) | `mi_beta/ear/r3/dsp/timbre.py` -- high-quarter energy ratio. PROXY: not true Zwicker weighting. | `psychoacoustics/Pressnitzer_2000_ContMusRev.md` |
| 14 | tonalness | Terhardt (1979); Aures (1985) | `mi_beta/ear/r3/dsp/timbre.py` -- max(mel)/sum(mel). PROXY: single peak dominance. | -- |
| 15 | clarity | Standard MIR (spectral centroid) | `mi_beta/ear/r3/dsp/timbre.py` -- spectral_centroid / N. Mislabeled: "clarity" is C80 in acoustics. | -- |
| 16 | spectral_smoothness | Krimphoff et al. (1994) spectral irregularity | `mi_beta/ear/r3/dsp/timbre.py` -- 1 - spectral_irregularity. NOTE: complement of [1]. | -- |
| 17 | spectral_autocorrelation | Terhardt (1979) | `mi_beta/ear/r3/dsp/timbre.py` -- lag-1 autocorrelation. NOTE: identical to [2]. | -- |
| 18 | tristimulus1 | Pollard & Jansson (1982) | `mi_beta/ear/r3/dsp/timbre.py` -- bottom-third energy ratio. Mel-band proxy for partial-based tristimulus. | -- |
| 19 | tristimulus2 | Pollard & Jansson (1982) | `mi_beta/ear/r3/dsp/timbre.py` -- middle-third energy ratio | -- |
| 20 | tristimulus3 | Pollard & Jansson (1982) | `mi_beta/ear/r3/dsp/timbre.py` -- top-third energy ratio | -- |

---

## Group D: Change [21:25] -- 4D (EXISTING)

| Index | Feature Name | Primary Paper | DSP Reference | Local File |
|:-----:|-------------|--------------|---------------|------------|
| 21 | spectral_flux | Standard MIR; Bello et al. (2005) | `mi_beta/ear/r3/dsp/change.py` -- L2 full-spectrum flux, max-normalized | -- |
| 22 | distribution_entropy | Shannon (1948) "A mathematical theory of communication" | `mi_beta/ear/r3/dsp/change.py` -- Shannon entropy / log(N) | -- |
| 23 | distribution_flatness | MPEG-7 (Wiener entropy) | `mi_beta/ear/r3/dsp/change.py` -- geometric/arithmetic mean | -- |
| 24 | distribution_concentration | Herfindahl-Hirschman Index | `mi_beta/ear/r3/dsp/change.py` -- HHI * N. BUG: normalization destroys discrimination. | -- |

---

## Group E: Interactions [25:49] -- 24D (EXISTING)

| Index | Feature Name | Primary Paper | DSP Reference | Local File |
|:-----:|-------------|--------------|---------------|------------|
| 25 | x_amp_roughness | Cross-domain interaction (Energy x Consonance) | `mi_beta/ear/r3/cross_domain/interactions.py` -- element-wise product | -- |
| 26 | x_amp_sethares | " | " | -- |
| 27 | x_amp_helmholtz | " | " | -- |
| 28 | x_amp_stumpf | " | " | -- |
| 29 | x_vel_roughness | " | " | -- |
| 30 | x_vel_sethares | " | " | -- |
| 31 | x_vel_helmholtz | " | " | -- |
| 32 | x_vel_stumpf | " | " | -- |
| 33 | x_flux_roughness | Cross-domain interaction (Change x Consonance) | " | -- |
| 34 | x_flux_sethares | " | " | -- |
| 35 | x_flux_helmholtz | " | " | -- |
| 36 | x_flux_stumpf | " | " | -- |
| 37 | x_ent_roughness | " | " | -- |
| 38 | x_ent_sethares | " | " | -- |
| 39 | x_ent_helmholtz | " | " | -- |
| 40 | x_ent_stumpf | " | " | -- |
| 41 | x_rough_warmth | Cross-domain interaction (Consonance x Timbre) | " | -- |
| 42 | x_rough_sharp | " | " | -- |
| 43 | x_rough_tonal | " | " | -- |
| 44 | x_rough_autocorr | " | " | -- |
| 45 | x_stumpf_warmth | " | " | -- |
| 46 | x_stumpf_sharp | " | " | -- |
| 47 | x_stumpf_tonal | " | " | -- |
| 48 | x_stumpf_autocorr | " | " | -- |

**Note**: E group uses independently computed proxy features, not actual A-D outputs. Two proxy mismatches documented in R3-CROSSREF.md Section 5.4. Phase 6 will fix proxies and expand interactions to include new F-K groups.

---

## Group F: Pitch & Chroma [49:65] -- 16D (NEW)

| Index | Feature Name | Primary Paper | DSP Reference | Local File |
|:-----:|-------------|--------------|---------------|------------|
| 49 | chroma_C | Shepard (1964) "Circularity in judgments of relative pitch"; Krumhansl (1990) | mel -> freq mapping -> pitch class 0 fold -> L1 norm. See R3-DSP-SURVEY-TOOLS Appendix B. | `computational-music-theory/Balzano-GroupTheoreticDescription12Fold-1980.md` |
| 50 | chroma_Db | " | pitch class 1 | " |
| 51 | chroma_D | " | pitch class 2 | " |
| 52 | chroma_Eb | " | pitch class 3 | " |
| 53 | chroma_E | " | pitch class 4 | " |
| 54 | chroma_F | " | pitch class 5 | " |
| 55 | chroma_Gb | " | pitch class 6 | " |
| 56 | chroma_G | " | pitch class 7 | " |
| 57 | chroma_Ab | " | pitch class 8 | " |
| 58 | chroma_A | " | pitch class 9 | " |
| 59 | chroma_Bb | " | pitch class 10 | " |
| 60 | chroma_B | " | pitch class 11 | " |
| 61 | pitch_height | Weber-Fechner law; Stevens (1957) | Weighted mean log-frequency: sum(log(f_k) * M_k) / sum(M_k), normalized [0,1] | -- |
| 62 | pitch_class_entropy | Shannon (1948); standard pitch-class analysis | H = -sum(chroma_c * log(chroma_c)) / log(12). High = chromatic, low = tonal. | -- |
| 63 | pitch_salience | Parncutt (1989) "Harmony: A Psychoacoustical Approach" | max(mel) prominence / surrounding noise floor ratio. Proxy for harmonic resolvability. | `music-theory-analysis/mp3604_05_parncutt_406430.md` |
| 64 | inharmonicity_index | Standard; Stanford spectral music theory | Spectral peak deviation from nearest harmonic series: sum(|f_k - k*f_0|/(k*f_0)) | `spectral-music/Stanford-Spectral.md` |

---

## Group G: Rhythm & Groove [65:75] -- 10D (NEW)

| Index | Feature Name | Primary Paper | DSP Reference | Local File |
|:-----:|-------------|--------------|---------------|------------|
| 65 | tempo_estimate | Fraisse (1982) "Rhythm and tempo"; standard MIR | Onset strength autocorrelation -> dominant period -> BPM, normalized [0,1] (30-300 BPM). librosa: `beat.tempo(onset_envelope=oenv)` | -- |
| 66 | beat_strength | Standard MIR (autocorrelation peak) | Autocorrelation peak value at estimated tempo period. librosa: `feature.tempogram` peak extraction. | -- |
| 67 | pulse_clarity | Standard MIR | Autocorrelation peak / noise floor ratio. librosa: `beat.plp(onset_envelope=oenv)` | -- |
| 68 | syncopation_index | Witek et al. (2014) "Effects of high-level musical features on body movement"; Longuet-Higgins & Lee (1984) | LHL: onset accent at off-beat positions relative to metrical grid. Requires beat tracking + metrical grid. | -- |
| 69 | metricality_index | Grahn & Brett (2007) "Rhythm and beat perception in motor areas of the brain" | Multi-scale autocorrelation: count of nested integer-ratio pulse levels detected. | -- |
| 70 | isochrony_nPVI | Ravignani (2021) "Isochrony, the neural metronome"; Burchardt et al. (2025) | nPVI = 100 * mean(|IOI_k - IOI_{k+1}| / mean(IOI_k, IOI_{k+1})) from onset times | -- |
| 71 | groove_index | Madison (2006); Janata et al. (2012) "Sensorimotor coupling in music and the psychology of the groove" | Composite: syncopation x bass_energy x pulse_clarity -> movement-inducing quality | -- |
| 72 | event_density | Standard MIR (onset rate) | Count of onsets per second, normalized. essentia: `OnsetRate` | -- |
| 73 | tempo_stability | Standard MIR | Variance of local tempo estimates over sliding window, inverted. High = stable. | -- |
| 74 | rhythmic_regularity | Standard information theory | 1 - entropy(IOI distribution). High = regular, low = irregular. Inverse proxy for rhythmic entropy. | -- |

---

## Group H: Harmony & Tonality [75:87] -- 12D (NEW)

| Index | Feature Name | Primary Paper | DSP Reference | Local File |
|:-----:|-------------|--------------|---------------|------------|
| 75 | key_clarity | Krumhansl & Kessler (1982) "Tracing the dynamic changes in perceived tonal organization"; Krumhansl (1990) | max(corr(chroma, 24_key_profiles)). Krumhansl-Schmuckler algorithm. librosa: via chroma + key template correlation. | `music-theory-analysis/perception_of_affect_in_unfamiliar_musical_chords.md` |
| 76 | tonnetz_fifth_x | Harte (2006) PhD thesis; Balzano (1980) | sum(chroma_c * sin(c*7*pi/6)). 6D tonal centroid. librosa: `feature.tonnetz(chroma=chroma_approx)` | `computational-music-theory/Balzano-GroupTheoreticDescription12Fold-1980.md`; `music-theory-analysis/the_tonnetz_at_first_sight.md` |
| 77 | tonnetz_fifth_y | Harte (2006); Balzano (1980) | sum(chroma_c * cos(c*7*pi/6)) | " |
| 78 | tonnetz_minor_x | Harte (2006) | sum(chroma_c * sin(c*3*pi/6)). Minor-third relations. | " |
| 79 | tonnetz_minor_y | Harte (2006) | sum(chroma_c * cos(c*3*pi/6)) | " |
| 80 | tonnetz_major_x | Harte (2006) | sum(chroma_c * sin(c*4*pi/6)). Major-third relations. | " |
| 81 | tonnetz_major_y | Harte (2006) | sum(chroma_c * cos(c*4*pi/6)) | " |
| 82 | voice_leading_distance | Tymoczko "A Geometry of Music" | L1 norm: sum(|chroma_t - chroma_{t-1}|). Approximate voice-leading parsimony. | `computational-music-theory/Geometry_of_Music_Part2.md` |
| 83 | harmonic_change | Standard MIR (chroma cosine distance) | 1 - cosine(chroma_t, chroma_{t-1}). Frame-to-frame harmonic shift. | -- |
| 84 | tonal_stability | Krumhansl & Kessler (1982) | 1 / (1 + harmonic_change_rate + (1 - key_clarity)), normalized. High = stable tonal center. | -- |
| 85 | diatonicity | Tymoczko "macroharmony" concept | Count of distinct PCs with energy > threshold in window / 12. Low = diatonic. | `computational-music-theory/Tymoczko.md` |
| 86 | syntactic_irregularity | Lerdahl (2001) "Tonal Pitch Space"; Kim (2021) MEG study | KL divergence of current chroma from diatonic key template. Harmonic syntax violation. | -- |

---

## Group I: Information & Surprise [87:94] -- 7D (NEW)

| Index | Feature Name | Primary Paper | DSP Reference | Local File |
|:-----:|-------------|--------------|---------------|------------|
| 87 | melodic_entropy | Pearce (2005/2018) "Statistical learning and expectation generation in auditory cognition"; Gold et al. (2019) | Entropy of frame-to-frame chroma transition distribution over sliding window. Approximates IDyOM melodic IC. | -- |
| 88 | harmonic_entropy | Gold et al. (2019) "Predictability and uncertainty in the pleasure of music"; Cheung et al. (2019) | KL divergence of current chroma from running chroma average. Chord-level unexpectedness. | -- |
| 89 | rhythmic_information_content | Spiech et al. (2022); Gold et al. (2019) | -log(p(IOI_current | IOI_context)) from onset interval statistics. Rhythmic surprise. | -- |
| 90 | spectral_surprise | Friston (free energy principle); standard information theory | D_KL(mel_t || mel_running_avg). Frame-level spectral unexpectedness. | `psychoacoustics/elife-neural_Part1.md` |
| 91 | information_rate | Weineck et al. (2022) (spectral flux as neural sync driver); Shannon MI | I(mel_t; mel_{t-1}) = H(mel_t) + H(mel_{t-1}) - H(mel_t, mel_{t-1}). Mutual information between consecutive frames. | `psychoacoustics/elife-neural_Part1.md` |
| 92 | predictive_entropy | Cheung et al. (2019); Gold et al. (2023) | Entropy of conditional distribution p(frame_t | context) from running statistics. High = unpredictable. | -- |
| 93 | tonal_ambiguity | Kim (2021) MEG F(2,36)=12.373; standard tonal analysis | Entropy of key profile correlation softmax: H = -sum(p_key * log(p_key)). High = ambiguous tonality. | -- |

---

## Group J: Timbre Extended [94:114] -- 20D (NEW)

| Index | Feature Name | Primary Paper | DSP Reference | Local File |
|:-----:|-------------|--------------|---------------|------------|
| 94 | mfcc_1 | Davis & Mermelstein (1980) "Comparison of parametric representations for monosyllabic word recognition" | DCT of log-mel: coefficient 1. librosa: `feature.mfcc(S=log_mel, n_mfcc=13)` | `dsp-and-ml/CNN_Genre_Classification.md` |
| 95 | mfcc_2 | " | coefficient 2 | " |
| 96 | mfcc_3 | " | coefficient 3 | " |
| 97 | mfcc_4 | " | coefficient 4 | " |
| 98 | mfcc_5 | " | coefficient 5 | " |
| 99 | mfcc_6 | " | coefficient 6 | " |
| 100 | mfcc_7 | " | coefficient 7 | " |
| 101 | mfcc_8 | " | coefficient 8 | " |
| 102 | mfcc_9 | " | coefficient 9 | " |
| 103 | mfcc_10 | " | coefficient 10 | " |
| 104 | mfcc_11 | " | coefficient 11 | " |
| 105 | mfcc_12 | " | coefficient 12 | " |
| 106 | mfcc_13 | " | coefficient 13 | " |
| 107 | spectral_contrast_1 | Jiang et al. (2002) "Music type classification by spectral contrast feature" | librosa: `feature.spectral_contrast(S=mel_power, n_bands=6)` -- octave sub-band 1 peak-valley | `dsp-and-ml/Music_type_classification_by_spectral_contrast_fea.md` |
| 108 | spectral_contrast_2 | " | sub-band 2 | " |
| 109 | spectral_contrast_3 | " | sub-band 3 | " |
| 110 | spectral_contrast_4 | " | sub-band 4 | " |
| 111 | spectral_contrast_5 | " | sub-band 5 | " |
| 112 | spectral_contrast_6 | " | sub-band 6 | " |
| 113 | spectral_contrast_7 | " | sub-band 7 (residual) | " |

---

## Group K: Modulation & Psychoacoustic [114:128] -- 14D (NEW)

| Index | Feature Name | Primary Paper | DSP Reference | Local File |
|:-----:|-------------|--------------|---------------|------------|
| 114 | modulation_0_5Hz | Chi, Ru & Shamma (2005) "Multiresolution spectrotemporal analysis of complex sounds" | Per-band FFT of mel temporal envelope -> energy at 0.5 Hz AM rate. ~2s sliding window required. | `dsp-and-ml/Automatic_Music_Genre_Classification_Based_on_Modu.md` |
| 115 | modulation_1Hz | " | energy at 1 Hz. Phrase-level rhythmic modulation. | " |
| 116 | modulation_2Hz | " | energy at 2 Hz. Beat-rate modulation. | " |
| 117 | modulation_4Hz | " | energy at 4 Hz. Speech syllabic rate / strong beat. | " |
| 118 | modulation_8Hz | " | energy at 8 Hz. Rapid articulation / tremolo. | " |
| 119 | modulation_16Hz | " | energy at 16 Hz. Roughness boundary / vibrato upper limit. | " |
| 120 | modulation_centroid | Derived from Chi/Shamma model | Weighted mean of modulation spectrum. Dominant modulation rate. | -- |
| 121 | modulation_bandwidth | Derived from Chi/Shamma model | Standard deviation of modulation spectrum. Modulation rate diversity. | -- |
| 122 | sharpness_zwicker | Zwicker & Fastl (1999) "Psychoacoustics: Facts and Models"; DIN 45692 | S = 0.11 * integral(N'(z)*g(z)*z dz) / integral(N'(z) dz) on Bark scale. Requires mel-to-Bark rebinning. | `psychoacoustics/Pressnitzer_2000_ContMusRev.md` |
| 123 | fluctuation_strength | Zwicker & Fastl (1999) | Temporal modulation at ~4 Hz: mel envelope band-pass -> amplitude. Peak at 4 Hz. | `psychoacoustics/Pressnitzer_2000_ContMusRev.md` |
| 124 | loudness_a_weighted | ISO 226:2003 "Equal-loudness contours"; Fletcher & Munson (1933) | A-weighting curve applied to mel bands -> total weighted energy. | -- |
| 125 | alpha_ratio | Eyben et al. (2015) eGeMAPS | Low-band (0-1kHz) / high-band (1k-5kHz) energy ratio on mel. | -- |
| 126 | hammarberg_index | Eyben et al. (2015) eGeMAPS; Hammarberg et al. (1980) | Peak energy ratio 0-2kHz / 2k-5kHz on mel. Spectral tilt measure. | -- |
| 127 | spectral_slope_0_500 | Eyben et al. (2015) eGeMAPS | Linear regression slope of mel bands in 0-500 Hz range. Low-frequency spectral envelope shape. | -- |

---

## Summary Statistics

| Group | Range | Dim | Status | Primary Lit. Sources | Local Files |
|-------|-------|:---:|--------|---------------------|:-----------:|
| A: Consonance | [0:7] | 7 | Existing | Plomp-Levelt, Sethares, Terhardt, Stumpf, Harrison-Pearce | 4 |
| B: Energy | [7:12] | 5 | Existing | Stevens, Bello, Weineck | 2 |
| C: Timbre | [12:21] | 9 | Existing | Zwicker, Pollard-Jansson, Krimphoff, Alluri-Toiviainen | 1 |
| D: Change | [21:25] | 4 | Existing | Shannon, MPEG-7, Bello | 0 |
| E: Interactions | [25:49] | 24 | Existing | Cross-domain products (no single primary reference) | 0 |
| F: Pitch & Chroma | [49:65] | 16 | New | Shepard, Krumhansl, Parncutt, Balzano | 3 |
| G: Rhythm & Groove | [65:75] | 10 | New | Witek, Grahn-Brett, Madison, Janata, Ravignani | 0 |
| H: Harmony & Tonality | [75:87] | 12 | New | Krumhansl-Kessler, Harte, Tymoczko, Lerdahl | 4 |
| I: Information & Surprise | [87:94] | 7 | New | Pearce, Gold, Cheung, Shannon, Friston | 2 |
| J: Timbre Extended | [94:114] | 20 | New | Davis-Mermelstein, Jiang | 2 |
| K: Modulation & Psychoacoustic | [114:128] | 14 | New | Chi-Shamma, Zwicker-Fastl, ISO 226, eGeMAPS | 2 |
| **Total** | **[0:128]** | **128** | | | **20** |

---

## Key Papers -- Full Citation List

| # | Author(s) | Year | Title | Relevance |
|---|-----------|------|-------|-----------|
| 1 | Plomp, R. & Levelt, W.J.M. | 1965 | Tonal consonance and critical bandwidth | A: roughness within critical bands |
| 2 | Sethares, W.A. | 1993 | Local consonance and the relationship between timbre and scale | A: timbre-dependent dissonance |
| 3 | Shepard, R.N. | 1964 | Circularity in judgments of relative pitch | F: octave equivalence / chroma |
| 4 | Harte, C. | 2006 | Towards automatic extraction of harmony information from music signals (PhD) | H: 6D Tonnetz from chroma |
| 5 | Witek, M.A.G. et al. | 2014 | Effects of polyphonic context, instrumentation, and metrical location on syncopation | G: syncopation and groove |
| 6 | Pearce, M.T. | 2005 | The construction and evaluation of statistical models of melodic structure (PhD) | I: IDyOM / melodic entropy |
| 7 | Krumhansl, C.L. | 1990 | Cognitive Foundations of Musical Pitch | F/H: tonal hierarchy, key profiles |
| 8 | Chi, T., Ru, P. & Shamma, S.A. | 2005 | Multiresolution spectrotemporal analysis of complex sounds | K: modulation spectrum |
| 9 | Zwicker, E. & Fastl, H. | 1999 | Psychoacoustics: Facts and Models (3rd ed.) | K: loudness, sharpness, fluctuation, roughness |
| 10 | Jiang, D.-N. et al. | 2002 | Music type classification by spectral contrast feature | J: spectral contrast |
| 11 | Stevens, S.S. | 1957 | On the psychophysical law | B: loudness power law |
| 12 | Terhardt, E. | 1979 | Calculating virtual pitch | A/C: harmonicity, tonalness |
| 13 | Parncutt, R. | 1989 | Harmony: A Psychoacoustical Approach | A/F: virtual pitch, tonal fusion |
| 14 | Tymoczko, D. | 2011 | A Geometry of Music | H: voice-leading distance, macroharmony |
| 15 | Lerdahl, F. | 2001 | Tonal Pitch Space | H: harmonic tension hierarchy |
| 16 | Balzano, G.J. | 1980 | The group-theoretic description of 12-fold and microtonal pitch systems | F/H: circle of fifths, thirds-space |
| 17 | Krumhansl, C.L. & Kessler, E.J. | 1982 | Tracing the dynamic changes in perceived tonal organization | H: key profiles, tonal hierarchy |
| 18 | Harrison, P.M.C. & Pearce, M.T. | 2020 | Simultaneous consonance in music perception and composition | A: composite consonance model |
| 19 | Grahn, J.A. & Brett, M. | 2007 | Rhythm and beat perception in motor areas of the brain | G: metricality |
| 20 | Madison, G. | 2006 | Experiencing groove induced by music | G: groove features |
| 21 | Janata, P. et al. | 2012 | Sensorimotor coupling in music and the psychology of the groove | G: groove-sensorimotor |
| 22 | Ravignani, A. | 2021 | Isochrony, the neural metronome, and the evolution of speech | G: nPVI, rhythmic regularity |
| 23 | Gold, B.P. et al. | 2019 | Predictability and uncertainty in the pleasure of music | I: melodic/harmonic entropy |
| 24 | Cheung, V.K.M. et al. | 2019 | Uncertainty and surprise jointly predict musical pleasure and amygdala activation | I: prediction error, reward |
| 25 | Shannon, C.E. | 1948 | A mathematical theory of communication | D/I: entropy, information theory |
| 26 | Bello, J.P. et al. | 2005 | A tutorial on onset detection in music signals | B/D: onset strength, spectral flux |
| 27 | Weineck, K. et al. | 2022 | Neural synchronization is strongest to the spectral flux of slow music | B: onset strength validation |
| 28 | Pressnitzer, D. & McAdams, S. | 2000 | Acoustics, psychoacoustics, and spectral music (Contemporary Music Review) | A/C/K: critical bandwidth, roughness, masking |
| 29 | Davis, S.B. & Mermelstein, P. | 1980 | Comparison of parametric representations for monosyllabic word recognition | J: MFCC origin |
| 30 | Eyben, F. et al. | 2015 | The Geneva Minimalistic Acoustic Parameter Set (GeMAPS) | K: alpha_ratio, hammarberg, slopes |
| 31 | Vassilakis, P.N. | 2005 | Auditory roughness as a means of musical expression | A: 3-factor roughness |
| 32 | Krimphoff, J. et al. | 1994 | Characterization of the timbre of complex sounds | A/C: spectral irregularity |
| 33 | Pollard, H.F. & Jansson, E.V. | 1982 | A tristimulus method for the specification of musical timbre | C: tristimulus (partial-based) |
| 34 | Longuet-Higgins, H.C. & Lee, C. | 1984 | The rhythmic interpretation of monophonic music | G: syncopation algorithm (LHL) |
| 35 | Spiech, C. et al. | 2022 | Information content of auditory rhythms | I: rhythmic IC |
| 36 | ISO 532-1 | 2017 | Acoustics -- Methods for calculating loudness -- Part 1: Zwicker method | K: loudness standard |
| 37 | ISO 226 | 2003 | Acoustics -- Normal equal-loudness-level contours | K: A-weighting curves |
| 38 | DIN 45692 | -- | Measurement technique for the simulation of the auditory sensation of sharpness | K: Zwicker sharpness |
| 39 | Kim, S.G. et al. | 2021 | Neural correlates of syntactic irregularity and perceptual ambiguity (MEG) | H/I: syntactic irregularity, tonal ambiguity |

---

## Local Literature File Matrix

Full mapping from local `Literature/r3/` files to the features they support.
Based on R3-DSP-SURVEY-THEORY.md Section 7.

| Local File | Category | Features Supported |
|-----------|----------|-------------------|
| `psychoacoustics/Consonance&Dissonance_Part1.md` | Consonance | [0] roughness, [3] stumpf_fusion (CDC taxonomy) |
| `psychoacoustics/Consonance&Dissonance_Part2.md` | Consonance | [0] roughness, [1] sethares_dissonance, Vassilakis 3-factor model |
| `psychoacoustics/Fundamental_Principles_Part1.md` | Consonance/Pitch | Cents formula, JND, combination tones |
| `psychoacoustics/Fundamental_Principles_Part2.md` | Consonance | Harmonic distance, harmonic intersection |
| `psychoacoustics/Pressnitzer_2000_ContMusRev.md` | Consonance/Timbre/Psycho | [0] critical bandwidth, [13] sharpness, [122] sharpness_zwicker, [123] fluctuation_strength |
| `psychoacoustics/elife-neural_Part1.md` | Energy/Information | [11] onset_strength, [90] spectral_surprise, [91] information_rate |
| `psychoacoustics/ji_primer_ed3.md` | Consonance | Benade's special relationships, coincident harmonics |
| `psychoacoustics/Intonation_of_Harmonic_Intervals.md` | Consonance/Change | 4-factor intonation model, beat frequency |
| `dsp-and-ml/CNN_Genre_Classification.md` | Timbre | [94:106] MFCC, spectral centroid, spectral rolloff |
| `dsp-and-ml/Modulation_Classification.md` | Change/Rhythm | [114:119] modulation spectrum at 4-16 Hz |
| `dsp-and-ml/Music_type_classification_by_spectral_contrast_fea.md` | Timbre | [107:113] spectral contrast (6 octave sub-bands) |
| `spectral-music/Anderson.md` | Timbre/Change | Harmonic/non-harmonic spectra, rate of spectral change |
| `spectral-music/Fineberg_Basics.md` | Pitch/Timbre | Partial frequency tracking, spectral envelope |
| `spectral-music/Stanford-Spectral.md` | Timbre/Harmony | [64] inharmonicity_index, harmonic vs. inharmonic continuum |
| `computational-music-theory/Tymoczko.md` | Harmony | [82] voice_leading_distance, [85] diatonicity, 5 components of tonality |
| `computational-music-theory/Balzano-1980.md` | Harmony/Pitch | [49:60] chroma, [76:81] tonnetz, circle-of-fifths |
| `computational-music-theory/Geometry_Part1-5.md` | Harmony | [82] voice_leading_distance, chord space geometry |
| `computational-music-theory/Neo-Riemannian_Part1-5.md` | Harmony | [76:81] tonnetz coordinates, P/L/R transformations |
| `music-theory-analysis/harmony_perception_by_periodicity.md` | Consonance | [2] helmholtz_kang, periodicity detection |
| `music-theory-analysis/a_neurodynamic_account.md` | Harmony | Mode-locking stability, Farey ratio table |
| `music-theory-analysis/simultaneous_consonance.md` | Consonance | [4] sensory_pleasantness, Harrison-Pearce 3-component model |
| `music-theory-analysis/perception_of_affect.md` | Information/Harmony | [75] key_clarity, spectral entropy predicts chord affect |
| `music-theory-analysis/fluidharmony.md` | Harmony | PC-DFT magnitudes, tonal index |
| `music-theory-analysis/the_tonnetz_at_first_sight.md` | Harmony | [76:81] tonnetz as cognitive interface |
| `music-theory-analysis/geometry_of_music_perception.md` | Harmony | Stratified chord space, roughness/harmonicity gradients |
| `music-theory-analysis/thinking_about_musical_time.md` | Rhythm | [69] metricality, hierarchical temporal nesting |
| `music-theory-analysis/mp3604_05_parncutt_406430.md` | Pitch | [63] pitch_salience, virtual pitch perception |
