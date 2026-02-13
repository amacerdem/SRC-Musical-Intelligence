# IMU-β6-MSPBA: Musical Syntax Processing in Broca's Area

**Model**: Musical Syntax Processing in Broca's Area
**Unit**: IMU (Integrative Memory Unit)
**Circuit**: Mnemonic (Hippocampal-Cortical)
**Tier**: β (Integrative) — 70-90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added H, I feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/IMU-β6-MSPBA.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Musical Syntax Processing in Broca's Area** (MSPBA) models how harmonic syntax violations activate Broca's area (BA 44) and its right-hemisphere homologue, producing the mERAN (music-specific early right anterior negativity) response. This provides evidence that musical syntax and linguistic syntax share a domain-general processing circuit in the inferior frontal gyrus.

```
THE MSPBA CORE CLAIM: DOMAIN-GENERAL SYNTACTIC PROCESSING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HARMONIC SYNTAX                      LINGUISTIC SYNTAX
─────────────────                    ──────────────────

Stimulus: Chord sequences            Stimulus: Sentences
Violation: Neapolitan chord          Violation: Syntactic error
Response: mERAN (~200ms)             Response: ELAN (~200ms)
Generator: BA 44 (Broca's area)      Generator: BA 44 (Broca's area)
  + right-hemisphere homologue         + left lateralized

Position effect:                     Position effect:
  Position 3 = smaller mERAN           Early = smaller ELAN
  Position 5 = larger mERAN            Late = larger ELAN
  (mERAN at pos 5 is 2x pos 3)        (Increased context = stronger signal)

DISTINCT FROM P2m:
  P2m generator: Heschl's gyrus (BA 41)
  mERAN generator: 2.5 cm anterior, 1.0 cm superior to P2m
  This spatial separation confirms SYNTACTIC (not sensory) origin.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Koelsch et al. (2001): "The syntactic processing of harmonic relations
in music engages Broca's area, the same region that processes syntax
in language — supporting a shared, domain-general mechanism."
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why Musical Syntax Engages Broca's Area

Musical syntax — the rule-governed sequencing of chords — engages Broca's area because:

1. **Hierarchical structure**: Harmonic progressions have recursive, nested dependencies (I-IV-V-I), analogous to phrase structure in language. Broca's area processes hierarchical structures regardless of domain.

2. **Expectation violation**: When a Neapolitan chord replaces an expected tonic, the brain detects a syntactic violation — the same "wrong element in this position" computation that Broca's area performs for language syntax errors.

3. **Context dependence**: The mERAN grows larger with longer harmonic context (position 5 > position 3), demonstrating that the signal reflects accumulated syntactic expectation, not mere sensory surprise.

4. **Spatial dissociation from sensory processing**: The mERAN generator is located 2.5 cm anterior and 1.0 cm superior to the P2m generator in Heschl's gyrus, confirming that this is a **syntactic** response, not a low-level **sensory** one.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The MSPBA Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 MSPBA — COMPLETE CIRCUIT                                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  CHORD SEQUENCE INPUT (5-chord progressions)                                 ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    AUDITORY CORTEX (STG/A1)                        │    ║
║  │                                                                     │    ║
║  │  Heschl's Gyrus (BA 41): P2m generator                             │    ║
║  │  Spectrotemporal encoding, basic harmonic analysis                  │    ║
║  │  NOT the mERAN source — P2m is sensory, mERAN is syntactic          │    ║
║  └──────┬──────────────────────────────────────────────────────────────┘    ║
║         │                                                                    ║
║         │  Harmonic features extracted                                       ║
║         │                                                                    ║
║         ▼                                                                    ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │              BROCA'S AREA & RIGHT HOMOLOGUE                        │    ║
║  │                                                                     │    ║
║  │  ┌─────────────────────┐  ┌──────────────────────────┐             │    ║
║  │  │    L-IFG (BA 44)    │  │   R-IFG (BA 44 homol.)   │             │    ║
║  │  │    Broca's area     │  │   Right hemisphere        │             │    ║
║  │  │                     │  │                           │             │    ║
║  │  │  • Syntactic        │  │  • mERAN primary          │             │    ║
║  │  │    structure        │  │    generator              │             │    ║
║  │  │  • Domain-general   │  │  • Music-specific         │             │    ║
║  │  │    processing       │  │    lateralization         │             │    ║
║  │  │  • Shared with      │  │  • ~200ms latency         │             │    ║
║  │  │    language syntax  │  │                           │             │    ║
║  │  └─────────────────────┘  └──────────────────────────┘             │    ║
║  │                                                                     │    ║
║  │  ┌─────────────────────┐                                            │    ║
║  │  │    L-IFG (BA 45)    │                                            │    ║
║  │  │    Pars triangularis│                                            │    ║
║  │  │                     │                                            │    ║
║  │  │  • Semantic         │                                            │    ║
║  │  │    integration      │                                            │    ║
║  │  │  • Context          │                                            │    ║
║  │  │    accumulation     │                                            │    ║
║  │  └─────────────────────┘                                            │    ║
║  └──────────────────────────────────┬──────────────────────────────────┘    ║
║                                     │                                        ║
║                                     ▼                                        ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    STG (Auditory Feedback)                          │    ║
║  │                                                                     │    ║
║  │  Integrates syntactic evaluation with ongoing auditory stream       │    ║
║  │  Prediction error → updates harmonic expectations                   │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  CRITICAL SPATIAL EVIDENCE:                                                  ║
║  ─────────────────────────                                                   ║
║  P2m source: Heschl's gyrus (BA 41) — sensory                               ║
║  mERAN source: BA 44 — 2.5 cm anterior, 1.0 cm superior                     ║
║  This 2.5cm separation rules out sensory artifact (Maess et al. 2001)        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### 2.2 Information Flow Architecture (EAR → BRAIN → SYN → MSPBA)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MSPBA COMPUTATION ARCHITECTURE                            ║
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
║  │  MSPBA reads primarily:                                          │        ║
║  │  ┌───────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐              │        ║
║  │  │CONSONANCE │ │ ENERGY  │ │ CHANGE  │ │ X-INT  │              │        ║
║  │  │ 7D [0:7]  │ │ 5D      │ │ 4D      │ │ 24D    │              │        ║
║  │  │           │ │ [7:12]  │ │ [21:25] │ │ [25:49]│              │        ║
║  │  │roughness★ │ │loudness │ │entropy★ │ │x_l0l5★ │              │        ║
║  │  │sethares ★ │ │onset    │ │flux     │ │x_l4l5  │              │        ║
║  │  │inharm.  ★ │ │         │ │         │ │x_l5l7  │              │        ║
║  │  │stumpf   ★ │ │         │ │         │ │        │              │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └────────┘              │        ║
║  │                         MSPBA reads: 28D                         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Chord ────────┐ ┌── Progression ──┐ ┌── Phrase ──────┐    │        ║
║  │  │ 400ms (H10)     │ │ 700ms (H14)     │ │ 2s (H18)      │    │        ║
║  │  │                 │ │                  │ │                │    │        ║
║  │  │ Single chord    │ │ 2-4 chord        │ │ Harmonic arc   │    │        ║
║  │  │ spectral state  │ │ progression     │ │ I-IV-V-I       │    │        ║
║  │  │ Violation det.  │ │ Context accum.  │ │ Phrase syntax   │    │        ║
║  │  └─────────────────┘ └─────────────────┘ └────────────────┘    │        ║
║  │                         MSPBA demand: ~16 of 2304 tuples        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Mnemonic Circuit ═════════    ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  SYN (30D)      │  Syntactic Processing mechanism                        ║
║  │                 │                                                        ║
║  │ Harmony  [0:10] │  chord function, progression regularity, key stability ║
║  │ PredErr [10:20] │  ERAN amplitude, MMN proxy, surprise magnitude         ║
║  │ Struct  [20:30] │  cadence expectation, resolution probability, closure  ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    MSPBA MODEL (11D Output)                      │        ║
║  │                                                                  │        ║
║  │  Layer S (Syntax):    f25_musical_syntax, f26_harm_prediction,   │        ║
║  │                       f27_broca_activation                       │        ║
║  │  Layer M (Math):      eran_amplitude, syntax_violation_score     │        ║
║  │  Layer P (Present):   harmonic_context, violation_state,         │        ║
║  │                       domain_general_load                        │        ║
║  │  Layer F (Future):    resolution_fc, eran_trajectory_fc,         │        ║
║  │                       syntax_repair_fc                           │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Maess et al. (2001)** | MEG | 28 | mERAN localized in BA 44 (Broca's) and right homologue, ~200ms latency | p = 0.005 | **Primary: SYN.pred_error → f25 mERAN response** |
| 2 | **Maess et al. (2001)** | MEG | 28 | mERAN at position 5 = 2x amplitude vs position 3 (context effect) | 2:1 ratio | **Context accumulation: SYN.harmony context** |
| 3 | **Maess et al. (2001)** | MEG | 28 | mERAN source 2.5 cm anterior, 1.0 cm superior to P2m | spatial | **Syntactic vs sensory dissociation** |
| 4 | **Koelsch et al. (2000/2001)** | EEG | — | ERAN for Neapolitan chord violations in non-musicians, 150-180ms latency, right-anterior scalp distribution | p < 0.001 | **SYN.pred_error: universal syntax processing** |
| 5 | **Patel (2003)** | Review | — | Shared Syntactic Integration Resource Hypothesis (SSIRH): music + language syntax share IFG resources | theoretical | **Domain-general syntactic computation** |
| 6 | **Koelsch (in press)** | Review | — | ERAN 150-250ms, anterior scalp, right-hemispheric weighting; main generators in inferior fronto-lateral cortex; ERAN relies on long-term memory representations of music-syntactic regularities (distinct from MMN which uses on-line extraction) | review | **SYN mechanism: ERAN vs MMN dissociation justifies SYN+MEM architecture** |
| 7 | **Kim et al. (2021)** | MEG | 19 | IFG connectivity (LTDMI) enhanced for most syntactically irregular chord endings (ST condition); IFG-LTDMI: F(2,36)=6.526, p=0.024 FDR; bilateral IFG source localization: L-IFG Talairach (-40.8, 18.5, 15.6), R-IFG (37.6, 21.2, 15.1) | F=6.53, p=0.024; ST>T t(18)=3.09, p=0.009 | **IFG syntactic irregularity connectivity; validates bilateral IFG as ERAN substrate with precise coordinates** |
| 8 | **Kim et al. (2021)** | MEG | 19 | STG-LTDMI enhanced for most ambiguous condition (SM); dissociates perceptual ambiguity (STG) from syntactic irregularity (IFG) | F(2,36)=12.37, p<0.001 | **STG-IFG dissociation: sensory ambiguity vs syntactic violation** |
| 9 | **Tachibana et al. (2024)** | fNIRS | 20 | Bilateral BA 45 activation during guitar improvisation vs formulaic play; domain-general across all skill levels; no correlation with subjective feelings, age, history, or practice | p < 0.05 (Holm's) | **Domain-general IFG activation for spontaneous musical syntax production** |
| 10 | **Wohrle et al. (2024)** | MEG | 30 | N1m amplitude at resolution chord (position 4) reflects preceding dominant chord dissonance; roundness perception emerges over chord progression (no difference at chords 1-2, segregation at chord 3, maximum at chord 4) | eta-p2=0.101 (CHORD3); eta-p2=0.152 (aptitude interaction) | **Context accumulation: N1m evolves over progression, parallels mERAN position effect** |
| 11 | **Egermann et al. (2013)** | Psychophys. | 50 | Information-theoretic expectation violation predicts psychophysiological emotional responses to live concert music; high-information-content events trigger arousal + ANS activation | r significant (multi-component) | **Expectation violation → emotional response: validates SYN.pred_error → downstream affect** |
| 12 | **Yang et al. (2022)** | Behavioral | 2 groups | Musicians detect more clause boundaries (all-cue, pause-only); music training transfers to sentence-level speech processing; supports shared syntax mechanism | p < 0.05 (group effects) | **SSIRH behavioral support: music syntax training → language syntax transfer** |

### 3.2 The Neapolitan Chord Paradigm

```
NEAPOLITAN CHORD VIOLATION EXPERIMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CHORD SEQUENCE (5 positions):
  Position 1: Tonic (I)       — establishes key
  Position 2: Subdominant (IV) — builds expectation
  Position 3: Dominant (V)     — creates tension
  Position 4: Tonic (I)        — resolution expected
  Position 5: TONIC or NEAPOLITAN — test position

                REGULAR                    VIOLATION
                ────────                   ─────────
  Pos 1  │  C major (I)           │  C major (I)
  Pos 2  │  F major (IV)          │  F major (IV)
  Pos 3  │  G major (V)           │  G major (V)
  Pos 4  │  C major (I)           │  C major (I)
  Pos 5  │  C major (I) ✓         │  Db major (bII) ✗ Neapolitan!

