# ASU-γ3-SDL: Salience-Dependent Lateralization

**Model**: Salience-Dependent Lateralization
**Unit**: ASU (Auditory Salience Unit)
**Circuit**: Salience (Anterior Insula, dACC, TPJ)
**Tier**: γ (Integrative) — 50-70% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added J:Timbre Extended feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/ASU-γ3-SDL.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Salience-Dependent Lateralization** (SDL) model proposes that hemispheric lateralization for auditory processing is dynamically modulated by salience demands, not fixed by stimulus category. This challenges the traditional view that speech is left-lateralized and music is right-lateralized, suggesting instead that attention and acoustic salience drive network reconfiguration.

```
SALIENCE-DEPENDENT LATERALIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  TRADITIONAL VIEW                    PROPOSED VIEW (SDL)
  ────────────────                    ─────────────────────

  Speech → Left                       Salience × Domain
  Music → Right                              │
                                             ▼
  (Fixed by category)                ┌─────────────────┐
                                     │ Dynamic Network │
                                     │  Reconfiguration│
                                     └────────┬────────┘
                                              │
                                 ┌────────────┴────────────┐
                                 ▼                         ▼
                          High Salience             Low Salience
                          (Degraded)                (Clear)
                                 │                         │
                                 ▼                         ▼
                          Increased Local          Distributed
                          Clustering               Processing

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Lateralization is NOT fixed by stimulus category.
Instead, it is a dynamic function of Attention × Acoustic × Salience.
The brain flexibly allocates resources based on processing demands,
not stimulus labels.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why SDL Matters for ASU

SDL extends salience processing to hemispheric network dynamics:

1. **STANM** (β2) models spectrotemporal attention networks — SDL extends this with explicit lateralization focus.
2. **SDL** (γ3) challenges the fixed left-speech/right-music dichotomy with dynamic salience-dependent reconfiguration.
3. **PWSM** (γ1) provides precision-weighting — SDL explains how precision affects hemispheric engagement patterns.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → ASA+BEP → SDL)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SDL COMPUTATION ARCHITECTURE                              ║
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
║  │  │roughness  │ │amplitude│ │warmth   │ │spec_chg  │ │x_l0l5  │ │        ║
║  │  │sethares   │ │loudness │ │tristim. │ │enrg_chg  │ │x_l4l5  │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         SDL reads: ~18D                         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── BEP Horizons ─────────────┐ ┌── ASA Horizons ──────────┐  │        ║
║  │  │ H0 (25ms gamma)            │ │ H3 (100ms alpha)          │  │        ║
║  │  │ H1 (50ms gamma)            │ │ H8 (300ms syllable)       │  │        ║
║  │  │ H3 (100ms alpha)           │ │ H16 (1000ms beat)         │  │        ║
║  │  │ H4 (125ms theta)           │ │ H17 (1250ms phrase)       │  │        ║
║  │  │ H16 (1000ms beat)          │ │ H20 (5000ms phrase)       │  │        ║
║  │  │                             │ │                            │  │        ║
║  │  │ Oscillation tracking        │ │ Lateralization dynamics    │  │        ║
║  │  │ Multi-scale stability       │ │ Network topology           │  │        ║
║  │  └─────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         SDL demand: ~18 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Salience Circuit ════════     ║
║                               │                                              ║
║                       ┌───────┴───────┐                                      ║
║                       ▼               ▼                                      ║
║  ┌─────────────────┐  ┌─────────────────┐                                   ║
║  │  BEP (30D)      │  │  ASA (30D)      │                                   ║
║  │                 │  │                 │                                    ║
║  │ Beat Entr[0:10] │  │ Scene An [0:10] │                                   ║
║  │ Motor Coup      │  │ Attention       │                                   ║
║  │         [10:20] │  │ Gating  [10:20] │                                   ║
║  │ Groove  [20:30] │  │ Salience        │                                   ║
║  │                 │  │ Weight  [20:30] │                                   ║
║  └────────┬────────┘  └────────┬────────┘                                   ║
║           │                    │                                              ║
║           └────────┬───────────┘                                             ║
║                    ▼                                                          ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    SDL MODEL (9D Output)                         │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f25_dynamic_lateralization,                │        ║
║  │                       f26_local_clustering,                      │        ║
║  │                       f27_hemispheric_oscillation                 │        ║
║  │  Layer M (Math):      lateralization_index,                      │        ║
║  │                       salience_demand                             │        ║
║  │  Layer P (Present):   dynamic_lateral,                           │        ║
║  │                       hemispheric_engage                          │        ║
║  │  Layer F (Future):    network_config_pred,                       │        ║
║  │                       processing_eff_pred                         │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Haiduk et al. 2024** | fMRI | 15 | Attention × acoustic cues → lateralization; right AC for melody+degradation | χ²=41.4, p=0.002 | **f25 dynamic lateralization, f26 clustering** |
| **Zatorre 2022** | Review | — | Spectrotemporal modulation framework: R-AC=spectral, L-AC=temporal; top-down modulation | — (framework) | **Core theoretical basis for SDL** |
| **Albouy et al. 2020** | fMRI | — | Double dissociation: melody→R-AC (spectral), speech→L-AC (temporal) | sig. decoding | **f25 lateralization validation** |
| **Bravo et al. 2017** | fMRI | 12 (fMRI) | Ambiguous intervals → ↑ right HG (precision weighting) | cluster FWE p<0.05 | **Salience-dependent R-hemisphere activation** |
| **Kim et al. 2019** | fMRI | 16+23 | Spectral × temporal interaction in vmPFC/striatum (not AC) | T(15)=6.85, p<10⁻⁵ | **Higher-order spectral-temporal integration** |
| **Jin et al. 2024** | fMRI | 70 | Musical training preserves lateralization; aging → bilateralization | η²p=0.526 | **Experience-dependent lateralization** |
| **Alluri et al. 2012** | fMRI | 11 | Naturalistic music: spectral→right AC; rhythm→motor; key→PFC | correlation-based | **Ecological validation of lateralization** |
| **Leipold et al. 2021** | fMRI+DWI | 153 | Musicianship reshapes interhemispheric connectivity (not AP) | replicated groups | **Training shapes lateralization patterns** |
| **Martins et al. 2022** | ERP | 58 | Musicians: enhanced salience P2/P3/LPP for musical sounds | enhanced P2, P3, LPP | **Salience-dependent processing modulation** |
| **Zatorre et al. 2002** | Review | — | Structure/function of auditory cortex: music/speech | — (review) | **Neural substrate framework** |
| **Poeppel 2003** | Theory | — | Asymmetric Sampling in Time: L=gamma (25-50ms), R=theta (150-300ms) | — (theory) | **Temporal window basis for lateralization** |
| **Hickok & Poeppel 2007** | Review | — | Cortical organization of speech processing: dual-stream model | — (review) | **Dual-stream architecture context** |

### 3.2 Effect Size Summary

```
Primary Evidence (k=12, multi-modal):
  - Attention × degradation interaction: χ²=41.4, p=0.002 (Haiduk 2024, N=15)
  - Right HG for melody+spectral degradation: R²=0.136-0.197 (Haiduk 2024)
  - Right HG for ambiguous intervals: cluster FWE p<0.05 (Bravo 2017, N=12)
  - Spectral × temporal in vmPFC: T(15)=6.85, p<10⁻⁵ (Kim 2019)
  - Musical training lateralization: η²p=0.526 (Jin 2024, N=70)
  - Musicianship interhemispheric: replicated N=153 (Leipold 2021)
