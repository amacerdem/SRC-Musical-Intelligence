# Group K: Modulation & Psychoacoustic [114:128] -- Temporal Demand Analysis

> Version 2.0.0 | Updated 2026-02-13

## 1. Group Summary

Group K introduces 14 features spanning two distinct sub-domains: modulation spectrum analysis (8 features quantifying temporal modulation rates) and psychoacoustic descriptors (6 features capturing perceptual quality). This dual nature creates a split temporal demand profile -- modulation features encode rates of temporal variation (meta-temporal), while psychoacoustic features encode perceptual qualities whose evolution over time is musically informative.

### Modulation Sub-Group [114:121]

| Feature | Index | Dim | Quality | Description |
|---------|:-----:|:---:|:-------:|-------------|
| modulation_0_5Hz | 114 | 1D | A | Modulation energy at 0.5 Hz (slow amplitude fluctuation) |
| modulation_1Hz | 115 | 1D | A | Modulation energy at 1 Hz (sub-beat fluctuation) |
| modulation_2Hz | 116 | 1D | A | Modulation energy at 2 Hz (beat-rate region) |
| modulation_4Hz | 117 | 1D | A | Modulation energy at 4 Hz (syllabic/tactus rate) |
| modulation_8Hz | 118 | 1D | A | Modulation energy at 8 Hz (trill/vibrato region) |
| modulation_16Hz | 119 | 1D | A | Modulation energy at 16 Hz (flutter/roughness boundary) |
| modulation_centroid | 120 | 1D | S | Spectral centroid of the modulation spectrum |
| modulation_bandwidth | 121 | 1D | S | Bandwidth of the modulation spectrum |

### Psychoacoustic Sub-Group [122:128]

| Feature | Index | Dim | Quality | Description |
|---------|:-----:|:---:|:-------:|-------------|
| sharpness_zwicker | 122 | 1D | R | Zwicker sharpness (perceptual brightness); Reference quality |
| fluctuation_strength | 123 | 1D | S | Fluctuation strength (~4 Hz AM perception) |
| loudness_a_weighted | 124 | 1D | S | A-weighted loudness level |
| alpha_ratio | 125 | 1D | S | Ratio of energy below/above 1 kHz |
| hammarberg_index | 126 | 1D | S | Ratio of peak energy 0-2 kHz to 2-5 kHz |
| spectral_slope_0_500 | 127 | 1D | S | Spectral slope in the 0-500 Hz region |

**Dependencies**: None beyond base spectrogram. Pipeline stage 1.

**Quality distribution**: 6 Approximate (modulation rate bands), 7 Standard (centroid, bandwidth, fluctuation, loudness, alpha, hammarberg, slope), 1 Reference (sharpness_zwicker). sharpness_zwicker is the only R-tier (Reference) quality feature in the entire 128D R3 space -- it uses Zwicker's original psychoacoustic model with bark-scale specific loudness weighting.

**Implementation**: Modulation features are computed via sliding-window FFT over the amplitude envelope (344-frame window, hop 86 frames, FFT size 512). This imposes a 344-frame (~2s) warm-up period before stable values are produced. See Section 8 for the critical interaction between this warm-up and H3 horizons.

---

## 2. Temporal Relevance

Group K features have a distinctive split temporal character:

### Modulation Features [114:121]

Modulation features already encode temporal modulation rates -- they measure *how fast* the signal amplitude varies at specific frequency bands. H3 temporal analysis of modulation features therefore captures *how these rates evolve over time*: "the dominant modulation rate shifts from 2 Hz (beat rate) to 4 Hz (syllabic rate) across this section." This is a meta-temporal representation -- the temporal morphology of temporal modulation.

Key temporal questions for modulation features:
- Is the dominant modulation rate shifting (tempo transition, section change)? (modulation_centroid trend at Macro)
- Is the rhythmic texture broadening or narrowing? (modulation_bandwidth trend at Macro)
- Are beat-rate modulations (2-4 Hz) becoming more or less prominent? (modulation_2Hz/4Hz trend at Macro)
- Is there periodicity in the modulation pattern itself (e.g., alternating sections with different rhythmic density)? (modulation_centroid periodicity at Macro)

### Psychoacoustic Features [122:128]

Psychoacoustic features encode perceptual qualities (sharpness, loudness, spectral tilt) whose temporal evolution tracks production dynamics, mixing decisions, and listener fatigue factors.

Key temporal questions for psychoacoustic features:
- Is the mix getting brighter or darker over time? (sharpness_zwicker trend at Meso-Macro)
- What is the loudness contour of this section? (loudness_a_weighted at multiple horizons)
- Is spectral balance shifting? (alpha_ratio, hammarberg_index trends at Macro)
- Are fluctuation patterns (4 Hz AM) consistent or changing? (fluctuation_strength std at Meso-Macro)

