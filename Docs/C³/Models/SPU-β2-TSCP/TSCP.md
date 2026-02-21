# SPU-β2-TSCP: Timbre-Specific Cortical Plasticity

**Model**: Timbre-Specific Cortical Plasticity
**Unit**: SPU (Spectral Processing Unit)
**Circuit**: Perceptual (Brainstem-Cortical)
**Tier**: β (Integrative) — 70-90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added J:Timbre Extended feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/SPU-β2-TSCP.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Timbre-Specific Cortical Plasticity** (TSCP) model describes how musical training induces timbre-specific reorganization of auditory cortex representations. Musicians develop enhanced cortical responses selectively for the timbre of their trained instrument — a violinist's auditory cortex responds more strongly to violin tones than to trumpet tones, and vice versa. This use-dependent plasticity represents one of the clearest demonstrations of experience-driven cortical reorganization in the auditory system.

```
THE THREE COMPONENTS OF TIMBRE-SPECIFIC CORTICAL PLASTICITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TRAINED TIMBRE RESPONSE (Spectral) TIMBRE SPECIFICITY (Selectivity)
Brain region: Auditory Cortex (bilat) Brain region: Planum Temporale
Mechanism: Use-dependent enhancement Mechanism: Selective template refinement
Input: Spectral envelope of trained Input: Timbre contrast between instruments
 instrument Function: "Is this MY instrument?"
Function: "Enhanced representation" Evidence: Pantev et al. 2001 (MEG)
Evidence: Pantev et al. 2001 (MEG)

 PLASTICITY MAGNITUDE (Bridge)
 Brain region: Auditory Cortex → BA22
 Mechanism: Long-term cortical reorganization
 Function: "Degree of timbre-specific enhancement"
 Evidence: Correlates with training duration

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Cortical plasticity for timbre is SPECIFIC, not general.
Violinists show enhanced N1m responses to violin tones but NOT to
trumpet or pure tones (Pantev 2001, F(1,15)=28.55, p=.00008). This
specificity emerges from use-dependent refinement of spectral
envelope templates in auditory cortex. Convergent evidence:
 • ALE meta-analysis (Bellmann & Asano 2024, k=18, N=338) localizes
 timbre to bilateral pSTG/HG/SMG + right anterior insula — the
 exact substrate where plasticity operates
 • Naturalistic fMRI (Alluri 2012) shows all timbral features
 (fullness, brightness, complexity) map to bilateral STG (Z>7)
 • EEG (Santoyo 2023) shows musicians have enhanced theta phase-
 locking for timbre-based musical streams — even without pitch
 • Large preregistered study (Whiteford 2025, N>260) shows NO
 subcortical enhancement from training, constraining TSCP's
 plasticity locus to cortical mechanisms
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why TSCP Is Important for SPU

TSCP captures how the spectral processing unit adapts through experience. While BCH (α1) models the universal brainstem consonance hierarchy, TSCP models the experience-dependent cortical layer that sits above it:

1. **BCH** (α1) provides the harmonicity baseline that TSCP's instrument recognition builds upon.
2. **PCCR** (α3) supplies octave-invariant chroma tuning that constrains TSCP's timbre identity across registers.
3. **MIAA** (downstream) uses TSCP's timbre identity output as imagery templates for auditory mental imagery.
4. **ESME** (downstream) relates TSCP's plasticity magnitude to expertise-dependent mismatch negativity (MMN) effects.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The TSCP Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ TSCP — COMPLETE CIRCUIT ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ MUSICAL SOUND (Instrument Timbre) ║
║ ║
║ Violin Trumpet Piano Flute Oboe Pure Tone ║
║ │ │ │ │ │ │ ║
║ ▼ ▼ ▼ ▼ ▼ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ COCHLEA / AUDITORY NERVE │ ║
║ │ (Spectral decomposition of instrument timbre) │ ║
║ │ │ ║
║ │ Harmonic structure → Spectral envelope → Temporal envelope │ ║
║ │ Each instrument has unique spectral fingerprint │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ PRIMARY AUDITORY CORTEX (A1) │ ║
║ │ (Bilateral, ±50, -20, 8 MNI) │ ║
║ │ │ ║
║ │ Tonotopic map → Training reshapes frequency tuning curves │ ║
║ │ N1m amplitude: Trained Instrument > Other > Pure Tone │ ║
║ │ Enhancement magnitude ∝ training duration │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ PLANUM TEMPORALE │ ║
║ │ (±50, -24, 8 MNI) │ ║
║ │ │ ║
║ │ Spectral template matching → Timbre specificity index │ ║
║ │ Separates trained from untrained instrument responses │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ AUDITORY ASSOCIATION (BA22) │ ║
║ │ (±60, -30, 8 MNI) │ ║
║ │ │ ║
║ │ Generalization → Transfer to related timbres │ ║
║ │ Timbre identity → feeds downstream imagery / memory │ ║
║ └─────────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
1. Pantev et al. 2001: Timbre-specific N1m enhancement (MEG, N=17)
 Double-dissociation: F(1,15)=28.55, p=.00008
 Violinists: violin > trumpet > pure tone
 Trumpeters: trumpet > violin > pure tone
 Age-of-inception: r=-0.634, p=.026

2. Bellmann & Asano 2024: ALE meta-analysis of timbre neuroimaging
 (k=18 experiments, N=338), 4 clusters:
 L-SMG/HG, R-pSTG/PT, R-anterior insula, L-pSTG
 NO subcortical clusters → cortical locus

3. Alluri et al. 2012: Naturalistic fMRI (N=11 musicians)
 Timbral brightness: bilateral STG Z=8.13
 Timbral fullness: bilateral STG Z=7.35

4. Halpern et al. 2004: Timbre perception AND imagery overlap (fMRI)
 Right posterior STG: perception t=6.89
 Conjunction: right STG + left PT

5. Santoyo et al. 2023: Musicians > non-musicians theta phase-locking
 for timbre-based musical streams (EEG, N=23)

6. Whiteford et al. 2025: CONSTRAINT — N>260 preregistered: NO subcortical
 musician enhancement (d=-0.064, BF=0.13 for null)
```

