"""Brain Region Interpreter — RAM 26D activation narrative (premium+ tier).

Reads the 26D Regional Activation Map and produces narratives about
which brain areas are most engaged and what that means experientially.
"""

from __future__ import annotations

import json
from typing import Any

from Musical_Intelligence.brain.llm.config import KNOWLEDGE_DIR
from .polarity import classify_value, polarity_label

# ── Region Card Cache ───────────────────────────────────────────

_region_cards: list[dict] | None = None


def _load_cards() -> list[dict]:
    global _region_cards
    if _region_cards is None:
        path = KNOWLEDGE_DIR / "ram_regions.jsonl"
        _region_cards = []
        if path.exists():
            for line in path.read_text(encoding="utf-8").strip().splitlines():
                if line.strip():
                    _region_cards.append(json.loads(line))
    return _region_cards


# ── Meaningful Combinations ─────────────────────────────────────

_COMBOS: list[dict[str, Any]] = [
    {
        "regions": ["NAcc", "VTA"],
        "threshold": 0.6,
        "label_en": "Reward Circuit Active",
        "label_tr": "Ödül Devresi Aktif",
        "text_en": "The dopamine factory (VTA) and pleasure center (NAcc) are both firing — strong reward circuit engagement. This is the neural signature of musical pleasure.",
        "text_tr": "Dopamin fabrikası (VTA) ve haz merkezi (NAcc) birlikte ateşleniyor — güçlü ödül devresi bağlanması. Bu müzikal hazzın nöral imzası.",
    },
    {
        "regions": ["hippocampus", "vmPFC"],
        "threshold": 0.55,
        "label_en": "Memory-Self Circuit",
        "label_tr": "Hafıza-Benlik Devresi",
        "text_en": "Memory hub and self-referential processing are co-active — the music is connecting to personal identity and autobiographical memory. 'This is MY song' territory.",
        "text_tr": "Hafıza merkezi ve öz-referanslı işleme birlikte aktif — müzik kişisel kimliğe ve otobiyografik hafızaya bağlanıyor. 'Bu BENİM şarkım' alanı.",
    },
    {
        "regions": ["SMA", "PMC", "putamen"],
        "threshold": 0.55,
        "label_en": "Motor-Timing Network",
        "label_tr": "Motor-Zamanlama Ağı",
        "text_en": "The full motor circuit is engaged — SMA (planning), PMC (execution), putamen (timing). The body wants to move. This is groove at the neural level.",
        "text_tr": "Tam motor devresi aktif — SMA (planlama), PMC (yürütme), putamen (zamanlama). Vücut hareket etmek istiyor. Bu nöral düzeyde groove.",
    },
    {
        "regions": ["amygdala", "insula"],
        "threshold": 0.55,
        "label_en": "Deep Emotional Processing",
        "label_tr": "Derin Duygusal İşleme",
        "text_en": "The emotional evaluator (amygdala) and body-awareness center (insula) are both active — the listener FEELS this music in their body, not just their mind.",
        "text_tr": "Duygusal değerlendirici (amigdala) ve vücut-farkındalık merkezi (insula) birlikte aktif — dinleyici bu müziği sadece zihninde değil vücudunda HİSSEDİYOR.",
    },
    {
        "regions": ["STG", "IFG"],
        "threshold": 0.6,
        "label_en": "Structural Processing",
        "label_tr": "Yapısal İşleme",
        "text_en": "The convergence hub (STG) and syntax processor (IFG/Broca's) are highly active — deep structural analysis of musical grammar, chord progressions, and hierarchical organization.",
        "text_tr": "Birleşim merkezi (STG) ve sözdizimi işlemcisi (IFG/Broca) çok aktif — müzikal gramer, akor ilerlemeleri ve hiyerarşik organizasyonun derin yapısal analizi.",
    },
]


# ── Main Interpreter ─────────────────────────────────────────────


