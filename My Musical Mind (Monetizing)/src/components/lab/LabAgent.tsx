/* ── LabAgent — Living M³ orb + expandable analysis chat panel ────────
 *  A mesmerizing green orb with orbiting light particles sits below
 *  the waveform. Clicking it smoothly expands a chat panel on the
 *  left side. The agent auto-loads current track context and starts
 *  fresh each time.
 *  ──────────────────────────────────────────────────────────────────── */

import { useState, useEffect, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Send } from "lucide-react";
import { useTranslation } from "react-i18next";
import { useChatStore } from "@/stores/useChatStore";
import { ChatMessage, TypingIndicator } from "@/components/chat/ChatMessage";
import { MiniOrganism } from "@/components/mind/MiniOrganism";
import type { MITrackDetail } from "@/types/mi-dataset";
import type { MelData } from "./peakExtractor";
import type { TemporalDimensions } from "@/stores/useLabStore";

/* ── Types ───────────────────────────────────────────────────────────── */

interface Props {
  accentColor: string;
  trackDetail: MITrackDetail | null;
  melData: MelData | null;
  temporal: TemporalDimensions | null;
}

/* ── Orb color ───────────────────────────────────────────────────────── */

const ORB_COLOR = "#22C55E";
const PANEL_WIDTH = 475;

/* ── Component ──────────────────────────────────────────────────────── */

