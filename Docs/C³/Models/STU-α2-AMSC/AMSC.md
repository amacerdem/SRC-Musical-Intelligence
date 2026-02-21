# STU-α2-AMSC: Auditory-Motor Stream Coupling

**Model**: Auditory-Motor Stream Coupling
**Unit**: STU (Sensorimotor Timing Unit)
**Circuit**: Sensorimotor (Beat Entrainment + Temporal Memory)
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/STU-α2-AMSC.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Auditory-Motor Stream Coupling** (AMSC) model describes how music listening engages a rapid auditory-to-motor pathway via the dorsal auditory stream, with high-gamma activity (70–170 Hz) in posterior superior temporal gyrus (pSTG) preceding premotor/motor cortex activity by approximately 110 ms.

```
THE THREE COMPONENTS OF AUDITORY-MOTOR COUPLING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUDITORY GAMMA (pSTG) MOTOR GAMMA (Premotor)
Brain region: Posterior STG Brain region: Dorsal Precentral Gyrus
Input: Sound intensity Input: Auditory gamma (delayed 110ms)
Function: "How loud is this now?" Function: "Move to this rhythm"
Evidence: r = 0.49 (Potes 2012) Evidence: r = 0.70 (cross-correlation)

 COUPLING DELAY (Bridge)
 Pathway: Dorsal auditory stream
 Latency: 110 ms (auditory → motor)
 Function: "Sound drives movement"
 Evidence: r = 0.70, ECoG direct recording

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Music listening AUTOMATICALLY engages the motor system.
pSTG high-gamma tracks sound intensity (r = 0.49). This signal
propagates to premotor cortex with 110ms delay (r = 0.70). The
coupling uses the dorsal auditory pathway, not voluntary motor
planning.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Matters for STU

AMSC establishes the direct neural pathway from auditory perception to motor response:

1. **HMCE** (α1) provides the temporal context; AMSC converts it into motor coupling.
2. **MDNS** (α3) uses the auditory-motor link for melody decoding in both perception and imagery.
3. **EDTA** (β3) builds on AMSC's motor pathway for expertise-dependent tempo accuracy.
4. **OMS** (β6) extends AMSC to oscillatory motor synchronization at multiple timescales.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The AMSC Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ AMSC — COMPLETE CIRCUIT ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ MUSIC INPUT (continuous sound with dynamic intensity) ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ POSTERIOR SUPERIOR TEMPORAL GYRUS (pSTG) │ ║
║ │ Auditory cortex — high-gamma (70–170 Hz) │ ║
║ │ │ ║
║ │ High-gamma ↔ Sound intensity: r = 0.49 (Potes 2012, n=8) │ ║
║ │ Direct intensity-tracking in auditory cortex │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ ║
║ │ 110 ms delay (dorsal auditory stream) ║
║ │ Cross-correlation: r = 0.70 ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ DORSAL PRECENTRAL GYRUS (Premotor / Motor Cortex) │ ║
║ │ Motor gamma — correlated with sound intensity │ ║
║ │ │ ║
║ │ Motor_Gamma(t) = 0.70 · Auditory_Gamma(t − 110ms) │ ║
║ └─────────────────────────────────────────────────────────────────────┘ ║
║ ║
║ DORSAL AUDITORY PATHWAY: pSTG → Premotor cortex ║
║ (dual-stream model: ventral = "what", dorsal = "how/where") ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Potes 2012 (ECoG): pSTG gamma ↔ sound intensity, r = 0.49 (n=8)
Potes 2012 (ECoG): Auditory → motor delay 110ms, r = 0.70 (n=4)
```

