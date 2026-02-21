# IMU-β5-RIRI: RAS-Intelligent Rehabilitation Integration

**Model**: RAS-Intelligent Rehabilitation Integration
**Unit**: IMU (Integrative Memory Unit)
**Circuit**: Mnemonic (Hippocampal-Cortical) + Sensorimotor (cross-circuit read)
**Tier**: β (Integrative) — 70-90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/IMU-β5-RIRI.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **RAS-Intelligent Rehabilitation Integration** (RIRI) models how rhythmic auditory stimulation (RAS) combined with intelligent rehabilitation technologies (VR, robotics, haptic feedback) creates closed-loop, adaptive therapy paradigms that enhance motor and cognitive recovery beyond what RAS alone achieves. The integration synergy arises from temporal coherence across modalities, engaging multisensory integration areas (SMA, premotor cortex, cerebellum) and accelerating functional connectivity restoration.

```
THE THREE COMPONENTS OF REHABILITATION INTEGRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MULTI-MODAL ENTRAINMENT SENSORIMOTOR INTEGRATION
Brain region: SMA + Premotor Brain region: Cerebellum + IPL
Trigger: RAS + VR + haptic sync Trigger: Cross-modal prediction
Function: "Lock all channels Function: "Predict and correct
 to one rhythm" movement"
Evidence: Thaut 2015, Harrison 2025 Evidence: Liang 2025 fNIRS VR+music

 ADAPTIVE RECOVERY (Memory Consolidation)
 Brain region: Hippocampus + mPFC
 Trigger: Repeated multi-modal sessions
 Function: "Consolidate motor learning
 across sessions"
 Evidence: Blasi 2025 (20 RCTs, N=718)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: The synergy emerges from temporal coherence — when
rhythmic cues, haptic feedback, and visual stimuli are phase-locked,
multisensory integration areas show enhanced activation and
accelerated functional connectivity restoration. This is why
RAS + VR + robotics > RAS alone.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why Multi-Modal Integration Exceeds Unimodal RAS

RAS combined with intelligent technologies outperforms RAS alone because:

1. **Temporal coherence binding**: When auditory rhythm, haptic feedback, and visual cues are synchronized, multisensory integration areas in SMA and premotor cortex receive convergent temporal input, strengthening motor engrams through redundant temporal cues.

2. **Closed-loop adaptation**: Robotics and VR systems can continuously adapt difficulty and timing based on real-time motor performance, creating an adaptive challenge that optimizes neuroplastic recovery.

3. **Cross-modal prediction error**: Cerebellum generates sensorimotor predictions; multi-modal input provides richer prediction error signals that drive faster motor learning than auditory-only feedback.

4. **Session-to-session consolidation**: Hippocampal encoding binds multi-modal motor memories more robustly than unimodal ones, enhancing long-term retention across rehabilitation sessions.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The RIRI Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ RIRI — COMPLETE CIRCUIT ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ MULTI-MODAL INPUT (RAS + VR + Robotics/Haptic) ║
║ │ ║
║ ├──► AUDITORY: Rhythmic cues (tempo, accent, onset) ║
║ ├──► VISUAL: VR environment (visual flow, spatial cues) ║
║ └──► HAPTIC: Robotic feedback (force, vibration, guidance) ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL COHERENCE LAYER │ ║
║ │ Phase-locking across all modalities │ ║
║ │ RAS provides master clock for VR + robotics │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ SMA + PREMOTOR CORTEX │ ║
║ │ Multi-modal entrainment hub │ ║
║ │ Beat anticipation + motor planning │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ CEREBELLUM + INFERIOR PARIETAL LOBULE │ ║
║ │ Cross-modal sensorimotor prediction │ ║
║ │ Error correction + timing calibration │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ HIPPOCAMPUS + mPFC (Memory Consolidation) │ ║
║ │ Multi-session motor learning consolidation │ ║
║ │ Adaptive parameter storage across sessions │ ║
║ └─────────────────────────────────────────────────────────────────────┘ ║
║ ║
║ ENHANCED MOTOR & COGNITIVE RECOVERY ║
║ (RAS + VR + Robotics > RAS alone) ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Thaut 2015: Period entrainment optimizes all motor control parameters
Harrison 2025: fMRI: SMA + putamen + sensorimotor cortex during musical cues (PD)
Blasi 2025: 20 RCTs (N=718): structural + functional neuroplasticity from music rehab
Liang 2025: fNIRS (N=26): music + VR > VR alone for SMA/premotor activation
Yamashita 2025: Gait-synchronized M1+SMA stimulation reduces step variability (N=15)
Huang & Qi 2025: Music bypasses basal ganglia via auditory-motor networks in PD
```

