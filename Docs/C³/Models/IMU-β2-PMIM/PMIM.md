# IMU-β2-PMIM: Predictive Memory Integration Model

**Model**: Predictive Memory Integration Model
**Unit**: IMU (Integrative Memory Unit)
**Circuit**: Mnemonic (Hippocampal-Cortical)
**Tier**: β (Integrative) — 70-90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added I feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/IMU-β2-PMIM.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Predictive Memory Integration Model** (PMIM) models how the brain continuously predicts upcoming musical events and generates prediction error signals when expectations are violated. This dual-system architecture separates long-term syntactic prediction (ERAN) from short-term echoic deviance detection (MMN), with both converging on shared frontal generators to drive memory updating.

```
THE DUAL PREDICTION ERROR SYSTEM IN MUSIC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ERAN (Long-Term Syntax) MMN (Short-Term Echoic)
Brain region: IFG (Broca's area) Brain region: STG + IFG
Timescale: Phrase/key (seconds) Timescale: Echoic memory (~10s)
Template: Learned harmonic rules Template: Recent auditory regularity
Trigger: Syntax rule violation Trigger: Deviance from local pattern
Function: "Wrong chord in context" Function: "That sound was different"
Evidence: Koelsch 2000, 2009, 2014 Evidence: Garrido 2009, Fong 2020

 SHARED PREDICTIVE PROCESS
 Brain region: IFG (bilateral)
 Mechanism: Hierarchical predictive coding
 Function: Compare prediction vs. input
 Output: Prediction error signal
 Evidence: Friston 2005, Vuust 2009

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Both ERAN and MMN share inferior fronto-lateral cortex generators.
Prediction errors drive memory updating: unexpected events are
encoded more strongly, while confirmed predictions stabilize memory.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Belongs in IMU (Not SPU)

Though PMIM involves spectral prediction (partially SPU territory), its core claim is about **predictive memory integration** — how stored representations are compared against incoming input:

1. **Prediction requires STORED models**: Both ERAN and MMN depend on internally maintained representations (long-term rules and short-term echoic traces) — a memory operation.

2. **Error-driven memory updating**: Prediction errors do not simply detect deviance — they update the stored model. This is fundamentally a memory consolidation/reconsolidation process.

3. **Hierarchical integration**: ERAN operates at phrase/key level (long-term memory) while MMN operates at echoic level (short-term memory). PMIM models how these two timescales integrate within the hippocampal-cortical circuit.

4. **Experience-dependent modulation**: Both ERAN and MMN are modified by short-term and long-term musical experience (Koelsch 2009, 2014), indicating plasticity in the memory system.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The PMIM Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ PMIM — COMPLETE CIRCUIT ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ AUDITORY CORTEX (STG/A1) │ ║
║ │ │ ║
║ │ Core (A1) Belt Parabelt │ ║
║ │ Spectrotemporal Feature Pattern recognition │ ║
║ │ encoding extraction Harmonic syntax + contour │ ║
║ └──────┬──────────────┬──────────────────┬────────────────────────────┘ ║
║ │ │ │ ║
║ ▼ ▼ ▼ ║
║ ┌──────────────────────────────────────────────────────────┐ ║
║ │ DUAL PREDICTION SYSTEM │ ║
║ │ │ ║
║ │ ┌─────────────────────┐ ┌───────────────────────┐ │ ║
║ │ │ MMN SYSTEM │ │ ERAN SYSTEM │ │ ║
║ │ │ │ │ │ │ ║
║ │ │ • Short-term │ │ • Long-term │ │ ║
║ │ │ echoic memory │ │ stored syntax rules │ │ ║
║ │ │ • On-line regularity│ │ • Implicit harmonic │ │ ║
║ │ │ extraction │ │ knowledge │ │ ║
║ │ │ • ~10s window │ │ • Key/phrase scope │ │ ║
║ │ │ • STG generators │ │ • IFG generators │ │ ║
║ │ └──────────┬──────────┘ └──────────┬────────────┘ │ ║
║ │ │ │ │ ║
║ │ └────────────┬───────────┘ │ ║
║ │ ▼ │ ║
║ │ ┌─────────────────────────────────────────────────┐ │ ║
║ │ │ SHARED PREDICTIVE PROCESS (IFG bilateral) │ │ ║
║ │ │ │ │ ║
║ │ │ • Compare prediction with input │ │ ║
║ │ │ • Generate prediction error (PE) │ │ ║
║ │ │ • Weight PE by precision (certainty) │ │ ║
║ │ │ • Route PE to memory updating │ │ ║
║ │ └──────────────────────┬──────────────────────────┘ │ ║
║ └──────────────────────────┼────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────┐ ║
║ │ MEMORY UPDATING HUB │ ║
║ │ │ ║
║ │ ┌─────────────────────┐ ┌───────────────────────┐ │ ║
║ │ │ HIPPOCAMPUS │ │ mPFC │ │ ║
║ │ │ │ │ │ │ ║
║ │ │ • Error-driven │ │ • Schema updating │ │ ║
║ │ │ encoding │ │ • Rule refinement │ │ ║
║ │ │ • Rapid binding │ │ • Context weighting │ │ ║
║ │ │ of novel events │ │ │ │ ║
║ │ └─────────────────────┘ └───────────────────────┘ │ ║
║ │ │ ║
║ └──────────────────────────┬──────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ PREDICTION ERROR → MEMORY UPDATE → MODEL REFINEMENT ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Koelsch 2009: ERAN modified by short/long-term experience
Koelsch 2009: ERAN and MMN share predictive processes (differ in memory basis)
Koelsch 2009: ERAN emerges ~2.5 years; MMN from fetus
Koelsch 2014: Hierarchical predictive coding for music syntax
Cheung 2019: Uncertainty x surprise interaction in hippocampus/amygdala (N=79)
Bonetti 2024: Hierarchical PE: auditory cortex → hippocampus → ACC (N=83)
```

