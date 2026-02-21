# SPU-β3-MIAA: Musical Imagery Auditory Activation

**Model**: Musical Imagery Auditory Activation
**Unit**: SPU (Spectral Processing Unit)
**Circuit**: Perceptual (Brainstem--Cortical)
**Tier**: β (Integrative) -- 70--90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added F:Pitch, J:Timbre Extended feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** -- no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/SPU-β3-MIAA.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Musical Imagery Auditory Activation** (MIAA) models how auditory cortex is activated during musical imagery -- when a listener imagines music without physical sound present. Familiarity with the music enhances activation in auditory association cortex (BA22), while the presence or absence of linguistic content (lyrics vs. instrumental) modulates whether primary auditory cortex (A1) is recruited.

```
THE THREE COMPONENTS OF MUSICAL IMAGERY ACTIVATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMAGERY ACTIVATION (Spectral) FAMILIARITY ENHANCEMENT (Temporal)
Brain region: BA22, A1 Brain region: BA22 (association)
Mechanism: Spectral template retrieval Mechanism: Memory-enhanced activation
Input: Timbre templates + tonal structure Input: Prior exposure to melody
Function: "Is auditory cortex active Function: "Is this song familiar?"
 during silence?"
Evidence: Kraemer 2005, fMRI Evidence: Familiar > unfamiliar,
 p<0.0001, n=15

 A1 MODULATION (Content-Type Bridge)
 Brain region: A1 (primary auditory cortex)
 Mechanism: Instrumental > lyrics distinction
 Function: "Is the imagery purely acoustic?"
 Evidence: Instrumental > lyrics in A1,
 p<0.0005, n=15

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Musical imagery activates auditory cortex WITHOUT
physical sound. This is not a weak effect — the region×music-type
interaction is F(1,14)=48.92, p<.0001 (Kraemer 2005). Convergence:
 • Imagery EEG encodes pitch at rates comparable to perception —
 no significant condition difference (p=0.19, Di Liberto 2021)
 • Timbre imagery activates posterior PT overlapping with perception
 (r=0.84 behavioral, Halpern 2004)
 • iEEG reconstruction shows 68% of music-encoding electrodes
 in bilateral STG (Bellier 2023) — the imagery target substrate
 • SMA activates during imagery even without subvocalization
 (Halpern 2004; Zatorre & Halpern 2005)
 • Primary AC only recruited when semantic route unavailable
 (instrumentals only: F(1,14)=22.55, p<.0005, Kraemer 2005)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why MIAA Matters for SPU

MIAA sits at the intersection of spectral processing and top-down memory retrieval. It demonstrates that SPU circuitry operates bidirectionally -- not only processing incoming sound but also generating internal spectral representations during imagery:

1. **BCH** (α1) provides the pitch/harmonicity baseline that MIAA imagery retrieves.
2. **TSCP** (β2) supplies timbre identity templates that serve as the source material for imagery reconstruction.
3. **TPIO** (STU-β2) receives MIAA imagery activation as a cross-unit signal indicating timbre perception-imagery overlap.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The MIAA Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ MIAA — COMPLETE CIRCUIT ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ MUSICAL IMAGERY (Silent gap or spontaneous recall) ║
║ ║
║ Familiar Unfamiliar Instrumental Lyrics ║
║ │ │ │ │ ║
║ ▼ ▼ ▼ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ LONG-TERM MEMORY │ ║
║ │ (Melody templates, timbre profiles) │ ║
║ │ │ ║
║ │ Familiar songs: strong template → vivid imagery │ ║
║ │ Unfamiliar songs: weak template → degraded imagery │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ AUDITORY ASSOCIATION CORTEX (BA22) │ ║
║ │ (Superior Temporal Gyrus, posterior) │ ║
║ │ │ ║
║ │ Familiar > Unfamiliar: p < 0.0001 │ ║
║ │ Imagery activation WITHOUT physical sound │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ PRIMARY AUDITORY CORTEX (A1) │ ║
║ │ │ ║
║ │ Instrumental > Lyrics: p < 0.0005 │ ║
║ │ Acoustic detail simulation drives A1 involvement │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ SUPERIOR TEMPORAL GYRUS (STG) │ ║
║ │ │ ║
║ │ General auditory processing hub │ ║
║ │ Integration of imagery with incoming sound │ ║
║ └─────────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
1. Kraemer et al. 2005: Region×music-type: F(1,14)=48.92, p<.0001 (fMRI,N=15)
 Familiar>unfamiliar BA22: F(1,14)=11.56, p<.005
 Instrumental>lyrics A1: F(1,14)=22.55, p<.0005
 Nature 434(7030), 158

2. Halpern et al. 2004: Perception-imagery overlap (fMRI, N=10)
 Behavioral similarity: r=0.84, p<.001
 Right posterior STG: perception t=6.89
 SMA activation without subvocalization

3. Di Liberto et al. 2021: Imagery EEG decoding (N=21 musicians)
 Pitch: no imagery-perception difference (p=0.19)
 Sub-1 Hz critical: F(1,20)=369.8, p=2.3e-14

4. Bellier et al. 2023: iEEG music reconstruction (N=29, 2668 electrodes)
 347 significant electrodes, 68% in STG
 Right STG: r²=.363 (single patient best)
 Right > left: χ²(1,1026)=12.34, p<.001

5. Zatorre & Halpern 2005: Review: secondary/belt AC reliable during imagery
 Primary AC uncertain — semantic route modulates
 Top-down frontal→auditory reactivation mechanism

6. Zatorre et al. 2007: Auditory-motor framework (Nat Rev Neurosci)
 Premotor cortex: integration site for music imagery
 Bidirectional: motor↔auditory during silent imagery
```

