# STU-γ2-NEWMD: Neural Entrainment-Working Memory Dissociation

**Model**: Neural Entrainment-Working Memory Dissociation
**Unit**: STU (Sensorimotor Timing Unit)
**Circuit**: Sensorimotor (Beat Entrainment + Temporal Memory Hierarchy)
**Tier**: γ (Speculative) — <70% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/STU-γ2-NEWMD.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Neural Entrainment-Working Memory Dissociation** (NEWMD) model describes a paradoxical dual-route architecture for rhythm production: automatic neural entrainment to beat (via steady-state evoked potentials, SS-EP) and cognitive working memory operate independently, with the surprising finding that stronger automatic entrainment predicts *worse* tapping performance.

```
THE DUAL-ROUTE PARADOX: ENTRAINMENT vs WORKING MEMORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ROUTE 1: AUTOMATIC ENTRAINMENT ROUTE 2: COGNITIVE CONTROL
Brain regions: Auditory cortex, Brain regions: DLPFC, premotor
 premotor cortex, cerebellum cortex, prefrontal cortex
Function: "Lock onto the beat" Function: "Remember and adapt"
Effect: β = -0.060 (PARADOXICAL) Effect: β = +0.068 (BENEFICIAL)
 Stronger SS-EP → worse tapping Higher WM → better performance

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Over-entrainment reduces temporal flexibility. When the
auditory system locks too tightly to a simple beat pattern (strong
SS-EP), the motor system loses adaptability. Working memory provides
a cognitive control route that compensates — higher WM capacity
enables better performance by maintaining flexible temporal
representations rather than rigid phase-locked ones.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Matters for STU

NEWMD provides the dissociation mechanism that contextualizes other STU models:

1. **AMSC** (α2) describes auditory-motor coupling; NEWMD explains why tight entrainment coupling can paradoxically impair motor output.
2. **HMCE** (α1) provides hierarchical context; NEWMD shows that cognitive context (WM) compensates when automatic entrainment fails.
3. **EDTA** (β3) addresses expertise-dependent tempo accuracy; NEWMD adds the insight that expertise may operate through the WM route rather than the entrainment route.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The NEWMD Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ NEWMD — COMPLETE CIRCUIT ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ RHYTHMIC INPUT (simple isochronous beat, e.g. 2.4Hz / 120 BPM) ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ ROUTE 1: AUDITORY CORTEX → CEREBELLUM (Automatic) │ ║
║ │ SS-EP (Steady-State Evoked Potential) │ ║
║ │ Function: Phase-locked neural response to beat │ ║
║ │ Effect: β = -0.060 (stronger → worse tapping) │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ ║
║ DISSOCIATED │ (independent, non-correlated pathways) ║
║ │ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ ROUTE 2: DLPFC → PREMOTOR CORTEX (Cognitive) │ ║
║ │ Working Memory capacity │ ║
║ │ Function: Flexible temporal representation and control │ ║
║ │ Effect: β = +0.068 (higher WM → better performance) │ ║
║ └──────────────────────────┬──────────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ MOTOR OUTPUT: TAPPING PERFORMANCE │ ║
║ │ Performance = f(Entrainment_paradox, WM_benefit) │ ║
║ │ Net effect: WM compensates for entrainment rigidity │ ║
║ └─────────────────────────────────────────────────────────────────────┘ ║
║ ║
║ DISSOCIATION: Entrainment () and WM () are independent predictors ║
║ KEY PARADOX: β_entrainment = -0.060 (negative), β_WM = +0.068 (positive) ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Sares 2023: SS-EP amplitude predicts worse tapping, β = -0.060 (n=48)
Sares 2023: WM (counting span) predicts better tapping, β = +0.068 (n=48)
Sares 2023: Entrainment and WM are independent predictors (dual-route model)
Noboa 2025: EXACT REPLICATION: β = -0.060, β = +0.068, R² = 0.316 (n=30)
Scartozzi 2024: Spontaneous beat β corr. musicality r=0.42, NOT rhythm discrim.
Zanto 2022: Rhythm training → STM via SPL, d = 0.52 (n=37, RCT)
```

