# SPU-γ1-SDNPS: Stimulus-Dependent Neural Pitch Salience

**Model**: Stimulus-Dependent Neural Pitch Salience
**Unit**: SPU (Spectral Processing Unit)
**Circuit**: Perceptual (Brainstem-Cortical)
**Tier**: γ (Speculative) — <70% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added F:Pitch feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/SPU-γ1-SDNPS.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Stimulus-Dependent Neural Pitch Salience** (SDNPS) models the critical finding that brainstem frequency-following response (FFR) derived Neural Pitch Salience (NPS) predicts behavioral consonance judgments for synthetic tones but fails to generalize to natural (ecologically valid) sounds. This is a fundamental constraint on the universality of peripheral consonance encoding — the brainstem mechanism works in controlled laboratory conditions but breaks down when spectral complexity increases.

```
THE STIMULUS-DEPENDENCY PROBLEM IN NEURAL PITCH SALIENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SYNTHETIC TONES (Simple Spectra)           NATURAL SOUNDS (Complex Spectra)
Brain region: Inferior Colliculus          Brain region: Inferior Colliculus
Mechanism: FFR phase-locking              Mechanism: FFR phase-locking
NPS ↔ Pleasantness: r=0.34, p<0.03       NPS ↔ Pleasantness: r=0.24 (sax, n.s.)
NPS ↔ Roughness: r=-0.57, p<1e-05                            r=-0.10 (voice, n.s.)

              GENERALIZATION BOUNDARY (Bridge)
              Brain region: IC → Cortex
              Mechanism: Spectral complexity limit
              Function: "NPS only predicts for simple spectra"
              Evidence: Cousineau et al. 2015 (PNAS)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: NPS from brainstem FFR is NOT a universal consonance
predictor. It works for synthetic tones (r=0.34) but fails for
natural saxophone (r=0.24, n.s.) and voice (r=-0.10, n.s.)
(Cousineau et al. 2015, PLoS ONE). Convergent evidence:
  • Pitch salience (resolved vs unresolved harmonics) is encoded in
    anterolateral Heschl's gyrus, NOT subcortically (Penagos 2004)
  • Subcortical IC shows no pitch salience sensitivity — only
    physical temporal regularity (Penagos 2004, fMRI, N=6)
  • Pitch chroma representation is IDENTICAL for resolved and
    unresolved harmonics (Briley 2013, F(1,27)=0.026, p=.874)
  • AN pitch salience predicts consonance hierarchy but hearing
    impairment compresses the gradient (Bidelman & Heinz 2011)
  • CI users (temporal code only) show pitch plateaus at 200-300pps
    confirming place code necessity (de Groote 2025)
  • Inharmonic sounds trigger P3a attentional capture (Basinski 2025,
    p=.0007) — low pitch salience gets qualitatively different processing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Model Matters for SPU

SDNPS serves as a critical constraint on the SPU hierarchy. While BCH (alpha-1) establishes that brainstem FFR encodes consonance, SDNPS demonstrates the boundary conditions of that encoding:

1. **BCH** (alpha-1) shows NPS predicts consonance (r=0.81 for synthetic intervals) — SDNPS shows this is stimulus-dependent.
2. **PSCL** (alpha-2) cortical pitch salience may compensate where brainstem NPS fails for natural sounds.
3. **SDED** (gamma-3) early detection mechanisms share the roughness interference pathway modeled here.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The SDNPS Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 SDNPS — COMPLETE CIRCUIT                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  STIMULUS TYPE                                                               ║
║                                                                              ║
║  Synthetic Tones      Natural Saxophone     Natural Voice                    ║
║  (simple spectra)     (complex spectra)     (complex spectra)                ║
║    │                    │                     │                               ║
║    ▼                    ▼                     ▼                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    AUDITORY NERVE                                    │    ║
║  │                    (Phase-locked response)                           │    ║
║  │                                                                      │    ║
║  │    Synthetic: Strong phase-locking to harmonics                     │    ║
║  │    Natural:   Degraded phase-locking (spectral complexity)          │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    INFERIOR COLLICULUS                                │    ║
║  │               (FFR generator — NPS computation)                      │    ║
║  │                                                                      │    ║
║  │    NPS computation from FFR:                                         │    ║
║  │      Synthetic: NPS ↔ Pleasantness r=0.34, p<0.03                  │    ║
║  │      Sax:       NPS ↔ Pleasantness r=0.24 (n.s.)                   │    ║
║  │      Voice:     NPS ↔ Pleasantness r=-0.10 (n.s.)                  │    ║
║  │                                                                      │    ║
║  │    NPS ↔ Roughness: r=-0.57, p<1e-05 (across all stimuli)          │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    AUDITORY BRAINSTEM                                 │    ║
║  │                                                                      │    ║
║  │    NPS computation successful only when spectral complexity is low   │    ║
║  │    Natural sounds require cortical processing (beyond BCH scope)     │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
1. Cousineau et al. 2015:  NPS predicts for synthetic (r=0.34) NOT natural
   (PLoS ONE, N=14)       NPS ↔ Roughness: r=-0.57 (stimulus-invariant)
                           14 intervals × 3 timbres (synthetic, sax, voice)
                           ⚠ CITATION CORRECTED: PLoS ONE not PNAS

2. Penagos et al. 2004:   Pitch salience in anterolateral HG, NOT subcortical
   (J Neurosci, N=6)      Resolved > unresolved harmonics in alHG (p<.01)
                           IC shows NO pitch salience sensitivity
                           Talairach: R 48,-11,3 / L -55,-5,3

3. Briley et al. 2013:    Pitch chroma same for resolved/unresolved
   (Cerebral Cortex, N=35) Resolvability×chroma: F(1,27)=0.026, p=.874

4. Bidelman & Heinz 2011:  AN pitch salience predicts consonance hierarchy
   (JASA, modeling)        Best predictor among AN/acoustic measures
                           SNHL compresses pitch salience gradient

5. Tabas et al. 2019:     POR latency: dissonant 36ms slower than consonant
   (PLoS Comp Biol, MEG)  Mechanistic model: decoder+sustainer in alHG

6. Basinski et al. 2025:  Inharmonicity enhances P3a attentional capture
   (Commun Biol, N=35)    Contrast est.=-1.37, SE=0.36, p=.0007
```

