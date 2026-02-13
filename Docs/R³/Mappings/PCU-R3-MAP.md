# PCU -- R3 Feature Mapping

## Overview
- **Unit**: Predictive Coding Unit
- **Model count**: 10 models (alpha: 3, beta: 4, gamma: 3)
- **Primary R3 domains**: A (Consonance), C (Timbre), E (Interactions)
- **R3 dependency strength**: Critical
- **ACOUSTIC gaps**: 4 (periodicity, 1/f_slope, key_clarity, index remapping)
- **New group demand**: I:Information (High), H:Harmony (Medium-High), F:Pitch (Medium)

## Current Usage (v1, [0:49])

| Group | Indices Used | Usage Level | Key Models |
|-------|-------------|-------------|------------|
| A: Consonance [0:7] | All 7D | Primary (7/10) | HTP, SPH, ICEM, PWUP, UDP, CHPI, MAA, PSH |
| B: Energy [7:12] | Selective | Moderate (4/10) | HTP, ICEM, WMED, CHPI, MAA |
| C: Timbre [12:21] | All 9D | Substantial (5/10) | HTP, SPH, CHPI, IGFE, MAA, PSH |
| D: Change [21:25] | spectral_flux [21] | Moderate (3/10) | HTP, WMED, UDP, CHPI |
| E: Interactions [25:49] | Cross-group products | Primary (7/10) | HTP, ICEM, PWUP, WMED, UDP, CHPI, MAA, PSH |

PCU is the most Interaction-heavy independent unit (7/10). Its core function
is prediction error computation, which requires cross-domain feature
combinations. Consonance and Timbre provide the spectral templates against
which predictions are checked.

## New Feature Consumption (v2, [49:128])

| Group | Indices | Relevance | Rationale |
|-------|---------|-----------|-----------|
| F: Pitch & Chroma [49:65] | chroma [49:61], pitch_height [61], pitch_salience [63], inharmonicity [64] | Medium | SPH (pitch height prediction), CHPI (cross-modal harmonic prediction). Chroma provides basis for harmonic prediction in H group. |
| G: Rhythm & Groove [65:75] | -- | Low | PCU does not process rhythmic structure directly. |
| H: Harmony & Tonality [75:87] | key_clarity [75], tonnetz [76:82], tonal_stability [84], harmonic_change [83], syntactic_irregularity [86] | Medium-High | UDP (key_clarity, 1/f slope via tonal stability), HTP (hierarchical tonal prediction), ICEM, CHPI (harmonic prediction). |
| I: Information & Surprise [87:94] | All 7D | **High** | PCU's core function is prediction error. melodic_entropy [87], harmonic_entropy [88], spectral_surprise [90], predictive_entropy [92] directly encode the uncertainty and surprise signals PCU models operate on. 5/10 models are primary consumers. |
| J: Timbre Extended [94:114] | mfcc [94:107] | Low-Medium | IGFE, MAA, PSH could use MFCC for richer timbral prediction. |
| K: Modulation [114:128] | spectral_slope_0_500 [127] | Low | UDP's 1/f_spectral_slope gap is addressed by K:spectral_slope_0_500. |

## Gap Resolution

| Gap ID | Description | Resolution | New Index |
|--------|------------|------------|-----------|
| PCU-PWUP-1 | R3[14] tonalness to brightness_kuttruff remap | NOT R3 EXPANSION: NAMING mismatch. Phase 5 doc-code reconciliation. | -- |
| PCU-PWUP-2 | R3[5] periodicity to roughness_total | Partially: F:pitch_salience [63] + A:harmonicity [2] together provide periodicity. Phase 6 formula revision for A[5]. | [63]+[2] |
| PCU-UDP-1 | 1/f_spectral_slope | RESOLVED: K:spectral_slope_0_500 | [127] |
| PCU-UDP-2 | key_clarity / tonal_stability | RESOLVED: H:key_clarity [75] and H:tonal_stability [84] | [75], [84] |

**Resolution rate**: 2 fully resolved, 1 partially resolved, 1 naming issue (not R3 expansion).

## Per-Model R3 Summary

| Model | Tier | Current R3 Groups | New R3 Groups | Priority |
|-------|------|------------------|---------------|----------|
| HTP | alpha1 | A, B, C, D, E | H (tonnetz, harmonic_change, key_clarity), I (melodic_entropy, predictive_entropy) | High |
| SPH | alpha2 | A, C | F (chroma, pitch_height, pitch_salience) | Medium |
| ICEM | alpha3 | A, B, E | I (melodic_entropy, harmonic_entropy, spectral_surprise) | High |
| PWUP | beta1 | A, E | F (pitch_salience), I (predictive_entropy) | Medium |
| WMED | beta2 | B, D, E | I (melodic_entropy, spectral_surprise, information_rate) | High |
| UDP | beta3 | A, D, E | H (key_clarity, tonal_stability), I (harmonic_entropy), K (spectral_slope) | High |
| CHPI | beta4 | A, B, C, D, E | F (chroma, inharmonicity), H (syntactic_irregularity, tonnetz), I (predictive_entropy) | High |
| IGFE | gamma1 | C | J (mfcc, spectral_contrast) | Low |
| MAA | gamma2 | A, B, C, E | -- | Low |
| PSH | gamma3 | A, C, E | -- | Low |
