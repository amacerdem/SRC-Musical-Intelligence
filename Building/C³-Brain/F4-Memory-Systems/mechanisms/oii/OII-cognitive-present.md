# OII P-Layer — Cognitive Present (3D)

**Layer**: Present Processing (P)
**Indices**: [5:8]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:integration_state | [0, 1] | Current theta/alpha integration level. sigma(0.30 * syntax.mean + 0.20 * tonalness_h16). |w| sum = 0.50. Harmonic syntax aggregation reflecting the real-time binding of distributed spectral features via theta coherence. Biau et al. 2025: neocortical and hippocampal theta oscillations track audiovisual integration (MEG N=23). |
| 6 | P1:segregation_state | [0, 1] | Current gamma segregation level. sigma(0.25 * roughness + 0.25 * entropy). |w| sum = 0.50. High roughness + high entropy = strong local processing demand = segregation mode active. Dobri et al. 2023: 40-Hz gamma ASSR correlates with hearing abilities and GABA levels (MEG). |
| 7 | P2:encoding_quality | [0, 1] | Pattern encoding success (integration result). sigma(0.25 * pleasantness_h16 + 0.25 * ...). |w| sum = 0.50. Integration output: how well the current input has been bound into a coherent representation for memory encoding. Borderie et al. 2024: theta-gamma PAC in hippocampus supports auditory STM; PAC strength predicts correct recall (iEEG). |

---

## Design Rationale

1. **Integration State (P0)**: Captures the current level of theta/alpha-mediated binding. Uses harmonic syntax from synthesis (reflecting distributed harmonic coherence) and tonalness at H16 (1s working memory window). When integration_state is high, the brain is in binding mode — distributed features across frontal-temporal networks are being unified into a coherent percept. This maps to the observation that high-Gf individuals show stronger theta/alpha degree connectivity.

2. **Segregation State (P1)**: Captures the current level of gamma-band local processing. Uses roughness (unresolved harmonics that demand fine-grained spectral analysis) and entropy (high entropy = complex local structure requiring segregated processing). When segregation_state is high, auditory cortex gamma oscillations are driving detailed feature extraction. Excessive gamma synchrony can be detrimental (Dobri 2023), so this is not a simple "more is better" metric.

3. **Encoding Quality (P2)**: Captures how successfully the current input has been integrated and bound for memory encoding. This is the output of the integration process — after theta has bound distributed features and gamma has extracted local details, encoding quality measures the result. Uses pleasantness at H16 (encoding is facilitated by pleasant stimuli) and integration-memory binding. Maps to hippocampal theta-gamma coupling, where gamma bursts nested within theta carry individual items for sequential encoding.

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (14, 16, 0, 2) | tonalness value H16 L2 | Current harmonic integration at 1s |
| (14, 20, 1, 0) | tonalness mean H20 L0 | Tonal stability over 5s consolidation |
| (4, 16, 0, 2) | sensory_pleasantness value H16 L2 | Current encoding reward at 1s |
| (4, 20, 18, 0) | sensory_pleasantness trend H20 L0 | Pleasantness trajectory over 5s |
| (0, 16, 0, 2) | roughness value H16 L2 | Current gamma-band demand at 1s |
| (10, 16, 0, 2) | loudness value H16 L2 | Current oscillatory drive at 1s |
| (10, 20, 1, 0) | loudness mean H20 L0 | Average drive over 5s consolidation |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | P1: gamma-band demand proxy |
| [4] | sensory_pleasantness | P2: encoding reward signal |
| [14] | tonalness | P0: harmonic integration measure |
| [10] | loudness | P0+P2: oscillatory drive / arousal |
| [22] | entropy | P1: integration demand (high=segregation) |

---

## Scientific Foundation

- **Biau et al. 2025**: MEG N=23, neocortical and hippocampal theta oscillations track audiovisual integration and replay of speech memories; theta phase determines LTP/LTD
- **Dobri et al. 2023**: MEG, 40-Hz gamma ASSR increases in older age; correlates with hearing loss and left auditory cortex GABA; excessive gamma = detrimental
- **Borderie et al. 2024**: iEEG, theta-gamma PAC in STS, IFG, ITG, hippocampus supports auditory STM; PAC strength decodes correct vs incorrect trials
- **Yuan et al. 2025**: EEG, auditory WM load decoded from alpha-band oscillation patterns; dynamic coding during maintenance

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/oii/cognitive_present.py`
