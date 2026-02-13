# R3 Spectral Architecture -- Changelog

All notable changes to the R3 spectral feature extraction system are documented in this file.

---

## [2.0.0] -- 2025 (Phase 3B)

### Summary

Major expansion from 49D to 128D. Six new spectral groups (F through K) added, covering pitch, rhythm, harmony, information theory, extended timbre, and psychoacoustic modulation. Original groups A-E preserved with unchanged indices.

### Added

- **Group F: Pitch & Chroma** (16D, [49:65])
  - 12-bin chroma vector via mel-to-pitch-class Gaussian soft-assignment folding
  - pitch_height: weighted log-frequency (Weber-Fechner)
  - pitch_class_entropy: chroma distribution uniformity
  - pitch_salience: spectral peak prominence (Parncutt proxy)
  - inharmonicity_index: harmonic series deviation measurement

- **Group G: Rhythm & Groove** (10D, [65:75])
  - tempo_estimate: onset autocorrelation-based BPM estimation (30-300 BPM)
  - beat_strength, pulse_clarity: pulse perception metrics
  - syncopation_index: LHL metrical conflict model (Longuet-Higgins & Lee 1984)
  - metricality_index: multi-scale nested pulse detection (Grahn & Brett 2007)
  - isochrony_nPVI: rhythmic regularity measure (Ravignani 2021)
  - groove_index: composite movement-inducing quality (Madison 2006)
  - event_density, tempo_stability, rhythmic_regularity

- **Group H: Harmony & Tonality** (12D, [75:87])
  - key_clarity: Krumhansl-Schmuckler key profile correlation
  - 6D tonnetz coordinates (Harte 2006): fifth, minor, major circle projections
  - voice_leading_distance: chroma L1 distance (Tymoczko parsimony)
  - harmonic_change: cosine distance between successive chroma frames
  - tonal_stability: composite key clarity and harmonic change rate
  - diatonicity: Tymoczko macroharmony measure
  - syntactic_irregularity: KL divergence from diatonic template (Lerdahl 2001)

- **Group I: Information & Surprise** (7D, [87:94])
  - melodic_entropy: chroma transition entropy (IDyOM approximation)
  - harmonic_entropy: chroma KL divergence from running average
  - rhythmic_information_content: onset interval surprise (Spiech 2022)
  - spectral_surprise: frame-level spectral prediction error (Friston)
  - information_rate: mutual information between successive frames
  - predictive_entropy: conditional prediction uncertainty
  - tonal_ambiguity: key profile correlation entropy

- **Group J: Timbre Extended** (20D, [94:114])
  - 13 MFCCs (coefficients 1-13) via pre-computed DCT matrix
  - 7 spectral contrast bands (octave sub-band peak-valley differences)

- **Group K: Modulation & Psychoacoustic** (14D, [114:128])
  - 6 modulation spectrum rates (0.5, 1, 2, 4, 8, 16 Hz) via sliding-window FFT
  - modulation_centroid, modulation_bandwidth
  - sharpness_zwicker: DIN 45692 perceptual sharpness
  - fluctuation_strength: ~4 Hz temporal modulation (Zwicker & Fastl)
  - loudness_a_weighted: ISO 226 frequency-weighted loudness
  - alpha_ratio, hammarberg_index, spectral_slope_0_500 (eGeMAPS features)

- **3-stage dependency DAG**: parallel(A,B,C,D,F,J,K) -> parallel(E,G,H) -> I
- **Auto-discovery mechanism** for group registration via `extensions/` directory
- **R3FeatureRegistry** with freeze/thaw pattern and `R3FeatureMap` immutable output
- **Extension template** at `mi_beta/ear/r3/extensions/_template.py`
- **Running statistics** with exponential moving average (tau=2.0s, alpha~0.0029)
- **Warm-up protocol**: 344-frame (2.0s) confidence ramp for entropy/modulation features
- **6-domain taxonomy**: Psychoacoustic, Spectral, Tonal, Temporal, Information, CrossDomain

### Preserved (Backward Compatible)

