# R³ DSP Feature Survey — Modern Audio Analysis Toolkits

> **Phase 3A-2 · Chat R3 Deliverable**
> Date: 2026-02-13 · Status: COMPLETE
> Input constraint: mel spectrogram `(B, 128, T)` @ 172.27 Hz (~5.8 ms/frame)

---

## Bölüm 1 — Executive Summary

This survey inventories **all computable audio features** from six modern toolkits (librosa, essentia, openSMILE/eGeMAPS, madmom, CREPE/pYIN/SPICE/Basic Pitch) and four international standards (ISO 532, ISO 226, ITU-R BS.1770, AES), evaluating each against the MI project's single constraint: **all computation must start from a pre-computed 128-band log-mel spectrogram at 172.27 Hz frame rate, with no access to raw audio.**

### Key Findings

| Metric | Value |
|--------|-------|
| Total features surveyed | ~300+ across all toolkits |
| Fully mel-compatible | ~95 distinct feature dimensions |
| Partially mel-compatible (approximations) | ~35 feature dimensions |
| Not mel-compatible (require raw audio) | ~170+ features |
| Current R³ dimensionality | 49D (5 groups: A–E) |
| Proposed new groups | 5 (F–J) adding 79–207D |
| Recommended target | **128D** (minimum) to **256D** (maximum) |

### The Fundamental Mel Constraint

The mel spectrogram is a **magnitude-only**, **frequency-smoothed** representation. This permanently blocks:

1. **Precise pitch (F0)** — CREPE, pYIN, SPICE, Basic Pitch, YIN all require raw audio
2. **Formants / jitter / shimmer** — need glottal-cycle-level waveform analysis
3. **Phase-based features** — mel is magnitude-only
4. **Pre-trained neural models** — madmom RNNs/CNNs, CREPE CNNs tied to specific spectral frontends
5. **True ITU-R BS.1770 compliance** — K-weighting requires IIR filtering on raw audio

What mel **does** support well: spectral shape descriptors, temporal modulation analysis, chromagram-derived harmony (approximate), onset/rhythm features, perceptual loudness approximations, statistical features, cross-band interactions.

---

## Bölüm 2 — Toolkit-Based Feature Tables

### 2.1 librosa (v0.11.0) — 70 Feature-Relevant Functions

*Verified against locally installed library with empirical shape tests.*

#### Chroma Features (4 functions)

| Function | Dim | Input | Mel-OK? | Cost |
|----------|-----|-------|---------|------|
| `chroma_stft` | 12D/frame | y or S (power STFT) | PARTIAL — needs STFT, not mel directly; but mel-to-chroma approximation possible via frequency folding | Medium |
| `chroma_cqt` | 12D/frame | y or C (CQT) | NO — requires CQT | Expensive |
| `chroma_cens` | 12D/frame | y or C (CQT) | NO — requires CQT + smoothing | Expensive |
| `chroma_vqt` | 12D/frame | y or V (VQT) | NO — requires VQT | Expensive |

#### Spectral Shape Features (8 functions)

| Function | Dim | Input | Mel-OK? | Cost |
|----------|-----|-------|---------|------|
| `melspectrogram` | 128D/frame | y or S | YES (identity) | — |
| `mfcc` | 20D/frame (default) | y or S (log-mel) | **YES** — DCT of log-mel is the definition | Cheap |
| `spectral_centroid` | 1D/frame | y or S | **YES** — weighted mean of mel bins | Cheap |
| `spectral_bandwidth` | 1D/frame | y or S | **YES** — weighted std of mel bins | Cheap |
| `spectral_contrast` | 7D/frame | y or S | **YES** — peak/valley per mel sub-band | Cheap |
| `spectral_flatness` | 1D/frame | y or S | **YES** — geometric/arithmetic mean of mel | Cheap |
| `spectral_rolloff` | 1D/frame | y or S | **YES** — cumulative energy threshold on mel | Cheap |
| `poly_features` | (order+1)D/frame | y or S | **YES** — polynomial fit on mel bins | Cheap |

#### Tonal Features (1 function)

| Function | Dim | Input | Mel-OK? | Cost |
|----------|-----|-------|---------|------|
| `tonnetz` | 6D/frame | y or chroma | PARTIAL — requires chroma as input; can feed mel-derived chroma | Medium |

#### Time-Domain & Energy (2 functions)

| Function | Dim | Input | Mel-OK? | Cost |
|----------|-----|-------|---------|------|
| `zero_crossing_rate` | 1D/frame | y only | **NO** — raw audio only | — |
| `rms` | 1D/frame | y or S | **YES** — sum of mel band powers | Cheap |

#### Rhythm / Tempo (4 functions)

| Function | Dim | Input | Mel-OK? | Cost |
|----------|-----|-------|---------|------|
| `tempogram` | 384D/frame | y or onset_env | **YES** — via mel-derived onset | Medium |
| `fourier_tempogram` | 193D/frame | y or onset_env | **YES** — via mel-derived onset | Medium |
| `tempogram_ratio` | 13D/frame | y, onset_env, or tg | **YES** | Medium |
| `tempo` | 1D global | y, onset_env, or tg | **YES** (indirect) | Medium |

#### Onset Detection (4 functions)

| Function | Dim | Input | Mel-OK? | Cost |
|----------|-----|-------|---------|------|
| `onset_strength` | 1D/frame | y or S | **YES** — spectral flux on mel | Medium |
| `onset_strength_multi` | n_ch × 1D/frame | y or S | **YES** — sub-band onset strength | Medium |
| `onset_detect` | sparse events | y or onset_env | **YES** (indirect) | Medium |
| `onset_backtrack` | sparse events | events + energy | **YES** (indirect) | Cheap |

#### Beat Tracking (3 functions)

| Function | Dim | Input | Mel-OK? | Cost |
|----------|-----|-------|---------|------|
| `beat_track` | events | y or onset_env | **YES** (indirect via onset) | Medium |
| `plp` | 1D/frame | y or onset_env | **YES** (indirect) | Medium |
| `beat.tempo` | 1D global | y, onset_env, or tg | **YES** (indirect) | Medium |

