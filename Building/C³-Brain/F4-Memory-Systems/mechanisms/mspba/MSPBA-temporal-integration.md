# MSPBA M-Layer — Temporal Integration (2D)

**Layer**: Mathematical Model (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:eran_amplitude | [0, 1] | Predicted mERAN amplitude. sigma(pred_error.mean * entropy * roughness.mean * (1-stumpf_fusion)). Models the 2:1 position ratio via context depth -- position 5 violation produces 2x the mERAN of position 3. Maess et al. 2001: mERAN amplitude at position 5 = 2x position 3 (N=28). |
| 4 | M1:syntax_violation | [0, 1] | Syntactic violation score. sigma(0.25 * roughness + 0.25 * entropy + 0.25 * inharmonicity + 0.25 * (1-stumpf_fusion)). Multi-feature violation detection combining four consonance/complexity markers. Koelsch et al. 2000: ERAN for Neapolitan chord violations. |

---

## Design Rationale

1. **ERAN Amplitude (M0)**: The core computational output -- predicts the magnitude of the mERAN response based on prediction error, harmonic complexity (entropy), dissonance (roughness), and tonal fusion deficit (1-stumpf). This multiplicative chain models the empirical finding that mERAN amplitude scales with context depth: more accumulated harmonic context means stronger expectation, producing a larger violation signal. The 2:1 position ratio (Maess 2001) emerges from context accumulation.

2. **Syntax Violation Score (M1)**: A normalized composite score from four independent markers of harmonic violation. Equal weighting (0.25 each) across roughness, entropy, inharmonicity, and fusion deficit provides a robust multi-feature detection. The Neapolitan chord (bII) simultaneously elevates all four markers: high roughness (unexpected partials), high entropy (unpredictable content), high inharmonicity (spectral deviation), and low fusion (out of key).

---

## Mathematical Formulation

```
mERAN(chord_position, violation) = pred_error x Context(position) x Dissonance

Context accumulation:
  Position 1: Context = base     --> mERAN = small
  Position 3: Context = moderate --> mERAN = 50% of max
  Position 5: Context = deep     --> mERAN = 100% of max
  Ratio: Position 5 / Position 3 = 2.0x (Maess et al. 2001)

eran_amplitude = sigma(pred_error * entropy * roughness * (1 - stumpf_fusion))

syntax_violation = sigma(0.25 * roughness + 0.25 * entropy
                       + 0.25 * inharmonicity + 0.25 * (1 - stumpf_fusion))
  coefficients: |0.25| + |0.25| + |0.25| + |0.25| = 1.00 <= 1.0

Neapolitan detection proxy:
  Normal tonic:     low roughness, low entropy, low inharmonicity, high fusion
  Neapolitan (bII): high roughness, high entropy, high inharmonicity, low fusion
```

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 14, 1, 0) | roughness mean H14 L0 | Average dissonance over chord progression |
| (5, 14, 1, 0) | inharmonicity mean H14 L0 | Average harmonic deviation over progression |
| (22, 14, 1, 0) | entropy mean H14 L0 | Average complexity over progression |
| (23, 14, 1, 0) | spectral_flux mean H14 L0 | Average spectral change rate |

M-layer combines E-layer outputs with progression-level (H14, 700ms) aggregated features.

---

## Scientific Foundation

- **Maess et al. 2001**: mERAN at position 5 = 2x amplitude vs position 3, context effect (MEG, N=28)
- **Koelsch et al. 2000/2001**: ERAN for Neapolitan chord violations, 150-180ms, right-anterior (EEG)
- **Wohrle et al. 2024**: N1m evolves over chord progression, parallels mERAN position effect (MEG, N=30, eta-p2=0.101)
- **Egermann et al. 2013**: Information-theoretic expectation violation predicts psychophysiological response (N=50)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/mspba/temporal_integration.py`
