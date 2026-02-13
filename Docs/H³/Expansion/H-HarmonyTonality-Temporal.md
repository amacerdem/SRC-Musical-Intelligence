# Group H: Harmony & Tonality [75:87] -- Temporal Demand Analysis

> Version 2.0.0 | Updated 2026-02-13

## 1. Group Summary

Group H introduces 12 features spanning tonal hierarchy, tonnetz geometry, voice leading mechanics, and harmonic rhythm. These features encode the harmonic language of music -- chord identity, key context, tonal motion, and syntactic structure.

| Feature | Index | Dim | Quality | Description |
|---------|:-----:|:---:|:-------:|-------------|
| key_clarity | 75 | 1D | A | Strength of estimated key (KS correlation peak) |
| tonnetz_fifth_x | 76 | 1D | S | Tonnetz fifth axis, cosine component |
| tonnetz_fifth_y | 77 | 1D | S | Tonnetz fifth axis, sine component |
| tonnetz_minor_x | 78 | 1D | S | Tonnetz minor third axis, cosine component |
| tonnetz_minor_y | 79 | 1D | S | Tonnetz minor third axis, sine component |
| tonnetz_major_x | 80 | 1D | S | Tonnetz major third axis, cosine component |
| tonnetz_major_y | 81 | 1D | S | Tonnetz major third axis, sine component |
| voice_leading_distance | 82 | 1D | S | Minimal voice leading distance between successive chroma frames |
| harmonic_change | 83 | 1D | S | Harmonic change detection function (HCDF) magnitude |
| tonal_stability | 84 | 1D | A | Stability of tonal context over running window |
| diatonicity | 85 | 1D | A | Proportion of chroma energy on diatonic scale degrees |
| syntactic_irregularity | 86 | 1D | A | Harmonic syntax violation strength (unexpected chord transitions) |

**Dependencies**: F chroma (pipeline stage 1). H group is computed at pipeline stage 2.

**Quality distribution**: 4 Approximate (key_clarity, tonal_stability, diatonicity, syntactic_irregularity), 8 Standard (tonnetz 6D, voice_leading_distance, harmonic_change). The tonnetz and voice leading features are direct geometric computations with no approximation.

---

## 2. Temporal Relevance

Group H features are among the most temporally structured in the entire R3 space. Harmonic rhythm -- the rate at which chords change -- is one of music's primary hierarchical temporal structures, operating simultaneously at beat, phrase, and section timescales. Key trajectory (modulation) operates at section and movement timescales, making it one of the slowest-evolving tonal parameters. Tonnetz position traces tonal motion through a continuous geometric space, and its trajectory over time encodes chord progression patterns that are central to Western tonal music.

Syntactic irregularity is of particular interest for H3 temporal analysis because it signals harmonic surprise -- moments where the actual chord deviates from the syntactically expected chord. This is strongly tied to predictive coding models (NDU, PCU) and emotional response models (IMU). The temporal profile of syntactic irregularity across a piece traces the composer's manipulation of harmonic expectation, a core driver of musical affect.

Key temporal questions H3 addresses for Group H:
- How fast is the harmonic rhythm at different structural levels? (harmonic_change at Meso-Macro)
- Is the key clarifying or dissolving over this section? (key_clarity trend at Macro)
- What is the trajectory of tonal motion through tonnetz space? (tonnetz velocity at Meso)
- Are harmonic surprises clustering or dispersing? (syntactic_irregularity std at Macro)
- Is there cyclic modulation (e.g., circle of fifths progressions)? (tonnetz periodicity at Macro)

---

## 3. Horizon Mapping

| Feature | Indices | Horizons | Band | Rationale |
|---------|---------|----------|------|-----------|
| key_clarity [75] | 1D | H12, H16, H18, H20 | Meso-Macro | Key perception stabilizes at phrase/section scale; requires accumulated chroma evidence |
| tonnetz [76:82] | 6D | H9, H12, H16, H18 | Meso-Macro | Tonal motion at chord/phrase/section scale; sub-beat tonnetz is noise |
| voice_leading_distance [82] | 1D | H6, H9, H12 | Micro-Meso | Voice leading operates at chord-to-chord (beat) timescale |
| harmonic_change [83] | 1D | H6, H9, H12 | Micro-Meso | HCDF at beat/phrase scale captures harmonic rhythm |
| tonal_stability [84] | 1D | H16, H18, H20 | Macro | Stability assessment requires section-scale context |
| diatonicity [85] | 1D | H12, H16, H18 | Meso-Macro | Chromatic vs diatonic character meaningful at phrase/section |
| syntactic_irregularity [86] | 1D | H6, H9, H12, H16 | Micro-Macro | Harmonic syntax violations operate at multiple timescales |

