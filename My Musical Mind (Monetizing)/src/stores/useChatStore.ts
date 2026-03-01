/* ── useChatStore — Musical Mind conversation state ─────────────────
 *
 *  Manages chat UI state + message history.
 *  Reads user profile from useUserStore/useM3Store to build ChatRequest.
 *  Persists messages + sessionId to localStorage for continuity.
 *  ──────────────────────────────────────────────────────────────── */

import { create } from "zustand";
import { persist } from "zustand/middleware";
import {
  sendMessageStream as apiSendMessageStream,
  sendSystemEventStream as apiSendSystemEvent,
  type ChatRequest,
  type AgentAction,
  type SystemEventRequest,
} from "@/services/agent";
import { useUserStore } from "./useUserStore";
import { useM3Store } from "./useM3Store";
import { personas } from "@/data/personas";
import { getDominantType } from "@/types/m3";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: string;
  eventType?: string; // "track_changed", "playback_paused", etc.
}

interface ChatState {
  isOpen: boolean;
  messages: ChatMessage[];
  sessionId: string | null;
  isLoading: boolean;
  statusText: string | null;
  streamingContent: string | null;
  hasUnread: boolean;
  error: string | null;

  /** Callback for dispatching agent actions to the player. */
  actionHandler: ((action: AgentAction) => void) | null;

  toggle: () => void;
  open: () => void;
  close: () => void;
  sendMessage: (text: string) => Promise<void>;
  sendSystemEvent: (eventType: string, data: Record<string, unknown>) => Promise<void>;
  setActionHandler: (handler: ((action: AgentAction) => void) | null) => void;
  clearChat: () => void;
}

/** Map MMM tier names to backend tier names */
function mapTier(tier: string): string {
  if (tier === "ultimate") return "research";
  return tier; // free, basic, premium pass through
}

/** Detect language from message text — Turkish if it contains
 *  Turkish-specific characters or common Turkish words, else English. */
function detectLanguage(text: string): "tr" | "en" {
  // Turkish-specific characters
  if (/[şŞçÇğĞüÜöÖıİ]/.test(text)) return "tr";
  // Common Turkish words (case-insensitive)
  const trWords = /\b(ve|bir|bu|da|de|ben|sen|ne|mi|mı|için|ile|var|yok|nasıl|neden|ama|çok|gibi|benim|senin|müzik|şarkı|dinle)\b/i;
  if (trWords.test(text)) return "tr";
  return "en";
}

/** Build a ChatRequest from current store state */
function buildChatRequest(
  message: string,
  sessionId: string | null,
): ChatRequest {
  const userStore = useUserStore.getState();
  const m3Store = useM3Store.getState();
  const mind = m3Store.mind;
  const genes = mind?.genes ?? { entropy: 0.5, resolution: 0.5, tension: 0.5, resonance: 0.5, plasticity: 0.5 };
  const personaId = mind?.activePersonaId ?? 1;
  const persona = personas.find((p) => p.id === personaId);
  const family = mind ? getDominantType(mind.genes) : "Alchemists";

  return {
    user_id: userStore.displayName || "anonymous",
    session_id: sessionId ?? undefined,
    message,
    language: detectLanguage(message),
    persona_id: personaId,
    persona_name: persona?.name ?? "Dopamine Seeker",
    family,
    level: mind?.level ?? 1,
    tier: mapTier(mind?.tier ?? "free"),
    genes: { ...genes },
  };
}

/** Build a SystemEventRequest from current store state */
function buildSystemEventRequest(
  eventType: string,
  data: Record<string, unknown>,
  sessionId: string | null,
  language: "tr" | "en",
): SystemEventRequest {
  const userStore = useUserStore.getState();
  const m3Store = useM3Store.getState();
  const mind = m3Store.mind;
  const genes = mind?.genes ?? { entropy: 0.5, resolution: 0.5, tension: 0.5, resonance: 0.5, plasticity: 0.5 };
  const personaId = mind?.activePersonaId ?? 1;
  const persona = personas.find((p) => p.id === personaId);
  const family = mind ? getDominantType(mind.genes) : "Alchemists";

  return {
    user_id: userStore.displayName || "anonymous",
    session_id: sessionId ?? undefined,
    event_type: eventType,
    data,
    language,
    persona_id: personaId,
    persona_name: persona?.name ?? "Dopamine Seeker",
    family,
    level: mind?.level ?? 1,
    tier: mapTier(mind?.tier ?? "free"),
    genes: { ...genes },
  };
}

