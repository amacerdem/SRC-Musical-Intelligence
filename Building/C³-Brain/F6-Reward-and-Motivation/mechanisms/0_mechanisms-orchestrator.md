# F6 Mechanism Orchestrator — Reward and Motivation

**Function**: F6 Reward and Motivation
**Models covered**: 10/10 primary — 1 IMPLEMENTED (DAED relay) + 9 PENDING
**Total F6 mechanism output**: 70D (8+7+8+6+7+6+11+6+5+6)
**Beliefs**: 16 (5C + 7A + 4N) — from DAED (2), MORMR (1), RPEM (2), IUCP (1), MCCN (2), MEAMR (1), SSRI (2), LDAC (1), IOTMS (2), SSPS (2)
**H3 demands**: ~170 tuples (16 DAED-implemented + ~154 pending)
**Architecture**: Depth-ordered — 3 alpha (Depth 0) -> 4 beta (Depth 1) -> 3 gamma (Depth 2)

---

## Model Pipeline (Depth Order)

```
R3 (97D) ---+--------------------------------------------
H3 tuples --+
            |
Depth 0:  DAED   (8D, relay, RPU-alpha1)  <- dopamine anticipation-experience dissociation (caudate/NAcc DA)
          MORMR  (7D, RPU-alpha2)          <- mu-opioid receptor music reward (MOR hedonic)
          RPEM   (8D, RPU-alpha3)          <- reward prediction error in music (VS RPE crossover)
            |
            |
Depth 1:  IUCP   (6D, RPU-beta1)   <- inverted-U complexity preference (Berlyne optimal complexity)
          MCCN   (7D, RPU-beta2)   <- musical chills cortical network (theta + arousal chills)
          MEAMR  (6D, RPU-beta3)   <- music-evoked autobiographical memory reward (dMPFC nostalgia)
          SSRI   (11D, RPU-beta4)  <- social synchrony reward integration (group coordination reward)
            |
            |
Depth 2:  LDAC   (6D, RPU-gamma1) <- liking-dependent auditory cortex (STG pleasure gating)
          IOTMS  (5D, RPU-gamma2) <- individual opioid tone music sensitivity (MOR trait)
          SSPS   (6D, RPU-gamma3) <- saddle-shaped preference surface (IC x entropy saddle)
```

---
---

# DAED — Dopamine Anticipation-Experience Dissociation

**Model**: RPU-alpha1-DAED
**Type**: Relay (Depth 0) — reads R3/H3 directly, kernel relay wrapper
**Tier**: alpha (Mechanistic, >90% confidence)
**Output**: 8D per frame (3 layers: E 4D + M 2D + P 2D)
**Phase**: 0a (independent relay, parallel with BCH, HMCE, etc.)
**Status**: IMPLEMENTED (relay wrapper)

---

## 1. Identity

DAED models the temporal-anatomical dissociation between anticipatory dopamine release in the caudate nucleus (wanting) and consummatory dopamine release in the nucleus accumbens (liking). Caudate DA ramps quasi-hyperbolically 15-30s before peak emotion; NAcc DA bursts phasically at the peak moment. DAED is the **F6 relay**: it directly bridges R3/H3 features to C3 cognitive-level reward representations.

The relay wrapper exports: `wanting_index`, `liking_index`, `caudate_activation`, `nacc_activation`.

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Tension level (inverse consonance) for anticipation |
| 2 | **[4]** | sensory_pleasantness | A: Consonance | Direct hedonic signal for consummation |
| 3 | **[7]** | amplitude | B: Dynamics | Energy build-up tracking |
| 4 | **[8]** | loudness | B: Dynamics | Perceptual loudness for intensity progression |
| 5 | **[10]** | spectral_flux | B: Dynamics | Onset detection for peak approach |
| 6 | **[21]** | spectral_change | D: Change | Spectral dynamics for prediction uncertainty |
| 7 | **[22]** | energy_change | D: Change | Crescendo/decrescendo dynamics |
| 8 | **[25:33]** | x_l0l5 | F: Interactions | Foundation x Perceptual coupling for peak timing |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 4D | f01:anticipatory_da, f02:consummatory_da, f03:wanting_index, f04:liking_index | 7 | Dual-pathway: caudate DA ramp (loudness velocity + spectral uncertainty + roughness velocity) vs NAcc DA burst (mean pleasantness + mean loudness). Berridge wanting/liking framework. Salimpoor 2011: caudate r=0.71, NAcc r=0.84. |
| **M** (Temporal) | 2D | dissociation_index, temporal_phase | 7 | dissociation = abs(f01 - f02); phase = f01/(f01+f02+eps). Quantifies anticipation vs consummation phase separation. Mohebi 2024: striatal gradient of reward time horizons. |
| **P** (Present) | 2D | caudate_activation, nacc_activation | 2 | Real-time caudate (anticipatory engagement) and NAcc (consummatory pleasure) activation states. Exported as relay fields to kernel scheduler. |

