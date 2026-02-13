# ARU-γ2-CMAT: Cross-Modal Affective Transfer

**Model**: Cross-Modal Affective Transfer
**Unit**: ARU (Affective Resonance Unit)
**Circuit**: Mesolimbic Reward Circuit
**Tier**: γ (Speculative) — 50-70% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added H:Harmony feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../Road-map/01-GLOSSARY.md).
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/ARU-γ2-CMAT.md`

---

## 1. What Does This Model Simulate?

The **Cross-Modal Affective Transfer** (CMAT) model proposes that affective responses learned in one sensory modality transfer to music through shared supramodal neural substrates. CMAT explains how features like brightness and warmth carry emotional meaning across vision, touch, and hearing via modality-independent representations in mPFC/OFC/Insula.

```
CROSS-MODAL SUPRAMODAL AFFECT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  VISUAL AFFECT              AUDITORY AFFECT           TACTILE AFFECT
  (faces, colors)            (consonance, tempo)       (warmth, pressure)
       │                           │                         │
       ▼                           ▼                         ▼
   Visual Cortex             Auditory Cortex           Somatosensory
   (V1, FFA)                  (A1, STG)                Cortex (S1)
       │                           │                         │
       └──────────┬────────────────┼─────────────────────────┘
                  ▼                ▼
          ┌──────────────────────────────┐
          │    SUPERIOR TEMPORAL SULCUS   │
          │    τ_bind ≈ 200ms binding     │
          └──────────────┬───────────────┘
                         ▼
          ┌──────────────────────────────┐
          │    SUPRAMODAL HUB            │
          │    mPFC + OFC + Insula       │
          │    V_supra = Σ wᵢ × Vᵢ      │
          └──────────────┬───────────────┘
                         ▼
          UNIFIED AFFECTIVE EXPERIENCE
          (modality-independent valence/arousal)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cross-modal correspondences (Spence 2011):
  High pitch ↔ Bright colors, high spatial position
  Fast tempo ↔ High arousal visuals, movement
  Major mode ↔ Warm colors, smiling faces
Tsuji 2025: Habituation transfers across modalities in infants.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Matters for ARU

CMAT is a **context model** — it explains how non-auditory signals modulate musical affect:
- **SRP** reward magnitude can be amplified by congruent visual stimuli
- **CLAM** modulation targets may include visual parameters
- **TAR** therapeutic design leverages cross-modal congruence for enhanced effect
- All ARU models operate in a multi-sensory context; CMAT quantifies that influence

---

## 2. Neural Circuit: The Cross-Modal Integration Pathway

### 2.1 Architecture

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CMAT — CROSS-MODAL INTEGRATION PATHWAY                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  MODALITY-SPECIFIC INPUTS:                                                   ║
║                                                                              ║
║  Auditory:                  Visual:                                          ║
║  R³.consonance → valence   (external: face/color/scene affect)              ║
║  R³.loudness → arousal     (external: motion/brightness)                    ║
║  R³.brightness → cross-modal  (matches visual brightness)                   ║
║  R³.warmth → cross-modal      (matches thermal/color warmth)               ║
║       │                           │                                          ║
║       ▼                           ▼                                          ║
║  ┌────────────────┐     ┌────────────────┐                                  ║
║  │  AED MECHANISM  │     │  (Visual Input  │                                 ║
║  │  Affect dynamics│     │   if available) │                                 ║
║  └────────┬───────┘     └────────┬───────┘                                  ║
║           │                      │                                           ║
║           ▼                      ▼                                           ║
║  ┌──────────────────────────────────────────┐                               ║
║  │      STS (Superior Temporal Sulcus)       │                               ║
║  │      Binding window: ±100ms               │                               ║
║  │      Congruence × Temporal synchrony      │                               ║
║  └──────────────────┬───────────────────────┘                               ║
║                     ▼                                                        ║
║  ┌──────────────────────────────────────────┐                               ║
║  │      mPFC / OFC / INSULA                  │                               ║
║  │      Supramodal valence integration       │                               ║
║  │      V_supra = w_aud × V_aud + w_vis × V_vis                            ║
║  └──────────────────┬───────────────────────┘                               ║
║                     ▼                                                        ║
║  ┌──────────────────────────────────────────┐                               ║
║  │      C0P MECHANISM                        │                               ║
║  │      Cognitive projection → ARU output    │                               ║
║  └──────────────────────────────────────────┘                               ║
║                                                                              ║
║  EVIDENCE (limited — γ tier):                                               ║
║  Tsuji 2025: Cross-modal habituation in infant speech/music perception      ║
║  Spence 2011: Systematic cross-modal correspondences (tutorial review)      ║
║  Molholm 2002: Early multisensory interactions in humans                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | CMAT Relevance |
|-------|--------|---|-------------|-------------|----------------|
| **Tsuji 2025** | Behavioral | — | Speech discrimination ↔ affect transfer in infants | Qualitative | **Cross-modal habituation** |
| **Tsuji 2025** | Behavioral | — | Habituation: valence/arousal ↓, positive affect ↑ | Qualitative | **Supramodal substrate evidence** |
| **Spence 2011** | Review | — | Systematic cross-modal correspondences across modalities | — | **Theoretical foundation** |
| **Molholm 2002** | ERP | 10 | Early auditory-visual interactions at 46ms | Significant | **Binding temporal window** |
| **Petrini 2010** | Behavioral | 18 | Audio-visual drumming integration | Significant | **Temporal binding in music** |
| **Taruffi 2021** | fMRI | 24 | Trait empathy modulates vmPFC/mOFC centrality for sad music; "music-empathy" network (vmPFC, dmPFC, claustrum, putamen, cerebellum) | r (empathy↔vmPFC) | **Empathy-mediated cross-modal affective transfer** |