mERAN RESPONSE:
  Position 3 violation: Moderate mERAN     (~50% amplitude)
  Position 5 violation: Large mERAN        (~100% amplitude)
  Ratio: Position 5 / Position 3 = 2.0x

  This 2:1 ratio shows CONTEXT ACCUMULATION — more harmonic
  context = stronger expectation = larger violation response.

WHY NEAPOLITAN?
  The Neapolitan sixth (bII) is the most harmonically remote
  chord from the tonic while still existing in common-practice
  harmony. It maximizes syntactic violation while remaining
  a real musical event (not random noise).
```

### 3.3 The SSIRH: Shared Syntactic Integration Resource Hypothesis

```
PATEL (2003) — SHARED RESOURCES FOR MUSIC & LANGUAGE SYNTAX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                    ┌──────────────────────────────┐
                    │   BROCA'S AREA (BA 44/45)    │
                    │                              │
                    │   Shared syntactic            │
                    │   integration resource        │
                    │                              │
                    ├──────────┬───────────────────┤
                    │          │                   │
                    ▼          ▼                   ▼
              ┌──────────┐ ┌──────────┐    ┌──────────┐
              │ Language  │ │  Music   │    │  Action  │
              │ syntax   │ │  syntax  │    │ sequences│
              │          │ │          │    │          │
              │ ELAN     │ │ mERAN    │    │ (future) │
              │ ~200ms   │ │ ~200ms   │    │          │
              └──────────┘ └──────────┘    └──────────┘