### 2.2 Information Flow Architecture (EAR → BRAIN → H³ direct → NEWMD)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ NEWMD COMPUTATION ARCHITECTURE ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ AUDIO (44.1kHz waveform) ║
║ │ ║
║ ▼ ║
║ ┌──────────────────┐ ║
║ │ COCHLEA │ 128 mel bins × 172.27Hz frame rate ║
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
║ │ │ │ │amplitude│ │ │ │spec_chg │ │x_l0l5 │ │ ║
║ │ │ │ │loudness │ │ │ │energy_chg│ │x_l4l5 │ │ ║
║ │ │ │ │centroid │ │ │ │pitch_chg │ │x_l5l7 │ │ ║
║ │ │ │ │flux │ │ │ │timbre_chg│ │ │ │ ║
║ │ │ │ │onset │ │ │ │ │ │ │ │ ║
║ │ └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │ ║
║ │ NEWMD reads: 33D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed morphological features │ ║
║ │ │ ║
║ │ ┌── Beat ──────────┐ ┌── Psych Present ──┐ ┌── Bar ─────────┐ │ ║
║ │ │ 200ms (H6) │ │ 500ms (H11) │ │ 1000ms (H16) │ │ ║
║ │ │ │ │ │ │ │ │ ║
║ │ │ Beat induction │ │ Meter extraction │ │ Motor entrain. │ │ ║
║ │ └──────┬───────────┘ └──────┬─────────────┘ └──────┬──────────┘ │ ║
║ │ │ │ │ │ ║
║ │ ┌── Syllable ────┐ ┌── Beat ──────────┐ ┌── Section ────────┐ │ ║
║ │ │ 300ms (H8) │ │ 700ms (H14) │ │ 5000ms (H20) │ │ ║
║ │ │ │ │ │ │ │ │ ║
║ │ │ Short context │ │ Medium context │ │ Long context │ │ ║
║ │ └──────┬──────────┘ └──────┬────────────┘ └──────┬─────────────┘ │ ║
║ │ │ │ │ │ ║
║ │ └───────────────────┴─────────────────────┘ │ ║
║ │ NEWMD demand: ~16 of 2304 tuples │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────┐ ┌─────────────────┐ ║
║ │ (primary) │ │ (primary) │ ║
║ │ │ │ │ ║
║ │ Beat Ind [0:10] │ │ Short [0:10] │ WM short-term buffer ║
║ │ Meter Ex [10:20]│ │ Medium [10:20]│ WM phrase-level context ║
║ │ Motor En [20:30]│ │ Long [20:30]│ WM long-term adaptation ║
║ └────────┬────────┘ └────────┬────────┘ ║
║ │ │ ║
║ └────────┬───────────┘ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ NEWMD MODEL (10D Output) │ ║
║ │ │ ║
║ │ Layer E (Explicit): f01_entrainment_strength, │ ║
║ │ f02_wm_capacity, │ ║
║ │ f03_flexibility_cost, │ ║
║ │ f04_dissociation_index │ ║
║ │ Layer M (Math): paradox_magnitude, dual_route_balance │ ║
║ │ Layer P (Present): current_entrainment, current_wm_load │ ║
║ │ Layer F (Future): performance_predict, adaptation_predict │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Sares 2023** | EEG (SS-EP) + behavioral | 48 | SS-EP amplitude predicts worse tapping performance | β = -0.060 | **f01_entrainment_strength**: paradoxical negative |
| 2 | **Sares 2023** | EEG (SS-EP) + behavioral | 48 | WM (counting span) predicts better tapping | β = +0.068 | **f02_wm_capacity**: cognitive control benefit |
| 3 | **Sares 2023** | EEG (SS-EP) + behavioral | 48 | Entrainment and WM are independent predictors | dissociated | **f04_dissociation_index**: dual-route independence |
| 4 | **Noboa 2025** | EEG (SS-EP) + behavioral | 30 | **EXACT REPLICATION**: identical regression β=-0.060 SS-EP, β=+0.068 WM | R² = 0.316, F(2,27)=6.235, p=.006 | Replication of all core coefficients |
| 5 | **Noboa 2025** | EEG (SS-EP) + behavioral | 30 | Tapping asynchrony predicted by SS-EP alone | F(1,28)=5.486, p=.027, R²=0.164, β=0.009 | Asynchrony route distinct from consistency |
| 6 | **Noboa 2025** | EEG (SS-EP) + behavioral | 30 | Musical background NOT significant predictor of tapping | n.s. | Expertise does NOT mediate the dissociation |
| 7 | **Scartozzi 2024** | EEG (beta/gamma), passive | 57 | Spontaneous beat processing: beta r=0.42 with musicality perceptual abilities (Bonferroni survives) | r = 0.42, p = .001; R² = 0.31 model | Beat processing neural markers ≠ rhythm discrimination (which has WM component) — supports dissociation |
| 8 | **Zanto 2022** | EEG, RCT, 8-wk rhythm training | 37 | Rhythm training improves STM via shared WM resources in SPL (MNI: 10, -45, 70), NOT sensory/attention | group×session F(1,35)=5.46, p=.025, d=0.52 | WM route is trainable and transferable; SPL as WM hub |
| 9 | **Lenoir 2025** | EEG + tapping | N/A | Auditory-specific beat periodization: acoustic>tactile for beat representation | acoustic d = 1.648 beat enhancement | Entrainment route is modality-specific (acoustic); constrains cross-modal generalization |
| 10 | **Pesnot Lerousseau 2021** | iEEG + MEG, passive | N/A | Low-frequency (2.5Hz) oscillations do NOT persist after stimulus offset; only high-γ persistent | Damped oscillator model | **CONSTRAINS**: SS-EP reflects stimulus-locked response, not autonomous oscillation; over-entrainment = over-tracking |
| 11 | **Grahn & Brett 2007** | fMRI | 27 | Putamen and SMA activated for beat-based rhythms | Putamen Z=5.67, SMA Z=5.03 | Motor entrainment circuit (Route 1 downstream) |
| 12 | **Ding 2025** | EEG + behavioral | 37 | All 12 rates (1-12Hz) entrain; entrainment strength correlates with valence/dominance changes | frequency-specific entrainment | Entrainment is robust across frequencies; emotional modulation via entrainment |

#### 3.1.1 Convergence Assessment

The NEWMD dual-route dissociation is supported by **8 converging methods**:

1. **EEG SS-EP + regression** (Sares 2023, Noboa 2025): Direct measurement of entrainment strength and its paradoxical negative prediction of tapping performance
2. **EEG SS-EP + counting span** (Sares 2023, Noboa 2025): WM capacity independently predicts better tapping
3. **EEG passive beta/gamma** (Scartozzi 2024): Spontaneous beat processing correlates with musicality but NOT rhythm discrimination (which loads on WM)
4. **RCT with EEG** (Zanto 2022): Rhythm training selectively improves WM encoding/maintenance via SPL, not sensory/attention
5. **EEG + tapping cross-modal** (Lenoir 2025): Auditory-specific beat periodization shows entrainment is modality-dependent
6. **iEEG + MEG passive** (Pesnot Lerousseau 2021): Low-frequency entrainment is stimulus-locked, not persistent — constrains over-entrainment mechanism
7. **fMRI** (Grahn & Brett 2007): Putamen/SMA circuit for beat-specific processing
8. **EEG frequency-domain** (Ding 2025): Broad entrainment across rates with emotion modulation