#### Pitch Tracking (3 functions)

| Function | Dim | Input | Mel-OK? | Cost |
|----------|-----|-------|---------|------|
| `piptrack` | 2 × 1025D/frame | y or S (STFT mag) | **NO** — needs linear spectrum | Medium |
| `yin` | 1D/frame | y only | **NO** — time-domain autocorrelation | Medium |
| `pyin` | 3D/frame | y only | **NO** — probabilistic YIN on waveform | Expensive |

#### Harmonic Analysis (3 functions)

| Function | Dim | Input | Mel-OK? | Cost |
|----------|-----|-------|---------|------|
| `f0_harmonics` | n_harmonics/frame | x (any TF) + f0 | PARTIAL — needs pre-computed F0 | Cheap |
| `interp_harmonics` | variable | x (any TF) + freqs | PARTIAL | Cheap |
| `salience` | same as S | S + freqs + harmonics | **NO** — needs linear spectrum | Medium |

#### Meta-Features (2 functions)

| Function | Dim | Input | Mel-OK? | Cost |
|----------|-----|-------|---------|------|
| `delta` | same as input | any 2D matrix | **YES** — Savitzky-Golay derivative | Cheap |
| `stack_memory` | input × n_steps | any 2D matrix | **YES** — temporal context stacking | Cheap |

#### Normalization & Weighting (10 functions)

| Function | Mel-OK? | Notes |
|----------|---------|-------|
| `pcen` | **YES** — per-channel energy normalization on mel | Alternative to log scaling |
| `amplitude_to_db` / `power_to_db` | **YES** — element-wise | Standard |
| `perceptual_weighting` | **YES** — per-mel-band weight | A/B/C/D curves |
| `A/B/C/D_weighting` | **YES** — static lookup | Per-frequency |

#### Decomposition (3 functions)

| Function | Mel-OK? | Notes |
|----------|---------|-------|
| `hpss` (spectrogram) | **YES** — median filtering on mel | Harmonic/percussive separation |
| `decompose` (NMF/PCA) | **YES** — on any feature matrix | Expensive but powerful |
| `nn_filter` | **YES** — nearest-neighbor on any matrix | Medium |

**librosa Summary: 33 functions fully mel-compatible, 5 partially, 7 not compatible.**

---

### 2.2 essentia (v2.1-beta6) — 68+ Algorithms

#### Fully Mel-Compatible (28 algorithms)

| Algorithm | Dim | Description |
|-----------|-----|-------------|
| MFCC | 13D | DCT of log-mel (exact) |
| Flux | 1D | Frame-to-frame mel difference |
| Flatness / FlatnessDB | 1D | Geometric/arithmetic mean ratio |
| HFC (High Freq Content) | 1D | Frequency-weighted mel sum |
| RollOff | 1D | Cumulative energy threshold |
| Decrease | 1D | Spectral envelope slope |
| Crest | 1D | Max/mean ratio of mel bands |
| CentralMoments | 5D | Moments 0–4 of mel distribution |
| DistributionShape | 3D | Spread, skewness, kurtosis from moments |
| Energy | 1D | Sum of mel band powers |
| Entropy | 1D | Shannon entropy of mel distribution |
| InstantPower | 1D | Mean mel band power |
| Centroid | 1D | Weighted mean of mel band indices |
| SuperFluxNovelty | 1D | Novelty from mel max-filtering + flux |
| NoveltyCurve | 1D | Band-energy novelty (explicit mel input) |
| EnergyBand | 1D/band | Sum mel bands in frequency range |
| EnergyBandRatio | 1D | Ratio of two frequency bands |
| MaxToTotal | 1D | Max/total energy of envelope |
| TCToTotal | 1D | Temporal centroid ratio |
| LogAttackTime | 3D | Attack time from mel energy envelope |
| StrongDecay | 1D | Percussiveness from mel envelope |
| DerivativeSFX | 2D | Envelope derivative features |
| FlatnessSFX | 1D | Envelope flatness |
| UnaryOperator | same | Generic element-wise math on mel |
| SpectralContrast | 6–12D | Peak/valley per mel sub-band |

#### Partially Mel-Compatible (~15 algorithms)

| Algorithm | Dim | Limitation |
|-----------|-----|------------|
| ERBBands | 40D | Mel-to-ERB scale mapping (moderate accuracy) |
| BarkBands | 27D | Mel-to-Bark rebinning (good accuracy with 128 mel) |
| GFCC | 13D | ERB approx from mel |
| BFCC | 13D | Bark approx from mel |
| StrongPeak | 1D | Mel profile peak-to-spread ratio |
| SpectralComplexity | 1D | Peak count in mel (coarser) |
| Dissonance | 1D | Roughness proxy from adjacent mel bands |
| DynamicComplexity | 2D | Mel energy variance as loudness proxy |
| SilenceRate | 3D | Energy threshold on mel total |
| OnsetRate | 1D | Peak-pick from mel flux |
| Leq | 1D | RMS in dB from mel total energy |
| BeatLoudness | 1D/beat | Mel energy at beat positions |

#### Not Mel-Compatible (~25 algorithms)

HPCP, Key, ChordsDetection, TuningFrequency, Inharmonicity, OddToEvenHarmonicEnergyRatio, Tristimulus, SpectralPeaks, PitchYin, PitchYinFFT, PredominantPitchMelodia, MultiPitchMelodia, ZeroCrossingRate, LogSpectrum, BeatTrackerDegara, BeatTrackerMultiFeature, LoudnessEBUR128, LoudnessVickers, Larm, Chromagram (CQT-based), Danceability, PowerSpectrum.

---

### 2.3 openSMILE / eGeMAPS — 88 Features

*Reference: Eyben et al. (2015) IEEE TAFFC 7(2), 190-202.*