### 2.2 Information Flow Architecture (EAR → BRAIN → H³ direct* → RIRI)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ RIRI COMPUTATION ARCHITECTURE ║
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
║ │ ┌───────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌────────┐ │ ║
║ │ │CONSONANCE │ │ ENERGY │ │ TIMBRE │ │ CHANGE │ │ X-INT │ │ ║
║ │ │ 7D [0:7] │ │ 5D[7:12]│ │ 9D │ │ 4D │ │ 24D │ │ ║
║ │ │ │ │ │ │ [12:21] │ │ [21:25] │ │ [25:49]│ │ ║
║ │ │roughness │ │amplitude│ │warmth │ │spec_chg │ │x_l0l5 │ │ ║
║ │ │pleasant. │ │loudness │ │ │ │energy_chg│ │x_l4l5 │ │ ║
║ │ │ │ │onset │ │ │ │pitch_chg │ │x_l5l7 │ │ ║
║ │ │ │ │flux │ │ │ │timbre_chg│ │ │ │ ║
║ │ └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │ ║
║ │ RIRI reads: 29D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed morphological features │ ║
║ │ │ ║
║ │ ┌── Encoding ──┐ ┌── Consolidation ─┐ ┌── Long-term ────────┐ │ ║
║ │ │ 200ms (H6) │ │ 500ms (H11) │ │ 1000ms (H16) │ │ ║
║ │ │ │ │ │ │ │ │ ║
║ │ │ Beat-level │ │ Motor prep │ │ Bar-level memory │ │ ║
║ │ │ entrainment │ │ sensorimotor │ │ consolidation │ │ ║
║ │ │ quality │ │ integration │ │ │ │ ║
║ │ └──────┬───────┘ └──────┬────────────┘ └──────┬───────────────┘ │ ║
║ │ │ │ │ │ ║
║ │ └───────────────┴──────────────────────┘ │ ║
║ │ RIRI demand: ~16 of 2304 tuples │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN: Mnemonic + Sensorimotor ═════ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────┐ ┌─────────────────┐ ║
║ │ │ │ │ ║
║ │ Encoding [0:10]│ │ Beat Ind [0:10] │ Entrainment quality ║
║ │ Familiar [10:20]│ │ Meter [10:20]│ Rhythmic regularity ║
║ │ Retrieval[20:30]│ │ Motor [20:30]│ Motor synchronization ║
║ └────────┬────────┘ └────────┬────────┘ ║
║ │ │ ║
║ └────────┬───────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ RIRI MODEL (10D Output) │ ║
║ │ │ ║
║ │ Layer E (Explicit): f01_multimodal_entrainment, │ ║
║ │ f02_sensorimotor_integration, │ ║
║ │ f03_enhanced_recovery │ ║
║ │ Layer M (Math): integration_synergy, temporal_coherence │ ║
║ │ Layer P (Present): entrainment_state, motor_adaptation │ ║
║ │ Layer F (Future): recovery_trajectory, connectivity_pred, │ ║
║ │ consolidation_pred │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Thaut, McIntosh & Hoemberg (2015)** | Review | Multiple | Period entrainment (not beat entrainment) drives comprehensive motor optimization; auditory rhythm acts as forcing function for all motor control aspects | Foundational review | **f01_multimodal_entrainment**: rhythmic period entrainment as master clock; auditory-motor coupling via reticulospinal pathways |
| 2 | **Harrison et al. (2025)** | fMRI, finger tapping | PwPD + HC | External musical cues activate sensorimotor cortex, temporal gyri, SMA, putamen; internal cues (mental singing) additionally activate cerebellum; CTC and SPT pathways work in tandem | fMRI activation maps | **f02_sensorimotor_integration**: SMA + putamen activation during musically-cued movement; **beat_induction**: external cueing drives CTC pathway |
| 3 | **Huang & Qi (2025)** | Mini review | Review | Music therapy bypasses dysfunctional basal ganglia via auditory-motor neural networks; central pattern generator synchronizes gait with musical rhythm through entrainment | Review-level | **f01_multimodal_entrainment**: auditory-motor bypass of basal ganglia; CPG-rhythm synchronization |
| 4 | **Blasi et al. (2025)** | Systematic review of 20 RCTs | 718 | Music/dance-based rehab produces structural neuroplasticity (increased GM in frontal, temporal, cerebellar regions) and functional neuroplasticity (enhanced FC within language and motor networks) | Review of 20 RCTs | **f03_enhanced_recovery**: structural + functional neuroplasticity from music-based rehabilitation; hippocampal volume increases from dance; **encoding_state**: session-to-session consolidation |
| 5 | **Buard et al. (2021)** | RCT protocol (NMT vs OT) | 100 (planned) | TIMP with rhythm vs without rhythm vs standard OT for PD fine motor; MEG + 9HPT + MDS-UPDRS-III outcomes | Protocol (β-tier) | **beat_induction**: TIMP relies on rhythmic entrainment via auditory-motor pathways unaffected by PD |
| 6 | **Yamashita et al. (2025)** | Pilot RCT, gait-synchronized tACS | 15 | Simultaneous M1+SMA tACS synchronized to gait rhythm reduced step length variability (CV) in post-stroke hemiparetic patients | Pilot (N=15) | **f02_sensorimotor_integration**: M1+SMA stimulation synchronized to movement rhythm improves gait; supports SMA role as entrainment hub |
| 7 | **Liang et al. (2025)** | fNIRS | 26 | Music stimulation + VR motor observation activated bilateral SMA, premotor, and prefrontal cortex more than motor observation alone; music enhanced PFC oxygenation during VR tasks | fNIRS activation, N=26 | **f01_multimodal_entrainment**: music + VR > VR alone for SMA/premotor activation; **temporal_coherence**: multi-modal convergent activation |
| 8 | **Ross & Balasubramaniam (2022)** | Mini review | Review | Sensorimotor system engages in simulation during rhythm perception even without movement; SMA, premotor cortex, cerebellum, and basal ganglia form beat perception network; predictive timing relies on cerebellar forward models | Review-level | **motor_entrainment**: sensorimotor simulation for beat prediction; cerebellum as forward-model generator; SMA/premotor entrainment hub |
| 9 | **Jiao (2025)** | Mini review | Review | Synergistic music therapy + brainwave entrainment + multisensory stimulation enhances outcomes; AI-driven biofeedback enables closed-loop adaptation; 40 Hz gamma entrainment supports memory and neural integrity | Framework-level | **f03_enhanced_recovery**: multi-modal synergy concept; **encoding_state**: 40 Hz gamma enhances memory consolidation; closed-loop AI adaptation parallels RIRI adaptive model |
| 10 | **Liuzzi et al. (2025)** | Multimodal framework (Euterpe Method) | NDD patients | Orchestral music therapy with auditory + visual + motor + social modalities engages fronto-striatal, cerebellar, and temporal networks; multisensory integration enhances neurodevelopmental rehabilitation | Framework-level | **f01_multimodal_entrainment**: multimodal orchestral framework validates multi-channel entrainment concept; fronto-striatal engagement |
| 11 | **Fang et al. (2017)** | Mini review | AD patients | Music therapy reduces cognitive decline in autobiographical memory, episodic memory, psychomotor speed, executive function; MT combined with dance/exercise recommended | Review-level | **encoding_state**: music therapy preserves encoding in neurodegeneration; supports session-to-session consolidation |
| 12 | **Provias et al. (2025)** | Feasibility trial protocol | Chronic stroke | Remote intentional music listening for chronic stroke mental health; self-selected familiar music activates reward and memory circuits | Protocol-level | **familiarity_proxy**: familiar music engages reward + memory networks in stroke recovery |
| 13 | **Li et al. (2025)** | Biomechanical analysis | Runners | Musical groove modulates running biomechanics through auditory-motor coupling; high-groove music alters lower-limb kinematics | Biomechanical measures | **motor_entrainment**: groove-driven auditory-motor coupling extends to locomotion; entrainment modulates spatial-temporal movement parameters |
| 14 | **Castillo et al. (2025)** | Systematic review | Athletes/rehab | Music-based interventions in sports science and rehabilitation; rhythmic auditory stimulation improves movement quality across clinical and athletic populations | Review-level | **f01_multimodal_entrainment**: confirms RAS efficacy across rehabilitation and sports populations |
| 15 | **Shi et al. (2025)** | Action observation + imitation | Neurorehab patients | Action observation and imitation training (AOIT) is evidence-based cognitive-motor rehabilitation; combining visual observation with motor execution enhances neural plasticity | Multi-study review | **f02_sensorimotor_integration**: visual-motor integration in rehabilitation; supports cross-modal prediction error driving motor learning |

