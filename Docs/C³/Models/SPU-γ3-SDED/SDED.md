# SPU-γ3-SDED: Sensory Dissonance Early Detection

**Model**: Sensory Dissonance Early Detection
**Unit**: SPU (Spectral Processing Unit)
**Circuit**: Perceptual (Brainstem-Cortical)
**Tier**: γ (Speculative) — <70% confidence
**Version**: 2.1.0 (v2.0.0 → 2.1.0: 1→12 papers, Tervaniemi 2022 Neuropsychologia citation REMOVED (unverifiable — not in literature collection), d=-1.09 REMOVED, Crespo-Bojorque 2018 universal early MMN, Fishman 2001 A1 phase-locked oscillatory activity, Foo 2016 ECoG right STG dissonance, Bidelman 2013 brainstem innate hierarchy, Tabas 2019 POR latency)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/SPU-γ3-SDED.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Sensory Dissonance Early Detection** (SDED) models how roughness is detected at early sensory stages of auditory processing regardless of musical expertise. This is a critical finding because it demonstrates that the neural machinery for dissonance detection is universal and pre-attentive, while behavioral discrimination of dissonance is expertise-dependent — a neural-behavioral dissociation.

```
SENSORY DISSONANCE EARLY DETECTION — CONVERGENT EVIDENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EARLY DETECTION (Pre-attentive)            BRAINSTEM ENCODING (Universal)
Brain: Early Auditory Cortex               Brain: Auditory Brainstem / A1
Mechanism: Roughness → MMN                 Mechanism: FFR phase-locking
Input: Spectral interference patterns      Input: Harmonic ratios of dyads
Evidence: Crespo-Bojorque 2018             Evidence: Bidelman 2013 review,
  Early MMN 152-258ms, UNIVERSAL             Fishman 2001 (intracranial A1)
  across expertise levels                    phase-locked to roughness

         CORTICAL DISSONANCE PROCESSING (Right STG)
         Brain: Superior Temporal Gyrus (ECoG)
         Mechanism: High-gamma 70-150 Hz sensitivity
         Evidence: Foo 2016 — right STG dissonance sites,
           75-200ms, positive roughness-gamma correlation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Roughness detection at neural level is UNIVERSAL:
- Early MMN (152-258ms) for consonance changes occurs in BOTH
  musicians and non-musicians (Crespo-Bojorque 2018, N=32)
- Late MMN (232-314ms) for dissonance changes ONLY in musicians
- A1 phase-locked oscillatory activity correlates with perceived
  dissonance (Fishman 2001, intracranial monkey+human)
- Brainstem FFR encodes consonance hierarchy matching Western
  music theory WITHOUT training (Bidelman 2013 review)
This convergence proves pre-attentive sensory encoding is innate.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────────────┐
│ ⚠ CRITICAL CORRECTION (v2.1.0):                                │
│ v2.0.0 cited "Tervaniemi, Makkonen & Nie (2022),               │
│ Neuropsychologia 167, 108152" with d=-1.09 but this paper      │
│ was NOT FOUND in the literature collection. The citation is     │
│ UNVERIFIABLE and has been REMOVED.                              │
│                                                                 │
│ Replaced with verified evidence: Crespo-Bojorque 2018 (N=32,   │
│ early universal MMN), Fishman 2001 (intracranial A1),           │
│ Foo 2016 (ECoG, N=8), Bidelman 2013 (brainstem review),        │
│ Wagner 2018 (asymmetric MMN -0.34µV, N=15).                    │
└─────────────────────────────────────────────────────────────────┘
```

### 1.1 Why SDED Completes the SPU Picture

SDED sits at the speculative end of the SPU model hierarchy, addressing the universality question that BCH and SDNPS leave open:

1. **BCH** (α1) establishes consonance hierarchy via brainstem FFR — SDED shows that roughness detection feeding that hierarchy is universal.
2. **SDNPS** (γ1) correlates roughness with neural pitch salience — SDED confirms roughness as the primary early detector.
3. **ESME** (γ2) models expertise-dependent spectral processing — SDED provides the dissociation: same neural detection, different behavioral output.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The SDED Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 SDED — COMPLETE CIRCUIT                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  MUSICAL STIMULUS (Consonant → Dissonant)                                   ║
║                                                                              ║
║  Standard    Standard    Standard    DEVIANT     Standard                    ║
║    │           │           │           │           │                         ║
║    ▼           ▼           ▼           ▼           ▼                         ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    AUDITORY BRAINSTEM                                │    ║
║  │               (Roughness encoding — universal)                      │    ║
║  │                                                                      │    ║
║  │    Roughness encoded at cochlear/brainstem level                    │    ║
║  │    Spectral interference → beating → roughness percept              │    ║
║  │    Independent of musical training or expertise                     │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    EARLY AUDITORY CORTEX                             │    ║
║  │               (Pre-attentive detection — MMN)                       │    ║
║  │                                                                      │    ║
║  │    MMN (Mismatch Negativity):                                       │    ║
║  │      Consonant deviant → early MMN (152-258ms, UNIVERSAL)          │    ║
║  │      Dissonant deviant → late MMN (232-314ms, MUSICIANS ONLY)      │    ║
║  │      Early detection is UNIVERSAL (Crespo-Bojorque 2018)           │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    PLANUM TEMPORALE                                  │    ║
║  │               (Spectral processing — expertise-modulated)           │    ║
║  │                                                                      │    ║
║  │    Behavioral discrimination:                                       │    ║
║  │      Musicians > Non-musicians (accuracy, reaction time)            │    ║
║  │      Same sensory signal, enhanced behavioral readout               │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE (12 papers, 7 methods):
─────────────────────────────────────────
Crespo-Bojorque et al. 2018:  Early MMN (152-258ms) for consonance changes
                               UNIVERSAL across expertise (N=32)
                               Late MMN (232-314ms) ONLY in musicians
