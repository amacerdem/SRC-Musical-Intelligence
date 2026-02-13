# SPU H3 Demand Profile

> Version 2.0.0 | Updated 2026-02-13

## Unit Summary

| Property | Value |
|----------|-------|
| **Unit** | SPU (Spectral Processing Unit) |
| **Models** | 9 (alpha: 3, beta: 3, gamma: 3) |
| **Mechanisms** | PPC (6 models), TPC (3 models) |
| **Primary Band** | Micro-Macro |
| **R3 Domains** | A (Consonance), C (Timbre) |
| **Est. Tuples** | ~450 |
| **Primary Law** | L2 (Integration) -- bidirectional spectral integration |

## Overview

The Spectral Processing Unit performs core spectral analysis and integration across the frequency domain. Its H3 demand is split between two mechanisms:

- **PPC** (Peripheral Processing Chain): 6 models operating at Micro horizons (H0, H3, H6) for rapid spectral feature extraction.
- **TPC** (Temporal Pattern Completion): 3 models spanning Micro-to-Macro horizons (H6, H12, H16) for spectral pattern integration over longer timescales.

SPU's primary law is L2 (Integration), reflecting the bidirectional nature of spectral processing -- both bottom-up feature extraction and top-down spectral template matching.

## Per-Model Demand Table

| Model | Tier | Mechanisms | Horizons | Key R3 Features | Est. Tuples |
|-------|------|------------|----------|-----------------|:-----------:|
| BCH   | alpha1 | PPC | H0, H3, H6 | A group (harmonicity, roughness) | ~60 |
| PSCL  | alpha2 | PPC | H0, H3, H6 | A, C (consonance, timbre) | ~60 |
| PCCR  | alpha3 | PPC | H0, H3, H6 | A (consonance cross-products) | ~60 |
| STAI  | beta1  | TPC | H6, H12, H16 | A, C, E (spectral integration) | ~45 |
| TSCP  | beta2  | TPC | H6, H12, H16 | C (timbre completion) | ~45 |
| MIAA  | beta3  | TPC | H6, H12, H16 | A, C (spectral attention) | ~45 |
| SDNPS | gamma1 | PPC | H0, H3, H6 | A (consonance) | ~30 |
| ESME  | gamma2 | PPC | H0, H3, H6 | A, C (spectral memory) | ~30 |
| SDED  | gamma3 | PPC | H0, H3, H6 | A (consonance) | ~30 |

**Total**: ~450 estimated tuples across 9 models.

## Horizon Coverage Heatmap

```
Horizon  H0   H3   H6   H9  H11  H12  H16  H18  H20  H22  H25
Band     |-- Micro --|   |--Meso--|   |---- Macro ----|  Ultra
         ============================================
BCH      [X]  [X]  [X]   .    .    .    .    .    .    .    .
PSCL     [X]  [X]  [X]   .    .    .    .    .    .    .    .
PCCR     [X]  [X]  [X]   .    .    .    .    .    .    .    .
STAI      .    .   [X]   .    .   [X]  [X]   .    .    .    .
TSCP      .    .   [X]   .    .   [X]  [X]   .    .    .    .
MIAA      .    .   [X]   .    .   [X]  [X]   .    .    .    .
SDNPS    [X]  [X]  [X]   .    .    .    .    .    .    .    .
ESME     [X]  [X]  [X]   .    .    .    .    .    .    .    .
SDED     [X]  [X]  [X]   .    .    .    .    .    .    .    .
         ============================================
Count     6    6    9    0    0    3    3    0    0    0    0
```

- **H6** is the most demanded horizon (9/9 models), serving as the junction between PPC and TPC.
- **H0, H3** are demanded by all 6 PPC models (Micro band).
- **H12, H16** are demanded only by the 3 TPC beta models (Meso-Macro band).
- No Meso-only or Ultra demand from SPU.

## Morph Demand Profile

SPU primarily demands the following morphs across its horizons:

| Morph | ID | Category | Usage |
|-------|----|----------|-------|
| Value | M0 | Level | Raw spectral feature magnitudes |
| Mean | M1 | Level | Averaged spectral features over horizon window |
| Std | M2 | Dispersion | Spectral variability within horizon |
| Velocity | M8 | Dynamics | Rate of spectral change |
| Trend | M18 | Dynamics | Long-term spectral drift (TPC models) |

### Morph-by-Tier Distribution

- **Alpha (PPC)**: M0, M1, M2, M8 -- raw extraction and first-order statistics.
- **Beta (TPC)**: M0, M1, M2, M8, M18 -- adds trend morph for pattern completion.
- **Gamma (PPC)**: M0, M1, M2 -- reduced morph set, consolidated features.

## Law Assignment

| Law | Code | Models | Rationale |
|-----|------|--------|-----------|
| L2 (Integration) | Bidirectional | All 9 | Spectral processing integrates both past context and predictive templates |

SPU does not use L0 (Memory) or L1 (Prediction) as primary laws. The bidirectional nature of spectral processing -- where harmonic templates constrain bottom-up analysis and vice versa -- makes L2 the natural fit across all tiers.

## R3 Feature Consumption

### v1 Features (Groups A-E)

| R3 Group | Features Used | Primary Consumers |
|----------|--------------|-------------------|
| A (Consonance) | harmonicity, roughness, roughness_total, consonance_dissonance, inharmonicity, periodicity, fundamental_freq | All 9 models |
| C (Timbre) | spectral_centroid, spectral_spread, spectral_rolloff, spectral_flatness, spectral_crest, mfcc_vector, spectral_contrast, brightness_kuttruff, zero_crossing_rate | PSCL, STAI, TSCP, MIAA, ESME |
| E (Interactions) | Spectral interaction terms | STAI |

### v2 Expansion (Groups F-K)

| R3 Group | Priority | Rationale |
|----------|----------|-----------|
| F (Pitch) | HIGH | chroma, pitch_height, pitch_salience directly serve harmonic analysis at existing PPC/TPC horizons |
| J (Timbre Extended) | MEDIUM | spectral_contrast_bands, timbral_brightness extend C group features |
| H (Harmony) | LOW | SPU focuses on spectral primitives, not harmonic structure |

Estimated v2 tuple expansion: ~180 additional tuples, primarily from F group features at H0/H3/H6 (PPC) and H6/H12/H16 (TPC).

## Demand Characteristics

### Bandwidth Profile

SPU's demand is concentrated in the Micro band (H0-H6), with a secondary peak at Meso-Macro (H12-H16) from TPC models. This creates a bimodal demand distribution:

- **Primary peak**: H0-H6 (5.8ms-46ms) -- peripheral spectral extraction
- **Secondary peak**: H12-H16 (500ms-1s) -- spectral pattern integration
- **Gap**: H7-H11 (no demand) -- SPU does not operate at beat-rate timescales

### Scaling Notes

- SPU demand scales linearly with R3 feature count. Adding F group features adds ~3 tuples per model per horizon.
- TPC models are the largest per-model consumers due to spanning 3 horizon bands.
- PPC models have high tuple counts despite fewer horizons due to broad A group consumption.

## Cross-References

- **Unit Models**: [../../C3/Models/SPU-*/](../../C3/Models/)
- **PPC Mechanism**: [../Contracts/](../Contracts/)
- **TPC Mechanism**: [../Contracts/](../Contracts/)
- **R3 A Group**: [../../R3/](../../R3/)
- **R3 C Group**: [../../R3/](../../R3/)
- **Demand Index**: [00-INDEX.md](00-INDEX.md)
- **H3 Architecture**: [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md)
- **Horizon Bands**: [../Bands/](../Bands/)

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial SPU demand profile |