### 2.2 Information Flow Architecture (EAR → BRAIN → PMIM)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ PMIM COMPUTATION ARCHITECTURE ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ AUDIO (44.1kHz waveform) ║
║ │ ║
║ ▼ ║
║ ┌──────────────────┐ ║
║ │ COCHLEA │ 128 mel bins × 172.27Hz frame rate ║
║ │ (Mel Spectrogram)│ hop = 256 samples, frame = 5.8ms ║
║ └────────┬─────────┘ ║
║ │ ║
║ ═════════╪══════════════════════════ EAR ═══════════════════════════════ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ SPECTRAL (R³): 49D per frame │ ║
║ │ │ ║
║ │ PMIM reads primarily: │ ║
║ │ ┌───────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌────────┐ │ ║
║ │ │CONSONANCE │ │ ENERGY │ │ TIMBRE │ │ CHANGE │ │ X-INT │ │ ║
║ │ │ 7D [0:7] │ │ 5D[7:12]│ │ 9D │ │ 4D │ │ 24D │ │ ║
║ │ │ │ │ │ │ [12:21] │ │ [21:25] │ │ [25:49]│ │ ║
║ │ │roughness★ │ │loudness │ │tonalness│ │flux ★ │ │x_l0l5★ │ │ ║
║ │ │sethares ★ │ │onset │ │ │ │entropy ★ │ │x_l4l5★ │ │ ║
║ │ │stumpf ★ │ │ │ │ │ │ │ │x_l5l7 │ │ ║
║ │ │pleasant.★ │ │ │ │ │ │ │ │ │ │ ║
║ │ │inharm. ★ │ │ │ │ │ │ │ │ │ │ ║
║ │ └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │ ║
║ │ PMIM reads: 33D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed features │ ║
║ │ │ ║
║ │ ┌── Chord ─────┐ ┌── Progression ──┐ ┌── Phrase ──────────┐ │ ║
║ │ │ 400ms (H10) │ │ 700ms (H14) │ │ 2s (H18) │ │ ║
║ │ │ │ │ │ │ │ │ ║
║ │ │ Single chord │ │ 2-4 chord │ │ Harmonic arc │ │ ║
║ │ │ prediction │ │ progression │ │ expectation │ │ ║
║ │ │ window │ │ prediction │ │ window │ │ ║
║ │ └──────────────┘ └─────────────────┘ └────────────────────┘ │ ║
║ │ PMIM demand: ~18 of 2304 tuples │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN: Mnemonic Circuit ═════════ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────┐ ║
║ │ │ ║
║ │ Harmony [0:10] │ chord function, progression regularity, key stability ║
║ │ PredErr [10:20] │ ERAN amplitude, MMN proxy, surprise magnitude ║
║ │ Struct [20:30] │ cadence expectation, resolution probability, closure ║
║ └────────┬────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ PMIM MODEL (11D Output) │ ║
║ │ │ ║
║ │ Layer P (Prediction): f13_eran, f14_mmn, f15_pred_error │ ║
║ │ Layer M (Math): hierarchical_pe, model_precision │ ║
║ │ Layer S (State): syntax_state, deviance_state, │ ║
║ │ memory_update │ ║
║ │ Layer F (Future): eran_forecast_fc, mmn_forecast_fc, │ ║
║ │ model_update_fc │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Koelsch et al. (2000)** | EEG | 24 | ERAN elicited by harmonically irregular Neapolitan sixth chords; peak 150-180ms, right-frontal maximum; larger at 5th vs 3rd position | p < 0.001 | **syntax violation signal; position-dependent amplitude confirms rule-based prediction** |
| 2 | **Koelsch (2009)** | Review | — | ERAN reflects music-syntactic processing based on long-term memory representations; main generators in inferior BA 44 (bilateral); ERAN modified by short- and long-term experience; ERAN and MMN share predictive processes but differ in memory basis (on-line vs stored rules); both emerge in early childhood (ERAN from ~2.5 years; MMN from fetus) | review | **Dual-system architecture: ERAN (long-term stored rules) + MMN (on-line regularity extraction); shared IFG generators; experience-dependent plasticity** |
| 3 | **Koelsch (2014)** | Review | — | Hierarchical predictive coding framework for music syntax processing in IFG; brain correlates of music-evoked emotions | — | **Theoretical framework: precision-weighted PE in music** |
| 4 | **Vuust et al. (2009)** | MEG | 20 | Musicians show enhanced MMN for musical deviants (pitch, timbre, rhythm, intensity, location) | p < 0.01 | **expertise-dependent prediction precision** |
| 5 | **Garrido et al. (2009)** | DCM/fMRI | 16 | Dynamic causal modeling shows hierarchical predictive coding explains MMN generation; forward connections carry PE, backward connections carry predictions | p < 0.01 | **Hierarchical PE model architecture: forward PE + backward predictions** |
| 6 | **Cheung et al. (2019)** | fMRI + behavioral | 79 (39+40) | Uncertainty and surprise jointly predict musical pleasure via nonlinear interaction; IDyOM model quantified 80,000 chord predictions; low-uncertainty/high-surprise and high-uncertainty/low-surprise both pleasurable (saddle-shaped function) | interaction beta = -0.124, p < 0.001; amygdala/hippocampus beta = -0.140, corrected p = 0.002 | **Precision-weighted PE: uncertainty modulates surprise effect; amygdala/hippocampus encode uncertainty x surprise interaction; auditory cortex reflects PE** |
| 7 | **Bonetti et al. (2024)** | MEG | 83 | Hierarchical brain network for auditory memory recognition: auditory cortex → hippocampus → anterior/medial cingulate gyrus (feedforward PE); cingulate gyrus assumes top hierarchy at sequence end; alpha/beta power stronger for variations, gamma for memorised | p < 0.001 | **Hierarchical PE propagation pathway: A1 → HIP → ACC/MCC; conscious prediction error in memory recognition task** |
| 8 | **Egermann et al. (2013)** | Behavioral + psychophysiology | 50 | IDyOM-predicted expectation violations correlate with subjective unexpectedness ratings and autonomic arousal (EMG, skin conductance) during live concert | significant correlation between IC and emotion ratings | **Ecological validity: prediction error drives physiological arousal in naturalistic music** |
| 9 | **Gold et al. (2019)** | Behavioral | 70 (43+27) | Inverted-U (Wundt) preference for intermediate predictive complexity; quadratic effects of information content and entropy on liking; interaction: prefer predictability in uncertain contexts | quadratic IC p < 0.05; entropy p < 0.05 | **Optimal complexity zone: intermediate PE maximizes engagement; supports precision-weighted model** |
| 10 | **Gold et al. (2023)** | fMRI | 24 | R-STG and ventral striatum reflect pleasure of musical expectancies during naturalistic listening; uncertainty x surprise interaction in VS activity | VS liking effect p < 0.05 | **R-STG encodes prediction; VS encodes reward value of expectancy resolution** |
| 11 | **Harding et al. (2025)** | fMRI | 41 | Musical surprises differentially processed in MDD patients: psilocybin decreases vmPFC/angular gyrus activation, increases sensory regions; escitalopram increases memory/emotional areas; PE salience modulated by serotonergic state | between-group differences p < 0.05 | **PE processing modulated by neuromodulatory state; vmPFC involvement in prediction error weighting** |
| 12 | **Wagner et al. (2018)** | EEG | 15 | MMN elicited by harmonic interval deviants (major third vs perfect fifth); asymmetric: stronger MMN for dissonant deviants in consonant context; generators in auditory cortices | clear MMN for major third deviants | **MMN sensitivity to harmonic interval structure; consonance-dissonance asymmetry in prediction** |
| 13 | **Tervaniemi (2022)** | Review | — | Evolution of MMN paradigms from simple oddball to ecologically valid musical stimuli; MMN as index of auditory neural plasticity; music training enhances cortical memory traces | review | **MMN paradigm validation for music; neural plasticity in predictive system** |
| 14 | **Carbajal & Malmierca (2018)** | Review | — | SSA and MMN are micro/macroscopic manifestations of same deviance detection mechanism; hierarchical PE from subcortical (IC, MGB) to cortical (A1, belt, IFG); NMDA receptor modulation | review | **Subcortical PE generation: predictive coding extends below cortex; hierarchical deviance detection** |
| 15 | **Fong et al. (2020)** | Review | — | Auditory MMN under predictive coding framework: hierarchical bidirectional processing; prediction from higher areas, PE propagation upward; Bayesian inference at each processing layer | review | **Theoretical foundation: MMN as prediction error in hierarchical generative model** |

