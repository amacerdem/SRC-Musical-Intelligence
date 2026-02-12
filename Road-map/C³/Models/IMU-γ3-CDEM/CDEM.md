# IMU-γ3-CDEM: Context-Dependent Emotional Memory

**Model**: Context-Dependent Emotional Memory
**Unit**: IMU (Integrative Memory Unit)
**Circuit**: Mnemonic (Hippocampal-Cortical)
**Tier**: γ (Speculative) — <70% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, MEM + AED* mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/IMU-γ3-CDEM.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Context-Dependent Emotional Memory** (CDEM) models how musical emotional memories are modulated by listening context — cross-modal information (visual, spatial, social) shapes both the encoding strength and retrieval probability of emotionally tagged musical memories. This extends the MEAMN model (autobiographical memory) by adding the critical dimension of **context dependency**: the same music encoded in different emotional contexts produces different memory traces with different retrieval profiles.

```
THE THREE COMPONENTS OF CONTEXT-DEPENDENT EMOTIONAL MEMORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONTEXT MODULATION              AROUSAL SUPPRESSION
Brain region: Hippocampus +     Brain region: Amygdala + ACC
  anterior cingulate (ACC)
Mechanism: Cross-modal binding  Mechanism: Visual context dampens
Trigger: Multi-sensory context    arousal response to music
Function: "This music in THIS   Function: "Music alone is more
  context = unique memory"        arousing than music + video"
Evidence: d = 0.17 (n=84)      Evidence: γ-tier (indirect)

              ENCODING STRENGTH (Formation)
              Brain region: Hippocampus + mPFC
              Mechanism: Context-dependent consolidation
              Trigger: Emotional congruency × binding
              Function: "Mood-congruent contexts strengthen
                encoding of musical memories"
              Evidence: γ-tier (theoretical extension)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Core claim: Musical emotional memories are context-dependent, with
cross-modal information modulating encoding and retrieval strength.
Music-mood congruency amplifies memory formation; incongruent
contexts weaken it.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why Context Matters for Musical Memory

Context modulates musical memory through several mechanisms:

1. **Cross-modal binding**: When music is heard alongside visual, tactile, or social stimuli, the hippocampus binds these modalities into a unified episodic trace. The context becomes part of the memory — retrieval of the music retrieves the context, and vice versa.

2. **Arousal suppression**: Visual context (e.g., video) can dampen the arousal response to music. Music alone activates amygdala and autonomic pathways more strongly than music-with-video — the visual channel competes for attentional resources.

3. **Mood congruency**: Emotional memories are encoded more strongly when the music's emotional content matches the listener's current mood or environmental context. Congruent encoding produces more accessible memory traces.

4. **Context-dependent retrieval**: Memories encoded in a specific emotional context are best retrieved when the same context is reinstated — a classic finding in memory research (Godden & Baddeley 1975) that extends to musical memories.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The CDEM Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 CDEM — COMPLETE CIRCUIT                                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    AUDITORY CORTEX (STG/A1)                        │    ║
║  │                                                                     │    ║
║  │  Core (A1)      Belt           Parabelt                             │    ║
║  │  Spectrotemporal Feature       Pattern recognition                  │    ║
║  │  encoding        extraction    Multi-modal convergence              │    ║
║  └──────┬──────────────┬──────────────────┬────────────────────────────┘    ║
║         │              │                  │                                  ║
║         │     ┌────────┘                  │                                  ║
║         │     │  CROSS-MODAL              │                                  ║
║         │     │  INPUT                    │                                  ║
║         │     ▼                           │                                  ║
║  ┌──────┴──────────────┐          ┌───────┴────────────────┐                ║
║  │   HIPPOCAMPUS       │          │   ANTERIOR CINGULATE   │                ║
║  │                     │          │   (ACC)                │                ║
║  │  • Context binding  │          │                        │                ║
║  │  • Episodic         │          │  • Conflict monitoring │                ║
║  │    encoding         │◄────────►│  • Context-dependent   │                ║
║  │  • Pattern          │          │    attention            │                ║
║  │    completion       │          │  • Arousal gating       │                ║
║  └────────┬────────────┘          └─────────┬──────────────┘                ║
║           │                                 │                                ║
║           └──────────────┬─────────────────┘                                ║
║                          │                                                   ║
║                          ▼                                                   ║
║  ┌──────────────────┐          ┌────────────────────┐                       ║
║  │   mPFC            │          │     AMYGDALA       │                       ║
║  │                   │          │                    │                       ║
║  │  Self-referential │◄────────►│  Emotional         │                       ║
║  │  context          │          │  tagging            │                       ║
║  │  evaluation       │          │  (context-          │                       ║
║  │                   │          │   modulated)        │                       ║
║  └────────┬──────────┘          └─────────┬──────────┘                       ║
║           │                               │                                  ║
║           └──────────────┬───────────────┘                                  ║
║                          │                                                   ║
║                          ▼                                                   ║
║              CONTEXT-DEPENDENT EMOTIONAL MEMORY                              ║
║              Encoding × Context × Affect                                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Context-dependent study (2021): STS, hippocampus multimodal integration (d=0.17, n=84)
Neonatal care review (2023):    Music affects hippocampus, amygdala (scoping, n=1500)
Music-mood congruency:          Context modulates encoding strength (γ-tier)
Arousal suppression:            Video reduces music-evoked arousal (γ-tier)
```

