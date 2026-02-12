> **DEPRECATED** — This document describes the old VMM-only semantic space (v1.x).
> Superseded by [L³-BRAIN-SEMANTIC-SPACE.md](L³-BRAIN-SEMANTIC-SPACE.md) which covers
> the unified 104D L³ layer (8 groups α→θ) for the MusicalBrain. Retained for historical reference.

# L³ — Semantic Space for the VMM Model

> Musical Intelligence (MI) v1.0.0 — 2026-02-11
> The interpretation layer: giving meaning to valence computation.
> Scope: ARU-α3-VMM model only. Companion to L³-SRP and L³-AAC.

---

## 1. What Is L³ for VMM?

L³ for VMM provides the **semantic interpretation** of the 12D valence output.
Where SRP L³ interprets dopaminergic reward and AAC L³ interprets autonomic
responses, VMM L³ interprets **perceived emotional valence** — the cognitive
categorization of music's emotional character (happy/sad/neutral).

```
┌─────────────────────────────────────────────────────────────────┐
│                     L³ VMM SEMANTIC SPACE                        │
│                                                                  │
│  ┌─── Group α ── Computation Semantics (Level 1) ───────── 5D  │
│  │   Which mechanisms and inputs drive valence?                  │
│  │                                                               │
│  ├─── Group β ── Neuroscience Semantics (Level 2) ────── 6D    │
│  │   Which neural pathways? Striatal vs limbic?                  │
│  │                                                               │
│  ├─── Group γ ── Psychology Semantics (Level 3) ──────── 5D    │
│  │   Perceived vs felt, certainty, emotional complexity          │
│  │                                                               │
│  └─── Group δ ── Validation Semantics (Level 4) ──────── 5D    │
│      Musical predictions, cross-model convergence                │
│                                                                  │
│  TOTAL L³: 21D interpretation for 12D computation                │
│  COMPLETE SEMANTIC FOOTPRINT: 12D + 21D = 33D                   │
└─────────────────────────────────────────────────────────────────┘
```

### VMM L³ vs SRP L³ vs AAC L³

| | SRP L³ | AAC L³ | VMM L³ |
|---|--------|--------|--------|
| Computation | 19D | 14D | 12D |
| L³ Interpretation | 45D | 26D | 21D |
| Ratio (interp/comp) | 2.37:1 | 1.86:1 | 1.75:1 |
| Focus | Reward, pleasure, DA | ANS, physiology | Valence, mode, emotion |
| Total | 64D | 40D | 33D |

VMM's L³ is the most compact because its output dimensions already map closely
to interpretable psychological constructs (happy/sad/valence are not as abstract
as wanting/liking). Still, the semantic layer adds crucial context about the
neuroscience, the computation sources, and the cross-model relationships.

---

## 2. Group α — Computation Semantics (5D)

These dimensions interpret WHAT the computation is doing at each frame —
which mechanisms and inputs drive VMM's valence output.

### α0: aed_contribution [0, 1]

**Formula**: Fraction of VMM output driven by AED mechanism (weight 0.8).

**What it reveals**: When high, valence is strongly modulated by arousal dynamics.
High arousal amplifies both happy and sad pathways (Trost 2012: arousal-valence
interaction). A quiet, low-arousal passage may have clear mode but muted pathway
activation because AED contribution is low.

**Feeds from VMM**: sad_pathway (aed_arousal × 0.3), parahippocampal (aed_arousal × 0.4),
reward_evaluation (aed_expectancy × 0.1), consonance_valence (aed_flow × 0.2).

### α1: c0p_contribution [0, 1]

**Formula**: Fraction of VMM output driven by C0P mechanism (weight 0.6).

**What it reveals**: When high, valence is modulated by the listener's cognitive
state — attention, memory retrieval, engagement level. A distracted listener
(low C0P engagement) may show weaker valence categorization.

**Feeds from VMM**: mode_signal (c0p_processing × 0.3), consonance_valence
(c0p_cognitive × 0.3), happy_pathway (c0p_cognitive × 0.2), parahippocampal
(c0p_processing × 0.3), reward_evaluation (c0p_integration × 0.2).

### α2: direct_h3_contribution [0, 1]

**Formula**: Fraction of VMM output derived from direct H³ reads (7 tuples).

