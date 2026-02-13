# C3 Cognitive Units -- Index

9 cognitive units model distinct neural circuits and cognitive functions within the MI-Beta brain architecture. Each unit contains multiple models at three evidence tiers (alpha, beta, gamma).

---

## Unit Roster

| Unit | Full Name | Circuit | Pooled *d* | Models | Output Dim | Dependency |
|------|-----------|---------|-----------|--------|-----------|------------|
| [SPU](SPU.md) | Spectral Processing Unit | perceptual | 0.84 | 9 | 99D | Independent |
| [STU](STU.md) | Sensorimotor Timing Unit | sensorimotor | 0.67 | 14 | 148D | Independent |
| [IMU](IMU.md) | Integrative Memory Unit | mnemonic | 0.53 | 15 | 159D | Independent |
| [ASU](ASU.md) | Auditory Salience Unit | salience | 0.60 | 9 | 94D | Independent |
| [NDU](NDU.md) | Novelty Detection Unit | salience | 0.55 | 9 | 94D | Independent |
| [MPU](MPU.md) | Motor Planning Unit | sensorimotor | 0.62 | 10 | 104D | Independent |
| [PCU](PCU.md) | Predictive Coding Unit | mnemonic | 0.58 | 9 | 94D | Independent |
| [ARU](ARU.md) | Affective Resonance Unit | mesolimbic | 0.83 | 10 | 120D | Dependent |
| [RPU](RPU.md) | Reward Processing Unit | mesolimbic | 0.70 | 9 | 94D | Dependent |

**Total: 94 models, 1006D brain output**

---

## Execution Order

Defined in `mi_beta.core.constants.UNIT_EXECUTION_ORDER`:

```
Phase 2 (Independent):   SPU -> STU -> IMU -> ASU -> NDU -> MPU -> PCU
                            |      |      |
Phase 3 (Pathways):        P1     P5     P3
                            |      |      |
                            v      v      v
Phase 4 (Dependent):              ARU -> RPU
```

Independent units read only from H3/R3 inputs. Dependent units (ARU, RPU) additionally receive cross-unit signals routed by the `PathwayRunner`.

---

## Core-4 (Validated)

Units with k >= 10 studies and meta-analytic pooled effect sizes:

| Rank | Unit | Pooled *d* | Circuit | Models | Dim |
|------|------|-----------|---------|--------|-----|
| 1 | SPU | 0.84 | perceptual | 9 | 99D |
| 2 | ARU | 0.83 | mesolimbic | 10 | 120D |
| 3 | STU | 0.67 | sensorimotor | 14 | 148D |
| 4 | IMU | 0.53 | mnemonic | 15 | 159D |

---

## Experimental-5

Units with k < 10 studies:

| Rank | Unit | Pooled *d* | Circuit | Models | Dim |
|------|------|-----------|---------|--------|-----|
| 1 | RPU | 0.70 | mesolimbic | 9 | 94D |
| 2 | MPU | 0.62 | sensorimotor | 10 | 104D |
| 3 | ASU | 0.60 | salience | 9 | 94D |
| 4 | PCU | 0.58 | mnemonic | 9 | 94D |
| 5 | NDU | 0.55 | salience | 9 | 94D |

---

## Units by Circuit

| Circuit | Units | Combined Dim |
|---------|-------|-------------|
| perceptual | SPU | 99D |
| sensorimotor | STU, MPU | 252D |
| mnemonic | IMU, PCU | 253D |
| mesolimbic | ARU, RPU | 214D |
| salience | ASU, NDU | 188D |

---

## Code Reference

- Unit registry: `mi_beta.brain.units.__init__`
- Unit runner: `mi_beta.brain.units.UnitRunner`
- Constants: `mi_beta.core.constants.UNIT_EXECUTION_ORDER`
- Base class: `mi_beta.contracts.BaseCognitiveUnit`

## See Also

- [C3 Architecture](../C3-ARCHITECTURE.md)
- [Models Index](../Models/00-INDEX.md)
- [Mechanisms](../Mechanisms/)
- [Pathways](../Pathways/)
