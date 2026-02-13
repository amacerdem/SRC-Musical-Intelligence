# ASU H3 Demand Profile

> Version 2.0.0 | Updated 2026-02-13

## Unit Summary

| Property | Value |
|----------|-------|
| **Unit** | ASU (Auditory Salience Unit) |
| **Models** | 9 (alpha: 3, beta: 3, gamma: 3) |
| **Mechanisms** | ASA (all 9 models) |
| **Primary Band** | Micro-Meso |
| **R3 Domains** | B (Energy), C (Timbre) |
| **Est. Tuples** | ~360 |
| **Primary Law** | L2 (Integration) -- salience detection is time-symmetric |

## Overview

The Auditory Salience Unit detects perceptually prominent events in the auditory stream -- transients, timbral novelty, energy peaks, and spectral discontinuities. ASU has the most uniform H3 demand profile of any unit: all 9 models use a single mechanism (ASA) with the same 3 horizons (H3, H6, H9).

ASA (Auditory Salience Analysis) operates at Micro-Meso horizons, reflecting the rapid timescales at which salience is computed. The primary law is L2 (Integration), as salience detection integrates both past context (what was expected) and future context (what follows the salient event) to determine perceptual prominence.

## Per-Model Demand Table

| Model | Tier | Mechanisms | Horizons | Key R3 Features | Est. Tuples |
|-------|------|------------|----------|-----------------|:-----------:|
| SNEM  | alpha1 | ASA | H3, H6, H9 | B (onset, loudness) | ~40 |
| IACM  | alpha2 | ASA | H3, H6, H9 | A, B, C (full spectral) | ~60 |
| CSG   | alpha3 | ASA | H3, H6, H9 | A, C (consonance, timbre) | ~50 |
| BARM  | beta1 | ASA | H3, H6, H9 | B, C, D (energy transients) | ~40 |
| STANM | beta2 | ASA | H3, H6, H9 | B, C, D (timbre novelty) | ~40 |
| AACM  | beta3 | ASA | H3, H6, H9 | B, C (amplitude, timbre) | ~35 |
| PWSM  | gamma1 | ASA | H3, H6, H9 | B, C, D | ~35 |
| DGTP  | gamma2 | ASA | H3, H6, H9 | B, D (energy, change) | ~30 |
| SDL   | gamma3 | ASA | H3, H6, H9 | B, C | ~30 |

**Total**: ~360 estimated tuples across 9 models.

## Horizon Coverage Heatmap

```
Horizon  H0   H3   H6   H9  H11  H12  H16  H18  H20  H22  H25
Band     |-- Micro --|   |--Meso--|   |---- Macro ----|  Ultra
         ============================================
SNEM      .   [X]  [X]  [X]   .    .    .    .    .    .    .
IACM      .   [X]  [X]  [X]   .    .    .    .    .    .    .
CSG       .   [X]  [X]  [X]   .    .    .    .    .    .    .
BARM      .   [X]  [X]  [X]   .    .    .    .    .    .    .
STANM     .   [X]  [X]  [X]   .    .    .    .    .    .    .
AACM      .   [X]  [X]  [X]   .    .    .    .    .    .    .
PWSM      .   [X]  [X]  [X]   .    .    .    .    .    .    .
DGTP      .   [X]  [X]  [X]   .    .    .    .    .    .    .
SDL       .   [X]  [X]  [X]   .    .    .    .    .    .    .
         ============================================
Count     0    9    9    9    0    0    0    0    0    0    0
```

### Key Observations

- **Perfect uniformity**: All 9 models demand exactly the same 3 horizons (H3, H6, H9).
- **Compact footprint**: Only 3 of 32 possible horizons are demanded, making ASU the most horizon-efficient unit.
- **No Macro or Ultra demand**: Salience is computed at short timescales; long-term context is handled by downstream units (IMU, STU).
- **H3** (Micro, ~23ms) captures sub-beat transient detection.
- **H6** (Micro, ~46ms) captures beat-rate salience events.
- **H9** (Meso, ~300ms) captures phrase-level salience context.

## Morph Demand Profile

ASU demands morphs focused on transient detection and deviation from expectation:

| Morph | ID | Category | Usage |
|-------|----|----------|-------|
| Value | M0 | Level | Instantaneous salience magnitude |
| Mean | M1 | Level | Baseline level for deviation detection |
| Std | M2 | Dispersion | Variability against which salience is measured |
| Velocity | M8 | Dynamics | Rate of change (onset steepness) |
| Acceleration | M9 | Dynamics | Onset acceleration (transient sharpness) |
| Peak | M11 | Dynamics | Local maxima (salience peaks) |
| Trough | M12 | Dynamics | Local minima (salience valleys) |
| Contrast | M15 | Dynamics | Peak-to-trough ratio (salience contrast) |

### Morph-by-Tier Distribution

- **Alpha**: M0, M1, M2, M8, M9, M11, M12, M15 -- full salience detection suite.
- **Beta**: M0, M1, M2, M8, M11, M15 -- focused on peak detection and contrast.
- **Gamma**: M0, M1, M2, M8, M11 -- streamlined for consolidated salience output.