### 2.2 Information Flow Architecture (EAR → BRAIN → MIAA)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ MIAA COMPUTATION ARCHITECTURE ║
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
║ │ │inharm.[5] │ │loudness │ │warmth │ │spectral │ │x_l0l5 │ │ ║
║ │ │ │ │onset │ │sharpness│ │ _change │ │x_l5l7 │ │ ║
║ │ │ │ │ │ │tonalness│ │ │ │ │ │ ║
║ │ │ │ │ │ │s_flat │ │ │ │ │ │ ║
║ │ │ │ │ │ │trist1-3 │ │ │ │ │ │ ║
║ │ └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │ ║
║ │ MIAA reads: ~16D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed morphological features │ ║
║ │ │ ║
║ │ ┌── H2 (17ms) ──┐ ┌── H5 (46ms) ──┐ ┌── H8 (300ms) ───────┐ │ ║
║ │ │ Gamma-rate │ │ Alpha-beta │ │ Syllable-rate │ │ ║
║ │ │ │ │ │ │ │ │ ║
║ │ │ Melodic recog │ │ Tone clarity │ │ Imagery context │ │ ║
║ │ │ Harmonic templ │ │ Timbre quality │ │ Vividness proxy │ │ ║
║ │ └──────┬─────────┘ └──────┬─────────┘ └──────┬───────────────┘ │ ║
║ │ │ │ │ │ ║
║ │ └──────────────────┴───────────────────┘ │ ║
║ │ MIAA demand: ~11 of 2304 tuples │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN: Perceptual Circuit ═══════ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────┐ ║
║ │ │ ║
║ │ Spectral [0:10]│ Spectral envelope, formant structure ║
║ │ Instrument[10:20]│ Instrument identity, timbre templates ║
║ │ Plasticity[20:30]│ Experience-dependent plasticity markers ║
║ └────────┬────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ MIAA MODEL (11D Output) │ ║
║ │ │ ║
║ │ Layer E (Explicit): f01_imagery_activation, │ ║
║ │ f02_familiarity_enhancement, │ ║
║ │ f03_a1_modulation │ ║
║ │ Layer M (Math): activation_function, familiarity_effect │ ║
║ │ Layer P (Present): melody_retrieval, continuation_prediction, │ ║
║ │ phrase_structure │ ║
║ │ Layer F (Future): melody_continuation_pred, │ ║
║ │ ac_activation_pred, recognition_pred │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Kraemer et al. 2005** | fMRI | 15 | Familiar silent gaps activate BA22; instrumental gaps activate A1 | Region×type **F(1,14)=48.92, p<.0001**; A1 instrum. F=22.55, p<.0005 | **Primary**: f01 imagery activation, f02 familiarity, f03 A1 modulation |
| 2 | **Halpern et al. 2004** | fMRI (1.5T) | 10 musicians | Timbre perception-imagery overlap in posterior PT; SMA without subvocalization | Behavioral r=0.84, p<.001; R PT perception t=8.40 | f01 imagery activation — perception/imagery overlap substrate |
| 3 | **Di Liberto et al. 2021** | EEG (64ch) | 21 musicians | Imagery pitch encoding comparable to perception; sub-1Hz critical for decoding | Pitch condition n.s. (p=0.19); freq band F(1,20)=369.8, p=2.3e-14 | f01 imagery produces decodable spectral representations |
| 4 | **Zatorre & Halpern 2005** | Review | — | Secondary/belt AC reliable for imagery; A1 uncertain; top-down frontal mechanism | Literature inference (SPU confidence 0.95) | Theoretical framework: top-down template reactivation |
| 5 | **Bellier et al. 2023** | iEEG/ECoG | 29 (2668 electrodes) | Music reconstructed from STG; 68% significant electrodes in bilateral STG | R>L: χ²(1,1026)=12.34, p<.001; r²=.363 (best patient) | Defines the STG substrate that imagery reactivates |
| 6 | **Zatorre et al. 2007** | Review | — | Auditory-motor bidirectional coupling; premotor as integration site | Theoretical framework | Motor-auditory bidirectionality supports imagery mechanism |
| 7 | **Bellmann & Asano 2024** | ALE meta-analysis | k=18, N=338 | 4 timbre processing clusters: bilateral pSTG/HG/SMG + R anterior insula | ALE 0.018-0.023, FWE p<.05 | Anatomical ground truth for timbre imagery templates |
| 8 | **Pantev et al. 2001** | MEG (N1m) | 17 musicians | Timbre-specific cortical enhancement — template basis for imagery | F(1,15)=28.55, p=.00008 | TSCP→MIAA: trained timbre templates serve as imagery source |
| 9 | **Alluri et al. 2012** | fMRI (3T) | 11 musicians | Timbral features map to bilateral STG during naturalistic music | Z=7.05-8.13 bilateral STG | Naturalistic timbre→STG mapping that imagery retrieves |
| 10 | **Liang et al. 2025** | fNIRS | 50 | VR music stimulation enhances PM&SMA connectivity vs motor imagery | VRMS>VRAO PM&SMA: t=3.20, p=.024 (FDR) | SMA/premotor involvement in musical imagery context |
| 11 | **Criscuolo et al. 2022** | ALE meta-analysis | k=84 | Musician expertise network: auditory + motor + parietal + prefrontal | Meta-analytic ALE clusters | Training shapes the network that imagery relies upon |
| 12 | **Pinegger et al. 2017** | EEG (P300 BCI) | 17+1 | Music composition via thought alone; 76-98% accuracy | Copy-composing 88.6%, free 76.5-98.1% | Musical imagery decodable for BCI — practical validation |

