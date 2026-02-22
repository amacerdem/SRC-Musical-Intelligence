# RASN E-Layer — Extraction (3D)

**Layer**: Extraction (E)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:f10_entrainment | [0, 1] | Rhythmic entrainment strength. SMA + auditory cortex phase-locking. f10 = sigma(0.35 * x_l0l5.mean * beat.mean + 0.35 * flux * onset * meter.mean + 0.30 * periodicity * encoding.mean). Nozaradan 2012 / Grahn & Brett 2007: SMA + putamen respond preferentially to beat-inducing rhythms (Z=5.67). |
| 1 | E1:f11_motor_facilitation | [0, 1] | Motor facilitation level. Premotor cortex + cerebellum activation. f11 = sigma(0.40 * x_l4l5.mean * motor.mean + 0.30 * amplitude * loudness + 0.30 * encoding.mean * stumpf). Harrison et al. 2025: both external and internal cues activate sensorimotor cortex (FWE-corrected, N=55). |
| 2 | E2:f12_neuroplasticity | [0, 1] | Neuroplasticity index. Hippocampus + corticospinal connectivity. f12 = sigma(0.35 * entropy_optimal * retrieval.mean + 0.35 * ... + 0.30 * stumpf * pleasantness). Blasi et al. 2025: structural neuroplasticity from rhythm interventions (20 RCTs, N=718). |

---

## Design Rationale

1. **Rhythmic Entrainment (E0)**: Tracks how strongly neural oscillations lock to beat frequency. Uses motor-auditory coupling (x_l0l5) combined with beat induction signals and spectral flux/onset. Rhythmic entrainment is the primary driver of RAS-based neuroplasticity. SMA phase-locking to regular beats provides the temporal scaffold for memory binding.

2. **Motor Facilitation (E1)**: Captures the degree of motor pathway activation from auditory stimulation. Uses sensorimotor integration features (x_l4l5) combined with energy envelope (amplitude, loudness) and encoding/binding quality (stumpf fusion). Motor facilitation reflects premotor cortex and cerebellar engagement for beat-driven movement.

3. **Neuroplasticity (E2)**: Measures the neuroplastic potential of current rhythmic stimulation. Uses an inverted-U complexity function (entropy_optimal = 1.0 - |entropy - 0.5| * 2.0) reflecting that moderate complexity produces optimal plasticity demand. Combined with binding stability (stumpf fusion) and engagement (pleasantness).

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 6, 0, 2) | spectral_flux value H6 L2 | Current beat onset at 200ms |
| (10, 11, 4, 0) | spectral_flux max H11 L0 | Peak onset over 500ms |
| (11, 6, 0, 2) | onset_strength value H6 L2 | Current onset sharpness at 200ms |
| (11, 11, 14, 0) | onset_strength periodicity H11 L0 | Beat regularity at 500ms |
| (7, 6, 0, 2) | amplitude value H6 L2 | Current beat energy at 200ms |
| (7, 11, 8, 0) | amplitude velocity H11 L0 | Energy dynamics over 500ms |
| (7, 16, 1, 0) | amplitude mean H16 L0 | Average energy over 1s |
| (8, 6, 0, 2) | loudness value H6 L2 | Current accent strength at 200ms |
| (8, 11, 17, 0) | loudness peaks H11 L0 | Beat count per 500ms |
| (8, 16, 1, 0) | loudness mean H16 L0 | Average loudness over 1s |
| (5, 6, 0, 2) | periodicity_strength value H6 L2 | Current rhythmic regularity |
| (5, 11, 14, 0) | periodicity_strength periodicity H11 L0 | Entrainment stability at 500ms |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [7] | amplitude | E1: beat intensity, motor activation trigger |
| [8] | loudness | E1: accent strength |
| [10] | spectral_flux | E0: onset salience, beat detection backbone |
| [11] | onset_strength | E0: beat precision |
| [5] | periodicity_strength | E0: rhythmic regularity |
| [25:33] | x_l0l5 | E0: motor-auditory coupling (Energy x Consonance) |
| [33:41] | x_l4l5 | E1: sensorimotor integration (Derivatives x Consonance) |
| [3] | stumpf_fusion | E1+E2: rhythmic coherence binding |
| [4] | sensory_pleasantness | E2: engagement proxy |
| [23] | entropy | E2: pattern complexity (inverted-U optimal) |

---

## Scientific Foundation

- **Grahn & Brett 2007**: fMRI N=27, SMA + putamen respond preferentially to beat-inducing rhythms (Z=5.67, FDR p<.05)
- **Harrison et al. 2025**: fMRI N=55, PD + HC cued movement, SMA/putamen/cerebellum activated (FWE-corrected clusters)
- **Blasi et al. 2025**: Systematic review 20 RCTs N=718, structural neuroplasticity from rhythm interventions
- **Noboa et al. 2025**: EEG N=30, SS-EPs at beat frequency 1.25 Hz
- **Thaut et al. 2015**: Review, auditory-motor entrainment theory (foundational)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/rasn/extraction.py`
