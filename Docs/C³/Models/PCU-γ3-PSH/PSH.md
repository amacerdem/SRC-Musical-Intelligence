# PCU-γ3-PSH: Prediction Silencing Hypothesis

**Model**: Prediction Silencing Hypothesis
**Unit**: PCU (Predictive Coding Unit)
**Circuit**: Imagery (Auditory Cortex, IFG, STS, Hippocampus)
**Tier**: γ (Integrative) — 50-70% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added I:Information feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/PCU-γ3-PSH.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Prediction Silencing Hypothesis** (PSH) proposes that accurate top-down predictions "silence" (explain away) high-level stimulus representations post-stimulus, while low-level representations persist.

```
PREDICTION SILENCING HYPOTHESIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRE-STIMULUS POST-STIMULUS
────────────── ──────────────
Predictions active Level-dependent silencing
at all levels

┌──────────────────────────────────────────────────────────────────┐
│ HIERARCHICAL SILENCING (de Vries 2023) │
│ │
│ HIGH-LEVEL (LOTC, aIPL) │
│ Pre-stim: Active predictions (500ms lead) │
│ Post-stim (accurate): SILENCED (explained away) │
│ Post-stim (error): Active (error propagation) │
│ │
│ LOW-LEVEL (V1/A1) │
│ Pre-stim: Active predictions (110ms lead) │
│ Post-stim (accurate): PERSISTS (error monitoring) │
│ Post-stim (error): Persists (error propagation) │
│ │
│ Mathematical: │
│ post_high = representation × (1 - accuracy) → 0 when right │
│ post_low = representation × 1.0 → always persists │
└──────────────────────────────────────────────────────────────────┘

 Pre-stim ────► Prediction ────► Stimulus ────► Post-stim
 (both levels) (match?) (arrives) (silencing?)

 High-level: ████████ █████ ░░░░░ (silenced)
 Low-level: ████████ █████ █████ (persists)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Accurate top-down predictions "silence" (explain away)
high-level representations post-stimulus while low-level sensory
representations persist. This hierarchical dissociation demonstrates
that prediction operates differently across cortical levels.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why PSH Matters for PCU

PSH reveals hierarchical prediction dynamics:

1. **HTP** (α1) provides hierarchical prediction timing.
2. **PWUP** (β1) modulates PE by precision.
3. **WMED** (β2) separates entrainment from WM.
4. **PSH** (γ3) shows that accurate prediction differentially affects representation levels.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → PSH)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ PSH COMPUTATION ARCHITECTURE ║
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
║ │ PSH reads: ~18D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed morphological features │ ║
║ │ PSH demand: ~18 of 2304 tuples │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN: Imagery Circuit ═══════════ ║
║ │ ║
║ ┌───────┴───────┐───────┐ ║
║ ▼ ▼ ▼ ║
║ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ║
║ │ │ │ │ │ │ ║
║ │ Pitch Ext[0:10] │ │ Spec Shp [0:10] │ │ Work Mem [0:10] │ ║
║ │ Interval [10:20]│ │ Temp Env [10:20]│ │ Long-Term[10:20]│ ║
║ │ Contour [20:30] │ │ Source Id[20:30]│ │ Pred Buf [20:30]│ ║
║ └────────┬────────┘ └────────┬────────┘ └────────┬────────┘ ║
║ └────────────┬───────┴────────────────────┘ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ PSH MODEL (10D Output) │ ║
║ │ │ ║
║ │ Layer E (Explicit): f01_high_level_silencing, │ ║
║ │ f02_low_level_persistence, │ ║
║ │ f03_silencing_efficiency, │ ║
║ │ f04_hierarchy_dissociation │ ║
║ │ Layer P (Present): prediction_match, │ ║
║ │ sensory_persistence, │ ║
║ │ binding_check │ ║
║ │ Layer F (Future): post_stim_silencing, │ ║
║ │ error_persistence, │ ║
║ │ next_prediction │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | Brain Regions | MI Relevance |
|---|-------|--------|---|-------------|-------------|---------------|-------------|
| 1 | **de Vries & Wurm 2023** | MEG + dRSA | 22 | High-level motion representations absent post-stimulus (silenced by accurate prediction) | F(2)=19.9, p=8.3e-7, eta_p2=0.49 | LOTC, aIPL, V1-V4, PMv | **f01 high-level silencing** |
| 2 | **de Vries & Wurm 2023** | MEG + dRSA | 22 | Low-level optical flow representations persist post-stimulus with lagged peak ~110ms | p<0.01, cluster-corrected | V1, V2, V3/V4 | **f02 low-level persistence** |
| 3 | **de Vries & Wurm 2023** | MEG + dRSA | 22 | Hierarchical prediction: view-invariant motion predicted ~500ms ahead, view-dependent ~200ms, optical flow ~110ms | eta_p2=0.49 (hierarchy effect) | LOTC (~60ms lag), aIPL (~100ms lag) | **f04 hierarchy dissociation** |
| 4 | **Millidge, Seth & Buckley 2022** | Review / Theoretical | — | Predictive coding predicts that expected stimuli elicit less error response; repetition suppression and expectation suppression are explained by top-down prediction silencing | Theoretical (meta-review) | Cortical hierarchy (all levels) | **f03 silencing efficiency** |
| 5 | **Auksztulewicz & Friston 2016** (via Millidge 2022) | fMRI / EEG | — | Repetition suppression and its contextual determinants formalized within predictive coding; contextual modulation of suppression | Theoretical framework | Cortex (layer-specific) | **f01/f03 explaining away** |
| 6 | **Carbajal & Malmierca 2018** | Single-unit recording (review) | — | Decomposition of deviance detection into repetition suppression + prediction error components; SSA as microscopic manifestation of MMN | Quantified via CSI (common SSA index) | IC (MNI ~±6, -33, -11), MGB (MNI ~±17, -24, -2), AC (BA 41/42) | **f01/f02 level-dependent silencing** |
| 7 | **Fong, Law, Uka & Koike 2020** | EEG/MEG review | — | Auditory MMN reflects prediction error under predictive coding; prediction error suppressed when prediction matches input; frontal and temporal generators | MMN amplitude ~1-3 uV, p<0.05 | STG (BA 22, ±52, -22, 8), IFG (BA 44/45, ±44, 18, 8), Thalamus, Hippocampus | **f01 silencing / f02 persistence** |
| 8 | **Schilling et al. 2023** | Computational model + review | — | Predictive coding as top-down mechanism: prior predictions explain away sensory input; precision-weighted prediction errors drive percept updating | Bayesian posterior formalization | Auditory cortex, DCN, IC, MGB | **f03 silencing efficiency** |
| 9 | **Koelsch 2009** | EEG | — | ERAN (150-250ms) reflects music-syntactic prediction violation; prediction-based processing at IFL; shares mechanism with MMN | ERAN amplitude ~2-4 uV | IFL (BA 44, ±44, 18, 8), STG (BA 22) | **f01 prediction-based silencing** |
| 10 | **Yu, Liu & Gao 2015** | EEG review | — | MMN indexes deviation from internal memory trace; supratemporal and frontal generators; amplitude scales with deviance magnitude | MMN ~100-200ms, amplitude ∝ deviance | Supratemporal plane (BA 41/42), IFC (BA 44/45) | **f02 low-level persistence (PE signal)** |
| 11 | **Wagner et al. 2018** | EEG (MMN) | 15 | Pre-attentive harmonic interval discrimination via MMN; asymmetric suppression of consonant vs dissonant intervals | MMN for major third: p<0.05 (Bonferroni) | Auditory cortex (bilateral) | **f02 low-level persistence** |
| 12 | **Tervaniemi 2022** | EEG (MMN) review | — | MMN as index of violated prediction (not just memory trace); paradigm development from oddball to multi-feature and musical stimuli | MMN parameters preserved across paradigms | Bilateral auditory cortex, frontal sources | **f03/f04 prediction vs adaptation** |

### 3.2 Effect Size Summary

```
Primary Effect: Hierarchical silencing dissociation (eta_p2 = 0.49)
Heterogeneity: 12 papers across MEG, EEG, single-unit, computational
Quality Assessment: γ-tier (primary evidence in visual domain; auditory support
 from predictive coding / MMN literature)