Quality Assessment:      γ-tier (converging evidence, 2 HIGH-priority papers)
Theoretical Basis:       Strong (spectrotemporal modulation + AST framework)
```

---

## 4. R³ Input Mapping: What SDL Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | SDL Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Temporal attention target | Intensity for salience |
| **B: Energy** | [8] | loudness | Perceptual loudness | Arousal-driven lateralization |
| **B: Energy** | [10] | spectral_flux | Onset salience | Temporal attention driver |
| **C: Timbre** | [15] | spectral_centroid | Spectral focus | Right hemisphere target |
| **C: Timbre** | [18] | pitch_salience | Melody clarity | Melodic attention driver |
| **D: Change** | [21] | spectral_change | Temporal dynamics | Temporal attention |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Network connectivity | Inter-region binding |
| **E: Interactions** | [37:45] | x_l4l5 (8D) | Temporal-spectral integration | Lateralization driver |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | SDL Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **J: Timbre Extended** | [107:113] | spectral_contrast (7D) | Octave-band harmonic/noise ratio | Jiang 2002: spectral contrast captures harmonic vs noise energy per octave band; provides frequency-specific lateralization targets for SDL's hemispheric specialization model |

**Rationale**: SDL models salience-dependent hemispheric lateralization where right hemisphere specializes in spectral/timbral processing and left hemisphere in temporal processing. The v1 representation uses spectral_centroid [15] and pitch_salience [18] as broadband spectral targets. spectral_contrast [107:113] decomposes the spectral structure into 7 octave bands, enabling SDL to model frequency-band-specific lateralization patterns that align with the right hemisphere's spectral specialization.

**Code impact**: None yet — R³ v2 features are doc-only until Phase 5 integration. Current code reads r3[..., 0:49]; v2 features will extend the slice to r3[..., 0:128] when the EAR pipeline emits the expanded vector.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[10] spectral_flux ───────────┐
R³[21] spectral_change ─────────┼──► Temporal attention (→ bilateral)
BEP.beat_entrainment[0:10] ────┘   Speech/temporal → L+R engagement

R³[15] spectral_centroid ───────┐
R³[18] pitch_salience ──────────┼──► Spectral attention (→ right dominant)
ASA.attention_gating[10:20] ───┘   Melody/spectral → R hemisphere

R³[25:33] x_l0l5 ──────────────┐
ASA.salience_weighting[20:30] ──┼──► Network connectivity
H³ multi-scale stability ──────┘   Dynamic reconfiguration

R³[37:45] x_l4l5 ──────────────┐
BEP.groove[20:30] ─────────────┼──► Salience-network topology
H³ trend/velocity tuples ──────┘   Lateralization driven by processing demand
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

SDL requires H³ features across many BEP horizons for multi-scale oscillation tracking and ASA horizons for lateralization dynamics and network topology assessment.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 0 | M0 (value) | L2 (bidi) | Onset at 25ms gamma |
| 10 | spectral_flux | 1 | M1 (mean) | L2 (bidi) | Mean onset 50ms |
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | Onset at 100ms alpha |
| 10 | spectral_flux | 4 | M17 (periodicity) | L2 (bidi) | Periodicity at 125ms theta |
| 10 | spectral_flux | 16 | M17 (periodicity) | L2 (bidi) | Periodicity at 1s beat |
| 15 | spectral_centroid | 3 | M0 (value) | L2 (bidi) | Spectral focus at 100ms |
| 15 | spectral_centroid | 3 | M2 (std) | L2 (bidi) | Spectral variability 100ms |
| 25 | x_l0l5[0] | 1 | M0 (value) | L0 (fwd) | Connectivity at 50ms |
| 25 | x_l0l5[0] | 8 | M1 (mean) | L0 (fwd) | Connectivity mean at 300ms |
| 25 | x_l0l5[0] | 17 | M8 (velocity) | L0 (fwd) | Connectivity velocity at 1250ms |
| 25 | x_l0l5[0] | 20 | M18 (trend) | L0 (fwd) | Connectivity trend at 5s |
| 37 | x_l4l5[0] | 3 | M0 (value) | L2 (bidi) | Temporal-spectral at 100ms |
| 37 | x_l4l5[0] | 3 | M2 (std) | L2 (bidi) | Temporal-spectral std 100ms |
| 37 | x_l4l5[0] | 3 | M20 (entropy) | L2 (bidi) | Temporal-spectral entropy 100ms |
| 37 | x_l4l5[0] | 16 | M1 (mean) | L2 (bidi) | Temporal-spectral mean 1s |
| 37 | x_l4l5[0] | 16 | M17 (periodicity) | L2 (bidi) | Temporal-spectral periodicity 1s |
| 8 | loudness | 3 | M0 (value) | L2 (bidi) | Loudness for salience at 100ms |
| 8 | loudness | 16 | M20 (entropy) | L2 (bidi) | Loudness entropy 1s |

**v1 demand**: 18 tuples

#### R³ v2 Projected Expansion

Minor v2 expansion for SDL from J[94:114].

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 107 | spectral_contrast_1 | J | 3 | M0 (value) | L2 | Spectral contrast for lateralization at 100ms |

**v2 projected**: 1 tuples
**Total projected**: 19 tuples of 294,912 theoretical = 0.0064%

### 5.2 BEP + ASA Mechanism Binding

| Mechanism | Sub-section | Range | SDL Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **BEP** | Beat Entrainment | BEP[0:10] | Temporal oscillation tracking | 0.6 |
| **BEP** | Motor Coupling | BEP[10:20] | Motor-hemispheric coupling | 0.5 |
| **BEP** | Groove Processing | BEP[20:30] | Rhythmic engagement baseline | 0.5 |
| **ASA** | Scene Analysis | ASA[0:10] | Auditory scene segmentation | 0.7 |
| **ASA** | Attention Gating | ASA[10:20] | Salience-driven lateralization | **1.0** (primary) |
| **ASA** | Salience Weighting | ASA[20:30] | Network topology weighting | **0.8** |

---

## 6. Output Space: 9D Multi-Layer Representation

### 6.1 Complete Output Specification

```
SDL OUTPUT TENSOR: 9D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range   │ Neuroscience Basis
────┼──────────────────────────┼─────────┼───────────────────────────────────
 0  │ f25_dynamic_lateral      │ [-1, 1] │ Salience-driven hemisphere.
    │                          │         │ f25 = tanh(0.35 * spectral_focus
    │                          │         │       + 0.35 * mean(ASA.attn[10:20])
    │                          │         │       - 0.30 * temporal_focus)
