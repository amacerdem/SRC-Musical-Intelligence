# PWSM F-Layer — Forecast (2D)

**Layer**: F (Forecast)
**Dimensions**: 2D (indices 7–8 of PWSM 9D output)
**Input**: E-layer + M-layer + P-layer features + H³ tuples
**Character**: Future predictions — MMN presence and context reliability forecasts

---

## Overview

The F-layer generates predictions about precision-weighted salience. Two outputs forecast: (1) whether an MMN response will be present in the upcoming 350ms window, and (2) the reliability of the current context over the next 2s. These predictions enable anticipatory precision allocation and are used by downstream beliefs for prediction error expectations.

---

## F0: MMN Presence Prediction (mmn_presence_pred_0.35s)

**Range**: [0, 1]
**Brain region**: STG + ACC (PE propagation and prediction)
**Question answered**: "Will an MMN response be present in the next 350ms?"

### Formula

```python
pe_phase_1s = H3[(37, 16, 21, 2)]   # x_l4l5 zero_crossings at H16, bidi

mmn_presence_pred = σ(0.35 * pe_weighted
                      + 0.30 * f19_precision_weighting
                      + 0.35 * (1 - pe_phase_1s))
# coefficients: 0.35 + 0.30 + 0.35 = 1.0 ✓
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Purpose |
|--------|---------|---|-------|-----|---------|
| 37 | x_l4l5[0] | 16 | M21 (zero_crossings) | L2 | PE phase resets over 1s |

### Logic

MMN prediction from current PE state and precision:
1. **PE weighted** (0.35): Strong precision-weighted PE → likely MMN in next window
2. **Precision** (0.30): High precision context → MMN expected (Basinski 2025)
3. **PE phase resets** (0.35, inverted): Few zero-crossings → stable PE direction → MMN more likely. Frequent phase resets → noisy PE → MMN less likely.

The 350ms prediction horizon aligns with the MMN latency window (100–250ms) plus processing buffer. Bonetti et al. 2024: hierarchical PE propagation from AC → hippocampus → cingulate occurs within this window.

### Evidence
- Basinski et al. 2025: Precision determines MMN presence/absence
- Bonetti et al. 2024: PE propagation hierarchy within 300–400ms (MEG, N=83)

---

## F1: Context Reliability Prediction (context_reliability_2s)

**Range**: [0, 1]
**Brain region**: IFG + AC (top-down reliability estimation)
**Question answered**: "How reliable will the temporal context be over the next 2 seconds?"

### Formula

```python
pe_period_1s = H3[(37, 16, 17, 2)]  # x_l4l5 periodicity at H16, bidi

context_reliability = σ(0.35 * f21_stability_encoding
                        + 0.35 * precision
                        + 0.30 * pe_period_1s)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Purpose |
|--------|---------|---|-------|-----|---------|
| 37 | x_l4l5[0] | 16 | M17 (periodicity) | L2 | PE pattern periodicity at 1s |

### Logic

Context reliability from stability and precision:
1. **Stability encoding** (0.35): E-layer stability → reliable context persists
2. **Precision** (0.35): M-layer precision → high precision predicts continued reliability
3. **PE periodicity** (0.30): Regular PE patterns at 1s → context maintains structure → reliability high

The 2s prediction horizon covers approximately 2 beat cycles in typical music (60–120 BPM), allowing precision estimation to anticipate upcoming context changes. Gold et al. 2019: predictability over this timescale modulates pleasure responses.

### Evidence
- Gold et al. 2019: Predictive complexity over seconds modulates pleasure (inverted-U)
- Schilling et al. 2023: Precision of likelihood determines perception quality

---

## Layer Summary

| Idx | Name | Range | Key Inputs | Downstream |
|-----|------|-------|------------|------------|
| F0 | mmn_presence_pred_0.35s | [0, 1] | M0 + E0 + H³ PE zero-crossings at H16 | → beliefs PE expectation |
| F1 | context_reliability_2s | [0, 1] | E2 + M1 + H³ PE periodicity at H16 | → NDU context, → beliefs |

**Total F-layer H³ tuples**: 2 (1 unique to F0, 1 unique to F1)

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f19_precision_weighting | Precision input for MMN prediction |
| E-layer | f21_stability_encoding | Stability for reliability estimation |
| M-layer | pe_weighted | PE magnitude for MMN prediction |
| M-layer | precision | Precision level for reliability |
| H³ | 2 unique tuples | Long-range PE patterns at H16 |