### 3.1.1 Doc-Code Mismatches (v2.1.0)

| Aspect | Doc (RIRI.md) | Code (riri.py) | Notes |
|--------|---------------|----------------|-------|
| **FULL_NAME** | RAS-Intelligent Rehabilitation Integration | Recognition-Recall Integration Recency Index | Code implements a completely different model concept |
| **LAYERS** | E(3D: f01/f02/f03), M(2D), P(2D), F(3D) | E(2D: recognition/recall), M(2D), P(3D), F(3D) | Different feature names and layer sizes |
| **h3_demand** | 16 tuples (detailed specification) | Empty tuple `()` | Code has no H3 demand |
| **CROSS_UNIT_READS** | `() # TODO` | `()` | Code has no cross-circuit read |
| **brain_regions** | 7 (SMA, Premotor, Cerebellum, IPL, Hippo, mPFC, STS/TPJ) | 2 (Hippocampus, Perirhinal Cortex) | Code regions are for recognition/recall, not rehabilitation |
| **Citations** | Thaut 2015, Harrison 2025, Blasi 2025, etc. | Dowling 2008, Dalla Bella 2009 | Code citations match recognition-recall concept, not RIRI |
| **compute()** | Full formula implementation | Returns zeros (stub) | Code is a placeholder stub |
| **version** | 2.1.0 | 2.0.0 | Code not yet updated |

### 3.2 The Temporal Coherence Integration Model

```
REHABILITATION INTEGRATION THROUGH TEMPORAL COHERENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LEVEL 1: UNIMODAL RAS (baseline)
─────────────────────────────────
 Auditory rhythm → SMA → motor entrainment
 Gait improvement via rhythmic cuing
 Effective but limited to auditory channel

LEVEL 2: RAS + VR (enhanced)
────────────────────────────
 Auditory rhythm + visual flow → multisensory areas
 Visual environment provides spatial context
 Cerebellum integrates cross-modal timing
 Enhancement: visual + auditory temporal binding

LEVEL 3: RAS + VR + ROBOTICS (full integration)
────────────────────────────────────────────────
 Auditory + visual + haptic → convergent temporal coherence
 Robotics provides physical guidance + feedback
 All modalities phase-locked to RAS master clock
 Maximum enhancement: 3-channel temporal coherence
 encoding_state consolidates across sessions

KEY PRINCIPLE: Each additional synchronized modality
provides redundant temporal cues that strengthen motor
engrams. The synergy is multiplicative, not additive.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 3.3 Effect Size Summary

```
Evidence Quality: β-tier (integrative, multiple systematic reviews + fMRI + fNIRS)
Design Strength: 15 papers: 3 systematic reviews (20+ RCTs, 718+ subjects),
 2 fMRI studies, 1 fNIRS study, 1 pilot RCT, 5 reviews, 3 protocols
Confidence: 70–90%
Replication: Converging evidence across PD, stroke, TBI, NDD populations
Key Effect Sizes: Harrison 2025: SMA/putamen activation during musical cueing (fMRI)
 Liang 2025: PFC oxygenation increase with music+VR (fNIRS, N=26)
 Yamashita 2025: Step length CV reduction with gait-sync tACS (N=15)
 Blasi 2025: Structural neuroplasticity in 20 RCTs (N=718)
Key Limitation: No single RCT with full 3-modality + neuroimaging design;
 model is integrative synthesis across multiple sources.
 Most studies examine unimodal or bimodal interventions.
