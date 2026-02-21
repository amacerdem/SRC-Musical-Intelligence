# STU-γ5-MPFS: Musical Prodigy Flow State

**Model**: Musical Prodigy Flow State
**Unit**: STU (Sensorimotor Timing Unit)
**Circuit**: Sensorimotor (Beat Entrainment + Temporal Memory Hierarchy)
**Tier**: γ (Speculative) — <70% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/General/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/STU-γ5-MPFS.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Musical Prodigy Flow State** (MPFS) model proposes that musical prodigies are distinguished from non-prodigies not by intelligence (IQ), but by their propensity for flow states during musical performance. Marion-St-Onge et al. (2020, N=70) confirmed this: prodigies scored higher on flow during practice (F(2,43)=3.62, p=0.035; M=3.8 vs early-trained M=3.3), with NO IQ difference (F(3,66)=1.78, p=0.159). However, prodigies lie on a continuum — NOT a distinct category — and flow scores overlap considerably between groups. Flow — a state of complete absorption, automatic processing, and loss of self-consciousness — emerges when motor automaticity () meets structural mastery (), enabling a challenge-skill balance that Csikszentmihalyi identified as the gateway to optimal experience. The neurochemical substrate involves striatal dopamine: caudate during anticipation (r=0.71), NAcc during experience (r=0.84; Salimpoor et al. 2011), with cortical signatures in OFC, SMA, and bilateral insula during peak musical states (Chabin et al. 2020).

