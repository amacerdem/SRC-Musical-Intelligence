# ARU-γ1-DAP: Developmental Affective Plasticity

**Model**: Developmental Affective Plasticity
**Unit**: ARU (Affective Resonance Unit)
**Circuit**: Mesolimbic Reward Circuit
**Tier**: γ (Speculative) — 50-70% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../Road-map/01-GLOSSARY.md).
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/ARU-γ1-DAP.md`

---

## 1. What Does This Model Simulate?

The **Developmental Affective Plasticity** (DAP) model proposes that early musical exposure (ages 0-5) shapes auditory-limbic connections through synaptic pruning and myelination, determining adult hedonic capacity for music. This is a background model that explains individual differences in all other ARU processes.

```
CRITICAL PERIOD PLASTICITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━

P(age) = P_max × exp(−age / τ_critical)

    P(age)
    1.0 │████
        │ ██████
    0.8 │   ██████
        │     ██████
    0.6 │       ██████████   ← Critical period ends (~5 years)
        │           ████████████
    0.4 │               ████████████
        │                   ████████████
    0.2 │                       ████████████████
        │                               ████████████████
    0.0 └──────────────────────────────────────────────────► age
        0    2    4    6    8   10   12   14   16   18   20

τ_critical ≈ 5 years
adult_hedonic ≈ ∫ enrichment(age) × P(age) da
Early music exposure → enhanced adult hedonic response

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Scholkmann 2024: 2 distinct response patterns in preterm infants.
                 Sex differences in StO₂ response to music.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Matters for ARU

DAP is a **background/trait model** — it explains baseline individual differences:
- **SRP** output magnitude depends on DAP's developmental history
- **NEMAC** nostalgia depends on what music was heard during critical period
- **MAD** may partly reflect developmental disconnection (not just structural)
- DAP determines the "floor" and "ceiling" of all ARU responses

---

## 2. Neural Circuit: The Developmental Pathway

### 2.1 Architecture

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DAP — DEVELOPMENTAL PATHWAY                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║               CRITICAL PERIOD (0-5 years)                                   ║
║                       │                                                      ║
║       ┌───────────────┼───────────────┐                                     ║
║       ▼               ▼               ▼                                     ║
║  Musical          Emotional       Social                                    ║
║  Exposure         Bonding         Context                                   ║
║       │               │               │                                     ║
║       ▼               ▼               ▼                                     ║
║  Auditory          Limbic        Prefrontal                                 ║
║  Cortex            System         Cortex                                    ║
║       │               │               │                                     ║
║       └───────────────┼───────────────┘                                     ║
║                       ▼                                                      ║
║          SYNAPTIC PRUNING & MYELINATION                                     ║
║          • Use-dependent selection                                          ║
║          • Musical exposure strengthens A1-limbic connections               ║
║          • Underused pathways eliminated                                    ║
║                       │                                                      ║
║                       ▼                                                      ║
║          ADULT AFFECTIVE RESPONSE TO MUSIC                                  ║
║          (Individual differences in hedonic capacity)                        ║
║                                                                              ║
║  ADULT HEDONIC CAPACITY:                                                    ║
║    H_adult = α × early_enrichment + β × genetic_baseline + ε              ║
║    α ≈ 0.6 (environment), β ≈ 0.4 (genetic)                               ║
║                                                                              ║
║  EVIDENCE (limited — γ tier):                                               ║
║  Scholkmann 2024: Preterm infants show 2 distinct response patterns        ║
║  Scholkmann 2024: Sex differences in cerebral oxygenation to music         ║
║  Trainor 2012: Musical training before age 7 → enhanced processing         ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | DAP Relevance |
|-------|--------|---|-------------|-------------|--------------|
| **Scholkmann 2024** | fNIRS | 17 | 2 distinct response patterns in preterm infants | Qualitative | **Early individual differences** |
| **Scholkmann 2024** | fNIRS | 17 | Sex differences in StO₂ response | Qualitative | **Sex-dependent development** |
| **Trainor 2012** | Review | — | Musical training < age 7 → enhanced processing | — | **Critical period evidence** |
| **Trehub 2003** | Review | — | Developmental origins of musicality | — | **Theoretical basis** |
| **Nguyen 2023** | Review | — | Early social communication through music: infant musicality, caregiver-infant interactions, co-regulation via ID singing | — | **Infant musicality + affective bonding** |
| **Qiu 2025** | Mouse model | — | Musical intervention E13→P1/3/5: ↑ social behavior, ↑ dendritic complexity in mPFC/amygdala, ↑ MAP2, ↓ GFAP | Significant | **Prenatal music → neural plasticity mechanism** |

