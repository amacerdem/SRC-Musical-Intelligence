"""Reward Interpreter — decomposes the reward formula into human narrative.

reward = Σ beliefs [salience × (1.5×surprise + 0.8×resolution +
         0.5×exploration − 0.6×monotony)] × familiarity_mod × DA_gain

Source: Building/Ontology/C³/REWARD-FORMULA.md v3.0
"""

from __future__ import annotations

from typing import Any

from .polarity import classify_value, polarity_label


# ── Reward Component Names ──────────────────────────────────────

_COMPONENTS = {
    "surprise": {
        "weight": 1.5,
        "name_en": "Surprise",
        "name_tr": "Sürpriz",
        "desc_en": "High prediction error in unfamiliar context — novel, unexpected musical moments.",
        "desc_tr": "Tanımadık bağlamda yüksek tahmin hatası — yeni, beklenmedik müzikal anlar.",
        "high_en": "The music is full of genuinely surprising moments that your brain didn't predict.",
        "high_tr": "Müzik beyninin tahmin edemediği gerçekten şaşırtıcı anlarla dolu.",
        "low_en": "Few surprises — the music is largely predictable from the brain's perspective.",
        "low_tr": "Az sürpriz — müzik beynin perspektifinden büyük ölçüde öngörülebilir.",
    },
    "resolution": {
        "weight": 0.8,
        "name_en": "Resolution",
        "name_tr": "Çözüm",
        "desc_en": "Low prediction error in familiar context — satisfying expectations, confirming predictions.",
        "desc_tr": "Tanıdık bağlamda düşük tahmin hatası — beklentileri karşılama, tahminleri doğrulama.",
        "high_en": "Your predictions are being confirmed beautifully — the music goes where you expected and it feels good.",
        "high_tr": "Tahminlerin güzel bir şekilde doğrulanıyor — müzik beklediğin yere gidiyor ve iyi hissettiriyor.",
        "low_en": "Predictions aren't being met or the music is too unfamiliar for resolution reward.",
        "low_tr": "Tahminler karşılanmıyor veya müzik çözüm ödülü için çok tanımadık.",
    },
    "exploration": {
        "weight": 0.5,
        "name_en": "Exploration",
        "name_tr": "Keşif",
        "desc_en": "High prediction error with low precision — learning new patterns, expanding neural models.",
        "desc_tr": "Düşük hassasiyetle yüksek tahmin hatası — yeni kalıplar öğrenme, nöral modelleri genişletme.",
        "high_en": "The brain is in learning mode — encountering new patterns and building new models. The joy of discovery.",
        "high_tr": "Beyin öğrenme modunda — yeni kalıplarla karşılaşma ve yeni modeller inşa etme. Keşfin sevinci.",
        "low_en": "Not much new to learn — either fully familiar or too random to form patterns.",
        "low_tr": "Öğrenecek çok yeni şey yok — ya tamamen tanıdık ya da kalıp oluşturamayacak kadar rastgele.",
    },
    "monotony": {
        "weight": -0.6,
        "name_en": "Monotony",
        "name_tr": "Monotonluk",
        "desc_en": "Too predictable — boredom penalty when prediction errors are consistently low.",
        "desc_tr": "Çok öngörülebilir — tahmin hataları sürekli düşük olduğunda sıkılma cezası.",
        "high_en": "Boredom signal — the music is too predictable. The brain has fully modeled it and there's nothing new.",
        "high_tr": "Sıkılma sinyali — müzik çok öngörülebilir. Beyin onu tamamen modelledi ve yeni bir şey yok.",
        "low_en": "Low monotony is good — the music maintains enough novelty to avoid boredom.",
        "low_tr": "Düşük monotonluk iyi — müzik sıkılmayı önleyecek kadar yenilik koruyor.",
    },
}


