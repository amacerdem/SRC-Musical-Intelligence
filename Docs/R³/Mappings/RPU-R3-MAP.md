# RPU -- R3 Feature Mapping

## Overview
- **Unit**: Reward Processing Unit
- **Model count**: 10 models (alpha: 3, beta: 4, gamma: 3)
- **Primary R3 domains**: A (Consonance), B (Energy), E (Interactions)
- **R3 dependency strength**: Important (pathway-mediated + direct)
- **ACOUSTIC gaps**: 7 (social synchrony x3, rhythmic IC/entropy x2, melodic/harmonic entropy x2)
- **New group demand**: I:Information (Very High), H:Harmony (Medium), G:Rhythm (Medium)

## Current Usage (v1, [0:49])

| Group | Indices Used | Usage Level | Key Models |
|-------|-------------|-------------|------------|
| A: Consonance [0:7] | All 7D | Substantial (8/10) | DAED, MORMR, RPEM, IUCP, MCCN, MEAMR, SSRI, LDAC, SSPS |
| B: Energy [7:12] | All 5D | Substantial (8/10) | DAED, MORMR, RPEM, MCCN, MEAMR, SSRI, LDAC, IOTMS, SSPS |
| C: Timbre [12:21] | Selective | Substantial (5/10) | MORMR, MCCN, MEAMR, SSRI, LDAC, SSPS |
| D: Change [21:25] | spectral_flux [21] | Substantial (4/10) | DAED, RPEM, IUCP, SSRI, IOTMS |
| E: Interactions [25:49] | Cross-group products | Substantial (8/10) | DAED, MORMR, RPEM, IUCP, MCCN, MEAMR, LDAC, SSPS |

RPU is a dependent unit receiving routed signals from ARU and SPU. Like ARU,
it has broad R3 access. The distinguishing feature is RPU's critical
dependence on information-theoretic features for reward computation. RPU has
the highest information group demand of any unit (6/10 direct consumers).

## New Feature Consumption (v2, [49:128])

| Group | Indices | Relevance | Rationale |
|-------|---------|-----------|-----------|
| F: Pitch & Chroma [49:65] | -- | Low | RPU does not process pitch directly. |
| G: Rhythm & Groove [65:75] | syncopation [68], groove [71], tempo [65] | Medium | SSRI (rhythmic_entrainment), IUCP (complexity), IOTMS (optimal tempo). Groove and syncopation are moderate-level reward signals. |
| H: Harmony & Tonality [75:87] | syntactic_irregularity [86], harmonic_change [83], tonal_stability [84] | Medium | RPEM, LDAC, SSPS, MCCN use harmonic prediction error for reward signals. |
| I: Information & Surprise [87:94] | All 7D | **Very High** | RPU is the single largest I group consumer. LDAC (melodic_entropy), IUCP (rhythmic_IC x entropy), RPEM (prediction error), SSRI (rhythmic IC), SSPS (IC x entropy saddle surface), MCCN (contextual uncertainty). RPU's reward computation is critically dependent on information-theoretic variables. |
| J: Timbre Extended [94:114] | -- | Low | RPU is not timbre-focused. |
| K: Modulation [114:128] | -- | Low | No direct demand. |

## Gap Resolution

| Gap ID | Description | Resolution | New Index |
|--------|------------|------------|-----------|
| RPU-001a | onset_synchrony_quality | OUT OF SCOPE: requires multi-track pipeline. Phase 4+ concern. | -- |
| RPU-001b | timbral_blend_index | OUT OF SCOPE: requires multi-track pipeline. | -- |
| RPU-001c | rhythmic_entrainment_index | OUT OF SCOPE: requires multi-track pipeline. | -- |
| RPU-002a | rhythmic_information_content | RESOLVED: I:rhythmic_information_content | [89] |
| RPU-002b | rhythmic_entropy | Partially: I:rhythmic_IC [89] + I:predictive_entropy [92] combined; G:rhythmic_regularity [74] is inverse proxy | [89]+[92] |
| RPU-004a | melodic_entropy | RESOLVED: I:melodic_entropy (approximate, chroma-based) | [87] |
| RPU-004b | harmonic_entropy | RESOLVED: I:harmonic_entropy (approximate, chroma-based) | [88] |

**Resolution rate**: 3 fully resolved, 1 partially resolved, 3 out of scope (multi-track).

## Per-Model R3 Summary

| Model | Tier | Current R3 Groups | New R3 Groups | Priority |
|-------|------|------------------|---------------|----------|
| DAED | alpha1 | A, B, D, E | I (spectral_surprise) | Low |
| MORMR | alpha2 | A, B, C, E | H (harmonic_change) | Low |
| RPEM | alpha3 | A, B, D, E | I (melodic_entropy, harmonic_entropy, predictive_entropy) | High |
| IUCP | beta1 | A, D, E | G (syncopation), I (rhythmic_IC, melodic_entropy, harmonic_entropy) | High |
| MCCN | beta2 | A, B, C, E | H (syntactic_irregularity), I (harmonic_entropy) | High |
| MEAMR | beta3 | A, B, C, E | -- | Low |
| SSRI | beta4 | A, B, C, D, E | G (groove, syncopation), I (rhythmic_IC, melodic_entropy) | High |
| LDAC | gamma1 | A, B, C, E | H (tonal_stability), I (melodic_entropy, harmonic_entropy) | High |
| IOTMS | gamma2 | B, D | G (tempo_estimate, tempo_stability) | Medium |
| SSPS | gamma3 | A, B, C, E | H (syntactic_irregularity), I (melodic_entropy, harmonic_entropy) | High |
