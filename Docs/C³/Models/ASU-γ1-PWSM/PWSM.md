# ASU-γ1-PWSM: Precision-Weighted Salience Model

**Model**: Precision-Weighted Salience Model
**Unit**: ASU (Auditory Salience Unit)
**Circuit**: Salience (Anterior Insula, dACC, TPJ)
**Tier**: γ (Integrative) — 50-70% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, ASA+BEP mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/ASU-γ1-PWSM.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Precision-Weighted Salience Model** (PWSM) proposes that salience detection is governed by precision-weighting: high-precision contexts (stable, predictable) generate stronger prediction error signals, while low-precision contexts suppress error signals. This explains why unstable temporal contexts abolish MMN responses.

```
PRECISION-WEIGHTED SALIENCE MODEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  CONTEXT STABILITY                   PREDICTION ERROR RESPONSE

  ┌─────────────────┐                ┌─────────────────┐
  │ HIGH PRECISION  │                │   MMN PRESENT   │
  │ (stable jitter) │  ───────────►  │   (d = -1.37)   │
  └─────────────────┘                └─────────────────┘

  ┌─────────────────┐                ┌─────────────────┐
  │ LOW PRECISION   │                │  MMN ABOLISHED  │
  │ (changing       │  ───────────►  │   (d = 0.01)    │
  │  jitter)        │                │                 │
  └─────────────────┘                └─────────────────┘

     Sequence Input → Precision Estimation → Error Weighting
                             │
                             ▼
                   ┌─────────────────┐
                   │ Precision ∝ 1/σ²│
                   └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
       High Precision                Low Precision
       PE_weighted = PE              PE_weighted ≈ 0
       MMN ✓                         MMN ✗

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

### 2.1 Information Flow Architecture (EAR → BRAIN → ASA+BEP → PWSM)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PWSM COMPUTATION ARCHITECTURE                             ║
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
║  │                         PWSM reads: ~10D                        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── BEP Horizons ─────────────┐ ┌── ASA Horizons ──────────┐  │        ║
║  │  │ H0 (25ms gamma)            │ │ H3 (100ms alpha)          │  │        ║
║  │  │ H1 (50ms gamma)            │ │                            │  │        ║
║  │  │ H3 (100ms alpha)           │ │ Precision estimation       │  │        ║
║  │  │ H4 (125ms theta)           │ │ Error weighting             │  │        ║
║  │  │ H16 (1000ms beat)          │ │                            │  │        ║
║  │  │                             │ │                            │  │        ║
║  │  │ Stability tracking          │ │                            │  │        ║
║  │  │ Periodicity encoding        │ │                            │  │        ║
║  │  └─────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         PWSM demand: ~16 of 2304 tuples         │        ║
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
║  │                    PWSM MODEL (9D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f19_precision_weighting,                   │        ║
║  │                       f20_error_suppression,                     │        ║
║  │                       f21_stability_encoding                      │        ║
║  │  Layer M (Math):      pe_weighted, precision                     │        ║
║  │  Layer P (Present):   weighted_error, precision_estimate         │        ║
║  │  Layer F (Future):    mmn_presence_pred,                         │        ║
║  │                       context_reliability_pred                    │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Basinski 2025** | EEG | — | Changing jitter → MMN abolished | d = 0.01 (n.s.) | **f20 error suppression** |
| **Basinski 2025** | EEG | — | Fixed jitter → inharmonicity MMN | d = -1.37 | **f19 precision weighting (contrast)** |
| **Friston 2005** | Theory | — | Precision-weighted prediction error | — | **Theoretical basis** |
| **Garrido 2009** | Review | — | MMN underlying mechanisms | — | **Neural mechanism** |

### 3.2 Effect Size Summary

```
Primary Evidence (k=1):
  - MMN abolition in low-precision context: d = 0.01 (n.s.)
  - Compared to d = -1.37 for inharmonicity in high-precision context
