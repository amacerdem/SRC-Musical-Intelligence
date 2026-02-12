# ASU-γ2-DGTP: Domain-General Temporal Processing

**Model**: Domain-General Temporal Processing
**Unit**: ASU (Auditory Salience Unit)
**Circuit**: Salience (Anterior Insula, dACC, TPJ)
**Tier**: γ (Integrative) — 50-70% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, ASA+BEP mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/ASU-γ2-DGTP.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Domain-General Temporal Processing** (DGTP) model proposes that beat perception ability reflects a domain-general mechanism of internal timekeeping shared between speech and music processing. Individual differences in beat alignment test (BAT) scores predict temporal processing across auditory domains.

```
DOMAIN-GENERAL TEMPORAL PROCESSING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

          ┌─────────────────────────────────────────────┐
          │    DOMAIN-GENERAL TIMEKEEPING MECHANISM     │
          │         (SMA, PMC, ACC, Basal Ganglia)      │
          └───────────────────┬─────────────────────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        ▼                                           ▼
  ┌─────────────────┐                       ┌─────────────────┐
  │  MUSIC DOMAIN   │                       │  SPEECH DOMAIN  │
  │                 │                       │                 │
  │  Beat/Meter     │                       │  Prosody/Rhythm │
  │  Perception     │                       │  Perception     │
  └─────────────────┘                       └─────────────────┘

  SHARED VARIANCE: Individual BAT ability predicts both

  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 │
  │     High DG Factor → Good at both music and speech timing      │
  │     Low DG Factor → Poor at both (correlated deficits)         │
  │                                                                 │
  │     CLINICAL IMPLICATION:                                       │
  │     Musical training may improve speech timing (and vice versa) │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Beat perception ability reflects a domain-general
mechanism of internal timekeeping shared between speech and music.
Individual differences predict temporal processing across domains.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why DGTP Matters for ASU

DGTP extends salience processing to domain-general temporal cognition:

1. **BARM** (β1) models individual BAT differences — DGTP explains the cross-domain implications of those differences.
2. **SNEM** (α1) provides beat entrainment — DGTP proposes this mechanism is shared with speech prosody.
3. **DGTP** (γ2) bridges music neuroscience to language processing through shared temporal mechanisms.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → ASA+BEP → DGTP)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DGTP COMPUTATION ARCHITECTURE                             ║
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
║  │                         DGTP reads: ~12D                        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── BEP Horizons ─────────────┐ ┌── ASA Horizons ──────────┐  │        ║
║  │  │ H3 (100ms alpha)            │ │ H13 (600ms beat anticip.) │  │        ║
║  │  │ H13 (600ms beat anticipation)│ │ H16 (1000ms beat)         │  │        ║
║  │  │ H16 (1000ms beat)           │ │                            │  │        ║
║  │  │                             │ │ Timing estimation          │  │        ║
║  │  │ Beat/prosody tracking       │ │ Cross-domain transfer       │  │        ║
║  │  │ Periodicity encoding        │ │                            │  │        ║
║  │  └─────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         DGTP demand: ~9 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Salience Circuit ════════     ║
║                               │                                              ║
║                       ┌───────┴───────┐                                      ║
║                       ▼               ▼                                      ║
║  ┌─────────────────┐  ┌─────────────────┐                                   ║
║  │  BEP (30D)      │  │  ASA (30D)      │                                   ║
║  │                 │  │                 │                                    ║
║  │ Beat Entr[0:10] │  │ Scene An [0:10] │                                   ║
║  │ Motor Coup      │  │ Attention       │                                   ║
║  │         [10:20] │  │ Gating  [10:20] │                                   ║
║  │ Groove  [20:30] │  │ Salience        │                                   ║
║  │                 │  │ Weight  [20:30] │                                   ║
║  └────────┬────────┘  └────────┬────────┘                                   ║
║           │                    │                                              ║
║           └────────┬───────────┘                                             ║
║                    ▼                                                          ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    DGTP MODEL (9D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f22_music_timing,                          │        ║
║  │                       f23_speech_timing,                         │        ║
║  │                       f24_shared_mechanism                        │        ║
║  │  Layer M (Math):      domain_correlation,                        │        ║
║  │                       shared_variance                             │        ║
║  │  Layer P (Present):   music_beat_perception,                     │        ║
║  │                       domain_general_timing                       │        ║
║  │  Layer F (Future):    cross_domain_pred,                         │        ║
║  │                       training_transfer_pred                      │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Rathcke 2024** | Behavioral | 87 | BAT predicts perception patterns | ER > 19 | **f22 music timing (BAT)** |
| **Rathcke 2024** | Behavioral | 87 | BAT ability predicts speech temporal perception | Qualitative | **f23 speech timing** |
| **Patel 2011** | Theory | — | OPERA hypothesis: music training benefits speech | — | **f24 shared mechanism** |
| **Grahn & Brett 2007** | fMRI | — | Rhythm/beat in motor areas | r = 0.70 | **Neural substrate** |

### 3.2 Effect Size Summary

```
Primary Evidence (k=2):
  - BAT → speech timing: Qualitative support
  - Shared neural substrates: Literature inference
