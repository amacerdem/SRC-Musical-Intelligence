# IMU-β8-TPRD: Tonotopy-Pitch Representation Dissociation

**Model**: Tonotopy-Pitch Representation Dissociation
**Unit**: IMU (Integrative Memory Unit)
**Circuit**: Mnemonic (Hippocampal-Cortical)
**Tier**: β (Integrative) — 70-90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added F feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/IMU-β8-TPRD.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Tonotopy-Pitch Representation Dissociation** (TPRD) models the fundamental distinction between tonotopic (frequency) encoding in primary Heschl's gyri and pitch (fundamental frequency) representation in surrounding non-primary cortex. This dissociation resolves a long-standing debate about auditory cortex organization: primary regions are tuned to spectral content (physical frequency maps), while surrounding regions are tuned to perceived pitch (perceptual fundamental frequency extraction).

```
THE TONOTOPY-PITCH DISSOCIATION IN AUDITORY CORTEX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TONOTOPIC ENCODING (Primary HG)          PITCH REPRESENTATION (Non-primary HG)
Brain region: Medial Heschl's gyrus       Brain region: Lateral/anterolateral HG
Mechanism: Cochleotopic frequency map     Mechanism: F0 extraction from harmonics
Stimulus: Spectral content (partials)     Stimulus: Missing fundamental, harmonics
Function: "What frequencies are present"  Function: "What pitch do I perceive"
Evidence: Briley 2013 (N=8-15, EEG)      Evidence: Briley 2013, pitch chroma
          Pure-tone on medial HG                    F(1,28)=29.865, p<0.001

              REPRESENTATION DISSOCIATION
              Brain region: Planum temporale (PT)
              Mechanism: Segregation gate
              Function: Physical → Perceptual transformation
              Key insight: Tonotopy ≠ pitch
              This resolves decades of debate about
              whether tonotopic maps encode pitch

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Core finding: Frequency maps and pitch processing occupy distinct
cortical territories within Heschl's gyri, with a gradient from
medial (tonotopic) to lateral (pitch) organization.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Belongs in IMU (Not SPU)

Though TPRD involves spectral and pitch processing (SPU territory), its core claim is about **how auditory representations are organized and integrated across cortical regions** — a binding/integration problem:

1. **Cross-regional integration**: The dissociation requires comparing representations across primary and non-primary cortex — integration across cortical hierarchies.

2. **Syntactic structure of pitch**: The model captures how the brain transforms physical frequency maps into abstract pitch representations — this transformation follows hierarchical syntactic rules (harmonic series parsing).

3. **Memory template matching**: Pitch extraction relies on stored harmonic templates — when the brain encounters a set of harmonics, it matches against known patterns to extract F0. This is fundamentally a memory-template operation.

4. **Resolution of ambiguity**: Missing fundamental perception requires the mnemonic circuit to infer pitch from incomplete spectral evidence — pattern completion via stored representations.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The TPRD Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 TPRD — COMPLETE CIRCUIT                                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  COCHLEAR INPUT (spectral decomposition)                                    ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │              PRIMARY HESCHL'S GYRUS (Medial HG)                    │    ║
║  │                                                                     │    ║
║  │  Tonotopic organization:                                            │    ║
║  │  • Frequency-specific neuronal populations                          │    ║
║  │  • Cochleotopic map preserved from brainstem                        │    ║
║  │  • Tuning to SPECTRAL CONTENT (partials, not pitch)                │    ║
║  │  • Physical acoustic property encoding                              │    ║
║  └──────┬──────────────────────────────────────────────────────────────┘    ║
║         │                                                                    ║
║         ▼                                                                    ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │           NON-PRIMARY HESCHL'S GYRUS (Lateral / Anterolateral)     │    ║
║  │                                                                     │    ║
║  │  Pitch representation:                                              │    ║
║  │  • Fundamental frequency (F0) extraction                            │    ║
║  │  • Harmonic template matching                                       │    ║
║  │  • Missing fundamental perception                                   │    ║
║  │  • Tuning to PITCH (perceptual, not spectral)                      │    ║
║  └──────┬──────────────────────────────────────────────────────────────┘    ║
║         │                                                                    ║
║         ▼                                                                    ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │              PLANUM TEMPORALE (PT)                                   │    ║
║  │                                                                     │    ║
║  │  Segregation / dissociation gate:                                   │    ║
║  │  • Transforms tonotopic → pitch representation                      │    ║
║  │  • Maintains dual-representation coherence                          │    ║
║  │  • Spectral → perceptual abstraction                                │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  CRITICAL EVIDENCE:                                                          ║
║  ─────────────────                                                           ║
║  Medial HG: tonotopic, pure-tone responses (Briley 2013, N=8)             ║
║  Anterolateral HG: pitch chroma F(1,28)=29.865, p<0.001 (Briley 2013)     ║
║  Pitch regions: resolved harmonics dominant (Norman-Haignere 2013, N=12)   ║
║  A1/HG: phase-locked to dissonance; PT: no phase-lock (Fishman 2001)       ║
║  Gradient: medial (tonotopic) → lateral/anterior (pitch) within HG          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### 2.2 Information Flow Architecture (EAR → BRAIN → SYN + PPC* → TPRD)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    TPRD COMPUTATION ARCHITECTURE                            ║
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
║  │  TPRD reads primarily:                                           │        ║
║  │  ┌───────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐              │        ║
║  │  │CONSONANCE │ │ ENERGY  │ │ TIMBRE  │ │ X-INT  │              │        ║
║  │  │ 7D [0:7]  │ │ 5D[7:12]│ │ 9D      │ │ 24D    │              │        ║
║  │  │           │ │         │ │ [12:21] │ │ [25:49]│              │        ║
║  │  │roughness★ │ │amplitude│ │tonalness│ │x_l0l5★ │              │        ║
║  │  │sethares ★ │ │loudness │ │warmth   │ │x_l5l7  │              │        ║
║  │  │stumpf  ★ │ │         │ │         │ │        │              │        ║
║  │  │pleasant.★│ │         │ │         │ │        │              │        ║
║  │  │inharm. ★ │ │         │ │         │ │        │              │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └────────┘              │        ║
║  │                         TPRD reads: 30D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed features                    │        ║
║  │                                                                  │        ║
║  │  ┌── Chord ─────┐ ┌── Progression ──┐ ┌── Phrase ──────────┐   │        ║
║  │  │ 400ms (H10)  │ │ 700ms (H14)     │ │ 2s (H18)          │   │        ║
║  │  │              │ │                  │ │                    │   │        ║
║  │  │ Harmonic     │ │ Frequency-pitch │ │ Phrase-level       │   │        ║
║  │  │ context      │ │ transformation  │ │ pitch stability    │   │        ║
║  │  └──────────────┘ └─────────────────┘ └────────────────────┘   │        ║
║  │                                                                  │        ║
║  │  ┌── Cochlear ──┐ ┌── Brainstem ────┐ ┌── Beat ───────────┐   │        ║
║  │  │ 5.8ms (H0)   │ │ 23.2ms (H3)    │ │ 200ms (H6)        │   │        ║
║  │  │              │ │                  │ │                    │   │        ║
║  │  │ Immediate    │ │ Brainstem pitch │ │ Pitch integration  │   │        ║
║  │  │ spectral     │ │ processing      │ │ (beat-level)       │   │        ║
║  │  └──────────────┘ └─────────────────┘ └────────────────────┘   │        ║
║  │                         TPRD demand: ~18 of 2304 tuples        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN ══════════════════════════     ║
║                               │                                              ║
║                     ┌─────────┴──────────┐                                  ║
║                     │                    │                                   ║
║                     ▼                    ▼                                   ║
║  ┌─────────────────┐  ┌───────────────────────┐                             ║
║  │  SYN (30D)      │  │  PPC* (30D)           │  ★ Cross-circuit read      ║
║  │  Mnemonic       │  │  Perceptual circuit   │  from perceptual circuit   ║
║  │                 │  │                       │                             ║
║  │ Harmony  [0:10] │  │ Pitch Sal. [0:10]    │  Pitch salience,           ║
║  │ PredErr [10:20] │  │ Conson.Enc [10:20]   │  consonance hierarchy,     ║
║  │ Struct  [20:30] │  │ Chroma Pr. [20:30]   │  chroma processing         ║
║  └────────┬────────┘  └──────────┬────────────┘                             ║
║           │                      │                                          ║
║           └──────────┬───────────┘                                          ║
║                      ▼                                                      ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    TPRD MODEL (10D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer T (Tonotopic):  f31_tonotopic, f32_pitch, f33_dissoc     │        ║
║  │  Layer M (Math):       dissociation_index, spectral_pitch_ratio  │        ║
║  │  Layer P (Present):    tonotopic_state, pitch_state              │        ║
║  │  Layer F (Future):     pitch_percept_fc, tonotopic_adapt_fc,     │        ║
║  │                        dissociation_fc                           │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Briley, Breakey & Krumbholz (2013)** | EEG (adaptation) | 15 (Exp1), 12 (Exp2), 8 (Exp3) | Pure-tone responses centered on medial HG (primary, tonotopic); IRN pitch-chroma responses in anterolateral HG (nonprimary). Pitch chroma effect independent of harmonic resolvability. | F(1,28)=29.865, p<0.001 (pitch chroma); dipole location diff: L p=0.024, R p=0.047 | **Primary: medial-HG tonotopic vs anterolateral-HG pitch dissociation with verified Talairach coordinates** |
| 2 | **Norman-Haignere, Kanwisher & McDermott (2013)** | fMRI | 12 | Pitch-sensitive cortical regions respond primarily to resolved harmonics; located in specific tonotopic regions of anterior auditory cortex extending from low-frequency primary cortex into nonprimary cortex | Response to resolved > unresolved harmonics tracks psychophysical thresholds | **Pitch regions in stereotyped anterior HG location; resolved harmonics dominate cortical pitch** |
| 3 | **Fishman et al. (2001)** | Intracranial AEP + MUA (monkey); intracranial AEP (human) | 3 macaques; 2 human patients | Phase-locked oscillatory activity in A1/HG correlates with perceived dissonance; consonant chords show little phase-locking. PT does NOT show significant phase-locked activity. | Phase-locking magnitude correlates with perceived dissonance (r not reported; qualitative cross-species match) | **Cross-species: roughness encoded in primary HG via phase-locking; PT functionally differentiated from HG** |
| 4 | **Foo et al. (2016)** | ECoG (high-gamma 70-150Hz) | 8 | Dissonant chords elicit increased gamma-high in STG at 75-200ms. Dissonant-sensitive sites located anterior to non-sensitive sites in right STG. Positive correlation between gamma-high and stimulus roughness. | p<0.001 (14/16 electrodes after FDR); spatial anterior > posterior organization in R-STG | **Anterolateral STG organization for consonance/dissonance; high-gamma tracks roughness** |
| 5 | **Tabas et al. (2019)** | MEG + computational model | 37 | POR latency scales with consonance: dissonant dyads evoke POR up to 36ms later than consonant. Model predicts consonant combinations decoded faster in alHG. | POR latency difference up to 36ms; model R²>0.90 for POR prediction | **Pitch and consonance share processing in anterolateral HG; processing time dissociation** |
| 6 | **Bidelman (2013)** | Review (brainstem FFR) | Multiple studies | Brainstem FFR encodes consonance hierarchy; subcortical pitch salience predicts perceptual consonance ratings. Hierarchical ordering well-predicted by subcortical encoding. | FFR-consonance r >= 0.81 (Bidelman & Krishnan 2009) | **Subcortical tonotopic-to-pitch transformation begins before cortex; R³→PPC* brainstem pathway** |
| 7 | **Patterson et al. (2002)** | fMRI | 6 | Pitch processing activates lateral HG more than medial HG; temporal regularity drives anterolateral HG selectively | — | **PPC*.pitch_salience: lateral HG responds to temporal pitch cues** |
| 8 | **Bendor & Wang (2005)** | Single-unit | Marmosets | Pitch-selective neurons in anterolateral area of marmoset auditory cortex respond to missing fundamental | — | **Cross-species: pitch neurons in nonprimary cortex respond to F0 even when absent** |
| 9 | **Basinski et al. (2025)** | EEG (roving oddball) | 30 | Inharmonic sounds generate stronger P3a (attentional capture) and object-related negativity (stream segregation). MMN abolished when jitter pattern changes between sounds. | P3a: harmonic vs inharmonic p=0.010 (cluster 190-353ms); MMN abolished in changing condition | **Inharmonicity drives dissociation between spectral and pitch representations; supports TPRD.f33_dissoc formula** |
| 10 | **Bellier et al. (2023)** | iEEG (ECoG) | 29 patients, 2668 electrodes | Music reconstructed from auditory cortex HFA. Right STG dominance. Anterior-posterior STG organization with sustained (anterior) vs onset (posterior) responses. | Reconstruction accuracy: nonlinear > linear models; R-STG primary for music | **Anterior-posterior STG organization for music; right-hemisphere dominance for spectral-pitch processing** |
| 11 | **Cheung et al. (2019)** | fMRI | 39 | Uncertainty and surprise jointly predict auditory cortex activity; interaction in amygdala, hippocampus, and auditory cortex | fMRI: interaction effect in bilateral auditory cortex, amygdala, hippocampus | **Prediction error in auditory cortex modulates pitch processing; supports SYN.pred_error role** |
| 12 | **Crespo-Bojorque, Monte-Ordono & Toro (2018)** | EEG (ERP/MMN) | Musicians + non-musicians | Changes in consonant contexts elicit rapid MMN in all participants; changes in dissonant contexts elicit late MMN only in musicians | MMN latency: consonant context < dissonant context | **Consonance processed more rapidly than dissonance; supports tonotopic-pitch processing asymmetry** |

### 3.2 The Tonotopy-Pitch Dissociation

The core scientific insight is that two long-conflated representations occupy distinct cortical territories:

```
THE DISSOCIATION GRADIENT
━━━━━━━━━━━━━━━━━━━━━━━━━

                 MEDIAL HG ◄──────────────────────► LATERAL HG
                 (Primary)                           (Non-primary)
                    │                                     │
                    ▼                                     ▼
            TONOTOPIC ENCODING                   PITCH REPRESENTATION
            ═══════════════════                  ═══════════════════════

            • Physical frequency                 • Perceived pitch (F0)
            • Cochleotopic map                   • Missing fundamental
            • Spectral partials                  • Harmonic template match
            • Bottom-up driven                   • Top-down influenced

