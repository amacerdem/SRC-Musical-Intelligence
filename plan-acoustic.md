# Plan: Acoustic Mode + Default 4P

## Overview
Add "Acoustic" mode alongside "NeuroAcoustic" in the Lab page top panel. Acoustic shows direct R³ perceptual signals (what the sound IS), NeuroAcoustic shows C³ cognitive outputs (what the brain DOES with the sound).

---

## 1. Default Peak Count → 4P
**File:** `Lab.tsx` — Change `useState<4 | 8 | 16>(8)` → `useState<4 | 8 | 16>(4)`

---

## 2. R³ Acoustic Dimension Selections

Verified against R³ Ontology v1.0.0 (FROZEN). All indices from the 97D post-dissolution map.

### 6D — Essential Sound
| # | R³[idx] | Feature | EN | TR | Family Color |
|---|---------|---------|-----|-----|-------------|
| 0 | [10] | loudness | Loudness | Gürlük | #F97316 |
| 1 | [13] | sharpness | Brightness | Parlaklık | #F59E0B |
| 2 | [0] | roughness | Roughness | Pürüz | #14B8A6 |
| 3 | [42] | beat_strength | Pulse | Nabız | #0EA5E9 |
| 4 | [21] | spectral_flux | Movement | Hareket | #F43F5E |
| 5 | [51] | key_clarity | Harmony | Harmoni | #8B5CF6 |

### +6 → 12D Detailed Sound
| # | R³[idx] | Feature | EN | TR | Color |
|---|---------|---------|-----|-----|-------|
| 6 | [12] | warmth | Warmth | Sıcaklık | #F97316CC |
| 7 | [11] | onset_strength | Attack | Atak | #F59E0BCC |
| 8 | [22] | distribution_entropy | Richness | Zenginlik | #14B8A6CC |
| 9 | [41] | tempo_estimate | Tempo | Tempo | #0EA5E9CC |
| 10 | [48] | event_density | Density | Yoğunluk | #F43F5ECC |
| 11 | [37] | pitch_height | Pitch | Perde | #8B5CF6CC |

### +12 → 24D Full Analysis
| # | R³[idx] | Feature | EN | TR | Color |
|---|---------|---------|-----|-----|-------|
| 12 | [4] | sensory_pleasantness | Consonance | Uyum | #F9731699 |
| 13 | [14] | tonalness | Tonalness | Tonalite | #F59E0B99 |
| 14 | [16] | spectral_smoothness | Smoothness | Pürüzsüzlük | #14B8A699 |
| 15 | [47] | groove_index | Groove | Groove | #0EA5E999 |
| 16 | [44] | syncopation_index | Syncopation | Senkop | #F43F5E99 |
| 17 | [60] | tonal_stability | Stability | Kararlılık | #8B5CF699 |
| 18 | [8] | velocity_A | Speed | Hız | #F9731677 |
| 19 | [15] | clarity | Clarity | Netlik | #F59E0B77 |
| 20 | [94] | alpha_ratio | Bass Weight | Bas Ağırlığı | #14B8A677 |
| 21 | [50] | rhythmic_regularity | Regularity | Düzenlilik | #0EA5E977 |
| 22 | [59] | harmonic_change | Chord Flow | Akor Akışı | #F43F5E77 |
| 23 | [89] | modulation_centroid | Vibrato | Titreşim | #8B5CF677 |

**6 Families** (each has 4 members across depth levels):
- Sound Power (#F97316): Loudness → Warmth → Consonance → Speed
- Sound Color (#F59E0B): Brightness → Attack → Tonalness → Clarity
- Texture (#14B8A6): Roughness → Richness → Smoothness → Bass Weight
- Rhythm (#0EA5E9): Pulse → Tempo → Groove → Regularity
- Motion (#F43F5E): Movement → Density → Syncopation → Chord Flow
- Harmony (#8B5CF6): Harmony → Pitch → Stability → Vibrato

**Depth = direct signals** (NOT tree averages):
- 6D → dims 0-5, 12D → dims 0-11, 24D → dims 0-23

---

## 3. Python Pipeline (3 lines)
**File:** `Repetuare/generate_full_dataset.py`

```python
ACOUSTIC_R3_IDX = [10,13,0,42,21,51, 12,11,22,41,48,37, 4,14,16,47,44,60,8,15,94,50,59,89]
acoustic_segs = _seg_stats(r3_np[:, ACOUSTIC_R3_IDX], N_SEGMENTS)
# In temporal_profile dict:
"acoustic_per_segment": _round_matrix(acoustic_segs),  # (64, 24)
```

---

## 4. Frontend Changes

### 4a. Types (`mi-dataset.ts`, `dimensions.ts`)
- Add `acoustic_per_segment?: number[][]` to temporal_profile
- Add `acoustic_6d/12d/24d?: number[]` to DimensionState

### 4b. Dimension Definitions (`dimensions.ts`)
- Add `ALL_ACOUSTIC` array (24 entries) with r3Index, name, nameTr, color, parentKey
- Add `ALL_ACOUSTIC_6D/12D/24D` as slices
- Add `computeAcousticSlice(r3_24: number[])` helper

### 4c. Lab Store (`useLabStore.ts`)
- Add `labMode: "neuro" | "acoustic"` state
- In compute functions: if acoustic_per_segment exists, slice into 6/12/24 per segment

### 4d. Lab Page (`Lab.tsx`)
- Default peakCount → 4
- Add `[NeuroAcoustic | Acoustic]` segmented toggle in Panel 1 header
- Pass mode to FlowTimeline

### 4e. FlowTimeline (`FlowTimeline.tsx`)
- New prop: `mode: "neuro" | "acoustic"`
- Switch dimList based on mode
- Switch getDimValues to return acoustic arrays when mode=acoustic
- Visual differentiation:
  - Left strip bg: neuro=`rgba(6,6,14,0.95)` / acoustic=`rgba(14,10,6,0.95)`
  - Hide reward heatmap + neurochemical strips in acoustic mode
  - Acoustic color palette auto-applied via dimension definitions

---

## 5. Visual Differentiation

| Aspect | NeuroAcoustic | Acoustic |
|--------|--------------|----------|
| Palette | Cool neons | Warm earth tones |
| Left strip | Cool tint | Warm tint |
| Reward heatmap | Shown | Hidden |
| Neuro strips | Shown at 12D+ | Hidden |
| Data source | C³ beliefs → tree | R³ direct signals |

---

## 6. Implementation Order
1. Default peak count 4P (trivial, Lab.tsx)
2. Acoustic dimension definitions (dimensions.ts)
3. TypeScript types (mi-dataset.ts, dimensions.ts)
4. Lab store: labMode + acoustic computation (useLabStore.ts)
5. Mode toggle UI (Lab.tsx)
6. FlowTimeline mode support (FlowTimeline.tsx)
7. Python pipeline + regenerate dataset
8. Build & verify
