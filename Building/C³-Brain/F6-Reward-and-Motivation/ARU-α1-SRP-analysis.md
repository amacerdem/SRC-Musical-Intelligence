# ARU-α1-SRP — Functional Architecture Analysis

**Model**: Striatal Reward Pathway
**Unit Origin**: ARU (Affective Resonance Unit)
**Tier**: α (Mechanistic) — >90% confidence
**Output**: 19D (6 layers: N/C/P/T/M/F)
**H³ Demand**: ~124 tuples (5.4% of 2304)
**R³ Demand**: 49D (Groups A+B+C+D+E) — NOTE: E dissolved in v1.0.0, now C³ internal

---

## 1. Function Assignment

**Primary Function**: F6 Reward & Motivation (PURE — single-function model)

SRP is the foundational model of F6. Per the 96-model functional brain map, it is a **pure single-function** model — no secondary Function assignments.

However, SRP's outputs have downstream impact on:
- **RAM**: Region activations (wanting→caudate, liking→NAcc, tension→IFG)
- **Reward Formula**: SRP hedonic pathway feeds terminal reward aggregation
- **Salience (F3)**: SRP.tension contributes to relay-based salience signal
- **Familiarity (F4)**: SRP.reward_forecast contributes to familiarity modulation

---

## 2. SRP 19D → F6 Belief Mapping

### 2.1 Direct Belief Mappings (11 of 19 → F6 beliefs)

| SRP Output Idx | SRP Dimension | F6 Belief | Category | τ | Mapping |
|:-:|---|---|:-:|:-:|---|
| 6 | `wanting` | `wanting` | **Core** | 0.6 | Direct: σ(β₂ × da_caudate), β₂=0.71 |
| 7 | `liking` | `liking` | **Core** | 0.65 | Direct: σ(β₁ × da_nacc), β₁=0.84 |
| 8 | `pleasure` | `pleasure` | **Core** | 0.7 | Direct: clamp(β₁×da_nacc + β₂×da_caudate) |
| 5 | `prediction_error` | `prediction_error` | **Core** | 0.5 | Direct: Schultz RPE δ = R + γV(t+1) − V(t) |
| 9 | `tension` | `tension` | **Core** | 0.55 | Direct: Huron T preparatory arousal |
| 10 | `prediction_match` | `prediction_match` | **Appraisal** | — | Direct: Huron P confirmation/violation |
| 15 | `peak_detection` | `peak_detection` | **Appraisal** | — | Direct: Chill trigger (Sloboda 1991 features) |
| 13 | `harmonic_tension` | `harmonic_tension` | **Appraisal** | — | Direct: Tonal distance from tonic |
| 16 | `reward_forecast` | `reward_forecast` | **Anticipation** | — | Direct: Expected reward 2-8s ahead |
| 17 | `chills_proximity` | `chills_proximity` | **Anticipation** | — | Direct: Proximity to chills, refractory ~10-30s |
| 18 | `resolution_expect` | `resolution_expectation` | **Anticipation** | — | Direct: Harmonic resolution expected 0.5-2s |

### 2.2 Internal Intermediates (8 of 19 — NOT beliefs, mechanism internals)

| SRP Output Idx | SRP Dimension | Range | Role | Where Consumed |
|:-:|---|:-:|---|---|
| 0 | `da_caudate` | [0,1] | Dorsal striatal DA ramp (anticipatory) | Feeds wanting, pleasure. **NOTE**: DAED model "owns" the F6 Appraisal belief `da_caudate`. SRP computes this as mechanism intermediate; DAED refines it. |
| 1 | `da_nacc` | [0,1] | Ventral striatal DA burst (consummatory) | Feeds liking, pleasure. **NOTE**: DAED model "owns" F6 Appraisal belief `da_nacc`. |
| 2 | `opioid_proxy` | [0,1] | μ-opioid receptor activation proxy | Feeds liking (hedonic component). Internal to SRP mechanism. |
| 3 | `vta_drive` | [0,1] | VTA→Striatum pathway activation | σ(0.5×da_caudate + 0.5×da_nacc). Internal circuit. |
| 4 | `stg_nacc_coupling` | [0,1] | Auditory cortex ↔ NAcc connectivity | Critical individual-difference variable. Internal. |
| 11 | `reaction` | [0,1] | Huron R: reflexive brainstem response ~150ms | Internal ITPRA component. |
| 12 | `appraisal` | [-1,1] | Huron A: conscious evaluation 0.5-2s after | Internal ITPRA component. |
| 14 | `dynamic_intensity` | [0,1] | Energy trajectory (crescendo/decrescendo) | Internal musical meaning signal. |

### 2.3 Belief Ownership Summary

