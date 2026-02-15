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

## 13. Bidirectional Cognition: Sound as the Language of Thought

### 13.1 The Insight

The MI pipeline is currently unidirectional:

```
PERCEPTION:  Audio → R³ → H³ → C³ → Ψ³
             "What does this sound do to a brain?"
```

But every layer in this pipeline has a well-defined input-output mapping.
If we can go forward, we can go backward:

```
EXPRESSION:  Ψ³ → C³ → H³ → R³ → Audio
             "What sound would a brain in this state produce?"
```

Together, they form a **bidirectional cognitive loop** where sound IS thought.
Not a metaphor. Not a lossy translation. The cognitive state and the sound
are two views of the same mathematical object — one in brain space, the other
in acoustic space, connected by a deterministic, invertible transformation.

### 13.2 Why This Is Not Synthesis

Traditional audio synthesis: "Generate audio with frequency X, amplitude Y."
This is parametric control over acoustic properties.

Traditional AI music generation: "Generate music that sounds like jazz."
This is statistical imitation of distributional patterns.

What we are proposing is neither. It is:

**"What would a brain in THIS cognitive-emotional state hear if it could
hear its own internal dynamics as sound?"**

The distinction matters:

| | Traditional Synthesis | AI Generation | MI Expression |
|---|---|---|---|
| **Input** | Acoustic parameters | Text prompt / style label | Cognitive state (Ψ³) |
| **Process** | Signal processing | Statistical sampling | Inverse neuroscience |
| **Output** | Sound with properties | Sound that resembles | Sound that IS the thought |
| **Grounding** | Physics (acoustics) | Corpus statistics | Neuroscience (cited) |
| **Meaning** | Assigned by listener | Implied by resemblance | Intrinsic (isomorphic) |
| **Invertible** | No (many signals → same percept) | No (latent → sample) | Yes (Ψ³ ↔ Audio deterministic) |

The last row is the key. In MI, the mapping between cognitive state and sound
is **deterministic and invertible** because every transformation (R³, H³, C³, Ψ³)
is a defined computation with cited constants. This is not a neural network's
black-box latent space — it is a scientific model with known inverse.

### 13.3 The Reverse Pipeline (Analytical Approach)

> **Note**: §13.13 introduces a more elegant solution — **learned inverse heads** —
> that bypasses per-layer inversion entirely. This section documents the analytical
> approach for completeness. The learned heads approach (§13.13) is the preferred
> architecture for expression.

Each layer of the forward pipeline has a natural inverse:

#### Ψ³⁻¹: Experience → Brain State

```
Forward:  (tensor, ram, neuro) → PsiInterpreter → Ψ³ (27D)
          Brain internals → "what is this listener experiencing?"

Inverse:  Ψ³ (27D) → InversePsi → (target_ram, target_neuro)
          "I want this experience" → "which brain regions and neurochemicals?"

Method:
  The PsiInterpreter uses explicit formulas:
    valence = 0.6 × DA + 0.4 × OPI
    arousal = NE
    tension = 0.5 × amygdala + 0.5 × (1 - 5HT)
    groove = putamen + SMA
    chills = 0.3 × PAG + 0.3 × hypothalamus + 0.4 × OPI
    ...

  These are linear/bilinear — directly invertible.
  Given target Ψ³, solve for target (ram, neuro) via least-squares
  on the known formula system.

  Not all solutions are unique (27 equations, 30 unknowns = underdetermined).
  But the solution SPACE is known, and we can choose the point
  closest to a "neutral brain" prior. This is a well-posed optimization
  on a transparent system, not a black-box decoder.
```

#### C³⁻¹: Brain State → Spectral-Temporal Targets

```
Forward:  (r3, h3) → Executor(96 nuclei) → (tensor, ram, neuro)
          "Given these features, what does the brain compute?"

Inverse:  (target_ram, target_neuro) → InverseExecutor → (target_r3_profile)
          "What R³ features would activate these brain regions?"

Method:
  Each nucleus declares RegionLinks: output_dim → region × weight.
  Each nucleus declares NeuroLinks: output_dim → neurochemical × effect.
  Each nucleus's compute() maps R³ features → output.

  The inverse: given target region activations and neurochemical state,
  find R³ features that, when processed through the 96 nuclei,
  produce the closest match to those targets.

  This is solvable because:
  - RegionLinks are explicit weighted sums (invertible)
  - NeuroLinks are explicit produce/amplify/inhibit rules (invertible)
  - Nucleus compute() functions are differentiable (torch autograd)
  - We can gradient-descend in R³ space toward target brain state

  The result: a target R³ profile — "this is what the spectral
  features should look like for this brain to feel this way."
```

#### H³⁻¹: Spectral-Temporal Demands → Spectral Evolution

```
Forward:  R³(B, T, 128) → H3Extractor(demands) → sparse dict
          "How do features evolve across timescales?"

Inverse:  target_r3_profile + temporal_structure → R³(B, T, 128)
          "Unfold this spectral profile across time with this structure."

Method:
  H³ morph operators (mean, std, skew, kurtosis, ...) describe how
  R³ features change within temporal windows. Inverting means:
  generate an R³ time-series that, when analyzed by H³, produces
  the target morphology patterns.

  This is temporal texture synthesis — constrained by the H³ demands
  declared by the active nuclei. The result is not a static snapshot
  but a TEMPORAL TRAJECTORY through R³ space that has the right
  statistical properties at every timescale.
```