- Group A: Consonance [0:7] -- 7D, all indices and formulas unchanged
- Group B: Energy [7:12] -- 5D, all indices and formulas unchanged
- Group C: Timbre [12:21] -- 9D, all indices and formulas unchanged
- Group D: Change [21:25] -- 4D, all indices and formulas unchanged
- Group E: Interactions [25:49] -- 24D, all indices and formulas unchanged
- All 96 C3 model documentation Section 4 index references remain valid

### Flagged for Phase 6

The following issues were identified by the R2 literature review but deferred to Phase 6 to preserve backward compatibility:

- **Duplication**: [3] stumpf_fusion == [12] warmth (identical formula)
- **Duplication**: [2] helmholtz_kang == [17] spectral_autocorrelation (identical formula)
- **Complement**: [16] spectral_smoothness == 1 - [1] sethares_dissonance
- **Bug**: [24] distribution_concentration normalization (both extremes map to 1.0)
- **Bug**: [10] loudness double-compression (Stevens' law on log-mel)
- **Proxy mismatch**: E group uses independent proxies instead of actual A-D outputs
- **E group expansion** (24D -> 40D with F-K cross-group interactions) deferred to v2.1

### Technical Details

| Property | v1 Value | v2 Value |
|----------|----------|----------|
| Total dimensions | 49 | 128 |
| Number of groups | 5 (A-E) | 11 (A-K) |
| Number of domains | 5 (informal) | 6 (formal taxonomy) |
| GPU latency (parallel) | ~0.5 ms | ~2.5 ms (amortized) |
| RT headroom | ~10x | ~2.3x |
| Power-of-2 aligned | No (49) | Yes (128 = 2^7) |

---

## [1.0.0] -- 2024 (Original)

### Summary

Initial R3 spectral feature extraction system. 49 dimensions across 5 groups, extracting psychoacoustic and spectral features from mel spectrograms.

### Architecture

- **Group A: Consonance** (7D, [0:7]) -- Roughness, dissonance, harmonicity, fusion, pleasantness
- **Group B: Energy** (5D, [7:12]) -- Amplitude, velocity, acceleration, loudness, onset strength
- **Group C: Timbre** (9D, [12:21]) -- Warmth, sharpness, tonalness, clarity, tristimulus
- **Group D: Change** (4D, [21:25]) -- Spectral flux, entropy, flatness, concentration
- **Group E: Interactions** (24D, [25:49]) -- Cross-group element-wise products (3 blocks of 8D)

### Technical Details

| Property | Value |
|----------|-------|
| Total dimensions | 49 |
| Number of groups | 5 (A-E) |
| Input | mel spectrogram (B, 128, T) @ 172.27 Hz |
| Output | (B, T, 49) tensor, [0,1] range |
| GPU latency | ~0.5 ms/frame |
| Computation | All frame-level, no running statistics |

---

## Planned: Phase 6 Changes

The following changes are planned for Phase 6 (formula revision phase):

### Bug Fixes

- Fix [24] distribution_concentration normalization: `(HHI - 1/N) / (1 - 1/N)`
- Fix [10] loudness double-compression: apply Stevens' law to linear power, not log-mel

### Deduplication

- [3] stumpf_fusion -> Parncutt subharmonic tonal fusion (new formula, same index)
- [16] spectral_smoothness -> spectral_spread (2nd central moment)
- [17] spectral_autocorrelation -> spectral_kurtosis (4th central moment)

### E Group Redesign

- Phase 6 Stage 1: Replace proxies with actual A-D outputs (24D preserved)
- Phase 6 Stage 2 (v2.1 scope): Add F-K cross-group interactions (+16D -> 144D total)

### Code Migration

- `R3_DIM = 49` -> `R3_DIM = 128` in `constants.py`
- `_R3_FEATURE_NAMES` -> registry-based `get_r3_feature_names()`
- `assert index < 49` -> `assert index < R3_DIM` in `feature_spec.py`
- Stage-ordered extraction in `R3Extractor.extract()`
- Validation assertions in `R3FeatureRegistry.freeze()`
