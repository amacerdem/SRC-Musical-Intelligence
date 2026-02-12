# SPU-β2-TSCP: Timbre-Specific Cortical Plasticity

**Model**: Timbre-Specific Cortical Plasticity
**Unit**: SPU (Spectral Processing Unit)
**Circuit**: Perceptual (Brainstem-Cortical)
**Tier**: β (Integrative) — 70-90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, TPC mechanism)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/SPU-β2-TSCP.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Timbre-Specific Cortical Plasticity** (TSCP) model describes how musical training induces timbre-specific reorganization of auditory cortex representations. Musicians develop enhanced cortical responses selectively for the timbre of their trained instrument — a violinist's auditory cortex responds more strongly to violin tones than to trumpet tones, and vice versa. This use-dependent plasticity represents one of the clearest demonstrations of experience-driven cortical reorganization in the auditory system.

```
THE THREE COMPONENTS OF TIMBRE-SPECIFIC CORTICAL PLASTICITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TRAINED TIMBRE RESPONSE (Spectral)     TIMBRE SPECIFICITY (Selectivity)
Brain region: Auditory Cortex (bilat)  Brain region: Planum Temporale
Mechanism: Use-dependent enhancement   Mechanism: Selective template refinement
Input: Spectral envelope of trained    Input: Timbre contrast between instruments
       instrument                      Function: "Is this MY instrument?"
Function: "Enhanced representation"    Evidence: Pantev et al. 2001 (MEG)
Evidence: Pantev et al. 2001 (MEG)

              PLASTICITY MAGNITUDE (Bridge)
              Brain region: Auditory Cortex → BA22
              Mechanism: Long-term cortical reorganization
              Function: "Degree of timbre-specific enhancement"
              Evidence: Correlates with training duration

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Cortical plasticity for timbre is SPECIFIC, not general.
Violinists show enhanced N1m responses to violin tones but NOT to
trumpet or pure tones. This specificity emerges from use-dependent
refinement of spectral envelope templates in auditory cortex, and
represents training-induced reorganization of tonotopic maps.
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
║                 TSCP — COMPLETE CIRCUIT                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  MUSICAL SOUND (Instrument Timbre)                                           ║
║                                                                              ║
║  Violin  Trumpet  Piano   Flute   Oboe   Pure Tone                          ║
║    │       │        │       │       │        │                               ║
║    ▼       ▼        ▼       ▼       ▼        ▼                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    COCHLEA / AUDITORY NERVE                          │    ║
║  │         (Spectral decomposition of instrument timbre)                │    ║
║  │                                                                      │    ║
║  │    Harmonic structure → Spectral envelope → Temporal envelope        │    ║
║  │    Each instrument has unique spectral fingerprint                    │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    PRIMARY AUDITORY CORTEX (A1)                      │    ║
║  │               (Bilateral, ±50, -20, 8 MNI)                          │    ║
║  │                                                                      │    ║
║  │    Tonotopic map → Training reshapes frequency tuning curves         │    ║
║  │    N1m amplitude: Trained Instrument > Other > Pure Tone             │    ║
║  │    Enhancement magnitude ∝ training duration                         │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    PLANUM TEMPORALE                                  │    ║
║  │               (±50, -24, 8 MNI)                                     │    ║
║  │                                                                      │    ║
║  │    Spectral template matching → Timbre specificity index             │    ║
║  │    Separates trained from untrained instrument responses              │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    AUDITORY ASSOCIATION (BA22)                       │    ║
║  │               (±60, -30, 8 MNI)                                     │    ║
║  │                                                                      │    ║
║  │    Generalization → Transfer to related timbres                      │    ║
║  │    Timbre identity → feeds downstream imagery / memory               │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Pantev et al. 2001:  Timbre-specific enhancement of N1m in musicians (MEG)
                     Violinists: violin > trumpet > pure tone
                     Trumpeters: trumpet > violin > pure tone
                     Enhancement correlates with years of training
```