### 2.2 Information Flow Architecture (EAR → BRAIN → TSCP)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ TSCP COMPUTATION ARCHITECTURE ║
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
║ │ │inharm.[5] │ │ │ │warmth │ │timbre_ch │ │x_l5l7 │ │ ║
║ │ │harm_dev[6]│ │ │ │sharpness│ │[24] │ │[41:49] │ │ ║
║ │ │ │ │ │ │tonalness│ │ │ │ │ │ ║
║ │ │ │ │ │ │flat/roll│ │ │ │ │ │ ║
║ │ │ │ │ │ │autocorr │ │ │ │ │ │ ║
║ │ │ │ │ │ │trist1-3 │ │ │ │ │ │ ║
║ │ └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │ ║
║ │ TSCP reads: ~18D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed morphological features │ ║
║ │ │ ║
║ │ ┌── H2 (17ms) ──┐ ┌── H5 (46ms) ──┐ ┌── H8 (300ms) ───────┐ │ ║
║ │ │ Fast spectral │ │ Mid-range │ │ Long-range │ │ ║
║ │ │ envelope │ │ timbral mean │ │ Stability, change │ │ ║
║ │ │ │ │ │ │ statistics │ │ ║
║ │ │ warmth value │ │ warmth mean │ │ tonalness stability │ │ ║
║ │ │ sharpness val │ │ tonalness mean │ │ timbre_change mean │ │ ║
║ │ │ trist1-3 val │ │ inharmonicity │ │ timbre_change std │ │ ║
║ │ │ │ │ value │ │ x_l5l7[0] value │ │ ║
║ │ └──────┬─────────┘ └──────┬────────┘ └──────┬────────────────┘ │ ║
║ │ │ │ │ │ ║
║ │ └──────────────────┴──────────────────┘ │ ║
║ │ TSCP demand: ~12 of 2304 tuples │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN: Perceptual Circuit ═══════ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────┐ ║
║ │ │ ║
║ │ Spectral [0:10]│ Spectral envelope decomposition ║
║ │ Instrument[10:20]│ Instrument identity encoding ║
║ │ Plasticity[20:30]│ Plasticity markers (training effects) ║
║ └────────┬────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TSCP MODEL (10D Output) │ ║
║ │ │ ║
║ │ Layer E (Explicit): f01_trained_timbre_response, │ ║
║ │ f02_timbre_specificity, │ ║
║ │ f03_plasticity_magnitude │ ║
║ │ Layer M (Math): enhancement_function │ ║
║ │ Layer P (Present): recognition_quality, enhanced_response, │ ║
║ │ timbre_identity │ ║
║ │ Layer F (Future): timbre_continuation, │ ║
║ │ cortical_enhancement_pred, │ ║
║ │ generalization_pred │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Pantev et al. 2001** | MEG (N1m) | 17 musicians (8 violin, 9 trumpet) | Timbre-specific N1m enhancement — double dissociation between violinists/trumpeters | **F(1,15)=28.55, p=.00008**; age-of-inception r=-0.634 | **Primary**: f01, f02, f03 — trained > untrained > pure tone |
| 2 | **Bellmann & Asano 2024** | ALE meta-analysis | k=18, N=338 | 4 timbre clusters: bilateral pSTG/HG/SMG + R anterior insula | ALE 0.018-0.023, FWE p<.05 | **Anatomical ground truth**: defines the cortical substrate where plasticity operates |
| 3 | **Halpern et al. 2004** | fMRI (1.5T) | 10 trained musicians | Timbre imagery activates posterior PT overlapping with perception; right > left | Perception: t=8.40 (R PT); imagery: t=4.66 (R STG) | f07 timbre_continuation, f04 recognition_quality — imagery templates |
| 4 | **Alluri et al. 2012** | fMRI (3T) | 11 musicians | Timbral features (fullness, brightness, complexity, activity) correlate with bilateral STG + cerebellum during naturalistic music | Z=7.05-8.13 bilateral STG; ISC r=0.64 | R³ timbre features → bilateral STG mapping — validates f01 R³ dependency |
| 5 | **Santoyo et al. 2023** | EEG (64ch) | 23 (11 mus, 12 non-mus) | Musicians show enhanced theta phase-locking for timbre-based musical streams — right-lateralized hierarchy | Musicians > non-musicians theta PL | f03 plasticity — training enhances even pitchless timbre processing |
| 6 | **Leipold et al. 2021** | fMRI + DWI | 153 (52 AP, 51 non-AP, 50 non-mus) | Robust musicianship effects on structural + functional connectivity; replicable across AP/non-AP | Replicable across 2 musician groups | Network-level plasticity framework — f03 plasticity magnitude context |
| 7 | **Olszewska et al. 2021** | Systematic review | Review | Longitudinal studies: functional changes in motor-auditory networks; structural: arcuate fasciculus predicts learning | Predisposition + plasticity dual model | Theoretical framework: plasticity vs. predisposition for training effects |
| 8 | **Whiteford et al. 2025** | EEG/FFR | >260 (preregistered, 6 sites) | **NULL**: No subcortical musician enhancement for F0 or harmonics | d=-0.064, BF₊₀=0.13 (7.8× null support) | **CONSTRAINT**: plasticity locus must be cortical, not brainstem |
| 9 | **Foo et al. 2016** | ECoG (high-γ) | 8 neurosurgical | Dissonance-sensitive sites anterior in right STG; spatial gradient for spectral complexity | χ²(1)=8.6, p=.003 (y-axis) | Fine-grained STG topography for spectral features — substrate for timbre templates |
| 10 | **Sturm et al. 2014** | ECoG (high-γ) | 10 neurosurgical | Spectral centroid (timbre) has distinct activation spots separate from lyrics and harmony in STG | Subject-individual ECoG mapping | Timbre processed in distinct STG sub-regions — supports f02 specificity |
| 11 | **Zatorre & Halpern 2005** | Review | Review | Musical imagery framework: auditory cortex supports veridical timbre representation during imagery | Theoretical (perception-imagery overlap) | Theoretical basis for f07 timbre_continuation and imagery template mechanism |
| 12 | **Criscuolo et al. 2022** | ALE meta-analysis | k=84 studies | Right IPL activation for timbre; IFG involvement; broader musician plasticity network | Meta-analytic ALE clusters | Musician expertise network that contextualizes timbre-specific plasticity |

