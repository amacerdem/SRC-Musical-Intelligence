# R3 Spectral Architecture

**Version**: 2.0.0
**Dimensions**: 128D (11 groups, 6 domains)
**Source**: R3-V2-DESIGN.md (Phase 3B Architecture Design)
**Updated**: 2026-02-13

---

## Table of Contents

1. [Design Philosophy](#1-design-philosophy)
2. [Pipeline Overview](#2-pipeline-overview)
3. [128D Dimension Inventory](#3-128d-dimension-inventory)
4. [Domain Taxonomy](#4-domain-taxonomy)
5. [Input Contract](#5-input-contract)
6. [Output Contract](#6-output-contract)
7. [Auto-Discovery Mechanism](#7-auto-discovery-mechanism)
8. [Extension Model](#8-extension-model)
9. [Dependency Graph](#9-dependency-graph)
10. [Code Structure Mapping](#10-code-structure-mapping)
11. [Real-Time Feasibility](#11-real-time-feasibility)
12. [Warm-up Behavior](#12-warm-up-behavior)

---

## 1. Design Philosophy

R3 v2 follows a **domain-based modular architecture** designed around four principles:

1. **Psychoacoustic Grounding**: Every feature dimension has a documented psychoacoustic basis or computational motivation. Features are organized by perceptual domain (consonance, pitch, rhythm, harmony, information, timbre, modulation) rather than by implementation convenience.

2. **Backward Compatibility**: The original 49 dimensions (`[0:49]`, groups A-E) are preserved at their existing indices. New features are appended in the range `[49:128]`. This ensures that all existing C3 model documentation referencing feature indices remains valid.

3. **Auto-Discovery and Extensibility**: Groups are auto-discovered from subdirectory exports. New groups can be added by placing a `BaseSpectralGroup` subclass in the `extensions/` directory without modifying any core files. The `R3FeatureRegistry` assigns index ranges at freeze time.

4. **Real-Time GPU Feasibility**: The full 128D vector is computed within the frame budget of 5.8 ms (at 172.27 Hz frame rate) using a 3-stage parallel execution DAG. Power-of-2 dimensionality (128 = 2^7) provides optimal GPU tensor alignment.

### Design Inputs

The v2 architecture was designed through a three-perspective synthesis:

| Perspective | Source | Contribution |
|------------|--------|-------------|
| **R1** (Bottom-up) | 96 C3 model gap analysis | Identified 31 acoustic gaps; demanded 19+ new features |
| **R2** (Literature) | 121 psychoacoustic papers | Validated features against perceptual science; found quality issues in v1 |
| **R3** (Toolkit) | 6 MIR toolkits + standards | Established computational feasibility and implementation patterns |

**Consensus**: All three perspectives agreed that 128D is the appropriate target. R1 demands are fully met, R2 psychoacoustic coverage is comprehensive, and R3 confirms real-time GPU feasibility.

---

## 2. Pipeline Overview

```
Audio Signal
    |
    v
Cochlea (mel spectrogram: B, 128, T @ 172.27 Hz, 44100 Hz SR)
    |
    v
+================================================================+
|                     R3 Spectral Extractor                      |
|                                                                |
|  STAGE 1 (parallel):                                           |
|    A: Consonance (7D)      B: Energy (5D)     C: Timbre (9D)  |
|    D: Change (4D)          F: Pitch (16D)     J: TimbreExt(20D)|
|    K: Modulation (14D)                                         |
|    [All groups read mel directly -- fully parallel]            |
|                                                                |
|  STAGE 2 (parallel, after Stage 1):                            |
|    E: Interactions (24D)   <- A, B, C, D outputs               |
|    G: Rhythm (10D)         <- B[11] onset_strength             |
|    H: Harmony (12D)        <- F[49:61] chroma                  |
|                                                                |
|  STAGE 3 (after Stages 1+2):                                  |
|    I: Information (7D)     <- F chroma, G onset, H key, mel   |
|                                                                |
|  CONCAT: torch.cat([A,B,C,D,E,F,G,H,I,J,K], dim=-1)         |
+================================================================+
    |
    v
R3 Output: (B, T, 128) feature tensor, [0,1] range
    |
    v
Brain (C3 models: SPU, STU, IMU, ASU, NDU, MPU, PCU, ARU, RPU)
```

The pipeline is strictly feedforward. Each frame of the mel spectrogram is processed independently (except for features requiring running statistics, which maintain internal state).

---

## 3. 128D Dimension Inventory

### Group Summary

| Group | Name | Range | Dim | Domain | Status | Stage | Est. Cost |
|-------|------|-------|:---:|--------|--------|:-----:|-----------|
| A | Consonance | [0:7] | 7 | Psychoacoustic | Existing | 1 | ~0.1 ms |
| B | Energy | [7:12] | 5 | Spectral | Existing | 1 | ~0.1 ms |
| C | Timbre | [12:21] | 9 | Spectral | Existing | 1 | ~0.1 ms |
| D | Change | [21:25] | 4 | Temporal | Existing | 1 | ~0.1 ms |
| E | Interactions | [25:49] | 24 | CrossDomain | Existing | 2 | ~0.1 ms |
| F | Pitch & Chroma | [49:65] | 16 | Tonal | New | 1 | ~1.0 ms |
| G | Rhythm & Groove | [65:75] | 10 | Temporal | New | 2 | ~0.8 ms |
| H | Harmony & Tonality | [75:87] | 12 | Tonal | New | 2 | ~1.0 ms |
| I | Information & Surprise | [87:94] | 7 | Information | New | 3 | ~0.8 ms |
| J | Timbre Extended | [94:114] | 20 | Spectral | New | 1 | ~0.5 ms |
| K | Modulation & Psychoacoustic | [114:128] | 14 | Psychoacoustic | New | 1 | ~0.5 ms* |
| | **Total** | **[0:128]** | **128** | | | | |

*K group cost is amortized; full FFT runs every 86 frames.

### Complete Dimension Table

#### Group A: Consonance [0:7] -- 7D (Existing)

| Index | Feature Name | Psychoacoustic Basis |
|:-----:|-------------|---------------------|
| 0 | roughness | Plomp-Levelt critical band beating (proxy) |
| 1 | sethares_dissonance | Sethares timbre-dependent dissonance (proxy) |
| 2 | helmholtz_kang | Periodicity detection, lag-1 autocorrelation |
| 3 | stumpf_fusion | Stumpf tonal fusion, low-frequency ratio (proxy) |
| 4 | sensory_pleasantness | Harrison & Pearce 2020 consonance model |
| 5 | inharmonicity | Harmonic series deviation (derived from [2]) |
| 6 | harmonic_deviation | Spectral irregularity (derived from [1],[2]) |

#### Group B: Energy [7:12] -- 5D (Existing)

| Index | Feature Name | Psychoacoustic Basis |
|:-----:|-------------|---------------------|
| 7 | amplitude | RMS energy |
| 8 | velocity_A | Energy change rate (1st derivative) |
| 9 | acceleration_A | Energy buildup curvature (2nd derivative) |
| 10 | loudness | Stevens' power law sone approximation |
| 11 | onset_strength | Spectral flux (HWR), neural sync driver |

#### Group C: Timbre [12:21] -- 9D (Existing)

| Index | Feature Name | Psychoacoustic Basis |
|:-----:|-------------|---------------------|
| 12 | warmth | Low-frequency energy balance |
| 13 | sharpness | High-frequency energy ratio |
| 14 | tonalness | Spectral peak dominance (Terhardt proxy) |
| 15 | clarity | Spectral centroid (normalized) |
| 16 | spectral_smoothness | Spectral envelope regularity |
| 17 | spectral_autocorrelation | Spectral periodicity |
| 18 | tristimulus1 | Fundamental strength (Pollard-Jansson) |
| 19 | tristimulus2 | Mid-harmonic energy |
| 20 | tristimulus3 | High-harmonic energy |

#### Group D: Change [21:25] -- 4D (Existing)

| Index | Feature Name | Psychoacoustic Basis |
|:-----:|-------------|---------------------|
| 21 | spectral_flux | L2 frame-to-frame spectral change |
| 22 | distribution_entropy | Shannon entropy of spectral distribution |
| 23 | distribution_flatness | Wiener entropy (MPEG-7 spectral flatness) |
| 24 | distribution_concentration | HHI-based spectral concentration |

#### Group E: Interactions [25:49] -- 24D (Existing)

| Index | Feature Name | Description |
|:-----:|-------------|-------------|
| 25-32 | x_l0l5 (8D) | Energy x Consonance cross-products |
| 33-40 | x_l4l5 (8D) | Change x Consonance cross-products |
| 41-48 | x_l5l7 (8D) | Consonance x Timbre cross-products |

#### Group F: Pitch & Chroma [49:65] -- 16D (New)

| Index | Feature Name | Psychoacoustic Basis |
|:-----:|-------------|---------------------|
| 49 | chroma_C | Octave equivalence: pitch class 0 (Shepard 1964) |
| 50 | chroma_Db | Octave equivalence: pitch class 1 |
| 51 | chroma_D | Octave equivalence: pitch class 2 |
| 52 | chroma_Eb | Octave equivalence: pitch class 3 |
| 53 | chroma_E | Octave equivalence: pitch class 4 |
| 54 | chroma_F | Octave equivalence: pitch class 5 |
| 55 | chroma_Gb | Octave equivalence: pitch class 6 |
| 56 | chroma_G | Octave equivalence: pitch class 7 |
| 57 | chroma_Ab | Octave equivalence: pitch class 8 |
| 58 | chroma_A | Octave equivalence: pitch class 9 |
| 59 | chroma_Bb | Octave equivalence: pitch class 10 |
| 60 | chroma_B | Octave equivalence: pitch class 11 |
| 61 | pitch_height | Weber-Fechner: perceived pitch ~ log(frequency) |
| 62 | pitch_class_entropy | Pitch distribution uniformity (information theory) |
| 63 | pitch_salience | Virtual pitch salience (Parncutt 1989 proxy) |
| 64 | inharmonicity_index | Harmonic series deviation measurement |

#### Group G: Rhythm & Groove [65:75] -- 10D (New)

| Index | Feature Name | Psychoacoustic Basis |
|:-----:|-------------|---------------------|
| 65 | tempo_estimate | Preferred tempo / entrainment (Fraisse 1982) |
| 66 | beat_strength | Pulse perception strength |
| 67 | pulse_clarity | Beat ambiguity measure (Witek 2014) |
| 68 | syncopation_index | LHL metrical conflict (Longuet-Higgins & Lee 1984) |
| 69 | metricality_index | Metrical hierarchy strength (Grahn & Brett 2007) |
| 70 | isochrony_nPVI | Rhythmic regularity (Ravignani 2021, nPVI) |
| 71 | groove_index | Movement-inducing quality (Madison 2006, Janata 2012) |
| 72 | event_density | Temporal density of auditory events |
| 73 | tempo_stability | Temporal prediction reliability |
| 74 | rhythmic_regularity | IOI distribution regularity (inverse entropy) |

#### Group H: Harmony & Tonality [75:87] -- 12D (New)

| Index | Feature Name | Psychoacoustic Basis |
|:-----:|-------------|---------------------|
| 75 | key_clarity | Tonal hierarchy (Krumhansl & Kessler 1982) |
| 76 | tonnetz_fifth_x | Tonal space: circle-of-fifths x (Harte 2006) |
| 77 | tonnetz_fifth_y | Tonal space: circle-of-fifths y |
| 78 | tonnetz_minor_x | Tonal space: minor-third x |
| 79 | tonnetz_minor_y | Tonal space: minor-third y |
| 80 | tonnetz_major_x | Tonal space: major-third x |
| 81 | tonnetz_major_y | Tonal space: major-third y |
| 82 | voice_leading_distance | Voice-leading parsimony (Tymoczko) |
| 83 | harmonic_change | Frame-to-frame harmonic shift (HCDF) |
| 84 | tonal_stability | Stability of tonal center over time |
| 85 | diatonicity | Tymoczko macroharmony: diatonic vs chromatic |
| 86 | syntactic_irregularity | Harmonic syntax violation (Lerdahl 2001) |

#### Group I: Information & Surprise [87:94] -- 7D (New)

| Index | Feature Name | Psychoacoustic Basis |
|:-----:|-------------|---------------------|
| 87 | melodic_entropy | Melodic prediction error (IDyOM approx., Pearce 2005) |
| 88 | harmonic_entropy | Chord transition surprise (Gold 2019) |
| 89 | rhythmic_information_content | Rhythmic surprise (Spiech 2022) |
| 90 | spectral_surprise | Spectral prediction error (Friston free energy) |
| 91 | information_rate | Mutual information per frame |
| 92 | predictive_entropy | Frame prediction uncertainty |
| 93 | tonal_ambiguity | Key profile entropy (tonal uncertainty) |

#### Group J: Timbre Extended [94:114] -- 20D (New)

| Index | Feature Name | Psychoacoustic Basis |
|:-----:|-------------|---------------------|
| 94 | mfcc_1 | Cepstral timbre coefficient 1 |
| 95 | mfcc_2 | Cepstral timbre coefficient 2 |
| 96 | mfcc_3 | Cepstral timbre coefficient 3 |
| 97 | mfcc_4 | Cepstral timbre coefficient 4 |
| 98 | mfcc_5 | Cepstral timbre coefficient 5 |
| 99 | mfcc_6 | Cepstral timbre coefficient 6 |
| 100 | mfcc_7 | Cepstral timbre coefficient 7 |
| 101 | mfcc_8 | Cepstral timbre coefficient 8 |
| 102 | mfcc_9 | Cepstral timbre coefficient 9 |
| 103 | mfcc_10 | Cepstral timbre coefficient 10 |
| 104 | mfcc_11 | Cepstral timbre coefficient 11 |
| 105 | mfcc_12 | Cepstral timbre coefficient 12 |
| 106 | mfcc_13 | Cepstral timbre coefficient 13 |
| 107 | spectral_contrast_1 | Octave sub-band 1 peak-valley (Jiang 2002) |
| 108 | spectral_contrast_2 | Octave sub-band 2 peak-valley |
| 109 | spectral_contrast_3 | Octave sub-band 3 peak-valley |
| 110 | spectral_contrast_4 | Octave sub-band 4 peak-valley |
| 111 | spectral_contrast_5 | Octave sub-band 5 peak-valley |
| 112 | spectral_contrast_6 | Octave sub-band 6 peak-valley |
| 113 | spectral_contrast_7 | Octave sub-band 7 (residual) peak-valley |

#### Group K: Modulation & Psychoacoustic [114:128] -- 14D (New)

| Index | Feature Name | Psychoacoustic Basis |
|:-----:|-------------|---------------------|
| 114 | modulation_0_5Hz | Cortical temporal modulation at 0.5 Hz (Chi/Shamma 2005) |
| 115 | modulation_1Hz | Phrase-level rhythmic modulation |
| 116 | modulation_2Hz | Beat-rate modulation |
| 117 | modulation_4Hz | Speech syllabic rate / strong beat |
| 118 | modulation_8Hz | Rapid articulation / tremolo |
| 119 | modulation_16Hz | Roughness boundary / vibrato upper limit |
| 120 | modulation_centroid | Dominant modulation rate |
| 121 | modulation_bandwidth | Modulation rate diversity |
| 122 | sharpness_zwicker | DIN 45692 perceptual sharpness (Zwicker & Fastl) |
| 123 | fluctuation_strength | Temporal fluctuation at ~4 Hz (Zwicker & Fastl) |
| 124 | loudness_a_weighted | ISO 226 frequency-weighted loudness |
| 125 | alpha_ratio | Low/high band energy ratio (eGeMAPS) |
| 126 | hammarberg_index | Spectral tilt measure (eGeMAPS) |
| 127 | spectral_slope_0_500 | Low-frequency spectral shape (eGeMAPS) |

---

## 4. Domain Taxonomy

R3 v2 organizes its 11 groups into 6 perceptual domains:

### 4.1 Psychoacoustic Domain

**Groups**: A (Consonance, 7D), K (Modulation & Psychoacoustic, 14D)
**Total**: 21D
**Scope**: Features grounded in fundamental psychoacoustic models -- roughness, dissonance, consonance, Zwicker sharpness, modulation perception, fluctuation strength.
**Code path**: `mi_beta/ear/r3/psychoacoustic/`

### 4.2 Spectral Domain

**Groups**: B (Energy, 5D), C (Timbre, 9D), J (Timbre Extended, 20D)
**Total**: 34D
**Scope**: Spectral shape, energy distribution, loudness, MFCC cepstral representation, spectral contrast. Pure spectral descriptors without explicit perceptual modeling.
**Code path**: `mi_beta/ear/r3/dsp/`

### 4.3 Tonal Domain

**Groups**: F (Pitch & Chroma, 16D), H (Harmony & Tonality, 12D)
**Total**: 28D
**Scope**: Pitch class profiles (chroma), pitch height, tonal hierarchy, key estimation, tonnetz coordinates, harmonic change detection, voice leading.
**Code path**: `mi_beta/ear/r3/extensions/` (new groups)

### 4.4 Temporal Domain

**Groups**: D (Change, 4D), G (Rhythm & Groove, 10D)
**Total**: 14D
**Scope**: Frame-to-frame spectral change, tempo estimation, beat tracking, syncopation, metricality, groove, rhythmic regularity.
**Code path**: `mi_beta/ear/r3/dsp/` (D), `mi_beta/ear/r3/extensions/` (G)

### 4.5 Information Domain

**Groups**: I (Information & Surprise, 7D)
**Total**: 7D
**Scope**: Information-theoretic features -- melodic/harmonic/rhythmic entropy, spectral surprise, mutual information, predictive entropy, tonal ambiguity. Based on predictive coding and information theory frameworks.
**Code path**: `mi_beta/ear/r3/extensions/` (new group)

### 4.6 CrossDomain

**Groups**: E (Interactions, 24D)
**Total**: 24D
**Scope**: Cross-group interaction products capturing simultaneous perceptual events (e.g., energy-consonance coupling, change-consonance coupling).
**Code path**: `mi_beta/ear/r3/cross_domain/`

---

## 5. Input Contract

| Property | Value |
|----------|-------|
| **Tensor shape** | `(B, 128, T)` |
| **B** | Batch size (variable) |
| **128** | Number of mel bins (n_mels) |
| **T** | Number of time frames (variable) |
| **Frame rate** | 172.27 Hz (hop_length = 256 @ sr = 44100) |
| **Sample rate** | 44,100 Hz |
| **Frequency range** | fmin = 0 Hz, fmax = sr/2 = 22,050 Hz |
| **Value domain** | log-mel spectrogram (log1p normalized) |
| **Data type** | `torch.float32` |
| **Device** | CPU or CUDA (groups must be device-agnostic) |

The mel spectrogram is produced by the Cochlea module upstream. All R3 groups receive the same mel tensor as input. Groups that require inter-group dependencies (Stages 2 and 3) receive additional inputs via the dependency injection mechanism.

---

## 6. Output Contract

| Property | Value |
|----------|-------|
| **Tensor shape** | `(B, T, 128)` |
| **Value range** | `[0, 1]` for all dimensions |
| **Data type** | `torch.float32` |
| **Feature ordering** | Contiguous by group: `[A|B|C|D|E|F|G|H|I|J|K]` |
| **Wrapper type** | `R3Output(features=Tensor, feature_names=Tuple[str, ...])` |

**Normalization guarantees**:
- All features are normalized to `[0, 1]` range
- Normalization methods vary by feature: min-max, sigmoid, ratio, complement, L1-norm
- Tonnetz features are naturally `[-1, 1]` and mapped to `[0, 1]` via `(x + 1) / 2`
- MFCC features are per-coefficient scaled from empirical ranges to `[0, 1]`

**Dimension guarantee**: The output dimension is determined by `R3FeatureRegistry.freeze().total_dim`. In v2, this equals 128. The `R3Extractor.total_dim` property provides runtime access.

---

## 7. Auto-Discovery Mechanism

R3 groups are auto-discovered at initialization time via Python's `importlib` system:

```
R3Extractor.__init__()
  |
  +-- _discover_groups()
  |     |
  |     +-- Scan subdirectories in order:
  |     |     1. psychoacoustic/   (A: Consonance)
  |     |     2. dsp/              (B: Energy, C: Timbre, D: Change)
  |     |     3. cross_domain/     (E: Interactions)
  |     |     4. extensions/       (F, G, H, I, J, K -- new groups)
  |     |
  |     +-- For each subdirectory:
  |           import __init__.py
  |           collect classes listed in __all__
  |           filter: issubclass(cls, BaseSpectralGroup) and cls is not BaseSpectralGroup
  |           instantiate: cls()
  |
  +-- R3FeatureRegistry.register(group) for each discovered group
  |
  +-- R3FeatureRegistry.freeze()
        |
        +-- Assign contiguous INDEX_RANGE to each group
        +-- Return R3FeatureMap(total_dim, groups)
```

**Key implementation** (from `mi_beta/ear/r3/__init__.py`):

```python
_SUBDIRECTORY_NAMES = ("psychoacoustic", "dsp", "cross_domain", "extensions")

def _discover_groups() -> List[BaseSpectralGroup]:
    groups = []
    for subdir in _SUBDIRECTORY_NAMES:
        mod = importlib.import_module(f".{subdir}", package=__name__)
        for attr_name in getattr(mod, "__all__", []):
            cls = getattr(mod, attr_name, None)
            if isinstance(cls, type) and issubclass(cls, BaseSpectralGroup):
                groups.append(cls())
    return groups
```

**Registration** (from `mi_beta/ear/r3/_registry.py`):

The `R3FeatureRegistry` collects groups, checks for duplicate `GROUP_NAME` values, and at `freeze()` time assigns contiguous index ranges. Once frozen, no further groups can be registered. The frozen `R3FeatureMap` is an immutable dataclass providing `total_dim` and per-group metadata (`R3GroupInfo`: name, dim, start, end, feature_names).

---

## 8. Extension Model

New spectral groups are added via the `extensions/` directory following the template pattern:

1. **Copy** `mi_beta/ear/r3/extensions/_template.py` to a new file
2. **Implement** `GROUP_NAME`, `OUTPUT_DIM`, `feature_names`, `compute()`
3. **Export** from `extensions/__init__.py` via `__all__`
4. **Done** -- the registry auto-discovers and assigns index ranges

**BaseSpectralGroup contract** (from `mi_beta/contracts/base_spectral_group.py`):

| Attribute | Type | Description |
|-----------|------|-------------|
| `GROUP_NAME` | `str` | Unique canonical name (e.g., `"pitch_chroma"`) |
| `DOMAIN` | `str` | Perceptual domain (e.g., `"tonal"`) |
| `OUTPUT_DIM` | `int` | Number of features produced |
| `INDEX_RANGE` | `Tuple[int, int]` | Auto-assigned `[start, end)` in the R3 vector |
| `feature_names` | `List[str]` | Ordered list of feature names (length == OUTPUT_DIM) |
| `compute(mel)` | `Tensor -> Tensor` | `(B, 128, T) -> (B, T, OUTPUT_DIM)` |

See [EXTENSION-GUIDE.md](EXTENSION-GUIDE.md) for detailed walkthrough.

---

## 9. Dependency Graph

### 9.1 Stage-Level DAG

```
                    +-------------------------------+
                    |      mel (B, 128, T)          |
                    +--+--+--+--+--+--+-------------+
                       |  |  |  |  |  |
  Stage 1 (parallel):  v  v  v  v  v  v  v
                      [A][B][C][D][F][J][K]
                       |  |  |  |  |  |  |
                       |  |  |  |  |  |  |
  Stage 2 (parallel):  |  |  |  |  |  |  |
                       +--+--+--+  |  |  |
                          |        |  |  |
                          v     +--+  |  |
                         [E]    |     |  |
                         (A,B,  v     |  |
                          C,D) [G]    |  |
                               (B[11])|  |
                                   +--+  |
                                   v     |
                                  [H]    |
                                  (F     |
                                 chroma) |
                                   |     |
  Stage 3:                         |     |
                          +--------+     |
                          v        v     |
                         [I]             |
                         (F chroma,      |
                          G onset,       |
                          H key)         |
                                         |
  Concat:     torch.cat([A,B,C,D,E,F,G,H,I,J,K], dim=-1) -> (B, T, 128)
```

### 9.2 Stage Execution Summary

| Stage | Groups | Dependencies | Max Latency | Parallel Streams |
|:-----:|--------|-------------|:-----------:|:----------------:|
| 1 | A, B, C, D, F, J, K | mel only | ~3.0 ms* | 7 |
| 2 | E, G, H | A-D, B[11], F chroma | ~1.0 ms | 3 |
| 3 | I | F chroma, G onset, H key, mel | ~0.8 ms | 1 |
| Concat | all | all stages | <0.1 ms | 1 |
| **Total** | | | **~4.5 ms** | |

*K group amortized: full FFT every 86 frames; average K cost ~0.5 ms/frame.
**Amortized total: ~2.5 ms/frame** with 2.3x real-time headroom (5.8 ms budget).

### 9.3 Feature-Level Dependencies

```
mel --+-- A[0:7]   ----------------------------------------> E[25:49]
      +-- B[7:12] --+-- B[11] onset_strength --> G[65:75] --> I[89]
      |              +-------------------------> E[25:49]
      +-- C[12:21] -----------------------------> E[25:49]
      +-- D[21:25] -----------------------------> E[25:49]
      +-- F[49:65] --+-- chroma[49:61] --+--> H[75:87] ----> I[87,88,93]
      |              |                    +--> I[87,88]
      |              +-- pitch_height[61]
      |              +-- PC_entropy[62]
      |              +-- pitch_salience[63]
      |              +-- inharmonicity[64]
      +-- J[94:114]    (independent)
      +-- K[114:128] -- mod_4Hz[117] --> fluctuation[123]
```

---

## 10. Code Structure Mapping

Documentation and code maintain a 1:1 correspondence:

| Documentation | Code Path | Purpose |
|--------------|-----------|---------|
| `Docs/R3/00-INDEX.md` | `mi_beta/ear/r3/__init__.py` | Master index / R3Extractor |
| `Docs/R3/R3-SPECTRAL-ARCHITECTURE.md` | `mi_beta/ear/r3/__init__.py` | Architecture spec |
| `Docs/R3/Registry/FeatureCatalog.md` | `mi_beta/ear/r3/_registry.py` | Feature registry |
| `Docs/R3/Registry/DimensionMap.md` | `mi_beta/core/dimension_map.py` | Dimension mapping |
| `Docs/R3/EXTENSION-GUIDE.md` | `mi_beta/ear/r3/extensions/_template.py` | Extension template |
| `Docs/R3/Contracts/` | `mi_beta/contracts/base_spectral_group.py` | Contract spec |
| `Docs/R3/Domains/Psychoacoustic/` | `mi_beta/ear/r3/psychoacoustic/` | Group A code |
| `Docs/R3/Domains/Spectral/` | `mi_beta/ear/r3/dsp/` | Groups B, C code |
| `Docs/R3/Domains/CrossDomain/` | `mi_beta/ear/r3/cross_domain/` | Group E code |
| `Docs/R3/Domains/{Tonal,Temporal,Information}/` | `mi_beta/ear/r3/extensions/` | Groups F-K code |

---

## 11. Real-Time Feasibility

**Frame budget**: 5.8 ms (172.27 Hz frame rate)

| Component | Dim | Tier | Estimated Cost |
|-----------|:---:|:----:|:--------------|
| A-E (existing) | 49D | 0-1 | ~0.5 ms/frame |
| F: Pitch & Chroma | 16D | 1 | ~1.0 ms/frame |
| G: Rhythm & Groove | 10D | 2 | ~0.5 ms/frame |
| H: Harmony & Tonality | 12D | 2 | ~1.0 ms/frame |
| I: Information & Surprise | 7D | 2 | ~0.5 ms/frame |
| J: Timbre Extended | 20D | 0-1 | ~0.5 ms/frame |
| K: Modulation & Psychoacoustic | 14D | 2-3 | ~3.0 ms/frame |
| **Sequential total** | **128D** | | **~7.0 ms** |
| **Parallel (3-stage)** | | | **~3-4 ms** |

K group modulation uses a sliding window (hop=86 frames). Real GPU batch parallelism brings effective latency to ~2.5 ms/frame with **2.3x RT headroom**.

---

## 12. Warm-up Behavior

Some features require a minimum number of frames before producing reliable output:

| Feature/Group | Warm-up Duration | Behavior During Warm-up |
|--------------|:----------------:|------------------------|
| K modulation [114:121] | 344 frames (2.0s) | Zero output |
| I entropy [87, 88, 92] | 344 frames (2.0s) | Linear confidence ramp: `min(1.0, t/344)` |
| I spectral_surprise [90] | 344 frames (2.0s) | Running average convergence |
| G tempo [65:67] | 344 frames (2.0s) | Autocorrelation window fill |
| G syncopation [68] | 688 frames (4.0s) | Tempo + metrical grid stabilization |
| All other features | 0 (immediate) | Frame-level computation, no warm-up |

**Warm-up strategy**: During the first 344 frames (~2.0 seconds), warm-up-dependent features gradually become reliable. C3 models handle this transition period through their BEP/ASA temporal mechanisms.

---

## References

- R3-V2-DESIGN.md -- Definitive v2 architecture design (Phase 3B)
- R3-CROSSREF.md -- Three-perspective synthesis (R1+R2+R3)
- Krumhansl, C. L. (1990). Cognitive Foundations of Musical Pitch
- Plomp, R., & Levelt, W. J. M. (1965). Tonal Consonance and Critical Bandwidth
- Shepard, R. N. (1964). Circularity in Judgments of Relative Pitch
- Witek, M. A. G., et al. (2014). Syncopation, Body-Movement and Pleasure in Groove Music
- Chi, T., & Shamma, S. A. (2005). Multiresolution Spectrotemporal Analysis
- Zwicker, E., & Fastl, H. (1999). Psychoacoustics: Facts and Models
- Pearce, M. T. (2005). The Construction and Evaluation of Statistical Models of Melodic Structure
