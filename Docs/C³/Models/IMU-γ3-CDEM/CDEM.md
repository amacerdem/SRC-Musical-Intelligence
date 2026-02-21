# IMU-γ3-CDEM: Context-Dependent Emotional Memory

**Model**: Context-Dependent Emotional Memory
**Unit**: IMU (Integrative Memory Unit)
**Circuit**: Mnemonic (Hippocampal-Cortical)
**Tier**: γ (Speculative) — <70% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added I, H feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/IMU-γ3-CDEM.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Context-Dependent Emotional Memory** (CDEM) models how musical emotional memories are modulated by listening context — cross-modal information (visual, spatial, social) shapes both the encoding strength and retrieval probability of emotionally tagged musical memories. This extends the MEAMN model (autobiographical memory) by adding the critical dimension of **context dependency**: the same music encoded in different emotional contexts produces different memory traces with different retrieval profiles.

```
THE THREE COMPONENTS OF CONTEXT-DEPENDENT EMOTIONAL MEMORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONTEXT MODULATION AROUSAL SUPPRESSION
Brain region: Hippocampus + Brain region: Amygdala + ACC
 anterior cingulate (ACC)
Mechanism: Cross-modal binding Mechanism: Visual context dampens
Trigger: Multi-sensory context arousal response to music
Function: "This music in THIS Function: "Music alone is more
 context = unique memory" arousing than music + video"
Evidence: Sachs 2025 fMRI Evidence: Mitterschiffthaler 2007
 (N=39, 6.26s context shift) (N=16, hippocampus/amygdala)

 ENCODING STRENGTH (Formation)
 Brain region: Hippocampus + mPFC
 Mechanism: Context-dependent consolidation
 Trigger: Emotional congruency x binding
 Function: "Mood-congruent contexts strengthen
 encoding of musical memories"
 Evidence: Janata 2009, Cheung 2019

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Core claim: Musical emotional memories are context-dependent, with
cross-modal information modulating encoding and retrieval strength.
Music-mood congruency amplifies memory formation; incongruent
contexts weaken it.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why Context Matters for Musical Memory

Context modulates musical memory through several mechanisms:

1. **Cross-modal binding**: When music is heard alongside visual, tactile, or social stimuli, the hippocampus binds these modalities into a unified episodic trace. The context becomes part of the memory — retrieval of the music retrieves the context, and vice versa. Billig et al. (2022) review extensive evidence that hippocampal computational architecture (trisynaptic loop, pattern completion) is engaged by auditory binding tasks.

2. **Arousal suppression**: Visual context (e.g., video) can dampen the arousal response to music. Music alone activates amygdala and autonomic pathways more strongly than music-with-video — the visual channel competes for attentional resources. Mitterschiffthaler et al. (2007) show sad music activates right hippocampus/amygdala (Talairach: 24, -15, -20, p = 0.051 FWE) while happy music activates ventral striatum and ACC.

3. **Mood congruency**: Emotional memories are encoded more strongly when the music's emotional content matches the listener's current mood or environmental context. Congruent encoding produces more accessible memory traces. Sachs et al. (2025) demonstrate that same-valence emotional transitions produce brain-state shifts 6.26s earlier than different-valence transitions (N=39, fMRI).

4. **Context-dependent retrieval**: Memories encoded in a specific emotional context are best retrieved when the same context is reinstated — a classic finding in memory research (Godden & Baddeley 1975) that extends to musical memories. Sakakibara et al. (2025) show that music-evoked nostalgia enhances memory vividness (Cohen's r = 0.88, N=33) via context-dependent autobiographical memory pathways.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The CDEM Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ CDEM — COMPLETE CIRCUIT ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ AUDITORY CORTEX (STG/A1) │ ║
║ │ │ ║
║ │ Core (A1) Belt Parabelt │ ║
║ │ Spectrotemporal Feature Pattern recognition │ ║
║ │ encoding extraction Multi-modal convergence │ ║
║ └──────┬──────────────┬──────────────────┬────────────────────────────┘ ║
║ │ │ │ ║
║ │ ┌────────┘ │ ║
║ │ │ CROSS-MODAL │ ║
║ │ │ INPUT │ ║
║ │ ▼ │ ║
║ ┌──────┴──────────────┐ ┌───────┴────────────────┐ ║
║ │ HIPPOCAMPUS │ │ ANTERIOR CINGULATE │ ║
║ │ │ │ (ACC) │ ║
║ │ • Context binding │ │ │ ║
║ │ • Episodic │ │ • Conflict monitoring │ ║
║ │ encoding │◄────────►│ • Context-dependent │ ║
║ │ • Pattern │ │ attention │ ║
║ │ completion │ │ • Arousal gating │ ║
║ └────────┬────────────┘ └─────────┬──────────────┘ ║
║ │ │ ║
║ └──────────────┬─────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────┐ ┌────────────────────┐ ║
║ │ mPFC │ │ AMYGDALA │ ║
║ │ │ │ │ ║
║ │ Self-referential │◄────────►│ Emotional │ ║
║ │ context │ │ tagging │ ║
║ │ evaluation │ │ (context- │ ║
║ │ │ │ modulated) │ ║
║ └────────┬──────────┘ └─────────┬──────────┘ ║
║ │ │ ║
║ └──────────────┬───────────────┘ ║
║ │ ║
║ ▼ ║
║ CONTEXT-DEPENDENT EMOTIONAL MEMORY ║
║ Encoding x Context x Affect ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Sachs et al. 2025: Context modulates emotion transitions (N=39, fMRI)
 Tempoparietal axis: same-valence 6.26s faster
Mitterschiffthaler 2007: Happy→striatum+ACC; Sad→hippocampus/amygdala (N=16)
Cheung et al. 2019: Amygdala+hippocampus: uncertainty x surprise (N=40)
Janata 2009: dMPFC hub for music-memory-emotion binding (N=13)
Billig et al. 2022: Hippocampus binds auditory+context (review)
Mori & Zatorre 2024: Pre-listening auditory-reward FC predicts chills (N=49)
```

