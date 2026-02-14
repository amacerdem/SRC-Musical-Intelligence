# Spectral Language Manifesto

**Version**: 0.1.0
**Date**: 2026-02-14
**Status**: DRAFT

---

## 1. Declaration

The Musical Intelligence system operates in a single computational language: **spectral**.

Every measurement, every temporal pattern, every data point that flows through R³ and H³ is grounded in the physical properties of sound — frequency content, energy distribution, temporal change, psychoacoustic percepts. No symbolic music theory concept — chord, key, cadence, dominant, tonic, scale degree — exists as a computational primitive in R³ or H³.

Traditional music theory concepts are **emergent properties** that arise in C³ (the cognitive layer) when the brain models spectral+temporal patterns. They are not inputs to the system; they are outputs of it.

---

## 2. Why This Matters

### 2.1 The Problem We're Solving

The MI system contains 96 C³ models derived from 500+ neuroscience and music cognition papers. These papers speak two languages:

**Language A — Spectral/Physical:**
> "Increased roughness and spectral flux at phrase boundaries correlate with heightened prediction error in auditory cortex."

**Language B — Traditional Music Theory:**
> "The unexpected dominant chord creates harmonic tension through syntactic violation of the tonal hierarchy."

Both describe the same phenomenon. But Language B uses abstractions ("dominant chord", "syntactic violation", "tonal hierarchy") that are:
1. **Culture-specific** — Western tonal music theory, not universal
2. **Discretized** — Continuous spectral phenomena forced into categorical labels
3. **Information-lossy** — A "dominant chord" label discards timbre, tuning, voicing, dynamics
4. **Requires symbolic transcription** — f0 detection, chord recognition, key estimation — each introducing errors

Language A describes what the auditory system actually measures. Language B describes what the brain interprets from those measurements.

### 2.2 The Architectural Consequence

If R³ tries to compute "chord recognition" or "syntactic violation", it's doing C³'s job with C³'s language at the wrong layer. This causes:

1. **Error cascade**: Approximate chroma → approximate chord label → approximate "violation" → garbage input to C³
2. **Information loss**: The rich spectral detail is discarded during symbolic labeling
3. **False precision**: A "V chord" label implies certainty about a fundamentally uncertain spectral measurement
4. **Cultural lock-in**: The system only works for 12-TET Western tonal music

If instead R³ provides rich spectral data and H³ provides temporal context, C³ can derive whatever "music theory concepts" it needs from the full spectral evidence.

---

## 3. The Three Layers

### 3.1 R³ — The Spectral Microscope

**Role**: Decompose the audio signal into 128 spectral measurements per 5.8ms frame.

**Language**: Physical properties of sound.
- Frequency-domain energy distribution (mel spectrum → derived features)
- Psychoacoustic percepts (roughness, loudness, sharpness, fusion)
- Spectral shape (centroid, flatness, flux, entropy)
- Pitch-class energy distribution (chroma — NOT "notes", but energy in 12 frequency bands)
- Temporal micro-events (onset strength, spectral change rate)
- Cross-domain interactions (how energy relates to consonance, how change relates to timbre)

**R³ does NOT**:
- Label chords
- Identify keys
- Detect cadences
- Classify intervals by name
- Measure "syntactic irregularity" (this implies syntax → music theory)
- Compute "tonal stability" (this implies tonal hierarchy → music theory)

**R³ DOES**:
- Measure chroma distribution stability over time
- Measure correlation between chroma and reference profiles (Krumhansl-Kessler)
- Measure cosine distance between successive chroma frames
- Measure spectral periodicity, roughness, energy patterns
- These are PHYSICAL MEASUREMENTS, not THEORETICAL INTERPRETATIONS

### 3.2 H³ — The Temporal Lens (First Meaning Layer)

**Role**: Integrate R³ micro-reports across temporal horizons to produce temporal perceptual events.

**What changed from old design**: H³ was conceived as "windowed statistics over R³ features" — a passive computation. In the spectral language framework, H³ is the **first meaning layer**:

```
Old view:  H³ = window(R³_feature, horizon) → statistic
New view:  H³ = integrate(R³_micro_reports, horizon) → temporal perceptual event
```