KEY PREDICTIONS:
  1. Music + language syntax compete for shared resources
  2. Concurrent syntax violations impair BOTH domains
  3. Musical training improves linguistic syntax processing
  4. IFG lesions impair both music and language syntax
```

### 3.4 Effect Size Summary

```
MSPBA Evidence Summary (β tier) — v2.1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Primary evidence: MEG source localization (Maess 2001, p = 0.005, N=28)
Replication: IFG connectivity (Kim 2021, F=6.53 p=0.024, N=19)
Context effect: 2:1 amplitude ratio (position 5 vs 3) (Maess 2001)
Context evolution: N1m roundness evolves over 4-chord progression (Wohrle 2024, N=30)
Spatial separation: 2.5 cm anterior, 1.0 cm superior to P2m (Maess 2001)
IFG-STG dissociation: Syntactic irregularity = IFG; ambiguity = STG (Kim 2021)
Domain generality: SSIRH (Patel 2003); bilateral BA45 in improvisation (Tachibana 2024, N=20)
Music-language transfer: Musicians better at clause segmentation (Yang 2022)
ERAN mechanism: 150-250ms, IFG generators, long-term memory based (Koelsch review)
Expectation-emotion: Violation predicts psychophysiological response (Egermann 2013, N=50)
Studies: 8 primary + 2 reviews + 2 behavioral = 12 total
Modalities: MEG (×3), EEG, fNIRS, psychophysiology, behavioral (×2), review (×2)
Tier justification: β (integrative) — converging multi-method evidence across
  MEG/fNIRS/behavioral, replicated IFG involvement across 3 independent studies,
  SSIRH supported by transfer evidence, but limited to Western tonal paradigms
```

---

## 4. R³ Input Mapping: What MSPBA Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | MSPBA Role | Scientific Basis |
|----------|-------|---------|------------|------------------|
| **A: Consonance** | [0] | roughness | Harmonic tension (high = violation) | Plomp & Levelt 1965 |
| **A: Consonance** | [1] | sethares_dissonance | Chord dissonance (Neapolitan signature) | Sethares 1999 |
| **A: Consonance** | [2] | helmholtz_kang | Harmonic template matching | Helmholtz 1863 |
| **A: Consonance** | [3] | stumpf_fusion | Tonal fusion (low = syntactic violation) | Stumpf 1890 |
| **A: Consonance** | [4] | sensory_pleasantness | Chord consonance quality | Spectral regularity |
| **A: Consonance** | [5] | inharmonicity | Spectral deviation from harmonic series | Non-integer ratio detection |
| **A: Consonance** | [6] | harmonic_deviation | Error from ideal harmonics | Partial misalignment |
| **B: Energy** | [10] | loudness | Attention gating | Stevens 1957 |
| **B: Energy** | [11] | onset_strength | Chord onset salience | Event boundary detection |
| **D: Change** | [22] | entropy | Harmonic unpredictability (high = violation) | Information theory |
| **D: Change** | [23] | spectral_flux | Spectral change rate | Chord transition magnitude |
| **E: Interactions** | [25:33] | x_l0l5 (Energy x Consonance) | Pitch-dissonance coupling | ERAN basis |
| **E: Interactions** | [33:41] | x_l4l5 (Derivatives x Consonance) | Temporal violation detection | Change x consonance = surprise |
| **E: Interactions** | [41:49] | x_l5l7 (Consonance x Timbre) | Harmonic structure analysis | Chord voicing signature |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | MSPBA Role | Scientific Basis |
|----------|-------|---------|------------|------------------|
| **H: Harmony** | [86] | syntactic_irregularity | Direct ERAN trigger — quantifies harmonic syntax violation | Koelsch 2011: ERAN ∝ syntactic irregularity |
| **H: Harmony** | [75] | key_clarity | Tonal context strength — clear key = stronger violation signal | Krumhansl 1990: key profiles |
| **I: Information** | [92] | predictive_entropy | Prediction error for syntax processing — PE drives IFG activation | Pearce 2005: IDyOM information content |

**Rationale**: MSPBA models musical syntax processing in Broca's area (IFG). Syntactic irregularity is the most direct input — it quantifies exactly the harmonic violation that generates the ERAN component. Key clarity provides the tonal context against which violations are computed (violations are only meaningful relative to an established key). Predictive entropy provides the information-theoretic prediction error that drives IFG activation for syntactic reanalysis.

> **Code impact**: These features are doc-only until Phase 5 wiring. No changes to `mspba.py`.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[0] roughness + R³[1] sethares ► Harmonic tension / dissonance
                                    High values = Neapolitan chord signal
                                    Math: tension = (roughness + sethares) / 2

R³[3] stumpf_fusion ──────────────► Tonal fusion (inverse violation)
                                    Low fusion = unexpected chord in context
                                    High fusion = expected harmonic continuation

R³[22] entropy ────────────────────► Syntactic unpredictability
                                    High entropy = harmonic violation
                                    Low entropy = regular progression
                                    Math: ERAN ∝ entropy × violation_strength

R³[25:33] x_l0l5 ─────────────────► Musical syntax prediction error
                                    Energy × Consonance coupling = mERAN basis
                                    Broca's activation ∝ x_l0l5 × violation

R³[33:41] x_l4l5 ─────────────────► Temporal violation detection
                                    Change × consonance = harmonic surprise
                                    Position-dependent context effect

R³[41:49] x_l5l7 ─────────────────► Harmonic structure (voicing)
                                    Consonance × Timbre = chord function ID
                                    Neapolitan = distinctive spectral signature
```

