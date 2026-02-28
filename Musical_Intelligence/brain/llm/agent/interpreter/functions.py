"""Function Interpreter — F1-F9 comparative narrative.

Compares function activations to each other (not just absolute values)
to produce meaningful contrasts like:
  F2 >> F1 → "predicting more than sensing"
  F6 highest → "peak enjoyment"
  F4 spike → "nostalgia"
"""

from __future__ import annotations

import json
from typing import Any

from Musical_Intelligence.brain.llm.config import KNOWLEDGE_DIR
from .polarity import classify_value, polarity_label

# ── Function Card Cache ──────────────────────────────────────────

_fn_cards: list[dict] | None = None


def _load_cards() -> list[dict]:
    global _fn_cards
    if _fn_cards is None:
        path = KNOWLEDGE_DIR / "functions.jsonl"
        _fn_cards = []
        if path.exists():
            for line in path.read_text(encoding="utf-8").strip().splitlines():
                if line.strip():
                    _fn_cards.append(json.loads(line))
    return _fn_cards


# ── Comparative Patterns ────────────────────────────────────────

_CONTRASTS: list[dict[str, Any]] = [
    {
        "condition": lambda f: f.get("F2", 0) - f.get("F1", 0) > 0.15,
        "text_en": "The brain is predicting more than sensing — the music has patterns the brain is actively tracking. You know what's coming (mostly), and that's where the engagement lives.",
        "text_tr": "Beyin duymaktan çok tahmin ediyor — müziğin beynin aktif olarak takip ettiği kalıpları var. Ne geleceğini (çoğunlukla) biliyorsun ve bağlanma tam da burada yaşıyor.",
    },
    {
        "condition": lambda f: f.get("F6", 0) > 0.65 and f.get("F6", 0) == max(f.values()),
        "text_en": "Peak enjoyment — the reward system leads all other functions. This is where musical pleasure is most concentrated.",
        "text_tr": "Zirve keyif — ödül sistemi diğer tüm fonksiyonların önünde. Müzikal hazzın en yoğun olduğu yer burası.",
    },
    {
        "condition": lambda f: f.get("F5", 0) > 0.6 and f.get("F6", 0) > 0.6,
        "text_en": "Deep emotional reward — emotion AND pleasure are both high. This is the most powerful musical experience: feeling something deeply AND finding it rewarding.",
        "text_tr": "Derin duygusal ödül — duygu VE haz birlikte yüksek. Bu en güçlü müzikal deneyim: bir şeyi derinden hissedip onu ödüllendirici bulma.",
    },
    {
        "condition": lambda f: f.get("F3", 0) > 0.6 and f.get("F3", 0) >= max(f.get("F1", 0), f.get("F2", 0)),
        "text_en": "Attention-demanding music — the salience network is leading. Something novel, complex, or rhythmically compelling is commanding focus.",
        "text_tr": "Dikkat talep eden müzik — belirginlik ağı önde. Yeni, karmaşık veya ritmik olarak çekici bir şey odağı komuta ediyor.",
    },
    {
        "condition": lambda f: f.get("F7", 0) > 0.6 and f.get("F3", 0) > 0.5,
        "text_en": "Groove-driven attention — motor coupling and salience are both high. The rhythm grabs you and won't let go. Dance music territory.",
        "text_tr": "Groove güdümlü dikkat — motor bağlanma ve belirginlik birlikte yüksek. Ritim seni yakalıyor ve bırakmıyor. Dans müziği alanı.",
    },
    {
        "condition": lambda f: f.get("F4", 0) > 0.6 and f.get("F4", 0) - max(f.get("F1", 0), f.get("F2", 0), f.get("F3", 0)) > 0.1,
        "text_en": "Memory leads — nostalgia or recognition is the dominant experience. The music is transporting you somewhere you've been before.",
        "text_tr": "Hafıza önde — nostalji veya tanıma baskın deneyim. Müzik seni daha önce gittiğin bir yere taşıyor.",
    },
    {
        "condition": lambda f: f.get("F8", 0) > 0.55 and f.get("F2", 0) > 0.5,
        "text_en": "Learning mode — the brain is adapting and forming new prediction models. This music is expanding your neural repertoire.",
        "text_tr": "Öğrenme modu — beyin yeni tahmin modelleri oluşturuyor ve uyum sağlıyor. Bu müzik nöral repertuarını genişletiyor.",
    },
]


# ── Main Interpreter ─────────────────────────────────────────────


def interpret_functions(
    function_values: dict[str, float],
    language: str = "tr",
    tier: str = "free",
) -> dict[str, Any]:
    """Interpret F1-F9 function activations comparatively.

    Args:
        function_values: {F1..F9} → float 0-1
        language: "tr" or "en"
        tier: user tier

    Returns:
        Dict with "narrative", "highlights", "ranking", "contrasts".
    """
    cards = _load_cards()
    card_map = {c["key"]: c for c in cards}
    sfx = "tr" if language == "tr" else "en"

    # Rank functions by activation
    ranking = sorted(
        [(k, v) for k, v in function_values.items() if k.startswith("F")],
        key=lambda x: x[1],
        reverse=True,
    )

    ranked_info: list[dict] = []
    for fn_key, fn_val in ranking:
        card = card_map.get(fn_key, {})
        pol = classify_value(fn_val)
        if pol in ("very_high", "high"):
            desc = card.get(f"high_{sfx}", "")
        elif pol in ("very_low", "low"):
            desc = card.get(f"low_{sfx}", "")
        else:
            desc = ""

        ranked_info.append({
            "key": fn_key,
            "name": card.get(f"name_{sfx}", fn_key),
            "value": round(fn_val, 3),
            "polarity": polarity_label(fn_val, language),
            "role": card.get(f"role_{sfx}", ""),
            "text": desc,
        })

    # Detect contrastive patterns
    contrasts: list[str] = []
    for pattern in _CONTRASTS:
        if pattern["condition"](function_values):
            contrasts.append(pattern[f"text_{sfx}"])

    # Build narrative
    parts: list[str] = []

    # Dominant function
    if ranking:
        top_fn, top_val = ranking[0]
        top_card = card_map.get(top_fn, {})
        top_name = top_card.get(f"name_{sfx}", top_fn)
        top_role = top_card.get(f"role_{sfx}", "")

        if language == "tr":
            parts.append(f"**Baskın fonksiyon**: {top_name} — {top_role}")
        else:
            parts.append(f"**Dominant function**: {top_name} — {top_role}")

    # Contrast narratives
    if contrasts:
        parts.append("")
        for c in contrasts[:2]:
            parts.append(c)

    # Secondary functions worth noting
    if len(ranking) >= 3:
        second = ranked_info[1]
        if second["value"] > 0.5 and second["text"]:
            parts.append("")
            if language == "tr":
                parts.append(f"**İkincil**: {second['name']} — {second['text']}")
            else:
                parts.append(f"**Secondary**: {second['name']} — {second['text']}")

    highlights: list[str] = []
    for r in ranked_info[:3]:
        if r["value"] > 0.5:
            highlights.append(f"{r['name']}: {r['role']}")
    highlights.extend(contrasts[:2])

    return {
        "narrative": "\n".join(parts),
        "highlights": highlights[:5],
        "ranking": ranked_info,
        "contrasts": contrasts,
    }
