# PSCL E-Layer — Extraction (4D)

**Layer**: E (Extraction)
**Dimensions**: 4D (indices 0–3 of PSCL 16D output)
**Input**: R³ direct features only (no H³, no BCH upstream)
**Character**: Instantaneous cortical pitch salience features — frame-local, no temporal integration

---

## Overview

The E-layer computes 4 instantaneous acoustic measures from R³ features. These represent the cortex's immediate assessment of pitch salience and spectral structure — the "raw material" for cortical pitch processing in anterolateral Heschl's Gyrus.

Like BCH's E-layer, no sigmoid gating or temporal smoothing is applied. Output ceilings (0.80–0.90) preserve dynamic range for downstream integration.

---

## E0: Pitch Salience Raw

**Range**: [0, 0.90]
**Brain region**: Anterolateral HG (pitch salience sensitivity)
**Question answered**: "How prominent is the pitch at this instant?"

### Formula

```python
E0_pitch_salience_raw = 0.90 * (
    0.40 * R3[39]                    # direct pitch salience
  + 0.35 * R3[14] * R3[17]          # tonalness × autocorrelation (proxy)
  + 0.25 * R3[24]                    # spectral concentration
)
```

### R³ Inputs

| R³ Index | Feature | Role |
|----------|---------|------|
| **[39]** | pitch_salience | Direct harmonic peak prominence (Parncutt 1989) |
| **[14]** | tonalness | Harmonic-to-noise ratio — pitch clarity proxy |
| **[17]** | spectral_autocorrelation | Harmonic periodicity in spectrum |
| **[24]** | distribution_concentration | Spectral energy focus (Herfindahl) |

### Logic

Three complementary pitch salience measures:
1. **Direct** (40%): R³'s pitch_salience — the most explicit measure of pitch prominence
2. **Proxy** (35%): Tonalness × autocorrelation — captures pitch clarity from spectral structure
3. **Focus** (25%): Spectral concentration — how peaked the energy distribution is

The 0.90 ceiling matches BCH E0 (NPS), as PSCL's extraction inherits the same dynamic range.

### Evidence
- Penagos 2004: alHG responds parametrically with pitch salience (fMRI, N=6)
- Parncutt 1989: Virtual pitch salience = harmonic peak prominence

---

## E1: HG Activation Proxy

**Range**: [0, 0.85]
**Brain region**: Anterolateral HG (non-primary auditory cortex)
**Question answered**: "How strongly does Heschl's Gyrus respond to this stimulus?"

### Formula

```python
E1_hg_activation_proxy = 0.85 * (1 - R3[5]) * (
    0.50 * R3[18]                    # tristimulus1 (F0 strength)
  + 0.30 * R3[16]                    # spectral smoothness
  + 0.20 * R3[39]                    # pitch salience
)
```

### R³ Inputs

| R³ Index | Feature | Role |
|----------|---------|------|
| **[5]** | inharmonicity (inv) | Gate: Low inharmonicity → high HG response |
| **[18]** | tristimulus1 | Fundamental energy — F0 drives pitch-selective neurons |
| **[16]** | spectral_smoothness | Smooth spectrum → resolved harmonics |
| **[39]** | pitch_salience | Direct salience measure enriches HG estimate |

### Logic

The inharmonicity gate (`1 - R3[5]`) ensures that only harmonic sounds activate HG strongly. Inside the gate, three factors contribute:
1. **F0 strength** (50%): Strong fundamental is the primary pitch cue for cortical neurons
2. **Spectral smoothness** (30%): Smooth spectra have resolved harmonics — easier to extract pitch
3. **Pitch salience** (20%): Direct confirmation of pitch prominence

The 0.85 ceiling differentiates cortical activation from brainstem NPS — cortical responses are slightly attenuated relative to brainstem precision.

### Evidence
- Penagos 2004: 9/10 hemispheres showed parametric HG activation with pitch salience
- Schonwiesner & Zatorre 2008: Lateral HG = pitch, medial HG = sound onset (double dissociation)
- Allen 2022: ~18% pitch-only voxels outside HG (focal but not exclusive)

---

## E2: Salience Gradient

**Range**: [0, 0.80]
**Brain region**: Anterolateral HG (parametric response)
**Question answered**: "Where does this stimulus sit in the Strong > Weak > Noise ordering?"

### Formula

```python
E2_salience_gradient = 0.80 * (1 - R3[22]) * (1 - R3[23]) * R3[4]
```

### R³ Inputs

| R³ Index | Feature | Role |
|----------|---------|------|
| **[22]** | distribution_entropy (inv) | Low entropy = tonal/ordered signal |
| **[23]** | distribution_flatness (inv) | Low flatness = peaked spectrum (not noise) |
| **[4]** | sensory_pleasantness | Spectral regularity = high salience |

### Logic

Three-way product captures the salience hierarchy:
- **Noise**: High entropy × high flatness → product near 0
- **Weak pitch**: Moderate values → intermediate product
- **Strong pitch**: Low entropy × low flatness × high pleasantness → product near 0.80

This mirrors the parametric relationship found by Penagos 2004: HG activation scales with pitch salience even when temporal regularity is controlled.

### Evidence
- Penagos 2004: Strong > Weak > Noise gradient with matched temporal regularity
- Bravo 2017: Right HG upregulated for low-salience (ambiguous) stimuli (t=4.22)

---

## E3: Spectral Focus

**Range**: [0, 1]
**Brain region**: Cortical spectral analysis
**Question answered**: "How focused is spectral energy for pitch extraction?"

### Formula

```python
E3_spectral_focus = R3[24] * R3[15] * (1 - R3[23])
```

### R³ Inputs

| R³ Index | Feature | Role |
|----------|---------|------|
| **[24]** | distribution_concentration | Herfindahl index — energy focused in few bins |
| **[15]** | clarity | Signal clarity for pitch extraction |
| **[23]** | distribution_flatness (inv) | Not flat = not noise |

### Logic

Three spectral quality measures combine:
1. **Concentration**: Energy focused in specific spectral regions (not spread)
2. **Clarity**: Clear signal, low noise interference
3. **Not flat**: Spectrum has peaks (harmonic structure present)

This output enriches P-layer periodicity assessment and contributes to M-layer temporal integration as a spectral quality indicator.

---

## Layer Summary

| Idx | Name | Range | Reads | Downstream |
|-----|------|-------|-------|------------|
| E0 | pitch_salience_raw | [0, 0.90] | R³[14,17,24,39] | M-layer, P-layer |
| E1 | hg_activation_proxy | [0, 0.85] | R³[5,16,18,39] | P-layer |
| E2 | salience_gradient | [0, 0.80] | R³[4,22,23] | P-layer |
| E3 | spectral_focus | [0, 1] | R³[15,23,24] | M-layer, P-layer |

**Total E-layer R³ reads**: [4,5,14,15,16,17,18,22,23,24,39] = 11 indices
