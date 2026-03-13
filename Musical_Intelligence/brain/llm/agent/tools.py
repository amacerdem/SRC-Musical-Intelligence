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
        "name": "get_listening_profile",
        "description": (
            "Get statistics about the MI music catalog — category distribution, "
            "family breakdown, and average gene profile across available tracks. "
            "NOTE: This is the MI reference catalog (not the user's personal library). "
            "For the user's personal listening profile, use get_spotify_listening_profile instead. "
            "Use this tool when you need catalog overview or want to find tracks by category."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "search_tracks",
        "description": (
            "Search the user's music library for tracks by artist name, "
            "song title, or keywords. Returns matching tracks with IDs and "
            "gene/family info. For mood-based searches, include gene-related terms "
            "(e.g., 'high tension' → intense tracks, 'groovy' → groove tracks). "
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
        "name": "get_belief_timeline",
        "description": (
            "Get frame-level belief trajectories for a track — downsampled to 16 "
            "time points with peak/valley moments and timestamps. Use this when "
            "the user asks about specific moments in a song, how a belief changes "
            "over time, or wants a detailed temporal story of the listening experience. "
            "Much more precise than get_temporal_journey — uses frame-level data "
            "(~5ms resolution) instead of segment averages."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "track_id": {
                    "type": "string",
                    "description": "Track ID to get timeline for",
                },
                "belief_keys": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "Specific belief keys to track over time "
                        "(e.g. ['wanting', 'harmonic_stability', 'beat_entrainment']). "
                        "If omitted, returns top 10 most notable beliefs."
                    ),
                },
                "n_points": {
                    "type": "integer",
                    "description": "Number of timeline points (default 16, max 32)",
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
    # ── Music Control Tools (frontend-executed actions) ────────────
    {
        "name": "play_track",
        "description": (
            "Play a specific track IMMEDIATELY. Search by name/artist keywords or "
            "provide a direct track_id. Returns an action for the frontend to execute, "
            "along with the track's MI analysis (6D dimensions, genes, top beliefs). "
            "IMPORTANT: When the user asks to play music, suggest a song, or says "
            "'play something' — call this tool DIRECTLY without asking questions. "
            "Consider the user's genes, persona, and current dimensions when choosing. "
            "After playing, explain your choice referencing MI data (gene alignment, "
            "dimension match, belief patterns)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Track name, artist, or search keywords",
                },
                "track_id": {
                    "type": "string",
                    "description": "Direct track ID if already known from search_tracks",
                },
            },
        },
    },
    {
        "name": "queue_tracks",
        "description": (
            "Queue multiple tracks (5-10) to play in sequence. Use this when "
            "the user asks for a playlist, queue, or multiple songs. Accepts a "
            "list of queries or track_ids. Returns actions for the frontend with "
            "MI data per track (6D dimensions, gene match). Build thematic queues "
            "with a narrative arc (e.g., start calm → build tension → climax → "
            "resolve). After calling, explain the energy/gene progression of the queue."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "tracks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Track name, artist, or search keywords",
                            },
                            "track_id": {
                                "type": "string",
                                "description": "Direct track ID if already known",
                            },
                        },
                    },
                    "description": "List of tracks to queue (5-10 items)",
                    "minItems": 1,
                    "maxItems": 15,
                },
            },
            "required": ["tracks"],
        },
    },
    {
        "name": "control_playback",
        "description": (
            "Control music playback: pause, resume, skip to next/previous track, "
            "adjust volume, toggle shuffle, cycle repeat mode. Use when the user "
            "says 'pause', 'stop', 'next', 'skip', 'louder', 'quieter', 'shuffle', "
            "'repeat', 'durdur', 'sonraki', 'önceki', 'sesini aç/kıs'."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "enum": [
                        "pause", "resume", "next", "previous",
                        "volume_up", "volume_down",
                        "shuffle_toggle", "repeat_cycle",
                    ],
                    "description": "Playback command to execute",
                },
                "value": {
                    "type": "number",
                    "description": "Optional numeric value (e.g. volume percentage 0-100)",
                },
            },
            "required": ["command"],
        },
    },
    {
        "name": "get_now_playing",
        "description": (
            "Get information about the currently playing track — title, artist, "
            "progress, features, family, genre. Use when the user asks 'what's "
            "playing?', 'ne çalıyor?', or when you need context about the "
            "current track before making a comment or recommendation."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "get_spotify_listening_profile",
        "description": (
            "Get the connected user's Spotify listening profile with MI analysis. "
            "Returns their gene profile derived from real Spotify data, top genres, "
            "family distribution across their library, listening diversity metrics "
            "(genre entropy, artist entropy, tempo range), and taste evolution over time. "
            "Use this when you want to understand the user's real musical identity, "
            "comment on their listening patterns, or personalize deep recommendations. "
            "Only available if the user connected their Spotify account."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "recommend_tracks",
        "description": (
            "Get personalized track recommendations based on the user's gene "
            "profile and optional mood filter. Returns top-matching tracks scored "
            "by gene alignment. Use when the user says 'recommend something', "
            "'suggest music', 'what should I listen to?', 'bana bir şey öner', "
            "'ne dinlemeliyim?'. Can filter by mood: energetic, calm, emotional, "
            "groovy, complex, intense, surprising."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "mood": {
                    "type": "string",
                    "description": (
                        "Optional mood filter: energetic, calm, emotional, groovy, "
                        "complex, intense, surprising, nostalgic"
                    ),
                },
                "count": {
                    "type": "integer",
                    "description": "Number of recommendations (default 5, max 10)",
                },
                "exclude_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Track IDs to exclude (e.g., recently played)",
                },
            },
        },
    },
    {
        "name": "fetch_spotify_link",
        "description": (
            "Fetch and analyze tracks from a Spotify URL (album, playlist, or single track). "
            "When the user shares a Spotify link like 'https://open.spotify.com/album/...', "
            "call this tool to fetch all tracks and compute MI gene profiles for each. "
            "Returns track list with 6D genes, dominant family/gene, and aggregate averages. "
            "Works without user Spotify login — uses app-level API access. "
            "ALWAYS call this tool when you see a Spotify URL in the user's message."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "Spotify URL (album, playlist, or track link)",
                },
            },
            "required": ["url"],
        },
    },
]


