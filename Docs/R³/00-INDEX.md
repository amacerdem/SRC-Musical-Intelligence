# R³ Spectral Architecture Index

**Status**: Skeleton — will be populated after Phase 1 (C³ model revision)
**Current dimensions**: 49D (5 groups)
**Version**: 2.0.0

---

## Current R³ Space (49D)

| Group | Name | Dims | Range | Source |
|-------|------|------|-------|--------|
| A | Consonance | 7D | [0:7] | Psychoacoustic harmony (Plomp & Levelt) |
| B | Energy | 5D | [7:12] | Amplitude dynamics (RMS, loudness) |
| C | Timbre | 9D | [12:21] | Spectral shape (warmth, brightness, tristimulus) |
| D | Change | 4D | [21:25] | Temporal derivatives (flux, onset) |
| E | Interactions | 24D | [25:49] | Cross-group coupling |

## Detailed Specs (to be created in Phase 2)

- [ ] `A-CONSONANCE.md`
- [ ] `B-ENERGY.md`
- [ ] `C-TIMBRE.md`
- [ ] `D-CHANGE.md`
- [ ] `E-INTERACTIONS.md`
- [ ] `F-{NEW}.md` (if gaps found)

## Per-Unit Mappings (to be created in Phase 2)

- [ ] `mappings/SPU-R3-MAP.md`
- [ ] `mappings/STU-R3-MAP.md`
- [ ] `mappings/IMU-R3-MAP.md`
- [ ] `mappings/ASU-R3-MAP.md`
- [ ] `mappings/NDU-R3-MAP.md`
- [ ] `mappings/MPU-R3-MAP.md`
- [ ] `mappings/PCU-R3-MAP.md`
- [ ] `mappings/ARU-R3-MAP.md`
- [ ] `mappings/RPU-R3-MAP.md`

## Gap Analysis

See [R3-GAP-LOG.md](R3-GAP-LOG.md) for running log of gaps found during C³ revision.