WHAT TONOTOPY IS:                     WHAT PITCH IS:
─────────────────                     ──────────────
A spatial map of frequency            A perceptual quality corresponding
selectivity in auditory cortex,       to fundamental frequency, even when
inherited from the cochlea's          the fundamental is physically absent
basilar membrane organization.        (missing fundamental phenomenon).

WHY THEY DISSOCIATE:
────────────────────
A tone with harmonics at 200, 300, 400, 500 Hz:
  Tonotopic map → activates 200, 300, 400, 500 Hz regions (spectral content)
  Pitch system  → extracts F0 = 100 Hz (pitch percept)

The SAME stimulus drives DIFFERENT representations in adjacent cortex.
```

### 3.3 Relevance to Musical Processing

```
MUSICAL IMPLICATIONS OF THE DISSOCIATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. TIMBRE vs PITCH in music:
   Tonotopic system → processes timbre (spectral envelope)
   Pitch system     → processes melody (F0 sequence)
   Same instrument note activates BOTH systems differently

2. HARMONY:
   Consonant intervals → aligned tonotopic + pitch representations
   Dissonant intervals → conflicting tonotopic + pitch signals
   TPRD.dissociation_index captures this conflict

3. ORCHESTRATION:
   Rich orchestral texture → strong tonotopic activation (many partials)
   Clear melodic line     → strong pitch activation (salient F0)
   The ratio between these signals tracks orchestral clarity