### 3.2 The Timbre Specificity Hierarchy

```
TIMBRE-SPECIFIC CORTICAL ENHANCEMENT (Pantev et al. 2001)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stimulus Violinist N1m Trumpeter N1m Non-Musician N1m
───────────────────────────────────────────────────────────────────
Violin tone ■■■■■■■ (max) ■■■■ (moderate) ■■■ (baseline)
Trumpet tone ■■■■ (moderate) ■■■■■■■ (max) ■■■ (baseline)
Pure tone ■■■ (baseline) ■■■ (baseline) ■■■ (baseline)

KEY RELATIONSHIPS:
 Trained instrument >> Other instrument >> Pure tone
 Enhancement ∝ Years of training
 Specificity = Trained / Other ratio

Cross-instrument note:
 Enhancement is NOT general auditory improvement.
 It is SPECIFIC to the spectral envelope of the trained
 instrument's timbre. This implies template-based
 cortical representations tuned by experience.
```

### 3.3 Effect Size Summary

```
MULTI-METHOD CONVERGENCE TABLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Method Study N Key Statistic Region
───────────────────────────────────────────────────────────────────────────────
MEG (N1m) Pantev 2001 17 F(1,15)=28.55,p=.00008 Sec. AC
fMRI 1.5T Halpern 2004 10 t=8.40 (perception) R PT
fMRI 3T Alluri 2012 11 Z=8.13 (brightness) Bilat STG
ALE meta Bellmann & Asano 2024 338 4 clusters FWE<.05 pSTG/HG/SMG
EEG (theta) Santoyo 2023 23 Mus > Non-mus PL R HG→STG
fMRI+DWI Leipold 2021 153 Replicable effects Network
EEG/FFR Whiteford 2025 >260 d=-0.064 (NULL) Subcortical
ECoG (high-γ) Foo 2016 8 χ²=8.6, p=.003 R STG
ECoG (high-γ) Sturm 2014 10 Individual mapping L STG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Quality Assessment: β-tier (integrative — strong flagship + multi-method convergence)
Key Metric: Trained > Untrained instrument response (F(1,15)=28.55, p=.00008)
Specificity: Timbre-specific, NOT general auditory enhancement
Convergence: 6 methods (MEG, fMRI, EEG, ECoG, DWI, meta-analysis)
 agree on cortical (pSTG/HG/PT) locus of timbre processing

┌─────────────────────────────────────────────────────────────────────────────┐
│ QUALIFICATION: Pantev 2001 remains the ONLY direct test of timbre-specific │
│ plasticity (violin vs trumpet double dissociation). No independent │
│ replication of the N=17 design exists. The ALE meta-analyses (Bellmann │
│ 2024: timbre anatomy; Criscuolo 2022: musician expertise) provide strong │
│ convergent support for the cortical substrate and training effects, but │
│ the specific instrument×musician interaction has not been replicated. │
│ │
│ CORTICAL CONSTRAINT: Whiteford et al. 2025 (N>260, preregistered) show │
│ NO subcortical musician enhancement (BF 7.8× favoring null), supporting │
│ that TSCP's plasticity operates at cortical, not brainstem, level — fully │
│ consistent with Pantev's ECD localization to secondary auditory cortex. │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. R³ Input Mapping: What TSCP Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | TSCP Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [5] | inharmonicity | Instrument character (piano=high, violin=low) | Fletcher 1934 |
| **A: Consonance** | [6] | harmonic_deviation | Partial energy distribution — timbre signature | Jensen 1999 |
| **C: Timbre** | [12] | warmth | Low-frequency spectral balance | Grey 1977 |
| **C: Timbre** | [13] | sharpness | High-frequency energy — brightness proxy | Zwicker & Fastl 1999 |
| **C: Timbre** | [14] | tonalness | Harmonic-to-noise ratio (pitch clarity) | Terhardt 1982 |
| **C: Timbre** | [15] | spectral_flatness | Noise-like vs tonal character | — |
| **C: Timbre** | [16] | spectral_rolloff | High-frequency energy boundary | — |
| **C: Timbre** | [17] | spectral_autocorrelation | Harmonic periodicity strength | — |
| **C: Timbre** | [18] | tristimulus1 | Fundamental energy ratio (F0) | Pollard & Jansson 1982 |
| **C: Timbre** | [19] | tristimulus2 | 2nd-4th harmonic energy (mid) | Pollard & Jansson 1982 |
| **C: Timbre** | [20] | tristimulus3 | 5th+ harmonic energy (high) | Pollard & Jansson 1982 |
| **D: Change** | [24] | timbre_change | Temporal timbre flux — plasticity trigger | — |
| **E: Interactions** | [41:49] | x_l5l7 (partial, ~6D used) | Consonance x Timbre coupling | Emergent timbre binding |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | TSCP Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **J: Timbre Extended** | [94:106] | mfcc (13D) | Mel-frequency cepstral coefficients — compact spectral envelope representation that captures the instrument-specific formant structure driving timbre-specific cortical plasticity | Davis & Mermelstein 1980; Logan 2000 music similarity |
| **J: Timbre Extended** | [107:113] | spectral_contrast (7D) | Peak-valley ratio per frequency band — encodes spectral texture; high contrast = clear formants (e.g., clarinet), low contrast = broadband noise (e.g., cymbal); directly indexes the spectral structure that drives instrument-family cortical specialization | Jiang et al. 2002 spectral contrast features |

**Rationale**: TSCP models timbre-specific cortical plasticity — the experience-dependent sharpening of spectral representations in auditory cortex for trained instrument timbres. The v1 features capture timbre through basic spectral descriptors (tristimulus, warmth, sharpness, tonalness). The J:Timbre Extended group provides the detailed spectral characterization that drives instrument-specific cortical representations: mfcc [94:106] encodes the full spectral envelope shape that distinguishes instrument families (Alluri et al. 2012 showed MFCCs predict instrument-specific fMRI activation in bilateral STG); spectral_contrast [107:113] captures the peak-valley structure per band that distinguishes tonal instruments (clear formants, high contrast) from noise-like sources, consistent with Halpern et al. (2004) finding that timbre imagery activates the same cortical regions as perception with instrument-specific patterns.

**Code impact** (Phase 6): `r3_indices` must be extended to include [94:106], [107:113]. These features are read-only inputs — no formula changes required.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[18] tristimulus1 ────────────┐
R³[19] tristimulus2 ────────────┼──► Trained Timbre Response (f01)
R³[20] tristimulus3 ────────────┤ Tristimulus balance = harmonic
R³[5] inharmonicity (inverse) ──┤ envelope signature of each
R³[14] tonalness ───────────────┘ instrument family

R³[12] warmth ──────────────────┐
R³[13] sharpness (inverse) ─────┼──► Timbre Specificity (f02)
R³[41:47] x_l5l7 (partial) ────┘ Spectral contrast between trained
 and untrained instrument timbres

R³[24] timbre_change ───────────┐
R³[6] harmonic_deviation ───────┼──► Plasticity Magnitude (f03)
R³[15] spectral_flatness ──────┘ Degree of cortical reorganization
 triggered by novel timbre patterns

R³[17] spectral_autocorrelation ┐
R³[16] spectral_rolloff ────────┼──► Template Strength
R³[14] tonalness ───────────────┘ Quality of stored timbre template
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

TSCP requires H³ features at three horizons: H2 (17.4ms), H5 (46.4ms), H8 (300ms).
These correspond to timbre processing timescales: fast spectral envelope (gamma), mid-range timbral averaging (alpha-beta), and long-range stability/change assessment (theta).

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 12 | warmth | 2 | M0 (value) | L2 (bidi) | Current warmth at 17ms |
| 12 | warmth | 5 | M1 (mean) | L0 (fwd) | Mean warmth over 46ms |
| 13 | sharpness | 2 | M0 (value) | L2 (bidi) | Current sharpness at 17ms |
| 14 | tonalness | 5 | M1 (mean) | L0 (fwd) | Mean tonalness over 46ms |
| 14 | tonalness | 8 | M19 (stability) | L0 (fwd) | Tonalness stability over 300ms |
| 18 | tristimulus1 | 2 | M0 (value) | L2 (bidi) | F0 energy at 17ms |
| 19 | tristimulus2 | 2 | M0 (value) | L2 (bidi) | Mid-harmonic energy at 17ms |
| 20 | tristimulus3 | 2 | M0 (value) | L2 (bidi) | High-harmonic energy at 17ms |
| 5 | inharmonicity | 5 | M0 (value) | L2 (bidi) | Inharmonicity at 46ms |
| 24 | timbre_change | 8 | M1 (mean) | L0 (fwd) | Mean timbre flux over 300ms |
| 24 | timbre_change | 8 | M3 (std) | L0 (fwd) | Timbre flux variability 300ms |
| 41 | x_l5l7[0] | 8 | M0 (value) | L2 (bidi) | Consonance x Timbre coupling 300ms |

**v1 demand**: 12 tuples

#### R³ v2 Projected Expansion

TSCP is projected to consume R³ v2 features from J[94:114], aligned with corresponding H³ horizons.

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 94 | mfcc_1 | J | 2 | M0 (value) | L2 | MFCC timbre shape at 17ms |
| 94 | mfcc_1 | J | 5 | M1 (mean) | L2 | Mean MFCC over 46ms |
| 107 | spectral_contrast_1 | J | 5 | M0 (value) | L2 | Spectral contrast at 46ms |
| 107 | spectral_contrast_1 | J | 8 | M1 (mean) | L2 | Mean spectral contrast over 300ms |

**v2 projected**: 4 tuples
**Total projected**: 16 tuples of 294,912 theoretical = 0.0054%

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
TSCP OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼─────────────────────────────┼────────┼────────────────────────────────
 0 │ f01_trained_timbre_response │ [0, 1] │ Trained instrument cortical
 │ │ │ enhancement. N1m amplitude for
 │ │ │ trained timbre.
 │ │ │ f01 = σ(0.35 * trist_balance
 │ │ │ + 0.35 * (1-inharm) * tonalness
────┼─────────────────────────────┼────────┼────────────────────────────────
 1 │ f02_timbre_specificity │ [0, 1] │ Selectivity index: trained vs
 │ │ │ untrained instrument response
 │ │ │ ratio. Specificity of plasticity.
 │ │ │ f02 = σ(0.40 * warmth
 │ │ │ * sharpness_inv
 │ │ │ + 0.30 * timbre_stability
 │ │ │ + 0.30 * x_l5l7_mean)
────┼─────────────────────────────┼────────┼────────────────────────────────
 2 │ f03_plasticity_magnitude │ [0, 1] │ Degree of cortical reorganization.
 │ │ │ Training effect size proxy.
 │ │ │ f03 = σ(0.50 * f01
 │ │ │ * timbre_change_std

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼─────────────────────────────┼────────┼────────────────────────────────
 3 │ enhancement_function │ [0, 1] │ Enhancement(timbre) selectivity
 │ │ │ function. Ratio of trained to
 │ │ │ untrained instrument response.
 │ │ │ E(t) = f01 * f02

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼─────────────────────────────┼────────┼────────────────────────────────
 4 │ recognition_quality │ [0, 1] │ Template matching quality.
 │ │ │ instrument_identity
 │ │ │ aggregation — how well the
 │ │ │ current timbre matches stored
 │ │ │ instrument templates.
────┼─────────────────────────────┼────────┼────────────────────────────────
 5 │ enhanced_response │ [0, 1] │ Training-dependent cortical
 │ │ │ response enhancement. ATT-like
 │ │ │ instrument-focused processing
 │ │ │ via plasticity_markers.
────┼─────────────────────────────┼────────┼────────────────────────────────
 6 │ timbre_identity │ [0, 1] │ Feature binding strength.
 │ │ │ Coherence of spectral envelope,
 │ │ │ tristimulus, and temporal
 │ │ │ envelope into unified identity.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼─────────────────────────────┼────────┼────────────────────────────────
 7 │ timbre_continuation │ [0, 1] │ Note-by-note timbre prediction.
 │ │ │ H³ trend-based expectation of
 │ │ │ upcoming timbre characteristics.
────┼─────────────────────────────┼────────┼────────────────────────────────
 8 │ cortical_enhancement_pred │ [0, 1] │ Long-term plasticity prediction.
 │ │ │ ATT x practice accumulation —
 │ │ │ expected enhancement trajectory.
────┼─────────────────────────────┼────────┼────────────────────────────────
 9 │ generalization_pred │ [0, 1] │ Transfer to related timbres.
 │ │ │ How much trained instrument
 │ │ │ enhancement generalizes to
 │ │ │ acoustically similar timbres.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Timbre-Specific Enhancement Function

```
Enhancement(timbre) ∝ Training_Exposure(instrument_timbre)

