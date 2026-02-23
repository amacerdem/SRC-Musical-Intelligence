# F11 -- Development & Evolution

**Function**: F11 Development & Evolution
**Type**: META-LAYER -- evidence-only, NO beliefs, NO relay
**Models**: 6 total (all cross-unit: NDU 3, IMU 2, ARU 1) + 0 secondary
**Beliefs**: 0 (meta-layer -- evidence feeds INTO F1-F9 observe())
**Total output**: 63D (DAP 10D + DMMS 10D + CSSL 10D + SDDP 10D + ONI 11D + DSP 12D)
**H3 demands**: 86 tuples total (DAP 6, DMMS 15, CSSL 15, SDDP 16, ONI 16, DSP 18)
**Phase**: meta (deferred -- evidence-only)
**Relay**: NONE -- F11 is a meta-layer with no dedicated relay
**Implemented**: no F11 mechanism models yet

---

## 1. What F11 Does

F11 processes the DEVELOPMENTAL AND EVOLUTIONARY dimension of music cognition -- how musical capacities emerge across ontogeny (individual development) and phylogeny (species evolution). It captures the developmental scaffolding of musical memory, affective plasticity across the lifespan, cross-species song learning as evolutionary evidence, sex-dependent developmental trajectories, and the risks of over-normalization in clinical/educational music interventions.

F11 is a **META-LAYER** -- it has **NO beliefs** and **NO relay**. All 6 models produce evidence that feeds unidirectionally INTO F1-F9 observe() via cross-function signal routes. This architecture reflects that developmental and evolutionary phenomena are not separate cognitive processes but rather modulatory contexts for the same F1-F9 machinery: how affective processing matures (F5), how memory scaffolding develops (F4), how reward circuits crystallize (F6), and how sensory processing adapts across sex and age (F1, F3).

F11 has **NO dedicated unit**. Its 6 models are distributed across 3 units belonging to other functions: NDU (Neural Dynamics Unit, 3 models), IMU (Integrative Memory Unit, 2 models), and ARU (Affective Response Unit, 1 model). SDDP and ONI are F11-primary models with mechanism docs in this directory; DSP is cross-referenced from F10.

### Developmental Domains

1. **Affective Development**: DAP (developmental affective plasticity across the lifespan)
2. **Memory Development**: DMMS, CSSL (developmental music memory scaffold, cross-species song learning)
3. **Neural Development**: SDDP, ONI, DSP (sex-dependent plasticity, over-normalization, deviance processing)

### Key Neuroscience Circuits

- **Affective Plasticity**: Amygdala + mPFC + insula -> lifespan changes in music-evoked emotional processing (Vieillard 2008, Eerola 2013)
- **Memory Scaffolding**: Hippocampus + parahippocampal gyrus -> developmental trajectory of musical memory encoding (Trainor 2005, Hannon & Trehub 2005)
- **Cross-Species Song Learning**: HVC + RA + Area X (songbird) <-> Broca's + SMA + basal ganglia (human) -> shared vocal learning circuits (Jarvis 2004, Fitch 2006)
- **Sex-Dependent Development**: Heschl's gyrus + planum temporale -> sex-differentiated cortical auditory development (Zatorre 2012, Hyde 2008)
- **Over-Normalization**: Prefrontal + basal ganglia -> intervention-driven over-regularization of natural variability (Tervaniemi 2009)

```
Audio -> R3 (97D) ---+--------------------------------------------
H3 tuples -----------+
                     |
                     v
 [Affective Dev]     DAP    (10D, ARU-g)    <- developmental affective plasticity
 [Memory Dev]        DMMS   (10D, IMU-g)    <- developmental music memory scaffold
                     CSSL   (10D, IMU-g)    <- cross-species song learning
 [Neural Dev]        SDDP   (10D, NDU-g)    <- sex-dependent developmental plasticity
                     ONI    (11D, NDU-g)    <- over-normalization in intervention
                     DSP    (12D, NDU-b)    <- deviance salience processing
                     |
                     v
         Evidence -> F1-F9 observe() (unidirectional)
```

---

## 2. Complete Model Inventory

| # | Model | Unit | Tier | Output | H3 | Primary Fn | Status |
|---|-------|------|------|--------|-----|-----------|--------|
| 1 | **DAP** | ARU | g | 10D | 6 | F11 | pending |
| 2 | **DMMS** | IMU | g | 10D | 15 | F11 | pending |
| 3 | **CSSL** | IMU | g | 10D | 15 | F11 | pending |
| 4 | **SDDP** | NDU | g | 10D | 16 | F11 | pending |
| 5 | **ONI** | NDU | g | 11D | 16 | F11 | pending |
| 6 | **DSP** | NDU | b | 12D | 18 | F10 | pending |

4/6 models have mechanism layer docs in their primary function directories:
- **DAP**: `F5-Emotion-and-Valence/mechanisms/dap/`
- **DMMS**: `F4-Memory-Systems/mechanisms/dmms/`
- **CSSL**: `F4-Memory-Systems/mechanisms/cssl/`
- **DSP**: `F10-Clinical-and-Therapeutic/mechanisms/dsp/` (cross-ref from F10)

2/6 models are F11-primary with docs in this directory:
- **SDDP**: `F11-Development-and-Evolution/mechanisms/sddp/` (NEW -- pending layer docs)
- **ONI**: `F11-Development-and-Evolution/mechanisms/oni/` (NEW -- pending layer docs)

---

## 3. Meta-Layer Architecture -- NO Beliefs

