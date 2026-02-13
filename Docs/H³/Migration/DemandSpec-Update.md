# H3 DemandSpec Update Guide -- V2 Tuples

> Version 2.0.0 | Updated 2026-02-13

## 1. Overview

Each C3 model declares its H3 temporal demand as a set of 4-tuples in its DemandSpec. The v1-to-v2 migration means adding new tuples that reference R3 feature indices in [49:128] (groups F through K). This document provides the procedure, conventions, and validation checklist for these updates.

The migration is purely additive: existing v1 tuples are never modified or removed. New v2 tuples are appended to the model's `h3_demand` set following the same 4-tuple format, respecting the model's mechanism assignments and perceptual role.

---

## 2. DemandSpec 4-Tuple Format

```
(r3_idx, horizon, morph, law)
```

| Field | Type | Range (v1) | Range (v2) | Description |
|-------|:----:|:----------:|:----------:|-------------|
| r3_idx | int | 0--48 | 0--127 | R3 feature index. v1 features at [0:49], v2 additions at [49:128]. |
| horizon | int | 0--31 | 0--31 | Horizon index. Unchanged between v1 and v2. |
| morph | int | 0--23 | 0--23 | Morph index. Unchanged between v1 and v2. |
| law | int | 0--2 | 0--2 | Law index. Unchanged between v1 and v2. |

The 4-tuple uniquely identifies a single H3 output time series: "the M{morph} statistic of R3 feature {r3_idx} computed over a window of H{horizon} frames using L{law} temporal perspective."

**Address space**:
- v1: 49 x 32 x 24 x 3 = 112,896 possible tuples
- v2: 128 x 32 x 24 x 3 = 294,912 possible tuples
- Actual occupancy remains sparse (~2.9% at ~8,610 tuples)

---

## 3. How to Add V2 Tuples

Step-by-step procedure for adding v2 demand to a C3 model:

### Step 1: Identify Relevant V2 R3 Features

Consult the unit's R3 mapping file (e.g., `R3/Mappings/PCU-R3-MAP.md`) for the "New Feature Consumption (v2)" section. This lists which v2 features (indices [49:128]) are relevant to the unit's perceptual domain.

For quick reference, v2 feature groups:

| Group | Indices | Features | Dim |
|-------|:-------:|----------|:---:|
| F: Pitch & Chroma | [49:65] | chroma_vector (12D), pitch_height, pitch_salience, pitch_confidence, pitch_class | 16 |
| G: Rhythm & Groove | [65:75] | beat_strength, tempo_estimate, onset_density, groove_regularity, syncopation, pulse_clarity, beat_phase, subdivision_ratio, tempo_stability, rhythmic_complexity | 10 |
| H: Harmony & Tonality | [75:87] | tonnetz (6D), key_clarity, mode_indicator, chord_complexity, harmonic_change, tonal_tension, tonal_stability | 12 |
| I: Information & Surprise | [87:94] | information_rate, spectral_flatness_info, predictive_entropy, surprise_index, redundancy, compression_ratio, novelty_score | 7 |
| J: Timbre Extended | [94:114] | mfcc_1 through mfcc_13, spectral_contrast (4D), formant_ratio, timbral_roughness, timbral_warmth | 20 |
| K: Modulation & Psycho | [114:128] | am_depth, am_rate, fm_depth, fm_rate, modulation_spectrum (4D), fluctuation_strength, roughness_model, sharpness_zwicker, loudness_specific (2D), masking_level | 14 |

### Step 2: Determine Appropriate Horizons

Use the model's mechanism assignment to determine which horizons are available. Each mechanism operates at specific horizons:

| Mechanism | Horizons | Frames |
|-----------|----------|--------|
| PPC | H0, H3, H6 | 1, 5, 26 |
| ASA | H3, H6, H9 | 5, 26, 69 |
| BEP | H6, H9, H11 | 26, 69, 104 |
| TPC | H6, H12, H16 | 26, 138, 518 |
| SYN | H12, H16, H18 | 138, 518, 1724 |
| AED | H6, H16 | 26, 518 |
| CPD | H9, H16, H18 | 69, 518, 1724 |
| C0P | H18, H19, H20 | 1724, 2586, 3448 |
| TMH | H16, H18, H20, H22 | 518, 1724, 3448, 5172 |
| MEM | H18, H20, H22, H25 | 1724, 3448, 5172, 12931 |

