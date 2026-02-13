# R3 Naming Conventions

**Version**: 2.0.0
**Source**: R3-CROSSREF.md Section 1.4, R3-V2-DESIGN.md Section 2
**Updated**: 2026-02-13

---

## Table of Contents

1. [Feature Names](#1-feature-names)
2. [Group Names](#2-group-names)
3. [Domain Names](#3-domain-names)
4. [Canonical Name Resolution](#4-canonical-name-resolution)
5. [Semantic vs Computational Names](#5-semantic-vs-computational-names)
6. [Reserved Prefixes by Domain](#6-reserved-prefixes-by-domain)

---

## 1. Feature Names

### Convention: `snake_case`

All R3 feature names use lowercase `snake_case`. This applies to:

- Feature names in `BaseSpectralGroup.feature_names`
- Feature names in `R3FeatureMap` and `R3GroupInfo`
- Feature names in documentation tables and indexes
- Feature names in C3 model documentation Section 4 references

### Rules

| Rule | Example (correct) | Example (incorrect) |
|------|-------------------|---------------------|
| Lowercase only | `spectral_flux` | `Spectral_Flux`, `SPECTRAL_FLUX` |
| Underscore separator | `onset_strength` | `onsetStrength`, `onset-strength` |
| No leading/trailing underscores | `roughness` | `_roughness`, `roughness_` |
| No double underscores | `spectral_flux` | `spectral__flux` |
| No digits at start | `mfcc_1` | `1_mfcc` |
| Descriptive, not abbreviated | `pitch_height` | `ph`, `p_h` |
| Standard abbreviations allowed | `mfcc_1`, `nPVI` | Arbitrary abbreviations |

### Allowed Abbreviations

| Abbreviation | Expansion | Usage |
|-------------|-----------|-------|
| mfcc | Mel-Frequency Cepstral Coefficient | `mfcc_1` through `mfcc_13` |
| nPVI | normalized Pairwise Variability Index | `isochrony_nPVI` |
| HHI | Herfindahl-Hirschman Index | Internal reference only |
| KL | Kullback-Leibler | Internal reference only |
| IOI | Inter-Onset Interval | Internal reference only |
| BPM | Beats Per Minute | Internal reference only |
| RMS | Root Mean Square | Internal reference only |
| DCT | Discrete Cosine Transform | Internal reference only |
| FFT | Fast Fourier Transform | Internal reference only |
| EMA | Exponential Moving Average | Internal reference only |

### Naming Patterns by Feature Type

| Pattern | Rule | Examples |
|---------|------|---------|
| Chroma features | `chroma_{note}` using standard note names | `chroma_C`, `chroma_Db`, `chroma_Gb` |
| MFCC features | `mfcc_{n}` where n is coefficient number (1-13) | `mfcc_1`, `mfcc_13` |
| Spectral contrast | `spectral_contrast_{n}` where n is sub-band (1-7) | `spectral_contrast_1`, `spectral_contrast_7` |
| Modulation rates | `modulation_{rate}Hz` or `modulation_{rate}_Hz` | `modulation_0_5Hz`, `modulation_4Hz` |
| Tonnetz | `tonnetz_{interval}_{axis}` | `tonnetz_fifth_x`, `tonnetz_minor_y` |
| Interaction terms | `x_{block}_{n}` | `x_l0l5_0`, `x_l4l5_3` |

### Chroma Note Names

The 12 chroma features use standard Western music note names with flat notation:

| Index | Note | Feature Name |
|:-----:|------|-------------|
| 0 | C | `chroma_C` |
| 1 | Db | `chroma_Db` |
| 2 | D | `chroma_D` |
| 3 | Eb | `chroma_Eb` |
| 4 | E | `chroma_E` |
| 5 | F | `chroma_F` |
| 6 | Gb | `chroma_Gb` |
| 7 | G | `chroma_G` |
| 8 | Ab | `chroma_Ab` |
| 9 | A | `chroma_A` |
| 10 | Bb | `chroma_Bb` |
| 11 | B | `chroma_B` |

**Rationale**: Flat notation (Db, Eb, Gb, Ab, Bb) is chosen over sharp notation (C#, D#, F#, G#, A#) to avoid the `#` character, which has special meaning in many programming contexts and comment syntaxes.

---

## 2. Group Names

### Convention: Dual Format

Group names have two canonical forms:

| Context | Format | Rule | Example |
|---------|--------|------|---------|
| Class name | PascalCase | `{GroupName}Group` suffix | `ConsonanceGroup`, `PitchChromaGroup` |
| GROUP_NAME attribute | snake_case | Lowercase with underscores | `"consonance"`, `"pitch_chroma"` |
| Documentation | Title Case | Human-readable full name | "Pitch & Chroma", "Rhythm & Groove" |
| Letter designation | Single uppercase | A through K | `A`, `F`, `K` |

### Complete Group Name Registry

| Letter | CLASS_NAME | GROUP_NAME | Doc Name | Domain |
|:------:|-----------|-----------|----------|--------|
| A | `ConsonanceGroup` | `"consonance"` | Consonance | Psychoacoustic |
| B | `EnergyGroup` | `"energy"` | Energy | Spectral |
| C | `TimbreGroup` | `"timbre"` | Timbre | Spectral |
| D | `ChangeGroup` | `"change"` | Change | Temporal |
| E | `InteractionsGroup` | `"interactions"` | Interactions | CrossDomain |
| F | `PitchChromaGroup` | `"pitch_chroma"` | Pitch & Chroma | Tonal |
| G | `RhythmGrooveGroup` | `"rhythm_groove"` | Rhythm & Groove | Temporal |
| H | `HarmonyTonalityGroup` | `"harmony_tonality"` | Harmony & Tonality | Tonal |
| I | `InformationSurpriseGroup` | `"information_surprise"` | Information & Surprise | Information |
| J | `TimbreExtendedGroup` | `"timbre_extended"` | Timbre Extended | Spectral |
| K | `ModulationPsychoacousticGroup` | `"modulation_psychoacoustic"` | Modulation & Psychoacoustic | Psychoacoustic |

### GROUP_NAME Uniqueness

The `GROUP_NAME` attribute must be unique across all registered groups. The `R3FeatureRegistry.register()` method enforces this with a `ValueError` on duplicate names.

---

## 3. Domain Names

### Convention: PascalCase for Directories, snake_case for Code

| Domain | Directory Name | Code Value | DOMAIN Attribute |
|--------|---------------|------------|-----------------|
| Psychoacoustic | `Psychoacoustic/` | `"psychoacoustic"` | `"psychoacoustic"` |
| Spectral | `Spectral/` | `"spectral"` or `"dsp"` | `"spectral"` |
| Tonal | `Tonal/` | `"tonal"` | `"tonal"` |
| Temporal | `Temporal/` | `"temporal"` | `"temporal"` |
| Information | `Information/` | `"information"` | `"information"` |
| CrossDomain | `CrossDomain/` | `"cross_domain"` | `"cross_domain"` |

### Documentation Directory Structure

```
Docs/R3/Domains/
  Psychoacoustic/     Groups A, K
  Spectral/           Groups B, C, J
  Tonal/              Groups F, H
  Temporal/           Groups D, G
  Information/        Groups I
  CrossDomain/        Groups E
```

### Code Directory Structure

```
mi_beta/ear/r3/
  psychoacoustic/     Group A (consonance)
  dsp/                Groups B, C, D (energy, timbre, change)
  cross_domain/       Group E (interactions)
  extensions/         Groups F, G, H, I, J, K (new groups)
```

**Note**: The code directory structure does not perfectly mirror the domain taxonomy. The `dsp/` directory contains groups from both the Spectral and Temporal domains, and `extensions/` contains groups from multiple domains. The documentation directory structure (`Docs/R3/Domains/`) follows the formal domain taxonomy.

---

## 4. Canonical Name Resolution

### R1/R2/R3 Name Conflicts

During the R3 v2 design process, the same psychoacoustic concepts were given different names by the three research perspectives (R1: bottom-up gap analysis, R2: literature review, R3: toolkit survey). The canonical names were resolved as follows:

| Concept | R1 Name | R2 Name | R3 Name | Canonical Name |
|---------|---------|---------|---------|---------------|
| Pitch class distribution | pitch_chroma | chroma_vector | approximate_chromagram | **chroma_vector** (stored as `chroma_C` through `chroma_B`) |
| Melodic uncertainty | melodic_entropy | melodic_information_content | -- | **melodic_entropy** |
| Harmonic uncertainty | harmonic_entropy | harmonic_surprisal | -- | **harmonic_entropy** |
| Syncopation measure | syncopation_index | syncopation_index | syncopation | **syncopation_index** |
| Metric regularity | metricality_index | metrical_level | -- | **metricality_index** |
| Tonal stability | tonal_stability | tonal_stability / key_clarity | -- | **tonal_stability** (separate: **key_clarity**) |
| Spectral surprise | -- | spectral_surprise | spectral_surprise | **spectral_surprise** |
| Rhythmic info content | rhythmic_information_content | -- | information_content | **rhythmic_information_content** |
| Groove quality | groove_index | groove_factor | groove_features | **groove_index** |
| Tonal space position | tonal_space_trajectory | tonnetz_coordinates | tonnetz | **tonnetz** (6D, stored as `tonnetz_fifth_x` etc.) |
| Spectral contrast | -- | spectral_contrast | spectral_contrast | **spectral_contrast** (7D) |
| MFCC | -- | -- | MFCC | **mfcc** (13D) |
| Modulation spectrum | -- | modulation_spectrum | modulation_spectrum | **modulation_spectrum** (6D rates) |

### Resolution Rules

1. **Prefer the most specific name**: If one perspective uses a more descriptive name, prefer it (e.g., `rhythmic_information_content` over `information_content`).
2. **Prefer established MIR terminology**: Use names that are standard in MIR literature (e.g., `tonnetz` over `tonal_space_trajectory`).
3. **Separate distinct concepts**: If a single R-perspective name conflates two distinct concepts, separate them (e.g., `tonal_stability` and `key_clarity` are separate features, not aliases).
4. **Use snake_case for feature names**: Even if the canonical concept name uses different formatting (e.g., "nPVI" becomes `isochrony_nPVI`).

---

## 5. Semantic vs Computational Names

R3 feature names follow a **semantic naming** convention: names describe what the feature represents perceptually, not how it is computed.

### Semantic Names (Preferred)

| Feature Name | What It Means | How It Is Computed |
|-------------|--------------|-------------------|
| `roughness` | Perceived surface roughness of the sound | `sigmoid(mel.var(dim=1) / mel.mean(dim=1))` |
| `key_clarity` | How clearly the music has a tonal center | `max(pearson_corr(chroma, 24_key_profiles))` |
| `groove_index` | How much the music induces body movement | `syncopation * bass_energy * pulse_clarity` |
| `tonal_ambiguity` | How uncertain the key identification is | `entropy(softmax(key_correlations))` |

### Computational Names (Discouraged for Features)

| Discouraged | Preferred |
|-------------|-----------|
| `mel_variance_ratio` | `roughness` |
| `key_profile_max_corr` | `key_clarity` |
| `chroma_transition_entropy` | `melodic_entropy` |
| `onset_autocorr_peak` | `beat_strength` |

### Exceptions

Computational names are acceptable when:

1. **The computation IS the concept**: `mfcc_1` through `mfcc_13` (MFCCs are defined by their computation). Similarly, `spectral_flux`, `spectral_contrast`, `distribution_entropy`.
2. **No established semantic name exists**: `alpha_ratio`, `hammarberg_index` (named after the researchers who defined them).
3. **The name disambiguates**: `spectral_slope_0_500` specifies the frequency range, which is essential for distinguishing from other slopes.

---

## 6. Reserved Prefixes by Domain

Each domain has reserved name prefixes that should only be used for features within that domain. This prevents cross-domain naming collisions and makes feature domain membership clear from the name alone.

### Prefix Registry

| Domain | Reserved Prefixes | Examples |
|--------|------------------|---------|
| **Psychoacoustic** | `roughness_`, `consonance_`, `dissonance_`, `sharpness_`, `fluctuation_`, `modulation_` | `roughness`, `sharpness_zwicker`, `modulation_4Hz` |
| **Spectral** | `spectral_`, `mfcc_`, `tristimulus`, `amplitude_`, `loudness_` | `spectral_flux`, `mfcc_1`, `loudness_a_weighted` |
| **Tonal** | `chroma_`, `pitch_`, `key_`, `tonnetz_`, `tonal_`, `harmonic_`, `diatonic` | `chroma_C`, `pitch_height`, `key_clarity`, `tonnetz_fifth_x` |
| **Temporal** | `tempo_`, `beat_`, `rhythm_`, `onset_`, `groove_`, `syncopation_`, `metrical_`, `event_` | `tempo_estimate`, `beat_strength`, `rhythmic_regularity` |
| **Information** | `entropy_`, `surprise_`, `information_`, `predictive_`, `ambiguity_` | `melodic_entropy`, `spectral_surprise`, `predictive_entropy` |
| **CrossDomain** | `x_`, `interaction_` | `x_l0l5_0`, `x_l4l5_3` |

### Prefix Ownership Rules

1. **Strict ownership**: A feature name starting with a domain's reserved prefix should belong to a group within that domain.
2. **Cross-references allowed**: A feature may conceptually bridge domains (e.g., `tonal_ambiguity` in Information domain uses the `tonal_` prefix). In such cases, the feature belongs to the domain of its group, and the prefix is a semantic hint, not a strict domain assignment.
3. **New prefixes**: When adding a new feature that does not fit existing prefixes, consult the naming conventions before creating a new prefix. New prefixes should be registered in this document.

### Name Uniqueness

**All 128 feature names must be globally unique.** The `R3FeatureRegistry.freeze()` method (Phase 6) will enforce this constraint. Currently, uniqueness is maintained by convention and documentation review.

Verification command:
```python
from mi_beta.ear.r3 import R3Extractor
extractor = R3Extractor()
names = extractor.feature_names
assert len(names) == len(set(names)), "Duplicate feature names detected!"
```

---

## Appendix: Complete Sorted Feature Name List

For reference, all 128 feature names sorted alphabetically:

```
acceleration_A              [9]   B  Spectral
alpha_ratio                 [125] K  Psychoacoustic
amplitude                   [7]   B  Spectral
beat_strength               [66]  G  Temporal
chroma_A                    [58]  F  Tonal
chroma_Ab                   [57]  F  Tonal
chroma_B                    [60]  F  Tonal
chroma_Bb                   [59]  F  Tonal
chroma_C                    [49]  F  Tonal
chroma_D                    [51]  F  Tonal
chroma_Db                   [50]  F  Tonal
chroma_E                    [53]  F  Tonal
chroma_Eb                   [52]  F  Tonal
chroma_F                    [54]  F  Tonal
chroma_G                    [56]  F  Tonal
chroma_Gb                   [55]  F  Tonal
clarity                     [15]  C  Spectral
diatonicity                 [85]  H  Tonal
distribution_concentration  [24]  D  Temporal
distribution_entropy        [22]  D  Temporal
distribution_flatness       [23]  D  Temporal
event_density               [72]  G  Temporal
fluctuation_strength        [123] K  Psychoacoustic
groove_index                [71]  G  Temporal
hammarberg_index            [126] K  Psychoacoustic
harmonic_change             [83]  H  Tonal
harmonic_deviation          [6]   A  Psychoacoustic
harmonic_entropy            [88]  I  Information
helmholtz_kang              [2]   A  Psychoacoustic
inharmonicity               [5]   A  Psychoacoustic
inharmonicity_index         [64]  F  Tonal
information_rate            [91]  I  Information
isochrony_nPVI              [70]  G  Temporal
key_clarity                 [75]  H  Tonal
loudness                    [10]  B  Spectral
loudness_a_weighted         [124] K  Psychoacoustic
melodic_entropy             [87]  I  Information
metricality_index           [69]  G  Temporal
mfcc_1                      [94]  J  Spectral
mfcc_10                     [103] J  Spectral
mfcc_11                     [104] J  Spectral
mfcc_12                     [105] J  Spectral
mfcc_13                     [106] J  Spectral
mfcc_2                      [95]  J  Spectral
mfcc_3                      [96]  J  Spectral
mfcc_4                      [97]  J  Spectral
mfcc_5                      [98]  J  Spectral
mfcc_6                      [99]  J  Spectral
mfcc_7                      [100] J  Spectral
mfcc_8                      [101] J  Spectral
mfcc_9                      [102] J  Spectral
modulation_0_5Hz            [114] K  Psychoacoustic
modulation_16Hz             [119] K  Psychoacoustic
modulation_1Hz              [115] K  Psychoacoustic
modulation_2Hz              [116] K  Psychoacoustic
modulation_4Hz              [117] K  Psychoacoustic
modulation_8Hz              [118] K  Psychoacoustic
modulation_bandwidth        [121] K  Psychoacoustic
modulation_centroid         [120] K  Psychoacoustic
onset_strength              [11]  B  Spectral
pitch_class_entropy         [62]  F  Tonal
pitch_height                [61]  F  Tonal
pitch_salience              [63]  F  Tonal
predictive_entropy          [92]  I  Information
pulse_clarity               [67]  G  Temporal
rhythmic_information_content [89] I  Information
rhythmic_regularity         [74]  G  Temporal
roughness                   [0]   A  Psychoacoustic
sensory_pleasantness        [4]   A  Psychoacoustic
sethares_dissonance         [1]   A  Psychoacoustic
sharpness                   [13]  C  Spectral
sharpness_zwicker           [122] K  Psychoacoustic
spectral_autocorrelation    [17]  C  Spectral
spectral_contrast_1         [107] J  Spectral
spectral_contrast_2         [108] J  Spectral
spectral_contrast_3         [109] J  Spectral
spectral_contrast_4         [110] J  Spectral
spectral_contrast_5         [111] J  Spectral
spectral_contrast_6         [112] J  Spectral
spectral_contrast_7         [113] J  Spectral
spectral_flux               [21]  D  Temporal
spectral_slope_0_500        [127] K  Psychoacoustic
spectral_smoothness         [16]  C  Spectral
spectral_surprise           [90]  I  Information
stumpf_fusion               [3]   A  Psychoacoustic
syncopation_index           [68]  G  Temporal
syntactic_irregularity      [86]  H  Tonal
tempo_estimate              [65]  G  Temporal
tempo_stability             [73]  G  Temporal
tonal_ambiguity             [93]  I  Information
tonal_stability             [84]  H  Tonal
tonalness                   [14]  C  Spectral
tonnetz_fifth_x             [76]  H  Tonal
tonnetz_fifth_y             [77]  H  Tonal
tonnetz_major_x             [80]  H  Tonal
tonnetz_major_y             [81]  H  Tonal
tonnetz_minor_x             [78]  H  Tonal
tonnetz_minor_y             [79]  H  Tonal
tristimulus1                [18]  C  Spectral
tristimulus2                [19]  C  Spectral
tristimulus3                [20]  C  Spectral
velocity_A                  [8]   B  Spectral
voice_leading_distance      [82]  H  Tonal
warmth                      [12]  C  Spectral
x_l0l5_0                   [25]  E  CrossDomain
x_l0l5_1                   [26]  E  CrossDomain
x_l0l5_2                   [27]  E  CrossDomain
x_l0l5_3                   [28]  E  CrossDomain
x_l0l5_4                   [29]  E  CrossDomain
x_l0l5_5                   [30]  E  CrossDomain
x_l0l5_6                   [31]  E  CrossDomain
x_l0l5_7                   [32]  E  CrossDomain
x_l4l5_0                   [33]  E  CrossDomain
x_l4l5_1                   [34]  E  CrossDomain
x_l4l5_2                   [35]  E  CrossDomain
x_l4l5_3                   [36]  E  CrossDomain
x_l4l5_4                   [37]  E  CrossDomain
x_l4l5_5                   [38]  E  CrossDomain
x_l4l5_6                   [39]  E  CrossDomain
x_l4l5_7                   [40]  E  CrossDomain
x_l5l7_0                   [41]  E  CrossDomain
x_l5l7_1                   [42]  E  CrossDomain
x_l5l7_2                   [43]  E  CrossDomain
x_l5l7_3                   [44]  E  CrossDomain
x_l5l7_4                   [45]  E  CrossDomain
x_l5l7_5                   [46]  E  CrossDomain
x_l5l7_6                   [47]  E  CrossDomain
x_l5l7_7                   [48]  E  CrossDomain
```

Total: 128 unique feature names (verified: no duplicates).
