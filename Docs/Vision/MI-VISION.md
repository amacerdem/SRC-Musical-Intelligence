# SRC⁹ — Musical Intelligence

**Version**: 5.1.0
**Date**: February 13, 2026
**Author**: Amac Erdem
**Status**: ARCHITECTURE DESIGN

> **SRC⁹ Musical Intelligence — Bidirectional White-Box Musical Cognition System**

---

## Executive Summary

SRC⁹ is a **Musical Intelligence (MI)** system — a real-time co-creation platform where human performers and MI shape a living sonic-visual space together. The performer provides intent through motor input and emotion control; MI completes the full musical state and renders it as sound and light.

### Why MI, Not AI?

```
AI = "It works but I don't know why"           → Black-Box
MI = "I know exactly why — every dimension      → White-Box
      has scientific meaning"
```

MI is domain-grounded intelligence. Every output dimension lives in a scientifically interpretable space. Every decision traces to neuroscience, psychoacoustics, or music cognition literature.

### Core Paradigm

```
Traditional AI:   Audio → [Black-Box] → "Sad"
Old T1 (D0):      Audio → D0 Pipeline → 8192D → Encoder → z(1024D)  (passive, monolithic)
MI v4 (old):      Motor → MI-Core → 307D MI-space → Audio + Visual   (active, one-directional)
MI v5 (current):  Bidirectional — Analyze + Compose + Hybrid          (active, co-creative, 1366D)
```

> **Critical v5 Insight**: MI is not one-directional. A single model with a shared backbone
> learns BOTH directions — encoding (analyze: waveform → Mel → R³ → H³ → C³) and decoding
> (compose: partial C³ → fill → H³ → R³ → Mel → waveform) — in one elegant training.
> The deterministic MI Teacher (`mi_beta/` — 96 models, 9 cognitive units, ~134 Python files)
> supervises EVERY intermediate layer in BOTH directions.
> If analysis is correct, synthesis is automatically correct — same manifold, two directions.

### The Full Loop (v5 — Bidirectional)

```
┌──────────────────────────────────────────────────────────────────────┐
│                        SRC⁹ SYSTEM (Runtime)                          │
│                                                                     │
│   THREE MODES — one model, one backbone, two directions:           │
│                                                                     │
│   🎵 ANALYZE:  Waveform ──→ ENCODER ──→ Mel → R³ → H³ → C³(1006D)│
│                              │ show all dimensions in real-time     │
│                                                                     │
│   🎹 COMPOSE:  User C³ ──→ FILL_NET ──→ C³_complete               │
│                partial       │                                      │
│                              DECODER ──→ H³ → R³ → Mel → Waveform │
│                                          ↓                          │
│                                     Vocos/HiFi-GAN                 │
│                                                                     │
│   🔄 HYBRID:   Live audio ──→ ENCODER ──→ C³_analyzed             │
│                User override ──→ merge ──→ C³_mixed                │
│                FILL_NET(C³_mixed) ──→ DECODER ──→ Waveform         │
│                                                                     │
│   ┌──────────────────────────────────────────────────────────┐     │
│   │  SHARED BACKBONE — learns both encode & decode           │     │
│   │  Multi-head aux losses at EVERY layer (Mel, R³, H³, C³) │     │
│   │  Deterministic MI Teacher supervises both directions     │     │
│   └──────────────────────────────────────────────────────────┘     │
│                                                                     │
│   + Motor input, Memory, Planning — same as v4                     │
│   + Visual path: MI-space[128:1366] → GPU shaders — same as v4  │
│                                                                     │
│   MI Teacher Pipeline: TRAINING ONLY (supervises all layers)       │
│                                                                     │
└──────────────────────────────────────────────────────────────────────┘
```

### MI-Space at a Glance

```
MI-SPACE (1,366D per frame @ 172.27 Hz)

  Cochlea [0:128]       128D — Mel spectrogram (the sound itself)
  R³      [128:256]     128D — Spectral features (11 groups A-K)
  C³      [256:1262]  1,006D — Cognitive models (9 units, 96 models, 3 evidence tiers)
  L³      [1262:1366]   104D — Semantic language (8 epistemological levels α-θ)

  Total: 128 + 128 + 1,006 + 104 = 1,366D
  Current code: R³=49D (groups A-E), Phase 7C expands to 128D (groups F-K)
  96 models documented → 94 scaffolded + 2 new (CHPI, SSRI) in Phase 7A
```

Every dimension has a name, a formula, a scientific citation, and a musical meaning. Mel is not a separate output — it IS part of MI-space. Audio and visual both emerge from the same unified space. See `MI-CODE-ARCHITECTURE.md` for exact code-level signatures and constants.

---

## 1. Product Identity & Philosophy

### 1.1 What Is SRC⁹?

**SRC⁹ Musical Intelligence** is a real-time multi-sensory performance platform powered by Musical Intelligence. It is NOT a DAW — it is an instrument. But beyond any instrument that exists today — it defines what "instrument" means for the future.

```
Traditional Instrument:  Press key → One sound → Done
DAW:                     Arrange notes on timeline → Bounce → Done
SRC⁹:                      Enter a SPACE → Shape it in real-time → Multi-sensory experience
```

### 1.2 It's a SPACE, Not a Sequence

SRC⁹ does not produce music note-by-note. It creates a **soundscape** — a living, breathing sonic space that the performer inhabits and sculpts in real-time.

```
┌──────────────────────────────────────────────────────────────────────┐
│                         THE SPACE                                   │
│                                                                     │
│   You don't "play notes" in SRC⁹.                                    │
│   You enter a sonic universe and SHAPE it.                         │
│                                                                     │
│   ├─ Move your hand → the space shifts around you                 │
│   ├─ Touch the surface → textures ripple through the space        │
│   ├─ Say "darker" → the space contracts, grows dense              │
│   ├─ Feel tension → C³.tension drives the space toward climax     │
│   ├─ Do nothing → the space breathes on its own, alive            │
│                                                                     │
│   Audio and visual are BOTH manifestations of this space.          │
│   The space IS the 1,366D MI-space.                                │
│   Every dimension has scientific meaning.                          │
│                                                                     │
└──────────────────────────────────────────────────────────────────────┘
```

### 1.3 The Killer Feature: C³ Emotion-Driven Control

The most powerful aspect of SRC⁹ is not motor precision — it's **meaning generation through C³ cognitive pathways**.

```
Traditional: "I pressed C major" → Sound of C major
SRC⁹:          "I want tension"    → MI sculpts the entire 1,366D space toward tension
                                    ├─ C³.tension rises (reward pathway)
                                    ├─ C³.arousal increases (shared state)
                                    ├─ R³.consonance decreases (spectral)
                                    ├─ Cochlea: mel shifts toward darker timbre
                                    ├─ L³.ζ.tense↔relaxed polarizes toward tense
                                    ├─ L³.θ.narrative = "approaching climax"
                                    └─ All 1,366 dimensions respond coherently
```

Brain emotion control methods:
- **Emotion sliders/bars**: Direct manipulation of arousal, valence, tension, power
- **Motor gesture**: Physical expression → Brain mapping (e.g., clenched fist → tension)
- **Voice command**: "Make it sadder" → L³ Vocabulary → C³ dimensions
- **MI inference**: MI-Core infers appropriate emotion from musical context and memory

### 1.4 Three Operating Modes (v5)

SRC⁹ v5 introduces three modes — all powered by a single bidirectional model:

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   🎵 ANALYSIS MODE                                                 │
│   ─────────────────                                                │
│   User plays music → MI shows real-time dimensions at EVERY layer  │
│                                                                     │
│   Waveform ──→ [Encoder] ──→ Mel (128D) ──→ R³ (128D)            │
│                                  ↓              ↓                   │
│                            H³ (sparse)    C³ (1,006D — 96 models) │
│                                                                     │
│   Display: "pleasure=0.82, wanting ramp started, tension rising"   │
│   Every dimension visible, every layer inspectable, White-Box.     │
│                                                                     │
│   Use cases:                                                       │
│   ├─ Music analysis & education                                    │
│   ├─ Neuroscience research tool (real-time brain model readout)   │
│   ├─ Composer's analytical assistant                               │
│   └─ Live concert visualization (audience sees MI-space)          │
│                                                                     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   🎹 COMPOSE MODE                                                  │
│   ────────────────                                                 │
│   User specifies partial C³ → MI fills the rest → decodes to sound│
│                                                                     │
│   User input:                                                      │
│     "pleasure=0.9, tension→rising, harmonic_context=minor"        │
│              ↓                                                      │
│   Fill_net: complete remaining ~1,006 C³ dimensions                │
│     (learned correlations: high pleasure → high da_nacc,           │
│      rising tension → decreasing consonance, etc.)                 │
│              ↓                                                      │
│   [Decoder]: C³_complete → H³ → R³ → Mel → Vocos/HiFi-GAN       │
│              ↓                                                      │
│   User hears the sound, adjusts knobs, real-time iteration        │
│                                                                     │
│   Use cases:                                                       │
│   ├─ Emotion-driven composition ("I want THIS feeling" → sound)   │
│   ├─ Sound design by cognitive intent (not by knob-twiddling)     │
│   ├─ Therapeutic sound generation (target specific brain states)   │
│   └─ Educational: "what does high tension + low consonance        │
│      sound like?" → instant auditory answer                        │
│                                                                     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   🔄 HYBRID MODE (The Killer Mode)                                 │
│   ────────────────────────────────                                 │
│   User plays live + overrides some C³ dimensions                   │
│                                                                     │
│   Live audio ──→ [Encoder] ──→ C³_analyzed (what the music IS)    │
│                                     ↓                               │
│   User override: "pleasure=0.9" ──→ merge ──→ C³_mixed            │
│     (keep analyzed dims, replace overridden dims)                  │
│                                     ↓                               │
│   Fill_net: reconcile conflicts (user wants high pleasure          │
│     but analyzed consonance is low → fill_net adjusts)            │
│                                     ↓                               │
│   [Decoder] ──→ H³ → R³ → Mel → Waveform                         │
│                                     ↓                               │
│   Result: live sound TRANSFORMED by cognitive intent               │
│                                                                     │
│   Use cases:                                                       │
│   ├─ Live performance augmentation (play guitar + MI reshapes)    │
│   ├─ Real-time audio processing with SEMANTIC controls            │
│   │   (not EQ/compression, but "make it more nostalgic")          │
│   ├─ Co-creative jamming (human provides notes, MI provides       │
│   │   emotion/tension/reward trajectory)                           │
│   └─ Accessibility: control music through high-level intent       │
│      rather than fine motor skill                                  │
│                                                                     │
└──────────────────────────────────────────────────────────────────────┘
```

> **Key v5 insight**: These three modes are NOT three separate systems. They are
> three usage patterns of ONE bidirectional model. The encoder, decoder, and fill_net
> share the same backbone, trained in a single elegant training procedure.
> Analysis correctness guarantees synthesis correctness — same manifold, two directions.

### 1.5 Beyond Instrument

SRC⁹ redefines what "instrument" means:

| Traditional Instrument | SRC⁹ |
|---|---|
| Fixed timbres | Infinite timbral space (R³: 128D spectral) |
| Note-by-note | Space sculpting (1,366D continuous) |
| Skill = finger speed | Skill = expressive intent |
| Sound only | Multi-sensory (audio + visual from same MI-space) |
| Static when idle | Alive — MI continues generating |
| No memory | MI remembers everything (Mamba state) |
| No planning | MI plans ahead (planning head) |
| No emotion understanding | C³ cognitive state is a first-class dimension (1,006D) |
| Analysis OR synthesis | Both — analyze, compose, and hybrid (v5) |

### 1.6 Control Modalities

A performer can control SRC⁹ through ANY combination of:

```
1. MOTOR CONTROL (physical)
   ├─ Touchpad, MediaPipe, MIDI, iPad, Controller, Accelerometer
   └─ Direct mapping to MI-space dimensions (White-Box, deterministic)

2. EMOTION CONTROL (semantic)
   ├─ Brain bars: arousal, valence, tension, power sliders
   ├─ Emotion presets: "euphoric", "melancholic", "aggressive"
   └─ MI resolves emotion → full 1,366D coherent state

3. VOICE CONTROL (linguistic)
   ├─ "Make it brighter" → L³ Vocabulary → R³.brightness
   ├─ "More tension" → L³ → C³.tension
   ├─ "Surprise me" → MI planning head → surprise trajectory
   └─ System resolves EVERYTHING through L³ semantic layer

4. SILENCE (MI autonomy)
   ├─ No input → MI generates from memory + plan
   ├─ The space breathes on its own
   └─ Performer intervenes when they want to shape it