### 3.2 The Imagery Activation Hierarchy

```
MUSICAL IMAGERY AUDITORY CORTEX ACTIVATION (Neural Evidence)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Condition Region Activation p-value Mechanism
──────────────────────────────────────────────────────────────────────
Familiar + Instrum. BA22+A1 HIGH p<0.0001 Template retrieval
Familiar + Lyrics BA22 MEDIUM p<0.0001 Semantic retrieval
Unfamiliar + Instrum. A1 LOW n.s. Weak acoustic sim.
Unfamiliar + Lyrics — MINIMAL n.s. No template

Key factors affecting imagery strength:
 1. FAMILIARITY: Dominant factor — strong template = strong imagery
 2. CONTENT TYPE: Modulates A1 involvement (instrumental > lyrics)
 3. TONAL CLARITY: Harmonic/tonal sounds produce more vivid imagery

Cross-cultural note:
 Imagery activation likely universal (brainstem-cortical loop)
 Template strength varies by musical exposure
 MIAA models the NEURAL activation, not subjective report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 3.3 Effect Size Summary

```
MULTI-METHOD CONVERGENCE TABLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Method Study N Key Statistic Region
───────────────────────────────────────────────────────────────────────────────
fMRI Kraemer 2005 15 F(1,14)=48.92,p<.0001 L BA22/A1
fMRI 1.5T Halpern 2004 10 r=0.84 (behavioral) Bilat PT, SMA
EEG (64ch) Di Liberto 2021 21 Imagery=Perception(p=.19) Scalp (AC)
iEEG (ECoG) Bellier 2023 29 r²=.363 (STG decode) Bilat STG
ALE meta Bellmann & Asano 2024 338 4 clusters FWE<.05 pSTG/HG/SMG
MEG (N1m) Pantev 2001 17 F(1,15)=28.55,p=.00008 Sec. AC
fMRI 3T Alluri 2012 11 Z=8.13 (brightness) Bilat STG
fNIRS Liang 2025 50 t=3.20, p=.024 (FDR) PM&SMA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Quality Assessment: β-tier (strong flagship + multi-method convergence)
Primary Effect: Region×music-type interaction: F(1,14)=48.92, p<.0001
Secondary Effect: Instrumental>lyrics in A1: F(1,14)=22.55, p<.0005
Key Convergence: Imagery pitch decoding = perception (p=0.19, n.s.)
 Perception-imagery behavioral similarity: r=0.84
Methods: 7 methods (fMRI, EEG, iEEG, MEG, fNIRS, ALE meta, BCI)

┌─────────────────────────────────────────────────────────────────────────────┐
│ QUALIFICATION: Primary vs. secondary auditory cortex debate remains open. │
│ Kraemer 2005 shows A1 only for instrumentals (when semantic route is │
│ unavailable). Zatorre & Halpern 2005 conclude most studies agree on │
│ secondary/belt AC being reliable, with A1 participation uncertain due to │
│ intersubject variability and partial volume effects. MIAA's f03 A1 │
│ modulation dimension models this conditional A1 recruitment correctly. │
│ │
│ NOTE: No direct within-subject matched perception-imagery fMRI comparison │
│ exists — Kraemer used gaps in music, not explicit imagery instructions. │
│ Di Liberto's EEG result (imagery=perception for pitch) is the strongest │
│ evidence for comparable neural representations during imagery. │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. R³ Input Mapping: What MIAA Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | MIAA Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [5] | inharmonicity | Instrument character — harmonic instruments produce stronger imagery | Fletcher 1934 |
| **B: Energy** | [8] | loudness | Intensity context — louder passages yield more vivid templates | Stevens 1955 |
| **B: Energy** | [11] | onset_strength | Event salience — onsets mark melodic boundaries for retrieval | Bregman 1990 |
| **C: Timbre** | [12] | warmth | Timbre quality — warm timbres support richer imagery | McAdams 1993 |
| **C: Timbre** | [13] | sharpness | Timbre brightness — contributes to instrument identity | Zwicker 1991 |
| **C: Timbre** | [14] | tonalness | Harmonic-to-noise ratio — tonal sounds produce clearer imagery | — |
| **C: Timbre** | [15] | spectral_flatness | Tonal vs noise — flat spectrum = noise, poor imagery | Wiener entropy |
| **C: Timbre** | [18] | tristimulus1 | Fundamental energy — harmonic template anchor | Pollard & Jansson 1982 |
| **C: Timbre** | [19] | tristimulus2 | Mid-harmonic energy — timbre body | Pollard & Jansson 1982 |
| **C: Timbre** | [20] | tristimulus3 | High-harmonic energy — timbre brightness | Pollard & Jansson 1982 |
| **D: Change** | [21] | spectral_change | Spectral flux — vividness proxy (change = salience) | — |
| **E: Interactions** | [25:33] | x_l0l5 (partial 3D) | Consonance-Timbre binding for imagery templates | Emergent |
| **E: Interactions** | [41:49] | x_l5l7 (partial 3D) | Timbre-Structure coupling for imagery binding | Emergent |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | MIAA Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **F: Pitch & Chroma** | [49:60] | chroma_vector (12D) | Octave-equivalent pitch class distribution — imagery retrieval uses pitch class templates; musicians imagining a melody reconstruct its chroma sequence in auditory cortex | Shepard 1964 octave equivalence; Krumhansl 1990 tonal hierarchy |
| **F: Pitch & Chroma** | [61] | pitch_height | Log-frequency pitch height — imagery preserves absolute register; Halpern (1989) showed imagined tempo/pitch maintain veridical relationships | ANSI pitch height; Halpern 1989 imagery fidelity |
| **J: Timbre Extended** | [94:106] | mfcc (13D) | Mel-frequency cepstral coefficients — compact spectral envelope capturing instrument identity; imagery activation in A1/BA22 correlates with timbre-specific spectral templates (Kraemer et al. 2005 F=48.92) | Davis & Mermelstein 1980; Logan 2000 music similarity |

