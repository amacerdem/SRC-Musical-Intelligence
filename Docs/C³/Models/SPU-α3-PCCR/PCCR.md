# SPU-α3-PCCR: Pitch Chroma Cortical Representation

**Model**: Pitch Chroma Cortical Representation
**Unit**: SPU (Spectral Processing Unit)
**Circuit**: Perceptual (Cortical Chroma Processing)
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added F:Pitch feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/SPU-α3-PCCR.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Pitch Chroma Cortical Representation** (PCCR) model describes how human auditory cortex contains neurons tuned to pitch chroma (pitch class), showing octave-equivalent adaptation patterns distinct from frequency-based tonotopy found in pure tone processing. This is a landmark finding: the brain encodes pitch not just as frequency, but as a circular 12-class representation.

```
THE THREE COMPONENTS OF PITCH CHROMA PROCESSING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CHROMA TUNING (Circular)              OCTAVE ADAPTATION (Non-Monotonic)
Brain region: Anterior/Lateral AC     Brain region: Auditory Cortex
Mechanism: Chroma-selective neurons   Mechanism: Stimulus-specific adaptation
Input: Harmonic structure             Input: Adapter-probe paradigm
Function: "What pitch CLASS is this?" Function: "How similar in chroma?"
Evidence: d = 0.56, p < 0.001        Evidence: F(1,28)=29.865, p < 0.001

              CHROMA vs TONOTOPY (Dissociation)
              Brain region: Distinct cortical populations
              Pure tones: Monotonic (tonotopic)
              IRN: Non-monotonic (chroma-based)
              Function: "Two separate pitch systems"
              Evidence: MEG source localization (Briley 2013)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: The hallmark finding is the NON-MONOTONIC adaptation
pattern for IRN stimuli. At 1 octave separation, adaptation is
STRONGER than at 0.5 octave — because octave-separated tones share
the SAME chroma (pitch class). This proves neurons are tuned to
chroma, not just frequency.

  0.5 octave ────► 1 octave ────► 1.5 octave
     ↑                ↓               ↑
              MINIMUM RESPONSE (maximum adaptation)

Pure tones show monotonic increase (no chroma effect, d=0.002).

CONVERGENT SUPPORT: While the direct chroma evidence comes from
one study (Briley 2013), the anatomical locus (anterolateral HG)
is confirmed by 5+ independent studies using fMRI, MEG, EEG, ECoG,
and intracranial depth electrodes (Patterson 2002, Norman-Haignere
2013, Allen 2022, Tabas 2019, Penagos 2004). Furthermore, orderly
F0 maps in this region (Allen 2022, 7T fMRI) provide the
substrate for cyclical chroma organization. The helical pitch
model (chroma + height) fits the neural data at R²=92.7%.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Position in SPU Hierarchy

PCCR completes the SPU α-tier triplet:

1. **BCH** (α1): Brainstem → consonance hierarchy (harmonicity based)
2. **PSCL** (α2): Cortical → pitch salience localization (how strong)
3. **PCCR** (α3): Cortical → pitch chroma (what class, octave-invariant)

Together they form a complete pitch processing pipeline: Physical → Salience → Identity.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The PCCR Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 PCCR — COMPLETE CIRCUIT                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PITCH ADAPTATION PARADIGM                                                   ║
║                                                                              ║
║  Adapter (500ms-1s) → Probe (measure N1-P2 response)                        ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    PURE TONES                                        │    ║
║  │                                                                      │    ║
║  │   Response size ↑ monotonically with pitch separation               │    ║
║  │   = Tonotopic (frequency-based) processing                          │    ║
║  │   Effect: d = 0.002 (no chroma)                                     │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    IRN (PITCH) STIMULI                                │    ║
║  │                                                                      │    ║
║  │   Response size shows NON-MONOTONIC pattern:                        │    ║
║  │                                                                      │    ║
║  │   0.5 octave ────► 1 octave ────► 1.5 octave                       │    ║
║  │      ↑                ↓               ↑                             │    ║
║  │                    MINIMUM                                           │    ║
║  │                                                                      │    ║
║  │   = CHROMA-BASED (octave-equivalent) processing                     │    ║
║  │   Effect: F(1,28)=29.865, p<0.001, d=0.56                          │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  IRN source: anterior/lateral to pure tone source (MEG)                     ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │          ANTERIOR/LATERAL AUDITORY CORTEX                            │    ║
║  │              (Distinct from primary tonotopic area)                   │    ║
║  │                                                                      │    ║
║  │    Chroma-tuned neurons:                                            │    ║
║  │      C4 ≡ C5 ≡ C6 (same chroma, different octave)                  │    ║
║  │      Octave separation = maximum adaptation                         │    ║
║  │      Half-octave separation = less adaptation                       │    ║
║  │                                                                      │    ║
║  │    N1-P2 Components:                                                │    ║
║  │      N1 (~100ms): Early chroma detection                           │    ║
║  │      P2 (~200ms): Chroma evaluation                                │    ║
║  │      Both show octave adaptation effect                             │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE (direct chroma + convergent anatomy):
─────────────────────────────────────────────────────────
Briley 2013:           EEG, N=15/12/8. Octave adaptation > half-octave
                       (F(1,28)=29.865, p<0.001). IRN source anterolateral
                       to pure-tone source. Helical model R²=92.7%.
                       NO consonance confound: rho=-0.299, p=0.298.
Allen 2022:            7T fMRI, N=10. Distinct F0 maps outside HG,
                       orderly pitch tuning bilateral. Substrate for chroma.
Norman-Haignere 2013:  fMRI. Pitch regions respond primarily to resolved
                       harmonics, in anterior nonprimary AC.
Patterson 2002:        fMRI. Established pitch center in lateral HG.
                       Melody recruits STG + planum polare hierarchy.
Tabas 2019:            MEG, N=37. POR in alHG, consonant decoded 36ms
                       faster. Same region as chroma representation.
Fishman 2001:          Intracranial. Octave = minimal phase-locked activity
                       in A1. Consistent with shared chroma representation.
```