The decreasing morph count across tiers reflects progressive salience abstraction: alpha models compute raw salience features, beta models refine them, and gamma models produce consolidated salience maps.

## Law Assignment

| Law | Code | Models | Rationale |
|-----|------|--------|-----------|
| L2 (Integration) | Bidirectional | All 9 | Salience detection compares events against both past and future context |

All ASU models use L2 (Integration). Salience is inherently time-symmetric: a loud event is salient because it deviates from both preceding and following context. Neither purely causal (L0) nor purely predictive (L1) processing captures this bidirectional comparison.

## R3 Feature Consumption

### v1 Features (Groups A-E)

| R3 Group | Features Used | Primary Consumers |
|----------|--------------|-------------------|
| B (Energy) | onset_strength, loudness, rms_energy, velocity_A, velocity_D | All 9 models |
| C (Timbre) | spectral_centroid, spectral_spread, spectral_flatness, mfcc_vector, brightness_kuttruff | IACM, CSG, BARM, STANM, AACM, PWSM, SDL |
| D (Change) | spectral_flux, delta_loudness, onset_density | BARM, STANM, PWSM, DGTP |
| A (Consonance) | harmonicity, consonance_dissonance | IACM, CSG |

### v2 Expansion (Groups F-K)

| R3 Group | Priority | Rationale |
|----------|----------|-----------|
| F (Pitch) | MEDIUM | inharmonicity, pitch_salience directly serve salience detection -- pitch deviations are salient events |
| J (Timbre Extended) | MEDIUM | spectral_contrast_bands provide fine-grained timbral novelty detection for STANM, BARM |
| G (Rhythm) | LOW-MEDIUM | syncopation as a salience signal (rhythmic unexpectedness) for BARM, PWSM |
| K (Modulation) | LOW | Modulation rates not primary for transient salience |
| H (Harmony) | LOW | Harmonic features processed by SPU/IMU, not ASU |
| I (Information) | LOW | Information-theoretic features more relevant to IMU |

**Estimated v2 tuple expansion**: ~120 additional tuples, primarily from F:pitch_salience and J:spectral_contrast_bands at H3/H6/H9.

## Demand Characteristics

### Bandwidth Profile

ASU has the narrowest bandwidth profile of any unit:

- **Active range**: H3-H9 (23ms-300ms) -- 3 horizons only
- **Bandwidth**: 1.28 octaves of temporal resolution
- **Center**: H6 (~46ms) -- the perceptual present for transient events

This narrow bandwidth reflects ASU's specialized role: salience is computed over short windows and then passed to downstream units for integration over longer timescales.

### Uniformity Analysis

ASU's perfect demand uniformity has implications for implementation:

1. **Single mechanism pipeline**: No mechanism routing or switching logic needed.
2. **Fixed horizon buffer**: Only 3 horizon buffers required per model.
3. **Predictable compute**: All models have identical temporal complexity.
4. **Simple scheduling**: No horizon-dependent scheduling variation.

This makes ASU the simplest unit to implement and optimize from an H3 perspective.

### Tuple Density

Despite its compact footprint, ASU achieves moderate tuple counts through broad R3 feature consumption:

| Tier | Models | Horizons | Avg R3 Features | Avg Morphs | Avg Tuples/Model |
|------|:------:|:--------:|:---------------:|:----------:|:----------------:|
| Alpha | 3 | 3 | ~10 | ~8 | ~50 |
| Beta | 3 | 3 | ~8 | ~6 | ~38 |
| Gamma | 3 | 3 | ~6 | ~5 | ~32 |

The tuple count per model decreases across tiers as feature sets narrow through progressive abstraction.

### Comparison with Other ASA Users

ASU is not the only unit that uses ASA, but it is the purest:

| Unit | ASA Models | Additional Mechanisms | Horizons |
|------|:----------:|----------------------|----------|
| **ASU** | **9/9** | **None** | **H3, H6, H9** |
| NDU | 3/9 | PPC, TMH, MEM | H3, H6, H9 |
| PCU | 2/10 | PPC, TPC, MEM, AED, C0P | H3, H6, H9 |
| ARU | 3/10 | AED, CPD, C0P, MEM | H3, H6, H9 |
| RPU | 2/10 | AED, CPD, C0P, TMH, MEM, BEP | H3, H6, H9 |

ASU's exclusive reliance on ASA makes it the canonical reference implementation for the mechanism.

## Cross-References

- **Unit Models**: [../../C3/Models/ASU-*/](../../C3/Models/)
- **ASA Mechanism**: [../Contracts/](../Contracts/)
- **R3 B Group**: [../../R3/](../../R3/)
- **R3 C Group**: [../../R3/](../../R3/)
- **Demand Index**: [00-INDEX.md](00-INDEX.md)
- **H3 Architecture**: [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md)
- **Horizon Bands**: [../Bands/](../Bands/)
- **ASU Code Pattern Notes**: See MEMORY.md -- all 9 ASU models have known code-vs-doc discrepancies deferred to Phase 5 |

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial ASU demand profile |
