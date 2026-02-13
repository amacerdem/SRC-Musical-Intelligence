# H3 Morphology -- Category Index

**Version**: 2.0.0
**Morphs**: 24 (M0-M23) across 5 categories
**Purpose**: Cross-cutting morph documentation organized by statistical category
**Code reference**: `mi_beta.ear.h3.morph.MorphComputer`
**Updated**: 2026-02-13

---

## Overview

The Morphology directory provides detailed documentation for each of the 24 H3 morphs, organized by statistical category. These documents complement the compact reference in [Registry/MorphCatalog.md](../Registry/MorphCatalog.md) with expanded formulas, musical interpretations, scaling notes, horizon constraints, and common use cases across C3 units.

Each morph is a function that takes a windowed slice of an R3 feature and produces a single scalar descriptor per frame. Morph outputs are normalized to [0, 1] via the `MORPH_SCALE` calibration system documented in [MorphScaling.md](MorphScaling.md).

---

## Category Summary

| Category | File | Morphs | Count | Description |
|----------|------|--------|:-----:|-------------|
| **Distribution** | [Distribution.md](Distribution.md) | M0-M7 | 8 | Central tendency, spread, and shape of value distribution |
| **Dynamics** | [Dynamics.md](Dynamics.md) | M8-M13, M15, M18, M21 | 9 | Temporal derivatives, trend, smoothness, oscillation |
| **Rhythm** | [Rhythm.md](Rhythm.md) | M14, M17, M22 | 3 | Periodicity, dominant cycle, event density |
| **Information** | [Information.md](Information.md) | M20 | 1 | Shannon entropy of value distribution |
| **Symmetry** | [Symmetry.md](Symmetry.md) | M16, M19, M23 | 3 | Curvature, stability, time-reversal symmetry |
| **Scaling** | [MorphScaling.md](MorphScaling.md) | All 24 | -- | MORPH_SCALE calibration and normalization protocol |
| | | **Total** | **24** | |

---

## File Listing

| File | Contents |
|------|----------|
| [Distribution.md](Distribution.md) | M0-M7: attention_weighted_mean, unweighted_mean, std, median, max, range, skewness, kurtosis |
| [Dynamics.md](Dynamics.md) | M8-M13, M15, M18, M21: velocity, acceleration, smoothness, trend, zero_crossings |
| [Rhythm.md](Rhythm.md) | M14, M17, M22: periodicity, shape_period, peaks |
| [Information.md](Information.md) | M20: entropy (Shannon, 16-bin histogram, normalized) |
| [Symmetry.md](Symmetry.md) | M16, M19, M23: curvature, stability, symmetry |
| [MorphScaling.md](MorphScaling.md) | MORPH_SCALE array, calibration protocol, signed/unsigned normalization, edge cases |

---

## Cross-References

| Related Document | Location |
|-----------------|----------|
| Morph catalog (compact reference) | [../Registry/MorphCatalog.md](../Registry/MorphCatalog.md) |
| H3 architecture (morph axis) | [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) |
| Extension guide (adding morphs) | [../EXTENSION-GUIDE.md](../EXTENSION-GUIDE.md) |
| H3 master index | [../00-INDEX.md](../00-INDEX.md) |
| MorphComputer implementation | `mi_beta/ear/h3/morph.py` |
| MORPH_SCALE constants | `mi_beta/core/constants.py` |