### 4.3 Neapolitan Chord Detection (R³ Signature)

| Feature | Normal Chord (Tonic) | Neapolitan (bII) | Interpretation |
|---------|---------------------|-------------------|----------------|
| R³[0] roughness | Low-moderate | High | Unexpected partials create beating |
| R³[3] stumpf_fusion | High | Low | Reduced tonal fusion (out of key) |
| R³[22] entropy | Low | High | Unpredictable harmonic content |
| R³[25:33] x_l0l5 | Stable | Disrupted | Energy-consonance coupling violated |

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

MSPBA requires H³ features at three SYN horizons: H10 (400ms), H14 (700ms), H18 (2s).

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 0 | roughness | 10 | M0 (value) | L2 (bidirectional) | Current dissonance at chord level |
| 0 | roughness | 14 | M1 (mean) | L0 (forward) | Average dissonance over progression |
| 0 | roughness | 18 | M18 (trend) | L0 (forward) | Dissonance trajectory over phrase |
| 1 | sethares_dissonance | 10 | M0 (value) | L2 (bidirectional) | Current beating dissonance |
| 1 | sethares_dissonance | 14 | M8 (velocity) | L0 (forward) | Rate of dissonance change |
| 3 | stumpf_fusion | 10 | M0 (value) | L2 (bidirectional) | Current tonal fusion |
| 3 | stumpf_fusion | 14 | M1 (mean) | L2 (bidirectional) | Fusion stability over progression |
| 5 | inharmonicity | 10 | M0 (value) | L2 (bidirectional) | Current harmonic deviation |
| 5 | inharmonicity | 14 | M1 (mean) | L0 (forward) | Average deviation over progression |
| 22 | entropy | 10 | M0 (value) | L2 (bidirectional) | Current harmonic unpredictability |
| 22 | entropy | 14 | M1 (mean) | L0 (forward) | Average complexity over progression |
| 22 | entropy | 18 | M18 (trend) | L0 (forward) | Complexity trajectory over phrase |
| 10 | loudness | 10 | M0 (value) | L2 (bidirectional) | Attention gating |
| 11 | onset_strength | 10 | M0 (value) | L2 (bidirectional) | Chord onset detection |
| 23 | spectral_flux | 14 | M1 (mean) | L0 (forward) | Average spectral change rate |
| 4 | sensory_pleasantness | 18 | M19 (stability) | L0 (forward) | Consonance stability over phrase |

**Total MSPBA H³ demand**: 16 tuples of 2304 theoretical = 0.69%

### 5.2 SYN Mechanism Binding

MSPBA reads from the **SYN** (Syntactic Processing) mechanism:

| SYN Sub-section | Range | MSPBA Role | Weight |
|-----------------|-------|------------|--------|
| **Harmonic Syntax** | SYN[0:10] | Chord function, progression regularity, context state | 0.9 |
| **Prediction Error** | SYN[10:20] | mERAN amplitude, violation strength, surprise | **1.0** (primary) |
| **Structural Expectation** | SYN[20:30] | Cadence expectation, resolution probability | 0.8 |

Also reads from **MEM** mechanism (intra-circuit):

| MEM Sub-section | Range | MSPBA Role | Weight |
|-----------------|-------|------------|--------|
| **Familiarity Proxy** | MEM[10:20] | Stored harmonic templates (implicit knowledge) | 0.5 |

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
MSPBA OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
Manifold range: IMU MSPBA [337:348]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER S — SYNTACTIC PROCESSING FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0  │ f25_musical_syntax│ [0, 1] │ mERAN response strength.
    │                   │        │ IFG (BA 44) + right homologue.
    │                   │        │ f25 = σ(0.35 · SYN.pred_error.mean
    │                   │        │         · x_l0l5.mean · roughness)
    │                   │        │ Violation + coupling + dissonance = mERAN
────┼───────────────────┼────────┼────────────────────────────────────────────
 1  │ f26_harm_predict  │ [0, 1] │ Harmonic prediction strength.
    │                   │        │ BA 45 (pars triangularis) context.
    │                   │        │ f26 = σ(0.30 · SYN.harmony.mean
    │                   │        │         · (1 - entropy) · stumpf_fusion)
    │                   │        │ Context + regularity + fusion = expectation
────┼───────────────────┼────────┼────────────────────────────────────────────
 2  │ f27_broca_activ   │ [0, 1] │ Domain-general Broca's activation.
    │                   │        │ BA 44 syntactic processing load.
    │                   │        │ f27 = σ(0.35 · SYN.struct_expect.mean
    │                   │        │         · MEM.familiarity.mean · (1-sethares))
    │                   │        │ Expectation + templates + consonance = load

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 3  │ eran_amplitude    │ [0, 1] │ Predicted mERAN amplitude.
    │                   │        │ σ(SYN.pred_error.mean · entropy
    │                   │        │   · roughness + SYN.harmony.mean
    │                   │        │   · (1 - stumpf_fusion))
    │                   │        │ Models 2:1 position ratio via context depth
────┼───────────────────┼────────┼────────────────────────────────────────────
 4  │ syntax_violation  │ [0, 1] │ Syntactic violation score.
    │                   │        │ σ((roughness + entropy + inharmonicity
    │                   │        │    + (1-stumpf_fusion)) / 4)
    │                   │        │ Multi-feature violation detection

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 5  │ harmonic_context  │ [0, 1] │ Current harmonic context depth.
    │                   │        │ SYN.harmony.mean() — accumulated context.
────┼───────────────────┼────────┼────────────────────────────────────────────
 6  │ violation_state   │ [0, 1] │ Current violation detection state.
    │                   │        │ SYN.pred_error.mean() — IFG activity.