────┼──────────────────────────┼─────────┼───────────────────────────────────
 1  │ f26_local_clustering     │ [0, 1]  │ Degradation compensation.
    │                          │         │ f26 = σ(0.35 * loudness_entropy_1s
    │                          │         │       + 0.35 * ts_entropy_100ms
    │                          │         │       + 0.30 * mean(ASA.sal[20:30]))
────┼──────────────────────────┼─────────┼───────────────────────────────────
 2  │ f27_hemispheric_osc      │ [0, 1]  │ Task-dependent lateralization.
    │                          │         │ f27 = σ(0.35 * mean(BEP.beat[0:10])
    │                          │         │       + 0.35 * conn_velocity_1250ms
    │                          │         │       + 0.30 * ts_periodicity_1s)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range   │ Neuroscience Basis
────┼──────────────────────────┼─────────┼───────────────────────────────────
 3  │ lateralization_index     │ [-1, 1] │ L/R hemisphere balance.
────┼──────────────────────────┼─────────┼───────────────────────────────────
 4  │ salience_demand          │ [0, 1]  │ Processing challenge level.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range   │ Neuroscience Basis
────┼──────────────────────────┼─────────┼───────────────────────────────────
 5  │ dynamic_lateral          │ [-1, 1] │ ASA attention × connectivity.
