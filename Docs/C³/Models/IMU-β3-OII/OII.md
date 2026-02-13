# IMU-β3-OII: Oscillatory Intelligence Integration

**Model**: Oscillatory Intelligence Integration
**Unit**: IMU (Integrative Memory Unit)
**Circuit**: Mnemonic (Hippocampal-Cortical)
**Tier**: β (Integrative) — 70-90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/IMU-β3-OII.md` (v1.0.0, S⁰/HC⁰ naming). v2.1.0 updates v2.0.0 with deep literature review (2→12 papers).

---

## 1. What Does This Model Simulate?

The **Oscillatory Intelligence Integration** (OII) models how musical aptitude and processing efficiency correlate with neural oscillatory patterns and general fluid intelligence (Gf). Slow oscillations (theta 4-8 Hz, alpha 8-12 Hz) support large-scale integration across brain regions, while fast oscillations (gamma 30-100 Hz) support local segregation and fine-grained processing. The efficiency of switching between these modes — integration for binding distant features, segregation for local detail — constitutes a core mechanism of musical intelligence.

```
OSCILLATORY INTELLIGENCE: INTEGRATION vs SEGREGATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SLOW OSCILLATIONS (Theta/Alpha)         FAST OSCILLATIONS (Gamma)
Function: INTEGRATION                   Function: SEGREGATION
Binding: Distant brain regions          Binding: Local circuits
Scale: Large (frontal-temporal)         Scale: Small (cortical column)

HIGH Gf individuals:                    HIGH Gf individuals:
  Stronger theta/alpha degree             Lower gamma degree
  Lower slow segregation                  Higher gamma segregation
  = EFFICIENT INTEGRATION                 = EFFICIENT LOCAL PROCESSING

AVERAGE Gf individuals:                 AVERAGE Gf individuals:
  Weaker theta/alpha degree               Stronger gamma degree
  Higher slow segregation                 Lower gamma segregation
  = DIFFUSE INTEGRATION                   = DIFFUSE LOCAL PROCESSING

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY FINDING: Musical aptitude correlates with oscillatory patterns
AND general fluid intelligence. d = 2.99 (very large effect).
Brain regions: Frontal cortex (theta), temporal cortex (alpha/gamma),
hippocampus (binding).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Belongs in IMU (Not SPU or STU)

Though OII involves oscillatory dynamics (STU territory) and spectral processing (SPU territory), its core mechanism is about **memory-guided integration**:

1. **Hippocampal binding**: Theta oscillations originating from hippocampus bind distributed cortical representations into unified percepts — this is a mnemonic operation.

2. **Syntactic templates**: Efficient mode switching requires stored templates of harmonic progressions and structural expectations against which current input is compared — SYN mechanism territory.

3. **Encoding efficiency**: High Gf individuals encode musical patterns more efficiently because they switch between integration (binding) and segregation (detail extraction) adaptively — an encoding optimization.