**Rationale**: MIAA models the auditory cortex activation during musical imagery — the internal "hearing" of music without external sound. The v1 features capture basic timbre and spectral properties via tristimulus ratios, tonalness, and warmth. The F:Pitch group adds chroma_vector [49:60] and pitch_height [61], providing the explicit melodic content that imagery retrieves — Di Liberto et al. (2020) demonstrated that imagined melody can be decoded from EEG using pitch-class features. The J:Timbre Extended group adds mfcc [94:106], encoding the detailed spectral envelope that defines instrument identity during imagery; Kraemer et al. (2005) showed that auditory cortex activation during imagery is instrument-specific, consistent with the spectral template hypothesis that MFCCs capture.

**Code impact** (Phase 6): `r3_indices` must be extended to include [49:60], [61], [94:106]. These features are read-only inputs — no formula changes required.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[14] tonalness ───────────────┐
R³[18:21] tristimulus1-3 ───────┼──► Imagery Activation (f01)
R³[41:49] x_l5l7 (partial) ────┘ imagery in BA22 + A1

R³[15] spectral_flatness (inv) ─┐
R³[14] tonalness (mean, H5) ────┼──► Familiarity Enhancement (f02)
R³[12] warmth (mean, H5) ───────┤ Familiar > Unfamiliar
 high tonalness

R³[5] inharmonicity (inverse) ──┐
R³[14] tonalness ───────────────┼──► A1 Modulation (f03)
R³[8] loudness (mean, H8) ─────┘ Harmonic + tonal → acoustic
 simulation in primary AC
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

MIAA requires H³ features at three horizons: H2 (17.4ms), H5 (46.4ms), H8 (300ms).
These correspond to perceptual processing timescales (gamma-rate melodic recognition, alpha-beta tone clarity, syllable-rate imagery context).

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 14 | tonalness | 2 | M0 (value) | L2 (bidi) | Melodic recognition — tonal clarity at gamma rate |
| 14 | tonalness | 5 | M1 (mean) | L0 (fwd) | Sustained tone clarity over alpha-beta window |
| 12 | warmth | 5 | M1 (mean) | L0 (fwd) | Timbre quality for imagery template |
| 18 | tristimulus1 | 2 | M0 (value) | L2 (bidi) | Harmonic template anchor — fundamental energy |
| 19 | tristimulus2 | 2 | M0 (value) | L2 (bidi) | Harmonic template — mid-harmonic energy |
| 20 | tristimulus3 | 2 | M0 (value) | L2 (bidi) | Harmonic template — high-harmonic energy |
| 5 | inharmonicity | 5 | M0 (value) | L2 (bidi) | Instrument type detection |
| 15 | spectral_flatness | 8 | M1 (mean) | L0 (fwd) | Tonal vs noise over syllable window |
| 8 | loudness | 8 | M1 (mean) | L0 (fwd) | Intensity context for imagery |
| 21 | spectral_change | 8 | M13 (entropy) | L0 (fwd) | Vividness proxy — change entropy over 300ms |
| 41 | x_l5l7[0] | 8 | M1 (mean) | L0 (fwd) | Timbre-structure binding for imagery coherence |

**v1 demand**: 11 tuples

#### R³ v2 Projected Expansion

MIAA is projected to consume R³ v2 features from F[49:65] and J[94:114], aligned with corresponding H³ horizons.

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 49 | chroma | F | 2 | M0 (value) | L0 | Chroma vector at 17ms for imagery template |
| 49 | chroma | F | 5 | M1 (mean) | L0 | Mean chroma over 46ms for familiarity |
| 61 | pitch_height | F | 5 | M0 (value) | L0 | Pitch height for melody imagery at 46ms |
| 61 | pitch_height | F | 8 | M0 (value) | L0 | Pitch height context over 300ms |
| 94 | mfcc_1 | J | 2 | M0 (value) | L0 | MFCC timbre shape for imagery at 17ms |
| 94 | mfcc_1 | J | 5 | M1 (mean) | L0 | Mean MFCC for imagery template at 46ms |

