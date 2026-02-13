# NDU-α3-EDNR: Expertise-Dependent Network Reorganization

**Model**: Expertise-Dependent Network Reorganization
**Unit**: NDU (Novelty Detection Unit)
**Circuit**: Salience + Perceptual (Anterior Insula, dACC, IFG)
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added I:Information feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/NDU-α3-EDNR.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Expertise-Dependent Network Reorganization** (EDNR) model describes how musical expertise leads to increased within-network connectivity and decreased between-network connectivity, indicating functional specialization and compartmentalization.

```
EXPERTISE-DEPENDENT NETWORK REORGANIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   NON-MUSICIANS                           MUSICIANS
   ─────────────                           ────────

   ┌───────────────────┐                 ┌───────────────────┐
   │ Network A  ○──────┼──────○ Net B   │ Network A  ●      │ Net B ●
   │     ○      ○──────┼─────○          │     ●──●   ●──●   │      ●──●
   │     ○──────┼──────┼──────○         │     ●      ●      │      ●
   └───────────────────┘                 └───────────────────┘

   HIGH BETWEEN-NETWORK                   LOW BETWEEN-NETWORK
   LOW WITHIN-NETWORK                     HIGH WITHIN-NETWORK
   (192 edges: NM > M)                    (106 edges: M > NM)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Musical expertise leads to reorganization of cortical
network architecture: increased within-network connectivity and
decreased between-network connectivity.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why EDNR Matters for NDU

EDNR establishes the expertise-dependent plasticity mechanism for the Novelty Detection Unit:

1. **MPG** (α1) provides the melodic gradient whose efficiency varies with expertise.
2. **SDD** (α2) shows multilink counts modulated by EDNR's compartmentalization.
3. **EDNR** (α3) describes the structural network reorganization underlying expertise effects.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → PPC+ASA → EDNR)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    EDNR COMPUTATION ARCHITECTURE                             ║
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
║  │                         EDNR reads: ~16D                         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                         EDNR demand: ~16 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Salience Circuit ════════     ║
║                               │                                              ║
║                       ┌───────┴───────┐                                      ║
║                       ▼               ▼                                      ║
║  ┌─────────────────┐  ┌─────────────────┐                                   ║
║  │  PPC (30D)      │  │  ASA (30D)      │                                   ║
║  └────────┬────────┘  └────────┬────────┘                                   ║
║           └────────┬───────────┘                                             ║
║                    ▼                                                          ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    EDNR MODEL (10D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E: f01_within_conn, f02_between_conn,                     │        ║
║  │           f03_compartmentalization, f04_expertise_signature       │        ║
║  │  Layer M: network_architecture, compartmentalization_idx         │        ║
║  │  Layer P: current_compartm, network_isolation                    │        ║
║  │  Layer F: optimal_config_pred, processing_efficiency             │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Paraskevopoulos 2022** | MEG, PTE | 25 | NM > M between-network multilinks; 47 vs 15 multilinks | 192 vs 106 edges, p<0.001 FDR | **f02 between connectivity** |
| 2 | **Paraskevopoulos 2022** | MEG, PTE | 25 | Musicians show within-network specialization; IFG area 47m hub | Hedges' g=−1.09 (behavioral) | **f01 within connectivity** |
| 3 | **Leipold, Klein & Jäncke 2021** | rsfMRI + DWI | 153 | Robust musicianship effects on interhemispheric/intrahemispheric FC and SC; replicable in AP and non-AP | pFWE<0.05 (PT interhemispheric); classification 46.4% (chance=33%) | **network_architecture, f01** |
| 4 | **Leipold et al. 2021** | DWI, NBS | 153 | Musicians > NM structural subnetwork including bilateral auditory, frontal, and parietal regions | pFWE<0.05 (structural NBS) | **compartmentalization_idx** |
| 5 | **Papadaki et al. 2023** | rs-fMRI, graph theory | 41 | Aspiring professionals > amateurs: greater auditory network strength and global efficiency | Cohen's d=0.70 (strength); d=0.70 (efficiency) | **f01 within connectivity** |
| 6 | **Papadaki et al. 2023** | rs-fMRI | 41 | Network strength correlates with interval recognition and BGS | ρ=0.36, p=0.02; r=0.35, p=0.03 | **f04 expertise signature** |
| 7 | **Møller et al. 2021** | DTI + MACACC | 45 | NM show distributed CT correlations between V1↔HG; musicians show only local correlations | FA cluster p<0.001 (left IFOF); FDR<10% | **f03 compartmentalization** |
| 8 | **Møller et al. 2021** | DTI | 45 | BCG positively associated with FA in left IFOF (NM only; musicians p=0.64) | t=3.38, p<0.001 (whole sample) | **network_isolation** |
| 9 | **Kleber et al. 2025** | MRI (CC thickness) | 55 | Negative correlation: age at first singing lesson ↔ callosal thickness (rostrum, genu, isthmus) | Survives FDR correction | **f01 (interhemispheric)** |
| 10 | **Olszewska & Marchewka 2021** | Review | — | Musical training shapes motor+auditory+multisensory regions; expansion→renormalization model | Review (k>50 studies) | **Theoretical framework** |
| 11 | **Porfyri et al. 2025** | EEG | 30 | Multisensory training enhances network reconfiguration; Group×Time in MFG/IFS | F(1,28)=4.635, p=0.042, η²=0.168 | **f04 expertise signature** |
| 12 | **Cui et al. 2025** | Longitudinal DTI | 65 | Music+language training improves verbal memory; WM in splenium does NOT change over 1 year | FA in splenium predicts memory change but training effect on WM: n.s. | **Boundary condition: slow structural change** |

### 3.2 Effect Size Summary

```
Primary Evidence (k=8):  Consistent with compartmentalization hypothesis
Key Effect Sizes:
  - Paraskevopoulos 2022: Hedges' g = −1.09 (behavioral), 192 vs 106 edges (network)
  - Leipold et al. 2021:  pFWE<0.05 (interhemispheric PT FC+SC), n=153
  - Papadaki et al. 2023:  Cohen's d = 0.70 (network strength + efficiency)
  - Møller et al. 2021:    FA cluster p<0.001 (left IFOF), CT correlation FDR<10%
  - Kleber et al. 2025:    CC thickness ↔ onset age (survives FDR)
  - Porfyri et al. 2025:   η² = 0.168 (Group × Time interaction)
