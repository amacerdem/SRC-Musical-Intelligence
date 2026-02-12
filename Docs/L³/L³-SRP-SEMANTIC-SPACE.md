> **DEPRECATED** — This document describes the old SRP-only semantic space (v1.x).
> Superseded by [L³-BRAIN-SEMANTIC-SPACE.md](L³-BRAIN-SEMANTIC-SPACE.md) which covers
> the unified 104D L³ layer (8 groups α→θ) for the MusicalBrain. Retained for historical reference.

# L³ — Semantic Space for the SRP Model

> Musical Intelligence (MI) v1.1.0 — 2026-02-11
> The interpretation layer: giving meaning to computation.
> Scope: ARU-α1-SRP model. See also: [L³-AAC-SEMANTIC-SPACE.md](L³-AAC-SEMANTIC-SPACE.md) for AAC (α2).

---

## 1. What Is L³?

L³ (Lexical LOGOS Lattice) is MI's **semantic interpretation layer**. It
answers the question: "What does this computation MEAN?"

The SRP model produces 19 scalar values per frame (Level 1 — computation).
These are numbers. By themselves, they say nothing about brain regions,
subjective experience, or how to test them. L³ provides the three
interpretation layers that give the 19D computation its scientific and
psychological meaning:

```
┌─────────────────────────────────────────────────────────────────┐
│                     L³ SEMANTIC SPACE                            │
│                                                                  │
│  ┌─── Group α ── Computation Semantics (Level 1) ───────── 6D  │
│  │   What does the formula do? Which pathway dominates?         │
│  │                                                               │
│  ├─── Group β ── Neuroscience Semantics (Level 2) ────── 14D   │
│  │   Which brain region? Which neurotransmitter?                 │
│  │                                                               │
│  ├─── Group γ ── Psychology Semantics (Level 3) ──────── 13D   │
│  │   Which subjective experience? What emotion?                  │
│  │                                                               │
│  └─── Group δ ── Validation Semantics (Level 4) ──────── 12D   │
│      What can we measure? How do we test?                        │
│                                                                  │
│  TOTAL L³: 45D interpretation for 19D computation                │
│  COMPLETE SEMANTIC FOOTPRINT: 19D + 45D = 64D                   │
└─────────────────────────────────────────────────────────────────┘
```

### Why L³ Exists

A number is not knowledge. `da_caudate = 0.73` means nothing without
context. L³ provides three layers of context:

1. **For neuroscientists**: "This value correlates with caudate nucleus DA
   release (Salimpoor 2011, r=0.71)" → Group β
2. **For psychologists**: "This represents anticipatory wanting — the
   listener desires to hear what comes next" → Group γ
3. **For experimenters**: "Test this by comparing with fMRI caudate BOLD
   signal during self-selected music" → Group δ

And even the computation itself benefits from interpretation:

4. **For implementers**: "This value is 50% driven by cognitive processing
   (C0P), 30% by climax trajectory (CPD), 20% by expectancy (AED)" → Group α

### L³ Dimensions Are Temporal

Like SRP outputs, L³ dimensions are **per-frame temporal signals** (172.27 Hz).
They are computed FROM SRP outputs (and sometimes from mechanism intermediates).
They are NOT static labels — they change over time as the music unfolds.

### Relationship to D0's Ψ⁰

The old D0 pipeline had Ψ⁰ (2,560D): Polarity (512D), Vocabulary (1,024D),
Narrative (512D), Cross (384D), Reserved (128D). MI's L³ is conceptually
different:

| | D0 Ψ⁰ | MI L³ |
|---|---|---|
| Purpose | Linguistic text generation | Scientific interpretation |
| Structure | Flat dimensional allocation | 4 epistemological groups |
| Scope | All 8,192D manifold | Per-model (SRP=45D) |
| Content | Vocabulary terms, polarity axes | Brain regions, psychology, validation |
| Growth | Fixed at 2,560D | Grows with each new model |

---

## 2. Deep Analysis: SRP 19D → 4-Level Semantic Mapping

Before enumerating L³ dimensions, we trace each SRP output through all
four interpretive levels. This is the **complete semantic identity** of
every dimension the SRP model produces.

### Layer N — Neurochemical (3D)

#### N0: da_caudate

| Level | Content |
|-------|---------|
| **L1 Computation** | `σ(0.5 × c0p_processing + 0.3 × cpd_climax + 0.2 × aed_expectancy)` |
| **L2 Neuroscience** | Caudate nucleus dopamine release. Anticipatory ramp 2-30s before peak (Salimpoor 2011, Howe 2013). Tonic DA signal — slow, sustained. |
| **L3 Psychology** | "Wanting" — incentive salience (Berridge 2003). Anticipatory pleasure, motivation to keep listening. "I want to hear what comes next." |
| **L4 Validation** | Should ramp before pleasure peaks. fMRI caudate BOLD correlation r ≈ 0.71 (Salimpoor 2011, n=8, PET [11C]raclopride). |
| **Dependencies** | C0P processing (50%) + CPD climax (30%) + AED expectancy (20%) |
| **Mechanism paths** | C0P → c0p_processing = mean(C0P[10:18]); CPD → cpd_climax = mean(CPD[10:18]); AED → aed_expectancy = mean(AED[8:16]) |

#### N1: da_nacc

| Level | Content |
|-------|---------|
| **L1 Computation** | `σ(0.6 × c0p_cognitive + 0.3 × cpd_release + 0.1 × aed_arousal)` |
| **L2 Neuroscience** | Nucleus Accumbens DA release. Consummatory burst at peak moment (Salimpoor 2011). Phasic DA — fast, transient. |
| **L3 Psychology** | "Liking" — hedonic impact (Berridge 2003). Pleasure at the moment of experience. "This sounds beautiful right now." |
| **L4 Validation** | Should spike at chill moments. fMRI NAcc BOLD correlation r ≈ 0.84 (Salimpoor 2011). |
| **Dependencies** | C0P cognitive (60%) + CPD release (30%) + AED arousal (10%) |
| **Mechanism paths** | C0P → c0p_cognitive = mean(C0P[0:10]); CPD → cpd_release = mean(CPD[18:24]); AED → aed_arousal = mean(AED[0:8]) |

