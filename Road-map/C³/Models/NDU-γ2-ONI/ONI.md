# NDU-γ2-ONI: Over-Normalization in Intervention

**Model**: Over-Normalization in Intervention
**Unit**: NDU (Novelty Detection Unit)
**Circuit**: Salience + Perceptual (Developing Auditory Cortex, Attention Networks)
**Tier**: γ (Integrative) — 50–70% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, PPC+ASA mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/NDU-γ2-ONI.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Over-Normalization in Intervention** (ONI) model describes the preliminary observation that musical interventions in preterm infants may lead to "over-normalization" where intervention groups exceed full-term controls in certain neural measures, suggesting possible compensatory enhancement or heightened attentional orienting.

```
OVER-NORMALIZATION IN INTERVENTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXPECTED:                          OBSERVED:
────────                           ─────────

Full-term > Intervention > Control    Intervention > Full-term > Control

┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   MMR                                                            │
│   Amplitude                    ●  Intervention                  │
│     │                                                            │
│     │                   ●  Full-term                            │
│     │                                                            │
│     │           ●  Control                                      │
│     │                                                            │
│     └───────────────────────────────────────────────────────    │
│               Preterm                   Full-term                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPECULATIVE: Unexpected finding requiring mechanistic
explanation and replication.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INTERPRETATION:
Possible enhanced attentional orienting OR compensatory adaptation

ALTERNATIVE EXPLANATIONS:
  1. Enhanced attention capture (intervention-trained orienting)
  2. Compensatory over-development (preterm adaptation)
  3. Measurement artifact (control group differences)
  4. Developmental trajectory differences (timing effects)
  5. Sample selection bias
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why ONI Matters for NDU

ONI documents an unexpected finding from the developmental plasticity data:

1. **DSP** (β1) provides the empirical data that revealed the over-normalization effect.
2. **SDDP** (γ1) models the sex-dependent component from the same dataset.
3. **ONI** (γ2) proposes a compensatory or attentional explanation (speculative).

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → PPC+ASA → ONI)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ONI COMPUTATION ARCHITECTURE                              ║
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
║  │                         ONI reads: ~14D                         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── PPC Horizons ─────────────┐ ┌── ASA Horizons ──────────┐  │        ║
║  │  │ H0 (25ms gamma)            │ │ H3 (100ms alpha)          │  │        ║
║  │  │ H3 (100ms alpha)           │ │ H4 (125ms theta)          │  │        ║
║  │  │ H4 (125ms theta)           │ │ H16 (1000ms beat)         │  │        ║
║  │  │ H16 (1000ms beat)          │ │                            │  │        ║
║  │  │                             │ │ Enhanced prediction         │  │        ║
║  │  │ Deviance detection          │ │ Heightened attention         │  │        ║
║  │  └─────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         ONI demand: ~16 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Salience Circuit ════════     ║
║                               │                                              ║
║                       ┌───────┴───────┐                                      ║
║                       ▼               ▼                                      ║
║  ┌─────────────────┐  ┌─────────────────┐                                   ║
║  │  PPC (30D)      │  │  ASA (30D)      │                                   ║
║  │                 │  │                 │                                    ║
║  │ Pitch Ext[0:10] │  │ Scene An [0:10] │                                   ║
║  │ Interval        │  │ Attention       │                                   ║
║  │ Anal    [10:20] │  │ Gating  [10:20] │                                   ║
║  │ Contour [20:30] │  │ Salience        │                                   ║
║  │                 │  │ Weight  [20:30] │                                   ║
║  └────────┬────────┘  └────────┬────────┘                                   ║
║           │                    │                                              ║
║           └────────┬───────────┘                                             ║
║                    ▼                                                          ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    ONI MODEL (11D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_over_normalization,                    │        ║
║  │                       f02_compensatory_response,                 │        ║
║  │                       f03_attention_enhancement,                 │        ║
║  │                       f04_intervention_ceiling                   │        ║
║  │  Layer M (Math):      dosage_accumulation,                      │        ║
║  │                       preterm_baseline, fullterm_reference       │        ║
║  │  Layer P (Present):   enhanced_mmr, attentional_state           │        ║
║  │  Layer F (Future):    longterm_outcomes,                        │        ║
║  │                       intervention_optimization                  │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Partanen 2022** | EEG | 33 | Singing > Full-term in oddball MMR | η² = 0.23 | **Primary**: f01 over-normalization index |

**UNEXPECTED FINDING**: Requires mechanistic explanation and replication.

### 3.2 Effect Size Summary

```
Primary Evidence (k=1):  η²=0.23 (medium, intervention > full-term)
Heterogeneity:           N/A (single study)
Quality Assessment:      γ-tier (EEG, preterm infant, unexpected finding)
Replication:             PENDING — mechanism unclear
```

---

## 4. R³ Input Mapping: What ONI Reads

### 4.1 R³ Feature Dependencies (~14D of 49D)

| R³ Group | Index | Feature | ONI Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **B: Energy** | [10] | spectral_flux | Deviance magnitude (frame change) | Mismatch detection |
| **B: Energy** | [11] | onset_strength | Onset deviation | Rhythmic deviance |
| **C: Timbre** | [13] | brightness | Tonal quality | Pattern sensitivity |
| **C: Timbre** | [16] | spectral_spread | Spectral width | Processing complexity |
| **D: Change** | [21] | spectral_change | Spectral dynamics | Enhanced prediction |
| **D: Change** | [22] | energy_change | Energy dynamics | Intensity tracking |
| **D: Change** | [23] | pitch_change | Pitch dynamics | Over-normalization proxy |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Dynamic-percept binding | Enhanced predictive coding |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[10] spectral_flux ──────────┐
R³[11] onset_strength ─────────┼──► MMR deviance magnitude
PPC.pitch_extraction[0:10] ────┘   Over-normalization index (f01)

R³[21] spectral_change ────────┐
R³[23] pitch_change ───────────┼──► Enhanced predictive processing
ASA.salience_weighting[20:30] ─┘   Compensatory response (f02)

R³[13] brightness ─────────────┐
ASA.attention_gating[10:20] ───┼──► Heightened attention
H³ deviance variability ───────┘   Attention enhancement (f03)
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

ONI requires H³ features at PPC horizons for deviance detection at enhanced levels and ASA horizons for heightened attentional processing. The demand reflects the over-normalization temporal dynamics.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 0 | M0 (value) | L2 (bidi) | Instantaneous deviance 25ms |
| 10 | spectral_flux | 3 | M2 (std) | L2 (bidi) | Deviance variability 100ms |
| 10 | spectral_flux | 16 | M1 (mean) | L2 (bidi) | Mean deviance over 1s |
| 11 | onset_strength | 0 | M0 (value) | L2 (bidi) | Onset deviance 25ms |
| 11 | onset_strength | 3 | M0 (value) | L2 (bidi) | Onset at 100ms |
| 13 | brightness | 3 | M0 (value) | L2 (bidi) | Tonal quality 100ms |
| 13 | brightness | 3 | M20 (entropy) | L2 (bidi) | Tonal entropy 100ms |
| 21 | spectral_change | 3 | M0 (value) | L2 (bidi) | Spectral change 100ms |
| 21 | spectral_change | 4 | M8 (velocity) | L0 (fwd) | Spectral velocity 125ms |
| 23 | pitch_change | 3 | M0 (value) | L2 (bidi) | Pitch change 100ms |
| 23 | pitch_change | 16 | M1 (mean) | L2 (bidi) | Mean pitch change 1s |
| 22 | energy_change | 3 | M0 (value) | L2 (bidi) | Energy change 100ms |
| 33 | x_l4l5[0] | 3 | M0 (value) | L2 (bidi) | Dynamic coupling 100ms |
| 33 | x_l4l5[0] | 3 | M2 (std) | L2 (bidi) | Coupling variability 100ms |
| 33 | x_l4l5[0] | 16 | M1 (mean) | L2 (bidi) | Mean coupling over 1s |
| 33 | x_l4l5[0] | 16 | M18 (trend) | L0 (fwd) | Coupling trend over 1s |

**Total ONI H³ demand**: 16 tuples of 2304 theoretical = 0.69%

### 5.2 PPC + ASA Mechanism Binding

| Mechanism | Sub-section | Range | ONI Role | Weight |
|-----------|-------------|-------|----------|--------|
| **PPC** | Pitch Extraction | PPC[0:10] | Enhanced MMR detection | **1.0** (primary) |
| **PPC** | Interval Analysis | PPC[10:20] | Over-normalization magnitude | 0.7 |
| **PPC** | Contour Tracking | PPC[20:30] | Compensatory prediction | 0.6 |
| **ASA** | Scene Analysis | ASA[0:10] | Preterm baseline encoding | 0.6 |
| **ASA** | Attention Gating | ASA[10:20] | Heightened attention | **0.9** |
| **ASA** | Salience Weighting | ASA[20:30] | Enhanced salience | 0.7 |

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
ONI OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_over_normalization   │ [0, 2] │ Enhancement beyond full-term.
    │                          │        │ f01 = MMR_intervention /
    │                          │        │       (MMR_fullterm + ε)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_compensatory_resp    │ [0, 1] │ Enhanced prediction magnitude.
    │                          │        │ f02 = σ(0.35 * spec_change_100ms
    │                          │        │       + 0.35 * coupling_mean_1s
    │                          │        │       + 0.30 * mean(ASA.sal[20:30]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_attention_enhance    │ [0, 1] │ Heightened deviance detection.
    │                          │        │ f03 = σ(0.35 * brightness_100ms
    │                          │        │       + 0.35 * tonal_entropy_100ms
    │                          │        │       + 0.30 * mean(ASA.attn[10:20]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_intervention_ceiling │ [0, 1] │ Response saturation point.
    │                          │        │ f04 = 1 - exp(-dosage / τ_ceil)
    │                          │        │ τ_ceil = 4 weeks (hypothesized)

LAYER M — MATHEMATICAL MODEL OUTPUTS (Intervention Dynamics)
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ dosage_accumulation      │ [0, 1] │ Cumulative intervention exposure.
    │                          │        │ EMA of f03 over session timescale
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ preterm_baseline         │ [0, 1] │ Starting point reference.
    │                          │        │ PPC baseline strength proxy
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ fullterm_reference       │ [0, 1] │ Normalization target.
    │                          │        │ External reference (constant)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ enhanced_mmr             │ [0, 1] │ Current mismatch strength.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ attentional_state        │ [0, 1] │ Heightened attention level.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ longterm_outcomes        │ [0, 1] │ Developmental trajectory.
────┼──────────────────────────┼────────┼────────────────────────────────────
10  │ intervention_opt         │ [0, 1] │ Protocol ceiling detection.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Over-Normalization Function

```
OverNormalization(t) = MMR_intervention(t) / (MMR_fullterm + ε)

