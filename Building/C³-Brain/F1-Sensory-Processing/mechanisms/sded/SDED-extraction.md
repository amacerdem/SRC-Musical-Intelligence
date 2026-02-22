# SDED E-Layer — Extraction (3D)

**Layer**: Extraction (E)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:early_detection | [0, 1] | Pre-attentive roughness detection. sigma(0.40*roughness_h0*tonalness_mean + 0.30*sethares_h0 + 0.30*(1-helmholtz_h0)). Crespo-Bojorque 2018: universal early MMN 152-258ms. |
| 1 | E1:mmn_dissonance | [0, 1] | MMN amplitude for dissonant deviants. sigma(0.50*E0*stumpf + 0.50*|roughness_h0 - roughness_mean|). Fishman 2001: A1 oscillatory activity correlates with dissonance. |
| 2 | E2:behavioral_accuracy | [0, 1] | Baseline behavioral discrimination = E1 (no expertise modulation). Neural-behavioral dissociation: same neural, different behavioral. |

---

## Design Rationale

Three features model the neural-behavioral dissociation from Crespo-Bojorque 2018:

1. **Early Detection (E0)**: Roughness * pitch clarity (tonalness) captures how clearly the brainstem detects spectral interference. Sethares provides psychoacoustic confirmation. (1 - helmholtz) inverts consonance into dissonance. Universal across expertise.

2. **MMN Dissonance (E1)**: Detection signal gated by tonal fusion (stumpf as pitch salience proxy) plus absolute roughness deviation from 100ms context. The deviation term captures the mismatch negativity — it fires when current roughness differs from the established standard.

3. **Behavioral Accuracy (E2)**: Equals E1 at baseline. The neural-behavioral dissociation means the neural signal is the same for musicians and non-musicians, but behavioral readout differs (expertise-dependent downstream, not modeled here).

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 0, 0, 2) | roughness value H0 L2 | Instant roughness at brainstem timescale |
| (0, 3, 1, 2) | roughness mean H3 L2 | Sustained context for deviance detection |
| (1, 0, 0, 2) | sethares value H0 L2 | Psychoacoustic dissonance confirmation |
| (2, 0, 0, 2) | helmholtz value H0 L2 | Consonance (inverted for dissonance) |
| (14, 3, 1, 0) | tonalness mean H3 L0 | Pitch clarity modulation |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| 3 | stumpf | E1: tonal fusion as pitch salience proxy for MMN gating |

---

## Scientific Foundation

- **Crespo-Bojorque 2018**: Early MMN (152-258ms) UNIVERSAL across expertise (N=32)
- **Fishman 2001**: A1 phase-locked oscillatory activity correlates with dissonance
- **Wagner 2018**: MMN -0.34uV for major 3rd deviant (non-musicians, p=0.003)

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/sded/extraction.py`
