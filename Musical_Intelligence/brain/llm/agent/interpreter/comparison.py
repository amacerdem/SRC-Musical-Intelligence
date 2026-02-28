"""Track Comparison Interpreter — rich comparative narrative.

Compares two tracks across dimensions, neurochemicals, functions,
and gene profiles to produce experiential, "why", "how", and
"who for" narratives.
"""

from __future__ import annotations

from typing import Any

from .polarity import polarity_label
from .dimensions import interpret_6d
from .neurochemicals import interpret_neurochemicals
from .functions import interpret_functions
from .genes import interpret_genes, GENE_FAMILY

# ── Comparison Helpers ──────────────────────────────────────────


def _delta_narrative(
    key: str,
    name: str,
    val_a: float,
    val_b: float,
    language: str = "en",
) -> str | None:
    """Generate a single-line comparison for a dimension/metric."""
    delta = val_b - val_a
    if abs(delta) < 0.08:
        return None

    if language == "tr":
        if delta > 0.2:
            return f"{name}: B çok daha yüksek (+{delta:.2f})"
        elif delta > 0:
            return f"{name}: B daha yüksek (+{delta:.2f})"
        elif delta < -0.2:
            return f"{name}: A çok daha yüksek ({delta:.2f})"
        else:
            return f"{name}: A daha yüksek ({delta:.2f})"
    else:
        if delta > 0.2:
            return f"{name}: B much higher (+{delta:.2f})"
        elif delta > 0:
            return f"{name}: B higher (+{delta:.2f})"
        elif delta < -0.2:
            return f"{name}: A much higher ({delta:.2f})"
        else:
            return f"{name}: A higher ({delta:.2f})"


# ── Main Comparison ─────────────────────────────────────────────