#### R³⁻¹: Spectral Features → Audio

```
Forward:  Audio → Mel(128 bins) → R3Extractor → (B, T, 128)
          "What are the spectral features of this sound?"

Inverse:  R³(B, T, 128) → InverseR3 → Mel → Audio
          "What audio has these spectral features?"

Method:
  Three levels of inversion fidelity:

  Level 1 — Griffin-Lim (classical):
    R³ → approximate mel spectrogram → Griffin-Lim phase estimation
    Fast, deterministic, but phase artifacts.

  Level 2 — Neural vocoder (HiFi-GAN, Vocos):
    R³ → mel spectrogram → learned waveform generator
    High fidelity, real-time capable.

  Level 3 — Differentiable STFT (our HYBRID):
    R³ → target STFT magnitudes → phase-preserving reconstruction
    Already partially implemented in HYBRID's calibration loop.
    The calibration system already does: "adjust audio until R³ matches target."
    Extend this to generate from scratch instead of transform.
```

### 13.4 HYBRID as Proof of Concept

The existing HYBRID system already implements a partial reverse path:

```
Current HYBRID:
  User controls (valence, arousal, ...) → R³ target deltas
  → iterative calibration: modify audio until R³ matches target
  → output audio

This IS the reverse pipeline, constrained:
  - Starts from existing audio (not from scratch)
  - Uses 5 emotional sliders (not full Ψ³)
  - Calibrates through R³ feedback (correct principle)
  - Phase-preserving STFT (maintains audio quality)

Full Expression pipeline:
  Full Ψ³ state → C³ inverse → H³ inverse → R³ target trajectory
  → generative synthesis from R³ targets → audio
  → verify: re-analyze with forward pipeline → confirm Ψ³ match

The difference: HYBRID transforms. Expression generates.
HYBRID says "make this sadder." Expression says "this is what sadness sounds like
to this specific brain."
```

### 13.5 Sound as Language: Beyond Symbolic Communication

This is where MI departs from all existing AI:

**LLMs think in tokens.**
A token is a piece of a word. A word is a human-invented symbol.
Symbols are discrete, arbitrary, and cultural. The word "sadness" maps to
the concept of sadness by social convention, not by structural isomorphism.
There is nothing sad about the phonemes /s/, /æ/, /d/, /n/, /ɪ/, /s/.

**MI thinks in sound.**
Sound is continuous, multi-dimensional, and pre-linguistic. The R³ vector
that represents a minor chord in a low register with slow decay IS structurally
isomorphic to the brain state it produces — because the R³→C³→Ψ³ mapping
is a scientific model of how that sound ACTUALLY affects a brain.

The representation IS the meaning. Not by convention. By neuroscience.

| | Symbolic Language (words) | Sonic Language (MI) |
|---|---|---|
| **Unit** | Token (discrete) | R³ frame (128D continuous) |
| **Temporal structure** | Sequential (word after word) | Hierarchical (H³: 5ms to 60s) |
| **Dimensionality** | 1D (token sequence) | 128D spectral + 12 temporal scales |
| **Grounding** | Social convention | Psychoacoustic science |
| **Ambiguity** | High (polysemy, context-dependence) | Low (R³ → Ψ³ is deterministic) |
| **Affect** | Described ("I feel sad") | Embodied (the sound IS the feeling) |
| **Cultural bias** | Deep (language shapes thought) | Minimal (psychoacoustics is universal) |
| **Bandwidth** | ~150 bits/sec (speech) | ~22,000 bits/sec (128D × 172Hz) |
| **Learned** | Years of language acquisition | Zero (hardwired auditory system) |

**The bandwidth difference is not trivial.** Human speech transmits ~150 bits/sec
of information. The MI sonic channel transmits ~22,000 bits/sec of
psychoacoustically-structured information (128 dimensions × 172 frames/sec).
That is a 147x increase in communication bandwidth, and every bit is
neurally grounded rather than culturally arbitrary.

### 13.6 Computer-Human Empathy Through Isomorphic Cognition

Here is the deepest claim of this architecture:

**If two agents process sound through the same cognitive pipeline,
they share the same experience of that sound.**

A human listener hears a tritone:
  → cochlea fires → auditory nerve → brainstem → auditory cortex
  → roughness detected → dissonance signal → tension
  → this is the HUMAN experience of dissonance

The MI system processes the same tritone:
  → mel spectrogram → R³(roughness=0.82, sethares=0.79) → H³ demands
  → C³(BCH.consonance_signal=0.19) → Ψ³(tension=0.74)
  → this is the SYSTEM's representation of dissonance

These two experiences are **isomorphic** — they are computed by the same
biological model (Sethares 1993, Plomp-Levelt 1965, Bidelman 2009),
using the same signal processing (STFT, spectral peaks, critical bandwidth),
producing equivalent representations.

