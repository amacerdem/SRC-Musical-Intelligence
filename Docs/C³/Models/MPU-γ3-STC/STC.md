# MPU-γ3-STC: Singing Training Connectivity

**Model**: Singing Training Connectivity
**Unit**: MPU (Motor Planning Unit)
**Circuit**: Sensorimotor (SMA, PMC, Cerebellum, Basal Ganglia)
**Tier**: γ (Integrative) — 50-70% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/MPU-γ3-STC.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Singing Training Connectivity** (STC) model proposes that singing training increases resting-state connectivity between insula and speech/respiratory sensorimotor areas, suggesting enhanced interoceptive-motor integration. Singing uniquely engages respiratory control, vocal production, and interoceptive monitoring in an integrated circuit.

```
SINGING TRAINING CONNECTIVITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

       INTEROCEPTIVE-MOTOR INTEGRATION
       ═════════════════════════════════

┌─────────────────┐          ┌─────────────────┐
│    INSULA       │          │  SPEECH/RESP    │
│ Interoceptive   │◄────────►│  SENSORIMOTOR   │
│ Monitoring      │          │  AREAS          │
│                 │          │                 │
│ Body awareness  │          │ Voice production│
│ Breath state    │          │ Breath control  │
│ Vocal effort    │          │ Articulation    │
└────────┬────────┘          └────────┬────────┘
         │                            │
         └────────────┬───────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────────┐
│              SINGING TRAINING EFFECT                              │
│                                                                  │
│   Pre-training:  Weak insula-sensorimotor connectivity           │
│   Post-training: Enhanced resting-state connectivity             │
│                                                                  │
│   MECHANISMS:                                                    │
│   ════════════                                                   │
│   Respiratory motor control (breath-phrase coupling)             │
│   Interoceptive awareness (vocal effort monitoring)              │
│   Voice-body integration (sensorimotor feedback)                 │
└──────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Singing training enhances the connection between
interoceptive monitoring (insula) and speech/respiratory motor
areas. This creates a lasting resting-state connectivity change,
suggesting neural plasticity in the interoceptive-motor circuit
that supports voice production and respiratory control.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why STC Matters for MPU

STC extends motor planning to vocal-respiratory integration in the Motor Planning Unit:

1. **PEOM/MSR** (α-tier) establish motor entrainment and training effects.
2. **SPMC** (β4) describes the core motor circuit.
3. **STC** (γ3) extends to singing-specific motor planning: interoceptive-motor integration for vocal production, respiratory control, and voice-body coupling through training-induced plasticity.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → BEP+TMH → STC)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    STC COMPUTATION ARCHITECTURE                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  AUDIO (44.1kHz waveform)                                                    ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌──────────────────┐                                                        ║
║  │ COCHLEA          │  128 mel bins x 172.27Hz frame rate                    ║
║  │ (Mel Spectrogram)│  hop = 256 samples, frame = 5.8ms                     ║
║  └────────┬─────────┘                                                        ║
║           │                                                                  ║
║  ═════════╪══════════════════════════ EAR ═══════════════════════════════    ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  SPECTRAL (R³): 49D per frame                                    │        ║
║  │                         STC reads: ~16D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                         STC demand: ~12 of 2304 tuples           │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════  ║
║                               │                                              ║
║                       ┌───────┴───────┐                                      ║
║                       ▼               ▼                                      ║
║  ┌─────────────────┐  ┌─────────────────┐                                   ║
║  │  BEP (30D)      │  │  TMH (30D)      │                                   ║
║  │                 │  │                 │                                    ║
║  │ Beat Entr[0:10] │  │ Short-term      │                                   ║
║  │ Motor Coup      │  │ Memory  [0:10]  │                                   ║
║  │         [10:20] │  │ Sequence        │                                   ║
║  │ Groove  [20:30] │  │ Integ  [10:20]  │                                   ║
║  │                 │  │ Hierarch        │                                   ║
║  │                 │  │ Struct  [20:30] │                                   ║
║  └────────┬────────┘  └────────┬────────┘                                   ║
║           │                    │                                              ║
║           └────────┬───────────┘                                             ║
║                    ▼                                                          ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    STC MODEL (11D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f28_interoceptive_coupling,                │        ║
║  │                       f29_respiratory_integration,                │        ║
║  │                       f30_speech_sensorimotor                     │        ║
║  │  Layer M (Math):      connectivity_strength, respiratory_index,  │        ║
║  │                       voice_body_coupling                         │        ║
║  │  Layer P (Present):   insula_activity, vocal_motor               │        ║
║  │  Layer F (Future):    connectivity_pred, respiratory_pred,       │        ║
║  │                       vocal_pred                                  │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Zamorano et al. 2023** (PRIMARY) | Resting-state fMRI, singers vs non-singers | ~25/group | Bilateral anterior insula connectivity ↑ with speech sensorimotor network; accumulated singing training predicts enhanced insula co-activation with sensorimotor areas (diaphragm, larynx), bilateral thalamus, left putamen | Connectivity increase reported (correlation with training hours) | **Primary**: f28 interoceptive coupling, f29 respiratory integration, f30 speech sensorimotor |
| **Kleber et al. 2013** (CAUSAL) | 3T fMRI + vocal-fold anesthesia, singers vs nonsingers | N=26 (14+12) | Right anterior insula dissociates expertise × anesthesia: decreased in singers, increased in nonsingers; connectivity with M1, S1, auditory cortex | **F=22.08** (Group×Condition, right AIC MNI: 48,0,−3); pitch deviation **t(728)=−4.8, p<.001**; Group **F(1,728)=106.63**; Cerebellum Lobule VI **t=−5.02** | Causal evidence for right AIC in vocal feedback integration; MNI coords for all brain regions |
| **Zarate & Zatorre 2008** | fMRI, pitch-shifted feedback during singing | N=31 | ACC + pSTS + anterior insula network for compensatory vocal control; experience-dependent activation differences | Singers > nonsingers in compensatory network activation | Vocal pitch regulation network supporting f30 speech sensorimotor |
| **Zarate & Zatorre 2010** | fMRI, voluntary/involuntary pitch regulation | Experienced singers | RCZa + pSTS + anterior insula functionally connected for compensation; singers less able to ignore 25-cent vs 200-cent shifts | Stimulus-modulated connectivity | Involuntary pitch correction supports automatic interoceptive-motor loop (f28) |
| **Tsunada, Wang & Eliades 2024** | Single-neuron electrophysiology, marmoset auditory cortex | 3,285 units, 5 monkeys | Dual vocal suppression: phasic (gating) and tonic (prediction); both present within individual neurons | Phrase-interval **r=0.46, p=8×10⁻¹⁸⁶**; pre-vocal→tonic **r=0.22, p=4×10⁻³⁷** | Mechanistic basis for vocal sensorimotor integration; dual process supports separate interoceptive and motor pathways |
| **Criscuolo et al. 2022** | ALE meta-analysis of fMRI/sMRI/DTI | 84 studies, 3,005 participants | Coherent cortico-subcortical network: increased volume in auditory, sensorimotor, interoceptive, limbic regions in musicians | Meta-analytic convergence across 58 coordinate studies | Population-level validation of insula-sensorimotor-interoceptive circuit |

> **NOTE — Resting-state limitation**: Zamorano 2023 uses resting-state fMRI connectivity, which measures correlation not causation. The causal link is established by Kleber 2013's anesthesia manipulation showing that disrupting somatosensory feedback causally modulates right AIC activity differentially in singers vs nonsingers.
>
> **NOTE — Cross-species evidence**: Eliades 2024 provides mechanistic single-neuron evidence from marmosets showing dual vocal suppression processes, but translation to human singing training requires caution. The phasic/tonic dissociation supports the model's separate interoceptive vs motor pathways.

### 3.2 Effect Size Summary

```
Primary Evidence (k=6):  Multi-method convergence across species
Method Range:            rs-fMRI, task fMRI + anesthesia (causal), single-neuron, ALE meta-analysis
Key Effect Sizes:        F = 22.08 (Kleber 2013 right AIC interaction)
                         t(728) = −4.8 (pitch accuracy singers > nonsingers)
                         F(1,728) = 106.63 (pitch reproduction group main effect)
                         r = 0.46 (phrase-interval correlation, 3285 units)
