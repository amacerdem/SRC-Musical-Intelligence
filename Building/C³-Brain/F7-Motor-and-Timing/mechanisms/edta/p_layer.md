# EDTA — Cognitive Present

**Model**: Expertise-Dependent Tempo Accuracy
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: β
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 5 | beat_tracking | Current beat tracking state. Aggregated beat induction signal from onset detection and energy periodicity. Measures how well the system is currently tracking beat events. Maps to basal ganglia beat-specific activation (Grahn & Brett 2007: putamen Z=5.67 for metric > complex rhythms). |
| 6 | meter_state | Current metrical state. Aggregated meter extraction signal from loudness periodicity and energy dynamics at H11. Measures the current strength of metrical structure perception. Maps to SMA continuous beat-strength encoding (Hoddinott & Grahn 2024: C-Score model). |

---

## H³ Demands

No additional unique H³ demands beyond E/M layers. The P-layer reuses tuples from E and M layers.

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| — | — | — | — | — | No unique H³ demands; reuses E/M layer tuples |

---

## Computation

The P-layer computes the real-time state of tempo tracking:

1. **Beat tracking** (idx 5): Current beat detection aggregation from onset signals and energy periodicity. Represents the real-time quality of pulse extraction from the auditory input. Higher when onsets are clear and periodic.

2. **Meter state** (idx 6): Current metrical perception from loudness and energy patterns at the psychological present (H11 = 500ms). Represents the system's current estimate of metrical structure strength.

Both outputs are sigmoid-bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_beat_accuracy | Beat signals for tracking |
| M-layer | tempo_stability | Stability context for meter state |
| H³ (shared) | Reuses E/M tuples | Current-state features |
