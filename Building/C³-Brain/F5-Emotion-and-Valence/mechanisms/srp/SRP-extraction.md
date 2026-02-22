# SRP Extraction — Neurochemical + Circuit (6D)

**Layer**: Extraction (N+C)
**Indices**: [0:6]
**Scope**: internal
**Activation**: sigmoid / clamp [-1, 1] (prediction_error only)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | N0:da_caudate | [0, 1] | Dorsal striatal DA. Ramps quasi-hyperbolically toward expected reward. f00 = sigma(0.50 * energy_velocity_H24 + 0.30 * harmonic_tension_trend + 0.20 * anticipation_gap). Salimpoor 2011: caudate DA correlates with anticipation (r=0.71). Howe 2013: DA ramps scale with proximity x magnitude. |
| 1 | N1:da_nacc | [0, 1] | Ventral striatal DA. Phasic burst at peak moment. f01 = sigma(0.40 * consonance_resolution + 0.30 * stg_nacc_coupling + 0.30 * abs(prediction_error)). Salimpoor 2011: NAcc DA correlates with peak pleasure (r=0.84). Mohebi 2024: VS tau=981s (long horizons). |
| 2 | N2:opioid_proxy | [0, 1] | mu-Opioid receptor activation proxy. f02 = sigma(0.40 * consonance_mean_H18 + 0.30 * resolution_signal + 0.30 * spectral_smoothness_H18). Nummenmaa 2025: [11C]carfentanil PET binding in NAcc shell during pleasurable music. |
| 3 | C0:vta_drive | [0, 1] | VTA-striatum pathway activation. f03 = sigma(0.50 * da_caudate + 0.50 * da_nacc). Menon & Levitin 2005: VTA-NAcc functional connectivity during pleasant music. |
| 4 | C1:stg_nacc_coupling | [0, 1] | Auditory cortex-NAcc functional connectivity. f04 = sigma(0.40 * x_l0l5_mean + 0.30 * consonance_state + 0.30 * onset_rate). Salimpoor 2013: NAcc-STG connectivity predicts reward value (Science). Martinez-Molina 2016: absent in musical anhedonia. |
| 5 | C2:prediction_error | [-1, 1] | Schultz RPE: delta = R(t) + gamma*V(t+1) - V(t). f05 = tanh(0.40 * spectral_flux_velocity + 0.30 * entropy_change + 0.30 * consonance_surprise). +1 = max positive surprise, -1 = max negative surprise. Cheung 2019: pleasure = nonlinear f(uncertainty, surprise), d=3.8-8.53. |

---

## Design Rationale

1. **Caudate DA (N0)**: The anticipatory "wanting" neurochemical signal. Models the quasi-hyperbolic ramp in dorsal striatum that begins 2-30s before expected reward arrival. Uses energy velocity at section-level (H24) to detect building crescendos, harmonic tension trend for tonal buildup, and anticipation gap (future max - current) for proximity scaling. Peaks BEFORE the rewarding event, then drops sharply at consummation.

2. **NAcc DA (N1)**: The consummatory "liking" neurochemical signal. Models the phasic burst in ventral striatum that occurs AT the peak moment. Driven by consonance resolution (dissonance -> consonance transition), auditory-reward coupling strength, and prediction error magnitude. Duration 1-5s. The NAcc-STG connectivity (Salimpoor 2013) is the critical structural link.

3. **Opioid Proxy (N2)**: The hedonic "liking" component mediated by mu-opioid receptors in NAcc shell hotspots. Unlike DA which signals prediction error and incentive salience, opioids directly produce hedonic pleasure. Proxied via consonance (resolved = pleasant), resolution events (tension release), and spectral smoothness (instrument-like = warm). Nummenmaa 2025 provides first PET evidence of opioid release during music.

4. **VTA Drive (C0)**: Source of DA neurons projecting to striatum. Composite of caudate and NAcc DA — when either pathway is active, VTA must be driving. Simple average reflects the VTA as the common upstream source.

5. **STG-NAcc Coupling (C1)**: The critical auditory-reward structural link. Integrity of this pathway predicts individual differences in music reward (Loui 2017: r=0.61). Uses energy-consonance interaction (x_l0l5) as the binding signal, consonance state for tonal quality, and onset rate for event density. Martinez-Molina 2016 showed this is specifically absent in musical anhedonia.