The difference:
- **Old**: H³ output is a number. "Mean of harmonic_change over 525ms = 0.42"
- **New**: H³ output is a NAMED EVENT with PROVENANCE. "Spectral distance between successive pitch-class distributions has been consistently moderate (mean=0.42) over the past 525ms, with low variance (std=0.08) and slight upward trend — indicating gradual spectral reorganization."

The computation is the same. The FRAMING is different. H³ output is no longer just a statistic — it's the first piece of information that has temporal meaning.

**H³ provides three temporal perspectives (laws)**:
- **L0 (Memory)**: What has the spectral pattern been? (past → present)
- **L1 (Prediction)**: What will the spectral pattern become? (present → future)
- **L2 (Integration)**: What is the complete spectral pattern? (past ↔ future)

**H³ provides 32 temporal scales (horizons)**:
- Micro (5.8ms → 250ms): Individual spectral events, attack transients
- Meso (300ms → 800ms): Perceptual grouping, beat-level patterns
- Macro (1s → 25s): Extended patterns, large-scale spectral trajectories
- Ultra (36s → 981s): Global spectral characteristics

### 3.3 C³ — The Cognitive Brain

**Role**: Receive R³+H³ temporal perceptual events and model cognitive processes.

**C³ is where "music theory" lives** — not as input, but as emergent computation:
- A C³ model for predictive coding (PCU) receives spectral stability patterns and derives what we'd call "tonal expectation"
- A C³ model for reward processing (RPU) receives spectral surprise patterns and derives what we'd call "harmonic tension release"
- A C³ model for motor planning (MPU) receives spectral periodicity patterns and derives what we'd call "metric entrainment"

**C³ models CAN use music-theory language internally** in their documentation. A paper-derived model can say "this model computes harmonic surprise". But what it receives as INPUT is always spectral+temporal data with full provenance.

---

## 4. What We Reject

### 4.1 Rejected: Symbolic Primitives in R³/H³

The following are **NOT** valid R³ or H³ computations:

| Rejected Concept | Why | Spectral Alternative |
|-----------------|-----|---------------------|
| "Chord recognition" | Symbolic label, information-lossy | Chroma template correlation vector (continuous, 12-25D) |
| "Key detection" | Categorical label (C major, A minor) | Pitch-class energy distribution stability (continuous) |
| "Cadence detection" | Music-theory structural concept | Spectral change deceleration + energy pattern at phrase boundaries |
| "Syntactic violation" | Requires music-theory syntax model | Spectral distribution divergence from running statistics |
| "Dominant function" | Music-theory harmonic function | Spectral energy in specific pitch-class relationships |
| "Melodic interval" | Requires note detection | Pitch-class transition pattern in chroma sequence |
| "Meter" | Requires beat hierarchy model | Multi-scale onset periodicity |
| "Phrase boundary" | Music-theory structural concept | Spectral novelty peak + temporal periodicity change |

### 4.2 Rejected: Culture-Specific Assumptions

The following assumptions are **NOT** valid in R³/H³:

- 12-tone equal temperament is the only tuning system
- Octave equivalence is universal (it is, but as a spectral phenomenon, not a theoretical axiom)
- Consonance = simple integer frequency ratios (consonance = low roughness + high fusion + spectral smoothness)
- Music has "notes" (music has spectral events with varying pitch salience)
- Rhythm implies a metrical grid (rhythm = onset periodicity patterns)

### 4.3 Accepted: Music Theory as Emergent Description

Music theory concepts ARE valid as descriptions of what the system computes. The key distinction:

```
WRONG: R³ computes "the key is C major" → H³ tracks "key stability" → C³ uses "key"
RIGHT: R³ measures pitch-class energy distribution → H³ tracks distribution stability
       across horizons → C³ model interprets stable distribution as "key"
```

The computation is grounded in spectral measurement. The interpretation is emergent.

---

## 5. Naming Conventions

### 5.1 R³ Feature Names

R³ features are named by what they MEASURE, not what they MEAN:

