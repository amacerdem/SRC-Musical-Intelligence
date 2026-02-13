# Group F: Pitch & Chroma -- Temporal Demand Analysis

> Version 2.0.0 | Updated 2026-02-13

## 1. Group Summary

| Property | Value |
|----------|-------|
| **Group** | F: Pitch & Chroma |
| **Dimensions** | 16D |
| **Indices** | [49:65] |
| **Temporal Priority** | HIGH |
| **Est. New Tuples** | ~800-1,200 |
| **Primary Consumers** | SPU, IMU, PCU |

### Feature Inventory

| Feature | Index | Dim | Quality Tier | Description |
|---------|:-----:|:---:|:------------:|-------------|
| chroma_C | 49 | 1D | A | Chroma energy: C |
| chroma_Cs | 50 | 1D | A | Chroma energy: C#/Db |
| chroma_D | 51 | 1D | A | Chroma energy: D |
| chroma_Ds | 52 | 1D | A | Chroma energy: D#/Eb |
| chroma_E | 53 | 1D | A | Chroma energy: E |
| chroma_F | 54 | 1D | A | Chroma energy: F |
| chroma_Fs | 55 | 1D | A | Chroma energy: F#/Gb |
| chroma_G | 56 | 1D | A | Chroma energy: G |
| chroma_Gs | 57 | 1D | A | Chroma energy: G#/Ab |
| chroma_A | 58 | 1D | A | Chroma energy: A |
| chroma_As | 59 | 1D | A | Chroma energy: A#/Bb |
| chroma_B | 60 | 1D | A | Chroma energy: B |
| pitch_height | 61 | 1D | A | Perceptual pitch height (weighted centroid) |
| pitch_class_entropy | 62 | 1D | S | Shannon entropy over 12-bin chroma distribution |
| pitch_salience | 63 | 1D | A | Harmonic peak prominence relative to noise floor |
| inharmonicity_index | 64 | 1D | A | Deviation of partials from harmonic series |

**Quality tiers**: A = Approximate (15 features), S = Standard (1 feature: pitch_class_entropy).

**Implementation**: Mel-to-frequency exponential mapping, Gaussian soft-assignment via 128x12 chroma projection matrix, L1 normalization. Pitch height derived as energy-weighted frequency centroid. Pitch class entropy computed as Shannon entropy of the normalized 12-bin chroma vector.

---

## 2. Temporal Relevance

Group F features exhibit temporal dynamics across multiple timescales, making them strong candidates for H3 demand:

- **Chroma vector** ([49:61]): The 12-bin chroma profile evolves as chords change, keys modulate, and tonal centers shift. Chord-level chroma changes occur at beat/phrase timescales (H6-H12). Key-level changes occur at section timescales (H16-H18). Cyclic tonal returns (e.g., verse-chorus alternation) operate at phrase-to-section scales (H12-H18).

- **Pitch height** ([61]): The overall pitch register contour reflects melodic shape (note-level, H3-H6), phrase contour (H9-H12), and registral planning across sections (H16). Pitch height velocity captures melodic interval direction and magnitude.

- **Pitch class entropy** ([62]): Tonal ambiguity evolves slowly. High entropy (atonal/chromatic passages) versus low entropy (diatonic/tonal passages) shifts at phrase-to-section boundaries. Entropy trend over Macro horizons captures large-scale tonal architecture (e.g., development section increasing entropy, recapitulation decreasing it).

- **Pitch salience** ([63]): Salience varies with textural complexity. Monophonic passages yield high salience; dense polyphonic or noise-dominated passages reduce it. Changes correlate with textural shifts at beat/phrase timescales (H6-H12).

- **Inharmonicity index** ([64]): Varies with instrument type (piano has high inharmonicity, strings have low) and register (higher registers increase inharmonicity). Changes occur at phrase-to-section timescales as instrumentation shifts.

---

## 3. Horizon Mapping

| Feature | Indices | Horizons | Band | Rationale |
|---------|---------|----------|------|-----------|
| chroma [49:61] | 12D | H6, H9, H12, H16, H18 | Micro-Macro | Chord duration (H6-H9), phrase tonal center (H12-H16), section key (H18) |
| pitch_height [61] | 1D | H3, H6, H9 | Micro-Meso | Note-level pitch contour, melodic shape at beat/motif scale |
| pitch_class_entropy [62] | 1D | H12, H16, H18 | Meso-Macro | Tonal ambiguity evolves at phrase/section scale |
| pitch_salience [63] | 1D | H6, H9, H12 | Micro-Meso | Salience changes with textural complexity at beat/phrase scale |
| inharmonicity_index [64] | 1D | H9, H12, H16 | Meso-Macro | Instrument/register shifts at phrase timescales |

