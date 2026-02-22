# CDEM C-Layer — Extraction (3D)

**Layer**: Context-Dependent Features (C)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | C0:context_modulation | [0, 1] | Cross-modal context modulation. Hippocampus + ACC multi-modal binding. f43 = sigma(0.35 * x_l0l5.mean * encoding + 0.35 * (1-roughness) * familiar + 0.30 * stumpf * retrieval). Sachs et al. 2025: same-valence context shifts brain-state transitions 6.26s earlier (fMRI, N=39, z=3.6-4.32). |
| 1 | C1:arousal_suppression | [0, 1] | Context-dependent arousal suppression. Amygdala arousal gated by context. f44 = sigma(0.40 * arousal * loudness + 0.30 * entropy * (1-stumpf) + 0.30 * flux * amplitude). Mitterschiffthaler et al. 2007: sad music activates R hippocampus/amygdala (N=16, Z=3.25). |
| 2 | C2:encoding_strength | [0, 1] | Context-dependent encoding strength. Hippocampus + mPFC consolidation. f45 = sigma(0.40 * encoding * x_l5l7.mean + 0.30 * (1-roughness) * warmth + 0.30 * expectancy * stumpf). Cheung et al. 2019: uncertainty x surprise jointly predict pleasure and amygdala/hippocampus activity (N=40). |

---

## Design Rationale

1. **Context Modulation (C0)**: Tracks how cross-modal context shapes memory encoding. Uses energy-consonance interaction (x_l0l5) as the context-memory binding signal, consonance times familiarity for mood-congruent encoding, and stumpf times retrieval for context-dependent retrieval strength. The hippocampus binds auditory and contextual features into a unified episodic trace. Primary basis: Sachs 2025 showing tempoparietal brain-state transitions track emotional changes to music.

2. **Arousal Suppression (C1)**: Tracks how visual/environmental context dampens the arousal response to music. Music alone activates amygdala more strongly than music-with-video. Uses arousal times loudness (the raw arousal signal), entropy times inverse binding (contextual complexity), and spectral flux times amplitude (context change rate). Basis: Mitterschiffthaler 2007 showing valence-specific activation of hippocampal-amygdalar complex.

3. **Encoding Strength (C2)**: Tracks the strength of context-dependent memory formation. Uses encoding times consonance-timbre interaction (x_l5l7) for mood-congruent encoding, consonance times warmth for emotional congruency, and expectancy times binding for prediction-driven encoding. Basis: Cheung 2019 showing prediction error drives amygdala-hippocampal engagement.

---

## H3 Dependencies (C-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 16, 1, 2) | stumpf_fusion mean H16 L2 | Binding stability at 1s for context modulation |
| (4, 16, 0, 2) | sensory_pleasantness value H16 L2 | Current mood input for congruency |
| (10, 16, 0, 2) | loudness value H16 L2 | Current arousal level for suppression |
| (0, 16, 0, 2) | roughness value H16 L2 | Current valence (inverse) for context |
| (21, 16, 0, 2) | spectral_flux value H16 L2 | Context change rate |
| (22, 16, 0, 2) | entropy value H16 L2 | Current context complexity |
| (12, 16, 0, 2) | warmth value H16 L2 | Current context warmth |
| (11, 16, 0, 2) | onset_strength value H16 L2 | Event boundary detection for context shifts |
| (7, 16, 8, 0) | amplitude velocity H16 L0 | Energy change rate for arousal dynamics |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | C0+C2: valence proxy (1 - roughness = consonance) |
| [3] | stumpf_fusion | C0+C1+C2: binding strength proxy |
| [4] | sensory_pleasantness | C2: mood congruency input |
| [7] | amplitude | C1: arousal correlate |
| [10] | loudness | C1: arousal proxy |
| [11] | onset_strength | C0: event salience / context boundary |
| [12] | warmth | C2: context warmth |
| [14] | tonalness | Pattern clarity |
| [21] | spectral_flux | C1: context change detection |
| [22] | entropy | C1+C2: context complexity |
| [24] | spectral_concentration | Event salience |
| [25:33] | x_l0l5 | C0: context-memory binding strength |
| [41:49] | x_l5l7 | C0+C2: mood congruency signal |

---

## Brain Regions

| Region | MNI / Talairach | C-Layer Role |
|--------|-----------------|-------------|
| Hippocampus | +/-20, -24, -12 (MNI) | C0+C2: context-dependent episodic encoding; pattern completion |
| Amygdala | Talairach: 24, -15, -20 (R) | C1: emotional tagging modulated by context |
| ACC | Talairach: -4, 10, 36 (BA32) | C0+C1: context-music conflict monitoring; arousal gating |
| STG / STS | Cortical surface (MNI) | C0: tempoparietal emotion tracking; multimodal integration |

---

## Scientific Foundation

- **Sachs et al. 2025**: Emotions in the brain are dynamic and contextually dependent; tempoparietal brain-state transitions track emotional changes (fMRI, N=39, z=3.6-4.32)
- **Mitterschiffthaler et al. 2007**: Happy music -> ventral striatum + ACC; Sad music -> R hippocampus/amygdala (fMRI, N=16, Z=3.25-4.96)
- **Cheung et al. 2019**: Uncertainty x surprise jointly predict musical pleasure and amygdala/hippocampus activity (fMRI, N=40)
- **Billig et al. 2022**: Hippocampus binds auditory information with spatiotemporal context (comprehensive review)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/cdem/extraction.py`
