# NDU-α2-SDD: Supramodal Deviance Detection

**Model**: Supramodal Deviance Detection
**Unit**: NDU (Novelty Detection Unit)
**Circuit**: Salience + Perceptual (Anterior Insula, dACC, IFG)
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added H:Harmony, I:Information feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/NDU-α2-SDD.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Supramodal Deviance Detection** (SDD) model describes a domain-general mechanism for identifying statistical irregularities across sensory modalities, with significant multilinks (edge-to-edge correlations) between modality-specific deviance detection networks.

```
SUPRAMODAL DEVIANCE DETECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

              ┌───────────────────────────────────────────┐
              │        SUPRAMODAL HUB                     │
              │   (IFG: BA44, BA45, area 47m)            │
              └──────────────────┬────────────────────────┘
                                 │
       ┌─────────────────────────┴─────────────────────────┐
       │                         │                         │
       ▼                         ▼                         ▼
   ┌────────────┐          ┌────────────┐          ┌────────────┐
   │  AUDITORY  │          │   VISUAL   │          │   TACTILE  │
   │  DEVIANCE  │◄────────►│  DEVIANCE  │◄────────►│  DEVIANCE  │
   │  NETWORK   │  MULTI-  │  NETWORK   │  MULTI-  │  NETWORK   │
   │            │  LINKS   │            │  LINKS   │            │
   └────────────┘          └────────────┘          └────────────┘

   KEY FINDING:
   Deviance networks > Standard networks in between-network correlation

   NON-MUSICIANS: 47 multilinks
   MUSICIANS: 15 multilinks (more compartmentalized)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: A supramodal mechanism supports identification of
statistical irregularities across sensory modalities, with
significant multilinks between deviance networks.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why SDD Matters for NDU

SDD establishes the cross-modal deviance detection mechanism for the Novelty Detection Unit:

1. **MPG** (α1) provides melodic gradient context for deviance.
2. **SDD** (α2) extends to supramodal statistical irregularity detection.
3. **EDNR** (α3) links expertise to network reorganization affecting SDD multilinks.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → PPC+ASA → SDD)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SDD COMPUTATION ARCHITECTURE                              ║
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
║  │                         SDD reads: ~16D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                         SDD demand: ~18 of 2304 tuples           │        ║
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
║  │                    SDD MODEL (11D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_deviance_magnitude,                    │        ║
║  │                       f02_multilink_count,                       │        ║
║  │                       f03_supramodal_index,                      │        ║
║  │                       f04_ifg_hub_activation                     │        ║
║  │  Layer M (Math):      multilinks_function,                       │        ║
║  │                       supramodal_ratio                           │        ║
║  │  Layer P (Present):   deviance_signal, multilink_activation,     │        ║
║  │                       ifg_state                                  │        ║
║  │  Layer F (Future):    expectation_update,                        │        ║
║  │                       attention_reorienting                      │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Paraskevopoulos et al. 2022** | MEG | 25 | Supramodal mechanism: 47 multilinks (non-musicians) vs 15 (musicians) across deviance networks | Hedges' g = −1.09 (behavioral); p < 0.001 FDR | **Primary**: f02 multilink count, f03 supramodal index |
| **Paraskevopoulos et al. 2022** | MEG | 25 | IFG (area 47m left) is the dominant hub across all network layers; non-musicians: 192 edges/267 nodes vs musicians: 106 edges/123 nodes | Node degree ranking: area 47m left highest in 5/6 layers | **f04 IFG hub activation** |
| **Porfyri, Paraskevopoulos et al. 2025** | EEG | 30 | Multisensory training alters effective connectivity in all 3 modalities; unisensory training: no significant effect | F(1,28) = 4.635, p = 0.042, η² = 0.168 (Group × Time) | **f01 deviance magnitude**: top-down mechanism via IFG/MFG/insula |
| **Porfyri et al. 2025** | EEG | 30 | Left MFG (6v), left IFS (IFJa), left insula (PoI1) are central nodes of multisensory-induced neuroplasticity | p < 0.001 FDR corrected, 10,000 permutations | **f04 IFG hub**: confirms fronto-insular integration |
| **Kim et al. 2021** | MEG | 19 | IFG-LTDMI enhanced for most irregular condition; dissociable from perceptual ambiguity (STG-LTDMI) | F(2,36) = 6.526, p = 0.024 FDR; STG: F(2,36) = 12.373, p < 0.001 | **f01 deviance magnitude**: IFG indexes syntactic irregularity |
| **Carbajal & Malmierca 2018** | Review | — | SSA and MMN are micro/macroscopic manifestations of same deviance detection mechanism along auditory neuraxis | IC → MGB → AC hierarchy; NMDA-dependent | **Mechanistic basis**: hierarchical predictive coding for f01 |
| **Fong et al. 2020** | Review | — | MMN under predictive coding: 150-250ms latency, hierarchical prediction error propagation; disrupted in schizophrenia | MMN peak: 150-250ms from deviance onset | **f09 expectation update**: temporal constraint for prediction |
| **Cheung et al. 2019** | fMRI | 39 | Uncertainty and surprise jointly predict musical pleasure; amygdala, hippocampus, auditory cortex activity | Information-theoretic entropy/surprise model; p < 0.05 FWE | **Cross-unit**: SDD deviance → RPU reward pathway |

### 3.2 Effect Size Summary

```
Primary Evidence (k=8):  Converging across MEG, EEG, fMRI, review
Heterogeneity:           Low (consistent supramodal/IFG findings across labs)
Quality Assessment:      α-tier (direct MEG/EEG network analysis, replication)
Key Effect Sizes:
  - Multilinks: 47 vs 15 (non-musicians vs musicians) — Paraskevopoulos 2022
  - Behavioral SL advantage: Hedges' g = −1.09 — Paraskevopoulos 2022
  - Multisensory training: η² = 0.168 — Porfyri et al. 2025
  - IFG syntactic irregularity: F(2,36) = 6.526, p = 0.024 — Kim et al. 2021
  - SSA/MMN convergence: IC → MGB → AC — Carbajal & Malmierca 2018
