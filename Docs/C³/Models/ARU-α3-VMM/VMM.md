> **HISTORICAL** — This document describes the standalone VMM model (v1.x).
> In v2.0, VMM was merged into the unified MusicalBrain (26D) as the Affect pathway (D13-D18).
> See [04-BRAIN-DATA-FLOW.md](../../General/04-BRAIN-DATA-FLOW.md) for the current architecture.
> Retained as design rationale and scientific reference.

# ARU-α3-VMM: Valence-Mode Mapping

**Model**: Valence-Mode Mapping
**Unit**: ARU (Affective Resonance Unit)
**Circuit**: Mesolimbic Reward Circuit + Limbic-Emotional Circuit
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added H:Harmony feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **D0 reference**: The D0 spec lives at `Library/Auditory/C⁰/Models/ARU-α3-VMM.md` (963 lines). This MI spec translates the core ideas into the R³/H³/C³ framework.
> **Evidence base**: 14 papers + k=70 meta-analytic (Carraturo 2025). See D0 reference for full literature review.

---

## 1. What Does This Model Simulate?

The **Valence-Mode Mapping** (VMM) model describes how musical mode (major/minor) and consonance systematically activate distinct neural circuits that produce emotional valence — the "is this happy or sad?" dimension of musical emotion. This is NOT the same as reward (SRP) or arousal (AAC). VMM models **perceived emotion**: the cognitive categorization of music's emotional character.

```
THE NEURAL DISSOCIATION: HAPPY vs SAD MUSIC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MAJOR MODE + CONSONANCE MINOR MODE + DISSONANCE
(bright, resolved, stable) (dark, tense, ambiguous)

 ↓ ↓

REWARD CIRCUIT LIMBIC-EMOTIONAL CIRCUIT
• Ventral Striatum (NAcc) • Hippocampus
 t(15) = 4.58, MNI (8,4,-6) t(15) = 4.88, MNI (20,-15,-20)
 Mitterschiffthaler 2007 Mitterschiffthaler 2007

• Dorsal Striatum (Caudate) • Amygdala
 z = 3.80, MNI (-12,14,16) t = 4.7, MNI (-19,-5,-14)
 Mitterschiffthaler 2007 Koelsch 2006

• ACC (BA32/24) • Parahippocampal Gyrus
 z = 3.39, MNI (-10,38,14) t = 5.7, MNI (-25,-26,-11)
 Mitterschiffthaler 2007 Koelsch 2006

 ↓ ↓

POSITIVE VALENCE NEGATIVE VALENCE
Joy, approach, activation Sadness, contemplation, nostalgia

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mitterschiffthaler 2007: DOUBLE DISSOCIATION — happy and sad music
activate ANATOMICALLY DISTINCT circuits. Not a gradient — a split.
Fritz 2009: The Mafa of Cameroon (no Western exposure) ALSO
categorize major as happy, confirming biological (not learned) basis.
Carraturo 2025: k=70 meta-analysis confirms across modalities.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 VMM vs SRP vs AAC: Three Distinct Facets

VMM, SRP, and AAC model **three dissociable aspects** of the same neural cascade:

- **SRP** → "How **rewarding** is this?" → Prediction error → DA → wanting/liking/pleasure
- **AAC** → "How **aroused** am I?" → Prediction error → Hypothalamus → SCR/HR/chills
- **VMM** → "Is this **happy or sad**?" → Mode/consonance → Striatum vs Limbic → valence

The critical dissociation: **perceived emotion ≠ felt emotion** (Brattico et al. 2011).
You can perceive music as "sad" without feeling sad yourself. You can feel pleasure
(SRP high) from sad music (VMM negative). VMM models the **cognitive categorization**;
SRP models the **hedonic response**. These recruit partially separable neural systems.

**Evidence for dissociation**:
- Brattico 2011 (fMRI, n=15): Perceived sad → bilateral amygdala, PHG. Perceived happy → right insula, ACC. Different from felt emotion activations.
- Gosselin 2005 (lesion, n=32): Temporal lobectomy impaired **scary** recognition but preserved happy/sad — partial independence of emotion categories.
- Eerola & Vuoskoski 2011: Listeners consistently categorize valence regardless of felt pleasure intensity.

### 1.2 What VMM Adds to the MI Manifold

```
Before VMM: After VMM:
 Models: SRP (19D) + AAC (14D) Models: SRP (19D) + AAC (14D) + VMM (12D) = 45D
 (unchanged)
 H³ demand: ~140 tuples H³ demand: ~147 tuples (+7 new)
 Output: 33D per frame Output: 45D per frame