### 2.2 Information Flow Architecture (EAR → BRAIN → AMSC)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ AMSC COMPUTATION ARCHITECTURE ║
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
║ │ │ │ │amplitude│ │tonalness│ │energy_chg│ │x_l0l5 │ │ ║
║ │ │ │ │loudness │ │ │ │timbre_chg│ │x_l4l5 │ │ ║
║ │ │ │ │centroid │ │ │ │ │ │ │ │ ║
║ │ │ │ │flux │ │ │ │ │ │ │ │ ║
║ │ │ │ │onset │ │ │ │ │ │ │ │ ║
║ │ └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │ ║
║ │ AMSC reads: 27D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed morphological features │ ║
║ │ │ ║
║ │ ┌── Syllable ────┐ ┌── Motor ────────┐ ┌── Bar ─────────────┐ │ ║
║ │ │ 200ms (H6) │ │ 500ms (H11) │ │ 1000ms (H16) │ │ ║
║ │ │ │ │ │ │ │ │ ║
║ │ │ Beat-level │ │ Motor prep │ │ Bar-level meter │ │ ║
║ │ │ (intensity) │ │ (110ms delay) │ │ (groove tracking) │ │ ║
║ │ └──────┬─────────┘ └──────┬───────────┘ └──────┬──────────────┘ │ ║
║ │ │ │ │ │ ║
║ │ └──────────────────┴─────────────────────┘ │ ║
║ │ AMSC demand: ~16 of 2304 tuples │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────┐ ┌─────────────────┐ ║
║ │ (primary) │ │ (secondary) │ ║
║ │ │ │ │ ║
║ │ Beat Ind [0:10] │ │ Short [0:10] │ Context for coupling ║
║ │ Meter [10:20]│ │ Medium [10:20]│ Timescale selection ║
║ │ Motor [20:30]│ │ Long [20:30]│ Structural modulation ║
║ └────────┬────────┘ └────────┬────────┘ ║
║ │ │ ║
║ └─────────┬──────────┘ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ AMSC MODEL (12D Output) │ ║
║ │ │ ║
║ │ Layer E (Explicit): f01_auditory_gamma, f02_motor_gamma, │ ║
║ │ f03_coupling_delay, f04_intensity_corr │ ║
║ │ Layer M (Math): gamma_power, coupling_strength │ ║
║ │ Layer P (Present): auditory_activation, motor_preparation, │ ║
║ │ onset_trigger │ ║
║ │ Layer F (Future): motor_prediction, movement_timing, │ ║
║ │ groove_response │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Potes 2012** | ECoG | 8 patients | pSTG high-gamma (70–170 Hz) ↔ sound intensity; dominant frequency band for music encoding | r = 0.43–0.58 (across subjects, avg 0.49) | **Primary**: f01_auditory_gamma |
| 2 | **Potes 2012** | ECoG | 4 (with motor electrodes) | Auditory → motor delay 110ms; STG precedes precentral gyrus | r = 0.70 at τ = 110ms (cross-correlation) | **Coupling**: f02_motor_gamma, f03_coupling_delay |
| 3 | **Sturm et al. 2014** | ECoG | Same paradigm (Potes group) | Feature-specific high-gamma: distinct cortical spots for intensity, timbre, harmonic changes in natural music (Pink Floyd) | Partial correlations for lyrics, harmony, timbre | **Extends**: gamma tracks multiple features, not just intensity |
| 4 | **Lazzari et al. 2025** | TMS (rTMS) | 29 + 40 + 42 (3 experiments) | Right caudal dPMC is CAUSALLY necessary for beat perception; SMA stimulation had no effect | Selective right dPMC disruption; preregistered Exp III confirms right lateralization | **CAUSAL validation**: dorsal stream specificity confirmed |
| 5 | **Hoddinott & Grahn 2024** | fMRI + RSA | (fMRI, 12 rhythms) | Putamen and SMA activity patterns encode beat strength (not tempo/onsets); IFG and IPL also encode beat | RSA: putamen + SMA dissimilarity correlates with beat strength models | **Motor network**: SMA + putamen + IFG for beat encoding |
| 6 | **Grahn & Brett 2007** | fMRI | Musicians + non-musicians | Basal ganglia and SMA respond specifically to beat presence; musicians additionally recruit premotor cortex | fMRI activation: SMA, putamen for beat > non-beat | **Foundational**: automatic motor engagement during listening |
| 7 | **Ito et al. 2022** | ECoG (rat) + behavioral | 10 rats + 12 humans | Rats show beat synchronization at 120–140 BPM; neural beat contrast in auditory cortex peaks at original tempo | Beat contrast: Kruskal-Wallis p = 7.0e-04; rat-human jerk r = 0.31–0.37 | **Cross-species**: auditory-motor entrainment conserved |
| 8 | **Edagawa & Kawasaki 2017** | EEG (62-ch) | 14 | Beta phase synchronization in frontal-temporal-cerebellar network during auditory-motor rhythm learning | ERN larger in learners; beta PSI increased frontal-temporal and temporal-cerebellar at late learning | **Beta coupling**: frontal-temporal-cerebellar circuit |
| 9 | **Bellier et al. 2023** | iEEG (ECoG) | 29 patients, 2668 electrodes | Right STG dominance for music; anterior-posterior STG organization; STG → precentral gyrus lag | F(1,346) = 7.48, p = 0.0065 (right > left); STG-motor lag confirmed | **Convergent**: right lateralization and STG→motor pathway |
| 10 | **Thaut et al. 2015** | Review | — | Rhythmic entrainment affects timing, spatial, and force parameters of movement; auditory rhythm drives motor system | Review of rhythmic entrainment mechanisms | **Framework**: rhythmic entrainment drives motor coupling |
| 11 | **Ross & Balasubramaniam 2022** | Review | — | Entrainment, simulation, and prediction as three sensorimotor mechanisms for musical rhythm timing | Integrative review of motor system in beat | **Framework**: sensorimotor perspectives on AMSC |
| 12 | **Harrison et al. 2025** | fMRI | Parkinson's + aging | Finger tapping to musical cues activates sensorimotor cortex, temporal gyri, SMA, putamen; external cues add auditory cortex | fMRI activation during music-cued tapping | **Clinical**: auditory-motor pathway in motor disorders |