Replication:             Paraskevopoulos 2022 → Porfyri et al. 2025 (same group, EEG confirmation)
```

---

## 4. R³ Input Mapping: What SDD Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | SDD Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **A: Consonance** | [0] | roughness | Deviance detection signal | Sensory dissonance |
| **B: Energy** | [7] | amplitude | Deviance magnitude proxy | Intensity changes |
| **B: Energy** | [8] | loudness | Perceptual loudness | Attention capture |
| **B: Energy** | [10] | spectral_flux | Spectral change detection | Frame-to-frame deviance |
| **D: Change** | [21] | spectral_change | Statistical irregularity | Rate of spectral change |
| **D: Change** | [22] | energy_change | Dynamic contrast | Energy deviation |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Cross-band coupling | Inter-feature correlation |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | Cross-level integration | Supramodal binding |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | SDD Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **H: Harmony** | [86] | syntactic_irregularity | Tonal syntax violation level | Lerdahl 2001: quantifies distance from tonal prototype; primary new feature for NDU — enables direct harmonic deviance detection beyond spectral change proxies |
| **I: Information** | [93] | tonal_ambiguity | Key uncertainty level | Quantifies tonal center ambiguity; high values signal perceptual contexts where deviance detection thresholds shift |

**Rationale**: SDD models supramodal deviance detection using v1 features spectral_flux [10] and spectral_change [21] as proxies for acoustic irregularity. syntactic_irregularity [86] provides a direct measure of tonal syntax violation — the most important new feature for NDU, resolving the NDU-001 gap. tonal_ambiguity [93] addresses the NDU-002 gap (perceptual_ambiguity) by quantifying key uncertainty, which modulates deviance detection thresholds. Together these features ground SDD's deviance computation in music-theoretic and information-theoretic frameworks.

**Code impact**: None yet — R³ v2 features are doc-only until Phase 5 integration. Current code reads r3[..., 0:49]; v2 features will extend the slice to r3[..., 0:128] when the EAR pipeline emits the expanded vector.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[10] spectral_flux ────────────┐
R³[21] spectral_change ──────────┼──► Deviance detection
ASA.attention_gating[10:20] ─────┘   Statistical irregularity signal

R³[25:33] x_l0l5 ───────────────┐
R³[41:49] x_l5l7 ───────────────┼──► Cross-modal multilink activation
PPC.interval_analysis[10:20] ────┘   Edge-to-edge correlation

R³[0] roughness ─────────────────┐
ASA.salience_weighting[20:30] ───┼──► IFG hub engagement
H³ entropy tuples ──────────────┘   Supramodal integration
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

SDD requires H³ features for deviance tracking at fast timescales and cross-modal integration at slower timescales. The demand reflects the multi-scale processing needed for supramodal irregularity detection.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 0 | M0 (value) | L2 (bidi) | Instantaneous deviance at 25ms |
| 10 | spectral_flux | 1 | M1 (mean) | L2 (bidi) | Mean deviance over 50ms |
| 10 | spectral_flux | 3 | M2 (std) | L2 (bidi) | Deviance variability 100ms |
| 21 | spectral_change | 3 | M0 (value) | L2 (bidi) | Spectral change at 100ms |
| 21 | spectral_change | 4 | M8 (velocity) | L0 (fwd) | Change velocity at 125ms |
| 21 | spectral_change | 16 | M20 (entropy) | L2 (bidi) | Change entropy at 1s |
| 22 | energy_change | 3 | M0 (value) | L2 (bidi) | Energy change at 100ms |
| 22 | energy_change | 3 | M2 (std) | L2 (bidi) | Energy variability 100ms |
| 0 | roughness | 3 | M0 (value) | L2 (bidi) | Roughness at 100ms |
| 0 | roughness | 3 | M20 (entropy) | L2 (bidi) | Roughness entropy 100ms |
| 7 | amplitude | 3 | M0 (value) | L2 (bidi) | Amplitude at 100ms |
| 8 | loudness | 3 | M0 (value) | L2 (bidi) | Loudness at 100ms |
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Cross-band coupling 100ms |
| 25 | x_l0l5[0] | 3 | M2 (std) | L2 (bidi) | Coupling variability 100ms |
| 41 | x_l5l7[0] | 3 | M0 (value) | L2 (bidi) | Cross-level integration 100ms |
| 41 | x_l5l7[0] | 16 | M14 (periodicity) | L2 (bidi) | Integration periodicity 1s |
| 8 | loudness | 3 | M20 (entropy) | L2 (bidi) | Loudness entropy 100ms |
| 10 | spectral_flux | 16 | M14 (periodicity) | L2 (bidi) | Flux periodicity at 1s |

**Total SDD H³ demand**: 18 tuples of 2304 theoretical = 0.78%

### 5.2 PPC + ASA Mechanism Binding

| Mechanism | Sub-section | Range | SDD Role | Weight |
|-----------|-------------|-------|----------|--------|
| **PPC** | Pitch Extraction | PPC[0:10] | Deviance magnitude encoding | 0.7 |
| **PPC** | Interval Analysis | PPC[10:20] | Cross-network edge correlation | 0.8 |
| **PPC** | Contour Tracking | PPC[20:30] | Deviance context (from MPG) | 0.5 |
| **ASA** | Scene Analysis | ASA[0:10] | Cross-modal scene segmentation | 0.6 |
| **ASA** | Attention Gating | ASA[10:20] | Deviance-directed attention | **1.0** (primary) |
| **ASA** | Salience Weighting | ASA[20:30] | IFG hub salience weighting | **0.9** |

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
SDD OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_deviance_magnitude   │ [0, 1] │ Statistical irregularity strength.
    │                          │        │ f01 = σ(0.35 * change_entropy_1s
    │                          │        │       + 0.35 * mean(ASA.attn[10:20])
    │                          │        │       + 0.30 * roughness_entropy)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_multilink_count      │ [0, 1] │ Cross-network edge correlations.
    │                          │        │ f02 = σ(0.35 * coupling_std_100ms
    │                          │        │       + 0.35 * integration_100ms
    │                          │        │       + 0.30 * mean(PPC.intv[10:20]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_supramodal_index     │ [0, 1] │ Cross-modal integration ratio.
    │                          │        │ f03 = σ(0.40 * f01 * f02
    │                          │        │       + 0.30 * integration_period_1s
    │                          │        │       + 0.30 * loudness_entropy)
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_ifg_hub_activation   │ [0, 1] │ Central hub engagement.
    │                          │        │ f04 = σ(0.35 * f01
    │                          │        │       + 0.35 * f02
    │                          │        │       + 0.30 * mean(ASA.sal[20:30]))

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ multilinks_function      │ [0, 1] │ Edge correlation measure.
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ supramodal_ratio         │ [0, 1] │ Deviance/standard ratio.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ deviance_signal          │ [0, 1] │ Current irregularity detection.
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ multilink_activation     │ [0, 1] │ Current cross-modal binding.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ ifg_state                │ [0, 1] │ Current integration state.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ expectation_update       │ [0, 1] │ 300ms ahead learning.
────┼──────────────────────────┼────────┼────────────────────────────────────
10  │ attention_reorienting    │ [0, 1] │ 100-200ms frontal allocation.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Multilinks Function

```
Multilinks(Network_i, Network_j) = Σ edge_correlation(e_i, e_j)

