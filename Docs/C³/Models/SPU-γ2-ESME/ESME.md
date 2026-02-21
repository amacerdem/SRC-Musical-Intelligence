# SPU-γ2-ESME: Expertise-Specific MMN Enhancement

**Model**: Expertise-Specific MMN Enhancement
**Unit**: SPU (Spectral Processing Unit)
**Circuit**: Perceptual (Brainstem-Cortical)
**Tier**: γ (Speculative) — <70% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added F:Pitch, J:Timbre Extended feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/SPU-γ2-ESME.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Expertise-Specific MMN Enhancement** (ESME) models how mismatch negativity (MMN) amplitude reflects trained musical instrument expertise. Musicians with different specializations show selectively enhanced MMN responses for their domain of expertise: singers show enhanced pitch MMN, drummers show enhanced rhythm MMN, and instrumentalists show enhanced timbre MMN. This dissociation reveals that long-term musical training reshapes pre-attentive auditory processing in an expertise-specific manner.

```
EXPERTISE-SPECIFIC MMN ENHANCEMENT — CONVERGENT EVIDENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PITCH MMN (Violinists/Singers) RHYTHM MMN (Jazz/Drummers)
Brain region: Auditory Cortex Brain region: Auditory Cortex
Mechanism: Pitch deviance detection Mechanism: Temporal deviance detection
Input: Pitch change velocity Input: Onset timing deviation
Evidence: Koelsch 1999 — violinists Evidence: Vuust 2012 — jazz > rock
detect 0.75% pitch deviants; for complex rhythmic deviants;
MMN absent in non-musicians Liao 2024 — percussionists recruit
 distinct NMR network

 GENRE-SPECIFIC GRADIENT (Vuust 2012)
 Jazz > Rock > Pop > Non-musicians
 "Sound parameters most important in performance
 evoke the largest MMN" (Tervaniemi 2022 review)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: MMN amplitude is enhanced in a DOMAIN-SPECIFIC manner
by musical training, but the pattern is a GRADIENT — not a clean
dissociation. The strongest enhancement occurs for features most
relevant to the trained instrument/genre (Tervaniemi 2022 review;
Vuust 2012). Cross-domain enhancement also exists (all musicians
show some general enhancement over non-musicians: Criscuolo 2022
ALE, k=84, N=3005).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────────────┐
│ ⚠ CRITICAL CORRECTION (v2.1.0): │
│ v2.0.0 attributed d = -1.09 to "Tervaniemi et al. 2022" but │
│ that paper is a paradigm REVIEW (Frontiers in Neuroscience, │
│ 16, 1025763) — it does NOT report original effect sizes. │
│ The d=-1.09 was UNVERIFIABLE and has been REMOVED. │
│ │
│ Verified effects: Koelsch 1999 (MMN presence/absence for │
│ 0.75% pitch deviants); Vuust 2012 (genre differentiation); │
│ Wagner 2018 (MMN -0.34 µV for harmonic interval deviants). │
│ │
│ ⚠ CONSTRAINT (v2.1.0): Martins et al. 2022 (N=58) found │
│ NO singer vs instrumentalist difference in P2/P3/LPP for │
│ musical vs vocal sounds. The clean 3-way dissociation │
│ (singers=pitch, drummers=rhythm, instrumentalists=timbre) │
│ is an OVERSIMPLIFICATION. The actual pattern is a gradient. │
└─────────────────────────────────────────────────────────────────┘
```

### 1.1 Why This Model Is Important for SPU

ESME builds on the universal deviance detection mechanisms established by lower-tier SPU models and adds an expertise-dependent modulation layer:

