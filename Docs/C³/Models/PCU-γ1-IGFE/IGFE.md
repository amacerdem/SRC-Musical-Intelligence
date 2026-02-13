# PCU-γ1-IGFE: Individual Gamma Frequency Enhancement

**Model**: Individual Gamma Frequency Enhancement
**Unit**: PCU (Predictive Coding Unit)
**Circuit**: Imagery (Auditory Cortex, IFG, STS, Hippocampus)
**Tier**: γ (Integrative) — 50-70% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added I:Information feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/PCU-γ1-IGFE.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Individual Gamma Frequency Enhancement** (IGFE) model proposes that auditory stimulation at an individual's peak gamma frequency enhances cognitive performance (memory, executive control).

```
INDIVIDUAL GAMMA FREQUENCY ENHANCEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUDITORY INPUT                          COGNITIVE OUTPUT
──────────────                          ─────────────────
Music with spectral energy              Enhanced performance
matching individual gamma freq          (memory, executive control)

  Stimulus ────► IGF Match ────► Gamma ────► Cognitive
  Frequency      Assessment     Entrainment   Enhancement

┌──────────────────────────────────────────────────────────────────┐
│             IGF STIMULATION PATHWAY (Yokota 2025)                │
│                                                                  │
│  Step 1: Identify individual peak gamma frequency (30-80 Hz)    │
│  Step 2: Present auditory stimulation at IGF                    │
│  Step 3: Gamma oscillations entrain to stimulus                 │
│  Step 4: Enhanced memory (word recall) + executive control (IES)│
│                                                                  │
│  DOSE-RESPONSE:                                                 │
│    Brief (5 min):  Minimal enhancement                          │
│    Full (15 min):  Maximal enhancement                          │
└──────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Auditory stimulation at an individual's peak gamma
frequency (30-80 Hz) enhances cognitive performance through
frequency-specific entrainment. The enhancement shows a dose-response
relationship: longer exposure yields greater benefits.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why IGFE Matters for PCU

IGFE extends predictive coding to frequency-specific neural enhancement:

1. **HTP** (α1) provides hierarchical prediction timing.
2. **PWUP** (β1) modulates PE by contextual precision.
3. **IGFE** (γ1) proposes that gamma-band matching enhances the prediction system itself.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → PPC+TPC+MEM → IGFE)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    IGFE COMPUTATION ARCHITECTURE                            ║
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
║  │                         IGFE reads: ~14D                         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                         IGFE demand: ~18 of 2304 tuples          │        ║
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
║  │                    IGFE MODEL (9D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_igf_match,                             │        ║
║  │                       f02_memory_enhancement,                    │        ║
║  │                       f03_executive_enhancement,                 │        ║
║  │                       f04_dose_response                          │        ║
║  │  Layer P (Present):   gamma_synchronization,                     │        ║
║  │                       dose_accumulation,                         │        ║
║  │                       memory_access                              │        ║
║  │  Layer F (Future):    memory_enhancement_post,                   │        ║
║  │                       executive_improvement_post                 │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Yokota 2025** | EEG + Behavioral | 29 | IGF music → word recall improvement | significant | **f02 memory enhancement** |
| 2 | **Yokota 2025** | EEG + Behavioral | 29 | IGF music → executive control improvement (IES) | significant | **f03 executive enhancement** |
| 3 | **Yokota 2025** | EEG + Behavioral | 29 | Dose-response: longer exposure = better recall | significant | **f04 dose response** |
| 4 | **Bolland et al. 2025** | Systematic Review | 62 studies (2,179 participants) | Auditory gamma stimulation improves cognition; optimal frequency varies 37-48 Hz across individuals; 16 individual differences influence entrainment | k=62 studies; chronic stimulation: maintained/enhanced MoCA, MMSE, ADCS-ADL; reduced brain atrophy (MRI) | **f01 igf match** (individual optimal frequency), **f04 dose response** (chronic > acute) |
| 5 | **Dobri et al. 2023** | MEG + MRS | 38 (19 young + 19 older) | 40 Hz ASSR reflects gamma synchrony with sensory + binding components; left auditory cortex GABA positively correlated with gamma synchrony in quiet; increased gamma in aging linked to poorer SIN performance | R²=0.31 (GABA–gamma), R²=0.34 (gamma–SIN loss), η²=0.36 (age effect on ASSR phase) | **gamma_synchronization** (ASSR mechanism), **f01 igf match** (GABA-dependent optimal frequency) |
| 6 | **Jiao 2025** | Mini Review | Review | 40 Hz gamma entrainment facilitates memory + concentration; multisensory 40 Hz stimulation enhances memory in Alzheimer's; individual variability in gamma response | Narrative (no pooled ES) | **f02 memory enhancement**, **f04 dose response** (therapeutic dosing) |
| 7 | **Noboa et al. 2025** | EEG (64-ch) + Behavioral | 30 | SS-EPs at beat-related frequencies; working memory capacity predicts tapping consistency; fronto-central entrainment topography | R²=0.316 (tapping consistency model) | **memory_access** (WM role in entrainment), **gamma_synchronization** (fronto-central topography) |
| 8 | **Ding et al. 2025** | EEG (64-ch) + Behavioral | 37 (31 analysed) | All 12 tonal rates (1-12 Hz) significantly entrain neural oscillations; >6 Hz stimuli: ITPC correlates with increased valence; frontocentral entrainment | η²=0.14 (ITPC interaction), r=0.22 (ITPC–valence >6 Hz, p=.002) | **gamma_synchronization** (frequency-specific entrainment), **dose_accumulation** (rate-dependent effects) |
| 9 | **Thaut et al. 2015** | Review | Review | Auditory rhythm entrains motor + cognitive systems; temporal scaffolding supports memory rehabilitation; beta/gamma modulation in auditory + motor areas | Narrative (no pooled ES) | **f02 memory enhancement** (entrainment as cognitive rehabilitation) |
| 10 | **Aparicio-Terres et al. 2025** | EEG (36-ch) + Behavioral | 19 | Tempo-driven modulation of neural entrainment; entrainment strength predicts reaction time; fronto-central distribution | R²=0.086 (RT vs entrainment) | **gamma_synchronization** (entrainment-cognition link) |
| 11 | **Bridwell et al. 2017** | EEG (24-ch) | 13 | Cortical entrainment to 4 Hz guitar note patterns; ERP amplitude modulation by musical structure; 8 Hz alpha from 4 Hz input | r=0.65 (175 ms peak correlation with MMN); 45% amplitude increase random vs pattern | **f01 igf match** (frequency-specific cortical entrainment) |
| 12 | **Leeuwis et al. 2021** | EEG (9-ch) + Behavioral | 30 | Neural synchrony (ISC) predicts Spotify streams; alpha-band ISC at central electrodes; gamma activity at fronto-central sites predicts engagement | R²adj=0.40 (ISC → streams at 3 weeks) | **gamma_synchronization** (gamma as engagement predictor) |

### 3.2 Effect Size Summary

```
Primary Evidence (k=12 rows from 10 papers):
  Direct gamma-cognition:   3 papers (Yokota, Bolland, Jiao)
  Gamma mechanisms (ASSR):  2 papers (Dobri, Ding)
  Entrainment-cognition:    3 papers (Noboa, Aparicio-Terres, Thaut)
  Cortical entrainment:     2 papers (Bridwell, Leeuwis)
