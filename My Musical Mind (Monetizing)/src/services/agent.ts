/**
 * Agent API Service — Musical Mind chat endpoint client.
 *
 * Connects to Lab backend /api/agent/* endpoints via Vite proxy.
 */

export interface ChatRequest {
  user_id: string;
  session_id?: string;
  message: string;
  language: string;
  persona_id: number;
  persona_name: string;
  family: string;
  level: number;
  tier: string;
  genes: Record<string, number>;
  dimensions_6d?: Record<string, number>;
  spotify_profile?: {
    total_tracks: number;
    total_minutes: number;
    top_genres: string[];
    genre_diversity: number;
    artist_count: number;
    family_distribution: Record<string, number>;
    taste_shift: number;
  };
}

export interface ChatResponse {
  session_id: string;
  message: string;
  model_used: string;
  tokens_in: number;
  tokens_out: number;
  cost_usd: number;
  actions?: AgentAction[];
}

export interface AgentAction {
  type: "play_track" | "queue_tracks" | "control_playback" | "get_now_playing";
  track_id?: string;
  track_name?: string;
  artist?: string;
  command?: string;
  value?: number;
  tracks?: { track_id: string; track_name: string; artist: string; dominant_family?: string }[];
}

export interface SystemEventRequest {
  user_id: string;
  session_id?: string;
  event_type: string;
  data: Record<string, unknown>;
  language: string;
  persona_id: number;
  persona_name: string;
  family: string;
  level: number;
  tier: string;
  genes: Record<string, number>;
}

export interface AgentHealth {
  status: string;
  knowledge_files: number;
  knowledge_entries: number;
  chroma_ready: boolean;
  anthropic_api_key_set: boolean;
  mode: "full" | "fallback";
}

export async function sendMessage(req: ChatRequest): Promise<ChatResponse> {
  const res = await fetch("/api/agent/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`Agent chat failed (${res.status}): ${detail}`);
  }
  return res.json();
}

/* ── Shared SSE Parser ──────────────────────────────────────────── */

interface SSECallbacks {
  onStatus: (text: string) => void;
  onToken: (text: string) => void;
  onAction?: (action: AgentAction) => void;
}

async function parseSSEStream(
  res: Response,
  callbacks: SSECallbacks,
): Promise<ChatResponse> {
  const reader = res.body?.getReader();
  if (!reader) throw new Error("No response stream");

  const decoder = new TextDecoder();
  let buffer = "";
  let result: ChatResponse | null = null;
  let errorDetail: string | null = null;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    const parts = buffer.split("\n\n");
    buffer = parts.pop() ?? "";

    for (const part of parts) {
      if (!part.trim()) continue;

      let eventType = "message";
      let data = "";

      for (const line of part.split("\n")) {
        if (line.startsWith("event: ")) {
          eventType = line.slice(7).trim();
        } else if (line.startsWith("data: ")) {
          data = line.slice(6);
        }
      }

      if (!data) continue;

      try {
        const parsed = JSON.parse(data);
        if (eventType === "status") {
          callbacks.onStatus(parsed.text ?? "");
        } else if (eventType === "token") {
          callbacks.onToken(parsed.text ?? "");
        } else if (eventType === "action") {
          callbacks.onAction?.(parsed as AgentAction);
        } else if (eventType === "done") {
          result = parsed as ChatResponse;
        } else if (eventType === "error") {
          errorDetail = parsed.detail ?? "Unknown error";
        }
      } catch {
        // Ignore malformed SSE data
      }
    }
  }

  if (errorDetail) throw new Error(errorDetail);
  if (!result) throw new Error("No response received");
  return result;
}

/** SSE streaming chat — receives status updates + final response. */
export async function sendMessageStream(
  req: ChatRequest,
  onStatus: (text: string) => void,
  onToken: (text: string) => void,
  onAction?: (action: AgentAction) => void,
): Promise<ChatResponse> {
  const res = await fetch("/api/agent/chat/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });

  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`Agent chat failed (${res.status}): ${detail}`);
  }

  return parseSSEStream(res, { onStatus, onToken, onAction });
}

/** SSE streaming system event — for proactive agent messages. */
export async function sendSystemEventStream(
  req: SystemEventRequest,
  onStatus: (text: string) => void,
  onToken: (text: string) => void,
): Promise<ChatResponse> {
  const res = await fetch("/api/agent/chat/system-event", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });

  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`System event failed (${res.status}): ${detail}`);
  }

  return parseSSEStream(res, { onStatus, onToken });
}

export async function getHistory(
  userId: string,
  sessionId: string,
  limit = 50,
): Promise<{
  session_id: string;
  messages: Array<{
    message_id: string;
    role: string;
    content: string;
    timestamp: string;
    metadata: Record<string, unknown>;
  }>;
  count: number;
}> {
  const params = new URLSearchParams({ user_id: userId, session_id: sessionId, limit: String(limit) });
  const res = await fetch(`/api/agent/history?${params}`);
  if (!res.ok) throw new Error(`History fetch failed (${res.status})`);
  return res.json();
}

export async function getAgentHealth(): Promise<AgentHealth> {
  const res = await fetch("/api/agent/health");
  if (!res.ok) throw new Error(`Health check failed (${res.status})`);
  return res.json();
}
