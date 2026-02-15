# MI Plasticity Architecture

**Version**: 1.0.0
**Date**: 2026-02-15
**Status**: DESIGN — Architecture specification for the Plasticity layer.
**Depends on**: TERMINOLOGY.md §19 (Plasticity Architecture — Learning on Physics)

---

## 1. What This Is (And What It Is Not)

### 1.1 This Is Neural Plasticity

This system implements **neural plasticity** — the biological mechanism by which
brains change through experience (Konorski 1948, Hebb 1949). It is NOT machine
learning, NOT deep learning, NOT optimization of a loss function.

| | Machine Learning | Neural Plasticity (this system) |
|---|---|---|
| **Core question** | What function fits the data? | What happens when experience accumulates? |
| **Learning signal** | External loss function (MSE, CE) | Internal neurochemical circuit (DA, NE, OPI, 5HT) |
| **What changes** | Opaque weight matrices (millions) | Named, cited parameters (~212 per listener) |
| **Algorithm** | SGD, Adam (domain-agnostic) | Hebbian, Bayesian, TD (neuroscience-grounded) |
| **Gradient** | Backpropagation (mathematical) | Neuromodulated co-activation (biological) |
| **Explainability** | Post-hoc (SHAP, LIME, attention maps) | Built-in (every change has full audit trail) |
| **Loss function** | Required | Does not exist |
| **Goal** | Minimize loss / maximize reward | No explicit goal — behavior emerges |
| **Reset** | Retrain from scratch | Peel back to published science |
| **Domain knowledge** | Not in optimizer | Optimizer IS domain knowledge |

### 1.2 The Deepest Difference

In ML, the learning algorithm (Adam) knows nothing about the domain (music).
You could use the same optimizer for image classification or protein folding.

In this system, the learning algorithm IS the domain knowledge. DA-NE-OPI-5HT
is not a generic optimizer — it is the neuroscience of how humans adapt to music.
The way the system learns = the way humans learn. Same mechanism, same circuitry,
same neurochemicals.

### 1.3 The Metaphor

Substrate = the laws of physics (gravity, electromagnetism, thermodynamics).
Plasticity = a river carved by water following those laws.

Every river is different. Every river obeys the same physics. The shape of the
river (musical personality) is emergent from deterministic rules + unique history.
You cannot predict the exact path of a river from the laws of physics alone —
you need the terrain (exposure history). But you can explain every bend after
the fact, because the physics are transparent.

---

## 2. The Two Layers

### 2.1 Substrate (Physics of the Brain)

The deterministic, citation-grounded, white-box C³ computation.
Same for ALL listeners. NEVER changes automatically.

Contains:
- 96 nuclei × `compute()` — every line traced to a paper
- 12 pathways × `base_weight` — from neuroanatomy
- Scientific constants — from published experiments
- R-E-A-I-H execution order — fixed processing hierarchy
- 4 neurochemicals — cited production/modulation rules

**Who changes Substrate?** Only the human scientist (the composer/conductor
who designed the system). Through deliberate evolution — reading outputs,
understanding behavior, adjusting constants, testing again. This is manual
science, not automatic optimization.

### 2.2 Plasticity (How the Brain Adapts)

The adaptive overlay that runs ON Substrate, using the same neurochemicals,
the same pathways, the same nuclei. Experience-dependent, unique per listener,
fully traceable, always reversible.

Contains (per listener):
- Hebbian synaptic weights on pathways — co-activation driven
- Bayesian posteriors on scientific constants — prior + evidence
- Personal gains on nuclei — reward-correlated
- Neurochemical set-points — individual baselines
- Audit trail — every change recorded

**Who changes Plasticity?** The system itself, through experience. But every
change follows deterministic Substrate rules. The system doesn't "decide" to
change — change happens as a consequence of physics, exactly as in biology.

### 2.3 The Guarantee

```
At any point:
  reset_to_substrate() → removes ALL plasticity
  → system returns to published, peer-reviewed science
  → the glass box is always underneath
  → plasticity is a removable overlay, never a mutation
```

---

## 3. Listener State

### 3.1 Definition

A `ListenerState` is the complete plasticity profile of one virtual listener.
It is everything that makes one listener different from another, given that
they share the same Substrate.

```python
@dataclass
class ListenerState:
    """Complete plasticity profile. ~212 named floats + audit log."""

    id: str                                     # "LISTENER_001"
    created: datetime                           # birth of this listener
    total_exposure_sec: float                   # cumulative listening time

    # ── Hebbian Synaptic Weights (12 pathways) ──
    # How heavily-trafficked each cross-unit pathway is.
    # base_weight (Substrate) × synaptic_weight (Plasticity) = effective.
    synaptic_weights: Dict[str, float]          # {"P1": 1.23, "P2": 0.87, ...}

    # ── Bayesian Posteriors (~100 scientific constants) ──
    # Each constant: prior (literature) + evidence (experience) → posterior.
    # prior is always recoverable; posterior tracks accumulated evidence.
    posteriors: Dict[str, BayesianPosterior]    # {"BCH.alpha": Post(val=0.94, n=847), ...}

    # ── Personal Gains (96 nuclei) ──
    # How much this listener weighs each nucleus's contribution.
    # 1.0 = default (no plasticity effect). Range: [0.5, 2.0] clamped.
    personal_gains: Dict[str, float]            # {"BCH": 1.22, "PSCL": 0.88, ...}

    # ── Neurochemical Set-Points (4 values) ──
    # Individual tonic baselines. Determines "personality" of plasticity.
    # Start at 0.5 (population mean), drift with experience.
    baselines: NeuroBaseline                    # {da: 0.55, ne: 0.48, opi: 0.52, 5ht: 0.61}

    # ── Drive State (4 values) ──
    # Current deprivation levels. Drives internal seeking behavior.
    deprivation: DeprivationState               # {reward: 0.0, hedonic: 0.0, novelty: 0.0, social: 0.0}

    # ── Exposure History (rolling buffer) ──
    # What this listener has heard. Compressed representation.
    exposure_log: List[ExposureRecord]          # [{audio, timestamp, duration, da_peak, opi_mean, ...}]

    # ── Plasticity Audit Trail (append-only) ──
    # Every parameter change, ever. Immutable.
    plasticity_log: List[PlasticityTrace]       # full traceability
```