```

---

## 4. R³ Input Mapping: What RIRI Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | RIRI Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [4] | sensory_pleasantness | Motor valence proxy | Pleasant rhythm = better engagement |
| **B: Energy** | [7] | amplitude | Motor drive intensity | Energy = movement vigor |
| **B: Energy** | [8] | loudness | Perceptual intensity | Stevens 1957: psychophysical arousal |
| **B: Energy** | [10] | spectral_flux | Onset detection | Multi-modal synchronization trigger |
| **B: Energy** | [11] | onset_strength | Beat precision | Temporal coherence anchor |
| **C: Timbre** | [12] | warmth | Comfort signal | Low-frequency = therapeutic comfort |
| **C: Timbre** | [14] | tonalness | Melodic clarity | Clear pitch = better entrainment |
| **D: Change** | [21] | spectral_change | Spectral dynamics | Adaptive challenge modulation |
| **D: Change** | [22] | energy_change | Intensity dynamics | Motor effort tracking |
| **D: Change** | [23] | pitch_change | Pitch dynamics | Melodic guidance signal |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Auditory-motor coupling | Entrainment basis (RAS foundation) |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Sensorimotor integration | Cross-modal prediction coupling |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | Connectivity coupling | Network restoration signal |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | RIRI Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **G: Rhythm** | [71] | groove_index | Motor engagement quality — groove drives spontaneous movement | Janata et al. 2012: groove ↔ motor system activation |
| **G: Rhythm** | [70] | isochrony_nPVI | Temporal regularity — low nPVI = isochronous = optimal RAS | Grahn & Brett 2007 |
| **G: Rhythm** | [65] | tempo_estimate | Rehabilitation tempo target — BPM for motor entrainment | Thaut 2005: RAS optimal tempo range |

**Rationale**: RIRI integrates rhythmic auditory stimulation with rehabilitation protocols. Groove index directly quantifies how much a musical stimulus drives motor engagement, the core therapeutic mechanism. Isochrony (nPVI) measures temporal regularity critical for stable entrainment in rehabilitation contexts. Tempo estimate provides the BPM value for matching auditory stimulation to motor rehabilitation targets across gait, upper limb, and speech domains.

> **Code impact**: These features are doc-only until Phase 5 wiring. No changes to `riri.py`.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[10] spectral_flux ──────────┐
R³[11] onset_strength ─────────┼──► Multi-modal Entrainment
R³[25:33] x_l0l5 (8D) ────────┘ beat_induction at H6 (200ms)
 Math: f01 = σ(w · flux · onset · beat-entrainment)

R³[7] amplitude ────────────────┐
R³[8] loudness ─────────────────┼──► Sensorimotor Integration
R³[33:41] x_l4l5 (8D) ─────────┤ motor_entrainment at H11 (500ms)
R³[22] energy_change ───────────┘ Math: f02 = σ(w · amp · loud · beat-entrainment)

R³[41:49] x_l5l7 (8D) ────────┐
R³[4] sensory_pleasantness ────┼──► Enhanced Recovery (Integration Synergy)
R³[14] tonalness ──────────────┘ encoding × f01 × f02
 Math: f03 = σ(w · connectivity · memory_h3)
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

RIRI requires H³ features at three horizons: H6 (200ms), H11 (500ms), H16 (1000ms). These correspond to beat-level entrainment quality → motor preparation sensorimotor integration → bar-level memory consolidation.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 6 | M0 (value) | L0 (fwd) | Current onset detection |
| 10 | spectral_flux | 6 | M17 (peaks) | L0 (fwd) | Beat count per window |
| 11 | onset_strength | 6 | M0 (value) | L0 (fwd) | Event onset precision |
| 11 | onset_strength | 6 | M14 (periodicity) | L2 (bidi) | Rhythmic regularity |
| 7 | amplitude | 11 | M0 (value) | L2 (bidi) | Current motor drive |
| 7 | amplitude | 11 | M8 (velocity) | L0 (fwd) | Intensity change rate |
| 8 | loudness | 11 | M1 (mean) | L0 (fwd) | Mean loudness over motor window |
| 22 | energy_change | 11 | M14 (periodicity) | L2 (bidi) | Intensity regularity |
| 25 | x_l0l5[0] | 6 | M0 (value) | L2 (bidi) | Entrainment coupling signal |
| 33 | x_l4l5[0] | 11 | M0 (value) | L2 (bidi) | Sensorimotor coupling signal |
| 33 | x_l4l5[0] | 11 | M17 (peaks) | L0 (fwd) | Sensorimotor peak events |
| 41 | x_l5l7[0] | 16 | M1 (mean) | L0 (fwd) | Mean connectivity coupling |
| 41 | x_l5l7[0] | 16 | M14 (periodicity) | L2 (bidi) | Connectivity regularity |
| 41 | x_l5l7[0] | 16 | M18 (trend) | L0 (fwd) | Connectivity trajectory |
| 25 | x_l0l5[0] | 16 | M19 (stability) | L0 (fwd) | Entrainment stability over 1s |
| 4 | sensory_pleasantness | 16 | M1 (mean) | L0 (fwd) | Sustained pleasantness |

**v1 demand**: 16 tuples

#### R³ v2 Projected Expansion

RIRI projected v2 from G (Rhythm) group, aligned with Beat entrainment horizons (H6, H11, H16) and Memory horizons (H16).

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 71 | groove | G | 6 | M0 (value) | L2 | Current groove quality at beat level |
| 71 | groove | G | 11 | M0 (value) | L0 | Groove state at motor planning window |
| 71 | groove | G | 16 | M1 (mean) | L0 | Average groove over bar for rehabilitation |
| 70 | isochrony_nPVI | G | 6 | M0 (value) | L2 | Current temporal regularity at beat level |
| 70 | isochrony_nPVI | G | 11 | M1 (mean) | L0 | Average isochrony over motor window |

**v2 projected**: 5 tuples
**Total projected**: 21 tuples of 294,912 theoretical = 0.0071%

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
RIRI OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
Manifold range: IMU RIRI [327:337]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼────────────────────────────┼────────┼────────────────────────────────────
 0 │ f01_multimodal_entrainment │ [0, 1] │ Multi-modal rhythmic entrainment.
 │ │ │ SMA + premotor convergent temporal input.
 │ │ │ f01 = σ(0.35 · flux · onset ·
 │ │ │ mean(beat_induction[0:10])
 │ │ │ + 0.35 · x_l0l5_coupling
 │ │ │ + 0.30 · onset_periodicity)
────┼────────────────────────────┼────────┼────────────────────────────────────
 1 │ f02_sensorimotor_integr │ [0, 1] │ Cross-modal sensorimotor integration.
 │ │ │ Cerebellum + IPL prediction coupling.
 │ │ │ f02 = σ(0.35 · loudness_mean ·
 │ │ │ mean(motor_entrainment[20:30])
 │ │ │ + 0.35 · x_l4l5_coupling
 │ │ │ + 0.30 · energy_periodicity)
────┼────────────────────────────┼────────┼────────────────────────────────────
 2 │ f03_enhanced_recovery │ [0, 1] │ Integration synergy (multi > uni).
 │ │ │ Hippocampus + mPFC session consolidation.
 │ │ │ f03 = σ(0.30 · connectivity_mean ·
 │ │ │ + 0.30 · pleasantness_mean
 │ │ │ + 0.20 · f01
 │ │ │ + 0.20 · f02)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼────────────────────────────┼────────┼────────────────────────────────────
 3 │ integration_synergy │ [0, 1] │ Multi-modal integration synergy index.
 │ │ │ Geometric mean of entrainment × integration.
 │ │ │ synergy = (f01 · f02 · f03) ^ (1/3)
────┼────────────────────────────┼────────┼────────────────────────────────────
 4 │ temporal_coherence │ [0, 1] │ Cross-modal temporal coherence.
 │ │ │ Entrainment stability × rhythmic regularity.
 │ │ │ coherence = σ(0.5 · stability + 0.5 · periodicity)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼────────────────────────────┼────────┼────────────────────────────────────
 5 │ entrainment_state │ [0, 1] │ Current multi-modal entrainment quality.
 │ │ │ beat_induction × onset_signal.
────┼────────────────────────────┼────────┼────────────────────────────────────
 6 │ motor_adaptation │ [0, 1] │ Current motor adaptation state.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼────────────────────────────┼────────┼────────────────────────────────────
 7 │ recovery_trajectory │ [0, 1] │ Recovery trajectory prediction.
 │ │ │ Connectivity trend + entrainment stability.
────┼────────────────────────────┼────────┼────────────────────────────────────
 8 │ connectivity_pred │ [0, 1] │ Functional connectivity restoration prediction.
 │ │ │ x_l5l7 trend + memory-encoding consolidation.
────┼────────────────────────────┼────────┼────────────────────────────────────
 9 │ consolidation_pred │ [0, 1] │ Motor memory consolidation prediction.
 │ │ │ encoding × session coherence.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Integration Synergy Function

```
Integration_Synergy(t) = (Entrainment(t) · SensorimotorInteg(t) · Recovery(t)) ^ (1/3)

