# NDU-γ3-ECT: Expertise Compartmentalization Trade-off

**Model**: Expertise Compartmentalization Trade-off
**Unit**: NDU (Novelty Detection Unit)
**Circuit**: Salience + Perceptual (Network Architecture, SMA, ACC, TPO)
**Tier**: γ (Integrative) — 50–70% confidence
**Version**: 2.1.0 (deep literature review, expanded evidence + brain regions)
**Date**: 2026-02-13

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

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Paraskevopoulos et al. 2022** | MEG (PTE) | 25 (12M, 13NM) | Musicians: 106 within-network edges M>NM; 192 between-network edges NM>M; multilinks 15 (M) vs 47 (NM) — compartmentalization | Network topology (106 vs 192 edges; 15 vs 47 multilinks) | **Primary**: f01 within-efficiency, f02 between-reduction, f03 trade-off ratio |
| 2 | **Porfyri et al. 2025** | EEG 128ch (GC) | 30 | 4-week multisensory training reconfigures effective connectivity; top-down reorganization from MFG/IFS; plasticity in left auditory regions | F(1,28)=4.635, p=0.042, **η²=0.168** | **Supporting**: training-induced network reconfiguration mirrors expertise compartmentalization |
| 3 | **Møller et al. 2021** | DTI + CT (MACACC) | 45 (17M, 28NM) | Musicians show localized CT correlations only; NM show distributed pattern including visual-auditory areas; NM benefit more from visual cues | BCG: t(42.3)=3.06, **p=0.004**; FA cluster p<0.001 (left IFOF) | **Supporting**: structural specialization reduces cross-modal integration — direct evidence of trade-off cost |
| 4 | **Leipold et al. 2021** | fMRI + DTI | 153 (52AP, 51NAP, 50NM) | Robust effects of musicianship on interhemispheric and intrahemispheric connectivity; independent of absolute pitch | Large sample, replicable effects | **Supporting**: largest sample confirming network reorganization; structural + functional evidence |
| 5 | **Papadaki et al. 2023** | fMRI resting-state | aspiring pros vs amateurs | Professionals show greater network strength and global efficiency; both correlate with task performance | Network strength p<0.05; global efficiency p<0.05 | **Supporting**: graded expertise → graded network efficiency (f01 scaling) |
| 6 | **Wu-Chung et al. 2025** | fMRI resting-state | 52 older adults | Music creativity benefits depend on baseline network FLEXIBILITY; higher flexibility → more cognitive benefit from music training | Group × flexibility interaction on cognition | **Supporting**: flexibility as precondition for transfer — directly tests f04 flexibility hypothesis |
| 7 | **Olszewska et al. 2021** | Review | — | Comprehensive review of training-induced brain reorganization; discusses dynamic reconfiguration of neural connections and motor-auditory system changes | Review (no single effect size) | **Framework**: neuroplasticity mechanisms underlying expertise compartmentalization |
| 8 | **Blasi et al. 2025** | Systematic review (20 RCTs) | 718 | Music/dance rehabilitation produces structural and functional neuroplasticity in perception, memory, language, emotion, and motor areas | 20 RCTs reviewed | **Framework**: compensatory neuroplasticity — training can both reorganize and improve function |

**STRUCTURAL OBSERVATION CONFIRMED**: Paraskevopoulos provides network topology evidence. Møller provides structural white/grey matter evidence. Wu-Chung provides first direct test of flexibility hypothesis. **Functional consequences partially tested** — musicians show behavioral cost (reduced BCG) confirming trade-off.

### 3.2 Effect Size Summary