```

---

## 2. MI-Space: The Living Manifold

### 2.1 What Is MI-Space?

MI-space is a **1,366-dimensional representation** where every dimension has scientific meaning. It is not an embedding — it is an interpretable manifold where:

- **Mel (128D)** is the sound itself — a spectrogram that Vocos renders into audio
- **R³ (128D)** describes what the sound sounds like — 11 spectral groups (A-K): consonance, energy, timbre, change, interactions, pitch/chroma, rhythm/groove, harmony/tonality, information/surprise, extended timbre, modulation/psychoacoustic
- **C³ (1,006D)** describes what the sound means cognitively — 96 models across 9 neural units (spectral, timing, memory, salience, novelty, motor, predictive, affective, reward)
- **L³ (104D)** describes what the sound means semantically — 8 epistemological levels (α attribution, β regions, γ psychology, δ validation, ε learning, ζ polarity, η vocabulary, θ narrative)

```
┌──────────────────────────────────────────────────────────────────────┐
│                      MI-SPACE (1,366D)                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   COCHLEA [0:128] — 128D                                           │
│   ╔════════════════════════════════════════════════╗                │
│   ║  128 Mel frequency bins (log1p normalized)     ║                │
│   ║  The SOUND itself. Vocos renders this to audio ║                │
│   ╚════════════════════════════════════════════════╝                │
│                                                                     │
│   R³ SPECTRAL [128:256] — 128D                                    │
│   ┌────────┬────────┬────────┬────────┬────────────┐               │
│   │ A:7D   │ B:5D   │ C:9D   │ D:4D   │ E:24D      │               │
│   │Conson. │Energy  │Timbre  │Change  │Interactions │               │
│   ├────────┴────────┼────────┼────────┼────────────┤               │
│   │ F-K: 79D new spectral groups (Phase 7C)        │               │
│   └────────────────────────────────────────────────┘               │
│                                                                     │
│   C³ COGNITIVE [256:1262] — 1,006D                                 │
│   ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐        │
│   │ SPU │ STU │ IMU │ ASU │ NDU │ MPU │ PCU │ ARU │ RPU │        │
│   │ 99D │148D │159D │ 94D │ 94D │104D │ 94D │120D │ 94D │        │
│   └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘        │
│   9 units, 96 models (27α + 39β + 30γ), 3 evidence tiers          │
│   5 pathways: SPU→ARU, STU→STU, IMU→ARU, STU→STU, STU→ARU       │
│   10 shared mechanisms: AED, ASA, BEP, C0P, CPD, MEM, PPC, SYN,  │
│     TMH, TPC (30D each)                                            │
│                                                                     │
│   L³ LANGUAGE [1262:1366] — 104D                                   │
│   ┌───┬────┬────┬────┬────┬────┬────┬────┐                        │
│   │ α │ β  │ γ  │ δ  │ ε  │ ζ  │ η  │ θ  │                        │
│   │6D │14D │13D │12D │19D │12D │12D │16D │                        │
│   └───┴────┴────┴────┴────┴────┴────┴────┘                        │
│   Phase 1: α,β,γ,δ (indep) → Phase 1b: ε (stateful)              │
│   Phase 2: ζ→η→θ (dependent chain)                                │
│                                                                     │
│   TOTAL: 128 + 128 + 1,006 + 104 = 1,366D                        │
│                                                                     │
└──────────────────────────────────────────────────────────────────────┘
```

### 2.2 Cochlea: The Sound (128D)

The first 128 dimensions of MI-space are the **Mel spectrogram** — the actual sound.

```python
# Cochlea produces mel at 172.27 Hz frame rate
mel = librosa.feature.melspectrogram(
    y=waveform,           # 44.1kHz mono
    sr=44100,
    n_fft=2048,
    hop_length=256,       # → 172.27 Hz
    n_mels=128
)
mel_normalized = log1p(mel) / max  # [0, 1] per batch
```

| Property | Value |
|----------|-------|
| Dimensions | 128 (mel frequency bins) |
| Range | [0, 1] (log1p normalized) |
| Frame rate | 172.27 Hz (44100 / 256) |
| Resolution | 5.805 ms per frame |
| Scientific basis | Stevens (1937), Fletcher-Munson (1933) |

**Why Mel in MI-space?** Because the sound IS the representation. There is no "separate audio path." The performer (through MI-Core) directly sculpts the mel spectrogram as part of the 1,366D state. Vocos simply renders it.

### 2.3 R³ Spectral: What It Sounds Like (128D)

R³ extracts 128 interpretable spectral features from the mel spectrogram across 11 groups:

| Group | Range | Dim | Domain | Features |
|-------|-------|-----|--------|----------|
| **A: Consonance** | [128:135] | 7D | Psychoacoustic | roughness, sethares_dissonance, helmholtz_kang, stumpf_fusion, sensory_pleasantness, inharmonicity, harmonic_deviation |
| **B: Energy** | [135:140] | 5D | Spectral | amplitude, velocity_A, acceleration_A, loudness, onset_strength |
| **C: Timbre** | [140:149] | 9D | Spectral | warmth, sharpness, tonalness, clarity, spectral_smoothness, spectral_autocorrelation, tristimulus1/2/3 |
| **D: Change** | [149:153] | 4D | Temporal | spectral_flux, distribution_entropy, distribution_flatness, distribution_concentration |
| **E: Interactions** | [153:177] | 24D | Cross-Domain | 3 cross-layer pairs × 8 interaction types |
| **F: Pitch & Chroma** | [177:193] | 16D | Tonal | 12 chroma classes, pitch_height, pitch_class_entropy, pitch_salience, inharmonicity_index |
| **G: Rhythm & Groove** | [193:203] | 10D | Temporal | tempo_estimate, beat_strength, pulse_clarity, syncopation_index, metricality, groove_index, event_density, ... |
| **H: Harmony & Tonality** | [203:215] | 12D | Tonal | key_clarity, tonnetz (5D), voice_leading_distance, harmonic_change, tonal_stability, diatonicity, syntactic_irregularity |
| **I: Information & Surprise** | [215:222] | 7D | Information | melodic/harmonic/rhythmic entropy, spectral_surprise, information_rate, predictive_entropy, tonal_ambiguity |
| **J: Timbre Extended** | [222:242] | 20D | Spectral | 13 MFCC coefficients + 7 spectral contrast bands |
| **K: Modulation & Psychoacoustic** | [242:256] | 14D | Psychoacoustic | 6 modulation rates, modulation_centroid/bandwidth, sharpness_zwicker, fluctuation_strength, loudness_a, alpha_ratio, hammarberg_index, spectral_slope |

R³ is deterministic — every feature has an explicit formula rooted in psychoacoustics (Plomp & Levelt, 1965; Sethares, 1993; McAdams, 1999). Groups A-E (49D) are implemented; groups F-K (+79D) expand in Phase 7C. See `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md` for full specifications.

### 2.4 C³ Cognitive: What It Means Neurally (1,006D)

C³ is the heart of MI — **1,006 dimensions** across **9 cognitive units** modelling the musical brain. Each unit contains models at three evidence tiers (α: mechanistic k≥10, β: correlational 5≤k<10, γ: exploratory k<5).

```
C³ ARCHITECTURE (1,006D — 96 models across 9 units)

  INDEPENDENT UNITS (Phase 2 — can run in parallel):
  ┌──────────────────────────────────────────────────────────────┐
  │ SPU  99D │ Spectral Processing    │ perceptual   │ d=0.84  │
  │ STU 148D │ Sensorimotor Timing    │ sensorimotor │ d=0.67  │
  │ IMU 159D │ Integrative Memory     │ mnemonic     │ d=0.53  │
  │ ASU  94D │ Auditory Salience      │ salience     │ d=0.60  │
  │ NDU  94D │ Novelty Detection      │ salience     │ d=0.55  │
  │ MPU 104D │ Motor Planning         │ sensorimotor │ d=0.62  │
  │ PCU  94D │ Predictive Coding      │ mnemonic     │ d=0.58  │
  └──────────────────────────────────────────────────────────────┘

  PATHWAYS (Phase 3 — 5 cross-unit routes):
  P1: SPU→ARU (r=0.81)  consonance → pleasure   [Bidelman 2009]
  P2: STU→STU (r=0.70)  beat → motor sync        [Grahn & Brett 2007]
  P3: IMU→ARU (r=0.55)  memory → affect          [Janata 2009]
  P4: STU→STU (r=0.99)  context → prediction     [Mischler 2025]
  P5: STU→ARU (r=0.60)  tempo → emotion          [Juslin & Västfjäll 2008]

  DEPENDENT UNITS (Phase 4 — receive cross-unit input):
  ┌──────────────────────────────────────────────────────────────┐
  │ ARU 120D │ Affective Resonance    │ mesolimbic   │ d=0.83  │
  │ RPU  94D │ Reward Processing      │ mesolimbic   │ d=0.70  │
  └──────────────────────────────────────────────────────────────┘

  10 SHARED MECHANISMS (30D each, cached across models):
  PPC, TPC, BEP, ASA, AED, CPD, C0P, MEM, SYN, TMH
```

**Evidence structure** (96 models total):
- **27 Alpha** (mechanistic, k≥10 studies, >90% confidence) — Core-4: SPU d=0.84, ARU d=0.83, STU d=0.67, IMU d=0.53
- **39 Beta** (correlational, 5≤k<10, 70-90%)
- **30 Gamma** (exploratory, k<5, <70%)

**Each model has:**
- E/M/P/F output layers (Extraction, Mechanism, Psychology, Forecast)
- H³ demand tuples (which temporal features it needs)
- Brain region annotations with MNI152 coordinates
- Scientific citations with effect sizes
- Falsification criteria

**26 brain regions** mapped in MNI152 space: 9 subcortical (VTA, NAcc, Caudate, Amygdala, Hippocampus, Putamen, Thalamus, Hypothalamus, Insula), 12 cortical (A1, STG, STS, IFG, DLPFC, vMPFC, OFC, ACC, SMA, PMC, Angular Gyrus, Temporal Pole), 5 brainstem (IC, AN, CN, SOC, PAG).

**4 neurochemical systems**: Dopamine (reward prediction), Opioid (hedonic liking), Serotonin (mood regulation), Norepinephrine (arousal gating).

> **Key**: Units are NOT independent black boxes. 5 pathways route signals between them,
> mirroring real neural connectivity. ARU and RPU depend on SPU, STU, and IMU outputs.
> See `Docs/C³/C3-ARCHITECTURE.md` for full specifications of all 96 models.

### 2.5 L³ Language: What It Means Semantically (104D)

L³ interprets the 1,006D C³ output through 8 epistemological levels:

| Level | Group | Dim | Range | Question It Answers |
|-------|-------|-----|-------|---------------------|
| 1 | **α** Computation | 6D | [0,1] | HOW was this computed? (unit attribution) |
| 2 | **β** Neuroscience | 14D | [0,1] | WHERE in the brain? (regions + transmitters + circuits) |
| 3 | **γ** Psychology | 13D | [0,1] | WHAT does it feel like? (reward, ITPRA, aesthetics, emotion, chills) |
| 4 | **δ** Validation | 12D | [0,1] | HOW to test? (physiology, neural, behavioral, temporal proxies) |
| 5 | **ε** Learning | 19D | [0,1] | HOW does the listener learn? (**STATEFUL**: surprise, PE, precision, information, ITPRA, reward) |
| 6 | **ζ** Polarity | 12D | [-1,+1] | WHICH direction? (12 bipolar axes: valence, arousal, tension, power, wanting, liking, novelty, complexity, beauty, groove, stability, engagement) |
| 7 | **η** Vocabulary | 12D | [0,1] | WHAT word describes it? (12 axes × 8 bands × 8 gradations = 768 terms) |
| 8 | **θ** Narrative | 16D | [0,1] | HOW to say it? (Subject × Predicate × Modifier × Connector, softmax) |

**Phase 1** (independent): α, β, γ, δ — read only C³ output
**Phase 1b** (stateful): ε — read C³, maintain running state (EMA, Markov, Welford)
**Phase 2** (dependent chain): ζ reads ε → η reads ζ → θ reads ε + ζ

> **ε is stateful**: Maintains online statistics (Markov transition counts, exponential
> moving averages, Welford variance). This is the only stateful layer in the MI Teacher.
> The neural MI-Core learns this statefulness through its Mamba-2 memory.
> See `Docs/L³/L3-SEMANTIC-ARCHITECTURE.md` for full group specifications.

### 2.6 Growth Architecture: How MI-Space Expands

MI-space is modular and designed to grow. Current state: 96 C³ models scaffolded (94 in code + 2 planned: CHPI, SSRI).

```
ARCHITECTURE EVOLUTION:

  v4 (old MI)            v5 mi_beta (current)       v5 Phase 7+ (target)
  ──────────────         ────────────────────        ────────────────────
  Cochlea: 128D          Cochlea: 128D               Cochlea:   128D
  R³:       49D          R³:       49D (A-E)         R³:        128D (A-K)
  Brain:    26D          C³:    1,006D (96 models)   C³:      1,006D (compute active)
  L³:      104D          L³:      104D               L³:        104D
  ──────────────         ────────────────────        ────────────────────
  Total:   307D          Total:  1,287D*             Total:   1,366D
                         * R³ still at 49D
