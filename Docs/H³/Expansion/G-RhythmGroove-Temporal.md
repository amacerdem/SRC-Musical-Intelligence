# Group G: Rhythm & Groove -- Temporal Demand Analysis

> Version 2.0.0 | Updated 2026-02-13

## 1. Group Summary

| Property | Value |
|----------|-------|
| **Group** | G: Rhythm & Groove |
| **Dimensions** | 10D |
| **Indices** | [65:75] |
| **Temporal Priority** | HIGH |
| **Est. New Tuples** | ~400-600 |
| **Primary Consumers** | STU, MPU |

### Feature Inventory

| Feature | Index | Dim | Quality Tier | Description |
|---------|:-----:|:---:|:------------:|-------------|
| tempo_estimate | 65 | 1D | A | Instantaneous tempo estimate (BPM-derived, normalized) |
| beat_strength | 66 | 1D | A | Strength of detected beat pulse relative to onset envelope |
| pulse_clarity | 67 | 1D | A | Distinctness of dominant pulse period in autocorrelation |
| syncopation_index | 68 | 1D | A | Degree of accent displacement from metric grid positions |
| metricality_index | 69 | 1D | A | Strength of hierarchical metric structure (beat > sub-beat > sub-sub-beat) |
| isochrony_nPVI | 70 | 1D | S | Normalized Pairwise Variability Index of inter-onset intervals |
| groove_index | 71 | 1D | A | Composite micro-timing deviation measure (swing, push, lay-back) |
| event_density | 72 | 1D | S | Note onset rate per unit time (events/second, normalized) |
| tempo_stability | 73 | 1D | S | Coefficient of variation of inter-beat intervals over window |
| rhythmic_regularity | 74 | 1D | S | Autocorrelation peak-to-sidelobe ratio of IOI sequence |

**Quality tiers**: A = Approximate (6 features), S = Standard (4 features: isochrony_nPVI, event_density, tempo_stability, rhythmic_regularity).

**Dependencies**: B[11] onset_strength (all G features depend on onset detection). Pipeline stage 2 -- G features are computed after B group onset extraction.

---

## 2. Temporal Relevance

Group G is unique among the R3 v2 groups because its features are **already temporal in nature**. Tempo, beat strength, pulse clarity, and groove are all computed from onset patterns distributed over time. A single audio frame has no "tempo" -- tempo emerges from the relationship between successive onsets spanning hundreds of milliseconds.

This creates a distinctive relationship with H3: the temporal morphology layer computes temporal statistics of features that are themselves temporal. This **temporal-of-temporal hierarchy** is not redundant -- it captures a qualitatively different level of description:

| Level | Question | Timescale | Example |
|-------|----------|-----------|---------|
| R3 (G group) | What is the rhythm right now? | Instantaneous (per-frame, derived from ~1s window) | Tempo = 120 BPM |
| H3 on G | How does the rhythm change over time? | Multi-second to multi-minute | Tempo accelerates from 120 to 140 BPM over 16 bars |

This hierarchy is musically essential. "How does the groove develop through the piece?" is a macro-temporal question about a meso-temporal feature that no single R3 frame can answer. H3 provides the framework to track rhythmic evolution at phrase, section, and movement timescales.

---

## 3. Horizon Mapping

| Feature | Index | Horizons | Band | Rationale |
|---------|:-----:|----------|------|-----------|
| tempo_estimate [65] | 1D | H9, H11, H12, H16 | Meso-Macro | Tempo tracking at beat/phrase/measure scale; tempo changes are meaningful over 4-16 beat spans |
| beat_strength [66] | 1D | H6, H9, H11 | Micro-Meso | Beat strength varies at beat-rate timescales; accent patterns cycle at measure level |
| pulse_clarity [67] | 1D | H9, H11, H12 | Meso | Clarity at beat/phrase level; breakdowns and builds affect clarity over 2-8 beat spans |
| syncopation_index [68] | 1D | H9, H11, H16 | Meso-Macro | Syncopation patterns at phrase/measure scale; syncopation density shifts at section boundaries |
| metricality_index [69] | 1D | H11, H12, H16 | Meso-Macro | Metric hierarchy at measure/section scale; meter changes operate at phrase boundaries |
| isochrony_nPVI [70] | 1D | H12, H16, H18 | Meso-Macro | Rhythmic regularity at phrase/section scale; swing feel evolves over longer passages |
| groove_index [71] | 1D | H12, H16, H18 | Meso-Macro | Groove development over sections; micro-timing character shifts at structural boundaries |
| event_density [72] | 1D | H9, H11, H12 | Meso | Event rate at beat/phrase level; textural density changes with arrangement |
| tempo_stability [73] | 1D | H16, H18, H20 | Macro | Tempo consistency at section/movement scale; rubato vs. metronomic character |
| rhythmic_regularity [74] | 1D | H12, H16, H18 | Meso-Macro | IOI regularity at phrase/section scale; rhythmic complexity evolution |

