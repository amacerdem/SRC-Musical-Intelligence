# R³-H³ Pipeline & Provenance Chain

**Version**: 0.1.0
**Date**: 2026-02-14
**Status**: DRAFT
**Prerequisite**: [01_MANIFESTO.md](01_MANIFESTO.md)

---

## 1. Overview: What C³ Sees

A C³ model never sees raw R³ or raw H³ independently. It sees a **unified data structure** with three access levels:

```
Level 1 — R³ Base (raw micro-reports, 5.8ms resolution)
  "What is the spectral state RIGHT NOW?"

Level 2 — H³ Integrated (temporal context at specific horizons)
  "What has the spectral pattern been DOING over this timescale?"

Level 3 — Provenance Chain (full lineage)
  "WHERE does this number come from and WHAT does it mean?"
```

Every value C³ accesses carries all three levels. This is not optional — it is the foundation of the system's integrity.

---

## 2. The Pipeline

### 2.1 Data Flow

```
Audio (44.1kHz waveform)
  │
  ▼
Cochlea (STFT, hop=256)
  │
  ▼
R³ Extractor (128D per frame, 172.27 Hz)
  │ Stage 1: A,B,C,D,F,J,K (independent, parallel)
  │ Stage 2: E←(A,B,C,D), G←(B), H←(F)
  │ Stage 3: I←(F,G,H)
  │
  ├──────────────────────────────┐
  ▼                              ▼
R³ Base Output               H³ Temporal Integration
(B, T, 128)                  For each demanded (r3_idx, horizon, morph, law):
 = 128 spectral features       Window R³ base data → apply morph → temporal event
 @ 172.27 Hz
  │                              │
  ▼                              ▼
  └──────────┬───────────────────┘
             ▼
      C³ Input Package
      ┌─────────────────────────────────────┐
      │ .base[idx]           → R³ raw value │
      │ .temporal[address]   → H³ morph     │
      │ .provenance[address] → full chain   │
      └─────────────────────────────────────┘
```

### 2.2 The Two Data Streams

**Stream A — R³ Base (always available)**

Every C³ model can access the raw R³ values at frame resolution. These are the 5.8ms micro-reports:

```python
# C³ model accesses R³ base
roughness_now = input.base[0]           # scalar, current frame
chroma_now = input.base[49:61]          # 12D vector, current frame
onset_now = input.base[11]              # scalar, current frame

# These are instantaneous spectral measurements.
# No temporal context. No interpretation. Pure physics.
```

**Stream B — H³ Temporal (demand-driven)**

Each C³ model declares its H³ demands. These are processed by H³ and delivered as morph values with provenance:

```python
# C³ model accesses H³ temporal data
demand = (83, H12, M9, L0)  # chroma_frame_distance, beat, velocity_mean, memory

result = input.temporal[demand]
# result.value = 0.073       (the morph value)
# result.morph = M9          (velocity_mean)
# result.law = L0            (memory: looking backward)
# result.horizon = H12       (525ms window)
# result.r3_source = {
#     index: 83,
#     name: "chroma_frame_distance",
#     group: "H",
#     spectral_definition: "1 - cosine_similarity(chroma_t, chroma_{t-1})",
#     unit: "dimensionless [0,1]",
#     frame_rate: 172.27
# }
# result.interpretation =
#     "Mean rate of change of inter-frame chroma cosine distance
#      over the past 525ms (beat-length memory window).
#      High value = chroma distribution changing rapidly.
#      Low value = chroma distribution stable."
```

---

## 3. The Provenance Chain

### 3.1 Why Provenance is Mandatory

