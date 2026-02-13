# MPU -- R3 Feature Mapping

## Overview
- **Unit**: Motor Planning Unit
- **Model count**: 10 models (alpha: 3, beta: 4, gamma: 3)
- **Primary R3 domains**: B (Energy), D (Change)
- **R3 dependency strength**: Critical
- **ACOUSTIC gaps**: 3 (syncopation_index, metrical_structure_complexity, locomotion_periodicity)
- **New group demand**: G:Rhythm (Very High)

## Current Usage (v1, [0:49])

| Group | Indices Used | Usage Level | Key Models |
|-------|-------------|-------------|------------|
| A: Consonance [0:7] | Minimal | Minor (0/10) | -- |
| B: Energy [7:12] | All 5D, esp. onset_strength [11] | Dominant (10/10) | All 10 models |
| C: Timbre [12:21] | Minimal | Minor (0/10) | -- |
| D: Change [21:25] | spectral_flux [21] | Primary (8/10) | PEOM, MSR, GSSM, ASAP, DDSMI, SPMC, CTBB, STC |
| E: Interactions [25:49] | Selective | Minor (2/10) | GSSM, NSCP |

MPU is tied with STU for the highest Energy consumption rate (10/10 models).
Motor planning is driven entirely by onset energy and spectral flux -- the raw
temporal dynamics of the audio signal. MPU currently has zero access to
dedicated rhythmic structure features, making G:Rhythm its most critical
expansion.

## New Feature Consumption (v2, [49:128])

| Group | Indices | Relevance | Rationale |
|-------|---------|-----------|-----------|
| F: Pitch & Chroma [49:65] | -- | Low | MPU does not process pitch features. |
| G: Rhythm & Groove [65:75] | All 10D | **Very High** | MPU is the second-largest G group consumer (after STU). syncopation_index [68] and metricality_index [69] were explicitly requested in gap logs. PEOM, GSSM, MSR, ASAP, DDSMI, SPMC, STC all need rhythmic structure. |
| H: Harmony [75:87] | -- | Low | MPU does not process harmonic structure. |
| I: Information [87:94] | -- | Low | MPU does not use information-theoretic features. |
| J: Timbre Extended [94:114] | -- | Low | MPU is not timbre-focused. |
| K: Modulation [114:128] | modulation_1Hz [115], modulation_2Hz [116] | Medium | Locomotion-relevant modulation (0.5-2 Hz) for GSSM stride periodicity. |

## Gap Resolution

| Gap ID | Description | Resolution | New Index |
|--------|------------|------------|-----------|
| MPU-1 | syncopation_index | RESOLVED: G:syncopation_index | [68] |
| MPU-2 | metrical_structure_complexity | Partially: G:metricality_index [69] provides regularity; complexity is approximately 1 - metricality. K:modulation_spectrum reflects metrical layer count indirectly. | [69] inverse |
| MPU-6 | locomotion_periodicity (0.5-2 Hz) | Partially: K:modulation_0.5Hz [114], modulation_1Hz [115], modulation_2Hz [116] cover the band. G:tempo_estimate [65] also operates in this range. | [114:117] |

**Resolution rate**: 1 fully resolved, 2 partially resolved.

## Per-Model R3 Summary

| Model | Tier | Current R3 Groups | New R3 Groups | Priority |
|-------|------|------------------|---------------|----------|
| PEOM | alpha1 | B, D | G (syncopation, metricality, beat_strength, groove) | High |
| MSR | alpha2 | B, D | G (syncopation, tempo_estimate, tempo_stability) | High |
| GSSM | alpha3 | B, D, E | G (groove, syncopation, metricality), K (mod_0.5-2Hz) | High |
| ASAP | beta1 | B, D | G (syncopation, metricality, pulse_clarity) | High |
| DDSMI | beta2 | B, D | G (syncopation, beat_strength) | Medium |
| VRMSME | beta3 | B | -- | Low |
| SPMC | beta4 | B, D | G (syncopation, metricality, beat_strength) | Medium |
| NSCP | gamma1 | B, E | G (pulse_clarity) | Low |
| CTBB | gamma2 | B, D | G (tempo_estimate, metricality) | Medium |
| STC | gamma3 | B, D | G (syncopation, metricality, tempo_stability) | Medium |
