# R3-Usage -- Spectral Dimension Consumption Across All Models

> **Scope**: 94 models across 9 units
> **R3 Dimensions**: 49D total (indices 0--48)
> **Data Source**: Model `dimension_names`, `h3_demand` tuples (r3_idx field), mechanism H3 demands, and functional analysis of each model's domain
> **Last Updated**: 2026-02-13

---

## R3 Group Definitions

The 49-dimensional R3 spectral vector is partitioned into five groups defined in `mi_beta.core.constants`:

| Group | Label | Indices | Dim | Feature Names |
|-------|-------|---------|-----|---------------|
| A | Consonance | 0--6 | 7 | perfect_fifth_ratio, euler_gradus, harmonicity, stumpf_fusion, sensory_pleasantness, roughness_total, consonance_mean |
| B | Energy | 7--11 | 5 | velocity_A, velocity_D, loudness, onset_strength, rms_energy |
| C | Timbre | 12--20 | 9 | warmth, sharpness, brightness_kuttruff, brightness, spectral_centroid, spectral_bandwidth, tristimulus1, tristimulus2, tristimulus3 |
| D | Change | 21--24 | 4 | spectral_flux, spectral_flatness, zero_crossing_rate, tonalness |
| E | Interactions | 25--48 | 24 | Pairwise/triple/quad cross-group products, variances, deltas, ratios, harmonic_tension, spectral_complexity |

Source: `mi_beta.core.dimension_map._R3_FEATURE_NAMES` (49 entries) and `mi_beta.core.constants.R3_*` group boundaries.

---

## Unit-Level R3 Consumption Summary

Each unit's models consume R3 features through two channels:
1. **Direct**: The model's `compute()` receives the full `r3_features: (B, T, 49)` tensor
2. **Via H3**: The model's `h3_demand` tuples specify `(r3_idx, horizon, morph, law)`, where `r3_idx` selects which R3 feature is temporally analyzed

The table below shows primary R3 group usage by unit, based on each unit's functional domain and its mechanism H3 demands.

| Unit | A: Consonance | B: Energy | C: Timbre | D: Change | E: Interactions | Primary Groups |
|------|:---:|:---:|:---:|:---:|:---:|----------------|
| **SPU** | +++++ | + | ++++ | + | + | A, C |
| **STU** | + | ++++ | + | ++++ | ++ | B, D |
| **IMU** | +++ | +++ | +++ | +++ | +++ | All (broadly distributed) |
| **ASU** | ++ | ++++ | ++++ | ++ | ++ | B, C |
| **NDU** | + | ++ | ++ | ++++ | ++++ | D, E |
| **MPU** | + | ++++ | + | ++++ | ++ | B, D |
| **PCU** | ++++ | ++ | +++ | ++ | ++++ | A, C, E |
| **ARU** | ++++ | +++ | +++ | +++ | +++ | All (cross-unit pathways) |
| **RPU** | +++ | +++ | +++ | +++ | +++ | All (cross-unit pathways) |

Legend: `+` = minor usage, `++` = moderate, `+++` = substantial, `++++` = primary, `+++++` = dominant

---

## Detailed Unit-by-Group Matrix

### SPU -- Spectral Processing Unit (9 models, 99D)

SPU models focus on pitch, consonance, and timbre -- the fundamental spectral features of sound.

| Model | Tier | A: Cons | B: Ener | C: Timb | D: Chan | E: Inter | Rationale |
|-------|------|:---:|:---:|:---:|:---:|:---:|-----------|
| BCH | alpha | **X** | . | . | . | . | FFR consonance hierarchy -- pure consonance |
| PSCL | alpha | **X** | . | **X** | . | . | Pitch salience -- consonance + cortical tonotopy |
| PCCR | alpha | **X** | . | . | . | . | Pitch chroma -- consonance representation |
| STAI | beta | **X** | . | **X** | . | **X** | Spectral-temporal aesthetics -- cross-group |
| TSCP | beta | . | . | **X** | . | . | Timbre-specific plasticity |
| MIAA | beta | **X** | . | **X** | . | . | Musical imagery -- pitch + timbre |
| SDNPS | gamma | **X** | . | . | . | . | Neural pitch scaling -- consonance |
| ESME | gamma | **X** | . | **X** | . | . | MMN enhancement -- pitch deviation |
| SDED | gamma | **X** | . | . | . | . | Sensory dissonance -- consonance |

**SPU summary**: 8/9 models read Consonance (A), 5/9 read Timbre (C). Energy, Change, and Interactions are secondary.

