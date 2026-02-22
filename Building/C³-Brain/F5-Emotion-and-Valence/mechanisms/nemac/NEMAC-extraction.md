# NEMAC E-Layer — Extraction (2D)

**Layer**: Extraction (E)
**Indices**: [0:2]
**Scope**: internal
**Activation**: sigmoid | clamp [0, 1]

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:f05_chills | [0, 1] | Peak emotional magnitude at nostalgic moments. f05 = sigma(alpha * warmth * vividness * reward * 3.0). Chills emerge when nostalgic warmth, memory vividness, and reward activation converge. Salimpoor 2011: chills correlate with dopamine release, r = 0.84. |
| 1 | E1:f11_nostalgia | [0, 1] | Memory-enhanced emotional response. f11 = clamp(0.6 * mpfc + 0.4 * hippocampus, 0, 1). Weighted combination of self-referential processing (mPFC) and memory retrieval (hippocampus). Sakakibara 2025: nostalgic > non-nostalgic, d = 0.711. |

---

## Design Rationale

1. **Chills Intensity (E0)**: The peak emotional response during nostalgic listening. Computed as a multiplicative gate of warmth (timbral pleasantness), memory vividness (hippocampal-mPFC binding quality), and reward activation. The triple product ensures chills only emerge when all three conditions are simultaneously high — warm familiar music that vividly recalls personal history and activates the reward circuit. Primary basis: Salimpoor 2011 PET study showing dopamine release during musical chills.

2. **Nostalgia (E1)**: The core NEMAC extraction feature. Measures the strength of the nostalgia response as a weighted combination of self-referential processing (mPFC: "this is MY music") and autobiographical memory retrieval (hippocampus: episodic recall). The 0.6/0.4 weighting reflects the primacy of self-reference in nostalgia — recognition of personal significance drives the experience more than raw memory recall. Primary basis: Sakakibara 2025 EEG/behavioral study.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 16, 1, 2) | stumpf_fusion mean H16 L2 | Binding stability at 1s — coherence for chills |
| (3, 20, 1, 2) | stumpf_fusion mean H20 L2 | Binding over 5s consolidation window |
| (12, 16, 0, 2) | warmth value H16 L2 | Current timbre warmth — nostalgia cue |
| (12, 20, 1, 0) | warmth mean H20 L0 | Sustained warmth = nostalgia activation |
| (0, 16, 0, 2) | roughness value H16 L2 | Current dissonance — inverse valence |
| (0, 20, 18, 0) | roughness trend H20 L0 | Dissonance trajectory for chills buildup |
| (10, 16, 0, 2) | loudness value H16 L2 | Current arousal — chills magnitude |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | E1: inverse pleasantness for valence |
| [4] | sensory_pleasantness | E0: hedonic signal for warmth computation |
| [10] | loudness | E0: emotional intensity for chills magnitude |
| [12] | spectral_centroid | E0: brightness (low = warm) for nostalgia warmth |
| [14] | tonalness | E1: tonal quality for familiarity estimation |
| [25:33] | x_l0l5 | E0/E1: energy-consonance memory-affect binding |

---

## Scientific Foundation

- **Salimpoor et al. 2011**: Chills correlate with dopamine release in ventral striatum (PET, N=8, r=0.84)
- **Sakakibara 2025**: Nostalgic > non-nostalgic music response (EEG + behavioral, N=33, d=0.711)
- **Barrett et al. 2010**: Music-evoked nostalgia modulated by arousal, valence, and personality (behavioral)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/nemac/extraction.py`