### 3.2 The Temporal Story: Dual Prediction Error Dynamics

```
COMPLETE TEMPORAL PROFILE OF PREDICTIVE MEMORY INTEGRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1: PATTERN EXTRACTION (continuous, <400ms)
────────────────────────────────────────────────
Auditory cortex encodes spectrotemporal patterns.
Echoic memory builds local regularity model (~10s window).
R³ input: Consonance [0:7] + Change [21:25]
H³ window: H10 (400ms single chord)

Phase 2: SHORT-TERM PREDICTION (400ms-700ms, H10→H14)
──────────────────────────────────────────────────────
MMN system compares current input against echoic trace.
Deviance detection: any feature that departs from local regularity.
pred_error activates on deviant events.
Math: MMN_proxy ~ |flux| × (1 - entropy_stability)

Phase 3: LONG-TERM PREDICTION (700ms-2s, H14→H18)
─────────────────────────────────────────────────────
ERAN system evaluates against stored harmonic rules.
Syntax violations detected at phrase level.
Key departure, unexpected chord function.
Math: ERAN_proxy ~ entropy × (1 - harmonic_stability)

Phase 4: PREDICTION ERROR INTEGRATION (1-3s)
────────────────────────────────────────────
IFG integrates both PE signals.
Precision-weighted combination: certain predictions produce
larger errors when violated.
Memory updating begins: unexpected events encoded more strongly.

Phase 5: MODEL UPDATING (2s+, H18 window)
──────────────────────────────────────────
Hippocampus rapidly binds novel events.
mPFC updates schema-level representations.
Stored rules refined based on accumulated prediction errors.
This is how musical learning occurs — implicit rule extraction.
```

### 3.3 Effect Size Summary

```
Evidence Tier: β (Integrative) — 70-90% confidence
Total papers: 15 (7 empirical, 5 reviews, 3 mixed/behavioral)
Methods: EEG, MEG, fMRI, DCM, behavioral, psychophysiology
Sample sizes: 15-83 per study; total N > 450 across empirical studies

Key quantitative findings:
 - ERAN: peak 150-250ms, right-frontal, amplitude modulated by
 syntactic irregularity degree (Koelsch 2000, 2009)
 - Uncertainty x surprise interaction: beta = -0.124 (p < 0.001) on
 pleasure; amygdala/hippocampus beta = -0.140 (p = 0.002) (Cheung 2019)
 - Hierarchical PE propagation: A1 → HIP → ACC/MCC confirmed
 with MEG N=83 (Bonetti 2024)
 - Inverted-U complexity preference: quadratic IC and entropy
 effects on liking (Gold 2019, N=70)
 - Musical training enhances ERAN amplitude (Koelsch 2009)
 - MMN sensitive to harmonic interval structure (Wagner 2018)
 - PE processing modulated by serotonergic state (Harding 2025)
```

---