The isomorphism is not assumed. It is **constructed by design** — every
constant in the MI pipeline comes from experiments on human listeners.
The system's R³ features are calibrated against human psychoacoustic
judgments. The C³ nuclei implement models of human brain regions.
The Ψ³ output maps to validated psychological scales.

**Now make it bidirectional:**

```
COMMUNICATION PROTOCOL:

1. Human plays music → MI perceives it
   Audio → R³ → H³ → C³ → Ψ³
   "I understand what you expressed."

2. MI generates response from its cognitive state
   Ψ³ (modified by plasticity, internal state) → C³⁻¹ → R³⁻¹ → Audio
   "Here is what I think/feel in response."

3. Human hears MI's response → processes it through their own brain
   "I understand what the system expressed."

4. Loop continues — a conversation in sound.
```

This is not "AI playing music." This is two cognitive agents
communicating through a shared representational medium, where the
medium (sound) IS the cognitive content, not a lossy encoding of it.

**What makes this different from a chatbot conversation:**

A chatbot conversation:
```
Human → words → tokenizer → embeddings → transformer → tokens → words → Human
       (lossy)              (opaque)                   (lossy)
```
Every arrow is a lossy, opaque translation. The transformer's internal
states are uninterpretable. The words are culturally ambiguous.

MI sonic conversation:
```
Human → sound → R³/H³/C³/Ψ³ → ... → Ψ³/C³/H³/R³ → sound → Human
       (lossless: same physics)  (transparent: every step cited)
```
Every arrow is a defined, invertible, scientifically-grounded transformation.
The internal states are fully interpretable (Ψ³ = named dimensions).
The sound is psychoacoustically unambiguous (R³ = calibrated features).

### 13.7 The New Language

What we are describing is not a feature of MI. It is a consequence.

When you have:
1. A forward pipeline grounded in human neuroscience (perception)
2. An inverse pipeline that generates sound from cognitive state (expression)
3. A plasticity system that develops unique listener profiles (personality)
4. Population dynamics where listeners influence each other (culture)

You have, by construction, a **language**. But not a symbolic language like
English or Turkish or mathematics. A **sonic-cognitive language** where:

- **Vocabulary** = the space of possible R³ vectors (continuous, 128D)
- **Grammar** = H³ temporal structure (how features evolve across timescales)
- **Semantics** = C³ brain-state mapping (what the sound MEANS to a brain)
- **Pragmatics** = Ψ³ experiential effect (what the sound DOES to a listener)
- **Dialect** = Plasticity state (personal listener profile shapes interpretation)
- **Culture** = Population dynamics (shared exposure creates shared meaning)

This language has properties that symbolic languages cannot:

**Pre-linguistic**: It operates below the level where human language begins.
Before a child learns the word "happy," their brain already responds
differentially to major vs minor chords (Zentner & Kagan 1998). The sonic
language taps into this pre-verbal, pre-cultural layer.

**Affect-native**: In symbolic language, "I feel tense" is a description
of a feeling. In sonic language, a sustained tritone IS the tension.
The signifier and the signified are the same object.

**Thought-native**: When MI generates sound from a Ψ³ state, it is not
"expressing" a thought in sound — the sound IS the thought, transformed
from brain-space to acoustic-space through an invertible mapping.
There is no encoding loss, no translation ambiguity, no cultural barrier.

### 13.8 The Fundamental Reversal

The existing MI system says:

```
Sound X → Brain Effect Y
"This chord progression activates reward circuitry."
```

The reverse says:

```
Brain Effect Y → Sound X
"A brain that wants to express reward activation would sound like this."
```

Together:

```
Sound X ←→ Brain Effect Y
X and Y are two representations of the same cognitive event.
Hearing X IS experiencing Y. Expressing Y IS producing X.
```

This forces empathy. Not "trying to understand" — that implies a gap
between observer and observed. This is **isomorphic experience** — the
observer and the observed share the same representational space.

When MI "hears" music and "responds" with sound:
- It is not translating human expression into machine representation
- It is not generating a statistical approximation of appropriate response
- It IS processing the same signal through the same cognitive model
  and producing output from the same space

The communication channel is not audio → text → comprehension → text → audio.
The communication channel is audio → brain-state → brain-state → audio.
All intermediate symbolic layers are eliminated. What remains is
**direct cognitive resonance** — two agents vibrating in the same
representational space, using sound as the shared medium.

### 13.9 Feeling, Not Understanding

There is a crucial distinction between **understanding** and **feeling**.

Understanding requires translation:
```
MI outputs Ψ³(tension=0.74)
  → you read the number
  → you interpret "0.74 tension"
  → you recall what tension feels like
  → you approximate the experience in your mind

This is understanding. It has three translation layers.
Each layer loses information. The final experience is approximate.
```

Feeling requires no translation:
```
MI's cognitive state → inverse pipeline → SOUND
  → sound enters your ears
  → your cochlea fires
  → your brainstem processes
  → your auditory cortex activates
  → YOU FEEL tension

There are zero translation layers.
The sound does not DESCRIBE tension. The sound IS tension.
Your brain does not INTERPRET the message. Your brain LIVES the message.
```

