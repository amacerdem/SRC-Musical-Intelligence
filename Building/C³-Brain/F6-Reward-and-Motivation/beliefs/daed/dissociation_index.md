# dissociation_index — Appraisal Belief (DAED)

**Category**: Appraisal (observe-only)
**Owner**: DAED (RPU-a1)

---

## Definition

"Expectation and experience temporally dissociated." Observes the magnitude of temporal-anatomical dissociation between anticipatory dopamine (caudate) and consummatory dopamine (NAcc). High dissociation means the listener is strongly in one phase or the other; low dissociation means both systems are similarly active (transition zone or neutral state).

---

## Observation Formula

```
# Direct read from DAED M-layer:
dissociation_index = DAED.dissociation_index[M0]  # index [4]

# Formula: |f01_anticipatory_da - f02_consummatory_da|
# where:
#   f01 = sigma(0.35 * loudness_velocity_1s
#               + 0.20 * spectral_uncertainty_125ms
#               + 0.15 * roughness_velocity_500ms)
#   f02 = sigma(0.35 * mean_pleasantness_1s
#               + 0.15 * mean_loudness_1s)
```

No prediction -- observe-only appraisal. The value is directly consumed by the reward formula and downstream beliefs as a phase-separation indicator.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| DAED M0 | dissociation_index [4] | Absolute difference of anticipatory vs consummatory DA |
| DAED E0 | f01_anticipatory_da [0] | Caudate DA proxy (anticipation signal) |
| DAED E1 | f02_consummatory_da [1] | NAcc DA proxy (consummation signal) |
| H3 | (8, 16, 8, 0) | Loudness velocity at 1s -- drives f01 |
| H3 | (0, 8, 8, 0) | Roughness velocity at 500ms -- drives f01 |
| H3 | (21, 4, 20, 0) | Spectral uncertainty at 125ms -- drives f01 |
| H3 | (4, 16, 1, 2) | Mean pleasantness at 1s -- drives f02 |
| H3 | (8, 16, 1, 2) | Mean loudness at 1s -- drives f02 |

---

## Kernel Usage

The dissociation_index appraisal provides phase-separation information to the reward computation:

```python
# Phase 5 in scheduler:
# High dissociation = clear anticipation OR consummation phase
# Low dissociation = transition zone or neutral
dissociation = daed_relay['dissociation_index']  # |f01 - f02|
```

This value contextualizes the reward signal: when dissociation is high, the reward system can confidently apply phase-specific processing (anticipatory weighting vs consummatory pleasure). When low, the system is in a mixed or neutral state.

---

## Scientific Foundation

- **Salimpoor 2011**: PET [11C]raclopride shows anatomically distinct DA release -- caudate during anticipation (r = 0.71 with chills count), NAcc during experience (r = 0.84 with pleasure rating)
- **Mohebi 2024**: DA transients follow striatal gradient of reward time horizons (ventral->dorsal), supporting temporal-anatomical dissociation
- **Gold 2023**: VS and R STG reflect pleasure of musical expectancies; VS activity shows liking x surprise interaction

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/daed_relay.py` (planned)
Source model: `Musical_Intelligence/brain/functions/f6/mechanisms/daed/`
