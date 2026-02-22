# F9 Mechanism Orchestrator -- Social Cognition

**Function**: F9 Social Cognition
**Models covered**: 3/3 -- 0 IMPLEMENTED + 3 PENDING
**Total F9 mechanism output**: 33D (11D + 11D + 11D)
**Beliefs**: 10 (from NSCP, SSRI, DDSMI)
**H3 demands**: 43 tuples (all pending)
**Architecture**: Parallel -- no inter-model depth ordering within F9

---

## IMPORTANT: Cross-Reference Architecture

F9 has NO dedicated unit. All 3 models have their mechanism layer docs in their **primary
function directories**, NOT duplicated here. This orchestrator provides F9-specific summaries
and cross-references to the canonical mechanism documentation.

| Model | Primary Function | Mechanism Docs Location |
|-------|-----------------|------------------------|
| **NSCP** | F7 Motor & Timing | `F7-Motor-and-Timing/mechanisms/nscp/` (e_layer.md, m_layer.md, p_layer.md, f_layer.md) |
| **SSRI** | F6 Reward & Motivation | `F6-Reward-and-Motivation/mechanisms/ssri/` (e_layer.md, m_layer.md, p_layer.md, f_layer.md) |
| **DDSMI** | F7 Motor & Timing | `F7-Motor-and-Timing/mechanisms/ddsmi/` (e_layer.md, m_layer.md, p_layer.md, f_layer.md) |

---

## Model Pipeline

```
R3 (97D) ---+--------------------------------------------
H3 tuples --+
            |
            v
         NSCP   (11D, MPU-gamma1)  <- neural synchrony commercial prediction (ISC-popularity)
         SSRI   (11D, RPU-beta4)   <- social synchrony reward integration (group coordination reward)
         DDSMI  (11D, MPU-beta2)   <- dyadic dance social motor integration (mTRF resource)
```

F9 models operate in **parallel** -- they do not form a depth-ordered DAG among themselves.
Each model reads from R3/H3 and from upstream models within their home units (MPU or RPU).
The outputs converge at the social prediction error -> F6 RewardAggregator junction.

---
---

# NSCP -- Neural Synchrony Commercial Prediction

**Model**: MPU-gamma1-NSCP
**Type**: Mechanism -- reads PEOM, ASAP, SPMC motor timing outputs + R3/H3
**Tier**: gamma (50-70% confidence)
**Output**: 11D per frame (4 layers: E 3D + M 3D + P 2D + F 3D)
**Phase**: 3
**Status**: PENDING
**F9 Role**: F9-primary model -- the only model with F9 as its primary function

> **Canonical docs**: `F7-Motor-and-Timing/mechanisms/nscp/` (4 layer docs)

---

## 1. Identity

NSCP models the pathway from population-level neural synchrony (inter-subject correlation) to commercial success prediction. ISC predicts streaming popularity (R^2=0.619 combined model); 1% ISC increase corresponds to ~2.4M more Spotify streams. Catchiness (groove/motor entrainment) drives repeated listening via an inverted-U syncopation-groove relationship. Leeuwis 2021: EEG ISC + Spotify streams, R^2=0.404 early, R^2=0.619 combined.

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[3]** | stumpf | A: Consonance | Harmonic consonance for cross-subject consistency |
| 2 | **[7]** | amplitude | B: Dynamics | Acoustic salience for attention capture |
| 3 | **[8]** | loudness | B: Dynamics | Loudness entropy for engagement driver |
| 4 | **[10]** | spectral_flux | B: Dynamics | Musical events for ISC engagement |
| 5 | **[25:33]** | x_l0l5 | F: Interactions | Cross-layer coherence as neural sync proxy |
| 6 | **[33:41]** | x_l4l5 | G: Interactions | Multi-feature binding for ISC prediction |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 3D | f22:neural_synchrony, f23:commercial_prediction, f24:catchiness_index | 5 | ISC proxy from coherence periodicity + consonance; commercial from f22 + binding periodicity; catchiness from onset periodicity + loudness entropy. Leeuwis 2021: R^2=0.619. Spiech 2022: groove inverted-U F(1,29)=10.515. |
| **M** (Temporal) | 3D | isc_magnitude, sync_consistency, popularity_estimate | 3 | ISC = f22; consistency from coherence + binding periodicity dual; popularity = f23. Leeuwis 2021: early R^2=0.404 vs late R^2=0.393 (stable). |
| **P** (Present) | 2D | coherence_level, groove_response | 6 | Coherence from shortest H3 (25ms-100ms) cross-layer coupling; groove from short-timescale onset tracking. Hasson 2004: ISC content-driven and reliable. |
| **F** (Forecast) | 3D | synchrony_pred, popularity_pred, catchiness_pred | 5 | Synchrony from f22 + coherence period; popularity from f23 + binding period; catchiness from f24 + onset period. ISC temporal stability supports prediction. |