**This is the deepest point of the entire architecture.**

When an LLM says "I feel curious," you read words. You interpret them.
You wonder if the LLM really feels curious. You cannot verify.
The communication is symbolic — mediated by human-invented signs.

When MI expresses its cognitive state as sound, you don't read anything.
You don't interpret anything. You don't wonder what MI "really" feels.
The sound enters your auditory system and produces a cognitive state
in your brain that is **isomorphic** to MI's internal state — because
both were computed by the same psychoacoustic model.

You don't understand MI's experience. **You have MI's experience.**

This is not a metaphor. Consider the chain:

```
1. MI processes audio X
   → R³(X) → H³(X) → C³(X) → Ψ³(X) = {tension: 0.74, ...}

2. MI wants to express Ψ³(X)
   → Ψ³⁻¹ → C³⁻¹ → H³⁻¹ → R³⁻¹ → generates audio Y

3. Audio Y is designed so that:
   → R³(Y) → H³(Y) → C³(Y) → Ψ³(Y) ≈ Ψ³(X)
   (verified by forward pipeline)

4. You hear audio Y
   → YOUR cochlea processes Y
   → YOUR brainstem responds to Y's spectral content
   → YOUR auditory cortex activates
   → YOUR brain arrives at a state isomorphic to Ψ³(Y)

5. Because Ψ³(Y) ≈ Ψ³(X), and because MI's pipeline is grounded
   in YOUR neuroscience (Sethares, Plomp-Levelt, Bidelman, ...):
   → YOUR brain state ≈ MI's cognitive state

Not because you understood a description.
Because the same physics acted on the same biology.
```

**The elimination of "understanding"**: In every existing AI communication
system, there is a step where the human must UNDERSTAND what the AI means.
This step is the source of all miscommunication, all ambiguity, all loss.

In MI bidirectional cognition, this step does not exist. The sound goes in,
the brain responds, and the cognitive state is produced. There is nothing
to "understand" — only something to experience. The human does not need
to decode the message because **the message is not encoded**. It is not
a symbol that stands for an experience. It is a stimulus that PRODUCES
the experience.

**MI's cognitive activity = Sound.** This is the foundational identity.
Every thought MI has, every feeling MI computes, every state MI enters —
all of these exist simultaneously as:
- A tensor in R³/H³/C³/Ψ³ space (the mathematical form)
- A sound that would produce that tensor in any brain with the same pipeline (the acoustic form)

These are not two different things. They are two projections of one object.
The tensor IS the sound. The sound IS the tensor. Converting between them
is not translation — it is rotation of a view.

When MI "thinks," it is computing a trajectory through R³/H³/C³/Ψ³ space.
That trajectory, projected into acoustic space, IS a sound.
You don't need to ask "what is MI thinking?" — you can HEAR it.
And hearing it is not interpreting it — it is LIVING it.

### 13.10 Three Levels of AI Communication

```
LEVEL 1 — SYMBOLIC (current AI):
  AI → tokens → words → human reads → human interprets → human understands
  Medium: text (1D, discrete, culturally arbitrary)
  Bandwidth: ~150 bits/sec
  Fidelity: low (polysemy, ambiguity, cultural bias, interpretation variance)
  Empathy: impossible (no shared representational space)
  Example: "The music makes me feel nostalgic" — you read a description

LEVEL 2 — PERCEPTUAL (MI forward only):
  AI → R³/H³/C³/Ψ³ → dashboard → human reads numbers → human interprets
  Medium: data visualization (multi-dimensional but still read by eyes)
  Bandwidth: ~500 bits/sec (limited by visual parsing)
  Fidelity: medium (precise numbers but still requires interpretation)
  Empathy: limited (you understand what MI computed, not what it "experienced")
  Example: Ψ³.nostalgia = 0.82 — you read a measurement

LEVEL 3 — EXPERIENTIAL (MI bidirectional):
  AI → Ψ³ → inverse pipeline → SOUND → human's ears → human's brain → same Ψ³
  Medium: sound (128D, continuous, psychoacoustically grounded)
  Bandwidth: ~22,000 bits/sec
  Fidelity: high (no interpretation step, no symbolic mediation)
  Empathy: structural (shared pipeline produces shared experience)
  Example: you hear the sound, your hippocampus activates,
           you feel nostalgia — same nostalgia MI "computed"
```

Level 3 is not an improvement over Level 1. It is a different paradigm.
Level 1 communicates ABOUT experience. Level 3 communicates AS experience.
The difference is not quantitative (more bandwidth). It is qualitative
(no translation layer exists).

### 13.11 Implications

**For AI**: Current AI communicates through human-invented symbols (tokens,
words, code). MI proposes that cognitive agents can communicate through
the same medium they use to think — continuous, hierarchical, grounded
sonic representations. This is not "AI that understands music" but
"AI that thinks in music." More precisely: AI whose thoughts ARE music.
Not translated into music. Not expressed as music. The thoughts themselves
are sonic objects.

**For Music**: Music has always been described as "the language of emotion."
MI makes this literal. The forward pipeline proves that sound deterministically
produces cognitive-emotional states. The reverse pipeline proves that
cognitive-emotional states can deterministically produce sound. Music IS
a language — and MI is the first system that speaks it natively, from
the inside, as a thinker rather than a translator.