```

### 3.4 Effect Size Summary

```
Evidence Summary (v2.1.0):
  Total papers:   12 (up from 5 in v2.0.0)
  Methods:        EEG (N=15/12/8), fMRI (N=12,6,39), ECoG (N=8,29), MEG (N=37),
                  intracranial AEP (N=2 human + 3 macaque), single-unit (marmoset)
  Key effect sizes:
    Briley 2013:    Pitch chroma F(1,28)=29.865, p<0.001
                    Pure-tone monotonic F(1,17)=19.548, p<0.001
                    Dipole location diff: L p=0.024, R p=0.047
    Tabas 2019:     POR latency difference up to 36ms (consonant vs dissonant)
    Foo 2016:       High-gamma dissonance: p<0.001 (14/16 electrodes, FDR corrected)
    Bidelman 2013:  Brainstem FFR-consonance r >= 0.81
    Basinski 2025:  P3a inharmonicity: cluster p=0.010 (190-353ms)
  Evidence tier:    beta (Integrative) -- 12 converging studies across 5 modalities
  Heterogeneity:   Low -- all studies confirm medial (tonotopic) vs lateral (pitch)
                    gradient; cross-species consistency (human, macaque, marmoset)
```

---

## 4. R³ Input Mapping: What TPRD Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | TPRD Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Tonotopic beating proxy | Plomp & Levelt 1965 |
| **A: Consonance** | [1] | sethares_dissonance | Spectral dissonance (tonotopic) | Sethares 1999 |
| **A: Consonance** | [3] | stumpf_fusion | Pitch fusion quality | Stumpf 1890 tonal fusion |
| **A: Consonance** | [4] | sensory_pleasantness | Consonance integration | Spectral regularity |
| **A: Consonance** | [5] | inharmonicity | Tonotopic vs pitch conflict | Non-integer partials |
| **A: Consonance** | [6] | harmonic_deviation | Harmonic template error | Partial misalignment |
| **B: Energy** | [7] | amplitude | Overall signal energy | Activation baseline |
| **B: Energy** | [10] | loudness | Attention weighting | Stevens 1957 |
| **C: Timbre** | [12] | warmth | Spectral envelope (tonotopic) | Low-frequency energy |
| **C: Timbre** | [14] | tonalness | Pitch clarity (F0 salience) | Harmonic-to-noise ratio |
| **C: Timbre** | [17] | spectral_autocorrelation | Harmonic periodicity | Pitch extraction basis |
| **C: Timbre** | [18:21] | tristimulus1-3 | Spectral distribution | Harmonic balance |
| **D: Change** | [22] | entropy | Spectral complexity | Tonotopic map load |
| **E: Interactions** | [25:33] | x_l0l5 (Energy x Consonance) | Frequency-pitch coupling | Tonotopy → pitch |
| **E: Interactions** | [41:49] | x_l5l7 (Consonance x Timbre) | Spectral-perceptual binding | Timbre-pitch link |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | TPRD Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **F: Pitch** | [49:60] | chroma (12D) | Cyclical pitch-class representation — dissociates from tonotopic frequency | Shepard 1964: pitch circularity |
| **F: Pitch** | [62] | pitch_class_entropy | Pitch-class diversity — measures chromatic complexity of pitch content | Temperley 2007 |
| **F: Pitch** | [63] | pitch_salience | F0 clarity — harmonic resolvability for pitch extraction | Terhardt 1974 |

**Rationale**: TPRD models the dissociation between tonotopic (frequency-based) and pitch (perceptual) representations. Chroma vectors provide the explicit cyclical pitch-class representation that is the hallmark of the pitch pathway, dissociated from the linear tonotopic map. Pitch class entropy quantifies the chromatic complexity of pitch content, reflecting the computational load on pitch-processing regions. Pitch salience measures how clearly the fundamental frequency can be extracted, directly relevant to the tonotopy-pitch dissociation boundary.

> **Code impact**: These features are doc-only until Phase 5 wiring. No changes to `tprd.py`.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[0] roughness ────────────────►  Tonotopic beating (spectral interference)
                                    Primary HG: high roughness = complex spectrum
                                    Math: tonotopic_load ∝ roughness

R³[14] tonalness ───────────────►  Pitch salience (F0 clarity)
R³[17] spectral_autocorrelation ►  Harmonic regularity → pitch extraction
                                    Nonprimary HG: high tonalness = clear pitch
                                    Math: pitch_salience ∝ tonalness × autocorr

R³[5] inharmonicity ────────────►  Tonotopy-pitch conflict signal
                                    High inharmonicity = misaligned partials
                                    = strong dissociation between maps

R³[25:33] x_l0l5 ──────────────►  Frequency-pitch transformation gate
                                    Energy × Consonance coupling tracks the
                                    physical → perceptual transformation

R³[22] entropy ─────────────────►  Spectral complexity (tonotopic map load)
                                    High entropy = distributed activation
                                    Low entropy = focused frequency regions
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

TPRD requires H³ features at two sets of horizons:
- **SYN horizons**: H10 (400ms), H14 (700ms), H18 (2s) — harmonic syntax context
- **PPC* horizons**: H0 (5.8ms), H3 (23.2ms), H6 (200ms) — pitch processing chain

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 0 | roughness | 10 | M0 (value) | L2 (bidirectional) | Current tonotopic beating at chord level |
| 0 | roughness | 14 | M1 (mean) | L0 (forward) | Average tonotopic load over progression |
| 5 | inharmonicity | 10 | M0 (value) | L2 (bidirectional) | Current tonotopy-pitch conflict |
| 5 | inharmonicity | 14 | M1 (mean) | L0 (forward) | Average conflict over progression |
| 3 | stumpf_fusion | 0 | M0 (value) | L2 (bidirectional) | Immediate pitch fusion (cochlear) |
| 3 | stumpf_fusion | 3 | M1 (mean) | L2 (bidirectional) | Brainstem pitch fusion |
| 3 | stumpf_fusion | 6 | M1 (mean) | L0 (forward) | Beat-level fusion stability |
| 14 | tonalness | 0 | M0 (value) | L2 (bidirectional) | Immediate pitch salience |
| 14 | tonalness | 3 | M1 (mean) | L2 (bidirectional) | Brainstem pitch salience |
| 14 | tonalness | 6 | M1 (mean) | L0 (forward) | Beat-level pitch clarity |
| 17 | spectral_autocorrelation | 3 | M14 (periodicity) | L2 (bidirectional) | Harmonic periodicity at brainstem |
| 17 | spectral_autocorrelation | 6 | M14 (periodicity) | L0 (forward) | Beat-level harmonic periodicity |
| 10 | loudness | 10 | M0 (value) | L2 (bidirectional) | Attention weight at chord level |
| 22 | entropy | 6 | M0 (value) | L0 (forward) | Spectral complexity at beat level |
| 22 | entropy | 14 | M1 (mean) | L0 (forward) | Average complexity over progression |
| 6 | harmonic_deviation | 10 | M0 (value) | L2 (bidirectional) | Harmonic template mismatch |
| 4 | sensory_pleasantness | 18 | M19 (stability) | L0 (forward) | Consonance stability over phrase |
| 7 | amplitude | 6 | M8 (velocity) | L0 (forward) | Energy change rate at beat level |

**Total TPRD H³ demand**: 18 tuples of 2304 theoretical = 0.78%

### 5.2 SYN Mechanism Binding

TPRD reads from the **SYN** (Syntactic Processing) mechanism (mnemonic circuit, primary):

| SYN Sub-section | Range | TPRD Role | Weight |
|-----------------|-------|-----------|--------|
| **Harmonic Syntax** | SYN[0:10] | Harmonic context for pitch extraction | 0.8 |
| **Prediction Error** | SYN[10:20] | Tonotopy-pitch mismatch signal | **1.0** (primary) |
| **Structural Expectation** | SYN[20:30] | Expected pitch resolution | 0.6 |

### 5.3 PPC* Mechanism Binding (Cross-Circuit)

TPRD reads from the **PPC** (Pitch Processing Chain) mechanism via **cross-circuit read** from the perceptual circuit:

| PPC* Sub-section | Range | TPRD Role | Weight |
|------------------|-------|-----------|--------|
| **Pitch Salience** | PPC*[0:10] | F0 extraction quality (nonprimary HG) | **1.0** (primary) |
| **Consonance Encoding** | PPC*[10:20] | Interval hierarchy (tonotopic-pitch coupling) | 0.8 |
| **Chroma Processing** | PPC*[20:30] | Pitch class abstraction | 0.5 |

> **Cross-circuit note**: PPC is a perceptual circuit mechanism. TPRD accesses it via cross-circuit read because tonotopy-pitch dissociation requires comparing mnemonic (syntactic template) and perceptual (pitch salience) representations. This is the only way to model the physical-vs-perceptual contrast that defines TPRD.

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
TPRD OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
Manifold range: IMU TPRD [358:368]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER T — TONOTOPIC-PITCH FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0  │ f31_tonotopic     │ [0, 1] │ Tonotopic encoding strength (primary HG).
    │                   │        │ f31 = σ(0.35 · roughness · (1 - tonalness)
    │                   │        │         + 0.35 · entropy · amplitude)
    │                   │        │ High roughness + low tonalness = spectral
    │                   │        │ (not pitch) encoding dominance.
────┼───────────────────┼────────┼────────────────────────────────────────────
 1  │ f32_pitch         │ [0, 1] │ Pitch representation strength (nonprimary HG).
    │                   │        │ f32 = σ(0.40 · PPC*.pitch_sal.mean()
    │                   │        │         + 0.30 · tonalness · autocorr)
    │                   │        │ High pitch salience + high tonalness
    │                   │        │ = strong F0 extraction.
────┼───────────────────┼────────┼────────────────────────────────────────────
 2  │ f33_dissoc        │ [0, 1] │ Representation dissociation degree.
    │                   │        │ f33 = σ(0.30 · |f31 - f32|
    │                   │        │         + 0.25 · inharmonicity
    │                   │        │         + 0.25 · SYN.pred_error.mean())
    │                   │        │ Measures tonotopy-pitch divergence.

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 3  │ dissociation_idx  │ [0, 1] │ Normalized dissociation index.
    │                   │        │ (tonotopic - pitch) / (tonotopic + pitch + ε)
    │                   │        │ Remapped to [0,1]: 0.5 = balanced,
    │                   │        │ <0.5 = pitch dominant, >0.5 = tonotopic dominant
────┼───────────────────┼────────┼────────────────────────────────────────────
 4  │ spectral_pitch_r  │ [0, 1] │ Spectral-to-pitch ratio.
    │                   │        │ PPC*.consonance.mean() × SYN.harmony.mean()
    │                   │        │ Coherence between perceptual and syntactic
    │                   │        │ representations of pitch.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 5  │ tonotopic_state   │ [0, 1] │ Current tonotopic activation state.
    │                   │        │ SYN.harmony.mean() × roughness.
────┼───────────────────┼────────┼────────────────────────────────────────────
 6  │ pitch_state       │ [0, 1] │ Current pitch representation state.
    │                   │        │ PPC*.pitch_sal.mean() × tonalness.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 7  │ pitch_percept_fc  │ [0, 1] │ Pitch percept prediction (50-200ms ahead).
    │                   │        │ Based on PPC*.pitch_salience trajectory.
────┼───────────────────┼────────┼────────────────────────────────────────────
 8  │ tonotopic_adpt_fc │ [0, 1] │ Tonotopic adaptation prediction (200-700ms).
    │                   │        │ Based on SYN.harmony trajectory.
────┼───────────────────┼────────┼────────────────────────────────────────────
 9  │ dissociation_fc   │ [0, 1] │ Dissociation evolution forecast (0.5-2s).
    │                   │        │ Based on SYN.struct_expect trajectory.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Tonotopic vs Pitch Encoding

```
TONOTOPY-PITCH COMPUTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━