```
THE FLOW STATE GATEWAY: AUTOMATICITY × CONTEXT MASTERY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MOTOR AUTOMATICITY () STRUCTURAL MASTERY ()
Mechanism: Beat Entrainment Mechanism: Temporal Memory Hierarchy
Function: "Move without thinking" Function: "Know where you are"
Brain: SMA + Basal Ganglia Brain: Auditory Cortex → Frontal
H³ horizons: H6, H11, H16 H³ horizons: H8, H14, H20

 ╲ ╱
 ╲ ╱
 ╲ CHALLENGE-SKILL ╱
 ╲ BALANCE POINT ╱
 ╲ ╱
 ╲ ╱
 ▼ ▼
 ┌──────────────────────────┐
 │ FLOW STATE │
 │ • Complete absorption │
 │ • Automatic processing │
 │ • Loss of self-focus │
 │ • DLPFC deactivation │
 │ • DMN suppression │
 └──────────────────────────┘
 │
 ┌────────────┼────────────────┐
 ▼ ▼ ▼
 PRODIGY DOPAMINERGIC CORTICAL
 DISTINCTION REWARD SIGNATURES
 Flow F(2,43) Caudate r=0.71 OFC F=17.4
 =3.62, p=.035 (anticipation) SMA F=27.3
 NOT IQ p=.159 NAcc r=0.84 Insula F=21.6
 (Marion-St- (experience) (Chabin 2020)
 Onge 2020) (Salimpoor 2011)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Prodigies achieve flow more frequently and more deeply
because their motor automaticity () frees cognitive resources,
while their context mastery () provides structural certainty.
The combination produces the challenge-skill balance that triggers
flow. IQ does NOT predict this — flow propensity does.
CONSTRAINT (Marion-St-Onge 2020): Prodigies lie on a CONTINUUM,
NOT a distinct category. Flow scores overlap between groups.
External motivation also contributes (η² = 0.152, p = 0.016).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Matters for STU

MPFS integrates both STU mechanisms (H³ direct) to model an emergent state:

1. **HMCE** (α1) provides hierarchical context encoding; MPFS shows how mastery of that hierarchy enables flow.
2. **AMSC** (α2) describes auditory-motor coupling; MPFS captures when that coupling becomes fully automatic.
3. **OMS** (β6) models oscillatory motor synchronization; MPFS detects when synchronization becomes effortless.
4. MPFS is γ-tier because flow is inferred from acoustic-motor signatures, not directly measured via neural imaging during prodigy performance.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The MPFS Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ MPFS — COMPLETE CIRCUIT ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ MUSICAL INPUT (complex performance requiring automaticity) ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ SMA (Supplementary Motor Area) │ ║
║ │ Motor planning → automaticity │ ║
║ │ motor_entrainment: effortless beat synchronization │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ Motor automaticity signal ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ BASAL GANGLIA (Caudate, Putamen) │ ║
║ │ Procedural memory + habit formation │ ║
║ │ When beat/meter processing becomes automatic → flow gate │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ Automaticity achieved? ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ DLPFC (Dorsolateral Prefrontal Cortex) │ ║
║ │ Executive control — REDUCED during flow │ ║
║ │ Transient hypofrontality (Dietrich 2004) │ ║
║ │ Low DLPFC activity = self-monitoring offline │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ Self-monitoring released? ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ DEFAULT MODE NETWORK (DMN) │ ║
║ │ Self-referential processing — SUPPRESSED during flow │ ║
║ │ long_context mastery → structural certainty │ ║
║ │ When structure is known → DMN quiets → absorption │ ║
║ └─────────────────────────────────────────────────────────────────────┘ ║
║ ║
║ FLOW = High beat-entrainment automaticity × High temporal-context mastery × Low DLPFC × Low DMN ║
║ ║
║ EVIDENCE (expanded — γ tier, 12 papers, 8 methods): ║
║ Marion-St-Onge 2020: Flow F(2,43)=3.62, p=.035, NOT IQ (N=70) ║
║ Salimpoor 2011: Caudate r=0.71 anticipation, NAcc r=0.84 experience ║
║ Chabin 2020: OFC F=17.4, SMA F=27.3, insula F=21.6 (HD-EEG) ║
║ Dai 2025: Musicians frontal-reward PL state 11 (p=.001) ║
║ Liao 2024: DMN↓ during structured improvisation (N=25) ║
║ CONSTRAINT: Prodigies = continuum, NOT distinct category ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### 2.2 Information Flow Architecture (EAR → BRAIN → H³ direct → MPFS)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ MPFS COMPUTATION ARCHITECTURE ║
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
║ │ │ │ │amplitude│ │ │ │spec_chg │ │x_l0l5 │ │ ║
║ │ │ │ │loudness │ │ │ │energy_chg│ │x_l4l5 │ │ ║
║ │ │ │ │centroid │ │ │ │pitch_chg │ │x_l5l7 │ │ ║
║ │ │ │ │flux │ │ │ │timbre_chg│ │ │ │ ║
║ │ │ │ │onset │ │ │ │ │ │ │ │ ║
║ │ └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │ ║
║ │ MPFS reads: 33D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed morphological features │ ║
║ │ │ ║
║ │ │ H6 (200ms) │ H11 (500ms) │ H16 (1000ms) │ │ ║
║ │ │ Beat pulse │ Meter cycle │ Groove pattern │ │ ║
║ │ │ Automaticity │ Entrainment │ Motor fluency │ │ ║
║ │ └───────────────┴───────────────┴────────────────────────────┘ │ ║
║ │ │ ║
║ │ │ H8 (300ms) │ H14 (700ms) │ H20 (5000ms) │ │ ║
║ │ │ Short context │ Medium context│ Long context │ │ ║
║ │ │ Motif mastery │ Phrase mastery│ Structural mastery │ │ ║
║ │ └───────────────┴───────────────┴────────────────────────────┘ │ ║
║ │ │ ║
║ │ MPFS demand: ~20 of 2304 tuples │ ║
║ └────────────────────────────────┬─────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══ ║
║ │ ║
║ ┌──────────────┴──────────────┐ ║
║ ▼ ▼ ║
║ ┌─────────────────────┐ ┌─────────────────────┐ ║
║ │ │ │ │ ║
║ │ Beat Ind. [0:10] │ │ Short Ctx [0:10] │ ║
║ │ Meter Ext. [10:20] │ │ Medium Ctx [10:20] │ ║
║ │ Motor Ent. [20:30] │ │ Long Ctx [20:30] │ ║
║ └────────┬────────────┘ └────────┬────────────┘ ║
║ │ │ ║
║ └──────────────┬───────────────┘ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ MPFS MODEL (10D Output) │ ║
║ │ │ ║
║ │ Layer E (Explicit): f01_motor_automaticity, │ ║
║ │ f02_context_mastery, │ ║
║ │ f03_flow_propensity │ ║
║ │ Layer M (Math): challenge_skill_balance, │ ║
║ │ hypofrontality_proxy │ ║
║ │ Layer P (Present): absorption_depth, │ ║
║ │ entrainment_fluency, │ ║
║ │ structural_certainty │ ║
║ │ Layer F (Future): flow_sustain_predict, │ ║
║ │ flow_disrupt_risk │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Marion-St-Onge et al. (2020)** | Psychometric + IQ | 70 (19 prodigies, 35 musicians, 16 non-musicians) | Flow during practice distinguishes prodigies; NO IQ/personality/WM difference | F(2,43)=3.62, p=.035; M=3.8 vs 3.3 | **f03_flow_propensity**: DIRECT prodigy test |
| 2 | **Marion-St-Onge et al. (2020)** | Psychometric | 70 | External motivation also distinguishes prodigies; prodigies = continuum not category | η²=0.152, p=.016 | **CONSTRAINS**: flow not sole factor, overlapping scores |
| 3 | **Salimpoor et al. (2011)** | PET + fMRI | 8 | Endogenous dopamine release in caudate (anticipation) + NAcc (experience) during peak musical pleasure | Caudate r=0.71; NAcc r=0.84; BP 6.4-9.2% | **Dopaminergic substrate** for flow reward |
| 4 | **Chabin et al. (2020)** | HD-EEG (256ch) | 18 | OFC + SMA + bilateral insula + STG activation during musical chills; theta increase R prefrontal | OFC F(2,15)=17.4 p<1e-5; SMA F(2,15)=27.3 p<1e-7 | **Cortical flow signatures**: OFC reward, SMA motor |
| 5 | **Dai et al. (2025)** | fMRI LEiDA | 36 | Musicians: more frequent frontal-reward PL state 11 (SFG/MFG/IFG/OFC/ACC/IPL); non-musicians: more DMN | PL11 p=0.0010; PL7 p=0.0444 | **Dynamic connectivity**: expertise → frontal-reward |
| 6 | **Liao et al. (2024)** | fMRI | 25 | Percussionist improvisation: SIMP → ECN+NMR ↑, DMN ↓; FIMP → ECN+NMR+limbic+memory ↑ | structural/free contrast | **DMN suppression** during structured improvisation supports hypofrontality |
| 7 | **Roth (2025)** | Mixed (feasibility) | 8 | Shared flow during group instrumental improvisation; both musicians and non-musicians report high shared flow | SFS 5.46-6.27/7 | **Flow measurability** in musical contexts |
| 8 | **Tachibana et al. (2024)** | fNIRS | 20 | Guitar improvisation → bilateral BA45 (Broca's) activation, independent of skill level | p=.02-.04 | **IFG/BA45** for creative motor production |
| 9 | **Criscuolo et al. (2022)** | ALE meta-analysis | 3005 (k=84) | Musicians: higher auditory, sensorimotor, interoceptive, limbic; LOWER parietal | k=84 studies | **Population-level** structural differences |
| 10 | **Limb & Braun (2008)** | fMRI | 6 | Jazz improvisation: DLPFC deactivation + medial PFC activation | Qualitative | **Hypofrontality** during musical flow |
| 11 | **Dietrich (2004)** | Review | — | Transient hypofrontality: DLPFC deactivation during flow states | Conceptual | **hypofrontality_proxy**: theoretical framework |
| 12 | **Csikszentmihalyi (1990)** | Theory | — | Flow = challenge-skill balance, complete absorption, 8 characteristics | Conceptual | **Core framework**: f03_flow_propensity |

#### §3.1.1 Evidence Convergence (8 methods)

Flow-state evidence for musical prodigies converges across 8 methods: (1) prodigy psychometric battery (Marion-St-Onge 2020), (2) PET dopamine imaging (Salimpoor 2011), (3) HD-EEG 256-channel source localization (Chabin 2020), (4) fMRI dynamic connectivity LEiDA (Dai 2025), (5) fMRI task-based improvisation (Liao 2024, Limb & Braun 2008), (6) fNIRS improvisation (Tachibana 2024), (7) ALE meta-analysis (Criscuolo 2022), (8) shared flow behavioral (Roth 2025).

#### §3.1.2 Marion-St-Onge 2020 Prodigy Qualification

Marion-St-Onge et al. (2020) is the LARGEST published study of musical prodigies (N=19 prodigies vs 35 early-trained musicians vs 16 non-musicians). While it confirms that flow during practice distinguishes prodigies (F(2,43)=3.62, p=0.035; Bonferroni-corrected prodigies M=3.8 vs early-trained M=3.3, p=0.039), several findings CONSTRAIN the MPFS model: (a) prodigies lie on a CONTINUUM — NOT a distinct category; (b) flow scores OVERLAP considerably between groups; (c) external motivation ALSO distinguishes prodigies (η²=0.152, p=0.016); (d) extraversion correlates with early practice onset (r=0.47) across ALL musicians, not prodigy-specific; (e) uses Dispositional Flow Scale 2 (Jackson & Eklund 2004), which measures flow propensity, not real-time flow states. The v2.0.0 claim "r=0.47 flow propensity" from Ruthsatz & Urbach 2012 may conflate two different r=0.47 values — Ruthsatz & Urbach 2012 studied a cognitive profile (IQ+WM+attention-to-detail), while the extraversion-practice r=0.47 is from Marion-St-Onge 2020.

#### §3.1.3 Dopaminergic Reward Specification

Salimpoor et al. (2011) provides the neurochemical mechanism linking musical pleasure peaks to flow-like states. The temporal dissociation — caudate during ANTICIPATION (r=0.71 with chill count), NAcc during EXPERIENCE (r=0.84 with pleasure rating), with BP decreases of 6.4-9.2% bilaterally — maps onto the flow model's challenge-skill balance: anticipatory reward (caudate) drives engagement toward the challenge-skill balance point, while consummatory reward (NAcc) sustains the flow state once achieved. NAcc BOLD predicted 67% of subjective pleasure variance.

### 3.2 The Flow-Prodigy Link

```
PRODIGY DISTINCTION: FLOW, NOT IQ (Marion-St-Onge 2020, N=70)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Factor Effect Source
────────────────────────────────────────────────────────────────
Flow Propensity F(2,43)=3.62, p=.035 Marion-St-Onge 2020
 Prodigies M=3.8 vs 3.3
