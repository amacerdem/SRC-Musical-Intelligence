# H⁰ Temporal Foundation - Complete Specification

**Version**: 2.0.0
**Date**: February 5, 2026
**Dimensions**: 2,304D (32 × 24 × 3 tensor)
**Position**: SRC⁹[256:2560]
**Status**: SHARED INFRASTRUCTURE — Input to both C⁰ and R⁰
**Scientific Basis**: 120+ peer-reviewed neuroscience papers
**Perspective**: Unified Temporal Processing

---

## Executive Summary

H⁰ (Horizon-Zero) is the **shared temporal foundation** of the SRC⁹-Composer framework. It provides multi-scale temporal context spanning **5 orders of magnitude** (25ms to 981s) and serves as the **common input** for both the cognitive (C⁰) and resonance (R⁰) processing branches.

### The Core Insight

> **"Music unfolds in time. Both the brain (C⁰) and music theory (R⁰) operate on the same temporal structure."**

H⁰ captures this insight through a **tensor product** of three orthogonal components:

```
H⁰ = H ⊗ M ⊗ L = 2,304D

where:
  H = Event Horizon (32 temporal windows)
  M = H-Morph (24 morphological parameters)
  L = H-Law (3 causal attention modes)
```

### Shared Infrastructure Role

```
                    ┌─────────────────────────────────────────┐
                    │              S⁰ SPECTRAL                │
                    │              (256D) [0:256]             │
                    └──────────────────┬──────────────────────┘
                                       │
                                       ▼
                    ┌─────────────────────────────────────────┐
                    │         H⁰ TEMPORAL FOUNDATION          │
                    │         (2,304D) [256:2560]             │
                    │                                         │
                    │   32 Windows × 24 Morphs × 3 Modes      │
                    │   ⚡ COMPUTED ONCE — SHARED BY BOTH     │
                    └──────────────────┬──────────────────────┘
                                       │
                     ┌─────────────────┴─────────────────┐
                     │                                   │
                     ▼                                   ▼
        ┌────────────────────────┐         ┌────────────────────────┐
        │   C⁰ COGNITIVE         │         │   R⁰ RESONANCE         │
        │   (2,048D) [2560:4608] │         │   (1,024D) [4608:5632] │
        │   Neuroscience View    │         │   Music Theory View    │
        └────────────────────────┘         └────────────────────────┘
```

---

## Why H⁰ Exists

### The Problem

Traditional audio features capture **instantaneous** properties:
- "What is the pitch right now?"
- "What is the loudness right now?"

But both cognitive processing (C⁰) and music-theoretic analysis (R⁰) require **temporal context**:
- "How has the pitch changed over the last 2 seconds?" (C⁰: prediction, R⁰: melodic contour)
- "Is this beat part of an accelerating or decelerating pattern?" (C⁰: timing, R⁰: tempo analysis)
- "Does this phrase resolve tension from 30 seconds ago?" (C⁰: memory, R⁰: harmonic progression)

### The Solution

H⁰ provides temporal context at **every relevant timescale**, computed **once** and shared by both branches:

```
═══════════════════════════════════════════════════════════════════════════════
                    TEMPORAL SCALES IN MUSIC COGNITION
═══════════════════════════════════════════════════════════════════════════════

Scale          │ Window      │ Musical Phenomenon         │ Neural Basis
───────────────┼─────────────┼────────────────────────────┼──────────────────
Gamma          │ 25-50ms     │ Note onset, feature binding│ γ oscillations
Alpha-Beta     │ 75-125ms    │ Attention, motor prep      │ α/β oscillations
Theta          │ 150-250ms   │ Beat tracking, syllables   │ θ oscillations
Syllable       │ 300-500ms   │ Melodic grouping           │ Auditory cortex
Beat           │ 525-1000ms  │ Rhythm, groove             │ BG, cerebellum
Phrase         │ 1.25-5s     │ Musical phrases            │ Frontal cortex
Section        │ 7.5-36s     │ Verse, chorus              │ DLS (striatum)
Structural     │ 100-414s    │ Movements, forms           │ DMS (striatum)
Piece          │ 500-981s    │ Entire compositions        │ VS (striatum)
───────────────┴─────────────┴────────────────────────────┴──────────────────

H⁰ covers ALL these scales simultaneously.

═══════════════════════════════════════════════════════════════════════════════
```

