# TAR T+I-Layer — Temporal Integration (6D)

**Layer**: Therapeutic Targets (T) + Intervention Parameters (I)
**Indices**: [1:7]
**Scope**: internal
**Activation**: sigmoid | clamp [0, 1]

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 1 | T0:arousal_mod_tgt | [0, 1] | Arousal modulation potential. arousal_mod = sigma(0.4 * tempo_proxy + 0.3 * energy + 0.3 * mood_fast). What arousal change this music provides via tempo/energy to ANS entrainment pathway. Low = calming (anxiolytic), High = activating (antidepressant). Thoma 2013: music reduces stress response via autonomic pathway. |
| 2 | T1:valence_mod_tgt | [0, 1] | Valence modulation potential. valence_mod = sigma(0.4 * consonance + 0.3 * (valence + 1)/2 + 0.3 * mood_slow). What valence shift this music provides via consonance/mode to reward circuit. High = positive valence induction for depression. Koelsch 2014: consonance drives reward pathway activation. |
| 3 | T2:anxiety_reduction | [0, 1] | Anxiolytic potential. anxiety_reduction = sigma(0.3 * tempo_factor + 0.3 * consonance + 0.2 * warmth + 0.2 * (1.0 - arousal)). Low tempo x high consonance x soft dynamics x warmth targets amygdala downregulation and PNS activation. tempo_factor = clamp(1.0 - tempo_proxy, 0, 1). Bradt & Dileo 2014: music anxiety interventions, d ~ 0.5-0.8. |
| 4 | T3:depression_improv | [0, 1] | Antidepressant potential. depression_improvement = sigma(0.3 * (valence + 1)/2 + 0.3 * energy_factor + 0.4 * c0p_mean). Positive valence x moderate energy x reward activation targets striatal DA upregulation. energy_factor = exp(-((tempo_proxy - 0.5) * 3.0)^2). Kheirkhah 2025: music therapy for depression, d = 0.88. |
| 5 | I0:rec_tempo_norm | [0, 1] | Recommended tempo (normalized). rec_tempo = sigma(0.5 * (1.0 - anxiety_reduction) + 0.5 * depression_improvement). 0.0=60 BPM (anxiolytic), 0.5=90 BPM (moderate), 1.0=120 BPM (activating). Adaptive recommendation based on current therapeutic need — high anxiety shifts toward slow tempo, high depression shifts toward moderate-fast tempo. |
| 6 | I1:rec_consonance | [0, 1] | Recommended consonance level. rec_consonance = clamp(0.7 + 0.3 * mood_stability, 0, 1). Typically >= 0.7 for all therapeutic targets — consonance is universally therapeutic. Higher mood stability allows lower minimum consonance. Koelsch 2014: consonance → reward → therapeutic benefit across conditions. |

---

## Design Rationale

1. **Arousal Modulation (T0)**: Estimates what arousal change the current music provides. Combines tempo proxy (primary arousal driver), energy level (amplitude + onset strength), and fast mood dynamics from H3. This maps the acoustic properties to the autonomic nervous system pathway — slow/soft music activates PNS (calming) while fast/loud music activates SNS (activating).

2. **Valence Modulation (T1)**: Estimates what valence shift the current music provides. Combines consonance (harmonic quality), explicit valence (pleasantness - roughness), and slow mood dynamics from H3. This maps acoustic properties to the reward circuit — consonant, pleasant music with positive mood context drives hedonic activation.

3. **Anxiety Reduction (T2)**: The condition-specific anxiolytic potential. Uses four factors: slow tempo (low tempo_proxy inverted), high consonance, timbral warmth, and soft dynamics (low arousal). All four contribute to amygdala downregulation and parasympathetic activation. The 0.3/0.3/0.2/0.2 weighting reflects tempo and consonance as primary anxiolytic drivers.

4. **Depression Improvement (T3)**: The condition-specific antidepressant potential. Uses positive valence, moderate energy (Gaussian peak at tempo_proxy=0.5), and reward pathway activation (cognitive-projection mean). The Gaussian energy factor ensures that neither too-slow (sedating) nor too-fast (agitating) tempi are optimal — moderate activation is the antidepressant target.

5. **Recommended Tempo (I0)**: An adaptive tempo recommendation. Balances anxiety reduction (favoring slow tempo) against depression improvement (favoring moderate tempo). The recommendation shifts dynamically based on the current therapeutic need.

6. **Recommended Consonance (I1)**: A consonance floor recommendation. Minimum 0.7 for all therapeutic conditions, rising to 1.0 with high mood stability. Consonance is universally beneficial in therapeutic contexts — dissonance increases stress and anxiety.

---

## H3 Dependencies (T+I-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 6, 0, 2) | sensory_pleasantness value H6 L2 | Fast mood state for arousal modulation |
| (4, 16, 0, 2) | sensory_pleasantness value H16 L2 | Slow mood state for valence modulation |
| (4, 6, 8, 0) | sensory_pleasantness velocity H6 L0 | Affect velocity for mood fast dynamics |
| (4, 16, 2, 0) | sensory_pleasantness std H16 L0 | Mood stability for consonance recommendation |
| (0, 12, 18, 0) | roughness trend H12 L0 | Dissonance trajectory for anxiety tracking |
| (0, 15, 18, 0) | roughness trend H15 L0 | Sustained dissonance for peak context |
| (8, 6, 8, 0) | velocity_A velocity H6 L0 | Tempo proxy for arousal target |
| (8, 12, 8, 0) | velocity_A velocity H12 L0 | Tempo buildup for therapeutic trajectory |
| (8, 12, 18, 0) | velocity_A trend H12 L0 | Tempo trend for buildup tracking |
| (10, 6, 0, 2) | loudness value H6 L2 | Current arousal for dynamics |
| (4, 11, 1, 0) | sensory_pleasantness mean H11 L0 | Cognitive-projection for depression signal |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | T1/T2: consonance for valence and anxiety |
| [4] | sensory_pleasantness | T1: hedonic quality for valence modulation |
| [5] | harmonicity | T1/I1: harmonic purity for consonance computation |
| [7] | amplitude | T0: energy level for arousal modulation |
| [8] | velocity_A | T0/I0: rate of change as tempo proxy |
| [10] | loudness | T0/T2: overall level for arousal/dynamics |
| [11] | onset_strength | T0: rhythmic events for energy computation |
| [16] | warmth | T2: comfort signal for anxiety reduction |
| [21] | spectral_flux | T2: predictability for stress pathway |
| [33:41] | x_l4l5 | T3: derivatives-consonance therapeutic engagement |

---

## Scientific Foundation

- **Thoma et al. 2013**: Music reduces stress response via cortisol reduction (RCT, N=60, PLOS ONE)
- **Koelsch 2014**: Brain correlates of music-evoked emotions — consonance drives reward pathway (review, Nature Reviews Neuroscience, 15(3), 170-180)
- **Bradt & Dileo 2014**: Music interventions for anxiety — meta-analysis of 26 trials, d ~ 0.5-0.8 (Cochrane Database)
- **Kheirkhah et al. 2025**: Music + ketamine + mindfulness for treatment-resistant depression (RCT, d=0.88)
- **Bowling 2023**: 4 biological principles for therapeutic music: tonality, rhythm, reward, sociality (review, Translational Psychiatry, 13, 374)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/tar/temporal_integration.py`