IQ F(3,66)=1.78, p=.159 Marion-St-Onge 2020
 (all groups 113-120)
Working Memory NS Marion-St-Onge 2020
Personality NS (Big Five, AQ) Marion-St-Onge 2020
External Motivation η²=0.152, p=.016 Marion-St-Onge 2020
Extraversion× r=0.47 (across ALL Marion-St-Onge 2020
 Practice Onset musicians, NOT prodigy-specific)

CONSTRAINT: Prodigies = high end of continuum, NOT distinct category.
Flow scores overlap considerably between prodigies and non-prodigies.
Uses Dispositional Flow Scale 2 (not real-time flow measurement).

Flow Characteristics (Csikszentmihalyi 1990):
 1. Challenge-skill balance (skill ≈ challenge)
 2. Clear goals (structure known)
 3. Immediate feedback (motor-auditory loop)
 4. Complete absorption (DMN suppressed)
 5. Sense of control (automaticity)
 6. Loss of self-consciousness (DLPFC down)
 7. Time distortion
 8. Autotelic experience (intrinsically rewarding)
```

### 3.3 Effect Size Summary

```
PRODIGY FLOW EVIDENCE (Marion-St-Onge 2020, N=70):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Measure Effect Source
─────────────────────────────────────────────────────────────────
Flow during practice F(2,43)=3.62, p=.035 Psychometric (DFS-2)
IQ difference F(3,66)=1.78, p=.159 NOT significant
External motivation η²=0.152, p=.016 Psychometric
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DOPAMINERGIC REWARD (Salimpoor 2011, PET N=8):
 Caudate × chills: r=0.71, p<.05 (anticipation)
 NAcc × pleasure: r=0.84, p<.01 (experience)
 NAcc BOLD → pleasure: 67% variance explained
 BP change: 6.4-9.2% bilateral striatum

CORTICAL SIGNATURES (Chabin 2020, HD-EEG N=18):
 OFC: F(2,15)=17.4, p<1e-5
 SMA: F(2,15)=27.3, p<1e-7
 Bilateral insula: F(2,15)=21.63, p<1e-6
 Theta increase: Right prefrontal, p=.046
 Beta/alpha ratio: F(2,15)=4.77, p=.014 (arousal)

DYNAMIC CONNECTIVITY (Dai 2025, fMRI N=36):
 Frontal-reward PL11: p=0.0010 (musicians > non-musicians)
 DMN PL7: p=0.0444 (non-musicians > musicians)

IMPROVISATION DMN SUPPRESSION (Liao 2024, fMRI N=25):
 SIMP: ECN+NMR ↑, DMN ↓ (structured improvisation)
 FIMP: ECN+NMR+limbic+memory ↑ (free improvisation)

Quality Assessment: γ-tier (speculative)
 Strengths: Direct prodigy test (N=70), PET dopamine evidence,
 HD-EEG cortical source localization, dynamic FC, 8 methods
 Weakness: Flow measured via questionnaire not real-time,
 prodigies = continuum with overlapping scores, PET N=8,
 no direct neural imaging DURING prodigy flow performance