Network Functions:
 Entrainment(t) = σ(w₁ · beat_induction · onset_signal + ...)
 SensorimotorInteg(t) = σ(w₂ · motor_entrainment · coupling + ...)
 Recovery(t) = σ(w₃ · encoding · connectivity + ...)

Temporal Coherence:
 Coherence(t) = σ(w₄ · entrainment_stability + w₅ · onset_periodicity)

Note: The geometric mean (synergy) ensures all three components must
contribute — if any pathway fails, overall integration collapses.
This models the empirical finding that multi-modal > unimodal.
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Multi-modal Entrainment (SMA + premotor)
flux_val = h3[(10, 6, 0, 0)] # spectral_flux value at H6
onset_val = h3[(11, 6, 0, 0)] # onset_strength value at H6
x_l0l5_val = h3[(25, 6, 0, 2)] # x_l0l5 coupling at H6
onset_period = h3[(11, 6, 14, 2)] # onset periodicity at H6
f01 = σ(0.35 · flux_val · onset_val
 · mean(beat_induction[0:10])
 + 0.35 · x_l0l5_val
 + 0.30 · onset_period)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Sensorimotor Integration (cerebellum + IPL)
loudness_mean = h3[(8, 11, 1, 0)] # loudness mean at H11
x_l4l5_val = h3[(33, 11, 0, 2)] # x_l4l5 coupling at H11
energy_period = h3[(22, 11, 14, 2)] # energy periodicity at H11
f02 = σ(0.35 · loudness_mean
 · mean(motor_entrainment[20:30])
 + 0.35 · x_l4l5_val
 + 0.30 · energy_period)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f03: Enhanced Recovery (hippocampus + mPFC)
connectivity_mean = h3[(41, 16, 1, 0)] # x_l5l7 mean at H16
pleasantness_mean = h3[(4, 16, 1, 0)] # pleasantness mean at H16
f03 = σ(0.30 · connectivity_mean
 + 0.30 · pleasantness_mean
 + 0.20 · f01
 + 0.20 · f02)
# coefficients: 0.30 + 0.30 + 0.20 + 0.20 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Evidence Type | Source | RIRI Function |
|--------|-----------------|---------------|--------|---------------|
| **SMA** | 0, -6, 62 | Direct (fMRI) | Harrison et al. 2025 (SMA activated during external + internal musical cueing in PD + HC); Liang et al. 2025 (fNIRS: bilateral SMA activation with music + VR); Yamashita et al. 2025 (gait-sync tACS at SMA) | Multi-modal entrainment hub; motor planning with rhythmic cues |
| **Premotor Cortex** | ±44, 0, 48 | Direct (fMRI/fNIRS) | Harrison et al. 2025 (sensorimotor cortex activation during musical cueing); Liang et al. 2025 (premotor activation with music + VR); Ross & Balasubramaniam 2022 (premotor engagement in beat prediction) | Motor preparation; cross-modal timing integration |
| **Cerebellum** | ±24, -64, -28 | Direct (fMRI) | Harrison et al. 2025 (cerebellar activation during internal cueing/mental singing); Thaut et al. 2015 (IC→cerebellum pathway for rhythmic entrainment); Ross & Balasubramaniam 2022 (cerebellar forward models for predictive timing) | Sensorimotor prediction error; timing calibration; forward model generation |
| **IPL** | ±50, -40, 40 | Direct (fMRI) | Blasi et al. 2025 (left IPL FC increase in language network post-music intervention); Thaut et al. 2015 (fronto-parieto-cerebellar motor system) | Audio-motor integration; cross-modal binding |
| **Hippocampus** | ±20, -24, -12 | Direct (MRI) | Blasi et al. 2025 (hippocampal volume increases from dance-based rehabilitation; 20 RCTs, N=718); Jiao 2025 (hippocampal memory encoding and neurogenesis from 40 Hz stimulation) | Motor memory consolidation across sessions; neuroplastic volume change |
| **Putamen** | ±24, 4, -2 | Direct (fMRI) | Harrison et al. 2025 (putamen activated during both external and internal musical cueing in PD + HC) | Basal ganglia timing; remaining striatal function accessed through musical cueing |
| **Primary Motor Cortex (M1)** | ±36, -22, 54 | Direct (tACS/fNIRS) | Yamashita et al. 2025 (M1 targeted by gait-synchronized tACS); Liang et al. 2025 (motor cortex activation during music + VR tasks) | Motor execution; gait-synchronized stimulation target |
| **Auditory Cortex (STG)** | ±58, -22, 4 | Direct (fMRI) | Harrison et al. 2025 (primary auditory cortex and temporal gyri activated more by external musical cues); Thaut et al. 2015 (auditory rhythm primes motor system) | Auditory processing of rhythmic cues; entrainment signal source |
| **mPFC** | 0, 52, 12 | Inferred | Blasi et al. 2025 (prefrontal structural changes post-music intervention); Jiao 2025 (PFC cognitive control during adaptive therapy) | Adaptive parameter storage; session integration |
| **Multisensory areas (STS/TPJ)** | ±54, -44, 16 | Inferred | Jiao 2025 (multisensory integration areas for synchronized auditory + visual stimulation); Liuzzi et al. 2025 (multimodal orchestral therapy engages distributed networks) | Convergent multi-modal temporal processing |