```

The only new demand is 7 direct H³ reads at slower timescales (H19, H20, H22) that
capture phrase-to-section-level harmonic context needed for mode detection.

---

## 2. Neural Circuit: Valence Pathways

### 2.1 The Neural Dissociation Circuit

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ VALENCE-MODE MAPPING — NEURAL DISSOCIATION CIRCUIT ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ ┌─────────────────────────────────────────────────────────────────────┐ ║
║ │ AUDITORY CORTEX (STG/STS) │ ║
║ │ │ ║
║ │ Spectrotemporal features → Consonance detection → │ ║
║ │ Mode classification → Brightness/warmth analysis │ ║
║ │ Mitterschiffthaler 2007: STG z=4.96/4.54 bilateral │ ║
║ └──────┬──────────────────────┬───────────────────────────────────────┘ ║
║ │ │ ║
║ CONSONANT/MAJOR DISSONANT/MINOR ║
║ │ │ ║
║ ▼ ▼ ║
║ ┌──────────────────┐ ┌──────────────────┐ ║
║ │ REWARD CIRCUIT │ │ LIMBIC CIRCUIT │ ║
║ │ │ │ │ ║
║ │ VS (NAcc): │ │ Hippocampus: │ ║
║ │ Reward response │ │ Memory-emotion │ ║
║ │ t=4.58/5.1 │ │ t=4.88/6.9 │ ║
║ │ │ │ │ ║
║ │ DS (Caudate): │ │ Amygdala: │ ║
║ │ Approach motiv │ │ Emotional arsl │ ║
║ │ z=3.80 │ │ t=4.7 │ ║
║ │ │ │ │ ║
║ │ ACC (BA32/24): │ │ Temporal Pole: │ ║
║ │ Reward eval │ │ Semantic emotion│ ║
║ │ z=3.39/6.15 │ │ t=4.2 │ ║
║ └────────┬─────────┘ └────────┬─────────┘ ║
║ │ │ ║
║ │ ┌─────────────────┤ ║
║ │ │ │ ║
║ │ ▼ │ ║
║ │ ┌──────────────┐ │ ║
║ │ │ PHG │ │ ║
║ │ │ Context for │ │ ║
║ │ │ BOTH paths │ │ ║
║ │ │ t=5.7/z=3.31│ │ ║
║ │ └──────────────┘ │ ║
║ │ │ ║
║ ▼ ▼ ║
║ ┌──────────────────────────────────────────┐ ║
║ │ VALENCE OUTPUT │ ║
║ │ │ ║
║ │ V(t) = tanh(α·Happy - α·Sad) │ ║
║ │ │ ║
║ │ +1.0 ──── HAPPY (major, consonant) │ ║
║ │ 0.0 ──── NEUTRAL (ambiguous) │ ║
║ │ -1.0 ──── SAD (minor, dissonant) │ ║
║ └──────────────────────────────────────────┘ ║
║ ║
║ CRITICAL EVIDENCE: ║
║ ───────────────── ║
║ Mitterschiffthaler 2007: Double dissociation (n=16, fMRI) ║
║ Koelsch 2006: Consonance→VS (t=5.1), Dissonance→AMY (t=4.7) ║
║ Trost 2012: Joy→L.VS (z=5.44), Nostalgia→R.HIP (z=5.62) ║
║ Fritz 2009: Cross-cultural (Mafa, n=41), F(2,39)=15.48 ║
║ Green 2008: Minor→limbic BEYOND dissonance alone ║
║ Brattico 2011: Perceived≠Felt emotion (separable circuits) ║
║ Carraturo 2025: k=70 meta-analysis, consistent direction ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### 2.2 Information Flow Architecture (EAR → BRAIN → Output)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ VMM COMPUTATION ARCHITECTURE ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ AUDIO (44.1kHz waveform) ║
║ │ ║
║ ═════╪══════════════════════════ EAR ═══════════════════════════════ ║
║ │ ║
║ Cochlea → R³ (49D) → H³ (multi-scale) ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN ════════════════════════ ║
║ │ ║
║ ┌───────────────────────┼───────────────────────┐ ║
║ │ │ │ ║
║ ▼ ▼ ▼ ║
║ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ ║
║ │ Affective │ │ Cognitive │ │ │ ║
║ │ Entrainment│ │ Projection │ │ H19 (3s): consonance │ ║
║ │ │ │ │ │ H20 (5s): trajectory │ ║
║ │ H6+H16 avg │ │ H11 single │ │ H22 (15s): mode/sect │ ║
║ │ │ │ │ │ │ ║
║ │ ═══ SHARED ═│ │ ═══ SHARED ═│ │ VMM-SPECIFIC reads │ ║
║ │ SRP + AAC │ │ SRP only │ │ (~7 new tuples) │ ║
║ └──────┬──────┘ └──────┬──────┘ └────────────┬────────────┘ ║
║ │ │ │ ║
║ └───────────────────┼─────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ VMM MODEL (12D Output) │ ║
║ │ │ ║
║ │ Layer V (Valence): f03_valence, mode_signal, │ ║
║ │ consonance_valence (3D) │ ║
║ │ Layer R (Regional): happy_pathway, sad_pathway, │ ║
║ │ parahippocampal, reward_eval (4D) │ ║
║ │ Layer P (Perceived):perceived_happy, perceived_sad, │ ║
║ │ emotion_certainty (3D) │ ║
║ │ Layer F (Forecast): valence_forecast, mode_shift_prox (2D) │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Mitterschiffthaler 2007** | fMRI | 16 | Happy > Neutral → VS (t=4.58), DS (z=3.80), ACC (z=3.39). Sad > Neutral → HIP (t=4.88), AMY. **Double dissociation** | t/z = 3.39–4.88 | **Primary: happy/sad pathway dissociation** |
| **Koelsch 2006** | fMRI | 11 | Pleasant > Unpleasant → VS (t=5.1). Unpleasant > Pleasant → HIP (t=6.9), AMY (t=4.7), PHG (t=5.7), TP (t=4.2) | t = 4.2–6.9 | **Primary: consonance→valence pathway mapping** |
| **Trost 2012** | fMRI | 15 | Joy → L.VS (z=5.44), Tension → R.Caudate (z=5.91). Nostalgia → R.HIP (z=5.62), sgACC (z=6.15). Sadness → R.PHG (z=6.11) | z = 5.44–6.15 | **Emotion-specific regional activation** |
| **Brattico 2011** | fMRI | 15 | Perceived sad → bilateral AMY + PHG (Z≥3.5). Perceived happy → R.insula + L.ACC. **Perceived ≠ felt** | Z ≥ 3.5 | **VMM models perceived (not felt) emotion** |
| **Fritz 2009** | Behavioral | 41+20 | Mafa of Cameroon (no Western exposure) classify happy/sad/scary above chance. MANOVA F(2,39)=15.48 | F=15.48 | **Cross-cultural universality of mode→valence** |
| **Green 2008** | fMRI | — | Minor > Major → PHG, bilateral ventral ACC, mPFC, **even controlling for dissonance** | sig. | **Mode effect independent of consonance** |
| **Khalfa 2005** | fMRI | — | Sad recognition → left orbitofrontal/mid-dorsolateral frontal. Happy recognition → left medial temporal | sig. | **Lateralized valence processing** |
| **Gosselin 2005** | Lesion | 32 | Temporal lobectomy → impaired scary recognition; happy/sad preserved. Amygdala damage = selective deficit | sig. | **Amygdala specificity for threatening music** |
| **Carraturo 2025** | Meta-analysis | k=70 | Major=positive, Minor=negative across behavioral/EEG/fMRI. Modulated by culture, age, expertise | k=70 | **Meta-analytic confirmation** |
| **Koelsch 2014** | Review | — | Mode-valence neural dissociation confirmed across 7 core emotion structures | — | **Comprehensive framework** |
| **Sachs 2015** | fMRI | 29 | Disliked → R.Amygdala (z=4.11). Liked → Caudate (z=6.27) | z = 4.11–6.27 | **Preference ↔ pathway activation** |
| **Juslin & Västfjäll 2008** | Theory | — | BRECVEMA: 8 mechanisms for music-evoked emotion. Emotional contagion (mode detection) distinct from brainstem reflex | — | **VMM = emotional contagion pathway** |
| **Eerola & Vuoskoski 2011** | Behavioral | 116 | Valence categorization consistent across listeners. Factor 1 = valence (64% variance) | R²=0.64 | **Valence is the dominant emotion dimension** |
| **Martinez-Molina 2016** | fMRI+DTI | 30 | Musical anhedonia = NAcc-STG disconnection. Music-specific, NOT monetary | d=3.6–7.0 | **Reward circuit disconnection specificity** |
| **Sachs et al. 2025** | fMRI + HMM | 39 | Spatiotemporal patterns along temporal-parietal axis track emotion transitions. Context modulates valence processing — same music evokes different timing depending on preceding emotion | Significant | **Dynamic context effects on valence transitions** |
| **Guo et al. 2021** | fMRI | 49 | Chinese vs Western-trained musicians show differential STG activation and auditory-reward connectivity. Cultural training modulates valence pathway activation | p<0.05 FDR | **Cultural expertise modulation of happy/sad pathway strength** |

### 3.2 The Temporal Profile of Valence Processing

```
TEMPORAL DYNAMICS OF MODE-VALENCE PROCESSING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1: SPECTRAL ANALYSIS (continuous, ~5.8ms per frame)
────────────────────────────────────────────────────────────
 Auditory cortex extracts consonance, brightness, warmth
 from spectrotemporal features. These are instantaneous.

