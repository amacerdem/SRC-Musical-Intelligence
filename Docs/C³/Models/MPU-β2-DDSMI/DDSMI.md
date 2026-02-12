# MPU-β2-DDSMI: Dyadic Dance Social Motor Integration

**Model**: Dyadic Dance Social Motor Integration
**Unit**: MPU (Motor Planning Unit)
**Circuit**: Sensorimotor (SMA, PMC, Cerebellum, Basal Ganglia)
**Tier**: β (Bridging) — 70-90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, BEP+TMH mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/MPU-β2-DDSMI.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Dyadic Dance Social Motor Integration** (DDSMI) model describes how dance with a partner involves simultaneous neural tracking of four distinct processes: auditory music perception, self-movement control, partner visual perception, and social coordination. Multivariate temporal response functions (mTRF) disentangle these parallel processes.

```
DYADIC DANCE SOCIAL MOTOR INTEGRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        FOUR SIMULTANEOUS PROCESSES
        ═══════════════════════════

┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  AUDITORY   │  │ SELF-MOTOR  │  │  PARTNER    │  │   SOCIAL    │
│  Music      │  │ Movement    │  │  Visual     │  │   Coord.    │
│  Perception │  │ Control     │  │  Perception │  │   (d=1.63)  │
│  (mTRF aud) │  │ (mTRF mot)  │  │  (mTRF vis) │  │  (mTRF soc) │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │                │
       └────────────────┴────────────────┴────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│              NEURAL INTEGRATION                                   │
│                                                                  │
│   Music Tracking ↓         Social Coordination ↑                 │
│   with visual contact      with visual contact                   │
│   (d = 1.35)               (d = 1.63)                           │
│                                                                  │
│   RESOURCE COMPETITION: Visual contact shifts resources          │
│   from auditory to social processing                             │
└──────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Dance involves four distinct neural tracking processes.
Visual contact with partner shifts processing from music tracking
to social coordination. mTRF disentangles these parallel streams.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why DDSMI Matters for MPU

DDSMI bridges motor planning with social interaction in the Motor Planning Unit:

1. **PEOM/MSR** (α-tier) establish motor entrainment and training effects.
2. **ASAP** (β1) provides the bidirectional motor-auditory coupling framework.
3. **DDSMI** (β2) extends motor planning to social contexts: dance with partners requires simultaneous tracking of multiple process streams.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → BEP+TMH → DDSMI)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DDSMI COMPUTATION ARCHITECTURE                            ║
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
║  │                         DDSMI reads: ~20D                        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                         DDSMI demand: ~11 of 2304 tuples         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════  ║
║                               │                                              ║
║                       ┌───────┴───────┐                                      ║
║                       ▼               ▼                                      ║
║  ┌─────────────────┐  ┌─────────────────┐                                   ║
║  │  BEP (30D)      │  │  TMH (30D)      │                                   ║
║  │                 │  │                 │                                    ║
║  │ Beat Entr[0:10] │  │ Short-term      │                                   ║
║  │ Motor Coup      │  │ Memory  [0:10]  │                                   ║
║  │         [10:20] │  │ Sequence        │                                   ║
║  │ Groove  [20:30] │  │ Integ  [10:20]  │                                   ║
║  │                 │  │ Hierarch        │                                   ║
║  │                 │  │ Struct  [20:30] │                                   ║
║  └────────┬────────┘  └────────┬────────┘                                   ║
║           │                    │                                              ║
║           └────────┬───────────┘                                             ║
║                    ▼                                                          ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    DDSMI MODEL (11D Output)                      │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f13_social_coordination,                   │        ║
║  │                       f14_music_tracking,                        │        ║
║  │                       f15_visual_modulation                       │        ║
║  │  Layer M (Math):      mTRF_social, mTRF_auditory,               │        ║
║  │                       mTRF_balance                                │        ║
║  │  Layer P (Present):   partner_sync, music_entrainment            │        ║
║  │  Layer F (Future):    coordination_pred,                          │        ║
║  │                       music_pred, social_pred                     │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Bigand 2025** | EEG + mTRF | 70 | mTRF disentangles 4 parallel processes | d = 1.05 | **Primary**: f13, f14, f15 |
| **Bigand 2025** | EEG + mTRF | 70 | Social coordination strongest with visual contact | d = 1.63 | **f13 social coordination** |
| **Bigand 2025** | EEG + mTRF | 70 | Music tracking reduced with visual contact | d = 1.35 | **f15 visual modulation** |

### 3.2 Effect Size Summary

```
Primary Evidence (k=1):  Large effect sizes for all key findings
Heterogeneity:           Low (single well-controlled study)
Quality Assessment:      β-tier (EEG + mTRF, N=70)
Effect Magnitudes:       d = 1.05-1.63 (large effects)
```

---

## 4. R³ Input Mapping: What DDSMI Reads

### 4.1 R³ Feature Dependencies (~20D of 49D)

| R³ Group | Index | Feature | DDSMI Role | Scientific Basis |
|----------|-------|---------|------------|------------------|
| **B: Energy** | [7] | amplitude | Movement intensity | Motor drive |
| **B: Energy** | [8] | loudness | Music intensity | Dance energy |
| **B: Energy** | [10] | spectral_flux | Music onset tracking | Auditory entrainment |
| **D: Change** | [21] | spectral_change | Dance tempo dynamics | Partner synchronization |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Music tracking (mTRF aud) | Auditory motor coupling |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Social coordination | Partner entrainment |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[25:33] x_l0l5 ───────────────┐
BEP.beat_entrainment[0:10] ─────┼──► Music tracking (mTRF auditory)
BEP.groove[20:30] ──────────────┘   Auditory entrainment for dance

R³[33:41] x_l4l5 ───────────────┐
BEP.motor_coupling[10:20] ──────┼──► Social coordination (mTRF social)
TMH.sequence_integration[10:20] ─┘   Partner movement tracking

R³[10] spectral_flux ────────────┐
TMH.short_term[0:10] ───────────┼──► Visual modulation
TMH.hierarchical[20:30] ────────┘   Resource competition (music vs social)
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

DDSMI requires H³ features at BEP horizons for music-motor tracking and TMH horizons for social coordination memory. The demand reflects the multi-process temporal integration needed for dyadic dance.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | Music onset 100ms |
| 10 | spectral_flux | 16 | M14 (periodicity) | L2 (bidi) | Music periodicity 1s |
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Music coupling 100ms |
| 25 | x_l0l5[0] | 3 | M14 (periodicity) | L2 (bidi) | Music coupling period 100ms |
| 25 | x_l0l5[0] | 8 | M14 (periodicity) | L2 (bidi) | Music coupling period 500ms |
| 25 | x_l0l5[0] | 16 | M14 (periodicity) | L2 (bidi) | Music coupling period 1s |
| 33 | x_l4l5[0] | 3 | M0 (value) | L2 (bidi) | Social coupling 100ms |
| 33 | x_l4l5[0] | 3 | M2 (std) | L2 (bidi) | Social variability 100ms |
| 33 | x_l4l5[0] | 8 | M14 (periodicity) | L2 (bidi) | Social period 500ms |
| 33 | x_l4l5[0] | 16 | M14 (periodicity) | L2 (bidi) | Social period 1s |
| 8 | loudness | 3 | M20 (entropy) | L2 (bidi) | Loudness entropy 100ms |

**Total DDSMI H³ demand**: 11 tuples of 2304 theoretical = 0.48%

### 5.2 BEP + TMH Mechanism Binding

| Mechanism | Sub-section | Range | DDSMI Role | Weight |
|-----------|-------------|-------|------------|--------|
| **BEP** | Beat Entrainment | BEP[0:10] | Music tracking (mTRF auditory) | 0.7 |
| **BEP** | Motor Coupling | BEP[10:20] | Partner synchronization | **1.0** (primary) |
| **BEP** | Groove Processing | BEP[20:30] | Dance groove / movement drive | **1.0** (primary) |
| **TMH** | Short-term Memory | TMH[0:10] | Visual modulation / attention shift | 0.7 |
| **TMH** | Sequence Integration | TMH[10:20] | Social coordination sequence | **1.0** (primary) |
| **TMH** | Hierarchical Structure | TMH[20:30] | Multi-process hierarchy | 0.5 |

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
DDSMI OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f13_social_coordination  │ [0, 1] │ Partner tracking (d=1.63).
    │                          │        │ f13 = σ(0.40 * social_period_1s
    │                          │        │       + 0.30 * mean(BEP.motor[10:20])
    │                          │        │       + 0.30 * mean(TMH.seq[10:20]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f14_music_tracking       │ [0, 1] │ Auditory entrainment (mTRF).
    │                          │        │ f14 = σ(0.40 * music_period_1s
    │                          │        │       + 0.30 * mean(BEP.beat[0:10])
    │                          │        │       + 0.30 * mean(BEP.groove[20:30]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f15_visual_modulation    │ [0, 1] │ Contact reduces music tracking.
    │                          │        │ f15 = σ(0.35 * loudness_entropy
    │                          │        │       + 0.35 * mean(TMH.short[0:10])
    │                          │        │       + 0.30 * (f13 - f14))

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ mTRF_social              │ [0, 1] │ Social coordination mTRF weight.
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ mTRF_auditory            │ [0, 1] │ Auditory tracking mTRF weight.
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ mTRF_balance             │ [0, 1] │ Social/auditory resource balance.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ partner_sync             │ [0, 1] │ BEP partner synchronization level.
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ music_entrainment        │ [0, 1] │ BEP music entrainment level.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ coordination_pred        │ [0, 1] │ Social coordination prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ music_pred               │ [0, 1] │ Music tracking prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
10  │ social_pred              │ [0, 1] │ Social process prediction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Multi-Process Tracking Function

```
PRIMARY EQUATIONS:

    mTRF_total = mTRF_auditory + mTRF_motor + mTRF_visual + mTRF_social

