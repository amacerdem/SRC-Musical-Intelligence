# PCU-β3-UDP: Uncertainty-Driven Pleasure

**Model**: Uncertainty-Driven Pleasure
**Unit**: PCU (Predictive Coding Unit)
**Circuit**: Imagery (Auditory Cortex, IFG, STS, Hippocampus)
**Tier**: β (Bridging) — 70-90% confidence
**Version**: 2.1.0 (deep C³ literature review: 1 → 12 papers)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/PCU-β3-UDP.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Uncertainty-Driven Pleasure** (UDP) model describes how in high-uncertainty contexts (atonal music), correct predictions become more rewarding than prediction errors, as they signal model improvement and reduced uncertainty.

```
UNCERTAINTY-DRIVEN PLEASURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TONAL CONTEXT (Low Uncertainty)        ATONAL CONTEXT (High Uncertainty)
────────────────────────────          ──────────────────────────────
Entropy: Low                          Entropy: High
Predictions: Easy                     Predictions: Hard

  Prediction ────► Error ────►         Prediction ────► Confirm ────►
  Easy             REWARDING           Hard              REWARDING
  (standard RPE)                       (model improvement signal)

  Confirmation ──► Neutral             Error ──────────► Less Rewarding
  (expected)                           (expected given uncertainty)

┌──────────────────────────────────────────────────────────────────┐
│             REWARD INVERSION (Mencke 2019)                       │
│                                                                  │
│  Standard:  Reward(error) > Reward(confirmation)                │
│  Inverted:  Reward(confirmation) > Reward(error)                │
│                                                                  │
│  Switch point: When context uncertainty exceeds threshold        │
│  Mechanism: Correct predictions signal learning progress         │
└──────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: In high-uncertainty contexts (atonal music), correct
predictions become more rewarding than prediction errors because
they signal model improvement and reduced uncertainty — the brain
values learning progress over surprise.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why UDP Matters for PCU

UDP reveals context-dependent reward inversion:

1. **HTP** (α1) provides hierarchical prediction timing.
2. **PWUP** (β1) modulates PE by contextual precision.
3. **WMED** (β2) separates entrainment from WM.
4. **UDP** (β3) shows that reward valence inverts under high uncertainty.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → PPC+TPC+MEM → UDP)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    UDP COMPUTATION ARCHITECTURE                             ║
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
║  │                         UDP reads: ~17D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                         UDP demand: ~16 of 2304 tuples           │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Imagery Circuit ═══════════   ║
║                               │                                              ║
║                       ┌───────┴───────┐───────┐                              ║
║                       ▼               ▼       ▼                              ║
║  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              ║
║  │  PPC (30D)      │  │  TPC (30D)      │  │  MEM (30D)      │              ║
║  │                 │  │                 │  │                 │              ║
║  │ Pitch Ext[0:10] │  │ Spec Shp [0:10] │  │ Work Mem [0:10] │              ║
║  │ Interval  [10:20]│ │ Temp Env [10:20]│  │ Long-Term[10:20]│              ║
║  │ Contour  [20:30] │ │ Source Id[20:30]│  │ Pred Buf [20:30]│              ║
║  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘              ║
║           └────────────┬───────┴────────────────────┘                        ║
║                        ▼                                                     ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    UDP MODEL (10D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_uncertainty_level,                     │        ║
║  │                       f02_confirmation_reward,                   │        ║
║  │                       f03_error_reward,                          │        ║
║  │                       f04_pleasure_index                         │        ║
║  │  Layer P (Present):   context_assessment,                        │        ║
║  │                       prediction_accuracy,                       │        ║
║  │                       reward_computation                         │        ║
║  │  Layer F (Future):    reward_expectation,                        │        ║
║  │                       model_improvement,                         │        ║
║  │                       pleasure_anticipation                      │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Year | Method | N | Key Finding | Effect Size | Brain Regions (MNI) | MI Relevance |
|---|-------|------|--------|---|-------------|-------------|---------------------|-------------|
| 1 | **Mencke et al.** | 2019 | Behavioral + MIR corpus | 100 segments | In atonal (high-uncertainty) contexts, correct predictions more rewarding than errors; key clarity d=3.0, pulse clarity d=2.0 (tonal vs atonal) | d_Cohen=3.0 (key), d_Cohen=2.0 (pulse) | — (behavioral) | **f02 confirmation reward, f01 uncertainty** |
| 2 | **Gold et al.** | 2019 | Behavioral (IDyOM) | 43 + 27 | Inverted-U for IC and entropy on liking; IC x entropy interaction: preference for predictability in high-uncertainty contexts | Quadratic IC: significant; R²=0.13 (IC-unexpectedness) | — (behavioral) | **f01 uncertainty, f04 pleasure (Wundt curve)** |
| 3 | **Cheung et al.** | 2019 | fMRI + behavioral | 39 + 40 | Uncertainty x surprise interaction on pleasure; low-uncertainty/high-surprise and high-uncertainty/low-surprise both pleasurable (saddle surface) | beta_interaction=-0.124 (p<0.001); marginal R²=0.476 | Amygdala/Hipp (L: -20,-6,-16; R: 22,-6,-16), Aud Cortex (L: -54,-22,8; R: 52,-16,6), NAcc (R: 10,12,-8), Caudate (L: -10,12,8), pre-SMA (0,8,52) | **f01 uncertainty, f03 error reward, f04 pleasure** |
| 4 | **Gold et al.** | 2023 | fMRI + behavioral (IDyOM) | 24 | IC x entropy interaction replicated in naturalistic music; VS and R STG reflect pleasure of musical expectancies; VS tracks liked surprises | IC x entropy interaction replicated; VS liking effect | R STG (~58,-22,8), VS (~10,10,-8) | **f04 pleasure, reward_expectation** |
| 5 | **Salimpoor et al.** | 2011 | PET ([11C]raclopride) + fMRI | 8 | Dopamine release in caudate during anticipation, NAcc during peak pleasure; 6.4-9.2% binding potential change | delta_BP: caudate 6.4%, NAcc 9.2% | Caudate (14,-6,20), NAcc (8,10,-8), Putamen (23,1,1) | **reward_expectation (caudate anticipation), f04 pleasure (NAcc consummation)** |
| 6 | **Mas-Herrero et al.** | 2014 | Behavioral + psychophysiology | 30 (10 per group) | Specific musical anhedonia: dissociation between music and monetary reward; SCR-pleasure slope R²=0.32 | SCR slope: R²=0.32 (p=0.001); BMRQ group F(2,23)=19.14, p<0.001 | — (behavioral/psychophysiology) | **f04 pleasure (individual differences in reward access)** |
| 7 | **Chabin et al.** | 2020 | HD-EEG (256-ch) | 18 | Musical chills: increased theta in right prefrontal (OFC source); decreased theta in right central (SMA) and right temporal (STG) during chills; beta/alpha ratio tracks arousal | Theta RC: F(2,15)=4.09, p=0.025; RT: F(2,15)=5.88, p=0.006; RPF: F(2,15)=3.28, p=0.049 | OFC source (prefrontal), SMA source (central), R STG source (temporal) | **pleasure_anticipation (OFC theta), f04 pleasure (chills peak)** |
| 8 | **Borges et al.** | 2019 | EEG + ECG | 28 | 1/f scaling of resting-state neural activity predicts music pleasure; temporal cortex scaling change linked to pleasure | r_s=0.37 (parietal alpha), r_s=-0.42 (left temporal gamma_m change) | Temporal cortex (left > right), Parietal, Occipital (EEG scalp) | **f01 uncertainty (1/f scaling as predictability proxy)** |
| 9 | **Bravo et al.** | 2017 | fMRI + behavioral | 12 (fMRI) + 75 (behav) | Intermediate dissonance (minor thirds) = most ambiguous; heightened right Heschl's gyrus response under uncertainty; slowest RT for ambiguous stimuli | RT: intermediate dissonance slowest; R HG BOLD increase | R Heschl's gyrus (~46,-14,8) | **f01 uncertainty (sensory precision weighting under uncertainty)** |
| 10 | **Mohebi et al.** | 2024 | Fiber photometry (dLight) in rats | 13 rats | DA transients follow striatal gradient: DLS (fast, short horizon) → DMS (medium) → VS/NAcc (slow, long horizon); best-fit tau: DLS=36s, DMS=414s, VS=981s | tau_DLS=36s, tau_DMS=414s, tau_VS=981s; F(2,39)=23.6, p=2.0e-5 | DLS, DMS, VS (rat striatum) | **reward_expectation (multi-timescale DA prediction errors)** |
| 11 | **Schilling et al.** | 2023 | Theoretical / computational | — | Predictive coding + stochastic resonance as fundamental auditory principles; Bayesian brain: percept = posterior from prior prediction + likelihood; precision weighting of prediction errors | Theoretical framework | Auditory pathway (DCN → cortex) | **f01 uncertainty (Bayesian precision), f02/f03 (PE weighting)** |
| 12 | **Harding et al.** | 2025 | fMRI + behavioral (RCT) | 41 MDD patients | Psilocybin > escitalopram for anhedonia reduction (F(1,39)=4.17, p=0.048); PT maintains surprise-related valence; escitalopram diminishes surprise differentiation; vmPFC decreases post-PT | Anhedonia interaction: F(1,39)=4.17, p=0.048; vmPFC interaction: F(1,39)=7.07, p=0.011 | vmPFC (-2,46,-8), NAcc (11,9,-1), R STG (task-derived), Angular gyrus (whole-brain) | **f04 pleasure (hedonic processing), f01 uncertainty (predictive priors)** |

### 3.2 Effect Size Summary

```
Primary Effect:       Reward inversion in high-uncertainty contexts (Mencke 2019)
                      IC x entropy saddle interaction on pleasure (Cheung 2019, Gold 2019, 2023)
                      Dopamine release caudate (anticipation) and NAcc (peak): 6-9% BP change