#### N2: opioid_proxy

| Level | Content |
|-------|---------|
| **L1 Computation** | `σ(0.4 × consonance_mean + 0.3 × AED[15] + 0.3 × smoothness)` |
| **L2 Neuroscience** | μ-opioid receptor activation. Hedonic "gloss" overlaid on dopaminergic reward (Nummenmaa 2025, Mallik 2017). |
| **L3 Psychology** | Pure sensory pleasure — distinct from wanting. Consonance + smoothness → pleasant sensory experience. |
| **L4 Validation** | Should be high during consonant, smooth passages. Naltrexone (μ-opioid antagonist) should suppress (Mallik 2017). |
| **Dependencies** | H³ direct reads (70%) + AED[15] resolution_satisfaction (30%) |
| **Mechanism paths** | consonance_mean = H³(H18, M0, L2); smoothness = H³(H18, M15, L2); AED[15] from mechanism |

### Layer C — Circuit (3D)

#### C0: vta_drive

| Level | Content |
|-------|---------|
| **L1** | `σ(0.5 × da_caudate + 0.5 × da_nacc)` |
| **L2** | VTA (Ventral Tegmental Area) activation. Source of mesolimbic DA projections to NAcc and caudate (Blood & Zatorre 2001, Menon & Levitin 2005). |
| **L3** | Reward circuit engagement — how strongly music activates the entire reward system. |
| **L4** | Should track overall musical engagement. High for favorite music, low for musical anhedonia (Martinez-Molina 2016, d=3.6-7.0). |

#### C1: stg_nacc_coupling

| Level | Content |
|-------|---------|
| **L1** | `σ(0.6 × aed_arousal + 0.4 × dynamic_intensity)` |
| **L2** | STG→NAcc functional connectivity. Auditory processing feeding reward system (Salimpoor 2013). |
| **L3** | "Musicality" — how well the auditory experience translates into reward value. |
| **L4** | Should predict willingness-to-pay (Salimpoor 2013: STG-NAcc connectivity predicted auction bids). |

#### C2: prediction_error

| Level | Content |
|-------|---------|
| **L1** | `tanh(AED[13])` where AED[13] = `tanh(h0[M18,L0] - h0[M18,L1])` |
| **L2** | Reward Prediction Error (Schultz 1997). Phasic DA burst (positive RPE) or dip (negative RPE). 50-110ms latency. |
| **L3** | "Better/worse than expected." Positive = pleasant surprise. Negative = disappointment. Zero = predictable. |
| **L4** | Should spike +1 at confirmed predictions, -1 at violations, ~0 for predictable passages. Bipolar (tanh). |

### Layer P — Psychological (3D)

#### P0: wanting

| Level | Content |
|-------|---------|
| **L1** | `σ(0.71 × da_caudate)` — β₂ coefficient from Salimpoor 2011 |
| **L2** | Berridge's incentive salience. DA-mediated anticipatory drive (Berridge & Robinson 2003). |
| **L3** | Anticipatory desire. "I want to hear what comes next." |
| **L4** | Must ramp BEFORE liking peaks (temporal dissociation). Should decrease with repeated exposure. |

#### P1: liking

| Level | Content |
|-------|---------|
| **L1** | `σ(0.84 × da_nacc)` — β₁ coefficient from Salimpoor 2011 |
| **L2** | Berridge's hedonic "liking." Opioid + DA convergence in NAcc shell (Berridge 2007). |
| **L3** | In-the-moment pleasure. "This sounds beautiful right now." |
| **L4** | Must spike AT chill moments (not before). Should track with opioid_proxy. |

#### P2: pleasure

| Level | Content |
|-------|---------|
| **L1** | `clamp(0.84 × da_nacc + 0.71 × da_caudate, 0, 1)` |
| **L2** | Integrated reward signal — both anticipatory and consummatory DA components. |
| **L3** | Overall musical pleasure. The "final answer" of the reward circuit. |
| **L4** | Should track self-reported pleasure. Broader temporal peak than liking alone. |

### Layer T — Temporal/ITPRA (4D)

#### T0: tension

| Level | Content |
|-------|---------|
| **L1** | `σ(0.5 × cpd_buildup + 0.3 × harmonic_tension + 0.2 × AED[14])` |
| **L2** | Huron ITPRA "Tension" response. Autonomic arousal during uncertainty (Huron 2006). |
| **L3** | "Something is about to happen." Suspense, anticipation of resolution. |
| **L4** | Should build during dominant 7th chords, drop at resolution to tonic. |

#### T1: prediction_match

| Level | Content |
|-------|---------|
| **L1** | `tanh(AED[12] - AED[11])` (prediction_pleasure - violation_magnitude) |
| **L2** | Huron ITPRA "Prediction" response. Confirmed vs violated expectations. |
| **L3** | "That's what I expected" (+1) vs "That surprised me" (-1). |
| **L4** | Should be positive for predictable progressions, negative for deceptive cadences. |

#### T2: reaction

| Level | Content |
|-------|---------|
| **L1** | `σ(0.5 × CPD[0] + 0.5 × AED[1])` (melodic_tension + arousal_change) |
| **L2** | Huron ITPRA "Reaction" response. Fast reflexive autonomic response (50-200ms). |
| **L3** | Startle-like immediate response to musical events. |
| **L4** | Should spike at sudden dynamic changes, sforzando, unexpected instrument entries. |

#### T3: appraisal

| Level | Content |
|-------|---------|
| **L1** | `σ(0.4 × pleasure + 0.3 × prediction_match + 0.3 × opioid_proxy)` |
| **L2** | Huron ITPRA "Appraisal" response. PFC-mediated conscious evaluation (0.5-2s delay). |
| **L3** | "That was beautiful" — reflective aesthetic judgment. |
| **L4** | Must lag behind pleasure by 0.5-2s. Should integrate prediction success with hedonic value. |

