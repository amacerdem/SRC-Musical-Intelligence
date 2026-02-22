# F8 Mechanism Orchestrator — Learning and Plasticity

**Function**: F8 Learning & Plasticity
**Models covered**: 6/6 primary — 0 IMPLEMENTED + 6 PENDING
**Total F8 mechanism output**: 67D (10D + 10D + 11D + 13D + 11D + 12D)
**Beliefs**: 14 (from EDNR, TSCP, CDMR, SLEE, ESME, ECT)
**H3 demands**: 92 tuples (all pending)
**Architecture**: Depth-ordered — 1 alpha (Depth 0) -> 3 beta (Depth 1) -> 2 gamma (Depth 2)

---

## Model Pipeline (Depth Order)

```
R3 (97D) ---+--------------------------------------------
H3 tuples --+
            |
Depth 0:  EDNR   (10D, NDU-alpha3)  <- expertise-dependent network reorganization (within/between connectivity)
            |
            |
Depth 1:  TSCP   (10D, SPU-beta2)   <- timbre-specific cortical plasticity (N1m enhancement)
          CDMR   (11D, NDU-beta2)   <- context-dependent mismatch response (MMN context modulation)
          SLEE   (13D, NDU-beta3)   <- statistical learning expertise enhancement (irregularity detection)
            |
            |
Depth 2:  ESME   (11D, SPU-gamma2) <- expertise-specific MMN enhancement (domain-specific gradient)
          ECT    (12D, NDU-gamma3) <- expertise compartmentalization trade-off (within/between ratio)
```

---
---

# EDNR — Expertise-Dependent Network Reorganization

