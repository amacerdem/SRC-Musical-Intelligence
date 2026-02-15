# Musical Intelligence

A computational model of human musical cognition — from acoustic waveform to psychological experience.

Musical Intelligence (MI) transforms raw audio into a multi-layered representation that mirrors the human auditory pathway: spectral decomposition in the ear, temporal pattern extraction across timescales, cognitive processing through anatomically-grounded brain nuclei, and psychological interpretation across six experiential domains.

```
Audio (44.1 kHz)
  -> Cochlea: 128-band mel spectrogram @ 172 Hz frame rate
    -> R3: 128D spectral features (11 psychoacoustic groups)
      -> H3: Sparse temporal morphology (4-tuple demands across 12 timescales)
        -> C3: 96 cognitive nuclei in 9 units, 26 brain regions, 4 neurochemicals
          -> Psi3: 6 psychological domains, 27 experiential dimensions
```

## Architecture

### R3 — Spectral Representation (128D)

Eleven spectral groups extract psychoacoustic features from audio, organized in a three-stage dependency DAG:

| Group | Dimensions | Domain |
|-------|-----------|--------|
| A Consonance | 7D | Roughness, Sethares dissonance, Helmholtz consonance, Stumpf fusion |
| B Energy | 5D | Loudness, dynamics, velocity |
| C Timbre | 10D | Brightness, spectral shape, tristimulus |
| D Change | 4D | Spectral flux, onset detection |
| E Interactions | 25D | Cross-group coupling (Stage 2, depends on A-D) |
| F Pitch & Chroma | 7D | Pitch class distribution, salience |
| G Rhythm & Groove | 6D | Tempo, periodicity, beat strength |
| H Harmony & Tonality | 9D | Key clarity, chord type, tonal hierarchy |
| I Information | 8D | Spectral entropy, predictability |
| J Timbre Extended | 10D | Extended timbral descriptors |
| K Modulation | 7D | AM/FM modulation depth and rate |

When raw audio is available, Group A uses real psychoacoustic models (Sethares 1993 pairwise dissonance, Plomp-Levelt roughness, HPS F0 estimation, harmonic template matching) instead of mel-based proxies. All other callers passing only mel spectrograms continue to work unchanged.

### H3 — Temporal Morphology (Sparse)

H3 extracts temporal demand patterns as sparse 4-tuples:

```
(r3_index, horizon, morph, law)
```

- **r3_index**: Which R3 feature to track (0-127)
- **horizon**: Timescale of integration (12 levels, 5ms to 60s+)
- **morph**: Statistical shape (mean, std, skew, kurtosis, min, max, range, entropy)
- **law**: Temporal direction — memory (past), prediction (future), integration (bidirectional)

Each nucleus declares which H3 tuples it needs. Only requested tuples are computed, keeping the extraction sparse and efficient. Computation uses vectorized `torch.unfold` across all frames.

### C3 — Cognitive Architecture (96 Nuclei)

Nine cognitive units, each containing nuclei at five processing depths:

| Depth | Role | Reads | Count |
|-------|------|-------|-------|
| 0 | Relay | R3 + H3 directly | 9 |
| 1 | Encoder | Relay outputs from same unit | ~23 |
| 2 | Associator | Relay + Encoder outputs | ~30 |
| 3 | Integrator | All upstream + cross-unit pathways | ~22 |
| 4-5 | Hub | Full convergence | ~12 |

**Units:**

| Unit | Full Name | Models | Circuit |
|------|-----------|--------|---------|
| SPU | Spectral Processing Unit | 9 | Ascending auditory (CN, SOC, IC, MGB, A1) |
| STU | Sensorimotor Timing Unit | 14 | Motor timing (SMA, PMC, cerebellum) |
| IMU | Integrative Memory Unit | 15 | Episodic memory (hippocampus, mPFC) |
| ARU | Affective Resonance Unit | 10 | Limbic reward (NAcc, VTA, amygdala) |
| ASU | Auditory Salience Unit | 9 | Salience detection (anterior insula, dACC) |
| NDU | Novelty Detection Unit | 9 | Prediction error (IFG, STG) |
| MPU | Motor Planning Unit | 10 | Sensorimotor integration (SMA, PMC) |
| PCU | Predictive Coding Unit | 10 | Imagery and prediction (AC, IFG, STS) |
| RPU | Reward Processing Unit | 10 | Mesolimbic reward (NAcc, VTA, vmPFC) |