The eGeMAPS extracts 25 Low-Level Descriptors (LLDs) per frame, then applies functionals (mean, CoV, percentiles, slopes) over segments to produce 88 features.

#### LLD Mel Compatibility

| Category | LLDs | Count | From Mel? |
|----------|------|-------|-----------|
| **Cepstral** | MFCC 1–4 | 4 | **YES** (exact) |
| **Spectral** | spectralFlux, alphaRatio, hammarbergIndex, slope0-500, slope500-1500 | 5 | **PARTIAL** (flux: yes; ratios/slopes: approximate) |
| **Energy** | loudness | 1 | **PARTIAL** (Zwicker approx from mel-to-Bark) |
| **Frequency** | F0, jitter, shimmer, HNR, H1-H2, H1-A3 | 6 | **NO** — all require raw waveform |
| **Formant** | F1/F2/F3 freq, bandwidth, amplitude (×3) | 9 | **NO** — require LPC or linear spectrum |

#### Impact on 88 Final Features

| Feature Subset | Count | From Mel? |
|----------------|-------|-----------|
| MFCC 1–4 functionals | 8 | **YES** |
| Spectral flux functionals | ~4 | YES (approximate) |
| Loudness functionals | ~10 | APPROXIMATE |
| Alpha ratio, Hammarberg, slopes (V/UV) | ~20 | APPROXIMATE |
| F0 functionals | ~10 | NO |
| Jitter/shimmer functionals | ~4 | NO |
| Formant functionals | ~18 | NO |
| Temporal/voicing features | ~7 | NO (need F0) |
| HNR, H1-H2, H1-A3 | ~7 | NO |
| **Total computable/approximable** | **~42** | |
| **Total not computable** | **~46** | |

**eGeMAPS Summary: Roughly half (42/88) computable from mel. The other half fundamentally requires raw audio.**

#### Other openSMILE Configurations

| Config | Features | Year | Notes |
|--------|----------|------|-------|
| IS09_emotion | 384 | 2009 | 16 LLDs × 2 (delta) × 12 functionals |
| IS10_paraling | 1,582 | 2010 | 34 LLDs, extended functionals |
| ComParE 2016 | 6,373 | 2016 | 65 LLDs × 2 × ~39 functionals |
| GeMAPS | 62 | 2015 | Subset of eGeMAPS |
| **eGeMAPS** | **88** | **2015** | **Minimalistic, theory-driven** |

---

### 2.4 madmom — 16+ Processors

| Processor | Input | Output | Frame? | Mel-OK? |
|-----------|-------|--------|--------|---------|
| RNNBeatProcessor | raw → LogFilteredSpec | 1D beat activation | Yes | **NO** — specific filterbank |
| TCNBeatProcessor | raw → spec | 2D (beat+downbeat) | Yes | **NO** |
| SpectralOnsetProcessor | Spectrogram | 1D onset function | Yes | **PARTIAL** (spectral flux: yes) |
| RNNOnsetProcessor | raw → 3× spec | 1D onset activation | Yes | **NO** |
| CNNOnsetDetectionProcessor | raw → spec | 1D onset activation | Yes | **NO** |
| TempoEstimationProcessor | onset activation | (bpm, strength) | No | INDIRECT (via mel onset) |
| CNNKeyRecognitionProcessor | raw → spec | key label | No | **NO** |
| CNNChordRecognitionProcessor | raw → spec | chord sequence | Yes | **NO** |
| RNNPianoNoteProcessor | raw → spec | 88D note activation | Yes | **NO** |
| RNNDownBeatProcessor | raw → spec | 2D beat+downbeat | Yes | **NO** |

**madmom Summary: Only SpectralOnsetProcessor (spectral flux mode) is directly usable from mel. All neural models are tied to their specific spectrogram frontends. Tempo estimation works indirectly via mel-derived onset strength.**

---

### 2.5 CREPE / pYIN / SPICE / Basic Pitch — Pitch Estimators

| Tool | Architecture | Input | Mel-OK? | Why Not |
|------|-------------|-------|---------|---------|
| **CREPE** (2018) | 6-layer CNN → 360 bins | 1024 raw samples @16kHz | **NO** | Learns TF from waveform; phase needed |
| **pYIN** (2014) | Probabilistic YIN + HMM | Raw waveform | **NO** | Time-domain autocorrelation |
| **YIN** (2002) | Autocorrelation diff fn | Raw waveform | **NO** | Same as pYIN |
| **SPICE** (2020) | Self-supervised CNN | Raw @16kHz | **NO** | Waveform encoder, contrastive learning |
| **Basic Pitch** (2022) | CNN on HCQT (6 harmonics) | Raw → Harmonic CQT | **NO** | 6-channel harmonic CQT, not mel |

**Pitch Summary: ALL modern pitch estimators require raw audio. No mel-spectrogram workaround exists for precise F0 estimation. Mel can only provide rough pitch-class information via chromagram approximation.**

---

### 2.6 ISO / AES Standards

| Standard | Measures | Output Dim | Mel-OK? | Quality |
|----------|----------|------------|---------|---------|
| **ISO 532-1** (Zwicker) | Loudness (sone) | 24 Bark + 1 total | YES (rebin mel→Bark) | MODERATE-GOOD |
| **ISO 532-2** (Moore-Glasberg) | Loudness (sone) | ~380 ERB + 1 | PARTIAL (no roex filters) | MODERATE |
| **ISO 226** | Equal-loudness contours | Weight vector | **YES** (freq weighting) | HIGH |
| **ITU-R BS.1770** | LUFS loudness | 3 (M/S/I) | PARTIAL (no true peak) | MODERATE |
| **AES17** | Equipment metrics | Various | **NO** (test signals) | N/A |
| **DIN 45692** | Sharpness (acum) | 1D | **YES** (weighted centroid) | GOOD |
| Zwicker/Fastl | Fluctuation strength (vacil) | 1D (or per-band) | **YES** | GOOD |
| Zwicker/Fastl | Roughness (asper) | 1D (or per-band) | PARTIAL (hop too large) | POOR at 5.8ms hop |

