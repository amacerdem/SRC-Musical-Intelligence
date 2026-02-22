"""F5 beliefs — 14 total (4 Core + 8 Appraisal + 2 Anticipation).

VMM (6):   perceived_happy(C), perceived_sad(C), mode_detection(A),
           emotion_certainty(A), happy_pathway(A), sad_pathway(A)
AAC (4):   emotional_arousal(C), chills_intensity(A), ans_dominance(A),
           driving_signal(N)
NEMAC (4): nostalgia_affect(C), self_referential_nostalgia(A),
           wellbeing_enhancement(A), nostalgia_peak_pred(N)
"""
from .vmm import (
    PerceivedHappy,
    PerceivedSad,
    ModeDetection,
    EmotionCertainty,
    HappyPathway,
    SadPathway,
)
from .aac import (
    EmotionalArousal,
    ChillsIntensity,
    AnsDominance,
    DrivingSignal,
)
from .nemac import (
    NostalgiaAffect,
    SelfReferentialNostalgia,
    WellbeingEnhancement,
    NostalgiaPeakPred,
)

__all__ = [
    "PerceivedHappy", "PerceivedSad", "ModeDetection",
    "EmotionCertainty", "HappyPathway", "SadPathway",
    "EmotionalArousal", "ChillsIntensity", "AnsDominance", "DrivingSignal",
    "NostalgiaAffect", "SelfReferentialNostalgia",
    "WellbeingEnhancement", "NostalgiaPeakPred",
]