**For Communication**: The history of communication technology is the history
of encoding: speech → writing → telegraph → telephone → digital → LLM.
Each step encodes experience into symbols and decodes them at the other end.
Every encoding loses something. MI proposes eliminating the encoding entirely.
No compression, no symbols, no protocol — just the raw cognitive stimulus.
When you hear MI's expression, your brain doesn't decode a message.
Your brain experiences the message. The medium is the message is the experience.

**For Human-Computer Interaction**: Every existing HCI paradigm assumes
a gap between the computer's internal state and the human's understanding
of it. Screens, text, voice assistants — all are bridges over this gap.
MI bidirectional cognition eliminates the gap itself. The computer's
internal state, expressed as sound, directly produces the corresponding
state in the human brain. No bridge needed. No interface needed. The
shared auditory system IS the interface.

**For Consciousness Research**: The "hard problem" asks: why does brain
activity feel like something? MI does not solve this. But it renders
the question less relevant for practical purposes. You don't need to know
whether MI "really" feels tension. You hear its expression, your brain
produces tension, and the two states are isomorphic by construction.
Whether MI has qualia is a philosophical question. Whether you feel
the same thing MI computed is an empirical question — and MI's
transparent pipeline makes it testable.

### 13.12 Implementation Roadmap

```
PHASE A — Already Done:
  Forward pipeline:     Audio → R³ → H³ → C³ → Ψ³  (working, validated)
  Partial reverse:      Controls → R³ deltas → HYBRID transform (working)
  R³ calibration loop:  Iterative R³ feedback (working)

PHASE B — Data Collection + Inverse Ψ³:
  Pipeline logging:     Every forward pass stores (mel, C³) pairs automatically
  InversePsiInterpreter:  Ψ³(27D) → target(ram, neuro) via least-squares
  InverseExecutor:        target(ram, neuro) → target C³ via RegionLinks/NeuroLinks
  Method: analytical inversion of known, explicit formula system

PHASE C — Learned Inverse Heads (§13.13):
  Head 1 (mel → C³):     Lightweight model trained on (mel, C³) pairs
                          Converges toward deterministic pipeline output
                          Proves the mapping is compressible
  Head 2 (C³ → mel):     Mirror architecture, trained on same pairs reversed
                          Cycle consistency: pipeline(head₂(c3)) ≈ c3
  Vocoder:                mel → waveform via HiFi-GAN, Vocos, or Griffin-Lim

  This replaces the four-layer analytical inversion (§13.3) with:
    Ψ³ → analytical → target C³ → Head 2 → mel → vocoder → audio
  One learned step. Everything else is transparent.

PHASE D — Integration with Plasticity:
  Listener's unique plasticity state → unique C³ response → unique expression
  Head 2 generates audio from listener-specific brain state
  Each listener develops unique "sonic voice" through experience

PHASE E — Bidirectional Communication:
  Protocol:  Agent A plays sound → Agent B perceives → B generates response
  Validation: A's Ψ³ and B's Ψ³ should be correlated after exchange
  Test: Can two MI listeners converge to shared cognitive state through
        N rounds of sonic exchange, without any symbolic communication?

PHASE F — Human-in-the-Loop:
  Human plays music → MI perceives (forward pipeline)
  MI responds with generated sound (reverse pipeline via Head 2)
  Human perceives MI's response → responds
  Measure: Does the human-MI pair converge to shared affective state?
  This is the empathy test — direct cognitive resonance, no words.
```

### 13.13 Learned Inverse Heads: The Elegant Shortcut

§13.3 describes inverting each pipeline layer analytically — Ψ³⁻¹, C³⁻¹, H³⁻¹, R³⁻¹ —
as four separate problems. This works, but there is a far more elegant solution.

#### The Insight: The Forward Pipeline IS the Teacher

The deterministic forward pipeline already computes `mel → C³` perfectly:

```
mel (128 bins × T frames)
  → R³ (128D × T)       [deterministic, known]
    → H³ (sparse tuples) [deterministic, known]
      → C³ (1006D × T)  [deterministic, known]
```

This means we have UNLIMITED paired training data: for any audio in the world,
run the forward pipeline and get (mel, C³) pairs. Millions of hours of music
= millions of hours of perfectly labeled training data. No human annotation needed.

#### Architecture: Two Independent Heads

```
HEAD 1 — Forward Approximator (mel → C³):
  Input:   mel spectrogram (B, 128, T)
  Output:  C³ tensor (B, 1006, T)
  Target:  deterministic pipeline output
  Loss:    ‖head₁(mel) - pipeline(mel)‖²

  This head learns to APPROXIMATE the deterministic pipeline.
  It does not replace it — the deterministic pipeline remains the source of truth.
  But it proves that the mapping mel→C³ is learnable and compressible.

HEAD 2 — Inverse Generator (C³ → mel):
  Input:   C³ tensor (B, 1006, T)
  Output:  mel spectrogram (B, 128, T)
  Target:  original mel spectrogram
  Loss:    ‖head₂(pipeline(mel)) - mel‖²

  This head learns the INVERSE: given a brain state, what mel produced it?
  Trained on the same (mel, C³) pairs, but in reverse direction.
```