F11 is fundamentally different from F1-F9. It has **0 beliefs**, **0 Core**, **0 Appraisal**, **0 Anticipation**. There is no Bayesian update cycle, no precision engine, no prediction error tracking.

Instead, F11 models produce **evidence signals** that feed INTO F1-F9 observe() unidirectionally:

```
F11 Models -> F1-F9 Evidence Routes:
DAP    -> F5 Emotion                      (affective developmental context)
DMMS   -> F4 Memory                       (memory scaffold maturation)
CSSL   -> F4 Memory                       (evolutionary song learning evidence)
SDDP   -> F5 Emotion / F1 Sensory        (sex-dependent processing context)
ONI    -> F6 Reward / F8 Learning         (over-normalization risk signal)
DSP    -> F3 Attention                    (deviance in developmental context)
```

This evidence-only architecture means:
- No tau values (no Core beliefs)
- No precision tracking (no PE history)
- No relay wrapper (no kernel integration)
- No phase in the scheduler (meta-layer)
- All computation is deferred to the receiving F1-F9 beliefs

---

## 4. Dependency Graph

```
                R3 (97D) + H3
                    |
    +---+---+---+---+---+---+
    v   v   v   v   v   v
   DAP DMMS CSSL SDDP ONI DSP
   10D 10D  10D  10D  11D 12D
   ARU IMU  IMU  NDU  NDU NDU
    |   |    |    |    |   |
    v   v    v    v    v   v
   F5  F4   F4  F5/F1 F6  F3
                      F8
        Evidence -> F1-F9 observe()
```

### Key Dependencies

| Model | Reads From |
|-------|-----------|
| DAP (ARU-g) | R3/H3 + upstream SRP, CLAM, TAR outputs (ARU) |
| DMMS (IMU-g) | R3/H3 + upstream MEAMN, HCMC memory outputs (IMU) |
| CSSL (IMU-g) | R3/H3 + upstream MEAMN, HCMC memory outputs (IMU) |
| SDDP (NDU-g) | R3/H3 + upstream MPG, SDD outputs (NDU) |
| ONI (NDU-g) | R3/H3 + upstream MPG, SDD outputs (NDU) |
| DSP (NDU-b) | R3/H3 + upstream MPG outputs (NDU) |

### Cross-Function Evidence Flow

F11 models feed evidence into F1-F9 unidirectionally:
- **F1 Sensory**: SDDP sex-dependent auditory processing context
- **F3 Attention**: DSP deviance detection in developmental context
- **F4 Memory**: DMMS memory scaffold maturation, CSSL evolutionary song learning
- **F5 Emotion**: DAP affective plasticity, SDDP sex-dependent emotional processing
- **F6 Reward**: ONI over-normalization risk for reward calibration
- **F8 Learning**: ONI over-normalization risk for learning adaptation

---

## 5. Unit Architecture

### ARU -- Affective Response Unit (1 F11 model)

ARU contributes 1 model to F11: DAP (developmental affective plasticity, gamma). DAP is a background model for ALL ARU -- it provides the developmental context for how affective processing varies across the lifespan, from infant preference for consonance to adolescent reward-seeking to elderly emotional regulation.

```
ARU models in F11:  DAP (g)
                    developmental
                    affective
                    plasticity
```

### IMU -- Integrative Memory Unit (2 F11 models)

IMU contributes 2 models to F11: DMMS (developmental music memory scaffold, gamma) and CSSL (cross-species song learning, gamma). Both capture the developmental/evolutionary dimension of musical memory: DMMS tracks how memory encoding matures from infancy through adulthood; CSSL provides cross-species evidence for shared vocal learning mechanisms.

```
IMU models in F11:  DMMS (g) --- CSSL (g)
                    memory       cross-species
                    scaffold     song learning
```

### NDU -- Neural Dynamics Unit (3 F11 models)

NDU contributes 3 models to F11: SDDP (sex-dependent developmental plasticity, gamma), ONI (over-normalization in intervention, gamma), and DSP (deviance salience processing, beta -- cross-ref from F10). SDDP and ONI are F11-primary models. DSP contributes developmental deviance processing evidence alongside its F10 clinical role.

```
NDU models in F11:  SDDP (g) --- ONI (g) --- DSP (b)
                    sex-dependent over-       deviance
                    plasticity    normalization salience
```

---

## 6. Documentation Structure

```
F11-Development-and-Evolution/
+-- 0_F11-orchestrator.md                  <- this file
+-- collections.md                         <- full model inventory
+-- mechanisms/
    +-- 0_mechanisms-orchestrator.md       <- cross-references + SDDP/ONI summary
    +-- sddp/                             <- SDDP mechanism layer docs (NEW, pending)
    +-- oni/                              <- ONI mechanism layer docs (NEW, pending)
```

**NOTE**: F11 has NO beliefs directory -- meta-layers have 0 beliefs.
4/6 models have their mechanism docs in their primary unit function directories:
- DAP: `F5-Emotion-and-Valence/mechanisms/dap/`
- DMMS: `F4-Memory-Systems/mechanisms/dmms/`
- CSSL: `F4-Memory-Systems/mechanisms/cssl/`
- DSP: `F10-Clinical-and-Therapeutic/mechanisms/dsp/`

Only SDDP and ONI have mechanism docs in this directory: `F11-Development-and-Evolution/mechanisms/`

**0 models implemented.** Pending: 5 g (DAP, DMMS, CSSL, SDDP, ONI) + 1 b (DSP) -- 86 H3 tuples total.