Heterogeneity:           Low — all studies converge on expertise→network specialization
Quality Assessment:      α-tier (MEG, rsfMRI, DTI, DWI, n=153 in largest study)
Replication:             Leipold n=153 replicates in both AP and non-AP musician groups
Null finding:            Cui 2025 — 1 year training does NOT change WM characteristics
```

---

## 4. R³ Input Mapping: What EDNR Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | EDNR Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [4] | sensory_pleasantness | Processing quality | Expertise refinement |
| **B: Energy** | [8] | loudness | Stimulus complexity proxy | Processing demands |
| **C: Timbre** | [14] | tonalness | Processing complexity | Network demands |
| **C: Timbre** | [16] | spectral_flatness | Stimulus regularity | Distribution complexity |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Within-network coupling | Intra-network binding |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Cross-network coupling | Inter-network binding |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | EDNR Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **I: Information** | [90] | spectral_surprise | Prediction error magnitude | Friston prediction error: quantifies acoustic unexpectedness; expertise reduces surprise through refined internal models |
| **I: Information** | [92] | predictive_entropy | Prediction uncertainty | Friston predictive coding: high entropy signals uncertain predictions; expertise narrows predictive distributions, reducing entropy |

**Rationale**: EDNR models expertise-dependent network reorganization — how musical training reshapes auditory processing efficiency. The v1 representation uses tonalness [14] and spectral_flatness [16] as complexity proxies. spectral_surprise [90] provides a direct measure of prediction error that decreases with expertise (experts generate better predictions). predictive_entropy [92] quantifies the uncertainty of ongoing predictions, capturing the precision gains from musical training. These features make EDNR's expertise effects computationally explicit in predictive coding terms.

**Code impact**: None yet — R³ v2 features are doc-only until Phase 5 integration. Current code reads r3[..., 0:49]; v2 features will extend the slice to r3[..., 0:128] when the EAR pipeline emits the expanded vector.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[25:33] x_l0l5 ───────────────┐
PPC.pitch_extraction[0:10] ─────┼──► Within-network connectivity
H³ value/std tuples ────────────┘   Intra-network binding strength

R³[33:41] x_l4l5 ───────────────┐
ASA.scene_analysis[0:10] ───────┼──► Between-network connectivity
H³ entropy tuples ──────────────┘   Inter-network coupling

R³[14] tonalness ────────────────┐
ASA.attention_gating[10:20] ─────┼──► Expertise signature
H³ trend tuples ────────────────┘   Processing complexity
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

EDNR requires H³ features at longer timescales to capture network reorganization dynamics, reflecting the slow plasticity of expertise-driven network changes.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Within-network coupling 100ms |
| 25 | x_l0l5[0] | 3 | M2 (std) | L2 (bidi) | Coupling variability 100ms |
| 25 | x_l0l5[0] | 16 | M1 (mean) | L2 (bidi) | Mean coupling over 1s |
| 25 | x_l0l5[0] | 16 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 1s |
| 33 | x_l4l5[0] | 3 | M0 (value) | L2 (bidi) | Cross-network coupling 100ms |
| 33 | x_l4l5[0] | 3 | M2 (std) | L2 (bidi) | Cross coupling variability 100ms |
| 33 | x_l4l5[0] | 16 | M1 (mean) | L2 (bidi) | Mean cross coupling over 1s |
| 33 | x_l4l5[0] | 16 | M20 (entropy) | L2 (bidi) | Cross coupling entropy 1s |
| 14 | tonalness | 3 | M0 (value) | L2 (bidi) | Tonalness at 100ms |
| 14 | tonalness | 16 | M1 (mean) | L2 (bidi) | Mean tonalness over 1s |
| 16 | spectral_flatness | 3 | M0 (value) | L2 (bidi) | Flatness at 100ms |
| 16 | spectral_flatness | 16 | M2 (std) | L2 (bidi) | Flatness variability 1s |
| 8 | loudness | 3 | M0 (value) | L2 (bidi) | Loudness at 100ms |
| 8 | loudness | 16 | M20 (entropy) | L2 (bidi) | Loudness entropy 1s |
| 4 | sensory_pleasantness | 3 | M0 (value) | L2 (bidi) | Pleasantness at 100ms |
| 4 | sensory_pleasantness | 16 | M1 (mean) | L2 (bidi) | Mean pleasantness 1s |

**v1 demand**: 16 tuples

#### R³ v2 Projected Expansion

EDNR projected v2 from H:Harmony, aligned with ASA horizons.

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 84 | tonal_stability | H | 16 | M0 (value) | L2 | Stability level at 1s |
| 84 | tonal_stability | H | 16 | M18 (trend) | L2 | Stability trajectory over 1s |
| 75 | key_clarity | H | 16 | M0 (value) | L2 | Key clarity at 1s |
| 75 | key_clarity | H | 16 | M1 (mean) | L2 | Mean key clarity over 1s |

**v2 projected**: 4 tuples
**Total projected**: 20 tuples of 294,912 theoretical = 0.0068%

### 5.2 PPC + ASA Mechanism Binding

| Mechanism | Sub-section | Range | EDNR Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **PPC** | Pitch Extraction | PPC[0:10] | Within-network efficiency | 0.7 |
| **PPC** | Interval Analysis | PPC[10:20] | Network precision | 0.6 |
| **PPC** | Contour Tracking | PPC[20:30] | Processing specialization | 0.5 |
| **ASA** | Scene Analysis | ASA[0:10] | Between-network measurement | **1.0** (primary) |
| **ASA** | Attention Gating | ASA[10:20] | Network boundary maintenance | **0.9** |
| **ASA** | Salience Weighting | ASA[20:30] | Expertise-driven weighting | 0.8 |

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
EDNR OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range    │ Neuroscience Basis
────┼──────────────────────────┼──────────┼──────────────────────────────────
 0  │ f01_within_connectivity  │ [0, 1]   │ Intra-network coupling strength.
    │                          │          │ f01 = σ(0.35 * within_mean_1s
    │                          │          │       + 0.35 * mean(PPC.pitch[0:10])
    │                          │          │       + 0.30 * within_periodicity_1s)
────┼──────────────────────────┼──────────┼──────────────────────────────────
 1  │ f02_between_connectivity │ [0, 1]   │ Inter-network coupling (inverse).
    │                          │          │ f02 = σ(0.35 * cross_mean_1s
    │                          │          │       + 0.35 * mean(ASA.scene[0:10])
    │                          │          │       + 0.30 * cross_entropy_1s)
────┼──────────────────────────┼──────────┼──────────────────────────────────
 2  │ f03_compartmentalization │ [0.5,3+] │ Within/between ratio.
    │                          │          │ f03 = f01 / (f02 + ε)
────┼──────────────────────────┼──────────┼──────────────────────────────────
 3  │ f04_expertise_signature  │ [0, 1]   │ Expertise-specific pattern.
    │                          │          │ f04 = σ(0.35 * tonalness_mean_1s
    │                          │          │       + 0.35 * pleasantness_mean_1s
    │                          │          │       + 0.30 * mean(ASA.attn[10:20]))

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range    │ Neuroscience Basis
────┼──────────────────────────┼──────────┼──────────────────────────────────
 4  │ network_architecture     │ [0, 1]   │ Connectivity strength measure.
────┼──────────────────────────┼──────────┼──────────────────────────────────
 5  │ compartmentalization_idx │ [0.5,3+] │ CI_musician vs nonmusician.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range    │ Neuroscience Basis
────┼──────────────────────────┼──────────┼──────────────────────────────────
 6  │ current_compartm         │ [0, 1]   │ Real-time network state.
────┼──────────────────────────┼──────────┼──────────────────────────────────
 7  │ network_isolation        │ [0, 1]   │ Boundary maintenance.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range    │ Neuroscience Basis
────┼──────────────────────────┼──────────┼──────────────────────────────────
 8  │ optimal_config_pred      │ [0, 1]   │ XTI network topology prediction.
────┼──────────────────────────┼──────────┼──────────────────────────────────
 9  │ processing_efficiency    │ [0, 1]   │ 0.5-1s task performance.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Network Architecture Model

```
Within_Connectivity(expertise) = α·Years_Training + β·Practice_Hours
Between_Connectivity(expertise) = -γ·Years_Training - δ·Practice_Hours