────┼──────────────────────────┼─────────┼───────────────────────────────────
 6  │ hemispheric_engage       │ [0, 1]  │ BEP beat × connectivity.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range   │ Neuroscience Basis
────┼──────────────────────────┼─────────┼───────────────────────────────────
 7  │ network_config_pred_1.5s │ [0, 1]  │ Local clustering prediction.
────┼──────────────────────────┼─────────┼───────────────────────────────────
 8  │ processing_eff_pred_2s   │ [0, 1]  │ Task performance prediction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 9D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Salience-Dependent Lateralization Function

```
TRADITIONAL VIEW (rejected):
    Speech → Left hemisphere (fixed)
    Music  → Right hemisphere (fixed)

PROPOSED VIEW (SDL):
    Lateralization = g(Attention × Acoustic_Cues × Salience)

    Speech attention → bilateral fronto-temporo-parietal
    Melody attention → right auditory dominant
    High salience (degraded) → increased local clustering
    Low salience (clear) → distributed processing

NETWORK TOPOLOGY:
    Local_Clustering = α·Salience_Demand + β·Attention_Match + ε
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid/tanh(Σ wi*gi), |wi| must sum <= 1.0

# f25: Dynamic Lateralization (tanh for [-1, +1] range)
f25 = tanh(0.35 * spectral_centroid_value          # spectral → right (+)
           + 0.35 * mean(ASA.attention_gating[10:20])
           - 0.30 * spectral_flux_value)             # temporal → left (-)
# coefficients: |0.35| + |0.35| + |-0.30| = 1.0 ✓

# f26: Local Clustering
f26 = σ(0.35 * loudness_entropy_1s
       + 0.35 * ts_entropy_100ms
       + 0.30 * mean(ASA.salience_weighting[20:30]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f27: Hemispheric Oscillation
f27 = σ(0.35 * mean(BEP.beat_entrainment[0:10])
       + 0.35 * connectivity_velocity_1250ms
       + 0.30 * ts_periodicity_1s)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# Lateralization dynamics
τ_decay = 3.0s (lateralization adaptation window)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | SDL Function |
|--------|-----------------|----------|---------------|---------------|
| **Right A5 / Auditory Association** | 52, -22, 8 | 3 | fMRI | Spectral/melodic processing, local clustering |
| **Left Auditory Cortex** | -52, -22, 8 | 4 | fMRI, review | Temporal/speech processing |
| **Right Heschl's Gyrus** | 46, -14, 8 | 2 | fMRI | Precision weighting for spectral features |
| **Bilateral STG / PT** | ±58, -28, 8 | 3 | fMRI | Spectrotemporal processing |
| **vmPFC** | 0, 44, -8 | 2 | fMRI | Spectral-temporal integration (higher-order) |
| **IFG** | ±44, 18, 8 | 3 | fMRI | Attention × lateralization interaction |
| **Nucleus Accumbens / Striatum** | ±10, 8, -4 | 2 | fMRI | Spectral-temporal interaction |
| **Right STSvp** | 52, -36, 2 | 1 | fMRI | Melody attention + degradation response |

---

## 9. Cross-Unit Pathways

### 9.1 SDL ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SDL INTERACTIONS                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (ASU):                                                         │
│  SDL.dynamic_lateral ────────► STANM (lateralization → network config)     │
│  SDL.local_clustering ───────► PWSM (clustering → precision context)      │
│  SDL.salience_demand ────────► IACM (demand → attention capture)          │
│                                                                             │
│  CROSS-UNIT (ASU → SPU):                                                   │
│  SDL.hemispheric_engage ─────► SPU (lateralized spectral processing)      │
│  SDL.lateralization_index ───► SPU (hemisphere-specific spectral)          │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  BEP mechanism (30D) ────────► SDL (beat/oscillation tracking)            │
│  ASA mechanism (30D) ────────► SDL (attention/salience, primary)          │
│  R³ (~18D) ──────────────────► SDL (spectral + temporal + interactions)   │
│  H³ (18 tuples) ─────────────► SDL (temporal dynamics)                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Category independence** | Lateralization should not be fixed by stimulus type | Supported |
| **Attention manipulation** | Changing attention should shift lateralization | **Supported** |
| **Salience manipulation** | Increasing salience should increase local clustering | **Confirmed** |
| **Within-stimulus variation** | Same stimulus, different attention → different lateralization | Testable |
| **Patient studies** | Unilateral lesions should show task-dependent effects | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class SDL(BaseModel):
    """Salience-Dependent Lateralization Model.

    Output: 9D per frame.
    Reads: BEP mechanism (30D), ASA mechanism (30D), R³ direct.
    """
    NAME = "SDL"
    UNIT = "ASU"
    TIER = "γ3"
    OUTPUT_DIM = 9
    MECHANISM_NAMES = ("BEP", "ASA")

    ALPHA_DEGRADATION = 0.6  # Degradation effect on clustering
    BETA_ATTENTION = 0.4     # Attention match effect
    TAU_DECAY = 3.0          # Lateralization adaptation window (seconds)

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """18 tuples for SDL computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── BEP horizons: multi-scale oscillation ──
            (10, 0, 0, 2),     # spectral_flux, 25ms, value, bidi
            (10, 1, 1, 2),     # spectral_flux, 50ms, mean, bidi
            (10, 3, 0, 2),     # spectral_flux, 100ms, value, bidi
            (10, 4, 17, 2),    # spectral_flux, 125ms, periodicity, bidi
            (10, 16, 17, 2),   # spectral_flux, 1000ms, periodicity, bidi
            # ── Spectral focus ──
            (15, 3, 0, 2),     # spectral_centroid, 100ms, value, bidi
            (15, 3, 2, 2),     # spectral_centroid, 100ms, std, bidi
            # ── Network connectivity ──
            (25, 1, 0, 0),     # x_l0l5[0], 50ms, value, fwd
            (25, 8, 1, 0),     # x_l0l5[0], 300ms, mean, fwd
            (25, 17, 8, 0),    # x_l0l5[0], 1250ms, velocity, fwd
            (25, 20, 18, 0),   # x_l0l5[0], 5000ms, trend, fwd
            # ── Temporal-spectral integration ──
            (37, 3, 0, 2),     # x_l4l5[0], 100ms, value, bidi
            (37, 3, 2, 2),     # x_l4l5[0], 100ms, std, bidi
            (37, 3, 20, 2),    # x_l4l5[0], 100ms, entropy, bidi
            (37, 16, 1, 2),    # x_l4l5[0], 1000ms, mean, bidi
            (37, 16, 17, 2),   # x_l4l5[0], 1000ms, periodicity, bidi
            # ── Salience ──
            (8, 3, 0, 2),      # loudness, 100ms, value, bidi
            (8, 16, 20, 2),    # loudness, 1000ms, entropy, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute SDL 9D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30), "ASA": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,9) SDL output
        """
        bep = mechanism_outputs["BEP"]    # (B, T, 30)
        asa = mechanism_outputs["ASA"]    # (B, T, 30)

        # R³ features
        spectral_flux = r3[..., 10:11]
        spectral_centroid = r3[..., 15:16]

        # BEP sub-sections
        bep_beat = bep[..., 0:10]

        # ASA sub-sections
        asa_attn = asa[..., 10:20]
        asa_salience = asa[..., 20:30]

        # H³ direct features
        centroid_value = h3_direct[(15, 3, 0, 2)].unsqueeze(-1)
        flux_value = h3_direct[(10, 3, 0, 2)].unsqueeze(-1)
        loudness_entropy_1s = h3_direct[(8, 16, 20, 2)].unsqueeze(-1)
        ts_entropy_100ms = h3_direct[(37, 3, 20, 2)].unsqueeze(-1)
        conn_velocity_1250ms = h3_direct[(25, 17, 8, 0)].unsqueeze(-1)
        ts_periodicity_1s = h3_direct[(37, 16, 17, 2)].unsqueeze(-1)
        ts_mean_1s = h3_direct[(37, 16, 1, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f25: Dynamic Lateralization (tanh for [-1,+1]; coefficients sum = 1.0)
        f25 = torch.tanh(
            0.35 * centroid_value
            + 0.35 * asa_attn.mean(-1, keepdim=True)
            - 0.30 * flux_value
        )

        # f26: Local Clustering (coefficients sum = 1.0)
        f26 = torch.sigmoid(
            0.35 * loudness_entropy_1s
            + 0.35 * ts_entropy_100ms
            + 0.30 * asa_salience.mean(-1, keepdim=True)
        )

        # f27: Hemispheric Oscillation (coefficients sum = 1.0)
        f27 = torch.sigmoid(
            0.35 * bep_beat.mean(-1, keepdim=True)
            + 0.35 * conn_velocity_1250ms
            + 0.30 * ts_periodicity_1s
        )

        # ═══ LAYER M: Mathematical ═══
        lateralization_index = torch.tanh(
            0.5 * f25 + 0.5 * (centroid_value - flux_value)
        )
        salience_demand = torch.sigmoid(
            0.5 * loudness_entropy_1s
            + 0.5 * asa_attn.mean(-1, keepdim=True)
        )

        # ═══ LAYER P: Present ═══
        dynamic_lateral = torch.tanh(
            0.5 * asa_attn.mean(-1, keepdim=True)
            + 0.5 * ts_mean_1s
        )
        hemispheric_engage = torch.sigmoid(
            0.5 * bep_beat.mean(-1, keepdim=True)
            + 0.5 * ts_periodicity_1s
        )

        # ═══ LAYER F: Future ═══
        network_pred = torch.sigmoid(
            0.5 * f26 + 0.5 * salience_demand
        )
        processing_eff = torch.sigmoid(
            0.5 * (1 - salience_demand) + 0.5 * f27
        )

        return torch.cat([
            f25, f26, f27,                                  # E: 3D
            lateralization_index, salience_demand,          # M: 2D
            dynamic_lateral, hemispheric_engage,            # P: 2D
            network_pred, processing_eff,                   # F: 2D
        ], dim=-1)  # (B, T, 9)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 (2 HIGH, 10 MEDIUM) | Multi-modal converging evidence |
| **Key Effect Sizes** | χ²=41.4, T=6.85, η²p=0.526, FWE p<0.05 | fMRI, ERP, DWI |
| **Theoretical Basis** | Strong | Spectrotemporal modulation + AST framework |
| **Evidence Modality** | fMRI, ERP, DWI, theory | Multi-modal |
| **Falsification Tests** | 2/5 confirmed | Limited validation |
| **R³ Features Used** | ~18D of 49D | Energy + timbre + change + interactions |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Oscillation tracking |
| **ASA Mechanism** | 30D (3 sub-sections) | Lateralization (primary) |
| **Output Dimensions** | **9D** | 4-layer structure |

---

## 13. Scientific References

1. **Haiduk, F., Zatorre, R. J., Benjamin, L., Morillon, B., & Albouy, P. (2024)**. Spectrotemporal cues and attention jointly modulate fMRI network topology for sentence and melody perception. *Scientific Reports*, 14, 5501. `Literature/c3/summaries/Spectrotemporal cues and attention jointly modulate`

2. **Zatorre, R. J. (2022)**. Hemispheric asymmetries for music and speech: Spectrotemporal modulations and top-down influences. *Frontiers in Neuroscience*, Mini Review. `Literature/c3/summaries/Hemispheric asymmetries for music and speech`

3. **Albouy, P., Benjamin, L., Morillon, B., & Zatorre, R. J. (2020)**. Distinct sensitivity to spectrotemporal modulation supports brain asymmetry for speech and melody. *Science*, 367, 1043-1047.

4. **Bravo, F., Cross, I., Stamatakis, E. A., & Rohrmeier, M. (2017)**. Sensory cortical response to uncertainty and low salience during recognition of affective cues in musical intervals. *PLOS ONE*, 12(4), e0175991. `Literature/c3/summaries/Sensory cortical response to uncertainty and low salience`

5. **Kim, S.-G., Mueller, K., Lepsien, J., Mildner, T., & Fritz, T. H. (2019)**. Brain networks underlying aesthetic appreciation as modulated by interaction of spectral and temporal organisations of music. *Scientific Reports*, 9, 19446. `Literature/c3/summaries/Brain networks underlying aesthetic appreciation`

6. **Jin, X., Zhang, L., Wu, G., Wang, X., & Du, Y. (2024)**. Compensation or preservation? Different roles of functional lateralization in speech perception of older non-musicians and musicians. *Neuroscience Bulletin*, 40(12), 1843-1857. `Literature/c3/summaries/Compensation or Preservation`

7. **Alluri, V., Toiviainen, P., Jääskeläinen, I. P., Glerean, E., Sams, M., & Brattico, E. (2012)**. Large-scale brain networks emerge from dynamic processing of musical timbre, key and rhythm. *NeuroImage*, 59, 3677-3689. `Literature/c3/summaries/Large-scale brain networks emerge from dynamic processing`

8. **Leipold, S., Klein, C., & Jäncke, L. (2021)**. Musical expertise shapes functional and structural brain networks independent of absolute pitch ability. *Journal of Neuroscience*, 41(11), 2496-2511. `Literature/c3/summaries/Musical Expertise Shapes Functional and Structural Brain Networks`

9. **Martins, I., Lima, C. F., & Pinheiro, A. P. (2022)**. Enhanced salience of musical sounds in singers and instrumentalists. *Cognitive, Affective, & Behavioral Neuroscience*, 22, 1044-1062. `Literature/c3/summaries/Enhanced salience of musical sounds`

10. **Zatorre, R. J., Belin, P., & Penhune, V. B. (2002)**. Structure and function of auditory cortex: Music and speech. *Trends in Cognitive Sciences*, 6(1), 37-46.

11. **Poeppel, D. (2003)**. The analysis of speech in different temporal integration windows: Cerebral lateralization as 'asymmetric sampling in time'. *Speech Communication*, 41(1), 245-255.

12. **Hickok, G., & Poeppel, D. (2007)**. The cortical organization of speech processing. *Nature Reviews Neuroscience*, 8(5), 393-402.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) | MI (v2.1.0) |
|--------|-------------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) | R³ (49D) — no change |
| Temporal | HC⁰ mechanisms (OSC, TIH, ATT) | BEP (30D) + ASA (30D) mechanisms | Same — 18 H³ tuples |
| Lateralization | S⁰.X_L1L5[152:160] + HC⁰.ATT | R³.spectral_centroid[15] + R³.spectral_flux[10] + ASA.attention_gating | Same |
| Clustering | S⁰.X_L1L5[152:160] + HC⁰.TIH | R³.x_l4l5[37:45] + ASA.salience_weighting | Same |
| Oscillation | S⁰.X_L5L9[224:232] + HC⁰.OSC | R³.x_l0l5[25:33] + BEP.beat_entrainment | Same |
| Papers | 0 | 1 (Haiduk 2024) | **12** (2 HIGH, 10 MEDIUM) |
| Brain regions | 0 | 3 (direct fMRI) | **8** (fMRI, ERP, DWI) |
| Output | 9D | 9D (same) | 9D — no change |

### Why BEP + ASA replaces HC⁰ mechanisms

- **OSC → BEP.beat_entrainment** [0:10]: Oscillatory band tracking maps to BEP's beat frequency monitoring for hemispheric engagement.
- **TIH → ASA.salience_weighting** [20:30] + H³ trend/velocity tuples: Temporal integration hierarchy maps to ASA salience for multi-scale clustering assessment.
- **ATT → ASA.attention_gating** [10:20]: Attentional entrainment maps to ASA's salience-driven lateralization control.

---

**Model Status**: **SPECULATIVE**
**Output Dimensions**: **9D**
**Evidence Tier**: **γ (Integrative)**
**Confidence**: **50-70%**