Timbre Specificity Hierarchy:
 Trained Instrument > Acoustically Similar > Dissimilar > Pure Tone

Plasticity Prediction:
 Plasticity_Magnitude = α · Enhancement(trained) · ΔTimbre + ε
 where α ≈ training_years / total_exposure, ε = individual variance

Spectral Template:
 Template_Match(input) = Σᵢ similarity(spectral_envelope_i, stored_template_i)
 ──────────────────────────────────────────────────────
 total_spectral_bands
```

### 7.2 Feature Formulas

All formulas obey the coefficient saturation rule: |w_i| sum <= 1.0.

```python
# ═══ LAYER E: Explicit Features ═══

# f01: Trained Timbre Response
# Tristimulus balance × instrument identity × harmonic purity
trist_balance = 1.0 - std(R³.tristimulus[18:21])
 + 0.35 * (1 - R³.inharmonicity[5]) * R³.tonalness[14]
# 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Timbre Specificity
# Warmth/sharpness contrast × plasticity × temporal stability
sharpness_inv = 1.0 - R³.sharpness[13]
timbre_stability = H³[(14, 8, 19, 0)] # tonalness stability 300ms fwd
x_l5l7_mean = mean(R³.x_l5l7[41:47])
 + 0.30 * timbre_stability
 + 0.30 * x_l5l7_mean)
