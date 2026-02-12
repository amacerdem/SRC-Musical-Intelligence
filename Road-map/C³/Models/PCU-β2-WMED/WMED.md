# PCU-β2-WMED: Working Memory-Entrainment Dissociation

**Model**: Working Memory-Entrainment Dissociation
**Unit**: PCU (Predictive Coding Unit)
**Circuit**: Imagery (Auditory Cortex, IFG, STS, Hippocampus)
**Tier**: β (Bridging) — 70-90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, PPC+TPC+MEM mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/PCU-β2-WMED.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Working Memory-Entrainment Dissociation** (WMED) model describes how neural entrainment and working memory contribute independently to rhythm production, with a paradoxical finding that stronger entrainment to simple rhythms predicts worse tapping performance.

```
WORKING MEMORY-ENTRAINMENT DISSOCIATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ENTRAINMENT PATHWAY                     WORKING MEMORY PATHWAY
──────────────────                      ─────────────────────
SS-EP at beat frequencies               Counting span / WM capacity

  Beat ────► Neural ────► Motor          Pattern ────► WM ────► Motor
  Input     Entrainment   Output         Complexity   Load     Output

  PARADOX: ↑ Entrainment → ↓ Tapping    STANDARD: ↑ WM → ↑ Tapping
  (over-synchronization reduces          (cognitive control aids
   motor flexibility)                     motor adaptation)

┌──────────────────────────────────────────────────────────────────┐
│         DUAL-ROUTE INDEPENDENCE (Noboa 2025)                     │
│                                                                  │
│  Route 1 (Automatic):   SS-EP strength ↑ → Tapping ↓ (p<0.006) │
│  Route 2 (Controlled):  WM capacity ↑  → Tapping ↑ (p<0.006)  │
│                                                                  │
│  These routes are INDEPENDENT (no interaction term significant)  │
└──────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Neural entrainment and working memory contribute
independently to rhythm production. Stronger entrainment paradoxically
predicts worse tapping — over-reliance on automatic entrainment
reduces the motor flexibility needed for accurate reproduction.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why WMED Matters for PCU

WMED separates automatic entrainment from controlled WM contributions:

1. **HTP** (α1) provides hierarchical prediction timing.
2. **PWUP** (β1) modulates PE by contextual precision.
3. **WMED** (β2) reveals independent entrainment vs WM routes in rhythm production.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → PPC+TPC+MEM → WMED)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    WMED COMPUTATION ARCHITECTURE                            ║
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
║  │                         WMED reads: ~15D                         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                         WMED demand: ~16 of 2304 tuples          │        ║
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
║  │                    WMED MODEL (11D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_entrainment_strength,                  │        ║
║  │                       f02_wm_contribution,                       │        ║
║  │                       f03_tapping_accuracy,                      │        ║
║  │                       f04_dissociation_index                     │        ║
║  │  Layer P (Present):   phase_locking_strength,                    │        ║
║  │                       pattern_segmentation,                      │        ║
║  │                       rhythmic_engagement                        │        ║
║  │  Layer F (Future):    next_beat_pred, tapping_accuracy_pred,     │        ║
║  │                       wm_interference_pred,                      │        ║
║  │                       paradox_strength_pred                      │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Noboa 2025** | EEG + Behavioral | 30 | SS-EP at beat frequencies > noise | p < 0.001 | **f01 entrainment strength** |
| **Noboa 2025** | EEG + Behavioral | 30 | Stronger unsyncopated SS-EP → worse tapping | p < 0.006 | **f04 dissociation / paradox** |
| **Noboa 2025** | EEG + Behavioral | 30 | Higher WM → better tapping consistency | p < 0.006 | **f02 WM contribution** |

### 3.2 Effect Size Summary

```
Primary Evidence (k=3):  All findings from single well-powered study
Heterogeneity:           N/A (single study, multiple findings)
Quality Assessment:      β-tier (EEG + behavioral, within-subjects)
Replication:             Awaiting independent replication
```

---

## 4. R³ Input Mapping: What WMED Reads

### 4.1 R³ Feature Dependencies (~15D of 49D)

| R³ Group | Index | Feature | WMED Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Beat strength | Temporal intensity |
| **B: Energy** | [8] | loudness | Perceptual loudness | Arousal correlate |
| **B: Energy** | [10] | spectral_flux | Beat salience / onset | Rhythmic event detection |
| **B: Energy** | [11] | onset_strength | Beat marker strength | Entrainment target |
| **D: Change** | [21] | spectral_change | Timing variability | Tapping accuracy basis |
| **D: Change** | [22] | energy_change | Energy dynamics | Syncopation detection |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Automatic entrainment pathway | SS-EP basis (paradox route) |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | WM pathway | Counting span basis |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[10] spectral_flux ────────────┐
R³[11] onset_strength ───────────┼──► Entrainment strength (SS-EP proxy)
PPC.pitch_extraction[0:10] ──────┘   High periodicity → strong SS-EP

R³[25:33] x_l0l5 ───────────────┐
TPC.temporal_envelope[10:20] ────┼──► Automatic entrainment pathway
H³ periodicity tuples ──────────┘   Paradox: high x_l0l5 → worse tapping (p<0.006)

R³[41:49] x_l5l7 ───────────────┐
MEM.working_memory[0:10] ───────┼──► Working memory pathway
H³ entropy tuples ──────────────┘   Higher x_l5l7 → better tapping (p<0.006)

R³[21] spectral_change ─────────┐
MEM.prediction_buffer[20:30] ───┼──► Tapping accuracy (outcome measure)
                                    Lower change variability → better consistency
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

WMED requires H³ features for entrainment tracking (beat-scale periodicity) and WM loading (longer integration windows). The demand reflects the dual-route architecture: automatic entrainment (fast, periodic) vs working memory (slow, contextual).

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | Onset salience at 100ms |
| 10 | spectral_flux | 3 | M14 (periodicity) | L2 (bidi) | Beat periodicity at 100ms |
| 10 | spectral_flux | 16 | M14 (periodicity) | L2 (bidi) | Beat periodicity at 1s |
| 11 | onset_strength | 3 | M0 (value) | L2 (bidi) | Onset strength at 100ms |
| 11 | onset_strength | 16 | M14 (periodicity) | L2 (bidi) | Onset periodicity at 1s |
| 7 | amplitude | 3 | M2 (std) | L2 (bidi) | Amplitude variability 100ms |
| 7 | amplitude | 16 | M1 (mean) | L2 (bidi) | Mean amplitude over 1s |
| 25 | x_l0l5[0] | 3 | M14 (periodicity) | L2 (bidi) | Entrainment periodicity 100ms |
| 25 | x_l0l5[0] | 16 | M14 (periodicity) | L2 (bidi) | Entrainment periodicity 1s |
| 25 | x_l0l5[0] | 16 | M21 (zero_crossings) | L2 (bidi) | Phase resets 1s |
| 41 | x_l5l7[0] | 8 | M0 (value) | L0 (fwd) | WM coupling at 500ms |
| 41 | x_l5l7[0] | 16 | M1 (mean) | L0 (fwd) | Mean WM coupling 1s |
| 41 | x_l5l7[0] | 16 | M20 (entropy) | L0 (fwd) | WM entropy 1s |
| 21 | spectral_change | 3 | M0 (value) | L2 (bidi) | Timing variability 100ms |
| 21 | spectral_change | 16 | M2 (std) | L0 (fwd) | Timing std over 1s |
| 21 | spectral_change | 16 | M19 (stability) | L0 (fwd) | Timing stability 1s |

**Total WMED H³ demand**: 16 tuples of 2304 theoretical = 0.69%

### 5.2 PPC + TPC + MEM Mechanism Binding

| Mechanism | Sub-section | Range | WMED Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **PPC** | Pitch Extraction | PPC[0:10] | Phase-locking for entrainment | 0.7 |
| **PPC** | Interval Analysis | PPC[10:20] | Beat interval tracking | 0.6 |
| **PPC** | Contour Tracking | PPC[20:30] | Rhythmic contour | 0.5 |
| **TPC** | Spectral Shape | TPC[0:10] | Rhythm pattern recognition | 0.6 |
| **TPC** | Temporal Envelope | TPC[10:20] | Entrainment pathway (automatic) | **0.9** |
| **TPC** | Source Identity | TPC[20:30] | Syncopation detection | 0.5 |
| **MEM** | Working Memory | MEM[0:10] | WM capacity (counting span) | **1.0** (primary) |
| **MEM** | Long-Term Memory | MEM[10:20] | Pattern familiarity | 0.7 |
| **MEM** | Prediction Buffer | MEM[20:30] | Tapping prediction | **0.9** |

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
WMED OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_entrainment_strength │ [0, 1] │ SS-EP magnitude at beat frequency.
    │                          │        │ f01 = σ(0.35 * beat_periodicity_1s
    │                          │        │       + 0.35 * onset_periodicity_1s
    │                          │        │       + 0.30 * mean(TPC.env[10:20]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_wm_contribution      │ [0, 1] │ Working memory capacity measure.
    │                          │        │ f02 = σ(0.40 * wm_coupling_mean_1s
    │                          │        │       + 0.30 * wm_entropy_1s
    │                          │        │       + 0.30 * mean(MEM.wm[0:10]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_tapping_accuracy     │ [0, 1] │ Motor precision outcome.
    │                          │        │ f03 = σ(0.40 * timing_stability_1s
    │                          │        │       + 0.30 * mean(MEM.pred[20:30])
    │                          │        │       + 0.30 * (1 - timing_std_1s))
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_dissociation_index   │ [0, 1] │ Independence of entrainment vs WM.
    │                          │        │ f04 = σ(0.50 * |f01 - f02|
    │                          │        │       + 0.50 * entrainment_phase_resets)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ phase_locking_strength   │ [0, 1] │ TPC entrainment magnitude.
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ pattern_segmentation     │ [0, 1] │ MEM working memory loading.
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ rhythmic_engagement      │ [0, 1] │ PPC motor preparation level.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ next_beat_pred           │ [0, 1] │ Motor system beat timing.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ tapping_accuracy_pred    │ [0, 1] │ Performance prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ wm_interference_pred     │ [0, 1] │ Entrainment-motor conflict.
────┼──────────────────────────┼────────┼────────────────────────────────────
10  │ paradox_strength_pred    │ [0, 1] │ Entrainment→tapping inverse.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Dual-Route Model

```
Tapping_Accuracy = α·WM_Contribution - β·Entrainment_Paradox + ε

