"""Gene Profile Interpreter — musical gene matching and persona alignment.

5 genes: entropy, resolution, tension, resonance, plasticity
5 families: Explorers, Architects, Alchemists, Anchors, Kineticists
"""

from __future__ import annotations

from typing import Any

from .polarity import classify_value, polarity_label

# ── Gene → Family Mapping ───────────────────────────────────────

GENE_FAMILY = {
    "entropy": "Explorers",
    "resolution": "Architects",
    "tension": "Alchemists",
    "resonance": "Anchors",
    "plasticity": "Kineticists",
}

_GENE_INFO: dict[str, dict[str, str]] = {
    "entropy": {
        "name_en": "Entropy",
        "name_tr": "Entropi",
        "high_en": "Seeks novelty, unpredictability, and the unknown. Thrives on musical surprise.",
        "high_tr": "Yenilik, öngörülemezlik ve bilinmeyeni arar. Müzikal sürprizle gelişir.",
        "low_en": "Prefers familiar, predictable structures. Comfort in the known.",
        "low_tr": "Tanıdık, öngörülebilir yapıları tercih eder. Bilinenin konforu.",
    },
    "resolution": {
        "name_en": "Resolution",
        "name_tr": "Çözünürlük",
        "high_en": "Sensitive to detail, fine structure, and harmonic clarity. Hears everything.",
        "high_tr": "Detaya, ince yapıya ve harmonik netliğe duyarlı. Her şeyi duyar.",
        "low_en": "Focuses on big-picture gestures rather than fine detail.",
        "low_tr": "İnce detaydan ziyade büyük-resim hareketlerine odaklanır.",
    },
    "tension": {
        "name_en": "Tension",
        "name_tr": "Gerilim",
        "high_en": "Appetite for harmonic and rhythmic tension. Loves build-ups, dissonance, and drama.",
        "high_tr": "Harmonik ve ritmik gerilime iştah. Birikimleri, disonansı ve dramayı sever.",
        "low_en": "Prefers resolved, consonant, smooth musical surfaces.",
        "low_tr": "Çözülmüş, konsonant, pürüzsüz müzikal yüzeyleri tercih eder.",
    },
    "resonance": {
        "name_en": "Resonance",
        "name_tr": "Rezonans",
        "high_en": "Deep emotional and memory engagement. Music touches the soul.",
        "high_tr": "Derin duygusal ve hafıza bağlanması. Müzik ruha dokunur.",
        "low_en": "Listens more analytically, less emotional immersion.",
        "low_tr": "Daha analitik dinler, daha az duygusal daldırma.",
    },
    "plasticity": {
        "name_en": "Plasticity",
        "name_tr": "Plastisite",
        "high_en": "Strong motor coupling and rhythmic flexibility. Music moves the body.",
        "high_tr": "Güçlü motor bağlanma ve ritmik esneklik. Müzik vücudu hareket ettirir.",
        "low_en": "Less physically responsive. Cerebral listening style.",
        "low_tr": "Daha az fiziksel tepki. Beynsel dinleme stili.",
    },
}


# ── Main Interpreter ─────────────────────────────────────────────