def interpret_comparison(
    track_a: dict[str, Any],
    track_b: dict[str, Any],
    tier: str = "free",
    language: str = "tr",
    user_genes: dict[str, float] | None = None,
    persona_family: str | None = None,
) -> dict[str, Any]:
    """Compare two tracks with multi-layer narrative.

    Args:
        track_a: First track analysis dict.
        track_b: Second track analysis dict.
        tier: user tier
        language: "tr" or "en"
        user_genes: Optional user gene profile.
        persona_family: Optional user persona family.

    Returns:
        Dict with "narrative", "highlights", "dimension_deltas",
        "neurochemical_deltas", "function_deltas", "gene_comparison".
    """
    sfx = "tr" if language == "tr" else "en"

    parts: list[str] = []
    highlights: list[str] = []

    # Track identifiers
    a_name = f"{track_a.get('artist', '?')} — {track_a.get('title', '?')}"
    b_name = f"{track_b.get('artist', '?')} — {track_b.get('title', '?')}"

    if language == "tr":
        parts.append(f"**Karşılaştırma**: {a_name} vs {b_name}")
    else:
        parts.append(f"**Comparison**: {a_name} vs {b_name}")

    # ── 6D Dimension Deltas ─────────────────────────────────────
    dims_a = track_a.get("dimensions", {}).get("psychology_6d", {})
    dims_b = track_b.get("dimensions", {}).get("psychology_6d", {})

    dim_names = {
        "en": {"discovery": "Discovery", "intensity": "Intensity", "flow": "Flow",
               "depth": "Depth", "trace": "Trace", "sharing": "Sharing"},
        "tr": {"discovery": "Keşif", "intensity": "Gerilim", "flow": "Ritim",
               "depth": "Duygu", "trace": "Hafıza", "sharing": "Bağ"},
    }

    dimension_deltas: list[dict] = []
    if isinstance(dims_a, dict) and isinstance(dims_b, dict):
        parts.append("")
        if language == "tr":
            parts.append("**Deneyimsel fark (6D):**")
        else:
            parts.append("**Experiential difference (6D):**")

        for key in ["discovery", "intensity", "flow", "depth", "trace", "sharing"]:
            va = dims_a.get(key, 0.5) if isinstance(dims_a, dict) else 0.5
            vb = dims_b.get(key, 0.5) if isinstance(dims_b, dict) else 0.5
            name = dim_names.get(language, dim_names["en"]).get(key, key)
            line = _delta_narrative(key, name, va, vb, language)
            dimension_deltas.append({"key": key, "name": name, "a": round(va, 3), "b": round(vb, 3), "delta": round(vb - va, 3)})
            if line:
                parts.append(f"- {line}")
    elif isinstance(dims_a, list) and isinstance(dims_b, list):
        dim_keys = ["discovery", "intensity", "flow", "depth", "trace", "sharing"]
        parts.append("")
        if language == "tr":
            parts.append("**Deneyimsel fark (6D):**")
        else:
            parts.append("**Experiential difference (6D):**")
        for i, key in enumerate(dim_keys):
            va = dims_a[i] if i < len(dims_a) else 0.5
            vb = dims_b[i] if i < len(dims_b) else 0.5
            name = dim_names.get(language, dim_names["en"]).get(key, key)
            line = _delta_narrative(key, name, va, vb, language)
            dimension_deltas.append({"key": key, "name": name, "a": round(va, 3), "b": round(vb, 3), "delta": round(vb - va, 3)})
            if line:
                parts.append(f"- {line}")

    # Biggest delta highlight
    if dimension_deltas:
        biggest = max(dimension_deltas, key=lambda d: abs(d["delta"]))
        if abs(biggest["delta"]) > 0.1:
            if language == "tr":
                highlights.append(f"En büyük fark: {biggest['name']} ({biggest['delta']:+.2f})")
            else:
                highlights.append(f"Biggest difference: {biggest['name']} ({biggest['delta']:+.2f})")

    # ── Neurochemical Deltas ────────────────────────────────────
    neuro_a = track_a.get("neuro_4d", {})
    neuro_b = track_b.get("neuro_4d", {})
    neurochemical_deltas: list[dict] = []

    if neuro_a and neuro_b:
        parts.append("")
        if language == "tr":
            parts.append("**Nörokimyasal fark (neden):**")
        else:
            parts.append("**Neurochemical difference (why):**")

        neuro_names = {"DA": "Dopamine", "NE": "Norepinephrine", "OPI": "Opioid", "5HT": "Serotonin"}
        for key in ["DA", "NE", "OPI", "5HT"]:
            va = neuro_a.get(key, 0.5)
            vb = neuro_b.get(key, 0.5)
            line = _delta_narrative(key, neuro_names.get(key, key), va, vb, language)
            neurochemical_deltas.append({"key": key, "a": round(va, 3), "b": round(vb, 3), "delta": round(vb - va, 3)})
            if line:
                parts.append(f"- {line}")

    # ── Function Deltas ─────────────────────────────────────────
    fn_a = track_a.get("functions", {})
    fn_b = track_b.get("functions", {})
    function_deltas: list[dict] = []

    if fn_a and fn_b:
        fn_names_en = {
            "F1": "Sensory", "F2": "Prediction", "F3": "Attention",
            "F4": "Memory", "F5": "Emotion", "F6": "Reward",
            "F7": "Motor", "F8": "Learning", "F9": "Social",
        }
        fn_names_tr = {
            "F1": "Duyusal", "F2": "Tahmin", "F3": "Dikkat",
            "F4": "Hafıza", "F5": "Duygu", "F6": "Ödül",
            "F7": "Motor", "F8": "Öğrenme", "F9": "Sosyal",
        }
        fn_names = fn_names_tr if language == "tr" else fn_names_en

        notable_fn: list[str] = []
        for key in ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9"]:
            va = fn_a.get(key, 0.5)
            vb = fn_b.get(key, 0.5)
            function_deltas.append({"key": key, "name": fn_names.get(key, key), "a": round(va, 3), "b": round(vb, 3), "delta": round(vb - va, 3)})
            line = _delta_narrative(key, fn_names.get(key, key), va, vb, language)
            if line:
                notable_fn.append(line)

        if notable_fn:
            parts.append("")
            if language == "tr":
                parts.append("**Fonksiyonel fark (nasıl):**")
            else:
                parts.append("**Functional difference (how):**")
            for line in notable_fn[:4]:
                parts.append(f"- {line}")

    # ── Gene Comparison ─────────────────────────────────────────
    genes_a = track_a.get("genes", {})
    genes_b = track_b.get("genes", {})
    gene_comparison: dict[str, Any] = {}

    if genes_a and genes_b:
        dom_a = track_a.get("dominant_gene", "")
        dom_b = track_b.get("dominant_gene", "")
        fam_a = track_a.get("dominant_family", "")
        fam_b = track_b.get("dominant_family", "")

        if dom_a != dom_b:
            parts.append("")
            if language == "tr":
                parts.append(f"**Kim için**: A → {fam_a} dinleyicileri, B → {fam_b} dinleyicileri")
            else:
                parts.append(f"**Who for**: A → {fam_a} listeners, B → {fam_b} listeners")
            highlights.append(f"A={fam_a}, B={fam_b}")

        gene_comparison = {
            "dominant_gene_a": dom_a,
            "dominant_gene_b": dom_b,
            "family_a": fam_a,
            "family_b": fam_b,
        }

    return {
        "narrative": "\n".join(parts),
        "highlights": highlights[:5],
        "dimension_deltas": dimension_deltas,
        "neurochemical_deltas": neurochemical_deltas,
        "function_deltas": function_deltas,
        "gene_comparison": gene_comparison,
    }