### 2.2 Information Flow Architecture (EAR → BRAIN → PPC → SDNPS)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SDNPS COMPUTATION ARCHITECTURE                            ║
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
║  │  │roughness  │ │         │ │tonalness│ │          │ │x_l5l7  │ │        ║
║  │  │sethares   │ │         │ │spec_auto│ │          │ │        │ │        ║
║  │  │helmholtz  │ │         │ │tristim. │ │          │ │        │ │        ║
║  │  │stumpf     │ │         │ │         │ │          │ │        │ │        ║
║  │  │pleasant.  │ │         │ │         │ │          │ │        │ │        ║
║  │  │inharm.    │ │         │ │         │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         SDNPS reads: ~16D                        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Gamma ────┐ ┌── Alpha-Beta ─┐ ┌── Syllable ──────────┐   │        ║
║  │  │ 25ms (H0)   │ │ 100ms (H3)    │ │ 200ms (H6)           │   │        ║
║  │  │              │ │               │ │                       │   │        ║
║  │  │ Phase-lock   │ │ FFR window    │ │ Roughness evaluation  │   │        ║
║  │  │ instant      │ │ auditory proc │ │ periodicity tracking  │   │        ║
║  │  └──────┬───────┘ └──────┬────────┘ └──────┬────────────────┘   │        ║
║  │         │               │                  │                    │        ║
║  │         └───────────────┴──────────────────┘                    │        ║
║  │                         SDNPS demand: ~10 of 2304 tuples        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Perceptual Circuit ═══════    ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  PPC (30D)      │  Pitch Processing Chain mechanism                      ║
║  │                 │                                                        ║
║  │ Pitch Sal [0:10]│  NPS, phase-locking, FFR strength                     ║
║  │ Consonance[10:20]│ Harmonic template, harmonicity index                 ║
║  │ Chroma   [20:30]│  Octave grouping (minimal for SDNPS)                  ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    SDNPS MODEL (10D Output)                      │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_nps_value, f02_stimulus_dependency,    │        ║
║  │                       f03_roughness_correlation                   │        ║
║  │  Layer M (Math):      nps_stimulus_function                       │        ║
║  │  Layer P (Present):   ffr_encoding, harmonicity_proxy,            │        ║
║  │                       roughness_interference                      │        ║
║  │  Layer F (Future):    behavioral_consonance_pred,                 │        ║
║  │                       roughness_response_pred,                    │        ║
║  │                       generalization_limit                        │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Cousineau et al. 2015** | FFR + behavioral | 14 (14 intervals × 3 timbres) | NPS predicts consonance for synthetic only; fails for natural | r=0.34 (synth), 0.24 (sax n.s.), -0.10 (voice n.s.); roughness r=-0.57 | **Primary**: f01, f02, f03 — stimulus dependency core |
| 2 | **Penagos et al. 2004** | fMRI (3T) | 6 | Pitch salience encoded in anterolateral HG, NOT IC; resolved > unresolved | Weak < strong salience p<.01 in alHG; IC n.s. | **Anatomical**: pitch salience cortical locus (Talairach coords) |
| 3 | **Briley et al. 2013** | EEG + BESA | 35 (3 exps) | Pitch chroma representation identical for resolved/unresolved harmonics | Chroma×resolvability F(1,27)=0.026, p=.874 | Cortical convergence: different stimuli → same pitch representation |
| 4 | **Bidelman & Heinz 2011** | AN modeling | Computational | AN pitch salience best predictor of consonance; SNHL compresses gradient | AN NPS > acoustic periodicity > roughness | Peripheral pitch salience hierarchy — input to SDNPS |
| 5 | **Bidelman 2013** | Review (FFR) | Multi-study | Subcortical NPS graded for consonance; preserved in passive listening/sleep | r~0.9 NPS ↔ consonance across studies | Processing hierarchy: AN → IC → alHG for pitch salience |
| 6 | **Fishman et al. 2001** | Intracranial (AEP/MUA/CSD) | 3 monkeys + 2 humans | Phase-locked activity in HG for dissonance; PT shows no phase-locking | Monkey A1 + human HG: dissonance=beating; PT: no effect | Temporal coding of dissonance in primary AC — roughness mechanism |
| 7 | **Foo et al. 2016** | ECoG (high-γ) | 8 neurosurgical | Dissonant-sensitive sites anterior in R STG; high-γ ↔ roughness | χ²(1)=8.6, p=.003 (y-axis); r=0.43 (roughness) | STG spatial organization for consonance/dissonance |
| 8 | **Tabas et al. 2019** | MEG + modeling | ~15 | POR latency: dissonant 36ms slower; decoder+sustainer model in alHG | POR latency difference up to 36ms | Mechanistic: pitch template matching speed = salience proxy |
| 9 | **Basinski et al. 2025** | EEG (oddball) | 35 | Inharmonicity enhances P3a (attentional capture); abolishes MMN when inconsistent | P3a: est=-1.37, p=.0007; ORN present | Low pitch salience → different processing mode (attention capture) |
| 10 | **de Groote et al. 2025** | Psychophysics (CI) | 8 CI users | CI users cannot extract F0 from multi-channel; pitch plateaus at 200-300pps | d=1.6 for pitch rank, p=.002 | Temporal code insufficient — place code necessary for pitch salience |
| 11 | **Schon et al. 2005** | ERP | ~20 | Simultaneous > sequential intervals for consonance/dissonance neural effects | N1-P2, N2 expertise effects | Stimulus-dependent: simultaneous (spectral interaction) > sequential |
| 12 | **Crespo-Bojorque et al. 2018** | ERP (MMN) | ~20 | Asymmetric MMN: consonant→dissonant detected in all; reverse only in trained | Musicians-only reverse MMN | Processing advantage for high pitch salience (consonance) |