1. **BCH** (α1) provides the brainstem consonance baseline that ESME uses as a pitch reference for detecting pitch deviants.
2. **TSCP** (β2) establishes timbre-specific cortical plasticity mechanisms that ESME leverages for expertise-dependent timbre enhancement.
3. **SDED** (γ3) models universal early spectral deviance detection; ESME extends this with expertise-specific amplification of those detection signals.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The ESME Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ ESME — COMPLETE CIRCUIT ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ AUDITORY ODDBALL (Standard → Deviant) ║
║ ║
║ Pitch Deviant Rhythm Deviant Timbre Deviant ║
║ │ │ │ ║
║ ▼ ▼ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ AUDITORY CORTEX │ ║
║ │ (Primary generators of MMN) │ ║
║ │ │ ║
║ │ Standard template formation (repetition suppression) │ ║
║ │ Deviant detection (prediction error signal) │ ║
║ │ MMN amplitude ∝ |deviant - template| │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ PLANUM TEMPORALE │ ║
║ │ (Expertise-modulated processing) │ ║
║ │ │ ║
║ │ Singers: Enhanced pitch MMN (trained vocal control) │ ║
║ │ Drummers: Enhanced rhythm MMN (temporal precision) │ ║
║ │ Instrumentalists: Enhanced timbre MMN (spectral discrimination) │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ FRONTAL MMN SOURCES │ ║
║ │ │ ║
║ │ Deviance evaluation and attention switching │ ║
║ │ Expertise enhancement modulates frontal response │ ║
║ └─────────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE (12 papers, 8 methods):
─────────────────────────────────────────
Koelsch et al. 1999: Violinists: MMN to 0.75% pitch deviants (absent in NM)
Vuust et al. 2012: Genre-specific: jazz > rock > pop > NM (multi-feature)
Tervaniemi 2022 review: "Parameters most important in performance → largest MMN"
Wagner et al. 2018: Pre-attentive harmonic interval MMN: -0.34 µV, 173ms
Criscuolo et al. 2022: ALE meta k=84: bilateral STG + L IFG (BA44) in musicians
Koelsch ~2009: ERAN generators: inferior BA44 bilateral, 150-250ms
Martins et al. 2022: CONSTRAINT: no singer/instrumentalist P2/P3 difference
Mischler et al. 2025: Musicians: left-hemisphere enhanced contextual encoding
```

### 2.2 Information Flow Architecture (EAR → BRAIN → H³ direct → ESME)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ ESME COMPUTATION ARCHITECTURE ║
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
║ │ │sethares │ │loudness │ │tristim. │ │ener_chg │ │x_l4l5 │ │ ║
║ │ │helmholtz │ │onset │ │tonalness│ │pitch_chg │ │x_l5l7 │ │ ║
║ │ │stumpf │ │ │ │ │ │timbr_chg │ │ │ │ ║
║ │ │pleasant. │ │ │ │ │ │ │ │ │ │ ║
║ │ │inharm. │ │ │ │ │ │ │ │ │ │ ║
║ │ │harm_dev │ │ │ │ │ │ │ │ │ │ ║
║ │ └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │ ║
║ │ ESME reads: ~20D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed morphological features │ ║
║ │ │ ║
║ │ ┌── Gamma ────┐ ┌── Alpha-Beta ─┐ ┌── Syllable ──────────┐ │ ║
║ │ │ 17ms (H2) │ │ 100ms (H3) │ │ 300ms (H8) │ │ ║
║ │ │ │ │ │ │ │ │ ║
║ │ │ Timbre │ │ Deviance │ │ Deviant magnitude │ │ ║
║ │ │ instant │ │ template │ │ sustained evaluation │ │ ║
║ │ └──────┬───────┘ └──────┬────────┘ └──────┬────────────────┘ │ ║
║ │ │ │ │ │ ║
║ │ └───────────────┴──────────────────┘ │ ║
║ │ ESME demand: ~12 of 2304 tuples │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN: Perceptual Circuit ═══════ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────┐ ┌─────────────────┐ ║
║ │ │ │ │ ║
║ │ Pitch Sal [0:10]│ │ Spec Env [0:10]│ ║
║ │ Consonance[10:20]│ │ Inst ID [10:20]│ ║
║ │ Chroma [20:30]│ │ Plastic [20:30]│ ║
║ └────────┬────────┘ └────────┬────────┘ ║
║ │ │ ║
║ └────────┬───────────┘ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ ESME MODEL (11D Output) │ ║
║ │ │ ║
║ │ Layer E (Explicit): f01_pitch_mmn, f02_rhythm_mmn, │ ║
║ │ f03_timbre_mmn, f04_expertise_enhancement │ ║
║ │ Layer M (Math): mmn_expertise_function │ ║
║ │ Layer P (Present): pitch_deviance_detection, │ ║
║ │ rhythm_deviance_detection, │ ║
║ │ timbre_deviance_detection │ ║
║ │ Layer F (Future): feature_enhancement_pred, │ ║
║ │ expertise_transfer_pred, │ ║
║ │ developmental_trajectory │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Koelsch, Schröger & Tervaniemi 1999** | EEG (MMN) | ~20/group | Violinists: MMN to 0.75% pitch deviants in major chord triads; MMN absent in non-musicians | Qualitative: presence/absence | **Primary evidence**: expertise-specific pitch MMN |
| 2 | **Vuust, Brattico, Seppänen, Näätänen & Tervaniemi 2012** | EEG (MMN) | ~40-60 | Musical multi-feature paradigm: genre-specific MMN differentiation. Jazz > rock > pop > non-musicians for complex deviants | Genre × deviant interaction | **Primary evidence**: genre-specific gradient |
| 3 | **Tervaniemi 2022** | Review | — | "Sound parameters most important in performance evoke largest MMN." Paradigm overview: multi-feature, melodic, chord paradigms. Gradual feature-specific emergence during training (ages 9-13) | Review (no original effect sizes) | **Principle**: domain-specific enhancement gradient |
| 4 | **Yu, Liu & Gao 2015** | Review | — | Comprehensive MMN-music review: musicians show larger MMN to pitch, rhythm, timbre, harmony deviants. MMN peaks 100-200ms, amplitude varies with deviance magnitude | Review (synthesizes multiple studies) | **Convergence**: MMN as expertise indicator |
| 5 | **Wagner, Rahne, Plontke & Heidekrüger 2018** | EEG (MMN) | 15 | Pre-attentive harmonic interval discrimination: major third MMN = -0.34 µV ± 0.32 at 173ms (p=0.003); perfect fifth MMN = -0.02 µV (n.s.) | MMN = -0.34 µV (major 3rd) | **Baseline**: harmonic deviance in non-musicians |
| 6 | **Koelsch ~2009** | Review (ERP/fMRI) | — | ERAN: 150-250ms, right anterior. Generators: bilateral inferior BA44, ventrolateral premotor cortex, anterior STG. Larger ERAN in musicians. ERAN reflects long-term memory; MMN reflects online processing | ERAN amplitude difference: M > NM | **ERAN generators**: IFG (BA44) as frontal source |
| 7 | **Criscuolo, Pando-Naude, Bonetti, Vuust & Brattico 2022** | ALE meta-analysis | 3005 (k=84) | Musicians > NM: structural — bilateral STG (BA41), HG, PT; functional — L IFG (BA44, BA9), bilateral STG (BA22). Cortico-subcortical sensorimotor + limbic network | ALE Z=4.8 (L STG), Z=5.0 (L IFG) | **ALE validation**: auditory cortex + IFG network |
| 8 | **Martins, Lima & Pinheiro 2022** | EEG (ERP) | 58 | Musicians: enhanced P2, P3, LPP for musical (vs vocal) sounds. BUT: no singer vs instrumentalist difference for vocal vs musical processing | P2/P3/LPP enhancement (M > NM) | **CONSTRAINT**: no instrument-type dissociation for salience |
| 9 | **Bonetti, Fernández-Rubio et al. 2024** | MEG | 83 | Hierarchical auditory memory: AC → hippocampus → cingulate. Alpha/beta stronger for variations; gamma enhanced for memorized sequences | H(4) = 36.38, p<0.001 (accuracy) | **Hierarchy**: prediction error propagation path |
| 10 | **Bücher, Bernhofs, Thieme, Christiner & Schneider 2023** | MEG | 162 | OFC co-activation timing: musicians synchronous with P1; non-musicians 25-40ms later. HG 130% larger in professional musicians | P1-OFC latency: 25-40ms faster (M) | **Timing**: earlier orbitofrontal co-activation in musicians |
| 11 | **Mischler, Li, Bickel, Mehta & Mesgarani 2025** | EEG + iEEG | 20 + 6 | Musicians: deeper transformer layers more predictive of neural responses. Left hemisphere enhanced contextual encoding. Anatomical gradient from A1 outward | Prediction accuracy: M > NM in deep layers | **Gradient**: expertise enhances hierarchical encoding |
| 12 | **Liao, Yang, Yu et al. 2024** | fMRI | 25 | Percussionists: NMR network (putamen, GP, IFG, IPL, SMA). Structural vs free improvisation engage distinct pathways | Network identification (not M vs NM) | **Percussionist network**: basal ganglia + IFG |

### 3.2 The Expertise-MMN Gradient

```
EXPERTISE-SPECIFIC MMN ENHANCEMENT (Convergent Evidence)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Training Profile Best-Domain MMN General MMN Source
──────────────────────────────────────────────────────────────
Violinists ★★★ Pitch (0.75%) ★★ Enhanced Koelsch 1999
Jazz musicians ★★★ Complex harm ★★ Enhanced Vuust 2012
Rock musicians ★★ Moderate ★★ Enhanced Vuust 2012
Pop musicians ★ Slight ★ Some Vuust 2012
Percussionists ★★★ Rhythm/timing ★★ Enhanced Liao 2024
Non-musicians ★ baseline ★ baseline Multiple

