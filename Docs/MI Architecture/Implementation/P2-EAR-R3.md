# Phase 2: Ear -- R3 Spectral Feature Extraction (128D)

**Phase**: P2-R3
**Depends on**: P1 (Contracts -- `BaseSpectralGroup`, `R3FeatureSpec`)
**Output**: ~62 Python files in `Musical_Intelligence/ear/r3/`
**Gate**: G2 -- `R3Extractor` produces `(B, T, 128)` tensor, all features in `[0,1]`

---

## Overview

R3 extracts 128 spectral features from mel spectrograms via 11 groups (A-K), 6 domains, and a 3-stage DAG:

| Stage | Groups | Dependencies | Parallel |
|:-----:|--------|-------------|:--------:|
| 1 | A, B, C, D, F, J, K | mel only | 7 |
| 2 | E, G, H | E: A,B,C,D; G: B[11]; H: F[49:61] | 3 |
| 3 | I | F chroma, G onset, H key | 1 |

Implementation order: constants -> registry -> pipeline -> groups -> extractor.

---

## P2.1 -- Constants

### `ear/r3/constants/__init__.py`

**Purpose**: Re-export all R3 constants.
**Exports**: All symbols from sub-modules below.

---

### `ear/r3/constants/feature_names.py`

**Purpose**: All 128 feature name constants as a single ordered tuple.

**Primary Docs**:
- `Docs/R³/Registry/FeatureCatalog.md` -- all 128 names in index order
- `Docs/R³/Registry/DimensionMap.md` -- Section 1: index-to-name mapping

**Related Docs**: `Docs/R³/Registry/NamingConventions.md`

**Depends On**: Nothing.

**Exports**: `R3_FEATURE_NAMES` (Tuple[str, ...], len=128), `R3_DIM` (int=128)

**Key Constraints**:
- Exactly 128 snake_case strings, all unique
- Positions match FeatureCatalog (idx 0="roughness", 48="x_l5l7_7", 49="chroma_C", 127="spectral_slope_0_500")

**Verification**: [ ] 128 entries, [ ] spot-check indices 0/48/49/127, [ ] no duplicates

---

### `ear/r3/constants/group_boundaries.py`

**Purpose**: 11 group boundaries (letter, name, start, end, dim, stage).

**Primary Docs**:
- `Docs/R³/Registry/DimensionMap.md` -- Section 2: Group Boundary Table
- `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md` -- Section 3: stage assignments

**Depends On**: Nothing.

**Exports**: `R3GroupBoundary` (NamedTuple), `R3_GROUP_BOUNDARIES` (Tuple, len=11), slice constants (`R3_CONSONANCE=(0,7)`, etc.)

**Key Constraints**:
- Contiguous, no gaps/overlaps, dims sum to 128
- Stages: 1={A,B,C,D,F,J,K}, 2={E,G,H}, 3={I}
- A=(0,7) B=(7,12) C=(12,21) D=(21,25) E=(25,49) F=(49,65) G=(65,75) H=(75,87) I=(87,94) J=(94,114) K=(114,128)

**Verification**: [ ] 11 entries sum=128, [ ] stages correct, [ ] contiguous

---

### `ear/r3/constants/quality_tiers.py`

**Purpose**: Per-feature P/A/S/R tier assignments.

**Primary Docs**:
- `Docs/R³/Registry/FeatureCatalog.md` -- Tier column
- `Docs/R³/Standards/QualityTiers.md` -- tier definitions

**Depends On**: `feature_names.py`.

**Exports**: `QualityTier` (Enum), `R3_QUALITY_TIERS` (Dict[str, QualityTier])

**Key Constraints**: P=36, A=49, S=42, R=1 (total=128). Only sharpness_zwicker[122]=R.

**Verification**: [ ] 128 entries, [ ] tier counts match, [ ] idx 122=R

---

### `ear/r3/constants/domain_map.py`

**Purpose**: 6 perceptual domains mapped to groups.

**Primary Docs**:
- `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md` -- Section 4: Domain Taxonomy
- `Docs/R³/Registry/DimensionMap.md` -- Section 3: Domain Boundary Table

**Depends On**: `group_boundaries.py`.

**Exports**: `R3Domain` (Enum: PSYCHOACOUSTIC, SPECTRAL, TONAL, TEMPORAL, INFORMATION, CROSS_DOMAIN), `R3_DOMAIN_MAP`

