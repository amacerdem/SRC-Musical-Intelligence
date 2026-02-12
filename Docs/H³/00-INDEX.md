# H³ Temporal Architecture Index

**Status**: Skeleton — will be populated after Phase 1 (C³ model revision)
**Theoretical space**: 2304D (32 horizons x 24 morphs x 3 laws)
**Actual usage**: Sparse (~1-5% per model)
**Version**: 2.0.0

---

## H³ Space Overview

### 32 Horizons (temporal scales)

| Band | Horizons | Duration | Musical Meaning |
|------|----------|----------|-----------------|
| Sub-beat | H0-H5 | 5.8ms - 46.4ms | Onset, attack, spectral transient |
| Beat | H6-H11 | 200ms - 450ms | Beat, pulse, tactus |
| Phrase | H12-H17 | 525ms - 1500ms | Motif, measure, phrase |
| Section | H18-H23 | 2s - 25s | Section, theme, passage |
| Form | H24-H31 | 36s - 981s | Movement, piece, large-scale form |

### 24 Morphs (statistical features)

M0-M7: Distribution (value, mean, std, median, max, range, skewness, kurtosis)
M8-M13: Dynamics (velocity, velocity_mean, velocity_std, acceleration, acceleration_mean, acceleration_std)
M14-M23: Shape (periodicity, smoothness, curvature, shape_period, trend, stability, entropy, zero_crossings, peaks, symmetry)

### 3 Laws (temporal perspective)

| Law | Name | Direction |
|-----|------|-----------|
| L0 | Memory | Past → Now (causal) |
| L1 | Prediction | Now → Future (anticipatory) |
| L2 | Integration | Past ↔ Future (bidirectional) |

## Detailed Specs (to be created in Phase 3)

- [ ] `H3-TEMPORAL-ARCHITECTURE.md`
- [ ] `H0-H5-SUB-BEAT.md`
- [ ] `H6-H11-BEAT.md`
- [ ] `H12-H17-PHRASE.md`
- [ ] `H18-H23-SECTION.md`
- [ ] `H24-H31-FORM.md`

## Per-Unit Demands (to be created in Phase 3)

- [ ] `demands/SPU-H3-DEMAND.md`
- [ ] `demands/STU-H3-DEMAND.md`
- [ ] `demands/IMU-H3-DEMAND.md`
- [ ] `demands/ASU-H3-DEMAND.md`
- [ ] `demands/NDU-H3-DEMAND.md`
- [ ] `demands/MPU-H3-DEMAND.md`
- [ ] `demands/PCU-H3-DEMAND.md`
- [ ] `demands/ARU-H3-DEMAND.md`
- [ ] `demands/RPU-H3-DEMAND.md`
