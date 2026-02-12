# IMU-β7-VRIAP: VR-Integrated Analgesia Paradigm

**Model**: VR-Integrated Analgesia Paradigm
**Unit**: IMU (Integrative Memory Unit)
**Circuit**: Mnemonic (Hippocampal-Cortical)
**Tier**: β (Integrative) — 70-90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, MEM mechanism)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/IMU-β7-VRIAP.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **VR-Integrated Analgesia Paradigm** (VRIAP) models how active motor interaction with music in a virtual-reality environment produces stronger analgesic effects than passive listening alone. The mechanism operates through enhanced visual-sensorimotor cortical activation and reduced connectivity within the pain processing matrix (S1, insula). This positions music-VR synergy as a multi-modal cognitive intervention where motor engagement actively gates pain signals.

```
THE TWO MODES OF MUSIC-VR ANALGESIA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACTIVE MODE (motor interaction)         PASSIVE MODE (listening only)
Brain: S1↓, Premotor↑, Occipital↑      Brain: S1 connectivity maintained
Mechanism: Efference copy + gating      Mechanism: Auditory distraction only
Motor coupling: Strong                  Motor coupling: None
Function: "Engaged body = less pain"    Function: "Diverted attention"
Evidence: t=2.59-3.99, p<0.001-0.015   Evidence: Moderate activation

              PAIN MATRIX MODULATION
              Brain: S1 (primary somatosensory), Insula
              Mechanism: Connectivity reduction
              Trigger: Active motor engagement × musical structure
              Function: "Disconnect pain processing"
              Evidence: t=-4.64 to -3.53, p=0.029-0.049

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Key finding: Active VR + music > passive listening for analgesia.
Motor interaction modulates S1 connectivity, reducing pain signal
propagation through the somatosensory cortex.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why Music-VR Synergy Is Special for Pain Modulation

Music combined with active VR engagement produces analgesia beyond what either modality achieves alone because:

1. **Motor gating of pain**: Active motor engagement generates efference copies that suppress afferent pain signals at the spinal and cortical level — S1 connectivity decreases when the motor system is actively engaged with musical structure.

2. **Multi-modal binding**: VR creates a rich sensory environment where visual, auditory, and proprioceptive signals compete with nociceptive input for attentional resources — the hippocampus binds these multi-modal streams into a coherent non-pain experience.

3. **Groove-driven engagement**: Musical features (rhythm, loudness dynamics, onset patterns) drive motor coupling through groove processing — stronger groove = stronger motor engagement = greater analgesic effect.

4. **Memory consolidation of analgesia**: The mPFC-hippocampal circuit encodes the pain-free state associated with active music engagement, potentially building long-term analgesic associations for therapeutic use.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The VRIAP Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 VRIAP — COMPLETE CIRCUIT                                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    AUDITORY CORTEX (STG/A1)                        │    ║
║  │                                                                     │    ║
║  │  Core (A1)      Belt           Parabelt                             │    ║
║  │  Spectrotemporal Feature       Rhythmic pattern                    │    ║
║  │  encoding        extraction    Groove + onset detection             │    ║
║  └──────┬──────────────┬──────────────────┬────────────────────────────┘    ║
║         │              │                  │                                  ║
║         │              │                  │                                  ║
║         ▼              ▼                  ▼                                  ║
║  ┌──────────────────┐          ┌────────────────────┐                       ║
║  │   PREMOTOR CTX   │          │     mPFC           │                       ║
║  │                  │          │                    │                       ║
║  │  Motor planning  │          │  Pain appraisal    │                       ║
║  │  Efference copy  │          │  Self-referential   │                       ║
║  │  generation      │          │  processing         │                       ║
║  │                  │          │                    │                       ║
║  └────────┬─────────┘          └─────────┬──────────┘                       ║
║           │                              │                                  ║
║           └──────────────┬───────────────┘                                  ║
║                          │                                                  ║
║                          ▼                                                  ║
║  ┌─────────────────────────────────────────────────────────────┐            ║
║  │                    PAIN MODULATION HUB                       │            ║
║  │                                                             │            ║
║  │  ┌─────────────────────┐  ┌───────────────────────┐        │            ║
║  │  │    S1 (Primary      │  │       INSULA          │        │            ║
║  │  │    Somatosensory)   │  │   (Anterior/Posterior) │        │            ║
║  │  │                     │  │                       │        │            ║
║  │  │  • Pain signal      │  │  • Interoception      │        │            ║
║  │  │    propagation ↓    │  │  • Pain awareness     │        │            ║
║  │  │  • Connectivity     │  │  • Salience gating    │        │            ║
║  │  │    reduced by       │  │                       │        │            ║
║  │  │    active mode      │  │                       │        │            ║
║  │  └─────────────────────┘  └───────────────────────┘        │            ║
║  │                                                             │            ║
║  │  ┌─────────────────────┐  ┌───────────────────────┐        │            ║
║  │  │    HIPPOCAMPUS      │  │       mPFC            │        │            ║
║  │  │                     │  │                       │        │            ║
║  │  │  • Multi-modal      │  │  • Context encoding   │        │            ║
║  │  │    binding           │  │  • Therapeutic        │        │            ║
║  │  │  • Analgesic memory │  │    association         │        │            ║
║  │  │    consolidation    │  │                       │        │            ║
║  │  └─────────────────────┘  └───────────────────────┘        │            ║
║  │                                                             │            ║
║  └──────────────────────────┬──────────────────────────────────┘            ║
║                             │                                                ║
║                             ▼                                                ║
║              ANALGESIC RESPONSE + MOTOR-PAIN GATING                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Active > passive analgesia:        n=15, p=0.001
Active > passive activation:       n=15, p=0.001 (premotor, occipital)
Active < passive S1 connectivity:  n=15, t=-4.64 to -3.53, p=0.029-0.049
```