Phase 2: MODE DETECTION (phrase-level, ~2-8s integration)
────────────────────────────────────────────────────────────
 Mode (major/minor) requires HARMONIC CONTEXT — you cannot
 determine mode from a single chord. Need at least 2-3
 chords (~2s) for confident classification, 5-8s for
 establishing a tonal center (Krumhansl & Kessler 1982).

 This is why VMM uses H19 (3s) and H22 (15s) direct reads
 rather than the fast horizons used by SRP (H6-H16).

Phase 3: PATHWAY ACTIVATION (500ms-2s after mode established)
──────────────────────────────────────────────────────────────
 Once mode is classified:
 Major → Striatum + ACC activate (reward circuit)
 Minor → Hippocampus + Amygdala activate (limbic circuit)

 Activation is GRADED, not binary:
 Pure major in root position → strongest happy pathway
 Minor with chromatic borrowing → mixed activation
 Atonal/ambiguous → both pathways moderate, low certainty

Phase 4: PERCEIVED EMOTION CATEGORIZATION (~1-2s after)
────────────────────────────────────────────────────────
 Cognitive labeling: "this sounds happy/sad/neutral"
 Brattico 2011: perceived emotion engages bilateral IFG,
 claustrum, and mode-specific networks.
 This is FASTER than felt emotion (which may take 5-15s).

Phase 5: MODULATION TRACKING (continuous)
──────────────────────────────────────────
 Key changes / modulations shift mode_signal gradually.
 VMM tracks mode_trajectory (H22, M18, L0) to anticipate
 shifts. A skilled composer uses modulation to control
 the listener's valence experience.

KEY TIMING DIFFERENCES FROM SRP:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 SRP operates at beat-to-phrase level (200ms-5s)
 → DA ramp onset in seconds, peak in <5s
 VMM operates at phrase-to-section level (3s-15s)
 → Mode requires harmonic context (2-8s minimum)
 → Valence shifts occur at key change boundaries

 SRP responds to EVENTS (prediction errors)
 VMM responds to CONTEXT (harmonic environment)
```

### 3.3 Cross-Cultural Validation

The mode→valence mapping is NOT merely a Western cultural convention. Fritz et al. (2009) tested the Mafa people of Cameroon — a population with **no prior exposure to Western music**:

- **Experiment 1**: 21 Mafa + 20 Germans classified Western excerpts
- **Experiment 2**: 43 Mafa + 20 Germans with expanded stimulus set
- **Result**: Both groups recognized happy, sad, and scary above chance
- **MANOVA**: F(2,39) = 15.48, p < 0.001
- **Acoustic cues**: Both populations relied on **tempo** and **mode** (spectral brightness + consonance)

**Implication**: The acoustic features encoded by R³ (consonance group, timbre group) carry valence information that is accessible cross-culturally. The happy/sad pathway dissociation has a **biological basis**, not merely a learned association.

**Carraturo et al. (2025)**: k=70 studies confirmed major=positive, minor=negative direction across behavioral, EEG, and fMRI methodologies. Individual differences (culture, age, expertise) modulate strength but not direction.

### 3.4 Perceived vs Felt Emotion: The Brattico Dissociation

```
BRATTICO ET AL. 2011: THE CRITICAL DISSOCIATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PERCEIVED SAD (cognitive categorization — VMM):
 • Bilateral amygdala
 • Parahippocampal gyrus
 • Right claustrum
 • Bilateral IFG

