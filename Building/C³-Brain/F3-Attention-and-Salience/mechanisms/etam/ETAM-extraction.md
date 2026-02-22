# ETAM E-Layer — Extraction (4D)

**Layer**: Extraction (E)
**Indices**: [0:4]
**Scope**: internal
**Activation**: sigmoid
**Model**: ETAM (STU-B4, Entrainment Tempo & Attention Modulation, 11D, beta-tier 70-90%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:early_window | [0, 1] | sigma(0.35*amp_val*loud_val + 0.35*onset_val + 0.30*amp_peak). Early attention window at 150-220ms latency. Captures the initial cortical response to stimulus onset — amplitude-loudness interaction weighted by onset strength. Hausfeld 2021: first delay window in attentional streaming (d=0.60). |
| 1 | E1:middle_window | [0, 1] | sigma(0.40*flux_val + 0.30*spec_chg_mean + 0.30*energy_vel). Middle attention window at 320-360ms. Spectral flux-dominated feature integration — captures the sustained processing phase where spectral change is evaluated. Hausfeld 2021: second delay window. |
| 2 | E2:late_window | [0, 1] | sigma(0.35*x_coupling_bar + 0.35*x_l5l7_mean + 0.30*stream_entropy). Late attention window at 410-450ms. Cross-domain coupling features at bar-level timescale — captures higher-order integration. Hausfeld 2021: third delay window. |
| 3 | E3:instrument_asymmetry | [0, 1] | sigma(0.50*timbre_var + 0.50*(f02*f03)). Instrument-dependent attention asymmetry. Timbre variability modulates the interaction of middle and late windows — some instruments capture attention more effectively. Doelling & Poeppel 2015: musicians show enhanced entrainment. |

---

## Design Rationale

1. **Early Window (E0)**: The 150-220ms window corresponds to the N1/P2 auditory evoked response. Amplitude-loudness interaction captures the initial perceptual impact, while onset strength signals event boundaries. This is the "what just happened" signal — the earliest attentional capture.

2. **Middle Window (E1)**: The 320-360ms window captures the sustained evaluation phase. Spectral flux dominates (0.40 weight) because timbral change is the primary mid-latency attention driver. Spectral change mean and energy velocity provide context about ongoing spectral dynamics.

3. **Late Window (E2)**: The 410-450ms window captures higher-order integration via cross-domain coupling features. The bar-level x_l0l5 coupling, x_l5l7 mean, and stream entropy reflect the brain's integration of multiple feature streams at the bar timescale. This is the "structural context" window.

4. **Instrument Asymmetry (E3)**: Instruments with high timbre variability (e.g., voice, violin) capture more attention than those with stable timbre (e.g., organ drone). The multiplicative interaction of middle and late windows (f02*f03) reflects the finding that sustained timbral change at structural boundaries is maximally attention-capturing.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (7, 6, 0, 2) | amplitude value H6 L2 | E0: amplitude at 200ms — early window |
| (7, 6, 4, 2) | amplitude max H6 L2 | E0: amplitude peak at 200ms |
| (8, 6, 0, 0) | loudness value H6 L0 | E0: perceptual loudness at 200ms |
| (11, 6, 0, 0) | onset_strength value H6 L0 | E0: onset detection at 200ms |
| (10, 11, 0, 0) | spectral_flux value H11 L0 | E1: spectral flux at 350ms |
| (21, 8, 1, 0) | spectral_change mean H8 L0 | E1: spectral change mean at 250ms |
| (22, 11, 8, 0) | energy_change velocity H11 L0 | E1: energy velocity at 350ms |
| (25, 16, 0, 2) | x_l0l5 value H16 L2 | E2: coupling at bar level 500ms |
| (41, 14, 1, 0) | x_l5l7 mean H14 L0 | E2: higher-order coupling mean |
| (41, 14, 13, 0) | x_l5l7 entropy H14 L0 | E2: stream entropy at 440ms |
| (24, 14, 3, 0) | timbre_change std H14 L0 | E3: timbre variability at 440ms |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [7] | amplitude | E0: onset envelope amplitude |
| [8] | loudness | E0: perceptual loudness weighting |
| [10] | spectral_flux | E1: spectral change detection |
| [11] | onset_strength | E0: event onset boundary |
| [21] | spectral_change | E1: spectral dynamics |
| [22] | energy_change | E1: energy velocity |
| [24] | timbre_change | E3: instrument asymmetry |
| [25:33] | x_l0l5 | E2: motor-auditory coupling |
| [33:41] | x_l4l5 | E2+F: mid-level coupling |
| [41:49] | x_l5l7 | E2: higher-order coupling |

---

## Scientific Foundation

- **Hausfeld et al. 2021**: Three delay windows (d=0.60-0.68) in attentional modulation of auditory streaming, 3T fMRI, N=14
- **Doelling & Poeppel 2015**: Musicians show enhanced neural entrainment to musical rhythms (MEG)
- **Pesnot Lerousseau et al. 2021**: High-gamma persistent activity during attention-modulated auditory processing (iEEG)
- **Aparicio-Terres et al. 2025**: Tempo modulates entrainment strength — faster tempi require stronger attention

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/etam/extraction.py`