def interpret_genes(
    track_genes: dict[str, float],
    language: str = "tr",
    user_genes: dict[str, float] | None = None,
    user_persona_family: str | None = None,
) -> dict[str, Any]:
    """Interpret track gene profile and match against user.

    Args:
        track_genes: {entropy, resolution, tension, resonance, plasticity} → float
        language: "tr" or "en"
        user_genes: Optional user's gene profile for matching.
        user_persona_family: Optional user's persona family.

    Returns:
        Dict with "narrative", "highlights", "dominant_gene",
        "profile", "match_note".
    """
    sfx = "tr" if language == "tr" else "en"

    # Find dominant gene
    sorted_genes = sorted(track_genes.items(), key=lambda x: x[1], reverse=True)
    dominant_gene = sorted_genes[0][0] if sorted_genes else ""
    dominant_family = GENE_FAMILY.get(dominant_gene, "")

    # Profile description
    profile: list[dict] = []
    for gene, value in sorted_genes:
        info = _GENE_INFO.get(gene, {})
        pol = classify_value(value)
        if pol in ("very_high", "high"):
            desc = info.get(f"high_{sfx}", "")
        elif pol in ("very_low", "low"):
            desc = info.get(f"low_{sfx}", "")
        else:
            desc = ""

        profile.append({
            "gene": gene,
            "name": info.get(f"name_{sfx}", gene),
            "value": round(value, 3),
            "polarity": polarity_label(value, language),
            "family": GENE_FAMILY.get(gene, ""),
            "text": desc,
        })

    # Build narrative
    parts: list[str] = []

    dom_info = _GENE_INFO.get(dominant_gene, {})
    dom_name = dom_info.get(f"name_{sfx}", dominant_gene)

    if language == "tr":
        parts.append(f"**Baskın gen**: {dom_name} → {dominant_family} ailesi")
        parts.append(dom_info.get(f"high_{sfx}", ""))
    else:
        parts.append(f"**Dominant gene**: {dom_name} → {dominant_family} family")
        parts.append(dom_info.get(f"high_{sfx}", ""))

    # Secondary notable genes
    for gene_info in profile[1:3]:
        if gene_info["value"] > 0.5:
            parts.append(f"- {gene_info['name']}: {gene_info['text']}")

    # User matching
    match_note = ""
    if user_genes:
        parts.append("")

        # Calculate alignment
        alignment = sum(
            1.0 - abs(track_genes.get(g, 0.5) - user_genes.get(g, 0.5))
            for g in GENE_FAMILY
        ) / len(GENE_FAMILY)

        # Strongest match and complement
        deltas = {
            g: track_genes.get(g, 0.5) - user_genes.get(g, 0.5)
            for g in GENE_FAMILY
        }
        match_gene = min(deltas, key=lambda g: abs(deltas[g]))
        complement_gene = max(deltas, key=lambda g: abs(deltas[g]))

        match_info = _GENE_INFO.get(match_gene, {})
        comp_info = _GENE_INFO.get(complement_gene, {})

        if alignment > 0.75:
            if language == "tr":
                match_note = f"Bu parça senin gen profilinle güçlü uyum gösteriyor — özellikle {match_info.get(f'name_{sfx}', match_gene)} geninde."
            else:
                match_note = f"This track shows strong alignment with your gene profile — especially in {match_info.get(f'name_{sfx}', match_gene)}."
        elif alignment > 0.55:
            if language == "tr":
                match_note = f"Kısmi uyum — {match_info.get(f'name_{sfx}', match_gene)} genin eşleşiyor ama {comp_info.get(f'name_{sfx}', complement_gene)} genin farklı bir alan açıyor."
            else:
                match_note = f"Partial alignment — your {match_info.get(f'name_{sfx}', match_gene)} gene matches but {comp_info.get(f'name_{sfx}', complement_gene)} opens a different window."
        else:
            if language == "tr":
                match_note = f"Bu parça senin nöral profilini tamamlıyor — özellikle {comp_info.get(f'name_{sfx}', complement_gene)} geninde yeni bir pencere açıyor."
            else:
                match_note = f"This track complements your neural profile — it opens a new window especially in {comp_info.get(f'name_{sfx}', complement_gene)}."

        parts.append(match_note)

        # Family match note
        if user_persona_family:
            track_family = dominant_family
            if track_family == user_persona_family:
                if language == "tr":
                    parts.append(f"Bu parça sendeki {track_family}'ı konuşturuyor — kendi ailenin müziği.")
                else:
                    parts.append(f"This track speaks to the {track_family} in you — your own family's music.")
            else:
                if language == "tr":
                    parts.append(f"Bu parça {track_family} ailesinin müziği — senin {user_persona_family} profilinin dışında, tamamlayıcı bir deneyim.")
                else:
                    parts.append(f"This track is {track_family} family music — outside your {user_persona_family} profile, a complementary experience.")

    highlights: list[str] = []
    if language == "tr":
        highlights.append(f"Baskın: {dom_name} ({dominant_family})")
    else:
        highlights.append(f"Dominant: {dom_name} ({dominant_family})")
    if match_note:
        highlights.append(match_note[:80])

    return {
        "narrative": "\n".join(parts),
        "highlights": highlights,
        "dominant_gene": dominant_gene,
        "dominant_family": dominant_family,
        "profile": profile,
        "match_note": match_note,
    }
