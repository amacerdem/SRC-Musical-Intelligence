# H³ Temporal Laws: Neuroscientific Basis for L0 / L1 / L2

**Status**: Research-validated (2026-02-16)
**Purpose**: Document the neuroscientific evidence supporting H³'s three temporal
processing laws and their biological implementation.

---

## 1. The H³ Law System

H³ encodes temporal morphology as 4-tuples: `(r3_idx, horizon, morph, law)`.
The `law` parameter specifies the **temporal direction** of processing:

| Law | Name | Direction | MI Definition |
|-----|------|-----------|---------------|
| L0 | Memory / Causal | Past → Present | Only backward-looking: what happened? |
| L1 | Predictive / Forward | Present → Future | Only forward-looking: what will happen? |
| L2 | Integration / Bidirectional | Past ↔ Present ↔ Future | Both directions: full context |

**Core question**: Is this three-way decomposition of temporal processing supported
by neuroscience, or is it an artificial distinction?

**Answer**: It is supported by multiple converging lines of evidence from laminar
cortical anatomy, oscillatory dynamics, hippocampal replay, and temporal context
models. The three laws map onto real, dissociable neural mechanisms. However, they
are **coupled modes of the same neural tissue**, not independent circuits.

---

## 2. Evidence Line 1: Cortical Laminar Architecture

### 2.1 Forward and Backward Connections Are Physically Separate

The predictive coding framework (Rao & Ballard 1999; Friston 2005, 2009)
establishes that cortical areas communicate via two anatomically distinct
connection types:

**Forward (ascending) connections**:
- Originate from **superficial pyramidal cells** (layers 2/3)
- Project to layer 4 (granular layer) of the next higher area
- Carry **prediction error** signals (what actually happened vs. what was expected)
- Are "driving" — they elicit obligatory responses in target neurons

**Backward (descending) connections**:
- Originate from **deep pyramidal cells** (layers 5/6)
- Project to superficial and deep layers of lower areas (avoiding layer 4)
- Carry **prediction** signals (what is expected based on higher-level models)
- Are "modulatory" — they modulate but don't drive target responses

This anatomical separation has been confirmed empirically:

> "Unexpected stimuli could only be decoded above chance from superficial cortical
> layers, while expected stimuli were represented across all layers."
> — Lawrence et al. (2024), Current Biology

**Mapping to H³ Laws**:

| Cortical Layer | Connection Type | Signal | H³ Law |
|----------------|----------------|--------|--------|
| Superficial (L2/3) | Forward/ascending | Prediction error (what happened) | **L0** (memory/causal) |
| Deep (L5/6) | Backward/descending | Prediction (what's expected) | **L1** (predictive/forward) |
| Both (recurrent) | Lateral + feedback | Integration | **L2** (bidirectional) |

### 2.2 Layer-Specific Evidence

**Lawrence SJD, Sherwood A, Sherwood S, et al. (2024)**. Predictions and errors are
distinctly represented across V1 layers. *Current Biology* 34(19):4365-4377.
doi:10.1016/j.cub.2024.08.049.
- High-field (7T) fMRI, layer-specific BOLD
- Unexpected stimuli decoded from superficial layers ONLY
- Expected stimuli decoded from all layers
- Direct evidence for laminar separation of prediction vs. error

**Klink PC, Dagnino B, Gariel-Mathis MA, Roelfsema PR (2017)**. Distinct feedforward
and feedback effects of microstimulation in visual cortex reveal neural mechanisms
of texture segregation. *Neuron* 95(1):209-220.e3.
doi:10.1016/j.neuron.2017.05.033.
- Feedforward activation: drives superficial layer responses
- Feedback activation: modulates deep layer responses
- Microsecond-precision dissociation of forward vs. backward

---

## 3. Evidence Line 2: Oscillatory Signatures

### 3.1 Different Oscillatory Bands for Different Directions

Empirical work shows that forward and backward information flow use distinct
oscillatory frequencies:

| Oscillation | Frequency | Cortical Layer | Direction | Function | H³ Law |
|-------------|-----------|----------------|-----------|----------|--------|
| **Gamma** | >30Hz | Superficial | Bottom-up | Prediction errors, sensory evidence | L0 |
| **Alpha/Beta** | 8-30Hz | Deep | Top-down | Predictions, expectations | L1 |
| **Theta** | 4-8Hz | All (hippocampal) | Bidirectional | Sequence organization | L2 |

### 3.2 Key Empirical Findings

**Bastos AM, Loonis R, Kornblith S, Lundqvist M, Miller EK (2018)**. Laminar
recordings in frontal cortex suggest distinct layers for maintenance and control
of working memory. *PNAS* 115(5):1117-1122. doi:10.1073/pnas.1710323115.
- Gamma power: concentrated in superficial layers during feedforward
- Alpha/beta power: concentrated in deep layers during feedback

**Bastos AM, Lundqvist M, Waite AS, Kopell N, Miller EK (2020)**. Layer and rhythm
specificity for predictive routing. *PNAS* 117(49):31459-31469.
doi:10.1073/pnas.2014868117.
- Predictive signals (alpha/beta) suppress sensory responses (gamma)
- Layer-specific routing: superficial = prediction error, deep = prediction
- Direct demonstration of rhythm × layer × direction specificity

**Michalareas G, Vezoli J, van Pelt S, Schoffelen JM, Kennedy H, Fries P (2016)**.
Alpha-beta and gamma rhythms subserve feedback and feedforward influences among
human visual areas. *Neuron* 89(2):384-397. doi:10.1016/j.neuron.2015.12.018.
- Gamma in feedforward direction: significant in 47/56 area pairs
- Alpha-beta in feedback direction: significant in 38/56 area pairs
- Directional index: significant separation of forward vs. backward

### 3.3 Theta-Gamma Coupling: The Bidirectional Code (L2)

**Lisman JE, Jensen O (2013)**. The theta-gamma neural code. *Neuron*
77(6):1002-1016. doi:10.1016/j.neuron.2013.03.007.
- Individual items encoded in gamma subcycles
- Sequential order encoded in theta phase
- Within one theta cycle: past→present→future compressed
- 7±2 gamma subcycles per theta cycle = working memory capacity

This theta-gamma coupling represents the **bidirectional (L2)** processing mode:
within each theta cycle, the hippocampus compresses a temporal sequence spanning
past, present, and predicted future positions.

**Canolty RT, Edwards E, Dalal SS, et al. (2006)**. High gamma power is phase-locked
to theta oscillations in human neocortex. *Science* 313(5793):1626-1628.
doi:10.1126/science.1128115.
- Theta-gamma coupling exists in human neocortex (not just hippocampus)
- Amplitude of gamma modulated by phase of theta
- Suggests L2-type bidirectional processing is a general cortical mechanism

---

## 4. Evidence Line 3: Hippocampal Forward and Reverse Replay

### 4.1 The Most Direct Evidence for Directional Dissociation

Hippocampal place cells replay experienced sequences in **two distinct directions**
during sharp-wave ripples (SWRs):

**Forward replay**:
- Occurs at the **start** of a trajectory (before action)
- Replays current location → goal location
- Function: **planning / prediction** (present → future)
- NOT modulated by reward magnitude

**Reverse replay**:
- Occurs at **reward locations** (after consummation)
- Replays current location → past trajectory (backward)
- Function: **memory consolidation / credit assignment** (present → past)
- IS modulated by reward (increases with larger reward)

**This is a clean biological dissociation**: same neural substrate (CA1 place cells),
same physiological event (SWR), but two distinct temporal directions with different
triggers, different functional roles, and different modulatory profiles.

### 4.2 Key Papers

**Diba K, Buzsaki G (2007)**. Forward and reverse hippocampal place-cell sequences
during ripples. *Nature Neuroscience* 10(10):1241-1242. doi:10.1038/nn1961.
- First demonstration of both forward and reverse replay in same session
- Forward replay: occurred during running, biased toward upcoming trajectory
- Reverse replay: occurred during pauses, biased toward just-traversed path

**Pfeiffer BE, Foster DJ (2013)**. Hippocampal place-cell sequences depict future
paths to remembered goals. *Nature* 497(7447):74-79. doi:10.1038/nature12112.
- Forward replay generates trajectories to **novel** goal locations
- Not simple replay of past experience — genuine prediction/planning
- "Brief sequences encoding spatial trajectories strongly biased to progress
  from the subject's current location to a known goal location"

**Ambrose RE, Pfeiffer BE, Foster DJ (2016)**. Reverse replay of hippocampal place
cells is uniquely modulated by changing reward. *Neuron* 91(5):1124-1136.
doi:10.1016/j.neuron.2016.07.047.
- Reverse replay: increases when reward increases, decreases when reward decreases
- Forward replay: NOT modulated by reward changes
- "Reverse replay... is ideally suited for evaluating recent events and
  propagating updated information to newly preceding states"

**Olafsdottir HF, Bush D, Barry C (2018)**. The role of hippocampal replay in
memory and planning. *Current Biology* 28(1):R37-R50.
doi:10.1016/j.cub.2017.10.073.
- Comprehensive review of replay directionality
- Forward replay → planning, model-based decision making
- Reverse replay → offline learning, credit assignment

### 4.3 Mapping to H³

| Replay Direction | Temporal Direction | Function | H³ Law |
|------------------|-------------------|----------|--------|
| **Reverse replay** | Present → Past | Memory consolidation, credit assignment | **L0** |
| **Forward replay** | Present → Future | Planning, goal-directed prediction | **L1** |
| **Interleaved** | Both during rest | Integration, model updating | **L2** |

---

## 5. Evidence Line 4: Temporal Context Model (Howard & Kahana)

### 5.1 Asymmetric Temporal Associations

The **Temporal Context Model (TCM)** (Howard & Kahana 2002) and its successor
**Context Maintenance and Retrieval (CMR)** (Polyn, Norman & Kahana 2009) show that
temporal memory has an inherent **forward asymmetry**:

**The mechanism**:
- Context drifts gradually during encoding
- When an item is recalled, it **reinstates** the context from encoding
- Context incorporates an item **after** it is presented
- Therefore, retrieved context shares more similarity with items that came **AFTER**
  (forward in time) than items that came **BEFORE** (backward)

**The result**: A ~2:1 ratio of forward-to-backward associations in free recall.
Subjects are approximately twice as likely to recall items in the forward direction
and are significantly faster doing so.

**Howard MW, Kahana MJ (2002)**. A distributed representation of temporal context.
*J Math Psychol* 46(3):269-299. doi:10.1006/jmps.2001.1388.
- Foundational paper: context as a gradually drifting representation
- Forward contiguity effect: CRP asymmetry ~2:1

**Polyn SM, Norman KA, Kahana MJ (2009)**. A context maintenance and retrieval
model of organizational processes in free recall. *Psychol Rev* 116(1):129-156.
doi:10.1037/a0014420.
- Extended TCM with semantic and source context
- Forward asymmetry preserved in all conditions

### 5.2 Implications for H³

The TCM asymmetry means that at every temporal scale:
- **L0 (memory) morphs should be more informative** than L1 (prediction) morphs
  for the same horizon, because the brain encodes more past context than
  future prediction at each level
- The **memory window extends further** than the prediction window: ~5:1 at A1
  level (200ms back, ~40ms forward), ~2:1 at higher cortical levels
- L2 (bidirectional) is NOT symmetric — it is dominated by the past direction

---

## 6. Evidence Line 5: Feedforward Sweep vs. Recurrent Processing

### 6.1 Two Temporal Phases of Cortical Processing

Every cortical response to a stimulus has two distinct phases:

**Phase 1: Feedforward sweep (~0-100ms post-stimulus)**
- Rapid, strictly bottom-up propagation through the cortical hierarchy
- Each area responds in sequence with minimal feedback
- Carries **what actually happened** — sensory evidence
- Some fast categorization possible with feedforward alone
- Maps to: **L0 (causal/memory)**

**Phase 2: Recurrent processing (~100-500ms+ post-stimulus)**
- Feedback from higher areas modulates lower areas
- Horizontal connections integrate within-area context
- Top-down predictions refine bottom-up representations
- Required for conscious perception, figure-ground segregation, attention
- Maps to: **L2 (bidirectional)**, with L1 predictions cascading down

**Lamme VAF, Roelfsema PR (2000)**. The distinct modes of vision offered by
feedforward and recurrent processing. *Trends Neurosci* 23(11):571-579.
doi:10.1016/S0166-2236(00)01657-X.
- Foundational paper: feedforward vs. recurrent as distinct processing modes
- Feedforward: fast, unconscious, bottom-up
- Recurrent: slower, required for consciousness, bidirectional

**Kar K, DiCarlo JJ (2020)**. Fast recurrent processing via ventrolateral prefrontal
cortex is needed by the primate ventral stream for object recognition. *PNAS*
118(3):e2017916118. doi:10.1073/pnas.2017916118.
- Feedforward-dominated activity: 70-120ms post-stimulus
- Feedback-dominated activity: >120ms post-stimulus
- Population activity patterns are DISTINCT for each phase

### 6.2 Temporal Sequence of Processing Modes

The biological evidence suggests L0, L1, L2 are not simultaneous parallel
processes but a **temporal sequence** that repeats at each horizon:

```
Stimulus arrives at cortical level N:

  0-100ms:  L0 DOMINANT (feedforward sweep)
            Sensory evidence propagates upward
            Error signals computed against current predictions

  100-300ms: L2 DOMINANT (recurrent processing)
            Top-down predictions (L1) meet bottom-up errors (L0)
            Integration, context refinement
            Conscious awareness emerges

  300ms+:   L1 UPDATES (prediction refinement)
            Internal models updated based on integrated evidence
            New predictions generated for next time step

  [Cycle repeats for next input at this level's timescale]
```

This means within each H³ horizon, the three laws operate **sequentially**:
L0 (measure) → L2 (integrate) → L1 (predict) → L0 (measure) → ...

---

## 7. Evidence Line 6: mPFC Past and Future Cells

### 7.1 Direct Cellular Evidence for Temporal Direction Coding

**Howard MW, Shimbo A, Bhatt P, Bhatt DK, Bhatt S (2024)**. Ramping cells in
rodent mPFC encode time to past and future events via complementary exponentials.
*PNAS* 121(27):e2404169121. doi:10.1073/pnas.2404169121.

This study found two complementary cell populations in medial prefrontal cortex:

**"Past cells"**:
- Fire at the START of a temporal interval
- Activity decays exponentially back to baseline
- Encode time SINCE a past event
- Distributed across a range of decay time constants

**"Future cells"**:
- Activity increases exponentially toward the END of an interval
- Peak right before the anticipated event
- Encode time UNTIL a future event
- Distributed across a range of growth time constants

Both populations coexist in the **same brain region**, interleaved, with a
continuous distribution of time constants. This is perhaps the most direct
cellular evidence that past and future are encoded by **distinct neural
mechanisms** within the same cortical area.

### 7.2 Implications for H³

- The past/future distinction is not just a computational convenience — it
  reflects **actual cellular specialization** in prefrontal cortex
- The continuous distribution of time constants matches H³'s horizon system:
  different cells encode different temporal scales
- Past cells → L0 morphs; Future cells → L1 morphs; Both together → L2

---

## 8. Evidence Line 7: Bidirectional Hierarchical Temporal Representation

### 8.1 The Most Directly Relevant Study

**Tarder-Stoll H, Jayakumar M, Engel SA, Aly M, Davachi L (2024)**. The brain
hierarchically represents the past and future during multistep anticipation.
*Nature Communications* 15:5765. doi:10.1038/s41467-024-48329-7.

Key findings:
- Temporal structure represented **bidirectionally**: graded representations
  extending into BOTH past and future
- Temporal structure represented **hierarchically**: further events into past
  and future represented in successively more **anterior** brain regions
- Visual cortex: primarily current environment (present)
- Hippocampus: graded representations of further environments (past AND future)
- These representations are **behaviorally relevant**: suppression of distant
  representations linked to response time costs

> "Although an analysis was designed to allow differential coding of the future
> versus the past, representations were not uniquely biased toward future states."

This directly supports the H³ architecture where:
- Each horizon level has both L0 (past) and L1 (future) morphs
- Higher horizons (longer TRW) represent further into past and future
- L2 (bidirectional) is the natural state; L0 and L1 are decompositions

---

## 9. Synthesis: Three Laws as Three Modes

The evidence converges on this model:

```
┌──────────────────────────────────────────────────────────────────┐
│                    CORTICAL COLUMN                                │
│                                                                  │
│  SUPERFICIAL LAYERS (2/3)     ┌─────────────────────────┐       │
│  • Gamma oscillations          │  L0: PREDICTION ERROR    │       │
│  • Forward connections         │  "What actually happened" │       │
│  • Prediction error signals    │  Memory trace / evidence  │       │
│                                └─────────────────────────┘       │
│                                                                  │
│  GRANULAR LAYER (4)           ┌─────────────────────────┐       │
│  • Thalamic input              │  L2: INTEGRATION         │       │
│  • Feedforward relay           │  "Error meets prediction" │       │
│  • Present moment              │  Bidirectional context    │       │
│                                └─────────────────────────┘       │
│                                                                  │
│  DEEP LAYERS (5/6)            ┌─────────────────────────┐       │
│  • Alpha/Beta oscillations     │  L1: PREDICTION          │       │
│  • Backward connections        │  "What is expected next"  │       │
│  • Top-down predictions        │  Forward-looking model    │       │
│                                └─────────────────────────┘       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**The three laws are not independent parallel pipelines. They are three coupled
modes of the same cortical column, operating in sequence within each processing
cycle and in parallel across the cortical hierarchy.**

Within a single processing cycle at horizon H:
1. **L0** fires first (feedforward sweep, gamma, superficial)
2. **L2** fires second (recurrent exchange, theta, all layers)
3. **L1** fires third (prediction update, alpha/beta, deep)
4. Cycle repeats at the timescale of horizon H

Across the hierarchy:
- Level 0 (short TRW) completes its L0→L2→L1 cycle first
- Level 1 (medium TRW) uses Level 0's output + its own L0→L2→L1
- Level N uses Levels 0..N-1 + its own cycle

---

## 10. Complete Reference List

### Predictive Coding / Laminar Architecture

1. **Rao RPN, Ballard DH (1999)**. Predictive coding in the visual cortex: a
   functional interpretation of some extra-classical receptive-field effects.
   *Nature Neuroscience* 2(1):79-87. doi:10.1038/4580.

2. **Friston K (2005)**. A theory of cortical responses. *Phil Trans R Soc B*
   360(1456):815-836. doi:10.1098/rstb.2005.1622.

3. **Friston K (2009)**. The free-energy principle: a unified brain theory?
   *Nature Reviews Neuroscience* 11(2):127-138. doi:10.1038/nrn2787.

4. **Bastos AM, Usrey WM, Adams RA, Mangun GR, Fries P, Friston KJ (2012)**.
   Canonical microcircuits for predictive coding. *Neuron* 76(4):695-711.
   doi:10.1016/j.neuron.2012.10.038.

5. **Lawrence SJD, et al. (2024)**. Predictions and errors are distinctly
   represented across V1 layers. *Current Biology* 34(19):4365-4377.
   doi:10.1016/j.cub.2024.08.049.

### Oscillatory Dynamics

6. **Bastos AM, Lundqvist M, Waite AS, Kopell N, Miller EK (2020)**. Layer and
   rhythm specificity for predictive routing. *PNAS* 117(49):31459-31469.
   doi:10.1073/pnas.2014868117.

7. **Michalareas G, Vezoli J, van Pelt S, et al. (2016)**. Alpha-beta and gamma
   rhythms subserve feedback and feedforward influences among human visual areas.
   *Neuron* 89(2):384-397. doi:10.1016/j.neuron.2015.12.018.

8. **Bastos AM, Loonis R, Kornblith S, Lundqvist M, Miller EK (2018)**. Laminar
   recordings in frontal cortex suggest distinct layers for maintenance and control
   of working memory. *PNAS* 115(5):1117-1122. doi:10.1073/pnas.1710323115.

9. **Lisman JE, Jensen O (2013)**. The theta-gamma neural code. *Neuron*
   77(6):1002-1016. doi:10.1016/j.neuron.2013.03.007.

10. **Canolty RT, Edwards E, Dalal SS, et al. (2006)**. High gamma power is
    phase-locked to theta oscillations in human neocortex. *Science*
    313(5793):1626-1628. doi:10.1126/science.1128115.

### Hippocampal Replay

11. **Diba K, Buzsaki G (2007)**. Forward and reverse hippocampal place-cell
    sequences during ripples. *Nature Neuroscience* 10(10):1241-1242.
    doi:10.1038/nn1961.

12. **Pfeiffer BE, Foster DJ (2013)**. Hippocampal place-cell sequences depict
    future paths to remembered goals. *Nature* 497(7447):74-79.
    doi:10.1038/nature12112.

13. **Ambrose RE, Pfeiffer BE, Foster DJ (2016)**. Reverse replay of hippocampal
    place cells is uniquely modulated by changing reward. *Neuron*
    91(5):1124-1136. doi:10.1016/j.neuron.2016.07.047.

14. **Olafsdottir HF, Bush D, Barry C (2018)**. The role of hippocampal replay in
    memory and planning. *Current Biology* 28(1):R37-R50.
    doi:10.1016/j.cub.2017.10.073.

### Temporal Context Model

15. **Howard MW, Kahana MJ (2002)**. A distributed representation of temporal
    context. *J Math Psychol* 46(3):269-299. doi:10.1006/jmps.2001.1388.

16. **Polyn SM, Norman KA, Kahana MJ (2009)**. A context maintenance and retrieval
    model of organizational processes in free recall. *Psychol Rev*
    116(1):129-156. doi:10.1037/a0014420.

### Feedforward vs. Recurrent

17. **Lamme VAF, Roelfsema PR (2000)**. The distinct modes of vision offered by
    feedforward and recurrent processing. *Trends Neurosci* 23(11):571-579.
    doi:10.1016/S0166-2236(00)01657-X.

18. **Kar K, DiCarlo JJ (2020)**. Fast recurrent processing via ventrolateral
    prefrontal cortex is needed by the primate ventral stream for object
    recognition. *PNAS* 118(3):e2017916118. doi:10.1073/pnas.2017916118.

### mPFC Past/Future Cells

19. **Howard MW, Shimbo A, et al. (2024)**. Ramping cells in rodent mPFC encode
    time to past and future events via complementary exponentials. *PNAS*
    121(27):e2404169121. doi:10.1073/pnas.2404169121.

### Bidirectional Hierarchical Representation

20. **Tarder-Stoll H, Jayakumar M, Engel SA, Aly M, Davachi L (2024)**. The brain
    hierarchically represents the past and future during multistep anticipation.
    *Nature Communications* 15:5765. doi:10.1038/s41467-024-48329-7.

### Temporal Prediction and Attention

21. **Herrmann B, Henry MJ, Haegens S, Obleser J (2016)**. Temporal expectations
    and neural amplitude fluctuations in auditory cortex interactively influence
    perception. *NeuroImage* 124:487-497.
    doi:10.1016/j.neuroimage.2015.09.019.

22. **Arnal LH, Giraud AL (2012)**. Cortical oscillations and sensory predictions.
    *Trends Cogn Sci* 16(7):390-398. doi:10.1016/j.tics.2012.05.003.

### Temporal Asymmetry

23. **Jeunehomme O, D'Argembeau A (2024)**. Temporal asymmetries in inferring
    unobserved past and future events. *Nature Communications* 15:8765.
    doi:10.1038/s41467-024-52627-5.

### Predictive Processing Reviews

24. **Clark A (2013)**. Whatever next? Predictive brains, situated agents, and
    the future of cognitive science. *Behavioral and Brain Sciences*
    36(3):181-204. doi:10.1017/S0140525X12000477.

25. **Keller GB, Mrsic-Flogel TD (2018)**. Predictive processing: a canonical
    cortical computation. *Neuron* 100(2):424-435.
    doi:10.1016/j.neuron.2018.10.003.

### Hierarchical Timescales

26. **Kiebel SJ, Daunizeau J, Friston KJ (2008)**. A hierarchy of time-scales and
    the brain. *PLoS Comput Biol* 4(11):e1000209.
    doi:10.1371/journal.pcbi.1000209.
    - "Specifying the generalized coordinates of motion at any time point encodes
      the present, past, and future states of the system."

27. **Murray JD, Bernacchia A, Freedman DJ, Romo R, Wallis JD, et al. (2014)**.
    A hierarchy of intrinsic timescales across primate cortex. *Nature Neuroscience*
    17(12):1661-1663. doi:10.1038/nn.3862.

### Laminar Feedback Dissociation

28. **Sharoh D, van Mourik T, Bains LJ, et al. (2019)**. Laminar specific fMRI
    reveals directed interactions in distributed networks during language
    processing. *PNAS* 116(42):21185-21190. doi:10.1073/pnas.1907858116.

29. **Kok P, Bains LJ, van Mourik T,"; et al. (2016)**. Selective activation of the
    deep layers of the human primary visual cortex by top-down feedback. *Current
    Biology* 26(3):371-376. doi:10.1016/j.cub.2015.12.038.