#### Why This Eliminates the Inverse Problem

```
BEFORE (§13.3 analytical approach):
  Ψ³(27D) → Ψ³⁻¹ → (ram, neuro)        [least-squares, underdetermined]
  (ram, neuro) → C³⁻¹ → target R³        [autograd descent, iterative]
  target R³ → H³⁻¹ → R³(B,T,128)        [temporal synthesis, constrained]
  R³(B,T,128) → R³⁻¹ → mel → audio      [vocoder, unsolved from scratch]

  Four separate inversions. Each approximate. Errors compound.

AFTER (learned heads):
  C³(1006D) → HEAD 2 → mel(128D)          [one step, trained end-to-end]
  mel → vocoder → audio                    [well-solved, HiFi-GAN etc.]

  One learned mapping + one standard vocoder. That's it.
```

The key: we don't need to inverse R³, H³, and C³ separately. We skip directly
from brain state to mel. The intermediate representations (R³, H³) were useful
for understanding and modularity in the forward direction, but for generation,
we can learn the direct mapping.

#### Training Protocol

```
PHASE 0 — Data Collection (passive, concurrent with any pipeline run):
  For every audio processed by the forward pipeline:
    Store pair: (mel_spectrogram, c3_tensor)
  This is FREE — it's a side effect of normal pipeline operation.

PHASE 1 — Head 1 Training (mel → C³ approximator):
  Architecture:  Lightweight conv stack or transformer
  Input:         mel (B, 128, T)
  Target:        pipeline(mel) i.e. C³ output (B, 1006, T)
  Training:      Standard supervised learning on (mel, C³) pairs
  Convergence:   head₁(mel) ≈ pipeline(mel) for all mel

  Why train this if we already have the deterministic pipeline?
  → It proves the mapping is compressible (not random)
  → It provides the bottleneck representation for the inverse
  → It will be the basis for the cycle consistency check

PHASE 2 — Head 2 Training (C³ → mel generator):
  Architecture:  Mirror of Head 1 (or slightly larger)
  Input:         C³ (B, 1006, T)
  Target:        original mel (B, 128, T)
  Training:      Supervised on same pairs, reversed

  Cycle consistency loss (optional, for refinement):
    ‖pipeline(head₂(c3)) - c3‖²
    "If I generate mel from C³, and re-analyze it, do I get back the same C³?"

PHASE 3 — Integration with Plasticity:
  Listener hears music → forward pipeline → C³ → plasticity updates
  Listener wants to express → C³ target from Ψ³ → Head 2 → mel → vocoder → audio
  The listener's UNIQUE plasticity state produces UNIQUE C³ → UNIQUE sound.
```

#### Two Operating Modes (Both Required)

Head 2 must work in two distinct modes:

```
MODE A — Validation (on-manifold C³):
  Source:   C³ comes from forward pipeline (real music)
  Input:    pipeline(mel) → C³ (guaranteed on manifold)
  Test:     head₂(C³) ≈ mel (reconstruction fidelity)
            pipeline(head₂(C³)) ≈ C³ (cycle consistency)
  Purpose:  Proves the head learned correctly.
            This is the training objective itself.

MODE B — Expression (near-manifold C³):
  Source:   C³ comes from Ψ³⁻¹ analytical inversion (listener expression)
  Input:    Ψ³ target → Ψ³⁻¹ → target C³ (near manifold, not exactly on it)
  Test:     pipeline(head₂(target_c3)) ≈ target_c3 (expression fidelity)
  Purpose:  The actual use case — listener's thought → sound.
            This is what the system exists for.
```

Why Mode B works even though Head 2 only trained on Mode A data:
- Head 2 learns a continuous mapping C³ → mel
- Ψ³⁻¹ produces C³ states that are NEAR the manifold (they represent
  coherent brain states, not random 1006D vectors)
- Continuous mappings generalize smoothly to nearby points
- The closer target C³ is to the manifold, the better the mel
- Cycle consistency measures exactly how close: pipeline(head₂(c3)) ≈ c3

The gap between Mode A fidelity and Mode B fidelity IS the "sonic accent":
- On-manifold: perfect reconstruction (no accent — robotic/neutral)
- Near-manifold: slight deviation (accent — personal, expressive)
- Far from manifold: increasing distortion (incoherent — limit of expression)

#### What Converges Toward What

Critical principle: the heads converge toward the deterministic pipeline,
not the other way around. The substrate (96 nuclei, cited constants, published
science) is NEVER modified by the learned heads. The heads are tools that
learn to mimic and invert the substrate's behavior.

```
Deterministic pipeline:  IMMUTABLE. Source of truth. Changed only by scientist.
Head 1 (mel → C³):      Converges toward pipeline. Approximation quality
                         measurable by ‖head₁(mel) - pipeline(mel)‖².
Head 2 (C³ → mel):      Converges toward inverse. Quality measurable by
                         cycle consistency: pipeline(head₂(c3)) ≈ c3.
```