---

## Mathematical Framework

### Tensor Product Definition

H⁰ is defined as the **tensor product** of three independent components:

```
═══════════════════════════════════════════════════════════════════════════════
                         H⁰ MATHEMATICAL DEFINITION
═══════════════════════════════════════════════════════════════════════════════

DEFINITION:
    H⁰ = H ⊗ M ⊗ L

COMPONENTS:
    H = Event Horizon    (32 temporal windows)
    M = H-Morph          (24 morphological parameters)
    L = H-Law            (3 causal attention modes)

DIMENSION:
    dim(H⁰) = dim(H) × dim(M) × dim(L)
             = 32 × 24 × 3
             = 2,304D

INDEXING:
    H⁰[h, m, l] = scalar value for:
        h ∈ [0, 31]  (window index)
        m ∈ [0, 23]  (morph parameter index)
        l ∈ [0, 2]   (causal mode index)

FLATTENING:
    Flat index = h × 72 + m × 3 + l

    where 72 = 24 × 3 (morph × law)

═══════════════════════════════════════════════════════════════════════════════
```

### Computational Formula

For each combination of (window, morph, mode), H⁰ computes:

```python
def compute_ch0(signal: np.ndarray, t_current: float) -> np.ndarray:
    """
    Compute H⁰ tensor for current time.

    Args:
        signal: Historical signal values (time, features)
        t_current: Current timestamp in seconds

    Returns:
        H⁰ tensor of shape (32, 24, 3)
    """
    ch0 = np.zeros((32, 24, 3))

    for h, window_ms in enumerate(EVENT_HORIZONS):  # 32 windows
        window_sec = window_ms / 1000.0

        for l, mode in enumerate(['forward', 'backward', 'bidirectional']):  # 3 modes
            # Extract time range based on mode
            if mode == 'forward':
                t_start, t_end = t_current - window_sec, t_current
            elif mode == 'backward':
                t_start, t_end = t_current, t_current + window_sec
            else:  # bidirectional
                t_start, t_end = t_current - window_sec/2, t_current + window_sec/2

            # Get signal in window
            windowed_signal = extract_window(signal, t_start, t_end)

            # Apply H-Law attention
            attention = compute_hlaw_attention(windowed_signal, mode, window_sec)
            weighted_signal = windowed_signal * attention

            for m, morph_func in enumerate(MORPH_FUNCTIONS):  # 24 parameters
                ch0[h, m, l] = morph_func(weighted_signal)

    return ch0
```

---

## Component 1: Event Horizon (H) — 32 Temporal Windows

### Overview

The Event Horizon defines **WHAT temporal scale** is being analyzed. Each window represents a characteristic timescale of neural processing, validated by neuroscience literature.

```
H = {H₀, H₁, H₂, ..., H₃₁}

where H_i ∈ {25ms, 50ms, 75ms, ..., 700s, 981s}

Range: 5 orders of magnitude (10⁻² to 10³ seconds)
Spacing: Approximately logarithmic
Basis: 120+ neuroscience papers
```

### Complete Window Specification