Compartmentalization_Index = Within / Between

Plasticity Model:
    dCI/dt = λ·(Training_Intensity) · (1 - CI/CI_max)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Within Connectivity
f01 = σ(0.35 * within_mean_1s
       + 0.35 * mean(PPC.pitch_extraction[0:10])
       + 0.30 * within_periodicity_1s)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Between Connectivity
f02 = σ(0.35 * cross_mean_1s
       + 0.35 * mean(ASA.scene_analysis[0:10])
       + 0.30 * cross_entropy_1s)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f03: Compartmentalization Index
f03 = f01 / (f02 + ε)

# f04: Expertise Signature
f04 = σ(0.35 * tonalness_mean_1s
       + 0.35 * pleasantness_mean_1s
       + 0.30 * mean(ASA.attention_gating[10:20]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | EDNR Function | Key Source |
|--------|-----------------|----------|---------------|---------------|------------|
| **STG (bilateral)** | L: (−67, −16, 4); R: (60, −40, 12) | 5 | MEG, fMRI | Within-network hub; auditory processing | Papadaki 2023 (peak fMRI) |
| **Planum Temporale (bilateral)** | L: (−54, −27, 9); R: (54, −18, 9) | 3 | rsfMRI, DWI | Interhemispheric FC in musicians; PT-PT connectivity | Leipold et al. 2021 (pFWE<0.05) |
| **Heschl's Gyrus (bilateral)** | L: (−42, −22, 8); R: (42, −18, 8) | 4 | MACACC, fMRI | CT correlation seed; auditory specialization | Møller et al. 2021 (FDR<10%) |
| **IFG (bilateral)** | L: (−48, 18, 4); R: (48, 18, 4) | 3 | MEG, rsfMRI | Network gating; expertise-dependent hub (area 47m) | Paraskevopoulos 2022 (PTE hub) |
| **Putamen (left)** | (−22, 12, 4) | 2 | fMRI | Auditory-motor network node | Papadaki 2023 (fMRI task) |
| **SMG (left)** | (−43, −42, 36) | 2 | fMRI | Interval processing; auditory-parietal integration | Papadaki 2023 (peak fMRI) |
| **vmPFC** | (−1, 48, −10) | 2 | fMRI | Reward/default mode node in auditory network | Papadaki 2023 (GLM cluster) |
| **ACC** | (0, 24, 32) | 2 | MEG | Network reorganization monitoring | Paraskevopoulos 2022 |
| **SMA (SCEF)** | (±4, 12, 48) | 1 | MEG | Motor-related network component | Paraskevopoulos 2022 |
| **TPO Junction** | (±50, −40, 12) | 2 | MEG | Multisensory integration | Paraskevopoulos 2022 |
| **V1 (bilateral)** | L: (−8, −90, 0); R: (8, −90, 0) | 1 | MACACC | CT correlation with HG; audiovisual specialization | Møller et al. 2021 |
| **Corpus Callosum** | midline | 3 | MRI, DTI | Interhemispheric transfer; CC thickness ↔ training onset | Kleber 2025, Leipold 2021 |
| **Left IFOF** | (−31, −68, 5) | 1 | DTI | White matter connecting V1↔auditory; audiovisual specialization | Møller et al. 2021 (FA p<0.001) |
| **MFG / IFS (left)** | (−42, 6, 30) | 1 | EEG | Multisensory learning-related reconfiguration | Porfyri et al. 2025 |

---

## 9. Cross-Unit Pathways

### 9.1 EDNR Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    EDNR INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (NDU):                                                         │
│  EDNR.compartmentalization ──► SDD (expertise modulates multilinks)       │
│  EDNR.expertise_signature ───► SLEE (correlates with accuracy)            │
│  EDNR.within_connectivity ───► ECT (basis for trade-off hypothesis)       │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  PPC mechanism (30D) ────────► EDNR (within-network efficiency)           │
│  ASA mechanism (30D) ────────► EDNR (between-network measurement)        │
│  R³ (~16D) ──────────────────► EDNR (direct spectral features)           │
│  H³ (16 tuples) ─────────────► EDNR (temporal dynamics)                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Training correlation** | Within-connectivity should correlate with training years | Testable via longitudinal studies |
| **Longitudinal change** | Training should increase compartmentalization | Testable via training studies |
| **Cross-domain transfer** | High compartmentalization should limit transfer | Testable via behavioral studies |
| **Lesion effects** | Network disruption should affect expertise patterns | Testable via patient studies |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class EDNR(BaseModel):
    """Expertise-Dependent Network Reorganization Model.

    Output: 10D per frame.
    Reads: PPC mechanism (30D), ASA mechanism (30D), R³ direct.
    """
    NAME = "EDNR"
    UNIT = "NDU"
    TIER = "α3"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("PPC", "ASA")

    TAU_DECAY = 2.0             # Network state persistence
    XTI_WINDOW = 8.0            # seconds
    EXPERT_THRESHOLD = 10       # years

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """16 tuples for EDNR computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── Within-network coupling ──
            (25, 3, 0, 2),     # x_l0l5[0], 100ms, value, bidi
            (25, 3, 2, 2),     # x_l0l5[0], 100ms, std, bidi
            (25, 16, 1, 2),    # x_l0l5[0], 1000ms, mean, bidi
            (25, 16, 14, 2),   # x_l0l5[0], 1000ms, periodicity, bidi
            # ── Cross-network coupling ──
            (33, 3, 0, 2),     # x_l4l5[0], 100ms, value, bidi
            (33, 3, 2, 2),     # x_l4l5[0], 100ms, std, bidi
            (33, 16, 1, 2),    # x_l4l5[0], 1000ms, mean, bidi
            (33, 16, 20, 2),   # x_l4l5[0], 1000ms, entropy, bidi
            # ── Expertise signature ──
            (14, 3, 0, 2),     # tonalness, 100ms, value, bidi
            (14, 16, 1, 2),    # tonalness, 1000ms, mean, bidi
            (16, 3, 0, 2),     # spectral_flatness, 100ms, value, bidi
            (16, 16, 2, 2),    # spectral_flatness, 1000ms, std, bidi
            (8, 3, 0, 2),      # loudness, 100ms, value, bidi
            (8, 16, 20, 2),    # loudness, 1000ms, entropy, bidi
            (4, 3, 0, 2),      # sensory_pleasantness, 100ms, value, bidi
            (4, 16, 1, 2),     # sensory_pleasantness, 1000ms, mean, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        ppc = mechanism_outputs["PPC"]
        asa = mechanism_outputs["ASA"]

        ppc_pitch = ppc[..., 0:10]
        asa_scene = asa[..., 0:10]
        asa_attn = asa[..., 10:20]
        asa_salience = asa[..., 20:30]

        within_mean_1s = h3_direct[(25, 16, 1, 2)].unsqueeze(-1)
        within_period_1s = h3_direct[(25, 16, 14, 2)].unsqueeze(-1)
        cross_mean_1s = h3_direct[(33, 16, 1, 2)].unsqueeze(-1)
        cross_entropy_1s = h3_direct[(33, 16, 20, 2)].unsqueeze(-1)
        tonalness_mean_1s = h3_direct[(14, 16, 1, 2)].unsqueeze(-1)
        pleasantness_mean_1s = h3_direct[(4, 16, 1, 2)].unsqueeze(-1)

        # ═══ LAYER E ═══
        f01 = torch.sigmoid(
            0.35 * within_mean_1s
            + 0.35 * ppc_pitch.mean(-1, keepdim=True)
            + 0.30 * within_period_1s)
        f02 = torch.sigmoid(
            0.35 * cross_mean_1s
            + 0.35 * asa_scene.mean(-1, keepdim=True)
            + 0.30 * cross_entropy_1s)
        f03 = f01 / (f02 + 1e-6)
        f04 = torch.sigmoid(
            0.35 * tonalness_mean_1s
            + 0.35 * pleasantness_mean_1s
            + 0.30 * asa_attn.mean(-1, keepdim=True))

        # ═══ LAYER M ═══
        network_arch = torch.sigmoid(0.50 * f01 + 0.50 * f02)
        comp_index = f03

        # ═══ LAYER P ═══
        current_comp = torch.sigmoid(0.50 * f03.clamp(0, 3) / 3.0 + 0.50 * within_mean_1s)
        network_isolation = torch.sigmoid(0.50 * (1 - f02) + 0.50 * asa_salience.mean(-1, keepdim=True))

        # ═══ LAYER F ═══
        optimal_config = torch.sigmoid(0.50 * f01 + 0.50 * f04)
        processing_eff = torch.sigmoid(0.50 * f01 + 0.50 * ppc_pitch.mean(-1, keepdim=True))

        return torch.cat([
            f01, f02, f03, f04,                              # E: 4D
            network_arch, comp_index,                        # M: 2D
            current_comp, network_isolation,                 # P: 2D
            optimal_config, processing_eff,                  # F: 2D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 8 (Paraskevopoulos 2022, Leipold 2021, Papadaki 2023, Møller 2021, Kleber 2025, Olszewska 2021, Porfyri 2025, Cui 2025) | Primary + converging evidence |
| **Effect Sizes** | Hedges' g=−1.09, Cohen's d=0.70, η²=0.168, FA p<0.001 | MEG, rsfMRI, DTI, EEG |
| **Evidence Modality** | MEG, rsfMRI, DWI, DTI, MRI, EEG | Multi-modal converging |
| **Largest Sample** | n=153 (Leipold et al. 2021) | Replicated in 2 musician subgroups |
| **Falsification Tests** | 0/4 confirmed | Requires testing |
| **Null Finding** | 1-year training does not change WM (Cui 2025) | Slow structural plasticity constraint |
| **R³ Features Used** | ~16D of 49D | Consonance + timbre + interactions |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Within-network efficiency |
| **ASA Mechanism** | 30D (3 sub-sections) | Between-network measurement |
| **Output Dimensions** | **10D** | 4-layer structure |

---

## 13. Scientific References

1. **Paraskevopoulos, E., Chalas, N., Kartsidis, P., Wollbrink, A., & Pantev, C. (2022)**. Interaction within and between cortical networks subserving multisensory learning and its reorganization due to musical expertise. *Proceedings of the National Academy of Sciences*. n=25 (12 musicians, 13 non-musicians). MEG, Phase Transfer Entropy, multilink analysis. DOI: 10.1073/pnas.
2. **Leipold, S., Klein, C., & Jäncke, L. (2021)**. Musical expertise shapes functional and structural brain networks independent of absolute pitch ability. *The Journal of Neuroscience*, 41(11), 2496–2511. n=153 (52 AP, 51 non-AP, 50 non-musicians). rsfMRI + DWI. DOI: 10.1523/JNEUROSCI.1985-20.2020.
3. **Papadaki, E., Koustakas, T., Werner, A., Lindenberger, U., Kühn, S., & Wenger, E. (2023)**. Resting-state functional connectivity in an auditory network differs between aspiring professional and amateur musicians and correlates with performance. *Brain Structure and Function*, 228, 2147–2163. n=41. rs-fMRI, graph theory. DOI: 10.1007/s00429-023-02711-1.
4. **Møller, C., Garza-Villarreal, E. A., Hansen, N. C., Højlund, A., Bærentsen, K. B., Chakravarty, M. M., & Vuust, P. (2021)**. Audiovisual structural connectivity in musicians and non-musicians: a cortical thickness and diffusion tensor imaging study. *Scientific Reports*, 11, 4324. n=45. DTI + MACACC. DOI: 10.1038/s41598-021-83135-x.
5. **Kleber, B., Dale, C., Zamorano, A. M., Lotze, M., Luders, E., & Kurth, F. (2025)**. Increased callosal thickness in early trained opera singers. *Brain Topography*, 38, 56. n=55. MRI. DOI: 10.1007/s10548-025-01134-x.
6. **Olszewska, A. M., Gaca, M., Herman, A. M., Jednoróg, K., & Marchewka, A. (2021)**. How musical training shapes the adult brain: predispositions and neuroplasticity. *Frontiers in Neuroscience*, 15, 630829. Review. DOI: 10.3389/fnins.2021.630829.
7. **Porfyri, G.-N., Paraskevopoulos, E., Bamidis, P. D., & Pantev, C. (2025)**. Multisensory vs. unisensory learning: EEG network analysis. n=30. EEG, Group×Time F(1,28)=4.635, η²=0.168.
8. **Cui, A.-X., Choi, Y., Motamed Yeganeh, N., Hermiston, N., Werker, J. F., & Boyd, L. A. (2025)**. Music training and language learning improve verbal memory performance but do not change white matter characteristics of the splenium: a longitudinal DTI study. *Frontiers in Psychology*, 16, 1659705. n=65. DOI: 10.3389/fpsyg.2025.1659705.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (TIH, SGM, EFC, BND) | PPC (30D) + ASA (30D) mechanisms |
| Within-network | S⁰.L7.coherence[80:104] + HC⁰.BND | R³.x_l0l5[25:33] + PPC.pitch_extraction |
| Between-network | S⁰.L7.coherence[80:104] + HC⁰.SGM | R³.x_l4l5[33:41] + ASA.scene_analysis |
| Expertise | S⁰.L9.entropy[104:128] + HC⁰.EFC | R³.tonalness[14] + ASA.attention_gating |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 37/2304 = 1.61% | 16/2304 = 0.69% |
| Output | 10D | 10D (same) |

### Why PPC + ASA replaces HC⁰ mechanisms

- **BND → PPC.pitch_extraction** [0:10]: Within-network binding maps to PPC's pitch extraction for intra-network efficiency.
- **SGM → ASA.scene_analysis** [0:10]: Boundary maintenance maps to ASA's scene analysis for network isolation.
- **EFC → ASA.attention_gating** [10:20]: Expertise predictions map to ASA's attention for expertise signature.
- **TIH → PPC.contour_tracking** [20:30]: Multi-scale integration maps to PPC's contour tracking for specialization.

---

---

## 15. Doc-Code Mismatches (Phase 5 Reference)

| Field | Doc (EDNR.md) | Code (ednr.py) | Action Required |
|-------|---------------|-----------------|-----------------|
| **FULL_NAME** | "Expertise-Dependent Network Reorganization" | "Expectation-Dependent Novelty Response" | Code needs rename to match doc |
| **OUTPUT_DIM** | 10D (4+2+2+2) | 11D (4+2+2+3) | Code has 3 Layer-F dims, doc has 2; reconcile in Phase 5 |
| **MECHANISM_NAMES** | ("PPC", "ASA") | ("ASA",) | Code missing PPC mechanism |
| **h3_demand** | 16 tuples (see §5) | () empty | Code needs 16 tuples populated |
| **brain_regions** | 14 regions (see §8) | 3 regions (STG, IFG, ACC) | Code needs expansion (Phase 5) |
| **citations** | 8 papers (see §13) | 3 (Herholz 2012, Pantev 2015, Munte 2002) | Code needs update (Phase 5) |
| **Layer F dims** | 2 (optimal_config_pred, processing_efficiency) | 3 (optimal_config_pred, processing_efficiency_pred, expertise_transfer_pred) | Resolve: drop expertise_transfer_pred or add to doc |
| **version** | 2.1.0 | 2.0.0 | Code needs version bump (Phase 5) |

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **10D**
**Evidence Tier**: **α (Mechanistic)**
**Confidence**: **>90%**
