# PNH P-Layer — Cognitive Present (3D)

**Layer**: Present (P)
**Indices**: [5:8]
**Scope**: hybrid
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:ratio_enc | [0, 1] | Current ratio encoding state. sigma(0.40*tonalness_h10 + 0.30*autocorr_period + 0.30*velocity_d_h10). Tonalness (purity) * harmonic regularity * loudness attention. |
| 6 | P1:conflict_mon | [0, 1] | Current conflict monitoring activation (IFG/ACC). sigma(0.60*M1 + 0.40*H1). Neural activation weighted by raw conflict response. Kim 2021: IFG connectivity for irregularity. |
| 7 | P2:consonance_pref | [0, 1] | Consonance-preference binding. sigma(0.50*pleasant_h10*(1-roughness) + 0.30*H2 + 0.20*M0). Aesthetic appreciation modulated by expertise. Sarasso 2019: eta2p=0.685 for aesthetic judgment. |

---

## Design Rationale

Three present-processing dimensions for ratio hierarchy:

1. **Ratio Encoding State (P0)**: Three H3 features at chord level (H10): tonalness provides ratio purity (harmonic-to-noise ratio), spectral autocorrelation periodicity captures harmonic regularity, and velocity_D provides loudness-based attention weighting. Together they represent the current state of harmonic ratio encoding.

2. **Conflict Monitoring (P1)**: Neural activation (M1, product of ratio and conflict) weighted 0.60 plus raw conflict response (H1) at 0.40. This reflects the ongoing IFG/ACC activation for ratio complexity processing — higher for dissonant intervals.

3. **Consonance Preference (P2)**: Pleasantness at chord level gated by (1-roughness) for sensory consonance, plus expertise modulation (H2) and ratio complexity (M0). This models the consonance-to-aesthetic-appreciation pathway documented by Sarasso 2019.

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 10, 0, 2) | pleasantness value H10 L2 | Current consonance perception |
| (14, 10, 0, 2) | tonalness value H10 L2 | Ratio purity |
| (17, 10, 14, 2) | spectral_auto period H10 L2 | Harmonic regularity at chord level |
| (8, 10, 0, 2) | velocity_D value H10 L2 | Loudness attention weight |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| 0 | roughness | Consonance-preference gating (1-roughness) |

---

## Scientific Foundation

- **Sarasso 2019**: Consonance -> aesthetic appreciation -> motor inhibition; eta2p=0.685 (AJ), 0.225 (N1)
- **Kim 2021**: R-IFG->L-IFG connectivity for syntactic irregularity
- **Bidelman & Krishnan 2009**: FFR magnitude correlates with pitch salience across intervals

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/pnh/cognitive_present.py`