### Horizon Heatmap

```
Horizon  H6   H9   H12  H16  H18  H20
Band     Mic  Meso Meso Mac  Mac  Mac
         ================================
key_clarity       .    .   [X]  [X]  [X]  [X]
tonnetz (6D)      .   [X]  [X]  [X]  [X]   .
voice_leading    [X]  [X]  [X]   .    .    .
harmonic_change  [X]  [X]  [X]   .    .    .
tonal_stability   .    .    .   [X]  [X]  [X]
diatonicity       .    .   [X]  [X]  [X]   .
syntactic_irreg  [X]  [X]  [X]  [X]   .    .
         ================================
```

**Key observations**:
- H12 (525ms, phrase boundary) is the most demanded horizon -- 5 of 7 feature groups use it.
- H16 (1s) is demanded by 5 of 7, reflecting harmony's structural timescale.
- No Micro-only demand below H6; harmonic features require minimum beat-level context.
- No Ultra demand; harmonic features are consumed by Macro-level mechanisms.

---

## 4. Morph Profiles

### Tonnetz [76:82]
| Morph | ID | Demand | Rationale |
|-------|----|:------:|-----------|
| Value | M0 | High | Instantaneous tonal position in tonnetz space |
| Mean | M1 | High | Average position = estimated tonal center |
| Velocity | M8 | High | Rate of tonal motion (chord change speed) |
| Periodicity | M14 | Medium | Cyclic modulation patterns (circle progressions) |
| Trend | M18 | Medium | Directional drift through tonal space |

### Harmonic Change [83]
| Morph | ID | Demand | Rationale |
|-------|----|:------:|-----------|
| Value | M0 | High | Instantaneous harmonic change magnitude |
| Mean | M1 | High | Mean rate = harmonic rhythm |
| Max | M4 | Medium | Strongest harmonic event in window |
| Periodicity | M14 | Medium | Regular chord rhythm detection |
| Peaks | M22 | Medium | Count of chord changes in window |

### Key Clarity [75]
| Morph | ID | Demand | Rationale |
|-------|----|:------:|-----------|
| Value | M0 | High | Current key clarity |
| Mean | M1 | High | Average key clarity over section |
| Trend | M18 | High | Key clarifying (rising) or dissolving (falling) |
| Stability | M19 | Medium | Consistency of key clarity |

### Syntactic Irregularity [86]
| Morph | ID | Demand | Rationale |
|-------|----|:------:|-----------|
| Value | M0 | High | Instantaneous syntax violation strength |
| Mean | M1 | High | Average surprise level |
| Std | M2 | High | Prediction error variability |
| Max | M4 | High | Strongest syntax violation (peak surprise) |
| Velocity | M8 | Medium | Rate of surprise change |

---

## 5. Law Preferences

| Law | Code | Primary Users | H Group Application |
|-----|------|---------------|---------------------|
| L0 (Memory) | Past | IMU, NDU | Tonal center estimated from accumulated past chroma; harmonic memory builds key context from what has been heard |
| L1 (Prediction) | Future | PCU | Anticipating harmonic resolution; predicting upcoming chord transitions and tonal motion |
| L2 (Integration) | Both | SPU | Bidirectional tonal stability assessment; key estimation benefits from both preceding and following context |

**Distribution**: L0 dominates for memory-oriented consumers (IMU tonal emotional encoding, NDU accumulated syntactic context). L1 is critical for PCU's predictive coding models (HTP, CHPI). L2 is used where bidirectional context improves tonal stability estimates.

---

## 6. Consuming Units

| Unit | Models | H Features | Mechanism | Priority |
|------|:------:|-----------|-----------|:--------:|
| NDU | SDD, SSNI, EDNR, NSGS, NSAD | syntactic_irregularity, tonnetz, key_clarity | ASA, SYN | High |
| PCU | HTP, CHPI, UDP, ICEM | tonnetz, harmonic_change, key_clarity, syntactic_irregularity | TPC, MEM, PPC | Medium-High |
| IMU | MEAMN, PNH, MSPBA, PMIM | tonnetz, tonal_stability, key_clarity, syntactic_irregularity | MEM, TMH, SYN | Medium-High |
| RPU | Models reading H via pathways | key_clarity, tonal_stability | Various | Medium |