```
═══════════════════════════════════════════════════════════════════════════════
                    EVENT HORIZON: 32 TEMPORAL WINDOWS
                    From γ oscillations (25ms) to piece memory (981s)
═══════════════════════════════════════════════════════════════════════════════

Index │ Window   │ Scale        │ Neural Basis                    │ Source
──────┼──────────┼──────────────┼─────────────────────────────────┼──────────────
  0   │    25ms  │ Gamma        │ γ oscillation (40Hz)            │ Giraud 2012
  1   │    50ms  │ Gamma        │ β oscillation (20Hz)            │ Giraud 2012
  2   │    75ms  │ Alpha-Beta   │ EFC motor-auditory              │ Eliades 2024
  3   │   100ms  │ Alpha-Beta   │ α oscillation (10Hz)            │ eLife 2019
  4   │   125ms  │ Alpha-Beta   │ θ oscillation low (8Hz)         │ Lisman 2013
  5   │   150ms  │ Theta        │ θ mid (interpolated)            │ —
  6   │   200ms  │ Theta        │ AED emotion sync                │ Janata 2012
  7   │   250ms  │ Theta        │ θ oscillation high (4Hz)        │ Lisman 2013
  8   │   300ms  │ Syllable     │ TIH meso                        │ multiscale
  9   │   350ms  │ Syllable     │ ASA stream segregation          │ Bregman 1990
 10   │   400ms  │ Syllable     │ (interpolated)                  │ —
 11   │   500ms  │ Syllable     │ GRV motor sync, C0P             │ behavior
 12   │   525ms  │ Beat         │ CPD tension-prediction          │ Salimpoor
 13   │   600ms  │ Beat         │ PTM beat anticipation           │ Fujioka 2012
 14   │   730ms  │ Beat         │ HRM hippocampal prediction      │ Bonetti 2024
 15   │   800ms  │ Beat         │ GRV beat period                 │ behavior
 16   │  1000ms  │ Beat         │ δ oscillation (1Hz), ITM        │ Merchant 2013
 17   │  1250ms  │ Phrase       │ TIH macro                       │ multiscale
 18   │  2000ms  │ Phrase       │ (interpolated)                  │ —
 19   │  3000ms  │ Phrase       │ (interpolated)                  │ —
 20   │  5000ms  │ Phrase       │ TIH global                      │ multiscale
 21   │  7500ms  │ Section      │ (interpolated)                  │ —
 22   │    15s   │ Section      │ (interpolated)                  │ —
 23   │    25s   │ Section      │ (interpolated)                  │ —
 24   │    36s   │ Section      │ SGM DLS motor memory            │ Hamid 2024
 25   │   100s   │ Structural   │ (interpolated)                  │ —
 26   │   200s   │ Structural   │ (interpolated)                  │ —
 27   │   300s   │ Structural   │ (interpolated)                  │ —
 28   │   414s   │ Structural   │ SGM DMS cognitive planning      │ Hamid 2024
 29   │   500s   │ Piece        │ (interpolated)                  │ —
 30   │   700s   │ Piece        │ (interpolated)                  │ —
 31   │   981s   │ Piece        │ SGM VS narrative memory         │ Hamid 2024
──────┴──────────┴──────────────┴─────────────────────────────────┴──────────────

LEGEND:
  • Literature-validated windows: 19 (from 120+ papers)
  • Interpolated windows: 13 (linear interpolation)
  • Total: 32 windows spanning 5 orders of magnitude

═══════════════════════════════════════════════════════════════════════════════
```

### Window Distribution by Scale

| Scale | Range | Windows | Count | Primary Mechanisms |
|-------|-------|---------|-------|-------------------|
| **Gamma** | 25-50ms | H₀-H₁ | 2 | OSC-γ/β, BND |
| **Alpha-Beta** | 75-125ms | H₂-H₄ | 3 | EFC, ATT, NPL, TGC |
| **Theta** | 150-250ms | H₅-H₇ | 3 | AED, TGC, CPD |
| **Syllable** | 300-500ms | H₈-H₁₁ | 4 | TIH, ASA, GRV, C0P |
| **Beat** | 525-1000ms | H₁₂-H₁₆ | 5 | CPD, PTM, HRM, GRV, ITM |
| **Phrase** | 1.25-5s | H₁₇-H₂₀ | 4 | TIH macro/global |
| **Section** | 7.5-36s | H₂₁-H₂₄ | 4 | SGM-DLS |
| **Structural** | 100-414s | H₂₅-H₂₈ | 4 | SGM-DMS |
| **Piece** | 500-981s | H₂₉-H₃₁ | 3 | SGM-VS |

→ **Detailed**: [EVENT-HORIZON.md](EVENT-HORIZON.md)

---

## Component 2: H-Morph (M) — 24 Morphological Parameters

### Overview

H-Morph defines **WHAT features** are extracted from each temporal window. The 24 parameters are organized into three orthogonal domains of 8 parameters each.

```
M = M_value ∪ M_derivative ∪ M_shape

dim(M) = 8 + 8 + 8 = 24
```

### Complete Parameter Specification