New v2 tuples should use the same horizons as the model's existing v1 tuples. Adding a v2 feature at a horizon not covered by the model's mechanism is not prohibited but should be justified.

### Step 3: Select Morphs

Use the group-specific morph recommendations (Section 5) as a starting point, then refine based on the model's perceptual function:

- **State-tracking models** (e.g., tonality detectors): Emphasize M0(value), M1(mean), M3(median).
- **Change-detecting models** (e.g., novelty detectors): Emphasize M8(velocity), M11(acceleration), M18(trend).
- **Stability-assessing models** (e.g., rhythm trackers): Emphasize M2(std), M19(stability), M15(smoothness).
- **Pattern-finding models** (e.g., structure analyzers): Emphasize M14(periodicity), M17(shape_period), M22(peaks).
- **Information models** (e.g., predictive coders): Emphasize M20(entropy), M6(skewness), M7(kurtosis).

### Step 4: Select Law

Match to the model's existing law preference:

| Law | Temporal Perspective | Typical Models |
|-----|---------------------|----------------|
| L0 | Memory (causal, past-only) | IMU, STU rhythm models |
| L1 | Prediction (anticipatory, future-only) | PCU, NDU prediction models |
| L2 | Integration (bidirectional) | SPU, ASU, ARU integration models |

Most models use a single primary law. v2 tuples should use the same law unless the new feature's temporal character demands a different perspective (rare).

### Step 5: Append Tuples

Add new 4-tuples to the model's `h3_demand` set in the model documentation and (during Phase 5) in the model code.

---

## 4. Worked Example: Adding I:predictive_entropy to PCU-alpha1-HTP

### Context

PCU-alpha1-HTP (Harmonic Temporal Prediction) uses TPC mechanism (H6, H12, H16) with L1 (Prediction) law. Its primary function is predicting harmonic-temporal patterns.

### Current V1 Demand (abbreviated)

```python
h3_demand = {
    (0, 6, 0, 1),    # roughness, H6, value, prediction
    (0, 12, 1, 1),   # roughness, H12, mean, prediction
    (11, 6, 8, 0),   # onset_strength, H6, velocity, memory
    (14, 12, 0, 1),  # brightness_kuttruff, H12, value, prediction
    (14, 16, 1, 1),  # brightness_kuttruff, H16, mean, prediction
    ...               # ~45 total v1 tuples
}
```

### V2 Feature Selection

From the PCU R3 mapping, predictive_entropy [92] is identified as a priority I-group feature for HTP. Rationale: HTP's prediction function directly benefits from a measure of prediction uncertainty at the model's operating horizons.

### New V2 Tuples

```python
# V2 additions for HTP: predictive_entropy [92]
(92, 6, 0, 1),    # predictive_entropy, H6, value, prediction
(92, 12, 1, 1),   # predictive_entropy, H12, mean, prediction
(92, 16, 1, 1),   # predictive_entropy, H16, mean, prediction
(92, 12, 8, 1),   # predictive_entropy, H12, velocity, prediction
(92, 16, 18, 1),  # predictive_entropy, H16, trend, prediction
```

### Rationale

| Tuple | Justification |
|-------|--------------|
| (92, 6, 0, 1) | Instantaneous predictive entropy at beat-subdivision scale. Captures moment-to-moment prediction uncertainty. |
| (92, 12, 1, 1) | Average predictive entropy over phrase-level window. Baseline prediction difficulty for the musical context. |
| (92, 16, 1, 1) | Average predictive entropy over measure-level window. Broader prediction difficulty context. |
| (92, 12, 8, 1) | Rate of change of predictive entropy at phrase level. Detects transitions between predictable and unpredictable passages. |
| (92, 16, 18, 1) | Trend of predictive entropy at measure level. Captures gradual increase/decrease in prediction difficulty over longer spans. |

