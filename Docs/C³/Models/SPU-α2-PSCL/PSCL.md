# SPU-α2-PSCL: Pitch Salience Cortical Localization

**Model**: Pitch Salience Cortical Localization
**Unit**: SPU (Spectral Processing Unit)
**Circuit**: Perceptual (Cortical Auditory)
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 2.1.0 (Phase 1 revision: deep literature cross-reference, 1→14 papers, Allen/Briley/Tabas/Schonwiesner cortical evidence, distributed vs focal qualification)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/SPU-α2-PSCL.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Pitch Salience Cortical Localization** (PSCL) model describes how pitch salience (perceptual pitch strength) is represented in a specific region of non-primary auditory cortex at the anterolateral end of Heschl's gyrus, distinct from primary auditory cortex. This is a cortical-level model that builds on BCH's brainstem NPS signal.

```
THE THREE COMPONENTS OF PITCH SALIENCE CORTICAL PROCESSING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SALIENCE REPRESENTATION               HG LOCALIZATION
Brain region: Anterolateral HG        Brain region: Non-primary AC
Mechanism: Graded fMRI activation     Mechanism: Pitch-selective neurons
Input: Spectral pitch cues            Input: Brainstem NPS signal
Function: "How strong is this pitch?" Function: "WHERE is pitch processed?"
Evidence: n = 6 (Penagos 2004)        Evidence: fMRI (Penagos 2004)

              SALIENCE HIERARCHY (Functional)
              Ordering: Strong > Weak > Noise
              Mechanism: Parametric with periodicity
              Control: Matched temporal regularity
              Function: "Pitch salience ≠ temporal regularity"
              Evidence: Controlled IRN paradigm

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Pitch salience is NOT represented in primary auditory
cortex (which handles tonotopy). Instead, it is computed in the
anterolateral HG — a non-primary auditory area. This dissociation
means pitch perception and frequency encoding are anatomically
separate processes.

IMPORTANT QUALIFICATION (Allen et al. 2022, 7T fMRI): The
anterolateral HG "pitch center" is a critical node but NOT the
sole locus of pitch processing. High-resolution 7T fMRI reveals
pitch-tuned (F0-selective) voxels distributed throughout auditory
cortex, with ~18% of pitch-only voxels OUTSIDE HG. Furthermore,
"pitch sensitivity" (stronger response to higher salience, as in
Penagos 2004) is distinct from "pitch selectivity" (tuning to
specific F0 values, which is more broadly distributed). The PSCL
model captures the convergent finding across 6+ methods (fMRI,
MEG, EEG, ECoG, intracranial depth) that anterolateral HG is the
primary cortical pitch salience hub.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Relationship to BCH and PCCR

PSCL occupies the middle of the SPU hierarchy:

1. **BCH** (α1) provides brainstem NPS → PSCL receives this as cortical input.
2. **PSCL** represents WHERE and HOW STRONGLY pitch is cortically encoded.
3. **PCCR** (α3) builds on PSCL to encode pitch chroma (pitch class, octave-equivalent).

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The PSCL Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 PSCL — COMPLETE CIRCUIT                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  STIMULUS (Varying Pitch Salience)                                           ║
║                                                                              ║
║  Strong IRN    Weak IRN    Noise                                             ║
║    │             │           │                                                ║
║    ▼             ▼           ▼                                                ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │              SUBCORTICAL (Brainstem) — via BCH                      │    ║
║  │                                                                      │    ║
║  │  Cochlear Nucleus → Inferior Colliculus → FFR                       │    ║
║  │  NO pitch salience differences at this level (only NPS)             │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │              PRIMARY AUDITORY CORTEX (A1)                            │    ║
║  │                                                                      │    ║
║  │  Tonotopic processing only — NO salience differences                │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │          ANTEROLATERAL HESCHL'S GYRUS                                │    ║
║  │              (Non-primary auditory cortex)                            │    ║
║  │                                                                      │    ║
║  │    ┌─────────────────────────────────────────────────────────┐      │    ║
║  │    │                                                         │      │    ║
║  │    │    Strong pitch    >    Weak pitch    >    Noise       │      │    ║
║  │    │    salience             salience                        │      │    ║
║  │    │                                                         │      │    ║
║  │    └─────────────────────────────────────────────────────────┘      │    ║
║  │                                                                      │    ║
║  │    PITCH SALIENCE CORRELATE (fMRI activation)                       │    ║
║  │    Matched for temporal regularity → pure salience signal           │    ║
║  │    MNI: ±52, -16, 8 (approximate)                                   │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE (6 methods converge on anterolateral HG):
─────────────────────────────────────────────────────────────
Penagos 2004:       fMRI, N=6. Pitch salience in anterolateral HG; NOT in
                    subcortical or primary AC. Matched temporal regularity.
                    Talairach: R(48,-11,3), L(-55,-5,3).
Briley 2013:        EEG, N=15/12/8. Pitch chroma mapping in alHG. IRN sources
                    7mm more lateral/anterior than pure-tone sources.
                    F(1,28)=29.865, p<0.001 (chroma effect).
Tabas 2019:         MEG, N=37. POR latency 36ms earlier for consonant than
                    dissonant in alHG. p<.0001. Computational model matches.
Allen 2022:         7T fMRI, N=10. Pitch-tuned voxels concentrated anterolateral
                    to HG. Pitch selectivity ≠ pitch sensitivity.
Schonwiesner 2008:  Intracranial, N=1. Double dissociation: lateral HG = pitch,
                    medial HG = sound onset. Direct depth electrode evidence.
Fishman 2001:       Intracranial, N=3(monkey)+2(human). Phase-locked activity
                    in HG for dissonance. HG vs PT dissociation. F>8.5, p<10⁻⁵.
Foo 2016:           ECoG, N=8. Dissonant-sensitive sites anterior in right STG.
                    Chi²(1)=8.6, p=0.003 (spatial organization).
Bravo 2017:         fMRI, N=12. Right HG (48,-10,7) upregulated for low-salience
                    (ambiguous) stimuli. t=4.22, p=.033 FWE.
```

