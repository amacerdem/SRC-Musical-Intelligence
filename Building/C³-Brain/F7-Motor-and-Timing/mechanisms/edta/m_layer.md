# EDTA — Temporal Integration

**Model**: Expertise-Dependent Tempo Accuracy
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: β
**Layer**: M — Temporal Integration
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 3 | tempo_stability | Temporal stability of estimated tempo. Low energy variance = high stability. Computed as 1 − σ(energy_velocity) at H11 (500ms). When energy dynamics are smooth and non-accelerating, tempo estimation is stable. Maps to putamen beat-timing circuit (Grahn & Brett 2007: L putamen Z=5.67). |
| 4 | domain_specificity | Domain match strength. How well current tempo matches trained range. Combines f03 expertise effect with bar-level energy periodicity at H16. High when the current tempo falls within the trained range (120-139 BPM for DJs, 100-139 BPM for percussionists) AND motor stability is maintained. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 8 | 11 | M1 (mean) | L0 | Mean loudness over meter grouping |
| 1 | 8 | 11 | M14 (periodicity) | L0 | Tempo periodicity estimate |
| 2 | 22 | 11 | M8 (velocity) | L0 | Tempo acceleration |
| 3 | 22 | 11 | M3 (std) | L0 | Tempo variability (precision) |
| 4 | 9 | 11 | M1 (mean) | L0 | Mean brightness at meter level |

---

## Computation

The M-layer integrates E-layer signals into unified tempo metrics:

1. **Tempo stability** (idx 3): Inverted energy velocity — when energy dynamics are slow and stable, tempo estimation is reliable. High energy velocity (rapid tempo changes) reduces stability. Maps to the putamen's beat-based timing mechanism.

2. **Domain specificity** (idx 4): Product of expertise effect (f03) and bar-level energy periodicity. When the expertise advantage is activated AND bar-level patterns are periodic, the current tempo strongly matches the trained domain. Hoddinott & Grahn 2024: C-Score model in SMA/putamen encodes beat strength continuously.

Both outputs are bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01, f02, f03 | Accuracy and expertise for stability/specificity |
| R³ [8] | loudness | Periodicity for tempo estimate |
| R³ [9] | spectral_centroid | Mean brightness at meter level |
| R³ [22] | energy_change | Velocity and variability for tempo dynamics |
| H³ | 5 tuples (see above) | Meter-level features at H11 (500ms) |