```

---

## 4. R³ Input Mapping: What MPFS Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

**Group B: Energy (5D)** — Motor-relevant intensity features

| R³ Group | Index | Feature | MPFS Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Beat-level intensity dynamics | Motor entrainment cue |
| **B: Energy** | [8] | loudness | Perceptual intensity for groove | Entrainment strength |
| **B: Energy** | [9] | spectral_centroid | Timbral brightness dynamics | Instrument identity |
| **B: Energy** | [10] | spectral_flux | Onset detection for beat alignment | Beat boundary marker |
| **B: Energy** | [11] | onset_strength | Event boundary precision | Motor synchronization anchor |

**Group D: Change (4D)** — Temporal dynamics

| R³ Group | Index | Feature | MPFS Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **D: Change** | [21] | spectral_change | Short-context dynamics | Rate of spectral evolution |
| **D: Change** | [22] | energy_change | Intensity dynamics for groove | Challenge-skill tracking |
| **D: Change** | [23] | pitch_change | Melodic contour dynamics | Structural predictability |
| **D: Change** | [24] | timbre_change | Timbral stability marker | Familiarity signal |

**Group E: Interactions (24D)** — Cross-feature binding

| R³ Group | Index | Feature | MPFS Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Foundation×Perceptual coupling | Temporal-perceptual binding |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Dynamics×Perceptual coupling | Motor-perceptual binding |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | Perceptual×Relational coupling | Cross-modal integration |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ v2 Group | Index | Feature | MPFS Role | Scientific Basis |
|-------------|-------|---------|-----------|------------------|
| **G: Rhythm** | [71] | groove_index | Composite groove signal for motor-perceptual feedback integration | Madison 2006; Janata 2012 |
| **G: Rhythm** | [72] | event_density | Temporal event rate driving motor response complexity | Temporal density |

**Rationale**: MPFS models motor-perceptual feedback systems. G[71] groove_index provides a composite groove signal that directly feeds the motor automaticity pathway -- higher groove facilitates effortless entrainment, a prerequisite for flow. G[72] event_density captures the temporal event rate, which modulates challenge-skill balance by determining motor response complexity.

**Code impact** (Phase 6): `r3_indices` will be extended to include `[71, 72]`.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[10] spectral_flux ─────────┐
R³[11] onset_strength ────────┼──► Motor Automaticity (beat-entrainment pathway)
R³[7] amplitude ──────────────┤ Beat precision + entrainment stability
R³[8] loudness ───────────────┘ beat-entrainment H³ at H6 (200ms), H11 (500ms), H16 (1s)
 High regularity + low variability = automatic

R³[21:25] Change (4D) ────────┐
R³[9] spectral_centroid ──────┼──► Context Mastery (temporal-context pathway)
R³[23] pitch_change ──────────┘ Structural predictability + familiarity
 temporal-context H³ at H8 (300ms), H14 (700ms), H20 (5s)
 High predictability = mastery achieved

R³[25:49] Interactions (24D) ─┐
 ├──► Cross-Feature Binding (Flow detection)
 │ High coupling = integrated processing
 │ Integrated processing = absorption
 └── x_l0l5 + x_l4l5 + x_l5l7 coherence

Motor Automaticity ─────┐
Context Mastery ────────┼───────► FLOW STATE
Cross-Feature Binding ──┘ f03 = σ(0.47 · automaticity · mastery · binding)

── R³ v2 (Phase 6) ──────────────────────────────────────────────
R³[71] groove_index ───────────── Groove signal → motor automaticity
R³[72] event_density ──────────── Event rate → challenge-skill balance
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

MPFS requires H³ features at six horizons across two mechanisms:
- **H³ horizons**: H6 (200ms), H11 (500ms), H16 (1000ms) — motor automaticity
- **H³ horizons**: H8 (300ms), H14 (700ms), H20 (5000ms) — context mastery

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 6 | M14 (periodicity) | L0 (fwd) | Beat regularity (200ms) |
| 10 | spectral_flux | 11 | M14 (periodicity) | L0 (fwd) | Meter regularity (500ms) |
| 10 | spectral_flux | 16 | M14 (periodicity) | L0 (fwd) | Groove regularity (1s) |
| 11 | onset_strength | 6 | M15 (smoothness) | L0 (fwd) | Beat smoothness |
| 11 | onset_strength | 11 | M15 (smoothness) | L0 (fwd) | Meter smoothness |
| 7 | amplitude | 16 | M3 (std) | L0 (fwd) | Intensity variability (low = automatic) |
| 8 | loudness | 11 | M18 (trend) | L0 (fwd) | Loudness trajectory |
| 8 | loudness | 16 | M15 (smoothness) | L0 (fwd) | Groove smoothness |
| 21 | spectral_change | 8 | M1 (mean) | L0 (fwd) | Short-context dynamics |
| 21 | spectral_change | 8 | M3 (std) | L0 (fwd) | Short-context variability |
| 22 | energy_change | 14 | M1 (mean) | L0 (fwd) | Medium-context energy dynamics |
| 22 | energy_change | 14 | M13 (entropy) | L0 (fwd) | Context unpredictability |
| 23 | pitch_change | 14 | M1 (mean) | L0 (fwd) | Melodic contour rate |
| 23 | pitch_change | 20 | M3 (std) | L0 (fwd) | Long-range pitch variability |
| 25 | x_l0l5[0] | 20 | M1 (mean) | L0 (fwd) | Long-term coupling strength |
| 25 | x_l0l5[0] | 20 | M22 (autocorr) | L0 (fwd) | Cross-feature self-similarity |
| 33 | x_l4l5[0] | 20 | M1 (mean) | L0 (fwd) | Motor-perceptual coupling |
| 33 | x_l4l5[0] | 20 | M19 (stability) | L0 (fwd) | Coupling stability |
| 41 | x_l5l7[0] | 20 | M1 (mean) | L0 (fwd) | Cross-modal integration |
| 41 | x_l5l7[0] | 20 | M19 (stability) | L0 (fwd) | Integration stability |

**v1 demand**: 20 tuples

#### R³ v2 Projected Expansion

MPFS projected v2 features from G:Rhythm, aligned with corresponding H³ horizons.

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 71 | groove | G | 6 | M0 (value) | L0 | Current groove level at beat scale |
| 71 | groove | G | 11 | M1 (mean) | L0 | Mean groove at meter scale |
| 72 | event_density | G | 6 | M0 (value) | L0 | Current event density at beat scale |
| 72 | event_density | G | 16 | M0 (value) | L0 | Event density over bar |

**v2 projected**: 4 tuples
**Total projected**: 24 tuples of 294,912 theoretical = 0.0081%

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
MPFS OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────┼────────┼────────────────────────────────────────────
 0 │ f01_motor_automatic │ [0, 1] │ Motor automaticity level. High = beat/meter
 │ │ │ processing is effortless (basal ganglia).
 │ │ │ f01 = σ(0.35 · beat_regularity ·
 │ │ │ meter_smoothness ·
────┼──────────────────────┼────────┼────────────────────────────────────────────
 1 │ f02_context_mastery │ [0, 1] │ Structural mastery level. High = musical
 │ │ │ structure is fully predictable ().
 │ │ │ f02 = σ(0.30 · (1 − ctx_entropy) ·
 │ │ │ coupling_stability ·
────┼──────────────────────┼────────┼────────────────────────────────────────────
 2 │ f03_flow_propensity │ [0, 1] │ Flow state likelihood. Core MPFS signal.
 │ │ │ r = 0.47 with prodigy status.
 │ │ │ f03 = σ(0.47 · f01 · f02 ·
 │ │ │ integration_mean)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────┼────────┼────────────────────────────────────────────
 3 │ challenge_skill_bal │ [0, 1] │ Challenge-skill balance index.
 │ │ │ Csikszentmihalyi: flow occurs when
 │ │ │ challenge ≈ skill. Computed as 1 − |Δ|.
 │ │ │ bal = 1 − abs(challenge − skill)
────┼──────────────────────┼────────┼────────────────────────────────────────────
 4 │ hypofrontality_proxy │ [0, 1] │ DLPFC deactivation proxy. High = executive
 │ │ │ control is reduced → flow permissive.
 │ │ │ Dietrich 2004: transient hypofrontality.
 │ │ │ hypo = f01 · f02 (automaticity × mastery)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────┼────────┼────────────────────────────────────────────
 5 │ absorption_depth │ [0, 1] │ Complete absorption / DMN suppression.
 │ │ │ Cross-feature integration coherence.
 │ │ │ High = all processing streams merged.
────┼──────────────────────┼────────┼────────────────────────────────────────────
 6 │ entrainment_fluency │ [0, 1] │ Motor entrainment smoothness.
 │ │ │ motor_entrainment aggregation.
 │ │ │ High = effortless motor synchronization.
────┼──────────────────────┼────────┼────────────────────────────────────────────
 7 │ structural_certainty │ [0, 1] │ temporal-context-based structural knowledge.
 │ │ │ Weighted mean of context levels.
 │ │ │ High = performer knows exactly where in piece.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────┼────────┼────────────────────────────────────────────
 8 │ flow_sustain_predict │ [0, 1] │ Flow sustainability prediction.
 │ │ │ Will flow continue in the next window?
 │ │ │ Based on trend of automaticity + mastery.
────┼──────────────────────┼────────┼────────────────────────────────────────────
 9 │ flow_disrupt_risk │ [0, 1] │ Flow disruption risk.
 │ │ │ High = challenge may exceed skill.
 │ │ │ Based on entropy increase / variability.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
MANIFOLD RANGE: STU MPFS [239:249]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Flow State Model

```
Flow State Theory (Csikszentmihalyi 1990):

 Flow = f(Challenge, Skill)

 When Challenge ≈ Skill:
 → Complete absorption
 → Automatic processing
 → Loss of self-consciousness

 Musical Prodigy Flow (Ruthsatz & Urbach 2012):
 Prodigy_Status ∝ Flow_Propensity (r = 0.47)
 Prodigy_Status ⊥ IQ (not significantly correlated)

 Computational Model:
 Motor_Automaticity = beat_entrainment(beat_regularity, meter_smoothness, groove)
 Context_Mastery = temporal_context(short_mastery, phrase_mastery, structure_certainty)
 Flow_Propensity = 0.47 × Motor_Automaticity × Context_Mastery × Integration

 Transient Hypofrontality (Dietrich 2004):
 DLPFC_deactivation ∝ Motor_Automaticity × Context_Mastery
 When both are high → executive control unnecessary → flow