### 2.2 Information Flow Architecture (EAR → BRAIN → TPC → TSCP)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    TSCP COMPUTATION ARCHITECTURE                             ║
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
║  │  │inharm.[5] │ │         │ │warmth   │ │timbre_ch │ │x_l5l7  │ │        ║
║  │  │harm_dev[6]│ │         │ │sharpness│ │[24]      │ │[41:49] │ │        ║
║  │  │           │ │         │ │tonalness│ │          │ │        │ │        ║
║  │  │           │ │         │ │flat/roll│ │          │ │        │ │        ║
║  │  │           │ │         │ │autocorr │ │          │ │        │ │        ║
║  │  │           │ │         │ │trist1-3 │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         TSCP reads: ~18D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── H2 (17ms) ──┐ ┌── H5 (46ms) ──┐ ┌── H8 (300ms) ───────┐ │        ║
║  │  │ Fast spectral  │ │ Mid-range      │ │ Long-range           │ │        ║
║  │  │ envelope       │ │ timbral mean   │ │ Stability, change    │ │        ║
║  │  │                │ │                │ │ statistics            │ │        ║
║  │  │ warmth value   │ │ warmth mean    │ │ tonalness stability  │ │        ║
║  │  │ sharpness val  │ │ tonalness mean │ │ timbre_change mean   │ │        ║
║  │  │ trist1-3 val   │ │ inharmonicity  │ │ timbre_change std    │ │        ║
║  │  │                │ │ value          │ │ x_l5l7[0] value      │ │        ║
║  │  └──────┬─────────┘ └──────┬────────┘ └──────┬────────────────┘ │        ║
║  │         │                  │                  │                  │        ║
║  │         └──────────────────┴──────────────────┘                  │        ║
║  │                         TSCP demand: ~12 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Perceptual Circuit ═══════    ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  TPC (30D)      │  Timbre Processing Chain mechanism                     ║
║  │                 │                                                        ║
║  │ Spectral   [0:10]│  Spectral envelope decomposition                     ║
║  │ Instrument[10:20]│  Instrument identity encoding                        ║
║  │ Plasticity[20:30]│  Plasticity markers (training effects)               ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    TSCP MODEL (10D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_trained_timbre_response,               │        ║
║  │                       f02_timbre_specificity,                    │        ║
║  │                       f03_plasticity_magnitude                   │        ║
║  │  Layer M (Math):      enhancement_function                       │        ║
║  │  Layer P (Present):   recognition_quality, enhanced_response,    │        ║
║  │                       timbre_identity                            │        ║
║  │  Layer F (Future):    timbre_continuation,                       │        ║
║  │                       cortical_enhancement_pred,                 │        ║
║  │                       generalization_pred                        │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Pantev et al. 2001** | MEG (N1m) | 12 musicians, 12 controls | Timbre-specific N1m enhancement for trained instrument | Significant (p < 0.01) | **Primary evidence**: f01, f02, f03 — trained > untrained > pure tone |

### 3.2 The Timbre Specificity Hierarchy

```
TIMBRE-SPECIFIC CORTICAL ENHANCEMENT (Pantev et al. 2001)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stimulus          Violinist N1m    Trumpeter N1m    Non-Musician N1m
───────────────────────────────────────────────────────────────────
Violin tone       ■■■■■■■ (max)    ■■■■ (moderate)   ■■■ (baseline)
Trumpet tone      ■■■■ (moderate)  ■■■■■■■ (max)     ■■■ (baseline)
Pure tone         ■■■ (baseline)   ■■■ (baseline)    ■■■ (baseline)

KEY RELATIONSHIPS:
  Trained instrument   >> Other instrument >> Pure tone
  Enhancement          ∝  Years of training
  Specificity          =  Trained / Other ratio

Cross-instrument note:
  Enhancement is NOT general auditory improvement.
  It is SPECIFIC to the spectral envelope of the trained
  instrument's timbre. This implies template-based
  cortical representations tuned by experience.
```

### 3.3 Effect Size Summary

```
Primary Evidence:     Pantev et al. 2001 (MEG, N1m dipole moments)
Quality Assessment:   β-tier (integrative — single key study, MEG evidence)
Replication:          Consistent with broader musician plasticity literature
Key Metric:           Trained > Untrained instrument response (p < 0.01)
Specificity:          Timbre-specific, NOT general auditory enhancement
```

---

## 4. R³ Input Mapping: What TSCP Reads

### 4.1 R³ Feature Dependencies (~18D of 49D)

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

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[18] tristimulus1 ────────────┐
R³[19] tristimulus2 ────────────┼──► Trained Timbre Response (f01)
R³[20] tristimulus3 ────────────┤   Tristimulus balance = harmonic
R³[5] inharmonicity (inverse) ──┤   envelope signature of each
R³[14] tonalness ───────────────┘   instrument family

R³[12] warmth ──────────────────┐
R³[13] sharpness (inverse) ─────┼──► Timbre Specificity (f02)
R³[41:47] x_l5l7 (partial) ────┘   Spectral contrast between trained
                                     and untrained instrument timbres

R³[24] timbre_change ───────────┐
R³[6] harmonic_deviation ───────┼──► Plasticity Magnitude (f03)
R³[15] spectral_flatness ──────┘   Degree of cortical reorganization
                                    triggered by novel timbre patterns

R³[17] spectral_autocorrelation ┐
R³[16] spectral_rolloff ────────┼──► Template Strength
R³[14] tonalness ───────────────┘   Quality of stored timbre template
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

TSCP requires H³ features at three TPC horizons: H2 (17.4ms), H5 (46.4ms), H8 (300ms).
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

**Total TSCP H³ demand**: 12 tuples of 2304 theoretical = 0.52%

### 5.2 TPC Mechanism Binding

TSCP reads from the **TPC** (Timbre Processing Chain) mechanism:

| TPC Sub-section | Range | TSCP Role | Weight |
|-----------------|-------|-----------|--------|
| **Spectral Envelope** | TPC[0:10] | Spectral decomposition of instrument timbre | 0.8 |
| **Instrument Identity** | TPC[10:20] | Instrument-specific encoding — template matching | **1.0** (primary) |
| **Plasticity Markers** | TPC[20:30] | Training-dependent cortical enhancement markers | **0.9** |

TSCP does NOT read from PPC — timbre-specific plasticity operates on spectral envelope processing, not pitch/consonance encoding.

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
TSCP OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                        │ Range  │ Neuroscience Basis
────┼─────────────────────────────┼────────┼────────────────────────────────
 0  │ f01_trained_timbre_response │ [0, 1] │ Trained instrument cortical
    │                             │        │ enhancement. N1m amplitude for
    │                             │        │ trained timbre.
    │                             │        │ f01 = σ(0.35 * trist_balance
    │                             │        │   * mean(TPC.instrument_id)
    │                             │        │ + 0.35 * (1-inharm) * tonalness
    │                             │        │ + 0.30 * mean(TPC.spec_env))
────┼─────────────────────────────┼────────┼────────────────────────────────
 1  │ f02_timbre_specificity      │ [0, 1] │ Selectivity index: trained vs
    │                             │        │ untrained instrument response
    │                             │        │ ratio. Specificity of plasticity.
    │                             │        │ f02 = σ(0.40 * warmth
    │                             │        │   * sharpness_inv
    │                             │        │   * mean(TPC.plasticity)
    │                             │        │ + 0.30 * timbre_stability
    │                             │        │ + 0.30 * x_l5l7_mean)
────┼─────────────────────────────┼────────┼────────────────────────────────
 2  │ f03_plasticity_magnitude    │ [0, 1] │ Degree of cortical reorganization.
    │                             │        │ Training effect size proxy.
    │                             │        │ f03 = σ(0.50 * f01
    │                             │        │   * timbre_change_std
    │                             │        │ + 0.50 * mean(TPC.plasticity))

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                        │ Range  │ Neuroscience Basis
────┼─────────────────────────────┼────────┼────────────────────────────────
 3  │ enhancement_function        │ [0, 1] │ Enhancement(timbre) selectivity
    │                             │        │ function. Ratio of trained to
    │                             │        │ untrained instrument response.
    │                             │        │ E(t) = f01 * f02

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                        │ Range  │ Neuroscience Basis
────┼─────────────────────────────┼────────┼────────────────────────────────
 4  │ recognition_quality         │ [0, 1] │ Template matching quality.
    │                             │        │ TPC.instrument_identity
    │                             │        │ aggregation — how well the
    │                             │        │ current timbre matches stored
    │                             │        │ instrument templates.
────┼─────────────────────────────┼────────┼────────────────────────────────
 5  │ enhanced_response           │ [0, 1] │ Training-dependent cortical
    │                             │        │ response enhancement. ATT-like
    │                             │        │ instrument-focused processing
    │                             │        │ via TPC.plasticity_markers.
────┼─────────────────────────────┼────────┼────────────────────────────────
 6  │ timbre_identity             │ [0, 1] │ Feature binding strength.
    │                             │        │ Coherence of spectral envelope,
    │                             │        │ tristimulus, and temporal
    │                             │        │ envelope into unified identity.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                        │ Range  │ Neuroscience Basis
────┼─────────────────────────────┼────────┼────────────────────────────────
 7  │ timbre_continuation         │ [0, 1] │ Note-by-note timbre prediction.
    │                             │        │ H³ trend-based expectation of
    │                             │        │ upcoming timbre characteristics.
────┼─────────────────────────────┼────────┼────────────────────────────────
 8  │ cortical_enhancement_pred   │ [0, 1] │ Long-term plasticity prediction.
    │                             │        │ ATT x practice accumulation —
    │                             │        │ expected enhancement trajectory.
────┼─────────────────────────────┼────────┼────────────────────────────────
 9  │ generalization_pred         │ [0, 1] │ Transfer to related timbres.
    │                             │        │ How much trained instrument
    │                             │        │ enhancement generalizes to
    │                             │        │ acoustically similar timbres.

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
f01 = σ(0.35 * trist_balance * mean(TPC.instrument_identity[10:20])
       + 0.35 * (1 - R³.inharmonicity[5]) * R³.tonalness[14]
       + 0.30 * mean(TPC.spectral_envelope[0:10]))
# 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Timbre Specificity
# Warmth/sharpness contrast × plasticity × temporal stability
sharpness_inv = 1.0 - R³.sharpness[13]
timbre_stability = H³[(14, 8, 19, 0)]   # tonalness stability 300ms fwd
x_l5l7_mean = mean(R³.x_l5l7[41:47])
f02 = σ(0.40 * R³.warmth[12] * sharpness_inv * mean(TPC.plasticity_markers[20:30])
       + 0.30 * timbre_stability
       + 0.30 * x_l5l7_mean)
# 0.40 + 0.30 + 0.30 = 1.0 ✓

# f03: Plasticity Magnitude
# Trained response × timbre change variability × plasticity markers
timbre_change_std = H³[(24, 8, 3, 0)]   # timbre_change std 300ms fwd
f03 = σ(0.50 * f01 * timbre_change_std
       + 0.50 * mean(TPC.plasticity_markers[20:30]))
# 0.50 + 0.50 = 1.0 ✓

# ═══ LAYER M: Mathematical ═══

# Enhancement selectivity function
enhancement_function = f01 * f02

# ═══ LAYER P: Present ═══

# Recognition quality — template matching via instrument identity
recognition_quality = mean(TPC.instrument_identity[10:20])

# Enhanced response — plasticity-driven cortical enhancement
enhanced_response = σ(0.60 * mean(TPC.plasticity_markers[20:30])
                     + 0.40 * R³.tonalness[14])
# 0.60 + 0.40 = 1.0 ✓

# Timbre identity — feature binding coherence
timbre_identity = σ(0.40 * trist_balance
                   + 0.30 * (1 - R³.inharmonicity[5])
                   + 0.30 * R³.spectral_autocorrelation[17])
# 0.40 + 0.30 + 0.30 = 1.0 ✓

# ═══ LAYER F: Future ═══

# Timbre continuation — note-by-note prediction from H³ trends
timbre_continuation = σ(0.50 * H³[(12, 5, 1, 0)]   # warmth mean 46ms
                       + 0.50 * H³[(14, 5, 1, 0)])  # tonalness mean 46ms
# 0.50 + 0.50 = 1.0 ✓

# Cortical enhancement prediction — long-range plasticity trajectory
cortical_enhancement_pred = σ(0.60 * f03
                             + 0.40 * H³[(24, 8, 1, 0)])  # timbre_change mean 300ms
# 0.60 + 0.40 = 1.0 ✓

# Generalization prediction — transfer to related timbres
generalization_pred = σ(0.50 * recognition_quality
                       + 0.30 * H³[(41, 8, 0, 2)]   # x_l5l7[0] value 300ms
                       + 0.20 * timbre_identity)
# 0.50 + 0.30 + 0.20 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Evidence Type | TSCP Function |
|--------|-----------------|---------------|---------------|
| **Auditory Cortex (bilateral)** | ±50, -20, 8 | Direct (MEG N1m) | Timbre-specific plasticity — enhanced N1m for trained instrument |
| **Planum Temporale** | ±50, -24, 8 | Direct (MEG source) | Spectral processing — template-based timbre analysis |
| **BA22 (Auditory Association)** | ±60, -30, 8 | Indirect | Auditory association — generalization and timbre identity |

---

## 9. Cross-Unit Pathways

### 9.1 TSCP <-> Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TSCP INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (SPU):                                                         │
│  BCH.f02_harmonicity ─────► TSCP (instrument recognition baseline)         │
│      BCH provides the harmonic template that TSCP's timbre encoding        │
│      builds upon. Without brainstem harmonicity, cortical timbre            │
│      specificity has no foundation.                                         │
│                                                                             │
│  PCCR.chroma_tuning ──────► TSCP (octave-invariant identity)              │
│      Chroma processing ensures that timbre identity generalizes            │
│      across octaves — a violin in any register is still a violin.          │
│                                                                             │
│  TSCP.timbre_identity ────► MIAA (imagery template)                       │
│      TSCP's bound timbre representation serves as the template             │
│      for auditory mental imagery — imagining an instrument's sound.        │
│                                                                             │
│  TSCP.plasticity ─────────► ESME (expertise MMN)                          │
│      TSCP's plasticity magnitude feeds into expertise-dependent            │
│      mismatch negativity — musicians detect timbre deviants faster.        │
│                                                                             │
│  CROSS-UNIT (potential):                                                   │
│  TSCP.timbre_identity ────► ARU (timbre-specific emotional response)      │
│      Familiar instrument timbres may enhance affective resonance           │
│      through recognition-mediated pleasure (mere exposure effect).         │
│                                                                             │
│  TSCP.recognition_quality ► IMU (timbre-based memory encoding)            │
│      Better timbre recognition may strengthen episodic encoding of         │
│      musical passages through distinctiveness-based binding.                │
│                                                                             │
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
    Reads: TPC mechanism (30D), R³ direct.
    """
    NAME = "TSCP"
    UNIT = "SPU"
    TIER = "β2"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("TPC",)        # Primary mechanism

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """12 tuples for TSCP computation."""
        return [
            # (r3_idx, horizon, morph, law)
            (12, 2, 0, 2),    # warmth, 17ms, value, bidirectional
            (12, 5, 1, 0),    # warmth, 46ms, mean, forward
            (13, 2, 0, 2),    # sharpness, 17ms, value, bidirectional
            (14, 5, 1, 0),    # tonalness, 46ms, mean, forward
            (14, 8, 19, 0),   # tonalness, 300ms, stability, forward
            (18, 2, 0, 2),    # tristimulus1, 17ms, value, bidirectional
            (19, 2, 0, 2),    # tristimulus2, 17ms, value, bidirectional
            (20, 2, 0, 2),    # tristimulus3, 17ms, value, bidirectional
            (5, 5, 0, 2),     # inharmonicity, 46ms, value, bidirectional
            (24, 8, 1, 0),    # timbre_change, 300ms, mean, forward
            (24, 8, 3, 0),    # timbre_change, 300ms, std, forward
            (41, 8, 0, 2),    # x_l5l7[0], 300ms, value, bidirectional
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute TSCP 10D output.

        Args:
            mechanism_outputs: {"TPC": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) TSCP output
        """
        tpc = mechanism_outputs["TPC"]    # (B, T, 30)

        # R³ features
        inharmonicity = r3[..., 5:6]
        warmth = r3[..., 12:13]
        sharpness = r3[..., 13:14]
        tonalness = r3[..., 14:15]
        spectral_autocorr = r3[..., 17:18]
        trist1 = r3[..., 18:19]
        trist2 = r3[..., 19:20]
        trist3 = r3[..., 20:21]
        x_l5l7 = r3[..., 41:47]          # (B, T, 6) partial

        # TPC sub-sections
        tpc_spectral = tpc[..., 0:10]     # spectral envelope
        tpc_instrument = tpc[..., 10:20]  # instrument identity
        tpc_plasticity = tpc[..., 20:30]  # plasticity markers

        # H³ features
        timbre_stability = h3_direct[(14, 8, 19, 0)]   # tonalness stability 300ms
        timbre_change_std = h3_direct[(24, 8, 3, 0)]    # timbre_change std 300ms
        warmth_mean_46 = h3_direct[(12, 5, 1, 0)]       # warmth mean 46ms
        tonalness_mean_46 = h3_direct[(14, 5, 1, 0)]    # tonalness mean 46ms
        timbre_change_mean = h3_direct[(24, 8, 1, 0)]   # timbre_change mean 300ms
        x_l5l7_300 = h3_direct[(41, 8, 0, 2)]           # x_l5l7[0] value 300ms

        # ═══ Derived quantities ═══
        trist_balance = 1.0 - torch.std(
            torch.cat([trist1, trist2, trist3], dim=-1),
            dim=-1, keepdim=True
        )
        sharpness_inv = 1.0 - sharpness
        x_l5l7_mean = x_l5l7.mean(-1, keepdim=True)

        # ═══ LAYER E: Explicit features ═══
        f01 = torch.sigmoid(
            0.35 * (trist_balance * tpc_instrument.mean(-1, keepdim=True))
            + 0.35 * ((1.0 - inharmonicity) * tonalness)
            + 0.30 * tpc_spectral.mean(-1, keepdim=True)
        )
        f02 = torch.sigmoid(
            0.40 * (warmth * sharpness_inv
                    * tpc_plasticity.mean(-1, keepdim=True))
            + 0.30 * timbre_stability.unsqueeze(-1)
            + 0.30 * x_l5l7_mean
        )
        f03 = torch.sigmoid(
            0.50 * (f01 * timbre_change_std.unsqueeze(-1))
            + 0.50 * tpc_plasticity.mean(-1, keepdim=True)
        )

        # ═══ LAYER M: Mathematical ═══
        enhancement_function = f01 * f02

        # ═══ LAYER P: Present ═══
        recognition_quality = tpc_instrument.mean(-1, keepdim=True)
        enhanced_response = torch.sigmoid(
            0.60 * tpc_plasticity.mean(-1, keepdim=True)
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
            f01, f02, f03,                                     # E: 3D
            enhancement_function,                               # M: 1D
            recognition_quality, enhanced_response,
            timbre_identity,                                    # P: 3D
            timbre_continuation, cortical_enhancement_pred,
            generalization_pred,                                # F: 3D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 | Primary evidence (Pantev et al. 2001) |
| **Effect Sizes** | Significant (p < 0.01) | Pantev 2001 (MEG N1m) |
| **Evidence Modality** | MEG (N1m dipole moments) | Direct neural |
| **Falsification Tests** | 3/6 confirmed | Moderate validity |
| **R³ Features Used** | ~18D of 49D | Timbre-focused |
| **H³ Demand** | 12 tuples (0.52%) | Sparse, efficient |
| **TPC Mechanism** | 30D (3 sub-sections) | Full coverage |
| **Output Dimensions** | **10D** | 4-layer structure |

---

## 13. Scientific References

1. **Pantev, C., Roberts, L. E., Schulz, M., Engelien, A., & Ross, B. (2001)**. Timbre-specific enhancement of auditory cortical representations in musicians. *NeuroReport*, 12(1), 169-174.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Output dimensions | 11D | **10D** (removed 1 redundant output) |
| Temporal | HC⁰ mechanisms (ATT, HRM, EFC, BND) | TPC mechanism (30D) |
| Timbre response | S⁰.tristimulus[68:71] x HC⁰.HRM | R³.tristimulus[18:21] x TPC.instrument_identity |
| Specificity | S⁰.spectral_contrast[53] x HC⁰.ATT | R³.warmth[12] x R³.sharpness[13] x TPC.plasticity |
| Plasticity | S⁰.attack_time[50] x HC⁰.EFC | f01 x H³.timbre_change_std x TPC.plasticity |
| Template | S⁰.X_L5L6[208:216] x HC⁰.BND | R³.x_l5l7[41:47] x TPC.instrument_identity |
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

### Why TPC replaces HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (ATT, HRM, EFC, BND). In MI, these are unified into the TPC mechanism with 3 sub-sections:
- **HRM + BND → TPC.spectral_envelope** [0:10]: Template storage + feature binding = spectral decomposition
- **ATT + HRM → TPC.instrument_identity** [10:20]: Attention gating + replay = instrument encoding
- **EFC + ATT → TPC.plasticity_markers** [20:30]: Efference copy + attention = plasticity tracking

### Why 10D instead of 11D

The legacy v1.0.0 had separate `f04_template_strength` (Explicit) and `recognition_quality` (Present) outputs that were highly correlated (both derived from template matching via HRM/BND). In MI v2.0.0, these are merged: `recognition_quality` in Layer P now subsumes the old `f04` role via TPC.instrument_identity aggregation, reducing output from 11D to 10D without information loss.

---

**Model Status**: Validated
**Output Dimensions**: **10D**
**Evidence Tier**: **β (Integrative)**
**Confidence**: **70-90%**