#### 3.1.2 Noboa 2025 Replication Qualification

The Noboa et al. (2025, Scientific Reports 15:10466) replication is **extraordinary** in its precision: the regression coefficients for both SS-EP (β=-0.060) and WM counting span (β=+0.068) are IDENTICAL to Sares 2023, despite a completely independent sample (N=30 vs N=48). The full regression equation is replicated:

```
Tapping consistency = 0.52 + (−0.060 × unsyncopated SS-EP) + (0.068 × counting span)
```

Additional Noboa 2025 findings:
- SS-EP ANOVA: Frequency of interest F(1,29)=148.618, p<.001, η²=0.199
- Unsyncopated SS-EP × tapping consistency: r=-0.449* (negative paradox confirmed)
- Counting span × tapping consistency: r=0.378* (positive WM effect confirmed)
- Musical background: NOT a significant predictor (expertise does not mediate the dissociation)
- Tapping asynchrony: F(1,28)=5.486, p=.027, R²=0.164 — separate route for timing precision vs consistency

**Quality upgrade**: With exact replication, the dual-route dissociation moves from "novel single-study finding" to "replicated phenomenon." However, both studies used very similar paradigms (SS-EP + counting span + tapping), so the replication is methodologically narrow. Independent paradigm replication (e.g., fMRI dual-task, TMS disruption) would further strengthen the case.

#### 3.1.3 Dissociation Mechanism: Over-Entrainment as Rigidity

The paradoxical negative β for entrainment is mechanistically clarified by converging evidence:

- **Pesnot Lerousseau 2021**: Low-frequency entrainment does NOT persist — it is stimulus-locked tracking, not autonomous oscillation. This suggests over-entrainment = excessive stimulus tracking, reducing flexibility.
- **Scartozzi 2024**: Neural beat correlates (automatic, passive) do NOT predict rhythm discrimination (which requires WM-mediated cognitive control). The two routes access different cognitive resources.
- **Zanto 2022**: Rhythm training selectively improves WM encoding/maintenance via SPL, not sensory entrainment. This confirms the WM route is the trainable, beneficial route.
- **Lenoir 2025**: Acoustic entrainment produces behaviour-relevant periodized representation; tactile does not. The entrainment route is modality-specific and automatic.

### 3.2 The Entrainment Paradox

```
THE DUAL-ROUTE MODEL OF RHYTHM PRODUCTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Route Brain Pathway Effect Interpretation
────────────────────────────────────────────────────────────────────────
Automatic Aud. Cortex → Cerebellum β = -0.060 Over-entrainment
Entrainment (SS-EP phase-locking) reduces flexibility

Cognitive DLPFC → Premotor Cortex β = +0.068 WM provides flexible
Control (WM) (counting span capacity) temporal control

Net Performance = Entrainment_effect + WM_effect + ε
 = (-0.060 · SS_EP) + (0.068 · WM_span) + ε

Paradox Explanation:
 Strong SS-EP = rigid phase-locking to simple beat structure
 This rigidity REDUCES ability to adapt timing when needed
 WM provides FLEXIBILITY that rigid entrainment lacks
 Both routes operate INDEPENDENTLY (no interaction term)
```

### 3.3 Effect Size Summary

```
CORE DUAL-ROUTE COEFFICIENTS (REPLICATED):
─────────────────────────────────────────────────────────────────────
 Sares 2023 Noboa 2025
 (N=48) (N=30, REPLICATION)
Entrainment Effect (SS-EP): β = -0.060 β = -0.060 (IDENTICAL)
WM Effect (counting span): β = +0.068 β = +0.068 (IDENTICAL)
Model R²: not reported R² = 0.316
Regression F: not reported F(2,27) = 6.235, p=.006

SUPPORTING EFFECT SIZES:
─────────────────────────────────────────────────────────────────────
Noboa 2025 SS-EP × consistency: r = -0.449* (paradoxical negative)
Noboa 2025 WM span × consistency: r = 0.378* (beneficial positive)
Noboa 2025 tapping asynchrony: R² = 0.164, β = 0.009 (separate route)
Scartozzi 2024 beta × musicality: r = 0.42, p = .001 (spontaneous beat)
Scartozzi 2024 beta → rhythm disc: n.s. (dissociation confirmed)
Zanto 2022 rhythm → STM transfer: d = 0.52, ηp² = 0.13 (WM route trainable)
Lenoir 2025 acoustic beat enhance: d = 1.648 (auditory-specific)
Grahn & Brett 2007 putamen: Z = 5.67 (beat-specific motor circuit)
Grahn & Brett 2007 SMA: Z = 5.03 (beat-specific motor circuit)

Quality Assessment: γ-tier (replicated in 2 studies, but same paradigm;
 awaits independent paradigm replication)
Replication: EXACT REPLICATION by Noboa 2025 (identical β values)
 Convergent support from 8 methods (§3.1.1)
 Constrained by Pesnot Lerousseau 2021 (no persistent
 low-freq entrainment) and Scartozzi 2024 (automatic
 beat ≠ WM-loaded rhythm discrimination)
```

---