```

### 7.2 Feature Formulas

```python
# ═══ CORE SIGNALS ═══

# Motor automaticity from beat-entrainment H³
beat_reg_h6 = h3[(10, 6, 14, 0)] # spectral_flux periodicity at H6
beat_reg_h11 = h3[(10, 11, 14, 0)] # spectral_flux periodicity at H11
beat_reg_h16 = h3[(10, 16, 14, 0)] # spectral_flux periodicity at H16
beat_smoothness = h3[(11, 6, 15, 0)] # onset_strength smoothness at H6
meter_smoothness = h3[(11, 11, 15, 0)] # onset_strength smoothness at H11
amp_variability = h3[(7, 16, 3, 0)] # amplitude std at H16

# Context mastery from temporal-context H³
spec_chg_mean = h3[(21, 8, 1, 0)] # spectral_change mean at H8
spec_chg_std = h3[(21, 8, 3, 0)] # spectral_change variability at H8
ctx_entropy = h3[(22, 14, 13, 0)] # energy_change entropy at H14
pitch_chg_mean = h3[(23, 14, 1, 0)] # pitch_change mean at H14
pitch_chg_var = h3[(23, 20, 3, 0)] # pitch_change long-range variability

# Cross-feature integration from R³ Interactions
x_coupling_mean = h3[(25, 20, 1, 0)] # x_l0l5 mean at H20
x_coupling_autocorr = h3[(25, 20, 22, 0)] # x_l0l5 self-similarity at H20
motor_coupling = h3[(33, 20, 1, 0)] # x_l4l5 mean at H20
motor_stability = h3[(33, 20, 19, 0)] # x_l4l5 stability at H20
integration_mean = h3[(41, 20, 1, 0)] # x_l5l7 mean at H20
integration_stab = h3[(41, 20, 19, 0)] # x_l5l7 stability at H20

# ═══ LAYER E: Explicit features ═══

