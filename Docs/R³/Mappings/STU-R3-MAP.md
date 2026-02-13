# STU -- R3 Feature Mapping

## Overview
- **Unit**: Sensorimotor Timing Unit
- **Model count**: 14 models (alpha: 3, beta: 7, gamma: 4)
- **Primary R3 domains**: B (Energy), D (Change)
- **R3 dependency strength**: Critical
- **ACOUSTIC gaps**: 0 (indirect -- G:Rhythm addresses STU's core needs)
- **New group demand**: G:Rhythm (Very High), K:Modulation (Low-Medium)

## Current Usage (v1, [0:49])

| Group | Indices Used | Usage Level | Key Models |
|-------|-------------|-------------|------------|
| A: Consonance [0:7] | Minimal | Minor (1/14) | MDNS |
| B: Energy [7:12] | All 5D, esp. onset_strength [11], loudness [10] | Dominant (13/14) | All except TPIO |
| C: Timbre [12:21] | Selective | Minor (2/14) | AMSS, TPIO |
| D: Change [21:25] | spectral_flux [21] primary | Primary (10/14) | HMCE, AMSC, EDTA, ETAM, HGSIC, OMS, TMRM, NEWMD, MPFS |
| E: Interactions [25:49] | Selective | Minor (1/14) | HGSIC |

STU is the second most Energy-dependent unit (13/14 tied with MPU). The onset
strength and spectral flux features drive beat tracking, entrainment, and
temporal prediction across nearly all models.

## New Feature Consumption (v2, [49:128])

| Group | Indices | Relevance | Rationale |
|-------|---------|-----------|-----------|
| F: Pitch & Chroma [49:65] | pitch_height [61] | Low | Only MDNS (melodic decoding) uses pitch features. |
| G: Rhythm & Groove [65:75] | All 10D | **Very High** | STU's primary domain. 10/14 models directly benefit from syncopation [68], metricality [69], tempo [65], beat_strength [66], groove [71]. STU is the single largest consumer of G group. |
| H: Harmony [75:87] | -- | Low | STU does not process harmonic structure. |
| I: Information [87:94] | rhythmic_IC [89] | Low-Medium | HGSIC and ETAM can use rhythmic information content for groove integration. |
| J: Timbre Extended [94:114] | -- | Low | STU is not timbre-focused. |
| K: Modulation [114:128] | modulation_1Hz [115], modulation_2Hz [116], modulation_4Hz [117], fluctuation_strength [123] | Medium | Beat-rate modulation (1-4 Hz) directly relevant to entrainment models (ETAM, OMS, TMRM). |

## Gap Resolution

STU had no explicit ACOUSTIC gaps in the gap log. However, the demand matrix
shows that ~12 of 14 models benefit from the new G:Rhythm group features.

| Gap ID | Description | Resolution | New Index |
|--------|------------|------------|-----------|
| (indirect) | No dedicated rhythm features | G group provides syncopation, metricality, groove, tempo | [65:75] |

## Per-Model R3 Summary

| Model | Tier | Current R3 Groups | New R3 Groups | Priority |
|-------|------|------------------|---------------|----------|
| HMCE | alpha1 | B, D | G (syncopation, metricality, tempo) | High |
| AMSC | alpha2 | B, D | G (syncopation, metricality, beat_strength) | High |
| MDNS | alpha3 | A, B | F (pitch_height), G (tempo) | Medium |
| AMSS | beta1 | B, C | G (tempo_stability) | Low |
| TPIO | beta2 | C | -- | Low |
| EDTA | beta3 | B, D | G (tempo_estimate, tempo_stability, metricality) | High |
| ETAM | beta4 | B, D | G (syncopation, groove), I (rhythmic_IC), K (mod_2Hz) | High |
| HGSIC | beta5 | B, D, E | G (groove, syncopation), I (rhythmic_IC), K (mod_4Hz) | High |
| OMS | beta6 | B, D | G (metricality, beat_strength, syncopation), K (mod_2Hz) | High |
| TMRM | gamma1 | B, D | G (tempo_estimate, tempo_stability) | Medium |
| NEWMD | gamma2 | B, D | G (beat_strength, pulse_clarity) | Medium |
| MTNE | gamma3 | B | G (tempo_stability) | Low |
| PTGMP | gamma4 | B | G (tempo_stability) | Low |
| MPFS | gamma5 | B, D | G (groove, event_density) | Medium |