**Total**: 11D, 14 H3 tuples (L2)

---

## 4. F9 Output Routing

| Output | -> F9 Belief | Type |
|--------|-------------|------|
| coherence_level + groove_response | -> `neural_synchrony` | Core (tau=0.65) |
| catchiness_pred | -> `catchiness_pred` | Anticipation |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Frontocentral Cortex | Strongest ISC effects (Leeuwis 2021: EEG) |
| Temporal Cortex | ISC during naturalistic listening (Hasson 2004) |
| NAcc | Predicts future sales (Berns 2010: r=0.33) |
| Motor Cortex | Groove/motor entrainment (Sarasso 2019: eta^2=0.685) |

4+ papers: Leeuwis 2021 (EEG, R^2=0.619), Berns 2010 (fMRI), Spiech 2022, Sarasso 2019, Hasson 2004.

---

## 6. Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [3,7,8,10,25:33,33:41] | 6 feature groups | Consonance, dynamics, interactions |
| H3 | 14 tuples | Multi-scale coherence, binding, onset periodicity |
| Upstream (MPU) | PEOM, ASAP, SPMC outputs | Motor timing context within home unit |

---
---

# SSRI -- Social Synchrony Reward Integration

**Model**: RPU-beta4-SSRI
**Type**: Mechanism -- reads DAED, RPEM reward outputs + R3/H3
**Tier**: beta (Bridging, 70-90% confidence)
**Output**: 11D per frame (4 layers: E 5D + M 2D + P 2D + F 2D)
**Phase**: 3
**Status**: PENDING
**F9 Role**: F6-primary, contributes 6 of 10 F9 beliefs (dominant social belief source)

> **Canonical docs**: `F6-Reward-and-Motivation/mechanisms/ssri/` (4 layer docs)

---

## 1. Identity

SSRI models the reward amplification from interpersonal musical synchrony. Joint music-making activates caudate with synchrony quality; social bonding increases prefrontal neural synchronization (d=0.85); beta-endorphin release from sustained coordinated activity mediates social bonding and pain threshold elevation. Group music-making amplifies hedonic reward by 1.3-1.8x vs solo listening. Ni et al. 2024: fNIRS hyperscanning, N=528, d=0.85.

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[4]** | sensory_pleasantness | A: Consonance | Shared hedonic quality |
| 2 | **[7]** | amplitude | B: Dynamics | Shared dynamic envelope |
| 3 | **[8]** | loudness | B: Dynamics | Perceptual intensity matching |
| 4 | **[10]** | spectral_flux | B: Dynamics | Temporal alignment / onset synchrony |
| 5 | **[12]** | warmth | C: Timbre | Timbral blending quality |
| 6 | **[21]** | spectral_change | D: Change | Structural coordination demand |
| 7 | **[22]** | energy_change | D: Change | Dynamic coordination tracking |
| 8 | **[25:33]** | x_l0l5 | F: Interactions | Foundation-perceptual coupling |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 5D | f01:synchrony_reward, f02:social_bonding_index, f03:group_flow_state, f04:entrainment_quality, f05:collective_pleasure | 12 | Synchrony reward from onset periodicity + pleasantness + coupling trend. Bonding builds on synchrony over 5s LTI. Flow = f01 + dynamics. Entrainment = fast-scale onset alignment (100-500ms). Collective pleasure = f02 + f03 + pleasantness. Kokal 2011: caudate activation with synchrony quality. |
| **M** (Temporal) | 2D | social_prediction_error, synchrony_amplification | 0 | SPE = f04 - expected coordination (from beliefs). Amplification = 1.0 + f01*(f04+f02), range [1.0, ~3.0]. kappa_social=0.60. Cheung 2019: uncertainty x surprise interaction. |
| **P** (Present) | 2D | prefrontal_coupling, endorphin_proxy | 2 | Prefrontal = sigma(0.4*f04 + 0.3*coupling_500ms). Ni 2024: rDLPFC sync d=0.85. Endorphin = sigma(0.4*f02 + 0.3*f03 + 0.3*coupling_5s). tau_endorphin=30.0s. Dunbar 2012: pain threshold elevation. |
| **F** (Forecast) | 2D | bonding_trajectory_pred, flow_sustain_pred | 2 | Bonding direction from f02 + coupling trend + loudness trend. tau_bonding=120.0s. Flow sustainability from f03 + f04 + arousal. Gold 2019: optimal complexity. |