Heterogeneity:        Low — IC x entropy interaction replicated across 3 independent groups
Quality Assessment:   β-tier (behavioral + fMRI + PET + EEG convergence)
Replication:          Cheung 2019 → Gold 2023 (direct replication of IC x entropy)
                      Salimpoor 2011 → Gold 2023 (VS pleasure correlation)
Sample Sizes:         Range 8-75; majority 18-43; total across studies ~370+
```

---

## 4. R³ Input Mapping: What UDP Reads

### 4.1 R³ Feature Dependencies (~17D of 49D)

| R³ Group | Index | Feature | UDP Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **A: Consonance** | [4] | sensory_pleasantness | Context certainty | Inverse of uncertainty |
| **A: Consonance** | [5] | periodicity | Tonal certainty | Harmonic structure |
| **B: Energy** | [10] | spectral_flux | Event detection | Confirmation/error trigger |
| **C: Timbre** | [14] | tonalness | Key clarity proxy | Uncertainty threshold |
| **C: Timbre** | [18:21] | tristimulus1-3 | Harmonic context | Tonal cues |
| **D: Change** | [21] | spectral_change | Prediction accuracy | Correct vs incorrect |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | Reward computation | Pleasure signal |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[4] sensory_pleasantness ────┐
R³[14] tonalness ──────────────┼──► Context certainty (inverse of uncertainty)
MEM.long_term_memory[10:20] ───┘   Low consonance → high uncertainty (atonal)

R³[21] spectral_change ────────┐
MEM.working_memory[0:10] ──────┼──► Prediction accuracy
PPC.pitch_extraction[0:10] ────┘   Low change = match (confirmation)
                                   High change = error

R³[41:49] x_l5l7 ─────────────┐
MEM.prediction_buffer[20:30] ──┼──► Context-dependent reward
H³ entropy tuples ─────────────┘   Tonal: Reward(error) > Reward(confirm)
                                   Atonal: Reward(confirm) > Reward(error)
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

UDP requires H³ features for context assessment (slow uncertainty estimation over long windows) and event detection (fast confirmation/error detection). The demand reflects the need for both rapid event categorization and slow contextual evaluation.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 4 | sensory_pleasantness | 3 | M0 (value) | L2 (bidi) | Consonance at 100ms |
| 4 | sensory_pleasantness | 16 | M1 (mean) | L0 (fwd) | Mean consonance over 1s |
| 4 | sensory_pleasantness | 16 | M20 (entropy) | L0 (fwd) | Consonance entropy 1s |
| 14 | tonalness | 8 | M1 (mean) | L0 (fwd) | Mean tonalness over 500ms |
| 14 | tonalness | 16 | M1 (mean) | L0 (fwd) | Mean tonalness over 1s |
| 21 | spectral_change | 1 | M0 (value) | L2 (bidi) | PE at 50ms (fast) |
| 21 | spectral_change | 3 | M0 (value) | L2 (bidi) | PE at 100ms |
| 21 | spectral_change | 3 | M4 (max) | L2 (bidi) | Peak PE at 100ms |
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | Event salience 100ms |
| 10 | spectral_flux | 3 | M8 (velocity) | L2 (bidi) | Event velocity 100ms |
| 41 | x_l5l7[0] | 8 | M0 (value) | L0 (fwd) | Reward coupling at 500ms |
| 41 | x_l5l7[0] | 16 | M1 (mean) | L0 (fwd) | Mean reward coupling 1s |
| 41 | x_l5l7[0] | 16 | M20 (entropy) | L0 (fwd) | Reward entropy 1s |
| 41 | x_l5l7[0] | 16 | M6 (skew) | L0 (fwd) | Reward skew 1s |
| 5 | periodicity | 8 | M1 (mean) | L0 (fwd) | Mean periodicity 500ms |
| 5 | periodicity | 16 | M18 (trend) | L0 (fwd) | Periodicity trend 1s |

**Total UDP H³ demand**: 16 tuples of 2304 theoretical = 0.69%

### 5.2 PPC + TPC + MEM Mechanism Binding

| Mechanism | Sub-section | Range | UDP Role | Weight |
|-----------|-------------|-------|----------|--------|
| **PPC** | Pitch Extraction | PPC[0:10] | Pitch prediction accuracy | 0.7 |
| **PPC** | Interval Analysis | PPC[10:20] | Interval confirmation/error | 0.8 |
| **PPC** | Contour Tracking | PPC[20:30] | Melodic expectation | 0.6 |
| **TPC** | Spectral Shape | TPC[0:10] | Timbral context assessment | 0.5 |
| **TPC** | Temporal Envelope | TPC[10:20] | Event timing confirmation | 0.6 |
| **TPC** | Source Identity | TPC[20:30] | Context categorization | 0.5 |
| **MEM** | Working Memory | MEM[0:10] | Prediction-outcome comparison | **1.0** (primary) |
| **MEM** | Long-Term Memory | MEM[10:20] | Context uncertainty estimation | **1.0** (primary) |
| **MEM** | Prediction Buffer | MEM[20:30] | Reward computation | **0.9** |

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
UDP OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_uncertainty_level    │ [0, 1] │ Context uncertainty index.
    │                          │        │ f01 = σ(0.40 * consonance_entropy_1s
    │                          │        │       + 0.30 * (1 - tonalness_mean_1s)
    │                          │        │       + 0.30 * reward_entropy_1s)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_confirmation_reward  │ [0, 1] │ Context-dependent confirmation reward.
    │                          │        │ f02 = σ(0.40 * f01 * (1 - pe_100ms)
    │                          │        │       + 0.30 * mean(MEM.ltm[10:20])
    │                          │        │       + 0.30 * periodicity_trend_1s)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_error_reward         │ [0, 1] │ Standard error reward.
    │                          │        │ f03 = σ(0.40 * (1 - f01) * pe_100ms
    │                          │        │       + 0.30 * pe_max_100ms
    │                          │        │       + 0.30 * mean(MEM.wm[0:10]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_pleasure_index       │ [0, 1] │ Net pleasure signal.
    │                          │        │ f04 = σ(0.50 * max(f02, f03)
    │                          │        │       + 0.50 * mean(MEM.pred[20:30]))

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ context_assessment       │ [0, 1] │ MEM uncertainty assessment.
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ prediction_accuracy      │ [0, 1] │ PPC match/mismatch signal.
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ reward_computation       │ [0, 1] │ MEM context-dependent reward.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ reward_expectation       │ [0, 1] │ Striatum reward prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ model_improvement        │ [0, 1] │ Prediction quality trajectory.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ pleasure_anticipation    │ [0, 1] │ Affective state (1-3s).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Reward Inversion Function

```
Reward = α·Confirmation + β·Error
where:
  if Uncertainty > threshold:  α > β (atonal: confirmation rewarding)
  else:                        β > α (tonal: error rewarding)