### 2.2 Information Flow Architecture (EAR -> BRAIN -> H³ direct* -> CDEM)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ CDEM COMPUTATION ARCHITECTURE ║
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
║ │ │roughness │ │amplitude│ │warmth │ │flux │ │x_l0l5 │ │ ║
║ │ │stumpf │ │loudness │ │tonalness│ │entropy │ │x_l4l5 │ │ ║
║ │ │pleasant. │ │onset │ │ │ │concent. │ │x_l5l7 │ │ ║
║ │ └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │ ║
║ │ CDEM reads: 31D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed morphological features │ ║
║ │ │ ║
║ │ ┌── Encoding ──┐ ┌── Consolidation ─┐ ┌── Retrieval ──────┐ │ ║
║ │ │ 1s (H16) │ │ 5s (H20) │ │ 36s (H24) │ │ ║
║ │ │ │ │ │ │ │ │ ║
║ │ │ Working mem │ │ Hippocampal │ │ Long-term │ │ ║
║ │ │ context bind │ │ context window │ │ context chunk │ │ ║
║ │ └──────┬───────┘ └──────┬────────────┘ └──────┬────────────┘ │ ║
║ │ │ │ │ │ ║
║ │ └───────────────┴──────────────────────┘ │ ║
║ │ CDEM demand: ~18 of 2304 tuples │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN: Mnemonic Circuit ═════════ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────┐ ┌──────────────────────────┐ ║
║ │ [Mnemonic] │ │ [Mesolimbic, cross-cir.] │ ║
║ │ │ │ │ ║
║ │ Encoding [0:10]│ │ Arousal [0:10] │ ║
║ │ Familiar [10:20]│ │ Expectancy [10:20] │ ║
║ │ Retrieval[20:30]│ │ Motor-Aff. [20:30] │ ║
║ └────────┬────────┘ └──────────┬────────────────┘ ║
║ │ │ ║
║ └──────────┬──────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ CDEM MODEL (10D Output) │ ║
║ │ Manifold [398:408] │ ║
║ │ │ ║
║ │ Layer C (Context): f43_ctx_mod, f44_arousal_supp, │ ║
║ │ f45_encoding_str │ ║
║ │ Layer M (Math): congruency_index, context_recall_prob │ ║
║ │ Layer P (Present): binding_state, arousal_gate │ ║
║ │ Layer F (Future): encoding_strength_fc, retrieval_context_fc, │ ║
║ │ mood_congruency_fc │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Year | Method | N | Key Finding | Effect Size | Brain Regions | MNI/Talairach | MI Relevance |
|---|-------|------|--------|---|-------------|-------------|---------------|---------------|-------------|
| 1 | **Sachs, Kozak, Ochsner & Baldassano** | 2025 | fMRI (HMM + pattern analysis) | 39 | Emotions in the brain are dynamic and contextually dependent; tempoparietal brain-state transitions track emotional changes to music; same-valence context shifts transitions 6.26s earlier | z = 3.6-4.32 (transition alignment, p < 0.001); within > across context r: 0.303 vs 0.265 (p = 0.04) | Bilateral STG, MTG, angular gyrus, supramarginal gyrus, auditory cortex | Cortical surface searchlight (MNI space) | **f43_ctx_mod, congruency_index: context modulates emotional memory encoding and temporal dynamics** |
| 2 | **Mitterschiffthaler, Fu, Dalton, Andrew & Williams** | 2007 | fMRI (blocked, conjunction) | 16 | Happy music activates ventral/dorsal striatum, ACC, parahippocampal gyrus; sad music activates R hippocampus/amygdala | Happy > neutral: Z = 3.41-4.96 (p < 0.05 FWE); Sad hippocampus/amygdala: Z = 3.25, p = 0.051 FWE | L ventral striatum, L ACC (BA32/24), L parahippocampal gyrus, R hippocampus/amygdala | Talairach: L-VS (-8, 10, -6); L-ACC (-4, 10, 36) & (-4, 4, 12); R-HC/Amy (24, -15, -20) | **f44_arousal_supp, arousal: valence-specific activation of hippocampal-amygdalar complex** |
| 3 | **Cheung, Harrison, Meyer, Pearce, Haynes & Koelsch** | 2019 | fMRI + computational modeling | 79 (beh) + 40 (fMRI) | Uncertainty and surprise jointly predict musical pleasure; amygdala and hippocampus show interaction effect | Significant uncertainty x surprise interaction (p < 0.05 FWE); amygdala + auditory cortex reflect joint modulation | Amygdala, hippocampus, auditory cortex, nucleus accumbens | Whole-brain FWE-corrected | **f45_encoding_str, congruency_index: prediction error modulates emotional memory encoding via amygdala-hippocampal interaction** |
| 4 | **Janata** | 2009 | fMRI (parametric) | 13 | Dorsal MPFC (BA8/9) parametrically tracks autobiographical salience of music; MPFC serves as hub associating music, memories, and emotions; tonality tracking in same region | BOLD positively correlated with autobiographical salience (p < 0.05 corrected) | dMPFC (BA8/9), ventral MPFC, lateral PFC, posterior cortices | MNI: dMPFC ~(0, 38, 44) | **f43_ctx_mod, ctx_recall_prob: self-referential context evaluation via mPFC** |
| 5 | **Billig, Lad, Sedley & Griffiths** | 2022 | Comprehensive review | — | Hippocampus binds auditory information with spatiotemporal context; trisynaptic loop supports pattern completion for auditory memories; predictive map framework extends to sound | Review (100+ studies synthesized) | Hippocampus (CA1, CA3, DG), entorhinal cortex, parahippocampal cortex, perirhinal cortex | Multiple MNI/Talairach from reviewed studies | **binding_state, ctx_recall_prob: hippocampal computational architecture for auditory context binding** |
| 6 | **Sakakibara, Kusutomi, Kondoh et al.** | 2025 | EEG + behavioral (N-BMI neurofeedback) | 33 (17 older, 16 younger) | Nostalgia Brain-Music Interface enhances nostalgic feelings, well-being, and memory vividness; EEG decoder accuracy 64-72% above chance | Cohen's r = 0.71-0.88 (nostalgia/well-being/memory ratings, p < 0.003); EEG decoder: 64-72% (p < 0.01) | Temporal cortex (in-ear EEG) | N/A (in-ear EEG) | **congruency_index, mood_cong_fc: nostalgia as context-dependent emotional memory enhancing recall** |
| 7 | **Mori & Zatorre** | 2024 | fMRI (machine learning, LASSO) | 49 | Pre-listening auditory-reward functional connectivity predicts chills duration; right auditory cortex-striatum/OFC connections predict NAcc activation; auditory-amygdala FC predicts physiological arousal | r = 0.53 (LOPOCV, p < 0.001 FDR); generalized to independent dataset | R auditory cortex, striatum, OFC, nucleus accumbens, amygdala, insula | Auditory seeds from Morillon et al. 2012 | **arousal_gate, f44_arousal_supp: state-dependent auditory-reward coupling modulates emotional response** |
| 8 | **Borderie, Caclin, Lachaux et al.** | 2024 | iEEG (intracranial) | Epilepsy patients (clinical) | Theta-gamma phase-amplitude coupling in cortico-hippocampal networks supports auditory short-term memory retention; hippocampus + STS + IFG | Machine learning decodes correct/incorrect trials; theta-gamma CFC correlates with STM performance | Hippocampus, STS, IFG, inferior temporal gyrus | Intracranial electrode placement | **binding_state: theta-gamma coupling as neural mechanism for auditory memory binding** |
| 9 | **Calabria, Ciongoli, Grunden, Ordas & Garcia-Sanchez** | 2023 | Behavioral (3 experiments) | MCI patients (varies) | Background music during memory tasks: no main effect, but high-arousal music x mood regulation predicts performance; individual differences modulate music-memory interaction | Moderation by mood regulation (p < 0.05); negative pleasantness-performance relationship for low-arousal | N/A (behavioral) | N/A | **f44_arousal_supp: arousal level of musical context modulates memory encoding in clinical populations** |
| 10 | **Godden & Baddeley** | 1975 | Behavioral (field) | 18 | Context-dependent memory: words learned underwater recalled better underwater; encoding specificity principle | ~40% better recall in same context | N/A (behavioral, pre-neuroimaging) | N/A | **ctx_recall_prob: foundational context-dependent retrieval principle** |
| 11 | **Tulving & Thomson** | 1973 | Behavioral | — | Encoding specificity: retrieval cues effective only if encoded with target information | Theoretical framework | N/A | N/A | **ctx_recall_prob: encoding specificity principle for context-dependent memory** |
| 12 | **Huron** | 2006 | Theoretical (ITPRA model) | — | Sweet Anticipation: music and expectation; ITPRA framework for affective entrainment dynamics | Theoretical | N/A | N/A | **affective-dynamics mechanism: expectancy-based affective response framework** |

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
Evidence: Sachs 2025 — auditory cortex tracks emotional transitions

