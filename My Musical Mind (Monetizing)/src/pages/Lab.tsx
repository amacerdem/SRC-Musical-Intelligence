/* ── Lab — MI Analysis Studio ────────────────────────────────────────
 *  Audio analysis with progressive 6D→12D→24D dimension visualization.
 *  Waveform + temporal overlay + agent chat + neurochemical gauges.
 *  ──────────────────────────────────────────────────────────────────── */

import { useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { FlaskConical, Send, Clock, Music2, Search } from "lucide-react";
import { useTranslation } from "react-i18next";

import { useLabStore } from "@/stores/useLabStore";
import { useActiveIdentity } from "@/hooks/useActiveIdentity";
import { useChatStore } from "@/stores/useChatStore";
import { pageTransition, fadeIn } from "@/design/animations";
import { beliefColors } from "@/design/tokens";

import { AudioInput } from "@/components/lab/AudioInput";
import { DepthSelector } from "@/components/lab/DepthSelector";
import { WaveformOverlay } from "@/components/lab/WaveformOverlay";
import { NeuroGauges } from "@/components/lab/NeuroGauges";
import { AnalysisSummary } from "@/components/lab/AnalysisSummary";
import { ChatMessage, TypingIndicator } from "@/components/chat/ChatMessage";
import { MiniOrganism } from "@/components/mind/MiniOrganism";

export function Lab() {
  const { t } = useTranslation();
  const identity = useActiveIdentity();
  const color = identity.color;

  /* ── Lab store ──────────────────────────────────── */
  const trackDetail = useLabStore((s) => s.trackDetail);
  const depth = useLabStore((s) => s.depth);
  const setDepth = useLabStore((s) => s.setDepth);
  const temporal = useLabStore((s) => s.temporal);
  const phase = useLabStore((s) => s.phase);
  const setPhase = useLabStore((s) => s.setPhase);
  const progress = useLabStore((s) => s.progress);
  const setActiveTab = useLabStore((s) => s.setActiveTab);

  /* ── Chat store ─────────────────────────────────── */
  const messages = useChatStore((s) => s.messages);
  const isLoading = useChatStore((s) => s.isLoading);
  const statusText = useChatStore((s) => s.statusText);
  const error = useChatStore((s) => s.error);
  const sendMessage = useChatStore((s) => s.sendMessage);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages.length, isLoading]);

  const handleSend = () => {
    const el = inputRef.current;
    if (!el) return;
    const text = el.value.trim();
    if (!text || isLoading) return;
    sendMessage(text);
    el.value = "";
    el.style.height = "auto";
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = () => {
    const el = inputRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 80) + "px";
  };

  const hasAnalysis = phase === "done" && trackDetail && temporal;

  return (
    <motion.div {...pageTransition} className="relative min-h-screen">
      {/* Ambient background */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div
          className="absolute inset-0"
          style={{ background: `radial-gradient(ellipse 60% 50% at 30% 30%, ${color}06 0%, transparent 60%)` }}
        />
        <div
          className="absolute inset-0"
          style={{ background: `radial-gradient(ellipse 40% 40% at 70% 70%, ${beliefColors.consonance.primary}04 0%, transparent 50%)` }}
        />
      </div>
      <div className="cinematic-vignette z-[1] pointer-events-none fixed inset-0" />

      {/* ═══ MAIN LAYOUT ══════════════════════════════════════════ */}
      <div className="relative z-10 grid grid-cols-12 gap-4 min-h-[calc(100vh-8rem)]">

        {/* ═ LEFT: Analysis Area (8 cols) ═════════════════════════ */}
        <div className="col-span-12 lg:col-span-8 flex flex-col gap-3">

          {/* ── Header: Title + Input + Depth ──────────────────── */}
          <motion.div
            {...fadeIn}
            className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3"
          >
            <div className="flex items-center gap-2.5">
              <FlaskConical size={18} style={{ color }} />
              <h1 className="text-lg font-display font-bold" style={{ color }}>
                Lab
              </h1>
              <span className="text-xs font-display text-slate-600 font-light">Analysis Studio</span>
            </div>
            <DepthSelector depth={depth} onChange={setDepth} accentColor={color} />
          </motion.div>

          {/* ── Audio Input ────────────────────────────────────── */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1, duration: 0.6 }}
            className="spatial-card p-3"
          >
            <AudioInput accentColor={color} />
          </motion.div>

          {/* ── Analysis Result Area ───────────────────────────── */}
          {phase === "analyzing" && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="spatial-card p-6 flex flex-col items-center justify-center gap-3"
            >
              <div className="w-full max-w-xs">
                <div className="h-1 rounded-full bg-white/5 overflow-hidden">
                  <motion.div
                    className="h-full rounded-full"
                    style={{ background: color }}
                    animate={{ width: `${progress}%` }}
                    transition={{ duration: 0.5 }}
                  />
                </div>
              </div>
              <span className="text-xs font-mono text-slate-500">
                Analyzing... {Math.round(progress)}%
              </span>
            </motion.div>
          )}

          {phase === "error" && (
            <motion.div
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              className="spatial-card p-5 flex flex-col items-center gap-4"
            >
              <div className="w-10 h-10 rounded-full flex items-center justify-center" style={{ background: "rgba(239,68,68,0.08)", border: "1px solid rgba(239,68,68,0.15)" }}>
                <FlaskConical size={18} className="text-red-400/60" />
              </div>
              <div className="text-center">
                <p className="text-sm text-slate-300 font-display mb-1">Backend not reachable</p>
                <p className="text-xs text-slate-600 font-body leading-relaxed max-w-[320px]">
                  Upload and microphone require the MI-Lab backend running at localhost:8000.
                </p>
              </div>
              <button
                onClick={() => { setActiveTab("dataset"); setPhase("idle"); }}
                className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-display transition-all duration-300"
                style={{ background: `${color}15`, color, border: `1px solid ${color}25` }}
              >
                <Search size={14} />
                Browse Dataset
              </button>
              <code className="text-[10px] font-mono text-slate-600 px-2 py-1 rounded bg-white/[0.03] border border-white/[0.06]">
                cd Lab/backend && uvicorn main:app --port 8000
              </code>
            </motion.div>
          )}

          {hasAnalysis && (
            <>
              {/* Track info bar */}
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.15, duration: 0.6 }}
                className="flex items-center gap-3 px-3 py-2 rounded-lg"
                style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.04)" }}
              >
                <Music2 size={14} className="text-slate-600 flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <span className="text-sm font-display text-slate-300">{trackDetail.title}</span>
                  <span className="text-xs text-slate-600 ml-2">{trackDetail.artist}</span>
                </div>
                <div className="flex items-center gap-1.5 text-slate-600">
                  <Clock size={11} />
                  <span className="text-[11px] font-mono">
                    {Math.floor(trackDetail.duration_s / 60)}:{Math.floor(trackDetail.duration_s % 60).toString().padStart(2, "0")}
                  </span>
                </div>
              </motion.div>

              {/* Waveform + Dimension Overlay */}
              <motion.div
                initial={{ opacity: 0, y: 12, filter: "blur(8px)" }}
                animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
                transition={{ delay: 0.2, duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
                className="spatial-card p-4"
              >
                <WaveformOverlay
                  temporal={temporal}
                  depth={depth}
                  duration={trackDetail.duration_s}
                  accentColor={color}
                />
              </motion.div>

              {/* Neuro Gauges */}
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3, duration: 0.6 }}
                className="spatial-card p-3"
              >
                <NeuroGauges data={trackDetail.neuro_4d} />
              </motion.div>

              {/* Summary */}
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.35, duration: 0.6 }}
                className="spatial-card p-3"
              >
                <AnalysisSummary detail={trackDetail} depth={depth} accentColor={color} />
              </motion.div>
            </>
          )}

          {/* Empty state */}
          {phase === "idle" && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 0.5 }}
              transition={{ delay: 0.3, duration: 1 }}
              className="flex-1 flex flex-col items-center justify-center gap-4 py-12"
            >
              <FlaskConical size={36} className="text-slate-800" />
              <p className="text-sm font-body text-slate-700 text-center max-w-[260px]">
                Select a track, upload audio, or record from your microphone to begin analysis.
              </p>
            </motion.div>
          )}
        </div>

        {/* ═ RIGHT: Agent Chat (4 cols) ═══════════════════════════ */}
        <motion.div
          initial={{ opacity: 0, x: 20, filter: "blur(12px)" }}
          animate={{ opacity: 1, x: 0, filter: "blur(0px)" }}
          transition={{ duration: 0.8, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
          className="col-span-12 lg:col-span-4 flex flex-col min-h-0 rounded-2xl overflow-hidden relative"
          style={{ maxHeight: "calc(100vh - 8rem)" }}
        >
          {/* Glass panel */}
          <div
            className="absolute inset-0 rounded-2xl pointer-events-none"
            style={{
              background: "rgba(0, 0, 0, 0.45)",
              backdropFilter: "blur(20px)",
              WebkitBackdropFilter: "blur(20px)",
              border: `1px solid ${color}10`,
              boxShadow: `0 0 40px ${color}04, 0 8px 24px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.03)`,
            }}
          />

          {/* Content */}
          <div className="relative z-10 flex flex-col flex-1 min-h-0">
            {/* Chat Header */}
            <div
              className="flex-shrink-0 flex items-center gap-3 px-4 py-3 border-b border-white/[0.06]"
              style={{ background: `${color}04` }}
            >
              <motion.div
                animate={{ scale: [1, 1.05, 1] }}
                transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
              >
                <MiniOrganism color={color} size={28} animated />
              </motion.div>
              <div className="flex-1">
                <div className="text-sm font-display font-medium text-white/90">
                  Lab Assistant
                </div>
                <div className="text-[10px] font-mono" style={{ color: `${color}60` }}>
                  Analysis Interpreter
                </div>
              </div>
            </div>

            {/* Chat Messages */}
            <div
              ref={scrollRef}
              className="flex-1 min-h-0 overflow-y-auto px-4 py-4 space-y-3 scroll-smooth"
              style={{ scrollbarWidth: "thin", scrollbarColor: `${color}30 transparent` }}
            >
              {messages.length === 0 && !isLoading && (
                <div className="flex flex-col items-center justify-center h-full gap-3 py-6">
                  <MiniOrganism color={color} size={40} animated />
                  <p className="text-sm text-slate-500 font-body text-center max-w-[200px] leading-relaxed">
                    Select a track to analyze, then ask me about the results.
                  </p>
                </div>
              )}

              {messages.map((msg) => (
                <ChatMessage
                  key={msg.id}
                  role={msg.role}
                  content={msg.content}
                  accentColor={color}
                />
              ))}

              {isLoading && <TypingIndicator accentColor={color} statusText={statusText} />}

              {error && (
                <div className="text-center py-2">
                  <p className="text-xs text-red-400/70 font-body">{t("chat.error")}</p>
                </div>
              )}
            </div>

            {/* Chat Input */}
            <div className="flex items-end gap-2 px-3 py-3 border-t border-white/[0.06]">
              <textarea
                ref={inputRef}
                onChange={handleInput}
                onKeyDown={handleKeyDown}
                placeholder="Ask about the analysis..."
                disabled={isLoading}
                rows={1}
                className="flex-1 resize-none bg-white/[0.04] border border-white/[0.08] rounded-xl px-3 py-2 text-sm text-slate-200 placeholder:text-slate-600 outline-none focus:border-white/[0.15] transition-colors font-body"
                style={{ maxHeight: 80 }}
              />
              <button
                onClick={handleSend}
                disabled={isLoading}
                className="flex-shrink-0 w-8 h-8 rounded-xl flex items-center justify-center transition-all duration-200 disabled:opacity-30"
                style={{ background: `${color}20`, border: `1px solid ${color}30` }}
              >
                <Send size={14} style={{ color }} />
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
}
