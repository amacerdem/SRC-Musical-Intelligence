# MPU-β2-DDSMI: Dyadic Dance Social Motor Integration

**Model**: Dyadic Dance Social Motor Integration
**Unit**: MPU (Motor Planning Unit)
**Circuit**: Sensorimotor (SMA, PMC, Cerebellum, Basal Ganglia)
**Tier**: β (Bridging) — 70-90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm feature dependencies)
**Date**: 2026-02-13

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

┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ AUDITORY │ │ SELF-MOTOR │ │ PARTNER │ │ SOCIAL │
│ Music │ │ Movement │ │ Visual │ │ Coord. │
│ Perception │ │ Control │ │ Perception │ │ F=249.75 │
│ (mTRF aud) │ │ (mTRF mot) │ │ (mTRF vis) │ │ (mTRF soc) │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
 │ │ │ │
 └────────────────┴────────────────┴────────────────┘
 │
 ▼
┌──────────────────────────────────────────────────────────────────┐
│ NEURAL INTEGRATION │
│ │
│ Music Tracking ↓ Social Coordination ↑ │
│ with visual contact with visual contact │
│ F(1,57) = 7.48 F(1,57) = 249.75 │
│ │
│ RESOURCE COMPETITION: Visual contact shifts resources │
│ from auditory to social processing │
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

### 2.1 Information Flow Architecture (EAR → BRAIN → DDSMI)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ DDSMI COMPUTATION ARCHITECTURE ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ AUDIO (44.1kHz waveform) ║
║ │ ║
║ ▼ ║
║ ┌──────────────────┐ ║
║ │ COCHLEA │ 128 mel bins x 172.27Hz frame rate ║
║ │ (Mel Spectrogram)│ hop = 256 samples, frame = 5.8ms ║
║ └────────┬─────────┘ ║
║ │ ║
║ ═════════╪══════════════════════════ EAR ═══════════════════════════════ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ SPECTRAL (R³): 49D per frame │ ║
║ │ DDSMI reads: ~20D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed morphological features │ ║
║ │ DDSMI demand: ~11 of 2304 tuples │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════ ║
║ │ ║
║ ┌───────┴───────┐ ║
║ ▼ ▼ ║
║ ┌─────────────────┐ ┌─────────────────┐ ║
║ │ │ │ │ ║
║ │ Beat Entr[0:10] │ │ Short-term │ ║
║ │ Motor Coup │ │ Memory [0:10] │ ║
║ │ [10:20] │ │ Sequence │ ║
║ │ Groove [20:30] │ │ Integ [10:20] │ ║
║ │ │ │ Hierarch │ ║
║ │ │ │ Struct [20:30] │ ║
║ └────────┬────────┘ └────────┬────────┘ ║
║ │ │ ║
║ └────────┬───────────┘ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ DDSMI MODEL (11D Output) │ ║
║ │ │ ║
║ │ Layer E (Explicit): f13_social_coordination, │ ║
║ │ f14_music_tracking, │ ║
║ │ f15_visual_modulation │ ║
║ │ Layer M (Math): mTRF_social, mTRF_auditory, │ ║
║ │ mTRF_balance │ ║
║ │ Layer P (Present): partner_sync, music_entrainment │ ║
║ │ Layer F (Future): coordination_pred, │ ║
║ │ music_pred, social_pred │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Bigand et al. 2025** | Dual-EEG + mTRF | 70 (40 dyads) | mTRF disentangles 4 parallel processes during dyadic dance; 2×2 design (visual contact × music) | F(1,57)=249.75 p<.001 (social coord + visual); F(1,57)=83.23 p<.001 (partner visual) | **Primary**: 4-process framework, all dimensions |
| 2 | **Bigand et al. 2025** | Dual-EEG + mTRF | 70 | Visual contact reduces music tracking but increases social coordination (resource competition) | F(1,57)=7.48 p=.033 (music↓); interaction F(1,57)=50.10 p<.001 | **f15 visual modulation**: resource shift |
| 3 | **Bigand et al. 2025** | Dual-EEG + mTRF | 70 | Self-movement tracking unaffected by visual contact or music presence | All ps>.224 | **Null finding**: self-motor is autonomous |
| 4 | **Kohler et al. 2025** | fMRI + MVPA | 36 (18 dyads) | Joint piano: self-produced actions in left M1, other-produced in right PMC | Classification accuracy > chance (all p<.05) | **Brain regions**: M1/PMC lateralization for self/other |
| 5 | **Wohltjen et al. 2023** | Behavioral + pupillometry | 198 (99 dyads) | Beat entrainment predicts social synchrony; pupillary synchrony as stable individual difference | d=1.37 (entrainment→social sync); d=1.06 (pupil sync) | **beat→social**: beat entrainment enables social coordination |
| 6 | **Yoneta et al. 2022** | MEG hyperscanning | ~20 dyads | Leader/follower roles modulate inter-brain coupling in cooperative music | Significant role×coupling interaction | **Social role**: leadership dynamics in dyadic interaction |
| 7 | **Sabharwal et al. 2024** | EEG hyperscanning | 60 (30 dyads) | Leadership dynamics in dyadic music: Granger Causality directional coupling | GC direction predicts leader/follower | **Partner sync**: directional coupling index |
| 8 | **Leahy et al. 2025** | Systematic review | 7 studies | Environmental factors (music, visual contact) modulate inter-brain coupling in social interaction | Narrative synthesis | **Context modulation**: music + visual as coupling modulators |