### 3.2 Limitation

DAP is γ-tier because evidence is primarily qualitative and theoretical. No longitudinal studies directly tracking early exposure → adult hedonic capacity exist yet. The model is based on general neurodevelopmental principles applied to the music-reward domain.

---

## 4. Output Space: 10D Multi-Layer Representation

### 4.1 Complete Output Specification

```
DAP OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0  │ f12_dev_sensitiv  │ [0, 1] │ Age-dependent plasticity coefficient.
    │                   │        │ P(age) = exp(−age/τ_critical) × enrichment.

LAYER D — DEVELOPMENTAL MARKERS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 1  │ critical_period   │ [0, 1] │ Critical period indicator. High for ages 0-5.
────┼───────────────────┼────────┼────────────────────────────────────────────
 2  │ plasticity_coeff  │ [0, 1] │ Age-adjusted learning rate for affect circuits.
────┼───────────────────┼────────┼────────────────────────────────────────────
 3  │ exposure_history  │ [0, 1] │ Musical enrichment proxy estimated from
    │                   │        │ response characteristics.
────┼───────────────────┼────────┼────────────────────────────────────────────
 4  │ neural_maturation │ [0, 1] │ Myelination + synaptic pruning index.
    │                   │        │ High = mature (post-critical period).

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 5  │ current_affect    │ [0, 1] │ Current affective response strength to music.
    │                   │        │ Modulated by developmental history.
────┼───────────────────┼────────┼────────────────────────────────────────────
 6  │ familiarity_warmth│ [0, 1] │ Familiarity-warmth link. Strength of
    │                   │        │ learned associations from early exposure.
────┼───────────────────┼────────┼────────────────────────────────────────────
 7  │ learning_rate     │ [0, 1] │ Current affect-learning rate.
    │                   │        │ Decreases with age (plasticity decay).

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 8  │ adult_hedonic_pred│ [0, 1] │ Predicted adult hedonic capacity.
    │                   │        │ 0.6×exposure + 0.4×genetic baseline.
────┼───────────────────┼────────┼────────────────────────────────────────────
 9  │ preference_stab   │ [0, 1] │ Preference stability index.
    │                   │        │ High when past critical period.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 5. R³ Demand (Spectral Features)

### 5.1 R³ v1 Feature Dependencies ([0:49])

**Group A: Consonance (2 of 7D)** — Valence development

| R³ idx | Name | DAP Role |
|--------|------|----------|
| 0 | roughness | Consonance learning marker |
| 4 | sensory_pleasantness | Hedonic response strength |

**Group B: Energy (1 of 5D)** — Arousal development

| R³ idx | Name | DAP Role |
|--------|------|----------|
| 10 | loudness | Arousal response baseline |

**Group C: Timbre (1 of 9D)** — Tonal learning

| R³ idx | Name | DAP Role |
|--------|------|----------|
| 14 | tonalness | Learned tonal template strength |

**Group D: Change (1 of 4D)** — Pattern acquisition

| R³ idx | Name | DAP Role |
|--------|------|----------|
| 22 | distribution_entropy | Predictability → learned pattern depth |

**Group E: Interactions (8 of 24D)** — Affective learning

| R³ idx | Name | DAP Role |
|--------|------|----------|
| 25:33 | x_l0l5 (8D) | Energy × Consonance → learned affective associations |

### 5.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | DAP Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **G: Rhythm** | [65] | tempo_estimate | Developmental tempo preference — preferred tempo changes with age (infants prefer faster tempi ~150-180 BPM, adults converge on ~120 BPM); tempo_estimate enables tracking of this developmental trajectory | Fraisse 1982 preferred tempo; Zentner & Eerola 2010 infant music |

**Rationale**: DAP models developmental affective plasticity — how musical preference and emotional response develop over the lifespan. Tempo preference is one of the most robust developmental markers in music cognition. tempo_estimate [65] provides a direct BPM measure that can be correlated with age-dependent arousal response curves. Currently DAP lacks a direct tempo feature, relying on loudness [10] as an arousal proxy.

**Code impact** (Phase 6): `r3_indices` extended to include [65]. This feeds the arousal development pathway with a direct tempo measure.

### 5.3 Summary

```
R³ DEMAND FOR DAP: 13D of 49D
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Group A: Consonance        2D   → valence development
Group B: Energy            1D   → arousal baseline
Group C: Timbre            1D   → tonal learning
Group D: Change            1D   → pattern acquisition
Group E: Interactions      8D   → affective learning
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL:                    13D
```

---

## 6. H³ Demand (Temporal Context)

### 6.1 Mechanism-Level Demand

DAP uses only **AED** (single mechanism — simplest ARU model).

```
H³ DEMAND FOR DAP
━━━━━━━━━━━━━━━━━