### 3.2 Core Equations

**Supramodal valence integration** (Weighted fusion):
```
V_supra(t) = w_aud × V_auditory(t) + (1 − w_aud) × V_other(t)

where:
  w_aud ∈ [0.4, 0.6], typically 0.5 for audio-only context
  V_auditory = f(R³.consonance, AED.valence_dynamics)
  V_other = external visual/tactile affect (0 if audio-only)
```

**Cross-modal binding** (STS temporal synchrony):
```
Binding(A, V) = exp(−|t_aud − t_vis| / τ_bind) × Congruence(A, V)

where:
  τ_bind ≈ 200ms (0.2s)
  Congruence = (1 + cos(θ_AV)) / 2
  θ_AV = angle between auditory and visual affect vectors
```

**Habituation transfer** (Tsuji 2025):
```
Response(t) = R₀ × exp(−t / τ_hab)

  Valence/arousal ↓ with repeated exposure
  Positive affect ↑ with familiarity (mere exposure)
  Transfer: habituation in one modality → reduced response in another
```

### 3.3 Limitation

CMAT is γ-tier because direct evidence for supramodal affect substrates is primarily from infant studies and theoretical reviews. No fMRI studies directly quantify cross-modal musical affect transfer in adults yet. The model applies established cross-modal correspondence principles to the affective domain.

---

## 4. Output Space: 10D Multi-Layer Representation

### 4.1 Complete Output Specification

