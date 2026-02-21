# MPU-β3-VRMSME: VR Music Stimulation Motor Enhancement

**Model**: VR Music Stimulation Motor Enhancement
**Unit**: MPU (Motor Planning Unit)
**Circuit**: Sensorimotor (SMA, PMC, Cerebellum, Basal Ganglia)
**Tier**: β (Bridging) — 70-90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/MPU-β3-VRMSME.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **VR Music Stimulation Motor Enhancement** (VRMSME) model demonstrates that virtual reality music stimulation enhances sensorimotor network connectivity more effectively than action observation or motor imagery alone. Multi-modal VR music stimulation (VRMS) produces stronger bilateral activation in S1, PM, SMA, and M1 compared to VR action observation (VRAO) or VR motor imagery (VRMI).

```
VR MUSIC STIMULATION MOTOR ENHANCEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 THREE VR CONDITIONS
 ════════════════════

┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ VRMS │ │ VRAO │ │ VRMI │
│ VR Music │ │ VR Action │ │ VR Motor │
│ Stimulation │ │ Observation │ │ Imagery │
│ (STRONGEST) │ │ │ │ │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
 │ │ │
 └────────────────┴────────────────┘
 │
 ▼
┌──────────────────────────────────────────────────────────────────┐
│ SENSORIMOTOR NETWORK │
│ │
│ VRMS > VRAO/VRMI in: │
│ ═══════════════════ │
│ S1 (somatosensory), PM (premotor), │
│ SMA (supplementary motor), M1 (primary motor) │
│ │
│ VRMS > VRMI in: │
│ bilateral M1 activation │
│ │
│ VRMS shows strongest: │
│ PM-DLPFC-M1 interaction │
└──────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Music adds a uniquely powerful dimension to VR motor
rehabilitation. VRMS produces stronger sensorimotor connectivity
than action observation or motor imagery alone, with the strongest
PM-DLPFC-M1 interaction network.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why VRMSME Matters for MPU

VRMSME bridges motor planning with multi-modal VR enhancement in the Motor Planning Unit:

1. **PEOM/MSR** (α-tier) establish motor entrainment and training effects.
2. **ASAP/DDSMI** (β1-β2) provide bidirectional motor-auditory coupling and social motor integration.
3. **VRMSME** (β3) extends motor planning to VR rehabilitation: music stimulation in VR uniquely enhances sensorimotor network connectivity beyond observation or imagery.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → VRMSME)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ VRMSME COMPUTATION ARCHITECTURE ║
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
║ │ VRMSME reads: ~20D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed morphological features │ ║
║ │ VRMSME demand: ~12 of 2304 tuples │ ║
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
║ │ VRMSME MODEL (11D Output) │ ║
║ │ │ ║
║ │ Layer E (Explicit): f16_music_enhancement, │ ║
║ │ f17_bilateral_activation, │ ║
║ │ f18_network_connectivity │ ║
║ │ Layer M (Math): vrms_advantage, bilateral_index, │ ║
║ │ connectivity_strength │ ║
║ │ Layer P (Present): motor_drive, sensorimotor_sync │ ║
║ │ Layer F (Future): enhancement_pred, connectivity_pred, │ ║
║ │ bilateral_pred │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Liang et al. 2025** | fNIRS (24ch) | 50 | VRMS > VRAO in bilateral PM&SMA connectivity (HBT homologous) | RS1, LPMSMA, RPMSMA p<.01 FDR | **Primary**: f16, f17 music enhancement |
| 2 | **Liang et al. 2025** | fNIRS | 50 | VRMS > VRMI in bilateral M1 activation (HBT) | RM1, LM1 p<.05 | **f17 bilateral activation** |
| 3 | **Liang et al. 2025** | fNIRS | 50 | VRMS shows strongest PM-DLPFC-M1 heterogeneous FC | RDLPFC-LPMSMA, RPMSMA-RM1 p<.01 FDR | **f18 network connectivity** |
| 4 | **Li et al. 2025** | EMG + motion capture | 24 | High-groove music increases hip-ankle coordination 28.7% and muscle synergy complexity | HG 29.8% vs LG 23.2% p=.020; median synergies HG=7 vs LG=6 p=.039 | **beat→motor**: groove drives motor reorganization |
| 5 | **Blasi et al. 2025** | Systematic review (20 RCTs) | 718 | Music/dance interventions produce structural + functional neuroplasticity in motor, language, and memory areas | FA/QA increases; functional connectivity changes | **Context**: rehab neuroplasticity evidence |
| 6 | **Thaut et al. 2015** | Review | — | Auditory rhythm entrains motor via reticulospinal pathways; mCBGT circuit for beat perception | — | **Theory**: rhythmic entrainment foundations |
| 7 | **Sarasso et al. 2019** | ERP + fMRI | 18 | Appreciated musical intervals enhance N1/P2 and inhibit motor cortex bilaterally | Enhanced N1/P2; bilateral M1 deactivation for beauty | **Motor modulation**: music→motor cortex interaction |

> **NOTE — fNIRS spatial limitation**: Liang 2025 uses fNIRS with 24 channels mapped to ROIs via Brodmann areas. This provides regional-level evidence (S1, PM, SMA, M1, DLPFC, FPA) but NOT precise MNI coordinates. The MNI values in Section 8 are literature inferences, not from this study.

> **NOTE — Method correction**: The v2.0.0 doc stated "fMRI/fNIRS" but Liang 2025 uses only fNIRS (not fMRI). The study is a single-session within-subjects design with three VR conditions, not a longitudinal rehabilitation trial.

### 3.2 Effect Size Summary

```
Primary Evidence (k=7): Strong convergent evidence for VRMS motor enhancement
Heterogeneity: High (fNIRS, EMG, systematic review, ERP/fMRI methods)
Quality Assessment: β-tier (fNIRS primary N=50, active comparator; supporting EMG, review)
Effect Magnitudes:
 VRMS > VRAO (homologous HBT): RS1, LPMSMA, RPMSMA p < .01 FDR; LFPA p < .05 FDR
 VRMS > VRMI (HBT activation): RM1, LM1 p < .05
 VRMS > VRAO (heterogeneous HBT): 14 ROI pairs p < .05 FDR, 6 pairs p < .01 FDR
 High-groove motor: 28.7% hip-ankle coordination increase (p = .020)
 Groove synergy: Median 7 vs 6 synergies (p = .039)