Causal Evidence:         YES — vocal-fold anesthesia (Kleber 2013) + microstimulation (Eliades 2024)
Heterogeneity:           Low (consistent insula-sensorimotor finding across paradigms)
Quality Assessment:      γ-tier → approaching β (causal anesthesia evidence strengthens claim)
Replication:             Partially replicated across Zarate 2008, 2010, Kleber 2013, Zamorano 2023
```

---

## 4. R³ Input Mapping: What STC Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | STC Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **B: Energy** | [7] | amplitude | Vocal intensity | Voice production |
| **B: Energy** | [8] | loudness | Respiratory amplitude | Breath monitoring |
| **C: Timbre** | [12] | warmth | Vocal warmth | Singing resonance quality |
| **C: Timbre** | [15] | tristimulus1 | Harmonic balance | Voice timbre |
| **C: Timbre** | [16] | tristimulus2 | Mid-harmonic energy | Vocal quality |
| **C: Timbre** | [17] | tristimulus3 | High-harmonic energy | Vocal brightness |
| **D: Change** | [21] | spectral_change | Vocal dynamics | Phrase transitions |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Respiratory timing | Breath-phrase coupling |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Interoceptive-motor | Voice-body connection |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ v2 Group | Index | Feature | STC Role | Citation |
|-------------|-------|---------|----------|----------|
| **G: Rhythm** | [68] | syncopation_index | Vocal rhythmic complexity for singing timing | Longuet-Higgins & Lee 1984; Witek 2014 |
| **G: Rhythm** | [69] | metricality_index | Metrical regularity for phrase-level vocal timing | Grahn & Brett 2007 |
| **G: Rhythm** | [74] | rhythmic_regularity | Rhythmic regularity for vocal-motor coordination stability | Lartillot & Toiviainen 2007 |

**Rationale**: STC models singing training connectivity between insula and sensorimotor cortex. Singing requires precise rhythmic control of vocal production: metricality_index and rhythmic_regularity capture the temporal regularity that vocalists must track for phrase timing, while syncopation_index modulates the rhythmic complexity of vocal passages. Criscuolo 2022's meta-analysis (84 studies) showed that singing training enhances temporal coordination, which these features directly quantify.

**Code impact** (future): `r3[..., 68:70]` and `r3[..., 74]` will feed STC's vocal timing pathway alongside existing timbre and interaction features.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[33:41] x_l4l5 ───────────────┐
TMH.sequence_integration[10:20] ─┼──► Interoceptive-motor connectivity
BEP.motor_coupling[10:20] ──────┘   Insula ↔ sensorimotor binding

R³[7] amplitude ─────────────────┐
R³[8] loudness ──────────────────┼──► Respiratory motor control
BEP.groove[20:30] ──────────────┘   Vocal intensity → breath coupling

R³[12,15:18] timbre features ───┐
TMH.short_term[0:10] ───────────┼──► Speech sensorimotor areas
TMH.hierarchical[20:30] ────────┘   Vocal formants → articulatory feedback
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

STC requires H³ features at TMH horizons for interoceptive memory and BEP horizons for respiratory motor coupling. The demand reflects the vocal-respiratory temporal integration needed for singing.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 33 | x_l4l5[0] | 3 | M0 (value) | L2 (bidi) | Interoceptive signal 100ms |
| 33 | x_l4l5[0] | 3 | M2 (std) | L2 (bidi) | Interoceptive variability 100ms |
| 33 | x_l4l5[0] | 8 | M14 (periodicity) | L2 (bidi) | Interoceptive period 500ms |
| 33 | x_l4l5[0] | 16 | M14 (periodicity) | L2 (bidi) | Interoceptive period 1s |
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Respiratory coupling 100ms |
| 25 | x_l0l5[0] | 8 | M14 (periodicity) | L2 (bidi) | Respiratory period 500ms |
| 25 | x_l0l5[0] | 16 | M14 (periodicity) | L2 (bidi) | Respiratory period 1s |
| 8 | loudness | 3 | M0 (value) | L2 (bidi) | Breath amplitude 100ms |
| 8 | loudness | 3 | M20 (entropy) | L2 (bidi) | Breath entropy 100ms |
| 12 | warmth | 3 | M0 (value) | L2 (bidi) | Vocal warmth 100ms |
| 15 | tristimulus1 | 3 | M0 (value) | L2 (bidi) | Voice harmonic 100ms |
| 7 | amplitude | 8 | M1 (mean) | L2 (bidi) | Mean vocal intensity 500ms |

**Total STC H³ demand**: 12 tuples of 2304 theoretical = 0.52%

### 5.2 BEP + TMH Mechanism Binding

| Mechanism | Sub-section | Range | STC Role | Weight |
|-----------|-------------|-------|----------|--------|
| **BEP** | Beat Entrainment | BEP[0:10] | Phrase rhythmic structure | 0.5 |
| **BEP** | Motor Coupling | BEP[10:20] | Insula-sensorimotor coupling | **1.0** (primary) |
| **BEP** | Groove Processing | BEP[20:30] | Respiratory motor drive | 0.7 |
| **TMH** | Short-term Memory | TMH[0:10] | Vocal timbre tracking | 0.7 |
| **TMH** | Sequence Integration | TMH[10:20] | Interoceptive sequence | **1.0** (primary) |
| **TMH** | Hierarchical Structure | TMH[20:30] | Voice-body hierarchy | **1.0** (primary) |

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
STC OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f28_interoceptive_coupling│[0, 1] │ Insula-sensorimotor connectivity.
    │                          │        │ f28 = σ(0.40 * interoceptive_period_1s
    │                          │        │       + 0.30 * mean(TMH.seq[10:20])
    │                          │        │       + 0.30 * mean(BEP.motor[10:20]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f29_respiratory_integration│[0, 1]│ Respiratory motor control.
    │                          │        │ f29 = σ(0.40 * respiratory_period_1s
    │                          │        │       + 0.30 * mean(BEP.groove[20:30])
    │                          │        │       + 0.30 * breath_entropy)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f30_speech_sensorimotor  │ [0, 1] │ Speech motor areas activation.
    │                          │        │ f30 = σ(0.35 * vocal_warmth_100ms
    │                          │        │       + 0.35 * mean(TMH.hier[20:30])
    │                          │        │       + 0.30 * mean(TMH.short[0:10]))

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ connectivity_strength    │ [0, 1] │ Insula-sensorimotor connectivity.
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ respiratory_index        │ [0, 1] │ Respiratory control quality.
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ voice_body_coupling      │ [0, 1] │ Voice-body integration index.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ insula_activity          │ [0, 1] │ TMH interoceptive monitoring level.
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ vocal_motor              │ [0, 1] │ BEP vocal motor output level.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ connectivity_pred        │ [0, 1] │ Connectivity change prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ respiratory_pred         │ [0, 1] │ Respiratory control prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
10  │ vocal_pred               │ [0, 1] │ Vocal production prediction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Interoceptive-Motor Integration Function

```
PRIMARY EQUATIONS:

    Connectivity_Change = Post_Training_RS - Pre_Training_RS
    (RS = resting-state functional connectivity)