Without provenance, C³ sees a naked number: `0.073`. This is useless:
- Is it big or small? (depends on the morph's range)
- What does it represent? (depends on the R³ source)
- At what timescale? (depends on the horizon)
- Looking forward or backward? (depends on the law)

With provenance, C³ sees:
> "The average rate of spectral reorganization in the pitch-class domain over the past half-second is 0.073, which is in the lower-moderate range, indicating gentle chroma evolution."

This is the difference between a system that works and a system that collapses.

### 3.2 Provenance Data Structure

Every H³ output carries this structure:

```
H3Output {
  ── VALUE ──
  value: float                    # The computed morph value, normalized [0,1]

  ── H³ PROCESSING ──
  morph: MorphSpec {
    index: int                    # M0-M23
    name: str                     # "velocity_mean"
    category: str                 # "dynamics"
    formula: str                  # "mean(dx/dt) over window"
    output_range: (float, float)  # raw range before normalization
  }
  law: LawSpec {
    index: int                    # L0-L2
    name: str                     # "memory"
    direction: str                # "past → present"
    kernel: str                   # "A(dt) = exp(-3|dt|/H), past only"
  }
  horizon: HorizonSpec {
    index: int                    # H0-H31
    frames: int                   # 90 (for H12)
    duration_ms: float            # 525.0
    perceptual_label: str         # "beat"
    band: str                     # "meso"
  }

  ── R³ SOURCE ──
  r3_source: R3FeatureSpec {
    index: int                    # 83
    name: str                     # "chroma_frame_distance"
    spectral_name: str            # same (no music-theory alias)
    group: str                    # "H"
    group_name: str               # "spectral_harmony"
    spectral_definition: str      # "1 - cosine_sim(chroma_t, chroma_{t-1})"
    computation: str              # "cosine distance between successive 12D
                                  #  pitch-class energy distributions"
    input_source: str             # "mel spectrogram → chroma soft-assignment"
    dependencies: list[int]       # [49,50,...,60] (chroma features from Group F)
    unit: str                     # "dimensionless"
    raw_range: (float, float)     # (0.0, 1.0)
    warm_up_frames: int           # 1 (no warm-up needed)
    quality_tier: str             # "standard"
  }

  ── HUMAN-READABLE ──
  address: str                    # "83.H12.M9.L0"
  spectral_label: str             # "chroma_frame_distance.beat.velocity_mean.memory"
  interpretation: str             # "Mean rate of change of inter-frame chroma
                                  #  cosine distance over past 525ms"
}
```

### 3.3 Address Format

Every H³ output has a unique address in two formats:

**Numeric**: `{r3_idx}.{horizon_idx}.{morph_idx}.{law_idx}`
```
83.H12.M9.L0
```

**Spectral label**: `{r3_spectral_name}.{horizon_label}.{morph_name}.{law_name}`
```
chroma_frame_distance.beat.velocity_mean.memory
```

Both formats are valid. The spectral label is for human readers. The numeric address is for computation.

---

## 4. R³-H³ Matrix: Structure

### 4.1 The Matrix Concept

The R³-H³ matrix defines, for each R³ feature, which H³ combinations produce meaningful outputs:

```
           ┌─────────── HORIZONS ───────────┐
           │ micro    meso    macro    ultra │
R³         │ H0..H7   H8..H15 H16..H23 H24+│
Features   ├────────────────────────────────┤
[0] rough  │ ○●○○○○○○ ●●●●○○○○ ●●○○○○○○ ○○○│
[1] seth   │ ○●○○○○○○ ●●●●○○○○ ●●○○○○○○ ○○○│
...        │                                 │
[83] chfrd │ ○○○○○●●● ●●●●●●●● ●●●●○○○○ ○○○│
...        │                                 │
[127] slpe │ ○○○○○○○○ ○○●●●●○○ ●●●●●●○○ ○○○│
           └────────────────────────────────┘

● = meaningful combination (demanded by C³ models)
○ = not demanded or not meaningful
```

For each ● cell, the matrix specifies which morphs and laws apply.

### 4.2 Meaningful Combinations

Not every R³ × H³ combination makes sense:

| R³ Feature Type | Meaningful Horizons | Meaningful Morphs | Reasoning |
|-----------------|--------------------|--------------------|-----------|
| Fast-varying (roughness, onset) | H3+ (≥25ms) | M1,M2,M4,M5,M8,M14 | Need enough samples for statistics |
| Slow-varying (chroma stability) | H8+ (≥300ms) | M1,M18,M19,M20 | Need perceptual timescale |
| Already-temporal (tempo, beat) | H12+ (≥525ms) | M18,M19,M2,M14 | Second-order temporal: need long windows |
| Information (entropy, surprise) | H9+ (≥340ms) | M1,M4,M8,M18,M20 | Warm-up + statistical stability |
| Broadband (amplitude, loudness) | H0+ (any) | All 24 | Meaningful at all timescales |

### 4.3 Matrix Example: Group H (Spectral Harmony, indices 75-86)

Below is the full matrix for Group H, showing which horizon-morph-law combinations are meaningful:

#### R³[75] — `pitch_class_profile_correlation_peak` (was: key_clarity)

**Spectral definition**: Maximum correlation between 12D pitch-class energy distribution and 24 Krumhansl-Kessler reference profiles. Measures how strongly spectral energy clusters into a single reference pattern.

```
Horizon    Morph                   Law    Spectral Label
─────────────────────────────────────────────────────────────────────
H6 (200ms) M1  mean               L2     pcpc_peak.sub_beat.mean.integration
           M2  std                L2     pcpc_peak.sub_beat.std.integration
           M5  range              L2     pcpc_peak.sub_beat.range.integration

H12(525ms) M1  mean               L0     pcpc_peak.beat.mean.memory
           M2  std                L0     pcpc_peak.beat.std.memory
           M8  velocity           L0     pcpc_peak.beat.velocity.memory
           M18 trend              L0     pcpc_peak.beat.trend.memory
           M19 stability          L0     pcpc_peak.beat.stability.memory
           M4  max                L1     pcpc_peak.beat.max.prediction

H16(1.0s)  M1  mean               L0     pcpc_peak.phrase.mean.memory
           M18 trend              L0     pcpc_peak.phrase.trend.memory
           M19 stability          L0     pcpc_peak.phrase.stability.memory
           M5  range              L2     pcpc_peak.phrase.range.integration

H18(2.0s)  M18 trend              L0     pcpc_peak.section.trend.memory
           M19 stability          L0     pcpc_peak.section.stability.memory
           M14 periodicity        L2     pcpc_peak.section.periodicity.integration
```

**What C³ learns from these**:
- `pcpc_peak.beat.mean.memory` = average spectral clustering strength over past beat → high = spectrally organized
- `pcpc_peak.beat.trend.memory` = is clustering strengthening or weakening? → positive = spectral organization increasing
- `pcpc_peak.phrase.stability.memory` = how consistent is clustering over a phrase? → high = spectrally stable
- `pcpc_peak.section.periodicity.integration` = does clustering oscillate periodically? → high = alternating spectral organization patterns

**C³ translation**: A paper says "strong key center with increasing tonal stability." Spectral: `pcpc_peak.beat.mean.memory > 0.7 AND pcpc_peak.phrase.trend.memory > 0`.

#### R³[83] — `chroma_frame_distance` (was: harmonic_change)

**Spectral definition**: `1 - cosine_similarity(chroma_t, chroma_{t-1})`. Measures frame-to-frame change in 12D pitch-class energy distribution.

```
Horizon    Morph                   Law    Spectral Label
─────────────────────────────────────────────────────────────────────
H6 (200ms) M1  mean               L0     chroma_dist.sub_beat.mean.memory
           M4  max                L0     chroma_dist.sub_beat.max.memory
           M2  std                L2     chroma_dist.sub_beat.std.integration

H9 (340ms) M1  mean               L0     chroma_dist.meso.mean.memory
           M14 periodicity        L2     chroma_dist.meso.periodicity.integration

H12(525ms) M1  mean               L0     chroma_dist.beat.mean.memory
           M2  std                L0     chroma_dist.beat.std.memory
           M4  max                L0     chroma_dist.beat.max.memory
           M8  velocity           L0     chroma_dist.beat.velocity.memory
           M9  velocity_mean      L0     chroma_dist.beat.velocity_mean.memory
           M14 periodicity        L2     chroma_dist.beat.periodicity.integration
           M18 trend              L0     chroma_dist.beat.trend.memory
           M18 trend              L1     chroma_dist.beat.trend.prediction

H16(1.0s)  M1  mean               L0     chroma_dist.phrase.mean.memory
           M4  max                L0     chroma_dist.phrase.max.memory
           M18 trend              L0     chroma_dist.phrase.trend.memory
           M19 stability          L0     chroma_dist.phrase.stability.memory

H18(2.0s)  M18 trend              L0     chroma_dist.section.trend.memory
           M14 periodicity        L2     chroma_dist.section.periodicity.integration
           M20 entropy            L2     chroma_dist.section.entropy.integration
```

**What C³ learns from these**:
- `chroma_dist.beat.mean.memory` = average chroma change rate per beat → high = "rapid spectral reorganization in pitch-class space"
- `chroma_dist.beat.periodicity.integration` = does chroma change rhythmically? → high = "periodic spectral reorganization" (what a musician would call "harmonic rhythm")
- `chroma_dist.section.trend.memory` = is chroma change rate increasing over 2s? → positive = "spectral evolution accelerating"

#### R³[76:81] — `tonnetz_*` → `pitch_class_geometry_*`

**Spectral definition**: Projection of 12D chroma onto 3 harmonic circles (fifths, minor-thirds, major-thirds). 6D geometric position of pitch-class energy distribution.

```
Horizon    Morph                   Law    Spectral Label
─────────────────────────────────────────────────────────────────────
H12(525ms) M1  mean               L0     pcg_fifth_x.beat.mean.memory
           M8  velocity           L0     pcg_fifth_x.beat.velocity.memory
           (same for all 6 tonnetz dimensions)

           M5  range (on 6D norm) L2     pcg_norm.beat.range.integration

H16(1.0s)  M18 trend (on norm)   L0     pcg_norm.phrase.trend.memory
           M14 period (on norm)  L2     pcg_norm.phrase.periodicity.integration

H22(8.5s)  M18 trend (on norm)   L0     pcg_norm.passage.trend.memory
```

**What C³ learns**:
- `pcg_fifth_x.beat.velocity.memory` = rate of movement along the fifths circle → high = "spectral energy traversing the fifths-circle geometry rapidly"
- `pcg_norm.phrase.periodicity.integration` = does the pitch-class geometry oscillate periodically over phrases? → high = "cyclic spectral pattern" (what theory calls "circle-of-fifths modulation")

---

## 5. C³ Model Interface Contract

### 5.1 What a C³ Model Declares

Each C³ model declares its data requirements in two parts:

**Part A — R³ Base Demands (frame-level)**
```python
R3_BASE_DEMANDS = [
    0,    # roughness (instantaneous spectral roughness)
    7,    # amplitude (instantaneous spectral energy)
    11,   # onset_strength (spectral change detection)
    83,   # chroma_frame_distance (pitch-class distribution change)
]
```

**Part B — H³ Temporal Demands (horizon-integrated)**
```python
H3_DEMANDS = [
    # (r3_idx, horizon, morph, law)
    (83, 12, 9, 0),   # chroma_dist.beat.velocity_mean.memory
    (75, 12, 18, 0),  # pcpc_peak.beat.trend.memory
    (90, 12, 4, 0),   # spectral_surprise.beat.max.memory
    (0,  12, 5, 2),   # roughness.beat.range.integration
]
```

### 5.2 What a C³ Model Receives

For each frame, the model receives:

```python
class C3Input:
    # R³ base values (frame-level, 5.8ms)
    base: Tensor           # shape (B, T, len(R3_BASE_DEMANDS))

    # H³ morph values (temporally integrated)
    temporal: Tensor       # shape (B, T, len(H3_DEMANDS))

    # Provenance metadata (static, set at initialization)
    provenance: list[H3Provenance]  # one per H3_DEMAND entry
```

### 5.3 How a C³ Model Document Maps Paper Concepts

Every C³ model document (Section 3: R³ Input Mapping) contains a table like:

```
┌──────────────────────────────────────────────────────────────────────┐
│ MODEL: PUPF (Pleasure-Uncertainty Prediction Function)               │
│ PAPER: Cheung et al. 2019 — "Uncertainty and surprise jointly        │
│        predict musical pleasure"                                     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ Paper Concept         │ Spectral Mapping           │ Address          │
│ ─────────────────────┼────────────────────────────┼──────────────── │
│ "Uncertainty (U)"     │ pitch_class_transition_    │ [87].H12.M1.L0  │
│                       │ entropy.beat.mean.memory   │                  │
│                       │                            │                  │
│ "Surprise (S)"        │ chroma_distribution_       │ [88].H12.M4.L0  │
│                       │ divergence.beat.max.memory │                  │
│                       │                            │                  │
│ "Pleasure = f(U,S)"   │ Computed by PUPF model     │ (C³ internal)   │
│                       │ from spectral inputs above │                  │
│                       │                            │                  │
│ "Tonal context"       │ pcpc_peak.phrase.          │ [75].H16.M1.L0  │
│                       │ mean.memory                │                  │
│                       │                            │                  │
│ "Arousal baseline"    │ amplitude.beat.            │ [7].H12.M1.L0   │
│                       │ mean.memory                │                  │
│                       │                            │                  │
│ PROVENANCE NARRATIVE:                                                │
│ "PUPF computes musical pleasure as a function of uncertainty and     │
│  surprise (Cheung 2019). Uncertainty is measured as the mean entropy │
│  of pitch-class transition probabilities over beat-length windows    │
│  [87.H12.M1.L0], which captures how predictable the pitch-class     │
│  sequence has been. Surprise is measured as the peak divergence of   │
│  pitch-class energy distribution from its running average over       │
│  beat-length windows [88.H12.M4.L0]. Both are purely spectral       │
│  measurements — no chord or key labels are used."                    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 6. The R³-H³ Matrix: Complete Structure

### 6.1 Matrix Organization

The full matrix is organized by R³ GROUP, not by individual features, because features within a group share temporal characteristics:

```
GROUP A: Spectral Consonance [0:6]    — 7 features  × relevant horizons
GROUP B: Spectral Energy [7:11]       — 5 features  × relevant horizons
GROUP C: Spectral Timbre [12:20]      — 9 features  × relevant horizons
GROUP D: Spectral Change [21:24]      — 4 features  × relevant horizons
GROUP E: Spectral Interactions [25:48]— 24 features × relevant horizons
GROUP F: Pitch-Class Distribution [49:64]   — 16 features × relevant horizons
GROUP G: Onset Periodicity [65:74]          — 10 features × relevant horizons
GROUP H: Spectral Harmony [75:86]           — 12 features × relevant horizons
GROUP I: Spectral Information [87:93]       — 7 features  × relevant horizons
GROUP J: Spectral Timbre Extended [94:113]  — 20 features × relevant horizons
GROUP K: Spectral Modulation [114:127]      — 14 features × relevant horizons
```

Note: Group names are now spectral. "Harmony & Tonality" → "Spectral Harmony". "Information & Surprise" → "Spectral Information". "Rhythm & Groove" → "Onset Periodicity".

### 6.2 Horizon Relevance by Group

| Group | Micro (H0-H7) | Meso (H8-H15) | Macro (H16-H23) | Ultra (H24-H31) | Reasoning |
|-------|:-:|:-:|:-:|:-:|-----------|
| A: Consonance | ●● | ●●● | ●● | ○ | Roughness/fusion vary at note-to-phrase scales |
| B: Energy | ●●● | ●●● | ●● | ● | Energy varies at all scales |
| C: Timbre | ● | ●●● | ●●● | ● | Timbre varies at phrase-to-section scales |
| D: Change | ●● | ●●● | ●● | ○ | Change is inherently short-to-medium term |
| E: Interactions | ○ | ●● | ●●● | ● | Cross-domain patterns need extended context |
| F: Pitch-Class | ● | ●●● | ●●● | ●● | Chroma evolves at beat-to-section scales |
| G: Onset Period. | ○ | ●● | ●●● | ●● | Already temporal; 2nd-order needs long windows |
| H: Spectral Harm. | ● | ●●● | ●●● | ● | Tonal patterns at beat-to-section scales |
| I: Spectral Info. | ○ | ●●● | ●●● | ● | Information features need statistical stability |
| J: Timbre Ext. | ● | ●● | ●●● | ●● | MFCCs/contrast evolve at phrase-to-movement scales |
| K: Modulation | ○ | ●● | ●●● | ●●● | Modulation rates are inherently slow |

### 6.3 Morph Relevance by Feature Type

| Feature Type | Primary Morphs | Secondary Morphs | Reasoning |
|-------------|----------------|-------------------|-----------|
| **Level features** (roughness, loudness, chroma) | M1(mean), M2(std), M4(max), M5(range) | M3(median), M6(skew), M7(kurt) | Statistical distribution of values |
| **Rate features** (spectral_flux, chroma_dist) | M1(mean), M8(vel), M18(trend) | M2(std), M14(period), M19(stab) | How fast things change, and is the rate itself changing? |
| **Periodic features** (tempo, beat_strength) | M14(period), M18(trend), M19(stab) | M2(std), M5(range) | Second-order periodicity; is the period stable? |
| **Entropy features** (pc_entropy, pred_entropy) | M1(mean), M18(trend), M4(max) | M2(std), M5(range), M19(stab) | Predictability patterns over time |
| **Geometric features** (tonnetz, spiral_array) | M8(vel), M18(trend), M14(period) | M1(mean), M5(range) | Movement in geometric space |

---

## 7. Naming Convention: R³ Feature Renaming

### 7.1 Complete Spectral Naming Table

The following table maps every R³ feature from its current (possibly music-theory) name to its spectral name. **The computation does not change — only the name.**

#### Group A: Spectral Consonance [0:6]
| Idx | Current Name | Spectral Name | Change? |
|-----|-------------|---------------|---------|
| 0 | roughness | roughness | No |
| 1 | sethares_dissonance | sethares_dissonance | No |
| 2 | helmholtz_kang | helmholtz_fusion_index | Minor |
| 3 | stumpf_fusion | stumpf_fusion | No |
| 4 | sensory_pleasantness | sensory_pleasantness | No |
| 5 | inharmonicity | inharmonicity | No |
| 6 | harmonic_deviation | partial_deviation | Minor |

#### Group B: Spectral Energy [7:11]
| Idx | Current Name | Spectral Name | Change? |
|-----|-------------|---------------|---------|
| 7 | amplitude | amplitude | No |
| 8 | velocity_A | amplitude_velocity | No |
| 9 | acceleration_A | amplitude_acceleration | No |
| 10 | loudness | loudness | No |
| 11 | onset_strength | onset_strength | No |

#### Group C: Spectral Timbre [12:20]
| Idx | Current Name | Spectral Name | Change? |
|-----|-------------|---------------|---------|
| 12 | warmth | spectral_warmth | No |
| 13 | sharpness | spectral_sharpness | No |
| 14 | tonalness | spectral_periodicity | **Yes** — "tonalness" implies music-theory "tonal" |
| 15 | clarity | spectral_clarity | No |
| 16 | spectral_smoothness | spectral_smoothness | No |
| 17 | spectral_autocorrelation | spectral_autocorrelation | No |
| 18-20 | tristimulus1/2/3 | tristimulus_low/mid/high | Minor |

#### Group D: Spectral Change [21:24]
| Idx | Current Name | Spectral Name | Change? |
|-----|-------------|---------------|---------|
| 21 | spectral_flux | spectral_flux | No |
| 22 | distribution_entropy | spectral_entropy | Minor |
| 23 | distribution_flatness | spectral_flatness | Minor |
| 24 | distribution_concentration | spectral_concentration | Minor |

#### Group E: Spectral Interactions [25:48]
| Idx | Current Name | Spectral Name | Change? |
|-----|-------------|---------------|---------|
| 25:32 | energy×consonance | energy_consonance_product_0..7 | No |
| 33:40 | change×consonance | change_consonance_product_0..7 | No |
| 41:48 | consonance×timbre | consonance_timbre_product_0..7 | No |

#### Group F: Pitch-Class Distribution [49:64]
| Idx | Current Name | Spectral Name | Change? |
|-----|-------------|---------------|---------|
| 49:60 | chroma_0..11 | pitch_class_energy_0..11 | **Yes** — "chroma" is OK but "pitch_class_energy" is more explicit |
| 61 | pitch_height | spectral_centroid_log | **Yes** — describes the actual computation |
| 62 | pitch_class_entropy | pitch_class_distribution_entropy | Minor |
| 63 | pitch_salience | pitch_class_peak_salience | Minor |
| 64 | inharmonicity_index | spectral_inharmonicity_ratio | Minor |

#### Group G: Onset Periodicity [65:74]
| Idx | Current Name | Spectral Name | Change? |
|-----|-------------|---------------|---------|
| 65 | tempo_estimate | onset_period_dominant | **Yes** — "tempo" implies musical meter |
| 66 | beat_strength | onset_autocorrelation_peak | **Yes** — "beat" implies metrical structure |
| 67 | pulse_clarity | onset_periodicity_clarity | **Yes** — "pulse" implies beat |
| 68 | syncopation_index | onset_offbeat_ratio | **Yes** — "syncopation" is music-theory |
| 69 | metricality_index | onset_subdivision_depth | **Yes** — "metricality" is music-theory |
| 70 | isochrony_nPVI | onset_interval_regularity | **Yes** — clearer spectral description |
| 71 | groove_index | onset_offbeat_bass_pulse_product | **Yes** — "groove" is subjective |
| 72 | event_density | onset_density | Minor |
| 73 | tempo_stability | onset_period_stability | **Yes** — "tempo" → "onset_period" |
| 74 | rhythmic_regularity | onset_interval_entropy_inv | **Yes** — describes computation |

#### Group H: Spectral Harmony [75:86]
| Idx | Current Name | Spectral Name | Change? |
|-----|-------------|---------------|---------|
| 75 | key_clarity | pitch_class_profile_correlation_peak | **Yes** |
| 76:81 | tonnetz_fifth_x/y, minor_x/y, major_x/y | pitch_class_geometry_5th_x/y, 3rd_min_x/y, 3rd_maj_x/y | **Yes** |
| 82 | voice_leading_distance | chroma_L1_distance | **Yes** |
| 83 | harmonic_change | chroma_frame_distance | **Yes** |
| 84 | tonal_stability | chroma_distribution_temporal_consistency | **Yes** |
| 85 | diatonicity | pitch_class_template_fit_max | **Yes** |
| 86 | syntactic_irregularity | chroma_divergence_from_reference | **Yes** |

#### Group I: Spectral Information [87:93]
| Idx | Current Name | Spectral Name | Change? |
|-----|-------------|---------------|---------|
| 87 | melodic_entropy | pitch_class_transition_entropy | **Yes** |
| 88 | harmonic_entropy | chroma_distribution_divergence | **Yes** |
| 89 | rhythmic_information_content | onset_interval_surprisal | **Yes** |
| 90 | spectral_surprise | spectral_distribution_divergence | Minor |
| 91 | information_rate | spectral_mutual_information | Minor |
| 92 | predictive_entropy | spectral_prediction_uncertainty | Minor |
| 93 | tonal_ambiguity | pitch_class_distribution_entropy_keyed | **Yes** |

#### Groups J, K: Already spectral — minimal renaming needed.

### 7.2 Group Renaming

| Current Group Name | Spectral Group Name |
|-------------------|-------------------|
| A: Consonance | A: Spectral Consonance |
| B: Energy | B: Spectral Energy |
| C: Timbre | C: Spectral Timbre |
| D: Change | D: Spectral Change |
| E: Interactions | E: Spectral Interactions |
| F: Pitch & Chroma | F: Pitch-Class Distribution |
| G: Rhythm & Groove | G: Onset Periodicity |
| H: Harmony & Tonality | H: Spectral Harmony |
| I: Information & Surprise | I: Spectral Information |
| J: Timbre Extended | J: Spectral Timbre Extended |
| K: Modulation & Psychoacoustic | K: Spectral Modulation |

---

## 8. Example: End-to-End Trace

### Scenario: C³ model EDNR (Expertise-Dependent Neural Response) needs "harmonic surprise"

**Step 1 — EDNR paper says:**
> "Experts show reduced N1/P2 amplitude for expected chords but enhanced response to unexpected harmonic events (Koelsch 2011)."

**Step 2 — Translate to spectral language:**
> "Listeners with trained auditory models show reduced cortical prediction error for spectrally predictable pitch-class distributions but enhanced error for unexpected pitch-class reorganization."

**Step 3 — Map to R³+H³ addresses:**

```
R³ Base (5.8ms, for onset detection):
  [11] onset_strength                → instant spectral change detection
  [83] chroma_frame_distance         → instant pitch-class reorganization

H³ Temporal (beat-level, ~525ms):
  [88].H12.M4.L0  → chroma_distribution_divergence.beat.max.memory
    "Peak divergence of pitch-class distribution from running average
     over past 525ms. High = unexpected pitch-class reorganization."

  [83].H12.M9.L0  → chroma_frame_distance.beat.velocity_mean.memory
    "Mean rate of pitch-class distance change over past 525ms.
     Increasing = accelerating spectral reorganization."

  [92].H12.M1.L0  → spectral_prediction_uncertainty.beat.mean.memory
    "Mean prediction uncertainty of spectral distribution over past 525ms.
     High = uncertain spectral predictions (high entropy in residuals)."

H³ Temporal (phrase-level, ~1s):
  [75].H16.M19.L0 → pitch_class_profile_correlation_peak.phrase.stability.memory
    "Stability of pitch-class clustering strength over past 1s.
     High = consistent spectral organization (context for surprise)."
```

**Step 4 — EDNR model computation:**
```python
# All inputs are spectral. No "chord" or "key" labels.
# The model computes "harmonic surprise" INTERNALLY from spectral evidence.

surprise = temporal[88_H12_M4_L0]          # peak chroma divergence
context_stability = temporal[75_H16_M19_L0] # spectral organization stability
prediction_error = temporal[92_H12_M1_L0]   # prediction uncertainty

# Model-internal: high surprise in stable context = strong N1/P2
# This IS what the paper calls "unexpected harmonic event"
# But the computation is purely spectral.
```

**Step 5 — Provenance chain (traceable at any point):**
```
EDNR output "harmonic_surprise_response" = 0.82

Trace:
  ← EDNR model internal computation
    ← H³ morph: chroma_distribution_divergence.beat.max.memory = 0.73
      ← R³ feature [88] chroma_distribution_divergence
        ← KL(pitch_class_energy_t || running_avg_pitch_class_energy)
          ← Group F: pitch_class_energy_0..11 (12D chroma from mel)
            ← Mel spectrogram → 128×12 Gaussian soft-assignment
              ← Audio (44.1kHz)
```

Every number traces back to audio through an unbroken chain of spectral operations.

---

## 9. Migration Notes

### 9.1 What Changes

1. **Feature names** in `constants/feature_names.py` → spectral names
2. **Group names** in group classes → spectral group names
3. **C³ model docs** Section 3 → spectral mapping tables with provenance
4. **H³ demand declarations** → use spectral addresses
5. **Documentation language** → spectral throughout

### 9.2 What Does NOT Change

1. **Computation** — all math stays exactly the same
2. **128D dimensionality** — same features, different names
3. **3-stage DAG** — same pipeline structure
4. **H³ morph/horizon/law system** — same 24×32×3 architecture
5. **C³ model logic** — same internal computations

### 9.3 Backward Compatibility

Old names can be maintained as aliases during transition:
```python
# In feature_names.py
FEATURE_ALIASES = {
    "key_clarity": 75,                    # → pitch_class_profile_correlation_peak
    "harmonic_change": 83,                # → chroma_frame_distance
    "melodic_entropy": 87,                # → pitch_class_transition_entropy
    "tonal_stability": 84,                # → chroma_distribution_temporal_consistency
    # ... etc
}
```

---

**Next**: [03_TRANSLATION_GUIDE.md](03_TRANSLATION_GUIDE.md) — Complete mapping of music theory terms to spectral equivalents, for use in C³ model documentation.