**Total**: 11D, 18 H3 tuples (L0 + L2)

---

## 4. F9 Output Routing

| Output | -> F9 Belief | Type |
|--------|-------------|------|
| f01:synchrony_reward | -> `synchrony_reward` | Appraisal |
| f02:social_bonding_index | -> `social_bonding` | Appraisal |
| f03:group_flow_state | -> `group_flow` | Appraisal |
| f04:entrainment_quality | -> `entrainment_quality` | Appraisal |
| social_prediction_error | -> `social_prediction_error` | Appraisal |
| flow_sustain_pred | -> `collective_pleasure_pred` | Anticipation |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Caudate | Synchrony-dependent activation (Kokal 2011) |
| rDLPFC / rTPJ | Inter-brain prefrontal sync (Ni 2024, d=0.85) |
| NAcc | Social reward amplification |
| VTA | Endorphin-DA interaction for social bonding |

4+ papers: Kokal 2011, Ni 2024 (N=528, d=0.85), Dunbar 2012, Wohltjen 2023, Williamson & Bonshor 2019, Tarr 2014.

---

## 6. Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [4,7,8,10,12,21,22,25:33] | 8 feature groups | Consonance, dynamics, timbre, change, interactions |
| H3 | 18 tuples | Fast (100-125ms) to long-range (5s) coordination tracking |
| Upstream (RPU) | DAED, RPEM outputs | DA anticipation, prediction error for social RPE |

---
---

# DDSMI -- Dyadic Dance Social Motor Integration

**Model**: MPU-beta2-DDSMI
**Type**: Mechanism -- reads PEOM, ASAP outputs + R3/H3
**Tier**: beta (Bridging, 70-90% confidence)
**Output**: 11D per frame (4 layers: E 3D + M 3D + P 2D + F 3D)
**Phase**: 3
**Status**: PENDING
**F9 Role**: F7-primary, contributes 2 F9 beliefs (social_coordination + resource_allocation)

> **Canonical docs**: `F7-Motor-and-Timing/mechanisms/ddsmi/` (4 layer docs)

---

## 1. Identity

DDSMI models the four parallel neural tracking processes during dyadic dance (social coordination, music tracking, self-movement, partner tracking), compressed into three distinct computational signals. Resource competition between auditory and social processing is the key mechanism: visual contact shifts resources from music tracking to social coordination (F(1,57)=7.48, p=.033). Self-movement tracking is autonomous from social context (all ps>.224). Bigand et al. 2025: dual-EEG mTRF, F(1,57)=249.75.

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[8]** | loudness | B: Dynamics | Loudness entropy for resource demand |
| 2 | **[10]** | spectral_flux | B: Dynamics | Music onset detection for auditory tracking |
| 3 | **[25:33]** | x_l0l5 | F: Interactions | Music-motor coupling pathway |
| 4 | **[33:41]** | x_l4l5 | G: Interactions | Social coupling / partner coordination pathway |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 3D | f13:social_coordination, f14:music_tracking, f15:visual_modulation | 11 | Social from x_l4l5 periodicity multi-scale; music from x_l0l5 periodicity + onset; visual = f13-f14 resource shift + loudness entropy. Bigand 2025: social mTRF F(1,57)=249.75; music F(1,57)=30.22. |
| **M** (Temporal) | 3D | mTRF_social, mTRF_auditory, mTRF_balance | 0 | Social = f13; auditory = f14; balance = sigma(0.5*f13 + 0.5*(1-f14)). Visual contact x music interaction F(1,57)=50.10. |
| **P** (Present) | 2D | partner_sync, music_entrainment | 0 | Partner sync from social mTRF + fast coupling; music entrainment from auditory mTRF + coupling. Wohltjen 2023: beat entrainment predicts social synchrony (d=1.37). |
| **F** (Forecast) | 3D | coordination_pred, music_pred, social_pred | 0 | Coordination from f13 + social period 1s; music from f14 + music period 1s; social from f13 + f15. Sabharwal 2024: Granger causality predicts leader/follower. |

**Total**: 11D, 11 H3 tuples (L2)

---

## 4. F9 Output Routing

| Output | -> F9 Belief | Type |
|--------|-------------|------|
| partner_sync + music_entrainment | -> `social_coordination` | Core (tau=0.60) |
| mTRF_balance | -> `resource_allocation` | Appraisal |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Left M1 | Self-produced actions (Kohler 2025: MVPA) |
| Right PMC | Other-produced actions (Kohler 2025) |
| Bilateral STG | Auditory tracking during dance |
| Prefrontal | Social coordination (Bigand 2025: mTRF) |