# ── Tool Call Handler ───────────────────────────────────────────────


def handle_tool_call(
    tool_name: str,
    tool_input: dict[str, Any],
    user_tier: str = "free",
    user_genes: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Route a tool call to the appropriate handler.

    Args:
        tool_name: Name of the tool being called.
        tool_input: Input parameters from the LLM.
        user_tier: User's subscription tier for access control.
        user_genes: User's 6-gene profile for match scoring.

    Returns:
        Tool result dict to feed back to the LLM.
    """
    handlers = {
        "get_listening_profile": _handle_listening_profile,
        "get_spotify_listening_profile": _handle_spotify_listening_profile,
        "fetch_spotify_link": _handle_fetch_spotify_link,
        "search_tracks": _handle_search_tracks,
        "analyze_track": _handle_analyze_track,
        "get_current_dimensions": _handle_get_dimensions,
        "get_beliefs": _handle_get_beliefs,
        "compare_tracks": _handle_compare_tracks,
        "search_knowledge": _handle_search_knowledge,
        "get_persona_info": _handle_get_persona,
        "get_temporal_journey": _handle_temporal_journey,
        "get_belief_timeline": _handle_belief_timeline,
        "get_brain_activation": _handle_brain_activation,
        "play_track": _handle_play_track,
        "queue_tracks": _handle_queue_tracks,
        "control_playback": _handle_control_playback,
        "get_now_playing": _handle_get_now_playing,
        "recommend_tracks": _handle_recommend_tracks,
    }

    handler = handlers.get(tool_name)
    if not handler:
        return {"error": f"Unknown tool: {tool_name}"}

    # Pass user_genes to handlers that use it
    if tool_name in ("play_track", "queue_tracks", "recommend_tracks"):
        return handler(tool_input, user_tier, user_genes=user_genes)
    return handler(tool_input, user_tier)


# ── Listening Profile Handler ──────────────────────────────────────


def _handle_listening_profile(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Get user's listening profile."""
    from .track_data import get_listening_profile

    return get_listening_profile()


# ── Spotify Listening Profile Handler ─────────────────────────────

# Thread-local storage for per-request spotify profile injection
_spotify_profile_store: dict[str, Any] = {}


def set_spotify_profile(profile: dict[str, Any] | None) -> None:
    """Inject Spotify profile for the current request (called by router)."""
    _spotify_profile_store.clear()
    if profile:
        _spotify_profile_store.update(profile)


def _handle_spotify_listening_profile(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Get user's Spotify-derived MI listening profile."""
    if not _spotify_profile_store:
        return {
            "error": "No Spotify profile available. The user has not connected their Spotify account.",
            "suggestion": "Ask the user to connect their Spotify account or share a playlist link.",
        }

    sp = _spotify_profile_store
    result: dict[str, Any] = {
        "source": "spotify",
        "stats": {
            "total_tracks": sp.get("total_tracks", 0),
            "total_minutes": sp.get("total_minutes", 0),
            "artist_count": sp.get("artist_count", 0),
        },
        "top_genres": sp.get("top_genres", []),
        "genre_diversity": sp.get("genre_diversity", 0),
        "family_distribution": sp.get("family_distribution", {}),
        "taste_shift": sp.get("taste_shift", 0),
    }

    return result


# ── Spotify Link Fetch Handler ───────────────────────────────────────

# Per-request store for Spotify link fetch results (set by router)
_spotify_fetch_store: dict[str, Any] = {}


def set_spotify_fetch_result(result: dict[str, Any] | None) -> None:
    """Inject Spotify link fetch result for the current request (called by router)."""
    _spotify_fetch_store.clear()
    if result:
        _spotify_fetch_store.update(result)


def _handle_fetch_spotify_link(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Fetch and analyze tracks from a Spotify URL."""
    url = inputs.get("url", "")
    if not url:
        return {"error": "A Spotify URL is required."}

    # If the router already fetched this URL, return cached result
    if _spotify_fetch_store and _spotify_fetch_store.get("_url") == url:
        result = dict(_spotify_fetch_store)
        result.pop("_url", None)
        return result

    # Otherwise, tell the router to fetch it (deferred execution)
    return {
        "_action": "fetch_spotify_link",
        "_url": url,
        "status": "pending",
        "message": "Spotify link fetch will be handled by the backend router.",
    }


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
                delta = round(dims_b[i] - dims_a[i], 2)
                deltas[key] = {
                    "a": round(dims_a[i], 2),
                    "b": round(dims_b[i], 2),
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


def _handle_belief_timeline(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Get frame-level belief trajectories for a track."""
    from .track_data import get_belief_timeline, search_tracks

    track_id = inputs.get("track_id", "")
    if not track_id:
        return {"error": "track_id is required."}

    belief_keys = inputs.get("belief_keys")
    n_points = min(inputs.get("n_points", 16), 32)

    result = get_belief_timeline(track_id, belief_keys=belief_keys, n_points=n_points)
    if "error" in result:
        # Try fuzzy search fallback
        results = search_tracks(track_id, limit=1)
        if results:
            result = get_belief_timeline(
                results[0]["id"], belief_keys=belief_keys, n_points=n_points,
            )

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


# ── Music Control Helpers ─────────────────────────────────────────


def _gene_match_score(
    user_genes: dict[str, float] | None,
    track_genes: dict[str, float],
) -> float | None:
    """Cosine similarity between user and track gene profiles (0-1)."""
    if not user_genes or not track_genes:
        return None
    keys = ["energy", "valence", "tempo", "tension", "groove", "density"]
    u = [user_genes.get(k, 0.5) for k in keys]
    t = [track_genes.get(k, 0.5) for k in keys]
    dot = sum(a * b for a, b in zip(u, t))
    mag_u = sum(a * a for a in u) ** 0.5
    mag_t = sum(a * a for a in t) ** 0.5
    if mag_u == 0 or mag_t == 0:
        return 0.0
    return round(dot / (mag_u * mag_t), 3)


def _enrich_track_info(
    track: dict[str, Any],
    user_genes: dict[str, float] | None = None,
    include_beliefs: bool = True,
) -> dict[str, Any]:
    """Build enriched track info with MI data for tool results."""
    from .track_data import DIM_6D, _named_dims, _top_beliefs

    info: dict[str, Any] = {
        "title": track.get("title"),
        "artist": track.get("artist"),
        "duration_s": track.get("duration_s"),
        "dominant_family": track.get("dominant_family"),
        "dominant_gene": track.get("dominant_gene"),
        "genre": (
            track.get("categories", ["Unknown"])[0]
            if track.get("categories")
            else "Unknown"
        ),
    }

    # 6D dimensions
    dims = track.get("dimensions", {})
    if "psychology_6d" in dims:
        info["dimensions_6d"] = _named_dims(dims["psychology_6d"], DIM_6D)

    # Gene profile + match score
    genes = track.get("genes", {})
    if genes:
        info["genes"] = {k: round(v, 2) for k, v in genes.items()}
        match = _gene_match_score(user_genes, genes)
        if match is not None:
            info["gene_match"] = match

    # Top notable beliefs (compact)
    if include_beliefs:
        beliefs = track.get("beliefs", {})
        means = beliefs.get("means", [])
        stds = beliefs.get("stds", [])
        if means and stds:
            top = _top_beliefs(means, stds, n=3)
            info["top_beliefs"] = [
                {"key": b["key"], "value": b["value"], "what": b["what"][:80]}
                for b in top
            ]

    return info


# ── Music Control Handlers (frontend-executed actions) ───────────


def _handle_play_track(
    inputs: dict[str, Any],
    tier: str,
    user_genes: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Search for a track and return a play action descriptor with MI data.

    The backend does NOT control playback directly — it returns an
    action dict that the frontend interprets and dispatches to
    SpotifyService or the local AudioPlayer.
    """
    from .track_data import search_tracks, load_track

    track_id = inputs.get("track_id")
    query = inputs.get("query", "")

    if not track_id and not query:
        return {"error": "Provide either query or track_id."}

    # Resolve track
    if not track_id:
        results = search_tracks(query, limit=1)
        if not results:
            return {
                "error": f"No tracks found for '{query}'.",
                "suggestion": "Try a different search term or ask the user for more detail.",
            }
        track_id = results[0]["id"]

    track = load_track(track_id)
    if not track:
        return {"error": f"Track '{track_id}' not found."}

    return {
        "action": {
            "type": "play_track",
            "track_id": track_id,
            "track_name": track.get("title", ""),
            "artist": track.get("artist", ""),
        },
        "track_info": _enrich_track_info(track, user_genes=user_genes),
    }


def _handle_queue_tracks(
    inputs: dict[str, Any],
    tier: str,
    user_genes: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Queue multiple tracks and return action descriptors with MI data."""
    from .track_data import DIM_6D, _named_dims, search_tracks, load_track

    tracks_input = inputs.get("tracks", [])
    if not tracks_input:
        return {"error": "Provide a list of tracks to queue."}

    queued = []
    tracks_detail = []
    failed = []

    for item in tracks_input:
        track_id = item.get("track_id")
        query = item.get("query", "")

        if not track_id and not query:
            continue

        # Resolve track
        if not track_id:
            results = search_tracks(query, limit=1)
            if not results:
                failed.append(query)
                continue
            track_id = results[0]["id"]

        track = load_track(track_id)
        if not track:
            failed.append(track_id)
            continue

        # Action payload (lightweight, for frontend)
        queued.append({
            "track_id": track_id,
            "track_name": track.get("title", ""),
            "artist": track.get("artist", ""),
            "dominant_family": track.get("dominant_family", ""),
        })

        # Detail payload (enriched, for LLM context)
        detail: dict[str, Any] = {
            "title": track.get("title", ""),
            "artist": track.get("artist", ""),
            "dominant_family": track.get("dominant_family", ""),
            "dominant_gene": track.get("dominant_gene", ""),
        }
        dims = track.get("dimensions", {})
        if "psychology_6d" in dims:
            detail["dimensions_6d"] = _named_dims(dims["psychology_6d"], DIM_6D)
        genes = track.get("genes", {})
        if genes:
            match = _gene_match_score(user_genes, genes)
            if match is not None:
                detail["gene_match"] = match
        tracks_detail.append(detail)

    if not queued:
        return {"error": "No matching tracks found for the queue."}

    return {
        "action": {
            "type": "queue_tracks",
            "tracks": queued,
        },
        "queued_count": len(queued),
        "failed": failed,
        "tracks": tracks_detail,
    }


def _handle_control_playback(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Return a playback control action descriptor."""
    command = inputs.get("command", "")
    value = inputs.get("value")

    valid_commands = {
        "pause", "resume", "next", "previous",
        "volume_up", "volume_down",
        "shuffle_toggle", "repeat_cycle",
    }
    if command not in valid_commands:
        return {"error": f"Unknown command: {command}. Valid: {sorted(valid_commands)}"}

    action: dict[str, Any] = {"type": "control_playback", "command": command}
    if value is not None:
        action["value"] = value

    return {"action": action, "result": f"Playback command '{command}' sent to frontend."}


def _handle_get_now_playing(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Return a get_now_playing action descriptor.

    The actual track data comes from the frontend via the action response —
    the backend doesn't have direct access to the user's playback state.
    """
    return {
        "action": {"type": "get_now_playing"},
        "message": "Requesting current playback state from the frontend.",
    }


# ── Recommendation Handler ───────────────────────────────────────


# Mood → gene affinity (which genes should be high/low for this mood)
# Genes have wide variance (0.09-0.95) so thresholds work well here.
_MOOD_GENE_FILTERS: dict[str, dict[str, tuple[float, float]]] = {
    "energetic": {"energy": (0.6, 1.0), "groove": (0.55, 1.0)},
    "calm": {"energy": (0.0, 0.35), "tension": (0.0, 0.35)},
    "emotional": {"valence": (0.0, 0.4), "tension": (0.4, 1.0)},
    "groovy": {"groove": (0.6, 1.0)},
    "complex": {"density": (0.55, 1.0)},
    "intense": {"energy": (0.6, 1.0), "tension": (0.6, 1.0)},
    "surprising": {"density": (0.55, 1.0), "tension": (0.5, 1.0)},
    "nostalgic": {"valence": (0.3, 0.6), "energy": (0.2, 0.5)},
}


def _handle_recommend_tracks(
    inputs: dict[str, Any],
    tier: str,
    user_genes: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Recommend tracks by gene profile match + mood filter."""
    from .track_data import DIM_6D, _named_dims, load_catalog, load_track

    mood = inputs.get("mood", "").lower().strip()
    count = min(inputs.get("count", 5), 10)
    exclude_ids = set(inputs.get("exclude_ids", []))

    catalog = load_catalog()
    tracks = catalog.get("tracks", [])

    scored: list[tuple[float, dict]] = []
    mood_filter = _MOOD_GENE_FILTERS.get(mood, {})

    for t in tracks:
        tid = t.get("id", "")
        if tid in exclude_ids:
            continue

        track_data = load_track(tid)
        if not track_data:
            continue

        # Gene match score
        genes = track_data.get("genes", {})
        match = _gene_match_score(user_genes, genes) if genes else 0.5
        if match is None:
            match = 0.5

        # Mood filter: check if track's gene values fall within mood ranges
        mood_bonus = 0.0
        mood_pass = True
        if mood_filter and genes:
            for gene_key, (lo, hi) in mood_filter.items():
                val = genes.get(gene_key, 0.5)
                if lo <= val <= hi:
                    mood_bonus += 0.1
                else:
                    mood_pass = False

        if mood_filter and not mood_pass:
            continue

        score = match + mood_bonus
        scored.append((score, track_data))

    scored.sort(key=lambda x: -x[0])
    top = scored[:count]

    if not top:
        return {
            "recommendations": [],
            "message": f"No tracks found matching mood='{mood}'." if mood else "No tracks available.",
        }

    recommendations = []
    for score, track_data in top:
        rec: dict[str, Any] = {
            "track_id": track_data.get("id", ""),
            "title": track_data.get("title", ""),
            "artist": track_data.get("artist", ""),
            "dominant_family": track_data.get("dominant_family", ""),
            "dominant_gene": track_data.get("dominant_gene", ""),
            "match_score": round(score, 2),
        }
        dims = track_data.get("dimensions", {})
        if "psychology_6d" in dims:
            rec["dimensions_6d"] = _named_dims(dims["psychology_6d"], DIM_6D)
        genes = track_data.get("genes", {})
        if genes:
            gene_match = _gene_match_score(user_genes, genes)
            if gene_match is not None:
                rec["gene_match"] = gene_match
        recommendations.append(rec)

    return {
        "recommendations": recommendations,
        "count": len(recommendations),
        "mood_filter": mood or None,
    }
