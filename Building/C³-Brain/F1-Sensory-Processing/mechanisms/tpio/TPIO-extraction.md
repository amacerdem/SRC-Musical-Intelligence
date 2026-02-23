# TPIO E-Layer — Extraction (4D)

**Layer**: E (Extraction)
**Dimensions**: 4D (indices 0–3 of TPIO 10D output)
**Input**: R³ direct + H³ tuples
**Character**: Timbre perception-imagery overlap features — shared pSTG substrate and SMA motor simulation

---

## Overview

The E-layer extracts 4 features capturing the neural substrate for timbre processing during both perception and imagery. The core finding is that posterior STG (pSTG) is activated in both conditions with behavioral correlation r=0.84 (Halpern et al. 2004). SMA engagement during imagery (d=0.90) suggests motor simulation without execution. Evidence: 12 papers, 7 methods (fMRI, MEG, ECoG, iEEG, EEG, ALE meta-analysis, behavioral MDS).

---

## E0: Perception Substrate (f01_perception_substrate)

**Range**: [0, 1]
**Brain region**: Posterior STG (pSTG) — timbre perception encoding
**Question answered**: "How strongly is the pSTG encoding timbre during perception?"

### Formula

```python
warmth_val = H3[(12, 2, 0, 2)]      # warmth value at H2 (17ms), bidi
sharpness_val = H3[(13, 2, 0, 2)]   # sharpness value at H2, bidi
tonalness_mean = H3[(14, 5, 1, 0)]  # tonalness mean at H5 (46ms)
clarity_val = H3[(15, 5, 0, 0)]     # clarity value at H5
trist1 = H3[(18, 2, 0, 2)]          # tristimulus1 at H2, bidi
trist2 = H3[(19, 2, 0, 2)]          # tristimulus2 at H2, bidi
trist3 = H3[(20, 2, 0, 2)]          # tristimulus3 at H2, bidi
trist_balance = (trist1 + trist2 + trist3) / 3

f01_perception_substrate = σ(0.35 * warmth_val * sharpness_val
                            + 0.35 * trist_balance
                            + 0.30 * tonalness_mean * clarity_val)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Purpose |
|--------|---------|---|-------|-----|---------|
| 12 | warmth | 2 | M0 (value) | L2 | Low-frequency balance at gamma |
| 13 | sharpness | 2 | M0 (value) | L2 | High-frequency weighting |
| 14 | tonalness | 5 | M1 (mean) | L0 | Mean tonal clarity at alpha |
| 15 | clarity | 5 | M0 (value) | L0 | Brightness proxy |
| 18 | tristimulus1 | 2 | M0 (value) | L2 | F0 energy |
| 19 | tristimulus2 | 2 | M0 (value) | L2 | Mid-harmonic energy |
| 20 | tristimulus3 | 2 | M0 (value) | L2 | High-harmonic energy |

### Logic

Three components of timbre perception:
1. **Warmth × Sharpness** (0.35): Spectral envelope quality — low-high frequency balance at gamma timescale
2. **Tristimulus balance** (0.35): Harmonic energy distribution — instrument identity fingerprint
3. **Tonalness × Clarity** (0.30): Pitch-timbre interaction — harmonic purity

All at fast timescales (H2=17ms, H5=46ms) reflecting real-time spectral processing in pSTG.

### Evidence
- Halpern et al. 2004: pSTG conjunction, R-pSTG t=4.66; L-PT t=4.98 (fMRI, n=10)
- Alluri et al. 2012: Timbral features correlate with bilateral STG, R-STG Z=8.13 (fMRI, n=11)

---

## E1: Imagery Substrate (f02_imagery_substrate)

**Range**: [0, 1]
**Brain region**: Posterior STG (pSTG) — timbre imagery retrieval
**Question answered**: "How strongly is the pSTG encoding timbre during imagery?"

### Formula

```python
warmth_phrase = H3[(12, 14, 1, 0)]     # warmth mean at H14 (700ms)
tonalness_phrase = H3[(14, 14, 1, 0)]  # tonalness mean at H14
trist1_long = H3[(18, 20, 1, 0)]       # tristimulus1 mean at H20 (5000ms)

