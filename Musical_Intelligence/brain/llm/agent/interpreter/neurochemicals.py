"""Neurochemical Interpreter — combination narrative for DA, NE, OPI, 5HT.

Goes beyond single-chemical polarity to detect meaningful combinations:
DA↑+OPI↑ = "wanting and liking together"
DA↑+OPI↓ = "wanting but not yet liking"
NE↑+DA↑  = "alert and seeking"
5HT↑+OPI↑ = "peaceful satisfaction"
"""

from __future__ import annotations

import json
from typing import Any

from Musical_Intelligence.brain.llm.config import KNOWLEDGE_DIR
from .polarity import classify_value, polarity_label

# ── Neurochemical Card Cache ────────────────────────────────────

_neuro_cards: list[dict] | None = None


def _load_cards() -> list[dict]:
    global _neuro_cards
    if _neuro_cards is None:
        path = KNOWLEDGE_DIR / "neurochemicals.jsonl"
        _neuro_cards = []
        if path.exists():
            for line in path.read_text(encoding="utf-8").strip().splitlines():
                if line.strip():
                    _neuro_cards.append(json.loads(line))
    return _neuro_cards


# ── Combination Patterns ────────────────────────────────────────

_COMBINATIONS: list[dict[str, Any]] = [
    {
        "condition": lambda l: l.get("DA", 0) > 0.6 and l.get("OPI", 0) > 0.6,
        "label_en": "Full Reward Cycle",
        "label_tr": "Tam Ödül Döngüsü",
        "text_en": "Both wanting and liking are active — the complete musical reward experience. The brain anticipated something rewarding (DA) AND found it pleasurable (OPI). This is the neural signature of musical bliss.",
        "text_tr": "Hem istek hem beğeni aktif — tam müzikal ödül deneyimi. Beyin ödüllendirici bir şey bekledi (DA) VE onu haz verici buldu (OPI). Bu müzikal mutluluğun nöral imzası.",
    },
    {
        "condition": lambda l: l.get("DA", 0) > 0.6 and l.get("OPI", 0) < 0.4,
        "label_en": "Anticipation Without Arrival",
        "label_tr": "Varışsız Beklenti",
        "text_en": "The brain is wanting but not yet liking — anticipation mode. The build-up is happening but the peak hasn't arrived. Classic pre-drop, pre-chorus, or tension-building state.",
        "text_tr": "Beyin istiyor ama henüz beğenmiyor — beklenti modu. Birikim oluyor ama doruk henüz gelmedi. Klasik drop-öncesi, nakarat-öncesi veya gerilim-inşa durumu.",
    },
    {
        "condition": lambda l: l.get("DA", 0) < 0.4 and l.get("OPI", 0) > 0.6,
        "label_en": "Pure Pleasure",
        "label_tr": "Saf Haz",
        "text_en": "Liking without strong wanting — the music is beautiful but not generating anticipation. Consummatory pleasure: a resolved chord, a held note, a moment of pure beauty. The brain is savoring, not seeking.",
        "text_tr": "Güçlü istek olmadan beğeni — müzik güzel ama beklenti üretmiyor. Tüketici haz: çözümlenmiş bir akor, tutulan bir nota, saf güzellik anı. Beyin arıyor değil, tadını çıkarıyor.",
    },
    {
        "condition": lambda l: l.get("NE", 0) > 0.6 and l.get("DA", 0) > 0.6,
        "label_en": "Alert Seeking",
        "label_tr": "Uyanık Arama",
        "text_en": "High attention AND high anticipation — the brain is alert and seeking. Something novel is happening and the brain expects it to be rewarding. Peak engagement state.",
        "text_tr": "Yüksek dikkat VE yüksek beklenti — beyin uyanık ve arıyor. Yeni bir şey oluyor ve beyin ödüllendirici olmasını bekliyor. Zirve bağlanma durumu.",
    },
    {
        "condition": lambda l: l.get("5HT", 0) > 0.6 and l.get("OPI", 0) > 0.6,
        "label_en": "Peaceful Satisfaction",
        "label_tr": "Huzurlu Memnuniyet",
        "text_en": "Contentment and pleasure together — calm, warm satisfaction. The brain is in a comfort zone: familiar music generating gentle pleasure. Like being home.",
        "text_tr": "Memnuniyet ve haz birlikte — sakin, sıcak tatmin. Beyin konfor bölgesinde: tanıdık müzik nazik haz üretiyor. Evde olmak gibi.",
    },
    {
        "condition": lambda l: l.get("5HT", 0) < 0.3 and l.get("DA", 0) > 0.6,
        "label_en": "Intense Seeking",
        "label_tr": "Yoğun Arama",
        "text_en": "Low comfort with high wanting — intense seeking behavior. The brain is restless, driven, hungry for the next peak. Low patience, high drive. The feeling before you discover a new favorite song.",
        "text_tr": "Düşük konfor, yüksek istek — yoğun arama davranışı. Beyin huzursuz, güdümlü, bir sonraki doruk için aç. Düşük sabır, yüksek dürtü. Yeni favori şarkını keşfetmeden önceki his.",
    },
    {
        "condition": lambda l: l.get("NE", 0) > 0.7 and l.get("OPI", 0) > 0.5,
        "label_en": "Chills State",
        "label_tr": "Ürperti Durumu",
        "text_en": "High arousal with pleasure — the physiological signature of musical chills. Goosebumps, hair standing on end, spine tingles. The most intense brief musical experience.",
        "text_tr": "Yüksek uyarılma ve haz — müzikal ürpertilerin fizyolojik imzası. Tüylerin diken diken olması, omurga karıncalanması. En yoğun kısa müzikal deneyim.",
    },
    {
        "condition": lambda l: all(l.get(k, 0) < 0.4 for k in ("DA", "NE", "OPI", "5HT")),
        "label_en": "Disengaged",
        "label_tr": "Bağlantısız",
        "text_en": "All neurochemical channels are low — the brain isn't strongly engaged with this music. This can mean boredom, distraction, or simply that the music isn't speaking to this listener's neural profile.",
        "text_tr": "Tüm nörokimyasal kanallar düşük — beyin bu müzikle güçlü bir şekilde bağlanmıyor. Bu sıkılma, dikkat dağınıklığı veya basitçe müziğin bu dinleyicinin nöral profiline konuşmaması anlamına gelebilir.",
    },
]