**Model**: NDU-alpha3-EDNR
**Type**: Mechanism (Depth 0) — reads R3/H3 directly
**Tier**: alpha (Mechanistic, >90% confidence)
**Output**: 10D per frame (4 layers: E 4D + M 2D + P 2D + F 2D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

EDNR models the expertise-dependent network reorganization observed in musicians. Musical training drives compartmentalization: within-network connectivity increases while between-network connectivity decreases. Paraskevopoulos 2022 found musicians show 106 within-network edges vs 192 between-network edges in non-musicians (p<0.001 FDR). The compartmentalization ratio (within/between) is the core metric of expertise-dependent network topology.

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[25:33]** | x_l0l5 | F: Interactions | Within-network coupling proxy for intra-network binding |
| 2 | **[33:41]** | x_l4l5 | G: Interactions | Cross-network coupling proxy for inter-network binding |
| 3 | **[14]** | tonalness | C: Timbre | Processing complexity indicator for expertise signature |
| 4 | **[4]** | sensory_pleasantness | A: Consonance | Processing quality proxy for expertise refinement |
| 5 | **[16]** | spectral_flatness | C: Timbre | Stimulus regularity proxy for processing complexity |
| 6 | **[8]** | loudness | B: Dynamics | Stimulus complexity proxy for processing demands |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 4D | f01:within_connectivity, f02:between_connectivity, f03:compartmentalization, f04:expertise_signature | 8 | Within from coupling mean/periodicity 1s; between from cross-coupling mean/entropy 1s; compartmentalization = f01/(f02+eps); expertise from tonalness+pleasantness mean 1s. Paraskevopoulos 2022: 106 vs 192 edges. |
| **M** (Temporal) | 2D | network_architecture, compartmentalization_idx | 4 | Architecture = 0.5*f01 + 0.5*f02; compartmentalization carries forward f03 ratio. Cui 2025: 1yr training does NOT change WM — slow structural constraint. |
| **P** (Cognitive Present) | 2D | current_compartm, network_isolation | 2 | Real-time compartmentalization from normalized f03 + within mean; isolation from boundary maintenance. Moller 2021: local CT correlations only in musicians. |
| **F** (Forecast) | 2D | optimal_config_pred, processing_efficiency | 2 | Config prediction from f01+f04; efficiency from network state + loudness entropy. Papadaki 2023: network strength rho=0.36. |

**Total**: 10D, 16 H3 tuples (L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| current_compartm + network_isolation | -> `network_compartmentalization` | Appraisal |
| optimal_config_pred + processing_efficiency | -> `expertise_efficiency` | Anticipation |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Bilateral STG / Planum Temporale | Within-network connectivity hub (Leipold 2021: pFWE<0.05) |
| IFG (area 47m) | Between-network hub; highest degree node (Paraskevopoulos 2022: Hedges' g=-1.09) |
| Heschl's Gyrus | Cortical thickness correlations (Moller 2021: FDR<10%) |
| SMG / vmPFC | Expertise signature (Papadaki 2023: Cohen's d=0.70) |

4+ papers: Paraskevopoulos 2022 (MEG), Leipold et al. 2021 (n=153), Moller et al. 2021, Papadaki et al. 2023, Cui et al. 2025, Porfyri et al. 2025.

---

## 6. Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [25:33,33:41,14,4,16,8] | 6 feature groups | Coupling, timbre, consonance, dynamics |
| H3 | 16 tuples | Multi-scale coupling, tonalness, pleasantness, flatness, loudness dynamics |

---
---

# TSCP — Timbre-Specific Cortical Plasticity

**Model**: SPU-beta2-TSCP
**Type**: Mechanism (Depth 1) — reads R3/H3 directly
**Tier**: beta (70-90% confidence)
**Output**: 10D per frame (4 layers: E 3D + M 1D + P 3D + F 3D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

TSCP models the timbre-specific cortical plasticity demonstrated by Pantev et al. 2001. Musical training produces instrument-specific N1m enhancement following a double dissociation (F(1,15)=28.55, p=.00008): violinists show enhanced responses to violin tones but not trumpet tones, and vice versa. The enhancement function captures both trained instrument response strength and timbre specificity selectivity. Plasticity locus is cortical not subcortical (Whiteford 2025: d=-0.064, BF=0.13).

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[18:21]** | tristimulus1/2/3 | C: Timbre | Harmonic envelope signature for instrument identity |
| 2 | **[5]** | inharmonicity | A: Consonance | Instrument character (piano=high, violin=low) |
| 3 | **[14]** | tonalness | C: Timbre | Harmonic-to-noise ratio for pitch clarity |
| 4 | **[12]** | warmth | C: Timbre | Low-frequency spectral balance for timbre contrast |
| 5 | **[13]** | sharpness | C: Timbre | High-frequency energy for brightness proxy |
| 6 | **[41:47]** | x_l5l7 (partial) | H: Interactions | Consonance-timbre coupling for binding strength |
| 7 | **[24]** | timbre_change | D: Change | Temporal timbre flux for plasticity trigger |
| 8 | **[17]** | spectral_autocorrelation | C: Timbre | Harmonic periodicity for identity coherence |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 3D | f01:trained_timbre_response, f02:timbre_specificity, f03:plasticity_magnitude | 6 | Trained response from tristimulus balance + harmonic purity; specificity from warmth/sharpness + stability; plasticity = f01*timbre_change_std. Pantev 2001: double dissociation F(1,15)=28.55. |
| **M** (Temporal) | 1D | enhancement_function | 0 | E(t) = f01*f02 multiplicative gating. High only when both trained response AND specificity present. Pantev 2001: trained >> other >> pure tone hierarchy. |
| **P** (Cognitive Present) | 3D | recognition_quality, enhanced_response, timbre_identity | 2 | Template matching quality; enhancement = 0.6*E(t) + 0.4*tonalness; identity binding from tristimulus+inharmonicity+autocorrelation. Bellmann & Asano 2024: ALE L-SMG/HG 4640mm3. |
| **F** (Forecast) | 3D | timbre_continuation, cortical_enhancement_pred, generalization_pred | 4 | Continuation from warmth+tonalness means 46ms; enhancement from f03+timbre_change trend; generalization from recognition+coupling+identity. Halpern 2004: timbre imagery overlaps perception. |

**Total**: 10D, 12 H3 tuples (L0 + L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| enhanced_response + timbre_identity | -> `timbre_plasticity` | Appraisal |
| timbre_continuation + generalization_pred | -> `timbre_prediction` | Anticipation |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Secondary Auditory Cortex | N1m enhancement (Pantev 2001: ECD posterior/lateral to HG) |
| Planum Temporale | Timbre specificity (Bellmann & Asano 2024: ALE R-pSTG/PT 3128mm3) |
| L-SMG / Heschl's Gyrus | Primary timbre processing cluster (4640mm3 ALE) |
| Bilateral pSTG/HG | Plasticity magnitude (Bellmann & Asano 2024: k=18, N=338) |

4+ papers: Pantev et al. 2001, Bellmann & Asano 2024 (ALE), Santoyo et al. 2023, Whiteford et al. 2025, Alluri et al. 2012, Sturm et al. 2014.

---

## 6. Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [18:21,5,14,12,13,41:47,24,17] | 8 feature groups | Timbre, consonance, interactions, change |
| H3 | 12 tuples | Fast spectral envelope, stability, timbre dynamics |

---
---

# CDMR — Context-Dependent Mismatch Response

**Model**: NDU-beta2-CDMR
**Type**: Mechanism (Depth 1) — reads R3/H3 directly
**Tier**: beta (70-90% confidence)
**Output**: 11D per frame (4 layers: E 4D + M 2D + P 3D + F 2D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

CDMR models the context-dependent mismatch response where musical expertise enhances MMN only in complex melodic contexts (Rupp/Hansen 2022: musicians = non-musicians in oddball, but musicians > non-musicians in melodic paradigm). The core finding is that expertise effects emerge when context complexity demands it. Subadditivity of combined deviants indicates integrated rather than additive processing (musicians > non-musicians). Consonance MMN is present in both groups but right-lateralized in musicians (Crespo-Bojorque 2018: F(1,15)=4.95).

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[10]** | spectral_flux | B: Dynamics | Frame-level deviance magnitude for mismatch detection |
| 2 | **[11]** | onset_strength | B: Dynamics | Onset deviation for rhythmic deviance detection |
| 3 | **[23]** | pitch_change | D: Change | Melodic context complexity for context modulation |
| 4 | **[41:49]** | x_l5l6 | H: Interactions | Perceptual-shape coupling for subadditivity |
| 5 | **[21]** | spectral_change | D: Change | Spectral context dynamics for trend computation |
| 6 | **[13]** | brightness | C: Timbre | Tonal context quality for P-layer gating |
| 7 | **[33:41]** | x_l4l5 | G: Interactions | Pattern-feature coupling for binding |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 4D | f01:mismatch_amplitude, f02:context_modulation, f03:subadditivity_index, f04:expertise_effect | 8 | Mismatch from flux+onset at 25ms gamma; context from pitch change at 100ms/1s; subadditivity from binding; expertise = (f01_complex-f01_simple)*indicator. Crespo-Bojorque 2018: p=0.007. Wagner 2018: MMN -0.34uV. |
| **M** (Temporal) | 2D | melodic_expectation, deviance_history | 4 | Expectation EMA of f02 over 2.5s context window; deviance history EMA of f01 with tau=0.4s. Tervaniemi 2022: genre-specific MMN modulation. |
| **P** (Cognitive Present) | 3D | mismatch_signal, context_state, binding_state | 3 | Context-sensitive violation signal; context richness gate for expertise effects; multi-feature integration state. Rupp/Hansen 2022: context-dependent MMR. |
| **F** (Forecast) | 2D | next_deviance, context_continuation | 1 | Deviance prediction from history+context+binding curvature; context continuation from f02+expectation. Fong 2020: MMN as prediction error. |

**Total**: 11D, 16 H3 tuples (L0 + L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| mismatch_signal + context_state | -> `mismatch_sensitivity` | Appraisal |
| next_deviance + context_continuation | -> `deviance_prediction` | Anticipation |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Bilateral Auditory Cortex (A1/STG) | Basic mismatch detection (Wagner 2018: BESA dipole) |
| Anterior Auditory Cortex | Pitch contour tracking gradient (Rupp 2022) |
| Fronto-central Cortex (Fz) | Subadditivity; multi-feature integration (Crespo-Bojorque 2018) |
| Right IFG | ERAN generators; expertise-context interaction (Koelsch) |

4+ papers: Rupp/Hansen 2022 (MEG), Crespo-Bojorque 2018, Wagner 2018, Fong 2020, Tervaniemi 2022, Carbajal & Malmierca 2018.

---

## 6. Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [10,11,23,41:49,21,13,33:41] | 7 feature groups | Dynamics, change, timbre, interactions |
| H3 | 16 tuples | Multi-scale deviance, context, binding, and trend dynamics |

---
---

# SLEE — Statistical Learning Expertise Enhancement

**Model**: NDU-beta3-SLEE
**Type**: Mechanism (Depth 1) — reads R3/H3 directly
**Tier**: beta (70-90% confidence)
**Output**: 13D per frame (4 layers: E 4D + M 3D + P 3D + F 3D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

SLEE models the expertise-dependent enhancement of statistical learning — musicians' superior ability to detect statistical irregularities in auditory streams (Paraskevopoulos 2022: Hedges' g=-1.09, t(23)=-2.815, p<0.05). The model integrates the internal distribution representation, irregularity detection accuracy, multisensory integration, and expertise advantage. IFG area 47m serves as the primary supramodal hub across 5/6 network states. Bridwell 2017 demonstrated 45% amplitude reduction for patterned vs random sequences, reflecting cortical sensitivity to learned statistical structure.

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[7]** | amplitude | B: Dynamics | Amplitude entropy for statistical model estimation |
| 2 | **[8]** | loudness | B: Dynamics | Mean loudness for distribution model |
| 3 | **[10]** | spectral_flux | B: Dynamics | Irregularity detection and variability |
| 4 | **[41:49]** | x_l5l6 | H: Interactions | Cross-modal binding proxy for multisensory integration |
| 5 | **[24]** | pitch_stability | D: Change | Statistical baseline for pattern memory |
| 6 | **[33:41]** | x_l4l5 | G: Interactions | Pattern-feature binding for expertise proxy |
| 7 | **[21]** | spectral_change | D: Change | Spectral dynamics for boundary detection |
| 8 | **[23]** | pitch_change | D: Change | Sequence segmentation for pattern boundary |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 4D | f01:statistical_model, f02:detection_accuracy, f03:multisensory_integration, f04:expertise_advantage | 7 | Statistical model from loudness+amplitude entropy 100ms; detection from flux variability; multisensory from binding 100ms/1s; expertise = f02*indicator. Paraskevopoulos 2022: g=-1.09. Bridwell 2017: 45% reduction. |
| **M** (Temporal) | 3D | exposure_model, pattern_memory, expertise_state | 3 | Exposure EMA of f01; pattern memory EMA with tau=3s; expertise state from binding trend 1s. Billig 2022: hippocampus supports sequence binding. Doelling & Poeppel 2015: training correlates with PLV. |
| **P** (Cognitive Present) | 3D | expectation_formation, cross_modal_binding, pattern_segmentation | 4 | Expectation from f01+exposure; binding from f03+interactions; segmentation from spectral/pitch change dynamics. Fong 2020: Bayesian framework. |
| **F** (Forecast) | 3D | next_probability, regularity_continuation, detection_predict | 4 | Probability from f01+f02; continuation from f01+exposure; detection from segmentation+expertise+binding. Carbajal & Malmierca 2018: predictive coding hierarchy. |

**Total**: 13D, 18 H3 tuples (L0 + L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| expectation_formation + cross_modal_binding | -> `statistical_learning` | Appraisal |
| next_probability + regularity_continuation | -> `regularity_prediction` | Anticipation |
| pattern_segmentation + detection_predict | -> `detection_readiness` | Appraisal |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| IFG (area 47m left) | Supramodal hub; highest degree in 5/6 network states (Paraskevopoulos 2022) |
| Hippocampus | Sequence binding and statistical learning memory (Billig 2022) |
| Left MFG / IFS / Insula | Effective connectivity reorganization (Porfyri 2025) |
| Auditory Cortex | Cortical entrainment at 4 Hz (Bridwell 2017) |

4+ papers: Paraskevopoulos 2022 (MEG), Bridwell 2017, Billig 2022, Fong et al. 2020, Porfyri et al. 2025, Carbajal & Malmierca 2018, Doelling & Poeppel 2015.

---

## 6. Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [7,8,10,41:49,24,33:41,21,23] | 8 feature groups | Dynamics, change, interactions |
| H3 | 18 tuples | Multi-scale loudness, flux, binding, stability, change dynamics |

---
---

# ESME — Expertise-Specific MMN Enhancement

**Model**: SPU-gamma2-ESME
**Type**: Mechanism (Depth 2) — reads R3/H3 directly
**Tier**: gamma (50-70% confidence)
**Output**: 11D per frame (4 layers: E 4D + M 1D + P 3D + F 3D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

ESME models domain-specific mismatch negativity enhancement in musicians, following a gradient pattern (Vuust et al. 2012: jazz > rock > pop > non-musicians for complex rhythmic deviants). Three parallel MMN channels — pitch, rhythm, timbre — are modulated by expertise in the trained domain. The pattern is a gradient rather than a clean dissociation (Martins et al. 2022 constraint: no singer vs instrumentalist P2/P3 difference). The ALE meta-analysis (Criscuolo et al. 2022: k=84, N=3005) confirms bilateral STG + L IFG (BA44) as the expertise-enhanced MMN network.

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[2]** | helmholtz_kang | A: Consonance | Consonance reference for pitch deviance baseline |
| 2 | **[11]** | onset_strength | B: Dynamics | Onset timing for rhythm deviance detection |
| 3 | **[21]** | spectral_change | D: Change | Spectral deviance velocity |
| 4 | **[23]** | pitch_change | D: Change | Pitch deviance velocity |
| 5 | **[33:41]** | x_l4l5 | G: Interactions | Temporal-spectral coupling for emergent deviance |
| 6 | **[18:21]** | tristimulus1/2/3 | C: Timbre | Harmonic energy distribution for spectral envelope |
| 7 | **[24]** | timbre_change | D: Change | Timbre change magnitude |
| 8 | **[12]** | warmth | C: Timbre | Timbre baseline context |
| 9 | **[14]** | tonalness | C: Timbre | Pitch clarity reference |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 4D | f01:pitch_mmn, f02:rhythm_mmn, f03:timbre_mmn, f04:expertise_enhancement | 10 | Pitch from pitch_change velocity+consonance; rhythm from onset+spectral_change velocity+coupling; timbre from timbre_change_std+tristimulus deviation; expertise = alpha*max(f01,f02,f03). Koelsch 1999: 0.75% pitch deviant. Vuust 2012: genre gradient. |
| **M** (Temporal) | 1D | mmn_expertise_function | 0 | Geometric mean: sqrt(f04 * max(f01,f02,f03)). Unified expertise-MMN metric — both expertise and deviance must be present. Yu 2015: MMN as comprehensive regularity indicator. |
| **P** (Cognitive Present) | 3D | pitch_deviance_detection, rhythm_deviance_detection, timbre_deviance_detection | 2 | Domain-specific present-moment detection signals. Pitch from pitch velocity; rhythm from onset deviation; timbre from envelope change. Wagner 2018: pre-attentive harmonic MMN -0.34uV. |
| **F** (Forecast) | 3D | feature_enhancement_pred, expertise_transfer_pred, developmental_trajectory | 0 | Enhancement from unified function+deviance; transfer = 0.3*f01+0.3*f02+0.4*f03; trajectory = 0.6*f04+0.4*unified. Criscuolo 2022 ALE: general enhancement. Bucher 2023: HG 130% larger. |

**Total**: 11D, 12 H3 tuples (L0 + L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| pitch_deviance_detection + rhythm_deviance_detection + timbre_deviance_detection | -> `domain_specific_sensitivity` | Appraisal |
| feature_enhancement_pred + expertise_transfer_pred | -> `expertise_enhancement` | Anticipation |
| developmental_trajectory | -> `plasticity_trajectory` | Anticipation |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Bilateral STG | Expertise-enhanced MMN network (Criscuolo 2022 ALE: k=84, N=3005) |
| L IFG (BA44) | ALE convergence with bilateral STG (Criscuolo 2022) |
| Heschl's Gyrus | 130% larger in professional musicians (Bucher 2023) |
| OFC | Co-activation 25-40ms faster in musicians (Bucher 2023) |
| Putamen / GP / SMA | Percussionist NMR network (Liao 2024) |

5+ papers: Criscuolo et al. 2022 (ALE, k=84, N=3005), Koelsch et al. 1999, Vuust et al. 2012, Tervaniemi 2022, Liao et al. 2024, Wagner 2018, Martins et al. 2022, Bucher et al. 2023, Bonetti et al. 2024.

---

## 6. Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [2,11,21,23,33:41,18:21,24,12,14] | 9 feature groups | Consonance, dynamics, change, timbre, interactions |
| H3 | 12 tuples | Deviance detection at gamma through delta timescales |

---
---

# ECT — Expertise Compartmentalization Trade-off

**Model**: NDU-gamma3-ECT
**Type**: Mechanism (Depth 2) — reads R3/H3 directly
**Tier**: gamma (50-70% confidence)
**Output**: 12D per frame (4 layers: E 4D + M 3D + P 2D + F 3D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

ECT models the expertise compartmentalization trade-off: musical expertise increases within-network efficiency at the cost of reduced between-network connectivity (Paraskevopoulos 2022: 106 within vs 192 between edges). The trade-off ratio captures the cost-benefit balance. Network flexibility (Wu-Chung 2025) moderates whether training produces cognitive benefit. Moller et al. 2021 provided the first behavioral evidence: musicians show reduced benefit from visual cues in audiovisual binding (BCG: t(42.3)=3.06, p=0.004), demonstrating the functional cost of compartmentalization.

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[25:33]** | x_l0l5 | F: Interactions | Intra-network coupling for within-network efficiency |
| 2 | **[33:41]** | x_l4l5 | G: Interactions | Pattern-feature binding for within-network binding |
| 3 | **[41:49]** | x_l5l6 | H: Interactions | Cross-network connectivity for between-network measurement |
| 4 | **[21]** | spectral_change | D: Change | Reconfiguration capacity proxy |
| 5 | **[7]** | amplitude | B: Dynamics | Task demand for efficiency context |
| 6 | **[8]** | loudness | B: Dynamics | Attention allocation context |
| 7 | **[23]** | pitch_change | D: Change | Specialization tracking |
| 8 | **[13]** | brightness | C: Timbre | Tonal adaptation for flexibility context |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 4D | f01:within_efficiency, f02:between_reduction, f03:trade_off_ratio, f04:flexibility_index | 10 | Within from coupling+binding means 1s; between from cross-network mean+entropy 1s; ratio = f01/(f02+eps) clamped [0,10]; flexibility from reconfig 100ms+speed 125ms. Paraskevopoulos 2022: 106 vs 192 edges. Wu-Chung 2025: baseline flexibility. |
| **M** (Temporal) | 3D | training_history, network_state, task_memory | 2 | Training from binding trend 1s; network = 0.5*f01+0.5*(1-f02); task memory from amplitude entropy EMA 500ms. Leipold 2021: graded expertise effects. |
| **P** (Cognitive Present) | 2D | within_binding, network_isolation | 4 | Within-binding from coupling+variability+binding at 100ms; isolation from cross-network binding+variability+inverted flexibility. Papadaki 2023: efficiency correlates with performance. |
| **F** (Forecast) | 3D | transfer_limit, efficiency_opt, flexibility_recovery | 2 | Transfer = 0.5*f02+0.5*(1-f04); efficiency from within_binding+training; recovery from f04+task_memory+isolation. Moller 2021: BCG behavioral cost. Wu-Chung 2025: recoverable flexibility. |

**Total**: 12D, 18 H3 tuples (L0 + L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| within_binding + network_isolation | -> `compartmentalization_state` | Appraisal |
| transfer_limit + flexibility_recovery | -> `transfer_capacity` | Anticipation |
| efficiency_opt | -> `specialization_trajectory` | Anticipation |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| IFG (area 47m) | Highest-degree supramodal hub (Paraskevopoulos 2022) |
| Bilateral STG | Within-network connectivity (Leipold 2021) |
| Heschl's Gyrus | Localized CT correlations in musicians (Moller 2021) |
| IFOF (white matter) | Structural connectivity for audiovisual binding (Moller 2021: FA cluster p<0.001) |

4+ papers: Paraskevopoulos et al. 2022, Moller et al. 2021, Leipold et al. 2021, Wu-Chung et al. 2025, Papadaki et al. 2023, Olszewska et al. 2021, Blasi et al. 2025.

---

## 6. Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [25:33,33:41,41:49,21,7,8,23,13] | 8 feature groups | Interactions, change, dynamics, timbre |
| H3 | 18 tuples | Coupling, binding, cross-network, reconfiguration, demand, and tonal dynamics |

---
---

## Summary Statistics

### Output Dimensions by Model

| Model | Unit | Tier | D | E-Layer | M-Layer | P-Layer | F-Layer | H3 |
|-------|------|------|---|---------|---------|---------|---------|-----|
| EDNR | NDU | alpha | 10 | 4 | 2 | 2 | 2 | 16 |
| TSCP | SPU | beta | 10 | 3 | 1 | 3 | 3 | 12 |
| CDMR | NDU | beta | 11 | 4 | 2 | 3 | 2 | 16 |
| SLEE | NDU | beta | 13 | 4 | 3 | 3 | 3 | 18 |
| ESME | SPU | gamma | 11 | 4 | 1 | 3 | 3 | 12 |
| ECT | NDU | gamma | 12 | 4 | 3 | 2 | 3 | 18 |
| **TOTAL** | | | **67** | **23** | **12** | **16** | **16** | **92** |

### Tier Gradient

| Tier | Count | Avg D | Avg H3 |
|------|-------|-------|--------|
| alpha | 1 | 10.0 | 16.0 |
| beta | 3 | 11.3 | 15.3 |
| gamma | 2 | 11.5 | 15.0 |

F8 outputs range from 10D (EDNR, TSCP) to 13D (SLEE), reflecting variable complexity across learning and plasticity mechanisms. H3 demand is highest for SLEE and ECT (18 each), driven by their multi-scale statistical and network dynamics tracking requirements. The two SPU models (TSCP, ESME) share the lowest H3 demand (12 each) with minimal M-layer computation (1D each), reflecting their focused sensory processing emphasis.

### Brain Region Convergence

**Bilateral STG**: mentioned in EDNR, TSCP, ESME, ECT -- 4 of 6 models.
**IFG (area 47m / BA44)**: mentioned in EDNR, CDMR, SLEE, ESME, ECT -- 5 of 6 models.
**Heschl's Gyrus**: mentioned in EDNR, TSCP, ESME, ECT -- 4 of 6 models.
**Hippocampus**: mentioned in SLEE -- 1 of 6 models (specialized for statistical learning memory).
**Planum Temporale**: mentioned in EDNR, TSCP -- 2 of 6 models.
**OFC**: mentioned in ESME -- 1 of 6 models (faster co-activation in musicians).

IFG is the convergence hub for F8: the inferior frontal gyrus (area 47m / BA44) appears across 5 of 6 models, consistent with its role as the supramodal hub for expertise-dependent auditory processing and music-syntactic prediction.

### Unit Distribution

| Unit | Count | Models |
|------|-------|--------|
| NDU (Neuroplasticity & Development Unit) | 4 | EDNR, CDMR, SLEE, ECT |
| SPU (Sensory Processing Unit) | 2 | TSCP, ESME |

F8 is predominantly NDU (4/6 models), reflecting that learning and plasticity is fundamentally a neuroplasticity function. The 2 SPU models (TSCP, ESME) address sensory-level plasticity — timbre-specific cortical enhancement and domain-specific MMN enhancement — that occurs at the sensory processing level.

### Layer Distribution

| Layer Type | Models With | Total Dims |
|------------|-------------|------------|
| E (Extraction) | 6/6 | 23D |
| M (Temporal Integration) | 6/6 | 12D |
| P (Cognitive Present) | 6/6 | 16D |
| F (Forecast) | 6/6 | 16D |

All 6 models have all 4 layers (E+M+P+F). The E-layer has the most dimensions (23D), reflecting the feature-rich extraction requirements of learning and plasticity mechanisms. The M-layer is the most compact (12D), with TSCP and ESME having only 1D each — their temporal integration is captured by a single multiplicative gating function rather than multi-dimensional tracking. P and F layers are balanced at 16D each.
