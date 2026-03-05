"""Agent router — Musical Mind conversational AI endpoint.

Endpoints:
    POST /api/agent/chat         — send a message, get a response
    POST /api/agent/chat/stream  — SSE streaming chat with status updates
    GET  /api/agent/history      — get conversation history
    POST /api/agent/interpret    — interpret analysis results as narrative
    GET  /api/agent/persona/{id} — get persona details
    GET  /api/agent/health       — agent subsystem health check
"""
from __future__ import annotations

import json as _json
import os
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
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
    spotify_profile: dict[str, Any] | None = None
    listening_history: dict[str, Any] | None = None


class ChatResponse(BaseModel):
    """Agent response to user."""

    session_id: str
    message: str
    model_used: str
    tokens_in: int = 0
    tokens_out: int = 0
    cost_usd: float = 0.0
    actions: list[dict[str, Any]] = Field(default_factory=list)


class SystemEventRequest(BaseModel):
    """System event from frontend (track changes, etc.)."""

    user_id: str
    session_id: str | None = None
    event_type: str  # "track_changed", "playback_paused", etc.
    data: dict[str, Any] = Field(default_factory=dict)
    language: str = "tr"

    # User profile (same as ChatRequest)
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


class InterpretRequest(BaseModel):
    """Interpret analysis data as natural language.

    Two modes:
    1. Track mode: provide track_id for full multi-layer interpretation.
    2. Dimension mode (backward-compat): provide dimensions_6d directly.
    """

    user_id: str
    tier: str = "free"
    language: str = "tr"

    # Track mode (new)
    track_id: str | None = None
    persona_family: str | None = None
    level: int = 1
    user_genes: dict[str, float] | None = None

    # Dimension mode (backward-compatible)
    dimensions_6d: dict[str, float] | None = None
    dimensions_12d: dict[str, float] | None = None
    dimensions_24d: dict[str, float] | None = None
    neurochemicals: dict[str, float] | None = None
    functions: dict[str, float] | None = None
    previous_6d: dict[str, float] | None = None


class InterpretResponse(BaseModel):
    """Interpretation result."""

    narrative: str
    tier: str
    dimensions_used: int
    highlights: list[str] | None = None
    temporal_summary: str | None = None
    reward_insight: str | None = None
    observation_type: str | None = None


# ── Chat Endpoint ───────────────────────────────────────────────────


