# MMP F-Layer — Cognitive Present (3D)

**Layer**: Future Predictions (F)
**Indices**: [6:9]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 6 | F0:recognition_fc | [0, 1] | Recognition accuracy prediction (1-5s ahead). Based on preserved pathway trajectory over H20 (5s) window. Predicts whether melody recognition will strengthen or weaken. Scarratt et al. 2025: familiar music engages distributed memory network (fMRI, N=57). |
| 7 | F1:emotional_fc | [0, 1] | Emotional response prediction (2-10s ahead). Well-being improvement trajectory over H24 (36s) window. Predicts the therapeutic emotional benefit of continued musical exposure. Fang et al. 2017: MT reduces cognitive decline in autobiographical/episodic memory (systematic review, multiple RCTs). |
| 8 | F2:scaffold_fc | [0, 1] | Cognitive scaffolding prediction. Session-level therapeutic benefit. f09_scaffold * hippocampal_indep — sustains the scaffold signal weighted by cortical independence. Luxton et al. 2025: Level 1 evidence for cognitive stimulation therapy (SMD=0.25, p=0.003). |

---

## Design Rationale

1. **Recognition Prediction (F0)**: Forecasts whether the preserved cortical recognition pathway will strengthen or weaken over the next 1-5 seconds. Uses the familiarity trajectory over the consolidation window (H20, 5s). Clinical use: monitor in real-time whether the selected music is maintaining therapeutic engagement.

2. **Emotional Prediction (F1)**: Forecasts the upcoming emotional response over a longer therapeutic timescale (2-10s). Uses the retrieval trajectory over the episodic chunk window (H24, 36s). This predicts whether continued musical exposure will deepen emotional engagement, informing session duration decisions.

3. **Scaffold Prediction (F2)**: Forecasts the cognitive scaffolding efficacy at the session level. Combines the scaffold feature (f09) with hippocampal independence to predict sustained therapeutic benefit. High scaffold_fc means the music is successfully bridging to otherwise inaccessible cognitive resources.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 24, 1, 0) | sensory_pleasantness mean H24 L0 | Long-term pleasantness for emotional trajectory |
| (22, 24, 1, 0) | entropy mean H24 L0 | Long-term predictability for scaffold trajectory |
| (16, 20, 1, 0) | spectral_smoothness mean H20 L0 | Timbral quality for recognition trajectory |

F-layer primarily reuses R+P outputs rather than reading new H3 tuples directly.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:recognition_fc | F4 Memory (internal) | Recognition trajectory for C-layer clinical metrics |
| F1:emotional_fc | F5 Emotion | Preserved emotional response trajectory |
| F2:scaffold_fc | Clinical output | Session-level therapeutic benefit prediction |

---

## Scientific Foundation

- **Scarratt et al. 2025**: Familiar music engages distributed memory network; 4 behavioral response clusters (fMRI, N=57)
- **Fang et al. 2017**: Music therapy reduces cognitive decline in autobiographical/episodic memory, psychomotor speed, executive function (systematic mini-review, multiple RCTs)
- **Luxton et al. 2025**: Level 1 evidence — cognitive stimulation therapy improves QoL (SMD=0.25, p=0.003); Level 2: music therapy (systematic review+meta-analysis, 324 studies)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/mmp/cognitive_present.py`
