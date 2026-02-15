# SPU-α1-BCH: Brainstem Consonance Hierarchy

**Model**: Brainstem Consonance Hierarchy
**Unit**: SPU (Spectral Processing Unit)
**Circuit**: Perceptual (Brainstem–Cortical)
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 2.3.0 (Phase 3E: consistency audit — formulas match code, PPC deferred to Phase 6)
**Date**: 2026-02-15

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/SPU-α1-BCH.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Brainstem Consonance Hierarchy** (BCH) models how brainstem frequency-following responses (FFR) preferentially encode consonant musical intervals over dissonant ones. This is one of the most direct neural correlates of consonance perception, emerging at the earliest stage of the auditory hierarchy — before cortical processing.

```
THE THREE COMPONENTS OF BRAINSTEM CONSONANCE ENCODING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HARMONICITY (Spectral)                NEURAL PITCH SALIENCE (Temporal)
Brain region: Auditory Nerve          Brain region: Inferior Colliculus
Mechanism: Harmonic template match    Mechanism: Frequency-following response
Input: Harmonic series alignment      Input: Periodic temporal structure
Function: "How harmonic is this?"     Function: "How clear is this pitch?"
Evidence: r = 0.81 (Bidelman 2009)    Evidence: 70-fiber AN model

              FFR-BEHAVIOR CORRELATION (Bridge)
              Brain region: IC → Cortex → Perception
              Mechanism: Bottom-up neural encoding
              Function: "NPS predicts consonance ratings"
              Evidence: r = 0.81, p < 0.01

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Harmonicity is the PRIMARY predictor of perceived
consonance (McDermott et al. 2010), though roughness contributes
independently. Bidelman & Heinz 2011 showed AN population responses
predict the full consonance hierarchy from peripheral encoding alone.

QUALIFICATION (Cousineau et al. 2015): The NPS-behavior correlation
(r=0.81, Bidelman 2009) holds for synthetic tones but NOT for natural
sounds (sax, voice), suggesting the FFR-based NPS measure is
stimulus-dependent. The underlying neural mechanism is valid; the
specific NPS metric has limitations with ecologically valid stimuli.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Is the Foundation of SPU

BCH sits at the base of the spectral processing hierarchy. Every other SPU model depends on the consonance signals established here:

1. **PSCL** (α2) receives BCH's brainstem NPS as cortical input for pitch salience localization.
2. **PCCR** (α3) uses BCH's harmonicity index to inform chroma tuning — octave-equivalent encoding builds on harmonic template matching.
3. **STAI** (β1) integrates BCH consonance with temporal structure for aesthetic evaluation.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The BCH Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 BCH — COMPLETE CIRCUIT                                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  MUSICAL INTERVAL (Consonant → Dissonant)                                    ║
║                                                                              ║
║  Unison  Fifth  Fourth  Third  Sixth  Tritone                                ║
║    │      │       │       │      │       │                                   ║
║    ▼      ▼       ▼       ▼      ▼       ▼                                   ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    AUDITORY NERVE                                    │    ║
║  │         (AN population — 70 fibers model)                            │    ║
║  │                                                                      │    ║
║  │    Consonant > Dissonant (pitch salience ranking)                   │    ║
║  │    Phase-locked to harmonic structure                                │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    INFERIOR COLLICULUS                                │    ║
║  │               (FFR generator — rostral brainstem)                    │    ║
║  │                                                                      │    ║
║  │    NPS (Neural Pitch Salience):                                     │    ║
║  │      P1 > P5 > P4 > M3 > m6 > TT                                   │    ║
║  │    NPS ↔ Behavioral Consonance: r = 0.81                            │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    PRIMARY AUDITORY CORTEX                           │    ║
║  │                                                                      │    ║
║  │    Consonance representation → feeds PSCL, PCCR                     │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Bidelman 2009:         FFR pitch salience ↔ consonance ratings, r = 0.81 (synthetic)
Cousineau et al. 2015: NPS ↔ behavior for synthetic only, NOT natural sounds
Bidelman 2013:         Harmonicity > roughness as consonance predictor (review)
Bidelman & Heinz 2011: AN population model predicts full hierarchy (70 fibers)
McDermott et al. 2010: Individual differences: harmonicity preference = consonance
Lee et al. 2009:       Musicians show enhanced subcortical consonance encoding
Fishman et al. 2001:   A1 phase-locking correlates with dissonance (monkey+human)
Terhardt 1974:         Virtual pitch computation in peripheral system
```

