# Micro Band Index

**Band**: Micro
**Horizons**: H0-H7
**Duration**: 5.8ms - 250ms
**Frames**: 1-43
**Neural correlate**: Gamma oscillations (30-100 Hz)
**Updated**: 2026-02-13

---

## Overview

The Micro band covers the shortest temporal horizons in H3, corresponding to sensory-level auditory processing. These horizons capture onset transients, attack characteristics, and sub-beat temporal structure. At these timescales, the auditory system performs feature extraction before conscious beat perception begins.

---

## Quick Reference

| Horizon | Duration | Frames | Musical Scale | Mechanisms | Units |
|---------|----------|:------:|---------------|------------|-------|
| H0 | 5.8ms | 1 | Single sample | PPC | SPU |
| H1 | 11.6ms | 2 | Double sample | -- | SPU |
| H2 | 17.4ms | 3 | Triple sample | -- | SPU |
| H3 | 23.2ms | 4 | Onset window | PPC, ASA | SPU, ASU, NDU |
| H4 | 34.8ms | 6 | Attack phase | -- | SPU |
| H5 | 46.4ms | 8 | Short transient | -- | SPU |
| H6 | 200ms | 34 | 16th note @75BPM | PPC, TPC, BEP, ASA, AED | SPU, ASU, NDU, STU, MPU |
| H7 | 250ms | 43 | 8th note @120BPM | -- | SPU |

---

## Key Mechanisms

- **PPC** (Pitch-Period Coupling): H0, H3, H6 -- tracks pitch periodicity at sample-level resolution
- **ASA** (Auditory Scene Analysis): H3, H6 -- onset-driven stream segregation
- **TPC** (Temporal Pattern Coding): Entry at H6 -- bridges into meso band
- **BEP** (Beat Entrainment Prediction): Entry at H6 -- earliest beat-level mechanism
- **AED** (Auditory Event Detection): Entry at H6 -- event boundary detection

---

## Primary Unit Consumers

| Unit | Mechanisms Used | Horizon Range | Typical Tuple Count |
|------|----------------|:-------------:|:-------------------:|
| SPU | PPC | H0-H6 | ~150 |
| ASU | ASA | H3-H6 | ~120 |
| NDU | ASA | H3-H6 | ~120 |

---

## Morph Constraints

Micro-band windows are short (1-43 frames), which severely limits which morphs produce reliable values:

- **Reliable**: M0 (value), M1 (mean), M8 (velocity)
- **Marginal at H5-H7**: M2 (std), M4 (max), M5 (range)
- **Unreliable**: M14 (periodicity), M16 (curvature), M19 (stability), M20 (entropy)

H0 (single frame) supports only M0 (instantaneous value).

---

## Sub-Documents

| File | Horizons | Description |
|------|----------|-------------|
| [H0-H5-SubBeat.md](H0-H5-SubBeat.md) | H0-H5 | Sub-beat sensory horizons |
| [H6-H7-BeatSubdivision.md](H6-H7-BeatSubdivision.md) | H6-H7 | Beat subdivision transition zone |

## Cross-References

| Document | Location |
|----------|----------|
| Band overview | [../00-INDEX.md](../00-INDEX.md) |
| Horizon catalog | [../../Registry/HorizonCatalog.md](../../Registry/HorizonCatalog.md) |
| Morph catalog | [../../Registry/MorphCatalog.md](../../Registry/MorphCatalog.md) |