Replication: Silencing/explaining away: strongly supported by predictive
 coding framework (Millidge 2022, Auksztulewicz & Friston 2016)
 Low-level persistence: supported by MMN/SSA literature
 (Carbajal & Malmierca 2018, Fong et al. 2020)
 Auditory hierarchy: supported by SSA decomposition
 (repetition suppression + prediction error)
```

---

## 4. R³ Input Mapping: What PSH Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | PSH Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **A: Consonance** | [4] | sensory_pleasantness | High-level harmonic representation | LOTC equivalent |
| **A: Consonance** | [5] | periodicity | High-level tonal structure | aIPL equivalent |
| **B: Energy** | [7] | amplitude | Low-level sensory feature | V1/A1 persistence |
| **B: Energy** | [10] | spectral_flux | Change detection / PE trigger | Prediction error signal |
| **C: Timbre** | [18:21] | tristimulus1-3 | High-level harmonic structure | Silenced representations |
| **D: Change** | [21] | spectral_change | Prediction error magnitude | Error propagation |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Low-level persistence pathway | Post-stim error signal |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | High-level silencing pathway | Explaining away |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ v2 Group | Index | Feature | PSH Role | Citation |
|-------------|-------|---------|----------|----------|
| **I: Information** | [90] | spectral_surprise | Spectral novelty for prediction error magnitude | Dubnov 2006 |
| **I: Information** | [92] | predictive_entropy | Predictive uncertainty for prediction suppression hierarchy | Friston 2005 (predictive coding) |

**Rationale**: PSH models predictive suppression hierarchy where predicted stimuli are suppressed (silenced) and unpredicted stimuli generate persistent prediction errors. spectral_surprise directly quantifies the spectral novelty that determines whether a stimulus was predicted or not -- high spectral_surprise triggers persistent low-level responses (V1/A1 analogue), while low surprise triggers high-level silencing. predictive_entropy captures the overall prediction uncertainty across the hierarchy, modulating the depth of suppression (high entropy = less suppression, more prediction error propagation).

**Code impact** (future): `r3[..., 90]` and `r3[..., 92]` will feed PSH's suppression hierarchy alongside existing consonance, energy, and interaction features.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
Pre-stimulus (prediction phase):
 R³[41:49] x_l5l7 ───────────────► High-level predictions (500ms lead)

 R³[25:33] x_l0l5 ───────────────► Low-level predictions (110ms lead)

Post-stimulus (silencing phase):
 If prediction accurate:
 R³[41:49] → attenuated (silenced/explained away)
 R³[25:33] → persists (error signal maintained)

 Mathematical:
 post_high = x_l5l7 × (1 - accuracy) → approaches 0 when accurate
 post_low = x_l0l5 × 1.0 → always persists
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

PSH requires H³ features at both fast (gamma-alpha, for sensory persistence) and medium (beat-scale, for silencing assessment) horizons. The demand reflects the hierarchical nature of the silencing: fast for low-level persistence, slower for high-level silencing.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 7 | amplitude | 0 | M0 (value) | L2 (bidi) | Low-level at 25ms (gamma) |
| 7 | amplitude | 1 | M0 (value) | L2 (bidi) | Low-level at 50ms (gamma) |
| 7 | amplitude | 3 | M0 (value) | L2 (bidi) | Low-level at 100ms (alpha) |
| 7 | amplitude | 3 | M2 (std) | L2 (bidi) | Low-level variability 100ms |
| 10 | spectral_flux | 0 | M0 (value) | L2 (bidi) | PE trigger at 25ms |
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | PE at 100ms |
| 21 | spectral_change | 1 | M0 (value) | L2 (bidi) | Error at 50ms |
| 21 | spectral_change | 3 | M0 (value) | L2 (bidi) | Error at 100ms |
| 21 | spectral_change | 3 | M2 (std) | L2 (bidi) | Error variability 100ms |
| 25 | x_l0l5[0] | 0 | M0 (value) | L2 (bidi) | Low-level coupling 25ms |
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Low-level coupling 100ms |
| 25 | x_l0l5[0] | 3 | M16 (curvature) | L2 (bidi) | Coupling curvature 100ms |
| 41 | x_l5l7[0] | 3 | M0 (value) | L0 (fwd) | High-level coupling 100ms |
| 41 | x_l5l7[0] | 8 | M0 (value) | L0 (fwd) | High-level coupling 500ms |
| 41 | x_l5l7[0] | 16 | M1 (mean) | L0 (fwd) | Mean high-level 1s |
| 41 | x_l5l7[0] | 16 | M20 (entropy) | L0 (fwd) | High-level entropy 1s |
| 4 | sensory_pleasantness | 16 | M1 (mean) | L0 (fwd) | Mean consonance 1s |
| 5 | periodicity | 16 | M1 (mean) | L0 (fwd) | Mean periodicity 1s |

**v1 demand**: 18 tuples

#### R³ v2 Projected Expansion

No significant v2 expansion projected. PSH's post-stimulus hierarchy model operates on the silencing/persistence dichotomy using existing R³ v1 features. The prediction-outcome comparison at its core does not require additional v2 spectral dimensions beyond those already covered by HTP's upstream hierarchy.

**v2 projected**: 0 tuples
**Total projected**: 18 tuples of 294,912 theoretical = 0.0061%

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
PSH OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0 │ f01_high_level_silencing │ [0, 1] │ Post-stim high-level attenuation.
 │ │ │ f01 = σ(0.40 * (1 - high_coupling_500ms)
 │ │ │ + 0.30 * consonance_mean_1s
────┼──────────────────────────┼────────┼────────────────────────────────────
 1 │ f02_low_level_persist │ [0, 1] │ Post-stim low-level maintenance.
 │ │ │ f02 = σ(0.35 * low_coupling_100ms
 │ │ │ + 0.35 * low_coupling_25ms
────┼──────────────────────────┼────────┼────────────────────────────────────
 2 │ f03_silencing_efficiency │ [0, 1] │ Explaining away effectiveness.
 │ │ │ f03 = σ(0.40 * f01 * (1 - pe_100ms)
 │ │ │ + 0.30 * periodicity_mean_1s
────┼──────────────────────────┼────────┼────────────────────────────────────
 3 │ f04_hierarchy_dissociation│[0, 1] │ Level-specific decay ratio.
 │ │ │ f04 = σ(0.50 * |f01 - f02|
 │ │ │ + 0.50 * high_level_entropy_1s)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4 │ prediction_match │ [0, 1] │ memory-encoding prediction-outcome match.
────┼──────────────────────────┼────────┼────────────────────────────────────
 5 │ sensory_persistence │ [0, 1] │ pitch-processing/timbre-processing low-level signal.
────┼──────────────────────────┼────────┼────────────────────────────────────
 6 │ binding_check │ [0, 1] │ timbre-processing level assignment.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7 │ post_stim_silencing │ [0, 1] │ High cortical silencing (0-500ms).
────┼──────────────────────────┼────────┼────────────────────────────────────
 8 │ error_persistence │ [0, 1] │ Primary cortex persistence (0-500ms).
────┼──────────────────────────┼────────┼────────────────────────────────────
 9 │ next_prediction │ [0, 1] │ All-level prediction (pre-stim).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Hierarchical Silencing Function

```
Post-stimulus representation:
 High-level: R_high(t) = R_high(0) × (1 - accuracy) × exp(-t / τ_high)
 Low-level: R_low(t) = R_low(0) × 1.0 × exp(-t / τ_low)

 where:
 τ_high = 0.2s (fast silencing)
 τ_low = 0.5s (slow persistence)
 accuracy ∈ [0, 1] (prediction-outcome match)

