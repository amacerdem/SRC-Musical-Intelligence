"""Observation Dispatcher — level-gated observation type selection.

Based on M³-LOGOS tier_rules.md level gates:
  L2+: mood_landscape
  L3+: daily_reflection
  L5+: pattern_discovery, music_recommendation
  L7+: predictive_insight, therapeutic_observation
  L9+: musical_counseling, cross_m3_insight
  L11+: meta_awareness
"""

from __future__ import annotations

from typing import Any

# ── Level Gates ─────────────────────────────────────────────────

_OBSERVATION_TYPES: list[dict[str, Any]] = [
    {
        "type": "mood_landscape",
        "min_level": 2,
        "label_en": "Mood Landscape",
        "label_tr": "Ruh Hali Manzarası",
        "desc_en": "How your current listening is coloring your emotional state.",
        "desc_tr": "Mevcut dinlemenin duygusal durumunu nasıl renklendirdiği.",
        "requires": ["dimensions_6d", "neurochemicals"],
    },
    {
        "type": "daily_reflection",
        "min_level": 3,
        "label_en": "Daily Reflection",
        "label_tr": "Günlük Yansıma",
        "desc_en": "How today's listening patterns compare to your recent history.",
        "desc_tr": "Bugünkü dinleme kalıplarının yakın geçmişinle nasıl karşılaştığı.",
        "requires": ["dimensions_6d", "previous_6d"],
    },
    {
        "type": "pattern_discovery",
        "min_level": 5,
        "label_en": "Pattern Discovery",
        "label_tr": "Kalıp Keşfi",
        "desc_en": "Emerging patterns in your musical preferences and neural responses.",
        "desc_tr": "Müzikal tercihlerinde ve nöral tepkilerinde ortaya çıkan kalıplar.",
        "requires": ["dimensions_6d", "functions", "beliefs"],
    },
    {
        "type": "music_recommendation",
        "min_level": 5,
        "label_en": "Music Recommendation",
        "label_tr": "Müzik Önerisi",
        "desc_en": "What kind of music your brain might be craving based on current state.",
        "desc_tr": "Mevcut durumuna göre beyninin ne tür müziğe hasret duyabileceği.",
        "requires": ["dimensions_6d", "neurochemicals", "genes"],
    },
    {
        "type": "predictive_insight",
        "min_level": 7,
        "label_en": "Predictive Insight",
        "label_tr": "Tahmine Dayalı İçgörü",
        "desc_en": "What your prediction engine reveals about your musical expertise and expectations.",
        "desc_tr": "Tahmin motorunun müzikal uzmanlığın ve beklentilerin hakkında ortaya koyduğu.",
        "requires": ["functions", "beliefs"],
    },
    {
        "type": "therapeutic_observation",
        "min_level": 7,
        "label_en": "Therapeutic Observation",
        "label_tr": "Terapötik Gözlem",
        "desc_en": "How music is affecting your stress, mood, and emotional regulation systems.",
        "desc_tr": "Müziğin stres, ruh hali ve duygusal düzenleme sistemlerini nasıl etkilediği.",
        "requires": ["neurochemicals", "functions", "ram_26d"],
    },
    {
        "type": "musical_counseling",
        "min_level": 9,
        "label_en": "Musical Counseling",
        "label_tr": "Müzikal Danışmanlık",
        "desc_en": "Deep insights about your relationship with music and its role in your life.",
        "desc_tr": "Müzikle ilişkin ve müziğin hayatındaki rolü hakkında derin içgörüler.",
        "requires": ["dimensions_6d", "functions", "beliefs", "genes"],
    },
    {
        "type": "cross_m3_insight",
        "min_level": 9,
        "label_en": "Cross-M³ Insight",
        "label_tr": "Çapraz-M³ İçgörü",
        "desc_en": "How different MI dimensions interact to create your unique listening fingerprint.",
        "desc_tr": "Farklı MI boyutlarının benzersiz dinleme parmak izini oluşturmak için nasıl etkileştiği.",
        "requires": ["dimensions_6d", "dimensions_12d", "beliefs", "ram_26d"],
    },
    {
        "type": "meta_awareness",
        "min_level": 11,
        "label_en": "Meta-Awareness",
        "label_tr": "Meta-Farkındalık",
        "desc_en": "Awareness of your own awareness — how your brain processes music and how that processing changes you.",
        "desc_tr": "Kendi farkındalığının farkındalığı — beyninin müziği nasıl işlediği ve bu işlemenin seni nasıl değiştirdiği.",
        "requires": ["dimensions_6d", "functions", "beliefs", "ram_26d", "temporal"],
    },
]


# ── Public API ──────────────────────────────────────────────────


def get_available_observations(
    level: int,
    language: str = "tr",
) -> list[dict[str, Any]]:
    """List observation types available at the given level.

    Returns:
        List of {type, label, desc, min_level} for each unlocked observation.
    """
    sfx = "tr" if language == "tr" else "en"

    available: list[dict] = []
    for obs in _OBSERVATION_TYPES:
        if level >= obs["min_level"]:
            available.append({
                "type": obs["type"],
                "label": obs[f"label_{sfx}"],
                "desc": obs[f"desc_{sfx}"],
                "min_level": obs["min_level"],
                "requires": obs["requires"],
            })

    return available


def get_observation_type(
    level: int,
    available_data: list[str],
    language: str = "tr",
) -> dict[str, Any] | None:
    """Select the best observation type for the given level and available data.

    Args:
        level: user level (1-12)
        available_data: list of data keys available
            (e.g., ["dimensions_6d", "neurochemicals", "functions"])
        language: "tr" or "en"

    Returns:
        Best matching observation type, or None if level < 2.
    """
    sfx = "tr" if language == "tr" else "en"

    # Iterate from highest level to lowest to find the best match
    candidates = [
        obs for obs in reversed(_OBSERVATION_TYPES)
        if level >= obs["min_level"]
    ]

    for obs in candidates:
        # Check if required data is available
        if all(req in available_data for req in obs["requires"]):
            return {
                "type": obs["type"],
                "label": obs[f"label_{sfx}"],
                "desc": obs[f"desc_{sfx}"],
                "min_level": obs["min_level"],
            }

    # Fall back to lowest available
    if candidates:
        obs = candidates[-1]
        return {
            "type": obs["type"],
            "label": obs[f"label_{sfx}"],
            "desc": obs[f"desc_{sfx}"],
            "min_level": obs["min_level"],
        }

    return None