The psychoacoustic features span all timescales from beat-level (loudness dynamics within a measure) to section-level (production automation curves), making their horizon mapping broader than the modulation features.

---

## 3. Horizon Mapping

| Feature | Indices | Horizons | Band | Rationale |
|---------|---------|----------|------|-----------|
| modulation_0.5Hz-4Hz [114:118] | 4D | H16, H18, H20 | Macro | Slow modulation rates evolve at section/movement scale; sub-Macro analysis is shorter than the modulation period |
| modulation_8Hz-16Hz [118:120] | 2D | H12, H16 | Meso-Macro | Fast modulation rates at phrase/section scale |
| modulation_centroid [120] | 1D | H16, H18, H20 | Macro | Dominant modulation rate shifts at section scale |
| modulation_bandwidth [121] | 1D | H16, H18 | Macro | Modulation diversity at section scale |
| sharpness_zwicker [122] | 1D | H6, H9, H12, H16 | Micro-Macro | Perceptual sharpness at beat/phrase/section |
| fluctuation_strength [123] | 1D | H9, H12, H16 | Meso-Macro | 4 Hz fluctuation at phrase/section |
| loudness_a_weighted [124] | 1D | H6, H9, H12, H16, H18 | Micro-Macro | A-weighted loudness at all structural scales |
| alpha_ratio [125] | 1D | H12, H16 | Meso-Macro | Low/high energy balance at phrase/section |
| hammarberg_index [126] | 1D | H12, H16 | Meso-Macro | Spectral tilt at phrase/section |
| spectral_slope_0_500 [127] | 1D | H12, H16 | Meso-Macro | Low-frequency spectral shape at phrase/section |

### Horizon Heatmap

```
Horizon  H6   H9   H12  H16  H18  H20
Band     Mic  Meso Meso Mac  Mac  Mac
         ================================
mod_0.5-4Hz (4D)      .    .    .   [X]  [X]  [X]
mod_8-16Hz (2D)        .    .   [X]  [X]   .    .
mod_centroid           .    .    .   [X]  [X]  [X]
mod_bandwidth          .    .    .   [X]  [X]   .
sharpness_zwicker     [X]  [X]  [X]  [X]   .    .
fluctuation_str        .   [X]  [X]  [X]   .    .
loudness_a_wt         [X]  [X]  [X]  [X]  [X]   .
alpha_ratio            .    .   [X]  [X]   .    .
hammarberg_idx         .    .   [X]  [X]   .    .
spectral_slope         .    .   [X]  [X]   .    .
         ================================
Count (unique dims):
  H6:   1+1 = 2D
  H9:   1+1+1 = 3D
  H12:  2+1+1+1+1+1+1 = 8D
  H16:  4+2+1+1+1+1+1+1+1+1 = 14D (all features)
  H18:  4+1+1 = 6D
  H20:  4+1 = 5D
```

**Key observations**:
- H16 (1s) is the universal horizon -- all 14 features are demanded there.
- Modulation features are Macro-only (H16+); their 344-frame warm-up precludes meaningful analysis below Meso.
- Psychoacoustic features have broader horizon spread, with sharpness_zwicker and loudness_a_weighted reaching into Micro (H6).
- loudness_a_weighted has the broadest horizon range (H6-H18, 5 horizons) -- loudness dynamics are perceptually relevant at all structural levels.
- No Ultra demand; K features do not serve movement/piece-scale mechanisms.

---

## 4. Morph Profiles

### Modulation Rate Bands [114:120]

| Morph | ID | Demand | Rationale |
|-------|----|:------:|-----------|
| Value | M0 | High | Instantaneous modulation energy at this rate |
| Mean | M1 | High | Average modulation energy (typical rhythmic texture) |
| Trend | M18 | High | Modulation rate drift -- tempo/texture evolution |
| Std | M2 | Medium | Modulation variability -- steady vs changing texture |

### Modulation Centroid/Bandwidth [120:122]

| Morph | ID | Demand | Rationale |
|-------|----|:------:|-----------|
| Value | M0 | High | Current dominant modulation rate / diversity |
| Mean | M1 | High | Average modulation center/diversity |
| Trend | M18 | High | Shift in dominant rate over sections |
| Periodicity | M14 | Medium | Cyclic modulation patterns |

### Psychoacoustic Features [122:128]