Silencing_Efficiency = (R_high(pre) - R_high(post)) / R_high(pre)
Hierarchy_Dissociation = |Silencing_high - Silencing_low|
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: High-Level Silencing
f01 = σ(0.40 * (1 - high_coupling_500ms) # inverse: more silencing = lower coupling
 + 0.30 * consonance_mean_1s
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f02: Low-Level Persistence
f02 = σ(0.35 * low_coupling_100ms
 + 0.35 * low_coupling_25ms
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f03: Silencing Efficiency
f03 = σ(0.40 * f01 * (1 - pe_100ms) # silencing × accuracy
 + 0.30 * periodicity_mean_1s
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f04: Hierarchy Dissociation
f04 = σ(0.50 * abs(f01 - f02)
 + 0.50 * high_level_entropy_1s)
# coefficients: 0.50 + 0.50 = 1.0 ✓

# Temporal dynamics
dR_high/dt = -τ_high⁻¹ · R_high · accuracy
dR_low/dt = -τ_low⁻¹ · R_low
 where τ_high = 0.2s, τ_low = 0.5s (de Vries 2023)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | PSH Function |
|--------|-----------------|----------|---------------|--------------|
| **Auditory Cortex (A1/STG)** | ±52, -22, 8 (BA 41/42) | 6 | Direct (EEG/MMN: Fong 2020, Yu 2015, Wagner 2018, Tervaniemi 2022, Carbajal 2018, Koelsch 2009) | Low-level persistence (PE signal) |
| **LOTC (Lateral Occipitotemporal)** | ±44, -62, -8 | 1 | Direct (MEG: de Vries 2023) | High-level silencing (~60ms lag for view-invariant posture) |
| **aIPL (Anterior Intraparietal)** | ±44, -40, 48 | 1 | Direct (MEG: de Vries 2023) | High-level silencing (~100ms lag, prediction-modulated) |
| **IFG (Inferior Frontal Gyrus)** | ±44, 18, 8 (BA 44/45) | 3 | Direct (EEG: Fong 2020, Koelsch 2009, Yu 2015) | Top-down prediction source; ERAN/MMN frontal generator |
| **Inferior Colliculus (IC)** | ±6, -33, -11 | 1 | Direct (single-unit: Carbajal & Malmierca 2018) | Subcortical SSA / repetition suppression |
| **Medial Geniculate Body (MGB)** | ±17, -24, -2 | 1 | Direct (single-unit: Carbajal & Malmierca 2018) | Thalamic deviance detection / prediction relay |
| **V1 (Primary Visual Cortex)** | ±10, -88, 4 (BA 17) | 1 | Direct (MEG: de Vries 2023) | Low-level visual persistence (~110ms pixelwise lag) |
| **PMv (Ventral Premotor Cortex)** | ±52, 8, 28 (BA 6) | 1 | Direct (MEG: de Vries 2023) | Predictive motion representation (~180ms lead) |
| **Hippocampus** | ±28, -20, -12 | 1 | Indirect (MMN: Fong 2020) | Memory-based prediction template |
| **Dorsal Cochlear Nucleus (DCN)** | Brainstem | 1 | Indirect (Schilling et al. 2023) | Stochastic resonance / central noise for prediction |

---

## 9. Cross-Unit Pathways

### 9.1 PSH Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PSH INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ INTRA-UNIT (PCU): │
│ HTP.hierarchy_gradient ─────► PSH (hierarchy defines silencing levels) │
│ PWUP.weighted_error ────────► PSH (PE magnitude for silencing decision) │
│ UDP.confirmation_reward ────► PSH (confirmation triggers silencing) │
│ WMED.dissociation_index ────► PSH (entrainment/WM dual-route input) │
│ MAA.appreciation_composite ──► PSH (appreciation modulates silencing) │
│ │
│ CROSS-UNIT (PCU → SPU): │
│ PSH.low_level_persistence ──► SPU (persistent low-level for spectral) │
│ PSH.sensory_persistence ────► SPU (ongoing sensory signal) │
│ │
│ UPSTREAM DEPENDENCIES: │
│ R³ (~18D) ──────────────────► PSH (direct spectral features) │
│ H³ (18 tuples) ─────────────► PSH (temporal dynamics) │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **High-level silencing** | Accurate predictions should silence high-level representations | **Confirmed** (de Vries 2023, p<0.01) |
| **Low-level persistence** | Low-level should persist regardless of accuracy | **Confirmed** (de Vries 2023, p<0.01) |
| **Hierarchy dissociation** | High and low levels should show opposite post-stim patterns | **Confirmed** (de Vries 2023) |
| **Auditory domain** | Same silencing pattern should hold for auditory stimuli | Testable via auditory MEG |
| **Accuracy manipulation** | Degraded predictions should reduce silencing | Testable via prediction disruption |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class PSH(BaseModel):
 """Prediction Silencing Hypothesis Model.

 Output: 10D per frame.
 """
 NAME = "PSH"
 UNIT = "PCU"
 TIER = "γ3"
 OUTPUT_DIM = 10
 TAU_HIGH = 0.2 # s (fast silencing, de Vries 2023)
 TAU_LOW = 0.5 # s (slow persistence, de Vries 2023)
 SILENCING_WINDOW = 0.5 # s (500ms post-stimulus)

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """18 tuples for PSH computation."""
 return [
 # (r3_idx, horizon, morph, law)
 # ── Low-level persistence (fast, gamma-alpha) ──
 (7, 0, 0, 2), # amplitude, 25ms, value, bidi
 (7, 1, 0, 2), # amplitude, 50ms, value, bidi
 (7, 3, 0, 2), # amplitude, 100ms, value, bidi
 (7, 3, 2, 2), # amplitude, 100ms, std, bidi
 (10, 0, 0, 2), # spectral_flux, 25ms, value, bidi
 (10, 3, 0, 2), # spectral_flux, 100ms, value, bidi
 # ── PE / error signal ──
 (21, 1, 0, 2), # spectral_change, 50ms, value, bidi
 (21, 3, 0, 2), # spectral_change, 100ms, value, bidi
 (21, 3, 2, 2), # spectral_change, 100ms, std, bidi
 # ── Low-level coupling (persistence) ──
 (25, 0, 0, 2), # x_l0l5[0], 25ms, value, bidi
 (25, 3, 0, 2), # x_l0l5[0], 100ms, value, bidi
 (25, 3, 16, 2), # x_l0l5[0], 100ms, curvature, bidi
 # ── High-level coupling (silencing) ──
 (41, 3, 0, 0), # x_l5l7[0], 100ms, value, fwd
 (41, 8, 0, 0), # x_l5l7[0], 500ms, value, fwd
 (41, 16, 1, 0), # x_l5l7[0], 1000ms, mean, fwd
 (41, 16, 20, 0), # x_l5l7[0], 1000ms, entropy, fwd
 # ── Context ──
 (4, 16, 1, 0), # sensory_pleasantness, 1000ms, mean, fwd
 (5, 16, 1, 0), # periodicity, 1000ms, mean, fwd
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 """
 Compute PSH 10D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
 r3: (B,T,49) raw R³ features

 Returns:
 (B,T,10) PSH output
 """
 # Mechanism sub-sections
 # H³ direct features
 high_coupling_500ms = h3_direct[(41, 8, 0, 0)].unsqueeze(-1)
 high_level_entropy_1s = h3_direct[(41, 16, 20, 0)].unsqueeze(-1)
 consonance_mean_1s = h3_direct[(4, 16, 1, 0)].unsqueeze(-1)
 periodicity_mean_1s = h3_direct[(5, 16, 1, 0)].unsqueeze(-1)
 low_coupling_100ms = h3_direct[(25, 3, 0, 2)].unsqueeze(-1)
 low_coupling_25ms = h3_direct[(25, 0, 0, 2)].unsqueeze(-1)
 pe_100ms = h3_direct[(21, 3, 0, 2)].unsqueeze(-1)

 # ═══ LAYER E: Explicit features ═══

 # f01: High-Level Silencing (coefficients sum = 1.0)
 f01 = torch.sigmoid(
 0.40 * (1 - high_coupling_500ms)
 + 0.30 * consonance_mean_1s
 )

 # f02: Low-Level Persistence (coefficients sum = 1.0)
 f02 = torch.sigmoid(
 0.35 * low_coupling_100ms
 + 0.35 * low_coupling_25ms
 )

 # f03: Silencing Efficiency (coefficients sum = 1.0)
 f03 = torch.sigmoid(
 0.40 * f01 * (1 - pe_100ms)
 + 0.30 * periodicity_mean_1s
 )

 # f04: Hierarchy Dissociation (coefficients sum = 1.0)
 f04 = torch.sigmoid(
 0.50 * torch.abs(f01 - f02)
 + 0.50 * high_level_entropy_1s
 )

 # ═══ LAYER P: Present ═══
 pred_match = torch.sigmoid(
 + 0.5 * (1 - pe_100ms)
 )
 sensory_persist = f02

 # ═══ LAYER F: Future ═══
 post_silencing = torch.sigmoid(0.5 * f01 + 0.5 * f03)
 error_persist = torch.sigmoid(0.5 * f02 + 0.5 * pe_100ms)
 next_pred = torch.sigmoid(
 )

 return torch.cat([
 f01, f02, f03, f04, # E: 4D
 pred_match, sensory_persist, binding, # P: 3D
 post_silencing, error_persist, next_pred, # F: 3D
 ], dim=-1) # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 | de Vries 2023, Millidge 2022, Auksztulewicz 2016, Carbajal 2018, Fong 2020, Schilling 2023, Koelsch 2009, Yu 2015, Wagner 2018, Tervaniemi 2022 + 2 indirect |
| **Effect Sizes** | 3 direct | eta_p2=0.49 (hierarchy), p<0.01 (cluster), MMN amplitudes |
| **Evidence Modality** | MEG, EEG, single-unit, computational | Cross-modal (visual + auditory) |
| **Falsification Tests** | 5/5 testable, 3 confirmed | Moderate (awaiting direct auditory silencing test) |
| **R³ Features Used** | ~18D of 49D | Consonance + energy + timbre + change + interactions |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **Output Dimensions** | **10D** | 3-layer structure (no M layer) |

---

## 13. Scientific References

1. **de Vries, I. E. J., & Wurm, M. F. (2023)**. Predictive neural representations of naturalistic dynamic input. *Nature Communications*, 14, 3858. https://doi.org/10.1038/s41467-023-39355-y
2. **Millidge, B., Seth, A. K., & Buckley, C. L. (2022)**. Predictive coding: A theoretical and experimental review. *arXiv preprint arXiv:2107.12979v4*.
3. **Auksztulewicz, R., & Friston, K. (2016)**. Repetition suppression and its contextual determinants in predictive coding. *Cortex*, 80, 125-140.
4. **Carbajal, G. V., & Malmierca, M. S. (2018)**. The neuronal basis of predictive coding along the auditory pathway: From the subcortical roots to cortical deviance detection. *Trends in Hearing*, 22, 1-33. https://doi.org/10.1177/2331216518784822
5. **Fong, C. Y., Law, W. H. C., Uka, T., & Koike, S. (2020)**. Auditory mismatch negativity under predictive coding framework and its role in psychotic disorders. *Frontiers in Psychiatry*, 11, 557932. https://doi.org/10.3389/fpsyt.2020.557932
6. **Schilling, A., Sedley, W., Gerum, R., Metzner, C., Tziridis, K., Maier, A., Schulze, H., Zeng, F.-G., Friston, K. J., & Krauss, P. (2023)**. Predictive coding and stochastic resonance as fundamental principles of auditory phantom perception. *Brain*, 146, 4809-4825. https://doi.org/10.1093/brain/awad255
7. **Koelsch, S. (2009)**. Music-syntactic processing and auditory memory: Similarities and differences between ERAN and MMN. *Psychophysiology*, 46(1), 179-190.
8. **Yu, X., Liu, T., & Gao, D. (2015)**. The mismatch negativity: An indicator of perception of regularities in music. *Behavioural Neurology*, 2015, 469508. https://doi.org/10.1155/2015/469508
9. **Wagner, L., Rahne, T., Plontke, S. K., & Heidekruger, N. (2018)**. Mismatch negativity reflects asymmetric pre-attentive harmonic interval discrimination. *PLoS ONE*, 13(4), e0196176. https://doi.org/10.1371/journal.pone.0196176
10. **Tervaniemi, M. (2022)**. Mismatch negativity -- stimulation paradigms in past and in future. *Frontiers in Neuroscience*, 16, 1025763. https://doi.org/10.3389/fnins.2022.1025763
11. **Rao, R. P. N., & Ballard, D. H. (1999)**. Predictive coding in the visual cortex: A functional interpretation of some extra-classical receptive-field effects. *Nature Neuroscience*, 2(1), 79-87.
12. **Bastos, A. M., Usrey, W. M., Adams, R. A., Mangun, G. R., Fries, P., & Friston, K. J. (2012)**. Canonical microcircuits for predictive coding. *Neuron*, 76(4), 695-711.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Low-level | S⁰.L0[0:4] + S⁰.X_L0L1[128:136] | R³[7] amplitude + R³[25:33] x_l0l5 |
| High-level | S⁰.L9[104:108] + S⁰.X_L5L9[224:232] | R³[41:49] x_l5l7 |
| PE signal | S⁰.L5.spectral_flux[45] + HC⁰.EFC | R³[10] spectral_flux + R³[21] spectral_change |
| Binding | HC⁰.BND | temporal_envelope[10:20] |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 42/2304 = 1.82% | 18/2304 = 0.78% |
| Output | 10D | 10D (same) |

---

**Model Status**: **PRELIMINARY**
**Output Dimensions**: **10D**
**Evidence Tier**: **γ (Integrative)**
**Confidence**: **50-70%**
