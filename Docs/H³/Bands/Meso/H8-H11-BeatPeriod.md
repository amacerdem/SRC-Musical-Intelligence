# H8-H11: Beat Period Horizons

**Band**: Meso
**Horizons**: H8-H11
**Duration**: 300ms - 450ms
**Frames**: 52-78
**Musical scale**: Quarter note at 133-200 BPM
**Neural correlate**: Motor cortex beta desynchronization, sensorimotor synchronization
**Updated**: 2026-02-13

---

## Overview

H8-H11 span the core beat-period range, corresponding to quarter-note durations at typical musical tempi (133-200 BPM). This is the temporal sweet spot for human beat perception and motor entrainment. The BEP (Beat Entrainment Prediction) mechanism has its primary domain here, and all 24 morphs produce reliable values at these frame counts.

The range 300-450ms aligns closely with the preferred spontaneous tapping rate in humans (~500ms, but with considerable individual variation from 300-700ms), and with the peak of the resonance curve for beat perception (Large & Palmer 2002).

---

## Per-Horizon Detail

| Horizon | Duration | Frames | BPM (Quarter) | BPM (8th) | Mechanisms | Units |
|---------|----------|:------:|:--------------:|:---------:|------------|-------|
| **H8** | 300ms | 52 | 200 | 400 | -- | STU, MPU |
| **H9** | 350ms | 60 | 171 | 343 | BEP, ASA, CPD | STU, MPU, ASU, NDU, ARU |
| **H10** | 400ms | 69 | 150 | 300 | -- | STU, MPU |
| **H11** | 450ms | 78 | 133 | 267 | BEP | STU, MPU |

### H8: Fast Beat Period (300ms, 52 frames)

The fastest standard beat period. At 200 BPM, this corresponds to fast dance music, double-time passages, and presto tempi. No dedicated mechanism at this horizon, but STU and MPU interpolate BEP outputs between H6 and H9.

### H9: Primary Beat Period (350ms, 60 frames)

The most mechanism-dense meso horizon with three mechanisms:

| Mechanism | Role at H9 | Horizon Range |
|-----------|-----------|:-------------:|
| **BEP** | Core beat tracking | H6, **H9**, H11 |
| **ASA** | Beat-rate scene segregation | H3, H6, **H9** |
| **CPD** | Beat-level change detection | **H9**, H16, H18 |

H9 at 171 BPM is near the center of the comfortable dance tempo range. ASA's presence at H9 reflects the fact that stream segregation is influenced by temporal regularity at beat rate -- regularly spaced events are more easily grouped into streams.

### H10: Moderate Beat Period (400ms, 69 frames)

Corresponds to 150 BPM, a common tempo for pop, rock, and uptempo jazz. No dedicated mechanism, but the densest frame count without mechanism overhead makes this a useful interpolation point.

### H11: Relaxed Beat Period (450ms, 78 frames)

BEP's upper meso-band anchor at 133 BPM. This corresponds to moderate walking tempo, ballads, and relaxed groove. Seventy-eight frames provide robust statistical estimates for all morphs.

---

## BPM Range Coverage

| BPM | Quarter (ms) | Nearest Horizon | Horizon Duration |
|:---:|:------------:|:---------------:|:----------------:|
| 200 | 300 | H8 | 300ms |
| 180 | 333 | H8-H9 | interpolated |
| 171 | 350 | H9 | 350ms |
| 160 | 375 | H9-H10 | interpolated |
| 150 | 400 | H10 | 400ms |
| 140 | 429 | H10-H11 | interpolated |
| 133 | 450 | H11 | 450ms |
| 120 | 500 | H11-H12 | gap (next is 525ms) |

**Notable gap**: Tempi between 114-133 BPM (450-525ms) fall between H11 and H12, requiring interpolation. This is a common tempo range (moderate pop, jazz ballad) that future horizon refinement may address.

---

## Morph Relevance

All 24 morphs are valid at H8-H11. Key morphs for beat-period processing:

| Morph | Name | Beat-Period Relevance |
|-------|------|-----------------------|
| M0 | value | Current beat-period feature value |
| M1 | mean | Average feature level over beat duration |
| M2 | std | Variability within beat (expressive micro-timing) |
| M5 | range | Dynamic range within single beat |
| M8 | velocity | Feature change rate at beat level |
| M14 | periodicity | **Core morph** -- measures sub-beat regularity within the beat window |
| M18 | trend | Crescendo/decrescendo within beat |

**M14 periodicity** is particularly important at H8-H11 because these windows are long enough to contain 2-4 sub-beat events, making periodicity estimation meaningful. A beat at 150 BPM with sixteenth-note subdivisions contains 4 events in the H10 window.

---

## R3 Features Commonly Tracked