**What it reveals**: When high, valence is primarily driven by the **raw acoustic
context** rather than mechanism-mediated processing. Direct reads capture
consonance, brightness, and mode at phrase-to-section timescales (3-15s).
This is the "bottom-up" contribution to valence.

**Feeds from VMM**: consonance_state, consonance_mean, consonance_var,
brightness_section, mode_trajectory, mode_stability, valence_velocity.

### α3: mode_dominance [0, 1]

**Formula**: |mode_signal - 0.5| × 2 — how strongly mode determines valence.

**What it reveals**: When high, the mode (major/minor) is the primary driver
of valence categorization. When low (mode_signal ≈ 0.5), mode is ambiguous
and consonance/brightness dominate instead. This dimension tracks whether
VMM is in "mode-driven" or "consonance-driven" operation.

### α4: timescale_active [0, 1]

**Formula**: Weighted indicator of which timescale dominates VMM:
- H19 (3s) dominant → phrase-level valence (local harmony)
- H22 (15s) dominant → section-level valence (tonal center)

**What it reveals**: Short timescale = fast harmonic changes; long timescale =
stable tonal context. During modulation, H19 leads the change while H22 lags.

---

## 3. Group β — Neuroscience Semantics (6D)

These dimensions interpret the **neural circuit activation** underlying VMM's
output — mapping computation to brain pathways.

### β0: striatal_dominance [0, 1]

**Formula**: happy_pathway / (happy_pathway + sad_pathway + ε)

**What it reveals**: The relative activation of the striatal reward circuit
(VS, DS, ACC) vs the limbic-emotional circuit (HIP, AMY, PHG). When > 0.5,
the music activates reward pathways (major/consonant). When < 0.5, limbic
pathways dominate (minor/dissonant). Maps to Mitterschiffthaler 2007 double
dissociation.

**Brain regions**: VS (NAcc, t=4.58), DS (Caudate, z=3.80), ACC (z=3.39)

### β1: limbic_dominance [0, 1]

**Formula**: sad_pathway / (happy_pathway + sad_pathway + ε)

**What it reveals**: Complement of β0. When high, music engages the limbic-
emotional circuit. Key for sad, contemplative, and nostalgic music.

**Brain regions**: HIP (t=4.88), AMY (t=4.7), PHG (t=5.7)

### β2: pathway_dissociation [-1, 1]

**Formula**: happy_pathway - sad_pathway

**What it reveals**: The DEGREE of dissociation between pathways. When ≈ 0,
both pathways are equally active (ambiguous, mixed emotion, modulation).
When strongly positive or negative, the music clearly activates one pathway.
Mitterschiffthaler 2007: the dissociation is anatomical, not just a gradient.

### β3: parahippocampal_activation [0, 1]

**Formula**: parahippocampal (directly from VMM output)

**What it reveals**: Context processing — active for BOTH happy and sad music,
strongest for contemplative and ambiguous passages. Green 2008: PHG responds
to mode (minor > major) even controlling for dissonance. This is the brain
region that processes harmonic context rather than simple valence polarity.

### β4: acc_evaluation [0, 1]

**Formula**: reward_evaluation (directly from VMM output)

**What it reveals**: Anterior cingulate cortex evaluation signal. Strongest
for confirmed positive valence. Trost 2012: sgACC z=6.15 for nostalgia.
This is the brain's "evaluation of the evaluation" — meta-monitoring of
emotional processing.

### β5: lateralization_index [-1, 1]

**Formula**: perceived_happy - perceived_sad (proxy for hemispheric lateralization)

**What it reveals**: Khalfa 2005 found lateralized processing: happy recognition
→ left medial temporal; sad recognition → left orbitofrontal/mid-dorsolateral.
While we don't model hemispheric differences explicitly, the balance between
perceived_happy and perceived_sad captures the functional lateralization pattern.

---

## 4. Group γ — Psychology Semantics (5D)

These dimensions interpret the **psychological experience** underlying VMM's
output — what the listener perceives and feels.

### γ0: perceived_felt_dissociation [-1, 1]

**Formula**: VMM.f03_valence × SRP.pleasure (cross-model)

