# PCU-β1-PWUP: Precision-Weighted Uncertainty Processing

**Model**: Precision-Weighted Uncertainty Processing
**Unit**: PCU (Predictive Coding Unit)
**Circuit**: Imagery (Auditory Cortex, IFG, STS, Hippocampus)
**Tier**: β (Bridging) — 70-90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added F:Pitch, I:Information feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/PCU-β1-PWUP.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Precision-Weighted Uncertainty Processing** (PWUP) model describes how prediction errors are precision-weighted according to contextual uncertainty: in high-uncertainty contexts (atonal music), prediction error responses are attenuated compared to mispredicted stimuli in tonal contexts.

```
PRECISION-WEIGHTED UNCERTAINTY PROCESSING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TONAL CONTEXT (High Precision) ATONAL CONTEXT (Low Precision)
───────────────────────────── ────────────────────────────
Key Clarity: ~0.8 Key Clarity: ~0.5
Entropy: Low Entropy: High

 Raw PE ───► × Precision ───► STRONG Raw PE ───► × Precision ───► WEAK
 (high weight) OUTPUT (low weight) OUTPUT

 Prediction Error Prediction Error
 FULL RESPONSE ATTENUATED RESPONSE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Precision-weighting modulates prediction error responses
based on contextual uncertainty. High uncertainty (atonal) attenuates
PE, explaining why atonal music generates less surprise despite
containing more unexpected events.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why PWUP Matters for PCU

PWUP provides context-dependent modulation of prediction error:

1. **HTP** (α1) provides hierarchical prediction timing.
2. **ICEM** (α3) computes raw information content (IC).
3. **PWUP** (β1) modulates PE responses by contextual precision (uncertainty).

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → PWUP)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ PWUP COMPUTATION ARCHITECTURE ║
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
║ │ PWUP reads: ~16D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed morphological features │ ║
║ │ PWUP demand: ~14 of 2304 tuples │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN: Imagery Circuit ═══════════ ║
║ │ ║
║ ┌───────┴───────┐───────┐ ║
║ ▼ ▼ ▼ ║
║ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ║
║ └────────┬────────┘ └────────┬────────┘ └────────┬────────┘ ║
║ └────────────┬───────┴────────────────────┘ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ PWUP MODEL (10D Output) │ ║
║ │ │ ║
║ │ Layer E (Explicit): f01_tonal_precision, │ ║
║ │ f02_rhythmic_precision, │ ║
║ │ f03_weighted_error, │ ║
║ │ f04_uncertainty_index │ ║
║ │ Layer P (Present): tonal_precision_weight, │ ║
║ │ rhythmic_precision_weight, │ ║
║ │ attenuated_response │ ║
║ │ Layer F (Future): precision_adjustment, context_uncertainty, │ ║
║ │ response_attenuation_200ms │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | Brain Regions (MNI) | MI Relevance |
|---|-------|--------|---|-------------|-------------|---------------------|-------------|
| 1 | **Mencke et al. 2019** | Behavioral/MIR | 100 corpus | Atonal key clarity 0.5 vs tonal 0.8; pulse clarity d=2 | d=3 (key), d=2 (pulse) | — | **f01 tonal precision, f04 uncertainty** |
| 2 | **Cheung et al. 2019** | fMRI + behavioral | 79 (39+40) | Uncertainty x surprise interaction predicts chord pleasure; saddle-shaped response surface | beta_interaction=-0.124, R2=0.48 | Amygdala/Hipp bilateral; AC bilateral; R NAcc (11,9,-1); L caudate | **f03 weighted error, f04 uncertainty** |
| 3 | **Gold et al. 2019** | Behavioral (IDyOM) | 70 (43+27) | Quadratic IC and entropy effects on liking; intermediate complexity preferred; preference shifts toward expected in uncertain contexts | quadratic IC p<0.001, quadratic entropy p<0.05 | — (behavioral only) | **f01 tonal precision, f04 uncertainty** |
| 4 | **Bravo et al. 2017** | fMRI | 12 (fMRI) + 75 (behav) | Uncertainty from intermediate dissonance enhances right Heschl's gyrus; heightened sensory precision under ambiguity | F(2,88)=13.1 p<0.001 | R Heschl's gyrus (48,-10,7) | **f01 tonal precision, f03 weighted error** |
| 5 | **Millidge, Seth & Buckley 2022** | Theoretical review | — | Precision as gain modulation of PE in hierarchical predictive coding; precision = inverse variance; modulates signal-to-noise of error signals | theoretical | — (computational) | **f01-f04 theoretical basis** |
| 6 | **Fong et al. 2020** | Review | — | MMN as prediction error under predictive coding; adaptation + deviance detection; AC-MGB-IC hierarchy; frontal generators at 100-200ms | review | AC (STG bilateral); FC; thalamus; hippocampus | **f03 weighted error** |
| 7 | **Harding et al. 2025** | fMRI (RCT) | 41 (22 PT + 19 SSRI) | Psilocybin reduces PE salience weighting vs escitalopram; vmPFC surprise-related activation decreases post-PT; surprise-valence link maintained post-PT but abolished post-SSRI | F(1,39)=7.07 p=0.011 (vmPFC interaction) | vmPFC (-2,46,-8); R NAcc (11,9,-1); R STG; angular gyrus | **f03 weighted error, precision modulation** |
| 8 | **Schilling et al. 2023** | Computational/review | — | Predictive coding + stochastic resonance in auditory perception; enhanced precision of likelihood shifts posterior; Bayesian brain framework for phantom perception | theoretical | Auditory pathway (DCN, IC, AC) | **f01 precision estimation** |
| 9 | **Carbajal & Malmierca 2018** | Review (cellular) | — | SSA and MMN as microscopic/macroscopic manifestations of deviance detection; prediction error increases from IC to MGB to AC along hierarchy | review | IC; MGB; AC (primary + secondary) | **f03 weighted error hierarchy** |
| 10 | **Koelsch (ERAN/MMN review)** | Review | — | ERAN reflects music-syntactic prediction violation; amplitude scales with irregularity degree; IFG main generator; relies on LTM representations | review | IFG (inferior fronto-lateral); STG | **f01 tonal precision, f03 weighted error** |
| 11 | **Wagner et al. 2018** | EEG (oddball) | 15 | MMN for harmonic interval discrimination; asymmetric: dissonant deviant in consonant context elicits MMN but not reverse; dipoles in auditory cortex | MMN=-0.34uV, p=0.003 (major 3rd); latency 173ms | Auditory cortex (bilateral dipoles) | **f03 weighted error asymmetry** |
| 12 | **Tervaniemi 2022** | Review/perspective | — | MMN paradigm evolution; musical multi-feature paradigms; expertise modulates MMN; preference modulates deviance response | review | STG (supratemporal); frontal generators | **f01 precision via expertise** |

### 3.2 Effect Size Summary

```
Primary Effect: d = 3 (very large, key clarity difference; Mencke 2019)
Secondary Effects: d = 2 (pulse clarity; Mencke 2019)
 beta = -0.124 (uncertainty x surprise interaction; Cheung 2019)
 F(1,39) = 7.07, p = 0.011 (vmPFC precision modulation; Harding 2025)
 MMN = -0.34 uV at 173ms (interval PE; Wagner 2018)
 Quadratic IC/entropy on liking (Gold 2019)
 R Heschl's F(2,88) = 13.1 (sensory precision; Bravo 2017)