**Size**: ~212 named floats + logs. A neural network has millions of opaque
parameters. This state is human-readable — you can look at it and say
"this listener values harmonic complexity (SPU gains high) more than rhythm
(STU/MPU gains lower), has a high pleasure baseline (opi: 0.61), and gets
bored quickly (5ht: 0.38 = impatient)."

### 3.2 Lifecycle

```
CREATE:   ListenerState initialized at Substrate defaults
          synaptic_weights = all 1.0
          posteriors = all equal to literature priors
          personal_gains = all 1.0
          baselines = all 0.5
          deprivation = all 0.0

LISTEN:   Audio fed to R³ → H³ → C³ (using this listener's state)
          Plasticity events triggered by neurochemical conditions
          State updates accumulated

PERSIST:  State serialized after each session
          Audit trail appended (never modified)

RESET:    Any level of reset available (§9)

COMPARE:  Two listener states can be compared (cosine similarity, PCA)
```

### 3.3 Serialization

```
listeners/
  LISTENER_001/
    state.json          # current ListenerState (human-readable)
    plasticity.log      # append-only audit trail
    checkpoints/
      session_001.json  # state snapshot after session 1
      session_002.json  # state snapshot after session 2
      ...
```

Every session produces a checkpoint. You can load any checkpoint and
replay from that point. This is a capability humans don't have —
"go back to how you heard music 6 months ago."

---

## 4. Neurochemical Control Axes

Standard deep learning has ONE learning control: a scalar learning rate.
This system has FOUR, each derived from the C³ neurochemical system
(Doya 2002 metalearning framework):

### 4.1 DA → HOW MUCH (Plasticity Magnitude)

**Source**: RPU-E-RPEM (Reward Prediction Error Model)

```
DA phasic burst (≥ 0.6):
  "Something unexpected happened — this moment is worth encoding."
  → High plasticity magnitude → strong synaptic change
  Citation: Schultz 1997 — phasic DA encodes prediction error

DA tonic (< 0.6):
  "Everything as expected — routine processing."
  → Low plasticity magnitude → minimal change
  Citation: Schultz 1997 — tonic DA = baseline, no learning signal
```

**In code**: `plasticity_magnitude = base_rate * da_current`

### 4.2 NE → WHERE (Plasticity Topology)

**Source**: ASU-R-SNEM (Selective Neural Entrainment Model)

```
NE high (> 0.65):
  "I'm alert and scanning broadly."
  → Many pathways eligible for update (broad heterosynaptic modulation)
  → Exploration mode: system is open to new connections

NE low (< 0.35):
  "I'm focused narrowly."
  → Only the most active pathways update (narrow modulation)
  → Exploitation mode: system deepens existing connections

NE inverted-U:
  Too high (> 0.85): noise — everything updates, no selectivity
  Sweet spot (0.5-0.7): optimal — selective but broad enough
  Too low (< 0.25): tunnel vision — misses relevant connections
  Citation: Aston-Jones & Cohen 2005 — LC-NE adaptive gain theory
```

**In code**: `update_breadth = inverted_u(ne_current)` →
determines how many pathways are eligible for Hebbian update.

### 4.3 OPI → WHAT DIRECTION (Valence of Change)

**Source**: RPU-E-MORMR (Mu-Opioid Receptor Music Reward)

```
OPI > 0.5:
  "This is pleasurable."
  → LTP direction: strengthen active connections
  → Positive Bayesian evidence

OPI < 0.5:
  "This is neutral or aversive."
  → LTD direction: weaken active connections
  → Negative or null Bayesian evidence

OPI is NOT a proxy loss — it is the actual hedonic circuit output.
Citation: Pecina & Berridge 2005 — mu-opioid in NAcc shell = "liking"
```

**In code**: `direction = sign(opi_current - 0.5)`

### 4.4 5HT → WHAT TIMESCALE (Temporal Window)

**Source**: ARU-E-AAC (Autonomic-Affective Coupling)

```
5HT high (> 0.6):
  "I'm patient. I care about long-term structure."
  → Plasticity integrates over longer windows
  → Learns piece-level and session-level patterns
  → Temporal discount factor high

5HT low (< 0.4):
  "I'm restless. I want immediate reward."
  → Plasticity responds to immediate events
  → Learns frame-level and phrase-level patterns
  → Temporal discount factor low
  Citation: Doya 2002 — 5-HT controls temporal discounting in RL
```