4+ papers: Bigand 2025 (EEG, N=58, dual-EEG mTRF), Wohltjen 2023 (d=1.37), Kohler 2025, Sabharwal 2024, Yoneta 2022.

---

## 6. Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [8,10,25:33,33:41] | 4 feature groups | Dynamics, interactions |
| H3 | 11 tuples | Fast (100ms) to sustained (1s) social and music tracking |
| Upstream (MPU) | PEOM, ASAP outputs | Period entrainment, beat prediction for motor context |

---
---

## Summary Statistics

### Output Dimensions by Model

| Model | Unit | Tier | D | E-Layer | M-Layer | P-Layer | F-Layer | H3 |
|-------|------|------|---|---------|---------|---------|---------|-----|
| NSCP | MPU | gamma | 11 | 3 | 3 | 2 | 3 | 14 |
| SSRI | RPU | beta | 11 | 5 | 2 | 2 | 2 | 18 |
| DDSMI | MPU | beta | 11 | 3 | 3 | 2 | 3 | 11 |
| **TOTAL** | | | **33** | **11** | **8** | **6** | **8** | **43** |

### Tier Gradient

| Tier | Count | Avg D | Avg H3 |
|------|-------|-------|--------|
| beta | 2 | 11.0 | 14.5 |
| gamma | 1 | 11.0 | 14.0 |

F9 outputs are perfectly uniform at 11D per model, reflecting the consistent 4-layer EMPF
architecture across all three models. H3 demand is highest for SSRI (18), driven by its
12 E-layer tuples spanning 100ms to 5s LTI timescales for comprehensive social coordination
tracking. NSCP requires 14 tuples for multi-scale ISC and groove features. DDSMI is most
compact at 11 tuples, with all H3 demands concentrated in the E-layer.

### Brain Region Convergence

**Frontocentral / Prefrontal Cortex**: mentioned in NSCP, SSRI, DDSMI -- 3 of 3 models.
Social cognition consistently engages prefrontal circuitry: ISC (frontocentral), inter-brain
sync (rDLPFC/rTPJ), and social coordination (prefrontal mTRF).

**NAcc / Ventral Striatum**: mentioned in NSCP, SSRI -- 2 of 3 models.
Reward-social convergence hub: predicts future sales (NSCP) and mediates social reward amplification (SSRI).

**Motor Cortex (M1/PMC)**: mentioned in NSCP, DDSMI -- 2 of 3 models.
Motor-social integration: groove entrainment (NSCP) and self/other action discrimination (DDSMI).

**Bilateral STG**: mentioned in DDSMI -- 1 of 3 models (auditory tracking during dance).

**Caudate**: mentioned in SSRI -- 1 of 3 models (synchrony-dependent activation).

Prefrontal cortex is the convergence hub for F9: all 3 models implicate prefrontal circuitry,
consistent with the role of prefrontal regions in social cognition, inter-brain synchronization,
and executive control of auditory-social resource allocation.

### Unit Distribution

| Unit | Count | Models |
|------|-------|--------|
| MPU (Motor Processing Unit) | 2 | NSCP, DDSMI |
| RPU (Reward Processing Unit) | 1 | SSRI |

F9 is predominantly MPU (2/3 models), reflecting that social cognition in music is fundamentally
a motor-social integration function. The 1 RPU model (SSRI) addresses the reward dimension of
social music -- how interpersonal coordination amplifies mesolimbic reward. All 3 models share
the same 11D output dimensionality.

### Layer Distribution

| Layer Type | Models With | Total Dims |
|------------|-------------|------------|
| E (Extraction) | 3/3 | 11D |
| M (Temporal Integration) | 3/3 | 8D |
| P (Cognitive Present) | 3/3 | 6D |
| F (Forecast) | 3/3 | 8D |

All 3 models have all 4 layers (E+M+P+F). The E-layer has the most dimensions (11D), with
SSRI alone contributing 5D of social reward features. The P-layer is the most compact (6D, 2D
per model), reflecting that social cognition requires fewer present-state outputs than
extraction or temporal integration. M and F layers are balanced at 8D each.

### H3 Demand Distribution

| Layer | NSCP | SSRI | DDSMI | Total |
|-------|------|------|-------|-------|
| E | 5 | 12 | 11 | 28 |
| M | 3 | 0 | 0 | 3 |
| P | 6 | 2 | 0 | 8 |
| F | 5 | 2 | 0 | 7 |
| **Unique** | **14** | **18** | **11** | **43** |

Note: Some H3 tuples may be shared across layers within a model (deduplicated in the unique count).
SSRI and DDSMI concentrate all or nearly all H3 demand in the E-layer, with M/P/F layers
operating on E-layer outputs. NSCP distributes demand more evenly across all 4 layers.