4. **Cross-frequency coupling**: Theta-gamma coupling in hippocampus enables rapid encoding of sequential musical items — the nested oscillation framework is fundamentally about memory formation.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The OII Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 OII — COMPLETE CIRCUIT                                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    AUDITORY CORTEX (STG/A1)                        │    ║
║  │                                                                     │    ║
║  │  Spectrotemporal encoding → oscillatory frequency analysis          │    ║
║  │  Alpha-band gating (8-12 Hz) filters incoming spectral input       │    ║
║  │  Gamma-band (30-100 Hz) supports local feature extraction          │    ║
║  └──────┬──────────────────────────────────────────────────────────────┘    ║
║         │                                                                    ║
║         ▼                                                                    ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │              FRONTAL CORTEX (Theta Hub)                             │    ║
║  │                                                                     │    ║
║  │  ┌─────────────────────┐  ┌───────────────────────┐                │    ║
║  │  │    mPFC              │  │      DLPFC            │                │    ║
║  │  │                     │  │                       │                │    ║
║  │  │  • Theta generation │  │  • Working memory     │                │    ║
║  │  │  • Long-range       │  │  • Mode switching     │                │    ║
║  │  │    integration      │  │  • Executive control  │                │    ║
║  │  │  • Top-down         │  │  • Integration-       │                │    ║
║  │  │    prediction       │  │    segregation balance│                │    ║
║  │  └─────────────────────┘  └───────────────────────┘                │    ║
║  └──────┬──────────────────────────────────────────────────────────────┘    ║
║         │                                                                    ║
║         ▼                                                                    ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │              TEMPORAL CORTEX (Alpha/Gamma Hub)                      │    ║
║  │                                                                     │    ║
║  │  ┌─────────────────────┐  ┌───────────────────────┐                │    ║
║  │  │    STG              │  │      MTG              │                │    ║
║  │  │                     │  │                       │                │    ║
║  │  │  • Alpha gating     │  │  • Gamma-band local   │                │    ║
║  │  │  • Spectral         │  │    processing         │                │    ║
║  │  │    integration      │  │  • Fine detail        │                │    ║
║  │  │                     │  │    extraction         │                │    ║
║  │  └─────────────────────┘  └───────────────────────┘                │    ║
║  └──────┬──────────────────────────────────────────────────────────────┘    ║
║         │                                                                    ║
║         ▼                                                                    ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │              HIPPOCAMPUS (Theta-Gamma Coupling Hub)                  │    ║
║  │                                                                     │    ║
║  │  • Theta-gamma cross-frequency coupling                             │    ║
║  │  • Sequential item encoding in gamma nested within theta            │    ║
║  │  • Pattern binding across cortical sources                          │    ║
║  │  • Integration-segregation coordination                             │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  CRITICAL EVIDENCE:                                                          ║
║  ─────────────────                                                          ║
║  Gf connectivity study:  DTI/MEG, d = 2.99 (very large), n=66+38           ║
║  Theta integration:      Frontal theta → temporal alpha coherence           ║
║  Gamma segregation:      Local gamma power → efficient detail extraction    ║
║  Mode switching:         Gf ∝ integration/segregation switching speed       ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### 2.2 Information Flow Architecture (EAR → BRAIN → SYN + MEM → OII)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    OII COMPUTATION ARCHITECTURE                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  AUDIO (44.1kHz waveform)                                                    ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌──────────────────┐                                                        ║
║  │ COCHLEA          │  128 mel bins × 172.27Hz frame rate                    ║
║  │ (Mel Spectrogram)│  hop = 256 samples, frame = 5.8ms                     ║
║  └────────┬─────────┘                                                        ║
║           │                                                                  ║
║  ═════════╪══════════════════════════ EAR ═══════════════════════════════    ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  SPECTRAL (R³): 49D per frame                                    │        ║
║  │                                                                  │        ║
║  │  ┌───────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌────────┐ │        ║
║  │  │CONSONANCE │ │ ENERGY  │ │ TIMBRE  │ │ CHANGE   │ │ X-INT  │ │        ║
║  │  │ 7D [0:7]  │ │ 5D[7:12]│ │ 9D      │ │ 4D       │ │ 24D    │ │        ║
║  │  │           │ │         │ │ [12:21] │ │ [21:25]  │ │ [25:49]│ │        ║
║  │  │roughness  │ │amplitude│ │warmth   │ │flux      │ │x_l0l5  │ │        ║
║  │  │sethares   │ │loudness │ │tristim. │ │entropy   │ │x_l4l5  │ │        ║
║  │  │pleasant.  │ │onset    │ │tonalness│ │concent.  │ │x_l5l7  │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         OII reads: 38D                            │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  SYN Horizons:             MEM Horizons:                         │        ║
║  │  ┌── Chord ───┐            ┌── Encoding ──┐                     │        ║
║  │  │ 400ms (H10)│            │ 1s (H16)     │                     │        ║
║  │  │ Harmonic   │            │ Working mem  │                     │        ║
║  │  │ state      │            │ binding      │                     │        ║
║  │  └──────┬─────┘            └──────┬───────┘                     │        ║
║  │  ┌── Progr. ──┐            ┌── Consolid. ─┐                     │        ║
║  │  │ 700ms (H14)│            │ 5s (H20)     │                     │        ║
║  │  │ Prediction │            │ Hippocampal  │                     │        ║
║  │  │ error      │            │ binding      │                     │        ║
║  │  └──────┬─────┘            └──────┬───────┘                     │        ║
║  │  ┌── Phrase ──┐            ┌── Retrieval ─┐                     │        ║
║  │  │ 2s (H18)   │            │ 36s (H24)    │                     │        ║
║  │  │ Structural │            │ Long-term    │                     │        ║
║  │  │ closure    │            │ episodic     │                     │        ║
║  │  └──────┬─────┘            └──────┬───────┘                     │        ║
║  │         └──────────┬──────────────┘                              │        ║
║  │                    OII demand: ~24 of 2304 tuples                │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Mnemonic Circuit ═════════    ║
║                               │                                              ║
║  ┌────────────────────────────┼─────────────────────────────────┐           ║
║  │                            ▼                                   │           ║
║  │  ┌─────────────────┐  ┌─────────────────┐                    │           ║
║  │  │  SYN (30D)      │  │  MEM (30D)      │                    │           ║
║  │  │                 │  │                 │                    │           ║
║  │  │ Syntax   [0:10] │  │ Encoding  [0:10]│                    │           ║
║  │  │ Predict [10:20] │  │ Familiar [10:20]│                    │           ║
║  │  │ Struct  [20:30] │  │ Retrieval[20:30]│                    │           ║
║  │  └────────┬────────┘  └────────┬────────┘                    │           ║
║  │           └──────────┬─────────┘                              │           ║
║  │                      ▼                                        │           ║
║  │  ┌──────────────────────────────────────────────────────────┐│           ║
║  │  │                    OII MODEL (10D Output)                ││           ║
║  │  │                                                          ││           ║
║  │  │  Layer E (Episodic):   f16_slow_integration,            ││           ║
║  │  │                        f17_fast_segregation,             ││           ║
║  │  │                        f18_mode_switching                ││           ║
║  │  │  Layer M (Math):       gf_proxy, switching_efficiency   ││           ║
║  │  │  Layer P (Present):    integration_state, segregation_st││           ║
║  │  │  Layer F (Future):     integration_pred, segregation_pred│           ║
║  │  │                        (reserved)                        ││           ║
║  │  └──────────────────────────────────────────────────────────┘│           ║
║  └──────────────────────────────────────────────────────────────┘           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Bruzzone et al. (2022)** — *Dissociated brain functional connectivity of fast versus slow frequencies underlying individual differences in fluid intelligence: a DTI and MEG study.* Scientific Reports, 12:4746. | DTI + MEG (resting-state), graph theory (degree, modularity, segregation coefficient), WAIS-IV Gf | 66 (MEG), 67 (DTI); high Gf N=38, avg Gf N=31 | High Gf individuals show stronger degree & lower segregation in theta/alpha bands (long-range integration); opposite in gamma (higher local segregation). Structural DTI confirms: high Gf = stronger long-range white matter connectivity. | Theta degree: p<0.001; Alpha degree: p<0.001; Gamma degree: p<0.001 (reversed); DTI degree: p=0.007; Gf group separation: t(55)=11.08, p<1e-7 | **Primary evidence for integration-segregation model.** Theta/alpha integration efficiency maps to SYN.harmonic_syntax; gamma segregation efficiency maps to local processing. Gf proxy directly supported. |
| 2 | **Samiee et al. (2022)** — *Cross-Frequency Brain Network Dynamics Support Pitch Change Detection.* J. Neuroscience, 42(18):3823-3835. | MEG (275-ch), source-level PAC (delta-beta), directed connectivity (PTE), functional connectivity (coherence) | 16 (8 amusics, 8 controls) | Delta(2-4 Hz)-to-beta(15-35 Hz) PAC in rAud and rIFG. Bottom-up delta from auditory to IFG/motor cortex. Top-down beta from motor to auditory/IFG. Amusia: elevated PAC (F(1)=11.1, p<0.001 in rAud) and depressed delta connectivity. | PAC group effect rAud: F(1)=11.1, p<0.001; rIFG: F(1)=43.95, p<0.0001; Coherence: delta>beta F(1)=49.7, p<0.0001; PTE Mot→Aud beta: t(15)=6.48, p<0.001 | **Cross-frequency coupling for pitch processing.** Delta-beta PAC = mode switching mechanism. Directed connectivity = integration (bottom-up delta) vs segregation (top-down beta). Amusia as model of impaired oscillatory intelligence. |
| 3 | **Borderie et al. (2024)** — *Cross-frequency coupling in cortico-hippocampal networks supports the maintenance of sequential auditory information in short-term memory.* PLOS Biology, 22(3):e3002512. | iEEG (intracranial SEEG), theta-gamma PAC, machine learning decoding | Drug-resistant epilepsy patients (iEEG) | Theta-gamma PAC in STS, IFG, ITG, and hippocampus supports auditory STM retention. PAC strength decodes correct vs incorrect trials via machine learning. PAC positively correlated with individual STM performance. Gamma bursts restricted to specific theta phases corresponding to higher neural excitability. | PAC decoding: ML accuracy significant; PAC-STM correlation: positive (individual differences) | **Direct evidence for hippocampal theta-gamma coupling in auditory memory.** Confirms cross-frequency coupling as memory encoding mechanism. STS + IFG + hippocampus pathway matches OII circuit. Sequential item encoding via nested gamma in theta. |
| 4 | **Dobri et al. (2023)** — *Synchrony in auditory 40-Hz gamma oscillations increases in older age and correlates with hearing abilities and cortical GABA levels.* Imaging Neuroscience, 1:imag_a_00035. | MEG, 40-Hz ASSR, MR spectroscopy (GABA) | Young + older adults | 40-Hz gamma ASSR amplitude increases in older adults; correlates with hearing loss in noise condition; correlates with left auditory cortex GABA concentration in quiet condition. Gamma synchrony has detrimental effect on auditory processing when excessive. | ASSR amplitude increase in aging: significant; GABA correlation: significant (left auditory cortex) | **Gamma-band local processing and aging.** Supports OII segregation model: excessive gamma synchrony impairs feature binding. GABA-mediated inhibition controls gamma synchrony — links to mode switching efficiency. |
| 5 | **Ding et al. (2025)** — *Entrainment of rhythmic tonal sequences on neural oscillations and the impact on subjective emotion.* Scientific Reports. | EEG (64-ch), ITPC, EPS, SAM emotional ratings | 31 (37 recruited) | All 12 presenting rates (1-12 Hz) significantly entrain neural oscillations. 6 Hz boundary: below decreases valence/increases dominance; above increases valence/decreases dominance. ITPC modulation intensity correlates with emotional changes for >6 Hz sequences. | ITPC: F(11,330)=4.81, p<0.001, eta2=0.14; EPS: F(11,330)=14.10, p<0.001, eta2=0.32; Dominance interaction: eta2=0.08 | **Entrainment rate and emotion.** 6 Hz boundary aligns with theta-alpha transition, supporting OII's integration-segregation switching model. Frontocentral entrainment maps to DLPFC mode switching hub. |
| 6 | **Fries (2015)** — *Rhythms for Cognition: Communication through Coherence.* Neuron, 88(1):220-235. | Review + CTC framework | — (Review) | Gamma (30-80 Hz): local computation. Beta (15-30 Hz): feedback/maintenance. Theta (4-8 Hz): long-range coordination. Alpha (8-12 Hz): inhibition/gating. Phase coherence gates information flow. | Framework; replicated across modalities | **Theoretical foundation for OII frequency-band assignment.** Gamma = segregation, theta = integration, alpha = gating. Directly supports OII layer structure. |
| 7 | **Gnanateja et al. (2022)** — *On the Role of Neural Oscillations Across Timescales in Speech and Music Processing.* Frontiers in Computational Neuroscience, 16:872093. | Review (clinician-scientist targeted) | — (Review) | Delta: words/syntax/prosody. Theta: syllabic rate. Alpha: attention. Beta: auditory-motor coupling. Gamma: phonetic features. Theta-gamma coupling for hierarchical parsing. Music shares oscillatory processing with speech. | Framework; cited >100 papers | **Oscillatory frequency bands in music processing.** Confirms theta-gamma coupling framework extends to music. Supports OII's multi-band integration model. |
| 8 | **Hovsepyan et al. (2020)** — *Combining predictive coding and neural oscillations enables online syllable recognition in natural speech.* Nature Communications, 11:3117. | Computational model (Precoss) | — (Computational) | Theta-gamma coupling + predictive coding enables online syllable segmentation. Recognition best when theta resets align with syllable onsets. Model demonstrates that oscillatory parsing + prediction synergize. | Model performance: theta-gamma coupling improves recognition accuracy | **Computational validation of theta-gamma-prediction integration.** Supports OII's SYN.prediction_error + theta-gamma coupling architecture. Mode switching = prediction-driven oscillatory reset. |
| 9 | **Biau et al. (2025)** — *Neocortical and Hippocampal Theta Oscillations Track Audiovisual Integration and Replay of Speech Memories.* J. Neuroscience, 45(21):e1797242025. | MEG (275-ch), time-frequency, pattern reinstatement | 23 | Theta oscillations in neocortex and hippocampus track audiovisual synchrony during encoding. Theta asynchrony during encoding reduces theta reinstatement accuracy during memory recall. Phase-modulated plasticity: theta phase determines LTP/LTD in hippocampus. | Theta power: synchronous > asynchronous; Reinstatement: synchronous > asynchronous | **Theta as binding mechanism in hippocampal memory.** Confirms hippocampal theta mediates integration across modalities and supports memory encoding. Directly supports OII hippocampal theta-gamma coupling hub. |
| 10 | **Cabral et al. (2022)** — *Metastable oscillatory modes emerge from synchronization in the brain spacetime connectome.* Communications Physics, 5:184. | Computational model (delay-coupled damped oscillators), MEG validation | 89 (MEG validation) | Metastable oscillatory modes (MOMs) at sub-gamma frequencies emerge from delay-coupled local gamma oscillations in the connectome. Frequency, duration, scale controlled by global coupling parameters. Matches MEG power spectra. | Model fits MEG spectra from N=89 | **Computational basis for integration-segregation dynamics.** Metastable modes = transient integration/segregation states. Global coupling strength controls mode switching — parallels OII switching_efficiency parameter. |
| 11 | **Yuan et al. (2025)** — *Decoding Auditory Working Memory Load From EEG Alpha Oscillations.* Psychophysiology, 62:e70210. | EEG, MVPA decoding, temporal generalization | ~40 | Auditory WM load decoded from alpha-band oscillation patterns. Alpha patterns change dynamically during maintenance (dynamic coding). No CDA equivalent for auditory WM (vision-specific). | MVPA decoding: significant above chance; Dynamic coding: temporal generalization reveals changing patterns | **Alpha oscillations encode auditory WM load.** Supports OII alpha gating model: alpha power modulates sensory input gating. Dynamic coding = mode switching over time. |
| 12 | **Sturm et al. (2014)** — *ECoG high gamma activity reveals distinct cortical representations of lyrics passages, harmonic and timbre-related changes in a rock song.* Frontiers Human Neuroscience, 8:798. | ECoG (intracranial), high gamma (70-170 Hz), partial correlations | 10 (ECoG patients) | High gamma power in temporal auditory areas driven by vocal onset/offset in music. Subject-individual activation spots for intensity, timbre, and harmonic features. Context-dependent feature selection. | Partial correlations: significant for lyrics, harmonic change, timbre | **Gamma-band local feature extraction in auditory cortex.** Confirms OII Phase 1 (local feature extraction): gamma oscillations support fine spectral/temporal feature analysis. Distinct cortical representations for different musical features. |

