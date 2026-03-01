/**
 * ListenChat — Inline full-height chat panel for the Listen page.
 *
 * Reuses ChatMessage, ChatInput, and TypingIndicator from the shared
 * chat components. Unlike the floating ChatPanel, this is always
 * visible in the split-view layout (no open/close toggle).
 */

import { useEffect, useRef } from "react";
import { useTranslation } from "react-i18next";
import { Trash2, Music2, Sparkles } from "lucide-react";
import { motion } from "framer-motion";
import { useChatStore } from "@/stores/useChatStore";
import { MiniOrganism } from "@/components/mind/MiniOrganism";
import { ChatMessage, TypingIndicator } from "@/components/chat/ChatMessage";
import { ChatInput } from "@/components/chat/ChatInput";

interface Props {
  personaName: string;
  accentColor: string;
}

export function ListenChat({ personaName, accentColor }: Props) {
  const { t } = useTranslation();
  const messages = useChatStore((s) => s.messages);
  const isLoading = useChatStore((s) => s.isLoading);
  const statusText = useChatStore((s) => s.statusText);
  const streamingContent = useChatStore((s) => s.streamingContent);
  const sendMessage = useChatStore((s) => s.sendMessage);
  const clearChat = useChatStore((s) => s.clearChat);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages.length, isLoading, streamingContent]);

  return (
    <div
      className="flex flex-col h-full"
      style={{
        background: "rgba(0, 0, 0, 0.6)",
        backdropFilter: "blur(16px)",
        borderRight: "1px solid rgba(255,255,255,0.06)",
      }}
    >
      {/* ── Header ─────────────────────────────────────────────── */}
      <div
        className="flex items-center justify-between px-4 py-3 border-b border-white/[0.06] flex-shrink-0"
        style={{ background: `${accentColor}06` }}
      >
        <div className="flex items-center gap-2.5">
          <MiniOrganism color={accentColor} size={28} animated />
          <div>
            <div className="text-sm font-display font-medium text-white/90">
              {personaName}
            </div>
            <div className="text-[10px] text-slate-500 font-mono">
              Music Companion
            </div>
          </div>
        </div>
        {messages.length > 0 && (
          <button
            onClick={clearChat}
            className="w-8 h-8 rounded-lg flex items-center justify-center text-slate-600 hover:text-slate-400 transition-colors"
            title={t("chat.clear")}
          >
            <Trash2 size={14} />
          </button>
        )}
      </div>

      {/* ── Messages ───────────────────────────────────────────── */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto px-3 py-3 space-y-3 scroll-smooth"
      >
        {/* Empty state */}
        {messages.length === 0 && !isLoading && (
          <div className="flex flex-col items-center justify-center h-full gap-4 py-12 px-4">
            <MiniOrganism color={accentColor} size={48} animated />
            <p className="text-sm text-slate-400 text-center max-w-[260px] font-body leading-relaxed">
              {t("chat.listenWelcome")}
            </p>
            <div className="flex flex-wrap justify-center gap-2 mt-2">
              {[
                t("chat.listenSuggestion1"),
                t("chat.listenSuggestion2"),
                t("chat.listenSuggestion3"),
              ].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => sendMessage(suggestion)}
                  className="px-3 py-1.5 text-[11px] rounded-full border transition-all hover:scale-105"
                  style={{
                    borderColor: `${accentColor}30`,
                    color: `${accentColor}cc`,
                    background: `${accentColor}08`,
                  }}
                >
                  <Sparkles size={10} className="inline mr-1 opacity-60" />
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Message list */}
        {messages.map((msg) =>
          msg.role === "system" ? (
            <SystemEventDivider
              key={msg.id}
              eventType={msg.eventType}
              accentColor={accentColor}
            />
          ) : (
            <ChatMessage
              key={msg.id}
              role={msg.role as "user" | "assistant"}
              content={msg.content}
              accentColor={accentColor}
            />
          ),
        )}

        {/* Streaming response */}
        {streamingContent && (
          <ChatMessage
            role="assistant"
            content={streamingContent}
            accentColor={accentColor}
          />
        )}

        {/* Typing indicator */}
        {isLoading && !streamingContent && (
          <TypingIndicator accentColor={accentColor} statusText={statusText} />
        )}
      </div>

      {/* ── Input ──────────────────────────────────────────────── */}
      <div className="flex-shrink-0">
        <ChatInput
          onSend={sendMessage}
          disabled={isLoading}
          accentColor={accentColor}
        />
      </div>
    </div>
  );
}

/* ── System Event Divider ─────────────────────────────────────────── */

function SystemEventDivider({
  eventType,
  accentColor,
}: {
  eventType?: string;
  accentColor: string;
}) {
  if (eventType === "track_changed") {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex items-center justify-center gap-1.5 py-1.5"
      >
        <div className="h-px flex-1 bg-white/[0.06]" />
        <Music2 size={10} style={{ color: `${accentColor}80` }} />
        <span
          className="text-[10px] font-mono"
          style={{ color: `${accentColor}60` }}
        >
          track changed
        </span>
        <div className="h-px flex-1 bg-white/[0.06]" />
      </motion.div>
    );
  }
  return null;
}