6. **Prediction Error (C2)**: The core Schultz RPE signal. Bipolar: positive = better than expected, negative = worse than expected. Uses spectral flux velocity (fast acoustic change), entropy change (information-theoretic surprise), and consonance surprise (deviation from harmonic expectation). This is the computational variable that drives both wanting ramp updates and learning. Cheung 2019: the uncertainty x surprise interaction in amygdala/hippocampus.

---

## H3 Dependencies (Extraction)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (7, 24, 8, 0) | amplitude velocity H24 L0 | Energy velocity at section level — caudate ramp buildup |
| (0, 24, 18, 0) | roughness trend H24 L0 | Harmonic tension trajectory over 36s — anticipation direction |
| (7, 20, 4, 1) | amplitude max H20 L1 | Future max energy at 5s — anticipation gap numerator |
| (7, 16, 0, 2) | amplitude value H16 L2 | Current energy state — anticipation gap denominator |
| (0, 18, 0, 2) | roughness value H18 L2 | Current dissonance at phrase level — consonance resolution |
| (0, 18, 1, 2) | roughness mean H18 L2 | Baseline dissonance at phrase level — resolution reference |
| (4, 18, 0, 2) | sensory_pleasantness value H18 L2 | Consonance at phrase level — opioid proxy |
| (16, 18, 15, 2) | spectral_smoothness smoothness H18 L2 | Smoothness at phrase — opioid hedonic signal |
| (21, 16, 8, 0) | spectral_flux velocity H16 L0 | Rate of spectral change — prediction error trigger |
| (22, 16, 8, 0) | distribution_entropy velocity H16 L0 | Rate of entropy change — surprise signal |
| (4, 16, 8, 0) | sensory_pleasantness velocity H16 L0 | Consonance surprise — deviation from expectation |
| (25, 18, 0, 2) | x_l0l5[0] value H18 L2 | Energy-consonance interaction — STG-NAcc coupling signal |
| (11, 16, 22, 2) | onset_strength peaks H16 L2 | Onset event density at 1s — coupling event rate |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | N2: inverse valence proxy, consonance resolution |
| [4] | sensory_pleasantness | N2: direct opioid correlate |
| [7] | amplitude | N0: energy dynamics for caudate ramp |
| [11] | onset_strength | C1: event density for coupling |
| [16] | spectral_smoothness | N2: hedonic warmth signal |
| [21] | spectral_flux | C2: frame-to-frame spectral change |
| [22] | distribution_entropy | C2: uncertainty context (Cheung 2019) |
| [25:33] | x_l0l5 | C1: energy-consonance interaction binding |

---

## Scientific Foundation

- **Salimpoor 2011**: Caudate DA r=0.71 (anticipation), NAcc DA r=0.84 (peak pleasure) (PET [11C]raclopride, N=8)
- **Salimpoor 2013**: NAcc-STG connectivity predicts reward value (fMRI + auction, N=19)
- **Cheung 2019**: Pleasure = nonlinear f(uncertainty, surprise), d=3.8-8.53 (ML + fMRI, N=39, 80,000 chords)
- **Ferreri 2019**: Levodopa increases pleasure Z=1.97, chills Z=2.34, WTP Z=2.44 (pharmacology double-blind, N=27)
- **Nummenmaa 2025**: mu-Opioid PET [11C]carfentanil binding in ventral striatum during pleasurable music
- **Menon & Levitin 2005**: VTA-NAcc functional connectivity during pleasant music (fMRI, N=13)
- **Martinez-Molina 2016**: Musical anhedonia = NAcc-STG disconnection, d=3.6-7.0 (fMRI + DTI, N=30)
- **Howe 2013**: DA ramps quasi-hyperbolically toward distant rewards (in vivo rodent)
- **Schultz 2016**: Two-component phasic DA — unselective detection 40-120ms + value-coding RPE
- **Mohebi 2024**: DA transients follow striatal gradient: VS tau=981s, DMS tau=414s (fiber photometry)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/srp/extraction.py`
