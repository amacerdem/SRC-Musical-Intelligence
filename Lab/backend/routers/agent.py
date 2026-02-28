"""Agent router — Musical Mind conversational AI endpoint.

Endpoints:
    POST /api/agent/chat         — send a message, get a response
    GET  /api/agent/history      — get conversation history
    POST /api/agent/interpret    — interpret analysis results as narrative
    GET  /api/agent/persona/{id} — get persona details
    GET  /api/agent/health       — agent subsystem health check
"""
from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(tags=["agent"])


# ── Request / Response Models ───────────────────────────────────────


class ChatRequest(BaseModel):
    """Chat message from user."""

    user_id: str
    session_id: str | None = None
    message: str
    language: str = "tr"

    # User profile (injected by frontend from auth/profile service)
    persona_id: int = 1
    persona_name: str = "Dopamine Seeker"
    family: str = "Alchemists"
    level: int = 1
    tier: str = "free"
    genes: dict[str, float] = Field(
        default_factory=lambda: {
            "entropy": 0.5,
            "resolution": 0.5,
            "tension": 0.5,
            "resonance": 0.5,
            "plasticity": 0.5,
        }
    )
    dimensions_6d: dict[str, float] | None = None


class ChatResponse(BaseModel):
    """Agent response to user."""

    session_id: str
    message: str
    model_used: str
    tokens_in: int = 0
    tokens_out: int = 0
    cost_usd: float = 0.0


class InterpretRequest(BaseModel):
    """Interpret analysis data as natural language."""

    user_id: str
    tier: str = "free"
    language: str = "tr"
    dimensions_6d: dict[str, float]
    dimensions_12d: dict[str, float] | None = None
    dimensions_24d: dict[str, float] | None = None
    neurochemicals: dict[str, float] | None = None
    previous_6d: dict[str, float] | None = None


class InterpretResponse(BaseModel):
    """Interpretation result."""

    narrative: str
    tier: str
    dimensions_used: int


# ── Chat Endpoint ───────────────────────────────────────────────────


