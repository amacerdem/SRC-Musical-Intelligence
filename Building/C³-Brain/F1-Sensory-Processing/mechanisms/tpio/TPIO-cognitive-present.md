# TPIO P-Layer — Cognitive Present (2D)

**Layer**: P (Present)
**Dimensions**: 2D (indices 5–6 of TPIO 10D output)
**Input**: H³ tuples + E-layer features
**Character**: Real-time brain region activation — pSTG and SMA states

---

## Overview

The P-layer represents the real-time activation state of the two key brain regions in the TPIO circuit: posterior STG (shared perception-imagery substrate) and supplementary motor area (imagery-specific motor simulation). These are the present-tense neural activation patterns that beliefs observe.

---

## P0: pSTG Activation (pstg_activation)

**Range**: [0, 1]
**Brain region**: Posterior STG (bilateral, right-weighted d=0.63)
**Question answered**: "What is the current activation level of the timbre processing hub?"

### Formula

```python
autocorr_mean = H3[(17, 8, 1, 0)]     # spectral_autocorrelation mean at H8
spec_chg_mean = H3[(21, 8, 1, 0)]     # spectral_change mean at H8
spec_chg_vel = H3[(21, 8, 8, 0)]      # spectral_change velocity at H8
timbre_chg = H3[(24, 8, 1, 0)]        # timbre_change mean at H8

pstg_activation = σ(0.30 * autocorr_mean
                    + 0.25 * spec_chg_mean
                    + 0.25 * spec_chg_vel
                    + 0.20 * timbre_chg)
# coefficients: 0.30 + 0.25 + 0.25 + 0.20 = 1.0 ✓
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Purpose |
|--------|---------|---|-------|-----|---------|
| 17 | spectral_autocorrelation | 8 | M1 (mean) | L0 | Harmonic periodicity at motif |
| 21 | spectral_change | 8 | M1 (mean) | L0 | Mean spectral flux |
| 21 | spectral_change | 8 | M8 (velocity) | L0 | Spectral change rate |
| 24 | timbre_change | 8 | M1 (mean) | L0 | Timbre evolution |

### Logic

Aggregates four motif-level (H8=300ms) spectral features that drive pSTG activation:
1. **Harmonic periodicity** (0.30): Instrument identity fingerprint (strongest weight)
2. **Spectral flux** (0.25): Timbral change rate — higher flux = more processing demand
3. **Spectral velocity** (0.25): Rate of spectral change acceleration
4. **Timbre change** (0.20): Instrument switching / timbral evolution

Right-hemisphere weighting (d=0.63 lateralization) is implicit in the model — the overall activation level represents the dominant (right) hemisphere contribution.

### Evidence
- Bellmann & Asano 2024: ALE meta-analysis, R-pSTG cluster 3,128 mm³ (9 experiments)
- Sturm et al. 2014: Spectral centroid drives high-gamma in temporal cortex (ECoG, n=10)

---

## P1: SMA Activation (sma_activation)

**Range**: [0, 1]
**Brain region**: Supplementary Motor Area (-6, -2, 60)
**Question answered**: "How active is the motor simulation system right now?"

### Formula

```python
tonalness_std = H3[(14, 14, 3, 0)]    # tonalness std at H14 (700ms)
trist1_autocorr = H3[(18, 20, 22, 0)] # tristimulus1 autocorrelation at H20

sma_activation = σ(0.40 * f04_sma_imagery
                  + 0.30 * (1.0 - tonalness_std)
                  + 0.30 * trist1_autocorr)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Purpose |
|--------|---------|---|-------|-----|---------|
| 14 | tonalness | 14 | M3 (std) | L0 | Tonalness variability at phrase |
| 18 | tristimulus1 | 20 | M22 (autocorr) | L0 | F0 self-similarity at section |

### Logic

Combines E-layer SMA imagery signal (E3) with phrase-level tonal stability and section-level spectral self-similarity:
1. **SMA imagery** (0.40): Direct imagery-driven motor simulation signal
2. **Tonal stability** (0.30): Low variability = stable timbre context → sustained motor simulation
3. **F0 self-similarity** (0.30): High autocorrelation = consistent instrument → motor rehearsal maintained

SMA is NOT activated during passive perception — only during imagery or motor simulation of timbre production.

### Evidence
- Halpern et al. 2004: SMA (-6, -2, 60), t=4.55 (imagery only, not perception)
- Zatorre & Halpern 2005: SMA consistent across imagery studies; no subvocalization component

---

## Layer Summary

| Idx | Name | Range | Key Inputs | Downstream |
|-----|------|-------|------------|------------|
| P0 | pstg_activation | [0, 1] | H³ spectral features at H8 | F-layer, → beliefs sensory state |
| P1 | sma_activation | [0, 1] | E3 + H³ stability at H14/H20 | F-layer, → AMSC motor coupling |

**Total P-layer H³ tuples**: 6 (4 unique to P0, 2 unique to P1)
