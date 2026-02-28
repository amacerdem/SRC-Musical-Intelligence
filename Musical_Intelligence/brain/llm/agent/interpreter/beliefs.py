"""Belief Pattern Interpreter — cross-function belief pattern detection.

Detects meaningful patterns across the 131 beliefs:
- harmonic_stability↑ + prediction_accuracy↓ = "stable but surprising"
- beat_entrainment↑ + groove_quality↑ = "visceral rhythmic engagement"
- wanting↑ + pleasure↓ = "anticipation mode"
- autobiographical_retrieval spike = "personal memory triggered"
- High std = dynamic/shifting experience
"""

from __future__ import annotations

from typing import Any

from Musical_Intelligence.brain.llm.agent.track_data import (
    belief_index_to_key,
    get_belief_meta,
    _ensure_belief_keys,
)
from .polarity import classify_value, polarity_label

# ── Cross-Function Patterns ─────────────────────────────────────

_PATTERNS: list[dict[str, Any]] = [
    {
        "name": "stable_but_surprising",
        "check": lambda b: b.get("harmonic_stability", 0) > 0.65 and b.get("prediction_accuracy", 0) < 0.4,
        "label_en": "Stable but Surprising",
        "label_tr": "Kararlı ama Şaşırtıcı",
        "text_en": "The music has a stable tonal center but does unexpected things within it — classic jazz, progressive rock, or sophisticated pop harmony.",
        "text_tr": "Müzik kararlı bir tonal merkeze sahip ama içinde beklenmedik şeyler yapıyor — klasik caz, progresif rock veya sofistike pop harmonisi.",
    },
    {
        "name": "visceral_groove",
        "check": lambda b: b.get("beat_entrainment", 0) > 0.65 and b.get("groove_quality", 0) > 0.6,
        "label_en": "Visceral Rhythmic Engagement",
        "label_tr": "İçgüdüsel Ritmik Bağlanma",
        "text_en": "The rhythm has locked in at a deep, physical level. Beat entrainment AND groove quality are both high — this is music that moves the body without asking permission.",
        "text_tr": "Ritim derin, fiziksel bir seviyede kilitlendi. Ritim senkronizasyonu VE groove kalitesi birlikte yüksek — bu, izin istemeden vücudu hareket ettiren müzik.",
    },
    {
        "name": "anticipation_mode",
        "check": lambda b: b.get("wanting", 0) > 0.6 and b.get("pleasure", 0) < 0.45,
        "label_en": "Anticipation Mode",
        "label_tr": "Beklenti Modu",
        "text_en": "The brain is wanting but not yet receiving — the best part hasn't come yet. Build-up state before the peak, the drop, or the resolution.",
        "text_tr": "Beyin istiyor ama henüz almıyor — en iyi kısım henüz gelmedi. Doruk, drop veya çözüm öncesi birikim durumu.",
    },
    {
        "name": "memory_triggered",
        "check": lambda b: b.get("autobiographical_retrieval", 0) > 0.65,
        "label_en": "Personal Memory Triggered",
        "label_tr": "Kişisel Anı Tetiklendi",
        "text_en": "The music has activated autobiographical memory — a personal association, a time, a place, a person. This is the 'music as time machine' phenomenon.",
        "text_tr": "Müzik otobiyografik hafızayı aktive etti — kişisel bir çağrışım, bir zaman, bir mekan, bir kişi. Bu 'zaman makinesi olarak müzik' fenomeni.",
    },
    {
        "name": "intellectual_reward",
        "check": lambda b: b.get("prediction_accuracy", 0) > 0.6 and b.get("information_content", 0) > 0.6 and b.get("beat_entrainment", 0) < 0.4,
        "label_en": "Intellectual Reward",
        "label_tr": "Entelektüel Ödül",
        "text_en": "Pattern recognition is driving the experience, not groove. The brain is engaged intellectually — tracking predictions, finding structure. Classical music listening, jazz analysis, or deep structural engagement.",
        "text_tr": "Deneyimi groove değil örüntü tanıma yönlendiriyor. Beyin entelektüel olarak bağlanmış — tahminleri takip etme, yapı bulma. Klasik müzik dinleme, caz analizi veya derin yapısal bağlanma.",
    },
    {
        "name": "emotional_peak",
        "check": lambda b: b.get("emotional_arousal", 0) > 0.65 and b.get("pleasure", 0) > 0.6,
        "label_en": "Emotional Peak",
        "label_tr": "Duygusal Doruk",
        "text_en": "High arousal AND pleasure together — the music is creating intense positive emotion. This is where chills happen, where tears of joy flow, where music feels transcendent.",
        "text_tr": "Yüksek uyarılma VE haz birlikte — müzik yoğun pozitif duygu yaratıyor. Ürpertilerin olduğu, mutluluk gözyaşlarının aktığı, müziğin aşkın hissettirdiği yer.",
    },
    {
        "name": "tension_without_resolution",
        "check": lambda b: b.get("harmonic_stability", 0) < 0.35 and b.get("pleasure", 0) < 0.4 and b.get("wanting", 0) > 0.5,
        "label_en": "Unresolved Tension",
        "label_tr": "Çözülmemiş Gerilim",
        "text_en": "Harmonic instability with wanting but no pleasure — the music is building tension without providing resolution. Suspended state, deferred gratification.",
        "text_tr": "İstek ile harmonik dengesizlik ama haz yok — müzik çözüm sağlamadan gerilim inşa ediyor. Askıda durum, ertelenmiş tatmin.",
    },
    {
        "name": "dynamic_experience",
        "check": lambda b: False,  # checked separately via std
        "label_en": "Dynamic Experience",
        "label_tr": "Dinamik Deneyim",
        "text_en": "High belief variability — the experience is shifting constantly. Each moment feels different from the last.",
        "text_tr": "Yüksek inanç değişkenliği — deneyim sürekli kayıyor. Her an bir öncekinden farklı hissettiriyor.",
    },
]


