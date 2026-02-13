# R3 Standards Compliance Documentation

**Scope**: ISO, AES, DIN, and ITU standard mapping for the R3 Spectral Architecture (128D).
**Phase**: 3C -- Documentation Layer
**Status**: Active

---

## Contents

| File | Description | Key Content |
|------|-------------|-------------|
| [ComplianceMatrix.md](ComplianceMatrix.md) | ISO/AES/DIN/ITU standard mapping | Standard-to-feature table, compliance levels, mel-based limitation notes |
| [QualityTiers.md](QualityTiers.md) | Feature quality tier system | Proxy/Approximate/Standard/Reference tiers, all 128 features classified, Phase 6 upgrade paths |

---

## Relationship to Other Documentation

| Related Doc | Relationship |
|-------------|--------------|
| `R3-V2-DESIGN.md` | Architectural source -- feature specifications and psychoacoustic references |
| `R3-DSP-SURVEY-TOOLS.md` | Toolkit survey -- comparison matrix of library capabilities |
| `R3-CROSSREF.md` | Three-perspective synthesis -- revision decisions and quality flags |
| `Validation/BenchmarkPlan.md` | Experimental validation plan for features requiring benchmark testing |
| `Migration/V1-to-V2.md` | Code migration guide -- changes to constants.py, dimension_map.py |

---

## Compliance Philosophy

R3 operates exclusively on mel-spectrogram input (`mel: (B, 128, T)` at 44.1 kHz, hop=256).
All psychoacoustic standard implementations are therefore **mel-based approximations**, not
full standard-compliant implementations. The compliance levels documented in ComplianceMatrix.md
reflect this fundamental constraint:

- **Full**: The R3 formula follows the published algorithm exactly (rare; mainly signal-level features).
- **Approximate**: The R3 formula captures the same perceptual dimension but uses mel-domain shortcuts.
- **Partial**: Only a subset of the standard is addressed.
- **Reference Only**: The standard informed the design but the implementation diverges significantly.

The QualityTiers.md document provides a finer-grained per-feature quality assessment independent
of formal standards, using four tiers: Proxy, Approximate, Standard, and Reference.

---

## Revision History

| Date | Change |
|------|--------|
| 2026-02-13 | Initial creation (Phase 3C) |