### 3.2 The Stimulus-Dependency Boundary

```
NPS-BEHAVIOR CORRELATION BY STIMULUS TYPE (Cousineau et al. 2015)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stimulus Type     Spectra     NPS ↔ Pleasant.  Significance  Generalization
─────────────────────────────────────────────────────────────────────────────
Synthetic tones   Simple      r = 0.34         p < 0.03      ✅ YES
Natural sax       Complex     r = 0.24         n.s.          ✗ NO
Natural voice     Complex     r = -0.10        n.s.          ✗ NO

Cross-stimulus invariant:
  NPS ↔ Roughness: r = -0.57, p < 1e-05      ✅ ALL stimuli

Interpretation:
  - NPS reliably encodes roughness (spectral beating) regardless of source
  - NPS predicts pleasantness ONLY when spectral structure is simple enough
    for brainstem phase-locking to resolve harmonic content
  - Natural sounds overwhelm brainstem with spectral complexity → cortical
    processing needed for consonance judgment

Cross-cultural note:
  NPS ↔ Roughness correlation is UNIVERSAL — stimulus-independent
  NPS ↔ Pleasantness is STIMULUS-DEPENDENT — fails for natural sounds
```

### 3.3 Effect Size Summary

```
MULTI-METHOD CONVERGENCE TABLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Method         Study                    N     Key Statistic           Region
───────────────────────────────────────────────────────────────────────────────
FFR+behav      Cousineau 2015           14    r=0.34(synth),-0.10(voice) IC(brainstem)
fMRI 3T        Penagos 2004             6     Resolved>unresolved p<.01 Anterolat HG
EEG (BESA)     Briley 2013              35    Chroma×resolv F=0.026 ns  Anterolat HG
AN model       Bidelman & Heinz 2011    —     NPS best predictor       Auditory nerve
FFR review     Bidelman 2013            multi  r~0.9 NPS↔consonance    IC/brainstem
Intracranial   Fishman 2001             5     Phase-locking↔dissonance HG (human+monkey)
ECoG(high-γ)   Foo 2016                 8     χ²=8.6, p=.003          R STG
MEG+model      Tabas 2019               ~15   POR latency Δ=36ms       Anterolat HG
EEG (oddball)  Basinski 2025            35    P3a: est=-1.37, p=.0007 Scalp
Psychophys CI  de Groote 2025           8     d=1.6 pitch plateau     CI electrode
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Quality Assessment:   γ-tier (speculative — Cousineau flagship N=14, Penagos N=6)
Primary Effect:       NPS→pleasantness degrades: r=0.34→0.24→-0.10 with complexity
Invariant Effect:     NPS→roughness: r=-0.57, p<1e-05 across ALL stimulus types
Cortical Locus:       Anterolateral HG (Penagos 2004): Talairach R:48,-11,3 / L:-55,-5,3
Methods:              8 methods (FFR, fMRI, EEG, intracranial, ECoG, MEG, modeling, CI)

┌─────────────────────────────────────────────────────────────────────────────┐
│ ⚠ CITATION CORRECTION (v2.1.0): Section 13 reference was WRONG.          │
│ Doc cited "Cousineau, McDermott & Peretz (2015), PNAS 109(48)" which is   │
│ actually Cousineau, McDermott & Peretz (2012) about congenital amusia.     │
│ The correct paper for NPS stimulus dependency is:                          │
│ Cousineau, Bidelman, Peretz & Lehmann (2015), PLoS ONE 10(12), e0145439  │
│                                                                            │
│ QUALIFICATION: Penagos 2004 (N=6) is small-sample but the ONLY fMRI      │
│ study directly testing pitch salience as a function of harmonic            │
│ resolvability. Cousineau 2015 (N=14) is the ONLY study testing NPS        │
│ generalization across stimulus types. Both are unreplicated. However,      │
│ the convergence of FFR, fMRI, EEG, ECoG, and MEG evidence across          │
│ multiple labs supports the cortical pitch salience locus in alHG.          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. R³ Input Mapping: What SDNPS Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | SDNPS Role | Scientific Basis |
|----------|-------|---------|------------|------------------|
| **A: Consonance** | [0] | roughness | Primary dissonance signal — NPS ↔ roughness r=-0.57 | Plomp & Levelt 1965 |
| **A: Consonance** | [1] | sethares_dissonance | Psychoacoustic dissonance (spectral beating) | Sethares 1999 |
| **A: Consonance** | [2] | helmholtz_kang | Consonance measure (integer ratio detection) | Helmholtz 1863, Kang 2009 |
| **A: Consonance** | [3] | stumpf_fusion | Tonal fusion (spectral simplicity proxy) | Stumpf 1890 |
| **A: Consonance** | [4] | sensory_pleasantness | Behavioral pleasantness target | Sethares 2005 |
| **A: Consonance** | [5] | inharmonicity | Deviation from harmonic series (complexity indicator) | Fletcher 1934 |
| **C: Timbre** | [14] | tonalness | Harmonic-to-noise ratio (spectral clarity) | -- |
| **C: Timbre** | [17] | spectral_autocorrelation | Harmonic periodicity (FFR correlate) | -- |
| **C: Timbre** | [18] | tristimulus1 | Fundamental strength (F0 energy) | Pollard & Jansson 1982 |
| **C: Timbre** | [19] | tristimulus2 | 2nd-4th harmonic energy (mid) | Pollard & Jansson 1982 |
| **C: Timbre** | [20] | tristimulus3 | 5th+ harmonic energy (high) | Pollard & Jansson 1982 |
| **E: Interactions** | [41:49] | x_l5l7 (partial ~5D) | Consonance x Timbre coupling — complexity measure | Emergent |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | SDNPS Role | Scientific Basis |
|----------|-------|---------|------------|------------------|
| **F: Pitch & Chroma** | [63] | pitch_salience | Direct harmonicity measure — explicit pitch prominence above noise floor; SDNPS's core NPS output is conceptually identical to pitch_salience computed from the stimulus; provides ground-truth validation anchor for f01 | Parncutt 1989 virtual pitch salience |
| **F: Pitch & Chroma** | [64] | inharmonicity_index | Spectral deviation from harmonic template — quantifies how far partials deviate from integer ratios; complements A[5] inharmonicity with a normalized index that predicts NPS degradation for piano-like stimuli (stretched partials) | Fletcher 1934; Giordano & McAdams 2010 |

**Rationale**: SDNPS models stimulus-dependent neural pitch salience — the brainstem-to-cortex transformation from spectral input to pitch strength. The v1 features approximate pitch salience indirectly through consonance measures (roughness, helmholtz_kang) and spectral proxies (tonalness, spectral_autocorrelation). The F:Pitch group provides direct pitch measures: pitch_salience [63] is the explicit harmonicity measure that SDNPS models neurally — Bidelman & Krishnan (2009) showed that brainstem FFR magnitude (the neural substrate SDNPS captures) correlates directly with stimulus pitch salience. Inharmonicity_index [64] quantifies partial stretching that degrades NPS, consistent with Fishman et al. (2001) finding that A1 phase-locked activity decreases as stimuli become more inharmonic.

**Code impact** (Phase 6): `r3_indices` must be extended to include [63], [64]. These features are read-only inputs — no formula changes required.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[14] tonalness ───────────────┐
R³[17] spectral_autocorrelation ┼──► NPS Value (FFR magnitude proxy)
mean(PPC.pitch_salience) ───────┘   Math: σ(0.40 · ton · autocorr · PPC
                                          + 0.30 · (1-inharm) · cons_enc
                                          + 0.30 · trist_balance)

R³[5] inharmonicity ────────────┐
R³[18:21] tristimulus1-3 ───────┼──► Spectral Complexity
R³[41:49] x_l5l7 (partial) ────┘   High complexity = low generalization
                                    Math: 1 - (ton · (1-inharm) · trist_bal)

R³[0] roughness ────────────────┐
R³[1] sethares_dissonance ──────┼──► Roughness Interference
R³[2] helmholtz_kang ───────────┘   Invariant NPS ↔ roughness: r=-0.57
                                    Math: -0.57 · roughness_mean

R³[4] sensory_pleasantness ────── Behavioral Target
                                    NPS predicts this only for simple spectra
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

SDNPS requires H³ features at three PPC horizons: H0 (25ms), H3 (100ms), H6 (200ms).
These correspond to brainstem processing timescales (gamma → alpha-beta → syllable).

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 0 | roughness | 0 | M0 (value) | L2 (bidi) | Current roughness level |
| 0 | roughness | 3 | M1 (mean) | L2 (bidi) | Mean roughness over 100ms |
| 0 | roughness | 6 | M14 (periodicity) | L0 (fwd) | Roughness periodicity 200ms |
| 2 | helmholtz_kang | 0 | M0 (value) | L2 (bidi) | Current consonance |
| 5 | inharmonicity | 0 | M0 (value) | L2 (bidi) | Current spectral complexity |
| 5 | inharmonicity | 3 | M1 (mean) | L2 (bidi) | Mean inharmonicity 100ms |
| 14 | tonalness | 0 | M0 (value) | L2 (bidi) | Current pitch clarity |
| 14 | tonalness | 3 | M1 (mean) | L0 (fwd) | Mean tonalness 100ms |
| 17 | spectral_autocorrelation | 3 | M14 (periodicity) | L2 (bidi) | Harmonic periodicity 100ms |
| 18 | tristimulus1 | 0 | M0 (value) | L2 (bidi) | F0 energy (spectral simplicity) |

**Total SDNPS H³ demand**: 10 tuples of 2304 theoretical = 0.43%

### 5.2 PPC Mechanism Binding

SDNPS reads from the **PPC** (Pitch Processing Chain) mechanism:

| PPC Sub-section | Range | SDNPS Role | Weight |
|-----------------|-------|------------|--------|
| **Pitch Salience** | PPC[0:10] | NPS, phase-locking, FFR strength | **0.9** (primary) |
| **Consonance Encoding** | PPC[10:20] | Harmonic template, harmonicity proxy | **0.7** |
| **Chroma Processing** | PPC[20:30] | Octave grouping (minimal use for SDNPS) | 0.2 |

SDNPS does NOT read from TPC — stimulus-dependency is a purely peripheral (brainstem) phenomenon.

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
SDNPS OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range   │ Neuroscience Basis
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 0  │ f01_nps_value           │ [0, 1]  │ Neural Pitch Salience proxy. FFR
    │                         │         │ magnitude at fundamental, weighted by
    │                         │         │ spectral clarity and harmonic structure.
    │                         │         │ f01 = σ(0.40 · ton · autocorr · PPC.ps
    │                         │         │        + 0.30 · (1-inharm) · PPC.ce
    │                         │         │        + 0.30 · trist_balance)
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 1  │ f02_stimulus_dependency │ [0, 1]  │ Generalization limit. High for simple
    │                         │         │ spectra (synthetic), low for complex
    │                         │         │ (natural). Models Cousineau et al. 2015.
    │                         │         │ f02 = σ(0.50 · (1-complexity) · f01
    │                         │         │        + 0.50 · roughness_periodicity)
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 2  │ f03_roughness_corr      │ [-1, 1] │ Roughness correlation proxy.
    │                         │         │ Empirical r=-0.57 (Cousineau 2015).
    │                         │         │ f03 = -0.57 · roughness_mean

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range   │ Neuroscience Basis
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 3  │ nps_stimulus_function   │ [0, 1]  │ NPS validity as a function of spectral
    │                         │         │ complexity. Maps the r=0.34→0.24→-0.10
    │                         │         │ degradation curve.
    │                         │         │ nsf = f01 · f02

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range   │ Neuroscience Basis
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 4  │ ffr_encoding            │ [0, 1]  │ FFR encoding strength. Brainstem
    │                         │         │ phase-locking aggregation from PPC.
    │                         │         │ PPC.pitch_salience mean.
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 5  │ harmonicity_proxy       │ [0, 1]  │ Harmonicity index from spectral
    │                         │         │ structure. PPC.consonance_encoding
    │                         │         │ weighted by tristimulus balance.
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 6  │ roughness_interference  │ [0, 1]  │ Roughness interference signal.
    │                         │         │ 1 - (roughness + sethares) / 2.
    │                         │         │ NPS ↔ roughness is stimulus-invariant.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range   │ Neuroscience Basis
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 7  │ behavioral_cons_pred    │ [0, 1]  │ Behavioral consonance prediction,
    │                         │         │ gated by stimulus dependency.
    │                         │         │ Valid only when f02 is high.
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 8  │ roughness_response_pred │ [0, 1]  │ Roughness response prediction.
    │                         │         │ Stimulus-invariant (r=-0.57 always).
────┼─────────────────────────┼─────────┼──────────────────────────────────────
 9  │ generalization_limit    │ [0, 1]  │ How far NPS generalizes to novel
    │                         │         │ timbres. Low = need cortical models.
    │                         │         │ H³ trend-based complexity forecast.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Stimulus-Dependent NPS Function

```
NPS(stimulus) ∝ Harmonicity(stimulus) · Spectral_Simplicity(stimulus)