Uncertainty = entropy_normalized(context)
Confirmation = 1 - |prediction - observation|
Error = |prediction - observation|

Pleasure = max(α·Confirmation, β·Error)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Uncertainty Level
f01 = σ(0.40 * consonance_entropy_1s
       + 0.30 * (1 - tonalness_mean_1s)
       + 0.30 * reward_entropy_1s)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f02: Confirmation Reward (high when uncertain + correct)
f02 = σ(0.40 * f01 * (1 - pe_100ms)        # uncertainty × confirmation
       + 0.30 * mean(MEM.long_term_memory[10:20])
       + 0.30 * periodicity_trend_1s)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f03: Error Reward (high when certain + error)
f03 = σ(0.40 * (1 - f01) * pe_100ms        # certainty × error
       + 0.30 * pe_max_100ms
       + 0.30 * mean(MEM.working_memory[0:10]))
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f04: Pleasure Index
f04 = σ(0.50 * max(f02, f03)
       + 0.50 * mean(MEM.prediction_buffer[20:30]))
# coefficients: 0.50 + 0.50 = 1.0 ✓

# Reward signal decay
dReward/dt = τ⁻¹ · (Target_Reward - Current_Reward)
    where τ = 3s (Mencke 2019)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Studies | Evidence Type | UDP Function |