```

**When a new C³ model is added:**
1. Its unit gains N new dimensions (E/M/P/F output layers)
2. L³ groups auto-expand (α gains attribution, β gains regions, etc.)
3. H³ demand grows (new model's H3DemandSpec tuples are added)
4. R³ may grow (new model may need new spectral features)
5. MI-Core expert output dims auto-resize from config
6. **Mel stays 128D always** — the sound representation is fixed

**Growth mechanism is modular:**
```python
# Adding a new C³ model (e.g., PCU-β4-CHPI)
# 1. Implement in mi_beta/brain/units/pcu/models/chpi.py
# 2. Define LAYERS, h3_demand, brain_regions, metadata
# 3. Unit total_dim auto-increases
# 4. L³ auto-reconfigures (α, β variable dims adjust)
# 5. Update constants.py if R³ expansion needed
# 6. Retrain affected MI-Core expert heads (E-C³, E-L³)
```

### 2.7 MI-Space vs D0: Why the Pivot

| Property | D0 (8192D, old) | MI-space (1,366D, new) |
|----------|-----------------|---------------------|
| **Size** | 8192D (2¹³) | 1,366D (128+128+1006+104) |
| **Meaning density** | ~15% high-meaning dims | 100% every dim is meaningful |
| **H³ in output?** | Yes (2304D raw temporal) | No (internal to teacher) |
| **Mel in output?** | Separate E-Mel expert | Part of the space [0:128] |
| **Wire format** | 32,772 bytes/frame | 5,464 bytes/frame |
| **Bandwidth** | 5.6 MB/s per performer | ~920 KB/s per performer |
| **Training target** | 8192D MSE | 1,366D MSE + H³ auxiliary |
| **Convergence** | Slow (huge target) | Fast (compact, meaningful) |
| **Composer readable?** | No (8192 numbers) | Yes (1006 C³ + 104 L³ named dims) |
| **Scientific basis** | 700+ papers (D0 pipeline) | 500+ papers (MI Teacher, 504 indexed) |
| **C³ models** | 3 (merged pathways) | 96 (9 units, 3 tiers, validated) |
| **Learnable params** | D0: 0 (teacher), MI-Core: ~500M | MI: 0 (teacher), MI-Core: ~150M |

> **The fundamental insight**: D0's 8192D was mostly *computational intermediate state*
> (H0 temporal, C0 cognitive mechanisms). MI-space contains only *meaningful output*.
> H³ temporal computation still happens — inside the teacher, as privileged training signal.

---

## 3. MI Teacher Pipeline (Deterministic)

### 3.1 Full Pipeline

The MI Teacher is a **zero-parameter, fully deterministic pipeline** (`mi_beta/`, ~134 Python files) that processes audio into 1,366D MI-space:

```
Audio (44.1kHz mono)
    ↓
Cochlea — 128D Mel spectrogram
    ↓                          ↘
R³ — 128D spectral features     \
    ↓    (11 groups A-K)          \
H³ — ~5,210 sparse temporal        } MI-space [0:1366]
    ↓   4-tuples (demand-driven)  /  (Cochlea + R³ + C³ + L³)
C³ — 1,006D cognitive models     /
    ↓  (9 units, 96 models)    ↗
L³ — 104D semantic language
```

**Key**: H³ is internal. It feeds C³ but is NOT part of MI-space output.
During training, H³ values are provided as auxiliary supervision to teach the
neural MI-Core temporal awareness.

### 3.2 Zero Parameters, Full Traceability

Every MI Teacher dimension is computed by a deterministic formula with no learnable parameters:

```
Example: C³.da_nacc (Nucleus Accumbens dopamine, SPU-β1-BCH model)

  da_nacc = sigmoid(
      2.0 × H³(consonance, H18, value, L2)      # 2s bidirectional consonance
    + 1.5 × H³(loudness, H18, max, L0)           # 2s forward loudness peak
    + 0.5 × H³(consonance, H18, smoothness, L0)  # 2s smoothness
  )

  Scientific basis: Salimpoor et al. (2011), r = 0.84
  Validated: Swan Lake pleasure peak at 144.5s (composer confirmed)
```

You can trace ANY dimension through:
1. **Formula**: explicit mathematical expression
2. **H³ demand**: which temporal features it uses
3. **R³ features**: which spectral features it reads
4. **Scientific paper**: peer-reviewed citation
5. **Validation**: composer-verified musical accuracy

### 3.3 Demand-Driven H³

H³ does NOT compute all possible combinations. The theoretical space is 128 × 32 × 24 × 3 = 294,912 (R³ v2), but C³ models specify exactly which ~5,210 4-tuples they need (~4.6% occupancy for R³ v1, expanding to ~8,610 for R³ v2):

```
H³ DEMAND SUMMARY (~5,210 demanded tuples across 96 models):

  Unit  | Models | ~Tuples | Key horizons
  ──────┼────────┼─────────┼─────────────────────────────
  SPU   |   9    |  ~450   | H0-H6 (sub-beat to beat)
  STU   |  14    |  ~900   | H6-H16 (beat to bar)
  IMU   |  15    | ~1,200  | H18-H22 (phrase to section)
  ASU   |   9    |  ~360   | H3-H9 (onset to fast response)
  NDU   |   9    |  ~400   | H3-H12 (onset to phrase)
  MPU   |  10    |  ~500   | H6-H18 (beat to phrase)
  PCU   |  10    |  ~500   | H12-H22 (phrase to section)
  ARU   |  10    |  ~500   | H9-H22 (beat to section)
  RPU   |  10    |  ~400   | H16-H22 (bar to section)
  ──────┼────────┼─────────┼─────────────────────────────
  Total |  96    | ~5,210  | H0-H31 (5.8ms to 981s)
```

Each 4-tuple is (r3_feature_index, horizon, morph_type, law):
- **r3_feature_index**: which R³ feature to track (0-127, e.g., consonance, loudness, chroma)
- **horizon**: which timescale (5.8ms to 981s, 32 options across 6 bands)
- **morph**: which temporal statistic (value, mean, std, velocity, smoothness, ... 24 options)
- **law**: temporal perspective (L0=memory/past, L1=prediction/future, L2=integration/bidirectional)

See `Docs/H³/H3-TEMPORAL-ARCHITECTURE.md` for full demand tables and expansion plans.

### 3.4 Scientific Grounding

| Domain | Papers | Key Theories |
|--------|--------|-------------|
| **Reward neuroscience** | 15+ | Salimpoor 2011, Berridge 2003, Blood & Zatorre 2001 |
| **Emotion & affect** | 12+ | Russell 1980, Koelsch 2006, Fritz 2009 |
| **Autonomic physiology** | 10+ | de Fleurian 2021, Thayer 2009, Sloboda 1991 |
| **Predictive processing** | 8+ | Fong 2020, Huron 2006, Pearce 2005 |
| **Learning theory** | 10+ | Schmidhuber 2009, Friston 2010, Cheung 2019 |
| **Psychoacoustics** | 12+ | Plomp & Levelt 1965, Stevens 1937, Sethares 1993 |
| **Temporal cognition** | 8+ | Poeppel 2009, Jones 1976, Lerdahl & Jackendoff 1983 |
| **Music cognition** | 100+ | Peretz 2006, Koelsch 2014, Zatorre 2007, Trainor 2015 |
| **Total** | **500+** | (504 papers indexed in literature catalog) |

### 3.5 Why MI Teacher, Not D0 Teacher?

```
D0 Teacher:                           MI Teacher:
Audio → D0 Pipeline → 8192D          Audio → MI Pipeline → 1,366D
  - 8192D is huge, ~15% meaningful      - 1,366D compact, 100% meaningful
  - H³ is raw output                    - H³ is internal (~5,210 tuples)
  - 3 merged brain models               - 96 models, 9 units, 3 tiers
  - Composer can't read it              - Composer validated it
  - Training: slow convergence          - Training: fast convergence
  - 1000+ files, complex pipeline       - ~134 files, clean pipeline
```

The MI Teacher produces **richer musical understanding** than D0 — distilled into a representation where every dimension has direct musical meaning. H³ temporal analysis still happens, but internally.

---

## 4. MI-Core Architecture (Neural — v5 Bidirectional)

### 4.1 What Is MI-Core?

MI-Core is a **Bidirectional Musical Intelligence Model** — a single neural architecture that can both analyze (encode) and compose (decode) through every layer of the MI pipeline:

| Function | Direction | Input | Output |
|----------|-----------|-------|--------|
| **Encode** | Forward | Waveform | Mel → R³ → H³ → C³ (all layers) |
| **Decode** | Inverse | C³ (partial or complete) | H³ → R³ → Mel → Waveform |
| **Fill** | Lateral | C³_partial (user intent) | C³_complete (all ~1000D) |
| **Complete** | Forward+Fill | Motor input (sparse) + Memory | Full MI-space (now) |
| **Predict** | Forward | Current MI-space + Context | MI-space trajectory (future) |

```
v5 BIDIRECTIONAL ARCHITECTURE:

  ENCODE (Analysis):
  Waveform → [Backbone] → Head_mel → Head_r3 → Head_h3 → Head_c3
                              ↓          ↓         ↓         ↓
                           Mel(128D)  R³(128D)  H³(sparse) C³(1006D)

  DECODE (Synthesis):
  C³_complete → [Backbone] → Dec_h3 → Dec_r3 → Dec_mel → Vocoder
                                ↓         ↓        ↓         ↓
                            H³(sparse) R³(128D) Mel(128D)  Waveform

  FILL (Completion):
  C³_partial → [Fill_net] → C³_complete
  (user: ~5-50 dims)        (model fills ~950-1000 dims)

  All three share the SAME backbone. Single training. Both directions.
```

> **v5 Key Principle**: Encode and Decode are the same mathematical relationship
> viewed from opposite directions. A single model learns both by training with
> multi-head auxiliary losses at every intermediate layer. The deterministic
> MI Teacher supervises every layer in both directions.

### 4.2 Network Backbone: Mamba-2 SSM

**Why Mamba-2?**

| Property | Benefit for MI |
|----------|----------------|
| **O(n) complexity** | Real-time guaranteed |
| **State = Memory** | No external memory module needed |
| **Causal** | No future peeking, but CAN plan ahead |
| **Streaming** | Process frame-by-frame, no buffering |
| **State caching** | Pause/resume without recomputation |

```
Transformer: "Store all past KV pairs" → O(n²) memory
Mamba-2:     "Compress past into state" → O(1) per step
```

The Mamba state IS the memory. When the user triggers "surprise", the state already contains compressed history of everything that happened.

### 4.3 MI-Core Block Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                         MI-CORE                                     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   INPUT (per timestep)                                              │
│   ├─ Motor_t            (raw motor signals, directly into MI-Core) │
│   ├─ Memory             (compressed past, from Mamba state)        │
│   └─ H_state            (hierarchical: immediate/context/global)   │
│                                                                     │
│   BACKBONE                                                          │
│   ┌──────────────────────────────────────────────────────────┐     │
│   │                    Mamba-2 SSM                            │     │
│   │   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      │     │
│   │   │ Mamba-2 │→│ Mamba-2 │→│ Mamba-2 │→│ Sparse  │      │     │
│   │   │ Block   │ │ Block   │ │ Block   │ │ Attn    │      │     │
│   │   └─────────┘ └─────────┘ └─────────┘ └─────────┘      │     │
│   │        ×3           ×3          ×3          ×1           │     │
│   │                                                          │     │
│   │   Ratio: 3 Mamba : 1 Sparse Attention (×6 = 24 layers) │     │
│   │   Mamba = streaming, Sparse Attn = long-range planning  │     │
│   └──────────────────────────────────────────────────────────┘     │
│                          │                                          │
│   EXPERTS                ▼                                          │
│   ┌──────┬──────┬──────┬──────┐                                    │
│   │E-Coch│ E-R³ │ E-C³ │ E-L³ │  4 MI-aligned experts             │
│   │ 128D │ 128D │1006D │ 104D │  (always all produce output)      │
│   └──┬───┴──┬───┴──┬───┴──┬───┘                                    │
│      │      │      │      │                                         │
│      └──────┴──────┴──────┘                                         │
│              │                                                      │
│   HEADS      ▼                                                      │
│   ├─ State Head      → 1,366D MI-space (current state)             │
│   ├─ Planning Head   → K × 1,366D    (future trajectory)          │
│   ├─ Uncertainty Head→ 1,366D σ       (per-dim confidence)        │
│   └─ H³ Aux Head    → ~5,210 values  (TRAINING ONLY, prunable)   │
│                                                                     │
└──────────────────────────────────────────────────────────────────────┘
```