f02_imagery_substrate = σ(0.35 * warmth_phrase
                         + 0.35 * tonalness_phrase
                         + 0.30 * trist1_long)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Purpose |
|--------|---------|---|-------|-----|---------|
| 12 | warmth | 14 | M1 (mean) | L0 | Mean warmth over phrase |
| 14 | tonalness | 14 | M1 (mean) | L0 | Mean tonalness over phrase |
| 18 | tristimulus1 | 20 | M1 (mean) | L0 | Long-range F0 energy |

### Logic

Imagery operates at longer timescales than perception — phrase (700ms) and section (5000ms) horizons. The same spectral features (warmth, tonalness, tristimulus) but integrated over temporal memory windows. When long-range spectral context is rich and stable, the imagery substrate is active.

### Evidence
- Zatorre & Halpern 2005: Secondary AC reliably activated during musical imagery (review)
- Halpern et al. 2004: Right > left imagery, t=1.97, p=0.04 (7/10 subjects)

---

## E2: Perception-Imagery Overlap (f03_perc_imag_overlap)

**Range**: [0, ~0.84]
**Brain region**: pSTG shared substrate (bilateral, right-dominant)
**Question answered**: "How much do perception and imagery share the same neural code?"

### Formula

```python
f03_perc_imag_overlap = 0.84 * f01_perception_substrate * f02_imagery_substrate
```

### Dependencies

| Source | Feature | Role |
|--------|---------|------|
| E0 | f01_perception_substrate | Perception encoding quality |
| E1 | f02_imagery_substrate | Imagery retrieval quality |

### Logic

Direct product of perception and imagery substrates, scaled by the behavioral correlation coefficient r=0.84 (Halpern 2004). When both pathways are active and strong, the overlap is maximal. The product structure ensures overlap requires BOTH components — imagery alone or perception alone yields low overlap.

### Evidence
- Halpern et al. 2004: r(26)=0.84, p<0.001 (perception-imagery behavioral MDS)
- Halpern et al. 2004: r=0.90 excluding flute-violin outlier pair

---

## E3: SMA Imagery (f04_sma_imagery)

**Range**: [0, 1]
**Brain region**: Supplementary Motor Area (SMA) — non-motor imagery
**Question answered**: "How engaged is the motor simulation system during timbre imagery?"

### Formula

```python
loudness_section = H3[(8, 20, 1, 0)]     # loudness mean at H20 (5000ms)
amplitude_trend = H3[(7, 20, 18, 0)]     # amplitude trend at H20
engagement = σ(0.50 * loudness_section + 0.50 * amplitude_trend)
# coefficients: 0.50 + 0.50 = 1.0 ✓

f04_sma_imagery = σ(0.90 * f02_imagery_substrate * engagement)
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Purpose |
|--------|---------|---|-------|-----|---------|
| 8 | loudness | 20 | M1 (mean) | L0 | Mean loudness over section |
| 7 | amplitude | 20 | M18 (trend) | L0 | Long-range intensity trend |

### Logic

SMA activation during imagery = imagery substrate × engagement level, scaled by d=0.90. Engagement is a blend of section-level loudness and amplitude trend. The SMA is NOT activated during perception — it specifically reflects motor simulation of timbre production during imagery.

**Note**: The d=0.90 is approximate — derived from t=4.55 (Halpern 2004), which was subthreshold at whole-brain level. Retained as the model constant.

### Evidence
- Halpern et al. 2004: SMA (-6, -2, 60), t=4.55 (subthreshold whole-brain)
- Zatorre & Halpern 2005: SMA consistently found across imagery studies

---

## Layer Summary

| Idx | Name | Range | Key Inputs | Downstream |
|-----|------|-------|------------|------------|
| E0 | f01_perception_substrate | [0, 1] | H³ timbre at H2/H5 | M-layer, P-layer |
| E1 | f02_imagery_substrate | [0, 1] | H³ timbre at H14/H20 | M-layer, P-layer, E3 |
| E2 | f03_perc_imag_overlap | [0, ~0.84] | E0 × E1 × 0.84 | F-layer, → ARU |
| E3 | f04_sma_imagery | [0, 1] | E1 × engagement × 0.90 | P-layer, → AMSC |

**Total E-layer H³ tuples**: 12 (of TPIO's 18 total)
