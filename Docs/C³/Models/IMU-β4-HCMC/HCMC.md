# IMU-β4-HCMC: Hippocampal-Cortical Memory Circuit

**Model**: Hippocampal-Cortical Memory Circuit
**Unit**: IMU (Integrative Memory Unit)
**Circuit**: Mnemonic (Hippocampal-Cortical)
**Tier**: β (Integrative) — 70-90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added I feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/IMU-β4-HCMC.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Hippocampal-Cortical Memory Circuit** (HCMC) models the core dialogue between hippocampus and cortical networks that underlies musical memory formation, consolidation, and retrieval. The hippocampus performs fast initial binding of musical features into episodic traces, while cortical networks (entorhinal cortex, mPFC, posterior cingulate) gradually consolidate these traces into long-term storage. This model captures the three canonical phases of memory: encoding, consolidation, and retrieval.

```
THE THREE PHASES OF HIPPOCAMPAL-CORTICAL MEMORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ENCODING (Fast, Hippocampal) CONSOLIDATION (Slow, Cortical)
Brain region: Hippocampus + EC Brain region: mPFC + PCC
Mechanism: Rapid feature binding Mechanism: Replay & reactivation
Timescale: Milliseconds → seconds Timescale: Seconds → hours
Function: "I am encoding this now" Function: "Strengthening the trace"
Evidence: L4 velocity triggers Evidence: Hippocampal replay during
 hippocampal binding rest/sleep transfers to cortex

 RETRIEVAL (Reconstructive, Bilateral)
 Brain region: Hippocampus ↔ Cortex
 Mechanism: Pattern completion + detail filling
 Timescale: ~500ms → seconds
 Function: "I remember this pattern"
 Evidence: Hippocampal cue → cortical reconstruction

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Complementary Learning Systems theory (McClelland et al. 1995):
Fast hippocampal binding + slow cortical integration = optimal
memory system. Musical memory is a clear instance of this principle.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why the Hippocampal-Cortical Dialogue Is Critical for Music

Musical memory depends on this two-system architecture because:

1. **Fast binding requirement**: Musical features unfold rapidly — a melodic phrase lasts 2-5 seconds. The hippocampus must bind pitch, timbre, and temporal features within this window before the information is lost.

2. **Long-term consolidation**: Familiar melodies can be recognized after decades. This requires gradual transfer from hippocampal traces to cortical networks (entorhinal cortex, mPFC) that are resistant to interference.

3. **Episodic segmentation**: Music naturally divides into events at spectral flux boundaries. The hippocampus detects these boundaries and creates distinct episodic segments — each phrase becomes a separate memory trace.

4. **Pattern completion at retrieval**: Hearing the first few notes of a familiar melody triggers hippocampal pattern completion, which then recruits cortical detail (full harmonic structure, timbral quality) for vivid reconstruction.

### 1.2 Relationship to Other IMU Models

HCMC is the **circuit-level** model of the hippocampal-cortical memory system. It complements:
- **MEAMN** (α1): Models autobiographical memory retrieval (what HCMC encodes, MEAMN retrieves)
- **MMP** (α3): Models preservation in neurodegeneration (what HCMC stores, MMP explains why it survives)
- **PMIM** (β2): Models predictive memory integration (HCMC provides the stored templates that PMIM predicts against)

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The HCMC Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ HCMC — COMPLETE CIRCUIT ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ AUDITORY CORTEX (STG/A1) │ ║
║ │ │ ║
║ │ Core (A1) Belt Parabelt │ ║
║ │ Spectrotemporal Feature Pattern recognition │ ║
║ │ encoding extraction Melodic contour + timbre │ ║
║ └──────┬──────────────┬──────────────────┬────────────────────────────┘ ║
║ │ │ │ ║
║ ▼ ▼ ▼ ║
║ ┌──────────────────────────────────────────────────────────────┐ ║
║ │ HIPPOCAMPAL FORMATION │ ║
║ │ │ ║
║ │ ┌──────────────────┐ ┌────────────────────┐ │ ║
║ │ │ ENTORHINAL CTX │ │ HIPPOCAMPUS │ │ ║
║ │ │ │ │ (CA1, CA3, DG) │ │ ║
║ │ │ Grid cells: │ │ │ │ ║
║ │ │ Spatial-temporal │ │ • Fast binding │ │ ║
║ │ │ context encoding│ │ • Pattern │ │ ║
║ │ │ │ │ completion │ │ ║
║ │ │ EC → DG → CA3 │ │ • Episodic │ │ ║
║ │ │ (trisynaptic) │ │ segmentation │ │ ║
║ │ └──────────────────┘ └─────────┬────────────┘ │ ║
║ └──────────────────────────────────┼─────────────────────────────┘ ║
║ │ ║
║ Hippocampal replay │ Cortical feedback ║
║ (consolidation) │ (top-down retrieval) ║
║ │ ║
║ ┌──────────────────────────────────┼─────────────────────────────┐ ║
║ │ CORTICAL NETWORKS │ ║
║ │ │ ║
║ │ ┌──────────────────┐ ┌────────────────────┐ │ ║
║ │ │ mPFC │ │ PCC │ │ ║
║ │ │ │ │ (Posterior │ │ ║
║ │ │ Schema memory: │ │ Cingulate) │ │ ║
║ │ │ Long-term │ │ │ │ ║
║ │ │ pattern storage │ │ Episodic │ │ ║
║ │ │ + consolidation │ │ recollection │ │ ║
║ │ └──────────────────┘ └────────────────────┘ │ ║
║ └────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Hippocampal fast binding: CA3 autoassociative network (Rolls 2013)
Cortical consolidation: Systems consolidation theory (Squire 2004)
Musical episodic segments: Event segmentation theory (Zacks 2007)
Hippocampal-cortical replay: Sharp-wave ripples drive transfer (Buzsaki 2015)
```