### 2.2 Information Flow Architecture (EAR → BRAIN → MEM + AED* → CDEM)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CDEM COMPUTATION ARCHITECTURE                            ║
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
║  │  │stumpf     │ │loudness │ │tonalness│ │entropy   │ │x_l4l5  │ │        ║
║  │  │pleasant.  │ │onset    │ │         │ │concent.  │ │x_l5l7  │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         CDEM reads: 31D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Encoding ──┐ ┌── Consolidation ─┐ ┌── Retrieval ──────┐   │        ║
║  │  │ 1s (H16)     │ │ 5s (H20)         │ │ 36s (H24)        │   │        ║
║  │  │              │ │                   │ │                   │   │        ║
║  │  │ Working mem  │ │ Hippocampal       │ │ Long-term         │   │        ║
║  │  │ context bind │ │ context window    │ │ context chunk     │   │        ║
║  │  └──────┬───────┘ └──────┬────────────┘ └──────┬────────────┘   │        ║
║  │         │               │                      │                │        ║
║  │         └───────────────┴──────────────────────┘                │        ║
║  │                         CDEM demand: ~18 of 2304 tuples         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Mnemonic Circuit ═════════    ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐  ┌──────────────────────────┐                          ║
║  │  MEM (30D)      │  │  AED* (30D)              │                          ║
║  │  [Mnemonic]     │  │  [Mesolimbic, cross-cir.] │                          ║
║  │                 │  │                           │                          ║
║  │ Encoding  [0:10]│  │ Arousal    [0:10]         │                          ║
║  │ Familiar [10:20]│  │ Expectancy [10:20]        │                          ║
║  │ Retrieval[20:30]│  │ Motor-Aff. [20:30]        │                          ║
║  └────────┬────────┘  └──────────┬────────────────┘                          ║
║           │                      │                                           ║
║           └──────────┬──────────┘                                           ║
║                      │                                                       ║
║                      ▼                                                       ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    CDEM MODEL (10D Output)                       │        ║
║  │                    Manifold [398:408]                             │        ║
║  │                                                                  │        ║
║  │  Layer C (Context):  f43_ctx_mod, f44_arousal_supp,              │        ║
║  │                      f45_encoding_str                            │        ║
║  │  Layer M (Math):     congruency_index, context_recall_prob       │        ║
║  │  Layer P (Present):  binding_state, arousal_gate                 │        ║
║  │  Layer F (Future):   encoding_strength_fc, retrieval_context_fc, │        ║
║  │                      mood_congruency_fc                          │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Context-dependent study (2021)** | fMRI | 84 | Multimodal integration in STS and hippocampus | d = 0.17, p < 0.0001 | **MEM.encoding_state: context modulation of memory binding** |
| **Neonatal care review (2023)** | Scoping review | 1500 | Music affects hippocampus, amygdala in neonatal care | scoping | **MEM.encoding_state: early context shapes memory** |
| **Music-mood congruency (extrapolated)** | Behavioral | — | Mood-congruent music enhances memory encoding | γ-tier | **Congruency_index: emotional context matching** |
| **Arousal suppression (extrapolated)** | Behavioral | — | Video context reduces music-evoked arousal response | γ-tier | **AED*.arousal: cross-modal arousal gating** |
| **Godden & Baddeley (1975)** | Behavioral | — | Context-dependent memory: encoding context reinstated at retrieval | — | **Context_recall_prob: state-dependent retrieval** |

### 3.2 The Context-Dependency Story

