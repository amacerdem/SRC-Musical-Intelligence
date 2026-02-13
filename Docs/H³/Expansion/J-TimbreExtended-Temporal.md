# Group J: Timbre Extended [94:114] -- Temporal Demand Analysis

> Version 2.0.0 | Updated 2026-02-13

## 1. Group Summary

Group J introduces 20 features that extend the timbral representation beyond the core C group (Timbre) features in R3 v1. The group comprises two sub-families: 13 Mel-frequency cepstral coefficients (MFCCs) providing a compact spectral envelope representation, and 7 spectral contrast bands quantifying the harmonic-to-noise balance across octave-spaced frequency regions.

| Feature | Index | Dim | Quality | Description |
|---------|:-----:|:---:|:-------:|-------------|
| mfcc_1 | 94 | 1D | S | 1st MFCC -- overall spectral energy (DC-like) |
| mfcc_2 | 95 | 1D | S | 2nd MFCC -- spectral tilt (bright vs dark) |
| mfcc_3 | 96 | 1D | S | 3rd MFCC -- spectral curvature |
| mfcc_4 | 97 | 1D | S | 4th MFCC -- broad formant structure |
| mfcc_5 | 98 | 1D | S | 5th MFCC -- finer spectral shape |
| mfcc_6 | 99 | 1D | S | 6th MFCC |
| mfcc_7 | 100 | 1D | S | 7th MFCC |
| mfcc_8 | 101 | 1D | S | 8th MFCC |
| mfcc_9 | 102 | 1D | S | 9th MFCC -- fine timbral texture |
| mfcc_10 | 103 | 1D | S | 10th MFCC |
| mfcc_11 | 104 | 1D | S | 11th MFCC |
| mfcc_12 | 105 | 1D | S | 12th MFCC |
| mfcc_13 | 106 | 1D | S | 13th MFCC -- finest timbral detail |
| spectral_contrast_1 | 107 | 1D | S | Contrast band 1 (lowest octave) |
| spectral_contrast_2 | 108 | 1D | S | Contrast band 2 |
| spectral_contrast_3 | 109 | 1D | S | Contrast band 3 |
| spectral_contrast_4 | 110 | 1D | S | Contrast band 4 |
| spectral_contrast_5 | 111 | 1D | S | Contrast band 5 |
| spectral_contrast_6 | 112 | 1D | S | Contrast band 6 |
| spectral_contrast_7 | 113 | 1D | S | Contrast band 7 (highest octave) |

**Dependencies**: None beyond base spectrogram. Pipeline stage 1 (independent of F, G, H).

**Quality distribution**: All 20 features are S (Standard). MFCC computation via pre-computed DCT matrix (128x13) is an exact mathematical transform. Spectral contrast via per-octave sort with top/bottom 20% quantile thresholds is a deterministic computation.

**Implementation**: MFCC coefficients are derived from the 128-mel spectrogram via a pre-computed DCT matrix, producing 13 coefficients per frame. Spectral contrast divides the spectrum into 7 octave-spaced bands and computes the difference between the top 20% and bottom 20% energy quantiles within each band.

---

## 2. Temporal Relevance

Timbral change is one of the strongest perceptual cues for musical structure. Instrument entries and exits, vocal transitions (verse singing to spoken word), orchestration shifts (strings to brass), and production effects (dry to reverb) all manifest as MFCC trajectory changes. Section boundaries in popular music (intro, verse, chorus, bridge) are often more reliably detected by timbral features than by harmonic or rhythmic features.

MFCC evolution over time captures:
- **Instrument changes**: A new instrument entering shifts the entire MFCC vector.
- **Vocal register shifts**: Chest voice to head voice alters lower MFCCs significantly.
- **Production dynamics**: Mix automation (EQ sweeps, filter cutoffs) creates smooth MFCC trajectories.
- **Arrangement density**: Adding or removing instruments changes spectral contrast across bands.

Spectral contrast dynamics track the harmonic-to-noise balance over time. Rising contrast indicates increasing tonal clarity (e.g., a solo instrument emerging from a texture). Falling contrast indicates increasing noise content (e.g., cymbals, distortion buildup).

Lower-order MFCCs (1-4) are the most temporally informative because they capture broad spectral envelope shape -- the perceptually dominant timbral characteristics. Higher-order MFCCs (9-13) capture progressively finer spectral detail that is less perceptually salient and changes less systematically over musical timescales.

---

## 3. Horizon Mapping

| Feature | Indices | Horizons | Band | Rationale |
|---------|---------|----------|------|-----------|
| mfcc_1-4 [94:98] | 4D | H6, H9, H12, H16 | Micro-Macro | Broad spectral envelope at beat/phrase/section |
| mfcc_5-8 [98:102] | 4D | H9, H12, H16 | Meso-Macro | Finer timbral detail at phrase/section scale |
| mfcc_9-13 [102:107] | 5D | H12, H16 | Meso-Macro | Fine timbral texture at phrase/section only |
| spectral_contrast_1-3 [107:110] | 3D | H6, H9, H12 | Micro-Meso | Low/mid band contrast at beat/phrase scale |
| spectral_contrast_4-7 [110:114] | 4D | H9, H12, H16 | Meso-Macro | High band contrast at phrase/section scale |