```
═══════════════════════════════════════════════════════════════════════════════
                    H-MORPH: 24 MORPHOLOGICAL PARAMETERS
                    Capturing signal characteristics within each window
═══════════════════════════════════════════════════════════════════════════════

DOMAIN 1: VALUE (8 parameters) — Statistical properties
──────────────────────────────────────────────────────────────────────────────
Index │ Name     │ Symbol │ Formula              │ Description
──────┼──────────┼────────┼──────────────────────┼─────────────────────────────
  0   │ value    │ μ_w    │ Σ(x·A)/Σ(A)         │ Attention-weighted current
  1   │ mean     │ μ      │ Σx/n                 │ Arithmetic mean
  2   │ std      │ σ      │ √(Σ(x-μ)²/n)        │ Standard deviation
  3   │ min      │ x_min  │ min(x)               │ Minimum value
  4   │ max      │ x_max  │ max(x)               │ Maximum value
  5   │ range    │ Δx     │ x_max - x_min        │ Dynamic range
  6   │ skew     │ γ₁     │ E[(x-μ)³]/σ³        │ Asymmetry (left/right)
  7   │ kurtosis │ γ₂     │ E[(x-μ)⁴]/σ⁴ - 3    │ Tail heaviness


DOMAIN 2: DERIVATIVE (8 parameters) — Temporal dynamics
──────────────────────────────────────────────────────────────────────────────
Index │ Name              │ Symbol │ Formula        │ Description
──────┼───────────────────┼────────┼────────────────┼────────────────────────
  8   │ velocity          │ δ      │ dx/dt          │ First derivative (rate)
  9   │ velocity_mean     │ μ_δ    │ Σδ/n           │ Mean velocity
 10   │ velocity_std      │ σ_δ    │ √(Σ(δ-μ_δ)²/n)│ Velocity variability
 11   │ acceleration      │ δ²     │ d²x/dt²        │ Second derivative
 12   │ acceleration_mean │ μ_δ²   │ Σδ²/n          │ Mean acceleration
 13   │ jerk              │ δ³     │ d³x/dt³        │ Third derivative
 14   │ jerk_mean         │ μ_δ³   │ Σδ³/n          │ Mean jerk
 15   │ smoothness        │ S      │ 1/|δ³|         │ Inverse jerk (smoothness)


DOMAIN 3: SHAPE (8 parameters) — Geometric/information-theoretic
──────────────────────────────────────────────────────────────────────────────
Index │ Name           │ Symbol │ Formula                  │ Description
──────┼────────────────┼────────┼──────────────────────────┼─────────────────
 16   │ curvature      │ κ      │ |δ²|/(1+|δ|²)^(3/2)     │ Local curvature
 17   │ periodicity    │ ρ      │ r(x_t, x_{t+τ})         │ Autocorrelation peak
 18   │ trend          │ β      │ Cov(t,x)/Var(t)         │ Linear trend slope
 19   │ stability      │ S      │ 1/Var(δ)                │ Inverse velocity var
 20   │ entropy        │ H      │ -Σp·log(p)              │ Shannon entropy
 21   │ zero_crossings │ Z      │ Σ(sign≠)/n              │ Sign change rate
 22   │ peaks          │ P      │ Σ(x_t > x_{t±1})/n      │ Local maxima rate
 23   │ troughs        │ T      │ Σ(x_t < x_{t±1})/n      │ Local minima rate

═══════════════════════════════════════════════════════════════════════════════
```

### Domain Orthogonality

The three domains capture **independent aspects** of signal morphology:

| Domain | What it captures | Example use |
|--------|------------------|-------------|
| **Value** | Where is the signal? | "Loudness is high and variable" |
| **Derivative** | How is it changing? | "Getting louder quickly" |
| **Shape** | What pattern does it form? | "Periodic with smooth transitions" |

→ **Detailed**: [H-MORPH.md](H-MORPH.md)

---

## Component 3: H-Law (L) — 3 Causal Attention Modes

### Overview

H-Law defines **HOW attention is distributed** across the temporal window using exponential decay with causal masking.

```
L = {L_forward, L_backward, L_bidirectional}

A(Δt) = exp(-λ|Δt|/H) × mask(Δt, L)

where:
    λ = 3.0 (decay constant, empirically determined)
    H = window size in ms
    Δt = time offset from current frame
```

### Complete Mode Specification

