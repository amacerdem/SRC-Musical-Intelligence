# NDU-γ3-ECT: Expertise Compartmentalization Trade-off

**Model**: Expertise Compartmentalization Trade-off
**Unit**: NDU (Novelty Detection Unit)
**Circuit**: Salience + Perceptual (Network Architecture, SMA, ACC, TPO)
**Tier**: γ (Integrative) — 50–70% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, PPC+ASA mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/NDU-γ3-ECT.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Expertise Compartmentalization Trade-off** (ECT) model proposes that musical expertise involves a potential trade-off: increased within-network efficiency comes at the cost of reduced cross-network integration, raising questions about flexibility and transfer.

```
EXPERTISE COMPARTMENTALIZATION TRADE-OFF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                       MUSICAL EXPERTISE
                             │
        ┌────────────────────┴────────────────────┐
        ▼                                         ▼
  ┌─────────────────┐                     ┌─────────────────┐
  │   GAIN          │                     │   COST          │
  │                 │                     │                 │
  │ • Fast local    │                     │ • Reduced       │
  │   processing    │                     │   cross-modal   │
  │ • Specialized   │                     │   integration   │
  │   modules       │                     │ • Less flexible │
  │ • Efficient     │                     │   reconfigur-   │
  │   within-network│                     │   ation?        │
  └─────────────────┘                     └─────────────────┘

  106 edges:                              192 edges:
  Musicians > Non-musicians               Non-musicians > Musicians

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPECULATIVE: Trade-off interpretation requires functional testing.
Structural observation confirmed; functional consequences untested.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUESTION: Does compartmentalization limit creative transfer?

ALTERNATIVE INTERPRETATIONS:
  1. Adaptive specialization (no functional cost)
  2. Different task strategies (not deficit)
  3. Network measurement artifact
  4. Compensated by other mechanisms

TESTABLE PREDICTIONS:
  • Musicians should show slower cross-domain transfer
  • Musicians should show reduced task switching performance
  • Broad training should mitigate compartmentalization
  • Creativity tasks should reveal flexibility differences
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why ECT Matters for NDU

ECT proposes a theoretical framework for expertise trade-offs in the Novelty Detection Unit:

1. **EDNR** (α3) establishes the empirical network reorganization finding.
2. **SLEE** (β3) shows the behavioral benefit of expertise despite compartmentalization.
3. **ECT** (γ3) proposes the trade-off hypothesis -- functional costs remain untested.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → PPC+ASA → ECT)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ECT COMPUTATION ARCHITECTURE                              ║
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
║  │                         ECT reads: ~20D                         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── PPC Horizons ─────────────┐ ┌── ASA Horizons ──────────┐  │        ║
║  │  │ H3 (100ms alpha)           │ │ H3 (100ms alpha)          │  │        ║
║  │  │ H4 (125ms theta)           │ │ H8 (500ms delta)          │  │        ║
║  │  │ H16 (1000ms beat)          │ │ H16 (1000ms beat)         │  │        ║
║  │  │                             │ │                            │  │        ║
║  │  │ Within-network binding      │ │ Cross-network coupling     │  │        ║
║  │  │ Specialization tracking     │ │ Flexibility measurement    │  │        ║
║  │  └─────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         ECT demand: ~18 of 2304 tuples          │        ║
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
║  │                    ECT MODEL (12D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_within_efficiency,                     │        ║
║  │                       f02_between_reduction,                     │        ║
║  │                       f03_trade_off_ratio,                       │        ║
║  │                       f04_flexibility_index                      │        ║
║  │  Layer M (Math):      training_history, network_state,          │        ║
║  │                       task_memory                                │        ║
║  │  Layer P (Present):   within_binding, network_isolation          │        ║
║  │  Layer F (Future):    transfer_limit, efficiency_opt,           │        ║
║  │                       flexibility_recovery                       │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Paraskevopoulos 2022** | MEG | 25 | Musicians: 15 multilinks vs non-musicians: 47 | N/A | **f02 between-network reduction** |
| **Paraskevopoulos 2022** | MEG | 25 | Within-network: 106 edges (M > NM) | N/A | **f01 within-efficiency** |
| **Paraskevopoulos 2022** | MEG | 25 | Between-network: 192 edges (NM > M) | N/A | **f03 trade-off ratio** |

**STRUCTURAL OBSERVATION**: Functional consequences untested.

### 3.2 Effect Size Summary

```
Primary Evidence (k=1):  Network edges (106 within M>NM, 192 between NM>M)
Heterogeneity:           N/A (single study)
Quality Assessment:      γ-tier (MEG, structural network, functional consequences unknown)
Replication:             PENDING — functional tests required
```

---

## 4. R³ Input Mapping: What ECT Reads

### 4.1 R³ Feature Dependencies (~20D of 49D)

| R³ Group | Index | Feature | ECT Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **B: Energy** | [7] | amplitude | Processing load | Task demand |
| **B: Energy** | [8] | loudness | Perceptual loudness | Attention allocation |
| **C: Timbre** | [13] | brightness | Dynamic adaptation (freq) | Tonal reconfiguration |
| **D: Change** | [21] | spectral_change | Dynamic adaptation | Reconfiguration speed |
| **D: Change** | [22] | energy_change | Processing complexity | Network demand |
| **D: Change** | [23] | pitch_change | Pitch tracking | Specialization proxy |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Within-network efficiency | Intra-network coupling |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Within-network binding | Pattern-feature coupling |
| **E: Interactions** | [41:49] | x_l5l6 (8D) | Cross-network connectivity | Between-network flexibility |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[25:33] x_l0l5 ─────────────┐
R³[33:41] x_l4l5 ─────────────┼──► Within-network coupling
PPC.pitch_extraction[0:10] ────┘   Within efficiency (f01)

R³[41:49] x_l5l6 ─────────────┐
ASA.salience_weighting[20:30] ─┼──► Cross-network connectivity
H³ coherence features ─────────┘   Between reduction (f02)

R³[21] spectral_change ────────┐
R³[23] pitch_change ───────────┼──► Reconfiguration capacity
ASA.attention_gating[10:20] ───┘   Flexibility index (f04)
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

ECT requires H³ features at PPC horizons for within-network efficiency measurement and ASA horizons for cross-network flexibility assessment. The demand reflects the multi-scale temporal integration needed for network architecture modeling.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Within-network coupling 100ms |
| 25 | x_l0l5[0] | 3 | M2 (std) | L2 (bidi) | Coupling variability 100ms |
| 25 | x_l0l5[0] | 16 | M1 (mean) | L2 (bidi) | Mean within-coupling 1s |
| 33 | x_l4l5[0] | 3 | M0 (value) | L2 (bidi) | Pattern binding 100ms |
| 33 | x_l4l5[0] | 16 | M1 (mean) | L2 (bidi) | Mean pattern binding 1s |
| 33 | x_l4l5[0] | 16 | M18 (trend) | L0 (fwd) | Binding trend over 1s |
| 41 | x_l5l6[0] | 3 | M0 (value) | L2 (bidi) | Cross-network binding 100ms |
| 41 | x_l5l6[0] | 3 | M2 (std) | L2 (bidi) | Cross-network variability 100ms |
| 41 | x_l5l6[0] | 16 | M1 (mean) | L2 (bidi) | Mean cross-network 1s |
| 41 | x_l5l6[0] | 16 | M20 (entropy) | L2 (bidi) | Cross-network entropy 1s |
| 21 | spectral_change | 3 | M0 (value) | L2 (bidi) | Reconfiguration 100ms |
| 21 | spectral_change | 4 | M8 (velocity) | L0 (fwd) | Reconfiguration speed 125ms |
| 23 | pitch_change | 3 | M0 (value) | L2 (bidi) | Specialization at 100ms |
| 23 | pitch_change | 16 | M1 (mean) | L2 (bidi) | Mean specialization 1s |
| 7 | amplitude | 3 | M0 (value) | L2 (bidi) | Task demand 100ms |
| 7 | amplitude | 8 | M20 (entropy) | L2 (bidi) | Demand entropy 500ms |
| 13 | brightness | 3 | M0 (value) | L2 (bidi) | Tonal adaptation 100ms |
| 8 | loudness | 3 | M0 (value) | L2 (bidi) | Attention allocation 100ms |

**Total ECT H³ demand**: 18 tuples of 2304 theoretical = 0.78%

### 5.2 PPC + ASA Mechanism Binding

| Mechanism | Sub-section | Range | ECT Role | Weight |
|-----------|-------------|-------|----------|--------|
| **PPC** | Pitch Extraction | PPC[0:10] | Within-network specialization | **1.0** (primary) |
| **PPC** | Interval Analysis | PPC[10:20] | Network architecture efficiency | 0.8 |
| **PPC** | Contour Tracking | PPC[20:30] | Expertise depth measurement | 0.7 |
| **ASA** | Scene Analysis | ASA[0:10] | Cross-network integration | 0.7 |
| **ASA** | Attention Gating | ASA[10:20] | Flexibility/reconfiguration | **0.9** |
| **ASA** | Salience Weighting | ASA[20:30] | Between-network connectivity | 0.8 |

---

## 6. Output Space: 12D Multi-Layer Representation

### 6.1 Complete Output Specification

```
ECT OUTPUT TENSOR: 12D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_within_efficiency    │ [0, 1] │ Intra-network coupling strength.
    │                          │        │ f01 = σ(0.35 * within_coupling_1s
    │                          │        │       + 0.35 * pattern_binding_1s
    │                          │        │       + 0.30 * mean(PPC.pitch[0:10]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_between_reduction    │ [0, 1] │ Cross-network connectivity loss.
    │                          │        │ f02 = σ(0.35 * cross_network_1s
    │                          │        │       + 0.35 * cross_entropy_1s
    │                          │        │       + 0.30 * mean(ASA.sal[20:30]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_trade_off_ratio      │[0, 10] │ Cost-benefit balance.
    │                          │        │ f03 = f01 / (f02 + ε)
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_flexibility_index    │ [0, 1] │ Reconfiguration capacity.
    │                          │        │ f04 = σ(0.35 * reconfig_100ms
    │                          │        │       + 0.35 * reconfig_speed_125ms
    │                          │        │       + 0.30 * mean(ASA.attn[10:20]))

LAYER M — MATHEMATICAL MODEL OUTPUTS (Expertise Dynamics)
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ training_history         │ [0, 1] │ Specialization accumulation.
    │                          │        │ binding_trend_1s proxy
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ network_state            │ [0, 1] │ Recent architecture state.
    │                          │        │ f01 - f02 (efficiency delta)
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ task_memory              │ [0, 1] │ Demand-driven shaping.
    │                          │        │ EMA of task demand entropy

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ within_binding           │ [0, 1] │ Current within-network efficiency.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ network_isolation        │ [0, 1] │ Current cross-network reduction.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ transfer_limit           │ [0, 1] │ Cross-domain performance.
────┼──────────────────────────┼────────┼────────────────────────────────────
10  │ efficiency_opt           │ [0, 1] │ Within-network speed prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
11  │ flexibility_recovery     │ [0, 1] │ Network reconfiguration capacity.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 12D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Compartmentalization Trade-off Function

```
TradeOff(t) = WithinEfficiency(t) / (BetweenReduction(t) + ε)

Parameters:
    WithinEfficiency = intra-network coupling strength (106 edges, M > NM)
    BetweenReduction = cross-network connectivity loss (192 edges, NM > M)
    Empirical: TradeOff ≈ 0.55 (106/192) — more loss than gain
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Within-Network Efficiency (coefficients sum = 1.0)
f01 = σ(0.35 * within_coupling_mean_1s
       + 0.35 * pattern_binding_mean_1s
       + 0.30 * mean(PPC.pitch_extraction[0:10]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Between-Network Reduction (coefficients sum = 1.0)
f02 = σ(0.35 * cross_network_mean_1s
       + 0.35 * cross_entropy_1s
       + 0.30 * mean(ASA.salience_weighting[20:30]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f03: Trade-off Ratio
f03 = clamp(f01 / (f02 + 1e-6), 0, 10)
# f03 > 1.0: Gain exceeds cost
# f03 < 1.0: Cost exceeds gain

# f04: Flexibility Index (coefficients sum = 1.0)
f04 = σ(0.35 * spectral_change_100ms
       + 0.35 * reconfig_speed_125ms
       + 0.30 * mean(ASA.attention_gating[10:20]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | ECT Function |
|--------|-----------------|----------|---------------|--------------|
| **Within-network (SMA, ACC, TPO)** | N/A | 2 | Direct (MEG) | Fast specialized processing |
| **Between-network connections** | N/A | 2 | Direct (MEG) | Cross-domain integration |

---

## 9. Cross-Unit Pathways

### 9.1 ECT Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ECT INTERACTIONS                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (NDU):                                                         │
│  EDNR.network_reorganization ► ECT (functional trade-off interpretation)  │
│  SLEE.detection_accuracy ────► ECT (behavioral benefit despite trade-off) │
│                                                                             │
│  CROSS-UNIT (NDU → IMU):                                                   │
│  ECT.flexibility_index ──────► IMU (network flexibility for memory)       │
│  ECT.within_efficiency ──────► SPU (processing speed for spectral)        │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  PPC mechanism (30D) ────────► ECT (within-network specialization)        │
│  ASA mechanism (30D) ────────► ECT (cross-network flexibility)            │
│  R³ (~20D) ──────────────────► ECT (direct spectral features)              │
│  H³ (18 tuples) ─────────────► ECT (temporal dynamics)                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Network structure** | Musicians should show compartmentalization | **Confirmed** by Paraskevopoulos |
| **Transfer tasks** | Musicians should show slower cross-domain transfer | **UNTESTED** |
| **Task switching** | Musicians should show switching costs | **UNTESTED** |
| **Creativity** | Musicians may show reduced cross-domain creativity | **UNTESTED** |
| **Broad training** | Cross-training should reduce compartmentalization | **UNTESTED** |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class ECT(BaseModel):
    """Expertise Compartmentalization Trade-off Model.

    Output: 12D per frame.
    Reads: PPC mechanism (30D), ASA mechanism (30D), R³ direct.
    SPECULATIVE: Functional consequences of compartmentalization untested.
    """
    NAME = "ECT"
    UNIT = "NDU"
    TIER = "γ3"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("PPC", "ASA")

    TAU_DECAY = 2.0             # Network state persistence (seconds)
    XTI_WINDOW = 8.0            # Reconfiguration window (seconds)
    WITHIN_EDGES_MUSICIAN = 106
    BETWEEN_EDGES_NONMUSICIAN = 192

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """18 tuples for ECT computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── PPC horizons: within-network efficiency ──
            (25, 3, 0, 2),     # x_l0l5[0], 100ms, value, bidi
            (25, 3, 2, 2),     # x_l0l5[0], 100ms, std, bidi
            (25, 16, 1, 2),    # x_l0l5[0], 1000ms, mean, bidi
            (33, 3, 0, 2),     # x_l4l5[0], 100ms, value, bidi
            (33, 16, 1, 2),    # x_l4l5[0], 1000ms, mean, bidi
            (33, 16, 18, 0),   # x_l4l5[0], 1000ms, trend, fwd
            # ── ASA horizons: cross-network flexibility ──
            (41, 3, 0, 2),     # x_l5l6[0], 100ms, value, bidi
            (41, 3, 2, 2),     # x_l5l6[0], 100ms, std, bidi
            (41, 16, 1, 2),    # x_l5l6[0], 1000ms, mean, bidi
            (41, 16, 20, 2),   # x_l5l6[0], 1000ms, entropy, bidi
            # ── Reconfiguration dynamics ──
            (21, 3, 0, 2),     # spectral_change, 100ms, value, bidi
            (21, 4, 8, 0),     # spectral_change, 125ms, velocity, fwd
            (23, 3, 0, 2),     # pitch_change, 100ms, value, bidi
            (23, 16, 1, 2),    # pitch_change, 1000ms, mean, bidi
            # ── Task demand ──
            (7, 3, 0, 2),      # amplitude, 100ms, value, bidi
            (7, 8, 20, 2),     # amplitude, 500ms, entropy, bidi
            (13, 3, 0, 2),     # brightness, 100ms, value, bidi
            (8, 3, 0, 2),      # loudness, 100ms, value, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute ECT 12D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30), "ASA": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,12) ECT output
        """
        ppc = mechanism_outputs["PPC"]    # (B, T, 30)
        asa = mechanism_outputs["ASA"]    # (B, T, 30)

        # R³ features
        x_l0l5 = r3[..., 25:33]          # (B, T, 8)
        x_l4l5 = r3[..., 33:41]          # (B, T, 8)
        x_l5l6 = r3[..., 41:49]          # (B, T, 8)
        spectral_change = r3[..., 21:22]
        pitch_change = r3[..., 23:24]

        # PPC sub-sections
        ppc_pitch = ppc[..., 0:10]
        ppc_interval = ppc[..., 10:20]
        ppc_contour = ppc[..., 20:30]

        # ASA sub-sections
        asa_scene = asa[..., 0:10]
        asa_attn = asa[..., 10:20]
        asa_salience = asa[..., 20:30]

        # H³ direct features
        within_coupling_mean_1s = h3_direct[(25, 16, 1, 2)].unsqueeze(-1)
        pattern_binding_mean_1s = h3_direct[(33, 16, 1, 2)].unsqueeze(-1)
        binding_trend_1s = h3_direct[(33, 16, 18, 0)].unsqueeze(-1)
        cross_network_mean_1s = h3_direct[(41, 16, 1, 2)].unsqueeze(-1)
        cross_entropy_1s = h3_direct[(41, 16, 20, 2)].unsqueeze(-1)
        reconfig_100ms = h3_direct[(21, 3, 0, 2)].unsqueeze(-1)
        reconfig_speed_125ms = h3_direct[(21, 4, 8, 0)].unsqueeze(-1)
        demand_entropy_500ms = h3_direct[(7, 8, 20, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: Within-Network Efficiency (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.35 * within_coupling_mean_1s
            + 0.35 * pattern_binding_mean_1s
            + 0.30 * ppc_pitch.mean(-1, keepdim=True)
        )

        # f02: Between-Network Reduction (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.35 * cross_network_mean_1s
            + 0.35 * cross_entropy_1s
            + 0.30 * asa_salience.mean(-1, keepdim=True)
        )

        # f03: Trade-off Ratio
        f03 = torch.clamp(f01 / (f02 + 1e-6), 0, 10)

        # f04: Flexibility Index (coefficients sum = 1.0)
        f04 = torch.sigmoid(
            0.35 * reconfig_100ms
            + 0.35 * reconfig_speed_125ms
            + 0.30 * asa_attn.mean(-1, keepdim=True)
        )

        # ═══ LAYER M: Expertise Dynamics ═══
        training_history = binding_trend_1s
        network_state = torch.sigmoid(
            0.50 * f01 + 0.50 * (1 - f02)
        )
        task_memory = demand_entropy_500ms

        # ═══ LAYER P: Present ═══
        within_binding = ppc_pitch.mean(-1, keepdim=True)
        network_isolation = asa_salience.mean(-1, keepdim=True)

        # ═══ LAYER F: Future ═══
        transfer_limit = torch.sigmoid(
            0.50 * f02 + 0.50 * (1 - f04)
        )
        efficiency_opt = torch.sigmoid(
            0.50 * f01 + 0.50 * ppc_interval.mean(-1, keepdim=True)
        )
        flexibility_recovery = torch.sigmoid(
            0.50 * f04 + 0.50 * asa_attn.mean(-1, keepdim=True)
        )

        return torch.cat([
            f01, f02, f03, f04,                                     # E: 4D
            training_history, network_state, task_memory,           # M: 3D
            within_binding, network_isolation,                      # P: 2D
            transfer_limit, efficiency_opt, flexibility_recovery,   # F: 3D
        ], dim=-1)  # (B, T, 12)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 (Paraskevopoulos 2022) | Primary evidence |
| **Effect Sizes** | Network edges: 106 vs 192 | Structural measures |
| **Evidence Modality** | MEG | Network connectivity |
| **Falsification Tests** | 1/5 structural only | Low validity (needs functional tests) |
| **R³ Features Used** | ~20D of 49D | Energy + timbre + change + all interactions |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Within-network specialization |
| **ASA Mechanism** | 30D (3 sub-sections) | Cross-network flexibility |
| **Output Dimensions** | **12D** | 4-layer structure |

**Research Priorities**:
1. **CRITICAL: Functional testing** -- Does compartmentalization limit transfer?
2. Task switching paradigms to assess flexibility
3. Creativity and cross-domain innovation tasks
4. Broad vs narrow training intervention studies
5. Longitudinal tracking of network development

---

## 13. Scientific References

1. **Paraskevopoulos, E. et al. (2022)**. Network compartmentalization in musicians: Within-network > between-network connectivity. MEG study, n=25.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (TIH, SGM, EFC, BND) | PPC (30D) + ASA (30D) mechanisms |
| Within-network | S⁰.L7.crossband[80:104] + HC⁰.BND | R³.x_l0l5[25:33] + PPC.pitch_extraction |
| Between-network | S⁰.X_L5L6[208:216] + HC⁰.SGM | R³.x_l5l6[41:49] + ASA.salience_weighting |
| Adaptation | S⁰.L4.velocity_F[16] + HC⁰.TIH | R³.spectral_change[21] + ASA.attention_gating |
| Optimization | S⁰.L3.coherence[14] + HC⁰.EFC | R³.x_l4l5[33:41] + PPC.interval_analysis |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 37/2304 = 1.61% | 18/2304 = 0.78% |
| Output | 12D | 12D (same) |

### Why PPC + ASA replaces HC⁰ mechanisms

- **BND → PPC.pitch_extraction** [0:10]: Within-network binding efficiency maps to PPC's specialized processing.
- **SGM → ASA.salience_weighting** [20:30]: Between-network isolation maps to ASA's cross-network connectivity.
- **TIH → ASA.attention_gating** [10:20]: Integration scope limitation maps to ASA's flexibility/reconfiguration.
- **EFC → PPC.interval_analysis** [10:20]: Expertise-based optimization maps to PPC's network efficiency.

---

**Model Status**: **SPECULATIVE**
**Output Dimensions**: **12D**
**Evidence Tier**: **γ (Integrative)**
**Confidence**: **50–70%**
**Functional Consequences**: **UNTESTED**
