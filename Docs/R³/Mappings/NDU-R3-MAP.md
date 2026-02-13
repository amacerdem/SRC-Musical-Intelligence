# NDU -- R3 Feature Mapping

## Overview
- **Unit**: Novelty Detection Unit
- **Model count**: 9 models (alpha: 3, beta: 3, gamma: 3)
- **Primary R3 domains**: D (Change), E (Interactions)
- **R3 dependency strength**: Critical
- **ACOUSTIC gaps**: 4 (syntactic_irregularity, perceptual_ambiguity, musical_roundness, entrainment_index)
- **New group demand**: H:Harmony (High), I:Information (Medium-High)

## Current Usage (v1, [0:49])

| Group | Indices Used | Usage Level | Key Models |
|-------|-------------|-------------|------------|
| A: Consonance [0:7] | Selective | Minor (2/9) | SDD, SLEE |
| B: Energy [7:12] | Selective | Moderate (2/9) | EDNR, ONI |
| C: Timbre [12:21] | Selective | Minor (2/9) | SDD, SDDP |
| D: Change [21:25] | All 4D | Dominant (9/9) | All 9 models |
| E: Interactions [25:49] | Cross-group products | Primary (7/9) | MPG, EDNR, DSP_, CDMR, SLEE, ONI, ECT |

NDU is the only unit where all 9 models read the Change group. The
Change+Interactions combination provides the deviation signals that drive
novelty detection. The new H and I groups will add harmonic syntax and
information-theoretic dimensions that are currently missing.

## New Feature Consumption (v2, [49:128])

| Group | Indices | Relevance | Rationale |
|-------|---------|-----------|-----------|
| F: Pitch & Chroma [49:65] | chroma [49:61] | Low | Only SDD uses pitch for deviance detection. Chroma provides basis for H group features. |
| G: Rhythm & Groove [65:75] | -- | Low | NDU detects deviations, not rhythmic structure. |
| H: Harmony & Tonality [75:87] | syntactic_irregularity [86], key_clarity [75], tonal_stability [84], diatonicity [85], tonnetz [76:82] | **High** | SDD, CDMR, SLEE, EDNR perform harmonic syntax deviation detection. syntactic_irregularity is the single most important new feature for NDU. Tonnetz enables tonal space deviation measurement. |
| I: Information & Surprise [87:94] | melodic_entropy [87], harmonic_entropy [88], spectral_surprise [90], tonal_ambiguity [93] | Medium-High | SDD, CDMR, SLEE can use predictive surprise signals. tonal_ambiguity directly addresses the perceptual_ambiguity gap. |
| J: Timbre Extended [94:114] | -- | Low | NDU is not timbre-focused. |
| K: Modulation [114:128] | -- | Low | NDU does not process modulation rates. |

## Gap Resolution

| Gap ID | Description | Resolution | New Index |
|--------|------------|------------|-----------|
| NDU-001 | syntactic_irregularity_level | RESOLVED: H:syntactic_irregularity | [86] |
| NDU-002 | perceptual_ambiguity_level | RESOLVED: I:tonal_ambiguity | [93] |
| NDU-003 | cortical_entrainment_index | OUT OF SCOPE: neural metric, not acoustic. Handled by H3/BEP mechanism. | -- |
| NDU-004 | perceived_musical_roundness | Partially: H:tonal_stability [84] + H:key_clarity [75] composite proxy. "Roundness" lacks clear acoustic definition. | [84]+[75] proxy |

**Resolution rate**: 2 fully resolved, 1 partially resolved, 1 out of scope.

## Per-Model R3 Summary

| Model | Tier | Current R3 Groups | New R3 Groups | Priority |
|-------|------|------------------|---------------|----------|
| MPG | alpha1 | D, E | I (spectral_surprise) | Low |
| SDD | alpha2 | A, C, D | H (syntactic_irregularity, tonnetz), I (melodic_entropy, tonal_ambiguity) | High |
| EDNR | alpha3 | B, D, E | H (tonal_stability, key_clarity) | Medium |
| DSP_ | beta1 | D, E | I (spectral_surprise) | Low |
| CDMR | beta2 | D, E | H (syntactic_irregularity, tonnetz, diatonicity), I (harmonic_entropy) | High |
| SLEE | beta3 | A, D, E | H (syntactic_irregularity, tonal_stability), I (melodic_entropy) | High |
| SDDP | gamma1 | C, D | -- | Low |
| ONI | gamma2 | B, D, E | -- | Low |
| ECT | gamma3 | D, E | I (spectral_surprise) | Low |