**Standards Summary: ISO 226 frequency weighting and sharpness are directly applicable. Zwicker loudness approximation works via mel-to-Bark rebinning. Roughness is problematic — peak sensitivity at 70 Hz modulation requires <1.67ms hop, but MI's 5.8ms hop only captures up to ~86 Hz modulation (borderline). Fluctuation strength (peak 4 Hz) works well at any standard hop size.**

---

## Bölüm 3 — Mel-Compatible Feature Catalog

All features below can be computed from the input `(B, 128, T)` log-mel spectrogram at 172.27 Hz frame rate.

### Priority: HIGH — Well-established, proven value, low cost

| # | Feature | Dim | Source | Already in R³? | Notes |
|---|---------|-----|--------|---------------|-------|
| 1 | MFCC (coefficients 1–13) | 13D | librosa, essentia, openSMILE | No | DCT of log-mel; standard timbral descriptor |
| 2 | MFCC delta (1st derivative) | 13D | librosa.feature.delta | No | Temporal change of timbre |
| 3 | Spectral centroid | 1D | librosa, essentia | Related: clarity [15] | Weighted mean of mel bins |
| 4 | Spectral bandwidth | 1D | librosa, essentia (DistShape.spread) | No | 2nd moment of mel distribution |
| 5 | Spectral contrast | 7D | librosa, essentia | No | Peak-to-valley per octave sub-band |
| 6 | Spectral flatness | 1D | librosa, essentia | Related: distribution_flatness [22] | Geometric/arithmetic mean |
| 7 | Spectral rolloff | 1D | librosa, essentia | No | 85% cumulative energy frequency |
| 8 | Onset strength | 1D | librosa, essentia (SuperFlux) | Related: onset_strength [11] | Mel spectral flux |
| 9 | Onset strength multi-band | 4D | librosa (onset_strength_multi) | No | Sub-band onset detection |
| 10 | RMS energy | 1D | librosa | Related: amplitude [7] | Sum of mel powers |
| 11 | Approximate chromagram | 12D | mel→frequency→pitch class fold | No | Pitch-class profile from mel |
| 12 | A/C-weighted loudness | 2D | ISO 226, librosa weighting | No | Perceptual frequency weighting |
| 13 | Spectral skewness | 1D | essentia DistributionShape | No | 3rd moment of mel |
| 14 | Spectral kurtosis | 1D | essentia DistributionShape | No | 4th moment of mel |
| 15 | Spectral decrease | 1D | essentia Decrease | No | Envelope slope measure |
| 16 | Spectral crest | 1D | essentia Crest | No | Max/mean of mel bands |
| 17 | HFC (High Freq Content) | 1D | essentia | No | Frequency-weighted mel sum |

**HIGH priority subtotal: ~63D** (many overlap with existing R³)

### Priority: MEDIUM — Valuable but require multi-step computation

| # | Feature | Dim | Source | Notes |
|---|---------|-----|--------|-------|
| 18 | Tonnetz (tonal centroid) | 6D | librosa (from chroma) | Requires mel→chroma first |
| 19 | Harmonic tension | 3D | Lerdahl/Herremans via chroma | Tonal distance + entropy + flux |
| 20 | Tempogram (reduced) | 8D | librosa (sub-sampled from 384D) | Key tempo bins at musical subdivisions |
| 21 | Tempogram ratio | 13D | librosa | Metrical subdivision strengths |
| 22 | PLP (predominant local pulse) | 1D | librosa.beat.plp | Continuous pulse curve |
| 23 | Syncopation index | 1D | LHL via onset strength | Metrical conflict measure |
| 24 | Groove features | 5D | Janata et al. via onset/beat | Beat clarity, density, stability, regularity |
| 25 | Information content | 3D | Pearce/Dubnov via KL div | Entropy, surprise, predictability |
| 26 | Modulation spectrum | 6D | Chi/Shamma via per-band FFT | Energy at 0.5, 1, 2, 4, 8, 16 Hz rates |
| 27 | Specific loudness (Bark) | 24D | ISO 532-1 via mel→Bark | Approximate Zwicker loudness per band |
| 28 | Sharpness (DIN 45692) | 1D | Zwicker/Fastl | Weighted spectral centroid on Bark |
| 29 | Fluctuation strength | 1D | Zwicker/Fastl | Temporal modulation at ~4 Hz |
| 30 | HPSS features | 2D | librosa.decompose.hpss | Harmonic/percussive energy ratio |
| 31 | Alpha ratio | 1D | eGeMAPS | Low-band / high-band energy ratio |
| 32 | Hammarberg index | 1D | eGeMAPS | Peak energy ratio 0-2k / 2k-5k Hz |
| 33 | Spectral slopes | 2D | eGeMAPS | Linear regression 0-500, 500-1500 Hz |
| 34 | PCEN | 128D→features | librosa | Per-channel energy normalization |

**MEDIUM priority subtotal: ~79D**

### Priority: LOW — Experimental, approximate, or high-cost

| # | Feature | Dim | Source | Notes |
|---|---------|-----|--------|-------|
| 35 | Roughness (approximation) | 1D | Zwicker/Fastl | Limited by 5.8ms hop; captures only <86 Hz mod |
| 36 | ERB bands | 40D | essentia (rebinned from mel) | Moderate approximation quality |
| 37 | NMF activations | kD | librosa.decompose | Expensive; k=8-16 typical |
| 38 | Polynomial features | 3D | librosa poly_features (order=2) | Spectral shape coefficients |
| 39 | Modulation centroid | 1D | Derived from modulation spectrum | Weighted average modulation rate |
| 40 | Approximate Bark loudness | 24D | ISO 532-1 simplified | Without masking spread model |
| 41 | Log attack time | 1D | essentia | Segment-level, not frame-level |
| 42 | Strong decay | 1D | essentia | Segment-level percussiveness |
| 43 | Envelope derivative features | 2D | essentia DerivativeSFX | Segment-level ADSR descriptors |

