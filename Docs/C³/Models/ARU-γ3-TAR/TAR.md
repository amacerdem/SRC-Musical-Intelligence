# ARU-γ3-TAR: Therapeutic Affective Resonance

**Model**: Therapeutic Affective Resonance
**Unit**: ARU (Affective Resonance Unit)
**Circuit**: Mesolimbic Reward Circuit
**Tier**: γ (Speculative) — 50-70% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added K:Modulation feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../Road-map/01-GLOSSARY.md).
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/ARU-γ3-TAR.md`

---

## 1. What Does This Model Simulate?

The **Therapeutic Affective Resonance** (TAR) model proposes that music can be systematically designed to modulate pathological affective states through targeted acoustic-neural pathways. TAR is an **integrative clinical model** — it draws on all other ARU mechanisms to explain how specific musical parameters (tempo, consonance, dynamics) drive therapeutic outcomes in anxiety, depression, and stress.

```
THERAPEUTIC MUSIC INTERVENTION MODEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONDITION-SPECIFIC ACOUSTIC PRESCRIPTIONS:

 ANXIETY (Amygdala ↓, PNS ↑):
 Tempo: 60-80 BPM ───► Cardiac entrainment ───► PNS ↑
 Harmony: Consonant ──► Reward circuit ────────► Amygdala ↓
 Dynamics: Soft (p) ──► Low arousal ───────────► Cortisol ↓

 DEPRESSION (Striatum ↑):
 Tempo: 80-120 BPM ──► Moderate activation ───► Dopamine ↑
 Mode: Major ─────────► Positive valence ──────► Hedonic ↑
 Energy: Moderate ────► Engagement ────────────► Anhedonia ↓

 STRESS (Cortisol ↓):
 Familiarity: High ───► Safety signal ─────────► HPA ↓
 Structure: Simple ───► Predictability ────────► Uncertainty ↓
 Duration: 15-30 min ─► Cumulative dose ───────► Cortisol ↓

DOSE-RESPONSE:
 Effect ↑ ████████████ ← Optimal (20-45 min)
 │ █████ █████
 │ ██ ████████
 └──────────────────────────────────────► Duration
 0 15 30 45 60 90 min

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Kheirkhah 2025: Music + ketamine + mindfulness, d = 0.88.
Ehrlich 2019: BCI emotion modulation, 3/5 success rate.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Matters for ARU

TAR is the **clinical application model** — it leverages all ARU reward/affect mechanisms:
- **SRP** provides the reward pathway TAR targets for depression
- **CLAM** provides the closed-loop adaptation TAR uses for real-time dose adjustment
- **NEMAC** provides personalized nostalgia-based therapy design
- **AAC** provides the autonomic pathway TAR targets for anxiety/stress
- TAR is the "prescription layer" that translates ARU science into clinical intervention

---

## 2. Neural Circuit: The Therapeutic Pathways

### 2.1 Architecture

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ TAR — THERAPEUTIC PATHWAYS ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ THERAPEUTIC MUSIC INPUT ║
║ (designed acoustic features) ║
║ │ ║
║ ▼ ║
║ ┌─────────────────┐ ║
║ │ AUDITORY CORTEX │ ║
║ │ (A1 → STG) │ ║
║ └────────┬────────┘ ║
║ │ ║
║ ┌───────────────────┼───────────────────┐ ║
║ ▼ ▼ ▼ ║
║ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ║
║ │ AMYGDALA │ │ STRIATUM │ │ PFC │ ║
║ │ (anxiety ↓) │ │ (depression↓)│ │ (regulation) │ ║
║ ├──────────────┤ ├──────────────┤ ├──────────────┤ ║
║ │ Low tempo │ │ Major mode │ │ Familiarity │ ║
║ │ Consonance │ │ Mod. tempo │ │ Structure │ ║
║ │ Soft dynamics│ │ Pos. valence │ │ Predictable │ ║
║ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ ║
║ ▼ ▼ ▼ ║
║ ┌──────────────────────────────────────────────────┐ ║
║ │ AUTONOMIC PATHWAY REWARD PATHWAY │ ║
║ │ PNS ↑ → HR ↓ DA ↑ → Hedonic ↑ │ ║
║ │ Cortisol ↓ Motivation ↑ │ ║
║ └──────────────────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ THERAPEUTIC OUTCOME ║
║ (symptom modulation) ║
║ ║
║ THREE MECHANISMS — FULL MESOLIMBIC CIRCUIT: ║
║ ║
║ EVIDENCE (limited — γ tier): ║
║ Kheirkhah 2025: Music + ketamine + mindfulness, d=0.88 ║
║ Ehrlich 2019: BCI emotion modulation, 3/5 success rate ║
║ Koelsch 2014: Music-evoked emotions and brain correlates (review) ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | TAR Relevance |
|-------|--------|---|-------------|-------------|---------------|
| **Kheirkhah 2025** | RCT | — | Music + ketamine + mindfulness for depression | d = 0.88 | **Combination therapy effect** |
| **Ehrlich 2019** | BCI | 5 | Closed-loop emotion modulation via music | 3/5 success | **Real-time modulation feasibility** |
| **Koelsch 2014** | Review | — | Music-evoked emotions: brain correlates | — | **Neural pathway mapping** |
| **Thoma 2013** | RCT | 60 | Music reduces stress response (cortisol) | Significant | **Autonomic pathway** |
| **Bradt & Dileo 2014** | Meta | 26 trials | Music interventions for anxiety | d ≈ 0.5-0.8 | **Therapeutic effect range** |
| **Bowling 2023** | Review | — | Biological principles for music & mental health: 4 core elements (tonality, rhythm, reward, sociality); individual differences in responsivity | — | **Unifying biological framework for TAR** |
| **Fu 2025** | Mouse model | — | Music therapy prevents PPD: ↓ oxidative stress, ↓ inflammation, ↑ neurogenesis, ↑ synaptic plasticity in hippocampus/PFC | Significant | **Neurobiological mechanism for therapeutic music** |