### Layer M — Musical (3D)

#### M0: harmonic_tension

| Level | Content |
|-------|---------|
| **L1** | `σ(0.5 × roughness_trend + 0.3 × inv_consonance + 0.2 × entropy)` |
| **L2** | STG harmonic processing. Dissonance detection in auditory cortex. |
| **L3** | Musical tension from harmony — dissonant chords create tension, consonant chords release it. |
| **L4** | Should be high for diminished/augmented chords, low for major triads. |

#### M1: dynamic_intensity

| Level | Content |
|-------|---------|
| **L1** | `σ(0.7 × energy_velocity + 0.3 × energy_acceleration)` |
| **L2** | Auditory cortex loudness change detection. Belt/parabelt amplitude envelope tracking. |
| **L3** | "The music is getting louder/softer." Crescendo/decrescendo perception. |
| **L4** | Should correlate with actual dB changes. High during crescendos. |

#### M2: peak_detection

| Level | Content |
|-------|---------|
| **L1** | `σ(0.5 × cpd_buildup + 0.5 × cpd_release)` |
| **L2** | NAcc DA burst threshold crossing. "Chill moment" detector. |
| **L3** | "This is a peak moment in the music." Climax detection. |
| **L4** | Should fire at self-reported chills (±1s tolerance). ~3.7 peaks per excerpt average (Salimpoor 2011). |

### Layer F — Forecast (3D)

#### F0: reward_forecast

| Level | Content |
|-------|---------|
| **L1** | `σ(0.6 × da_caudate + 0.4 × cpd_climax)` |
| **L2** | Caudate anticipatory ramp. Howe 2013 quasi-hyperbolic approach signal. |
| **L3** | "Something rewarding is coming." Forward-looking reward expectation. |
| **L4** | Should ramp 15-30s before major peaks. Should follow caudate quasi-hyperbolic profile. |

#### F1: chills_proximity

| Level | Content |
|-------|---------|
| **L1** | `σ(0.5 × da_nacc + 0.3 × cpd_release + 0.2 × aed_expectancy)` |
| **L2** | DA + opioid convergence approaching ANS threshold for piloerection. |
| **L3** | "Goosebumps are about to happen." Proximity to chill moment. |
| **L4** | Should peak 0-5s before self-reported chills. |

#### F2: resolution_expect

| Level | Content |
|-------|---------|
| **L1** | `σ(0.6 × c0p_integration + 0.4 × aed_expectancy)` |
| **L2** | Prefrontal expectation of harmonic resolution (Koelsch 2014). |
| **L3** | "The tension will resolve soon." Expectation of consonance. |
| **L4** | Should be high during prolonged dominant chords. Drops after resolution. |

---

## 3. L³ Dimension Groups

### Overview

| Group | Level | Dimensions | What It Provides |
|-------|-------|------------|-----------------|
| **α** | L1 — Computation | 6D | Which pathways are active, signal confidence |
| **β** | L2 — Neuroscience | 14D | Brain regions, neurotransmitters, circuits |
| **γ** | L3 — Psychology | 13D | Reward, ITPRA, aesthetics, emotion, chills |
| **δ** | L4 — Validation | 12D | Physiological, neural, behavioral predictions |
| | | **45D** | **Total L³ interpretation space** |

Combined with the 19D SRP computation:

**Complete SRP semantic footprint: 19D + 45D = 64D (2^6)**

---

## 4. Group α — Computation Semantics (6D)

These dimensions interpret WHAT the computation is doing at each frame.
They are meta-signals about the SRP pipeline state.

### α0: aed_contribution [0, 1]

**Formula**: Fraction of active SRP dimensions whose dominant input traces
to AED mechanism sub-section means (aed_arousal, aed_expectancy) or direct
AED dimension reads (AED[1], AED[11-15]).

**What it reveals**: When α0 is high, the system is in "arousal-expectancy
mode" — the current musical moment is dominated by how the body responds
(arousal) and what it anticipates (expectancy). Typical during dynamic
passages with strong emotional engagement.

**Feeds from SRP**: N2 (AED[15]), C1 (aed_arousal), C2 (AED[13]),
T0 (AED[14]), T1 (AED[11,12]), T2 (AED[1]), F2 (aed_expectancy)

### α1: cpd_contribution [0, 1]

**Formula**: Fraction of active SRP dimensions whose dominant input traces
to CPD mechanism sub-section means (cpd_buildup, cpd_climax, cpd_release)
or direct CPD reads (CPD[0]).

**What it reveals**: When α1 is high, the system is in "chill-detection
mode" — the music is approaching, at, or receding from a peak moment.
Typical near climactic passages.

**Feeds from SRP**: N0 (cpd_climax), N1 (cpd_release), T0 (cpd_buildup),
T2 (CPD[0]), M2 (cpd_buildup, cpd_release), F0 (cpd_climax), F1 (cpd_release)

### α2: c0p_contribution [0, 1]

**Formula**: Fraction of active SRP dimensions whose dominant input traces
to C0P mechanism sub-section means (c0p_cognitive, c0p_processing,
c0p_integration).

**What it reveals**: When α2 is high, the system is in "cognitive mode" —
the brain's processing state (attention, prediction, memory) dominates the
output. Typical during complex, intellectually engaging passages.

**Feeds from SRP**: N0 (c0p_processing), N1 (c0p_cognitive), F2 (c0p_integration)

### α3: direct_read_contribution [0, 1]

**Formula**: Fraction of active SRP dimensions whose dominant input traces
to direct H³/R³ reads (consonance_mean, smoothness, roughness_trend,
energy_velocity, energy_acceleration, entropy, inv_consonance).

**What it reveals**: When α3 is high, the system is in "music-driven mode" —
the musical features themselves (harmony, dynamics) dominate over neural
circuit modeling. Typical during passages with strong harmonic or dynamic
character.