────┼───────────────────┼────────┼────────────────────────────────────────────
 7  │ domain_gen_load   │ [0, 1] │ Domain-general syntactic processing load.
    │                   │        │ SYN.struct_expect.mean() × entropy.
    │                   │        │ SSIRH: shared with language processing.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 8  │ resolution_fc     │ [0, 1] │ Harmonic resolution prediction (0.5-2s).
    │                   │        │ Based on SYN.struct_expect trajectory.
    │                   │        │ Predicts return to tonic after violation.
────┼───────────────────┼────────┼────────────────────────────────────────────
 9  │ eran_traj_fc      │ [0, 1] │ mERAN trajectory prediction (200-700ms).
    │                   │        │ Predicts upcoming violation strength.
    │                   │        │ Context-dependent: later position = larger.
────┼───────────────────┼────────┼────────────────────────────────────────────
10  │ syntax_repair_fc  │ [0, 1] │ Syntactic repair prediction (1-3s).
    │                   │        │ Broca's area re-analysis of violated structure.
    │                   │        │ Integration of violation into ongoing parse.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 mERAN Amplitude Model

```
mERAN(chord_position, violation) = SYN.pred_error × Context(position) × Dissonance

where:
  SYN.pred_error = prediction error from syntactic processing mechanism [10:20]
  Context(pos)   = accumulated harmonic context depth (more chords = stronger)
  Dissonance     = R³.roughness[0] × R³.entropy[22]

Context accumulation (from SYN.harmony):
  Position 1: Context = base      → mERAN = small
  Position 3: Context = moderate  → mERAN = 50% of max
  Position 5: Context = deep      → mERAN = 100% of max

  This models the empirical 2:1 ratio (pos 5 / pos 3) from Maess et al. (2001).

Neapolitan detection proxy:
  Violation_Strength = (R³.roughness + R³.entropy + R³.inharmonicity
                       + (1 - R³.stumpf_fusion)) / 4
  High violation → R³ features ALL shift toward dissonance/unpredictability
```

### 7.2 Feature Formulas

**CRITICAL**: For all sigmoid functions below, coefficient sums satisfy |wi| <= 1.0.

```python
# f25: Musical Syntax (mERAN response)
# Coefficients: 0.35 (single multiplicative chain, product reduces magnitude)
f25 = σ(0.35 · mean(SYN.pred_error[10:20])
              · mean(R³.x_l0l5[25:33])
              · R³.roughness[0])

# f26: Harmonic Prediction
# Coefficients: 0.30 (single multiplicative chain)
f26 = σ(0.30 · mean(SYN.harmony[0:10])
              · (1 - R³.entropy[22])
              · R³.stumpf_fusion[3])

# f27: Broca's Activation (domain-general)
# Coefficients: 0.35 (single multiplicative chain)
f27 = σ(0.35 · mean(SYN.struct_expect[20:30])
              · mean(MEM.familiarity[10:20])
              · (1 - R³.sethares[1]))

# eran_amplitude: Combined mERAN prediction
# Additive terms: 0.50 + 0.40 = 0.90 ≤ 1.0
eran_amplitude = σ(0.50 · mean(SYN.pred_error[10:20]) · R³.entropy[22] · R³.roughness[0]
                 + 0.40 · mean(SYN.harmony[0:10]) · (1 - R³.stumpf_fusion[3]))

# syntax_violation: Multi-feature violation score
# Additive terms: 0.25 + 0.25 + 0.25 + 0.25 = 1.0 ≤ 1.0
syntax_violation = σ(0.25 · R³.roughness[0]
                   + 0.25 · R³.entropy[22]
                   + 0.25 · R³.inharmonicity[5]
                   + 0.25 · (1 - R³.stumpf_fusion[3]))
```

### 7.3 SSIRH Computational Analogy