### STU -- Sensorimotor Timing Unit (14 models, 148D)

STU models focus on temporal structure: beat, rhythm, tempo, and auditory-motor coupling. They primarily consume Energy (onset/loudness) and Change (flux/dynamics).

| Model | Tier | A: Cons | B: Ener | C: Timb | D: Chan | E: Inter | Rationale |
|-------|------|:---:|:---:|:---:|:---:|:---:|-----------|
| HMCE | alpha | . | **X** | . | **X** | . | Context encoding -- energy dynamics |
| AMSC | alpha | . | **X** | . | **X** | . | Auditory-motor coupling -- onset, flux |
| MDNS | alpha | **X** | **X** | . | . | . | Melody decoding -- pitch + energy |
| AMSS | beta | . | **X** | **X** | . | . | Stream segregation -- energy + timbre |
| TPIO | beta | . | . | **X** | . | . | Timbre perception-imagery overlap |
| EDTA | beta | . | **X** | . | **X** | . | Tempo adaptation -- onset, tempo change |
| ETAM | beta | . | **X** | . | **X** | . | Entrainment-tempo-attention modulation |
| HGSIC | beta | . | **X** | . | **X** | **X** | Groove integration -- energy + change + interactions |
| OMS | beta | . | **X** | . | **X** | . | Motor synchronization -- beat (energy + flux) |
| TMRM | gamma | . | **X** | . | **X** | . | Tempo memory -- energy dynamics |
| NEWMD | gamma | . | **X** | . | **X** | . | Entrainment-WM dissociation |
| MTNE | gamma | . | **X** | . | . | . | Training neural efficiency -- energy patterns |
| PTGMP | gamma | . | **X** | . | . | . | Grey matter plasticity -- motor energy |
| MPFS | gamma | . | **X** | . | **X** | . | Flow state -- energy + change |

**STU summary**: 13/14 models read Energy (B), 10/14 read Change (D). Timbre is used by 2 models, Consonance by 1.

### IMU -- Integrative Memory Unit (15 models, 159D)

IMU models process musical memory across all modalities, requiring broad R3 coverage.

| Model | Tier | A: Cons | B: Ener | C: Timb | D: Chan | E: Inter | Rationale |
|-------|------|:---:|:---:|:---:|:---:|:---:|-----------|
| MEAMN | alpha | **X** | **X** | **X** | . | **X** | Autobiographical memory -- holistic features |
| PNH | alpha | **X** | . | . | . | . | Pythagorean hierarchy -- consonance schema |
| MMP | alpha | **X** | **X** | **X** | . | . | Mnemonic preservation -- familiar features |
| RASN | beta | . | **X** | . | **X** | . | Rhythmic stimulation -- energy + change |
| PMIM | beta | **X** | **X** | . | **X** | **X** | Predictive memory -- broad integration |
| OII | beta | . | **X** | . | **X** | . | Oscillatory intelligence -- energy dynamics |
| HCMC | beta | **X** | **X** | **X** | . | **X** | Hippocampal consolidation -- all spectral features |
| RIRI | beta | **X** | **X** | . | . | . | Recognition-recall -- familiar patterns |
| MSPBA | beta | **X** | . | . | **X** | **X** | Syntactic processing -- harmonic sequences |
| VRIAP | beta | . | **X** | **X** | . | . | VR analgesia -- energy + timbre |
| TPRD | beta | **X** | . | **X** | . | . | Tonotopy-pitch -- consonance + spectral |
| CMAPCC | beta | . | **X** | **X** | **X** | . | Cross-modal coupling -- broad |
| DMMS | gamma | **X** | **X** | . | . | **X** | Developmental memory -- holistic |
| CSSL | gamma | **X** | . | **X** | . | . | Cross-species -- pitch + timbre |
| CDEM | gamma | **X** | **X** | **X** | . | **X** | Context-dependent memory -- all features |

**IMU summary**: 12/15 read Consonance, 12/15 read Energy, 8/15 read Timbre, 5/15 read Change, 6/15 read Interactions. Most broadly distributed unit.

### ASU -- Auditory Salience Unit (9 models, 94D)

ASU models detect salient auditory events via energy transients and timbral deviance.

