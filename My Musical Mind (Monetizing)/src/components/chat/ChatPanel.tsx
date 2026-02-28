import { useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { X, Trash2 } from "lucide-react";
import { useTranslation } from "react-i18next";
import { useChatStore } from "@/stores/useChatStore";
import { useMobile } from "@/hooks/useMediaQuery";
import { MiniOrganism } from "@/components/mind/MiniOrganism";
import { ChatMessage, TypingIndicator } from "./ChatMessage";
import { ChatInput } from "./ChatInput";

interface Props {
  personaName: string;
  accentColor: string;
}

export function ChatPanel({ personaName, accentColor }: Props) {
  const { t } = useTranslation();
  const isMobile = useMobile();
  const messages = useChatStore((s) => s.messages);
  const isLoading = useChatStore((s) => s.isLoading);
  const error = useChatStore((s) => s.error);
  const close = useChatStore((s) => s.close);
  const sendMessage = useChatStore((s) => s.sendMessage);
  const clearChat = useChatStore((s) => s.clearChat);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    const el = scrollRef.current;
    if (el) {
      el.scrollTop = el.scrollHeight;
    }
  }, [messages.length, isLoading]);

  const panelContent = (
    <>
      {/* Header */}
      <div
        className="flex items-center justify-between px-4 py-3 border-b border-white/[0.06]"
        style={{ background: `${accentColor}08` }}
      >
        <div className="flex items-center gap-2.5">
          <MiniOrganism color={accentColor} size={28} animated />
          <div>
            <div className="text-sm font-display font-medium text-white/90">
              {personaName}
            </div>
            <div className="text-[10px] text-slate-500 font-mono">
              {t("chat.title")}
            </div>
          </div>
        </div>
        <div className="flex items-center gap-1">
          {messages.length > 0 && (
            <button
              onClick={clearChat}
              className="w-8 h-8 rounded-lg flex items-center justify-center text-slate-600 hover:text-slate-400 transition-colors"
              title={t("chat.clear")}
            >
              <Trash2 size={14} />
            </button>
          )}
          <button
            onClick={close}
            className="w-8 h-8 rounded-lg flex items-center justify-center text-slate-500 hover:text-slate-300 transition-colors"
          >
            <X size={16} />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto px-3 py-3 space-y-3 scroll-smooth"
      >
        {messages.length === 0 && !isLoading && (
          <div className="flex flex-col items-center justify-center h-full gap-3 py-12">
            <MiniOrganism color={accentColor} size={48} animated />
            <p className="text-sm text-slate-500 text-center max-w-[240px] font-body">
              {t("chat.welcome")}
            </p>
          </div>
        )}

        {messages.map((msg) => (
          <ChatMessage
            key={msg.id}
            role={msg.role}
            content={msg.content}
            accentColor={accentColor}
          />
        ))}

        {isLoading && <TypingIndicator accentColor={accentColor} />}

        {error && (
          <div className="text-center py-2">
            <p className="text-xs text-red-400/70 font-body">{t("chat.error")}</p>
            <button
              onClick={() => {
                const lastUser = [...messages].reverse().find((m) => m.role === "user");
                if (lastUser) sendMessage(lastUser.content);
              }}
              className="text-xs text-slate-500 hover:text-slate-300 mt-1 transition-colors"
            >
              {t("chat.retry")}
            </button>
          </div>
        )}
      </div>

      {/* Input */}
      <ChatInput
        onSend={sendMessage}
        disabled={isLoading}
        accentColor={accentColor}
      />
    </>
  );

  // Mobile: full-screen overlay
  if (isMobile) {
    return (
      <motion.div
        initial={{ opacity: 0, y: "100%" }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: "100%" }}
        transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
        className="fixed inset-0 z-[60] flex flex-col bg-black/95 backdrop-blur-xl"
        style={{
          paddingTop: "env(safe-area-inset-top, 0px)",
          paddingBottom: "env(safe-area-inset-bottom, 0px)",
        }}
      >
        {panelContent}
      </motion.div>
    );
  }

  // Desktop: floating panel above bubble
  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: 20, scale: 0.95 }}
      transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
      className="fixed z-[55] flex flex-col overflow-hidden"
      style={{
        width: 380,
        height: 520,
        bottom: 80,
        left: "50%",
        transform: "translateX(-50%)",
        background: "rgba(0, 0, 0, 0.92)",
        backdropFilter: "blur(24px)",
        border: `1px solid ${accentColor}15`,
        borderRadius: 20,
        boxShadow: `0 0 60px ${accentColor}08, 0 20px 50px rgba(0,0,0,0.5)`,
      }}
    >
      {panelContent}
    </motion.div>
  );
}