# ── Main Interpreter ─────────────────────────────────────────────


def interpret_neurochemicals(
    levels: dict[str, float],
    language: str = "tr",
    tier: str = "free",
) -> dict[str, Any]:
    """Interpret neurochemical levels with combination detection.

    Args:
        levels: {DA, NE, OPI, 5HT} → float 0-1
        language: "tr" or "en"
        tier: user tier

    Returns:
        Dict with "narrative", "highlights", "individual", "combinations".
    """
    cards = _load_cards()
    card_map = {c["key"]: c for c in cards}
    sfx = "tr" if language == "tr" else "en"

    # Individual channel descriptions
    individual: list[dict] = []
    active_channels: list[str] = []

    for key in ("DA", "NE", "OPI", "5HT"):
        value = levels.get(key, 0.0)
        card = card_map.get(key, {})
        pol = classify_value(value)

        name = card.get(f"name_{sfx}", key)
        role = card.get(f"role_{sfx}", "")
        symbol = card.get("symbol", key)

        individual.append({
            "key": key,
            "symbol": symbol,
            "name": name,
            "value": round(value, 3),
            "polarity": polarity_label(value, language),
            "role": role,
        })

        if value > 0.6:
            active_channels.append(f"{symbol} ({role})")

    # Detect combination patterns
    combinations: list[dict] = []
    for combo in _COMBINATIONS:
        if combo["condition"](levels):
            combinations.append({
                "label": combo[f"label_{sfx}"],
                "text": combo[f"text_{sfx}"],
            })

    # Build narrative
    parts: list[str] = []

    # Combination narrative first (most insightful)
    if combinations:
        for combo in combinations[:2]:  # max 2 combinations
            parts.append(f"**{combo['label']}**: {combo['text']}")
    elif active_channels:
        if language == "tr":
            parts.append("**Aktif nörokimyasallar:**")
        else:
            parts.append("**Active neurochemicals:**")
        for ch in active_channels:
            parts.append(f"- {ch}")
    else:
        if language == "tr":
            parts.append("Nörokimyasal aktivite düşük — beyin bu müzikle güçlü kimyasal bağlanma göstermiyor.")
        else:
            parts.append("Neurochemical activity is low — the brain isn't showing strong chemical engagement with this music.")

    highlights = [c["label"] for c in combinations[:2]]
    if not highlights:
        highlights = active_channels[:3]

    return {
        "narrative": "\n".join(parts),
        "highlights": highlights,
        "individual": individual,
        "combinations": combinations,
    }