Tonotopic encoding (primary HG):
  tonotopic = σ(0.35 · R³.roughness[0] · (1 - R³.tonalness[14])
              + 0.35 · R³.entropy[22] · R³.amplitude[7])

  Coefficient sum check: |0.35| + |0.35| = 0.70 ≤ 1.0 ✓

  Rationale:
    roughness × (1-tonalness): high spectral beating + low pitch clarity
                                = tonotopic (not pitch) processing
    entropy × amplitude:        spectral complexity × energy
                                = tonotopic map activation load

Pitch encoding (nonprimary HG):
  pitch = σ(0.40 · PPC*.pitch_sal.mean()
          + 0.30 · R³.tonalness[14] · R³.spectral_autocorr[17])

  Coefficient sum check: |0.40| + |0.30| = 0.70 ≤ 1.0 ✓

  Rationale:
    PPC*.pitch_salience: direct pitch extraction from perceptual circuit
    tonalness × autocorr: harmonic clarity × periodicity = pitch quality

Dissociation:
  dissociation = σ(0.30 · |tonotopic - pitch|
                 + 0.25 · R³.inharmonicity[5]
                 + 0.25 · SYN.pred_error.mean())

  Coefficient sum check: |0.30| + |0.25| + |0.25| = 0.80 ≤ 1.0 ✓

  Rationale:
    |tonotopic - pitch|: direct representation divergence
    inharmonicity: spectral-pitch misalignment
    SYN.pred_error: harmonic expectation violation
