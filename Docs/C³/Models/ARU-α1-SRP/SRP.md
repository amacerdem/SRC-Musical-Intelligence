> **HISTORICAL** — This document describes the standalone SRP model (v1.x).
> In v2.0, SRP was merged into the unified MusicalBrain (26D) as the Reward pathway (D4-D12).
> See [04-BRAIN-DATA-FLOW.md](../../General/04-BRAIN-DATA-FLOW.md) for the current architecture.
> Retained as design rationale and scientific reference.

# ARU-α1-SRP: Complete Reverse Engineering

**Model**: Striatal Reward Pathway
**Unit**: ARU (Affective Resonance Unit)
**Circuit**: Mesolimbic Reward Circuit
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 5.2.0 (Phase 3E: R³ v2 expansion — added I:Information feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../Road-map/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.

---

## 1. What Does This Model Simulate?

The **Striatal Reward Pathway** (SRP) models how the human brain generates musical pleasure through dopamine release in the striatum. But "pleasure" is not a single thing — it decomposes into at least three independent neurochemical/psychological systems:

```
THE THREE FACES OF MUSICAL REWARD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WANTING (Incentive Salience)          LIKING (Hedonic Impact)
Neurotransmitter: DOPAMINE            Neurotransmitter: μ-OPIOID + DA
Brain region: Caudate nucleus         Brain region: NAcc shell hotspots
                (dorsal striatum)                    (ventral striatum)
Timing: BEFORE the event              Timing: AT the event
Duration: 2-30s ramp                  Duration: 1-5s burst
Function: "I want more of this"       Function: "This feels good"
Can exist WITHOUT liking              Can exist WITHOUT wanting

                    LEARNING (Prediction Error)
                    Neurotransmitter: DOPAMINE (phasic)
                    Brain region: VTA → NAcc/Caudate
                    Timing: ~50-110ms after event
                    Duration: <200ms burst
                    Function: "That was better/worse than expected"
                    Updates future predictions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Berridge & Robinson (1993, 2003, 2016): These are DISSOCIABLE systems.
You can "want" music you don't "like" (earworm you hate).
You can "like" music you didn't "want" (unexpected beauty).
You can "learn" without either wanting or liking (mere exposure).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 What Dopamine Actually Represents

Dopamine in the striatum during music listening is **NOT simply "pleasure"**. Deep research reveals it is a **composite signal** encoding:

1. **Reward Prediction Error** (Schultz 1997, 2016): δ(t) = R(t) + γV(t+1) - V(t)
   - Positive RPE → "better than expected" → phasic DA burst (14-30 Hz, <200ms)
   - Zero RPE → "exactly as predicted" → no change from baseline (~5 Hz tonic)
   - Negative RPE → "worse than expected" → DA dip below baseline

2. **Incentive Salience** (Berridge 2007): Motivational "wanting" signal
   - Computed **de novo** at moment of cue encounter: Wanting = f(learned_association, current_state)
   - DA-dependent: levodopa ↑ wanting, risperidone ↓ wanting (Ferreri 2019)
   - Can motivate approach behavior even without hedonic pleasure

3. **Anticipatory Value** (Howe et al. 2013): Ramping proximity signal
   - Gradual, quasi-hyperbolic DA increase as expected reward approaches
   - Scales with both **distance** and **magnitude** of expected reward
   - NOT linear — accelerates toward the target

4. **Possibly Direct Hedonic Modulation** (unique to abstract rewards like music)
   - Ferreri et al. (2019): Levodopa increased subjective pleasure ratings (Z=1.968, P<0.049)
   - For music (unlike food/drugs), DA may directly modulate hedonic experience
   - This challenges a strict wanting/liking dissociation for abstract cognitive rewards

The **pure hedonic "liking"** component is primarily mediated by the **μ-opioid system**:
- Nummenmaa et al. (2025): PET showed [¹¹C]carfentanil binding (μ-opioid activation) in ventral striatum and OFC during pleasurable music
- Mallik et al. (2017): Naltrexone (opioid antagonist) reduced emotional intensity of music
- Hedonic hotspots: NAcc shell, ventral pallidum, parabrachial nucleus (Berridge & Kringelbach 2008)

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The Full Striatal Reward Circuit for Music

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 STRIATAL REWARD PATHWAY — COMPLETE CIRCUIT                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    AUDITORY CORTEX (STG/STS)                        │    ║
║  │                                                                     │    ║
║  │  Core (A1)      Belt           Parabelt                             │    ║
║  │  BA 41          BA 42, 52      Anterior/posterior STG               │    ║
║  │  Spectrotemporal Feature extraction Pattern recognition             │    ║
║  └──────┬──────────────┬──────────────────┬────────────────────────────┘    ║
║         │              │                  │                                  ║
║         │   ┌──────────┘                  │                                  ║
║         │   │                             │                                  ║
║         ▼   ▼                             ▼                                  ║
║  ┌──────────────────┐          ┌────────────────────┐                       ║
║  │   FRONTAL CORTEX │          │     AMYGDALA       │                       ║
║  │                  │          │                    │                       ║
║  │  IFG (BA 44/45): │          │  Superficial:      │                       ║
║  │  Musical syntax,  │          │  Pleasant/unpleas. │                       ║
║  │  expectation      │          │  evaluation        │                       ║
║  │                  │          │                    │                       ║
║  │  dlPFC:          │          │  Laterobasal:      │                       ║
║  │  Working memory,  │          │  Salience,         │                       ║
║  │  prediction       │          │  uncertainty×      │                       ║
║  │                  │          │  surprise           │                       ║
║  │  vmPFC/OFC:      │          │  (Cheung 2019)     │                       ║
║  │  Reward value,    │          │                    │                       ║
║  │  evaluation       │          └─────────┬──────────┘                       ║
║  └────────┬─────────┘                     │                                  ║
║           │                               │                                  ║
║           │  ┌────────────────────────────┘                                  ║
║           │  │                                                               ║
║           ▼  ▼                                                               ║
║  ┌─────────────────────────────────────────────────────────┐                ║
║  │                    S T R I A T U M                       │                ║
║  │                                                         │                ║
║  │  ┌─────────────────────┐  ┌───────────────────────┐    │                ║
║  │  │  CAUDATE NUCLEUS    │  │  NUCLEUS ACCUMBENS    │    │                ║
║  │  │  (Dorsal Striatum)  │  │  (Ventral Striatum)   │    │                ║
║  │  │                     │  │                       │    │                ║
║  │  │  ANTICIPATION       │  │  CONSUMMATION         │    │                ║
║  │  │                     │  │                       │    │                ║
║  │  │  • Receives:        │  │  • Receives:          │    │                ║
║  │  │    PFC predictions  │  │    VTA DA burst       │    │                ║
║  │  │    Auditory patterns│  │    Auditory cortex    │    │                ║
║  │  │                     │  │    connectivity        │    │                ║
║  │  │  • Computes:        │  │                       │    │                ║
║  │  │    Proximity to     │  │  • Computes:          │    │                ║
║  │  │    expected reward  │  │    Hedonic evaluation  │    │                ║
║  │  │    (ramping DA)     │  │    (phasic DA + opioid)│    │                ║
║  │  │                     │  │                       │    │                ║
║  │  │  • Output:          │  │  • Output:            │    │                ║
║  │  │    WANTING signal   │  │    LIKING signal      │    │                ║
║  │  │    (r=0.71)         │  │    (r=0.84)           │    │                ║
║  │  └─────────────────────┘  └───────────────────────┘    │                ║
║  │                                                         │                ║
║  └──────────────────────────┬──────────────────────────────┘                ║
║                             │                                                ║
║                             │  ◄───── VTA (Ventral Tegmental Area)          ║
║                             │         Source of DA neurons                    ║
║                             │         Menon & Levitin 2005:                  ║
║                             │         VTA↔NAcc connectivity during           ║
║                             │         pleasant music listening               ║
║                             │                                                ║
║                             ▼                                                ║
║  ┌─────────────────────────────────────────────────────────┐                ║
║  │                  HIPPOCAMPUS                             │                ║
║  │                                                         │                ║
║  │  Uniquely activated by music (not money, not sex)       │                ║
║  │  (Koelsch 2014 meta-analysis)                           │                ║
║  │                                                         │                ║
║  │  Functions: Memory encoding, contextual association,    │                ║
║  │  familiarity signal, nostalgia pathway                  │                ║
║  └─────────────────────────────────────────────────────────┘                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Salimpoor 2013:  NAcc-STG connectivity PREDICTS reward value (Science)
Martinez-Molina 2016: Musical anhedonia = NAcc-STG DISCONNECTION (PNAS)
Mas-Herrero 2021: dlPFC TMS causally modulates NAcc reward (d=0.81)
Loui 2017:       NAcc-STG white matter tract integrity ↔ pleasure (r=0.61)

The auditory cortex → NAcc connection is THE critical link for music reward.
```

### 2.2 Information Flow Architecture (EAR → BRAIN → Output)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SRP COMPUTATION ARCHITECTURE                              ║
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
║  │  │CONSONANCE │ │ ENERGY  │ │ TIMBRE  │ │ SURPRISE │ │ X-INT  │ │        ║
║  │  │ 7D        │ │ 5D      │ │ 9D      │ │ 4D       │ │ 24D    │ │        ║
║  │  │           │ │         │ │         │ │          │ │        │ │        ║
║  │  │roughness  │ │ampli.   │ │warmth   │ │flux      │ │L0×L5   │ │        ║
║  │  │sethares   │ │vel_A    │ │sharpness│ │entropy   │ │L4×L5   │ │        ║
║  │  │helmholtz  │ │acc_A    │ │tonalness│ │flatness  │ │L5×L7   │ │        ║
║  │  │stumpf     │ │loudness │ │clarity  │ │concent.  │ │        │ │        ║
║  │  │pleasant.  │ │onset    │ │smooth.  │ │          │ │        │ │        ║
║  │  │inharm.    │ │         │ │autocorr.│ │          │ │        │ │        ║
║  │  │harm_dev   │ │         │ │trist1-3 │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         SRP Demand: 49D                            │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Beat ────┐ ┌── Phrase ──┐ ┌── Section ──┐ ┌── Struct. ──┐ │        ║
║  │  │ 200ms-1s   │ │ 2s-5s      │ │ 15s-36s     │ │ 200s-414s  │ │        ║
║  │  │ H6-H16     │ │ H18-H20    │ │ H22-H24     │ │ H26-H28    │ │        ║
║  │  │            │ │            │ │             │ │            │ │        ║
║  │  │ Huron P+R  │ │ Huron T    │ │ Salimpoor   │ │ Narrative  │ │        ║
║  │  │ (at event) │ │ (buildup)  │ │ (anticipn.) │ │ (arc)      │ │        ║
║  │  └──────┬─────┘ └──────┬─────┘ └──────┬──────┘ └──────┬─────┘ │        ║
║  │         │              │              │               │        │        ║
║  │         └──────────────┴──────────────┴───────────────┘        │        ║
║  │                         SRP Demand: ~124 of 2304 tuples         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Mesolimbic Circuit ════════    ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐                ║
║  │  AED (30D)      │ │  CPD (30D)      │ │  C0P (30D)      │                ║
║  │  Affective      │ │  Chills & Peak  │ │  Cognitive       │                ║
║  │  Entrainment    │ │  Detection      │ │  Projection      │                ║
║  │                 │ │                 │ │                 │                ║
║  │ Arousal [0:10]  │ │ Trigger [0:10]  │ │ Aggreg. [0:10]  │                ║
║  │ Expect. [10:20] │ │ Buildup [10:20] │ │ Cognit. [10:20] │                ║
║  │ Motor   [20:30] │ │ Peak    [20:30] │ │ Project.[20:30] │                ║
║  └────────┬────────┘ └────────┬────────┘ └────────┬────────┘                ║
║           │                   │                   │                          ║
║           └───────────────────┼───────────────────┘                          ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    SRP MODEL (19D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer N (Neurochemical):  da_caudate, da_nacc, opioid_proxy    │        ║
║  │  Layer C (Circuit):        vta_drive, stg_nacc, pred_error      │        ║
║  │  Layer P (Psychological):  wanting, liking, pleasure            │        ║
║  │  Layer T (Temporal/ITPRA): tension, pred_match, reaction, appr. │        ║
║  │  Layer M (Musical):        harm_tension, dyn_intensity, peak    │        ║
║  │  Layer F (Forecast):       reward_fc, chills_prox, resol_exp    │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation (Deep Research)

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Salimpoor 2011** | PET [¹¹C]raclopride | 8 | NAcc DA ↑ at consummation; Caudate DA ↑ at anticipation. ~3.7 chills per excerpt | r=0.84 (NAcc), r=0.71 (Caudate) | **Primary coefficients** β₁=0.84, β₂=0.71 |
| **Salimpoor 2013** | fMRI + auction | 19 | NAcc-STG connectivity predicts how much listeners would PAY for novel music | NAcc best predictor | **stg_nacc_coupling dimension** |
| **Cheung 2019** | ML + fMRI | 39 | Pleasure = nonlinear f(uncertainty, surprise). 80,000 chords analyzed | d=3.8-8.53 | **prediction_error: signed RPE** |
| **Ferreri 2019** | Pharmacology (blind) | 27 | Levodopa ↑ pleasure (Z=1.97, P<0.049), chills (Z=2.34, P<0.019), willingness to pay (Z=2.44, P=0.015). Risperidone blocks all | Causal evidence | **DA causally modulates BOTH wanting AND liking in music** |
| **Mas-Herrero 2021** | TMS + fMRI | 17 | dlPFC TMS causally modulates NAcc. Pre-experience NAcc → motivation (R²=0.47). Experience NAcc → pleasure (R²=0.44) | d=0.81 (pleasure), d=0.50 (wanting) | **Temporal dissociation: anticipation ≠ consummation** |
| **Martinez-Molina 2016** | fMRI + DTI | 15+15 | Musical anhedonia (~5% of population) = NAcc-STG disconnection. Music-specific, NOT monetary | d=3.6-7.0 | **STG→NAcc is THE critical link** |
| **Gold 2019** | fMRI + IDyOM | 20 | NAcc RPE-related activity. Listeners learned to find preferred endings. Music = neurobiological reward for learning | Significant | **prediction_error drives learning** |
| **Nummenmaa 2025** | PET [¹¹C]carfentanil | — | Pleasurable music activates μ-opioid receptors in ventral striatum and OFC. MOR availability in NAcc correlates with chills | Significant | **opioid_proxy dimension justified** |
| **Blood & Zatorre 2001** | PET (rCBF) | 10 | Chills correlate with: ↑ ventral striatum, midbrain (VTA), OFC; ↓ amygdala, hippocampus. Self-selected familiar music still rewards | Linear with intensity | **Same regions respond across repeated exposure** |
| **Menon & Levitin 2005** | fMRI | 13 | VTA↔NAcc significant functional connectivity during pleasant music | Significant | **vta_drive dimension** |
| **Howe 2013** | In vivo rodent | — | DA ramps gradually toward distant goals. Quasi-hyperbolic, scales with distance × magnitude | — | **da_caudate ramp profile** |
| **Schultz 2016** | Review | — | Two-component phasic DA: (1) unselective detection 40-120ms, (2) value-coding RPE. Baseline ~5 Hz, burst 14-30 Hz | — | **prediction_error temporal profile** |
| **Loui 2017** | DTI | 20 | White matter NAcc-STG tract integrity ↔ pleasure | r=0.61 | **Structural basis for individual differences** |
| **Mori & Zatorre 2024** | fMRI + ML (LASSO) | 49 | Pre-listening auditory-reward network connectivity predicts subsequent chills duration and NAcc activation. Right AC-striatum/OFC connections most predictive | r=0.53 (chills), r=0.61 (NAcc BOLD) | **stg_nacc_coupling has tonic baseline component; pre-listening state matters** |
| **Mohebi et al. 2024** | Fiber photometry (dLight, rodent) | — | DA transients follow striatal gradient of reward time horizons: VS τ=981s, DMS τ=414s, DLS τ=36s. Ventral = long horizons, dorsal = short | Gradient significant | **Mechanistic basis for multi-timescale da_caudate vs da_nacc** |
| **Chabin et al. 2020** | HD-EEG (256ch) + source localization | 18 | Theta ↑ in fronto-prefrontal (OFC) with pleasure; decreased theta in right central (SMA) + right temporal (STG) during chills. Beta/alpha ratio ↑ with arousal | F(2,15)=17.4-27.3, p<10⁻⁵ | **EEG temporal validation of chills circuit (OFC, SMA, STG)** |
| **Sachs et al. 2025** | fMRI + HMM | 39 | Spatiotemporal patterns along temporal-parietal axis track emotion transitions. Context modulates neural event boundaries — same music evokes different timing depending on preceding emotion | Significant | **Dynamic emotion context effects on temporal processing** |
| **Mas-Herrero et al. 2014** | fMRI + behavioral + SCR/HR | 30 | Musical anhedonia is SPECIFIC to music (money/sex unaffected). ANH group: no SCR-pleasure correlation (t(9)=0.88, p=0.4) vs HDN: r significant (t(9)=5.43, p<0.001) | BMRQ F(2,23)=19.14, p<0.001 | **Original anhedonia specificity evidence; extends Martinez-Molina 2016** |

### 3.2 The Temporal Story: Exact Timing

```
COMPLETE TEMPORAL PROFILE OF MUSIC REWARD RESPONSE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1: PERCEPTUAL PROCESSING (continuous)
─────────────────────────────────────────────
Auditory cortex (STG) encodes spectrotemporal patterns.
Matched against stored templates from prior exposure.
Patterns transmitted to frontal cortex via auditory-frontal loops.

Phase 2: PREDICTION GENERATION (continuous, ~100-500ms ahead)
──────────────────────────────────────────────────────────────
Frontal cortex (IFG, dlPFC) generates predictions.
Predictions transmitted to caudate via fronto-striatal pathways.
Prediction confidence modulates caudate signal strength.
(Mas-Herrero 2021: dlPFC→caudate R²=0.41, dlPFC→NAcc R²=0.42)

Phase 3: ANTICIPATION BUILDUP (~2-30s before peak)
───────────────────────────────────────────────────
As musical structure signals approaching climax:
  - Caudate DA ramps up quasi-hyperbolically (Howe 2013)
  - NOT linear — accelerates toward expected reward
  - Scales with: proximity × expected magnitude × prediction confidence
  - Huron "Tension" (T) response engaged
  - Huron "Imagination" (I) response for longer timescales

Phase 4: EVENT — PREDICTION ERROR (~50-110ms after musical event)
─────────────────────────────────────────────────────────────────
At the critical musical moment:
  - Two-component Schultz DA response:
    Component 1 (40-120ms): Unselective detection, sensory intensity
    Component 2 (evolves): Value-coded RPE = R(t) + γV(t+1) - V(t)

  - If better than expected: phasic burst (14-30 Hz, <200ms)
  - If exactly as expected: no change from baseline (~5 Hz)
  - If worse than expected: dip below baseline (contrast enhancement)

  - For deceptive cadences / violated expectations:
    DA dip → then delayed resolution → ENHANCED burst
    (This is why delayed resolutions are so rewarding)

Phase 5: PEAK PLEASURE (0-5 seconds)
─────────────────────────────────────
  - NAcc DA release peaks during experience (Salimpoor 2011)
  - μ-opioid release in NAcc hedonic hotspots (Nummenmaa 2025)
  - STG→NAcc connectivity at maximum (Mas-Herrero 2021: R²=0.40)
  - Convergence of DA + opioid → crosses ANS threshold:
    → Skin conductance ↑ (Ferreri 2019: t(25)=-2.26, P=0.033)
    → Heart rate ↑
    → Piloerection (~50% of chill episodes)
    → Pupil dilation
  - This convergence = CHILLS/FRISSON

Phase 6: APPRAISAL (0.5-2s after peak)
───────────────────────────────────────
  - Huron "Appraisal" (A) response: conscious evaluation
  - OFC value judgment, vmPFC integration
  - Hippocampal encoding for future anticipation
  - Prediction model updated (learning)

Phase 7: RESET
──────────────
  - Caudate activity drops to baseline at peak arrival
  - NAcc activity gradually declines over seconds
  - Neuronal refractory period: 1-3ms (negligible)
  - BEHAVIORAL refractory: ~10-30s between chills (Grewe 2009)
    (Not neural exhaustion — time needed to build new predictions)
```

### 3.3 Dopamine Dynamics: Quantitative Parameters

| Parameter | Value | Source | MI Mapping |
|-----------|-------|--------|-----------|
| Tonic DA baseline | ~5.3 ± 1.5 Hz | Schultz 1998 | da_caudate/da_nacc resting state |
| Phasic burst latency | 50-110 ms after stimulus | Schultz 2016 | prediction_error onset |
| Phasic burst duration | <200 ms total | Schultz 2016 | prediction_error window |
| Phasic burst frequency | 14-30 Hz intraburst | Schultz 2016 | prediction_error magnitude |
| DA reuptake half-life | ~200 ms (striatum) | Jones et al. 1998 | Decay constant |
| Anticipatory ramp onset | 2-30s before peak | Salimpoor 2011, Howe 2013 | da_caudate ramp start |
| Anticipatory ramp profile | Quasi-hyperbolic | Howe 2013 | da_caudate curve shape |
| Peak chill duration | 1-5 s | Salimpoor 2009 | liking peak width |
| Chills per excerpt | ~3.7 average | Salimpoor 2011 | peak_detection frequency |
| Inter-chill refractory | ~10-30 s | Grewe et al. 2009 | peak_detection cooldown |
| Chill prevalence | 55-90% of listeners | de Fleurian & Pearce 2021 | Individual differences |
| Musical anhedonia | ~5% of population | Martinez-Molina 2016 | Floor effect |

### 3.4 Chills/Frisson: The Physical Response

**Prevalence**: 55-90% report musical chills at least sometimes (Goldstein 1980, Panksepp 1995, de Fleurian & Pearce 2021).

**Musical Triggers** (Sloboda 1991, Panksepp 1995, Grewe 2007):
- Melodic appoggiaturas (dissonance → resolution)
- Chord progressions descending circle of fifths to tonic
- Onset of unexpected harmonies
- Dramatic crescendos (**most common trigger** — Panksepp 1995)
- Melodic/harmonic sequences at different pitch levels
- Moments of modulation (key changes)
- Melodies in human vocal register (~300-3000 Hz)

**Common thread**: All triggers involve either **expectancy violation** (harmonic surprises, unexpected entries) or **dramatic intensification** (crescendos, textural changes) — both generate large prediction errors.

**Chills ≠ DA release**: DA release occurs throughout anticipation without chills. Chills = **threshold crossing** when DA + opioid + ANS activation converge. You can have DA without chills, but not chills without DA.

### 3.5 The Uncertainty × Surprise Interaction (Cheung 2019)

Musical pleasure is NOT simply "high surprise = good". It follows a **2D nonlinear surface**:

```
PLEASURE AS f(UNCERTAINTY, SURPRISE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                    HIGH SURPRISE
                         │
                    ╱────┼────╲
                   ╱ MAXIMUM  ╲
                  ╱  PLEASURE  ╲
    LOW          ╱      │       ╲          HIGH
    UNCERTAINTY ─┼──────┼───────┼── UNCERTAINTY
                  ╲     │      ╱
                   ╲ MAXIMUM  ╱
                    ╲PLEASURE╱
                     ╲──┼──╱
                         │
                    LOW SURPRISE

Peak pleasure at two sweet spots:
  (1) Low uncertainty + High surprise = "I thought I knew, but WOW"
  (2) High uncertainty + Low surprise = "I was confused, but it resolved"

Brain mapping (Cheung 2019):
  Uncertainty × Surprise interaction: Amygdala, Hippocampus, Auditory cortex
  Uncertainty alone: NAcc, Caudate, pre-SMA
```

### 3.6 Huron's ITPRA: Five Temporal Response Systems

| System | Timing | Valence | Brain Basis | MI Dimension |
|--------|--------|---------|-------------|-------------|
| **I**magination | Seconds to minutes before | Positive (anticipatory) | dlPFC, default mode | reward_forecast |
| **T**ension | Seconds before | Negative (arousal) | Autonomic, caudate ramp | tension |
| **P**rediction | ~130-250ms before event | Positive if confirmed | Striatal RPE | prediction_match |
| **R**eaction | ~150ms after event | Negative (protective) | Brainstem reflex | reaction |
| **A**ppraisal | 0.5-2s after event | Context-dependent | OFC, vmPFC | appraisal |

The speed of musical events determines which components engage. Fast passages may only trigger T-P-R. Slow passages allow full I-T-P-R-A engagement.

### 3.7 Habituation and Repeated Exposure

**Within-session**: After a peak, the system needs a new anticipation-buildup cycle. Not neural exhaustion — prediction update means next similar event produces smaller RPE.

**Across-session** (the inverted-U exposure curve):
- 1st-10th exposure: Increasing pleasure (mere exposure effect, Zajonc 1968)
- Optimal zone: Familiar enough for confident predictions, uncertain enough for RPE
- Overexposure (>>10th): RPE → 0, hedonic decline (but see below)

**Critical nuance**: Blood & Zatorre (2001) showed the SAME brain regions (NAcc, VTA, ventral striatum) respond to **self-selected familiar music** that participants had heard many times. This means familiar music that maintains emotional power continues to activate reward circuitry — micro-prediction-errors at local level sustain engagement even when global structure is fully predicted.

---

## 4. Output Space: 19D Multi-Layer Representation

The SRP output is organized in six neuroscience-grounded layers. See [representation-space.md](../../representation-space.md) for full framework.

### 4.1 Complete Output Specification

```
SRP OUTPUT TENSOR: 19D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER N — NEUROCHEMICAL SIGNALS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0  │ da_caudate        │ [0, 1] │ Dorsal striatal DA. Ramps quasi-hyperbolically
    │                   │        │ toward expected reward. Salimpoor 2011 (r=0.71),
    │                   │        │ Howe 2013 (proximity signal). Peaks BEFORE event.
────┼───────────────────┼────────┼────────────────────────────────────────────
 1  │ da_nacc           │ [0, 1] │ Ventral striatal DA. Phasic burst at peak moment.
    │                   │        │ Salimpoor 2011 (r=0.84). 1-5s duration.
    │                   │        │ STG→NAcc connectivity drives this (Salimpoor 2013).
────┼───────────────────┼────────┼────────────────────────────────────────────
 2  │ opioid_proxy      │ [0, 1] │ μ-opioid receptor activation in NAcc shell.
    │                   │        │ Nummenmaa 2025: [¹¹C]carfentanil PET.
    │                   │        │ Hedonic "liking" component. Proxied via
    │                   │        │ consonance resolution + spectral smoothness.

LAYER C — CIRCUIT ACTIVATION
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 3  │ vta_drive         │ [0, 1] │ VTA → Striatum pathway activation.
    │                   │        │ Menon & Levitin 2005. Source of DA.
────┼───────────────────┼────────┼────────────────────────────────────────────
 4  │ stg_nacc_coupling │ [0, 1] │ Auditory cortex ↔ NAcc functional connectivity.
    │                   │        │ Salimpoor 2013: predicts reward value.
    │                   │        │ Martinez-Molina 2016: absent in anhedonia.
────┼───────────────────┼────────┼────────────────────────────────────────────
 5  │ prediction_error  │[-1, 1] │ Schultz RPE: δ = R + γV(t+1) - V(t).
    │                   │        │ +1 = max positive surprise (better than expected).
    │                   │        │ -1 = max negative surprise (worse than expected).
    │                   │        │ 0 = exactly as predicted.

LAYER P — PSYCHOLOGICAL STATES (Berridge Framework)
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 6  │ wanting           │ [0, 1] │ Berridge incentive salience. DA-dependent.
    │                   │        │ f(da_caudate). Ramps BEFORE event.
    │                   │        │ Ferreri 2019: levodopa ↑, risperidone ↓.
────┼───────────────────┼────────┼────────────────────────────────────────────
 7  │ liking            │ [0, 1] │ Berridge hedonic impact. Opioid + DA.
    │                   │        │ f(opioid_proxy, da_nacc). Peaks AT event.
    │                   │        │ Mallik 2017: naltrexone ↓ emotional intensity.
────┼───────────────────┼────────┼────────────────────────────────────────────
 8  │ pleasure          │ [0, 1] │ Composite subjective pleasure P(t).
    │                   │        │ P = 0.84·da_nacc + 0.71·da_caudate
    │                   │        │ (Salimpoor 2011 coefficients)

LAYER T — TEMPORAL RESPONSE (Huron ITPRA)
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 9  │ tension           │ [0, 1] │ Huron T: preparatory arousal before event.
    │                   │        │ Scales with uncertainty × significance.
────┼───────────────────┼────────┼────────────────────────────────────────────
10  │ prediction_match  │[-1, 1] │ Huron P: +1 = confirmed, -1 = violated.
    │                   │        │ Phasic at event boundaries.
────┼───────────────────┼────────┼────────────────────────────────────────────
11  │ reaction          │ [0, 1] │ Huron R: reflexive brainstem response.
    │                   │        │ ~150ms after event. Startle/orienting.
────┼───────────────────┼────────┼────────────────────────────────────────────
12  │ appraisal         │[-1, 1] │ Huron A: conscious evaluation 0.5-2s after.
    │                   │        │ +1 = positive, -1 = negative reappraisal.

LAYER M — MUSICAL MEANING
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Musical Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
13  │ harmonic_tension  │ [0, 1] │ Tonal distance from tonic. High = dominant/
    │                   │        │ applied chord. Low = tonic, resolved.
────┼───────────────────┼────────┼────────────────────────────────────────────
14  │ dynamic_intensity │ [0, 1] │ Energy trajectory (crescendo/decrescendo).
    │                   │        │ Correlates with arousal.
────┼───────────────────┼────────┼────────────────────────────────────────────
15  │ peak_detection    │ [0, 1] │ Chill trigger detection. Sloboda 1991 features:
    │                   │        │ appoggiaturas, crescendos, harmonic changes.

LAYER F — FORECAST (Predictive Signals)
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
16  │ reward_forecast   │ [0, 1] │ Expected reward in 2-8s. Based on current
    │                   │        │ buildup trajectory + harmonic tension.
────┼───────────────────┼────────┼────────────────────────────────────────────
17  │ chills_proximity  │ [0, 1] │ Estimated proximity to chills event.
    │                   │        │ Respects refractory (~10-30s, Grewe 2009).
────┼───────────────────┼────────┼────────────────────────────────────────────
18  │ resolution_expect │ [0, 1] │ Expected harmonic resolution in 0.5-2s.
    │                   │        │ High when dominant → tonic anticipated.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 19D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 5. Complete EAR Demand (R³ Features)

### 5.1 R³ v1 Feature Dependencies ([0:49])

> **Note**: R³ indices are MI's own (0-48), NOT D0 S⁰ indices.
> See [Road-map/02-R3-SPECTRAL.md](../../Road-map/02-R3-SPECTRAL.md) for full specification.

**Group A: Consonance/Dissonance (7D)** [R³ 0:7] — "Can this moment be liked?"

| R³ idx | Name | Psychoacoustic Basis | SRP Role |
|--------|------|---------------------|----------|
| 0 | roughness | Plomp-Levelt critical band beating | Inverse valence proxy. High roughness = unpleasant → opioid_proxy ↓ |
| 1 | sethares_dissonance | Timbre-dependent dissonance | How harmonic content affects consonance |
| 2 | helmholtz_kang | Harmonic template matching | Simple integer ratio detection (consonant) |
| 3 | stumpf_fusion | Tonal fusion in critical bands | Sounds merge into unity (pleasant) |
| 4 | sensory_pleasantness | Spectral regularity + smoothness | **Direct opioid_proxy correlate** |
| 5 | inharmonicity | Deviation from harmonic series | Low = in-tune = resolved = pleasant |
| 6 | harmonic_deviation | Error from ideal harmonics | Direct consonance measure |

**Group B: Energy/Dynamics (5D)** [R³ 7:12] — "Is the music building or releasing?"

| R³ idx | Name | What It Measures | SRP Role |
|--------|------|-----------------|----------|
| 7 | amplitude (A) | RMS energy | Loudness proxy → dynamic_intensity |
| 8 | velocity_A (dA/dt) | Rate of energy change | Crescendo detection → tension, wanting ramp |
| 9 | acceleration_A | Energy buildup curvature | Natural vs forced dynamics → anticipation profile |
| 10 | loudness | Stevens' law (sone scale) | Perceptual volume → arousal → reaction |
| 11 | onset_strength | Transient energy | Attack sharpness → peak_detection trigger |

**Group C: Timbre/Quality (9D)** [R³ 12:21] — "Does this sound good?"

| R³ idx | Name | What It Measures | SRP Role |
|--------|------|-----------------|----------|
| 12 | warmth | Low-frequency balance | Affective warmth → opioid_proxy |
| 13 | sharpness | High-frequency weighting | Harsh vs brilliant → liking modulator |
| 14 | tonalness | Harmonic-to-noise ratio | Tonal = more pleasant → opioid_proxy |
| 15 | clarity | Signal-to-noise definition | Clear = pleasant → opioid_proxy |
| 16 | spectral_smoothness | Spectral envelope regularity | Smooth = instrument → opioid_proxy |
| 17 | spectral_autocorrelation | Harmonic periodicity | Strong periodicity = musical |
| 18 | tristimulus1 | Fundamental strength | Pure tone dominance |
| 19 | tristimulus2 | 2nd-4th harmonic energy | Brilliance |
| 20 | tristimulus3 | 5th+ harmonic energy | Brightness/edge |

**Group D: Change/Surprise (4D)** [R³ 21:25] — "Did something unexpected happen?"

| R³ idx | Name | What It Measures | SRP Role |
|--------|------|-----------------|----------|
| 21 | spectral_flux | Frame-to-frame spectral change | prediction_error trigger |
| 22 | distribution_entropy | Shannon entropy of spectrum | Uncertainty context (Cheung 2019) |
| 23 | distribution_flatness | Wiener entropy | Noisy/unpredictable → tension |
| 24 | distribution_concentration | Herfindahl index | Focused/tonal = more predictable |

**Group E: Cross-Layer Interactions (24D)** [R³ 25:49] — "How do features relate?"

| R³ idx | Name | Interaction | SRP Role |
|--------|------|------------|----------|
| 25:33 | x_l0l5 (8D) | Energy × Consonance | Raw state → pleasure coupling |
| 33:41 | x_l4l5 (8D) | Derivatives × Consonance | Dynamics → pleasure (**critical for tension**) |
| 41:49 | x_l5l7 (8D) | Consonance × Timbre | Pleasure → spectral coherence |

### 5.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | SRP Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **I: Information** | [87] | melodic_entropy | Prediction error magnitude — melodic surprise is a primary driver of striatal RPE; high melodic entropy signals uncertain predictions, amplifying both anticipatory caudate DA and phasic NAcc burst at resolution | Pearce 2005 IDyOM; Gold 2019 RPE in NAcc |
| **I: Information** | [88] | harmonic_entropy | Harmonic prediction error — chord-level surprise drives the uncertainty × surprise interaction (Cheung 2019) that determines peak pleasure; directly feeds prediction_error computation | Gold 2019 chord transition probability; Cheung 2019 |

**Rationale**: SRP is the foundational reward model computing wanting, liking, and prediction error from striatal dopamine dynamics. The I:Information group provides direct measures of the musical information content that drives prediction error — the core computational variable of the reward pathway. Currently SRP infers surprise from spectral_flux [21] and distribution_entropy [22], which are acoustic-level proxies. melodic_entropy [87] and harmonic_entropy [88] provide music-theoretic surprise measures grounded in probabilistic prediction (IDyOM), directly mapping to the Schultz RPE signal that SRP models. These features flow through pathway-mediated access (P1/P3/P5) to all dependent ARU models.

**Code impact** (Phase 6): `r3_indices` extended to include [87], [88]. These feed prediction_error, harmonic_tension, and the Cheung uncertainty × surprise interaction.

### 5.3 Summary

```
TOTAL EAR DIMENSIONS FOR SRP: 49D
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Group A: Consonance        7D   → opioid_proxy, liking
Group B: Energy            5D   → dynamic_intensity, tension, wanting
Group C: Timbre            9D   → opioid_proxy, liking
Group D: Change            4D   → prediction_error, reaction
Group E: Interactions     24D   → cross-feature coupling
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL:                    49D
```

---

## 6. Complete Temporal Demand (H³ Context)

### 6.1 How R³ and H³ Relate

```
R³ = WHAT the sound is (spectral snapshot, single frame, 5.8ms)
H³ = HOW the sound is CHANGING over time (multi-scale temporal context)

R³ answers: "What am I hearing RIGHT NOW?"
H³ answers: "What has been happening? What's the trajectory?"

RELATIONSHIP:
━━━━━━━━━━━━
     R³(t-N) ─────┐
     R³(t-N+1) ───┤
     R³(t-N+2) ───┤
     ...           ├──► H³(t) = 24 morphs × 3 h-laws computed
     R³(t-1) ─────┤    over attention-weighted R³ window
     R³(t) ───────┘
                        Attention: A(dt) = exp(-3|dt|/H)
                        where H = horizon window size in frames

H³ takes R³ features, windows them across time,
and computes morphological features that reduce both temporal
and feature dimensions to a single scalar per (horizon, morph, law).

Total H³ dimensions: 32 horizons × 24 morphs × 3 laws = 2304D
SRP uses: ~124 specific (h, m, l) tuples (5.4%)
         See Road-map/03-H3-TEMPORAL.md for exact demand tree.
```

### 6.2 Temporal Layers (Nested, Overlapping, Simultaneous)

**Critical neuroscience insight**: These layers mirror the brain's **nested oscillatory hierarchy** (Giraud & Poeppel 2012, Lakatos et al. 2005):
- Gamma phase (25-50 Hz) modulates at note level
- Theta phase (4-8 Hz) modulates at beat level
- Delta phase (1-3 Hz) modulates at phrase level
- Infra-slow oscillations modulate at section/form level

All running simultaneously, with cross-frequency coupling binding them.

```
TEMPORAL CONTEXT LAYERS (Nested, Overlapping)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Layer 1: IMMEDIATE (Beat-level, 200ms-1s)
┌─────────────────────────────────────────────────────────────┐
│  H6 (200ms, 34 frames)    H7 (250ms, 43 frames)            │
│  H11 (500ms, 86 frames)   H12 (525ms, 90 frames)           │
│  H15 (800ms, 138 frames)  H16 (1000ms, 172 frames)         │
│                                                              │
│  Captures: Note attacks, beat cycles,                        │
│  immediate consonance/dissonance, onset detection             │
│  Huron ITPRA: Prediction (P) + Reaction (R) responses        │
│                                                              │
│  Feeds: AED (arousal, expectancy), CPD (triggers, peaks),    │
│         C0P (cognitive state)                                 │
│  Maps to: prediction_error, reaction, peak_detection         │
└─────────────────────────────────────────────────────────────┘

Layer 2: PHRASE (2-8 seconds)
┌─────────────────────────────────────────────────────────────┐
│  H18 (2s, 344 frames)   H19 (3s, 517 frames)               │
│  H20 (5s, 862 frames)                                       │
│                                                              │
│  Captures: Melodic phrase arcs,                              │
│  harmonic progressions (I-IV-V-I ~ 4s at 60bpm),            │
│  Huron "Tension" (T) response,                               │
│  groove establishment, short buildup patterns                 │
│                                                              │
│  Feeds: CPD (buildup tracking), AED (motor-affective)        │
│  Maps to: tension, harmonic_tension, dynamic_intensity       │
│                                                              │
│  SRP demands phrase-level context (Layers 1 + 2).           │
└─────────────────────────────────────────────────────────────┘

Layer 3: SECTION (15-60 seconds)
┌─────────────────────────────────────────────────────────────┐
│  H22 (15s, 2585 frames)  H23 (25s, 4309 frames)            │
│  H24 (36s, 6202 frames)                                     │
│                                                              │
│  Captures: Verse→Chorus transitions,                         │
│  Salimpoor's "anticipation phase" (15-30s caudate ramp),     │
│  section-level tension-resolution arcs,                      │
│  Huron "Imagination" (I) response                            │
│                                                              │
│  THIS IS THE SALIMPOOR WINDOW                                │
│  Feeds: da_caudate ramp, wanting, reward_forecast            │
│                                                              │
│  Section-level context for Salimpoor anticipation window.     │
└─────────────────────────────────────────────────────────────┘

Layer 4: STRUCTURAL (2-7 minutes) — OPTIONAL for v1
┌─────────────────────────────────────────────────────────────┐
│  H26 (200s, 34454 frames)  H28 (414s, 71343 frames)        │
│                                                              │
│  Captures: Movement-level narrative,                         │
│  development→recapitulation (sonata),                        │
│  build→drop (EDM), overall emotional arc                     │
│                                                              │
│  Nice-to-have for symphonic/long-form music validation       │
└─────────────────────────────────────────────────────────────┘

SIMULTANEOUS PROCESSING AT EVERY FRAME:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Frame t:  R³(t)         "what am I hearing now?"              5.8ms
          ↕
Layer 1:  H³(t, H12)   "how has this beat evolved?"          525ms
          ↕
Layer 2:  H³(t, H20)   "where is this phrase going?"         5s
          ↕
Layer 3:  H³(t, H24)   "is the chorus approaching?"          36s
          ↕
Layer 4:  H³(t, H28)   "where am I in the piece?"            7min

Each layer feeds different SRP mechanisms:
  Layer 1 → prediction_error, reaction, peak_detection
  Layer 2 → tension, harmonic_tension, dynamic_intensity
  Layer 3 → da_caudate (wanting ramp), reward_forecast
  Layer 4 → overall pleasure trajectory (narrative arc)
```

### 6.3 H³ Morphs Relevant to SRP

| Morph | Name | Computation | SRP Role |
|-------|------|------------|----------|
| M0 | value | Attention-weighted mean | Current feature state |
| M1 | mean | Unweighted mean | Baseline reference level |
| M2 | std | Standard deviation | Variability (stability metric) |
| M4 | max | Maximum in window | Peak detection |
| M5 | range | Max - Min | Dynamic contrast measure |
| M8 | velocity | First derivative | Rate of change (crescendo) |
| M9 | velocity_mean | Mean of velocity | Sustained buildup |
| M10 | velocity_std | Velocity variance | Jerk-like surprise signal |
| M11 | acceleration | Second derivative | Buildup acceleration |
| M14 | periodicity | Autocorrelation peak | Groove/entrainment |
| M15 | smoothness | 1/(1+\|jerk\|/σ) | Naturalness (scale-invariant) |
| M17 | shape_period | Oscillation period | Rhythmic structure |
| M18 | trend | Linear regression slope | Long-term trajectory |
| M19 | stability | 1/(1+var/σ²) | Resistance to change (resolution = stable) |
| M20 | entropy | Shannon entropy of histogram | Complexity/unpredictability |
| M21 | zero_crossings | Sign change count | Textural complexity |
| M22 | peaks | Local maxima count | Event density |

### 6.4 Complete H³ Demand Matrix

> **CORRECTED in v4.0**: The original demand matrix listed ~55 "primary" tuples.
> An exhaustive audit of all 90 mechanism formulas (Section 7.1) reveals **124 unique
> H³ scalar values** actually needed. See [Road-map/03-H3-TEMPORAL.md](../../Road-map/03-H3-TEMPORAL.md)
> for the complete branching demand tree with per-mechanism breakdowns.

```
H³ DEMAND SUMMARY FOR SRP
━━━━━━━━━━━━━━━━━━━━━━━━━

Mechanism │ Horizons            │ Unique (M,L) pairs │ Total H³ scalars
──────────┼─────────────────────┼────────────────────┼──────────────────
AED       │ H6 (200ms),         │ 21 pairs           │ 21 × 2 = 42
          │ H16 (1000ms)        │ (averaged)         │
──────────┼─────────────────────┼────────────────────┼──────────────────
CPD       │ H7 (250ms),         │ 20 pairs           │ 20 × 3 = 60
          │ H12 (525ms),        │ (averaged)         │
          │ H15 (800ms)         │                    │
──────────┼─────────────────────┼────────────────────┼──────────────────
C0P       │ H11 (500ms)         │ 16 pairs           │ 16 × 1 = 16
          │ (single)            │                    │
──────────┼─────────────────────┼────────────────────┼──────────────────
SRP Direct│ H18 (2000ms)        │ 6 pairs            │ 6 × 1 = 6
          │                     │                    │
──────────┼─────────────────────┼────────────────────┼──────────────────
TOTAL     │ 7 horizons          │ ~57 unique pairs   │ 124 H³ scalars
          │ (of 32 possible)    │ (22 of 24 morphs)  │ (5.4% of 2304)
```

### 6.5 R³ v2 Projected Expansion

No significant direct v2 expansion projected for SRP. As a pathway-dependent ARU model, SRP receives R³ features indirectly through cross-unit pathways (P1/SPU, P3/IMU, P5/STU). New v2 features flow automatically through these pathways.

**v2 projected**: 0 additional tuples (pathway-mediated)

---

## 7. Mechanism Computation: Exact Formulas

### 7.1 Mechanisms (All 90 Dimensions)

Each mechanism receives H³ values indexed as `_idx(morph, law) = morph * 3 + law` into a 72D vector (24 morphs × 3 laws) averaged across the mechanism's horizons.

#### AED — Affective Entrainment Dynamics (30D)

**Horizons**: H6 (200ms), H16 (1000ms) — bidirectional
**Scientific basis**: Huron 2006 (ITPRA), Meyer 1956, Koelsch 2019, Janata 2012

```
AROUSAL DYNAMICS [0:10]
  D0  arousal_level          = σ(h0[M4,L2])     # ANS activation proxy
  D1  arousal_change         = tanh(h0[M8,L2])   # Rate of arousal change
  D2  arousal_peak           = σ(h0[M4,L0])      # Proximity to peak
  D3  autonomic_activation   = σ(h0[M5,L2])      # Range → ANS drive
  D4  skin_conductance_proxy = σ(h0[M9,L2])      # Acceleration → SCR
  D5  heart_rate_change      = tanh(h0[M8,L0])   # Forward velocity → HR
  D6  respiratory_coupling   = σ(h0[M14,L2])     # Periodicity → breath
  D7  pupil_dilation_proxy   = σ(h0[M10,L2])     # Jerk → pupil
  D8  arousal_habituation    = σ(h0[M19,L2])     # Stability → habituation
  D9  arousal_recovery       = σ(h0[M9,L1])      # Backward accel → recovery

EXPECTANCY AFFECT [10:20] — Implements ITPRA
  D10 expectation_strength   = σ(h0[M18,L0])     # Forward trend
  D11 violation_magnitude    = σ(h0[M10,L2])     # Jerk = surprise
  D12 prediction_pleasure    = σ(h0[M22,L2])     # Regularity → confirmed
  D13 surprise_valence       = tanh(h0[M18,L0]-h0[M18,L1])  # Fwd-Bwd trend
  D14 tension_level          = σ(h0[M9,L0])      # Forward acceleration
  D15 resolution_satisfaction= σ(h0[M19,L1])     # Backward stability
  D16 suspense               = σ(h0[M20,L2])     # Entropy → uncertainty
  D17 curiosity_drive        = σ(h0[M20,L0])     # Forward entropy
  D18 contrastive_valence    = tanh(h0[M8,L2])   # Velocity direction
  D19 aesthetic_flow          = σ(h0[M19,L2])     # Stability = flow

MOTOR-AFFECTIVE COUPLING [20:30] — Groove/embodiment
  D20 entrainment_strength   = σ(h0[M14,L2])     # Periodicity → sync
  D21 movement_urge          = σ(h0[M8,L2])      # Velocity → move
  D22 groove_pleasure        = σ(h0[M15,L2])     # Smoothness → groove
  D23 body_arousal           = σ(h0[M4,L2])      # Max → bodily activation
  D24 synchrony_reward       = σ(h0[M22,L2])     # Regularity → sync reward
  D25 social_bonding         = σ(h0[M23,L2])     # Symmetry → social
  D26 motor_fluency          = σ(h0[M19,L2])     # Stability → fluency
  D27 embodiment_depth       = σ(h0[M1,L2])      # Mean → baseline level
  D28 rhythmic_pleasure      = σ(h0[M17,L2])     # Shape period → rhythm
  D29 motor_affect_coupling  = σ(h0[M15,L0])     # Forward smoothness
```

#### CPD — Chills & Peak Detection (30D)

**Horizons**: H7 (250ms), H12 (525ms), H15 (800ms) — bidirectional
**Scientific basis**: Sloboda 1991, Salimpoor 2011, Lehne & Koelsch 2015, Guhn 2007

```
TRIGGER FEATURES [0:10] — Chill-inducing acoustic features
  D0  melodic_tension        = σ(h0[M10,L0])     # Jerk → melodic surprise
  D1  harmonic_surprise      = σ(h0[M11,L2])     # Snap → harmonic change
  D2  dynamic_swell          = σ(h0[M8,L0])      # Velocity → crescendo
  D3  timbral_change         = σ(h0[M16,L0])     # Curvature → timbre shift
  D4  registral_shift        = σ(h0[M5,L0])      # Range → register change
  D5  textural_expansion     = σ(h0[M21,L0])     # Complexity → texture
  D6  rhythmic_deviation     = σ(h0[M10,L2])     # Jerk → rhythmic surprise
  D7  vocal_entry            = σ(h0[M0,L0])      # Value → new element entry
  D8  trigger_density        = σ(h0[M21,L2])     # Complexity → density
  D9  trigger_novelty        = σ(h0[M20,L2])     # Entropy → novelty

BUILDUP TRACKING [10:20] — Tension accumulation
  D10 tension_accumulation   = σ(h0[M18,L0])     # Forward trend → buildup
  D11 buildup_rate           = σ(h0[M8,L0])      # Velocity → buildup speed
  D12 buildup_duration       = σ(h0[M5,L0])      # Range → how long building
  D13 harmonic_tension_acc   = σ(h0[M9,L2])      # Acceleration → harmonic
  D14 dynamic_gradient       = σ(h0[M18,L2])     # Bidi trend → dynamics
  D15 textural_density_growth= σ(h0[M21,L0])     # Complexity growth
  D16 anticipatory_da        = σ(h0[M4,L0])      # Forward max → DA proxy
  D17 climax_proximity       = σ(h0[M4,L2])      # Bidi max → near climax
  D18 suspension_count       = σ(h0[M10,L0])     # Jerk count → suspensions
  D19 buildup_momentum       = σ(h0[M8,L2])      # Bidi velocity → momentum

PEAK RESPONSE [20:30] — Peak experience encoding
  D20 chill_intensity        = σ(h0[M4,L2])      # Bidi max → intensity
  D21 goosebump_proxy        = σ(h0[M9,L2])      # Acceleration → ANS
  D22 dopamine_release       = σ(h0[M4,L0])      # Forward max → DA burst
  D23 emotional_peak         = σ(h0[M5,L2])      # Range → emotional range
  D24 tears_proxy            = σ(h0[M18,L1])     # Backward trend → tears
  D25 spine_shiver           = σ(h0[M11,L2])     # Snap → spine response
  D26 pleasure_valence       = σ(h0[M22,L2])     # Regularity → pleasant
  D27 awe_wonder             = σ(h0[M20,L2])     # Entropy → awe
  D28 peak_duration          = σ(h0[M5,L0])      # Forward range → duration
  D29 afterglow              = σ(h0[M19,L1])     # Backward stability → glow
```

#### C0P — Cognitive Projection (30D)

**Horizons**: H11 (500ms) — forward only
**Scientific basis**: Baars 1988 (Global Workspace), Tononi 2004, Koelsch 2014, Raichle 2001

```
FEATURE AGGREGATION [0:10] — Information compression
  D0  oscillatory_summary    = σ(h0[M1,L2])      # Mean → oscillatory
  D1  timing_summary         = σ(h0[M14,L2])     # Periodicity → timing
  D2  memory_summary         = σ(h0[M19,L2])     # Stability → memory
  D3  affective_summary      = σ(h0[M4,L2])      # Max → affect
  D4  cross_layer_coherence  = σ(h0[M22,L2])     # Regularity → coherence
  D5  information_rate       = σ(h0[M8,L2])      # Velocity → info rate
  D6  processing_load        = σ(h0[M21,L2])     # Complexity → load
  D7  feature_salience       = σ(h0[M5,L2])      # Range → salience
  D8  integration_quality    = σ(h0[M23,L2])     # Symmetry → quality
  D9  state_complexity       = σ(h0[M20,L2])     # Entropy → complexity

COGNITIVE STATE [10:20] — Default Mode / Task Positive
  D10 attention_mode         = σ(h0[M4,L2])      # Max → attention
  D11 prediction_mode        = σ(h0[M18,L0])     # Forward trend → predict
  D12 memory_mode            = σ(h0[M19,L1])     # Backward stability → mem
  D13 emotional_mode         = σ(h0[M1,L2])      # Mean → emotional base
  D14 engagement_level       = σ(h0[M8,L2])      # Velocity → engagement
  D15 consciousness_level    = σ(h0[M5,L2])      # Range → awareness
  D16 processing_efficiency  = σ(h0[M22,L2])     # Regularity → efficiency
  D17 meta_cognitive_state   = σ(h0[M20,L2])     # Entropy → meta-cognition
  D18 default_mode_activity  = σ(h0[M19,L1])     # Bwd stability → DMN
  D19 task_positive_activity = σ(h0[M4,L0])      # Fwd max → TPN

UNIT PROJECTION [20:30] — To 9 cognitive units
  D20 spu_projection         = σ(h0[M5,L2])      # Range → SPU
  D21 stu_projection         = σ(h0[M14,L2])     # Periodicity → STU
  D22 imu_projection         = σ(h0[M19,L2])     # Stability → IMU
  D23 aru_projection         = σ(h0[M1,L2])      # Mean → ARU
  D24 asu_projection         = σ(h0[M10,L2])     # Jerk → ASU
  D25 mpu_projection         = σ(h0[M8,L0])      # Velocity → MPU
  D26 pcu_projection         = σ(h0[M16,L2])     # Curvature → PCU
  D27 rpu_projection         = σ(h0[M4,L2])      # Max → RPU
  D28 ndu_projection         = σ(h0[M20,L2])     # Entropy → NDU
  D29 projection_confidence  = σ(h0[M22,L2])     # Regularity → confidence
```

### 7.2 SRP Final Computation (Mechanisms → 19D)

The SRP model reads from AED, CPD, C0P mechanisms using sub-section means:

```python
# ─── INPUT SLICING ───────────────────────────────────────────────────
# AED (30D)
aed_arousal     = mean(AED[0:8])       # Arousal dynamics
aed_expectancy  = mean(AED[8:16])      # Expectancy affect
aed_dynamics    = mean(AED[16:24])     # Motor-affective coupling
aed_regulation  = mean(AED[24:28])     # Regulation
aed_integration = mean(AED[28:30])     # Integration summary

# CPD (30D)
cpd_buildup     = mean(CPD[0:10])      # Trigger + buildup features
cpd_climax      = mean(CPD[10:18])     # Climax proximity
cpd_release     = mean(CPD[18:24])     # Peak response (DA release)
cpd_trajectory  = mean(CPD[24:28])     # Trajectory
cpd_intensity   = mean(CPD[28:30])     # Intensity summary

# C0P (30D)
c0p_cognitive   = mean(C0P[0:10])      # Feature aggregation
c0p_processing  = mean(C0P[10:18])     # Cognitive state
c0p_integration = mean(C0P[18:24])     # Integration
c0p_gate        = mean(C0P[24:28])     # Output gate
c0p_summary     = mean(C0P[28:30])     # Summary

# ─── LAYER N: NEUROCHEMICAL ─────────────────────────────────────────
BETA_1 = 0.84    # Salimpoor 2011: NAcc-BP ↔ pleasure, r=0.84
BETA_2 = 0.71    # Salimpoor 2011: Caudate-BP ↔ chills, r=0.71

da_caudate    = σ(0.5 * c0p_processing + 0.3 * cpd_climax + 0.2 * aed_expectancy)
da_nacc       = σ(0.6 * c0p_cognitive + 0.3 * cpd_release + 0.1 * aed_arousal)
opioid_proxy  = σ(0.4 * consonance_mean + 0.3 * resolution_signal + 0.3 * smoothness)
# where:
#   consonance_mean = mean(R³[0:7]) → H³(H18, M0, L2) — phrase-level consonance
#   resolution_signal = AED[D15] (resolution_satisfaction)
#   smoothness = R³[16] (spectral_smoothness) → H³(H18, M15, L2)

# ─── LAYER C: CIRCUIT ───────────────────────────────────────────────
vta_drive         = σ(0.5 * da_caudate + 0.5 * da_nacc)
stg_nacc_coupling = σ(0.6 * aed_arousal + 0.4 * dynamic_intensity)
prediction_error  = tanh(AED[D13])  # surprise_valence: fwd_trend - bwd_trend

# ─── LAYER P: PSYCHOLOGICAL ─────────────────────────────────────────
wanting  = σ(BETA_2 * da_caudate)          # r=0.71 Salimpoor
liking   = σ(BETA_1 * da_nacc)            # r=0.84 Salimpoor
pleasure = clamp(BETA_1 * da_nacc + BETA_2 * da_caudate, 0, 1)

# ─── LAYER T: TEMPORAL (ITPRA) ──────────────────────────────────────
tension          = σ(0.5 * cpd_buildup + 0.3 * harmonic_tension + 0.2 * AED[D14])
prediction_match = tanh(AED[D12] - AED[D11])  # prediction_pleasure - violation
reaction         = σ(0.5 * CPD[D0] + 0.5 * AED[D1])  # trigger + arousal_change
appraisal        = σ(0.4 * pleasure + 0.3 * prediction_match + 0.3 * opioid_proxy)

# ─── LAYER M: MUSICAL ───────────────────────────────────────────────
harmonic_tension  = σ(0.5 * roughness_trend + 0.3 * inv_consonance + 0.2 * entropy)
# where:
#   roughness_trend = R³[0] (roughness) → H³(H18, M18, L0) — forward trend
#   inv_consonance  = 1 - consonance_mean
#   entropy         = R³[22] (distribution_entropy) → H³(H18, M0, L2)
dynamic_intensity = σ(0.7 * energy_velocity + 0.3 * energy_acceleration)
# where:
#   energy_velocity     = R³[7] (amplitude) → H³(H18, M8, L0) — forward rate
#   energy_acceleration = R³[7] (amplitude) → H³(H18, M11, L0) — forward accel
peak_detection    = σ(0.5 * cpd_buildup + 0.5 * cpd_release)

# ─── LAYER F: FORECAST ──────────────────────────────────────────────
reward_forecast   = σ(0.6 * da_caudate + 0.4 * cpd_climax)
chills_proximity  = σ(0.5 * da_nacc + 0.3 * cpd_release + 0.2 * aed_expectancy)
resolution_expect = σ(0.6 * c0p_integration + 0.4 * aed_expectancy)

# ─── OUTPUT ASSEMBLY ─────────────────────────────────────────────────
output = [
    da_caudate, da_nacc, opioid_proxy,           # Layer N (3D)
    vta_drive, stg_nacc_coupling, prediction_error, # Layer C (3D)
    wanting, liking, pleasure,                     # Layer P (3D)
    tension, prediction_match, reaction, appraisal, # Layer T (4D)
    harmonic_tension, dynamic_intensity, peak_detection, # Layer M (3D)
    reward_forecast, chills_proximity, resolution_expect  # Layer F (3D)
]  # Total: 19D
```

---

## 8. Composer Validation Guide

### 8.1 Expected Behaviors per Musical Event

| Musical Event | wanting | liking | tension | pred_error | peak_det | da_caudate | da_nacc |
|--------------|---------|--------|---------|------------|----------|------------|---------|
| Dominant 7th chord held | **HIGH** ↑ | low | **HIGH** ↑ | ~0 (expected) | low | **RAMPING** | low |
| Resolution to tonic | drops → | **SPIKES** | drops → | +1 (confirmed) | **SPIKE** | drops | **SPIKES** |
| Crescendo toward climax | **ramps up** | moderate | **builds** | small + | building | **RAMPING** | moderate |
| Silence after climax | drops | afterglow | drops | -1 (unexpected) | possible | drops | decaying |
| Repeated predictable phrase | **decreasing** | moderate | low | ~0 | low | low | moderate |
| Unexpected modulation | **SPIKES** | depends | **SPIKES** | **-1 then +1** | possible | spikes | depends |
| Beautiful melody entering | building | **HIGH** | moderate | +1 if expected | possible | building | **HIGH** |
| Dissonant cluster | low | **VERY LOW** | **HIGH** | -1 | low | drops | low |
| Dissonance → consonance | was building | **SPIKES** | drops → | **+1** | **SPIKE** | was ramping | **SPIKES** |
| Deceptive cadence (V→vi) | **spikes further** | dip then rise | **spikes** | **-1 then +1** | possible | extends ramp | delayed spike |

### 8.2 The Chill Test

When the composer experiences goosebumps/chills at a specific moment:

```
EXPECTED SRP SIGNATURE FOR CHILLS:

-30s ─────────── -15s ────────── -5s ────── 0s (CHILL) ── +2s ── +10s
  │                │               │          │              │       │
  │  da_caudate:   │    RAMP ──────────►     │   DROP ──────────────│
  │                │   (Howe quasi-hyperbolic) │                     │
  │                │               │          │              │       │
  │  wanting:      │   FOLLOWS ────────►     │   DROP ──────────────│
  │                │   da_caudate             │                     │
  │                │               │          │              │       │
  │  tension:      │      BUILD ──────►     │   DROPS ─────────────│
  │                │               │          │              │       │
  │  da_nacc:      │               │  RAMP ─►│ SPIKE ──────► decay │
  │                │               │          │              │       │
  │  liking:       │               │          │ SPIKE ──────► decay │
  │                │               │          │              │       │
  │  opioid:       │               │  RISES ─│ PEAK ───────► decay │
  │                │               │          │              │       │
  │  pleasure:     │        BROAD ────────────── PEAK ──────► decay │
  │                │               │          │              │       │
  │  pred_error:   │               │          │ SPIKE (+1) ──► ~0   │
  │                │               │          │              │       │
  │  peak_det:     │               │          │ ████ SPIKE ██│       │
  │                │               │          │              │       │
  │  appraisal:    │               │          │    RISES ───── HIGH │
  │                │               │          │    (0.5-2s delay)   │
```

### 8.3 Validation Criteria

The composer should confirm:
1. **Temporal alignment**: wanting ramps BEFORE liking peaks — not simultaneous
2. **Emotional accuracy**: high pleasure moments match their felt experience
3. **Tension tracking**: harmonic_tension reflects actual harmonic analysis
4. **Peak precision**: peak_detection fires at actual chill/frisson moments (±1s)
5. **Deceptive cadence**: prediction_error goes negative, then wanting EXTENDS (doesn't drop)
6. **Silence after climax**: liking shows brief afterglow, not instant drop
7. **Overall narrative**: pleasure trajectory follows the piece's emotional arc

**If the composer feels chills but the model is flat → model is missing something.**
**If the model shows high values but the composer feels nothing → model is wrong.**

---

## 9. References

### Primary (α-tier causal/mechanistic evidence)

1. Salimpoor, V.N., Benovoy, M., Larcher, K., Dagher, A. & Zatorre, R.J. (2011). Anatomically distinct dopamine release during anticipation and experience of peak emotion to music. *Nature Neuroscience*, 14(2), 257-262.
2. Salimpoor, V.N., van den Bosch, I., Kovacevic, N., McIntosh, A.R., Dagher, A. & Zatorre, R.J. (2013). Interactions between the nucleus accumbens and auditory cortices predict music reward value. *Science*, 340(6129), 216-219.
3. Ferreri, L., Mas-Herrero, E., Zatorre, R.J., Ripollés, P., Gomez-Andres, A., Alicart, H., Olivé, G., Marco-Pallarés, J., Antonijoan, R.M., Valle, M., Riba, J. & Rodriguez-Fornells, A. (2019). Dopamine modulates the reward experiences elicited by music. *PNAS*, 116(9), 3793-3798.
4. Mas-Herrero, E., Dagher, A., Farres-Franch, M. & Zatorre, R.J. (2021). Unraveling the temporal dynamics of reward signals in music-induced pleasure with TMS. *Journal of Neuroscience*, 41(17), 3889-3900.
5. Cheung, V.K., Harrison, P.M.C., Meyer, L., Pearce, M.T., Haynes, J.-D. & Koelsch, S. (2019). Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. *Current Biology*, 29(23), 4084-4092.
6. Martinez-Molina, N., Mas-Herrero, E., Rodriguez-Fornells, A., Zatorre, R.J. & Marco-Pallarés, J. (2016). Neural correlates of specific musical anhedonia. *PNAS*, 113(46), E7337-E7345.

### Neurochemistry and Circuit Evidence

7. Schultz, W. (1997). A neural substrate of prediction and reward. *Science*, 275(5306), 1593-1599.
8. Schultz, W. (2016). Dopamine reward prediction-error signalling: a two-component response. *Nature Reviews Neuroscience*, 17, 183-195.
9. Berridge, K.C. & Robinson, T.E. (2003). Parsing reward. *Trends in Neurosciences*, 26(9), 507-513.
10. Berridge, K.C. (2007). The debate over dopamine's role in reward: the case for incentive salience. *Psychopharmacology*, 191, 391-431.
11. Nummenmaa, L. et al. (2025). Pleasurable music activates cerebral μ-opioid receptors. *European Journal of Nuclear Medicine and Molecular Imaging*.
12. Mallik, A., Chanda, M.L. & Levitin, D.J. (2017). Anhedonia to music and mu-opioids. *Scientific Reports*, 7, 41952.
13. Howe, M.W., Tierney, P.L., Sandberg, S.G., Phillips, P.E.M. & Graybiel, A.M. (2013). Prolonged dopamine signalling in striatum signals proximity and value of distant rewards. *Nature*, 500, 575-579.
14. Menon, V. & Levitin, D.J. (2005). The rewards of music listening. *NeuroImage*, 28(1), 175-184.
15. Blood, A.J. & Zatorre, R.J. (2001). Intensely pleasurable responses to music correlate with activity in brain regions implicated in reward and emotion. *PNAS*, 98(20), 11818-11823.

### Theoretical Frameworks

16. Huron, D. (2006). *Sweet Anticipation: Music and the Psychology of Expectation*. MIT Press.
17. Zatorre, R.J. & Salimpoor, V.N. (2013). From perception to pleasure: Music and its neural substrates. *PNAS*, 110(S2), 10430-10437.
18. Koelsch, S. (2014). Brain correlates of music-evoked emotions. *Nature Reviews Neuroscience*, 15, 170-180.
19. Gold, B.P., Pearce, M.T., Mas-Herrero, E., Dagher, A. & Zatorre, R.J. (2019). Predictability and uncertainty in the pleasure of music: A reward for learning? *Journal of Neuroscience*, 39(47), 9397-9409.
20. Koelsch, S., Vuust, P. & Friston, K. (2019). Predictive processes and the peculiar case of music. *Trends in Cognitive Sciences*, 23(1), 63-77.

### Chills/Frisson

21. Sloboda, J.A. (1991). Music structure and emotional response. *Psychology of Music*, 19(2), 110-120.
22. Panksepp, J. (1995). The emotional sources of "chills" induced by music. *Music Perception*, 13(2), 171-207.
23. Grewe, O., Kopiez, R. & Altenmüller, E. (2009). Listening to music as a re-creative process. *PLoS ONE*, 4(5), e5776.
24. de Fleurian, R. & Pearce, M.T. (2021). Chills in music: A systematic review. *Psychological Bulletin*, 147, 890-920.
25. Goldstein, A. (1980). Thrills in response to music and other stimuli. *Physiological Psychology*, 8, 126-129.

### Temporal and Perceptual

26. Giraud, A.L. & Poeppel, D. (2012). Cortical oscillations and speech processing. *Nature Neuroscience*, 15(4), 511-517.
27. Lakatos, P. et al. (2005). An oscillatory hierarchy controlling neuronal excitability. *Journal of Neurophysiology*, 94, 1904-1911.
28. Loui, P. et al. (2017). White matter correlates of musical anhedonia. *Frontiers in Psychology*, 8, 1664.
29. Meyer, L.B. (1956). *Emotion and Meaning in Music*. University of Chicago Press.
30. Juslin, P.N. (2013). From everyday emotions to aesthetic emotions (BRECVEMA). *Physics of Life Reviews*, 10(3), 235-266.

### Added in v2.1.0 Beta Upgrade

31. Mori, K. & Zatorre, R.J. (2024). State-dependent connectivity in auditory-reward networks predicts peak pleasure experiences to music. *PLoS Biology*, 22(8), e3002732.
32. Mohebi, A., Wei, W., Pelattini, L., Kim, K. & Berke, J.D. (2024). Dopamine transients follow a striatal gradient of reward time horizons. *Nature Neuroscience*, 27, 737-746.
33. Chabin, T., Gabriel, D., Chansophonkul, T. et al. (2020). Cortical patterns of pleasurable musical chills revealed by high-density EEG. *Frontiers in Neuroscience*, 14, 565815.
34. Sachs, M.E., Kozak, M.S., Ochsner, K.N. & Baldassano, C. (2025). Emotions in the brain are dynamic and contextually dependent: using music to measure affective transitions. *eNeuro*.
35. Mas-Herrero, E., Zatorre, R.J., Rodriguez-Fornells, A. & Marco-Pallarés, J. (2014). Dissociation between musical and monetary reward responses in specific musical anhedonia. *Current Biology*, 24(6), 699-704.
