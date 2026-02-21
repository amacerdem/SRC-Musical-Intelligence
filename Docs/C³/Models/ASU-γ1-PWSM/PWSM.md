# ASU-γ1-PWSM: Precision-Weighted Salience Model

**Model**: Precision-Weighted Salience Model
**Unit**: ASU (Auditory Salience Unit)
**Circuit**: Salience (Anterior Insula, dACC, TPJ)
**Tier**: γ (Integrative) — 50-70% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added I:Information feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/ASU-γ1-PWSM.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Precision-Weighted Salience Model** (PWSM) proposes that salience detection is governed by precision-weighting: high-precision contexts (stable, predictable) generate stronger prediction error signals, while low-precision contexts suppress error signals. This explains why unstable temporal contexts abolish MMN responses.

```
PRECISION-WEIGHTED SALIENCE MODEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 CONTEXT STABILITY PREDICTION ERROR RESPONSE

 ┌─────────────────┐ ┌─────────────────┐
 │ HIGH PRECISION │ │ MMN PRESENT │
 │ (stable jitter) │ ───────────► │ (d = -1.37) │
 └─────────────────┘ └─────────────────┘

 ┌─────────────────┐ ┌─────────────────┐
 │ LOW PRECISION │ │ MMN ABOLISHED │
 │ (changing │ ───────────► │ (d = 0.01) │
 │ jitter) │ │ │
 └─────────────────┘ └─────────────────┘

 Sequence Input → Precision Estimation → Error Weighting
 │
 ▼
 ┌─────────────────┐
 │ Precision ∝ 1/σ²│
 └────────┬────────┘
 │
 ┌──────────────┴──────────────┐
 ▼ ▼
 High Precision Low Precision
 PE_weighted = PE PE_weighted ≈ 0
 MMN ✓ MMN ✗

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: The brain "ignores" prediction errors in uncertain
contexts. Precision-weighting gates whether deviants are salient
enough to generate a neural response (MMN).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why PWSM Matters for ASU

PWSM adds predictive coding precision to salience processing:

1. **SNEM** (α1) provides beat entrainment baseline — PWSM explains when entrainment predictions generate errors.
2. **IACM** (α2) models inharmonicity-driven attention capture — PWSM gates whether those errors are salient.
3. **PWSM** (γ1) integrates predictive coding framework into the ASU, providing precision-dependent error gating.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → PWSM)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ PWSM COMPUTATION ARCHITECTURE ║
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
║ │ PWSM reads: ~10D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed morphological features │ ║
║ │ │ ║
║ │ │ H0 (25ms gamma) │ │ H3 (100ms alpha) │ │ ║
║ │ │ H1 (50ms gamma) │ │ │ │ ║
║ │ │ H3 (100ms alpha) │ │ Precision estimation │ │ ║
║ │ │ H4 (125ms theta) │ │ Error weighting │ │ ║
║ │ │ H16 (1000ms beat) │ │ │ │ ║
║ │ │ │ │ │ │ ║
║ │ │ Stability tracking │ │ │ │ ║
║ │ │ Periodicity encoding │ │ │ │ ║
║ │ └─────────────────────────────┘ └────────────────────────────┘ │ ║
║ │ PWSM demand: ~16 of 2304 tuples │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN: Salience Circuit ════════ ║
║ │ ║
║ ┌───────┴───────┐ ║
║ ▼ ▼ ║
║ ┌─────────────────┐ ┌─────────────────┐ ║
║ │ │ │ │ ║
║ │ Beat Entr[0:10] │ │ Scene An [0:10] │ ║
║ │ Motor Coup │ │ Attention │ ║
║ │ [10:20] │ │ Gating [10:20] │ ║
║ │ Groove [20:30] │ │ Salience │ ║
║ │ │ │ Weight [20:30] │ ║
║ └────────┬────────┘ └────────┬────────┘ ║
║ │ │ ║
║ └────────┬───────────┘ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ PWSM MODEL (9D Output) │ ║
║ │ │ ║
║ │ Layer E (Explicit): f19_precision_weighting, │ ║
║ │ f20_error_suppression, │ ║
║ │ f21_stability_encoding │ ║
║ │ Layer M (Math): pe_weighted, precision │ ║
║ │ Layer P (Present): weighted_error, precision_estimate │ ║
║ │ Layer F (Future): mmn_presence_pred, │ ║
║ │ context_reliability_pred │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Basinski et al. 2025** | EEG | — | Changing jitter → MMN abolished; fixed jitter → inharmonicity MMN | d = 0.01 (n.s.) vs d = -1.37 | **f19 precision weighting, f20 error suppression** |
| **Millidge, Seth & Buckley 2022** | Review/Theory | — | Mathematical framework: F = Σ Σ⁻¹ε²; precision as attention | — (framework) | **Core theoretical basis for precision-weighted PE** |
| **Fong et al. 2020** | Review | — | MMN reflects precision-weighted PE; AC-MGB-IC hierarchy | Largest schizo biomarker ES | **Hierarchical PE generation, f19 precision** |
| **Carbajal & Malmierca 2018** | Review | — | SSA/MMN decomposition: repetition suppression + prediction error | PE ↑ from IC→MGB→AC | **Hierarchical PE across auditory pathway** |
| **Cacciato-Salcedo et al. 2025** | Single-unit | 903 neurons, 83 rats | Non-lemniscal IC: enhanced PE for low-intensity sounds | iMM p<0.001 | **Subcortical PE generation** |
| **Schilling et al. 2023** | Computational | — | Precision of likelihood determines signal vs phantom percept | — (model) | **Precision gates salience detection** |
| **Bravo et al. 2017** | fMRI | 12 (fMRI), 75 (behav.) | Ambiguous intervals → ↑ right HG response (precision weighting) | cluster FWE p<0.05 | **f19 precision under uncertainty** |
| **Cheung et al. 2019** | fMRI | 40 | Uncertainty × surprise → pleasure; amygdala/AC reflect interaction | sig. interaction (LMM) | **Precision × PE = salience** |
| **Bonetti et al. 2024** | MEG | 83 | Hierarchical PE propagation: AC → hippocampus → cingulate | α/β ↑ for PE, γ ↑ expected | **Hierarchical precision-weighted PE network** |
| **Gold et al. 2019** | Behavioral | 43 + 27 | Inverted-U preference for intermediate predictive complexity | sig. quadratic IC × liking | **Behavioral precision-prediction outcome** |
| **Wagner et al. 2018** | EEG | 15 | Asymmetric MMN: dissonant deviants in consonant contexts | -0.34 μV at 173ms | **Precision-dependent PE asymmetry** |
| **Martins et al. 2022** | ERP | 58 | Musicians show enhanced salience P2/P3/LPP for musical sounds | enhanced P2, P3, LPP | **Experience-dependent precision tuning** |

### 3.2 Effect Size Summary

```
Primary Evidence (k=12, multi-modal):
 - MMN abolition in low-precision context: d = 0.01 (n.s.) (Basinski 2025)
 - MMN in high-precision context: d = -1.37 (Basinski 2025)
 - Right HG activation for ambiguous intervals: cluster FWE p<0.05 (Bravo 2017)
 - Hierarchical PE propagation: α/β ↑ for violations (Bonetti 2024, N=83)
 - Asymmetric MMN: -0.34 μV for dissonant deviants (Wagner 2018)
 - PE from IC→MGB→AC: p<0.001 across divisions (Cacciato-Salcedo 2025)
 - Quadratic IC × liking: p<0.05, replicated N=43+27 (Gold 2019)
