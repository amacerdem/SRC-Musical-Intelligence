# H18-H23: Section Horizons

**Band**: Macro (upper)
**Horizons**: H18-H23
**Duration**: 2,000ms - 25,000ms
**Frames**: 345-4,307
**Musical scale**: Full measure at 120BPM to extended section (~16-32 bars)
**Neural correlate**: Auditory cortex temporal receptive fields, memory consolidation
**Updated**: 2026-02-13

---

## Overview

H18-H23 span the section-level region of the macro band, where long-term memory encoding, predictive coding, and form-level processing operate. This is the primary domain for MEM (Memory Encoding/Retrieval) and C0P (Comparative Processing) mechanisms, which build hierarchical representations of musical structure over multi-second timescales.

At these durations (2-25 seconds), the auditory system integrates information far beyond echoic memory, relying on encoded representations. Statistical morphs (mean, trend, stability, entropy) dominate because instantaneous dynamics become less informative when aggregated over hundreds to thousands of frames.

---

## Per-Horizon Detail

| Horizon | Duration | Frames | Musical Scale | Mechanisms | Units |
|---------|----------|:------:|---------------|------------|-------|
| **H18** | 2,000ms | 345 | 1 bar @120BPM (4/4) | MEM, SYN, CPD, C0P | IMU, ARU, PCU, STU |
| **H19** | 3,000ms | 517 | 2 bars @160BPM | C0P | PCU |
| **H20** | 5,000ms | 861 | 4 bars @120BPM | TMH, MEM, C0P | IMU, PCU |
| **H21** | 8,000ms | 1,378 | ~8 bars @120BPM | -- | IMU |
| **H22** | 15,000ms | 2,584 | ~16 bars @120BPM | TMH, MEM | IMU |
| **H23** | 25,000ms | 4,307 | ~32 bars @120BPM | -- | IMU |

### H18: Measure/Section Entry (2,000ms, 345 frames)

The most mechanism-dense section horizon with four mechanisms:

| Mechanism | Role at H18 | Horizon Range |
|-----------|-------------|:-------------:|
| **MEM** | Memory encoding entry | **H18**, H20, H22, H25 |
| **SYN** | Longest syntactic window | H12, H16, **H18** |
| **CPD** | Longest change-point detection | H9, H16, **H18** |
| **C0P** | Comparative processing entry | **H18**, H19, H20 |

At 2s (one bar at 120 BPM), H18 captures complete harmonic measures and is the point where memory encoding begins. SYN completes its upward span here, having processed syntax from phrase (H12) through measure (H16) to section entry (H18). CPD similarly reaches its final horizon, providing structural boundary information to higher mechanisms.

### H19: Two-Bar Grouping (3,000ms, 517 frames)

C0P's middle horizon. At 3s, this captures two-bar units at 160 BPM or a bar-and-a-half at 120 BPM. Typical antecedent-consequent phrase pairs fall within this window. PCU uses H19 for predictive comparison across phrase boundaries.

### H20: Four-Bar Section (5,000ms, 861 frames)

A critical section horizon with three mechanisms converging:

| Mechanism | Role at H20 | Horizon Range |
|-----------|-------------|:-------------:|
| **TMH** | Section-level memory hierarchy | H16, H18, **H20**, H22 |
| **MEM** | Section-level memory encoding | H18, **H20**, H22, H25 |
| **C0P** | Section-level comparison | H18, H19, **H20** |

At 5s (~4 bars at 120 BPM), H20 captures a complete musical period (typically 4-bar or 8-bar). This is where the system can compare verse-to-chorus or A-section-to-B-section level structure. C0P completes its span here, having accumulated enough context for meaningful section comparison.

### H21: Eight-Bar Block (8,000ms, 1,378 frames)

At 8s (~8 bars at 120 BPM), H21 captures complete 8-bar periods, which form the fundamental structural unit of most Western tonal music. No dedicated mechanism at this horizon, but IMU uses it for interpolation between H20 and H22.

### H22: Extended Section (15,000ms, 2,584 frames)

TMH and MEM's penultimate horizon:

| Mechanism | Role at H22 | Horizon Range |
|-----------|-------------|:-------------:|
| **TMH** | Longest temporal memory window | H16, H18, H20, **H22** |
| **MEM** | Long-term memory encoding | H18, H20, **H22**, H25 |

At 15s (~16 bars at 120 BPM), H22 captures full sections (verse, chorus, bridge) of standard-form music. TMH completes its macro-band span here before ultra-band extensions. This is the timescale at which listeners form representations of musical form.

### H23: Extended Section Boundary (25,000ms, 4,307 frames)

The longest macro horizon at 25s (~32 bars at 120 BPM). This captures extended sections or transitions between major formal boundaries. No dedicated mechanism -- IMU uses this as an interpolation endpoint before the ultra band begins at H24.

---

## Morph Relevance

Statistical summary morphs dominate at section timescales:

| Morph | Name | Section Relevance | Notes |
|-------|------|-------------------|-------|
| M1 | mean | **Primary** | Average feature level over section |
| M2 | std | **Primary** | Section-level variability (contrast) |
| M5 | range | Important | Dynamic range of section |
| M18 | trend | **Primary** | Section-level trajectory (builds, decays) |
| M19 | stability | **Primary** | Consistency of feature over section |
| M20 | entropy | **Primary** | Information content / complexity of section |
| M6 | skewness | Useful | Distribution asymmetry (e.g., accent placement patterns) |
| M7 | kurtosis | Useful | Peakedness of distribution |
| M14 | periodicity | Useful at H18-H20 | Regularity of phrase-level patterns |
| M8 | velocity | Less informative | Instantaneous rate of change -- averaged out over long windows |
| M9 | acceleration | Less informative | Second-order dynamics -- high noise at section scale |

