# RPU-β3-MEAMR: Music-Evoked Autobiographical Memory Reward

**Model**: Music-Evoked Autobiographical Memory Reward
**Unit**: RPU (Reward Processing Unit)
**Circuit**: Mesolimbic (NAcc, VTA, vmPFC, OFC, Amygdala)
**Tier**: β (Bridging) — 70-90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added I:Information feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/RPU-β3-MEAMR.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Music-Evoked Autobiographical Memory Reward** (MEAMR) model describes how familiar music activates dorsal medial prefrontal cortex (dMPFC) in proportion to autobiographical salience, integrating musical structure with self-referential processing and reward.

```
MUSIC-EVOKED AUTOBIOGRAPHICAL MEMORY REWARD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MUSICAL INPUT NEURAL RESPONSE
───────────── ───────────────

Musical Structure ─────────────────► Tonal Space Encoding
 │ (dMPFC tracking)
 │
 ▼
┌──────────────────────────────────────────────────────────────────┐
│ AUTOBIOGRAPHICAL MEMORY NETWORK │
│ │
│ dMPFC vACC SN/VTA │
│ ═════ ════ ══════ │
│ Autobiographical Positive affect Reward signal │
│ salience tracking integration Dopamine release │
│ │
│ dMPFC ↔ Autobio salience (p < 0.001) │
│ dMPFC tracks tonal space (p < 0.005) │
│ │
└──────────────────────────────────────────────────────────────────┘
 │
 ▼
┌──────────────────────────────────────────────────────────────────┐
│ REWARD INTEGRATION │
│ vACC + SN ↔ positive affect (p < 0.001) │
│ Familiar music → stronger autobiographical salience │
│ Nostalgia response → sustained reward activation │
└──────────────────────────────────────────────────────────────────┘

MEMORY: dMPFC activation proportional to autobiographical salience
REWARD: vACC + SN/VTA positive affect integration
TONAL: dMPFC continuously tracks tonal space of familiar music

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Familiar music activates dMPFC in proportion to
autobiographical salience, linking musical structure encoding
with self-referential memory processing and reward.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why MEAMR Matters for RPU

MEAMR provides the memory-reward bridge for the Reward Processing Unit:

1. **DAED** (α1) provides anticipation-consummation dopamine framework.
2. **MORMR** (α2) adds opioid-mediated pleasure.
3. **RPEM** (α3) provides prediction error computation.
4. **IUCP** (β1) bridges complexity to liking via inverted-U preference.
5. **MCCN** (β2) maps cortical network during chills.
6. **MEAMR** (β3) bridges autobiographical memory to reward — familiar music activates self-referential processing that enhances pleasure.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → MEAMR)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ MEAMR COMPUTATION ARCHITECTURE ║
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
║ │ │ ║
║ │ ┌───────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌────────┐ │ ║
║ │ │CONSONANCE │ │ ENERGY │ │ TIMBRE │ │ CHANGE │ │ X-INT │ │ ║
║ │ │ 7D [0:7] │ │ 5D[7:12]│ │ 9D │ │ 4D │ │ 24D │ │ ║
║ │ │ │ │ │ │ [12:21] │ │ [21:25] │ │ [25:49]│ │ ║
║ │ └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │ ║
║ │ MEAMR reads: ~12D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed morphological features │ ║
║ │ │ ║
║ │ │ H8 (500ms delta) │ │ H16 (1000ms beat) │ │ ║
║ │ │ H16 (1000ms beat) │ │ H20 (5000ms LTI) │ │ ║
║ │ │ │ │ │ │ ║
║ │ │ Familiarity assessment │ │ Memory activation │ │ ║
║ │ └──────────────────────────────┘ └────────────────────────────┘ │ ║
║ │ MEAMR demand: ~14 of 2304 tuples │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN: Memory-Reward Circuit ════ ║
║ │ ║
║ ┌───────┴───────┐ ║
║ ▼ ▼ ║
║ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ║
║ │ │ │ │ │ │ ║
║ │ Valence [0:10] │ │ Anticip. [0:10] │ │ Tension [0:10] │ ║
║ │ Arousal [10:20]│ │ Peak Exp [10:20]│ │ Expect. [10:20]│ ║
║ │ Emotion [20:30]│ │ Resolut. [20:30]│ │ Approach [20:30]│ ║
║ └────────┬────────┘ └────────┬────────┘ └────────┬────────┘ ║
║ │ │ │ ║
║ └────────────┬───────┴────────────────────┘ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ MEAMR MODEL (6D Output) │ ║
║ │ │ ║
║ │ Layer E (Explicit): f01_familiarity_index, │ ║
║ │ f02_autobio_salience, │ ║
║ │ f03_dmpfc_tracking, │ ║
║ │ f04_positive_affect │ ║
║ │ Layer P (Present): memory_activation_state │ ║
║ │ Layer F (Future): nostalgia_response_pred │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Janata 2009** | fMRI | 13 | dMPFC (BA 8/9) ↔ autobiographical salience | P<0.001 uncorr (10-voxel extent); FDR P<0.025 in MPFC ROI | **Primary**: f02 autobio salience |
| **Janata 2009** | fMRI | 13 | dMPFC tracks tonal space (tonality tracking) | P<0.005 (40-voxel cluster) | **f03 dMPFC tracking** |
| **Janata 2009** | fMRI | 13 | Familiarity → pre-SMA, IFG, SFG, thalamus, STG | P<0.001 uncorr (Table 2, multiple clusters) | **f01 familiarity index** |
| **Janata 2009** | fMRI | 13 | Combined FAV (familiarity+autobio+valence) in MPFC | FDR P<0.025 | **f04 positive affect** |
| **Salimpoor 2011** | PET [¹¹C]raclopride | 8 | DA release in caudate→NAcc during familiar music chills | r=0.71 (caudate BP vs chills) | **Supporting**: DA reward during familiar music |

### 3.2 Effect Size Summary

```
Primary Evidence (k=5): fMRI (Janata 2009) + PET (Salimpoor 2011)
Heterogeneity: Low — single primary fMRI study with PET convergence
Quality Assessment: β-tier (fMRI with behavioral + PET dopamine convergence)
Note: Janata 2009 N=13 (all female-dominated, 11/13 F). Small sample.
 Combined FAV contrast captures integrated familiarity-autobio-valence.
 Salimpoor 2011 provides DA mechanism for familiar music reward.
