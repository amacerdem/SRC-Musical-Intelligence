# H12-H15: Phrase-Level Horizons

**Band**: Meso (upper)
**Horizons**: H12-H15
**Duration**: 525ms - 800ms
**Frames**: 90-138
**Musical scale**: Half-bar to two-beat grouping
**Neural correlate**: Phrase-level chunking, syntactic processing
**Updated**: 2026-02-13

---

## Overview

H12-H15 span the phrase-level region of the meso band, bridging beat-period processing into measure-level structure. These horizons capture half-bar to two-beat groupings, where musical syntax (harmonic progression, melodic contour) begins to manifest. The SYN (Syntactic Processing) mechanism enters at H12, and TPC (Temporal Pattern Coding) provides its meso-band anchor here.

At the phrase level, listeners begin to perceive musical grammar: tension-resolution patterns, antecedent-consequent structures, and harmonic cadential expectations. Koelsch (2011) demonstrated that syntactic violations in music activate Broca's area analogs within this timescale.

---

## Per-Horizon Detail

| Horizon | Duration | Frames | BPM (Half Note) | Mechanisms | Units |
|---------|----------|:------:|:----------------:|------------|-------|
| **H12** | 525ms | 90 | 114 | TPC, SYN | SPU, STU |
| **H13** | 600ms | 103 | 100 | -- | STU |
| **H14** | 700ms | 121 | 86 | -- | STU |
| **H15** | 800ms | 138 | 75 | -- | STU |

### H12: Phrase Entry Point (525ms, 90 frames)

H12 is the gateway to phrase-level processing. Two mechanisms converge:

| Mechanism | Role at H12 | Horizon Range |
|-----------|-------------|:-------------:|
| **TPC** | Meso-band temporal patterns | H6, **H12**, H16 |
| **SYN** | Musical syntax entry point | **H12**, H16, H18 |

At 525ms (114 BPM half note), H12 captures the shortest phrase-level groupings: two-beat motifs, anacrusis-downbeat pairs, and call-response micro-phrases. TPC uses H12 to detect recurring temporal patterns at the sub-measure scale, while SYN begins evaluating harmonic and melodic syntax.

### H13: Standard Phrase (600ms, 103 frames)

At 600ms, H13 corresponds to a half note at 100 BPM -- a natural breathing/phrasing interval in vocal music. No dedicated mechanism, but STU uses this horizon for interpolation between H12 and H14.

### H14: Extended Phrase (700ms, 121 frames)

Covers longer phrase groupings at moderate tempi. At 86 BPM (half note), this aligns with slow ballad phrasing and legato melodic lines. The 121-frame window provides strong statistical reliability for all morphs.

### H15: Phrase Boundary (800ms, 138 frames)

The longest meso horizon. At 800ms, this approaches the lower boundary of measure-level processing (H16 = 1,000ms). H15 captures complete two-beat phrases at moderate tempi and serves as the bridge point between meso and macro bands.

---

## Musical Timing Equivalents

| Horizon | Duration | As Quarter Note | As Half Note | As Bar (4/4) |
|---------|----------|:--------------:|:------------:|:------------:|
| H12 | 525ms | 114 BPM | 57 BPM | -- |
| H13 | 600ms | 100 BPM | 50 BPM | -- |
| H14 | 700ms | 86 BPM | 43 BPM | -- |
| H15 | 800ms | 75 BPM | 38 BPM | -- |

**Note**: At phrase timescales, the "as bar" column is typically empty because these horizons capture sub-measure groupings, not full measures.

---

## Morph Relevance

All 24 morphs are valid and reliable at H12-H15 (90-138 frames). Key morphs for phrase processing:

| Morph | Name | Phrase-Level Relevance |
|-------|------|-----------------------|
| M1 | mean | Average feature level over phrase |
| M2 | std | Variability within phrase (expressiveness) |
| M5 | range | Dynamic range of phrase |
| M6 | skewness | Asymmetry of feature distribution (e.g., accent placement) |
| M8 | velocity | Feature change rate across phrase |
| M14 | periodicity | Sub-phrase rhythmic regularity |
| M18 | trend | Phrase-level crescendo/decrescendo, ascending/descending contour |
| M20 | entropy | Information content of phrase |

**M18 trend** becomes particularly informative at phrase timescales because musical phrases often exhibit directional contours (rising melodic lines, crescendo-decrescendo arcs) that linear trend captures well.

**M14 periodicity** at H12-H15 measures whether the phrase exhibits regular internal structure (e.g., repeated motifs, regular accent patterns).

---