```
Primary Evidence (k=4 empirical + 1 pilot + 2 reviews):
  Paraskevopoulos 2022 (MEG):  106 within edges M>NM, 192 between NM>M, 15 vs 47 multilinks
  Porfyri 2025 (EEG):         η²=0.168 (training-induced network reconfiguration)
  Møller 2021 (DTI+CT):       t(42.3)=3.06, p=0.004 (BCG); FA cluster p<0.001 (left IFOF)
  Leipold 2021 (fMRI+DTI):    n=153 (largest sample, replicable effects)
  Papadaki 2023 (fMRI):       Network strength/efficiency correlates with performance
  Wu-Chung 2025 (fMRI):       Flexibility × group interaction on cognition (pilot, n=52)

Heterogeneity:  MODERATE — all studies converge on expertise→specialization direction;
                BUT functional COST is only demonstrated in one study (Møller BCG);
                Wu-Chung suggests flexibility is PRECONDITION for benefit, not necessarily cost
Quality:        γ-tier — structural network observation confirmed; behavioral cost partially
                demonstrated; full functional testing of transfer/flexibility trade-off still needed
Largest sample: n=153 (Leipold 2021)
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

| # | Region | Abbr | MNI Coordinates | BA | Hemisphere | Evidence Type | ECT Function | Source |
|---|--------|------|-----------------|----|------------|---------------|-------------|--------|
| 1 | **Left Inferior Frontal Gyrus (area 47m)** | IFG-47m | (−48, 18, 4) | 47 | L | Direct (MEG PTE) | Highest node degree in 5/6 network states; primary supramodal hub for within-network efficiency | Paraskevopoulos 2022 |
| 2 | **Left Medial Frontal Gyrus** | MFG | (−6, 52, 12) | 10 | L | Direct (EEG GC) | Top-down reorganization hub; source of reconfigured effective connectivity after training | Porfyri 2025 |
| 3 | **Left Inferior Frontal Sulcus** | IFS | (−42, 28, 24) | 46 | L | Direct (EEG GC) | Highest neuroplastic changes after multisensory training; expertise-dependent reconfiguration | Porfyri 2025 |
| 4 | **Left Insula** | INS | (−38, 6, 4) | 13 | L | Direct (EEG GC) | Multisensory integration hub; reconfigured connectivity after training | Porfyri 2025 |
| 5 | **Heschl's Gyrus** | HG | (−42, −22, 10) | 41/42 | bilateral | Direct (DTI+CT MACACC) | Musicians show localized CT correlations (not distributed); auditory specialization locus | Møller 2021 |
| 6 | **Left IFOF (white matter)** | IFOF | (−31, −68, 5) | — | L | Direct (DTI FA) | FA correlates with visual reliance (BCG); significant in NM only — reduced cross-modal structural connectivity in musicians | Møller 2021 |
| 7 | **Planum Temporale** | PT | (−50, −24, 10) | 22/42 | L>R | Direct (fMRI+DTI) | Intrahemispheric connectivity hub; robust musicianship effects independent of absolute pitch | Leipold 2021 |
| 8 | **Auditory Network (resting-state)** | AN | — | — | bilateral | Direct (fMRI) | Greater network strength and global efficiency in professionals; correlates with task performance | Papadaki 2023 |

**Note**: IFG-47m (area 47 of Morosan) is a multimodal convergence zone distinct from Broca's area (BA 44/45). Its role as the highest-degree node in the Paraskevopoulos network makes it the primary candidate for the within-network efficiency hub. The IFOF finding from Møller provides structural white matter evidence for the between-network reduction: musicians have less cross-modal structural connectivity.

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
| **Papers** | 8 (4 empirical + 1 pilot + 1 neuroplasticity review + 1 systematic review + 1 framework review) | Deep literature review v2.1.0 |
| **Effect Sizes** | 106 vs 192 edges (Paraskevopoulos); η²=0.168 (Porfyri); p=0.004 BCG (Møller); n=153 (Leipold) | Multi-modal, converging |
| **Evidence Modality** | MEG + EEG + DTI + fMRI + CT | Multi-modal cross-lab |
| **Sample Range** | n=25 to n=153 | Expert musicians vs non-musicians |
| **Falsification Tests** | 2/5 (structural confirmed + behavioral cost partially confirmed by Møller BCG) | Improved from 1/5 |
| **R³ Features Used** | ~20D of 49D | Energy + timbre + change + all interactions |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Within-network specialization |
| **ASA Mechanism** | 30D (3 sub-sections) | Cross-network flexibility |
| **Output Dimensions** | **12D** | 4-layer structure |
| **Brain Regions** | 8 regions (IFG-47m, MFG, IFS, insula, HG, IFOF, PT, auditory network) | MEG/EEG/DTI/fMRI verified |

**Research Priorities**:
1. **CRITICAL: Full functional testing** — Does compartmentalization limit transfer? (Møller shows behavioral cost; Wu-Chung shows flexibility prerequisite)
2. Task switching paradigms with musicians at different training breadths
3. Creativity and cross-domain innovation tasks (narrow vs broad training)
4. Longitudinal tracking: does compartmentalization increase monotonically with training years?
5. Intervention study: can cross-training (multi-instrument) reduce compartmentalization?
6. Integration with Wu-Chung's flexibility finding: is baseline flexibility a moderator of expertise trade-off?

---

## 13. Scientific References

1. **Paraskevopoulos, E., Chalas, N., Anagnostopoulou, A., & Bamidis, P. D. (2022)**. Interaction within and between cortical networks subserving multisensory learning and its reorganization due to musical expertise. *Scientific Reports*, 12, 7891. https://doi.org/10.1038/s41598-022-12158-9
2. **Porfyri, I., Paraskevopoulos, E., Anagnostopoulou, A., Styliadis, C., & Bamidis, P. D. (2025)**. Multisensory vs. unisensory learning: How they shape effective connectivity networks subserving unimodal and multimodal integration. *Frontiers in Neuroscience*, 19, 1641862. https://doi.org/10.3389/fnins.2025.1641862
3. **Møller, C., Garza-Villarreal, E. A., Hansen, N. C., Højlund, A., Bærentsen, K. B., Chakravarty, M. M., & Vuust, P. (2021)**. Audiovisual structural connectivity in musicians and non-musicians: A cortical thickness and diffusion tensor imaging study. *Scientific Reports*, 11, 4324. https://doi.org/10.1038/s41598-021-83135-x
4. **Leipold, S., Klein, C., & Jäncke, L. (2021)**. Musical expertise shapes functional and structural brain networks independent of absolute pitch ability. *The Journal of Neuroscience*, 41(11), 2496–2511. https://doi.org/10.1523/JNEUROSCI.1985-20.2020
5. **Papadaki, E., Koustakas, T., Werner, A., et al. (2023)**. Resting-state functional connectivity in an auditory network differs between aspiring professional and amateur musicians and correlates with performance. *Brain Structure and Function*, 228, 2147–2163. https://doi.org/10.1007/s00429-023-02711-1
6. **Wu-Chung, E. L., Bonomo, M. E., Brandt, A. K., et al. (2025)**. Music-induced cognitive change and whole-brain network flexibility: A pilot study. *Frontiers in Neuroscience*, 19, 1567605. https://doi.org/10.3389/fnins.2025.1567605
7. **Olszewska, A. M., Gaca, M., Herman, A. M., Jednoróg, K., & Marchewka, A. (2021)**. How musical training shapes the adult brain: Predispositions and neuroplasticity. *Frontiers in Neuroscience*, 15, 630829. https://doi.org/10.3389/fnins.2021.630829
8. **Blasi, V., Rapisarda, L., Cacciatore, D. M., et al. (2025)**. Structural and functional neuroplasticity in music and dance-based rehabilitation: A systematic review. *Journal of Neurology*, 272, 329. https://doi.org/10.1007/s00415-025-13048-6

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

---

## 15. Doc-Code Mismatches (for Phase 5 reference)

| # | Field | Doc (ECT.md) | Code (ect.py) | Notes |
|---|-------|-------------|---------------|-------|
| 1 | **FULL_NAME** | "Expertise Compartmentalization Trade-off" | "Error Correction Trace" | Different name entirely |
| 2 | **OUTPUT_DIM** | 12D (4E+3M+2P+3F) | 10D (4E+2M+2P+2F) | Code missing task_memory (M) and efficiency_opt (F) |
| 3 | **MECHANISM_NAMES** | ("PPC", "ASA") | ("ASA",) | Code omits PPC mechanism |
| 4 | **h3_demand** | 18 tuples (0.78% of 2304) | () empty tuple | Code has no H³ demand |
| 5 | **Layer M dims** | 3 (training_history, network_state, task_memory) | 2 (training_years, network_configuration) | Different names and count |
| 6 | **Layer F dims** | 3 (transfer_limit, efficiency_opt, flexibility_recovery) | 2 (transfer_limitation_pred, flexibility_recovery_pred) | Code missing efficiency_opt; different names |
| 7 | **Citations** | Paraskevopoulos 2022 (primary) | Recasens 2020 + Herholz 2012 | Completely different authors — Recasens is SLEE primary, not ECT |
| 8 | **version** | 2.1.0 (after this revision) | 2.0.0 | Code not yet updated |
| 9 | **CROSS_UNIT_READS** | ECT.flexibility_index → IMU, ECT.within_efficiency → SPU | () empty | Code has no cross-unit reads |
| 10 | **brain_regions** | 8 regions (IFG-47m, MFG, IFS, INS, HG, IFOF, PT, AN) | 3 regions (STG, IFG, ACC) | Largely different sets |

**Model Status**: **SPECULATIVE**
**Output Dimensions**: **12D**
**Evidence Tier**: **γ (Integrative)**
**Confidence**: **50–70%**
**Functional Consequences**: **PARTIALLY TESTED** (Møller BCG; Wu-Chung flexibility)