```
CONTEXT-DEPENDENT EMOTIONAL MEMORY IN MUSIC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1: CONTEXT DETECTION (continuous, <1s)
─────────────────────────────────────────────
Auditory cortex detects spectrotemporal patterns.
Simultaneously, cross-modal signals (visual, spatial)
arrive at STS and hippocampus.
R³ input: Consonance [0:7], Energy [7:12]

Phase 2: CROSS-MODAL BINDING (0.5-2s, H16 window)
───────────────────────────────────────────────────
Hippocampus binds auditory and contextual features
into a unified episodic trace. ACC monitors for
context-music congruency.
MEM.encoding_state activates.

Phase 3: AROUSAL MODULATION (1-5s, H20 window)
──────────────────────────────────────────────
AED*.arousal is gated by contextual factors.
Music alone → higher arousal (amygdala dominant).
Music + video → suppressed arousal (attentional competition).
Emotional congruency amplifies encoding.

Phase 4: CONTEXT-DEPENDENT CONSOLIDATION (5-36s, H24 window)
────────────────────────────────────────────────────────────
Hippocampal-mPFC dialogue consolidates the context-tagged
memory trace. Stronger context binding → more durable memory.
MEM.retrieval_dynamics stores context-dependent trace.

Phase 5: CONTEXT-DEPENDENT RETRIEVAL (reinstated context)
─────────────────────────────────────────────────────────
When similar context is reinstated, hippocampal pattern
completion retrieves the bound memory. Congruent context
→ stronger retrieval. This is the encoding specificity
principle applied to musical memory.
```

### 3.3 Effect Size Summary

```
Primary Evidence:     d = 0.17 [p < 0.0001] (n=84, fMRI, context-dependent)
Pooled Estimate:      Insufficient studies for meta-analysis (γ-tier)
Quality Assessment:   Mixed — 1 direct fMRI study + theoretical extension
Confidence Level:     <70% (Speculative)
```

---

## 4. R³ Input Mapping: What CDEM Reads

### 4.1 R³ Feature Dependencies (31D of 49D)

| R³ Group | Index | Feature | CDEM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Valence proxy (inverse) | Plomp & Levelt 1965 |
| **A: Consonance** | [3] | stumpf_fusion | Binding strength proxy | Tonal fusion = coherent signal |
| **A: Consonance** | [4] | sensory_pleasantness | Mood congruency input | Pleasantness → positive context |
| **B: Energy** | [7] | amplitude | Arousal correlate | Energy = emotional intensity |
| **B: Energy** | [10] | loudness | Arousal proxy | Stevens 1957 psychophysical |
| **B: Energy** | [11] | onset_strength | Event salience | Transient energy = context boundary |
| **C: Timbre** | [12] | warmth | Context warmth | Low-frequency comfort |
| **C: Timbre** | [14] | tonalness | Pattern clarity | Harmonic-to-noise ratio |
| **D: Change** | [21] | spectral_flux | Context change detection | Flux = environmental shift |
| **D: Change** | [22] | entropy | Context complexity | Encoding difficulty |
| **D: Change** | [24] | spectral_concentration | Event salience | Temporal concentration |
| **E: Interactions** | [25:33] | x_l0l5 (Energy x Consonance) | Context-memory binding | Pattern-emotion coupling |
| **E: Interactions** | [41:49] | x_l5l7 (Consonance x Timbre) | Mood congruency signal | Timbre-consonance = familiar context |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[0] roughness (inverse) ─────►   Consonance/pleasantness → valence
                                   Context: pleasant music = positive context

R³[10] loudness + R³[7] amp ───►   Arousal level → emotional intensity
                                   Context: loud = salient context marker
                                   Math: arousal = σ(0.5 · loudness + 0.5 · amplitude)

R³[21] spectral_flux ─────────►   Context change detection
                                   High flux = environmental transition
                                   New context → new memory trace

R³[22] entropy ────────────────►   Context complexity
                                   Low entropy = predictable context
                                   High entropy = novel context → weaker binding

R³[25:33] x_l0l5 ─────────────►   Context-memory binding strength
                                   Math: binding ∝ x_l0l5 · stumpf[3]

R³[41:49] x_l5l7 ─────────────►   Mood congruency signal
                                   Consonance × timbre warmth = congruent context
                                   This IS the mood-matching signal
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