### Horizon Coverage Heatmap

```
Horizon  H0   H3   H6   H9  H11  H12  H16  H18  H20  H22  H25
Band     |-- Micro --|   |--Meso--|   |---- Macro ----|  Ultra
         ============================================
tempo     .    .    .   [X]  [X]  [X]  [X]   .    .    .    .
beat_str  .    .   [X]  [X]  [X]   .    .    .    .    .    .
pulse_cl  .    .    .   [X]  [X]  [X]   .    .    .    .    .
syncop    .    .    .   [X]  [X]   .   [X]   .    .    .    .
metric    .    .    .    .   [X]  [X]  [X]   .    .    .    .
iso_nPVI  .    .    .    .    .   [X]  [X]  [X]   .    .    .
groove    .    .    .    .    .   [X]  [X]  [X]   .    .    .
evt_dens  .    .    .   [X]  [X]  [X]   .    .    .    .    .
tempo_st  .    .    .    .    .    .   [X]  [X]  [X]   .    .
rhy_reg   .    .    .    .    .   [X]  [X]  [X]   .    .    .
         ============================================
Count     0    0    1    5    6    7    7    4    1    0    0
```

### Key Observations

- **H12 and H16** are the most demanded horizons (7/10 features each) -- the phrase and measure timescales where rhythmic structure is most meaningfully characterized.
- **H11** is close behind (6/10) -- the upper Meso range where beat-level patterns aggregate.
- **No Micro-early demand** (H0, H3): Rhythm features do not have meaningful sub-beat temporal dynamics (they are already derived from multi-onset windows).
- **H6** is demanded only by beat_strength -- the fastest rhythmic feature, tracking accent patterns at beat-subdivision timescales.
- **H20** is demanded only by tempo_stability -- the slowest rhythmic feature, tracking tempo consistency over movement-length passages.
- **No Ultra demand**: Rhythmic features do not require 36s+ observation windows.

---

## 4. Morph Profiles

### Tempo Features ([65], [73])

| Morph | ID | Usage |
|-------|----|-------|
| Value | M0 | Instantaneous tempo / tempo stability values |
| Mean | M1 | Average tempo over horizon (prevailing tempo) |
| Std | M2 | Tempo variability within horizon (rubato magnitude) |
| Velocity | M8 | Tempo rate of change (accelerando = positive, ritardando = negative) |
| Trend | M18 | Long-term tempo drift (global acceleration/deceleration across sections) |

### Beat Features ([66], [67], [68])

| Morph | ID | Usage |
|-------|----|-------|
| Value | M0 | Instantaneous beat strength / pulse clarity / syncopation |
| Mean | M1 | Average metric prominence over horizon |
| Std | M2 | Beat variability (irregular accents, metric instability) |
| Periodicity | M14 | Cyclic beat patterns (4-bar hypermetric cycles, verse/chorus accent alternation) |

### Groove and Regularity Features ([70], [71], [74])

| Morph | ID | Usage |
|-------|----|-------|
| Value | M0 | Instantaneous groove / regularity measure |
| Mean | M1 | Average groove character over horizon |
| Trend | M18 | Groove evolution trajectory (increasing/decreasing groove intensity) |
| Entropy | M20 | Rhythmic complexity measure (high entropy = unpredictable rhythm) |

### Metricality and Density Features ([69], [72])

| Morph | ID | Usage |
|-------|----|-------|
| Value | M0 | Instantaneous metricality / event density |
| Mean | M1 | Average metric strength / density over horizon |
| Std | M2 | Metric / density variability |

