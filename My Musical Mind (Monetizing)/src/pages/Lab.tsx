/* ── Lab — MI Analysis Studio (Instrument Panel) ───────────────────────
 *  3-column + 2-row full-screen layout — no scroll.
 *
 *  ┌───────────┬─────────────────────────┬──────────────┐
 *  │  SOURCE   │     ANIMATED RADAR      │ LAB ASSIST   │  Row 1
 *  │  + SUMMARY│                         │ (chat)       │
 *  ├───────────┴─────────────────────────┴──────────────┤
 *  │            WAVEFORM OVERLAY (compact)              │  Row 2
 *  └────────────────────────────────────────────────────┘
 *  ──────────────────────────────────────────────────────────────────── */

import { useRef, useEffect, useMemo, useState, useCallback } from "react";
import { motion } from "framer-motion";
import { FlaskConical, Send, Clock, Music2, Search, Activity } from "lucide-react";
import { useTranslation } from "react-i18next";

import { useLabStore } from "@/stores/useLabStore";
import { useActiveIdentity } from "@/hooks/useActiveIdentity";
import { useChatStore } from "@/stores/useChatStore";
import { useM3Store } from "@/stores/useM3Store";
import { levelToOrganismStage } from "@/types/m3";
import { pageTransition, fadeIn } from "@/design/animations";
import { beliefColors } from "@/design/tokens";
import { ALL_PSYCHOLOGY } from "@/data/dimensions";

import { AudioInput } from "@/components/lab/AudioInput";
import { DepthSelector } from "@/components/lab/DepthSelector";
import { WaveformOverlay } from "@/components/lab/WaveformOverlay";
import { AnalysisSummary } from "@/components/lab/AnalysisSummary";
import { ChatMessage, TypingIndicator } from "@/components/chat/ChatMessage";
import { MiniOrganism } from "@/components/mind/MiniOrganism";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";

