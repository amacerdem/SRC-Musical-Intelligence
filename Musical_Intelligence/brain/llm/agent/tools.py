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
        "name": "get_current_dimensions",
        "description": (
            "Get the user's current 6D/12D/24D dimension values "
            "from their most recent listening session. Use this when "
            "the user asks about their current state or profile."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "Session ID (optional, defaults to most recent)",
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
            "Get specific belief values from the user's most recent "
            "analysis session. Only use for Premium/Research tier users "
            "who ask about specific beliefs."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "Session ID (optional, defaults to most recent)",
                },
                "belief_keys": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of belief keys to retrieve (e.g., ['wanting_ramp', 'prediction_accuracy'])",
                },
            },
            "required": ["belief_keys"],
        },
    },
    {
        "name": "compare_sessions",
        "description": (
            "Compare two listening sessions — show dimension and belief "
            "deltas. Use when the user asks 'how was this different from last time?'"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "session_a": {
                    "type": "string",
                    "description": "First session ID (earlier)",
                },
                "session_b": {
                    "type": "string",
                    "description": "Second session ID (later, or 'latest')",
                },
                "layer": {
                    "type": "string",
                    "enum": ["6d", "12d", "24d"],
                    "description": "Comparison depth",
                },
            },
            "required": ["session_a", "session_b"],
        },
    },
    {
        "name": "get_belief_trajectory",
        "description": (
            "Get time-series trajectory of specific beliefs or dimensions "
            "across multiple sessions. Use for trend analysis and evolution insights."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "keys": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Belief keys or dimension keys to track",
                },
                "period": {
                    "type": "string",
                    "enum": ["week", "month", "all"],
                    "description": "Time period to retrieve",
                },
            },
            "required": ["keys", "period"],
        },
    },
    {
        "name": "analyze_track",
        "description": (
            "Run MI analysis on a specific track and return a summary "
            "of dimensions and notable belief patterns. Use when the user "
            "shares a song and asks 'what does this music do to my brain?'"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "track_id": {
                    "type": "string",
                    "description": "Track identifier or Spotify URI",
                },
            },
            "required": ["track_id"],
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
]


# ── Tool Call Handler ───────────────────────────────────────────────


def handle_tool_call(
    tool_name: str,
    tool_input: dict[str, Any],
    user_tier: str = "free",
) -> dict[str, Any]:
    """Route a tool call to the appropriate handler.

    In production, these handlers connect to the Lab backend API
    or directly to the MI analysis pipeline. For now, they return
    structured placeholder responses.

    Args:
        tool_name: Name of the tool being called.
        tool_input: Input parameters from the LLM.
        user_tier: User's subscription tier for access control.

    Returns:
        Tool result dict to feed back to the LLM.
    """
    handlers = {
        "get_current_dimensions": _handle_get_dimensions,
        "get_beliefs": _handle_get_beliefs,
        "compare_sessions": _handle_compare_sessions,
        "get_belief_trajectory": _handle_get_trajectory,
        "analyze_track": _handle_analyze_track,
        "search_knowledge": _handle_search_knowledge,
        "get_persona_info": _handle_get_persona,
    }

    handler = handlers.get(tool_name)
    if not handler:
        return {"error": f"Unknown tool: {tool_name}"}

    return handler(tool_input, user_tier)


# ── Placeholder Handlers ───────────────────────────────────────────
# These will be connected to the Lab backend in Phase 5.


def _handle_get_dimensions(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Placeholder: Returns mock dimension data."""
    return {
        "status": "not_connected",
        "message": "MI analysis pipeline not yet connected. Connect via Lab backend API.",
        "expected_format": {
            "session_id": "str",
            "dimensions": {"dim_key": "float (0-1)"},
            "timestamp": "ISO 8601",
        },
    }


def _handle_get_beliefs(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Placeholder: Returns mock belief data."""
    if tier not in ("premium", "research"):
        return {"error": "Belief-level access requires Premium or Research tier."}
    return {
        "status": "not_connected",
        "message": "MI analysis pipeline not yet connected.",
    }


def _handle_compare_sessions(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Placeholder: Returns mock comparison."""
    return {
        "status": "not_connected",
        "message": "Session comparison requires connected MI pipeline.",
    }


def _handle_get_trajectory(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Placeholder: Returns mock trajectory."""
    return {
        "status": "not_connected",
        "message": "Trajectory analysis requires historical session data.",
    }


def _handle_analyze_track(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Placeholder: Returns mock analysis."""
    return {
        "status": "not_connected",
        "message": "Track analysis requires connected MI pipeline and audio processing.",
    }


def _handle_search_knowledge(
    inputs: dict[str, Any], tier: str
) -> dict[str, Any]:
    """Search knowledge base via RAG retriever."""
    import os

    query = inputs.get("query", "")
    collection = inputs.get("collection", "knowledge_cards")

    if not query:
        return {"error": "Query is required."}

    # Use local embeddings if no OpenAI key is set
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