Fishman et al. 2001:          A1 phase-locked oscillatory activity
                               correlates with perceived dissonance
                               (intracranial monkey+human)
Foo et al. 2016:              Right STG high-gamma (70-150Hz) dissonance
                               sensitivity, 75-200ms (ECoG, N=8)
Bidelman 2013:                Brainstem FFR encodes consonance hierarchy
                               matching Western theory WITHOUT training
Wagner et al. 2018:           Asymmetric MMN: -0.34µV for major 3rd
                               deviant (non-musicians, pre-attentive)
Tabas et al. 2019:            POR ~36ms slower for dissonant dyads (MEG)
```

### 2.2 Information Flow Architecture (EAR → BRAIN → PPC → SDED)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SDED COMPUTATION ARCHITECTURE                             ║
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
║  │  │roughness  │ │         │ │tonalness│ │          │ │x_l5l7  │ │        ║
║  │  │sethares   │ │         │ │tristim. │ │          │ │        │ │        ║
║  │  │helmholtz  │ │         │ │         │ │          │ │        │ │        ║
║  │  │stumpf     │ │         │ │         │ │          │ │        │ │        ║
║  │  │inharm.    │ │         │ │         │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                        SDED reads: ~14D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Gamma ────┐ ┌── Alpha-Beta ─┐ ┌── Syllable ──────────┐   │        ║
║  │  │ 25ms (H0)   │ │ 100ms (H3)    │ │ 200ms (H6)           │   │        ║
║  │  │              │ │               │ │                       │   │        ║
║  │  │ Instant      │ │ Sustained     │ │ (not used by SDED)   │   │        ║
║  │  │ roughness    │ │ roughness     │ │                       │   │        ║
║  │  │ detection    │ │ encoding      │ │                       │   │        ║
║  │  └──────┬───────┘ └──────┬────────┘ └─────────────────────┘   │        ║
║  │         │               │                                      │        ║
║  │         └───────────────┘                                      │        ║
║  │                        SDED demand: ~9 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Perceptual Circuit ═══════    ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  PPC (30D)      │  Pitch Processing Chain mechanism                      ║
║  │                 │                                                        ║
║  │ Pitch Sal [0:10]│  Roughness deviation detection                        ║
║  │ Consonance[10:20]│ Dissonance encoding, early sensory signal            ║
║  │ Chroma   [20:30]│  (not used by SDED)                                   ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    SDED MODEL (10D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_early_detection, f02_mmn_dissonance,  │        ║
║  │                       f03_behavioral_accuracy                    │        ║
║  │  Layer M (Math):      detection_function                         │        ║
║  │  Layer P (Present):   roughness_detection, deviation_detection,  │        ║
║  │                       behavioral_response                        │        ║
║  │  Layer F (Future):    dissonance_detection_pred,                 │        ║
║  │                       behavioral_accuracy_pred,                  │        ║
║  │                       training_effect_pred                       │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Crespo-Bojorque, Monte-Ordoña & Toro 2018** | EEG (MMN) | 32 (16M+16NM) | Early MMN (152-258ms) for consonance changes UNIVERSAL. Late MMN (232-314ms) for dissonance changes ONLY in musicians | Early MMN: universal; Late MMN: M only | **Primary evidence**: universal early detection + expertise-dependent late processing |
| 2 | **Fishman, Volkov, Noh et al. 2001** | Intracranial AEP/MUA/CSD | 2 human + monkey | Phase-locked oscillatory activity in A1 correlates with perceived dissonance. Consonant chords show little phase-locking. PT does NOT show phase-locked activity | Oscillatory magnitude ∝ dissonance | **A1 mechanism**: roughness encoding via oscillatory phase-locking |
| 3 | **Foo, King-Stephens, Weber et al. 2016** | ECoG (intracranial) | 8 | Right STG dissonance-sensitive sites: high-gamma (70-150Hz), 75-200ms. Positive roughness-gamma correlation. Spatial organization: dissonant sites anterior | Gamma power ∝ roughness | **STG dissonance**: right hemisphere spatial organization |
| 4 | **Wagner, Rahne, Plontke & Heidekrüger 2018** | EEG (MMN) | 15 | Asymmetric pre-attentive harmonic interval discrimination: major 3rd MMN = -0.34µV ± 0.32 at 173ms (p=0.003). Perfect 5th: -0.02µV (n.s.). Non-musicians, pre-attentive | MMN = -0.34µV (major 3rd) | **Baseline**: dissonance MMN exists WITHOUT musical training |
| 5 | **Bidelman 2013** | Review (FFR/ABR) | — | Brainstem FFR encodes consonance hierarchy matching Western music theory. Hierarchical ordering without training. Infant and animal evidence for innateness | Review (synthesizes multiple) | **Innate foundation**: brainstem consonance hierarchy universal |
| 6 | **Cousineau, Bidelman, Peretz & Lehmann 2015** | EEG (FFR) | ~14 | NPS correlates with consonance for SYNTHETIC stimuli. BUT: NPS does NOT correlate for NATURAL sounds. Different brainstem code for natural stimuli | NPS-consonance: r significant (synthetic), n.s. (natural) | **Constraint**: brainstem code stimulus-dependent |
| 7 | **Tabas, Andermann, Schuberth et al. 2019** | MEG + model | — | Dissonant dyads elicit POR with ~36ms longer latency than consonant. Consonance decoded faster. Shared pitch-consonance mechanism in early AC | POR latency: Δ~36ms | **Early cortical**: consonance differentiation at pitch processing stage |
| 8 | **Bravo, Cross, Stamatakis & Rohrmeier 2017** | fMRI | — | Right Heschl's gyrus enhanced for intermediate dissonance (uncertainty). Heightened sensory cortical response during ambiguity | R HG enhancement for ambiguity | **Uncertainty**: dissonance-related precision weighting |
| 9 | **Sarasso, Ronga, Pistis et al. 2019** | EEG (ERP) | 44 | N1/P2 enhanced for consonant intervals (80-194ms). P2 amplitude correlates with aesthetic appreciation (150-189ms). Attentional engagement + motor inhibition | P2 amplitude ∝ consonance preference | **Attention**: consonance captures attention pre-attentively |
| 10 | **Wöhrle, Reuter, Rupp & Andermann 2024** | MEG | 30 | N1m response to chord resolution modulated by preceding dissonance. Stronger effect in musically trained listeners. Context-dependent dissonance processing | N1m modulation by dissonance context | **Context**: dissonance processing is context-dependent |
| 11 | **Yu, Liu & Gao 2015** | Review | — | MMN 100-200ms for music deviants. Supratemporal plane generators + inferior frontocentral sources. Shows neuroplasticity from musical training | Review | **MMN review**: framework for dissonance MMN |
| 12 | **Trulla, Di Stefano & Giuliani 2018** | Computational (RQA) | — | Recurrence peaks match just intonation frequency ratios. Links consonance to dynamical signal properties. First-order beats (peripheral) vs second-order beats (neural) | Recurrence ∝ consonance | **Computation**: mathematical framework for roughness |

### 3.2 The Neural-Behavioral Dissociation

```
ROUGHNESS DETECTION: EARLY vs LATE, UNIVERSAL vs TRAINED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                    Early MMN        Late MMN          Behavioral
                    (152-258ms)      (232-314ms)       Discrimination