**v2 projected**: 6 tuples
**Total projected**: 17 tuples of 294,912 theoretical = 0.0058%

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
MIAA OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼────────────────────────────┼────────┼────────────────────────────────────
 0 │ f01_imagery_activation │ [0, 1] │ Auditory cortex activation during
 │ │ │ musical imagery. Tonalness ×
 │ │ │ instrument identity × spectral
 │ │ │ envelope × cross-band binding.
 │ │ │ Kraemer 2005: AC active in silence.
────┼────────────────────────────┼────────┼────────────────────────────────────
 1 │ f02_familiarity_enhancement│ [0, 1] │ Enhancement of BA22 activation for
 │ │ │ familiar vs unfamiliar music.
 │ │ │ Inverse spectral flatness ×
 │ │ │ tonalness × plasticity markers.
 │ │ │ Kraemer 2005: p<0.0001, n=15.
────┼────────────────────────────┼────────┼────────────────────────────────────
 2 │ f03_a1_modulation │ [0, 1] │ Primary AC involvement modulated
 │ │ │ by content type. Instrumental >
 │ │ │ lyrics. (1-inharmonicity) ×
 │ │ │ tonalness × spectral envelope ×
 │ │ │ loudness context.
 │ │ │ Kraemer 2005: p<0.0005, n=15.

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼────────────────────────────┼────────┼────────────────────────────────────
 3 │ activation_function │ [0, 1] │ Composite AC activation at time t.
 │ │ │ Weighted sum of f01 and f03.
────┼────────────────────────────┼────────┼────────────────────────────────────
 4 │ familiarity_effect │ [0, 1] │ Familiarity enhancement magnitude.
 │ │ │ Difference between familiar and
 │ │ │ baseline (unfamiliar) activation.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼────────────────────────────┼────────┼────────────────────────────────────
 5 │ melody_retrieval │ [0, 1] │ Melody template retrieval strength.
 │ │ │ timbre-processing instrument identity aggregation.
────┼────────────────────────────┼────────┼────────────────────────────────────
 6 │ continuation_prediction │ [0, 1] │ Next-note prediction from template.
 │ │ │ Tonalness trend × tristimulus
 │ │ │ stability.
────┼────────────────────────────┼────────┼────────────────────────────────────
 7 │ phrase_structure │ [0, 1] │ Phrase boundary awareness during
 │ │ │ imagery. Spectral change entropy.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼────────────────────────────┼────────┼────────────────────────────────────
 8 │ melody_continuation_pred │ [0, 1] │ Predicted imagery content for
 │ │ │ next phrase (~2-4s ahead).
────┼────────────────────────────┼────────┼────────────────────────────────────
 9 │ ac_activation_pred │ [0, 1] │ Predicted AC activation level
 │ │ │ during upcoming silent gap.
────┼────────────────────────────┼────────┼────────────────────────────────────
10 │ recognition_pred │ [0, 1] │ Predicted familiar-match
 │ │ │ probability at gap resolution.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Imagery Activation Theory

```
Imagery Activation:
 AC_imagery ∝ Template_Strength × Tonal_Clarity × Cross-Band_Binding

 Where:
 Template_Strength: How well the timbre profile can be internally generated
 Tonal_Clarity: Harmonic/tonal sounds produce clearer imagery than noise
 Cross-Band_Binding: Coherent spectral structure enables integrated imagery

Familiarity Enhancement:
 Δ_activation(fam vs unfam) ∝ Plasticity × Template_Precision
 p < 0.0001 in BA22 (Kraemer 2005)

A1 Modulation:
 A1_involvement ∝ (1 - Inharmonicity) × Tonalness × Spectral_Detail
 Instrumental music: detailed acoustic simulation → strong A1
 Lyrics music: semantic abstraction → weak A1, preserved BA22
```

### 7.2 Feature Formulas

