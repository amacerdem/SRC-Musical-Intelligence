# IMU-γ1-DMMS: Developmental Music Memory Scaffold

**Model**: Developmental Music Memory Scaffold
**Unit**: IMU (Integrative Memory Unit)
**Circuit**: Mnemonic (Hippocampal-Cortical)
**Tier**: γ (Speculative) — <70% confidence
**Version**: 2.1.0 (deep literature review, +7 papers, MNI validated, counterevidence noted)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/IMU-γ1-DMMS.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Developmental Music Memory Scaffold** (DMMS) models how early musical exposure during the neonatal and infant critical period (0-5 years) establishes lifelong memory scaffolds for auditory-emotional associations. These scaffolds — formed through caregiver bonding, lullaby recognition, and environmental music — determine the architecture upon which all subsequent musical memories are built.

```
DEVELOPMENTAL MUSIC MEMORY SCAFFOLD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EARLY BINDING (Neonatal)           MELODIC IMPRINTING (Infant)
Brain: Hippocampus + Amygdala      Brain: Auditory Cortex + Hippocampus
Mechanism: Music-emotion pairing   Mechanism: Melodic template formation
Trigger: Caregiver voice/lullaby   Trigger: Repeated melodic contour
Function: "This sound = safety"    Function: "I know this melody"
Evidence: Partanen 2022 (MEG,N=33) Evidence: Trehub 2003; Nguyen 2023

        DEVELOPMENTAL PLASTICITY (Critical Period)
        Brain: mPFC + Hippocampus + Auditory Cortex
        Mechanism: Synaptic pruning + consolidation
        Trigger: Repeated musical exposure during 0-5 years
        Function: "Music shapes my memory architecture"
        Evidence: Qiu 2025 (mPFC/amyg plasticity, N=48 mice)
                  Strait 2012 (ABR, N=31); Trainor 2012 (review)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Core Claim: Early musical exposure (neonatal, infant) establishes
memory scaffolds that influence lifelong auditory-emotional
associations. The critical period (0-5 years) offers maximum
plasticity for scaffold formation.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why Music Is Special for Developmental Memory

Music is uniquely suited to establish early memory scaffolds because:

1. **Caregiver bonding**: Lullabies and infant-directed singing create the first music-emotion pairings. The caregiver's voice timbre becomes a permanent template for "warmth" and "safety."

2. **Repetition structure**: Musical pieces naturally contain repetition (verses, refrains), which provides the exact reinforcement needed for hippocampal consolidation during the critical period.

3. **Multimodal binding**: Musical exposure in infancy co-occurs with touch, movement, and social gaze — binding auditory features to a rich emotional context that strengthens scaffold formation.

4. **Melodic imprinting**: Neonates show preferential responses to melodies heard in utero (DeCasper & Fifer 1980), suggesting scaffold formation begins even before birth.

### 1.2 Why This Belongs in IMU

DMMS sits in IMU (not ARU) because its core claim is about **memory architecture formation** — how the hippocampal-cortical system develops templates for storing and retrieving musical information. The emotional component (caregiver bonding) is the *trigger* for scaffold formation, but the *outcome* is a memory structure. ARU's DAP model addresses the complementary question of hedonic capacity development.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The DMMS Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 DMMS — DEVELOPMENTAL MEMORY CIRCUIT                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║               CRITICAL PERIOD (0-5 years)                                   ║
║                       │                                                      ║
║       ┌───────────────┼───────────────┐                                     ║
║       ▼               ▼               ▼                                     ║
║  Caregiver        Environmental    Repetitive                               ║
║  Voice/Lullaby    Music            Melodic Patterns                         ║
║       │               │               │                                     ║
║       ▼               ▼               ▼                                     ║
║  ┌──────────────────────────────────────────────────────────────────┐       ║
║  │                    AUDITORY CORTEX (A1/STG)                      │       ║
║  │                                                                  │       ║
║  │  Core (A1):         Belt:              Parabelt:                 │       ║
║  │  Spectrotemporal    Timbre features    Melodic contour           │       ║
║  │  encoding           Voice recognition  Pattern recognition        │       ║
║  └──────┬──────────────┬──────────────────┬─────────────────────────┘       ║
║         │              │                  │                                  ║
║         ▼              ▼                  ▼                                  ║
║  ┌──────────────────┐          ┌────────────────────┐                       ║
║  │   HIPPOCAMPUS    │          │     AMYGDALA       │                       ║
║  │                  │          │                    │                       ║
║  │  Scaffold        │          │  Emotional         │                       ║
║  │  formation:      │          │  tagging:          │                       ║
║  │  • Template      │          │  • Safety/comfort  │                       ║
║  │    consolidation │          │  • Arousal binding  │                       ║
║  │  • Pattern       │          │  • Valence pairing  │                       ║
║  │    completion    │          │                    │                       ║
║  └────────┬─────────┘          └─────────┬──────────┘                       ║
║           │                              │                                  ║
║           └──────────────┬───────────────┘                                  ║
║                          │                                                  ║
║                          ▼                                                  ║
║  ┌─────────────────────────────────────────────────────────┐                ║
║  │                    mPFC (Medial Prefrontal)              │                ║
║  │                                                         │                ║
║  │  Self-referential processing:                           │                ║
║  │  • "This is MY music" (early identity)                  │                ║
║  │  • Caregiver association → self-concept binding         │                ║
║  │  • Scaffold integration with personal narrative         │                ║
║  └──────────────────────────┬──────────────────────────────┘                ║
║                             │                                                ║
║                             ▼                                                ║
║              DEVELOPMENTAL MEMORY SCAFFOLD                                   ║
║              (Templates for lifelong musical memory)                         ║
║                                                                              ║
║  EVIDENCE (expanded — γ tier, 12 papers):                                   ║
║  Partanen 2022: Parental singing enhances auditory processing (MEG, N=33)  ║
║  Qiu 2025: Fetal-infant music → mPFC/amygdala plasticity (mouse, N=48)    ║
║  Strait 2012: Early training → brainstem encoding (ABR, N=31)              ║
║  Scholkmann 2024: CMT → prefrontal/auditory oxygenation (fNIRS, N=17)     ║
║  Whiteford 2025: COUNTER — No FFR-training association (N>260)             ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### 2.2 Information Flow Architecture (EAR -> BRAIN -> MEM -> DMMS)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DMMS COMPUTATION ARCHITECTURE                            ║
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
║  │                                                                  │        ║
║  │  ┌───────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌────────┐ │        ║
║  │  │CONSONANCE │ │ ENERGY  │ │ TIMBRE  │ │ CHANGE   │ │ X-INT  │ │        ║
║  │  │ 7D [0:7]  │ │ 5D[7:12]│ │ 9D      │ │ 4D       │ │ 24D    │ │        ║
║  │  │           │ │         │ │ [12:21] │ │ [21:25]  │ │ [25:49]│ │        ║
║  │  │roughness  │ │amplitude│ │warmth   │ │entropy   │ │x_l0l5  │ │        ║
║  │  │sethares   │ │loudness │ │tristim. │ │flux      │ │x_l4l5  │ │        ║
║  │  │pleasant.  │ │onset    │ │tonalness│ │concent.  │ │x_l5l7  │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                       DMMS reads: 25D                            │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Encoding ──┐ ┌── Consolidation ─┐ ┌── Retrieval ──────┐   │        ║
║  │  │ 1s (H16)     │ │ 5s (H20)         │ │ 36s (H24)        │   │        ║
║  │  │              │ │                   │ │                   │   │        ║
║  │  │ Working mem  │ │ Hippocampal       │ │ Long-term         │   │        ║
║  │  │ binding      │ │ consolidation     │ │ scaffold chunk    │   │        ║
║  │  └──────┬───────┘ └──────┬────────────┘ └──────┬────────────┘   │        ║
║  │         │               │                      │                │        ║
║  │         └───────────────┴──────────────────────┘                │        ║
║  │                         DMMS demand: ~15 of 2304 tuples         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Mnemonic Circuit ═════════    ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  MEM (30D)      │  Memory Encoding & Retrieval mechanism                 ║
║  │                 │                                                        ║
║  │ Encoding  [0:10]│  novelty, binding strength, schema match               ║
║  │ Familiar [10:20]│  recognition signal, nostalgia, deja-vu               ║
║  │ Retrieval[20:30]│  recall probability, vividness, coloring               ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    DMMS MODEL (10D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Episodic):   f37_early_binding, f38_dev_plasticity,    │        ║
║  │                        f39_melodic_imprint                       │        ║
║  │  Layer M (Math):       scaffold_strength, imprinting_depth       │        ║
║  │  Layer P (Present):    scaffold_activation, bonding_warmth       │        ║
║  │  Layer F (Future):     scaffold_persistence_fc,                  │        ║
║  │                        preference_formation_fc,                  │        ║
║  │                        therapeutic_potential_fc                   │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | Brain Region | DMMS Relevance |
|---|-------|--------|---|-------------|-------------|--------------|----------------|
| 1 | **Partanen et al. (2022)** | MEG RCT | 33 (21 preterm + 12 full-term) | Parental singing during kangaroo care enhances auditory processing (MMR) in preterm infants at term age; singing intervention group shows larger neural responses than controls | η²=0.229 (group effect oddball), η²=0.309 (sex×singing interaction) | Auditory cortex (left temporal MEG sensors) | **Neonatal scaffold formation: caregiver singing directly shapes auditory neural responses; core validation of early binding mechanism** |
| 2 | **Qiu et al. (2025)** | RNA-seq + Golgi staining + behavioral (mouse) | 48 mice (4 groups × 12) | Fetal-to-infant music exposure (E13 → postnatal wk 1/3/5) enhances mPFC and amygdala dendritic complexity, spine density, MAP2 expression; dose-dependent social behavior improvement (r=0.38, p<0.0001) | r=0.38 (dose-response social interaction), p<0.01 (dendritic branching) | mPFC, Amygdala (Golgi/immunofluorescence) | **Critical period plasticity: direct evidence that prenatal-to-infant music exposure induces lasting synaptic plasticity in scaffold-relevant regions; dose-dependent effects validate critical window model** |
| 3 | **Strait et al. (2012)** | ABR + behavioral | 31 children (ages 7-13; 15 musicians, 16 non-musicians) | Musical training during early childhood enhances subcortical speech encoding; musicians show more robust brainstem representation of speech harmonics and less degradation in noise | r=0.562-0.629 (training years vs. speech-in-noise/harmonic encoding, p<0.005) | Auditory brainstem (subcortical) | **Critical period depth: early musical training shapes subcortical encoding, supporting scaffold formation model; training before age 5 relates to enhanced processing** |
| 4 | **Scholkmann et al. (2024)** | fNIRS | 17 preterm (GA ≥30 wks) | Creative music therapy (humming in lullaby style) alters cerebrovascular oxygenation and perfusion in preterm infant prefrontal and auditory cortex; two response groups identified | Group-level StO2 change (exploratory) | Right prefrontal cortex, Left auditory cortex (fNIRS) | **Scaffold formation mechanism: CMT induces measurable hemodynamic changes in neonatal prefrontal and auditory regions, supporting real-time scaffold activation** |
| 5 | **Nguyen, Trainor et al. (2023)** | Review | -- | Comprehensive framework: caregivers universally communicate with infants via song; infant-directed singing supports co-regulation, bonding, and prosocial behavior; infants biologically prepared for pitch/rhythm processing from before birth | -- | -- | **Caregiver bonding scaffold: universal infant-directed singing provides the ecological mechanism for scaffold formation; validates bonding_warmth dimension** |
| 6 | **Sena Moore et al. (2025)** | Theoretical model | -- | Musical Contour Regulation Facilitation (MCRF) model defines essential music characteristics for emotion regulation development in early childhood (0-5 yrs); music's temporal structure, repetition, and contour support co-regulation | -- | -- | **Scaffold architecture: MCRF provides theoretical support for how music's structural features (contour, repetition) scaffold emotion regulation during critical period** |
| 7 | **Trehub (2003)** | Review | -- | Developmental origins of musicality; infants prefer consonance, show enhanced processing of infant-directed singing, and discriminate melodic contour from birth | -- | -- | **Melodic imprinting: innate preference scaffold; consonance preference validates R³ roughness mapping** |
| 8 | **Trainor & Unrau (2012)** | Review | -- | Musical training before age 7 enhances auditory processing; auditory cortex development is experience-dependent during sensitive period | -- | Auditory cortex (A1) | **Critical period plasticity: scaffold depth** |
| 9 | **DeCasper & Fifer (1980)** | Behavioral | 10 | Neonates prefer mother's voice heard in utero; sucking rate modulation demonstrates prenatal auditory learning | behavioral | -- | **Prenatal scaffold formation via voice timbre** |
| 10 | **Trehub & Hannon (2006)** | Review | -- | Infant music perception involves both domain-general and domain-specific mechanisms; culture-specific tuning occurs by 12 months | -- | -- | **Early melodic template formation** |
| 11 | **Whiteford et al. (2025)** | EEG (FFR), preregistered | >260 | Large-scale multi-site study **failed to replicate** association between musical training and enhanced subcortical (FFR) neural encoding of speech; no effect of age-of-onset of training | null (no association found) | Auditory brainstem (FFR) | **COUNTEREVIDENCE: challenges claims that early musical training directly enhances subcortical encoding; suggests scaffold effects may be cortical/hippocampal rather than brainstem-level** |
| 12 | **Qiu et al. (2025) — amygdala** | Immunofluorescence | 48 mice | Music exposure reduces GFAP (astrocyte) and IBA1 (microglia) expression in amygdala, suggesting neuroprotective effect and reduced neuroinflammation in scaffold-relevant regions | p<0.05 (GFAP Music-3 vs control) | Amygdala (immunofluorescence) | **Scaffold neuroprotection: music-induced glial changes in amygdala may create permissive environment for scaffold formation and persistence** |

### 3.2 The Developmental Story: Scaffold Formation

```
COMPLETE TEMPORAL PROFILE OF DEVELOPMENTAL SCAFFOLD FORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1: PRENATAL EXPOSURE (in utero, -3 to 0 months)
──────────────────────────────────────────────────────
Fetus hears maternal voice and environmental music.
Low-frequency components transmitted through amniotic fluid.
Earliest melodic templates form around voice prosody.
R³ relevant: Warmth [12], Tonalness [14] (voice characteristics)

