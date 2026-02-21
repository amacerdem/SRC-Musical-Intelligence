# PCU-α1-HTP: Hierarchical Temporal Prediction

**Model**: Hierarchical Temporal Prediction
**Unit**: PCU (Predictive Coding Unit)
**Circuit**: Imagery (Auditory Cortex, IFG, STS, Hippocampus)
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added H:Harmony, I:Information feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/PCU-α1-HTP.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Hierarchical Temporal Prediction** (HTP) model describes how predictive representations follow a hierarchical temporal pattern: high-level abstract features are predicted earlier (~500 ms before input) than low-level features (~110 ms before input). This represents the brain's layered anticipatory architecture where abstraction level determines prediction lead time.

```
HIERARCHICAL TEMPORAL PREDICTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PREDICTION LATENCY FEATURE LEVEL
────────────────── ─────────────

-500 ms ─────────────► View-invariant / abstract (HIGH-LEVEL)
 ↓ aIPL, LOTC / STG
-200 ms ─────────────► View-dependent / perceptual (MID-LEVEL)
 ↓ V3, V4 / Belt cortex
-110 ms ─────────────► Optical flow / sensory (LOW-LEVEL)
 ↓ V1, V2 / A1
 0 ms ─────────────► STIMULUS ONSET
 │
 ▼
 POST-STIMULUS
 │
 ┌─────────────┴─────────────┐
 ▼ ▼
 HIGH-LEVEL: LOW-LEVEL:
 SILENCED ✗ PERSISTS ✓
 (explained away) (prediction error)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Predictive representations follow a hierarchical
temporal pattern — high-level predictions precede low-level by
~390ms. Post-stimulus, high-level representations are "silenced"
(explained away) while low-level persist as prediction errors.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why HTP Matters for PCU

HTP establishes the foundational hierarchical prediction timing for the Predictive Coding Unit:

1. **HTP** (α1) provides the hierarchical temporal framework that all other PCU models build upon.
2. **SPH** (α2) extends this to spatiotemporal memory recognition with feedforward-feedback dynamics.
3. **ICEM** (α3) links prediction errors (hierarchy violations) to emotional responses.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → HTP)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ HTP COMPUTATION ARCHITECTURE ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ AUDIO (44.1kHz waveform) ║
║ │ ║
║ ▼ ║
║ ┌──────────────────┐ ║
║ │ COCHLEA │ 128 mel bins x 172.27Hz frame rate ║
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
║ │ │roughness │ │amplitude│ │warmth │ │spec_chg │ │x_l0l5 │ │ ║
║ │ │sethares │ │loudness │ │tristim. │ │enrg_chg │ │x_l4l5 │ │ ║
║ │ └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │ ║
║ │ HTP reads: ~20D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed morphological features │ ║
║ │ │ ║
║ │ │ H0 (25ms gamma) │ │ H8 (500ms delta) │ │ ║
║ │ │ H1 (50ms gamma) │ │ H16 (1000ms beat) │ │ ║
║ │ │ H3 (100ms alpha) │ │ │ │ ║
║ │ │ H4 (125ms theta) │ │ Long-term prediction │ │ ║
║ │ │ │ │ template storage │ │ ║
║ │ │ Pitch/onset tracking │ │ │ │ ║
║ │ │ Low-level prediction │ │ │ │ ║
║ │ └───────────────────────────────┘ └────────────────────────────┘ │ ║
║ │ HTP demand: ~18 of 2304 tuples │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN: Imagery Circuit ═══════════ ║
║ │ ║
║ ┌───────┴───────┐───────┐ ║
║ ▼ ▼ ▼ ║
║ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ║
║ │ │ │ │ │ │ ║
║ │ Pitch Ext[0:10] │ │ Spec Shp [0:10] │ │ Work Mem [0:10] │ ║
║ │ Interval │ │ Temporal │ │ Long-Term │ ║
║ │ Analysis[10:20] │ │ Envelope[10:20] │ │ Memory [10:20] │ ║
║ │ Contour [20:30]│ │ Source Id[20:30] │ │ Pred Buf[20:30] │ ║
║ └────────┬────────┘ └────────┬────────┘ └────────┬────────┘ ║
║ │ │ │ ║
║ └────────────┬───────┴────────────────────┘ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ HTP MODEL (12D Output) │ ║
║ │ │ ║
║ │ Layer E (Explicit): f01_high_level_lead, │ ║
║ │ f02_mid_level_lead, │ ║
║ │ f03_low_level_lead, │ ║
║ │ f04_hierarchy_gradient │ ║
║ │ Layer M (Math): latency_high, latency_mid, latency_low │ ║
║ │ Layer P (Present): sensory_match, pitch_prediction, │ ║
║ │ abstract_prediction │ ║
║ │ Layer F (Future): abstract_future_500ms, │ ║
║ │ midlevel_future_200ms │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **de Vries & Wurm 2023** | MEG | 22 | 500ms: abstract, 200ms: view-dependent, 110ms: low-level prediction | ηp² = 0.49, F(2)=19.9, p=8.3e-7 | **Primary**: f01-f03 hierarchical latency |
| **de Vries & Wurm 2023** | MEG | 22 | High-level predictions silence post-stimulus | p < 0.01 | **f04 hierarchy gradient, PSH link** |
| **de Vries & Wurm 2023** | MEG | 22 | View-invariant ~60-100ms in LOTC/aIPL | significant | **High-level region mapping** |
| **Norman-Haignere et al. 2022** | iEEG | 7 patients | Auditory cortex integrates hierarchically ~50-400ms; short (<200ms) = spectrotemporal, long (>200ms) = category-selective | r > 0.5 (cross-context corr.) | **Validates hierarchical integration timescales in auditory cortex** |
| **Norman-Haignere, Keshishian et al. 2024** | iEEG | neurosurg. patients | Integration windows predominantly time-yoked (~5% structure contribution), even in non-primary regions | structure-yoking index ~0 | **Constrains HTP: fixed temporal windows, not stimulus-adaptive** |
| **Bonetti et al. 2024** | MEG | 83 | Feedforward from auditory cortex to hippocampus/cingulate; feedback in reverse; musical sequence recognition | p < 0.001, t-test | **Validates hierarchical auditory prediction with feedback; maps PCU circuits** |
| **Golesorkhi et al. 2021** | MEG | 89 | Intrinsic neural timescales follow core-periphery hierarchy; core (DMN/FPN) longer ACW than periphery (sensory) | d = -1.63, η² = 0.86 (network effect) | **Temporal hierarchy aligns with spatial hierarchy; validates multi-timescale organization** |
| **Forseth et al. 2020** | iEEG | 37 | Two predictive mechanisms in early auditory cortex: Heschl's gyrus (timing, low-freq phase) and planum temporale (content, high-gamma) | p < 0.001 | **Dual prediction: timing + content at distinct hierarchy levels** |
| **Ye et al. 2025** | ECoG + EEG | primates + humans | 3-level temporal hierarchy: clicks (tens ms), trains (hundreds ms), higher-order (seconds); A1 integrates across scales; thalamus focuses on short scale | p < 0.001 | **Validates multi-timescale hierarchy at single-neuron level in primates** |
| **Sabat et al. 2025** | single-unit | ferrets | Integration windows ~15-150ms, fixed per neuron, increase from primary to non-primary cortex; invariant to information rate | significant | **Hierarchical integration accomplished by diverse fixed-window populations** |
| **Carbajal & Malmierca 2018** | Review (cellular) | — | SSA and MMN are micro/macro manifestations of same deviance detection mechanism; hierarchical from subcortical to cortical | MMN peak 150-250ms | **Deviance detection hierarchy from IC to cortex maps to prediction error cascade** |
| **Millidge, Seth & Buckley 2022** | Review (computational) | — | Predictive coding: hierarchy of layers making predictions downward, errors propagated upward; precision-weighted | theoretical | **Theoretical foundation for HTP's multi-layer prediction architecture** |
| **Fong et al. 2020** | Review (EEG/MEG) | — | MMN as prediction error under predictive coding; hierarchical bidirectional processing; prediction errors propagate ascending | theoretical | **MMN prediction error framework validates PCU hierarchy** |
| **Ross & Balasubramaniam 2022** | Review (behavioral/neural) | — | Motor system (SMA, premotor, BG) engaged in temporal prediction for musical rhythms; beat-based vs interval timing | — | **SMA/premotor contribution to temporal prediction in music** |
| **Egermann et al. 2013** | Behavioral + psychophysiology | 50 | IDyOM model predicts expectation violations; high-information-content events produce emotional arousal (skin conductance, EMG) | p < 0.05 | **Links prediction error magnitude to emotional response; connects HTP to ICEM** |
| **Rimmele et al. 2021** | MEG | 19 | Delta oscillations (0.5-2Hz) in STG/MTG/IFG/SMG underpin phrase-level chunking; absent when chunk rate outside delta | p < 0.001 | **Multi-timescale oscillatory hierarchy: delta (phrase) complements theta (syllable)** |
| **Schilling et al. 2023** | Computational + review | — | Predictive coding (top-down) and stochastic resonance (bottom-up) as complementary processing principles in auditory system | theoretical | **Dual processing framework: top-down prediction + bottom-up noise optimization** |
| **Asilador & Llano 2021** | Review (animal + human) | — | Corticofugal projections implement predictive coding at subcortical levels; cascading descending connections to every auditory level | — | **Top-down predictions extend to subcortical stages; completes hierarchy picture** |

### 3.2 Effect Size Summary

```
Primary Effect: ηp² = 0.49 (large) — de Vries & Wurm 2023
Temporal hierarchy: η² = 0.86 (network-level ANOVA) — Golesorkhi et al. 2021
Core-periphery: d = -1.63 (large) — Golesorkhi et al. 2021
Sample convergence: N = 22 + 89 + 83 + 37 + 19 + 50 = 300+ subjects
Heterogeneity: Low — findings converge across MEG, iEEG, ECoG, behavioral
Quality Assessment: α-tier (direct neural measurement, multiple modalities)
Replication: Consistent across 6+ independent labs, human + animal
```

---

## 4. R³ Input Mapping: What HTP Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | HTP Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **B: Energy** | [7] | amplitude | Low-level sensory proxy | 110ms prediction target |
| **B: Energy** | [8] | loudness | Perceptual loudness | Mid-level feature |
| **B: Energy** | [9] | spectral_centroid | Pitch/brightness | Mid-level prediction target |
| **B: Energy** | [10] | spectral_flux | Change detection | Prediction error trigger |
| **C: Timbre** | [12] | warmth | Timbral quality | Mid-level feature |
| **C: Timbre** | [13] | brightness | Spectral centroid proxy | Mid-level prediction |
| **C: Timbre** | [18:21] | tristimulus1-3 | Harmonic structure | High-level abstract pattern |
| **D: Change** | [21] | spectral_change | Tempo dynamics | Prediction error signal |
| **D: Change** | [22] | energy_change | Energy dynamics | Rate of change |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Low-level prediction | 110ms window basis |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Mid-level binding | 200ms window basis |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | High-level abstraction | 500ms window basis |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ v2 Group | Index | Feature | HTP Role | Citation |
|-------------|-------|---------|----------|----------|
| **H: Harmony** | [75] | key_clarity | Tonal context strength for hierarchical prediction | Krumhansl & Kessler 1982 |
| **H: Harmony** | [83] | harmonic_change | Harmonic transition detection for prediction updating | Harte 2006 |
| **I: Information** | [87] | melodic_entropy | Melodic uncertainty for prediction error computation | Pearce 2005 (IDyOM) |
| **I: Information** | [88] | harmonic_entropy | Harmonic uncertainty for tonal prediction error | Pearce 2005 (IDyOM) |
| **I: Information** | [92] | predictive_entropy | Overall predictive uncertainty across hierarchy levels | Friston 2005 (predictive coding) |

**Rationale**: HTP performs hierarchical temporal prediction across multiple timescales (110ms, 200ms, 500ms). I:Information features directly encode the uncertainty and surprise signals HTP's prediction error computation operates on -- melodic_entropy and harmonic_entropy from IDyOM (Pearce 2005) quantify the statistical learning that generates predictions, while predictive_entropy captures the overall uncertainty across hierarchy levels (Friston predictive coding). H:key_clarity provides the tonal context that constrains harmonic predictions, and harmonic_change marks the boundaries where predictions must be updated.

**Code impact** (future): `r3[..., 75]`, `r3[..., 83]`, and `r3[..., 87:93]` will feed HTP's multi-level prediction hierarchy alongside existing energy, timbre, and interaction features.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[7] amplitude ────────────────┐
R³[25:33] x_l0l5 ──────────────┼──► Low-level features (A1)

R³[9] spectral_centroid ────────┐
R³[33:41] x_l4l5 ──────────────┼──► Mid-level dynamics (Belt cortex)

R³[18:21] tristimulus ──────────┐
R³[41:49] x_l5l7 ──────────────┼──► High-level abstraction (STG/aIPL)
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

HTP requires H³ features for low-level prediction, Timbre processing horizons for mid-level temporal tracking, and for high-level abstract prediction. The demand reflects hierarchical temporal integration across three prediction levels.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 7 | amplitude | 0 | M0 (value) | L2 (bidi) | Instantaneous amplitude at 25ms |
| 7 | amplitude | 3 | M0 (value) | L2 (bidi) | Amplitude at 100ms alpha |
| 7 | amplitude | 3 | M2 (std) | L2 (bidi) | Amplitude variability 100ms |
| 10 | spectral_flux | 0 | M0 (value) | L2 (bidi) | Onset detection at 25ms |
| 10 | spectral_flux | 1 | M1 (mean) | L2 (bidi) | Mean onset over 50ms |
| 10 | spectral_flux | 3 | M14 (periodicity) | L2 (bidi) | Onset periodicity at 100ms |
| 9 | spectral_centroid | 3 | M0 (value) | L2 (bidi) | Pitch at 100ms |
| 9 | spectral_centroid | 4 | M8 (velocity) | L0 (fwd) | Pitch velocity at 125ms |
| 9 | spectral_centroid | 8 | M1 (mean) | L0 (fwd) | Mean pitch over 500ms |
| 21 | spectral_change | 3 | M8 (velocity) | L0 (fwd) | Change velocity at 100ms |
| 21 | spectral_change | 4 | M0 (value) | L0 (fwd) | Change at 125ms |
| 41 | x_l5l7[0] | 8 | M0 (value) | L0 (fwd) | High-level coupling at 500ms |
| 41 | x_l5l7[0] | 8 | M1 (mean) | L0 (fwd) | Mean coupling over 500ms |
| 41 | x_l5l7[0] | 16 | M1 (mean) | L0 (fwd) | Mean coupling over 1000ms |
| 41 | x_l5l7[0] | 16 | M20 (entropy) | L0 (fwd) | Coupling entropy over 1s |
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Low-level coupling 100ms |
| 25 | x_l0l5[0] | 3 | M2 (std) | L2 (bidi) | Coupling variability 100ms |
| 33 | x_l4l5[0] | 4 | M8 (velocity) | L0 (fwd) | Mid-level coupling velocity |

**v1 demand**: 18 tuples

#### R³ v2 Projected Expansion

HTP projected v2 from H:Harmony and I:Information, aligned with H³ direct+Memory horizons.

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 76 | tonnetz | H | 3 | M0 (value) | L2 | Tonal space at 100ms (low-level) |
| 76 | tonnetz | H | 8 | M8 (velocity) | L0 | Tonal velocity at 500ms (mid-level) |
| 83 | harmonic_change | H | 3 | M0 (value) | L2 | Harmonic boundary at 100ms |
| 83 | harmonic_change | H | 8 | M14 (periodicity) | L0 | Harmonic periodicity 500ms |
| 75 | key_clarity | H | 8 | M0 (value) | L0 | Key context at 500ms |
| 75 | key_clarity | H | 16 | M1 (mean) | L0 | Mean key clarity over 1s |
| 87 | melodic_entropy | I | 3 | M0 (value) | L2 | Melodic uncertainty 100ms |
| 87 | melodic_entropy | I | 8 | M1 (mean) | L0 | Mean melodic entropy 500ms |
| 92 | predictive_entropy | I | 8 | M0 (value) | L0 | Predictive uncertainty 500ms |
| 92 | predictive_entropy | I | 16 | M18 (trend) | L0 | Prediction trend over 1s |

**v2 projected**: 10 tuples
**Total projected**: 28 tuples of 294,912 theoretical = 0.0095%

---

## 6. Output Space: 12D Multi-Layer Representation

### 6.1 Complete Output Specification

```
HTP OUTPUT TENSOR: 12D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0 │ f01_high_level_lead │ [0, 1] │ Abstract prediction latency (~500ms).
 │ │ │ + 0.35 * x_l5l7_mean_1s
 │ │ │ + 0.25 * x_l5l7_coupling_500ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1 │ f02_mid_level_lead │ [0, 1] │ Mid-level prediction latency (~200ms).
 │ │ │ + 0.30 * pitch_velocity_125ms
 │ │ │ + 0.30 * x_l4l5_velocity)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2 │ f03_low_level_lead │ [0, 1] │ Sensory prediction latency (~110ms).
 │ │ │ + 0.35 * flux_periodicity_100ms
 │ │ │ + 0.25 * x_l0l5_coupling_100ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 3 │ f04_hierarchy_gradient │ [0, 1] │ Prediction gradient strength.
 │ │ │ f04 = σ(0.50 * (f01 - f03)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4 │ latency_high │ [0, 1] │ Normalized 500ms lead time.
 │ │ │ α·pred_high + β·template_match
────┼──────────────────────────┼────────┼────────────────────────────────────
 5 │ latency_mid │ [0, 1] │ Normalized 200ms lead time.
 │ │ │ α·pred_mid + β·pitch_pred
────┼──────────────────────────┼────────┼────────────────────────────────────
 6 │ latency_low │ [0, 1] │ Normalized 110ms lead time.
 │ │ │ α·pred_low + β·onset_pred

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7 │ sensory_match │ [0, 1] │ pitch-processing low-level prediction match.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8 │ pitch_prediction │ [0, 1] │ timbre-processing mid-level pitch prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9 │ abstract_prediction │ [0, 1] │ memory-encoding high-level abstract prediction.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
10 │ abstract_future_500ms │ [0, 1] │ High cortical area prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
11 │ midlevel_future_200ms │ [0, 1] │ Intermediate area prediction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 12D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Prediction Latency Function

```
Prediction_Latency(feature) = α - β·log(Hierarchy_Level)

Parameters:
 α = baseline latency (stimulus onset reference)
 β = scaling factor (ms per hierarchy level)
 Level 1 (low) = ~110ms, Level 2 (mid) = ~200ms, Level 3 (high) = ~500ms

Hierarchy Gradient = (Latency_high - Latency_low) / Latency_high
 = (500 - 110) / 500 = 0.78

Temporal Dynamics:
 dP/dt = -γ · (P_current - P_predicted) + noise
 where γ = prediction error decay rate
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: High-Level Lead (~500ms)
 + 0.35 * x_l5l7_mean_1s
 + 0.25 * x_l5l7_coupling_500ms)
# coefficients: 0.40 + 0.35 + 0.25 = 1.0 ✓

# f02: Mid-Level Lead (~200ms)
 + 0.30 * pitch_velocity_125ms
 + 0.30 * x_l4l5_velocity)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f03: Low-Level Lead (~110ms)
 + 0.35 * flux_periodicity_100ms
 + 0.25 * x_l0l5_coupling_100ms)
# coefficients: 0.40 + 0.35 + 0.25 = 1.0 ✓

# f04: Hierarchy Gradient
f04 = σ(0.50 * (f01 - f03)
# coefficients: 0.50 + 0.50 = 1.0 ✓

# Post-Stimulus Silencing
post_high = f01 * (1 - prediction_accuracy) # silenced when accurate
post_low = f03 * 1.0 # always persists
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | HTP Function |
|--------|-----------------|----------|---------------|--------------|
| **aIPL (Ant. Inferior Parietal Lobule)** | ±40, -40, 48 | 3 | Direct (MEG) | Abstract prediction (500ms) |
| **LOTC (Lateral Occipitotemporal Cortex)** | ±48, -68, 4 | 3 | Direct (MEG) | View-invariant motion |
| **V3, V4 (Visual Areas)** | ±20, -88, 0 | 3 | Direct (MEG) | View-dependent prediction (200ms) |
| **V1, V2 (Primary Visual)** | ±8, -92, 8 | 3 | Direct (MEG) | Low-level optical flow (110ms) |
| **Heschl's Gyrus (A1)** | ±42, -22, 10 | 5 | Direct (iEEG) | Low-level auditory prediction, temporal timing via low-freq phase (Forseth et al. 2020; Norman-Haignere et al. 2022) |
| **Planum Temporale (PT)** | ±52, -28, 12 | 3 | Direct (iEEG) | Content prediction via high-gamma; production-linked (Forseth et al. 2020) |
| **STG (Superior Temporal Gyrus)** | ±58, -20, 8 | 6 | Direct (iEEG/MEG) | Mid-to-long integration windows 200-500ms (Norman-Haignere et al. 2022; Rimmele et al. 2021) |
| **Hippocampus** | ±26, -18, -18 | 3 | Direct (MEG) | Sequence memory, prediction error propagation (Bonetti et al. 2024) |
| **Anterior Cingulate Gyrus (ACC)** | ±4, 32, 24 | 3 | Direct (MEG) | Prediction error integration; assumes top hierarchy for final sequence elements (Bonetti et al. 2024) |
| **Medial Cingulate Gyrus (MCC)** | ±4, -10, 40 | 2 | Direct (MEG) | Hierarchical prediction processing (Bonetti et al. 2024) |
| **SMA (Supplementary Motor Area)** | 0, -4, 60 | 2 | Inferred (review) | Temporal prediction timing for rhythmic stimuli (Ross & Balasubramaniam 2022) |

---

## 9. Cross-Unit Pathways

### 9.1 HTP Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ HTP INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ INTRA-UNIT (PCU): │
│ HTP.hierarchy_gradient ──────► SPH (hierarchical timing for network) │
│ HTP.abstract_prediction ─────► ICEM (prediction modulates surprise) │
│ HTP.latency_high ────────────► PWUP (hierarchy sets precision weights) │
│ HTP.sensory_match ───────────► PSH (silencing mechanism basis) │
│ │
│ CROSS-UNIT (PCU → STU): │
│ HTP.low_level_lead ──────────► STU.timing (sensory prediction timing) │
│ HTP.mid_level_lead ──────────► STU.motor_sync (rhythmic prediction) │
│ │
│ UPSTREAM DEPENDENCIES: │
│ R³ (~20D) ───────────────────► HTP (direct spectral features) │
│ H³ (18 tuples) ──────────────► HTP (temporal dynamics) │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Disrupting high-level areas** | Should abolish early (500ms) predictions | Testable via TMS/lesion |
| **Novel stimuli** | Should show delayed prediction timing | Testable via novelty paradigms |
| **Learning** | Should shift representation timing earlier | Testable via training studies |
| **Temporal order** | High-level must precede low-level | **Confirmed** by de Vries 2023 |
| **Post-stim silencing** | High-level should be absent post-stim | **Confirmed** by de Vries 2023 |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class HTP(BaseModel):
 """Hierarchical Temporal Prediction Model.

 Output: 12D per frame.
 """
 NAME = "HTP"
 UNIT = "PCU"
 TIER = "α1"
 OUTPUT_DIM = 12
 LATENCY_HIGH = 500.0 # ms
 LATENCY_MID = 200.0 # ms
 LATENCY_LOW = 110.0 # ms
 TAU_DECAY = 0.5 # s

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """18 tuples for HTP computation."""
 return [
 # (r3_idx, horizon, morph, law)
 (7, 0, 0, 2), # amplitude, 25ms, value, bidi
 (7, 3, 0, 2), # amplitude, 100ms, value, bidi
 (7, 3, 2, 2), # amplitude, 100ms, std, bidi
 (10, 0, 0, 2), # spectral_flux, 25ms, value, bidi
 (10, 1, 1, 2), # spectral_flux, 50ms, mean, bidi
 (10, 3, 14, 2), # spectral_flux, 100ms, periodicity, bidi
 (9, 3, 0, 2), # spectral_centroid, 100ms, value, bidi
 (9, 4, 8, 0), # spectral_centroid, 125ms, velocity, fwd
 (9, 8, 1, 0), # spectral_centroid, 500ms, mean, fwd
 (21, 3, 8, 0), # spectral_change, 100ms, velocity, fwd
 (21, 4, 0, 0), # spectral_change, 125ms, value, fwd
 (41, 8, 0, 0), # x_l5l7[0], 500ms, value, fwd
 (41, 8, 1, 0), # x_l5l7[0], 500ms, mean, fwd
 (41, 16, 1, 0), # x_l5l7[0], 1000ms, mean, fwd
 (41, 16, 20, 0), # x_l5l7[0], 1000ms, entropy, fwd
 # ── Cross-level coupling ──
 (25, 3, 0, 2), # x_l0l5[0], 100ms, value, bidi
 (25, 3, 2, 2), # x_l0l5[0], 100ms, std, bidi
 (33, 4, 8, 0), # x_l4l5[0], 125ms, velocity, fwd
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 """
 Compute HTP 12D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
 r3: (B,T,49) raw R³ features

 Returns:
 (B,T,12) HTP output
 """
 # R³ features
 amplitude = r3[..., 7:8]
 spectral_centroid = r3[..., 9:10]
 spectral_flux = r3[..., 10:11]
 tristimulus = r3[..., 18:21] # (B, T, 3)
 x_l0l5 = r3[..., 25:33] # (B, T, 8)
 x_l4l5 = r3[..., 33:41] # (B, T, 8)
 x_l5l7 = r3[..., 41:49] # (B, T, 8)

 # Mechanism sub-sections
 # H³ direct features
 flux_period_100ms = h3_direct[(10, 3, 14, 2)].unsqueeze(-1)
 pitch_vel_125ms = h3_direct[(9, 4, 8, 0)].unsqueeze(-1)
 x_l5l7_coupling_500ms = h3_direct[(41, 8, 0, 0)].unsqueeze(-1)
 x_l5l7_mean_1s = h3_direct[(41, 16, 1, 0)].unsqueeze(-1)
 x_l0l5_coupling_100ms = h3_direct[(25, 3, 0, 2)].unsqueeze(-1)
 x_l4l5_velocity = h3_direct[(33, 4, 8, 0)].unsqueeze(-1)

 # ═══ LAYER E: Explicit features ═══

 # f01: High-Level Lead (coefficients sum = 1.0)
 f01 = torch.sigmoid(
 + 0.35 * x_l5l7_mean_1s
 + 0.25 * x_l5l7_coupling_500ms
 )

 # f02: Mid-Level Lead (coefficients sum = 1.0)
 f02 = torch.sigmoid(
 + 0.30 * pitch_vel_125ms
 + 0.30 * x_l4l5_velocity
 )

 # f03: Low-Level Lead (coefficients sum = 1.0)
 f03 = torch.sigmoid(
 + 0.35 * flux_period_100ms
 + 0.25 * x_l0l5_coupling_100ms
 )

 # f04: Hierarchy Gradient (coefficients sum = 1.0)
 f04 = torch.sigmoid(
 0.50 * (f01 - f03)
 )

 # ═══ LAYER M: Mathematical ═══
 latency_high = torch.sigmoid(
 )
 latency_mid = torch.sigmoid(
 )
 latency_low = torch.sigmoid(
 )

 # ═══ LAYER P: Present ═══

 # ═══ LAYER F: Future ═══
 abstract_future = torch.sigmoid(
 0.5 * f01 + 0.5 * x_l5l7_mean_1s
 )
 midlevel_future = torch.sigmoid(
 0.5 * f02 + 0.5 * pitch_vel_125ms
 )

 return torch.cat([
 f01, f02, f03, f04, # E: 4D
 latency_high, latency_mid, latency_low, # M: 3D
 sensory_match, pitch_prediction, abstract_prediction, # P: 3D
 abstract_future, midlevel_future, # F: 2D
 ], dim=-1) # (B, T, 12)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 15 (6 empirical + 5 reviews + 4 theoretical/computational) | Deep C³ literature search |
| **Effect Sizes** | 4+ | ηp²=0.49, η²=0.86, d=-1.63, multiple p<0.001 |
| **Evidence Modality** | MEG, iEEG, ECoG, EEG, single-unit, behavioral | Multi-modal convergence |
| **Falsification Tests** | 5/5 testable, 2 confirmed | High validity |
| **R³ Features Used** | ~20D of 49D | Energy + timbre + change + interactions |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **Output Dimensions** | **12D** | 4-layer structure |

---

## 13. Scientific References

1. **de Vries, I. E. J., & Wurm, M. F. (2023)**. Predictive neural representations of naturalistic dynamic input. *Nature Communications*, 14, 3858. https://doi.org/10.1038/s41467-023-39355-y
2. **Norman-Haignere, S. V., Long, L. K., Devinsky, O., Doyle, W., Irobunda, I., Merricks, E. M., ... & Mesgarani, N. (2022)**. Multiscale temporal integration organizes hierarchical computation in human auditory cortex. *Nature Human Behaviour*, 6(3), 455-469. https://doi.org/10.1038/s41562-021-01261-y
3. **Bonetti, L., Fernandez-Rubio, G., Carlomagno, F., Dietz, M., Pantazis, D., Vuust, P., & Kringelbach, M. L. (2024)**. Spatiotemporal brain hierarchies of auditory memory recognition and predictive coding. *Nature Communications*, 15, 4313. https://doi.org/10.1038/s41467-024-48302-4
4. **Golesorkhi, M., Gomez-Pilar, J., Tumati, S., Fraser, M., & Northoff, G. (2021)**. Temporal hierarchy of intrinsic neural timescales converges with spatial core-periphery organization. *Communications Biology*, 4, 277. https://doi.org/10.1038/s42003-021-01785-z
5. **Forseth, K. J., Hickok, G., Rollo, P. S., & Tandon, N. (2020)**. Language prediction mechanisms in human auditory cortex. *Nature Communications*, 11, 5240. https://doi.org/10.1038/s41467-020-19010-6
6. **Norman-Haignere, S. V., Keshishian, M., Devinsky, O., Doyle, W., McKhann, G. M., Schevon, C. A., Flinker, A., & Mesgarani, N. (2024)**. Temporal integration in human auditory cortex is predominantly yoked to absolute time, not structure duration. *bioRxiv*. https://doi.org/10.1101/2024.09.23.614358
7. **Ye, H., Song, P., Xu, H., Li, Q., Chen, Y., Zhai, Y., ... & Yu, X. (2025)**. Hierarchical temporal processing in the primate thalamocortical system: Insights from nonlinguistic structured stimuli. *Research*, 8, Article 0960. https://doi.org/10.34133/research.0960
8. **Sabat, M., Gouyette, H., Gaucher, Q., Lopez Espejo, M., David, S. V., Norman-Haignere, S. V., & Boubenec, Y. (2025)**. Neurons in auditory cortex integrate information within constrained temporal windows that are invariant to the stimulus context and information rate. *bioRxiv*. https://doi.org/10.1101/2025.02.14.637944
9. **Carbajal, G. V., & Malmierca, M. S. (2018)**. The neuronal basis of predictive coding along the auditory pathway: From the subcortical roots to cortical deviance detection. *Trends in Hearing*, 22, 1-33. https://doi.org/10.1177/2331216518784822
10. **Millidge, B., Seth, A. K., & Buckley, C. L. (2022)**. Predictive coding: A theoretical and experimental review. *arXiv:2107.12979v4*.
11. **Fong, C. Y., Law, W. H. C., Uka, T., & Koike, S. (2020)**. Auditory mismatch negativity under predictive coding framework and its role in psychotic disorders. *Frontiers in Psychiatry*, 11, 557932. https://doi.org/10.3389/fpsyt.2020.557932
12. **Ross, J. M., & Balasubramaniam, R. (2022)**. Time perception for musical rhythms: Sensorimotor perspectives on entrainment, simulation, and prediction. *Frontiers in Integrative Neuroscience*, 16, 916220. https://doi.org/10.3389/fnint.2022.916220
13. **Egermann, H., Pearce, M. T., Wiggins, G. A., & McAdams, S. (2013)**. Probabilistic models of expectation violation predict psychophysiological emotional responses to live concert music. *Cognitive, Affective, & Behavioral Neuroscience*, 13, 533-553. https://doi.org/10.3758/s13415-013-0161-y
14. **Rimmele, J. M., Poeppel, D., & Ghitza, O. (2021)**. Acoustically driven cortical delta oscillations underpin prosodic chunking. *eNeuro*, 8(4), ENEURO.0562-20.2021. https://doi.org/10.1523/ENEURO.0562-20.2021
15. **Schilling, A., Sedley, W., Gerum, R., Metzner, C., Tziridis, K., Maier, A., ... & Krauss, P. (2023)**. Predictive coding and stochastic resonance as fundamental principles of auditory phantom perception. *Brain*, 146, 4809-4825. https://doi.org/10.1093/brain/awad255
16. **Asilador, A., & Llano, D. A. (2021)**. Top-down inference in the auditory system: Potential roles for corticofugal projections. *Frontiers in Neural Circuits*, 14, 615259. https://doi.org/10.3389/fncir.2020.615259

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Low-level signal | S⁰.L0[0:4] + S⁰.X_L0L1[128:136] + HC⁰.OSC | R³[7] amplitude + R³[25:33] x_l0l5 |
| Mid-level signal | S⁰.L4[15:19] + S⁰.X_L4L5[192:200] + HC⁰.TIH | R³[9] spectral_centroid + R³[33:41] x_l4l5 |
| High-level signal | S⁰.L9[104:128] + S⁰.X_L5L9[224:232] + HC⁰.EFC | R³[41:49] x_l5l7 |
| Binding | S⁰.L6[68:71] + HC⁰.BND | prediction_buffer[20:30] |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 42/2304 = 1.82% | 18/2304 = 0.78% |
| Output | 12D | 12D (same) |

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **12D**
**Evidence Tier**: **α (Mechanistic)**
**Confidence**: **>90%**
