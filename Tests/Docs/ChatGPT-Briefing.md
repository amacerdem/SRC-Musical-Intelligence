# Musical Intelligence (MI) — Comprehensive System Briefing

**Date:** March 5, 2026
**Author:** Amaç Erdem
**Purpose:** Full technical briefing for deep analysis and scientific evaluation

---

## 1. What Is MI?

MI (Musical Intelligence) is a **computational model of music cognition** — a three-layer neural processing pipeline that takes raw audio waveform as input and produces a complete cognitive representation of the musical experience: perception, prediction, emotion, memory, reward, motor planning, and social cognition.

It is NOT:
- A music classifier or recommendation system
- A machine learning model trained on labeled data
- A music information retrieval (MIR) tool

It IS:
- A **cognitive architecture** (comparable to ACT-R, SOAR, or Friston's active inference)
- A **neuroscience-grounded computational model** (every parameter cites published neuroscience)
- A **real-time audio processing pipeline** running at 172.27 Hz frame rate
- A system with **zero training** — all weights are hand-specified from literature, not learned

---

## 2. Three-Layer Architecture: R³ → H³ → C³

### Layer 1: R³ — Early Perceptual Front-End (97 dimensions, FROZEN v1.0.0)

Extracts psychoacoustic features from audio at 172.27 Hz (44100 / 256 hop). Nine feature groups:

| Group | Dims | Features |
|-------|------|----------|
| A [0:7] | 7 | Spectral shape (centroid, spread, rolloff, flatness) |
| B [7:12] | 5 | Dynamics (loudness, amplitude velocity, onset strength) |
| C [12:21] | 9 | Harmonic content (harmonicity, inharmonicity, warmth, brightness) |
| D [21:25] | 4 | Spectral change (flux, entropy, zero-crossing rate) |
| F [25:41] | 16 | Pitch (12 chroma + salience + entropy + clarity + mode) |
| G [41:51] | 10 | Rhythm & groove (tempo, beat strength, onset periodicity) |
| H [51:63] | 12 | Tonal structure (key clarity, tonal stability, Krumhansl hierarchy) |
| J [63:83] | 20 | Texture (roughness, density, register, spectral smoothness) |
| K [83:97] | 14 | Modulation (AM/FM rates, depth, tremolo, vibrato) |

R³ is **deterministic, stateless, and frozen** — no EMA, no cross-domain, no prediction, no learning.

### Layer 2: H³ — Multi-Scale Temporal Morphology (FROZEN v1.0.0)

A **sparse temporal integration engine** that computes window-based statistical descriptors of R³ features across multiple timescales. Each feature is parameterized as a 4-tuple:

```
(r3_idx, horizon, morph, law)
```

- **r3_idx** [0-96]: which of the 97 R³ features
- **horizon** [0-31]: 32 exponentially-spaced time windows from ~6ms to ~800s
  - Micro (H0-H7): ~6ms to ~100ms — sensory processing
  - Meso (H8-H15): ~100ms to ~1s — beat/event level
  - Macro (H16-H23): ~1s to ~10s — phrase level
  - Ultra (H24-H31): ~10s to ~800s — section/piece level
- **morph** [0-23]: 24 statistical transforms
  - M0=mean, M2=std, M4=max, M8=velocity (first derivative), M13=entropy, M14=periodicity, M18=trend (linear slope), etc.
- **law** [0-2]: causal direction
  - L0=memory (backward/causal — uses only past frames)
  - L1=forward (uses only future frames)
  - L2=integration (bidirectional)

Theoretical space: 97 × 32 × 24 × 3 = **223,488 dimensions**. Only ~8,600 are active (~3.9% occupancy) — each cognitive model declares which H³ tuples it needs ("demand tuples").

H³ is **deterministic, stateless, and frozen**. It adds no parameters — it is pure temporal morphology.

### Layer 3: C³ — Cognitive Brain (Kernel v4.0)

The cognitive layer where perception becomes cognition. Contains:

- **88 mechanisms** (computational models organized by processing depth)
- **131 beliefs** (cognitive state variables, each a scalar in [0,1] per frame)
- **26 brain regions** (Region Activation Map, MNI152 coordinates)
- **4 neurochemicals** (DA, NE, OPI, 5HT)
- **9 cognitive functions** (F1-F9)

#### 9 Cognitive Functions

| Function | Name | Beliefs | Key Models |
|----------|------|---------|------------|
| F1 | Sensory Processing | 17 | BCH (consonance), PSCL (pitch), PCCR (chroma), MIAA (timbre) |
| F2 | Prediction | 15 | HTP (hierarchical temporal prediction), SPH (spatiotemporal), ICEM (information content → emotion) |
| F3 | Attention | 15 | SNEM (novelty/expectation), IACM (inhibition/cognitive load) |
| F4 | Memory | 13 | MEAMN (autobiographical), MMP (melodic pattern), HCMC (hierarchical context) |
| F5 | Emotion | 14 | VMM (valence-mode), AAC (autonomic arousal), NEMAC (nostalgia) |
| F6 | Reward | 16 | SRP (hedonic blend), DAED (wanting/liking dissociation) |
| F7 | Motor & Timing | 17 | PEOM (entrainment), HGSIC (groove), HMCE (hierarchical meter) |
| F8 | Learning | 14 | TSCP (template consolidation), ESME (statistical learning), EDNR (error-driven) |
| F9 | Social Cognition | 10 | NSCP (neural synchrony), SSRI (social reward), DDSMI (dual-stream integration) |

#### Belief Types (131 total)

| Type | Count | Update Rule |
|------|-------|-------------|
| **Core** | 36 | Full Bayesian: observe → predict → update with gain = π_obs / (π_obs + π_pred) |
| **Appraisal** | 65 | Observe-only: weighted combination of mechanism outputs |
| **Anticipation** | 30 | Forward prediction: τ × prev + (1-τ) × baseline + w_trend × M18 + w_period × M14 + w_ctx × context |

#### Mechanism Architecture (4 internal layers per mechanism)

Every mechanism follows the same E → M → P → F pipeline:

1. **E-layer (Extraction)**: Combines R³ and H³ features into domain-specific signals
2. **M-layer (Temporal Integration)**: Accumulates evidence over time
3. **P-layer (Cognitive Present)**: Current-moment assessment, exported to beliefs
4. **F-layer (Forecast)**: Forward predictions that feed back as context

Each mechanism declares:
- `OUTPUT_DIM`: number of output dimensions
- `PROCESSING_DEPTH`: execution order (0=relay, 1=encoder, 2=associator, etc.)
- `H3_DEMANDS`: list of (r3_idx, horizon, morph, law) tuples it needs
- `REGION_LINKS`: list of (dimension, brain_region, weight, citation) mappings
- `NEURO_LINKS`: list of (dimension, neurochemical, weight, citation) mappings

#### Bayesian Belief Update (Core Beliefs)

Every frame at 172.27 Hz, each Core Belief runs:

```
1. OBSERVE:  obs = f(R³, H³, mechanism_outputs)
2. PREDICT:  pred = τ × prev + (1-τ) × baseline + w_trend × M18 + w_period × M14 + w_ctx × beliefs_{t-1}
3. UPDATE:   posterior = (1 - gain) × predicted + gain × observed
             where gain = π_obs / (π_obs + π_pred + ε)
```

Prediction precision (π_pred) is estimated from prediction error history:
```
stability   = 1 / (mean(|PE|) + 0.1)
consistency = 1 / (std(|PE|) + 0.1)
π_raw = stability × consistency × τ_factor × fill_factor
π_pred = EMA(π_prev, π_raw, smooth_τ=0.6)
```

This means: when predictions have been accurate, the system trusts its model (high π_pred → low gain → resist sensory updates). When predictions fail, the system opens up to new observations (low π_pred → high gain → accept sensory input).

---

## 3. The Reward System (F6) — Most Novel Component

### Reward Formula (v3.0)

```
reward = Σ_beliefs [ salience × (
    1.5 × surprise
  + 0.8 × resolution
  + 0.5 × exploration
  − 0.6 × monotony
)] × familiarity_mod × emotional_mod × da_gain
```

Where:
```
π_eff = tanh(π_raw / 12)                           # precision compression

surprise   = |PE| × π_eff × (1 − familiarity)      # unexpected in unfamiliar context
resolution = (1 − |PE|) × π_eff × familiarity       # expected in familiar context
exploration = |PE| × (1 − π_eff)                     # high PE + low precision = epistemic reward
monotony   = π_eff²                                  # too predictable = boring

familiarity_mod = 0.5 + 0.5 × [4 × fam × (1 − fam)]  # inverted-U, peak at 0.5
da_gain = 1 + 0.25 × (0.6 × wanting + 0.4 × liking)  # DA amplification [1.0, 1.25]
```

### DAED — Wanting/Liking Dissociation (8D)

Based on Berridge (2003) wanting vs. liking framework, but computationally explicit for music:

- **Anticipatory pathway** (wanting): driven by loudness velocity, spectral uncertainty, roughness velocity → maps to caudate nucleus
- **Consummatory pathway** (liking): driven by mean pleasantness, mean loudness → maps to nucleus accumbens
- **temporal_phase** = anticipatory / (anticipatory + consummatory) → continuous phase indicator [0=at peak, 1=building up]
- **dissociation_index** = |anticipatory − consummatory| → how clearly separated the two phases are

This produces the Salimpoor (2011) temporal dissociation: caudate DA ramp 15-30s before peak → NAcc burst at peak pleasure moment.

### Neurochemical System (4 channels)

| Channel | Neuromodulator | Primary Role | Key Mapping |
|---------|---------------|--------------|-------------|
| DA [0] | Dopamine | Wanting, reward prediction error | Anticipatory: caudate ramp; Consummatory: NAcc burst |
| NE [1] | Norepinephrine | Arousal, attention, novelty | Phasic bursts for unexpected events |
| OPI [2] | Endogenous Opioids | Liking, hedonic pleasure, chills | Peak during frisson; Naltrexone reduces pleasure |
| 5HT [3] | Serotonin | Temporal discount rate, patience | High 5HT = long-horizon reward sensitivity |

### Psi-3 Interpreter (28D experiential output)

Reads RAM (26D) + neurochemicals (4D) to produce 6 experiential domains:

- **Affect (4D)**: valence = 0.9×DA + 0.1×OPI; arousal = 0.7×NE + 0.3×OPI; tension = 0.5×amygdala + 0.5×(1−5HT); dominance = dlPFC
- **Emotion (7D)**: joy = valence × arousal; awe = valence × arousal × NAcc; nostalgia = valence × hippocampus; etc.
- **Aesthetic (5D)**: beauty = 0.5×DA + 0.5×OPI; groove = 0.5×putamen + 0.5×SMA
- **Bodily (4D)**: chills = 0.3×PAG + 0.3×hypothalamus + 0.4×OPI; movement_urge = 0.5×putamen + 0.5×SMA
- **Cognitive (4D)**: familiarity = hippocampus; absorption = 0.5×insula + 0.5×NAcc
- **Temporal (4D)**: anticipation = DA above baseline; resolution = OPI peak

---

## 4. Region Activation Map (RAM) — 26D Brain Output

Every frame produces a 26-dimensional brain activation tensor. Each dimension = a specific brain region with real MNI152 stereotaxic coordinates.

### Cortical (12 regions)

| Idx | Region | MNI (x,y,z) | Role |
|-----|--------|-------------|------|
| 0 | A1/HG (Heschl's Gyrus) | (48,-18,8) | Primary auditory processing |
| 1 | STG (Superior Temporal Gyrus) | (-58,-22,4) | Auditory association, convergence hub |
| 2 | STS (Superior Temporal Sulcus) | (-54,-40,4) | Voice processing, social cognition |
| 3 | IFG (Inferior Frontal Gyrus) | (-48,14,20) | Musical syntax (Broca's area) |
| 4 | dlPFC | (-44,36,22) | Working memory, executive control |
| 5 | vmPFC | (0,44,-18) | Self-referential processing |
| 6 | OFC (Orbitofrontal) | (2,38,-16) | Aesthetic evaluation |
| 7 | ACC (Anterior Cingulate) | (0,24,32) | Salience, error detection |
| 8 | SMA (Supplementary Motor) | (0,-8,56) | Beat anticipation |
| 9 | PMC (Premotor Cortex) | (-40,-4,52) | Movement execution |
| 10 | AG (Angular Gyrus) | (-46,-66,32) | Semantic processing |
| 11 | TP (Temporal Pole) | (-42,16,-28) | Conceptual knowledge |

### Subcortical (9 regions)

| Idx | Region | MNI (x,y,z) | Role |
|-----|--------|-------------|------|
| 12 | VTA | (0,-16,-8) | Dopamine source |
| 13 | NAcc (Nucleus Accumbens) | (10,12,-8) | Reward convergence |
| 14 | Caudate | (12,12,10) | Anticipation/wanting |
| 15 | Amygdala | (-22,-4,-16) | Emotional valence |
| 16 | Hippocampus | (28,-22,-12) | Memory encoding/retrieval |
| 17 | Putamen | (-24,4,4) | Motor timing, groove |
| 18 | MGB (Medial Geniculate) | (-14,-24,-4) | Auditory thalamic relay |
| 19 | Hypothalamus | (0,-4,-12) | Autonomic arousal |
| 20 | Insula | (-38,8,4) | Interoception |

### Brainstem (5 regions)

| Idx | Region | MNI (x,y,z) | Role |
|-----|--------|-------------|------|
| 21 | IC (Inferior Colliculus) | (0,-34,-8) | Midbrain auditory |
| 22 | AN (Auditory Nerve) | (8,-38,-32) | Peripheral input |
| 23 | CN (Cochlear Nucleus) | (8,-38,-30) | First central processing |
| 24 | SOC (Superior Olivary Complex) | (0,-36,-26) | Binaural hearing |
| 25 | PAG (Periaqueductal Gray) | (0,-30,-10) | Opioid release, pain modulation |

RAM assembly: `ram[region] += Σ(mechanism_output[dim] × link_weight)` → ReLU → z-normalize → sigmoid → [0,1]. RAM is **read-only** — it does not feed back into beliefs or reward.

---

## 5. Test & Validation: What Has Been Done

### Test Infrastructure (7 suites, 450+ test functions)

| Suite | Files | What It Tests |
|-------|-------|---------------|
| **Smoke Test** (11 layers) | 11 | Progressive integration: contracts → R³ → H³ → mechanisms → beliefs → RAM → end-to-end |
| **Benchmark Real Audio** | 11 | 7 real recordings (Bach, Swan Lake, Mahler, etc.), performance, determinism, cross-genre |
| **Micro-Belief Tests** | 37 | Per-belief semantic validation with controlled synthetic stimuli for F1-F9 |
| **Deep Standalone** | 2 | Exhaustive R³ (100+ cases) and F1 (100+ cases) with effect sizes |
| **Functional Tests** | 34 | Stimulus→response validation for F1-F3 mechanisms with custom WAV files |
| **Test Audio Corpus** | 654 WAV | Synthesized stimuli with 349 ordinal comparisons, all literature-grounded |
| **Validation V1-V7** | 35 | External empirical benchmarks against published datasets and studies |

**Coverage: 131/131 beliefs (100%), 84/84 mechanisms, 26/26 regions, 4/4 neurochemicals.**

### Micro-Belief Test Examples

Each belief is tested with controlled stimuli designed to produce known ordinal relationships:

- **BCH consonance**: Unison > P5 > m2 (Sethares 1993)
- **Pitch salience**: Harmonic > Noise > Silence
- **Emotional valence**: Major chord > Minor chord for happiness (Pallesen 2005)
- **Reward**: Consonant crescendo > Dissonant cluster for pleasure (Salimpoor 2011)
- **Motor entrainment**: Isochronous > Random for beat entrainment
- **Groove**: Medium syncopation > Zero syncopation (Madison 2011 inverted-U)
- **Social synchrony**: Multi-voice groove > Solo rubato (Wohltjen 2023)

All 349 ordinal comparisons cite published neuroscience with effect sizes.

### V1-V7 External Validation Results

**25 tests passed, 6 skipped (hardware/data constraints), 0 failed.**

#### V1 — Pharmacological Simulation (11/11 PASS)

Simulates drug effects by modifying neurochemical gain parameters, validates against 3 landmark studies:

**Ferreri et al. (2019, PNAS, N=27) — Dopamine and musical reward:**

| Condition | Reward | DA | Change |
|-----------|--------|-----|--------|
| Levodopa (DA ↑, gain=1.5) | 0.617 | 0.628 | +13.4% |
| Placebo (baseline) | 0.544 | 0.378 | — |
| Risperidone (DA ↓, gain=0.1) | 0.444 | 0.034 | -18.4% |

✓ Levodopa > Placebo > Risperidone ordering reproduced
✓ Effect driven by DA pathway specifically

**Mallik et al. (2017, Scientific Reports, N=15) — Opioid blockade:**

| Condition | Reward | OPI | Change |
|-----------|--------|-----|--------|
| Placebo | 0.544 | 0.500 | — |
| Naltrexone (OPI ↓, gain=0.1) | 0.397 | 0.050 | -27.0% |

✓ Opioid blockade reduces reward by 27%
✓ DA unchanged (0.378 in both conditions) — pathway-specific

**Laeng et al. (2021, Psychophysiology, N=30) — Opioid-arousal dissociation:**

✓ Naltrexone reduces arousal 3× more than valence (|0.135| vs |0.045|)
✓ Replicates arousal-selective effect of opioid blockade

#### V2 — IDyOM Convergent Validity (3/3 PASS)

Cross-modal comparison: MI (processes audio waveforms) vs. IDyOM (processes symbolic MIDI pitch). Using Essen Folksong Collection (10 melodies):

- Mean Pearson r = 0.072 (positive directional agreement)
- Mean Spearman ρ = 0.070
- 1/10 melodies significant at p < 0.05 (usa03: r = 0.295, p = 0.036)

The weak but positive correlation is expected given the fundamental domain gap (acoustic vs. symbolic).

#### V3 — Krumhansl Tonal Hierarchy (7/7 PASS)

MI reproduces Krumhansl & Kessler (1982) probe-tone ratings from audio:
- Major key: Pearson r > 0.85 (p < 0.001)
- Minor key: Pearson r > 0.70 (p < 0.01)
- Correct tonic/dominant prominence
- Major-minor dissociation verified

#### V4 — DEAM Continuous Emotion (3/3 PASS)

MI's Psi-3 affect output compared to human arousal/valence annotations (DEAM dataset, 10 songs, 2 Hz):
- Mean arousal r = 0.156 (positive agreement)
- Mean valence r = positive
- At least 1 song significant at p < 0.05

Limited by 8 GB RAM (10-song subset, 15s effective overlap).

#### V5 — EEG Encoding (SKIPPED — dataset not downloaded)
#### V6 — fMRI ROI Encoding (SKIPPED — requires ≥12 GB RAM)

#### V7 — RSA Analysis (4/4 PASS)

Representational Similarity Analysis (Kriegeskorte 2008):
- Belief RDM (131D) positively correlates with Acoustic RDM (97D) — ✓
- Correlation < 1.0 (beliefs add information beyond acoustics) — ✓
- Both RDMs show temporal structure — ✓

---

## 6. Literature Foundation

### Systematic Review (PRISMA 2020)
- **2,847 studies screened → 612 assessed → 448 included**
- **1,116 empirical claims** extracted (983 from Core-4 relays)
- **634 effect sizes** (574 after Core-4 filtering)
- **416 bibliography entries** in the manuscript
- **91 theoretical models** in manuscript → **96 in implementation** (5 added post-manuscript)
- Random-effects meta-analysis across 4 core processing units:
  - SPU (Sensory): d = 0.84
  - STU (Temporal): d = 0.67
  - IMU (Integration): d = 0.53
  - ARU (Reward): d = 0.83

### Evidence Tiers
- **α (Mechanistic)**: Direct causal evidence with published replication — V1 pharmacology, V4 DEAM
- **β (Integrative)**: Correlational and encoding models — V2 IDyOM, V3 Krumhansl, V5 EEG, V6 fMRI, V7 RSA
- **γ (Speculative)**: Theory-driven with limited direct evidence — F9 social cognition, parts of F8 learning

---

## 7. Implementation Details

### Scale
- **756 Python files** in `Musical_Intelligence/`
- **654 test WAV stimuli** in `Test-Audio/micro_beliefs/`
- **75+ test modules**, **450+ test functions**
- **131/131 beliefs at 100% test coverage**

### Performance
- ~249 fps throughput
- ~1.7 GB peak memory for 30s excerpt
- Deterministic (bit-exact reproducibility verified)
- O(T) linear time and memory scaling
- Runs on MacBook Air M2, 8 GB RAM

### Processing Pipeline (per frame)
```
Audio (44.1 kHz, mono)
  → Mel Spectrogram (1, 128, T)
    → R³ Extraction (B, T, 97) — 9 groups, deterministic
      → H³ Morphology — 637 demand tuples, 32 horizons × 24 morphs × 3 laws
        → C³ Kernel v4.0
          → Phase 0a-0c: Relay mechanisms (depth 0)
          → Phase 1: Encoder mechanisms (depth 1)
          → Phase 2a-2c: Associator mechanisms (depth 2)
          → Phase 3: Belief observe → predict → update
          → RAM: Region activation accumulation (26D)
          → Neuro: Neurochemical accumulation (4D)
          → Psi-3: Experiential output (28D across 6 domains)
          → Reward: 4-component PE-based + hedonic blend
```

---

## 8. What Is Genuinely Novel

### 8.1 Four-Component Reward Decomposition
No existing model decomposes musical reward into surprise + resolution + exploration − monotony with precision weighting and familiarity modulation. This captures the full range from "thrill of the unexpected" to "satisfaction of the familiar" to "boredom of the predictable."

### 8.2 Computational Wanting/Liking Dissociation
DAED provides the first computational model of Berridge's wanting/liking framework for music. continuous temporal_phase signal tracks where the listener is in the anticipation-consummation cycle at every frame.

### 8.3 Multi-Scale Temporal Prediction (32 horizons)
No existing prediction model operates at 32 simultaneous temporal scales. IDyOM is note-by-note (single scale). GTTM analyzes one structural level at a time.

### 8.4 Acoustic-Domain Cognitive Architecture
MI operates on raw audio, not symbolic representations. This means it can model timbral surprise, dynamic change, and spectral events that symbolic models fundamentally cannot.

### 8.5 Precision-Weighted Bayesian Belief Architecture
The adaptive precision mechanism has no analogue in IDyOM (fixed distributions) or GTTM (no dynamics). When predictions are accurate, the system trusts its model. When wrong, it opens up.

### 8.6 Pharmacological Testability
The neurochemical system enables drug-effect simulation — a novel validation paradigm for cognitive architectures. No other music cognition model can simulate levodopa vs. naltrexone effects.

### 8.7 Cross-Function Prediction Modulation
HTP's prediction quality modulates precision for ALL 36 Core Beliefs across ALL 9 Functions. The prediction engine doesn't just predict — it modulates the entire cognitive system's certainty.

---

## 9. Known Limitations

1. **V2 IDyOM correlation is weak** (r = 0.072) — cross-modal gap between acoustic and symbolic domains
2. **V4 DEAM correlation is modest** (arousal r = 0.156) — limited by 10-song subset and 8 GB RAM
3. **V5/V6 skipped** — EEG and fMRI encoding are the strongest potential neural validation but need more hardware
4. **All weights are hand-specified** — no data-driven optimization, no sensitivity analysis
5. **No learning/plasticity** — same input always produces same output, no adaptation across exposures
6. **RAM is one-directional** — brain regions don't feed back into beliefs (neurologically unrealistic)
7. **No ablation study** — with 88 mechanisms and 131 beliefs, model complexity vs. necessity is untested
8. **Synthesized test stimuli** — V2 and V3 use MIDI piano, not real polyphonic music

---

## 10. The Critical Question

This system's strongest scientific contribution appears to be in **musical reward**:

- The 4-component reward formula is genuinely novel
- The wanting/liking computational dissociation has no precedent
- Pharmacological validation (V1) successfully replicates 3 landmark studies
- The inverted-U familiarity modulation is a testable behavioral prediction

The critical test that would establish this as a genuine scientific discovery:

```
MI reward(t)  vs  human continuous pleasure rating
```

If this correlation is significant, the reward formula becomes the first computational model that predicts moment-by-moment musical pleasure from raw audio using neuroscience-grounded mechanisms.

---

## 11. Key Files for Reference

| Component | Path |
|-----------|------|
| Full validation report | `Tests/Docs/MI-Validation-Report.md` |
| Comprehensive test report | `Tests/Docs/MI-Test-Report.tex` (.pdf) |
| Reward formula spec | `Building/Ontology/C³/REWARD-FORMULA.md` |
| Belief cycle spec | `Building/Ontology/C³/BELIEF-CYCLE.md` |
| Precision engine spec | `Building/Ontology/C³/PRECISION-ENGINE.md` |
| Region activation map spec | `Building/Ontology/C³/REGION-ACTIVATION-MAP.md` |
| Model atlas (96 models) | `Building/Ontology/C³/MODEL-ATLAS.md` |
| R³ ontology (frozen) | `Building/Ontology/R³/R3-ONTOLOGY-BOUNDARY.md` |
| H³ ontology (frozen) | `Building/Ontology/H³/H3-ONTOLOGY-BOUNDARY.md` |
| C³ ontology | `Building/Ontology/C³/C3-ONTOLOGY-BOUNDARY.md` |
| Manuscript | `Literature/C³/Manuscript/C³-Meta-Theory-F01.tex` |

---

*This briefing covers the complete MI system as of March 5, 2026.*
*756 Python files | 88 mechanisms | 131 beliefs | 26 brain regions | 4 neurochemicals*
*654 test stimuli | 450+ test functions | 25/31 validation tests passed*