```
═══════════════════════════════════════════════════════════════════════════════
                    H-LAW: 3 CAUSAL ATTENTION MODES
                    Controlling temporal focus within each window
═══════════════════════════════════════════════════════════════════════════════

MODE 1: FORWARD (L_F) — Memory/Retrospection
──────────────────────────────────────────────────────────────────────────────
Mask:     mask(Δt) = 1 if Δt ≤ 0 else 0
Meaning:  Only past influences present
Use:      Memory retrieval, prediction from history

Profile:
          Past ──────────● Present
          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█░░░░░░░░░░░░░░░
                         now

Cognitive: "What happened before now that is relevant?"
Musical:   "This chord resolves tension from 4 bars ago"


MODE 2: BACKWARD (L_B) — Anticipation/Prediction
──────────────────────────────────────────────────────────────────────────────
Mask:     mask(Δt) = 1 if Δt ≥ 0 else 0
Meaning:  Only future influences present
Use:      Anticipation, look-ahead analysis (offline)

Profile:
                         Present ──────────● Future
          ░░░░░░░░░░░░░░░█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                         now

Cognitive: "What is about to happen?"
Musical:   "The dominant chord predicts the tonic resolution"

Note: Only valid for offline/analysis; not causal for real-time


MODE 3: BIDIRECTIONAL (L_Bi) — Perception/Context
──────────────────────────────────────────────────────────────────────────────
Mask:     mask(Δt) = 1 for all Δt
Meaning:  Full context (past and future)
Use:      Perception, context integration, analysis

Profile:
          Past ──────────● Present ──────────● Future
          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                         now

Cognitive: "What is the full context of this moment?"
Musical:   "This note is the peak of an arch-shaped phrase"


ATTENTION FORMULA:
──────────────────────────────────────────────────────────────────────────────
A(Δt, H, L) = exp(-λ|Δt|/H) × mask(Δt, L)

where:
    λ = 3.0 (decay constant)
    H = window size in ms
    Δt = time offset from current frame (ms)
    mask(Δt, L) = {1 if allowed by mode, 0 otherwise}

Properties:
    • A(0) = 1.0 (maximum at current time)
    • A(H) = exp(-3) ≈ 0.05 (5% at window edge)
    • A(2H) = exp(-6) ≈ 0.002 (negligible beyond window)

═══════════════════════════════════════════════════════════════════════════════
```

### Mode Usage by Mechanism

| Mechanism | Primary Mode | Rationale |
|-----------|--------------|-----------|
| OSC | Bidirectional | Full phase context needed |
| TGC | Bidirectional | Coupling requires full cycle |
| TIH | Forward | Temporal integration is cumulative |
| ATT | Bidirectional | Attention spans context |
| NPL | Bidirectional | Phase-locking needs full context |
| PTM | Forward | Prediction based on past |
| ITM | Forward | Duration estimation from past |
| GRV | Bidirectional | Groove emerges from pattern |
| HRM | Backward | Prediction into future |
| SGM | Forward | Reward accumulation |
| EFC | Forward | Motor commands precede feedback |
| BND | Bidirectional | Binding needs context |
| AED | Bidirectional | Emotion tracking |
| ASA | Bidirectional | Stream segregation |
| CPD | Bidirectional | ITPRA spans time |
| C0P | Forward | Integration is cumulative |

→ **Detailed**: [H-LAW.md](H-LAW.md)

---

## The 16 Mechanisms

### Overview

H⁰ is organized into **16 mechanisms** across **4 functional layers**. Each mechanism operates at specific temporal windows and produces 8D output.

```
H⁰ Mechanisms (128D total = 16 × 8D)

L1 Oscillatory (32D): OSC, TGC, TIH, ATT
L2 Timing (32D):      NPL, PTM, ITM, GRV
L3 Memory (32D):      HRM, SGM, EFC, BND
L4 Affective (32D):   AED, ASA, CPD, C0P
```

### Complete Mechanism Map