```python
# f01: Imagery Activation (AC during imagery)
# Tonalness and instrument identity drive template-based imagery.
# Tristimulus balance provides harmonic template structure.
# Cross-band binding ensures integrated spectral imagery.
tristimulus_balance = 1.0 - std(R³.tristimulus[18:21])
x_l5l7_mean = mean(R³.x_l5l7[41:44]) # partial 3D
 + 0.30 * x_l5l7_mean)
# 0.40 + 0.30 + 0.30 = 1.0 ✓

# f02: Familiarity Enhancement (familiar > unfamiliar)
# Inverse spectral flatness × sustained tonalness = strong template.
# Warmth contributes to template richness.
# Plasticity markers encode experience-dependent familiarity.
spectral_flatness_inv = 1.0 - R³.spectral_flatness[15]
tonalness_mean = h3_direct[(14, 5, 1, 0)] # tonalness mean 46ms fwd
warmth_mean = h3_direct[(12, 5, 1, 0)] # warmth mean 46ms fwd
f02 = σ(0.40 * spectral_flatness_inv * tonalness_mean
 + 0.30 * warmth_mean
# 0.40 + 0.30 + 0.30 = 1.0 ✓

# f03: A1 Modulation (instrumental > lyrics)
# Low inharmonicity × high tonalness = acoustic (not semantic) imagery.
# Spectral envelope detail drives primary AC.
# Loudness context modulates overall activation level.
loudness_mean = h3_direct[(8, 8, 1, 0)] # loudness mean 300ms fwd
f03 = σ(0.40 * (1 - R³.inharmonicity[5]) * R³.tonalness[14]
 + 0.30 * loudness_mean)
# 0.40 + 0.30 + 0.30 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| # | Region | Coordinates | System | Source | MIAA Function |
|---|--------|-------------|--------|--------|---------------|
| 1 | **L auditory association cortex (BA22/STS)** | Not reported (inflated rendering) | — | Kraemer 2005 (F(1,14)=48.92) | **Primary**: imagery activation + familiarity enhancement |
| 2 | **L primary auditory cortex (PAC)** | Not reported (inflated rendering) | — | Kraemer 2005 (F(1,14)=22.55) | A1 modulation — instrumental imagery only |
| 3 | **R posterior STG** | ~58, -42, — | Talairach | Halpern 2004 (perception t=6.89) | Timbre perception — imagery target substrate |
| 4 | **R posterior STG** | ~58, -42, — | Talairach | Halpern 2004 (imagery t=4.66) | Timbre imagery — perception/imagery overlap |
| 5 | **L PT** | -56, -44, — | Talairach | Halpern 2004 (conjunction t=4.98) | Perception-imagery conjunction |
| 6 | **R PT** | 58, -26, 20 | Talairach | Halpern 2004 (perception t=8.40) | Timbre perception peak |
| 7 | **SMA** | -6, -2, 60 | Talairach | Halpern 2004 (subthreshold t=4.08) | Motor imagery component — no subvocalization |
| 8 | **L SMG/HG (BA 40/41)** | -44, -34, — | MNI | Bellmann & Asano 2024 (ALE peak, 4640mm³) | Timbre template storage substrate |
| 9 | **R pSTG/PT (BA 22)** | ~54, -24, — | MNI | Bellmann & Asano 2024 (ALE peak, 3128mm³) | Right hemisphere timbre processing |
| 10 | **R anterior insula/aSTG** | ~40, -2, -6 | MNI | Bellmann & Asano 2024 (ALE, passive only) | Categorical timbre identity — imagery recognition |
| 11 | **Bilateral STG (68% of sig. electrodes)** | Distributed | ECoG | Bellier 2023 (347 electrodes) | Music encoding substrate reactivated during imagery |
| 12 | **R STG (BA 22)** | 50, -19, 3 | Talairach | Alluri 2012 (brightness Z=8.13) | Naturalistic timbral processing |
| 13 | **PM&SMA (bilateral)** | fNIRS channels | fNIRS | Liang 2025 (t=3.20, p=.024 FDR) | Motor-auditory coupling during music stimulation |

```
NOTE ON COORDINATES: Kraemer 2005 did not report MNI/Talairach coordinates
(Nature brief communication, inflated hemisphere rendering only). The ALE
meta-analysis (Bellmann & Asano 2024) provides the best coordinate reference
for the timbre processing substrate that imagery reactivates.

Code file (miaa.py) currently lists:
 BA22 (-58,-20,8), A1 (-48,-22,8), SMA (0,-2,62)