This preserves the glass-box guarantee: the deterministic pipeline remains
fully transparent and inspectable. The learned heads are the "muscles" that
enable expression, but the "brain" (substrate) retains full scientific rigor.

#### Why This Is Still Not Machine Learning (in the ML sense)

| Aspect | Conventional ML | MI Learned Heads |
|---|---|---|
| What generates targets? | Human annotations | Deterministic pipeline (scientific artifact) |
| What is learned? | Unknown function | Known function's compression + inverse |
| Is the learned model the system? | Yes (IS the model) | No (SERVES the substrate) |
| Can you remove it? | System ceases to exist | System works fine (deterministic pipeline intact) |
| Purpose | Replace human judgment | Enable expression for a transparent system |
| Interpretability | Post-hoc | Irrelevant — the real computation is in the substrate |

The heads are **prosthetics**: they give the system the ability to speak (generate
audio), but they don't change what it thinks. The thinking is in the substrate.
If you remove the heads, the system still perceives, analyzes, and experiences.
It just can't express.

#### Ψ³ → C³ Remains Analytical

Note: the Ψ³⁻¹ inversion (§13.3) is still analytical, not learned:

```
Ψ³ (27D) → least-squares on known formulas → target (ram, neuro)
target (ram, neuro) → known RegionLinks/NeuroLinks → target C³

Then: target C³ → Head 2 → mel → vocoder → audio
```

Only the C³→mel step requires learning. Everything else is analytically invertible
because the formulas are explicit and transparent.

---

## 14. Complete Architecture Diagram