| Morph | ID | Demand | Rationale |
|-------|----|:------:|-----------|
| Value | M0 | High | Instantaneous perceptual quality |
| Mean | M1 | High | Average perceptual quality over window |
| Std | M2 | Medium | Perceptual quality variability |
| Velocity | M8 | Medium | Rate of perceptual change (sharpness sweep, loudness ramp) |
| Trend | M18 | Medium | Long-term perceptual drift (mix evolution) |
| Max | M4 | Medium | Peak sharpness/loudness (climax detection) |

---

## 5. Law Preferences

| Law | Code | Primary Users | K Group Application |
|-----|------|---------------|---------------------|
| L0 (Memory) | Past | STU | Accumulated modulation/perceptual history; entrainment memory of rhythmic texture |
| L1 (Prediction) | Future | PCU | Anticipating modulation rate changes; predicting perceptual quality trajectory |
| L2 (Integration) | Both | ARU | Bidirectional perceptual context; aesthetic evaluation of overall perceptual quality |

**Distribution**: L0 (Memory) is the primary law for K modulation features, reflecting their role in STU entrainment models -- the rhythmic texture memory that drives beat expectations. L2 (Integration) is the primary law for K psychoacoustic features, reflecting their use in ARU aesthetic evaluation where bidirectional context improves perceptual quality assessment. L1 is used sparingly, primarily by PCU for predicting loudness and sharpness trajectories.

---

## 6. Consuming Units

| Unit | Models | K Features | Mechanism | Priority |
|------|:------:|-----------|-----------|:--------:|
| STU | ETAM, OMS, TMRM | modulation_1Hz-4Hz, fluctuation_strength | BEP | Medium |
| ARU | TAR, CMAT | fluctuation_strength, sharpness_zwicker | AED | Low |
| PCU | UDP | spectral_slope_0_500 | MEM | Low (gap resolution) |
| MPU | (minor) | modulation_2Hz, modulation_4Hz | BEP | Low |

### Demand Concentration

STU (Structural Temporal Unit) is the primary consumer of K group features. STU's entrainment models (ETAM -- Entrainment and Temporal Adaptation Model, OMS -- Oscillator-based Meter Selection, TMRM -- Temporal Model of Rhythmic Memory) use modulation rate bands at 1-4 Hz to detect and track beat-rate temporal structure. The modulation spectrum provides a direct readout of the rhythmic texture, and its evolution over Macro horizons (H16-H18) tracks tempo transitions and section-level rhythmic changes via the BEP mechanism.

ARU (Aesthetic Resonance Unit) is a secondary consumer, using fluctuation_strength and sharpness_zwicker at H6 and H16 via the AED (Arousal/Energy Detection) mechanism. These psychoacoustic features contribute to ARU's aesthetic evaluation -- perceived sharpness and fluctuation interact with affective valence and arousal dimensions.

PCU demand for K features is limited to UDP (Uncertainty-Driven Prediction) using spectral_slope_0_500 as a gap resolution feature via MEM mechanism. This is a low-priority demand that was identified during R3 gap analysis.

MPU (Motor Planning Unit) has minor demand for modulation_2Hz and modulation_4Hz, using beat-rate modulation as an input to motor entrainment at the BEP mechanism's characteristic horizons.

---

## 7. Estimated Tuple Count

| Source | Features | Horizons | Morphs | Laws | Est. Tuples |
|--------|:--------:|:--------:|:------:|:----:|:-----------:|
| modulation_0.5-4Hz | 4 | 3 (H16,H18,H20) | 4 (M0,M1,M2,M18) | 1 (L0) | ~48 |
| modulation_8-16Hz | 2 | 2 (H12,H16) | 3 (M0,M1,M18) | 1 (L0) | ~12 |
| modulation_centroid | 1 | 3 (H16,H18,H20) | 4 (M0,M1,M14,M18) | 2 (L0,L2) | ~24 |
| modulation_bandwidth | 1 | 2 (H16,H18) | 3 (M0,M1,M18) | 1 (L0) | ~6 |
| sharpness_zwicker | 1 | 4 (H6,H9,H12,H16) | 5 (M0,M1,M2,M8,M4) | 2 (L0,L2) | ~40 |
| fluctuation_strength | 1 | 3 (H9,H12,H16) | 4 (M0,M1,M2,M8) | 2 (L0,L2) | ~24 |
| loudness_a_weighted | 1 | 5 (H6,H9,H12,H16,H18) | 6 (M0,M1,M2,M4,M8,M18) | 2 (L0,L2) | ~60 |
| alpha_ratio | 1 | 2 (H12,H16) | 3 (M0,M1,M18) | 1 (L2) | ~6 |
| hammarberg_index | 1 | 2 (H12,H16) | 3 (M0,M1,M18) | 1 (L2) | ~6 |
| spectral_slope_0_500 | 1 | 2 (H12,H16) | 3 (M0,M1,M18) | 1 (L2) | ~6 |
| **Total** | **14** | | | | **~232** |