**Total**: 8D, 16 H3 tuples (L0 + L2)

---

## 4. Output Routing

### 4.1 Internal -> Beliefs

| Output | -> Belief | Type |
|--------|----------|------|
| f03:wanting_index + caudate_activation | -> `wanting` | Core (tau=0.6) |
| f04:liking_index + nacc_activation | -> `hedonic_pleasure` | Appraisal |

### 4.2 External -> Other Functions

| Output | -> Function | -> Purpose |
|--------|-----------|-----------|
| wanting_index | F3 (Attention) | Salience mixer: relay tension |
| liking_index | F5 (Emotion) | Hedonic contribution |
| caudate_activation | Reward computation | Anticipatory reward component |
| nacc_activation | Reward computation | Consummatory reward component |
| DAED relay (RPU) | MORMR, RPEM (siblings) | Cross-relay opioid/RPE modulation |

---

## 5. Brain Regions

| Region | Role | Evidence |
|--------|------|----------|
| Caudate (dorsal striatum) | Anticipatory DA ramp — wanting | Salimpoor 2011 (r=0.71) |
| NAcc (ventral striatum) | Consummatory DA burst — liking | Salimpoor 2011 (r=0.84) |
| VTA | DA neuron source for striatum | Menon & Levitin 2005 |

---

## 6. Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [0,4,7,8,10,21,22,25:33] | 8 feature groups | Consonance, dynamics, change, interactions |
| H3 | 16 tuples | Multi-scale temporal dynamics for anticipation/consummation |

---
---

# MORMR — mu-Opioid Receptor Music Reward

**Model**: RPU-alpha2-MORMR
**Type**: Mechanism (Depth 0) — reads R3/H3 directly
**Tier**: alpha (Mechanistic, >90% confidence)
**Output**: 7D per frame (4 layers: E 4D + M 1D + P 1D + F 1D)
**Phase**: 1 (F6 reward models)
**Status**: PENDING

---

## 1. Identity

MORMR models endogenous mu-opioid receptor (MOR) activation during musical pleasure. Sustained consonant, warm, pleasant music drives tonic opioid release; peak emotional moments trigger phasic MOR activation (chills/frisson). NAcc shows strongest music-induced MOR activation. Baseline MOR tone modulates the strength of pleasure-BOLD coupling across brain regions (d=1.16).

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Consonance quality (inverse) for pleasure |
| 2 | **[4]** | sensory_pleasantness | A: Consonance | Direct hedonic signal |
| 3 | **[7]** | amplitude | B: Dynamics | Peak magnitude for chills intensity |
| 4 | **[8]** | loudness | B: Dynamics | Pleasure intensity level |
| 5 | **[12]** | warmth | C: Timbre | Timbral richness for aesthetic quality |
| 6 | **[13]** | brightness | C: Timbre | Spectral character for timbre recognition |
| 7 | **[22]** | energy_change | D: Change | Dynamic modulation for expressive intensity |
| 8 | **[33:41]** | x_l4l5 | G: Interactions | Sustained pleasure (Derivatives x Perceptual) |
| 9 | **[41:49]** | x_l5l7 | H: Interactions | Beauty coupling (Perceptual x Crossband) |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 4D | f01:opioid_release, f02:chills_count, f03:nacc_binding, f04:reward_sensitivity | 7 | Tonic MOR from sustained pleasantness/warmth; phasic MOR at peak amplitude + beauty coupling. NAcc binding = opioid + pleasantness velocity. Sensitivity = f01*f02 interaction. Putkinen 2025: d=4.8. |
| **M** (Temporal) | 1D | opioid_tone | 5 | sigma(0.5*f01 + 0.5*f02). Integrated tonic+phasic opioid system state. Slower pharmacokinetics than dopamine. |
| **P** (Present) | 1D | current_opioid_state | 3 | Real-time MOR activity with tau_decay=5.0s (slower than DAED tau=3.0s). Feeds reward hedonic component. |
| **F** (Forecast) | 1D | chills_onset_pred | 0 | 2-5s forward prediction of chills from rising f01 trajectory + beauty coupling entropy. |