Key Principle (Tervaniemi 2022 review):
 "Sound parameters most important in performance evoke largest MMN"
 This is a GRADIENT — not a clean dissociation
 Pre-attentive processing — occurs WITHOUT conscious attention

Constraint (Martins et al. 2022, N=58):
 Singers vs instrumentalists showed NO difference in P2/P3/LPP
 for musical vs vocal sounds — clean instrument-type dissociation
 is NOT supported at the salience detection level.

Cross-domain note:
 All musicians show SOME enhancement over non-musicians
 ALE meta (Criscuolo 2022, k=84): bilateral STG + L IFG (BA44)
 The LARGEST enhancement is in the trained domain/genre
```

### 3.3 Effect Size Summary

```
┌────────────────────────────────────────────────────────────────┐
│ ⚠ NOTE: v2.0.0 reported d = -1.09 from "Tervaniemi 2022" │
│ but that paper is a REVIEW — no original effect sizes. │
│ The d = -1.09 has been REMOVED as unverifiable. │
└────────────────────────────────────────────────────────────────┘

MULTI-METHOD CONVERGENCE TABLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Method Study N Key Effect
──────────────────────────────────────────────────────────────────
EEG (MMN) Koelsch 1999 ~20/grp MMN presence/absence for 0.75% pitch
EEG (MMN) Vuust 2012 ~40-60 Genre × deviant interaction
EEG (MMN) Wagner 2018 15 -0.34 µV (major 3rd, 173ms, p=0.003)
EEG (ERP) Martins 2022 58 P2/P3/LPP: M > NM (no type difference)
EEG (ERP) Zhang 2015 28 P2: 5.91 vs 3.29 µV, p=0.01
EEG + iEEG Mischler 2025 26 Left-hemisphere enhanced encoding (M)
MEG Bonetti 2024 83 AC→Hipp→ACC hierarchy, H(4)=36.38
MEG Bücher 2023 162 P1-OFC: 25-40ms faster in musicians
fMRI Liao 2024 25 Percussionist NMR network
ALE meta Criscuolo 2022 3005 STG Z=4.8, IFG Z=5.0 (k=84)
Review Tervaniemi 2022 — Domain-specific gradient principle
Review Yu et al. 2015 — MMN as expertise indicator

Methods: 8 (EEG-MMN, EEG-ERP, EEG+iEEG, MEG×2, fMRI, ALE meta, review×2)
Total unique participants: >3,400

Quality Assessment: γ-tier (convergent evidence across methods,
 but no single study demonstrates clean 3-way
 dissociation with verified effect sizes)
Replication: Koelsch 1999 violinist effect supported by
 Vuust 2012 genre-specific findings