Morphs selected: M0(value) for instantaneous state, M1(mean) for average level, M8(velocity) for change rate, M18(trend) for trajectory. This matches HTP's prediction-oriented function.

### Updated Demand

```python
h3_demand = {
    # ... existing v1 tuples unchanged ...
    # V2 additions
    (92, 6, 0, 1),
    (92, 12, 1, 1),
    (92, 16, 1, 1),
    (92, 12, 8, 1),
    (92, 16, 18, 1),
}
# Total: ~45 (v1) + 5 (v2) = ~50 tuples
```

---

## 5. Per-Group Conventions

Default tuple patterns recommended for each new R3 feature group. These serve as starting points; individual models should adjust based on their specific perceptual function.

| Group | Indices | Default Horizons | Default Morphs | Default Law | Notes |
|-------|:-------:|:----------------:|:--------------:|:-----------:|-------|
| F: Pitch & Chroma | [49:65] | Match mechanism | M0, M1, M8, M14 | Model-specific | Chroma (12D): M0, M1 minimum per chroma bin. Pitch height: add M8(velocity) for melodic contour. |
| G: Rhythm & Groove | [65:75] | Match BEP/TMH | M0, M1, M2, M14 | L0 (causal) | Tempo features: add M18(trend) for tempo drift. beat_strength: add M22(peaks). |
| H: Harmony & Tonality | [75:87] | Match mechanism | M0, M1, M8, M18 | Model-specific | Tonnetz (6D): M0, M1 minimum per dimension. key_clarity: add M19(stability). |
| I: Information & Surprise | [87:94] | Match mechanism | M0, M1, M2, M18 | L1 (predictive) | predictive_entropy is the most cross-unit demanded feature. information_rate: add M8(velocity). |
| J: Timbre Extended | [94:114] | Match mechanism | M0, M1, M2, M8 | L0 or L2 | MFCC 1-4 are highest priority (indices [94:98]). Higher MFCCs are lower priority. |
| K: Modulation & Psycho | [114:128] | H12+ only | M0, M1, M18 | L0 | Warm-up limits restrict Micro-band use. am/fm features need >= Meso horizons for meaningful periodicity. |

### Typical Tuple Counts Per Group Per Model

| Group | Alpha Tier | Beta Tier | Gamma Tier |
|-------|:----------:|:---------:|:----------:|
| F: Pitch | 15--30 | 8--15 | 4--8 |
| G: Rhythm | 10--20 | 5--12 | 3--6 |
| H: Harmony | 12--25 | 6--15 | 3--8 |
| I: Information | 8--15 | 4--10 | 2--5 |
| J: Timbre | 10--25 | 5--15 | 3--8 |
| K: Modulation | 5--12 | 3--8 | 2--4 |

---

## 6. Validation Checklist

After adding v2 tuples to a model, verify the following:

- [ ] All new `r3_idx` values are in [49:127] (valid v2 range).
- [ ] No new `r3_idx` duplicates an existing v1 tuple with the same (horizon, morph, law).
- [ ] Horizons match the model's mechanism assignment (see mechanism-horizon table in Section 3).
- [ ] Morphs are supported at the chosen horizon tier (see [Standards/MorphQualityTiers.md](../Standards/MorphQualityTiers.md)).
- [ ] Law matches the model's primary temporal perspective.
- [ ] No duplicate tuples in the combined v1+v2 demand set.
- [ ] Total tuple count is reasonable for the model tier:
  - Alpha: 50--150 tuples
  - Beta: 30--100 tuples
  - Gamma: 20--60 tuples
- [ ] Model documentation version is incremented.
- [ ] New tuples are listed in the model's "V2 H3 Demand" section.

---

## 7. Priority Order for Adoption

Recommended adoption order based on cross-unit demand analysis and implementation readiness:

| Priority | Group | Indices | Rationale |
|:--------:|-------|:-------:|-----------|
| 1 | I: Information & Surprise | [87:94] | Highest cross-unit demand. PCU (10 models), RPU (10 models), and IMU (15 models) all require prediction-related features. predictive_entropy [92] is the single most demanded v2 feature. |
| 2 | G: Rhythm & Groove | [65:75] | Critical for STU (14 models, largest unit) and MPU (10 models). beat_strength and tempo_estimate are foundational for motor and timing computations. |
| 3 | H: Harmony & Tonality | [75:87] | High demand from NDU (9 models), PCU (10 models), and IMU (15 models). Tonnetz features provide 6D harmonic space representation not available in v1. |
| 4 | F: Pitch & Chroma | [49:65] | Medium demand from SPU (9 models), IMU (15 models), and PCU (10 models). Chroma vector (12D) is the largest single v2 feature block. |
| 5 | J: Timbre Extended | [94:114] | Medium demand, primarily SPU (9 models) and ASU (9 models). MFCC features extend timbral representation beyond v1 spectral descriptors. |
| 6 | K: Modulation & Psycho | [114:128] | Lowest cross-unit demand. Primarily STU (14 models) and ARU (10 models). Modulation features require longer horizons (H12+) limiting Micro-band use. |

### Per-Unit Adoption Roadmap

| Unit | P1 (I) | P2 (G) | P3 (H) | P4 (F) | P5 (J) | P6 (K) |
|------|:------:|:------:|:------:|:------:|:------:|:------:|
| SPU | -- | -- | -- | High | High | -- |
| STU | Low | **High** | Low | Low | -- | Medium |
| IMU | **High** | Low | **High** | Medium | -- | -- |
| ASU | -- | -- | -- | -- | **High** | -- |
| NDU | Medium | -- | **High** | Low | -- | -- |
| MPU | -- | **High** | -- | -- | -- | -- |
| PCU | **High** | Low | Medium | Medium | -- | -- |
| ARU | Medium | -- | Low | -- | Low | Medium |
| RPU | **High** | Medium | Medium | Low | Low | Low |

Bold entries indicate the primary adoption targets for each group.

---

## 8. Cross-References

| Related Document | Location |
|-----------------|----------|
| V1-to-V2 migration guide | [V1-to-V2.md](V1-to-V2.md) |
| R3 v2 H3 impact analysis | [../Expansion/R3v2-H3-Impact.md](../Expansion/R3v2-H3-Impact.md) |
| F: Pitch & Chroma temporal | [../Expansion/F-PitchChroma-Temporal.md](../Expansion/F-PitchChroma-Temporal.md) |
| G: Rhythm & Groove temporal | [../Expansion/G-RhythmGroove-Temporal.md](../Expansion/G-RhythmGroove-Temporal.md) |
| H: Harmony & Tonality temporal | [../Expansion/H-HarmonyTonality-Temporal.md](../Expansion/H-HarmonyTonality-Temporal.md) |
| I: Information & Surprise temporal | [../Expansion/I-InformationSurprise-Temporal.md](../Expansion/I-InformationSurprise-Temporal.md) |
| J: Timbre Extended temporal | [../Expansion/J-TimbreExtended-Temporal.md](../Expansion/J-TimbreExtended-Temporal.md) |
| K: Modulation & Psycho temporal | [../Expansion/K-ModulationPsychoacoustic-Temporal.md](../Expansion/K-ModulationPsychoacoustic-Temporal.md) |
| Morph quality tiers | [../Standards/MorphQualityTiers.md](../Standards/MorphQualityTiers.md) |
| Acceptance criteria | [../Validation/AcceptanceCriteria.md](../Validation/AcceptanceCriteria.md) |
| Per-unit demand documentation | [../Demand/](../Demand/) |
| H3DemandSpec contract (C3) | [../../C3/Contracts/H3DemandSpec.md](../../C3/Contracts/H3DemandSpec.md) |
| R3 feature catalog | [../../R3/Registry/FeatureCatalog.md](../../R3/Registry/FeatureCatalog.md) |
| Migration index | [00-INDEX.md](00-INDEX.md) |
| H3 master index | [../00-INDEX.md](../00-INDEX.md) |

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial DemandSpec update guide (Phase 4H) |