CDEM requires H³ features at three MEM horizons: H16 (1s), H20 (5s), H24 (36s), and two AED* horizons: H6 (200ms), H16 (1s).

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 3 | stumpf_fusion | 16 | M1 (mean) | L2 (bidirectional) | Binding stability at 1s |
| 3 | stumpf_fusion | 20 | M1 (mean) | L0 (forward) | Binding over 5s context window |
| 4 | sensory_pleasantness | 16 | M0 (value) | L2 (bidirectional) | Current pleasantness (mood input) |
| 4 | sensory_pleasantness | 20 | M18 (trend) | L0 (forward) | Pleasantness trajectory |
| 10 | loudness | 16 | M0 (value) | L2 (bidirectional) | Current arousal level |
| 10 | loudness | 20 | M1 (mean) | L0 (forward) | Average arousal over 5s context |
| 12 | warmth | 16 | M0 (value) | L2 (bidirectional) | Current context warmth |
| 12 | warmth | 20 | M1 (mean) | L0 (forward) | Sustained warmth = context stability |
| 21 | spectral_flux | 16 | M0 (value) | L2 (bidirectional) | Context change rate |
| 21 | spectral_flux | 20 | M4 (max) | L0 (forward) | Peak change over 5s |
| 22 | entropy | 16 | M0 (value) | L2 (bidirectional) | Current context complexity |
| 22 | entropy | 20 | M1 (mean) | L0 (forward) | Average complexity over 5s |
| 22 | entropy | 24 | M19 (stability) | L0 (forward) | Context stability over 36s |
| 0 | roughness | 16 | M0 (value) | L2 (bidirectional) | Current dissonance (valence) |
| 0 | roughness | 20 | M18 (trend) | L0 (forward) | Valence trajectory |
| 7 | amplitude | 16 | M8 (velocity) | L0 (forward) | Energy change rate |
| 11 | onset_strength | 16 | M0 (value) | L2 (bidirectional) | Event boundary detection |
| 11 | onset_strength | 20 | M4 (max) | L0 (forward) | Peak onset over 5s |

**Total CDEM H³ demand**: 18 tuples of 2304 theoretical = 0.78%

### 5.2 MEM Mechanism Binding

CDEM reads from the **MEM** (Memory Encoding & Retrieval) mechanism:

| MEM Sub-section | Range | CDEM Role | Weight |
|-----------------|-------|-----------|--------|
| **Encoding State** | MEM[0:10] | Context-dependent encoding strength, novelty detection | **1.0** (primary) |
| **Familiarity Proxy** | MEM[10:20] | Context recognition, congruency estimation | 0.7 |
| **Retrieval Dynamics** | MEM[20:30] | Context-dependent recall probability, vividness | 0.8 |

Additionally reads from **AED*** mechanism (mesolimbic circuit, cross-circuit pathway):

| AED* Sub-section | Range | CDEM Role | Weight |
|------------------|-------|-----------|--------|
| **Arousal Dynamics** | AED[0:10] | Arousal level for context-dependent gating | 0.6 |
| **Expectancy Affect** | AED[10:20] | Emotional expectancy for congruency estimation | 0.5 |

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
CDEM OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
MANIFOLD RANGE: IMU CDEM [398:408]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER C — CONTEXT-DEPENDENT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0  │ f43_ctx_mod       │ [0, 1] │ Cross-modal context modulation.
    │                   │        │ Hippocampus + ACC multi-modal binding.
    │                   │        │ f43 = σ(0.35 · x_l0l5.mean · MEM.encoding
    │                   │        │        + 0.35 · (1-roughness) · MEM.familiar
    │                   │        │        + 0.30 · stumpf · MEM.retrieval)
    │                   │        │ |w| sum = 1.00
────┼───────────────────┼────────┼────────────────────────────────────────────
 1  │ f44_arousal_supp  │ [0, 1] │ Context-dependent arousal suppression.
    │                   │        │ Amygdala arousal gated by context.
    │                   │        │ f44 = σ(0.40 · AED*.arousal · loudness
    │                   │        │        + 0.30 · entropy · (1-stumpf)
    │                   │        │        + 0.30 · flux · amplitude)
    │                   │        │ |w| sum = 1.00