|--------|-----------------|---------|---------------|--------------|
| **Auditory Cortex (STG)** | L: -54, -22, 8; R: 52, -16, 6 | Cheung 2019, Gold 2023, Chabin 2020, Harding 2025 | fMRI, EEG source | Prediction generation; uncertainty x surprise interaction (beta=-0.182 L, -0.128 R) |
| **Ventral Striatum (NAcc)** | R: 8, 10, -8 (Salimpoor); R: 10, 12, -8 (Cheung); R: 11, 9, -1 (Harding) | Salimpoor 2011, Cheung 2019, Gold 2023, Harding 2025 | PET, fMRI | Reward computation; dopamine release during peak pleasure (9.2% BP change); uncertainty tracking (beta=0.242) |
| **Caudate Nucleus** | R: 14, -6, 20 (Salimpoor); L: -10, 12, 8 (Cheung) | Salimpoor 2011, Cheung 2019 | PET, fMRI | Anticipatory reward; dopamine release during anticipation (6.4% BP change); uncertainty tracking |
| **Amygdala / Anterior Hippocampus** | L: ~-20, -6, -16; R: ~22, -6, -16 | Cheung 2019 | fMRI | Uncertainty x surprise interaction (beta=-0.116 L, -0.140 R); emotional salience of prediction outcomes |
| **IFG (Inferior Frontal Gyrus)** | ~±44, 18, 8 | Cheung 2019 (discussion) | Literature inference | Expectation generation; top-down prediction to auditory cortex |
| **vmPFC** | -2, 46, -8 | Harding 2025 | fMRI | Higher-order reward processing; decreases post-psilocybin (F(1,39)=7.07, p=0.011); hedonic prior encoding |
| **OFC (Orbitofrontal Cortex)** | Prefrontal (EEG source) | Chabin 2020 | HD-EEG source | Increased theta during pleasurable chills; reward evaluation |
| **pre-SMA** | 0, 8, 52 | Cheung 2019 | fMRI | Uncertainty tracking (beta=0.358); anticipatory motor preparation |
| **R Heschl's Gyrus** | ~46, -14, 8 | Bravo 2017 | fMRI | Heightened sensory cortical response under uncertainty; precision weighting of auditory evidence |
| **Putamen** | 23, 1, 1 | Salimpoor 2011 | PET | Dopamine release during pleasurable music (6.5-7.9% BP change) |