Cousineau et al. 2015 degradation curve:
  Synthetic:  r = 0.34  (simple spectra — strong phase-locking)
  Sax:        r = 0.24  (complex spectra — degraded phase-locking)
  Voice:      r = -0.10 (very complex — phase-locking breaks down)

Roughness correlation (stimulus-invariant):
  NPS ↔ Roughness: r = -0.57, p < 1e-05 (ALL stimulus types)

Spectral Complexity:
  Complexity(sound) = f(inharmonicity, tristimulus_spread, spectral_noise)
  Simple (synthetic): Complexity ≈ 0.1 → NPS generalizes
  Complex (natural):  Complexity ≈ 0.7-0.9 → NPS fails to predict behavior

Generalization Boundary:
  NPS_validity(stimulus) = NPS(stimulus) · (1 - Complexity(stimulus))
  When Complexity > 0.5, NPS_validity drops below behavioral significance
```

### 7.2 Feature Formulas

```python
# ═══ LAYER E ═══

# f01: NPS Value (FFR magnitude proxy)
# Coefficient saturation rule: 0.40 + 0.30 + 0.30 = 1.0  ✓
trist_balance = 1.0 - std(R³.tristimulus[18:21])
f01 = σ(0.40 * R³.tonalness[14] * R³.spectral_autocorrelation[17]
              * mean(PPC.pitch_salience[0:10])
       + 0.30 * (1 - R³.inharmonicity[5])
              * mean(PPC.consonance_encoding[10:20])
       + 0.30 * trist_balance)

