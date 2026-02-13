# H0-H5: Sub-Beat Horizons

**Band**: Micro
**Horizons**: H0-H5
**Duration**: 5.8ms - 46.4ms
**Frames**: 1-8
**Musical scale**: Single-sample to short transient
**Neural correlate**: Gamma oscillations, cortical onset response, frequency following response
**Updated**: 2026-02-13

---

## Overview

H0-H5 are the shortest temporal horizons in the H3 system. They capture sub-beat sensory phenomena: individual onsets, attack transients, and the earliest stages of auditory feature extraction. These horizons operate below the threshold of conscious beat perception (which typically emerges around 100-250ms) and correspond to the auditory system's initial spectro-temporal analysis.

At these timescales, the auditory nerve performs phase-locking to stimulus periodicity, and cortical onset responses are generated. The temporal resolution is sufficient to track individual partials and spectral changes within a single note onset.

---

## Per-Horizon Detail

| Horizon | Duration | Frames | Musical Scale | Mechanisms | Units |
|---------|----------|:------:|---------------|------------|-------|
| **H0** | 5.8ms | 1 | Single frame | PPC | SPU |
| **H1** | 11.6ms | 2 | 2-frame pair | -- | SPU |
| **H2** | 17.4ms | 3 | 3-frame triplet | -- | SPU |
| **H3** | 23.2ms | 4 | Onset window | PPC, ASA | SPU, ASU, NDU |
| **H4** | 34.8ms | 6 | Attack phase | -- | SPU |
| **H5** | 46.4ms | 8 | Short transient | -- | SPU |

### H0: Single Frame (5.8ms, 1 frame)

The atomic unit of temporal resolution. H0 provides instantaneous snapshots with no temporal context. Only M0 (value) is meaningful -- all other morphs require at least 2 frames. Used by PPC for instantaneous pitch period estimation.

**Computational cost**: Minimal (no windowing needed).

### H1: Double Frame (11.6ms, 2 frames)

Allows computation of M8 (velocity) as a simple first difference. No higher-order morphs are reliable. Useful for detecting the sharpest onset transients.

### H2: Triple Frame (17.4ms, 3 frames)

Minimum window for M9 (acceleration) as a second difference. Still too short for any statistical morphs (M2 std, M6 skewness, M7 kurtosis).

### H3: Onset Window (23.2ms, 4 frames)

First horizon with mechanism support beyond PPC. ASA enters here, enabling onset-driven stream segregation. Four frames provide enough context for basic statistical descriptors (M1 mean, M2 std) though reliability is low. This is the shortest horizon where multiple units (SPU, ASU, NDU) overlap.

**Key role**: Establishes the earliest point at which auditory scene analysis can begin to separate concurrent sound sources.

### H4: Attack Phase (34.8ms, 6 frames)

Corresponds to the typical attack phase of percussive instruments. No dedicated mechanism at this horizon, but SPU uses it for PPC interpolation between H3 and H5.

### H5: Short Transient (46.4ms, 8 frames)

Covers the attack-sustain transition for many instruments. Eight frames allow marginal computation of M5 (range) and M2 (std). Corresponds roughly to the minimum integration window for timbre perception.

---

## Morph Relevance

| Morph | Name | H0 | H1 | H2 | H3 | H4 | H5 |
|-------|------|:--:|:--:|:--:|:--:|:--:|:--:|
| M0 | value | Y | Y | Y | Y | Y | Y |
| M1 | mean | -- | Y | Y | Y | Y | Y |
| M2 | std | -- | -- | -- | * | * | * |
| M4 | max | -- | Y | Y | Y | Y | Y |
| M5 | range | -- | Y | Y | Y | Y | Y |
| M8 | velocity | -- | Y | Y | Y | Y | Y |
| M9 | acceleration | -- | -- | Y | Y | Y | Y |

**Y** = reliable, **\*** = marginal (high variance), **--** = not meaningful

All other morphs (M6 skewness, M7 kurtosis, M14 periodicity, M16 curvature, M19 stability, M20 entropy, etc.) require substantially more frames and are not computed at H0-H5.

---

## R3 Features Commonly Tracked