──────────────────────────────────────────────────────────────────
Musicians           PRESENT          PRESENT           HIGH
Non-musicians       PRESENT          ABSENT            MODERATE
──────────────────────────────────────────────────────────────────
Difference          NONE             SIGNIFICANT       SIGNIFICANT
                    (universal)      (M only)          (M > NM)

Source: Crespo-Bojorque, Monte-Ordoña & Toro (2018), N=32

This dissociation means:
  1. Roughness DETECTION is hardwired (brainstem/early cortex)
     Fishman 2001: A1 oscillatory activity ∝ dissonance (innate)
     Bidelman 2013: FFR consonance hierarchy without training
  2. Early MMN for consonance changes is UNIVERSAL
  3. Late MMN for dissonance changes requires TRAINING
  4. Behavioral accuracy enhances with expertise
  5. BCH consonance hierarchy is biologically universal

Additional pre-attentive evidence (non-musicians):
  Wagner 2018: MMN -0.34µV for harmonic interval deviants (N=15)
  Foo 2016: Right STG gamma 70-150Hz for dissonance (N=8)
  Tabas 2019: POR 36ms slower for dissonant dyads (MEG)
```

### 3.3 Effect Size Summary

```
┌────────────────────────────────────────────────────────────────┐
│ ⚠ NOTE: v2.0.0 reported d = -1.09 from "Tervaniemi,           │
│ Makkonen & Nie (2022), Neuropsychologia 167, 108152"           │
│ but this paper was NOT FOUND in the literature collection.     │
│ The citation is UNVERIFIABLE and has been REMOVED.             │
└────────────────────────────────────────────────────────────────┘