**Key Constraints**: Psychoacoustic={A,K}(21D), Spectral={B,C,J}(34D), Tonal={F,H}(28D), Temporal={D,G}(14D), Information={I}(7D), CrossDomain={E}(24D). Domains NOT contiguous in index space.

**Verification**: [ ] 6 domains, 11 groups covered, [ ] dims sum to 128

---

## P2.1 -- Registry

### `ear/r3/registry/__init__.py`

**Purpose**: Re-export `R3FeatureRegistry`, `R3FeatureMap`, `auto_discover_groups`.

---

### `ear/r3/registry/feature_registry.py`

**Purpose**: Mutable registry that collects groups, then freezes into immutable R3FeatureMap.

**Primary Docs**:
- `Docs/R³/Contracts/R3FeatureRegistry.md` -- register(), freeze(), validation
- `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md` -- Section 7: registration flow

**Related Docs**: `Docs/R³/Contracts/BaseSpectralGroup.md`, `Docs/R³/Contracts/R3FeatureSpec.md`

**Depends On**: `contracts/bases/base_spectral_group.py`, `contracts/dataclasses/feature_spec.py`, `ear/r3/registry/feature_map.py`

**Exports**: `R3FeatureRegistry`

**Key Constraints**:
- `register(group)` rejects duplicate GROUP_NAME or post-freeze calls
- `freeze() -> R3FeatureMap` assigns contiguous INDEX_RANGE per group
- Creates R3FeatureSpec instances during freeze
- Double freeze() is idempotent

**Verification**: [ ] duplicate rejected, [ ] freeze assigns contiguous indices, [ ] post-freeze register raises

---

### `ear/r3/registry/feature_map.py`

**Purpose**: Frozen immutable snapshot -- read-only group/feature metadata.

**Primary Docs**: `Docs/R³/Contracts/R3FeatureRegistry.md` -- R3FeatureMap/R3GroupInfo sections

**Depends On**: `contracts/dataclasses/feature_spec.py`

**Exports**: `R3FeatureMap` (frozen), `R3GroupInfo` (frozen)

**Key Constraints**:
- R3FeatureMap: `total_dim`, `groups` (Tuple[R3GroupInfo,...]), `feature_specs`, `get_group(name)`, `get_feature(index)`
- R3GroupInfo: `name`, `dim`, `start`, `end`, `feature_names`

**Verification**: [ ] frozen, [ ] get_group/get_feature work, [ ] total_dim=128

---

### `ear/r3/registry/auto_discovery.py`

**Purpose**: Auto-discover BaseSpectralGroup subclasses from group subdirectories.

**Primary Docs**:
- `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md` -- Section 7: discovery algorithm
- `Docs/R³/Contracts/ExtensionProtocol.md`

**Depends On**: `contracts/bases/base_spectral_group.py`, all `ear/r3/groups/*/` directories

**Exports**: `auto_discover_groups() -> List[BaseSpectralGroup]`

**Key Constraints**: Scans a_consonance through k_modulation in order. Filters `issubclass(cls, BaseSpectralGroup) and cls is not BaseSpectralGroup`. Returns 11 instances for v2.

**Verification**: [ ] discovers 11 groups in A-K order, [ ] no BaseSpectralGroup in results

---

## P2.2 -- Pipeline

### `ear/r3/pipeline/__init__.py`

**Purpose**: Re-export `DependencyDAG`, `StageExecutor`, `FeatureNormalizer`, `WarmupManager`.

---

### `ear/r3/pipeline/dag.py`

**Purpose**: 3-stage dependency DAG for group execution ordering.

**Primary Docs**:
- `Docs/R³/Pipeline/DependencyDAG.md` -- DAG spec, stages, edges
- `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md` -- Section 9: Dependency Graph

**Related Docs**: `Docs/R³/Pipeline/Performance.md`, `Docs/R³/Pipeline/StateManagement.md`

**Depends On**: `ear/r3/constants/group_boundaries.py`, `contracts/bases/base_spectral_group.py`

**Exports**: `DependencyDAG`

**Key Constraints**:
- Stage 1: {A,B,C,D,F,J,K} -- mel only
- Stage 2: E deps={A,B,C,D}, G deps={B}, H deps={F}
- Stage 3: I deps={F,G,H}
- `validate()` checks no cycles, all deps satisfied
- `get_stage(n)`, `get_dependencies(group_name)`