def interpret_brain_regions(
    ram_26d: dict[str, float] | list[float],
    language: str = "tr",
    tier: str = "premium",
) -> dict[str, Any]:
    """Interpret 26D brain region activation map.

    Args:
        ram_26d: Either {region_key: float} dict or [26 floats] list.
        language: "tr" or "en"
        tier: user tier (only premium+ gets this)

    Returns:
        Dict with "narrative", "highlights", "top_regions",
        "combinations", "group_summary".
    """
    cards = _load_cards()
    card_map = {c["key"]: c for c in cards}
    sfx = "tr" if language == "tr" else "en"

    # Normalize input to dict {region_key: float}
    # Accepts: list[float], dict with "means" key, or flat {key: float}
    if isinstance(ram_26d, dict) and "means" in ram_26d:
        # Nested format: {"means": [26 floats], "stds": [26 floats]}
        raw_list = ram_26d["means"]
        raw_values: dict[str, float] = {}
        for card in cards:
            idx = card.get("index", -1)
            if 0 <= idx < len(raw_list):
                raw_values[card["key"]] = raw_list[idx]
    elif isinstance(ram_26d, list):
        raw_values = {}
        for card in cards:
            idx = card.get("index", -1)
            if 0 <= idx < len(ram_26d):
                raw_values[card["key"]] = ram_26d[idx]
    else:
        raw_values = ram_26d

    # Scale to [0, 1] if values exceed 1.0 (raw activation sums)
    max_val = max(raw_values.values()) if raw_values else 1.0
    if max_val > 1.0:
        values: dict[str, float] = {k: v / max_val for k, v in raw_values.items()}
    else:
        values = raw_values

    # Rank regions by activation
    ranked = sorted(values.items(), key=lambda x: x[1], reverse=True)

    top_regions: list[dict] = []
    for key, val in ranked[:10]:
        card = card_map.get(key, {})
        pol = classify_value(val)
        desc = card.get(f"high_{sfx}", "") if pol in ("very_high", "high") else ""

        top_regions.append({
            "key": key,
            "name": card.get(f"name_{sfx}", key),
            "abbreviation": card.get("abbreviation", key),
            "value": round(val, 3),
            "polarity": polarity_label(val, language),
            "group": card.get("group", "unknown"),
            "functions": card.get("associated_functions", []),
            "text": desc,
        })

    # Detect meaningful combinations
    detected_combos: list[dict] = []
    for combo in _COMBOS:
        all_active = all(
            values.get(r, 0) >= combo["threshold"]
            for r in combo["regions"]
        )
        if all_active:
            detected_combos.append({
                "label": combo[f"label_{sfx}"],
                "text": combo[f"text_{sfx}"],
                "regions": combo["regions"],
            })

    # Group summary
    groups = {"cortical": [], "subcortical": [], "brainstem": []}
    for key, val in values.items():
        card = card_map.get(key, {})
        group = card.get("group", "unknown")
        if group in groups:
            groups[group].append(val)

    group_summary: dict[str, float] = {}
    for group, vals in groups.items():
        if vals:
            group_summary[group] = round(sum(vals) / len(vals), 3)

    # Build narrative
    parts: list[str] = []

    if language == "tr":
        parts.append("**Beyin Aktivasyon Haritası:**")
    else:
        parts.append("**Brain Activation Map:**")

    # Combinations first
    if detected_combos:
        for combo in detected_combos[:2]:
            parts.append(f"**{combo['label']}**: {combo['text']}")
        parts.append("")

    # Top 5 regions
    active_regions = [r for r in top_regions if r["value"] > 0.5][:5]
    if active_regions:
        if language == "tr":
            parts.append("**En aktif bölgeler:**")
        else:
            parts.append("**Most active regions:**")
        for r in active_regions:
            fn_str = ", ".join(r["functions"])
            parts.append(f"- **{r['abbreviation']}** ({r['polarity']}): {r['text']} [{fn_str}]")

    # Group balance
    parts.append("")
    if language == "tr":
        parts.append(f"**Grup dengesi**: Kortikal={group_summary.get('cortical', 0):.2f}, "
                     f"Subkortikal={group_summary.get('subcortical', 0):.2f}, "
                     f"Beyin sapı={group_summary.get('brainstem', 0):.2f}")
    else:
        parts.append(f"**Group balance**: Cortical={group_summary.get('cortical', 0):.2f}, "
                     f"Subcortical={group_summary.get('subcortical', 0):.2f}, "
                     f"Brainstem={group_summary.get('brainstem', 0):.2f}")

    highlights = [c["label"] for c in detected_combos[:2]]
    if not highlights:
        highlights = [f"{r['abbreviation']}: {r['polarity']}" for r in active_regions[:3]]

    return {
        "narrative": "\n".join(parts),
        "highlights": highlights,
        "top_regions": top_regions,
        "combinations": detected_combos,
        "group_summary": group_summary,
    }