These R3 v1 features are most frequently demanded at H0-H5 by consuming units:

| R3 Index | Feature | Primary Consumer | Rationale |
|:--------:|---------|------------------|-----------|
| [0] | roughness_total | SPU (PPC) | Sensory dissonance at onset |
| [7] | velocity_A | SPU (PPC) | Attack velocity (ADSR) |
| [10] | spectral_flux | SPU (PPC) | Spectral change rate |
| [11] | onset_strength | ASU (ASA), NDU (ASA) | Onset detection trigger |

### R3 v2 Candidates

These v2 features are expected to be demanded at H3-H5 (too few frames at H0-H2):

| R3 Index | Feature | Candidate Consumer | Rationale |
|:--------:|---------|-------------------|-----------|
| [63] | pitch_salience | SPU | Pitch clarity at onset |
| [49:60] | chroma_vector | SPU, ASU | Pitch class at onset (only meaningful at H3-H5 where there are enough frames for stable chroma estimation) |

**Note**: Chroma features at H0-H2 are unreliable because the FFT window for chroma computation (typically 23ms+) exceeds the horizon window.

---

## Neuroscience Basis

### Gamma Oscillations (30-100 Hz)

The micro band aligns with cortical gamma-band oscillations, which are associated with:
- **Feature binding**: Linking spectral features into coherent percepts
- **Onset response**: The auditory cortex generates onset responses within 10-20ms of stimulus arrival
- **Temporal resolution**: Gamma oscillations provide the finest temporal resolution in the cortical hierarchy

### Frequency Following Response (FFR)

At H0-H3 timescales, the auditory brainstem generates frequency-following responses that phase-lock to stimulus periodicity. This is the neural basis for PPC mechanism's pitch-period tracking.

### Cortical Onset Response

The auditory cortex onset response (N1/P2 complex) peaks at approximately 50-100ms post-stimulus, which maps to the H4-H5 range. This response is the neural correlate of onset_strength[11] tracking.

---

## Computation Notes

### Frame Buffer Requirements

| Horizon | Frames | Buffer Size (128D float32) | Notes |
|---------|:------:|:--------------------------:|-------|
| H0 | 1 | 512 bytes | No buffer needed |
| H1 | 2 | 1 KB | Minimal |
| H2 | 3 | 1.5 KB | Minimal |
| H3 | 4 | 2 KB | First multi-mechanism horizon |
| H4 | 6 | 3 KB | |
| H5 | 8 | 4 KB | |

Buffer requirements at H0-H5 are negligible. The main computational consideration is that these horizons update at every frame (172.27 Hz), so per-frame overhead must be minimized.

### Single-Frame Constraint (H0)

H0 is the only horizon where the morph computation is trivial -- M0(x) = x. No windowing, no statistics, no temporal context. This makes H0 demands equivalent to raw R3 feature passthrough.

### Attention Kernel

The H3 attention kernel A(dt) = exp(-3|dt|/H) has the following effective support at sub-beat horizons:

| Horizon | H (frames) | 95% support (frames) | Notes |
|---------|:----------:|:--------------------:|-------|
| H0 | 1 | 1 | Dirac delta |
| H1 | 2 | 2 | |
| H3 | 4 | 4 | |
| H5 | 8 | 8 | |

At these short horizons, the exponential kernel is nearly rectangular, meaning all frames in the window contribute almost equally.

---

## Cross-References

| Document | Location |
|----------|----------|
| Band index | [00-INDEX.md](00-INDEX.md) |
| Beat subdivision (H6-H7) | [H6-H7-BeatSubdivision.md](H6-H7-BeatSubdivision.md) |
| Horizon catalog | [../../Registry/HorizonCatalog.md](../../Registry/HorizonCatalog.md) |
| PPC mechanism | [../../../C³/Mechanisms/PPC.md](../../../C³/Mechanisms/PPC.md) |
| ASA mechanism | [../../../C³/Mechanisms/ASA.md](../../../C³/Mechanisms/ASA.md) |
| R3 feature catalog | [../../../R³/Registry/FeatureCatalog.md](../../../R³/Registry/FeatureCatalog.md) |