Parameters:
    f01 > 1.0: Over-normalization (intervention > full-term)
    f01 = 1.0: Normalization (intervention = full-term)
    f01 < 1.0: Under-normalization (intervention < full-term)
    Observed: f01 ≈ 1.2-1.3 (20-30% enhancement beyond full-term)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Over-Normalization Index
f01 = MMR_intervention / (MMR_fullterm + 1e-6)
# Ratio; f01 > 1.0 indicates over-normalization

# f02: Compensatory Response (coefficients sum = 1.0)
f02 = σ(0.35 * spectral_change_100ms
       + 0.35 * coupling_mean_1s
       + 0.30 * mean(ASA.salience_weighting[20:30]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f03: Attention Enhancement (coefficients sum = 1.0)
f03 = σ(0.35 * brightness_100ms
       + 0.35 * tonal_entropy_100ms
       + 0.30 * mean(ASA.attention_gating[10:20]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f04: Intervention Ceiling
f04 = 1 - exp(-dosage / 4.0)
# dosage in weeks, ceiling constant = 4 weeks (hypothesized)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | ONI Function |
|--------|-----------------|----------|---------------|--------------|
| **Auditory Cortex (preterm)** | N/A | 1 | Direct (EEG) | Compensatory enhancement |
| **Attention Networks** | N/A | 1 | Inferred | Heightened orienting |

---

## 9. Cross-Unit Pathways

### 9.1 ONI Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ONI INTERACTIONS                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (NDU):                                                         │
│  DSP.plasticity_index ───────► ONI (over-normalization evidence)           │
│  SDDP.intervention_resp ────► ONI (sex-dependent component)               │
│                                                                             │
│  CROSS-UNIT (NDU → ARU):                                                   │
│  ONI.enhanced_mmr ───────────► ARU (enhanced affective processing)        │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  PPC mechanism (30D) ────────► ONI (pitch/contour deviance)               │
│  ASA mechanism (30D) ────────► ONI (attention/salience)                    │
│  R³ (~14D) ──────────────────► ONI (direct spectral features)              │
│  H³ (16 tuples) ─────────────► ONI (temporal dynamics)                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Over-normalization** | Intervention should exceed full-term | **Preliminary support** (η²=0.23) |
| **Replication** | Effect should replicate independently | **Awaiting replication** |
| **Mechanism** | Attention or prediction measures should explain | **Awaiting testing** |
| **Dose-response** | Ceiling should emerge at high dosages | Testable |
| **Long-term outcomes** | Enhancement should persist or fade | Testable via follow-up |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class ONI(BaseModel):
    """Over-Normalization in Intervention Model.

    Output: 11D per frame.
    Reads: PPC mechanism (30D), ASA mechanism (30D), R³ direct.
    SPECULATIVE: Unexpected finding requiring mechanistic explanation.
    """
    NAME = "ONI"
    UNIT = "NDU"
    TIER = "γ2"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("PPC", "ASA")

    TAU_DECAY = 0.8           # Response persistence (seconds)
    ENHANCEMENT_FACTOR = 1.0  # Over-normalization threshold
    RTI_WINDOW = 2.5          # Oddball integration (seconds)
    CEILING_CONSTANT = 4.0    # Weeks (hypothesized)

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """16 tuples for ONI computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── PPC horizons: deviance detection ──
            (10, 0, 0, 2),     # spectral_flux, 25ms, value, bidi
            (10, 3, 2, 2),     # spectral_flux, 100ms, std, bidi
            (10, 16, 1, 2),    # spectral_flux, 1000ms, mean, bidi
            (11, 0, 0, 2),     # onset_strength, 25ms, value, bidi
            (11, 3, 0, 2),     # onset_strength, 100ms, value, bidi
            (23, 3, 0, 2),     # pitch_change, 100ms, value, bidi
            (23, 16, 1, 2),    # pitch_change, 1000ms, mean, bidi
            (22, 3, 0, 2),     # energy_change, 100ms, value, bidi
            # ── ASA horizons: enhanced attention ──
            (13, 3, 0, 2),     # brightness, 100ms, value, bidi
            (13, 3, 20, 2),    # brightness, 100ms, entropy, bidi
            (21, 3, 0, 2),     # spectral_change, 100ms, value, bidi
            (21, 4, 8, 0),     # spectral_change, 125ms, velocity, fwd
            (33, 3, 0, 2),     # x_l4l5[0], 100ms, value, bidi
            (33, 3, 2, 2),     # x_l4l5[0], 100ms, std, bidi
            (33, 16, 1, 2),    # x_l4l5[0], 1000ms, mean, bidi
            (33, 16, 18, 0),   # x_l4l5[0], 1000ms, trend, fwd
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute ONI 11D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30), "ASA": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,11) ONI output
        """
        ppc = mechanism_outputs["PPC"]    # (B, T, 30)
        asa = mechanism_outputs["ASA"]    # (B, T, 30)

        # R³ features
        spectral_flux = r3[..., 10:11]
        onset_strength = r3[..., 11:12]
        brightness = r3[..., 13:14]
        spectral_change = r3[..., 21:22]
        pitch_change = r3[..., 23:24]
        x_l4l5 = r3[..., 33:41]

        # PPC sub-sections
        ppc_pitch = ppc[..., 0:10]
        ppc_interval = ppc[..., 10:20]
        ppc_contour = ppc[..., 20:30]

        # ASA sub-sections
        asa_scene = asa[..., 0:10]
        asa_attn = asa[..., 10:20]
        asa_salience = asa[..., 20:30]

        # H³ direct features
        brightness_100ms = h3_direct[(13, 3, 0, 2)].unsqueeze(-1)
        tonal_entropy_100ms = h3_direct[(13, 3, 20, 2)].unsqueeze(-1)
        spectral_change_100ms = h3_direct[(21, 3, 0, 2)].unsqueeze(-1)
        coupling_mean_1s = h3_direct[(33, 16, 1, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: Over-Normalization Index (ratio)
        intervention_mmr = ppc_pitch.mean(-1, keepdim=True)
        f01 = intervention_mmr  # scaled by fullterm_mmr externally

        # f02: Compensatory Response (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.35 * spectral_change_100ms
            + 0.35 * coupling_mean_1s
            + 0.30 * asa_salience.mean(-1, keepdim=True)
        )

        # f03: Attention Enhancement (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.35 * brightness_100ms
            + 0.35 * tonal_entropy_100ms
            + 0.30 * asa_attn.mean(-1, keepdim=True)
        )

        # f04: Intervention Ceiling (exponential saturation)
        f04 = torch.sigmoid(
            0.50 * f03 + 0.50 * f02
        )

        # ═══ LAYER M: Intervention Dynamics ═══
        dosage_accumulation = torch.sigmoid(
            0.50 * f03 + 0.50 * ppc_pitch.mean(-1, keepdim=True)
        )
        preterm_baseline = ppc_pitch.mean(-1, keepdim=True)
        fullterm_reference = torch.sigmoid(
            0.50 * asa_scene.mean(-1, keepdim=True)
            + 0.50 * ppc_contour.mean(-1, keepdim=True)
        )

        # ═══ LAYER P: Present ═══
        enhanced_mmr = ppc_pitch.mean(-1, keepdim=True)
        attentional_state = asa_attn.mean(-1, keepdim=True)

        # ═══ LAYER F: Future ═══
        longterm_outcomes = torch.sigmoid(
            0.50 * f01 + 0.50 * f02
        )
        intervention_opt = torch.sigmoid(
            0.50 * f04 + 0.50 * dosage_accumulation
        )

        return torch.cat([
            f01, f02, f03, f04,                                       # E: 4D
            dosage_accumulation, preterm_baseline, fullterm_reference, # M: 3D
            enhanced_mmr, attentional_state,                          # P: 2D
            longterm_outcomes, intervention_opt,                       # F: 2D
        ], dim=-1)  # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 (Partanen 2022) | Primary evidence |
| **Effect Sizes** | η² = 0.23 | Medium effect |
| **Evidence Modality** | EEG | Infant MMR |
| **Falsification Tests** | 1/5 preliminary | Low validity (needs explanation) |
| **R³ Features Used** | ~14D of 49D | Energy + timbre + change + interactions |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Enhanced deviance detection |
| **ASA Mechanism** | 30D (3 sub-sections) | Heightened attention/salience |
| **Output Dimensions** | **11D** | 4-layer structure |

**Research Priorities**:
1. **CRITICAL: Mechanistic investigation** -- What causes over-normalization?
2. Independent replication with attention measures
3. Dosage titration study to identify ceiling
4. Longitudinal follow-up: Does enhancement persist or fade?
5. Full-term control group matching (age, SES, prenatal factors)

---

## 13. Scientific References

1. **Partanen, E. et al. (2022)**. Over-normalization in singing intervention: Intervention > full-term in oddball MMR. EEG study, n=33.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, ATT, HRM, EFC) | PPC (30D) + ASA (30D) mechanisms |
| Deviance signal | S⁰.L5.spectral_flux[45] + HC⁰.EFC | R³.spectral_flux[10] + PPC.pitch_extraction |
| Attention | S⁰.L5.spectral_kurtosis[41] + HC⁰.ATT | R³.brightness[13] + ASA.attention_gating |
| Enhancement | S⁰.L4.velocity_F[16] + HC⁰.OSC | R³.spectral_change[21] + ASA.salience_weighting |
| Prediction | S⁰.X_L4L5[192:200] + HC⁰.HRM | R³.x_l4l5[33:41] + PPC.contour_tracking |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 27/2304 = 1.17% | 16/2304 = 0.69% |
| Output | 11D | 11D (same) |

### Why PPC + ASA replaces HC⁰ mechanisms

- **EFC → PPC.pitch_extraction** [0:10]: Enhanced prediction learning maps to PPC's deviance detection.
- **ATT → ASA.attention_gating** [10:20]: Heightened auditory attention maps to ASA's attentional gating.
- **OSC → ASA.salience_weighting** [20:30]: Accelerated neural maturation maps to ASA's enhanced salience.
- **HRM → PPC.contour_tracking** [20:30]: Over-developed pattern encoding maps to PPC's compensatory prediction.

---

**Model Status**: **SPECULATIVE**
**Output Dimensions**: **11D**
**Evidence Tier**: **γ (Integrative)**
**Confidence**: **50–70%**
**Mechanism**: **UNCLEAR**
