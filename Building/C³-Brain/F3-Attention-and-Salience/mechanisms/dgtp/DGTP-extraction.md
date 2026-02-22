# DGTP E-Layer — Extraction (3D)

**Layer**: Extraction (E)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid
**Model**: ASU-gamma2, Domain-General Temporal Processing (9D, gamma-tier 50-70%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:music_timing | [0, 1] | Music timing ability. f22 = sigma(0.40*beat_periodicity_1s + 0.30*coupling_period_100ms). Beat perception tracked via spectral_flux periodicity at 1s horizon and motor-auditory coupling at 100ms. Rathcke 2024: domain-general timing mechanisms shared across music and speech. |
| 1 | E1:speech_timing | [0, 1] | Prosody perception. f23 = sigma(0.35*onset_velocity_600ms + 0.30*coupling_stability_1s). Onset velocity captures syllable-rate temporal events; coupling stability reflects sustained entrainment to prosodic rhythm. Hoddinott & Grahn 2024: 7T RSA reveals shared temporal representations. |
| 2 | E2:shared_mechanism | [0, 1] | Cross-domain timing factor. f24 = sqrt(f22*f23). Geometric mean ensures both domains must contribute — captures the shared variance rather than domain-specific timing. Grahn & Brett 2007: SMA/putamen engagement is domain-general. |

---

## Design Rationale

1. **Music Timing (E0)**: Tracks beat perception ability using spectral flux periodicity at the 1s bar-level horizon combined with fast motor-auditory coupling (100ms). The 0.40/0.30 weighting prioritizes the acoustic beat signal over the coupling measurement. Primary basis: rhythm perception engages domain-general circuitry in SMA and putamen.

2. **Speech Timing (E1)**: Tracks prosodic timing perception via onset velocity at 600ms (syllable/phrase rate) and coupling stability at 1s (sustained entrainment). Speech timing operates at slightly different timescales than music but recruits overlapping circuits. Hoddinott & Grahn 2024 RSA data at 7T confirms shared representations.

3. **Shared Mechanism (E2)**: The geometric mean sqrt(f22*f23) is the key computation — it only gives high values when BOTH music and speech timing are strong. This captures the domain-general component that transfers across modalities. Zero in either domain collapses the shared signal.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 16, 17, 2) | spectral_flux periodicity H16 L2 | Beat periodicity at 1s — music timing signal |
| (25, 3, 17, 2) | x_l0l5[0] periodicity H3 L2 | Coupling periodicity at 100ms — fast motor-auditory |
| (11, 13, 8, 0) | onset_strength velocity H13 L0 | Onset velocity at 600ms — syllable-rate events |
| (25, 16, 19, 0) | x_l0l5[0] stability H16 L0 | Coupling stability at 1s — sustained entrainment |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [10] | spectral_flux | E0: onset detection for beat periodicity |
| [11] | onset_strength | E1: event boundary detection for prosody |
| [25:33] | x_l0l5 | E0+E1: motor-auditory coupling signal |

---

## Scientific Foundation

- **Rathcke 2024**: Domain-general timing mechanisms shared across music and speech perception
- **Grahn & Brett 2007**: Beat perception recruits SMA + putamen (fMRI, N=27) — domain-general motor timing
- **Hoddinott & Grahn 2024**: 7T RSA reveals shared temporal representations for music and speech
- **Large 2023**: Review of neural resonance theory — oscillatory timing is domain-general

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/dgtp/extraction.py` (pending)
