# EDTA — Extraction

**Model**: Expertise-Dependent Tempo Accuracy
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: β
**Layer**: E — Extraction
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_beat_accuracy | Beat onset detection accuracy. Precision of beat induction from spectral flux × onset strength at H6 (200ms). Measures how precisely the system detects beat boundaries for tempo estimation. Foster 2021: DJs achieve 3.10% error at 120-139 BPM vs. untrained 7.91%. Formula: σ(0.50 × flux_val × onset_val). |
| 1 | f02_tempo_precision | Tempo estimation precision. Inverse of timing variance in BPM range. Computed from loudness periodicity × (1 − energy_std) at H11 (500ms). Regular, low-variance intensity patterns enable precise tempo estimation. Vigl 2024 (N=403): quadratic peak at ~120 BPM, χ²(1)=152.57. Formula: σ(0.45 × loud_periodicity × (1 − energy_std)). |
| 2 | f03_expertise_effect | Domain-specific expertise effect (d=0.54). Modulates accuracy in trained BPM ranges. Combines f01 beat accuracy × f02 tempo precision × motor stability at H16. Foster 2021: DJs 120-139 BPM, percussionists 100-139 BPM — advantage does NOT transfer outside trained range. Formula: σ(0.54 × f01 × f02 × motor_stability). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 6 | M0 (value) | L0 | Spectral flux — current onset strength |
| 1 | 10 | 6 | M14 (periodicity) | L0 | Beat regularity at onset level |
| 2 | 11 | 6 | M0 (value) | L0 | Onset strength — current beat boundary |
| 3 | 11 | 6 | M17 (peaks) | L0 | Beat count per window |
| 4 | 7 | 6 | M4 (max) | L0 | Peak beat intensity |

---

## Computation

The E-layer extracts three levels of tempo accuracy:

1. **Beat accuracy** (f01): Onset detection precision at beat level (H6). Sharp, well-timed onsets produce high f01. Maps to Heschl's gyrus / STG beat induction.

2. **Tempo precision** (f02): Periodicity-based tempo estimation at the psychological present (H11 = 500ms, Poeppel). When loudness is periodic and energy variance is low, tempo estimation is precise. Maps to putamen / SMA metric extraction.

3. **Expertise effect** (f03): Domain-specific accuracy boost. The d = 0.54 coefficient modulates when both beat detection and tempo estimation are accurate AND motor stability is high. Foster 2021 demonstrates this is domain-specific: DJs' advantage at 120-139 BPM does not transfer to 80-99 BPM.

All outputs are sigmoid-bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [7] | amplitude | Peak beat intensity |
| R³ [10] | spectral_flux | Onset detection for beat boundary |
| R³ [11] | onset_strength | Beat event marking precision |
| H³ | 5 tuples (see above) | Beat-level features at H6 (200ms) |
