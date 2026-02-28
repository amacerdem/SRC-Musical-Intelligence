"""MI System Tool Definitions — Claude API tool_use schema.

Defines the tools the Musical Mind agent can call to access
real-time MI analysis data, session history, and knowledge search.

Usage:
    from Musical_Intelligence.brain.llm.agent.tools import TOOLS, handle_tool_call
"""

from __future__ import annotations

from typing import Any

# ── Tool Definitions (Claude API format) ────────────────────────────

TOOLS = [
    {
        "name": "search_tracks",
        "description": (
            "Search the user's music library for tracks by artist name, "
            "song title, or keywords. Returns matching tracks with IDs. "
            "ALWAYS use this first to find a track before calling analyze_track."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Artist name, song title, or keywords to search for",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max results to return (default 10)",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "analyze_track",
        "description": (
            "Get the full MI brain analysis for a specific track — dimensions, "
            "beliefs, functions, neurochemicals, temporal profile. Use when the "
            "user asks about a specific song. Use search_tracks first to find "
            "the track_id."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "track_id": {
                    "type": "string",
                    "description": "Track ID from search_tracks results (e.g. 'tool__lateralus')",
                },
            },
            "required": ["track_id"],
        },
    },
    {
        "name": "get_current_dimensions",
        "description": (
            "Get the user's current 6D/12D/24D dimension values "
            "from a specific track analysis. Use this when "
            "the user asks about their current state or a track's dimensions."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "track_id": {
                    "type": "string",
                    "description": "Track ID to get dimensions for",
                },
                "layer": {
                    "type": "string",
                    "enum": ["6d", "12d", "24d"],
                    "description": "Dimension depth to retrieve",
                },
            },
            "required": ["layer"],
        },
    },
    {
        "name": "get_beliefs",
        "description": (
            "Get specific belief values from a track analysis. "
            "Beliefs are the 131 neural computations the C³ brain performs. "
            "Can request specific belief keys or get the most notable ones."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "track_id": {
                    "type": "string",
                    "description": "Track ID to get beliefs for",
                },
                "belief_keys": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "Specific belief keys (e.g. ['wanting', 'harmonic_stability', "
                        "'beat_entrainment']). If omitted, returns top 15 most notable."
                    ),
                },
            },
        },
    },
    {
        "name": "compare_tracks",
        "description": (
            "Compare the MI analysis of two tracks — show dimension and "
            "belief differences. Use when the user asks 'what's the difference "
            "between these songs?' or 'how do they compare?'"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "track_a": {
                    "type": "string",
                    "description": "First track ID",
                },
                "track_b": {
                    "type": "string",
                    "description": "Second track ID",
                },
            },
            "required": ["track_a", "track_b"],
        },
    },
    {
        "name": "search_knowledge",
        "description": (
            "Search the M³ knowledge base for concepts, beliefs, "
            "literature findings, or mechanism explanations. Use when "
            "the user asks 'what is X?' or 'how does Y work?'"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query in natural language",
                },
                "collection": {
                    "type": "string",
                    "enum": ["knowledge_cards", "literature_c3", "literature_c0", "mechanisms"],
                    "description": "Which collection to search (default: knowledge_cards)",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_persona_info",
        "description": (
            "Get detailed information about a persona — its traits, "
            "conversation style, dimension profile, shadow/growth area. "
            "Use when the user asks about their persona or a specific persona type."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "persona_id": {
                    "type": "integer",
                    "description": "Persona ID (1-24)",
                },
                "persona_name": {
                    "type": "string",
                    "description": "Persona name (alternative to ID)",
                },
            },
        },
    },
    {
        "name": "get_temporal_journey",
        "description": (
            "Get the temporal arc of a track — how the listening experience "
            "evolves across 8 segments. Shows mood transitions, turning points, "
            "and key belief changes over time. Use when asking 'what's the "
            "journey of this song?' or 'how does the experience change?'"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "track_id": {
                    "type": "string",
                    "description": "Track ID to analyze temporally",
                },
                "focus_beliefs": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "Optional belief keys to focus on "
                        "(e.g. ['wanting', 'pleasure', 'harmonic_stability'])"
                    ),
                },
            },
            "required": ["track_id"],
        },
    },
    {
        "name": "get_brain_activation",
        "description": (
            "Get the brain region activation map (RAM 26D) for a track — "
            "which brain areas are most engaged and what that means. "
            "Shows cortical, subcortical, and brainstem activations. "
            "Premium tier and above only."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "track_id": {
                    "type": "string",
                    "description": "Track ID to get brain activation for",
                },
            },
            "required": ["track_id"],
        },
    },
]