### 2.2 Information Flow Architecture (EAR → BRAIN → MEM → VRIAP)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    VRIAP COMPUTATION ARCHITECTURE                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  AUDIO (44.1kHz waveform)                                                    ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌──────────────────┐                                                        ║
║  │ COCHLEA          │  128 mel bins × 172.27Hz frame rate                    ║
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
║  │  │roughness  │ │amplitude│ │warmth   │ │flux      │ │x_l0l5  │ │        ║
║  │  │sethares   │ │loudness │ │tristim. │ │entropy   │ │x_l4l5  │ │        ║
║  │  │pleasant.  │ │onset    │ │tonalness│ │concent.  │ │x_l5l7  │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         VRIAP reads: 36D                         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Encoding ──┐ ┌── Consolidation ─┐ ┌── Retrieval ──────┐   │        ║
║  │  │ 1s (H16)     │ │ 5s (H20)         │ │ 36s (H24)        │   │        ║
║  │  │              │ │                   │ │                   │   │        ║
║  │  │ Motor-pain   │ │ Analgesic         │ │ Session-level     │   │        ║
║  │  │ gating       │ │ integration       │ │ consolidation     │   │        ║
║  │  └──────┬───────┘ └──────┬────────────┘ └──────┬────────────┘   │        ║
║  │         │               │                      │                │        ║
║  │         └───────────────┴──────────────────────┘                │        ║
║  │                         VRIAP demand: ~18 of 2304 tuples        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Mnemonic Circuit ═════════    ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  MEM (30D)      │  Memory Encoding & Retrieval mechanism                 ║
║  │                 │                                                        ║
║  │ Encoding  [0:10]│  novelty, binding strength, schema match               ║
║  │ Familiar [10:20]│  recognition, nostalgia, déjà-vu                       ║
║  │ Retrieval[20:30]│  recall probability, vividness, coloring               ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    VRIAP MODEL (10D Output)                      │        ║
║  │                                                                  │        ║
║  │  Layer E (Episodic):   f01_engagement, f02_pain_gate,            │        ║
║  │                        f03_multimodal_bind                       │        ║
║  │  Layer M (Math):       analgesia_index, active_passive_diff      │        ║
║  │  Layer P (Present):    motor_pain_state, s1_connectivity         │        ║
║  │  Layer F (Future):     analgesia_pred, engagement_pred,          │        ║
║  │                        (reserved)                                │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **VR analgesia RCT (2024)** | fMRI + behavioral | 15 | Active VR > passive for analgesia; S1 connectivity reduced | t=2.59-3.99, p<0.001 | **MEM.encoding_state: motor-pain gating** |
| **VR analgesia activation (2024)** | fMRI | 15 | Active mode: premotor + occipital activation increase | t=2.59-3.99, p=0.001-0.015 | **MEM.encoding_state: sensorimotor engagement** |
| **S1 connectivity (2024)** | fMRI connectivity | 15 | Active < passive S1 connectivity | t=-4.64 to -3.53, p=0.029-0.049 | **MEM.retrieval_dynamics: pain matrix decoupling** |
| **Music distraction meta-analysis** | Systematic review | Multiple | Music reduces pain perception across conditions | Moderate effects | **MEM.familiarity_proxy: auditory distraction baseline** |
| **Gate control theory (Melzack & Wall 1965)** | Theory | — | Non-nociceptive input gates pain signal transmission | — | **Why motor engagement gates pain** |