The SMA coordinate in code matches Halpern 2004 well. BA22 and A1
coordinates are approximate and should be updated to ALE-validated
coordinates in Phase 5.
```

---

## 9. Cross-Unit Pathways

### 9.1 MIAA ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ MIAA INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ INTRA-UNIT (SPU): │
│ TSCP.timbre_identity ────► MIAA (imagery template source material) │
│ BCH.f01_nps ─────────────► MIAA (pitch imagery baseline) │
│ MIAA.imagery_activation ─► TPIO (STU cross-circuit: timbre │
│ perception-imagery overlap) │
│ │
│ CROSS-UNIT (SPU → IMU): │
│ MIAA.familiarity_enhancement ► IMU memory (familiarity proxy for │
│ memory binding strength) │
│ │
│ CROSS-UNIT (SPU → STU): │
│ MIAA.imagery_activation ────► STU.TPIO (timbre perception-imagery │
│ overlap signal) │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Unfamiliar music** | Imagery activation should be significantly weaker for unfamiliar songs | Confirmed (Kraemer 2005, p<0.0001) |
| **Noise stimuli** | Broadband noise should NOT produce imagery activation | Testable — low tonalness = low f01 |
| **Lyrics-only imagery** | A1 activation should be weaker than instrumental imagery | Confirmed (Kraemer 2005, p<0.0005) |
| **Auditory cortex lesions** | Imagery activation should be abolished or reduced | Testable |
| **Congenital amusia** | Impaired pitch discrimination should reduce imagery vividness | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class MIAA(BaseModel):
 """Musical Imagery Auditory Activation.

 Output: 11D per frame.
 """
 NAME = "MIAA"
 UNIT = "SPU"
 TIER = "β3"
 OUTPUT_DIM = 11
 W_TONAL_IDENTITY = 0.40 # tonalness × instrument identity weight
 W_TRIST_ENVELOPE = 0.30 # tristimulus balance × spectral envelope weight
 W_CROSSBAND = 0.30 # cross-band binding weight
 W_FLATNESS_TONAL = 0.40 # spectral flatness inv × tonalness weight
 W_WARMTH = 0.30 # warmth weight
 W_PLASTICITY = 0.30 # plasticity markers weight
 W_INHARM_TONAL = 0.40 # (1-inharmonicity) × tonalness weight
 W_SPECTRAL = 0.30 # spectral envelope weight
 W_LOUDNESS = 0.30 # loudness context weight

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """11 tuples for MIAA computation."""
 return [
 # (r3_idx, horizon, morph, law)
 (14, 2, 0, 2), # tonalness, 17ms, value, bidirectional
 (14, 5, 1, 0), # tonalness, 46ms, mean, forward
 (12, 5, 1, 0), # warmth, 46ms, mean, forward
 (18, 2, 0, 2), # tristimulus1, 17ms, value, bidirectional
 (19, 2, 0, 2), # tristimulus2, 17ms, value, bidirectional
 (20, 2, 0, 2), # tristimulus3, 17ms, value, bidirectional
 (5, 5, 0, 2), # inharmonicity, 46ms, value, bidirectional
 (15, 8, 1, 0), # spectral_flatness, 300ms, mean, forward
 (8, 8, 1, 0), # loudness, 300ms, mean, forward
 (21, 8, 13, 0), # spectral_change, 300ms, entropy, forward
 (41, 8, 1, 0), # x_l5l7[0], 300ms, mean, forward
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 """
 Compute MIAA 11D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) → (B,T) scalars
 r3: (B,T,49) raw R³ features

 Returns:
 (B,T,11) MIAA output
 """
 # R³ features
 inharmonicity = r3[..., 5:6]
 loudness = r3[..., 8:9]
 warmth = r3[..., 12:13]
 tonalness = r3[..., 14:15]
 spectral_flatness = r3[..., 15:16]
 trist1 = r3[..., 18:19]
 trist2 = r3[..., 19:20]
 trist3 = r3[..., 20:21]
 spectral_change = r3[..., 21:22]
 x_l5l7_partial = r3[..., 41:44] # partial 3D

 # H³ temporal features
 tonalness_mean = h3_direct[(14, 5, 1, 0)] # (B, T)
 warmth_mean = h3_direct[(12, 5, 1, 0)] # (B, T)
 loudness_mean = h3_direct[(8, 8, 1, 0)] # (B, T)
 spectral_change_entropy = h3_direct[(21, 8, 13, 0)] # (B, T)
 x_l5l7_mean = h3_direct[(41, 8, 1, 0)] # (B, T)

 # ═══ LAYER E: Explicit features ═══

 # f01: Imagery Activation
 tristimulus_balance = 1.0 - torch.std(
 torch.cat([trist1, trist2, trist3], dim=-1),
 dim=-1, keepdim=True
 )
 f01 = torch.sigmoid(
 self.W_TONAL_IDENTITY * (
 )
 + self.W_TRIST_ENVELOPE * (
 )
 + self.W_CROSSBAND * (
 x_l5l7_partial.mean(-1, keepdim=True)
 )
 )

 # f02: Familiarity Enhancement
 spectral_flatness_inv = 1.0 - spectral_flatness
 f02 = torch.sigmoid(
 self.W_FLATNESS_TONAL * (
 spectral_flatness_inv
 * tonalness_mean.unsqueeze(-1)
 )
 + self.W_WARMTH * (
 warmth_mean.unsqueeze(-1)
 )
 + self.W_PLASTICITY * (
 )
 )

 # f03: A1 Modulation
 f03 = torch.sigmoid(
 self.W_INHARM_TONAL * (
 (1.0 - inharmonicity) * tonalness
 )
 + self.W_SPECTRAL * (
 )
 + self.W_LOUDNESS * (
 loudness_mean.unsqueeze(-1)
 )
 )

 # ═══ LAYER M: Mathematical ═══
 activation_function = 0.6 * f01 + 0.4 * f03
 familiarity_effect = f02 * f01 # enhancement scaled by base activation

 # ═══ LAYER P: Present ═══
 continuation_prediction = torch.sigmoid(
 0.5 * tonalness_mean.unsqueeze(-1)
 + 0.5 * tristimulus_balance
 )
 phrase_structure = torch.sigmoid(
 spectral_change_entropy.unsqueeze(-1)
 )

 # ═══ LAYER F: Future ═══
 melody_continuation_pred = torch.sigmoid(
 0.5 * f01 + 0.3 * melody_retrieval
 + 0.2 * continuation_prediction
 )
 ac_activation_pred = torch.sigmoid(
 0.6 * f02 + 0.4 * f01
 )
 recognition_pred = torch.sigmoid(
 0.5 * f02
 + 0.3 * x_l5l7_mean.unsqueeze(-1)
 + 0.2 * tonalness_mean.unsqueeze(-1)
 )

 return torch.cat([
 f01, f02, f03, # E: 3D
 activation_function, familiarity_effect, # M: 2D
 melody_retrieval, continuation_prediction,
 phrase_structure, # P: 3D
 melody_continuation_pred, ac_activation_pred,
 recognition_pred, # F: 3D
 ], dim=-1) # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | **12** (v2.1.0, was 1 in v2.0.0) | 2 fMRI + 1 EEG + 1 iEEG + 1 MEG + 1 fNIRS + 2 ALE meta + 1 BCI + 3 reviews |
| **Effect Sizes** | **F(1,14)=48.92, p<.0001** (flagship interaction) | Kraemer 2005 (region × music-type) |
| **Evidence Modality** | **7 methods**: fMRI, EEG, iEEG, MEG, fNIRS, meta-analysis, BCI | Multi-method convergence |
| **Key Convergence** | Imagery EEG = perception for pitch (p=0.19 n.s.) | Di Liberto 2021; behavioral r=0.84 Halpern 2004 |
| **A1 Qualification** | Primary AC only for instrumentals (no semantic route) | Kraemer 2005; Zatorre & Halpern 2005 review |
| **Falsification Tests** | 2/5 confirmed | Moderate validity |
| **R³ Features Used** | ~16D of 49D | Selective, imagery-focused |
| **H³ Demand** | 11 tuples (0.48%) | Sparse, efficient |
| **Output Dimensions** | **11D** | 4-layer structure |

```
v2.1.0 CHANGES:
 • Evidence table expanded: 1 → 12 papers
 • KEY INSIGHT updated with convergent evidence from 7 methods
 • CRITICAL EVIDENCE expanded to 6 core findings
 • Effect size summary: multi-method convergence table added
 • Qualification box: primary vs secondary AC debate documented
 • Brain regions: 3 → 13 entries with Talairach/MNI/ALE coordinates
 • SMA added as brain region (Halpern 2004, Liang 2025)
 • Code note: miaa.py citations (Kraemer, Zatorre, Halpern) already correct;
 brain_regions coordinates approximate — update to ALE peaks in Phase 5