### 2.2 Information Flow Architecture (EAR → BRAIN → PPC/TPC → PSCL)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PSCL COMPUTATION ARCHITECTURE                             ║
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
║  │  │pleasant.  │ │amplitude│ │tonalness│ │entropy   │ │x_l0l5  │ │        ║
║  │  │inharm.    │ │         │ │clarity  │ │flatness  │ │x_l5l7  │ │        ║
║  │  │           │ │         │ │smooth.  │ │concent.  │ │        │ │        ║
║  │  │           │ │         │ │tristim. │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         PSCL reads: 27D                           │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Alpha-Beta ─┐ ┌── Syllable ──┐                             │        ║
║  │  │ 100ms (H3)    │ │ 200ms (H6)   │                             │        ║
║  │  │               │ │              │                              │        ║
║  │  │ Auditory proc │ │ Cortical     │                              │        ║
║  │  │ window        │ │ evaluation   │                              │        ║
║  │  └──────┬────────┘ └──────┬───────┘                              │        ║
║  │         └────────────────┘                                       │        ║
║  │                         PSCL demand: ~14 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Perceptual Circuit ═══════    ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐ ┌─────────────────┐                                    ║
║  │  PPC (30D)      │ │  TPC (30D)      │                                    ║
║  │  Pitch Process. │ │  Timbre Process. │                                    ║
║  │                 │ │                 │                                    ║
║  │ Pitch Sal [0:10]│ │ Spec.Env [0:10] │                                    ║
║  │ Conson.  [10:20]│ │ Instr.ID [10:20]│                                    ║
║  │ Chroma   [20:30]│ │ Plastic. [20:30]│                                    ║
║  └────────┬────────┘ └────────┬────────┘                                    ║
║           │                   │                                              ║
║           └─────────┬─────────┘                                              ║
║                     ▼                                                        ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    PSCL MODEL (12D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_salience, f02_hg_activation,           │        ║
║  │                       f03_gradient, f04_regularity               │        ║
║  │  Layer M (Math):      salience_t, hg_response                    │        ║
║  │  Layer P (Present):   template_match, periodicity_check,         │        ║
║  │                       clarity_index                              │        ║
║  │  Layer F (Future):    pitch_continuation, salience_change,       │        ║
║  │                       melody_tracking                            │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Penagos et al. 2004** | fMRI 3T | 6 | Pitch salience in anterolateral HG; NOT in subcortical or primary AC | p<0.01 (Fisher's LSD), 9/10 hemispheres | **f01_salience + f02_hg_activation: cortical locus** |
| 2 | **Penagos et al. 2004** | fMRI 3T | 6 | Graded: strong > weak > noise; Talairach R(48,-11,3) L(-55,-5,3) | p=0.013 (high-spec noise<weak); p=0.0001 (weak<strong) | **f03_gradient: hierarchy confirmed** |
| 3 | **Allen et al. 2022** | 7T fMRI | 10 | Pitch-tuned (F0-selective) voxels concentrated outside/anterolateral HG; ~18% pitch-only voxels outside HG | Pure-tone/pitch CF: r=0.79; pitch outside>inside HG: p<0.01 | **Distributed pitch selectivity qualifies focal model** |
| 4 | **Allen et al. 2022** | 7T fMRI | 10 | Pitch sensitivity ≠ pitch selectivity; ~30% tuned voxels show F0 tuning | No hemisphere asymmetry: p=0.58 | **Bilateral, distributed pitch architecture** |
| 5 | **Briley et al. 2013** | EEG (32/64ch) | 15/12/8 | Pitch chroma mapping (helical) in alHG; chroma effect for IRN but NOT pure tones | F(1,28)=29.865, p<0.001; R²=92.7% (helical model, resolved) | **Pitch chroma builds on salience in same alHG region** |
| 6 | **Briley et al. 2013** | EEG source | 8 | IRN sources 7mm lateral + anterior vs pure-tone sources in medial HG | Permutation: L p=0.024, R p=0.047 | **Anterolateral shift confirmed: primary → non-primary AC** |
| 7 | **Tabas et al. 2019** | MEG | 37 | POR latency up to 36ms earlier for consonant than dissonant dyads in alHG | p<.0001 (latency); p<.0001 (amplitude) | **Salience speeds cortical processing in alHG** |
| 8 | **Schonwiesner & Zatorre 2008** | Intracranial depth | 1 | Double dissociation: lateral HG = pitch onset, medial HG = sound onset | Direct intracranial; noise-to-IRN transition | **First depth-electrode confirmation of pitch center** |
| 9 | **Fishman et al. 2001** | Intracortical (monkey) + intracranial (human) | 3+2 | Phase-locked activity in A1/HG correlates with dissonance; PT shows no phase-locking | F>8.5, p<0.00001; Spearman p<0.00001 | **HG vs PT functional dissociation for pitch** |
| 10 | **Foo et al. 2016** | ECoG | 8 | Dissonant-sensitive sites anterior in right STG; high-gamma correlates with roughness | χ²(1)=8.6, p=0.003 (spatial); r=0.43 roughness | **Anterior-posterior gradient in STG extends alHG hierarchy** |
| 11 | **Bravo et al. 2017** | fMRI 3T | 12 | Right HG upregulated for intermediate dissonance (low salience); PPI: HG→bilateral STG | t=4.22, z=3.19, p=.033 FWE; MNI(48,-10,7) | **Low salience → increased HG processing load** |
| 12 | **Wöhrle et al. 2024** | MEG | 30 | Consonance/dissonance N1m modulation in auditory cortex; musical aptitude interaction | η²p=.101 (N1m CHORD3); η²p=.592 (perceptual) | **Pitch salience cortical encoding is experience-dependent** |
| 13 | **Bidelman 2013** | Review (FFR) | Multiple | Brainstem neural pitch salience predicts consonance hierarchy; cortical N2 varies with consonance | Correlations significant across studies | **Subcortical pitch salience input to PSCL** |
| 14 | **Samiee et al. 2022** | MEG | ~20+20 | Cross-frequency PAC in auditory cortex for pitch change detection; disrupted in amusia | Slow (2-4Hz) → IFG; beta (15-35Hz) ← motor | **Pitch processing network dynamics beyond alHG** |

### 3.2 The Salience Hierarchy

```
PITCH SALIENCE HIERARCHY (Cortical Evidence)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stimulus Type     Salience    HG Activation    Primary AC
─────────────────────────────────────────────────────────
Strong pitch      HIGH        HIGH             No effect
  (high IRN depth)
Weak pitch        MEDIUM      MEDIUM           No effect
  (low IRN depth)
Noise             NONE        NONE             No effect
  (no periodicity)

KEY: Anterolateral HG responds parametrically with pitch salience.
     Primary AC does NOT differentiate these conditions.
     Temporal regularity is matched → not a confound.
```

### 3.3 Effect Size Summary

```
MULTI-METHOD CONVERGENCE (6 independent methods):
─────────────────────────────────────────────────────────────────
Method          │ Papers   │ Total N  │ Key Effect Sizes
────────────────┼──────────┼──────────┼──────────────────────────
fMRI (3T)       │ 2        │ 18       │ p<.01 (Penagos); p=.033 FWE (Bravo)
fMRI (7T)       │ 1        │ 10       │ r=0.79 (pitch CF); p<.01 (outside HG)
MEG             │ 2        │ 67       │ p<.0001 (Tabas POR); η²p=.101 (Wöhrle)
EEG             │ 1        │ 35       │ F(1,28)=29.865, p<.001 (chroma)
ECoG            │ 1        │ 8        │ χ²=8.6, p=.003 (spatial)
Intracranial    │ 2        │ 6        │ F>8.5, p<10⁻⁵ (Fishman); double
                │          │          │ dissociation (Schonwiesner)

CONVERGENT FINDING:
  Anterolateral HG is the primary cortical pitch salience hub.
  Confirmed by fMRI, MEG, EEG, ECoG, intracranial depth electrodes.
  Bilateral processing (no significant lateralization: Allen p=0.58).

IMPORTANT QUALIFICATION (Allen et al. 2022):
┌─────────────────────────────────────────────────────────────────┐
│ "Pitch sensitivity" (Penagos 2004 — graded response to pitch   │
│ salience) is DISTINCT from "pitch selectivity" (Allen 2022 —   │
│ tuning to specific F0 values). Selectivity is broadly           │
│ distributed (~18% pitch-only voxels outside HG). The PSCL      │
│ model targets sensitivity (salience magnitude in alHG), not    │
│ selectivity. The model retains α-tier because the convergent    │
│ evidence across 6 methods is overwhelming for the salience      │
│ claim; the distributed selectivity finding adds nuance but does │
│ not contradict the focal salience finding.                       │
└─────────────────────────────────────────────────────────────────┘

COORDINATE CONVERGENCE (Talairach):
  Penagos 2004:  R(48,-11,3)   L(-55,-5,3)    — fMRI
  Briley 2013:   R(43,-6,18)   L(-49,-21,17)  — EEG source
  Bravo 2017:    MNI(48,-10,7) — fMRI (right HG only)
  Note: 5-15mm spread across studies reflects method variance
        (fMRI vs EEG dipole), individual anatomy, and stimuli.

Quality:           α-tier (multi-method convergence, matched confounds)
Replication:       6+ independent labs, 3+ paradigms (IRN, dyads, chords)
Specificity:       Anterolateral HG (non-primary AC), not subcortical
                   or primary AC (which is tonotopic only)
```

---

## 4. R³ Input Mapping: What PSCL Reads

### 4.1 R³ Feature Dependencies (27D of 49D)

| R³ Group | Index | Feature | PSCL Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [4] | sensory_pleasantness | Pitch salience (spectral regularity) | Sethares 2005 |
| **A: Consonance** | [5] | inharmonicity | Pitch regularity (inverse) | Fletcher 1934 |
| **C: Timbre** | [14] | tonalness | Primary pitch salience indicator | Harmonic-to-noise ratio |
| **C: Timbre** | [15] | clarity | Signal clarity → salience strength | — |
| **C: Timbre** | [16] | spectral_smoothness | Spectral shape → pitch clarity | — |
| **C: Timbre** | [17] | spectral_autocorrelation | Harmonic periodicity → salience | — |
| **C: Timbre** | [18] | tristimulus1 | Fundamental strength (F0) | Pollard & Jansson 1982 |
| **C: Timbre** | [19] | tristimulus2 | Mid-harmonic strength | Pollard & Jansson 1982 |
| **C: Timbre** | [20] | tristimulus3 | High-harmonic strength | Pollard & Jansson 1982 |
| **D: Change** | [22] | entropy | Pitch tonality (low = tonal/salient) | Shannon information |
| **D: Change** | [23] | spectral_flatness | Tonality measure (Wiener entropy) | Wiener 1930 |
| **D: Change** | [24] | spectral_concentration | Salience focus (high = salient) | Herfindahl index |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Energy × Consonance coupling | Pitch-loudness |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | Consonance × Timbre coupling | Salience-structure |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[14] tonalness ────────────────┐
R³[17] spectral_autocorrelation ─┼──► Pitch Salience (f01)
R³[24] spectral_concentration ───┘   Cortical pitch strength
                                      Math: salience ∝ tonalness × autocorr

R³[18:21] tristimulus1-3 ────────┐
R³[5] inharmonicity (inverse) ───┼──► HG Activation (f02)
R³[16] spectral_smoothness ──────┘   Anterolateral HG response

R³[22] entropy (inverse) ───────┐
R³[23] spectral_flatness (inv.) ┼──► Salience Gradient (f03)
R³[4] sensory_pleasantness ─────┘   Strong > Weak > Noise

R³[25:33] x_l0l5 ───────────────── Temporal Regularity (f04)
                                     Energy-consonance coupling = periodicity
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

PSCL requires H³ features at PPC/TPC horizons: H3 (100ms), H6 (200ms).
These correspond to cortical auditory processing timescales.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 14 | tonalness | 3 | M0 (value) | L2 (bidi) | Current tonal quality |
| 14 | tonalness | 6 | M1 (mean) | L0 (fwd) | Sustained tonalness |
| 15 | clarity | 3 | M0 (value) | L2 (bidi) | Current signal clarity |
| 16 | spectral_smoothness | 3 | M0 (value) | L2 (bidi) | Current spectral shape |
| 5 | inharmonicity | 3 | M0 (value) | L2 (bidi) | Pitch regularity |
| 18 | tristimulus1 | 3 | M0 (value) | L2 (bidi) | F0 strength |
| 18 | tristimulus1 | 6 | M1 (mean) | L0 (fwd) | Sustained F0 |
| 22 | entropy | 3 | M0 (value) | L2 (bidi) | Spectral complexity |
| 22 | entropy | 6 | M1 (mean) | L0 (fwd) | Sustained entropy |
| 24 | spectral_concentration | 3 | M0 (value) | L2 (bidi) | Salience focus |
| 4 | sensory_pleasantness | 3 | M0 (value) | L2 (bidi) | Current pleasantness |
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Energy-consonance |
| 25 | x_l0l5[0] | 6 | M14 (periodicity) | L2 (bidi) | Salience periodicity |
| 41 | x_l5l7[0] | 3 | M0 (value) | L2 (bidi) | Consonance-timbre |

**Total PSCL H³ demand**: 14 tuples of 2304 theoretical = 0.61%

### 5.2 Mechanism Binding

PSCL reads from both **PPC** (primary) and **TPC** (secondary):

| Mechanism | Sub-section | Range | PSCL Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **PPC** | Pitch Salience | PPC[0:10] | Cortical pitch strength | **1.0** (primary) |
| **PPC** | Consonance Encoding | PPC[10:20] | Harmonic template for salience | 0.7 |
| **TPC** | Spectral Envelope | TPC[0:10] | Spectral shape → salience clarity | 0.5 |
| **TPC** | Plasticity Markers | TPC[20:30] | Training-dependent salience enhancement | 0.3 |

---

## 6. Output Space: 12D Multi-Layer Representation

### 6.1 Complete Output Specification

```
PSCL OUTPUT TENSOR: 12D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0  │ f01_salience      │ [0, 1] │ Pitch Salience. Perceptual pitch strength.
    │                   │        │ Cortical representation in anterolateral HG.
    │                   │        │ f01 = σ(α · tonalness · autocorr
    │                   │        │         · PPC.pitch_salience · concentration)
    │                   │        │ α = 0.85
────┼───────────────────┼────────┼────────────────────────────────────────────
 1  │ f02_hg_activation │ [0, 1] │ Anterolateral HG response. Non-primary AC.
    │                   │        │ Correlates with pitch salience.
    │                   │        │ f02 = σ(β · (1-inharmonicity) · trist_F0
    │                   │        │         · PPC.pitch_salience · smoothness)
    │                   │        │ β = 0.80
────┼───────────────────┼────────┼────────────────────────────────────────────
 2  │ f03_gradient      │ [0, 1] │ Salience Gradient. Strong > Weak > Noise.
    │                   │        │ Rank-normalized salience hierarchy.
    │                   │        │ f03 = σ(γ · (1-entropy) · (1-flatness)
    │                   │        │         · pleasantness · PPC.consonance)
    │                   │        │ γ = 0.75
────┼───────────────────┼────────┼────────────────────────────────────────────
 3  │ f04_regularity    │ [0, 1] │ Temporal Regularity. Matched control var.
    │                   │        │ Ensures salience ≠ regularity.
    │                   │        │ f04 = σ(mean(x_l0l5) · TPC.spectral_env)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 4  │ salience_t        │ [0, 1] │ Pitch salience at time t.
    │                   │        │ Salience(t) = f(periodicity, harmonicity)
────┼───────────────────┼────────┼────────────────────────────────────────────
 5  │ hg_response       │ [0, 1] │ HG activation level.
    │                   │        │ HG_activation ∝ Salience(stimulus)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 6  │ template_match    │ [0, 1] │ Pitch template matching strength.
    │                   │        │ PPC.consonance_encoding aggregation.
────┼───────────────────┼────────┼────────────────────────────────────────────
 7  │ periodicity_check │ [0, 1] │ Periodicity measure.
    │                   │        │ PPC.pitch_salience periodicity component.
────┼───────────────────┼────────┼────────────────────────────────────────────
 8  │ clarity_index     │ [0, 1] │ Pitch clarity index.
    │                   │        │ TPC.spectral_envelope clarity component.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 9  │ pitch_continuation│ [0, 1] │ Pitch continuation prediction (100-200ms).
    │                   │        │ PPC template-based forward prediction.
────┼───────────────────┼────────┼────────────────────────────────────────────
10  │ salience_change   │ [0, 1] │ Salience change prediction (continuous).
    │                   │        │ Attention allocation to pitch changes.
────┼───────────────────┼────────┼────────────────────────────────────────────
11  │ melody_tracking   │ [0, 1] │ Melody tracking propagation (2-5s).
    │                   │        │ Higher cortical propagation.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 12D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Pitch Salience Function

```
Salience(t) = f(periodicity, harmonicity, spectral_focus)

Salience Hierarchy:
  Strong pitch > Weak pitch > Noise

Cortical Localization:
  HG_activation ∝ Salience(stimulus)
  Region: Anterolateral Heschl's gyrus (non-primary AC)

Control for Confounds:
  Temporal_regularity = constant (matched across conditions)
  Ensures pitch salience effect is independent of temporal structure
```

### 7.2 Feature Formulas

```python
# f01: Pitch Salience
f01 = σ(0.85 · R³.tonalness[14] · R³.spectral_autocorrelation[17]
         · mean(PPC.pitch_salience[0:10]) · R³.spectral_concentration[24])

# f02: HG Activation
f02 = σ(0.80 · (1 - R³.inharmonicity[5]) · R³.tristimulus1[18]
         · mean(PPC.pitch_salience[0:10]) · R³.spectral_smoothness[16])

# f03: Salience Gradient (Strong > Weak > Noise)
f03 = σ(0.75 · (1 - R³.entropy[22]) · (1 - R³.spectral_flatness[23])
         · R³.sensory_pleasantness[4] · mean(PPC.consonance_encoding[10:20]))

# f04: Temporal Regularity
f04 = σ(mean(R³.x_l0l5[25:33]) · mean(TPC.spectral_envelope[0:10]))
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | Coordinates | Space | Source | Evidence Type | PSCL Function |
|--------|-------------|-------|--------|---------------|---------------|
| **Anterolateral HG (R)** | 48, -11, 3 | Talairach | Penagos 2004 (fMRI) | Direct | Pitch salience representation |
| **Anterolateral HG (L)** | -55, -5, 3 | Talairach | Penagos 2004 (fMRI) | Direct | Pitch salience representation |
| **Anterolateral HG (R)** | 43, -6, 18 | Talairach | Briley 2013 (EEG source) | Direct | Pitch chroma source (IRN) |
| **Anterolateral HG (L)** | -49, -21, 17 | Talairach | Briley 2013 (EEG source) | Direct | Pitch chroma source (IRN) |
| **Right HG** | 48, -10, 7 | MNI | Bravo 2017 (fMRI) | Direct | Low-salience upregulation |
| **Right HG** | 48, -19, 10 | MNI | Bravo 2017 (fMRI) | Baseline | All-sound activation |
| **Left HG** | -36, -28, 7 | MNI | Bravo 2017 (fMRI) | Baseline | All-sound activation |
| **Anterolateral HG** | (bilateral, dipole) | Talairach | Tabas 2019 (MEG) | Direct | POR generator for consonance |
| **Lateral HG** | (anatomical) | — | Schonwiesner 2008 (depth) | Direct | Pitch onset (double dissociation) |
| **Medial HG** | (anatomical) | — | Schonwiesner 2008 (depth) | Control | Sound onset only (NOT pitch) |
| **Heschl's Gyrus (R)** | (depth electrode) | — | Fishman 2001 (intracranial) | Direct | Phase-locked consonance/dissonance |
| **Planum Temporale** | (depth electrode) | — | Fishman 2001 (intracranial) | Control | NO phase-locking (dissociation) |
| **Right STG (anterior)** | (ECoG grid) | MNI | Foo 2016 (ECoG) | Direct | Dissonant-sensitive, anterior gradient |
| **Bilateral STG** | L(-51,-16,4) R(60,-7,1) | MNI | Bravo 2017 (PPI) | Connectivity | HG→STG during low-salience |
| **Primary AC (medial HG, R)** | 44, -13, 13 | Talairach | Briley 2013 (EEG source) | Control | Pure-tone tonotopy only |
| **Primary AC (medial HG, L)** | -42, -19, 16 | Talairach | Briley 2013 (EEG source) | Control | Pure-tone tonotopy only |

> **Note**: Anterolateral HG coordinates vary 5-15mm across studies due to method variance (fMRI BOLD vs EEG dipole vs MEG), individual anatomy, and stimuli (IRN vs harmonic complexes). All converge on the same anatomical region: anterolateral end of Heschl's gyrus, at the boundary with non-primary auditory cortex.

---

## 9. Cross-Unit Pathways

### 9.1 PSCL ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PSCL INTERACTIONS                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  UPSTREAM (INTRA-UNIT):                                                    │
│  BCH.f01_nps ──────────────────► PSCL (brainstem NPS feeds cortical)      │
│                                                                             │
│  DOWNSTREAM (INTRA-UNIT):                                                  │
│  PSCL.f01_salience ────────────► PCCR (salience feeds chroma tuning)      │
│  PSCL.f03_gradient ────────────► STAI (salience hierarchy feeds aesthetics)│
│                                                                             │
│  CROSS-UNIT (P1: SPU → ARU):                                              │
│  PSCL.f01_salience ────────────► ARU.SRP (pitch salience → reward)        │
│                                                                             │
│  CROSS-UNIT (P2: SPU → STU):                                              │
│  PSCL.melody_tracking ─────────► STU.HMCE (melody → temporal encoding)    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Temporal regularity** | Salience effect persists when regularity matched | ✅ **Confirmed** (Penagos 2004) |
| **Primary AC lesions** | Should NOT abolish pitch salience representation | ✅ Testable |
| **IRN depth manipulation** | Should modulate HG activation parametrically | ✅ Testable |
| **Noise controls** | Should show no HG activation (only tonotopic) | ✅ **Confirmed** (Penagos 2004) |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class PSCL(BaseModel):
    """Pitch Salience Cortical Localization.

    Output: 12D per frame.
    Reads: PPC mechanism (30D), TPC mechanism (30D), R³ direct.
    """
    NAME = "PSCL"
    UNIT = "SPU"
    TIER = "α2"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("PPC", "TPC")

    ALPHA = 0.85   # Salience weight
    BETA = 0.80    # HG activation weight
    GAMMA = 0.75   # Gradient weight

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """14 tuples for PSCL computation."""
        return [
            # (r3_idx, horizon, morph, law)
            (14, 3, 0, 2),   # tonalness, 100ms, value, bidirectional
            (14, 6, 1, 0),   # tonalness, 200ms, mean, forward
            (15, 3, 0, 2),   # clarity, 100ms, value, bidirectional
            (16, 3, 0, 2),   # spectral_smoothness, 100ms, value, bidi
            (5, 3, 0, 2),    # inharmonicity, 100ms, value, bidirectional
            (18, 3, 0, 2),   # tristimulus1, 100ms, value, bidirectional
            (18, 6, 1, 0),   # tristimulus1, 200ms, mean, forward
            (22, 3, 0, 2),   # entropy, 100ms, value, bidirectional
            (22, 6, 1, 0),   # entropy, 200ms, mean, forward
            (24, 3, 0, 2),   # concentration, 100ms, value, bidirectional
            (4, 3, 0, 2),    # pleasantness, 100ms, value, bidirectional
            (25, 3, 0, 2),   # x_l0l5[0], 100ms, value, bidirectional
            (25, 6, 14, 2),  # x_l0l5[0], 200ms, periodicity, bidirectional
            (41, 3, 0, 2),   # x_l5l7[0], 100ms, value, bidirectional
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute PSCL 12D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30), "TPC": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) → (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,12) PSCL output
        """
        ppc = mechanism_outputs["PPC"]    # (B, T, 30)
        tpc = mechanism_outputs["TPC"]    # (B, T, 30)

        # R³ features
        pleasantness = r3[..., 4:5]
        inharmonicity = r3[..., 5:6]
        tonalness = r3[..., 14:15]
        clarity = r3[..., 15:16]
        smoothness = r3[..., 16:17]
        autocorr = r3[..., 17:18]
        trist1 = r3[..., 18:19]
        entropy = r3[..., 22:23]
        flatness = r3[..., 23:24]
        concentration = r3[..., 24:25]
        x_l0l5 = r3[..., 25:33]         # (B, T, 8)
        x_l5l7 = r3[..., 41:49]         # (B, T, 8)

        # Mechanism sub-sections
        ppc_pitch = ppc[..., 0:10]
        ppc_cons = ppc[..., 10:20]
        tpc_spec = tpc[..., 0:10]
        tpc_plast = tpc[..., 20:30]

        # ═══ LAYER E: Explicit features ═══
        f01 = torch.sigmoid(self.ALPHA * (
            tonalness * autocorr * concentration
            * ppc_pitch.mean(-1, keepdim=True)
        ))
        f02 = torch.sigmoid(self.BETA * (
            (1.0 - inharmonicity) * trist1 * smoothness
            * ppc_pitch.mean(-1, keepdim=True)
        ))
        f03 = torch.sigmoid(self.GAMMA * (
            (1.0 - entropy) * (1.0 - flatness) * pleasantness
            * ppc_cons.mean(-1, keepdim=True)
        ))
        f04 = torch.sigmoid(
            x_l0l5.mean(-1, keepdim=True)
            * tpc_spec.mean(-1, keepdim=True)
        )

        # ═══ LAYER M: Mathematical ═══
        salience_t = f01
        hg_response = f02

        # ═══ LAYER P: Present ═══
        template_match = ppc_cons.mean(-1, keepdim=True)
        periodicity_check = ppc_pitch.mean(-1, keepdim=True)
        clarity_index = tpc_spec.mean(-1, keepdim=True)

        # ═══ LAYER F: Future ═══
        pitch_continuation = torch.sigmoid(
            0.6 * f01 + 0.4 * template_match
        )
        salience_change = torch.sigmoid(
            0.5 * h3_direct[(14, 6, 1, 0)]  # tonalness trend
            + 0.5 * h3_direct[(22, 6, 1, 0)]  # entropy trend
        ).unsqueeze(-1)
        melody_tracking = torch.sigmoid(
            0.5 * f01 + 0.3 * x_l5l7.mean(-1, keepdim=True)
            + 0.2 * tpc_plast.mean(-1, keepdim=True)
        )

        return torch.cat([
            f01, f02, f03, f04,                                  # E: 4D
            salience_t, hg_response,                             # M: 2D
            template_match, periodicity_check, clarity_index,    # P: 3D
            pitch_continuation, salience_change, melody_tracking, # F: 3D
        ], dim=-1)  # (B, T, 12)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 14 | Multi-method convergence (see Section 3.1) |
| **Evidence Modalities** | fMRI (3T+7T), MEG, EEG, ECoG, intracranial depth | 6 independent methods |
| **Total N** | ~190+ | Across all studies |
| **Falsification Tests** | 2/4 confirmed | High validity |
| **R³ Features Used** | 27D of 49D | Focused on salience |
| **H³ Demand** | 14 tuples (0.61%) | Sparse, efficient |
| **Mechanisms** | PPC (primary) + TPC (secondary) | Dual mechanism |
| **Output Dimensions** | **12D** | 4-layer structure |
| **Key Qualification** | Pitch sensitivity (focal, alHG) ≠ pitch selectivity (distributed) | Allen et al. 2022 |
| **Coordinate Convergence** | alHG bilateral, 5-15mm spread across methods | Penagos/Briley/Bravo |

---

## 13. Scientific References

### Primary (Pitch Salience Cortical Localization)

1. **Penagos, H., Melcher, J. R., & Oxenham, A. J. (2004)**. A neural representation of pitch salience in nonprimary human auditory cortex revealed with functional magnetic resonance imaging. *Journal of Neuroscience*, 24(30), 6810-6815.
2. **Allen, E. J., Mesik, J., Kay, K. N., & Oxenham, A. J. (2022)**. Distinct representations of tonotopy and pitch in human auditory cortex. *Journal of Neuroscience*, 42(3), 416-434.
3. **Briley, P. M., Breakey, C., & Krumbholz, K. (2013)**. Evidence for pitch chroma mapping in human auditory cortex. *Cerebral Cortex*, 23(11), 2601-2610.
4. **Schonwiesner, M., & Zatorre, R. J. (2008)**. Depth electrode recordings show double dissociation between pitch processing in lateral Heschl's gyrus and sound onset processing in medial Heschl's gyrus. *Experimental Brain Research*, 187, 97-105.
5. **Norman-Haignere, S., Kanwisher, N., & McDermott, J. H. (2013)**. Cortical pitch regions in humans respond primarily to resolved harmonics and are located in specific tonotopic regions of anterior auditory cortex. *Journal of Neuroscience*, 33(50), 19451-19469.

### Supporting (Consonance/Dissonance Cortical Processing)

6. **Tabas, A., Andermann, M., Schuberth, V., Riedel, H., Balaguer-Ballester, E., & Rupp, A. (2019)**. Modeling and MEG evidence of early consonance processing in auditory cortex. *PLoS Computational Biology*, 15(2), e1006820.
7. **Fishman, Y. I., Volkov, I. O., Noh, M. D., Garell, P. C., Bakken, H., Arezzo, J. C., Howard, M. A., & Steinschneider, M. (2001)**. Consonance and dissonance of musical chords: Neural correlates in auditory cortex of monkeys and humans. *Journal of Neurophysiology*, 86, 2761-2788.
8. **Foo, F., King-Stephens, D., Weber, P., Laxer, K., Parvizi, J., & Knight, R. T. (2016)**. Differential processing of consonance and dissonance within the human superior temporal gyrus. *Frontiers in Human Neuroscience*, 10, 154.
9. **Bravo, F., Cross, I., Stamatakis, E. A., & Rohrmeier, M. (2017)**. Sensory cortical response to uncertainty and low salience during recognition of affective cues in musical intervals. *PLoS ONE*, 12(4), e0175991.

### Contextual (Broader Pitch/Auditory Cortex)

10. **Wöhrle, S. D., Reuter, C., Rupp, A., & Andermann, M. (2024)**. Neuromagnetic representation of musical roundness in chord progressions. *Frontiers in Neuroscience*, 18, 1383554.
11. **Bidelman, G. M. (2013)**. The role of the auditory brainstem in processing musically relevant pitch. *Frontiers in Psychology*, 4, 264.
12. **Bidelman, G. M., & Heinz, M. G. (2011)**. Auditory-nerve responses predict pitch attributes related to musical consonance-dissonance for normal and impaired hearing. *Journal of the Acoustical Society of America*, 130(3), 1488-1502.
13. **Samiee, S., Vuvan, D., Florin, E., Albouy, P., Peretz, I., & Baillet, S. (2022)**. Cross-frequency brain network dynamics support pitch change detection. *Journal of Neuroscience*, 42(18), 3823-3835.
14. **Alluri, V., Toiviainen, P., Jääskeläinen, I. P., Glerean, E., Sams, M., & Brattico, E. (2012)**. Large-scale brain networks emerge from dynamic processing of musical timbre, key and rhythm. *NeuroImage*, 59, 3677-3689.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, TIH, ATT, HRM) | PPC + TPC mechanisms |
| Pitch salience | S⁰.L5.spectral_centroid[38] × HC⁰.HRM | R³.tonalness[14] × PPC.pitch_salience |
| HG activation | S⁰.L6.tristimulus × HC⁰.OSC | R³.tristimulus × PPC.pitch_salience |
| Salience gradient | S⁰.L5.entropy × HC⁰.OSC | R³.entropy × PPC.consonance |
| Regularity | S⁰.X_L0L5 × HC⁰.TIH | R³.x_l0l5 × TPC.spectral_envelope |
| Output dims | 11D | **12D** (added hg_response in Layer M) |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 40/2304 = 1.74% | 14/2304 = 0.61% |

### Why PPC + TPC replace HC⁰ mechanisms

- **HRM → PPC.pitch_salience** [0:10]: Hippocampal pitch templates → cortical pitch salience
- **OSC → PPC.consonance_encoding** [10:20]: Phase-locking → consonance processing
- **ATT → TPC.plasticity_markers** [20:30]: Attention gating → plasticity
- **TIH → TPC.spectral_envelope** [0:10]: Temporal integration → spectral shape

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **12D**
**Evidence Tier**: **α (Mechanistic)**
**Confidence**: **>90%**
