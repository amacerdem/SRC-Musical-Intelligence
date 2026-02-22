# SNEM P-Layer — Cognitive Present (3D)

**Layer**: Present Processing (P)
**Indices**: [6:9]
**Scope**: exported (kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 6 | P0:beat_locked_activity | [0, 1] | Beat-locked neural activity state. Combines E-layer beat entrainment with M-layer enhancement to produce the real-time "am I locked to the beat" signal. Grahn & Brett 2007: beat perception in motor areas. |
| 7 | P1:entrainment_strength | [0, 1] | Oscillation entrainment coupling strength. How tightly neural oscillations are phase-locked to the external rhythm. Yang 2025: PLV=0.76 frontal-parietal at fast tempo. |
| 8 | P2:selective_gain | [0, 1] | Attentional gain for beat-aligned events. Multiplicative attention gate — events on the beat receive amplified processing. Nozaradan 2012: selective enhancement above envelope. |

---

## Design Rationale

1. **Beat-Locked Activity (P0)**: The summary "present-moment" signal for beat tracking. This is the primary F3 output that the kernel scheduler reads as `beat_locked`. It feeds the Core belief `beat_entrainment`.

2. **Entrainment Strength (P1)**: Phase-locking value between internal oscillation and external rhythm. This is the coupling strength — can be high even when meter position is uncertain. Feeds both `beat_entrainment` and `meter_hierarchy` Core beliefs.

3. **Selective Gain (P2)**: The attention gate. This is the output that the kernel uses as a multiplicative factor: `salience *= 1 + 0.3 * selective_gain`. Higher selective gain means stronger attentional amplification of on-beat events.

---

## Kernel Relay Export

P-layer outputs are the primary relay exports:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `beat_locked` | P0 [6] | Salience mixer: 0.35 × relay component |
| `entrainment_strength` | P1 [7] | Salience mixer: relay component |
| `selective_gain` | P2 [8] | Multiplicative gate: value *= 1 + 0.3 × selective_gain |

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (11, 0, 0, 2) | onset_strength value H0 L2 | Instantaneous onset for beat-lock |
| (11, 3, 1, 2) | onset_strength mean H3 L2 | Sustained onset 100ms |
| (8, 3, 0, 2) | loudness value H3 L2 | Perceptual loudness at beat scale |

---

## Scientific Foundation

- **Grahn & Brett 2007**: Beat perception recruits SMA + basal ganglia (fMRI, N=27)
- **Yang et al. 2025**: PLV=0.76 frontal-parietal connectivity at fast tempo (EEG, N=26)
- **Nozaradan 2012**: Selective enhancement beyond acoustic envelope (EEG, N=9)

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/snem/cognitive_present.py`