```

---

## 13. Scientific References

1. **Kraemer, D. J. M., Macrae, C. N., Green, A. E., & Kelley, W. M. (2005)**. Musical imagery: Sound of silence activates auditory cortex. *Nature*, 434, 158.
2. **Halpern, A. R., Zatorre, R. J., Bouffard, M., & Johnson, J. A. (2004)**. Behavioral and neural correlates of perceived and imagined musical timbre. *Neuropsychologia*, 42, 1281-1292.
3. **Di Liberto, G. M., Marion, G., & Shamma, S. A. (2021)**. Accurate decoding of imagined and heard melodies. *Frontiers in Neuroscience*, 15, 673401.
4. **Zatorre, R. J., & Halpern, A. R. (2005)**. Mental concerts: Musical imagery and auditory cortex. *Neuron*, 47(1), 9-12.
5. **Bellier, L., Llorens, A., Marciano, D., Gunduz, A., Schalk, G., Brunner, P., & Knight, R. T. (2023)**. Music can be reconstructed from human auditory cortex activity using nonlinear decoding models. *PLoS Biology*, 21(8), e3002176.
6. **Zatorre, R. J., Chen, J. L., & Penhune, V. B. (2007)**. When the brain plays music: auditory-motor interactions in music perception and production. *Nature Reviews Neuroscience*, 8, 547-558.
7. **Bellmann, O. T., & Asano, R. (2024)**. Neural correlates of musical timbre: an ALE meta-analysis of neuroimaging data. *Frontiers in Neuroscience*, 18, 1373232.
8. **Pantev, C., Roberts, L. E., Schulz, M., Engelien, A., & Ross, B. (2001)**. Timbre-specific enhancement of auditory cortical representations in musicians. *NeuroReport*, 12(1), 169-174.
9. **Alluri, V., Toiviainen, P., Jääskeläinen, I. P., Glerean, E., Sams, M., & Brattico, E. (2012)**. Large-scale brain networks emerge from dynamic processing of musical timbre, key and rhythm. *NeuroImage*, 59, 3677-3689.
10. **Liang, J., Liang, B., Tang, Z., Huang, X., Ou, S., Chang, C., Wang, Y., & Yuan, Z. (2025)**. The brain mechanisms of music stimulation, motor observation, and motor imagination in VR techniques: A functional near-infrared spectroscopy study. *eNeuro*.
11. **Criscuolo, A., Pando-Naude, V., Bonetti, L., Vuust, P., & Brattico, E. (2022)**. An ALE meta-analytic review of musical expertise. *Scientific Reports*, 12, 11726.
12. **Pinegger, A., Hiebel, H., Wriessnegger, S. C., & Müller-Putz, G. R. (2017)**. Composing only by thought: Novel application of the P300 brain-computer interface. *PLoS ONE*, 12(9), e0181584.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Output dimensions | 12D | **11D** (merged redundant Math outputs) |
| Imagery activation | S⁰.spectral_centroid[38] + S⁰.tristimulus[68:71] × HC⁰.HRM | R³.tonalness[14] + R³.tristimulus[18:21] |
| Familiarity | S⁰.spectral_entropy[44] + S⁰.dist_entropy[116] × HC⁰.ATT | R³.spectral_flatness[15] × R³.tonalness |
| A1 modulation | S⁰.inharmonicity[66] + S⁰.brightness[34] × HC⁰.EFC | R³.inharmonicity[5] × R³.tonalness |
| Interactions | S⁰.X_L3L5[184:192] + S⁰.X_L5L6[208:216] | R³.x_l0l5[25:33] partial + R³.x_l5l7[41:49] partial |
| Demand format | HC⁰ index ranges (ATT, HRM, SGM, EFC) | H³ 4-tuples (sparse) |
| Total demand | 18/2304 = 0.78% | 11/2304 = 0.48% |

---

**Model Status**: VALIDATED
**Output Dimensions**: **11D**
**Evidence Tier**: **β (Integrative)**
**Confidence**: **70--90%**