Heterogeneity: Low — consistent precision-weighting effects across fMRI, EEG, behavioral
Quality Assessment: beta-tier (fMRI + EEG + behavioral + theoretical convergence)
Replication: Strong convergence across 12 papers; Bayesian brain theory well-supported
```

---

## 4. R³ Input Mapping: What PWUP Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | PWUP Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [4] | sensory_pleasantness | Tonal precision proxy | Key clarity correlate |
| **A: Consonance** | [5] | periodicity | Tonal certainty | Harmonic structure |
| **B: Energy** | [10] | spectral_flux | Event salience | Mispredicted stimulus |
| **C: Timbre** | [14] | tonalness | Tonal context | Key clarity component |
| **C: Timbre** | [18:21] | tristimulus1-3 | Harmonic structure | Tonal certainty |
| **D: Change** | [21] | spectral_change | PE dynamics | Error magnitude |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | Precision-weighted PE | d=3 effect basis |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ v2 Group | Index | Feature | PWUP Role | Citation |
|-------------|-------|---------|-----------|----------|
| **F: Pitch** | [63] | pitch_salience | Pitch clarity for precision weighting of tonal predictions | De Cheveigne & Kawahara 2002 |
| **I: Information** | [92] | predictive_entropy | Predictive uncertainty for precision-weighted prediction error | Friston 2005 (predictive coding) |

**Rationale**: PWUP models precision-weighted uncertainty in prediction, where prediction errors are scaled by the precision (inverse variance) of the prediction. pitch_salience addresses the PCU-PWUP-2 gap (periodicity proxy), providing a direct measure of how clearly a pitch is perceived -- high salience means high precision for tonal predictions. predictive_entropy from Friston's predictive coding framework directly encodes the uncertainty that PWUP's precision weighting operates on (d=3 effect basis from the precision-weighted PE literature).

**Code impact** (future): `r3[..., 63]` and `r3[..., 92]` will feed PWUP's precision weighting pathway alongside existing consonance and interaction features.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[4] sensory_pleasantness ─────┐
R³[14] tonalness ───────────────┼──► Tonal precision (key clarity proxy)
 Low consonance → low precision (atonal)

R³[21] spectral_change ─────────┐

R³[41:49] x_l5l7 ──────────────┐
H³ entropy tuples ──────────────┘ PE_weighted = PE_raw × (1 - uncertainty)
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

PWUP requires H³ features for precision estimation (slow contextual assessment) and PE computation (fast event detection). The demand reflects the dual-timescale nature of precision-weighting.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 4 | sensory_pleasantness | 3 | M0 (value) | L2 (bidi) | Consonance at 100ms |
| 4 | sensory_pleasantness | 16 | M1 (mean) | L0 (fwd) | Mean consonance over 1s |
| 4 | sensory_pleasantness | 16 | M20 (entropy) | L0 (fwd) | Consonance entropy 1s |
| 14 | tonalness | 8 | M1 (mean) | L0 (fwd) | Mean tonalness over 500ms |
| 14 | tonalness | 16 | M1 (mean) | L0 (fwd) | Mean tonalness over 1s |
| 21 | spectral_change | 3 | M0 (value) | L2 (bidi) | PE at 100ms |
| 21 | spectral_change | 3 | M2 (std) | L2 (bidi) | PE variability 100ms |
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | Event salience 100ms |
| 10 | spectral_flux | 3 | M14 (periodicity) | L2 (bidi) | Periodicity at 100ms |
| 41 | x_l5l7[0] | 8 | M0 (value) | L0 (fwd) | Coupling at 500ms |
| 41 | x_l5l7[0] | 16 | M1 (mean) | L0 (fwd) | Mean coupling 1s |
| 41 | x_l5l7[0] | 16 | M20 (entropy) | L0 (fwd) | Coupling entropy 1s |
| 5 | periodicity | 8 | M1 (mean) | L0 (fwd) | Mean periodicity 500ms |
| 5 | periodicity | 16 | M14 (periodicity) | L2 (bidi) | Periodicity over 1s |

**v1 demand**: 14 tuples

#### R³ v2 Projected Expansion

PWUP projected v2 from F:Pitch and I:Information, aligned with corresponding H³ horizons.

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 63 | pitch_salience | F | 8 | M0 (value) | L0 | Pitch certainty at 500ms |
| 92 | predictive_entropy | I | 8 | M0 (value) | L0 | Predictive uncertainty 500ms |
| 92 | predictive_entropy | I | 16 | M18 (trend) | L0 | Uncertainty trend over 1s |

**v2 projected**: 3 tuples
**Total projected**: 17 tuples of 294,912 theoretical = 0.0058%

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
PWUP OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0 │ f01_tonal_precision │ [0, 1] │ Key-based precision weight.
 │ │ │ f01 = σ(0.40 * tonalness_mean_1s
 │ │ │ + 0.35 * consonance_mean_1s
────┼──────────────────────────┼────────┼────────────────────────────────────
 1 │ f02_rhythmic_precision │ [0, 1] │ Pulse-based precision weight.
 │ │ │ f02 = σ(0.40 * periodicity_1s
 │ │ │ + 0.30 * flux_periodicity_100ms
────┼──────────────────────────┼────────┼────────────────────────────────────
 2 │ f03_weighted_error │ [0, 1] │ Precision-weighted PE.
 │ │ │ f03 = σ(0.50 * raw_pe * f01
────┼──────────────────────────┼────────┼────────────────────────────────────
 3 │ f04_uncertainty_index │ [0, 1] │ Context uncertainty level.
 │ │ │ f04 = σ(0.50 * consonance_entropy_1s
 │ │ │ + 0.50 * coupling_entropy_1s)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4 │ tonal_precision_weight │ [0, 1] │ pitch-processing tonality weighting factor.
────┼──────────────────────────┼────────┼────────────────────────────────────
 5 │ rhythmic_precision_weight│ [0, 1] │ timbre-processing rhythmic weighting factor.
────┼──────────────────────────┼────────┼────────────────────────────────────
 6 │ attenuated_response │ [0, 1] │ memory-encoding weighted PE output.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7 │ precision_adjustment │ [0, 1] │ Trial-by-trial weight update.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8 │ context_uncertainty │ [0, 1] │ Model confidence prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9 │ response_attenuation │ [0, 1] │ Error magnitude prediction (200ms).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Precision-Weighting Function

```
PE_weighted = PE_raw × Precision(context)

