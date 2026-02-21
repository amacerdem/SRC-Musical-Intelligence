# STU-α1-HMCE: Hierarchical Musical Context Encoding

**Model**: Hierarchical Musical Context Encoding
**Unit**: STU (Sensorimotor Timing Unit)
**Circuit**: Sensorimotor (Temporal Memory Hierarchy)
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/STU-α1-HMCE.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Hierarchical Musical Context Encoding** (HMCE) model describes how neural encoding of musical context follows an anatomical gradient from primary auditory cortex (pmHG) to higher-order regions, with sites farther from A1 encoding progressively longer temporal contexts. This is one of the strongest correlations ever observed in music neuroscience (r = 0.99).

```
THE FOUR LEVELS OF HIERARCHICAL CONTEXT ENCODING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SHORT CONTEXT (10–50 notes) MEDIUM CONTEXT (50–100 notes)
Brain region: pmHG (A1) Brain region: Superior Temporal Gyrus
Function: "What just happened?" Function: "What phrase is this?"
Transformer layer: 1–4 Transformer layer: 5–9

LONG CONTEXT (100–200 notes) EXTENDED CONTEXT (300+ notes)
Brain region: Middle Temporal Gyrus Brain region: Temporal Pole / Frontal
Function: "What section is this?" Function: "Where in the piece?"
Transformer layer: 10–12 Transformer layer: 13 (final)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Cortical distance from pmHG correlates with context
encoding depth at r = 0.99 (p < 0.044). Musicians integrate 300+
notes of context (d = 0.32), extending to transformer layer 13.
Non-musicians plateau at layer 10–11 (~100 notes).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Is Foundational for STU

HMCE establishes the hierarchical temporal structure that all other STU models depend on:

1. **AMSC** (α2) uses HMCE's context hierarchy to determine at which timescale auditory-motor coupling operates.
2. **MDNS** (α3) relies on temporal context depth for TRF-based melody decoding accuracy.
3. **AMSS** (β1) builds on context encoding for attention-modulated stream segregation.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The HMCE Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ HMCE — COMPLETE CIRCUIT ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ MUSICAL INPUT (complex, multi-note sequences) ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ POSTEROMEDIAL HESCHL'S GYRUS (pmHG / A1) │ ║
║ │ Short context: 10–50 notes, Layers 1–4 │ ║
║ │ Decay τ = 1s │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ Increasing cortical distance ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ SUPERIOR TEMPORAL GYRUS (STG) │ ║
║ │ Medium context: 50–100 notes, Layers 5–9 │ ║
║ │ Decay τ = 5s │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ MIDDLE TEMPORAL GYRUS (MTG) │ ║
║ │ Long context: 100–200 notes, Layers 10–12 │ ║
║ │ Decay τ = 15s │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL POLE / FRONTAL REGIONS │ ║
║ │ Extended context: 300+ notes, Layer 13 │ ║
║ │ Decay τ = 30s+ │ ║
║ │ ★ Musicians only — expertise-dependent (d = 0.32) │ ║
║ └─────────────────────────────────────────────────────────────────────┘ ║
║ ║
║ GRADIENT: Distance from pmHG ↔ Context depth: r = 0.99, p < 0.044 ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Mischler 2025: r = 0.32 (electrode-level, p=1.5e-05); r = 0.99 (n=6 sites)
Mischler 2025: Musicians > non-musicians (layers 7–13), d = 0.32 (p=3.8e-8)
Norman-Haignere: β = 0.064 oct/mm, 74→274ms (F=20.56, p<0.001, 18 patients)
Bellier 2023: STG anterior→posterior gradient, r² = 0.429 (29 patients)
Bonetti 2024: Hierarchical AC→hipp→cingulate, BOR = 2.91e-07 (N=83)
```