```
SRP OWNS (11 beliefs in F6):
  Core (5):        wanting, liking, pleasure, prediction_error, tension
  Appraisal (3):   prediction_match, peak_detection, harmonic_tension
  Anticipation (3): reward_forecast, chills_proximity, resolution_expectation

SRP DOES NOT OWN (remaining F6 beliefs — owned by DAED):
  Appraisal (4):   dissociation_index, temporal_phase, da_caudate, da_nacc
  Anticipation (1): wanting_ramp

F6 Total: 16 beliefs (11 SRP + 5 DAED)
```

---

## 3. Mechanisms & Scientific Basis

### 3.1 Three Dissociable Reward Systems

SRP implements Berridge & Robinson (1993, 2003, 2016): wanting, liking, and learning are **dissociable** neurochemical systems.

| System | Neurotransmitter | Brain Region | Timing | SRP Belief |
|--------|-----------------|--------------|--------|------------|
| **Wanting** (Incentive Salience) | Dopamine | Caudate (dorsal striatum) | 2-30s BEFORE event | `wanting` (C, τ=0.6) |
| **Liking** (Hedonic Impact) | μ-Opioid + DA | NAcc shell (ventral striatum) | AT event, 1-5s burst | `liking` (C, τ=0.65) |
| **Learning** (Prediction Error) | Dopamine (phasic) | VTA → NAcc/Caudate | ~50-110ms after event | `prediction_error` (C, τ=0.5) |

Key evidence:
- Salimpoor 2011: β₁=0.84 (NAcc↔pleasure), β₂=0.71 (Caudate↔chills)
- Ferreri 2019: Levodopa↑ both wanting AND liking (causal pharmacological)
- Martinez-Molina 2016: Musical anhedonia = NAcc-STG disconnection

### 3.2 ITPRA Temporal Framework (Huron 2006)

SRP implements 5 temporal response systems:

| System | Timing | SRP Dimension | Belief? |
|--------|--------|---------------|---------|
| **I**magination | Seconds–minutes before | reward_forecast | Yes (N) |
| **T**ension | Seconds before | tension | Yes (C, τ=0.55) |
| **P**rediction | ~130-250ms before | prediction_match | Yes (A) |
| **R**eaction | ~150ms after | reaction | No (internal) |
| **A**ppraisal | 0.5-2s after | appraisal | No (internal) |

### 3.3 Key Mechanism Formulas

```
# Neurochemical layer
opioid_proxy = σ(0.4×consonance_mean + 0.3×resolution_signal + 0.3×smoothness)
da_caudate   = quasi-hyperbolic ramp toward expected reward (Howe 2013)
da_nacc      = phasic burst at peak moment (Salimpoor 2011)

# Psychological layer
wanting  = σ(0.71 × da_caudate)      # Salimpoor β₂
liking   = σ(0.84 × da_nacc)          # Salimpoor β₁
pleasure = clamp(0.84×da_nacc + 0.71×da_caudate, 0, 1)

# Musical meaning layer
harmonic_tension = σ(0.5×roughness_trend + 0.3×inv_consonance + 0.2×entropy)
dynamic_intensity = σ(0.7×energy_velocity + 0.3×energy_acceleration)

# Forecast layer
chills_proximity: refractory ~10-30s (Grewe 2009), threshold crossing DA+opioid+ANS
```

### 3.4 Uncertainty × Surprise Interaction (Cheung 2019)

Pleasure is NOT simply "high surprise = good." Two optimal zones:
1. Low uncertainty + High surprise = "I thought I knew, but WOW"
2. High uncertainty + Low surprise = "I was confused, but it resolved"

Brain mapping: Amygdala + Hippocampus + Auditory cortex (interaction), NAcc + Caudate + pre-SMA (uncertainty alone).

---

## 4. Cross-Model Dependencies

### 4.1 SRP Reads From (upstream dependencies)

SRP is a convergence hub. Its R³ demand spans 4 groups (49D in legacy, 25D in v1.0.0 after E/I dissolution):

| Source | What SRP Reads | Purpose |
|--------|---------------|---------|
| R³ Group A (Consonance 7D) | roughness, sethares, helmholtz, stumpf, pleasantness, inharmonicity, harmonic_deviation | opioid_proxy, harmonic_tension |
| R³ Group B (Energy 5D) | amplitude, velocity_A, acceleration_A, loudness, onset_strength | dynamic_intensity, tension, peak_detection |
| R³ Group C (Timbre 9D) | warmth, sharpness, tonalness, clarity, smoothness, autocorrelation, tristimulus1-3 | opioid_proxy (spectral quality) |
| R³ Group D (Change 4D) | spectral_flux, entropy, flatness, concentration | prediction_error, tension |
| H³ (124 tuples) | M0, M2, M4, M5, M8, M9, M10, M11, M14, M15, M17, M18, M19, M20, M21, M22 across 7 horizons | Multi-scale temporal context |

