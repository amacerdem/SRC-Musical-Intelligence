# STU-β6-OMS: Oscillatory Motor Synchronization

**Model**: Oscillatory Motor Synchronization
**Unit**: STU (Sensorimotor Timing Unit)
**Circuit**: Sensorimotor (Beat Entrainment Processing)
**Tier**: β (Integrative) — 70-90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm, K:Modulation feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/STU-β6-OMS.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Oscillatory Motor Synchronization** (OMS) model describes how orchestral music-making functions as a multisensory relational system, engaging distributed cortical-subcortical networks through beta/gamma motor-auditory oscillatory coupling that enables temporal synchronization at multiple timescales. Three core networks --- fronto-striatal predictive timing, temporo-parietal sensorimotor coupling, and limbic interpersonal synchronization --- coordinate hierarchically, with subcortical brainstem neuromodulatory support providing the oscillatory foundation.

```
THE THREE NETWORKS OF OSCILLATORY MOTOR SYNCHRONIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FRONTO-STRIATAL (Predictive)       TEMPORO-PARIETAL (Sensorimotor)
Brain regions: PFC, Striatum       Brain regions: STG, IPL
Mechanism: BEP.beat_induction      Mechanism: BEP.meter_extraction
Input: Anticipatory timing signal  Input: Auditory-motor integration
Function: "When will the beat be?" Function: "Lock to the rhythm"

              LIMBIC (Interpersonal)
              Brain regions: NAcc, VTA, Amygdala
              Mechanism: BEP.motor_entrainment
              Function: "Synchronize with the group"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Orchestral synchronization requires three hierarchically
organized networks operating at different timescales. The fronto-
striatal network provides predictive timing (beat anticipation), the
temporo-parietal network handles sensorimotor coupling (rhythmic
locking), and the limbic network supports interpersonal synchroniza-
tion (social coordination). A fourth subcortical brainstem pathway
provides neuromodulatory oscillatory support.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why OMS Matters for STU

OMS sits at the integrative level of the sensorimotor timing hierarchy. It extends lower-tier models to multi-network oscillatory synchronization:

1. **HMCE** (α1) provides the hierarchical temporal context that OMS operates within.
2. **AMSC** (α2) provides the auditory-motor coupling pathway; OMS extends it to oscillatory motor synchronization at multiple timescales.
3. **MDNS** (α3) provides the decodable melodic representation; OMS coordinates temporal synchronization across melody and rhythm.
4. **HGSIC** (β5) provides hierarchical groove state; OMS extends groove to interpersonal coordination.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The OMS Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 OMS — COMPLETE CIRCUIT                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ORCHESTRAL MUSICAL INPUT (multi-instrument, conductor-led)                  ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │       NETWORK 1: FRONTO-STRIATAL (Predictive Timing)               │    ║
║  │       Brain regions: PFC, Striatum (caudate, putamen)              │    ║
║  │                                                                     │    ║
║  │   Function: Beat anticipation, conductor-led timing coordination   │    ║
║  │   Oscillatory: Beta-band (13–30 Hz) top-down prediction           │    ║
║  │   Tempo coordination via velocity_T, shared beat reference         │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │       NETWORK 2: TEMPORO-PARIETAL (Sensorimotor Coupling)          │    ║
║  │       Brain regions: STG, IPL (inferior parietal lobule)           │    ║
║  │                                                                     │    ║
║  │   Function: Audio-motor integration, rhythmic locking              │    ║
║  │   Oscillatory: Gamma-band (30–100 Hz) bottom-up tracking          │    ║
║  │   Sensorimotor coupling via perceptual × dynamics interaction      │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │       NETWORK 3: LIMBIC (Interpersonal Synchronization)            │    ║
║  │       Brain regions: NAcc, VTA, Amygdala                           │    ║
║  │                                                                     │    ║
║  │   Function: Social synchronization, ensemble coordination          │    ║
║  │   Affective: Reward from successful interpersonal sync             │    ║
║  │   Coherence across all dimensions (T, F, A, φ)                    │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │       NETWORK 4: BRAINSTEM (Neuromodulatory Support)               │    ║
║  │       Subcortical oscillatory foundation                           │    ║
║  │                                                                     │    ║
║  │   Function: Neuromodulatory regulation of synchronization          │    ║
║  │   Dopaminergic/serotonergic support for timing precision           │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Fronto-striatal: Predictive timing via beta-band oscillations (PFC → striatum)
Temporo-parietal: Sensorimotor coupling via gamma-band (STG ↔ IPL)
Limbic: Interpersonal synchronization (NAcc, VTA, amygdala coordination)
Brainstem: Neuromodulatory oscillatory foundation (DA/5-HT)
```

