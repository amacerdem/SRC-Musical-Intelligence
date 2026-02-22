# IGFE E-Layer — Extraction (4D)

**Layer**: Extraction (E)
**Indices**: [0:4]
**Scope**: internal
**Activation**: sigmoid
**Model**: PCU-γ1 (Individual Gamma Frequency Enhancement, 9D, γ-tier 50-70%)
**Note**: IGFE has NO M-layer. Architecture: E(4D) + P(3D) + F(2D) = 9D total.

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:igf_match | [0, 1] | Individual Gamma Frequency alignment. f01 = sigma(0.35*gamma_periodicity_25ms + 0.35*gamma_periodicity_50ms). Matches stimulus gamma content to individual IGF (~30-80 Hz). Yokota 2025: IGF-matched stimulation enhances cognition. |
| 1 | E1:memory_enhancement | [0, 1] | Verbal memory improvement signal. f02 = sigma(0.40*f01*cog_coupling_mean_1s). Multiplicative: IGF match must be present for memory benefit. Yokota 2025: word recall improvement with IGF-tuned stimulation. |
| 2 | E2:executive_enhancement | [0, 1] | Executive control improvement (IES proxy). f03 = sigma(0.40*f01*cog_coupling_500ms). Executive function enhancement at shorter timescale than memory. Yokota 2025: IES improvement with gamma stimulation. |
| 3 | E3:dose_response | [0, 1] | Exposure-benefit accumulation. f04 = sigma(0.50*coupling_trend_1s + 0.50*mean_intensity_1s). Enhancement builds over exposure time — not instantaneous. Bolland 2025: systematic review confirms dose-dependence. |

---

## Design Rationale

1. **IGF Match (E0)**: The core gating signal. Individual Gamma Frequency varies across listeners (~30-80 Hz). Enhancement only occurs when the stimulus gamma content aligns with the listener's IGF. Uses periodicity at two fast timescales: 25ms (~40 Hz) and 50ms (~20 Hz) to capture the gamma band. Bidirectional (L2) because IGF is a trait, not directional.

2. **Memory Enhancement (E1)**: Verbal memory improvement is multiplicative with IGF match — no match means no benefit. Uses 1s horizon cognitive coupling (x_l5l7) to capture the sustained engagement needed for memory encoding. Yokota 2025 showed significant word recall improvement when stimulation matched IGF.

3. **Executive Enhancement (E2)**: Executive control (measured by Inverse Efficiency Score) improves at a shorter timescale (500ms) than memory (1s). Same multiplicative gating by IGF match. This captures the faster attentional mechanism underlying executive function benefit.

4. **Dose Response (E3)**: Enhancement is not instantaneous — it accumulates with exposure. Combines coupling trend (increasing engagement over time) with mean intensity. This reflects the systematic review finding (Bolland 2025, k=62) that stimulation duration matters.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (5, 0, 0, 2) | periodicity value H0 L2 | Gamma periodicity at 25ms (~40 Hz) — IGF match |
| (5, 1, 0, 2) | periodicity value H1 L2 | Gamma periodicity at 50ms (~20 Hz) — IGF match |
| (41, 16, 1, 0) | x_l5l7[0] mean H16 L0 | Cognitive coupling mean at 1s — memory signal |
| (41, 8, 0, 0) | x_l5l7[0] value H8 L0 | Cognitive coupling at 500ms — executive signal |
| (41, 16, 18, 0) | x_l5l7[0] trend H16 L0 | Coupling trend at 1s — dose accumulation |
| (7, 16, 1, 2) | amplitude mean H16 L2 | Mean intensity at 1s — dose intensity |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [5] | periodicity | E0: gamma periodicity for IGF match |
| [7] | amplitude | E3: intensity for dose response |
| [10] | spectral_flux | E0: onset/spectral modulation |
| [14] | tonalness | E0: tonal context for gamma |
| [25:33] | x_l0l5 | E0: motor-auditory coupling context |
| [41:49] | x_l5l7 | E1+E2+E3: cognitive coupling features |

---

## Scientific Foundation

- **Yokota et al. 2025**: IGF-matched stimulation improves word recall and IES (N=29, within-subjects)
- **Bolland et al. 2025**: Systematic review (k=62) confirms dose-dependent gamma enhancement effects
- **Dobri et al. 2023**: R²=0.31 for GABA-gamma relationship — individual differences in gamma are neurochemically grounded
- **Leeuwis et al. 2021**: R²adj=0.40 for gamma-cognition relationship — individual gamma predicts cognitive benefit

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/igfe/extraction.py` (pending)
