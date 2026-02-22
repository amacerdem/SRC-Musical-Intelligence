# NEMAC P-Layer — Cognitive Present (2D)

**Layer**: Present Processing (P)
**Indices**: [7:9]
**Scope**: exported (kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | P0:nostalgia_correl | [0, 1] | R3 warmth x affective-dynamics spectral nostalgia cue. nostalgia_correl = sigma(R3.sensory_pleasantness[4] * warmth * 2.0). The real-time acoustic nostalgia correlate — how strongly the current spectral content matches the timbral signature of nostalgia-inducing music. Sakakibara 2025: acoustic features predict nostalgia, r = 0.985. |
| 8 | P1:memory_reward_lnk | [0, 1] | Memory x cognitive-projection reward from retrieval. memory_reward_link = sigma(familiarity * projection_mean * 2.0). The coupling strength between autobiographical memory retrieval and reward circuit activation. Janata 2009: mPFC tracks autobiographical salience parametrically (t(9)=5.784). |

---

## Design Rationale

1. **Nostalgia Correlate (P0)**: The present-moment acoustic nostalgia signal. Uses sensory pleasantness (hedonic quality) multiplied by timbral warmth to produce a real-time estimate of how "nostalgic" the current sound is. This is the spectral fingerprint of nostalgia — warm, consonant music consistently triggers stronger nostalgic responses. The 2.0 scaling factor before sigmoid sharpens the discrimination between nostalgic and non-nostalgic timbral profiles.

2. **Memory-Reward Link (P1)**: The coupling between memory retrieval and reward activation. Uses familiarity strength multiplied by the cognitive-projection H3 mean to estimate how strongly the retrieved memory is generating reward. This captures the finding that not all memories are equally rewarding — vivid, positively-valenced memories produce stronger reward circuit activation.

---

## Kernel Relay Export

P-layer outputs feed the kernel relay for cross-function integration:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `nostalgia_correl` | P0 [7] | Familiarity computation: nostalgia-weighted acoustic match |
| `memory_reward_lnk` | P1 [8] | Reward: memory-derived hedonic signal |

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 16, 0, 2) | sensory_pleasantness value H16 L2 | Current hedonic quality for nostalgia correlate |
| (12, 16, 0, 2) | warmth value H16 L2 | Timbral warmth for nostalgia detection |
| (14, 20, 1, 0) | tonalness mean H20 L0 | Tonal stability for familiarity estimation |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [4] | sensory_pleasantness | P0: hedonic quality for nostalgia correlate |
| [12] | spectral_centroid | P0: warmth proxy (low centroid = warm) |
| [14] | tonalness | P1: tonal quality for familiarity estimation |

---

## Scientific Foundation

- **Sakakibara 2025**: Acoustic features predict nostalgia with r = 0.985; EEG decoder accuracy 64.0% younger, 71.5% older (EEG + ML, N=33)
- **Janata 2009**: Dorsal MPFC parametrically tracks autobiographical salience (fMRI 3T, N=13, t(9)=5.784, p<0.0003)
- **Scarratt et al. 2025**: Familiar music activates auditory, motor, emotion, and memory areas; 4 distinct response clusters (fMRI, N=57)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/nemac/cognitive_present.py`