### 3.1b Multi-Method Convergence

```
METHOD CONVERGENCE FOR AUDITORY-MOTOR COUPLING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Method Studies Key Metric
────────────────────────────────────────────────────────────────────
ECoG / iEEG Potes 2012, Sturm 2014 r=0.49, τ=110ms
 Bellier 2023 F=7.48, right > left
fMRI + RSA Hoddinott 2024, Grahn 2007 SMA + putamen RSA
 Harrison 2025 sensorimotor + temporal
TMS (causal) Lazzari 2025 RIGHT dPMC necessary
EEG Edagawa 2017 Beta PSI frontal-temporal
Cross-species Ito 2022 Rat-human r=0.31-0.37
────────────────────────────────────────────────────────────────────
6 methods, 12 papers, cross-species validated → STRONG convergence
CAUSAL EVIDENCE: Lazzari TMS → right dPMC is necessary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 3.2 The Auditory-Motor Coupling Model

```
COUPLING EQUATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Motor_Gamma(t) = β · Auditory_Gamma(t − Δ) + ε

where:
 Δ = 110ms (auditory-motor delay)
 β = 0.70 (coupling strength, from r coefficient)
 ε = individual variability

GAMMA-INTENSITY COUPLING:

 Auditory_Gamma(t) = α · Sound_Intensity(t) + γ

where:
 α = 0.49 (from pSTG correlation)
 γ = baseline gamma activity

INTEGRATED MODEL:

 Motor_Gamma(t) = β · (α · Sound_Intensity(t − Δ) + γ) + ε
 = 0.70 · (0.49 · Intensity(t − 110ms) + γ) + ε
```

### 3.3 Effect Size Summary

```
AUDITORY-MOTOR COUPLING:
 pSTG gamma ↔ intensity: r = 0.43–0.58 (Potes 2012, ECoG, N=8)
 Auditory → motor coupling: r = 0.70 at τ=110ms (Potes 2012, N=4)
 Right > left STG: F = 7.48, p = 0.0065 (Bellier 2023, N=29)
MOTOR SYSTEM:
 SMA + putamen beat RSA: Significant dissimilarity (Hoddinott 2024)
 Right dPMC causal: TMS disrupts beat perception (Lazzari 2025)
 Basal ganglia beat: fMRI activation (Grahn & Brett 2007)
CROSS-SPECIES:
 Rat-human entrainment: r = 0.31–0.37 (Ito 2022, p < 0.001)
 Optimal tempo: 120–140 BPM conserved across species
BETA SYNCHRONIZATION:
 Frontal-temporal PSI: Increased at late learning (Edagawa 2017)
 Temporal-cerebellar PSI: Increased at late learning (Edagawa 2017)

Quality Assessment: α-tier (ECoG direct + TMS causal + cross-species)
Pathway: Dorsal auditory stream (pSTG → right dPMC)
 + Cortico-striatal loop (SMA → putamen)