---

## 9. Cross-Unit Pathways

### 9.1 UDP Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    UDP INTERACTIONS                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (PCU):                                                         │
│  PWUP.uncertainty_index ─────► UDP (uncertainty determines reward mode)    │
│  UDP.pleasure_index ─────────► MAA (pleasure for appreciation)             │
│  UDP.confirmation_reward ────► PSH (confirmation triggers silencing)       │
│  WMED.wm_contribution ──────► UDP (WM aids uncertainty estimation)         │
│                                                                             │
│  CROSS-UNIT (PCU → ARU):                                                   │
│  UDP.pleasure_index ─────────► ARU (pleasure signal for reward circuit)    │
│  UDP.reward_expectation ─────► ARU (anticipatory reward signal)            │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  PPC mechanism (30D) ────────► UDP (pitch prediction accuracy)             │
│  TPC mechanism (30D) ────────► UDP (temporal context assessment)           │
│  MEM mechanism (30D) ────────► UDP (context/prediction/reward)             │
│  R³ (~17D) ──────────────────► UDP (direct spectral features)             │
│  H³ (16 tuples) ─────────────► UDP (temporal dynamics)                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Reward inversion** | Atonal: confirmation > error reward | **Confirmed** (Mencke 2019; supported by Cheung 2019 high-uncertainty/low-surprise = pleasurable) |
| **Context dependence** | Reward pattern should flip with uncertainty level | **Confirmed** (Cheung 2019 saddle surface; Gold 2019 IC x entropy interaction) |
| **Uncertainty threshold** | Should exist a clear inversion point | Testable via parametric design |
| **Learning effect** | Familiarity should shift uncertainty downward | Testable via exposure (Gold 2019 repetition decreased liking but maintained complexity preference) |
| **Neural correlate** | NAcc should track context-dependent reward | **Partially confirmed** (Cheung 2019: NAcc tracks uncertainty; Salimpoor 2011: NAcc dopamine at peak pleasure; Gold 2023: VS reflects liked surprises) |
| **Dopamine anticipation** | Caudate should be active during anticipatory phase | **Confirmed** (Salimpoor 2011: caudate anticipation, NAcc consummation) |
| **Anhedonia dissociation** | Musical pleasure should be selectively impaired in musical anhedonia | **Confirmed** (Mas-Herrero 2014: preserved monetary, absent musical reward) |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class UDP(BaseModel):
    """Uncertainty-Driven Pleasure Model.

    Output: 10D per frame.
    Reads: PPC mechanism (30D), TPC mechanism (30D), MEM mechanism (30D), R³ direct.
    """
    NAME = "UDP"
    UNIT = "PCU"
    TIER = "β3"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("PPC", "TPC", "MEM")

    TAU_DECAY = 3.0                # s (Mencke 2019)
    UNCERTAINTY_THRESHOLD = 0.5    # Inversion point

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """16 tuples for UDP computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── Context assessment: slow uncertainty ──
            (4, 3, 0, 2),      # sensory_pleasantness, 100ms, value, bidi
            (4, 16, 1, 0),     # sensory_pleasantness, 1000ms, mean, fwd
            (4, 16, 20, 0),    # sensory_pleasantness, 1000ms, entropy, fwd
            (14, 8, 1, 0),     # tonalness, 500ms, mean, fwd
            (14, 16, 1, 0),    # tonalness, 1000ms, mean, fwd
            (5, 8, 1, 0),      # periodicity, 500ms, mean, fwd
            (5, 16, 18, 0),    # periodicity, 1000ms, trend, fwd
            # ── Event detection: fast PE ──
            (21, 1, 0, 2),     # spectral_change, 50ms, value, bidi
            (21, 3, 0, 2),     # spectral_change, 100ms, value, bidi
            (21, 3, 4, 2),     # spectral_change, 100ms, max, bidi
            (10, 3, 0, 2),     # spectral_flux, 100ms, value, bidi
            (10, 3, 8, 2),     # spectral_flux, 100ms, velocity, bidi
            # ── Reward computation: coupling ──
            (41, 8, 0, 0),     # x_l5l7[0], 500ms, value, fwd
            (41, 16, 1, 0),    # x_l5l7[0], 1000ms, mean, fwd
            (41, 16, 20, 0),   # x_l5l7[0], 1000ms, entropy, fwd
            (41, 16, 6, 0),    # x_l5l7[0], 1000ms, skew, fwd
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute UDP 10D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30), "TPC": (B,T,30), "MEM": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) UDP output
        """
        ppc = mechanism_outputs["PPC"]
        tpc = mechanism_outputs["TPC"]
        mem = mechanism_outputs["MEM"]

        # Mechanism sub-sections
        ppc_pitch = ppc[..., 0:10]
        ppc_interval = ppc[..., 10:20]
        mem_wm = mem[..., 0:10]
        mem_ltm = mem[..., 10:20]
        mem_pred = mem[..., 20:30]

        # H³ direct features
        consonance_entropy_1s = h3_direct[(4, 16, 20, 0)].unsqueeze(-1)
        tonalness_mean_1s = h3_direct[(14, 16, 1, 0)].unsqueeze(-1)
        reward_entropy_1s = h3_direct[(41, 16, 20, 0)].unsqueeze(-1)
        pe_100ms = h3_direct[(21, 3, 0, 2)].unsqueeze(-1)
        pe_max_100ms = h3_direct[(21, 3, 4, 2)].unsqueeze(-1)
        periodicity_trend_1s = h3_direct[(5, 16, 18, 0)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: Uncertainty Level (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.40 * consonance_entropy_1s
            + 0.30 * (1 - tonalness_mean_1s)
            + 0.30 * reward_entropy_1s
        )

        # f02: Confirmation Reward (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.40 * f01 * (1 - pe_100ms)
            + 0.30 * mem_ltm.mean(-1, keepdim=True)
            + 0.30 * periodicity_trend_1s
        )

        # f03: Error Reward (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.40 * (1 - f01) * pe_100ms
            + 0.30 * pe_max_100ms
            + 0.30 * mem_wm.mean(-1, keepdim=True)
        )

        # f04: Pleasure Index (coefficients sum = 1.0)
        f04 = torch.sigmoid(
            0.50 * torch.max(f02, f03)
            + 0.50 * mem_pred.mean(-1, keepdim=True)
        )

        # ═══ LAYER P: Present ═══
        context_assess = f01
        pred_accuracy = torch.sigmoid(
            0.5 * ppc_pitch.mean(-1, keepdim=True)
            + 0.5 * (1 - pe_100ms)
        )
        reward_comp = f04

        # ═══ LAYER F: Future ═══
        reward_expect = torch.sigmoid(0.5 * f04 + 0.5 * f01)
        model_improve = torch.sigmoid(
            0.5 * f02 + 0.5 * periodicity_trend_1s
        )
        pleasure_antic = torch.sigmoid(0.5 * f04 + 0.5 * reward_expect)

        return torch.cat([
            f01, f02, f03, f04,                             # E: 4D
            context_assess, pred_accuracy, reward_comp,     # P: 3D
            reward_expect, model_improve, pleasure_antic,   # F: 3D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 (Mencke 2019, Gold 2019, Cheung 2019, Gold 2023, Salimpoor 2011, Mas-Herrero 2014, Chabin 2020, Borges 2019, Bravo 2017, Mohebi 2024, Schilling 2023, Harding 2025) | Primary + convergent evidence |
| **Effect Sizes** | 15+ | IC x entropy interaction, dopamine BP change, saddle surface, SCR slopes, EEG theta, BOLD betas |
| **Evidence Modality** | Behavioral + fMRI + PET + EEG + psychophysiology + computational | Multi-modal convergence |
| **Falsification Tests** | 7/7 testable, 5 confirmed or partially confirmed | Strong validity |
| **R³ Features Used** | ~17D of 49D | Consonance + energy + timbre + change + interactions |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Pitch prediction accuracy |
| **TPC Mechanism** | 30D (3 sub-sections) | Temporal context assessment |
| **MEM Mechanism** | 30D (3 sub-sections) | Context/prediction/reward |
| **Output Dimensions** | **10D** | 3-layer structure (no M layer) |

---

## 13. Scientific References

1. **Mencke, I., Omigie, D., Wald-Fuhrmann, M., & Brattico, E. (2019)**. Atonal music: Can uncertainty lead to pleasure? *Frontiers in Neuroscience*, 12, 979. https://doi.org/10.3389/fnins.2018.00979
2. **Gold, B. P., Pearce, M. T., Mas-Herrero, E., Dagher, A., & Zatorre, R. J. (2019)**. Predictability and uncertainty in the pleasure of music: A reward for learning? *Journal of Neuroscience*, 39(47), 9397-9409. https://doi.org/10.1523/JNEUROSCI.0428-19.2019
3. **Cheung, V. K. M., Harrison, P. M. C., Meyer, L., Pearce, M. T., Haynes, J.-D., & Koelsch, S. (2019)**. Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. *Current Biology*, 29(23), 4084-4092. https://doi.org/10.1016/j.cub.2019.09.067
4. **Gold, B. P., Pearce, M. T., McIntosh, A. R., Chang, C., Dagher, A., & Zatorre, R. J. (2023)**. Auditory and reward structures reflect the pleasure of musical expectancies during naturalistic listening. *Frontiers in Neuroscience*, 17, 1209398. https://doi.org/10.3389/fnins.2023.1209398
5. **Salimpoor, V. N., Benovoy, M., Larcher, K., Dagher, A., & Zatorre, R. J. (2011)**. Anatomically distinct dopamine release during anticipation and experience of peak emotion to music. *Nature Neuroscience*, 14(2), 257-262. https://doi.org/10.1038/nn.2726
6. **Mas-Herrero, E., Zatorre, R. J., Rodriguez-Fornells, A., & Marco-Pallares, J. (2014)**. Dissociation between musical and monetary reward responses in specific musical anhedonia. *Current Biology*, 24(6), 699-704. https://doi.org/10.1016/j.cub.2014.01.068
7. **Chabin, T., Gabriel, D., Chansophonkul, T., Michelant, L., Joucla, C., Haffen, E., Moulin, T., Comte, A., & Pazart, L. (2020)**. Cortical patterns of pleasurable musical chills revealed by high-density EEG. *Frontiers in Neuroscience*, 14, 565815. https://doi.org/10.3389/fnins.2020.565815
8. **Borges, A. F. T., Irrmischer, M., Brockmeier, T., Smit, D. J. A., Mansvelder, H. D., & Linkenkaer-Hansen, K. (2019)**. Scaling behaviour in music and cortical dynamics interplay to mediate music listening pleasure. *Scientific Reports*, 9, 17700. https://doi.org/10.1038/s41598-019-54060-x
9. **Bravo, F., Cross, I., Stamatakis, E. A., & Rohrmeier, M. (2017)**. Sensory cortical response to uncertainty and low salience during recognition of affective cues in musical intervals. *PLoS ONE*, 12(4), e0175991. https://doi.org/10.1371/journal.pone.0175991
10. **Mohebi, A., Wei, W., Pelattini, L., Kim, K., & Berke, J. D. (2024)**. Dopamine transients follow a striatal gradient of reward time horizons. *Nature Neuroscience*, 27(4), 737-746. https://doi.org/10.1038/s41593-023-01566-3
11. **Schilling, A., Sedley, W., Gerum, R., Metzner, C., Tziridis, K., Maier, A., Schulze, H., Zeng, F.-G., Friston, K. J., & Krauss, P. (2023)**. Predictive coding and stochastic resonance as fundamental principles of auditory phantom perception. *Brain*, 146(12), 4809-4825. https://doi.org/10.1093/brain/awad255
12. **Harding, R., Singer, N., Wall, M. B., Hendler, T., Erritzoe, D., Nutt, D., Carhart-Harris, R., & Roseman, L. (2025)**. Dissociable effects of psilocybin and escitalopram for depression on processing of musical surprises. *Molecular Psychiatry*, 30, 3188-3196. https://doi.org/10.1038/s41380-025-03035-8

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (EFC, AED, ASA, CPD) | PPC (30D) + TPC (30D) + MEM (30D) mechanisms |
| Context certainty | S⁰.L3.coherence[14] | R³[4] sensory_pleasantness + R³[14] tonalness |
| Uncertainty | S⁰.L9.entropy[116:120] | H³ consonance/coupling entropy tuples |
| Prediction accuracy | S⁰.L9.kurtosis[120:124] + HC⁰.EFC | R³[21] spectral_change + MEM.working_memory |
| Reward computation | S⁰.X_L5L9[224:232] + HC⁰.AED/CPD | R³[41:49] x_l5l7 + MEM.prediction_buffer |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 24/2304 = 1.04% | 16/2304 = 0.69% |
| Output | 10D | 10D (same) |

### What Changed from v2.0.0 to v2.1.0

| Aspect | v2.0.0 | v2.1.0 |
|--------|--------|--------|
| Papers | 1 (Mencke 2019) | 12 papers (deep C³ literature review) |
| Brain regions | 4 (indirect/inferred) | 10 with MNI coordinates from fMRI/PET/EEG |
| Evidence modality | Behavioral + theoretical | Behavioral + fMRI + PET + EEG + psychophysiology + computational |
| Falsification | 5 criteria, 1 confirmed | 7 criteria, 5 confirmed or partially confirmed |
| Effect sizes | 1 (reward inversion demonstrated) | 15+ quantitative effect sizes |

### Why PPC + TPC + MEM replaces HC⁰ mechanisms

- **EFC → MEM.working_memory** [0:10]: Efference copy for prediction-outcome comparison maps to MEM's working memory.
- **AED → MEM.prediction_buffer** [20:30]: Affective entrainment dynamics for reward computation maps to MEM's prediction/reward buffer.
- **ASA → TPC.source_identity** [20:30]: Auditory scene analysis for context categorization maps to TPC's source identity.
- **CPD → MEM.long_term_memory** [10:20]: Chills/peak detection for reward peaks maps to MEM's long-term contextual assessment.

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **10D**
**Evidence Tier**: **β (Bridging)**
**Confidence**: **70-90%**
