# OMS — Cognitive Present

**Model**: Oscillatory Motor Synchronization
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: β
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 5 | beat_prediction | Current beat anticipation state. Aggregated beat induction signal from onset detection and spectral flux at H6 (200ms). Represents the fronto-striatal network's real-time beat anticipation quality. Maps to putamen beat-specific activation (Grahn & Brett 2007: L putamen Z=5.67) and SMA continuous beat encoding (Hoddinott & Grahn 2024: C-Score model). |
| 6 | motor_locking | Current motor-auditory lock state. Aggregated sensorimotor coupling from dynamics-perceptual binding at H11 (500ms). Represents the temporo-parietal network's real-time rhythmic locking quality. Maps to STG-IPL gamma-band coupling (Potes 2012: 110ms auditory-motor delay, r=0.70). |

---

## H³ Demands

No additional unique H³ demands beyond E/M layers. The P-layer reuses tuples from E and M layers.

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| — | — | — | — | — | No unique H³ demands; reuses E/M layer tuples |

---

## Computation

The P-layer computes the real-time state of oscillatory motor synchronization:

1. **Beat prediction** (idx 5): Current beat anticipation from onset × flux interaction. Represents how well the fronto-striatal network is currently tracking beat events. High when onsets are clear and predictable.

2. **Motor locking** (idx 6): Current motor-auditory lock from sensorimotor coupling signal. Represents the temporo-parietal network's real-time rhythmic entrainment quality. High when dynamics-perceptual binding is strong.

Both outputs are sigmoid-bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_predictive_timing | Beat anticipation for prediction state |
| E-layer | f02_sensorimotor_coupling | Coupling for motor lock state |
| M-layer | sync_quality | Synchronization context |
| H³ (shared) | Reuses E/M tuples | Current-state features |
