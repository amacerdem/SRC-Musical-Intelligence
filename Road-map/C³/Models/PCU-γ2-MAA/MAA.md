# PCU-γ2-MAA: Multifactorial Atonal Appreciation

**Model**: Multifactorial Atonal Appreciation
**Unit**: PCU (Predictive Coding Unit)
**Circuit**: Imagery (Auditory Cortex, IFG, STS, Hippocampus)
**Tier**: γ (Integrative) — 50-70% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, PPC+TPC+MEM mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/PCU-γ2-MAA.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Multifactorial Atonal Appreciation** (MAA) model proposes that appreciation of atonal music emerges from the interaction of personality (openness), aesthetic framing (cognitive mastering), and exposure (familiarity).

```
MULTIFACTORIAL ATONAL APPRECIATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ATONAL MUSIC INPUT                      APPRECIATION OUTPUT
──────────────────                      ───────────────────
High entropy                            Modulated by three factors
Low tonal coherence

┌──────────────────────────────────────────────────────────────────┐
│         THREE-FACTOR MODEL (Mencke 2019)                         │
│                                                                  │
│  Factor 1: PERSONALITY (Openness to Experience)                 │
│    High openness → higher complexity tolerance                  │
│    Trait-level modulation of appreciation threshold             │
│                                                                  │
│  Factor 2: FRAMING (Cognitive Mastering)                        │
│    Aesthetic framing → better interpretation                    │
│    Context → meaning extraction from complexity                 │
│                                                                  │
│  Factor 3: EXPOSURE (Familiarity)                               │
│    Mere exposure effect → increased familiarity                │
│    Repeated listening → pattern recognition                     │
│                                                                  │
│  Appreciation = f(Complexity × Tolerance × Framing × Exposure)  │
└──────────────────────────────────────────────────────────────────┘

  Complexity ────► × Openness ────► × Framing ────► × Exposure ────► Appreciation
  (R³ features)    (trait gain)      (context)       (repetition)      (output)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Appreciation of atonal music is not simply a function
of acoustic complexity but emerges from the interaction of personality
traits (openness), cognitive framing (aesthetic context), and exposure
(familiarity through repeated listening).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why MAA Matters for PCU

MAA extends prediction to aesthetic appreciation under complexity:

1. **HTP** (α1) provides hierarchical prediction timing.
2. **PWUP** (β1) modulates PE by contextual precision.
3. **UDP** (β3) shows reward inversion under uncertainty.
4. **MAA** (γ2) explains how appreciation emerges despite high uncertainty.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → PPC+TPC+MEM → MAA)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MAA COMPUTATION ARCHITECTURE                             ║
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
║  │                         MAA reads: ~16D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                         MAA demand: ~14 of 2304 tuples           │        ║
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
║  │                    MAA MODEL (10D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_complexity_tolerance,                  │        ║
║  │                       f02_familiarity_index,                     │        ║
║  │                       f03_framing_effect,                        │        ║
║  │                       f04_appreciation_composite                 │        ║
║  │  Layer P (Present):   pattern_search,                            │        ║
║  │                       context_assessment,                        │        ║
║  │                       aesthetic_evaluation                       │        ║
║  │  Layer F (Future):    appreciation_growth,                       │        ║
║  │                       pattern_recognition,                       │        ║
║  │                       aesthetic_development                      │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Mencke 2019** | Behavioral | 100 | Multiple factors contribute to atonal appreciation | significant | **f01-f04 multifactorial model** |
| **Mencke 2019** | Theoretical | — | Openness, framing, and exposure interact | theoretical | **Three-factor architecture** |

### 3.2 Effect Size Summary

```
Primary Effect:       Multifactorial appreciation demonstrated
Heterogeneity:        Single study + theoretical framework
Quality Assessment:   γ-tier (theoretical model with behavioral support)
Replication:          Consistent with mere exposure and personality research
```

---

## 4. R³ Input Mapping: What MAA Reads

### 4.1 R³ Feature Dependencies (~16D of 49D)

| R³ Group | Index | Feature | MAA Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **A: Consonance** | [0] | roughness | Dissonance level | Harmonic tension |
| **A: Consonance** | [4] | sensory_pleasantness | Consonance proxy | Inverse of atonality |
| **A: Consonance** | [5] | periodicity | Tonal certainty | Key clarity component |
| **C: Timbre** | [14] | tonalness | Key clarity proxy | Atonality index |
| **C: Timbre** | [18:21] | tristimulus1-3 | Harmonic structure | Tonal cues |
| **D: Change** | [21] | spectral_change | Structural complexity | Pattern detection basis |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | Complexity tolerance pathway | Appreciation pathway |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[4] sensory_pleasantness ────┐
R³[14] tonalness ──────────────┼──► Atonality index (inverse)
R³[0] roughness ───────────────┘   Low consonance → high atonality

R³[41:49] x_l5l7 ─────────────┐
MEM.working_memory[0:10] ──────┼──► Complexity tolerance pathway
H³ entropy tuples ─────────────┘   Moderated by: openness, framing, exposure
                                   Appreciation = f(complexity × tolerance)

R³[21] spectral_change ────────┐
MEM.long_term_memory[10:20] ───┼──► Familiarity / pattern recognition
TPC.source_identity[20:30] ────┘   More exposure → higher familiarity
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

MAA requires H³ features for complexity assessment (medium-term context) and familiarity estimation (long-term pattern recognition). The demand reflects the need for piece-level integration to assess appreciation over extended listening.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 4 | sensory_pleasantness | 3 | M0 (value) | L2 (bidi) | Consonance at 100ms |
| 4 | sensory_pleasantness | 16 | M1 (mean) | L0 (fwd) | Mean consonance over 1s |
| 4 | sensory_pleasantness | 16 | M20 (entropy) | L0 (fwd) | Consonance entropy 1s |
| 14 | tonalness | 8 | M1 (mean) | L0 (fwd) | Mean tonalness 500ms |
| 14 | tonalness | 16 | M1 (mean) | L0 (fwd) | Mean tonalness 1s |
| 0 | roughness | 3 | M0 (value) | L2 (bidi) | Roughness at 100ms |
| 0 | roughness | 16 | M1 (mean) | L0 (fwd) | Mean roughness 1s |
| 21 | spectral_change | 8 | M1 (mean) | L0 (fwd) | Mean change 500ms |
| 21 | spectral_change | 16 | M20 (entropy) | L0 (fwd) | Change entropy 1s |
| 41 | x_l5l7[0] | 8 | M0 (value) | L0 (fwd) | Coupling 500ms |
| 41 | x_l5l7[0] | 16 | M1 (mean) | L0 (fwd) | Mean coupling 1s |
| 41 | x_l5l7[0] | 16 | M20 (entropy) | L0 (fwd) | Coupling entropy 1s |
| 41 | x_l5l7[0] | 16 | M18 (trend) | L0 (fwd) | Coupling trend 1s |
| 5 | periodicity | 16 | M1 (mean) | L0 (fwd) | Mean periodicity 1s |

**Total MAA H³ demand**: 14 tuples of 2304 theoretical = 0.61%

### 5.2 PPC + TPC + MEM Mechanism Binding

| Mechanism | Sub-section | Range | MAA Role | Weight |
|-----------|-------------|-------|----------|--------|
| **PPC** | Pitch Extraction | PPC[0:10] | Pattern detection in complex harmony | 0.6 |
| **PPC** | Interval Analysis | PPC[10:20] | Interval pattern recognition | 0.7 |
| **PPC** | Contour Tracking | PPC[20:30] | Melodic contour in atonal context | 0.5 |
| **TPC** | Spectral Shape | TPC[0:10] | Timbral complexity assessment | 0.6 |
| **TPC** | Temporal Envelope | TPC[10:20] | Rhythmic pattern extraction | 0.5 |
| **TPC** | Source Identity | TPC[20:30] | Framing / context categorization | 0.7 |
| **MEM** | Working Memory | MEM[0:10] | Complexity tolerance assessment | **1.0** (primary) |
| **MEM** | Long-Term Memory | MEM[10:20] | Familiarity / exposure tracking | **1.0** (primary) |
| **MEM** | Prediction Buffer | MEM[20:30] | Appreciation prediction | 0.8 |

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
MAA OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_complexity_tolerance │ [0, 1] │ Ability to process complexity.
    │                          │        │ f01 = σ(0.35 * consonance_entropy_1s
    │                          │        │       + 0.35 * coupling_entropy_1s
    │                          │        │       + 0.30 * mean(MEM.wm[0:10]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_familiarity_index    │ [0, 1] │ Mere exposure / familiarity.
    │                          │        │ f02 = σ(0.40 * coupling_trend_1s
    │                          │        │       + 0.30 * mean(MEM.ltm[10:20])
    │                          │        │       + 0.30 * periodicity_mean_1s)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_framing_effect       │ [0, 1] │ Cognitive framing benefit.
    │                          │        │ f03 = σ(0.40 * mean(TPC.src[20:30])
    │                          │        │       + 0.30 * change_mean_500ms
    │                          │        │       + 0.30 * mean(PPC.interval[10:20]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_appreciation_compos  │ [0, 1] │ Overall appreciation index.
    │                          │        │ f04 = σ(0.35 * f01 * f02
    │                          │        │       + 0.35 * f03
    │                          │        │       + 0.30 * mean(MEM.pred[20:30]))

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ pattern_search           │ [0, 1] │ PPC pattern recognition attempt.
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ context_assessment       │ [0, 1] │ TPC framing application.
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ aesthetic_evaluation     │ [0, 1] │ MEM appreciation response.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ appreciation_growth      │ [0, 1] │ Liking increase prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ pattern_recognition      │ [0, 1] │ Structure perception prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ aesthetic_development    │ [0, 1] │ Taste evolution prediction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Multifactorial Appreciation Model

```
Appreciation = Complexity_Tolerance × Familiarity × Framing