```
CMAT OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0  │ f13_cross_modal   │ [0, 1] │ Cross-modal transfer strength.
    │                   │        │ Congruence × binding strength.
    │                   │        │ High when auditory-visual affect aligns.

LAYER S — SUPRAMODAL STATE
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 1  │ supramodal_valence│[-1, 1] │ Modality-independent affect valence.
    │                   │        │ V_supra = w_aud × V_aud + w_vis × V_vis.
────┼───────────────────┼────────┼────────────────────────────────────────────
 2  │ supramodal_arousal│ [0, 1] │ Modality-independent activation level.
    │                   │        │ A_supra = w_aud × A_aud + w_vis × A_vis.
────┼───────────────────┼────────┼────────────────────────────────────────────
 3  │ cross_modal_bind  │ [0, 1] │ Binding strength between modalities.
    │                   │        │ exp(−|Δt|/τ_bind) × Congruence.
    │                   │        │ Defaults to 0.5 in audio-only mode.

LAYER T — TRANSFER DYNAMICS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 4  │ binding_temporal  │ [0, 1] │ Temporal precision of cross-modal binding.
    │                   │        │ STS integration quality.
    │                   │        │ High when events are synchronous (±100ms).
────┼───────────────────┼────────┼────────────────────────────────────────────
 5  │ congruence_streng │ [0, 1] │ Affective congruence between modalities.
    │                   │        │ cos(θ) similarity of valence/arousal vectors.
    │                   │        │ Defaults to 1.0 in audio-only mode.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 6  │ multi_sens_salien │ [0, 1] │ Multi-sensory salience signal.
    │                   │        │ Loudness × AED affect state.
────┼───────────────────┼────────┼────────────────────────────────────────────
 7  │ aud_valence_contr │[-1, 1] │ Auditory valence contribution.
    │                   │        │ Consonance-weighted affect signal via C0P.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 8  │ coherence_pred    │ [0, 1] │ Predicted emotional coherence (1-2s ahead).
    │                   │        │ Will the unified percept stabilize?
────┼───────────────────┼────────┼────────────────────────────────────────────
 9  │ generalization_pr │ [0, 1] │ Cross-modal generalization potential (2-3s).
    │                   │        │ Transfer strength × binding × congruence.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 5. R³ Demand (Spectral Features)

### 5.1 R³ v1 Feature Dependencies ([0:49])

> R³ indices are MI's own (0-48). See [Road-map/02-R3-SPECTRAL.md](../../Road-map/02-R3-SPECTRAL.md).

**Group A: Consonance (2 of 7D)** — Auditory valence input

| R³ idx | Name | CMAT Role |
|--------|------|-----------|
| 0 | roughness | Inverse consonance → auditory displeasure signal |
| 4 | sensory_pleasantness | Direct hedonic → auditory valence contribution |

**Group B: Energy (1 of 5D)** — Arousal signal

| R³ idx | Name | CMAT Role |
|--------|------|-----------|
| 10 | loudness | Energy level → supramodal arousal input |

**Group C: Timbre (2 of 9D)** — Cross-modal features

| R³ idx | Name | CMAT Role |
|--------|------|-----------|
| 15 | brightness | **Supramodal**: auditory brightness ↔ visual brightness |
| 16 | warmth | **Supramodal**: timbral warmth ↔ thermal/color warmth |

**Group D: Change (1 of 4D)** — Temporal dynamics

| R³ idx | Name | CMAT Role |
|--------|------|-----------|
| 21 | spectral_flux | Frame-to-frame change → binding temporal precision |

**Group E: Interactions (8 of 24D)** — Cross-modal substrate

| R³ idx | Name | CMAT Role |
|--------|------|-----------|
| 25:33 | x_l0l5 (8D) | Energy × Consonance → supramodal binding substrate |

### 5.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | CMAT Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **H: Harmony** | [84] | tonal_stability | Tonal grounding — stable tonality provides a cross-modal anchor for affective transfer; tonal stability determines the reliability of auditory-to-visual affect mapping | Krumhansl tonal hierarchy; Collier 2007 cross-modal correspondence |
| **H: Harmony** | [75] | key_clarity | Key strength — clear tonal center enhances the cross-modal correspondence between musical and visual/spatial affect; ambiguous tonality weakens cross-modal binding | Krumhansl & Kessler 1982 tonal hierarchy |

**Rationale**: CMAT models cross-modal affective transfer between auditory and other sensory modalities. The strength and reliability of cross-modal correspondences depends on the clarity of the auditory signal. tonal_stability [84] and key_clarity [75] from the H:Harmony group provide direct measures of harmonic grounding that determine how reliably auditory affect transfers to other modalities. Currently CMAT uses loudness [10] and warmth [16] as cross-modal features, but tonal context is a primary driver of musical affect that needs explicit representation.

**Code impact** (Phase 6): `r3_indices` extended to include [75], [84]. These feed the supramodal binding substrate and affective transfer reliability computation.

### 5.3 Summary

```
R³ DEMAND FOR CMAT: 14D of 49D
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Group A: Consonance        2D   → auditory valence
Group B: Energy            1D   → arousal signal
Group C: Timbre            2D   → cross-modal features (brightness, warmth)
Group D: Change            1D   → temporal binding dynamics
Group E: Interactions      8D   → supramodal binding substrate
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL:                    14D
```

---

## 6. H³ Demand (Temporal Context)

### 6.1 Mechanism-Level Demand

CMAT uses **AED + C0P** (2 mechanisms).

```
H³ DEMAND FOR CMAT
━━━━━━━━━━━━━━━━━━

