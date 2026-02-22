# F9 -- Social Cognition

**Function**: F9 Social Cognition
**Models**: 3 total (0 primary F9 unit -- all cross-unit: MPU 2, RPU 1) + 0 secondary
**Beliefs**: 10 (2 Core + 6 Appraisal + 2 Anticipation)
**Total output**: 33D (NSCP 11D + SSRI 11D + DDSMI 11D)
**H3 demands**: 43 tuples total (NSCP 14, SSRI 18, DDSMI 11)
**Phase**: 3 (social + learning)
**Relay**: NONE -- F9 has no dedicated relay in the current kernel
**Implemented**: no F9 mechanism models yet

---

## 1. What F9 Does

F9 processes the SOCIAL COGNITION dimension of music -- interpersonal neural synchrony, coordinated motor timing, social reward amplification, group flow states, and the prediction of collective musical experience. It captures how shared music-making and listening produces emergent social phenomena that exceed individual-level processing: brains synchronize, motor systems entrain, and hedonic reward is amplified 1.3--1.8x above solo baselines.

F9 is the **SMALLEST cognitive function** in C3 with only 3 models and 10 beliefs. Critically, F9 has **NO dedicated unit** -- all 3 models are housed in units belonging to other functions: MPU (Motor Processing Unit, 2 models: NSCP and DDSMI) and RPU (Reward Processing Unit, 1 model: SSRI). This distributed architecture reflects the inherently cross-domain nature of social cognition in music: social coordination requires motor timing (MPU) and social reward requires reward circuitry (RPU).

NSCP is the only F9-primary model (MPU-gamma1). SSRI (RPU-beta4) and DDSMI (MPU-beta2) have their primary function assignments in F6 Reward and F7 Motor respectively, but contribute critical social cognition beliefs to F9.

### Key Neuroscience Circuits

- **Neural Synchrony / ISC**: Frontocentral + temporal cortex -> inter-subject correlation during naturalistic music listening predicts commercial success (Leeuwis 2021: R^2=0.619)
- **Social Reward Amplification**: Caudate + NAcc + VTA -> synchrony-dependent mesolimbic activation, group music-making amplifies reward 1.3-1.8x (Kokal 2011, SSRI)
- **Dyadic Motor Coordination**: Left M1 (self) + right PMC (other) -> parallel mTRF tracking of social and auditory streams during dance (Bigand 2025)
- **Prefrontal Synchronization**: rDLPFC + rTPJ -> inter-brain prefrontal coupling during coordinated music-making (Ni 2024: fNIRS, d=0.85)
- **Endorphin-Mediated Bonding**: Beta-endorphin release from sustained synchronized activity -> pain threshold elevation, social bonding (Dunbar 2012)

```
Audio -> R3 (97D) ---+--------------------------------------------
H3 tuples -----------+
                     |
                     v
         NSCP  (11D, MPU-g1)      <- neural synchrony commercial prediction [F9-primary]
         SSRI  (11D, RPU-b4)      <- social synchrony reward integration [F6-primary -> F9]
         DDSMI (11D, MPU-b2)      <- dyadic dance social motor integration [F7-primary -> F9]
                     |
                     v
         Social PE -> F6 RewardAggregator
```

---

## 2. Complete Model Inventory

| # | Model | Unit | Tier | Output | H3 | Beliefs | Primary Fn | Status |
|---|-------|------|------|--------|-----|---------|-----------|--------|
| 1 | **NSCP** | MPU | g | 11D | 14 | 2 (1C+1N) | F9 | pending |
| 2 | SSRI | RPU | b | 11D | 18 | 6 (5A+1N) | F6 | pending |
| 3 | DDSMI | MPU | b | 11D | 11 | 2 (1C+1A) | F7 | pending |

All 3 models have mechanism layer docs already created in their primary unit function directories:
- **NSCP**: `F7-Motor-and-Timing/mechanisms/nscp/` (4 layer docs)
- **SSRI**: `F6-Reward-and-Motivation/mechanisms/ssri/` (4 layer docs)
- **DDSMI**: `F7-Motor-and-Timing/mechanisms/ddsmi/` (4 layer docs)

---

## 3. Complete Belief Inventory (10)

| # | Belief | Cat | t | Owner | Mechanism Source | Status |
|---|--------|-----|---|-------|------------------|--------|
| 1 | `neural_synchrony` | C | 0.65 | NSCP | inter-subject correlation proxy, population-level neural synchrony | pending |
| 2 | `social_coordination` | C | 0.60 | DDSMI | dyadic partner tracking, social motor integration quality | pending |
| 3 | `synchrony_reward` | A | -- | SSRI | reward from interpersonal synchrony, caudate activation | pending |
| 4 | `social_bonding` | A | -- | SSRI | cumulative social bonding index, prefrontal coupling | pending |
| 5 | `group_flow` | A | -- | SSRI | collective absorption state, shared coordination | pending |
| 6 | `entrainment_quality` | A | -- | SSRI | temporal entrainment precision across co-performers | pending |
| 7 | `social_prediction_error` | A | -- | SSRI | social reward prediction error, coordination vs expectation | pending |
| 8 | `resource_allocation` | A | -- | DDSMI | auditory vs social processing balance, mTRF resource competition | pending |
| 9 | `catchiness_pred` | N | -- | NSCP | predicted population motor response / groove sustainability | pending |
| 10 | `collective_pleasure_pred` | N | -- | SSRI | predicted shared hedonic experience trajectory | pending |