Phase 2: CROSS-MODAL BINDING (0.5-2s, H16 window)
───────────────────────────────────────────────────
Hippocampus binds auditory and contextual features
into a unified episodic trace. ACC monitors for
context-music congruency.
encoding_state activates.
Evidence: Billig 2022 — hippocampal trisynaptic loop for binding
 Borderie 2024 — theta-gamma CFC in hippocampus+STS

Phase 3: AROUSAL MODULATION (1-5s, H20 window)
──────────────────────────────────────────────
arousal is gated by contextual factors.
Music alone → higher arousal (amygdala dominant).
Music + video → suppressed arousal (attentional competition).
Emotional congruency amplifies encoding.
Evidence: Mitterschiffthaler 2007 — sad music → R-hippocampus/amygdala
 Mori & Zatorre 2024 — auditory-amygdala FC predicts arousal
 Calabria 2023 — arousal x mood regulation interaction

Phase 4: CONTEXT-DEPENDENT CONSOLIDATION (5-36s, H24 window)
────────────────────────────────────────────────────────────
Hippocampal-mPFC dialogue consolidates the context-tagged
memory trace. Stronger context binding → more durable memory.
retrieval_dynamics stores context-dependent trace.
Evidence: Janata 2009 — dMPFC tracks autobiographical salience
 Cheung 2019 — uncertainty x surprise in amygdala+hippocampus

Phase 5: CONTEXT-DEPENDENT RETRIEVAL (reinstated context)
─────────────────────────────────────────────────────────
When similar context is reinstated, hippocampal pattern
completion retrieves the bound memory. Congruent context
→ stronger retrieval. This is the encoding specificity
principle applied to musical memory.
Evidence: Sachs 2025 — same-valence context shifts transitions 6.26s earlier
 Sakakibara 2025 — nostalgia N-BMI enhances memory vividness