## 4. R³ Input Mapping: What NEWMD Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | NEWMD Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Beat intensity for entrainment | SS-EP tracks intensity envelope |
| **B: Energy** | [8] | loudness | Perceptual beat salience | Stevens 1957: power law |
| **B: Energy** | [9] | spectral_centroid | Beat spectral profile | Timbre of beat events |
| **B: Energy** | [10] | spectral_flux | Beat onset detection | Onset precision for entrainment |
| **B: Energy** | [11] | onset_strength | Event boundary marking | Phase-locking target |
| **D: Change** | [21] | spectral_change | Beat-to-beat spectral dynamics | Entrainment flexibility demand |
| **D: Change** | [22] | energy_change | Intensity dynamics | Tempo adaptation signal |
| **D: Change** | [23] | pitch_change | Melodic contour dynamics | WM encoding complexity |
| **D: Change** | [24] | timbre_change | Timbral evolution | Context complexity for WM |
| **A: Consonance** | [0:7] | all consonance (7D) | Harmonic context richness | temporal-context context complexity |
| **C: Timbre** | [12:21] | all timbre (9D) | Spectral complexity for WM | Richer timbre → more WM demand |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Foundation×Perceptual coupling | Cross-domain integration for WM |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ v2 Group | Index | Feature | NEWMD Role | Scientific Basis |
|-------------|-------|---------|-----------|------------------|
| **G: Rhythm** | [66] | beat_strength | Beat salience for temporal expectation generation | Large & Palmer 2002 |
| **G: Rhythm** | [67] | pulse_clarity | Pulse ambiguity level modulating prediction confidence | Witek 2014 |

**Rationale**: NEWMD models neural expectation and working memory dynamics. G[66] beat_strength provides beat salience that drives temporal expectation formation, and G[67] pulse_clarity indicates how clearly the pulse is perceived, modulating prediction confidence.

**Code impact** (Phase 6): `r3_indices` will be extended to include `[66, 67]`.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[7] amplitude ──────────────┐
R³[10] spectral_flux ─────────┼──► Entrainment Strength (SS-EP proxy)
R³[11] onset_strength ────────┘ beat_induction at H6 (200ms)
 Math: E = σ(α₁ · onset · flux ·
 beat[mean])
 Paradox: high E → β = -0.060

R³[8] loudness ────────────────┐
R³[9] spectral_centroid ───────┼──► Motor Entrainment (coupling)
R³[21] spectral_change ────────┘ motor_entrainment at H16 (1000ms)
 Math: M = σ(α₂ · loudness ·
 motor[mean])

R³[22] energy_change ──────────┐
R³[23] pitch_change ───────────┤
R³[0:7] consonance (7D) ──────┼──► WM Capacity (cognitive control)
R³[12:21] timbre (9D) ────────┘ short_context at H8 (300ms)
 medium_context at H14 (700ms)
 Math: W = σ(β₁ · context_complexity ·
 short[mean])
 Benefit: high W → β = +0.068

R³[25:33] x_l0l5 (8D) ────────── Flexibility / Adaptation
 long_context at H20 (5000ms)
 Math: F = σ(γ₁ · coupling_var ·
 long[entropy])

── R³ v2 (Phase 6) ──────────────────────────────────────────────
R³[66] beat_strength ──────────── Beat salience → temporal expectation
R³[67] pulse_clarity ──────────── Pulse ambiguity → prediction confidence
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

NEWMD requires H³ features at both horizons (H6, H11, H16) and Temporal hierarchy horizons (H8, H14, H20). The dual-scale demand reflects the dual-route model: beat-entrainment captures automatic entrainment, temporal-context captures working memory context.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 7 | amplitude | 6 | M0 (value) | L0 (fwd) | Current beat intensity |
| 10 | spectral_flux | 6 | M4 (max) | L0 (fwd) | Peak onset in beat window |
| 11 | onset_strength | 6 | M0 (value) | L0 (fwd) | Current beat onset |
| 11 | onset_strength | 11 | M14 (periodicity) | L0 (fwd) | Beat regularity (SS-EP proxy) |
| 8 | loudness | 16 | M1 (mean) | L0 (fwd) | Mean loudness over bar |
| 9 | spectral_centroid | 16 | M15 (smoothness) | L0 (fwd) | Beat smoothness for groove |
| 21 | spectral_change | 11 | M8 (velocity) | L0 (fwd) | Tempo dynamics at psychological present |
| 21 | spectral_change | 11 | M17 (peaks) | L0 (fwd) | Beat count per window |
| 22 | energy_change | 8 | M1 (mean) | L0 (fwd) | Short-term intensity dynamics |
| 22 | energy_change | 14 | M13 (entropy) | L0 (fwd) | Context unpredictability (WM load) |
| 23 | pitch_change | 8 | M3 (std) | L0 (fwd) | Pitch variability (WM complexity) |
| 23 | pitch_change | 14 | M1 (mean) | L0 (fwd) | Mean pitch dynamics (WM context) |
| 25 | x_l0l5[0] | 20 | M1 (mean) | L0 (fwd) | Long-term coupling (adaptation) |
| 25 | x_l0l5[0] | 20 | M13 (entropy) | L0 (fwd) | Coupling unpredictability (flexibility) |
| 25 | x_l0l5[0] | 20 | M22 (autocorr) | L0 (fwd) | Self-similarity (routine vs novel) |
| 33 | x_l4l5[0] | 20 | M19 (stability) | L0 (fwd) | Temporal stability for adaptation |

**v1 demand**: 16 tuples

#### R³ v2 Projected Expansion

NEWMD projected v2 features from G:Rhythm, aligned with corresponding H³ horizons.

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 66 | beat_strength | G | 6 | M0 (value) | L0 | Instantaneous beat salience |
| 66 | beat_strength | G | 16 | M0 (value) | L0 | Bar-level beat salience |
| 67 | pulse_clarity | G | 6 | M0 (value) | L0 | Current pulse clarity at beat scale |
| 67 | pulse_clarity | G | 11 | M1 (mean) | L0 | Mean pulse clarity at meter scale |

