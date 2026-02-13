# SPU -- R3 Feature Mapping

## Overview
- **Unit**: Spectral Processing Unit
- **Model count**: 9 models (alpha: 3, beta: 3, gamma: 3)
- **Primary R3 domains**: A (Consonance), C (Timbre)
- **R3 dependency strength**: Critical
- **ACOUSTIC gaps**: 0 (SPU is fully covered by current 49D)
- **New group demand**: F:Pitch (High), H:Harmony (Medium)

## Current Usage (v1, [0:49])

| Group | Indices Used | Usage Level | Key Models |
|-------|-------------|-------------|------------|
| A: Consonance [0:7] | All 7D | Dominant (8/9) | BCH, PSCL, PCCR, STAI, MIAA, SDNPS, ESME, SDED |
| B: Energy [7:12] | Minimal | Minor (0/9 primary) | -- |
| C: Timbre [12:21] | All 9D | Primary (5/9) | PSCL, STAI, TSCP, MIAA, ESME |
| D: Change [21:25] | Minimal | Minor (0/9 primary) | -- |
| E: Interactions [25:49] | Selective | Minor (1/9) | STAI |

SPU is the most Consonance-dependent unit (8/9 models). Timbre features support
cortical tonotopy and spectral processing. Energy and Change groups are not
directly consumed because SPU processes spectral structure, not temporal dynamics.

## New Feature Consumption (v2, [49:128])

| Group | Indices | Relevance | Rationale |
|-------|---------|-----------|-----------|
| F: Pitch & Chroma [49:65] | chroma [49:61], pitch_height [61], pitch_salience [63], inharmonicity [64] | **High** | SPU's core domain is pitch processing. chroma_vector directly serves PSCL, PCCR, TPRD-related features. pitch_salience replaces indirect proxy via A group harmonicity. |
| G: Rhythm & Groove [65:75] | -- | Low | SPU does not process temporal structure. |
| H: Harmony & Tonality [75:87] | key_clarity [75], tonnetz [76:82], tonal_stability [84] | Medium | BCH, STAI benefit from harmonic structure context. Tonnetz provides geometric pitch-class relations. |
| I: Information [87:94] | -- | Low | SPU does not use information-theoretic features. |
| J: Timbre Extended [94:114] | mfcc [94:107], spectral_contrast [107:114] | Medium | MFCC extends timbre representation for TSCP, MIAA, ESME. Spectral contrast complements existing C group. |
| K: Modulation [114:128] | sharpness_zwicker [122] | Low | Only Zwicker sharpness is relevant; DIN 45692 complements the existing C:sharpness proxy [13]. |

## Gap Resolution

No ACOUSTIC gaps were identified for SPU. All spectral processing needs are
met by the current 49D plus the new F and H groups.

| Gap ID | Description | Resolution | New Index |
|--------|------------|------------|-----------|
| -- | No gaps | -- | -- |

## Per-Model R3 Summary

| Model | Tier | Current R3 Groups | New R3 Groups | Priority |
|-------|------|------------------|---------------|----------|
| BCH | alpha1 | A | F (chroma, salience), H (key_clarity) | High |
| PSCL | alpha2 | A, C | F (chroma, pitch_height, salience) | High |
| PCCR | alpha3 | A | F (chroma, pitch_salience) | High |
| STAI | beta1 | A, C, E | F (inharmonicity), H (tonnetz, tonal_stability) | Medium |
| TSCP | beta2 | C | J (mfcc, spectral_contrast) | Medium |
| MIAA | beta3 | A, C | F (chroma, pitch_height), J (mfcc) | Medium |
| SDNPS | gamma1 | A | F (pitch_salience, inharmonicity) | Low |
| ESME | gamma2 | A, C | F (chroma), J (spectral_contrast) | Low |
| SDED | gamma3 | A | F (inharmonicity) | Low |