**LOW priority subtotal: ~73D**

---

## Bölüm 4 — Computation Cost Analysis

Frame rate: 172.27 Hz (5.8 ms/frame). All costs assume batch processing on GPU (PyTorch).

### Cost Tiers

| Tier | Per-Frame Time | Real-Time Factor @172Hz | Category |
|------|---------------|------------------------|----------|
| **Tier 0: Trivial** | <0.01 ms | >5800× RT | Element-wise ops, lookups |
| **Tier 1: Cheap** | 0.01–0.1 ms | 580–5800× RT | Simple reductions, moments |
| **Tier 2: Medium** | 0.1–1 ms | 58–580× RT | Windowed stats, onset detection |
| **Tier 3: Expensive** | 1–10 ms | 5.8–58× RT | NMF, modulation FFT, tempogram |
| **Tier 4: Very Expensive** | >10 ms | <5.8× RT | Neural inference, full PEAQ |

### Feature Cost Classification

| Feature Group | Dim | Tier | Operations |
|---------------|-----|------|-----------|
| Mel → spectral moments (centroid, bandwidth, skew, kurt) | 4D | 0 | Weighted stats on 128 bins |
| Mel → spectral shape (flatness, rolloff, crest, decrease, HFC) | 5D | 0 | Simple reductions |
| Mel → frequency weighting (A/C/ISO226) | 2D | 0 | Pre-computed weight vector multiply |
| Mel → MFCC (DCT) | 13D | 1 | `torch.fft.dct` or matrix multiply (128→13) |
| Mel → MFCC delta | 13D | 1 | Savitzky-Golay convolution |
| Mel → spectral contrast | 7D | 1 | Sort + percentile per sub-band |
| Mel → onset strength | 1D | 1 | Diff + ReLU + sum |
| Mel → multi-band onset | 4D | 1 | Same as above per sub-band |
| Mel → chroma (approximate) | 12D | 1 | Mel-to-frequency mapping + pitch-class fold |
| Mel → specific loudness (Bark) | 24D | 1 | Mel-to-Bark rebin + compression |
| Mel → sharpness | 1D | 1 | Weighted centroid on Bark-converted |
| Mel → alpha ratio, Hammarberg, slopes | 4D | 1 | Band summation + regression |
| Mel → HPSS | 2D | 2 | Median filtering on mel (kernel ~17) |
| Mel → tonnetz | 6D | 2 | Chroma computation + tonal centroid |
| Mel → harmonic tension | 3D | 2 | Chroma → key → distance |
| Mel → information content (entropy, KL) | 3D | 2 | Per-frame entropy + rolling KL divergence |
| Mel → groove features | 5D | 2 | Onset → beat → stats |
| Mel → syncopation | 1D | 2 | Onset → beat → metrical grid → LHL |
| Mel → PLP (pulse curve) | 1D | 2 | Onset → autocorrelation |
| Mel → fluctuation strength | 1D | 2 | Per-band temporal envelope → 4 Hz filter |
| Mel → tempogram (reduced 8D) | 8D | 3 | Onset → autocorrelation bank |
| Mel → tempogram ratio | 13D | 3 | Tempogram → metrical ratios |
| Mel → modulation spectrum | 6D | 3 | Per-band short-time FFT |
| Mel → roughness approximation | 1D | 3 | High-rate modulation extraction |
| Mel → NMF activations | 8D | 3 | Iterative NMF (50–100 iterations) |

### Real-Time Budget

At 172.27 Hz, each frame gets **5.8 ms** of real-time budget. Assuming GPU batch processing:

- **Core R³ (49D current)**: ~0.5 ms/frame → **11.5× RT headroom**
- **+Tier 0+1 features (~90D)**: ~0.2 ms additional → total ~0.7 ms → **8.3× RT**
- **+Tier 2 features (~20D)**: ~0.5 ms additional → total ~1.2 ms → **4.8× RT**
- **+Tier 3 features (~36D)**: ~3 ms additional → total ~4.2 ms → **1.4× RT**
- **All proposed (~195D)**: ~4.2 ms/frame → **1.4× RT** (still real-time on GPU)

**Conclusion**: Expansion to 128–256D is feasible in real-time on GPU. Tier 3 features (tempogram, modulation spectrum, NMF) dominate cost but are still within budget.

---

## Bölüm 5 — Proposed New R³ Groups

Current: A:Consonance(7D), B:Energy(5D), C:Timbre(9D), D:Change(4D), E:Interactions(24D) = **49D**

### Group F: Pitch & Harmony (18D) [49:67]

Approximate pitch-class and tonal features from mel.

| Sub-group | Dim | Features | Source |
|-----------|-----|----------|--------|
| f_chroma | 12D | Approximate chromagram (12 pitch classes) | Mel→freq→pitch fold |
| f_tonnetz | 6D | Tonal centroid (fifth_x/y, minor_x/y, major_x/y) | librosa.tonnetz from chroma |

**Rationale**: Chroma captures harmonic content that consonance (Group A) cannot — specifically pitch-class distribution and tonal space position. This is the most-requested missing feature class across all C³ model gap logs.

### Group G: Rhythm & Groove (12D) [67:79]

Temporal structure features from onset strength.

| Sub-group | Dim | Features | Source |
|-----------|-----|----------|--------|
| g_groove | 5D | beat_clarity, onset_density, tempo_stability, syncopation, onset_regularity | Janata/Madison/LHL |
| g_tempo | 5D | Top-5 tempogram peaks (metrical hierarchy) | librosa.tempogram |
| g_pulse | 1D | Predominant local pulse strength | librosa.plp |
| g_modbeat | 1D | Beat-rate modulation energy (1–2 Hz) | Modulation spectrum |

**Rationale**: R³ currently has zero rhythm/tempo features. Groove and syncopation are among the strongest predictors of musical engagement.

### Group H: Spectral Detail (20D) [79:99]

Extended spectral shape and statistics.