### 2.2 Information Flow Architecture (EAR → BRAIN → HCMC)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ HCMC COMPUTATION ARCHITECTURE ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ AUDIO (44.1kHz waveform) ║
║ │ ║
║ ▼ ║
║ ┌──────────────────┐ ║
║ │ COCHLEA │ 128 mel bins × 172.27Hz frame rate ║
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
║ │ │sethares │ │loudness │ │tristim. │ │entropy │ │x_l4l5 │ │ ║
║ │ │pleasant. │ │onset │ │tonalness│ │concent. │ │x_l5l7 │ │ ║
║ │ └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │ ║
║ │ HCMC reads: 38D │ ║
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
║ │ │ binding │ │ binding window │ │ episodic chunk │ │ ║
║ │ └──────┬───────┘ └──────┬────────────┘ └──────┬────────────┘ │ ║
║ │ │ │ │ │ ║
║ │ └───────────────┴──────────────────────┘ │ ║
║ │ HCMC demand: ~42 of 2304 tuples │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN: Mnemonic Circuit ═════════ ║
║ │ ║
║ ▼ ║
║ ┌─────────────────┐ ║
║ │ │ ║
║ │ Encoding [0:10]│ novelty, binding strength, schema match ║
║ │ Familiar [10:20]│ recognition, nostalgia, deja-vu ║
║ │ Retrieval[20:30]│ recall probability, vividness, coloring ║
║ └────────┬────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ HCMC MODEL (11D Output) │ ║
║ │ │ ║
║ │ Layer E (Episodic): f19_fast_binding, f20_episodic_seg, │ ║
║ │ f21_cortical_storage │ ║
║ │ Layer M (Math): consolidation_strength, encoding_rate │ ║
║ │ Layer P (Present): binding_state, segmentation_state, │ ║
║ │ storage_state │ ║
║ │ Layer F (Future): consolidation_pred, retrieval_pred, │ ║
║ │ pattern_completion_pred │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Squire & Alvarez 1995** | Review/lesion | — | Hippocampal-cortical complementary learning systems theory | — | **fast binding architecture** |
| 2 | **McClelland et al. 1995** | Computational | — | Complementary learning systems: fast hippocampal + slow cortical | — | **Encoding vs consolidation timescales** |
| 3 | **Zacks et al. 2007** | Behavioral + fMRI | — | Event segmentation theory: boundaries trigger encoding | — | **f20_episodic_seg: event boundaries** |
| 4 | **Rolls 2013** | Computational | — | CA3 autoassociative network for fast pattern binding | — | **f19_fast_binding: hippocampal binding** |
| 5 | **Buzsaki 2015** | Review | — | Sharp-wave ripples drive hippocampal-cortical transfer | — | **consolidation mechanism** |
| 6 | **Cheung et al. 2019** | fMRI | 79 (39 beh + 40 fMRI) | Uncertainty × surprise interaction modulates bilateral amygdala/hippocampus and auditory cortex BOLD during chord listening; hippocampus encodes sequence uncertainty | beta = -0.140 [CI -0.238, -0.041], p = 0.002 (R amygdala/hippo); marginal R² = 0.476 | **f19_fast_binding: hippocampal encoding of musical expectation uncertainty; f20_episodic_seg: surprise-driven boundary detection** |
| 7 | **Billig et al. 2022** | Review | — | Comprehensive review of hippocampal auditory processing: hippocampus tracks and manipulates auditory information including music; connectivity from EC → DG → CA3 → CA1 trisynaptic pathway processes temporal sequences | — | **Circuit architecture: validates EC → hippocampus → cortex pathway for auditory/musical information** |
| 8 | **Fernandez-Rubio et al. 2022** | MEG | 71 | Tonal sequence recognition activates hippocampus + cingulate; atonal recognition activates auditory processing network; left hippocampus and parahippocampal gyrus activated at 4th tone of memorized tonal sequences | F(3,280) = 6.87, p = 0.002 (accuracy); MCS p < 0.001 (source clusters) | **f21_cortical_storage: tonal familiarity recruits hippocampal-cingulate memory circuit; f19_fast_binding: tone-by-tone hippocampal activation** |
| 9 | **Borderie et al. 2024** | SEEG (intracranial) | epilepsy patients | Theta-gamma phase-amplitude coupling in STS, IFG, ITG, and hippocampus supports short-term retention of auditory sequences; PAC strength decodes correct/incorrect memory trials; positively correlated with individual STM performance | ML decoding of correct/incorrect trials; PAC strength ∝ individual performance | **f19_fast_binding: theta-gamma PAC mechanism for hippocampal auditory binding; consolidation_str: cross-frequency coupling as binding mechanism** |
| 10 | **Liu et al. 2024** | EEG-fMRI | 33 | Memory replay events trigger heightened hippocampal and mPFC activation; replay strengthens hippocampus-DMN functional connectivity; post-learning rest shows stronger hippocampal-entorhinal connectivity | Replay-aligned fMRI beta significant, hippocampus-EC connectivity increase post-learning | **f21_cortical_storage: hippocampal replay drives mPFC consolidation; consolidation_str: replay-triggered hippocampal-cortical transfer** |
| 11 | **Sikka et al. 2015** | fMRI | 40 (20 young, 20 old) | Familiar melody recognition activates R-STG, bilateral IFG, L-supramarginal; age-related shift from medial temporal lobe (hippocampus) to prefrontal cortex for musical semantic memory | ROI analysis, p < 0.05 FWE-corrected | **f21_cortical_storage: cortical consolidation of musical memories; age-related hippocampal → cortical shift validates consolidation trajectory** |
| 12 | **Biau et al. 2025** | MEG | 23 | Neocortical and hippocampal theta oscillations track audiovisual integration; theta synchrony determines hippocampal memory encoding via LTP/LTD; theta reinstatement during memory recall disrupted by encoding asynchrony | Theta power difference sync > async, p < 0.05 cluster-corrected | **f19_fast_binding: theta oscillation as hippocampal binding mechanism; retrieval_dynamics: theta reinstatement during retrieval** |
| 13 | **Hippocampal music encoding (2023)** | fMRI | 84 | Hippocampus, STS multimodal integration during music | d = 0.17, p < 0.0001 | **hippocampal binding** |
| 14 | **Neonatal music review (2023)** | Scoping review | 1500 | Music affects hippocampus and amygdala | scoping | **early binding** |