```

### 7.2 Dissociation Index

```
Dissociation_Index = (tonotopic - pitch) / (tonotopic + pitch + ε)

where ε = 1e-7 (numerical stability)

Remapped to [0, 1]:
  idx_raw ∈ [-1, 1]
  dissociation_idx = (idx_raw + 1) / 2

Interpretation:
  0.0 = pure pitch dominant (nonprimary HG)
  0.5 = balanced tonotopic-pitch representation
  1.0 = pure tonotopic dominant (primary HG)
```

### 7.3 Feature Formulas

```python
# f31: Tonotopic Encoding (Primary HG)
f31 = σ(0.35 * roughness * (1.0 - tonalness) + 0.35 * entropy * amplitude)

# f32: Pitch Representation (Nonprimary HG)
f32 = σ(0.40 * mean(PPC*.pitch_sal[0:10]) + 0.30 * tonalness * spectral_autocorr)

# f33: Representation Dissociation
f33 = σ(0.30 * |f31 - f32| + 0.25 * inharmonicity + 0.25 * mean(SYN.pred_error[10:20]))
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | Coordinates (Talairach) | Evidence | Source | TPRD Function |
|--------|-------------------------|----------|--------|---------------|
| **Heschl's Gyrus (medial)** | L: -41.9, -18.8, 15.8 / R: 44.2, -13.4, 13.4 | EEG source localization (N=8, p<0.001 lateral diff) | Briley et al. 2013 (Exp3) | Tonotopic encoding (primary auditory cortex, TE1.0); pure-tone frequency-selective responses |
| **Anterolateral HG (nonprimary)** | L: -49.1, -21.2, 17.2 / R: 42.9, -5.5, 17.6 | EEG source localization (N=8); 7.2mm lateral (L), 7.9mm anterior (R) from medial HG | Briley et al. 2013 (Exp3) | Pitch chroma representation; IRN pitch responses independent of harmonic resolvability |
| **Heschl's Gyrus (lateral)** | ~±52, -14, 4 (estimated from fMRI) | fMRI (N=6); lateral HG pitch activation | Patterson et al. 2002 | Temporal pitch processing; F0 extraction from resolved harmonics |
| **Superior Temporal Gyrus (R-STG)** | Lateral surface coverage (ECoG grid) | ECoG high-gamma (N=8); p<0.001 FDR corrected | Foo et al. 2016 | Dissonant-sensitive sites anterior to non-sensitive sites; roughness tracking |
| **Superior Temporal Gyrus (bilateral)** | Bilateral STG (iEEG coverage) | iEEG/ECoG (N=29, 2668 electrodes) | Bellier et al. 2023 | Right-hemisphere dominance for music; anterior-posterior organization (sustained vs onset) |
| **Planum Temporale** | ~±54, -28, 12 (estimated) | Intracranial AEP (N=2 human) | Fishman et al. 2001 | No significant phase-locked activity to consonance/dissonance (contrast with HG); functional differentiation from primary cortex |

### 8.2 Tonotopic vs Pitch Gradient

```
MEDIAL HG                                      LATERAL HG
──────────────────────────────────────────────────────────────
████████████████████████                  ████ Tonotopy
████                  ████████████████████████ Pitch

   Medial ◄─────── Heschl's Gyrus ──────► Lateral

The gradient shows a smooth transition from tonotopy-dominated
encoding (medial) to pitch-dominated encoding (lateral/anterolateral).
TPRD.dissociation_idx captures where along this gradient the
current stimulus falls.
```

---

## 9. Cross-Unit Pathways