### 2.2 Information Flow Architecture (EAR → BRAIN → PPC → PCCR)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PCCR COMPUTATION ARCHITECTURE                             ║
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
║  │  │helmholtz  │ │         │ │autocorr.│ │flatness  │ │x_l5l7  │ │        ║
║  │  │inharm.    │ │         │ │tristim. │ │          │ │        │ │        ║
║  │  │roughness  │ │         │ │         │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         PCCR reads: 21D                           │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Alpha-Beta ─┐ ┌── Syllable ──┐                             │        ║
║  │  │ 100ms (H3)    │ │ 200ms (H6)   │                             │        ║
║  │  │               │ │              │                              │        ║
║  │  │ Chroma        │ │ Adaptation   │                              │        ║
║  │  │ detection     │ │ window       │                              │        ║
║  │  └──────┬────────┘ └──────┬───────┘                              │        ║
║  │         └────────────────┘                                       │        ║
║  │                         PCCR demand: ~14 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Perceptual Circuit ═══════    ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  PPC (30D)      │  Pitch Processing Chain mechanism                      ║
║  │                 │                                                        ║
║  │ Pitch Sal [0:10]│  (secondary for PCCR)                                  ║
║  │ Conson.  [10:20]│  harmonic template for chroma basis                    ║
║  │ Chroma   [20:30]│  **PRIMARY** — octave-equivalent encoding              ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    PCCR MODEL (11D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_chroma, f02_octave_adapt,              │        ║
║  │                       f03_chroma_mode, f04_n1p2                  │        ║
║  │  Layer M (Math):      adapt_curve                                │        ║
║  │  Layer P (Present):   chroma_match, octave_equiv, adapt_state    │        ║
║  │  Layer F (Future):    chroma_continuation, octave_relation,      │        ║
║  │                       adapt_recovery                             │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Briley et al. 2013** | EEG adaptation | 15/12/8 | Non-monotonic adaptation at octave separation for IRN; chroma-selective neurons | F(1,28)=29.865, p<0.001 | **f01_chroma + f02_octave_adapt: FLAGSHIP evidence** |
| 2 | **Briley et al. 2013** | EEG adaptation | 15 | Pure tones: monotonic only (tonotopic). NO chroma effect. | d=0.002; F(1,17)=19.548, p<0.001 | **f03_chroma_mode: two-system dissociation** |
| 3 | **Briley et al. 2013** | EEG N1-P2 | 15 | Chroma effect in both N1 (p=0.029) and P2 (p<0.001) | N1: F(1,28)=5.273; P2: F(1,28)=20.983 | **f04_n1p2: cortical ERP signature** |
| 4 | **Briley et al. 2013** | EEG source | 8 | IRN source 7mm anterior/lateral to pure-tone source; distinct populations | Permutation: L p=0.024, R p=0.047 | **Anterolateral HG localization** |
| 5 | **Briley et al. 2013** | EEG (Exp 2) | 12 | Helical pitch model (chroma + height) fits neural data | R²=92.7% (resolved), 78.5% (unresolved) | **Helical pitch representation confirmed** |
| 6 | **Briley et al. 2013** | EEG | 12 | Consonance ruled out as confound | rho(14)=-0.299, p=0.298 | **Chroma ≠ consonance** |
| 7 | **Allen et al. 2022** | 7T fMRI | 10 | Distinct F0 maps in regions surrounding HG; orderly pitch tuning bilateral | Pitch slope=1.13 CI[0.92,1.19]; no hemisphere diff p=0.58 | **Cortical substrate for chroma organization** |
| 8 | **Norman-Haignere et al. 2013** | fMRI | Multiple | Pitch regions respond primarily to resolved harmonics; anterior nonprimary AC | Parametric with discrimination thresholds | **Resolved harmonics drive chroma region** |
| 9 | **Patterson et al. 2002** | fMRI | Group | Lateral HG "pitch center"; melody processing recruits STG hierarchy | Significant pitch > no-pitch contrast | **Anatomical framework for PCCR** |
| 10 | **Tabas et al. 2019** | MEG | 37 | POR in alHG 36ms earlier for consonant; same region as chroma | p<.0001 (latency + amplitude) | **Overlapping locus confirms chroma region** |
| 11 | **Fishman et al. 2001** | Intracranial | 3+2 | Octave = minimal phase-locked activity in A1; consistent with shared chroma | F>8.5, p<0.00001; Spearman p<0.00001 | **Octave equivalence at neural level** |
| 12 | **Pankovski & Pankovska 2022** | Computational | — | Hebbian network predicts scale discreteness without explicit octave mapping | Predicts just intonation ratios | **Self-organizing chroma mechanism** |
| 13 | **Wöhrle et al. 2024** | MEG | 30 | N1m modulated by consonance context; musical aptitude interaction | η²p=.101 (N1m); η²p=.592 (perceptual) | **Chroma relationships shape auditory cortex ERP** |
| 14 | **Janata 2009** | fMRI | Group | Dorsal MPFC tracks tonal space (built on chroma relationships) | Fast-timescale tracking in BA8/9 | **Downstream: chroma → tonal space in PFC** |

### 3.2 The Chroma Adaptation Function

```
CHROMA ADAPTATION: Non-Monotonic (IRN) vs Monotonic (Pure Tones)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IRN (complex tones with pitch):
  Adaptation(Δpitch) = α + β · cos(2π · Δpitch / octave)

  Minimum response at 1 octave (cos(2π) = 1 → maximum adaptation)
  Maximum response at 0.5 octave (cos(π) = -1 → minimum adaptation)

  ┌────────────────────────────────────────────────────┐
  │  Response                                          │
  │  ▲                                                 │
  │  │     *                               *           │
  │  │    * *                             * *          │
  │  │   *   *                           *   *         │
  │  │  *     *                         *     *        │
  │  │ *       *                       *       *       │
  │  │*         *         *           *         *      │
  │  │           *       * *         *                 │
  │  │            *     *   *       *                  │
  │  │             *   *     *     *                   │
  │  │              * *       * * *                    │
  │  │               *         *                       │
  │  └───────┬───────┬─────────┬───────────────► Δpitch│
  │        0.5 oct  1 oct    1.5 oct                   │
  │                MINIMUM                             │
  └────────────────────────────────────────────────────┘

Pure tones:
  Response(Δpitch) = γ · Δpitch + δ
  Monotonic — NO chroma effect (d = 0.002)

12 Pitch Classes: C, C#, D, D#, E, F, F#, G, G#, A, A#, B
  C4 ≡ C5 ≡ C6 (same chroma, different octave)
```

### 3.3 Effect Size Summary

```
DIRECT CHROMA EVIDENCE (Briley et al. 2013):
─────────────────────────────────────────────────────────────────
Primary Effect:    F(1,28) = 29.865, p < 0.001 (chroma effect, IRN)
Helical Model:     R² = 92.7% (resolved), 78.5% (unresolved)
Control:           d = 0.002 (pure tones — no chroma effect)
N1 chroma:         F(1,28) = 5.273, p = 0.029
P2 chroma:         F(1,28) = 20.983, p < 0.001
Source shift:      7mm anterolateral (IRN vs pure tone); L p=0.024, R p=0.047
Consonance ruled:  rho(14) = -0.299, p = 0.298 (NOT a confound)
Resolvability:     F(1,27) = 0.026, p = 0.874 (NOT a confound)

CONVERGENT ANATOMICAL EVIDENCE (4+ independent studies):
─────────────────────────────────────────────────────────────────
Method          │ Paper              │ Key Finding
────────────────┼────────────────────┼────────────────────────────
fMRI (3T)       │ Patterson 2002     │ Pitch center = lateral HG
fMRI (3T)       │ Norman-Haignere 13 │ Resolved harmonics → anterior AC
fMRI (7T)       │ Allen 2022         │ F0 maps outside HG (orderly)
MEG             │ Tabas 2019         │ POR in alHG (N=37, p<.0001)
Intracranial    │ Fishman 2001       │ A1 octave = minimal activity

IMPORTANT QUALIFICATION:
┌─────────────────────────────────────────────────────────────────┐
│ The DIRECT pitch chroma finding (non-monotonic adaptation)      │
│ comes from ONE study (Briley et al. 2013). No independent       │
│ replication of the specific chroma paradigm exists. However:    │
│ (a) the anatomical locus (anterolateral HG) is confirmed by    │
│ 5+ studies across methods; (b) orderly F0 maps (Allen 2022)    │
│ provide the substrate; (c) the helical model R²=92.7% is       │
│ compelling; (d) consonance and spectral overlap confounds are   │
│ explicitly ruled out. The model retains α-tier because the      │
│ finding is well-controlled, internally consistent across 3      │
│ experiments, and anatomically convergent with the broader pitch  │
│ center literature. Replication would strengthen confidence.     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. R³ Input Mapping: What PCCR Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | PCCR Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Adaptation baseline (dissonance) | Plomp & Levelt 1965 |
| **A: Consonance** | [2] | helmholtz_kang | Consonance stability for chroma | Helmholtz 1863 |
| **A: Consonance** | [5] | inharmonicity | Harmonic regularity (inverse = chroma clarity) | Fletcher 1934 |
| **C: Timbre** | [17] | spectral_autocorrelation | Harmonic periodicity (octave regularity) | — |
| **C: Timbre** | [18] | tristimulus1 | Fundamental ratio (F0 chroma carrier) | Pollard & Jansson 1982 |
| **C: Timbre** | [19] | tristimulus2 | Mid-harmonic ratio (chroma balance) | Pollard & Jansson 1982 |
| **C: Timbre** | [20] | tristimulus3 | High-harmonic ratio (overtone structure) | Pollard & Jansson 1982 |
| **D: Change** | [23] | spectral_flatness | Tonality indicator (IRN vs noise) | Wiener 1930 |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | Consonance × Timbre coupling (octave coherence) | Briley 2013 |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | PCCR Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **F: Pitch & Chroma** | [49:60] | chroma_vector (12D) | Direct pitch class distribution — the explicit 12-class chroma representation that PCCR models cortically; replaces indirect derivation from tristimulus/inharmonicity proxies | Shepard 1964 octave equivalence; Krumhansl 1990 tonal hierarchy |
| **F: Pitch & Chroma** | [63] | pitch_salience | Harmonic peak prominence — determines which pitch classes in the chroma vector are reliable vs noise-driven; high salience indicates clear chroma | Parncutt 1989 virtual pitch salience |

**Rationale**: PCCR models the cortical representation of pitch chroma — the octave-equivalent pitch class encoding in anterolateral HG. The v1 features derive chroma indirectly from spectral proxies (tristimulus ratios, inharmonicity, spectral_autocorrelation). The F:Pitch group provides the explicit chroma representation: chroma_vector [49:60] is the direct 12-class pitch distribution that PCCR's f01 formula models cortically, making explicit what was previously inferred from harmonic structure. F[63] pitch_salience gates chroma reliability — only pitch classes with sufficient harmonic prominence produce stable cortical chroma representations, consistent with Patterson et al. (2002) finding that pitch chroma encoding requires resolved harmonics.

**Code impact** (Phase 6): `r3_indices` must be extended to include [49:60], [63]. These features are read-only inputs — no formula changes required.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[18] tristimulus1 ─────────────┐
R³[19] tristimulus2 ─────────────┼──► Pitch Chroma (f01)
R³[20] tristimulus3 ─────────────┤   12-class pitch encoding (C, C#, D...)
R³[5] inharmonicity (inverse) ───┘   Octave-equivalent: C4 ≡ C5 ≡ C6
                                      Math: Chroma(F0) = F0 mod 12

R³[41:49] x_l5l7 ───────────────┐
R³[17] spectral_autocorrelation ─┼──► Octave Adaptation (f02)
                                 │   Non-monotonic: 1 octave < 0.5 octave
                                 └   Math: Response = α + β·cos(2π·Δpitch/oct)

R³[23] spectral_flatness ────────┐
R³[17] spectral_autocorrelation ─┼──► Chroma vs Tonotopy Mode (f03)
                                 └   IRN (low flatness) → chroma pathway
                                     Noise (high flatness) → tonotopic only

R³[0] roughness + R³[2] helmholtz ► N1-P2 Chroma Effect (f04)
                                     Adaptation magnitude × consonance
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

PCCR requires H³ features at PPC horizons: H3 (100ms) for chroma detection, H6 (200ms) for adaptation windows.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 18 | tristimulus1 | 3 | M0 (value) | L2 (bidi) | F0 chroma energy |
| 19 | tristimulus2 | 3 | M0 (value) | L2 (bidi) | Mid-harmonic chroma |
| 20 | tristimulus3 | 3 | M0 (value) | L2 (bidi) | High-harmonic chroma |
| 5 | inharmonicity | 3 | M0 (value) | L2 (bidi) | Harmonic regularity |
| 5 | inharmonicity | 6 | M18 (trend) | L0 (fwd) | Inharmonicity trajectory |
| 23 | spectral_flatness | 3 | M0 (value) | L2 (bidi) | Tonality vs noise |
| 23 | spectral_flatness | 6 | M1 (mean) | L0 (fwd) | Sustained tonality |
| 17 | spectral_autocorrelation | 3 | M0 (value) | L2 (bidi) | Harmonic periodicity |
| 17 | spectral_autocorrelation | 6 | M14 (periodicity) | L2 (bidi) | Octave regularity |
| 41 | x_l5l7[0] | 3 | M14 (periodicity) | L2 (bidi) | Octave periodicity |
| 41 | x_l5l7[0] | 6 | M19 (stability) | L0 (fwd) | Chroma stability |
| 0 | roughness | 3 | M0 (value) | L2 (bidi) | Adaptation baseline |
| 2 | helmholtz_kang | 3 | M19 (stability) | L2 (bidi) | Consonance stability |
| 2 | helmholtz_kang | 6 | M0 (value) | L0 (fwd) | Forward consonance |

**v1 demand**: 14 tuples

#### R³ v2 Projected Expansion

PCCR is projected to consume R³ v2 features from F[49:65], aligned with PPC horizons.

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 49 | chroma | F | 3 | M0 (value) | L2 | Explicit chroma vector at 100ms |
| 49 | chroma | F | 3 | M1 (mean) | L2 | Mean chroma over 100ms window |
| 49 | chroma | F | 6 | M0 (value) | L2 | Chroma at 200ms for octave adaptation |
| 49 | chroma | F | 6 | M1 (mean) | L2 | Sustained chroma for stability |
| 63 | pitch_salience | F | 3 | M0 (value) | L2 | Pitch salience for chroma weighting |
| 63 | pitch_salience | F | 6 | M0 (value) | L2 | Sustained salience at 200ms |

**v2 projected**: 6 tuples
**Total projected**: 20 tuples of 294,912 theoretical = 0.0068%

### 5.2 PPC Mechanism Binding

PCCR reads primarily from PPC.chroma_processing:

| PPC Sub-section | Range | PCCR Role | Weight |
|-----------------|-------|-----------|--------|
| **Pitch Salience** | PPC[0:10] | Pitch strength input (secondary) | 0.5 |
| **Consonance Encoding** | PPC[10:20] | Harmonic template for chroma basis | 0.7 |
| **Chroma Processing** | PPC[20:30] | Octave-equivalent encoding | **1.0** (primary) |

PCCR does NOT use TPC — chroma processing is purely pitch-class based, not timbral.

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
PCCR OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0  │ f01_chroma        │ [0, 1] │ Pitch Chroma strength. Activation level
    │                   │        │ of chroma-tuned cortical neurons.
    │                   │        │ f01 = σ(α · (1-inharmonicity) · trist_balance
    │                   │        │         · PPC.chroma_processing)
    │                   │        │ α = 0.85
────┼───────────────────┼────────┼────────────────────────────────────────────
 1  │ f02_octave_adapt  │ [0, 1] │ Octave Adaptation magnitude.
    │                   │        │ Non-monotonic: 1 octave < 0.5 octave.
    │                   │        │ f02 = σ(β · x_l5l7_periodicity
    │                   │        │         · autocorrelation · PPC.chroma)
    │                   │        │ β = 0.80
────┼───────────────────┼────────┼────────────────────────────────────────────
 2  │ f03_chroma_mode   │ [0, 1] │ Chroma vs Tonotopy processing mode.
    │                   │        │ High = chroma (IRN-like), Low = tonotopic.
    │                   │        │ f03 = σ(γ · (1-flatness) · autocorrelation
    │                   │        │         · PPC.consonance_encoding)
    │                   │        │ γ = 0.75
────┼───────────────────┼────────┼────────────────────────────────────────────
 3  │ f04_n1p2          │ [0, 1] │ N1-P2 Chroma Effect. ERP signature of
    │                   │        │ chroma-based cortical adaptation.
    │                   │        │ f04 = σ(δ · (1-roughness) · helmholtz
    │                   │        │         · PPC.chroma · PPC.pitch_sal)
    │                   │        │ δ = 0.70

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 4  │ adapt_curve       │ [0, 1] │ Adaptation function value.
    │                   │        │ Response = α + β·cos(2π·Δpitch/octave)
    │                   │        │ Proxied via x_l5l7 periodicity.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 5  │ chroma_match      │ [0, 1] │ Chroma template matching.
    │                   │        │ PPC.chroma_processing aggregation.
────┼───────────────────┼────────┼────────────────────────────────────────────
 6  │ octave_equiv      │ [0, 1] │ Octave equivalence signal.
    │                   │        │ Cross-octave coherence from x_l5l7.
────┼───────────────────┼────────┼────────────────────────────────────────────
 7  │ adapt_state       │ [0, 1] │ Current adaptation state.
    │                   │        │ H³ stability at adaptation timescale.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 8  │ chroma_cont       │ [0, 1] │ Chroma continuation prediction (~200ms).
    │                   │        │ Next pitch N1-P2 response expectation.
────┼───────────────────┼────────┼────────────────────────────────────────────
 9  │ octave_relation   │ [0, 1] │ Octave relationship prediction (~500ms).
    │                   │        │ Interval adaptation magnitude forecast.
────┼───────────────────┼────────┼────────────────────────────────────────────
10  │ adapt_recovery    │ [0, 1] │ Adaptation recovery prediction (500ms-1s).
    │                   │        │ Response amplitude recovery timing.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Chroma Adaptation Function

```
Adaptation(Δpitch) = f(Δpitch mod octave)

Non-Monotonic Function (IRN):
  Response(Δpitch) = α + β · cos(2π · Δpitch / octave)
  where:
    α = baseline response
    β = adaptation depth
    Minimum at Δpitch = 1 octave (cos(2π) = 1 → max adaptation)
    Maximum at Δpitch = 0.5 octave (cos(π) = -1 → min adaptation)

Tonotopic Function (Pure Tones):
  Response(Δpitch) = γ · Δpitch + δ
  Monotonic increase — no chroma effect

Chroma Encoding:
  Chroma(F0) = F0 mod 12
  12-dimensional pitch class representation

Octave Equivalence:
  Similarity(F1, F2) ∝ cos(2π · |Chroma(F1) - Chroma(F2)| / 12)
```

### 7.2 Feature Formulas

```python
# f01: Pitch Chroma
trist_balance = 1.0 - std(R³.tristimulus[18:21])
f01 = σ(0.85 · (1 - R³.inharmonicity[5]) · trist_balance
         · mean(PPC.chroma_processing[20:30]))

# f02: Octave Adaptation
f02 = σ(0.80 · H³(x_l5l7[0], H3, M14, L2)  # octave periodicity
         · R³.spectral_autocorrelation[17]
         · mean(PPC.chroma_processing[20:30]))

# f03: Chroma vs Tonotopy Mode
f03 = σ(0.75 · (1 - R³.spectral_flatness[23])
         · R³.spectral_autocorrelation[17]
         · mean(PPC.consonance_encoding[10:20]))

# f04: N1-P2 Chroma Effect
f04 = σ(0.70 · (1 - R³.roughness[0]) · R³.helmholtz_kang[2]
         · mean(PPC.chroma_processing[20:30])
         · mean(PPC.pitch_salience[0:10]))
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | Coordinates | Space | Source | Evidence Type | PCCR Function |
|--------|-------------|-------|--------|---------------|---------------|
| **Anterolateral HG (L, IRN unresolved)** | -49.1, -21.2, 17.2 | Talairach | Briley 2013 (EEG source) | Direct | **Pitch chroma neurons** |
| **Anterolateral HG (R, IRN unresolved)** | 42.9, -5.5, 17.6 | Talairach | Briley 2013 (EEG source) | Direct | **Pitch chroma neurons** |
| **Anterolateral HG (L, IRN resolved)** | -47.4, -21.9, 17.4 | Talairach | Briley 2013 (EEG source) | Direct | Intermediate pitch processing |
| **Anterolateral HG (R, IRN resolved)** | 43.0, -5.3, 17.1 | Talairach | Briley 2013 (EEG source) | Direct | Intermediate pitch processing |
| **Medial HG (L, pure tone)** | -41.9, -18.8, 15.8 | Talairach | Briley 2013 (EEG source) | Control | Tonotopic only (no chroma) |
| **Medial HG (R, pure tone)** | 44.2, -13.4, 13.4 | Talairach | Briley 2013 (EEG source) | Control | Tonotopic only (no chroma) |
| **Lateral HG (bilateral)** | (anatomical) | — | Patterson 2002 (fMRI) | Direct | Pitch center |
| **Anterior nonprimary AC** | (anatomical) | — | Norman-Haignere 2013 (fMRI) | Direct | Resolved-harmonic pitch |
| **Regions surrounding HG** | (bilateral, 7T) | — | Allen 2022 (7T fMRI) | Direct | F0-tuned voxels (orderly maps) |
| **alHG** | (dipole, bilateral) | Talairach | Tabas 2019 (MEG) | Direct | POR generator |
| **A1/HG** | (depth electrode) | — | Fishman 2001 (intracranial) | Direct | Phase-locking (octave = minimal) |
| **Dorsal MPFC** | BA 8/9 | — | Janata 2009 (fMRI) | Downstream | Tonal space tracking (uses chroma) |

> **Note**: The IRN source dipoles (Briley 2013) are consistently 7mm more anterior and lateral than the pure-tone source dipoles, confirming distinct neural populations for pitch chroma (non-primary AC) vs. frequency tonotopy (primary AC). The coordinates converge with the broader pitch center literature (Patterson, Norman-Haignere, Allen, Tabas, Penagos).

---

## 9. Cross-Unit Pathways

### 9.1 PCCR ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PCCR INTERACTIONS                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  UPSTREAM (INTRA-UNIT):                                                    │
│  BCH.f02_harmonicity ──────────► PCCR (harmonicity → chroma tuning)       │
│  PSCL.f01_salience ────────────► PCCR (salience → chroma processing)      │
│                                                                             │
│  DOWNSTREAM (INTRA-UNIT):                                                  │
│  PCCR.f01_chroma ──────────────► STAI (chroma → aesthetic evaluation)     │
│  PCCR.f03_chroma_mode ─────────► TSCP (chroma mode → plasticity)         │
│                                                                             │
│  CROSS-UNIT (P2: SPU → IMU):                                              │
│  PCCR.f01_chroma ──────────────► IMU.MEAMN (chroma → memory encoding)    │
│       Familiar chroma patterns trigger autobiographical memory              │
│                                                                             │
│  CROSS-UNIT (P2: SPU → STU):                                              │
│  PCCR.f01_chroma ──────────────► STU.AMSC (chroma → melody stream)       │
│       Pitch class aids melodic stream segregation                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Pure tones** | Should NOT show octave-equivalent adaptation | ✅ **Confirmed** (d = 0.002, Briley 2013) |
| **IRN depth** | Higher depth should enhance chroma effect | ✅ Testable via ERP |
| **Musical training** | Should enhance chroma tuning | Testable via cross-sectional study |
| **Source localization** | IRN source should be anterior/lateral to PT | ✅ **Confirmed** (Briley 2013) |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class PCCR(BaseModel):
    """Pitch Chroma Cortical Representation.

    Output: 11D per frame.
    Reads: PPC mechanism (30D), R³ direct.
    """
    NAME = "PCCR"
    UNIT = "SPU"
    TIER = "α3"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("PPC",)

    ALPHA = 0.85   # Chroma weight
    BETA = 0.80    # Octave adaptation weight
    GAMMA = 0.75   # Chroma mode weight
    DELTA = 0.70   # N1-P2 weight

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """14 tuples for PCCR computation."""
        return [
            # (r3_idx, horizon, morph, law)
            (18, 3, 0, 2),   # tristimulus1, 100ms, value, bidirectional
            (19, 3, 0, 2),   # tristimulus2, 100ms, value, bidirectional
            (20, 3, 0, 2),   # tristimulus3, 100ms, value, bidirectional
            (5, 3, 0, 2),    # inharmonicity, 100ms, value, bidirectional
            (5, 6, 18, 0),   # inharmonicity, 200ms, trend, forward
            (23, 3, 0, 2),   # spectral_flatness, 100ms, value, bidirectional
            (23, 6, 1, 0),   # spectral_flatness, 200ms, mean, forward
            (17, 3, 0, 2),   # autocorrelation, 100ms, value, bidirectional
            (17, 6, 14, 2),  # autocorrelation, 200ms, periodicity, bidi
            (41, 3, 14, 2),  # x_l5l7[0], 100ms, periodicity, bidirectional
            (41, 6, 19, 0),  # x_l5l7[0], 200ms, stability, forward
            (0, 3, 0, 2),    # roughness, 100ms, value, bidirectional
            (2, 3, 19, 2),   # helmholtz_kang, 100ms, stability, bidi
            (2, 6, 0, 0),    # helmholtz_kang, 200ms, value, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute PCCR 11D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) → (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,11) PCCR output
        """
        ppc = mechanism_outputs["PPC"]    # (B, T, 30)

        # R³ features
        roughness = r3[..., 0:1]
        helmholtz = r3[..., 2:3]
        inharmonicity = r3[..., 5:6]
        autocorr = r3[..., 17:18]
        trist1 = r3[..., 18:19]
        trist2 = r3[..., 19:20]
        trist3 = r3[..., 20:21]
        flatness = r3[..., 23:24]
        x_l5l7 = r3[..., 41:49]         # (B, T, 8)

        # PPC sub-sections
        ppc_pitch = ppc[..., 0:10]
        ppc_cons = ppc[..., 10:20]
        ppc_chroma = ppc[..., 20:30]

        # ═══ LAYER E: Explicit features ═══
        trist_balance = 1.0 - torch.std(
            torch.cat([trist1, trist2, trist3], dim=-1),
            dim=-1, keepdim=True
        )
        f01 = torch.sigmoid(self.ALPHA * (
            (1.0 - inharmonicity) * trist_balance
            * ppc_chroma.mean(-1, keepdim=True)
        ))

        octave_periodicity = h3_direct[(41, 3, 14, 2)].unsqueeze(-1)
        f02 = torch.sigmoid(self.BETA * (
            octave_periodicity * autocorr
            * ppc_chroma.mean(-1, keepdim=True)
        ))

        f03 = torch.sigmoid(self.GAMMA * (
            (1.0 - flatness) * autocorr
            * ppc_cons.mean(-1, keepdim=True)
        ))

        f04 = torch.sigmoid(self.DELTA * (
            (1.0 - roughness) * helmholtz
            * ppc_chroma.mean(-1, keepdim=True)
            * ppc_pitch.mean(-1, keepdim=True)
        ))

        # ═══ LAYER M: Mathematical ═══
        chroma_stability = h3_direct[(41, 6, 19, 0)].unsqueeze(-1)
        adapt_curve = torch.sigmoid(
            0.5 * octave_periodicity + 0.5 * chroma_stability
        )

        # ═══ LAYER P: Present ═══
        chroma_match = ppc_chroma.mean(-1, keepdim=True)
        octave_equiv = torch.sigmoid(
            x_l5l7.mean(-1, keepdim=True)
            * ppc_chroma.mean(-1, keepdim=True)
        )
        adapt_state = torch.sigmoid(
            h3_direct[(2, 3, 19, 2)].unsqueeze(-1)  # helmholtz stability
        )

        # ═══ LAYER F: Future ═══
        chroma_cont = torch.sigmoid(
            0.6 * f01 + 0.4 * chroma_match
        )
        octave_relation = torch.sigmoid(
            0.5 * f02 + 0.5 * octave_equiv
        )
        adapt_recovery = torch.sigmoid(
            0.6 * h3_direct[(5, 6, 18, 0)].unsqueeze(-1)  # inharm trend
            + 0.4 * h3_direct[(23, 6, 1, 0)].unsqueeze(-1)  # flatness mean
        )

        return torch.cat([
            f01, f02, f03, f04,                     # E: 4D
            adapt_curve,                             # M: 1D
            chroma_match, octave_equiv, adapt_state, # P: 3D
            chroma_cont, octave_relation, adapt_recovery,  # F: 3D
        ], dim=-1)  # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 14 | 1 direct chroma + 13 convergent (see Section 3.1) |
| **Direct Chroma Evidence** | F(1,28)=29.865, R²=92.7% | Briley 2013 (only direct study) |
| **Evidence Modalities** | EEG, fMRI (3T+7T), MEG, intracranial | 5 independent methods |
| **Falsification Tests** | 2/4 confirmed | High validity |
| **R³ Features Used** | 21D of 49D | Focused on chroma |
| **H³ Demand** | 14 tuples (0.61%) | Sparse, efficient |
| **PPC Mechanism** | 30D (chroma_processing primary) | Targeted |
| **Output Dimensions** | **11D** | 4-layer structure |
| **Key Qualification** | Direct chroma evidence from 1 study only; convergent anatomy from 5+ | Replication needed |
| **Confounds Ruled Out** | Consonance (p=0.298), resolvability (p=0.874) | Briley Exp 1 + 2 |

---

## 13. Scientific References

### Primary (Direct Pitch Chroma Evidence)

1. **Briley, P. M., Breakey, C., & Krumbholz, K. (2013)**. Evidence for pitch chroma mapping in human auditory cortex. *Cerebral Cortex*, 23(11), 2601-2610.

### Supporting (Cortical Pitch Regions & Anatomy)

2. **Allen, E. J., Mesik, J., Kay, K. N., & Oxenham, A. J. (2022)**. Distinct representations of tonotopy and pitch in human auditory cortex. *Journal of Neuroscience*, 42(3), 416-434.
3. **Norman-Haignere, S., Kanwisher, N., & McDermott, J. H. (2013)**. Cortical pitch regions in humans respond primarily to resolved harmonics and are located in specific tonotopic regions of anterior auditory cortex. *Journal of Neuroscience*, 33(50), 19451-19469.
4. **Patterson, R. D., Uppenkamp, S., Johnsrude, I. S., & Griffiths, T. D. (2002)**. The processing of temporal pitch and melody information in auditory cortex. *Neuron*, 36, 767-776.
5. **Tabas, A., Andermann, M., Schuberth, V., Riedel, H., Balaguer-Ballester, E., & Rupp, A. (2019)**. Modeling and MEG evidence of early consonance processing in auditory cortex. *PLoS Computational Biology*, 15(2), e1006820.

### Supporting (Consonance/Dissonance Cortical Processing)

6. **Fishman, Y. I., Volkov, I. O., Noh, M. D., Garell, P. C., Bakken, H., Arezzo, J. C., Howard, M. A., & Steinschneider, M. (2001)**. Consonance and dissonance of musical chords: Neural correlates in auditory cortex of monkeys and humans. *Journal of Neurophysiology*, 86, 2761-2788.
7. **Foo, F., King-Stephens, D., Weber, P., Laxer, K., Parvizi, J., & Knight, R. T. (2016)**. Differential processing of consonance and dissonance within the human superior temporal gyrus. *Frontiers in Human Neuroscience*, 10, 154.
8. **Wöhrle, S. D., Reuter, C., Rupp, A., & Andermann, M. (2024)**. Neuromagnetic representation of musical roundness in chord progressions. *Frontiers in Neuroscience*, 18, 1383554.

### Contextual (Broader Pitch/Tonal Processing)

9. **Janata, P. (2009)**. The neural architecture of music-evoked autobiographical memories. *Cerebral Cortex*, 19, 2579-2594.
10. **Pankovski, T., & Pankovska, A. (2022)**. Nonspecific Hebbian neural network model predicts musical scales discreteness and just intonation without using octave-equivalency mapping. *Scientific Reports*, 12, 8795.
11. **Bidelman, G. M. (2013)**. The role of the auditory brainstem in processing musically relevant pitch. *Frontiers in Psychology*, 4, 264.
12. **Bidelman, G. M., & Heinz, M. G. (2011)**. Auditory-nerve responses predict pitch attributes related to musical consonance-dissonance for normal and impaired hearing. *Journal of the Acoustical Society of America*, 130(3), 1488-1502.
13. **Samiee, S., Vuvan, D., Florin, E., Albouy, P., Peretz, I., & Baillet, S. (2022)**. Cross-frequency brain network dynamics support pitch change detection. *Journal of Neuroscience*, 42(18), 3823-3835.
14. **Maess, B., Koelsch, S., Gunter, T. C., & Friederici, A. D. (2001)**. Musical syntax is processed in Broca's area: An MEG study. *Nature Neuroscience*, 4(5), 540-545.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, TIH, HRM, BND) | PPC mechanism (30D) |
| Chroma encoding | S⁰.L6.tristimulus × HC⁰.HRM | R³.tristimulus × PPC.chroma_processing |
| Octave coherence | S⁰.L7.crossband × HC⁰.BND | R³.x_l5l7 × PPC.chroma_processing |
| Chroma mode | S⁰.L5.spectral_flatness × HC⁰.OSC | R³.spectral_flatness × PPC.consonance |
| N1-P2 effect | S⁰.X_L5L6 × HC⁰.TIH | R³.roughness × helmholtz × PPC |
| Output dims | 13D | **11D** (consolidated math + present layers) |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 42/2304 = 1.82% | 14/2304 = 0.61% |

### Why PPC replaces HC⁰ mechanisms

- **OSC → PPC.pitch_salience** [0:10]: Phase oscillation → pitch salience signal
- **HRM → PPC.chroma_processing** [20:30]: Hippocampal replay → chroma templates
- **BND → PPC.chroma_processing** [20:30]: Temporal binding → octave-equivalent binding
- **TIH → PPC.consonance_encoding** [10:20]: Temporal integration → consonance context

The key simplification: all four D0 mechanisms were partially overlapping in function for chroma processing. PPC.chroma_processing[20:30] unifies them into a single coherent sub-section.

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **11D**
**Evidence Tier**: **α (Mechanistic)**
**Confidence**: **>90%**