### 3.2 The Temporal Story: Hippocampal-Cortical Dynamics

```
COMPLETE TEMPORAL PROFILE OF HIPPOCAMPAL-CORTICAL MEMORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1: FAST BINDING (continuous, <1s, H16 window)
─────────────────────────────────────────────────────
Hippocampus receives auditory input via entorhinal cortex.
Rapid feature binding: pitch × timbre × temporal context.
High spectral flux triggers episodic boundary detection.
R³ input: Consonance [0:7] + Interactions [25:49]

Phase 2: EPISODIC SEGMENTATION (0.5-2s, H16 window)
────────────────────────────────────────────────────
Event boundaries detected at points of high spectral flux.
Each segment = distinct episodic trace in hippocampus.
R³[21] spectral_flux + R³[22] entropy signal boundaries.
encoding_state activates.

Phase 3: HIPPOCAMPAL CONSOLIDATION (2-5s, H20 window)
─────────────────────────────────────────────────────
Hippocampal trace stabilizes via replay within binding window.
Cross-feature interactions (R³[25:49]) strengthen associations.
Binding strength correlates with consonance (coherent signal).

Phase 4: CORTICAL TRANSFER (5-36s, H20→H24 window)
───────────────────────────────────────────────────
Hippocampal replay drives gradual cortical storage.
mPFC receives schema-consistent patterns for long-term integration.
PCC supports episodic recollection during active listening.
retrieval_dynamics produces cortical storage signal.

Phase 5: LONG-TERM STORAGE (36s+, H24 window)
──────────────────────────────────────────────
Cortical networks (mPFC, PCC) hold consolidated musical patterns.
Retrieval cue (partial melody) triggers hippocampal pattern completion.
Cortex fills in stored detail (full harmonic context, timbral quality).
This is how familiar melodies can be recognized after decades.
```

### 3.3 Effect Size Summary

```
Evidence Base: β-tier (integrative), 70-90% confidence
Total Papers: 14 (5 fMRI, 1 SEEG, 2 MEG, 1 EEG-fMRI, 2 review, 2 computational, 1 scoping)
Primary Evidence: beta = -0.140 [CI -0.238, -0.041] (Cheung 2019, hippocampal uncertainty×surprise)
 d = 0.17 [p < 0.0001] (hippocampal music encoding 2023)
 PAC strength ∝ individual STM performance (Borderie 2024, intracranial)
Supporting Evidence: Hippocampal replay → mPFC/DMN connectivity (Liu 2024, N=33)
 Tonal recognition → hippocampus + cingulate (Fernandez-Rubio 2022, N=71)
 Age-related hippocampal → cortical shift for music memory (Sikka 2015, N=40)
 Theta reinstatement during memory recall (Biau 2025, N=23)
Heterogeneity: Low-moderate (multiple methods converge on hippocampal role)
Quality Assessment: Strong — 5 direct imaging studies + intracranial SEEG + 2 reviews
```

---

## 4. R³ Input Mapping: What HCMC Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | HCMC Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Binding quality (inverse) | Rough = incoherent = weak binding |
| **A: Consonance** | [1] | sethares_dissonance | Encoding difficulty | Dissonant = harder to bind |
| **A: Consonance** | [3] | stumpf_fusion | Binding strength proxy | High fusion = coherent trace |
| **A: Consonance** | [4] | sensory_pleasantness | Encoding valence | Pleasant = stronger encoding |
| **A: Consonance** | [5] | harmonicity | Harmonic template match | Cortical pattern recognition |
| **A: Consonance** | [6] | spectral_regularity | Pattern predictability | Regular = easier consolidation |
| **B: Energy** | [7] | amplitude | Encoding salience | Louder = stronger trace |
| **B: Energy** | [8] | rms_energy | Energy level | Sustained energy = ongoing encoding |
| **B: Energy** | [10] | loudness | Arousal correlate | Arousal modulates encoding strength |
| **B: Energy** | [11] | onset_strength | Event boundary marker | Onsets trigger episodic segmentation |
| **C: Timbre** | [12] | warmth | Cortical template cue | Familiar timbre = retrieval trigger |
| **C: Timbre** | [14] | tonalness | Melodic encoding | Tonal content = hippocampal trace |
| **D: Change** | [21] | spectral_flux | Segmentation trigger | High flux = event boundary |
| **D: Change** | [22] | entropy | Pattern complexity | Encoding difficulty proxy |
| **E: Interactions** | [25:33] | x_l0l5 (Energy×Consonance) | Fast binding coupling | Cross-feature hippocampal trace |
| **E: Interactions** | [33:41] | x_l4l5 (Derivatives×Consonance) | Temporal encoding | Change × consonance = encoding signal |
| **E: Interactions** | [41:49] | x_l5l7 (Consonance×Timbre) | Cortical storage pattern | Consonance-timbre = long-term template |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | HCMC Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **I: Information** | [92] | predictive_entropy | Encoding strength modulator — high PE = stronger hippocampal trace | Cheung et al. 2019: prediction error drives hippocampal encoding |
| **I: Information** | [88] | harmonic_entropy | Chord-level encoding complexity — harmonic surprise triggers binding | Harrison & Pearce 2020 |
| **I: Information** | [87] | melodic_entropy | Note-level encoding difficulty — information content per event | Pearce 2005: IDyOM information content |