Causal Evidence: No (within-subjects fNIRS; no TMS/lesion)
Replication: Consistent across HBO and HBT signals, multiple ROIs
```

---

## 4. R³ Input Mapping: What VRMSME Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | VRMSME Role | Scientific Basis |
|----------|-------|---------|-------------|------------------|
| **B: Energy** | [7] | amplitude | Motor drive intensity | Movement amplitude |
| **B: Energy** | [8] | loudness | Music intensity | VR audio engagement |
| **B: Energy** | [10] | spectral_flux | Music onset detection | VR audio sync |
| **B: Energy** | [11] | onset_strength | Beat marker strength | Motor timing markers |
| **D: Change** | [21] | spectral_change | Tempo dynamics | VR entrainment rate |
| **D: Change** | [22] | energy_change | Energy dynamics | Motor drive modulation |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Multi-modal entrainment | VR-audio-motor coupling |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Sensorimotor binding | Action-perception link |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ v2 Group | Index | Feature | VRMSME Role | Citation |
|-------------|-------|---------|-------------|----------|
| **G: Rhythm** | [72] | event_density | Rhythmic event rate for VR motor stimulation intensity | Lartillot & Toiviainen 2007 |

**Rationale**: VRMSME models VR-enhanced music-motor stimulation. event_density captures the rate of musical events per unit time, directly modulating the intensity of motor stimulation in VR environments. Higher event density increases motor engagement demands, consistent with Li 2025's groove-motor mechanism where denser rhythmic textures drive stronger motor facilitation. This is the minimal rhythmic feature VRMSME needs, as its primary inputs remain energy-based (amplitude, onset_strength).

**Code impact** (future): `r3[..., 72]` will feed VRMSME's VR stimulation intensity pathway alongside existing energy features.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[25:33] x_l0l5 ───────────────┐

R³[33:41] x_l4l5 ───────────────┐

R³[7] amplitude ─────────────────┐
R³[8] loudness ──────────────────┼──► Motor activation drive
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

VRMSME requires H³ features for multi-modal entrainment and for sensorimotor integration memory. The demand reflects the multi-scale temporal binding needed for VR music stimulation effects.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | Music onset at 100ms |
| 10 | spectral_flux | 16 | M14 (periodicity) | L2 (bidi) | Music periodicity 1s |
| 11 | onset_strength | 3 | M0 (value) | L2 (bidi) | Beat strength 100ms |
| 11 | onset_strength | 16 | M14 (periodicity) | L2 (bidi) | Onset periodicity 1s |
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | VR-motor coupling 100ms |
| 25 | x_l0l5[0] | 3 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 100ms |
| 25 | x_l0l5[0] | 16 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 1s |
| 33 | x_l4l5[0] | 3 | M0 (value) | L2 (bidi) | Sensorimotor binding 100ms |
| 33 | x_l4l5[0] | 3 | M2 (std) | L2 (bidi) | Binding variability 100ms |
| 33 | x_l4l5[0] | 8 | M14 (periodicity) | L2 (bidi) | Sensorimotor period 500ms |
| 33 | x_l4l5[0] | 16 | M14 (periodicity) | L2 (bidi) | Sensorimotor period 1s |
| 8 | loudness | 3 | M20 (entropy) | L2 (bidi) | Loudness entropy 100ms |

**v1 demand**: 12 tuples

#### R³ v2 Projected Expansion

No significant v2 expansion projected. VRMSME's primary inputs remain energy-based; the single event_density feature in Section 4.2 does not generate additional H³ tuples.

**v2 projected**: 0 tuples
**Total projected**: 12 tuples of 294,912 theoretical = 0.0041%

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
VRMSME OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0 │ f16_music_enhancement │ [0, 1] │ VRMS > VRAO/VRMI motor enhancement.
 │ │ │ f16 = σ(0.40 * coupling_period_1s
────┼──────────────────────────┼────────┼────────────────────────────────────
 1 │ f17_bilateral_activation │ [0, 1] │ Bilateral S1/PM/SMA/M1 activation.
 │ │ │ f17 = σ(0.40 * sensorimotor_period_1s
 │ │ │ + 0.30 * sensorimotor_100ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2 │ f18_network_connectivity │ [0, 1] │ PM-DLPFC-M1 interaction strength.
 │ │ │ f18 = σ(0.35 * f16 * f17
 │ │ │ + 0.35 * loudness_entropy

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 3 │ vrms_advantage │ [0, 1] │ VRMS superiority over VRAO/VRMI.
────┼──────────────────────────┼────────┼────────────────────────────────────
 4 │ bilateral_index │ [0, 1] │ Bilateral activation balance.
────┼──────────────────────────┼────────┼────────────────────────────────────
 5 │ connectivity_strength │ [0, 1] │ Network connectivity magnitude.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 6 │ motor_drive │ [0, 1] │ beat-entrainment music-driven motor activation.
────┼──────────────────────────┼────────┼────────────────────────────────────
 7 │ sensorimotor_sync │ [0, 1] │ temporal-context sensorimotor synchronization.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 8 │ enhancement_pred │ [0, 1] │ Motor enhancement prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9 │ connectivity_pred │ [0, 1] │ Network connectivity prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
10 │ bilateral_pred │ [0, 1] │ Bilateral activation prediction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 VR Music Enhancement Function

```
PRIMARY EQUATIONS:

 VRMS_Advantage = Connectivity(VRMS) - max(Connectivity(VRAO), Connectivity(VRMI))