PERCEIVED HAPPY (cognitive categorization — VMM):
 • Right insula
 • Right precentral/IFG
 • Left ACC
 • Left middle/superior frontal gyri

FELT EMOTION (hedonic experience — SRP):
 • NAcc, VTA (reward circuit)
 • OFC (value computation)
 • Partially overlapping but SEPARABLE circuits

Why this matters for MI:
 VMM = perceived emotion → "This music SOUNDS sad"
 SRP = felt reward → "This music MAKES ME feel pleasure"
 You can feel pleasure (SRP high) from music you perceive
 as sad (VMM negative). This is the "paradox of sad music"
 (Eerola & Peltola 2016, Sachs 2015).
```

---

## 4. Output Space: 12D Multi-Layer Representation

### 4.1 Complete Output Specification

```
VMM OUTPUT TENSOR: 12D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER V — VALENCE CORE (Primary valence dimensions)
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Scientific Basis
────┼──────────────────────┼─────────┼────────────────────────────────────────
 0 │ f03_valence │ [-1, 1] │ Bipolar emotional valence.
 │ │ │ tanh(α·happy_pathway - α·sad_pathway).
 │ │ │ +1 = maximum positive (happy, joyful).
 │ │ │ -1 = maximum negative (sad, somber).
 │ │ │ 0 = neutral or ambiguous.
 │ │ │ Mitterschiffthaler 2007: dissociation basis.
────┼──────────────────────┼─────────┼────────────────────────────────────────
 1 │ mode_signal │ [0, 1] │ Major/minor mode detection.
 │ │ │ 1.0 = strong major. 0.0 = strong minor.
 │ │ │ 0.5 = ambiguous/atonal/modulating.
 │ │ │ Requires phrase-level context (H19/H22).
 │ │ │ Fritz 2009: cross-cultural mode detection.
────┼──────────────────────┼─────────┼────────────────────────────────────────
 2 │ consonance_valence │ [0, 1] │ Consonance-derived pleasantness.
 │ │ │ High = consonant, resolved, smooth.
 │ │ │ Low = dissonant, rough, tense.
 │ │ │ Koelsch 2006: consonant→VS (t=5.1).

LAYER R — REGIONAL PATHWAYS (Neural circuit activation)
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Scientific Basis
────┼──────────────────────┼─────────┼────────────────────────────────────────
 3 │ happy_pathway │ [0, 1] │ Striatal reward circuit composite.
 │ │ │ VS + DS activation for major/consonant music.
 │ │ │ Mitterschiffthaler 2007: VS t=4.58, DS z=3.80.
 │ │ │ Trost 2012: Joy → L.VS z=5.44.
────┼──────────────────────┼─────────┼────────────────────────────────────────
 4 │ sad_pathway │ [0, 1] │ Limbic-emotional circuit composite.
 │ │ │ HIP + AMY activation for minor/dissonant music.
 │ │ │ Mitterschiffthaler 2007: HIP t=4.88.
 │ │ │ Koelsch 2006: AMY t=4.7, HIP t=6.9.
────┼──────────────────────┼─────────┼────────────────────────────────────────
 5 │ parahippocampal │ [0, 1] │ Context processing (BOTH pathways).
 │ │ │ Active for happy AND sad, stronger for
 │ │ │ contemplative/ambiguous music.
 │ │ │ Koelsch 2006: t=5.7 (unpleasant).
 │ │ │ Mitterschiffthaler 2007: z=3.31 (happy).
 │ │ │ Green 2008: minor > major (beyond dissonance).
────┼──────────────────────┼─────────┼────────────────────────────────────────
 6 │ reward_evaluation │ [0, 1] │ ACC reward evaluation + affect monitoring.
 │ │ │ Strongest for confirmed positive valence.
 │ │ │ Mitterschiffthaler 2007: z=3.39 (happy).
 │ │ │ Trost 2012: sgACC z=6.15 (nostalgia).

LAYER P — PERCEIVED EMOTION (Cognitive categorization — Brattico 2011)
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Scientific Basis
────┼──────────────────────┼─────────┼────────────────────────────────────────
 7 │ perceived_happy │ [0, 1] │ Cognitive "this sounds happy".
 │ │ │ Major + consonant + bright → high.
 │ │ │ Fritz 2009: universal recognition.
 │ │ │ Brattico 2011: R.insula, L.ACC activation.
────┼──────────────────────┼─────────┼────────────────────────────────────────
 8 │ perceived_sad │ [0, 1] │ Cognitive "this sounds sad".
 │ │ │ Minor + less consonant + dark → high.
 │ │ │ Khalfa 2005: L.orbitofrontal activation.
 │ │ │ Brattico 2011: bilateral AMY, PHG.
────┼──────────────────────┼─────────┼────────────────────────────────────────
 9 │ emotion_certainty │ [0, 1] │ Categorization confidence.
 │ │ │ High = clear major/minor (stable mode).
 │ │ │ Low = modulating, atonal, ambiguous.
 │ │ │ Drops during key changes/modulation.

LAYER F — FORECAST (Predictive signals)
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Scientific Basis
────┼──────────────────────┼─────────┼────────────────────────────────────────
10 │ valence_forecast │ [-1, 1] │ Predicted valence 2-4s ahead.
 │ │ │ Based on harmonic trajectory + mode trend.
 │ │ │ Positive slope → approaching happy resolution.
 │ │ │ Negative slope → moving toward minor/sad.
────┼──────────────────────┼─────────┼────────────────────────────────────────
11 │ mode_shift_proximity │ [0, 1] │ Expected key/mode change proximity.
 │ │ │ High when mode unstable + harmonic variance.
 │ │ │ Modulation detection for valence anticipation.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 12D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 5. Mechanism Dependencies