**Rationale**: HCMC models hippocampal-cortical memory encoding and consolidation. The Information group provides direct measures of encoding difficulty: predictive entropy quantifies how surprising each moment is (high PE = stronger hippocampal trace formation per Cheung et al. 2019), harmonic entropy measures chord-level unpredictability driving binding operations, and melodic entropy provides note-level information content that modulates encoding strength.

> **Code impact**: These features are doc-only until Phase 5 wiring. No changes to `hcmc.py`.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[3] stumpf_fusion ──────────► Binding coherence (hippocampal)
 High fusion = strong, coherent trace
 Math: binding ∝ stumpf × mean(x_l0l5)

R³[21] spectral_flux ─────────► Event boundary detection
 High flux = episodic segmentation point
 This is the HCMC segmentation trigger

R³[25:33] x_l0l5 ─────────────► Fast hippocampal binding
 Energy × Consonance = initial trace
 Math: encoding = σ(x_l0l5 · stumpf)

R³[41:49] x_l5l7 ─────────────► Cortical long-term storage
 Consonance × Timbre = stable template
 Math: storage = σ(x_l5l7 · harmonicity)

R³[33:41] x_l4l5 ─────────────► Temporal encoding dynamics
 Derivative × Consonance = encoding rate
 Rapid changes trigger stronger encoding

R³[22] entropy ────────────────► Encoding difficulty
 Low entropy = predictable = easier storage
 High entropy = complex = stronger encoding effort
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

HCMC requires H³ features at three horizons: H16 (1s), H20 (5s), H24 (36s).

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 3 | stumpf_fusion | 16 | M1 (mean) | L2 (bidirectional) | Binding coherence at 1s |
| 3 | stumpf_fusion | 20 | M1 (mean) | L0 (forward) | Binding stability over 5s |
| 3 | stumpf_fusion | 24 | M19 (stability) | L0 (forward) | Long-term binding stability |
| 3 | stumpf_fusion | 16 | M3 (std) | L2 (bidirectional) | Binding variability at 1s |
| 5 | harmonicity | 16 | M1 (mean) | L2 (bidirectional) | Harmonic template at 1s |
| 5 | harmonicity | 20 | M1 (mean) | L0 (forward) | Harmonic stability over 5s |
| 5 | harmonicity | 24 | M22 (autocorrelation) | L0 (forward) | Harmonic repetition detection |
| 11 | onset_strength | 16 | M1 (mean) | L2 (bidirectional) | Event density at 1s |
| 11 | onset_strength | 20 | M5 (range) | L0 (forward) | Onset dynamic range over 5s |
| 21 | spectral_flux | 16 | M1 (mean) | L2 (bidirectional) | Current segmentation rate |
| 21 | spectral_flux | 20 | M5 (range) | L0 (forward) | Flux dynamic range over 5s |
| 21 | spectral_flux | 16 | M3 (std) | L2 (bidirectional) | Flux variability at 1s |
| 22 | entropy | 16 | M1 (mean) | L2 (bidirectional) | Current pattern complexity |
| 22 | entropy | 20 | M13 (entropy) | L0 (forward) | Entropy of entropy over 5s |
| 22 | entropy | 24 | M19 (stability) | L0 (forward) | Pattern stability over 36s |
| 10 | loudness | 16 | M1 (mean) | L2 (bidirectional) | Encoding salience at 1s |
| 10 | loudness | 20 | M1 (mean) | L0 (forward) | Average salience over 5s |
| 10 | loudness | 24 | M3 (std) | L0 (forward) | Salience variability over 36s |
| 7 | amplitude | 16 | M1 (mean) | L2 (bidirectional) | Energy level at 1s |
| 7 | amplitude | 20 | M5 (range) | L0 (forward) | Energy dynamic range over 5s |
| 14 | tonalness | 16 | M1 (mean) | L2 (bidirectional) | Melodic content at 1s |
| 14 | tonalness | 20 | M22 (autocorrelation) | L0 (forward) | Tonal repetition over 5s |

**v1 demand**: 22 tuples

#### R³ v2 Projected Expansion

HCMC projected v2 from I (Information) group, aligned with corresponding H³ horizons (H16, H20, H24).

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 88 | harmonic_entropy | I | 16 | M0 (value) | L2 | Current harmonic uncertainty for encoding difficulty |
| 88 | harmonic_entropy | I | 20 | M0 (value) | L0 | Harmonic entropy state over consolidation |
| 88 | harmonic_entropy | I | 20 | M1 (mean) | L0 | Average harmonic complexity over 5s |
| 88 | harmonic_entropy | I | 24 | M1 (mean) | L0 | Long-term harmonic predictability |
| 92 | predictive_entropy | I | 16 | M0 (value) | L2 | Current prediction error for fast binding |
| 92 | predictive_entropy | I | 20 | M0 (value) | L0 | Prediction error over consolidation window |
| 92 | predictive_entropy | I | 24 | M18 (trend) | L0 | Long-term prediction error trajectory |