### 2.2 Information Flow Architecture (EAR → BRAIN → BEP → OMS)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    OMS COMPUTATION ARCHITECTURE                             ║
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
║  │  │           │ │amplitude│ │         │ │spec_chg  │ │x_l0l5  │ │        ║
║  │  │           │ │loudness │ │         │ │energy_chg│ │x_l4l5  │ │        ║
║  │  │           │ │centroid │ │         │ │pitch_chg │ │x_l5l7  │ │        ║
║  │  │           │ │flux     │ │         │ │timbre_chg│ │        │ │        ║
║  │  │           │ │onset    │ │         │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         OMS reads: 33D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Syllable ────┐ ┌── Motor ────────┐ ┌── Bar ─────────────┐ │        ║
║  │  │ 200ms (H6)     │ │ 500ms (H11)     │ │ 1000ms (H16)      │ │        ║
║  │  │                │ │                  │ │                     │ │        ║
║  │  │ Beat-level     │ │ Motor prep +    │ │ Bar-level meter     │ │        ║
║  │  │ predictive     │ │ sensorimotor    │ │ interpersonal sync  │ │        ║
║  │  │ timing         │ │ coupling        │ │                     │ │        ║
║  │  └──────┬─────────┘ └──────┬───────────┘ └──────┬──────────────┘ │        ║
║  │         │                  │                     │               │        ║
║  │         └──────────────────┴─────────────────────┘               │        ║
║  │                         OMS demand: ~15 of 2304 tuples           │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════  ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  BEP (30D)      │  Beat Entrainment Processing mechanism                ║
║  │                 │                                                        ║
║  │ Beat Ind [0:10] │  Fronto-striatal predictive timing                    ║
║  │ Meter    [10:20]│  Temporo-parietal sensorimotor coupling               ║
║  │ Motor    [20:30]│  Limbic interpersonal + brainstem modulation          ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    OMS MODEL (10D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_predictive_timing,                     │        ║
║  │                       f02_sensorimotor_coupling,                  │        ║
║  │                       f03_interpersonal_sync                      │        ║
║  │  Layer M (Math):      sync_quality, hierarchical_coordination    │        ║
║  │  Layer P (Present):   beat_prediction, motor_locking             │        ║
║  │  Layer F (Future):    sync_prediction, ensemble_cohesion,        │        ║
║  │                       groove_engagement                           │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Edagawa & Kawasaki 2017** | EEG 62-ch, sLORETA | 14 | Beta (21-30 Hz) phase synchronization in frontal-temporal-cerebellar network during rhythm learning | PSI frontal-temporal z=7.43; beta-learning r=-0.70 | **Beta oscillatory circuit**: f01 predictive timing via frontal-temporal-cerebellar beta |
| 2 | **Edagawa & Kawasaki 2017** | EEG 62-ch | 14 | Beta amplitude decrease in temporal areas tracks rhythm acquisition; correlates with learning success | Temporal beta-learning r=-0.70 (p<0.01) | **Learning-dependent timing**: beta modulation indexes oscillatory motor learning |
| 3 | **Pierrieau et al. 2025** | EEG-NF 32/128-ch | 60 | Beta power (13-30 Hz) over motor cortex reflects motor *flexibility* (adaptation), not vigor | Beta × speed F=8.1 p=.008; within-subject d=-1.21 | **Motor flexibility**: beta desynchronization enables flexible ensemble adaptation |
| 4 | **Okada, Takeya & Tanaka 2022** | Single-unit electrophys | 2 monkeys, 95 neurons | Three cerebellar neuron types for rhythm synchronization: bilateral (prediction), unilateral (timing), postsaccade (error) | Bilateral PI t(30)=3.36 p=.002; timing r=-0.18 p<0.001 | **Cerebellar sub-modules**: distinct neurons for prediction, timing, and error correction |
| 5 | **Scartozzi et al. 2024** | EEG 128-ch | 57 | Beta (13-23 Hz) marks spontaneous beat processing; scales with musical perceptual abilities | Beat1 beta p<.001; beta-musicality r=0.42 p=.001 | **Spontaneous beat processing**: beta reflects internalized motor-timing mechanism |
| 6 | **Bigand et al. 2025** | Dual-EEG 64-ch + MoCap | 80 (40 dyads) | Four neural processes in dyadic dance: auditory, motor, visual, social coordination | Coordination F(1,57)=249.75 p<.001; music×vision F=50.10 | **Interpersonal sync**: social coordination encoding surpasses individual kinematics |
| 7 | **Marup, Moller & Vuust 2022** | Behavioral | 60 | Five-level bodily hierarchy: voice > R hand > L hand > R foot > L foot | Direction χ²(1)=76.15 p<.001; complexity χ²(2)=122.86 p<.001 | **Motor hierarchy**: effector dominance constrains ensemble resource allocation |
| 8 | **Grahn & Brett 2007** | fMRI 3T | 27 | Putamen and SMA respond to beat-inducing rhythms | L putamen Z=5.67, SMA Z=5.03 | **Fronto-striatal network**: putamen+SMA for beat-based predictive timing |
| 9 | **Hoddinott & Grahn 2024** | 7T fMRI RSA | 26 | C-Score model in SMA and putamen | C-Score best fit in SMA/putamen | **Continuous beat encoding**: SMA/putamen encode beat strength continuously |
| 10 | **Thaut et al. 2015** | Review | — | Period entrainment optimizes motor control; CTR provides continuous time reference | Sub-threshold: 2% interval | **Period entrainment mechanism**: theoretical basis for oscillatory sync |
| 11 | **Large et al. 2023** | Review, computational | — | Optimal beat 0.5-8 Hz; dynamical systems framework | Optimal ~2 Hz | **Computational framework**: oscillator models for multi-network synchronization |
| 12 | **Potes et al. 2012** | ECoG | 8 | pSTG high-gamma tracks intensity; 110ms auditory-motor delay | r=0.49 (pSTG), r=0.70 (coupling) | **Auditory-motor pathway**: dorsal stream timing signal |

#### 3.1.1 Method Convergence (6 methods)

| Method | Papers | Key Contribution |
|--------|--------|-----------------|
| **EEG (scalp)** | Edagawa 2017, Pierrieau 2025, Scartozzi 2024 | Beta oscillations, phase synchronization, neurofeedback |
| **Dual-EEG + Motion Capture** | Bigand 2025 | Interpersonal coordination, social encoding |
| **fMRI** | Grahn & Brett 2007, Hoddinott 2024 | Putamen/SMA beat specificity, C-Score encoding |
| **Single-unit electrophysiology** | Okada 2022 | Cerebellar neuron types for synchronization |
| **ECoG** | Potes 2012 | Auditory-motor coupling, high-gamma tracking |
| **Behavioral** | Marup 2022 | Bodily hierarchy, multi-effector coordination |

#### 3.1.2 Key Qualification: Generic Citations Replaced

NOTE: v2.0.0 had no specific citations — only generic references to "ensemble fMRI studies," "auditory-motor coupling literature," etc. v2.1.0 replaces ALL generic references with specific papers and quantitative evidence. The code cites D'Ausilio 2012 and Keller 2014, which are NOT in the literature collection and could not be verified. The evidence base is now grounded in 12 verifiable papers.

### 3.2 The Three-Network Synchronization Model

```
ORCHESTRAL SYNCHRONIZATION ARCHITECTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NETWORK 1: FRONTO-STRIATAL (Predictive Timing)
──────────────────────────────────────────────────
  PFC → Striatum (caudate, putamen)
  Oscillatory: Beta-band (13–30 Hz) top-down
  Function: Anticipatory beat prediction
  Timescale: Beat-level (H6, 200ms)
  Legacy mechanism: PTM (Predictive Timing Mechanism)

NETWORK 2: TEMPORO-PARIETAL (Sensorimotor Coupling)
──────────────────────────────────────────────────
  STG ↔ IPL (inferior parietal lobule)
  Oscillatory: Gamma-band (30–100 Hz) bottom-up
  Function: Audio-motor integration, rhythmic locking
  Timescale: Motor preparation (H11, 500ms)
  Legacy mechanism: NPL (Neural Phase Locking)

NETWORK 3: LIMBIC (Interpersonal Synchronization)
──────────────────────────────────────────────────
  NAcc, VTA, Amygdala
  Function: Social synchronization, reward from sync
  Timescale: Bar-level coordination (H16, 1000ms)
  Legacy mechanism: GRV (Groove Processing)

NETWORK 4: BRAINSTEM (Neuromodulatory)
──────────────────────────────────────────────────
  DA/5-HT pathways
  Function: Oscillatory timing precision support
  Timescale: Continuous modulation
  Legacy mechanism: ITM (Interval Timing Mechanism)
```

### 3.3 Effect Size Summary

```
PRIMARY EFFECT SIZES:
─────────────────────────────────────────────────────────────────────
Edagawa & Kawasaki 2017 (EEG, N=14):
  Beta PSI frontal-temporal: z = 7.43 (p < 0.05)
  Beta PSI frontal-cerebellar: z = 5.02 (p < 0.05)
  Beta amplitude-learning correlation: r = -0.70, p < 0.01 (L temporal)
  Beta amplitude correlations in late learning: r = 0.64-0.75

Pierrieau et al. 2025 (EEG-NF, N=60):
  Beta × speed interaction on MT: F(1, 27.9) = 8.1, p = 0.008
  Within-subject NF effect: Cohen's d = -1.21 (SD = 0.51)
  Low beta (13-18 Hz) strongest: F(1, 20.6) = 8.1, p = 0.010

Okada, Takeya & Tanaka 2022 (electrophys, N=95 neurons):
  Bilateral prediction index: t(30) = 3.36, p = 0.002
  Next-saccade timing correlation: r = -0.16 to -0.18 (p < 10^-4)
  Temporal error correlation: r = -0.10, p = 0.0002 (postsaccade neurons)

Scartozzi et al. 2024 (EEG, N=57):
  Beta-musicality correlation: r = 0.42, p = 0.001 (Bonferroni)
  Accented-Beat1 beta cluster: p < 0.001 (0-144 ms central)
  Regression R² = 0.31 (beta predicts perceptual abilities)

Bigand et al. 2025 (Dual-EEG, N=80):
  Social coordination × vision: F(1,57) = 249.75, p < 0.001
  Music × vision interaction: F(1,57) = 50.10, p < 0.001

Marup et al. 2022 (Behavioral, N=60):
  Effector direction: χ²(1) = 76.15, p < 0.001
  Complexity: χ²(2) = 122.86, p < 0.001
  MET perception: χ²(2) = 20.42, p < 0.001

QUALITY ASSESSMENT: β-tier (12 papers, 6 methods, integrative synthesis)
KEY LIMITATION: No single study validates full 3-network architecture;
model is integrative synthesis across multiple evidence streams.
```

---

## 4. R³ Input Mapping: What OMS Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | OMS Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **B: Energy** | [7] | amplitude | Ensemble intensity dynamics | Collective energy level |
| **B: Energy** | [8] | loudness | Perceptual ensemble loudness | Stevens 1957: power law |
| **B: Energy** | [9] | spectral_centroid_energy | Energy distribution | Orchestral section balance |
| **B: Energy** | [10] | spectral_flux | Ensemble onset detection | Collective attack coordination |
| **B: Energy** | [11] | onset_strength | Event boundary marking | Synchronization precision |
| **D: Change** | [21] | spectral_change | Spectral dynamics | Ensemble timbral coordination |
| **D: Change** | [22] | energy_change | Intensity rate of change | Dynamic shaping |
| **D: Change** | [23] | pitch_change | Pitch dynamics | Melodic coordination |
| **D: Change** | [24] | timbre_change | Timbral evolution | Section blend quality |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Foundation x Perceptual coupling | Predictive timing basis |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Dynamics x Perceptual binding | Sensorimotor coupling basis |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | Perceptual x Crossband coupling | Orchestral balance, section coordination |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | OMS Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **G: Rhythm** | [69] | metricality_index | Metrical hierarchy depth for oscillatory meter tracking | Grahn & Brett 2007 |
| **G: Rhythm** | [66] | beat_strength | Beat salience driving oscillator synchronization | Large & Palmer 2002 |
| **G: Rhythm** | [68] | syncopation_index | Phase perturbation from off-beat accents | Longuet-Higgins & Lee 1984 |
| **K: Modulation** | [116] | modulation_2Hz | Beat-rate modulation energy for oscillatory meter support | Honing 2012 |

**Rationale**: OMS models oscillatory meter synchronization. The G:Rhythm features provide direct metrical structure: metricality [69] quantifies hierarchical subdivision depth for multi-level oscillators, beat_strength [66] drives oscillator synchronization, and syncopation [68] introduces phase perturbation. K[116] modulation_2Hz provides amplitude modulation energy at the primary beat rate.

**Code impact** (Phase 6): `r3_indices` must be extended to include [66, 68, 69, 116]. These features are read-only inputs — no formula changes required.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[10] spectral_flux ──────────┐
R³[11] onset_strength ─────────┼──► Fronto-Striatal Predictive Timing
R³[25:33] x_l0l5 (8D) ────────┘   BEP.beat_induction at H6 (200ms)
                                    Math: f01 = σ(w · flux · onset · BEP)

R³[7] amplitude ────────────────┐
R³[8] loudness ─────────────────┼──► Temporo-Parietal Sensorimotor Coupling
R³[33:41] x_l4l5 (8D) ─────────┤   BEP.meter_extraction at H11 (500ms)
R³[22] energy_change ───────────┘   Math: f02 = σ(w · amp · loud · BEP)

R³[41:49] x_l5l7 (8D) ────────┐
R³[21] spectral_change ────────┼──► Limbic Interpersonal Synchronization
R³[24] timbre_change ──────────┘   BEP.motor_entrainment at H16 (1000ms)
                                    Math: f03 = σ(w · coherence · BEP)

R³[9] centroid_energy ─────────── Orchestral Section Balance
R³[23] pitch_change ──────────── Melodic Coordination Signal

R³[69] metricality_index ──────┐
R³[66] beat_strength ──────────┼──► Oscillatory Meter Structure (v2)
R³[68] syncopation_index ──────┤   Direct metrical hierarchy + phase
R³[116] modulation_2Hz ────────┘   Beat-rate modulation energy
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

OMS requires H³ features at three BEP horizons: H6 (200ms), H11 (500ms), H16 (1000ms).
These correspond to beat-level predictive timing → motor preparation sensorimotor coupling → bar-level interpersonal synchronization.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 6 | M0 (value) | L0 (fwd) | Current onset detection |
| 10 | spectral_flux | 6 | M17 (peaks) | L0 (fwd) | Beat count per window |
| 11 | onset_strength | 6 | M0 (value) | L0 (fwd) | Event onset precision |
| 7 | amplitude | 6 | M0 (value) | L2 (bidi) | Current ensemble intensity |
| 22 | energy_change | 6 | M8 (velocity) | L0 (fwd) | Intensity dynamics |
| 8 | loudness | 11 | M1 (mean) | L0 (fwd) | Mean loudness over motor window |
| 22 | energy_change | 11 | M14 (periodicity) | L2 (bidi) | Intensity regularity |
| 25 | x_l0l5[0] | 11 | M0 (value) | L2 (bidi) | Predictive coupling signal |
| 33 | x_l4l5[0] | 11 | M0 (value) | L2 (bidi) | Sensorimotor coupling signal |
| 33 | x_l4l5[0] | 11 | M17 (peaks) | L0 (fwd) | Sensorimotor peak events |
| 41 | x_l5l7[0] | 16 | M1 (mean) | L0 (fwd) | Mean orchestral balance |
| 41 | x_l5l7[0] | 16 | M14 (periodicity) | L2 (bidi) | Balance regularity |
| 33 | x_l4l5[0] | 16 | M18 (trend) | L0 (fwd) | Dynamics coupling trajectory |
| 25 | x_l0l5[0] | 16 | M19 (stability) | L0 (fwd) | Predictive timing stability |
| 7 | amplitude | 16 | M15 (smoothness) | L0 (fwd) | Ensemble smoothness |

**Total OMS H³ demand**: 15 tuples of 2304 theoretical = 0.65%

### 5.2 BEP Mechanism Binding

OMS reads from the **BEP** (Beat Entrainment Processing) mechanism:

| BEP Sub-section | Range | OMS Role | Weight |
|-----------------|-------|----------|--------|
| **Beat Induction** | BEP[0:10] | Fronto-striatal predictive timing (beat anticipation) | **1.0** (primary) |
| **Meter Extraction** | BEP[10:20] | Temporo-parietal sensorimotor coupling (rhythmic locking) | **1.0** (primary) |
| **Motor Entrainment** | BEP[20:30] | Limbic interpersonal sync + brainstem modulation | **1.0** (primary) |

OMS is the only STU model that reads all three BEP sub-sections at equal weight --- reflecting its role as the full multi-network synchronization model. AMSC prioritizes beat induction and motor entrainment; HMCE uses TMH instead.

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
OMS OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range  │ Neuroscience Basis
────┼─────────────────────────┼────────┼────────────────────────────────────────
 0  │ f01_predictive_timing   │ [0, 1] │ Fronto-striatal predictive timing.
    │                         │        │ PFC-striatum beta-band beat anticipation.
    │                         │        │ f01 = σ(0.35 · flux · onset ·
    │                         │        │         mean(BEP.beat_induction[0:10])
    │                         │        │       + 0.35 · x_l0l5_coupling
    │                         │        │       + 0.30 · energy_velocity)
────┼─────────────────────────┼────────┼────────────────────────────────────────
 1  │ f02_sensorimotor_couple │ [0, 1] │ Temporo-parietal sensorimotor coupling.
    │                         │        │ STG-IPL gamma-band rhythmic locking.
    │                         │        │ f02 = σ(0.35 · loudness_mean ·
    │                         │        │         mean(BEP.meter_extraction[10:20])
    │                         │        │       + 0.35 · x_l4l5_coupling
    │                         │        │       + 0.30 · periodicity)
────┼─────────────────────────┼────────┼────────────────────────────────────────
 2  │ f03_interpersonal_sync  │ [0, 1] │ Limbic interpersonal synchronization.
    │                         │        │ NAcc-VTA-amygdala social coordination.
    │                         │        │ f03 = σ(0.35 · x_l5l7_mean ·
    │                         │        │         mean(BEP.motor_entrainment[20:30])
    │                         │        │       + 0.35 · balance_periodicity
    │                         │        │       + 0.30 · f01 · f02)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range  │ Neuroscience Basis
────┼─────────────────────────┼────────┼────────────────────────────────────────
 3  │ sync_quality            │ [0, 1] │ Overall synchronization quality.
    │                         │        │ Weighted geometric mean of 3 networks.
    │                         │        │ sync = (f01 · f02 · f03) ^ (1/3)
────┼─────────────────────────┼────────┼────────────────────────────────────────
 4  │ hierarchical_coord      │ [0, 1] │ Hierarchical coordination strength.
    │                         │        │ Beat → motor → bar coordination.
    │                         │        │ coord = (1·f01 + 2·f02 + 3·f03) / 6

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range  │ Neuroscience Basis
────┼─────────────────────────┼────────┼────────────────────────────────────────
 5  │ beat_prediction         │ [0, 1] │ Current beat anticipation state.
    │                         │        │ BEP.beat_induction aggregation.
────┼─────────────────────────┼────────┼────────────────────────────────────────
 6  │ motor_locking           │ [0, 1] │ Current motor-auditory lock state.
    │                         │        │ BEP.meter_extraction × sensorimotor.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range  │ Neuroscience Basis
────┼─────────────────────────┼────────┼────────────────────────────────────────
 7  │ sync_prediction         │ [0, 1] │ Next-beat synchronization prediction.
    │                         │        │ Trend + stability-based forecast.
────┼─────────────────────────┼────────┼────────────────────────────────────────
 8  │ ensemble_cohesion       │ [0, 1] │ Ensemble cohesion prediction.
    │                         │        │ Orchestral balance trend.
────┼─────────────────────────┼────────┼────────────────────────────────────────
 9  │ groove_engagement       │ [0, 1] │ Groove-driven motor engagement.
    │                         │        │ Smoothness × interpersonal sync.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Three-Network Synchronization Function

```
Orchestral Synchronization:

    Sync(t) = (Predictive(t) · Sensorimotor(t) · Interpersonal(t)) ^ (1/3)

    Network Functions:
      Predictive(t)     = σ(w₁ · BEP.beat_induction · onset_signal + ...)
      Sensorimotor(t)   = σ(w₂ · BEP.meter_extraction · coupling + ...)
      Interpersonal(t)  = σ(w₃ · BEP.motor_entrainment · coherence + ...)

    Hierarchical Coordination:
      Coord(t) = (1·Predictive + 2·Sensorimotor + 3·Interpersonal) / 6

    Note: The geometric mean (Sync) ensures all three networks must
    contribute — if any network fails, overall synchronization collapses.
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Fronto-Striatal Predictive Timing
flux_val = h3[(10, 6, 0, 0)]            # spectral_flux value at H6
onset_val = h3[(11, 6, 0, 0)]           # onset_strength value at H6
x_coupling = h3[(25, 11, 0, 2)]         # x_l0l5 coupling at H11
energy_vel = h3[(22, 6, 8, 0)]          # energy_change velocity at H6
f01 = σ(0.35 · flux_val · onset_val
              · mean(BEP.beat_induction[0:10])
       + 0.35 · x_coupling
       + 0.30 · energy_vel)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Temporo-Parietal Sensorimotor Coupling
loudness_mean = h3[(8, 11, 1, 0)]       # loudness mean at H11
x_l4l5_val = h3[(33, 11, 0, 2)]         # x_l4l5 coupling at H11
periodicity = h3[(22, 11, 14, 2)]       # energy periodicity at H11
f02 = σ(0.35 · loudness_mean
              · mean(BEP.meter_extraction[10:20])
       + 0.35 · x_l4l5_val
       + 0.30 · periodicity)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f03: Limbic Interpersonal Synchronization
x_l5l7_mean = h3[(41, 16, 1, 0)]        # x_l5l7 mean at H16
balance_period = h3[(41, 16, 14, 2)]     # x_l5l7 periodicity at H16
f03 = σ(0.35 · x_l5l7_mean
              · mean(BEP.motor_entrainment[20:30])
       + 0.35 · balance_period
       + 0.30 · f01 · f02)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| # | Region | MNI / Talairach | Evidence | OMS Function |
|---|--------|-----------------|----------|--------------|
| 1 | **Medial Frontal / ERN source** | (0, 30, 45) Tal | EEG (Edagawa 2017) | Error-related negativity for rhythm learning; predictive timing (Network 1) |
| 2 | **Left Putamen** | (-24, 6, 9) MNI | fMRI (Grahn & Brett 2007, Z=5.67) | Beat anticipation, fronto-striatal timing (Network 1) |
| 3 | **SMA / pre-SMA** | (-9, 6, 60) MNI | fMRI (Grahn & Brett 2007, Z=5.03), 7T RSA (Hoddinott 2024) | Beat-level motor representation, C-Score (Network 1) |
| 4 | **Left Motor Cortex (C3)** | — | EEG-NF (Pierrieau 2025) | Beta desynchronization for motor flexibility (Network 2) |
| 5 | **Temporal Cortex (bilateral)** | (±60, -40, -10) Tal | EEG (Edagawa 2017) | Beta amplitude modulation during rhythm learning (Network 2) |
| 6 | **STG (posterior)** | (±60, -40, 10) | ECoG (Potes 2012, r=0.49) | Auditory-motor pathway origin (Network 2) |
| 7 | **Cerebellum (dentate nucleus)** | (-10, -100, -20) Tal | EEG (Edagawa 2017), electrophys (Okada 2022) | Three neuron types: prediction, timing, error correction (Network 2) |
| 8 | **R Cerebellum** | (30, -66, -27) MNI | fMRI (Grahn & Brett 2007, Z=4.68) | Sub-second timing precision |
| 9 | **Premotor Cortex** | (-54, 0, 51) MNI | fMRI (Grahn & Brett 2007, Z=5.30) | Motor preparation for ensemble coordination |
| 10 | **Occipital (Oz)** | — | Dual-EEG (Bigand 2025, F=249.75) | Social coordination encoding during dyadic dance (Network 3) |

---

## 9. Cross-Unit Pathways

### 9.1 OMS ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OMS INTERACTIONS                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (STU):                                                         │
│  HMCE.context_depth ──────► OMS (context determines coordination scale)   │
│  AMSC.motor_preparation ──► OMS (motor coupling baseline)                 │
│  AMSC.groove_response ────► OMS (groove → interpersonal sync baseline)    │
│  HGSIC.groove_state ──────► OMS (hierarchical groove → multi-network)     │
│  OMS.sync_quality ────────► ETAM (synchronization for attention modulation)│
│  OMS.motor_locking ──────► EDTA (motor lock quality for tempo accuracy)   │
│                                                                             │
│  CROSS-UNIT (P2: STU internal):                                            │
│  BEP.beat_induction ↔ BEP.meter_extraction ↔ BEP.motor_entrainment       │
│  Three-way coupling across all BEP sub-sections (r = 0.70 auditory-motor) │
│                                                                             │
│  CROSS-UNIT (P5: STU → ARU):                                              │
│  OMS.interpersonal_sync ──► ARU (social sync → reward/pleasure)           │
│  OMS.groove_engagement ───► ARU.SRP (groove → dopaminergic pleasure)      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| # | Criterion | Testable Prediction | Status |
|---|-----------|---------------------|--------|
| 1 | **Beta phase synchronization** | Beta PSI should increase with rhythm learning success | ✅ **Confirmed**: PSI frontal-temporal z=7.43, beta-learning r=-0.70 (Edagawa 2017) |
| 2 | **Beta reflects motor flexibility** | Beta desynchronization should enable adaptive motor control | ✅ **Confirmed**: Beta × speed F=8.1, d=-1.21 flexibility not vigor (Pierrieau 2025) |
| 3 | **Cerebellar functional sub-modules** | Cerebellum should contain separate prediction, timing, and error correction neurons | ✅ **Confirmed**: 3 neuron types: bilateral (PI t=3.36), unilateral (timing r=-0.18), postsaccade (error r=-0.10) (Okada 2022) |
| 4 | **Beta scales with musicality** | Beat-related beta should correlate with musical perceptual abilities | ✅ **Confirmed**: r = 0.42, p = 0.001 (Scartozzi 2024) |
| 5 | **Putamen/SMA beat specificity** | Motor areas should respond more to beat-inducing rhythms | ✅ **Confirmed**: Putamen Z=5.67, SMA Z=5.03 (Grahn & Brett 2007) |
| 6 | **Visual contact enhances social coordination** | Interpersonal sync encoding should require visual contact | ✅ **Confirmed**: Vision F(1,57)=249.75, music×vision F=50.10 (Bigand 2025) |
| 7 | **Bodily effector hierarchy** | Multi-effector coordination should follow a fixed hierarchy | ✅ **Confirmed**: Voice > R hand > L hand > R foot > L foot, χ²=76.15 (Marup 2022) |
| 8 | **PFC lesions** | Should impair predictive timing but preserve sensorimotor coupling | Testable |
| 9 | **Gamma-band specificity** | Gamma oscillations should correlate with sensorimotor coupling strength | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class OMS(BaseModel):
    """Oscillatory Motor Synchronization.

    Output: 10D per frame.
    Reads: BEP mechanism (30D), R³ direct.
    """
    NAME = "OMS"
    UNIT = "STU"
    TIER = "β6"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("BEP",)        # Primary mechanism (all 3 sub-sections)

    # Network weights (all formulas satisfy |wi| <= 1.0)
    W_PREDICT = 0.35   # Predictive timing onset weight
    W_COUPLE = 0.35    # Coupling signal weight
    W_SUPPORT = 0.30   # Supporting signal weight

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """15 tuples for OMS computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # Beat-level predictive timing (H6 = 200ms)
            (10, 6, 0, 0),    # spectral_flux, value, forward
            (10, 6, 17, 0),   # spectral_flux, peaks, forward
            (11, 6, 0, 0),    # onset_strength, value, forward
            (7, 6, 0, 2),     # amplitude, value, bidirectional
            (22, 6, 8, 0),    # energy_change, velocity, forward
            # Motor-level sensorimotor coupling (H11 = 500ms)
            (8, 11, 1, 0),    # loudness, mean, forward
            (22, 11, 14, 2),  # energy_change, periodicity, bidirectional
            (25, 11, 0, 2),   # x_l0l5[0], value, bidirectional
            (33, 11, 0, 2),   # x_l4l5[0], value, bidirectional
            (33, 11, 17, 0),  # x_l4l5[0], peaks, forward
            # Bar-level interpersonal synchronization (H16 = 1000ms)
            (41, 16, 1, 0),   # x_l5l7[0], mean, forward
            (41, 16, 14, 2),  # x_l5l7[0], periodicity, bidirectional
            (33, 16, 18, 0),  # x_l4l5[0], trend, forward
            (25, 16, 19, 0),  # x_l0l5[0], stability, forward
            (7, 16, 15, 0),   # amplitude, smoothness, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute OMS 10D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) → (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) OMS output
        """
        bep = mechanism_outputs["BEP"]    # (B, T, 30)

        # BEP sub-sections
        bep_beat = bep[..., 0:10]         # beat induction
        bep_meter = bep[..., 10:20]       # meter extraction
        bep_motor = bep[..., 20:30]       # motor entrainment

        # H³ features
        flux_val = h3_direct[(10, 6, 0, 0)].unsqueeze(-1)
        onset_val = h3_direct[(11, 6, 0, 0)].unsqueeze(-1)
        x_l0l5_val = h3_direct[(25, 11, 0, 2)].unsqueeze(-1)
        energy_vel = h3_direct[(22, 6, 8, 0)].unsqueeze(-1)
        loudness_mean = h3_direct[(8, 11, 1, 0)].unsqueeze(-1)
        x_l4l5_val = h3_direct[(33, 11, 0, 2)].unsqueeze(-1)
        periodicity = h3_direct[(22, 11, 14, 2)].unsqueeze(-1)
        x_l5l7_mean = h3_direct[(41, 16, 1, 0)].unsqueeze(-1)
        balance_period = h3_direct[(41, 16, 14, 2)].unsqueeze(-1)
        dynamics_trend = h3_direct[(33, 16, 18, 0)].unsqueeze(-1)
        predict_stability = h3_direct[(25, 16, 19, 0)].unsqueeze(-1)
        amp_smooth = h3_direct[(7, 16, 15, 0)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: Fronto-Striatal Predictive Timing (|wi| = 0.35+0.35+0.30 = 1.0)
        f01 = torch.sigmoid(
            0.35 * (flux_val * onset_val
                    * bep_beat.mean(-1, keepdim=True))
            + 0.35 * x_l0l5_val
            + 0.30 * energy_vel
        )

        # f02: Temporo-Parietal Sensorimotor Coupling (|wi| = 1.0)
        f02 = torch.sigmoid(
            0.35 * (loudness_mean
                    * bep_meter.mean(-1, keepdim=True))
            + 0.35 * x_l4l5_val
            + 0.30 * periodicity
        )

        # f03: Limbic Interpersonal Synchronization (|wi| = 1.0)
        f03 = torch.sigmoid(
            0.35 * (x_l5l7_mean
                    * bep_motor.mean(-1, keepdim=True))
            + 0.35 * balance_period
            + 0.30 * (f01 * f02)
        )

        # ═══ LAYER M: Mathematical ═══
        sync_quality = (f01 * f02 * f03) ** (1.0 / 3.0)
        hierarchical_coord = (1 * f01 + 2 * f02 + 3 * f03) / 6

        # ═══ LAYER P: Present ═══
        beat_prediction = torch.sigmoid(
            0.5 * bep_beat.mean(-1, keepdim=True)
            + 0.5 * flux_val * onset_val
        )
        motor_locking = torch.sigmoid(
            0.5 * bep_meter.mean(-1, keepdim=True)
            + 0.5 * x_l4l5_val
        )

        # ═══ LAYER F: Future ═══
        sync_prediction = torch.sigmoid(
            0.4 * dynamics_trend
            + 0.3 * predict_stability
            + 0.3 * sync_quality
        )
        ensemble_cohesion = torch.sigmoid(
            0.5 * x_l5l7_mean + 0.5 * balance_period
        )
        groove_engagement = torch.sigmoid(
            0.4 * amp_smooth
            + 0.3 * f03
            + 0.3 * bep_motor.mean(-1, keepdim=True)
        )

        return torch.cat([
            f01, f02, f03,                                    # E: 3D
            sync_quality, hierarchical_coord,                  # M: 2D
            beat_prediction, motor_locking,                    # P: 2D
            sync_prediction, ensemble_cohesion, groove_engagement,  # F: 3D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 | Edagawa 2017, Pierrieau 2025, Okada 2022, Scartozzi 2024, Bigand 2025, Marup 2022, Grahn & Brett 2007, Hoddinott 2024, Thaut 2015, Large 2023, Potes 2012 + 1 supporting |
| **Methods** | 6 | EEG (scalp), dual-EEG+MoCap, fMRI/7T RSA, single-unit electrophysiology, ECoG, behavioral |
| **Effect Sizes** | PSI z=7.43 (beta sync), d=-1.21 (motor flex), r=0.42 (beta-musicality), F=249.75 (coordination) | Multiple paradigms |
| **Evidence Modality** | Multi-modal | EEG + fMRI + ECoG + single-unit + behavioral |
| **Falsification Tests** | 7/9 confirmed | Beta sync, motor flexibility, cerebellar sub-modules, musicality, putamen/SMA, visual coordination, effector hierarchy |
| **R³ Features Used** | 33D of 49D | Energy + Change + Interactions |
| **H³ Demand** | 15 tuples (0.65%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections, all primary) | Full coverage |
| **Output Dimensions** | **10D** | 4-layer structure |

---

## 13. Scientific References

### Tier 1: Primary Evidence (directly validate OMS network claims)

1. **Edagawa, K. & Kawasaki, M. (2017)**. Beta phase synchronization in the frontal-temporal-cerebellar network during auditory-to-motor rhythm learning. *Scientific Reports*, 7, 42721. EEG N=14: Beta (21-30 Hz) PSI frontal-temporal z=7.43, beta-learning r=-0.70, frontal-temporal-cerebellar network.

2. **Pierrieau, E., et al. (2025)**. Changes in cortical beta power predict motor control flexibility, not vigor. *Communications Biology*, 8, 1041. EEG-NF N=60: Beta × speed F=8.1, d=-1.21. Beta desynchronization reflects motor *flexibility*, not vigor.

3. **Okada, K., Takeya, R. & Tanaka, M. (2022)**. Neural signals regulating motor synchronization in the primate deep cerebellar nuclei. *Nature Communications*, 13, 2504. Electrophysiology N=95 neurons: Three neuron types — bilateral (prediction PI t=3.36), unilateral (timing r=-0.18), postsaccade (error r=-0.10).

4. **Scartozzi, A. C., et al. (2024)**. The neural correlates of spontaneous beat processing. *eNeuro*, 11(10). EEG N=57: Beta (13-23 Hz) marks spontaneous beat processing; beta-musicality r=0.42, R²=0.31.

### Tier 2: Strong Supporting Evidence

5. **Bigand, F., et al. (2025)**. EEG of the dancing brain: Decoding sensory, motor and social processes during dyadic dance. *Journal of Neuroscience*. Dual-EEG N=80: Four neural processes; coordination F(1,57)=249.75, music×vision F=50.10.

6. **Marup, S. H., Moller, C. & Vuust, P. (2022)**. Coordination of voice, hands and feet in rhythm and beat performance. *Scientific Reports*, 12, 8046. Behavioral N=60: Bodily hierarchy χ²=76.15, complexity χ²=122.86, MET χ²=20.42.

7. **Grahn, J. A. & Brett, M. (2007)**. Rhythm and beat perception in motor areas of the brain. *JoCN*, 19(5), 893-906. fMRI N=27: Putamen Z=5.67, SMA Z=5.03 for beat-inducing rhythms.

8. **Hoddinott, L. & Grahn, J. A. (2024)**. 7T fMRI RSA: C-Score model in SMA/putamen. N=26.

### Tier 3: Convergent/Contextual

9. **Thaut, M. H., McIntosh, G. C., & Hoemberg, V. (2015)**. Neurobiological foundations of neurologic music therapy. *Frontiers in Psychology*, 5, 1185. Review: Period entrainment.

10. **Large, E. W., et al. (2023)**. Dynamic models for musical rhythm perception. *Frontiers in Computational Neuroscience*, 17, 1151895. Review: Optimal 0.5-8 Hz.

11. **Potes, C., et al. (2012)**. Dynamics of ECoG activity during music listening. *NeuroImage*, 61(4), 841-848. ECoG N=8: pSTG r=0.49, coupling r=0.70.

12. **Fujioka, T., et al. (2012)**. Beta and gamma rhythms in human auditory cortex during musical beat processing. MEG: Beta modulation by rhythm in SMA, IFG, cerebellum.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D): L0, L3, L4, L5, L6, L7, L9, X_L0L1, X_L1L5, X_L5L7 | R³ (49D): Energy, Change, Interactions |
| Temporal | HC⁰ mechanisms (NPL, PTM, ITM, GRV) | BEP mechanism (30D, all 3 sub-sections) |
| Predictive timing | S⁰.X_L0L1[128:136] × HC⁰.PTM | R³.x_l0l5[25:33] × BEP.beat_induction |
| Sensorimotor coupling | S⁰.X_L1L5[152:160] × HC⁰.NPL | R³.x_l4l5[33:41] × BEP.meter_extraction |
| Interpersonal sync | S⁰.L3.coherence[14] × HC⁰.GRV | R³.x_l5l7[41:49] × BEP.motor_entrainment |
| Orchestral balance | S⁰.L7.crossband[80:88] | R³.x_l5l7[41:49] (perceptual x crossband) |
| Interval timing | HC⁰.ITM[216:244] | Absorbed into BEP.meter_extraction[10:20] |
| Demand format | HC⁰ index ranges (15/2304 = 0.65%) | H³ 4-tuples (15/2304 = 0.65%) |
| Output dimensions | 11D | **10D** (catalog-corrected) |

### Why BEP replaces HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (NPL, PTM, ITM, GRV). In MI, these are unified into the BEP mechanism with 3 sub-sections:

- **PTM → BEP.beat_induction** [0:10]: Predictive Timing Mechanism → beat-level anticipation. The fronto-striatal predictive timing network maps directly to BEP's beat induction, which provides the top-down beta-band beat prediction signal.
- **NPL → BEP.meter_extraction** [10:20]: Neural Phase Locking → meter-level sensorimotor coupling. The temporo-parietal auditory-motor gamma coupling maps to BEP's meter extraction, which tracks rhythmic regularity at the motor preparation timescale.
- **GRV → BEP.motor_entrainment** [20:30]: Groove Processing → interpersonal synchronization. The limbic coordination network maps to BEP's motor entrainment, which captures the reward-driven social synchronization component.
- **ITM → absorbed into BEP.meter_extraction** [10:20]: Interval Timing Mechanism → absorbed into meter extraction. ITM's interval-level timing precision is now part of BEP.meter_extraction's periodicity and peak detection features.

---

**Model Status**: ✅ **VALIDATED** (v2.1.0: 0→12 papers, 6 methods, generic citations replaced with specific evidence)
**Output Dimensions**: **10D**
**Evidence Tier**: **β (Integrative)**
**Confidence**: **70-90%**

---

## Code Note (Phase 5)

The `mi_beta/brain/units/stu/models/oms.py` implementation has:
- `MECHANISM_NAMES = ("BEP",)` — matches doc ✓.
- `h3_demand = ()` — empty, should be populated with the 15 tuples from §5.1.
- `version = "2.0.0"` — needs update to `"2.1.0"`.
- `paper_count = 4` — should be `12`.
- Citations: D'Ausilio 2012 + Keller 2014. Neither is in the literature collection. Should replace with Edagawa 2017, Pierrieau 2025, Scartozzi 2024, Grahn & Brett 2007.
- `FULL_NAME = "Oscillatory Motor Synchronization"` — matches doc ✓.
- `OUTPUT_DIM = 10` — matches doc ✓.