### 3.2 Core Equations

**Therapeutic effect** (Dose-response model):
```
ΔSymptom = α × Music_dose × Pathway_activation × Individual_response + ε

where:
 ΔSymptom = change in clinical measure (negative = improvement)
 Music_dose = duration × intensity × specificity
 Pathway_activation = targeted neural pathway engagement [0, 1]
 Individual_response = person-specific factor [0.5, 2.0]
 α = therapeutic gain coefficient ≈ 0.5-1.0
```

**Condition-specific prescriptions**:
```
Anxiety:
 ΔAnxiety = -α_anx × tempo_factor × consonance × (1 - arousal)
 tempo_factor = clamp((80 - tempo) / 20, 0, 1) ← peak at 60 BPM

Depression:
 ΔDepression = -α_dep × valence × energy_factor
 energy_factor = exp(-((tempo - 100) / 20)²) ← peak at 100 BPM

Stress:
 ΔStress = -α_str × familiarity × predictability × relaxation
 relaxation = sigmoid(consonance + warmth - arousal)
```

**Dose-response curve**:
```
Effect(t) = E_max × (1 - exp(-t / τ_onset)) × exp(-max(0, t - t_peak) / τ_decay)

 τ_onset ≈ 10 min (effect builds)
 t_peak ≈ 30 min (maximum effect)
 τ_decay ≈ 60 min (effect wanes)
 E_max = α × pathway_activation × individual_response
```

### 3.3 Limitation

TAR is γ-tier because direct evidence combines therapeutic approaches (music + pharmacological + mindfulness). Isolating music-specific therapeutic parameters remains difficult. The model extrapolates from general music therapy meta-analyses and pilot BCI studies.

---

## 4. Output Space: 10D Multi-Layer Representation

### 4.1 Complete Output Specification