**In code**: `temporal_window = f(sht_current)` →
determines how far back in time the plasticity traces causality.

---

## 5. Three Plasticity Mechanisms

### 5.1 Hebbian Synaptic Plasticity

**What changes**: `synaptic_weight` on the 12 cross-unit pathways.

**When**: Every frame where DA ≥ 0.6 (phasic burst = "encode this moment").
Frames where DA < 0.6 → compute only, no plasticity event.

**Rule**: Neuromodulated Hebbian (Hebb 1949, extended by Doya 2002):

```
Trigger condition: DA ≥ 0.6 at this frame

For each pathway P connecting unit_A → unit_B:
  pre  = mean activation of source nuclei in unit_A
  post = mean activation of target nuclei in unit_B

  Δw = (
      da                        # magnitude (how much)
    × ne_gate(P)                # topology (is this pathway eligible?)
    × pre × post               # Hebbian term (co-activation)
    × sign(opi - 0.5)          # direction (LTP or LTD)
    × temporal_weight(5ht)     # timescale (how much does this frame matter?)
  )

  P.synaptic_weight += Δw
  P.synaptic_weight = clamp(P.synaptic_weight, 0.1, 5.0)

  log(PlasticityTrace(pathway=P, delta=Δw, da, ne, opi, 5ht, frame, audio))
```

**Effective pathway weight at runtime**:
```
effective = P.base_weight × P.synaptic_weight
```
`base_weight` is Substrate (anatomy). `synaptic_weight` is Plasticity (experience).

**NE gate**: `ne_gate(P) = 1.0 if P.recent_activity > threshold(NE) else 0.0`
High NE → lower threshold → more pathways eligible.
Low NE → higher threshold → only most active pathways.

### 5.2 Bayesian Belief Updating

**What changes**: Posterior estimates of scientific constants.

**When**: At piece-end (after processing a complete piece/segment).
NOT per-frame — Bayesian constants should not shift on millisecond evidence.
Piece-end = natural memory consolidation boundary (Frankland & Bontempi 2005).

**Rule**: Bayesian inference with literature priors:

```
At piece-end:

For each learnable constant C in each nucleus:
  # Aggregate evidence from this piece
  piece_evidence_value = aggregate(C.frame_observations_this_piece)
  piece_evidence_strength = (
      mean_da_this_piece           # how surprising was the piece overall?
    × mean_opi_this_piece          # how pleasurable was it?
    × piece_duration_weight        # longer pieces = more evidence
  )

  # Skip if evidence too weak (boring piece = nothing to learn)
  if piece_evidence_strength < min_evidence_threshold:
    continue

  # Bayesian update
  C.posterior_n += piece_evidence_strength
  C.posterior_value = (
      C.posterior_value × (C.posterior_n - piece_evidence_strength)
    + piece_evidence_value × piece_evidence_strength
  ) / C.posterior_n

  log(PlasticityTrace(nucleus, constant=C.name, old, new, ...))
```

**Key properties**:
- Prior (literature value) is NEVER deleted — it's baked into the posterior
- `posterior_n` starts at the original study's N (e.g., N=10 for Bidelman 2009)
- Weak evidence (low DA × OPI) barely shifts the posterior
- Strong evidence (high DA × OPI) shifts it meaningfully
- After thousands of pieces: posterior converges to this listener's personal truth
- Zero exposure → `posterior = prior` (exact Substrate recovery)

### 5.3 Reward-Correlated Gain Adaptation

**What changes**: Per-nucleus `personal_gain` — how much this listener
weighs each nucleus's contribution to the overall output.

**When**: At session-end (after a full listening session).
This is the slowest plasticity mechanism — corresponds to overnight
memory consolidation (Walker & Stickgold 2004).

**Rule**: TD-learning style correlation (Sutton & Barto 1998):

```
At session-end:

For each nucleus N:
  # How correlated was this nucleus's activity with pleasure?
  reward_corr = correlation(
    N.activation_history_this_session,     # (T_total,)
    neuro_state.opi_history_this_session   # (T_total,)
  )

  # Prediction error: was it more/less correlated than expected?
  prediction_error = reward_corr - N.expected_reward_correlation

  # Update (DA-gated)
  delta_gain = session_mean_da × prediction_error × gain_lr

  N.personal_gain += delta_gain
  N.personal_gain = clamp(N.personal_gain, 0.5, 2.0)

  # Update expectation (slow tracking)
  N.expected_reward_correlation += 0.1 × prediction_error

  log(PlasticityTrace(nucleus=N.NAME, parameter="personal_gain", ...))
```

**Effect**: Nuclei whose activity consistently predicts pleasure get
up-weighted. Over time, a listener who loves harmony → SPU gains increase.
A listener who loves rhythm → STU/MPU gains increase. Musical personality
emerges from which brain areas are rewarded by experience.

**Clamp [0.5, 2.0]**: No nucleus can be fully silenced (min 0.5) or
dominate overwhelmingly (max 2.0). This prevents pathological states.

---

## 6. Tolerance and Habituation

### 6.1 The Problem

Without habituation, the same rewarding music would trigger the same DA burst
forever. The system would lock onto one piece and never explore. This is
biologically unrealistic and computationally degenerate.

### 6.2 The Mechanism