```

### 3.3 Effect Size Summary

```
Primary Evidence:
 Sachs 2025: z = 3.6-4.32 (emotion transition alignment, N=39)
 Mitterschiffthaler 2007: Z = 3.25-4.96 (valence-specific regions, N=16)
 Cheung 2019: Significant interaction (uncertainty x surprise, N=40)
 Mori & Zatorre 2024: r = 0.53 (auditory-reward FC predicts chills, N=49)
 Sakakibara 2025: Cohen's r = 0.71-0.88 (nostalgia ratings, N=33)

Pooled Estimate: Multiple converging fMRI + behavioral studies;
 insufficient overlap for formal meta-analysis
Quality Assessment: Substantially improved — 5 fMRI studies + 2 behavioral
 + 1 iEEG + 1 comprehensive review + 3 theoretical
Confidence Level: <70% (Speculative) — direct context-dependent MUSIC
 memory study still lacking; inferred from
 context-dependent emotion + music-evoked memory literatures
```

---

## 4. R³ Input Mapping: What CDEM Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | CDEM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Valence proxy (inverse) | Plomp & Levelt 1965; Mitterschiffthaler 2007 — consonance/dissonance maps to happy/sad brain activation |
| **A: Consonance** | [3] | stumpf_fusion | Binding strength proxy | Tonal fusion = coherent signal; Billig 2022 — hippocampal binding requires coherent input |
| **A: Consonance** | [4] | sensory_pleasantness | Mood congruency input | Pleasantness → positive context; Cheung 2019 — pleasantness from uncertainty x surprise |
| **B: Energy** | [7] | amplitude | Arousal correlate | Energy = emotional intensity; Calabria 2023 — arousal modulates memory |
| **B: Energy** | [10] | loudness | Arousal proxy | Stevens 1957 psychophysical; Mori & Zatorre 2024 — arousal predicts chills |
| **B: Energy** | [11] | onset_strength | Event salience | Transient energy = context boundary; Sachs 2025 — event boundaries drive brain-state transitions |
| **C: Timbre** | [12] | warmth | Context warmth | Low-frequency comfort |
| **C: Timbre** | [14] | tonalness | Pattern clarity | Harmonic-to-noise ratio |
| **D: Change** | [21] | spectral_flux | Context change detection | Flux = environmental shift; Sachs 2025 — emotional transitions marked by acoustic changes |
| **D: Change** | [22] | entropy | Context complexity | Encoding difficulty; Cheung 2019 — high entropy = high uncertainty |
| **D: Change** | [24] | spectral_concentration | Event salience | Temporal concentration |
| **E: Interactions** | [25:33] | x_l0l5 (Energy x Consonance) | Context-memory binding | Pattern-emotion coupling |
| **E: Interactions** | [41:49] | x_l5l7 (Consonance x Timbre) | Mood congruency signal | Timbre-consonance = familiar context |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | CDEM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **I: Information** | [87] | melodic_entropy | Emotional surprise — high melodic information = stronger emotional encoding | Pearce 2005: IDyOM information content |
| **I: Information** | [88] | harmonic_entropy | Harmonic unpredictability — chord surprise modulates emotional context | Harrison & Pearce 2020; Cheung 2019 |
| **H: Harmony** | [84] | tonal_stability | Tonal context strength — stable key = congruent emotional context | Krumhansl 1990: tonal hierarchy |

**Rationale**: CDEM models context-dependent emotional memory, where emotional context during encoding determines retrieval. Melodic and harmonic entropy quantify the surprise/information content that modulates emotional encoding strength (per Cheung et al. 2019, prediction error from uncertainty drives stronger hippocampal-amygdala engagement). Tonal stability provides the harmonic context against which emotional congruency is computed — stable tonal contexts create coherent emotional memories, while tonal ambiguity creates context-dependent variability in emotional retrieval.

> **Code impact**: These features are doc-only until Phase 5 wiring. No changes to `cdem.py`.

### 4.3 Physical -> Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[0] roughness (inverse) ─────► Consonance/pleasantness → valence
 Context: pleasant music = positive context

R³[10] loudness + R³[7] amp ───► Arousal level → emotional intensity
 Context: loud = salient context marker
 Math: arousal = σ(0.5 · loudness + 0.5 · amplitude)

R³[21] spectral_flux ─────────► Context change detection
 High flux = environmental transition
 New context → new memory trace

R³[22] entropy ────────────────► Context complexity
 Low entropy = predictable context
 High entropy = novel context → weaker binding

R³[25:33] x_l0l5 ─────────────► Context-memory binding strength
 Math: binding ∝ x_l0l5 · stumpf[3]

R³[41:49] x_l5l7 ─────────────► Mood congruency signal
 Consonance x timbre warmth = congruent context
 This IS the mood-matching signal
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

CDEM requires H³ features at three horizons: H16 (1s), H20 (5s), H24 (36s), and two affective-dynamics horizons: H6 (200ms), H16 (1s).

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

**v1 demand**: 18 tuples

#### R³ v2 Projected Expansion

No significant v2 expansion projected. CDEM's context-dependent emotional memory operates through v1 spectral features (entropy, flux, warmth, interactions) that fully capture the mood-congruent encoding mechanism. The v2 groups do not add distinct context-dependency inputs.

**v2 projected**: 0 tuples
**Total projected**: 18 tuples of 294,912 theoretical = 0.0061%

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
CDEM OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
MANIFOLD RANGE: IMU CDEM [398:408]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER C — CONTEXT-DEPENDENT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0 │ f43_ctx_mod │ [0, 1] │ Cross-modal context modulation.
 │ │ │ Hippocampus + ACC multi-modal binding.
 │ │ │ f43 = σ(0.35 · x_l0l5.mean · encoding
 │ │ │ + 0.35 · (1-roughness) · familiar
 │ │ │ + 0.30 · stumpf · retrieval)
 │ │ │ |w| sum = 1.00
 │ │ │ Basis: Sachs 2025, Billig 2022
────┼───────────────────┼────────┼────────────────────────────────────────────
 1 │ f44_arousal_supp │ [0, 1] │ Context-dependent arousal suppression.
 │ │ │ Amygdala arousal gated by context.
 │ │ │ f44 = σ(0.40 · arousal · loudness
 │ │ │ + 0.30 · entropy · (1-stumpf)
 │ │ │ + 0.30 · flux · amplitude)
 │ │ │ |w| sum = 1.00
 │ │ │ Basis: Mitterschiffthaler 2007, Mori 2024
────┼───────────────────┼────────┼────────────────────────────────────────────
 2 │ f45_encoding_str │ [0, 1] │ Context-dependent encoding strength.
 │ │ │ Hippocampus + mPFC consolidation.
 │ │ │ f45 = σ(0.40 · encoding · x_l5l7.mean
 │ │ │ + 0.30 · (1-roughness) · warmth
 │ │ │ + 0.30 · expectancy · stumpf)
 │ │ │ |w| sum = 1.00
 │ │ │ Basis: Cheung 2019, Janata 2009

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 3 │ congruency_index │ [0, 1] │ Music-mood congruency estimation.
 │ │ │ f(context_valence x music_valence x
 │ │ │ context_arousal x music_arousal)
 │ │ │ Congruent context = stronger encoding.
 │ │ │ σ(0.50 · (1-roughness) · familiar
 │ │ │ + 0.50 · x_l5l7.mean · warmth)
 │ │ │ |w| sum = 1.00
 │ │ │ Basis: Sachs 2025, Sakakibara 2025
────┼───────────────────┼────────┼────────────────────────────────────────────
 4 │ ctx_recall_prob │ [0, 1] │ P(recall | context reinstated).
 │ │ │ σ(0.35 · retrieval
 │ │ │ + 0.35 · familiar
 │ │ │ + 0.30 · (1-entropy))
 │ │ │ |w| sum = 1.00
 │ │ │ Basis: Godden & Baddeley 1975, Billig 2022

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 5 │ binding_state │ [0, 1] │ Current cross-modal binding activation.
 │ │ │ encoding.mean() x stumpf.
 │ │ │ Basis: Borderie 2024, Billig 2022
────┼───────────────────┼────────┼────────────────────────────────────────────
 6 │ arousal_gate │ [0, 1] │ Context-modulated arousal gate.
 │ │ │ arousal.mean() x (1-entropy).
 │ │ │ Basis: Mori & Zatorre 2024, Calabria 2023

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 7 │ enc_strength_fc │ [0, 1] │ Encoding strength prediction (2-5s ahead).
 │ │ │ Hippocampal consolidation trajectory.
────┼───────────────────┼────────┼────────────────────────────────────────────
 8 │ retrieval_ctx_fc │ [0, 1] │ Context retrieval prediction (5-10s ahead).
 │ │ │ mPFC context reinstatement trajectory.
────┼───────────────────┼────────┼────────────────────────────────────────────
 9 │ mood_cong_fc │ [0, 1] │ Mood congruency prediction (1-3s ahead).
 │ │ │ Congruency trend trajectory.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Context-Dependent Encoding Function

```
Context_Encoding(music, context) = f(Binding x Congruency x ArousalGate)

