# H3 Temporal Bands -- Cross-Band Index

**Version**: 2.0.0
**Bands**: 4 (Micro, Meso, Macro, Ultra)
**Horizons**: 32 (H0-H31), 5.8ms to 981s
**Frame rate**: 172.27 Hz (5.8 ms/frame)
**Updated**: 2026-02-13

---

## Band Summary

| Band | Horizons | Duration | Frames | Mechanisms | Primary Units | Musical Scale |
|------|----------|----------|--------|------------|---------------|---------------|
| **Micro** | H0-H7 | 5.8ms - 250ms | 1-43 | PPC, ASA, TPC, BEP, AED (at H6) | SPU, ASU, NDU | Onset, attack, transient |
| **Meso** | H8-H15 | 300ms - 800ms | 52-138 | BEP, TPC, SYN, ASA, CPD | STU, MPU, SPU | Beat, quarter note, motif |
| **Macro** | H16-H23 | 1s - 25s | 172-4,307 | TMH, MEM, C0P, SYN, AED, CPD, TPC | IMU, ARU, PCU | Measure, section, passage |
| **Ultra** | H24-H31 | 36s - 981s | 6,202-168,999 | MEM (sparse) | IMU (sparse) | Movement, piece, full work |

---

## Cross-Band Comparison

### Mechanism Density

| Band | Distinct Mechanisms | Peak Horizon | Mechanisms at Peak |
|------|:-------------------:|--------------|:------------------:|
| Micro | 5 | H6 (200ms) | 5 (PPC, TPC, BEP, ASA, AED) |
| Meso | 5 | H9 (350ms) | 3 (BEP, ASA, CPD) |
| Macro | 7 | H16 (1,000ms) | 5 (TMH, TPC, SYN, AED, CPD) |
| Ultra | 1 | H25 (60s) | 1 (MEM) |

**Observation**: H6 and H16 are the two most mechanism-dense horizons in the system. H6 bridges sensory and beat processing; H16 bridges phrase and section processing. These two horizons serve as convergence points where multiple mechanisms share temporal context.

### Unit Coverage

| Band | Units Active | Estimated Tuples | % of Total |
|------|:------------:|:----------------:|:----------:|
| Micro | SPU, ASU, NDU | ~1,200 | ~14% |
| Meso | STU, MPU, SPU, ASU, ARU | ~2,400 | ~28% |
| Macro | IMU, ARU, PCU, STU, NDU, RPU | ~4,200 | ~49% |
| Ultra | IMU | ~800 | ~9% |

Macro is the densest band by tuple count, reflecting the cognitive importance of 1-25s timescales for musical understanding.

### Morph Applicability

| Band | Reliable Morphs | Unreliable Morphs | Rationale |
|------|:---------------:|:------------------:|-----------|
| Micro | M0, M1, M8 | M14, M16, M17, M19, M20, M22, M23 | Too few frames for periodicity, curvature, entropy |
| Meso | All 24 | None | Sufficient frames for all statistical descriptors |
| Macro | M1, M2, M18, M19, M20 preferred | None unreliable, but M8/M9 less informative | Statistical summaries dominate over instantaneous dynamics |
| Ultra | M1, M18, M19 | M8, M9, M14, M16, M22 | Only simple aggregates meaningful at 36s+ |

---

## Band Transition Boundaries

| Transition | Horizon | Duration | What Changes |
|------------|---------|----------|--------------|
| Micro --> Meso | H7/H8 | 250-300ms | From sensory onset processing to beat-period entrainment. Motor system engagement begins. |
| Meso --> Macro | H15/H16 | 800ms-1s | From beat/motif to measure/section. Higher-order predictive models engage. Memory encoding begins. |
| Macro --> Ultra | H23/H24 | 25-36s | From section to movement/piece. Extremely sparse demand. Long-term form processing. |

**Key insight**: Transitions are not sharp boundaries. Mechanisms like TPC (H6-H16) and MEM (H18-H25) deliberately span band boundaries to provide continuity of temporal context across scales.

---

## Neuroscience Oscillation Correspondence

| Band | Neural Oscillation | Frequency Range | Brain Regions | Key References |
|------|-------------------|-----------------|---------------|----------------|
| Micro | Gamma | 30-100 Hz | A1, auditory nerve | Onset response, phase-locking |
| Meso | Beta-Theta | 4-30 Hz | Motor cortex, basal ganglia | Grahn & Brett 2007, Large & Palmer 2002 |
| Macro | Delta-Theta | 1-4 Hz | Auditory cortex, hippocampus | Norman-Haignere 2022, Golesorkhi 2021 |
| Ultra | Infra-slow | <0.1 Hz | Default mode network, PFC | Long-term memory retrieval |

---

## Directory Contents

| File | Description |
|------|-------------|
| [Micro/00-INDEX.md](Micro/00-INDEX.md) | Micro band overview (H0-H7) |
| [Micro/H0-H5-SubBeat.md](Micro/H0-H5-SubBeat.md) | Sub-beat horizons |
| [Micro/H6-H7-BeatSubdivision.md](Micro/H6-H7-BeatSubdivision.md) | Beat subdivision horizons |
| [Meso/00-INDEX.md](Meso/00-INDEX.md) | Meso band overview (H8-H15) |
| [Meso/H8-H11-BeatPeriod.md](Meso/H8-H11-BeatPeriod.md) | Beat period horizons |
| [Meso/H12-H15-Phrase.md](Meso/H12-H15-Phrase.md) | Phrase-level horizons |
| [Macro/00-INDEX.md](Macro/00-INDEX.md) | Macro band overview (H16-H23) |
| [Macro/H16-H17-Measure.md](Macro/H16-H17-Measure.md) | Measure-level horizons |
| [Macro/H18-H23-Section.md](Macro/H18-H23-Section.md) | Section horizons |
| [Ultra/00-INDEX.md](Ultra/00-INDEX.md) | Ultra band overview (H24-H31) |
| [Ultra/H24-H28-Movement.md](Ultra/H24-H28-Movement.md) | Movement-level horizons |
| [Ultra/H29-H31-Piece.md](Ultra/H29-H31-Piece.md) | Piece-level horizons |

## Cross-References

| Document | Location |
|----------|----------|
| Horizon catalog (all 32) | [../Registry/HorizonCatalog.md](../Registry/HorizonCatalog.md) |
| Morph catalog (all 24) | [../Registry/MorphCatalog.md](../Registry/MorphCatalog.md) |
| Law catalog (L0-L2) | [../Registry/LawCatalog.md](../Registry/LawCatalog.md) |
| H3 master index | [../00-INDEX.md](../00-INDEX.md) |
| R3 feature catalog | [../../R³/Registry/FeatureCatalog.md](../../R³/Registry/FeatureCatalog.md) |
| C3 mechanism index | [../../C³/Mechanisms/00-INDEX.md](../../C³/Mechanisms/00-INDEX.md) |
