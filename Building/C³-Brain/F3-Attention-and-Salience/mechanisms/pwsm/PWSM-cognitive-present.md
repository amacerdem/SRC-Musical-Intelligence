# PWSM P-Layer — Cognitive Present (2D)

**Layer**: P (Present)
**Dimensions**: 2D (indices 5–6 of PWSM 9D output)
**Input**: E-layer + M-layer features + H³ tuples
**Character**: Real-time precision-weighted processing — attended error and precision state

---

## Overview

The P-layer represents the current processing state of the precision-weighted salience system. Two outputs capture: (1) the attention-modulated weighted error signal that determines whether a deviant triggers a neural response, and (2) the ongoing precision estimate based on beat-level regularity. These are the present-tense signals that beliefs observe for salience gating.

---

## P0: Weighted Error (weighted_error)

**Range**: [0, 1]
**Brain region**: STG (PE generation) + Anterior Insula (salience network)
**Question answered**: "What is the current attention-weighted prediction error?"

### Formula

```python
pe_period = H3[(37, 3, 17, 2)]      # x_l4l5 periodicity at H3, bidi

weighted_error = σ(0.35 * pe_weighted
                   + 0.35 * f19_precision_weighting
                   + 0.30 * pe_period)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Purpose |
|--------|---------|---|-------|-----|---------|
| 37 | x_l4l5[0] | 3 | M17 (periodicity) | L2 | PE regularity at 100ms |

### Logic

Combines three signals for attentional error gating:
1. **PE weighted** (0.35): The precision-modulated PE from M-layer — the core signal
2. **Precision** (0.35): Current context precision → attention allocation (Millidge 2022: precision as attention)
3. **PE regularity** (0.30): Periodic PE patterns indicate systematic deviations rather than noise → higher salience

When PE is weighted AND context is precise AND PE pattern is regular → strong weighted error → MMN and neural response. Cheung et al. 2019: uncertainty × surprise → pleasure; this feature captures the neural processing of that interaction.

### Evidence
- Cheung et al. 2019: Uncertainty × surprise interaction in amygdala/AC
- Millidge et al. 2022: Precision as attention in free energy framework

---

## P1: Precision Estimate (precision_estimate)

**Range**: [0, 1]
**Brain region**: AC → MGB → IC (hierarchical precision propagation)
**Question answered**: "What is the current beat-level precision estimate?"

### Formula

```python
onset_value = H3[(11, 3, 0, 2)]     # onset_strength value at H3, bidi

precision_estimate = σ(0.40 * onset_period_1s
                       + 0.30 * onset_value
                       + 0.30 * (1 - onset_std))
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓
# Uses onset_period_1s and onset_std from E-layer
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Purpose |
|--------|---------|---|-------|-----|---------|
| 11 | onset_strength | 3 | M0 (value) | L2 | Current onset strength at 100ms |

### Logic

Beat-level precision from onset regularity:
1. **Onset periodicity** (0.40): 1s-scale onset regularity — the strongest precision cue (fixed jitter = high)
2. **Onset value** (0.30): Current onset strength — strong onsets provide better precision anchors
3. **Onset regularity** (0.30, inverted std): Low variability → reliable timing → high precision

This provides a real-time precision estimate that SNEM can use for beat prediction confidence and that the F-layer uses for MMN prediction. The hierarchical propagation from AC→MGB→IC mirrors precision estimation across the auditory pathway (Carbajal & Malmierca 2018).

### Evidence
- Carbajal & Malmierca 2018: Hierarchical precision across IC→MGB→AC
- Cacciato-Salcedo et al. 2025: Subcortical PE generation modulated by context

---

## Layer Summary

| Idx | Name | Range | Key Inputs | Downstream |
|-----|------|-------|------------|------------|
| P0 | weighted_error | [0, 1] | M0 + E0 + H³ PE periodicity at H3 | F-layer, → beliefs salience |
| P1 | precision_estimate | [0, 1] | E-layer onset features + H³ onset value at H3 | F-layer, → SNEM |

**Total P-layer H³ tuples**: 2 (1 unique to P0, 1 unique to P1)

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f19_precision_weighting | Precision signal for attention weighting |
| E-layer | onset_period_1s, onset_std | Shared onset features for precision estimate |
| M-layer | pe_weighted | Core precision-weighted PE for error signal |
| H³ | 2 unique tuples | PE regularity + onset value |