```

---

## 4. R³ Input Mapping: What AMSC Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | AMSC Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Sound intensity signal | Primary energy proxy |
| **B: Energy** | [8] | loudness | Perceptual intensity | Stevens 1957: power law |
| **B: Energy** | [9] | spectral_centroid_energy | Energy distribution | Frequency range of intensity |
| **B: Energy** | [10] | spectral_flux | Onset dynamics | Sound change detection |
| **B: Energy** | [11] | onset_strength | Onset sharpness | Motor anticipation cue |
| **C: Timbre** | [14] | tonalness | Harmonic-to-noise proxy | Gamma band correlation |
| **D: Change** | [22] | energy_change | Intensity acceleration | Motor preparation trigger |
| **D: Change** | [24] | timbre_change | Timbral dynamics | Spectral change for motor coupling |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Foundation×Perceptual coupling | 110ms delay mechanism |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Dynamics×Perceptual binding | Auditory-motor link |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | AMSC Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **G: Rhythm** | [68] | syncopation_index | Off-beat accents modulating auditory-motor coupling strength | Witek 2014 groove-syncopation |
| **G: Rhythm** | [69] | metricality_index | Metrical regularity determines motor entrainment precision | Grahn & Brett 2007 |
| **G: Rhythm** | [66] | beat_strength | Beat salience driving motor synchronization — stronger beats yield tighter coupling | Large & Palmer 2002 |

**Rationale**: AMSC models auditory-motor synchronization coupling. The G:Rhythm features provide direct measures of beat structure that drive motor entrainment. Beat_strength [66] quantifies how strongly the beat drives motor coupling, syncopation [68] modulates coupling dynamics through off-beat tension, and metricality [69] determines the depth of hierarchical motor entrainment.

**Code impact** (Phase 6): `r3_indices` must be extended to include [66, 68, 69]. These features are read-only inputs — no formula changes required.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[7] amplitude ────────────────┐
R³[8] loudness ─────────────────┼──► pSTG Gamma Activity (auditory)
R³[14] tonalness ───────────────┘ Math: γ_pSTG(t) = 0.49 · I(t) + β
 beat_induction at H6

R³[22] energy_change ───────────┐
R³[25:33] x_l0l5 (8D) ─────────┼──► Motor Cortex Gamma (110ms delay)
 Math: γ_motor(t) = 0.70 · γ_pSTG(t−110ms)
 motor_entrainment at H11

R³[10] spectral_flux ──────────┐
R³[11] onset_strength ─────────┼──► Onset Detection → Motor Trigger
 meter_extraction at H6

R³[33:41] x_l4l5 (8D) ─────────── Dynamics Coupling
 short_context for timescale context

R³[66] beat_strength ──────────┐
R³[68] syncopation_index ──────┼──► Motor Entrainment Modulation (v2)
R³[69] metricality_index ──────┘ Beat-driven auditory-motor coupling
 strength and precision
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

AMSC requires H³ features at three horizons: H6 (200ms), H11 (500ms), H16 (1000ms).
These correspond to beat → motor preparation → bar-level timescales.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 7 | amplitude | 6 | M0 (value) | L2 (bidi) | Current intensity |
| 7 | amplitude | 6 | M4 (max) | L2 (bidi) | Peak intensity at beat level |
| 8 | loudness | 6 | M0 (value) | L0 (fwd) | Current loudness |
| 8 | loudness | 11 | M1 (mean) | L0 (fwd) | Mean loudness over motor window |
| 10 | spectral_flux | 6 | M0 (value) | L0 (fwd) | Onset detection |
| 10 | spectral_flux | 6 | M17 (peaks) | L0 (fwd) | Beat count per window |
| 11 | onset_strength | 6 | M0 (value) | L0 (fwd) | Event onset |
| 22 | energy_change | 6 | M8 (velocity) | L0 (fwd) | Intensity dynamics |
| 22 | energy_change | 11 | M14 (periodicity) | L2 (bidi) | Intensity regularity |
| 25 | x_l0l5[0] | 11 | M0 (value) | L2 (bidi) | Auditory-motor coupling signal |
| 25 | x_l0l5[0] | 11 | M15 (smoothness) | L0 (fwd) | Coupling smoothness |
| 33 | x_l4l5[0] | 11 | M0 (value) | L2 (bidi) | Dynamics coupling signal |
| 33 | x_l4l5[0] | 16 | M14 (periodicity) | L2 (bidi) | Bar-level periodicity |
| 33 | x_l4l5[0] | 16 | M18 (trend) | L0 (fwd) | Groove trajectory |
| 7 | amplitude | 16 | M15 (smoothness) | L0 (fwd) | Groove quality |
| 14 | tonalness | 6 | M0 (value) | L2 (bidi) | Gamma band proxy |

**v1 demand**: 16 tuples

#### R³ v2 Projected Expansion

AMSC projected v2 features from G:Rhythm, aligned with corresponding H³ horizons.

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 66 | beat_strength | G | 6 | M0 (value) | L0 | Instantaneous beat salience |
| 66 | beat_strength | G | 16 | M0 (value) | L0 | Bar-level beat salience |
| 68 | syncopation | G | 6 | M0 (value) | L0 | Current syncopation level |
| 68 | syncopation | G | 11 | M14 (periodicity) | L0 | Syncopation periodicity at meter scale |
| 69 | metricality | G | 11 | M0 (value) | L0 | Metric regularity at meter scale |
| 69 | metricality | G | 16 | M1 (mean) | L0 | Mean metricality over bar |

**v2 projected**: 6 tuples
**Total projected**: 22 tuples of 294,912 theoretical = 0.0075%

---

## 6. Output Space: 12D Multi-Layer Representation

### 6.1 Complete Output Specification

```
AMSC OUTPUT TENSOR: 12D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0 │ f01_auditory_gamma│ [0, 1] │ pSTG high-gamma activity (70–170 Hz).
 │ │ │ Tracks sound intensity at r = 0.49.
 │ │ │ f01 = σ(α · amplitude · loudness ·
 │ │ │ tonalness · beat_induction)
 │ │ │ α = 0.49