function uid(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
}

/** Debounce: minimum 10s between system events */
let lastSystemEventTime = 0;
const SYSTEM_EVENT_DEBOUNCE_MS = 10_000;

export const useChatStore = create<ChatState>()(
  persist(
    (set, get) => ({
      isOpen: false,
      messages: [],
      sessionId: null,
      isLoading: false,
      statusText: null,
      streamingContent: null,
      hasUnread: false,
      error: null,
      actionHandler: null,

      toggle: () => set((s) => {
        const opening = !s.isOpen;
        return { isOpen: opening, hasUnread: opening ? false : s.hasUnread };
      }),

      open: () => set({ isOpen: true, hasUnread: false }),

      close: () => set({ isOpen: false }),

      setActionHandler: (handler) => set({ actionHandler: handler }),

      sendMessage: async (text: string) => {
        const trimmed = text.trim();
        if (!trimmed || get().isLoading) return;

        // Optimistic: add user message immediately
        const userMsg: ChatMessage = {
          id: uid(),
          role: "user",
          content: trimmed,
          timestamp: new Date().toISOString(),
        };

        set((s) => ({
          messages: [...s.messages, userMsg],
          isLoading: true,
          statusText: null,
          error: null,
        }));

        try {
          const req = buildChatRequest(trimmed, get().sessionId);
          const res = await apiSendMessageStream(
            req,
            (status) => set({ statusText: status, streamingContent: null }),
            (token) => set((s) => ({
              streamingContent: (s.streamingContent ?? "") + token,
              statusText: null,
            })),
            // Dispatch agent actions to the registered handler
            (action) => {
              const handler = get().actionHandler;
              if (handler) handler(action);
            },
          );

          const assistantMsg: ChatMessage = {
            id: uid(),
            role: "assistant",
            content: res.message,
            timestamp: new Date().toISOString(),
          };

          set((s) => ({
            messages: [...s.messages, assistantMsg],
            sessionId: res.session_id,
            isLoading: false,
            statusText: null,
            streamingContent: null,
            hasUnread: !s.isOpen,
          }));
        } catch (err) {
          const errorMsg = err instanceof Error ? err.message : "Unknown error";
          set({ isLoading: false, statusText: null, streamingContent: null, error: errorMsg });
        }
      },

      sendSystemEvent: async (eventType: string, data: Record<string, unknown>) => {
        const state = get();
        // Debounce: skip if too soon or already loading
        const now = Date.now();
        if (state.isLoading || now - lastSystemEventTime < SYSTEM_EVENT_DEBOUNCE_MS) return;
        lastSystemEventTime = now;

        // Detect language from i18n setting
        const lang: "tr" | "en" = (document.documentElement.lang === "tr" || navigator.language.startsWith("tr")) ? "tr" : "en";

        const req = buildSystemEventRequest(eventType, data, state.sessionId, lang);

        set({ isLoading: true, statusText: null, error: null });

        try {
          const res = await apiSendSystemEvent(
            req,
            (status) => set({ statusText: status }),
            (token) => set((s) => ({
              streamingContent: (s.streamingContent ?? "") + token,
              statusText: null,
            })),
          );

          const assistantMsg: ChatMessage = {
            id: uid(),
            role: "assistant",
            content: res.message,
            timestamp: new Date().toISOString(),
          };

          set((s) => ({
            messages: [...s.messages, assistantMsg],
            sessionId: res.session_id,
            isLoading: false,
            statusText: null,
            streamingContent: null,
            hasUnread: !s.isOpen,
          }));
        } catch {
          // System events are best-effort — don't show error
          set({ isLoading: false, statusText: null, streamingContent: null });
        }
      },

      clearChat: () => set({
        messages: [],
        sessionId: null,
        error: null,
      }),
    }),
    {
      name: "m3-chat-store",
      partialize: (state) => ({
        messages: state.messages.slice(-50), // Keep last 50 messages
        sessionId: state.sessionId,
      }),
    },
  ),
);
