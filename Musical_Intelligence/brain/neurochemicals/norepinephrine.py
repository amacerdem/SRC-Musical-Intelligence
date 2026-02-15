"""Neurochemical: Norepinephrine (NE)

Exploration-exploitation balance mediated by the locus coeruleus (LC). Phasic
NE bursts signal unexpected events, driving attention reorienting toward
surprising musical features. Tonic NE levels set the exploration-exploitation
tradeoff: high tonic NE promotes exploration (scanning for new patterns),
low tonic NE promotes exploitation (deepening engagement with current stream).
In music: surprise triggers NE burst, which enhances downstream processing
of the unexpected event.

Channel Index: 1
Key References: Doya 2002, Aston-Jones & Cohen 2005
"""

CHANNEL: int = 1
NAME: str = "NE"
BASELINE: float = 0.5

# Reference values from literature
REFERENCE_VALUES = {
    "resting_baseline": (0.50, "tonic baseline level"),
    "unexpected_event": (0.75, "phasic burst to surprising musical event"),
    "familiar_predictable": (0.35, "low tonic during predictable sequences"),
}

# Interactions
INTERACTIONS = {
    "DA": "NE phasic burst enhances DA reward prediction error signal",
    "5HT": "Inverse relationship: high NE arousal often coincides with low 5HT",
    "OPI": "Arousal modulates hedonic response: NE amplifies OPI-mediated pleasure",
}