def _inverted_u_label(familiarity: float, language: str = "en") -> str:
    """Describe where on the inverted-U familiarity curve this falls."""
    # Familiarity modifier: 4 × f × (1-f), peaks at 0.5
    mod = 4.0 * familiarity * (1.0 - familiarity)

    if familiarity < 0.2:
        return {
            "en": "Too new — the brain hasn't built enough models yet. Reward grows with repeated listening.",
            "tr": "Çok yeni — beyin henüz yeterli model oluşturmadı. Ödül tekrar dinlemeyle büyür.",
        }[language]
    elif familiarity < 0.4:
        return {
            "en": "Getting familiar — approaching the sweet spot. A few more listens and reward will peak.",
            "tr": "Tanıdık olmaya başlıyor — tatlı noktaya yaklaşıyor. Birkaç dinleme daha ve ödül zirve yapacak.",
        }[language]
    elif familiarity <= 0.6:
        return {
            "en": "The sweet spot — not too new, not too old. This is where the 3rd listen magic happens. Maximum reward potential.",
            "tr": "Tatlı nokta — ne çok yeni ne çok eski. 3. dinleme büyüsünün gerçekleştiği yer. Maksimum ödül potansiyeli.",
        }[language]
    elif familiarity <= 0.8:
        return {
            "en": "Getting overly familiar — reward is declining. The brain has heard this enough times that surprise is rare.",
            "tr": "Aşırı tanıdık olmaya başlıyor — ödül azalıyor. Beyin bunu yeterince dinledi, sürpriz nadir.",
        }[language]
    else:
        return {
            "en": "Overexposed — strong familiarity penalty. Only nostalgia can rescue reward at this point.",
            "tr": "Aşırı maruz kalma — güçlü tanıdıklık cezası. Bu noktada sadece nostalji ödülü kurtarabilir.",
        }[language]


# ── Main Interpreter ─────────────────────────────────────────────


def interpret_reward(
    reward_data: dict[str, Any],
    language: str = "tr",
    tier: str = "free",
) -> dict[str, Any]:
    """Decompose reward into its component narratives.

    Args:
        reward_data: Dict with keys:
            - total: float (overall reward 0-1)
            - surprise: float (0-1)
            - resolution: float (0-1)
            - exploration: float (0-1)
            - monotony: float (0-1)
            - familiarity: float (0-1, optional)
            - da_gain: float (optional)
        language: "tr" or "en"
        tier: user tier

    Returns:
        Dict with "narrative", "highlights", "components", "familiarity_note".
    """
    sfx = "tr" if language == "tr" else "en"

    total = reward_data.get("total", reward_data.get("reward", 0.5))
    familiarity = reward_data.get("familiarity", None)

    # Component analysis
    components: list[dict] = []
    dominant_component = ""
    dominant_value = 0.0

    for comp_key, comp_info in _COMPONENTS.items():
        value = reward_data.get(comp_key, 0.5)
        pol = classify_value(value)

        if pol in ("very_high", "high"):
            desc = comp_info[f"high_{sfx}"]
        elif pol in ("very_low", "low"):
            desc = comp_info[f"low_{sfx}"]
        else:
            desc = comp_info[f"desc_{sfx}"]

        # Track dominant positive component
        if comp_key != "monotony" and value > dominant_value:
            dominant_value = value
            dominant_component = comp_key

        components.append({
            "key": comp_key,
            "name": comp_info[f"name_{sfx}"],
            "value": round(value, 3),
            "weight": comp_info["weight"],
            "polarity": polarity_label(value, language),
            "text": desc,
        })

    # Build narrative
    parts: list[str] = []

    # Overall reward level
    total_pol = classify_value(total)
    if language == "tr":
        parts.append(f"**Toplam ödül**: {polarity_label(total, language)} ({total:.2f})")
    else:
        parts.append(f"**Total reward**: {polarity_label(total, language)} ({total:.2f})")

    # Dominant component
    if dominant_component:
        dom = _COMPONENTS[dominant_component]
        if language == "tr":
            parts.append(f"**Baskın kaynak**: {dom[f'name_{sfx}']} — {dom[f'desc_{sfx}']}")
        else:
            parts.append(f"**Dominant source**: {dom[f'name_{sfx}']} — {dom[f'desc_{sfx}']}")

    # Monotony warning
    monotony = reward_data.get("monotony", 0.0)
    if monotony > 0.6:
        parts.append("")
        mono_comp = _COMPONENTS["monotony"]
        parts.append(f"⚠ {mono_comp[f'name_{sfx}']}: {mono_comp[f'high_{sfx}']}")

    # Familiarity curve
    familiarity_note = ""
    if familiarity is not None:
        familiarity_note = _inverted_u_label(familiarity, language)
        parts.append("")
        if language == "tr":
            parts.append(f"**Tanıdıklık** ({familiarity:.2f}): {familiarity_note}")
        else:
            parts.append(f"**Familiarity** ({familiarity:.2f}): {familiarity_note}")

    highlights: list[str] = []
    if total_pol in ("very_high", "high"):
        if language == "tr":
            highlights.append("Güçlü ödül deneyimi")
        else:
            highlights.append("Strong reward experience")
    if dominant_component:
        highlights.append(f"{_COMPONENTS[dominant_component][f'name_{sfx}']} dominant")
    if monotony > 0.6:
        if language == "tr":
            highlights.append("Monotonluk uyarısı")
        else:
            highlights.append("Monotony warning")

    return {
        "narrative": "\n".join(parts),
        "highlights": highlights,
        "components": components,
        "familiarity_note": familiarity_note,
    }
