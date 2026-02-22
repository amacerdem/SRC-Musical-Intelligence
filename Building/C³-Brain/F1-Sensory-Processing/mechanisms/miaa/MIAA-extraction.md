# MIAA E-Layer — Extraction (3D)

**Layer**: Extraction (E)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|------------------|
| 0 | E0:imagery_activation | [0, 1] | AC activation during musical imagery. σ(0.40×tonalness_val×trist_balance + 0.30×trist_balance + 0.30×spectral_auto). Kraemer 2005: F(1,14)=48.92, p<.0001 |
| 1 | E1:familiarity_enhancement | [0, 1] | Familiar > unfamiliar BA22 enhancement. σ(0.40×clarity×tonalness_mean + 0.30×warmth_mean + 0.30×spectral_auto). Kraemer 2005: p<.0001 |
| 2 | E2:a1_modulation | [0, 1] | Primary AC involvement for instrumentals. σ(0.40×(1−inharm)×tonalness + 0.30×trist_balance + 0.30×loudness_mean). Kraemer 2005: F(1,14)=22.55, p<.0005 |

---

## Design Rationale

Three explicit features model the three main findings from Kraemer et al. 2005:

1. **Imagery Activation (E0)**: Tonal clarity and harmonic template structure drive AC activation during silence. Tristimulus balance measures how uniformly energy is distributed across fundamental, mid, and high harmonics — balanced = rich template. Spectral autocorrelation captures cross-band binding.

2. **Familiarity Enhancement (E1)**: Familiar music activates BA22 more strongly. Clarity (inverse spectral flatness) × sustained tonalness indicates a clear, well-defined spectral template. Warmth adds timbre richness. Spectral autocorrelation serves as plasticity proxy — self-similar spectra are easier to memorize.

3. **A1 Modulation (E2)**: Primary AC only recruited when semantic route unavailable (instrumental, not lyrics). Low inharmonicity × high tonalness = acoustic rather than semantic content. Tristimulus balance provides spectral detail. Loudness context modulates overall activation.

---

## H³ Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (14, 2, 0, 2) | tonalness value H2 L2 | Tonal clarity at gamma-rate |
| (18, 2, 0, 2) | tristimulus1 value H2 L2 | Harmonic template — fundamental |
| (19, 2, 0, 2) | tristimulus2 value H2 L2 | Harmonic template — mid |
| (20, 2, 0, 2) | tristimulus3 value H2 L2 | Harmonic template — high |
| (14, 5, 1, 0) | tonalness mean H5 L0 | Sustained tonal clarity |
| (12, 5, 1, 0) | warmth mean H5 L0 | Timbre quality |
| (10, 8, 1, 0) | loudness mean H8 L0 | Intensity context |

---

## R³ Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| 5 | inharmonicity | E2: (1−inharm) × tonalness |
| 14 | tonalness | E2: instantaneous tonal clarity |
| 15 | clarity | E1: template clarity (was spectral_flatness inverted) |
| 17 | spectral_autocorrelation | E0, E1: cross-band binding / plasticity |

---

## Scientific Foundation

- **Kraemer 2005**: AC active during musical imagery silence gaps (fMRI, n=15)
- **Halpern 2004**: Perception-imagery overlap in posterior PT (r=0.84)
- **Di Liberto 2021**: Imagery pitch encoding comparable to perception (p=0.19 n.s.)

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/miaa/extraction.py`