**v2 projected**: 4 tuples
**Total projected**: 20 tuples of 294,912 theoretical = 0.0068%

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
NEWMD OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
Manifold Range: STU NEWMD [209:219]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0 │ f01_entrainment │ [0, 1] │ Automatic entrainment strength (SS-EP
 │ _strength │ │ proxy). Phase-locked response to beat.
 │ │ │ HIGH value = strong SS-EP = rigid coupling.
 │ │ │ f01 = σ(0.30 · onset_val · flux_peak ·
 │ │ │ beat_mean + 0.20 · periodicity)
────┼───────────────────┼────────┼────────────────────────────────────────────
 1 │ f02_wm_capacity │ [0, 1] │ Working memory capacity proxy.
 │ │ │ Flexible temporal representation.
 │ │ │ HIGH value = high WM = better performance.
 │ │ │ f02 = σ(0.25 · context_complexity ·
 │ │ │ short_mean + 0.20 · pitch_std)
────┼───────────────────┼────────┼────────────────────────────────────────────
 2 │ f03_flexibility │ [0, 1] │ Temporal flexibility: inverse of entrainment
 │ _cost │ │ rigidity. The "cost" of over-entrainment.
 │ │ │ f03 = σ(0.25 · (1 - f01) · motor_mean
 │ │ │ + 0.25 · long_entropy)
────┼───────────────────┼────────┼────────────────────────────────────────────
 3 │ f04_dissociation │ [0, 1] │ Degree of independence between routes.
 │ _index │ │ High when entrainment and WM contribute
 │ │ │ unequally (one dominates).
 │ │ │ f04 = |f01 - f02| (absolute difference)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 4 │ paradox_magnitude │ [0, 1] │ Magnitude of the entrainment paradox.
 │ │ │ High when strong entrainment co-occurs
 │ │ │ with low flexibility.
 │ │ │ paradox = f01 · (1 - f03)
────┼───────────────────┼────────┼────────────────────────────────────────────
 5 │ dual_route_balance│ [0, 1] │ Balance between automatic and cognitive.
 │ │ │ 0.5 = equal contribution, 0/1 = one
 │ │ │ route dominates.
 │ │ │ balance = σ(0.50 · f01 + 0.50 · f02)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 6 │ current_entrain │ [0, 1] │ Instantaneous entrainment level.
 │ │ │ beat_induction aggregation.
────┼───────────────────┼────────┼────────────────────────────────────────────
 7 │ current_wm_load │ [0, 1] │ Current working memory engagement.
 │ │ │ short_context + medium_context.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 8 │ performance_pred │ [0, 1] │ Predicted tapping performance.
 │ │ │ Net effect: WM benefit minus entrainment
 │ │ │ cost.
 │ │ │ perf = σ(0.35 · f02 - 0.30 · paradox
 │ │ │ + 0.25 · f03)
────┼───────────────────┼────────┼────────────────────────────────────────────
 9 │ adaptation_pred │ [0, 1] │ Predicted adaptation to tempo changes.
 │ │ │ Coupling stability and WM capacity.
 │ │ │ adapt = σ(0.40 · stability_long
 │ │ │ + 0.30 · f02)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Dual-Route Rhythm Production Function

```
Dual-Route Rhythm Production:

 Performance = f(Entrainment, WM, Flexibility)

 Route 1 — Automatic Entrainment ():
 Entrainment = σ(α₁ · Onset · Flux_peak · beat + α₂ · Periodicity)
 |α₁| + |α₂| = 0.50 (≤ 1.0, saturation rule)
 Paradox: high Entrainment → β = -0.060 (negative contribution)

 Route 2 — Cognitive Control ():
 WM_Capacity = σ(β₁ · Context_Complexity · short + β₂ · Pitch_std)
 |β₁| + |β₂| = 0.45 (≤ 1.0, saturation rule)
 Benefit: high WM → β = +0.068 (positive contribution)

 Flexibility:
 Flex = σ(γ₁ · (1 - Entrainment) · motor + γ₂ · long_entropy)
 |γ₁| + |γ₂| = 0.50 (≤ 1.0, saturation rule)

 Net Performance:
 perf = σ(δ₁ · WM - δ₂ · Paradox + δ₃ · Flex)
 |δ₁| + |δ₂| + |δ₃| = 0.90 (≤ 1.0, saturation rule)

 Dissociation:
 dissoc = |Entrainment - WM| (route independence measure)
```

### 7.2 Feature Formulas