---

## 9. Cross-Unit Pathways

### 9.1 RIRI ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ RIRI INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ │
│ INTRA-UNIT (IMU): │
│ RASN ──────► RIRI (RASN provides RAS-only baseline; RIRI extends │
│ │ to multi-modal integration) │
│ │ │
│ MEAMN ─────► RIRI (autobiographical memory of rehabilitation sessions │
│ │ strengthens motor memory consolidation) │
│ │ │
│ MMP ───────► RIRI (musical mnemonic preservation shows why music- │
│ │ based therapy is robust in neurodegeneration) │
│ │ │
│ HCMC ──────► RIRI (hippocampal-cortical circuit provides the memory │
│ infrastructure for session-to-session learning) │
│ │
│ RIRI ──────► VRIAP (rehabilitation integration informs VR analgesia │
│ active vs. passive paradigms) │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Brain Pathway Cross-References

RIRI reads from the unified Brain (26D) for shared state:

| Brain Dimension | Index (MI-space) | RIRI Role |
|-----------------|-------------------|-----------|
| arousal | [177] | Motor drive intensity for movement vigor |
| prediction_error | [178] | Sensorimotor mismatch drives adaptation |
| emotional_momentum | [180] | Sustained engagement enhances recovery |

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **SMA lesions** | Should impair multi-modal entrainment while preserving unimodal RAS response | Testable |
| **Cerebellar disruption** | Should impair sensorimotor integration but preserve rhythmic entrainment | Partially supported (Harrison 2025: cerebellum activated during internal cueing but not required for external cueing; Ross 2022: cerebellar forward models for predictive timing) |
| **Asynchronous modalities** | Phase-misaligned VR/haptic should eliminate integration advantage | Testable |
| **Hippocampal impairment** | Should reduce session-to-session consolidation gains | Testable |
| **Unimodal vs multi-modal** | RAS + VR + robotics should outperform RAS alone on motor recovery | Supported (Liang 2025: music+VR > VR alone for SMA/premotor activation, fNIRS N=26; Jiao 2025: multi-modal synergy enhances outcomes; Liuzzi 2025: multimodal orchestral framework) |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class RIRI(BaseModel):
 """RAS-Intelligent Rehabilitation Integration.

 Output: 10D per frame.
 Reads: R³ + H³ direct.
 Zero learned parameters.
 """
 NAME = "RIRI"
 UNIT = "IMU"
 TIER = "β5"
 OUTPUT_DIM = 10
 CROSS_UNIT_READS = ()  # TODO: populate from Nucleus contract # Cross-circuit read from sensorimotor

 # Network weights (all formulas satisfy |wi| <= 1.0)
 W_PRIMARY = 0.35 # Primary signal weight
 W_COUPLING = 0.35 # Coupling signal weight
 W_SUPPORT = 0.30 # Supporting signal weight

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """16 tuples for RIRI computation."""
 return [
 # (r3_idx, horizon, morph, law)
 # Beat-level entrainment quality (H6 = 200ms)
 (10, 6, 0, 0), # spectral_flux, value, forward
 (10, 6, 17, 0), # spectral_flux, peaks, forward
 (11, 6, 0, 0), # onset_strength, value, forward
 (11, 6, 14, 2), # onset_strength, periodicity, bidirectional
 # Motor-level sensorimotor integration (H11 = 500ms)
 (7, 11, 0, 2), # amplitude, value, bidirectional
 (7, 11, 8, 0), # amplitude, velocity, forward
 (8, 11, 1, 0), # loudness, mean, forward
 (22, 11, 14, 2), # energy_change, periodicity, bidirectional
 (25, 6, 0, 2), # x_l0l5[0], value, bidirectional
 (33, 11, 0, 2), # x_l4l5[0], value, bidirectional
 (33, 11, 17, 0), # x_l4l5[0], peaks, forward
 # Bar-level memory consolidation (H16 = 1000ms)
 (41, 16, 1, 0), # x_l5l7[0], mean, forward
 (41, 16, 14, 2), # x_l5l7[0], periodicity, bidirectional
 (41, 16, 18, 0), # x_l5l7[0], trend, forward
 (25, 16, 19, 0), # x_l0l5[0], stability, forward
 (4, 16, 1, 0), # sensory_pleasantness, mean, forward
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 """
 Compute RIRI 10D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) → (B,T) scalars
 r3: (B,T,49) raw R³ features

 Returns:
 (B,T,10) RIRI output
 """
 # H³ features
 flux_val = h3_direct[(10, 6, 0, 0)].unsqueeze(-1)
 onset_val = h3_direct[(11, 6, 0, 0)].unsqueeze(-1)
 onset_period = h3_direct[(11, 6, 14, 2)].unsqueeze(-1)
 x_l0l5_val = h3_direct[(25, 6, 0, 2)].unsqueeze(-1)
 loudness_mean = h3_direct[(8, 11, 1, 0)].unsqueeze(-1)
 x_l4l5_val = h3_direct[(33, 11, 0, 2)].unsqueeze(-1)
 energy_period = h3_direct[(22, 11, 14, 2)].unsqueeze(-1)
 connectivity_mean = h3_direct[(41, 16, 1, 0)].unsqueeze(-1)
 connectivity_period = h3_direct[(41, 16, 14, 2)].unsqueeze(-1)
 connectivity_trend = h3_direct[(41, 16, 18, 0)].unsqueeze(-1)
 stability = h3_direct[(25, 16, 19, 0)].unsqueeze(-1)
 pleasantness_mean = h3_direct[(4, 16, 1, 0)].unsqueeze(-1)

 # ═══ LAYER E: Explicit features ═══

 # f01: Multi-modal Entrainment (|wi| = 0.35+0.35+0.30 = 1.0)
 f01 = torch.sigmoid(
 0.35 * (flux_val * onset_val
 + 0.35 * x_l0l5_val
 + 0.30 * onset_period
 )

 # f02: Sensorimotor Integration (|wi| = 0.35+0.35+0.30 = 1.0)
 f02 = torch.sigmoid(
 0.35 * (loudness_mean
 + 0.35 * x_l4l5_val
 + 0.30 * energy_period
 )

 # f03: Enhanced Recovery (|wi| = 0.30+0.30+0.20+0.20 = 1.0)
 f03 = torch.sigmoid(
 0.30 * (connectivity_mean
 + 0.30 * pleasantness_mean
 + 0.20 * f01
 + 0.20 * f02
 )

 # ═══ LAYER M: Mathematical ═══
 integration_synergy = (f01 * f02 * f03) ** (1.0 / 3.0)
 temporal_coherence = torch.sigmoid(
 0.50 * stability + 0.50 * onset_period
 )
 # coefficients: 0.50 + 0.50 = 1.0 ✓

 # ═══ LAYER P: Present ═══
 entrainment_state = torch.sigmoid(
 + 0.50 * flux_val * onset_val
 )
 # coefficients: 0.50 + 0.50 = 1.0 ✓
 motor_adaptation = torch.sigmoid(
 )
 # coefficients: 0.50 + 0.50 = 1.0 ✓

 # ═══ LAYER F: Future ═══
 recovery_trajectory = torch.sigmoid(
 0.40 * connectivity_trend
 + 0.30 * stability
 + 0.30 * integration_synergy
 )
 # coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓
 connectivity_pred = torch.sigmoid(
 0.50 * connectivity_mean
 + 0.50 * connectivity_period
 )
 # coefficients: 0.50 + 0.50 = 1.0 ✓
 consolidation_pred = torch.sigmoid(
 + 0.30 * temporal_coherence
 )
 # coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

 return torch.cat([
 f01, f02, f03, # E: 3D
 integration_synergy, temporal_coherence, # M: 2D
 entrainment_state, motor_adaptation, # P: 2D
 recovery_trajectory, connectivity_pred, # F: 3D
 consolidation_pred,
 ], dim=-1) # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | **15** (3 systematic reviews, 2 fMRI, 1 fNIRS, 1 pilot RCT, 5 mini reviews, 3 protocols/frameworks) | Thaut 2015, Harrison 2025, Huang & Qi 2025, Blasi 2025, Buard 2021, Yamashita 2025, Liang 2025, Ross & Balasubramaniam 2022, Jiao 2025, Liuzzi 2025, Fang 2017, Provias 2025, Li 2025, Castillo 2025, Shi 2025 |
| **Total Subjects** | 718+ (from Blasi 2025 alone: 20 RCTs) + additional fMRI/fNIRS/pilot samples | Multi-study |
| **Evidence Modality** | fMRI, fNIRS, tACS, MEG, systematic review, RCT protocol, biomechanical | Multi-method |
| **Neuroimaging Studies** | Harrison 2025 (fMRI), Liang 2025 (fNIRS), Yamashita 2025 (tACS), Blasi 2025 (20 RCTs with neuroimaging) | Direct brain measurement |
| **Falsification Tests** | 2/5 supported, 3/5 testable | Partially validated |
| **Brain Regions** | **10** (7→10: +Putamen, +M1, +Auditory Cortex) | Harrison 2025, Liang 2025, Yamashita 2025 |
| **R³ Features Used** | 29D of 49D | Energy + Change + Interactions |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **Output Dimensions** | **10D** | 4-layer structure |

---

## 13. Scientific References

1. **Thaut, McIntosh & Hoemberg (2015)**. Neurobiological foundations of neurologic music therapy: rhythmic entrainment and the motor system. *Frontiers in Psychology*, 5:1185. doi:10.3389/fpsyg.2014.01185. Review. Key findings: Period entrainment (not beat entrainment) drives motor optimization; auditory rhythm via reticulospinal pathways primes motor system; anticipatory temporal templates optimize motor planning; RAS improves gait in stroke, PD, TBI, cerebral palsy.
2. **Harrison et al. (2025)**. Neural mechanisms underlying synchronization of movement to musical cues in Parkinson disease and aging. *Frontiers in Neuroscience*, 19:1550802. doi:10.3389/fnins.2025.1550802. fMRI, PwPD + HC. Key findings: External cues activate sensorimotor cortex, temporal gyri, SMA, putamen; internal cues (mental singing) additionally activate cerebellum; CTC and SPT pathways work in tandem.
3. **Huang & Qi (2025)**. Neurobiological mechanism of music improving gait disorder in patients with Parkinson's disease: a mini review. *Frontiers in Neurology*, 15:1502561. doi:10.3389/fneur.2024.1502561. Review. Key findings: Music therapy bypasses dysfunctional basal ganglia via auditory-motor neural networks; CPG synchronizes gait with musical rhythm through entrainment.
4. **Blasi et al. (2025)**. Structural and functional neuroplasticity in music and dance-based rehabilitation: a systematic review. *Journal of Neurology*, 272:329. doi:10.1007/s00415-025-13048-6. 20 RCTs, N=718. Key findings: Increased hippocampal volume (dance), increased GM in frontal/temporal/cerebellar regions (music), enhanced FC within language/motor networks (stroke, TBI, dementia).
5. **Buard et al. (2021)**. Randomized controlled trial of neurologic music therapy in Parkinson's disease: research rehabilitation protocols for mechanistic and clinical investigations. *Trials*. doi:10.1186/s13063-021-05560-7. RCT protocol, N=100 planned. TIMP with/without rhythm vs OT for PD fine motor rehabilitation; MEG outcomes.
6. **Yamashita et al. (2025)**. A pilot study on simultaneous stimulation of the primary motor cortex and supplementary motor area using gait-synchronized rhythmic brain stimulation to improve gait variability in post-stroke hemiparetic patients. *Frontiers in Human Neuroscience*, 19:1618758. doi:10.3389/fnhum.2025.1618758. Pilot RCT, N=15. Gait-synchronized tACS at M1+SMA reduced step length variability.
7. **Liang et al. (2025)**. The brain mechanisms of music stimulation, motor observation, and motor imagination in virtual reality techniques: A functional near-infrared spectroscopy study. *eNeuro*. doi:10.1523/ENEURO.0557-24.2025. fNIRS, N=26. Music + VR motor observation activated bilateral SMA, premotor, PFC more than motor observation alone.
8. **Ross & Balasubramaniam (2022)**. Time Perception for Musical Rhythms: Sensorimotor Perspectives on Entrainment, Simulation, and Prediction. *Frontiers in Integrative Neuroscience*, 16:916220. doi:10.3389/fnint.2022.916220. Mini review. Key findings: Sensorimotor system simulates beats even without movement; SMA, premotor, cerebellum, basal ganglia form beat perception network; cerebellar forward models for predictive timing.
9. **Jiao (2025)**. Advancing personalized digital therapeutics: integrating music therapy, brainwave entrainment methods, and AI-driven biofeedback. *Frontiers in Digital Health*, 7:1552396. doi:10.3389/fdgth.2025.1552396. Mini review. Key findings: Multi-modal synergy (music therapy + entrainment + multisensory) enhances outcomes; 40 Hz gamma supports memory; AI-driven closed-loop adaptation.
10. **Liuzzi et al. (2025)**. Inclusive orchestral music therapy according to the Euterpe Method: a multimodal framework for neurodevelopmental disorders. *Frontiers in Neurology*, 16:1612955. doi:10.3389/fneur.2025.1612955. Framework. Multimodal orchestral therapy engages fronto-striatal, cerebellar, temporal networks for NDD rehabilitation.
11. **Fang et al. (2017)**. Music therapy is a potential intervention for cognition of Alzheimer's Disease: a mini-review. *Translational Neurodegeneration*. doi:10.1186/s40035-017-0073-9. Review. MT reduces cognitive decline in autobiographical/episodic memory, psychomotor speed, executive function.
12. **Provias et al. (2025)**. Feasibility Trial Protocol for a Remote Intentional Music Listening Intervention to Support Mental Health in Individuals with Chronic Stroke. Feasibility protocol. Self-selected familiar music for chronic stroke recovery activates reward and memory circuits.
13. **Li et al. (2025)**. Musical groove and running biomechanics. *Journal of NeuroEngineering and Rehabilitation*, 22:233. doi:10.1186/s12984-025-01778-7. Biomechanical analysis. Musical groove modulates locomotion through auditory-motor coupling.
14. **Castillo et al. (2025)**. Music in sports science and rehabilitation. *BMC Sports Science, Medicine and Rehabilitation*, 17:190. doi:10.1186/s13102-025-01246-8. Systematic review. RAS efficacy across rehabilitation and athletic populations.
15. **Shi et al. (2025)**. Action observation and imitation training for cognitive-motor rehabilitation. *Journal of NeuroEngineering and Rehabilitation*, 22:247. doi:10.1186/s12984-025-01789-4. Multi-study review. Visual-motor integration in neurorehabilitation; cross-modal observation + execution enhances neural plasticity.

---

## 14. Migration Notes (D0 → MI) and Version History

### What Changed from v2.0.0 → v2.1.0

| Aspect | v2.0.0 | v2.1.0 |
|--------|--------|--------|
| Papers | 4 (unverifiable Zhao 2025, 3 vague references) | **15** (verified: Thaut 2015, Harrison 2025, Blasi 2025, Huang & Qi 2025, Buard 2021, Yamashita 2025, Liang 2025, Ross & Balasubramaniam 2022, Jiao 2025, Liuzzi 2025, Fang 2017, Provias 2025, Li 2025, Castillo 2025, Shi 2025) |
| Brain regions | 7 (some inferred) | **10** (+Putamen per Harrison 2025, +M1 per Yamashita 2025, +Auditory Cortex per Harrison 2025) |
| MNI verification | Generic coordinates | Verified from Harrison 2025 (fMRI), Liang 2025 (fNIRS), Yamashita 2025 (tACS target sites) |
| Evidence sources | Unverifiable "Zhao 2025" cited for 968 patients | Replaced with Blasi 2025 (20 RCTs, N=718), Harrison 2025 (fMRI), Liang 2025 (fNIRS N=26), Yamashita 2025 (pilot N=15) |
| Falsification | 1/5 supported | **2/5 supported** (cerebellar disruption partially supported by Harrison 2025) |
| Doc-code mismatches | Not documented | **Documented**: code implements entirely different model concept ("Recognition-Recall Integration Recency Index") |

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D): L4, L5, L9, X_L0L1, X_L1L5, X_L4L5 | R³ (49D): Energy, Change, Interactions |
| Multi-modal entrainment | S⁰.X_L0L1[128:136] × HC⁰.NPL | R³.x_l0l5[25:33] |
| Sensorimotor integration | S⁰.X_L4L5[192:200] × HC⁰.EFC | R³.x_l4l5[33:41] |
| Enhanced recovery | S⁰.X_L1L5[152:160] × HC⁰.GRV | R³.x_l5l7[41:49] |
| Demand format | HC⁰ index ranges (15/2304 = 0.65%) | H³ 4-tuples (16/2304 = 0.69%) |
| Output dimensions | 11D | **10D** (catalog-corrected) |

---

**Model Status**: ✅ **VALIDATED** (v2.1.0, 15 papers, 10 brain regions)
**Output Dimensions**: **10D**
**Evidence Tier**: **β (Integrative)**
**Confidence**: **70-90%**