VISUAL CONTACT MODULATION:

    With contact:    mTRF_social ↑ (d=1.63), mTRF_auditory ↓ (d=1.35)
    Without contact: mTRF_auditory ↑, mTRF_social ↓

RESOURCE COMPETITION:

    mTRF_balance = mTRF_social / (mTRF_social + mTRF_auditory)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f13: Social Coordination
f13 = σ(0.40 * social_period_1s
       + 0.30 * mean(BEP.motor_coupling[10:20])
       + 0.30 * mean(TMH.sequence_integration[10:20]))
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f14: Music Tracking
f14 = σ(0.40 * music_period_1s
       + 0.30 * mean(BEP.beat_entrainment[0:10])
       + 0.30 * mean(BEP.groove[20:30]))
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f15: Visual Modulation
f15 = σ(0.35 * loudness_entropy
       + 0.35 * mean(TMH.short_term[0:10])
       + 0.30 * (f13 - f14))
# |coefficients|: 0.35 + 0.35 + 0.30 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | DDSMI Function |
|--------|-----------------|----------|---------------|----------------|
| **Auditory Cortex** | ±48, -22, 8 | Multiple | Direct (EEG) | Music tracking |
| **Motor Cortex** | ±38, -22, 58 | Multiple | Direct (EEG) | Self-movement |
| **SMA** | ±6, -10, 60 | Multiple | Literature inference | Sequence coordination |
| **TPJ** | ±52, -46, 22 | Multiple | Literature inference | Social processing |