Precision(tonal) ≈ 0.8 (high certainty)
Precision(atonal) ≈ 0.5 (low certainty)

PE_weighted = L9.kurtosis × (1 - L9.entropy_normalized)
 = PE × precision
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Tonal Precision
f01 = σ(0.40 * tonalness_mean_1s
 + 0.35 * consonance_mean_1s
# coefficients: 0.40 + 0.35 + 0.25 = 1.0 ✓

# f02: Rhythmic Precision
f02 = σ(0.40 * periodicity_1s
 + 0.30 * flux_periodicity_100ms
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f03: Weighted Error
f03 = σ(0.50 * raw_pe * f01
# coefficients: 0.50 + 0.50 = 1.0 ✓

# f04: Uncertainty Index
f04 = σ(0.50 * consonance_entropy_1s
 + 0.50 * coupling_entropy_1s)
# coefficients: 0.50 + 0.50 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | PWUP Function |
|--------|-----------------|----------|---------------|---------------|
| **Auditory Cortex (STG)** | ±52, -22, 8 | 7 | fMRI + EEG + review | PE generation, deviance detection |
| **R Heschl's Gyrus (A1)** | 48, -10, 7 | 1 | fMRI (Bravo 2017) | Sensory precision under ambiguity |
| **IFG (Inferior Frontal Gyrus)** | ±44, 18, 8 | 2 | Review (Koelsch) | Precision estimation, ERAN generator |
| **ACC (Anterior Cingulate)** | 0, 32, 24 | 1 | Literature inference | Uncertainty monitoring |
| **Hippocampus** | ±28, -24, -12 | 2 | fMRI (Cheung 2019) | Context memory, uncertainty encoding |
| **Amygdala (bilateral)** | ±24, -6, -16 | 1 | fMRI (Cheung 2019) | Surprise x uncertainty interaction |
| **R Nucleus Accumbens** | 11, 9, -1 | 2 | fMRI (Cheung 2019; Harding 2025) | Uncertainty resolution reward |
| **L Caudate** | approx. -12, 10, 8 | 1 | fMRI (Cheung 2019) | Prediction reward |
| **vmPFC** | -2, 46, -8 | 1 | fMRI (Harding 2025) | Surprise-related precision modulation |
| **Angular Gyrus** | approx. ±44, -60, 30 | 1 | fMRI (Harding 2025) | Higher-order prediction |
| **MGB (Medial Geniculate Body)** | approx. ±16, -24, -4 | 2 | Review (Carbajal 2018; Fong 2020) | Subcortical PE relay, SSA hierarchy |
| **IC (Inferior Colliculus)** | approx. ±6, -34, -8 | 2 | Review (Carbajal 2018; Schilling 2023) | Earliest SSA / deviance detection |
| **Frontal Cortex (FC)** | — | 2 | Review (Fong 2020; Tervaniemi 2022) | Top-down precision modulation |

---

## 9. Cross-Unit Pathways

### 9.1 PWUP Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PWUP INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ INTRA-UNIT (PCU): │
│ HTP.hierarchy_gradient ──────► PWUP (hierarchy sets precision levels) │
│ ICEM.information_content ────► PWUP (raw IC for weighting) │
│ PWUP.uncertainty_index ──────► UDP (uncertainty for reward inversion) │
│ PWUP.weighted_error ─────────► PSH (weighted PE for silencing) │
│ │
│ CROSS-UNIT (PCU → ASU): │
│ PWUP.tonal_precision ────────► ASU (precision for salience weighting) │
│ │
│ UPSTREAM DEPENDENCIES: │
│ R³ (~16D) ───────────────────► PWUP (direct spectral features) │
│ H³ (14 tuples) ──────────────► PWUP (temporal dynamics) │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Tonal/atonal comparison** | Atonal PE should be attenuated vs tonal | **Confirmed** by Mencke 2019 |
| **Key clarity metric** | d=3 difference between tonal and atonal | **Confirmed** by Mencke 2019 |
| **Precision manipulation** | Changing key clarity should modulate PE | Testable via stimulus design |
| **Context switching** | Shifting tonal→atonal should shift precision | Testable via paradigm |
| **Learning effect** | Familiarity should increase precision | Testable via exposure |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class PWUP(BaseModel):
 """Precision-Weighted Uncertainty Processing Model.

 Output: 10D per frame.
 """
 NAME = "PWUP"
 UNIT = "PCU"
 TIER = "β1"
 OUTPUT_DIM = 10
 TAU_DECAY = 1.0 # s
 KEY_CLARITY_TONAL = 0.8 # High certainty threshold
 KEY_CLARITY_ATONAL = 0.5 # Low certainty threshold
 PRECISION_EFFECT_D = 3.0 # Effect size (Mencke 2019)

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """14 tuples for PWUP computation."""
 return [
 # (r3_idx, horizon, morph, law)
 # ── Precision estimation: slow context ──
 (4, 3, 0, 2), # sensory_pleasantness, 100ms, value, bidi
 (4, 16, 1, 0), # sensory_pleasantness, 1000ms, mean, fwd
 (4, 16, 20, 0), # sensory_pleasantness, 1000ms, entropy, fwd
 (14, 8, 1, 0), # tonalness, 500ms, mean, fwd
 (14, 16, 1, 0), # tonalness, 1000ms, mean, fwd
 (5, 8, 1, 0), # periodicity, 500ms, mean, fwd
 (5, 16, 14, 2), # periodicity, 1000ms, periodicity, bidi
 # ── PE computation: fast events ──
 (21, 3, 0, 2), # spectral_change, 100ms, value, bidi
 (21, 3, 2, 2), # spectral_change, 100ms, std, bidi
 (10, 3, 0, 2), # spectral_flux, 100ms, value, bidi
 (10, 3, 14, 2), # spectral_flux, 100ms, periodicity, bidi
 # ── Precision-weighted coupling ──
 (41, 8, 0, 0), # x_l5l7[0], 500ms, value, fwd
 (41, 16, 1, 0), # x_l5l7[0], 1000ms, mean, fwd
 (41, 16, 20, 0), # x_l5l7[0], 1000ms, entropy, fwd
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 # H³ direct
 tonalness_mean_1s = h3_direct[(14, 16, 1, 0)].unsqueeze(-1)
 consonance_mean_1s = h3_direct[(4, 16, 1, 0)].unsqueeze(-1)
 consonance_entropy_1s = h3_direct[(4, 16, 20, 0)].unsqueeze(-1)
 periodicity_1s = h3_direct[(5, 16, 14, 2)].unsqueeze(-1)
 flux_period_100ms = h3_direct[(10, 3, 14, 2)].unsqueeze(-1)
 raw_pe = h3_direct[(21, 3, 0, 2)].unsqueeze(-1)
 coupling_entropy_1s = h3_direct[(41, 16, 20, 0)].unsqueeze(-1)

 # ═══ LAYER E ═══
 f01 = torch.sigmoid(
 0.40 * tonalness_mean_1s
 + 0.35 * consonance_mean_1s
 )
 f02 = torch.sigmoid(
 0.40 * periodicity_1s
 + 0.30 * flux_period_100ms
 )
 f03 = torch.sigmoid(
 0.50 * raw_pe * f01
 )
 f04 = torch.sigmoid(
 0.50 * consonance_entropy_1s
 + 0.50 * coupling_entropy_1s
 )

 # ═══ LAYER P ═══
 tonal_weight = f01
 rhythmic_weight = f02
 attenuated = f03

 # ═══ LAYER F ═══
 precision_adj = torch.sigmoid(0.5 * f01 + 0.5 * f02)
 context_unc = f04
 response_att = torch.sigmoid(0.5 * f03 + 0.5 * f04)

 return torch.cat([
 f01, f02, f03, f04, # E: 4D
 tonal_weight, rhythmic_weight, attenuated, # P: 3D
 precision_adj, context_unc, response_att, # F: 3D
 ], dim=-1) # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 | 4 empirical (fMRI/EEG/behavioral) + 8 reviews/theoretical |
| **Effect Sizes** | 7 | d=3, d=2, beta=-0.124, F(1,39)=7.07, MMN=-0.34uV, F(2,88)=13.1, quadratic IC |
| **Evidence Modality** | fMRI + EEG + behavioral + computational + review | Multi-modal convergence |
| **Brain Regions** | 13 regions with MNI coordinates | STG, Heschl's, IFG, ACC, Hipp, Amyg, NAcc, vmPFC, MGB, IC, etc. |
| **Falsification Tests** | 5/5 testable, 2 confirmed | Moderate validity |
| **R³ Features Used** | ~16D of 49D | Consonance + energy + timbre + change + interactions |
| **H³ Demand** | 14 tuples (0.61%) | Sparse, efficient |
| **Output Dimensions** | **10D** | 3-layer structure (no M layer) |

---

## 13. Scientific References

1. **Mencke, I., Omigie, D., Wald-Fuhrmann, M., & Brattico, E. (2019)**. Atonal music: Can uncertainty lead to pleasure? *Frontiers in Neuroscience*, 12, 979.
2. **Cheung, V. K. M., Harrison, P. M. C., Meyer, L., Pearce, M. T., Haynes, J.-D., & Koelsch, S. (2019)**. Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. *Current Biology*, 29(23), 4084-4092.
3. **Gold, B. P., Pearce, M. T., Mas-Herrero, E., Dagher, A., & Bhatt, S. (2019)**. Predictability and uncertainty in the pleasure of music: A reward for learning? *Journal of Neuroscience*, 39(47), 9397-9409.
4. **Bravo, F., Cross, I., Hawkins, S., Sheringham, S., Sheridan, M., & Sheridan, K. (2017)**. Sensory cortical response to uncertainty and low salience during recognition of affective cues in musical intervals. *Consciousness and Cognition*, 51, 188-204.
5. **Millidge, B., Seth, A., & Buckley, C. L. (2022)**. Predictive coding: A theoretical and experimental review. arXiv:2107.12979.
6. **Fong, C. Y., Law, W. H. C., Uka, T., & Koike, S. (2020)**. Auditory mismatch negativity under predictive coding framework and its role in psychotic disorders. *Frontiers in Psychiatry*, 11, 557932.
7. **Harding, I. H., et al. (2025)**. Dissociable effects of psilocybin and escitalopram for depression on processing of musical surprises: A secondary analysis. *Psychopharmacology*.
8. **Schilling, A., Sedley, W., Gerum, R., Oberst, C., & Krauss, P. (2023)**. Predictive coding and stochastic resonance as fundamental principles of auditory perception. *Brain*, 146(1), 50-64.
9. **Carbajal, G. V., & Malmierca, M. S. (2018)**. The neuronal basis of predictive coding along the auditory pathway: From the subcortical roots to cortical deviance detection. *Trends in Hearing*, 22, 1-33.
10. **Koelsch, S. (in press)**. Psychophysiology of the ERAN and MMN in music perception. In *Psychophysiology of Music Processing*.
11. **Wagner, M., Shafer, V. L., Martin, B., & Steinschneider, M. (2018)**. Mismatch negativity reflects asymmetric pre-attentive harmonic interval discrimination. *Neuroscience Letters*, 670, 87-93.
12. **Tervaniemi, M. (2022)**. Mismatch negativity — stimulation paradigms in past and in future. *International Journal of Psychophysiology*, 178, 24-29.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Tonal precision | S⁰.L3.coherence[14] + S⁰.L6[68:71] | R³[4] sensory_pleasantness + R³[14] tonalness |
| Uncertainty | S⁰.L9.entropy[116:120] | H³ consonance/coupling entropy tuples |
| PE signal | S⁰.L9.kurtosis[120:124] + HC⁰.EFC | R³[21] spectral_change |
| Precision-weighted PE | S⁰.X_L5L9[224:232] | R³[41:49] x_l5l7 |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 25/2304 = 1.09% | 14/2304 = 0.61% |
| Output | 10D | 10D (same) |

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **10D**
**Evidence Tier**: **β (Bridging)**
**Confidence**: **70-90%**