**What it reveals**: The critical Brattico 2011 dissociation.
- Positive × positive = happy music that feels good (concordant)
- Negative × positive = **sad music that feels good** (paradox of sad music)
- Negative × negative = sad music that feels bad (aversive)
- Positive × negative = happy music that doesn't feel rewarding (disconnected)

This is VMM's unique contribution: it separates WHAT we perceive from WHAT
we feel, enabling the system to model music enjoyment regardless of valence.

### γ1: emotion_clarity [0, 1]

**Formula**: emotion_certainty (directly from VMM)

**What it reveals**: How clearly the listener categorizes the music's emotion.
High during stable major or minor passages. Low during modulation, atonal
passages, chromatic ambiguity, or mode mixture. Drops predict that the
listener is uncertain about the music's emotional character.

### γ2: emotional_complexity [0, 1]

**Formula**: parahippocampal × (1 - |pathway_dissociation|)

**What it reveals**: When both pathways are moderately active AND context
processing is high, the music evokes **mixed emotions** — bittersweet,
nostalgic, contemplative. This is musically important: the most emotionally
rich passages often resist simple happy/sad categorization.

### γ3: valence_stability [0, 1]

**Formula**: mode_stability × emotion_certainty

**What it reveals**: How stable the emotional character is over time. High
during extended passages in a clear key. Drops during modulation sequences,
development sections, or transitions. A high value suggests the listener has
a sustained emotional impression.

### γ4: valence_trajectory [-1, 1]

**Formula**: valence_forecast (directly from VMM)

**What it reveals**: Where the emotional character is heading — approaching
resolution (positive) or moving toward tension/sadness (negative). This gives
the listener's implicit sense of emotional direction, which skilled composers
manipulate through harmonic progressions and key relationships.

---

## 5. Group δ — Validation Semantics (5D)

These dimensions provide **testable predictions** and cross-model convergence
signals for composer validation in MI-Lab.

### δ0: mode_accuracy [0, 1]

**Formula**: Correlation between mode_signal and known musical mode annotations.

**What it reveals**: Whether VMM's mode detection matches the actual musical mode.
If the music is in major and mode_signal < 0.5, mode detection is failing.
This is the primary validation signal for VMM's mode classification.

### δ1: picardy_response [0, 1]

**Formula**: max(happy_pathway change) at Picardy third moments

**What it reveals**: The Picardy third (major chord at the end of a minor piece)
should produce a dramatic positive jump in happy_pathway. The jump should be
≥ 2× the surrounding context. Failure to detect this = VMM is too slow or mode
detection is insufficiently sensitive.

### δ2: srp_convergence [0, 1]

**Formula**: Correlation between VMM.happy_pathway and SRP.da_nacc over time

**What it reveals**: Happy pathway activation should positively correlate with
striatal DA release (SRP). If the correlation is near zero, VMM and SRP are
measuring unrelated signals. Moderate positive correlation (~0.3-0.6) is
expected because the circuits overlap but are not identical.

### δ3: aac_convergence [0, 1]

**Formula**: |Correlation between VMM.sad_pathway and AAC.scr|

**What it reveals**: Sad/scary music elevates SCR (Gosselin 2005). We expect a
moderate positive correlation between sad_pathway and skin conductance. If zero,
VMM valence and ANS arousal are completely disconnected.

### δ4: paradox_of_sad_music [0, 1]

**Formula**: max(0, -VMM.f03_valence × SRP.pleasure)

**What it reveals**: Active when VMM says "sad" and SRP says "pleasurable."
This captures the central paradox that VMM was designed to model. If this
dimension is never active across a corpus of sad music, either VMM or SRP
is miscalibrated.

---

## 6. Complete L³ VMM Dimension Map