### Horizon Heatmap

```
Horizon  H6   H9   H12  H16
Band     Mic  Meso Meso Mac
         ====================
mfcc_1-4 (4D)        [X]  [X]  [X]  [X]
mfcc_5-8 (4D)         .   [X]  [X]  [X]
mfcc_9-13 (5D)        .    .   [X]  [X]
contrast_1-3 (3D)    [X]  [X]  [X]   .
contrast_4-7 (4D)     .   [X]  [X]  [X]
         ====================
Dim x Horizon:
  H6:   4+3 = 7D
  H9:   4+4+3+4 = 15D
  H12:  4+4+5+3+4 = 20D (all features)
  H16:  4+4+5+4 = 17D
```

**Key observations**:
- H12 (525ms, phrase scale) is the universal horizon -- all 20 features are demanded there.
- MFCC demand follows an information-content gradient: lower MFCCs span more horizons, higher MFCCs are restricted to Meso-Macro only.
- No Macro demand beyond H16; timbral features at section scale (H18+) would require consumption by TMH or MEM mechanisms, which is not typical for J group.
- No Ultra demand; timbral evolution at movement/piece scale is captured indirectly via IMU memory consolidation of lower-horizon morphs.
- Spectral contrast has a split horizon pattern: low bands (1-3) reach into Micro for beat-level contrast tracking; high bands (4-7) are Meso-Macro only.

---

## 4. Morph Profiles

### MFCC [94:107]

| Morph | ID | Demand | Rationale |
|-------|----|:------:|-----------|
| Value | M0 | High | Instantaneous timbral snapshot |
| Mean | M1 | High | Average timbre over horizon (timbral center) |
| Std | M2 | High | Timbral variability -- homogeneous vs diverse texture |
| Velocity | M8 | High | Rate of timbral change -- fast transitions signal boundaries |
| Periodicity | M14 | Medium | Cyclic timbral patterns (e.g., verse-chorus alternation) |
| Trend | M18 | Medium | Long-term timbral drift (arrangement buildup/decay) |

### Spectral Contrast [107:114]

| Morph | ID | Demand | Rationale |
|-------|----|:------:|-----------|
| Value | M0 | High | Instantaneous harmonic/noise balance |
| Mean | M1 | High | Average contrast (overall tonal clarity) |
| Std | M2 | Medium | Contrast variability |
| Max | M4 | Medium | Peak contrast moment (clearest tonal event) |
| Velocity | M8 | Medium | Rate of contrast change |

### Morph Demand Gradient

Lower-order MFCCs (1-4) demand more morphs (M0, M1, M2, M4, M8, M14, M18) because their broad spectral shape is perceptually dominant and varies meaningfully at all demanded timescales. Higher-order MFCCs (9-13) demand fewer morphs (M0, M1, M2) because their fine spectral detail is primarily useful as a timbral fingerprint (level morphs) rather than for dynamic analysis.

---

## 5. Law Preferences

| Law | Code | Primary Users | J Group Application |
|-----|------|---------------|---------------------|
| L0 (Memory) | Past | IMU | Timbral memory -- encoding the current instrument/voice from accumulated past spectral context |
| L2 (Integration) | Both | SPU, ASU | Bidirectional timbral stability -- identifying instrument identity from surrounding context |

**Distribution**: L2 (Integration) is the primary law for J group features. Timbral identification benefits strongly from bidirectional context -- knowing what comes after a timbral transition helps classify the transition itself. L0 (Memory) is used by IMU for encoding timbral memory traces. L1 (Prediction) has low demand for J features because timbral prediction is not a primary function of any unit; timbre serves more as a contextual descriptor than a prediction target.

---

## 6. Consuming Units

| Unit | Models | J Features | Mechanism | Priority |
|------|:------:|-----------|-----------|:--------:|
| SPU | Multiple models | mfcc_1-4, spectral_contrast | PPC, TPC | Medium |
| ASU | OASD, CGCD, ASIE | mfcc (salience cues) | ASA | Low-Medium |
| IMU | MEAMN, HCMC, MMP | mfcc (timbral memory encoding) | MEM | Low-Medium |
| PCU | IGFE, MAA, PSH | mfcc, spectral_contrast | PPC | Low |

### Demand Concentration

SPU is the primary consumer of J group features. As the Spectral Processing Unit, SPU's core function is spectral analysis and integration, and the extended timbral features in J group complement the existing C group timbre features. SPU's PPC models (BCH, PSCL, PCCR) use lower MFCCs at H6 for rapid timbral classification. SPU's TPC models (STAI, TSCP, MIAA) use MFCCs and spectral contrast at H12-H16 for timbral pattern completion.

ASU (Auditory Scene Analysis Unit) uses MFCCs as salience cues for stream segregation. In a multi-source auditory scene, timbral differences between streams are a primary segregation criterion. ASU models demand mfcc_1-4 at H6-H9 via the ASA mechanism, using timbral trajectories to maintain separate auditory streams.

