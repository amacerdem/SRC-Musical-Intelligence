"""Published pharmacological targets from the literature.

These are the empirical findings that MI's neurochemical system must reproduce.
Each target specifies the drug, its mechanism, and the expected effect on
musical experience measures.

Sources:
    - Ferreri et al. (2019) Dopamine modulates the reward experiences elicited by music. PNAS.
    - Mallik et al. (2017) Anhedonia to music and mu-opioids. Neuropsychopharmacology.
    - Laeng et al. (2021) Opioid antagonism and emotional responses to music.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class PharmTarget:
    """A single pharmacological validation target."""
    study: str
    year: int
    drug: str
    mechanism: str           # e.g. "DA agonist", "OPI antagonist"
    mi_channel: str          # MI neurochemical channel: "DA", "NE", "OPI", "5HT"
    mi_gain: float           # How to modify the gain (e.g. 1.5 for enhancement)
    expected_effect: str     # e.g. "increase", "decrease"
    target_measure: str      # What MI output to measure
    effect_size_d: float     # Published Cohen's d (0 if not reported)
    n_subjects: int
    journal: str
    notes: str = ""


# ── Ferreri et al. 2019 (PNAS) — Dopamine & Musical Reward ──

FERRERI_LEVODOPA = PharmTarget(
    study="Ferreri et al.",
    year=2019,
    drug="Levodopa",
    mechanism="DA precursor → enhanced DA transmission",
    mi_channel="DA",
    mi_gain=1.5,
    expected_effect="increase",
    target_measure="reward",
    effect_size_d=0.84,
    n_subjects=27,
    journal="PNAS",
    notes="Levodopa increased pleasure and motivation for music. "
          "Participants reported more chills, higher pleasure ratings.",
)

FERRERI_RISPERIDONE = PharmTarget(
    study="Ferreri et al.",
    year=2019,
    drug="Risperidone",
    mechanism="D2 antagonist → reduced DA transmission",
    mi_channel="DA",
    mi_gain=0.3,
    expected_effect="decrease",
    target_measure="reward",
    effect_size_d=-0.67,
    n_subjects=27,
    journal="PNAS",
    notes="Risperidone reduced musical pleasure and hedonic responses. "
          "Also reduced autonomic correlates (skin conductance).",
)

FERRERI_PLACEBO = PharmTarget(
    study="Ferreri et al.",
    year=2019,
    drug="Placebo",
    mechanism="No pharmacological effect",
    mi_channel="DA",
    mi_gain=1.0,
    expected_effect="baseline",
    target_measure="reward",
    effect_size_d=0.0,
    n_subjects=27,
    journal="PNAS",
    notes="Control condition. Normal reward processing.",
)


# ── Mallik et al. 2017 (Neuropsychopharmacology) — Opioids & Music Emotion ──

MALLIK_NALTREXONE = PharmTarget(
    study="Mallik et al.",
    year=2017,
    drug="Naltrexone",
    mechanism="Non-selective opioid antagonist (mu, delta, kappa)",
    mi_channel="OPI",
    mi_gain=0.1,
    expected_effect="decrease",
    target_measure="emotion",
    effect_size_d=-0.53,
    n_subjects=15,
    journal="Neuropsychopharmacology",
    notes="50mg naltrexone reduced pleasure from both happy and sad music. "
          "Participants reported less emotional engagement and fewer chills.",
)

MALLIK_PLACEBO = PharmTarget(
    study="Mallik et al.",
    year=2017,
    drug="Placebo",
    mechanism="No pharmacological effect",
    mi_channel="OPI",
    mi_gain=1.0,
    expected_effect="baseline",
    target_measure="emotion",
    effect_size_d=0.0,
    n_subjects=15,
    journal="Neuropsychopharmacology",
    notes="Control condition. Normal emotional processing.",
)


# ── Laeng et al. 2021 — Opioids & Arousal/Valence ──

LAENG_NALTREXONE = PharmTarget(
    study="Laeng et al.",
    year=2021,
    drug="Naltrexone",
    mechanism="Non-selective opioid antagonist",
    mi_channel="OPI",
    mi_gain=0.1,
    expected_effect="decrease",
    target_measure="arousal",
    effect_size_d=-0.45,
    n_subjects=30,
    journal="Frontiers in Psychology",
    notes="Naltrexone reduced physiological arousal (pupil dilation) to music. "
          "Valence ratings were relatively preserved, suggesting dissociation.",
)

LAENG_VALENCE_PRESERVED = PharmTarget(
    study="Laeng et al.",
    year=2021,
    drug="Naltrexone",
    mechanism="Non-selective opioid antagonist",
    mi_channel="OPI",
    mi_gain=0.1,
    expected_effect="preserved",
    target_measure="valence",
    effect_size_d=0.05,
    n_subjects=30,
    journal="Frontiers in Psychology",
    notes="Valence was preserved under naltrexone. The drug selectively "
          "affected arousal/bodily responses but not cognitive valence judgments.",
)

LAENG_PLACEBO = PharmTarget(
    study="Laeng et al.",
    year=2021,
    drug="Placebo",
    mechanism="No pharmacological effect",
    mi_channel="OPI",
    mi_gain=1.0,
    expected_effect="baseline",
    target_measure="arousal",
    effect_size_d=0.0,
    n_subjects=30,
    journal="Frontiers in Psychology",
    notes="Control condition.",
)


# ── Grouped targets ──

FERRERI_TARGETS: List[PharmTarget] = [
    FERRERI_LEVODOPA, FERRERI_RISPERIDONE, FERRERI_PLACEBO,
]

MALLIK_TARGETS: List[PharmTarget] = [
    MALLIK_NALTREXONE, MALLIK_PLACEBO,
]

LAENG_TARGETS: List[PharmTarget] = [
    LAENG_NALTREXONE, LAENG_VALENCE_PRESERVED, LAENG_PLACEBO,
]

ALL_TARGETS: List[PharmTarget] = FERRERI_TARGETS + MALLIK_TARGETS + LAENG_TARGETS


# ── Target measures mapped to MI output fields ──

MEASURE_TO_MI_OUTPUT: Dict[str, str] = {
    "reward": "reward",              # ExperimentResult.reward mean
    "emotion": "psi.emotion",        # Ψ³ emotion domain mean
    "arousal": "psi.affect",         # Ψ³ affect[1] (arousal dimension)
    "valence": "psi.affect",         # Ψ³ affect[0] (valence dimension)
}
