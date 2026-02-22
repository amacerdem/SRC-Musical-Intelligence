# NEMAC M+W-Layer — Temporal Integration (5D)

**Layer**: Memory Integration (M) + Well-being (W)
**Indices**: [2:7]
**Scope**: internal
**Activation**: sigmoid | tanh | clamp [0, 1]

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 2 | M0:mpfc_activation | [0, 1] | Self-referential processing. mPFC activation level. mpfc = sigma(0.5 * memory_reward + 0.5 * familiarity). "This is MY music" signal — the self-reference component that distinguishes nostalgia from mere recognition. Barrett 2010: mPFC engagement during nostalgic music. |
| 3 | M1:hippocampus_activ | [0, 1] | Memory retrieval strength. Hippocampal episodic recall activation. hippocampus = sigma(0.5 * warmth + 0.5 * familiarity). Pattern completion for autobiographical memory retrieval. Janata 2007: music-evoked autobiographical memories via hippocampal binding. |
| 4 | M2:memory_vividness | [0, 1] | Autobiographical memory clarity. Combined memory and self-reference quality. vividness = tanh(mpfc * hippocampus * 2.0). Multiplicative gate: both self-reference and memory retrieval must be active for vivid recall. Sakakibara 2025: nostalgia enhances memory vividness (eta_p^2=0.541). |
| 5 | W0:nostalgia_intens | [0, 1] | Nostalgic feeling strength. nostalgia_intensity = clamp(f11 * boost, 0, 1). Self-selected boost factor of 1.2 for personally chosen music. Sakakibara 2025: self > other-selected, d = 0.88. |
| 6 | W1:wellbeing_enhance | [-1, 1] | Mood improvement from nostalgia. wellbeing = tanh(0.7 * nostalgia_intensity). Nostalgic engagement drives positive well-being shift proportional to nostalgia intensity. Sakakibara 2025: nostalgia → well-being enhancement via N-BMI loop. |

---

## Design Rationale

1. **mPFC Activation (M0)**: Tracks the self-referential processing component of the memory-affect circuit. Self-reference is computed as the average of memory-reward coupling (how rewarding is the retrieved memory?) and familiarity (how well-known is this music?). This captures the finding that personal significance is necessary — unfamiliar music may be pleasant but does not evoke nostalgia.

2. **Hippocampal Activation (M1)**: Tracks episodic memory retrieval strength. Combines timbral warmth (the acoustic familiarity cue) with overall familiarity estimation. Warmth is a powerful nostalgia trigger because warm timbres are associated with early musical experiences (lullabies, family environments).

3. **Memory Vividness (M2)**: The multiplicative binding of self-reference and memory retrieval. Uses tanh for [-1,1] range compressed by the 2.0 scaling factor. Both mPFC and hippocampus must be jointly active for vivid autobiographical memory — this captures the finding that nostalgia requires both personal significance AND successful memory retrieval.

4. **Nostalgia Intensity (W0)**: Integrates the E-layer nostalgia score with a self-selected music boost (1.2x). The self-selected advantage reflects the consistent finding that personally chosen music produces stronger nostalgic responses.

5. **Well-being Enhancement (W1)**: The therapeutic outcome of nostalgia. Uses tanh for bidirectional range, with a 0.7 coefficient reflecting the estimated nostalgia-to-wellbeing transfer efficiency. Negative values possible when nostalgia triggers bittersweet or painful memories.

---

## H3 Dependencies (M+W-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 16, 0, 2) | sensory_pleasantness value H16 L2 | Current pleasantness for reward computation |
| (22, 16, 20, 2) | entropy entropy H16 L2 | Predictability — low entropy = familiar |
| (22, 20, 1, 0) | entropy mean H20 L0 | Average complexity over 5s |
| (10, 20, 1, 0) | loudness mean H20 L0 | Average arousal over 5s consolidation |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | Valence proxy (inverse) for memory-reward |
| [4] | sensory_pleasantness | Hedonic signal for memory-reward coupling |
| [10] | loudness | Arousal correlate for well-being arousal component |
| [22] | distribution_entropy | Predictability — low = familiar = strong memory |

---

## Scientific Foundation

- **Barrett et al. 2010**: Nostalgic music activates mPFC + hippocampus; personality modulates response (behavioral, N=226)
- **Janata et al. 2007**: Music-evoked autobiographical memories — 30-80% trigger rate with familiar songs (behavioral, N~300)
- **Sakakibara 2025**: Self > other-selected for nostalgia (d=0.88); nostalgia enhances memory vividness (eta_p^2=0.541); N-BMI loop validates well-being enhancement (EEG, N=33)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/nemac/temporal_integration.py`