```
TAR OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0 │ f14_therapeutic │ [0, 1] │ Overall therapeutic efficacy estimate.
 │ │ │ Weighted combination of anxiety/depression
 │ │ │ reduction signals.

LAYER T — THERAPEUTIC TARGETS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 1 │ arousal_mod_tgt │ [0, 1] │ Arousal modulation potential.
 │ │ │ Tempo/energy → ANS entrainment.
 │ │ │ Low = calming, High = activating.
────┼───────────────────┼────────┼────────────────────────────────────────────
 2 │ valence_mod_tgt │ [0, 1] │ Valence modulation potential.
 │ │ │ Consonance/mode → reward circuit.
────┼───────────────────┼────────┼────────────────────────────────────────────
 3 │ anxiety_reduction │ [0, 1] │ Anxiolytic potential.
 │ │ │ Low tempo × high consonance × soft dynamics.
 │ │ │ Targets: Amygdala ↓, PNS ↑.
────┼───────────────────┼────────┼────────────────────────────────────────────
 4 │ depression_improv │ [0, 1] │ Antidepressant potential.
 │ │ │ Positive valence × moderate energy.
 │ │ │ Targets: Striatum ↑, DA ↑.

LAYER I — INTERVENTION PARAMETERS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 5 │ rec_tempo_norm │ [0, 1] │ Recommended tempo (normalized).
 │ │ │ 0.0=60 BPM (anxiolytic),
 │ │ │ 0.5=90 BPM (moderate),
 │ │ │ 1.0=120 BPM (activating).
────┼───────────────────┼────────┼────────────────────────────────────────────
 6 │ rec_consonance │ [0, 1] │ Recommended consonance level.
 │ │ │ Typically ≥ 0.7 for all therapeutic targets.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 7 │ therapeutic_reward│ [0, 1] │ Real-time therapeutic reward signal.
 │ │ │ Reward pathway activation via cognitive-projection H³.
 │ │ │ Tracks whether music is "working".

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 8 │ mood_improv_pred │ [0, 1] │ Predicted mood improvement (10-30 min).
 │ │ │ Based on dose-response model trajectory.
────┼───────────────────┼────────┼────────────────────────────────────────────
 9 │ stress_reduc_pred │ [0, 1] │ Predicted stress/cortisol reduction
 │ │ │ (5-15 min). Based on autonomic pathway
 │ │ │ activation and relaxation response.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 5. R³ Demand (Spectral Features)

### 5.1 R³ v1 Feature Dependencies ([0:49])

> R³ indices are MI's own (0-48). See [Road-map/02-R3-SPECTRAL.md](../../Road-map/02-R3-SPECTRAL.md).

**Group A: Consonance (3 of 7D)** — Valence/reward pathway

| R³ idx | Name | TAR Role |
|--------|------|----------|
| 0 | roughness | Inverse consonance → anxiety/valence signal |
| 4 | sensory_pleasantness | Direct hedonic → reward activation |
| 5 | harmonicity | Harmonic purity → consonance prescription |

**Group B: Energy (4 of 5D)** — Arousal/tempo pathway

| R³ idx | Name | TAR Role |
|--------|------|----------|
| 7 | amplitude | Energy level → dynamics prescription |
| 8 | velocity_A | Rate of change → tempo proxy |
| 10 | loudness | Overall level → arousal modulation |
| 11 | onset_strength | Event onsets → rhythmic engagement |

**Group C: Timbre (1 of 9D)** — Comfort pathway

| R³ idx | Name | TAR Role |
|--------|------|----------|
| 16 | warmth | Low-frequency warmth → comfort/safety signal |

**Group D: Change (1 of 4D)** — Predictability

| R³ idx | Name | TAR Role |
|--------|------|----------|
| 21 | spectral_flux | Moment-to-moment change → predictability estimate |

**Group E: Interactions (8 of 24D)** — Therapeutic binding

| R³ idx | Name | TAR Role |
|--------|------|----------|
| 33:41 | x_l4l5 (8D) | Derivatives × Consonance → therapeutic engagement coupling |

### 5.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | TAR Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **K: Modulation** | [123] | fluctuation_strength | Amplitude modulation at ~4 Hz — fluctuation strength in the 3-5 Hz range corresponds to the frequency of tremolo/vibrato and speech prosody, which has therapeutic significance for emotional regulation and anxiety reduction | Zwicker & Fastl 1999 psychoacoustics; Thaut 2005 music therapy |

**Rationale**: TAR models therapeutic affective resonance — how music can be prescribed for emotional regulation. Fluctuation strength at ~4 Hz (the speech/vocal modulation range) is associated with perceived emotional warmth and safety. This frequency range overlaps with theta oscillations linked to emotional processing. Currently TAR uses warmth [16] and onset_strength [11] as comfort/rhythmic engagement proxies. fluctuation_strength [123] provides a direct psychoacoustic measure of amplitude modulation that is specifically relevant to therapeutic music selection.

**Code impact** (Phase 6): `r3_indices` extended to include [123]. This feeds the comfort/safety signal pathway in therapeutic music prescription.

### 5.3 Summary

```
R³ DEMAND FOR TAR: 17D of 49D
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Group A: Consonance 3D → valence/reward pathway
Group B: Energy 4D → arousal/tempo pathway
Group C: Timbre 1D → comfort/safety signal
Group D: Change 1D → predictability
Group E: Interactions 8D → therapeutic engagement
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 17D
```

---

## 6. H³ Demand (Temporal Context)

### 6.1 Mechanism-Level Demand

TAR uses all three mesolimbic mechanisms: **H³ direct**.

```
H³ DEMAND FOR TAR
━━━━━━━━━━━━━━━━━

