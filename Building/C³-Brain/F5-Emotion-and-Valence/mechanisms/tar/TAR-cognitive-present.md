# TAR P-Layer — Cognitive Present (1D)

**Layer**: Present Processing (P)
**Indices**: [7:8]
**Scope**: exported (kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | P0:therapeutic_reward | [0, 1] | Real-time therapeutic reward signal. therapeutic_reward = sigma(0.3 * f14 + 0.3 * consonance + 0.4 * c0p_mean). Tracks whether the music is "working" — whether the therapeutic intent is producing measurable reward circuit activation. Combines the overall therapeutic efficacy (E-layer), current consonance, and cognitive-projection mean from H3. Ehrlich 2019: BCI emotion modulation via music achieves 3/5 success rate. |

---

## Design Rationale

1. **Therapeutic Reward (P0)**: The present-moment assessment of therapeutic effectiveness. This is the "is it working?" signal that tracks whether the current music is producing the intended therapeutic outcome. Combines three signals: the E-layer therapeutic efficacy estimate (overall quality of the therapeutic prescription match), current consonance (direct reward pathway activation), and the cognitive-projection H3 mean (temporal integration of the reward signal). The 0.3/0.3/0.4 weighting prioritizes the temporal context from H3 because therapeutic effects build over time — instantaneous features alone are insufficient to assess whether therapy is progressing.

---

## Kernel Relay Export

P-layer output feeds the kernel relay for cross-function integration:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `therapeutic_reward` | P0 [7] | Reward: therapeutic reward contribution to hedonic signal |

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 11, 1, 0) | sensory_pleasantness mean H11 L0 | Cognitive-projection reward state |
| (4, 15, 1, 0) | sensory_pleasantness mean H15 L0 | Peak therapeutic response magnitude |
| (0, 16, 0, 2) | roughness value H16 L2 | Current consonance for reward |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | P0: inverse consonance for reward computation |
| [4] | sensory_pleasantness | P0: direct hedonic for reward signal |
| [5] | harmonicity | P0: harmonic purity for consonance |

---

## Scientific Foundation

- **Ehrlich et al. 2019**: Closed-loop music-based BCI for emotion mediation — 3/5 success rate demonstrates real-time therapeutic monitoring feasibility (BCI, N=5, PLOS ONE)
- **Koelsch 2014**: Consonance drives reward pathway activation — basis for therapeutic reward tracking (review, Nature Reviews Neuroscience, 15(3), 170-180)
- **Fu et al. 2025**: Music therapy prevents PPD via neurogenesis and synaptic plasticity — reward pathway engagement is the therapeutic mechanism (mouse model, Translational Psychiatry)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/tar/cognitive_present.py`