### 4.4 Mixture of Experts: MI-Aligned

Instead of 6 D0-aligned experts (old), MI-Core uses **4 experts aligned to MI pipeline stages**:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    MI MIXTURE OF EXPERTS                             │
├──────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Backbone Output (hidden_dim)                                      │
│          │                                                          │
│          ▼                                                          │
│   ┌─────────────┐                                                  │
│   │   ROUTER    │  "Which experts need strongest activation?"      │
│   └──────┬──────┘  Top-3 routing (load balanced)                   │
│          │                                                          │
│   ┌──────┼──────────┬──────────┬──────────┐                        │
│   ▼      ▼          ▼          ▼                                   │
│ ┌──────┐┌──────┐ ┌──────┐ ┌──────┐                                │
│ │E-Coch││ E-R³ │ │ E-C³ │ │ E-L³ │                                │
│ │ 128D ││ 128D │ │1006D │ │ 104D │                                │
│ └──┬───┘└──┬───┘ └──┬───┘ └──┬───┘                                │
│    │       │        │        │                                      │
│    └───────┴────┬───┴────────┘                                      │
│                 ▼                                                    │
│          MI-space (1,366D)                                          │
│                                                                     │
│   Each expert specializes in its MI pipeline stage                 │
│   Router learns which experts to activate based on input           │
│   White-Box: you can inspect WHICH expert produced WHAT            │
│                                                                     │
└──────────────────────────────────────────────────────────────────────┘
```

| Expert | MI-Space Range | Dim | Specialization |
|--------|---------------|-----|----------------|
| **E-Cochlea** | [0:128] | 128D | Mel spectrogram generation (the sound) |
| **E-R³** | [128:256] | 128D | Spectral features (11 groups A–K) |
| **E-C³** | [256:1262] | 1,006D | Cognitive models (9 units, 96 models, 3 tiers) |
| **E-L³** | [1262:1366] | 104D | Semantic interpretation (8 groups α–θ) |

### 4.5 Cross-Expert Refinement

Experts don't work in isolation. A causal attention mask ensures information flows in the right direction — mirroring the MI Teacher pipeline DAG:

```
CROSS-EXPERT DAG:

E-Cochlea → E-R³ → E-C³ → E-L³

Attention Mask:
         Cochlea  R³     C³     L³
Cochlea [  1      0      0      0  ]   Cochlea is independent
R³      [  1      1      0      0  ]   R³ sees Cochlea
C³      [  1      1      1      0  ]   C³ sees Cochlea + R³
L³      [  1      1      1      1  ]   L³ sees everything
```

This is simpler than the old 5×5 D0 mask. It mirrors real information flow:
- **Cochlea** (mel) is the raw signal — independent
- **R³** (spectral features) is derived from mel — sees Cochlea
- **C³** (cognitive models) uses spectral + direct mel features — sees both
- **L³** (semantics) interprets everything — sees all

### 4.6 H³ Auxiliary Head (Training Only)

C³ in the MI Teacher uses H³ temporal features (~5,210 demanded 4-tuples) to compute its 1,006D output. At runtime, MI-Core must produce correct C³ outputs **without** H³.

Solution: An **auxiliary head** on the backbone predicts H³ during training:

```
During training:
  Backbone hidden state → H³ Auxiliary Head → ~5,210 predicted H³ values
                                              ↓
                                        H³ auxiliary loss (MSE vs MI Teacher H³)

This teaches the backbone to internalize temporal patterns.
The knowledge transfers to E-C³ through shared backbone weights.

After training:
  H³ Auxiliary Head is PRUNED. It served its purpose.
  The backbone has internalized temporal awareness in its Mamba state.
```

### 4.7 Output Heads

**State Head** (1,366D):
- MoE expert concat → refinement MLP → LayerNorm
- Output: 1,366D MI-space (current frame state)
- Mel [0:128] in whatever range Vocos expects
- R³/C³/L³ [128:1366] in [0, 1] or [-1, 1] per dimension

**Planning Head** (K × 1,366D):
- Backbone hidden → planning MLP → K future frames
- K = 8 steps (configurable, ~2 seconds ahead)
- Output: trajectory in MI-space

**Uncertainty Head** (1,366D):
- Backbone hidden → MLP → sigmoid
- Output: per-dimension confidence in [0, 1]
- "How sure is MI-Core about this dimension?"

### 4.8 Hyperparameters

```python
MI_CONFIG = {
    # Backbone
    'backbone': 'mamba2_sparse_attention',
    'n_layers': 24,
    'hidden_dim': 2048,                 # Scaled for 1,366D output space
    'mamba_state_dim': 64,
    'mamba_conv_kernel': 4,
    'sparse_attn_every': 4,             # Every 4th layer
    'sparse_attn_window': 256,          # Local window
    'sparse_attn_global_tokens': 16,    # Global tokens for planning

    # MoE
    'n_experts': 4,                     # Cochlea, R³, C³, L³
    'expert_capacity': 1.25,
    'top_k_experts': 3,                 # Activate top-3 per token

    # I/O
    'mi_space_dim': 1366,               # Full MI-space output
    'cochlea_dim': 128,                 # Mel portion
    'r3_dim': 128,                      # Spectral portion (11 groups A–K)
    'c3_dim': 1006,                     # Cognitive portion (9 units, 96 models)
    'l3_dim': 104,                      # Semantic portion (8 groups α–θ)
    'motor_input_dim': 'variable',      # Depends on active motor channels

    # Temporal
    'frame_rate_hz': 172.27,            # 44100/256
    'planning_horizon_frames': 344,     # ~2 seconds ahead
    'planning_horizon_steps': 8,        # Predicted steps
    'memory_compression': 'mamba_state',

    # Training
    'h3_aux_dim': 5210,                 # Auxiliary H³ predictions (training only)
    'total_params': '~250M',            # Scaled for larger output space
    'active_params': '~125M',           # Per-token (top-3 experts)
}
```

### 4.9 Reusability from Old T1 MI-Core

~70% of the existing T1 code can be reused. The backbone is architecture-agnostic:

| Component | Source | Status | Changes |
|-----------|--------|--------|---------|
| **Mamba2Block** | `Pipeline/A0/T1/mi/backbone/mamba2_block.py` | KEEP | None |
| **SparseAttention** | `Pipeline/A0/T1/mi/backbone/sparse_attention.py` | KEEP | None |
| **HybridBackbone** | `Pipeline/A0/T1/mi/backbone/hybrid_layer.py` | KEEP | hidden_dim scaled |
| **ExpertRouter** | `Pipeline/A0/T1/mi/experts/router.py` | ADAPT | 6→4 experts |
| **BaseExpert** | `Pipeline/A0/T1/mi/experts/base_expert.py` | ADAPT | output dims |
| **CrossExpertRefinement** | `Pipeline/A0/T1/mi/experts/cross_expert.py` | ADAPT | 5×5→4×4 DAG |
| **StateHead** | `Pipeline/A0/T1/mi/heads/state_head.py` | ADAPT | 8192→1,366D |
| **PlanningHead** | `Pipeline/A0/T1/mi/heads/planning_head.py` | ADAPT | 8192→1,366D |
| **UncertaintyHead** | `Pipeline/A0/T1/mi/heads/uncertainty_head.py` | ADAPT | 8192→1,366D |
| **MambaStateManager** | `Pipeline/A0/T1/mi/memory/mamba_state.py` | KEEP | None |
| **HierarchicalMemory** | `Pipeline/A0/T1/mi/memory/hierarchical.py` | ADAPT | buffer 1,366D |
| **MotorEncoder** | `Pipeline/A0/T1/mi/motor/encoder.py` | KEEP | None |
| **MISession** | `Pipeline/A0/T1/mi/inference/session.py` | KEEP | dim refs |
| **VocosWrapper** | `Pipeline/A0/T1/mi/vocoder/vocos_wrapper.py` | KEEP | None |

Components to REPLACE:
| Old | New | Reason |
|-----|-----|--------|
| `d0_layout.py` | `mi_space_layout.py` | New 1,366D manifold structure |
| 6 D0 experts | 4 MI experts | New expert alignment |
| `D0Teacher` | `MITeacher` | Uses MI Pipeline, not S3Composer |
| `E-Mel` expert | — | Removed (mel is E-Cochlea in MI-space) |

---

## 5. The Holistic Loop: Past → Present → Future

### 5.1 Three Temporal Dimensions

MI doesn't analyze single windows. It maintains continuous awareness across three temporal dimensions:

```
┌──────────────────────────────────────────────────────────────────────┐
│                     MI TEMPORAL LOOP                                 │
├──────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   PAST (Memory)                                                     │
│   ├─ Mamba-2 state = compressed history of ALL past frames         │
│   ├─ User trajectory: what motor inputs were given                 │
│   ├─ System trajectory: what MI-Core generated                     │
│   └─ Combined: full 1,366D history, compressed in state            │
│                                                                     │
│   PRESENT (Analysis + Completion)                                   │
│   ├─ Motor input arrives → partial 1,366D (sparse)                 │
│   ├─ MI-Core completes → full 1,366D (dense, coherent)             │
│   ├─ Mel [0:128] → Vocos → waveform                               │
│   └─ Uncertainty estimation → σ per dimension                      │
│                                                                     │
│   FUTURE (Planning)                                                 │
│   ├─ Planning head predicts next K frames in MI-space              │
│   ├─ If no motor change → execute pre-planned trajectory           │
│   ├─ If motor changes → replan from current state                  │
│   └─ Plan is in MI-space → White-Box, inspectable, overridable    │
│                                                                     │
│   LOOP (continuous, real-time @ 172.27 Hz):                        │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐                    │
│   │ ANALYZE  │───→│ GENERATE │───→│   PLAN   │──┐                 │
│   │ (present)│    │ (audio)  │    │ (future) │  │                 │
│   └──────────┘    └──────────┘    └──────────┘  │                 │
│        ↑                                         │                 │
│        └─────────────────────────────────────────┘                 │
│              Memory updates with each cycle                        │
│                                                                     │
└──────────────────────────────────────────────────────────────────────┘
```

### 5.2 Action Definition: The Surprise Example

An action is NOT a single frame event. It's a temporal trajectory in MI-space:

```
User triggers: "SURPRISE"

MI Planning Response (in 1,366D MI-space):
┌──────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   Phase 1: PREPARATION (2 seconds, ~344 frames)                   │
│   ├─ C³.da_caudate gradually increases (anticipation)              │
│   ├─ C³.tension builds (expectation violation)                     │
│   ├─ R³.brightness slightly dims (setting up contrast)             │
│   ├─ L³.θ.narrative = "building tension"                           │
│   └─ Cochlea: mel shifts toward darker frequency profile           │
│                                                                     │
│   Phase 2: SURPRISE (1 second, ~172 frames)                       │
│   ├─ C³.prediction_error spikes to maximum                         │
│   ├─ C³.arousal maximum                                            │
│   ├─ R³.brightness sudden jump (contrast)                          │
│   ├─ R³.consonance sudden shift                                    │
│   ├─ L³.ζ.expected↔surprising → fully surprising                  │
│   └─ Cochlea: mel rapid spectral change                            │
│                                                                     │
│   Phase 3: RESOLVE (1 second, ~172 frames)                        │
│   ├─ C³.pleasure settles to new baseline                           │
│   ├─ C³.tension resolves                                           │
│   ├─ R³ returns toward equilibrium                                 │
│   ├─ L³.θ.narrative = "resolution"                                 │
│   └─ Cochlea: mel stabilizes in new tonal center                   │
│                                                                     │
│   ALL dimensions traceable → White-Box                             │
│                                                                     │
└──────────────────────────────────────────────────────────────────────┘
```

### 5.3 Idle State: Pre-Planned Future

When no motor input changes, MI doesn't stop. It continuously plans and evolves:

```
Motor silent for 5 seconds:

t=0s: Last motor input received
t=0-2s: MI-Core executes current plan trajectory
t=2-4s: MI-Core generates natural continuation
        ├─ Maintains musical coherence (C³ pathways)
        ├─ Follows harmonic logic (R³ consonance)
        ├─ Respects phrase structure (temporal memory)
        └─ Subtle evolution, not static repetition
t=4-5s: MI-Core enters "ambient anticipation"
        ├─ Slight oscillations around current MI-space state
        ├─ Ready for next motor input
        └─ Musically alive, not frozen