**Feeds from SRP**: N2 (consonance_mean, smoothness), T0 (harmonic_tension),
M0 (roughness_trend, inv_consonance, entropy), M1 (energy_velocity,
energy_acceleration)

**Constraint**: α0 + α1 + α2 + α3 ≈ 1 (sums to approximately 1, allowing
for mixed attribution when multiple pathways contribute equally).

### α4: computation_certainty [0, 1]

**Formula**: Mean distance from 0.5 across all 17 sigmoid-based SRP
dimensions (excluding the 2 tanh dimensions: prediction_error and
prediction_match).

```
α4 = mean(|SRP_σ[i] - 0.5|) × 2   for all σ-activated dims
```

**What it reveals**: When α4 is high, the system is making **confident
decisions** — most sigmoid outputs are near 0 or 1. When low, the system
is in an **ambiguous state** — outputs hover near 0.5 (maximum uncertainty
for a sigmoid).

**Interpretation**: High certainty during musical passages with clear
emotional character (loud climax → high certainty). Low certainty during
ambiguous transitions (key change in progress → low certainty).

### α5: bipolar_activation [-1, 1]

**Formula**: Mean of the 2 tanh-activated SRP dimensions
(prediction_error, prediction_match).

```
α5 = mean(prediction_error, prediction_match)
```

**What it reveals**: The system's **prediction state**. Positive → the
music is confirming or exceeding expectations. Negative → the music is
violating expectations. Near zero → the music is predictable/neutral.

**Interpretation**: This is the "surprise compass" — it tells you whether
the system is in a state of positive surprise (delight), negative surprise
(disappointment), or neutral tracking.

---

## 5. Group β — Neuroscience Semantics (14D)

These dimensions map SRP outputs to brain structures, neurotransmitters,
and neural circuits. They are the Level 2 interpretation: "What would a
neuroscientist see?"

### Brain Region Activations (8D)

Each brain region aggregates multiple SRP dimensions that neuroscience
literature associates with that region.

#### β0: caudate_activation [0, 1]

**Formula**: `σ(0.5 × da_caudate + 0.3 × wanting + 0.2 × reward_forecast)`

**Neuroscience**: Caudate nucleus — dorsal striatum. Primary site of
anticipatory DA release during music (Salimpoor 2011). Part of the
nigrostriatal pathway. Active during approach behavior and reward
expectation.

**SRP sources**: N0 da_caudate (direct mapping), P0 wanting (scaled),
F0 reward_forecast (anticipatory ramp). All three involve caudate
processing.

#### β1: nacc_activation [0, 1]

**Formula**: `σ(0.35 × da_nacc + 0.25 × liking + 0.15 × pleasure + 0.15 × peak_detection + 0.10 × chills_proximity)`

**Neuroscience**: Nucleus Accumbens — ventral striatum. Site of
consummatory DA release and opioid hedonic "hotspot" (Berridge 2007).
Active during peak pleasure moments.

**SRP sources**: N1 da_nacc, P1 liking, P2 pleasure, M2 peak_detection,
F1 chills_proximity. All involve NAcc processing.

#### β2: vta_activation [0, 1]

**Formula**: `vta_drive` (direct mapping)

**Neuroscience**: Ventral Tegmental Area — midbrain dopamine source.
Projects to both NAcc (mesolimbic) and PFC (mesocortical). The "master
switch" of the reward circuit (Blood & Zatorre 2001, Menon & Levitin 2005).

#### β3: stg_activation [0, 1]

**Formula**: `σ(0.5 × stg_nacc_coupling + 0.3 × harmonic_tension + 0.2 × dynamic_intensity)`

**Neuroscience**: Superior Temporal Gyrus — auditory association cortex.
Processes musical structure (harmony, melody) and feeds reward evaluation
via STG→NAcc pathway (Salimpoor 2013).

#### β4: auditory_cortex_activation [0, 1]

**Formula**: `σ(0.6 × dynamic_intensity + 0.4 × reaction)`

**Neuroscience**: Primary auditory cortex (A1) and belt regions. Encodes
acoustic features: spectral content, amplitude envelope, onset detection.
The first cortical stage of auditory processing.

#### β5: pfc_activation [0, 1]

**Formula**: `σ(0.35 × appraisal + 0.30 × resolution_expect + 0.20 × prediction_match + 0.15 × reward_forecast)`

**Neuroscience**: Prefrontal Cortex — executive control, conscious
evaluation, planning. Active during aesthetic appraisal (Koelsch 2014),
expectation formation, and goal-directed listening.

#### β6: insula_activation [0, 1]

**Formula**: `σ(0.4 × tension + 0.3 × reaction + 0.2 × dynamic_intensity + 0.1 × chills_proximity)`

**Neuroscience**: Insular cortex — interoception, autonomic awareness.
Bridges bodily sensations (heart rate, skin conductance) with conscious
emotional experience. Critical for "feeling" musical emotions.

#### β7: amygdala_activation [0, 1]

**Formula**: `σ(0.4 × |prediction_error| + 0.3 × reaction + 0.2 × tension + 0.1 × |prediction_match|)`

**Neuroscience**: Amygdala — salience detection, fear/surprise processing.
Active during unexpected musical events (deceptive cadences, sudden
dynamic changes). Uses absolute values because amygdala responds to
salience regardless of valence.

### Neurotransmitter Dynamics (3D)

#### β8: da_tonic [0, 1]

**Formula**: `low_pass(da_caudate, τ=500ms)`

**Neuroscience**: Tonic dopamine — sustained, baseline DA level. Reflects
the slow caudate ramp (Howe 2013). Changes over seconds, not milliseconds.
The "wanting signal."

**Computation note**: Low-pass filter with ~500ms time constant on
da_caudate. This separates the slow anticipatory ramp from frame-by-frame
fluctuations.

#### β9: da_phasic [0, 1]

**Formula**: `max(prediction_error, 0)` (rectified positive RPE)