---

## 5. Law Preferences

| Law | Name | G Group Usage | Primary Models |
|-----|------|--------------|----------------|
| L0 | Memory | **Primary law for G group**. Beat tracking is inherently causal -- past onsets drive current pulse estimate. Tempo memory accumulates evidence from preceding beats. Groove character is built from accumulated micro-timing patterns. | STU (BEP, TMH), MPU (BEP) |
| L1 | Prediction | Secondary law. Tempo prediction for anticipatory timing -- the motor system predicts the next beat to prepare movement. Used by timing models that generate predictive pulse. | HMCE, TMRM (STU), MPU prediction models |
| L2 | Integration | Rarely used for rhythm. Rhythmic perception is inherently forward-causal (past onsets produce current pulse). Bidirectional integration has limited perceptual grounding for rhythmic features. | (sparse -- analysis models only) |

### Law Distribution

- **L0 dominates**: ~70% of G group tuples. Rhythm perception is fundamentally causal -- you cannot hear a beat before it occurs.
- **L1 is secondary**: ~25% of G group tuples. Motor planning requires beat prediction for synchronization.
- **L2 is rare**: ~5% of G group tuples. Used only where offline analysis (non-real-time) needs bidirectional context.

---

## 6. Consuming Units

| Unit | Models | G Features | Mechanism | Horizons | Priority |
|------|:------:|-----------|-----------|----------|:--------:|
| STU | HMCE, AMSC, MDNS, AMSS, TPIO, EDTA, ETAM, HGSIC, OMS, TMRM, NEWMD, MTNE, PTGMP, MPFS | All 10 features | BEP (H6,H9,H11), TMH (H16,H18,H20,H22) | H6-H22 | Very High |
| MPU | 8-10 models | tempo, beat_strength, syncopation, groove, event_density, metricality | BEP (H6,H9,H11) | H6-H11 | Very High |
| IMU | RASN, RIRI, CSSL | metricality, isochrony, groove, rhythmic_regularity | MEM (H18,H20,H22), TMH (H16,H18) | H16-H22 | Medium |

### Unit-Level Notes

- **STU** is the single largest consumer of G features across all units. Every STU model (14/14) demands at least some G group features. G features are mission-critical for STU -- they provide the explicit rhythmic descriptors that STU's BEP and TMH mechanisms operate on. The v2 expansion of STU is dominated by G group adoption. The temporal-of-temporal nature of H3-on-G is especially powerful for STU: BEP tracks beat-level rhythm (Meso), while TMH tracks how that rhythm evolves over sections (Macro).

- **MPU** is the second-largest consumer. Motor planning depends on rhythm: tempo for movement rate, beat_strength for synchronization targets, syncopation for timing anticipation, groove for movement quality. MPU demands G features at BEP horizons (H6-H11) -- the motor-relevant timescales.

- **IMU** consumes G features at longer timescales (H16-H22) through MEM and TMH mechanisms. The integrative memory unit tracks rhythmic character across sections and movements -- how does the groove of the bridge compare to the verse? This is a fundamentally integrative, retrospective question.

---

## 7. Estimated Tuple Count

### Breakdown by Consumer

| Consumer | Features | Horizons | Morphs | Laws | Est. Tuples |
|----------|:--------:|:--------:|:------:|:----:|:-----------:|
| STU (BEP) | 10 | 3 (H6,H9,H11) | 4-5 | 2 (L0,L1) | ~250-350 |
| STU (TMH) | 6 | 4 (H16,H18,H20,H22) | 3-4 | 1-2 (L0,L1) | ~70-100 |
| MPU | 6 | 3 (H6,H9,H11) | 3-4 | 2 (L0,L1) | ~100-150 |
| IMU | 4 | 3-4 (H16-H22) | 2-3 | 1 (L0) | ~30-50 |

### Total

- **Theoretical maximum** (10 features x 4 avg horizons x 5 avg morphs x 3 laws): ~600
- **Estimated actual demand**: ~400-600 tuples
- **STU dominates**: ~320-450 tuples (~75% of G group demand), reflecting STU's role as the rhythm-processing center.
- **MPU secondary**: ~100-150 tuples (~22%), focused on motor-relevant rhythm features at BEP horizons.
- **IMU tertiary**: ~30-50 tuples (~5%), focused on long-timescale rhythmic memory.

