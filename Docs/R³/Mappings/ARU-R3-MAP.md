# ARU -- R3 Feature Mapping

## Overview
- **Unit**: Affective Resonance Unit
- **Model count**: 10 models (alpha: 3, beta: 4, gamma: 3)
- **Primary R3 domains**: All groups via cross-unit pathways (P1, P3, P5)
- **R3 dependency strength**: Important (pathway-mediated, not direct)
- **ACOUSTIC gaps**: 0 (ARU is fully covered by current 49D)
- **New group demand**: Minimal direct; I:Information (Medium) for PUPF only

## Current Usage (v1, [0:49])

| Group | Indices Used | Usage Level | Key Models |
|-------|-------------|-------------|------------|
| A: Consonance [0:7] | All 7D via pathways | Primary (7/10) | SRP, AAC, VMM, PUPF, MAD, NEMAC, DAP |
| B: Energy [7:12] | All 5D via pathways | Dominant (10/10) | All 10 models |
| C: Timbre [12:21] | All 9D via pathways | Substantial (7/10) | SRP, AAC, VMM, MAD, NEMAC, CMAT, TAR |
| D: Change [21:25] | spectral_flux via pathways | Substantial (4/10) | SRP, AAC, PUPF, CLAM |
| E: Interactions [25:49] | Cross-group products | Substantial (7/10) | SRP, AAC, VMM, PUPF, MAD, NEMAC, CMAT |

ARU is a dependent unit that receives R3 features through cross-unit pathways
from SPU (P1), IMU (P3), and STU (P5). This architecture means ARU has the
broadest R3 coverage of any unit (10/10 read Energy, 7/10 read Consonance and
Timbre). New R3 features will automatically flow to ARU via these pathways.

## New Feature Consumption (v2, [49:128])

| Group | Indices | Relevance | Rationale |
|-------|---------|-----------|-----------|
| F: Pitch & Chroma [49:65] | Indirect via pathways | Low | SRP, AAC, VMM receive pitch indirectly through P1 (SPU). No direct demand. |
| G: Rhythm & Groove [65:75] | Indirect via pathways | Low | SRP, AAC receive rhythm indirectly through P5 (STU). No direct demand. |
| H: Harmony & Tonality [75:87] | Indirect via pathways | Low | VMM, SRP may receive tonal features indirectly. No direct demand. |
| I: Information & Surprise [87:94] | predictive_entropy [92] | Medium | PUPF (Prediction-Uncertainty-Pleasure Function) directly couples prediction uncertainty to pleasure valence. predictive_entropy is the one I group feature with genuine direct demand from ARU. |
| J: Timbre Extended [94:114] | mfcc [94:107] | Low-Medium | CMAT, TAR, NEMAC could benefit from richer timbral features via pathways. |
| K: Modulation [114:128] | fluctuation_strength [123] | Low | Only TAR (therapeutic resonance) may benefit from 4 Hz fluctuation strength. |

## Gap Resolution

ARU had zero ACOUSTIC gaps in the gap log. The unit's needs are entirely
served by current features plus pathway-mediated access to new features from
upstream units.

| Gap ID | Description | Resolution | New Index |
|--------|------------|------------|-----------|
| -- | No gaps | -- | -- |

## Per-Model R3 Summary

| Model | Tier | Current R3 Groups | New R3 Groups | Priority |
|-------|------|------------------|---------------|----------|
| SRP | alpha1 | A, B, C, D, E | Indirect: all new groups via P1/P3/P5 | Low |
| AAC | alpha2 | A, B, C, D, E | Indirect: all new groups via pathways | Low |
| VMM | alpha3 | A, B, C, E | Indirect: F, H via P1 | Low |
| PUPF | beta1 | A, B, D, E | I (predictive_entropy) -- direct demand | Medium |
| CLAM | beta2 | B, D | -- | Low |
| MAD | beta3 | A, B, C, E | -- | Low |
| NEMAC | beta4 | A, B, C, E | J (mfcc) via pathways | Low |
| DAP | gamma1 | A, B | -- | Low |
| CMAT | gamma2 | B, C, E | J (spectral_contrast) via pathways | Low |
| TAR | gamma3 | B, C | K (fluctuation_strength) | Low |