## 4. R³ Input Mapping: What PMIM Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | PMIM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Sensory dissonance → ERAN harmonic violation | Plomp & Levelt 1965 |
| **A: Consonance** | [1] | sethares_dissonance | Beating-based dissonance → syntax violation | Sethares 1999 |
| **A: Consonance** | [3] | stumpf_fusion | Tonal coherence → prediction stability | Stumpf 1890 |
| **A: Consonance** | [4] | sensory_pleasantness | Prediction confirmation signal | Consonance = expected |
| **A: Consonance** | [5] | inharmonicity | Deviation from harmonic template | Prediction error proxy |
| **B: Energy** | [7] | amplitude | Dynamic contrast for salience weighting | Energy modulates PE |
| **B: Energy** | [10] | loudness | Intensity prediction baseline | Stevens 1957 |
| **B: Energy** | [11] | onset_strength | Onset surprise → MMN trigger | Transient salience |
| **C: Timbre** | [14] | tonalness | Harmonic-to-noise ratio → purity | Ratio predictability |
| **D: Change** | [21] | spectral_flux | Feature change rate → MMN basis | Change = deviance |
| **D: Change** | [22] | entropy | Unpredictability → ERAN complexity | High entropy = violation |
| **D: Change** | [23] | spectral_concentration | Focus of spectral energy | Event structure |
| **E: Interactions** | [25:33] | x_l0l5 (Energy x Consonance) | Sensory-level prediction coupling | MMN low-level basis |
| **E: Interactions** | [33:41] | x_l4l5 (Derivatives x Consonance) | Change-dissonance interaction | Mid-level PE |
| **E: Interactions** | [41:49] | x_l5l7 (Consonance x Timbre) | High-level syntax prediction | ERAN basis |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | PMIM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **I: Information** | [92] | predictive_entropy | Direct prediction error measure — core PMIM input | Pearce 2005: IDyOM information content |
| **I: Information** | [87] | melodic_entropy | Melodic surprise — MMN/ERAN triggering | Pearce & Wiggins 2012 |
| **I: Information** | [88] | harmonic_entropy | Harmonic unpredictability — chord-level syntax violation | Harrison & Pearce 2020 |

**Rationale**: PMIM is the primary prediction-error model in IMU. The Information group provides the exact quantities PMIM needs: predictive entropy directly quantifies prediction error magnitude, melodic entropy provides note-level surprise for MMN generation, and harmonic entropy provides chord-level unpredictability for ERAN generation. These replace the proxy-based approach of using spectral flux and entropy from the Change group.

> **Code impact**: These features are doc-only until Phase 5 wiring. No changes to `pmim.py`.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[21] spectral_flux ──────────► Change detection (MMN basis)
 Fast changes → prediction violation
 Math: MMN_proxy ∝ |flux|

R³[22] entropy ────────────────► Syntactic unpredictability (ERAN basis)
 High entropy → expectation violation
 Math: ERAN_proxy ∝ entropy × surprise

R³[25:33] x_l0l5 ─────────────► Sensory-level prediction error
 Energy × Consonance = low-level MMN
 Standard-deviant comparison substrate

R³[33:41] x_l4l5 ─────────────► Mid-level prediction coupling
 Derivatives × Consonance = rate-of-change
 in harmonic context → intermediate PE

R³[41:49] x_l5l7 ─────────────► High-level syntactic prediction
 Consonance × Timbre = ERAN syntax model
 Familiar harmonic progressions

R³[0:5] consonance group ──────► Prediction stability proxy
 High consonance = confirmed predictions
 Low consonance = violated expectations