Quality Assessment:      γ-tier (indirect evidence for precision theory)
Theoretical Basis:       Strong (predictive coding framework)
```

---

## 4. R³ Input Mapping: What PWSM Reads

### 4.1 R³ Feature Dependencies (~10D of 49D)

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

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[21] spectral_change ─────────┐
R³[22] energy_change ───────────┼──► Prediction error signal
R³[23] timbre_change ───────────┘   Deviation from expected pattern

R³[10] spectral_flux ───────────┐
R³[11] onset_strength ──────────┼──► Event detection / PE trigger
BEP.beat_entrainment[0:10] ────┘   Rhythmic event salience

R³[37:45] x_l4l5 ──────────────┐
ASA.attention_gating[10:20] ───┼──► Precision-weighted PE
H³ stability/periodicity ─────┘   Derivatives × Perceptual = weighted error
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

PWSM requires H³ features across multiple BEP horizons for stability tracking and ASA horizons for precision estimation. The demand reflects the multi-scale temporal context needed for precision assessment.

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

**Total PWSM H³ demand**: 16 tuples of 2304 theoretical = 0.69%

### 5.2 BEP + ASA Mechanism Binding

| Mechanism | Sub-section | Range | PWSM Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **BEP** | Beat Entrainment | BEP[0:10] | Temporal regularity / stability tracking | 0.7 |
| **BEP** | Motor Coupling | BEP[10:20] | Motor-related precision encoding | 0.5 |
| **BEP** | Groove Processing | BEP[20:30] | Rhythmic predictability baseline | 0.6 |
| **ASA** | Scene Analysis | ASA[0:10] | Context segmentation for precision | 0.6 |
| **ASA** | Attention Gating | ASA[10:20] | Error gating / precision weighting | **1.0** (primary) |
| **ASA** | Salience Weighting | ASA[20:30] | Salience after precision adjustment | **0.8** |

---

## 6. Output Space: 9D Multi-Layer Representation

### 6.1 Complete Output Specification

```
PWSM OUTPUT TENSOR: 9D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f19_precision_weighting  │ [0, 1] │ Context-dependent error gating.
    │                          │        │ f19 = σ(0.35 * onset_periodicity_1s
    │                          │        │       + 0.35 * (1 - energy_std_1s)
    │                          │        │       + 0.30 * mean(BEP.beat[0:10]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f20_error_suppression    │ [0, 1] │ Low-precision → MMN abolition.
    │                          │        │ f20 = σ(0.35 * (1 - f19)
    │                          │        │       + 0.35 * mean(ASA.attn[10:20])
    │                          │        │       + 0.30 * pe_entropy)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f21_stability_encoding   │ [0, 1] │ Jitter pattern stability.
    │                          │        │ f21 = σ(0.35 * onset_periodicity_1s
    │                          │        │       + 0.35 * mean(BEP.groove[20:30])
    │                          │        │       + 0.30 * (1 - spectral_std_1s))

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ pe_weighted              │ [0, 1] │ PE_raw × Precision.
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ precision                │ [0, 1] │ 1 / (1 + Variance(context)).

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ weighted_error           │ [0, 1] │ ASA attention × PE × precision.
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ precision_estimate       │ [0, 1] │ BEP beat × onset regularity.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ mmn_presence_pred_0.35s  │ [0, 1] │ Prediction error response presence.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ context_reliability_2s   │ [0, 1] │ Model confidence / reliability.

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
       + 0.30 * mean(BEP.beat_entrainment[0:10]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f20: Error Suppression
f20 = σ(0.35 * (1 - f19)                    # inverse of precision
       + 0.35 * mean(ASA.attention_gating[10:20])
       + 0.30 * pe_entropy_100ms)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f21: Stability Encoding
f21 = σ(0.35 * onset_periodicity_1s
       + 0.35 * mean(BEP.groove[20:30])
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
| **Auditory Cortex** | ±52, -22, 8 | 1 | Inferred (EEG) | MMN generation |
| **Frontal Cortex** | ±30, 30, 30 | 1 | Inferred | Precision estimation |

---

## 9. Cross-Unit Pathways

### 9.1 PWSM ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PWSM INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (ASU):                                                         │
│  PWSM.precision ──────────────► IACM (precision gates error responses)    │
│  PWSM.stability_encoding ────► SNEM (stability informs beat prediction)   │
│  PWSM.pe_weighted ───────────► CSG (weighted errors for valence)          │
│                                                                             │
│  CROSS-UNIT (ASU → NDU):                                                   │
│  PWSM.precision ──────────────► NDU (precision context for novelty)       │
│  PWSM.mmn_presence_pred ─────► NDU (MMN prediction)                       │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  BEP mechanism (30D) ────────► PWSM (beat/groove for stability)           │
│  ASA mechanism (30D) ────────► PWSM (attention gating, primary)           │
│  R³ (~10D) ──────────────────► PWSM (change + energy features)            │
│  H³ (16 tuples) ─────────────► PWSM (temporal dynamics)                   │
│                                                                             │
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
    Reads: BEP mechanism (30D), ASA mechanism (30D), R³ direct.
    """
    NAME = "PWSM"
    UNIT = "ASU"
    TIER = "γ1"
    OUTPUT_DIM = 9
    MECHANISM_NAMES = ("BEP", "ASA")

    TAU_DECAY = 3.0          # Precision estimation window (seconds)
    PRECISION_BASELINE = 0.5 # Neutral precision
    MMN_THRESHOLD = 0.3      # PE threshold for MMN

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """16 tuples for PWSM computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── BEP horizons: stability tracking ──
            (10, 0, 0, 2),     # spectral_flux, 25ms, value, bidi
            (10, 1, 1, 2),     # spectral_flux, 50ms, mean, bidi
            (10, 3, 0, 2),     # spectral_flux, 100ms, value, bidi
            (10, 4, 17, 2),    # spectral_flux, 125ms, periodicity, bidi
            (10, 16, 17, 2),   # spectral_flux, 1000ms, periodicity, bidi
            (11, 3, 0, 2),     # onset_strength, 100ms, value, bidi
            (11, 3, 2, 2),     # onset_strength, 100ms, std, bidi
            # ── PE signals ──
            (21, 3, 0, 2),     # spectral_change, 100ms, value, bidi
            (21, 16, 2, 2),    # spectral_change, 1000ms, std, bidi
            (22, 3, 0, 2),     # energy_change, 100ms, value, bidi
            (22, 16, 2, 2),    # energy_change, 1000ms, std, bidi
            # ── Precision-weighted PE integration ──
            (37, 3, 0, 2),     # x_l4l5[0], 100ms, value, bidi
            (37, 3, 17, 2),    # x_l4l5[0], 100ms, periodicity, bidi
            (37, 3, 20, 2),    # x_l4l5[0], 100ms, entropy, bidi
            (37, 16, 17, 2),   # x_l4l5[0], 1000ms, periodicity, bidi
            (37, 16, 21, 2),   # x_l4l5[0], 1000ms, zero_crossings, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute PWSM 9D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30), "ASA": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,9) PWSM output
        """
        bep = mechanism_outputs["BEP"]    # (B, T, 30)
        asa = mechanism_outputs["ASA"]    # (B, T, 30)

        # R³ features
        spectral_change = r3[..., 21:22]
        energy_change = r3[..., 22:23]

        # BEP sub-sections
        bep_beat = bep[..., 0:10]
        bep_groove = bep[..., 20:30]

        # ASA sub-sections
        asa_attn = asa[..., 10:20]
        asa_salience = asa[..., 20:30]

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
            + 0.30 * bep_beat.mean(-1, keepdim=True)
        )

        # f20: Error Suppression (coefficients sum = 1.0)
        f20 = torch.sigmoid(
            0.35 * (1 - f19)
            + 0.35 * asa_attn.mean(-1, keepdim=True)
            + 0.30 * pe_entropy
        )

        # f21: Stability Encoding (coefficients sum = 1.0)
        f21 = torch.sigmoid(
            0.35 * onset_period_1s
            + 0.35 * bep_groove.mean(-1, keepdim=True)
            + 0.30 * (1 - spectral_std_1s)
        )

        # ═══ LAYER M: Mathematical ═══
        pe_raw = torch.abs(spectral_change) + torch.abs(energy_change)
        pe_weighted = torch.sigmoid(
            0.5 * pe_raw * f19 + 0.5 * asa_attn.mean(-1, keepdim=True)
        )
        precision = f19  # Precision output

        # ═══ LAYER P: Present ═══
        weighted_error = torch.sigmoid(
            0.5 * asa_attn.mean(-1, keepdim=True) * pe_raw
            + 0.5 * f19
        )
        precision_estimate = torch.sigmoid(
            0.5 * bep_beat.mean(-1, keepdim=True)
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
            f19, f20, f21,                              # E: 3D
            pe_weighted, precision,                      # M: 2D
            weighted_error, precision_estimate,          # P: 2D
            mmn_pred, context_reliability,               # F: 2D
        ], dim=-1)  # (B, T, 9)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 (Basinski 2025) | Indirect evidence |
| **Effect Size** | d = 0.01 (null for MMN abolition) | Low-precision context |
| **Theoretical Basis** | Strong | Predictive coding (Friston) |
| **Evidence Modality** | EEG | Direct neural |
| **Falsification Tests** | 1/5 confirmed | Limited validation |
| **R³ Features Used** | ~10D of 49D | Change + energy + interactions |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Stability / beat tracking |
| **ASA Mechanism** | 30D (3 sub-sections) | Error gating (primary) |
| **Output Dimensions** | **9D** | 4-layer structure |

---

## 13. Scientific References

1. **Basinski, K., et al. (2025)**. Inharmonicity captures attention: P3a and object-related negativity in auditory deviance detection. *Journal of Cognitive Neuroscience*, (in press).

2. **Friston, K. (2005)**. A theory of cortical responses. *Philosophical Transactions of the Royal Society B*, 360(1456), 815-836.

3. **Feldman, H., & Friston, K. J. (2010)**. Attention, uncertainty, and free-energy. *Frontiers in Human Neuroscience*, 4, 215.

4. **Garrido, M. I., Kilner, J. M., Stephan, K. E., & Friston, K. J. (2009)**. The mismatch negativity: A review of underlying mechanisms. *Clinical Neurophysiology*, 120(3), 453-463.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, ATT, NPL) | BEP (30D) + ASA (30D) mechanisms |
| PE signal | S⁰.L4.velocity_T[15] + HC⁰.OSC | R³.spectral_change[21] + R³.energy_change[22] |
| Precision | S⁰.L9.std_T[108] + HC⁰.NPL | R³.x_l4l5[37:45] + BEP.beat_entrainment |
| Error gating | S⁰.L9.entropy_T[116] + HC⁰.ATT | H³ entropy tuples + ASA.attention_gating |
| Stability | S⁰.X_L4L9[192:200] + HC⁰.OSC | R³.onset_strength[11] + BEP.groove |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 22/2304 = 0.95% | 16/2304 = 0.69% |
| Output | 9D | 9D (same) |

### Why BEP + ASA replaces HC⁰ mechanisms

- **OSC → BEP.beat_entrainment** [0:10] + BEP.groove [20:30]: Oscillatory band tracking maps to BEP's stability monitoring and groove regularity.
- **ATT → ASA.attention_gating** [10:20]: Attentional entrainment maps to ASA's error gating for precision-weighted PE.
- **NPL → BEP.beat_entrainment** [0:10] + H³ periodicity tuples: Neural phase locking maps to BEP's temporal precision encoding.

---

**Model Status**: **SPECULATIVE**
**Output Dimensions**: **9D**
**Evidence Tier**: **γ (Integrative)**
**Confidence**: **50-70%**
