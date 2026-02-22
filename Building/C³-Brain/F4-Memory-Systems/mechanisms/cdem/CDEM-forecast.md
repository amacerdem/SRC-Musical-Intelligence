# CDEM F-Layer — Forecast (3D)

**Layer**: Future Predictions (F)
**Indices**: [7:10]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:encoding_strength_fc | [0, 1] | Encoding strength prediction (2-5s ahead). Hippocampal consolidation trajectory from H20 window. Predicts whether context-dependent encoding will strengthen or weaken. Janata 2009: dMPFC parametrically tracks autobiographical salience (fMRI, N=13). |
| 8 | F1:retrieval_context_fc | [0, 1] | Context retrieval prediction (5-10s ahead). mPFC context reinstatement trajectory from H24 window. Predicts whether the current context will facilitate retrieval of stored traces. Sachs 2025: same-valence context shifts transitions 6.26s earlier (fMRI, N=39). |
| 9 | F2:mood_congruency_fc | [0, 1] | Mood congruency prediction (1-3s ahead). Congruency trend trajectory from H16 window. Predicts whether music-mood alignment will increase or decrease. Sakakibara 2025: nostalgia enhances memory vividness (EEG, N=33, Cohen's r=0.88). |

---

## Design Rationale

1. **Encoding Strength Forecast (F0)**: Predicts the trajectory of context-dependent encoding over the next 2-5 seconds. Uses the H20 consolidation window. High encoding strength prediction means the hippocampal-mPFC dialogue is actively strengthening the context-tagged memory trace. This is the "will this memory consolidate?" forecast.

2. **Retrieval Context Forecast (F1)**: Predicts context-dependent retrieval probability over a 5-10 second horizon. Uses the H24 long-term window. High retrieval context prediction means the mPFC is actively reinstating a context pattern that will facilitate memory retrieval. This is aligned with Sachs 2025's finding that same-valence emotional contexts produce brain-state shifts 6.26s earlier than different-valence transitions.

3. **Mood Congruency Forecast (F2)**: Predicts whether the music-mood alignment will strengthen or weaken over the next 1-3 seconds. Uses the H16 working memory window. This short-horizon prediction captures rapid shifts in emotional congruency — when music suddenly matches or mismatches the listener's mood. Enables anticipation of emotional memory encoding windows.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (22, 24, 19, 0) | entropy stability H24 L0 | Context stability over 36s for retrieval prediction |
| (0, 20, 18, 0) | roughness trend H20 L0 | Valence trajectory for congruency forecast |
| (4, 20, 18, 0) | sensory_pleasantness trend H20 L0 | Pleasantness trajectory for encoding forecast |
| (11, 20, 4, 0) | onset_strength max H20 L0 | Peak onset over 5s for context boundary detection |

F-layer also reuses C-layer encoding_strength and M-layer congruency_index.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:encoding_strength_fc | F4 Memory (MEAMN) | Context-dependent encoding strength modulates autobiographical memory |
| F1:retrieval_context_fc | F6 Reward (SRP) | Context reinstatement triggers hedonic response |
| F2:mood_congruency_fc | F5 Emotion | Mood-congruency trajectory feeds emotional momentum |

---

## Scientific Foundation

- **Janata 2009**: dMPFC parametrically tracks autobiographical salience of music; hub for music-memory-emotion integration (fMRI, N=13)
- **Sachs et al. 2025**: Same-valence context shifts brain-state transitions 6.26s earlier than different-valence (fMRI, N=39, z=3.6-4.32)
- **Sakakibara et al. 2025**: Nostalgia Brain-Music Interface enhances nostalgic feelings and memory vividness (EEG, N=33, Cohen's r=0.71-0.88)
- **Huron 2006**: ITPRA framework for expectancy-based affective response and anticipation dynamics (theoretical)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/cdem/forecast.py`
