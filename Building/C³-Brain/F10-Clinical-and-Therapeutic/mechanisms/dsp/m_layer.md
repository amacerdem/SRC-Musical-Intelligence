# DSP — Temporal Integration

**Model**: Developmental Singing Plasticity
**Unit**: NDU
**Function**: F10 Clinical & Therapeutic
**Tier**: beta
**Layer**: M — Temporal Integration
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 4 | cumulative_plasticity | Long-term singing exposure accumulation. Exponential moving average of singing quality (f01) over session timescale, tracking the cumulative neural maturation driven by repeated high-quality singing exposure. Uses mean consonance at 1s beat timescale as a long-horizon quality anchor. Partanen 2022: group x singing time interaction eta^2=0.262 — cumulative quality exposure predicts auditory processing enhancement. |
| 5 | session_memory | Recent session impact trace. Temporal integration of plasticity-relevant variation combining mean pitch change over 1s and spectral change variability at 100ms. Captures whether the current singing session provides sufficient melodic and spectral diversity to drive plasticity. Papatzikis 2024: 56 NICU studies confirm session-level music exposure effects on neonatal outcomes. |
| 6 | voice_recognition | Parental voice familiarity index. Derived from mean vocal coupling (x_l0l5) at 500ms forward-only horizon, tracking the stability of voice-specific acoustic features across time. Higher values indicate consistent, recognizable parental voice patterns. Kaminska 2025: voice-evoked delta brushes show stimulus-specific topography (mid-temporal), distinct from noise — voice discrimination develops in preterm period. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 8 | 4 | 16 | M1 (mean) | L2 (bidi) | Mean consonance over 1s beat window |
| 9 | 23 | 16 | M1 (mean) | L2 (bidi) | Mean pitch change over 1s |
| 10 | 21 | 3 | M2 (std) | L2 (bidi) | Spectral change variability at 100ms |
| 11 | 25 | 8 | M1 (mean) | L0 (fwd) | Mean vocal coupling over 500ms forward |

---

## Computation

The M-layer integrates E-layer outputs over time to maintain plasticity dynamics memory:

1. **Cumulative plasticity** (idx 4): Temporal smoothing of singing quality (f01) over a session-length timescale, anchored by mean consonance at the 1s beat horizon. This tracks the accumulated effect of high-quality parental singing on auditory cortex maturation. Under the quality-over-quantity principle (Partanen 2022), cumulative plasticity grows faster when singing quality is high even if total singing duration is modest. The 1s mean consonance provides a stable reference that smooths out frame-level fluctuations in vocal harmonics.

2. **Session memory** (idx 5): Integrates recent singing session diversity through mean pitch change at 1s and spectral change variability at 100ms. A session with varied melodic contours (high mean pitch change) and rich spectral dynamics (high spectral variability) produces a stronger session memory trace, indicating that the current exposure is driving active plasticity. Low values indicate monotonous singing that may not engage the plasticity mechanisms as effectively.

3. **Voice recognition** (idx 6): Tracks parental voice familiarity through the forward-only mean of vocal coupling at 500ms. The L0 (forward) law is used because voice recognition develops cumulatively — each new frame of consistent voice features strengthens recognition without requiring backward reanalysis. Kaminska 2025 demonstrated that preterm infants develop voice-specific neural responses (delta brushes with mid-temporal T7-T8 topography) distinguishable from non-voice stimuli, establishing that voice discrimination is active during the preterm period.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_singing_quality | Input to cumulative plasticity EMA |
| R3 [4] | consonance | Long-horizon quality anchor via H3 mean |
| R3 [21] | spectral_change | Spectral diversity for session impact assessment |
| R3 [23] | pitch_change | Melodic diversity for session memory |
| R3 [25] | x_l0l5[0] | Vocal coupling stability for voice familiarity |
| H3 | 4 tuples (see above) | Mean consonance, mean pitch change, spectral variability, vocal coupling |