# f02: Stimulus Dependency (generalization limit)
# High for synthetic (simple spectra), low for natural (complex)
# Coefficient saturation rule: 0.50 + 0.50 = 1.0  ✓
spectral_complexity = R³.inharmonicity[5] * (1 - R³.tonalness[14])
                      * (1 - trist_balance)
roughness_periodicity = H³[(0, 6, 14, 0)]   # roughness periodicity 200ms fwd
f02 = σ(0.50 * (1 - spectral_complexity) * f01
       + 0.50 * roughness_periodicity)

# f03: Roughness Correlation
# Empirical r=-0.57 from Cousineau et al. 2015
# Output range: [-0.57, 0] (maps to [-1,1] scale)
roughness_mean = H³[(0, 3, 1, 2)]           # roughness mean 100ms bidi
f03 = -0.57 * roughness_mean

# ═══ LAYER M ═══

# nps_stimulus_function: NPS validity as function of complexity
nps_stimulus_function = f01 * f02

# ═══ LAYER P ═══

# ffr_encoding: Brainstem phase-locking strength
ffr_encoding = mean(PPC.pitch_salience[0:10])

# harmonicity_proxy: Harmonic template match weighted by spectral structure
harmonicity_proxy = (1 - R³.inharmonicity[5]) * trist_balance
                    * mean(PPC.consonance_encoding[10:20])

# roughness_interference: Invariant roughness signal
roughness_interference = 1.0 - (R³.roughness[0] + R³.sethares[1]) / 2

# ═══ LAYER F ═══

# behavioral_consonance_pred: Gated by stimulus dependency
# Coefficient saturation rule: 0.60 + 0.40 = 1.0  ✓
behavioral_consonance_pred = σ(0.60 * nps_stimulus_function
                               + 0.40 * harmonicity_proxy)