| R3 Index | Feature | Mechanism | Rationale |
|:--------:|---------|:---------:|-----------|
| [7] | velocity_A | BEP | Attack velocity pattern within beat |
| [8] | velocity_D | BEP | Decay pattern (legato vs staccato) |
| [9] | velocity_S | BEP | Sustain level stability |
| [10] | spectral_flux | BEP, CPD | Spectral change at beat boundaries |
| [11] | onset_strength | BEP, ASA | Onset salience for beat tracking |
| [21] | spectral_change | CPD | Change rate for boundary detection |
| [22] | energy_change | CPD | Energy dynamics at beat rate |
| [23] | timbre_change | CPD | Timbral shifts between beats |
| [24] | rhythm_change | CPD | Rhythmic pattern evolution |

### R3 v2 Candidates

| R3 Index | Feature | Candidate Mechanism | Rationale |
|:--------:|---------|:-------------------:|-----------|
| [65] | tempo_estimate | BEP | Local tempo within beat window |
| [66] | beat_strength | BEP | Beat salience for entrainment |
| [68] | syncopation | BEP | Syncopation level at beat scale |
| [71] | groove | BEP | Micro-timing groove pattern |

These v2 features directly encode rhythmic properties that BEP currently infers indirectly from Energy features.

---

## Neuroscience Basis

### Motor Cortex Beta Desynchronization

During rhythmic listening, the motor cortex exhibits event-related beta desynchronization (ERD) approximately 200-500ms before expected beats (Grahn & Brett 2007). This predictive motor response is strongest at tempi within the H8-H11 range (133-200 BPM), which aligns with the preferred rate for spontaneous motor synchronization.

### Sensorimotor Synchronization

The basal ganglia-thalamo-cortical loop generates predictive timing signals that enable beat-synchronous tapping. This circuit's temporal resolution matches the H8-H11 range. Lesion studies show that basal ganglia damage impairs beat perception specifically at these timescales (Grahn & Brett 2007).

### Beat Perception Resonance

Large & Palmer (2002) proposed that beat perception arises from resonance in a network of neural oscillators. The strongest resonance occurs in the 300-600ms period range, which spans H8-H12. H9 (350ms) and H10 (400ms) sit near the resonance peak.

### Auditory-Motor Coupling

Even passive listening to rhythmic stimuli activates motor cortex areas, demonstrating automatic auditory-motor coupling at beat-period timescales. This coupling is strongest for tempi near 120-150 BPM (H10-H12 range) and provides the neural basis for the BEP mechanism.

---

## Computation Notes

### Buffer Requirements

| Horizon | Frames | Buffer Size (128D float32) |
|---------|:------:|:--------------------------:|
| H8 | 52 | 26 KB |
| H9 | 60 | 30 KB |
| H10 | 69 | 35 KB |
| H11 | 78 | 39 KB |

Buffers remain modest. The primary computational cost at meso timescales is morph computation over the full 24-morph palette, which involves O(N log N) operations for periodicity (M14, via autocorrelation/FFT).

### Morph Computation Cost

At H8-H11, all 24 morphs are computed. Per-horizon morph costs:

| Morph Category | Operations | Notes |
|---------------|------------|-------|
| Distribution (M0-M7) | O(N) | Simple statistics |
| Dynamics (M8-M13, M15, M18, M21) | O(N) | First/second differences, linear regression |
| Rhythm (M14, M17, M22) | O(N log N) | Autocorrelation via FFT |
| Information (M20) | O(N log N) | Histogram + entropy |
| Symmetry (M16, M19, M23) | O(N) | Curvature, variance of velocity |

### Attention Kernel Shape

At H8-H11, the exponential kernel A(dt) = exp(-3|dt|/H) provides substantial temporal weighting:

| Horizon | H (frames) | 50% weight at | 95% weight span |
|---------|:----------:|:-------------:|:---------------:|
| H8 | 52 | 12 frames | ~52 frames |
| H9 | 60 | 14 frames | ~60 frames |
| H10 | 69 | 16 frames | ~69 frames |
| H11 | 78 | 18 frames | ~78 frames |

The kernel becomes meaningfully shaped (not near-rectangular) at these horizons, giving higher weight to recent frames and providing temporal locality.

---

## Cross-References

| Document | Location |
|----------|----------|
| Band index | [00-INDEX.md](00-INDEX.md) |
| Beat subdivision (H6-H7) | [../Micro/H6-H7-BeatSubdivision.md](../Micro/H6-H7-BeatSubdivision.md) |
| Phrase (H12-H15) | [H12-H15-Phrase.md](H12-H15-Phrase.md) |
| BEP mechanism | [../../../C³/Mechanisms/BEP.md](../../../C³/Mechanisms/BEP.md) |
| ASA mechanism | [../../../C³/Mechanisms/ASA.md](../../../C³/Mechanisms/ASA.md) |
| CPD mechanism | [../../../C³/Mechanisms/CPD.md](../../../C³/Mechanisms/CPD.md) |
| Morph catalog | [../../Registry/MorphCatalog.md](../../Registry/MorphCatalog.md) |