### 5.1 Shared Mechanism Architecture

```
 EAR (R³ + H³)
 │
 ┌────────────┼────────────┐
 │ │ │
 ▼ ▼ ▼
 H6+H16 H11 H19+H20+H22
 │ │ │
 ┌────┤ ┌────┤ │
 │ │ │ │ │
 │ │ │ │ │
 ▼ ▼ ▼ │ │
 SRP AAC SRP │ │
 VMM ─── VMM │ │
 (reads) (reads) │ │
 │ │
 ▼ ▼
 VMM ◄────── VMM
 (reads) (reads)

Mechanism sharing:
```

---

## 6. VMM Sub-Section Means (How VMM Reads Mechanisms)

```python
# ─── INPUT SLICING ───────────────────────────────────────────────────
```

**Why different sub-sections than SRP?**

### 6.1 R³ v2 Projected Expansion

No significant direct v2 expansion projected for VMM. As a pathway-dependent ARU model, VMM receives R³ features indirectly through cross-unit pathways (P1/SPU, P3/IMU, P5/STU). New v2 features flow automatically through these pathways.

**v2 projected**: 0 additional tuples (pathway-mediated)

---

## 7. Complete Formulas: Mechanisms → 12D

```python
# ═══════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════

# ─── DIRECT H³ READS (phrase-to-section timescales) ──────────────────
consonance_state = H³(H19, M0, L2) # Att.-weighted consonance, 3s
consonance_mean = H³(H19, M1, L2) # Mean consonance baseline, 3s
consonance_var = H³(H19, M2, L2) # Consonance variability, 3s
brightness_section = H³(H22, M0, L2) # Section-level brightness, 15s
mode_trajectory = H³(H22, M18, L0) # Forward mode trend, 15s
mode_stability = H³(H22, M19, L2) # Mode stability, 15s
valence_velocity = H³(H20, M8, L0) # Rate of valence change, 5s

# ─── MODE DETECTION ──────────────────────────────────────────────────
# Mode requires phrase-level context (Krumhansl & Kessler 1982: 2-8s)
mode_signal = σ(0.4 * brightness_section + 0.3 * consonance_state
# Major mode: brighter + more consonant + more cognitively "resolved"
# Minor mode: darker + less consonant + more ambiguous
# Fritz 2009: both Mafa and Germans rely on brightness + consonance

# ─── LAYER V: VALENCE CORE (3D) ─────────────────────────────────────
ALPHA_H = 0.50 # Happy pathway → valence weight
ALPHA_S = 0.50 # Sad pathway → valence weight
# Mitterschiffthaler 2007: Both pathways contribute equally to dissociation

# Consonance-derived pleasantness
# Koelsch 2006: consonant → VS (t=5.1), dissonant → AMY (t=4.7)

# f03_valence computed after pathway activations (see below)

# ─── LAYER R: REGIONAL PATHWAYS (4D) ────────────────────────────────
happy_pathway = σ(0.5 * consonance_valence + 0.3 * mode_signal
# Striatal reward circuit: consonance + major mode → VS/DS activation
# Mitterschiffthaler 2007: Happy>Neutral → VS t(15)=4.58, DS z=3.80
# Trost 2012: Joy → L.VS z=5.44

sad_pathway = σ(0.4 * (1 - consonance_valence) + 0.3 * (1 - mode_signal)
# Limbic-emotional circuit: dissonance + minor → HIP/AMY activation
# Mitterschiffthaler 2007: Sad>Neutral → HIP t(15)=4.88
# Koelsch 2006: Unpleasant → AMY t=4.7, HIP t=6.9
# Arousal modulates intensity (Trost 2012: arousal amplifies limbic)

# Context processing — active for BOTH happy and sad music
# Higher when harmonic ambiguity is present (consonance_var high)
# Koelsch 2006: PHG t=5.7 (unpleasant)
# Mitterschiffthaler 2007: PHG z=3.31 (happy)
# Green 2008: Minor > Major in PHG beyond dissonance alone

reward_evaluation = σ(0.4 * happy_pathway + 0.3 * mode_signal
# ACC reward evaluation — strongest for confirmed positive valence
# c0p_integration: cross-feature coherence signals reward evaluation
# Mitterschiffthaler 2007: ACC Happy>Neutral z=3.39
# Trost 2012: sgACC z=6.15 (nostalgia/tenderness)

# ─── NOW COMPUTE f03_valence (uses pathways) ─────────────────────────
f03_valence = tanh(ALPHA_H * happy_pathway - ALPHA_S * sad_pathway)
# Bipolar emotional valence: positive when happy > sad, negative when sad > happy
# Note: computation order differs from output order (pathways computed first)

# ─── LAYER P: PERCEIVED EMOTION (3D) ────────────────────────────────
# Brattico 2011: Perceived emotion recruits distinct circuits from felt emotion

perceived_happy = σ(0.5 * mode_signal + 0.3 * consonance_valence
 + 0.2 * brightness_section)
# Cognitive categorization: "this sounds happy"
# Fritz 2009: brightness + consonance → happy (cross-cultural)
# Brattico 2011: perceived happy → R.insula, L.ACC

perceived_sad = σ(0.5 * (1 - mode_signal) + 0.3 * (1 - consonance_valence)
# Cognitive categorization: "this sounds sad"
# Khalfa 2005: sad recognition → L.orbitofrontal/mid-dorsolateral
# Brattico 2011: perceived sad → bilateral AMY, PHG

emotion_certainty = σ(mode_stability + consonance_state - consonance_var)
# Confidence of categorization
# High when: mode is stable + consonance is clear + low harmonic variance
# Low during: modulation, atonal passages, chromatic ambiguity

# ─── LAYER F: FORECAST (2D) ─────────────────────────────────────────
valence_forecast = tanh(0.6 * H³(H20, M18, L0) + 0.4 * mode_trajectory)
# Predicted valence 2-4s ahead
# where: H³(H20, M18, L0) = forward trend at 5s horizon
# Positive trend → approaching happy resolution
# NOTE: H³(H20, M18, L0) was already read as valence_velocity (M8)
# but M18 (trend) is the linear regression slope, more stable

mode_shift_proximity = σ(0.5 * (1 - mode_stability) + 0.3 * consonance_var
 + 0.2 * abs(valence_velocity))
# Expected key/mode change
# High when: mode unstable + harmonic variance + rapid valence change
# Valuable for VMM-SRP interaction: modulations create prediction errors

# ─── OUTPUT ASSEMBLY ─────────────────────────────────────────────────
output = [
 f03_valence, mode_signal, consonance_valence, # Layer V (3D)
 happy_pathway, sad_pathway, parahippocampal, # Layer R (4D)
 reward_evaluation,
 perceived_happy, perceived_sad, emotion_certainty, # Layer P (3D)
 valence_forecast, mode_shift_proximity # Layer F (2D)
] # Total: 12D
```