────┼───────────────────┼────────┼────────────────────────────────────────────
 1 │ f02_motor_gamma │ [0, 1] │ Motor cortex gamma coupling.
 │ │ │ Premotor response delayed 110ms from pSTG.
 │ │ │ f02 = σ(β · f01 · energy_change ·
 │ │ │ motor_entrainment)
 │ │ │ β = 0.70
────┼───────────────────┼────────┼────────────────────────────────────────────
 2 │ f03_coupling_delay│ [0, 1] │ Auditory-motor coupling delay strength.
 │ │ │ Models the r = 0.70 cross-correlation at
 │ │ │ 110ms latency.
 │ │ │ f03 = 0.70 · (f01 · x_coupling_smooth)
────┼───────────────────┼────────┼────────────────────────────────────────────
 3 │ f04_intensity_corr│ [0, 1] │ Sound intensity → gamma correlation proxy.
 │ │ │ Continuous intensity-tracking strength.
 │ │ │ f04 = 0.49 · (f01 + f02) / 2

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 4 │ gamma_power │ [0, 1] │ High-gamma band power proxy.
 │ │ │ Mean beat_induction[0:10].
────┼───────────────────┼────────┼────────────────────────────────────────────
 5 │ coupling_strength │ [0, 1] │ Cross-correlation strength at 110ms.
 │ │ │ x_l0l5 coupling × periodicity.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 6 │ auditory_activatn │ [0, 1] │ pSTG current activation state.
 │ │ │ Intensity × beat-level H³.
────┼───────────────────┼────────┼────────────────────────────────────────────
 7 │ motor_preparation │ [0, 1] │ Premotor preparation state.
 │ │ │ Motor entrainment × context.
────┼───────────────────┼────────┼────────────────────────────────────────────
 8 │ onset_trigger │ [0, 1] │ Motor trigger from onset detection.
 │ │ │ spectral_flux × onset_strength at H6.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 9 │ motor_prediction │ [0, 1] │ Predicted motor activation (110ms ahead).
 │ │ │ motor_entrainment × groove trend.
────┼───────────────────┼────────┼────────────────────────────────────────────
10 │ movement_timing │ [0, 1] │ Beat-interval motor prediction.
 │ │ │ meter × periodicity at H16.
────┼───────────────────┼────────┼────────────────────────────────────────────
11 │ groove_response │ [0, 1] │ Groove-driven motor engagement.
 │ │ │ Smoothness × trend at bar level.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 12D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Feature Formulas