# ── Main Interpreter ─────────────────────────────────────────────


def interpret_beliefs(
    means: list[float],
    stds: list[float],
    language: str = "tr",
    tier: str = "free",
    n_notable: int = 10,
) -> dict[str, Any]:
    """Interpret belief patterns with cross-function analysis.

    Args:
        means: 131 belief means
        stds: 131 belief stds
        language: "tr" or "en"
        tier: user tier
        n_notable: number of notable beliefs to highlight

    Returns:
        Dict with "narrative", "highlights", "patterns", "notable_beliefs".
    """
    _ensure_belief_keys()
    sfx = "tr" if language == "tr" else "en"

    # Build belief lookup by name
    belief_values: dict[str, float] = {}
    belief_stds: dict[str, float] = {}
    for i, (m, s) in enumerate(zip(means, stds)):
        key = belief_index_to_key(i)
        belief_values[key] = m
        belief_stds[key] = s

    # Find notable beliefs (most extreme + most dynamic)
    scored: list[dict] = []
    for i, (m, s) in enumerate(zip(means, stds)):
        key = belief_index_to_key(i)
        meta = get_belief_meta(key)
        extremity = abs(m - 0.5) * 2
        dynamism = min(s * 10, 1.0)
        notability = extremity * 0.6 + dynamism * 0.4

        scored.append({
            "key": key,
            "value": round(m, 3),
            "std": round(s, 3),
            "polarity": polarity_label(m, language),
            "function": meta.get("function", ""),
            "type": meta.get("type", ""),
            "what": meta.get(f"what_{sfx}", meta.get("what_en", "")),
            "analogy": meta.get(f"analogy_{sfx}", meta.get("analogy_en", "")),
            "notability": round(notability, 3),
        })

    scored.sort(key=lambda x: x["notability"], reverse=True)
    notable = scored[:n_notable]

    # Detect patterns
    detected: list[dict] = []
    for pattern in _PATTERNS:
        if pattern["name"] == "dynamic_experience":
            # Check average std
            avg_std = sum(stds) / len(stds) if stds else 0
            if avg_std > 0.08:
                detected.append({
                    "name": pattern["name"],
                    "label": pattern[f"label_{sfx}"],
                    "text": pattern[f"text_{sfx}"],
                })
        elif pattern["check"](belief_values):
            detected.append({
                "name": pattern["name"],
                "label": pattern[f"label_{sfx}"],
                "text": pattern[f"text_{sfx}"],
            })

    # Build narrative
    parts: list[str] = []

    # Patterns first (most insightful)
    if detected:
        for p in detected[:3]:
            parts.append(f"**{p['label']}**: {p['text']}")
            parts.append("")

    # Notable beliefs
    if notable:
        if language == "tr":
            parts.append("**Öne çıkan inançlar:**")
        else:
            parts.append("**Notable beliefs:**")

        for b in notable[:6]:
            std_note = ""
            if b["std"] > 0.08:
                if language == "tr":
                    std_note = " (dinamik — parça boyunca değişken)"
                else:
                    std_note = " (dynamic — varies across the piece)"

            parts.append(f"- **{b['key']}** [{b['function']}] ({b['polarity']}): {b['what']}{std_note}")

    highlights = [p["label"] for p in detected[:3]]
    if not highlights:
        highlights = [f"{b['key']}: {b['polarity']}" for b in notable[:3]]

    return {
        "narrative": "\n".join(parts),
        "highlights": highlights,
        "patterns": detected,
        "notable_beliefs": notable,
    }
