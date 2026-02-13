# L³ Vocabulary — Index

**Scope**: The 64-gradation vocabulary system that translates continuous polarity signals into discrete human-readable terms.
**Version**: 2.1.0
**Updated**: 2026-02-13

---

## Overview

The Vocabulary subsystem documents how 12 bipolar polarity axes (from the ζ zeta group) are quantized into 64 discrete gradations by the η (eta) group, producing human-readable semantic terms for musical experience description.

**Key numbers**:

| Parameter | Value | Rationale |
|-----------|:-----:|-----------|
| Polarity axes | 12 | From ζ (zeta): valence, arousal, tension, power, wanting, liking, novelty, complexity, beauty, groove, stability, engagement |
| Gradations per axis | 64 | 6 bits; step size 1/64 = 1.56%, below human JND (~3%) |
| Bands per axis | 8 | 8 gradations per band; bands 0-3 negative, band 4 neutral, bands 5-7 positive |
| Vocabulary terms | 96 | 12 axes x 8 band-level terms |
| Total information | 72 bits | 6 bits/axis x 12 axes; state space = 64^12 = 2^72 |

**Pipeline position**: ζ polarity [-1,+1] --> η quantization [0,1] --> vocabulary term lookup

**Code**: `mi_beta/language/groups/eta.py` (176 lines)

---

## Files

| File | Description | Lines |
|------|-------------|:-----:|
| [TermCatalog.md](TermCatalog.md) | Complete 12x8 term table matching `AXIS_TERMS` in eta.py | ~200 |
| [GradationSystem.md](GradationSystem.md) | 64-level quantization design: JND, Weber's Law, bit budget, formulas | ~150 |
| [AxisDefinitions.md](AxisDefinitions.md) | 12 polarity axes: poles, source formulas, subcategories, citations | ~180 |

---

## Cross-References

| Related Document | Location |
|-----------------|----------|
| η group specification | [Groups/Dependent/Eta.md](../Groups/Dependent/Eta.md) |
| ζ group specification | [Groups/Dependent/Zeta.md](../Groups/Dependent/Zeta.md) |
| Epistemology: Vocabulary | [Epistemology/Vocabulary.md](../Epistemology/Vocabulary.md) |
| Epistemology: Polarity | [Epistemology/Polarity.md](../Epistemology/Polarity.md) |
| Dimension Catalog (all 104D) | [Registry/DimensionCatalog.md](../Registry/DimensionCatalog.md) |
| Group Map | [Registry/GroupMap.md](../Registry/GroupMap.md) |
| L³ Master Index | [00-INDEX.md](../00-INDEX.md) |
| η code | `mi_beta/language/groups/eta.py` |
| ζ code | `mi_beta/language/groups/zeta.py` |

---

**Parent**: [L³ 00-INDEX.md](../00-INDEX.md)
