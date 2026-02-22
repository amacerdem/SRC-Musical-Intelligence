# SNEM E-Layer — Extraction (3D)

**Layer**: Extraction (E)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:beat_entrainment | [0, 1] | SS-EP enhancement at beat frequency. f01 = sigma(0.40*beat_periodicity_1s + 0.35*onset_periodicity_1s + 0.25*amplitude_mean_1s). Nozaradan 2012: SS-EPs enhanced at beat/meter > envelope (p<0.0001). |
| 1 | E1:meter_entrainment | [0, 1] | SS-EP enhancement at meter frequency. f02 = sigma(0.40*coupling_periodicity_1s + 0.30*coupling_periodicity_100ms + 0.30*coupling_zero_crossings_1s). Nozaradan 2012: metric hierarchy creates multiple nested periodicities. |
| 2 | E2:selective_enhancement | [0, 1] | Selective gain for beat frequencies. f03 = sigma(0.35*f01*f02 + 0.35*spectral_change_velocity + 0.30*loudness_entropy). Nozaradan 2012: enhancement goes beyond acoustic envelope. |

---

## Design Rationale

1. **Beat Entrainment (E0)**: Tracks how strongly neural oscillations lock to the beat frequency. Uses H³ periodicity at 1s horizon for spectral_flux and onset_strength. Primary basis: Nozaradan 2012 SS-EP paradigm showing neural enhancement at beat frequency.

2. **Meter Entrainment (E1)**: Tracks metric hierarchy — the grouping of beats into bars. Uses motor-auditory coupling features (x_l0l5) at two timescales: 100ms (beat-level) and 1s (bar-level). Meter is always slower than beat.

3. **Selective Enhancement (E2)**: The interaction of beat and meter creates selective gain: processing resources are amplified for expected beat positions. This is multiplicative (f01*f02), not additive — both beat and meter must be present.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 16, 14, 2) | spectral_flux periodicity H16 L2 | Beat periodicity at 1s — main beat signal |
| (11, 16, 14, 2) | onset_strength periodicity H16 L2 | Onset periodicity at 1s — confirms beat |
| (7, 16, 1, 2) | amplitude mean H16 L2 | Mean amplitude over 1s — beat strength |
| (25, 16, 14, 2) | x_l0l5[0] periodicity H16 L2 | Motor-auditory coupling periodicity 1s |
| (25, 3, 14, 2) | x_l0l5[0] periodicity H3 L2 | Coupling periodicity at 100ms |
| (25, 16, 21, 2) | x_l0l5[0] zero_crossings H16 L2 | Phase resets in coupling at 1s |
| (21, 4, 8, 0) | spectral_change velocity H4 L0 | Tempo velocity at 125ms |
| (8, 3, 20, 2) | loudness entropy H3 L2 | Loudness entropy 100ms |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [7] | amplitude | E0: beat amplitude envelope |
| [10] | spectral_flux | E0: onset detection for beat |
| [11] | onset_strength | E0: event boundary detection |
| [25:33] | x_l0l5 | E1+E2: motor-auditory coupling |

---

## Scientific Foundation

- **Nozaradan 2012**: SS-EPs enhanced at beat/meter > acoustic envelope (p<0.0001, EEG, N=9)
- **Nozaradan 2011**: Neuronal entrainment tagging methodology validated
- **Ding et al. 2025**: Entrainment across 1-12 Hz (ITPC eta2=0.14, EPS eta2=0.32, EEG, N=31)

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/snem/extraction.py`