# 0.40 + 0.30 + 0.30 = 1.0 ✓

# f03: Plasticity Magnitude
# Trained response × timbre change variability × plasticity markers
timbre_change_std = H³[(24, 8, 3, 0)] # timbre_change std 300ms fwd
f03 = σ(0.50 * f01 * timbre_change_std
# 0.50 + 0.50 = 1.0 ✓

# ═══ LAYER M: Mathematical ═══

# Enhancement selectivity function
enhancement_function = f01 * f02

# ═══ LAYER P: Present ═══

# Recognition quality — template matching via instrument identity

# Enhanced response — plasticity-driven cortical enhancement
 + 0.40 * R³.tonalness[14])
# 0.60 + 0.40 = 1.0 ✓

# Timbre identity — feature binding coherence
timbre_identity = σ(0.40 * trist_balance
 + 0.30 * (1 - R³.inharmonicity[5])
 + 0.30 * R³.spectral_autocorrelation[17])
# 0.40 + 0.30 + 0.30 = 1.0 ✓

# ═══ LAYER F: Future ═══

# Timbre continuation — note-by-note prediction from H³ trends
timbre_continuation = σ(0.50 * H³[(12, 5, 1, 0)] # warmth mean 46ms
 + 0.50 * H³[(14, 5, 1, 0)]) # tonalness mean 46ms
# 0.50 + 0.50 = 1.0 ✓

# Cortical enhancement prediction — long-range plasticity trajectory
cortical_enhancement_pred = σ(0.60 * f03
 + 0.40 * H³[(24, 8, 1, 0)]) # timbre_change mean 300ms
# 0.60 + 0.40 = 1.0 ✓