P(recall | context) = σ(b0 + b1·Familiarity + b2·Congruency + b3·Binding)

where:
 Binding = encoding_state.mean() x R³.stumpf[3]
 Congruency = (1 - R³.roughness[0]) x R³.warmth[12] x x_l5l7.mean()
 ArousalGate = arousal.mean() x (1 - R³.entropy[22])
 Familiarity = familiarity_proxy.mean()

Expanded form with mechanisms:
.mean() · Congruency
.mean() · ArousalGate

CONSTRAINT: For all sigmoid formulas, |wi| must sum <= 1.0
```

### 7.2 Feature Formulas

```python
# f43: Context Modulation — cross-modal memory binding
# |w| = 0.35 + 0.35 + 0.30 = 1.00 <= 1.0 checkmark

# f44: Arousal Suppression — context-dependent arousal gating
# |w| = 0.40 + 0.30 + 0.30 = 1.00 <= 1.0 checkmark
f44 = σ(0.40 · mean(arousal[0:10]) · R³.loudness[10]
 + 0.30 · R³.entropy[22] · (1 - R³.stumpf[3])
 + 0.30 · R³.spectral_flux[21] · R³.amplitude[7])

# f45: Encoding Strength — context-dependent memory formation
# |w| = 0.40 + 0.30 + 0.30 = 1.00 <= 1.0 checkmark
 + 0.30 · (1 - R³.roughness[0]) · R³.warmth[12]
 + 0.30 · mean(expectancy[10:20]) · R³.stumpf[3])

# congruency_index: Music-mood matching
# |w| = 0.50 + 0.50 = 1.00 <= 1.0 checkmark
 + 0.50 · mean(R³.x_l5l7[41:49]) · R³.warmth[12])