### 4.2 SRP is Read By (downstream consumers in v4.0)

| Consumer | What It Reads | Purpose |
|----------|--------------|---------|
| DAED (RPU) | SRP.wanting, SRP.liking | Cross-relay: caudate/nacc_activation refinement |
| Reward Aggregator | SRP.wanting, SRP.liking, SRP.pleasure, SRP.tension | SRP hedonic pathway (w_srp × reward_srp) |
| Reward Aggregator | SRP.chills_proximity, SRP.resolution_expect, SRP.reward_forecast | Chills multiplier, resolution amplifier, SRP confidence |
| Salience (F3) | SRP.tension | Relay-based salience signal component |
| RAM | SRP.wanting, SRP.liking, SRP.tension | Region activations (caudate, NAcc, IFG) |

### 4.3 Cross-Unit Reads (Legacy SRP Document)

The original SRP document specifies reads from 5 units:
- SPU (consonance, pitch)
- STU (temporal context)
- IMU (memory, familiarity)
- NDU (onset, contour)
- PCU (prediction hierarchy)

In v3.0+ Function architecture, these become cross-Function reads mediated by the phase DAG:
- F1 (harmonic_stability, pitch_prominence) → F6 observes consonance state
- F7 (period_entrainment, context_depth) → F6 observes rhythmic context
- F2 (prediction_hierarchy) → F6 reads prediction state for RPE computation
- F4 (autobiographical_retrieval) → F6 reads familiarity for inverted-U modulation
- F3 (beat_entrainment) → F6 reads salience for reward gating

---

## 5. H³ Temporal Demand

### 5.1 Temporal Layers (4 nested scales)

| Layer | Horizons | Duration | SRP Role |
|-------|----------|----------|----------|
| **Beat** (Immediate) | H6-H16 | 200ms–1s | prediction_error, reaction, peak_detection |
| **Phrase** | H18-H20 | 2s–5s | tension, harmonic_tension, dynamic_intensity |
| **Section** | H22-H24 | 15s–36s | da_caudate ramp, wanting, reward_forecast |
| **Structural** (optional) | H26-H28 | 200s–414s | Narrative arc (nice-to-have) |

### 5.2 Demand Summary

```
Total H³ scalars: ~124 (of 2304 theoretical = 5.4%)
Unique horizons used: 7 (of 32)
Unique morph types: 22 (of 24)
Law: L0 only (causal, backward-looking)
```

SRP is the **largest H³ consumer** of all 96 models (~124 tuples). This is because reward computation requires multi-scale temporal context from beat-level to structural-level.

---

## 6. v4.0 Kernel Relay Integration

### 6.1 SRP Relay Wrapper (ARU)

The SRP relay wrapper exports the following fields to the scheduler:

```
SRP relay fields (consumed by beliefs in v4.0):
  wanting          → F6 Core Belief wanting (observe)
  liking           → F6 Core Belief liking (observe)
  pleasure         → F6 Core Belief pleasure + Reward hedonic pathway
  tension          → F6 Core Belief tension + Salience relay signal
  reward_forecast  → Reward SRP confidence (srp_confidence = 0.5 + 0.5×forecast)
  chills_proximity → Reward chills multiplier (1 + 0.5×chills_proximity)
  resolution_expect → Reward resolution amplifier (0.8 + 0.4×resolution)
```

### 6.2 Reward Formula — SRP Hedonic Pathway

```
srp_hedonic   = 0.30×wanting + 0.30×liking + 0.25×pleasure + 0.15×tension
chills_mult   = 1 + 0.5 × chills_proximity
resolution_amp = 0.8 + 0.4 × resolution_expect
reward_srp    = salience × srp_hedonic × chills_mult × resolution_amp

srp_confidence = 0.5 + 0.5 × reward_forecast
w_srp          = 0.25 × srp_confidence              # range [0.125, 0.25]

reward = (1 − w_srp) × reward_pe + w_srp × reward_srp
```

### 6.3 RAM Region Links

| SRP Output | Region | Weight | Role |
|------------|--------|--------|------|
| wanting | caudate | 0.70 | Anticipatory DA ramp |
| liking | NAcc | 0.80 | Consummatory DA + opioid |
| tension | IFG | 0.60 | Preparatory arousal |

---

## 7. Phase Schedule Position

SRP operates in **Phase 5 (Terminal)** — the last computational phase.