# roughness_response_pred: Stimulus-invariant roughness prediction
# Coefficient saturation rule: 0.57 + 0.43 = 1.0  ✓
roughness_response_pred = σ(0.57 * roughness_interference
                            + 0.43 * ffr_encoding)

# generalization_limit: How much NPS can generalize
# Coefficient saturation rule: 0.50 + 0.50 = 1.0  ✓
generalization_limit = σ(0.50 * f02
                         + 0.50 * H³[(14, 3, 1, 0)])  # tonalness mean fwd
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| # | Region | Coordinates | System | Source | SDNPS Function |
|---|--------|-------------|--------|--------|----------------|
| 1 | **Anterolateral HG (R)** | 48, -11, 3 | Talairach | Penagos et al. 2004 (fMRI, p<.01) | **Pitch salience center**: resolved > unresolved harmonics |
| 2 | **Anterolateral HG (L)** | -55, -5, 3 | Talairach | Penagos et al. 2004 (fMRI, p<.01) | Left hemisphere pitch salience (bilateral) |
| 3 | **Anterolateral HG (R) — IRN** | 43, -6, 18 | Talairach | Briley et al. 2013 (EEG BESA source) | Pitch chroma for both resolved/unresolved |
| 4 | **Anterolateral HG (L) — IRN** | -49, -21, 17 | Talairach | Briley et al. 2013 (EEG BESA source) | Pitch chroma source (left) |
| 5 | **Medial HG (R) — primary** | 44, -13, 13 | Talairach | Briley et al. 2013 (pure-tone source) | Primary AC — tonotopic, not pitch salience |
| 6 | **Medial HG (L) — primary** | -42, -19, 16 | Talairach | Briley et al. 2013 (pure-tone source) | Primary AC — tonotopic processing |
| 7 | **Inferior Colliculus** | 0, -32, -8 | MNI (approx) | Cousineau 2015; Bidelman 2013 | FFR generation — NPS computation (temporal code) |
| 8 | **Auditory Nerve** | Peripheral | — | Bidelman & Heinz 2011 | Phase-locked harmonic response — AN pitch salience |
| 9 | **Human HG** | Intracranial | — | Fishman et al. 2001 (2 patients) | Phase-locked activity for dissonance (beating) |
| 10 | **R STG (anterior gradient)** | y-axis significant | ECoG | Foo et al. 2016 (χ²=8.6, p=.003) | Dissonant-sensitive sites anterior in STG |
| 11 | **Anterolateral HG** | MEG source | — | Tabas et al. 2019 (POR source) | Pitch onset response — consonance/dissonance latency |

```
KEY ANATOMICAL INSIGHT (Penagos et al. 2004):
  Anterolateral Heschl's gyrus (nonprimary auditory cortex) encodes
  PERCEPTUAL pitch salience — not physical temporal regularity.
  Subcortical stations (CN, IC) show NO sensitivity to pitch salience.
  This means SDNPS's stimulus-dependency effect operates at the
  cortical level, not the brainstem level as previously assumed.

  Processing hierarchy:
    AN → IC → medial HG (tonotopic) → anterolateral HG (pitch salience)
    ↑ temporal code ↑               ↑ pitch salience emerges here ↑

Code file (sdnps.py) currently lists:
  IC (0,-32,-8) and AN (0,-38,-40)
Should add anterolateral HG from Penagos 2004 in Phase 5.
```

---

## 9. Cross-Unit Pathways

