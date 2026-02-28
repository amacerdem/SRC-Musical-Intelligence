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
}

export interface ChatResponse {
  session_id: string;
  message: string;
  model_used: string;
  tokens_in: number;
  tokens_out: number;
  cost_usd: number;
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