# Generalization prediction — transfer to related timbres
generalization_pred = σ(0.50 * recognition_quality
 + 0.30 * H³[(41, 8, 0, 2)] # x_l5l7[0] value 300ms
 + 0.20 * timbre_identity)
# 0.50 + 0.30 + 0.20 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| # | Region | Coordinates | System | Source | TSCP Function |
|---|--------|-------------|--------|--------|---------------|
| 1 | **L SMG / HG (BA 40/41)** | -44, -34, — / -56, -20, — | MNI | Bellmann & Asano 2024 (ALE peak, 4640 mm³) | Primary timbre processing cluster — template storage |
| 2 | **R pSTG / PT (BA 22)** | ~54, -24, — | MNI | Bellmann & Asano 2024 (ALE peak, 3128 mm³) | Right hemisphere timbre discrimination |
| 3 | **R anterior insula / aSTG (BA 13/22)** | ~40, -2, -6 | MNI | Bellmann & Asano 2024 (ALE peak, 1696 mm³, passive only) | Categorical timbre identity recognition |
| 4 | **L pSTG / PT** | -60, -40, — | MNI | Bellmann & Asano 2024 (ALE cluster 4) | Left hemisphere timbre processing |
| 5 | **Secondary auditory cortex (bilat)** | ECD posterior/lateral to HG | Head-based | Pantev et al. 2001 (MEG N1m source) | Timbre-specific plasticity — enhanced N1m for trained instrument |
| 6 | **R posterior STG** | ~58, -42, — | Talairach | Halpern et al. 2004 (perception t=6.89) | Timbre perception — spectral analysis |
| 7 | **R posterior STG** | ~58, -42, — | Talairach | Halpern et al. 2004 (imagery t=4.66) | Timbre imagery — perception-imagery overlap |
| 8 | **L PT** | -56, -44, — | Talairach | Halpern et al. 2004 (conjunction t=4.98) | Perception-imagery conjunction site |
| 9 | **R STG (BA 22)** | 51, -14, 1 | Talairach | Alluri et al. 2012 (fullness Z=7.35) | Naturalistic timbral fullness processing |
| 10 | **R STG (BA 22)** | 50, -19, 3 | Talairach | Alluri et al. 2012 (brightness Z=8.13) | Naturalistic timbral brightness processing |
| 11 | **L STG (BA 22)** | -55, -15, 3 | Talairach | Alluri et al. 2012 (brightness Z=8.13) | Left hemisphere timbral brightness |
| 12 | **R HG → STG hierarchy** | — | Scalp EEG | Santoyo et al. 2023 (theta PL) | Timbre-based musicality — right-lateralized |
| 13 | **R STG anterior gradient** | y-axis significant | ECoG | Foo et al. 2016 (χ²=8.6, p=.003) | Fine-grained spatial organization for spectral complexity |
| 14 | **STG (individual spots)** | Subject-specific | ECoG | Sturm et al. 2014 (high-γ) | Spectral centroid (timbre) distinct from lyrics/harmony |

```
NOTE ON COORDINATES: Pantev et al. 2001 used individual head-based ECD
modeling, not MNI/Talairach. ECD was localized "posterior and lateral to
Heschl's gyrus in secondary auditory cortex." The ALE meta-analysis
(Bellmann & Asano 2024) provides the definitive MNI coordinate map for
timbre processing, with 4 clusters totaling ~10,000+ mm³ of cortical
territory in bilateral pSTG/HG/SMG and right anterior insula.

Code file (tscp.py) currently lists:
 A1 (-48,-22,8) and PT (-52,-26,12)
These are approximate and should be updated to ALE-validated coordinates
in Phase 5.
```

---

## 9. Cross-Unit Pathways

