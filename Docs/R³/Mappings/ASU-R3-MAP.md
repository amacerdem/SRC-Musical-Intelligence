# ASU -- R3 Feature Mapping

## Overview
- **Unit**: Auditory Salience Unit
- **Model count**: 9 models (alpha: 3, beta: 3, gamma: 3)
- **Primary R3 domains**: B (Energy), C (Timbre)
- **R3 dependency strength**: Critical
- **ACOUSTIC gaps**: 2 (inharmonicity_index, consonance_gradient)
- **New group demand**: F:Pitch (Medium), G:Rhythm (Low-Medium)

## Current Usage (v1, [0:49])

| Group | Indices Used | Usage Level | Key Models |
|-------|-------------|-------------|------------|
| A: Consonance [0:7] | Selective | Moderate (2/9) | IACM, CSG |
| B: Energy [7:12] | All 5D, esp. onset_strength [11], loudness [10] | Primary (8/9) | All except CSG |
| C: Timbre [12:21] | All 9D | Primary (7/9) | IACM, CSG, BARM, STANM, AACM, PWSM, SDL |
| D: Change [21:25] | spectral_flux [21] | Moderate (4/9) | BARM, STANM, PWSM, DGTP |
| E: Interactions [25:49] | Minimal | Minor (0/9) | -- |

ASU detects salient auditory events through energy transients and timbral
deviance. The B+C combination dominates: 8/9 read Energy, 7/9 read Timbre.
ASU has the heaviest NAMING mismatch load (~50 entries) but these are doc-code
reconciliation issues, not R3 expansion needs.

## New Feature Consumption (v2, [49:128])

| Group | Indices | Relevance | Rationale |
|-------|---------|-----------|-----------|
| F: Pitch & Chroma [49:65] | inharmonicity_index [64], pitch_salience [63] | Medium | IACM (inharmonicity attention capture), CSG (consonance-salience gradient). Inharmonicity is the primary new feature for ASU. |
| G: Rhythm & Groove [65:75] | beat_strength [66], event_density [72] | Low-Medium | SNEM, BARM, DGTP process beat-salience but current B group onset_strength suffices. G adds marginal clarity for beat-driven salience. |
| H: Harmony [75:87] | -- | Low | ASU does not process harmonic structure. |
| I: Information [87:94] | -- | Low | ASU does not use information-theoretic features. |
| J: Timbre Extended [94:114] | spectral_contrast [107:114] | Medium | BARM, STANM, AACM, PWSM, SDL -- timbre-focused models benefit from octave-band contrast. |
| K: Modulation [114:128] | sharpness_zwicker [122] | Low | Complements existing C:sharpness [13] with perceptual grounding. |

## Gap Resolution

| Gap ID | Description | Resolution | New Index |
|--------|------------|------------|-----------|
| ASU-G04 | inharmonicity_index | RESOLVED: F:inharmonicity_index | [64] |
| ASU-G05 | consonance_gradient | Partially: A group temporal derivative + D:spectral_flux covers gradient. No separate feature needed. | -- (A+D combo) |

**Resolution rate**: 1 fully resolved, 1 covered by existing combination.

## Per-Model R3 Summary

| Model | Tier | Current R3 Groups | New R3 Groups | Priority |
|-------|------|------------------|---------------|----------|
| SNEM | alpha1 | B | G (beat_strength, event_density) | Low |
| IACM | alpha2 | A, B, C | F (inharmonicity_index, pitch_salience) | High |
| CSG | alpha3 | A, C | F (inharmonicity_index) | Medium |
| BARM | beta1 | B, C, D | G (beat_strength), J (spectral_contrast) | Low |
| STANM | beta2 | B, C, D | J (spectral_contrast) | Low |
| AACM | beta3 | B, C | J (spectral_contrast) | Low |
| PWSM | gamma1 | B, C, D | J (spectral_contrast) | Low |
| DGTP | gamma2 | B, D | G (beat_strength, event_density) | Low |
| SDL | gamma3 | B, C | J (spectral_contrast) | Low |
