"""Polarity classification — value and delta thresholds for 0-1 beliefs/dimensions.

Migrated from the original flat interpreter.py.
"""

from __future__ import annotations


def classify_value(value: float) -> str:
    """Classify a 0-1 value into polarity band."""
    if value >= 0.75:
        return "very_high"
    if value >= 0.6:
        return "high"
    if value >= 0.4:
        return "moderate"
    if value >= 0.25:
        return "low"
    return "very_low"


def classify_delta(current: float, previous: float | None) -> str | None:
    """Classify change direction between two values."""
    if previous is None:
        return None
    delta = current - previous
    if delta > 0.15:
        return "rising_fast"
    if delta > 0.08:
        return "rising"
    if delta < -0.15:
        return "falling_fast"
    if delta < -0.08:
        return "falling"
    return None


def polarity_label(value: float, language: str = "en") -> str:
    """Human-readable polarity label."""
    pol = classify_value(value)
    labels = {
        "en": {
            "very_high": "very high",
            "high": "high",
            "moderate": "moderate",
            "low": "low",
            "very_low": "very low",
        },
        "tr": {
            "very_high": "çok yüksek",
            "high": "yüksek",
            "moderate": "orta",
            "low": "düşük",
            "very_low": "çok düşük",
        },
    }
    return labels.get(language, labels["en"]).get(pol, pol)


def delta_label(current: float, previous: float | None, language: str = "en") -> str | None:
    """Human-readable delta label."""
    d = classify_delta(current, previous)
    if d is None:
        return None
    labels = {
        "en": {
            "rising_fast": "rising sharply",
            "rising": "rising",
            "falling_fast": "falling sharply",
            "falling": "falling",
        },
        "tr": {
            "rising_fast": "hızla yükseliyor",
            "rising": "yükseliyor",
            "falling_fast": "hızla düşüyor",
            "falling": "düşüyor",
        },
    }
    return labels.get(language, labels["en"]).get(d, d)