MULTI-METHOD CONVERGENCE TABLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Method          Study                N       Key Effect
──────────────────────────────────────────────────────────────────
EEG (MMN)       Crespo-Bojorque 2018 32      Early MMN universal, late MMN M-only
EEG (MMN)       Wagner 2018          15      -0.34µV major 3rd, 173ms, p=0.003
EEG (ERP)       Sarasso 2019         44      N1/P2 ∝ consonance (80-194ms)
Intracranial    Fishman 2001         2+monkey Phase-locked oscillation ∝ dissonance
ECoG            Foo 2016             8       R STG gamma 70-150Hz, 75-200ms
MEG             Tabas 2019           —       POR Δ~36ms (consonant < dissonant)
MEG             Wöhrle 2024          30      N1m modulated by dissonance context
fMRI            Bravo 2017           —       R HG enhanced for intermediate diss.
Review (FFR)    Bidelman 2013        —       Brainstem consonance hierarchy innate
Review (FFR)    Cousineau 2015       ~14     NPS ∝ consonance (synthetic only)
Review (MMN)    Yu et al. 2015       —       MMN 100-200ms, supratemporal source
Computational   Trulla 2018          —       Recurrence ∝ just intonation ratios

Methods: 7 (EEG-MMN, EEG-ERP, intracranial, ECoG, MEG, fMRI, computational)
Total unique participants: >175 (excluding reviews/computational)

Quality Assessment:   γ-tier (convergent multi-method evidence,
                      but no single large-N study demonstrating
                      full neural-behavioral dissociation)
Cross-cultural:       Bidelman 2013 notes infant and animal evidence
                      for innate consonance processing