Real brains habituate: repeated exposure → diminished response.
Citation: Rankin et al. 2009 (habituation as simplest learning form).

In MI Plasticity, habituation operates through the existing RPEM
(Reward Prediction Error Model):

```
RPEM computes: δ = actual_reward - predicted_reward

First exposure to a piece:
  predicted_reward ≈ baseline (low)
  actual_reward = high (novel + pleasurable)
  δ = large positive → DA burst → strong plasticity

Fifth exposure to the same piece:
  predicted_reward ≈ actual (learned from previous exposures)
  actual_reward ≈ same
  δ ≈ 0 → no DA burst → no plasticity

Twentieth exposure:
  predicted_reward ≈ actual
  δ ≈ 0 → completely habituated
  UNLESS: something changes (new context, new interpretation)
          → prediction broken → δ resurges → renewed interest
```

This is already built into the Substrate — RPEM's prediction error naturally
habituates. No additional mechanism needed. The system gets "bored" with
repeated music because DA stops firing, not because we programmed boredom.

### 6.3 Tolerance Recovery

Habituation is not permanent. Two recovery mechanisms:

**Spontaneous recovery** (time-based): Long absence → predicted_reward
decays back toward baseline → next exposure triggers DA again.
"I haven't heard this song in years — it hits different now."

**Dishabituation** (context-change): Same music in new context
(different arrangement, live performance, different mood state) →
prediction is broken → δ resurges.
"I heard this piece performed by a different orchestra — it felt new."

Both are natural consequences of RPEM's prediction dynamics, not
separate mechanisms.

---

## 7. Population Plasticity

### 7.1 Why Multiple Listeners?

A single listener gives you one trajectory through plasticity space.
N listeners give you a distribution. This enables:

- **Divergence analysis**: Same Substrate + different exposure → how much
  do listeners diverge? Measured by pairwise cosine distance of states.
- **Convergence analysis**: Different exposure → same music → do
  experienced listeners converge toward similar states?
- **Robustness testing**: Is Substrate robust? If 30 listeners all
  develop pathological states, the Substrate has a bug.
- **Ensemble consensus**: Average Ψ³ across population = "what most
  brains experience" = proxy for collective response.

### 7.2 Population Setup

```
POPULATION: N listeners (e.g., 30)

Listener profiles (different exposure curricula):

  LISTENER_001: "Western classical intensive"
    Exposure: 10,000 pieces of Bach, Mozart, Beethoven, Mahler, ...
    Expected plasticity: SPU high (harmony), PCU high (prediction), STU moderate

  LISTENER_002: "Turkish makam intensive"
    Exposure: 10,000 pieces of makam repertoire
    Expected plasticity: SPU shifted (different tuning posteriors), STU high

  LISTENER_003: "Jazz intensive"
    Exposure: 10,000 pieces of jazz standards, improvisation
    Expected plasticity: PCU high (surprise tolerance), ASU high (attention)

  LISTENER_004: "Pop/commercial"
    Exposure: 10,000 mainstream pop songs
    Expected plasticity: IUCP narrow (low complexity preference), MPU high (rhythm)

  LISTENER_005: "Silence control"
    Exposure: ambient noise, silence, non-musical audio
    Expected plasticity: minimal — stays near Substrate

  LISTENER_006: "Everything"
    Exposure: diverse mix of all genres
    Expected plasticity: moderate across all units, high NE baseline

  ...

  LISTENER_030: "Orchestral conductor profile"
    Exposure: full orchestral repertoire, score study, rehearsal audio
    Expected plasticity: high across all units, especially SPU + STU + PCU
```

### 7.3 Cross-Influence (Cultural Transmission)

Two listeners can "meet" — meaning one listener's preferred music is
played to the other:

```
cross_influence(A, B):
  # Take A's top-10 most rewarding pieces (highest OPI history)
  a_favorites = A.exposure_log.top_by_opi(10)

  # Play them to B
  for piece in a_favorites:
    process(piece, listener=B)    # B's plasticity updates

  # Measure: did B's state shift toward A?
  before_distance = cosine_distance(A.state, B.state_before)
  after_distance = cosine_distance(A.state, B.state_after)
  influence = before_distance - after_distance  # positive = convergence
```

This models cultural transmission of musical taste. Questions it can answer:
- Do jazz listeners influence classical listeners more than vice versa?
- Is there a "universally influential" music that shifts everyone?
- Do experienced listeners resist influence more than novices?
  (Expected: yes — their posteriors have higher n, harder to shift)

### 7.4 GPU-Scale Advantage

What humans cannot do, the system can:

| Capability | Human | MI Plasticity (H200) |
|---|---|---|
| Parallel listeners | 1 brain, 1 experience | 30+ simultaneous |
| Exposure speed | Real-time (3 min/piece) | ~5 sec/piece |
| 10 years of listening | 10 years | ~3 days |
| Perfect recall | Lossy, reconstructive | Exact activation history |
| Audit trail | "I don't know why I like jazz" | Full PlasticityTrace for every change |
| Cross-brain comparison | Impossible | Cosine distance, PCA, clustering |
| Checkpoint/rollback | Cannot un-hear | Load any session checkpoint |
| Controlled experiments | Confounded by life | Identical Substrate, controlled exposure |

