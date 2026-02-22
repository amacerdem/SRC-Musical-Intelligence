"""MIAA beliefs — Musical Imagery Auditory Activation.

Two beliefs grounded in MIAA mechanism output:

    timbral_character    (Core, τ=0.5)   "I recognize this timbre"
    imagery_recognition  (Anticipation)   "Recognition probability at gap resolution"
"""
from .imagery_recognition import ImageryRecognition
from .timbral_character import TimbralCharacter

__all__ = ["TimbralCharacter", "ImageryRecognition"]