Deduplication across units is minimal (~5%) since K features have few multi-unit overlaps. **Estimated net: ~200-400 tuples**.

K group has the lowest total demand of the new R3 groups. This reflects two factors: (1) the 344-frame warm-up limits Micro-band utility for modulation features, concentrating demand at Macro; and (2) K features serve a narrower set of consuming units (primarily STU and ARU) compared to H, I, or J groups.

Loudness_a_weighted contributes disproportionately (~60 tuples, ~25% of total) due to its exceptionally broad horizon range and morph diversity, reflecting the pervasive perceptual importance of loudness dynamics across all structural levels.

---

## 8. Warm-Up Interaction

K group modulation features require a 344-frame (~2s) warm-up period before producing stable output. This warm-up arises from the sliding-window FFT implementation (344-frame analysis window, hop 86 frames, FFT size 512). During warm-up, the FFT window contains zero-padded or partial data, producing unreliable modulation estimates.

### Impact on H3 Horizons

This warm-up has a direct and significant impact on H3 temporal demand:

**Micro band (H0-H7, up to 250ms)**: The warm-up window (~2s) is 8-344x longer than the Micro horizon windows. H3 morphs at Micro horizons would be computed entirely within the warm-up period, producing meaningless values. **No K modulation features are demanded at Micro horizons.**

**Meso band (H8-H15, 300ms-800ms)**: The warm-up window exceeds all Meso horizon windows. While modulation features begin stabilizing during the Meso window, early-frame artifacts remain. Only modulation_8Hz and modulation_16Hz are demanded at H12 (525ms), and only for audio segments where the warm-up has completed. **K modulation demand at Meso is limited to the faster modulation bands.**

**Macro band (H16-H23, 1s-25s)**: The analysis windows exceed the warm-up duration. H3 morphs at Macro horizons are computed over stable modulation values. **Macro is the primary band for K modulation features.**

**Psychoacoustic features** (sharpness_zwicker, loudness_a_weighted, etc.) do not share this warm-up constraint -- they are computed frame-by-frame from the spectrogram without windowed FFT. Their H3 demand extends into Micro (H6) without restriction.

### Design Implication

The warm-up constraint is a key reason K group has the lowest H3 demand among the new groups. The modulation features (8 of 14 dimensions) are effectively restricted to Macro horizons, eliminating Micro and most Meso demand. This is an inherent limitation of the modulation spectrum approach rather than a design choice -- accurately estimating modulation rates below 16 Hz requires analysis windows of at least 1-2 seconds.

This constraint is documented in [../Pipeline/WarmUp.md](../Pipeline/WarmUp.md).

---

## 9. Cross-References

- **H3 Architecture**: [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md)
- **Expansion Index**: [00-INDEX.md](00-INDEX.md)
- **R3 Feature Catalog**: [../../R3/Registry/FeatureCatalog.md](../../R3/Registry/FeatureCatalog.md)
- **Horizon Catalog**: [../Registry/HorizonCatalog.md](../Registry/HorizonCatalog.md)
- **Morph Catalog**: [../Registry/MorphCatalog.md](../Registry/MorphCatalog.md)
- **Law Catalog**: [../Registry/LawCatalog.md](../Registry/LawCatalog.md)
- **STU Demand Profile**: [../Demand/STU-H3-DEMAND.md](../Demand/STU-H3-DEMAND.md)
- **ARU Demand Profile**: [../Demand/ARU-H3-DEMAND.md](../Demand/ARU-H3-DEMAND.md)
- **PCU Demand Profile**: [../Demand/PCU-H3-DEMAND.md](../Demand/PCU-H3-DEMAND.md)
- **MPU Demand Profile**: [../Demand/MPU-H3-DEMAND.md](../Demand/MPU-H3-DEMAND.md)
- **Demand Address Space**: [../Registry/DemandAddressSpace.md](../Registry/DemandAddressSpace.md)
- **Pipeline / WarmUp**: [../Pipeline/WarmUp.md](../Pipeline/WarmUp.md)
- **Pipeline / Performance**: [../Pipeline/Performance.md](../Pipeline/Performance.md)
- **J Group (related -- extended timbre)**: [J-TimbreExtended-Temporal.md](J-TimbreExtended-Temporal.md)
- **G Group (related -- rhythm)**: [G-RhythmGroove-Temporal.md](G-RhythmGroove-Temporal.md)

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial Group K temporal demand analysis (Phase 4G) |