Cross-cultural: Tested primarily in Western musical tradition
```

---

## 4. R³ Input Mapping: What ESME Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | ESME Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Dissonance baseline for pitch deviance | Plomp & Levelt 1965 |
| **A: Consonance** | [2] | helmholtz_kang | Consonance deviance baseline | Helmholtz 1863, Kang 2009 |
| **A: Consonance** | [3] | stumpf_fusion | Tonal fusion reference | Stumpf 1890 |
| **A: Consonance** | [4] | sensory_pleasantness | Spectral regularity proxy | Sethares 2005 |
| **B: Energy** | [11] | onset_strength | Rhythm deviance (onset timing) | — |
| **C: Timbre** | [12] | warmth | Timbre deviance baseline | — |
| **C: Timbre** | [14] | tonalness | Harmonic-to-noise (pitch clarity) | — |
| **C: Timbre** | [18] | tristimulus1 | Fundamental strength (F0 energy) | Pollard & Jansson 1982 |
| **C: Timbre** | [19] | tristimulus2 | 2nd-4th harmonic energy (mid) | Pollard & Jansson 1982 |
| **C: Timbre** | [20] | tristimulus3 | 5th+ harmonic energy (high) | Pollard & Jansson 1982 |
| **D: Change** | [21] | spectral_change | Spectral flux (deviance signal) | — |
| **D: Change** | [22] | energy_change | Energy flux (rhythm deviance) | — |
| **D: Change** | [23] | pitch_change | Pitch flux (pitch deviance) | — |
| **E: Interactions** | [33:41] | x_l4l5 (4D) | Temporal-spectral coupling | Emergent deviance |
| **E: Interactions** | [41:49] | x_l5l7 (3D) | Consonance-timbre coupling | Emergent deviance |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | ESME Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **F: Pitch & Chroma** | [49:60] | chroma_vector (12D) | Octave-equivalent pitch class distribution — MMN for pitch deviants requires a pitch class template against which deviations are detected; chroma encodes the expected pitch classes in the regularity representation | Shepard 1964 octave equivalence; Krumhansl 1990 tonal hierarchy |
| **J: Timbre Extended** | [107:113] | spectral_contrast (7D) | Peak-valley ratio per frequency band — timbre MMN requires a spectral template; spectral_contrast encodes the formant structure that defines instrument identity, enabling detection of timbre deviants (e.g., violin replaced by trumpet) | Jiang et al. 2002 spectral contrast features |

**Rationale**: ESME models expertise-specific MMN enhancement — the larger mismatch negativity responses that musicians show to deviants in their trained domain. The v1 features capture deviance through change signals (spectral_change, energy_change, pitch_change) and consonance baselines. The F:Pitch group adds chroma_vector [49:60], providing the explicit pitch class template against which pitch deviants are detected — Koelsch et al. (1999) demonstrated that violinists show enhanced MMN to mistuned notes, requiring a pitch class reference that chroma encodes directly. The J:Timbre Extended group adds spectral_contrast [107:113], encoding the formant structure that defines instrument-specific timbre templates; Vuust et al. (2012) showed that genre-specific expertise enhances MMN for instrument-relevant timbral deviants, consistent with spectral contrast capturing the per-band structure that distinguishes familiar vs novel instrument timbres.

**Code impact** (Phase 6): `r3_indices` must be extended to include [49:60], [107:113]. These features are read-only inputs — no formula changes required.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[2] helmholtz_kang ───────────┐
R³[3] stumpf_fusion ────────────┼──► Pitch Deviance Detection
R³[23] pitch_change ────────────┤ Deviation from consonance template
R³[4] sensory_pleasantness ─────┘ Math: |pitch_change_vel|

R³[11] onset_strength ──────────┐
R³[22] energy_change ───────────┼──► Rhythm Deviance Detection
R³[21] spectral_change ─────────┤ Onset timing deviation
R³[33:37] x_l4l5 ──────────────┘ Math: |onset_deviation|

R³[12] warmth ──────────────────┐
R³[18] tristimulus1 ────────────┤
R³[19] tristimulus2 ────────────┼──► Timbre Deviance Detection
R³[20] tristimulus3 ────────────┤ Spectral envelope change
R³[14] tonalness ───────────────┘ Math: timbre_change_std

R³[0] roughness ────────────────── Baseline Dissonance Reference
 For normalizing pitch deviants
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

ESME requires H³ features at these horizons (H0, H3, H6) and Timbre processing horizons (H2, H5, H8).
These correspond to timbre instantaneous processing (gamma), deviance template building (alpha-beta), and sustained deviant magnitude evaluation.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 2 | helmholtz_kang | 0 | M0 (value) | L2 (bidi) | Consonance deviance baseline |
| 2 | helmholtz_kang | 3 | M1 (mean) | L2 (bidi) | Standard template |
| 23 | pitch_change | 3 | M8 (velocity) | L0 (fwd) | Pitch deviant detection |
| 12 | warmth | 2 | M0 (value) | L2 (bidi) | Timbre instantaneous |
| 14 | tonalness | 5 | M1 (mean) | L0 (fwd) | Tonalness template |
| 18 | tristimulus1 | 2 | M0 (value) | L2 (bidi) | F0 energy instantaneous |
| 19 | tristimulus2 | 2 | M0 (value) | L2 (bidi) | Mid-harmonic instantaneous |
| 20 | tristimulus3 | 2 | M0 (value) | L2 (bidi) | High-harmonic instantaneous |
| 24 | timbre_change | 8 | M3 (std) | L0 (fwd) | Timbre deviant magnitude |
| 11 | onset_strength | 3 | M0 (value) | L0 (fwd) | Rhythm deviance |
| 21 | spectral_change | 3 | M8 (velocity) | L0 (fwd) | Spectral deviance velocity |
| 33 | x_l4l5[0] | 8 | M0 (value) | L2 (bidi) | Temporal deviance |

**v1 demand**: 12 tuples

#### R³ v2 Projected Expansion

Minor v2 expansion for ESME from F[49:65] and J[94:114].

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 49 | chroma | F | 3 | M0 (value) | L2 | Chroma deviance baseline at 100ms |
| 107 | spectral_contrast_1 | J | 5 | M0 (value) | L2 | Spectral contrast for timbre deviance at 46ms |

**v2 projected**: 2 tuples
**Total projected**: 14 tuples of 294,912 theoretical = 0.0047%

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
ESME OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────────────┼────────┼────────────────────────────────────
 0 │ f01_pitch_mmn │ [0, 1] │ Pitch MMN amplitude. Enhanced in
 │ │ │ singers. Pitch deviance detection
 │ │ │ strength weighted by pitch-processing pitch
 │ │ │ salience.
 │ │ │ f01 = σ(0.40 · |pitch_change_vel|
 │ │ │ + 0.30 · |helmholtz_diff|
 │ │ │ + 0.30 · onset_val)
────┼───────────────────────────┼────────┼────────────────────────────────────
 1 │ f02_rhythm_mmn │ [0, 1] │ Rhythm MMN amplitude. Enhanced in
 │ │ │ drummers. Onset timing deviation
 │ │ │ weighted by timbre-processing spectral envelope.
 │ │ │ f02 = σ(0.40 · |onset_deviation|
 │ │ │ + 0.30 · spec_change_vel
 │ │ │ + 0.30 · x_l4l5_mean)
────┼───────────────────────────┼────────┼────────────────────────────────────
 2 │ f03_timbre_mmn │ [0, 1] │ Timbre MMN amplitude. Enhanced for
 │ │ │ trained instrument. Spectral
 │ │ │ envelope change weighted by timbre-processing
 │ │ │ instrument identity.
 │ │ │ f03 = σ(0.40 · timbre_change_std
 │ │ │ + 0.30 · tristimulus_deviation
────┼───────────────────────────┼────────┼────────────────────────────────────
 3 │ f04_expertise_enhancement │ [0, 1] │ Expertise Enhancement modulation.
 │ │ │ α = trainable (domain-specific).
 │ │ │ f04 = σ(α · max(f01, f02, f03)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────────────┼────────┼────────────────────────────────────
 4 │ mmn_expertise_function │ [0, 1] │ Unified MMN-expertise function.
 │ │ │ Models the interaction between
 │ │ │ deviance magnitude and expertise
 │ │ │ modulation across all three domains.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────────────┼────────┼────────────────────────────────────
 5 │ pitch_deviance_detection │ [0, 1] │ Current pitch deviance signal.
 │ │ │ |current_pitch - template_pitch|
────┼───────────────────────────┼────────┼────────────────────────────────────
 6 │ rhythm_deviance_detection │ [0, 1] │ Current rhythm deviance signal.
 │ │ │ |current_onset - expected_onset|
────┼───────────────────────────┼────────┼────────────────────────────────────
 7 │ timbre_deviance_detection │ [0, 1] │ Current timbre deviance signal.
 │ │ │ |current_envelope - template_env|

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────────────┼────────┼────────────────────────────────────
 8 │ feature_enhancement_pred │ [0, 1] │ Predicted MMN enhancement level
 │ │ │ for upcoming features.
────┼───────────────────────────┼────────┼────────────────────────────────────
 9 │ expertise_transfer_pred │ [0, 1] │ Cross-domain transfer prediction.
 │ │ │ How much expertise in one domain
 │ │ │ transfers to another.
────┼───────────────────────────┼────────┼────────────────────────────────────
10 │ developmental_trajectory │ [0, 1] │ Long-term plasticity trajectory.
 │ │ │ Expertise accumulation estimate
 │ │ │ based on enhancement magnitude.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 MMN Expertise Model

```
MMN Amplitude ∝ Expertise(domain) × Deviance(domain)