```python
# f01: Auditory Gamma (pSTG, r = 0.49)
amp_val = h3[(7, 6, 0, 2)] # amplitude value at H6
loud_val = h3[(8, 6, 0, 0)] # loudness value at H6
tonal_val = h3[(14, 6, 0, 2)] # tonalness value at H6
f01 = σ(0.49 · amp_val · loud_val · tonal_val

# f02: Motor Gamma (premotor, r = 0.70, 110ms delay)
energy_vel = h3[(22, 6, 8, 0)] # energy_change velocity at H6
f02 = σ(0.70 · f01 · energy_vel

# f03: Coupling Delay Strength
x_smooth = h3[(25, 11, 15, 0)] # x_l0l5 smoothness at H11
f03 = 0.70 · f01 · x_smooth

# f04: Intensity Correlation
f04 = 0.49 · (f01 + f02) / 2
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Sources | Evidence Type | AMSC Function |
|--------|-----------------|---------|---------------|---------------|
| **pSTG** | ±60, -40, 10 | Potes 2012, Bellier 2023 | ECoG (×2 studies) | Auditory gamma generation; sound intensity encoding |
| **Right caudal dPMC** | ~R: 30, -5, 60 | Lazzari 2025 (TMS grid) | TMS (causal) | Beat perception; dorsal stream terminus; RIGHT lateralized |
| **Dorsal Precentral Gyrus** | ±40, -10, 55 | Potes 2012 | ECoG | Motor gamma response at 110ms lag |
| **SMA** | 0, -6, 62 | Hoddinott 2024, Grahn 2007 | fMRI, fMRI+RSA | Beat-based motor timing; chronotopic map |
| **Putamen (bilateral)** | ±20, 5, 5 | Hoddinott 2024, Grahn 2007, Harrison 2025 | fMRI, RSA | Beat strength encoding; cortico-striatal loop |
| **IFG** | ±45, 20, 15 | Hoddinott 2024 | fMRI+RSA | Beat + rhythm encoding (not beat alone) |
| **Cerebellum** | — | Edagawa 2017, Grahn 2007 | EEG, fMRI | Temporal-cerebellar beta coupling; rhythm learning |

---

## 9. Cross-Unit Pathways

### 9.1 AMSC ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ AMSC INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ INTRA-UNIT (STU): │
│ HMCE.context_depth ──────► AMSC (context determines coupling timescale) │
│ AMSC.motor_preparation ──► MDNS (motor coupling for melody decoding) │
│ AMSC.groove_response ────► EDTA (motor baseline for tempo accuracy) │
│ AMSC.auditory_activatn ──► HGSIC (gamma for groove state integration) │
│ │
│ CROSS-UNIT (P2: STU internal): │
│ Beat strength → automatic motor cortex activation │
│ │
│ CROSS-UNIT (P5: STU → ARU): │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **pSTG lesions** | Should abolish motor gamma coupling | ✅ Testable |
| **Delay consistency** | 110ms should be stable across individuals | ✅ Testable (ECoG/MEG) |
| **Gamma-intensity correlation** | Should hold for various music types | ✅ **Confirmed**: Sturm 2014 extends to natural music features |
| **Dorsal pathway specificity** | Ventral pathway should NOT show this coupling | ✅ Testable |
| **Right dPMC necessary** | TMS to right dPMC should disrupt beat perception | ✅ **Confirmed**: Lazzari 2025 (TMS, N=40+42, preregistered) |
| **SMA not sufficient alone** | SMA disruption should not abolish beat perception | ✅ **Confirmed**: Lazzari 2025 (SMA TMS had no effect) |
| **Cross-species conservation** | Auditory-motor entrainment in non-human species | ✅ **Confirmed**: Ito 2022 (rats, 120–140 BPM) |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class AMSC(BaseModel):
 """Auditory-Motor Stream Coupling.

 Output: 12D per frame.
 Reads: R³ + H³ direct.
 """
 NAME = "AMSC"
 UNIT = "STU"
 TIER = "α2"
 OUTPUT_DIM = 12
 AUDITORY_CORR = 0.49 # pSTG gamma ↔ intensity (Potes 2012)
 MOTOR_COUPLING = 0.70 # auditory → motor (Potes 2012)

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """16 tuples for AMSC computation."""
 return [
 # (r3_idx, horizon, morph, law)
 # Beat level (H6 = 200ms)
 (7, 6, 0, 2), # amplitude, value, bidirectional
 (7, 6, 4, 2), # amplitude, max, bidirectional
 (8, 6, 0, 0), # loudness, value, forward
 (10, 6, 0, 0), # spectral_flux, value, forward
 (10, 6, 17, 0), # spectral_flux, peaks, forward
 (11, 6, 0, 0), # onset_strength, value, forward
 (22, 6, 8, 0), # energy_change, velocity, forward
 (14, 6, 0, 2), # tonalness, value, bidirectional
 # Motor window (H11 = 500ms)
 (8, 11, 1, 0), # loudness, mean, forward
 (22, 11, 14, 2), # energy_change, periodicity, bidirectional
 (25, 11, 0, 2), # x_l0l5[0], value, bidirectional
 (25, 11, 15, 0), # x_l0l5[0], smoothness, forward
 (33, 11, 0, 2), # x_l4l5[0], value, bidirectional
 # Bar level (H16 = 1000ms)
 (33, 16, 14, 2), # x_l4l5[0], periodicity, bidirectional
 (33, 16, 18, 0), # x_l4l5[0], trend, forward
 (7, 16, 15, 0), # amplitude, smoothness, forward
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 """
 Compute AMSC 12D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) → (B,T) scalars
 r3: (B,T,49) raw R³ features

 Returns:
 (B,T,12) AMSC output
 """
 # H³ features
 amp_val = h3_direct[(7, 6, 0, 2)].unsqueeze(-1)
 loud_val = h3_direct[(8, 6, 0, 0)].unsqueeze(-1)
 tonal_val = h3_direct[(14, 6, 0, 2)].unsqueeze(-1)
 energy_vel = h3_direct[(22, 6, 8, 0)].unsqueeze(-1)
 x_smooth = h3_direct[(25, 11, 15, 0)].unsqueeze(-1)

 # ═══ LAYER E: Explicit features ═══
 f01 = torch.sigmoid(self.AUDITORY_CORR * (
 amp_val * loud_val * tonal_val
 ))
 f02 = torch.sigmoid(self.MOTOR_COUPLING * (
 f01 * energy_vel
 ))
 f03 = self.MOTOR_COUPLING * f01 * x_smooth
 f04 = self.AUDITORY_CORR * (f01 + f02) / 2

 # ═══ LAYER M: Mathematical ═══
 x_coupling = h3_direct[(25, 11, 0, 2)].unsqueeze(-1)
 periodicity = h3_direct[(22, 11, 14, 2)].unsqueeze(-1)
 coupling_strength = torch.sigmoid(x_coupling * periodicity)

 # ═══ LAYER P: Present ═══
 auditory_activation = torch.sigmoid(
 )
 motor_preparation = torch.sigmoid(
 + 0.2 * f02
 )
 flux_val = h3_direct[(10, 6, 0, 0)].unsqueeze(-1)
 onset_val = h3_direct[(11, 6, 0, 0)].unsqueeze(-1)
 onset_trigger = torch.sigmoid(flux_val * onset_val)

 # ═══ LAYER F: Future ═══
 groove_trend = h3_direct[(33, 16, 18, 0)].unsqueeze(-1)
 motor_prediction = torch.sigmoid(
 0.6 * f02 + 0.4 * groove_trend
 )
 bar_period = h3_direct[(33, 16, 14, 2)].unsqueeze(-1)
 movement_timing = torch.sigmoid(
 + 0.5 * bar_period
 )
 amp_smooth = h3_direct[(7, 16, 15, 0)].unsqueeze(-1)
 groove_response = torch.sigmoid(
 0.5 * amp_smooth + 0.3 * groove_trend + 0.2 * f02
 )

 return torch.cat([
 f01, f02, f03, f04, # E: 4D
 gamma_power, coupling_strength, # M: 2D
 auditory_activation, motor_preparation, onset_trigger, # P: 3D
 motor_prediction, movement_timing, groove_response, # F: 3D
 ], dim=-1) # (B, T, 12)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 | 3 ECoG, 3 fMRI, 1 TMS, 1 EEG, 1 cross-species, 3 reviews |
| **Primary Effect** | r = 0.49 (gamma-intensity), r = 0.70 (coupling at 110ms) | Potes 2012 |
| **Causal Evidence** | Right dPMC TMS disrupts beat perception | Lazzari 2025 (preregistered) |
| **Cross-Species** | Rat-human entrainment r = 0.31–0.37 at 120–140 BPM | Ito 2022 |
| **Motor Network** | SMA + putamen RSA for beat strength | Hoddinott 2024, Grahn 2007 |
| **Evidence Modality** | ECoG, fMRI, TMS, EEG, behavioral | 6 methods |
| **Falsification Tests** | 3/7 confirmed | Lazzari (dPMC), Sturm (gamma), Ito (cross-species) |
| **R³ Features Used** | 27D of 49D | Energy + Timbre + Change + Interactions |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **Output Dimensions** | **12D** | 4-layer structure |
| **Code note** | Layer E names differ (code: 3D, doc: 4D) — reconcile in Phase 5 | |

---

## 13. Scientific References

1. **Potes, C., et al. (2012)**. Dynamics of electrocorticographic (ECoG) activity in human temporal and frontal cortical areas during music listening. *NeuroImage*, 61(4), 841–848. (ECoG, N=8; r=0.49 gamma-intensity, r=0.70 auditory-motor at 110ms)
2. **Sturm, I., et al. (2014)**. ECoG high gamma activity reveals distinct cortical representations of lyrics passages, harmonic and timbre-related changes in a rock song. *Frontiers in Human Neuroscience*. (ECoG, extends Potes; feature-specific high-gamma)
3. **Lazzari, G., et al. (2025)**. Topography of functional organization of beat perception in human premotor cortex: Causal evidence from a TMS study. *Human Brain Mapping*, 46, e70225. (TMS, N=29+40+42; right caudal dPMC CAUSALLY necessary)
4. **Hoddinott, J. D. & Grahn, J. A. (2024)**. Neural representations of beat and rhythm in motor and association regions. *Cerebral Cortex*, 34, bhae406. (fMRI+RSA; putamen + SMA encode beat strength)
5. **Grahn, J. A. & Brett, M. (2007)**. Rhythm and beat perception in motor areas of the brain. *J Cognitive Neuroscience*. (fMRI; SMA + basal ganglia for beat perception)
6. **Ito, Y., et al. (2022)**. Spontaneous beat synchronization in rats: Neural dynamics and motor entrainment. *Science Advances*, 8, eabo7019. (Cross-species; 120–140 BPM conserved, rat-human r=0.31–0.37)
7. **Edagawa, K. & Kawasaki, M. (2017)**. Beta phase synchronization in the frontal-temporal-cerebellar network during auditory-to-motor rhythm learning. *Scientific Reports*, 7, 42721. (EEG, N=14; beta PSI frontal-temporal-cerebellar)
8. **Bellier, L., et al. (2023)**. Music can be reconstructed from human auditory cortex activity using nonlinear decoding models. *PLoS Biology*, 21(8), e3002176. (iEEG, N=29; right STG dominance, anterior-posterior organization)
9. **Thaut, M. H., et al. (2015)**. Neurobiological foundations of neurologic music therapy: rhythmic entrainment and the motor system. *Frontiers in Neuroscience*. (Review; rhythmic entrainment and motor system)
10. **Ross, J. M. & Balasubramaniam, R. (2022)**. Time perception for musical rhythms: Sensorimotor perspectives on entrainment, simulation, and prediction. (Review; 3 sensorimotor mechanisms)
11. **Harrison, E. C., et al. (2025)**. Neural mechanisms underlying synchronization of movement to musical cues in Parkinson disease and aging. (fMRI; sensorimotor + temporal + SMA + putamen during music-cued tapping)
12. **Barchet, S., et al. (2024)**. Auditory-motor synchronization and perception suggest partially distinct time scales in speech and music. (Behavioral; effector-specific rate preferences for auditory-motor coupling)

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D): L0, L4, L5, L6, L7, X_L0L4, X_L4L5 | R³ (49D): Energy, Timbre, Change, Interactions |
| Intensity signal | S⁰.L0.amplitude[2] + HC⁰.OSC | R³.amplitude[7] |
| Motor coupling | S⁰.L7.crossband × HC⁰.NPL | R³.x_l0l5[25:33] |
| Gamma proxy | S⁰.L7[80:104] (crossband ratios) | R³.tonalness[14] + beat-entrainment features |
| Onset detection | S⁰.L5.attack_time[50] × HC⁰.ITM | R³.onset_strength[11] |
| Groove | S⁰.L5 × HC⁰.GRV | R³.Change |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 30/2304 = 1.30% | 16/2304 = 0.69% |

---

**Model Status**: ✅ **VALIDATED** (v2.1.0: 1→12 papers, Lazzari TMS CAUSAL evidence, Ito cross-species, Grahn/Hoddinott SMA+putamen)
**Output Dimensions**: **12D**
**Evidence Tier**: **α (Mechanistic)** — strengthened by TMS causal evidence and cross-species replication
**Confidence**: **>90%** — right dPMC role causally confirmed; 110ms delay remains single-study (Potes 2012)
**Code note**: Layer E dimension names differ between doc (4D: auditory_gamma, motor_gamma, coupling_delay, intensity_corr) and code (3D: gamma_coupling, motor_lag, dorsal_stream) — reconcile in Phase 5