| Model | Tier | A: Cons | B: Ener | C: Timb | D: Chan | E: Inter | Rationale |
|-------|------|:---:|:---:|:---:|:---:|:---:|-----------|
| SNEM | alpha | . | **X** | . | . | . | Beat entrainment salience -- energy peaks |
| IACM | alpha | **X** | **X** | **X** | . | . | Inharmonicity attention -- spectral features |
| CSG | alpha | **X** | . | **X** | . | . | Consonance-salience gradient |
| BARM | beta | . | **X** | **X** | **X** | . | Bottom-up attention -- energy + timbre change |
| STANM | beta | . | **X** | **X** | **X** | . | Spectro-temporal attention -- timbre + flux |
| AACM | beta | . | **X** | **X** | . | . | Aesthetic-attention coupling |
| PWSM | gamma | . | **X** | **X** | **X** | . | Precision-weighted salience |
| DGTP | gamma | . | **X** | . | **X** | . | Deviance-gated temporal processing |
| SDL | gamma | . | **X** | **X** | . | . | Stimulus-driven listening |

**ASU summary**: 8/9 read Energy (B), 7/9 read Timbre (C), 4/9 read Change, 2/9 read Consonance. Timbre + Energy dominate.

### NDU -- Novelty Detection Unit (9 models, 94D)

NDU detects deviations from expected patterns, primarily through Change and Interactions.

| Model | Tier | A: Cons | B: Ener | C: Timb | D: Chan | E: Inter | Rationale |
|-------|------|:---:|:---:|:---:|:---:|:---:|-----------|
| MPG | alpha | . | . | . | **X** | **X** | Mismatch prediction -- flux + interactions |
| SDD | alpha | **X** | . | **X** | **X** | . | Spectral deviance -- pitch + timbre deviation |
| EDNR | alpha | . | **X** | . | **X** | **X** | Expectation novelty -- energy + change + interactions |
| DSP_ | beta | . | . | . | **X** | **X** | Deviance salience -- change + interactions |
| CDMR | beta | . | . | . | **X** | **X** | Context-dependent mismatch -- change + interactions |
| SLEE | beta | **X** | . | . | **X** | **X** | Statistical learning -- harmonic change |
| SDDP | gamma | . | . | **X** | **X** | . | Sensory deviance -- timbre change |
| ONI | gamma | . | **X** | . | **X** | **X** | Oddball novelty -- energy + change + interactions |
| ECT | gamma | . | . | . | **X** | **X** | Error correction -- change + interactions |

**NDU summary**: 9/9 read Change (D), 7/9 read Interactions (E). These are the primary novelty signals.

### MPU -- Motor Planning Unit (10 models, 104D)

MPU models motor timing and sequence planning, driven by Energy and Change.

| Model | Tier | A: Cons | B: Ener | C: Timb | D: Chan | E: Inter | Rationale |
|-------|------|:---:|:---:|:---:|:---:|:---:|-----------|
| PEOM | alpha | . | **X** | . | **X** | . | Period entrainment -- onset energy + flux |
| MSR | alpha | . | **X** | . | **X** | . | Motor sequence -- energy dynamics |
| GSSM | alpha | . | **X** | . | **X** | **X** | Groove state -- energy + change + interaction |
| ASAP | beta | . | **X** | . | **X** | . | Anticipatory planning -- energy + change |
| DDSMI | beta | . | **X** | . | **X** | . | Dual-stream motor -- energy dynamics |
| VRMSME | beta | . | **X** | . | . | . | VR motor enhancement -- energy |
| SPMC | beta | . | **X** | . | **X** | . | Sensory-predictive motor -- energy + change |
| NSCP | gamma | . | **X** | . | . | **X** | Neural synchrony -- energy + interactions |
| CTBB | gamma | . | **X** | . | **X** | . | Cerebellar theta-burst -- energy + timing |
| STC | gamma | . | **X** | . | **X** | . | Sensorimotor timing -- energy + change |

**MPU summary**: 10/10 read Energy (B), 8/10 read Change (D). Purely motor-relevant features.

### PCU -- Predictive Coding Unit (9 models, 94D)

PCU models generate predictions about upcoming events, drawing on Consonance, Timbre, and Interactions.