| Group | ID | Name | Range | Source |
|-------|----|------|-------|--------|
| α (Comp) | α0 | aed_contribution | [0,1] | AED weight in VMM |
| | α1 | c0p_contribution | [0,1] | C0P weight in VMM |
| | α2 | direct_h3_contribution | [0,1] | Raw H³ contribution |
| | α3 | mode_dominance | [0,1] | Mode vs consonance driver |
| | α4 | timescale_active | [0,1] | H19 vs H22 dominance |
| β (Neuro) | β0 | striatal_dominance | [0,1] | VS/DS activation ratio |
| | β1 | limbic_dominance | [0,1] | HIP/AMY activation ratio |
| | β2 | pathway_dissociation | [-1,1] | Degree of pathway split |
| | β3 | parahippocampal_activation | [0,1] | Context processing |
| | β4 | acc_evaluation | [0,1] | ACC reward evaluation |
| | β5 | lateralization_index | [-1,1] | Happy/sad lateralization |
| γ (Psych) | γ0 | perceived_felt_dissociation | [-1,1] | Brattico dissociation |
| | γ1 | emotion_clarity | [0,1] | Categorization confidence |
| | γ2 | emotional_complexity | [0,1] | Mixed emotion richness |
| | γ3 | valence_stability | [0,1] | Temporal emotional stability |
| | γ4 | valence_trajectory | [-1,1] | Emotional direction |
| δ (Valid) | δ0 | mode_accuracy | [0,1] | Mode detection correctness |
| | δ1 | picardy_response | [0,1] | Picardy third detection |
| | δ2 | srp_convergence | [0,1] | VMM↔SRP correlation |
| | δ3 | aac_convergence | [0,1] | VMM↔AAC correlation |
| | δ4 | paradox_of_sad_music | [0,1] | Sad+pleasure paradox |

---

## 7. Cross-Model Semantic Integration

### Combined Semantic Footprint (SRP + AAC + VMM)

```
COMPLETE MI SEMANTIC FOOTPRINT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Computation Layer:
  SRP  19D  +  AAC  14D  +  VMM  12D  =  45D

L³ Interpretation Layer:
  SRP  45D  +  AAC  26D  +  VMM  21D  =  92D

Total Semantic Footprint:
  SRP  64D  +  AAC  40D  +  VMM  33D  = 137D

Every one of these 137 dimensions has:
  ✓ A name (snake_case)
  ✓ A formula (deterministic)
  ✓ A brain region or pathway (neuroscience)
  ✓ A musical meaning (interpretable)
  ✓ Zero learnable parameters
```

### Key Cross-Model Semantic Signals

| Signal | VMM | SRP | AAC | What It Means |
|--------|-----|-----|-----|---------------|
| Happy major chorus | valence→+0.8, happy_path→HIGH | da_nacc→SPIKE, pleasure→PEAK | scr→↑, chills→PEAK | Full convergence: perceived happy + felt reward + body response |
| Sad minor passage | valence→-0.6, sad_path→HIGH | pleasure→moderate (if beautiful) | scr→moderate | Paradox active: sounds sad, feels good |
| Modulation point | certainty→DROPS, mode_shift→HIGH | prediction_error→SPIKE | scr→↑ (surprise) | All models detect the transition through different pathways |
| Picardy third | valence→jumps +, happy_path→SPIKE | da_nacc→SPIKE (surprise) | scr→↑ (arousal) | Emotional surprise: all models spike simultaneously |

---

## 8. References

1. Brattico, E. et al. (2011). *Frontiers in Psychology*, 2, 308.
2. Mitterschiffthaler, M.T. et al. (2007). *Human Brain Mapping*, 28(11), 1150-1162.
3. Fritz, T. et al. (2009). *Current Biology*, 19(7), 573-576.
4. Trost, W. et al. (2012). *Cerebral Cortex*, 22(12), 2769-2783.
5. Koelsch, S. et al. (2006). *Human Brain Mapping*, 27(3), 239-250.
6. Khalfa, S. et al. (2005). *NeuroReport*, 16(18), 1981-1984.
7. Green, A.C. et al. (2008). *NeuroReport*, 19(7), 711-715.
8. Sachs, M.E. et al. (2015). *SCAN*, 10(7), 988-994.
9. Gosselin, N. et al. (2005). *Brain*, 128(3), 628-640.

---

*See also: [L³-SRP-SEMANTIC-SPACE.md](L³-SRP-SEMANTIC-SPACE.md) | [L³-AAC-SEMANTIC-SPACE.md](L³-AAC-SEMANTIC-SPACE.md)*
*Model spec: [VMM.md](../C³/Models/ARU-α3-VMM/VMM.md)*
*Data flow: [08-VMM-DATA-FLOW.md](../General/08-VMM-DATA-FLOW.md)*
*Back to: [00-INDEX.md](../General/00-INDEX.md)*