Supramodal_Index = Deviance_Multilinks / Standard_Multilinks

Expected: Supramodal_Index > 1.0 (stronger correlation for deviance)

Expertise Effect:
    Multilinks_nonmusician > Multilinks_musician (compartmentalization)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Deviance Magnitude
f01 = σ(0.35 * change_entropy_1s
       + 0.35 * mean(ASA.attention_gating[10:20])
       + 0.30 * roughness_entropy)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Multilink Count
f02 = σ(0.35 * coupling_std_100ms
       + 0.35 * integration_100ms
       + 0.30 * mean(PPC.interval_analysis[10:20]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f03: Supramodal Index
f03 = σ(0.40 * f01 * f02
       + 0.30 * integration_periodicity_1s
       + 0.30 * loudness_entropy)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f04: IFG Hub Activation
f04 = σ(0.35 * f01
       + 0.35 * f02
       + 0.30 * mean(ASA.salience_weighting[20:30]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | SDD Function |
|--------|-----------------|----------|---------------|--------------|
| **IFG (BA44)** | ±52, 16, 8 | 3 | Direct (MEG, EEG) | Supramodal hub — highest node degree in 5/6 network layers (Paraskevopoulos 2022) |
| **IFG (BA45)** | ±50, 26, 12 | 3 | Direct (MEG, EEG) | Language-related deviance; IFJa/IFJp neuroplasticity hub (Porfyri 2025) |
| **Area 47m (left)** | −46, 32, −4 | 3 | Direct (MEG, EEG) | Statistical learning hub; key node across all multilink layers (Paraskevopoulos 2022; Porfyri 2025) |
| **IFG (bilateral)** | L: −40.8, 18.5, 15.6; R: 37.6, 21.2, 15.1 (Talairach) | 2 | Direct (MEG) | IFG-LTDMI enhanced for syntactic irregularity, F(2,36)=6.526, p=0.024 (Kim 2021) |
| **STG (bilateral)** | L: −58, −20, 8; R: 58, −20, 8 | 2 | Direct (MEG) | STG-LTDMI enhanced for perceptual ambiguity, F(2,36)=12.373, p<0.001 (Kim 2021) |
| **TPO Junction** | ±50, −40, 12 | 2 | Direct (MEG) | Multisensory integration; musicians' clustering (Paraskevopoulos 2022) |
| **Intraparietal Lobule** | ±40, −48, 44 | 2 | Direct (MEG) | Cross-modal binding; multisensory hub (Paraskevopoulos 2022) |
| **ACC (area 25/32)** | 0, 24, 32 | 2 | Direct (EEG) | Musicians' clustering for inter-modal connectivity (Paraskevopoulos 2022; Porfyri 2025) |
| **Left Insula (PoI1)** | ~−38, −18, 14 | 1 | Direct (EEG) | Central node for multisensory-induced neuroplasticity (Porfyri 2025) |
| **Left MFG (6v/8C)** | ~−44, 4, 30 | 1 | Direct (EEG) | Caudal middle frontal gyrus; frequent in multisensory reconfiguration (Porfyri 2025) |
| **SMA/SCEF (left)** | ~−6, 10, 50 | 1 | Direct (MEG) | Highest degree node in non-musicians > musicians contrast (Paraskevopoulos 2022) |

---

## 9. Cross-Unit Pathways

### 9.1 SDD Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SDD INTERACTIONS                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (NDU):                                                         │
│  MPG.gradient_ratio ─────────► SDD (melodic gradient context)             │
│  SDD.deviance_signal ────────► CDMR (deviance for mismatch)              │
│  SDD.multilink_count ────────► EDNR (multilinks modulated by expertise)  │
│  SDD.supramodal_index ──────► SLEE (statistical learning link)           │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  PPC mechanism (30D) ────────► SDD (pitch/interval deviance)             │
│  ASA mechanism (30D) ────────► SDD (attention/salience)                  │
│  R³ (~16D) ──────────────────► SDD (direct spectral features)            │
│  H³ (18 tuples) ─────────────► SDD (temporal dynamics)                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Standard networks** | Should show fewer multilinks than deviance | **Confirmed** by Paraskevopoulos 2022 |
| **Single-modality** | Should show reduced supramodal activation | Testable via unimodal conditions |
| **IFG lesions** | Should impair cross-modal deviance detection | Testable via lesion studies |
| **Multilink threshold** | Should predict behavioral detection accuracy | Testable via correlation analysis |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class SDD(BaseModel):
    """Supramodal Deviance Detection Model.

    Output: 11D per frame.
    Reads: PPC mechanism (30D), ASA mechanism (30D), R³ direct.
    """
    NAME = "SDD"
    UNIT = "NDU"
    TIER = "α2"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("PPC", "ASA")

    MULTILINK_THRESHOLD = 0.6   # Edge correlation threshold
    TAU_DECAY = 0.5             # Prediction error decay
    RTI_WINDOW = 2.5            # seconds

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """18 tuples for SDD computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── Deviance detection (fast) ──
            (10, 0, 0, 2),     # spectral_flux, 25ms, value, bidi
            (10, 1, 1, 2),     # spectral_flux, 50ms, mean, bidi
            (10, 3, 2, 2),     # spectral_flux, 100ms, std, bidi
            (21, 3, 0, 2),     # spectral_change, 100ms, value, bidi
            (21, 4, 8, 0),     # spectral_change, 125ms, velocity, fwd
            (21, 16, 20, 2),   # spectral_change, 1000ms, entropy, bidi
            (22, 3, 0, 2),     # energy_change, 100ms, value, bidi
            (22, 3, 2, 2),     # energy_change, 100ms, std, bidi
            # ── Cross-modal integration ──
            (0, 3, 0, 2),      # roughness, 100ms, value, bidi
            (0, 3, 20, 2),     # roughness, 100ms, entropy, bidi
            (7, 3, 0, 2),      # amplitude, 100ms, value, bidi
            (8, 3, 0, 2),      # loudness, 100ms, value, bidi
            (25, 3, 0, 2),     # x_l0l5[0], 100ms, value, bidi
            (25, 3, 2, 2),     # x_l0l5[0], 100ms, std, bidi
            (41, 3, 0, 2),     # x_l5l7[0], 100ms, value, bidi
            (41, 16, 14, 2),   # x_l5l7[0], 1000ms, periodicity, bidi
            (8, 3, 20, 2),     # loudness, 100ms, entropy, bidi
            (10, 16, 14, 2),   # spectral_flux, 1000ms, periodicity, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute SDD 11D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30), "ASA": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,11) SDD output
        """
        ppc = mechanism_outputs["PPC"]    # (B, T, 30)
        asa = mechanism_outputs["ASA"]    # (B, T, 30)

        # PPC sub-sections
        ppc_pitch = ppc[..., 0:10]
        ppc_interval = ppc[..., 10:20]
        ppc_contour = ppc[..., 20:30]

        # ASA sub-sections
        asa_scene = asa[..., 0:10]
        asa_attn = asa[..., 10:20]
        asa_salience = asa[..., 20:30]

        # H³ direct features
        change_entropy_1s = h3_direct[(21, 16, 20, 2)].unsqueeze(-1)
        roughness_entropy = h3_direct[(0, 3, 20, 2)].unsqueeze(-1)
        coupling_std_100ms = h3_direct[(25, 3, 2, 2)].unsqueeze(-1)
        integration_100ms = h3_direct[(41, 3, 0, 2)].unsqueeze(-1)
        integration_period_1s = h3_direct[(41, 16, 14, 2)].unsqueeze(-1)
        loudness_entropy = h3_direct[(8, 3, 20, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══
        f01 = torch.sigmoid(
            0.35 * change_entropy_1s
            + 0.35 * asa_attn.mean(-1, keepdim=True)
            + 0.30 * roughness_entropy
        )
        f02 = torch.sigmoid(
            0.35 * coupling_std_100ms
            + 0.35 * integration_100ms
            + 0.30 * ppc_interval.mean(-1, keepdim=True)
        )
        f03 = torch.sigmoid(
            0.40 * (f01 * f02)
            + 0.30 * integration_period_1s
            + 0.30 * loudness_entropy
        )
        f04 = torch.sigmoid(
            0.35 * f01 + 0.35 * f02
            + 0.30 * asa_salience.mean(-1, keepdim=True)
        )

        # ═══ LAYER M: Mathematical ═══
        multilinks_func = torch.sigmoid(
            0.50 * f02 + 0.50 * integration_100ms
        )
        supramodal_ratio = f03

        # ═══ LAYER P: Present ═══
        deviance_signal = torch.sigmoid(
            0.50 * f01 + 0.50 * change_entropy_1s
        )
        multilink_activation = f02
        ifg_state = f04

        # ═══ LAYER F: Future ═══
        expectation_update = torch.sigmoid(
            0.50 * f01 + 0.50 * asa_attn.mean(-1, keepdim=True)
        )
        attention_reorienting = torch.sigmoid(
            0.50 * f04 + 0.50 * asa_salience.mean(-1, keepdim=True)
        )

        return torch.cat([
            f01, f02, f03, f04,                                    # E: 4D
            multilinks_func, supramodal_ratio,                     # M: 2D
            deviance_signal, multilink_activation, ifg_state,      # P: 3D
            expectation_update, attention_reorienting,             # F: 2D
        ], dim=-1)  # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 8 (3 empirical, 3 reviews, 2 cross-domain) | Deep literature review |
| **Effect Sizes** | Multilinks: 47 vs 15; Hedges' g = −1.09; η² = 0.168; F(2,36) = 6.526 | MEG/EEG network analysis |
| **Evidence Modality** | MEG, EEG, fMRI | Multi-modal convergence |
| **Falsification Tests** | 1/4 confirmed | Moderate validity |
| **R³ Features Used** | ~16D of 49D | Consonance + energy + change + interactions |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Pitch/interval deviance |
| **ASA Mechanism** | 30D (3 sub-sections) | Attention/salience |
| **Output Dimensions** | **11D** | 4-layer structure |

---

## 13. Scientific References

1. **Paraskevopoulos, E., Chalas, N., Anagnostopoulou, A. & Bamidis, P.D. (2022)**. Interaction within and between cortical networks subserving multisensory learning and its reorganization due to musical expertise. *Scientific Reports*, 12, 7891. n=25 (12 musicians, 13 non-musicians). MEG, Phase Transfer Entropy (PTE), multilayer network analysis. doi:10.1038/s41598-022-12158-9.
2. **Porfyri, I., Paraskevopoulos, E., Anagnostopoulou, A., Styliadis, C. & Bamidis, P.D. (2025)**. Multisensory vs. unisensory learning: how they shape effective connectivity networks subserving unimodal and multimodal integration. *Frontiers in Neuroscience*, 19, 1641862. n=30. EEG, Granger Causality, NBS. doi:10.3389/fnins.2025.1641862.
3. **Carbajal, G.V. & Malmierca, M.S. (2018)**. The Neuronal Basis of Predictive Coding Along the Auditory Pathway: From the Subcortical Roots to Cortical Deviance Detection. *Trends in Hearing*, 22, 1-33. Review. doi:10.1177/2331216518784822.
4. **Fong, C.Y., Law, W.H.C., Uka, T. & Koike, S. (2020)**. Auditory Mismatch Negativity Under Predictive Coding Framework and Its Role in Psychotic Disorders. *Frontiers in Psychiatry*, 11, 557932. Review. doi:10.3389/fpsyt.2020.557932.
5. **Kim, C.H., Jin, S.-H., Kim, J.S., Kim, Y., Yi, S.W. & Chung, C.K. (2021)**. Dissociation of Connectivity for Syntactic Irregularity and Perceptual Ambiguity in Musical Chord Stimuli. *Frontiers in Neuroscience*, 15, 693629. n=19. MEG, LTDMI. doi:10.3389/fnins.2021.693629.
6. **Cheung, V.K.M., Harrison, P.M.C., Meyer, L., Pearce, M.T., Haynes, J.-D. & Koelsch, S. (2019)**. Uncertainty and Surprise Jointly Predict Musical Pleasure and Amygdala, Hippocampus, and Auditory Cortex Activity. *Current Biology*, 29(23), 4084-4092.e4. n=39. fMRI. doi:10.1016/j.cub.2019.09.067.
7. **Kobayashi, K., Shiba, Y., Honda, S., Nakajima, S., Fujii, S., Mimura, M. & Noda, Y. (2024)**. Short-Term Effect of Auditory Stimulation on Neural Activities: A Scoping Review of Longitudinal Electroencephalography and Magnetoencephalography Studies. *Brain Sciences*, 14, 131. Scoping review. doi:10.3390/brainsci14020131.
8. **Billig, A.J., Lad, M., Sedley, W. & Griffiths, T.D. (2022)**. The hearing hippocampus. *Progress in Neurobiology*, 218, 102326. Review. doi:10.1016/j.pneurobio.2022.102326.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, ATT, EFC, BND) | PPC (30D) + ASA (30D) mechanisms |
| Deviance signal | S⁰.L9.kurtosis[104:128] + HC⁰.EFC | R³.spectral_change[21] + ASA.attention_gating |
| Multilink | S⁰.L7.band_correlation[80:104] + HC⁰.BND | R³.x_l0l5[25:33] + PPC.interval_analysis |
| Hub activation | S⁰.L5.contrast[30:55] + HC⁰.ATT | R³.roughness[0] + ASA.salience_weighting |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 27/2304 = 1.17% | 18/2304 = 0.78% |
| Output | 11D | 11D (same) |

### Why PPC + ASA replaces HC⁰ mechanisms

- **OSC → PPC.pitch_extraction** [0:10]: Gamma-band deviance signal maps to PPC's pitch extraction for deviance encoding.
- **ATT → ASA.attention_gating** [10:20]: Cross-modal attention maps to ASA's auditory scene attention.
- **EFC → ASA.salience_weighting** [20:30]: Expectation comparison maps to ASA's salience for statistical learning.
- **BND → PPC.interval_analysis** [10:20]: Cross-network binding maps to PPC's interval analysis for multilink computation.

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **11D**
**Evidence Tier**: **α (Mechanistic)**
**Confidence**: **>90%**

### Doc-Code Mismatches (for Phase 5)

| Aspect | Doc | Code (sdd.py) | Action |
|--------|-----|---------------|--------|
| FULL_NAME | Supramodal Deviance Detection | Spectral Deviance Detection | Fix in Phase 5 |
| h3_demand | 18 tuples specified | Empty `()` | Populate in Phase 5 |
| brain_regions | 11 regions (IFG, STG, TPO, IPL, ACC, Insula, MFG, SMA) | 3 regions (STG, IFG, ACC) | Expand in Phase 5 |
| metadata.citations | 8 papers | 3 papers (Recasens 2020, Naatanen 2007, Schroger 2015) | Update in Phase 5 |
| metadata.paper_count | 8 | 3 | Update in Phase 5 |