Replication: Consistent with Platel (2003) music-memory, Janata (2007) tonal space
```

---

## 4. R³ Input Mapping: What MEAMR Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | MEAMR Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [4] | sensory_pleasantness | Familiarity cue | Tonal recognition |
| **B: Energy** | [8] | loudness | Familiarity dynamics | Familiar loudness patterns |
| **C: Timbre** | [12] | warmth | Timbre familiarity | Brightness recognition |
| **C: Timbre** | [13] | spectral_centroid | Brightness familiarity | Timbre tracking |
| **D: Change** | [21] | spectral_change | Structural complexity | Memory accessibility |
| **D: Change** | [22] | energy_change | Temporal patterns | Time signature cues |
| **E: Interactions** | [41:49] | x_l5l6 (8D) | Memory-structure binding | Autobiographical salience |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | MEAMR Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **I: Information** | [87] | melodic_entropy | Melodic familiarity index — low melodic entropy signals familiar, predictable melodic patterns that trigger autobiographical memory retrieval and nostalgia-associated reward | Pearce 2005 IDyOM; Janata 2009 MEAM |

**Rationale**: MEAMR models music-evoked autobiographical memory reward. Memory retrieval is triggered by recognition of familiar musical patterns — melodic contour is the strongest cue for autobiographical memory (Janata 2009). melodic_entropy [87] provides a direct measure of melodic predictability: low values indicate familiar, well-learned melodic patterns that activate the hippocampal-striatal memory-reward circuit. Currently MEAMR infers familiarity from spectral_change [21] and timbre features, which are weaker proxies for melodic recognition.

**Code impact** (Phase 6): `r3_indices` extended to include [87]. Familiarity index computation augmented with melodic predictability measure.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[4] sensory_pleasantness ────┐
R³[8] loudness ────────────────┼──► Familiarity index
H³ trend/mean tuples ──────────┘ Recognition of familiar patterns

R³[41:49] x_l5l6 ─────────────┐
H³ long-range tuples ──────────┘ Memory-structure binding

R³[12] warmth ─────────────────┐
R³[13] spectral_centroid ──────┼──► dMPFC tonal space tracking

R³[4] sensory_pleasantness ────┘ vACC + SN reward signal
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

MEAMR requires H³ features at long time scales: familiarity assessment needs 1-5s context windows, and autobiographical salience benefits from sustained temporal integration to capture tonal trajectory recognition.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 4 | sensory_pleasantness | 8 | M1 (mean) | L2 (bidi) | Mean pleasantness over 500ms |
| 4 | sensory_pleasantness | 16 | M18 (trend) | L2 (bidi) | Pleasantness trend over 1s |
| 8 | loudness | 8 | M1 (mean) | L2 (bidi) | Mean loudness over 500ms |
| 8 | loudness | 16 | M1 (mean) | L2 (bidi) | Mean loudness over 1s |
| 12 | warmth | 16 | M1 (mean) | L2 (bidi) | Mean warmth over 1s |
| 13 | spectral_centroid | 16 | M1 (mean) | L2 (bidi) | Mean brightness over 1s |
| 21 | spectral_change | 8 | M20 (entropy) | L2 (bidi) | Structural entropy 500ms |
| 21 | spectral_change | 16 | M1 (mean) | L2 (bidi) | Mean structural change 1s |
| 22 | energy_change | 8 | M8 (velocity) | L0 (fwd) | Energy velocity at 500ms |
| 41 | x_l5l6[0] | 8 | M1 (mean) | L2 (bidi) | Memory-structure coupling 500ms |
| 41 | x_l5l6[0] | 16 | M1 (mean) | L2 (bidi) | Mean memory-structure 1s |
| 41 | x_l5l6[0] | 16 | M18 (trend) | L2 (bidi) | Memory-structure trend 1s |
| 41 | x_l5l6[0] | 16 | M5 (range) | L0 (fwd) | Memory-structure range 1s |
| 22 | energy_change | 16 | M18 (trend) | L0 (fwd) | Energy change trend 1s |

**v1 demand**: 14 tuples

#### R³ v2 Projected Expansion

No significant v2 expansion projected.

**v2 projected**: 0 tuples
**Total projected**: 14 tuples of 294,912 theoretical = 0.0047%

---

## 6. Output Space: 6D Multi-Layer Representation

### 6.1 Complete Output Specification

```
MEAMR OUTPUT TENSOR: 6D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0 │ f01_familiarity_index │ [0, 1] │ Musical familiarity level.
 │ │ │ f01 = σ(0.35 * pleasantness_trend_1s
 │ │ │ + 0.30 * mean_warmth_1s)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1 │ f02_autobio_salience │ [0, 1] │ Autobiographical salience.
 │ │ │ f02 = σ(0.35 * memory_struct_trend_1s
 │ │ │ + 0.30 * f01)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2 │ f03_dmpfc_tracking │ [0, 1] │ dMPFC tonal space tracking.
 │ │ │ f03 = σ(0.35 * mean_centroid_1s
 │ │ │ + 0.35 * mean_pleasantness_500ms
 │ │ │ + 0.30 * structural_entropy_500ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 3 │ f04_positive_affect │ [0, 1] │ Positive affect from familiar music.
 │ │ │ + 0.30 * f02 * f01)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4 │ memory_activation_state │ [0, 1] │ Current autobiographical activation.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 5 │ nostalgia_response_pred │ [0, 1] │ Predicted nostalgia response.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 6D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Autobiographical Memory Reward Function

