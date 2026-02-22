# OII E-Layer — Extraction (3D)

**Layer**: Extraction (E)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:f16_slow_integration | [0, 1] | Theta/alpha integration strength. Frontal theta to temporal alpha coherence. f16 = sigma(0.30 * syntax.mean + 0.20 * fusion_h10). |w| sum = 0.50. Bruzzone et al. 2022: high Gf individuals show stronger theta/alpha degree (p<0.001, MEG N=66). |
| 1 | E1:f17_fast_segregation | [0, 1] | Gamma-band local processing efficiency. Temporal cortex gamma segregation. f17 = sigma(0.25 * roughness + 0.25 * onset_h10). |w| sum = 0.50. Sturm et al. 2014: ECoG high gamma (70-170 Hz) reveals distinct cortical representations for lyrics, harmonic, and timbre features (N=10). |
| 2 | E2:f18_mode_switching | [0, 1] | Integration-segregation switch efficiency. DLPFC-mediated mode coordination. f18 = sigma(0.20 * predict_err.mean + 0.15 * flux_h10 + 0.15 * encoding.mean). |w| sum = 0.50. Samiee et al. 2022: delta-beta PAC in rIFG F(1)=43.95 p<0.0001 — cross-frequency coupling as mode switching mechanism (MEG N=16). |

---

## Design Rationale

1. **Slow Integration (E0)**: Tracks theta/alpha long-range binding strength. Theta oscillations from frontal cortex bind distributed features across temporal and parietal regions into unified percepts. Uses harmonic syntax from synthesis (reflecting how well distributed harmonic features are bound) and stumpf fusion at chord-level timescale (H10, 400ms). High integration = the brain successfully assembles a coherent harmonic picture from distributed spectral input.

2. **Fast Segregation (E1)**: Tracks gamma-band local processing efficiency. Gamma oscillations in auditory cortex support fine-grained spectral and temporal feature extraction. Uses roughness (which drives gamma demand — unresolved harmonics require local processing) and onset strength at H10 (transient events trigger gamma bursts). High segregation = the brain efficiently processes local spectral detail.

3. **Mode Switching (E2)**: Tracks the efficiency of transitions between integration and segregation modes. DLPFC coordinates when to switch from binding (theta) to detail extraction (gamma) and back. Uses prediction error (which drives the need to switch — violated predictions require mode change), spectral flux at H10 (acoustic transitions that trigger switching), and encoding quality. High mode switching = flexible, adaptive oscillatory control.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 10, 1, 2) | stumpf_fusion mean H10 L2 | Harmonic binding state at chord level (400ms) |
| (11, 10, 0, 2) | onset_strength value H10 L2 | Current gamma burst trigger at chord level |
| (21, 10, 0, 2) | spectral_flux value H10 L2 | Current transition signal at chord level |
| (5, 10, 0, 2) | periodicity value H10 L2 | Current oscillatory regularity |
| (22, 10, 0, 2) | entropy value H10 L2 | Current integration demand |
| (15, 10, 0, 2) | spectral_centroid value H10 L2 | Frequency balance at chord level |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | E1: gamma-band complexity proxy (unresolved harmonics) |
| [3] | stumpf_fusion | E0: tonal fusion = theta-mediated binding success |
| [5] | periodicity | E0: oscillatory regularity proxy |
| [11] | onset_strength | E1+E2: mode switch trigger (gamma burst) |
| [21] | spectral_flux | E2: integration-segregation transition signal |
| [22] | entropy | E2: integration demand (low=integration, high=segregation) |

---

## Scientific Foundation

- **Bruzzone et al. 2022**: DTI + MEG N=66/67, high Gf = stronger theta/alpha degree (p<0.001), lower theta/alpha segregation; reversed pattern in gamma (p<0.001)
- **Samiee et al. 2022**: MEG N=16, delta-beta PAC in rAud (F(1)=11.1, p<0.001) and rIFG (F(1)=43.95, p<0.0001); cross-frequency coupling for pitch processing
- **Sturm et al. 2014**: ECoG N=10, high gamma (70-170 Hz) reveals distinct cortical representations for musical features
- **Fries 2015**: Review, CTC framework — gamma=local computation, theta=long-range coordination, alpha=gating

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/oii/extraction.py`