Expertise-Specific Enhancement (gradient, not dissociation):
 MMN_domain = baseline_domain × (1 + α × expertise_domain)

 where α = expertise_weight (domain-specific, trainable parameter)
 NOTE: v2.0.0 used fixed d=-1.09 from Tervaniemi 2022 but that
 was a review paper — no verified single effect size exists.
 The α parameter should be fit to data or estimated from
 Koelsch 1999 (presence/absence) and Vuust 2012 (genre gradient).

 All musicians: general enhancement (Criscuolo 2022 ALE)
 Best-domain: strongest enhancement (Tervaniemi 2022 principle)

Deviance Detection:
 Deviance(t) = |feature(t) - template(t)|
 template(t) = running_mean(feature, window)
 window depends on domain: pitch=100ms, rhythm=100ms, timbre=300ms

Expertise Modulation:
 The plasticity_markers encode the degree of cortical plasticity
 that modulates the baseline deviance detection signal
```

### 7.2 Feature Formulas

```python
# f01: Pitch MMN (enhanced in singers)
# Pitch deviance weighted by pitch-processing pitch salience and consonance reference
# Coefficients: 0.40 + 0.30 + 0.30 = 1.0
pitch_change_vel = h3[(23, 3, 8, 0)] # pitch_change velocity 100ms fwd
helmholtz_val = h3[(2, 0, 0, 2)] # helmholtz value 25ms bidi
helmholtz_mean = h3[(2, 3, 1, 2)] # helmholtz mean 100ms bidi
helmholtz_diff = abs(helmholtz_val - helmholtz_mean)
onset_val = h3[(11, 3, 0, 0)] # onset_strength value 100ms fwd

 + 0.30 * helmholtz_diff
 + 0.30 * onset_val)