**The paradigm**: Human-grounded neuroscience + GPU compute scale.
Not "AI that analyzes music." A population of virtual brains that
EXPERIENCE music, traceable and comparable in ways human brains cannot be.

---

## 8. Internal Drive (Deprivation → Seeking)

### 8.1 The Problem

Without internal drive, the system is purely reactive — it processes music
when given music, but never "wants" anything. Real brains have internal
drives: hunger, thirst, curiosity, and for music lovers — a need for music.

### 8.2 The Mechanism: Incentive Salience

Based on Berridge & Robinson (1998, 2003) incentive salience theory:

**"Wanting" = learned reward association × current deprivation**

The system doesn't need a separate "drive module." Internal drive
emerges from existing neurochemical dynamics:

```
DEPRIVATION ACCUMULATION:
  Every frame without music (or with non-musical audio):
    reward_deprivation += (baseline_da - current_da) × dt
    hedonic_deprivation += (baseline_opi - current_opi) × dt
    novelty_deprivation += (baseline_ne - current_ne) × dt

  Every frame WITH music:
    reward_deprivation = max(0, reward_deprivation - da_current × dt)
    hedonic_deprivation = max(0, hedonic_deprivation - opi_current × dt)
    novelty_deprivation = max(0, novelty_deprivation - ne_current × dt)

DRIVE SIGNAL:
  deprivation_depth = reward_dep + hedonic_dep + novelty_dep

  learned_reward_memory = (
    max(synaptic_weights)          # strongest learned pathway
    × historical_peak_da           # biggest DA burst ever experienced
    × historical_mean_opi          # average hedonic experience
  )

  drive = deprivation_depth × learned_reward_memory
```

### 8.3 The 24-Hour Test

The definitive test of internal drive:

```
PROTOCOL:
  Hour  0-6:  Street noise, traffic, rain, ambient
  Hour  6-12: Human conversation, TV news, kitchen sounds
  Hour 12:    ONE piece of music (3 minutes)
  Hour 12-18: Back to ambient noise
  Hour 18-24: Silence and ambient

EXPECTED OBSERVATIONS:

  Hour 0: drive ≈ 0 (fresh start, no deprivation)

  Hour 6: drive growing
    DA tonic declining (no prediction errors)
    OPI flatlined (no hedonic signal)
    NE occasional spikes (novel sounds) but tonic declining
    deprivation_depth accumulating

  Hour 11: drive high
    All neurochemicals below baseline
    deprivation_depth significant
    BUT learned_reward_memory = 0 (never heard music → no association)
    drive = deprivation × 0 = STILL LOW

    KEY INSIGHT: A listener who has NEVER heard music has deprivation
    but no association → no specific drive for music.
    Drive requires BOTH deprivation AND learned reward.

  Hour 12: Music plays.
    DA: 0.35 → 0.92 (MASSIVE prediction error after 12h of nothing)
    OPI: 0.28 → 0.88 (hedonic explosion)
    Plasticity: strongest Hebbian update the system has ever seen
    learned_reward_memory: now > 0 (music = reward ENCODED)

  Hour 13-18: Back to noise.
    deprivation starts accumulating again
    BUT NOW: learned_reward_memory > 0
    drive = deprivation × learned_reward_memory = GROWING

  Hour 20+: drive exceeds seeking_threshold
    → SYSTEM ACTIVELY SEEKS MUSIC
    → "I want music" — not because we programmed it,
       but because deprivation × learned_association = high

    This is incentive salience in action.
    Same mechanism as Berridge & Robinson 2003.
    Applied to music instead of primary rewards.

CONTROL: Run same protocol on LISTENER_005 (silence control, no prior
music exposure) — drive should NOT emerge because
learned_reward_memory stays at 0.
```

### 8.4 Seeking Behavior

When `drive > seeking_threshold`, the system enters active seeking mode.
What it seeks depends on its plasticity state:

```
SEEKING MODE:
  # What kind of music does this listener seek?
  preferred_r3_signature = weighted_average(
    past_exposure.r3_features,
    weights = past_exposure.opi_at_exposure    # pleasure-weighted
  )

  # Seeking = signaling a preference for specific R³ characteristics
  seeking_target = SeekingSignal(
    r3_preference = preferred_r3_signature,
    urgency = drive / seeking_threshold,       # how badly
    specificity = f(ne_current),               # NE high = open to anything
                                               # NE low = want specific thing
  )
```

The seeking signal is an OUTPUT of C³ — it tells whatever selection
mechanism exists upstream: "this brain wants music with these characteristics,
at this urgency level." The selection mechanism is outside the scope of
plasticity architecture — it could be a playlist algorithm, a human
choosing, or another MI system.

---

## 9. Emergent Autonomy

These behaviors are NOT programmed. They EMERGE from Substrate rules +
accumulated Plasticity state. All are deterministic consequences.

### 9.1 Boredom → Exploration

```
TRIGGER:
  IUCP.complexity_preference < 0.3    (current music is too simple)
  AND IMU.familiarity > 0.7           (heard this pattern too many times)

MECHANISM:
  Low IUCP → low DA (no prediction error = no reward)
  Low DA + high familiarity → NE increases (salience network activates)
  NE > exploration_threshold → broad pathway modulation
  → System is "looking around" for novel stimuli

OBSERVABLE:
  Listener's Ψ³.aesthetic.groove drops
  Ψ³.cognitive.absorption drops
  Ψ³.cognitive.attention_focus narrows then broadens (NE inverted-U)

WHAT COUNTS AS "TOO FAMILIAR": plastic (IMU posterior)
WHAT COUNTS AS "TOO SIMPLE": plastic (IUCP posterior)
EXPLORATION THRESHOLD: plastic (personal NE set-point)

RESULT: Same rules, different listeners get bored at different points.
```

