# MEAMN P-Layer — Cognitive Present (3D)

**Layer**: Present Processing (P)
**Indices**: [5:8]
**Scope**: exported (kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:memory_state | [0, 1] | Current memory retrieval activation. Retrieval_dynamics aggregation — how strongly the hippocampus-mPFC-PCC hub is engaged right now. Janata 2009: dorsal MPFC tracks tonal space movement parametrically. |
| 6 | P1:emotional_color | [0, 1] | Affective tag strength on current memory. arousal * (1-roughness) — emotional intensity of the retrieved memory. Sakakibara 2025: nostalgia enhances memory vividness (eta_p^2=0.541). |
| 7 | P2:nostalgia_link | [0, 1] | Nostalgia-familiarity warmth signal. familiarity * x_l5l7.mean — the consonance-timbre interaction weighted by familiarity. Sakakibara 2025: acoustic similarity triggers nostalgia (Cohen's r=0.878 older). |

---

## Design Rationale

1. **Memory State (P0)**: The summary "present-moment" signal for memory retrieval. This is the primary F4 output that the kernel scheduler reads as `memory_state`. It aggregates the retrieval dynamics from E-layer and M-layer into a single activation level indicating how strongly autobiographical memory is currently being accessed.

2. **Emotional Coloring (P1)**: The affective tag applied to the current memory. Combines arousal (loudness-based) with valence (consonance-based) to produce the emotional quality of the retrieved memory. This feeds the kernel's familiarity computation and downstream reward processing via MEAMN relay.

3. **Nostalgia Link (P2)**: The warmth-familiarity binding signal. This is the specific output that captures the "this music reminds me of..." experience. Uses consonance-timbre interaction (x_l5l7) as the acoustic basis for nostalgia, modulated by familiarity strength.

---

## Kernel Relay Export

P-layer outputs are the primary relay exports:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `memory_state` | P0 [5] | Familiarity computation: familiarity module input |
| `emotional_color` | P1 [6] | Reward: emotion component of hedonic signal |
| `nostalgia_link` | P2 [7] | Familiarity + Reward: nostalgia-enhanced binding |

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (14, 16, 0, 2) | tonalness value H16 L2 | Melodic recognition state |
| (14, 20, 1, 0) | tonalness mean H20 L0 | Tonal stability over 5s |
| (3, 24, 1, 0) | stumpf_fusion mean H24 L0 | Long-term binding context |

---

## Scientific Foundation

- **Janata 2009**: Dorsal MPFC parametrically tracks autobiographical salience; left-lateralized FAV (fMRI 3T, N=13, t(12)=2.96, p=0.012)
- **Sakakibara et al. 2025**: Nostalgia enhances memory vividness (eta_p^2=0.541) and well-being; acoustic similarity as nostalgia trigger (EEG, N=33)
- **Barrett et al. 2010**: Music-evoked nostalgia modulated by arousal, valence, and personality (behavioral)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/meamn/cognitive_present.py`