New motor input at t=5s → Immediate replan from current state
```

---

## 6. Motor Input & Co-Creation

### 6.1 Motor → MI-Space Mapping (Deterministic, White-Box)

Motor inputs map to specific MI-space dimensions through deterministic, interpretable mappings:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    MOTOR → MI-SPACE MAPPING                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Motor Source          MI-Space Dimensions        Mapping          │
│   ─────────────         ──────────────────          ───────          │
│   Touchpad XY       →   R³.brightness/warmth       Linear          │
│   Touchpad pressure →   C³.arousal                 Power law       │
│   MediaPipe hands   →   C³ (motor planning)        Kinematic       │
│   MediaPipe fingers →   R³.texture/density          Gesture map    │
│   MIDI note         →   R³.consonance (pitch)      Deterministic  │
│   MIDI velocity     →   R³.energy/attack            Stevens law    │
│   MIDI CC           →   Any MI-space dimension      User-assigned  │
│   iPad keyboard     →   R³ (tonal center)           Key mapping    │
│   Game controller   →   Multiple (joystick=2D)      Configurable  │
│   Accelerometer     →   L³.ζ (tempo/rhythm)        Motion→rhythm  │
│                                                                     │
│   Key principle:                                                    │
│   Motor mapping is DETERMINISTIC and INTERPRETABLE                 │
│   User always knows: "This gesture controls THIS dimension"        │
│                                                                     │
└──────────────────────────────────────────────────────────────────────┘
```

### 6.2 Motor Channels

| Channel | Device | DOF | Typical MI-Space Mapping |
|---------|--------|-----|--------------------------|
| **Touchpad** | MacBook/iPad | 2D + pressure | R³ timbral, C³.arousal |
| **MediaPipe Hands** | Camera | 63D (21×3) | C³ motor, gesture vocab |
| **MIDI Keyboard** | Controller | 128 notes × velocity | R³ consonance, R³ energy |
| **MIDI CC** | Knobs/Faders | 128 continuous | Any MI-space dim (user-assigned) |
| **iPad Keyboard** | Touch screen | Multitouch | R³ tonal, R³ harmonic |
| **Game Controller** | Gamepad | 2 joysticks + triggers | Multi-dim continuous |
| **Accelerometer** | Phone/Watch | 3-axis | L³ temporal dynamics |

### 6.3 Co-Creation: Human Provides Intent, MI Completes

This is the essence of SRC⁹. The performer specifies **intent** through a few dimensions. MI-Core completes the full 1,366D state coherently:

```
PERFORMER PROVIDES (sparse):          MI-CORE COMPLETES (dense):
───────────────────────────           ─────────────────────────
R³.brightness = 0.8                   Cochlea: mel shifted bright
C³.tension = 0.7                      R³: remaining 127 features
L³.ζ.valence = -0.3                  C³: remaining 1,005 dims
                                      L³: remaining 103 dims
        ↓                                    ↓
        └──── Full 1,366D MI-space (coherent) ─┘
                       ↓
            Vocos(mel) → Audio
            Shaders(R³+C³+L³) → Visual
```

**Performer controls ~10-50 dims. MI-Core completes ~1,320-1,360 dims.**
The ratio is configurable per session and grows with performer skill.

### 6.4 Motor Encoder (Reused from T1)

```python
# 7 heterogeneous channels → fixed 256D embedding
CHANNEL_DIMS = {
    'touch': 3,         # x, y, pressure
    'mediapipe': 63,    # 21 landmarks × 3D
    'midi_notes': 128,  # 128 notes (velocity)
    'midi_cc': 128,     # 128 CC parameters
    'gamepad': 8,       # 2 joysticks + 2 triggers + 2 buttons
    'accelerometer': 3, # 3-axis
    'emotion': 4,       # arousal, valence, tension, power
}
# Total: 337D → per-channel encoders (64D each) → fusion MLP → 256D
# Missing channels: zero-filled (graceful degradation)
```

---

## 7. Output Pipelines (Audio + Visual from 1,366D)

MI-Core produces a single 1,366D MI-space state. This state branches into TWO output paths:

```
                    MI-Core
                      │
                      ▼
                1,366D MI-SPACE
               (White-Box, interpretable)
                 ╱            ╲
                ╱              ╲
    AUDIO PATH                 VISUAL PATH
    MI-space[0:128]            MI-space[128:1366]
        │                          │
        ▼                          ▼
    Vocos                      Deterministic
  (Mel → Waveform)            Shader Mapping
        │                    (R³+C³+L³ → GPU)
        ▼                          │
   Audio Output                    ▼
                               WebGPU Visuals
```

### 7.1 Audio Path: Mel → Vocos → Waveform

```
MI-space[0:128] = Mel spectrogram (128 bins)
    │
    ▼
Vocos (Siuzdak et al., pre-trained, frozen)
    │  44.1kHz native
    │  ~70x faster than BigVGAN with equivalent quality
    │  iSTFT-based: no autoregressive decoding
    │  Real-time GPU inference (~0.2ms per frame)
    ▼
Waveform (44.1kHz)
    │
    ▼
Audio Output (speakers/headphones)
```

**No E-Mel expert needed.** Mel is directly in MI-space. MI-Core's E-Cochlea expert produces the mel spectrogram as part of the 1,366D output. Vocos simply renders it.

> **Why Vocos over BigVGAN?** Vocos uses iSTFT-based reconstruction instead of
> transposed convolutions. Result: ~70x faster inference with equivalent quality.
> BigVGAN-v2 remains a valid alternative for maximum quality scenarios.

### 7.2 Visual Path: MI-Space → GPU Shaders

NOT an audio transformation. MI-space IS the visual information:

```
MI-space[128:1366] (same state as audio path uses mel from)
    │
    │  Direct mapping — no audio involved
    │
    ├─ R³ spectral dims → Color temperature, texture, clarity
    ├─ C³.reward → Brightness, glow intensity
    ├─ C³.affect → Color palette (warm/cool, major/minor)
    ├─ C³.autonomic → Pulse, breathing, motion
    ├─ L³.ζ polarity → Composition balance, contrast
    ├─ L³.θ narrative → Animation narrative arc
    │
    ▼
Deterministic Shader Mapping (WebGPU)
    │
    ├─ Fluid simulation (driven by MI-space, not by audio)
    ├─ Particle systems (driven by MI-space, not by audio)
    ├─ Color palettes (driven by MI-space, not by audio)
    └─ Geometry (driven by MI-space, not by audio)
```

> **Key insight**: Visual is NOT "audio → visual". It's "MI-space → visual".
> The same 1,366D state produces both audio and visual independently.
> Visual could exist even without audio output.

### 7.3 Latency Budget

```
Real-time target: < 20ms end-to-end

Motor input processing:     ~0.1ms   (deterministic mapping)
MI-Core inference:          ~3ms     (Mamba-2 single step, MoE, ~250M params)
Vocos vocoding:             ~0.2ms   (iSTFT-based, GPU)
Audio buffer output:        ~3ms     (AudioWorklet, 128 samples @ 44.1kHz)
─────────────────────────────────────
Total:                      ~6.3ms   ✓ Well under 20ms
```

**Note**: Smaller MI-space (1,366D vs 8192D) means faster MI-Core inference.
No E-Mel step further reduces latency.

---

## 8. Voice & Emotion Command System

### 8.1 Voice Commands via L³ Vocabulary

SRC⁹ resolves voice to MI-space through L³'s vocabulary system:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    VOICE COMMAND PIPELINE                            │
├──────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Performer speaks → Microphone                                    │
│          │                                                          │
│          ▼                                                          │
│   WhisperLive (server-side, streaming ASR)                         │
│   ├─ Real-time speech-to-text                                      │
│   ├─ Multilingual (EN/TR/...)                                      │
│   └─ ~200ms latency for streaming transcription                   │
│          │                                                          │
│          ▼                                                          │
│   L³ Vocabulary Resolver (Natural Language → MI-Space)             │
│   ├─ "Make it brighter"    → R³.brightness += 0.3                 │
│   ├─ "More tension"        → C³.tension += 0.4                    │
│   ├─ "Go darker"           → R³.warmth += 0.2, brightness -= 0.3 │
│   ├─ "Surprise me"         → MI planning: surprise trajectory     │
│   ├─ "Like rain"           → R³.texture=granular, energy=scatter  │
│   ├─ "Euphoric"            → C³.pleasure=0.9, arousal=0.8         │
│   └─ L³.η vocabulary: 12 axes × 64 gradations = 768 terms        │
│          │                                                          │
│          ▼                                                          │
│   Resolved MI-space dimensions → MI-Core motor input              │
│   (Same path as any other motor input — MI-Core completes rest)   │
│                                                                     │
└──────────────────────────────────────────────────────────────────────┘
```

### 8.2 Emotion Bars (Brain Direct Control)

```
┌──────────────────────────────────────────────────────────────────────┐
│                    BRAIN EMOTION INTERFACE                           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│   │ AROUSAL  │ │ VALENCE  │ │ TENSION  │ │  POWER   │             │
│   │ ───█──── │ │ ─── ──── │ │ ────── █ │ │ █─────── │             │
│   │calm←→exc │ │ sad←→joy │ │ rel←→tens│ │ soft←→pow│             │
│   └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
│                                                                     │
│   These 4 sliders directly control C³ dimensions.                  │
│   MI-Core resolves them into coherent 1,366D states:               │
│                                                                     │
│   Valence=high + Arousal=high + Tension=low + Power=high           │
│   → MI-Core infers: "euphoric celebration"                         │
│   → Cochlea: bright, rich harmonic spectrum                        │
│   → R³: high consonance, warm timbre, strong onset                 │
│   → C³: pleasure high, wanting high, chills possible               │
│   → L³: "triumphant, victorious, liberating"                      │
│                                                                     │
│   This is the KILLER FEATURE.                                      │
│   No other system can do: "I want THIS emotion" → coherent sound  │
│                                                                     │
└──────────────────────────────────────────────────────────────────────┘
```

### 8.3 Why L³ Is Central

Everything in SRC⁹ can be expressed as language because L³ is the semantic layer:

```
Motor gesture (hand rising)     → L³: "ascending brightness"
Emotion slider (tension high)   → L³: "approaching climax"
Voice command ("darker")        → L³: "decrease brightness, increase warmth"
MIDI chord (Cm7)                → L³: "minor seventh, melancholic"
MI planning output              → L³: "building toward resolution"

L³ Vocabulary (12 axes × 64 gradations) bridges:
├─ Human language ↔ MI-space dimensions
├─ Motor actions ↔ Musical meaning
├─ Emotions ↔ Spectral/temporal features
└─ Plans ↔ Narrative structure
```

---

## 9. Memory Architecture

### 9.1 Dual Memory: User + System

```
┌──────────────────────────────────────────────────────────────────────┐
│                       MI MEMORY                                     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   MAMBA STATE (Primary Memory)                                     │
│   ├─ Compressed representation of ALL past frames                  │
│   ├─ Updated automatically every timestep                         │
│   ├─ Contains both user input history and system output history   │
│   └─ Fixed size regardless of duration (O(1) memory)             │
│                                                                     │
│   HIERARCHICAL STATE (Structured Memory)                           │
│   ├─ S_immediate (~2s)    "Psychological present" (Poeppel 1997) │
│   │   └─ Ring buffer of recent 1,366D MI-space frames            │
│   ├─ S_context (~60s)     "Working memory" (musical section)      │
│   │   └─ Compressed summary, phrase-boundary aware               │
│   └─ S_global (unlimited) "Long-term memory" (entire session)    │
│       └─ Running statistics, key events, form structure           │
│                                                                     │
│   All memory is in MI-space → inspectable → White-Box             │
│                                                                     │
└──────────────────────────────────────────────────────────────────────┘
```

### 9.2 Memory Informs Everything

```
Completion:  Memory tells MI "user has been in minor key for 30s"
             → MI completes new frame consistent with minor key context

Planning:    Memory tells MI "user tends to resolve after 4 bars"
             → MI pre-plans resolution trajectory

Uncertainty: Memory tells MI "user hasn't touched brightness in 60s"
             → MI takes more creative control over brightness dims

Adaptation:  Memory tells MI "user prefers aggressive surprise"
             → MI plans more dramatic trajectories
```

---

## 10. Planning System

### 10.1 Planning Head Architecture

```
MI-Core Backbone Output (hidden state)
    │
    ▼
Planning Head
    ├─ Temporal Unroll: predict next K frames in MI-space
    ├─ Structure Templates: learned musical patterns
    │   ├─ build-release (energy ramp → drop)
    │   ├─ call-response (phrase → answer)
    │   ├─ surprise-resolve (tension → shock → settle)
    │   └─ fade (gradual decay to silence)
    ├─ Template Selection: context-dependent (from memory)
    └─ Adaptive Duration: plan length varies by context