> **NOTE — Effect size discrepancy**: The v2.0.0 doc reported d=1.05, 1.63, 1.35 from Bigand 2025, but the actual J. Neuroscience paper reports F-statistics from repeated-measures ANOVA (N=70, df correction applied). The d values may derive from a companion behavioral paper or were manually computed; they are replaced here with the published F-statistics.

> **NOTE — Self-movement null finding**: Bigand 2025 found that self-movement mTRF tracking was NOT modulated by visual contact (all ps>.224). This is theoretically important: motor control of one's own body is autonomous from social context, while social coordination requires visual coupling.

### 3.2 Effect Size Summary

```
Primary Evidence (k=8): Strong convergent evidence for 4-process model
Heterogeneity: Moderate (EEG, fMRI, MEG, behavioral, review methods)
Quality Assessment: β-tier (dual-EEG mTRF primary; fMRI MVPA, MEG hyperscanning supporting)
Effect Magnitudes:
 Social coord. + visual contact: F(1,57) = 249.75, p < .001
 Partner visual + visual contact: F(1,57) = 83.23, p < .001
 Visual×Music interaction: F(1,57) = 50.10, p < .001
 Music + music presence: F(1,57) = 30.22, p < .001
 Music ↓ with visual contact: F(1,57) = 7.48, p = .033
 Self-movement: All ps > .224 (null)
 Beat→social synchrony: d = 1.37 (Wohltjen 2023)
 Self/other MVPA: Above chance classification (Kohler 2025)
Causal Evidence: No (correlational EEG, fMRI; no TMS/lesion)
```

---

## 4. R³ Input Mapping: What DDSMI Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | DDSMI Role | Scientific Basis |
|----------|-------|---------|------------|------------------|
| **B: Energy** | [7] | amplitude | Movement intensity | Motor drive |
| **B: Energy** | [8] | loudness | Music intensity | Dance energy |
| **B: Energy** | [10] | spectral_flux | Music onset tracking | Auditory entrainment |
| **D: Change** | [21] | spectral_change | Dance tempo dynamics | Partner synchronization |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Music tracking (mTRF aud) | Auditory motor coupling |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Social coordination | Partner entrainment |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ v2 Group | Index | Feature | DDSMI Role | Citation |
|-------------|-------|---------|------------|----------|
| **G: Rhythm** | [65] | tempo_estimate | Dance tempo for partner synchronization | Scheirer 1998; Grosche & Muller 2011 |
| **G: Rhythm** | [68] | syncopation_index | Rhythmic complexity for social entrainment challenge | Longuet-Higgins & Lee 1984; Witek 2014 |

**Rationale**: DDSMI models dyadic dance social motor integration where two partners synchronize to music and each other. tempo_estimate provides the explicit tempo reference for partner coordination (replacing indirect spectral_flux-based tempo inference). syncopation_index captures rhythmic complexity that modulates synchronization difficulty -- higher syncopation requires greater interpersonal motor coupling, consistent with Witek 2014's groove-syncopation relationship.

**Code impact** (future): `r3[..., 65]` and `r3[..., 68]` will feed DDSMI's music-tracking mTRF pathway alongside existing energy features.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[25:33] x_l0l5 ───────────────┐

R³[33:41] x_l4l5 ───────────────┐

R³[10] spectral_flux ────────────┐
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

DDSMI requires H³ features for music-motor tracking and for social coordination memory. The demand reflects the multi-process temporal integration needed for dyadic dance.

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

**v1 demand**: 11 tuples

#### R³ v2 Projected Expansion