**Key insight**: At H22-H23, morphs M8 (velocity) and M9 (acceleration) approach the noise floor because instantaneous dynamics are smoothed away in 15-25s windows. The system should rely on M18 (trend) for directional information and M19 (stability) for consistency assessment.

---

## R3 Features Commonly Tracked

Section-level processing emphasizes Interactions and Energy features:

| R3 Index | Feature | Mechanism | Rationale |
|:--------:|---------|:---------:|-----------|
| [25:49] | Interactions (all) | MEM, TMH, C0P | Cross-feature interaction patterns over section |
| [7] | velocity_A | C0P | Attack pattern comparison across sections |
| [8] | velocity_D | C0P | Decay pattern comparison |
| [10] | spectral_flux | MEM | Spectral change density over section |
| [11] | onset_strength | MEM | Event density pattern over section |
| [12] | spectral_centroid | TMH | Brightness trajectory over section |

### R3 v2 Candidates

| R3 Index | Feature | Candidate Mechanism | Rationale |
|:--------:|---------|:-------------------:|-----------|
| [73] | tempo_stability | TMH, MEM | Tempo consistency over section |
| [93] | tonal_ambiguity | MEM, SYN | Tonal clarity/ambiguity trajectory |
| [92] | predictive_entropy | C0P, MEM | Predictability level over section |
| [84] | tonal_stability | SYN | Key stability across section |
| [91] | information_rate | TMH | Information density trajectory |

These v2 features provide direct measures of structural properties (tonality, predictability, tempo stability) that current mechanisms must infer indirectly from lower-level features.

---

## Neuroscience Basis

### Auditory Cortex Temporal Receptive Fields (Norman-Haignere 2022)

Norman-Haignere (2022) mapped temporal receptive fields (TRFs) in human auditory cortex using fMRI, revealing a hierarchy of temporal integration windows:

- **Primary auditory cortex (A1)**: TRFs of ~200ms-1s (H6-H16)
- **Lateral belt/parabelt**: TRFs of 2-10s (H18-H21)
- **Superior temporal sulcus**: TRFs of 10-30s (H22-H23)

H18-H23 map directly onto the higher-order auditory cortex TRF hierarchy, supporting the assignment of memory and form-processing mechanisms at these horizons.

### Memory Consolidation (Golesorkhi 2021)

Golesorkhi (2021) demonstrated that temporal integration in hippocampus and medial prefrontal cortex operates at timescales of 2-20s, matching H18-H22. Key findings:

- **Hippocampal encoding**: Active at 2-10s integration windows (H18-H21)
- **Medial PFC consolidation**: Active at 10-25s windows (H22-H23)
- **Temporal hierarchy**: Hippocampus feeds into PFC at progressively longer timescales

This neural hierarchy directly parallels the MEM mechanism's progression from H18 (encoding) through H22 (consolidation).

### Predictive Coding at Section Scale

At 2-25s timescales, the brain generates predictions about upcoming musical events based on learned statistical regularities. This predictive processing, mediated by frontal-temporal circuits, aligns with C0P's comparative function at H18-H20 and TMH's hierarchical temporal model at H16-H22.

---

## Computation Notes

### Buffer Requirements

| Horizon | Frames | Buffer Size (128D float32) | Notes |
|---------|:------:|:--------------------------:|-------|
| H18 | 345 | 172 KB | Manageable |
| H19 | 517 | 258 KB | |
| H20 | 861 | 430 KB | ~0.5 MB |
| H21 | 1,378 | 689 KB | ~0.7 MB |
| H22 | 2,584 | 1.3 MB | First MB-scale buffer |
| H23 | 4,307 | 2.2 MB | Per batch element |

Buffer sizes become significant at H22-H23. For batch processing with B=32, H23 requires 32 x 2.2 MB = ~70 MB for a single feature's full morph computation.

### Update Rate Optimization

At section timescales, frame-rate morph updates are wasteful. Recommended update intervals:

| Horizon | Recommended Update | Rationale |
|---------|:------------------:|-----------|
| H18 | Every 172 frames (~1s) | Match H16 measure rate |
| H19 | Every 259 frames (~1.5s) | |
| H20 | Every 345 frames (~2s) | |
| H21 | Every 517 frames (~3s) | |
| H22 | Every 861 frames (~5s) | |
| H23 | Every 1,378 frames (~8s) | |

### Morph Computation Cost at Section Scale

For H22 (2,584 frames), the periodicity morph (M14) via FFT-based autocorrelation costs O(N log N) = O(2584 x 11.3) ~ 29K operations per feature per morph update. With 128 features and update every 861 frames, this averages to approximately 4.3M operations per second -- manageable but worth monitoring.

---

## Cross-References

| Document | Location |
|----------|----------|
| Band index | [00-INDEX.md](00-INDEX.md) |
| Measure (H16-H17) | [H16-H17-Measure.md](H16-H17-Measure.md) |
| Movement (H24-H28) | [../Ultra/H24-H28-Movement.md](../Ultra/H24-H28-Movement.md) |
| MEM mechanism | [../../../C³/Mechanisms/MEM.md](../../../C³/Mechanisms/MEM.md) |
| TMH mechanism | [../../../C³/Mechanisms/TMH.md](../../../C³/Mechanisms/TMH.md) |
| C0P mechanism | [../../../C³/Mechanisms/C0P.md](../../../C³/Mechanisms/C0P.md) |
| SYN mechanism | [../../../C³/Mechanisms/SYN.md](../../../C³/Mechanisms/SYN.md) |
| CPD mechanism | [../../../C³/Mechanisms/CPD.md](../../../C³/Mechanisms/CPD.md) |
