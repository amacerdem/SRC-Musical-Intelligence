# SDED P-Layer — Cognitive Present (3D)

**Layer**: Present (P)
**Indices**: [4:7]
**Scope**: hybrid
**Activation**: sigmoid (P0, P2) / absolute value (P1)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 4 | P0:roughness_detection | [0, 1] | Current roughness quality at sensory level. sigma(0.30*roughness_h0 + 0.25*(1-inharm)*trist1 + 0.25*tonalness_mean + 0.20*spectral_auto). Spectral clarity modulates roughness quality. |
| 5 | P1:deviation_detection | [0, 1] | Roughness deviation from context. |roughness_h0 - roughness_mean|. MMN substrate — mismatch magnitude. |
| 6 | P2:behavioral_response | [0, 1] | Behavioral response strength. sigma(0.40*M0 + 0.30*P0 + 0.30*helmholtz_mean). Pitch-modulated detection signal. |

---

## Design Rationale

1. **Roughness Detection (P0)**: Combines raw roughness with the Spectral Clarity Index — (1-inharmonicity)*tristimulus1 measures F0 energy in harmonic spectra, tonalness provides pitch clarity, spectral autocorrelation captures cross-band roughness coupling. High clarity = more precise roughness encoding.

2. **Deviation Detection (P1)**: Absolute difference between instant roughness and 100ms contextual mean. This is the raw MMN substrate — larger deviations trigger stronger mismatch responses. Range is [0, 1] since both inputs are normalized.

3. **Behavioral Response (P2)**: Integrates detection function (M0), roughness quality (P0), and consonance context (helmholtz_mean). Represents the observable behavioral response to dissonance — varies with expertise downstream.

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 0, 0, 2) | roughness value H0 L2 | Instant roughness (reused from E) |
| (0, 3, 1, 2) | roughness mean H3 L2 | Context for deviation (reused) |
| (5, 0, 0, 2) | inharmonicity value H0 L2 | Spectral clarity component |
| (14, 3, 1, 0) | tonalness mean H3 L0 | Pitch clarity (reused) |
| (18, 0, 0, 2) | tristimulus1 value H0 L2 | F0 energy for roughness quality |
| (17, 3, 0, 2) | spectral_auto value H3 L2 | Cross-band roughness coupling |
| (2, 3, 1, 2) | helmholtz mean H3 L2 | Consonance context |

---

## Scientific Foundation

- **Fishman 2001**: A1 phase-locked oscillatory activity for roughness (P0)
- **Crespo-Bojorque 2018**: MMN deviation detection universal (P1)
- **Trulla 2018**: Cross-band recurrence patterns link to consonance (P0)

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/sded/cognitive_present.py`
