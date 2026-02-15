# Translation Guide: Music Theory → Spectral Language

**Version**: 0.1.0
**Date**: 2026-02-14
**Status**: DRAFT
**Purpose**: When a C³ model paper uses traditional music theory terms, this guide maps them to spectral equivalents available in R³+H³.

---

## How to Use This Guide

1. Find the music theory term the paper uses
2. Read the spectral definition (what it ACTUALLY is in physical terms)
3. Find the R³+H³ address(es) that provide this measurement
4. Use the spectral address in the C³ model's input mapping

**Rule**: The C³ model document MAY reference the music-theory term for context. But the INPUT MAPPING must use spectral addresses.

---

## 1. Pitch & Melody

### "Note" / "Pitch"

| Theory | Spectral Reality |
|--------|-----------------|
| "A4 = 440 Hz" | Peak in spectral energy at 440 Hz and its integer multiples |
| "Note detection" | Pitch salience: degree to which spectral energy concentrates at harmonic series |
| "Melody" | Temporal sequence of pitch-class energy peaks |

**R³ mapping**: `pitch_class_energy_0..11` [49:60], `pitch_class_peak_salience` [63]
**H³ mapping**: `pitch_class_energy_*.{horizon}.velocity.memory` for melodic contour

### "Interval"

| Theory | Spectral Reality |
|--------|-----------------|
| "Perfect fifth (P5)" | Two spectral energy peaks whose fundamental frequencies have ratio near 3:2, resulting in aligned harmonics and low roughness |
| "Minor second (m2)" | Two peaks with ratio near 16:15, resulting in beating between close harmonics and high roughness |
| "Interval recognition" | Pattern of pitch-class energy transitions between successive frames |

**R³ mapping**: `pitch_class_transition_entropy` [87] captures unpredictability of these transitions. `roughness` [0] and `sethares_dissonance` [1] capture the physical consequence.

### "Melodic Contour" (up / down / same)

| Theory | Spectral Reality |
|--------|-----------------|
| "Ascending melody" | Temporal increase in spectral centroid weighted by pitch salience |
| "Descending melody" | Temporal decrease in same |
| "Contour" | Sign of velocity of dominant pitch-class index |

**H³ mapping**: `spectral_centroid_log.{horizon}.velocity.memory` [61].Hx.M8.L0

### "Melodic Expectation" / "Melodic Surprise"

| Theory | Spectral Reality |
|--------|-----------------|
| "Expected note" | Pitch-class transition consistent with running distribution (low IC) |
| "Unexpected note" | Pitch-class transition deviating from running distribution (high IC) |
| "IDyOM melodic IC" | Pitch-class transition probability under statistical model |

**R³ mapping**: `pitch_class_transition_entropy` [87]
**H³ mapping**: `[87].{horizon}.max.memory` for peak surprise, `[87].{horizon}.mean.memory` for average predictability

---

## 2. Harmony

### "Chord"

| Theory | Spectral Reality |
|--------|-----------------|
| "C major chord" | Simultaneous spectral energy concentrated at pitch classes 0 (C), 4 (E), 7 (G) with low roughness between partials |
| "Chord type" | Pattern of pitch-class energy distribution: which of 12 bins have significant energy and what are their relative amplitudes |
| "Chord change" | Rapid reorganization of pitch-class energy distribution between successive timepoints |

**R³ mapping**: `pitch_class_energy_0..11` [49:60] IS the chord representation — continuous, not labeled.
**H³ mapping**: `chroma_frame_distance.beat.max.memory` [83.H12.M4.L0] detects chord changes.

**Critical insight**: A "chord" in spectral language is simply the pitch-class energy distribution at a given moment. Whether it's "C major" or "Gdim7" is a labeling question for C³, not a measurement question for R³.

### "Key" / "Tonality"

| Theory | Spectral Reality |
|--------|-----------------|
| "The piece is in C major" | Over an extended period, pitch-class energy distribution statistically clusters around a pattern matching the Krumhansl-Kessler C major reference profile |
| "Key clarity" | How strongly pitch-class energy matches ANY single reference profile |
| "Key ambiguity" | Entropy of the match strength across all 24 reference profiles |
| "Modulation" | Temporal shift in which reference profile best fits the pitch-class distribution |

**R³ mapping**: `pitch_class_profile_correlation_peak` [75], `pitch_class_distribution_entropy_keyed` [93]
**H³ mapping**: `[75].phrase.trend.memory` for key strengthening/weakening. `[75].section.stability.memory` for key persistence.

### "Harmonic Tension" / "Tonal Tension"