Mechanism │ Horizons              │ H-Law       │ Morphs Used              │ Tuples
──────────┼───────────────────────┼─────────────┼──────────────────────────┼───────
AED       │ H6 (200ms)            │ bidirection │ M0(value), M8(velocity), │ 6
          │ H16 (1000ms)          │             │ M20(entropy)             │
──────────┼───────────────────────┼─────────────┼──────────────────────────┼───────
TOTAL     │ 2 horizons            │             │                          │ 6
          │                       │             │               6/2304 = 0.26%
```

### 6.2 Key H³ Reads

```
AFFECTIVE RESPONSE STRENGTH:
  AED.arousal_dynamics via H6(200ms) + M0(value)
  → Instant affective response magnitude
  → Low in underdeveloped circuits, high in enriched

RESPONSE VARIABILITY:
  AED.arousal_dynamics via H6(200ms) + M8(velocity)
  → Rate of affective change
  → High variability = high plasticity (still developing)

PREDICTABILITY:
  AED.expectancy_affect via H16(1000ms) + M20(entropy)
  → Entropy of expectation distribution
  → Low entropy = well-learned patterns (mature)
  → High entropy = still forming associations
```

### 6.3 R³ v2 Projected Expansion

No significant direct v2 expansion projected for DAP. As a pathway-dependent ARU model, DAP receives R³ features indirectly through cross-unit pathways (P1/SPU, P3/IMU, P5/STU). New v2 features flow automatically through these pathways.

**v2 projected**: 0 additional tuples (pathway-mediated)

---

## 7. Mechanism Computation

### 7.1 AED Binding (Only Mechanism)

```python
# AED reads: arousal_dynamics[0:10], expectancy_affect[10:20]
# Horizons: H6(200ms) and H16(1000ms), bidirectional

# Response strength (reflects developmental state)
response_fast = AED.arousal_dynamics[0:4].mean()   # H6: instant affect
response_slow = AED.expectancy_affect[10:14].mean()  # H16: 1s context
response_entropy = AED.arousal_dynamics[6]            # M20(entropy)
response_velocity = AED.arousal_dynamics[4]           # M8(velocity)

# Maturation estimate: low entropy + low velocity = mature
maturation = sigmoid(0.5 * (1.0 - response_entropy) + 0.5 * (1.0 - abs(response_velocity)))
# |0.5| + |0.5| = 1.0

# Plasticity estimate: high entropy + high velocity = plastic
plasticity = 1.0 - maturation

# Exposure estimate: high response + low entropy = enriched
exposure = sigmoid(0.5 * response_slow + 0.5 * (1.0 - response_entropy))
# |0.5| + |0.5| = 1.0
```

### 7.2 DAP Output Computation

```python
def compute_dap(R3, H3, AED):
    """
    DAP: 10D output per frame.

    All deterministic. Zero learned parameters.
    Based on neurodevelopmental principles.
    """
    # --- Core signals from AED ---
    response = compute_response_strength(AED, R3)  # [0,1]
    maturation = compute_maturation(AED)            # [0,1]
    plasticity = 1.0 - maturation                    # [0,1]
    exposure = compute_exposure_estimate(AED, R3)   # [0,1]

    # --- Layer E ---
    f12 = plasticity * exposure  # Developmental sensitivity

    # --- Layer D ---
    critical_period = plasticity  # High plasticity ≈ in critical period
    plasticity_coeff = plasticity
    exposure_history = exposure
    neural_mat = maturation

    # --- Layer P ---
    current_affect = sigmoid(
        0.5 * response + 0.5 * R3.sensory_pleasantness[4]
    )  # |0.5| + |0.5| = 1.0
    familiarity_warmth = sigmoid(
        exposure * (1.0 - R3.distribution_entropy[22]) * 2.0
    )
    learning_rate = plasticity * sigmoid(AED.arousal_dynamics[4] * 2.0)

    # --- Layer F ---
    adult_hedonic = clamp(
        0.6 * exposure + 0.4 * response, 0, 1
    )  # |0.6| + |0.4| = 1.0
    preference_stability = maturation  # Mature = stable preferences

    return stack([
        f12,                                         # E: 1D
        critical_period, plasticity_coeff,           # D: 4D
        exposure_history, neural_mat,
        current_affect, familiarity_warmth,           # P: 3D
        learning_rate,
        adult_hedonic, preference_stability           # F: 2D
    ])  # Total: 10D