| Sub-group | Dim | Features | Source |
|-----------|-----|----------|--------|
| h_mfcc | 13D | MFCC 1–13 | librosa/essentia |
| h_contrast | 7D | Spectral contrast (7 octave sub-bands) | librosa/essentia |

**Rationale**: MFCCs are the most-used audio feature in MIR, complementing mel directly. Spectral contrast captures harmonic/noisy texture distinction that R³ timbre features miss.

### Group I: Information Dynamics (9D) [99:108]

Surprise, predictability, and perceptual information measures.

| Sub-group | Dim | Features | Source |
|-----------|-----|----------|--------|
| i_info | 3D | spectral_surprise, temporal_predictability, modulation_depth | Pearce/Dubnov/Abdallah |
| i_tension | 3D | tonal_distance, chroma_entropy, chroma_flux | Lerdahl/Herremans |
| i_loudness | 3D | specific_loudness_low, specific_loudness_mid, specific_loudness_high | ISO 532-1 (3 Bark regions) |

**Rationale**: Prediction error (surprise) is fundamental to the MI brain's C³ models (BEP mechanism). Information dynamics provides the raw material for musical expectation computation.

### Group J: Modulation & Perception (20D) [108:128]

Temporal modulation and psychoacoustic features.

| Sub-group | Dim | Features | Source |
|-----------|-----|----------|--------|
| j_mod | 6D | Modulation energy at 0.5, 1, 2, 4, 8, 16 Hz | Chi/Shamma cortical model |
| j_mod_stats | 2D | modulation_centroid, modulation_bandwidth | Derived from modulation spectrum |
| j_percept | 4D | sharpness, fluctuation_strength, roughness_approx, loudness_A | DIN 45692/Zwicker/ISO 226 |
| j_shape | 4D | spectral_skewness, spectral_kurtosis, spectral_decrease, spectral_crest | essentia DistributionShape |
| j_ratios | 4D | alpha_ratio, hammarberg_index, spectral_slope_low, spectral_slope_high | eGeMAPS |

**Rationale**: Modulation spectrum captures perceptually critical temporal patterns (vibrato, tremolo, beat). Psychoacoustic features bridge mel space to human perception research.

### Summary: Proposed Expansion

| Group | Name | Dim | Range | Tier Cost |
|-------|------|-----|-------|-----------|
| F | Pitch & Harmony | 18D | [49:67] | 1–2 |
| G | Rhythm & Groove | 12D | [67:79] | 2–3 |
| H | Spectral Detail | 20D | [79:99] | 0–1 |
| I | Information Dynamics | 9D | [99:108] | 1–2 |
| J | Modulation & Perception | 20D | [108:128] | 1–3 |
| **New total** | | **79D** | [49:128] | |
| **R³ total** | A–J | **128D** | [0:128] | |

---

## Bölüm 6 — Comparison Matrix (Toolkit × Feature Category)

| Feature Category | librosa | essentia | openSMILE | madmom | CREPE/pYIN | ISO/AES |
|-----------------|---------|----------|-----------|--------|-----------|---------|
| **Spectral shape** (centroid, bandwidth, rolloff, flatness) | ★★★ | ★★★ | ★★☆ | — | — | — |
| **MFCC / cepstral** | ★★★ | ★★★ | ★★★ | — | — | — |
| **Chroma / tonal** | ★★☆ᵃ | ★☆☆ᵇ | — | ★☆☆ᶜ | — | — |
| **Onset / novelty** | ★★★ | ★★★ | ★★☆ | ★★☆ᵈ | — | — |
| **Beat / tempo** | ★★★ | ★☆☆ | — | ★☆☆ᵈ | — | — |
| **Pitch (F0)** | ★☆☆ᵉ | ★☆☆ᵉ | ★☆☆ᵉ | ★☆☆ᵉ | ★☆☆ᵉ | — |
| **Loudness / perception** | ★★☆ | ★★☆ | ★★☆ | — | — | ★★★ |
| **Modulation / rhythm** | ★★☆ | ★☆☆ | — | — | — | ★★☆ |
| **Statistical moments** | ★★☆ | ★★★ | ★★★ | — | — | — |
| **Information dynamics** | ★☆☆ | ★☆☆ | — | — | — | — |

Legend: ★★★ = rich mel-compatible support · ★★☆ = partial/approximate · ★☆☆ = minimal/indirect · — = not covered

ᵃ chroma_stft needs STFT but mel-to-chroma approximation works
ᵇ HPCP requires SpectralPeaks (not mel)
ᶜ Key/chord via template matching on mel-chroma (low quality)
ᵈ Only via mel-derived onset strength (indirect); all neural models blocked
ᵉ ALL pitch estimators require raw audio; mel provides only rough proxies

### Top Toolkit per Feature Category (mel-only mode)

| Category | Best Toolkit | Reason |
|----------|-------------|--------|
| Spectral shape | **librosa** | Comprehensive S= input, all tested |
| MFCC | **librosa** = essentia | Both compute identical DCT of log-mel |
| Chroma/tonal | **librosa** (custom mel→chroma) | tonnetz from chroma available |
| Onset/novelty | **essentia** (SuperFluxNovelty) | Designed for band-filtered spectrograms |
| Beat/tempo | **librosa** (tempogram family) | onset_envelope → tempogram pipeline |
| Loudness/perception | **ISO 532-1** (Zwicker via Bark) | Standardized psychoacoustic model |
| Modulation | **Custom** (per-band temporal FFT) | Chi/Shamma cortical model |
| Statistics | **essentia** (CentralMoments + DistShape) | Clean pipeline: moments → shape |
| Information dynamics | **Custom** (KL divergence + entropy) | No toolkit provides this directly |

---

## Bölüm 7 — Dimension Target Proposal

### Option A: Minimum (128D)

Current 49D + 79D new = **128D** — follows the proposed Groups F–J exactly.

| Pros | Cons |
|------|------|
| Clean power-of-2 size | No redundancy buffer |
| All Tier 0–2 features included | Tempogram/modulation coarsely sampled |
| Real-time feasible (~1.2 ms/frame) | Some C³ model demands may not be met |