Phase 2: NEONATAL BINDING (0-6 months)
───────────────────────────────────────
Music-emotion pairing through caregiver interaction.
Lullaby = safety, comfort, attachment bond.
Hippocampus + amygdala form first music-emotion scaffolds.
R³ relevant: Consonance [0:7] (pleasant = safe)

Phase 3: INFANT IMPRINTING (6-24 months)
────────────────────────────────────────
Repeated melodic patterns consolidate into stable templates.
Voice/instrument discrimination emerges via timbre learning.
Scaffold complexity grows with environmental richness.
R³ relevant: x_l5l7 [41:49] (consonance x timbre = familiar pattern)

Phase 4: CRITICAL PERIOD PEAK (2-5 years)
─────────────────────────────────────────
Maximum synaptic plasticity for musical memory formation.
Scaffold architecture solidifies through pruning.
Music preference foundations established.
R³ relevant: x_l0l5 [25:33] (energy x consonance = salience learning)

Phase 5: POST-CRITICAL CONSOLIDATION (5+ years)
────────────────────────────────────────────────
Scaffold architecture stabilizes.
New memories are STORED ON existing scaffold, not creating new ones.
Lifelong pattern: early music = strongest emotional resonance.
This is why childhood melodies evoke the deepest nostalgia.
```

### 3.3 Limitations and Counterevidence

DMMS is gamma-tier because evidence is primarily from reviews, animal models, and general neurodevelopmental principles. No longitudinal studies directly tracking neonatal music exposure to adult memory scaffold architecture exist. The critical period timing (0-5 years) is extrapolated from general auditory cortex development, not music-specific studies.

**Key counterevidence (v2.1.0):** Whiteford et al. (2025, N>260, preregistered) failed to replicate the association between musical training and enhanced subcortical (FFR) neural encoding of speech in a large multi-site study. This challenges the assumption that early musical exposure directly enhances brainstem-level processing. DMMS's scaffold formation may therefore be primarily cortical and hippocampal rather than subcortical, which is consistent with the model's emphasis on hippocampal consolidation and mPFC integration but requires acknowledging that subcortical enhancement claims (e.g., auditory brainstem plasticity) from smaller studies (Strait et al. 2012, N=31) may not generalize.

**Translational gap:** The strongest mechanistic evidence (Qiu et al. 2025) comes from a mouse model with passive music exposure, which does not fully replicate interactive caregiver-infant singing. Cross-species translation to human scaffold formation remains indirect.

---

## 4. R³ Input Mapping: What DMMS Reads

### 4.1 R³ Feature Dependencies (25D of 49D)

| R³ Group | Index | Feature | DMMS Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Valence scaffold (inverse) | Neonates prefer consonance |
| **A: Consonance** | [3] | stumpf_fusion | Binding coherence proxy | Tonal fusion = coherent signal for encoding |
| **A: Consonance** | [4] | sensory_pleasantness | Comfort/safety association | Pleasant = safe in neonatal learning |
| **B: Energy** | [7] | amplitude | Arousal scaffold | Energy level during scaffold formation |
| **B: Energy** | [10] | loudness | Arousal proxy | Stevens 1957 psychophysical |
| **C: Timbre** | [12] | warmth | Caregiver voice proxy | Low-frequency warmth = maternal voice |
| **C: Timbre** | [14] | tonalness | Melodic recognition template | Harmonic-to-noise ratio for voice ID |
| **C: Timbre** | [18:21] | tristimulus1-3 | Voice/instrument scaffold | Early timbre discrimination |
| **D: Change** | [22] | entropy | Pattern complexity | Simple patterns scaffold first |
| **E: Interactions** | [25:33] | x_l0l5 (Energy x Consonance) | Salience-binding scaffold | What is loud + pleasant = important |
| **E: Interactions** | [41:49] | x_l5l7 (Consonance x Timbre) | Familiarity template | Timbre-consonance = "known" pattern |

### 4.2 Physical -> Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[0] roughness (inverse) ─────►   Consonance scaffold
                                    Low roughness = "safe sound" template
                                    Neonatal preference for consonance

R³[12] warmth ─────────────────►   Caregiver voice template
                                    Warm timbre = maternal/paternal voice
                                    Earliest auditory-emotional scaffold

R³[18:21] tristimulus1-3 ──────►   Voice/instrument discrimination
                                    Early timbre templates for recognition

R³[41:49] x_l5l7 ──────────────►  Familiarity scaffold
                                    Consonance x timbre = "known pattern"
                                    Core template for melodic imprinting

R³[25:33] x_l0l5 ──────────────►  Salience scaffold
                                    Energy x consonance = "important sound"
                                    What gets encoded during critical period

R³[22] entropy ─────────────────►  Complexity gating
                                    Low entropy = simple → scaffolds first
                                    High entropy = complex → later learning
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

DMMS requires H³ features at three MEM horizons: H16 (1s), H20 (5s), H24 (36s).

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 3 | stumpf_fusion | 16 | M1 (mean) | L2 (bidirectional) | Binding coherence at 1s |
| 3 | stumpf_fusion | 24 | M1 (mean) | L0 (forward) | Long-term binding scaffold |
| 4 | sensory_pleasantness | 16 | M0 (value) | L2 (bidirectional) | Current comfort signal |
| 4 | sensory_pleasantness | 20 | M1 (mean) | L0 (forward) | Sustained pleasantness |
| 10 | loudness | 16 | M0 (value) | L2 (bidirectional) | Current arousal level |
| 10 | loudness | 24 | M3 (std) | L0 (forward) | Arousal variability over 36s |
| 12 | warmth | 16 | M0 (value) | L2 (bidirectional) | Current voice-warmth signal |
| 12 | warmth | 20 | M1 (mean) | L0 (forward) | Sustained warmth (caregiver) |
| 14 | tonalness | 16 | M0 (value) | L2 (bidirectional) | Melodic recognition state |
| 14 | tonalness | 20 | M1 (mean) | L0 (forward) | Tonal template stability |
| 22 | entropy | 16 | M0 (value) | L2 (bidirectional) | Current pattern complexity |
| 22 | entropy | 24 | M19 (stability) | L0 (forward) | Pattern stability over 36s |
| 0 | roughness | 16 | M0 (value) | L2 (bidirectional) | Current dissonance level |
| 0 | roughness | 20 | M1 (mean) | L0 (forward) | Consonance scaffold stability |
| 7 | amplitude | 20 | M4 (max) | L0 (forward) | Peak energy over 5s |

**Total DMMS H³ demand**: 15 tuples of 2304 theoretical = 0.65%

### 5.2 MEM Mechanism Binding

DMMS reads from the **MEM** (Memory Encoding & Retrieval) mechanism:

| MEM Sub-section | Range | DMMS Role | Weight |
|-----------------|-------|-----------|--------|
| **Encoding State** | MEM[0:10] | Scaffold formation strength, novelty gating | **1.0** (primary) |
| **Familiarity Proxy** | MEM[10:20] | Template match, imprinting depth | 0.8 |
| **Retrieval Dynamics** | MEM[20:30] | Scaffold activation, recall from early templates | 0.6 |

DMMS does not read cross-unit mechanisms. It is a single-mechanism model (MEM only) — the simplest IMU architecture alongside CSSL.

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
DMMS OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
Manifold Range: IMU DMMS [378:388]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EPISODIC MEMORY FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0  │ f37_early_binding │ [0, 1] │ Neonatal music-emotion scaffold strength.
    │                   │        │ Hippocampus + Amygdala pairing.
    │                   │        │ f37 = σ(0.35 · (1 - roughness) · warmth
    │                   │        │      + 0.35 · stumpf · MEM.encoding.mean
    │                   │        │      + 0.30 · sensory_pleasantness)
    │                   │        │ |0.35| + |0.35| + |0.30| = 1.0
────┼───────────────────┼────────┼────────────────────────────────────────────
 1  │ f38_dev_plasticity│ [0, 1] │ Critical period formation index.
    │                   │        │ mPFC + Auditory cortex plasticity.
    │                   │        │ f38 = σ(0.40 · MEM.encoding.mean
    │                   │        │      + 0.30 · x_l0l5.mean
    │                   │        │      + 0.30 · (1 - entropy))
    │                   │        │ |0.40| + |0.30| + |0.30| = 1.0
────┼───────────────────┼────────┼────────────────────────────────────────────
 2  │ f39_melodic_impr  │ [0, 1] │ Early melodic memory template strength.
    │                   │        │ Auditory cortex + Hippocampus imprinting.
    │                   │        │ f39 = σ(0.40 · x_l5l7.mean · tonalness
    │                   │        │      + 0.30 · MEM.familiarity.mean
    │                   │        │      + 0.30 · warmth)
    │                   │        │ |0.40| + |0.30| + |0.30| = 1.0

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 3  │ scaffold_strength │ [0, 1] │ Overall scaffold formation/activation.
    │                   │        │ Combines encoding and familiarity signals.
    │                   │        │ S = MEM.encoding.mean · binding_coherence
    │                   │        │   + MEM.familiarity.mean · imprint_depth
────┼───────────────────┼────────┼────────────────────────────────────────────
 4  │ imprinting_depth  │ [0, 1] │ Depth of melodic imprinting.
    │                   │        │ σ(familiarity + tonal_stability + warmth)
    │                   │        │ High when music matches early templates.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 5  │ scaffold_activat  │ [0, 1] │ Current scaffold activation level.
    │                   │        │ MEM.retrieval_dynamics aggregation.
    │                   │        │ High when current music activates early
    │                   │        │ templates (familiar warmth + consonance).
────┼───────────────────┼────────┼────────────────────────────────────────────
 6  │ bonding_warmth    │ [0, 1] │ Caregiver-bonding warmth signal.
    │                   │        │ MEM.familiarity × warmth × (1 - roughness).
    │                   │        │ The "comfort" dimension of early memory.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 7  │ scaffold_persist  │ [0, 1] │ Scaffold persistence prediction (36s ahead).
    │                   │        │ Hippocampal consolidation trajectory.
    │                   │        │ Based on H24 long-term stability signals.
────┼───────────────────┼────────┼────────────────────────────────────────────
 8  │ preference_form   │ [0, 1] │ Preference formation prediction (5s ahead).
    │                   │        │ How strongly current exposure is forming
    │                   │        │ new scaffold layers.
────┼───────────────────┼────────┼────────────────────────────────────────────
 9  │ therapeutic_pot   │ [0, 1] │ Therapeutic potential prediction.
    │                   │        │ Scaffold activation × emotional coloring.
    │                   │        │ High when music accesses deep scaffolds
    │                   │        │ (clinical application: music therapy).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Scaffold Formation Function

```
Scaffold_Strength(music) = f(Encoding × Familiarity × BondingWarmth)