**Verification**: [ ] 7+3+1 groups, [ ] dependency edges correct, [ ] validate passes/rejects

---

### `ear/r3/pipeline/stage_executor.py`

**Purpose**: Executes the 3-stage DAG with parallel groups per stage.

**Primary Docs**:
- `Docs/R³/Pipeline/DependencyDAG.md` -- execution semantics
- `Docs/R³/Pipeline/Performance.md` -- GPU stream strategy

**Related Docs**: `Docs/R³/Pipeline/StateManagement.md`, `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md` Section 11

**Depends On**: `ear/r3/pipeline/dag.py`, `contracts/bases/base_spectral_group.py`

**Exports**: `StageExecutor`

**Key Constraints**:
- `execute(mel, groups, dag) -> Dict[str, Tensor]`
- Stage 1: `group.compute(mel)`, Stage 2-3: `group.compute_with_deps(mel, deps)`
- Target: < 5.8 ms/frame total

**Verification**: [ ] correct dispatch (compute vs compute_with_deps), [ ] output shapes, [ ] DAG order

---

### `ear/r3/pipeline/normalization.py`

**Purpose**: Per-feature [0,1] normalization.

**Primary Docs**:
- `Docs/R³/Pipeline/Normalization.md` -- methods per feature
- `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md` -- Section 6: Output Contract

**Related Docs**: `Docs/R³/Registry/FeatureCatalog.md`, `Docs/R³/Standards/QualityTiers.md`

**Depends On**: `ear/r3/constants/feature_names.py`, `ear/r3/constants/group_boundaries.py`

**Exports**: `FeatureNormalizer`

**Key Constraints**:
- Methods: min-max, sigmoid (derivatives), ratio (chroma), complement (1-x), affine (tonnetz [-1,1]->[0,1] via (x+1)/2), per-coefficient (MFCC)
- Safety clamp to [0,1] after normalization

**Verification**: [ ] all 128 in [0,1], [ ] tonnetz affine, [ ] MFCC scaling, [ ] clamp

---

### `ear/r3/pipeline/warmup.py`

**Purpose**: 344-frame warm-up management for temporal features.

**Primary Docs**:
- `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md` -- Section 12: Warm-up table
- `Docs/R³/Pipeline/StateManagement.md` -- confidence ramp

**Depends On**: `ear/r3/constants/group_boundaries.py`

**Exports**: `WarmupManager`

**Key Constraints**:
- 344 frames (2.0s): K modulation[114:121] (zero output), I entropy[87,88,92] (ramp `min(1.0,t/344)`), I[90] (running avg), G tempo[65:67] (window fill)
- 688 frames (4.0s): G syncopation[68]
- `is_warmed_up(frame_count)`, `get_confidence(frame_count, feature_index)`

**Verification**: [ ] 344/688 thresholds, [ ] ramp formula, [ ] K zeros before warmup

---

## P2.2 -- Groups (A through K)