### 3.2 The Temporal Story: Music-VR Analgesia Dynamics

```
COMPLETE TEMPORAL PROFILE OF MUSIC-VR ANALGESIA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1: AUDITORY ENGAGEMENT (continuous, <1s)
─────────────────────────────────────────────
Auditory cortex encodes spectrotemporal patterns.
Rhythmic structure drives groove detection.
Onset strength and loudness dynamics processed.
R³ input: Energy [7:12] + Change [21:25]

Phase 2: MOTOR COUPLING (0.5-2s, H16 window)
────────────────────────────────────────────────────
Premotor cortex generates efference copies.
Active engagement initiates motor-sensory loop.
Groove features (onset, amplitude velocity) drive coupling.
MEM.encoding_state activates (motor-pain binding).

Phase 3: PAIN GATING (2-5s, H20 window)
─────────────────────────────────────────
S1 connectivity reduction begins.
Motor engagement competes with nociceptive input.
Insula salience gating redirected to musical stream.
MEM.retrieval_dynamics produces pain modulation signal.

Phase 4: ANALGESIC INTEGRATION (5-15s, sustained)
───────────────────────────────────────────────────
Multi-modal binding (auditory + visual + motor) stabilizes.
Hippocampal context encoding consolidates pain-free state.
mPFC appraisal shifts from pain to engagement.
Full analgesic effect emerges.

Phase 5: THERAPEUTIC CONSOLIDATION (36s+, H24 window)
───────────────────────────────────────────────────
Hippocampus-mPFC circuit encodes analgesic association.
Long-term context: active engagement = pain relief.
This is how repeated music-VR therapy builds lasting effects.
```

### 3.3 Effect Size Summary

```
Active > Passive analgesia:      p = 0.001 (n=15)
Active > Passive activation:     t = 2.59-3.99, p = 0.001-0.015
S1 connectivity reduction:       t = -4.64 to -3.53, p = 0.029-0.049
Evidence tier:                   β (Integrative) — single study, small n
```

---

## 4. R³ Input Mapping: What VRIAP Reads

### 4.1 R³ Feature Dependencies (36D of 49D)

| R³ Group | Index | Feature | VRIAP Role | Scientific Basis |
|----------|-------|---------|------------|------------------|
| **A: Consonance** | [0] | roughness | Pain-consonance inverse proxy | Dissonance = distress signal |
| **A: Consonance** | [3] | stumpf_fusion | Binding coherence | Tonal fusion = multi-modal coherence |
| **A: Consonance** | [4] | sensory_pleasantness | Positive valence for analgesia | Pleasant = pain-reducing context |
| **B: Energy** | [7] | amplitude | Engagement intensity | Energy = immersion level |
| **B: Energy** | [8] | spectral_centroid | Brightness proxy | Alert/active state |
| **B: Energy** | [10] | loudness | Arousal correlate | Loudness modulates engagement depth |
| **B: Energy** | [11] | onset_strength | Motor cueing | Transient events drive action |
| **C: Timbre** | [12] | warmth | Comfort signal | Low-frequency warmth = safety |
| **C: Timbre** | [14] | tonalness | Predictability proxy | Tonal = predictable = less threat |
| **D: Change** | [21] | spectral_flux | Event detection | Flux = change salience |
| **D: Change** | [22] | entropy | Unpredictability | High entropy = attention demand |
| **D: Change** | [23] | flatness | Spectral uniformity | Noise-like = non-musical distraction |
| **E: Interactions** | [25:33] | x_l0l5 (Energy x Consonance) | Motor-sensory binding | Energy-harmony coupling for groove |
| **E: Interactions** | [33:41] | x_l4l5 (Derivatives x Consonance) | Sensorimotor dynamics | Change-consonance = active engagement |
| **E: Interactions** | [41:49] | x_l5l7 (Consonance x Timbre) | Comfort-familiarity binding | Timbre warmth + consonance = safety signal |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[11] onset_strength ────────►   Motor cueing signal → active engagement
R³[10] loudness + R³[7] amp ──►   Engagement intensity → immersion depth
                                   Math: engagement = σ(0.4·onset + 0.3·loudness + 0.3·amp)