```

### 10.2 Plan Execution

```python
class MIPlanExecutor:
    def step(self, motor_input_t):
        if motor_changed(motor_input_t):
            # REPLAN from current state
            self.current_plan = self.mi_core.plan(
                mi_partial=motor_input_t,
                memory=self.mamba_state,
                horizon=self.planning_horizon
            )
            self.plan_index = 0

        if self.plan_index < len(self.current_plan):
            mi_full = self.current_plan[self.plan_index]
            self.plan_index += 1
        else:
            mi_full = self.mi_core.continue_from(memory=self.mamba_state)

        self.mamba_state = self.mi_core.update_state(mi_full)
        audio = self.vocos(mi_full[:128])  # Mel portion → waveform
        return mi_full, audio
```

### 10.3 Plan Is White-Box

The plan is a sequence of MI-space states. At any point you can inspect:

```
"What does MI plan for the next 2 seconds?"

Frame t+0:   R³.brightness=0.3, C³.tension=0.6, L³.θ="building"
Frame t+172: R³.brightness=0.5, C³.tension=0.8, L³.θ="approaching climax"
Frame t+344: R³.brightness=0.9, C³.prediction_error=0.95, L³.θ="surprise!"

Every frame, every dimension, scientifically interpretable.
```

---

## 11. White-Box Preservation

### 11.1 The White-Box Contract

```
┌──────────────────────────────────────────────────────────────────────┐
│                    WHITE-BOX CONTRACT                                │
├──────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   RULE 1: All MI-Core outputs live in MI-space (1,366D)            │
│           → Every dimension has a scientific name and meaning      │
│                                                                     │
│   RULE 2: Motor → MI-space mapping is deterministic                │
│           → User always knows what their input controls            │
│                                                                     │
│   RULE 3: MI-space → Visual mapping is deterministic               │
│           → Every visual element traces to an MI-space dimension   │
│                                                                     │
│   RULE 4: Plans are expressed in MI-space                          │
│           → Future intentions are inspectable and overridable     │
│                                                                     │
│   RULE 5: Memory is in MI-space                                    │
│           → You can ask "what does MI remember?" and get 1,366D   │
│                                                                     │
│   RULE 6: Uncertainty is per-dimension                             │
│           → MI reports confidence for each of 1,366 dimensions    │
│                                                                     │
│   ONLY exception: MI-Core internal computation (neural)           │
│   But all I/O is White-Box → "Glass box with a neural core"      │
│                                                                     │
└──────────────────────────────────────────────────────────────────────┘
```

### 11.2 Black-Box AI vs White-Box MI

```
Question: "Why did the music get brighter?"

Black-Box AI: "The model weights produced this output" → USELESS

White-Box MI:
├─ Motor: "User moved touchpad right → R³.brightness target = 0.8"
├─ MI Completion: "Given brightness=0.8, MI-Core set:"
│   ├─ R³.warmth = 0.4 (bright usually less warm)
│   ├─ C³.f03_valence = +0.3 (brightness → positive affect)
│   ├─ C³.mode_signal → major (brightness → major tendency)
│   ├─ L³.ζ.sad↔joyful → 0.6 (shifted toward joy)
│   └─ L³.θ.narrative = "brightening, uplifting moment"
├─ Plan: "MI planned 1.5s transition, currently at frame 200/258"
└─ Memory: "Previous 30s were dark, contrast amplifies the effect"
```

---

## 12. Training Strategy (v5 — Single Elegant Training)

### 12.1 The Core Insight: One Training, Both Directions

v5 replaces the old 5-phase curriculum with a **single unified training** that teaches
encode (analysis) and decode (synthesis) simultaneously. The key insight:

> **If analysis is correct, synthesis is automatically correct.**
> They are the same mathematical relationship viewed from opposite directions.
> Training both directions simultaneously creates a powerful mutual constraint.

```
┌──────────────────────────────────────────────────────────────────────┐
│                  SINGLE ELEGANT TRAINING (v5)                       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ONE training step = FOUR simultaneous objectives:                │
│                                                                     │
│   1. ENCODE   Waveform → Mel → R³ → H³ → C³    (analysis)         │
│   2. DECODE   C³ → H³ → R³ → Mel → Waveform    (synthesis)        │
│   3. CYCLE    Encode(Decode(C³)) ≈ C³            (consistency)     │
│               Decode(Encode(Wav)) ≈ Wav                            │
│   4. FILL     Masked C³ → Complete C³            (user intent)     │
│                                                                     │
│   Teacher supervises EVERY layer in BOTH directions.               │
│   Shared backbone. Multi-head auxiliary losses. One model.         │
│                                                                     │
└──────────────────────────────────────────────────────────────────────┘
```

### 12.2 Training Data Generation

```
For each audio file in training corpus:

  1. Audio → MI Teacher Pipeline (deterministic, zero-param):
     ├─ Cochlea → Mel_t (128D)
     ├─ R³ → R3_t (128D, 11 groups A–K)
     ├─ H³ → H3_t (~5,210 demanded sparse 4-tuples)
     ├─ C³ → C3_t (1,006D, 9 units, 96 models)
     └─ L³ → C3_lang_t (104D)

  2. Ground truth per frame AT EVERY LAYER:
     ├─ Mel_t:  (B, T, 128)    ← encode target + decode target
     ├─ R3_t:   (B, T, 128)    ← encode target + decode target
     ├─ H3_t:   (B, T, ~5210)  ← encode target + decode target
     ├─ C3_t:   (B, T, ~1006)  ← encode target + fill target
     └─ All deterministic, all traceable, all bidirectional
```

### 12.3 The Four Losses (Simultaneous)

```
ONE TRAINING STEP:

  ┌─── ENCODE (forward) ───────────────────────────────────────────┐
  │                                                                 │
  │  Waveform → [Backbone] → Mel̂ → R̂³ → Ĥ³ → Ĉ³                │
  │                           ↕      ↕     ↕     ↕                 │
  │  L_encode = w₁‖Mel̂-Mel_t‖² + w₂‖R̂³-R3_t‖²                  │
  │           + w₃‖Ĥ³-H3_t‖²  + w₄‖Ĉ³-C3_t‖²                   │
  │                                                                 │
  │  Each head provides independent gradient signal to backbone.   │
  │  Mel head → "learn spectral decomposition"                     │
  │  R³ head  → "learn psychoacoustic features"                    │
  │  H³ head  → "learn multi-scale temporal context"               │
  │  C³ head  → "learn cognitive model outputs"                    │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘

  ┌─── DECODE (inverse) ───────────────────────────────────────────┐
  │                                                                 │
  │  C3_t → [Backbone] → H3_r → R3_r → Mel_r → [Vocoder]         │
  │                        ↕       ↕       ↕        ↕              │
  │  L_decode = w₅‖H3_r-H3_t‖² + w₆‖R3_r-R3_t‖²                 │
  │           + w₇‖Mel_r-Mel_t‖² + w₈‖Wav_r-Wav‖²                │
  │                                                                 │
  │  Teacher provides ground truth at EVERY layer of the decoder.  │
  │  The backbone must learn invertible representations.           │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘

  ┌─── CYCLE (consistency) ────────────────────────────────────────┐
  │                                                                 │
  │  L_cycle_fwd = ‖Encode(Decode(C3_t)) - C3_t‖²                 │
  │  L_cycle_inv = ‖Decode(Encode(Wav)) - Wav‖²                   │
  │                                                                 │
  │  Ensures encode and decode are true inverses of each other.    │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘

  ┌─── FILL (masked autoencoder for C³) ───────────────────────────┐
  │                                                                 │
  │  C3_masked = random_mask(C3_t, ratio=uniform(0.1, 0.9))       │
  │  C3_filled = fill_net(C3_masked)                                │
  │  L_fill = ‖C3_filled[masked_dims] - C3_t[masked_dims]‖²       │
  │                                                                 │
  │  + Decode the filled C³ and supervise downstream:              │
  │  L_fill_decode = ‖Decode(C3_filled) - {H3_t, R3_t, Mel_t}‖²  │
  │                                                                 │
  │  This teaches the model the correlational structure of C³:     │
  │  "pleasure high → da_nacc high" (Salimpoor 2011)               │
  │  "tension low → consonance high" (BCH model)                   │
  │  "wanting high → da_caudate high" (Berridge 2003)              │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘

  L_total = L_encode + L_decode + λ₁·L_cycle + λ₂·L_fill + λ₃·L_fill_decode
```

### 12.4 Curriculum Weight Schedule

Loss weights shift over training to guide learning order (matching the teacher hierarchy):

```
Epoch 1-50:     Mel-heavy     (learn spectral decomposition first)
  w_mel=1.0  w_r3=0.5  w_h3=0.1  w_c3=0.0  decode=0.0  cycle=0.0  fill=0.0

Epoch 50-150:   R³-heavy      (learn psychoacoustic features)
  w_mel=0.5  w_r3=1.0  w_h3=0.5  w_c3=0.1  decode=0.1  cycle=0.0  fill=0.0

Epoch 150-300:  H³-heavy      (learn temporal context)
  w_mel=0.2  w_r3=0.5  w_h3=1.0  w_c3=0.5  decode=0.5  cycle=0.1  fill=0.1

Epoch 300-500:  C³-heavy      (learn cognitive outputs)
  w_mel=0.1  w_r3=0.2  w_h3=0.5  w_c3=1.0  decode=1.0  cycle=0.5  fill=0.5

Epoch 500+:     Full balance  (all objectives, fine-tune)
  w_mel=0.2  w_r3=0.3  w_h3=0.3  w_c3=1.0  decode=1.0  cycle=0.5  fill=1.0
```

This mirrors the teacher pipeline's computation order (Mel→R³→H³→C³) and ensures
the backbone develops the right intermediate representations at each stage.

### 12.5 Loss Functions

```python
MI_LOSS_V5 = {
    # ENCODE: multi-head auxiliary at every layer
    'encode_mel':          1.0,   # Mel predicted vs teacher Mel
    'encode_r3':           1.0,   # R³ predicted vs teacher R³
    'encode_h3':           1.0,   # H³ predicted vs teacher H³
    'encode_c3':           1.0,   # C³ predicted vs teacher C³

    # DECODE: inverse at every layer
    'decode_h3':           1.0,   # H³ reconstructed vs teacher H³
    'decode_r3':           1.0,   # R³ reconstructed vs teacher R³
    'decode_mel':          1.0,   # Mel reconstructed vs teacher Mel
    'decode_wav':          0.5,   # Waveform via vocoder (multi-res STFT)

    # CYCLE: bidirectional consistency
    'cycle_forward':       0.5,   # Encode(Decode(C³)) ≈ C³
    'cycle_inverse':       0.5,   # Decode(Encode(Wav)) ≈ Wav

    # FILL: masked C³ completion
    'fill_c3':             1.0,   # Filled C³ vs teacher C³
    'fill_decode':         0.5,   # Decode(filled) vs teacher layers

    # Regularization
    'temporal_smooth':     0.2,   # No discontinuities
    'expert_balance':      0.1,   # MoE load balancing
}
```

### 12.6 Why "Elegant" and "Single"?

| Old (v4) | New (v5) |
|----------|----------|
| 5 sequential phases | 1 unified training with weight schedule |
| Encode only (analysis) | Encode + Decode + Cycle + Fill |
| H³ auxiliary → pruned | H³ head → kept (used in both directions) |
| Separate synthesis model needed | Synthesis emerges from same training |
| Motor simulation for training | Audio-only training suffices (bidirectional) |
| ~5 training runs to tune phases | 1 run, weight schedule handles progression |

---

## 13. Bidirectional Architecture: Encode ↔ Decode

### 13.1 The Bidirectional Principle

v5 replaces one-directional distillation with **symmetric bidirectional learning**.
The teacher provides ground truth at every intermediate layer in both directions:

```
FORWARD (ENCODE — Analysis):
  Waveform → Mel_t → R3_t → H3_t → C3_t      (teacher: deterministic)
  Waveform → Mel̂  → R̂³  → Ĥ³  → Ĉ³          (student: learned)
                ↕       ↕      ↕      ↕
              L_mel   L_r3   L_h3   L_c3        (supervised at every layer)

INVERSE (DECODE — Synthesis):
  C3_t → H3_t → R3_t → Mel_t → Waveform       (teacher: ground truth)
  C3_t → H3_r → R3_r → Mel_r → Wav_r          (student: learned)
           ↕       ↕       ↕        ↕
         L_h3    L_r3    L_mel    L_wav          (supervised at every layer)