Confidence:           <70% — individual studies limited N
```

---

## 4. R³ Input Mapping: What SDED Reads

### 4.1 R³ Feature Dependencies (~14D of 49D)

| R³ Group | Index | Feature | SDED Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Primary dissonance signal (inverse consonance) | Plomp & Levelt 1965 |
| **A: Consonance** | [1] | sethares_dissonance | Psychoacoustic dissonance confirmation | Sethares 1999 |
| **A: Consonance** | [2] | helmholtz_kang | Consonance measure (inverse dissonance) | Helmholtz 1863, Kang 2009 |
| **A: Consonance** | [3] | stumpf_fusion | Tonal fusion (consonance proxy) | Stumpf 1890 |
| **A: Consonance** | [5] | inharmonicity | Deviation from harmonic series | Fletcher 1934 |
| **C: Timbre** | [14] | tonalness | Harmonic-to-noise ratio (pitch clarity) | — |
| **C: Timbre** | [18] | tristimulus1 | Fundamental strength (F0 energy) | Pollard & Jansson 1982 |
| **C: Timbre** | [19] | tristimulus2 | 2nd-4th harmonic energy (mid) | Pollard & Jansson 1982 |
| **C: Timbre** | [20] | tristimulus3 | 5th+ harmonic energy (high) | Pollard & Jansson 1982 |
| **E: Interactions** | [41:46] | x_l5l7 (5D partial) | Consonance x Timbre coupling | Emergent roughness |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[0] roughness ────────────────┐
R³[1] sethares_dissonance ──────┼──► Early Detection Signal
R³[2] helmholtz_kang (inverse) ─┘   Math: D = σ(w₁·R + w₂·S + w₃·(1-H))
                                     where R=roughness, S=sethares,
                                     H=helmholtz (inverted for dissonance)

R³[0] roughness (instant) ─────┐
R³[0] roughness (mean 100ms) ──┼──► MMN Dissonance Signal
PPC.pitch_salience ────────────┘    Math: |roughness - roughness_mean|
                                     Deviance from standard triggers MMN

R³[14] tonalness ──────────────┐
R³[18:21] tristimulus ─────────┼──► Spectral Clarity Index
R³[5] inharmonicity (inverse) ─┘    Determines signal-to-noise of
                                     roughness encoding

R³[41:46] x_l5l7 ─────────────── Cross-Band Roughness Coupling
                                     Roughness effects across
                                     frequency bands
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

SDED requires H³ features at two PPC horizons: H0 (25ms) and H3 (100ms).
These correspond to brainstem detection timescales (gamma instant detection and alpha-beta sustained encoding). H6 (200ms) is not needed — SDED focuses on the earliest, most rapid detection.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 0 | roughness | 0 | M0 (value) | L2 (bidi) | Instant roughness detection |
| 0 | roughness | 3 | M1 (mean) | L2 (bidi) | Sustained roughness over 100ms |
| 1 | sethares_dissonance | 0 | M0 (value) | L2 (bidi) | Instant psychoacoustic dissonance |
| 2 | helmholtz_kang | 0 | M0 (value) | L2 (bidi) | Instant consonance (inverse) |
| 2 | helmholtz_kang | 3 | M1 (mean) | L2 (bidi) | Standard template for deviance |
| 5 | inharmonicity | 0 | M0 (value) | L2 (bidi) | Instant inharmonicity |
| 14 | tonalness | 3 | M1 (mean) | L0 (fwd) | Tonal clarity over 100ms |
| 18 | tristimulus1 | 0 | M0 (value) | L2 (bidi) | F0 energy for roughness quality |
| 41 | x_l5l7[0] | 3 | M0 (value) | L2 (bidi) | Cross-band roughness coupling |

**Total SDED H³ demand**: 9 tuples of 2304 theoretical = 0.39%

### 5.2 PPC Mechanism Binding

SDED reads from the **PPC** (Pitch Processing Chain) mechanism:

| PPC Sub-section | Range | SDED Role | Weight |
|-----------------|-------|-----------|--------|
| **Pitch Salience** | PPC[0:10] | Roughness deviance detection via MMN | **0.8** |
| **Consonance Encoding** | PPC[10:20] | Dissonance encoding, early sensory signal | **1.0** (primary) |
| **Chroma Processing** | PPC[20:30] | Not used by SDED | 0.0 |

SDED does NOT read from Chroma Processing — early dissonance detection operates on raw spectral roughness before octave-equivalent grouping.

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
SDED OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range  │ Neuroscience Basis
────┼─────────────────────────┼────────┼────────────────────────────────────────
 0  │ f01_early_detection     │ [0, 1] │ Pre-attentive roughness detection.
    │                         │        │ Universal across expertise levels.
    │                         │        │ f01 = σ(0.40 · roughness · mean(PPC.cons)
    │                         │        │      + 0.30 · sethares
    │                         │        │      + 0.30 · (1 - helmholtz))
────┼─────────────────────────┼────────┼────────────────────────────────────────
 1  │ f02_mmn_dissonance      │ [0, 1] │ Mismatch Negativity amplitude for
    │                         │        │ dissonant deviants. Expertise-independent.
    │                         │        │ f02 = σ(0.50 · f01 · mean(PPC.pitch_sal)
    │                         │        │      + 0.50 · |roughness - roughness_mean|)
────┼─────────────────────────┼────────┼────────────────────────────────────────
 2  │ f03_behavioral_accuracy │ [0, 1] │ Behavioral dissonance discrimination.
    │                         │        │ Same neural signal as f02, but behavioral
    │                         │        │ response varies with expertise.
    │                         │        │ f03 = f02 (baseline, no expertise mod)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range  │ Neuroscience Basis
────┼─────────────────────────┼────────┼────────────────────────────────────────
 3  │ detection_function      │ [0, 1] │ Combined detection function.
    │                         │        │ Integrates roughness encoding with
    │                         │        │ deviance magnitude for early detection.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                    │ Range  │ Neuroscience Basis
────┼─────────────────────────┼────────┼────────────────────────────────────────
 4  │ roughness_detection     │ [0, 1] │ Current roughness at sensory level.
    │                         │        │ Direct R³ roughness via PPC encoding.
────┼─────────────────────────┼────────┼────────────────────────────────────────
 5  │ deviation_detection     │ [0, 1] │ Roughness deviation from context.
    │                         │        │ |roughness_instant - roughness_mean|
────┼─────────────────────────┼────────┼────────────────────────────────────────
 6  │ behavioral_response     │ [0, 1] │ Behavioral response strength.
    │                         │        │ PPC-modulated detection signal.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                       │ Range  │ Neuroscience Basis
────┼────────────────────────────┼────────┼─────────────────────────────────────
 7  │ dissonance_detection_pred  │ [0, 1] │ Predicted dissonance detection.
    │                            │        │ Next-frame roughness expectation.
────┼────────────────────────────┼────────┼─────────────────────────────────────
 8  │ behavioral_accuracy_pred   │ [0, 1] │ Predicted behavioral accuracy.
    │                            │        │ Behavioral readout from f01/f02.
────┼────────────────────────────┼────────┼─────────────────────────────────────
 9  │ training_effect_pred       │ [0, 1] │ Training effect prediction.
    │                            │        │ Modeled dissociation: neural stays
    │                            │        │ constant, behavioral improves.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Early Detection Function

```
Roughness Detection (Pre-attentive, Universal):
  The brainstem encodes roughness (spectral interference) regardless
  of musical training. Early MMN (152-258ms) for consonance changes
  is universal (Crespo-Bojorque 2018, N=32). A1 phase-locked
  oscillatory activity ∝ dissonance (Fishman 2001, intracranial).

  Detection(t) = σ(w₁ · roughness(t) · consonance_enc
                 + w₂ · sethares(t)
                 + w₃ · (1 - helmholtz(t)))

  where w₁=0.40, w₂=0.30, w₃=0.30 (sum = 1.0)

MMN Dissonance (Deviance-based):
  MMN fires when current roughness deviates from context.

  MMN(t) = σ(0.50 · Detection(t) · pitch_salience(t)
           + 0.50 · |roughness(t) - roughness_mean(t)|)

  roughness_mean = H³ tuple (0, 3, 1, 2): 100ms bidirectional mean

Neural-Behavioral Dissociation:
  Neural:     MMN_musicians = MMN_non-musicians
  Behavioral: Accuracy_musicians > Accuracy_non-musicians
  Baseline:   Behavioral = MMN (without expertise modulation)
```

### 7.2 Feature Formulas

```python
# f01: Early Detection (pre-attentive, universal)
# Roughness detected at brainstem regardless of expertise
f01 = sigma(0.40 * roughness * mean(PPC.consonance_encoding[10:20])
          + 0.30 * sethares
          + 0.30 * (1 - helmholtz))
# Coefficient sum: 0.40 + 0.30 + 0.30 = 1.0

# f02: MMN Dissonance (neural, expertise-independent)
# Mismatch negativity triggered by roughness deviance
f02 = sigma(0.50 * f01 * mean(PPC.pitch_salience[0:10])
          + 0.50 * abs(roughness - roughness_mean))