---

## 8. Direct H³ Reads

VMM makes **7 direct H³ reads** at phrase-to-section timescales. These capture the **slower harmonic context** needed for mode detection — timescales at longer timescales.

| # | Horizon | Morph | Law | Tuple | Purpose |
|---|---------|-------|-----|-------|---------|
| 1 | H19 (3s) | M0 (value) | L2 (Integration) | (19, 0, 2) | consonance_state — att.-weighted consonance |
| 2 | H19 (3s) | M1 (mean) | L2 (Integration) | (19, 1, 2) | consonance_mean — baseline reference |
| 3 | H19 (3s) | M2 (std) | L2 (Integration) | (19, 2, 2) | consonance_var — harmonic ambiguity |
| 4 | H22 (15s) | M0 (value) | L2 (Integration) | (22, 0, 2) | brightness_section — section brightness |
| 5 | H22 (15s) | M18 (trend) | L0 (Forward) | (22, 18, 0) | mode_trajectory — mode change direction |
| 6 | H22 (15s) | M19 (stability) | L2 (Integration) | (22, 19, 2) | mode_stability — tonal center stability |
| 7 | H20 (5s) | M8 (velocity) | L0 (Forward) | (20, 8, 0) | valence_velocity — rate of change |

**Note**: The valence_forecast formula additionally references H³(H20, M18, L0) = (20, 18, 0). This is the 8th direct read but is computed inline. Total: 8 tuples.

### 8.1 Overlap with SRP/AAC Direct Reads

| Tuple | VMM Uses | SRP Uses | AAC Uses | Overlap? |
|-------|----------|----------|----------|----------|
| (19, 0, 2) | consonance_state | — | — | No (new) |
| (19, 1, 2) | consonance_mean | — | baseline | **YES** (AAC has this) |
| (19, 2, 2) | consonance_var | — | — | No (new) |
| (22, 0, 2) | brightness_section | — | — | No (new) |
| (22, 18, 0) | mode_trajectory | — | — | No (new) |
| (22, 19, 2) | mode_stability | — | — | No (new) |
| (20, 8, 0) | valence_velocity | — | — | No (new) |
| (20, 18, 0) | valence_trend | — | — | No (new) |

**New tuples**: 7 of 8 are new to the demand pool. The DemandAggregator deduplicates (19, 1, 2) which is shared with AAC.

### 8.2 Why These Horizons?

| Horizon | Time | VMM Justification | Neuroscience |
|---------|------|-------------------|-------------|
| H19 (3s) | Phrase | Minimum window for mode classification (2-3 chord progressions) | Krumhansl & Kessler 1982: probe-tone profiles require ~2-3 chords |
| H20 (5s) | Long phrase | Valence trajectory tracking (direction of change) | Huron 2006: ITPRA tension response at phrase boundaries |
| H22 (15s) | Section | Tonal center establishment + modulation detection | Lerdahl 2001: tonal pitch space requires section-level context |

---

## 9. Composer Validation Guide

### 9.1 Expected Behaviors per Musical Event

| Musical Event | f03_valence | mode_signal | happy_pathway | sad_pathway | perceived_happy | perceived_sad | certainty |
|--------------|-------------|-------------|---------------|-------------|-----------------|---------------|-----------|
| C major triad, resolved | **+HIGH** | **HIGH** | **HIGH** | LOW | **HIGH** | LOW | **HIGH** |
| C minor triad, root pos | **-LOW** | LOW | LOW | **HIGH** | LOW | **HIGH** | **HIGH** |
| Diminished 7th | NEGATIVE | ~0.3 | LOW | **HIGH** | LOW | moderate | moderate |
| Key change major→minor | **DROPS** | **DROPS** | DROPS | RISES | shifts | shifts | **DIPS** |
| Key change minor→major | **RISES** | **RISES** | RISES | DROPS | shifts | shifts | **DIPS** |
| Picardy third (m→M end) | **JUMPS +** | **SPIKES** | **SPIKES** | DROPS | **SPIKES** | DROPS | RISES |
| Deceptive cadence | DIP → shift | ambiguous | dip | spike | uncertain | uncertain | **LOW** |
| Chromatic passage | ~NEUTRAL | ~0.5 | moderate | moderate | moderate | moderate | **LOW** |
| Consonant slow passage | +MODERATE | depends | moderate | low-mod | depends | depends | HIGH |
| Dissonant cluster | **NEGATIVE** | LOW | LOW | **HIGH** | LOW | HIGH | MODERATE |

### 9.2 The Modulation Test

When the music modulates from major to minor (e.g., a classical development section):