export function LabAgent({ accentColor, trackDetail, melData, temporal }: Props) {
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  /* ── Chat store ─────────────────────────────────── */
  const messages = useChatStore((s) => s.messages);
  const isLoading = useChatStore((s) => s.isLoading);
  const statusText = useChatStore((s) => s.statusText);
  const streamingContent = useChatStore((s) => s.streamingContent);
  const error = useChatStore((s) => s.error);
  const sendMessage = useChatStore((s) => s.sendMessage);
  const clearChat = useChatStore((s) => s.clearChat);

  /* ── Input state ────────────────────────────────── */
  const [text, setText] = useState("");
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  /* ── Auto-scroll ────────────────────────────────── */
  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages.length, isLoading, streamingContent]);

  /* ── Focus input when opened ────────────────────── */
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 400);
    }
  }, [isOpen]);

  /* ── Open handler: always clear + inject track context ── */
  const handleOpen = useCallback(() => {
    clearChat();
    setIsOpen(true);
  }, [clearChat]);

  /* ── Send handler — first message gets track context prepended ── */
  const handleSend = useCallback(() => {
    const trimmed = text.trim();
    if (!trimmed || isLoading) return;

    // If this is the first message, prepend full analysis context
    if (messages.length === 0 && trackDetail) {
      const lines = [
        `[MI Lab Analysis Context]`,
        `Track: "${trackDetail.title}" by ${trackDetail.artist}`,
        `Duration: ${trackDetail.duration_s.toFixed(1)}s (${Math.floor(trackDetail.duration_s / 60)}m ${Math.floor(trackDetail.duration_s % 60)}s)`,
      ];
      if (melData) {
        lines.push(`Mel spectrogram: ${melData.nMels} bins × ${melData.nFrames} frames @ ${melData.frameRate.toFixed(2)} Hz`);
        lines.push(`Mel duration: ${(melData.nFrames / melData.frameRate).toFixed(1)}s`);
      }
      if (temporal) {
        lines.push(`Temporal data: ${temporal.frameCount} segments, source=${temporal.source}`);
        lines.push(`Segment keys: ${temporal.segments.length > 0 ? Object.keys(temporal.segments[0].psychology).join(", ") : "n/a"}`);
      }
      const ctx = lines.join("\n") + `\n\n${trimmed}`;
      sendMessage(ctx);
    } else {
      sendMessage(trimmed);
    }

    setText("");
    if (inputRef.current) inputRef.current.style.height = "auto";
  }, [text, isLoading, sendMessage, messages.length, trackDetail]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  /* ── Track info for welcome state ───────────────── */
  const trackTitle = trackDetail?.title ?? "";
  const trackArtist = trackDetail?.artist ?? "";

  return (
    <>
      {/* ── Living Orb (collapsed state) ─────────────────────── */}
      <AnimatePresence>
        {!isOpen && (
          <motion.button
            initial={{ opacity: 0, scale: 0.3 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.3 }}
            transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
            onClick={handleOpen}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            className="group relative flex items-center gap-3"
          >
            {/* The living orb container */}
            <div className="relative w-12 h-12">
              {/* Orbiting ring 1 — slow outer orbit */}
              <motion.div
                className="absolute inset-[-6px] rounded-full"
                style={{
                  border: `1.5px solid transparent`,
                  borderTopColor: `${ORB_COLOR}50`,
                  borderRightColor: `${ORB_COLOR}20`,
                }}
                animate={{ rotate: 360 }}
                transition={{ duration: isHovered ? 1.5 : 4, repeat: Infinity, ease: "linear" }}
              />

              {/* Orbiting ring 2 — faster inner orbit, opposite direction */}
              <motion.div
                className="absolute inset-[-2px] rounded-full"
                style={{
                  border: `1px solid transparent`,
                  borderBottomColor: `${ORB_COLOR}40`,
                  borderLeftColor: `${ORB_COLOR}15`,
                }}
                animate={{ rotate: -360 }}
                transition={{ duration: isHovered ? 1 : 3, repeat: Infinity, ease: "linear" }}
              />

              {/* Orbiting particle 1 */}
              <motion.div
                className="absolute w-1.5 h-1.5 rounded-full"
                style={{
                  background: ORB_COLOR,
                  boxShadow: `0 0 6px ${ORB_COLOR}, 0 0 12px ${ORB_COLOR}80`,
                  top: "50%",
                  left: "50%",
                }}
                animate={{
                  x: ["-50%", "18px", "-50%", "-24px", "-50%"],
                  y: ["-24px", "-50%", "18px", "-50%", "-24px"],
                }}
                transition={{ duration: isHovered ? 2 : 5, repeat: Infinity, ease: "easeInOut" }}
              />

              {/* Orbiting particle 2 */}
              <motion.div
                className="absolute w-1 h-1 rounded-full"
                style={{
                  background: `${ORB_COLOR}cc`,
                  boxShadow: `0 0 4px ${ORB_COLOR}`,
                  top: "50%",
                  left: "50%",
                }}
                animate={{
                  x: ["20px", "-50%", "-20px", "-50%", "20px"],
                  y: ["-50%", "-20px", "-50%", "16px", "-50%"],
                }}
                transition={{ duration: isHovered ? 1.5 : 3.5, repeat: Infinity, ease: "easeInOut" }}
              />

              {/* Outer breath glow */}
              <motion.div
                className="absolute inset-[-8px] rounded-full"
                style={{
                  background: `radial-gradient(circle, ${ORB_COLOR}25 0%, transparent 70%)`,
                }}
                animate={{
                  scale: isHovered ? [1, 1.8, 1] : [1, 1.4, 1],
                  opacity: isHovered ? [0.8, 0.4, 0.8] : [0.5, 0.2, 0.5],
                }}
                transition={{ duration: isHovered ? 1.5 : 3, repeat: Infinity, ease: "easeInOut" }}
              />

              {/* Hover burst rings */}
              <AnimatePresence>
                {isHovered && (
                  <>
                    <motion.div
                      className="absolute inset-[-12px] rounded-full"
                      style={{ border: `1px solid ${ORB_COLOR}30` }}
                      initial={{ scale: 0.8, opacity: 0 }}
                      animate={{ scale: [1, 1.6], opacity: [0.6, 0] }}
                      exit={{ opacity: 0 }}
                      transition={{ duration: 1.2, repeat: Infinity, ease: "easeOut" }}
                    />
                    <motion.div
                      className="absolute inset-[-12px] rounded-full"
                      style={{ border: `1px solid ${ORB_COLOR}20` }}
                      initial={{ scale: 0.8, opacity: 0 }}
                      animate={{ scale: [1, 2], opacity: [0.4, 0] }}
                      exit={{ opacity: 0 }}
                      transition={{ duration: 1.5, repeat: Infinity, ease: "easeOut", delay: 0.3 }}
                    />
                  </>
                )}
              </AnimatePresence>

              {/* Core orb with MiniOrganism */}
              <motion.div
                className="absolute inset-0 rounded-full flex items-center justify-center overflow-hidden"
                style={{
                  background: `radial-gradient(circle at 35% 35%, ${ORB_COLOR}dd, ${ORB_COLOR}66 60%, ${ORB_COLOR}22 100%)`,
                  border: `1.5px solid ${ORB_COLOR}50`,
                }}
                animate={{
                  boxShadow: isHovered
                    ? [
                        `0 0 30px ${ORB_COLOR}70, 0 0 60px ${ORB_COLOR}35, inset 0 -3px 6px ${ORB_COLOR}30`,
                        `0 0 40px ${ORB_COLOR}90, 0 0 80px ${ORB_COLOR}45, inset 0 -3px 6px ${ORB_COLOR}30`,
                        `0 0 30px ${ORB_COLOR}70, 0 0 60px ${ORB_COLOR}35, inset 0 -3px 6px ${ORB_COLOR}30`,
                      ]
                    : [
                        `0 0 20px ${ORB_COLOR}40, 0 0 40px ${ORB_COLOR}15, inset 0 -3px 6px ${ORB_COLOR}30`,
                        `0 0 30px ${ORB_COLOR}60, 0 0 60px ${ORB_COLOR}25, inset 0 -3px 6px ${ORB_COLOR}30`,
                        `0 0 20px ${ORB_COLOR}40, 0 0 40px ${ORB_COLOR}15, inset 0 -3px 6px ${ORB_COLOR}30`,
                      ],
                  scale: isHovered ? 1.15 : 1,
                }}
                transition={{ duration: isHovered ? 1.2 : 2.5, repeat: Infinity, ease: "easeInOut" }}
              >
                <MiniOrganism color={ORB_COLOR} size={32} animated />
              </motion.div>
            </div>

            {/* Label text */}
            <div className="flex flex-col items-start">
              <span className="text-[11px] font-display font-semibold text-white/80 group-hover:text-white transition-colors">
                M³ {t("chat.labTitle")}
              </span>
              <motion.span
                className="text-[10px] font-display font-medium"
                style={{ color: `${ORB_COLOR}cc` }}
                animate={{ opacity: [0.6, 1, 0.6] }}
                transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
              >
                {t("chat.labAskMe")}
              </motion.span>
            </div>
          </motion.button>
        )}
      </AnimatePresence>

      {/* ── Expanded Chat Panel ───────────────────────────────── */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, width: 0, x: -20 }}
            animate={{ opacity: 1, width: PANEL_WIDTH, x: 0 }}
            exit={{ opacity: 0, width: 0, x: -20 }}
            transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
            className="fixed left-0 top-0 bottom-0 z-[55] flex flex-col overflow-hidden"
            style={{
              background: "rgba(6,6,14,0.96)",
              backdropFilter: "blur(24px)",
              borderRight: `1px solid rgba(255,255,255,0.06)`,
              boxShadow: `4px 0 40px rgba(0,0,0,0.4), 0 0 60px ${ORB_COLOR}05`,
            }}
          >
            {/* Header */}
            <div
              className="flex items-center justify-between px-4 py-3 border-b border-white/[0.06] flex-shrink-0"
              style={{ background: `${ORB_COLOR}06` }}
            >
              <div className="flex items-center gap-3">
                <MiniOrganism color={ORB_COLOR} size={28} animated />
                <div>
                  <div className="text-sm font-display font-medium text-white/90">
                    M³ {t("chat.labTitle")}
                  </div>
                  <div className="text-[10px] font-mono text-slate-500">
                    {t("chat.labSubtitle")}
                  </div>
                </div>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="w-8 h-8 rounded-lg flex items-center justify-center text-slate-500 hover:text-slate-300 transition-colors"
              >
                <X size={16} />
              </button>
            </div>

            {/* Track context bar */}
            {trackDetail && (
              <div className="flex items-center gap-2.5 px-4 py-2 border-b border-white/[0.04] flex-shrink-0"
                style={{ background: `${ORB_COLOR}04` }}
              >
                <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ background: ORB_COLOR }} />
                <span className="text-[11px] font-display text-slate-400 truncate">
                  {trackTitle}
                </span>
                <span className="text-[10px] font-mono text-slate-600 flex-shrink-0">
                  {trackArtist}
                </span>
              </div>
            )}

            {/* Messages */}
            <div
              ref={scrollRef}
              className="flex-1 overflow-y-auto px-3 py-3 space-y-3 scroll-smooth"
              style={{ scrollbarWidth: "thin" }}
            >
              {messages.length === 0 && !isLoading && (
                <div className="flex flex-col items-center justify-center h-full gap-4 py-12">
                  <MiniOrganism color={ORB_COLOR} size={48} animated />
                  <div className="text-center max-w-[280px]">
                    <p className="text-[13px] font-display text-white/70 mb-3">
                      {t("chat.labWelcome")}
                    </p>
                    <p className="text-[11px] text-slate-500 font-body leading-relaxed">
                      {t("chat.labWelcomeDetail")}
                    </p>
                  </div>
                </div>
              )}

              {messages.filter((msg) => msg.role !== "system").map((msg) => (
                <ChatMessage
                  key={msg.id}
                  role={msg.role as "user" | "assistant"}
                  content={msg.content}
                  accentColor={ORB_COLOR}
                />
              ))}

              {streamingContent && (
                <ChatMessage role="assistant" content={streamingContent} accentColor={ORB_COLOR} />
              )}
              {isLoading && !streamingContent && (
                <TypingIndicator accentColor={ORB_COLOR} statusText={statusText} />
              )}

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
            <div className="flex items-end gap-2 p-3 border-t border-white/[0.06] flex-shrink-0">
              <textarea
                ref={inputRef}
                value={text}
                onChange={(e) => {
                  setText(e.target.value);
                  const el = inputRef.current;
                  if (el) { el.style.height = "auto"; el.style.height = Math.min(el.scrollHeight, 120) + "px"; }
                }}
                onKeyDown={handleKeyDown}
                placeholder={t("chat.labPlaceholder")}
                disabled={isLoading}
                rows={1}
                className="flex-1 resize-none bg-white/[0.04] border border-white/[0.08] rounded-xl px-3.5 py-2.5 text-sm text-slate-200 placeholder:text-slate-600 outline-none focus:border-white/[0.15] transition-colors font-body"
                style={{ maxHeight: 120 }}
              />
              <button
                onClick={handleSend}
                disabled={isLoading || !text.trim()}
                className="flex-shrink-0 w-9 h-9 rounded-xl flex items-center justify-center transition-all duration-200 disabled:opacity-30"
                style={{
                  background: text.trim() && !isLoading ? `${ORB_COLOR}25` : "transparent",
                  border: `1px solid ${text.trim() && !isLoading ? ORB_COLOR + "40" : "transparent"}`,
                }}
              >
                <Send
                  size={16}
                  style={{ color: text.trim() && !isLoading ? ORB_COLOR : "#64748b" }}
                />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