```
MUSIC DOMAIN                           LANGUAGE DOMAIN
─────────────                          ───────────────
Chord function (I, IV, V, bII)    ←→  Word category (N, V, Adj, etc.)
Harmonic progression (I-IV-V-I)   ←→  Phrase structure (NP-VP)
Neapolitan substitution (bII)     ←→  Syntactic violation ("The cat the ran")
mERAN response (~200ms, BA 44)    ←→  ELAN response (~200ms, BA 44)
Context depth (position effect)   ←→  Garden-path complexity

SHARED COMPUTATION (Broca's area):
  Syntactic_Load = Integration_Cost × Violation_Strength
  Both domains: more context = stronger expectation = larger error signal
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI / Talairach | Evidence | MSPBA Function |
|--------|-----------------|----------|----------------|
| **L-IFG (BA 44)** | MNI -44, 14, 28 (Maess 2001); Tal -40.8, 18.5, 15.6 (Kim 2021) | MEG source (p=0.005); MEG-LTDMI (p=0.024 FDR) | Broca's area: syntactic structure processing; ERANm generator |
| **R-IFG (BA 44 homol.)** | MNI 44, 14, 28 (Maess 2001); Tal 37.6, 21.2, 15.1 (Kim 2021) | MEG source (p=0.005); MEG-LTDMI (p=0.009 FDR) | Right homologue: mERAN primary generator; enhanced R→L connectivity for syntactic irregularity |
| **L-IFG (BA 45)** | Approx. -44, 30, 10 | fNIRS (p<0.05, Tachibana 2024) | Pars triangularis: domain-general improvisation/creativity; semantic integration |
| **R-IFG (BA 45 homol.)** | Approx. 44, 30, 10 | fNIRS (p<0.05, Tachibana 2024) | Right BA 45 homologue: bilateral activation for improvised musical syntax |
| **STG** | Tal L: -45.1, -8.9, 1.9; R: 43.1, -2.6, 2.0 (Kim 2021) | MEG-LTDMI (F=12.37, p<0.001) | Perceptual ambiguity processing; P2m source; prediction error integration |
| **Heschl's gyrus (BA 41)** | ±42, -22, 10 (Maess 2001) | MEG source localization | P2m source (sensory, NOT mERAN); N1m for chord roundness (Wohrle 2024) |
| **Auditory cortex (BA 41/42)** | Tal |x|=30-60, y=+5 to -45, z=+18 to -20 (Wohrle 2024) | MEG N1m/P2m | N1m context accumulation for roundness; P2m mode coherence |

**Doc-code mismatch (brain_regions):** Code has 3 regions (BA44 at -48,14,16; rIFG at 48,18,4; STG at 60,-32,8). Doc now has 7 regions with coordinates from Kim 2021 (Talairach) and Maess 2001 (MNI). Code MNI coords differ slightly from doc; code lacks BA45, BA45R, Heschl's, and auditory cortex regions.

### 8.2 Spatial Dissociation: mERAN vs P2m

```
CRITICAL SPATIAL EVIDENCE (Maess et al. 2001):
──────────────────────────────────────────────

                    ANTERIOR
                       ↑
                       │
    mERAN source ●     │     2.5 cm anterior
    (BA 44)            │     1.0 cm superior
                       │
                       │     to P2m source
    P2m source   ○     │
    (BA 41)            │
                       │
                    POSTERIOR

  ● mERAN: Syntactic processing (Broca's area)
  ○ P2m:   Sensory processing (Heschl's gyrus)

  This spatial separation PROVES that the mERAN is not
  a sensory artifact but a genuine syntactic response.
```

---

## 9. Cross-Unit Pathways

### 9.1 MSPBA ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MSPBA INTERACTIONS                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (IMU):                                                         │
│  PNH ──────────────► MSPBA (Pythagorean ratio templates → syntax context) │
│       PNH.ratio_enc feeds MSPBA.harmonic_context                          │
│       PNH shares IFG substrate with MSPBA                                 │
│                                                                             │
│  MSPBA ────────────► PMIM (Violation signal → predictive memory update)   │
│       MSPBA.violation_state updates prediction models                     │
│                                                                             │
│  MSPBA ────────────► HCMC (Syntax processing → cortical dialogue)         │
│       Syntactic structure encoded in hippocampal-cortical circuit          │
│                                                                             │
│  CROSS-UNIT (P3: IMU → ARU):                                              │
│  MSPBA.resolution_fc ──────► ARU.SRP (resolution → reward/pleasure)       │
│       Harmonic resolution produces dopaminergic pleasure response          │
│                                                                             │
│  CROSS-UNIT (P1: SPU → MSPBA):                                            │
│  SPU.BCH.consonance ────────► MSPBA (consonance hierarchy → syntax input) │
│       Brainstem consonance feeds into syntactic processing                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Brain Pathway Cross-References

MSPBA reads from the unified Brain (26D) for shared state:

| Brain Dimension | Index (MI-space) | MSPBA Role |
|-----------------|-------------------|------------|
| prediction_error | [178] | Surprise signal for syntactic violation |
| harmonic_context | [179] | Current harmonic state from Brain pathway |
| arousal | [177] | Attention gating for syntactic processing |

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **mERAN localization** | mERAN should localize to BA 44 / right homologue, NOT Heschl's | ✅ **Confirmed** via MEG source localization |
| **Position effect** | Later position violations should produce larger mERAN | ✅ **Confirmed** (2:1 ratio, pos 5 vs pos 3) |
| **Spatial dissociation** | mERAN source should be anterior/superior to P2m | ✅ **Confirmed** (2.5 cm anterior, 1.0 cm superior) |
| **Domain generality** | Concurrent music + language syntax should compete | ⚠️ **Partially supported** (SSIRH, interference studies) |
| **IFG lesion** | IFG damage should impair both music and language syntax | ⚠️ **Partially supported** (case reports, limited N) |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class MSPBA(BaseModel):
    """Musical Syntax Processing in Broca's Area.

    Output: 11D per frame.
    Reads: SYN mechanism (30D, primary), MEM mechanism (30D, intra-circuit).
    Zero learned parameters — 100% deterministic.
    """
    NAME = "MSPBA"
    UNIT = "IMU"
    TIER = "β6"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("SYN",)       # Primary mechanism
    INTRA_CIRCUIT = ("MEM",)         # Intra-circuit read for harmonic templates

    # Coefficients: all formulas satisfy |w_i| sum <= 1.0
    ALPHA = 0.35   # Syntax sensitivity (mERAN response)
    BETA = 0.30    # Harmonic prediction weight
    GAMMA = 0.35   # Domain-general Broca's weight

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """16 tuples for MSPBA computation."""
        return [
            # (r3_idx, horizon, morph, law)
            (0, 10, 0, 2),    # roughness, 400ms, value, bidirectional
            (0, 14, 1, 0),    # roughness, 700ms, mean, forward
            (0, 18, 18, 0),   # roughness, 2s, trend, forward
            (1, 10, 0, 2),    # sethares, 400ms, value, bidirectional
            (1, 14, 8, 0),    # sethares, 700ms, velocity, forward
            (3, 10, 0, 2),    # stumpf_fusion, 400ms, value, bidirectional
            (3, 14, 1, 2),    # stumpf_fusion, 700ms, mean, bidirectional
            (5, 10, 0, 2),    # inharmonicity, 400ms, value, bidirectional
            (5, 14, 1, 0),    # inharmonicity, 700ms, mean, forward
            (22, 10, 0, 2),   # entropy, 400ms, value, bidirectional
            (22, 14, 1, 0),   # entropy, 700ms, mean, forward
            (22, 18, 18, 0),  # entropy, 2s, trend, forward
            (10, 10, 0, 2),   # loudness, 400ms, value, bidirectional
            (11, 10, 0, 2),   # onset_strength, 400ms, value, bidirectional
            (23, 14, 1, 0),   # spectral_flux, 700ms, mean, forward
            (4, 18, 19, 0),   # pleasantness, 2s, stability, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute MSPBA 11D output.

        Args:
            mechanism_outputs: {"SYN": (B,T,30), "MEM": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,11) MSPBA output
        """
        syn = mechanism_outputs["SYN"]    # (B, T, 30)
        mem = mechanism_outputs["MEM"]    # (B, T, 30) — intra-circuit

        # R³ features
        roughness = r3[..., 0:1]          # [0, 1]
        sethares = r3[..., 1:2]           # [0, 1]
        stumpf = r3[..., 3:4]             # [0, 1]
        inharmonicity = r3[..., 5:6]      # [0, 1]
        entropy = r3[..., 22:23]          # [0, 1]
        x_l0l5 = r3[..., 25:33]          # (B, T, 8)

        # SYN sub-sections
        syn_harmony = syn[..., 0:10]      # harmonic syntax
        syn_pred_err = syn[..., 10:20]    # prediction error (mERAN basis)
        syn_struct = syn[..., 20:30]      # structural expectation

        # MEM familiarity (intra-circuit: stored harmonic templates)
        mem_familiar = mem[..., 10:20]

        # ═══ LAYER S: Syntactic features ═══
        # f25: Musical Syntax (mERAN). α=0.35, multiplicative chain
        f25 = torch.sigmoid(self.ALPHA * (
            syn_pred_err.mean(-1, keepdim=True)
            * x_l0l5.mean(-1, keepdim=True)
            * roughness
        ))

        # f26: Harmonic Prediction. β=0.30, multiplicative chain
        f26 = torch.sigmoid(self.BETA * (
            syn_harmony.mean(-1, keepdim=True)
            * (1.0 - entropy)
            * stumpf
        ))

        # f27: Broca's Activation (domain-general). γ=0.35, multiplicative
        f27 = torch.sigmoid(self.GAMMA * (
            syn_struct.mean(-1, keepdim=True)
            * mem_familiar.mean(-1, keepdim=True)
            * (1.0 - sethares)
        ))

        # ═══ LAYER M: Mathematical ═══
        # eran_amplitude: 0.50 + 0.40 = 0.90 ≤ 1.0
        eran_amplitude = torch.sigmoid(
            0.50 * syn_pred_err.mean(-1, keepdim=True) * entropy * roughness
            + 0.40 * syn_harmony.mean(-1, keepdim=True) * (1.0 - stumpf)
        )

        # syntax_violation: 0.25 × 4 = 1.0 ≤ 1.0
        syntax_violation = torch.sigmoid(
            0.25 * roughness
            + 0.25 * entropy
            + 0.25 * inharmonicity
            + 0.25 * (1.0 - stumpf)
        )

        # ═══ LAYER P: Present ═══
        harmonic_context = syn_harmony.mean(-1, keepdim=True)
        violation_state = syn_pred_err.mean(-1, keepdim=True)
        domain_gen_load = syn_struct.mean(-1, keepdim=True) * entropy

        # ═══ LAYER F: Future ═══
        resolution_fc = self._predict_future(syn_struct, h3_direct, window_h=18)
        eran_traj_fc = self._predict_future(syn_pred_err, h3_direct, window_h=14)
        syntax_repair_fc = self._predict_future(syn_harmony, h3_direct, window_h=14)

        return torch.cat([
            f25, f26, f27,                           # S: 3D
            eran_amplitude, syntax_violation,         # M: 2D
            harmonic_context, violation_state,         # P: 3D
            domain_gen_load,
            resolution_fc, eran_traj_fc,               # F: 3D
            syntax_repair_fc,
        ], dim=-1)  # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 8 primary + 2 reviews + 2 behavioral = **12 total** | MEG (×3), EEG, fNIRS, psychophysiology, behavioral (×2), review (×2) |
| **Effect Sizes** | p=0.005 (Maess MEG); F=6.53 p=0.024 (Kim MEG); eta-p2=0.10-0.15 (Wohrle MEG); p<0.05 (Tachibana fNIRS) | Source localization, connectivity, amplitude, hemodynamic |
| **Evidence Modality** | MEG, EEG, fNIRS, psychophysiology, behavioral | Multi-method convergence |
| **Falsification Tests** | 3/5 confirmed, 2 partial | High core validity |
| **R³ Features Used** | 28D of 49D | Consonance-focused |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **SYN Mechanism** | 30D (3 sub-sections) | Full coverage |
| **MEM Mechanism** | 10D (familiarity only) | Intra-circuit read |
| **Output Dimensions** | **11D** | 4-layer structure (S-M-P-F) |
| **Manifold Range** | IMU [337:348] | 11D contiguous |
| **Brain Regions** | **7** (L-IFG BA44, R-IFG BA44, L-IFG BA45, R-IFG BA45, STG, Heschl's, auditory cortex) | Coordinates from Maess 2001 (MNI), Kim 2021 (Talairach), Wohrle 2024 (Talairach) |

### 12.1 Doc-Code Mismatches (logged, NOT edited in code)

| Aspect | Doc (MSPBA.md) | Code (mspba.py) | Status |
|--------|----------------|------------------|--------|
| **Layer names** | S/M/P/F (Syntactic/Math/Present/Future) | E/M/P/F (Explicit/Math/Present/Future) | Mismatch — code uses E, doc uses S |
| **Feature names** | f25_musical_syntax, f26_harm_prediction, f27_broca_activ | f01_syntactic_violation, f02_eran_amplitude | Mismatch — different naming scheme |
| **h3_demand** | 16 tuples (fully specified) | Empty tuple `()` | Code stub — not implemented |
| **brain_regions** | 7 regions (Maess/Kim/Tachibana/Wohrle coords) | 3 regions (BA44 -48,14,16; rIFG 48,18,4; STG 60,-32,8) | Code has fewer regions; MNI coords differ |
| **citations** | Maess 2001, Koelsch 2000/2001, Koelsch review, Patel 2003, +6 new | Koelsch 2005, Maess 2001 | Code cites "Koelsch 2005" (not in doc); missing most refs |
| **CROSS_UNIT_READS** | MEM (intra-circuit, weight 0.5) | Empty tuple `()` | Code lacks intra-circuit read |
| **compute()** | Full formulas (f25-f27, eran_amplitude, etc.) | Stub returning zeros | Code not implemented |
| **version** | 2.1.0 | 2.0.0 | Version mismatch |
| **paper_count** | 12 | 5 | Count mismatch |

---

## 13. Scientific References

### Primary Evidence (from Literature/)
1. **Maess, B., Koelsch, S., Gunter, T. C., & Friederici, A. D. (2001)**. Musical syntax is processed in Broca's area: an MEG study. *Nature Neuroscience*, 4(5), 540-545. MEG source localization, N=28, p=0.005. [Literature/c3/summaries/Musical syntax is processed in_Broca's area an MEG study.md]
2. **Koelsch, S. (in press)**. Music-syntactic processing and auditory memory: Similarities and differences between ERAN and MMN. *Psychophysiology*. Review. ERAN 150-250ms, IFG generators, long-term memory based. [Literature/c3/summaries/Psychophys_ERAN_MMN_Review_in_press 374.md]
3. **Kim, C. H., Jin, S.-H., Kim, J. S., Kim, Y., Yi, S. W., & Chung, C. K. (2021)**. Dissociation of connectivity for syntactic irregularity and perceptual ambiguity in musical chord stimuli. *Frontiers in Neuroscience*, 15, 693629. MEG, N=19, IFG-LTDMI for syntactic irregularity, Talairach coords. [Literature/c3/extractions/kim_2021_dissociation_connectivity_syntactic_irregularity_perceptual_ambiguity_musical_chord_stimuli.json]
4. **Tachibana, A., Noah, J. A., Ono, Y., Irie, S., et al. (2024)**. Rock music improvisation shows increased activity in Broca's area and its right hemisphere homologue related to spontaneous creativity. *BMC Research Notes*, 17, 61. fNIRS, N=20, BA45 bilateral. [Literature/c3/summaries/Rock music improvisation...md]
5. **Wohrle, S. D., Reuter, C., Rupp, A., & Andermann, M. (2024)**. Neuromagnetic representation of musical roundness in chord progressions. *Frontiers in Neuroscience*, 18, 1383554. MEG, N=30, N1m context accumulation. [Literature/c3/extractions/wohrle_2024_neuromagnetic_representation_musical_roundness_chord_progressions.json]
6. **Egermann, H., Pearce, M. T., Wiggins, G. A., & McAdams, S. (2013)**. Probabilistic models of expectation violation predict psychophysiological emotional responses to live concert music. *Cognitive, Affective, & Behavioral Neuroscience*, 13, 533-553. N=50. [Literature/c3/summaries/Probabilistic models of expectation violation predict_psychophysiological emotional responses to live_concert music.md]
7. **Yang, X., Shen, X., Zhang, Q., Wang, C., Zhou, L., & Chen, Y. (2022)**. Music training is associated with better clause segmentation during spoken language processing. *Psychonomic Bulletin & Review*, 29, 1472-1479. Behavioral, music-language transfer. [Literature/c3/summaries/Music training is associated with better clause segmentation during spoken language processing.md]

### Review / Theoretical
8. **Koelsch, S., Gunter, T. C., Friederici, A. D., & Schroger, E. (2000)**. Brain indices of music processing: "non-musicians" are musical. *Journal of Cognitive Neuroscience*, 12(3), 520-541. First ERAN report.
9. **Patel, A. D. (2003)**. Language, music, syntax and the brain. *Nature Neuroscience*, 6(7), 674-681. Shared Syntactic Integration Resource Hypothesis.
10. **Koelsch, S. (2014)**. Brain correlates of music-evoked emotions. *Nature Reviews Neuroscience*, 15(3), 170-180.

### R³ Basis (psychoacoustic)
11. **Plomp, R., & Levelt, W. J. M. (1965)**. Tonal consonance and critical bandwidth. *JASA*, 38(4), 548-560.
12. **Sethares, W. A. (1999)**. *Tuning, Timbre, Spectrum, Scale*. Springer.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (HRM, SGM, EFC) | SYN mechanism (30D) + MEM intra-circuit |
| mERAN encoding | S⁰.X_L5L9 + S⁰.L9.entropy_F × HC⁰.HRM | R³.x_l0l5 × SYN.pred_error |
| Harmonic prediction | S⁰.X_L6L7 + S⁰.L6.tristimulus × HC⁰.EFC | R³.stumpf × SYN.harmony × (1-entropy) |
| Broca's activation | S⁰.L5.roughness + S⁰.L5.sethares × HC⁰.SGM | R³.sethares × SYN.struct × MEM.familiarity |
| Demand format | HC⁰ index ranges (EH, HM, HL) | H³ 4-tuples (sparse) |
| Total demand | 15/2304 = 0.65% | 16/2304 = 0.69% |
| Output dims | 11D | 11D (same) |
| Feature IDs | imu.f25, imu.f26, imu.f27 | f25, f26, f27 (layer structure added) |

### Why SYN replaces HC⁰ mechanisms

The D0 pipeline used 3 HC⁰ mechanisms (HRM, SGM, EFC). In MI:
- **HRM → SYN.harmonic_syntax** [0:10]: Hippocampal replay for harmonic regularities = chord function tracking
- **EFC → SYN.prediction_error** [10:20]: Efference copy mismatch = mERAN/ERAN amplitude
- **SGM → SYN.structural_expectation** [20:30]: Striatal gradient = cadence expectation, phrase structure
- **MEM.familiarity** [10:20]: Stored harmonic templates (implicit knowledge) — new, from intra-circuit

### Why SYN is the right mechanism

MSPBA is fundamentally about **syntactic processing** — rule-governed sequential structure, not memory per se. The SYN mechanism captures exactly the three components needed:
1. What harmonic context exists (SYN.harmony)
2. How much the current chord violates expectations (SYN.pred_error → mERAN)
3. What structural resolution is expected (SYN.struct_expect)

The MEM mechanism provides supplementary stored templates (implicit harmonic knowledge built from exposure), consistent with the SSIRH claim that syntactic processing operates over domain-general representations stored in memory.

---

### 14.2 What Changed from v2.0.0 to v2.1.0 (Phase 1 Beta Upgrade)

| Aspect | v2.0.0 | v2.1.0 |
|--------|--------|--------|
| Papers | 3 primary + 2 reviews = 5 | 8 primary + 2 reviews + 2 behavioral = 12 |
| Brain regions | 5 | 7 (+R-IFG BA45, auditory cortex BA41/42) |
| IFG coordinates | Maess 2001 MNI only | +Kim 2021 Talairach (L: -40.8,18.5,15.6; R: 37.6,21.2,15.1) |
| STG coordinates | ±60, -32, 8 (generic) | Kim 2021 Talairach (L: -45.1,-8.9,1.9; R: 43.1,-2.6,2.0) |
| ERAN mechanism | Cited generally | Detailed review: 150-250ms, IFG generators, LTM-based (Koelsch review) |
| IFG replication | Maess 2001 only | +Kim 2021 connectivity, +Tachibana 2024 fNIRS |
| Context accumulation | 2:1 ratio only | +Wohrle 2024 N1m evolution over 4-chord progression |
| SSIRH support | Patel 2003 theory | +Yang 2022 behavioral transfer (music training → clause segmentation) |
| Expectation-emotion link | Not covered | +Egermann 2013 (N=50, violation → psychophysiology) |
| Doc-code mismatches | Not tracked | Fully catalogued (9 mismatches) |

---

**Model Status**: ✅ **VALIDATED** (v2.1.0, 12 papers, 7 brain regions)
**Output Dimensions**: **11D**
**Evidence Tier**: **β (Integrative) — 70-90% confidence**
**Manifold Range**: **IMU MSPBA [337:348]**