# f02: Rhythm MMN (enhanced in drummers)
# Onset timing deviation weighted by timbre-processing spectral envelope
# Coefficients: 0.40 + 0.30 + 0.30 = 1.0
onset_deviation = h3[(11, 3, 0, 0)] # onset_strength value 100ms fwd
spec_change_vel = h3[(21, 3, 8, 0)] # spectral_change velocity 100ms fwd
x_l4l5_mean = h3[(33, 8, 0, 2)] # x_l4l5[0] value 300ms bidi

 + 0.30 * spec_change_vel
 + 0.30 * x_l4l5_mean)

# f03: Timbre MMN (enhanced for trained instrument)
# Spectral envelope change weighted by timbre-processing instrument identity
# Coefficients: 0.40 + 0.30 + 0.30 = 1.0
timbre_change_std = h3[(24, 8, 3, 0)] # timbre_change std 300ms fwd
trist1 = h3[(18, 2, 0, 2)] # tristimulus1 value 17ms bidi
trist2 = h3[(19, 2, 0, 2)] # tristimulus2 value 17ms bidi
trist3 = h3[(20, 2, 0, 2)] # tristimulus3 value 17ms bidi
tristimulus_deviation = std([trist1, trist2, trist3])

 + 0.30 * tristimulus_deviation

# f04: Expertise Enhancement (α = trainable, domain-specific)
# Modulates the maximum domain-specific MMN by plasticity markers
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| # | Region | MNI Coordinates | Source | Evidence Type | ESME Function |
|---|--------|-----------------|--------|---------------|---------------|
| 1 | **L Superior Temporal Gyrus (BA41)** | -56, -20, Z=4.8 | Criscuolo 2022 ALE (structural, k=20) | ALE meta-analysis | MMN generators — primary auditory cortex, expertise-enlarged |
| 2 | **R Superior Temporal Gyrus (BA41)** | ~50, -30, Z=3.3 | Criscuolo 2022 ALE (structural) | ALE meta-analysis | Right AC — MMN bilateral generators |
| 3 | **L Superior Temporal Gyrus (BA22)** | -58, -46, Z=4.6 | Criscuolo 2022 ALE (functional, k=34) | ALE meta-analysis | Posterior STG — complex deviance processing |
| 4 | **R Superior Temporal Gyrus (BA22)** | ~50, -10, Z=4.9 | Criscuolo 2022 ALE (functional) | ALE meta-analysis | Right STG — musical structure processing |
| 5 | **L Inferior Frontal Gyrus (BA44)** | -54, Z=4.9 | Criscuolo 2022 ALE (functional) | ALE meta-analysis | Broca's homologue — ERAN generators (Koelsch ~2009) |
| 6 | **L Inferior Frontal Gyrus (BA9)** | -50, Z=5.0 | Criscuolo 2022 ALE (functional) | ALE meta-analysis | Frontal MMN sources — deviance evaluation |
| 7 | **Heschl's Gyrus** | bilateral | Bücher 2023 (N=162) | MEG | 130% larger in professional musicians; P1 source |
| 8 | **Planum Temporale** | ~±50, -24, 8 | Criscuolo 2022 ALE (structural) | ALE meta-analysis | Timbre/pitch expertise-modulated processing |
| 9 | **Orbitofrontal Cortex (BA10)** | — | Bücher 2023 (N=162) | MEG | Co-activation timing: synchronous in musicians, 25-40ms delayed in NM |
| 10 | **Hippocampus** | bilateral | Bonetti 2024 (N=83) | MEG | Auditory memory hierarchy — feedforward from AC |
| 11 | **Anterior Cingulate** | — | Bonetti 2024 (N=83) | MEG | Top of hierarchy for prediction error at sequence boundaries |
| 12 | **Putamen / Globus Pallidus** | — | Liao 2024 (N=25) | fMRI | Percussionist NMR: internal pacemaker for rhythm |
| 13 | **SMA** | — | Liao 2024 (N=25) | fMRI | Complex rhythmic patterns in percussionists |

```
⚠ NOTE on MNI coordinates: The Criscuolo 2022 ALE table uses FWE-
corrected cluster-level p<0.05. Some x/y/z values could not be fully
extracted from the summary due to formatting; verify against original
Table 2. The ALE peaks confirm bilateral STG + L IFG as the core
expertise network across 84 studies / 3005 participants.
```

---

## 9. Cross-Unit Pathways