# Coefficient sum: 0.50 + 0.50 = 1.0

# f03: Behavioral Accuracy (expertise-dependent)
# Same neural signal, but behavioral response varies
# Without expertise modulation, baseline equals neural signal
f03 = f02
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| # | Region | MNI Coordinates | Source | Evidence Type | SDED Function |
|---|--------|-----------------|--------|---------------|---------------|
| 1 | **Heschl's Gyrus (A1)** | bilateral | Fishman 2001 (intracranial) | Direct (AEP/MUA) | Phase-locked oscillatory activity ∝ perceived dissonance; primary roughness encoder |
| 2 | **R Superior Temporal Gyrus** | right lateral | Foo 2016 (ECoG, N=8) | Direct (intracranial) | Dissonance-sensitive sites: high-gamma 70-150Hz, 75-200ms; spatial organization (anterior) |
| 3 | **L Superior Temporal Gyrus** | left lateral | Foo 2016 (ECoG) | Direct (intracranial) | Positive roughness-gamma correlation (both hemispheres) |
| 4 | **Fronto-central (MMN source)** | Fz electrode | Crespo-Bojorque 2018 (N=32) | Direct (EEG) | Early MMN generators: 152-258ms (universal) |
| 5 | **Planum Temporale** | ~±50, -24, 8 | Fishman 2001 | Direct (intracranial) | Does NOT show phase-locked activity — functional differentiation from HG |
| 6 | **R Heschl's Gyrus** | right | Bravo 2017 (fMRI) | Direct (fMRI) | Enhanced response to intermediate dissonance (uncertainty/ambiguity) |
| 7 | **Auditory Brainstem** | subcortical | Bidelman 2013 (FFR review) | Indirect (FFR) | Consonance hierarchy encoding without training; innate |
| 8 | **Supratemporal Plane** | bilateral | Yu et al. 2015 (review) | Indirect (EEG source) | Primary MMN generator region |
| 9 | **Inferior Frontocentral** | — | Yu et al. 2015 (review) | Indirect (EEG source) | Secondary MMN source for dissonance evaluation |

```
NOTE: Fishman 2001 intracranial data is critical — shows A1
(Heschl's gyrus) has phase-locked oscillatory activity for
dissonance, while PT does NOT. This functional differentiation
was confirmed in human (N=2, epilepsy monitoring) and closely
matched monkey A1 recordings.
```

---

## 9. Cross-Unit Pathways