Heterogeneity:              Moderate — methods span EEG, MEG, MRS, behavioral
Quality Assessment:         γ-tier (Bolland 2025 systematic review strengthens base)
Replication:                Bolland 2025 reviews 62 studies corroborating gamma-cognition link
```

---

## 4. R³ Input Mapping: What IGFE Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | IGFE Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [5] | periodicity | Frequency structure | Gamma-band proxy |
| **B: Energy** | [7] | amplitude | Stimulus intensity | Entrainment driver |
| **B: Energy** | [10] | spectral_flux | Temporal modulation rate | Rhythmic entrainment |
| **C: Timbre** | [12] | warmth | Spectral center | Frequency center proxy |
| **C: Timbre** | [14] | tonalness | Harmonic structure | IGF match component |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Frequency-perception binding | IGF enhancement basis |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | Gamma-cognitive coupling | Memory/executive pathway |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ v2 Group | Index | Feature | IGFE Role | Citation |
|-------------|-------|---------|-----------|----------|
| **I: Information** | [90] | spectral_surprise | Spectral novelty for gamma frequency entrainment modulation | Dubnov 2006 |
| **I: Information** | [91] | information_rate | Information flow rate for IGF enhancement scaling | Shannon 1948; Dubnov 2006 |

**Rationale**: IGFE models individual gamma frequency enhancement where stimulus frequency matching to individual gamma peaks enhances neural processing. spectral_surprise captures spectral novelty -- unexpected spectral events that modulate gamma entrainment strength. information_rate quantifies the overall information flow, which scales the degree of IGF enhancement (higher information rates demand more gamma-band processing). These features complement existing periodicity [5] and tonalness [14] by adding the information-theoretic dimension.

**Code impact** (future): `r3[..., 90]` and `r3[..., 91]` will feed IGFE's gamma entrainment pathway alongside existing consonance, timbre, and interaction features.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[5] periodicity ─────────────┐
R³[14] tonalness ──────────────┼──► IGF match quality
PPC.pitch_extraction[0:10] ────┘   Stimulus frequency vs individual gamma peak

R³[25:33] x_l0l5 ─────────────┐
TPC.spectral_shape[0:10] ─────┼──► Gamma synchronization strength
H³ periodicity tuples ─────────┘   Better match → stronger entrainment

R³[41:49] x_l5l7 ─────────────┐
MEM.working_memory[0:10] ──────┼──► Cognitive enhancement pathway
MEM.long_term_memory[10:20] ───┘   Memory: word recall ↑ (Yokota 2025)
                                   Executive: IES ↓ (Yokota 2025)
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

IGFE requires H³ features at gamma-scale horizons for frequency matching and longer integration for dose-response accumulation. The demand reflects the need for both fast frequency tracking and slow dose accumulation over minutes.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 5 | periodicity | 0 | M0 (value) | L2 (bidi) | Periodicity at 25ms (gamma) |
| 5 | periodicity | 1 | M0 (value) | L2 (bidi) | Periodicity at 50ms (gamma) |
| 5 | periodicity | 3 | M1 (mean) | L2 (bidi) | Mean periodicity 100ms |
| 5 | periodicity | 16 | M1 (mean) | L0 (fwd) | Mean periodicity 1s |
| 14 | tonalness | 3 | M0 (value) | L2 (bidi) | Tonalness at 100ms |
| 14 | tonalness | 16 | M1 (mean) | L0 (fwd) | Mean tonalness 1s |
| 7 | amplitude | 3 | M0 (value) | L2 (bidi) | Stimulus intensity 100ms |
| 7 | amplitude | 16 | M1 (mean) | L2 (bidi) | Mean intensity 1s |
| 25 | x_l0l5[0] | 0 | M0 (value) | L2 (bidi) | Coupling at 25ms (gamma) |
| 25 | x_l0l5[0] | 1 | M0 (value) | L2 (bidi) | Coupling at 50ms (gamma) |
| 25 | x_l0l5[0] | 3 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 100ms |
| 25 | x_l0l5[0] | 16 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 1s |
| 41 | x_l5l7[0] | 8 | M0 (value) | L0 (fwd) | Cognitive coupling 500ms |
| 41 | x_l5l7[0] | 16 | M1 (mean) | L0 (fwd) | Mean cognitive coupling 1s |
| 41 | x_l5l7[0] | 16 | M18 (trend) | L0 (fwd) | Coupling trend 1s (dose) |
| 10 | spectral_flux | 0 | M0 (value) | L2 (bidi) | Modulation rate 25ms |
| 10 | spectral_flux | 1 | M14 (periodicity) | L2 (bidi) | Modulation periodicity 50ms |
| 10 | spectral_flux | 3 | M1 (mean) | L2 (bidi) | Mean modulation 100ms |

**Total IGFE H³ demand**: 18 tuples of 2304 theoretical = 0.78%

### 5.2 PPC + TPC + MEM Mechanism Binding

| Mechanism | Sub-section | Range | IGFE Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **PPC** | Pitch Extraction | PPC[0:10] | IGF frequency matching | **1.0** (primary) |
| **PPC** | Interval Analysis | PPC[10:20] | Frequency stability tracking | 0.7 |
| **PPC** | Contour Tracking | PPC[20:30] | Spectral contour in gamma band | 0.5 |
| **TPC** | Spectral Shape | TPC[0:10] | Gamma power distribution | **0.9** |
| **TPC** | Temporal Envelope | TPC[10:20] | Modulation rate assessment | 0.7 |
| **TPC** | Source Identity | TPC[20:30] | Stimulus categorization | 0.5 |
| **MEM** | Working Memory | MEM[0:10] | Memory enhancement tracking | **0.9** |
| **MEM** | Long-Term Memory | MEM[10:20] | Dose accumulation | 0.8 |
| **MEM** | Prediction Buffer | MEM[20:30] | Enhancement prediction | 0.6 |

---

## 6. Output Space: 9D Multi-Layer Representation

### 6.1 Complete Output Specification

```
IGFE OUTPUT TENSOR: 9D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_igf_match            │ [0, 1] │ Individual gamma frequency alignment.
    │                          │        │ f01 = σ(0.35 * gamma_periodicity_25ms
    │                          │        │       + 0.35 * gamma_periodicity_50ms
    │                          │        │       + 0.30 * mean(PPC.pitch[0:10]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_memory_enhancement   │ [0, 1] │ Verbal memory improvement.
    │                          │        │ f02 = σ(0.40 * f01 * cog_coupling_mean_1s
    │                          │        │       + 0.30 * mean(MEM.wm[0:10])
    │                          │        │       + 0.30 * mean(MEM.ltm[10:20]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_executive_enhancement│ [0, 1] │ Executive control improvement.
    │                          │        │ f03 = σ(0.40 * f01 * cog_coupling_500ms
    │                          │        │       + 0.30 * mean(PPC.interval[10:20])
    │                          │        │       + 0.30 * mean(TPC.shape[0:10]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_dose_response        │ [0, 1] │ Exposure-benefit relationship.
    │                          │        │ f04 = σ(0.50 * coupling_trend_1s
    │                          │        │       + 0.50 * mean_intensity_1s)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ gamma_synchronization    │ [0, 1] │ TPC gamma entrainment strength.
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ dose_accumulation        │ [0, 1] │ MEM integration over time.
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ memory_access            │ [0, 1] │ MEM recall enhancement signal.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ memory_enhancement_post  │ [0, 1] │ Word recall prediction (post).
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ executive_improve_post   │ [0, 1] │ IES reduction prediction (post).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 9D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 IGF Enhancement Function

```
Enhancement(f) = Match(f, IGF) × Dose(t) × Intensity

Match(f, IGF) = exp(-(f - IGF)² / (2σ_gamma²))
    where σ_gamma ≈ 5 Hz, IGF ∈ [30, 80] Hz

Dose(t) = 1 - exp(-t / τ_dose)
    where τ_dose = 300s (5 min half-life)

Memory_Gain = α × Enhancement × WM_baseline
Executive_Gain = β × Enhancement × Executive_baseline
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: IGF Match
f01 = σ(0.35 * gamma_periodicity_25ms
       + 0.35 * gamma_periodicity_50ms
       + 0.30 * mean(PPC.pitch_extraction[0:10]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Memory Enhancement
f02 = σ(0.40 * f01 * cog_coupling_mean_1s
       + 0.30 * mean(MEM.working_memory[0:10])
       + 0.30 * mean(MEM.long_term_memory[10:20]))
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f03: Executive Enhancement
f03 = σ(0.40 * f01 * cog_coupling_500ms
       + 0.30 * mean(PPC.interval_analysis[10:20])
       + 0.30 * mean(TPC.spectral_shape[0:10]))
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f04: Dose Response
f04 = σ(0.50 * coupling_trend_1s
       + 0.50 * mean_intensity_1s)
# coefficients: 0.50 + 0.50 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | IGFE Function |
|--------|-----------------|----------|---------------|---------------|
| **Auditory Cortex (A1/STG)** | ±52, -22, 8 | 5 | EEG (Yokota 2025), MEG dipole (Dobri 2023), Review (Bolland 2025, Jiao 2025, Thaut 2015) | Gamma entrainment site; 40 Hz ASSR source |
| **Primary Auditory Cortex (Heschl's Gyrus)** | L: -48, -17, 8; R: 48, -20, 8 | 1 | MEG dipole source (Dobri et al. 2023) | 40 Hz ASSR generation; sensory + binding gamma components |
| **Hippocampus** | ±28, -24, -12 | 3 | Literature inference (Yokota 2025), Review (Bolland 2025, Jiao 2025) | Memory enhancement; gamma-driven amyloid clearance (preclinical) |
| **DLPFC** | ±42, 36, 24 | 2 | Literature inference (Yokota 2025), Review (Jiao 2025) | Executive control enhancement |
| **Thalamus** | 0, -12, 8 | 2 | Literature inference, Review (Dobri 2023 — thalamocortical circuits) | Gamma relay; reciprocal thalamocortical 40 Hz generation |
| **Fronto-central Cortex (FC/Cz)** | ~0, -20, 65 | 4 | EEG topography (Noboa 2025, Ding 2025, Aparicio-Terres 2025, Leeuwis 2021) | Entrainment maxima; gamma synchronization topography |
| **Sensorimotor Cortex / SMA** | ~0, -10, 55 | 1 | Review (Thaut et al. 2015) | Auditory-motor entrainment coupling |
| **Posterior Cingulate / Precuneus** | ~0, -52, 28 | 1 | fMRI (Bolland 2025 review — chronic stimulation) | Increased functional connectivity with gamma stimulation in MCI |

---

## 9. Cross-Unit Pathways

### 9.1 IGFE Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    IGFE INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (PCU):                                                         │
│  WMED.wm_contribution ──────► IGFE (WM baseline for enhancement)          │
│  IGFE.memory_enhancement ────► PSH (enhanced memory affects silencing)     │
│  IGFE.gamma_sync ────────────► MAA (gamma entrainment for appreciation)    │
│  HTP.hierarchy_gradient ─────► IGFE (hierarchy for gamma integration)      │
│                                                                             │
│  CROSS-UNIT (PCU → IMU):                                                   │
│  IGFE.memory_enhancement ────► IMU (memory enhancement for integration)    │
│  IGFE.dose_accumulation ─────► IMU (temporal accumulation signal)          │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  PPC mechanism (30D) ────────► IGFE (pitch/frequency matching)             │
│  TPC mechanism (30D) ────────► IGFE (gamma power / modulation)             │
│  MEM mechanism (30D) ────────► IGFE (memory/dose/prediction)               │
│  R³ (~14D) ──────────────────► IGFE (direct spectral features)             │
│  H³ (18 tuples) ─────────────► IGFE (temporal dynamics)                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **IGF specificity** | Enhancement should be frequency-specific to IGF | Testable via non-IGF control |
| **Dose-response** | Longer exposure should yield greater enhancement | **Supported** (Yokota 2025) |
| **Memory enhancement** | IGF music should improve word recall | **Supported** (Yokota 2025) |
| **Executive enhancement** | IGF music should reduce IES | **Supported** (Yokota 2025) |
| **Individual differences** | IGF varies across individuals (30-80 Hz) | Testable via EEG assessment |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class IGFE(BaseModel):
    """Individual Gamma Frequency Enhancement Model.

    Output: 9D per frame.
    Reads: PPC mechanism (30D), TPC mechanism (30D), MEM mechanism (30D), R³ direct.
    """
    NAME = "IGFE"
    UNIT = "PCU"
    TIER = "γ1"
    OUTPUT_DIM = 9
    MECHANISM_NAMES = ("PPC", "TPC", "MEM")

    TAU_DOSE = 300.0               # s (5 min half-life)
    IGF_RANGE = (30.0, 80.0)       # Hz (gamma band)
    SIGMA_GAMMA = 5.0              # Hz (matching bandwidth)

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """18 tuples for IGFE computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── Gamma-scale frequency matching ──
            (5, 0, 0, 2),      # periodicity, 25ms, value, bidi
            (5, 1, 0, 2),      # periodicity, 50ms, value, bidi
            (5, 3, 1, 2),      # periodicity, 100ms, mean, bidi
            (5, 16, 1, 0),     # periodicity, 1000ms, mean, fwd
            (14, 3, 0, 2),     # tonalness, 100ms, value, bidi
            (14, 16, 1, 0),    # tonalness, 1000ms, mean, fwd
            # ── Stimulus intensity ──
            (7, 3, 0, 2),      # amplitude, 100ms, value, bidi
            (7, 16, 1, 2),     # amplitude, 1000ms, mean, bidi
            # ── Gamma entrainment coupling ──
            (25, 0, 0, 2),     # x_l0l5[0], 25ms, value, bidi
            (25, 1, 0, 2),     # x_l0l5[0], 50ms, value, bidi
            (25, 3, 14, 2),    # x_l0l5[0], 100ms, periodicity, bidi
            (25, 16, 14, 2),   # x_l0l5[0], 1000ms, periodicity, bidi
            # ── Cognitive enhancement coupling ──
            (41, 8, 0, 0),     # x_l5l7[0], 500ms, value, fwd
            (41, 16, 1, 0),    # x_l5l7[0], 1000ms, mean, fwd
            (41, 16, 18, 0),   # x_l5l7[0], 1000ms, trend, fwd
            # ── Modulation rate ──
            (10, 0, 0, 2),     # spectral_flux, 25ms, value, bidi
            (10, 1, 14, 2),    # spectral_flux, 50ms, periodicity, bidi
            (10, 3, 1, 2),     # spectral_flux, 100ms, mean, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute IGFE 9D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30), "TPC": (B,T,30), "MEM": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,9) IGFE output
        """
        ppc = mechanism_outputs["PPC"]
        tpc = mechanism_outputs["TPC"]
        mem = mechanism_outputs["MEM"]

        # Mechanism sub-sections
        ppc_pitch = ppc[..., 0:10]
        ppc_interval = ppc[..., 10:20]
        tpc_shape = tpc[..., 0:10]
        tpc_env = tpc[..., 10:20]
        mem_wm = mem[..., 0:10]
        mem_ltm = mem[..., 10:20]
        mem_pred = mem[..., 20:30]

        # H³ direct features
        gamma_period_25ms = h3_direct[(5, 0, 0, 2)].unsqueeze(-1)
        gamma_period_50ms = h3_direct[(5, 1, 0, 2)].unsqueeze(-1)
        cog_coupling_500ms = h3_direct[(41, 8, 0, 0)].unsqueeze(-1)
        cog_coupling_mean_1s = h3_direct[(41, 16, 1, 0)].unsqueeze(-1)
        coupling_trend_1s = h3_direct[(41, 16, 18, 0)].unsqueeze(-1)
        mean_intensity_1s = h3_direct[(7, 16, 1, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: IGF Match (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.35 * gamma_period_25ms
            + 0.35 * gamma_period_50ms
            + 0.30 * ppc_pitch.mean(-1, keepdim=True)
        )

        # f02: Memory Enhancement (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.40 * f01 * cog_coupling_mean_1s
            + 0.30 * mem_wm.mean(-1, keepdim=True)
            + 0.30 * mem_ltm.mean(-1, keepdim=True)
        )

        # f03: Executive Enhancement (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.40 * f01 * cog_coupling_500ms
            + 0.30 * ppc_interval.mean(-1, keepdim=True)
            + 0.30 * tpc_shape.mean(-1, keepdim=True)
        )

        # f04: Dose Response (coefficients sum = 1.0)
        f04 = torch.sigmoid(
            0.50 * coupling_trend_1s
            + 0.50 * mean_intensity_1s
        )

        # ═══ LAYER P: Present ═══
        gamma_sync = tpc_env.mean(-1, keepdim=True)
        dose_accum = f04
        memory_acc = mem_wm.mean(-1, keepdim=True)

        # ═══ LAYER F: Future ═══
        memory_post = torch.sigmoid(0.5 * f02 + 0.5 * f04)
        executive_post = torch.sigmoid(0.5 * f03 + 0.5 * f04)

        return torch.cat([
            f01, f02, f03, f04,                       # E: 4D
            gamma_sync, dose_accum, memory_acc,       # P: 3D
            memory_post, executive_post,              # F: 2D
        ], dim=-1)  # (B, T, 9)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 10 | 3 direct gamma-cognition + 2 gamma mechanisms + 3 entrainment-cognition + 2 cortical entrainment |
| **Effect Sizes** | 12+ | R²=0.31-0.40, η²=0.14-0.36, r=0.22-0.65, plus narrative reviews |
| **Evidence Modality** | EEG, MEG, MRS, fMRI, behavioral | Multi-modal neural + behavioral |
| **Falsification Tests** | 5/5 testable, 3 supported | Moderate (awaiting replication) |
| **R³ Features Used** | ~14D of 49D | Consonance + energy + timbre + interactions |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Pitch/frequency matching |
| **TPC Mechanism** | 30D (3 sub-sections) | Gamma power / modulation |
| **MEM Mechanism** | 30D (3 sub-sections) | Memory/dose/prediction |
| **Output Dimensions** | **9D** | 3-layer structure (no M layer) |

---

## 13. Scientific References

1. **Yokota, Y., et al. (2025)**. Individual gamma frequency enhancement through auditory stimulation. *Frontiers in Human Neuroscience*, in press.
2. **Bolland, E., De Burca, A., Wang, S. H., Khalil, A., & McLoughlin, G. (2025)**. Efficacy of auditory gamma stimulation for cognitive decline: a systematic review of individual and group differences across cognitively impaired and healthy populations. *npj Aging*. https://doi.org/10.1038/s41514-025-00305-1
3. **Dobri, S., Chen, J. J., & Ross, B. (2023)**. Synchrony in auditory 40-Hz gamma oscillations increases in older age and correlates with hearing abilities and cortical GABA levels. *Imaging Neuroscience*, 1. https://doi.org/10.1162/imag_a_00035
4. **Jiao, D. (2025)**. Advancing personalized digital therapeutics integrating music therapy, brainwave entrainment methods, and AI-driven biofeedback. *Frontiers in Digital Health*, 7, 1552396.
5. **Noboa, M. L., Kertesz, C., & Honbolygo, F. (2025)**. Neural entrainment to the beat. *Scientific Reports*, 15, 10466.
6. **Ding, J., Zhang, X., Liu, J., Hu, Z., Yang, Z., Tang, Y., & Ding, Y. (2025)**. Entrainment of rhythmic tonal sequences on neural oscillations and the impact on subjective emotion. *Scientific Reports*, 15, 17462.
7. **Thaut, M. H., McIntosh, G. C., & Hoemberg, V. (2015)**. Neurobiological foundations of neurologic music therapy: rhythmic entrainment and the motor system. *Frontiers in Psychology*, 5, 1185.
8. **Aparicio-Terres, R., Lopez-Mochales, S., Diaz-Andreu, M., & Escera, C. (2025)**. The strength of neural entrainment to electronic music correlates with proxies of altered states of consciousness. *Frontiers in Human Neuroscience*, 19, 1574836.
9. **Bridwell, D. A., Leslie, E., McCoy, D. Q., Plis, S. M., & Calhoun, V. D. (2017)**. Cortical sensitivity to guitar note patterns: EEG entrainment to repetition and key. *Frontiers in Human Neuroscience*, 11, 90.
10. **Leeuwis, N., Pistone, D., Flick, N., & van Bommel, T. (2021)**. A sound prediction: EEG-based neural synchrony predicts online music streams. *Frontiers in Psychology*, 12, 672980.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, TIH, HRM, EFC) | PPC (30D) + TPC (30D) + MEM (30D) mechanisms |
| Frequency matching | S⁰.L0.frequency[1] + HC⁰.OSC | R³[5] periodicity + PPC.pitch_extraction |
| Gamma power | S⁰.L7[80:88] + HC⁰.TIH | R³[25:33] x_l0l5 + TPC.spectral_shape |
| Cognitive pathway | S⁰.X_L5L7[216:224] + HC⁰.HRM | R³[41:49] x_l5l7 + MEM.working_memory |
| Enhancement | S⁰.X_L0L5[136:144] | R³[25:33] x_l0l5 + PPC.pitch_extraction |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 42/2304 = 1.82% | 18/2304 = 0.78% |
| Output | 9D | 9D (same) |

### Why PPC + TPC + MEM replaces HC⁰ mechanisms

- **OSC → PPC.pitch_extraction** [0:10]: Neural oscillation coupling for gamma-frequency matching maps to PPC's pitch/frequency extraction.
- **TIH → TPC.temporal_envelope** [10:20]: Temporal integration hierarchy for dose accumulation maps to TPC's temporal envelope tracking.
- **HRM → MEM.long_term_memory** [10:20]: Hippocampal replay for memory enhancement maps to MEM's long-term memory.
- **EFC → MEM.working_memory** [0:10]: Efference copy for executive control maps to MEM's working memory.

---

**Model Status**: **PRELIMINARY**
**Output Dimensions**: **9D**
**Evidence Tier**: **γ (Integrative)**
**Confidence**: **50-70%**