Each nucleus is a self-documenting scientific artifact with:
- Cited constants (author, year, effect size)
- Explicit brain region mappings with MNI coordinates
- Neurochemical coupling (DA, NE, OPI, 5HT) via typed NeuroLinks
- H3 demand declarations
- Falsification criteria

**Evidence tiers:**
- **Alpha** (27 models): >90% confidence, direct neural evidence
- **Beta** (40 models): 70-90% confidence, cross-domain synthesis
- **Gamma** (29 models): 50-70% confidence, theoretical extrapolation

### Psi3 — Psychological Interpretation (27D)

The Psi3 interpreter maps C3 internal state (nucleus outputs + region activations + neurochemistry) to six experiential domains:

| Domain | Dimensions | Examples |
|--------|-----------|----------|
| Affect | 4D | Valence, arousal, tension, dominance |
| Emotion | 7D | Joy, sadness, fear, awe, nostalgia, tenderness, serenity |
| Aesthetic | 5D | Beauty, groove, flow, surprise, closure |
| Bodily | 4D | Chills, movement urge, breathing change, tension release |
| Cognitive | 4D | Familiarity, absorption, expectation, attention focus |
| Temporal | 4D | Anticipation, resolution, buildup, release |

All mappings are formula-based with citations (no learned parameters).

### Brain Regions (26) and Neurochemicals (4)

**Region Activation Map (RAM)**: Each nucleus declares RegionLinks mapping output dimensions to anatomical regions. The executor accumulates these into a `(B, T, 26)` activation tensor covering brainstem, thalamus, auditory cortex, association cortex, frontal, prefrontal, parietal, limbic, and reward areas.

**Neurochemical state**: Four neuromodulatory channels tracked as `(B, T, 4)`:
- **DA** (dopamine): Reward, wanting, prediction error
- **NE** (norepinephrine): Arousal, attention, vigilance
- **OPI** (opioid): Pleasure, hedonic tone, comfort
- **5HT** (serotonin): Mood, patience, social bonding

Nuclei declare NeuroLinks with produce/amplify/inhibit effects on these channels.

## HYBRID — Audio Transformation

HYBRID transforms audio's emotional character using R3 as a perceptual feedback loop:

```
Audio -> STFT (phase-preserving) -> HPSS -> Spectral + Transient + Harmonic ops -> Recombine -> Safety -> Output
```

**Controls**: 5 timbral sliders (valence, arousal, tension, warmth, brightness) + 7 structural sliders (tempo, rubato, swing, push-pull, rhythm density, harmonic mode bias, harmonic rhythm).

**Closed-loop calibration**: Iteratively adjusts transform strength until target R3 deltas are achieved (2-5 iterations typical).

**Safety**: Gain clamp [-12dB, +6dB], soft-clip limiter, loudness normalization, temporal smoothing.

```bash
python -m Musical_Intelligence.hybrid.cli input.wav --preset joyful -o output.wav
python -m Musical_Intelligence.hybrid.cli input.wav --warmth 0.5 --brightness 0.3 -o output.wav
python -m Musical_Intelligence.hybrid.cli input.wav --batch --output-dir results/
```

## L3 — Semantic Layer (104D)

L3 maps C3 outputs to an eight-level epistemological framework:

| Level | Group | Question | Dimensions |
|-------|-------|----------|-----------|
| 1 | Alpha | How is it computed? | 6D |
| 2 | Beta | Where in the brain? | 14D |
| 3 | Gamma | What does it mean subjectively? | 13D |
| 4 | Delta | How to test empirically? | 12D |
| 5 | Epsilon | How does the listener learn? | 19D |
| 6 | Zeta | Which direction (polarity)? | 12D |
| 7 | Eta | What word describes it? | 12D |
| 8 | Theta | How to narrate it? | 16D |

Zero learned parameters. Every dimension has a formula and a citation.

## WebLab — Experiment Visualization

Interactive React + FastAPI platform for inspecting MI pipeline output:

- **7 pages**: R3 spectral heatmap, H3 temporal grid, nucleus output, brain regions, neurochemistry, Psi3 state, evidence/citations
- **10 panels**: Per-layer drill-down, region activation flow, neurochemical timelines, citation browser
- **Audio transport**: Web Audio API playback synchronized with visualizations
- **Experiments**: Pre-computed pipeline runs stored as JSON with audio passthrough

```
Lab/WebLab/
  app/src/         32 TypeScript/React source files (6,566 lines)
  server/          FastAPI backend
  scripts/         5 Python pipeline/visualization scripts
  experiments/     Pre-computed experiment datasets
```