MAX_TOOL_ROUNDS = 5  # Safety limit for tool call loop


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Send a message to the Musical Mind agent and get a response.

    Handles tool_use responses: when Claude calls a tool, we execute it
    and send the result back, repeating until Claude produces a text response.
    """
    from Musical_Intelligence.brain.llm.agent.conversation import ConversationManager
    from Musical_Intelligence.brain.llm.agent.context_builder import build_api_request
    from Musical_Intelligence.brain.llm.agent.router import estimate_cost
    from Musical_Intelligence.brain.llm.agent.tools import handle_tool_call, set_spotify_profile

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
    if req.spotify_profile:
        user_profile["spotify_profile"] = req.spotify_profile
    if req.listening_history:
        user_profile["listening_history"] = req.listening_history

    # Inject Spotify profile into tool system
    set_spotify_profile(req.spotify_profile)

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
            collected_actions: list[dict] = []
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
                        user_genes=req.genes,
                    )
                    # Collect frontend actions from tool results
                    if "action" in result:
                        collected_actions.append(result["action"])
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
        actions=collected_actions if api_key else [],
    )


# ── Streaming Chat Endpoint (SSE) ──────────────────────────────────


def _sse_event(event: str, data: dict) -> str:
    """Format a Server-Sent Event."""
    return f"event: {event}\ndata: {_json.dumps(data, ensure_ascii=False)}\n\n"


@router.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    """SSE streaming chat — sends status updates as processing progresses.

    Events:
        status  — {"text": "...", "step": "context|rag|api|tool|done"}
        done    — ChatResponse JSON (final result)
        error   — {"detail": "..."}
    """

    async def generate():
        from Musical_Intelligence.brain.llm.agent.conversation import ConversationManager
        from Musical_Intelligence.brain.llm.agent.context_builder import build_api_request
        from Musical_Intelligence.brain.llm.agent.router import estimate_cost
        from Musical_Intelligence.brain.llm.agent.tools import handle_tool_call, set_spotify_profile

        lang = req.language

        # Step 1: Build context
        yield _sse_event("status", {
            "text": "Profil ve bağlam hazırlanıyor..." if lang == "tr" else "Preparing context...",
            "step": "context",
        })

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
        if req.spotify_profile:
            user_profile["spotify_profile"] = req.spotify_profile
        if req.listening_history:
            user_profile["listening_history"] = req.listening_history

        # Inject Spotify profile into tool system
        set_spotify_profile(req.spotify_profile)

        mgr = ConversationManager()
        session_id = req.session_id or mgr.create_session(req.user_id)
        history = mgr.get_api_messages(req.user_id, session_id, max_tokens=2000)

        # Step 2: RAG search
        yield _sse_event("status", {
            "text": "Bilgi tabanı aranıyor..." if lang == "tr" else "Searching knowledge base...",
            "step": "rag",
        })

        api_request = build_api_request(
            user_message=req.message,
            user_profile=user_profile,
            language=lang,
            conversation_history=history,
        )

        api_key = os.environ.get("ANTHROPIC_API_KEY")

        if not api_key:
            response_text = _fallback_response(req.message, req.tier, lang)
            mgr.add_message(req.user_id, session_id, "user", req.message)
            mgr.add_message(req.user_id, session_id, "assistant", response_text)
            yield _sse_event("done", {
                "session_id": session_id,
                "message": response_text,
                "model_used": api_request["model"],
                "tokens_in": 0, "tokens_out": 0, "cost_usd": 0.0,
            })
            return

        # Step 3: Call Claude
        yield _sse_event("status", {
            "text": "Düşünüyorum..." if lang == "tr" else "Thinking...",
            "step": "api",
        })

        try:
            import anthropic

            client = anthropic.AsyncAnthropic(api_key=api_key)
            total_in = 0
            total_out = 0
            response_text = ""
            messages = api_request.pop("messages")

            for _round in range(MAX_TOOL_ROUNDS):
                # Stream tokens to client in real-time
                async with client.messages.stream(
                    messages=messages,
                    **api_request,
                ) as stream:
                    async for text in stream.text_stream:
                        yield _sse_event("token", {"text": text})
                        response_text += text
                    response = await stream.get_final_message()

                total_in += response.usage.input_tokens
                total_out += response.usage.output_tokens

                tool_use_blocks = [
                    b for b in response.content if b.type == "tool_use"
                ]

                if not tool_use_blocks:
                    break

                # Step 4: Tool use — show which tools
                tool_names = [b.name for b in tool_use_blocks]
                tool_labels = {
                    "get_listening_profile": ("Dinleme profili yükleniyor...", "Loading listening profile..."),
                    "search_tracks": ("Müzik kütüphanesi aranıyor...", "Searching music library..."),
                    "analyze_track": ("Parça analiz ediliyor...", "Analyzing track..."),
                    "get_current_dimensions": ("Boyutlar okunuyor...", "Reading dimensions..."),
                    "get_beliefs": ("İnançlar okunuyor...", "Reading beliefs..."),
                    "compare_tracks": ("Parçalar karşılaştırılıyor...", "Comparing tracks..."),
                    "search_knowledge": ("Bilgi tabanı aranıyor...", "Searching knowledge..."),
                    "get_persona_info": ("Persona bilgisi alınıyor...", "Getting persona info..."),
                    "get_temporal_journey": ("Zamansal yolculuk analiz ediliyor...", "Analyzing temporal journey..."),
                    "get_belief_timeline": ("İnanç zaman çizelgesi oluşturuluyor...", "Building belief timeline..."),
                    "get_brain_activation": ("Beyin aktivasyonu okunuyor...", "Reading brain activation..."),
                    "play_track": ("Parça çalınıyor...", "Playing track..."),
                    "queue_tracks": ("Kuyruk oluşturuluyor...", "Building queue..."),
                    "control_playback": ("Oynatma kontrol ediliyor...", "Controlling playback..."),
                    "get_now_playing": ("Şu an çalan alınıyor...", "Getting now playing..."),
                    "recommend_tracks": ("Kişisel öneriler hazırlanıyor...", "Preparing personalized recommendations..."),
                    "get_spotify_listening_profile": ("Spotify dinleme profili yükleniyor...", "Loading Spotify listening profile..."),
                }
                for tn in tool_names:
                    tr_label, en_label = tool_labels.get(tn, (f"{tn}...", f"{tn}..."))
                    yield _sse_event("status", {
                        "text": tr_label if lang == "tr" else en_label,
                        "step": "tool",
                        "tool": tn,
                    })

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

                tool_results = []
                for tool_block in tool_use_blocks:
                    result = handle_tool_call(
                        tool_name=tool_block.name,
                        tool_input=tool_block.input,
                        user_tier=req.tier,
                        user_genes=req.genes,
                    )
                    # Emit frontend action via SSE
                    if "action" in result:
                        yield _sse_event("action", result["action"])
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_block.id,
                        "content": _json.dumps(result, ensure_ascii=False),
                    })

                messages.append({
                    "role": "user",
                    "content": tool_results,
                })

                # Back to thinking after tools
                yield _sse_event("status", {
                    "text": "Sonuçlar yorumlanıyor..." if lang == "tr" else "Interpreting results...",
                    "step": "api",
                })
                response_text = ""

            cost = estimate_cost(api_request["model"], total_in, total_out)

            mgr.add_message(req.user_id, session_id, "user", req.message)
            mgr.add_message(req.user_id, session_id, "assistant", response_text)

            yield _sse_event("done", {
                "session_id": session_id,
                "message": response_text,
                "model_used": api_request["model"],
                "tokens_in": total_in,
                "tokens_out": total_out,
                "cost_usd": cost,
            })

        except Exception as e:
            yield _sse_event("error", {"detail": str(e)})

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# ── System Event Endpoint (proactive agent) ────────────────────────


def _build_system_event_message(event_type: str, data: dict, lang: str) -> str:
    """Convert a system event into a prompt-formatted message.

    For track_changed events, enriches with MI data (6D, genes, neurochemicals)
    so the agent can provide data-driven commentary.
    """
    if event_type == "track_changed":
        name = data.get("track_name", "?")
        artist = data.get("artist", "?")
        family = data.get("family", "")
        genre = data.get("genre", "")
        track_id = data.get("track_id", "")

        # Try to load MI data for richer context
        mi_context = ""
        if track_id:
            try:
                from Musical_Intelligence.brain.llm.agent.track_data import (
                    DIM_6D, load_track,
                )
                track = load_track(track_id)
                if track:
                    dims = track.get("dimensions", {}).get("psychology_6d", [])
                    if dims and len(dims) >= 6:
                        dim_str = ", ".join(
                            f"{k}={round(v, 2)}"
                            for k, v in zip(DIM_6D, dims)
                        )
                        mi_context += f" 6D: [{dim_str}]."
                    gene = track.get("dominant_gene", "")
                    if gene:
                        mi_context += f" Dominant gene: {gene}."
                    neuro = track.get("neuro_4d", {})
                    if neuro:
                        top_neuro = max(neuro, key=neuro.get)
                        mi_context += f" Top neurochemical: {top_neuro} ({round(neuro[top_neuro], 2)})."
            except Exception:
                pass  # MI enrichment is best-effort

        if lang == "tr":
            return (
                f"[SİSTEM: Şu an çalan parça değişti → '{name}' — {artist} "
                f"({genre}, {family}).{mi_context} Kısa ve doğal bir yorum yap, "
                f"parçanın müzikal karakteri hakkında 1-2 cümle söyle. "
                f"MI verilerini referans göster.]"
            )
        return (
            f"[SYSTEM: Now playing changed → '{name}' by {artist} "
            f"({genre}, {family}).{mi_context} Make a brief, natural comment about "
            f"this track's musical character in 1-2 sentences. "
            f"Reference the MI data.]"
        )

    if event_type == "playback_paused":
        if lang == "tr":
            return "[SİSTEM: Kullanıcı müziği duraklattı. Gerekirse kısa tepki ver.]"
        return "[SYSTEM: User paused playback. React briefly if appropriate.]"

    return f"[SYSTEM: {event_type} — {_json.dumps(data, ensure_ascii=False)}]"


@router.post("/chat/system-event")
async def system_event_stream(req: SystemEventRequest):
    """Handle system events (track changes, etc.) and generate proactive insights.

    Converts the system event into a hidden context message and streams
    the agent's proactive response via SSE.
    """
    system_message = _build_system_event_message(
        req.event_type, req.data, req.language,
    )

    chat_req = ChatRequest(
        user_id=req.user_id,
        session_id=req.session_id,
        message=system_message,
        language=req.language,
        persona_id=req.persona_id,
        persona_name=req.persona_name,
        family=req.family,
        level=req.level,
        tier=req.tier,
        genes=req.genes,
    )

    return await chat_stream(chat_req)


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
    """Interpret analysis data as natural language narrative.

    Two modes:
    1. Track mode: provide track_id → full multi-layer interpretation.
    2. Dimension mode: provide dimensions_6d → backward-compatible string.

    Doesn't require Claude API — uses the local interpreter.
    """
    # ── Track mode: full interpretation ────────────────────────
    if req.track_id:
        from Musical_Intelligence.brain.llm.agent.track_data import load_track
        from Musical_Intelligence.brain.llm.agent.interpreter import interpret_track

        track = load_track(req.track_id)
        if not track:
            raise HTTPException(
                status_code=404,
                detail=f"Track '{req.track_id}' not found in analysis database.",
            )

        result = interpret_track(
            track=track,
            tier=req.tier,
            language=req.language,
            persona_family=req.persona_family,
            level=req.level,
            user_genes=req.user_genes,
            previous_6d=req.previous_6d,
        )

        dim_count = 6
        if track.get("dimensions", {}).get("cognition_12d"):
            dim_count += 12
        if track.get("dimensions", {}).get("neuroscience_24d"):
            dim_count += 24

        return InterpretResponse(
            narrative=result.get("narrative", ""),
            tier=req.tier,
            dimensions_used=dim_count,
            highlights=result.get("highlights"),
            temporal_summary=result.get("temporal_summary", {}).get("narrative") if isinstance(result.get("temporal_summary"), dict) else None,
            reward_insight=result.get("reward_insight", {}).get("narrative") if isinstance(result.get("reward_insight"), dict) else None,
            observation_type=result.get("observation_type", {}).get("type") if isinstance(result.get("observation_type"), dict) else None,
        )

    # ── Dimension mode: backward-compatible ────────────────────
    if not req.dimensions_6d:
        raise HTTPException(
            status_code=400,
            detail="Either track_id or dimensions_6d is required.",
        )

    from Musical_Intelligence.brain.llm.agent.interpreter import interpret_dimensions

    narrative = interpret_dimensions(
        dimensions_6d=req.dimensions_6d,
        tier=req.tier,
        language=req.language,
        dimensions_12d=req.dimensions_12d,
        dimensions_24d=req.dimensions_24d,
        neurochemicals=req.neurochemicals,
        previous_6d=req.previous_6d,
        persona_family=req.persona_family,
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