### 3.2 The Temporal Story: Oscillatory Mode Dynamics

```
COMPLETE TEMPORAL PROFILE OF OSCILLATORY INTELLIGENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1: LOCAL FEATURE EXTRACTION (continuous, <100ms)
──────────────────────────────────────────────────────
Gamma oscillations (30-100 Hz) in auditory cortex.
Fine spectral and temporal features extracted.
R³ input: Consonance [0:7], Timbre [12:21], Change [21:25]
SYN.harmonic_syntax tracks ongoing harmonic state.

Phase 2: INTEGRATION BINDING (200-400ms, H10 window)
────────────────────────────────────────────────────
Theta oscillations (4-8 Hz) from frontal cortex.
Distributed features bound into unified percept.
SYN.prediction_error computes deviation from template.
Harmonic syntax expectation evaluated.

Phase 3: MODE SWITCHING (400-700ms, H14 window)
───────────────────────────────────────────────
Alpha oscillations (8-12 Hz) gate cortical input.
DLPFC coordinates integration vs segregation balance.
High Gf = faster, more adaptive switching.
SYN.structural_expect tracks closure/continuation.

Phase 4: PATTERN ENCODING (1-5s, H16-H20 window)
────────────────────────────────────────────────
Hippocampal theta-gamma coupling.
Sequential musical items encoded in gamma cycles
nested within theta oscillations.
MEM.encoding_state tracks binding success.
MEM.familiarity_proxy detects known patterns.

Phase 5: CONSOLIDATION (5-36s, H20-H24 window)
──────────────────────────────────────────────
Hippocampal-cortical dialogue.
Short-term representations consolidated.
Integration history updates Gf-dependent baseline.
MEM.retrieval_dynamics tracks recall readiness.
```

### 3.3 Effect Size Summary

```
PRIMARY EVIDENCE (Bruzzone et al. 2022):
  N = 66 (MEG), 67 (DTI); Gf groups: high N=38, average N=31
  Gf group separation:     t(55) = 11.08, p < 1e-7 (very large)
  Theta degree:            p < 0.001 (high Gf > average Gf)
  Alpha degree:            p < 0.001 (high Gf > average Gf)
  Gamma degree:            p < 0.001 (average Gf > high Gf, reversed)
  DTI structural degree:   p = 0.007 (high Gf > average Gf)
  Segregation coefficient: p < 0.001 (theta, alpha, DTI); p = 0.003 (gamma, reversed)

CROSS-FREQUENCY COUPLING (Borderie et al. 2024):
  Method: iEEG (intracranial), theta-gamma PAC
  Regions: STS, IFG, ITG, hippocampus
  ML decoding: correct vs incorrect trials from PAC strength
  PAC-STM correlation: positive (individual differences)

PITCH PROCESSING (Samiee et al. 2022):
  N = 16 (8 amusics, 8 controls)
  PAC group effect rAud:   F(1) = 11.1, p < 0.001
  PAC group effect rIFG:   F(1) = 43.95, p < 0.0001
  Delta coherence:         F(1) = 49.7, p < 0.0001

ENTRAINMENT (Ding et al. 2025):
  N = 31; EEG 64-ch
  ITPC: F(11,330) = 4.81, p < 0.001, eta2 = 0.14
  EPS:  F(11,330) = 14.10, p < 0.001, eta2 = 0.32

Papers:               12 (5 original research, 3 computational/review, 4 supporting)
Total N (original):   ~220 across empirical studies
Quality Assessment:   beta-tier — well-replicated across modalities (MEG, DTI, iEEG, EEG)
                      Cross-frequency coupling confirmed in hippocampus (intracranial)
                      Integration-segregation model replicated (Bruzzone + Cabral + Fries)
Key limitation:       No single study combines music + Gf + oscillatory connectivity.
                      Bruzzone 2022 uses resting-state (not music). Music-specific
                      oscillatory intelligence awaits direct investigation.
```

