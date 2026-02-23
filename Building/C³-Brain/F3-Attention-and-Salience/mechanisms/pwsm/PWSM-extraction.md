# PWSM E-Layer — Extraction (3D)

**Layer**: E (Extraction)
**Dimensions**: 3D (indices 0–2 of PWSM 9D output)
**Input**: R³ direct + H³ tuples
**Character**: Precision-weighted salience features — precision gating, error suppression, stability encoding

---

## Overview

The E-layer extracts 3 features implementing the precision-weighted prediction error framework. The core finding: high-precision (stable) contexts generate MMN responses (d=-1.37), while low-precision (changing jitter) contexts abolish MMN entirely (d=0.01). Precision gates whether prediction errors are salient enough for neural response. Evidence: Basinski et al. 2025 (EEG), Millidge et al. 2022 (variational free energy framework), Fong et al. 2020 (MMN as precision-weighted PE).

---

## E0: Precision Weighting (f19_precision_weighting)

**Range**: [0, 1]
**Brain region**: STG / Auditory Cortex + Right Heschl's Gyrus
**Question answered**: "How precise is the current temporal context for error detection?"

### Formula

```python
onset_period_1s = H3[(10, 16, 17, 2)]    # spectral_flux periodicity at H16, bidi
energy_std_1s = H3[(22, 16, 2, 2)]       # energy_change std at H16, bidi
onset_std = H3[(11, 3, 2, 2)]            # onset_strength std at H3, bidi

f19_precision_weighting = σ(0.35 * onset_period_1s
                           + 0.35 * (1 - energy_std_1s)
                           + 0.30 * (1 - onset_std))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Purpose |
|--------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 16 | M17 (periodicity) | L2 | Beat-level onset periodicity |
| 22 | energy_change | 16 | M2 (std) | L2 | Energy stability over 1s |
| 11 | onset_strength | 3 | M2 (std) | L2 | Onset variability at 100ms |

### Logic

Three signals of context precision:
1. **Onset periodicity** (0.35): Regular beat structure → high precision (stable jitter)
2. **Energy stability** (0.35, inverted): Low energy variability → predictable dynamics
3. **Onset regularity** (0.30, inverted): Low onset variability → consistent timing

When all three are high: stable context → precision is high → prediction errors will be weighted strongly (MMN present). Basinski 2025: fixed jitter → d=-1.37 inharmonicity MMN.

### Evidence
- Basinski et al. 2025: Fixed jitter → MMN d=-1.37; changing jitter → d=0.01 (abolished)
- Bravo et al. 2017: Right HG response for ambiguous intervals (cluster FWE p<0.05)

---

## E1: Error Suppression (f20_error_suppression)

**Range**: [0, 1]
**Brain region**: IFG (top-down) + STG (bottom-up suppression)
**Question answered**: "How much are prediction errors being suppressed by low precision?"

### Formula

```python
pe_entropy = H3[(37, 3, 20, 2)]    # x_l4l5 entropy at H3, bidi
spectral_pe = H3[(21, 3, 0, 2)]    # spectral_change value at H3, bidi

f20_error_suppression = σ(0.35 * (1 - f19_precision_weighting)
                         + 0.35 * pe_entropy
                         + 0.30 * (1 - spectral_pe))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Purpose |
|--------|---------|---|-------|-----|---------|
| 37 | x_l4l5[0] | 3 | M20 (entropy) | L2 | PE entropy at 100ms |
| 21 | spectral_change | 3 | M0 (value) | L2 | Spectral PE current |

### Logic

Error suppression = inverse of precision + high PE entropy + low spectral deviation. When context is imprecise (low f19) AND PE patterns are unpredictable (high entropy), the brain suppresses error responses → MMN abolished. This is the predictive coding mechanism: uncertain contexts downweight prediction errors.

### Evidence
- Basinski et al. 2025: Changing jitter abolishes MMN (d=0.01, n.s.)
- Millidge et al. 2022: F = Σ Σ⁻¹ε²; precision as attention in free energy

---

## E2: Stability Encoding (f21_stability_encoding)

**Range**: [0, 1]
**Brain region**: IC → MGB → AC (hierarchical stability tracking)
**Question answered**: "How stable is the current jitter/timing pattern?"

### Formula

```python
spectral_std_1s = H3[(21, 16, 2, 2)]    # spectral_change std at H16, bidi

f21_stability_encoding = σ(0.35 * onset_period_1s
                          + 0.35 * (1 - spectral_std_1s)
                          + 0.30 * (1 - energy_std_1s))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Purpose |
|--------|---------|---|-------|-----|---------|
| 21 | spectral_change | 16 | M2 (std) | L2 | Spectral stability over 1s |

### Logic

Jitter pattern stability from onset periodicity, spectral stability, and energy stability at the 1s timescale. High stability → the brain can build reliable predictions → precision-weighted PE responses are enabled. Tracks the "fixed vs changing jitter" manipulation of Basinski 2025.

### Evidence
- Basinski et al. 2025: Fixed jitter = stable encoding → MMN; changing jitter = unstable → no MMN
- Carbajal & Malmierca 2018: SSA/MMN decomposition across IC→MGB→AC hierarchy

---

## Layer Summary

| Idx | Name | Range | Key Inputs | Downstream |
|-----|------|-------|------------|------------|
| E0 | f19_precision_weighting | [0, 1] | H³ periodicity+stability at H3/H16 | M-layer, E1, → IACM |
| E1 | f20_error_suppression | [0, 1] | E0 inverted + H³ entropy | M-layer, → beliefs |
| E2 | f21_stability_encoding | [0, 1] | H³ periodicity+std at H16 | F-layer, → SNEM |

**Total E-layer H³ tuples**: 6 (of PWSM's 16 total)