# ctx_recall_prob: Context-dependent recall probability
# |w| = 0.35 + 0.35 + 0.30 = 1.00 <= 1.0 checkmark
 + 0.30 · (1 - R³.entropy[22]))
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| # | Region | MNI / Talairach | Evidence | Source | CDEM Function |
|---|--------|-----------------|----------|--------|---------------|
| 1 | **Hippocampus** | +/-20, -24, -12 (MNI bilateral) | Direct (fMRI) | Cheung 2019; Billig 2022 (review); Borderie 2024 (iEEG) | Context-dependent episodic encoding/retrieval; pattern completion |
| 2 | **Amygdala** | Talairach: 24, -15, -20 (R) | Direct (fMRI) | Mitterschiffthaler 2007 (Z=3.25); Cheung 2019 | Emotional tagging modulated by context; uncertainty x surprise interaction |
| 3 | **mPFC / dMPFC** | MNI: ~0, 38, 44 (BA8/9) | Direct (fMRI) | Janata 2009 (N=13, parametric) | Self-referential context evaluation; music-memory-emotion integration hub |
| 4 | **ACC** | Talairach: -4, 10, 36 (BA32); -4, 4, 12 (BA24) | Direct (fMRI) | Mitterschiffthaler 2007 (Z=3.39-3.92, p<0.02 FWE) | Context-music conflict monitoring; arousal gating; reward processing |
| 5 | **STG / STS (bilateral)** | Cortical surface (MNI space) | Direct (fMRI, iEEG) | Sachs 2025 (N=39); Borderie 2024 (iEEG theta-gamma) | Tempoparietal emotion tracking; auditory context-dependent processing; multimodal integration |
| 6 | **Parahippocampal gyrus** | Talairach: -14, -46, -6 (L) | Direct (fMRI) | Mitterschiffthaler 2007 (Z=3.31, p=0.022 FWE) | Context-dependent spatial/emotional information retrieval |
| 7 | **Ventral striatum** | Talairach: -8, 10, -6 (L) | Direct (fMRI) | Mitterschiffthaler 2007 (Z=3.41, p=0.018 FWE); Mori 2024 | Reward processing for emotionally congruent musical contexts |

---

## 9. Cross-Unit Pathways