### 9.1 SDNPS ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SDNPS INTERACTIONS                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (SPU):                                                         │
│  BCH.f01_nps ─────────────► SDNPS challenges BCH's universality claim     │
│  SDNPS.f02_stim_dep ─────► BCH NPS validity is stimulus-dependent         │
│  SDNPS.f01_nps_value ────► PSCL (when brainstem NPS fails, cortex takes   │
│                              over — PSCL compensates for natural sounds)    │
│  SDED.early_detection ───► SDNPS.roughness_interference (shared pathway)  │
│  SDNPS.roughness_corr ──► STAI (roughness invariance informs aesthetics)  │
│                                                                             │
│  CROSS-UNIT (P1: SPU → ARU):                                              │
│  SDNPS.behavioral_cons_pred ► ARU.SRP (gated consonance → pleasure)       │
│    Note: ARU should weight BCH higher when SDNPS.f02 indicates natural    │
│                                                                             │
│  KEY RELATIONSHIP — BCH vs SDNPS:                                          │
│  BCH claims:  NPS ↔ consonance r=0.81 (universal)                         │
│  SDNPS shows: NPS ↔ consonance r=0.34 (synthetic only)                   │
│               NPS ↔ consonance r≈0.0  (natural sounds)                    │
│  Resolution:  BCH is correct for the NEURAL level                          │
│               SDNPS adds the BEHAVIORAL generalization constraint           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Natural sounds** | NPS should NOT predict pleasantness for natural timbres | Supported (r=0.24 sax, r=-0.10 voice — both n.s.) |
| **Synthetic tones** | NPS SHOULD predict pleasantness for synthetic tones | Supported (r=0.34, p<0.03) |
| **Roughness invariance** | NPS ↔ roughness should hold across ALL stimulus types | Supported (r=-0.57, p<1e-05 across all) |
| **Spectral simplification** | Reducing natural sound complexity should restore NPS predictive power | Testable |
| **Cross-cultural** | Stimulus-dependency should be universal (not cultural) | Testable |
| **Hearing impairment** | Cochlear damage should disproportionately affect synthetic > natural NPS | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class SDNPS(BaseModel):
    """Stimulus-Dependent Neural Pitch Salience.

    Output: 10D per frame.
    Reads: PPC mechanism (30D), R³ direct.
    """
    NAME = "SDNPS"
    UNIT = "SPU"
    TIER = "γ1"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("PPC",)        # Primary mechanism

    # Empirical coefficients from Cousineau et al. 2015
    NPS_SYNTH_R = 0.34    # NPS ↔ pleasantness for synthetic
    NPS_SAX_R = 0.24      # NPS ↔ pleasantness for sax (n.s.)
    NPS_VOICE_R = -0.10   # NPS ↔ pleasantness for voice (n.s.)
    NPS_ROUGH_R = -0.57   # NPS ↔ roughness (invariant)

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """10 tuples for SDNPS computation."""
        return [
            # (r3_idx, horizon, morph, law)
            (0, 0, 0, 2),     # roughness, 25ms, value, bidirectional
            (0, 3, 1, 2),     # roughness, 100ms, mean, bidirectional
            (0, 6, 14, 0),    # roughness, 200ms, periodicity, forward
            (2, 0, 0, 2),     # helmholtz_kang, 25ms, value, bidirectional
            (5, 0, 0, 2),     # inharmonicity, 25ms, value, bidirectional
            (5, 3, 1, 2),     # inharmonicity, 100ms, mean, bidirectional
            (14, 0, 0, 2),    # tonalness, 25ms, value, bidirectional
            (14, 3, 1, 0),    # tonalness, 100ms, mean, forward
            (17, 3, 14, 2),   # spectral_autocorr, 100ms, periodicity, bidi
            (18, 0, 0, 2),    # tristimulus1, 25ms, value, bidirectional
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute SDNPS 10D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) SDNPS output
        """
        ppc = mechanism_outputs["PPC"]    # (B, T, 30)

        # R³ features
        roughness = r3[..., 0:1]
        sethares = r3[..., 1:2]
        inharmonicity = r3[..., 5:6]
        tonalness = r3[..., 14:15]
        autocorr = r3[..., 17:18]
        trist1 = r3[..., 18:19]
        trist2 = r3[..., 19:20]
        trist3 = r3[..., 20:21]

        # PPC sub-sections
        ppc_pitch = ppc[..., 0:10]       # pitch salience
        ppc_cons = ppc[..., 10:20]       # consonance encoding

        # Derived quantities
        trist_balance = 1.0 - torch.std(
            torch.cat([trist1, trist2, trist3], dim=-1),
            dim=-1, keepdim=True
        )
        spectral_complexity = (
            inharmonicity * (1 - tonalness) * (1 - trist_balance)
        )

        # H³ temporal features
        roughness_mean = h3_direct[(0, 3, 1, 2)].unsqueeze(-1)
        roughness_periodicity = h3_direct[(0, 6, 14, 0)].unsqueeze(-1)
        tonalness_mean_fwd = h3_direct[(14, 3, 1, 0)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features (3D) ═══
        # f01: NPS Value — coefficient sum: 0.40 + 0.30 + 0.30 = 1.0
        f01 = torch.sigmoid(
            0.40 * tonalness * autocorr
                 * ppc_pitch.mean(-1, keepdim=True)
            + 0.30 * (1.0 - inharmonicity)
                   * ppc_cons.mean(-1, keepdim=True)
            + 0.30 * trist_balance
        )

        # f02: Stimulus Dependency — coefficient sum: 0.50 + 0.50 = 1.0
        f02 = torch.sigmoid(
            0.50 * (1.0 - spectral_complexity) * f01
            + 0.50 * roughness_periodicity
        )

        # f03: Roughness Correlation — empirical r=-0.57
        f03 = self.NPS_ROUGH_R * roughness_mean   # range: [-0.57, 0]

        # ═══ LAYER M: Mathematical (1D) ═══
        nps_stimulus_function = f01 * f02

        # ═══ LAYER P: Present (3D) ═══
        ffr_encoding = ppc_pitch.mean(-1, keepdim=True)
        harmonicity_proxy = (
            (1.0 - inharmonicity) * trist_balance
            * ppc_cons.mean(-1, keepdim=True)
        )
        roughness_interference = 1.0 - (roughness + sethares) / 2

        # ═══ LAYER F: Future (3D) ═══
        # behavioral_consonance_pred — coefficient sum: 0.60 + 0.40 = 1.0
        behavioral_consonance_pred = torch.sigmoid(
            0.60 * nps_stimulus_function
            + 0.40 * harmonicity_proxy
        )

        # roughness_response_pred — coefficient sum: 0.57 + 0.43 = 1.0
        roughness_response_pred = torch.sigmoid(
            0.57 * roughness_interference
            + 0.43 * ffr_encoding
        )

        # generalization_limit — coefficient sum: 0.50 + 0.50 = 1.0
        generalization_limit = torch.sigmoid(
            0.50 * f02
            + 0.50 * tonalness_mean_fwd
        )

        return torch.cat([
            f01, f02, f03,                                     # E: 3D
            nps_stimulus_function,                             # M: 1D
            ffr_encoding, harmonicity_proxy,
                roughness_interference,                        # P: 3D
            behavioral_consonance_pred,
                roughness_response_pred,
                generalization_limit,                          # F: 3D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | **12** (v2.1.0, was 1 in v2.0.0) | 2 FFR + 1 fMRI + 3 EEG + 1 ECoG + 1 MEG + 1 intracranial + 1 psychophysics + 1 AN model + 1 review |
| **Effect Sizes** | r=0.34→-0.10 degradation; r=-0.57 roughness (invariant) | Cousineau 2015 (PLoS ONE, CORRECTED) |
| **Cortical Locus** | Anterolateral HG: Talairach R:48,-11,3 / L:-55,-5,3 | Penagos 2004 — pitch salience center |
| **Evidence Modality** | **8 methods**: FFR, fMRI, EEG, intracranial, ECoG, MEG, modeling, CI | Multi-method convergence on cortical pitch salience |
| **Falsification Tests** | 3/6 supported | Moderate validity |
| **R³ Features Used** | ~16D of 49D | Focused |
| **H³ Demand** | 10 tuples (0.43%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Pitch salience primary |
| **Output Dimensions** | **10D** | 4-layer structure |

```
v2.1.0 CHANGES:
  • ⚠ CITATION CORRECTED: Cousineau reference was WRONG paper
    Old: Cousineau, McDermott & Peretz (2015), PNAS 109(48) [actually 2012, amusia]
    New: Cousineau, Bidelman, Peretz & Lehmann (2015), PLoS ONE 10(12), e0145439
  • Evidence table expanded: 1 → 12 papers
  • KEY INSIGHT updated with convergent evidence across 8 methods
  • CRITICAL EVIDENCE expanded to 6 core findings
  • Major addition: Penagos 2004 — anterolateral HG pitch salience center
  • Brain regions: 3 → 11 entries with Talairach coordinates from Penagos/Briley
  • Qualification: Penagos N=6, Cousineau N=14 — both unreplicated
  • Code discrepancy: sdnps.py brain regions missing anterolateral HG
```

---

## 13. Scientific References

1. **Cousineau, M., Bidelman, G. M., Peretz, I., & Lehmann, A. (2015)**. On the relevance of natural stimuli for the study of brainstem correlates: The example of consonance perception. *PLoS ONE*, 10(12), e0145439. ⚠ *CORRECTED in v2.1.0 — previously cited as Cousineau, McDermott & Peretz, PNAS 109(48), which is a different paper about congenital amusia (2012).*
2. **Penagos, H., Melcher, J. R., & Oxenham, A. J. (2004)**. A neural representation of pitch salience in nonprimary human auditory cortex revealed with functional magnetic resonance imaging. *Journal of Neuroscience*, 24(30), 6810-6815.
3. **Briley, P. M., Breakey, C., & Krumbholz, K. (2013)**. Evidence for pitch chroma mapping in human auditory cortex. *Cerebral Cortex*, 23(11), 2601-2610.
4. **Bidelman, G. M., & Heinz, M. G. (2011)**. Auditory-nerve responses predict pitch attributes related to musical consonance-dissonance for normal and impaired hearing. *Journal of the Acoustical Society of America*, 130(3), 1488-1502.
5. **Bidelman, G. M. (2013)**. The role of the auditory brainstem in processing musically relevant pitch. *Frontiers in Psychology*, 4, 264.
6. **Fishman, Y. I., Volkov, I. O., Noh, M. D., Garell, P. C., Bakken, H., Arezzo, J. C., Howard, M. A., & Steinschneider, M. (2001)**. Consonance and dissonance of musical chords: Neural correlates in auditory cortex of monkeys and humans. *Journal of Neurophysiology*, 86, 2761-2788.
7. **Foo, F., King-Stephens, D., Weber, P., Laxer, K., Parvizi, J., & Knight, R. T. (2016)**. Differential processing of consonance and dissonance within the human superior temporal gyrus. *Frontiers in Human Neuroscience*, 10, 154.
8. **Tabas, A., Andermann, M., Schuberth, V., Riedel, H., Balaguer-Ballester, E., & Rupp, A. (2019)**. Modeling and MEG evidence of early consonance processing in auditory cortex. *PLoS Computational Biology*, 15(2), e1006820.
9. **Basinski, K., Celma-Miralles, A., Quiroga-Martinez, D. R., & Vuust, P. (2025)**. Inharmonicity enhances brain signals of attentional capture and auditory stream segregation. *Communications Biology*, 8, 1584.
10. **de Groote, E., Macherey, O., Deeks, J. M., Roman, S., & Carlyon, R. P. (2025)**. Temporal pitch perception of multi-channel stimuli by cochlear-implant users. *Journal of the Association for Research in Otolaryngology*.
11. **Schon, D., Regnault, P., Ystad, S., & Besson, M. (2005)**. Sensory consonance: An ERP study. *Music Perception*, 23(2), 105-118.
12. **Crespo-Bojorque, P., Monte-Ordono, J., & Toro, J. M. (2018)**. Early neural responses underlie advantages for consonance over dissonance. *Neuropsychologia*, 117, 188-198.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Output dims | 11D | 10D (removed 1 redundant math output) |
| Temporal | HC⁰ mechanisms (OSC, NPL, HRM, BND) | PPC mechanism (30D) |
| Roughness signal | S⁰.roughness[30] + HC⁰.OSC | R³.roughness[0] + PPC.pitch_salience |
| Harmonicity | S⁰.helmholtz_kang[32] + HC⁰.HRM | R³.helmholtz_kang[2] + PPC.consonance_encoding |
| NPS | S⁰.tonalness × HC⁰.NPL | R³.tonalness[14] × PPC.pitch_salience |
| Spectral complexity | S⁰ multi-index manual | R³.inharmonicity × tonalness × trist_balance |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 27/2304 = 1.17% | 10/2304 = 0.43% |

### Why PPC replaces HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (OSC, NPL, HRM, BND). In MI, these are unified into the PPC mechanism with 3 sub-sections:
- **OSC + NPL → PPC.pitch_salience** [0:10]: Phase-locking + FFR = pitch encoding
- **HRM → PPC.consonance_encoding** [10:20]: Harmonic template = harmonicity
- **BND (partial) → PPC.chroma_processing** [20:30]: Band-level integration

### Why 11D → 10D

The legacy v1.0.0 had an 11th output (`f05_nps_roughness_product`) that was a mathematical redundancy — it was simply `f01 * f03` which can be computed from the existing outputs. Removing it reduces storage without information loss.

---

**Model Status**: SPECULATIVE
**Output Dimensions**: **10D**
**Evidence Tier**: **γ (Speculative)**
**Confidence**: **<70%**