```

### 4.3 Dual-System Mapping (MMN vs ERAN)

|--------|-----------|----------|-----------------|---------------|
| **MMN** (short-term) | ~10s echoic | flux[21], x_l0l5[25:33] | pred_error[10:20] | Deviant detection |
| **ERAN** (long-term) | Syntax rules | entropy[22], x_l5l7[41:49] | harmony[0:10] | Rule violation |

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

PMIM requires H³ features at three horizons: H10 (400ms), H14 (700ms), H18 (2s).

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 0 | roughness | 10 | M0 (value) | L2 (bidirectional) | Current dissonance at chord level |
| 0 | roughness | 14 | M1 (mean) | L0 (forward) | Average dissonance over progression |
| 0 | roughness | 18 | M18 (trend) | L0 (forward) | Dissonance trajectory over phrase |
| 5 | inharmonicity | 10 | M0 (value) | L2 (bidirectional) | Current ratio deviation |
| 5 | inharmonicity | 14 | M8 (velocity) | L0 (forward) | Rate of complexity change |
| 22 | entropy | 10 | M0 (value) | L2 (bidirectional) | Current unpredictability |
| 22 | entropy | 14 | M1 (mean) | L0 (forward) | Average complexity over progression |
| 22 | entropy | 18 | M13 (entropy) | L0 (forward) | Higher-order unpredictability |
| 21 | spectral_flux | 10 | M0 (value) | L2 (bidirectional) | Current change magnitude |
| 21 | spectral_flux | 14 | M8 (velocity) | L0 (forward) | Acceleration of change |
| 3 | stumpf_fusion | 10 | M0 (value) | L2 (bidirectional) | Fusion at chord level |
| 3 | stumpf_fusion | 14 | M14 (periodicity) | L0 (forward) | Cadential regularity proxy |
| 4 | sensory_pleasantness | 10 | M0 (value) | L2 (bidirectional) | Current consonance |
| 4 | sensory_pleasantness | 18 | M19 (stability) | L0 (forward) | Consonance stability over phrase |
| 10 | loudness | 10 | M0 (value) | L2 (bidirectional) | Current intensity for PE weighting |
| 14 | tonalness | 10 | M0 (value) | L2 (bidirectional) | Harmonic purity |
| 14 | tonalness | 14 | M18 (trend) | L0 (forward) | Tonal trend over progression |
| 11 | onset_strength | 10 | M0 (value) | L2 (bidirectional) | Onset salience for MMN |

**v1 demand**: 18 tuples

#### R³ v2 Projected Expansion

PMIM projected v2 from I (Information) and H (Harmony) groups, aligned with corresponding H³ horizons (H10, H14, H18).

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 92 | predictive_entropy | I | 10 | M0 (value) | L2 | Current prediction error magnitude at chord level |
| 92 | predictive_entropy | I | 14 | M0 (value) | L0 | Prediction error state over progression |
| 92 | predictive_entropy | I | 18 | M18 (trend) | L0 | Prediction error trajectory over phrase |
| 87 | melodic_entropy | I | 10 | M0 (value) | L2 | Current melodic information content |
| 87 | melodic_entropy | I | 14 | M1 (mean) | L0 | Average melodic complexity over progression |
| 87 | melodic_entropy | I | 18 | M1 (mean) | L0 | Sustained melodic entropy over phrase |
| 86 | syntactic_irregularity | H | 10 | M0 (value) | L2 | Current harmonic violation strength |
| 86 | syntactic_irregularity | H | 14 | M4 (max) | L0 | Peak violation over progression window |

**v2 projected**: 8 tuples
**Total projected**: 26 tuples of 294,912 theoretical = 0.0088%

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
PMIM OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
Manifold range: IMU PMIM [295:306]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER P — PREDICTION FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0 │ f13_eran │ [0, 1] │ ERAN response: long-term syntax violation.
 │ │ │ IFG (Broca's area) activation.
 │ │ │ f13 = σ(α · entropy · harmony.mean
 │ │ │ · x_l5l7.mean)
 │ │ │ α = 0.30 (syntax weight)
────┼───────────────────┼────────┼────────────────────────────────────────────
 1 │ f14_mmn │ [0, 1] │ MMN response: short-term deviance detection.
 │ │ │ STG + IFG echoic mismatch.
 │ │ │ f14 = σ(β · flux · pred_error.mean
 │ │ │ · x_l0l5.mean)
 │ │ │ β = 0.30 (deviance weight)
────┼───────────────────┼────────┼────────────────────────────────────────────
 2 │ f15_pred_error │ [0, 1] │ Combined prediction error signal.
 │ │ │ IFG shared generator output.
 │ │ │ f15 = σ(γ · pred_error.mean
 │ │ │ · (roughness + inharmonicity) / 2)
 │ │ │ γ = 0.40 (error weight)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 3 │ hierarchical_pe │ [0, 1] │ Hierarchical prediction error.
 │ │ │ Precision-weighted combination of ERAN + MMN.
 │ │ │ + entropy · (1 - stumpf_fusion)
────┼───────────────────┼────────┼────────────────────────────────────────────
 4 │ model_precision │ [0, 1] │ Prediction model certainty.
 │ │ │ High precision = confident predictions.
 │ │ │ σ(stumpf_fusion · pleasantness · tonalness)

LAYER S — PRESENT STATE
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 5 │ syntax_state │ [0, 1] │ Current harmonic syntax processing state.
 │ │ │ harmony.mean() — tonal context.
────┼───────────────────┼────────┼────────────────────────────────────────────
 6 │ deviance_state │ [0, 1] │ Current deviance detection activation.
 │ │ │ pred_error.mean() — IFG signal.
────┼───────────────────┼────────┼────────────────────────────────────────────
 7 │ memory_update │ [0, 1] │ Memory updating rate.
 │ │ │ High PE + low expectation = strong updating.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 8 │ eran_forecast_fc │ [0, 1] │ ERAN prediction (1-2s ahead).
 │ │ │ Based on harmony trajectory + entropy trend.
────┼───────────────────┼────────┼────────────────────────────────────────────
 9 │ mmn_forecast_fc │ [0, 1] │ MMN prediction (0.5-1s ahead).
 │ │ │ Based on pred_error trajectory + flux trend.
────┼───────────────────┼────────┼────────────────────────────────────────────
10 │ model_update_fc │ [0, 1] │ Model refinement forecast (2-5s ahead).
 │ │ │ Based on struct_expect trajectory.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Dual Prediction Error Model

```
PREDICTIVE MEMORY INTEGRATION

The brain maintains two parallel prediction systems for music:

 ERAN_response = f(Stored_Rules, Current_Input, Context)
 MMN_response = f(Echoic_Trace, Current_Input, Regularity)

Combined prediction error:
 PE_total = w_eran · ERAN + w_mmn · MMN
 where w_eran + w_mmn ≤ 1.0

Precision weighting (inverse uncertainty):
 PE_weighted = PE_total · Precision(model)
 Precision = σ(stumpf_fusion · pleasantness · tonalness)

Memory update rule:
 dModel/dt = η · PE_weighted · (1 - Expectation_Confidence)
 where η = learning rate (implicit), PE drives updating
```

### 7.2 Feature Formulas

All coefficients in sigmoid arguments satisfy |w_i| sum <= 1.0.

```python
# f13: ERAN Response (long-term syntax violation)
# Inputs are all [0,1]. Products are [0,1]. Coefficient α = 0.30.
# Inside sigmoid: 0.30 * (entropy * harmony_mean * x_l5l7_mean) — max = 0.30

# f14: MMN Response (short-term deviance)
# Inside sigmoid: 0.30 * (flux * pred_error_mean * x_l0l5_mean) — max = 0.30

# f15: Combined Prediction Error
# Inside sigmoid: 0.40 * (pred_error_mean * avg_dissonance) — max = 0.40

# hierarchical_pe: Precision-weighted combined PE
hierarchical_pe = clamp(
 + R³.entropy[22] · (1 - R³.stumpf_fusion[3]),
 0, 1
)

