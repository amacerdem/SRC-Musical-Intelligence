# PWSM M-Layer — Temporal Integration (2D)

**Layer**: M (Temporal Integration)
**Dimensions**: 2D (indices 3–4 of PWSM 9D output)
**Input**: E-layer features + H³ tuples + R³ direct
**Character**: Mathematical precision-weighted PE — raw PE modulated by context precision

---

## Overview

The M-layer implements the core mathematical operation of predictive coding: PE_weighted = PE_raw × Precision. This is the variational free energy computation where precision (inverse variance) gates whether prediction errors are propagated. From Millidge et al. 2022: F = Σ Σ⁻¹ε² — precision-weighted prediction errors minimize free energy. The M-layer computes both the raw precision-weighted PE signal and the context precision estimate across multiple temporal scales.

---

## M0: Precision-Weighted PE (pe_weighted)

**Range**: [0, 1]
**Brain region**: STG → IFG (PE propagation pathway)
**Question answered**: "What is the precision-weighted prediction error magnitude?"

### Formula

```python
flux_100ms = H3[(10, 3, 0, 2)]      # spectral_flux value at H3, bidi
energy_pe = H3[(22, 3, 0, 2)]       # energy_change value at H3, bidi
pe_interact = H3[(37, 3, 0, 2)]     # x_l4l5 value at H3, bidi

pe_raw = σ(0.30 * flux_100ms
           + 0.35 * energy_pe
           + 0.35 * pe_interact)
# coefficients: 0.30 + 0.35 + 0.35 = 1.0 ✓

pe_weighted = pe_raw × f19_precision_weighting
# Precision gates raw PE: high precision → full PE; low precision → suppressed
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Purpose |
|--------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 3 | M0 (value) | L2 | Onset PE at 100ms alpha |
| 22 | energy_change | 3 | M0 (value) | L2 | Energy PE at 100ms |
| 37 | x_l4l5[0] | 3 | M0 (value) | L2 | Weighted PE interaction at 100ms |

### Logic

Three PE signals at the 100ms alpha timescale:
1. **Onset flux** (0.30): Spectral flux captures event-level prediction errors
2. **Energy PE** (0.35): Energy change deviation from expected dynamics
3. **PE interaction** (0.35): Derivatives × perceptual cross-domain PE signal

The raw PE is then multiplicatively gated by f19 (precision weighting from E-layer). This implements the core predictive coding equation: PE_weighted = PE × Precision. When precision is high (stable context), PE passes through fully → MMN present. When precision is low (unstable jitter), PE is suppressed → MMN abolished.

### Evidence
- Millidge et al. 2022: F = Σ Σ⁻¹ε²; precision multiplicatively weights PE
- Basinski et al. 2025: Precision manipulation modulates PE response magnitude

---

## M1: Precision (precision)

**Range**: [0, 1]
**Brain region**: STG / Auditory Cortex (hierarchical precision estimation)
**Question answered**: "What is the current precision (inverse variance) of the temporal context?"

### Formula

```python
onset_25ms = H3[(10, 0, 0, 2)]      # spectral_flux value at H0, bidi
onset_50ms = H3[(10, 1, 1, 2)]      # spectral_flux mean at H1, bidi
onset_theta = H3[(10, 4, 17, 2)]    # spectral_flux periodicity at H4, bidi

precision = σ(0.30 * onset_25ms
              + 0.30 * onset_50ms
              + 0.40 * onset_theta)
# coefficients: 0.30 + 0.30 + 0.40 = 1.0 ✓
# Models Precision ∝ 1/(1+σ²_context) via multi-scale onset regularity
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Purpose |
|--------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 0 | M0 (value) | L2 | Gamma-rate onset detection (25ms) |
| 10 | spectral_flux | 1 | M1 (mean) | L2 | Mean onset at 50ms gamma |
| 10 | spectral_flux | 4 | M17 (periodicity) | L2 | Onset periodicity at 125ms theta |

### Logic

Multi-scale onset features estimate context precision:
1. **Gamma onset** (0.30): Instantaneous event detection at 25ms — the raw input to precision
2. **Mean onset** (0.30): Smoothed onset at 50ms — reduces noise in precision estimate
3. **Theta periodicity** (0.40, highest weight): Onset regularity at 125ms theta — the critical timescale for inter-onset interval variance estimation

Together these implement Precision ∝ 1/(1+σ²_context). Regular onsets (high periodicity) → high precision. Irregular onsets → low precision. The theta timescale (125ms) captures the inter-stimulus interval regularity that Basinski 2025 manipulated with fixed vs. changing jitter.

### Evidence
- Basinski et al. 2025: Inter-onset interval variance determines precision (fixed vs changing jitter)
- Fong et al. 2020: Precision estimation across auditory hierarchy (IC→MGB→AC)

---

## Layer Summary

| Idx | Name | Range | Key Inputs | Downstream |
|-----|------|-------|------------|------------|
| M0 | pe_weighted | [0, 1] | E0 × H³ PE signals at H3 | P-layer, F-layer, → beliefs |
| M1 | precision | [0, 1] | H³ onset multi-scale at H0/H1/H4 | P-layer, F-layer, → IACM |

**Total M-layer H³ tuples**: 6 (3 unique to M0, 3 unique to M1)

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f19_precision_weighting | Multiplicative precision gate for PE |
| H³ | 6 unique tuples | PE signals (3) + multi-scale precision (3) |
| R³ | spectral_change[21], energy_change[22] | Raw PE sources (indirect via H³) |