### Demand Concentration

NDU is the primary consumer of Group H features. The Novelty Detection Unit's core function is identifying unexpected events, and syntactic_irregularity directly encodes harmonic unexpectedness. NDU models (especially SSNI -- Spectral-Syntactic Novelty Integration, and EDNR -- Expectation-Deviation Novelty Response) demand syntactic_irregularity at H6 through H16, tracking surprise at beat, phrase, and section scales via ASA and SYN mechanisms.

PCU (Predictive Coding Unit) is the second-largest consumer, using tonnetz and harmonic_change features to build harmonic prediction models. HTP (Harmonic Trajectory Prediction) and CHPI (Contextual Harmonic Prediction Integration) demand tonnetz velocity and trend morphs at Meso-Macro horizons under L1 (Prediction).

---

## 7. Estimated Tuple Count

| Source | Features | Horizons | Morphs | Laws | Est. Tuples |
|--------|:--------:|:--------:|:------:|:----:|:-----------:|
| Tonnetz (6D) | 6 | 4 (H9,H12,H16,H18) | 5 (M0,M1,M8,M14,M18) | 2 (L0,L1) | ~240 |
| Key clarity (1D) | 1 | 4 (H12,H16,H18,H20) | 4 (M0,M1,M18,M19) | 2 (L0,L2) | ~32 |
| Syntactic irregularity (1D) | 1 | 4 (H6,H9,H12,H16) | 5 (M0,M1,M2,M4,M8) | 2 (L0,L1) | ~40 |
| Harmonic change (1D) | 1 | 3 (H6,H9,H12) | 5 (M0,M1,M4,M14,M22) | 2 (L0,L2) | ~30 |
| Voice leading (1D) | 1 | 3 (H6,H9,H12) | 3 (M0,M1,M8) | 2 (L0,L2) | ~18 |
| Tonal stability (1D) | 1 | 3 (H16,H18,H20) | 3 (M0,M1,M19) | 2 (L0,L2) | ~18 |
| Diatonicity (1D) | 1 | 3 (H12,H16,H18) | 3 (M0,M1,M18) | 2 (L0,L2) | ~18 |
| **Total** | **12** | | | | **~396** |

Deduplication across units (same tuple demanded by NDU and PCU computed once) reduces net count by ~15-25%. **Estimated net: ~500-800 tuples** after accounting for multi-unit overlap and tier-dependent morph expansion (alpha models demand more morphs than gamma).

Tonnetz (6D) generates the bulk of H group tuples (~60%) due to its high dimensionality. Scalar features contribute the remaining ~40%.

---

## 8. Cross-References

- **H3 Architecture**: [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md)
- **Expansion Index**: [00-INDEX.md](00-INDEX.md)
- **R3 Feature Catalog**: [../../R3/Registry/FeatureCatalog.md](../../R3/Registry/FeatureCatalog.md)
- **Horizon Catalog**: [../Registry/HorizonCatalog.md](../Registry/HorizonCatalog.md)
- **Morph Catalog**: [../Registry/MorphCatalog.md](../Registry/MorphCatalog.md)
- **Law Catalog**: [../Registry/LawCatalog.md](../Registry/LawCatalog.md)
- **NDU Demand Profile**: [../Demand/NDU-H3-DEMAND.md](../Demand/NDU-H3-DEMAND.md)
- **PCU Demand Profile**: [../Demand/PCU-H3-DEMAND.md](../Demand/PCU-H3-DEMAND.md)
- **IMU Demand Profile**: [../Demand/IMU-H3-DEMAND.md](../Demand/IMU-H3-DEMAND.md)
- **RPU Demand Profile**: [../Demand/RPU-H3-DEMAND.md](../Demand/RPU-H3-DEMAND.md)
- **Demand Address Space**: [../Registry/DemandAddressSpace.md](../Registry/DemandAddressSpace.md)
- **Pipeline / WarmUp**: [../Pipeline/WarmUp.md](../Pipeline/WarmUp.md)
- **I Group (related -- information/surprise)**: [I-InformationSurprise-Temporal.md](I-InformationSurprise-Temporal.md)
- **F Group (dependency -- chroma)**: [F-PitchChroma-Temporal.md](F-PitchChroma-Temporal.md)

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial Group H temporal demand analysis (Phase 4G) |