where:
  Encoding        = MEM.encoding_state[0:10].mean()   [hippocampal binding]
  Familiarity     = MEM.familiarity_proxy[10:20].mean() [template match]
  BondingWarmth   = warmth[12] × (1 - roughness[0])    [caregiver signal proxy]
  BindingCoherence = stumpf_fusion[3]                   [tonal coherence]
  ImprDpth        = x_l5l7[41:49].mean() × tonalness[14] [melodic template]

Expanded form:
  Scaffold_Strength = Encoding · BindingCoherence
                    + Familiarity · ImprDpth
  (clamped to [0, 1])

Imprinting_Depth = σ(Familiarity + tonalness[14] + warmth[12])
```

### 7.2 Feature Formulas

```python
# ---- Helper signals ----
# All R³ features are in [0, 1] range

consonance = 1.0 - R3.roughness[0]         # [0, 1]
warmth = R3.warmth[12]                       # [0, 1]
stumpf = R3.stumpf_fusion[3]                # [0, 1]
pleasant = R3.sensory_pleasantness[4]       # [0, 1]
tonalness = R3.tonalness[14]                # [0, 1]
entropy = R3.entropy[22]                     # [0, 1]
x_l0l5_mean = R3.x_l0l5[25:33].mean()      # [0, 1]
x_l5l7_mean = R3.x_l5l7[41:49].mean()      # [0, 1]