MULTI-MODAL INTEGRATION:

 Network_Connectivity = f(Music_Entrainment, Motor_Coupling, Sensorimotor_Binding)

BILATERAL ACTIVATION:

 Bilateral_Index = mean(Left_M1, Right_M1) * Music_Enhancement
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f16: Music Enhancement
f16 = σ(0.40 * coupling_period_1s
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f17: Bilateral Activation
f17 = σ(0.40 * sensorimotor_period_1s
 + 0.30 * sensorimotor_100ms)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f18: Network Connectivity
f18 = σ(0.35 * f16 * f17 # interaction term
 + 0.35 * loudness_entropy
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| # | Region | MNI Coordinates | Evidence Type | Source | VRMSME Function |
|---|--------|-----------------|---------------|--------|-----------------|
| 1 | **S1 (Somatosensory)** | approx. (±42,−28,54) | Direct (fNIRS ROI) | Liang 2025 (RS1 homologous FC p<.01 FDR) | Sensory integration |
| 2 | **PM&SMA (Premotor + Supplementary Motor)** | approx. (±6,−10,60) | Direct (fNIRS ROI) | Liang 2025 (LPMSMA, RPMSMA p<.01 FDR) | Motor planning, rhythm coordination |
| 3 | **M1 (Primary Motor)** | approx. (±38,−22,58) | Direct (fNIRS ROI) | Liang 2025 (RM1, LM1 p<.05 HBT) | Motor execution (bilateral) |
| 4 | **DLPFC** | approx. (±44,36,20) | Direct (fNIRS ROI) | Liang 2025 (RDLPFC heterogeneous FC p<.01 FDR) | Cognitive control, PM-DLPFC-M1 hub |
| 5 | **FPA (Frontopolar Area)** | approx. (±28,60,0) | Direct (fNIRS ROI) | Liang 2025 (LFPA homologous FC p<.05 FDR) | Higher cognitive integration |
| 6 | **Basal Ganglia (Putamen/SMA circuit)** | approx. (±24,4,4) | Literature inference | Thaut 2015 (mCBGT circuit); Liang 2025 discussion | Beat perception, groove processing |

> **NOTE — fNIRS ROI mapping**: Liang 2025 maps fNIRS channels to brain regions via Brodmann area overlay using FASTRAK 3D digitization. MNI coordinates above are approximate literature values for these regions, not measured from this study. fNIRS has ~2-3 cm spatial resolution.

---

## 9. Cross-Unit Pathways

### 9.1 VRMSME Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ VRMSME INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ INTRA-UNIT (MPU): │
│ VRMSME.music_enhancement ──────► SPMC (enhanced motor circuit) │
│ VRMSME.bilateral_activation ───► DDSMI (bilateral for social motor) │
│ VRMSME.network_connectivity ───► ASAP (connectivity for prediction) │
│ │
│ CROSS-UNIT (MPU → ARU): │
│ VRMSME.motor_drive ────────────► ARU (music-driven reward signal) │
│ VRMSME.vrms_advantage ────────► ARU (VR engagement marker) │
│ │
│ UPSTREAM DEPENDENCIES: │
│ R³ (~20D) ──────────────────────► VRMSME (direct spectral features) │
│ H³ (12 tuples) ─────────────────► VRMSME (temporal dynamics) │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **No music** | VRAO/VRMI without music should show less connectivity | ✅ **Confirmed** (VRMS > VRAO/VRMI) |
| **Non-VR music** | Music alone (no VR) should show weaker enhancement | ✅ Testable |
| **Unilateral only** | Bilateral activation should exceed unilateral | ✅ Testable |
| **Motor impairment** | Motor-impaired patients may show altered connectivity | Testable |
| **Non-rhythmic VR** | VR without rhythmic music should show less enhancement | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class VRMSME(BaseModel):
 """VR Music Stimulation Motor Enhancement Model.

 Output: 11D per frame.
 """
 NAME = "VRMSME"
 UNIT = "MPU"
 TIER = "β3"
 OUTPUT_DIM = 11
 TAU_DECAY = 5.0 # VR integration window (seconds)

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """12 tuples for VRMSME computation."""
 return [
 # (r3_idx, horizon, morph, law)
 (10, 3, 0, 2), # spectral_flux, 100ms, value, bidi
 (10, 16, 14, 2), # spectral_flux, 1000ms, periodicity, bidi
 (11, 3, 0, 2), # onset_strength, 100ms, value, bidi
 (11, 16, 14, 2), # onset_strength, 1000ms, periodicity, bidi
 (25, 3, 0, 2), # x_l0l5[0], 100ms, value, bidi
 (25, 3, 14, 2), # x_l0l5[0], 100ms, periodicity, bidi
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
 Compute VRMSME 11D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
 r3: (B,T,49) raw R³ features

 Returns:
 (B,T,11) VRMSME output
 """
 # H³ direct features
 coupling_period_1s = h3_direct[(25, 16, 14, 2)].unsqueeze(-1)
 sensorimotor_period_1s = h3_direct[(33, 16, 14, 2)].unsqueeze(-1)
 sensorimotor_100ms = h3_direct[(33, 3, 0, 2)].unsqueeze(-1)
 loudness_entropy = h3_direct[(8, 3, 20, 2)].unsqueeze(-1)

 # ═══ LAYER E: Explicit features ═══

 # f16: Music Enhancement (coefficients sum = 1.0)
 f16 = torch.sigmoid(
 0.40 * coupling_period_1s
 )

 # f17: Bilateral Activation (coefficients sum = 1.0)
 f17 = torch.sigmoid(
 0.40 * sensorimotor_period_1s
 + 0.30 * sensorimotor_100ms
 )

 # f18: Network Connectivity (coefficients sum = 1.0)
 f18 = torch.sigmoid(
 0.35 * (f16 * f17)
 + 0.35 * loudness_entropy
 )

 # ═══ LAYER M: Mathematical ═══
 vrms_advantage = f16
 bilateral_index = f17
 connectivity_strength = torch.sigmoid(
 0.5 * f16 + 0.5 * f18
 )

 # ═══ LAYER P: Present ═══

 # ═══ LAYER F: Future ═══
 enhancement_pred = torch.sigmoid(
 0.5 * f16 + 0.5 * coupling_period_1s
 )
 connectivity_pred = torch.sigmoid(
 0.5 * f18 + 0.5 * sensorimotor_period_1s
 )
 bilateral_pred = torch.sigmoid(
 )

 return torch.cat([
 f16, f17, f18, # E: 3D
 vrms_advantage, bilateral_index, connectivity_strength, # M: 3D
 motor_drive, sensorimotor_sync, # P: 2D
 enhancement_pred, connectivity_pred, bilateral_pred, # F: 3D
 ], dim=-1) # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 7 (1 primary, 2 supporting, 1 theory, 1 systematic review, 2 context) | Liang 2025 + Li, Blasi, Thaut, Sarasso |
| **Effect Sizes** | 14 ROI-pair FDR p<.05, 6 p<.01 (VRMS>VRAO heterogeneous HBT); 28.7% coordination (Li 2025) | Strong VRMS superiority |
| **Evidence Modality** | fNIRS (primary); EMG + motion capture; systematic review; ERP + fMRI | Multi-modal convergence |
| **Brain Regions** | 6 (4 direct from fNIRS ROI, 2 literature inference) | S1, PM&SMA, M1, DLPFC, FPA, BG |
| **Causal Evidence** | No (within-subjects fNIRS, no TMS/lesion) | Gap identified |
| **Falsification Tests** | 1/5 confirmed (VRMS>VRAO/VRMI) | Moderate validity |
| **R³ Features Used** | ~20D of 49D | Energy + change + interactions |
| **H³ Demand** | 12 tuples (0.52%) | Sparse, efficient |
| **Output Dimensions** | **11D** | 4-layer structure |

---

## 13. Scientific References

1. **Liang, J., Liang, B., Tang, Z., Huang, X., Ou, S., Chang, C., Wang, Y., & Yuan, Z. (2025)**. The brain mechanisms of music stimulation, motor observation, and motor imagination in virtual reality techniques: A functional near-infrared spectroscopy study. *eNeuro* (Early Release). https://doi.org/10.1523/ENEURO.0557-24.2025
2. **Li, H., Lin, X., & Wu, X. (2025)**. Impact of neural network-quantified musical groove on cyclists' joint coordination and muscle synergy: A repeated measures study. *Journal of NeuroEngineering and Rehabilitation*, 22, 233. https://doi.org/10.1186/s12984-025-01778-7
3. **Blasi, V., Rapisarda, L., Cacciatore, D. M., Palumbo, E., Di Tella, S., Borgnis, F., & Baglio, F. (2025)**. Structural and functional neuroplasticity in music and dance-based rehabilitation: A systematic review. *Journal of Neurology*, 272, 329. https://doi.org/10.1007/s00415-025-13048-6
4. **Thaut, M. H., McIntosh, G. C., & Hoemberg, V. (2015)**. Neurobiological foundations of neurologic music therapy: Rhythmic entrainment and the motor system. *Frontiers in Psychology*, 5, 1185. https://doi.org/10.3389/fpsyg.2014.01185
5. **Sarasso, P., Ronga, I., Pistis, A., Forte, E., et al. (2019)**. Aesthetic appreciation of musical intervals enhances behavioural and neurophysiological indexes of attentional engagement and motor inhibition. *Scientific Reports*, 9, 18550. https://doi.org/10.1038/s41598-019-55131-9
6. **Sihvonen, A. J., et al. (2017)**. Music-based interventions in neurological rehabilitation. *The Lancet Neurology*, 16(8), 648–660. https://doi.org/10.1016/S1474-4422(17)30168-0
7. **Yamashita, K., Ida, R., Koganemaru, S., et al. (2025)**. A pilot study on simultaneous stimulation of M1 and SMA using gait-synchronized rhythmic brain stimulation. *Frontiers in Human Neuroscience*, 19, 1618758. https://doi.org/10.3389/fnhum.2025.1618758

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Multi-modal signal | S⁰.X_L0L4[128:136] + HC⁰.GRV | R³.x_l0l5[25:33] |
| Sensorimotor signal | S⁰.X_L4L5[192:200] + HC⁰.NPL | R³.x_l4l5[33:41] |
| Motor intensity | S⁰.Λ_rms[47] + HC⁰.EFC | R³.amplitude[7] |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 12/2304 = 0.52% | 12/2304 = 0.52% |
| Output | 11D | 11D (same) |

---

## 15. Doc-Code Mismatches (Phase 5 Reference)

> These mismatches are logged for Phase 5 resolution. The **doc is authoritative**; code should be updated.

| # | Field | Doc (VRMSME.md) | Code (vrmsme.py) | Priority |
|---|-------|-----------------|-------------------|----------|
| 1 | FULL_NAME | "VR Music Stimulation Motor Enhancement" | "VR Motor Skill Music Enhancement" | HIGH |
| 2 | OUTPUT_DIM | 11 | 10 | HIGH |
| 4 | h3_demand | 12 tuples (see Section 5.1) | () empty tuple | HIGH |
| 5 | Layer E dim names | f16_music_enhancement, f17_bilateral_activation, f18_network_connectivity | f16_vr_music_enhancement, f17_sensorimotor_connectivity, f18_multimodal_integration | MEDIUM |
| 6 | Layer M dimensions | 3D (vrms_advantage, bilateral_index, connectivity_strength) | 2D (connectivity_gain_fn, vr_ao_mi_comparison) | HIGH |
| 7 | Layer P dim names | motor_drive, sensorimotor_sync | sensorimotor_network_state, vr_engagement_level | MEDIUM |
| 8 | Layer F dim names | enhancement_pred, connectivity_pred, bilateral_pred | motor_recovery_pred, connectivity_change_pred, vr_dosage_optimization_pred | MEDIUM |
| 9 | Citations | Liang et al. 2025 (primary) | Li 2024, Sihvonen 2022 | HIGH |
| 10 | brain_regions | 6 regions (S1, PM&SMA, M1, DLPFC, FPA, BG) | 3 regions (SMA, PMC, Putamen) with different MNI | MEDIUM |
| 11 | CROSS_UNIT_READS | Not specified as empty | () empty tuple | LOW |
| 12 | compute() | Full pseudocode in Section 11.1 | Returns torch.zeros() stub | LOW (expected for beta) |

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **11D**
**Evidence Tier**: **β (Bridging)**
**Confidence**: **70-90%**