---

## 4. R³ Input Mapping: What OII Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | OII Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **A: Consonance** | [0] | roughness | Gamma-band complexity proxy | Roughness = unresolved harmonics = local processing demand |
| **A: Consonance** | [1] | sethares_dissonance | Harmonic regularity (inverse) | Irregular = higher integration demand |
| **A: Consonance** | [3] | stumpf_fusion | Integration binding success | Tonal fusion = theta-mediated binding |
| **A: Consonance** | [4] | sensory_pleasantness | Encoding reward signal | Pleasantness facilitates encoding |
| **A: Consonance** | [5] | periodicity | Oscillatory regularity proxy | High periodicity = stable theta phase |
| **A: Consonance** | [6] | inharmonicity | Integration challenge | Inharmonic = harder to integrate |
| **B: Energy** | [7] | amplitude | Processing intensity | Energy = oscillatory power |
| **B: Energy** | [10] | loudness | Arousal / oscillatory drive | Stevens 1957 psychophysical |
| **B: Energy** | [11] | onset_strength | Mode switch trigger | Transient = gamma burst |
| **C: Timbre** | [12] | warmth | Slow integration quality | Low-frequency = theta-band affinity |
| **C: Timbre** | [14] | tonalness | Harmonic integration measure | Harmonic-to-noise = integration success |
| **C: Timbre** | [15] | spectral_centroid | Frequency balance | Balance = integration/segregation equilibrium |
| **D: Change** | [21] | spectral_flux | Mode switching trigger | Flux = integration-segregation transition |
| **D: Change** | [22] | entropy | Integration demand | Low entropy = easy integration; high = segregation needed |
| **D: Change** | [23] | spectral_change | Temporal dynamics | Rate of spectral evolution |
| **D: Change** | [24] | spectral_concentration | Segregation proxy | Concentrated = local; distributed = integrated |
| **E: Interactions** | [25:33] | x_l0l5 (Energy x Consonance) | Integration efficiency | Energy-consonance coupling = binding success |
| **E: Interactions** | [33:41] | x_l4l5 (Derivatives x Consonance) | Mode switching dynamics | Change rate x consonance = switch cost |
| **E: Interactions** | [41:49] | x_l5l7 (Consonance x Timbre) | Slow integration binding | Consonance-timbre = theta integration quality |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | OII Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **G: Rhythm** | [72] | event_density | Oscillatory load — event rate drives gamma burst frequency | Giraud & Poeppel 2012: event rate ↔ cortical oscillation band |
| **G: Rhythm** | [74] | rhythmic_regularity | Entrainment quality — regular rhythms stabilize theta phase | Large & Palmer 2002 |

**Rationale**: OII models oscillatory integration/segregation dynamics. Event density directly determines the frequency band of cortical oscillatory engagement (high event density maps to gamma, low to theta). Rhythmic regularity quantifies how well temporal structure supports stable phase-locking, the mechanism by which theta oscillations bind distributed representations into integrated percepts.

> **Code impact**: These features are doc-only until Phase 5 wiring. No changes to `oii.py`.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[3] stumpf_fusion ──────────────► Theta integration binding success
R³[5] periodicity ─────────────────► Oscillatory regularity
                                     Math: integration = σ(0.3·fusion + 0.2·period.)

R³[11] onset_strength ────────────► Gamma burst trigger → mode switch
R³[21] spectral_flux ──────────────► Integration-segregation transition
                                     Math: switch = σ(0.25·onset + 0.25·flux)

R³[22] entropy ────────────────────► Integration demand
                                     Low entropy → integration mode (theta)
                                     High entropy → segregation mode (gamma)

R³[25:33] x_l0l5 ─────────────────► Binding quality
                                     Energy-consonance coupling = theta success

R³[33:41] x_l4l5 ─────────────────► Mode switching cost
                                     Derivative-consonance = transition difficulty

R³[41:49] x_l5l7 ─────────────────► Slow integration quality
                                     Consonance-timbre = theta-alpha coherence
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

OII requires H³ features at both SYN horizons (H10, H14, H18) and MEM horizons (H16, H20, H24).

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 3 | stumpf_fusion | 10 | M1 (mean) | L2 (bidirectional) | Harmonic binding state at chord level |
| 3 | stumpf_fusion | 14 | M1 (mean) | L0 (forward) | Binding over progression window |
| 3 | stumpf_fusion | 18 | M1 (mean) | L0 (forward) | Phrase-level binding stability |
| 5 | periodicity | 10 | M0 (value) | L2 (bidirectional) | Current oscillatory regularity |
| 5 | periodicity | 14 | M14 (periodicity) | L0 (forward) | Regularity of regularity (meta) |
| 22 | entropy | 10 | M0 (value) | L2 (bidirectional) | Current integration demand |
| 22 | entropy | 14 | M1 (mean) | L0 (forward) | Average complexity over progression |
| 22 | entropy | 18 | M19 (stability) | L0 (forward) | Complexity stability over phrase |
| 11 | onset_strength | 10 | M0 (value) | L2 (bidirectional) | Current gamma burst trigger |
| 11 | onset_strength | 14 | M8 (velocity) | L0 (forward) | Mode switching rate |
| 21 | spectral_flux | 10 | M0 (value) | L2 (bidirectional) | Current transition signal |
| 21 | spectral_flux | 18 | M1 (mean) | L0 (forward) | Average transition over phrase |
| 10 | loudness | 16 | M0 (value) | L2 (bidirectional) | Current oscillatory drive |
| 10 | loudness | 20 | M1 (mean) | L0 (forward) | Average drive over consolidation |
| 14 | tonalness | 16 | M0 (value) | L2 (bidirectional) | Current harmonic integration |
| 14 | tonalness | 20 | M1 (mean) | L0 (forward) | Tonal stability over 5s |
| 4 | sensory_pleasantness | 16 | M0 (value) | L2 (bidirectional) | Current encoding reward |
| 4 | sensory_pleasantness | 20 | M18 (trend) | L0 (forward) | Pleasantness trajectory |
| 0 | roughness | 16 | M0 (value) | L2 (bidirectional) | Current gamma-band demand |
| 0 | roughness | 24 | M1 (mean) | L0 (forward) | Average dissonance over episodic chunk |
| 7 | amplitude | 16 | M8 (velocity) | L0 (forward) | Energy change rate (switch trigger) |
| 7 | amplitude | 20 | M4 (max) | L0 (forward) | Peak energy over consolidation window |
| 15 | spectral_centroid | 10 | M0 (value) | L2 (bidirectional) | Frequency balance |
| 15 | spectral_centroid | 18 | M3 (std) | L0 (forward) | Balance variability over phrase |

**v1 demand**: 24 tuples

#### R³ v2 Projected Expansion

No significant v2 expansion projected. OII's oscillatory integration-segregation dynamics are fully captured by v1 spectral features (roughness, entropy, onset, flux, interactions). The v2 rhythm and harmony groups do not directly map to the cross-frequency coupling mechanism.

**v2 projected**: 0 tuples
**Total projected**: 24 tuples of 294,912 theoretical = 0.0081%

### 5.2 Mechanism Binding

OII reads from two mechanisms in the mnemonic circuit:

**SYN** (Syntactic Processing, 30D) — H10/H14/H18:

| SYN Sub-section | Range | OII Role | Weight |
|-----------------|-------|----------|--------|
| **Harmonic Syntax** | SYN[0:10] | Integration state: theta-mediated binding of harmonic structure | **1.0** (primary) |
| **Prediction Error** | SYN[10:20] | Mode switching trigger: error signals drive gamma → theta transitions | 0.8 |
| **Structural Expectation** | SYN[20:30] | Closure/continuation: determines integration vs. segregation demand | 0.7 |

**MEM** (Memory Encoding & Retrieval, 30D) — H16/H20/H24:

| MEM Sub-section | Range | OII Role | Weight |
|-----------------|-------|----------|--------|
| **Encoding State** | MEM[0:10] | Binding success: how well current input is encoded | 0.8 |
| **Familiarity Proxy** | MEM[10:20] | Pattern recognition: familiar = theta-dominant; novel = gamma-dominant | 0.7 |
| **Retrieval Dynamics** | MEM[20:30] | Recall readiness: integrated representation strength | 0.6 |

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
OII OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
Manifold range: IMU OII [306:316]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EPISODIC OSCILLATORY FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 0  │ f16_slow_integration│ [0, 1] │ Theta/alpha integration strength.
    │                     │        │ Frontal theta → temporal alpha coherence.
    │                     │        │ f16 = σ(0.30·SYN.syntax.mean + 0.20·fusion_h10)
    │                     │        │ |w| sum = 0.50
────┼─────────────────────┼────────┼────────────────────────────────────────────
 1  │ f17_fast_segregation│ [0, 1] │ Gamma-band local processing efficiency.
    │                     │        │ Temporal cortex gamma segregation.
    │                     │        │ f17 = σ(0.25·roughness + 0.25·onset_h10)
    │                     │        │ |w| sum = 0.50
────┼─────────────────────┼────────┼────────────────────────────────────────────
 2  │ f18_mode_switching  │ [0, 1] │ Integration-segregation switch efficiency.
    │                     │        │ DLPFC-mediated mode coordination.
    │                     │        │ f18 = σ(0.20·SYN.predict_err.mean
    │                     │        │       + 0.15·flux_h10
    │                     │        │       + 0.15·MEM.encoding.mean)
    │                     │        │ |w| sum = 0.50

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 3  │ gf_proxy            │ [0, 1] │ Fluid intelligence proxy.
    │                     │        │ f(slow_integration × (1 - fast_segregation)
    │                     │        │   + fast_segregation × (1 - slow_integration))
    │                     │        │ Gf = balanced switching, not dominance.
────┼─────────────────────┼────────┼────────────────────────────────────────────
 4  │ switching_efficiency│ [0, 1] │ Mode switching efficiency metric.
    │                     │        │ |d(integration)/dt| × |d(segregation)/dt|
    │                     │        │ Fast complementary transitions = high Gf.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 5  │ integration_state   │ [0, 1] │ Current theta/alpha integration level.
    │                     │        │ SYN.harmonic_syntax aggregation.
────┼─────────────────────┼────────┼────────────────────────────────────────────
 6  │ segregation_state   │ [0, 1] │ Current gamma segregation level.
    │                     │        │ High roughness + high onset = segregation.
────┼─────────────────────┼────────┼────────────────────────────────────────────
 7  │ encoding_quality    │ [0, 1] │ Pattern encoding success (integration result).
    │                     │        │ MEM.encoding_state × SYN.syntax integration.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 8  │ integration_pred    │ [0, 1] │ Integration mode prediction (1-2s ahead).
    │                     │        │ SYN.structural_expect trajectory.
────┼─────────────────────┼────────┼────────────────────────────────────────────
 9  │ segregation_pred    │ [0, 1] │ Segregation mode prediction (0.5-1s ahead).
    │                     │        │ MEM.encoding × entropy trajectory.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Core Model: Integration-Segregation Balance

```
Oscillatory Intelligence = f(Integration, Segregation, Switching)

where:
  Integration   = theta/alpha long-range binding (SYN-derived)
  Segregation   = gamma local processing (R³-derived)
  Switching     = mode transition efficiency (SYN × MEM interaction)

Gf_proxy = Integration × (1 - Segregation) + Segregation × (1 - Integration)
         = XOR-like: high when modes are complementary, low when both active/inactive

Key insight: High Gf is NOT high integration OR high segregation alone,
but efficient SWITCHING between them.
```

### 7.2 Feature Formulas

All formulas use `g()` notation where `g(x)` is the MORPH_SCALE mapped value in [-3, +3], then passed through sigmoid. For all sigmoid(sum), |w_i| sum <= 1.0.