### 9.1 ESME ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ESME INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ INTRA-UNIT (SPU): │
│ BCH.f01_nps ──────────► ESME (pitch baseline for deviance detection) │
│ TSCP.plasticity ──────► ESME (timbre enhancement mechanism) │
│ SDED.early_detection ─► ESME (universal detection → expertise amplified) │
│ │
│ ESME.f01_pitch_mmn ──► PSCL (expertise-weighted pitch salience) │
│ ESME.f03_timbre_mmn ─► TSCP (expertise-weighted timbre plasticity) │
│ │
│ CROSS-UNIT (P1: SPU → ARU): │
│ ESME.f04_expertise ──► ARU.SRP (expertise reward signal) │
│ Enhanced detection → pleasure from mastery │
│ │
│ CROSS-UNIT (P2: SPU → IMU): │
│ ESME.f04_expertise ──► IMU.MEAMN (expertise → memory consolidation) │
│ Enhanced deviance → stronger memory encoding │
│ │
│ CROSS-UNIT (P3: SPU → STU): │
│ ESME.f02_rhythm_mmn ─► STU.HMCE (rhythm expertise → timing precision) │
│ Drummer-type enhancement feeds sensorimotor timing │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Non-musicians** | Should show NO domain-specific enhancement | Testable |
| **Cross-domain transfer** | Singers should NOT show enhanced timbre MMN | Testable |
| **Training intervention** | Pitch training should increase pitch MMN but not timbre MMN | Testable |
| **Deactivation** | Temporary auditory cortex deactivation should abolish expertise effect | Testable |
| **Passive listening** | Enhancement should persist WITHOUT attention (pre-attentive) | Testable |
| **Replication** | Domain-specific gradient should show instrument×feature interaction in within-subjects design | **Awaiting** |
| **Singer constraint** | Martins 2022 null result: no singer/instrumentalist P2/P3 difference for musical vs vocal sounds | **CONSTRAINT** |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class ESME(BaseModel):
 """Expertise-Specific MMN Enhancement.

 Output: 11D per frame.
 """
 NAME = "ESME"
 UNIT = "SPU"
 TIER = "γ2"
 OUTPUT_DIM = 11
 EXPERTISE_ALPHA = 1.0 # Trainable; v2.0.0 used 1.09 (unverified)

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """12 tuples for ESME computation."""
 return [
 # (r3_idx, horizon, morph, law)
 (2, 0, 0, 2), # helmholtz_kang, 25ms, value, bidirectional
 (2, 3, 1, 2), # helmholtz_kang, 100ms, mean, bidirectional
 (23, 3, 8, 0), # pitch_change, 100ms, velocity, forward
 (12, 2, 0, 2), # warmth, 17ms, value, bidirectional
 (14, 5, 1, 0), # tonalness, 46ms, mean, forward
 (18, 2, 0, 2), # tristimulus1, 17ms, value, bidirectional
 (19, 2, 0, 2), # tristimulus2, 17ms, value, bidirectional
 (20, 2, 0, 2), # tristimulus3, 17ms, value, bidirectional
 (24, 8, 3, 0), # timbre_change, 300ms, std, forward
 # Direct
 (11, 3, 0, 0), # onset_strength, 100ms, value, forward
 (21, 3, 8, 0), # spectral_change, 100ms, velocity, forward
 (33, 8, 0, 2), # x_l4l5[0], 300ms, value, bidirectional
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 """
 Compute ESME 11D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
 r3: (B,T,49) raw R³ features

 Returns:
 (B,T,11) ESME output
 """
 # H³ features
 helmholtz_val = h3_direct[(2, 0, 0, 2)]
 helmholtz_mean = h3_direct[(2, 3, 1, 2)]
 pitch_change_vel = h3_direct[(23, 3, 8, 0)]
 warmth_val = h3_direct[(12, 2, 0, 2)]
 tonalness_mean = h3_direct[(14, 5, 1, 0)]
 trist1_val = h3_direct[(18, 2, 0, 2)]
 trist2_val = h3_direct[(19, 2, 0, 2)]
 trist3_val = h3_direct[(20, 2, 0, 2)]
 timbre_change_std = h3_direct[(24, 8, 3, 0)]
 onset_val = h3_direct[(11, 3, 0, 0)]
 spec_change_vel = h3_direct[(21, 3, 8, 0)]
 x_l4l5_val = h3_direct[(33, 8, 0, 2)]

 # Derived quantities
 helmholtz_diff = torch.abs(helmholtz_val - helmholtz_mean)
 tristimulus_stack = torch.stack(
 [trist1_val, trist2_val, trist3_val], dim=-1
 )
 tristimulus_deviation = torch.std(tristimulus_stack, dim=-1)

 # ═══ LAYER E: Explicit features ═══

 # f01: Pitch MMN (enhanced in singers)
 f01 = torch.sigmoid(
 0.40 * torch.abs(pitch_change_vel)
 + 0.30 * helmholtz_diff
 + 0.30 * onset_val
 ).unsqueeze(-1)

 # f02: Rhythm MMN (enhanced in drummers)
 f02 = torch.sigmoid(
 0.40 * torch.abs(onset_val)
 + 0.30 * spec_change_vel
 + 0.30 * x_l4l5_val
 ).unsqueeze(-1)

 # f03: Timbre MMN (enhanced for trained instrument)
 f03 = torch.sigmoid(
 0.40 * timbre_change_std
 + 0.30 * tristimulus_deviation
 ).unsqueeze(-1)

 # f04: Expertise Enhancement (α = trainable)
 f04 = torch.sigmoid(
 self.EXPERTISE_ALPHA
 * torch.max(torch.max(f01, f02), f03)
 )

 # ═══ LAYER M: Mathematical ═══
 mmn_expertise_fn = (f04 * torch.max(
 torch.max(f01, f02), f03
 )) ** 0.5 # geometric mean of expertise and max MMN

 # ═══ LAYER P: Present ═══
 pitch_deviance = torch.abs(
 pitch_change_vel
 pitch_deviance = torch.sigmoid(pitch_deviance)

 rhythm_deviance = torch.abs(
 onset_val
 rhythm_deviance = torch.sigmoid(rhythm_deviance)

 timbre_deviance = (
 timbre_change_std
 timbre_deviance = torch.sigmoid(timbre_deviance)

 # ═══ LAYER F: Future ═══
 feature_enhancement_pred = torch.sigmoid(
 )
 expertise_transfer_pred = torch.sigmoid(
 0.3 * f01 + 0.3 * f02 + 0.4 * f03
 )
 developmental_trajectory = torch.sigmoid(
 0.6 * f04 + 0.4 * mmn_expertise_fn
 )

 return torch.cat([
 f01, f02, f03, f04, # E: 4D
 mmn_expertise_fn, # M: 1D
 pitch_deviance, rhythm_deviance, timbre_deviance, # P: 3D
 feature_enhancement_pred, expertise_transfer_pred,
 developmental_trajectory, # F: 3D
 ], dim=-1) # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 (v2.0.0→v2.1.0: 1→12) | 5 original + 3 reviews + 1 ALE meta + 3 supporting |
| **Effect Sizes** | MMN -0.34µV (Wagner 2018); P2 5.91 vs 3.29µV (Zhang 2015); ALE Z=4.8-5.0 (Criscuolo 2022) | Multiple verified effects |
| **Evidence Modality** | EEG-MMN, EEG-ERP, EEG+iEEG, MEG×2, fMRI, ALE meta-analysis | 8 methods |
| **Unique Participants** | >3,400 (includes ALE meta N=3005) | Multi-site convergence |
| **Critical Corrections** | d=-1.09 REMOVED (unverifiable from review); clean 3-way dissociation CONSTRAINED by Martins 2022 | Improved accuracy |
| **Falsification Tests** | 0/6 confirmed | Awaiting direct expertise-domain dissociation test |
| **R³ Features Used** | ~20D of 49D | Moderate coverage |
| **H³ Demand** | 12 tuples (0.52%) | Sparse, efficient |
| **Output Dimensions** | **11D** | 4-layer structure |
---

## 13. Scientific References

1. **Koelsch, S., Schröger, E., & Tervaniemi, M. (1999)**. Superior pre-attentive auditory processing in musicians. *NeuroReport*, 10(6), 1309-1313. PMID: 10363945. DOI: 10.1097/00001756-199904260-00029
2. **Vuust, P., Brattico, E., Seppänen, M., Näätänen, R., & Tervaniemi, M. (2012)**. The sound of music: Differentiating musicians using a fast, musical multi-feature mismatch negativity paradigm. *Neuropsychologia*, 50(7), 1432-1443. DOI: 10.1016/j.neuropsychologia.2012.02.028
3. **Tervaniemi, M. (2022)**. Mismatch negativity–stimulation paradigms in past and in future. *Frontiers in Neuroscience*, 16, 1025763. DOI: 10.3389/fnins.2022.1025763 ⚠ **v2.0.0 CORRECTION**: This is a paradigm review, NOT an original study. The d=-1.09 previously attributed to this paper was unverifiable and has been removed.
4. **Yu, X., Liu, T., & Gao, D. (2015)**. The mismatch negativity: An indicator of perception of regularities in music. *Behavioural Neurology*, 2015, Article ID 469508. DOI: 10.1155/2015/469508
5. **Wagner, L., Rahne, T., Plontke, S. K., & Heidekrüger, N. (2018)**. Mismatch negativity reflects asymmetric pre-attentive harmonic interval discrimination. *PLoS ONE*, 13(4), e0196176. DOI: 10.1371/journal.pone.0196176
6. **Koelsch, S. (~2009)**. Music-syntactic processing and auditory memory – Similarities and differences between ERAN and MMN. *Psychophysiology* (in press). — ERAN generators: bilateral inferior BA44, ventrolateral premotor cortex, anterior STG.
7. **Criscuolo, A., Pando-Naude, V., Bonetti, L., Vuust, P., & Brattico, E. (2022)**. An ALE meta-analytic review of musical expertise. *Scientific Reports*, 12, 11726. DOI: 10.1038/s41598-022-14959-4
8. **Martins, I., Lima, C. F., & Pinheiro, A. P. (2022)**. Enhanced salience of musical sounds in singers and instrumentalists. *Cognitive, Affective, & Behavioral Neuroscience*, 22, 1044-1062. DOI: 10.3758/s13415-022-01007-x — ⚠ **CONSTRAINT**: No singer vs instrumentalist difference.
9. **Bonetti, L., Fernández-Rubio, G., Carlomagno, F., Dietz, M., Pantazis, D., Vuust, P., & Kringelbach, M. L. (2024)**. Spatiotemporal brain hierarchies of auditory memory recognition and predictive coding. *Nature Communications*, 15, 4313. DOI: 10.1038/s41467-024-48302-4
10. **Bücher, S., Bernhofs, V., Thieme, A., Christiner, M., & Schneider, P. (2023)**. Chronology of auditory processing and related co-activation in the orbitofrontal cortex depends on musical expertise. *Frontiers in Neuroscience*, 16, 1041397. DOI: 10.3389/fnins.2022.1041397
11. **Mischler, G., Li, Y. A., Bickel, S., Mehta, A. D., & Mesgarani, N. (2025)**. The impact of musical expertise on disentangled and contextual neural encoding of music revealed by generative music models. *Nature Communications*, 16, 8874. DOI: 10.1038/s41467-025-63961-7
12. **Liao, Y.-C., Yang, C.-J., Yu, H.-Y., Huang, C.-J., Hong, T.-Y., Li, W.-C., Chen, L.-F., & Hsieh, J.-C. (2024)**. The rhythmic mind: Brain functions of percussionists in improvisation. *Frontiers in Human Neuroscience*, 18, 1418727. DOI: 10.3389/fnhum.2024.1418727

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Pitch MMN | S⁰.L5 pitch features × HC⁰.ATT | R³.pitch_change |
| Rhythm MMN | S⁰.L4 onset × HC⁰.NPL | R³.onset_strength |
| Timbre MMN | S⁰.L5 timbre × HC⁰.HRM | R³.tristimulus |
| Expertise | HC⁰.EFC static weight | plasticity_markers (30D dynamic) |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 11/2304 = 0.48% | 12/2304 = 0.52% |
| Output dimensions | 11D | 11D (unchanged) |

---

**Model Status**: **SPECULATIVE** (awaiting replication)
**Output Dimensions**: **11D**
**Evidence Tier**: **γ (Speculative)**
**Confidence**: **<70%**