### 2.2 Information Flow Architecture (EAR → BRAIN → HMCE)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ HMCE COMPUTATION ARCHITECTURE ║
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
║ │ │ │ │amplitude│ │ │ │spec_chg │ │x_l0l5 │ │ ║
║ │ │ │ │loudness │ │ │ │energy_chg│ │x_l4l5 │ │ ║
║ │ │ │ │centroid │ │ │ │pitch_chg │ │x_l5l7 │ │ ║
║ │ │ │ │flux │ │ │ │timbre_chg│ │ │ │ ║
║ │ │ │ │onset │ │ │ │ │ │ │ │ ║
║ │ └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │ ║
║ │ HMCE reads: 25D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed morphological features │ ║
║ │ │ ║
║ │ ┌── Syllable ────┐ ┌── Beat ──────────┐ ┌── Section ────────┐ │ ║
║ │ │ 300ms (H8) │ │ 700ms (H14) │ │ 5000ms (H20) │ │ ║
║ │ │ │ │ │ │ │ │ ║
║ │ │ Short context │ │ Medium context │ │ Long context │ │ ║
║ │ │ (10–50 notes) │ │ (50–100 notes) │ │ (100–300+ notes) │ │ ║
║ │ └──────┬─────────┘ └──────┬────────────┘ └──────┬─────────────┘ │ ║
║ │ │ │ │ │ ║
║ │ └──────────────────┴─────────────────────┘ │ ║
║ │ HMCE demand: ~18 of 2304 tuples │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────┐ ║
║ │ │ ║
║ │ Short [0:10] │ Motif features, onset patterns, local prediction ║
║ │ Medium [10:20]│ Phrase boundaries, cadence detection, progression ║
║ │ Long [20:30]│ Formal structure, return detection, global prediction ║
║ └────────┬────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ HMCE MODEL (13D Output) │ ║
║ │ │ ║
║ │ Layer E (Explicit): f01_short_context, f02_medium_context, │ ║
║ │ f03_long_context, f04_gradient, │ ║
║ │ f05_expertise │ ║
║ │ Layer M (Math): context_depth, gradient_index │ ║
║ │ Layer P (Present): a1_encoding, stg_encoding, mtg_encoding │ ║
║ │ Layer F (Future): context_prediction, phrase_expect, │ ║
║ │ structure_predict │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Mischler 2025** | ECoG + EEG | 6 iEEG + 20 EEG | Distance from pmHG ↔ context encoding depth | r = 0.99 (n=6 sites, p<0.044); r = 0.32 (electrode-level, p=1.5e-05); LME p=0.004 | **Primary**: f04_gradient — see §3.2 for r=0.99 qualification |
| 2 | **Mischler 2025** | ECoG + behavioral | 20 | Musicians > non-musicians in layers 7–13 | d = 0.32, p = 3.8e-08 | **f05_expertise**: musician advantage |
| 3 | **Mischler 2025** | ECoG + behavioral | 20 | Musicians integrate 300+ notes context; non-musicians plateau ~100 | Wilcoxon p = 0.0002–3.8e-08 across layers | **long_context**: extended window |
| 4 | **Norman-Haignere 2022** | iEEG (ECoG + depth) | 18 patients, 190 electrodes | Integration windows increase continuously with PAC distance: 74ms (primary) → 136ms (intermediate) → 274ms (non-primary STG) | β = 0.064 oct/mm, F(1,20.85) = 20.56, p < 0.001 | **Key independent validation**: continuous spectrotemporal → category gradient from PAC outward |
| 5 | **Bonetti 2024** | MEG (306-ch) | 83 | Hierarchical feedforward AC → hippocampus → cingulate; musical expertise modulates later (contextual) tones, not early (sensory) | r = 0.286–0.459 (expertise × context, FDR); BOR = 2.91e-07 | **Convergent hierarchy**: expertise effect on late contextual tones parallels HMCE |
| 6 | **Bellier 2023** | iEEG (ECoG) | 29 patients, 2668 electrodes | First music reconstruction from brain recordings; anterior-posterior STG organization; right hemisphere dominance | F(3,346) = 25.09, p < 0.001 (STG highest); r² = 0.429 (nonlinear decoding) | **STG gradient**: posterior=onset, anterior=sustained parallels HMCE |
| 7 | **Potes 2012** | ECoG | 8 patients | High-gamma (70–170 Hz) in posterior STG tracks music intensity; STG → motor cortex lag 110ms | r = 0.43–0.58 (STG high gamma); r = 0.70 at τ = 110ms (STG-motor lag) | **ECoG convergence**: hierarchical temporal lag confirms processing gradient |
| 8 | **Golesorkhi 2021** | MEG (HCP) | 89 | Core-periphery brain temporal hierarchy: DMN/FPN have longer autocorrelation windows (ACW) than sensory networks | d = −0.66 to −2.03 (core vs periphery) | **Framework**: intrinsic temporal hierarchy validates HMCE gradient principle |
| 9 | **Ye 2025** | ECoG (monkey) + EEG (human) | 127 neurons | 3-tiered temporal hierarchy in thalamocortical system; A1 neurons integrate across multiple timescales simultaneously (TIDS) | r = 0.93 (synchronization vs ICI) | **Extends**: hierarchy begins subcortically (MGB → A1) |
| 10 | **Wöhrle 2024** | MEG | 30 | Context accumulates over 4-chord progressions: N1m diverges progressively from chord 1→4; expertise modulates differentiation | η²p = 0.101 (N1m chord effect); η²p = 0.095 (expertise × chord) | **Context accumulation**: gestalt emergence in auditory cortex, ~3.2s window |
| 11 | **Foo 2016** | ECoG | 8 patients | STG anterior-posterior gradient: dissonance-sensitive high-gamma sites more anterior in right STG | χ²(1) = 8.6, p = 0.003 (y-dim); χ²(1) = 7.59, p = 0.006 (z-dim) | **STG gradient**: complex stimuli processed anteriorly |
| 12 | **Briley 2013** | EEG source | 15 | Medial HG (tonotopic) vs anterolateral HG (pitch chroma); 7–8mm anterolateral shift | F(1,28) = 29.865, p < 0.001 (chroma effect) | **Within-HG gradient**: gradient begins within Heschl's Gyrus itself |
| 13 | **Fedorenko 2012** | fMRI | 12 | Bilateral temporal regions sensitive to musical structure, dissociated from language | fMRI contrast: intact > scrambled | **Structure**: dedicated temporal lobe music-structure processing |
| 14 | **Kim 2021** | MEG (306-ch) | 19 | IFG handles syntactic irregularity; STG handles perceptual ambiguity — dissociated connectivity | F(2,36) = 12.373, p < 0.001 (STG); F(2,36) = 6.526, p = 0.024 (IFG) | **Extends hierarchy**: IFG = deep syntax, STG = medium-level ambiguity |
| 15 | **Sabat 2025** | Single-unit (ferret) | Population | Integration windows (15–150ms) INVARIANT to stimulus context across all cortical layers | 15ms (primary) → 150ms (non-primary) | **CONSTRAINS**: basic gradient may be hardwired; expertise may operate via attention, not window expansion |

