# F6 -- Reward & Motivation

**Function**: F6 Reward & Motivation
**Models**: 11 (10 RPU complete unit + 1 ARU relay: SRP) + 5 secondary (PUPF[ARU], MAD[ARU], UDP[PCU], STAI[SPU], AACM[ASU])
**Beliefs**: 16 (5 Core + 7 Appraisal + 4 Anticipation)
**Total output**: 89D (all 11 models)
**H3 demands**: ~271 tuples total (SRP ~124, DAED 16, MORMR 15, RPEM 16, IUCP 14, MCCN 16, MEAMR 14, SSRI 18, LDAC 12, IOTMS 12, SSPS 14)
**Phase**: 3 (reward computation -- terminal, reads ALL other Functions' PEs)
**Relay**: SRP (ARU-a1) -- F6 primary relay, provides wanting/liking/pleasure + tension/chills/resolution
**Implemented**: SRP relay done (kernel v4.0), DAED relay done (kernel v4.0), no F6 mechanism models yet

---

## 1. What F6 Does

F6 processes the REWARD dimension of music -- wanting (anticipatory dopamine), liking (consummatory opioid), pleasure integration, prediction error (TD error), tension-resolution dynamics, chills/frisson, and dopamine dissociation between anticipation and experience. It is the **terminal aggregator** in the belief cycle, reading PEs from ALL other Functions (F1-F5, F7-F9).

F6 is in **Phase 3**: it reads all preceding beliefs and PEs via the RewardAggregator. The SRP relay (a-tier) reads R3/H3 directly; DAED (a-tier) reads R3/H3 + cross-relay (BCH+MEAMN); b-models read a outputs; g-models read a+b. F6 receives cross-function inputs from ARU(PUPF, MAD), PCU(UDP), SPU(STAI), ASU(AACM).

### Key Neuroscience Circuits

- **Wanting Pathway**: Caudate nucleus + VTA dopamine -> anticipatory reward (DA ramp)
- **Liking Pathway**: NAcc + opioid/endocannabinoid system -> consummatory pleasure
- **Prediction Error Circuit**: VTA -> NAcc/caudate -> TD error signal (delta = R + gammaV' - V)
- **Chills/Frisson Pathway**: NAcc + insula + OFC -> peak emotional/reward experiences
- **Dopamine Dissociation**: Caudate (anticipation) vs NAcc (experience) temporal separation

```
Audio -> R3 (97D) ---+--------------------------------------------
H3 tuples -----------+
F1-F8 beliefs/PEs ---+
                     |
                     v
Depth 0:  SRP  (19D, relay)  <- striatal reward pathway [ARU-a1]
          DAED (8D)          <- dopamine anticipation-experience dissociation [RPU-a1]
          MORMR(7D)          <- mu-opioid receptor music reward [RPU-a2]
          RPEM (8D)          <- reward prediction error in music [RPU-a3]
                     |
                     v
Depth 1:  IUCP (6D)          <- inverted-U complexity preference [RPU-b1]
          MCCN (7D)          <- musical chills cortical network [RPU-b2]
          MEAMR(6D)          <- music-evoked autobiographical memory reward [RPU-b3]
          SSRI (11D)         <- social synchrony reward integration [RPU-b4]
                     |
                     v
Depth 2:  LDAC (6D)          <- liking-dependent auditory cortex [RPU-g1]
          IOTMS(5D)          <- individual opioid tone music sensitivity [RPU-g2]
          SSPS (6D)          <- saddle-shaped preference surface [RPU-g3]
```

---

## 2. Complete Model Inventory

| # | Model | Unit | Tier | Depth | Output | H3 | Beliefs | Primary Fn | Status |
|---|-------|------|------|-------|--------|-----|---------|-----------|--------|
| 1 | **SRP** | ARU | a | 0 | 19D | ~124 | 10 (5C+2A+3N) | F6 | relay done |
| 2 | **DAED** | RPU | a | 0 | 8D | 16 | 6 (3A+3N) | F6 | relay done |
| 3 | MORMR | RPU | a | 0 | 7D | 15 | 0 | F6 | pending |
| 4 | RPEM | RPU | a | 0 | 8D | 16 | 0 | F6 | pending |
| 5 | IUCP | RPU | b | 1 | 6D | 14 | 0 | F6 | pending |
| 6 | MCCN | RPU | b | 1 | 7D | 16 | 0 | F6 | pending |
| 7 | MEAMR | RPU | b | 1 | 6D | 14 | 0 | F6 | pending |
| 8 | SSRI | RPU | b | 1 | 11D | 18 | 0 | F6 | pending |
| 9 | LDAC | RPU | g | 2 | 6D | 12 | 0 | F6 | pending |
| 10 | IOTMS | RPU | g | 2 | 5D | 12 | 0 | F6 | pending |
| 11 | SSPS | RPU | g | 2 | 6D | 14 | 0 | F6 | pending |

**Secondary (cross-function):**

| # | Model | Unit | Primary | F6 Contribution |
|---|-------|------|---------|-----------------|
| * | PUPF | ARU-b1 | F2 | Pharmacological reward modulation (DA/serotonin/endorphin) |
| * | MAD | ARU-b3 | F10 | Anhedonia / reward lesion disconnection |
| * | UDP | PCU-b | F2 | Surprise -> pleasure pathway |
| * | STAI | SPU-b | F1 | Aesthetic -> reward feedback |
| * | AACM | ASU-b | F3 | Liking -> attention feedback |

---

## 3. Complete Belief Inventory (16)

| # | Belief | Cat | t | Owner | Mechanism Source | Status |
|---|--------|-----|---|-------|------------------|--------|
| 1 | `wanting` | C | 0.6 | SRP | caudate DA ramp, anticipatory reward | done |
| 2 | `liking` | C | 0.65 | SRP | NAcc DA + opioid, consummatory pleasure | done |
| 3 | `pleasure` | C | 0.7 | SRP | overall pleasure level integration | done |
| 4 | `prediction_error` | C | 0.5 | SRP | TD error (delta = R + gammaV' - V) | done |
| 5 | `tension` | C | 0.55 | SRP | tension-resolution dynamics | done |
| 6 | `prediction_match` | A | -- | SRP | prediction confirmed (+1) / violated (-1) | done |
| 7 | `peak_detection` | A | -- | SRP | musical peak/climax detection | done |
| 8 | `harmonic_tension` | A | -- | SRP | harmony far from tonic, unresolved | done |
| 9 | `dissociation_index` | A | -- | DAED | expectation-experience temporal dissociation | done |
| 10 | `temporal_phase` | A | -- | DAED | anticipation vs experience phase | done |
| 11 | `da_caudate` | A | -- | DAED | reward approaching, caudate DA ramp | done |
| 12 | `da_nacc` | A | -- | DAED | reward happening now, NAcc DA burst | done |
| 13 | `wanting_ramp` | N | -- | DAED | expectation increases as reward approaches | done |
| 14 | `chills_proximity` | N | -- | SRP | proximity to chills moment | done |
| 15 | `resolution_expectation` | N | -- | SRP | resolution expectation (deceptive -> extended) | done |
| 16 | `reward_forecast` | N | -- | SRP | upcoming reward estimate | done |

---

## 4. Observe Formula -- placeholder

No F6 mechanism models implemented yet. SRP and DAED relays are done (kernel v4.0).
F6 Core beliefs use MIXED tau (0.5-0.7), reflecting reward's moderate-to-slow temporal
persistence -- prediction_error is fastest (tau=0.5, rapid TD updates) while pleasure is
slowest (tau=0.7, integrated hedonic state).

**Reward formula** (kernel v4.0):
```
reward = sum(salience * (1.5*surprise + 0.8*resolution + 0.5*exploration - 0.6*monotony))
         * fam_mod * da_gain
```

Multi-scale horizons (to be defined per Core belief):
```
wanting:          TBD (single-scale, terminal aggregator)
liking:           TBD (single-scale, terminal aggregator)
pleasure:         TBD (single-scale, terminal aggregator)
prediction_error: TBD (single-scale, terminal aggregator)
tension:          TBD (single-scale, terminal aggregator)
```

---

## 5. Multi-Scale Horizons (all F6 Core Beliefs)

| Core Belief | T_char | Horizons | Band |
|-------------|--------|----------|------|
| wanting | ~2s | TBD | single-scale |
| liking | ~2s | TBD | single-scale |
| pleasure | ~4s | TBD | single-scale |
| prediction_error | ~0.5s | TBD | single-scale |
| tension | ~1s | TBD | single-scale |

---

## 6. Dependency Graph

```
                      R3 (97D) + H3
                          |
            +-------------+---------------+
            v             v               v
        SRP (a1)      DAED (a1)     MORMR (a2)    RPEM (a3)
        19D relay      8D             7D             8D
            |            |              |              |
     +------+-----+   +-+------+-------+              |
     v            v    v       v       v              |
  IUCP (b1)  MCCN(b2) MEAMR(b3) SSRI(b4)           |
    6D         7D       6D       11D                  |
     |            |      |         |                  |
     +----+-------+------+--------+                   |
     v    v              v         v                  |
  LDAC(g1) IOTMS(g2)  SSPS(g3)                      |
    6D      5D          6D                            |
```

### Key Dependencies

| Model | Reads From |
|-------|-----------|
| SRP (a1) | R3/H3 directly (relay) -- provides reward pathway from ARU |
| DAED (a1) | R3/H3 directly + BCH relay + MEAMN relay -- dopamine dissociation |
| MORMR (a2) | R3/H3 directly -- mu-opioid receptor reward |
| RPEM (a3) | R3/H3 directly -- reward prediction error; intra DAED, MORMR |
| IUCP (b1) | SRP, MORMR; inverted-U complexity preference |
| MCCN (b2) | SRP, DAED; musical chills cortical network; ->ARU (chills, arousal) |
| MEAMR (b3) | MEAMN relay (F4), SRP; autobiographical memory reward; ->IMU |
| SSRI (b4) | SRP, DAED; social synchrony reward integration; ->STU, ->ARU |
| LDAC (g1) | IUCP, MCCN; liking-dependent auditory cortex; ->ASU (sensory_gain) |
| IOTMS (g2) | MORMR, DAED; individual opioid tone sensitivity; ->ARU |
| SSPS (g3) | IUCP, MEAMR; saddle-shaped preference surface; ->IMU |

---

## 7. Unit Architecture

### RPU -- Reward Processing Unit (10 primary F6 models)

RPU is the **DOMINANT UNIT** for F6, housing 10 of 11 primary models.
RPU is the **SMALLEST OUTPUT** unit in the system -- models consistently produce 5-8D
(mean 7.0D). Reward signals are dimensionally compact. Only SSRI (11D, social synchrony)
breaks this pattern. RPU models lack M layers in b/g tiers (only a-tier + SSRI have M).

```
RPU models in F6:   DAED --- MORMR --- RPEM
                      |        |         |
                    IUCP --- MCCN --- MEAMR --- SSRI
                      |        |       |         |
                    LDAC --- IOTMS --- SSPS
```

Non-RPU model in F6:
- **ARU** (Aesthetic-Reward Unit): SRP (striatal reward pathway relay, 19D)

F6 also receives cross-function contributions from:
- **ARU** (Aesthetic-Reward Unit): PUPF (pharmacological), MAD (anhedonia)
- **PCU** (Predictive Coding Unit): UDP (surprise -> pleasure)
- **SPU** (Spectral Processing Unit): STAI (aesthetic -> reward)
- **ASU** (Attention-Salience Unit): AACM (liking -> attention feedback)

---

## 8. Documentation Structure

```
F6-Reward-and-Motivation/
+-- 0_F6-orchestrator.md                  <- this file
+-- collections.md                         <- full model inventory
+-- mechanisms/
|   +-- 0_mechanisms-orchestrator.md       <- all 11 models documented
|   +-- srp/ (4 layer docs)
|   +-- daed/ (4 layer docs)
|   +-- mormr/ (4 layer docs)
|   +-- rpem/ (4 layer docs)
|   +-- iucp/ (4 layer docs)
|   +-- mccn/ (4 layer docs)
|   +-- meamr/ (4 layer docs)
|   +-- ssri/ (4 layer docs)
|   +-- ldac/ (4 layer docs)
|   +-- iotms/ (4 layer docs)
|   +-- ssps/ (4 layer docs)
+-- beliefs/
    +-- 0_beliefs_orchestrator.md
    +-- srp/ (10 belief docs)
    +-- daed/ (6 belief docs)
```

**2 a-tier relays done (SRP ~124 H3 tuples, DAED 16 H3 tuples).** Pending: 2 a (MORMR, RPEM) + 4 b (IUCP, MCCN, MEAMR, SSRI) + 3 g (LDAC, IOTMS, SSPS) -- ~131 H3 tuples remaining.