```
Autobio_Salience = α·Familiarity + β·TonalTracking + γ·PositiveAffect

Parameters:
 α = 1.0 (familiarity weight)
 β = 0.8 (tonal tracking weight)
 γ = 0.7 (positive affect weight)

dMPFC_Tracking = f(tonal_trajectory, harmonic_complexity)
Positive_Affect = vACC_activation + SN_reward_signal

τ_decay = 10.0s (memory sustain window, long-term integration)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Familiarity Index
f01 = σ(0.35 * pleasantness_trend_1s
 + 0.30 * mean_warmth_1s)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Autobiographical Salience
f02 = σ(0.35 * memory_struct_trend_1s
 + 0.30 * f01)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f03: dMPFC Tracking
f03 = σ(0.35 * mean_centroid_1s
 + 0.35 * mean_pleasantness_500ms
 + 0.30 * structural_entropy_500ms)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f04: Positive Affect
 + 0.30 * f02 * f01)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# Temporal dynamics
dMemory/dt = τ⁻¹ · (Target_Activation - Current_Memory)
 where τ = 10.0s (long memory sustain)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | MEAMR Function |
|--------|-----------------|----------|---------------|---------------|
| **dMPFC (BA 8/9)** | 0, 52, 16 | 2 | Direct fMRI (Janata 2009: autobio+TT, FDR P<0.025) | Autobiographical salience + tonal tracking |
| **pre-SMA (BA 6)** | -2, 12, 54 | 1 | Direct fMRI (Janata 2009: familiarity, Z=5.37) | Familiarity motor response |
| **Bilateral STG** | ±60, -28, 16 / ±62, -22, 6 | 2 | Direct fMRI (Janata 2009: MusPlay+familiarity) | Auditory processing |
| **IFG (BA 44)** | -44, 14, 12 | 1 | Direct fMRI (Janata 2009: familiarity, Z=4.81) | Verbal/phonological processing |
| **Caudate/NAcc** | ±10, 12, -10 | 1 | PET DA (Salimpoor 2011: familiar music chills) | Dopamine reward during familiarity |

---

## 9. Cross-Unit Pathways

### 9.1 MEAMR ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ MEAMR INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ INTRA-UNIT (RPU): │
│ MEAMR.familiarity_index ─────► RPEM (familiarity → RPE modulation) │
│ MEAMR.positive_affect ───────► DAED (affect → DA consummation) │
│ MEAMR.autobio_salience ──────► MORMR (salience → opioid release) │
│ MEAMR.dmpfc_tracking ────────► IUCP (tonal tracking → complexity) │
│ │
│ CROSS-UNIT (RPU → IMU): │
│ MEAMR.familiarity_index ─────► IMU.memory_retrieval (familiar cue) │
│ MEAMR.memory_activation ─────► IMU.encoding_strength (consolidation) │
│ │
│ UPSTREAM DEPENDENCIES: │
│ R³ (~12D) ─────────────────────► MEAMR (direct spectral features) │
│ H³ (14 tuples) ────────────────► MEAMR (temporal dynamics) │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **dMPFC-autobio correlation** | dMPFC should correlate with autobiographical salience | ✅ **Confirmed** (p < 0.001, Janata 2009) |
| **dMPFC tonal tracking** | dMPFC should track tonal space of familiar music | ✅ **Confirmed** (p < 0.005, Janata 2009) |
| **Positive affect** | vACC + SN should correlate with positive affect | ✅ **Confirmed** (p < 0.001, Janata 2009) |
| **Unfamiliar music** | Unfamiliar music should show reduced dMPFC activation | Testable |
| **Memory interference** | Concurrent memory task should reduce MEAMR activation | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class MEAMR(BaseModel):
 """Music-Evoked Autobiographical Memory Reward Model.

 Output: 6D per frame.
 """
 NAME = "MEAMR"
 UNIT = "RPU"
 TIER = "β3"
 OUTPUT_DIM = 6
 TAU_DECAY = 10.0 # Long memory sustain (Janata 2009)

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """14 tuples for MEAMR computation."""
 return [
 # (r3_idx, horizon, morph, law)
 # ── Familiarity assessment ──
 (4, 8, 1, 2), # sensory_pleasantness, 500ms, mean, bidi
 (4, 16, 18, 2), # sensory_pleasantness, 1000ms, trend, bidi
 (8, 8, 1, 2), # loudness, 500ms, mean, bidi
 (8, 16, 1, 2), # loudness, 1000ms, mean, bidi
 (12, 16, 1, 2), # warmth, 1000ms, mean, bidi
 (13, 16, 1, 2), # spectral_centroid, 1000ms, mean, bidi
 # ── Structural complexity / memory ──
 (21, 8, 20, 2), # spectral_change, 500ms, entropy, bidi
 (21, 16, 1, 2), # spectral_change, 1000ms, mean, bidi
 (22, 8, 8, 0), # energy_change, 500ms, velocity, fwd
 (22, 16, 18, 0), # energy_change, 1000ms, trend, fwd
 # ── Memory-structure binding ──
 (41, 8, 1, 2), # x_l5l6[0], 500ms, mean, bidi
 (41, 16, 1, 2), # x_l5l6[0], 1000ms, mean, bidi
 (41, 16, 18, 2), # x_l5l6[0], 1000ms, trend, bidi
 (41, 16, 5, 0), # x_l5l6[0], 1000ms, range, fwd
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 """
 Compute MEAMR 6D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
 r3: (B,T,49) raw R³ features

 Returns:
 (B,T,6) MEAMR output
 """
 # Mechanism sub-sections
 # H³ direct features
 pleasantness_trend_1s = h3_direct[(4, 16, 18, 2)].unsqueeze(-1)
 mean_pleasantness_500ms = h3_direct[(4, 8, 1, 2)].unsqueeze(-1)
 mean_warmth_1s = h3_direct[(12, 16, 1, 2)].unsqueeze(-1)
 mean_centroid_1s = h3_direct[(13, 16, 1, 2)].unsqueeze(-1)
 structural_entropy_500ms = h3_direct[(21, 8, 20, 2)].unsqueeze(-1)
 memory_struct_trend_1s = h3_direct[(41, 16, 18, 2)].unsqueeze(-1)

 # ═══ LAYER E: Explicit features ═══

 # f01: Familiarity Index (coefficients sum = 1.0)
 f01 = torch.sigmoid(
 0.35 * pleasantness_trend_1s
 + 0.30 * mean_warmth_1s
 )

 # f02: Autobiographical Salience (coefficients sum = 1.0)
 f02 = torch.sigmoid(
 0.35 * memory_struct_trend_1s
 + 0.30 * f01
 )

 # f03: dMPFC Tracking (coefficients sum = 1.0)
 f03 = torch.sigmoid(
 0.35 * mean_centroid_1s
 + 0.35 * mean_pleasantness_500ms
 + 0.30 * structural_entropy_500ms
 )

 # f04: Positive Affect (coefficients sum = 1.0)
 f04 = torch.sigmoid(
 + 0.30 * (f02 * f01)
 )

 # ═══ LAYER P: Present ═══
 memory_activation = torch.sigmoid(
 0.5 * f02 + 0.5 * f01
 )

 # ═══ LAYER F: Future ═══
 nostalgia_pred = torch.sigmoid(
 0.5 * f04 + 0.5 * f02
 )

 return torch.cat([
 f01, f02, f03, f04, # E: 4D
 memory_activation, # P: 1D
 nostalgia_pred, # F: 1D
 ], dim=-1) # (B, T, 6)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 2 (Janata 2009, Salimpoor 2011) | Primary fMRI + supporting PET |
| **Effect Sizes** | 5 (autobio salience, TT, familiarity, FAV, DA chills) | fMRI + PET |
| **Evidence Modality** | fMRI (N=13), PET (N=8) | Convergent evidence |
| **Falsification Tests** | 3/5 confirmed | High validity |
| **R³ Features Used** | ~12D of 49D | Consonance + energy + timbre + change + interactions |
| **H³ Demand** | 14 tuples (0.61%) | Sparse, efficient |
| **Output Dimensions** | **6D** | 3-layer structure |

---

## 13. Scientific References

1. **Janata, P. (2009)**. The neural architecture of music-evoked autobiographical memories. *Cerebral Cortex*, 19(11), 2579-2594.

2. **Salimpoor, V. N., Benovoy, M., Larcher, K., Dagher, A., & Zatorre, R. J. (2011)**. Anatomically distinct dopamine release during anticipation and experience of peak emotion to music. *Nature Neuroscience*, 14(2), 257-262.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Familiarity | S⁰.L6[55:60] + S⁰.L5[35,38] + HC⁰.HRM | R³.sensory_pleasantness[4] + R³.warmth[12] |
| Autobio salience | S⁰.X_L5L6[208:216] + HC⁰.SGM | R³.x_l5l6[41:49] |
| Tonal tracking | S⁰.L9.entropy_T[116] + S⁰.L4.velocity_T[15] | R³.spectral_centroid[13] + H³ entropy/mean tuples |
| Affect | S⁰.L5.loudness[35] + HC⁰ affect | R³.loudness[8] |
| Demand format | HC⁰ index ranges (30 tuples) | H³ 4-tuples (14 tuples, sparse) |
| Total demand | 30/2304 = 1.30% | 14/2304 = 0.61% |
| Output | 6D | 6D (same) |

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **6D**
**Evidence Tier**: **β (Bridging)**
**Confidence**: **70-90%**