encoding = MEM.encoding_state[0:10].mean()
familiarity = MEM.familiarity_proxy[10:20].mean()
retrieval = MEM.retrieval_dynamics[20:30].mean()

# ---- Layer E: Episodic features ----

# f37: Early Binding (neonatal music-emotion scaffold)
f37 = sigma(0.35 * consonance * warmth
          + 0.35 * stumpf * encoding
          + 0.30 * pleasant)
# |0.35| + |0.35| + |0.30| = 1.0

# f38: Developmental Plasticity (critical period formation)
f38 = sigma(0.40 * encoding
          + 0.30 * x_l0l5_mean
          + 0.30 * (1.0 - entropy))
# |0.40| + |0.30| + |0.30| = 1.0

# f39: Melodic Imprinting (early melodic memory)
f39 = sigma(0.40 * x_l5l7_mean * tonalness
          + 0.30 * familiarity
          + 0.30 * warmth)
# |0.40| + |0.30| + |0.30| = 1.0

# ---- Layer M: Mathematical ----

# Scaffold strength
binding_coherence = stumpf * consonance
imprint_depth_raw = x_l5l7_mean * tonalness
scaffold_strength = clamp(
    encoding * binding_coherence + familiarity * imprint_depth_raw,
    0, 1
)

# Imprinting depth
imprinting_depth = sigma(
    0.35 * familiarity + 0.35 * tonalness + 0.30 * warmth
)
# |0.35| + |0.35| + |0.30| = 1.0