```python
# f01: Entrainment Strength (SS-EP proxy, β = -0.060 paradox)
onset_val = h3[(11, 6, 0, 0)] # onset_strength value at H6
flux_peak = h3[(10, 6, 4, 0)] # spectral_flux max at H6
periodicity = h3[(11, 11, 14, 0)] # onset periodicity at H11
f01 = σ(0.30 · onset_val · flux_peak
 + 0.20 · periodicity)
# |0.30| + |0.20| = 0.50 ≤ 1.0 ✓

# f02: WM Capacity (cognitive control, β = +0.068 benefit)
energy_chg_mean = h3[(22, 8, 1, 0)] # energy_change mean at H8
pitch_std = h3[(23, 8, 3, 0)] # pitch_change std at H8
f02 = σ(0.25 · energy_chg_mean
 + 0.20 · pitch_std)
# |0.25| + |0.20| = 0.45 ≤ 1.0 ✓

# f03: Flexibility Cost (inverse of rigid entrainment)
long_entropy = h3[(25, 20, 13, 0)] # x_l0l5 entropy at H20
f03 = σ(0.25 · (1 - f01) · motor_mean
 + 0.25 · long_entropy)
# |0.25| + |0.25| = 0.50 ≤ 1.0 ✓

# f04: Dissociation Index (route independence)
f04 = abs(f01 - f02)
# No sigmoid needed — |diff| is already [0, 1]

# ═══ LAYER M ═══

# paradox_magnitude: strong entrainment + low flexibility
paradox = f01 · (1 - f03)

# dual_route_balance: σ ensures [0,1] output
balance = σ(0.50 · f01 + 0.50 · f02)
# |0.50| + |0.50| = 1.0 ≤ 1.0 ✓

# ═══ LAYER P ═══

# current_entrainment: beat-entrainment aggregation

# current_wm_load: temporal-context aggregation
# |0.50| + |0.50| = 1.0 ≤ 1.0 ✓

# ═══ LAYER F ═══

# performance_predict: net effect of dual routes
stability_long = h3[(33, 20, 19, 0)] # x_l4l5 stability at H20
perf = σ(0.35 · f02 - 0.30 · paradox + 0.25 · f03)
# |0.35| + |0.30| + |0.25| = 0.90 ≤ 1.0 ✓

# adaptation_predict: flexibility + WM for tempo changes
adapt = σ(0.40 · stability_long + 0.30 · f02)
# |0.40| + |0.30| = 0.70 ≤ 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | NEWMD Function |
|--------|-----------------|----------|---------------|---------------|
| **Auditory Cortex** | ±55, -22, 10 | Direct | EEG SS-EP (Sares 2023, Noboa 2025) | Automatic entrainment (Route 1) — SS-EP generation |
| **SMA** | 0, -5, 55 | Direct | fMRI (Grahn & Brett 2007, Z=5.03) | Beat-specific motor circuit |
| **Putamen L** | -20, 4, 4 | Direct | fMRI (Grahn & Brett 2007, Z=5.67) | Beat entrainment subcortical hub |
| **Putamen R** | 20, 4, 4 | Direct | fMRI (Grahn & Brett 2007) | Beat entrainment subcortical hub |
| **Superior Parietal Lobule R** | 10, -45, 70 | Direct | EEG source (Zanto 2022, RCT) | WM encoding/maintenance (Route 2) |
| **Cerebellum** | ±20, -65, -30 | Indirect | Literature | Motor timing precision |
| **Premotor Cortex** | ±45, 0, 50 | Indirect | Literature | Sensorimotor integration |
| **DLPFC** | ±42, 36, 26 | Indirect | Literature | Working memory control (Route 2) |
| **STG** | ±60, -5, -5 | Indirect | EEG topography (Scartozzi 2024, central) | Beat processing relay |
| **Pre-SMA** | 0, 10, 50 | Indirect | Literature (Grahn beat network) | Internal beat generation |

---

## 9. Cross-Unit Pathways

### 9.1 NEWMD ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ NEWMD INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ INTRA-UNIT (STU): │
│ AMSC.motor_coupling ──────► NEWMD (coupling strength as entrainment base)│
│ NEWMD.flexibility_cost ───► EDTA (flexibility limits tempo accuracy) │
│ NEWMD.entrainment_strength → HGSIC (entrainment feeds groove) │
│ HMCE.context_depth ───────► NEWMD.wm_capacity (context enriches WM) │
│ │
│ CROSS-UNIT (P4: STU internal): │
│ beat_induction ↔ NEWMD.entrainment (r ~ -0.060 with performance) │
│ context_depth ↔ NEWMD.wm_capacity (r ~ +0.068 with performance) │
│ │
│ CROSS-UNIT (P5: STU → IMU): │
│ NEWMD.wm_capacity ──► IMU (working memory links to episodic encoding) │
│ │
│ CROSS-UNIT (P5: STU → ARU): │
│ NEWMD.dual_route_balance ──► ARU (route balance affects groove affect) │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **SS-EP negative effect** | Stronger SS-EP should predict worse (not better) tapping in simple rhythms | **CONFIRMED** — Sares 2023 β=-0.060, Noboa 2025 β=-0.060 (exact replication) |
| **WM positive effect** | Higher counting span should predict better tapping, independent of SS-EP | **CONFIRMED** — Sares 2023 β=+0.068, Noboa 2025 β=+0.068 (exact replication) |
| **Dissociation** | SS-EP and WM should show no significant interaction term (independent routes) | **CONFIRMED** — both studies find independent predictors; Scartozzi 2024 shows neural beat ≠ rhythm discrimination |
| **Replication** | Core coefficients should replicate in independent sample | **CONFIRMED** — Noboa 2025 N=30 produces identical β values to Sares 2023 N=48 |
| **WM route trainable** | WM-based temporal processing should be improvable through training | **CONFIRMED** — Zanto 2022 rhythm training improves STM d=0.52 via SPL, not sensory/attention |
| **Entrainment not persistent** | SS-EP should be stimulus-locked, not autonomous oscillation at beat frequency | **CONFIRMED** — Pesnot Lerousseau 2021: low-freq entrainment does not persist after stimulus offset |
| **Auditory-specific entrainment** | Beat-related entrainment periodization should be auditory-specific | **CONFIRMED** — Lenoir 2025: acoustic but not tactile rhythm produces periodized neural representation |
| **Complex rhythms** | Paradox may reverse for complex rhythms (entrainment beneficial when rhythm is unpredictable) | Testable |
| **TMS/lesion dissociation** | Disrupting DLPFC should impair WM route without affecting SS-EP; disrupting auditory cortex should affect SS-EP without affecting WM | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class NEWMD(BaseModel):
 """Neural Entrainment-Working Memory Dissociation.

 Output: 10D per frame.
 Reads: R³ + H³ direct.
 Dual-route model: beat-entrainment = automatic entrainment, temporal-context = cognitive control.
 """
 NAME = "NEWMD"
 UNIT = "STU"
 TIER = "γ2"
 OUTPUT_DIM = 10
 # Coefficient saturation rule: |wᵢ| must sum ≤ 1.0 per sigmoid
 ALPHA_1 = 0.30 # Entrainment onset × flux × beat-entrainment weight
 ALPHA_2 = 0.20 # Entrainment periodicity weight
 BETA_1 = 0.25 # WM context × temporal-context weight
 BETA_2 = 0.20 # WM pitch variability weight
 GAMMA_1 = 0.25 # Flexibility (1-entrainment) × motor weight
 GAMMA_2 = 0.25 # Flexibility temporal-context entropy weight
 DELTA_1 = 0.35 # Performance: WM contribution
 DELTA_2 = 0.30 # Performance: paradox penalty
 DELTA_3 = 0.25 # Performance: flexibility contribution

 # Sares 2023 regression coefficients
 ENTRAIN_BETA = -0.060 # Paradoxical negative effect
 WM_BETA = 0.068 # Beneficial positive effect

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """16 tuples for NEWMD computation."""
 return [
 # (r3_idx, horizon, morph, law)
 # beat-entrainment route — Entrainment (H6, H11, H16)
 (7, 6, 0, 0), # amplitude, value, forward
 (10, 6, 4, 0), # spectral_flux, max, forward
 (11, 6, 0, 0), # onset_strength, value, forward
 (11, 11, 14, 0), # onset_strength, periodicity, forward
 (8, 16, 1, 0), # loudness, mean, forward
 (9, 16, 15, 0), # spectral_centroid, smoothness, forward
 (21, 11, 8, 0), # spectral_change, velocity, forward
 (21, 11, 17, 0), # spectral_change, peaks, forward
 # temporal-context route — Working Memory (H8, H14, H20)
 (22, 8, 1, 0), # energy_change, mean, forward
 (22, 14, 13, 0), # energy_change, entropy, forward
 (23, 8, 3, 0), # pitch_change, std, forward
 (23, 14, 1, 0), # pitch_change, mean, forward
 (25, 20, 1, 0), # x_l0l5[0], mean, forward
 (25, 20, 13, 0), # x_l0l5[0], entropy, forward
 (25, 20, 22, 0), # x_l0l5[0], autocorrelation, forward
 (33, 20, 19, 0), # x_l4l5[0], stability, forward
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 """
 Compute NEWMD 10D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) → (B,T) scalars
 r3: (B,T,49) raw R³ features

 Returns:
 (B,T,10) NEWMD output
 """
 # ═══ LAYER E: Explicit features ═══

 # f01: Entrainment Strength (SS-EP proxy, paradoxical β=-0.060)
 onset_val = h3_direct[(11, 6, 0, 0)].unsqueeze(-1)
 flux_peak = h3_direct[(10, 6, 4, 0)].unsqueeze(-1)
 periodicity = h3_direct[(11, 11, 14, 0)].unsqueeze(-1)
 f01 = torch.sigmoid(
 self.ALPHA_1 * onset_val * flux_peak
 + self.ALPHA_2 * periodicity
 ) # |0.30| + |0.20| = 0.50 ≤ 1.0 ✓

 # f02: WM Capacity (cognitive control, β=+0.068)
 energy_chg_mean = h3_direct[(22, 8, 1, 0)].unsqueeze(-1)
 pitch_std = h3_direct[(23, 8, 3, 0)].unsqueeze(-1)
 f02 = torch.sigmoid(
 self.BETA_1 * energy_chg_mean
 + self.BETA_2 * pitch_std
 ) # |0.25| + |0.20| = 0.45 ≤ 1.0 ✓

 # f03: Flexibility Cost (rigidity penalty)
 long_entropy = h3_direct[(25, 20, 13, 0)].unsqueeze(-1)
 f03 = torch.sigmoid(
 self.GAMMA_1 * (1 - f01)
 + self.GAMMA_2 * long_entropy
 ) # |0.25| + |0.25| = 0.50 ≤ 1.0 ✓

 # f04: Dissociation Index (route independence)
 f04 = torch.abs(f01 - f02)

 # ═══ LAYER M: Mathematical ═══

 # Paradox magnitude: strong entrainment + low flexibility
 paradox = f01 * (1 - f03)

 # Dual-route balance
 balance = torch.sigmoid(
 0.50 * f01 + 0.50 * f02
 ) # |0.50| + |0.50| = 1.0 ≤ 1.0 ✓

 # ═══ LAYER P: Present ═══

 # Current entrainment level

 # Current WM load
 current_wm_load = torch.sigmoid(
 ) # |0.50| + |0.50| = 1.0 ≤ 1.0 ✓

 # ═══ LAYER F: Future ═══

 # Performance prediction (net dual-route effect)
 perf = torch.sigmoid(
 self.DELTA_1 * f02
 - self.DELTA_2 * paradox
 + self.DELTA_3 * f03
 ) # |0.35| + |0.30| + |0.25| = 0.90 ≤ 1.0 ✓

 # Adaptation prediction
 stability_long = h3_direct[(33, 20, 19, 0)].unsqueeze(-1)
 adapt = torch.sigmoid(
 0.40 * stability_long + 0.30 * f02
 ) # |0.40| + |0.30| = 0.70 ≤ 1.0 ✓

 return torch.cat([
 f01, f02, f03, f04, # E: 4D
 paradox, balance, # M: 2D
 current_entrain, current_wm_load, # P: 2D
 perf, adapt, # F: 2D
 ], dim=-1) # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 | 7 Tier 1 + 3 Tier 2 + 2 Tier 3 |
| **Effect Sizes** | β = -0.060 (SS-EP), β = +0.068 (WM) — **REPLICATED** | Sares 2023 + Noboa 2025 (identical) |
| **Evidence Modality** | EEG (SS-EP), fMRI, RCT-EEG, iEEG+MEG, behavioral | Multi-method (8 converging) |
| **Falsification Tests** | 7/9 confirmed | 2 testable (complex rhythms, TMS dissociation) |
| **R³ Features Used** | 33D of 49D | Consonance + Energy + Timbre + Change + Interactions |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **Output Dimensions** | **10D** | 4-layer structure |

---

## 13. Scientific References

### Tier 1: Direct quantitative evidence (in collection)

1. **Sares, A. G., et al. (2023)**. Neural entrainment to beat and working memory contribute independently to rhythm production. *Cognitive, Affective, & Behavioral Neuroscience*. (EEG + behavioral, N=48, SS-EP β=-0.060, WM β=+0.068, independent predictors — founding study)
2. **Noboa, G. N., et al. (2025)**. Neural entrainment to the beat: Steady-state evoked potentials and working memory predict tapping consistency. *Scientific Reports*, 15:10466. (EEG + behavioral, N=30, **EXACT REPLICATION**: β=-0.060 SS-EP, β=+0.068 WM, R²=0.316, F(2,27)=6.235)
3. **Scartozzi, A. C., et al. (2024)**. The neural correlates of spontaneous beat processing and its relationship with music-related characteristics. *eNeuro*, 11(10). (EEG passive, N=57, beta r=0.42 with musicality, NOT rhythm discrimination — supports dissociation)
4. **Zanto, T. P., et al. (2022)**. How musical rhythm training improves short-term memory for faces. *PNAS*, 119(41), e2201655119. (RCT EEG, N=37, group×session F(1,35)=5.46, p=.025, d=0.52, SPL MNI: 10,-45,70 — WM route trainable)
5. **Lenoir, C., et al. (2025)**. Behavior-relevant periodized neural representation of acoustic but not tactile rhythm in humans. *Journal of Neuroscience*. (EEG + tapping, acoustic d=1.648 beat enhancement, tactile n.s. — auditory-specific entrainment)
6. **Pesnot Lerousseau, J., et al. (2021)**. Frequency selectivity of persistent cortical oscillatory responses to auditory rhythmic stimulation. *Journal of Neuroscience*, 41(38), 7991-8006. (iEEG + MEG passive, low-freq NOT persistent — CONSTRAINS entrainment persistence)
7. **Grahn, J. A., & Brett, M. (2007)**. Rhythm and beat perception in motor areas of the brain. *Journal of Cognitive Neuroscience*, 19(5), 893-906. (fMRI, N=27, putamen Z=5.67, SMA Z=5.03 — beat-specific motor circuit)

### Tier 2: Supporting/review evidence (in collection)

8. **Ding, J., et al. (2025)**. Entrainment of rhythmic tonal sequences on neural oscillations and the impact on subjective emotion. *Scientific Reports*, 15:17462. (EEG + behavioral, N=37, all 12 rates entrain, entrainment × emotion)
9. **Ross, J. M., & Balasubramaniam, R. (2022)**. Time perception for musical rhythms: Sensorimotor perspectives. *Music Perception*, 40(2), 89-110. (Review: entrainment, simulation, prediction frameworks)
10. **Dalla Bella, S., et al. (2024)**. Unravelling individual rhythmic abilities using machine learning. *npj Science of Learning*, 9:13. (ML classification, N=79, musician d=1.8 — rhythmic ability multidimensional)

### Tier 3: Founding/historical (NOT in collection)

11. **Large, E. W., & Jones, M. R. (1999)**. The dynamics of attending: How people track time-varying events. *Psychological Review*, 106(1), 119-159. (Founding theory: dynamic attending, oscillatory entrainment)
12. **Grahn, J. A., & Schuit, D. (2012)**. Individual differences in rhythmic ability: Behavioral and neuroimaging investigations. *Psychomusicology*, 22(2), 105-121. (WM and timing; convergent context)

### Code Note (Phase 5)

The mi_beta code file (`newmd.py`) has several mismatches with this document:
- Code cites Nave-Blodgett 2021 + Grahn 2009 vs doc cites Sares 2023 + Noboa 2025 as primary
- Code dimension names differ (e.g., `f01_entrainment_strength` vs `entrainment_wm_dissociation`)
- Code `version="2.0.0"`, `paper_count=3` → needs update to `"2.1.0"`, `paper_count=12`
- These mismatches will be resolved in Phase 5 (mi_beta code update).

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D): L0, L3, L4, L5, L6, L9, X_L0L1, X_L4L5 | R³ (49D): Consonance, Energy, Timbre, Change, Interactions |
| Entrainment route | L3.coherence + X_L0L1 via NPL+GRV | beat_induction via beat-entrainment H³ |
| WM route | X_L4L5 via ITM+EFC | short_context via temporal-context H³ |
| Statistics | S⁰.L9 (std, entropy) | H³ morphs (M0, M1, M3, M4, M13, M14, M15, M17, M19, M22) |
| Cross-feature | X_L0L1[128:136] (entrainment), X_L4L5[192:200] (WM) | R³.x_l0l5[25:33], x_l4l5[33:41] |
| Demand format | HC⁰ index ranges (15 tuples, 0.65%) | H³ 4-tuples (16 tuples, 0.69%) |
| Output dimensions | 11D (legacy) | **10D** (catalog value) |
| Mechanisms | NPL+ITM+GRV+EFC (4 separate HC⁰) | H³ direct (2 unified mechanisms) |

---

**Model Status**: **EXPLORATORY** (substantially strengthened by Noboa 2025 exact replication; dual-route dissociation now a replicated phenomenon, though both studies use same paradigm; independent paradigm replication would support upgrade to β-tier)
**Output Dimensions**: **10D**
**Evidence Tier**: **γ (Speculative)** — retained because both direct studies use the same SS-EP+counting-span+tapping paradigm; broader methodological replication needed for β-tier
**Confidence**: **<70%** (upper end of γ range; core coefficients replicated but mechanistic interpretation awaits causal evidence)