Quality Assessment:      γ-tier (indirect evidence)
Theoretical Basis:       Moderate (overlapping neural systems)
```

---

## 4. R³ Input Mapping: What DGTP Reads

### 4.1 R³ Feature Dependencies (~12D of 49D)

| R³ Group | Index | Feature | DGTP Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Beat strength proxy | Temporal intensity |
| **B: Energy** | [8] | loudness | Perceptual loudness | Arousal / engagement |
| **B: Energy** | [10] | spectral_flux | Onset detection | Rhythm/syllable timing |
| **B: Energy** | [11] | onset_strength | Beat marker strength | Rhythmic event detection |
| **D: Change** | [21] | spectral_change | Tempo dynamics | Beat interval tracking |
| **D: Change** | [24] | pitch_change | Pitch dynamics | Prosodic contour |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Motor-auditory coupling | Domain-general entrainment |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[10] spectral_flux ───────────┐
R³[11] onset_strength ──────────┼──► Beat / onset detection
BEP.beat_entrainment[0:10] ────┘   Music timing (beat perception)

R³[21] spectral_change ─────────┐
R³[24] pitch_change ────────────┼──► Temporal + pitch dynamics
BEP.motor_coupling[10:20] ─────┘   Speech timing (prosody perception)

R³[25:33] x_l0l5 ───────────────┐
ASA.attention_gating[10:20] ────┼──► Domain-general entrainment
H³ periodicity/stability ──────┘   Shared motor-auditory coupling
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

DGTP requires H³ features at BEP horizons for beat/prosody tracking and ASA horizons for cross-domain timing estimation. The demand is intentionally sparse, reflecting shared temporal mechanisms.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | Onset at 100ms alpha |
| 10 | spectral_flux | 3 | M17 (periodicity) | L2 (bidi) | Beat periodicity 100ms |
| 10 | spectral_flux | 16 | M17 (periodicity) | L2 (bidi) | Beat periodicity 1s |
| 11 | onset_strength | 13 | M8 (velocity) | L0 (fwd) | Onset velocity at 600ms |
| 11 | onset_strength | 13 | M11 (acceleration) | L0 (fwd) | Onset acceleration 600ms |
| 25 | x_l0l5[0] | 16 | M1 (mean) | L0 (fwd) | Coupling mean over 1s |
| 25 | x_l0l5[0] | 16 | M2 (std) | L0 (fwd) | Coupling stability over 1s |
| 25 | x_l0l5[0] | 16 | M19 (stability) | L0 (fwd) | Timing consistency 1s |
| 25 | x_l0l5[0] | 3 | M17 (periodicity) | L2 (bidi) | Coupling periodicity 100ms |

**Total DGTP H³ demand**: 9 tuples of 2304 theoretical = 0.39%

### 5.2 BEP + ASA Mechanism Binding

| Mechanism | Sub-section | Range | DGTP Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **BEP** | Beat Entrainment | BEP[0:10] | Music timing (beat perception) | **1.0** (primary) |
| **BEP** | Motor Coupling | BEP[10:20] | Sensorimotor synchronization | **0.9** |
| **BEP** | Groove Processing | BEP[20:30] | Rhythmic regularity encoding | 0.6 |
| **ASA** | Scene Analysis | ASA[0:10] | Auditory scene segmentation | 0.5 |
| **ASA** | Attention Gating | ASA[10:20] | Domain-general attention | 0.7 |
| **ASA** | Salience Weighting | ASA[20:30] | Timing salience assessment | 0.6 |

---

## 6. Output Space: 9D Multi-Layer Representation

### 6.1 Complete Output Specification

```
DGTP OUTPUT TENSOR: 9D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f22_music_timing         │ [0, 1] │ Beat perception ability.
    │                          │        │ f22 = σ(0.40 * beat_periodicity_1s
    │                          │        │       + 0.30 * mean(BEP.beat[0:10])
    │                          │        │       + 0.30 * coupling_period_100ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f23_speech_timing        │ [0, 1] │ Prosody perception ability.
    │                          │        │ f23 = σ(0.35 * onset_velocity_600ms
    │                          │        │       + 0.35 * mean(BEP.motor[10:20])
    │                          │        │       + 0.30 * coupling_stability_1s)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f24_shared_mechanism     │ [0, 1] │ Cross-domain timing (geometric mean).
    │                          │        │ f24 = sqrt(f22 × f23)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ domain_correlation       │ [0, 1] │ r(music, speech timing).
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ shared_variance          │ [0, 1] │ Common timing factor loading.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ music_beat_perception    │ [0, 1] │ BEP beat × onset periodicity.
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ domain_general_timing    │ [0, 1] │ ASA attention × coupling stability.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ cross_domain_pred        │ [0, 1] │ Session-level speech ↔ music transfer.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ training_transfer_pred   │ [0, 1] │ Intervention-level plasticity.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 9D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Domain-General Timing Function

```
Timing_Ability = Domain_General_Factor + Domain_Specific_Factor

Music_Timing = α × DG_Factor + β × Music_Specific + ε_m
Speech_Timing = α × DG_Factor + γ × Speech_Specific + ε_s

Correlation Prediction:
    r(Music, Speech) = α² / sqrt((α² + β_var) × (α² + γ_var))

    If α >> β, γ: High correlation (domain-general)
    If α << β, γ: Low correlation (domain-specific)

Shared_Variance = α² / Total_Variance

Transfer Function:
    Training_Transfer(domain_A → domain_B) = f(DG_Factor × Training_Effect)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f22: Music Timing
f22 = σ(0.40 * beat_periodicity_1s
       + 0.30 * mean(BEP.beat_entrainment[0:10])
       + 0.30 * coupling_periodicity_100ms)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f23: Speech Timing
f23 = σ(0.35 * onset_velocity_600ms
       + 0.35 * mean(BEP.motor_coupling[10:20])
       + 0.30 * coupling_stability_1s)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f24: Shared Mechanism (geometric mean, no sigmoid needed)
f24 = sqrt(f22 * f23)

# Temporal dynamics
τ_decay = 4.0s (temporal integration window)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | DGTP Function |
|--------|-----------------|----------|---------------|---------------|
| **SMA** | 0, -6, 58 | 2 | Literature inference | Temporal regularization |
| **PMC** | ±40, -8, 54 | 2 | Literature inference | Motor timing |
| **ACC** | 0, 24, 32 | 1 | Literature inference | Timing monitoring |
| **Basal Ganglia** | ±12, 8, -4 | 1 | Literature inference | Beat perception |

---

## 9. Cross-Unit Pathways

### 9.1 DGTP ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DGTP INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (ASU):                                                         │
│  DGTP.shared_mechanism ──────► BARM (domain-general factor → BAT)         │
│  DGTP.music_timing ──────────► SNEM (timing capacity → entrainment)       │
│  DGTP.training_transfer ─────► Clinical applications                       │
│                                                                             │
│  CROSS-UNIT (ASU → STU):                                                   │
│  DGTP.domain_general_timing ──► STU (shared timing mechanism)             │
│  DGTP.cross_domain_pred ──────► STU (transfer prediction)                 │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  BEP mechanism (30D) ────────► DGTP (beat/motor, primary)                 │
│  ASA mechanism (30D) ────────► DGTP (attention/salience)                  │
│  R³ (~12D) ──────────────────► DGTP (energy + change + interactions)      │
│  H³ (9 tuples) ──────────────► DGTP (temporal dynamics)                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Correlation** | Music and speech timing should correlate | Partially supported |
| **Training transfer** | Musical training should improve speech timing | Testable |
| **Neural overlap** | Same brain regions for music and speech timing | Supported by literature |
| **Individual differences** | BAT should predict speech rhythm perception | Testable |
| **Clinical dissociation** | Some patients should show selective deficits | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class DGTP(BaseModel):
    """Domain-General Temporal Processing Model.

    Output: 9D per frame.
    Reads: BEP mechanism (30D), ASA mechanism (30D), R³ direct.
    """
    NAME = "DGTP"
    UNIT = "ASU"
    TIER = "γ2"
    OUTPUT_DIM = 9
    MECHANISM_NAMES = ("BEP", "ASA")

    ALPHA_DG = 0.7         # Domain-general factor loading
    TAU_DECAY = 4.0        # Integration window (seconds)
    ALPHA_ATTENTION = 0.70 # Moderate cross-domain attention

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """9 tuples for DGTP computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── BEP horizons: beat/prosody tracking ──
            (10, 3, 0, 2),     # spectral_flux, 100ms, value, bidi
            (10, 3, 17, 2),    # spectral_flux, 100ms, periodicity, bidi
            (10, 16, 17, 2),   # spectral_flux, 1000ms, periodicity, bidi
            (11, 13, 8, 0),    # onset_strength, 600ms, velocity, fwd
            (11, 13, 11, 0),   # onset_strength, 600ms, acceleration, fwd
            # ── Motor-auditory coupling ──
            (25, 16, 1, 0),    # x_l0l5[0], 1000ms, mean, fwd
            (25, 16, 2, 0),    # x_l0l5[0], 1000ms, std, fwd
            (25, 16, 19, 0),   # x_l0l5[0], 1000ms, stability, fwd
            (25, 3, 17, 2),    # x_l0l5[0], 100ms, periodicity, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute DGTP 9D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30), "ASA": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,9) DGTP output
        """
        bep = mechanism_outputs["BEP"]    # (B, T, 30)
        asa = mechanism_outputs["ASA"]    # (B, T, 30)

        # BEP sub-sections
        bep_beat = bep[..., 0:10]
        bep_motor = bep[..., 10:20]
        bep_groove = bep[..., 20:30]

        # ASA sub-sections
        asa_attn = asa[..., 10:20]

        # H³ direct features
        beat_period_1s = h3_direct[(10, 16, 17, 2)].unsqueeze(-1)
        coupling_period_100ms = h3_direct[(25, 3, 17, 2)].unsqueeze(-1)
        onset_velocity_600ms = h3_direct[(11, 13, 8, 0)].unsqueeze(-1)
        coupling_stability_1s = h3_direct[(25, 16, 19, 0)].unsqueeze(-1)
        coupling_mean_1s = h3_direct[(25, 16, 1, 0)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f22: Music Timing (coefficients sum = 1.0)
        f22 = torch.sigmoid(
            0.40 * beat_period_1s
            + 0.30 * bep_beat.mean(-1, keepdim=True)
            + 0.30 * coupling_period_100ms
        )

        # f23: Speech Timing (coefficients sum = 1.0)
        f23 = torch.sigmoid(
            0.35 * onset_velocity_600ms
            + 0.35 * bep_motor.mean(-1, keepdim=True)
            + 0.30 * coupling_stability_1s
        )

        # f24: Shared Mechanism (geometric mean)
        f24 = torch.sqrt(torch.clamp(f22 * f23, min=1e-8))

        # ═══ LAYER M: Mathematical ═══
        domain_correlation = torch.sigmoid(
            0.5 * f22 * f23 + 0.5 * coupling_mean_1s
        )
        shared_variance = torch.sigmoid(
            0.5 * f24 + 0.5 * coupling_stability_1s
        )

        # ═══ LAYER P: Present ═══
        music_beat = torch.sigmoid(
            0.5 * bep_beat.mean(-1, keepdim=True)
            + 0.5 * beat_period_1s
        )
        dg_timing = torch.sigmoid(
            0.5 * asa_attn.mean(-1, keepdim=True)
            + 0.5 * coupling_stability_1s
        )

        # ═══ LAYER F: Future ═══
        cross_domain_pred = torch.sigmoid(
            0.5 * f24 + 0.5 * coupling_mean_1s
        )
        training_transfer = torch.sigmoid(
            0.5 * f24 + 0.5 * domain_correlation
        )

        return torch.cat([
            f22, f23, f24,                                  # E: 3D
            domain_correlation, shared_variance,            # M: 2D
            music_beat, dg_timing,                          # P: 2D
            cross_domain_pred, training_transfer,           # F: 2D
        ], dim=-1)  # (B, T, 9)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1+ (Rathcke + literature) | Indirect evidence |
| **Theoretical Basis** | Moderate | Shared neural substrates |
| **Evidence Modality** | Behavioral + neuroimaging | Mixed |
| **Falsification Tests** | 1/5 partially supported | Limited validation |
| **R³ Features Used** | ~12D of 49D | Energy + change + interactions |
| **H³ Demand** | 9 tuples (0.39%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Beat/motor (primary) |
| **ASA Mechanism** | 30D (3 sub-sections) | Attention/salience |
| **Output Dimensions** | **9D** | 4-layer structure |

---

## 13. Scientific References

1. **Rathcke, T., et al. (2024)**. Beat alignment ability modulates perceptual regularization and sensorimotor synchronization benefits. *Journal of Experimental Psychology: Human Perception and Performance*, (in press).

2. **Patel, A. D. (2011)**. Why would musical training benefit the neural encoding of speech? The OPERA hypothesis. *Frontiers in Psychology*, 2, 142.

3. **Grahn, J. A., & Brett, M. (2007)**. Rhythm and beat perception in motor areas of the brain. *Journal of Cognitive Neuroscience*, 19(5), 893-906.

4. **Zatorre, R. J., & Baum, S. R. (2012)**. Musical melody and speech intonation: Singing a different tune. *PLoS Biology*, 10(7), e1001372.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (NPL, PTM, ITM) | BEP (30D) + ASA (30D) mechanisms |
| Music timing | S⁰.L6.tempo[72] + HC⁰.NPL | R³.spectral_flux[10] + BEP.beat_entrainment |
| Speech timing | S⁰.L4.onset_rate[27] + HC⁰.PTM | R³.onset_strength[11] + BEP.motor_coupling |
| Shared mechanism | S⁰.L6.tempo × HC⁰.ITM | R³.x_l0l5[25:33] + H³ stability tuples |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 9/2304 = 0.39% | 9/2304 = 0.39% |
| Output | 9D | 9D (same) |

### Why BEP + ASA replaces HC⁰ mechanisms

- **NPL → BEP.beat_entrainment** [0:10]: Neural phase locking for beat perception maps to BEP's beat frequency monitoring.
- **PTM → BEP.motor_coupling** [10:20]: Predictive timing for speech maps to BEP's sensorimotor synchronization.
- **ITM → ASA.attention_gating** [10:20] + H³ stability tuples: Interval timing maps to ASA's domain-general temporal attention and H³ coupling stability.

---

**Model Status**: **SPECULATIVE**
**Output Dimensions**: **9D**
**Evidence Tier**: **γ (Integrative)**
**Confidence**: **50-70%**