R³[4] pleasantness ───────────►   Positive valence → pain reduction context
R³[0] roughness (inverse) ────►   Consonance → safety/comfort signal
                                   Math: comfort ∝ pleasantness × (1-roughness)

R³[25:33] x_l0l5 ────────────►   Motor-sensory binding strength
                                   Energy × Consonance = groove-pain gating
                                   This IS the active engagement signal

R³[33:41] x_l4l5 ────────────►   Sensorimotor dynamics
                                   Change × Consonance = motor prediction quality
                                   Higher = better efference copy match

R³[41:49] x_l5l7 ────────────►   Comfort-familiarity context
                                   Timbre warmth × Consonance = safety
                                   Safe context enhances pain modulation

R³[22] entropy ────────────────►  Attention demand
                                   Low entropy = predictable = motor coupling easy
                                   High entropy = complex = attention diverted
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

VRIAP requires H³ features at three MEM horizons: H16 (1s), H20 (5s), H24 (36s).

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 11 | onset_strength | 16 | M0 (value) | L2 (bidirectional) | Current motor cueing |
| 11 | onset_strength | 20 | M1 (mean) | L0 (forward) | Sustained motor drive over 5s |
| 10 | loudness | 16 | M0 (value) | L2 (bidirectional) | Current engagement intensity |
| 10 | loudness | 20 | M1 (mean) | L0 (forward) | Average engagement over 5s |
| 10 | loudness | 24 | M3 (std) | L0 (forward) | Engagement variability over 36s |
| 7 | amplitude | 16 | M8 (velocity) | L0 (forward) | Energy change rate |
| 7 | amplitude | 20 | M4 (max) | L0 (forward) | Peak energy over 5s |
| 4 | sensory_pleasantness | 16 | M0 (value) | L2 (bidirectional) | Current comfort |
| 4 | sensory_pleasantness | 20 | M18 (trend) | L0 (forward) | Comfort trajectory |
| 0 | roughness | 16 | M0 (value) | L2 (bidirectional) | Current dissonance (pain proxy) |
| 0 | roughness | 20 | M18 (trend) | L0 (forward) | Dissonance trajectory |
| 22 | entropy | 16 | M0 (value) | L2 (bidirectional) | Current unpredictability |
| 22 | entropy | 20 | M1 (mean) | L0 (forward) | Average complexity over 5s |
| 22 | entropy | 24 | M19 (stability) | L0 (forward) | Pattern stability over 36s |
| 3 | stumpf_fusion | 16 | M1 (mean) | L2 (bidirectional) | Binding stability at 1s |
| 3 | stumpf_fusion | 20 | M1 (mean) | L0 (forward) | Binding over 5s integration |
| 21 | spectral_flux | 16 | M0 (value) | L2 (bidirectional) | Current event salience |
| 21 | spectral_flux | 20 | M1 (mean) | L0 (forward) | Sustained change rate |

**Total VRIAP H³ demand**: 18 tuples of 2304 theoretical = 0.78%

### 5.2 MEM Mechanism Binding

VRIAP reads from the **MEM** (Memory Encoding & Retrieval) mechanism:

| MEM Sub-section | Range | VRIAP Role | Weight |
|-----------------|-------|------------|--------|
| **Encoding State** | MEM[0:10] | Motor-pain gating, sensorimotor binding strength | **1.0** (primary) |
| **Familiarity Proxy** | MEM[10:20] | Auditory familiarity for distraction baseline | 0.5 |
| **Retrieval Dynamics** | MEM[20:30] | Pain modulation signal, analgesic consolidation | 0.8 |

No cross-unit mechanism reads. VRIAP operates entirely within the mnemonic circuit via MEM.

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
VRIAP OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
Manifold Range: IMU VRIAP [348:358]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EPISODIC ENGAGEMENT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0  │ f01_engagement    │ [0, 1] │ Active motor engagement level.
    │                   │        │ Premotor cortex + auditory-motor coupling.
    │                   │        │ f01 = σ(0.35·onset·x_l0l5.mean + 0.35·loudness·amp_vel
    │                   │        │        + 0.30·MEM.encoding.mean)