### Option B: Medium (192D)

128D base + 64D extended features:

- MFCC delta-delta (+13D)
- Full tempogram ratio (+13D)
- Expanded modulation spectrum (12 rates instead of 6, +6D)
- Bark-specific loudness (24 Bark bands instead of 3 regions, +21D)
- ERB-mapped features (+11D)

| Pros | Cons |
|------|------|
| Richer temporal + perceptual detail | Some redundancy with Bark/ERB bands |
| Better covers C³ model demands | Higher compute cost (~2.5 ms/frame) |
| Room for cross-group interactions | Not a clean power-of-2 |

### Option C: Maximum (256D)

192D base + 64D interactions & expansions:

- New cross-group interactions F×G, F×I, G×J (+48D)
- NMF activations (+8D)
- Full polynomial features (+3D)
- Expanded onset-strength multi-band (+4D)
- Roughness at sub-frame resolution (+1D)

| Pros | Cons |
|------|------|
| Covers virtually all mel-computable features | Some features may have low utility |
| Clean power-of-2 size | ~4.2 ms/frame (still real-time on GPU) |
| Maximum information for C³ models | Interaction terms may be redundant |

### Recommendation

**Start with 128D (Option A)**, then expand to 192D or 256D based on empirical C³ model performance. The BaseSpectralGroup architecture with R3FeatureRegistry auto-indexing makes incremental expansion trivial — just add new group classes.

---

## Bölüm 8 — Implementation References

### 8.1 Source Libraries & API Functions

| Feature | Library | API Call | Notes |
|---------|---------|----------|-------|
| MFCC | librosa 0.11 | `librosa.feature.mfcc(S=log_mel, n_mfcc=13)` | S must be log-power mel |
| MFCC delta | librosa 0.11 | `librosa.feature.delta(mfcc, order=1)` | Savitzky-Golay, width=9 |
| Spectral centroid | librosa 0.11 | `librosa.feature.spectral_centroid(S=mel_power)` | Returns Hz; normalize for [0,1] |
| Spectral bandwidth | librosa 0.11 | `librosa.feature.spectral_bandwidth(S=mel_power)` | 2nd moment |
| Spectral contrast | librosa 0.11 | `librosa.feature.spectral_contrast(S=mel_power, n_bands=6)` | 7D output |
| Spectral flatness | librosa 0.11 | `librosa.feature.spectral_flatness(S=mel_power)` | No sr needed |
| Spectral rolloff | librosa 0.11 | `librosa.feature.spectral_rolloff(S=mel_power, roll_percent=0.85)` | Returns Hz |
| Onset strength | librosa 0.11 | `librosa.onset.onset_strength(S=log_mel)` | Spectral flux |
| Tempogram | librosa 0.11 | `librosa.feature.tempogram(onset_envelope=oenv)` | 384D → subsample |
| PLP | librosa 0.11 | `librosa.beat.plp(onset_envelope=oenv)` | Continuous pulse |
| Tonnetz | librosa 0.11 | `librosa.feature.tonnetz(chroma=chroma_approx)` | From pre-computed chroma |
| HPSS | librosa 0.11 | `librosa.decompose.hpss(S=mel_power)` | Returns H, P matrices |
| PCEN | librosa 0.11 | `librosa.pcen(S=mel_power)` | Alternative to log |
| A-weighting | librosa 0.11 | `librosa.A_weighting(frequencies)` | Static weight vector |
| CentralMoments | essentia 2.1 | `CentralMoments()(mel_band_vector)` | 5 moments |
| DistributionShape | essentia 2.1 | `DistributionShape()(central_moments)` | spread, skew, kurt |
| SuperFluxNovelty | essentia 2.1 | `SuperFluxNovelty()(mel_bands)` | Designed for mel |
| Bark loudness | mosqito | `mosqito.loudness_zwst()` | ISO 532-1 compliant |

### 8.2 BaseSpectralGroup Conversion Pattern

All new groups follow the existing template at `mi_beta/ear/r3/extensions/_template.py`:

```python
class PitchHarmonyGroup(BaseSpectralGroup):
    """Group F: Pitch & Harmony (18D) [49:67]"""

    GROUP_NAME = "pitch_harmony"
    OUTPUT_DIM = 18
    INDEX_RANGE = (0, 0)  # Auto-assigned by registry.freeze()

    @property
    def feature_names(self) -> List[str]:
        return [
            # f_chroma (12D)
            "chroma_C", "chroma_Db", "chroma_D", "chroma_Eb",
            "chroma_E", "chroma_F", "chroma_Gb", "chroma_G",
            "chroma_Ab", "chroma_A", "chroma_Bb", "chroma_B",
            # f_tonnetz (6D)
            "tonnetz_fifth_x", "tonnetz_fifth_y",
            "tonnetz_minor_x", "tonnetz_minor_y",
            "tonnetz_major_x", "tonnetz_major_y",
        ]

    def compute(self, mel: Tensor) -> Tensor:
        """mel: (B, 128, T) → (B, T, 18)"""
        B, N, T = mel.shape
        # ... mel-to-chroma conversion ...
        # ... tonnetz from chroma ...
        return features.clamp(0, 1)
```

### 8.3 Key Algorithms to Implement in PyTorch

| Algorithm | Complexity | PyTorch Implementation Notes |
|-----------|-----------|------------------------------|
| Mel → Chroma | O(128) per frame | Pre-compute mel_bin→pitch_class mapping matrix (128×12); `chroma = mapping @ mel` |
| DCT (for MFCC) | O(128 log 128) | `torch.fft.dct` (torch ≥2.1) or pre-computed DCT matrix (128×13) |
| Spectral moments | O(128) per frame | Weighted mean/var/skew/kurt with `mel_bins` as weights |
| Onset strength | O(128) per frame | `relu(mel[:,1:] - mel[:,:-1]).sum(dim=1)` |
| Tempogram (autocorr) | O(T × lag_max) | `torch.fft.rfft` → magnitude² → `torch.fft.irfft` |
| Bark rebinning | O(128) per frame | Pre-compute mel→Bark mapping matrix (128×24) |
| Modulation spectrum | O(T × N_mels) | Per-band `torch.fft.rfft` on sliding windows |
| HPSS (median filter) | O(128 × kernel) | `torch.median` on sliding window; or `kornia.morphology` |
| KL divergence | O(128) per frame | `(p * (p.log() - q.log())).sum()` |