**Neuroscience**: Phasic dopamine burst — fast, transient DA release at
reward receipt or positive prediction error (Schultz 1997, 2016). Duration
< 200ms. The "surprise/reward signal."

#### β10: da_dip [0, 1]

**Formula**: `max(-prediction_error, 0)` (rectified negative RPE)

**Neuroscience**: Phasic dopamine dip — transient DA decrease at reward
omission or negative prediction error (Schultz 2016). The
"disappointment signal."

### Circuit States (3D)

#### β11: mesolimbic_engagement [0, 1]

**Formula**: `σ(0.4 × vta_drive + 0.3 × pleasure + 0.2 × wanting + 0.1 × liking)`

**Neuroscience**: Overall mesolimbic reward circuit engagement. The VTA →
NAcc/Caudate → PFC loop. When high, music is actively engaging the reward
system. When low (as in musical anhedonia), auditory processing is intact
but reward is absent (Martinez-Molina 2016).

#### β12: prediction_circuit [0, 1]

**Formula**: `σ(0.4 × |prediction_error| + 0.3 × (1 - |prediction_match|) + 0.3 × tension)`

**Neuroscience**: Cortical prediction hierarchy engagement. Active when
the brain is actively generating and testing predictions. High during
uncertain, expectation-rich passages. Low during familiar, predictable
music.

#### β13: autonomic_arousal [0, 1]

**Formula**: `σ(0.35 × tension + 0.25 × reaction + 0.20 × dynamic_intensity + 0.10 × |prediction_error| + 0.10 × chills_proximity)`

**Neuroscience**: Autonomic nervous system activation. Composite of all
SRP dimensions that would produce measurable physiological responses
(heart rate, skin conductance, pupil dilation, respiration).

---

## 6. Group γ — Psychology Semantics (13D)

These dimensions map SRP outputs to psychological constructs and subjective
experience. They are the Level 3 interpretation: "What does the listener
feel?"

### Reward Decomposition (3D)

#### γ0: wanting_liking_gap [-1, 1]

**Formula**: `wanting - liking`

**Psychology**: The **temporal dissociation** between wanting and liking
(Berridge & Robinson 2003). This is a key SRP validation target — wanting
must lead liking in time.

| Value | Interpretation |
|-------|---------------|
| > 0 | Anticipation exceeds current pleasure — "building up" |
| ≈ 0 | Balanced — wanting and liking are synchronized |
| < 0 | Current pleasure exceeds anticipation — "surprised by beauty" |

**Validation**: During the Chill Test, γ0 should be positive 5-30s before
the chill (wanting ramps first), then drop to negative at the chill moment
(liking spikes past wanting), then return to ~0 during decay.

#### γ1: reward_type [0, 1]

**Formula**: `opioid_proxy / (opioid_proxy + (da_nacc × da_caudate) + ε)`

**Psychology**: Balance between **sensory pleasure** (opioid-mediated:
consonance, smoothness) and **motivational pleasure** (DA-mediated:
prediction, anticipation).

| Value | Interpretation |
|-------|---------------|
| → 1 | Sensory-driven pleasure (beautiful harmony, warm timbre) |
| → 0 | Motivation-driven pleasure (tension-resolution, surprise) |
| ≈ 0.5 | Mixed — both sensory and motivational |

#### γ2: temporal_anticipation [-1, 1]

**Formula**: `reward_forecast - pleasure`

**Psychology**: How much the system is **looking forward** vs **experiencing
now**. Positive = the best is yet to come. Negative = the current moment is
the best.

### ITPRA Dynamics (2D)

#### γ3: itpra_dominant_phase [0, 1]

**Formula**: Soft classification across ITPRA phases:

```
I_score = reward_forecast
T_score = tension
P_score = σ(|prediction_match|)
R_score = reaction
A_score = appraisal

γ3 = weighted_index_of_max(I=0.0, T=0.25, P=0.50, R=0.75, A=1.0)
```

**Psychology**: Which ITPRA phase (Huron 2006) dominates at this moment?

| Range | Phase | Cognitive State |
|-------|-------|----------------|
| 0.0-0.12 | I — Imagination | Anticipating, predicting |
| 0.13-0.37 | T — Tension | Uncertain, aroused |
| 0.38-0.62 | P — Prediction | Evaluating match/mismatch |
| 0.63-0.87 | R — Reaction | Reflexive response |
| 0.88-1.0 | A — Appraisal | Conscious evaluation |

#### γ4: itpra_intensity [0, 1]

**Formula**: `max(reward_forecast, tension, |prediction_match|, reaction, appraisal)`

**Psychology**: How intensely the ITPRA system is engaged, regardless of
which phase. High during emotionally powerful passages, low during neutral
passages.

### Aesthetic Experience (3D)

#### γ5: aesthetic_value [0, 1]

**Formula**: `σ(0.35 × pleasure + 0.30 × opioid_proxy + 0.20 × appraisal + 0.15 × stg_nacc_coupling)`

**Psychology**: Integrated aesthetic evaluation. Combines hedonic pleasure,
sensory beauty, conscious appraisal, and auditory-reward connectivity. The
closest L³ dimension to "how beautiful is this music right now?"

#### γ6: engagement [0, 1]

**Formula**: `σ(0.4 × vta_drive + 0.3 × stg_nacc_coupling + 0.3 × wanting)`

**Psychology**: Listener engagement — how much attention and motivation
the music captures. High engagement = the listener is "in the music."
Low engagement = background music, not attending.

#### γ7: flow_proximity [0, 1]

**Formula**: `σ(0.4 × wanting + 0.3 × (1 - |prediction_error|) + 0.3 × aesthetic_value)`

**Psychology**: Proximity to musical flow state (Csikszentmihalyi 1990).
Flow requires: wanting (motivation), low prediction error (skill matches
challenge), and aesthetic value (intrinsic reward). High flow_proximity
means the listener is absorbed in the music.

### Emotional State (2D)

#### γ8: emotional_valence [-1, 1]