Complexity_Tolerance = f(openness, complexity_level)
    High openness → higher threshold for complexity aversion

Familiarity = 1 - exp(-exposure / τ_exposure)
    Mere exposure effect: repeated listening → increased familiarity

Framing = context_weight × cognitive_mastering
    Better framing → meaning extraction from complexity

Appreciation_Composite = α·(Tolerance × Familiarity) + β·Framing + γ·Prediction
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Complexity Tolerance
f01 = σ(0.35 * consonance_entropy_1s
       + 0.35 * coupling_entropy_1s
       + 0.30 * mean(MEM.working_memory[0:10]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Familiarity Index
f02 = σ(0.40 * coupling_trend_1s
       + 0.30 * mean(MEM.long_term_memory[10:20])
       + 0.30 * periodicity_mean_1s)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f03: Framing Effect
f03 = σ(0.40 * mean(TPC.source_identity[20:30])
       + 0.30 * change_mean_500ms
       + 0.30 * mean(PPC.interval_analysis[10:20]))
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f04: Appreciation Composite
f04 = σ(0.35 * f01 * f02          # tolerance × familiarity interaction
       + 0.35 * f03               # framing contribution
       + 0.30 * mean(MEM.prediction_buffer[20:30]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | MAA Function |
|--------|-----------------|----------|---------------|--------------|
| **Auditory Cortex (STG)** | ±52, -22, 8 | 1 | Indirect (behavioral) | Complexity processing |
| **IFG (Inferior Frontal Gyrus)** | ±44, 18, 8 | 1 | Literature inference | Cognitive framing |
| **Hippocampus** | ±28, -24, -12 | 1 | Literature inference | Familiarity/exposure |
| **mPFC** | 0, 46, 12 | 1 | Literature inference | Aesthetic evaluation |

---

## 9. Cross-Unit Pathways

### 9.1 MAA Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MAA INTERACTIONS                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (PCU):                                                         │
│  UDP.pleasure_index ─────────► MAA (pleasure baseline for appreciation)    │
│  PWUP.uncertainty_index ─────► MAA (uncertainty context)                   │
│  IGFE.gamma_sync ────────────► MAA (entrainment aids pattern detection)    │
│  MAA.appreciation_composite ──► PSH (appreciation modulates silencing)     │
│                                                                             │
│  CROSS-UNIT (PCU → ARU):                                                   │
│  MAA.appreciation_composite ──► ARU (appreciation as reward signal)        │
│  MAA.aesthetic_evaluation ────► ARU (aesthetic value for reward circuit)    │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  PPC mechanism (30D) ────────► MAA (pattern detection)                     │
│  TPC mechanism (30D) ────────► MAA (framing / context)                     │
│  MEM mechanism (30D) ────────► MAA (tolerance / familiarity / prediction)  │
│  R³ (~16D) ──────────────────► MAA (direct spectral features)             │
│  H³ (14 tuples) ─────────────► MAA (temporal dynamics)                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Openness modulation** | Higher openness should predict better atonal appreciation | **Supported** (Mencke 2019) |
| **Framing effect** | Aesthetic framing should increase appreciation | Testable via between-subjects |
| **Exposure effect** | Repeated listening should increase liking | Testable via longitudinal design |
| **Interaction** | Factors should interact multiplicatively | Testable via factorial design |
| **Complexity ceiling** | Very high complexity should reduce appreciation regardless | Testable via parametric design |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class MAA(BaseModel):
    """Multifactorial Atonal Appreciation Model.

    Output: 10D per frame.
    Reads: PPC mechanism (30D), TPC mechanism (30D), MEM mechanism (30D), R³ direct.
    """
    NAME = "MAA"
    UNIT = "PCU"
    TIER = "γ2"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("PPC", "TPC", "MEM")

    TAU_EXPOSURE = 600.0           # s (10 min for familiarity)
    COMPLEXITY_THRESHOLD = 0.7     # Entropy threshold for complexity

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """14 tuples for MAA computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── Complexity assessment ──
            (4, 3, 0, 2),      # sensory_pleasantness, 100ms, value, bidi
            (4, 16, 1, 0),     # sensory_pleasantness, 1000ms, mean, fwd
            (4, 16, 20, 0),    # sensory_pleasantness, 1000ms, entropy, fwd
            (14, 8, 1, 0),     # tonalness, 500ms, mean, fwd
            (14, 16, 1, 0),    # tonalness, 1000ms, mean, fwd
            (0, 3, 0, 2),      # roughness, 100ms, value, bidi
            (0, 16, 1, 0),     # roughness, 1000ms, mean, fwd
            # ── Familiarity / pattern recognition ──
            (21, 8, 1, 0),     # spectral_change, 500ms, mean, fwd
            (21, 16, 20, 0),   # spectral_change, 1000ms, entropy, fwd
            (5, 16, 1, 0),     # periodicity, 1000ms, mean, fwd
            # ── Appreciation pathway ──
            (41, 8, 0, 0),     # x_l5l7[0], 500ms, value, fwd
            (41, 16, 1, 0),    # x_l5l7[0], 1000ms, mean, fwd
            (41, 16, 20, 0),   # x_l5l7[0], 1000ms, entropy, fwd
            (41, 16, 18, 0),   # x_l5l7[0], 1000ms, trend, fwd
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute MAA 10D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30), "TPC": (B,T,30), "MEM": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) MAA output
        """
        ppc = mechanism_outputs["PPC"]
        tpc = mechanism_outputs["TPC"]
        mem = mechanism_outputs["MEM"]

        # Mechanism sub-sections
        ppc_interval = ppc[..., 10:20]
        tpc_src = tpc[..., 20:30]
        mem_wm = mem[..., 0:10]
        mem_ltm = mem[..., 10:20]
        mem_pred = mem[..., 20:30]

        # H³ direct features
        consonance_entropy_1s = h3_direct[(4, 16, 20, 0)].unsqueeze(-1)
        coupling_entropy_1s = h3_direct[(41, 16, 20, 0)].unsqueeze(-1)
        coupling_trend_1s = h3_direct[(41, 16, 18, 0)].unsqueeze(-1)
        periodicity_mean_1s = h3_direct[(5, 16, 1, 0)].unsqueeze(-1)
        change_mean_500ms = h3_direct[(21, 8, 1, 0)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: Complexity Tolerance (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.35 * consonance_entropy_1s
            + 0.35 * coupling_entropy_1s
            + 0.30 * mem_wm.mean(-1, keepdim=True)
        )

        # f02: Familiarity Index (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.40 * coupling_trend_1s
            + 0.30 * mem_ltm.mean(-1, keepdim=True)
            + 0.30 * periodicity_mean_1s
        )

        # f03: Framing Effect (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.40 * tpc_src.mean(-1, keepdim=True)
            + 0.30 * change_mean_500ms
            + 0.30 * ppc_interval.mean(-1, keepdim=True)
        )

        # f04: Appreciation Composite (coefficients sum = 1.0)
        f04 = torch.sigmoid(
            0.35 * f01 * f02
            + 0.35 * f03
            + 0.30 * mem_pred.mean(-1, keepdim=True)
        )

        # ═══ LAYER P: Present ═══
        pattern_search = ppc_interval.mean(-1, keepdim=True)
        context_assess = tpc_src.mean(-1, keepdim=True)
        aesthetic_eval = f04

        # ═══ LAYER F: Future ═══
        appreciation_growth = torch.sigmoid(0.5 * f02 + 0.5 * f04)
        pattern_recog = torch.sigmoid(0.5 * f01 + 0.5 * f02)
        aesthetic_dev = torch.sigmoid(0.5 * f03 + 0.5 * f04)

        return torch.cat([
            f01, f02, f03, f04,                             # E: 4D
            pattern_search, context_assess, aesthetic_eval,  # P: 3D
            appreciation_growth, pattern_recog, aesthetic_dev,# F: 3D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 (Mencke 2019) | Preliminary evidence |
| **Effect Sizes** | 1 | Multifactorial model |
| **Evidence Modality** | Behavioral + theoretical | Indirect |
| **Falsification Tests** | 5/5 testable, 1 supported | Low (awaiting empirical tests) |
| **R³ Features Used** | ~16D of 49D | Consonance + timbre + change + interactions |
| **H³ Demand** | 14 tuples (0.61%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Pattern detection |
| **TPC Mechanism** | 30D (3 sub-sections) | Framing / context |
| **MEM Mechanism** | 30D (3 sub-sections) | Tolerance / familiarity / prediction |
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
| Temporal | HC⁰ mechanisms (HRM, EFC, AED, CPD) | PPC (30D) + TPC (30D) + MEM (30D) mechanisms |
| Atonality index | S⁰.L3.coherence[14] (inverse) | R³[4] sensory_pleasantness + R³[14] tonalness |
| Complexity | S⁰.L9.entropy[116:120] | H³ consonance/coupling entropy tuples |
| Harmonic tension | S⁰.L5.roughness[30:33] + S⁰.L6[68:71] | R³[0] roughness + R³[18:21] tristimulus |
| Appreciation | S⁰.X_L5L9[224:232] | R³[41:49] x_l5l7 + MEM.prediction_buffer |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 24/2304 = 1.04% | 14/2304 = 0.61% |
| Output | 10D | 10D (same) |

### Why PPC + TPC + MEM replaces HC⁰ mechanisms

- **HRM → MEM.long_term_memory** [10:20]: Hippocampal replay for familiarity/exposure maps to MEM's long-term memory.
- **EFC → MEM.working_memory** [0:10]: Efference copy for complexity tolerance maps to MEM's working memory assessment.
- **AED → TPC.source_identity** [20:30]: Affective entrainment dynamics for framing maps to TPC's source identity / context categorization.
- **CPD → MEM.prediction_buffer** [20:30]: Chills/peak detection for appreciation peaks maps to MEM's prediction buffer.

---

**Model Status**: **PRELIMINARY**
**Output Dimensions**: **10D**
**Evidence Tier**: **γ (Integrative)**
**Confidence**: **50-70%**
