# TMRM — Extraction

**Model**: Tempo Memory Reproduction Method
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: E — Extraction
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_adjusting_advantage | Sensory support advantage (d=2.76 Levitin & Cook 1996; replicated at d≈0.54 by Vigl 2024 N=403). Adjusting (tempo slider) outperforms tapping for tempo accuracy. Computed from loudness peak × spectral flux periodicity at H6/H11. The sensory pathway via SMA + auditory cortex enables continuous perceptual comparison against internal template. Formula: σ(0.35 × loud_peak × flux_period). |
| 1 | f02_optimal_tempo | 120 BPM quadratic optimum (Vigl 2024: χ²(1)=152.57, p<.001; Drake & Botte 1993: Weber fraction minimum at 500ms IOI). Internal tempo reference at 120 BPM. Computed from loudness periodicity × spectral flux peaks at H11/H6. Peak accuracy when tempo aligns with the 500ms (H11) psychological present window. Formula: σ(0.30 × period_loud × period_flux). |
| 2 | f03_expertise_accuracy | Musical expertise effect (Vigl 2024: r=.09, p=.047; Dalla Bella 2024: d=1.8 PMI model). Expertise enhances reproduction precision as a continuous variable. Combines energy smoothness at bar level with f01 × f02 interaction. Stronger for tapping than adjusting (method × expertise: r=.04, p=.001). Formula: σ(0.30 × smooth_energy × f01 × f02). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 8 | 6 | M4 (max) | L0 | Beat peak loudness |
| 1 | 10 | 6 | M17 (peaks) | L0 | Beat onset count per window |
| 2 | 11 | 6 | M4 (max) | L0 | Strongest onset in beat window |
| 3 | 10 | 11 | M14 (periodicity) | L0 | Beat periodicity (tempo proxy) |
| 4 | 8 | 11 | M14 (periodicity) | L0 | Tempo regularity at 500ms |

---

## Computation

The E-layer extracts three levels of tempo memory reproduction accuracy:

1. **Adjusting advantage** (f01): Sensory pathway superiority from beat peak loudness and spectral flux periodicity. When beats are loud and periodic, the sensory pathway (SMA + auditory cortex) reliably matches perceived tempo against the internal template. Maps to Heschl's gyrus / STG beat induction.

2. **Optimal tempo** (f02): 120 BPM reference detection from loudness periodicity and beat count. When periodicity aligns with the ~500ms IOI window, tempo estimation peaks. Maps to the putamen/SMA beat-timing circuit.

3. **Expertise accuracy** (f03): Continuous expertise modulation from energy smoothness × sensory × tempo signals. When the adjusting pathway is strong AND tempo is near optimal AND energy dynamics are smooth, expertise further enhances accuracy.

All outputs are sigmoid-bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [8] | loudness | Peak loudness and periodicity for tempo |
| R³ [10] | spectral_flux | Beat periodicity and onset counting |
| R³ [11] | onset_strength | Strongest onset for beat precision |
| H³ | 5 tuples (see above) | Beat and motor-level features at H6/H11 |