```
Phase 0: F1(BCH→harmonic_stability) + F7(PEOM→period_entrainment)
Phase 1: F2(HTP→prediction_hierarchy) + F3(SNEM→beat_entrainment)
Phase 2: F4(MEAMN→familiarity) + F5(VMM→emotion)
Phase 3: F8(learning) + F9(social)
Phase 4: PE + Precision computation for ALL 36 Core Beliefs
Phase 5: F6(SRP→wanting, liking, pleasure, tension, prediction_error)  ← TERMINAL
         → Reward aggregation (all 36 PEs + SRP hedonic + familiarity + DA)
         → RAM assembly → Output
```

F6 is terminal because reward computation requires PEs from ALL other Functions.

---

## 8. Functional Architecture Decisions

### 8.1 What Maps Where

| SRP Layer | Dimensions | → F6 Beliefs | → Internal Only |
|-----------|:----------:|:------------:|:---------------:|
| N (Neurochemical) | 3 | 0 | 3 (da_caudate, da_nacc, opioid_proxy) |
| C (Circuit) | 3 | 1 (prediction_error) | 2 (vta_drive, stg_nacc_coupling) |
| P (Psychological) | 3 | 3 (wanting, liking, pleasure) | 0 |
| T (Temporal/ITPRA) | 4 | 2 (tension, prediction_match) | 2 (reaction, appraisal) |
| M (Musical) | 3 | 2 (harmonic_tension, peak_detection) | 1 (dynamic_intensity) |
| F (Forecast) | 3 | 3 (all three) | 0 |
| **Total** | **19** | **11** | **8** |

### 8.2 Unresolved Design Questions

1. **da_caudate/da_nacc overlap**: Both SRP and DAED compute these. SRP uses them as intermediates for wanting/liking; DAED "owns" them as F6 Appraisal beliefs. The current kernel avoids double-computation — SRP intermediates feed SRP's own beliefs, while DAED independently computes refined versions using cross-relay data (BCH+MEAMN). No conflict: different computations, same variable name.

2. **reaction and appraisal**: Huron R and A responses are SRP outputs but not F6 beliefs. Options:
   - (a) Keep as internal SRP intermediates (current approach)
   - (b) Promote to F6 Appraisal beliefs if needed by other consumers
   - Recommendation: Keep internal unless downstream demand emerges.

3. **dynamic_intensity**: SRP computes this but it's not an F6 belief. It could belong to F1 (sensory) or F3 (salience). Currently internal to SRP mechanism.
   - Recommendation: Keep internal — it's a musical meaning signal used for peak_detection computation.

4. **opioid_proxy, vta_drive, stg_nacc_coupling**: These are neurochemical/circuit-level intermediates. They could theoretically become Appraisal beliefs if HYBRID visualization needs them.
   - Recommendation: Defer to wave 3+ unless HYBRID demands arise.

---

## 9. Scientific References (Key Subset)

| Ref | Finding | SRP Impact |
|-----|---------|------------|
| Salimpoor 2011 | NAcc r=0.84, Caudate r=0.71 | Primary β coefficients |
| Salimpoor 2013 | NAcc-STG predicts willingness to pay | stg_nacc_coupling |
| Cheung 2019 | Uncertainty × surprise = 2D pleasure surface | prediction_error nonlinearity |
| Ferreri 2019 | Levodopa↑ both wanting AND liking | DA causal for both systems |
| Mas-Herrero 2021 | dlPFC TMS → NAcc (d=0.81) | Temporal dissociation |
| Martinez-Molina 2016 | Musical anhedonia = NAcc-STG disconnection | stg_nacc as critical link |
| Berridge & Robinson 2003 | Wanting ≠ Liking (dissociable) | 3-system architecture |
| Huron 2006 | ITPRA framework | 5 temporal responses |
| Howe 2013 | Quasi-hyperbolic DA ramp | da_caudate profile |
| Schultz 2016 | Two-component phasic DA RPE | prediction_error |
| Nummenmaa 2025 | μ-opioid PET during music pleasure | opioid_proxy justification |

---

## 10. Summary

```
ARU-α1-SRP → PURE F6 (Reward & Motivation)
  19D output → 11 F6 beliefs + 8 internal intermediates
  5 Core Beliefs (full Bayesian PE cycle): wanting, liking, pleasure, prediction_error, tension
  3 Appraisal Beliefs (observe-only): prediction_match, peak_detection, harmonic_tension
  3 Anticipation Beliefs (forward predictions): reward_forecast, chills_proximity, resolution_expectation

  Phase: 5 (Terminal — needs all other PEs)
  H³: ~124 tuples (largest consumer of all 96 models)
  Relay: 7 fields exported to scheduler
  RAM: 3 region links (caudate, NAcc, IFG)

  No secondary Function assignment. Pure reward model.
  Cross-Function reads: F1(consonance), F2(prediction), F3(salience), F4(familiarity), F7(tempo)
```