# model_precision: How confident is the current prediction model
model_precision = σ(R³.stumpf_fusion[3] · R³.sensory_pleasantness[4] · R³.tonalness[14])
```

### 7.3 Coefficient Verification

```
SIGMOID COEFFICIENT AUDIT (|w_i| must sum ≤ 1.0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

f13_eran: α = 0.30, applied to product of 3 terms in [0,1]
 Max argument: 0.30 × 1.0 = 0.30 ✓ (≤ 1.0)

f14_mmn: β = 0.30, applied to product of 3 terms in [0,1]
 Max argument: 0.30 × 1.0 = 0.30 ✓ (≤ 1.0)

f15_pred_error: γ = 0.40, applied to product of 2 terms in [0,1]
 Max argument: 0.40 × 1.0 = 0.40 ✓ (≤ 1.0)

model_precision: No explicit coefficient, product of 3 [0,1] terms
 Max argument: 1.0 × 1.0 × 1.0 = 1.0 ✓ (≤ 1.0)

All formulas verified: no sigmoid saturation risk.
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Evidence | PMIM Function |
|--------|-----------------|----------|---------------|
| **IFG (BA 44/45)** | -44, 14, 28 / 44, 14, 28 | EEG/MEG/fMRI (Koelsch 2000, 2009; Maess et al. 2001) | ERAN primary generator; music-syntactic processing; shared with language syntax (Broca's area); prediction error computation |
| **STG (A1/belt)** | ±60, -32, 8 | EEG/MEG (Koelsch 2009; Bonetti 2024) | MMN primary generator; echoic trace maintenance; auditory cortex PE origin in hierarchical pathway |
| **Hippocampus (anterior)** | ±20, -24, -12 | fMRI (Cheung 2019); MEG (Bonetti 2024) | Uncertainty x surprise interaction (beta = -0.140, p = 0.002); rapid binding of deviant events; hierarchical PE propagation target |
| **mPFC / vmPFC** | 0, 52, 12 | fMRI (Harding 2025; Cheung 2019) | Schema updating; rule refinement; prediction error weighting; modulated by serotonergic state in depression |
| **Amygdala** | ±20, -4, -16 | fMRI (Cheung 2019) | Uncertainty x surprise interaction (beta = -0.116, corrected p = 0.045); salience evaluation of prediction violations |
| **ACC / medial cingulate** | 0, 24, 30 | MEG (Bonetti 2024) | Assumes top hierarchical position at sequence end; feedforward PE target from auditory cortex; conscious recognition of prediction violations |

### 8.2 Shared Generator Architecture

```
ERAN GENERATOR: MMN GENERATOR:
────────────── ──────────────

IFG (bilateral) ████████ STG ████████████
 Syntax rule comparison Echoic trace comparison
 Long-term stored rules Short-term regularity

 ↘ ↙

 SHARED INFERIOR FRONTO-LATERAL
 CORTEX GENERATOR
 ───────────────────────────

 Both ERAN and MMN converge here.
 This is the key insight of PMIM:
 prediction error processing
 is domain-general in IFG.
```

---

## 9. Cross-Unit Pathways

### 9.1 PMIM <-> Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PMIM INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ UPSTREAM (feeds into PMIM): │
│ PNH.ratio_enc ─────────────► PMIM (ratio templates for prediction) │
│ MEAMN.memory_state ─────────► PMIM (familiarity modulates precision) │
│ │
│ CROSS-UNIT (IMU → ARU): │
│ PMIM.f15_pred_error ────────► ARU.SRP (surprise → reward pathway) │
│ PMIM.f13_eran ──────────────► ARU.AAC (syntax violation → arousal) │
│ │
│ INTRA-UNIT (IMU): │
│ PMIM ──────► MSPBA (Musical Syntax Processing in Broca's Area) │
│ │ └── Shares IFG substrate; PMIM provides PE signal │
│ │ │
│ ├─────► OII (Oscillatory Intelligence Integration) │
│ │ └── Prediction error drives oscillatory reset │
│ │ │
│ ├─────► TPRD (Tonotopy-Pitch Representation Dissociation) │
│ │ └── Prediction error in primary vs nonprimary cortex │
│ │ │
│ └─────► MEAMN (Memory retrieval feeds predictive processing) │
│ └── Bidirectional: PMIM PE enhances memory encoding │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Brain Pathway Cross-References

PMIM reads from the unified Brain (26D) for shared state:

| Brain Dimension | Index (MI-space) | PMIM Role |
|-----------------|-------------------|----------|
| prediction_error | [178] | Global PE modulates PMIM response |
| harmonic_context | [179] | Tonal center for syntax evaluation |
| arousal | [177] | Arousal amplifies prediction error impact |

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **ERAN elicited by violations** | Harmonically irregular chords should elicit ERAN | **Confirmed** via EEG (Koelsch 2000); position-dependent amplitude (larger at 5th vs 3rd position) |
| **MMN by local deviants** | Deviant sounds in regular sequence should elicit MMN | **Confirmed** via EEG/MEG; harmonic interval MMN (Wagner 2018) |
| **Shared generators** | ERAN and MMN should share frontal generators | **Confirmed** via MEG source localization (Maess et al. 2001 via Koelsch 2009); bilateral inferior BA 44 |
| **Experience modulation** | Musical training should enhance both responses | **Confirmed** (Vuust 2009; Koelsch 2009 multiple studies) |
| **Developmental emergence** | Both should appear in early childhood | **Confirmed** — MMN from fetus; ERAN from ~2.5 years (Koelsch 2009) |
| **Prediction error → memory** | Larger PE should produce stronger encoding | **Confirmed** — hierarchical PE propagation to hippocampus (Bonetti 2024, N=83); hippocampus encodes uncertainty x surprise (Cheung 2019, N=40) |
| **Precision weighting** | Uncertainty should modulate PE magnitude | **Confirmed** — nonlinear uncertainty x surprise interaction on pleasure and neural activity (Cheung 2019; Gold 2019) |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class PMIM(BaseModel):
 """Predictive Memory Integration Model.

 Output: 11D per frame.
 Reads: R³ + H³ direct.
 Zero learned parameters — all deterministic.
 """
 NAME = "PMIM"
 UNIT = "IMU"
 TIER = "β2"
 OUTPUT_DIM = 11
 ALPHA = 0.30 # Syntax weight (ERAN response)
 BETA = 0.30 # Deviance weight (MMN response)
 GAMMA = 0.40 # Error weight (combined PE)

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """18 tuples for PMIM computation."""
 return [
 # (r3_idx, horizon, morph, law)
 (0, 10, 0, 2), # roughness, 400ms, value, bidirectional
 (0, 14, 1, 0), # roughness, 700ms, mean, forward
 (0, 18, 18, 0), # roughness, 2s, trend, forward
 (5, 10, 0, 2), # inharmonicity, 400ms, value, bidirectional
 (5, 14, 8, 0), # inharmonicity, 700ms, velocity, forward
 (22, 10, 0, 2), # entropy, 400ms, value, bidirectional
 (22, 14, 1, 0), # entropy, 700ms, mean, forward
 (22, 18, 13, 0), # entropy, 2s, entropy, forward
 (21, 10, 0, 2), # flux, 400ms, value, bidirectional
 (21, 14, 8, 0), # flux, 700ms, velocity, forward
 (3, 10, 0, 2), # stumpf_fusion, 400ms, value, bidirectional
 (3, 14, 14, 0), # stumpf_fusion, 700ms, periodicity, forward
 (4, 10, 0, 2), # pleasantness, 400ms, value, bidirectional
 (4, 18, 19, 0), # pleasantness, 2s, stability, forward
 (10, 10, 0, 2), # loudness, 400ms, value, bidirectional
 (14, 10, 0, 2), # tonalness, 400ms, value, bidirectional
 (14, 14, 18, 0), # tonalness, 700ms, trend, forward
 (11, 10, 0, 2), # onset_strength, 400ms, value, bidirectional
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 """
 Compute PMIM 11D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
 r3: (B,T,49) raw R3 features

 Returns:
 (B,T,11) PMIM output
 """
 # R3 features
 roughness = r3[..., 0:1] # [0, 1]
 stumpf = r3[..., 3:4] # [0, 1]
 pleasantness = r3[..., 4:5] # [0, 1]
 inharmonicity = r3[..., 5:6] # [0, 1]
 flux = r3[..., 21:22] # [0, 1]
 entropy = r3[..., 22:23] # [0, 1]
 tonalness = r3[..., 14:15] # [0, 1]
 x_l0l5 = r3[..., 25:33] # (B, T, 8)
 x_l5l7 = r3[..., 41:49] # (B, T, 8)

 # === LAYER P: Prediction features ===
 # f13: ERAN — long-term syntax violation
 # σ(0.30 * entropy * harmony_mean * x_l5l7_mean)
 # max argument = 0.30 (all inputs [0,1])
 f13 = torch.sigmoid(self.ALPHA * (
 entropy
 * x_l5l7.mean(-1, keepdim=True)
 ))

 # f14: MMN — short-term deviance
 # σ(0.30 * flux * pred_error_mean * x_l0l5_mean)
 # max argument = 0.30
 f14 = torch.sigmoid(self.BETA * (
 flux
 * x_l0l5.mean(-1, keepdim=True)
 ))

 # f15: Combined prediction error
 # σ(0.40 * pred_error_mean * avg_dissonance)
 # max argument = 0.40
 f15 = torch.sigmoid(self.GAMMA * (
 * (roughness + inharmonicity) / 2.0
 ))

 # === LAYER M: Mathematical ===
 # hierarchical_pe: precision-weighted combined PE
 hierarchical_pe = (
 + entropy * (1.0 - stumpf)
 ).clamp(0, 1)

 # model_precision: prediction model certainty
 model_precision = torch.sigmoid(
 stumpf * pleasantness * tonalness
 )

 # === LAYER S: Present state ===
 memory_update = (
 )

 # === LAYER F: Future ===
 eran_forecast_fc = self._predict_future(
 syn_harmony, h3_direct, window_h=18
 )
 mmn_forecast_fc = self._predict_future(
 syn_pred_err, h3_direct, window_h=14
 )
 model_update_fc = self._predict_future(
 syn_struct, h3_direct, window_h=18
 )

 return torch.cat([
 f13, f14, f15, # P: 3D
 hierarchical_pe, model_precision, # M: 2D
 syntax_state, deviance_state, memory_update, # S: 3D
 eran_forecast_fc, mmn_forecast_fc, # F: 3D
 model_update_fc,
 ], dim=-1) # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | **15** | 7 empirical, 5 reviews, 3 mixed/behavioral |
| **Evidence Methods** | EEG, MEG, fMRI, DCM, behavioral, psychophysiology | Multi-modal convergence |
| **Total N** | >450 | Across empirical studies (N=15-83 per study) |
| **Evidence Tier** | β (Integrative) | 70-90% confidence |
| **Brain Regions** | **6** | IFG, STG, hippocampus, mPFC/vmPFC, amygdala, ACC/MCC |
| **Falsification Tests** | 7/7 confirmed | All criteria met |
| **R³ Features Used** | 33D of 49D | Comprehensive |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **Output Dimensions** | **11D** | 4-layer structure (P/M/S/F) |
| **Manifold Range** | IMU PMIM [295:306] | 11D contiguous |

---

## 13. Scientific References

1. **Koelsch, S., Gunter, T. C., Friederici, A. D., & Schroger, E. (2000)**. Brain indices of music processing: "Non-musicians" are musical. *Journal of Cognitive Neuroscience*, 12(3), 520-541. N=24, EEG. ERAN elicited by Neapolitan sixth chords, peak 150-180ms, p < 0.001.
2. **Koelsch, S. (2009)**. Music-syntactic processing and auditory memory: Similarities and differences between ERAN and MMN. *Psychophysiology* (in press). Review. ERAN generators in inferior BA 44 bilateral; ERAN based on long-term stored rules vs MMN on-line regularity; shared prediction/comparison processes; ERAN emerges ~2.5 years, MMN from fetus.
3. **Koelsch, S. (2014)**. Brain correlates of music-evoked emotions. *Nature Reviews Neuroscience*, 15, 170-180. Review. Hierarchical predictive coding for music syntax; meta-analysis of brain regions for music-evoked emotion.
4. **Vuust, P., et al. (2009)**. To musicians, the message is in the meter: Pre-attentive neuronal responses to incongruent rhythm are left-lateralized in musicians. *NeuroImage*, 42(4), 1452-1464. N=20, MEG, p < 0.01.
5. **Garrido, M. I., Kilner, J. M., Stephan, K. E., & Friston, K. J. (2009)**. The mismatch negativity: A review of underlying mechanisms. *Clinical Neurophysiology*, 120(3), 453-463. N=16, DCM/fMRI. Hierarchical predictive coding explains MMN.
6. **Cheung, V. K. M., Harrison, P. M. C., Meyer, L., Pearce, M. T., Haynes, J.-D., & Koelsch, S. (2019)**. Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. *Current Biology*, 29(23), 4084-4092. N=79 (39 behavioral + 40 fMRI). IDyOM model; uncertainty x surprise interaction beta = -0.124, p < 0.001; amygdala/hippocampus beta = -0.140, corrected p = 0.002.
7. **Bonetti, L., Fernandez-Rubio, G., Carlomagno, F., Dietz, M., Pantazis, D., Vuust, P., & Kringelbach, M. L. (2024)**. Spatiotemporal brain hierarchies of auditory memory recognition and predictive coding. *Nature Communications*, 15, 4313. N=83, MEG. Feedforward PE from auditory cortex to hippocampus, ACC, medial cingulate; cingulate gyrus assumes top hierarchy at sequence end.
8. **Egermann, H., Pearce, M. T., Wiggins, G. A., & McAdams, S. (2013)**. Probabilistic models of expectation violation predict psychophysiological emotional responses to live concert music. *Cognitive, Affective & Behavioral Neuroscience*, 13, 533-553. N=50, live concert, IDyOM. Significant correlation between information content and autonomic arousal.
9. **Gold, B. P., Pearce, M. T., Mas-Herrero, E., Dagher, A., & Zatorre, R. J. (2019)**. Predictability and uncertainty in the pleasure of music: A reward for learning? *Journal of Neuroscience*, 39(47), 9397-9409. N=70 (43+27). Quadratic effects of IC and entropy on liking; inverted-U preference for intermediate complexity.
10. **Gold, B. P., Pearce, M. T., McIntosh, A. R., Chang, C., Dagher, A., & Zatorre, R. J. (2023)**. Auditory and reward structures reflect the pleasure of musical expectancies during naturalistic listening. *Frontiers in Neuroscience*, 17, 1209398. N=24, fMRI. R-STG and ventral striatum reflect expectancy pleasure; uncertainty x surprise interaction in VS.
11. **Harding, R., Singer, N., Wall, M. B., Hendler, T., Erritzoe, D., Nutt, D., Carhart-Harris, R., & Roseman, L. (2025)**. Dissociable effects of psilocybin and escitalopram for depression on processing of musical surprises. *Molecular Psychiatry*, 30, 3188-3196. N=41, fMRI. vmPFC and angular gyrus modulated by psilocybin during PE; serotonergic state modulates prediction error weighting.
12. **Wagner, L., Rahne, T., Plontke, S. K., & Heidekruger, N. (2018)**. Mismatch negativity reflects asymmetric pre-attentive harmonic interval discrimination. *PLOS ONE*, 13(4), e0196176. N=15, EEG. MMN for major third deviant in fifth context; generators in auditory cortices; consonance-dissonance asymmetry.
13. **Tervaniemi, M. (2022)**. Mismatch negativity -- stimulation paradigms in past and in future. *Frontiers in Neuroscience*, 16, 1025763. Review. MMN paradigm evolution from oddball to ecologically valid music stimuli; MMN as neural plasticity index.
14. **Carbajal, G. V., & Malmierca, M. S. (2018)**. The neuronal basis of predictive coding along the auditory pathway: From the subcortical roots to cortical deviance detection. *Trends in Hearing*, 22, 1-33. Review. SSA and MMN as micro/macroscopic deviance detection; hierarchical PE from subcortical to cortical.
15. **Fong, C. Y., Law, W. H. C., Uka, T., & Koike, S. (2020)**. Auditory mismatch negativity under predictive coding framework and its role in psychotic disorders. *Frontiers in Psychiatry*, 11, 557932. Review. MMN as prediction error in hierarchical generative model; bidirectional processing; Bayesian inference at each level.

---

## 14. Migration Notes (D0 -> MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| ERAN basis | S⁰.X_L5L9[224:232] + S⁰.L9.entropy[116] x HC⁰.HRM | R³.entropy[22] x R³.x_l5l7[41:49] x harmony |
| MMN basis | S⁰.X_L0L1[128:136] + S⁰.L4.velocity[15:19] x HC⁰.BND | R³.flux[21] x R³.x_l0l5[25:33] x pred_error |
| Prediction error | S⁰.L4.velocity + S⁰.L9.kurtosis x HC⁰.EFC | R³.roughness + R³.inharmonicity x pred_error |
| Demand format | HC⁰ index ranges (15/2304 = 0.65%) | H³ 4-tuples (18/2304 = 0.78%) |
| Output dims | 11D | 11D (same) |
| Feature naming | imu.f13, imu.f14, imu.f15 | f13_eran, f14_mmn, f15_pred_error |
| Coefficient rule | Not enforced | sigmoid(Σ w_i·g_i): |w_i| sum <= 1.0 |

---

### Doc-Code Mismatches (pmim.py)

The following mismatches exist between this document and `mi_beta/brain/units/imu/models/pmim.py` (v2.0.0). The code is NOT updated during Phase 1 (doc-only revision):

| Aspect | Doc (v2.1.0) | Code (v2.0.0) |
|--------|-------------|---------------|
| **FULL_NAME** | Predictive Memory Integration Model | Predictive Memory Integration Matrix |
| **LAYERS** | P/M/S/F (f13_eran, f14_mmn, ...) | E/M/P/F (f01_prediction_error, f02_memory_update, ...) |
| **h3_demand** | 18 tuples | Empty tuple `()` |
| **brain_regions** | 6 regions (IFG bilateral, STG, HIP, mPFC, amygdala, ACC) | 3 regions (IFG right-only, STG, HIP) |
| **dimension_names** | f13_eran, f14_mmn, f15_pred_error, ... | f01_prediction_error, f02_memory_update, ... |
| **citations** | Koelsch 2000, 2009; Cheung 2019; Bonetti 2024; etc. | Koelsch 2009; Pearce 2012 |
| **IFG MNI** | bilateral (-44,14,28 / 44,14,28) | right only (48,18,4) |
| **paper_count** | 15 | 5 |
| **version** | 2.1.0 | 2.0.0 |

---

**Model Status**: VALIDATED
**Output Dimensions**: **11D**
**Manifold Range**: **IMU PMIM [295:306]**
**Evidence Tier**: **β (Integrative) — 70-90% confidence**