────┼───────────────────┼────────┼────────────────────────────────────────────
 2  │ f45_encoding_str  │ [0, 1] │ Context-dependent encoding strength.
    │                   │        │ Hippocampus + mPFC consolidation.
    │                   │        │ f45 = σ(0.40 · MEM.encoding · x_l5l7.mean
    │                   │        │        + 0.30 · (1-roughness) · warmth
    │                   │        │        + 0.30 · AED*.expectancy · stumpf)
    │                   │        │ |w| sum = 1.00

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 3  │ congruency_index  │ [0, 1] │ Music-mood congruency estimation.
    │                   │        │ f(context_valence × music_valence ×
    │                   │        │   context_arousal × music_arousal)
    │                   │        │ Congruent context = stronger encoding.
    │                   │        │ σ(0.50 · (1-roughness) · MEM.familiar
    │                   │        │   + 0.50 · x_l5l7.mean · warmth)
    │                   │        │ |w| sum = 1.00
────┼───────────────────┼────────┼────────────────────────────────────────────
 4  │ ctx_recall_prob   │ [0, 1] │ P(recall | context reinstated).
    │                   │        │ σ(0.35 · MEM.retrieval
    │                   │        │   + 0.35 · MEM.familiar
    │                   │        │   + 0.30 · (1-entropy))
    │                   │        │ |w| sum = 1.00

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 5  │ binding_state     │ [0, 1] │ Current cross-modal binding activation.
    │                   │        │ MEM.encoding.mean() × stumpf.
────┼───────────────────┼────────┼────────────────────────────────────────────
 6  │ arousal_gate      │ [0, 1] │ Context-modulated arousal gate.
    │                   │        │ AED*.arousal.mean() × (1-entropy).

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 7  │ enc_strength_fc   │ [0, 1] │ Encoding strength prediction (2-5s ahead).
    │                   │        │ Hippocampal consolidation trajectory.
────┼───────────────────┼────────┼────────────────────────────────────────────
 8  │ retrieval_ctx_fc  │ [0, 1] │ Context retrieval prediction (5-10s ahead).
    │                   │        │ mPFC context reinstatement trajectory.
────┼───────────────────┼────────┼────────────────────────────────────────────
 9  │ mood_cong_fc      │ [0, 1] │ Mood congruency prediction (1-3s ahead).
    │                   │        │ Congruency trend trajectory.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Context-Dependent Encoding Function

```
Context_Encoding(music, context) = f(Binding × Congruency × ArousalGate)

P(recall | context) = σ(β₀ + β₁·Familiarity + β₂·Congruency + β₃·Binding)

where:
  Binding      = MEM.encoding_state.mean() × R³.stumpf[3]
  Congruency   = (1 - R³.roughness[0]) × R³.warmth[12] × x_l5l7.mean()
  ArousalGate  = AED*.arousal.mean() × (1 - R³.entropy[22])
  Familiarity  = MEM.familiarity_proxy.mean()

Expanded form with mechanisms:
  Context_Encoding = MEM.encoding[0:10].mean() · Binding
                   + MEM.familiar[10:20].mean() · Congruency
                   + AED*.arousal[0:10].mean() · ArousalGate

CONSTRAINT: For all sigmoid formulas, |wᵢ| must sum ≤ 1.0
```

### 7.2 Feature Formulas