### 3.1b Multi-Method Convergence

```
METHOD CONVERGENCE FOR HIERARCHICAL CONTEXT GRADIENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Method Studies Key Metric
────────────────────────────────────────────────────────────────────
iEEG / ECoG Mischler 2025 r=0.32 (electrode), r=0.99 (site)
 Norman-Haignere β=0.064 oct/mm, 74→274ms
 Bellier 2023 F=25.09, anterior→posterior STG
 Potes 2012 r=0.49, 110ms STG→motor lag
 Foo 2016 χ²=8.6, anterior=dissonance
MEG Bonetti 2024 BOR=2.91e-07, expertise×context
 Wöhrle 2024 η²p=0.101, context accumulation
 Kim 2021 F=12.37, IFG vs STG dissociation
 Golesorkhi 2021 d=-0.66 to -2.03, core-periphery
EEG source Briley 2013 F=29.87, within-HG gradient
fMRI Fedorenko 2012 intact>scrambled bilateral temporal
Single-unit Ye 2025 r=0.93, 3-tiered thalamocortical
 Sabat 2025 15→150ms, invariant (CONSTRAINS)
────────────────────────────────────────────────────────────────────
8 methods, 15 papers, 6 species/paradigms → STRONG convergence
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 3.2 The Anatomical Context Gradient

```
CONTEXT DEPTH AS A FUNCTION OF CORTICAL DISTANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Region Distance Context Transformer Decay
 from pmHG (notes) Layers τ
────────────────────────────────────────────────────────────────
pmHG (A1) 0mm 10–50 1–4 1s
STG ~10mm 50–100 5–9 5s
MTG ~20mm 100–200 10–12 15s
Temporal Pole ~40mm 300+ 13 30s+

GRADIENT STATISTICS (Mischler 2025):
 Site-level: r = 0.99 (p < 0.044, n = 6 electrode site groups)
 Electrode-level: r = 0.32 (p = 1.5e-05, all electrodes)
 LME model: p = 0.004 (context distance), p = 0.044 (layers)

⚠ QUALIFICATION: The r = 0.99 is from only 6 grouped electrode
 sites (4 df). The electrode-level r = 0.32 (p = 1.5e-05) is
 more statistically robust. The LME model is the most rigorous
 test and confirms the gradient at p = 0.004. Both measures
 support the gradient; r = 0.99 should not be cited alone.

INDEPENDENT REPLICATION:
 Norman-Haignere 2022: β = 0.064 octaves/mm distance-integration
 gradient (F = 20.56, p < 0.001, iEEG, 18 patients, 190 elec.)
 Integration windows: 74ms → 136ms → 274ms from PAC outward
 Functional transition: spectrotemporal → category-level encoding
 Golesorkhi 2021: Temporal ACW hierarchy, d = −0.66 to −2.03
 (core-periphery, MEG, 89 participants from HCP)
 Bellier 2023: anterior-posterior STG organization for music
 (F = 25.09, iEEG, 29 patients, 2668 electrodes)

CONSTRAINT (Sabat 2025):
 Integration windows in ferret auditory cortex (15→150ms) are
 INVARIANT to stimulus context. This suggests the basic gradient
 is hardwired. Expertise effects (d = 0.32) may operate through
 attentional modulation or top-down feedback rather than
 expanding integration windows per se.
```

### 3.3 Effect Size Summary

```
PRIMARY GRADIENT:
 Site-level: r = 0.99 (Mischler 2025, ECoG, n=6 sites)
 Electrode-level: r = 0.32 (Mischler 2025, p=1.5e-05)
 Integration β: 0.064 oct/mm (Norman-Haignere 2022, iEEG)
 Temporal ACW: d = −0.66 to −2.03 (Golesorkhi 2021, MEG)
EXPERTISE EFFECT:
 Musicians > non: d = 0.32 (Mischler 2025, layers 7-13)
 Expertise×context: r = 0.286–0.459 (Bonetti 2024, FDR corrected)
 Aptitude×N1m: η²p = 0.095 (Wöhrle 2024, AMMA interaction)
AUDITORY CORTEX:
 STG high gamma: r = 0.43–0.58 (Potes 2012, music intensity)
 STG→motor lag: 110ms (Potes 2012, r=0.70 at τ=110ms)
 Within-HG shift: 7–8mm (Briley 2013, medial→anterolateral)
 STG A-P gradient: χ² = 8.6, p = 0.003 (Foo 2016, dissonance)