```python
# ═══ LAYER E: Episodic Oscillatory Features ═══

# f16: Slow Integration — theta/alpha binding strength
# SYN.syntax provides harmonic binding state; stumpf_fusion at H10 gives binding quality
# |w| = 0.30 + 0.20 = 0.50 <= 1.0
f16 = sigmoid(0.30 * g(mean(SYN.harmonic_syntax[0:10]))
            + 0.20 * g(H3[stumpf_fusion, H10, M1, L2]))

# f17: Fast Segregation — gamma local processing efficiency
# Roughness drives gamma demand; onset_strength at H10 gives gamma burst detection
# |w| = 0.25 + 0.25 = 0.50 <= 1.0
f17 = sigmoid(0.25 * g(R3.roughness[0])
            + 0.25 * g(H3[onset_strength, H10, M0, L2]))

# f18: Mode Switching — integration-segregation transition efficiency
# SYN.prediction_error drives switch need; flux triggers transition; MEM.encoding tracks result
# |w| = 0.20 + 0.15 + 0.15 = 0.50 <= 1.0
f18 = sigmoid(0.20 * g(mean(SYN.prediction_error[10:20]))
            + 0.15 * g(H3[spectral_flux, H10, M0, L2])
            + 0.15 * g(mean(MEM.encoding_state[0:10])))

# ═══ LAYER M: Mathematical Model Outputs ═══

# gf_proxy: Fluid intelligence proxy — balanced switching, not raw magnitude
gf_proxy = f16 * (1.0 - f17) + f17 * (1.0 - f16)
# This implements XOR: peaks when one mode is high and the other low
# = efficient complementary activation

# switching_efficiency: How fast and cleanly modes transition
# Uses H14 velocity morphs for dynamic assessment
onset_vel = H3[onset_strength, H14, M8, L0]     # mode switch rate
entropy_stability = H3[entropy, H18, M19, L0]    # pattern stability
switching_efficiency = sigmoid(0.25 * g(onset_vel)
                             + 0.25 * g(entropy_stability))
# |w| = 0.25 + 0.25 = 0.50 <= 1.0

# ═══ LAYER P: Present Processing ═══

# integration_state: Current theta/alpha level (from SYN harmonic syntax)
integration_state = sigmoid(0.30 * g(mean(SYN.harmonic_syntax[0:10]))
                          + 0.20 * g(H3[tonalness, H16, M0, L2]))
# |w| = 0.30 + 0.20 = 0.50 <= 1.0

# segregation_state: Current gamma level
segregation_state = sigmoid(0.25 * g(R3.roughness[0])
                          + 0.25 * g(R3.entropy[22]))
# |w| = 0.25 + 0.25 = 0.50 <= 1.0

# encoding_quality: Pattern encoding success (integration × memory binding)
encoding_quality = sigmoid(0.25 * g(mean(MEM.encoding_state[0:10]))
                         + 0.25 * g(mean(SYN.harmonic_syntax[0:10])))
# |w| = 0.25 + 0.25 = 0.50 <= 1.0

# ═══ LAYER F: Future Predictions ═══

# integration_pred: Predicted integration state (SYN.structural_expect trajectory)
integration_pred = sigmoid(0.25 * g(mean(SYN.structural_expect[20:30]))
                         + 0.20 * g(H3[stumpf_fusion, H18, M1, L0]))
# |w| = 0.25 + 0.20 = 0.45 <= 1.0

# segregation_pred: Predicted segregation state (entropy + onset trajectory)
segregation_pred = sigmoid(0.20 * g(H3[entropy, H14, M1, L0])
                         + 0.20 * g(H3[onset_strength, H14, M8, L0]))
# |w| = 0.20 + 0.20 = 0.40 <= 1.0
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | Source | OII Function |
|--------|-----------------|----------|---------------|--------|--------------|
| **Superior frontal gyrus (SFG)** | AAL bilateral | 3 | Direct (MEG) | Bruzzone 2022: high Gf = stronger theta/alpha degree (p<0.001) | Theta generation, long-range integration hub |
| **DLPFC (BA9)** | ±44, 36, 28 | 2 | Direct (EEG) | Ding 2025: frontocentral entrainment (BA6/BA8/BA9); Bruzzone 2022: frontal subnetwork | Mode switching, executive control, entrainment |
| **Supplementary motor area (SMA)** | AAL bilateral | 2 | Direct (MEG) | Bruzzone 2022: high Gf = stronger structural degree; Samiee 2022: motor cortex PTE beta→Aud | Motor-to-auditory top-down beta signaling |
| **Superior temporal gyrus (STG)** | ±60, -32, 8 | 5 | Direct (MEG, iEEG) | Samiee 2022: rAud PAC delta-beta F(1)=11.1; Borderie 2024: STS theta-gamma PAC; Sturm 2014: ECoG high gamma | Alpha gating, gamma local processing, delta tracking |
| **Middle temporal gyrus (MTG)** | ±62, -24, -4 | 2 | Direct (MEG) | Bruzzone 2022: temporal subnetwork theta/alpha degree; Gnanateja 2022 review | Gamma-band local processing, feature extraction |
| **Inferior frontal gyrus (IFG/BA45)** | ±48, 28, 8 | 4 | Direct (MEG, iEEG) | Samiee 2022: rIFG PAC F(1)=43.95, p<0.0001; Borderie 2024: IFG theta-gamma PAC in STM | Cross-frequency coupling hub, pitch deviance detection, auditory STM |
| **Hippocampus** | ±20, -24, -12 | 88 | Direct (iEEG, MEG) | Borderie 2024: hippocampal theta-gamma PAC for auditory STM; Biau 2025: hippocampal theta for memory encoding | Theta-gamma coupling, sequential encoding, memory binding |
| **Parahippocampal gyrus** | ±24, -32, -12 | 2 | Direct (MEG) | Bruzzone 2022: parahippocampal degree in theta/alpha functional connectivity | Memory-guided oscillatory patterns, integration support |
| **Inferior/superior parietal lobule** | AAL bilateral | 2 | Direct (MEG, DTI) | Bruzzone 2022: parietal subnetwork degree significant in both DTI and MEG theta/alpha | Parieto-frontal integration (P-FIT model), WM maintenance |
| **Cingulate gyrus** | AAL bilateral | 1 | Direct (MEG) | Bruzzone 2022: cingulate community assignment differs between high/average Gf groups | Integration-segregation mode indicator; frontal subnetwork in high Gf |

**Note on coordinates**: Bruzzone et al. (2022) used AAL parcellation (90 ROIs) for both DTI tractography and MEG source reconstruction. Individual ROI MNI centroids follow standard AAL atlas coordinates. Samiee et al. (2022) used functional localizers registered to individual anatomy for STG, IFG, and motor ROIs.

---

## 9. Cross-Unit Pathways

### 9.1 OII Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OII INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (IMU):                                                         │
│  OII ──────► PMIM (Predictive Memory Integration Model)                   │
│       │      └── Integration-segregation state feeds prediction error      │
│       │                                                                     │
│       ├─────► MEAMN (Music-Evoked Autobiographical Memory Network)        │
│       │      └── Encoding quality modulates memory binding success         │
│       │                                                                     │
│       ├─────► HCMC (Hippocampal-Cortical Memory Circuit)                  │
│       │      └── Theta-gamma coupling drives hippocampal encoding          │
│       │                                                                     │
│       ├─────► PNH (Pythagorean Neural Hierarchy)                          │
│       │      └── Harmonic syntax state supports interval encoding          │
│       │                                                                     │
│       └─────► MSPBA (Musical Syntax Processing in Broca's Area)           │
│              └── Prediction error feeds syntactic violation detection       │
│                                                                             │
│  SHARED MECHANISMS:                                                         │
│  SYN ◄──────── PNH, PMIM, MSPBA, TPRD, CMAPCC                           │
│  MEM ◄──────── MEAMN, MMP, HCMC, RASN, RIRI, VRIAP, DMMS, CSSL, CDEM   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Brain Pathway Cross-References

OII reads from the unified Brain (26D) for shared state:

| Brain Dimension | Index (MI-space) | OII Role |
|-----------------|-------------------|----------|
| arousal | [177] | Oscillatory drive level |
| prediction_error | [178] | Mode switching trigger |
| loudness_max | [179] | Processing intensity baseline |
| emotional_momentum | [180] | Sustained engagement modulates encoding |

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Theta disruption** | TMS disruption of frontal theta should impair integration (reduce f16) | Testable |
| **Gamma enhancement** | Gamma-band entrainment should enhance local processing (increase f17) | Testable |
| **Gf correlation** | OII.gf_proxy should correlate with standard Gf measures (e.g., Raven's) | Testable |
| **Mode switching speed** | High Gf individuals should show faster integration-segregation transitions | Testable |
| **Musical training** | Trained musicians should show higher switching_efficiency than non-musicians | Testable |
| **Cross-frequency coupling** | Theta-gamma coupling strength should predict encoding_quality | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class OII(BaseModel):
    """Oscillatory Intelligence Integration.

    Output: 10D per frame.
    Reads: SYN mechanism (30D), MEM mechanism (30D), R³ direct.
    Zero learned parameters.
    """
    NAME = "OII"
    UNIT = "IMU"
    TIER = "β3"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("SYN", "MEM")

    # All coefficient |w| sums <= 1.0 per sigmoid call
    W_SYN_SYNTAX = 0.30       # slow integration: SYN harmonic syntax weight
    W_FUSION = 0.20           # slow integration: stumpf fusion weight
    W_ROUGHNESS = 0.25        # fast segregation: roughness weight
    W_ONSET = 0.25            # fast segregation: onset strength weight
    W_PRED_ERR = 0.20         # mode switching: SYN prediction error weight
    W_FLUX = 0.15             # mode switching: spectral flux weight
    W_MEM_ENC = 0.15          # mode switching: MEM encoding weight
    W_ONSET_VEL = 0.25        # switching efficiency: onset velocity
    W_ENT_STAB = 0.25         # switching efficiency: entropy stability
    W_TONALNESS = 0.20        # integration state: tonalness weight
    W_ENTROPY_P = 0.25        # segregation state: entropy weight
    W_STRUCT = 0.25           # integration pred: structural expect weight
    W_FUSION_P = 0.20         # integration pred: fusion trajectory weight
    W_ENT_PRED = 0.20         # segregation pred: entropy trajectory
    W_ONS_PRED = 0.20         # segregation pred: onset trajectory

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """24 tuples for OII computation."""
        return [
            # SYN horizons (H10, H14, H18)
            # (r3_idx, horizon, morph, law)
            (3, 10, 1, 2),     # stumpf_fusion, 400ms, mean, bidirectional
            (3, 14, 1, 0),     # stumpf_fusion, 700ms, mean, forward
            (3, 18, 1, 0),     # stumpf_fusion, 2s, mean, forward
            (5, 10, 0, 2),     # periodicity, 400ms, value, bidirectional
            (5, 14, 14, 0),    # periodicity, 700ms, periodicity, forward
            (22, 10, 0, 2),    # entropy, 400ms, value, bidirectional
            (22, 14, 1, 0),    # entropy, 700ms, mean, forward
            (22, 18, 19, 0),   # entropy, 2s, stability, forward
            (11, 10, 0, 2),    # onset_strength, 400ms, value, bidirectional
            (11, 14, 8, 0),    # onset_strength, 700ms, velocity, forward
            (21, 10, 0, 2),    # spectral_flux, 400ms, value, bidirectional
            (21, 18, 1, 0),    # spectral_flux, 2s, mean, forward
            (15, 10, 0, 2),    # spectral_centroid, 400ms, value, bidirectional
            (15, 18, 3, 0),    # spectral_centroid, 2s, std, forward
            # MEM horizons (H16, H20, H24)
            (10, 16, 0, 2),    # loudness, 1s, value, bidirectional
            (10, 20, 1, 0),    # loudness, 5s, mean, forward
            (14, 16, 0, 2),    # tonalness, 1s, value, bidirectional
            (14, 20, 1, 0),    # tonalness, 5s, mean, forward
            (4, 16, 0, 2),     # sensory_pleasantness, 1s, value, bidirectional
            (4, 20, 18, 0),    # sensory_pleasantness, 5s, trend, forward
            (0, 16, 0, 2),     # roughness, 1s, value, bidirectional
            (0, 24, 1, 0),     # roughness, 36s, mean, forward
            (7, 16, 8, 0),     # amplitude, 1s, velocity, forward
            (7, 20, 4, 0),     # amplitude, 5s, max, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute OII 10D output.

        Args:
            mechanism_outputs: {"SYN": (B,T,30), "MEM": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) OII output
        """
        syn = mechanism_outputs["SYN"]    # (B, T, 30)
        mem = mechanism_outputs["MEM"]    # (B, T, 30)

        # SYN sub-sections
        syn_syntax = syn[..., 0:10]       # harmonic syntax
        syn_predict = syn[..., 10:20]     # prediction error
        syn_struct = syn[..., 20:30]      # structural expectation

        # MEM sub-sections
        mem_encoding = mem[..., 0:10]     # encoding state

        # R³ features
        roughness = r3[..., 0:1]          # [0, 1]
        onset_str = r3[..., 11:12]        # [0, 1]
        entropy = r3[..., 22:23]          # [0, 1]

        # H³ direct reads
        fusion_h10 = h3_direct[(3, 10, 1, 2)]    # stumpf mean at 400ms
        onset_h10 = h3_direct[(11, 10, 0, 2)]    # onset value at 400ms
        flux_h10 = h3_direct[(21, 10, 0, 2)]     # flux value at 400ms
        onset_vel_h14 = h3_direct[(11, 14, 8, 0)] # onset velocity at 700ms
        ent_stab_h18 = h3_direct[(22, 18, 19, 0)] # entropy stability at 2s
        tonalness_h16 = h3_direct[(14, 16, 0, 2)] # tonalness at 1s
        struct_mean = syn_struct.mean(-1, keepdim=True)
        fusion_h18 = h3_direct[(3, 18, 1, 0)]    # fusion mean at 2s
        ent_h14 = h3_direct[(22, 14, 1, 0)]      # entropy mean at 700ms

        # ═══ LAYER E: Episodic Features ═══
        # f16: Slow Integration — |w| = 0.30 + 0.20 = 0.50
        f16 = torch.sigmoid(
            self.W_SYN_SYNTAX * syn_syntax.mean(-1, keepdim=True)
            + self.W_FUSION * fusion_h10.unsqueeze(-1)
        )

        # f17: Fast Segregation — |w| = 0.25 + 0.25 = 0.50
        f17 = torch.sigmoid(
            self.W_ROUGHNESS * roughness
            + self.W_ONSET * onset_h10.unsqueeze(-1)
        )

        # f18: Mode Switching — |w| = 0.20 + 0.15 + 0.15 = 0.50
        f18 = torch.sigmoid(
            self.W_PRED_ERR * syn_predict.mean(-1, keepdim=True)
            + self.W_FLUX * flux_h10.unsqueeze(-1)
            + self.W_MEM_ENC * mem_encoding.mean(-1, keepdim=True)
        )

        # ═══ LAYER M: Mathematical ═══
        # gf_proxy: XOR-like balanced switching
        gf_proxy = (f16 * (1.0 - f17) + f17 * (1.0 - f16)).clamp(0, 1)

        # switching_efficiency — |w| = 0.25 + 0.25 = 0.50
        switch_eff = torch.sigmoid(
            self.W_ONSET_VEL * onset_vel_h14.unsqueeze(-1)
            + self.W_ENT_STAB * ent_stab_h18.unsqueeze(-1)
        )

        # ═══ LAYER P: Present ═══
        # integration_state — |w| = 0.30 + 0.20 = 0.50
        integ_state = torch.sigmoid(
            self.W_SYN_SYNTAX * syn_syntax.mean(-1, keepdim=True)
            + self.W_TONALNESS * tonalness_h16.unsqueeze(-1)
        )

        # segregation_state — |w| = 0.25 + 0.25 = 0.50
        seg_state = torch.sigmoid(
            self.W_ROUGHNESS * roughness
            + self.W_ENTROPY_P * entropy
        )

        # encoding_quality — |w| = 0.25 + 0.25 = 0.50
        enc_qual = torch.sigmoid(
            0.25 * mem_encoding.mean(-1, keepdim=True)
            + 0.25 * syn_syntax.mean(-1, keepdim=True)
        )

        # ═══ LAYER F: Future ═══
        # integration_pred — |w| = 0.25 + 0.20 = 0.45
        integ_pred = torch.sigmoid(
            self.W_STRUCT * syn_struct.mean(-1, keepdim=True)
            + self.W_FUSION_P * fusion_h18.unsqueeze(-1)
        )

        # segregation_pred — |w| = 0.20 + 0.20 = 0.40
        seg_pred = torch.sigmoid(
            self.W_ENT_PRED * ent_h14.unsqueeze(-1)
            + self.W_ONS_PRED * onset_vel_h14.unsqueeze(-1)
        )

        return torch.cat([
            f16, f17, f18,                           # E: 3D
            gf_proxy, switch_eff,                     # M: 2D
            integ_state, seg_state, enc_qual,         # P: 3D
            integ_pred, seg_pred,                     # F: 2D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 (5 original research + 3 computational/review + 4 supporting) | Deep literature review v2.1.0 |
| **Total N (empirical)** | ~220 across original studies | Bruzzone N=66/67, Samiee N=16, Borderie iEEG, Biau N=23, Ding N=31, Dobri young+older, Yuan ~40, Sturm N=10, Cabral N=89 |
| **Primary Effect** | Theta/alpha degree p<0.001; gamma reversed p<0.001 | Bruzzone et al. 2022 (Gf connectivity) |
| **Cross-frequency coupling** | Theta-gamma PAC in hippocampus for auditory STM | Borderie et al. 2024 (iEEG, intracranial) |
| **Pitch PAC** | Delta-beta PAC F(1)=43.95, p<0.0001 in IFG | Samiee et al. 2022 (MEG) |
| **Entrainment** | ITPC eta2=0.14, EPS eta2=0.32 | Ding et al. 2025 (EEG N=31) |
| **Evidence Modalities** | DTI, MEG, iEEG (intracranial), EEG, ECoG, MR spectroscopy, computational modeling | Multi-modal convergence |
| **Brain Regions** | 10 (6→10; +IFG, +SMA, +parietal, +cingulate) | Verified from Bruzzone, Samiee, Borderie |
| **Falsification Tests** | 0/6 confirmed (all testable) | Awaiting validation |
| **R³ Features Used** | 38D of 49D | Comprehensive |
| **H³ Demand** | 24 tuples (1.04%) | Sparse, efficient |
| **SYN Mechanism** | 30D (3 sub-sections) | Integration/syntax/prediction |
| **MEM Mechanism** | 30D (3 sub-sections) | Encoding/familiarity/retrieval |
| **Output Dimensions** | **10D** | 4-layer structure (E3/M2/P3/F2) |
| **Doc-code mismatches** | 7 noted | MECHANISM_NAMES, LAYERS, h3_demand, brain_regions, dimension_names, citations, paper_count |

---

## 13. Scientific References

### Primary Evidence (in catalog)
1. **Bruzzone, S. E. P., Lumaca, M., Brattico, E., Vuust, P., Kringelbach, M. L., & Bonetti, L. (2022)**. Dissociated brain functional connectivity of fast versus slow frequencies underlying individual differences in fluid intelligence: a DTI and MEG study. *Scientific Reports*, 12:4746. https://doi.org/10.1038/s41598-022-08521-5. **N=66 (MEG), 67 (DTI). High Gf: stronger theta/alpha degree p<0.001; reversed gamma p<0.001.**
2. **Samiee, S., Vuvan, D., Florin, E., Albouy, P., Peretz, I., & Baillet, S. (2022)**. Cross-Frequency Brain Network Dynamics Support Pitch Change Detection. *Journal of Neuroscience*, 42(18):3823-3835. https://doi.org/10.1523/JNEUROSCI.0630-21.2022. **N=16. Delta-beta PAC in rAud/rIFG; directed PTE.**
3. **Borderie, A., Caclin, A., Lachaux, J.-P., Perrone-Bertollotti, M., Hoyer, R. S., Kahane, P., Catenoix, H., Tillmann, B., & Albouy, P. (2024)**. Cross-frequency coupling in cortico-hippocampal networks supports the maintenance of sequential auditory information in short-term memory. *PLOS Biology*, 22(3):e3002512. **iEEG. Theta-gamma PAC in hippocampus for auditory STM.**
4. **Dobri, S., Chen, J. J., & Ross, B. (2023)**. Synchrony in auditory 40-Hz gamma oscillations increases in older age and correlates with hearing abilities and cortical GABA levels. *Imaging Neuroscience*, 1:imag_a_00035. **MEG. 40-Hz ASSR, GABA correlation.**
5. **Ding, J., Zhang, X., Liu, J., Hu, Z., Yang, Z., Tang, Y., & Ding, Y. (2025)**. Entrainment of rhythmic tonal sequences on neural oscillations and the impact on subjective emotion. *Scientific Reports*. https://doi.org/10.1038/s41598-025-98548-1. **N=31 EEG. ITPC eta2=0.14, EPS eta2=0.32.**
6. **Fries, P. (2015)**. Rhythms for Cognition: Communication through Coherence. *Neuron*, 88(1):220-235. **Review. CTC framework: gamma=local, theta=long-range, alpha=gating.**
7. **Gnanateja, G. N., Devaraju, D. S., Heyne, M., Quique, Y. M., Sitek, K. R., Tardif, M. C., Tessmer, R., & Dial, H. R. (2022)**. On the Role of Neural Oscillations Across Timescales in Speech and Music Processing. *Frontiers in Computational Neuroscience*, 16:872093. **Review. Oscillatory bands in music/speech processing.**
8. **Hovsepyan, S., Olasagasti, I., & Giraud, A.-L. (2020)**. Combining predictive coding and neural oscillations enables online syllable recognition in natural speech. *Nature Communications*, 11:3117. **Computational model. Theta-gamma + predictive coding.**
9. **Biau, E., Wang, D., Park, H., Jensen, O., & Hanslmayr, S. (2025)**. Neocortical and Hippocampal Theta Oscillations Track Audiovisual Integration and Replay of Speech Memories. *Journal of Neuroscience*, 45(21):e1797242025. **N=23 MEG. Hippocampal theta for memory encoding/replay.**
10. **Cabral, J., Castaldo, F., Vohryzek, J., et al. (2022)**. Metastable oscillatory modes emerge from synchronization in the brain spacetime connectome. *Communications Physics*, 5:184. **N=89 MEG validation. Delay-coupled oscillator model.**

### Supporting Evidence (in catalog)
11. **Yuan, Y., Gayet, S., Wisman, D. C., van der Stigchel, S., & van der Stoep, N. (2025)**. Decoding Auditory Working Memory Load From EEG Alpha Oscillations. *Psychophysiology*, 62:e70210. **Alpha patterns decode auditory WM load; dynamic coding.**
12. **Sturm, I., Blankertz, B., Potes, C., Schalk, G., & Curio, G. (2014)**. ECoG high gamma activity reveals distinct cortical representations of lyrics passages, harmonic and timbre-related changes in a rock song. *Frontiers in Human Neuroscience*, 8:798. **N=10 ECoG. High gamma (70-170 Hz) for music feature extraction.**

### Classic/Textbook References (not in catalog)
13. **Buzsaki, G. (2006)**. *Rhythms of the Brain*. Oxford University Press. Theta-gamma coupling framework.
14. **Klimesch, W. (2012)**. Alpha-band oscillations, attention, and controlled access to stored information. *Trends in Cognitive Sciences*.
15. **Canolty, R. T., & Knight, R. T. (2010)**. The functional role of cross-frequency coupling. *Trends in Cognitive Sciences*.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0 (v2.0.0) and v2.0.0→v2.1.0

**v2.0.0→v2.1.0 changes (2026-02-13)**:
- Evidence table: 5 vague entries → 12 verified papers with full citations, N, methods, effect sizes
- Brain regions: 6 → 10 regions; added IFG (Samiee/Borderie), SMA (Bruzzone/Samiee), parietal lobule (Bruzzone), cingulate gyrus (Bruzzone)
- Effect sizes: replaced single "d=2.99" with proper statistical reporting from Bruzzone 2022 (p-values per frequency band)
- Cross-frequency coupling: now supported by intracranial iEEG evidence (Borderie 2024) not just inferred
- Entrainment: added Ding 2025 (N=31, ITPC eta2=0.14, EPS eta2=0.32) with 6 Hz theta-alpha boundary
- References: 6 → 15 (12 in catalog + 3 classic textbook)
- Doc-code mismatches: 7 documented (MECHANISM_NAMES, LAYERS, h3_demand, brain_regions, dimension_names, citations, paper_count)

| Aspect | D0 (v1.0.0) | MI (v2.0.0→v2.1.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, TIH, BND) | SYN (30D) + MEM (30D) mechanisms |
| Slow integration | S⁰.L9.mean × HC⁰.OSC | R³.stumpf × SYN.harmonic_syntax |
| Fast segregation | S⁰.L4.velocity × HC⁰.TIH | R³.roughness × H³.onset_strength |
| Mode switching | S⁰.L3.coherence × HC⁰.BND | SYN.prediction_error × MEM.encoding |
| Output dims | 11D | **10D** (removed reserved dim) |
| Demand format | HC⁰ index ranges (39 tuples) | H³ 4-tuples (24 tuples, sparse) |
| Total demand | 39/2304 = 1.69% | 24/2304 = 1.04% |
| Coefficient rule | No constraint | **|w_i| sum <= 1.0 per sigmoid** |

### Why SYN + MEM replaces HC⁰ mechanisms

The D0 pipeline used 3 separate HC⁰ mechanisms (OSC, TIH, BND). In MI, these map to two mnemonic-circuit mechanisms:

- **OSC → SYN.harmonic_syntax** [0:10]: Neural oscillation coupling maps to harmonic syntax state — theta/alpha integration of harmonic structure.
- **TIH → SYN.prediction_error** [10:20] + **SYN.structural_expect** [20:30]: Temporal integration hierarchy maps to prediction error (surprise-driven mode switch) and structural expectation (closure detection).
- **BND → MEM.encoding_state** [0:10]: Temporal binding maps to encoding state — binding success in hippocampal theta-gamma coupling.
- **MEM.familiarity_proxy** [10:20] + **MEM.retrieval_dynamics** [20:30]: New in v2.0.0 — familiarity and retrieval support encoding quality assessment and long-term consolidation tracking.

---

**Model Status**: **REQUIRES VALIDATION**
**Output Dimensions**: **10D**
**Manifold Range**: **IMU OII [306:316]**
**Evidence Tier**: **beta (Integrative) — 70-90% confidence**
**Version**: **2.1.0** (2026-02-13)
**Papers**: **12** (5 original + 3 review/computational + 4 supporting)
**Doc-code mismatches**: 7 (MECHANISM_NAMES, LAYERS, h3_demand, brain_regions, dimension_names, citations, paper_count)