## Pipeline Performance

Measured on 30 seconds of audio (T=5,168 frames):

| Stage | Time |
|-------|------|
| Cochlea (mel) | 1.7s |
| R3 (128D) | 1.2s |
| H3 (sparse) | 146s |
| C3 (brain) | 0.16s |

## Project Structure

```
Musical_Intelligence/          237 Python files
  contracts/                   Bases (nucleus, spectral group, semantic group) + 14 dataclasses
  ear/
    r3/                        11 groups (A-K), registry, pipeline, extractor -> (B, T, 128)
    h3/                        Bands, morphology, attention, demand tree -> sparse dict
  brain/
    units/spu/relays/bch.py    First implemented nucleus (700 lines)
    regions/                   26 brain region modules
    neurochemicals/            DA, NE, OPI, 5HT managers
    executor.py                Depth-ordered nucleus execution
    psi_interpreter.py         C3 -> Psi3 (27D psychological output)
  hybrid/                      Phase-preserving audio transformation (14 files)
  training/                    Plasticity framework (Hebbian, Bayesian, TD-learning)

Docs/                          411 markdown files
  C3/Models/                   96 model specifications (one directory per nucleus)
  R3/                          Spectral feature documentation
  H3/                          Temporal demand documentation
  L3/                          Semantic layer (104D, 8 epistemological groups)
  MI Architecture/             Architecture evolution + 6-phase implementation plan

Tests/                         41 Python test files
  unit/                        R3, H3, mechanisms, models, pathways
  integration/                 Ear pipeline, brain pipeline, full pipeline
  brain/                       BCH nucleus (33 tests) + smoke tests (20 tests)
  scientific/                  Swan Lake benchmark, IMU validation
  hybrid/                      Audio transformation (29 tests)

Lab/WebLab/                    React visualization platform
Building/                      96-model construction system + progress tracking
Literature/                    Research papers organized by topic
Test-Audio/                    7 test tracks (~400 MB)
```

## Plasticity (Training Framework)

MI uses neural plasticity, not conventional machine learning:

| Aspect | Machine Learning | MI Plasticity |
|--------|-----------------|---------------|
| Learning signal | External loss function | Internal neurochemical circuit |
| What changes | Opaque weight matrices | ~212 named, cited parameters per listener |
| Algorithm | SGD / Adam | Hebbian, Bayesian, TD-learning |
| Explainability | Post-hoc (SHAP, LIME) | Built-in audit trail |
| Reset | Retrain from scratch | `reset_to_substrate()` returns to peer-reviewed baseline |

Two layers: **Substrate** (96 nuclei, deterministic, immutable) and **Plasticity** (adaptive overlay — Hebbian weights, Bayesian posteriors, personal gains, neurochemical baselines).

## Quick Start

```bash
pip install -r requirements.txt

# Run the full pipeline on an audio file
python Lab/WebLab/scripts/run_pipeline.py input.wav --slug my-experiment

# Transform audio emotion
python -m Musical_Intelligence.hybrid.cli input.wav --preset joyful -o output.wav

# Run tests
pytest Tests/
```

## Build System

The Building directory contains the construction infrastructure for all 96 nuclei. BCH (SPU Relay) is the gold standard — every other nucleus follows its pattern for scientific depth, test coverage, and documentation consistency.

```
Building/
  README.md              Build philosophy and 7-phase order
  teminology/            Nucleus hierarchy, layer naming, region catalog
  training/              MI-PLASTICITY framework specification
  progress/              Daily construction logs
```

Target per nucleus: ~700-800 lines of scientifically-documented code with 13+ cited papers, 4-6 brain regions with MNI coordinates, 12-20 H3 demand specifications, and 33+ unit tests.

## Validated Results

**BCH Consonance Hierarchy** (Feb 15, 2026): Six canonical intervals tested against Bidelman & Krishnan 2009 ranking:

```
P1 (Unison) > P5 (Fifth) > P4 (Fourth) > M3 (Major Third) > m6 (Minor Sixth) > TT (Tritone)
```

6/6 correct ordering. 45% spread between most consonant and most dissonant (was 0.6% with mel-proxy computations). Validated by composer evaluation on real piano performance: **96/100**.

**Swan Lake Integration Test**: 30 seconds of Tchaikovsky -> R3 (128D) -> H3 (7,782 tuples) -> C3 (1,006D) -> full pipeline PASS.

## License

MIT License. Copyright (c) 2026 Amac Erdem.