export function Lab() {
  const { t } = useTranslation();
  const identity = useActiveIdentity();
  const color = identity.color;
  const morphology = identity.morphology;
  const m3Mind = useM3Store((s) => s.mind);
  const organismStage = m3Mind ? levelToOrganismStage(m3Mind.level) : 1;

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
  const streamingContent = useChatStore((s) => s.streamingContent);
  const error = useChatStore((s) => s.error);
  const sendMessage = useChatStore((s) => s.sendMessage);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages.length, isLoading, streamingContent]);

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
    el.style.height = Math.min(el.scrollHeight, 72) + "px";
  };

  const handleWheel = (e: React.WheelEvent<HTMLDivElement>) => {
    const el = scrollRef.current;
    if (!el) return;
    e.stopPropagation();
    el.scrollTop += e.deltaY;
  };

  const hasAnalysis = phase === "done" && trackDetail && temporal;

  /* ── Radar data: overall + per-segment 6D ──────── */
  const overall6D = useMemo(
    () => temporal?.overall.psychology ?? [],
    [temporal],
  );
  const segments6D = useMemo(
    () => temporal?.segments.map((s) => s.psychology) ?? [],
    [temporal],
  );

  /* ── Flow animation — cycles through temporal segments ── */
  const [flowIdx, setFlowIdx] = useState(0);
  useEffect(() => {
    if (!hasAnalysis || segments6D.length <= 1) return;
    const stepMs = Math.max(180, 10000 / segments6D.length);
    const timer = setInterval(() => {
      setFlowIdx((prev) => (prev + 1) % segments6D.length);
    }, stepMs);
    return () => clearInterval(timer);
  }, [hasAnalysis, segments6D.length]);

  const flowValues = segments6D[flowIdx] ?? overall6D;

  /* ── Flow time indicator ────────────────────────── */
  const flowTime = useMemo(() => {
    if (!trackDetail || segments6D.length <= 1) return "";
    const secs = (flowIdx / Math.max(1, segments6D.length - 1)) * trackDetail.duration_s;
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  }, [flowIdx, segments6D.length, trackDetail]);

  /* ── Responsive radar sizing via ResizeObserver ── */
  const radarCellRef = useRef<HTMLDivElement>(null);
  const [radarSize, setRadarSize] = useState(320);
  useEffect(() => {
    const el = radarCellRef.current;
    if (!el) return;
    const ro = new ResizeObserver((entries) => {
      const { width, height } = entries[0].contentRect;
      setRadarSize(Math.max(200, Math.min(width - 48, height - 24, 440)));
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  return (
    <motion.div {...pageTransition} className="relative h-screen overflow-hidden">

      {/* ── Ambient background ─────────────────────────────────────── */}
      <div className="absolute inset-0 z-0">
        <div className="absolute inset-0" style={{ background: `radial-gradient(ellipse 80% 60% at 50% 30%, ${color}08 0%, transparent 60%)` }} />
        <div className="absolute inset-0" style={{ background: `radial-gradient(ellipse 50% 40% at 20% 80%, ${color}05 0%, transparent 50%)` }} />
        <div className="absolute inset-0" style={{ background: `radial-gradient(ellipse 40% 35% at 80% 70%, ${beliefColors.consonance.primary}04 0%, transparent 50%)` }} />
      </div>
      <div className="cinematic-vignette z-[2]" />

      {/* ═══ MAIN ═════════════════════════════════════════════════════ */}
      <div className="relative z-10 h-full flex flex-col px-5 sm:px-8 md:px-10 pt-6 pb-24">

        {/* ── Header ──────────────────────────────────────────────── */}
        <motion.div {...fadeIn} className="flex items-center justify-between pb-3 flex-shrink-0">
          <div className="flex items-center gap-2.5">
            <FlaskConical size={18} style={{ color }} />
            <h1 className="text-lg font-display font-bold" style={{ color }}>Lab</h1>
            <span className="text-xs font-display text-slate-600 font-light">Analysis Studio</span>
          </div>

          {/* Track info — center (visible when analysis done) */}
          {hasAnalysis && (
            <motion.div
              initial={{ opacity: 0, y: -6 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex items-center gap-2.5"
            >
              <Music2 size={13} className="text-slate-500" />
              <span className="text-xs font-display text-slate-300">{trackDetail.title}</span>
              <span className="text-[10px] text-slate-600">{trackDetail.artist}</span>
              <div className="flex items-center gap-1 text-slate-600">
                <Clock size={10} />
                <span className="text-[10px] font-mono">
                  {Math.floor(trackDetail.duration_s / 60)}:{Math.floor(trackDetail.duration_s % 60).toString().padStart(2, "0")}
                </span>
              </div>
            </motion.div>
          )}

          {/* Legend + Depth selector */}
          <div className="flex items-center gap-4">
            {hasAnalysis && (
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-1.5">
                  <div className="w-3 h-[2px] rounded-full bg-red-500" />
                  <span className="text-[9px] font-display text-slate-500">Total</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="w-3 h-[2px] rounded-full" style={{ background: color }} />
                  <span className="text-[9px] font-display text-slate-500">Flow</span>
                </div>
                {flowTime && (
                  <span className="text-[10px] font-mono" style={{ color: `${color}60` }}>{flowTime}</span>
                )}
              </div>
            )}
            <DepthSelector depth={depth} onChange={setDepth} accentColor={color} />
          </div>
        </motion.div>

        {/* ── 3-COL × 2-ROW GRID ─────────────────────────────────── */}
        <div
          className="flex-1 min-h-0 grid gap-0"
          style={{
            gridTemplateColumns: "240px 1fr 280px",
            gridTemplateRows: "1fr minmax(140px, 200px)",
          }}
        >

          {/* ═ COL 1 — Source + Summary ═══════════════════════════ */}
          <div
            className="flex flex-col min-h-0 overflow-hidden border-r border-white/[0.04]"
            style={{ gridRow: "1 / 2", gridColumn: "1 / 2" }}
          >
            <motion.div
              initial={{ opacity: 0, x: -12 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.15, ease: [0.22, 1, 0.36, 1] }}
              className="flex flex-col h-full"
            >
              {/* Audio Input — fills top portion */}
              <div className="flex-1 min-h-0 px-3 py-3">
                <AudioInput accentColor={color} />
              </div>

              {/* Analysis Summary — bottom of col 1 (when available) */}
              {hasAnalysis && (
                <motion.div
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4, duration: 0.6 }}
                  className="flex-shrink-0 px-3 py-2.5 border-t border-white/[0.04]"
                >
                  <AnalysisSummary detail={trackDetail} depth={depth} accentColor={color} temporal={temporal} />
                </motion.div>
              )}
            </motion.div>
          </div>

          {/* ═ COL 2 — Animated Radar (center stage) ══════════════ */}
          <div
            ref={radarCellRef}
            className="flex items-center justify-center min-h-0 overflow-hidden relative"
            style={{ gridRow: "1 / 2", gridColumn: "2 / 3" }}
          >
            {/* ── Idle state ────────────────────────── */}
            {phase === "idle" && (
              <div className="flex flex-col items-center justify-center gap-5 relative">
                <motion.div
                  animate={{ scale: [1, 1.08, 1], opacity: [0.25, 0.45, 0.25] }}
                  transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                >
                  <FlaskConical size={48} className="text-slate-700" />
                </motion.div>
                <p className="text-sm font-body text-slate-600 text-center max-w-[240px] leading-relaxed">
                  Select a track to begin analysis.
                </p>
                {/* Faded grid placeholder */}
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-[0.03]">
                  {[70, 110, 150, 190].map((r) => (
                    <div key={r} className="absolute rounded-full border border-white/40" style={{ width: r * 2, height: r * 2 }} />
                  ))}
                </div>
              </div>
            )}

            {/* ── Analyzing state ───────────────────── */}
            {phase === "analyzing" && (
              <div className="flex flex-col items-center justify-center gap-5 relative">
                <motion.div animate={{ rotate: 360 }} transition={{ duration: 4, repeat: Infinity, ease: "linear" }}>
                  <FlaskConical size={36} style={{ color: `${color}50` }} />
                </motion.div>
                <div className="w-48">
                  <div className="h-1.5 rounded-full bg-white/5 overflow-hidden">
                    <motion.div className="h-full rounded-full"
                      style={{ background: color, boxShadow: `0 0 12px ${color}60` }}
                      animate={{ width: `${progress}%` }} transition={{ duration: 0.5 }}
                    />
                  </div>
                </div>
                <span className="text-xs font-mono text-slate-500">Analyzing... {Math.round(progress)}%</span>
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                  {[100, 150, 200].map((r, i) => (
                    <motion.div key={r} className="absolute rounded-full"
                      style={{ width: r * 2, height: r * 2, border: `1px solid ${color}` }}
                      animate={{ opacity: [0.03, 0.08, 0.03], scale: [1, 1.02, 1] }}
                      transition={{ duration: 3, delay: i * 0.5, repeat: Infinity, ease: "easeInOut" }}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* ── Error state ───────────────────────── */}
            {phase === "error" && (
              <div className="flex flex-col items-center justify-center gap-4">
                <FlaskConical size={40} className="text-red-400/20" />
                <p className="text-xs font-body text-slate-600 text-center max-w-[200px]">
                  Waiting for audio input...
                </p>
              </div>
            )}

            {/* ── Analysis done — Animated Radar ───── */}
            {hasAnalysis && (
              <div className="flex flex-col items-center">
                <LabRadar overall={overall6D} flow={flowValues} color={color} size={radarSize} />
                {/* Flow progress bar below radar */}
                <div style={{ width: Math.min(radarSize - 40, 280) }} className="mt-2">
                  <div className="h-[2px] rounded-full bg-white/5 overflow-hidden">
                    <motion.div className="h-full rounded-full" style={{ background: color, opacity: 0.6 }}
                      animate={{ width: `${((flowIdx + 1) / Math.max(1, segments6D.length)) * 100}%` }}
                      transition={{ duration: 0.3 }}
                    />
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* ═ COL 3 — Lab Assistant Chat ══════════════════════════ */}
          <motion.div
            initial={{ opacity: 0, x: 12 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
            className="flex flex-col min-h-0 overflow-hidden relative border-l border-white/[0.04]"
            style={{ gridRow: "1 / 2", gridColumn: "3 / 4" }}
          >
            {/* Organism background */}
            <div className="absolute inset-0 z-0 pointer-events-none" style={{ transform: "scale(1.3)", transformOrigin: "center 40%" }}>
              <MindOrganismCanvas
                color={color} secondaryColor={`${color}80`}
                stage={organismStage} intensity={0.4} breathRate={5}
                familyMorphology={morphology} className="w-full h-full"
                variant="hero" constellations interactive={false}
              />
            </div>

            {/* Glass overlay */}
            <div className="absolute inset-0 z-[1] pointer-events-none" style={{
              background: "rgba(0, 0, 0, 0.6)",
              backdropFilter: "blur(20px)", WebkitBackdropFilter: "blur(20px)",
              border: `1px solid ${color}08`,
              boxShadow: `0 0 40px ${color}04, inset 0 1px 0 rgba(255,255,255,0.03)`,
            }} />

            {/* Chat content */}
            <div className="absolute inset-0 z-[2] flex flex-col overflow-hidden">

              {/* Chat Header */}
              <div className="flex-shrink-0 flex items-center gap-2 px-3 py-2 border-b border-white/[0.06]" style={{ background: `${color}04` }}>
                <motion.div animate={{ scale: [1, 1.05, 1] }} transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}>
                  <MiniOrganism color={color} size={24} animated />
                </motion.div>
                <div className="flex-1 min-w-0">
                  <div className="text-xs font-display font-medium text-white/90">Lab Assistant</div>
                  <div className="text-[9px] font-mono" style={{ color: `${color}60` }}>Analysis Interpreter</div>
                </div>
              </div>

              {/* Error panel */}
              {phase === "error" && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                  className="flex-shrink-0 px-3 py-2 border-b border-white/[0.06]" style={{ background: "rgba(239,68,68,0.03)" }}
                >
                  <div className="flex items-center gap-2">
                    <div className="w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0"
                      style={{ background: "rgba(239,68,68,0.08)", border: "1px solid rgba(239,68,68,0.15)" }}
                    >
                      <FlaskConical size={11} className="text-red-400/60" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-[10px] text-slate-300 font-display">Backend not reachable</p>
                      <p className="text-[9px] text-slate-600 font-body">localhost:8000</p>
                    </div>
                    <button onClick={() => { setActiveTab("dataset"); setPhase("idle"); }}
                      className="flex items-center gap-1 px-2 py-1 rounded-lg text-[10px] font-display transition-all flex-shrink-0"
                      style={{ background: `${color}15`, color, border: `1px solid ${color}25` }}
                    >
                      <Search size={10} /> Dataset
                    </button>
                  </div>
                </motion.div>
              )}

              {/* Analyzing progress strip */}
              {phase === "analyzing" && (
                <div className="flex-shrink-0 px-3 py-1.5 border-b border-white/[0.06]">
                  <div className="flex items-center gap-2">
                    <motion.div animate={{ rotate: 360 }} transition={{ duration: 2, repeat: Infinity, ease: "linear" }}>
                      <Activity size={11} style={{ color }} />
                    </motion.div>
                    <div className="flex-1 h-1 rounded-full bg-white/5 overflow-hidden">
                      <motion.div className="h-full rounded-full" style={{ background: color }}
                        animate={{ width: `${progress}%` }} transition={{ duration: 0.5 }} />
                    </div>
                    <span className="text-[9px] font-mono text-slate-500">{Math.round(progress)}%</span>
                  </div>
                </div>
              )}

              {/* Chat Messages */}
              <div ref={scrollRef} onWheel={handleWheel}
                className="flex-1 min-h-0 overflow-y-scroll px-3 py-3 space-y-2"
                style={{ scrollbarWidth: "thin", scrollbarColor: `${color}30 transparent`, overscrollBehavior: "contain" }}
              >
                {messages.length === 0 && !isLoading && (
                  <div className="flex flex-col items-center justify-center h-full gap-3 py-6">
                    <motion.div initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}
                      transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
                    >
                      <MiniOrganism color={color} size={36} animated />
                    </motion.div>
                    <motion.p initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.3, duration: 0.8 }}
                      className="text-xs text-slate-400 font-body text-center max-w-[200px] leading-relaxed"
                    >
                      Select a track to analyze, then ask me about the results.
                    </motion.p>
                  </div>
                )}

                {messages.map((msg) => (
                  <ChatMessage key={msg.id} role={msg.role} content={msg.content} accentColor={color} />
                ))}
                {streamingContent && <ChatMessage role="assistant" content={streamingContent} accentColor={color} />}
                {isLoading && !streamingContent && <TypingIndicator accentColor={color} statusText={statusText} />}
                {error && (
                  <div className="text-center py-1">
                    <p className="text-[10px] text-red-400/70 font-body">{t("chat.error")}</p>
                  </div>
                )}
              </div>

              {/* Chat Input */}
              <div className="flex-shrink-0 flex items-end gap-1.5 px-2 py-2 border-t border-white/[0.06]">
                <textarea ref={inputRef} onChange={handleInput} onKeyDown={handleKeyDown}
                  placeholder="Ask about the analysis..." disabled={isLoading} rows={1}
                  className="flex-1 resize-none bg-white/[0.04] border border-white/[0.08] rounded-lg px-2.5 py-2 text-xs text-slate-200 placeholder:text-slate-600 outline-none focus:border-white/[0.15] transition-colors font-body"
                  style={{ maxHeight: 72 }}
                />
                <button onClick={handleSend} disabled={isLoading}
                  className="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center transition-all duration-200 disabled:opacity-30"
                  style={{ background: `${color}20`, border: `1px solid ${color}30` }}
                >
                  <Send size={14} style={{ color }} />
                </button>
              </div>
            </div>
          </motion.div>

          {/* ═ ROW 2 — Waveform (spans all 3 columns) ═════════════ */}
          <div
            className="min-h-0 overflow-hidden border-t border-white/[0.06]"
            style={{ gridRow: "2 / 3", gridColumn: "1 / -1" }}
          >
            {hasAnalysis ? (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3, duration: 0.6 }}
                className="h-full flex flex-col px-4 py-2"
              >
                <div className="flex items-center gap-2 mb-1 flex-shrink-0">
                  <Activity size={11} className="text-slate-600" />
                  <span className="text-[10px] font-display font-light tracking-[0.12em] uppercase text-slate-500">
                    Temporal Flow
                  </span>
                </div>
                <div className="flex-1 min-h-0">
                  <WaveformOverlay temporal={temporal} depth={depth} duration={trackDetail.duration_s} accentColor={color} compact />
                </div>
              </motion.div>
            ) : (
              <div className="h-full flex items-center justify-center">
                <div className="flex items-center gap-2 text-slate-700">
                  <Activity size={14} />
                  <span className="text-[10px] font-display font-light tracking-[0.12em] uppercase">
                    Temporal Flow
                  </span>
                </div>
              </div>
            )}
          </div>

        </div>
      </div>
    </motion.div>
  );
}


/* ═══════════════════════════════════════════════════════════════════════
 *  LabRadar — Custom Animated 6D Hexagonal Radar
 *  Red polygon = overall average ("Total")
 *  Persona-color polygon = flow-synced segment ("Flow")
 *  Smooth animation via framer-motion SVG path morphing.
 * ═══════════════════════════════════════════════════════════════════════ */

const RADAR_ANGLES = Array.from({ length: 6 }, (_, i) => (-90 + i * 60) * (Math.PI / 180));

function LabRadar({ overall, flow, color, size }: {
  overall: number[];
  flow: number[];
  color: string;
  size: number;
}) {
  const cx = size / 2;
  const cy = size / 2;
  const maxR = size * 0.38;
  const labelR = maxR + 24;

  const toPath = useCallback((vals: number[]) => {
    const pts = RADAR_ANGLES.map((a, i) => {
      const r = maxR * Math.max(0, Math.min(1, vals[i] ?? 0));
      return `${cx + Math.cos(a) * r} ${cy + Math.sin(a) * r}`;
    });
    return `M ${pts.join(" L ")} Z`;
  }, [cx, cy, maxR]);

  const gridPath = useCallback((scale: number) => {
    const pts = RADAR_ANGLES.map((a) =>
      `${cx + Math.cos(a) * maxR * scale} ${cy + Math.sin(a) * maxR * scale}`
    );
    return `M ${pts.join(" L ")} Z`;
  }, [cx, cy, maxR]);

  const totalPts = useMemo(() =>
    RADAR_ANGLES.map((a, i) => {
      const r = maxR * Math.max(0, Math.min(1, overall[i] ?? 0));
      return { x: cx + Math.cos(a) * r, y: cy + Math.sin(a) * r };
    }),
  [overall, cx, cy, maxR]);

  const flowPts = useMemo(() =>
    RADAR_ANGLES.map((a, i) => {
      const r = maxR * Math.max(0, Math.min(1, flow[i] ?? 0));
      return { x: cx + Math.cos(a) * r, y: cy + Math.sin(a) * r };
    }),
  [flow, cx, cy, maxR]);

  const ease = [0.22, 1, 0.36, 1] as [number, number, number, number];

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="overflow-visible">

      {/* Grid hexagons */}
      {[0.25, 0.5, 0.75, 1].map((s) => (
        <path key={s} d={gridPath(s)} fill="none"
          stroke={s === 1 ? "rgba(255,255,255,0.08)" : "rgba(255,255,255,0.04)"}
          strokeWidth={s === 1 ? 0.8 : 0.5}
        />
      ))}

      {/* Axis lines */}
      {RADAR_ANGLES.map((a, i) => (
        <line key={i}
          x1={cx} y1={cy}
          x2={cx + Math.cos(a) * maxR}
          y2={cy + Math.sin(a) * maxR}
          stroke="rgba(255,255,255,0.05)" strokeWidth={0.5}
        />
      ))}

      {/* Center dot */}
      <circle cx={cx} cy={cy} r={1.5} fill="rgba(255,255,255,0.1)" />

      {/* ── Red total polygon ────────────────────── */}
      <path
        d={toPath(overall)}
        fill="rgba(239,68,68,0.10)"
        stroke="#EF4444"
        strokeWidth={1.5}
        strokeLinejoin="round"
        opacity={0.85}
      />

      {/* ── Animated flow polygon ────────────────── */}
      <motion.path
        initial={false}
        animate={{ d: toPath(flow) }}
        transition={{ duration: 0.35, ease }}
        fill={`${color}12`}
        stroke={color}
        strokeWidth={2}
        strokeLinejoin="round"
        style={{ filter: `drop-shadow(0 0 10px ${color}40)` }}
      />

      {/* Total data dots — red */}
      {totalPts.map((pt, i) => (
        <circle key={`t${i}`}
          cx={pt.x} cy={pt.y} r={2.5}
          fill="#EF4444" stroke="#0a0a0f" strokeWidth={0.8}
        />
      ))}

      {/* Flow data dots — animated, persona color */}
      {RADAR_ANGLES.map((_, i) => (
        <motion.circle key={`f${i}`}
          initial={false}
          animate={{ cx: flowPts[i].x, cy: flowPts[i].y }}
          transition={{ duration: 0.35, ease }}
          r={3.5}
          fill={color}
          stroke="#0a0a0f"
          strokeWidth={1}
          style={{ filter: `drop-shadow(0 0 6px ${color}80)` }}
        />
      ))}

      {/* Dimension labels */}
      {ALL_PSYCHOLOGY.map((dim, i) => {
        const x = cx + Math.cos(RADAR_ANGLES[i]) * labelR;
        const y = cy + Math.sin(RADAR_ANGLES[i]) * labelR;
        return (
          <text key={dim.key} x={x} y={y}
            textAnchor="middle" dominantBaseline="middle"
            fill={dim.color} fontSize={10} fontWeight="600"
            fontFamily="Inter" style={{ pointerEvents: "none" }}
          >
            {dim.name}
          </text>
        );
      })}

      {/* Percentage labels on total dots */}
      {overall.map((v, i) => {
        const pct = Math.round(Math.max(0, Math.min(1, v)) * 100);
        const pctR = maxR * Math.max(0, Math.min(1, v)) - 12;
        if (pctR < 10) return null;
        const x = cx + Math.cos(RADAR_ANGLES[i]) * pctR;
        const y = cy + Math.sin(RADAR_ANGLES[i]) * pctR;
        return (
          <text key={`pct${i}`} x={x} y={y}
            textAnchor="middle" dominantBaseline="middle"
            fill="rgba(239,68,68,0.5)" fontSize={7}
            fontFamily="monospace" style={{ pointerEvents: "none" }}
          >
            {pct}
          </text>
        );
      })}
    </svg>
  );
}