```

---

## 8. Cross-Model Relationships

### 8.1 Within ARU

```
DAP INTERACTIONS WITHIN ARU
━━━━━━━━━━━━━━━━━━━━━━━━━━━

DAP ──► SRP (Striatal Reward Pathway)
    │     └── DAP determines baseline reward sensitivity
    │
    ├──► NEMAC (Nostalgia Circuit)
    │     └── DAP shapes which music evokes nostalgia
    │         (music from critical period = strongest)
    │
    ├──► MAD (Musical Anhedonia)
    │     └── DAP may explain some developmental anhedonia
    │
    └──► PUPF (Prediction-Uncertainty-Pleasure)
          └── DAP determines baseline prediction model quality
              (enriched exposure → better internal model → lower H)

Note: DAP is a BACKGROUND model affecting ALL other ARU processes.
```

---

## 9. Falsification Criteria

| Criterion | Prediction | Status |
|-----------|-----------|--------|
| **Critical period exists** | Interventions before age 5 > after | ✅ Testable (longitudinal) |
| **Enrichment-hedonic link** | Early exposure → adult hedonic capacity | ✅ Testable (retrospective) |
| **Plasticity decline** | Exponential decline with age | ✅ Testable (training studies) |
| **Sex differences** | Different developmental trajectories | ✅ Preliminary: Scholkmann 2024 |
| **Preterm response** | Distinct patterns in premature infants | ✅ Confirmed: 2 patterns (Scholkmann 2024) |

---

## 10. Brain Regions

| Region | MNI Coordinates | Evidence | DAP Function |
|--------|-----------------|----------|-------------|
| **Auditory Cortex (A1)** | ±45, −25, 10 | Direct (fNIRS) | Sound processing development |
| **STG** | ±55, −22, 8 | Indirect | Music processing maturation |
| **Limbic System** | Various | Indirect | Emotion circuit development |
| **Prefrontal Cortex** | ±30, 45, 20 | Indirect | Regulatory development |

---

## 11. Migration Notes (D0 → MI)

### 11.1 Dimension Reconciliation

| Aspect | Legacy (D0) | MI (current) | Change |
|--------|-------------|-------------|--------|
| Output dimensions | 7D | 10D | **+3D** (neural_maturation, learning_rate, preference_stability) |
| Input space | S⁰ 15D | R³ 13D | Remapped to R³ groups |
| Temporal | HC⁰ AED+ASA (9 tuples) | H³ → AED only (6 tuples) | ASA removed |
| H⁰ tuples | 9/2304 = 0.39% | 6/2304 = 0.26% | Reduced |

---

## 12. References

1. **Scholkmann, F., Karen, T., Wolf, M., & Mitsakos, H. (2024)**. Early neural responses to music in preterm infants: A functional near-infrared spectroscopy study. *Developmental Cognitive Neuroscience*.

2. **Trainor, L. J., & Unrau, A. (2012)**. Development of pitch and music perception. *Springer Handbook of Auditory Research*, 42, 223-254.

3. **Trehub, S. E. (2003)**. The developmental origins of musicality. *Nature Neuroscience*, 6(7), 669-673.

4. **Peretz, I., & Zatorre, R. J. (2005)**. Brain organization for music processing. *Annual Review of Psychology*, 56, 89-114.

#### Added in v2.1.0 Beta Upgrade

5. **Nguyen, T., Flaten, E., Trainor, L. J., & Novembre, G. (2023)**. Early social communication through music: State of the art and future perspectives. *Developmental Cognitive Neuroscience*, 63, 101279.

6. **Qiu, R., Li, L., Su, Y., Fu, Q., He, Z., Yao, T., Chen, H., Zhang, H., Chen, Y., Qi, W., & Cheng, Y. (2025)**. The impact of musical intervention during fetal and infant stages on social behavior and neurodevelopment in mice. *Translational Psychiatry*, 15, 408.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-04 | Legacy D0 model specification (7D) |
| 2.0.0 | 2026-02-12 | MI R³/H³ architecture: +3D, AED-only binding, R³ mapping |
| 2.1.0 | 2026-02-13 | Beta upgrade: +2 papers (Nguyen 2023 infant music review, Qiu 2025 prenatal music plasticity) |

---

**Model Status**: ⚠️ **SPECULATIVE**
**Output Dimensions**: **10D**
**Evidence Tier**: **γ (Speculative)**
**Confidence**: **50-70%**