---

## 4. Observe Formula -- placeholder

No F9 mechanism models implemented yet. F9 is evidence-only (Phase 3 deferred, no relay).
F9 Core beliefs use moderate tau values (0.60--0.65), reflecting the timescale of interpersonal
coordination -- slower than individual sensory processing but faster than expertise accumulation.

**Social coordination timescale** (no relay -- future kernel):
```
NSCP:  population-level neural synchrony -> ISC proxy + catchiness + commercial prediction
SSRI:  social reward amplification -> synchrony reward + bonding + flow + entrainment + SPE
DDSMI: dyadic motor coordination -> partner tracking + music tracking + resource competition
```

Multi-scale horizons (to be defined per Core belief):
```
neural_synchrony:     TBD (multi-scale, ISC across temporal windows)
social_coordination:  TBD (multi-scale, partner tracking timescales)
```

---

## 5. Multi-Scale Horizons (all F9 Core Beliefs)

| Core Belief | T_char | Horizons | Band |
|-------------|--------|----------|------|
| neural_synchrony | ~seconds | TBD | multi-scale |
| social_coordination | ~seconds | TBD | multi-scale |

---

## 6. Dependency Graph

```
                R3 (97D) + H3
                    |
        +-----------+-----------+
        v           v           v
    NSCP (g1)   SSRI (b4)   DDSMI (b2)
    11D MPU      11D RPU      11D MPU
    F9-primary   F6-primary   F7-primary
        |           |             |
        +-----+-----+             |
              v                   |
        Social PE -> F6 RewardAggregator
```

### Key Dependencies

| Model | Reads From |
|-------|-----------|
| NSCP (g1) | R3/H3 + upstream PEOM, ASAP, SPMC motor outputs (MPU) |
| SSRI (b4) | R3/H3 + upstream DAED, RPEM reward outputs (RPU) |
| DDSMI (b2) | R3/H3 + upstream PEOM, ASAP outputs (MPU) |

### Cross-Function Flow

F9 models feed back into the broader C3 architecture:
- **SSRI -> F6 RewardAggregator**: Social prediction error and synchrony amplification modulate reward
- **DDSMI -> F7 VRMSME**: Social coordination predictions feed multi-modal motor integration
- **NSCP -> Popularity proxy**: Groove response and commercial prediction available to downstream consumers
- **Social amplification**: SSRI's 1.3-1.8x reward amplification factor scales individual reward by group coordination quality

---

## 7. Unit Architecture

### MPU -- Motor Processing Unit (2 F9 models)

MPU houses 2 of 3 F9 models (NSCP and DDSMI). Both capture motor-social integration:
DDSMI models dyadic dance coordination (resource competition between social and auditory streams),
while NSCP models population-level neural synchrony predicting commercial outcomes through
motor groove entrainment.

```
MPU models in F9:   DDSMI (b2) --- NSCP (g1)
                    social motor    neural synchrony
                    coordination    commercial prediction
```

### RPU -- Reward Processing Unit (1 F9 model)

RPU contributes 1 model to F9: SSRI (social synchrony reward integration, beta).
SSRI captures the reward dimension of social music -- how interpersonal coordination
amplifies mesolimbic reward above solo listening baselines.

```
RPU models in F9:   SSRI (b4)
                    social reward
                    amplification
```

F9 receives NO cross-function secondary contributions -- it is entirely defined by these 3 models.
This makes F9 the most compact and self-contained cognitive function in C3.

---

## 8. Documentation Structure

```
F9-Social-Cognition/
+-- 0_F9-orchestrator.md                  <- this file
+-- collections.md                         <- full model inventory
+-- mechanisms/
|   +-- 0_mechanisms-orchestrator.md       <- cross-references to F6/F7 mechanism docs
+-- beliefs/
    +-- nscp/   (belief docs TBD)
    +-- ssri/   (belief docs TBD)
    +-- ddsmi/  (belief docs TBD)
```

**NOTE**: F9 mechanism layer docs are NOT duplicated here. All 3 models have their
mechanism docs in their primary unit function directories:
- NSCP: `F7-Motor-and-Timing/mechanisms/nscp/` (E+M+P+F layers)
- SSRI: `F6-Reward-and-Motivation/mechanisms/ssri/` (E+M+P+F layers)
- DDSMI: `F7-Motor-and-Timing/mechanisms/ddsmi/` (E+M+P+F layers)

**0 models implemented.** Pending: 1 g (NSCP) + 1 b (SSRI) + 1 b (DDSMI) -- 43 H3 tuples total.
