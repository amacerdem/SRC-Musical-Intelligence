# CMAT S+T-Layer — Temporal Integration (5D)

**Layer**: Supramodal State (S) + Transfer Dynamics (T)
**Indices**: [1:6]
**Scope**: internal
**Activation**: tanh | sigmoid | constant

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 1 | S0:supramodal_valence | [-1, 1] | Modality-independent affect valence. V_supra = tanh(0.4 * aud_valence + 0.3 * (pleasantness - 0.5) + 0.3 * affect_mean). Weighted fusion of auditory valence, hedonic quality, and affective dynamics. In multi-modal mode, includes visual valence contribution. Spence 2011: supramodal affect representations in mPFC/OFC. |
| 2 | S1:supramodal_arousal | [0, 1] | Modality-independent activation level. A_supra = sigma(0.4 * aud_arousal + 0.3 * affect_velocity + 0.3 * spectral_flux). Combines loudness-based arousal with rate of affective change and spectral dynamics. Petrini 2010: audio-visual drumming integration shows supramodal arousal. |
| 3 | S2:cross_modal_bind | [0, 1] | Binding strength between modalities. Defaults to 0.5 in audio-only mode. With external visual: Binding(A,V) = exp(-abs(t_aud - t_vis) / tau_bind) * Congruence(A,V), where tau_bind ~ 200ms. Molholm 2002: early multisensory interactions at 46ms latency. |
| 4 | T0:binding_temporal | [0, 1] | Temporal precision of cross-modal binding. binding_temporal = sigma(0.5 * (1.0 - affect_entropy) + 0.5 * integration_state). STS integration quality — high when events are temporally coherent (within +/-100ms). Low entropy = predictable binding = high precision. Molholm 2002: STS temporal binding window. |
| 5 | T1:congruence_streng | [0, 1] | Affective congruence between modalities. Defaults to 1.0 in audio-only (perfect self-congruence). With external: Congruence = (1 + cos(theta_AV)) / 2, where theta_AV = angle between auditory and visual affect vectors. Spence 2011: congruent cross-modal stimuli enhance affect. |

---

## Design Rationale

1. **Supramodal Valence (S0)**: The modality-independent valence signal. Uses tanh for bidirectional range [-1, 1]. In audio-only mode, this integrates the auditory valence (pleasantness - roughness) with the H3 affective dynamics to produce a stable valence estimate. The 0.4/0.3/0.3 weighting prioritizes the direct auditory signal while incorporating temporal context.

2. **Supramodal Arousal (S1)**: The modality-independent activation signal. Combines three arousal-related signals: direct loudness, rate of affective change (velocity), and spectral flux (moment-to-moment acoustic change). These three sources provide complementary activation information.

3. **Cross-Modal Binding (S2)**: The binding strength between modalities. In audio-only mode, this defaults to 0.5 (moderate baseline). In multi-modal contexts, it uses the temporal synchrony model with an exponential decay based on inter-modal timing difference and a 200ms binding window.

4. **Binding Temporal Precision (T0)**: How temporally coherent the cross-modal integration is. Low affective entropy (predictable patterns) and high integration state produce high temporal precision. This captures the STS's role in temporal binding between modalities.

5. **Congruence Strength (T1)**: The affective agreement between modalities. In audio-only mode, this is 1.0 (perfect self-congruence). With external modalities, it uses the cosine similarity of the affect vectors to measure how well the modalities agree in their emotional content.

---

## H3 Dependencies (S+T-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 6, 0, 2) | sensory_pleasantness value H6 L2 | Fast affect state for supramodal valence |
| (4, 16, 0, 2) | sensory_pleasantness value H16 L2 | Slow affect state for integration |
| (4, 6, 8, 0) | sensory_pleasantness velocity H6 L0 | Affect velocity for supramodal arousal |
| (22, 16, 20, 2) | entropy entropy H16 L2 | Predictability for binding temporal precision |
| (4, 11, 1, 0) | sensory_pleasantness mean H11 L0 | Cognitive-projection integration state |
| (4, 11, 2, 0) | sensory_pleasantness std H11 L0 | Integration variability |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | S0: inverse consonance for auditory valence |
| [4] | sensory_pleasantness | S0: direct hedonic for valence computation |
| [10] | loudness | S1: energy level for supramodal arousal |
| [15] | brightness | S0/T0: supramodal brightness correspondence |
| [16] | warmth | S0/T0: supramodal warmth correspondence |
| [21] | spectral_flux | S1: frame-to-frame change for arousal dynamics |
| [25:33] | x_l0l5 | S0: energy-consonance supramodal binding substrate |

---

## Scientific Foundation

- **Spence 2011**: Systematic cross-modal correspondences across modalities; supramodal affect representations (tutorial review, Attention, Perception, & Psychophysics, 73(4), 971-995)
- **Molholm et al. 2002**: Early multisensory auditory-visual interactions at 46ms; STS temporal binding window (ERP, N=10, Cognitive Brain Research, 14(1), 115-128)
- **Petrini et al. 2010**: Audio-visual drumming integration demonstrates supramodal arousal processing (behavioral, N=18, Experimental Brain Research, 206(2), 169-182)
- **Taruffi et al. 2021**: Trait empathy modulates vmPFC/mOFC centrality for sad music — empathy-mediated cross-modal affective transfer (fMRI, N=24)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/cmat/temporal_integration.py`
