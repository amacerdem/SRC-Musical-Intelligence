# SDNPS P-Layer — Cognitive Present (3D)

**Layer**: Present (P)
**Indices**: [4:7]
**Scope**: hybrid
**Activation**: sigmoid (P0) / product (P1) / arithmetic (P2)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 4 | P0:ffr_encoding | [0, 1] | Brainstem FFR phase-locking strength. sigma(0.50*tonalness_h0 + 0.50*autocorr_period). Bidelman & Krishnan 2009: FFR magnitude correlates with pitch salience. |
| 5 | P1:harmonicity_proxy | [0, 1] | Harmonic template match weighted by spectral balance. (1-inharm)*trist_balance. High when spectrum is harmonic AND balanced. |
| 6 | P2:roughness_interference | [0, 1] | Stimulus-invariant roughness signal. 1-(roughness+sethares)/2. High when low roughness = low interference. Cousineau 2015: NPS ↔ roughness r=-0.57 across ALL timbres. |

---

## Design Rationale

Three present-processing dimensions for brainstem pitch salience:

1. **FFR Encoding (P0)**: Tonalness (instant pitch clarity) and harmonic periodicity (100ms context) jointly predict brainstem phase-locking magnitude. FFR is the physiological substrate of NPS.

2. **Harmonicity Proxy (P1)**: Product of (1-inharmonicity) and tristimulus balance. When the spectrum closely approximates a harmonic series (low inharmonicity) with balanced energy distribution (equal tristimulus values), the harmonicity proxy is high. No sigmoid — product naturally bounded.

3. **Roughness Interference (P2)**: The stimulus-invariant signal. Average of roughness and Sethares dissonance, inverted. High values = low interference = cleaner NPS. This dimension holds across all timbres (unlike E0/E1 which degrade with complexity).

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (14, 0, 0, 2) | tonalness value H0 L2 | Instant pitch clarity for FFR |
| (17, 3, 14, 2) | spectral_auto periodicity H3 L2 | Harmonic periodicity over 100ms |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| 0 | roughness | P2: roughness interference signal |
| 1 | sethares | P2: psychoacoustic dissonance |
| 5 | inharmonicity | P1: spectral deviation from harmonic series |

Note: `trist_balance` is pre-computed in `__init__.py` from tristimulus1/2/3 using `correction=0` to avoid NaN for T=1.

---

## Scientific Foundation

- **Bidelman & Krishnan 2009**: FFR magnitude follows Pythagorean hierarchy
- **Cousineau 2015**: NPS ↔ roughness r=-0.57 (stimulus-invariant)
- **Penagos 2004**: Pitch salience encoded in anterolateral HG

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/sdnps/cognitive_present.py`