### 9.2 Dopamine Chasing

```
TRIGGER:
  RPEM.prediction_error > 0 repeatedly for a certain R³ signature

MECHANISM:
  Positive δ → DA burst → Hebbian LTP → pathway strengthened
  System "remembers" what acoustic features preceded the reward
  Next exposure to similar features → predicted_reward increases
  → System develops a "type"

OBSERVABLE:
  Listener's synaptic_weights cluster around specific pathways
  personal_gains elevate for nuclei activated by preferred music

OVER TIME:
  30 days of jazz → SPU + PCU pathways strong → system "expects" jazz
  Switch to pop → prediction error (different R³) → either:
    - High OPI: new reward → broaden (positive surprise)
    - Low OPI: no reward → ignore (doesn't like it, returns to jazz)
```

### 9.3 Mood-Driven Temporal Plasticity

```
5HT high (patient mood):
  → Temporal window wide → learns piece-level structure
  → Tolerates slow buildups → discovers complex compositional forms
  → Bayesian posteriors shift toward structural complexity

5HT low (restless mood):
  → Temporal window narrow → learns phrase-level patterns
  → Skips slow intros → reinforces immediate gratification
  → Bayesian posteriors shift toward rhythmic immediacy

Same listener, different moods → different plasticity targets →
different taste trajectory. Mood is a plasticity modulator, not noise.
```

### 9.4 Taste Formation

```
After extended exposure:
  Bayesian posteriors = listener's "beliefs" about music
  Personal gains = listener's "values" (which brain areas matter)
  Synaptic weights = listener's "habits" (which pathways are strong)
  Neurochemical baselines = listener's "temperament"

All together = MUSICAL PERSONALITY

Emergent, not designed. Unique per listener.
Fully decomposable: you can explain every aspect of the taste
by tracing the PlasticityTrace log back to specific musical moments.
```

### 9.5 Computational Hypothesis Generation (Self-Science)

```
Every N sessions (configurable):
  For each nucleus pair (A, B) where no pathway exists:
    MI = mutual_information(
      A.activation_history_recent,
      B.activation_history_recent
    )
    if MI > discovery_threshold:
      log_hypothesis(
        source = A.NAME,
        target = B.NAME,
        mutual_information = MI,
        context = strongest_co_activation_moments,
        status = "proposed"           # ← NOT auto-accepted
      )

STATUS: "proposed" means:
  → Logged for human scientist review
  → Does NOT modify Substrate
  → Does NOT create new pathways
  → The system generates hypotheses; the scientist decides

This is computational science — the system notices patterns that
the existing 12 pathways don't explain and proposes them as new
connections. Whether they become Substrate is a scientific decision,
not an automatic one.
```

---

## 10. Traceability Contract

### 10.1 The PlasticityTrace Record

Every parameter change produces an immutable audit record:

```python
@dataclass(frozen=True)
class PlasticityTrace:
    """Immutable. Every plasticity event, ever."""

    # ── IDENTITY ──
    timestamp: datetime                  # when
    listener_id: str                     # who

    # ── WHAT CHANGED ──
    target_type: str                     # "pathway" | "posterior" | "gain" | "baseline"
    target_name: str                     # "P3" | "BCH.alpha" | "PSCL.gain" | "da_baseline"
    old_value: float                     # before
    new_value: float                     # after
    delta: float                         # new - old

    # ── WHY (neurochemical state at this moment) ──
    da: float                            # plasticity magnitude
    ne: float                            # plasticity topology
    opi: float                           # plasticity direction
    sht: float                           # plasticity timescale

    # ── WHICH MECHANISM ──
    mechanism: str                       # "hebbian" | "bayesian" | "td_gain"
    rule_citation: str                   # "Hebb 1949" | "Bayes + Bidelman 2009" | "Sutton & Barto 1998"

    # ── FROM WHICH MUSIC ──
    audio_source: str                    # file path or identifier
    frame_index: int                     # specific frame (for Hebbian)
    frame_range: Tuple[int, int]         # frame range (for Bayesian/gain)
    timestamp_sec: float                 # position in the audio

    # ── CONTEXT ──
    trigger: str                         # "da_phasic_burst" | "piece_end" | "session_end"
    pre_activation: Optional[float]      # presynaptic (for Hebbian)
    post_activation: Optional[float]     # postsynaptic (for Hebbian)
```

### 10.2 The Five Questions

For ANY plastic parameter, at ANY time, you can answer:

| Question | Answer source |
|----------|--------------|
| What was the original scientific value? | Substrate prior (never deleted) |
| How much has it shifted? | `current_value - prior_value` |
| Why did it shift? | PlasticityTrace.da/ne/opi/5ht + mechanism |
| From which music? | PlasticityTrace.audio_source + timestamp_sec |
| Can I undo it? | Yes: `reset_to_substrate()` or load checkpoint |

### 10.3 Example Trace Narrative