────┼───────────────────┼────────┼────────────────────────────────────────────
 1  │ f02_pain_gate     │ [0, 1] │ Pain gating signal (S1 connectivity reduction).
    │                   │        │ S1 + insula pain matrix modulation.
    │                   │        │ f02 = σ(0.40·engagement·MEM.retrieval.mean
    │                   │        │        + 0.30·pleasantness + 0.30·(1-roughness))
────┼───────────────────┼────────┼────────────────────────────────────────────
 2  │ f03_multimodal    │ [0, 1] │ Multi-modal binding strength.
    │                   │        │ Hippocampal binding of auditory+visual+motor.
    │                   │        │ f03 = σ(0.35·stumpf·x_l5l7.mean
    │                   │        │        + 0.35·MEM.encoding.mean
    │                   │        │        + 0.30·(1-entropy))

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 3  │ analgesia_index   │ [0, 1] │ Composite analgesia estimate.
    │                   │        │ f(engagement × pain_gate × multi_modal)
    │                   │        │ = engagement · pain_gate · multimodal_bind
────┼───────────────────┼────────┼────────────────────────────────────────────
 4  │ active_passive    │ [0, 1] │ Active-passive differential.
    │                   │        │ Motor contribution to analgesia.
    │                   │        │ = σ(0.50·engagement + 0.50·(engagement - familiarity))

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 5  │ motor_pain_state  │ [0, 1] │ Current motor-pain gating activation.
    │                   │        │ MEM.encoding × engagement.
────┼───────────────────┼────────┼────────────────────────────────────────────
 6  │ s1_connectivity   │ [0, 1] │ S1 connectivity proxy (inverse = good).
    │                   │        │ Higher = more pain gating (less S1).
    │                   │        │ pain_gate × MEM.retrieval.mean.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 7  │ analgesia_fc      │ [0, 1] │ Analgesia trajectory prediction (2-5s ahead).
    │                   │        │ Based on engagement and pain gating trends.
────┼───────────────────┼────────┼────────────────────────────────────────────
 8  │ engagement_fc     │ [0, 1] │ Motor engagement prediction (1-3s ahead).
    │                   │        │ Premotor activation trajectory.
────┼───────────────────┼────────┼────────────────────────────────────────────
 9  │ (reserved)        │ [0, 1] │ Future expansion.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Analgesia Index Function

```
Analgesia(music, VR) = Engagement × PainGate × MultiModalBind

where:
  Engagement     = σ(α₁·onset·x_l0l5.mean + α₂·loudness·amp_vel + α₃·MEM.encoding.mean)
  PainGate       = σ(β₁·engagement·MEM.retrieval.mean + β₂·pleasantness + β₃·(1-roughness))
  MultiModalBind = σ(γ₁·stumpf·x_l5l7.mean + γ₂·MEM.encoding.mean + γ₃·(1-entropy))

Constraints (|wᵢ| sum ≤ 1.0 per sigmoid):
  α₁ + α₂ + α₃ = 0.35 + 0.35 + 0.30 = 1.00  ✓
  β₁ + β₂ + β₃ = 0.40 + 0.30 + 0.30 = 1.00  ✓
  γ₁ + γ₂ + γ₃ = 0.35 + 0.35 + 0.30 = 1.00  ✓

Active-Passive differential:
  Active advantage = σ(0.50·Engagement + 0.50·(Engagement - Familiarity))
  When Engagement > Familiarity: active mode dominates (motor contribution)
  When Engagement ≈ Familiarity: passive-like (distraction only)

Temporal dynamics:
  dAnalgesia/dt = α · (Current_Engagement - Analgesia) + β · ∂PainGate/∂t
```

### 7.2 Feature Formulas