**v2 projected**: 7 tuples
**Total projected**: 29 tuples of 294,912 theoretical = 0.0098%

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
HCMC OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
Manifold range: IMU HCMC [316:327]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EPISODIC MEMORY FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0 │ f19_fast_binding │ [0, 1] │ Hippocampal initial encoding.
 │ │ │ CA3 autoassociative binding of features.
 │ │ │ f19 = σ(0.35 · x_l0l5.mean · encoding.mean
 │ │ │ + 0.35 · stumpf · encoding.mean
 │ │ │ + 0.30 · onset_str · loudness)
────┼───────────────────┼────────┼────────────────────────────────────────────
 1 │ f20_episodic_seg │ [0, 1] │ Event boundary detection.
 │ │ │ Hippocampal segmentation at flux boundaries.
 │ │ │ f20 = σ(0.40 · flux · encoding.mean
 │ │ │ + 0.30 · entropy · flux
 │ │ │ + 0.30 · onset_str · flux)
────┼───────────────────┼────────┼────────────────────────────────────────────
 2 │ f21_cortical_stor │ [0, 1] │ Long-term cortical pattern storage.
 │ │ │ mPFC + PCC consolidation.
 │ │ │ f21 = σ(0.35 · x_l5l7.mean · retrieval.mean
 │ │ │ + 0.35 · harmonicity · familiar.mean
 │ │ │ + 0.30 · (1 - entropy) · tonalness)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 3 │ consolidation_str │ [0, 1] │ Hippocampal → cortical transfer strength.
 │ │ │ f(Encoding_Strength × Pattern_Stability)
 │ │ │ × stumpf_fusion
────┼───────────────────┼────────┼────────────────────────────────────────────
 4 │ encoding_rate │ [0, 1] │ Rate of new episodic trace formation.
 │ │ │ σ(0.35 · flux + 0.35 · onset_str
 │ │ │ + 0.30 · loudness)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 5 │ binding_state │ [0, 1] │ Current hippocampal binding activation.
 │ │ │ encoding_state aggregation.
────┼───────────────────┼────────┼────────────────────────────────────────────
 6 │ segmentation_st │ [0, 1] │ Current episodic segmentation state.
 │ │ │ flux × entropy aggregation.
────┼───────────────────┼────────┼────────────────────────────────────────────
 7 │ storage_state │ [0, 1] │ Current cortical storage activation.
 │ │ │ retrieval_dynamics × x_l5l7.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 8 │ consolidation_fc │ [0, 1] │ Consolidation prediction (5-36s ahead).
 │ │ │ Hippocampal replay trajectory.
────┼───────────────────┼────────┼────────────────────────────────────────────
 9 │ retrieval_fc │ [0, 1] │ Retrieval probability prediction (1-5s ahead).
 │ │ │ Pattern completion trajectory.
────┼───────────────────┼────────┼────────────────────────────────────────────
10 │ pattern_compl_fc │ [0, 1] │ Pattern completion prediction (0.5-2s ahead).
 │ │ │ Hippocampal cue → cortical reconstruction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Hippocampal-Cortical Consolidation Function

```
Consolidation(music) = f(Encoding_Strength × Pattern_Stability × Time)

Encoding_Strength = encoding_state.mean() × binding_coherence
Pattern_Stability = familiarity_proxy.mean() × (1 - entropy)
Cortical_Storage = retrieval_dynamics.mean() × cortical_template

where:
 binding_coherence = R³.stumpf_fusion[3] × mean(R³.x_l0l5[25:33])
 cortical_template = R³.harmonicity[5] × mean(R³.x_l5l7[41:49])
 entropy = R³.entropy[22]

Temporal dynamics:
 dConsolidation/dt = α · (Encoding - Consolidation) + β · Pattern_Stability
 where α = hippocampal replay rate, β = cortical integration rate
```

### 7.2 Feature Formulas

All formulas satisfy: for `sigmoid(sum(wi * gi))`, `sum(|wi|) <= 1.0`.