---

## 8. The Temporal-of-Temporal Hierarchy

Group G occupies a unique position in the R3-H3 architecture because it creates a **second-order temporal representation**. This section explains why this is architecturally significant and musically meaningful, rather than redundant.

### The Two Levels

```
Level 1: R3 G-group feature extraction
  Input:  Raw audio onset patterns (from B[11] onset_strength)
  Output: Instantaneous rhythmic descriptors (tempo, groove, etc.)
  Scale:  ~0.5-2s analysis window (beat-rate)

Level 2: H3 morphs on G-group features
  Input:  Time-series of G-group features from Level 1
  Output: Temporal morphs of rhythmic descriptors (tempo trend, groove evolution)
  Scale:  ~1-25s observation horizon (phrase-to-section)
```

### Why This is Not Redundant

Level 1 answers: "What is the rhythm?" (e.g., tempo = 120 BPM, groove = high, syncopation = moderate).

Level 2 answers: "How does the rhythm change?" (e.g., tempo is accelerating, groove is intensifying through the bridge, syncopation increases approaching the chorus).

These are categorically different musical questions. A piece can have constant tempo (Level 1 unchanged) but systematically increasing groove (Level 2 trend is positive). A performer can maintain strict tempo (Level 1 stable) while progressively loosening rhythmic regularity (Level 2 std increasing). These second-order dynamics are perceptually salient and musically critical for understanding large-scale temporal structure.

### Musical Examples

| Musical Phenomenon | Level 1 (R3) | Level 2 (H3 on G) |
|-------------------|-------------|-------------------|
| Accelerando | tempo_estimate increasing | M8 velocity > 0 at H16 |
| Groove development | groove_index rising | M18 trend positive at H16-H18 |
| Metric disruption | metricality_index dropping | M2 std increasing at H12 |
| Rhythmic build | event_density increasing | M8 velocity > 0 at H12 |
| Swing intensification | isochrony_nPVI increasing | M18 trend positive at H16 |

### Architectural Implications

The temporal-of-temporal hierarchy means that H3 morph computations on G features should use **longer minimum horizons** than morphs on non-temporal features. Computing M1 (mean) of tempo_estimate at H3 (17ms) is meaningless because tempo_estimate itself already integrates over ~1s. The practical minimum horizon for G features is H9 (~170ms), and most meaningful morphs begin at H11-H12 (~250-500ms). This is reflected in the horizon mapping above, where no G feature demands horizons below H6.

---

## 9. Cross-References

- **Expansion Index**: [00-INDEX.md](00-INDEX.md)
- **Impact Analysis**: [R3v2-H3-Impact.md](R3v2-H3-Impact.md)
- **R3 Feature Catalog**: [../../R3/Registry/FeatureCatalog.md](../../R3/Registry/FeatureCatalog.md)
- **H3 Architecture**: [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md)
- **Horizon Catalog**: [../Registry/HorizonCatalog.md](../Registry/HorizonCatalog.md)
- **Morph Catalog**: [../Registry/MorphCatalog.md](../Registry/MorphCatalog.md)
- **STU Demand Profile**: [../Demand/STU-H3-DEMAND.md](../Demand/STU-H3-DEMAND.md)
- **MPU Demand Profile**: [../Demand/MPU-H3-DEMAND.md](../Demand/MPU-H3-DEMAND.md)
- **IMU Demand Profile**: [../Demand/IMU-H3-DEMAND.md](../Demand/IMU-H3-DEMAND.md)
- **BEP Mechanism**: [../Contracts/](../Contracts/)
- **TMH Mechanism**: [../Contracts/](../Contracts/)
- **Related Groups**:
  - [F-PitchChroma-Temporal.md](F-PitchChroma-Temporal.md) (melodic rhythm interaction)
  - [K-ModulationPsychoacoustic-Temporal.md](K-ModulationPsychoacoustic-Temporal.md) (beat-rate modulation overlap)

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial G group temporal demand analysis (Phase 4G) |