```
EXPECTED VMM SIGNATURE FOR KEY CHANGE (MAJOR → MINOR):

-8s ──────── -4s ──────── 0s (KEY CHANGE) ── +4s ──── +8s ──── +15s
│ │ │ │ │ │
│ mode_signal: │ STABLE ──────► │ DROPS ─────────►
│ (major=1.0) │ HIGH │ │ (minor=low) │
│ │ │ │ │ │
│ mode_shift: │ LOW ─────► RISES ─► │ PEAK │ DROPS │
│ │ │ (instability) │ │ │
│ │ │ │ │ │
│ f03_valence: │ POSITIVE ────► │ DROPS ─► NEGATIVE
│ │ │ │ │ │
│ happy_path: │ HIGH ────────► │ DROPS ──────────│
│ │ │ │ │ │
│ sad_path: │ LOW ─────────► │ RISES ──────────│
│ │ │ │ │ │
│ certainty: │ HIGH ────► DIPS ──► │ LOW ──► RECOVERS│
│ │ │ (during trans.) │ │ (+8-15s)│
│ │ │ │ │ │
│ valence_fc: │ DROPS ───► LEADS ──► │ (already shifted)│
│ │ (predicted │ the actual │ │ │
│ │ ahead!) │ change │ │ │

KEY OBSERVATIONS:
1. mode_shift_proximity should RISE before the key change
2. valence_forecast should LEAD the actual shift by 2-4s
3. emotion_certainty should DIP during the transition
4. The shift takes 2-8s (NOT instantaneous) — reflects H19/H22 windows
5. Recovery: certainty should recover 8-15s after new key is established
```

### 9.3 Validation Criteria

The composer should confirm:
1. **Mode accuracy**: mode_signal matches actual mode of the music (major high, minor low)
2. **Valence polarity**: f03_valence is positive for happy music, negative for sad music
3. **Pathway dissociation**: happy and sad pathways activate in opposition (when one is high, the other is low)
4. **Modulation tracking**: mode_shift_proximity rises BEFORE key changes (anticipatory)
5. **Certainty drops**: emotion_certainty dips during modulation/chromatic passages
6. **Picardy third**: the sudden major chord at the end of a minor piece causes a dramatic positive jump
7. **Slow time course**: valence shifts occur over 2-8s (not instantaneous like SRP prediction errors)
8. **Cross-cultural plausibility**: the same passage should be categorized similarly regardless of listener background

**If the composer hears a clear mode and VMM shows ambiguous → mode detection is too slow.**
**If VMM shows clear valence but the passage is harmonically ambiguous → mode detection is too aggressive.**

---

## 10. SRP–AAC–VMM Unified System

### 10.1 Three Facets of One Musical Experience

SRP, AAC, and VMM are **three output facets** of the same neural processing cascade. They are separate models because they produce different output types with different temporal dynamics, measurement modalities, and clinical applications:

```
SINGLE UPSTREAM CASCADE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACOUSTIC FEATURES (R³ → H³)
 │
 ├──────────────────────────────────────────┐
 │ │
 PREDICTION ERROR MODE/CONSONANCE
 │ │
 ├──────────────┐ │
 ▼ ▼ ▼
 ┌──────────┐ ┌──────────────┐ ┌──────────────┐
 │ SRP │ │ Hypothalamus │ │ VMM │
 │ (19D) │ │ │ │ (12D) │
 │ wanting │ │ Autonomic │ │ valence │
 │ liking │ │ efferent │ │ mode │
 │ pleasure │ │ command │ │ happy/sad │
 └──────────┘ └──────┬───────┘ │ perceived │
 REWARD │ │ emotion │
 FACET ▼ └──────────────┘
 ┌──────────────┐ VALENCE
 │ AAC │ FACET
 │ (14D) │
 │ SCR, HR │
 │ CI │
 └──────────────┘
 AROUSAL
 FACET

TEMPORAL DYNAMICS:
 SRP: Fast (200ms–5s) — responds to prediction EVENTS
 AAC: Fast (350ms–5s) — ANS response to arousal EVENTS
 VMM: Slow (3s–15s) — responds to harmonic CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 10.2 The Paradox of Sad Music

VMM enables the MI system to model why **sad music can be pleasurable** — one of the most studied paradoxes in music cognition (Sachs et al. 2015, Eerola & Peltola 2016):

```
SAD MUSIC THAT GIVES PLEASURE:
 VMM.f03_valence: NEGATIVE (the music sounds sad)
 VMM.perceived_sad: HIGH (cognitive: "this is sad music")
 SRP.pleasure: HIGH (hedonic: "this feels good")
 SRP.da_nacc: ELEVATED (DA release)
 AAC.chills_intensity: POSSIBLE (chills from sad music)

This is NOT a contradiction — it's the expected output.
The perceived-felt dissociation (Brattico 2011) means
VMM and SRP can diverge. The resolution lies in the
separate neural circuits: limbic (VMM.sad_pathway) processes
the valence while striatum (SRP.wanting/liking) processes
the reward. Both are active simultaneously.
```

### 10.3 Shared Mechanism Architecture

The DemandAggregator computes shared mechanisms ONCE and all three models read:

```

