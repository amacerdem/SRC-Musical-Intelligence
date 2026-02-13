# H3 Registry -- Index

**Version**: 2.0.0
**Purpose**: Canonical reference tables for all H3 axes and the demand address space
**Updated**: 2026-02-13

---

## Overview

The Registry directory contains the authoritative catalogs for the three H3 axes (horizons, morphs, laws) and the composite 4-tuple address space. These documents serve as the single source of truth for all H3 enumeration values, formulas, and mappings.

All values in these catalogs correspond to constants defined in code at `mi_beta/core/constants.py`.

---

## Files

| File | Contents | Code Reference |
|------|----------|---------------|
| [HorizonCatalog.md](HorizonCatalog.md) | All 32 horizons: duration, frames, band, musical scale, neuroscience correspondence, mechanism mappings | `HORIZON_MS` |
| [MorphCatalog.md](MorphCatalog.md) | All 24 morphs: formula, category, min window, output range, MORPH_SCALE calibration | `MORPH_NAMES`, `MORPH_SCALE` |
| [LawCatalog.md](LawCatalog.md) | All 3 laws: direction, window selection, kernel formula, neuroscience basis, unit usage | `LAW_NAMES` |
| [DemandAddressSpace.md](DemandAddressSpace.md) | 4-tuple address format, flat index formula, theoretical vs. actual space, sparsity analysis | H3DemandSpec contract |

---

## Quick Reference

| Axis | Count | Range | Code Constant |
|------|:-----:|-------|---------------|
| R3 features | 128 | [0:127] | `N_R3_FEATURES` |
| Horizons | 32 | H0-H31 | `HORIZON_MS` (len=32) |
| Morphs | 24 | M0-M23 | `MORPH_NAMES` (len=24) |
| Laws | 3 | L0-L2 | `LAW_NAMES` (len=3) |
| **Theoretical space** | **294,912** | | 128 x 32 x 24 x 3 |
| **Actual usage** | **~8,600** | | ~2.9% occupancy |

---

## Cross-References

| Related Document | Location |
|-----------------|----------|
| H3 master index | [../00-INDEX.md](../00-INDEX.md) |
| H3 architecture | [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) |
| H3DemandSpec contract | [../../C3/Contracts/H3DemandSpec.md](../../C3/Contracts/H3DemandSpec.md) |
| R3 feature catalog | [../../R3/Registry/FeatureCatalog.md](../../R3/Registry/FeatureCatalog.md) |
| Extension guide | [../EXTENSION-GUIDE.md](../EXTENSION-GUIDE.md) |
| Code constants | `mi_beta/core/constants.py` |