Quality Assessment: α-tier (direct neural measurement via ECoG/iEEG)
Replication: INDEPENDENTLY REPLICATED by Norman-Haignere 2022
 (different lab, method, larger sample, same gradient)
Methods: 8 methods, 15 papers, N > 400 total participants
```

---

## 4. R³ Input Mapping: What HMCE Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | HMCE Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Intensity dynamics for context tracking | Sound energy as context cue |
| **B: Energy** | [8] | loudness | Perceptual intensity | Stevens 1957: power law |
| **B: Energy** | [10] | spectral_flux | Onset/transition detection | Context boundary marker |
| **B: Energy** | [11] | onset_strength | Event boundary marking | Onset precision |
| **D: Change** | [21] | spectral_change | Short-context dynamics | Rate of spectral change |
| **D: Change** | [22] | energy_change | Medium-context dynamics | Intensity rate of change |
| **D: Change** | [23] | pitch_change | Melodic contour dynamics | Pitch rate of change |
| **D: Change** | [24] | timbre_change | Timbral evolution | Instrument identity dynamics |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Foundation×Perceptual coupling | Temporal-perceptual binding |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Dynamics×Perceptual coupling | Derivative-feature binding |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | HMCE Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **G: Rhythm** | [68] | syncopation_index | Temporal context disruption — syncopated events create expectation violations that hierarchical encoding must accommodate | Longuet-Higgins & Lee 1984 |
| **G: Rhythm** | [69] | metricality_index | Metrical hierarchy depth — maps directly to HMCE's multi-level context hierarchy (short/medium/long) | Grahn & Brett 2007 |
| **G: Rhythm** | [65] | tempo_estimate | Temporal grid for context window calibration — context encoding timescales depend on tempo | Fraisse 1982 |

**Rationale**: HMCE models hierarchical temporal context encoding. The G:Rhythm features provide explicit metrical structure information that directly maps to HMCE's multi-level context hierarchy. Syncopation [68] signals expectation violations across temporal levels, metricality [69] quantifies the depth of nested subdivisions that HMCE's layers encode, and tempo [65] calibrates the temporal grid against which context windows are measured.

**Code impact** (Phase 6): `r3_indices` must be extended to include [65, 68, 69]. These features are read-only inputs — no formula changes required.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[21:25] Change (4D) ─────────┐
R³[10] spectral_flux ──────────┼──► Short Context (10–50 notes)
R³[11] onset_strength ─────────┘ short_context at H8 (300ms)
 Math: C_short = Σ Δ(t)·w₁(t−τ), τ₁=1s

R³[7] amplitude ────────────────┐
R³[8] loudness ─────────────────┼──► Medium Context (50–100 notes)
R³[22] energy_change ───────────┘ medium_context at H14 (700ms)
 Math: C_med = Σ E(t)·w₂(t−τ), τ₂=5s

R³[25:33] x_l0l5 (8D) ────────┐
R³[33:41] x_l4l5 (8D) ────────┼──► Long Context (100–300+ notes)
 long_context at H20 (5000ms)
 Math: C_long = Σ X(t)·w₃(t−τ), τ₃=15s

Expertise Factor ───────────────── Extended Context (300+, musicians only)
 Expertise modulates long-context
 Math: C_ext = C_long · (1 + d·expert)
 d = 0.32 (Mischler 2025)

R³[65] tempo_estimate ─────────┐
R³[68] syncopation_index ──────┼──► Metrical Context (v2)
R³[69] metricality_index ──────┘ Hierarchical rhythm encoding
 maps to temporal-context context levels
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

HMCE requires H³ features at three horizons: H8 (300ms), H14 (700ms), H20 (5000ms).
These correspond to motif → phrase → section timescales.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 8 | M0 (value) | L0 (fwd) | Current onset detection |
| 10 | spectral_flux | 8 | M1 (mean) | L0 (fwd) | Mean onset rate (short) |
| 11 | onset_strength | 8 | M0 (value) | L0 (fwd) | Event boundary current |
| 21 | spectral_change | 8 | M1 (mean) | L0 (fwd) | Mean spectral dynamics |
| 21 | spectral_change | 8 | M8 (velocity) | L0 (fwd) | Change acceleration |
| 22 | energy_change | 14 | M1 (mean) | L0 (fwd) | Mean energy dynamics |
| 22 | energy_change | 14 | M13 (entropy) | L0 (fwd) | Context unpredictability |
| 23 | pitch_change | 14 | M1 (mean) | L0 (fwd) | Mean pitch dynamics |
| 23 | pitch_change | 14 | M3 (std) | L0 (fwd) | Pitch variability |
| 7 | amplitude | 14 | M18 (trend) | L0 (fwd) | Intensity trajectory |
| 8 | loudness | 14 | M1 (mean) | L0 (fwd) | Mean loudness over phrase |
| 25 | x_l0l5[0] | 20 | M1 (mean) | L0 (fwd) | Long-term foundation coupling |
| 25 | x_l0l5[0] | 20 | M13 (entropy) | L0 (fwd) | Long-term unpredictability |
| 33 | x_l4l5[0] | 20 | M1 (mean) | L0 (fwd) | Long-term dynamics coupling |
| 33 | x_l4l5[0] | 20 | M22 (autocorr) | L0 (fwd) | Self-similarity detection |
| 33 | x_l4l5[0] | 20 | M19 (stability) | L0 (fwd) | Temporal stability |
| 25 | x_l0l5[0] | 20 | M22 (autocorr) | L0 (fwd) | Section-level repetition |
| 8 | loudness | 20 | M18 (trend) | L0 (fwd) | Long-range loudness trend |

**v1 demand**: 18 tuples

#### R³ v2 Projected Expansion

HMCE projected v2 features from G:Rhythm, aligned with corresponding H³ horizons.

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 65 | tempo | G | 8 | M0 (value) | L0 | Current tempo estimate at short context |
| 65 | tempo | G | 20 | M18 (trend) | L0 | Long-range tempo trajectory |
| 68 | syncopation | G | 8 | M0 (value) | L0 | Instantaneous syncopation level |
| 68 | syncopation | G | 14 | M14 (periodicity) | L0 | Syncopation periodicity at phrase scale |
| 69 | metricality | G | 14 | M0 (value) | L0 | Metric regularity at phrase scale |
| 69 | metricality | G | 20 | M1 (mean) | L0 | Long-range mean metricality |

**v2 projected**: 6 tuples
**Total projected**: 24 tuples of 294,912 theoretical = 0.0081%

---

## 6. Output Space: 13D Multi-Layer Representation

### 6.1 Complete Output Specification

```
HMCE OUTPUT TENSOR: 13D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0 │ f01_short_context │ [0, 1] │ Short context encoding (pmHG, 10–50 notes).
 │ │ │ Layer 1–4 transformer correspondence.
 │ │ │ f01 = σ(α · flux_mean · onset ·
 │ │ │ short_context)
 │ │ │ α = 0.90