### 8.4 Key References

| # | Reference | Year | Use For |
|---|-----------|------|---------|
| 1 | McFee et al. "librosa: Audio and Music Signal Analysis in Python" | 2015 | All spectral features |
| 2 | Bogdanov et al. "Essentia: an Audio Analysis Library" | 2013 | Statistical + SFX features |
| 3 | Eyben et al. "eGeMAPS for Voice Research and Affective Computing" | 2015 | Minimalistic feature set design |
| 4 | Böck et al. "madmom: a New Python Audio and Music Signal Processing Library" | 2016 | Neural onset/beat models |
| 5 | Kim et al. "CREPE: A Convolutional Representation for Pitch Estimation" | 2018 | Why mel can't do pitch |
| 6 | Mauch & Dixon "pYIN: A Fundamental Frequency Estimator" | 2014 | Why mel can't do pitch |
| 7 | Zwicker & Fastl "Psychoacoustics: Facts and Models" | 1999 | Loudness, sharpness, roughness, fluctuation |
| 8 | ISO 532-1:2017 "Acoustics — Zwicker Loudness" | 2017 | Standardized loudness computation |
| 9 | ISO 226:2003 "Equal-Loudness Contours" | 2003 | Frequency weighting curves |
| 10 | ITU-R BS.1770-5 "Loudness and True-Peak Level" | 2023 | Broadcast loudness (LUFS) |
| 11 | Chi, Ru & Shamma "Multiresolution Spectrotemporal Analysis" | 2005 | Modulation spectrum / cortical model |
| 12 | Lerdahl "Tonal Pitch Space" | 2001 | Harmonic tension model |
| 13 | Pearce "Statistical Learning in Music Cognition" | 2018 | Information dynamics / surprise |
| 14 | Jiang et al. "Music Type Classification by Spectral Contrast" | 2002 | Spectral contrast feature |
| 15 | Longuet-Higgins & Lee "Rhythmic Interpretation of Monophonic Music" | 1984 | Syncopation index (LHL) |
| 16 | Janata et al. "Sensorimotor Coupling and the Psychology of Groove" | 2012 | Groove features |
| 17 | Farbood "A Parametric, Temporal Model of Musical Tension" | 2012 | Multi-parameter tension |
| 18 | Herremans & Chew "MorpheuS" | 2017 | Spiral Array tension computation |
| 19 | Krumhansl "Cognitive Foundations of Musical Pitch" | 1990 | Key profiles for tonal analysis |
| 20 | Gfeller et al. "SPICE: Self-supervised Pitch Estimation" | 2020 | Why mel can't do pitch |
| 21 | Bittner et al. "Basic Pitch: A Lightweight Polyphonic Note Transcription" | 2022 | Why mel can't do pitch (HCQT) |

---

## Appendix A — Feature Overlap with Current R³

| Current R³ Feature | Index | Closest New Feature | Action |
|-------------------|-------|-------------------|--------|
| roughness (A) | [0] | Dissonance (essentia approx) | Keep; complement with consonance×chroma interaction |
| sensory_pleasantness (A) | [4] | — (unique) | Keep |
| amplitude (B) | [7] | RMS energy | Already covered; do not duplicate |
| loudness (B) | [9] | specific_loudness (ISO 532-1) | Keep mel proxy; add Bark-based loudness in Group J |
| onset_strength (B) | [11] | SuperFluxNovelty (essentia) | Keep; add multi-band onset in Group G |
| warmth (C) | [12] | alpha_ratio (eGeMAPS) | Complementary; alpha_ratio in Group J |
| clarity (C) | [15] | spectral_centroid | Nearly identical; do not duplicate |
| spectral_flux (D) | [21] | Flux (essentia), spectral_flux (eGeMAPS) | Already covered; do not duplicate |
| distribution_entropy (D) | [22] | spectral_entropy (information content) | Keep in D; use IC version for prediction error in Group I |
| distribution_flatness (D) | [23] | spectral_flatness (librosa/essentia) | Already covered; do not duplicate |

**Key principle**: New groups should **complement**, not duplicate, existing features. Where overlap exists (5 cases above), the existing R³ implementation is retained and new features provide different computational approaches or additional context.

---

## Appendix B — Mel-to-Chroma Approximation Algorithm

The approximate chromagram from mel spectrogram is the foundation for Groups F and I. Algorithm:

```
Input: mel (B, 128, T) — log-mel spectrogram
       sr = 22050, n_mels = 128, fmin = 0, fmax = sr/2

1. Compute center frequency of each mel bin:
   f_center[m] = 700 * (10^(m * mel_to_hz_scale) - 1)

2. Map each frequency to MIDI pitch:
   midi[m] = 69 + 12 * log2(f_center[m] / 440)

3. Map MIDI pitch to pitch class (0–11):
   pc[m] = round(midi[m]) % 12

4. Build mapping matrix M (128 × 12):
   M[m, pc[m]] = 1  (or use soft assignment with Gaussian kernel)

5. Compute chroma:
   chroma = M^T @ mel_power  → (12, T)
   chroma = chroma / chroma.sum(dim=0, keepdim=True).clamp(min=1e-8)

Output: chroma (B, T, 12) — normalized pitch-class profile
```

Quality: MODERATE. Lower than CQT-based chroma but adequate for key estimation, tension computation, and tonnetz projection. Primary error source: mel bins below ~200 Hz span multiple semitones.

---

*End of R3-DSP-SURVEY-TOOLS.md*