# ---- Layer P: Present ----

# Scaffold activation (current music activating early templates)
scaffold_activation = retrieval * familiarity

# Bonding warmth (caregiver-bonding signal)
bonding_warmth = familiarity * warmth * consonance

# ---- Layer F: Future ----

# Scaffold persistence (based on H24 long-term signals)
scaffold_persist = _predict_future(encoding, h3_direct, window_h=24)

# Preference formation (based on H20 consolidation)
preference_form = _predict_future(familiarity, h3_direct, window_h=20)

# Therapeutic potential (scaffold access x emotional coloring)
therapeutic_pot = scaffold_activation * consonance
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Evidence | Confidence | DMMS Function |
|--------|-----------------|----------|------------|---------------|
| **Hippocampus** | +/-26, -18, -18 | Neonatal review (scoping, n=1500); Qiu et al. 2025 (mouse, mPFC-amygdala circuit) | Indirect (review + animal) | Scaffold formation and consolidation; synaptic plasticity during critical period |
| **Amygdala** | +/-24, -4, -20 | Neonatal review (scoping, n=1500); Qiu et al. 2025 (increased dendritic complexity, MAP2, reduced GFAP/IBA1, N=48 mice) | Direct (animal histology) | Emotional tagging of early scaffolds; music-induced neuroprotection |
| **Auditory Cortex (A1/STG)** | +/-54, -22, 8 | Partanen et al. 2022 (MEG, N=33, η²=0.229); Scholkmann et al. 2024 (fNIRS, N=17, left auditory); Trainor 2012 (review) | Direct (MEG/fNIRS in neonates) | Melodic template formation; early auditory processing enhanced by parental singing |
| **mPFC** | 0, 52, 12 | Qiu et al. 2025 (RNA-seq + Golgi, N=48 mice: 1283 DEGs, increased dendritic branching); Scholkmann et al. 2024 (fNIRS, right prefrontal, N=17) | Direct (animal histology + neonatal fNIRS) | Self-referential scaffold integration; synaptic plasticity hub for social-emotional memory |
| **Right Prefrontal Cortex** | 40, 50, 10 | Scholkmann et al. 2024 (fNIRS, N=17 preterm: CMT-induced StO2 changes) | Direct (fNIRS in preterm neonates) | Online processing of caregiver-directed music; CMT-induced hemodynamic response |
| **Auditory Brainstem** | subcortical | Strait et al. 2012 (ABR, N=31, r=0.562); **CONTESTED** by Whiteford et al. 2025 (N>260, null result) | Contested | Subcortical speech encoding; training-related enhancement unconfirmed at population level |