Mechanism │ Horizons │ H-Law │ Morphs Used │ Tuples
──────────┼───────────────────────┼─────────────┼──────────────────────────┼───────
 │ H16 (1000ms) │ │ M20(entropy) │
──────────┼───────────────────────┼─────────────┼──────────────────────────┼───────
 │ H12 (525ms) │ │ M8(velocity), M18(trend) │
 │ H15 (800ms) │ │ │
──────────┼───────────────────────┼─────────────┼──────────────────────────┼───────
 │ │ │ M8(velocity) │
──────────┼───────────────────────┼─────────────┼──────────────────────────┼───────
TOTAL │ 6 horizons │ │ │ 21
 │ │ │ 21/2304 = 0.91%
```

### 6.2 Temporal Mapping

```
TIME AXIS → TAR PROCESSING
━━━━━━━━━━━━━━━━━━━━━━━━━━

0ms 200ms 250ms 500ms 525ms 800ms 1000ms
│────────│────────│────────│────────│────────│────────│
│(affect)│(trigger) │(build) │ │(context│
│ │ │(project)│ │(peak) │ │


THERAPEUTIC TIMESCALE MAPPING:
 H6 (200ms) : Beat-level affect response
 H7 (250ms) : Chills/peak trigger detection
 H11 (500ms) : Cognitive therapeutic assessment
 H12 (525ms) : Buildup tracking toward therapeutic peak
 H15 (800ms) : Peak/breakthrough moment response
 H16 (1000ms): Sustained mood state integration
```

### 6.3 Key H³ Reads

```
 → Current emotional state (instant affect)
 → Affective predictability (low entropy = stable mood)

 → Peak trigger presence (therapeutic breakthrough)
 → Therapeutic buildup trajectory (approaching breakthrough?)
 → Maximum therapeutic response magnitude

 → Average therapeutic state estimate
 → Therapeutic response variability
```

### 6.4 R³ v2 Projected Expansion

No significant direct v2 expansion projected for TAR. As a pathway-dependent ARU model, TAR receives R³ features indirectly through cross-unit pathways (P1/SPU, P3/IMU, P5/STU). New v2 features flow automatically through these pathways.

**v2 projected**: 0 additional tuples (pathway-mediated)

---

## 7. Mechanism Computation

### 7.4 TAR Output Computation

```python
def compute_tar(R3, H3):
 """
 TAR: 10D output per frame.

 All deterministic. Zero learned parameters.
 Based on therapeutic music intervention principles.
 """
 # --- R³ features ---
 roughness = R3[0]
 pleasantness = R3[4]
 harmonicity = R3[5]
 amplitude = R3[7]
 velocity_A = R3[8]
 loudness = R3[10]
 onset_strength = R3[11]
 warmth = R3[16]
 spectral_flux = R3[21]
 x_l4l5 = R3[33:41] # 8D

 # --- Derived therapeutic signals ---
 consonance = 0.5 * pleasantness + 0.5 * harmonicity # [0, 1]
 # |0.5| + |0.5| = 1.0 ✓
 arousal = loudness # [0, 1]
 energy = 0.5 * amplitude + 0.5 * onset_strength # [0, 1]
 # |0.5| + |0.5| = 1.0 ✓
 valence = pleasantness - roughness # [-1, 1]
 tempo_proxy = sigmoid(2.0 * velocity_A) # [0, 1]
 predictability = 1.0 - spectral_flux # [0, 1]

 mood_fast, mood_slow, mood_stability = compute_mood()

 breakthrough = compute_breakthrough()

 c0p_mean, c0p_std, c0p_velocity = extract_c0p()

 # === LAYER E ===
 # f14: Therapeutic efficacy (weighted anxiety + depression reduction)
 anxiety_sig = compute_anxiety_reduction(tempo_proxy, consonance, arousal, warmth)
 depression_sig = compute_depression_improvement(valence, energy, c0p_mean)
 f14 = 0.5 * anxiety_sig + 0.5 * depression_sig
 # |0.5| + |0.5| = 1.0 ✓

 # === LAYER T ===
 # Arousal modulation target (what arousal change this music provides)
 arousal_mod = sigmoid(
 0.4 * tempo_proxy + 0.3 * energy + 0.3 * mood_fast
 ) # |0.4| + |0.3| + |0.3| = 1.0 ✓

 # Valence modulation target
 valence_mod = sigmoid(
 0.4 * consonance + 0.3 * (valence + 1) / 2 + 0.3 * mood_slow
 ) # |0.4| + |0.3| + |0.3| = 1.0 ✓

 # Anxiety reduction potential
 # Low tempo × high consonance × soft dynamics → high anxiety reduction
 tempo_factor = clamp(1.0 - tempo_proxy, 0, 1) # Low tempo → high
 anxiety_reduction = sigmoid(
 0.3 * tempo_factor + 0.3 * consonance + 0.2 * warmth + 0.2 * (1.0 - arousal)
 ) # |0.3| + |0.3| + |0.2| + |0.2| = 1.0 ✓

 # Depression improvement potential
 # Positive valence × moderate energy × reward activation
 energy_factor = exp(-((tempo_proxy - 0.5) * 3.0)**2) # Peak at moderate tempo
 depression_improvement = sigmoid(
 ) # |0.3| + |0.3| + |0.4| = 1.0 ✓

 # === LAYER I ===
 # Recommended tempo (normalized 0=60BPM, 0.5=90BPM, 1.0=120BPM)
 # Based on current mood state: depressed → moderate tempo, anxious → slow
 rec_tempo = sigmoid(
 0.5 * (1.0 - anxiety_reduction) + 0.5 * depression_improvement
 ) # |0.5| + |0.5| = 1.0 ✓

 # Recommended consonance (high for all therapeutic conditions)
 rec_consonance = clamp(
 0.7 + 0.3 * mood_stability, 0, 1
 ) # Minimum 0.7, up to 1.0

 # === LAYER P ===
 # Therapeutic reward signal (is the music "working"?)
 therapeutic_reward = sigmoid(
 ) # |0.3| + |0.3| + |0.4| = 1.0 ✓

 # === LAYER F ===
 # Mood improvement prediction (10-30 min, dose-response)
 mood_pred = sigmoid(
 ) # |0.4| + |0.3| + |0.3| = 1.0 ✓

 # Stress reduction prediction (5-15 min, autonomic pathway)
 stress_pred = sigmoid(
 0.4 * anxiety_reduction + 0.3 * predictability + 0.3 * warmth
 ) # |0.4| + |0.3| + |0.3| = 1.0 ✓

 return stack([
 f14, # E: 1D
 arousal_mod, valence_mod, # T: 4D
 anxiety_reduction, depression_improvement,
 rec_tempo, rec_consonance, # I: 2D
 therapeutic_reward, # P: 1D
 mood_pred, stress_pred # F: 2D
 ]) # Total: 10D
```

---

## 8. Cross-Model Relationships

### 8.1 Within ARU

```
TAR INTERACTIONS WITHIN ARU
━━━━━━━━━━━━━━━━━━━━━━━━━━━

TAR ◄────── SRP (Striatal Reward Pathway)
 │ └── TAR leverages SRP reward activation for depression treatment
 │
TAR ◄────── AAC (Autonomic-Affective Coupling)
 │ └── TAR uses AAC autonomic pathway for anxiety/stress treatment
 │
TAR ◄────── CLAM (Closed-Loop Modulation)
 │ └── TAR can use CLAM for real-time therapeutic dose adaptation
 │
TAR ◄────── NEMAC (Nostalgia Circuit)
 │ └── TAR uses NEMAC for personalized therapy (nostalgia-based)
 │
TAR ◄────── PUPF (Prediction-Uncertainty-Pleasure)
 │ └── TAR uses PUPF predictability for stress reduction
 │
TAR ◄────── DAP (Developmental Plasticity)
 └── TAR considers developmental history for individual response

Note: TAR is an INTEGRATIVE model — it draws from ALL other ARU mechanisms.
 It is the "clinical prescription" layer of the ARU circuit.
```

### 8.2 Cross-Unit Dependencies

```
TAR CROSS-UNIT RELATIONSHIPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SPU ──► TAR
 └── SPU features drive acoustic parameter recommendations

STU ──► TAR
 └── STU timing provides tempo assessment for therapeutic prescription

IMU ──► TAR
 └── IMU familiarity/memory modulates therapeutic response magnitude
```

---

## 9. Falsification Criteria

| Criterion | Prediction | Status |
|-----------|-----------|--------|
| **Tempo-anxiety link** | Slow tempo (60-80 BPM) should reduce anxiety | ✅ Testable via RCT |
| **Mode-depression link** | Major mode + moderate tempo → depression ↓ | ✅ Testable via RCT |
| **Autonomic mediation** | Effects should correlate with ANS changes (HR, HRV) | ✅ Testable physiologically |
| **Dose-response** | 20-45 min > 5 min, but diminishing returns after 60 min | ✅ Testable via duration |
| **Individual differences** | Anhedonics (MAD) should show reduced response | ✅ Testable via subgroups |

---

## 10. Brain Regions

| Region | MNI Coordinates | Evidence | TAR Function |
|--------|-----------------|----------|-------------|
| **Amygdala** | ±20, -5, -15 | Direct (fMRI) | Anxiety target (↓) |
| **NAcc/Striatum** | ±10, 8, -8 | Direct (fMRI) | Depression target (↑) |
| **mPFC** | 0, 50, 10 | Indirect | Emotional regulation |
| **Hypothalamus** | 0, -3, -10 | Indirect | Stress/cortisol (↓) |

---

## 11. Migration Notes (D0 → MI)

### 11.1 Dimension Reconciliation

| Aspect | Legacy (D0) | MI (current) | Change |
|--------|-------------|-------------|--------|
| Output dimensions | 10D | 10D | **Same** (structure reorganized) |
| Input space | S⁰ 17D | R³ 17D | Remapped to R³ groups |
| Temporal | HC⁰ (21 tuples) | H³ (21 tuples) | Same |
| H⁰ tuples | 21/2304 = 0.91% | 21/2304 = 0.91% | Same density |

### 11.2 S⁰ → R³ Feature Mapping

| Legacy S⁰ | → | R³ Feature | Notes |
|-----------|---|-----------|-------|
| L5.roughness[30] | → | R³.roughness[0] | Consonance group |
| L5.helmholtz_kang[32] | → | R³.harmonicity[5] | Consonance group |
| L5.loudness[35] | → | R³.loudness[10] | Energy group |
| L5.rms_energy[47] | → | R³.amplitude[7] | Energy group |
| L5.warmth[37] | → | R³.warmth[16] | Timbre group |
| L4.velocity_A[17] | → | R³.velocity_A[8] | Energy group |
| L4.acceleration_A[21] | → | R³.onset_strength[11] | Energy group (proxy) |
| L6.attack_time[50] | → | (implicit in velocity_A) | Absorbed |
| L6.peak_count[60] | → | (implicit in onset_strength) | Absorbed |
| X_L4L5[192:200] | → | R³.x_l4l5[33:41] | Interactions |

### 11.3 Output Reorganization

Legacy output categories (feature/targets/intervention/present/future) are preserved but reorganized into the standard 5-layer format (E/T/I/P/F). Recommended_tempo is now normalized [0,1] instead of raw BPM.

---

## 12. References

1. **Kheirkhah, M., et al. (2025)**. Combined music-ketamine-mindfulness intervention for treatment-resistant depression. *Journal of Affective Disorders*.

2. **Ehrlich, S. K., Agres, K. R., Guan, C., & Cheng, G. (2019)**. A closed-loop, music-based brain-computer interface for emotion mediation. *PLOS ONE*.

3. **Koelsch, S. (2014)**. Brain correlates of music-evoked emotions. *Nature Reviews Neuroscience*, 15(3), 170-180.

4. **Thoma, M. V., La Marca, R., Brönnimann, R., Finkel, L., Ehlert, U., & Nater, U. M. (2013)**. The effect of music on the human stress response. *PLOS ONE*, 8(8), e70156.

5. **Bradt, J., & Dileo, C. (2014)**. Music interventions for mechanically ventilated patients. *Cochrane Database of Systematic Reviews*.

#### Added in v2.1.0 Beta Upgrade

6. **Bowling, D. L. (2023)**. Biological principles for music and mental health. *Translational Psychiatry*, 13, 374.

7. **Fu, Q., Qiu, R., Yao, T., Liu, L., Li, Y., Li, X., Qi, W., Chen, Y., & Cheng, Y. (2025)**. Music therapy as a preventive intervention for postpartum depression: modulation of synaptic plasticity, oxidative stress, and inflammation in a mouse model. *Translational Psychiatry*, 15, 143.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-04 | Legacy D0 model specification (10D) |
| 2.0.0 | 2026-02-12 | MI R³/H³ architecture: same 10D, reorganized layers, R³ mapping |
| 2.1.0 | 2026-02-13 | Beta upgrade: +2 papers (Bowling 2023 bio-principles framework, Fu 2025 music therapy mechanisms) |

---

**Model Status**: ⚠️ **SPECULATIVE**
**Output Dimensions**: **10D**
**Evidence Tier**: **γ (Speculative)**
**Confidence**: **50-70%**