MAX_TOOL_ROUNDS = 5  # Safety limit for tool call loop


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Send a message to the Musical Mind agent and get a response.

    Handles tool_use responses: when Claude calls a tool, we execute it
    and send the result back, repeating until Claude produces a text response.
    """
    import json as _json

    from Musical_Intelligence.brain.llm.agent.conversation import ConversationManager
    from Musical_Intelligence.brain.llm.agent.context_builder import build_api_request
    from Musical_Intelligence.brain.llm.agent.router import estimate_cost
    from Musical_Intelligence.brain.llm.agent.tools import handle_tool_call

    # Build user profile dict
    user_profile = {
        "name": req.user_id,
        "persona_id": req.persona_id,
        "persona_name": req.persona_name,
        "family": req.family,
        "level": req.level,
        "tier": req.tier,
        "genes": req.genes,
    }
    if req.dimensions_6d:
        user_profile["dimensions_6d"] = req.dimensions_6d

    # Get conversation history
    mgr = ConversationManager()
    session_id = req.session_id or mgr.create_session(req.user_id)
    history = mgr.get_api_messages(req.user_id, session_id, max_tokens=2000)

    # Build API request
    api_request = build_api_request(
        user_message=req.message,
        user_profile=user_profile,
        language=req.language,
        conversation_history=history,
    )

    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if api_key:
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=api_key)

            # Tool call loop: keep sending until we get a final text response
            total_in = 0
            total_out = 0
            response_text = ""
            messages = api_request.pop("messages")

            for _round in range(MAX_TOOL_ROUNDS):
                response = client.messages.create(
                    messages=messages,
                    **api_request,
                )

                total_in += response.usage.input_tokens
                total_out += response.usage.output_tokens

                # Check if response contains tool_use blocks
                tool_use_blocks = [
                    b for b in response.content if b.type == "tool_use"
                ]
                text_blocks = [
                    b for b in response.content if hasattr(b, "text")
                ]

                # Collect any text produced alongside tool calls
                for tb in text_blocks:
                    response_text += tb.text

                if not tool_use_blocks:
                    # No tool calls — we have our final response
                    break

                # Process tool calls and build tool_result messages
                # First, add the assistant's response (with tool_use) to messages
                messages.append({
                    "role": "assistant",
                    "content": [
                        {
                            "type": b.type,
                            **({"text": b.text} if b.type == "text" else {}),
                            **({"id": b.id, "name": b.name, "input": b.input} if b.type == "tool_use" else {}),
                        }
                        for b in response.content
                    ],
                })

                # Execute each tool and collect results
                tool_results = []
                for tool_block in tool_use_blocks:
                    result = handle_tool_call(
                        tool_name=tool_block.name,
                        tool_input=tool_block.input,
                        user_tier=req.tier,
                    )
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_block.id,
                        "content": _json.dumps(result, ensure_ascii=False),
                    })

                # Add tool results as a user message
                messages.append({
                    "role": "user",
                    "content": tool_results,
                })

                # Clear text for the next round (we want the final response)
                response_text = ""

            cost = estimate_cost(api_request["model"], total_in, total_out)
            tokens_in = total_in
            tokens_out = total_out

        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Claude API error: {e}")

    else:
        # Fallback: knowledge-based response without API
        response_text = _fallback_response(req.message, req.tier, req.language)
        tokens_in = 0
        tokens_out = 0
        cost = 0.0

    # Save to conversation history
    mgr.add_message(req.user_id, session_id, "user", req.message)
    mgr.add_message(req.user_id, session_id, "assistant", response_text)

    return ChatResponse(
        session_id=session_id,
        message=response_text,
        model_used=api_request["model"],
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        cost_usd=cost,
    )


# ── History Endpoint ────────────────────────────────────────────────


@router.get("/history")
async def get_history(
    user_id: str = Query(...),
    session_id: str = Query(...),
    limit: int = Query(50, ge=1, le=200),
):
    """Get conversation history for a session."""
    from Musical_Intelligence.brain.llm.agent.conversation import ConversationManager

    mgr = ConversationManager()
    messages = mgr.get_history(user_id, session_id, limit=limit)
    return {
        "session_id": session_id,
        "messages": [m.to_dict() for m in messages],
        "count": len(messages),
    }


# ── Interpret Endpoint ──────────────────────────────────────────────


@router.post("/interpret", response_model=InterpretResponse)
async def interpret(req: InterpretRequest):
    """Interpret analysis dimensions as natural language narrative.

    Doesn't require Claude API — uses the local interpreter.
    """
    from Musical_Intelligence.brain.llm.agent.interpreter import interpret_dimensions

    narrative = interpret_dimensions(
        dimensions_6d=req.dimensions_6d,
        tier=req.tier,
        language=req.language,
        dimensions_12d=req.dimensions_12d,
        dimensions_24d=req.dimensions_24d,
        neurochemicals=req.neurochemicals,
        previous_6d=req.previous_6d,
    )

    dim_count = 6
    if req.dimensions_12d:
        dim_count += 12
    if req.dimensions_24d:
        dim_count += 24

    return InterpretResponse(
        narrative=narrative,
        tier=req.tier,
        dimensions_used=dim_count,
    )


# ── Persona Endpoint ────────────────────────────────────────────────


@router.get("/persona/{persona_id}")
async def get_persona(persona_id: int):
    """Get persona details by ID."""
    from Musical_Intelligence.brain.llm.agent.tools import handle_tool_call

    result = handle_tool_call(
        "get_persona_info",
        {"persona_id": persona_id},
    )
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


# ── Health Check ────────────────────────────────────────────────────


@router.get("/health")
async def agent_health():
    """Agent subsystem health check."""
    import json
    from pathlib import Path

    from Musical_Intelligence.brain.llm.config import CHROMA_DIR, KNOWLEDGE_DIR

    # Check knowledge files
    knowledge_files = list(KNOWLEDGE_DIR.glob("*.jsonl"))
    knowledge_entries = 0
    for f in knowledge_files:
        knowledge_entries += sum(1 for line in f.read_text().strip().splitlines() if line.strip())

    # Check ChromaDB
    chroma_ready = CHROMA_DIR.exists() and any(CHROMA_DIR.iterdir()) if CHROMA_DIR.exists() else False

    # Check API key
    has_api_key = bool(os.environ.get("ANTHROPIC_API_KEY"))

    return {
        "status": "ok",
        "knowledge_files": len(knowledge_files),
        "knowledge_entries": knowledge_entries,
        "chroma_ready": chroma_ready,
        "anthropic_api_key_set": has_api_key,
        "mode": "full" if has_api_key else "fallback",
    }


# ── Fallback Response (no API key) ──────────────────────────────────


def _fallback_response(message: str, tier: str, language: str) -> str:
    """Generate a basic response without Claude API.

    Uses RAG retrieval if available, otherwise returns a greeting.
    """
    try:
        from Musical_Intelligence.brain.llm.rag.retriever import retrieve_knowledge

        results = retrieve_knowledge(
            query=message,
            user_tier=tier,
            top_k=3,
            use_local_embeddings=True,
        )
        if results:
            texts = [r.text[:200] for r in results]
            if language == "tr":
                return (
                    "API anahtarı ayarlanmadığından tam sohbet modu devre dışı. "
                    "Ancak bilgi tabanından şu ilgili bilgileri buldum:\n\n"
                    + "\n\n".join(f"- {t}" for t in texts)
                )
            else:
                return (
                    "Full chat mode is disabled (no API key). "
                    "However, I found these relevant entries from the knowledge base:\n\n"
                    + "\n\n".join(f"- {t}" for t in texts)
                )
    except Exception:
        pass

    if language == "tr":
        return (
            "Musical Mind agent hazır ancak Claude API anahtarı (ANTHROPIC_API_KEY) "
            "ayarlanmamış. Tam sohbet deneyimi için ortam değişkenini ayarlayın."
        )
    return (
        "Musical Mind agent is ready but no Claude API key (ANTHROPIC_API_KEY) is set. "
        "Set the environment variable for the full chat experience."
    )