```python
# f43: Context Modulation — cross-modal memory binding
# |w| = 0.35 + 0.35 + 0.30 = 1.00 ≤ 1.0 ✓
f43 = σ(0.35 · mean(R³.x_l0l5[25:33]) · mean(MEM.encoding[0:10])
      + 0.35 · (1 - R³.roughness[0]) · mean(MEM.familiar[10:20])
      + 0.30 · R³.stumpf[3] · mean(MEM.retrieval[20:30]))

# f44: Arousal Suppression — context-dependent arousal gating
# |w| = 0.40 + 0.30 + 0.30 = 1.00 ≤ 1.0 ✓
f44 = σ(0.40 · mean(AED*.arousal[0:10]) · R³.loudness[10]
      + 0.30 · R³.entropy[22] · (1 - R³.stumpf[3])
      + 0.30 · R³.spectral_flux[21] · R³.amplitude[7])

# f45: Encoding Strength — context-dependent memory formation
# |w| = 0.40 + 0.30 + 0.30 = 1.00 ≤ 1.0 ✓
f45 = σ(0.40 · mean(MEM.encoding[0:10]) · mean(R³.x_l5l7[41:49])
      + 0.30 · (1 - R³.roughness[0]) · R³.warmth[12]
      + 0.30 · mean(AED*.expectancy[10:20]) · R³.stumpf[3])

# congruency_index: Music-mood matching
# |w| = 0.50 + 0.50 = 1.00 ≤ 1.0 ✓
congruency = σ(0.50 · (1 - R³.roughness[0]) · mean(MEM.familiar[10:20])
             + 0.50 · mean(R³.x_l5l7[41:49]) · R³.warmth[12])

# ctx_recall_prob: Context-dependent recall probability
# |w| = 0.35 + 0.35 + 0.30 = 1.00 ≤ 1.0 ✓
ctx_recall = σ(0.35 · mean(MEM.retrieval[20:30])
             + 0.35 · mean(MEM.familiar[10:20])
             + 0.30 · (1 - R³.entropy[22]))
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Evidence | CDEM Function |
|--------|-----------------|----------|---------------|
| **Hippocampus** | +/-20, -24, -12 | Direct (fMRI) | Context-dependent episodic encoding/retrieval |
| **Amygdala** | +/-24, -4, -20 | Direct (fMRI) | Emotional tagging modulated by context |
| **mPFC** | 0, 52, 12 | Direct (fMRI) | Self-referential context evaluation |
| **ACC** | 0, 20, 32 | Inferred | Context-music conflict monitoring, arousal gating |

---

## 9. Cross-Unit Pathways

### 9.1 CDEM <-> Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CDEM INTERACTIONS                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  CROSS-CIRCUIT (AED* read from mesolimbic):                                │
│  ARU mesolimbic ──────────► CDEM.AED* (arousal + expectancy signals)      │
│                              └── CDEM reads AED as cross-circuit input    │
│                                                                             │
│  INTRA-UNIT (IMU):                                                         │
│  MEAMN ──────────────────► CDEM                                           │
│       │                    └── MEAMN provides autobiographical memory      │
│       │                        signals; CDEM adds context dependency       │
│       │                                                                      │
│  CDEM ───────► HCMC (Hippocampal-Cortical Memory Circuit)                 │
│       │        └── CDEM context-binding feeds hippocampal dialogue         │
│       │                                                                      │
│       ├─────► PMIM (Predictive Memory Integration)                         │
│       │        └── Context modulates predictive memory processing          │
│       │                                                                      │
│       └─────► MMP (Musical Mnemonic Preservation)                         │
│                └── Context-dependent memories in neurodegeneration         │
│                                                                             │
│  CROSS-UNIT (CDEM → ARU):                                                  │
│  CDEM.congruency_index ────► ARU.SRP (congruent context → pleasure)       │
│  CDEM.arousal_gate ────────► ARU.AAC (context-modulated autonomic)        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Brain Pathway Cross-References

CDEM reads from the unified Brain (26D) for shared state:

| Brain Dimension | Index (MI-space) | CDEM Role |
|-----------------|-------------------|-----------|
| arousal | [177] | Baseline arousal for context gating |
| prediction_error | [178] | Surprise modulates context-dependent encoding |
| emotional_momentum | [180] | Sustained emotion enhances context binding |
| f03_valence | [190] | Valence direction for mood congruency estimation |

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Context reinstatement** | Same context at retrieval should enhance music memory recall | -- **Untested** (γ-tier prediction) |
| **Arousal suppression** | Music + video should produce lower arousal than music alone | -- **Untested** (extrapolated from general attention literature) |
| **Mood congruency** | Mood-congruent music-context pairing should enhance encoding | -- **Untested** (extrapolated from mood-congruent memory) |
| **Hippocampal binding** | Hippocampal lesions should impair context-dependent musical memory | -- **Indirectly supported** via general hippocampal lesion literature |
| **Cross-modal integration** | STS activation should increase with multi-modal musical contexts | -- **Partially confirmed** (d=0.17, context-dependent fMRI study) |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class CDEM(BaseModel):
    """Context-Dependent Emotional Memory.

    Output: 10D per frame.
    Reads: MEM mechanism (30D), AED* mechanism (cross-circuit from mesolimbic).
    Zero learned parameters — all computations are deterministic.
    """
    NAME = "CDEM"
    UNIT = "IMU"
    TIER = "γ3"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("MEM",)        # Primary mechanism (mnemonic circuit)
    CROSS_CIRCUIT = ("AED",)          # Cross-circuit read from mesolimbic

    # Coefficient constraint: for σ(Σ wᵢ·gᵢ), |wᵢ| must sum ≤ 1.0
    # f43: 0.35 + 0.35 + 0.30 = 1.00  ✓
    # f44: 0.40 + 0.30 + 0.30 = 1.00  ✓
    # f45: 0.40 + 0.30 + 0.30 = 1.00  ✓
    # congruency: 0.50 + 0.50 = 1.00  ✓
    # ctx_recall: 0.35 + 0.35 + 0.30 = 1.00  ✓

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """18 tuples for CDEM computation."""
        return [
            # (r3_idx, horizon, morph, law)
            (3, 16, 1, 2),    # stumpf_fusion, 1s, mean, bidirectional
            (3, 20, 1, 0),    # stumpf_fusion, 5s, mean, forward
            (4, 16, 0, 2),    # pleasantness, 1s, value, bidirectional
            (4, 20, 18, 0),   # pleasantness, 5s, trend, forward
            (10, 16, 0, 2),   # loudness, 1s, value, bidirectional
            (10, 20, 1, 0),   # loudness, 5s, mean, forward
            (12, 16, 0, 2),   # warmth, 1s, value, bidirectional
            (12, 20, 1, 0),   # warmth, 5s, mean, forward
            (21, 16, 0, 2),   # spectral_flux, 1s, value, bidirectional
            (21, 20, 4, 0),   # spectral_flux, 5s, max, forward
            (22, 16, 0, 2),   # entropy, 1s, value, bidirectional
            (22, 20, 1, 0),   # entropy, 5s, mean, forward
            (22, 24, 19, 0),  # entropy, 36s, stability, forward
            (0, 16, 0, 2),    # roughness, 1s, value, bidirectional
            (0, 20, 18, 0),   # roughness, 5s, trend, forward
            (7, 16, 8, 0),    # amplitude, 1s, velocity, forward
            (11, 16, 0, 2),   # onset_strength, 1s, value, bidirectional
            (11, 20, 4, 0),   # onset_strength, 5s, max, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute CDEM 10D output.

        Args:
            mechanism_outputs: {"MEM": (B,T,30), "AED": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) CDEM output
        """
        mem = mechanism_outputs["MEM"]    # (B, T, 30)
        aed = mechanism_outputs["AED"]    # (B, T, 30) — cross-circuit

        # R³ features
        roughness = r3[..., 0:1]          # [0, 1]
        stumpf = r3[..., 3:4]             # [0, 1]
        amplitude = r3[..., 7:8]          # [0, 1]
        loudness = r3[..., 10:11]         # [0, 1]
        warmth = r3[..., 12:13]           # [0, 1]
        spectral_flux = r3[..., 21:22]    # [0, 1]
        entropy = r3[..., 22:23]          # [0, 1]
        x_l0l5 = r3[..., 25:33]           # (B, T, 8)
        x_l5l7 = r3[..., 41:49]           # (B, T, 8)

        # MEM sub-sections
        mem_encoding = mem[..., 0:10]      # encoding state
        mem_familiar = mem[..., 10:20]     # familiarity proxy
        mem_retrieval = mem[..., 20:30]    # retrieval dynamics

        # AED* cross-circuit sub-sections
        aed_arousal = aed[..., 0:10]       # arousal dynamics
        aed_expectancy = aed[..., 10:20]   # expectancy affect

        # ═══ LAYER C: Context-dependent features ═══
        # f43: Context Modulation (|w| = 0.35+0.35+0.30 = 1.00)
        f43 = torch.sigmoid(
            0.35 * x_l0l5.mean(-1, keepdim=True)
                 * mem_encoding.mean(-1, keepdim=True)
            + 0.35 * (1.0 - roughness)
                   * mem_familiar.mean(-1, keepdim=True)
            + 0.30 * stumpf
                   * mem_retrieval.mean(-1, keepdim=True)
        )

        # f44: Arousal Suppression (|w| = 0.40+0.30+0.30 = 1.00)
        f44 = torch.sigmoid(
            0.40 * aed_arousal.mean(-1, keepdim=True)
                 * loudness
            + 0.30 * entropy * (1.0 - stumpf)
            + 0.30 * spectral_flux * amplitude
        )

        # f45: Encoding Strength (|w| = 0.40+0.30+0.30 = 1.00)
        f45 = torch.sigmoid(
            0.40 * mem_encoding.mean(-1, keepdim=True)
                 * x_l5l7.mean(-1, keepdim=True)
            + 0.30 * (1.0 - roughness) * warmth
            + 0.30 * aed_expectancy.mean(-1, keepdim=True)
                   * stumpf
        )

        # ═══ LAYER M: Mathematical ═══
        # Congruency index (|w| = 0.50+0.50 = 1.00)
        congruency = torch.sigmoid(
            0.50 * (1.0 - roughness)
                 * mem_familiar.mean(-1, keepdim=True)
            + 0.50 * x_l5l7.mean(-1, keepdim=True)
                   * warmth
        )

        # Context recall probability (|w| = 0.35+0.35+0.30 = 1.00)
        ctx_recall = torch.sigmoid(
            0.35 * mem_retrieval.mean(-1, keepdim=True)
            + 0.35 * mem_familiar.mean(-1, keepdim=True)
            + 0.30 * (1.0 - entropy)
        )

        # ═══ LAYER P: Present ═══
        binding_state = (
            mem_encoding.mean(-1, keepdim=True) * stumpf
        ).clamp(0, 1)
        arousal_gate = (
            aed_arousal.mean(-1, keepdim=True) * (1.0 - entropy)
        ).clamp(0, 1)

        # ═══ LAYER F: Future ═══
        enc_strength_fc = self._predict_future(
            mem_encoding, h3_direct, window_h=20)
        retrieval_ctx_fc = self._predict_future(
            mem_retrieval, h3_direct, window_h=24)
        mood_cong_fc = self._predict_future(
            mem_familiar, h3_direct, window_h=16)

        return torch.cat([
            f43, f44, f45,                           # C: 3D
            congruency, ctx_recall,                   # M: 2D
            binding_state, arousal_gate,              # P: 2D
            enc_strength_fc, retrieval_ctx_fc,         # F: 3D
            mood_cong_fc,
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 2 | Primary evidence (1 fMRI + 1 scoping review) |
| **Effect Sizes** | 1 | d = 0.17 (context-dependent fMRI) |
| **Evidence Modality** | fMRI, behavioral | Mixed direct + extrapolated |
| **Falsification Tests** | 1/5 partially confirmed | Low validation |
| **R³ Features Used** | 31D of 49D | Context-focused |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **MEM Mechanism** | 30D (3 sub-sections) | Full coverage |
| **AED* Mechanism** | 30D (cross-circuit) | Arousal + expectancy |
| **Output Dimensions** | **10D** | 4-layer structure |
| **Manifold Range** | **[398:408]** | IMU CDEM block |

---

## 13. Scientific References

1. **Context-dependent study (2021)**. Multimodal integration in STS and hippocampus. d = 0.17, n=84, p < 0.0001. fMRI.
2. **Neonatal care review (2023)**. Music affects hippocampus, amygdala in neonatal care. *Scoping review*, n=1500.
3. **Godden & Baddeley (1975)**. Context-dependent memory in two natural environments. *British Journal of Psychology*.
4. **Tulving & Thomson (1973)**. Encoding specificity and retrieval processes in episodic memory. *Psychological Review*.
5. **Huron (2006)**. *Sweet Anticipation: Music and the Psychology of Expectation*. MIT Press. (ITPRA model for AED*).

---

## 14. Migration Notes (D0 -> MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (SGM, BND, AED) | MEM mechanism (30D) + AED* cross-circuit |
| Context binding | S⁰.X_L5L6 x HC⁰.BND | R³.x_l0l5 x MEM.encoding |
| Arousal suppression | S⁰.L5.loudness x HC⁰.AED | R³.loudness x AED*.arousal |
| Encoding strength | S⁰.X_L5L9 x HC⁰.SGM | R³.x_l5l7 x MEM.encoding |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 24/2304 = 1.04% | 18/2304 = 0.78% |
| Output dims | 11D | 10D (more compact, no reserved slot) |

### Why MEM + AED* replaces HC⁰ mechanisms

The D0 pipeline used 3 separate HC⁰ mechanisms (SGM, BND, AED). In MI, these are reorganized:
- **SGM -> MEM.encoding_state** [0:10]: Striatal gradient = novelty/encoding strength
- **BND -> MEM.retrieval_dynamics** [20:30]: Temporal binding = context-dependent retrieval
- **AED -> AED* (cross-circuit)**: Remains in mesolimbic circuit, accessed as cross-circuit read. Provides arousal dynamics [0:10] and expectancy affect [10:20] for context-dependent emotional processing.

The key architectural change: AED is now explicitly marked as a **cross-circuit read** (AED*) because affective entrainment dynamics belong to the mesolimbic pathway (ARU territory), not the mnemonic pathway (IMU). CDEM accesses AED* via the cross-unit pathway, making the circuit architecture cleaner and more neuroscientifically accurate.

---

**Model Status**: -- **REQUIRES VALIDATION**
**Output Dimensions**: **10D**
**Manifold Range**: **[398:408]**
**Evidence Tier**: **γ (Speculative) — <70% confidence**