```python
# f19: Fast Hippocampal Binding
# Coefficients: |0.35| + |0.35| + |0.30| = 1.00 <= 1.0
 + 0.30 * R3.onset_strength[11] * R3.loudness[10])

# f20: Episodic Segmentation
# Coefficients: |0.40| + |0.30| + |0.30| = 1.00 <= 1.0
 + 0.30 * R3.entropy[22] * R3.spectral_flux[21]
 + 0.30 * R3.onset_strength[11] * R3.spectral_flux[21])

# f21: Cortical Storage
# Coefficients: |0.35| + |0.35| + |0.30| = 1.00 <= 1.0
 + 0.30 * (1.0 - R3.entropy[22]) * R3.tonalness[14])
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | HCMC Function | Key Citation |
|--------|-----------------|----------|---------------|---------------|--------------|
| **Hippocampus** | +/-20, -24, -12 | 88 | Direct (fMRI, SEEG, MEG) | Fast binding, pattern completion, theta-gamma PAC, sequence uncertainty encoding | Cheung 2019, Borderie 2024, Fernandez-Rubio 2022, Billig 2022 |
| **Entorhinal Cortex** | +/-24, -12, -24 | — | Direct (EEG-fMRI) | Sensory input gateway to hippocampus; post-learning replay strengthens HC-EC connectivity | Liu 2024, Billig 2022 (trisynaptic pathway) |
| **mPFC** | 0, 52, 12 | 14 | Direct (fMRI, EEG-fMRI) | Schema memory, cortical consolidation; replay-triggered activation; hippocampus-DMN connectivity hub | Liu 2024, Sikka 2015 |
| **PCC / Cingulate Gyrus** | 0, -52, 26 | — | Direct (MEG) | Episodic recollection, cortical storage; tonal sequence recognition memory | Fernandez-Rubio 2022 (middle/anterior cingulate for tonal recognition) |
| **Auditory Cortex (A1/STG)** | +/-48, -22, 8 | 18 | Direct (fMRI) | Sensory encoding input; uncertainty × surprise interaction modulates AC BOLD | Cheung 2019 (beta = -0.182, p = 0.0001 L-AC) |
| **Amygdala (anterior)** | +/-20, -6, -16 | — | Direct (fMRI) | Emotional modulation of hippocampal encoding; uncertainty × surprise interaction | Cheung 2019 (bilateral amygdala/hippocampus ROI) |
| **Parahippocampal Gyrus** | -28, -36, -8 | — | Direct (MEG) | Tonal sequence recognition memory; activated during 4th tone of memorized tonal sequences | Fernandez-Rubio 2022 (left parahippocampal, MCS p < 0.001) |

---

## 9. Cross-Unit Pathways

### 9.1 HCMC ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ HCMC INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ INTRA-UNIT (IMU): │
│ MEAMN ──────► HCMC │
│ │ └── MEAMN retrieval triggers HCMC pattern completion │
│ │ │
│ HCMC ───────► MEAMN │
│ │ └── HCMC encoding provides traces for MEAMN retrieval │
│ │ │
│ HCMC ───────► MMP (Musical Mnemonic Preservation) │
│ │ └── HCMC cortical storage explains MMP preservation │
│ │ │
│ HCMC ───────► PMIM (Predictive Memory Integration) │
│ │ └── HCMC stores the templates PMIM predicts against │
│ │ │
│ HCMC ───────► CDEM (Context-Dependent Emotional Memory) │
│ └── HCMC episodic traces carry contextual tags │
│ │
│ NO CROSS-UNIT PATHWAYS — HCMC uses memory-encoding mechanism only. │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Brain Pathway Cross-References

HCMC reads from the unified Brain (26D) for shared state:

| Brain Dimension | Index (MI-space) | HCMC Role |
|-----------------|-------------------|-----------|
| arousal | [177] | Arousal modulates encoding strength |
| prediction_error | [178] | Surprise modulates hippocampal binding |
| emotional_momentum | [180] | Sustained emotion enhances consolidation |

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Hippocampal lesions** | Should severely impair new musical memory encoding | **Confirmed** via neurological patients |
| **Cortical lesions (mPFC)** | Should impair long-term storage but spare encoding | **Partially confirmed** |
| **Fast binding temporal constraint** | Binding should operate at <1s timescale | **Confirmed** via ERP studies |
| **Event boundary effect** | High spectral flux should predict episodic segmentation | **Confirmed** via event segmentation theory |
| **Consolidation time course** | Hippocampal replay should drive cortical transfer over seconds-hours | **Confirmed** via sharp-wave ripple studies |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class HCMC(BaseModel):
 """Hippocampal-Cortical Memory Circuit.

 Output: 11D per frame.
 Zero learned parameters — all deterministic.
 """
 NAME = "HCMC"
 UNIT = "IMU"
 TIER = "β4"
 OUTPUT_DIM = 11
 MANIFOLD_RANGE = (316, 327) # IMU HCMC [316:327]

 # Coefficient constraints: for σ(Σ wᵢ·gᵢ), Σ|wᵢ| ≤ 1.0
 # f19: 0.35 + 0.35 + 0.30 = 1.00
 # f20: 0.40 + 0.30 + 0.30 = 1.00
 # f21: 0.35 + 0.35 + 0.30 = 1.00
 # encoding_rate: 0.35 + 0.35 + 0.30 = 1.00

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """22 tuples for HCMC computation."""
 return [
 # (r3_idx, horizon, morph, law)
 # --- stumpf_fusion: binding coherence ---
 (3, 16, 1, 2), # stumpf_fusion, 1s, mean, bidirectional
 (3, 20, 1, 0), # stumpf_fusion, 5s, mean, forward
 (3, 24, 19, 0), # stumpf_fusion, 36s, stability, forward
 (3, 16, 3, 2), # stumpf_fusion, 1s, std, bidirectional
 # --- harmonicity: cortical template ---
 (5, 16, 1, 2), # harmonicity, 1s, mean, bidirectional
 (5, 20, 1, 0), # harmonicity, 5s, mean, forward
 (5, 24, 22, 0), # harmonicity, 36s, autocorrelation, forward
 # --- onset_strength: event boundaries ---
 (11, 16, 1, 2), # onset_strength, 1s, mean, bidirectional
 (11, 20, 5, 0), # onset_strength, 5s, range, forward
 # --- spectral_flux: segmentation trigger ---
 (21, 16, 1, 2), # spectral_flux, 1s, mean, bidirectional
 (21, 20, 5, 0), # spectral_flux, 5s, range, forward
 (21, 16, 3, 2), # spectral_flux, 1s, std, bidirectional
 # --- entropy: encoding complexity ---
 (22, 16, 1, 2), # entropy, 1s, mean, bidirectional
 (22, 20, 13, 0), # entropy, 5s, entropy, forward
 (22, 24, 19, 0), # entropy, 36s, stability, forward
 # --- loudness: encoding salience ---
 (10, 16, 1, 2), # loudness, 1s, mean, bidirectional
 (10, 20, 1, 0), # loudness, 5s, mean, forward
 (10, 24, 3, 0), # loudness, 36s, std, forward
 # --- amplitude: energy ---
 (7, 16, 1, 2), # amplitude, 1s, mean, bidirectional
 (7, 20, 5, 0), # amplitude, 5s, range, forward
 # --- tonalness: melodic content ---
 (14, 16, 1, 2), # tonalness, 1s, mean, bidirectional
 (14, 20, 22, 0), # tonalness, 5s, autocorrelation, forward
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 """
 Compute HCMC 11D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
 r3: (B,T,49) raw R3 features

 Returns:
 (B,T,11) HCMC output
 """
 # R3 features
 stumpf = r3[..., 3:4] # [0, 1]
 harmonicity = r3[..., 5:6] # [0, 1]
 amplitude = r3[..., 7:8] # [0, 1]
 loudness = r3[..., 10:11] # [0, 1]
 onset_str = r3[..., 11:12] # [0, 1]
 tonalness = r3[..., 14:15] # [0, 1]
 flux = r3[..., 21:22] # [0, 1]
 entropy = r3[..., 22:23] # [0, 1]
 x_l0l5 = r3[..., 25:33] # (B, T, 8)
 x_l5l7 = r3[..., 41:49] # (B, T, 8)

 # ═══ LAYER E: Episodic features (3D) ═══

 # f19: Fast Hippocampal Binding
 # |0.35| + |0.35| + |0.30| = 1.00 <= 1.0
 f19 = torch.sigmoid(
 + 0.30 * onset_str * loudness
 )

 # f20: Episodic Segmentation
 # |0.40| + |0.30| + |0.30| = 1.00 <= 1.0
 f20 = torch.sigmoid(
 + 0.30 * entropy * flux
 + 0.30 * onset_str * flux
 )

 # f21: Cortical Storage
 # |0.35| + |0.35| + |0.30| = 1.00 <= 1.0
 f21 = torch.sigmoid(
 + 0.30 * (1.0 - entropy) * tonalness
 )

 # ═══ LAYER M: Mathematical (2D) ═══

 # Consolidation strength: encoding × retrieval × coherence
 consolidation_str = (
 * stumpf
 ).clamp(0, 1)

 # Encoding rate: event-driven encoding
 # |0.35| + |0.35| + |0.30| = 1.00 <= 1.0
 encoding_rate = torch.sigmoid(
 0.35 * flux + 0.35 * onset_str + 0.30 * loudness
 )

 # ═══ LAYER P: Present (3D) ═══
 segmentation_st = (flux * entropy).clamp(0, 1)
 storage_state = (
 * x_l5l7.mean(-1, keepdim=True)
 ).clamp(0, 1)

 # ═══ LAYER F: Future (3D) ═══
 consolidation_fc = self._predict_future(mem_encoding, h3_direct, window_h=24)
 retrieval_fc = self._predict_future(mem_retrieval, h3_direct, window_h=20)
 pattern_compl_fc = self._predict_future(mem_familiar, h3_direct, window_h=16)

 return torch.cat([
 f19, f20, f21, # E: 3D
 consolidation_str, encoding_rate, # M: 2D
 binding_state, segmentation_st, storage_state, # P: 3D
 consolidation_fc, retrieval_fc, pattern_compl_fc, # F: 3D
 ], dim=-1) # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 14 | 5 fMRI + 1 SEEG + 2 MEG + 1 EEG-fMRI + 2 review + 2 computational + 1 scoping |
| **Effect Sizes** | beta = -0.140 (Cheung 2019), d = 0.17 (hippocampal encoding 2023), PAC correlation (Borderie 2024) | Multiple direct imaging effect sizes |
| **Evidence Tier** | β (Integrative) — 70-90% confidence | Multi-factor integrative model |
| **Evidence Modality** | fMRI, SEEG, MEG, EEG-fMRI, computational, review | Strongly converging multimodal evidence |
| **Falsification Tests** | 5/5 (4 confirmed, 1 partial) | Good validity |
| **Brain Regions** | 7 | Hippocampus, EC, mPFC, PCC/Cingulate, AC/STG, Amygdala, Parahippocampal Gyrus |
| **R³ Features Used** | 38D of 49D | Comprehensive |
| **H³ Demand** | 22 tuples (0.95%) | Sparse, efficient |
| **Output Dimensions** | **11D** | 4-layer structure (3E+2M+3P+3F) |
| **Manifold Range** | IMU HCMC [316:327] | 11D allocated |

---

## 13. Scientific References

1. **Squire & Alvarez (1995)**. Memory consolidation and the medial temporal lobe: A simple network model. *PNAS*.
2. **McClelland, McNaughton & O'Reilly (1995)**. Why there are complementary learning systems in the hippocampus and neocortex. *Psychological Review*.
3. **Zacks, Speer, Swallow, Braver & Reynolds (2007)**. Event perception: A mind-brain perspective. *Psychological Bulletin*.
4. **Rolls (2013)**. A quantitative theory of the functions of the hippocampal CA3 network in memory. *Frontiers in Cellular Neuroscience*.
5. **Buzsaki (2015)**. Hippocampal sharp wave-ripple: A cognitive biomarker for episodic memory and planning. *Hippocampus*.
6. **Cheung, Harrison, Meyer, Pearce, Haynes & Koelsch (2019)**. Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. *Current Biology*, 29, 4084-4092. N=79 (39 beh + 40 fMRI). doi:10.1016/j.cub.2019.09.067.
7. **Billig, Lad, Sedley & Griffiths (2022)**. The hearing hippocampus. *Progress in Neurobiology*, 218, 102326. Review of hippocampal auditory processing across species. doi:10.1016/j.pneurobio.2022.102326.
8. **Fernandez-Rubio, Brattico, Kotz, Kringelbach, Vuust & Bonetti (2022)**. Magnetoencephalography recordings reveal the spatiotemporal dynamics of recognition memory for complex versus simple auditory sequences. *Communications Biology*, 5, 1272. N=71. doi:10.1038/s42003-022-04217-8.
9. **Borderie, Caclin, Lachaux, Perrone-Bertollotti, Hoyer, Kahane, Catenoix, Tillmann & Albouy (2024)**. Cross-frequency coupling in cortico-hippocampal networks supports the maintenance of sequential auditory information in short-term memory. *PLoS Biology*, 22(3), e3002512. SEEG intracranial recording. doi:10.1371/journal.pbio.3002512.
10. **Liu, Huang, Xiao, Yu, Luo, Xu, Qu, Dolan, Behrens (2024)**. Replay-triggered brain-wide activation in humans. *Nature Communications*, 15, 7185. N=33. EEG-fMRI simultaneous recording. doi:10.1038/s41467-024-51582-5.
11. **Sikka, Cuddy, Johnsrude & Vanstone (2015)**. An fMRI comparison of neural activity associated with recognition of familiar melodies in younger and older adults. *Frontiers in Neuroscience*, 9, 356. N=40. doi:10.3389/fnins.2015.00356.
12. **Biau, Wang, Park, Jensen & Hanslmayr (2025)**. Neocortical and hippocampal theta oscillations track audiovisual integration and replay of speech memories. *Journal of Neuroscience*, 45(21). N=23. doi:10.1523/JNEUROSCI.1797-24.2025.
13. **Hippocampal music encoding study (2023)**. Multimodal integration in STS and hippocampus. d = 0.17, n=84, p < 0.0001.
14. **Neonatal care music review (2023)**. Music affects hippocampus and amygdala in neonatal care. *Scoping review*, n=1500.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Fast binding | S⁰.X_L0L1 × HC⁰.BND | R³.x_l0l5 |
| Episodic segmentation | S⁰.L5.flux × HC⁰.SGM | R³.flux |
| Cortical storage | S⁰.X_L5L6 × HC⁰.HRM | R³.x_l5l7 |
| Demand format | HC⁰ EH/HM/HL tuples | H³ 4-tuples (sparse) |
| Total demand | 21/2304 = 0.91% | 22/2304 = 0.95% |

---

## 15. Doc-Code Mismatches (v2.1.0)

The following mismatches between this doc and `mi_beta/brain/units/imu/models/hcmc.py` were identified during the Phase 1 review. These are logged here for resolution in Phase 2 (code update).

| Aspect | Doc (v2.1.0) | Code (hcmc.py) | Severity |
|--------|-------------|----------------|----------|
| **LAYERS** | E: f19_fast_binding, f20_episodic_seg, f21_cortical_storage; M: consolidation_str, encoding_rate; P: binding_state, segmentation_st, storage_state; F: consolidation_fc, retrieval_fc, pattern_compl_fc | E: f01_encoding_strength, f02_consolidation_state (2D); M: hippocampal_binding, cortical_transfer, consolidation_index (3D); P: encoding_state, replay_activity, storage_phase (3D); F: consolidation_forecast, retrieval_readiness, decay_prediction (3D) | **High** — layer structure differs (doc 3E+2M+3P+3F vs code 2E+3M+3P+3F) |
| **h3_demand** | 22 tuples (stumpf, harmonicity, onset_strength, spectral_flux, entropy, loudness, amplitude, tonalness) | Empty tuple `()` | **High** — code has no H3 demand |
| **brain_regions** | 7 regions (Hippocampus, EC, mPFC, PCC, AC, Amygdala, Parahippocampal) | 3 regions (Hippocampus, Auditory Cortex, mPFC) — missing EC, PCC, Amygdala, Parahippocampal | **Medium** — code missing 4 regions |
| **dimension_names** | f19_fast_binding, f20_episodic_seg, f21_cortical_storage, consolidation_str, encoding_rate, binding_state, segmentation_st, storage_state, consolidation_fc, retrieval_fc, pattern_compl_fc | f01_encoding_strength, f02_consolidation_state, hippocampal_binding, cortical_transfer, consolidation_index, encoding_state, replay_activity, storage_phase, consolidation_forecast, retrieval_readiness, decay_prediction | **Medium** — all 11 names differ |
| **citations** | Squire 1995, McClelland 1995, Zacks 2007, Rolls 2013, Buzsaki 2015, Cheung 2019, Billig 2022, Fernandez-Rubio 2022, Borderie 2024, Liu 2024, Sikka 2015, Biau 2025 + 2 unverified | Watanabe 2008, Albouy 2017 (neither appears in doc evidence table) | **Medium** — code cites different papers |
| **FULL_NAME** | "Hippocampal-Cortical Memory Circuit" | "Hippocampal-Cortical Memory Consolidation" | **Low** — minor naming difference |
| **paper_count** | 14 | 4 | **Low** — code needs update |

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **11D**
**Evidence Tier**: **β (Integrative) — 70-90% confidence**
**Manifold Range**: IMU HCMC [316:327]