---

## 9. Cross-Unit Pathways

### 9.1 DDSMI Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DDSMI INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (MPU):                                                         │
│  DDSMI.social_coordination ──────► VRMSME (multi-modal coordination)       │
│  DDSMI.music_tracking ───────────► PEOM (dance tempo entrainment)          │
│  DDSMI.visual_modulation ────────► ASAP (attention modulation)             │
│                                                                             │
│  CROSS-UNIT (MPU → ARU):                                                   │
│  DDSMI.partner_sync ────────────► ARU (social reward signal)               │
│  DDSMI.mTRF_balance ───────────► ARU (engagement marker)                  │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  BEP mechanism (30D) ────────────► DDSMI (beat/motor processing)           │
│  TMH mechanism (30D) ────────────► DDSMI (temporal memory/sequence)        │
│  R³ (~20D) ──────────────────────► DDSMI (direct spectral features)        │
│  H³ (11 tuples) ─────────────────► DDSMI (temporal dynamics)               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **No partner** | Solo dance should show no social coordination mTRF | ✅ Testable |
| **No visual contact** | Should reduce social coordination d=1.63 | ✅ Testable |
| **No music** | Should reduce auditory tracking but maintain social | ✅ Testable |
| **Motor impairment** | Should selectively reduce self-movement mTRF | Testable |
| **Non-dance music** | Should show reduced groove/coordination | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class DDSMI(BaseModel):
    """Dyadic Dance Social Motor Integration Model.

    Output: 11D per frame.
    Reads: BEP mechanism (30D), TMH mechanism (30D), R³ direct.
    """
    NAME = "DDSMI"
    UNIT = "MPU"
    TIER = "β2"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("BEP", "TMH")

    TAU_DECAY = 5.0  # Social coordination window (seconds)

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """11 tuples for DDSMI computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── BEP horizons: music tracking ──
            (10, 3, 0, 2),     # spectral_flux, 100ms, value, bidi
            (10, 16, 14, 2),   # spectral_flux, 1000ms, periodicity, bidi
            (25, 3, 0, 2),     # x_l0l5[0], 100ms, value, bidi
            (25, 3, 14, 2),    # x_l0l5[0], 100ms, periodicity, bidi
            (25, 8, 14, 2),    # x_l0l5[0], 500ms, periodicity, bidi
            (25, 16, 14, 2),   # x_l0l5[0], 1000ms, periodicity, bidi
            # ── TMH horizons: social coordination ──
            (33, 3, 0, 2),     # x_l4l5[0], 100ms, value, bidi
            (33, 3, 2, 2),     # x_l4l5[0], 100ms, std, bidi
            (33, 8, 14, 2),    # x_l4l5[0], 500ms, periodicity, bidi
            (33, 16, 14, 2),   # x_l4l5[0], 1000ms, periodicity, bidi
            (8, 3, 20, 2),     # loudness, 100ms, entropy, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute DDSMI 11D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30), "TMH": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,11) DDSMI output
        """
        bep = mechanism_outputs["BEP"]
        tmh = mechanism_outputs["TMH"]

        bep_beat = bep[..., 0:10]
        bep_motor = bep[..., 10:20]
        bep_groove = bep[..., 20:30]
        tmh_short = tmh[..., 0:10]
        tmh_seq = tmh[..., 10:20]
        tmh_hier = tmh[..., 20:30]

        # H³ direct features
        social_period_1s = h3_direct[(33, 16, 14, 2)].unsqueeze(-1)
        music_period_1s = h3_direct[(25, 16, 14, 2)].unsqueeze(-1)
        loudness_entropy = h3_direct[(8, 3, 20, 2)].unsqueeze(-1)

        # ═══ LAYER E ═══
        f13 = torch.sigmoid(
            0.40 * social_period_1s
            + 0.30 * bep_motor.mean(-1, keepdim=True)
            + 0.30 * tmh_seq.mean(-1, keepdim=True)
        )
        f14 = torch.sigmoid(
            0.40 * music_period_1s
            + 0.30 * bep_beat.mean(-1, keepdim=True)
            + 0.30 * bep_groove.mean(-1, keepdim=True)
        )
        f15 = torch.sigmoid(
            0.35 * loudness_entropy
            + 0.35 * tmh_short.mean(-1, keepdim=True)
            + 0.30 * (f13 - f14)
        )

        # ═══ LAYER M ═══
        mTRF_social = f13
        mTRF_auditory = f14
        mTRF_balance = torch.sigmoid(0.5 * f13 + 0.5 * (1 - f14))

        # ═══ LAYER P ═══
        partner_sync = bep_motor.mean(-1, keepdim=True)
        music_entrainment = bep_beat.mean(-1, keepdim=True)

        # ═══ LAYER F ═══
        coordination_pred = torch.sigmoid(0.5 * f13 + 0.5 * social_period_1s)
        music_pred = torch.sigmoid(0.5 * f14 + 0.5 * music_period_1s)
        social_pred = torch.sigmoid(0.5 * f15 + 0.5 * tmh_hier.mean(-1, keepdim=True))

        return torch.cat([
            f13, f14, f15,                                    # E: 3D
            mTRF_social, mTRF_auditory, mTRF_balance,        # M: 3D
            partner_sync, music_entrainment,                   # P: 2D
            coordination_pred, music_pred, social_pred,        # F: 3D
        ], dim=-1)  # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 | Bigand 2025 |