| Theory | Spectral Reality |
|--------|-----------------|
| "Tension increases" | Combination of: roughness increasing, pitch-class distribution diverging from reference, spectral change rate increasing, loudness increasing |
| "Tension resolves" | Roughness decreasing, pitch-class distribution converging to reference, spectral change rate decreasing |
| "Lerdahl tonal tension" | Distance in pitch-class geometry space from "tonal center" (geometric, not symbolic) |

**R³ mapping**: Multi-feature composite:
- `roughness` [0] — sensory tension
- `chroma_frame_distance` [83] — spectral reorganization
- `pitch_class_profile_correlation_peak` [75] — proximity to reference pattern
- `amplitude_velocity` [8] — dynamic change
- `onset_density` [72] — event rate

**H³ mapping**: All of above at `phrase` horizon with `trend.memory` morph

### "Harmonic Rhythm"

| Theory | Spectral Reality |
|--------|-----------------|
| "Fast harmonic rhythm" | Frequent reorganization of pitch-class energy distribution |
| "Slow harmonic rhythm" | Stable pitch-class distribution over extended periods |
| "Harmonic rhythm periodicity" | Periodic pattern in chroma frame distance |

**R³ mapping**: `chroma_frame_distance` [83]
**H³ mapping**: `[83].beat.periodicity.integration` — does pitch-class reorganization happen rhythmically?

### "Cadence"

| Theory | Spectral Reality |
|--------|-----------------|
| "Perfect authentic cadence (V→I)" | Sequence: (1) pitch-class energy reorganization, (2) followed by convergence to reference profile, (3) with decreasing spectral change rate, (4) often with onset density decrease |
| "Deceptive cadence" | (1) occurs, but (2) does NOT — convergence goes to unexpected profile |
| "Half cadence" | (1) occurs, but stops — spectral change rate remains elevated |

**No single R³ feature maps to "cadence"**. It is a temporal PATTERN across multiple features — exactly what H³+C³ should derive:

**H³ mapping** (C³ derives "cadence" from these):
```
chroma_frame_distance.beat.trend.memory       [83].H12.M18.L0 → decreasing = approach
pcpc_peak.beat.velocity.memory                [75].H12.M8.L0  → increasing = resolution
onset_density.beat.trend.memory               [72].H12.M18.L0 → decreasing = phrase ending
spectral_prediction_uncertainty.beat.mean.memory [92].H12.M1.L0 → decreasing = predictable
```

### "Consonance" / "Dissonance"

| Theory | Spectral Reality |
|--------|-----------------|
| "Consonant interval" | Low spectral roughness, high fusion, smooth spectral envelope between partials |
| "Dissonant interval" | High roughness, low fusion, beating between close partials |
| "Consonant chord" | Low aggregate roughness across all partial pairs |
| "Dissonant chord" | High aggregate roughness |

**R³ mapping**: Group A is ALREADY spectral: `roughness` [0], `sethares_dissonance` [1], `stumpf_fusion` [3], `sensory_pleasantness` [4]. No translation needed — this group was always spectral.

### "Diatonic" / "Chromatic"

| Theory | Spectral Reality |
|--------|-----------------|
| "Diatonic music" | Pitch-class energy concentrated in 7 of 12 bins matching a diatonic template |
| "Chromatic music" | Pitch-class energy distributed across many/all 12 bins |
| "Chromaticism" | High pitch-class distribution entropy |

**R³ mapping**: `pitch_class_template_fit_max` [85], `pitch_class_distribution_entropy` [62]

---

## 3. Rhythm & Time

### "Beat" / "Tempo"

| Theory | Spectral Reality |
|--------|-----------------|
| "120 BPM" | Dominant periodicity in onset strength at 500ms interval |
| "Strong beat" | High autocorrelation of onset envelope at dominant period |
| "Beat perception" | Entrainment to periodic onset pattern |

**R³ mapping**: `onset_period_dominant` [65], `onset_autocorrelation_peak` [66]

### "Meter" / "Time Signature"

| Theory | Spectral Reality |
|--------|-----------------|
| "4/4 time" | Onset periodicity shows nested subdivisions at ratios 1:2:4 |
| "3/4 time" | Onset periodicity shows subdivisions at ratios 1:3 |
| "Complex meter" | Multiple subdivision levels detected |
| "Free time" | Low onset periodicity clarity |

**R³ mapping**: `onset_subdivision_depth` [69], `onset_periodicity_clarity` [67]

### "Syncopation"

| Theory | Spectral Reality |
|--------|-----------------|
| "Syncopated rhythm" | Onset energy peaks at positions between dominant period subdivisions |
| "Off-beat accent" | High onset strength at positions where onset autocorrelation has troughs |

