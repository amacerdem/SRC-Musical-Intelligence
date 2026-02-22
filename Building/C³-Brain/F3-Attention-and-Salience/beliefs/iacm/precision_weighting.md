# precision_weighting — Appraisal Belief (IACM)

**Category**: Appraisal (observe-only)
**Owner**: IACM (ASU-alpha2)

---

## Definition

"Context stability determines PE weight." Observes the degree to which the current auditory context provides stable precision for prediction error weighting. High precision weighting means the context is stable and predictable, so prediction errors carry more weight (they are informative). Low precision weighting means the context is volatile, so prediction errors are down-weighted (they are expected).

---

## Observation Formula

```
# Direct read from IACM E-layer:
precision_weighting = IACM.precision_weighting[E2]  # index [2]

# Formula: sigma(0.40*periodicity_value + 0.30*tonalness_period_1s + 0.30*coupling_phase_resets)
# periodicity_value = H3 (14, 0, 0, 2) tonalness 25ms
# tonalness_period_1s = H3 (14, 16, 14, 2) tonalness periodicity 1s
# coupling_phase_resets = H3 (25, 16, 21, 2) x_l0l5 zero_crossings 1s
```

No prediction — observe-only appraisal. The value modulates the precision engine's weighting of prediction errors from other beliefs.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| IACM E2 | precision_weighting [2] | Context-dependent precision state |
| H3 | (14, 0, 0, 2) | Tonalness value 25ms — instantaneous tonal quality |
| H3 | (14, 16, 14, 2) | Tonalness periodicity 1s — tonal stability |
| H3 | (25, 16, 21, 2) | Coupling zero_crossings 1s — phase resets |

---

## Kernel Usage

The precision_weighting appraisal modulates the precision engine:

```python
# Precision engine integration:
# pi_context = precision_weighting * pi_base
# High precision_weighting: PE is informative (stable context disrupted)
# Low precision_weighting: PE is expected (volatile context)
```

This implements Friston's precision-weighted predictive coding: the same magnitude prediction error carries different information depending on the stability of the context in which it occurs. A deviant in a stable tonal context (high precision) is highly informative, while a deviant in a chaotic passage (low precision) is unremarkable.

---

## Scientific Foundation

- **Friston 2005**: Precision-weighted prediction errors in predictive coding framework
- **Basinski 2025**: Context-dependent P3a modulation (EEG, N=35)
- **Koelsch 1999**: Musical context modulates deviant detection
- **Alain 2007**: ORN amplitude depends on spectral context stability

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/iacm_relay.py` (pending)