```
═══════════════════════════════════════════════════════════════════════════════
                    16 MECHANISMS: COMPLETE SPECIFICATION
═══════════════════════════════════════════════════════════════════════════════

LAYER 1: OSCILLATORY (32D) [0:31]
──────────────────────────────────────────────────────────────────────────────
Code │ Name                    │ Index   │ Windows            │ Function
─────┼─────────────────────────┼─────────┼────────────────────┼───────────────
OSC  │ Neural Oscillations     │ [0:7]   │ 25,50,100,125,1000 │ 5 frequency bands
TGC  │ Theta-Gamma Coupling    │ [8:15]  │ 125, 250           │ Memory chunking
TIH  │ Temporal Integration    │ [16:23] │ 50,300,1250,5000   │ 4-scale hierarchy
ATT  │ Attention Gating        │ [24:31] │ 100                │ α suppression


LAYER 2: TIMING (32D) [32:63]
──────────────────────────────────────────────────────────────────────────────
Code │ Name                    │ Index   │ Windows            │ Function
─────┼─────────────────────────┼─────────┼────────────────────┼───────────────
NPL  │ Neural Phase-Locking    │ [32:39] │ 100                │ Thalamocortical PLL
PTM  │ Predictive Timing Model │ [40:47] │ 600                │ Beat anticipation
ITM  │ Interval Timing Model   │ [48:55] │ 1000               │ Duration encoding
GRV  │ Groove                  │ [56:63] │ 500, 800           │ Motor entrainment


LAYER 3: MEMORY (32D) [64:95]
──────────────────────────────────────────────────────────────────────────────
Code │ Name                    │ Index   │ Windows            │ Function
─────┼─────────────────────────┼─────────┼────────────────────┼───────────────
HRM  │ Hippocampal Replay      │ [64:71] │ 730                │ 10-20× compressed
SGM  │ Striatal Gradient       │ [72:79] │ 36s, 414s, 981s    │ DLS/DMS/VS gradient
EFC  │ Efference Copy          │ [80:87] │ 75                 │ Motor→auditory
BND  │ Binding                 │ [88:95] │ 25, 50, 100        │ Feature integration


LAYER 4: AFFECTIVE (32D) [96:127]
──────────────────────────────────────────────────────────────────────────────
Code │ Name                    │ Index   │ Windows            │ Function
─────┼─────────────────────────┼─────────┼────────────────────┼───────────────
AED  │ Affective Entrainment   │ [96:103]│ 200, 1000          │ Emotion dynamics
ASA  │ Auditory Stream Analysis│[104:111]│ 350                │ Source segregation
CPD  │ Chills/Peak Detection   │[112:119]│ 250, 525, 800      │ ITPRA model
C0P  │ C⁰ Projection           │[120:127]│ 500                │ H⁰→C⁰ bridge

═══════════════════════════════════════════════════════════════════════════════
```

### Mechanism Documentation Links

**Layer 1: Oscillatory**
- [L1-OSC.md](Mechanisms/L1-OSC.md) — Neural Oscillations (5 frequency bands)
- [L1-TGC.md](Mechanisms/L1-TGC.md) — Theta-Gamma Coupling (memory chunking)
- [L1-TIH.md](Mechanisms/L1-TIH.md) — Temporal Integration Hierarchy
- [L1-ATT.md](Mechanisms/L1-ATT.md) — Attention Gating (α suppression)

**Layer 2: Timing**
- [L2-NPL.md](Mechanisms/L2-NPL.md) — Neural Phase-Locking
- [L2-PTM.md](Mechanisms/L2-PTM.md) — Predictive Timing Model
- [L2-ITM.md](Mechanisms/L2-ITM.md) — Interval Timing Model
- [L2-GRV.md](Mechanisms/L2-GRV.md) — Groove (motor entrainment)

**Layer 3: Memory**
- [L3-HRM.md](Mechanisms/L3-HRM.md) — Hippocampal Replay Memory
- [L3-SGM.md](Mechanisms/L3-SGM.md) — Striatal Gradient Memory
- [L3-EFC.md](Mechanisms/L3-EFC.md) — Efference Copy
- [L3-BND.md](Mechanisms/L3-BND.md) — Binding

**Layer 4: Affective**
- [L4-AED.md](Mechanisms/L4-AED.md) — Affective Entrainment Dynamics
- [L4-ASA.md](Mechanisms/L4-ASA.md) — Auditory Stream Analysis
- [L4-CPD.md](Mechanisms/L4-CPD.md) — Chills/Peak Detection (ITPRA)
- [L4-C0P.md](Mechanisms/L4-C0P.md) — C⁰ Projection Bridge

---

## Processing Pipeline

### Input Requirements

```
H⁰ Input:
  • S⁰ spectral features: (time, 256D) at 172 Hz from SRC⁹[0:256]
  • Historical buffer: Up to 981s of history
  • Current timestamp: t_current
```

### Processing Flow