## R3 Features Commonly Tracked

At phrase timescales, processing shifts from Energy-dominated features toward Timbre and Change:

| R3 Index | Feature | Mechanism | Rationale |
|:--------:|---------|:---------:|-----------|
| [12] | spectral_centroid | TPC | Brightness contour over phrase |
| [13] | spectral_bandwidth | TPC | Spectral spread evolution |
| [14] | brightness_kuttruff | TPC | Timbral brightness tracking |
| [15] | spectral_rolloff | TPC | High-frequency content trajectory |
| [16] | spectral_contrast | TPC | Spectral peak-valley pattern |
| [21] | spectral_change | SYN | Harmonic change at phrase boundaries |
| [22] | energy_change | SYN | Dynamic change across phrase |
| [23] | timbre_change | SYN | Timbral evolution within phrase |
| [24] | rhythm_change | SYN | Rhythmic pattern evolution |

### R3 v2 Candidates

| R3 Index | Feature | Candidate Mechanism | Rationale |
|:--------:|---------|:-------------------:|-----------|
| [75] | key_clarity | SYN | Tonal clarity within phrase |
| [83] | harmonic_change | SYN | Chord change rate at phrase level |
| [87] | melodic_entropy | SYN, TPC | Melodic unpredictability within phrase |
| [84] | tonal_stability | SYN | Tonal stability of phrase |

These v2 features capture harmonic and melodic properties that are fundamental to musical syntax processing at the phrase level.

---

## Neuroscience Basis

### Phrase-Level Chunking

Listeners naturally segment continuous music into phrase-level chunks of approximately 0.5-2s duration. This chunking process, mediated by auditory cortex and prefrontal regions, aligns with H12-H15. EEG studies show closure positive shift (CPS) at phrase boundaries, indicating active segmentation.

### Syntactic Processing (Koelsch 2011)

Koelsch (2011) demonstrated that harmonic syntax violations (unexpected chords in progressions) elicit an early right anterior negativity (ERAN) response within 200-500ms of the violation. At the phrase level (H12-H15), the system has accumulated enough harmonic context to detect these violations, justifying SYN's entry at H12.

Key findings relevant to H12-H15:
- ERAN amplitude scales with the degree of syntactic violation
- Processing engages inferior frontal gyrus (Broca's area homolog)
- Musical syntax processing shares resources with language syntax

### Theta-Band Phrase Tracking

Theta oscillations (4-8 Hz) track phrase-level temporal structure. Ding et al. (2016) showed that cortical theta activity entrains to phrase rate even when it is not acoustically marked, indicating top-down phrase-level temporal prediction.

---

## Computation Notes

### Buffer Requirements

| Horizon | Frames | Buffer Size (128D float32) |
|---------|:------:|:--------------------------:|
| H12 | 90 | 45 KB |
| H13 | 103 | 52 KB |
| H14 | 121 | 61 KB |
| H15 | 138 | 69 KB |

Buffers remain practical for real-time processing. At H15 (138 frames, ~800ms), the system maintains less than 70 KB per feature per horizon.

### Morph Computation at Phrase Scale

At 90-138 frames, all morphs are computed with high statistical reliability:

| Morph | Min Reliable Frames | H12-H15 Status |
|-------|:-------------------:|:--------------:|
| M6 skewness | ~30 | Fully reliable |
| M7 kurtosis | ~50 | Fully reliable |
| M14 periodicity | ~60 | Fully reliable |
| M20 entropy | ~50 | Fully reliable |

No morphs are marginal at these horizons.

### TPC Spanning Pattern

TPC operates at H6 (200ms), H12 (525ms), and H16 (1,000ms), giving it a 5x ratio between its shortest and longest horizons. At H12, TPC integrates temporal patterns that span roughly 2.5 beat periods (at 120 BPM), which is the typical length of a musical motif.

---

## Cross-References

| Document | Location |
|----------|----------|
| Band index | [00-INDEX.md](00-INDEX.md) |
| Beat period (H8-H11) | [H8-H11-BeatPeriod.md](H8-H11-BeatPeriod.md) |
| Measure (H16-H17) | [../Macro/H16-H17-Measure.md](../Macro/H16-H17-Measure.md) |
| TPC mechanism | [../../../C³/Mechanisms/TPC.md](../../../C³/Mechanisms/TPC.md) |
| SYN mechanism | [../../../C³/Mechanisms/SYN.md](../../../C³/Mechanisms/SYN.md) |
| Morph catalog | [../../Registry/MorphCatalog.md](../../Registry/MorphCatalog.md) |