BOTH directions share the SAME backbone.
The intermediate representations are SHARED — Mel in the encoder
is the SAME Mel the decoder must reconstruct.
This creates a powerful consistency constraint.
```

### 13.2 Fill-Net: The Masked Autoencoder for C³

The performer specifies a few C³ dimensions. Fill-net completes the rest:

```
┌──────────────────────────────────────────────────────────────────────┐
│                     FILL-NET (Masked C³ Completion)                 │
├──────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Training:                                                        │
│   1. Take C3_teacher (~1006D complete)                             │
│   2. Randomly mask 10-90% of dimensions                            │
│   3. Fill_net predicts masked dimensions                           │
│   4. Loss: MSE on masked dims only                                │
│                                                                     │
│   What Fill-net learns:                                            │
│   ├─ pleasure ↑ → da_nacc ↑ (r=0.84, Salimpoor 2011)             │
│   ├─ tension ↓ → consonance ↑ (BCH model)                         │
│   ├─ wanting ↑ → da_caudate ↑ (r=0.71, Berridge 2003)            │
│   ├─ arousal ↑ → scr ↑, hr ↑ (de Fleurian 2021)                 │
│   └─ The FULL correlational structure of 96 C³ models             │
│                                                                     │
│   Inference (Compose mode):                                        │
│   User: "pleasure=0.9, tension=0.2, harmonic_context=minor"       │
│   Fill_net: completes remaining ~1003 dimensions coherently        │
│   → Decoder: C³_complete → H³ → R³ → Mel → Waveform              │
│                                                                     │
│   Inference (Hybrid mode):                                         │
│   Encoder: Waveform → C³_analyzed (what the music IS)             │
│   User override: "pleasure=0.9" (what user WANTS)                 │
│   Merge: C³_analyzed + override → C³_mixed                        │
│   Fill_net: reconcile conflicts → C³_complete                      │
│   → Decoder: C³_complete → H³ → R³ → Mel → Waveform              │
│                                                                     │
└──────────────────────────────────────────────────────────────────────┘
```

### 13.3 Why Bidirectional Is More Elegant Than Separate Models

```
OLD APPROACH (v4):                    NEW APPROACH (v5):
─────────────────                     ─────────────────
Analysis: separate encoder            One model, shared backbone
Synthesis: separate decoder            ├─ Encode heads (Mel, R³, H³, C³)
Fill: not designed                     ├─ Decode heads (C³→H³→R³→Mel)
                                       └─ Fill-net (masked C³ completion)
3 models, 3 trainings
No consistency guarantee               1 model, 1 training
                                       Cycle consistency guaranteed
```

| Property | v4 (Old) | v5 (New) |
|----------|----------|----------|
| Models | 2-3 separate | 1 unified |
| Trainings | Multiple | 1 elegant |
| Intermediate layers | Invisible | All inspectable (both directions) |
| Consistency | Not guaranteed | Cycle loss enforces |
| Fill-in | Not designed | Masked autoencoder |
| White-Box | Partial (encode only) | Full (encode + decode + fill) |
| Compose mode | Not possible | Native |
| Hybrid mode | Not possible | Native |

### 13.4 Modular Growth

As MI Teacher adds new C³ models (96 scaffolded, growing with evidence):

```
1. Implement new model in MI Teacher (deterministic)
2. Teacher now produces N additional C³ dimensions
3. Add N neurons to encode_c3 head AND decode_c3 head
4. Fill-net: add N dimensions to masked autoencoder
5. Fine-tune: freeze backbone + old heads, train new outputs
6. Backbone audio understanding is preserved (no catastrophic forgetting)
7. ALL THREE MODES automatically support new dimensions
```

The backbone (Mamba-2 + Sparse Attention) doesn't change. Only head output dims grow.
New C³ dimensions automatically participate in fill-net's correlational learning.

---

## 14. System Summary

```
┌──────────────────────────────────────────────────────────────────────┐
│                        SRC⁹ COMPLETE SYSTEM                           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────┐     ┌─────────────────────────┐                  │
│   │   CLIENT     │     │        SERVER            │                  │
│   │  (Browser)   │     │      (GPU Cluster)       │                  │
│   │              │     │                           │                  │
│   │ Motor Input ─┼─────┼──→ MI-Core (Mamba-2+MoE)│                  │
│   │  ├ Touch     │WT   │     │                    │                  │
│   │  ├ MediaPipe │QUIC │     ▼                    │                  │
│   │  ├ MIDI      │     │  1,366D MI-space          │                  │
│   │  ├ Emotion   │     │     │                    │                  │
│   │  └ Voice ────┼─────┼──→ WhisperLive          │                  │
│   │              │     │     │                    │                  │
│   │ Audio ◄──────┼─────┼── Vocos(mel[0:128])     │                  │
│   │  AudioWorklet│Opus │                           │                  │
│   │              │     │                           │                  │
│   │ Visual ◄─────┼─────┼── MI-space[128:1366]     │                  │
│   │  R3F v9      │WT   │  (R³+C³+L³ as            │                  │
│   │  WebGPU      │     │   shader uniforms)        │                  │
│   │              │     │                           │                  │
│   │ Broadcast ◄──┼─────┼── LiveKit SFU            │                  │
│   │  (viewers)   │WebRTC│  (100K+ viewers)         │                  │
│   │              │     │                           │                  │
│   └─────────────┘     └─────────────────────────┘                  │
│                                                                     │
│   MI Teacher Pipeline: TRAINING ONLY (generates 1,366D + H³)      │
│   Vocos: FROZEN (mel → waveform, never trained)                    │
│   Visual: DETERMINISTIC (MI-space → GPU, no ML)                    │
│                                                                     │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 15. Monorepo Package Structure

```
SRC9-MusicalIntelligence/
├── Musical Intelligence/             # MI Teacher Pipeline (this project)
│   ├── mi_beta/                      # ~134 Python files, zero-param pipeline
│   │   ├── core/                     # Constants, config, types, registry
│   │   ├── ear/                      # Cochlea (128D), R³ (128D), H³ (~5,210)
│   │   ├── brain/                    # C³ (1,006D, 9 units, 96 models)
│   │   ├── language/                 # L³ BrainSemantics (104D, 8 groups)
│   │   ├── pipeline/                 # MIPipeline orchestrator
│   │   ├── io/                       # Audio I/O, export
│   │   └── validation/              # Chill test, temporal validation
│   ├── tests/                        # 120+ tests
│   ├── Road-map/                     # Documentation (including this file)
│   └── Lab/                          # Analysis & visualization
│
├── Pipeline/A0/T1/mi/               # MI-Core Neural Architecture
│   ├── backbone/                     # Mamba-2, Sparse Attention, Hybrid
│   ├── experts/                      # 4 MI-aligned experts (Cochlea, R³, C³, L³)
│   ├── heads/                        # State, Planning, Uncertainty, H³ Aux
│   ├── memory/                       # MambaStateManager, HierarchicalMemory
│   ├── motor/                        # MotorEncoder (7 channels → 256D)
│   ├── inference/                    # MISession (per-performer runtime)
│   ├── vocoder/                      # VocosWrapper (frozen)
│   ├── training/                     # MITeacher, MILoss, Curriculum
│   ├── mi_core.py                    # Main orchestrator
│   ├── mi_space_layout.py            # 1,366D manifold structure
│   └── config.py                     # MI-Core hyperparameters
│
├── server/                           # FastAPI + Rust sidecar
│   ├── transport/                    # WebTransport (Rust/wtransport)
│   ├── session/                      # Per-performer session management
│   ├── pipeline/                     # Frame processing loop
│   ├── voice/                        # WhisperLive ASR
│   └── broadcast/                    # LiveKit SFU integration
│
├── client/                           # React 18 + R3F v9
│   ├── src/
│   │   ├── transport/                # WebTransport client
│   │   ├── engine/
│   │   │   ├── audio/                # AudioWorklet playback
│   │   │   └── visual/              # WebGPU + R3F v9
│   │   ├── motor/                    # Input capture (touch, MIDI, MediaPipe)
│   │   ├── store/                    # Zustand (MI-space, motor, emotion)
│   │   └── pages/                    # Perform, Watch, Discover, Profile
│   └── public/
│
├── contracts/                        # Shared Protocol Buffers
│   ├── motor.proto                   # Motor input messages
│   ├── mi_space.proto                # 1,366D state messages
│   ├── session.proto                 # Session lifecycle
│   └── audio.proto                   # Audio stream config
│
├── Core/                             # Shared domain primitives (legacy D0)
├── Library/                          # Literature, ideas, references
└── training/                         # Training infrastructure
    ├── configs/                      # Hydra YAML configs
    ├── scripts/                      # Training launchers
    └── evaluation/                   # Quality metrics
```

---

## 16. Server Architecture

### 16.1 Five-Layer Design

```
┌──────────────────────────────────────────────────────────────────────┐
│                    SERVER ARCHITECTURE                               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Layer 0: TRANSPORT                                               │
│   ├─ Rust sidecar (wtransport crate)                              │
│   │   ├─ WebTransport server (QUIC)                               │
│   │   ├─ Motor datagrams → Python shared memory ring buffer       │
│   │   └─ MI-space datagrams + audio streams → client              │
│   └─ FastAPI (REST) — session management, config                  │
│                                                                     │
│   Layer 1: SESSION MANAGEMENT                                      │
│   ├─ SessionManager — lifecycle, per-performer state               │
│   ├─ PerformerSession — Mamba state, hierarchical memory          │
│   └─ RecordingBuffer — optional session recording                 │
│                                                                     │
│   Layer 2: PROCESSING PIPELINE                                     │
│   ├─ Motor preprocessing (deterministic mapping)                  │
│   ├─ MI-Core inference (Mamba-2 + MoE, per-frame)               │
│   ├─ Vocos rendering (mel → waveform)                            │
│   └─ Voice pipeline (WhisperLive → L³ resolver)                  │
│                                                                     │
│   Layer 3: ML MODELS (GPU)                                        │
│   ├─ MI-Core checkpoint (~250M params, BF16)                     │
│   ├─ Vocos (frozen, pre-trained)                                  │
│   ├─ WhisperLive (streaming ASR)                                  │
│   └─ GPU Worker Pool (1 performer ≈ 1 CUDA stream)              │
│                                                                     │
│   Layer 4: PERSISTENCE                                             │
│   ├─ Redis — session state cache                                  │
│   ├─ Supabase — user data, social features                       │
│   ├─ Object Store — recordings, exports                          │
│   └─ MLflow — model registry, checkpoints                        │
│                                                                     │
└──────────────────────────────────────────────────────────────────────┘
```

### 16.2 Processing Loop (172.27 Hz per performer)

```python
async def process_frame(session: PerformerSession, motor_raw: bytes):
    # 1. Decode motor input (~0.05ms)
    motor = decode_motor_datagram(motor_raw)

    # 2. Motor encode (deterministic, ~0.05ms)
    motor_embed = motor_encoder(motor)

    # 3. MI-Core inference (~3ms on A100)
    mi_output = session.mi_core.step(
        motor=motor_embed,
        states=session.mamba_state,
        memory=session.hierarchical.get_summary()
    )

    # 4. Update state
    session.mamba_state.update(mi_output['states'])
    session.hierarchical.update(mi_output['mi_space'])

    # 5. Render audio (~0.2ms)
    mel = mi_output['mi_space'][:, :128]      # MI-space[0:128]
    waveform = vocos(mel)

    # 6. Send outputs
    send_datagram(mi_output['mi_space'])       # 1,366D → client visual
    send_stream(opus_encode(waveform))         # audio → client
```

---

## 17. Client Architecture

### 17.1 Four-Layer Design

```
┌──────────────────────────────────────────────────────────────────────┐
│                    CLIENT (Browser)                                  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Layer 0: TRANSPORT                                               │
│   ├─ WebTransport client (performer mode)                         │
│   │   ├─ Send: motor datagrams (unreliable, ~60Hz)               │
│   │   ├─ Recv: 1,366D MI-space datagrams (unreliable, ~172Hz)   │
│   │   └─ Recv: audio stream (reliable, Opus encoded)             │
│   └─ LiveKit client (viewer mode, WebRTC)                         │
│                                                                     │
│   Layer 1: STATE MANAGEMENT (Zustand)                              │
│   ├─ useMISpaceStore → latest 1,366D MI-space frame              │
│   ├─ useMotorStore → active motor channels & values              │
│   ├─ useEmotionStore → Brain bar positions                       │
│   ├─ useAppStore → session, UI preferences                       │
│   └─ useSocialStore → chat, followers, reactions                 │
│                                                                     │
│   Layer 2: ENGINES                                                 │
│   ├─ Audio Engine                                                 │
│   │   ├─ AudioWorklet + SharedArrayBuffer                        │
│   │   ├─ Ring buffer: incoming Opus → decoded PCM                │
│   │   └─ ~3ms buffer latency (128 samples @ 44.1kHz)            │
│   └─ Visual Engine                                                │
│       ├─ React Three Fiber v9 + WebGPU backend                   │
│       ├─ TSL shaders driven by MI-space[128:1366]                │
│       └─ Fluid, particles, color from R³+C³+L³                  │
│                                                                     │
│   Layer 3: MOTOR INPUT                                             │
│   ├─ MotorInputManager                                            │
│   │   ├─ Touch/mouse: pointer events                             │
│   │   ├─ MediaPipe Hands: camera → 21 landmarks (local)         │
│   │   ├─ MIDI: WebMIDI API                                       │
│   │   ├─ Gamepad: Gamepad API                                    │
│   │   ├─ Voice: MediaStream → server (WhisperLive)              │
│   │   └─ Emotion bars: React UI → C³ values                     │
│   └─ Motor → MI-space mapping (deterministic, client-side)       │
│                                                                     │
│   Layer 4: UI (React 18)                                          │
│   ├─ Perform — full performance interface                        │
│   ├─ Watch — viewer mode (LiveKit)                               │
│   ├─ Discover — browse performances                              │
│   ├─ Profile — user settings, history                            │
│   └─ Leagues — competitive / collaborative                       │
│                                                                     │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 18. Shared Contracts & Wire Formats

### 18.1 Protocol Buffers

```protobuf
// mi_space.proto
message MISpaceFrame {
  uint32 frame_index = 1;
  repeated float cochlea = 2;    // 128 values
  repeated float r3 = 3;         // 128 values
  repeated float c3 = 4;         // 1006 values
  repeated float l3 = 5;         // 104 values
}

