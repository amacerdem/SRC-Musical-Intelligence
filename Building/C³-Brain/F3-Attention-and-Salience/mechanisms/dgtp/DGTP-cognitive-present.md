# DGTP P-Layer — Cognitive Present (2D)

**Layer**: Present Processing (P)
**Indices**: [5:7]
**Scope**: exported (kernel relay)
**Activation**: sigmoid
**Model**: ASU-gamma2, Domain-General Temporal Processing (9D, gamma-tier 50-70%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:music_beat_perception | [0, 1] | Beat-onset periodicity perception. sigma(0.5*beat_period_1s). Tracks present-moment beat periodicity strength from spectral_flux at the 1s horizon. Grahn & Brett 2007: putamen activation reflects online beat perception. |
| 6 | P1:domain_general_timing | [0, 1] | Domain-general timing engagement. sigma(0.5*coupling_stability_1s). Current strength of the shared timing mechanism estimated from motor-auditory coupling stability. Large 2023: oscillatory timing as a domain-general resource. |

---

## Design Rationale

1. **Music Beat Perception (P0)**: The present-moment beat perception signal — "how strongly is the beat detected right now?" Uses beat periodicity at 1s to provide a real-time readout of rhythmic entrainment. This is the music-specific component of the domain-general system.

2. **Domain-General Timing (P1)**: The shared timing engagement signal — "how active is the domain-general timing mechanism?" Uses coupling stability as a proxy for the engagement of SMA/putamen/cerebellum circuits that serve both music and speech. This is the relay-exported signal for downstream consumers.

---

## Kernel Relay Export

P-layer outputs are the primary relay exports:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `music_beat_perception` | P0 [5] | Beat perception for attention allocation |
| `domain_general_timing` | P1 [6] | Timing engagement for cross-domain processing |

---

## H3 Dependencies (P-Layer)

P-layer primarily combines E+M outputs. The beat_period_1s and coupling_stability_1s signals are already loaded by the E-layer and M-layer tuples:

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 16, 17, 2) | spectral_flux periodicity H16 L2 | Beat periodicity at 1s (shared with E-layer) |
| (25, 16, 19, 0) | x_l0l5[0] stability H16 L0 | Coupling stability at 1s (shared with M-layer) |

---

## Scientific Foundation

- **Grahn & Brett 2007**: Beat perception recruits SMA + putamen (fMRI, N=27) — real-time beat tracking
- **Large 2023**: Neural resonance theory — oscillatory timing as a domain-general resource
- **Hoddinott & Grahn 2024**: 7T RSA shows shared timing representations active during perception

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/dgtp/cognitive_present.py` (pending)
