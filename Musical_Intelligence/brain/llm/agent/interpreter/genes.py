"""Gene Profile Interpreter — musical gene matching and persona alignment.

6 genes: energy, valence, tempo, tension, groove, density
5 families: Explorers, Architects, Alchemists, Anchors, Kineticists
"""

from __future__ import annotations

from typing import Any

from .polarity import classify_value, polarity_label

# ── Gene → Family Mapping ───────────────────────────────────────

GENE_FAMILY = {
    "energy": "Explorers",
    "valence": "Anchors",
    "tempo": "Kineticists",
    "tension": "Alchemists",
    "groove": "Kineticists",
    "density": "Architects",
}

_GENE_INFO: dict[str, dict[str, str]] = {
    "energy": {
        "name_en": "Energy",
        "name_tr": "Enerji",
        "high_en": "Drawn to intense, powerful, driving music. High arousal and sonic force.",
        "high_tr": "Yoğun, güçlü, sürükleyici müziğe çekilir. Yüksek uyarılma ve sonik güç.",
        "low_en": "Prefers quiet, calm, gentle musical landscapes.",
        "low_tr": "Sessiz, sakin, yumuşak müzikal manzaraları tercih eder.",
    },
    "valence": {
        "name_en": "Valence",
        "name_tr": "Valans",
        "high_en": "Gravitates toward happy, uplifting, bright music. Emotional positivity.",
        "high_tr": "Mutlu, yükseltici, parlak müziğe yönelir. Duygusal pozitiflik.",
        "low_en": "Drawn to sad, dark, melancholic tones. Emotional depth through shadow.",
        "low_tr": "Hüzünlü, karanlık, melankolik tonlara çekilir. Gölge yoluyla duygusal derinlik.",
    },
    "tempo": {
        "name_en": "Tempo",
        "name_tr": "Tempo",
        "high_en": "Loves fast, energetic pacing. Thrives on speed and momentum.",
        "high_tr": "Hızlı, enerjik tempoya bayılır. Hız ve ivmeden beslenip gelişir.",
        "low_en": "Prefers slow, spacious, unhurried musical flow.",
        "low_tr": "Yavaş, geniş, acele etmeyen müzikal akışı tercih eder.",
    },
    "tension": {
        "name_en": "Tension",
        "name_tr": "Gerilim",
        "high_en": "Appetite for dissonance, suspense, and dark energy. Loves build-ups and drama.",
        "high_tr": "Disonans, gerilim ve karanlık enerjiye iştah. Birikimleri ve dramayı sever.",
        "low_en": "Prefers consonance, resolution, and smooth musical surfaces.",
        "low_tr": "Konsonans, çözünürlük ve pürüzsüz müzikal yüzeyleri tercih eder.",
    },
    "groove": {
        "name_en": "Groove",
        "name_tr": "Groove",
        "high_en": "Strong rhythmic and motor engagement. Music moves the body. Dance-oriented.",
        "high_tr": "Güçlü ritmik ve motor bağlanma. Müzik vücudu hareket ettirir. Dans odaklı.",
        "low_en": "Cerebral listening style. Less physically responsive to rhythm.",
        "low_tr": "Beynsel dinleme stili. Ritme daha az fiziksel tepki.",
    },
    "density": {
        "name_en": "Density",
        "name_tr": "Yoğunluk",
        "high_en": "Loves layered, intricate arrangements. Drawn to structural complexity.",
        "high_tr": "Katmanlı, karmaşık düzenlemelere bayılır. Yapısal karmaşıklığa çekilir.",
        "low_en": "Prefers minimal, simple textures. Clarity over complexity.",
        "low_tr": "Minimal, basit dokuları tercih eder. Karmaşıklık yerine netlik.",
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
        track_genes: {energy, valence, tempo, tension, groove, density} → float
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