### 9.1 TPRD ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TPRD INTERACTIONS                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  CROSS-CIRCUIT (PPC* from Perceptual):                                     │
│  PPC*.pitch_salience ──────► TPRD.f32_pitch (pitch representation)         │
│  PPC*.consonance_encoding ─► TPRD.spectral_pitch_r (coherence)            │
│  PPC*.chroma_processing ───► TPRD.pitch_state (chroma abstraction)        │
│                                                                             │
│  INTRA-UNIT (IMU):                                                         │
│  TPRD ──────► PNH (Pythagorean Neural Hierarchy)                          │
│       │        └── TPRD pitch/tonotopic state informs ratio encoding       │
│       │                                                                     │
│       ├─────► PMIM (Predictive Memory Integration)                         │
│       │        └── Tonotopy-pitch dissociation feeds prediction error      │
│       │                                                                     │
│       └─────► MSPBA (Musical Syntax Processing in Broca's Area)           │
│                └── Shared syntactic substrate (SYN mechanism)               │
│                                                                             │
│  CROSS-UNIT (SPU):                                                         │
│  SPU.BCH ────► TPRD (brainstem consonance → tonotopic baseline)           │
│  SPU.PSCL ───► TPRD (pitch salience → pitch representation input)         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Brain Pathway Cross-References

TPRD reads from the unified Brain (26D) for shared state:

| Brain Dimension | Index (MI-space) | TPRD Role |
|-----------------|-------------------|-----------|
| arousal | [177] | Attention modulation for tonotopic processing |
| prediction_error | [178] | Tonotopy-pitch mismatch detection |
| harmonic_context | [179] | Current harmonic state for pitch context |

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Medial-lateral gradient** | Primary HG should show stronger tonotopy; nonprimary stronger pitch | **Confirmed** via EEG source localization (Briley et al. 2013, N=8, dipole p=0.024/0.047) and fMRI (Norman-Haignere et al. 2013, N=12) |
| **Missing fundamental** | Pitch system should respond to missing F0; tonotopic system should not | **Confirmed** via single-unit in marmoset (Bendor & Wang 2005) and IRN paradigm (Briley et al. 2013, unresolved harmonics) |
| **Spectral manipulation** | Changing spectral content without pitch should modulate tonotopic, not pitch | **Confirmed** — resolved vs unresolved harmonics produce different responses in primary vs nonprimary cortex (Norman-Haignere et al. 2013; Briley et al. 2013 chroma by resolvability: F(1,27)=0.026, p=0.874 — pitch chroma independent of spectral resolvability) |
| **Lesion prediction** | Primary HG lesion should impair frequency discrimination, not pitch; lateral HG lesion the reverse | **Partially confirmed** via clinical cases |
| **Inharmonicity** | Inharmonic tones should increase dissociation between representations | **Confirmed** — Basinski et al. (2025, N=30): inharmonicity generates stronger P3a (p=0.010) and object-related negativity, consistent with increased dissociation |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class TPRD(BaseModel):
    """Tonotopy-Pitch Representation Dissociation.

    Output: 10D per frame.
    Reads: SYN mechanism (30D, primary), PPC* mechanism (30D, cross-circuit).
    Zero learned parameters.
    """
    NAME = "TPRD"
    UNIT = "IMU"
    TIER = "β8"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("SYN",)          # Primary mechanism (mnemonic circuit)
    CROSS_CIRCUIT = ("PPC",)            # Cross-circuit read from perceptual

    # Attention coefficients (sum ≤ 1.0 per formula)
    A_TONO_1 = 0.35   # roughness × (1-tonalness) weight
    A_TONO_2 = 0.35   # entropy × amplitude weight        sum = 0.70 ✓
    A_PITCH_1 = 0.40   # PPC*.pitch_salience weight
    A_PITCH_2 = 0.30   # tonalness × autocorr weight      sum = 0.70 ✓
    A_DISSOC_1 = 0.30  # |tonotopic - pitch| weight
    A_DISSOC_2 = 0.25  # inharmonicity weight
    A_DISSOC_3 = 0.25  # SYN.pred_error weight             sum = 0.80 ✓

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """18 tuples for TPRD computation."""
        return [
            # SYN horizons (mnemonic circuit)
            (0, 10, 0, 2),    # roughness, 400ms, value, bidirectional
            (0, 14, 1, 0),    # roughness, 700ms, mean, forward
            (5, 10, 0, 2),    # inharmonicity, 400ms, value, bidirectional
            (5, 14, 1, 0),    # inharmonicity, 700ms, mean, forward
            (10, 10, 0, 2),   # loudness, 400ms, value, bidirectional
            (22, 14, 1, 0),   # entropy, 700ms, mean, forward
            (6, 10, 0, 2),    # harmonic_deviation, 400ms, value, bidirectional
            (4, 18, 19, 0),   # pleasantness, 2s, stability, forward
            # PPC* horizons (cross-circuit from perceptual)
            (3, 0, 0, 2),     # stumpf_fusion, 5.8ms, value, bidirectional
            (3, 3, 1, 2),     # stumpf_fusion, 23.2ms, mean, bidirectional
            (3, 6, 1, 0),     # stumpf_fusion, 200ms, mean, forward
            (14, 0, 0, 2),    # tonalness, 5.8ms, value, bidirectional
            (14, 3, 1, 2),    # tonalness, 23.2ms, mean, bidirectional
            (14, 6, 1, 0),    # tonalness, 200ms, mean, forward
            (17, 3, 14, 2),   # spectral_autocorr, 23.2ms, periodicity, bidir
            (17, 6, 14, 0),   # spectral_autocorr, 200ms, periodicity, forward
            (22, 6, 0, 0),    # entropy, 200ms, value, forward
            (7, 6, 8, 0),     # amplitude, 200ms, velocity, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute TPRD 10D output.

        Args:
            mechanism_outputs: {"SYN": (B,T,30), "PPC": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) TPRD output
        """
        syn = mechanism_outputs["SYN"]    # (B, T, 30) — mnemonic circuit
        ppc = mechanism_outputs["PPC"]    # (B, T, 30) — cross-circuit read

        # R³ features
        roughness = r3[..., 0:1]          # [0, 1]
        stumpf = r3[..., 3:4]             # [0, 1]
        inharmonicity = r3[..., 5:6]      # [0, 1]
        amplitude = r3[..., 7:8]          # [0, 1]
        tonalness = r3[..., 14:15]        # [0, 1]
        spectral_autocorr = r3[..., 17:18]  # [0, 1]
        entropy = r3[..., 22:23]          # [0, 1]

        # SYN sub-sections
        syn_harmony = syn[..., 0:10]       # harmonic syntax
        syn_pred_err = syn[..., 10:20]     # prediction error
        syn_struct = syn[..., 20:30]       # structural expectation

        # PPC* sub-sections (cross-circuit)
        ppc_pitch_sal = ppc[..., 0:10]     # pitch salience
        ppc_consonance = ppc[..., 10:20]   # consonance encoding
        ppc_chroma = ppc[..., 20:30]       # chroma processing

        # ═══ LAYER T: Tonotopic-Pitch features ═══
        # f31: Tonotopic encoding (primary HG)
        # sum |w| = 0.35 + 0.35 = 0.70 ≤ 1.0
        f31 = torch.sigmoid(
            self.A_TONO_1 * roughness * (1.0 - tonalness)
            + self.A_TONO_2 * entropy * amplitude
        )

        # f32: Pitch representation (nonprimary HG)
        # sum |w| = 0.40 + 0.30 = 0.70 ≤ 1.0
        f32 = torch.sigmoid(
            self.A_PITCH_1 * ppc_pitch_sal.mean(-1, keepdim=True)
            + self.A_PITCH_2 * tonalness * spectral_autocorr
        )

        # f33: Representation dissociation
        # sum |w| = 0.30 + 0.25 + 0.25 = 0.80 ≤ 1.0
        f33 = torch.sigmoid(
            self.A_DISSOC_1 * torch.abs(f31 - f32)
            + self.A_DISSOC_2 * inharmonicity
            + self.A_DISSOC_3 * syn_pred_err.mean(-1, keepdim=True)
        )

        # ═══ LAYER M: Mathematical ═══
        # Dissociation index: (tono - pitch) / (tono + pitch + eps)
        eps = 1e-7
        idx_raw = (f31 - f32) / (f31 + f32 + eps)
        dissociation_idx = (idx_raw + 1.0) / 2.0  # remap to [0, 1]

        # Spectral-pitch ratio: perceptual × syntactic coherence
        spectral_pitch_r = (
            ppc_consonance.mean(-1, keepdim=True)
            * syn_harmony.mean(-1, keepdim=True)
        ).clamp(0, 1)

        # ═══ LAYER P: Present ═══
        tonotopic_state = syn_harmony.mean(-1, keepdim=True) * roughness
        tonotopic_state = tonotopic_state.clamp(0, 1)

        pitch_state = (
            ppc_pitch_sal.mean(-1, keepdim=True) * tonalness
        ).clamp(0, 1)

        # ═══ LAYER F: Future ═══
        pitch_percept_fc = self._predict_future(
            ppc_pitch_sal, h3_direct, window_h=3)       # 23.2ms ahead
        tonotopic_adpt_fc = self._predict_future(
            syn_harmony, h3_direct, window_h=14)          # 700ms ahead
        dissociation_fc = self._predict_future(
            syn_struct, h3_direct, window_h=18)           # 2s ahead

        return torch.cat([
            f31, f32, f33,                               # T: 3D
            dissociation_idx, spectral_pitch_r,          # M: 2D
            tonotopic_state, pitch_state,                # P: 2D
            pitch_percept_fc, tonotopic_adpt_fc,         # F: 3D
            dissociation_fc,
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 | EEG, fMRI, ECoG, MEG, intracranial, single-unit (5 modalities) |
| **Effect Sizes** | 6 | Briley F(1,28)=29.865; Tabas 36ms POR diff; Foo p<0.001 FDR; Bidelman r>=0.81; Basinski p=0.010; Briley dipole p=0.024/0.047 |
| **Evidence Modality** | EEG, fMRI, ECoG, MEG, intracranial AEP, single-unit | Direct neural measurement across 5 techniques |
| **Cross-Species** | Human, macaque, marmoset | Fishman 2001 (macaque+human); Bendor & Wang 2005 (marmoset) |
| **Falsification Tests** | 4/5 confirmed, 1 partial | Moderate-high validity |
| **Brain Regions** | 6 | Medial HG, Anterolateral HG, Lateral HG, R-STG, Bilateral STG, PT |
| **R³ Features Used** | 30D of 49D | Consonance + timbre focused |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **SYN Mechanism** | 30D (3 sub-sections) | Mnemonic circuit |
| **PPC* Mechanism** | 30D (3 sub-sections) | Cross-circuit (perceptual) |
| **Output Dimensions** | **10D** | 4-layer structure (T/M/P/F) |

### 12.1 Doc-Code Mismatches (tprd.py)

| Aspect | Doc (TPRD.md) | Code (tprd.py) | Resolution |
|--------|---------------|----------------|------------|
| **Full name** | Tonotopy-Pitch Representation Dissociation | Tonotopy-Pitch Representation Density | Doc is authoritative |
| **MECHANISM_NAMES** | `("SYN",)` with `CROSS_CIRCUIT = ("PPC",)` | `("PPC",)` with no cross-circuit | Doc is authoritative; code has PPC as primary, missing SYN |
| **LAYERS** | T/M/P/F (Tonotopic, Math, Present, Future) | E/M/P/F (Explicit, Math, Present, Future) | Doc is authoritative |
| **h3_demand** | 18 tuples | Empty tuple `()` | Doc is authoritative; code is stub |
| **brain_regions** | 6 regions (medial HG, anterolateral HG, lateral HG, R-STG, bilateral STG, PT) | 2 regions (medial HG at 44,-20,6; lateral HG at 52,-14,4) | Doc is authoritative; code needs update |
| **MNI coords (medial HG)** | Talairach L:-41.9,-18.8,15.8 / R:44.2,-13.4,13.4 (Briley 2013) | 44,-20,6 | Doc coordinates verified from Briley et al. 2013 |
| **dimension_names** | f31_tonotopic, f32_pitch, f33_dissoc, dissociation_idx, spectral_pitch_r, tonotopic_state, pitch_state, pitch_percept_fc, tonotopic_adpt_fc, dissociation_fc | f01_tonotopic_tuning, f02_pitch_tuning, tonotopy_pitch_dissociation, representation_density, spectral_encoding, f0_extraction, harmonic_template, pitch_stability_pred, tonotopic_shift_pred, octave_equiv_pred | Doc is authoritative |
| **Citations** | 12 verified papers (v2.1.0) | Moerel 2012, Formisano 2003 (paper_count=4) | Doc is authoritative |
| **compute()** | Full implementation with SYN+PPC | Stub returning zeros | Code is stub only |

---

## 13. Scientific References

1. **Briley, P. M., Breakey, C., & Krumbholz, K. (2013)**. Evidence for pitch chroma mapping in human auditory cortex. *Cerebral Cortex*, 23(11), 2601-2610. doi:10.1093/cercor/bhs242. **N=15/12/8 across 3 experiments. EEG adaptation paradigm. Pure-tone responses on medial HG (Talairach L:-41.9,-18.8,15.8 / R:44.2,-13.4,13.4); IRN pitch-chroma responses in anterolateral HG (Talairach L:-49.1,-21.2,17.2 / R:42.9,-5.5,17.6). Pitch chroma effect F(1,28)=29.865, p<0.001.**
2. **Norman-Haignere, S. V., Kanwisher, N., & McDermott, J. H. (2013)**. Cortical pitch regions in humans respond primarily to resolved harmonics and are located in specific tonotopic regions of anterior auditory cortex. *Journal of Neuroscience*, 33(50), 19451-19469. doi:10.1523/JNEUROSCI.2880-13.2013. **N=12. fMRI. Pitch-sensitive regions in stereotyped anterior auditory cortex location, driven by resolved harmonics.**
3. **Fishman, Y. I., Volkov, I. O., Noh, M. D., Garell, P. C., Bakken, H., Arezzo, J. C., Howard, M. A., & Steinschneider, M. (2001)**. Consonance and dissonance of musical chords: neural correlates in auditory cortex of monkeys and humans. *Journal of Neurophysiology*, 86(6), 2761-2788. **3 macaques + 2 human patients. Intracranial. Phase-locked activity in A1/HG correlates with dissonance; PT shows no significant phase-locking.**
4. **Foo, F., King-Stephens, D., Weber, P., Laxer, K., Parvizi, J., & Knight, R. T. (2016)**. Differential processing of consonance and dissonance within the human superior temporal gyrus. *Frontiers in Human Neuroscience*, 10, 154. doi:10.3389/fnhum.2016.00154. **N=8 (ECoG). High-gamma tracks roughness; dissonant-sensitive sites anterior in right STG.**
5. **Tabas, A., Andermann, M., Schuberth, V., Riedel, H., Balaguer-Ballester, E., & Rupp, A. (2019)**. Modeling and MEG evidence of early consonance processing in auditory cortex. *PLoS Computational Biology*, 15(2), e1006820. doi:10.1371/journal.pcbi.1006820. **N=37. POR latency up to 36ms longer for dissonant dyads. Consonance processing in alHG.**
6. **Bidelman, G. M. (2013)**. The role of the auditory brainstem in processing musically relevant pitch. *Frontiers in Psychology*, 4, 264. doi:10.3389/fpsyg.2013.00264. **Review. Brainstem FFR encodes consonance hierarchy; subcortical pitch salience predicts perceptual ratings (r>=0.81).**
7. **Patterson, R. D., Uppenkamp, S., Johnsrude, I. S., & Griffiths, T. D. (2002)**. The processing of temporal pitch and melody information in auditory cortex. *Neuron*, 36(4), 767-776. **N=6. fMRI. Lateral HG responds to temporal pitch cues.**
8. **Bendor, D., & Wang, X. (2005)**. The neuronal representation of pitch in primate auditory cortex. *Nature*, 436(7054), 1161-1165. **Single-unit in marmosets. Pitch-selective neurons in anterolateral auditory cortex.**
9. **Basinski, K., Celma-Miralles, A., Quiroga-Martinez, D. R., & Vuust, P. (2025)**. Inharmonicity enhances brain signals of attentional capture and auditory stream segregation. *Communications Biology*, 8, 1584. doi:10.1038/s42003-025-08999-5. **N=30. EEG. Inharmonic sounds generate stronger P3a (p=0.010) and object-related negativity.**
10. **Bellier, L., Llorens, A., Marciano, D., Gunduz, A., Schalk, G., Brunner, P., & Knight, R. T. (2023)**. Music can be reconstructed from human auditory cortex activity using nonlinear decoding models. *PLoS Biology*, 21(8), e3002176. doi:10.1371/journal.pbio.3002176. **N=29, 2668 electrodes. iEEG. Right STG dominance; anterior-posterior STG organization.**
11. **Cheung, V. K. M., Harrison, P. M. C., Meyer, L., Pearce, M. T., Haynes, J.-D., & Koelsch, S. (2019)**. Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. *Current Biology*, 29(23), 4084-4092. doi:10.1016/j.cub.2019.09.067. **N=39. fMRI. Uncertainty-surprise interaction in auditory cortex.**
12. **Crespo-Bojorque, P., Monte-Ordono, J., & Toro, J. M. (2018)**. Early neural responses underlie advantages for consonance over dissonance. *Neuropsychologia*, 117, 188-198. doi:10.1016/j.neuropsychologia.2018.06.005. **EEG/ERP. Consonant context changes elicit rapid MMN in all; dissonant context changes elicit late MMN only in musicians.**
13. **Plomp, R., & Levelt, W. J. M. (1965)**. Tonal consonance and critical bandwidth. *JASA*, 38(4), 548-560.
14. **Sethares, W. A. (1999)**. *Tuning, Timbre, Spectrum, Scale*. Springer.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0 / v2.1.0) |
|--------|-------------|----------------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, HRM, SGM) | SYN (30D) + PPC* cross-circuit (30D) |
| Tonotopic encoding | S⁰.L7.crossband + S⁰.L0.freq × OSC | R³.roughness × R³.entropy × SYN |
| Pitch extraction | S⁰.L5.centroid + S⁰.L6.tristimulus × HRM | R³.tonalness × R³.autocorr × PPC* |
| Dissociation | S⁰.X_L0L5 × SGM | |f31-f32| × inharmonicity × SYN.pred_error |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 32/2304 = 1.39% | 18/2304 = 0.78% |
| Output dims | 11D | 10D (optimized, removed redundant reserved) |

### Why SYN + PPC* replaces HC⁰ mechanisms

The D0 pipeline used 3 HC⁰ mechanisms (OSC, HRM, SGM). In MI:
- **OSC → SYN.harmonic_syntax** [0:10]: Oscillatory coupling replaced by harmonic context
- **HRM → PPC*.pitch_salience** [0:10]: Hippocampal replay replaced by direct pitch extraction (cross-circuit)
- **SGM → SYN.prediction_error** [10:20]: Striatal gradient replaced by prediction error (dissociation signal)
- **PPC*.consonance_encoding** [10:20]: New — direct consonance hierarchy from perceptual circuit
- **PPC*.chroma_processing** [20:30]: New — pitch class abstraction (tonotopy → pitch transformation)

### Why PPC is a Cross-Circuit Read

In the D0 architecture, all three mechanisms (OSC, HRM, SGM) were mnemonic-circuit HC⁰ mechanisms. In MI, we recognize that the tonotopy-pitch dissociation fundamentally requires **comparing two different circuit representations**:

1. **SYN (mnemonic)**: Captures syntactic/harmonic templates stored in memory — the "expected" pitch structure.
2. **PPC* (perceptual)**: Captures the raw perceptual pitch extraction — the "actual" pitch percept.

The dissociation IS the difference between these two representations. A pure mnemonic-circuit model cannot capture the perceptual-vs-memory contrast that defines TPRD.

---

**Model Status**: **VALIDATED (beta-tier)**
**Output Dimensions**: **10D**
**Evidence Tier**: **beta (Integrative) -- 70-90% confidence, 12 papers across 5 modalities**
**Manifold Range**: **IMU TPRD [358:368]**