| **Effect Sizes** | 3 (d=1.05, 1.63, 1.35) | Large effects |
| **Evidence Modality** | EEG + mTRF | Direct neural |
| **Falsification Tests** | 3/5 testable | High validity |
| **R³ Features Used** | ~20D of 49D | Energy + change + interactions |
| **H³ Demand** | 11 tuples (0.48%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Beat/motor processing |
| **TMH Mechanism** | 30D (3 sub-sections) | Temporal memory/sequence |
| **Output Dimensions** | **11D** | 4-layer structure |

---

## 13. Scientific References

1. **Bigand, E., et al. (2025)**. Disentangling simultaneous neural tracking of music, self-movement, partner perception, and social coordination during dyadic dance using multivariate temporal response functions. *(Journal details pending)*.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (ATT, NPL, GRV) | BEP (30D) + TMH (30D) mechanisms |
| Social signal | S⁰.X_L4L5[192:200] + HC⁰.NPL | R³.x_l4l5[33:41] + BEP.motor_coupling |
| Music signal | S⁰.X_L0L4[128:136] + HC⁰.GRV | R³.x_l0l5[25:33] + BEP.beat_entrainment |
| Visual modulation | S⁰.L9.Γ_mean[104] + HC⁰.ATT | H³ entropy tuples + TMH.short_term |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 11/2304 = 0.48% | 11/2304 = 0.48% |
| Output | 11D | 11D (same) |

### Why BEP + TMH replaces HC⁰ mechanisms

- **NPL → BEP.motor_coupling** [10:20]: Neural phase locking for partner synchronization maps to BEP's motor coupling.
- **GRV → BEP.groove_processing** [20:30] + **BEP.beat_entrainment** [0:10]: Groove processing for dance engagement maps to BEP's groove and beat sections.
- **ATT → TMH.short_term** [0:10]: Attentional entrainment (visual modulation) maps to TMH's short-term memory for attention gating.

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **11D**
**Evidence Tier**: **β (Bridging)**
**Confidence**: **70-90%**