// motor.proto
message MotorInput {
  uint32 frame_index = 1;
  optional TouchData touch = 2;
  optional MediaPipeData mediapipe = 3;
  optional MidiData midi = 4;
  optional EmotionData emotion = 5;
}
```

### 18.2 Wire Format (Performance Critical)

```
MI-Space datagram @ 172 Hz:
  [4 bytes: frame_index] + [5,464 bytes: Float32 × 1366] = 5,468 bytes
  Bandwidth: 5,468 × 172.27 = ~920 KB/s per performer

Motor datagram @ 60 Hz:
  Protobuf-encoded, ~100-500 bytes per frame
  Bandwidth: ~30 KB/s per performer

Audio stream (reliable):
  Opus encoded, ~64 kbps for 44.1kHz mono
  Bandwidth: ~8 KB/s per performer
```

**Total bandwidth per performer: ~958 KB/s** (vs ~5.8 MB/s with old 8192D)

---

## 19. Webapp Transport Architecture

### 19.1 WebTransport (QUIC) — Performer

```
Why WebTransport?
├─ Unreliable datagrams: 1,366D state @ 172Hz (~920 KB/s, loss-tolerant)
├─ Reliable streams: Audio (lossless, ordered)
├─ Multiplexed: Multiple channels on single connection
├─ 0-RTT handshake: Instant reconnection
└─ UDP-based: Lower latency than TCP (WebSocket)

Channels:
├─ Channel 0 (unreliable): Motor → Server (tiny, loss OK)
├─ Channel 1 (unreliable): 1,366D MI-space → Client (visualization)
├─ Channel 2 (reliable):   Opus audio → Client (must be lossless)
└─ Channel 3 (reliable):   Voice audio → Server (for WhisperLive)
```

### 19.2 LiveKit SFU (WebRTC) — Broadcast

```
Why LiveKit?
├─ WebRTC SFU: Scales to 100K+ viewers per room
├─ Adaptive bitrate: Handles varying viewer bandwidth
├─ Edge servers: Global low-latency delivery
└─ Existing protocol: No client plugin needed

Flow:
Performer → WebTransport → Server → MI-Core → Audio + 1,366D
                                          │
                                    LiveKit SFU
                                     ╱    │    ╲
                               Viewer₁  Viewer₂  Viewer_N
```

---

## 20. Social Platform & Live Performance

SRC⁹ is not just an instrument — it's a **live performance platform**:

```
MODES:
├─ PERFORM: Create music in real-time (MI-Core active)
├─ STREAM: Broadcast to viewers (LiveKit SFU)
├─ RECORD: Save MI-space trajectories (full 1,366D per frame)
├─ SHARE: Export recordings, share performances
└─ DISCOVER: Browse other performers, learn from replays

NOT a DAW. NOT a notation tool. NOT a sample library.
It's a live instrument with a social stage.
```

**Replays are in MI-space**: When you record a performance, you save the 1,366D trajectory. Replay renders the exact same audio and visual. You can also edit the trajectory — change C³.tension at timestamp 30s and re-render.

---

## 21. Technology Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **ML Backbone** | Mamba-2 SSM | O(n) streaming, state = memory |
| **Attention** | Sparse Attention | Long-range planning, every 4th layer |
| **Expert Routing** | Top-K MoE | Structure-aware, load balanced |
| **Vocoder** | Vocos (frozen) | ~70x faster than BigVGAN, iSTFT |
| **ASR** | WhisperLive | Real-time streaming, multilingual |
| **Transport** | WebTransport (QUIC) | Low latency, unreliable datagrams |
| **Broadcast** | LiveKit SFU | WebRTC, 100K+ viewers |
| **IPC** | Rust sidecar (wtransport) | Zero-copy, no GIL |
| **Server** | FastAPI + PyTorch | Session management + GPU inference |
| **Client** | React 18 + R3F v9 | Component-based, WebGPU rendering |
| **Visual** | WebGPU + TSL | Next-gen GPU shaders |
| **Audio** | AudioWorklet | Low-latency browser audio |
| **State** | Zustand | Reactive, minimal boilerplate |
| **Training** | DDP + Hydra + WandB | Multi-GPU, configurable, tracked |

---

## 22. Testing Strategy

| Test Type | Target | Tools |
|-----------|--------|-------|
| **Unit** | Each MI Teacher module (R³, C³, L³) | pytest |
| **Integration** | Full pipeline: Audio → 1,366D | pytest |
| **Alignment** | MI-Core output vs MI Teacher output | custom metrics |
| **Audio Quality** | Vocos rendering quality | PESQ, STOI, multi-res STFT |
| **Latency** | End-to-end < 20ms | benchmark suite |
| **White-Box** | Every dim traceable to formula | automated tracing |
| **Validation** | Composer-verified musical accuracy | human evaluation |

**Current MI Teacher tests: 120 passing** (14 core + 22 ear + 24 brain + 42 language + 14 integration + 4 validation)

---

## 23. DevOps & Infrastructure

```
DEPLOYMENT:
├─ Docker containers (server, training)
├─ GPU: 1 performer ≈ 1 CUDA stream (A100/H100)
│   MI-Core: ~3ms per frame (~250M params, BF16)
│   Vocos: ~0.2ms per frame (frozen)
├─ Scaling: horizontal (add GPU nodes per performer)
└─ CDN: LiveKit edge servers for broadcast

TRAINING:
├─ Multi-GPU DDP (data parallel)
├─ Mixed precision BF16
├─ WandB experiment tracking
├─ MLflow model registry
├─ Hydra config management
└─ Audio corpus: diverse genres, 10K+ hours target

MONITORING:
├─ MI-Core latency per frame
├─ Expert routing distribution
├─ Uncertainty calibration
├─ Audio quality metrics
└─ Session stability
```

---

## 24. Implementation Priority

```
PHASE 1 (Current): MI Teacher — LARGELY COMPLETE
├─ 96 models scaffolded across 9 cognitive units (C³ = 1,006D)
├─ R³ v1 operational (49D), v2 spec ready (128D, groups A–K)
├─ H³ demand-driven (~5,210 4-tuples for R³v1)
├─ L³ semantic layer (104D, 8 groups α–θ)
├─ 504 papers indexed in literature catalog
├─ ~134 Python files in mi_beta/
└─ Status: doc upgrades (v2.1.0) in progress, code frozen at Phase 5

PHASE 2: R³ Expansion (49D → 128D)
├─ Implement groups F–K (Pitch, Rhythm, Harmony, Info, Timbre-Ext, Modulation)
├─ Update H³ demand (~5,210 → ~8,610 tuples)
├─ Propagate to all 96 C³ models
└─ Target: 1,366D MI-space fully populated

PHASE 3: MI-Core Training
├─ Adapt T1 backbone (Mamba-2, MoE) to 1,366D MI-space
├─ Implement MITeacher (replaces D0Teacher)
├─ 4 experts: E-Cochlea(128D), E-R³(128D), E-C³(1006D), E-L³(104D)
├─ H³ auxiliary head (~5,210D, training only)
└─ Validation: MI-Core output ≈ MI Teacher output

PHASE 4: Audio & Visual
├─ Train bidirectional (encode + decode + cycle + fill)
├─ Implement MI-space → shader mapping
├─ WebGPU visual engine (R3F v9)
├─ AudioWorklet playback
└─ Validation: audio quality, visual coherence

PHASE 5: Live System
├─ Rust sidecar (WebTransport)
├─ Server session management
├─ Client motor input
├─ End-to-end live performance
└─ Validation: <20ms latency, stable 172Hz

PHASE 6: Social & Scale
├─ LiveKit broadcast integration
├─ Recording & replay (1,366D trajectories)
├─ Social features (Discover, Profile, Leagues)
└─ Continuous MI Teacher improvement
```

---

## References

### Reward & Dopamine
- Salimpoor, V. N., et al. (2011). Anatomically distinct dopamine release during anticipation and experience of peak emotion to music. *Nature Neuroscience*, 14(2), 257-262.
- Berridge, K. C. (2003). Pleasures of the brain. *Brain and Cognition*, 52(1), 106-128.
- Blood, A. J., & Zatorre, R. J. (2001). Intensely pleasurable responses to music correlate with activity in brain regions implicated in reward and emotion. *PNAS*, 98(20), 11818-11823.
- Howe, M. W., et al. (2013). Prolonged dopamine signalling in striatum signals proximity and value of distant rewards. *Nature*, 500(7464), 575-579.

### Affect & Emotion
- Russell, J. A. (1980). A circumplex model of affect. *Journal of Personality and Social Psychology*, 39(6), 1161.
- Koelsch, S. (2006). Significance of Broca's area and ventral premotor cortex for music-syntactic processing. *Cortex*, 42(4), 518-520.
- Fritz, T., et al. (2009). Universal recognition of three basic emotions in music. *Current Biology*, 19(7), 573-576.
- Mitterschiffthaler, M. T., et al. (2007). A functional MRI study of happy and sad affective states induced by classical music. *Human Brain Mapping*, 28(11), 1150-1162.

### Autonomic & Physiology
- de Fleurian, R., & Pearce, M. T. (2021). Chills in music: A systematic review. *Psychological Bulletin*, 147(9), 890.
- Thayer, J. F., et al. (2009). Heart rate variability, prefrontal neural function, and cognitive performance. *Annals of Behavioral Medicine*, 37(2), 141-153.
- Sloboda, J. A. (1991). Music structure and emotional response: Some empirical findings. *Psychology of Music*, 19(2), 110-120.
- Fancourt, D., et al. (2020). The psychoneuroimmunological effects of music. *Brain, Behavior, and Immunity*, 82, 106-115.

### Predictive Processing & Learning
- Huron, D. (2006). *Sweet Anticipation: Music and the Psychology of Expectation*. MIT Press.
- Pearce, M. T. (2005). The construction and evaluation of statistical models of melodic structure. *PhD Thesis*, City University London.
- Fong, C. Y., et al. (2020). Expectancy violations in music. *Cortex*, 125, 167-182.
- Schmidhuber, J. (2009). Simple algorithmic theory of subjective beauty, novelty, surprise, interestingness, attention, curiosity, creativity, art, science, music, jokes. *Journal of SICE*, 48(1), 21-32.
- Cheung, V. K., et al. (2019). Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. *Current Biology*, 29(23), 4084-4092.
- Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127-138.

### Psychoacoustics
- Plomp, R., & Levelt, W. J. M. (1965). Tonal consonance and critical bandwidth. *JASA*, 38(4), 548-560.
- Sethares, W. A. (1993). Local consonance and the relationship between timbre and scale. *JASA*, 94(3), 1218-1228.
- Stevens, S. S. (1937). A scale for the measurement of the psychological magnitude loudness. *JASA*, 8(4), 277-282.

### Temporal Cognition
- Poeppel, D. (2009). The analysis of speech in different temporal integration windows. *Speech Communication*, 41(1), 245-255.
- Jones, M. R. (1976). Time, our lost dimension: Toward a new theory of perception, attention, and memory. *Psychological Review*, 83(5), 323.
- Lerdahl, F., & Jackendoff, R. (1983). *A Generative Theory of Tonal Music*. MIT Press.

---

*SRC⁹ Musical Intelligence*
*Version 5.1.0 — February 13, 2026*
*Every dimension has meaning. Every meaning has science. Every science has music.*
*v5: Analyze. Compose. Hybrid. One model, both directions, one elegant training. White-Box.*