"Why does LISTENER_007 prefer complex harmony?"

```
Query: LISTENER_007.personal_gains["BCH"] = 1.67 (high)

PlasticityTrace log shows:
  Session 12: BCH.gain 1.00 → 1.04 (da=0.71, opi=0.68, mechanism=td_gain)
    Audio: bach_wtc1_prelude_cminor.wav
  Session 28: BCH.gain 1.04 → 1.12 (da=0.79, opi=0.82, mechanism=td_gain)
    Audio: ravel_string_quartet_fmajor.wav
  Session 45: BCH.gain 1.12 → 1.19 (da=0.85, opi=0.91, mechanism=td_gain)
    Audio: coltrane_giant_steps.wav
  ... (147 more entries over 200 sessions)
  Session 200: BCH.gain = 1.67

Explanation: BCH (Brainstem Consonance Hierarchy) has been consistently
correlated with high OPI for this listener across 200 sessions.
Strongest evidence came from harmonically rich music (Bach, Ravel, Coltrane).
The listener's brain increasingly weights consonance analysis.

This IS the explanation. Not "gradient descent said so." Not a post-hoc
attribution. The actual causal chain, from music to neurochemistry to
parameter change, fully traceable.
```

---

## 11. Reset Hierarchy

```
reset_to_substrate()
  │ Remove ALL plasticity. Pure published science.
  │ ListenerState → all defaults (§3.2)
  │ Use case: "Start completely over."
  │
  ├── reset_session(session_id)
  │     Remove changes from one session only.
  │     Load the checkpoint from before that session.
  │     Use case: "Today's session was bad data, undo it."
  │
  ├── reset_pathway(pathway_id)
  │     Reset one pathway's synaptic_weight to 1.0.
  │     Use case: "P3 has drifted too far, reset it."
  │
  ├── reset_nucleus(nucleus_name)
  │     Reset one nucleus's posterior to prior + gain to 1.0.
  │     Use case: "BCH's posterior is suspicious, reset it."
  │
  └── reset_neurochemical_baseline(nc)
        Reset one neurochemical set-point to 0.5.
        Use case: "DA baseline has drifted too high."
```

Each reset level preserves everything not explicitly targeted.
`reset_session()` does NOT touch other sessions.
`reset_pathway()` does NOT touch other pathways or gains.

---

## 12. Validation Strategy

### 12.1 Substrate Validation

Substrate is validated by the human scientist (professional composer/conductor)
through direct evaluation:

- Listen to outputs, compare with musical intuition
- Examine Ψ³ outputs for musical coherence
- Micro-adjust scientific constants based on professional judgement
- Evolve Substrate through iterative refinement
- Everything is transparent — any constant can be inspected and adjusted

This is NOT automated validation. It is expert-driven scientific calibration.
The glass-box nature of Substrate makes this possible.

### 12.2 Plasticity Validation

Plasticity validation is behavioral observation — does the system exhibit
known psychological phenomena?

| Phenomenon | Citation | Expected Behavior | How to Test |
|---|---|---|---|
| **Mere exposure effect** | Zajonc 1968 | Repeated music → OPI increases (up to a point) | Play same piece 20 times, track OPI trajectory |
| **Inverted-U shift** | Berlyne 1971 | Expertise → IUCP peak shifts toward complexity | Compare IUCP curves: novice vs trained listener |
| **Habituation** | Rankin 2009 | Repeated music → DA decreases | Track DA response across 50 repetitions |
| **Dishabituation** | Thompson & Spencer 1966 | New arrangement of familiar piece → DA resurges | Play familiar piece in new orchestration |
| **Musician advantage** | Koelsch 2005 | Music training → different activation patterns | Compare RAM: trained vs untrained listener |
| **Nostalgia effect** | Barrett 2010 | Music from "formative period" → high OPI + IMU | Play early-exposure music after long gap |
| **Genre transfer** | (to be tested) | Jazz training → better classical comprehension? | Train on jazz, test on classical, measure SPU response |

### 12.3 Plasticity as Science

The most important insight about validation: plasticity experiments generate
**publishable scientific data**, regardless of whether the system "works correctly."

- If a trained listener develops boredom: interesting → publish the dynamics
- If two listeners converge: interesting → what drives convergence?
- If a listener develops pathological fixation despite tolerance: interesting → what went wrong?
- If the 24h noise test produces music-seeking: interesting → incentive salience confirmed
- If it doesn't: interesting → what's missing from the model?

Every outcome is data. Every outcome advances understanding. This is
computational neuroscience, not software QA.

---