Mechanism │ Horizons              │ H-Law       │ Morphs Used              │ Tuples
──────────┼───────────────────────┼─────────────┼──────────────────────────┼───────
AED       │ H6 (200ms)            │ bidirection │ M0(value), M8(velocity), │ 6
          │ H16 (1000ms)          │             │ M20(entropy)             │
──────────┼───────────────────────┼─────────────┼──────────────────────────┼───────
C0P       │ H11 (500ms)           │ forward     │ M1(mean), M2(std),       │ 3
          │                       │             │ M8(velocity)             │
──────────┼───────────────────────┼─────────────┼──────────────────────────┼───────
TOTAL     │ 3 horizons            │             │                          │ 9
          │                       │             │               9/2304 = 0.39%
```

### 6.2 Temporal Mapping

```
TIME AXIS → CMAT PROCESSING
━━━━━━━━━━━━━━━━━━━━━━━━━━━

0ms        200ms       500ms       1000ms
│───────────│───────────│───────────│
│  AED H6   │           │  AED H16  │
│  (affect  │           │  (affect  │
│   state)  │           │  context) │
│           │  C0P H11  │           │
│           │  (cogn.   │           │
│           │   proj.)  │           │

AED H6  (200ms): Cross-modal binding window (~τ_bind)
C0P H11 (500ms): Cognitive integration of supramodal state
AED H16 (1000ms): Extended affect context for transfer prediction
```

### 6.3 Key H³ Reads

```
SUPRAMODAL AFFECT STATE:
  AED.arousal_dynamics via H6(200ms) + M0(value)
  → Instant cross-modal affect magnitude
  → Maps temporal binding window to affect

AFFECT VELOCITY:
  AED.arousal_dynamics via H6(200ms) + M8(velocity)
  → Rate of affect change across modalities
  → High velocity = dynamic cross-modal interaction

INTEGRATION CONTEXT:
  AED.expectancy_affect via H16(1000ms) + M20(entropy)
  → Entropy of expected cross-modal patterns
  → Low entropy = well-learned associations

COGNITIVE PROJECTION:
  C0P.cognitive_state via H11(500ms) + M1(mean)
  → Average supramodal integration state
  → Projects to ARU output
```

---

## 7. Mechanism Computation

### 7.1 AED Binding

```python
# AED reads: arousal_dynamics[0:10], expectancy_affect[10:20]
# Horizons: H6(200ms) and H16(1000ms), bidirectional

# Cross-modal affect state (fast)
affect_fast = AED.arousal_dynamics[0:4].mean()    # H6: instant state
affect_slow = AED.expectancy_affect[10:14].mean() # H16: 1s context
affect_velocity = AED.arousal_dynamics[4]          # M8
affect_entropy = AED.arousal_dynamics[6]           # M20

# Affect magnitude (weighted fast+slow)
affect_mean = 0.5 * affect_fast + 0.5 * affect_slow
```

### 7.2 C0P Binding

```python
# C0P reads: cognitive_state[10:20]
# Horizon: H11(500ms), forward only