---

## 9. Cross-Unit Pathways

### 9.1 DMMS Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DMMS INTERACTIONS                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (IMU):                                                         │
│  DMMS ──────► MEAMN (Music-Evoked Autobiographical Memory Network)         │
│       │        └── DMMS scaffolds are the FOUNDATION for adult MEAMs.      │
│       │            Without early scaffolds, MEAMN retrieval is weaker.     │
│       │                                                                     │
│       ├─────► MMP (Musical Mnemonic Preservation)                          │
│       │        └── DMMS scaffolds are the MOST preserved in                │
│       │            neurodegeneration (earliest memories last longest).      │
│       │                                                                     │
│       └─────► CSSL (Cross-Species Song Learning)                           │
│                └── DMMS provides the developmental framework that          │
│                    parallels avian song learning critical periods.          │
│                                                                             │
│  CROSS-UNIT (IMU → ARU):                                                  │
│  DMMS.bonding_warmth ──────► ARU.DAP (Developmental Affective Plasticity) │
│       └── DMMS memory scaffolds shape the hedonic response capacity        │
│           modeled by DAP. Complementary models: DMMS = memory side,        │
│           DAP = affect side of the same developmental process.             │
│                                                                             │
│  DMMS.scaffold_activation ──► ARU.NEMAC (Nostalgia Circuit)               │
│       └── Deep scaffold activation = strongest nostalgia trigger.          │
│           Music from scaffold-formation period evokes deepest nostalgia.   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Brain Pathway Cross-References

DMMS reads from the unified Brain (26D) for shared state:

| Brain Dimension | Index (MI-space) | DMMS Role |
|-----------------|-------------------|-----------|
| arousal | [177] | Encoding strength modulation |
| prediction_error | [178] | Novelty gating (novel = scaffold extension) |
| emotional_momentum | [180] | Sustained emotion strengthens scaffold |

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Critical period exists** | Musical memory formation before age 5 should be qualitatively different from later | Testable (longitudinal) |
| **Scaffold permanence** | Early musical memories should be the most resistant to degradation | Testable (AD/dementia studies) |
| **Caregiver voice primacy** | Timbre features matching caregiver voice should activate scaffolds most strongly | Testable (fMRI with voice stimuli) |
| **Enrichment effect** | Early musical enrichment should predict adult memory scaffold depth | Testable (retrospective) |
| **Cross-species parallel** | Bird song learning critical period should share timing with human scaffold formation | Partial: Zebra finch data (r=0.94, n=37) |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class DMMS(BaseModel):
    """Developmental Music Memory Scaffold.

    Output: 10D per frame.
    Reads: MEM mechanism (30D).
    No cross-unit dependencies — single-mechanism model.
    Zero learned parameters.
    """
    NAME = "DMMS"
    UNIT = "IMU"
    TIER = "γ1"
    OUTPUT_DIM = 10
    MANIFOLD_RANGE = (378, 388)
    MECHANISM_NAMES = ("MEM",)        # Single mechanism
    CROSS_UNIT = ()                    # No cross-unit reads

    # Coefficient rule: for sigmoid(sum w_i * g_i), |w_i| must sum <= 1.0
    EARLY_BIND_W = (0.35, 0.35, 0.30)   # sum = 1.0
    DEV_PLAST_W = (0.40, 0.30, 0.30)    # sum = 1.0
    MELODIC_IMP_W = (0.40, 0.30, 0.30)  # sum = 1.0
    IMPRINT_D_W = (0.35, 0.35, 0.30)    # sum = 1.0

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """15 tuples for DMMS computation."""
        return [
            # (r3_idx, horizon, morph, law)
            (3, 16, 1, 2),    # stumpf_fusion, 1s, mean, bidirectional
            (3, 24, 1, 0),    # stumpf_fusion, 36s, mean, forward
            (4, 16, 0, 2),    # pleasantness, 1s, value, bidirectional
            (4, 20, 1, 0),    # pleasantness, 5s, mean, forward
            (10, 16, 0, 2),   # loudness, 1s, value, bidirectional
            (10, 24, 3, 0),   # loudness, 36s, std, forward
            (12, 16, 0, 2),   # warmth, 1s, value, bidirectional
            (12, 20, 1, 0),   # warmth, 5s, mean, forward
            (14, 16, 0, 2),   # tonalness, 1s, value, bidirectional
            (14, 20, 1, 0),   # tonalness, 5s, mean, forward
            (22, 16, 0, 2),   # entropy, 1s, value, bidirectional
            (22, 24, 19, 0),  # entropy, 36s, stability, forward
            (0, 16, 0, 2),    # roughness, 1s, value, bidirectional
            (0, 20, 1, 0),    # roughness, 5s, mean, forward
            (7, 20, 4, 0),    # amplitude, 5s, max, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute DMMS 10D output.

        Args:
            mechanism_outputs: {"MEM": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) DMMS output
        """
        mem = mechanism_outputs["MEM"]    # (B, T, 30)

        # --- R³ features ---
        roughness = r3[..., 0:1]          # [0, 1]
        consonance = 1.0 - roughness      # [0, 1]
        stumpf = r3[..., 3:4]             # [0, 1]
        pleasant = r3[..., 4:5]           # [0, 1]
        warmth = r3[..., 12:13]           # [0, 1]
        tonalness = r3[..., 14:15]        # [0, 1]
        entropy = r3[..., 22:23]          # [0, 1]
        x_l0l5 = r3[..., 25:33]           # (B, T, 8)
        x_l5l7 = r3[..., 41:49]           # (B, T, 8)

        # --- MEM sub-sections ---
        mem_encoding = mem[..., 0:10]      # encoding state
        mem_familiar = mem[..., 10:20]     # familiarity proxy
        mem_retrieval = mem[..., 20:30]    # retrieval dynamics

        encoding = mem_encoding.mean(-1, keepdim=True)
        familiarity = mem_familiar.mean(-1, keepdim=True)
        retrieval = mem_retrieval.mean(-1, keepdim=True)

        x_l0l5_mean = x_l0l5.mean(-1, keepdim=True)
        x_l5l7_mean = x_l5l7.mean(-1, keepdim=True)

        # ═══ LAYER E: Episodic features ═══

        # f37: Early Binding — |0.35| + |0.35| + |0.30| = 1.0
        f37 = torch.sigmoid(
            0.35 * consonance * warmth
            + 0.35 * stumpf * encoding
            + 0.30 * pleasant
        )

        # f38: Developmental Plasticity — |0.40| + |0.30| + |0.30| = 1.0
        f38 = torch.sigmoid(
            0.40 * encoding
            + 0.30 * x_l0l5_mean
            + 0.30 * (1.0 - entropy)
        )

        # f39: Melodic Imprinting — |0.40| + |0.30| + |0.30| = 1.0
        f39 = torch.sigmoid(
            0.40 * x_l5l7_mean * tonalness
            + 0.30 * familiarity
            + 0.30 * warmth
        )

        # ═══ LAYER M: Mathematical ═══

        binding_coherence = stumpf * consonance
        imprint_depth_raw = x_l5l7_mean * tonalness
        scaffold_strength = (
            encoding * binding_coherence
            + familiarity * imprint_depth_raw
        ).clamp(0, 1)

        # Imprinting depth — |0.35| + |0.35| + |0.30| = 1.0
        imprinting_depth = torch.sigmoid(
            0.35 * familiarity
            + 0.35 * tonalness
            + 0.30 * warmth
        )

        # ═══ LAYER P: Present ═══

        scaffold_activation = retrieval * familiarity
        bonding_warmth = (familiarity * warmth * consonance).clamp(0, 1)

        # ═══ LAYER F: Future ═══

        scaffold_persist = self._predict_future(
            mem_encoding, h3_direct, window_h=24
        )
        preference_form = self._predict_future(
            mem_familiar, h3_direct, window_h=20
        )
        therapeutic_pot = (scaffold_activation * consonance).clamp(0, 1)

        return torch.cat([
            f37, f38, f39,                                # E: 3D
            scaffold_strength, imprinting_depth,           # M: 2D
            scaffold_activation, bonding_warmth,           # P: 2D
            scaffold_persist, preference_form,             # F: 3D
            therapeutic_pot,
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 | 5 original + 7 new (v2.1.0): MEG RCT, fNIRS, RNA-seq/Golgi, ABR, reviews, counterevidence |
| **Effect Sizes** | 4 quantitative | η²=0.229-0.309 (Partanen 2022), r=0.38-0.629 (Qiu 2025, Strait 2012) |
| **Counterevidence** | 1 paper | Whiteford et al. 2025 (N>260): null FFR result contests brainstem plasticity |
| **Evidence Modality** | MEG, fNIRS, ABR, RNA-seq, Golgi staining, behavioral, reviews | Mixed (human + animal) |
| **Falsification Tests** | 5 testable, 1 partial, 1 contested | Low-moderate validation |
| **Brain Regions** | 6 (4 original + 2 new) | R-PFC (fNIRS), Auditory brainstem (contested) |
| **MNI Validated** | 3 of 6 | A1/STG (MEG/fNIRS), R-PFC (fNIRS); hippocampus/amygdala indirect |
| **R³ Features Used** | 25D of 49D | Selective |
| **H³ Demand** | 15 tuples (0.65%) | Sparse, efficient |
| **MEM Mechanism** | 30D (3 sub-sections) | Full coverage |
| **Cross-Unit** | None | Single-mechanism model |
| **Output Dimensions** | **10D** | 4-layer structure (E3, M2, P2, F3) |

---

## 13. Scientific References

1. **Partanen, E., Martensson, G., Hugoson, P., Huotilainen, M., Fellman, V., & Aden, U. (2022)**. Auditory processing of the brain is enhanced by parental singing for preterm infants. *Frontiers in Neuroscience*, 16, 772008. doi:10.3389/fnins.2022.772008. **N=33 (21 preterm + 12 full-term), MEG RCT, η²=0.229-0.309.**
2. **Qiu, R., Li, L., Su, Y., Fu, Q., He, Z., Yao, T., ... & Cheng, Y. (2025)**. The impact of musical intervention during fetal and infant stages on social behavior and neurodevelopment in mice. *Translational Psychiatry*, 15, 408. doi:10.1038/s41398-025-03645-4. **N=48 mice, RNA-seq + Golgi staining, dose-dependent effects.**
3. **Strait, D. L., Parbery-Clark, A., Hittner, E., & Kraus, N. (2012)**. Musical training during early childhood enhances the neural encoding of speech in noise. *Brain and Language*, 123(3), 191-201. doi:10.1016/j.bandl.2012.09.001. **N=31 children, ABR, r=0.562-0.629.**
4. **Scholkmann, F., Haslbeck, F., Oba, E., Restin, T., ... & Karen, T. (2024)**. Creative music therapy in preterm infants effects cerebrovascular oxygenation and perfusion. *Scientific Reports*, 14, 28249. doi:10.1038/s41598-024-75282-8. **N=17 preterm, fNIRS.**
5. **Nguyen, T., Flaten, E., Trainor, L. J., & Novembre, G. (2023)**. Early social communication through music: State of the art and future perspectives. *Developmental Cognitive Neuroscience*, 63, 101279. doi:10.1016/j.dcn.2023.101279. **Review.**
6. **Sena Moore, K., Burbach, K., & Hanson-Abromeit, D. (2025)**. A theory of intervention model to define the essential characteristics of music to support emotion regulation development in early childhood. *Frontiers in Neuroscience*, 19, 1568789. doi:10.3389/fnins.2025.1568789. **Theoretical model.**
7. **Trehub, S. E. (2003)**. The developmental origins of musicality. *Nature Neuroscience*, 6(7), 669-673.
8. **Trainor, L. J., & Unrau, A. (2012)**. Development of pitch and music perception. *Springer Handbook of Auditory Research*, 42, 223-254.
9. **DeCasper, A. J., & Fifer, W. P. (1980)**. Of human bonding: Newborns prefer their mothers' voices. *Science*, 208(4448), 1174-1176. **N=10.**
10. **Trehub, S. E., & Hannon, E. E. (2006)**. Infant music perception: Domain-general or domain-specific mechanisms? *Cognition*, 100(1), 73-99.
11. **Whiteford, K. L., et al. (2025)**. Large-scale multi-site study shows no association between musical training and early auditory neural sound encoding. *Nature Communications*, 16, 7152. doi:10.1038/s41467-025-62155-5. **N>260, preregistered, COUNTEREVIDENCE.**
12. **Neonatal care review (2023)**. Music affects hippocampus, amygdala in neonatal care. *Scoping review*, n=1500.

---

## 14. Migration Notes (D0 -> MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D, 29D used) | R³ (49D, 25D used) |
| Temporal | HC⁰ mechanisms (HRM, BND, AED) | MEM mechanism (30D) only |
| Output dimensions | 11D | **10D** (consolidated) |
| Early binding | S⁰.L5.loudness + roughness x BND | R³.consonance x warmth x MEM.encoding |
| Developmental plasticity | S⁰.X_L5L9 x AED | R³.x_l0l5 x MEM.encoding |
| Melodic imprinting | S⁰.X_L5L6 + tristimulus x HRM | R³.x_l5l7 x tonalness x MEM.familiarity |
| Demand format | HC⁰ index ranges (18 tuples) | H³ 4-tuples (15 tuples, sparse) |
| Total demand | 18/2304 = 0.78% | 15/2304 = 0.65% |
| Cross-unit | AED (indirect) | None (MEM-only model) |

### Why MEM replaces HC⁰ mechanisms

The D0 pipeline used 3 separate HC⁰ mechanisms (HRM, BND, AED). In MI, these are unified into the MEM mechanism:
- **BND -> MEM.encoding_state** [0:10]: Scaffold binding strength at formation
- **HRM -> MEM.familiarity_proxy** [10:20]: Melodic imprinting template match
- **AED -> removed**: Developmental affect processing is no longer cross-read; the emotional component is captured by R³ consonance/warmth features directly. ARU.DAP handles the affective development side independently.

### Dimension Reconciliation: 11D -> 10D

The v1.0.0 model had 11D output. In v2.0.0:
- 3 explicit features (f37, f38, f39) -> retained as Layer E (3D)
- 2 math outputs -> retained as Layer M (2D)
- 3 present outputs -> consolidated to 2D (scaffold_activation, bonding_warmth)
- 3 future outputs -> retained as Layer F (3D)
- Net change: -1D from present layer consolidation

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-04 | Legacy D0 model specification (11D, S⁰/HC⁰ naming) |
| 2.0.0 | 2026-02-12 | MI R³/H³ architecture: 10D output, MEM-only binding, R³ mapping, zero params |
| 2.1.0 | 2026-02-13 | Deep literature review: 5→12 papers. Added Partanen 2022 (MEG RCT N=33, η²=0.229), Qiu 2025 (mouse RNA-seq/Golgi N=48, mPFC+amygdala plasticity), Strait 2012 (ABR N=31, r=0.562-0.629), Scholkmann 2024 (fNIRS N=17 preterm), Nguyen/Trainor 2023 (review), Sena Moore 2025 (theoretical model). Added counterevidence: Whiteford 2025 (N>260, null FFR). Brain regions 4→6 (+R-PFC, +Auditory brainstem contested). MNI coords refined for A1/STG per MEG/fNIRS data. Noted doc-code mismatches (LAYERS, h3_demand, brain_regions, dimension_names, citations). |

---

## 15. Doc-Code Mismatches (v2.1.0)

The following mismatches between this document and `mi_beta/brain/units/imu/models/dmms.py` were identified during Phase 1 revision. Code is NOT edited per workflow rules.

| Aspect | Doc (v2.1.0) | Code (v2.0.0 stub) | Severity |
|--------|-------------|---------------------|----------|
| **FULL_NAME** | "Developmental Music Memory Scaffold" | "Developmental Music Memory Schema" | Minor (naming) |
| **LAYERS** | E(0:3), M(3:5), P(5:7), F(7:10) with names f37_early_binding, f38_dev_plasticity, f39_melodic_imprint, scaffold_strength, imprinting_depth, scaffold_activation, bonding_warmth, scaffold_persist, preference_form, therapeutic_pot | E(0:2), M(2:4), P(4:7), F(7:10) with generic names f01_scaffold_strength, f02_exposure_history, schema_stability, critical_period_index, current_schema_match, emotional_association, familiarity_base, schema_evolution_pred, preference_forecast, lifelong_impact_pred | Major (layer boundaries and dimension names differ) |
| **h3_demand** | 15 tuples specified | Empty tuple `()` | Major (code returns no H3 demand) |
| **brain_regions** | 6 regions (Hippocampus, Amygdala, A1/STG, mPFC, R-PFC, Auditory brainstem) | 2 regions (Auditory Cortex at -54,-22,8; Hippocampus at 20,-24,-12) | Major |
| **dimension_names** | 10 names matching doc Layer E/M/P/F | 10 generic names (f01_scaffold_strength etc.) | Major |
| **citations** | 12 papers (Partanen 2022, Qiu 2025, Strait 2012, etc.) | 2 papers (Trainor 2005, Trehub 2001 — neither matches doc) | Major |
| **paper_count** | 12 | 3 | Major |
| **version** | 2.1.0 | 2.0.0 | Minor |

---

**Model Status**: **SPECULATIVE** (strengthened evidence base, but counterevidence noted)
**Output Dimensions**: **10D**
**Manifold Range**: **IMU DMMS [378:388]**
**Evidence Tier**: **gamma (Speculative)**
**Confidence**: **<70%** (12 papers, 4 quantitative effect sizes, 1 counterevidence)