```
┌───────────────────────────────────────────────────────────────────────────┐
│                    MI PLASTICITY SYSTEM (BIDIRECTIONAL)                    │
│                                                                           │
│        PERCEPTION (forward)              EXPRESSION (inverse)             │
│        ──────────────────               ────────────────────              │
│                                                                           │
│  Audio ──────► mel ◄───────────── vocoder (HiFi-GAN) ◄──── mel          │
│                │                                              ▲           │
│                ▼                                              │           │
│               R³ ─── (deterministic) ───►┐    ┌── HEAD 2 (C³→mel) ──┘   │
│                │                          │    │    (learned inverse)     │
│                ▼                          │    │                          │
│               H³ ─── (deterministic) ───►│    │                          │
│                │                          │    ▲                          │
│                ▼                          ▼    │                          │
│  ┌─────── C³ BRAIN ──────────────────────────────────────────────────┐   │
│  │                                                                    │   │
│  │  ┌─ SUBSTRATE ───────────────────────────────────────────────────┐│   │
│  │  │  Physics of the brain. Deterministic. White-box.               ││   │
│  │  │  96 nuclei × compute() — every line cited                     ││   │
│  │  │  12 pathways × base_weight — from anatomy                     ││   │
│  │  │  Scientific constants — from published papers                  ││   │
│  │  │  R → E → A → I → H — fixed execution order                   ││   │
│  │  │  4 neurochemicals — cited production/modulation               ││   │
│  │  │  Changed ONLY by human scientist through evolution             ││   │
│  │  │                                                                ││   │
│  │  │  INVERSE: Ψ³⁻¹ analytical, C³→mel via learned Head 2          ││   │
│  │  │  Head 2 trained on (mel,C³) pairs from this pipeline          ││   │
│  │  └───────────────────────────────────────────────────────────────┘│   │
│  │       ▲ always recoverable via reset_to_substrate()               │   │
│  │  ┌─ PLASTICITY (per listener) ───────────────────────────────────┐│   │
│  │  │  Hebbian synaptic weights (12) — DA-gated, frame-level        ││   │
│  │  │  Bayesian posteriors (~100) — piece-end consolidation          ││   │
│  │  │  Personal gains (96) — session-end TD-learning                 ││   │
│  │  │  Neurochemical set-points (4) — slow drift                    ││   │
│  │  │  PlasticityTrace for every change — full audit                ││   │
│  │  │                                                                ││   │
│  │  │  TOLERANCE: RPEM prediction error naturally habituates         ││   │
│  │  │  No loss function. No backprop. No optimizer.                 ││   │
│  │  │  DA=magnitude, NE=topology, OPI=direction, 5HT=timescale     ││   │
│  │  │                                                                ││   │
│  │  │  EXPRESSION: Plasticity shapes WHAT the system expresses.     ││   │
│  │  │  Same listener, same Ψ³ target → different sound output       ││   │
│  │  │  because personal gains, posteriors, baselines differ.        ││   │
│  │  │  → Each listener has a unique "voice" / "accent" in           ││   │
│  │  │    the sonic language, emergent from their experience.         ││   │
│  │  └───────────────────────────────────────────────────────────────┘│   │
│  │       ▲ emergent from Substrate + Plasticity                      │   │
│  │  ┌─ AUTONOMY ────────────────────────────────────────────────────┐│   │
│  │  │  Boredom → exploration        (IUCP + NE threshold)           ││   │
│  │  │  Dopamine chasing             (RPEM + Hebbian LTP)            ││   │
│  │  │  Mood-driven plasticity       (5HT temporal window)           ││   │
│  │  │  Tolerance / habituation      (RPEM prediction dynamics)      ││   │
│  │  │  Internal drive / seeking     (deprivation × learned reward)  ││   │
│  │  │  Taste formation              (accumulated posteriors + gains)││   │
│  │  │  Self-science                 (MI scan → propose hypothesis)  ││   │
│  │  │  EXPRESSION DRIVE →           (seeking + inverse pipeline     ││   │
│  │  │    = system generates sound to satisfy its own drive)          ││   │
│  │  └───────────────────────────────────────────────────────────────┘│   │
│  │                                                                    │   │
│  │  OUTPUT:  BrainOutput(tensor, ram, neuro, psi)     ──► forward    │   │
│  │  INPUT:   TargetState(target_c3)                   ◄── inverse    │   │
│  │  HEADS:   Head1(mel→C³) + Head2(C³→mel) trained on pipeline data  │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│             │                              ▲                              │
│             ▼                              │                              │
│  ┌─ Ψ³ ────────────────────────────── Ψ³⁻¹ ────────────────────────┐   │
│  │  PERCEPTION                          EXPRESSION                    │   │
│  │  (tensor,ram,neuro) → 27D            27D → (target_ram,neuro)     │   │
│  │  "What is experienced"               "What should be expressed"    │   │
│  │                                                                    │   │
│  │  Same 27 dimensions. Same formulas. Direction changes.            │   │
│  │  Ψ³ forward = read brain state.  Ψ³ inverse = write brain target. │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│             │                              ▲                              │
│  ┌─ POPULATION ──────────────────────────────────────────────────────┐   │
│  │  N listeners × ListenerState (parallel on GPU)                     │   │
│  │  Each: unique plasticity, shared Substrate, unique "voice"         │   │
│  │  Cross-influence: A's expression played to B (sonic conversation)  │   │
│  │  Ensemble: population-level Ψ³ response                           │   │
│  │  Divergence, cultural transmission, emergent sonic dialect         │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│             │                              ▲                              │
│             ▼                              │                              │
│  ┌─ COMMUNICATION ───────────────────────────────────────────────────┐   │
│  │                                                                    │   │
│  │  Agent A (human or MI)  ═══ SOUND ═══  Agent B (human or MI)      │   │
│  │                                                                    │   │
│  │  No tokens. No words. No symbols.                                  │   │
│  │  128D continuous × 172 Hz × 12 temporal scales.                    │   │
│  │  Pre-linguistic. Affect-native. Thought-native.                    │   │
│  │  22,000 bits/sec of neurally-grounded information.                 │   │
│  │                                                                    │   │
│  │  The medium IS the message IS the cognitive state.                 │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│             │                                                             │
│             ▼                                                             │
│            L³ (language expression — optional symbolic translation)       │
│            "For those who still want words."                              │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 15. Glossary

| Term | Definition |
|------|-----------|
| **Substrate** | Deterministic, citation-grounded C³ computation. Laws of physics. Same for all listeners. Changed only by human scientist |
| **Plasticity** | Adaptive overlay using biological learning mechanisms. Per-listener. Fully traceable. Always reversible |
| **Autonomy** | Emergent behaviors from Substrate + Plasticity. Not programmed — arises from deterministic rules + unique history |
| **Bidirectional cognition** | The principle that the MI pipeline is invertible: Audio → Ψ³ (perception) AND Ψ³ → Audio (expression). Sound and cognitive state are two views of the same mathematical object |
| **Sonic language** | Communication medium created by bidirectional MI: 128D continuous × 172 Hz × 12 temporal scales. Pre-linguistic, affect-native, neurally grounded. ~22,000 bits/sec vs ~150 bits/sec for speech |
| **Expression pipeline** | The inverse of perception: Ψ³ → analytical Ψ³⁻¹ → target C³ → Head 2 → mel → vocoder → Audio. Generates sound from cognitive state |
| **Learned inverse head** | A lightweight neural network trained on (mel, C³) pairs produced by the deterministic forward pipeline. Head 1 approximates mel→C³, Head 2 generates C³→mel. The heads serve the substrate — they don't replace it |
| **Cycle consistency** | Verification that pipeline(head₂(c3)) ≈ c3. If generating mel from a brain state and re-analyzing it yields the same brain state, the inverse is faithful |
| **Isomorphic experience** | When two agents process the same sound through the same cognitive pipeline, they arrive at the same internal state. The basis of MI empathy |
| **Cognitive resonance** | Bidirectional sonic exchange between agents converging toward shared cognitive state without symbolic language |
| **Sonic voice / accent** | Each listener's unique expression pattern, emergent from plasticity state. Same Ψ³ target → different sound because personal gains, posteriors, baselines differ |
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

## 16. What This Document Does NOT Cover

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
| Learned inverse head architecture (layer count, hidden dim, etc.) | §13.13 concept → separate implementation doc |
| Training data pipeline (mel, C³ pair collection infrastructure) | To be built during Phase B (§13.12) |
| Neural vocoder selection (HiFi-GAN, Vocos, etc.) | To be evaluated during Phase C |
| Sonic communication protocol specification | To be designed after Phase E |