| Current Name | Problem | Spectral Name |
|-------------|---------|---------------|
| `key_clarity` | Implies music-theory "key" concept | `pitch_class_profile_correlation_peak` |
| `tonal_stability` | "Tonal" is music-theory language | `chroma_distribution_temporal_consistency` |
| `syntactic_irregularity` | "Syntactic" implies formal grammar | `chroma_divergence_from_diatonic_template` |
| `tonal_ambiguity` | "Tonal" is music-theory language | `pitch_class_distribution_entropy` |
| `melodic_entropy` | "Melodic" implies note sequence | `pitch_class_transition_entropy` |
| `harmonic_entropy` | "Harmonic" ambiguous (spectral vs. music) | `chroma_distribution_divergence` |
| `harmonic_change` | Same ambiguity | `chroma_frame_distance` |
| `voice_leading_distance` | "Voice leading" = music theory | `chroma_L1_distance` |
| `diatonicity` | "Diatonic" = music theory | `pitch_class_template_fit_max` |
| `groove_index` | Subjective, not spectral | `syncopation_bass_pulse_product` |
| `rhythmic_information_content` | OK but could be clearer | `onset_interval_surprisal` |

**Principle**: If you can't explain the name without referencing music theory, rename it.

### 5.2 H³ Output Names

H³ outputs carry their provenance in the name:

```
Format: {r3_spectral_name}.{horizon_label}.{morph_name}.{law_label}

Examples:
  chroma_frame_distance.beat.mean.memory
  pitch_class_profile_correlation.phrase.trend.prediction
  roughness.sub_beat.peak.integration
  onset_strength.measure.periodicity.memory
```

**Horizon labels** (human-readable):
```
micro_1 (H0, 5.8ms)  ...  micro_8 (H7, 250ms)
sub_beat (H8, 300ms)  ...  beat (H12, 525ms)  ...  measure (H15, 800ms)
phrase (H16, 1s)  ...  section (H18, 2s)  ...  passage (H22, 8.5s)
movement (H26, 36s)  ...  work (H31, 981s)
```

### 5.3 C³ Input References

When a C³ model document says "this model uses harmonic surprise", it must map to a specific set of H³ outputs:

```
C³ concept: "harmonic surprise" (from paper: Gold et al. 2019)

Spectral mapping:
  PRIMARY:
    chroma_distribution_divergence.beat.peak.memory         → [88].H12.M4.L0
    chroma_frame_distance.beat.velocity_mean.memory         → [83].H12.M9.L0
    spectral_surprise.beat.max.memory                       → [90].H12.M4.L0

  SUPPORTING:
    pitch_class_profile_correlation.beat.velocity.memory    → [75].H12.M8.L0
    roughness.beat.range.memory                             → [0].H12.M5.L0

  PROVENANCE:
    "Harmonic surprise is computed from the peak divergence of
     pitch-class energy distribution from its running average [88],
     combined with the rate of change of inter-frame chroma distance [83]
     and peak spectral prediction error [90], all measured over
     beat-length windows (525ms) looking backward (memory law).
     This corresponds to what Gold et al. (2019) describe as
     'harmonic prediction error in nucleus accumbens.'"
```

---

## 6. Impact on System Architecture

### 6.1 R³ Changes Required

1. **Rename features** that use music-theory language (Section 5.1)
2. **Remove or reframe** features that are inherently symbolic:
   - `syntactic_irregularity` [86] → reframe as `chroma_divergence_from_diatonic_template`
   - `tonal_stability` [84] → reframe as `chroma_distribution_temporal_consistency`
   - `groove_index` [71] → reframe as composite product (already spectral in implementation)
3. **Computation stays the same** — the underlying math is already spectral. Only the naming and framing change.
4. **Add missing spectral analyses** identified in r3_update_v2.md Tier 1:
   - DFT of chroma (spectral, not music-theory)
   - Tonal centroid norm (geometric, not music-theory)
   - Interval-class content (autocorrelation, not music-theory)

### 6.2 H³ Changes Required

1. **Reframe H³** from "windowed statistics" to "temporal integration layer"
2. **Add provenance metadata** to H³ outputs (Section 5.2)
3. **Define meaningful horizon labels** (sub_beat, beat, phrase, etc. — these are perceptual, not music-theoretic)
4. **Consider cross-feature integration** within groups (future design)

### 6.3 C³ Changes Required

