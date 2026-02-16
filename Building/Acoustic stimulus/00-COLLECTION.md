# Acoustic Stimulus Collection

**Scope**: ALL acoustic stimulus types physically present in the sound wave
**Source**: R³ 128D Feature Catalog + 96 C³ Model Docs + R³ Demand Matrix
**Version**: 1.0.0
**Date**: 2026-02-16

> **Rule**: This collection contains ONLY properties that exist physically in the sound wave.
> Brain-derived phenomena (emotion, attention, memory, reward, expertise) are EXCLUDED.
> Each entry is an independent acoustic stimulus type — not comma-separated concepts.

---

## Master Table

| # | Acoustic Stimulus | R³ Index | Domain | Consuming Models |
|---|-------------------|----------|--------|:----------------:|
| 1 | [Roughness](#1-roughness) | [0] | Psychoacoustic | 69 (Group A) |
| 2 | [Sethares Dissonance](#2-sethares-dissonance) | [1] | Psychoacoustic | 69 |
| 3 | [Periodicity](#3-periodicity) | [2] | Psychoacoustic | 69 |
| 4 | [Tonal Fusion](#4-tonal-fusion) | [3] | Psychoacoustic | 69 |
| 5 | [Sensory Pleasantness](#5-sensory-pleasantness) | [4] | Psychoacoustic | 69 |
| 6 | [Inharmonicity](#6-inharmonicity) | [5] | Psychoacoustic | 69 |
| 7 | [Harmonic Deviation](#7-harmonic-deviation) | [6] | Psychoacoustic | 69 |
| 8 | [Amplitude](#8-amplitude) | [7] | Spectral | 81 (Group B) |
| 9 | [Energy Velocity](#9-energy-velocity) | [8] | Spectral | 81 |
| 10 | [Energy Acceleration](#10-energy-acceleration) | [9] | Spectral | 81 |
| 11 | [Loudness](#11-loudness) | [10] | Spectral | 81 |
| 12 | [Onset Strength](#12-onset-strength) | [11] | Spectral | 81 |
| 13 | [Warmth](#13-warmth) | [12] | Spectral | 55 (Group C) |
| 14 | [Sharpness](#14-sharpness) | [13] | Spectral | 55 |
| 15 | [Tonalness](#15-tonalness) | [14] | Spectral | 55 |
| 16 | [Spectral Centroid / Clarity](#16-spectral-centroid) | [15] | Spectral | 55 |
| 17 | [Spectral Smoothness](#17-spectral-smoothness) | [16] | Spectral | 55 |
| 18 | [Spectral Autocorrelation](#18-spectral-autocorrelation) | [17] | Spectral | 55 |
| 19 | [Tristimulus 1 — Fundamental Strength](#19-tristimulus-1) | [18] | Spectral | 55 |
| 20 | [Tristimulus 2 — Mid Harmonic Strength](#20-tristimulus-2) | [19] | Spectral | 55 |
| 21 | [Tristimulus 3 — High Harmonic Strength](#21-tristimulus-3) | [20] | Spectral | 55 |
| 22 | [Spectral Flux](#22-spectral-flux) | [21] | Temporal | 57 (Group D) |
| 23 | [Distribution Entropy](#23-distribution-entropy) | [22] | Temporal | 57 |
| 24 | [Distribution Flatness](#24-distribution-flatness) | [23] | Temporal | 57 |
| 25 | [Distribution Concentration](#25-distribution-concentration) | [24] | Temporal | 57 |
| 26 | [Energy × Consonance Interaction](#26-energy--consonance-interaction) | [25:33] | CrossDomain | 54 (Group E) |
| 27 | [Change × Consonance Interaction](#27-change--consonance-interaction) | [33:41] | CrossDomain | 54 |
| 28 | [Consonance × Timbre Interaction](#28-consonance--timbre-interaction) | [41:49] | CrossDomain | 54 |
| 29 | [Chroma — 12 Pitch Class Distribution](#29-chroma) | [49:61] | Tonal | 27 (Group F) |
| 30 | [Pitch Height](#30-pitch-height) | [61] | Tonal | 27 |
| 31 | [Pitch Class Entropy](#31-pitch-class-entropy) | [62] | Tonal | 27 |
| 32 | [Pitch Salience](#32-pitch-salience) | [63] | Tonal | 27 |
| 33 | [Inharmonicity Index](#33-inharmonicity-index) | [64] | Tonal | 27 |
| 34 | [Tempo Estimate](#34-tempo-estimate) | [65] | Temporal | 33 (Group G) |
| 35 | [Beat Strength](#35-beat-strength) | [66] | Temporal | 33 |
| 36 | [Pulse Clarity](#36-pulse-clarity) | [67] | Temporal | 33 |
| 37 | [Syncopation Index](#37-syncopation-index) | [68] | Temporal | 33 |
| 38 | [Metricality Index](#38-metricality-index) | [69] | Temporal | 33 |
| 39 | [Isochrony (nPVI)](#39-isochrony) | [70] | Temporal | 33 |
| 40 | [Groove Index](#40-groove-index) | [71] | Temporal | 33 |
| 41 | [Event Density](#41-event-density) | [72] | Temporal | 33 |
| 42 | [Tempo Stability](#42-tempo-stability) | [73] | Temporal | 33 |
| 43 | [Rhythmic Regularity](#43-rhythmic-regularity) | [74] | Temporal | 33 |
| 44 | [Key Clarity](#44-key-clarity) | [75] | Tonal | 22 (Group H) |
| 45 | [Tonnetz Fifth X](#45-tonnetz-fifth-x) | [76] | Tonal | 22 |
| 46 | [Tonnetz Fifth Y](#46-tonnetz-fifth-y) | [77] | Tonal | 22 |
| 47 | [Tonnetz Minor X](#47-tonnetz-minor-x) | [78] | Tonal | 22 |
| 48 | [Tonnetz Minor Y](#48-tonnetz-minor-y) | [79] | Tonal | 22 |
| 49 | [Tonnetz Major X](#49-tonnetz-major-x) | [80] | Tonal | 22 |
| 50 | [Tonnetz Major Y](#50-tonnetz-major-y) | [81] | Tonal | 22 |
| 51 | [Voice Leading Distance](#51-voice-leading-distance) | [82] | Tonal | 22 |
| 52 | [Harmonic Change](#52-harmonic-change) | [83] | Tonal | 22 |
| 53 | [Tonal Stability](#53-tonal-stability) | [84] | Tonal | 22 |
| 54 | [Diatonicity](#54-diatonicity) | [85] | Tonal | 22 |
| 55 | [Syntactic Irregularity](#55-syntactic-irregularity) | [86] | Tonal | 22 |
| 56 | [Melodic Entropy](#56-melodic-entropy) | [87] | Information | 32 (Group I) |
| 57 | [Harmonic Entropy](#57-harmonic-entropy) | [88] | Information | 32 |
| 58 | [Rhythmic Information Content](#58-rhythmic-information-content) | [89] | Information | 32 |
| 59 | [Spectral Surprise](#59-spectral-surprise) | [90] | Information | 32 |
| 60 | [Information Rate](#60-information-rate) | [91] | Information | 32 |
| 61 | [Predictive Entropy](#61-predictive-entropy) | [92] | Information | 32 |
| 62 | [Tonal Ambiguity](#62-tonal-ambiguity) | [93] | Information | 32 |
| 63 | [MFCC Coefficients (13D)](#63-mfcc-coefficients) | [94:107] | Spectral | — (Group J) |
| 64 | [Spectral Contrast (7D)](#64-spectral-contrast) | [107:114] | Spectral | — |
| 65 | [Temporal Modulation Spectrum](#65-temporal-modulation-spectrum) | [114:120] | Psychoacoustic | — (Group K) |
| 66 | [Modulation Centroid](#66-modulation-centroid) | [120] | Psychoacoustic | — |
| 67 | [Modulation Bandwidth](#67-modulation-bandwidth) | [121] | Psychoacoustic | — |
| 68 | [Zwicker Sharpness](#68-zwicker-sharpness) | [122] | Psychoacoustic | — |
| 69 | [Fluctuation Strength](#69-fluctuation-strength) | [123] | Psychoacoustic | — |
| 70 | [Loudness A-weighted](#70-loudness-a-weighted) | [124] | Psychoacoustic | — |
| 71 | [Alpha Ratio](#71-alpha-ratio) | [125] | Psychoacoustic | — |
| 72 | [Hammarberg Index](#72-hammarberg-index) | [126] | Psychoacoustic | — |
| 73 | [Spectral Slope 0-500 Hz](#73-spectral-slope) | [127] | Psychoacoustic | — |

**Total: 73 independent acoustic stimulus types** (spanning 128 R³ dimensions; chroma 12D, MFCC 13D, contrast 7D, modulation 6D, tonnetz 6D, interactions 24D grouped)

---

## Deep Explanations

---

### 1. Roughness
**R³ Index**: [0]
**Domain**: Psychoacoustic

**Physical definition**: Rapid amplitude fluctuation (beating) that arises when two frequencies fall within the same critical band. At beating rates between 20-70 Hz the auditory system perceives this as "rough."

**Measurement**: Plomp & Levelt (1965) model. Maximum roughness occurs when the frequency difference Δf between two sinusoidal tones equals approximately 25% of the critical bandwidth.

**Psychoacoustic basis**: Physical overlap of neighboring frequencies on the basilar membrane. When hair cells in the inner ear are stimulated in the same region, the neural signal fluctuates.

**Sonic examples**: Minor second interval (m2) = high roughness. Octave = near-zero roughness. Out-of-tune piano strings. Distortion pedal.

**Consuming models**: BCH (brainstem consonance), SDED (dissonance detection), CSG (consonance-salience)

---

### 2. Sethares Dissonance
**R³ Index**: [1]
**Domain**: Psychoacoustic

**Physical definition**: Total dissonance across ALL partial-frequency pairs of a sound. Unlike roughness, this considers the entire harmonic structure rather than just two sinusoids. It is timbre-dependent — gamelan and Western orchestra produce different dissonance for the same interval.

**Measurement**: Sethares (1993) formula. For each partial pair (fi, fj, ai, aj): d(fi,fj) = ai·aj·[e^(-A1·s·|fj-fi|) - e^(-A2·s·|fj-fi|)]. Parameters: Dstar=0.24, A1=-3.51, A2=-5.75.

**Psychoacoustic basis**: Generalization of Helmholtz's "beating partials" concept. Instrument timbre alters the consonance of an interval.

**Sonic examples**: The same interval produces different dissonance on different instruments. Trumpet fifth vs flute fifth. Gamelan's pelog scale sounds "out of tune" in Western ears but is optimized for its own timbre.

**Consuming models**: BCH, STAI, PNH, SPU-γ3-SDED

---

### 3. Periodicity
**R³ Index**: [2]
**Domain**: Psychoacoustic

**Physical definition**: How regularly a sound's waveform repeats. Periodic sound = clear pitch. Aperiodic sound = noise. Measured via lag-1 autocorrelation.

**Measurement**: Helmholtz-Kang approach. Lag-1 autocorrelation of the mel spectrogram. High value = periodic (violin note), low value = aperiodic (thunder).

**Psychoacoustic basis**: Terhardt (1979) periodicity detection. The brain uses temporal fine structure information to extract pitch. Phase-locking is strong in periodic sounds.

**Sonic examples**: Sustained violin note = high. Drum hit = low. Human voice = medium-high. Wind = very low.

**Consuming models**: BCH, PSCL, PCCR, PNH (Pythagorean hierarchy)

---

### 4. Tonal Fusion
**R³ Index**: [3]
**Domain**: Psychoacoustic

**Physical definition**: The degree to which two simultaneous sounds are perceived as a single sound. Octave yields the highest fusion, tritone the lowest. Related to the energy ratio in the low-frequency region.

**Measurement**: Stumpf (1898) concept. Current implementation: energy ratio in the lower quarter of the mel spectrum (mel[:N/4].sum() / total). Real Parncutt subharmonic matching planned for Phase 6.

**Psychoacoustic basis**: Stumpf's Tonverschmelzung (tonal fusion) experiments. Fusion increases as intervals approach simple frequency ratios. 2:1 > 3:2 > 4:3 > ...

**Sonic examples**: Organ chord = high fusion. Cluster chord = low fusion. Unison choir = very high.

**Consuming models**: BCH, STAI, Group E interactions

---

### 5. Sensory Pleasantness
**R³ Index**: [4]
**Domain**: Psychoacoustic

**Physical definition**: The degree of pleasantness based purely on acoustic properties. Low roughness + high harmonicity + simple frequency ratios = high sensory pleasantness. This operates BEYOND cultural preferences, at the physical level.

**Measurement**: Harrison & Pearce (2020) multi-factor consonance model. Weighted combination of roughness, harmonicity, and spectral familiarity components.

**Psychoacoustic basis**: The most comprehensive model of "consonance." A composite score combining multiple components rather than a single dimension.

**Sonic examples**: Major triad = high. Minor second = low. Bell tone = high. Metal scraping = very low.

**Consuming models**: BCH, STAI, PCU models, ARU pathway

---

### 6. Inharmonicity
**R³ Index**: [5]
**Domain**: Psychoacoustic

**Physical definition**: How much a sound's partials deviate from the integer harmonic series. Harmonic sounds (violin, flute): partials = f0, 2f0, 3f0... Inharmonic sounds (bell, upper piano register): partials ≠ nf0.

**Measurement**: 1 - harmonicity[2]. Computed as the inverse of periodicity.

**Psychoacoustic basis**: Inharmonic sounds create pitch ambiguity and attract attention (ASU-IACM: P3a amplitude d=-1.37). Bells, metallophones, and gamelan instruments are naturally inharmonic.

**Sonic examples**: Violin = low (harmonic). Bell = high (inharmonic). Piano lower register = low, upper register = high.

**Consuming models**: IACM (attention capture), PNH (interval hierarchy), PSCL (pitch salience)

---

### 7. Harmonic Deviation
**R³ Index**: [6]
**Domain**: Psychoacoustic

**Physical definition**: A measure of spectral irregularity. Composite of Sethares dissonance and periodicity: 0.5×sethares + 0.5×(1-harmonicity). The overall degree of deviation from harmonic quality.

**Measurement**: Derived dimension: 0.5×[1] + 0.5×(1-[2]).

**Sonic examples**: Clean tuning = low deviation. Half-step detuning = high deviation. Detuned synthesizer = medium-high.

**Consuming models**: BCH (consonance signal output), PCU-CHPI

---

### 8. Amplitude
**R³ Index**: [7]
**Domain**: Spectral

**Physical definition**: The instantaneous energy level of the sound wave. Root Mean Square per frame. Represents the physical power of the sound — the foundation of the decibel scale.

**Measurement**: Mean energy across all frequency bins of the log-mel spectrum.

**Psychoacoustic basis**: Sound Pressure Level (SPL). The fundamental input to the ear. All auditory processing depends on the presence of this signal.

**Sonic examples**: Fortissimo = high. Pianissimo = low. Silence = zero. Explosion = maximum.

**Consuming models**: 81 models (most widely consumed R³ dimension). STU (motor coupling), ARU (arousal), MPU (movement)

---

### 9. Energy Velocity
**R³ Index**: [8]
**Domain**: Spectral

**Physical definition**: First derivative of amplitude — how fast is the energy changing? Crescendo = positive velocity. Diminuendo = negative velocity. Sustained note = near zero.

**Measurement**: Frame-to-frame amplitude difference, sigmoid normalization.

**Psychoacoustic basis**: Dynamic change perception. Crescendo creates excitement, diminuendo creates relaxation. The brain adapts to steady sound but attends to changing sound (adaptation).

**Sonic examples**: Ravel's Bolero crescendo = sustained positive velocity. Sudden sforzando = spike. Sustained note = zero.

**Consuming models**: STU (timing), ARU (affect), AMSC (motor coupling)

---

### 10. Energy Acceleration
**R³ Index**: [9]
**Domain**: Spectral

**Physical definition**: Second derivative of amplitude — the rate of change of energy change. Is the crescendo speeding up or slowing down? At the moment of an explosion: high positive acceleration, then rapid negative acceleration.

**Measurement**: Frame-to-frame difference of velocity_A, sigmoid normalization.

**Sonic examples**: Drum hit attack = high positive → high negative. Slow crescendo = low positive. Steady sound = zero.

**Consuming models**: STU (beat detection), MPU (motor planning), ARU (arousal prediction)

---

### 11. Loudness
**R³ Index**: [10]
**Domain**: Spectral

**Physical definition**: Perceived sound intensity. NOT the same as amplitude — the human ear shows frequency-dependent sensitivity (Fletcher-Munson curves). Most sensitive at 3-4 kHz, less sensitive at low and very high frequencies.

**Measurement**: Stevens' power law: loudness ∝ (intensity)^0.3. Sone units. Current implementation has a double-compression bug (to be fixed in Phase 6).

**Psychoacoustic basis**: Stevens (1957) power law. ISO 226 equal-loudness contours. Weber-Fechner law.

**Sonic examples**: 1 kHz at 40 dB = 1 sone (reference). At the same dB, bass guitar is perceived as quieter. Baby cry (3 kHz) has high loudness even at low dB.

**Consuming models**: ARU (affect), AMSC (motor drive), HTP (prediction), STU (all models)

---

### 12. Onset Strength
**R³ Index**: [11]
**Domain**: Spectral

**Physical definition**: The energy rise at the beginning of a new sound event. Half-wave rectified version of spectral flux — counts only increasing energy. Every drum hit, every note onset, every consonant is an onset.

**Measurement**: HWR(spectral_flux) = max(0, flux). Weineck (2022) neural synchronization driver.

**Psychoacoustic basis**: Onset neurons in the auditory cortex. A new sound event triggers phase-locking. The raw material of beat perception.

**Sonic examples**: Drum kit = very high onset strength. Harp glissando = low. Pad synth = very low. Staccato = high, legato = low.

**Consuming models**: Group G (rhythm) dependency. STU beat entrainment. SNEM (neural entrainment). PEOM (period locking).

---

### 13. Warmth
**R³ Index**: [12]
**Domain**: Spectral

**Physical definition**: The proportion of energy in the lower frequency region of the spectrum. Dominance of low harmonics. The "warm" sound of tube amplifiers = boosted low harmonics.

**Measurement**: Total energy in the lower quarter of the mel spectrum / total energy.

**Psychoacoustic basis**: Low-frequency energy is described as "full, soft, warm." One of the timbral dimensions (McAdams 1995, Grey 1977).

**Sonic examples**: Cello = high warmth. Piccolo = low warmth. Double bass = very high. Cymbal = low.

**Consuming models**: SPU-TSCP (timbre plasticity), MEAMN (nostalgia trigger), ARU (valence)

---

### 14. Sharpness
**R³ Index**: [13]
**Domain**: Spectral

**Physical definition**: The proportion of energy in the upper frequency region of the spectrum. The inverse of warmth. Sharp, bright, piercing sounds show high sharpness.

**Measurement**: Energy ratio in the upper quarter of the mel spectrum. (A more accurate implementation using DIN 45692 Zwicker sharpness is at [122].)

**Psychoacoustic basis**: Zwicker & Fastl (1999). Acum units. Weighted spectral centroid on the Bark scale.

**Sonic examples**: Cymbal = high. Double bass = low. Trumpet ff = high. Flute pp = medium-low.

**Consuming models**: SPU-TSCP, STAI (aesthetic), ARU (arousal marker)

---

### 15. Tonalness
**R³ Index**: [14]
**Domain**: Spectral

**Physical definition**: How "tonal" (pitch-salient) a sound is — noise or tone? Measured by the dominance of spectral peaks. High tonalness = prominent harmonic structure. Low = noise-like.

**Measurement**: Terhardt (1979) proxy. Spectral peak-to-valley ratio.

**Psychoacoustic basis**: The auditory system separates tonal and noise components. Tonal components contribute to pitch, noise components contribute to timbre/texture perception.

**Sonic examples**: Flute = very high tonalness. Whisper = very low. Violin = high. Waterfall = low. Bongo = medium.

**Consuming models**: SPU (pitch processing), STANM (attention), PCU (prediction)

---

### 16. Spectral Centroid
**R³ Index**: [15]
**Domain**: Spectral

**Physical definition**: The "center of gravity" of the spectrum — where on the frequency axis the energy is concentrated. Directly related to brightness. High centroid = bright sound. Low centroid = dark sound.

**Measurement**: Σ(fi × ai) / Σ(ai), normalized on the mel frequency axis.

**Psychoacoustic basis**: The strongest dimension in McAdams (1995) timbre research. MPEG-7 audio descriptor. Used in ASA (Auditory Scene Analysis) source identification.

**Sonic examples**: Trumpet ff = high centroid (~3000 Hz). Double bass = low centroid (~200 Hz). "Wah" pedal = varying centroid.

**Consuming models**: SPU, STAI (aesthetic), PCU-CHPI (cross-modal), TSCP (timbre identity)

---

### 17. Spectral Smoothness
**R³ Index**: [16]
**Domain**: Spectral

**Physical definition**: How smooth/regular the spectral envelope is. Smooth spectral envelope = soft sound (flute). Irregular envelope = rough sound (oboe, bağlama).

**Measurement**: 1 - sethares_dissonance[1]. Currently computed as the inverse of the Sethares proxy.

**Psychoacoustic basis**: Krimphoff et al. (1994) spectral irregularity. An important dimension in timbre perception.

**Sonic examples**: Flute = high smoothness. Oboe = low (strong harmonic peaks). Synthesizer sawtooth wave = medium.

**Consuming models**: SPU (timbre), PCU-CHPI

---

### 18. Spectral Autocorrelation
**R³ Index**: [17]
**Domain**: Spectral

**Physical definition**: The periodicity within the spectrum itself — how prominent are the regularly spaced peaks of the harmonic series? Lag-1 autocorrelation is equivalent to temporal periodicity.

**Measurement**: Lag-1 spatial autocorrelation of the mel spectrum.

**Psychoacoustic basis**: Harmonic structure detection. Harmonic sounds have high spectral autocorrelation (evenly spaced peaks).

**Sonic examples**: Violin = high. Noise = low. Bell = medium (inharmonic but structured).

**Note**: Identical to [2] helmholtz_kang. To be replaced with spectral_kurtosis in Phase 6.

---

### 19. Tristimulus 1
**R³ Index**: [18]
**Domain**: Spectral

**Physical definition**: Ratio of the fundamental frequency (f0) energy to total spectral energy. Pollard-Jansson (1982) timbre model. What RGB is to visual color, tristimulus is to sound — the "color" components of a sound.

**Measurement**: Energy ratio in the lowest region of the mel spectrum (f0 proxy).

**Psychoacoustic basis**: Pollard & Jansson (1982). Tristimulus representation: T1=fundamental, T2=midrange, T3=highs. A powerful feature for instrument recognition.

**Sonic examples**: Flute = high T1 (strong fundamental). Oboe = low T1 (weak fundamental, strong harmonics). Clarinet = high T1 (odd harmonics dominant).

**Consuming models**: SPU-TSCP (instrument identification), SPU-MIAA (imagery)

---

### 20. Tristimulus 2
**R³ Index**: [19]
**Domain**: Spectral

**Physical definition**: Ratio of mid-range harmonics (around 2f0-4f0) to total energy. The "body" of the sound — neither too bright nor too dark.

**Measurement**: Energy ratio in the mid region of the mel spectrum.

**Sonic examples**: Human voice = high T2 (formant region). Piano = balanced T2. Tuba = low T2.

**Consuming models**: SPU-TSCP, timbre profile together with Group J

---

### 21. Tristimulus 3
**R³ Index**: [20]
**Domain**: Spectral

**Physical definition**: Ratio of high harmonics (5f0+) to total energy. The "brilliance" component of the sound. High T3 = metallic, bright. Low T3 = soft, dark.

**Measurement**: Energy ratio in the upper region of the mel spectrum.

**Sonic examples**: Trumpet ff = high T3. Flute = low T3. Xylophone = high T3. Double bass pizzicato = low T3.

**Consuming models**: SPU-TSCP, STAI (aesthetic integration)

---

### 22. Spectral Flux
**R³ Index**: [21]
**Domain**: Temporal

**Physical definition**: The amount of spectral change from frame to frame. Measured as L2 (Euclidean) norm. High flux = sound is changing rapidly (transitions, new notes). Low flux = stable sound.

**Measurement**: ||mel(t) - mel(t-1)||₂ / N_bins.

**Psychoacoustic basis**: Change detection. The auditory system adapts to steady signals — changing signals attract attention.

**Sonic examples**: Fast arpeggiation = high flux. Long organ note = low flux. Percussion = spikes. Atmospheric pad = low.

**Consuming models**: All Group D consumers (57 models). NDU (novelty), STU (timing), PCU (prediction error)

---

### 23. Distribution Entropy
**R³ Index**: [22]
**Domain**: Temporal

**Physical definition**: Shannon entropy of the spectral energy distribution. High entropy = energy is evenly distributed (noise-like, white noise = maximum). Low entropy = energy is concentrated in a few points (pure tone = minimum).

**Measurement**: H = -Σ p(i)·log₂(p(i)), where p(i) = mel(i) / Σmel.

**Sonic examples**: White noise = maximum entropy. Sine tone = minimum. Orchestral tutti = high. Solo flute = low.

**Consuming models**: NDU (deviance), STU (context), PWSM (salience)

---

### 24. Distribution Flatness
**R³ Index**: [23]
**Domain**: Temporal

**Physical definition**: Geometric mean / arithmetic mean ratio. MPEG-7 spectral flatness. 1.0 = perfectly flat (white noise). 0.0 = perfectly concentrated (pure tone). A measure of tonality/noise ratio.

**Measurement**: (∏ mel(i))^(1/N) / (Σ mel(i) / N).

**Psychoacoustic basis**: Equivalent to Wiener entropy. Standard for audio quality classification (tonal vs noise).

**Sonic examples**: Wind = high flatness. Violin = low. Traffic noise = medium-high. Ney flute = low.

**Consuming models**: ASU (salience), NDU (deviance)

---

### 25. Distribution Concentration
**R³ Index**: [24]
**Domain**: Temporal

**Physical definition**: Spectral energy concentration measured by Herfindahl-Hirschman Index. How few frequency bands is energy concentrated in? High = monopoly (single frequency). Low = dispersed (noise).

**Measurement**: HHI = Σ p(i)². Normalization bug exists (to be fixed in Phase 6).

**Sonic examples**: Sine tone = maximum concentration. Orchestral tutti = low. Solo instrument = medium-high.

**Consuming models**: NDU, PCU, ASU

---

### 26. Energy × Consonance Interaction
**R³ Index**: [25:33] (8D)
**Domain**: CrossDomain

**Physical definition**: Cross-products between amplitude/velocity/loudness and roughness/dissonance/harmonicity. Answers: "How dissonant is a loud sound?" High energy + high roughness = very disturbing.

**Measurement**: Group B × Group A pairwise products (8 combinations).

**Sonic examples**: Forte dissonant chord = high. Piano consonant chord = low. Fortissimo trumpet cluster = very high.

**Consuming models**: 54 models (Group E). PCU, ARU, RPU dominant consumers.

---

### 27. Change × Consonance Interaction
**R³ Index**: [33:41] (8D)
**Domain**: CrossDomain

**Physical definition**: Cross-products between spectral change and consonance. "Does consonance also change when the sound changes?" High during chord transitions: both the spectrum and the harmonic relationship change.

**Measurement**: Group D × Group A pairwise products.

**Sonic examples**: Transition from dissonant chord to consonant chord (resolution) = high. Steady consonant sound = low.

---

### 28. Consonance × Timbre Interaction
**R³ Index**: [41:49] (8D)
**Domain**: CrossDomain

**Physical definition**: Cross-products between consonance properties and timbre properties. "Is a warm sound's consonance different from a cold sound's?" Sethares' core insight: timbre changes consonance.

**Measurement**: Group A × Group C pairwise products.

**Sonic examples**: Warm cello fifth vs sharp trumpet fifth. Same interval, different timbre → different interaction.

---

### 29. Chroma
**R³ Index**: [49:61] (12D)
**Domain**: Tonal

**Physical definition**: Energy distribution across all 12 pitch classes (C, C#, D, ..., B) folded across all octaves. Octave equivalence: C2, C3, C4 are all summed as "C." A moment's "tonal fingerprint."

**Measurement**: Mel → exp → 128×12 Gaussian soft-assignment matrix → L1 norm. (CQT-based chroma is more precise but mel approximation works.)

**Psychoacoustic basis**: Shepard (1964) octave equivalence. Krumhansl (1990) tonal hierarchy. Pitch class perception is fundamental to the human auditory system.

**Sonic examples**: C major chord = high energy in C, E, G channels. G dominant = G, B, D. Chromatic passage = all 12 channels equal.

**Consuming models**: PCCR (pitch class), MDNS (melody), MSPBA (syntax), Group H (harmony dependency), Group I (entropy dependency)

---

### 30. Pitch Height
**R³ Index**: [61]
**Domain**: Tonal

**Physical definition**: Absolute height of perceived pitch — low or high? Unlike chroma, this preserves octave information: C2 ≠ C4. Logarithmic per the Weber-Fechner law: the 100→200 Hz difference is perceptually as large as 1000→2000 Hz.

**Measurement**: log₂(f0_estimate) normalized.

**Psychoacoustic basis**: Weber-Fechner (1860). Pitch perception is logarithmic. Each octave spans equal perceptual distance.

**Sonic examples**: Double bass = low pitch height. Piccolo = high. Baritone voice = medium-low. Soprano = medium-high.

**Consuming models**: PSCL, SPH (spatiotemporal prediction), MPG (melodic gradient)

---

### 31. Pitch Class Entropy
**R³ Index**: [62]
**Domain**: Tonal

**Physical definition**: Shannon entropy of the 12 chroma channels. Across how many different pitch classes is energy spread? High entropy = many notes active (chromatic, cluster). Low entropy = few notes active (unison, octave).

**Measurement**: H = -Σ chroma(i)·log₂(chroma(i)), over [49:61].

**Sonic examples**: Solo melody = low entropy. Ligeti cluster = high. Tonal chord = medium. 12-tone row = maximum.

**Consuming models**: PCCR, Group I (information dependency)

---

### 32. Pitch Salience
**R³ Index**: [63]
**Domain**: Tonal

**Physical definition**: How salient (prominent) the perceived pitch is. Strong pitch perception = high salience (violin note). Weak/ambiguous pitch = low salience (drum, noise). Virtual pitch concept: pitch inferred from harmonics even when the fundamental is physically absent.

**Measurement**: Parncutt (1989) approach. Max/mean ratio of the chroma vector.

**Psychoacoustic basis**: Terhardt (1979) virtual pitch. Parncutt (1989) pitch salience model. "Missing fundamental" phenomenon: you perceive 100 Hz pitch on a telephone even though it cuts off below 300 Hz.

**Sonic examples**: Sustained violin note = very high. Bass drum = low. Human voice = high. Water sound = low.

**Consuming models**: PSCL (cortical localization), SDNPS (neural pitch salience), BCH (brainstem)

---

### 33. Inharmonicity Index
**R³ Index**: [64]
**Domain**: Tonal

**Physical definition**: Unlike [5] inharmonicity, this is a harmonic series deviation measure derived directly from pitch/chroma information. Quantifies how much partials deviate from nf0.

**Measurement**: Deviation of the chroma distribution from the harmonic template.

**Sonic examples**: Similar to [6] but a more precise measurement based on Group F's pitch information.

**Consuming models**: IACM (P3a attention capture), PNH (Pythagorean ratios)

---

### 34. Tempo Estimate
**R³ Index**: [65]
**Domain**: Temporal

**Physical definition**: The perceived beat rate (BPM) of the sound. Autocorrelation of the onset strength signal detects the dominant periodicity. Human preference is ~120 BPM (Fraisse 1982).

**Measurement**: onset_strength[11] → autocorrelation → dominant peak → BPM → [0,1] normalized (30-300 BPM range).

**Psychoacoustic basis**: Fraisse (1982) natural tempo ~2 Hz. London (2012) metric perception limits: ~30-300 BPM.

**Sonic examples**: Allegro = ~0.7 (140 BPM). Adagio = ~0.3 (60 BPM). Free tempo rubato = unstable/varying.

**Consuming models**: STU (12/14 models), MPU (9/10 models), PEOM (period entrainment), EDTA (tempo accuracy)

---

### 35. Beat Strength
**R³ Index**: [66]
**Domain**: Temporal

**Physical definition**: How strong/prominent the perceived beat is. Regular drum pattern = high beat strength. Rubato violin = low. The peak value of the onset autocorrelation.

**Measurement**: Height of the autocorrelation peak at the tempo estimate.

**Sonic examples**: Pop/rock drum kit = very high. Solo piano Chopin rubato = low. March = high.

**Consuming models**: SNEM (entrainment), HGSIC (groove), OMS (motor sync)

---

### 36. Pulse Clarity
**R³ Index**: [67]
**Domain**: Temporal

**Physical definition**: How "clear" the beat is — is there a single dominant period or multiple competing periods? High clarity = single unambiguous beat. Low = ambiguous, multiple metric interpretations possible.

**Measurement**: Witek (2014) groove connection. Autocorrelation peak sharpness.

**Psychoacoustic basis**: Witek et al. (2014): Medium syncopation produces the highest groove. Too clear a beat = boring. Too ambiguous = confusing.

**Sonic examples**: Metronome = maximum clarity. Free jazz = low. Funk = medium (syncopation creates ambiguity but the beat is felt).

**Consuming models**: HGSIC, BARM (beat ability), ETAM (attention modulation)

---

### 37. Syncopation Index
**R³ Index**: [68]
**Domain**: Temporal

**Physical definition**: The degree of conflict between rhythmic accents and the metric grid. Silence on strong beats + accents on weak beats = syncopation. The defining feature of funk, reggae, and jazz.

**Measurement**: Longuet-Higgins & Lee (1984) LHL model. Inverse correlation between metric weight and onset strength.

**Psychoacoustic basis**: Witek (2014): syncopation ∝ groove (inverted-U). Grahn & Brett (2007): syncopation increases putamen/SMA activation.

**Sonic examples**: "The One" funk groove = high syncopation. March = low. Bossa nova = medium. Off-beat ska = high.

**Consuming models**: 17 models demand this (Tier 1). PEOM, MSR, GSSM, HMCE, EDTA, ETAM, HGSIC, OMS, RASN, SNEM...

---

### 38. Metricality Index
**R³ Index**: [69]
**Domain**: Temporal

**Physical definition**: How well the rhythmic structure conforms to integer-ratio regularity. High metricality = regular 4/4 or 3/4 is felt. Low = free rhythm, changing meters, asymmetric structures.

**Measurement**: Grahn & Brett (2007). Integer-ratio proximity between onset timings.

**Psychoacoustic basis**: Metric sounds activate the putamen and SMA (Grahn & Brett 2007 N=27 fMRI). The motor system locks onto metric structure.

**Sonic examples**: 4/4 rock = high. 7/8 Balkan = medium. Gregorian chant = low. Cage aleatoric = very low.

**Consuming models**: 14 models (Tier 1). STU and MPU dominant consumers.

---

### 39. Isochrony
**R³ Index**: [70]
**Domain**: Temporal

**Physical definition**: How equal successive inter-onset intervals (IOIs) are. nPVI = 0 → perfectly equal intervals (isochronous). High nPVI → irregular, variable intervals. A metric transferred from speech prosody research to music.

**Measurement**: Ravignani (2021), Grabe & Low (2002). nPVI = 100 × (1/(n-1)) × Σ |IOI_k - IOI_{k+1}| / ((IOI_k + IOI_{k+1})/2).

**Psychoacoustic basis**: Rhythmic regularity perception. Isochronous rhythms facilitate entrainment. Used in human language vs birdsong comparisons.

**Sonic examples**: Metronome = minimum nPVI (perfect isochrony). Speech = medium. Swing jazz = high. Rubato = very high.

**Consuming models**: CSSL (cross-species), RIRI (rehabilitation), RASN, OMS, AMSC

---

### 40. Groove Index
**R³ Index**: [71]
**Domain**: Temporal

**Physical definition**: A sound's capacity to induce the urge to move. Composite of syncopation, bass energy, metricality, and beat strength. The acoustic answer to "Does this music make you want to dance?"

**Measurement**: Madison (2006), Janata (2012). Syncopation × beat_strength × warmth composite.

**Psychoacoustic basis**: Witek (2014) inverted-U: medium syncopation + strong bass = maximum groove. Dorsal auditory-motor pathway activation.

**Sonic examples**: James Brown "Funky Drummer" = very high. Chopin Nocturne = low. Drum'n'bass = high. Gregorian hymn = very low.

**Consuming models**: HGSIC, RIRI, GSSM, MPFS (flow state), SSRI

---

### 41. Event Density
**R³ Index**: [72]
**Domain**: Temporal

**Physical definition**: Number of auditory events per unit time. Fast passage = high density. Long notes = low. Temporal density of onsets.

**Measurement**: Proportion of frames where onset_strength[11] > threshold, per window.

**Sonic examples**: Liszt La Campanella fast section = very high. Bruckner adagio = low. Drum solo = high. Drone music = very low.

**Consuming models**: STU (context), MPU (motor planning), IUCP (complexity)

---

### 42. Tempo Stability
**R³ Index**: [73]
**Domain**: Temporal

**Physical definition**: How constant the tempo remains over time. Metronome = maximum stability. Rubato = low. Accelerando/ritardando = transient drop.

**Measurement**: Inverse of the running variance of the tempo estimate.

**Sonic examples**: Electronic music (click track) = maximum. Live orchestra = medium. Aleatoric music = low.

**Consuming models**: PEOM (period entrainment), EDTA (tempo accuracy), HTP (prediction)

---

### 43. Rhythmic Regularity
**R³ Index**: [74]
**Domain**: Temporal

**Physical definition**: Regularity of the IOI (Inter-Onset Interval) distribution. An IOI-statistics-based version of isochrony_nPVI. Regular = low variety. Irregular = many different intervals.

**Measurement**: Spiech (2022) inverse IOI entropy.

**Sonic examples**: Military march = high regularity. Jazz improv = low. Minimalist music = very high.

**Consuming models**: STU, MPU, RASN (neuroplasticity)

---

### 44. Key Clarity
**R³ Index**: [75]
**Domain**: Tonal

**Physical definition**: The degree to which a moment belongs to a specific tonal center (key). High = clear tonality present (C major, D minor). Low = atonal, multi-tonal, or ambiguous.

**Measurement**: Krumhansl & Kessler (1982) key profiles correlated with chroma vector. Maximum correlation across all 24 major/minor profiles.

**Psychoacoustic basis**: Krumhansl (1990) tonal hierarchy: tonic > dominant > mediant > others. Probe-tone experiments.

**Sonic examples**: Mozart sonata = high key clarity. Schoenberg 12-tone = low. Modulation moment = transient drop.

**Consuming models**: UDP (uncertainty pleasure), MEAMN (tonal trajectory), STAI (aesthetic), CHPI, SLEE

---

### 45-50. Tonnetz Coordinates (6D)
**R³ Index**: [76:82]
**Domain**: Tonal

**Physical definition**: Projection of the chroma vector onto a 6-dimensional tonal space. Euler's Tonnetz grid: circles of fifths, minor thirds, and major thirds as coordinate axes. Each axis represents a tonal relationship dimension.

**Measurement**: Harte (2006), Balzano (1980). Chroma × trigonometric projection matrix. Natural range [-1, 1], normalized to [0, 1] in R³.

**Psychoacoustic basis**: Neo-Riemannian theory. Tonal harmony can be modeled as movement in a geometric space.

**Sonic examples**: C major → G major transition = movement along the fifth axis. C major → A minor = movement along the minor axis. Chromatic mediant = jump on the major axis.

**Consuming models**: STAI (aesthetic), CHPI (cross-modal harmonic), BCH (brainstem harmony)

---

### 51. Voice Leading Distance
**R³ Index**: [82]
**Domain**: Tonal

**Physical definition**: How little the notes move between successive chords. Small distance = smooth voice leading (Bach chorale). Large distance = leaping transitions.

**Measurement**: Tymoczko (2011) voice-leading parsimony. Frame-to-frame chroma difference norm.

**Sonic examples**: Bach chorale = low distance (each voice moves minimally). Stravinsky = high. Plagal cadence (IV→I) = low.

**Consuming models**: PCU (prediction), MSPBA (syntax), NDU (deviance)

---

### 52. Harmonic Change
**R³ Index**: [83]
**Domain**: Tonal

**Physical definition**: How rapidly the harmonic structure changes. Harmonic Change Detection Function. Every chord transition produces an HCDF spike. The tonal version of spectral flux.

**Measurement**: Frame-to-frame tonnetz Euclidean distance.

**Sonic examples**: Rapid chord changes (Giant Steps) = high. Improvisation over a single chord = low. Modulation moment = spike.

**Consuming models**: PCU, NDU (novelty), independent dimension of Group H

---

### 53. Tonal Stability
**R³ Index**: [84]
**Domain**: Tonal

**Physical definition**: How constant the tonal center remains over time. Composite of key_clarity × (1 - harmonic_change). High = staying in the same tonality for a long time. Low = constant modulation.

**Measurement**: Running average key_clarity × inverse harmonic_change.

**Sonic examples**: Folk song in one key = high. Wagner chromaticism = low. Pop verse = high, bridge = drop.

**Consuming models**: UDP (key_clarity demand), MEAMN, STAI, CHPI, SLEE

---

### 54. Diatonicity
**R³ Index**: [85]
**Domain**: Tonal

**Physical definition**: How closely the notes used conform to a diatonic (7-note scale) framework. High = diatonic (major/minor scale). Low = chromatic (all 12 notes used equally). Tymoczko's macroharmony concept.

**Measurement**: Tymoczko (2011). Fit of the chroma vector to the best-matching 7-note subset.

**Sonic examples**: "Twinkle Twinkle" = very high diatonicity. Messiaen modes of limited transposition = medium. Penderecki = low.

**Consuming models**: PCU, NDU, IMU (syntax)

---

### 55. Syntactic Irregularity
**R³ Index**: [86]
**Domain**: Tonal

**Physical definition**: How much the harmonic progression deviates from tonal grammar rules. Lerdahl (2001) tonal tension model. A Neapolitan chord where unexpected = high irregularity. V→I cadence = low (rule-conforming).

**Measurement**: Lerdahl (2001) tension model approach. Difference between expected chord transition probability and actual transition.

**Psychoacoustic basis**: Koelsch (2001) mERAN response: harmonic syntax violations activate Broca's area (BA 44). Music grammar = language grammar-like mechanism.

**Sonic examples**: V→I = low irregularity. Neapolitan 6th = high. Tritone substitution = medium. Random chord sequence = very high.

**Consuming models**: MSPBA (Broca's area syntax), SDD, CDMR, SLEE, PMIM — 5+ models demand this

---

### 56. Melodic Entropy
**R³ Index**: [87]
**Domain**: Information

**Physical definition**: How predictable melodic transitions are. How much "surprise" is there as one note transitions to the next? Low entropy = predictable melody (repeating motif). High = unexpected leaps.

**Measurement**: Pearce (2005) IDyOM approach. Running entropy estimate of chroma transition probabilities: H = -Σ P(note_t | context)·log₂P(note_t | context).

**Psychoacoustic basis**: Information theory + music perception. Huron (2006) ITPRA model. The "sweet spot" = medium surprise level produces the most pleasure.

**Sonic examples**: "Happy Birthday" = low. Schoenberg = high. Jazz improvisation = medium-high. Minimalist repetition = very low.

**Consuming models**: **18 models** (highest demand). LDAC, IUCP, RPEM, SSPS, MCCN, SSRI, UDP, HTP, ICEM, WMED, CHPI, PMIM, HCMC, MSPBA, SDD, CDMR, SLEE, PUPF

---

### 57. Harmonic Entropy
**R³ Index**: [88]
**Domain**: Information

**Physical definition**: Predictability of chord transitions. How much surprise is there as one chord transitions to the next? V→I = low surprise (expected). bVI→I = high surprise (deceptive cadence).

**Measurement**: Gold (2019). Frame-to-frame chroma KL-divergence: KL(chroma_t || chroma_{t-1}).

**Psychoacoustic basis**: Cheung (2019) uncertainty × surprise = pleasure. Harmonic surprise correlates with NAcc dopamine release.

**Sonic examples**: I-IV-V-I = low. Giant Steps = high. Deceptive cadence = spike. Pedal point = very low.

**Consuming models**: **13 models**. LDAC, IUCP, SSPS, MCCN, UDP, HTP, ICEM, CHPI, MSPBA, PMIM, HCMC, SDD, CDMR

---

### 58. Rhythmic Information Content
**R³ Index**: [89]
**Domain**: Information

**Physical definition**: How much surprise the rhythmic events carry. Regular beat = low IC. Syncopation = high IC. Unexpected odd meter = very high IC.

**Measurement**: Spiech (2022). Shannon information content of onset timing: IC = -log₂P(onset_t | metric_position).

**Sonic examples**: Metronome = minimum IC. Off-beat accent = high. Polyrhythm = very high.

**Consuming models**: **8 models**. SSRI, IUCP, LDAC, RPEM, SSPS, PEOM, GSSM, HGSIC

---

### 59. Spectral Surprise
**R³ Index**: [90]
**Domain**: Information

**Physical definition**: How unexpected a frame's spectral content is compared to preceding frames. Friston free energy framework. The brain continuously predicts "what will the next frame be?" — prediction error = surprise.

**Measurement**: Frame-to-frame mel KL-divergence, normalized with running average.

**Sonic examples**: Sudden instrument change = spike. Steady texture = low. New section onset = high.

**Consuming models**: PCU (prediction), NDU (novelty), independent dimension of Group I

---

### 60. Information Rate
**R³ Index**: [91]
**Domain**: Information

**Physical definition**: How much new information is transmitted per unit time. Mutual information per frame. Dense, rapidly changing music = high rate. Repetitive drone = low.

**Measurement**: Weineck (2022). Mutual information estimate between frame pairs.

**Sonic examples**: Bebop = high rate. Ambient = low. Speech = medium. Silence = zero.

**Consuming models**: PCU, NDU, RPU (reward sensitivity to information)

---

### 61. Predictive Entropy
**R³ Index**: [92]
**Domain**: Information

**Physical definition**: How uncertain the next frame is. Entropy of the conditional probability distribution. High = many possible continuations. Low = a single clear expected continuation.

**Measurement**: Running conditional entropy: H(frame_t | frame_{t-k:t-1}).

**Sonic examples**: Pre-cadence = low (V→I expected). Open-form moment = high. Post-fermata = high.

**Consuming models**: HTP (hierarchical prediction), ICEM (IC→emotion), UDP (uncertainty pleasure), PWUP, WMED

---

### 62. Tonal Ambiguity
**R³ Index**: [93]
**Domain**: Information

**Physical definition**: The state of multiple tonal centers being equally probable. Entropy of chroma correlations with Krumhansl key profiles. High = many keys equally plausible (tonal ambiguity). Low = single dominant key.

**Measurement**: Entropic inverse of key_clarity. H = -Σ corr(chroma, key_i)·log₂(corr) for all 24 keys.

**Sonic examples**: Chopin chromatic passage = high ambiguity. C major scale = low. Debussy whole-tone = high. Tritone = very high.

**Consuming models**: PCU, NDU (perceptual ambiguity demand), SLEE

---

### 63. MFCC Coefficients
**R³ Index**: [94:107] (13D)
**Domain**: Spectral

**Physical definition**: Cepstral (inverse-spectral) representation of the spectral envelope. 13 coefficients compactly encode the "shape" of a sound. The foundational feature for speech recognition, music information retrieval, and instrument identification.

- **MFCC 1**: Overall energy distribution (bright vs dark)
- **MFCC 2**: Spectral slope (falling vs rising)
- **MFCC 3-4**: Broad spectral shape variations
- **MFCC 5-8**: Mid-scale spectral detail
- **MFCC 9-13**: Fine spectral structure (formant-like detail)

**Measurement**: mel → log → DCT (Discrete Cosine Transform). Pre-computed 128×13 DCT matrix.

**Psychoacoustic basis**: Davis & Mermelstein (1980). The mel scale models human auditory frequency resolution. Cepstral decomposition approximates the source-filter model.

**Sonic examples**: Each instrument has a characteristic MFCC profile. Violin ≠ flute ≠ oboe. Different MFCCs at the same pitch = different timbre.

**Consuming models**: SPU-TSCP (timbre identity), SPU-MIAA (imagery), SPU-ESME (MMN)

---

### 64. Spectral Contrast
**R³ Index**: [107:114] (7D)
**Domain**: Spectral

**Physical definition**: The difference between spectral peaks and valleys in each octave sub-band. High contrast = prominent harmonic peaks (tonal sound). Low contrast = flat spectrum (noise-like). 7 octave bands:

- **Band 1**: ~50-100 Hz (sub-bass)
- **Band 2**: ~100-200 Hz (bass)
- **Band 3**: ~200-400 Hz (lower midrange)
- **Band 4**: ~400-800 Hz (midrange)
- **Band 5**: ~800-1600 Hz (upper midrange)
- **Band 6**: ~1600-3200 Hz (presence)
- **Band 7**: ~3200+ Hz (brilliance/residual)

**Measurement**: Jiang (2002). Per octave band: sort → top 20% quantile - bottom 20% quantile.

**Sonic examples**: Orchestral tutti = high contrast (strong harmonics). Pink noise = low. Solo oboe = high in Bands 4-5.

**Consuming models**: SPU-TSCP, complementary to Group J timbre profile

---

### 65. Temporal Modulation Spectrum
**R³ Index**: [114:120] (6D)
**Domain**: Psychoacoustic

**Physical definition**: The modulation frequency distribution of the sound's energy envelope. 6 bands:

- **0.5 Hz** [114]: Phrase-level modulation (breathing cycles, long crescendo)
- **1 Hz** [115]: Walking-pace modulation (slow tempo)
- **2 Hz** [116]: Beat-rate modulation (~120 BPM = natural tempo)
- **4 Hz** [117]: Speech syllable rate / strong beat subdivision
- **8 Hz** [118]: Rapid articulation / tremolo
- **16 Hz** [119]: Roughness threshold / upper limit of vibrato

**Measurement**: Chi & Shamma (2005) cortical modulation model. Sliding-window FFT (344 frame window, 86 hop, 512 FFT).

**Psychoacoustic basis**: The auditory cortex is tonotopically organized by modulation frequency. 4 Hz = optimal point for speech perception.

**Sonic examples**: Pop song = 2 Hz and 4 Hz dominant. Tremolo strings = 8 Hz spike. Slow doom metal = 0.5-1 Hz. Fast techno = 2-4 Hz.

**Consuming models**: Primary dimension of Group K

---

### 66. Modulation Centroid
**R³ Index**: [120]
**Domain**: Psychoacoustic

**Physical definition**: Center of gravity of the modulation spectrum — the dominant modulation rate. High centroid = fast modulations dominant (tremolo, rapid articulation). Low centroid = slow modulations dominant (crescendo, phrase structure).

**Measurement**: Weighted average: Σ(f_mod × power) / Σ(power).

**Sonic examples**: Vivaldi presto = high modulation centroid. Barber Adagio = low. Trill = high.

---

### 67. Modulation Bandwidth
**R³ Index**: [121]
**Domain**: Psychoacoustic

**Physical definition**: How diverse the modulation rates are. Wide band = multiple temporal scales active. Narrow band = single dominant modulation rate.

**Measurement**: Weighted standard deviation: σ_mod.

**Sonic examples**: Orchestral tutti = wide bandwidth. Solo tremolo = narrow. Polyrhythmic ensemble = wide.

---

### 68. Zwicker Sharpness
**R³ Index**: [122]
**Domain**: Psychoacoustic

**Physical definition**: DIN standard version of [13] sharpness. Bark-scale rebanding + Zwicker weighting function. Industry-standard perceptual sharpness measure. Acum units.

**Measurement**: DIN 45692. Mel → Bark rebinning → Zwicker weighting function → acum.

**Psychoacoustic basis**: Zwicker & Fastl (1999). 1 acum = 1 kHz narrowband noise at 60 dB.

**Sonic examples**: Similar to [13] but standards-based, more reliable.

---

### 69. Fluctuation Strength
**R³ Index**: [123]
**Domain**: Psychoacoustic

**Physical definition**: Temporal fluctuation strength at ~4 Hz. The human auditory system is most sensitive to energy fluctuations at this rate (speech syllable rate). Vacil units.

**Measurement**: Zwicker & Fastl (1999). Based on modulation_4Hz[117], weighted on the Bark scale.

**Psychoacoustic basis**: Fluctuation strength = maximum at ~4 Hz modulation. 4 Hz = speech syllabic rate = optimal temporal resolution.

**Sonic examples**: Vibrato (5-7 Hz) = medium. Tremolo (3-4 Hz) = high. Steady sound = low. Speech = high.

---

### 70. Loudness A-weighted
**R³ Index**: [124]
**Domain**: Psychoacoustic

**Physical definition**: Loudness with ISO 226 frequency weighting applied. Compensates for the human ear's frequency-dependent sensitivity. Unlike [10] loudness: the A-curve applies strong attenuation at low frequencies.

**Measurement**: ISO 226 A-weighting curve applied to total energy.

**Sonic examples**: At the same dB, bass guitar vs piccolo → piccolo has higher A-weighted loudness.

---

### 71. Alpha Ratio
**R³ Index**: [125]
**Domain**: Psychoacoustic

**Physical definition**: Energy ratio of 0-1 kHz to 1-5 kHz. Low/high band energy balance. Used in voice quality assessment. eGeMAPS (extended Geneva Minimalistic Acoustic Parameter Set) standard.

**Measurement**: Eyben (2015). sum(energy 0-1kHz) / sum(energy 1-5kHz).

**Sonic examples**: Bass-heavy mix = high alpha ratio. Bright treble mix = low. Human voice = ~1.0.

---

### 72. Hammarberg Index
**R³ Index**: [126]
**Domain**: Psychoacoustic

**Physical definition**: Difference between peak energy in the 0-2 kHz band and peak energy in the 2-5 kHz band. A measure of spectral slope/tilt. eGeMAPS standard.

**Measurement**: max(energy 0-2kHz) - max(energy 2-5kHz), in dB.

**Psychoacoustic basis**: Speech pathology and voice quality assessment. In music: instrument source classification.

**Sonic examples**: Soft flute = high Hammarberg (low frequencies dominant). Sharp bell = low (high frequencies dominant).

---

### 73. Spectral Slope
**R³ Index**: [127]
**Domain**: Psychoacoustic

**Physical definition**: The slope of the spectral envelope in the 0-500 Hz region. Falling slope = normal speech/music. Rising slope = weak low frequencies (telephone sound). eGeMAPS standard.

**Measurement**: Linear regression slope of mel bins in 0-500 Hz.

**Sonic examples**: Rich bass = flat/gentle slope. Thin/tinny sound = steeply falling slope.

---

## Summary Statistics

| Domain | Dimension Count | Independent Stimulus Count |
|--------|:-----------:|:------------------------:|
| Psychoacoustic (A+K) | 21 | 17 |
| Spectral (B+C+J) | 34 | 15 |
| Temporal (D+G) | 14 | 14 |
| Tonal (F+H) | 28 | 18 |
| Information (I) | 7 | 7 |
| CrossDomain (E) | 24 | 3 (grouped) |
| **TOTAL** | **128** | **73** |

---

## Classification Tree

```
ACOUSTIC STIMULUS
├── FREQUENCY STRUCTURE (Tonal Domain — 28D)
│   ├── Pitch: height, salience, 12 chroma, class entropy, inharmonicity index
│   └── Harmony: key clarity, 6 tonnetz, voice leading, harmonic change,
│                tonal stability, diatonicity, syntactic irregularity
│
├── ENERGY PROFILE (Spectral Domain — 34D)
│   ├── Dynamics: amplitude, velocity, acceleration, loudness, onset strength
│   ├── Timbre: warmth, sharpness, tonalness, centroid, smoothness,
│   │          autocorrelation, tristimulus 1-2-3
│   └── Timbre Extended: 13 MFCC, 7 spectral contrast
│
├── TEMPORAL STRUCTURE (Temporal Domain — 14D)
│   ├── Change: spectral flux, entropy, flatness, concentration
│   └── Rhythm: tempo, beat strength, pulse clarity, syncopation,
│              metricality, isochrony, groove, event density,
│              tempo stability, rhythmic regularity
│
├── PSYCHOACOUSTIC (Psychoacoustic Domain — 21D)
│   ├── Consonance: roughness, Sethares dissonance, periodicity,
│   │              tonal fusion, sensory pleasantness,
│   │              inharmonicity, harmonic deviation
│   └── Modulation: 6 mod bands, centroid, bandwidth,
│                   Zwicker sharpness, fluctuation strength,
│                   A-weighted loudness, alpha ratio,
│                   Hammarberg index, spectral slope
│
├── INFORMATION-THEORETIC (Information Domain — 7D)
│   └── Surprise: melodic entropy, harmonic entropy,
│                 rhythmic IC, spectral surprise,
│                 information rate, predictive entropy,
│                 tonal ambiguity
│
└── INTERACTION (CrossDomain — 24D)
    ├── Energy × Consonance (8D)
    ├── Change × Consonance (8D)
    └── Consonance × Timbre (8D)
```

---

**Last updated**: 2026-02-16
**Source**: R³ v2.0.0 (128D), 96 C³ model docs, R³ Demand Matrix
