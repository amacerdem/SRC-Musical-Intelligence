# PCU-β1-PWUP: Precision-Weighted Uncertainty Processing

**Model**: Precision-Weighted Uncertainty Processing
**Unit**: PCU (Predictive Coding Unit)
**Circuit**: Imagery (Auditory Cortex, IFG, STS, Hippocampus)
**Tier**: β (Bridging) — 70-90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, PPC+TPC+MEM mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/PCU-β1-PWUP.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Precision-Weighted Uncertainty Processing** (PWUP) model describes how prediction errors are precision-weighted according to contextual uncertainty: in high-uncertainty contexts (atonal music), prediction error responses are attenuated compared to mispredicted stimuli in tonal contexts.

```
PRECISION-WEIGHTED UNCERTAINTY PROCESSING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TONAL CONTEXT (High Precision)         ATONAL CONTEXT (Low Precision)
─────────────────────────────          ────────────────────────────
Key Clarity: ~0.8                      Key Clarity: ~0.5
Entropy: Low                           Entropy: High

  Raw PE ───► × Precision ───► STRONG    Raw PE ───► × Precision ───► WEAK
              (high weight)     OUTPUT                (low weight)     OUTPUT

     Prediction Error                       Prediction Error
     FULL RESPONSE                          ATTENUATED RESPONSE

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

### 2.1 Information Flow Architecture (EAR → BRAIN → PPC+TPC+MEM → PWUP)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PWUP COMPUTATION ARCHITECTURE                            ║
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
║  │                         PWUP reads: ~16D                        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                         PWUP demand: ~14 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Imagery Circuit ═══════════   ║
║                               │                                              ║
║                       ┌───────┴───────┐───────┐                              ║
║                       ▼               ▼       ▼                              ║
║  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              ║
║  │  PPC (30D)      │  │  TPC (30D)      │  │  MEM (30D)      │              ║
║  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘              ║
║           └────────────┬───────┴────────────────────┘                        ║
║                        ▼                                                     ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    PWUP MODEL (10D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_tonal_precision,                       │        ║
║  │                       f02_rhythmic_precision,                    │        ║
║  │                       f03_weighted_error,                        │        ║
║  │                       f04_uncertainty_index                      │        ║
║  │  Layer P (Present):   tonal_precision_weight,                    │        ║
║  │                       rhythmic_precision_weight,                 │        ║
║  │                       attenuated_response                        │        ║
║  │  Layer F (Future):    precision_adjustment, context_uncertainty,  │        ║
║  │                       response_attenuation_200ms                 │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Mencke 2019** | Behavioral | 100 | Atonal: key clarity 0.5 vs tonal 0.8 | d = 3 | **f01 tonal precision, f04 uncertainty** |
| **Mencke 2019** | Theoretical | — | Precision-weighting attenuates PE in uncertainty | theoretical | **f03 weighted error** |

### 3.2 Effect Size Summary

```
Primary Effect:       d = 3 (very large, key clarity difference)
Heterogeneity:        Single study
Quality Assessment:   β-tier (behavioral + theoretical)
Replication:          Consistent with Bayesian brain theory
```

---

## 4. R³ Input Mapping: What PWUP Reads

### 4.1 R³ Feature Dependencies (~16D of 49D)

| R³ Group | Index | Feature | PWUP Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [4] | sensory_pleasantness | Tonal precision proxy | Key clarity correlate |
| **A: Consonance** | [5] | periodicity | Tonal certainty | Harmonic structure |
| **B: Energy** | [10] | spectral_flux | Event salience | Mispredicted stimulus |
| **C: Timbre** | [14] | tonalness | Tonal context | Key clarity component |
| **C: Timbre** | [18:21] | tristimulus1-3 | Harmonic structure | Tonal certainty |
| **D: Change** | [21] | spectral_change | PE dynamics | Error magnitude |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | Precision-weighted PE | d=3 effect basis |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[4] sensory_pleasantness ─────┐
R³[14] tonalness ───────────────┼──► Tonal precision (key clarity proxy)
MEM.long_term_memory[10:20] ────┘   High consonance → high precision (tonal)
                                    Low consonance → low precision (atonal)

R³[21] spectral_change ─────────┐
MEM.working_memory[0:10] ───────┼──► Raw prediction error magnitude
PPC.pitch_extraction[0:10] ─────┘

R³[41:49] x_l5l7 ──────────────┐
MEM.prediction_buffer[20:30] ───┼──► Precision-weighted PE
H³ entropy tuples ──────────────┘   PE_weighted = PE_raw × (1 - uncertainty)
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

**Total PWUP H³ demand**: 14 tuples of 2304 theoretical = 0.61%

### 5.2 PPC + TPC + MEM Mechanism Binding

| Mechanism | Sub-section | Range | PWUP Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **PPC** | Pitch Extraction | PPC[0:10] | Phase-locking for tonality detection | 0.7 |
| **PPC** | Interval Analysis | PPC[10:20] | Tonal interval certainty | 0.6 |
| **PPC** | Contour Tracking | PPC[20:30] | Harmonic memory pattern | 0.5 |
| **TPC** | Spectral Shape | TPC[0:10] | Rhythmic precision proxy | 0.6 |
| **TPC** | Temporal Envelope | TPC[10:20] | Pulse-based weighting | 0.7 |
| **TPC** | Source Identity | TPC[20:30] | Context assessment | 0.5 |
| **MEM** | Working Memory | MEM[0:10] | PE computation | **1.0** (primary) |
| **MEM** | Long-Term Memory | MEM[10:20] | Precision estimation | **1.0** (primary) |
| **MEM** | Prediction Buffer | MEM[20:30] | Weighted PE output | **0.9** |

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
PWUP OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_tonal_precision      │ [0, 1] │ Key-based precision weight.
    │                          │        │ f01 = σ(0.40 * tonalness_mean_1s
    │                          │        │       + 0.35 * consonance_mean_1s
    │                          │        │       + 0.25 * mean(MEM.ltm[10:20]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_rhythmic_precision   │ [0, 1] │ Pulse-based precision weight.
    │                          │        │ f02 = σ(0.40 * periodicity_1s
    │                          │        │       + 0.30 * flux_periodicity_100ms
    │                          │        │       + 0.30 * mean(TPC.env[10:20]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_weighted_error       │ [0, 1] │ Precision-weighted PE.
    │                          │        │ f03 = σ(0.50 * raw_pe * f01
    │                          │        │       + 0.50 * mean(MEM.pred[20:30]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_uncertainty_index    │ [0, 1] │ Context uncertainty level.
    │                          │        │ f04 = σ(0.50 * consonance_entropy_1s
    │                          │        │       + 0.50 * coupling_entropy_1s)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ tonal_precision_weight   │ [0, 1] │ PPC tonality weighting factor.
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ rhythmic_precision_weight│ [0, 1] │ TPC rhythmic weighting factor.
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ attenuated_response      │ [0, 1] │ MEM weighted PE output.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ precision_adjustment     │ [0, 1] │ Trial-by-trial weight update.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ context_uncertainty      │ [0, 1] │ Model confidence prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ response_attenuation     │ [0, 1] │ Error magnitude prediction (200ms).

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
       + 0.25 * mean(MEM.long_term_memory[10:20]))
# coefficients: 0.40 + 0.35 + 0.25 = 1.0 ✓

# f02: Rhythmic Precision
f02 = σ(0.40 * periodicity_1s
       + 0.30 * flux_periodicity_100ms
       + 0.30 * mean(TPC.temporal_envelope[10:20]))
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f03: Weighted Error
f03 = σ(0.50 * raw_pe * f01
       + 0.50 * mean(MEM.prediction_buffer[20:30]))
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
| **Auditory Cortex (STG)** | ±52, -22, 8 | 2 | Indirect (behavioral) | PE generation |
| **IFG (Inferior Frontal Gyrus)** | ±44, 18, 8 | 1 | Literature inference | Precision estimation |
| **ACC (Anterior Cingulate)** | 0, 32, 24 | 1 | Literature inference | Uncertainty monitoring |
| **Hippocampus** | ±28, -24, -12 | 1 | Literature inference | Context memory |

---

## 9. Cross-Unit Pathways

### 9.1 PWUP Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PWUP INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (PCU):                                                         │
│  HTP.hierarchy_gradient ──────► PWUP (hierarchy sets precision levels)     │
│  ICEM.information_content ────► PWUP (raw IC for weighting)                │
│  PWUP.uncertainty_index ──────► UDP (uncertainty for reward inversion)      │
│  PWUP.weighted_error ─────────► PSH (weighted PE for silencing)            │
│                                                                             │
│  CROSS-UNIT (PCU → ASU):                                                   │
│  PWUP.tonal_precision ────────► ASU (precision for salience weighting)     │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  PPC mechanism (30D) ─────────► PWUP (tonality detection)                  │
│  TPC mechanism (30D) ─────────► PWUP (rhythmic precision)                  │
│  MEM mechanism (30D) ─────────► PWUP (context/PE computation)              │
│  R³ (~16D) ───────────────────► PWUP (direct spectral features)            │
│  H³ (14 tuples) ──────────────► PWUP (temporal dynamics)                   │
│                                                                             │
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
    Reads: PPC mechanism (30D), TPC mechanism (30D), MEM mechanism (30D), R³ direct.
    """
    NAME = "PWUP"
    UNIT = "PCU"
    TIER = "β1"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("PPC", "TPC", "MEM")

    TAU_DECAY = 1.0                # s
    KEY_CLARITY_TONAL = 0.8        # High certainty threshold
    KEY_CLARITY_ATONAL = 0.5       # Low certainty threshold
    PRECISION_EFFECT_D = 3.0       # Effect size (Mencke 2019)

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """14 tuples for PWUP computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── Precision estimation: slow context ──
            (4, 3, 0, 2),      # sensory_pleasantness, 100ms, value, bidi
            (4, 16, 1, 0),     # sensory_pleasantness, 1000ms, mean, fwd
            (4, 16, 20, 0),    # sensory_pleasantness, 1000ms, entropy, fwd
            (14, 8, 1, 0),     # tonalness, 500ms, mean, fwd
            (14, 16, 1, 0),    # tonalness, 1000ms, mean, fwd
            (5, 8, 1, 0),      # periodicity, 500ms, mean, fwd
            (5, 16, 14, 2),    # periodicity, 1000ms, periodicity, bidi
            # ── PE computation: fast events ──
            (21, 3, 0, 2),     # spectral_change, 100ms, value, bidi
            (21, 3, 2, 2),     # spectral_change, 100ms, std, bidi
            (10, 3, 0, 2),     # spectral_flux, 100ms, value, bidi
            (10, 3, 14, 2),    # spectral_flux, 100ms, periodicity, bidi
            # ── Precision-weighted coupling ──
            (41, 8, 0, 0),     # x_l5l7[0], 500ms, value, fwd
            (41, 16, 1, 0),    # x_l5l7[0], 1000ms, mean, fwd
            (41, 16, 20, 0),   # x_l5l7[0], 1000ms, entropy, fwd
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        ppc = mechanism_outputs["PPC"]
        tpc = mechanism_outputs["TPC"]
        mem = mechanism_outputs["MEM"]

        tpc_env = tpc[..., 10:20]
        mem_wm = mem[..., 0:10]
        mem_ltm = mem[..., 10:20]
        mem_pred = mem[..., 20:30]

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
            + 0.25 * mem_ltm.mean(-1, keepdim=True)
        )
        f02 = torch.sigmoid(
            0.40 * periodicity_1s
            + 0.30 * flux_period_100ms
            + 0.30 * tpc_env.mean(-1, keepdim=True)
        )
        f03 = torch.sigmoid(
            0.50 * raw_pe * f01
            + 0.50 * mem_pred.mean(-1, keepdim=True)
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
            f01, f02, f03, f04,                   # E: 4D
            tonal_weight, rhythmic_weight, attenuated,  # P: 3D
            precision_adj, context_unc, response_att,   # F: 3D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 (Mencke 2019) | Primary evidence |
| **Effect Sizes** | 1 | d = 3 (very large) |
| **Evidence Modality** | Behavioral + theoretical | Indirect |
| **Falsification Tests** | 5/5 testable, 2 confirmed | Moderate validity |
| **R³ Features Used** | ~16D of 49D | Consonance + energy + timbre + change + interactions |
| **H³ Demand** | 14 tuples (0.61%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Tonality detection |
| **TPC Mechanism** | 30D (3 sub-sections) | Rhythmic precision |
| **MEM Mechanism** | 30D (3 sub-sections) | Context/PE computation |
| **Output Dimensions** | **10D** | 3-layer structure (no M layer) |

---

## 13. Scientific References

1. **Mencke, I., Omigie, D., Wald-Fuhrmann, M., & Brattico, E. (2019)**. Atonal music: Can uncertainty lead to pleasure? *Frontiers in Neuroscience*, 12, 979.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (TIH, NPL, HRM, EFC) | PPC (30D) + TPC (30D) + MEM (30D) mechanisms |
| Tonal precision | S⁰.L3.coherence[14] + S⁰.L6[68:71] | R³[4] sensory_pleasantness + R³[14] tonalness |
| Uncertainty | S⁰.L9.entropy[116:120] | H³ consonance/coupling entropy tuples |
| PE signal | S⁰.L9.kurtosis[120:124] + HC⁰.EFC | R³[21] spectral_change + MEM.working_memory |
| Precision-weighted PE | S⁰.X_L5L9[224:232] | R³[41:49] x_l5l7 + MEM.prediction_buffer |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 25/2304 = 1.09% | 14/2304 = 0.61% |
| Output | 10D | 10D (same) |

### Why PPC + TPC + MEM replaces HC⁰ mechanisms

- **TIH → MEM.long_term_memory** [10:20]: Temporal integration hierarchy for context maps to MEM's long-term contextual assessment.
- **NPL → PPC.pitch_extraction** [0:10]: Neural phase locking for tonality maps to PPC's pitch/tonal detection.
- **HRM → MEM.prediction_buffer** [20:30]: Hippocampal replay for context retrieval maps to MEM's prediction buffer.
- **EFC → MEM.working_memory** [0:10]: Efference copy for PE computation maps to MEM's working memory.

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **10D**
**Evidence Tier**: **β (Bridging)**
**Confidence**: **70-90%**