Each group directory has: `__init__.py` + `group.py` (BaseSpectralGroup subclass) + feature sub-modules. All `group.py` files share these common docs:
- **Contract**: `Docs/R³/Contracts/BaseSpectralGroup.md`
- **Catalog**: `Docs/R³/Registry/FeatureCatalog.md` (for that group's index range)
- **Depends On**: `contracts/bases/base_spectral_group.py` + own sub-modules

Below, "Domain Doc" is the primary source for formulas and citations. "Cat range" indicates which FeatureCatalog entries to extract.

---

### Group A: Consonance [0:7], 7D, Stage 1, Psychoacoustic

**Domain Doc**: `Docs/R³/Domains/Psychoacoustic/A-Consonance.md`
**Cat range**: indices 0-6, all tier P

#### `ear/r3/groups/a_consonance/group.py`
**Exports**: `ConsonanceGroup`
**Constants**: GROUP_NAME="consonance", DOMAIN="psychoacoustic", OUTPUT_DIM=7, INDEX_RANGE=(0,7), STAGE=1, DEPENDENCIES=()
**Features**: roughness, sethares_dissonance, helmholtz_kang, stumpf_fusion, sensory_pleasantness, inharmonicity, harmonic_deviation

#### `ear/r3/groups/a_consonance/roughness.py`
**Exports**: `compute_roughness` (idx 0: Plomp-Levelt proxy, sigmoid(var/mean)), `compute_sethares_dissonance` (idx 1: mean(abs(diff)))

#### `ear/r3/groups/a_consonance/harmonicity.py`
**Exports**: `compute_helmholtz_kang` (idx 2: lag-1 autocorrelation), `compute_stumpf_fusion` (idx 3: mel[:N/4].sum()/total, identical to warmth[12])

#### `ear/r3/groups/a_consonance/dissonance.py`
**Exports**: `compute_sensory_pleasantness` (idx 4: Harrison & Pearce 2020), `compute_inharmonicity` (idx 5: 1-[2]), `compute_harmonic_deviation` (idx 6: 0.5*[1]+0.5*(1-[2]))

**Verification**: [ ] 7 features, [ ] STAGE=1, [ ] compute(mel) signature

---

### Group B: Energy [7:12], 5D, Stage 1, Spectral

**Domain Doc**: `Docs/R³/Domains/Temporal/B-Energy.md`
**Cat range**: indices 7-11
**Related**: `Docs/R³/Pipeline/Normalization.md` (sigmoid for velocity/acceleration)

#### `ear/r3/groups/b_energy/group.py`
**Exports**: `EnergyGroup`
**Constants**: GROUP_NAME="energy", DOMAIN="spectral", OUTPUT_DIM=5, INDEX_RANGE=(7,12), STAGE=1, DEPENDENCIES=()
**Features**: amplitude, velocity_A, acceleration_A, loudness, onset_strength
**Note**: onset_strength[11] is critical dependency for Stage 2 group G

#### `ear/r3/groups/b_energy/amplitude.py`
**Exports**: `compute_amplitude` (idx 7: RMS, tier P), `compute_loudness` (idx 10: Stevens' (RMS)^0.3, tier P), `compute_onset_strength` (idx 11: HWR spectral flux, tier S)

#### `ear/r3/groups/b_energy/dynamics.py`
**Exports**: `compute_velocity` (idx 8: 1st deriv, sigmoid, tier S), `compute_acceleration` (idx 9: 2nd deriv, sigmoid, tier S)

**Verification**: [ ] 5 features, [ ] onset_strength accessible downstream

---

### Group C: Timbre [12:21], 9D, Stage 1, Spectral

**Domain Doc**: `Docs/R³/Domains/Spectral/C-Timbre.md`
**Cat range**: indices 12-20

#### `ear/r3/groups/c_timbre/group.py`
**Exports**: `TimbreGroup`
**Constants**: GROUP_NAME="timbre", DOMAIN="spectral", OUTPUT_DIM=9, INDEX_RANGE=(12,21), STAGE=1, DEPENDENCIES=()
**Known duplications**: [12]==[3], [16]==1-[1], [17]==[2]. Effective independent dims ~4.

#### `ear/r3/groups/c_timbre/texture.py`
**Exports**: `compute_warmth`(12), `compute_sharpness`(13), `compute_tonalness`(14), `compute_clarity`(15), `compute_spectral_smoothness`(16), `compute_spectral_autocorrelation`(17)

#### `ear/r3/groups/c_timbre/tristimulus.py`
**Exports**: `compute_tristimulus` -> (18,19,20). Pollard-Jansson mel proxy, tier A. Must sum ~1.0.

#### `ear/r3/groups/c_timbre/spectral.py`
**Exports**: Shared spectral utilities for texture and tristimulus.

**Verification**: [ ] 9 features, [ ] duplication notes in docstrings

---

### Group D: Change [21:25], 4D, Stage 1, Temporal

**Domain Doc**: `Docs/R³/Domains/Spectral/D-Change.md`
**Cat range**: indices 21-24

#### `ear/r3/groups/d_change/group.py`
**Exports**: `ChangeGroup`
**Constants**: GROUP_NAME="change", DOMAIN="temporal", OUTPUT_DIM=4, INDEX_RANGE=(21,25), STAGE=1, DEPENDENCIES=()

#### `ear/r3/groups/d_change/features.py`
**Exports**: `compute_spectral_flux`(21, L2, tier S), `compute_distribution_entropy`(22, Shannon, tier S), `compute_distribution_flatness`(23, Wiener, tier S), `compute_distribution_concentration`(24, HHI, tier P, **known normalization bug** deferred to Phase 6)

**Verification**: [ ] 4 features, [ ] bug in [24] documented in comments

---

### Group E: Interactions [25:49], 24D, Stage 2, CrossDomain

**Domain Doc**: `Docs/R³/Domains/CrossDomain/E-Interactions.md`
**Cat range**: indices 25-48, all tier P
**Related**: `Docs/R³/Pipeline/DependencyDAG.md` (E deps: A,B,C,D)

#### `ear/r3/groups/e_interactions/group.py`
**Exports**: `InteractionsGroup`
**Constants**: GROUP_NAME="interactions", DOMAIN="cross_domain", OUTPUT_DIM=24, INDEX_RANGE=(25,49), STAGE=2, DEPENDENCIES=("consonance","energy","timbre","change")
**Note**: Uses `compute_with_deps(mel, deps)`. Currently proxy re-computation (Phase 6 fix).

#### `ear/r3/groups/e_interactions/energy_consonance.py`
**Exports**: `compute_energy_consonance_interactions` -- x_l0l5[25:33], 8D

#### `ear/r3/groups/e_interactions/change_consonance.py`
**Exports**: `compute_change_consonance_interactions` -- x_l4l5[33:41], 8D

#### `ear/r3/groups/e_interactions/consonance_timbre.py`
**Exports**: `compute_consonance_timbre_interactions` -- x_l5l7[41:49], 8D

**Verification**: [ ] 24D = 3x8, [ ] STAGE=2, [ ] compute_with_deps(), [ ] proxy note

---

### Group F: Pitch & Chroma [49:65], 16D, Stage 1, Tonal

**Domain Doc**: `Docs/R³/Domains/Tonal/F-PitchChroma.md`
**Cat range**: indices 49-64
**Related**: `Docs/R³/Pipeline/DependencyDAG.md` (F chroma feeds H, I)

#### `ear/r3/groups/f_pitch_chroma/group.py`
**Exports**: `PitchChromaGroup`
**Constants**: GROUP_NAME="pitch_chroma", DOMAIN="tonal", OUTPUT_DIM=16, INDEX_RANGE=(49,65), STAGE=1, DEPENDENCIES=()
**Note**: Chroma[49:61] is critical downstream input for H and I.

#### `ear/r3/groups/f_pitch_chroma/chroma.py`
**Exports**: `compute_chroma`, `build_chroma_matrix`
- 12 pitch classes (C,Db,D,...,B) via Gaussian soft-assignment matrix (128x12), L1 norm. Tier A.

#### `ear/r3/groups/f_pitch_chroma/pitch.py`
**Exports**: `compute_pitch_height`(61, Weber-Fechner, S), `compute_pitch_class_entropy`(62, Shannon, S), `compute_pitch_salience`(63, Parncutt proxy, A), `compute_inharmonicity_index`(64, A)

**Verification**: [ ] 16 features, [ ] chroma L1-normalized, [ ] chroma (B,T,12) for downstream

---

### Group G: Rhythm & Groove [65:75], 10D, Stage 2, Temporal

**Domain Doc**: `Docs/R³/Domains/Temporal/G-RhythmGroove.md`
**Cat range**: indices 65-74
**Related**: `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md` Section 12 (warm-up)

#### `ear/r3/groups/g_rhythm_groove/group.py`
**Exports**: `RhythmGrooveGroup`
**Constants**: GROUP_NAME="rhythm_groove", DOMAIN="temporal", OUTPUT_DIM=10, INDEX_RANGE=(65,75), STAGE=2, DEPENDENCIES=("energy",)
**Note**: Needs B[11] onset_strength (offset 4 within B output). Warm-up: tempo[65:67]=344fr, syncopation[68]=688fr.

#### `ear/r3/groups/g_rhythm_groove/tempo.py`
**Exports**: `compute_tempo_estimate`(65, Fraisse, A, 344fr), `compute_beat_strength`(66, A, 344fr), `compute_pulse_clarity`(67, Witek, A), `compute_syncopation_index`(68, LHL, A, 688fr), `compute_metricality_index`(69, Grahn, A)

#### `ear/r3/groups/g_rhythm_groove/groove.py`
**Exports**: `compute_isochrony_nPVI`(70, S), `compute_groove_index`(71, Madison, A), `compute_event_density`(72, S), `compute_tempo_stability`(73, S), `compute_rhythmic_regularity`(74, S)

**Verification**: [ ] 10 features, [ ] STAGE=2 deps=("energy",), [ ] warm-up documented, [ ] B[11] extraction correct

---

### Group H: Harmony & Tonality [75:87], 12D, Stage 2, Tonal

**Domain Doc**: `Docs/R³/Domains/Tonal/H-HarmonyTonality.md`
**Cat range**: indices 75-86
**Related**: `Docs/R³/Pipeline/DependencyDAG.md` (H deps: F chroma)

#### `ear/r3/groups/h_harmony/group.py`
**Exports**: `HarmonyGroup`
**Constants**: GROUP_NAME="harmony", DOMAIN="tonal", OUTPUT_DIM=12, INDEX_RANGE=(75,87), STAGE=2, DEPENDENCIES=("pitch_chroma",)
**Note**: Extracts first 12 of 16 F-output dims as chroma input.

#### `ear/r3/groups/h_harmony/key_detection.py`
**Exports**: `compute_key_clarity`(75, Krumhansl-Kessler 24 profiles, A), `get_krumhansl_kessler_profiles`

#### `ear/r3/groups/h_harmony/tonnetz.py`
**Exports**: `compute_tonnetz`(76-81, Harte 2006, S, raw [-1,1] -> [0,1] via (x+1)/2), `compute_voice_leading_distance`(82, Tymoczko, S), `compute_harmonic_change`(83, HCDF cosine, S)

#### `ear/r3/groups/h_harmony/syntax.py`
**Exports**: `compute_tonal_stability`(84, composite, A), `compute_diatonicity`(85, Tymoczko, A), `compute_syntactic_irregularity`(86, Lerdahl, A)

**Verification**: [ ] 12 features, [ ] STAGE=2 deps=("pitch_chroma",), [ ] tonnetz affine normalization

---

### Group I: Information & Surprise [87:94], 7D, Stage 3, Information

**Domain Doc**: `Docs/R³/Domains/Information/I-InformationSurprise.md`
**Cat range**: indices 87-93
**Related**: `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md` Section 12 (344fr warm-up, confidence ramp)

#### `ear/r3/groups/i_information/group.py`
**Exports**: `InformationGroup`
**Constants**: GROUP_NAME="information", DOMAIN="information", OUTPUT_DIM=7, INDEX_RANGE=(87,94), STAGE=3, DEPENDENCIES=("pitch_chroma","rhythm_groove","harmony")
**Note**: EMA running stats tau=2.0s. Warm-up 344fr for entropy features [87,88,92].

#### `ear/r3/groups/i_information/entropy.py`
**Exports**: `compute_melodic_entropy`(87, IDyOM approx, A, 344fr), `compute_harmonic_entropy`(88, chroma KL, A, 344fr), `compute_information_rate`(91, mutual info, S), `compute_predictive_entropy`(92, predictive coding, A, 344fr), `compute_tonal_ambiguity`(93, key entropy, A)

#### `ear/r3/groups/i_information/surprise.py`
**Exports**: `compute_rhythmic_information_content`(89, Spiech IC, A), `compute_spectral_surprise`(90, Friston free energy, A, 344fr running avg)

**Verification**: [ ] 7 features, [ ] STAGE=3 deps include F,G,H, [ ] warm-up ramp, [ ] EMA tau=2.0s

---

### Group J: Timbre Extended [94:114], 20D, Stage 1, Spectral

**Domain Doc**: `Docs/R³/Domains/Spectral/J-TimbreExtended.md`
**Cat range**: indices 94-113, all tier S

#### `ear/r3/groups/j_timbre_extended/group.py`
**Exports**: `TimbreExtendedGroup`
**Constants**: GROUP_NAME="timbre_extended", DOMAIN="spectral", OUTPUT_DIM=20, INDEX_RANGE=(94,114), STAGE=1, DEPENDENCIES=()

#### `ear/r3/groups/j_timbre_extended/mfcc.py`
**Exports**: `compute_mfcc`, `build_dct_matrix`
- 13 coefficients (c1-c13, no c0). DCT matrix (128,13). Per-coefficient empirical scaling.

#### `ear/r3/groups/j_timbre_extended/spectral_contrast.py`
**Exports**: `compute_spectral_contrast`
- 7 octave sub-bands (6+1 residual). Peak=top 20% mean, valley=bottom 20%. Log-domain contrast -> [0,1].

**Verification**: [ ] 20D = 13 MFCC + 7 contrast, [ ] STAGE=1

---

### Group K: Modulation & Psychoacoustic [114:128], 14D, Stage 1, Psychoacoustic

**Domain Doc**: `Docs/R³/Domains/Psychoacoustic/K-ModulationPerception.md`
**Cat range**: indices 114-127
**Related**: `Docs/R³/Pipeline/Performance.md` (sliding window FFT)

#### `ear/r3/groups/k_modulation/group.py`
**Exports**: `ModulationGroup`
**Constants**: GROUP_NAME="modulation", DOMAIN="psychoacoustic", OUTPUT_DIM=14, INDEX_RANGE=(114,128), STAGE=1, DEPENDENCIES=()
**Note**: Sliding-window FFT: window=344, hop=86, fft_size=512. Warm-up 344fr (zero output for [114:121]). Internal dep: mod_4Hz[117] -> fluctuation[123].

#### `ear/r3/groups/k_modulation/modulation_spectrum.py`
**Exports**: `compute_modulation_spectrum`, `compute_modulation_centroid`(120,S), `compute_modulation_bandwidth`(121,S)
- 6 bands at 0.5,1,2,4,8,16 Hz (indices 114-119, tier A)

#### `ear/r3/groups/k_modulation/psychoacoustic.py`
**Exports**: `compute_sharpness_zwicker`(122, DIN 45692, **tier R** -- only Reference feature), `compute_fluctuation_strength`(123, ~4Hz, A), `compute_loudness_a_weighted`(124, ISO 226, S), `compute_alpha_ratio`(125, eGeMAPS, S), `compute_hammarberg_index`(126, eGeMAPS, S), `compute_spectral_slope_0_500`(127, eGeMAPS, S)

**Verification**: [ ] 14 features, [ ] FFT params, [ ] warm-up zeros, [ ] idx 122 = tier R

---

## P2.3 -- R3 Extractor

### `ear/r3/extractor.py`

**Purpose**: Top-level orchestrator -- discovers groups, builds registry, executes 3-stage DAG, produces (B,T,128).

**Primary Docs**:
- `Docs/R³/Contracts/R3Extractor.md` -- full API: init flow, extract()
- `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md` -- Section 2: Pipeline Overview, Section 7: Auto-Discovery

**Related Docs**:
- `Docs/R³/Pipeline/DependencyDAG.md`, `Docs/R³/Pipeline/Performance.md`, `Docs/R³/Pipeline/Normalization.md`, `Docs/R³/Pipeline/StateManagement.md`

**Depends On**: All registry, pipeline, and group modules.

**Exports**: `R3Extractor`, `R3Output` (frozen: `features: Tensor`, `feature_names: Tuple[str,...]`)

**Key Constraints**:
- Init: auto_discover_groups() -> register each -> freeze() -> build DependencyDAG
- `extract(mel: Tensor) -> R3Output`:
  1. Validate mel: shape (B,128,T), float32
  2. StageExecutor.execute(mel, groups, dag)
  3. torch.cat(group outputs in order, dim=-1) -> (B,T,128)
  4. FeatureNormalizer.normalize() -> [0,1]
  5. Return R3Output
- Properties: `total_dim`=128, `feature_names`, `feature_map`
- Deterministic, device-agnostic

**Verification**: [ ] output (B,T,128), [ ] all [0,1], [ ] 128 feature names, [ ] deterministic

---

### `ear/r3/__init__.py`

**Purpose**: Package init -- clean public API.
**Exports**: `R3Extractor`, `R3Output`, `R3_DIM`, `R3_FEATURE_NAMES`
**Constraint**: `__all__` explicitly lists exports.

---

## DAG Quick Reference

```
                  mel (B, 128, T)
                  |
  +-------+-------+-------+-------+-------+-------+
  v       v       v       v       v       v       v
[A:7D] [B:5D]  [C:9D]  [D:4D] [F:16D] [J:20D] [K:14D]    Stage 1
  |       |       |       |       |               |
  +---+---+---+---+       |       |               |
      v                   |       v               |
   [E:24D]                |    [H:12D]            |         Stage 2
  deps:A,B,C,D            v   dep:F chroma        |
                        [G:10D]                    |
                       dep:B[11]                   |
                           |                       |
      +----------+---------+                       |
      v          v         v                       |
            [I:7D]                                 |         Stage 3
           deps:F,G,H                             |
                                                   |
  concat: [A|B|C|D|E|F|G|H|I|J|K] -> (B, T, 128)
```

---

## Verification Gate G2

```python
# G2 verification (R3 portion)
import torch
from Musical_Intelligence.ear.r3 import R3Extractor, R3Output, R3_DIM, R3_FEATURE_NAMES

extractor = R3Extractor()

# Dimensions
assert extractor.total_dim == 128 and R3_DIM == 128
assert len(R3_FEATURE_NAMES) == 128
fmap = extractor.feature_map
assert len(fmap.groups) == 11 and fmap.total_dim == 128

# Group boundaries
for name, s, e in [("consonance",0,7),("energy",7,12),("timbre",12,21),("change",21,25),
    ("interactions",25,49),("pitch_chroma",49,65),("rhythm_groove",65,75),
    ("harmony",75,87),("information",87,94),("timbre_extended",94,114),("modulation",114,128)]:
    g = fmap.get_group(name)
    assert g.start == s and g.end == e

# Extract
mel = torch.randn(2, 128, 1000)
output = extractor.extract(mel)
assert isinstance(output, R3Output)
assert output.features.shape == (2, 1000, 128)
assert output.features.min() >= 0.0 and output.features.max() <= 1.0
assert output.feature_names[0] == "roughness" and output.feature_names[127] == "spectral_slope_0_500"

# Determinism
assert torch.allclose(output.features, extractor.extract(mel).features)

print("G2 PASSED (R3): R3Extractor produces (B, T, 128) with [0,1] range")
```

---

## Cross-References

| Doc Path | Used By |
|----------|---------|
| `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md` | All files (architecture) |
| `Docs/R³/Registry/FeatureCatalog.md` | Constants + all groups (names, tiers, indices) |
| `Docs/R³/Registry/DimensionMap.md` | group_boundaries.py, domain_map.py |
| `Docs/R³/Registry/NamingConventions.md` | feature_names.py |
| `Docs/R³/Contracts/BaseSpectralGroup.md` | All 11 group.py files |
| `Docs/R³/Contracts/R3Extractor.md` | extractor.py |
| `Docs/R³/Contracts/R3FeatureRegistry.md` | feature_registry.py, feature_map.py |
| `Docs/R³/Contracts/R3FeatureSpec.md` | feature_registry.py |
| `Docs/R³/Contracts/ExtensionProtocol.md` | auto_discovery.py |
| `Docs/R³/Pipeline/DependencyDAG.md` | dag.py, stage_executor.py |
| `Docs/R³/Pipeline/Normalization.md` | normalization.py |
| `Docs/R³/Pipeline/Performance.md` | stage_executor.py, warmup.py |
| `Docs/R³/Pipeline/StateManagement.md` | warmup.py, stage_executor.py |
| `Docs/R³/Standards/QualityTiers.md` | quality_tiers.py |
| `Docs/R³/Domains/Psychoacoustic/A-Consonance.md` | Group A files |
| `Docs/R³/Domains/Temporal/B-Energy.md` | Group B files |
| `Docs/R³/Domains/Spectral/C-Timbre.md` | Group C files |
| `Docs/R³/Domains/Spectral/D-Change.md` | Group D files |
| `Docs/R³/Domains/CrossDomain/E-Interactions.md` | Group E files |
| `Docs/R³/Domains/Tonal/F-PitchChroma.md` | Group F files |
| `Docs/R³/Domains/Temporal/G-RhythmGroove.md` | Group G files |
| `Docs/R³/Domains/Tonal/H-HarmonyTonality.md` | Group H files |
| `Docs/R³/Domains/Information/I-InformationSurprise.md` | Group I files |
| `Docs/R³/Domains/Spectral/J-TimbreExtended.md` | Group J files |
| `Docs/R³/Domains/Psychoacoustic/K-ModulationPerception.md` | Group K files |
| `Docs/R³/upgrade_beta/R3-V2-DESIGN.md` | Historical design rationale (do not code) |
