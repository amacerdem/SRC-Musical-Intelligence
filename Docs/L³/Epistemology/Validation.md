# L³ Epistemology — Validation

**Level**: 4 (δ)
**Question**: HOW to test empirically?
**Audience**: Experimenters, empirical researchers
**Version**: 2.1.0
**Updated**: 2026-02-13

---

## Overview

The Validation group exists for one reason: to make L³ **falsifiable**. Every semantic interpretation (β, γ) must generate predictions that can be tested against real human data. Without δ, L³ would be a descriptive framework. With δ, it becomes a scientific one.

Delta produces 12 dimensions: 4 physiological predictions, 3 neural predictions, 2 behavioral predictions, and 3 temporal constraints.

---

## Design Principle

**Every L³ output should generate a testable prediction.** δ operationalizes this by mapping semantic dimensions to measurable physiological, neural, and behavioral signals. If the Brain says a listener is experiencing intense reward, δ predicts elevated skin conductance. If the Brain says anticipation is high, δ predicts caudate BOLD signal increase. These predictions can be compared against empirical data to validate or falsify the model.

---

## Physiological Predictions (4D)

| Local | Name | Measure | Source Dimensions | Citation |
|:-----:|------|---------|------------------|----------|
| δ0 | `skin_conductance` | Expected SCR signal | Arousal, reward intensity | de Fleurian & Pearce 2021 |
| δ1 | `heart_rate` | Expected HR change | Arousal, valence | Thayer 2009 |
| δ2 | `pupil_diameter` | Expected pupil dilation | Arousal * \|PE\| | Laeng et al. 2012 |
| δ3 | `piloerection` | Expected goosebump probability | Chill signature | Sloboda 1991 |

**Skin conductance response (SCR)** is the most reliable autonomic correlate of musical emotion. de Fleurian & Pearce (2021) found a meta-analytic effect size of d = 0.85 for SCR during musical chills.

**Heart rate (HR)** decelerates during high-attention musical moments and accelerates during high-arousal passages (Thayer 2009). δ1 predicts directional HR change.

**Pupil dilation** indexes cognitive load and emotional arousal. Laeng et al. (2012) showed that pupil diameter increases during unexpected musical events — a signal that combines arousal and prediction error.

**Piloerection** (goosebumps) is the gold standard for musical chills but is difficult to measure continuously. δ3 predicts its probability from the chill signature in γ.

---

## Neural Predictions (3D)

| Local | Name | Measure | Source Dimensions | Citation |
|:-----:|------|---------|------------------|----------|
| δ4 | `fmri_nacc_bold` | Expected NAcc BOLD signal | NAcc activation (β0) | Salimpoor et al. 2011 |
| δ5 | `fmri_caudate_bold` | Expected Caudate BOLD signal | Caudate activation (β1) | Salimpoor et al. 2011 |
| δ6 | `eeg_frontal_alpha` | Expected alpha suppression | 1 - pleasure | Sammler et al. 2007 |

These dimensions translate β's brain region activations into predictions about specific neuroimaging signals:

- **fMRI BOLD**: NAcc and Caudate BOLD signals are the primary fMRI markers of musical reward (Salimpoor et al. 2011, 2013). δ4-δ5 predict their time courses.
- **EEG alpha**: Frontal alpha power decreases during pleasurable music listening (Sammler et al. 2007). δ6 predicts alpha suppression as the inverse of pleasure.

---

## Behavioral Predictions (2D)

| Local | Name | Measure | Paradigm | Citation |
|:-----:|------|---------|----------|----------|
| δ7 | `willingness_to_pay` | Auction bid amount | Salimpoor 2013 auction | Salimpoor et al. 2013 |
| δ8 | `button_press_rating` | Continuous pleasure rating | Real-time dial | Schubert 2004 |

**Willingness-to-pay (WTP)**: Salimpoor et al. (2013) showed that NAcc activation during music preview predicted how much participants would bid in a subsequent auction. δ7 predicts WTP from reward intensity.

**Continuous rating**: Schubert (2004) pioneered real-time emotional rating during music. δ8 predicts the continuous pleasure trajectory that a listener would report via button press.

---

## Temporal Constraints (3D)

| Local | Name | Constraint | Prediction | Citation |
|:-----:|------|-----------|------------|----------|
| δ9 | `wanting_leads_liking` | σ(da_caudate - da_nacc) | Caudate peak before NAcc peak | Salimpoor et al. 2011 |
| δ10 | `rpe_latency` | \|prediction_error\| | RPE occurs at expectation violation | Fong et al. 2020 |
| δ11 | `refractory_state` | 1 - chills_intensity | Post-chill suppression period | Grewe et al. 2009 |

These dimensions encode **temporal ordering predictions** that constrain the model's dynamics:

- **Wanting leads liking** (δ9): Caudate (anticipation) must peak before NAcc (consummation). If the model ever shows the reverse, something is wrong.
- **RPE latency** (δ10): Reward prediction error should coincide with moments of expectation violation, not random time points.
- **Refractory state** (δ11): After a chill, there should be a suppression period where another chill is unlikely. This constrains chill spacing.

---

## Validation Strategy

1. **Collect**: Record physiological (SCR, HR, pupil, goosebump), neural (fMRI, EEG), and behavioral (WTP, rating) data during music listening.
2. **Predict**: Run the same music through MI's pipeline to generate δ predictions.
3. **Compare**: Correlate δ predictions with empirical measurements.
4. **Falsify**: If correlations are at chance, the upstream semantic interpretations are wrong.

This makes δ the scientific backbone of L³. It converts interpretive claims into quantitative hypotheses.

---

## Key Citations

- Salimpoor, V.N. et al. (2011). Anatomically distinct dopamine release during anticipation and experience of peak emotion to music. *Nature Neuroscience*, 14(2), 257-262.
- Salimpoor, V.N. et al. (2013). Interactions between the nucleus accumbens and auditory cortices predict music reward value. *Science*, 340(6129), 216-219.
- de Fleurian, R. & Pearce, M.T. (2021). Chills in music: A systematic review. *Psychological Bulletin*, 147(9), 890-920.
- Thayer, J.F. et al. (2009). Heart rate variability, prefrontal neural function, and cognitive performance. *Annals of Behavioral Medicine*, 37(2), 141-153.
- Laeng, B. et al. (2012). Pupil size and music. *Psychophysiology*, 49(7), 1070-1077.
- Schubert, E. (2004). Modeling perceived emotion with continuous musical features. *Music Perception*, 21(4), 561-585.
- Sammler, D. et al. (2007). Music and emotion: electrophysiological correlates. *Brain Research*, 1169, 132-143.
- Grewe, O., Kopiez, R., & Altenmuller, E. (2009). Chills as an indicator of individual emotional peaks. *ANYAS*, 1169, 351-354.

---

**Parent**: [00-INDEX.md](00-INDEX.md)
**See also**: [Groups/Independent/Delta.md](../Groups/Independent/Delta.md) for implementation details | [Registry/DimensionCatalog.md](../Registry/DimensionCatalog.md) for dimension metadata
