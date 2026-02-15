"""Neurochemical: Serotonin (5HT)

Temporal discount rate and mood baseline. Sets the temporal horizon for
reward evaluation: high 5HT promotes patience and long-term reward
integration, while low 5HT promotes impulsivity and preference for
immediate reward. In music cognition, 5HT modulates how far ahead the
prediction system looks when anticipating upcoming events, influencing
sensitivity to large-scale structure versus moment-to-moment changes.

Channel Index: 3
Key References: Doya 2002, Crockett 2009
"""

CHANNEL: int = 3
NAME: str = "5HT"
BASELINE: float = 0.5

# Reference values from literature
REFERENCE_VALUES = {
    "normal_baseline": (0.50, "resting serotonergic tone"),
    "elevated_calm_patient": (0.70, "enhanced patience, long-horizon reward sensitivity"),
    "depleted_anxious_impulsive": (0.30, "tryptophan depletion, short-horizon bias"),
}

# Interactions
INTERACTIONS = {
    "DA": "5HT2C on VTA inhibits DA release; 5HT1B on NAcc facilitates DA; dual modulation",
    "NE": "Inverse relationship: high NE arousal states often coincide with low 5HT",
    "OPI": "Mood baseline modulates hedonic capacity: low 5HT blunts opioid-mediated pleasure",
}