**Formula**: `tanh(pleasure - harmonic_tension)`

**Psychology**: Positive/negative affect balance (Russell's circumplex
model). Positive valence during pleasant, resolved music. Negative valence
during tense, dissonant passages.

#### γ9: emotional_arousal [0, 1]

**Formula**: `σ(0.4 × reaction + 0.3 × dynamic_intensity + 0.2 × tension + 0.1 × |prediction_error|)`

**Psychology**: Physiological arousal level (Russell's circumplex).
High arousal during loud, fast, surprising music. Low arousal during
quiet, slow, predictable music.

### Chills/Frisson (3D)

#### γ10: chill_probability [0, 1]

**Formula**: `σ(3.0 × (chills_proximity + peak_detection - 1.2))`

**Psychology**: Probability that the listener will experience goosebumps
in the next 1-5 seconds. Uses a steep sigmoid with threshold — chills
are binary events with graded approach.

| Value | Interpretation |
|-------|---------------|
| < 0.2 | No chill expected |
| 0.2-0.5 | Building toward chill |
| 0.5-0.8 | Chill likely imminent |
| > 0.8 | Chill occurring or about to occur |

#### γ11: chill_phase [0, 1]

**Formula**: State machine driven by chill_probability temporal profile:

```
0.0 = Baseline (no chill in recent or near future)
0.2 = Buildup (chill_probability rising, < 0.5)
0.4 = Approach (chill_probability > 0.5 and rising)
0.6 = Peak (chill_probability at local maximum)
0.8 = Decay (chill_probability falling from peak)
1.0 = Refractory (10-30s post-chill, system resetting)
```

**Psychology**: Maps the complete lifecycle of a chill event. Useful for
understanding the temporal dynamics of musical frisson (Grewe et al. 2009:
inter-chill refractory ~10-30s).

#### γ12: resolution_tension_ratio [0, 1]

**Formula**: `resolution_expect / (tension + resolution_expect + ε)`

**Psychology**: Balance between accumulated tension and expectation of
resolution. When high (→1), resolution feels imminent. When low (→0),
tension dominates with no clear resolution in sight.

---

## 7. Group δ — Validation Semantics (12D)

These dimensions are **predictions about measurable responses**. They
translate SRP outputs into what a researcher should observe in the lab.
Level 4: "How do we test this?"

### Physiological Predictions (4D)

#### δ0: predicted_scr [0, 1]

**Formula**: `σ(0.35 × tension + 0.25 × reaction + 0.20 × peak_detection + 0.10 × |prediction_error| + 0.10 × chills_proximity)`

**Target**: Skin conductance response (SCR). Measurable via galvanic
skin response electrodes.

**Evidence**: Ferreri 2019: SCR during musical pleasure, t(25)=-2.26,
P=0.033. Chills produce measurable SCR spikes.

#### δ1: predicted_hr_change [-1, 1]

**Formula**: `tanh(0.35 × wanting + 0.25 × tension - 0.20 × liking + 0.20 × dynamic_intensity)`

**Target**: Heart rate change (positive = acceleration, negative =
deceleration). Measurable via ECG/PPG.

**Note**: Wanting and tension accelerate HR (sympathetic). Liking
decelerates HR briefly (parasympathetic vagal response during peak
pleasure). This creates the characteristic HR deceleration at the
moment of chill.

#### δ2: predicted_pupil [0, 1]

**Formula**: `σ(0.4 × |prediction_error| + 0.3 × tension + 0.2 × reaction + 0.1 × wanting)`

**Target**: Pupil dilation. Measurable via eye tracking.

**Evidence**: Pupil dilation correlates with cognitive load, surprise,
and autonomic arousal — all of which are tracked by SRP.

#### δ3: predicted_piloerection [0, 1]

**Formula**: `σ(4.0 × (chills_proximity + peak_detection - 1.4))`

**Target**: Piloerection (goosebumps). Measurable via goosebump camera
or self-report button press.

**Evidence**: Occurs in ~50% of chill episodes (de Fleurian & Pearce 2021).
Very steep threshold — either happens or doesn't.

### Neural Correlate Predictions (3D)

#### δ4: predicted_caudate_bold [0, 1]

**Formula**: `0.71 × da_caudate`

**Target**: fMRI BOLD signal in caudate nucleus.

**Evidence**: Salimpoor 2011: PET [11C]raclopride binding during anticipation
correlated r=0.71 with pleasure ratings. This β₂ coefficient directly
scales da_caudate.

#### δ5: predicted_nacc_bold [0, 1]

**Formula**: `0.84 × da_nacc`

**Target**: fMRI BOLD signal in nucleus accumbens.

**Evidence**: Salimpoor 2011: PET [11C]raclopride binding during peak
pleasure correlated r=0.84. This β₁ coefficient directly scales da_nacc.

#### δ6: predicted_wtp [0, 1]

**Formula**: `σ(0.6 × stg_nacc_coupling + 0.4 × pleasure)`

**Target**: Willingness-to-pay in a music auction paradigm.

**Evidence**: Salimpoor 2013: STG→NAcc functional connectivity during
first listen predicted subsequent auction bids for unfamiliar music.

### Behavioral Predictions (2D)

#### δ7: predicted_pleasure_rating [0, 1]

**Formula**: `pleasure` (direct mapping)

**Target**: Continuous self-reported pleasure rating (slider/dial).

**Note**: This is the most straightforward validation target — the
integrated pleasure signal should track what listeners report feeling.

#### δ8: predicted_chill_report [0, 1]

**Formula**: `σ(5.0 × (peak_detection - 0.6))`

**Target**: Chill button press (binary: did the listener press the
"I felt a chill" button?).

**Evidence**: Self-reported chills should align with peak_detection
firing. Average ~3.7 chills per excerpt (Salimpoor 2011). Tolerance:
±1 second.

### Temporal Constraint Validation (3D)

#### δ9: wanting_leads_liking [-1, 1]

**Formula**: `temporal_derivative(wanting) - temporal_derivative(liking)`

**Target**: PASS/FAIL — wanting must ramp before liking peaks.

**Evidence**: Salimpoor 2011: Caudate DA release (anticipation) temporally
precedes NAcc DA release (pleasure). If δ9 is positive during the buildup
phase and negative at the peak, the temporal dissociation is correct.

#### δ10: appraisal_lags_pleasure [-1, 1]

**Formula**: `pleasure - appraisal`

**Target**: PASS/FAIL — appraisal must lag behind pleasure by 0.5-2s.

**Evidence**: Huron 2006 ITPRA model: Appraisal is the slowest response,
occurring 0.5-2s after the event. During a peak, pleasure should be high
while appraisal is still rising (δ10 > 0 during peak, δ10 ≈ 0 after 2s).

#### δ11: chill_test_phase [0, 1]

**Formula**: State machine encoding of the complete Chill Test timeline:

```
0.00 = Baseline (no musical event approaching)
0.15 = Perception (R³ features changing, -30s)
0.30 = Prediction (da_caudate ramping, -15s)
0.45 = Anticipation (wanting + tension peaking, -5s)
0.60 = Event (da_nacc + liking spiking, 0s)
0.75 = Peak (peak_detection firing, +0.2s)
0.85 = Appraisal (conscious evaluation rising, +1s)
1.00 = Reset (system re-baselining, +5-10s)
```

**Target**: When run on music with known chill moments, δ11 should trace
this exact trajectory. The most comprehensive single-dimension validation
of the entire SRP pipeline.

---

## 8. Cross-Level Mapping Matrix

Which SRP dimensions feed which L³ groups?

### SRP → L³ Input Matrix

| SRP Dimension | α (Comp) | β (Neuro) | γ (Psych) | δ (Valid) |
|--------------|----------|-----------|-----------|-----------|
| N0 da_caudate | α0,α2 | β0,β8,β11 | γ0,γ2 | δ4,δ9 |
| N1 da_nacc | α0,α1 | β1,β9,β10,β11 | γ0,γ1 | δ5,δ9 |
| N2 opioid_proxy | α3 | β1 | γ1,γ5 | δ10 |
| C0 vta_drive | α0 | β2,β11 | γ6 | — |
| C1 stg_nacc_coupling | α0 | β3 | γ5,γ6 | δ6 |
| C2 prediction_error | α5 | β7,β9,β10,β12 | γ4,γ8 | δ0,δ2 |
| P0 wanting | α2 | β0 | γ0,γ2,γ6,γ7 | δ1,δ9 |
| P1 liking | α1 | β1 | γ0 | δ1,δ9 |
| P2 pleasure | α1 | β11 | γ2,γ5,γ7,γ8 | δ7,δ10 |
| T0 tension | α0,α1 | β6,β12,β13 | γ4,γ8,γ9,γ12 | δ0,δ1,δ2 |
| T1 prediction_match | α5 | β5,β7 | γ3,γ4 | — |
| T2 reaction | α0,α1 | β4,β6,β7,β13 | γ4,γ9 | δ0,δ2 |
| T3 appraisal | α0 | β5 | γ5 | δ10 |
| M0 harmonic_tension | α3 | β3 | γ8 | — |
| M1 dynamic_intensity | α3 | β3,β4,β6,β13 | γ9 | δ1 |
| M2 peak_detection | α1 | β1 | γ10,γ11 | δ0,δ3,δ8,δ11 |
| F0 reward_forecast | α2 | β0,β5 | γ2,γ3 | — |
| F1 chills_proximity | α1 | β1,β6,β13 | γ10,γ11 | δ0,δ3,δ11 |
| F2 resolution_expect | α2 | β5 | γ12 | — |

### Most Connected SRP Dimensions

| SRP Dim | L³ Connections | Role |
|---------|---------------|------|
| T0 tension | 12 | Most broadly interpreted — touches all groups |
| P2 pleasure | 10 | Core output — most validation targets |
| N0 da_caudate | 10 | Key anticipatory signal |
| T2 reaction | 10 | High-salience events |
| N1 da_nacc | 9 | Key consummatory signal |
| F1 chills_proximity | 8 | Drives chill-related L³ dims |

### Least Connected SRP Dimensions

| SRP Dim | L³ Connections | Note |
|---------|---------------|------|
| C0 vta_drive | 3 | Simple aggregate, few unique interpretations |
| F2 resolution_expect | 3 | Narrow scope |
| M0 harmonic_tension | 3 | Musical feature, few cross-level mappings |

---

## 9. Dimension Count Summary

```
┌──────────────────────────────────────────────────────────────┐
│                  SRP SEMANTIC FOOTPRINT                        │
│                                                                │
│  LEVEL 1 — Computation (SRP output)                           │
│    N: da_caudate, da_nacc, opioid_proxy            3D         │
│    C: vta_drive, stg_nacc_coupling, prediction_err 3D         │
│    P: wanting, liking, pleasure                    3D         │
│    T: tension, pred_match, reaction, appraisal     4D         │
│    M: harmonic_tension, dynamic_intensity, peak    3D         │
│    F: reward_forecast, chills_prox, resol_expect   3D         │
│                                            ─────────          │
│                                 SRP Total: 19D                │
│                                                                │
│  L³ — INTERPRETATION                                          │
│                                                                │
│    Group α — Computation Semantics                             │
│      α0-α3: mechanism attribution               4D            │
│      α4: computation certainty                   1D            │
│      α5: bipolar activation                      1D            │
│                                            ─────────          │
│                                  α Total:  6D                 │
│                                                                │
│    Group β — Neuroscience Semantics                            │
│      β0-β7: brain region activations             8D            │
│      β8-β10: neurotransmitter dynamics           3D            │
│      β11-β13: circuit states                     3D            │
│                                            ─────────          │
│                                  β Total: 14D                 │
│                                                                │
│    Group γ — Psychology Semantics                              │
│      γ0-γ2: reward decomposition                 3D            │
│      γ3-γ4: ITPRA dynamics                       2D            │
│      γ5-γ7: aesthetic experience                 3D            │
│      γ8-γ9: emotional state                      2D            │
│      γ10-γ12: chills/frisson                     3D            │
│                                            ─────────          │
│                                  γ Total: 13D                 │
│                                                                │
│    Group δ — Validation Semantics                              │
│      δ0-δ3: physiological predictions            4D            │
│      δ4-δ6: neural correlate predictions         3D            │
│      δ7-δ8: behavioral predictions               2D            │
│      δ9-δ11: temporal constraint validation      3D            │
│                                            ─────────          │
│                                  δ Total: 12D                 │
│                                                                │
│                                            ═════════          │
│                                  L³ Total: 45D                │
│                                                                │
│  ═══════════════════════════════════════════════════           │
│  COMPLETE SRP SEMANTIC FOOTPRINT: 19D + 45D = 64D (2^6)      │
│  ═══════════════════════════════════════════════════           │
└──────────────────────────────────────────────────────────────┘
```

### Comparison with D0

| | D0 Ψ⁰ | MI L³ (SRP only) |
|---|---|---|
| Computation dimensions | 8,192D | 19D |
| Interpretation dimensions | 2,560D | 45D |
| Ratio (interp/comp) | 0.31:1 | 2.37:1 |
| Total | 10,752D | 64D |

MI inverts the ratio: where D0 had far more computation than interpretation,
MI has **more interpretation than computation**. This reflects the
white-box philosophy — understanding matters more than dimensionality.

### Growth Projection

Each new model added to MI will bring its own L³ dimensions:

| Model | Computation | L³ | Total | Status |
|-------|-------------|-----|-------|--------|
| **SRP** (current) | 19D | 45D | 64D | ✓ Complete |
| **AAC** (Autonomic-Affective) | 14D | 26D | 40D | ✓ Complete |
| → SRP + AAC combined | 33D | 71D | **104D** | — |
| VMM (Value-Memory) | ~12D | ~25D | ~37D | Future |
| → ARU unit complete | ~45D | ~96D* | ~141D | Future |
| BCH (Beat-Consonance) | ~20D | ~40D | ~60D | Future |

*Shared L³ dimensions between SRP, AAC, VMM reduce the total.

---

## 10. Implementation Notes

### Compute Order

L³ dimensions are computed AFTER SRP, in this order:

```
SRP 19D (Level 1)
  │
  ├──► Group α (6D) — needs SRP outputs only
  ├──► Group β (14D) — needs SRP outputs + some α
  ├──► Group γ (13D) — needs SRP outputs + some β
  └──► Group δ (12D) — needs SRP + α + β + γ
```

Groups α, β, γ can be computed in parallel (no inter-group dependencies).
Group δ depends on γ10 (chill_probability) and γ11 (chill_phase) for δ11.

### State Requirements

Most L³ dimensions are stateless (computed per frame from SRP outputs).
Exceptions:

| Dimension | State Required | Reason |
|-----------|---------------|--------|
| β8 da_tonic | Low-pass filter buffer (~86 frames) | Smoothing over 500ms |
| γ11 chill_phase | State machine (current phase + timer) | Phase transitions |
| δ9 wanting_leads_liking | Temporal derivative buffer (~2 frames) | First derivative |
| δ10 appraisal_lags | None (direct difference) | — |
| δ11 chill_test_phase | State machine (7 phases + transition rules) | Full timeline |

### File Structure

```
mi/
├── language/
│   ├── srp/
│   │   ├── __init__.py    ← SRPSemantics orchestrator: SRP → 45D
│   │   ├── alpha.py       ← Group α: computation semantics (6D)
│   │   ├── beta.py        ← Group β: neuroscience semantics (14D)
│   │   ├── gamma.py       ← Group γ: psychology semantics (13D)
│   │   └── delta.py       ← Group δ: validation semantics (12D)
│   └── aac/
│       ├── __init__.py    ← AACSemantics orchestrator: AAC → 26D
│       └── alpha.py       ← Group α: computation semantics (6D)
```

---

## 11. SRP-AAC Cascade: What They Say Together

SRP and AAC are NOT independent output spaces. They are two measurement
facets of one neural cascade:

```
prediction error -> DA release (VTA) -> { SRP: reward psychology
                                        { AAC: ANS physiology
```

### Combined L³ Semantic Footprint

```
SRP:    19D computation +  45D interpretation =   64D
AAC:    14D computation +  26D interpretation =   40D
                                                -----
Combined MI output:                             104D
```

### How to Read Them Together

| Event | SRP reports | AAC reports |
|-------|------------|-------------|
| Surprise (unexpected chord) | prediction_error spikes | SCR rises, HR brief accel |
| Anticipation (building tension) | wanting rises, tension climbs | SCR climbing, driving_signal up |
| Peak pleasure | pleasure max, liking peak | CI max, SCR peak + HR minimum |
| Resolution | tension resolves, PE calms | SCR decays, HR recovers |
| Chills | chills_proximity high | CI > 0.6, piloerection predicted |

### Key Validation Target: Convergence

SRP pleasure and AAC chills_intensity should correlate temporally. If they
diverge persistently, the cascade model is wrong. First validation on Swan
Lake shows strong temporal correlation — see [L³-AAC-SEMANTIC-SPACE.md](L³-AAC-SEMANTIC-SPACE.md)
Section 9 for empirical results.

---

*Previous: [04-SRP-DATA-FLOW.md](../General/04-SRP-DATA-FLOW.md) — Pipeline trace*
*Related: [L³-AAC-SEMANTIC-SPACE.md](L³-AAC-SEMANTIC-SPACE.md) — AAC semantic space (sibling)*
*Related: [01-GLOSSARY.md](../General/01-GLOSSARY.md) — Terminology*
*Related: [05-SCIENTIFIC-BASIS.md](../General/05-SCIENTIFIC-BASIS.md) — Research foundation*