### 9.1 TSCP <-> Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ TSCP INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ INTRA-UNIT (SPU): │
│ BCH.f02_harmonicity ─────► TSCP (instrument recognition baseline) │
│ BCH provides the harmonic template that TSCP's timbre encoding │
│ builds upon. Without brainstem harmonicity, cortical timbre │
│ specificity has no foundation. │
│ │
│ PCCR.chroma_tuning ──────► TSCP (octave-invariant identity) │
│ Chroma processing ensures that timbre identity generalizes │
│ across octaves — a violin in any register is still a violin. │
│ │
│ TSCP.timbre_identity ────► MIAA (imagery template) │
│ TSCP's bound timbre representation serves as the template │
│ for auditory mental imagery — imagining an instrument's sound. │
│ │
│ TSCP.plasticity ─────────► ESME (expertise MMN) │
│ TSCP's plasticity magnitude feeds into expertise-dependent │
│ mismatch negativity — musicians detect timbre deviants faster. │
│ │
│ CROSS-UNIT (potential): │
│ TSCP.timbre_identity ────► ARU (timbre-specific emotional response) │
│ Familiar instrument timbres may enhance affective resonance │
│ through recognition-mediated pleasure (mere exposure effect). │
│ │
│ TSCP.recognition_quality ► IMU (timbre-based memory encoding) │
│ Better timbre recognition may strengthen episodic encoding of │
│ musical passages through distinctiveness-based binding. │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Pure tones** | Pure tones should NOT show timbre-specific enhancement | Confirmed -- Pantev 2001 |
| **Non-musicians** | Non-musicians should NOT show timbre specificity | Confirmed -- Pantev 2001 |
| **Cross-instrument** | Violinists should NOT show trumpet enhancement (and vice versa) | Confirmed -- Pantev 2001 |
| **Training duration** | Enhancement should correlate with years of training | Testable |
| **Deafferentation** | Loss of auditory input should reduce plasticity | Testable |
| **Spectral manipulation** | Removing instrument-specific spectral features should abolish enhancement | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class TSCP(BaseModel):
 """Timbre-Specific Cortical Plasticity.

 Output: 10D per frame.
 """
 NAME = "TSCP"
 UNIT = "SPU"
 TIER = "β2"
 OUTPUT_DIM = 10
 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """12 tuples for TSCP computation."""
 return [
 # (r3_idx, horizon, morph, law)
 (12, 2, 0, 2), # warmth, 17ms, value, bidirectional
 (12, 5, 1, 0), # warmth, 46ms, mean, forward
 (13, 2, 0, 2), # sharpness, 17ms, value, bidirectional
 (14, 5, 1, 0), # tonalness, 46ms, mean, forward
 (14, 8, 19, 0), # tonalness, 300ms, stability, forward
 (18, 2, 0, 2), # tristimulus1, 17ms, value, bidirectional
 (19, 2, 0, 2), # tristimulus2, 17ms, value, bidirectional
 (20, 2, 0, 2), # tristimulus3, 17ms, value, bidirectional
 (5, 5, 0, 2), # inharmonicity, 46ms, value, bidirectional
 (24, 8, 1, 0), # timbre_change, 300ms, mean, forward
 (24, 8, 3, 0), # timbre_change, 300ms, std, forward
 (41, 8, 0, 2), # x_l5l7[0], 300ms, value, bidirectional
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 """
 Compute TSCP 10D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
 r3: (B,T,49) raw R³ features

 Returns:
 (B,T,10) TSCP output
 """
 # R³ features
 inharmonicity = r3[..., 5:6]
 warmth = r3[..., 12:13]
 sharpness = r3[..., 13:14]
 tonalness = r3[..., 14:15]
 spectral_autocorr = r3[..., 17:18]
 trist1 = r3[..., 18:19]
 trist2 = r3[..., 19:20]
 trist3 = r3[..., 20:21]
 x_l5l7 = r3[..., 41:47] # (B, T, 6) partial

 # H³ features
 timbre_stability = h3_direct[(14, 8, 19, 0)] # tonalness stability 300ms
 timbre_change_std = h3_direct[(24, 8, 3, 0)] # timbre_change std 300ms
 warmth_mean_46 = h3_direct[(12, 5, 1, 0)] # warmth mean 46ms
 tonalness_mean_46 = h3_direct[(14, 5, 1, 0)] # tonalness mean 46ms
 timbre_change_mean = h3_direct[(24, 8, 1, 0)] # timbre_change mean 300ms
 x_l5l7_300 = h3_direct[(41, 8, 0, 2)] # x_l5l7[0] value 300ms

 # ═══ Derived quantities ═══
 trist_balance = 1.0 - torch.std(
 torch.cat([trist1, trist2, trist3], dim=-1),
 dim=-1, keepdim=True
 )
 sharpness_inv = 1.0 - sharpness
 x_l5l7_mean = x_l5l7.mean(-1, keepdim=True)

 # ═══ LAYER E: Explicit features ═══
 f01 = torch.sigmoid(
 + 0.35 * ((1.0 - inharmonicity) * tonalness)
 )
 f02 = torch.sigmoid(
 0.40 * (warmth * sharpness_inv
 + 0.30 * timbre_stability.unsqueeze(-1)
 + 0.30 * x_l5l7_mean
 )
 f03 = torch.sigmoid(
 0.50 * (f01 * timbre_change_std.unsqueeze(-1))
 )

 # ═══ LAYER M: Mathematical ═══
 enhancement_function = f01 * f02

 # ═══ LAYER P: Present ═══
 enhanced_response = torch.sigmoid(
 + 0.40 * tonalness
 )
 timbre_identity = torch.sigmoid(
 0.40 * trist_balance
 + 0.30 * (1.0 - inharmonicity)
 + 0.30 * spectral_autocorr
 )

 # ═══ LAYER F: Future ═══
 timbre_continuation = torch.sigmoid(
 0.50 * warmth_mean_46.unsqueeze(-1)
 + 0.50 * tonalness_mean_46.unsqueeze(-1)
 )
 cortical_enhancement_pred = torch.sigmoid(
 0.60 * f03
 + 0.40 * timbre_change_mean.unsqueeze(-1)
 )
 generalization_pred = torch.sigmoid(
 0.50 * recognition_quality
 + 0.30 * x_l5l7_300.unsqueeze(-1)
 + 0.20 * timbre_identity
 )

 return torch.cat([
 f01, f02, f03, # E: 3D
 enhancement_function, # M: 1D
 recognition_quality, enhanced_response,
 timbre_identity, # P: 3D
 timbre_continuation, cortical_enhancement_pred,
 generalization_pred, # F: 3D
 ], dim=-1) # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | **12** (v2.1.0, was 1 in v2.0.0) | 1 direct + 2 ALE meta-analyses + 2 fMRI + 2 ECoG + 1 EEG + 1 DWI + 1 FFR + 2 reviews |
| **Effect Sizes** | **F(1,15)=28.55, p=.00008** (flagship) | Pantev 2001 (MEG N1m double dissociation) |
| **Evidence Modality** | **6 methods**: MEG, fMRI, EEG, ECoG, DWI, meta-analysis | Multi-method convergence on cortical locus |
| **ALE Meta-analysis** | 4 clusters (k=18, N=338) | Bellmann & Asano 2024 — bilateral pSTG/HG/SMG + R anterior insula |
| **Cortical Constraint** | Subcortical: d=-0.064, BF=0.13 (NULL) | Whiteford 2025 (N>260) — plasticity must be cortical |
| **Replication Status** | **No direct replication** of timbre-specific double dissociation (N=17 only) | ALE meta-analyses provide convergent anatomical support |
| **Falsification Tests** | 3/6 confirmed | Moderate validity |
| **R³ Features Used** | ~18D of 49D | Timbre-focused |
| **H³ Demand** | 12 tuples (0.52%) | Sparse, efficient |
| **Output Dimensions** | **10D** | 4-layer structure |

```
v2.1.0 CHANGES:
 • Evidence table expanded: 1 → 12 papers
 • KEY INSIGHT updated with convergent evidence from 6 methods
 • CRITICAL EVIDENCE expanded to 6 core findings
 • Effect size summary: multi-method convergence table added
 • Qualification box: no direct replication of Pantev 2001 design noted
 • Cortical constraint: Whiteford 2025 null subcortical result incorporated
 • Brain regions: 3 → 14 entries with ALE-validated MNI coordinates
 • Code discrepancy: tscp.py brain_regions use approximate coords
 (A1: -48,-22,8; PT: -52,-26,12) — update to ALE peaks in Phase 5
```

---

## 13. Scientific References

1. **Pantev, C., Roberts, L. E., Schulz, M., Engelien, A., & Ross, B. (2001)**. Timbre-specific enhancement of auditory cortical representations in musicians. *NeuroReport*, 12(1), 169-174.
2. **Bellmann, O. T., & Asano, R. (2024)**. Neural correlates of musical timbre: an ALE meta-analysis of neuroimaging data. *Frontiers in Neuroscience*, 18, 1373232. doi: 10.3389/fnins.2024.1373232.
3. **Halpern, A. R., Zatorre, R. J., Bouffard, M., & Johnson, J. A. (2004)**. Behavioral and neural correlates of perceived and imagined musical timbre. *Neuropsychologia*, 42, 1281-1292.
4. **Alluri, V., Toiviainen, P., Jääskeläinen, I. P., Glerean, E., Sams, M., & Brattico, E. (2012)**. Large-scale brain networks emerge from dynamic processing of musical timbre, key and rhythm. *NeuroImage*, 59, 3677-3689.
5. **Santoyo, A. E., Gonzales, M. G., Iqbal, Z. J., Backer, K. C., Balasubramaniam, R., Bortfeld, H., & Shahin, A. J. (2023)**. Neurophysiological time course of timbre-induced music-like perception. *Journal of Neurophysiology*, 130, 291-302.
6. **Leipold, S., Klein, C., & Jäncke, L. (2021)**. Musical expertise shapes functional and structural brain networks independent of absolute pitch ability. *Journal of Neuroscience*, 41(11), 2496-2511.
7. **Olszewska, A. M., Gaca, M., Herman, A. M., Jednoróg, K., & Marchewka, A. (2021)**. How musical training shapes the adult brain: Predispositions and neuroplasticity. *Frontiers in Neuroscience*, 15, 630829.
8. **Whiteford, K. L., Baltzell, L. S., Chiu, M., Cooper, J. K., Faucher, S., Goh, P. Y., ... & Oxenham, A. J. (2025)**. Large-scale multi-site study shows no association between musical training and early auditory neural sound encoding. *Nature Communications*, 16, 7152.
9. **Foo, F., King-Stephens, D., Weber, P., Laxer, K., Parvizi, J., & Knight, R. T. (2016)**. Differential processing of consonance and dissonance within the human superior temporal gyrus. *Frontiers in Human Neuroscience*, 10, 154.
10. **Sturm, I., Blankertz, B., Potes, C., Schalk, G., & Curio, G. (2014)**. ECoG high gamma activity reveals distinct cortical representations of lyrics passages, harmonic and timbre-related changes in a rock song. *Frontiers in Human Neuroscience*, 8, 798.
11. **Zatorre, R. J., & Halpern, A. R. (2005)**. Mental concerts: Musical imagery and auditory cortex. *Neuron*, 47(1), 9-12.
12. **Criscuolo, A., Pando-Naude, V., Bonetti, L., Vuust, P., & Brattico, E. (2022)**. An ALE meta-analytic review of musical expertise. *Scientific Reports*, 12, 11726.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Output dimensions | 11D | **10D** (removed 1 redundant output) |
| Timbre response | S⁰.tristimulus[68:71] x HC⁰.HRM | R³.tristimulus[18:21] x instrument_identity |
| Specificity | S⁰.spectral_contrast[53] x HC⁰.ATT | R³.warmth[12] x R³.sharpness[13] x plasticity |
| Plasticity | S⁰.attack_time[50] x HC⁰.EFC | f01 x H³.timbre_change_std x plasticity |
| Template | S⁰.X_L5L6[208:216] x HC⁰.BND | R³.x_l5l7[41:47] x instrument_identity |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 16/2304 = 0.69% | 12/2304 = 0.52% |

### Key Index Migrations

| D0 (S⁰) | MI (R³) | Feature |
|----------|---------|---------|
| S⁰.brightness[34] | R³.warmth[12] | Different naming, related spectral concept |
| S⁰.warmth[37] | R³.warmth[12] | Direct mapping |
| S⁰.tristimulus[68:71] | R³.tristimulus[18:21] | Same concept, new indices |
| S⁰.inharmonicity[66] | R³.inharmonicity[5] | Same concept, new index |
| S⁰.spectral_irregularity[62] | R³.harmonic_deviation[6] | Related spectral measure |
| S⁰.band_ratios[80:86] | R³.x_l5l7[41:47] | Cross-band → interaction features |
| S⁰.X_L5L6[208:216] | R³.x_l5l7[41:49] | Interaction space consolidated |

---

**Model Status**: Validated
**Output Dimensions**: **10D**
**Evidence Tier**: **β (Integrative)**
**Confidence**: **70-90%**