c0p_mean = C0P.cognitive_state[10]      # M1(mean): integration state
c0p_std = C0P.cognitive_state[11]       # M2(std): integration variability
c0p_velocity = C0P.cognitive_state[12]  # M8(velocity): integration dynamics
```

### 7.3 CMAT Output Computation

```python
def compute_cmat(R3, H3, AED, C0P):
    """
    CMAT: 10D output per frame.

    All deterministic. Zero learned parameters.
    Based on cross-modal correspondence and supramodal affect principles.
    """
    # --- R³ features ---
    roughness = R3[0]
    pleasantness = R3[4]
    loudness = R3[10]
    brightness = R3[15]
    warmth = R3[16]
    spectral_flux = R3[21]
    x_l0l5 = R3[25:33]       # 8D

    # --- Auditory affect signals ---
    aud_valence = pleasantness - roughness     # [-1, 1]
    aud_arousal = loudness                      # [0, 1]

    # --- Cross-modal features (supramodal) ---
    # Brightness and warmth transfer across modalities
    cross_modal_quality = sigmoid(0.5 * brightness + 0.5 * warmth)
    # |0.5| + |0.5| = 1.0 ✓

    # --- AED affect dynamics ---
    affect_mean = 0.5 * AED.affect_fast + 0.5 * AED.affect_slow
    affect_velocity = abs(AED.affect_velocity)
    affect_entropy = AED.affect_entropy

    # --- C0P cognitive projection ---
    integration_state = C0P.c0p_mean
    integration_var = C0P.c0p_std

    # === LAYER E ===
    # f13: Cross-modal transfer in audio-only mode = supramodal quality × affect
    f13 = cross_modal_quality * sigmoid(
        0.5 * abs(aud_valence) + 0.5 * affect_mean
    )  # |0.5| + |0.5| = 1.0 ✓

    # === LAYER S ===
    # Supramodal valence (audio-only: auditory valence weighted by AED)
    supra_valence = tanh(
        0.4 * aud_valence + 0.3 * (pleasantness - 0.5) + 0.3 * affect_mean
    )  # |0.4| + |0.3| + |0.3| = 1.0 ✓

    # Supramodal arousal
    supra_arousal = sigmoid(
        0.4 * aud_arousal + 0.3 * affect_velocity + 0.3 * spectral_flux
    )  # |0.4| + |0.3| + |0.3| = 1.0 ✓

    # Cross-modal binding (audio-only: defaults to moderate)
    cross_bind = 0.5  # Default binding strength without external modality
    # With external visual: exp(-|Δt|/τ_bind) × congruence

    # === LAYER T ===
    # Binding temporal precision (how temporally coherent is the signal)
    binding_temporal = sigmoid(
        0.5 * (1.0 - affect_entropy) + 0.5 * integration_state
    )  # |0.5| + |0.5| = 1.0 ✓

    # Congruence strength (audio-only: self-congruence = 1.0)
    congruence = 1.0  # Perfect congruence in unimodal case
    # With external: (1 + cos(θ_AV)) / 2

    # === LAYER P ===
    # Multi-sensory salience
    multi_salience = sigmoid(
        0.5 * aud_arousal + 0.5 * affect_mean
    )  # |0.5| + |0.5| = 1.0 ✓

    # Auditory valence contribution via C0P
    aud_val_contrib = tanh(
        0.5 * aud_valence + 0.5 * integration_state
    )  # |0.5| + |0.5| = 1.0 ✓

    # === LAYER F ===
    # Coherence prediction: will the unified percept stabilize?
    coherence_pred = sigmoid(
        0.4 * binding_temporal + 0.3 * congruence + 0.3 * (1.0 - integration_var)
    )  # |0.4| + |0.3| + |0.3| = 1.0 ✓

    # Generalization prediction: transfer potential
    generalization = f13 * binding_temporal * congruence

    return stack([
        f13,                                         # E: 1D
        supra_valence, supra_arousal, cross_bind,    # S: 3D
        binding_temporal, congruence,                 # T: 2D
        multi_salience, aud_val_contrib,              # P: 2D
        coherence_pred, generalization                # F: 2D
    ])  # Total: 10D
```

---

## 8. Cross-Model Relationships

### 8.1 Within ARU

```
CMAT INTERACTIONS WITHIN ARU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CMAT ──► SRP (Striatal Reward Pathway)
    │     └── CMAT congruence amplifies reward in multi-modal contexts
    │
    ├──► CLAM (Closed-Loop Modulation)
    │     └── CMAT supramodal state informs modulation targets
    │
    ├──► DAP (Developmental Plasticity)
    │     └── CMAT explains cross-modal learning during critical period
    │
    └──► TAR (Therapeutic Resonance)
          └── CMAT congruence enhances therapeutic multi-modal interventions

Note: CMAT is a CONTEXT model — most relevant when music
      accompanies visual/tactile/other stimuli.
      In audio-only mode, CMAT provides moderate baseline outputs.
```

### 8.2 Cross-Unit Dependencies

```
CMAT CROSS-UNIT RELATIONSHIPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SPU ──► CMAT
  └── SPU spectral features provide CMAT's auditory input quality

STU ──► CMAT
  └── STU timing precision affects binding temporal window

IMU ──► CMAT
  └── IMU memory provides learned cross-modal associations