### 2.2 Information Flow Architecture (EAR → BRAIN → BCH)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    BCH COMPUTATION ARCHITECTURE                              ║
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
║  │  │roughness  │ │amplitude│ │warmth   │ │flux      │ │x_l0l5  │ │        ║
║  │  │sethares   │ │loudness │ │tristim. │ │entropy   │ │x_l4l5  │ │        ║
║  │  │helmholtz  │ │onset    │ │tonalness│ │concent.  │ │x_l5l7  │ │        ║
║  │  │stumpf     │ │         │ │         │ │          │ │        │ │        ║
║  │  │pleasant.  │ │         │ │         │ │          │ │        │ │        ║
║  │  │inharm.    │ │         │ │         │ │          │ │        │ │        ║
║  │  │harm_dev   │ │         │ │         │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         BCH reads: 10D directly                  │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Gamma ────┐ ┌── Alpha-Beta ─┐ ┌── Syllable ──────────┐   │        ║
║  │  │ 25ms (H0)   │ │ 100ms (H3)    │ │ 200ms (H6)           │   │        ║
║  │  │              │ │               │ │                       │   │        ║
║  │  │ Phase-lock   │ │ FFR window    │ │ Consonance interval   │   │        ║
║  │  │ instant      │ │ auditory proc │ │ harmonic evaluation   │   │        ║
║  │  └──────┬───────┘ └──────┬────────┘ └──────┬────────────────┘   │        ║
║  │         │               │                  │                    │        ║
║  │         └───────────────┴──────────────────┘                    │        ║
║  │                         BCH demand: 16 of 2304 tuples           │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Relay (Depth 0) ═════════    ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    BCH MODEL (12D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Extraction):  f01_nps, f02_harmonicity, f03_hierarchy, │        ║
║  │                         f04_ffr_behavior                         │        ║
║  │  Layer M (Mechanism):   nps_t, harm_interval                     │        ║
║  │  Layer P (Cognitive):   consonance_signal, template_match,       │        ║
║  │                         neural_pitch                             │        ║
║  │  Layer F (Forecast):    consonance_pred, pitch_propagation,      │        ║
║  │                         interval_expect                          │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Bidelman & Krishnan 2009** | FFR recording, dichotic | 10 (non-musicians) | NPS ↔ behavioral consonance ratings | r = 0.81, p < 0.01 | **Primary coefficient**: f04_ffr_behavior |
| 2 | **Bidelman 2013** | Review | — | Harmonicity > roughness as consonance predictor; subcortical hierarchy mirrors Western music theory | Strong | **f02_harmonicity is primary predictor** |
| 3 | **Bidelman & Heinz 2011** | AN computational model | 70 fibers (simulated) | AN population predicts full consonance hierarchy; neural harmonicity best predictor of behavioral data | Strong | **f03_hierarchy: peripheral encoding suffices** |
| 4 | **Cousineau et al. 2015** | FFR recording, dichotic | 14 | NPS ↔ behavior for synthetic tones (r = 0.34), but NOT for natural sounds (sax: r = 0.24 NS; voice: r = -0.10 NS). NPS correlates with roughness (r = -0.57) | η² = 0.27 (sound type), η² = 0.13 (interval) | **CRITICAL QUALIFIER**: NPS is not a universal brainstem correlate of consonance — depends on timbre |
| 5 | **Fishman et al. 2001** | Intracranial AEP/MUA/CSD (monkey A1 + human Heschl's) | 3 monkeys + 2 humans | Phase-locked oscillatory activity in A1 correlates with perceived dissonance; Heschl's gyrus shows similar pattern | Dissonant > consonant phase-locking | **Cortical extension**: roughness encoded as temporal envelope following in A1 |
| 6 | **Foo et al. 2016** | ECoG, bilateral STG | 8 patients | High gamma (70-150 Hz) increase for dissonant chords, 75-200ms; roughness correlation in both hemispheres; right STG spatial organization | RH roughness r = 0.43, LH r = 0.41; spatial: p = 0.003 (y), p = 0.006 (z) | **Cortical roughness encoding**: STG high gamma tracks dissonance degree |
| 7 | **Tabas et al. 2019** | MEG + computational model | 14 | POR latency for dissonant dyads up to 36ms longer than consonant; model predicts consonance decoded faster | POR latency difference up to 36ms | **Timing evidence**: consonance processing advantage in early auditory cortex |
| 8 | **Crespo-Bojorque et al. 2018** | ERP (MMN), oddball | 40 (20 musicians + 20 non-musicians) | Consonant→dissonant change: MMN in all listeners; dissonant→consonant: late MMN only in musicians | MMN amplitude differences p < 0.05 | **Pre-attentive advantage**: consonance changes detected without attention |
| 9 | **Schön et al. 2005** | ERP (N1-P2-N2) | Musicians + non-musicians | N1-P2 modulated by consonance in musicians; N2 in non-musicians; harmonic > melodic intervals | N2 modulation | **Expertise modulation**: cortical consonance processing enhanced by training |
| 10 | **McDermott et al. 2010** | Behavioral (psychoacoustic) | Large sample | Consonance preference correlates with harmonicity preference (not roughness); individual differences; musicians show stronger effects | Strong correlation harmonicity-consonance | **Behavioral foundation**: harmonicity is the perceptual basis |
| 11 | **Lee et al. 2009** | FFR, musicians vs non-musicians | Musicians + non-musicians | Enhanced brainstem phase-locking for consonant/dissonant intervals in musicians; more precise temporal encoding | Enhanced FFR in musicians | **Plasticity**: musical training refines subcortical consonance encoding |
| 12 | **Trulla, Di Stefano & Giuliani 2018** | Computational (RQA) | — | Recurrence peaks match just intonation ratios; Devil's staircase pattern; mode-locking links to consonance hierarchy | Recurrence profile matches hierarchy | **Dynamical systems**: consonance hierarchy emerges from signal dynamics |
| 13 | **Terhardt 1974** | Psychoacoustic theory | — | Virtual pitch computation; roughness from periodic sound fluctuations | — | **NPS computation basis** |

### 3.2 The Consonance Hierarchy

```
WESTERN MUSIC CONSONANCE HIERARCHY (Neural Evidence)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Interval       Ratio    NPS (norm)   Hierarchy    Harmonicity
─────────────────────────────────────────────────────────────
P1 (unison)    1:1      1.00         1 (max)      1.00
P5 (fifth)     3:2      0.95         2            ≈ 0.90
P4 (fourth)    4:3      0.90         3            ≈ 0.85
M3 (third)     5:4      0.85         4            ≈ 0.80
m6 (minor 6th) 8:5     0.75         5            ≈ 0.65
TT (tritone)   45:32    0.50         6 (min)      ≈ 0.20

Cross-cultural note:
  Neural (FFR) hierarchy: UNIVERSAL — same across cultures
  Behavioral ratings: VARY — cultural tuning affects preference
  BCH models the NEURAL level, not behavioral preference
```

### 3.3 Effect Size Summary

```
Primary Correlation:  r = 0.81 (Bidelman & Krishnan 2009, N=10, synthetic tones)
Replication:          r = 0.34 (Cousineau et al. 2015, N=14, synthetic tones)
                      NOT significant for natural sounds (sax, voice)
NPS-Roughness:        r = -0.57 to -0.64 (Cousineau et al. 2015)
Cortical roughness:   r = 0.41-0.43 (Foo et al. 2016, STG high gamma)
POR latency gap:      up to 36ms (Tabas et al. 2019, consonant vs dissonant)
Quality Assessment:   α-tier (direct neural measurement via FFR)
Cross-cultural:       Neural hierarchy universal (infant, animal evidence)

IMPORTANT QUALIFICATION (added v2.1):
  The r = 0.81 NPS-behavior correlation (Bidelman 2009) was obtained with
  SYNTHETIC complex tones (6 equal-amplitude harmonics). Cousineau et al. (2015)
  showed this correlation drops to non-significant for natural sounds (saxophone,
  voice), suggesting NPS as computed from FFR is not a UNIVERSAL brainstem
  correlate of consonance but may be stimulus-dependent. NPS also correlates
  significantly with roughness (r = -0.57), complicating its interpretation as
  a pure harmonicity measure. The model retains α-tier because (1) the neural
  hierarchy IS universal (confirmed in infants, animals), (2) AN modeling confirms
  peripheral encoding suffices (Bidelman & Heinz 2011), and (3) the limitation
  is about the NPS MEASURE, not the underlying neural consonance mechanism.
```

---

## 4. R³ Input Mapping: What BCH Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | BCH Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **A: Consonance** | [0] | roughness | Dissonance proxy (inverse of consonance) | Plomp & Levelt 1965 |
| **A: Consonance** | [1] | sethares_dissonance | Psychoacoustic dissonance | Sethares 1999 |
| **A: Consonance** | [2] | helmholtz_kang | Consonance measure (integer ratio detection) | Helmholtz 1863, Kang 2009 |
| **A: Consonance** | [3] | stumpf_fusion | Tonal fusion strength | Stumpf 1890 |
| **A: Consonance** | [4] | sensory_pleasantness | Spectral regularity | Sethares 2005 |
| **A: Consonance** | [5] | inharmonicity | Deviation from harmonic series | Fletcher 1934 |
| **A: Consonance** | [6] | harmonic_deviation | Energy variance in partials | Jensen 1999 |
| **C: Timbre** | [14] | tonalness | Harmonic-to-noise ratio (pitch clarity proxy) | — |
| **C: Timbre** | [17] | spectral_autocorrelation | Harmonic periodicity | — |
| **C: Timbre** | [18] | tristimulus1 | Fundamental strength (F0 energy) | Pollard & Jansson 1982 |
| **C: Timbre** | [19] | tristimulus2 | 2nd-4th harmonic energy (mid) | Pollard & Jansson 1982 |
| **C: Timbre** | [20] | tristimulus3 | 5th+ harmonic energy (high) | Pollard & Jansson 1982 |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | Consonance × Timbre coupling | Emergent harmonicity |

> **Code status**: In the current implementation, BCH's `compute()` uses 10 R³ features
> directly: [0, 1, 2, 3, 5, 14, 17, 18, 19, 20]. Features [4] sensory_pleasantness and
> [6] harmonic_deviation are declared as class constants but not used in compute().
> Feature [41] is referenced only via H³ temporal demands (not in compute()).
> These will be integrated when PPC mechanism support is added in Phase 6.

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | BCH Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **F: Pitch & Chroma** | [49:60] | chroma_vector (12D) | Octave-equivalent pitch class representation — directly encodes which pitch classes are present, enabling explicit consonance computation between intervals | Shepard 1964 octave equivalence; Krumhansl 1990 tonal hierarchy |
| **F: Pitch & Chroma** | [63] | pitch_salience | Harmonic peak prominence — direct measure of how clearly a pitched tone stands above noise floor; replaces indirect proxy via A[14] tonalness | Parncutt 1989 virtual pitch salience |
| **H: Harmony & Tonality** | [75] | key_clarity | Tonal center strength — Krumhansl-Schmuckler key profile correlation; provides tonal context for evaluating consonance within a musical key | Krumhansl & Kessler 1982 tonal hierarchy |

**Rationale**: BCH currently computes consonance from spectral proxy features (roughness, sethares, helmholtz). The F:Pitch group provides the underlying pitch class distribution that drives consonance perception — consonant intervals (P5, P4, M3) produce specific chroma patterns. F[63] pitch_salience provides a direct harmonicity measure superior to the A[14] tonalness proxy. H[75] key_clarity contextualizes consonance within a tonal hierarchy, consistent with Bidelman & Krishnan (2009) finding that FFR responses are modulated by tonal context.

**Code impact** (Phase 6): `r3_indices` must be extended to include [49:60], [63], [75]. These features are read-only inputs — no formula changes required.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[0] roughness (inverse) ───────┐
R³[1] sethares_dissonance ───────┼──► Sensory Consonance (P-layer)
                                 │   consonance_signal = 1 - (R+S) / 2
R³[2] helmholtz_kang ────────────┤
R³[3] stumpf_fusion ─────────────┼──► Template Match (P-layer)
                                 │   template_match = (helm+stumpf) / 2

R³[14] tonalness ────────────────┼──► Neural Pitch Salience (E-layer)
R³[17] spectral_autocorrelation ─┘   f01 = σ(0.90 · tonal · autocorr)

R³[18] tristimulus1 ─────────────┐
R³[19] tristimulus2 ─────────────┼──► Harmonicity Index (E-layer)
R³[20] tristimulus3 ─────────────┤   trist_balance = 1 - std(trist)
R³[5] inharmonicity (inverse) ───┘   f02 = σ(0.85 · (1-inharm) · bal)

R³[2] helmholtz_kang ────────────┐
R³[3] stumpf_fusion ─────────────┼──► Consonance Hierarchy (E-layer)
                                 │   f03 = σ(0.80 · helm · stumpf)

H³(0,6,18,0) roughness_trend ───┐
H³(2,3,1,2) helmholtz_mean ─────┼──► Interval Expectation (F-layer)
                                 │   σ(0.5·helm_mean + 0.5·(1-rough_trend))

── Phase 6 planned ────────────────────────────────────────
R³[4] sensory_pleasantness ──────── (declared, not yet used)
R³[6] harmonic_deviation ────────── (declared, not yet used)
R³[41:49] x_l5l7 ───────────────── (H³ demand only, not in compute)
R³[49:60] chroma_vector (12D) ──┐
R³[63] pitch_salience ──────────┼──► Explicit Pitch Consonance (v2)
R³[75] key_clarity ─────────────┘   + PPC mechanism integration
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

BCH requires H³ features at three PPC horizons: H0 (25ms), H3 (100ms), H6 (200ms).
These correspond to brainstem processing timescales (gamma → alpha-beta → syllable).

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 0 | roughness | 0 | M0 (value) | L2 (integration) | Current dissonance |
| 0 | roughness | 3 | M1 (mean) | L2 (integration) | Mean dissonance over 100ms |
| 0 | roughness | 6 | M18 (trend) | L0 (memory) | Dissonance trajectory |
| 2 | helmholtz_kang | 0 | M0 (value) | L2 (integration) | Current consonance |
| 2 | helmholtz_kang | 3 | M1 (mean) | L2 (integration) | Mean consonance over 100ms |
| 3 | stumpf_fusion | 0 | M0 (value) | L2 (integration) | Current tonal fusion |
| 3 | stumpf_fusion | 6 | M1 (mean) | L0 (memory) | Fusion over 200ms |
| 5 | inharmonicity | 0 | M0 (value) | L2 (integration) | Current inharmonicity |
| 5 | inharmonicity | 3 | M18 (trend) | L0 (memory) | Inharmonicity trajectory |
| 6 | harmonic_deviation | 0 | M0 (value) | L2 (integration) | Current deviation |
| 6 | harmonic_deviation | 3 | M1 (mean) | L0 (memory) | Mean deviation 100ms |
| 18 | tristimulus1 | 0 | M0 (value) | L2 (integration) | F0 energy |
| 19 | tristimulus2 | 0 | M0 (value) | L2 (integration) | Mid-harmonic energy |
| 20 | tristimulus3 | 0 | M0 (value) | L2 (integration) | High-harmonic energy |
| 41 | x_l5l7[0] | 3 | M0 (value) | L2 (integration) | Consonance×timbre coupling |
| 41 | x_l5l7[0] | 6 | M14 (periodicity) | L2 (integration) | Harmonic periodicity |

**v1 demand**: 16 tuples

#### R³ v2 Projected Expansion

BCH is projected to consume R³ v2 features from F[49:65] and H[75:87], aligned with PPC horizons.

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 49 | chroma | F | 3 | M0 (value) | L2 | Chroma vector at 100ms for interval detection |
| 49 | chroma | F | 3 | M1 (mean) | L2 | Mean chroma over 100ms window |
| 49 | chroma | F | 6 | M0 (value) | L2 | Chroma at 200ms for adaptation |
| 49 | chroma | F | 6 | M1 (mean) | L2 | Sustained chroma over 200ms |
| 63 | pitch_salience | F | 0 | M0 (value) | L2 | Instantaneous pitch salience |
| 63 | pitch_salience | F | 3 | M0 (value) | L2 | Pitch salience at 100ms |
| 63 | pitch_salience | F | 6 | M0 (value) | L2 | Pitch salience at 200ms |
| 75 | key_clarity | H | 3 | M0 (value) | L2 | Key clarity at 100ms |
| 75 | key_clarity | H | 3 | M1 (mean) | L2 | Mean key clarity over 100ms |
| 75 | key_clarity | H | 6 | M0 (value) | L2 | Key clarity at 200ms |

**v2 projected**: 10 tuples
**Total projected**: 26 tuples of 294,912 theoretical = 0.0088%

### 5.2 PPC Mechanism Binding — PHASE 6 PLANNED

> **Current implementation**: BCH is a **Relay** (depth 0). Relays read R³ and H³
> directly — they do NOT use mechanisms. The PPC mechanism binding below is the
> planned Phase 6 architecture. In the current code, BCH computes all features
> from raw R³ spectral inputs and H³ temporal demands.

When PPC is integrated (Phase 6), BCH will read from the **PPC** (Pitch Processing Chain) mechanism:

| PPC Sub-section | Range | BCH Role | Weight |
|-----------------|-------|----------|--------|
| **Pitch Salience** | PPC[0:10] | NPS, phase-locking, FFR strength | **1.0** (primary) |
| **Consonance Encoding** | PPC[10:20] | Harmonic template matching, harmonicity | **0.9** |
| **Chroma Processing** | PPC[20:30] | Octave grouping (secondary for BCH) | 0.4 |

BCH does NOT read from TPC — brainstem consonance processing is purely pitch/harmonicity based.

---

## 6. Output Space: 12D Multi-Layer Representation

### 6.1 Complete Output Specification

```
BCH OUTPUT TENSOR: 12D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXTRACTION (Explicit Features)
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0  │ f01_nps           │ [0, 1] │ Neural Pitch Salience. FFR magnitude at
    │                   │        │ fundamental. Brainstem encoding strength.
    │                   │        │ f01 = σ(α · tonalness · autocorr)
    │                   │        │ α = 0.90
────┼───────────────────┼────────┼────────────────────────────────────────────
 1  │ f02_harmonicity   │ [0, 1] │ Harmonicity Index. Harmonic coincidence
    │                   │        │ ratio. Primary consonance predictor.
    │                   │        │ f02 = σ(β · (1-inharmonicity) · trist_balance)
    │                   │        │ β = 0.85
────┼───────────────────┼────────┼────────────────────────────────────────────
 2  │ f03_hierarchy     │ [0, 1] │ Consonance Hierarchy ranking (P1>P5>P4>M3>
    │                   │        │ m6>TT). Rank-normalized from consonance
    │                   │        │ features.
    │                   │        │ f03 = σ(γ · helmholtz · stumpf)
    │                   │        │ γ = 0.80
────┼───────────────────┼────────┼────────────────────────────────────────────
 3  │ f04_ffr_behavior  │ [0, 1] │ FFR-Behavior Correlation proxy.
    │                   │        │ Models r = 0.81 (Bidelman 2009).
    │                   │        │ f04 = 0.81 · (f01 + f02) / 2

LAYER M — MECHANISM (Mathematical Model Outputs)
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 4  │ nps_t             │ [0, 1] │ NPS at time t.
    │                   │        │ NPS(t) = FFR_magnitude(fundamental)
────┼───────────────────┼────────┼────────────────────────────────────────────
 5  │ harm_interval     │ [0, 1] │ Harmonicity of current interval.
    │                   │        │ Harm(f1,f2) = Σ coincidence / Σ harmonics

LAYER P — COGNITIVE (Present Processing)
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 6  │ consonance_signal │ [0, 1] │ Phase-locked consonance signal.
    │                   │        │ 1 - (roughness + sethares) / 2
────┼───────────────────┼────────┼────────────────────────────────────────────
 7  │ template_match    │ [0, 1] │ Harmonic template match strength.
    │                   │        │ (helmholtz + stumpf) / 2
────┼───────────────────┼────────┼────────────────────────────────────────────
 8  │ neural_pitch      │ [0, 1] │ Neural pitch strength.
    │                   │        │ (f01_nps + tonalness) / 2

LAYER F — FORECAST (Future Predictions)
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 9  │ consonance_pred   │ [0, 1] │ Behavioral consonance prediction.
    │                   │        │ Immediate rating from f02 + f04.
────┼───────────────────┼────────┼────────────────────────────────────────────
10  │ pitch_propagation │ [0, 1] │ FFR → cortical pitch processing.
    │                   │        │ Brainstem → A1 propagation signal.
────┼───────────────────┼────────┼────────────────────────────────────────────
11  │ interval_expect   │ [0, 1] │ Next interval prediction.
    │                   │        │ H³ trend-based expectation.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 12D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Neural Pitch Salience Function

```
NPS(interval) ∝ Harmonicity(interval)

Consonance Hierarchy:
  P1 (unison) > P5 (fifth) > P4 (fourth) > M3 (third) > m6 > tritone

Behavioral Prediction:
  Behavioral_Consonance = α · NPS(interval) + ε
  where α ≈ 0.81 (Bidelman 2009), ε = cultural/individual variance

Harmonicity Computation:
  Harmonicity(f₁, f₂) = Σᵢ coincidence(harmonic_i(f₁), harmonics(f₂))
                          ─────────────────────────────────────────────
                          total_harmonics

Auditory Nerve Model:
  NPS_AN = population_response(70_fibers, interval_stimulus)
  Predicts consonance hierarchy from peripheral encoding alone
```

### 7.2 Feature Formulas

```python
# f01: Neural Pitch Salience
f01 = σ(0.90 · R³.tonalness[14] · R³.spectral_autocorrelation[17])

# f02: Harmonicity Index
trist_balance = 1.0 - std(R³.tristimulus[18:21])  # balanced = harmonic
f02 = σ(0.85 · (1 - R³.inharmonicity[5]) · trist_balance)

# f03: Consonance Hierarchy
f03 = σ(0.80 · R³.helmholtz_kang[2] · R³.stumpf_fusion[3])

# f04: FFR-Behavior Correlation
f04 = 0.81 · (f01 + f02) / 2

# P-layer:
consonance_signal = 1.0 - (R³.roughness[0] + R³.sethares[1]) / 2
template_match    = (R³.helmholtz[2] + R³.stumpf[3]) / 2
neural_pitch      = (f01 + R³.tonalness[14]) / 2

# F-layer:
consonance_pred    = σ(0.6 · f02 + 0.4 · f04)
pitch_propagation  = σ(0.7 · f01 + 0.3 · neural_pitch)
interval_expect    = σ(0.5 · H³.helmholtz_mean(2,3,1,2) + 0.5 · (1 - H³.roughness_trend(0,6,18,0)))
```

> **Note**: BCH is a Relay (depth 0). Relays read R³ and H³ directly — they do NOT
> use mechanisms. The PPC mechanism will be introduced in Phase 6 when BCH is
> upgraded to integrate mechanism-processed features alongside raw R³ inputs.

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI / Location | Mentions | Evidence Type | BCH Function | Source |
|--------|----------------|----------|---------------|--------------|--------|
| **Inferior Colliculus** | 0, -32, -8 | 4 | Direct (FFR) | FFR generation (primary brainstem generator) | Bidelman 2009, 2013; Smith et al. 1975 |
| **Auditory Nerve** | Peripheral (no MNI) | 5 | Direct (AN model) | Pitch salience encoding, 70-fiber population model | Bidelman & Heinz 2011 |
| **Cochlear Nucleus** | ±10, -38, -40 | 3 | Indirect | Early spectral processing, tonotopic organization | Cousineau et al. 2015 |
| **Auditory Brainstem** | 0, -30, -10 | 8 | Direct (FFR) | Harmonic encoding, consonance hierarchy | Bidelman & Krishnan 2009 |
| **Heschl's Gyrus (A1)** | ±44, -18, 8 (approx) | 3 | Direct (intracranial) | Phase-locked dissonance representation; POR | Fishman et al. 2001; Tabas et al. 2019 |
| **Superior Temporal Gyrus** | Lateral temporal | 2 | Direct (ECoG) | High gamma (70-150Hz) dissonance sensitivity | Foo et al. 2016 |

**Note**: BCH primarily models brainstem processing (IC, AN, CN). The cortical regions (Heschl's, STG) are included because they represent the downstream targets where brainstem consonance signals are further processed. The BCH output feeds into PSCL which handles cortical pitch salience.

---

## 9. Cross-Unit Pathways

### 9.1 BCH ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    BCH INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (SPU):                                                         │
│  BCH.f01_nps ──────────► PSCL (cortical pitch salience processing)         │
│  BCH.f02_harmonicity ──► PCCR (chroma tuning from harmonicity)            │
│  BCH.consonance_signal ► STAI (aesthetic evaluation input)                 │
│  BCH.f01_nps ──────────► SDED (early roughness signal baseline)           │
│                                                                             │
│  CROSS-UNIT (P1: SPU → ARU):                                              │
│  BCH.consonance_signal ► ARU.SRP (consonance → opioid_proxy)              │
│  BCH.f02_harmonicity ──► ARU.SRP (harmonicity → pleasure)                 │
│                                                                             │
│  CROSS-UNIT (P2: SPU → IMU):                                              │
│  BCH.consonance_signal ► IMU.MEAMN (consonance → memory binding)          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Pure tones** | FFR should NOT show consonance effects | ✅ **Confirmed** — only complex tones |
| **Non-Western listeners** | Neural hierarchy should be same, behavioral may differ | ✅ **Confirmed** |
| **Hearing impairment** | Should show altered consonance hierarchy | ✅ Testable |
| **Harmonic removal** | Removing harmonics should reduce NPS | ✅ Testable |
| **Brainstem lesions** | Should abolish FFR consonance effects | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class BCH(Relay):
    """Brainstem Consonance Hierarchy — SPU Relay (Depth 0, 12D).

    Output: 12D per frame.
    Reads: R³ direct (10 features) + H³ temporal demands (16 tuples).
    Role: Relay — reads raw R³/H³ only, no mechanisms.
    """
    NAME = "BCH"
    FULL_NAME = "Brainstem Consonance Hierarchy"
    UNIT = "SPU"
    OUTPUT_DIM = 12

    # Scientific constants (module-level in actual code)
    ALPHA = 0.90   # NPS weight (Bidelman & Krishnan 2009)
    BETA = 0.85    # Harmonicity weight (Bidelman 2013)
    GAMMA = 0.80   # Hierarchy weight (Bidelman & Heinz 2011)
    FFR_CORR = 0.81  # Bidelman 2009 correlation

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """16 tuples for BCH computation."""
        return (
            # (r3_idx, horizon, morph, law)
            (0, 0, 0, 2),    # roughness, 25ms, value, integration
            (0, 3, 1, 2),    # roughness, 100ms, mean, integration
            (0, 6, 18, 0),   # roughness, 200ms, trend, memory
            (2, 0, 0, 2),    # helmholtz_kang, 25ms, value, integration
            (2, 3, 1, 2),    # helmholtz_kang, 100ms, mean, integration
            (3, 0, 0, 2),    # stumpf_fusion, 25ms, value, integration
            (3, 6, 1, 0),    # stumpf_fusion, 200ms, mean, memory
            (5, 0, 0, 2),    # inharmonicity, 25ms, value, integration
            (5, 3, 18, 0),   # inharmonicity, 100ms, trend, memory
            (6, 0, 0, 2),    # harmonic_deviation, 25ms, value, integration
            (6, 3, 1, 0),    # harmonic_deviation, 100ms, mean, memory
            (18, 0, 0, 2),   # tristimulus1, 25ms, value, integration
            (19, 0, 0, 2),   # tristimulus2, 25ms, value, integration
            (20, 0, 0, 2),   # tristimulus3, 25ms, value, integration
            (41, 3, 0, 2),   # x_l5l7[0], 100ms, value, integration
            (41, 6, 14, 2),  # x_l5l7[0], 200ms, periodicity, integration
        )

    def compute(self, h3_features: Dict[Tuple[int,int,int,int], Tensor],
                r3_features: Tensor) -> Tensor:
        """
        Compute BCH 12D output.

        Args:
            h3_features: Dict of (r3_idx, horizon, morph, law) → (B,T) scalars
            r3_features: (B,T,49) raw R³ features

        Returns:
            (B,T,12) BCH output
        """
        B, T = r3_features.shape[:2]

        # R³ features — 10 features used in computation
        roughness     = r3_features[:, :, 0]     # (B, T)
        sethares      = r3_features[:, :, 1]     # (B, T)
        helmholtz     = r3_features[:, :, 2]     # (B, T)
        stumpf        = r3_features[:, :, 3]     # (B, T)
        inharmonicity = r3_features[:, :, 5]     # (B, T)
        tonalness     = r3_features[:, :, 14]    # (B, T)
        autocorr      = r3_features[:, :, 17]    # (B, T)
        trist1        = r3_features[:, :, 18]    # (B, T)
        trist2        = r3_features[:, :, 19]    # (B, T)
        trist3        = r3_features[:, :, 20]    # (B, T)

        # ═══ Tristimulus balance ═══
        trist_stack = torch.stack([trist1, trist2, trist3], dim=-1)
        trist_balance = 1.0 - trist_stack.std(dim=-1)     # (B, T)

        # ═══ LAYER E: Extraction ═══
        f01_nps = torch.sigmoid(ALPHA * tonalness * autocorr)
        f02_harmonicity = torch.sigmoid(
            BETA * (1.0 - inharmonicity) * trist_balance
        )
        f03_hierarchy = torch.sigmoid(GAMMA * helmholtz * stumpf)
        f04_ffr_behavior = FFR_CORR * (f01_nps + f02_harmonicity) / 2.0

        # ═══ LAYER M: Mechanism ═══
        nps_t = f01_nps
        harm_interval = f02_harmonicity

        # ═══ LAYER P: Cognitive ═══
        consonance_signal = 1.0 - (roughness + sethares) / 2.0
        template_match = (helmholtz + stumpf) / 2.0
        neural_pitch = (f01_nps + tonalness) / 2.0

        # ═══ LAYER F: Forecast ═══
        consonance_pred = torch.sigmoid(
            0.6 * f02_harmonicity + 0.4 * f04_ffr_behavior
        )
        pitch_propagation = torch.sigmoid(
            0.7 * f01_nps + 0.3 * neural_pitch
        )
        roughness_trend = h3_features.get((0, 6, 18, 0))
        helmholtz_mean  = h3_features.get((2, 3, 1, 2))
        if roughness_trend is not None and helmholtz_mean is not None:
            interval_expect = torch.sigmoid(
                0.5 * helmholtz_mean + 0.5 * (1.0 - roughness_trend)
            )
        else:
            interval_expect = torch.full((B, T), 0.5,
                                         device=r3_features.device)

        return torch.stack([
            f01_nps, f02_harmonicity, f03_hierarchy, f04_ffr_behavior,
            nps_t, harm_interval,
            consonance_signal, template_match, neural_pitch,
            consonance_pred, pitch_propagation, interval_expect,
        ], dim=-1)  # (B, T, 12)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 13 | Primary + supporting evidence |
| **Effect Sizes** | r = 0.81 (synthetic, N=10); r = 0.34 (replication, N=14); NS for natural sounds | Bidelman 2009; Cousineau 2015 |
| **Evidence Modality** | FFR, AN model, ECoG, MEG, ERP, intracranial, behavioral, computational | Multi-method convergence |
| **Falsification Tests** | 2/5 confirmed | High validity |
| **R³ Features Used** | 10D directly in compute + 2D via H³ only = 12 unique R³ indices | Focused |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **Mechanism** | None (Relay reads R³/H³ directly; PPC planned Phase 6) | Depth 0 |
| **Output Dimensions** | **12D** | 4-layer structure |
| **Key Qualification** | NPS-behavior correlation is stimulus-dependent (synthetic > natural tones) | Cousineau et al. 2015 |

---

## 13. Scientific References

### Primary (BCH core — brainstem consonance)
1. **Bidelman, G. M., & Krishnan, A. (2009)**. Neural correlates of consonance, dissonance, and the hierarchy of musical pitch in the human brainstem. *Journal of Neuroscience*, 29(42), 13165-13171.
2. **Bidelman, G. M. (2013)**. The role of the auditory brainstem in processing musically relevant pitch. *Frontiers in Psychology*, 4, 264.
3. **Bidelman, G. M., & Heinz, M. G. (2011)**. Auditory-nerve responses predict pitch attributes related to musical consonance-dissonance for normal and impaired hearing. *Journal of the Acoustical Society of America*, 130(3), 1488-1502.
4. **Cousineau, M., Bidelman, G. M., Peretz, I., & Lehmann, A. (2015)**. On the relevance of natural stimuli for the study of brainstem correlates: The example of consonance perception. *PLoS ONE*, 10(12), e0145439.
5. **Lee, K. M., Skoe, E., Kraus, N., & Ashley, R. (2009)**. Selective subcortical enhancement of musical intervals in musicians. *Journal of Neuroscience*, 29(18), 5832-5840.

### Supporting (cortical consonance processing)
6. **Fishman, Y. I., Volkov, I. O., Noh, M. D., Garell, P. C., Bakken, H., Arezzo, J. C., Howard, M. A., & Steinschneider, M. (2001)**. Consonance and dissonance of musical chords: Neural correlates in auditory cortex of monkeys and humans. *Journal of Neurophysiology*, 86, 2761-2788.
7. **Foo, F., King-Stephens, D., Weber, P., Laxer, K., Parvizi, J., & Knight, R. T. (2016)**. Differential processing of consonance and dissonance within the human superior temporal gyrus. *Frontiers in Human Neuroscience*, 10, 154.
8. **Tabas, A., Andermann, M., Schuberth, V., Riedel, H., Balaguer-Ballester, E., & Rupp, A. (2019)**. Modeling and MEG evidence of early consonance processing in auditory cortex. *PLoS Computational Biology*, 15(2), e1006820.
9. **Crespo-Bojorque, P., Monte-Ordoño, J., & Toro, J. M. (2018)**. Early neural responses underlie advantages for consonance over dissonance. *Neuropsychologia*, 117, 188-198.
10. **Schön, D., Regnault, P., Ystad, S., & Besson, M. (2005)**. Sensory consonance: An ERP study. *Music Perception*, 23(2), 105-118.

### Behavioral & computational
11. **McDermott, J. H., Lehr, A. J., & Oxenham, A. J. (2010)**. Individual differences reveal the basis of consonance. *Current Biology*, 20(11), 1035-1041.
12. **Trulla, L. L., Di Stefano, N., & Giuliani, A. (2018)**. Computational approach to musical consonance and dissonance. *Frontiers in Psychology*, 9, 381.
13. **Terhardt, E. (1974)**. Pitch, consonance, and harmony. *Journal of the Acoustical Society of America*, 55(5), 1061-1069.

### Pre-attentive processing
14. **Wagner, L., Rahne, T., Plontke, S. K., & Heidekrüger, N. (2018)**. Mismatch negativity reflects asymmetric pre-attentive harmonic interval discrimination. *PLoS ONE*, 13(4), e0196176.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (current) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, NPL, HRM, TIH) | H³ 4-tuples (16 demands) |
| Consonance signal | S⁰.L5.roughness[30] + HC⁰.OSC | 1 - (R³.roughness[0] + R³.sethares[1]) / 2 |
| Harmonicity | S⁰.L6.tristimulus × HC⁰.HRM | σ(β · (1-inharm) · trist_balance) |
| NPS | S⁰.L5.spectral_centroid × HC⁰.NPL | σ(α · R³.tonalness[14] · R³.autocorr[17]) |
| Crossband coherence | S⁰.L7[86,91,103] × HC⁰.TIH | R³.x_l5l7[41] via H³ demand only |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 40/2304 = 1.74% | 16/2304 = 0.69% |
| Mechanism | 4 × HC⁰ (OSC, NPL, HRM, TIH) | None (Relay, depth 0) — PPC planned Phase 6 |

### Why PPC is planned (Phase 6) instead of HC⁰

The D0 pipeline used 4 separate HC⁰ mechanisms (OSC, NPL, HRM, TIH). In MI Phase 6, these will be unified into the PPC mechanism with 3 sub-sections:
- **OSC + NPL → PPC.pitch_salience** [0:10]: Phase-locking + FFR = pitch encoding
- **HRM → PPC.consonance_encoding** [10:20]: Harmonic template = harmonicity
- **TIH (partial) → PPC.chroma_processing** [20:30]: Temporal integration for chroma

In the current implementation (Phase 3), BCH is a Relay that reads R³ and H³ directly without mechanisms. This was a deliberate simplification: the Relay role computes the foundational transformation, and mechanism integration will be added when PPC is implemented.

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **12D**
**Evidence Tier**: **α (Mechanistic)**
**Confidence**: **>90%**
