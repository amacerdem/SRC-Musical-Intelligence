# Benchmark Plan

Empirical validation of L³ semantic output against human data.

## Phase 1: Physiological Alignment (δ Group)

**Goal**: Validate that δ group predictions correlate with actual physiological measurements.

| L³ Dimension | Measurement | Dataset | Target Metric |
|-------------|-------------|---------|---------------|
| δ0 skin_conductance | SCR (electrodermal) | Music-evoked chills dataset | r > 0.3 |
| δ1 heart_rate | HR (ECG) | Continuous music listening | r > 0.3 |
| δ2 pupil_diameter | Pupilometry | Surprise/novelty paradigm | r > 0.3 |
| δ3 piloerection | Self-report + camera | Chill-inducing passages | AUC > 0.65 |

**Key references**: de Fleurian & Pearce (2021), Grewe et al. (2009), Laeng et al. (2012)

## Phase 2: Emotion Ratings (γ, ζ Groups)

**Goal**: Validate affective dimensions against continuous listener ratings.

| L³ Dimension | Paradigm | Dataset | Target Metric |
|-------------|----------|---------|---------------|
| ζ.valence | Continuous valence rating | DEAM / PMEmo | r > 0.4 |
| ζ.arousal | Continuous arousal rating | DEAM / PMEmo | r > 0.4 |
| γ.reward_intensity | Post-hoc pleasure rating | Custom | r > 0.35 |
| γ.beauty | Aesthetic judgment | Custom | r > 0.3 |

**Key references**: Russell (1980), Schubert (2004), Gabrielsson (2001)

## Phase 3: Vocabulary Validation (η Group)

**Goal**: Validate that η vocabulary terms match human free-description.

| Test | Method | Target Metric |
|------|--------|---------------|
| Term appropriateness | Forced-choice: η term vs random | Accuracy > 70% |
| Band ordering | Listeners rank intensity of terms | τ > 0.7 (Kendall) |
| Cross-cultural validity | Same test in 3+ languages | κ > 0.5 |

**Key references**: Rosch (1975), Osgood et al. (1957)

## Phase 4: Chills Prediction

**Goal**: Predict chill onset from L³ features.

| Approach | Features | Target Metric |
|----------|----------|---------------|
| Binary classification | γ.chill_probability, ε.surprise, ζ.beauty | AUC > 0.70 |
| Temporal precision | Onset within ±2 seconds | Recall > 0.5 |
| Individual differences | Per-listener chill thresholds | Improvement over baseline |

**Key references**: de Fleurian & Pearce (2021) [k=116, d=0.85], Sloboda (1991)

## Phase 5: Learning Dynamics (ε Group)

**Goal**: Validate that ε group tracks temporal learning.

| Test | Method | Target Metric |
|------|--------|---------------|
| Familiarity growth | ε.familiarity vs repeated exposure count | r > 0.5 |
| IDyOM alignment | ε.surprise vs IDyOM surprisal | r > 0.4 |
| Wundt curve | ε.wundt_position vs preference ratings | inverted-U fit R² > 0.3 |
| Compression progress | ε.compression_progress vs learning rate | r > 0.3 |

**Key references**: Pearce (2005), Berlyne (1971), Schmidhuber (2009)

## Phase 6: Narrative Coherence (θ Group)

**Goal**: Validate that θ narrative structure produces coherent descriptions.

| Test | Method | Target Metric |
|------|--------|---------------|
| Sentence quality | Human raters judge generated sentences | Mean > 3.5/5 |
| Temporal coherence | Consecutive sentences follow musical form | Agreement > 60% |
| Subject accuracy | Dominant subject matches listener focus | Accuracy > 50% |

## Timeline

| Phase | Dependency | Priority |
|-------|-----------|----------|
| Phase 1 | Requires physiological recording setup | P1 |
| Phase 2 | DEAM/PMEmo datasets available | P1 |
| Phase 3 | Requires listener panel | P2 |
| Phase 4 | Phase 1 data + chill annotations | P2 |
| Phase 5 | IDyOM installation + repeated-exposure study | P3 |
| Phase 6 | θ group fully implemented | P3 |

---

**Parent**: [00-INDEX.md](00-INDEX.md)