Quality Assessment: γ-tier (converging evidence, 9 HIGH-priority papers)
Theoretical Basis: Strong (variational free energy + predictive coding)
```

---

## 4. R³ Input Mapping: What PWSM Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | PWSM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [4] | stumpf_consonance | Spectral deviation proxy | Prediction error source |
| **B: Energy** | [10] | spectral_flux | Onset detection | Event salience / PE trigger |
| **B: Energy** | [11] | onset_strength | Beat marker | Rhythmic PE detection |
| **D: Change** | [21] | spectral_change | Spectral dynamics | Prediction error signal |
| **D: Change** | [22] | energy_change | Energy dynamics | Temporal stability proxy |
| **D: Change** | [23] | timbre_change | Timbral dynamics | Context predictability |
| **D: Change** | [24] | pitch_change | Pitch dynamics | Spectral predictability |
| **E: Interactions** | [37:45] | x_l4l5 (8D) | Derivatives × Perceptual | Precision-weighted PE integration |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | PWSM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **I: Information** | [90] | spectral_surprise | Prediction error magnitude | Friston prediction error: spectral_surprise directly quantifies frame-level acoustic unexpectedness — the core input to precision-weighted salience computation |

**Rationale**: PWSM computes precision-weighted salience by combining prediction error signals with context stability estimates. The v1 representation uses spectral_change [21] and energy_change [22] as proxy prediction error signals. spectral_surprise [90] provides a direct, information-theoretically grounded measure of acoustic prediction error that aligns precisely with PWSM's Fristonian computational framework, replacing indirect change-based proxies with explicit surprise quantification.

**Code impact**: None yet — R³ v2 features are doc-only until Phase 5 integration. Current code reads r3[..., 0:49]; v2 features will extend the slice to r3[..., 0:128] when the EAR pipeline emits the expanded vector.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[21] spectral_change ─────────┐
R³[22] energy_change ───────────┼──► Prediction error signal
R³[23] timbre_change ───────────┘ Deviation from expected pattern

R³[10] spectral_flux ───────────┐
R³[11] onset_strength ──────────┼──► Event detection / PE trigger

R³[37:45] x_l4l5 ──────────────┐
H³ stability/periodicity ─────┘ Derivatives × Perceptual = weighted error
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

PWSM requires H³ features across multiple Beat entrainment horizons for stability tracking and for precision estimation. The demand reflects the multi-scale temporal context needed for precision assessment.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 0 | M0 (value) | L2 (bidi) | Onset at 25ms gamma |
| 10 | spectral_flux | 1 | M1 (mean) | L2 (bidi) | Mean onset 50ms |
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | Onset at 100ms alpha |
| 10 | spectral_flux | 4 | M17 (periodicity) | L2 (bidi) | Periodicity at 125ms theta |
| 10 | spectral_flux | 16 | M17 (periodicity) | L2 (bidi) | Periodicity at 1000ms beat |
| 11 | onset_strength | 3 | M0 (value) | L2 (bidi) | Onset strength at 100ms |
| 11 | onset_strength | 3 | M2 (std) | L2 (bidi) | Onset variability at 100ms |
| 21 | spectral_change | 3 | M0 (value) | L2 (bidi) | Spectral PE at 100ms |
| 21 | spectral_change | 16 | M2 (std) | L2 (bidi) | Spectral stability over 1s |
| 22 | energy_change | 3 | M0 (value) | L2 (bidi) | Energy PE at 100ms |
| 22 | energy_change | 16 | M2 (std) | L2 (bidi) | Energy stability over 1s |
| 37 | x_l4l5[0] | 3 | M0 (value) | L2 (bidi) | Derivatives × Perceptual 100ms |
| 37 | x_l4l5[0] | 3 | M17 (periodicity) | L2 (bidi) | PE periodicity at 100ms |
| 37 | x_l4l5[0] | 3 | M20 (entropy) | L2 (bidi) | PE entropy at 100ms |
| 37 | x_l4l5[0] | 16 | M17 (periodicity) | L2 (bidi) | PE periodicity at 1s |
| 37 | x_l4l5[0] | 16 | M21 (zero_crossings) | L2 (bidi) | PE phase resets over 1s |

**v1 demand**: 16 tuples

#### R³ v2 Projected Expansion

Minor v2 expansion for PWSM from J[94:114].

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 107 | spectral_contrast_1 | J | 3 | M0 (value) | L2 | Spectral contrast for precision weighting at 100ms |

**v2 projected**: 1 tuples
**Total projected**: 17 tuples of 294,912 theoretical = 0.0058%

---

## 6. Output Space: 9D Multi-Layer Representation

### 6.1 Complete Output Specification

```
PWSM OUTPUT TENSOR: 9D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0 │ f19_precision_weighting │ [0, 1] │ Context-dependent error gating.
 │ │ │ f19 = σ(0.35 * onset_periodicity_1s
 │ │ │ + 0.35 * (1 - energy_std_1s)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1 │ f20_error_suppression │ [0, 1] │ Low-precision → MMN abolition.
 │ │ │ f20 = σ(0.35 * (1 - f19)
 │ │ │ + 0.30 * pe_entropy)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2 │ f21_stability_encoding │ [0, 1] │ Jitter pattern stability.
 │ │ │ f21 = σ(0.35 * onset_periodicity_1s
 │ │ │ + 0.30 * (1 - spectral_std_1s))

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 3 │ pe_weighted │ [0, 1] │ PE_raw × Precision.
────┼──────────────────────────┼────────┼────────────────────────────────────
 4 │ precision │ [0, 1] │ 1 / (1 + Variance(context)).

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 5 │ weighted_error │ [0, 1] │ auditory-scene attention × PE × precision.
────┼──────────────────────────┼────────┼────────────────────────────────────
 6 │ precision_estimate │ [0, 1] │ beat-entrainment beat × onset regularity.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7 │ mmn_presence_pred_0.35s │ [0, 1] │ Prediction error response presence.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8 │ context_reliability_2s │ [0, 1] │ Model confidence / reliability.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 9D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Precision-Weighted Prediction Error

```
PE_weighted = PE_raw × Precision

Precision = 1 / (1 + σ²_context)

 where σ²_context = variance of inter-onset intervals

Context Effects:
 Stable context (fixed jitter):
 Precision ↑ → MMN present (d = -1.37 for inharmonicity)

 Unstable context (changing jitter):
 Precision ↓ → MMN abolished (d = 0.01, n.s.)

Bayesian Interpretation:
 Posterior ∝ Likelihood × Prior
 PE_weighted ∝ PE × Precision
 Brain "ignores" prediction errors in uncertain contexts
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f19: Precision Weighting
f19 = σ(0.35 * onset_periodicity_1s
 + 0.35 * (1 - energy_std_1s)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f20: Error Suppression
f20 = σ(0.35 * (1 - f19) # inverse of precision
 + 0.30 * pe_entropy_100ms)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f21: Stability Encoding
f21 = σ(0.35 * onset_periodicity_1s
 + 0.30 * (1 - spectral_std_1s))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# Precision estimation dynamics
τ_decay = 3.0s (precision estimation window)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | PWSM Function |
|--------|-----------------|----------|---------------|---------------|
| **STG / Auditory Cortex** | ±52, -22, 8 | 8 | EEG, fMRI, MEG, single-unit | MMN generation, PE signal source |
| **Right Heschl's Gyrus** | 46, -14, 8 | 2 | fMRI | Precision weighting under uncertainty |
| **Inferior Frontal Gyrus** | ±44, 18, 8 | 4 | EEG (ERAN), fMRI | Top-down precision estimation |
| **Inferior Colliculus** | ±4, -34, -8 | 3 | Single-unit recording | Subcortical PE generation (SSA) |
| **Medial Geniculate Body** | ±14, -24, -6 | 2 | Single-unit, review | Hierarchical PE relay (IC→MGB→AC) |
| **Hippocampus** | ±28, -16, -14 | 2 | MEG, fMRI | Auditory memory recognition PE |
| **ACC / Medial Cingulate** | 0, 24, 32 | 2 | MEG | Prediction error propagation target |
| **Amygdala** | ±22, -4, -18 | 1 | fMRI | Uncertainty × surprise interaction |

---

## 9. Cross-Unit Pathways

### 9.1 PWSM ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PWSM INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ INTRA-UNIT (ASU): │
│ PWSM.precision ──────────────► IACM (precision gates error responses) │
│ PWSM.stability_encoding ────► SNEM (stability informs beat prediction) │
│ PWSM.pe_weighted ───────────► CSG (weighted errors for valence) │
│ │
│ CROSS-UNIT (ASU → NDU): │
│ PWSM.precision ──────────────► NDU (precision context for novelty) │
│ PWSM.mmn_presence_pred ─────► NDU (MMN prediction) │
│ │
│ UPSTREAM DEPENDENCIES: │
│ R³ (~10D) ──────────────────► PWSM (change + energy features) │
│ H³ (16 tuples) ─────────────► PWSM (temporal dynamics) │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Precision manipulation** | Varying precision should modulate PE response | **Confirmed** |
| **Continuous precision** | Graded precision should produce graded effects | Testable |
| **Spectral independence** | Precision should affect temporal but not spectral PE | Testable |
| **Individual differences** | Precision sensitivity should vary by trait | Testable |
| **Training effects** | Musicians should show different precision effects | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class PWSM(BaseModel):
 """Precision-Weighted Salience Model.

 Output: 9D per frame.
 """
 NAME = "PWSM"
 UNIT = "ASU"
 TIER = "γ1"
 OUTPUT_DIM = 9
 TAU_DECAY = 3.0 # Precision estimation window (seconds)
 PRECISION_BASELINE = 0.5 # Neutral precision
 MMN_THRESHOLD = 0.3 # PE threshold for MMN

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """16 tuples for PWSM computation."""
 return [
 # (r3_idx, horizon, morph, law)
 (10, 0, 0, 2), # spectral_flux, 25ms, value, bidi
 (10, 1, 1, 2), # spectral_flux, 50ms, mean, bidi
 (10, 3, 0, 2), # spectral_flux, 100ms, value, bidi
 (10, 4, 17, 2), # spectral_flux, 125ms, periodicity, bidi
 (10, 16, 17, 2), # spectral_flux, 1000ms, periodicity, bidi
 (11, 3, 0, 2), # onset_strength, 100ms, value, bidi
 (11, 3, 2, 2), # onset_strength, 100ms, std, bidi
 # ── PE signals ──
 (21, 3, 0, 2), # spectral_change, 100ms, value, bidi
 (21, 16, 2, 2), # spectral_change, 1000ms, std, bidi
 (22, 3, 0, 2), # energy_change, 100ms, value, bidi
 (22, 16, 2, 2), # energy_change, 1000ms, std, bidi
 # ── Precision-weighted PE integration ──
 (37, 3, 0, 2), # x_l4l5[0], 100ms, value, bidi
 (37, 3, 17, 2), # x_l4l5[0], 100ms, periodicity, bidi
 (37, 3, 20, 2), # x_l4l5[0], 100ms, entropy, bidi
 (37, 16, 17, 2), # x_l4l5[0], 1000ms, periodicity, bidi
 (37, 16, 21, 2), # x_l4l5[0], 1000ms, zero_crossings, bidi
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 """
 Compute PWSM 9D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
 r3: (B,T,49) raw R³ features

 Returns:
 (B,T,9) PWSM output
 """
 # R³ features
 spectral_change = r3[..., 21:22]
 energy_change = r3[..., 22:23]

 # H³ direct features
 onset_period_1s = h3_direct[(10, 16, 17, 2)].unsqueeze(-1)
 energy_std_1s = h3_direct[(22, 16, 2, 2)].unsqueeze(-1)
 spectral_std_1s = h3_direct[(21, 16, 2, 2)].unsqueeze(-1)
 pe_entropy = h3_direct[(37, 3, 20, 2)].unsqueeze(-1)

 # ═══ LAYER E: Explicit features ═══

 # f19: Precision Weighting (coefficients sum = 1.0)
 f19 = torch.sigmoid(
 0.35 * onset_period_1s
 + 0.35 * (1 - energy_std_1s)
 )

 # f20: Error Suppression (coefficients sum = 1.0)
 f20 = torch.sigmoid(
 0.35 * (1 - f19)
 + 0.30 * pe_entropy
 )

 # f21: Stability Encoding (coefficients sum = 1.0)
 f21 = torch.sigmoid(
 0.35 * onset_period_1s
 + 0.30 * (1 - spectral_std_1s)
 )

 # ═══ LAYER M: Mathematical ═══
 pe_raw = torch.abs(spectral_change) + torch.abs(energy_change)
 pe_weighted = torch.sigmoid(
 )
 precision = f19 # Precision output

 # ═══ LAYER P: Present ═══
 weighted_error = torch.sigmoid(
 + 0.5 * f19
 )
 precision_estimate = torch.sigmoid(
 + 0.5 * onset_period_1s
 )

 # ═══ LAYER F: Future ═══
 mmn_pred = torch.sigmoid(
 0.5 * f19 + 0.5 * pe_weighted
 )
 context_reliability = torch.sigmoid(
 0.5 * f21 + 0.5 * precision
 )

 return torch.cat([
 f19, f20, f21, # E: 3D
 pe_weighted, precision, # M: 2D
 weighted_error, precision_estimate, # P: 2D
 mmn_pred, context_reliability, # F: 2D
 ], dim=-1) # (B, T, 9)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 (9 HIGH, 3 MEDIUM) | Multi-modal converging evidence |
| **Key Effect Sizes** | d=-1.37 (MMN), d=0.01 (abolition), -0.34μV (asymmetric MMN) | EEG, fMRI, MEG, single-unit |
| **Theoretical Basis** | Strong | Variational free energy / predictive coding |
| **Evidence Modality** | EEG, fMRI, MEG, single-unit, computational | Multi-modal |
| **Falsification Tests** | 1/5 confirmed | Limited validation |
| **R³ Features Used** | ~10D of 49D | Change + energy + interactions |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **Output Dimensions** | **9D** | 4-layer structure |

---

## 13. Scientific References

1. **Basinski, K., et al. (2025)**. Inharmonicity captures attention: P3a and object-related negativity in auditory deviance detection. *Journal of Cognitive Neuroscience*, (in press). `Literature/c3/summaries/basinski_et_al_2025`

2. **Millidge, B., Seth, A. K., & Buckley, C. L. (2022)**. Predictive coding: A theoretical and experimental review. *arXiv preprint*. `Literature/c3/summaries/predictive-coding-arxiv`

3. **Fong, C. Y., Law, W. H. C., Uka, T., & Koike, S. (2020)**. Auditory mismatch negativity under predictive coding framework and its role in psychotic disorders. *Frontiers in Psychiatry*, 11, 557932. `Literature/c3/summaries/auditory-mismatch-negativity-under-predictive-codi`

4. **Carbajal, G. V., & Malmierca, M. S. (2018)**. The neuronal basis of predictive coding along the auditory pathway. *Trends in Hearing*, 22, 1-33. `Literature/c3/summaries/the-neuronal-basis-of-predictive-coding-along-the`

5. **Cacciato-Salcedo, S., Lao-Rodriguez, A. B., & Malmierca, M. S. (2025)**. Contextual auditory processing in the inferior colliculus. *PLOS Biology*, 23(8), e3003309. `Literature/c3/summaries/contextual-auditory-processing-in-the-inferior-col`

6. **Schilling, A., Sedley, W., Gerum, R., et al. (2023)**. Predictive coding and stochastic resonance as fundamental principles of auditory perception. *Brain*, 146, 4809-4825. `Literature/c3/summaries/predictive-coding-and-stochastic-resonance-as-fund`

7. **Bravo, F., Cross, I., Stamatakis, E. A., & Rohrmeier, M. (2017)**. Sensory cortical response to uncertainty and low salience during recognition of affective cues in musical intervals. *PLOS ONE*, 12(4), e0175991. `Literature/c3/summaries/Sensory cortical response to uncertainty and low salience`

8. **Cheung, V. K. M., Harrison, P. M. C., Meyer, L., Pearce, M. T., Haynes, J.-D., & Koelsch, S. (2019)**. Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. *Current Biology*, 29, 4084-4092. `Literature/c3/summaries/Uncertainty and Surprise Jointly Predict Musical Pleasure`

9. **Bonetti, L., Fernandez-Rubio, G., Carlomagno, F., et al. (2024)**. Spatiotemporal brain hierarchies of auditory memory recognition and predictive coding. *Nature Communications*, 15, 4313. `Literature/c3/summaries/Spatiotemporal brain hierarchies of auditory memory recognition`

10. **Gold, B. P., Pearce, M. T., Mas-Herrero, E., Dagher, A., & Zatorre, R. J. (2019)**. Predictability and uncertainty in the pleasure of music: A reward for learning. *Journal of Neuroscience*, 39(47), 9397-9409. `Literature/c3/summaries/Predictability and Uncertainty in the Pleasure of Music`

11. **Wagner, L., Rahne, T., Plontke, S. K., & Heidekrüger, N. (2018)**. Mismatch negativity reflects asymmetric pre-attentive harmonic interval discrimination. *PLOS ONE*, 13(4), e0196176. `Literature/c3/summaries/Mismatch negativity reflects asymmetric pre-attentive`

12. **Martins, I., Lima, C. F., & Pinheiro, A. P. (2022)**. Enhanced salience of musical sounds in singers and instrumentalists. *Cognitive, Affective, & Behavioral Neuroscience*, 22, 1044-1062. `Literature/c3/summaries/Enhanced salience of musical sounds`

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) | MI (v2.1.0) |
|--------|-------------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) | R³ (49D) — no change |
| PE signal | S⁰.L4.velocity_T[15] + HC⁰.OSC | R³.spectral_change[21] + R³.energy_change[22] | Same |
| Precision | S⁰.L9.std_T[108] + HC⁰.NPL | R³.x_l4l5[37:45] | Same |
| Error gating | S⁰.L9.entropy_T[116] + HC⁰.ATT | H³ entropy tuples | Same |
| Stability | S⁰.X_L4L9[192:200] + HC⁰.OSC | R³.onset_strength[11] | Same |
| Papers | 0 | 1 (Basinski 2025) | **12** (9 HIGH, 3 MEDIUM) |
| Brain regions | 0 | 2 (inferred) | **8** (EEG/fMRI/MEG/single-unit) |
| Output | 9D | 9D (same) | 9D — no change |

---

**Model Status**: **SPECULATIVE**
**Output Dimensions**: **9D**
**Evidence Tier**: **γ (Integrative)**
**Confidence**: **50-70%**