# ── Tool Call Handler ───────────────────────────────────────────────


def handle_tool_call(
    tool_name: str,
    tool_input: dict[str, Any],
    user_tier: str = "free",
) -> dict[str, Any]:
    """Route a tool call to the appropriate handler.

    Args:
        tool_name: Name of the tool being called.
        tool_input: Input parameters from the LLM.
        user_tier: User's subscription tier for access control.

    Returns:
        Tool result dict to feed back to the LLM.
    """
    handlers = {
        "search_tracks": _handle_search_tracks,
        "analyze_track": _handle_analyze_track,
        "get_current_dimensions": _handle_get_dimensions,
        "get_beliefs": _handle_get_beliefs,
        "compare_tracks": _handle_compare_tracks,
        "search_knowledge": _handle_search_knowledge,
        "get_persona_info": _handle_get_persona,
        "get_temporal_journey": _handle_temporal_journey,
        "get_brain_activation": _handle_brain_activation,
    }

    handler = handlers.get(tool_name)
    if not handler:
        return {"error": f"Unknown tool: {tool_name}"}

    return handler(tool_input, user_tier)


# ── Track Data Handlers ────────────────────────────────────────────


def _handle_search_tracks(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Search the user's track library."""
    from .track_data import list_tracks, search_tracks

    query = inputs.get("query", "")
    limit = inputs.get("limit", 10)

    if not query:
        tracks = list_tracks()
        return {"tracks": tracks[:limit], "total": len(tracks)}

    results = search_tracks(query, limit=limit)
    if not results:
        return {
            "results": [],
            "message": f"No tracks found matching '{query}'. Try a different search term.",
        }
    return {"results": results, "count": len(results)}


def _handle_analyze_track(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Get full MI analysis for a track."""
    from .track_data import format_track_for_llm, load_track, search_tracks

    track_id = inputs.get("track_id", "")
    if not track_id:
        return {"error": "track_id is required. Use search_tracks first to find it."}

    track = load_track(track_id)

    # If exact ID not found, try fuzzy search
    if not track:
        results = search_tracks(track_id, limit=1)
        if results:
            track = load_track(results[0]["id"])

    if not track:
        return {
            "error": f"Track '{track_id}' not found in the analysis database.",
            "suggestion": "Use search_tracks to find available tracks.",
        }

    result = format_track_for_llm(track, tier=tier)

    # Enrich with interpreter insights
    try:
        from .interpreter import interpret_reward, interpret_genes

        # Reward insight
        signal = track.get("signal", {})
        if signal:
            reward_data = {
                "total": signal.get("reward", signal.get("total_reward", 0.5)),
                "surprise": signal.get("surprise", 0.5),
                "resolution": signal.get("resolution", 0.5),
                "exploration": signal.get("exploration", 0.5),
                "monotony": signal.get("monotony", 0.0),
                "familiarity": signal.get("familiarity", None),
            }
            reward_result = interpret_reward(reward_data, language="en", tier=tier)
            result["reward_insight"] = reward_result.get("narrative", "")

        # Temporal summary
        tp = track.get("temporal_profile", {})
        if tp.get("belief_means_per_segment"):
            from .interpreter import interpret_temporal
            beliefs = track.get("beliefs", {})
            temp_result = interpret_temporal(
                tp, beliefs.get("means", []), beliefs.get("stds", []),
                language="en", tier=tier,
            )
            result["temporal_summary"] = temp_result.get("narrative", "")

        # Gene match note
        genes = track.get("genes", {})
        if genes:
            gene_result = interpret_genes(genes, language="en")
            result["gene_match_note"] = (
                f"Dominant: {gene_result.get('dominant_gene', '')} "
                f"({gene_result.get('dominant_family', '')})"
            )
    except Exception:
        pass  # Interpreter enrichment is best-effort

    return result


def _handle_get_dimensions(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Get dimension values for a track."""
    from .track_data import format_dimensions_for_llm, load_track, search_tracks

    track_id = inputs.get("track_id")
    layer = inputs.get("layer", "6d")

    if layer == "12d" and tier == "free":
        return {"error": "12D dimensions require Basic tier or higher."}
    if layer == "24d" and tier not in ("premium", "research"):
        return {"error": "24D dimensions require Premium tier or higher."}

    if not track_id:
        return {"error": "track_id is required. Use search_tracks to find a track first."}

    track = load_track(track_id)
    if not track:
        results = search_tracks(track_id, limit=1)
        if results:
            track = load_track(results[0]["id"])

    if not track:
        return {"error": f"Track '{track_id}' not found."}

    return format_dimensions_for_llm(track, layer=layer, tier=tier)


def _handle_get_beliefs(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Get belief values for a track."""
    from .track_data import format_beliefs_for_llm, load_track, search_tracks

    track_id = inputs.get("track_id")
    belief_keys = inputs.get("belief_keys")

    if not track_id:
        return {"error": "track_id is required. Use search_tracks to find a track first."}

    track = load_track(track_id)
    if not track:
        results = search_tracks(track_id, limit=1)
        if results:
            track = load_track(results[0]["id"])

    if not track:
        return {"error": f"Track '{track_id}' not found."}

    return format_beliefs_for_llm(track, belief_keys=belief_keys, tier=tier)


def _handle_compare_tracks(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Compare two tracks."""
    from .track_data import DIM_6D, load_track

    track_a_id = inputs.get("track_a", "")
    track_b_id = inputs.get("track_b", "")

    track_a = load_track(track_a_id)
    track_b = load_track(track_b_id)

    if not track_a:
        return {"error": f"Track A '{track_a_id}' not found."}
    if not track_b:
        return {"error": f"Track B '{track_b_id}' not found."}

    result: dict[str, Any] = {
        "track_a": {"artist": track_a["artist"], "title": track_a["title"]},
        "track_b": {"artist": track_b["artist"], "title": track_b["title"]},
    }

    # Compare 6D
    dims_a = track_a.get("dimensions", {}).get("psychology_6d", [])
    dims_b = track_b.get("dimensions", {}).get("psychology_6d", [])
    if dims_a and dims_b:
        deltas = {}
        for i, key in enumerate(DIM_6D):
            if i < len(dims_a) and i < len(dims_b):
                delta = round(dims_b[i] - dims_a[i], 3)
                deltas[key] = {
                    "a": round(dims_a[i], 3),
                    "b": round(dims_b[i], 3),
                    "delta": delta,
                    "direction": "higher" if delta > 0.05 else ("lower" if delta < -0.05 else "similar"),
                }
        result["psychology_6d_comparison"] = deltas

    # Compare functions
    func_a = track_a.get("functions", {})
    func_b = track_b.get("functions", {})
    if func_a and func_b:
        func_deltas = {}
        for f in ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9"]:
            va = func_a.get(f, 0)
            vb = func_b.get(f, 0)
            func_deltas[f] = {
                "a": round(va, 3), "b": round(vb, 3), "delta": round(vb - va, 3),
            }
        result["function_comparison"] = func_deltas

    # Compare neurochemicals
    neuro_a = track_a.get("neuro_4d", {})
    neuro_b = track_b.get("neuro_4d", {})
    if neuro_a and neuro_b:
        neuro_deltas = {}
        for key in ["DA", "NE", "OPI", "5HT"]:
            va = neuro_a.get(key, 0)
            vb = neuro_b.get(key, 0)
            neuro_deltas[key] = {
                "a": round(va, 3), "b": round(vb, 3), "delta": round(vb - va, 3),
            }
        result["neurochemical_comparison"] = neuro_deltas

    # Enrich with comparison narrative from interpreter
    try:
        from .interpreter import interpret_comparison as _interp_comp

        comp_result = _interp_comp(track_a, track_b, tier=tier, language="en")
        result["comparison_narrative"] = comp_result.get("narrative", "")
        result["comparison_highlights"] = comp_result.get("highlights", [])
    except Exception:
        pass  # Enrichment is best-effort

    return result


# ── Temporal & Brain Activation Handlers ─────────────────────────


def _handle_temporal_journey(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Get temporal arc for a track."""
    from .track_data import load_track, search_tracks
    from .interpreter import interpret_temporal

    track_id = inputs.get("track_id", "")
    focus_beliefs = inputs.get("focus_beliefs")

    if not track_id:
        return {"error": "track_id is required."}

    track = load_track(track_id)
    if not track:
        results = search_tracks(track_id, limit=1)
        if results:
            track = load_track(results[0]["id"])

    if not track:
        return {"error": f"Track '{track_id}' not found."}

    tp = track.get("temporal_profile", {})
    if not tp.get("belief_means_per_segment"):
        return {
            "track_id": track_id,
            "message": "No temporal profile available for this track.",
        }

    beliefs = track.get("beliefs", {})
    result = interpret_temporal(
        tp,
        beliefs.get("means", []),
        beliefs.get("stds", []),
        language="en",
        tier=tier,
        focus_beliefs=focus_beliefs,
    )
    result["track_id"] = track_id
    result["artist"] = track.get("artist", "")
    result["title"] = track.get("title", "")
    return result


def _handle_brain_activation(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Get brain region activation map for a track."""
    from .track_data import load_track, search_tracks
    from .interpreter import interpret_brain_regions

    if tier not in ("premium", "research"):
        return {"error": "Brain activation map requires Premium tier or higher."}

    track_id = inputs.get("track_id", "")
    if not track_id:
        return {"error": "track_id is required."}

    track = load_track(track_id)
    if not track:
        results = search_tracks(track_id, limit=1)
        if results:
            track = load_track(results[0]["id"])

    if not track:
        return {"error": f"Track '{track_id}' not found."}

    ram = track.get("ram_26d")
    if not ram:
        return {
            "track_id": track_id,
            "message": "No brain activation data available for this track.",
        }

    result = interpret_brain_regions(ram, language="en", tier=tier)
    result["track_id"] = track_id
    result["artist"] = track.get("artist", "")
    result["title"] = track.get("title", "")
    return result


# ── Knowledge & Persona Handlers ──────────────────────────────────


def _handle_search_knowledge(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Search knowledge base via RAG retriever."""
    import os

    query = inputs.get("query", "")
    collection = inputs.get("collection", "knowledge_cards")

    if not query:
        return {"error": "Query is required."}

    use_local = not bool(os.environ.get("OPENAI_API_KEY"))

    try:
        from Musical_Intelligence.brain.llm.rag.retriever import retrieve

        results = retrieve(
            query=query,
            user_tier=tier,
            collections=[collection],
            top_k=5,
            use_local_embeddings=use_local,
        )
        return {
            "results": [
                {
                    "text": r.text[:500],
                    "doc_type": r.doc_type,
                    "score": round(r.score, 3),
                    "source": r.source_file,
                }
                for r in results
            ],
            "count": len(results),
        }
    except Exception as e:
        return {"error": f"RAG not initialized: {e}"}


def _handle_get_persona(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Look up persona info from knowledge cards."""
    import json
    from Musical_Intelligence.brain.llm.config import KNOWLEDGE_DIR

    persona_id = inputs.get("persona_id")
    persona_name = inputs.get("persona_name", "").lower()

    path = KNOWLEDGE_DIR / "personas.jsonl"
    for line in path.read_text(encoding="utf-8").strip().splitlines():
        card = json.loads(line)
        if persona_id and card.get("id") == persona_id:
            return card
        if persona_name and card.get("name", "").lower() == persona_name:
            return card

    return {"error": f"Persona not found: id={persona_id}, name={persona_name}"}