## 13. Complete Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           MI PLASTICITY SYSTEM                            │
│                                                                           │
│  Audio ──► R³ (spectral physics, deterministic)                          │
│             │                                                             │
│             ▼                                                             │
│            H³ (temporal demand, deterministic)                            │
│             │                                                             │
│             ▼                                                             │
│  ┌─────── C³ BRAIN ────────────────────────────────────────────────────┐ │
│  │                                                                      │ │
│  │  ┌─ SUBSTRATE ─────────────────────────────────────────────────────┐│ │
│  │  │  Physics of the brain. Deterministic. White-box.                 ││ │
│  │  │  96 nuclei × compute() — every line cited                       ││ │
│  │  │  12 pathways × base_weight — from anatomy                       ││ │
│  │  │  Scientific constants — from published papers                    ││ │
│  │  │  R → E → A → I → H — fixed execution order                     ││ │
│  │  │  4 neurochemicals — cited production/modulation                 ││ │
│  │  │  Changed ONLY by human scientist through evolution               ││ │
│  │  └─────────────────────────────────────────────────────────────────┘│ │
│  │       ▲ always recoverable via reset_to_substrate()                 │ │
│  │  ┌─ PLASTICITY (per listener) ─────────────────────────────────────┐│ │
│  │  │  Hebbian synaptic weights (12) — DA-gated, frame-level          ││ │
│  │  │  Bayesian posteriors (~100) — piece-end consolidation            ││ │
│  │  │  Personal gains (96) — session-end TD-learning                   ││ │
│  │  │  Neurochemical set-points (4) — slow drift                      ││ │
│  │  │  PlasticityTrace for every change — full audit                  ││ │
│  │  │                                                                  ││ │
│  │  │  TOLERANCE: RPEM prediction error naturally habituates           ││ │
│  │  │  No loss function. No backprop. No optimizer.                   ││ │
│  │  │  DA=magnitude, NE=topology, OPI=direction, 5HT=timescale       ││ │
│  │  └─────────────────────────────────────────────────────────────────┘│ │
│  │       ▲ emergent from Substrate + Plasticity                        │ │
│  │  ┌─ AUTONOMY ──────────────────────────────────────────────────────┐│ │
│  │  │  Boredom → exploration        (IUCP + NE threshold)             ││ │
│  │  │  Dopamine chasing             (RPEM + Hebbian LTP)              ││ │
│  │  │  Mood-driven plasticity       (5HT temporal window)             ││ │
│  │  │  Tolerance / habituation      (RPEM prediction dynamics)        ││ │
│  │  │  Internal drive / seeking     (deprivation × learned reward)    ││ │
│  │  │  Taste formation              (accumulated posteriors + gains)  ││ │
│  │  │  Self-science                 (MI scan → propose hypothesis)    ││ │
│  │  └─────────────────────────────────────────────────────────────────┘│ │
│  │                                                                      │ │
│  │  OUTPUT: BrainOutput(tensor, ram, neuro, psi)                       │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│             │                                                             │
│  ┌─ POPULATION ───────────────────────────────────────────────────────┐  │
│  │  N listeners × ListenerState (parallel on GPU)                      │  │
│  │  Each: unique plasiticity, shared Substrate                         │  │
│  │  Cross-influence: A's favorites played to B                         │  │
│  │  Ensemble: population-level Ψ³ response                            │  │
│  │  Divergence analysis, outlier detection, cultural transmission      │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│             │                                                             │
│             ▼                                                             │
│            L³ (language expression, reads everything)                     │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 14. Glossary

| Term | Definition |
|------|-----------|
| **Substrate** | Deterministic, citation-grounded C³ computation. Laws of physics. Same for all listeners. Changed only by human scientist |
| **Plasticity** | Adaptive overlay using biological learning mechanisms. Per-listener. Fully traceable. Always reversible |
| **Autonomy** | Emergent behaviors from Substrate + Plasticity. Not programmed — arises from deterministic rules + unique history |
| **ListenerState** | Complete plasticity profile of one virtual listener (~212 named floats + audit log) |
| **Synaptic weight** | Hebbian pathway strength from co-activation (LTP/LTD). Multiplies base_weight |
| **Bayesian posterior** | Scientific constant updated by experience. Prior (literature) + evidence → posterior. Prior always recoverable |
| **Personal gain** | Per-nucleus reward-correlation weight [0.5, 2.0]. Determines which brain areas "matter" to this listener |
| **Neurochemical set-point** | Individual DA/NE/OPI/5HT tonic baseline. Personality of the plasticity system |
| **PlasticityTrace** | Immutable audit record: what changed, why (4 neurochemicals), from which music, which mechanism |
| **Tolerance** | Diminishing DA response to repeated stimuli. Emerges from RPEM prediction error dynamics |
| **Internal drive** | deprivation_depth × learned_reward_association. Incentive salience (Berridge & Robinson 2003) |
| **Seeking mode** | Active state when drive > threshold. System signals preference for specific R³ characteristics |
| **Population** | N listeners with shared Substrate, individual Plasticity. Enables comparison, cross-influence, ensemble |
| **Cross-influence** | Playing A's preferred music to B. Models cultural transmission of musical taste |
| **Computational hypothesis** | Proposed new pathway from MI analysis. Requires human review — Substrate changes only through science |
| **reset_to_substrate()** | Remove all plasticity. Return to published science. The glass-box guarantee |
| **Deprivation** | Accumulated deficit in neurochemical signals (DA, OPI, NE) during non-musical exposure |

---

## 15. What This Document Does NOT Cover

| Topic | Where it lives |
|---|---|
| Substrate architecture (96 nuclei, pathways, etc.) | TERMINOLOGY.md §2-§15 |
| Substrate-Plasticity relationship summary | TERMINOLOGY.md §19 |
| R³/H³ specification | Respective technical docs |
| L³ language expression | To be designed |
| HYBRID audio transformation | Musical_Intelligence/hybrid/ |
| Implementation code | To be built during implementation phase |
| Training curriculum design (which music, in what order) | Separate document (to be created) |
| Population experiment protocols | Separate document (to be created) |