**R³ mapping**: `onset_offbeat_ratio` [68]

### "Groove"

| Theory | Spectral Reality |
|--------|-----------------|
| "Groovy feel" | Combination of moderate syncopation + clear pulse + low-frequency energy emphasis |
| "No groove" | Absent syncopation OR absent pulse clarity OR absent low-frequency emphasis |

**R³ mapping**: `onset_offbeat_bass_pulse_product` [71] — composite product already in spectral terms

### "Phrase" / "Musical Phrase"

| Theory | Spectral Reality |
|--------|-----------------|
| "Phrase boundary" | Temporal point where multiple spectral features simultaneously change character: spectral novelty peak, onset density dip, spectral prediction error peak |
| "Phrase length" | Duration between successive novelty peaks |
| "Phrase arc" | Temporal trajectory of energy/tension features within a phrase |

**Not a single R³ feature** — it's an H³ temporal pattern:
**H³ mapping**: `spectral_distribution_divergence.phrase.max.memory` [90].H16.M4.L0 + `onset_density.phrase.trend.memory` [72].H16.M18.L0

---

## 4. Form & Structure

### "Verse / Chorus / Bridge"

| Theory | Spectral Reality |
|--------|-----------------|
| "Verse" | Recurring spectral profile segment with relatively low energy and moderate complexity |
| "Chorus" | Recurring spectral profile segment with high energy, stable pitch-class distribution, high onset regularity |
| "Bridge" | Non-recurring spectral segment with high spectral change rate and divergent pitch-class distribution |

**Not available in R³+H³ alone** — requires section-level analysis. C³ models at Ultra horizons (H24+) could derive this from:
- `amplitude.passage.mean.memory` [7].H22.M1.L0
- `chroma_frame_distance.passage.mean.memory` [83].H22.M1.L0
- `spectral_distribution_divergence.passage.entropy.integration` [90].H22.M20.L2

### "Repetition" / "Recurrence"

| Theory | Spectral Reality |
|--------|-----------------|
| "Musical repetition" | Self-similarity: spectral feature vector at time t correlates with vector at time t-period |
| "Theme recurrence" | Non-adjacent self-similarity in spectral trajectory |

**H³ mapping**: `periodicity` morph (M14) at macro horizons captures periodic recurrence.

---

## 5. Emotion & Expression

### "Tension" / "Relaxation"

| Theory | Spectral Reality |
|--------|-----------------|
| "Musical tension" | Composite: increasing roughness + pitch-class instability + rising energy + accelerating spectral change |
| "Relaxation / Resolution" | Decreasing roughness + pitch-class stability + falling energy + decelerating spectral change |

**Spectral composite** (Farbood 2012 model, spectral version):
```
tension_spectral = w1 * roughness.trend +
                   w2 * chroma_frame_distance.trend +
                   w3 * amplitude.trend +
                   w4 * onset_density.trend +
                   w5 * (1 - pcpc_peak.trend)
```
All inputs are H³ morphs with `trend.memory` at appropriate horizon.

### "Surprise" / "Expectation Violation"

| Theory | Spectral Reality |
|--------|-----------------|
| "Harmonic surprise" | Peak divergence of pitch-class distribution from running average |
| "Melodic surprise" | Low-probability pitch-class transition |
| "Rhythmic surprise" | Low-probability onset interval |
| "Spectral surprise" | Peak divergence of overall spectral distribution from running average |

**R³ mapping**: Group I features — `chroma_distribution_divergence` [88], `pitch_class_transition_entropy` [87], `onset_interval_surprisal` [89], `spectral_distribution_divergence` [90]

### "Emotional Valence" (happy/sad)

| Theory | Spectral Reality |
|--------|-----------------|
| "Happy music" | Typically: high onset periodicity clarity + moderate onset rate + low roughness + high pitch-class profile correlation (strong clustering) + higher spectral centroid |
| "Sad music" | Typically: moderate onset clarity + slower onset rate + higher roughness in certain bands + lower spectral centroid + less concentrated pitch-class distribution |

**No single R³ feature**. C³ models (especially ARU, RPU) derive valence from multiple spectral inputs. The spectral profile of "happy" vs "sad" is a learned C³ pattern, not an R³ measurement.

---

## 6. Special Concepts

### "Predictive Coding" / "Free Energy Principle"

Many C³ models (especially PCU, NDU) reference Friston's predictive coding framework:

| Theory | Spectral Reality |
|--------|-----------------|
| "Prediction error" | Divergence between current spectral frame and running average (already R³ [90]) |
| "Precision" | Inverse variance of prediction error over time (H³ stability morph) |
| "Prediction update" | Rate of change in running average (H³ velocity morph on running stats) |
| "Hierarchical prediction" | Multi-horizon prediction: beat-level, phrase-level, section-level |

**R³+H³ mapping**:
```
Prediction error:   spectral_distribution_divergence [90] (R³ base)
Precision:          [90].beat.stability.memory  (H³ → low std = high precision)
Hierarchy:          [90].beat.mean  vs [90].phrase.mean  vs [90].section.mean
                    (same R³ feature at multiple H³ horizons = hierarchical)
```

**Key insight**: The predictive coding hierarchy IS the H³ horizon hierarchy. Multiple horizons on the same R³ feature = multiple levels of temporal prediction.

### "Auditory Scene Analysis" (Bregman)

| Theory | Spectral Reality |
|--------|-----------------|
| "Stream segregation" | Spectral coherence: features that co-vary temporally belong to same stream |
| "Stream integration" | Features that don't co-vary are separate streams |
| "Grouping" | Temporal continuity, proximity, and similarity in spectral features |

**H³ mapping**: `stability` (M19) and `periodicity` (M14) morphs on multiple R³ features at the same horizon. Features that show correlated M19/M14 patterns likely belong to the same "stream."

### "Musical Expertise" / "Training Effects"

| Theory | Spectral Reality |
|--------|-----------------|
| "Expert perception" | More precise internal models → lower prediction error for familiar patterns |
| "Novice perception" | Less precise models → higher prediction error, more reliance on bottom-up features |

**Not an R³/H³ property** — this is purely C³ model parameterization. The spectral input is the same for everyone; the PROCESSING differs.

---

## 7. Quick Reference: Music Theory Term → R³+H³ Address

| Music Theory Term | Primary R³ Index | Primary H³ Pattern | Address Example |
|-------------------|-----------------|-------------------|-----------------|
| Pitch | [49:60] | — | base only |
| Interval | [0],[1],[49:60] | — | base only |
| Melody | [49:60],[61] | velocity.memory | [61].H12.M8.L0 |
| Chord | [49:60] | mean.integration | [49:60].H12.M1.L2 |
| Key | [75] | mean.memory | [75].H16.M1.L0 |
| Modulation | [75] | trend.memory | [75].H22.M18.L0 |
| Cadence | [83],[75],[72] | trend.memory (multi) | composite |
| Consonance | [0:6] | — | base only |
| Tension | [0],[83],[7],[72],[75] | trend.memory (multi) | composite |
| Surprise | [88],[90] | max.memory | [88].H12.M4.L0 |
| Beat | [65],[66] | — | base only |
| Tempo | [65] | stability.memory | [65].H16.M19.L0 |
| Meter | [69] | — | base only |
| Syncopation | [68] | — | base only |
| Phrase boundary | [90],[72],[83] | max + trend (multi) | composite |
| Dynamics | [7],[8],[10] | trend.memory | [7].H16.M18.L0 |
| Timbre | [12:20],[94:113] | mean.memory | [94:106].H16.M1.L0 |
| Form section | multi | mean at ultra horizon | multi.H26.M1.L2 |

---

## 8. Guidelines for C³ Model Authors

### DO:
1. **Start from the paper's concepts** — understand what the paper describes
2. **Translate to spectral** — use this guide to find the spectral equivalent
3. **Map to R³+H³ addresses** — specific numeric/spectral addresses
4. **Write provenance narrative** — explain in plain language what the spectral inputs measure
5. **Use spectral names in input mapping tables** — not music-theory terms

### DON'T:
1. **Don't use music-theory terms as R³/H³ feature names** — "key_clarity" → `pitch_class_profile_correlation_peak`
2. **Don't assume symbolic labels exist** — there are no "chord labels" or "key labels" in R³/H³
3. **Don't require note-level transcription** — R³ works from spectral analysis, not note detection
4. **Don't design models that NEED "V→I"** — design them to detect the spectral PATTERN that V→I creates

### REMEMBER:
> The paper says "dominant chord creates harmonic tension."
> R³+H³ says "pitch-class energy reorganization with high roughness and divergence from reference profile."
> The C³ model computes the same thing — but from spectral evidence, not symbolic labels.
> **Same phenomenon. Different language. Spectral is universal.**

---

**Parent**: [00_INDEX.md](00_INDEX.md)
**Prerequisites**: [01_MANIFESTO.md](01_MANIFESTO.md), [02_R3_H3_PIPELINE.md](02_R3_H3_PIPELINE.md)