────┼───────────────────┼────────┼────────────────────────────────────────────
 1 │ f02_medium_context│ [0, 1] │ Medium context encoding (STG, 50–100 notes).
 │ │ │ Layer 5–9 transformer correspondence.
 │ │ │ f02 = σ(β · energy_mean · loudness_mean ·
 │ │ │ medium_context)
 │ │ │ β = 0.85
────┼───────────────────┼────────┼────────────────────────────────────────────
 2 │ f03_long_context │ [0, 1] │ Long context encoding (MTG, 100–200 notes).
 │ │ │ Layer 10–12 transformer correspondence.
 │ │ │ f03 = σ(γ · x_coupling · autocorr ·
 │ │ │ long_context)
 │ │ │ γ = 0.80
────┼───────────────────┼────────┼────────────────────────────────────────────
 3 │ f04_gradient │ [0, 1] │ Anatomical gradient strength (r = 0.99).
 │ │ │ f04 = 0.99 · (f01 + f02 + f03) / 3
────┼───────────────────┼────────┼────────────────────────────────────────────
 4 │ f05_expertise │ [0, 1] │ Musician advantage proxy (d = 0.32).
 │ │ │ Modulates extended context encoding.
 │ │ │ f05 = σ(0.32 · f03 · stability_long)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 5 │ context_depth │ [0, 1] │ Effective context integration depth.
 │ │ │ Weighted sum across scales.
 │ │ │ depth = (1·f01 + 2·f02 + 3·f03) / 6
────┼───────────────────┼────────┼────────────────────────────────────────────
 6 │ gradient_index │ [0, 1] │ Normalized distance from A1.
 │ │ │ Maps transformer layer correspondence.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 7 │ a1_encoding │ [0, 1] │ Primary auditory cortex current state.
 │ │ │ short_context aggregation.
────┼───────────────────┼────────┼────────────────────────────────────────────
 8 │ stg_encoding │ [0, 1] │ Superior temporal gyrus current state.
 │ │ │ medium_context aggregation.
────┼───────────────────┼────────┼────────────────────────────────────────────
 9 │ mtg_encoding │ [0, 1] │ Middle temporal gyrus current state.
 │ │ │ long_context aggregation.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
10 │ context_prediction│ [0, 1] │ Next context level prediction.
 │ │ │ H³ trend-based expectation.
────┼───────────────────┼────────┼────────────────────────────────────────────
11 │ phrase_expect │ [0, 1] │ Phrase boundary expectation.
 │ │ │ Entropy-driven boundary detection.
────┼───────────────────┼────────┼────────────────────────────────────────────
12 │ structure_predict │ [0, 1] │ Long-range structural prediction.
 │ │ │ Autocorrelation-based section return.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 13D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Context Encoding Function

```
Context Encoding:

 Context_Encoding(region) = f(Distance_from_pmHG)

 Transformer_Layer_Correspondence(region) ∝ Distance_from_pmHG

 For Musicians:
 Prediction_Accuracy(layer) ↑ continuously to layer 13
 Context_Integration ≈ 300 notes

 For Non-Musicians:
 Prediction_Accuracy(layer) plateaus at layer 10–11
 Context_Integration ≈ 100 notes

 Hierarchical Encoding:
 Context_Depth(region) = α · Distance + β · Expertise + ε
 where α: gradient coefficient (0.99 correlation)
 β: expertise modulation (d = 0.32)
 ε: individual variability
```