### 9.1 CDEM <-> Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ CDEM INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ └── CDEM reads affective-dynamics as cross-circuit input │
│ │
│ INTRA-UNIT (IMU): │
│ MEAMN ──────────────────► CDEM │
│ │ └── MEAMN provides autobiographical memory │
│ │ signals; CDEM adds context dependency │
│ │ │
│ CDEM ───────► HCMC (Hippocampal-Cortical Memory Circuit) │
│ │ └── CDEM context-binding feeds hippocampal dialogue │
│ │ │
│ ├─────► PMIM (Predictive Memory Integration) │
│ │ └── Context modulates predictive memory processing │
│ │ │
│ └─────► MMP (Musical Mnemonic Preservation) │
│ └── Context-dependent memories in neurodegeneration │
│ │
│ CROSS-UNIT (CDEM → ARU): │
│ CDEM.congruency_index ────► ARU.SRP (congruent context → pleasure) │
│ CDEM.arousal_gate ────────► ARU.AAC (context-modulated autonomic) │
│ │
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
| **Context reinstatement** | Same context at retrieval should enhance music memory recall | -- **Indirectly supported** — Sachs 2025 shows same-valence context produces earlier brain-state transitions (6.26s); Godden & Baddeley 1975 established principle |
| **Arousal suppression** | Music + video should produce lower arousal than music alone | -- **Indirectly supported** — Mori & Zatorre 2024 show auditory-amygdala FC predicts physiological arousal; Calabria 2023 shows arousal x mood regulation interaction |
| **Mood congruency** | Mood-congruent music-context pairing should enhance encoding | -- **Partially confirmed** — Sachs 2025 shows context modulates emotion ratings (within r=0.303 > across r=0.265, p=0.04); Sakakibara 2025 shows congruent nostalgia enhances memory |
| **Hippocampal binding** | Hippocampal lesions should impair context-dependent musical memory | -- **Indirectly supported** via Billig 2022 review of hippocampal lesion literature; Borderie 2024 iEEG theta-gamma coupling |
| **Cross-modal integration** | STS/tempoparietal activation should increase with multi-modal musical contexts | -- **Confirmed** — Sachs 2025 (N=39, z=3.6-4.32 for emotion transitions in tempoparietal axis, p<0.001) |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class CDEM(BaseModel):
 """Context-Dependent Emotional Memory.

 Output: 10D per frame.
 Zero learned parameters — all computations are deterministic.
 """
 NAME = "CDEM"
 UNIT = "IMU"
 TIER = "gamma3"
 OUTPUT_DIM = 10
 CROSS_UNIT_READS = ()  # TODO: populate from Nucleus contract # Cross-circuit read from mesolimbic

 # Coefficient constraint: for σ(Sum wi·gi), |wi| must sum <= 1.0
 # f43: 0.35 + 0.35 + 0.30 = 1.00 checkmark
 # f44: 0.40 + 0.30 + 0.30 = 1.00 checkmark
 # f45: 0.40 + 0.30 + 0.30 = 1.00 checkmark
 # congruency: 0.50 + 0.50 = 1.00 checkmark
 # ctx_recall: 0.35 + 0.35 + 0.30 = 1.00 checkmark

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """18 tuples for CDEM computation."""
 return [
 # (r3_idx, horizon, morph, law)
 (3, 16, 1, 2), # stumpf_fusion, 1s, mean, bidirectional
 (3, 20, 1, 0), # stumpf_fusion, 5s, mean, forward
 (4, 16, 0, 2), # pleasantness, 1s, value, bidirectional
 (4, 20, 18, 0), # pleasantness, 5s, trend, forward
 (10, 16, 0, 2), # loudness, 1s, value, bidirectional
 (10, 20, 1, 0), # loudness, 5s, mean, forward
 (12, 16, 0, 2), # warmth, 1s, value, bidirectional
 (12, 20, 1, 0), # warmth, 5s, mean, forward
 (21, 16, 0, 2), # spectral_flux, 1s, value, bidirectional
 (21, 20, 4, 0), # spectral_flux, 5s, max, forward
 (22, 16, 0, 2), # entropy, 1s, value, bidirectional
 (22, 20, 1, 0), # entropy, 5s, mean, forward
 (22, 24, 19, 0), # entropy, 36s, stability, forward
 (0, 16, 0, 2), # roughness, 1s, value, bidirectional
 (0, 20, 18, 0), # roughness, 5s, trend, forward
 (7, 16, 8, 0), # amplitude, 1s, velocity, forward
 (11, 16, 0, 2), # onset_strength, 1s, value, bidirectional
 (11, 20, 4, 0), # onset_strength, 5s, max, forward
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 """
 Compute CDEM 10D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
 r3: (B,T,49) raw R³ features

 Returns:
 (B,T,10) CDEM output
 """
 # R³ features
 roughness = r3[..., 0:1] # [0, 1]
 stumpf = r3[..., 3:4] # [0, 1]
 amplitude = r3[..., 7:8] # [0, 1]
 loudness = r3[..., 10:11] # [0, 1]
 warmth = r3[..., 12:13] # [0, 1]
 spectral_flux = r3[..., 21:22] # [0, 1]
 entropy = r3[..., 22:23] # [0, 1]
 x_l0l5 = r3[..., 25:33] # (B, T, 8)
 x_l5l7 = r3[..., 41:49] # (B, T, 8)

 # affective-dynamics cross-circuit sub-sections
 # === LAYER C: Context-dependent features ===
 # f43: Context Modulation (|w| = 0.35+0.35+0.30 = 1.00)
 f43 = torch.sigmoid(
 0.35 * x_l0l5.mean(-1, keepdim=True)
 + 0.35 * (1.0 - roughness)
 + 0.30 * stumpf
 )

 # f44: Arousal Suppression (|w| = 0.40+0.30+0.30 = 1.00)
 f44 = torch.sigmoid(
 * loudness
 + 0.30 * entropy * (1.0 - stumpf)
 + 0.30 * spectral_flux * amplitude
 )

 # f45: Encoding Strength (|w| = 0.40+0.30+0.30 = 1.00)
 f45 = torch.sigmoid(
 * x_l5l7.mean(-1, keepdim=True)
 + 0.30 * (1.0 - roughness) * warmth
 * stumpf
 )

 # === LAYER M: Mathematical ===
 # Congruency index (|w| = 0.50+0.50 = 1.00)
 congruency = torch.sigmoid(
 0.50 * (1.0 - roughness)
 + 0.50 * x_l5l7.mean(-1, keepdim=True)
 * warmth
 )

 # Context recall probability (|w| = 0.35+0.35+0.30 = 1.00)
 ctx_recall = torch.sigmoid(
 + 0.30 * (1.0 - entropy)
 )

 # === LAYER P: Present ===
 binding_state = (
 ).clamp(0, 1)
 arousal_gate = (
 ).clamp(0, 1)

 # === LAYER F: Future ===
 enc_strength_fc = self._predict_future(
 mem_encoding, h3_direct, window_h=20)
 retrieval_ctx_fc = self._predict_future(
 mem_retrieval, h3_direct, window_h=24)
 mood_cong_fc = self._predict_future(
 mem_familiar, h3_direct, window_h=16)

 return torch.cat([
 f43, f44, f45, # C: 3D
 congruency, ctx_recall, # M: 2D
 binding_state, arousal_gate, # P: 2D
 enc_strength_fc, retrieval_ctx_fc, # F: 3D
 mood_cong_fc,
 ], dim=-1) # (B, T, 10)
```

### 11.2 Doc-Code Mismatches (cdem.py vs this document)

| Aspect | Code (cdem.py) | Doc (this file) | Severity |
|--------|---------------|-----------------|----------|
| **LAYERS** | E(2D), M(2D), P(3D), F(3D) = different names | C(3D), M(2D), P(2D), F(3D) | High — feature names and layer structure diverge |
| **Dimension names** | f01_context_modulation, f02_emotional_encoding, context_dependency_index, cross_modal_enhancement, emotional_state, context_match, encoding_strength, retrieval_context_pred, emotional_decay_fc, recontextualization_pred | f43_ctx_mod, f44_arousal_supp, f45_encoding_str, congruency_index, ctx_recall_prob, binding_state, arousal_gate, enc_strength_fc, retrieval_ctx_fc, mood_cong_fc | High — complete naming divergence |
| **CROSS_UNIT_READS** | `()` (empty) | `CROSS_UNIT_READS = ()  # TODO: populate from Nucleus contract` | Medium — code missing cross-circuit read |
| **h3_demand** | `()` (empty tuple) | 18 tuples specified | Medium — code has no temporal demand |
| **brain_regions** | Hippocampus, Amygdala, STS (3 regions) | Hippocampus, Amygdala, mPFC, ACC, STG/STS, Parahippocampal, V-Striatum (7 regions) | Medium — code missing 4 regions |
| **Citations** | "Eschrich 2008" (not in doc) | 12 papers listed | Medium — code has unverified citation |
| **compute()** | Stub returning zeros | Full computation specified | Expected — stub pending Phase 2 |
| **version** | 2.0.0 | 2.1.0 | Low — will sync in Phase 2 |

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 | 5 fMRI + 1 iEEG + 2 behavioral + 1 review + 3 theoretical |
| **Effect Sizes** | 5+ | Sachs z=3.6-4.32; Mitterschiffthaler Z=3.25-4.96; Mori r=0.53; Sakakibara r=0.71-0.88 |
| **Evidence Modality** | fMRI, iEEG, EEG, behavioral | Multi-modal converging evidence |
| **Brain Regions with MNI** | 7 | Hippocampus, amygdala, mPFC, ACC, STG/STS, parahippocampal, ventral striatum |
| **Falsification Tests** | 3/5 partially confirmed or indirectly supported | Improved from 1/5 |
| **R³ Features Used** | 31D of 49D | Context-focused |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **Output Dimensions** | **10D** | 4-layer structure |
| **Manifold Range** | **[398:408]** | IMU CDEM block |

---

## 13. Scientific References

1. **Sachs, M. E., Kozak, M. S., Ochsner, K. N. & Baldassano, C.** (2025). Emotions in the brain are dynamic and contextually dependent: using music to measure affective transitions. *eNeuro*. https://doi.org/10.1523/ENEURO.0184-24.2025. N=39, fMRI. Tempoparietal brain-state transitions track emotional context; same-valence context shifts transitions 6.26s earlier.

2. **Mitterschiffthaler, M. T., Fu, C. H. Y., Dalton, J. A., Andrew, C. M. & Williams, S. C. R.** (2007). A functional MRI study of happy and sad affective states induced by classical music. *Human Brain Mapping*, 28, 1150-1162. N=16, fMRI. Happy music → ventral striatum + ACC; Sad music → R hippocampus/amygdala (Talairach: 24, -15, -20).

3. **Cheung, V. K. M., Harrison, P. M. C., Meyer, L., Pearce, M. T., Haynes, J.-D. & Koelsch, S.** (2019). Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. *Current Biology*, 29, 4084-4092. N=79 (beh) + 40 (fMRI). Uncertainty x surprise interaction in amygdala + hippocampus.

4. **Janata, P.** (2009). The neural architecture of music-evoked autobiographical memories. *Cerebral Cortex*, 19, 2579-2594. N=13, fMRI. Dorsal MPFC (BA8/9) parametrically tracks autobiographical salience; music-memory-emotion integration hub.

5. **Billig, A. J., Lad, M., Sedley, W. & Griffiths, T. D.** (2022). The hearing hippocampus. *Progress in Neurobiology*, 218, 102326. Comprehensive review of hippocampal role in auditory processing, binding, and memory.

6. **Sakakibara, Y., Kusutomi, T., Kondoh, S. et al.** (2025). A Nostalgia Brain-Music Interface for enhancing nostalgia, well-being, and memory vividness. *Scientific Reports*, 15, 32337. N=33 (17 older, 16 younger), EEG. Nostalgia enhances memory vividness (Cohen's r = 0.88).

7. **Mori, K. & Zatorre, R.** (2024). State-dependent connectivity in auditory-reward networks predicts peak pleasure experiences to music. *PLOS Biology*, 22(8), e3002732. N=49, fMRI. Pre-listening auditory-reward FC predicts chills (r=0.53, p<0.001).

8. **Borderie, A., Caclin, A., Lachaux, J.-P. et al.** (2024). Cross-frequency coupling in cortico-hippocampal networks supports the maintenance of sequential auditory information in short-term memory. *PLOS Biology*, 22(3), e3002512. iEEG. Theta-gamma CFC in hippocampus + STS supports auditory memory.

9. **Calabria, M., Ciongoli, F., Grunden, N., Ordas, C. & Garcia-Sanchez, C.** (2023). Background music and memory in mild cognitive impairment: the role of interindividual differences. *Journal of Alzheimer's Disease*, 92, 815-829. MCI patients. Arousal x mood regulation interaction for music-memory effects.

10. **Godden, D. R. & Baddeley, A. D.** (1975). Context-dependent memory in two natural environments: on land and underwater. *British Journal of Psychology*, 66, 325-331. N=18. Classic context-dependent memory demonstration.

11. **Tulving, E. & Thomson, D. M.** (1973). Encoding specificity and retrieval processes in episodic memory. *Psychological Review*, 80, 352-373. Encoding specificity principle.

12. **Huron, D.** (2006). *Sweet Anticipation: Music and the Psychology of Expectation*. MIT Press. ITPRA model for affective-dynamics mechanism framework.

---

## 14. Migration Notes (D0 -> MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) | MI (v2.1.0) |
|--------|-------------|-------------|-------------|
| Input space | S0 (256D) | R³ (49D) | R³ (49D) — unchanged |
| Context binding | S0.X_L5L6 x HC0.BND | R³.x_l0l5 x encoding | Unchanged |
| Arousal suppression | S0.L5.loudness x HC⁰ affect | R³.loudness x arousal | Unchanged |
| Encoding strength | S0.X_L5L9 x HC0.SGM | R³.x_l5l7 x encoding | Unchanged |
| Demand format | HC0 index ranges | H³ 4-tuples (sparse) | Unchanged |
| Total demand | 24/2304 = 1.04% | 18/2304 = 0.78% | Unchanged |
| Output dims | 11D | 10D (more compact, no reserved slot) | Unchanged |
| **Papers** | **2** | **2** | **12 (deep lit review)** |
| **Brain regions** | **4** | **4** | **7 (with verified MNI/Talairach)** |
| **Effect sizes** | **1** | **1** | **5+ (multi-study converging)** |

---

**Model Status**: -- **REQUIRES VALIDATION**
**Output Dimensions**: **10D**
**Manifold Range**: **[398:408]**
**Evidence Tier**: **gamma (Speculative) — <70% confidence**
