# CDEM P-Layer — Cognitive Present (2D)

**Layer**: Present Processing (P)
**Indices**: [5:7]
**Scope**: internal
**Activation**: clamp [0, 1]

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:binding_state | [0, 1] | Current cross-modal binding activation. encoding.mean * stumpf. High when the hippocampus is actively binding auditory and contextual features into a unified episodic trace. Borderie et al. 2024: theta-gamma CFC in hippocampus + STS supports auditory memory binding (iEEG). Billig 2022: hippocampal trisynaptic loop for auditory binding (review). |
| 6 | P1:arousal_gate | [0, 1] | Context-modulated arousal gate. arousal.mean * (1 - entropy). High when arousal is strong AND context is simple (low entropy). Gated arousal — complex contexts suppress the arousal response. Mori & Zatorre 2024: state-dependent auditory-reward FC predicts chills (fMRI, N=49, r=0.53). Calabria 2023: arousal x mood regulation interaction for music-memory (MCI patients). |

---

## Design Rationale

1. **Binding State (P0)**: The present-moment cross-modal binding signal. This is the product of encoding state and stumpf fusion — both must be active for binding to occur. When this signal is high, the hippocampus is actively integrating auditory features with contextual information into a unified episodic trace. This is the real-time "context is being bound" signal. Supported by Borderie 2024's iEEG evidence of theta-gamma phase-amplitude coupling in hippocampus+STS during auditory memory tasks.

2. **Arousal Gate (P1)**: The context-modulated arousal gate. This controls how much emotional arousal reaches downstream memory processes. The product of arousal and inverse entropy means high arousal in simple contexts produces strong gating (music alone = more arousing), while complex contexts (high entropy) suppress the gate. This implements the key finding from Mitterschiffthaler 2007 that music alone activates amygdala more strongly than music with competing stimuli.

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 20, 1, 0) | loudness mean H20 L0 | Average arousal over 5s context |
| (21, 20, 4, 0) | spectral_flux max H20 L0 | Peak context change over 5s |
| (11, 20, 4, 0) | onset_strength max H20 L0 | Peak event onset over 5s for binding |

P-layer primarily aggregates C+M outputs rather than introducing many new H3 tuples.

---

## Brain Regions

| Region | MNI / Talairach | P-Layer Role |
|--------|-----------------|-------------|
| Hippocampus | +/-20, -24, -12 (MNI) | P0: active cross-modal binding via pattern completion |
| mPFC / dMPFC | MNI: ~0, 38, 44 (BA8/9) | P0: self-referential context evaluation |
| STG / STS | Cortical surface (MNI) | P0: multimodal auditory-visual integration |
| Ventral striatum | Talairach: -8, 10, -6 (L) | P1: reward processing for emotionally congruent contexts |

---

## Scientific Foundation

- **Borderie et al. 2024**: Theta-gamma CFC in hippocampus + STS supports auditory memory retention (iEEG, epilepsy patients)
- **Billig et al. 2022**: Hippocampal trisynaptic loop (CA1, CA3, DG) for auditory context binding (comprehensive review)
- **Mori & Zatorre 2024**: Pre-listening auditory-reward FC predicts chills duration (fMRI, N=49, r=0.53)
- **Calabria et al. 2023**: Arousal x mood regulation interaction modulates music-memory in MCI patients (behavioral)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/cdem/cognitive_present.py`