### 7.2 Feature Formulas

```python
# f01: Short Context Encoding (pmHG, 10–50 notes)
flux_mean = h3[(10, 8, 1, 0)] # spectral_flux mean at H8
onset_val = h3[(11, 8, 0, 0)] # onset_strength value at H8
f01 = σ(0.90 · flux_mean · onset_val

# f02: Medium Context Encoding (STG, 50–100 notes)
energy_mean = h3[(22, 14, 1, 0)] # energy_change mean at H14
loudness_mean = h3[(8, 14, 1, 0)] # loudness mean at H14
f02 = σ(0.85 · energy_mean · loudness_mean

# f03: Long Context Encoding (MTG, 100–300+ notes)
x_coupling = h3[(25, 20, 1, 0)] # x_l0l5 mean at H20
autocorr = h3[(33, 20, 22, 0)] # x_l4l5 autocorrelation at H20
f03 = σ(0.80 · x_coupling · autocorr

# f04: Anatomical Gradient (r = 0.99)
f04 = 0.99 · (f01 + f02 + f03) / 3

# f05: Expertise Effect (d = 0.32)
stability_long = h3[(33, 20, 19, 0)] # x_l4l5 stability at H20
f05 = σ(0.32 · f03 · stability_long)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Sources | Evidence Type | HMCE Function |
|--------|-----------------|---------|---------------|---------------|
| **pmHG (A1)** | ±50, -20, 8 | Mischler 2025, Norman-Haignere 2022, Briley 2013 (Tal: ±42, -17, 14) | ECoG, iEEG, EEG | Short context (Layer 1–4); integration τ ≈ 74ms |
| **Anterolateral HG** | ±46, -13, 17 | Briley 2013 (Tal: ±46, -13, 17) | EEG source | Pitch chroma encoding; 7–8mm from medial HG |
| **Posterior STG** | ±60, -30, 8 | Mischler 2025, Bellier 2023, Potes 2012, Foo 2016 | ECoG (×4 studies) | Medium context (Layer 5–9); onset features; integration τ ≈ 136ms |
| **Anterior STG** | ±45, -5, 2 | Kim 2021 (Tal: ±44, -6, 2), Foo 2016 (anterior > posterior for dissonance) | MEG, ECoG | Medium-long context; perceptual ambiguity; complex stimuli |
| **MTG** | ±60, -40, 0 | Mischler 2025, Blasi 2025 | ECoG, review | Long context (Layer 10–12); integration τ ≈ 274ms |
| **Temporal Pole** | ±40, 10, -30 | Mischler 2025 | ECoG | Extended context (Layer 13); musicians only |
| **IFG (BA44/45)** | ±39, 20, 15 | Kim 2021 (Tal: ±39, 20, 15), Maess 2001, Tachibana 2024 | MEG, fNIRS | Syntactic irregularity processing; extends hierarchy beyond temporal lobe |
| **Hippocampus** | ±26, -30, -8 | Bonetti 2024 (AAL) | MEG source | Feedforward from AC; memory-based contextual predictions |
| **ACC / Cingulate** | ~2, 34, 0 | Bonetti 2024 (AAL) | MEG source | Top of feedforward hierarchy; prediction monitoring |

---

## 9. Cross-Unit Pathways

### 9.1 HMCE ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ HMCE INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ INTRA-UNIT (STU): │
│ HMCE.context_depth ──────► AMSC (context → motor coupling timescale) │
│ HMCE.a1_encoding ────────► MDNS (short context for TRF decoding) │
│ HMCE.structure_predict ──► AMSS (structure for stream segregation) │
│ │
│ CROSS-UNIT (P4: STU internal): │
│ context_depth ↔ HMCE.encoding_complexity (r = 0.99) │
│ Longer temporal context → higher cortical encoding │
│ │
│ CROSS-UNIT (P5: STU → ARU): │
│ HMCE.context_depth ──► ARU (context-dependent emotional processing) │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Temporal pole lesions** | Should impair long-range (300+) context processing | ✅ Testable |
| **Non-musician encoding** | Should show reduced late-layer (10+) encoding | ✅ **Confirmed**: d = 0.32 (Mischler), r=0.29–0.46 (Bonetti), η²p=0.095 (Wöhrle) |
| **Simple/repetitive music** | Should not engage full 4-level hierarchy | ✅ Testable |
| **Anatomical gradient** | Should hold across individuals and methods | ✅ **Confirmed**: r=0.32 (Mischler), β=0.064 (Norman-Haignere), d=−0.66 to −2.03 (Golesorkhi) |
| **Integration windows flexible** | Expertise should expand integration windows | ⚠️ **Challenged**: Sabat 2025 finds windows invariant to context in ferret AC |
| **Anterior-posterior STG gradient** | Complex/contextual stimuli processed more anteriorly | ✅ **Confirmed**: Foo 2016 (χ²=8.6), Bellier 2023 (F=25.09) |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class HMCE(BaseModel):
 """Hierarchical Musical Context Encoding.

 Output: 13D per frame.
 """
 NAME = "HMCE"
 UNIT = "STU"
 TIER = "α1"
 OUTPUT_DIM = 13
 ALPHA = 0.90 # Short context weight
 BETA = 0.85 # Medium context weight
 GAMMA = 0.80 # Long context weight
 GRADIENT_CORR = 0.99 # Mischler 2025 correlation
 EXPERTISE_D = 0.32 # Mischler 2025 musician advantage

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """18 tuples for HMCE computation."""
 return [
 # (r3_idx, horizon, morph, law)
 # Short context (H8 = 300ms)
 (10, 8, 0, 0), # spectral_flux, value, forward
 (10, 8, 1, 0), # spectral_flux, mean, forward
 (11, 8, 0, 0), # onset_strength, value, forward
 (21, 8, 1, 0), # spectral_change, mean, forward
 (21, 8, 8, 0), # spectral_change, velocity, forward
 # Medium context (H14 = 700ms)
 (22, 14, 1, 0), # energy_change, mean, forward
 (22, 14, 13, 0), # energy_change, entropy, forward
 (23, 14, 1, 0), # pitch_change, mean, forward
 (23, 14, 3, 0), # pitch_change, std, forward
 (7, 14, 18, 0), # amplitude, trend, forward
 (8, 14, 1, 0), # loudness, mean, forward
 # Long context (H20 = 5000ms)
 (25, 20, 1, 0), # x_l0l5[0], mean, forward
 (25, 20, 13, 0), # x_l0l5[0], entropy, forward
 (33, 20, 1, 0), # x_l4l5[0], mean, forward
 (33, 20, 22, 0), # x_l4l5[0], autocorrelation, forward
 (33, 20, 19, 0), # x_l4l5[0], stability, forward
 (25, 20, 22, 0), # x_l0l5[0], autocorrelation, forward
 (8, 20, 18, 0), # loudness, trend, forward
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 """
 Compute HMCE 13D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) → (B,T) scalars
 r3: (B,T,49) raw R³ features

 Returns:
 (B,T,13) HMCE output
 """
 # ═══ LAYER E: Explicit features ═══
 flux_mean = h3_direct[(10, 8, 1, 0)].unsqueeze(-1)
 onset_val = h3_direct[(11, 8, 0, 0)].unsqueeze(-1)
 f01 = torch.sigmoid(self.ALPHA * (
 flux_mean * onset_val
 ))

 energy_mean = h3_direct[(22, 14, 1, 0)].unsqueeze(-1)
 loudness_mean = h3_direct[(8, 14, 1, 0)].unsqueeze(-1)
 f02 = torch.sigmoid(self.BETA * (
 energy_mean * loudness_mean
 ))

 x_coupling = h3_direct[(25, 20, 1, 0)].unsqueeze(-1)
 autocorr = h3_direct[(33, 20, 22, 0)].unsqueeze(-1)
 f03 = torch.sigmoid(self.GAMMA * (
 x_coupling * autocorr
 ))

 f04 = self.GRADIENT_CORR * (f01 + f02 + f03) / 3

 stability_long = h3_direct[(33, 20, 19, 0)].unsqueeze(-1)
 f05 = torch.sigmoid(self.EXPERTISE_D * f03 * stability_long)

 # ═══ LAYER M: Mathematical ═══
 context_depth = (1 * f01 + 2 * f02 + 3 * f03) / 6
 gradient_index = f04

 # ═══ LAYER P: Present ═══

 # ═══ LAYER F: Future ═══
 amplitude_trend = h3_direct[(7, 14, 18, 0)].unsqueeze(-1)
 context_prediction = torch.sigmoid(
 0.5 * f03 + 0.3 * f02 + 0.2 * amplitude_trend
 )
 entropy_energy = h3_direct[(22, 14, 13, 0)].unsqueeze(-1)
 phrase_expect = torch.sigmoid(
 )
 long_autocorr = h3_direct[(25, 20, 22, 0)].unsqueeze(-1)
 structure_predict = torch.sigmoid(
 )

 return torch.cat([
 f01, f02, f03, f04, f05, # E: 5D
 context_depth, gradient_index, # M: 2D
 a1_encoding, stg_encoding, mtg_encoding, # P: 3D
 context_prediction, phrase_expect, structure_predict, # F: 3D
 ], dim=-1) # (B, T, 13)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 15 | 5 ECoG/iEEG, 4 MEG, 2 EEG, 1 fMRI, 1 fNIRS, 2 single-unit |
| **Primary Effect** | r = 0.32 (electrode-level, p=1.5e-05); r = 0.99 (n=6 sites) | Mischler 2025 |
| **Independent Replication** | β = 0.064 oct/mm (F=20.56, p<0.001) | Norman-Haignere 2022 |
| **Expertise Effect** | d = 0.32 (Mischler), r=0.29–0.46 (Bonetti), η²p=0.095 (Wöhrle) | 3 studies converge |
| **Evidence Modality** | ECoG, iEEG, MEG, EEG, fMRI, fNIRS, single-unit | 8 methods |
| **Constraint** | Integration windows invariant to context (Sabat 2025) | Basic gradient may be hardwired |
| **Falsification Tests** | 2/4 confirmed | High validity |
| **R³ Features Used** | 25D of 49D | Energy + Change + Interactions |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **Output Dimensions** | **13D** | 4-layer structure |

---

## 13. Scientific References

1. **Mischler, G., et al. (2025)**. The impact of musical expertise on disentangled and contextual neural encoding of music revealed by generative music models. *Nature Communications*. (ECoG + EEG, n=6 iEEG + 20 EEG; r=0.32 electrode-level, r=0.99 site-level, d=0.32 expertise)
2. **Norman-Haignere, S. V., et al. (2022)**. Multiscale temporal integration organizes hierarchical computation in human auditory cortex. *Nature Human Behaviour*, 6, 455–469. (iEEG, 18 patients, 190 electrodes; β=0.064 oct/mm, 74→274ms integration gradient)
3. **Bonetti, L., et al. (2024)**. Spatiotemporal brain hierarchies of auditory memory recognition and predictive coding. *Nature Communications*, 15, 4313. (MEG, N=83; hierarchical AC→hippocampus→cingulate, BOR=2.91e-07)
4. **Bellier, L., et al. (2023)**. Music can be reconstructed from human auditory cortex activity using nonlinear decoding models. *PLoS Biology*, 21(8), e3002176. (iEEG, 29 patients, 2668 electrodes; STG anterior-posterior organization)
5. **Potes, C., et al. (2012)**. Dynamics of electrocorticographic (ECoG) activity in human temporal and frontal cortical areas during music listening. *NeuroImage*, 61, 841–848. (ECoG, N=8; STG high gamma r=0.49, STG→motor lag 110ms)
6. **Golesorkhi, M., et al. (2021)**. The brain and its time: intrinsic neural timescales are key for input processing. *Communications Biology*, 4, 1280. (MEG, N=89 HCP; core-periphery temporal hierarchy d=−0.66 to −2.03)
7. **Ye, C., et al. (2025)**. Hierarchical temporal processing in the primate thalamocortical system. *Research* (Science Partner). (ECoG monkey + EEG human; 3-tiered hierarchy, r=0.93 synchronization)
8. **Wöhrle, J., et al. (2024)**. Neuromagnetic representation of musical roundness in chord progressions. MEG study. (N=30; context accumulation η²p=0.101, expertise interaction η²p=0.095)
9. **Foo, F., et al. (2016)**. Differential processing of consonance and dissonance within the human superior temporal gyrus. *J Neuroscience*. (ECoG, N=8; anterior-posterior STG gradient χ²=8.6, p=0.003)
10. **Briley, P. M., et al. (2013)**. Evidence for pitch chroma mapping in human auditory cortex. *Cerebral Cortex*. (EEG source, N=15; medial vs anterolateral HG, F=29.865, 7–8mm shift)
11. **Fedorenko, E., et al. (2012)**. Sensitivity to musical structure in the human brain. *J Neurophysiology*, 108(12), 3289–3300. (fMRI, N=12; bilateral temporal music-structure sensitivity)
12. **Kim, C. H., et al. (2021)**. Dissociation of connectivity for syntactic irregularity and perceptual ambiguity in musical chord stimuli. *Frontiers in Neuroscience*, 15, 693629. (MEG, N=19; IFG syntax vs STG ambiguity, F=12.37)
13. **Sabat, S., et al. (2025)**. Neurons in auditory cortex integrate information within constrained temporal windows. *bioRxiv*. (Single-unit ferret; integration 15→150ms, INVARIANT to context — CONSTRAINS HMCE)
14. **Hasson, U., et al. (2008)**. A hierarchy of temporal receptive windows in human cortex. *J Neuroscience*, 28(10), 2539–2550. (fMRI; TRW framework — foundational for HMCE concept)
15. **Honey, C. J., et al. (2012)**. Slow cortical dynamics and the accumulation of information over long timescales. *Neuron*, 76(2), 423–434. (fMRI; slow cortical dynamics, inter-subject correlation across timescales)

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D): L0, L4, L5, L6, L9, X_L4L5, X_L5L9 | R³ (49D): Energy, Change, Interactions |
| Context hierarchy | L4 derivatives (velocity→jerk) | H³ direct features |
| Statistics | S⁰.L9 (mean, entropy, kurtosis) | H³ morphs (M1, M3, M13, M22) |
| Cross-feature | X_L4L5[192:200], X_L5L9[224:232] | R³.x_l0l5[25:33], x_l4l5[33:41] |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 31/2304 = 1.35% | 18/2304 = 0.78% |
| Output dimensions | 12D | **13D** (added f05_expertise) |

---

**Model Status**: ✅ **VALIDATED** (v2.1.0: 1→15 papers, r=0.99 QUALIFIED to r=0.32 electrode-level, Norman-Haignere independent replication, Sabat constraint noted)
**Output Dimensions**: **13D**
**Evidence Tier**: **α (Mechanistic)** — strengthened by multi-method convergence (8 methods, 15 papers)
**Confidence**: **>90%** — gradient independently replicated; expertise mechanism nuanced by Sabat 2025