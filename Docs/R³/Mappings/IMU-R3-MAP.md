# IMU -- R3 Feature Mapping

## Overview
- **Unit**: Integrative Memory Unit
- **Model count**: 15 models (alpha: 3, beta: 9, gamma: 3)
- **Primary R3 domains**: All groups (broadest consumption of any independent unit)
- **R3 dependency strength**: Important
- **ACOUSTIC gaps**: 11 (highest of any unit)
- **New group demand**: I:Information (High), H:Harmony (Medium-High), F:Pitch (Medium), G:Rhythm (Medium)

## Current Usage (v1, [0:49])

| Group | Indices Used | Usage Level | Key Models |
|-------|-------------|-------------|------------|
| A: Consonance [0:7] | All 7D | Substantial (12/15) | MEAMN, PNH, MMP, PMIM, HCMC, RIRI, MSPBA, TPRD, DMMS, CSSL, CDEM |
| B: Energy [7:12] | All 5D | Substantial (12/15) | MEAMN, MMP, RASN, PMIM, OII, HCMC, RIRI, VRIAP, CMAPCC, DMMS, CDEM |
| C: Timbre [12:21] | All 9D | Substantial (8/15) | MEAMN, MMP, HCMC, VRIAP, TPRD, CMAPCC, CSSL, CDEM |
| D: Change [21:25] | spectral_flux [21] primary | Substantial (5/15) | RASN, PMIM, OII, MSPBA, CMAPCC |
| E: Interactions [25:49] | Cross-group products | Substantial (6/15) | MEAMN, PMIM, HCMC, MSPBA, DMMS, CDEM |

IMU is the most broadly distributed independent unit. Its memory function
requires encoding and retrieving patterns across all spectral domains. 12/15
models read Consonance, 12/15 read Energy, and 8/15 read Timbre.

## New Feature Consumption (v2, [49:128])

| Group | Indices | Relevance | Rationale |
|-------|---------|-----------|-----------|
| F: Pitch & Chroma [49:65] | chroma [49:61], pitch_height [61], inharmonicity [64] | Medium | TPRD (pitch_chroma, harmonic_resolvability), DMMS (melodic_contour via pitch_height delta), PNH (Pythagorean hierarchy). |
| G: Rhythm & Groove [65:75] | metricality [69], isochrony_nPVI [70], groove [71] | Medium | RASN (metricality), RIRI (groove, isochrony), CSSL (isochrony_nPVI). |
| H: Harmony & Tonality [75:87] | key_clarity [75], tonnetz [76:82], tonal_stability [84], syntactic_irregularity [86] | Medium-High | MSPBA (syntactic processing), MEAMN (tonal_space trajectory via tonnetz), PNH (tonal hierarchy). |
| I: Information [87:94] | melodic_entropy [87], harmonic_entropy [88], predictive_entropy [92] | **High** | PMIM, HCMC, MSPBA all process prediction error and information content. IMU is the third-largest I group consumer. |
| J: Timbre Extended [94:114] | mfcc [94:107] | Low-Medium | MEAMN, HCMC, MMP could use MFCC for finer timbral memory encoding. |
| K: Modulation [114:128] | fluctuation_strength [123] | Low | Only VRIAP (relaxation) may benefit from fluctuation strength at 4 Hz. |

## Gap Resolution

IMU had the highest ACOUSTIC gap count (11). The table below shows how each
is resolved in the R3 v2 feature set.

| Gap ID | Description | Resolution | New Index |
|--------|------------|------------|-----------|
| IMU-MEAMN-1 | nostalgia_acoustic_signature | OUT OF SCOPE: composite/CNN embedding, not acoustic | -- |
| IMU-MEAMN-2 | tonal_space_trajectory | Partially: tonnetz [76:82] provides position; trajectory via H3 | [76:82] |
| IMU-MMP-1 | arousal_potential | OUT OF SCOPE: composite of B group | -- |
| IMU-RASN-1 | metricality_index | RESOLVED: G:metricality_index | [69] |
| IMU-PMIM-1 | predictive_entropy | RESOLVED: I:predictive_entropy | [92] |
| IMU-TPRD-1 | pitch_chroma (cyclical) | RESOLVED: F:chroma_vector (12D) | [49:61] |
| IMU-TPRD-2 | harmonic_resolvability | Partially: F:pitch_salience as proxy | [63] |
| IMU-DMMS-1 | melodic_contour_direction | Partially: F:pitch_height delta via H3 | [61] |
| IMU-CSSL-1 | isochrony_nPVI | RESOLVED: G:isochrony_nPVI | [70] |
| IMU-RIRI-1 | groove_index | RESOLVED: G:groove_index | [71] |
| IMU-VRIAP-1 | relaxation_index | OUT OF SCOPE: composite of B, C | -- |

**Resolution rate**: 6 fully resolved, 3 partially resolved, 2 out of scope.

## Per-Model R3 Summary

| Model | Tier | Current R3 Groups | New R3 Groups | Priority |
|-------|------|------------------|---------------|----------|
| MEAMN | alpha1 | A, B, C, E | H (tonnetz, tonal_stability), F (chroma) | Medium |
| PNH | alpha2 | A | F (chroma, inharmonicity), H (key_clarity) | Medium |
| MMP | alpha3 | A, B, C | J (mfcc) | Low |
| RASN | beta1 | B, D | G (metricality, isochrony_nPVI) | High |
| PMIM | beta2 | A, B, D, E | I (predictive_entropy, melodic_entropy), H (syntactic_irregularity) | High |
| OII | beta3 | B, D | -- | Low |
| HCMC | beta4 | A, B, C, E | I (harmonic_entropy, predictive_entropy) | High |
| RIRI | beta5 | A, B | G (groove_index, isochrony_nPVI) | Medium |
| MSPBA | beta6 | A, D, E | H (syntactic_irregularity, tonnetz), I (melodic_entropy) | High |
| VRIAP | beta7 | B, C | K (fluctuation_strength) | Low |
| TPRD | beta8 | A, C | F (chroma, pitch_salience) | Medium |
| CMAPCC | beta9 | B, C, D | -- | Low |
| DMMS | gamma1 | A, B, E | F (chroma, pitch_height) | Medium |
| CSSL | gamma2 | A, C | G (isochrony_nPVI) | Medium |
| CDEM | gamma3 | A, B, C, E | -- | Low |