Route 1 (Entrainment):  Automatic SS-EP → Motor coupling
    High entrainment → WORSE tapping (over-synchronization)
Route 2 (Working Memory): Counting span → Cognitive control
    High WM → BETTER tapping (flexibility)

Dissociation_Index = |Route1 - Route2| / (Route1 + Route2)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Entrainment Strength
f01 = σ(0.35 * beat_periodicity_1s
       + 0.35 * onset_periodicity_1s
       + 0.30 * mean(TPC.temporal_envelope[10:20]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: WM Contribution
f02 = σ(0.40 * wm_coupling_mean_1s
       + 0.30 * wm_entropy_1s
       + 0.30 * mean(MEM.working_memory[0:10]))
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f03: Tapping Accuracy
f03 = σ(0.40 * timing_stability_1s
       + 0.30 * mean(MEM.prediction_buffer[20:30])
       + 0.30 * (1 - timing_std_1s))
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f04: Dissociation Index
f04 = σ(0.50 * abs(f01 - f02)
       + 0.50 * entrainment_phase_resets)
# coefficients: 0.50 + 0.50 = 1.0 ✓

# Paradox effect
paradox = f01 * (1 - f03)  # high entrainment × low accuracy
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | WMED Function |
|--------|-----------------|----------|---------------|---------------|
| **Auditory Cortex (STG)** | ±52, -22, 8 | 2 | Direct (EEG) | SS-EP generation |
| **SMA (Supplementary Motor)** | 0, -6, 58 | 1 | Literature inference | Motor timing |
| **DLPFC** | ±42, 36, 24 | 1 | Literature inference | Working memory |
| **Basal Ganglia** | ±14, 6, -4 | 1 | Literature inference | Beat tracking |

---

## 9. Cross-Unit Pathways

### 9.1 WMED Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    WMED INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (PCU):                                                         │
│  PWUP.precision_weight ─────► WMED (precision modulates entrainment PE)   │
│  WMED.entrainment_strength ──► UDP (entrainment context for reward)        │
│  WMED.dissociation_index ────► PSH (dual-route for silencing decision)    │
│  WMED.wm_contribution ──────► IGFE (WM baseline for enhancement)          │
│                                                                             │
│  CROSS-UNIT (PCU → STU):                                                   │
│  WMED.entrainment_strength ──► STU (entrainment for motor coupling)       │
│  WMED.tapping_accuracy ─────► STU.HMCE (tapping accuracy baseline)        │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  PPC mechanism (30D) ────────► WMED (phase-locking / entrainment)         │
│  TPC mechanism (30D) ────────► WMED (temporal envelope / entrainment)     │
│  MEM mechanism (30D) ────────► WMED (WM capacity / prediction)            │
│  R³ (~15D) ──────────────────► WMED (direct spectral features)            │
│  H³ (16 tuples) ─────────────► WMED (temporal dynamics)                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **SS-EP presence** | SS-EP at beat frequencies should exceed noise floor | **Confirmed** (p<0.001, Noboa 2025) |
| **Entrainment paradox** | Stronger SS-EP should predict worse tapping | **Confirmed** (p<0.006, Noboa 2025) |
| **WM benefit** | Higher WM capacity should predict better tapping | **Confirmed** (p<0.006, Noboa 2025) |
| **Route independence** | Entrainment and WM should show no interaction | Testable via factorial design |
| **Syncopation modulation** | Syncopation should modulate paradox strength | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class WMED(BaseModel):
    """Working Memory-Entrainment Dissociation Model.

    Output: 11D per frame.
    Reads: PPC mechanism (30D), TPC mechanism (30D), MEM mechanism (30D), R³ direct.
    """
    NAME = "WMED"
    UNIT = "PCU"
    TIER = "β2"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("PPC", "TPC", "MEM")

    TAU_DECAY = 0.5                # s (Noboa 2025)
    PARADOX_THRESHOLD = 0.6        # SS-EP level for paradox onset

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """16 tuples for WMED computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── Entrainment pathway: beat tracking ──
            (10, 3, 0, 2),      # spectral_flux, 100ms, value, bidi
            (10, 3, 14, 2),     # spectral_flux, 100ms, periodicity, bidi
            (10, 16, 14, 2),    # spectral_flux, 1000ms, periodicity, bidi
            (11, 3, 0, 2),      # onset_strength, 100ms, value, bidi
            (11, 16, 14, 2),    # onset_strength, 1000ms, periodicity, bidi
            (7, 3, 2, 2),       # amplitude, 100ms, std, bidi
            (7, 16, 1, 2),      # amplitude, 1000ms, mean, bidi
            # ── Entrainment route: automatic coupling ──
            (25, 3, 14, 2),     # x_l0l5[0], 100ms, periodicity, bidi
            (25, 16, 14, 2),    # x_l0l5[0], 1000ms, periodicity, bidi
            (25, 16, 21, 2),    # x_l0l5[0], 1000ms, zero_crossings, bidi
            # ── WM route: controlled processing ──
            (41, 8, 0, 0),      # x_l5l7[0], 500ms, value, fwd
            (41, 16, 1, 0),     # x_l5l7[0], 1000ms, mean, fwd
            (41, 16, 20, 0),    # x_l5l7[0], 1000ms, entropy, fwd
            # ── Tapping accuracy ──
            (21, 3, 0, 2),      # spectral_change, 100ms, value, bidi
            (21, 16, 2, 0),     # spectral_change, 1000ms, std, fwd
            (21, 16, 19, 0),    # spectral_change, 1000ms, stability, fwd
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute WMED 11D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30), "TPC": (B,T,30), "MEM": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,11) WMED output
        """
        ppc = mechanism_outputs["PPC"]
        tpc = mechanism_outputs["TPC"]
        mem = mechanism_outputs["MEM"]

        # Mechanism sub-sections
        ppc_pitch = ppc[..., 0:10]
        tpc_env = tpc[..., 10:20]
        mem_wm = mem[..., 0:10]
        mem_ltm = mem[..., 10:20]
        mem_pred = mem[..., 20:30]

        # H³ direct features
        beat_period_1s = h3_direct[(10, 16, 14, 2)].unsqueeze(-1)
        onset_period_1s = h3_direct[(11, 16, 14, 2)].unsqueeze(-1)
        wm_coupling_mean_1s = h3_direct[(41, 16, 1, 0)].unsqueeze(-1)
        wm_entropy_1s = h3_direct[(41, 16, 20, 0)].unsqueeze(-1)
        timing_stability_1s = h3_direct[(21, 16, 19, 0)].unsqueeze(-1)
        timing_std_1s = h3_direct[(21, 16, 2, 0)].unsqueeze(-1)
        phase_resets = h3_direct[(25, 16, 21, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: Entrainment Strength (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.35 * beat_period_1s
            + 0.35 * onset_period_1s
            + 0.30 * tpc_env.mean(-1, keepdim=True)
        )

        # f02: WM Contribution (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.40 * wm_coupling_mean_1s
            + 0.30 * wm_entropy_1s
            + 0.30 * mem_wm.mean(-1, keepdim=True)
        )

        # f03: Tapping Accuracy (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.40 * timing_stability_1s
            + 0.30 * mem_pred.mean(-1, keepdim=True)
            + 0.30 * (1 - timing_std_1s)
        )

        # f04: Dissociation Index (coefficients sum = 1.0)
        f04 = torch.sigmoid(
            0.50 * torch.abs(f01 - f02)
            + 0.50 * phase_resets
        )

        # ═══ LAYER P: Present ═══
        phase_lock = tpc_env.mean(-1, keepdim=True)
        pattern_seg = mem_wm.mean(-1, keepdim=True)
        rhythmic_eng = ppc_pitch.mean(-1, keepdim=True)

        # ═══ LAYER F: Future ═══
        next_beat = torch.sigmoid(0.5 * f01 + 0.5 * beat_period_1s)
        tapping_pred = torch.sigmoid(0.5 * f03 + 0.5 * f02)
        wm_interf = torch.sigmoid(
            0.5 * f01 + 0.5 * (1 - f02)
        )
        paradox = torch.sigmoid(
            0.5 * f01 + 0.5 * (1 - f03)
        )

        return torch.cat([
            f01, f02, f03, f04,                          # E: 4D
            phase_lock, pattern_seg, rhythmic_eng,       # P: 3D
            next_beat, tapping_pred, wm_interf, paradox, # F: 4D
        ], dim=-1)  # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 (Noboa 2025) | Primary evidence |
| **Effect Sizes** | 3 | All significant (p<0.006) |
| **Evidence Modality** | EEG + behavioral | Direct neural + behavioral |
| **Falsification Tests** | 5/5 testable, 3 confirmed | High validity |
| **R³ Features Used** | ~15D of 49D | Energy + change + interactions |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Phase-locking / entrainment |
| **TPC Mechanism** | 30D (3 sub-sections) | Temporal envelope / entrainment |
| **MEM Mechanism** | 30D (3 sub-sections) | WM capacity / prediction |
| **Output Dimensions** | **11D** | 3-layer structure (no M layer) |

---

## 13. Scientific References

1. **Noboa, S., et al. (2025)**. Neural entrainment and working memory contributions to rhythm production. *Journal of Cognitive Neuroscience*, in press.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (NPL, ITM, GRV, SGM) | PPC (30D) + TPC (30D) + MEM (30D) mechanisms |
| Entrainment signal | S⁰.L3.coherence[14] + S⁰.X_L0L1[128:136] | R³[10,11] onset/flux + TPC.temporal_envelope |
| WM pathway | S⁰.X_L4L5[192:200] | R³[41:49] x_l5l7 + MEM.working_memory |
| Tapping accuracy | S⁰.L9.std_T[108] | R³[21] spectral_change + MEM.prediction_buffer |
| Entrainment route | S⁰.X_L0L1[128:136] | R³[25:33] x_l0l5 + TPC.temporal_envelope |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 21/2304 = 0.91% | 16/2304 = 0.69% |
| Output | 11D | 11D (same) |

### Why PPC + TPC + MEM replaces HC⁰ mechanisms

- **NPL → TPC.temporal_envelope** [10:20]: Neural phase locking for entrainment maps to TPC's temporal envelope tracking.
- **ITM → MEM.prediction_buffer** [20:30]: Interval timing maps to MEM's prediction buffer for timing accuracy.
- **GRV → TPC.spectral_shape** [0:10] + PPC.pitch_extraction [0:10]: Groove processing spans rhythmic pattern and phase-locking.
- **SGM → MEM.long_term_memory** [10:20]: Striatal gradient memory maps to MEM's long-term pattern memory.

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **11D**
**Evidence Tier**: **β (Bridging)**
**Confidence**: **70-90%**