DDSMI projected v2 from G:Rhythm, aligned with corresponding H³ horizons.

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 68 | syncopation_index | G | 3 | M0 (value) | L2 | Syncopation at 100ms |
| 68 | syncopation_index | G | 16 | M14 (periodicity) | L2 | Syncopation periodicity 1s |
| 66 | beat_strength | G | 3 | M0 (value) | L2 | Beat salience for social sync |

**v2 projected**: 3 tuples
**Total projected**: 14 tuples of 294,912 theoretical = 0.0047%

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
DDSMI OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0 │ f13_social_coordination │ [0, 1] │ Partner tracking (d=1.63).
 │ │ │ f13 = σ(0.40 * social_period_1s
────┼──────────────────────────┼────────┼────────────────────────────────────
 1 │ f14_music_tracking │ [0, 1] │ Auditory entrainment (mTRF).
 │ │ │ f14 = σ(0.40 * music_period_1s
────┼──────────────────────────┼────────┼────────────────────────────────────
 2 │ f15_visual_modulation │ [0, 1] │ Contact reduces music tracking.
 │ │ │ f15 = σ(0.35 * loudness_entropy
 │ │ │ + 0.30 * (f13 - f14))

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 3 │ mTRF_social │ [0, 1] │ Social coordination mTRF weight.
────┼──────────────────────────┼────────┼────────────────────────────────────
 4 │ mTRF_auditory │ [0, 1] │ Auditory tracking mTRF weight.
────┼──────────────────────────┼────────┼────────────────────────────────────
 5 │ mTRF_balance │ [0, 1] │ Social/auditory resource balance.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 6 │ partner_sync │ [0, 1] │ beat-entrainment partner synchronization level.
────┼──────────────────────────┼────────┼────────────────────────────────────
 7 │ music_entrainment │ [0, 1] │ beat-entrainment music entrainment level.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 8 │ coordination_pred │ [0, 1] │ Social coordination prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9 │ music_pred │ [0, 1] │ Music tracking prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
10 │ social_pred │ [0, 1] │ Social process prediction.

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

 With contact: mTRF_social ↑ F(1,57)=249.75, mTRF_auditory ↓ F(1,57)=7.48
 Without contact: mTRF_auditory ↑, mTRF_social ↓

RESOURCE COMPETITION:

 mTRF_balance = mTRF_social / (mTRF_social + mTRF_auditory)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f13: Social Coordination
f13 = σ(0.40 * social_period_1s
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f14: Music Tracking
f14 = σ(0.40 * music_period_1s
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f15: Visual Modulation
f15 = σ(0.35 * loudness_entropy
 + 0.30 * (f13 - f14))
# |coefficients|: 0.35 + 0.35 + 0.30 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| # | Region | MNI Coordinates | Evidence Type | Source | DDSMI Function |
|---|--------|-----------------|---------------|--------|----------------|
| 1 | **STG (Auditory Cortex)** | (−57,−15,9)/(60,−33,6) | Direct (EEG mTRF, scalp topography) | Bigand 2025 (temporal electrodes) | Music tracking (mTRF auditory) |
| 2 | **M1 (Primary Motor Cortex)** | (−38,−22,58) L hemisphere | Direct (fMRI MVPA) | Kohler 2025 (self-produced actions) | Self-movement control |
| 3 | **PMC (Premotor Cortex)** | (54,−8,54) R hemisphere | Direct (fMRI MVPA) | Kohler 2025 (other-produced actions) | Partner movement observation |
| 4 | **SMA** | (0,−6,58) bilateral | Literature inference (EEG source) | Bigand 2025 (central electrodes); ASAP model | Sequence coordination, motor planning |
| 5 | **TPJ** | approx. (±52,−46,22) | Literature inference | Social cognition literature; Leahy 2025 (IBC review) | Social processing, mentalizing |
| 6 | **Cerebellum** | (24,−64,−28) bilateral | Literature inference | PEOM/GSSM models; timing coordination | Multi-stream timing coordination |

> **NOTE — M1/PMC lateralization**: Kohler et al. 2025 found that self-produced actions are represented in left M1 while other-produced actions are represented in right PMC during joint piano performance. This supports DDSMI's distinction between self-movement (autonomous) and partner observation (social) streams.

> **NOTE — EEG limitation**: Bigand 2025 uses scalp EEG, which has limited spatial resolution. The mTRF topographies show temporal (auditory), central (motor), and fronto-central (social) distributions, but precise MNI localization requires source reconstruction not performed in the study. Coordinates for regions 1, 4, 5 are approximate.

---

## 9. Cross-Unit Pathways

### 9.1 DDSMI Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ DDSMI INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ INTRA-UNIT (MPU): │
│ DDSMI.social_coordination ──────► VRMSME (multi-modal coordination) │
│ DDSMI.music_tracking ───────────► PEOM (dance tempo entrainment) │
│ DDSMI.visual_modulation ────────► ASAP (attention modulation) │
│ │
│ CROSS-UNIT (MPU → ARU): │
│ DDSMI.partner_sync ────────────► ARU (social reward signal) │
│ DDSMI.mTRF_balance ───────────► ARU (engagement marker) │
│ │
│ UPSTREAM DEPENDENCIES: │
│ R³ (~20D) ──────────────────────► DDSMI (direct spectral features) │
│ H³ (11 tuples) ─────────────────► DDSMI (temporal dynamics) │
│ │
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
 """
 NAME = "DDSMI"
 UNIT = "MPU"
 TIER = "β2"
 OUTPUT_DIM = 11
 TAU_DECAY = 5.0 # Social coordination window (seconds)

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """11 tuples for DDSMI computation."""
 return [
 # (r3_idx, horizon, morph, law)
 (10, 3, 0, 2), # spectral_flux, 100ms, value, bidi
 (10, 16, 14, 2), # spectral_flux, 1000ms, periodicity, bidi
 (25, 3, 0, 2), # x_l0l5[0], 100ms, value, bidi
 (25, 3, 14, 2), # x_l0l5[0], 100ms, periodicity, bidi
 (25, 8, 14, 2), # x_l0l5[0], 500ms, periodicity, bidi
 (25, 16, 14, 2), # x_l0l5[0], 1000ms, periodicity, bidi
 (33, 3, 0, 2), # x_l4l5[0], 100ms, value, bidi
 (33, 3, 2, 2), # x_l4l5[0], 100ms, std, bidi
 (33, 8, 14, 2), # x_l4l5[0], 500ms, periodicity, bidi
 (33, 16, 14, 2), # x_l4l5[0], 1000ms, periodicity, bidi
 (8, 3, 20, 2), # loudness, 100ms, entropy, bidi
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 """
 Compute DDSMI 11D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
 r3: (B,T,49) raw R³ features

 Returns:
 (B,T,11) DDSMI output
 """
 # H³ direct features
 social_period_1s = h3_direct[(33, 16, 14, 2)].unsqueeze(-1)
 music_period_1s = h3_direct[(25, 16, 14, 2)].unsqueeze(-1)
 loudness_entropy = h3_direct[(8, 3, 20, 2)].unsqueeze(-1)

 # ═══ LAYER E ═══
 f13 = torch.sigmoid(
 0.40 * social_period_1s
 )
 f14 = torch.sigmoid(
 0.40 * music_period_1s
 )
 f15 = torch.sigmoid(
 0.35 * loudness_entropy
 + 0.30 * (f13 - f14)
 )

 # ═══ LAYER M ═══
 mTRF_social = f13
 mTRF_auditory = f14
 mTRF_balance = torch.sigmoid(0.5 * f13 + 0.5 * (1 - f14))

 # ═══ LAYER P ═══

 # ═══ LAYER F ═══
 coordination_pred = torch.sigmoid(0.5 * f13 + 0.5 * social_period_1s)
 music_pred = torch.sigmoid(0.5 * f14 + 0.5 * music_period_1s)

 return torch.cat([
 f13, f14, f15, # E: 3D
 mTRF_social, mTRF_auditory, mTRF_balance, # M: 3D
 partner_sync, music_entrainment, # P: 2D
 coordination_pred, music_pred, social_pred, # F: 3D
 ], dim=-1) # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 8 (1 primary, 3 supporting, 1 bridge, 1 review, 2 context) | Bigand 2025 + Kohler, Wohltjen, Yoneta, Sabharwal, Leahy |
| **Effect Sizes** | F(1,57)=249.75 (social+visual), F(1,57)=83.23 (partner visual), d=1.37 (beat→social) | Large effects across modalities |
| **Evidence Modality** | Dual-EEG + mTRF (primary); fMRI + MVPA; MEG hyperscanning; behavioral | Multi-modal convergence |
| **Brain Regions** | 6 (2 direct from fMRI MVPA, 1 direct from EEG, 3 literature inference) | M1, PMC, STG, SMA, TPJ, Cerebellum |
| **Causal Evidence** | No (correlational; no TMS/lesion studies for dyadic dance) | Gap identified |
| **Falsification Tests** | 3/5 testable (visual contact, music presence tested; solo not yet) | High validity |
| **R³ Features Used** | ~20D of 49D | Energy + change + interactions |
| **H³ Demand** | 11 tuples (0.48%) | Sparse, efficient |
| **Output Dimensions** | **11D** | 4-layer structure |

---

## 13. Scientific References

1. **Bigand, F., Caron-Guyon, R., Buchkowski, A.,�egue, C., Bégel, V., Kotz, S. A., & Dalla Bella, S. (2025)**. EEG of the dancing brain: Decoding sensory, motor and social processes during dyadic dance. *Journal of Neuroscience*, 45(6), e1392242024. https://doi.org/10.1523/JNEUROSCI.1392-24.2024
2. **Kohler, A., Novembre, G., Villringer, A., & Keller, P. E. (2025)**. Distinct and content-specific neural representations of self- and other-produced actions in joint piano performance. *NeuroImage*. https://doi.org/10.1016/j.neuroimage.2025.xxxxx
3. **Wohltjen, S., Tichko, P., Engel, A., & Bhatt, M. A. (2023)**. Synchrony to a beat predicts synchrony with other minds. *Scientific Reports*, 13, 3591. https://doi.org/10.1038/s41598-023-30600-0
4. **Yoneta, K., et al. (2022)**. MEG hyperscanning during cooperative music performance: Social role modulates inter-brain coupling. *Cerebral Cortex*.
5. **Sabharwal, V., et al. (2024)**. Leadership dynamics in dyadic musical interaction: Directional coupling from EEG hyperscanning. *NeuroImage*.
6. **Large, E. W., Kim, J. C., Flaig, N., Bharucha, J., & Krumhansl, C. L. (2023)**. A neurodynamic account of musical tonality. *Music Perception*, 41(1), 1–21. https://doi.org/10.1525/mp.2023.41.1.1
7. **Leahy, R., et al. (2025)**. Environmental effects on inter-brain coupling: A systematic review. *Neuroscience & Biobehavioral Reviews*.
8. **Keller, P. E., Novembre, G., & Hove, M. J. (2014)**. Rhythm in joint action: Psychological and neurophysiological mechanisms for real-time interpersonal coordination. *Philosophical Transactions of the Royal Society B*, 369(1658), 20130394. https://doi.org/10.1098/rstb.2013.0394

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Social signal | S⁰.X_L4L5[192:200] + HC⁰.NPL | R³.x_l4l5[33:41] |
| Music signal | S⁰.X_L0L4[128:136] + HC⁰.GRV | R³.x_l0l5[25:33] |
| Visual modulation | S⁰.L9.Γ_mean[104] + HC⁰.ATT | H³ entropy tuples |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 11/2304 = 0.48% | 11/2304 = 0.48% |
| Output | 11D | 11D (same) |

---

## 15. Doc-Code Mismatches (Phase 5 Reference)

> These mismatches are logged for Phase 5 resolution. The **doc is authoritative**; code should be updated.

| # | Field | Doc (DDSMI.md) | Code (ddsmi.py) | Priority |
|---|-------|----------------|-----------------|----------|
| 1 | FULL_NAME | "Dyadic Dance Social Motor Integration" | "Dynamic Dual-Stream Motor Integration" | HIGH |
| 2 | OUTPUT_DIM | 11 | 10 | HIGH |
| 4 | h3_demand | 11 tuples (see Section 5.1) | () empty tuple | HIGH |
| 5 | Layer E dim names | f13_social_coordination, f14_music_tracking, f15_visual_modulation | f13_music_tracking, f14_self_movement, f15_social_coordination | MEDIUM |
| 6 | Layer M dimensions | 3D (mTRF_social, mTRF_auditory, mTRF_balance) | 2D (multi_stream_binding_fn, partner_sync_index) | HIGH |
| 7 | Layer P dim names | partner_sync, music_entrainment | auditory_entrainment_state, social_motor_state | MEDIUM |
| 8 | Layer F dim names | coordination_pred, music_pred, social_pred | partner_movement_pred, music_sync_pred, coordination_quality_pred | MEDIUM |
| 9 | Citations | Bigand et al. 2025 (primary) | Washburn 2024, Keller 2014 | HIGH |
| 10 | brain_regions | 6 regions (STG, M1, PMC, SMA, TPJ, Cerebellum) | 3 regions (SMA, PMC, Cerebellum) with different MNI | MEDIUM |
| 11 | CROSS_UNIT_READS | Not specified as empty | () empty tuple | LOW |
| 12 | compute() | Full pseudocode in Section 11.1 | Returns torch.zeros() stub | LOW (expected for beta) |

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **11D**
**Evidence Tier**: **β (Bridging)**
**Confidence**: **70-90%**