INTEROCEPTIVE-MOTOR COUPLING:

    Coupling = Insula_Activity × Sensorimotor_Activity × Training_Duration

RESPIRATORY INTEGRATION:

    Respiratory_Control = Breath_Regularity × Vocal_Intensity × Phrase_Alignment
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f28: Interoceptive Coupling
f28 = σ(0.40 * interoceptive_period_1s
       + 0.30 * mean(TMH.sequence_integration[10:20])
       + 0.30 * mean(BEP.motor_coupling[10:20]))
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f29: Respiratory Integration
f29 = σ(0.40 * respiratory_period_1s
       + 0.30 * mean(BEP.groove[20:30])
       + 0.30 * breath_entropy)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f30: Speech Sensorimotor
f30 = σ(0.35 * vocal_warmth_100ms
       + 0.35 * mean(TMH.hierarchical[20:30])
       + 0.30 * mean(TMH.short_term[0:10]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Source | Evidence Type | STC Function |
|--------|-----------------|--------|---------------|--------------|
| **Right Anterior Insula (AIC)** | (48, 0, −3) | Kleber 2013, F=22.08 | **Direct causal** (fMRI + anesthesia) | Interoceptive-motor integration hub; dissociates singers vs nonsingers |
| **Primary Sensorimotor Cortex (S1/M1)** | (−42, −12, 33) Area 4p; (57, 0, 21) Area 3a/3b | Kleber 2013, t=−4.05/−3.23 | Direct (fMRI connectivity) | Laryngeal/diaphragm somatotopic control |
| **Cerebellum Lobule V-VI** | (−33, −45, −39) | Kleber 2013, t=−5.02; Zamorano 2023 | Direct (fMRI) | Vocal timing calibration; singing-specific connectivity with insula |
| **Left Putamen** | (−24, 4, 4) | Zamorano 2023; Kleber 2013, t=−4.02 at (27,0,−3) | Direct (fMRI) | Interoceptive-motor gating; singing training connectivity |
| **Bilateral Thalamus** | (−3, −15, 6) L; (15, −6, −6) R | Kleber 2013, t=−3.91/−3.74 | Direct (fMRI) | Sensorimotor relay; singing training enhances insula-thalamus connectivity |
| **SMA** | (0, −6, 58) | Zarate 2008, literature inference | Indirect | Vocal motor planning and sequencing |

> **NOTE — Causal evidence**: Right AIC is the only region with causal evidence from the anesthesia manipulation (Kleber 2013). Other regions show correlational connectivity changes with singing training.
>
> **NOTE — Code uses different regions**: Code has SMA (0,−6,58), PMC (−40,−8,54), Cerebellum (24,−64,−28), Putamen (−24,4,4) — only 4 regions vs doc's 6. Doc is authoritative; code will be updated in Phase 5.

---

## 9. Cross-Unit Pathways

### 9.1 STC Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    STC INTERACTIONS                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (MPU):                                                         │
│  STC.interoceptive_coupling ────► MSR (training effects on connectivity)   │
│  STC.respiratory_integration ───► SPMC (respiratory in motor circuit)      │
│  STC.voice_body_coupling ───────► VRMSME (vocal in multi-modal)            │
│                                                                             │
│  CROSS-UNIT (MPU → ARU):                                                   │
│  STC.vocal_motor ────────────────► ARU (singing pleasure/reward)           │
│  STC.insula_activity ────────────► ARU (interoceptive affect signal)       │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  BEP mechanism (30D) ────────────► STC (beat/motor processing)             │
│  TMH mechanism (30D) ────────────► STC (temporal memory/sequence)          │
│  R³ (~16D) ──────────────────────► STC (direct spectral features)          │
│  H³ (12 tuples) ─────────────────► STC (temporal dynamics)                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **No training** | Untrained singers should show weaker insula connectivity | ✅ Testable |
| **Non-singing training** | Instrumental training should show different connectivity | ✅ Testable |
| **Respiratory disruption** | Disrupted breathing should reduce connectivity | Testable |
| **Insula lesion** | Insula damage should impair interoceptive-motor coupling | Testable |
| **Acute vs chronic** | Chronic training should show stronger resting-state changes | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class STC(BaseModel):
    """Singing Training Connectivity Model.

    Output: 11D per frame.
    Reads: BEP mechanism (30D), TMH mechanism (30D), R³ direct.
    """
    NAME = "STC"
    UNIT = "MPU"
    TIER = "γ3"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("BEP", "TMH")

    TAU_DECAY = None  # Training-dependent plasticity window

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """12 tuples for STC computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── TMH horizons: interoceptive-motor ──
            (33, 3, 0, 2),     # x_l4l5[0], 100ms, value, bidi
            (33, 3, 2, 2),     # x_l4l5[0], 100ms, std, bidi
            (33, 8, 14, 2),    # x_l4l5[0], 500ms, periodicity, bidi
            (33, 16, 14, 2),   # x_l4l5[0], 1000ms, periodicity, bidi
            # ── BEP horizons: respiratory coupling ──
            (25, 3, 0, 2),     # x_l0l5[0], 100ms, value, bidi
            (25, 8, 14, 2),    # x_l0l5[0], 500ms, periodicity, bidi
            (25, 16, 14, 2),   # x_l0l5[0], 1000ms, periodicity, bidi
            # ── Vocal/respiratory features ──
            (8, 3, 0, 2),      # loudness, 100ms, value, bidi
            (8, 3, 20, 2),     # loudness, 100ms, entropy, bidi
            (12, 3, 0, 2),     # warmth, 100ms, value, bidi
            (15, 3, 0, 2),     # tristimulus1, 100ms, value, bidi
            (7, 8, 1, 2),      # amplitude, 500ms, mean, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute STC 11D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30), "TMH": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,11) STC output
        """
        bep = mechanism_outputs["BEP"]    # (B, T, 30)
        tmh = mechanism_outputs["TMH"]    # (B, T, 30)

        # BEP sub-sections
        bep_beat = bep[..., 0:10]
        bep_motor = bep[..., 10:20]
        bep_groove = bep[..., 20:30]

        # TMH sub-sections
        tmh_short = tmh[..., 0:10]
        tmh_seq = tmh[..., 10:20]
        tmh_hier = tmh[..., 20:30]

        # H³ direct features
        interoceptive_period_1s = h3_direct[(33, 16, 14, 2)].unsqueeze(-1)
        respiratory_period_1s = h3_direct[(25, 16, 14, 2)].unsqueeze(-1)
        breath_entropy = h3_direct[(8, 3, 20, 2)].unsqueeze(-1)
        vocal_warmth_100ms = h3_direct[(12, 3, 0, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f28: Interoceptive Coupling (coefficients sum = 1.0)
        f28 = torch.sigmoid(
            0.40 * interoceptive_period_1s
            + 0.30 * tmh_seq.mean(-1, keepdim=True)
            + 0.30 * bep_motor.mean(-1, keepdim=True)
        )

        # f29: Respiratory Integration (coefficients sum = 1.0)
        f29 = torch.sigmoid(
            0.40 * respiratory_period_1s
            + 0.30 * bep_groove.mean(-1, keepdim=True)
            + 0.30 * breath_entropy
        )

        # f30: Speech Sensorimotor (coefficients sum = 1.0)
        f30 = torch.sigmoid(
            0.35 * vocal_warmth_100ms
            + 0.35 * tmh_hier.mean(-1, keepdim=True)
            + 0.30 * tmh_short.mean(-1, keepdim=True)
        )

        # ═══ LAYER M: Mathematical ═══
        connectivity_strength = torch.sigmoid(
            0.5 * f28 + 0.5 * interoceptive_period_1s
        )
        respiratory_index = f29
        voice_body_coupling = torch.sigmoid(
            0.5 * f28 + 0.5 * f30
        )

        # ═══ LAYER P: Present ═══
        insula_activity = tmh_seq.mean(-1, keepdim=True)
        vocal_motor = bep_groove.mean(-1, keepdim=True)

        # ═══ LAYER F: Future ═══
        connectivity_pred = torch.sigmoid(
            0.5 * f28 + 0.5 * interoceptive_period_1s
        )
        respiratory_pred = torch.sigmoid(
            0.5 * f29 + 0.5 * respiratory_period_1s
        )
        vocal_pred = torch.sigmoid(
            0.5 * f30 + 0.5 * vocal_warmth_100ms
        )

        return torch.cat([
            f28, f29, f30,                                          # E: 3D
            connectivity_strength, respiratory_index,
            voice_body_coupling,                                     # M: 3D
            insula_activity, vocal_motor,                            # P: 2D
            connectivity_pred, respiratory_pred, vocal_pred,         # F: 3D
        ], dim=-1)  # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 6 | Zamorano 2023, Kleber 2013, Zarate 2008/2010, Eliades 2024, Criscuolo 2022 |
| **Effect Sizes** | F=22.08 (AIC), t=−4.8 (pitch), r=0.46 (vocal suppression) | Multi-method, multi-species |
| **Evidence Modality** | rs-fMRI, task fMRI + anesthesia, single-neuron, ALE meta | Multi-modal with **causal evidence** |
| **Causal Evidence** | YES | Vocal-fold anesthesia (Kleber 2013) |
| **Brain Regions** | 6 regions with MNI coords | From Kleber 2013 (primary) + Zamorano 2023 |
| **Falsification Tests** | 2/5 testable | Anesthesia test partially validates criterion |
| **R³ Features Used** | ~16D of 49D | Energy + timbre + interactions |
| **H³ Demand** | 12 tuples (0.52%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Beat/motor processing |
| **TMH Mechanism** | 30D (3 sub-sections) | Temporal memory/sequence |
| **Output Dimensions** | **11D** | 4-layer structure |

---

## 13. Scientific References

1. Zamorano, A.M., Zatorre, R.J., Vuust, P., Friberg, A., Birbaumer, N., & Kleber, B. (2023). Singing training predicts increased insula connectivity with speech and respiratory sensorimotor areas at rest. *Brain Research*, 1813, 148418. DOI: 10.1016/j.brainres.2023.148418
2. Kleber, B., Zeitouni, A.G., Friberg, A., & Zatorre, R.J. (2013). Experience-dependent modulation of feedback integration during singing: Role of the right anterior insula. *Journal of Neuroscience*, 33(14), 6070-6080. DOI: 10.1523/JNEUROSCI.4893-12.2013
3. Zarate, J.M. & Zatorre, R.J. (2008). Experience-dependent neural substrates involved in vocal pitch regulation during singing. *NeuroImage*, 40(4), 1871-1887. DOI: 10.1016/j.neuroimage.2007.12.036
4. Zarate, J.M., Wood, S., & Bhatt, A. (2010). Neural networks involved in voluntary and involuntary vocal pitch regulation in experienced singers. *Neuropsychologia*, 48(2), 607-618. DOI: 10.1016/j.neuropsychologia.2009.10.025
5. Tsunada, J., Wang, X., & Eliades, S.J. (2024). Multiple processes of vocal sensory-motor interaction in primate auditory cortex. *Nature Communications*, 15, 3093. DOI: 10.1038/s41467-024-47510-2
6. Criscuolo, A., Pando-Naude, V., Bonetti, L., Vuust, P., & Brattico, E. (2022). An ALE meta-analytic review of musical expertise. *Scientific Reports*, 12, 11726. DOI: 10.1038/s41598-022-14959-4

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (NPL, GRV, EFC) | BEP (30D) + TMH (30D) mechanisms |
| Interoceptive signal | S⁰.X_L5L6[208:216] + HC⁰.EFC | R³.x_l4l5[33:41] + TMH.sequence_integration |
| Respiratory signal | S⁰.X_L4L5[192:200] + HC⁰.GRV | R³.x_l0l5[25:33] + BEP.groove |
| Vocal signal | S⁰.L6.spectral_envelope[55:60] + HC⁰.NPL | R³.timbre[12:21] + TMH.short_term |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 12/2304 = 0.52% | 12/2304 = 0.52% |
| Output | 11D | 11D (same) |

### Why BEP + TMH replaces HC⁰ mechanisms

- **EFC → TMH.sequence_integration** [10:20] + **BEP.motor_coupling** [10:20]: Efference copy mechanism for interoceptive-motor binding maps to TMH's sequence integration and BEP's motor coupling.
- **GRV → BEP.groove_processing** [20:30]: Groove processing for respiratory motor drive maps to BEP's groove section.
- **NPL → TMH.short_term** [0:10] + **TMH.hierarchical** [20:30]: Neural phase locking for vocal sensorimotor areas maps to TMH's short-term memory and hierarchical structure.

---

## 15. Doc-Code Mismatches (Phase 5 Reference)

> **Convention**: The **doc is authoritative**. Code will be updated in Phase 5.

| # | Field | Doc (this file) | Code (`stc.py`) | Resolution |
|---|-------|-----------------|------------------|------------|
| 1 | `FULL_NAME` | "Singing Training Connectivity" | "Sensorimotor Timing Calibration" | Update code |
| 2 | `OUTPUT_DIM` | 11 | 10 | Update code to 11 |
| 3 | `MECHANISM_NAMES` | ("BEP", "TMH") | ("BEP",) | Add TMH to code |
| 4 | `h3_demand` | 12 tuples (see §5.1) | () (empty) | Populate in code |
| 5 | `LAYERS` | E(3), M(3), P(2), F(3) = 11D | E(3), M(2), P(2), F(3) = 10D | Update Layer M to 3 dims |
| 6 | `dimension_names` | 11 names (§6.1) | 10 names (no voice_body_coupling) | Add missing dim |
| 7 | `citations` | Zamorano 2023 (primary) + Kleber 2013 + 4 more | Kleber 2023 (wrong year), Zarate 2010 | Update to 6 refs |
| 8 | `brain_regions` | 6 regions: Right AIC (48,0,−3), S1/M1, Cerebellum V-VI, Putamen, Thalamus, SMA | 4 regions: SMA (0,−6,58), PMC (−40,−8,54), CB (24,−64,−28), PUT (−24,4,4) | Update to 6 regions; AIC is primary |
| 9 | `evidence_count` | 6 papers | 2 citations total | Update counts per region |
| 10 | `confidence_range` | (0.50, 0.70) | (0.45, 0.65) | Update to match doc |
| 11 | `paper_count` | 6 | 2 | Update to 6 |
| 12 | `version` | "2.1.0" | "2.0.0" | Update version |

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **11D**
**Evidence Tier**: **γ (Integrative)**
**Confidence**: **50-70%**
