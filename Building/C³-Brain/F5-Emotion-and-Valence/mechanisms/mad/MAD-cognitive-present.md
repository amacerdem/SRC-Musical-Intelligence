# MAD P-Layer — Cognitive Present (2D)

**Layer**: Cognitive Present (P)
**Indices**: [7:9]
**Scope**: exported (kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | P0:impaired_reward | [0, 1] | Real-time disrupted reward signal. reward_signal * connectivity. In anhedonia: attenuated toward zero because connectivity near zero despite normal auditory input. The product of reward and connectivity captures the pathway-specific attenuation. Martinez-Molina 2016: NAcc deficit d=3.6-7.0. |
| 8 | P1:preserved_auditory | [0, 1] | Intact auditory processing signal. sigma(0.5 * auditory_response + 0.5 * loudness[10]). R3 spectral features fully functional — confirms the deficit is not perceptual. Normal values in anhedonia validate that hearing is intact. Loui 2017: preserved auditory perception. |

---

## Design Rationale

1. **Impaired Reward (P0)**: Captures the core real-time manifestation of musical anhedonia — the moment-to-moment attenuation of reward signal due to structural disconnection. Computed as the product of the reward projection signal and connectivity estimate. In normal listeners, connectivity is near 1.0 and the full reward signal propagates. In anhedonia, connectivity is near 0.0 and the reward signal is multiplicatively abolished regardless of how pleasant the music objectively is. This dimension should correlate with absent chills, absent SCR, and absent NAcc BOLD in anhedonia (Martinez-Molina 2016).

2. **Preserved Auditory (P1)**: The control dimension — confirms that the auditory processing pathway is intact. Uses a weighted combination of the H3-integrated auditory response and the R3 loudness feature. In musical anhedonia, this dimension remains normal (near 0.5-0.8), proving that the listener hears and processes music normally at the cortical level. The dissociation between low P0 and normal P1 is the real-time signature of musical anhedonia. Loui 2017 confirmed normal auditory discrimination in anhedonics.

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 6, 0, 0) | loudness value H6 L0 | Instantaneous arousal for preserved auditory check |
| (4, 6, 0, 0) | sensory_pleasantness value H6 L0 | Instantaneous hedonic response — absent reward in anhedonia |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [10] | loudness | P1: arousal signal for preserved auditory confirmation |
| [12] | spectral_centroid | P1: brightness (preserved spectral analysis) |
| [14] | tonalness | P1: tonal quality (preserved) |
| [4] | sensory_pleasantness | P0: hedonic signal, attenuated by connectivity |

---

## Scientific Foundation

- **Martinez-Molina et al. 2016**: NAcc deficit d=3.6-7.0 in musical anhedonia; normal STG activation confirmed (fMRI + DTI, N=45)
- **Loui et al. 2017**: Preserved auditory perception in anhedonics; white matter deficit is pathway-specific (DTI + behavioral, N=17)
- **Mas-Herrero et al. 2014**: Double dissociation — music reward absent, monetary reward present (behavioral, significant)
- **Belfi & Loui 2020**: Musical anhedonia model — rewards of music listening absent despite intact perception (review)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/mad/cognitive_present.py`