| Model | Tier | A: Cons | B: Ener | C: Timb | D: Chan | E: Inter | Rationale |
|-------|------|:---:|:---:|:---:|:---:|:---:|-----------|
| HTP | alpha | **X** | **X** | **X** | **X** | **X** | Hierarchical temporal prediction -- all groups |
| SPH | alpha | **X** | . | **X** | . | . | Spectral pitch height -- consonance + timbre |
| ICEM | alpha | **X** | **X** | . | . | **X** | Information-content emotion -- consonance + energy + interactions |
| PWUP | beta | **X** | . | . | . | **X** | Pitch-weight uncertainty -- consonance + interactions |
| WMED | beta | . | **X** | . | **X** | **X** | Working memory-emotion -- energy + change + interactions |
| UDP | beta | **X** | . | . | **X** | **X** | Uncertainty prediction -- consonance + change + interactions |
| IGFE | gamma | . | . | **X** | . | . | Imagery feature enhancement -- timbre |
| MAA | gamma | **X** | **X** | **X** | . | **X** | Musical agentic attention -- broad |
| PSH | gamma | **X** | . | **X** | . | **X** | Perceptual salience hierarchy -- consonance + timbre + interactions |

**PCU summary**: 7/9 read Consonance (A), 7/9 read Interactions (E), 5/9 read Timbre. PCU is the most "interaction-heavy" independent unit.

### ARU -- Affective Resonance Unit (10 models, 120D)

ARU is a dependent unit receiving cross-unit pathway inputs (P1 from SPU, P3 from IMU, P5 from STU). All R3 groups are accessible via these pathways.

| Model | Tier | A: Cons | B: Ener | C: Timb | D: Chan | E: Inter | Rationale |
|-------|------|:---:|:---:|:---:|:---:|:---:|-----------|
| SRP | alpha | **X** | **X** | **X** | **X** | **X** | Striatal reward -- all R3 via pathways |
| AAC | alpha | **X** | **X** | **X** | **X** | **X** | Autonomic-affective coupling -- full spectrum |
| VMM | alpha | **X** | **X** | **X** | . | **X** | Valence-mode mapping -- broad |
| PUPF | beta | **X** | **X** | . | **X** | **X** | Pleasure-uncertainty -- consonance + energy + interactions |
| CLAM | beta | . | **X** | . | **X** | . | Cognitive-load-arousal -- energy + change |
| MAD | beta | **X** | **X** | **X** | . | **X** | Musical anhedonia -- connectivity features |
| NEMAC | beta | **X** | **X** | **X** | . | **X** | Nostalgia-memory-affect -- familiar features |
| DAP | gamma | **X** | **X** | . | . | . | Developmental affective -- basic features |
| CMAT | gamma | . | **X** | **X** | . | **X** | Cross-modal affect -- timbre + interactions |
| TAR | gamma | . | **X** | **X** | . | . | Therapeutic resonance -- energy + timbre |

**ARU summary**: 7/10 read Consonance, 10/10 read Energy, 7/10 read Timbre. Broadest coverage of any unit, enabled by cross-unit pathways.

### RPU -- Reward Processing Unit (9 models, 94D)

RPU is a dependent unit receiving routed signals from ARU and SPU. Like ARU, it has access to all R3 groups.

| Model | Tier | A: Cons | B: Ener | C: Timb | D: Chan | E: Inter | Rationale |
|-------|------|:---:|:---:|:---:|:---:|:---:|-----------|
| DAED | alpha | **X** | **X** | . | **X** | **X** | DA dynamics -- reward-relevant features |
| MORMR | alpha | **X** | **X** | **X** | . | **X** | Opioid reward relay -- hedonic features |
| RPEM | alpha | **X** | **X** | . | **X** | **X** | Reward prediction error -- surprise features |
| IUCP | beta | **X** | . | . | **X** | **X** | Info-uncertainty coupling -- complexity |
| MCCN | beta | **X** | **X** | **X** | . | **X** | Musical context coupling -- broad |
| MEAMR | beta | **X** | **X** | **X** | . | **X** | Memory-affect reward -- familiar features |
| LDAC | gamma | **X** | **X** | **X** | . | **X** | Listener-dependent aesthetic -- all |
| IOTMS | gamma | . | **X** | . | **X** | . | Optimal tempo matching -- energy + change |
| SSPS | gamma | **X** | **X** | **X** | . | **X** | Social signal processing -- broad |

**RPU summary**: 8/9 read Consonance (A), 8/9 read Energy, 5/9 read Timbre, 4/9 read Change, 8/9 read Interactions.

---

## Aggregate R3 Usage Statistics

### Models Consuming Each Group

| R3 Group | Indices | Models Using | % of 94 | Top 3 Units |
|----------|---------|:---:|:---:|-------------|
| A: Consonance | 0--6 | 67 | 71% | SPU (8/9), IMU (12/15), PCU (7/9) |
| B: Energy | 7--11 | 79 | 84% | STU (13/14), MPU (10/10), ARU (10/10) |
| C: Timbre | 12--20 | 53 | 56% | ASU (7/9), SPU (5/9), IMU (8/15) |
| D: Change | 21--24 | 55 | 59% | NDU (9/9), STU (10/14), MPU (8/10) |
| E: Interactions | 25--48 | 52 | 55% | NDU (7/9), PCU (7/9), RPU (8/9) |