IMU (Integrative Memory Unit) uses MFCCs for timbral memory encoding -- associating emotional states with specific timbral contexts. This demand is at Macro horizons (H16) via MEM mechanism.

---

## 7. Estimated Tuple Count

| Source | Features | Horizons | Morphs | Laws | Est. Tuples |
|--------|:--------:|:--------:|:------:|:----:|:-----------:|
| mfcc_1-4 | 4 | 4 (H6,H9,H12,H16) | 6 (M0,M1,M2,M8,M14,M18) | 2 (L0,L2) | ~192 |
| mfcc_5-8 | 4 | 3 (H9,H12,H16) | 4 (M0,M1,M2,M8) | 2 (L0,L2) | ~96 |
| mfcc_9-13 | 5 | 2 (H12,H16) | 3 (M0,M1,M2) | 2 (L0,L2) | ~60 |
| spectral_contrast_1-3 | 3 | 3 (H6,H9,H12) | 5 (M0,M1,M2,M4,M8) | 2 (L0,L2) | ~90 |
| spectral_contrast_4-7 | 4 | 3 (H9,H12,H16) | 4 (M0,M1,M2,M4) | 2 (L0,L2) | ~96 |
| **Total** | **20** | | | | **~534** |

Deduplication across units is moderate (~10-15%) since SPU, ASU, and IMU demand overlapping mfcc subsets. **Estimated net: ~400-700 tuples**.

Lower-order MFCCs (1-4) contribute disproportionately despite being only 4 of 13 MFCC dimensions, because they span more horizons and demand more morphs. This concentration effect keeps the actual tuple count manageable despite J group's high dimensionality (20D).

---

## 8. Dimensionality Considerations

Group J is the largest new R3 group (20D), but its H3 demand does not scale linearly with dimensionality. Three factors create a natural demand gradient that concentrates tuples on the most informative features:

### 8.1 MFCC Information Ordering

MFCC coefficients are ordered by information content by construction. The DCT transforms the mel-spectrogram into decorrelated components where:
- **mfcc_1-4**: Capture >85% of spectral envelope variance (broad shape, tilt, curvature, formant structure).
- **mfcc_5-8**: Capture ~10% of remaining variance (finer spectral detail).
- **mfcc_9-13**: Capture <5% of remaining variance (very fine spectral texture, often noise-like in polyphonic music).

This energy compaction means that temporal morphs of higher MFCCs are increasingly dominated by noise rather than musically meaningful variation.

### 8.2 Horizon Narrowing

As MFCC order increases, the demanded horizon set narrows:
- mfcc_1-4: H6, H9, H12, H16 (4 horizons)
- mfcc_5-8: H9, H12, H16 (3 horizons)
- mfcc_9-13: H12, H16 (2 horizons)

This reflects the principle that fine timbral detail varies meaningfully only at slower timescales, where averaging suppresses frame-to-frame noise.

### 8.3 Morph Reduction

Higher MFCCs demand fewer morphs (only Level morphs M0, M1, M2) while lower MFCCs demand Dynamics and Rhythm morphs as well. Dynamics morphs (velocity, trend, periodicity) applied to high-order MFCCs produce mostly noise.

**Net effect**: Despite 20D, the effective tuple count (~400-700) is comparable to Group H (12D, ~500-800), because the demand gradient strongly concentrates computation on the 4-7 most informative dimensions.

---

## 9. Cross-References

- **H3 Architecture**: [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md)
- **Expansion Index**: [00-INDEX.md](00-INDEX.md)
- **R3 Feature Catalog**: [../../R3/Registry/FeatureCatalog.md](../../R3/Registry/FeatureCatalog.md)
- **Horizon Catalog**: [../Registry/HorizonCatalog.md](../Registry/HorizonCatalog.md)
- **Morph Catalog**: [../Registry/MorphCatalog.md](../Registry/MorphCatalog.md)
- **Law Catalog**: [../Registry/LawCatalog.md](../Registry/LawCatalog.md)
- **SPU Demand Profile**: [../Demand/SPU-H3-DEMAND.md](../Demand/SPU-H3-DEMAND.md)
- **ASU Demand Profile**: [../Demand/ASU-H3-DEMAND.md](../Demand/ASU-H3-DEMAND.md)
- **IMU Demand Profile**: [../Demand/IMU-H3-DEMAND.md](../Demand/IMU-H3-DEMAND.md)
- **PCU Demand Profile**: [../Demand/PCU-H3-DEMAND.md](../Demand/PCU-H3-DEMAND.md)
- **Demand Address Space**: [../Registry/DemandAddressSpace.md](../Registry/DemandAddressSpace.md)
- **Pipeline / Performance**: [../Pipeline/Performance.md](../Pipeline/Performance.md)
- **H Group (complementary -- tonal structure)**: [H-HarmonyTonality-Temporal.md](H-HarmonyTonality-Temporal.md)
- **K Group (related -- psychoacoustic)**: [K-ModulationPsychoacoustic-Temporal.md](K-ModulationPsychoacoustic-Temporal.md)

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial Group J temporal demand analysis (Phase 4G) |