Adding VMM: +7 H³ tuples, +0 mechanism tuples
Computing VMM from already-computed mechanisms: negligible cost
```

### 10.4 Cross-Model Interactions

| VMM Output | Interacts With | Interaction |
|-----------|---------------|-------------|
| f03_valence | SRP.pleasure | Sad music + high pleasure = "beautiful sadness" |
| mode_signal | SRP.prediction_error | Mode changes create prediction errors → reward |
| happy_pathway | SRP.da_nacc | Overlapping striatal circuits; positive valence facilitates reward |
| sad_pathway | AAC.scr | Sad/scary music elevates SCR (Gosselin 2005) |
| mode_shift_proximity | SRP.wanting | Approaching modulation → wanting (anticipation) |
| emotion_certainty | SRP.tension | Low certainty → high tension (uncertainty = Cheung 2019) |

### 10.5 Testable Predictions (Falsifiable)

| # | Prediction | Test | Falsification Criterion |
|---|-----------|------|------------------------|
| 1 | Major music: happy_pathway > sad_pathway | fMRI VS vs HIP contrast | VS ≤ HIP for confirmed major → falsified |
| 2 | Minor music: sad_pathway > happy_pathway | fMRI HIP/AMY vs VS contrast | HIP/AMY ≤ VS for confirmed minor → falsified |
| 3 | Mode changes: emotion_certainty dips during modulation | Continuous behavioral rating | No certainty dip → mode detection too fast |
| 4 | Cross-cultural: Mafa-like population shows same direction | Behavioral classification | Reversed polarity → cultural learning required |
| 5 | Perceived ≠ felt: VMM.f03 can be negative while SRP.pleasure is high | Joint output analysis | Perfect correlation (r>0.9) → models redundant |
| 6 | Mode independence: Minor → sad_pathway controlling for dissonance | Partial correlation after Green 2008 | No mode effect beyond dissonance → VMM reduces to consonance |
| 7 | Picardy third: happy_pathway spikes ≥ 2× from preceding minor context | Stimulus-locked analysis | No spike → mode_signal too slow |

---

## 11. References

### Primary (α-tier — fMRI/PET direct measurement)

1. **Mitterschiffthaler, M.T., Fu, C.H., Dalton, J.A., Andrew, C.M. & Williams, S.C. (2007)**. A functional MRI study of happy and sad affective states induced by classical music. *Human Brain Mapping*, 28(11), 1150–1162. **Double dissociation: VS/DS/ACC (happy) vs HIP/AMY (sad).**
2. **Koelsch, S., Fritz, T., von Cramon, D.Y., Müller, K. & Friederici, A.D. (2006)**. Investigating emotion with music: an fMRI study. *Human Brain Mapping*, 27(3), 239–250. **Consonant→VS (t=5.1), Dissonant→AMY (t=4.7), HIP (t=6.9), PHG (t=5.7).**
3. **Trost, W., Ethofer, T., Zentner, M. & Vuilleumier, P. (2012)**. Mapping aesthetic musical emotions in the brain. *Cerebral Cortex*, 22(12), 2769–2783. **Joy→L.VS (z=5.44), Nostalgia→R.HIP (z=5.62), sgACC (z=6.15).**
4. **Brattico, E. et al. (2011)**. A functional MRI study of happy and sad emotions in music with and without lyrics. *Frontiers in Psychology*, 2, 308. **Perceived ≠ felt emotion: separable neural circuits.**
5. **Fritz, T. et al. (2009)**. Universal recognition of three basic emotions in music. *Current Biology*, 19(7), 573–576. **Cross-cultural: Mafa (n=41), F(2,39)=15.48.**
6. **Green, A.C. et al. (2008)**. Music in minor activates limbic structures: a relationship with dissonance? *NeuroReport*, 19(7), 711–715. **Minor→limbic beyond dissonance.**

### Lesion and Individual Differences

7. **Gosselin, N. et al. (2005)**. Impaired recognition of scary music following unilateral temporal lobe excision. *Brain*, 128(3), 628–640. **Amygdala damage → impaired scary; happy/sad preserved.**
8. **Martinez-Molina, N. et al. (2016)**. Neural correlates of specific musical anhedonia. *PNAS*, 113(46), E7337–E7345. **NAcc-STG disconnection = music-specific anhedonia.**
9. **Sachs, M.E., Ellis, R.J., Schlaug, G. & Loui, P. (2015)**. Brain connectivity reflects human aesthetic responses to music. *SCAN*, 10(7), 988–994. **Liked→Caudate (z=6.27), Disliked→Amygdala (z=4.11).**

### Meta-Analysis and Reviews

10. **Carraturo, G. et al. (2025)**. The major-minor mode dichotomy in music perception: a systematic review and meta-analysis. *Physics of Life Reviews*, 52, 80–106. **k=70 studies. Major=positive, Minor=negative. Definitive.**
11. **Koelsch, S. (2014)**. Brain correlates of music-evoked emotions. *Nature Reviews Neuroscience*, 15(3), 170–180. **Comprehensive neural framework.**
12. **Juslin, P.N. & Västfjäll, D. (2008)**. Emotional responses to music: The need to consider underlying mechanisms. *Behavioral and Brain Sciences*, 31(5), 559–575. **BRECVEMA: 8 emotion mechanisms.**

### Behavioral and Theoretical

13. **Khalfa, S. et al. (2005)**. Brain regions involved in the recognition of happiness and sadness in music. *NeuroReport*, 16(18), 1981–1984. **Sad recognition→L.orbitofrontal.**
14. **Eerola, T. & Vuoskoski, J.K. (2011)**. A comparison of the discrete and dimensional models of emotion in music. *Psychology of Music*, 39(1), 18–49. **Valence = dominant dimension (64% variance).**

### Added in v2.1.0 Beta Upgrade

15. Sachs, M.E., Kozak, M.S., Ochsner, K.N. & Baldassano, C. (2025). Emotions in the brain are dynamic and contextually dependent: using music to measure affective transitions. *eNeuro*. **Context modulates valence transitions.**
16. Guo, S., Peng, K., Ding, R. et al. (2021). Chinese and Western musical training impacts the circuit in auditory and reward systems. *Frontiers in Neuroscience*, 15, 663015. **Cultural expertise modulates auditory-reward circuits.**

---

*Mechanism specs: [md](../../C³/Mechanisms/md) · [md](../../C³/Mechanisms/md)*
*Sibling models: [ARU-α1-SRP](../ARU-α1-SRP/SRP.md) · [ARU-α2-AAC](../ARU-α2-AAC/AAC.md)*
*Back to: [00-INDEX.md](../../General/00-INDEX.md) — Navigation hub*