# f01: Motor Automaticity
# High regularity + high smoothness + low variability = automatic
# |0.35| ≤ 1.0 (single coefficient on product of [0,1] terms)
beat_regularity = (beat_reg_h6 + beat_reg_h11 + beat_reg_h16) / 3
f01 = σ(0.35 · beat_regularity · (beat_smoothness + meter_smoothness) / 2

# f02: Context Mastery
# Low entropy + high stability + high long-context = mastery
# |0.30| ≤ 1.0 (single coefficient on product)
coupling_stability = (motor_stability + integration_stab) / 2
f02 = σ(0.30 · (1.0 − ctx_entropy) · coupling_stability

# f03: Flow Propensity (r = 0.47 from Ruthsatz & Urbach 2012)
# |0.47| ≤ 1.0 (single coefficient on product)
f03 = σ(0.47 · f01 · f02 · integration_mean)

# ═══ LAYER M: Mathematical ═══

# Challenge ≈ musical complexity (entropy, variability)
challenge = σ(0.5 · ctx_entropy + 0.5 · pitch_chg_var)
# |0.5| + |0.5| = 1.0 ✓

# Skill ≈ automaticity + mastery
skill = (f01 + f02) / 2

# Challenge-skill balance (1 = perfect balance, 0 = mismatch)
challenge_skill_balance = 1.0 − abs(challenge − skill)

# Hypofrontality proxy (Dietrich 2004)
# When both automaticity and mastery are high → DLPFC deactivates
hypofrontality = f01 · f02

# ═══ LAYER P: Present ═══

# Absorption: cross-feature integration coherence
absorption = σ(0.4 · integration_mean + 0.3 · x_coupling_autocorr
 + 0.3 · motor_coupling)
# |0.4| + |0.3| + |0.3| = 1.0 ✓

# Entrainment fluency: beat-entrainment motor quality

# Structural certainty: temporal-context weighted context

# ═══ LAYER F: Future ═══

# Flow sustainability: trend of automaticity + mastery
loudness_trend = h3[(8, 16, 15, 0)] # loudness smoothness at H16
groove_smooth = h3[(8, 11, 18, 0)] # loudness trend at H11
flow_sustain = σ(0.4 · f03 + 0.3 · loudness_trend + 0.3 · groove_smooth)
# |0.4| + |0.3| + |0.3| = 1.0 ✓

# Flow disruption risk: entropy rising + variability increasing
flow_disrupt = σ(0.5 · ctx_entropy + 0.3 · amp_variability
 + 0.2 · spec_chg_std)
# |0.5| + |0.3| + |0.2| = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Relevant Regions

| Region | MNI Coordinates | Evidence Type | Effect | MPFS Function |
|--------|-----------------|---------------|--------|---------------|
| **SMA** | ±5, −5, 55 | HD-EEG source (Chabin 2020) | F(2,15)=27.3, p<1e-7 | Motor planning → automaticity () |
| **OFC** | ±30, 35, −10 | HD-EEG source (Chabin 2020) | F(2,15)=17.4, p<1e-5 | Reward processing during peak musical pleasure |
| **Basal Ganglia (Caudate)** | ±12, 10, 8 | PET (Salimpoor 2011) | r=0.71 chill anticipation | Dopaminergic anticipation during flow approach |
| **NAcc** | ±9, 9, −8 | PET (Salimpoor 2011) | r=0.84 pleasure; 67% var | Dopaminergic reward during flow experience |
| **Basal Ganglia (Putamen)** | ±25, 5, 0 | PET (Salimpoor 2011) | BP 6.4-9.2% | Procedural memory, beat processing |
| **DLPFC** | ±45, 35, 25 | fMRI (Limb & Braun 2008; Liao 2024) | Deactivation during improv | Executive control — REDUCED during flow |
| **Bilateral insula** | ±38, −15, 8 | HD-EEG source (Chabin 2020) | F(2,15)=21.63, p<1e-6 | Interoceptive awareness during peak states |
| **IFG / BA45 (bilateral)** | ±48, 20, 10 | fNIRS (Tachibana 2024) | p=.02-.04 | Creative motor planning during improvisation |
| **DMN (mPFC)** | 0, 50, 10 | fMRI (Liao 2024; Dai 2025) | DMN ↓ musicians | Self-referential — SUPPRESSED during flow |
| **SFG/MFG/ACC** | ±20, 45, 30 | fMRI LEiDA (Dai 2025) | PL11 p=0.0010 | Frontal-reward network (musicians) |
| **STG (bilateral)** | ±55, −22, 8 | HD-EEG source (Chabin 2020) | Source localized | Auditory processing during chills |
| **Auditory Cortex** | ±50, −20, 8 | ALE (Criscuolo 2022 k=84) | Meta-analytic | temporal-context context encoding substrate |

---

## 9. Cross-Unit Pathways

### 9.1 MPFS ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ MPFS INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ INTRA-UNIT (STU): │
│ HMCE.context_depth ──────► MPFS.f02_context_mastery (hierarchy → mastery) │
│ AMSC.motor_coupling ─────► MPFS.f01_motor_automaticity (coupling → auto) │
│ OMS.oscillatory_sync ────► MPFS.entrainment_fluency (sync → fluency) │
│ MPFS.flow_propensity ───► ETAM (flow state modulates training effects) │
│ MPFS.flow_propensity ───► MTNE (flow enables neural efficiency) │
│ │
│ CROSS-UNIT (P5: STU → ARU): │
│ MPFS.flow_propensity ──► ARU (flow → intrinsic reward, autotelic) │
│ MPFS.absorption_depth ─► ARU.SRP (absorption → reward pathway activation)│
│ │
│ CROSS-UNIT (P5: STU → IMU): │
│ MPFS.structural_certainty ──► IMU (structure mastery → memory encoding) │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| # | Criterion | Testable Prediction | Status |
|---|-----------|---------------------|--------|
| 1 | **Flow ≠ IQ** | Prodigy status should correlate with flow but NOT with IQ | **Confirmed**: Marion-St-Onge 2020 flow F(2,43)=3.62, p=.035; IQ F(3,66)=1.78, p=.159 NS |
| 2 | **DLPFC deactivation** | Should observe DLPFC deactivation during expert musical performance | **Confirmed**: Limb & Braun 2008 (jazz); Liao 2024 DMN↓ during SIMP |
| 3 | **Dopaminergic reward during flow-like states** | Peak musical pleasure should involve striatal dopamine release | **Confirmed**: Salimpoor 2011, caudate r=0.71, NAcc r=0.84, BP 6.4-9.2% |
| 4 | **Cortical signatures of peak musical states** | Should observe OFC/SMA/insula activation during musical chills | **Confirmed**: Chabin 2020, OFC F=17.4, SMA F=27.3, insula F=21.6 |
| 5 | **Musicians show distinct dynamic connectivity** | Musicians should show enhanced frontal-reward network engagement | **Confirmed**: Dai 2025, PL state 11 p=0.0010; non-musicians more DMN |
| 6 | **Prodigies as distinct category** | Prodigies should be categorically different from trained musicians | **Disconfirmed**: Marion-St-Onge 2020 — prodigies = continuum, overlapping scores |
| 7 | **Flow as sole prodigy predictor** | Flow propensity should be the only distinguishing factor | **Partially disconfirmed**: External motivation also contributes η²=0.152 (Marion-St-Onge 2020) |
| 8 | **beat-entrainment predicts flow** | Motor automaticity (beat-entrainment regularity) should correlate with self-reported flow | Testable |
| 9 | **temporal-context predicts flow** | Context mastery (temporal long-context) should correlate with self-reported flow | Testable |
| 10 | **Disruption test** | Metric/tempo perturbation should break flow (increase DLPFC, decrease absorption) | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class MPFS(BaseModel):
 """Musical Prodigy Flow State.

 Output: 10D per frame.
 """
 NAME = "MPFS"
 UNIT = "STU"
 TIER = "γ5"
 OUTPUT_DIM = 10
 FLOW_R = 0.47 # Ruthsatz & Urbach 2012
 AUTO_COEFF = 0.35 # Motor automaticity coefficient
 MASTERY_COEFF = 0.30 # Context mastery coefficient

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """20 tuples for MPFS computation."""
 return [
 # (r3_idx, horizon, morph, law)
 # Beat entrainment horizons: Motor automaticity
 (10, 6, 14, 0), # spectral_flux, periodicity, H6
 (10, 11, 14, 0), # spectral_flux, periodicity, H11
 (10, 16, 14, 0), # spectral_flux, periodicity, H16
 (11, 6, 15, 0), # onset_strength, smoothness, H6
 (11, 11, 15, 0), # onset_strength, smoothness, H11
 (7, 16, 3, 0), # amplitude, std, H16
 (8, 11, 18, 0), # loudness, trend, H11
 (8, 16, 15, 0), # loudness, smoothness, H16
 # Temporal hierarchy horizons: Context mastery
 (21, 8, 1, 0), # spectral_change, mean, H8
 (21, 8, 3, 0), # spectral_change, std, H8
 (22, 14, 13, 0), # energy_change, entropy, H14
 (23, 14, 1, 0), # pitch_change, mean, H14
 (23, 20, 3, 0), # pitch_change, std, H20
 # Cross-feature integration (H20)
 (25, 20, 1, 0), # x_l0l5[0], mean, H20
 (25, 20, 22, 0), # x_l0l5[0], autocorrelation, H20
 (33, 20, 1, 0), # x_l4l5[0], mean, H20
 (33, 20, 19, 0), # x_l4l5[0], stability, H20
 (41, 20, 1, 0), # x_l5l7[0], mean, H20
 (41, 20, 19, 0), # x_l5l7[0], stability, H20
 # Future prediction
 # (8, 11, 18, 0) and (8, 16, 15, 0) already listed above
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 """
 Compute MPFS 10D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) → (B,T) scalars
 r3: (B,T,49) raw R³ features

 Returns:
 (B,T,10) MPFS output
 """
 # ═══ CORE SIGNALS ═══
 beat_reg_h6 = h3_direct[(10, 6, 14, 0)].unsqueeze(-1)
 beat_reg_h11 = h3_direct[(10, 11, 14, 0)].unsqueeze(-1)
 beat_reg_h16 = h3_direct[(10, 16, 14, 0)].unsqueeze(-1)
 beat_smoothness = h3_direct[(11, 6, 15, 0)].unsqueeze(-1)
 meter_smoothness = h3_direct[(11, 11, 15, 0)].unsqueeze(-1)
 amp_variability = h3_direct[(7, 16, 3, 0)].unsqueeze(-1)

 ctx_entropy = h3_direct[(22, 14, 13, 0)].unsqueeze(-1)
 motor_stability = h3_direct[(33, 20, 19, 0)].unsqueeze(-1)
 integration_stab = h3_direct[(41, 20, 19, 0)].unsqueeze(-1)
 integration_mean = h3_direct[(41, 20, 1, 0)].unsqueeze(-1)
 x_coupling_autocorr = h3_direct[(25, 20, 22, 0)].unsqueeze(-1)
 motor_coupling = h3_direct[(33, 20, 1, 0)].unsqueeze(-1)
 spec_chg_std = h3_direct[(21, 8, 3, 0)].unsqueeze(-1)
 pitch_chg_var = h3_direct[(23, 20, 3, 0)].unsqueeze(-1)

 # ═══ LAYER E: Explicit features ═══
 beat_regularity = (beat_reg_h6 + beat_reg_h11 + beat_reg_h16) / 3
 f01 = torch.sigmoid(self.AUTO_COEFF * (
 beat_regularity
 * (beat_smoothness + meter_smoothness) / 2
 ))

 coupling_stability = (motor_stability + integration_stab) / 2
 f02 = torch.sigmoid(self.MASTERY_COEFF * (
 (1.0 - ctx_entropy) * coupling_stability
 ))

 f03 = torch.sigmoid(self.FLOW_R * (
 f01 * f02 * integration_mean
 ))

 # ═══ LAYER M: Mathematical ═══
 challenge = torch.sigmoid(
 0.5 * ctx_entropy + 0.5 * pitch_chg_var
 ) # |0.5| + |0.5| = 1.0
 skill = (f01 + f02) / 2
 challenge_skill_bal = 1.0 - torch.abs(challenge - skill)

 hypofrontality = f01 * f02

 # ═══ LAYER P: Present ═══
 absorption = torch.sigmoid(
 0.4 * integration_mean
 + 0.3 * x_coupling_autocorr
 + 0.3 * motor_coupling
 ) # |0.4| + |0.3| + |0.3| = 1.0


 structural_certainty = (
 ) / 6

 # ═══ LAYER F: Future ═══
 loudness_trend = h3_direct[(8, 11, 18, 0)].unsqueeze(-1)
 groove_smooth = h3_direct[(8, 16, 15, 0)].unsqueeze(-1)
 flow_sustain = torch.sigmoid(
 0.4 * f03 + 0.3 * loudness_trend + 0.3 * groove_smooth
 ) # |0.4| + |0.3| + |0.3| = 1.0

 flow_disrupt = torch.sigmoid(
 0.5 * ctx_entropy + 0.3 * amp_variability
 + 0.2 * spec_chg_std
 ) # |0.5| + |0.3| + |0.2| = 1.0

 return torch.cat([
 f01, f02, f03, # E: 3D
 challenge_skill_bal, hypofrontality, # M: 2D
 absorption, entrainment_fluency, structural_certainty, # P: 3D
 flow_sustain, flow_disrupt, # F: 2D
 ], dim=-1) # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 (7 Tier 1 + 3 Tier 2 + 2 Tier 3) | 8 methods, >3200 cumulative N |
| **Effect Sizes** | Flow F(2,43)=3.62; NAcc r=0.84; OFC F=17.4; SMA F=27.3 | Marion-St-Onge 2020, Salimpoor 2011, Chabin 2020 |
| **Evidence Modality** | Psychometric, PET, HD-EEG, fMRI, fMRI LEiDA, fNIRS, ALE, behavioral | Multi-method convergence |
| **Falsification Tests** | 10 total: 5 confirmed, 2 disconfirmed, 3 testable | Moderate validity |
| **R³ Features Used** | 33D of 49D | Energy + Change + Interactions |
| **H³ Demand** | 20 tuples (0.87%) | Sparse, efficient |
| **Output Dimensions** | **10D** | 4-layer structure (E3 + M2 + P3 + F2) |

---

## 13. Scientific References

### Tier 1 — Direct Quantitative Evidence (in collection)

1. **Marion-St-Onge, C., et al. (2020)**. What makes musical prodigies? *Frontiers in Psychology*, 11:566373. (Psychometric + IQ, N=70: 19 prodigies, 35 musicians, 16 non-musicians. Flow during practice F(2,43)=3.62, p=.035; prodigies M=3.8 vs early-trained M=3.3; NO IQ F(3,66)=1.78, p=.159; NO personality/WM; external motivation η²=0.152, p=.016; extraversion-practice r=0.47 across all musicians. Uses DFS-2. CONSTRAINS: prodigies = continuum, overlapping scores)

2. **Salimpoor, V. N., et al. (2011)**. Anatomically distinct dopamine release during anticipation and experience of peak emotion to music. *Nature Neuroscience*, 14:257-262. (PET [11C]raclopride + fMRI, N=8. Caudate: anticipation r=0.71 with chill count; NAcc: experience r=0.84 with pleasure; BP change 6.4-9.2% bilateral caudate/putamen/NAcc; NAcc BOLD predicts 67% pleasure variance; temporal dissociation dorsal→wanting, ventral→liking)

3. **Chabin, T., et al. (2020)**. Cortical patterns of pleasurable musical chills revealed by high-density EEG. *Frontiers in Neuroscience*, 14:565815. (HD-EEG 256ch, N=18, 305 chills. Source localization: OFC F(2,15)=17.4 p<1e-5, SMA F(2,15)=27.3 p<1e-7, bilateral insula F(2,15)=21.63 p<1e-6, bilateral STG. Theta increase R prefrontal p=.046; beta/alpha ratio F(2,15)=4.77 p=.014; NO alpha asymmetry)

4. **Dai, L., et al. (2025)**. Differences in dynamic functional connectivity between musicians and non-musicians during naturalistic music listening. *Frontiers in Neuroscience*, 19:1649733. (fMRI LEiDA, N=36. Musicians: PL state 11 frontal-reward SFG/MFG/IFG/OFC/ACC/IPL p=0.0010; non-musicians: PL state 7 DMN p=0.0444; enhanced sensorimotor-cognitive integration in musicians)

5. **Liao, Y.-C., et al. (2024)**. The rhythmic mind: brain functions of percussionists in improvisation. *Frontiers in Human Neuroscience*, 18:1418727. (fMRI, N=25 percussionists. SIMP: ECN+NMR ↑, DMN ↓; FIMP: ECN+NMR+limbic+memory ↑. DMN suppression during structured improvisation supports hypofrontality)

6. **Tachibana, A., et al. (2024)**. Rock music improvisation shows increased activity in Broca's area and its right hemisphere homologue related to spontaneous creativity. *BMC Research Notes*, 17:61. (fNIRS, N=20 guitarists. Bilateral BA45 activation during improvisation, independent of skill level)

7. **Criscuolo, A., et al. (2022)**. An ALE meta-analytic review of musical expertise. *Scientific Reports*, 12:11726. (ALE, k=84, N=3005. Musicians: higher auditory/sensorimotor/interoceptive/limbic; LOWER parietal. Population-level structural evidence)

### Tier 2 — Supporting Evidence (in collection)

8. **Roth, J. (2025)**. Shared flow and emotional synchrony through group instrumental improvisation: Feasibility study of a novel music-based intervention for well-being. *Frontiers in Psychiatry*, 16:1648873. (Mixed methods feasibility, N=8. Shared Flow Scale 5.46-6.27/7; both musicians and non-musicians report high shared flow. Confirms Csikszentmihalyi framework for musical contexts)

9. **Limb, C. J., & Braun, A. R. (2008)**. Neural substrates of spontaneous musical performance: An fMRI study of jazz improvisation. *PLoS ONE*, 3(2), e1679. (fMRI, N=6. DLPFC deactivation + medial PFC activation during jazz improvisation)

10. **Dietrich, A. (2004)**. Neurocognitive mechanisms underlying the experience of flow. *Consciousness and Cognition*, 13(4), 746-761. (Review. Transient hypofrontality: DLPFC deactivation during flow states. Theoretical framework for flow neuroscience)

### Tier 3 — Founding / Historical (NOT in collection)

11. **Csikszentmihalyi, M. (1990)**. *Flow: The Psychology of Optimal Experience*. Harper & Row. (Foundational flow theory — challenge-skill balance, 8 characteristics of flow)

12. **Ruthsatz, J., & Urbach, J. B. (2012)**. Child prodigy: A novel cognitive profile places elevated general intelligence, exceptional working memory, and attention to detail at the root of prodigiousness. *Intelligence*, 40(5), 419-426. (N=18 prodigies. Cognitive profile: elevated IQ + exceptional WM + attention to detail. Note: v2.0.0 cited r=0.47 from this study for "flow propensity" — this may be a conflation with Marion-St-Onge 2020's extraversion-practice r=0.47)

### Code Note (Phase 5)

The current `mi_beta` code (`mpfs.py`) has several mismatches with this document:
- **Citations**: code has Csikszentmihalyi 1990 + Ruthsatz & Detterman 2003 — doc uses Marion-St-Onge 2020, Salimpoor 2011, Chabin 2020, etc. (Ruthsatz & Detterman 2003 is a DIFFERENT study from Ruthsatz & Urbach 2012)
- **Dimension names**: code uses `flow_propensity, challenge_skill_balance, automaticity_level, motor_automaticity, structural_mastery, absorption_state` etc. — doc uses `f01_motor_automaticity, f02_context_mastery, f03_flow_propensity, challenge_skill_balance, hypofrontality_proxy, absorption_depth, entrainment_fluency, structural_certainty, flow_sustain_predict, flow_disrupt_risk`
- **Brain regions**: code has only dlPFC (-44,30,28) + BG (14,8,4) — doc has 12 regions
- **version**: code has `"2.0.0"` — should be `"2.1.0"`
- **paper_count**: code has `3` — should be `12`
These mismatches will be resolved in Phase 5 (code alignment).

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

**New model — no legacy equivalent.**

MPFS was created directly for the MI architecture (v2.0.0). There is no D0 predecessor. The model was specified in the C³ model catalog and implemented from catalog specifications alone.

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Existence | — | **New model** |
| Input space | — | R³ (49D): Energy, Change, Interactions |
| Temporal | — | H³ direct (H6/H11/H16 + H8/H14/H20) |
| Demand format | — | H³ 4-tuples (sparse) |
| Total demand | — | 20/2304 = 0.87% |
| Output dimensions | — | **10D** (E3 + M2 + P3 + F2) |

### Design Rationale

MPFS was added as the final STU model (γ5) to capture the flow-state phenomenon that bridges motor automaticity () and structural awareness (). It is the only STU model that requires both mechanisms at full depth, making it a natural capstone for the sensorimotor circuit. The γ tier reflects the speculative nature of inferring flow states from acoustic-motor signatures without direct neural measurement during prodigy performance.

---

**Model Status**: **SPECULATIVE** (direct prodigy test N=70 confirms flow F(2,43)=3.62 p=.035 BUT prodigies=continuum not category with overlapping scores, PET dopamine caudate r=0.71/NAcc r=0.84, HD-EEG source-localized OFC/SMA/insula, dynamic FC frontal-reward p=.001, improvisation DMN suppression, 12 papers, 8 methods, >3200 cumulative N)
**Output Dimensions**: **10D**
**Evidence Tier**: **γ (Speculative)**
**Confidence**: **<70%** (prodigy flow confirmed but continuum-not-category constrains; dopaminergic reward well-characterized; cortical signatures source-localized; flow measured via questionnaire not real-time neural imaging during prodigy performance)