**Total**: 7D, 15 H3 tuples (L0 + L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| current_opioid_state + opioid_tone | -> `opioid_pleasure` | Appraisal |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| NAcc (ventral striatum) | Strongest MOR activation during music |
| OFC | Opioid-mediated hedonic evaluation |
| Amygdala | Emotional tagging of opioid pleasure |
| Thalamus | Opioid relay to cortex |
| VTA / SN | DA-opioid interaction |

5+ papers: Putkinen 2025 (PET, d=4.8), Salimpoor 2011, Mas-Herrero 2014.

---
---

# RPEM — Reward Prediction Error in Music

**Model**: RPU-alpha3-RPEM
**Type**: Mechanism (Depth 0) — reads R3/H3 directly
**Tier**: alpha (Mechanistic, >90% confidence)
**Output**: 8D per frame (3 layers: E 4D + M 2D + P 2D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

RPEM models the reward prediction error crossover pattern: surprise x liked = VS activation (positive RPE), surprise x disliked = VS deactivation (negative RPE). Information content (IC) and liking interact multiplicatively to produce signed RPE signals that drive reward learning. The RPE magnitude drives model updating and attention regardless of valence.

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Tension for liking signal and negative RPE |
| 2 | **[4]** | sensory_pleasantness | A: Consonance | Hedonic valence for liking signal |
| 3 | **[8]** | loudness | B: Dynamics | Salience encoding for attention capture |
| 4 | **[10]** | spectral_flux | B: Dynamics | Musical deviation / event detection |
| 5 | **[21]** | spectral_change | D: Change | Spectral surprise (IC proxy) |
| 6 | **[24]** | concentration_change | D: Change | Concentration shift / uncertainty signal |
| 7 | **[25:33]** | x_l0l5 | F: Interactions | Prediction generation |
| 8 | **[33:41]** | x_l4l5 | G: Interactions | Surprise x context RPE computation |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 4D | f01:surprise_signal, f02:liking_signal, f03:positive_rpe, f04:negative_rpe | 8 | IC from spectral entropy + change; liking from pleasantness + inverse roughness. Positive RPE = f01*f02; negative RPE = f01*(1-f02). Gold 2023: VS crossover d=1.07. |
| **M** (Temporal) | 2D | rpe_magnitude, vs_response | 5 | magnitude = max(f03, f04); vs_response = clamp(f03-f04+0.5, 0, 1). Unsigned + signed RPE. |
| **P** (Present) | 2D | current_rpe, vs_activation_state | 2 | Real-time signed RPE centered at 0.5. VS activation = sigma(0.5*current_rpe + 0.5*rpe_magnitude). Feeds reward learning and precision engine. |

**Total**: 8D, 15 H3 tuples (L0 + L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| current_rpe + vs_response | -> `reward_prediction_error` | Core (tau=0.35) |
| vs_activation_state | -> `striatal_engagement` | Appraisal |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Ventral Striatum (NAcc) | RPE crossover: up for liked surprise, down for disliked |
| R STG | Surprise magnitude (d=1.22) |
| Amygdala | IC x liking interaction |
| Hippocampus | Uncertainty x surprise interaction |

4+ papers: Gold 2023 (d=1.07), Cheung 2019, Gold 2019.

---
---

# IUCP — Inverted-U Complexity Preference

**Model**: RPU-beta1-IUCP
**Type**: Mechanism (Depth 1) — reads RPEM, DAED outputs
**Tier**: beta (70-90% confidence)
**Output**: 6D per frame (3 layers: E 4D + P 1D + F 1D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

IUCP models the Berlyne (1971) inverted-U complexity-preference function. Pleasure = f(IC, entropy), where both IC and entropy show independent quadratic (concave-down) relationships with liking. Medium complexity maximizes pleasure. The IC x entropy interaction creates a saddle-shaped surface where high entropy shifts optimal IC downward.

**Reads**: R3/H3 directly + RPEM prediction error context
**Feeds**: DAED (preference drives DA anticipation), reward computation

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Harmonic complexity / dissonance level |
| 2 | **[4]** | sensory_pleasantness | A: Consonance | Hedonic signal for pleasantness baseline |
| 3 | **[8]** | loudness | B: Dynamics | Structural salience / perceptual weight |
| 4 | **[21]** | spectral_change | D: Change | Information content (surprise level) |
| 5 | **[24]** | concentration_change | D: Change | Spectral uncertainty / timbral complexity |
| 6 | **[33:41]** | x_l4l5 | G: Interactions | IC x entropy surface / preference computation |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 4D | f01:ic_liking_curve, f02:entropy_liking_curve, f03:ic_entropy_interaction, f04:optimal_complexity | 14 | Quadratic transforms 4*x*(1-x) on IC and entropy, peaking at 0.5. Product f01*f02 for saddle interaction. Gold 2019: IC R2=26.3%, entropy R2=19.1%. |
| **P** (Present) | 1D | current_preference_state | 3 | sigma(0.5*f01 + 0.5*f02). Unified preference signal. High = music in optimal complexity zone. |
| **F** (Forecast) | 1D | optimal_zone_pred | 4 | sigma(0.5*f04 + 0.5*f03). Projects optimal complexity zone forward. tau_decay=2.0s. |

**Total**: 6D, 21 H3 tuples (L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| current_preference_state + optimal_zone_pred | -> `complexity_preference` | Appraisal |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| VS (NAcc) | Reward for optimal complexity (Gold 2023b: F(1,22)=4.83, p=0.039) |
| Amygdala + Hippocampus | IC x entropy interaction (Cheung 2019: d=3.8-4.16) |
| STG | IC encoding (Gold 2023a) |

3+ papers: Gold 2019 (N=43+27), Cheung 2019 (N=39+40), Gold 2023b (N=24).

---
---

# MCCN — Musical Chills Cortical Network

**Model**: RPU-beta2-MCCN
**Type**: Mechanism (Depth 1) — reads DAED, MORMR outputs
**Tier**: beta (70-90% confidence)
**Output**: 7D per frame (3 layers: E 4D + P 2D + F 1D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

MCCN models the cortical chills network: right prefrontal theta increase simultaneous with central/temporal theta decrease, combined with physiological arousal (beta/alpha ratio increase). Source localization reveals OFC, bilateral insula, SMA, and bilateral STG co-activation during chills. Peak chills magnitude requires co-activation of reward (theta prefrontal) and arousal.

**Reads**: DAED anticipatory DA, MORMR opioid signals
**Feeds**: Reward chills component, salience

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Tension level (inverse chills) |
| 2 | **[7]** | amplitude | B: Dynamics | Peak intensity proxy / crescendo detection |
| 3 | **[8]** | loudness | B: Dynamics | Peak pleasure intensity / chills trigger |
| 4 | **[9]** | rms_energy | B: Dynamics | Arousal correlate / physiological activation |
| 5 | **[21]** | spectral_change | D: Change | Musical deviation / surprise events |
| 6 | **[22]** | energy_change | D: Change | Dynamic shift / crescendo-decrescendo |
| 7 | **[25:33]** | x_l0l5 | F: Interactions | Theta oscillation proxy / low-band correlations |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 4D | f01:theta_prefrontal, f02:theta_central, f03:arousal_index, f04:chills_magnitude | 16 | Theta pathway: RPF theta up (F(2,15)=3.28) + central theta down (F(2,15)=5.88). Arousal: beta/alpha ratio proxy (F(2,15)=4.77). Chills = peak_loudness * f01*f03 co-activation. Chabin 2020. |
| **P** (Present) | 2D | network_state, theta_pattern | 6 | network = sigma(0.5*f04 + 0.5*f03); theta = sigma(0.5*f01 + 0.5*f02). Distributed cortical activation vs EEG biomarker. |
| **F** (Forecast) | 1D | chills_onset_pred | 6 | 1-3s chills onset prediction from amplitude buildup + energy velocity + spectral surprise. tau_decay=3.0s. |

**Total**: 7D, 28 H3 tuples (L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| network_state + theta_pattern | -> `chills_response` | Core (tau=0.3) |
| chills_onset_pred | -> `chills_anticipation` | Anticipation |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| OFC | Theta source, reward evaluation (p < 1e-05) |
| Bilateral Insula | Interoceptive chills awareness (p < 1e-06) |
| SMA | Motor preparation for chills (p < 1e-07) |
| Bilateral STG | Auditory processing co-activation |
| R Prefrontal Cortex | Theta increase signature |

3+ papers: Chabin 2020 (HD-EEG, N=18), Putkinen 2025 (PET), Salimpoor 2011 (PET).

---
---

# MEAMR — Music-Evoked Autobiographical Memory Reward

**Model**: RPU-beta3-MEAMR
**Type**: Mechanism (Depth 1) — reads DAED, MEAMN (F4) outputs
**Tier**: beta (70-90% confidence)
**Output**: 6D per frame (3 layers: E 4D + P 1D + F 1D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

MEAMR models the reward pathway for music-evoked autobiographical memory (MEAM). Familiarity activates pre-SMA/IFG/STG; autobiographical salience activates dMPFC (BA 8/9); positive affect integrates via vACC + SN/VTA. Familiarity is prerequisite for autobiographical salience, which feeds positive affect. Self-selected music boosts nostalgia.

**Reads**: DAED DA signals, MEAMN memory state (F4 cross-function)
**Feeds**: Kernel familiarity, reward nostalgia component

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[4]** | sensory_pleasantness | A: Consonance | Familiarity cue / tonal recognition |
| 2 | **[8]** | loudness | B: Dynamics | Familiarity dynamics |
| 3 | **[12]** | warmth | C: Timbre | Timbre familiarity |
| 4 | **[13]** | spectral_centroid | C: Timbre | Brightness / tonal space tracking |
| 5 | **[21]** | spectral_change | D: Change | Structural complexity |
| 6 | **[22]** | energy_change | D: Change | Temporal patterns |
| 7 | **[41:49]** | x_l5l7 | H: Interactions | Memory-structure binding |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 4D | f01:familiarity_index, f02:autobio_salience, f03:dmpfc_tracking, f04:positive_affect | 14 | Hierarchical: familiarity (pleasantness trend + warmth) -> autobio salience (memory-structure trend + f01) -> dMPFC tracking (centroid + pleasantness + structural entropy) -> positive affect (f02*f01). Janata 2009: pre-SMA Z=5.37, dMPFC P<0.001. |
| **P** (Present) | 1D | memory_activation_state | 3 | sigma(0.5*f02 + 0.5*f01). Unified memory activation. tau_decay=10.0s (extended retrieval). |
| **F** (Forecast) | 1D | nostalgia_response_pred | 4 | sigma(0.5*f04 + 0.5*f02). Predicted nostalgia from positive affect + autobio salience. tau_decay=10.0s. |

**Total**: 6D, 21 H3 tuples (L0 + L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| memory_activation_state + nostalgia_response_pred | -> `memory_reward` | Appraisal |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| dMPFC (BA 8/9) | Autobiographical salience (P < 0.001, FDR P < 0.025) |
| pre-SMA | Familiarity detection (Z = 5.37) |
| IFG | Familiarity processing (Z = 4.81) |
| vACC | Positive affect integration |
| SN / VTA | Reward activation from familiar music |
| Bilateral STG | Musical recognition |

3+ papers: Janata 2009 (fMRI, N=13), Salimpoor 2011 (PET, N=8).

---
---

# SSRI — Social Synchrony Reward Integration

**Model**: RPU-beta4-SSRI
**Type**: Mechanism (Depth 1) — reads DAED, RPEM outputs
**Tier**: beta (Bridging, 70-90% confidence)
**Output**: 11D per frame (4 layers: E 5D + M 2D + P 2D + F 2D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

SSRI models the reward amplification from interpersonal musical synchrony. Joint music-making activates caudate with synchrony quality; social bonding increases prefrontal neural synchronization (d=0.85); beta-endorphin release from sustained coordinated activity mediates social bonding and pain threshold elevation. Group music-making amplifies hedonic reward by 1.3-1.8x vs solo listening.

**Reads**: DAED DA anticipation, RPEM prediction error for social RPE
**Feeds**: Kernel reward social component, F9 Social

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
| **E** (Extraction) | 5D | f01:synchrony_reward, f02:social_bonding_index, f03:group_flow_state, f04:entrainment_quality, f05:collective_pleasure | 12 | Synchrony reward from onset periodicity + pleasantness + coupling trend. Bonding builds on synchrony over 5s LTI. Flow = f01 + dynamics. Entrainment = fast-scale onset alignment (100-500ms). Collective pleasure = f02 + f03 + pleasantness. |
| **M** (Temporal) | 2D | social_prediction_error, synchrony_amplification | 0 | SPE = f04 - expected coordination (from beliefs). Amplification = 1.0 + f01*(f04+f02), range [1.0, ~3.0]. kappa_social=0.60. |
| **P** (Present) | 2D | prefrontal_coupling, endorphin_proxy | 2 | Prefrontal = sigma(0.4*f04 + 0.3*coupling_500ms). Ni 2024: rDLPFC sync d=0.85. Endorphin = sigma(0.4*f02 + 0.3*f03 + 0.3*coupling_5s). tau_endorphin=30.0s. |
| **F** (Forecast) | 2D | bonding_trajectory_pred, flow_sustain_pred | 2 | Bonding direction from f02 + coupling trend + loudness trend. tau_bonding=120.0s. Flow sustainability from f03 + f04 + arousal. |

**Total**: 11D, 16 H3 tuples (L0 + L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| synchrony_reward + collective_pleasure | -> `social_reward` | Core (tau=0.5) |
| bonding_trajectory_pred + flow_sustain_pred | -> `social_engagement` | Anticipation |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Caudate | Synchrony-dependent activation (Kokal 2011) |
| rDLPFC / rTPJ | Inter-brain prefrontal sync (Ni 2024, d=0.85) |
| NAcc | Social reward amplification |
| VTA | Endorphin-DA interaction for social bonding |

4+ papers: Kokal 2011, Ni 2024 (N=528), Dunbar 2012, Wohltjen 2023.

---
---

# LDAC — Liking-Dependent Auditory Cortex

**Model**: RPU-gamma1-LDAC
**Type**: Mechanism (Depth 2) — reads IUCP, RPEM, DAED outputs
**Tier**: gamma (50-70% confidence)
**Output**: 6D per frame (3 layers: E 4D + P 1D + F 1D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

LDAC models the pleasure-dependent modulation of auditory cortex processing. Right STG continuously tracks moment-to-moment liking; pleasure gates sensory gain (top-down reward-to-perception pathway); high IC combined with disliking produces maximal sensory suppression. This demonstrates that sensory processing is not passive but pleasure-modulated.

**Reads**: IUCP preference state, RPEM RPE signals, DAED DA
**Feeds**: F3 Attention (sensory gain), reward sensory component

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[4]** | sensory_pleasantness | A: Consonance | Moment-to-moment pleasure |
| 2 | **[8]** | loudness | B: Dynamics | Sensory salience for gating |
| 3 | **[10]** | spectral_flux | B: Dynamics | Deviation detection |
| 4 | **[21]** | spectral_change | D: Change | IC for IC x liking interaction |
| 5 | **[25:33]** | x_l0l5 | F: Interactions | Auditory gating proxy |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 4D | f01:stg_liking_coupling, f02:pleasure_gating, f03:ic_liking_interaction, f04:moment_to_moment | 12 | STG-liking coupling from fast+smoothed pleasantness. Pleasure gates loudness response. IC x liking: ic*(1-f01) captures suppression for disliked surprise. Gold 2023a: R STG t(23)=2.56; IC x liking t(23)=2.92. |
| **P** (Present) | 1D | stg_modulation_state | 0 | sigma(0.5*f04 + 0.5*f02). Present reward-driven sensory processing state. tau_decay=0.5s. |
| **F** (Forecast) | 1D | sensory_gating_pred | 0 | sigma(0.5*f01 + 0.5*f03). Predicted near-future gating state for proactive attention allocation. |

**Total**: 6D, 12 H3 tuples (L0 + L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| stg_modulation_state + sensory_gating_pred | -> `sensory_reward_gate` | Appraisal |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| R STG | Moment-to-moment liking tracking (t(23)=2.56) |
| NAcc | STG-NAcc functional connectivity (Martinez-Molina 2016) |
| Auditory Cortex | IC x liking interaction for gating |

3+ papers: Gold 2023a (fMRI, N=24), Martinez-Molina 2016, Cheung 2019.

---
---

# IOTMS — Individual Opioid Tone Music Sensitivity

**Model**: RPU-gamma2-IOTMS
**Type**: Mechanism (Depth 2) — reads MORMR, DAED outputs
**Tier**: gamma (50-70% confidence)
**Output**: 5D per frame (2 layers: E 4D + P 1D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

IOTMS models individual differences in music reward sensitivity driven by baseline mu-opioid receptor (MOR) availability. Higher trait-level MOR tone produces steeper pleasure-BOLD coupling slopes. This is a trait-level model: outputs change slowly and represent stable individual differences rather than time-varying event signals. Smallest model in the entire C3 system (5D total).

**Reads**: MORMR opioid signals, DAED DA for coupling
**Feeds**: All intra-unit models as sensitivity modulator (MORMR, DAED, RPEM, MCCN, LDAC)

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Consonance quality for MOR baseline |
| 2 | **[4]** | sensory_pleasantness | A: Consonance | Primary pleasure signal |
| 3 | **[8]** | loudness | B: Dynamics | Modulates pleasure-BOLD slope |
| 4 | **[14]** | tristimulus1 | C: Timbre | Harmonic structure quality |
| 5 | **[33:41]** | x_l4l5 | G: Interactions | Sustained opioid-perceptual coupling |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 4D | f01:mor_baseline_proxy, f02:pleasure_bold_slope, f03:reward_propensity, f04:music_reward_index | 12 | Cascaded trait estimation: MOR baseline (pleasantness + inverse roughness skew) -> pleasure-BOLD slope (f01 + loudness) -> reward propensity (f02 + sustained coupling) -> composite index (f03 + coupling trend + tristimulus). Putkinen 2025: d=1.16. |
| **P** (Present) | 1D | individual_sensitivity_state | 0 | sigma(0.5*f01 + 0.5*f03). Trait-level sensitivity: neurochemical (MOR) + behavioral (propensity). |

**Total**: 5D, 12 H3 tuples (L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| individual_sensitivity_state | -> `music_reward_sensitivity` | Appraisal |
| mor_baseline_proxy | -> `opioid_trait` | Anticipation |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Insula | Pleasure-BOLD coupling (Putkinen 2025) |
| ACC | MOR-mediated pleasure modulation |
| SMA | Pleasure-BOLD slope |
| STG | Auditory reward sensitivity |
| NAcc | MOR binding for music reward |
| Thalamus | Opioid relay |

3+ papers: Putkinen 2025 (PET, d=1.16), Mas-Herrero 2014 (BMRQ R2=0.30), Martinez-Molina 2016 (R2=0.40).

---
---

# SSPS — Saddle-Shaped Preference Surface

**Model**: RPU-gamma3-SSPS
**Type**: Mechanism (Depth 2) — reads IUCP, RPEM outputs
**Tier**: gamma (50-70% confidence)
**Output**: 6D per frame (3 layers: E 4D + P 1D + F 1D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

SSPS models the saddle-shaped preference surface in IC x entropy space. Two distinct optimal zones exist: (1) high entropy + low IC (predictable events in uncertain contexts) and (2) low entropy + medium IC (moderate surprise in stable contexts). The saddle trough between zones is the preference minimum. SSPS refines IUCP's inverted-U with the full saddle topology.

**Reads**: IUCP inverted-U preference, RPEM IC-level for RPE
**Feeds**: DAED (peak proximity drives DA), precision engine, IMU learning target

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Harmonic complexity for entropy axis |
| 2 | **[4]** | sensory_pleasantness | A: Consonance | Hedonic quality for peak proximity |
| 3 | **[8]** | loudness | B: Dynamics | Perceptual salience / attention weight |
| 4 | **[21]** | spectral_change | D: Change | IC proxy (surprise level) |
| 5 | **[24]** | concentration_change | D: Change | Entropy proxy (uncertainty level) |
| 6 | **[25:33]** | x_l0l5 | F: Interactions | Context variability for entropy |
| 7 | **[33:41]** | x_l4l5 | G: Interactions | IC-perceptual coupling for saddle |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 4D | f01:ic_value, f02:entropy_value, f03:saddle_position, f04:peak_proximity | 14 | IC from 75ms surprise + 500ms velocity. Entropy from concentration + roughness variability + context variability. Saddle = max(zone1, zone2): zone1=f02*(1-f01), zone2=(1-f02)*4*f01*(1-f01). Peak proximity = f03 + pleasantness smoothness. Cheung 2019: beta=-0.124, p=0.000246. |
| **P** (Present) | 1D | surface_position_state | 0 | sigma(0.5*f03 + 0.5*f04). Real-time surface position. Near 1.0 = peak; near 0.5 = trough. tau=2.0s. |
| **F** (Forecast) | 1D | optimal_zone_pred | 0 | sigma(0.5*f04 + 0.5*saddle_value). Predicted movement toward/away from optimal peak. |

**Total**: 6D, 14 H3 tuples (L0 + L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| surface_position_state | -> `preference_surface` | Appraisal |
| optimal_zone_pred | -> `preference_trajectory` | Anticipation |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Bilateral Amygdala / Hippocampus | IC x entropy interaction (Cheung 2019) |
| Auditory Cortex | IC x entropy (bilateral AC) |
| NAcc | Uncertainty encoding (beta=0.242) |
| VS | RPE-like surprise x liking (Gold 2023) |

3+ papers: Cheung 2019 (N=39+40), Gold 2019 (N=43+27), Gold 2023 (R2=0.496).

---
---

## Summary Statistics

### Output Dimensions by Model

| Model | Unit | Tier | D | E-Layer | M-Layer | P-Layer | F-Layer | H3 |
|-------|------|------|---|---------|---------|---------|---------|-----|
| DAED | RPU | alpha | 8 | 4 | 2 | 2 | 0 | 16 |
| MORMR | RPU | alpha | 7 | 4 | 1 | 1 | 1 | 15 |
| RPEM | RPU | alpha | 8 | 4 | 2 | 2 | 0 | 15 |
| IUCP | RPU | beta | 6 | 4 | 0 | 1 | 1 | 21 |
| MCCN | RPU | beta | 7 | 4 | 0 | 2 | 1 | 28 |
| MEAMR | RPU | beta | 6 | 4 | 0 | 1 | 1 | 21 |
| SSRI | RPU | beta | 11 | 5 | 2 | 2 | 2 | 16 |
| LDAC | RPU | gamma | 6 | 4 | 0 | 1 | 1 | 12 |
| IOTMS | RPU | gamma | 5 | 4 | 0 | 1 | 0 | 12 |
| SSPS | RPU | gamma | 6 | 4 | 0 | 1 | 1 | 14 |
| **TOTAL** | | | **70** | **41** | **7** | **14** | **8** | **170** |

### Tier Gradient

| Tier | Count | Avg D | Avg H3 |
|------|-------|-------|--------|
| alpha | 3 | 7.7 | 15.3 |
| beta | 4 | 7.5 | 21.5 |
| gamma | 3 | 5.7 | 12.7 |

Clear tier gradient in dimensionality for gamma models (5-6D). Alpha models are the largest (7-8D) with the core dopamine/opioid/RPE mechanisms. Beta models show the most H3 demand variation (MCCN at 28 is the highest F6 model). SSRI at 11D is the largest single F6 model due to its 4-layer social coordination architecture.

### Brain Region Convergence

**NAcc / Ventral Striatum** is the convergence hub: mentioned in DAED, MORMR, RPEM, IUCP, MCCN, SSRI, LDAC, IOTMS, SSPS -- 9 of 10 models.
**STG / Auditory Cortex**: mentioned in RPEM, MCCN, MEAMR, LDAC, IOTMS -- 5 of 10 models.
**Amygdala / Hippocampus**: mentioned in MORMR, RPEM, IUCP, SSPS -- 4 of 10 models.
**OFC / vmPFC**: mentioned in MORMR, MCCN -- 2 of 10 models.
**Caudate (dorsal striatum)**: mentioned in DAED, SSRI -- 2 of 10 models.

### Unit Distribution

| Unit | Count | Models |
|------|-------|--------|
| RPU (Reward Processing Unit) | 10 | DAED, MORMR, RPEM, IUCP, MCCN, MEAMR, SSRI, LDAC, IOTMS, SSPS |

F6 is exclusively RPU (10/10 models), reflecting that reward and motivation is a unified reward processing function. All models share the same computational unit, distinguished only by depth tier (alpha/beta/gamma).

### Layer Distribution

| Layer Type | Models With | Total Dims |
|------------|-------------|------------|
| E (Extraction) | 10/10 | 41D |
| M (Temporal Integration) | 3/10 (DAED, MORMR, SSRI) | 7D |
| P (Cognitive Present) | 10/10 | 14D |
| F (Forecast) | 7/10 (not DAED, RPEM, IOTMS) | 8D |

All models have E and P layers. Only 3 models require dedicated M-layers for temporal integration (DAED dissociation, MORMR opioid tone, SSRI social prediction error). IOTMS is the only gamma model without a Forecast layer, reflecting its trait-level (stable) nature.