### Horizon Coverage Heatmap

```
Horizon  H0   H3   H6   H9  H11  H12  H16  H18  H20  H22  H25
Band     |-- Micro --|   |--Meso--|   |---- Macro ----|  Ultra
         ============================================
chroma    .   .    [X]  [X]   .   [X]  [X]  [X]   .    .    .
pitch_h   .  [X]   [X]  [X]   .    .    .    .    .    .    .
pc_ent    .   .     .    .    .   [X]  [X]  [X]   .    .    .
p_sal     .   .    [X]  [X]   .   [X]   .    .    .    .    .
inharm    .   .     .   [X]   .   [X]  [X]   .    .    .    .
         ============================================
Count     0   1     3    4    0    4    3    2    0    0    0
```

- **H9** is the most demanded horizon (4/5 feature subgroups) -- the beat/motif timescale where melodic and harmonic changes are most salient.
- **H12** ties with H9 (4/5) -- the phrase boundary timescale where tonal center shifts become apparent.
- **H3** is demanded only by pitch_height for note-level melodic contour.
- **No Ultra demand**: Pitch and chroma features do not require 36s+ observation windows.

---

## 4. Morph Profiles

### Chroma ([49:61])

| Morph | ID | Usage |
|-------|----|-------|
| Value | M0 | Instantaneous chroma vector (current chord identity) |
| Mean | M1 | Prevailing key center over horizon (averaged chroma = key profile) |
| Std | M2 | Tonal instability (high std = chromatic or modulatory passage) |
| Velocity | M8 | Harmonic rhythm rate (chroma change speed = chord change frequency) |
| Periodicity | M14 | Cyclic tonal patterns (verse/chorus key alternation, circle-of-fifths progressions) |
| Trend | M18 | Modulation direction (systematic shift in chroma centroid over time) |

### Pitch Height ([61])

| Morph | ID | Usage |
|-------|----|-------|
| Value | M0 | Instantaneous pitch register |
| Mean | M1 | Average pitch height over horizon (registral center) |
| Velocity | M8 | Melodic contour slope (ascending vs. descending movement) |
| Skewness | M6 | Contour shape asymmetry (arch vs. trough melodic profiles) |
| Acceleration | M11 | Melodic curvature (rate of change of contour direction) |

### Pitch Salience ([63])

| Morph | ID | Usage |
|-------|----|-------|
| Value | M0 | Instantaneous harmonic prominence |
| Mean | M1 | Average salience over horizon (overall harmonic clarity) |
| Std | M2 | Texture variation (alternation between clear and noisy passages) |

### Pitch Class Entropy ([62])

| Morph | ID | Usage |
|-------|----|-------|
| Value | M0 | Instantaneous tonal ambiguity |
| Mean | M1 | Average tonal certainty over horizon |
| Trend | M18 | Increasing/decreasing tonal certainty (e.g., building toward cadence) |

### Inharmonicity Index ([64])

| Morph | ID | Usage |
|-------|----|-------|
| Value | M0 | Instantaneous inharmonicity level |
| Mean | M1 | Average inharmonicity over horizon (instrument character) |
| Velocity | M8 | Rate of inharmonicity change (instrument/register transition speed) |

---

## 5. Law Preferences

| Law | Name | F Group Usage | Primary Models |
|-----|------|--------------|----------------|
| L0 | Memory | Accumulated tonal center from past context. Chroma memory builds a running key estimate. Most common law for F group features across all consuming units. | IMU (MEM), STU (TMH) |
| L1 | Prediction | Anticipating upcoming key area or pitch trajectory. PCU models predict next chord or tonal region based on current trajectory. | PCU (PPC, TPC) |
| L2 | Integration | Bidirectional tonal context for tonal stability assessment. Spectral integration models use both past and future chroma context. | SPU (PPC, TPC) |

### Law Distribution

- **L0 dominates** for chroma features: ~55% of F group tuples. Tonal perception is primarily retrospective -- what key have we been in?
- **L1 is secondary**: ~25% of F group tuples. Predictive models need chroma prediction for harmonic expectation.
- **L2 is tertiary**: ~20% of F group tuples. Integration is used by SPU for bidirectional spectral template matching.

---

## 6. Consuming Units