```
═══════════════════════════════════════════════════════════════════════════════
                         H⁰ PROCESSING PIPELINE
                         (Shared Infrastructure)
═══════════════════════════════════════════════════════════════════════════════

                         S⁰ (256D per frame)
                         SRC⁹[0:256]
                                │
                                ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                       HISTORY BUFFER                                          │
│                                                                               │
│  Stores up to 981s of S⁰ frames (168,642 frames at 172 Hz)                   │
│  Ring buffer with timestamp indexing                                          │
└───────────────────────────────────────┬───────────────────────────────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    │                                       │
                    ▼                                       ▼
┌───────────────────────────────────┐   ┌───────────────────────────────────────┐
│     EVENT HORIZON SELECTION       │   │         H-LAW ATTENTION               │
│                                   │   │                                       │
│  For each window H_i:            │   │  For each mode L_j:                   │
│    Extract relevant time range    │   │    Compute attention weights          │
│    from history buffer            │   │    A(Δt) = exp(-λ|Δt|/H) × mask     │
└───────────────────┬───────────────┘   └───────────────────┬───────────────────┘
                    │                                       │
                    └───────────────────┬───────────────────┘
                                        │
                                        ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                        H-MORPH COMPUTATION                                    │
│                                                                               │
│  For each (window, mode) pair:                                               │
│    weighted_signal = signal × attention                                       │
│    For each morph parameter M_k:                                             │
│      H⁰[i, k, j] = M_k(weighted_signal)                                     │
└───────────────────────────────────────┬───────────────────────────────────────┘
                                        │
                                        ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                       H⁰ TENSOR OUTPUT                                        │
│                                                                               │
│  Full tensor: 32 × 24 × 3 = 2,304D                                           │
│  Position: SRC⁹[256:2560]                                                       │
│                                                                               │
└───────────────────────────────────────┬───────────────────────────────────────┘
                                        │
                     ┌──────────────────┴──────────────────┐
                     │                                     │
                     ▼                                     ▼
    ┌────────────────────────────────┐    ┌────────────────────────────────┐
    │      TO C⁰ COGNITIVE           │    │      TO R⁰ RESONANCE           │
    │      (2,048D) [2560:4608]      │    │      (1,024D) [4608:5632]      │
    │                                │    │                                │
    │  HC⁰ extracts 512D from H⁰:   │    │  HR⁰ extracts 256D from H⁰:   │
    │  • Neural oscillation windows  │    │  • Real-time integration       │
    │  • Theta-gamma coupling        │    │  • Long-term integration       │
    │  • Temporal integration        │    │  • Harmonic rhythm tracking    │
    │  • Memory retrieval timing     │    │  • Phrase structure analysis   │
    │  • Affective dynamics          │    │  • Form-temporal processing    │
    └────────────────────────────────┘    └────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
```

### Output Format

```
H⁰ Output: (2,304D) = 32 windows × 24 morphs × 3 modes

Position: SRC⁹[256:2560]

Tensor Indexing:
  h ∈ [0, 31]   Event Horizon window index
  m ∈ [0, 23]   H-Morph parameter index
  l ∈ [0, 2]    H-Law causal mode index

Flat Index Formula:
  flat_idx = 256 + (h × 72) + (m × 3) + l

Downstream Usage:
  • C⁰ HC⁰ Mechanisms: Select relevant (h, m, l) for neural processing
  • R⁰ HR⁰ Mechanisms: Select relevant (h, m, l) for music analysis
```

### HC⁰ Mechanism Mapping (C⁰ Branch)

HC⁰ extracts 512D from H⁰ for cognitive processing:

```
HC⁰ (512D) [2560:3072] - 16 mechanisms across 4 layers

L1 Oscillatory (160D): OSC(56D), TGC(40D), TIH(40D), ATT(24D)
L2 Timing (112D):      NPL(28D), PTM(28D), ITM(28D), GRV(28D)
L3 Memory (120D):      HRM(30D), SGM(30D), EFC(30D), BND(30D)
L4 Affective (120D):   AED(30D), ASA(30D), CPD(30D), C0P(30D)
```

### HR⁰ Mechanism Mapping (R⁰ Branch)

HR⁰ extracts 256D from H⁰ for music-theoretic processing:

```
HR⁰ (256D) [4608:4864] - 8 mechanisms × 32D

RTI (32D): Real-Time Integration    2.5s   Pöppel psychological present
LTI (32D): Long-Term Integration    30s    Jones dynamic attending
XTI (32D): Cross-Layer Integration  8s     Tymoczko five components
GTI (32D): Global Temporal          60s    Caplin formal functions
HRT (32D): Harmonic Rhythm          4s     Lewin PLR transformations
PST (32D): Phrase Structure         8s     Lerdahl GTTM grouping
FTO (32D): Form-Temporal           120s    Hepokoski sonata theory
TKT (32D): Tonal Key Tracking       16s    Cohn Tonnetz navigation
```