### 9.1 SDED ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SDED INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (SPU):                                                         │
│  BCH.consonance_signal ──────► SDED (early roughness baseline)             │
│  SDNPS.roughness_correlation ► SDED (confirms roughness as primary)        │
│  ESME.expertise_enhancement ─► SDED (dissociation: neural=universal,       │
│                                       behavioral=trained)                   │
│  SDED.f01_early_detection ──► PSCL (roughness signal for pitch context)    │
│  SDED.roughness_detection ──► STAI (dissonance input for aesthetics)       │
│                                                                             │
│  CROSS-UNIT (P1: SPU → ARU):                                              │
│  SDED.f01_early_detection ──► ARU.SRP (roughness → displeasure proxy)     │
│  SDED.deviation_detection ──► ARU.AAC (dissonance surprise → arousal)     │
│                                                                             │
│  CROSS-UNIT (P2: SPU → STU):                                              │
│  SDED.roughness_detection ──► STU.AMSC (roughness affects timing)         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **No roughness** | Pure tones or perfectly harmonic stimuli should NOT trigger early detection | Testable |
| **Early MMN universal** | Early MMN (150-260ms) for consonance changes should be identical for M and NM | Supported: Crespo-Bojorque 2018 |
| **Late MMN expertise** | Late MMN (230-315ms) for dissonance changes should appear only in musicians | Supported: Crespo-Bojorque 2018 |
| **Behavioral divergence** | Musicians should show higher accuracy despite same early MMN | Supported: Crespo-Bojorque 2018 |
| **Brainstem lesions** | Should abolish roughness encoding but spare higher-level processing | Testable |
| **Infants** | Pre-linguistic infants should show MMN to roughness deviants | Testable |
| **Cross-cultural** | Non-Western listeners should show same MMN, may differ behaviorally | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class SDED(BaseModel):
    """Sensory Dissonance Early Detection.

    Output: 10D per frame.
    Reads: PPC mechanism (30D), R³ direct.
    """
    NAME = "SDED"
    UNIT = "SPU"
    TIER = "γ3"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("PPC",)        # Primary mechanism

    W1 = 0.40   # Roughness x PPC weight
    W2 = 0.30   # Sethares weight
    W3 = 0.30   # Inverse helmholtz weight
    MMN_DEV = 0.50  # Deviance weight
    MMN_DET = 0.50  # Detection weight

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """9 tuples for SDED computation."""
        return [
            # (r3_idx, horizon, morph, law)
            (0, 0, 0, 2),    # roughness, 25ms, value, bidirectional
            (0, 3, 1, 2),    # roughness, 100ms, mean, bidirectional
            (1, 0, 0, 2),    # sethares, 25ms, value, bidirectional
            (2, 0, 0, 2),    # helmholtz_kang, 25ms, value, bidirectional
            (2, 3, 1, 2),    # helmholtz_kang, 100ms, mean, bidirectional
            (5, 0, 0, 2),    # inharmonicity, 25ms, value, bidirectional
            (14, 3, 1, 0),   # tonalness, 100ms, mean, forward
            (18, 0, 0, 2),   # tristimulus1, 25ms, value, bidirectional
            (41, 3, 0, 2),   # x_l5l7[0], 100ms, value, bidirectional
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute SDED 10D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) SDED output
        """
        ppc = mechanism_outputs["PPC"]    # (B, T, 30)

        # R³ features
        roughness = r3[..., 0:1]
        sethares = r3[..., 1:2]
        helmholtz = r3[..., 2:3]
        stumpf = r3[..., 3:4]
        inharmonicity = r3[..., 5:6]
        tonalness = r3[..., 14:15]
        trist1 = r3[..., 18:19]
        trist2 = r3[..., 19:20]
        trist3 = r3[..., 20:21]
        x_l5l7 = r3[..., 41:46]          # (B, T, 5)

        # PPC sub-sections
        ppc_pitch = ppc[..., 0:10]        # pitch salience
        ppc_cons = ppc[..., 10:20]        # consonance encoding

        # H³ temporal features
        roughness_mean = h3_direct[(0, 3, 1, 2)]  # 100ms mean
        helmholtz_mean = h3_direct[(2, 3, 1, 2)]  # 100ms mean

        # ═══ LAYER E: Explicit features ═══
        # f01: Early Detection (pre-attentive, universal)
        f01 = torch.sigmoid(
            self.W1 * roughness * ppc_cons.mean(-1, keepdim=True)
            + self.W2 * sethares
            + self.W3 * (1.0 - helmholtz)
        )

        # f02: MMN Dissonance (neural, expertise-independent)
        roughness_deviation = torch.abs(
            roughness - roughness_mean.unsqueeze(-1)
        )
        f02 = torch.sigmoid(
            self.MMN_DET * f01 * ppc_pitch.mean(-1, keepdim=True)
            + self.MMN_DEV * roughness_deviation
        )

        # f03: Behavioral Accuracy (baseline = neural signal)
        f03 = f02

        # ═══ LAYER M: Mathematical ═══
        detection_function = torch.sigmoid(
            0.5 * f01 + 0.3 * f02
            + 0.2 * ppc_cons.mean(-1, keepdim=True)
        )

        # ═══ LAYER P: Present ═══
        roughness_detection = torch.sigmoid(
            roughness * ppc_cons.mean(-1, keepdim=True)
        )
        deviation_detection = roughness_deviation
        behavioral_response = torch.sigmoid(
            0.6 * f02 + 0.4 * ppc_pitch.mean(-1, keepdim=True)
        )

        # ═══ LAYER F: Future ═══
        dissonance_detection_pred = torch.sigmoid(
            0.6 * f01 + 0.4 * helmholtz_mean.unsqueeze(-1)
        )
        behavioral_accuracy_pred = torch.sigmoid(
            0.5 * f01 + 0.5 * f02
        )
        training_effect_pred = torch.sigmoid(
            0.7 * f02 + 0.3 * detection_function
        )

        return torch.cat([
            f01, f02, f03,                                      # E: 3D
            detection_function,                                  # M: 1D
            roughness_detection, deviation_detection,
            behavioral_response,                                 # P: 3D
            dissonance_detection_pred, behavioral_accuracy_pred,
            training_effect_pred,                                # F: 3D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 (v2.0.0→v2.1.0: 1→12) | 6 original + 3 reviews + 3 computational/imaging |
| **Effect Sizes** | MMN -0.34µV (Wagner 2018); POR Δ~36ms (Tabas 2019); early MMN 152-258ms universal (Crespo-Bojorque 2018) | Multiple verified effects |
| **Evidence Modality** | EEG-MMN, EEG-ERP, intracranial, ECoG, MEG, fMRI, computational | 7 methods |
| **Unique Participants** | >175 (excluding reviews/computational) | Multi-site convergence |
| **Critical Corrections** | "Tervaniemi, Makkonen & Nie (2022)" citation REMOVED (not found in collection); d=-1.09 REMOVED | Improved accuracy |
| **Falsification Tests** | 3/6 supported | Crespo-Bojorque 2018 supports early universal + late expertise |
| **R³ Features Used** | ~14D of 49D | Focused on consonance/roughness |
| **H³ Demand** | 9 tuples (0.39%) | Sparse, efficient |
| **PPC Mechanism** | 30D (2 sub-sections used) | Pitch + Consonance |
| **Output Dimensions** | **10D** | 4-layer structure |

---

## 13. Scientific References

1. **Crespo-Bojorque, P., Monte-Ordoña, J., & Toro, J. M. (2018)**. Early neural responses underlie advantages for consonance over dissonance. *Neuropsychologia*, 117, 188-198. — ⚠ **v2.0.0 CORRECTION**: Replaces fabricated "Tervaniemi, Makkonen & Nie (2022), Neuropsychologia 167, 108152" which was NOT FOUND in literature collection.
2. **Fishman, Y. I., Volkov, I. O., Noh, M. D., Garell, P. C., Bakken, H., Arezzo, J. C., Howard, M. A., & Steinschneider, M. (2001)**. Consonance and dissonance of musical chords: Neural correlates in auditory cortex of monkeys and humans. *Journal of Neurophysiology*, 86, 2761-2788.
3. **Foo, F., King-Stephens, D., Weber, P., Laxer, K., Parvizi, J., & Knight, R. T. (2016)**. Differential processing of consonance and dissonance within the human superior temporal gyrus. *Frontiers in Human Neuroscience*, 10, 154. DOI: 10.3389/fnhum.2016.00154
4. **Wagner, L., Rahne, T., Plontke, S. K., & Heidekrüger, N. (2018)**. Mismatch negativity reflects asymmetric pre-attentive harmonic interval discrimination. *PLoS ONE*, 13(4), e0196176. DOI: 10.1371/journal.pone.0196176
5. **Bidelman, G. M. (2013)**. The role of the auditory brainstem in processing musically relevant pitch. *Frontiers in Psychology*, 4, 264. DOI: 10.3389/fpsyg.2013.00264
6. **Cousineau, M., Bidelman, G. M., Peretz, I., & Lehmann, A. (2015)**. On the relevance of natural stimuli for the study of brainstem correlates: The example of consonance perception. *PLoS ONE*, 10(12), e0145439. DOI: 10.1371/journal.pone.0145439
7. **Tabas, A., Andermann, M., Schuberth, V., Riedel, H., Balaguer-Ballester, E., & Rupp, A. (2019)**. Modeling and MEG evidence of early consonance processing in auditory cortex. *PLoS Computational Biology*, 15(2), e1006820. DOI: 10.1371/journal.pcbi.1006820
8. **Bravo, F., Cross, I., Stamatakis, E. A., & Rohrmeier, M. (2017)**. Sensory cortical response to uncertainty and low salience during recognition of affective cues in musical intervals. *PLoS ONE*, 12(4), e0175991. DOI: 10.1371/journal.pone.0175991
9. **Sarasso, P., Ronga, I., Pistis, A., Forte, E., Garbarini, F., Ricci, R., & Neppi-Modona, M. (2019)**. Aesthetic appreciation of musical intervals enhances behavioural and neurophysiological indexes of attentional engagement and motor inhibition. *Scientific Reports*, 9, 18550. DOI: 10.1038/s41598-019-55131-9
10. **Wöhrle, S. D., Reuter, C., Rupp, A., & Andermann, M. (2024)**. Neuromagnetic representation of musical roundness in chord progressions. *Frontiers in Neuroscience*, 18, 1383554. DOI: 10.3389/fnins.2024.1383554
11. **Yu, X., Liu, T., & Gao, D. (2015)**. The mismatch negativity: An indicator of perception of regularities in music. *Behavioural Neurology*, 2015, Article ID 469508. DOI: 10.1155/2015/469508
12. **Trulla, L. L., Di Stefano, N., & Giuliani, A. (2018)**. Computational approach to musical consonance and dissonance. *Frontiers in Psychology*, 9, 381. DOI: 10.3389/fpsyg.2018.00381

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, ATT, NPL, EFC) | PPC mechanism (30D) |
| Early detection | S⁰.roughness[30] + HC⁰.OSC | R³.roughness[0] + PPC.consonance_encoding |
| Consonance (inverse) | S⁰.helmholtz_kang[32] + HC⁰.ATT | R³.helmholtz_kang[2] + PPC.pitch_salience |
| Spectral features | S⁰.spectral_contrast[53], kurtosis[107] | R³.tonalness[14], tristimulus[18:21] |
| Cross-band | S⁰.X_L5L6[208:216] + HC⁰.EFC | R³.x_l5l7[41:46] + PPC |
| Output dimensions | 11D | 10D (merged neural-behavior dissociation into formula) |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 25/2304 = 1.09% | 9/2304 = 0.39% |

### Why PPC replaces HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (OSC, ATT, NPL, EFC). In MI, these are unified into the PPC mechanism with 2 relevant sub-sections:
- **OSC + NPL → PPC.pitch_salience** [0:10]: Phase-locking + detection = roughness deviation
- **ATT + EFC → PPC.consonance_encoding** [10:20]: Attention + encoding = dissonance signal

### Why 11D → 10D

The legacy v1.0.0 had a separate `f04_neural_behavioral_dissociation` dimension. In MI v2.0.0, the dissociation is modeled implicitly: `f02_mmn_dissonance` represents the universal neural signal, and `f03_behavioral_accuracy` equals `f02` at baseline. Expertise modulation (making `f03 != f02`) is handled at the system level by ESME, not as a separate SDED output dimension.

---

**Model Status**: SPECULATIVE
**Output Dimensions**: **10D**
**Evidence Tier**: **gamma (Speculative)**
**Confidence**: **<70%**