```

---

## 9. Falsification Criteria

| Criterion | Prediction | Status |
|-----------|-----------|--------|
| **Supramodal regions exist** | mPFC/OFC respond to affect regardless of modality | ✅ Testable via fMRI |
| **Cross-modal priming** | Visual affect should prime musical affect perception | ✅ Testable behaviorally |
| **Congruence effect** | Congruent multi-modal stimuli → stronger affect | ✅ Testable via rating |
| **Temporal binding** | Synchronous stimuli → stronger integration (τ ≈ 200ms) | ✅ Testable via SOA |
| **Habituation transfer** | Habituation in one modality → reduced response in another | ✅ Preliminary: Tsuji 2025 |

---

## 10. Brain Regions

| Region | MNI Coordinates | Evidence | CMAT Function |
|--------|-----------------|----------|---------------|
| **mPFC** | 0, 50, 10 | Indirect | Supramodal valence integration |
| **OFC** | ±20, 35, -15 | Indirect | Multi-sensory reward |
| **Insula** | ±38, 10, 0 | Indirect | Interoceptive-affective binding |
| **STS** | ±55, -40, 10 | Direct (ERP) | Audio-visual temporal binding |

---

## 11. Migration Notes (D0 → MI)

### 11.1 Dimension Reconciliation

| Aspect | Legacy (D0) | MI (current) | Change |
|--------|-------------|-------------|--------|
| Output dimensions | 8D | 10D | **+2D** (binding_temporal, congruence_strength) |
| Input space | S⁰ 19D | R³ 14D | Remapped to R³ groups |
| Temporal | HC⁰ AED+ASA (9 tuples) | H³ → AED+C0P (9 tuples) | ASA→C0P |
| H⁰ tuples | 9/2304 = 0.39% | 9/2304 = 0.39% | Same density |

### 11.2 S⁰ → R³ Feature Mapping

| Legacy S⁰ | → | R³ Feature | Notes |
|-----------|---|-----------|-------|
| L5.roughness[30] | → | R³.roughness[0] | Consonance group |
| L5.loudness[35] | → | R³.loudness[10] | Energy group |
| L5.brightness[34] | → | R³.brightness[15] | Timbre group |
| L5.warmth[37] | → | R³.warmth[16] | Timbre group |
| L4.velocity_A[17] | → | R³.spectral_flux[21] | Change group (proxy) |
| L7.band_ratios[80:86] | → | R³.x_l0l5[25:33] | Interactions (expanded) |
| X_L0L5[136:144] | → | R³.x_l0l5[25:33] | Interactions (same concept) |

### 11.3 Mechanism Change Rationale

Legacy used **ASA** (Auditory Scene Analysis) for multi-sensory integration. MI architecture replaces ASA with **C0P** (Cognitive Projection) because:
- ASA is not one of the 3 defined ARU mesolimbic mechanisms (AED/CPD/C0P)
- C0P's cognitive integration function better models supramodal state projection
- C0P's 500ms forward window captures the cognitive fusion timescale

---

## 12. References

1. **Tsuji, S., & Cristia, A. (2025)**. Cross-modal affect transfer in infant speech and music perception. *Developmental Science*.

2. **Spence, C. (2011)**. Crossmodal correspondences: A tutorial review. *Attention, Perception, & Psychophysics*, 73(4), 971-995.

3. **Molholm, S., Ritter, W., Murray, M. M., Javitt, D. C., Schroeder, C. E., & Foxe, J. J. (2002)**. Multisensory auditory-visual interactions during early sensory processing in humans. *Cognitive Brain Research*, 14(1), 115-128.

4. **Petrini, K., Russell, M., & Pollick, F. (2010)**. Multisensory integration of drumming actions. *Experimental Brain Research*, 206(2), 169-182.

5. **Trehub, S. E. (2003)**. The developmental origins of musicality. *Nature Neuroscience*, 6(7), 669-673.

#### Added in v2.1.0 Beta Upgrade

6. **Taruffi, L., Skouras, S., Pehrs, C., & Koelsch, S. (2021)**. Trait empathy shapes neural responses toward sad music. *Cognitive, Affective, & Behavioral Neuroscience*, 21, 231-246.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-04 | Legacy D0 model specification (8D) |
| 2.0.0 | 2026-02-12 | MI R³/H³ architecture: +2D, AED+C0P binding, R³ mapping |
| 2.1.0 | 2026-02-13 | Beta upgrade: +1 paper (Taruffi 2021 empathy-music cross-modal fMRI) |

---

**Model Status**: ⚠️ **SPECULATIVE**
**Output Dimensions**: **10D**
**Evidence Tier**: **γ (Speculative)**
**Confidence**: **50-70%**