```python
# Helper values
onset = R³.onset_strength[11]            # [0, 1]
loudness = R³.loudness[10]               # [0, 1]
amplitude = R³.amplitude[7]              # [0, 1]
pleasantness = R³.sensory_pleasantness[4]  # [0, 1]
roughness = R³.roughness[0]              # [0, 1]
stumpf = R³.stumpf_fusion[3]             # [0, 1]
entropy = R³.entropy[22]                 # [0, 1]
x_l0l5_mean = mean(R³.x_l0l5[25:33])    # [0, 1]
x_l5l7_mean = mean(R³.x_l5l7[41:49])    # [0, 1]
amp_vel = H³(7, 16, M8, L0)             # amplitude velocity at 1s

mem_enc = mean(MEM.encoding[0:10])       # [0, 1]
mem_fam = mean(MEM.familiarity[10:20])   # [0, 1]
mem_ret = mean(MEM.retrieval[20:30])     # [0, 1]

# f01: Active Motor Engagement
f01 = σ(0.35 · onset · x_l0l5_mean + 0.35 · loudness · amp_vel + 0.30 · mem_enc)

# f02: Pain Gating Signal
f02 = σ(0.40 · f01 · mem_ret + 0.30 · pleasantness + 0.30 · (1 - roughness))

# f03: Multi-modal Binding
f03 = σ(0.35 · stumpf · x_l5l7_mean + 0.35 · mem_enc + 0.30 · (1 - entropy))
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Evidence Type | VRIAP Function |
|--------|-----------------|---------------|----------------|
| **S1 (Primary Somatosensory)** | ±42, -24, 54 | Direct (fMRI) | Pain signal propagation; connectivity reduced by active mode |
| **Insula (Anterior)** | ±36, 16, 2 | Inferred | Pain awareness, interoceptive salience gating |
| **mPFC** | 0, 52, 12 | Inferred | Pain appraisal, therapeutic context encoding |
| **Hippocampus** | ±20, -24, -12 | Inferred | Multi-modal binding, analgesic memory consolidation |
| **Premotor Cortex** | ±44, 0, 48 | Direct (fMRI) | Motor planning, efference copy generation |
| **Occipital Cortex** | ±18, -88, 4 | Direct (fMRI) | Visual-sensorimotor integration in VR |

---

## 9. Cross-Unit Pathways

### 9.1 VRIAP ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    VRIAP INTERACTIONS                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (IMU):                                                         │
│  VRIAP ──────► RIRI (RAS-Intelligent Rehabilitation Integration)           │
│       │        └── VRIAP pain gating informs rehabilitation motor recovery │
│       │                                                                      │
│       ├─────► HCMC (Hippocampal-Cortical Memory Circuit)                  │
│       │        └── VRIAP hippocampal binding feeds memory circuit          │
│       │                                                                      │
│       ├─────► MEAMN (Music-Evoked Autobiographical Memory)                │
│       │        └── Analgesic context encoded alongside music memory        │
│       │                                                                      │
│       └─────► CMAPCC (Cross-Modal Action-Perception Common Code)          │
│                └── Active engagement shares perception-action code         │
│                                                                             │
│  CROSS-UNIT (P3: IMU → ARU):                                              │
│  VRIAP.pain_gate ──────► ARU.AAC (autonomic response to pain relief)     │
│  VRIAP.engagement ─────► ARU.SRP (reward from active music engagement)    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Brain Pathway Cross-References

VRIAP reads from the unified Brain (26D) for shared state:

| Brain Dimension | Index (MI-space) | VRIAP Role |
|-----------------|-------------------|------------|
| arousal | [177] | Engagement intensity modulation |
| prediction_error | [178] | Motor prediction quality (efference copy mismatch) |
| emotional_momentum | [180] | Sustained comfort for analgesic context |

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Active > passive** | Active VR + music should produce greater analgesia than passive listening | Supported (p=0.001, n=15) |
| **S1 connectivity** | Active mode should reduce S1 pain-processing connectivity | Supported (t=-4.64 to -3.53) |
| **Motor requirement** | Removing motor component should eliminate active-passive difference | Testable — not yet directly tested |
| **Groove dependence** | Higher groove music should enhance active mode advantage | Testable — predicted by MEM.encoding × onset coupling |
| **Familiarity effect** | Familiar music should enhance passive mode (distraction) more than active mode | Testable — predicted by MEM.familiarity dissociation |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class VRIAP(BaseModel):
    """VR-Integrated Analgesia Paradigm.

    Output: 10D per frame.
    Reads: MEM mechanism (30D), R³ direct.
    Zero learned parameters — all deterministic.
    """
    NAME = "VRIAP"
    UNIT = "IMU"
    TIER = "β7"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("MEM",)        # Primary mechanism
    CROSS_UNIT = ()                    # No cross-unit reads

    ALPHA_1 = 0.35   # Onset × groove weight (engagement)
    ALPHA_2 = 0.35   # Loudness × velocity weight (engagement)
    ALPHA_3 = 0.30   # MEM encoding weight (engagement)
    BETA_1 = 0.40    # Engagement × retrieval weight (pain gate)
    BETA_2 = 0.30    # Pleasantness weight (pain gate)
    BETA_3 = 0.30    # Consonance weight (pain gate)
    GAMMA_1 = 0.35   # Stumpf × timbre-consonance weight (binding)
    GAMMA_2 = 0.35   # MEM encoding weight (binding)
    GAMMA_3 = 0.30   # Predictability weight (binding)

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """18 tuples for VRIAP computation."""
        return [
            # (r3_idx, horizon, morph, law)
            (11, 16, 0, 2),   # onset_strength, 1s, value, bidirectional
            (11, 20, 1, 0),   # onset_strength, 5s, mean, forward
            (10, 16, 0, 2),   # loudness, 1s, value, bidirectional
            (10, 20, 1, 0),   # loudness, 5s, mean, forward
            (10, 24, 3, 0),   # loudness, 36s, std, forward
            (7, 16, 8, 0),    # amplitude, 1s, velocity, forward
            (7, 20, 4, 0),    # amplitude, 5s, max, forward
            (4, 16, 0, 2),    # pleasantness, 1s, value, bidirectional
            (4, 20, 18, 0),   # pleasantness, 5s, trend, forward
            (0, 16, 0, 2),    # roughness, 1s, value, bidirectional
            (0, 20, 18, 0),   # roughness, 5s, trend, forward
            (22, 16, 0, 2),   # entropy, 1s, value, bidirectional
            (22, 20, 1, 0),   # entropy, 5s, mean, forward
            (22, 24, 19, 0),  # entropy, 36s, stability, forward
            (3, 16, 1, 2),    # stumpf_fusion, 1s, mean, bidirectional
            (3, 20, 1, 0),    # stumpf_fusion, 5s, mean, forward
            (21, 16, 0, 2),   # spectral_flux, 1s, value, bidirectional
            (21, 20, 1, 0),   # spectral_flux, 5s, mean, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute VRIAP 10D output.

        Args:
            mechanism_outputs: {"MEM": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) → (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) VRIAP output
        """
        mem = mechanism_outputs["MEM"]    # (B, T, 30)

        # R³ features
        roughness = r3[..., 0:1]          # [0, 1]
        stumpf = r3[..., 3:4]             # [0, 1]
        pleasantness = r3[..., 4:5]       # [0, 1]
        amplitude = r3[..., 7:8]          # [0, 1]
        loudness = r3[..., 10:11]         # [0, 1]
        onset = r3[..., 11:12]            # [0, 1]
        entropy = r3[..., 22:23]          # [0, 1]
        x_l0l5 = r3[..., 25:33]           # (B, T, 8)
        x_l5l7 = r3[..., 41:49]           # (B, T, 8)

        # MEM sub-sections
        mem_encoding = mem[..., 0:10]      # encoding state
        mem_familiar = mem[..., 10:20]     # familiarity proxy
        mem_retrieval = mem[..., 20:30]    # retrieval dynamics

        # H³ direct reads
        amp_vel = h3_direct[(7, 16, 8, 0)].unsqueeze(-1)  # amplitude velocity

        # ═══ LAYER E: Episodic Engagement ═══
        f01 = torch.sigmoid(
            self.ALPHA_1 * onset * x_l0l5.mean(-1, keepdim=True)
            + self.ALPHA_2 * loudness * amp_vel
            + self.ALPHA_3 * mem_encoding.mean(-1, keepdim=True)
        )
        f02 = torch.sigmoid(
            self.BETA_1 * f01 * mem_retrieval.mean(-1, keepdim=True)
            + self.BETA_2 * pleasantness
            + self.BETA_3 * (1.0 - roughness)
        )
        f03 = torch.sigmoid(
            self.GAMMA_1 * stumpf * x_l5l7.mean(-1, keepdim=True)
            + self.GAMMA_2 * mem_encoding.mean(-1, keepdim=True)
            + self.GAMMA_3 * (1.0 - entropy)
        )

        # ═══ LAYER M: Mathematical ═══
        analgesia_index = (f01 * f02 * f03).clamp(0, 1)
        familiarity = mem_familiar.mean(-1, keepdim=True)
        active_passive = torch.sigmoid(
            0.50 * f01 + 0.50 * (f01 - familiarity)
        )

        # ═══ LAYER P: Present ═══
        motor_pain_state = (
            mem_encoding.mean(-1, keepdim=True) * f01
        ).clamp(0, 1)
        s1_connectivity = (
            f02 * mem_retrieval.mean(-1, keepdim=True)
        ).clamp(0, 1)

        # ═══ LAYER F: Future ═══
        analgesia_fc = self._predict_future(
            mem_retrieval, h3_direct, window_h=20
        )
        engagement_fc = self._predict_future(
            mem_encoding, h3_direct, window_h=16
        )
        reserved = torch.zeros_like(f01)

        return torch.cat([
            f01, f02, f03,                           # E: 3D
            analgesia_index, active_passive,          # M: 2D
            motor_pain_state, s1_connectivity,        # P: 2D
            analgesia_fc, engagement_fc, reserved,    # F: 3D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 (primary) + supporting reviews | Single study with strong effects |
| **Effect Sizes** | Multiple t-values (2.59-3.99, -4.64 to -3.53) | fMRI + behavioral |
| **Sample Size** | n=15 | Small — hence β tier |
| **Evidence Modality** | fMRI, behavioral (pain ratings) | Direct neural + behavioral |
| **Falsification Tests** | 2/5 supported, 3/5 testable | Moderate validity |
| **R³ Features Used** | 36D of 49D | Comprehensive |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **MEM Mechanism** | 30D (3 sub-sections) | Full coverage |
| **Output Dimensions** | **10D** | 4-layer structure (E3 + M2 + P2 + F3) |

---

## 13. Scientific References

1. **VR analgesia RCT (2024)**. Active VR mode > passive listening for analgesia; S1 connectivity reduced in active mode. fMRI + behavioral, n=15, p=0.001 (active > passive), t=-4.64 to -3.53 (S1 connectivity).
2. **Melzack & Wall (1965)**. Gate control theory of pain. *Science*. Non-nociceptive input gates pain signal transmission at the spinal cord.
3. **Music distraction meta-analysis**. Music reduces pain perception through attentional and emotional mechanisms. Systematic review, moderate effects across conditions.
4. **Bushnell et al. (2013)**. Cognitive and emotional control of pain and its disruption in chronic pain. *Nature Reviews Neuroscience*. mPFC and insula modulate pain processing.
5. **Garza-Villarreal et al. (2014)**. Music reduces pain and increases functional mobility in fibromyalgia. *Frontiers in Psychology*. Music-induced analgesia in clinical populations.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Name | VR-Induced Analgesia Active-Passive | VR-Integrated Analgesia Paradigm |
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (GRV, EFC, BND) | MEM mechanism (30D) |
| Motor cueing | S⁰.X_L0L1 × HC⁰.EFC | R³.onset × R³.x_l0l5 × MEM.encoding |
| Pain reduction | S⁰.X_L1L5 × HC⁰.GRV | R³.pleasantness × (1-roughness) × MEM.retrieval |
| Multi-modal binding | S⁰.X_L4L5 × HC⁰.BND | R³.stumpf × R³.x_l5l7 × MEM.encoding |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 18/2304 = 0.78% | 18/2304 = 0.78% |
| Output dims | 11D | **10D** (consolidated) |

### Why MEM replaces HC⁰ mechanisms

The D0 pipeline used 3 separate HC⁰ mechanisms (GRV, EFC, BND). In MI, these are unified into the MEM mechanism with 3 sub-sections:
- **EFC → MEM.encoding_state** [0:10]: Efference copy / motor-pain binding → encoding strength
- **BND → MEM.encoding_state** [0:10]: Temporal binding for multi-modal integration → encoding
- **GRV → MEM.retrieval_dynamics** [20:30]: Groove-driven pain gating → retrieval modulation

The consolidation is natural: groove processing (GRV), efference copy (EFC), and temporal binding (BND) all serve the core function of encoding and retrieving pain-modulated states. MEM unifies this under a single memory mechanism.

---

**Model Status**: ⚠️ **REQUIRES VALIDATION**
**Output Dimensions**: **10D**
**Manifold Range**: **IMU VRIAP [348:358]**
**Evidence Tier**: **β (Integrative) — 70-90% confidence**