| Unit | Models | F Features | Mechanism | Horizons | Priority |
|------|:------:|-----------|-----------|----------|:--------:|
| SPU | BCH, PSCL, PCCR, STAI, TSCP, MIAA | chroma, pitch_height, pitch_salience | PPC (H0,H3,H6), TPC (H6,H12,H16) | H3-H16 | High |
| IMU | TPRD, DMMS, PNH, MEAMN | chroma, pitch_height, inharmonicity_index | MEM (H18,H20,H22), TMH (H16,H18) | H16-H22 | Medium |
| PCU | SPH, CHPI, PWUP | chroma, pitch_salience, inharmonicity_index | PPC (H0,H3,H6), TPC (H6,H12,H16) | H3-H16 | Medium |
| NDU | (indirect via H group) | pitch_class_entropy | -- | H12-H18 | Low |
| ASU | (limited) | pitch_salience | ASA (H3,H6,H9) | H3-H9 | Low |

### Unit-Level Notes

- **SPU** is the heaviest F consumer: 6 models across both PPC and TPC mechanisms. Chroma and pitch features are core spectral primitives that directly serve SPU's harmonic analysis function. SPU demands F features at Micro-Macro horizons (H3 through H16), covering note-level through section-level tonal analysis.

- **IMU** consumes F features at Macro horizons (H16-H22) through MEM and TMH mechanisms. The integrative memory unit tracks how tonal content evolves over longer timescales -- tonal memory is fundamentally a Macro-band phenomenon.

- **PCU** consumes F features for predictive coding: chroma prediction (what chord comes next?), salience prediction (will the texture clarify or thicken?), and inharmonicity prediction (instrument change detection).

- **NDU** has only indirect F consumption through pitch_class_entropy, which serves as a novelty indicator -- sudden entropy changes signal tonal surprises.

---

## 7. Estimated Tuple Count

### Breakdown by Feature Subgroup

| Feature Subgroup | Dim | Horizons | Morphs | Laws | Est. Tuples |
|-----------------|:---:|:--------:|:------:|:----:|:-----------:|
| Chroma [49:61] | 12D | 5 (H6,H9,H12,H16,H18) | 6 (M0,M1,M2,M8,M14,M18) | 2-3 | ~600-800 |
| Pitch height [61] | 1D | 3 (H3,H6,H9) | 5 (M0,M1,M8,M6,M11) | 2 | ~30-50 |
| Pitch class entropy [62] | 1D | 3 (H12,H16,H18) | 3 (M0,M1,M18) | 2 | ~20-30 |
| Pitch salience [63] | 1D | 3 (H6,H9,H12) | 3 (M0,M1,M2) | 2 | ~20-30 |
| Inharmonicity index [64] | 1D | 3 (H9,H12,H16) | 3 (M0,M1,M8) | 2 | ~20-30 |

### Total

- **Theoretical maximum** (16 features x 5 avg horizons x 6 avg morphs x 3 laws): ~1,440
- **Estimated actual demand**: ~800-1,200 tuples
- **Chroma dominates**: The 12D chroma vector accounts for ~70% of F group tuples due to its high dimensionality and broad horizon/morph coverage.

### Note on Chroma Dimensionality

Each chroma bin (C through B) is independently indexed in R3 and therefore independently addressable in H3. A model demanding the mean chroma profile at H12 under L0 requires 12 separate tuples: `(49, H12, M1, L0)` through `(60, H12, M1, L0)`. This multiplicative effect of 12D chroma is the primary reason F group has the highest tuple count among v2 groups.

---

## 8. Cross-References

- **Expansion Index**: [00-INDEX.md](00-INDEX.md)
- **Impact Analysis**: [R3v2-H3-Impact.md](R3v2-H3-Impact.md)
- **R3 Feature Catalog**: [../../R3/Registry/FeatureCatalog.md](../../R3/Registry/FeatureCatalog.md)
- **H3 Architecture**: [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md)
- **Horizon Catalog**: [../Registry/HorizonCatalog.md](../Registry/HorizonCatalog.md)
- **Morph Catalog**: [../Registry/MorphCatalog.md](../Registry/MorphCatalog.md)
- **SPU Demand Profile**: [../Demand/SPU-H3-DEMAND.md](../Demand/SPU-H3-DEMAND.md)
- **IMU Demand Profile**: [../Demand/IMU-H3-DEMAND.md](../Demand/IMU-H3-DEMAND.md)
- **PCU Demand Profile**: [../Demand/PCU-H3-DEMAND.md](../Demand/PCU-H3-DEMAND.md)
- **Related Groups**:
  - [H-HarmonyTonality-Temporal.md](H-HarmonyTonality-Temporal.md) (closely related: harmony is built on pitch/chroma)
  - [G-RhythmGroove-Temporal.md](G-RhythmGroove-Temporal.md) (melodic rhythm interaction)

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial F group temporal demand analysis (Phase 4G) |