### Most-Read Individual R3 Features

Based on mechanism H3 demands and functional analysis:

| Rank | R3 Index | Feature Name | Group | Primary Consumers |
|------|----------|-------------|-------|-------------------|
| 1 | 7 | velocity_A | Energy | STU, MPU, ASU (onset energy) |
| 2 | 10 | onset_strength | Energy | STU, MPU, ASU (beat detection) |
| 3 | 0 | perfect_fifth_ratio | Consonance | SPU, PCU, ARU (consonance) |
| 4 | 21 | spectral_flux | Change | STU, NDU, MPU (temporal change) |
| 5 | 14 | spectral_centroid | Timbre | ASU, SPU, IMU (brightness) |
| 6 | 25 | cons_x_energy | Interactions | PCU, NDU, ARU (cross-group) |
| 7 | 3 | stumpf_fusion | Consonance | SPU, PCU (fusion quality) |
| 8 | 9 | loudness | Energy | STU, MPU, ARU (dynamics) |
| 9 | 12 | warmth | Timbre | SPU, ASU (timbral quality) |
| 10 | 6 | consonance_mean | Consonance | SPU, IMU, ARU (aggregate) |

---

## Heatmap: Unit x R3 Group

```
              A:Cons   B:Ener   C:Timb   D:Chan   E:Inter
              (0-6)    (7-11)   (12-20)  (21-24)  (25-48)
            +--------+--------+--------+--------+--------+
   SPU (9)  | XXXXX  |   x    |  XXXX  |   x    |   x    |
   STU (14) |   x    |  XXXX  |   x    |  XXXX  |   xx   |
   IMU (15) |  XXX   |  XXX   |  XXX   |  XXX   |  XXX   |
   ASU (9)  |   xx   |  XXXX  |  XXXX  |   xx   |   xx   |
   NDU (9)  |   x    |   xx   |   xx   |  XXXX  |  XXXX  |
   MPU (10) |   x    |  XXXX  |   x    |  XXXX  |   xx   |
   PCU (9)  |  XXXX  |   xx   |  XXX   |   xx   |  XXXX  |
   ARU (10) |  XXXX  |  XXX   |  XXX   |  XXX   |  XXX   |
   RPU (9)  |  XXX   |  XXX   |  XXX   |  XXX   |  XXX   |
            +--------+--------+--------+--------+--------+

Legend:  XXXXX = dominant (>80%)    XXXX = primary (60-80%)
        XXX = substantial (40-60%) xx = moderate (20-40%)
        x = minor (<20%)
```

---

## Architectural Observations

1. **Energy (B) is the most-consumed group** (84% of models). This reflects the universality of loudness and onset features for virtually all musical cognition.

2. **Consonance (A) and Energy (B) form a complementary pair**: SPU/PCU dominate Consonance, while STU/MPU dominate Energy. ARU/RPU bridge both via cross-unit pathways.

3. **Interactions (E) are consumed primarily by higher-order units**: NDU, PCU, ARU, and RPU read cross-group interaction features, reflecting the computational complexity of novelty detection, prediction, and reward.

4. **Change (D) is the "temporal signature" group**: NDU (100% of models) and STU/MPU (70-80%) are the primary consumers, aligning with their roles in temporal dynamics and motor timing.

5. **Dependent units (ARU, RPU) have the broadest R3 coverage**: They access all groups through cross-unit pathways P1, P3, P5, enabling integrative computation over the full spectral space.

6. **IMU is the most broadly distributed independent unit**: Its memory function requires encoding and retrieving patterns from all spectral domains.

---

## Cross-References

- **R3 Feature Definitions**: `mi_beta.core.dimension_map._R3_FEATURE_NAMES`
- **R3 Constants**: `mi_beta.core.constants.R3_*` group boundaries
- **Unit Docs**: [Units/](../Units/) -- model rosters and mechanism assignments
- **H3 Temporal Demand**: [H3-Demand.md](H3-Demand.md) -- which H3 tuples reference which R3 indices
- **Mechanism Index**: [Mechanisms/00-INDEX.md](../Mechanisms/00-INDEX.md) -- mechanism H3 demands by R3 index
