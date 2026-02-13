# C³ Brain Regions -- Atlas Index

> **Module**: `mi_beta.brain.regions`
> **Singleton**: `ATLAS = RegionAtlas()` -- import and query directly
> **Total regions**: 26 (9 subcortical + 12 cortical + 5 brainstem)

## Coordinate System: MNI152

All coordinates are in **MNI152 standard space** (Montreal Neurological Institute). MNI152 is the most widely used neuroimaging coordinate system, derived from averaging 152 healthy adult brains.

| Axis | Direction | Negative | Positive | Origin |
|------|-----------|----------|----------|--------|
| **x** | Sagittal | Left hemisphere | Right hemisphere | Midline (interhemispheric fissure) |
| **y** | Coronal | Posterior (occipital) | Anterior (frontal) | Anterior commissure |
| **z** | Axial | Inferior (ventral) | Superior (dorsal) | Anterior commissure |

Units are millimeters. Coordinates represent bilateral centroids unless hemisphere is specified as `"L"` or `"R"`. Brainstem structures carry higher spatial uncertainty (+/- 2-3 mm).

---

## Region Categories

| Category | Count | Documentation | Code Reference |
|----------|-------|---------------|----------------|
| [Subcortical](Subcortical.md) | 9 | VTA, NAcc, caudate, amygdala, hippocampus, putamen, MGB, hypothalamus, insula | `mi_beta/brain/regions/subcortical.py` |
| [Cortical](Cortical.md) | 12 | A1/HG, STG, STS, IFG, dlPFC, vmPFC, OFC, ACC, SMA, PMC, AG, TP | `mi_beta/brain/regions/cortical.py` |
| [Brainstem](Brainstem.md) | 5 | IC, AN, CN, SOC, PAG | `mi_beta/brain/regions/brainstem.py` |

---

## Evidence Summary

Total evidence citations across all 26 regions: **396**

| Category | Regions | Total Evidence | Mean Evidence |
|----------|---------|----------------|---------------|
| Subcortical | 9 | 163 | 18.1 |
| Cortical | 12 | 198 | 16.5 |
| Brainstem | 5 | 35 | 7.0 |

---

## RegionAtlas API

The `RegionAtlas` class provides O(1) lookup by abbreviation:

```python
from mi_beta.brain.regions import ATLAS

# Single lookup
vta = ATLAS["VTA"]

# Multiple lookup
reward_regions = ATLAS.by_abbreviations("VTA", "NAcc", "caudate")

# Search by function
timing = ATLAS.by_function_keyword("timing")

# Category access
ATLAS.subcortical   # Tuple[BrainRegion, ...]
ATLAS.cortical      # Tuple[BrainRegion, ...]
ATLAS.brainstem     # Tuple[BrainRegion, ...]
ATLAS.all           # All regions in canonical order
```

---

## Quick Reference: All Regions

| # | Abbreviation | Name | Hemisphere | MNI (x, y, z) | BA | Evidence |
|---|-------------|------|------------|----------------|-----|----------|
| 1 | VTA | Ventral Tegmental Area | bilateral | (0, -16, -8) | -- | 18 |
| 2 | NAcc | Nucleus Accumbens | bilateral | (10, 12, -8) | -- | 24 |
| 3 | caudate | Caudate Nucleus | bilateral | (12, 10, 10) | -- | 19 |
| 4 | amygdala | Amygdala | bilateral | (24, -4, -18) | -- | 31 |
| 5 | hippocampus | Hippocampus | bilateral | (28, -22, -12) | -- | 22 |
| 6 | putamen | Putamen | bilateral | (26, 4, 2) | -- | 16 |
| 7 | MGB | Thalamus (MGB) | bilateral | (14, -24, -2) | -- | 11 |
| 8 | hypothalamus | Hypothalamus | bilateral | (0, -4, -8) | -- | 9 |
| 9 | insula | Insula | bilateral | (36, 16, 0) | -- | 14 |
| 10 | A1/HG | Primary Auditory Cortex | bilateral | (48, -18, 8) | 41 | 42 |
| 11 | STG | Superior Temporal Gyrus | bilateral | (58, -22, 4) | 22 | 38 |
| 12 | STS | Superior Temporal Sulcus | bilateral | (54, -32, 4) | 21 | 15 |
| 13 | IFG | Inferior Frontal Gyrus | R | (48, 18, 8) | 44 | 27 |
| 14 | dlPFC | Dorsolateral Prefrontal Cortex | bilateral | (42, 32, 30) | 46 | 13 |
| 15 | vmPFC | Ventromedial Prefrontal Cortex | bilateral | (2, 46, -10) | 10 | 17 |
| 16 | OFC | Orbitofrontal Cortex | bilateral | (28, 34, -16) | 11 | 15 |
| 17 | ACC | Anterior Cingulate Cortex | bilateral | (2, 30, 28) | 32 | 12 |
| 18 | SMA | Supplementary Motor Area | bilateral | (2, -2, 56) | 6 | 21 |
| 19 | PMC | Premotor Cortex | bilateral | (46, 0, 48) | 6 | 14 |
| 20 | AG | Angular Gyrus | bilateral | (48, -60, 30) | 39 | 8 |
| 21 | TP | Temporal Pole | bilateral | (42, 12, -32) | 38 | 7 |
| 22 | IC | Inferior Colliculus | bilateral | (0, -34, -8) | -- | 12 |
| 23 | AN | Auditory Nerve | bilateral | (8, -26, -24) | -- | 6 |
| 24 | CN | Cochlear Nucleus | bilateral | (10, -38, -32) | -- | 5 |
| 25 | SOC | Superior Olivary Complex | bilateral | (6, -34, -24) | -- | 4 |
| 26 | PAG | Periaqueductal Gray | bilateral | (0, -30, -10) | -- | 8 |