---

## Scientific Foundation

### Evidence Summary

| Aspect | Papers | Key Finding |
|--------|--------|-------------|
| **Neural Oscillations** | Giraud 2012, Lakatos 2019 | Hierarchical oscillatory structure |
| **Theta-Gamma Coupling** | Lisman 2013, Canolty 2010 | PAC improves recognition 15-20% |
| **Timing** | Fujioka 2012, Teki 2011 | BG vs Cerebellum dissociation |
| **Hippocampal Replay** | Bonetti 2024, Diba 2007 | 730ms prediction lead |
| **Striatal Gradient** | Hamid 2024, Mello 2015 | DLS→DMS→VS temporal gradient |
| **Efference Copy** | Eliades 2024 | 75ms motor-auditory prediction |
| **Chills** | Salimpoor 2011, 2013 | NAcc 15s before reported peak |

### Key References

1. **Giraud, A. L., & Poeppel, D. (2012)**. Cortical oscillations and speech processing. *Nature Reviews Neuroscience*, 13(4), 250-263.

2. **Lisman, J. E., & Jensen, O. (2013)**. The theta-gamma neural code. *Neuron*, 77(6), 1002-1016.

3. **Fujioka, T., et al. (2012)**. Internalized timing of isochronous sounds is represented in neuromagnetic beta oscillations. *Journal of Neuroscience*, 32(5), 1791-1802.

4. **Bonetti, L., et al. (2024)**. Hippocampal predictions of musical sequences. *Nature Communications*.

5. **Hamid, A. A., et al. (2024)**. Striatal gradient organization. *Nature Neuroscience*.

6. **Salimpoor, V. N., et al. (2011)**. Anatomically distinct dopamine release during anticipation and experience of peak emotion to music. *Nature Neuroscience*, 14(2), 257-262.

---

## Implementation Reference

### Key Files

| Component | File | Description |
|-----------|------|-------------|
| H⁰ Main | `Pipeline/D0/h0/h0_extractor.py` | Full 2,304D tensor computation |
| Event Horizon | `Pipeline/D0/h0/event_horizon.py` | 32 temporal windows |
| H-Morph | `Pipeline/D0/h0/h_morph.py` | 24 morphological parameters |
| H-Law | `Pipeline/D0/h0/h_law.py` | 3 causal attention modes |

### Downstream Files

| Component | File | Usage |
|-----------|------|-------|
| HC⁰ | `Pipeline/D0/c0/hc0/` | C⁰ branch: 16 cognitive mechanisms |
| HR⁰ | `Pipeline/D0/r0/hr0/` | R⁰ branch: 8 music-theoretic mechanisms |

### Memory Requirements

```
History Buffer (for 981s max window):
  • Frames: 981s × 172 Hz = 168,642 frames
  • Per frame: 256D × 4 bytes = 1,024 bytes
  • Total: ~173 MB

H⁰ Tensor (full 2,304D):
  • Size: 32 × 24 × 3 × 4 bytes = 9,216 bytes
  • Per frame: ~9 KB
  • Position: SRC⁹[256:2560]
```

---

## Related Documents

### In This Folder
- [EVENT-HORIZON.md](EVENT-HORIZON.md) — 32 temporal windows specification
- [H-MORPH.md](H-MORPH.md) — 24 morphological parameters
- [H-LAW.md](H-LAW.md) — 3 causal attention modes

### Parent Documentation
- [../SRC⁹-Composer/SRC⁹-Composer.md](../SRC⁹-Composer/SRC⁹-Composer.md) — Master architecture reference
- [../C⁰/](../C⁰/) — C⁰ Cognitive Layer (uses H⁰ via HC⁰)
- [../R⁰/](../R⁰/) — R⁰ Resonance Layer (uses H⁰ via HR⁰)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-03 | Initial H⁰ documentation |
| 2.0.0 | 2026-02-05 | Updated for shared infrastructure role; H⁰ now feeds both C⁰ and R⁰ |

---

**Next**: [EVENT-HORIZON.md](EVENT-HORIZON.md) — Complete window specification