1. **Every model's R³ input mapping** must be translated to spectral language
2. **Section 4.2 (R³ v2 expansion)** in each model doc must use spectral names
3. **H³ demand tuples** must reference spectral feature names
4. **Paper-derived music-theory concepts** must include explicit spectral mapping (Section 5.3)

### 6.4 Migration Strategy

This is a NAMING and FRAMING change, not a computational change:

```
Phase 1: Define spectral vocabulary (THIS DOCUMENT)
Phase 2: Create R³-H³ provenance chain design (02_R3_H3_PIPELINE.md)
Phase 3: Create translation guide (03_TRANSLATION_GUIDE.md)
Phase 4: Rename R³ features in code and docs
Phase 5: Update H³ output format with provenance
Phase 6: Update all 96 C³ model docs with spectral mappings
Phase 7: Validate end-to-end pipeline with new naming
```

Phases 1-3 are design. Phases 4-7 are implementation. The system's behavior does not change — only its language.

---

## 7. Philosophical Foundation

### 7.1 Why Spectral is Universal

Sound is vibration. All music — Western classical, Javanese gamelan, Indian raga, electronic, environmental — is vibration. The cochlea performs spectral decomposition of vibration. This is biology, not culture.

Music theory (Western: chord, key, cadence; Indian: raga, tala, shruti; etc.) is a COGNITIVE MODEL of spectral patterns. Different cultures model the same spectral phenomena differently. A spectral-first system can accommodate all models because it operates at the pre-cognitive level.

### 7.2 The Brain Doesn't Hear "Chords"

The auditory pathway:
1. **Cochlea**: Tonotopic frequency decomposition (spectral)
2. **Cochlear nucleus**: Temporal pattern extraction (spectral + temporal)
3. **Superior olive**: Binaural processing, roughness computation (spectral)
4. **Inferior colliculus**: Periodicity detection, AM coding (spectral + temporal)
5. **Medial geniculate**: Feature binding, streaming (perceptual organization)
6. **Primary auditory cortex (A1)**: Spectral pattern recognition (spectral)
7. **Secondary auditory cortex**: Category formation (FIRST emergence of "chord-like" concepts)
8. **Prefrontal, temporal, limbic**: Musical understanding, emotion, memory

R³ ≈ stages 1-4 (spectral).
H³ ≈ stages 4-6 (temporal integration).
C³ ≈ stages 6-8 (cognitive).

"Chord" first appears at stage 7. It does not belong in stages 1-6.

### 7.3 Information Preservation

Every symbolic label destroys information:

```
Full spectral snapshot (128D at 172Hz):
  roughness=0.23, sethares=0.31, chroma=[0.1,0.05,0.02,0.8,0.03,
  0.02,0.04,0.7,0.02,0.03,0.01,0.6], loudness=0.65, onset=0.12,
  spectral_flux=0.08, pitch_height=0.45, ...

Symbolic label: "C major chord"

What's lost:
  - The specific roughness profile (bright vs. warm C major)
  - The balance between root, third, fifth (open vs. close voicing)
  - The absolute register (C3 vs. C5)
  - The dynamic level
  - The onset character (plucked, bowed, struck)
  - The spectral envelope (piano, guitar, voice)
  - The inharmonicity pattern
  - The micro-detuning
  - 120+ dimensions of spectral detail → 1 categorical label
```

The spectral representation preserves ALL of this. The C³ model can derive "C major" if it needs to, but it doesn't lose the other 120+ dimensions in the process.

---

## 8. Summary

| Principle | Statement |
|-----------|-----------|
| **Language** | MI speaks spectral. One language. All layers. |
| **R³** | Spectral decomposition. Physical measurements. No theory. |
| **H³** | Temporal integration. First meaning. Full provenance. |
| **C³** | Cognitive modeling. Theory emerges here. |
| **Naming** | Names describe measurement, not interpretation. |
| **Provenance** | Every C³ input traces back to R³ source + H³ processing. |
| **Universality** | Works for any music, any culture, any sound. |
| **Computation** | Math stays the same. Language changes. |

---

**Next**: [02_R3_H3_PIPELINE.md](02_R3_H3_PIPELINE.md) — The provenance chain and what C³ actually sees.
