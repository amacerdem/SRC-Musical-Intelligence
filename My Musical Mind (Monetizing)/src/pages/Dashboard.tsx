import { useMemo, useRef, useEffect, useState, useCallback } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { motion, AnimatePresence } from "framer-motion";
import {
  Flame, ChevronRight, Sparkles,
  TrendingUp, Send, FlaskConical, Activity,
  Clock, Music2, Play, Pause,
} from "lucide-react";
import { useUserStore } from "@/stores/useUserStore";
import { getPersona } from "@/data/personas";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { generateBrainQuote } from "@/data/mind-insights";
import { beliefColors } from "@/design/tokens";
import { pageTransition, fadeIn, cinematicReveal } from "@/design/animations";
import { weeklyStats } from "@/data/mock-listening";
import { useM3Store } from "@/stores/useM3Store";
import { levelToOrganismStage } from "@/types/m3";
import { useActiveIdentity } from "@/hooks/useActiveIdentity";
import { ALL_PSYCHOLOGY, ALL_COGNITION, ALL_NEUROSCIENCE, PSYCHOLOGY_COLORS, genesToDimensions, arrayToProfile, profileToArray } from "@/data/dimensions";
import { DIMENSION_KEYS_6D } from "@/types/dimensions";
import type { DimensionKey6D } from "@/types/dimensions";
import { DashboardRadar } from "@/components/mind/DashboardRadar";
import { SpotifyMiniPlayer } from "@/components/dashboard/SpotifyMiniPlayer";
import { useNowPlaying } from "@/hooks/useNowPlaying";
import { useDemoFlow } from "@/hooks/useDemoFlow";
import { useChatStore } from "@/stores/useChatStore";
import { MiniOrganism } from "@/components/mind/MiniOrganism";
import { PersonaAvatar } from "@/components/mind/PersonaAvatar";
import { ChatMessage, TypingIndicator } from "@/components/chat/ChatMessage";

/* Lab imports */
import { useLabStore } from "@/stores/useLabStore";
import { AudioInput } from "@/components/lab/AudioInput";
import { DepthSelector } from "@/components/lab/DepthSelector";
import { FlowTimeline } from "@/components/lab/FlowTimeline";

/* Listen imports */
import { ListenPanel } from "@/components/listen/ListenPanel";

const DIM_KEYS: DimensionKey6D[] = [...DIMENSION_KEYS_6D];

/** Concept-appropriate point labels for Weekly Evolution */
const POINT_LABELS: Record<string, { en: string; tr: string }> = {
  discovery: { en: "Spark",    tr: "Kıvılcım" },
  intensity: { en: "Surge",    tr: "Dalga" },
  flow:      { en: "Pulse",    tr: "Nabız" },
  depth:     { en: "Bloom",    tr: "Çiçek" },
  trace:     { en: "Echo",     tr: "Yankı" },
  sharing:   { en: "Sync",     tr: "Senkron" },
};

/* ── Audio-file mapping (shared with Lab) ──────── */
const TRACK_AUDIO: Record<string, string> = {
  "tchaikovsky__swan_lake_suite_op20a_scene": "/music/swan-lake.wav",
  "pyotr_ilyich_tchaikovsky_berliner_philharmoniker_mstislav_rostropovich__swan_lake_suite_op_20a_i_scene_swan_theme_modera": "/music/swan-lake.wav",
};

export function Dashboard() {
  const navigate = useNavigate();
  const location = useLocation();
  const labMode = location.pathname === "/lab";
  const listenMode = location.pathname === "/listen";
  const { t, i18n } = useTranslation();
  const isTr = i18n.language === "tr";
  const { mind, level, xp, streak, displayName } = useUserStore();
  const m3Mind = useM3Store((s) => s.mind);
  const identity = useActiveIdentity();
  const activePersonaId = m3Mind?.activePersonaId ?? mind?.personaId;
  const persona = activePersonaId ? getPersona(activePersonaId) : null;

  // Chat state
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

  if (!mind || !persona) return null;

  const color = identity.color;
  const xpForNext = level * 200;
  const xpProgress = Math.min(100, (xp % xpForNext) / xpForNext * 100);
  const genes = m3Mind?.genes ?? { entropy: 0.5, resolution: 0.5, tension: 0.5, resonance: 0.5, plasticity: 0.5 };
  const dim6D = useMemo(() => {
    const d = genesToDimensions(genes);
    return Object.fromEntries(DIM_KEYS.map((k, i) => [k, d.psychology[i]])) as Record<DimensionKey6D, number>;
  }, [genes]);
  const avgDimStrength = useMemo(() => DIM_KEYS.reduce((s, k) => s + dim6D[k], 0) / 6, [dim6D]);
  const dim6DProfile = useMemo(() => arrayToProfile(genesToDimensions(genes).psychology), [genes]);
  const total6D = useMemo(() => profileToArray(dim6DProfile), [dim6DProfile]);

  // Now playing & demo flow
  const { track: nowPlayingTrack, isPlaying, isDemo } = useNowPlaying();
  const flow6D = useDemoFlow(total6D, isPlaying);

  const brainQuote = useMemo(() => generateBrainQuote(identity.family, persona.id, t), [identity.family, persona.id, t]);

  const morphology = identity.morphology;
  const organismStage = m3Mind ? levelToOrganismStage(m3Mind.level) : mind.stage;
  const personaLevel = m3Mind?.level ?? 1;

  /* ── Lab state ─────────────────────────────────── */
  const trackDetail = useLabStore((s) => s.trackDetail);
  const labDepth = useLabStore((s) => s.depth);
  const setLabDepth = useLabStore((s) => s.setDepth);
  const temporal = useLabStore((s) => s.temporal);
  const labPhase = useLabStore((s) => s.phase);
  const labProgress = useLabStore((s) => s.progress);

  const hasLabAnalysis = labPhase === "done" && !!trackDetail && !!temporal;

  /* Lab audio playback */
  const labAudioRef = useRef<HTMLAudioElement | null>(null);
  const [labPlaying, setLabPlaying] = useState(false);
  const [labEverPlayed, setLabEverPlayed] = useState(false);
  const [labFlowIdx, setLabFlowIdx] = useState(0);

  const labSegments6D = useMemo(
    () => temporal?.segments.map((s) => s.psychology) ?? [],
    [temporal],
  );
  const labOverall6D = useMemo(
    () => temporal?.overall.psychology ?? [],
    [temporal],
  );
  const labSegCountRef = useRef(labSegments6D.length);
  labSegCountRef.current = labSegments6D.length;

  useEffect(() => {
    if (!labMode) return;
    if (labAudioRef.current) {
      labAudioRef.current.pause();
      labAudioRef.current.src = "";
      labAudioRef.current = null;
    }
    setLabPlaying(false);
    setLabEverPlayed(false);
    setLabFlowIdx(0);
    if (!trackDetail) return;
    const url = TRACK_AUDIO[trackDetail.id];
    if (!url) return;
    const audio = new Audio(url);
    audio.preload = "auto";
    labAudioRef.current = audio;
    const onTime = () => {
      if (!audio.duration || labSegCountRef.current <= 1) return;
      const r = audio.currentTime / audio.duration;
      const idx = Math.round(r * (labSegCountRef.current - 1));
      setLabFlowIdx(Math.max(0, Math.min(labSegCountRef.current - 1, idx)));
    };
    const onEnd = () => { setLabPlaying(false); setLabFlowIdx(0); };
    audio.addEventListener("timeupdate", onTime);
    audio.addEventListener("ended", onEnd);
    return () => {
      audio.removeEventListener("timeupdate", onTime);
      audio.removeEventListener("ended", onEnd);
      audio.pause();
      audio.src = "";
      labAudioRef.current = null;
    };
  }, [labMode, trackDetail]);

  const toggleLabPlay = useCallback(() => {
    const audio = labAudioRef.current;
    if (!audio) return;
    if (labPlaying) { audio.pause(); setLabPlaying(false); }
    else { setLabEverPlayed(true); audio.play().catch(() => {}); setLabPlaying(true); }
  }, [labPlaying]);

  const labFlowValues = labSegments6D[labFlowIdx] ?? labOverall6D;
  const labShowFlow = labEverPlayed;

  const labFlowTime = useMemo(() => {
    if (!trackDetail || labSegments6D.length <= 1) return "";
    const secs = (labFlowIdx / Math.max(1, labSegments6D.length - 1)) * trackDetail.duration_s;
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  }, [labFlowIdx, labSegments6D.length, trackDetail]);

  const labTotalTime = useMemo(() => {
    if (!trackDetail) return "";
    const m = Math.floor(trackDetail.duration_s / 60);
    const s = Math.floor(trackDetail.duration_s % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  }, [trackDetail]);

  const handleLabSeek = useCallback((ratio: number) => {
    const audio = labAudioRef.current;
    if (!audio || !audio.duration) return;
    audio.currentTime = ratio * audio.duration;
    const idx = Math.round(ratio * (labSegments6D.length - 1));
    setLabFlowIdx(Math.max(0, Math.min(labSegments6D.length - 1, idx)));
    if (!labEverPlayed) setLabEverPlayed(true);
  }, [labSegments6D.length, labEverPlayed]);

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
    el.style.height = Math.min(el.scrollHeight, 100) + "px";
  };

  // JS failsafe: explicitly scroll messages on wheel events
  const handleWheel = (e: React.WheelEvent<HTMLDivElement>) => {
    const el = scrollRef.current;
    if (!el) return;
    e.stopPropagation();
    el.scrollTop += e.deltaY;
  };

  return (
    <motion.div {...pageTransition} className="relative h-screen overflow-hidden">
      {/* Subtle persona-colored ambient background — no WebGL */}
      <div className="absolute inset-0 z-0">
        <div
          className="absolute inset-0"
          style={{
            background: `radial-gradient(ellipse 80% 60% at 50% 30%, ${color}08 0%, transparent 60%)`,
          }}
        />
        <div
          className="absolute inset-0"
          style={{
            background: `radial-gradient(ellipse 50% 40% at 20% 80%, ${color}05 0%, transparent 50%)`,
          }}
        />
        <div
          className="absolute inset-0"
          style={{
            background: `radial-gradient(ellipse 40% 35% at 80% 70%, ${PSYCHOLOGY_COLORS.trace}04 0%, transparent 50%)`,
          }}
        />
      </div>
      <div className="cinematic-vignette z-[2]" />

      {/* ── TOP-LEFT: HUD Stats ──────────────────────────────────── */}
      <motion.div
        variants={fadeIn}
        initial="initial"
        animate="animate"
        className="fixed top-10 left-6 z-30 flex items-center gap-5"
      >
        <HUDStat label={t("dashboard.streak")} value={`${streak}d`} icon={<Flame size={14} />} accent={color} />
        <HUDStat label={t("dashboard.level")} value={`L${personaLevel}/12`} icon={<TrendingUp size={13} />} />
        <div className="flex items-center gap-2.5">
          <div className="w-24 h-1.5 rounded-full overflow-hidden" style={{ background: `${color}15` }}>
            <motion.div className="h-full rounded-full" style={{ background: color, opacity: 0.7 }}
              initial={{ width: 0 }} animate={{ width: `${xpProgress}%` }}
              transition={{ duration: 1.2, ease: [0.22, 1, 0.36, 1] }}
            />
          </div>
          <span className="text-xs font-mono text-slate-500">{xp.toLocaleString()} XP</span>
        </div>
      </motion.div>

      {/* ── TOP-RIGHT: Spotify Mini-Player ──────────────────────── */}
      <AnimatePresence>
        {nowPlayingTrack && (
          <motion.div
            key="mini-player"
            initial={{ opacity: 0, x: 30, filter: "blur(8px)" }}
            animate={{ opacity: 1, x: 0, filter: "blur(0px)" }}
            exit={{ opacity: 0, x: 30, filter: "blur(8px)" }}
            transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
            className="fixed top-20 right-12 z-30"
          >
            <SpotifyMiniPlayer track={nowPlayingTrack} isDemo={isDemo} accentColor={color} />
          </motion.div>
        )}
      </AnimatePresence>

      {/* ═══ MAIN LAYOUT ══════════════════════════════════════════ */}
      <div className="relative z-10 h-full flex flex-col px-5 sm:px-8 md:px-10 -mt-8 pb-24">

        {/* ── TOP: Persona Identity — prominent, personal ──────── */}
        <motion.div {...cinematicReveal} className="text-center pt-1 pb-2">
          {displayName && displayName !== "You" && (
            <motion.p
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 0.5, y: 0 }}
              transition={{ delay: 0.1, duration: 0.8 }}
              className="text-sm text-slate-500 font-display font-light mb-1"
            >
              {t("dashboard.welcomeBack")} <span className="text-slate-300 font-medium">{displayName}</span>
            </motion.p>
          )}
          <motion.div
            initial={{ opacity: 0, scale: 0.92 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1.2, ease: [0.22, 1, 0.36, 1], delay: 0.15 }}
            className="flex items-center justify-center gap-3"
          >
            {/* Persona Character Avatar — left of name */}
            <motion.div
              initial={{ opacity: 0, scale: 0.85 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 1.2, delay: 0.05, ease: [0.22, 1, 0.36, 1] }}
              className="relative flex-shrink-0"
            >
              <PersonaAvatar
                personaId={persona.id}
                color={color}
                family={identity.family}
                size={52}
                level={personaLevel}
                showAura
              />
            </motion.div>
            <h1
              className="text-3xl md:text-4xl lg:text-5xl font-display font-bold tracking-tight leading-none"
              style={{ color }}
            >
              {t(`personas.${persona.id}.name`)}
            </h1>
            <motion.button
              onClick={() => navigate(`/info/${persona.id}`)}
              className="group p-1.5 rounded-full transition-all duration-500 hover:scale-110"
              style={{ background: `${color}10`, border: `1px solid ${color}15` }}
              whileHover={{ boxShadow: `0 0 20px ${color}20` }}
            >
              <ChevronRight size={16} style={{ color }} className="group-hover:translate-x-0.5 transition-transform" />
            </motion.button>
          </motion.div>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.45 }}
            transition={{ delay: 0.4, duration: 1 }}
            className="text-sm text-slate-500 font-display font-light italic mt-1"
          >
            "{t(`personas.${persona.id}.tagline`)}"
          </motion.p>
        </motion.div>

        {/* ── MAIN GRID ───────────────────────────────────────── */}
        <div className="flex-1 grid grid-cols-2 gap-4 min-h-0 overflow-hidden mt-1">

          {/* ═ LEFT — Chat with Organism ═ */}
          <motion.div
            initial={{ opacity: 0, y: 20, filter: "blur(12px)" }}
            animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
            transition={{ duration: 0.8, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
            className="flex flex-col min-h-0 rounded-2xl overflow-hidden relative"
          >
            {/* Living organism background — persona-specific */}
            <div
              className="absolute inset-0 z-0 pointer-events-none"
              style={{ transform: "scale(1.6, 1.3)", transformOrigin: "center 40%" }}
            >
              <MindOrganismCanvas
                color={color}
                secondaryColor={`${color}80`}
                stage={organismStage}
                intensity={0.65}
                breathRate={4}
                familyMorphology={morphology}
                className="w-full h-full"
                variant="hero"
                constellations
                interactive
              />
            </div>

            {/* Glassmorphism overlay */}
            <div
              className="absolute inset-0 z-[1] rounded-2xl pointer-events-none"
              style={{
                background: "rgba(0, 0, 0, 0.55)",
                backdropFilter: "blur(20px)",
                WebkitBackdropFilter: "blur(20px)",
                border: `1px solid ${color}12`,
                boxShadow: `0 0 60px ${color}06, 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.04)`,
              }}
            />

            {/* Content layer */}
            <div className="absolute inset-0 z-[2] flex flex-col overflow-hidden">
            {/* Chat Header — persona identity */}
            <div
              className="flex-shrink-0 flex items-center gap-3 px-4 py-3 border-b border-white/[0.06]"
              style={{ background: `${color}06` }}
            >
              <motion.div
                animate={{ scale: [1, 1.05, 1] }}
                transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
              >
                <MiniOrganism color={color} size={32} animated />
              </motion.div>
              <div className="flex-1">
                <div className="text-sm font-display font-medium text-white/90">
                  {t(`personas.${persona.id}.name`)}
                </div>
                <div className="text-[10px] font-mono" style={{ color: `${color}70` }}>
                  {t("chat.title")}
                </div>
              </div>
              <div
                className="px-2.5 py-1 rounded-full text-[8px] font-display font-medium tracking-wider uppercase"
                style={{
                  background: `${color}10`,
                  color: `${color}90`,
                  border: `1px solid ${color}15`,
                }}
              >
                {identity.family}
              </div>
            </div>

            {/* Chat Messages */}
            <div
              ref={scrollRef}
              onWheel={handleWheel}
              className="flex-1 min-h-0 overflow-y-scroll px-4 py-4 space-y-3"
              style={{ scrollbarWidth: "thin", scrollbarColor: `${color}30 transparent`, overscrollBehavior: "contain" }}
            >
              {messages.length === 0 && !isLoading && (
                <div className="flex flex-col items-center justify-center h-full gap-4 py-8">
                  <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
                  >
                    <MiniOrganism color={color} size={56} animated />
                  </motion.div>
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3, duration: 0.8 }}
                    className="text-center max-w-[320px]"
                  >
                    <p className="text-sm text-slate-400 font-body leading-relaxed">
                      {t("chat.welcome")}
                    </p>
                  </motion.div>

                  {/* Brain quote as conversation starter */}
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.6, duration: 1 }}
                    className="max-w-[340px] mt-2"
                  >
                    <div
                      className="rounded-2xl rounded-bl-md px-4 py-3 text-[13px] font-body leading-relaxed"
                      style={{
                        background: "rgba(255,255,255,0.04)",
                        border: "1px solid rgba(255,255,255,0.06)",
                        color: "#cbd5e1",
                      }}
                    >
                      <p className="italic">"{brainQuote}"</p>
                      <p className="text-[10px] font-mono mt-2" style={{ color: `${color}60` }}>
                        — {t("dashboard.yourMind", { family: identity.family.slice(0, -1) })}
                      </p>
                    </div>
                  </motion.div>
                </div>
              )}

              {messages.filter((msg) => msg.role !== "system").map((msg) => (
                <ChatMessage
                  key={msg.id}
                  role={msg.role as "user" | "assistant"}
                  content={msg.content}
                  accentColor={color}
                />
              ))}

              {streamingContent && (
                <ChatMessage role="assistant" content={streamingContent} accentColor={color} />
              )}
              {isLoading && !streamingContent && (
                <TypingIndicator accentColor={color} statusText={statusText} />
              )}

              {error && (
                <div className="text-center py-2">
                  <p className="text-xs text-red-400/70 font-body">{t("chat.error")}</p>
                </div>
              )}
            </div>

            {/* Chat Input */}
            <div className="flex-shrink-0 flex items-end gap-2 px-3 py-3 border-t border-white/[0.06]">
              <textarea
                ref={inputRef}
                onChange={handleInput}
                onKeyDown={handleKeyDown}
                placeholder={t("chat.placeholder")}
                disabled={isLoading}
                rows={1}
                className="flex-1 resize-none bg-white/[0.04] border border-white/[0.08] rounded-xl px-3.5 py-2.5 text-sm text-slate-200 placeholder:text-slate-600 outline-none focus:border-white/[0.15] transition-colors font-body"
                style={{ maxHeight: 100 }}
              />
              <button
                onClick={handleSend}
                disabled={isLoading}
                className="flex-shrink-0 w-9 h-9 rounded-xl flex items-center justify-center transition-all duration-200 disabled:opacity-30"
                style={{
                  background: `${color}20`,
                  border: `1px solid ${color}30`,
                }}
              >
                <Send size={16} style={{ color }} />
              </button>
            </div>
            </div>{/* /content layer */}
          </motion.div>

          {/* ═ RIGHT — Animated switch between Mind, Lab & Listen ═ */}
          <AnimatePresence mode="wait">
            {listenMode ? (
              /* ── LISTEN PANEL ──────────────────────────── */
              <motion.div
                key="listen"
                initial={{ opacity: 0, x: 30, filter: "blur(10px)" }}
                animate={{ opacity: 1, x: 0, filter: "blur(0px)" }}
                exit={{ opacity: 0, x: -30, filter: "blur(10px)" }}
                transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
                className="flex flex-col min-h-0 overflow-hidden spatial-card"
              >
                <ListenPanel accentColor={color} />
              </motion.div>
            ) : labMode ? (
              /* ── LAB PANEL ─────────────────────────────── */
              <motion.div
                key="lab"
                initial={{ opacity: 0, x: 30, filter: "blur(10px)" }}
                animate={{ opacity: 1, x: 0, filter: "blur(0px)" }}
                exit={{ opacity: 0, x: -30, filter: "blur(10px)" }}
                transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
                className="flex flex-col gap-0 min-h-0 overflow-hidden spatial-card"
              >
                {/* Lab Header */}
                <div className="flex-shrink-0 flex items-center justify-between px-4 py-2 border-b border-white/[0.06]">
                  <div className="flex items-center gap-2">
                    <FlaskConical size={15} style={{ color }} />
                    <span className="text-sm font-display font-bold" style={{ color }}>Lab</span>
                    <span className="text-[10px] font-display text-slate-600 font-light">Analysis Studio</span>
                  </div>
                  <DepthSelector depth={labDepth} onChange={setLabDepth} accentColor={color} />
                </div>

                {/* Track info (when analysis available) */}
                {hasLabAnalysis && (
                  <div className="flex-shrink-0 flex items-center gap-2.5 px-4 py-1.5 border-b border-white/[0.04]">
                    <Music2 size={12} className="text-slate-500" />
                    <span className="text-[11px] font-display text-slate-300 truncate">{trackDetail.title}</span>
                    <span className="text-[10px] text-slate-600 truncate">{trackDetail.artist}</span>
                    <div className="flex items-center gap-1 text-slate-600 ml-auto flex-shrink-0">
                      <Clock size={10} />
                      <span className="text-[10px] font-mono">{labTotalTime}</span>
                    </div>
                  </div>
                )}

                {/* Audio Source Selector — hidden once analysis is ready */}
                {!hasLabAnalysis && (
                  <div className="flex-shrink-0 px-3 py-2 border-b border-white/[0.04]">
                    <AudioInput accentColor={color} />
                  </div>
                )}

                {/* Flow Timeline area */}
                <div className="flex-1 min-h-0 flex flex-col">
                  {hasLabAnalysis ? (
                    <>
                      {/* Play controls + info */}
                      <div className="flex items-center gap-2 px-3 py-1.5 flex-shrink-0 border-b border-white/[0.04]">
                        <button
                          onClick={toggleLabPlay}
                          className="w-6 h-6 rounded-full flex items-center justify-center transition-all"
                          style={{
                            background: labPlaying ? `${color}20` : `${color}12`,
                            border: `1px solid ${labPlaying ? `${color}40` : `${color}25`}`,
                          }}
                        >
                          {labPlaying
                            ? <Pause size={11} style={{ color }} />
                            : <Play size={11} style={{ color }} className="ml-0.5" />
                          }
                        </button>
                        <Activity size={10} className="text-slate-600" />
                        <span className="text-[9px] font-display font-light tracking-[0.12em] uppercase text-slate-500">Temporal Flow</span>
                        <span className="text-[7px] font-mono text-slate-700">
                          {temporal.source === "full" ? `${temporal.frameCount} frames` : "64 seg"}
                        </span>
                        {labEverPlayed && labFlowTime && (
                          <span className="text-[9px] font-mono ml-auto" style={{ color: `${color}60` }}>
                            {labFlowTime} / {labTotalTime}
                          </span>
                        )}
                      </div>

                      {/* Dim labels + Flow canvas */}
                      <div className="flex-1 min-h-0 flex">
                        <LabDimLabels
                          values={
                            labDepth === 6 ? labFlowValues
                              : labDepth === 12 ? (temporal.segments[labFlowIdx]?.cognition ?? temporal.overall.cognition)
                              : (temporal.segments[labFlowIdx]?.neuroscience ?? temporal.overall.neuroscience)
                          }
                          dims={labDepth === 6 ? ALL_PSYCHOLOGY : labDepth === 12 ? ALL_COGNITION : ALL_NEUROSCIENCE}
                          animated={labShowFlow}
                        />
                        <div className="flex-1 min-h-0">
                          <FlowTimeline
                            temporal={temporal}
                            trackDetail={trackDetail}
                            depth={labDepth}
                            accentColor={color}
                            audioRef={labAudioRef}
                            isPlaying={labPlaying}
                            onSeek={handleLabSeek}
                            labMode="neuro"
                          />
                        </div>
                      </div>
                    </>
                  ) : (
                    <div className="flex-1 flex items-center justify-center">
                      {labPhase === "analyzing" ? (
                        <div className="flex flex-col items-center gap-3">
                          <motion.div animate={{ rotate: 360 }} transition={{ duration: 4, repeat: Infinity, ease: "linear" }}>
                            <FlaskConical size={28} style={{ color: `${color}50` }} />
                          </motion.div>
                          <div className="w-32">
                            <div className="h-1.5 rounded-full bg-white/5 overflow-hidden">
                              <motion.div className="h-full rounded-full"
                                style={{ background: color }}
                                animate={{ width: `${labProgress}%` }}
                                transition={{ duration: 0.5 }}
                              />
                            </div>
                          </div>
                          <span className="text-[10px] font-mono text-slate-500">{Math.round(labProgress)}%</span>
                        </div>
                      ) : (
                        <div className="flex flex-col items-center gap-3">
                          <FlaskConical size={32} className="text-slate-700" />
                          <p className="text-xs text-slate-600 font-body text-center max-w-[180px]">
                            Select a track above to begin analysis.
                          </p>
                        </div>
                      )}
                    </div>
                  )}
                </div>

              </motion.div>
            ) : (
              /* ── MIND PANEL (Radar + Stats) ────────────── */
              <motion.div
                key="mind"
                initial={{ opacity: 0, x: -30, filter: "blur(10px)" }}
                animate={{ opacity: 1, x: 0, filter: "blur(0px)" }}
                exit={{ opacity: 0, x: 30, filter: "blur(10px)" }}
                transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
                className="flex flex-col gap-3 min-h-0 overflow-hidden"
              >
                <motion.div
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 1, delay: 0.2 }}
                  className="spatial-card flex flex-col flex-1 min-h-0 overflow-hidden"
                >
                  {/* Peak Moment — top strip */}
                  <div className="flex-shrink-0 px-4 py-2.5 border-b border-white/[0.06]">
                    <div className="flex items-start gap-2.5">
                      <Sparkles size={14} className="mt-0.5 shrink-0" style={{ color: beliefColors.reward.primary }} />
                      <div className="flex-1 min-w-0">
                        <span className="text-[10px] font-display font-light tracking-[0.1em] uppercase" style={{ color: `${beliefColors.reward.primary}90` }}>
                          {t("dashboard.peakMomentThisWeek")}
                        </span>
                        <p className="text-[11px] text-slate-400 font-body font-light mt-0.5 leading-relaxed">
                          {weeklyStats.peakPE.description.slice(0, 100)}
                        </p>
                        <div className="flex items-center gap-2 mt-1">
                          <div className="h-1 flex-1 rounded-full bg-white/5 overflow-hidden">
                            <motion.div className="h-full rounded-full" style={{ background: beliefColors.reward.primary }}
                              initial={{ width: 0 }} animate={{ width: `${weeklyStats.peakPE.magnitude * 100}%` }}
                              transition={{ duration: 1.2, delay: 1 }}
                            />
                          </div>
                          <span className="text-[10px] font-mono" style={{ color: beliefColors.reward.primary }}>
                            {(weeklyStats.peakPE.magnitude * 100).toFixed(0)}%
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Radar with orbital rings */}
                  <div className="flex-1 flex items-center justify-center relative">
                    <div className="absolute inset-0 overflow-hidden">
                      {ALL_PSYCHOLOGY.map((dim, i) => {
                        const bColor = dim.color;
                        const radius = 185 + i * 25;
                        return (
                          <div key={dim.key} className="absolute inset-0 flex items-center justify-center pointer-events-none">
                            <div className="absolute rounded-full" style={{
                              width: radius * 2, height: radius * 2,
                              background: `conic-gradient(from ${i * 60}deg, ${bColor}30, ${bColor}18 8%, ${bColor}0A 20%, transparent 40%, transparent 100%)`,
                              maskImage: `radial-gradient(transparent ${radius - 2}px, black ${radius - 1}px, black ${radius + 1}px, transparent ${radius + 2}px)`,
                              WebkitMaskImage: `radial-gradient(transparent ${radius - 2}px, black ${radius - 1}px, black ${radius + 1}px, transparent ${radius + 2}px)`,
                              animation: `orbit ${26 + i * 5}s linear infinite`,
                            }} />
                            <div className="absolute rounded-full" style={{ width: radius * 2, height: radius * 2, border: `1px solid ${bColor}06` }} />
                            <motion.div className="absolute" style={{
                              width: 5, height: 5, borderRadius: "50%", background: bColor,
                              boxShadow: `0 0 10px ${bColor}80, 0 0 25px ${bColor}40`,
                              left: `calc(50% + ${radius}px - 2.5px)`, top: "calc(50% - 2.5px)",
                              transformOrigin: `${-radius + 2.5}px 2.5px`,
                              animation: `orbit ${26 + i * 5}s linear infinite`,
                            }} />
                          </div>
                        );
                      })}
                    </div>
                    <div className="relative z-10">
                      <DashboardRadar total={total6D} flow={flow6D} color={color} size={380} showFlow={isPlaying} />
                    </div>
                  </div>

                  {/* Radar legend */}
                  <div className="flex-shrink-0 flex items-center justify-center gap-5 py-1.5 border-t border-white/[0.04]">
                    <div className="flex items-center gap-1.5">
                      <div className="w-3 h-[2px] rounded-full bg-red-500" />
                      <span className="text-[9px] font-display text-slate-500">Total</span>
                    </div>
                    {isPlaying && (
                      <div className="flex items-center gap-1.5">
                        <div className="w-3 h-[2px] rounded-full" style={{ background: color }} />
                        <span className="text-[9px] font-display text-slate-500">Flow</span>
                      </div>
                    )}
                  </div>

                  {/* Weekly Evolution bars */}
                  <div className="flex-shrink-0 px-4 pb-3 pt-1 border-t border-white/[0.06]">
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-xs font-display font-light tracking-[0.15em] uppercase text-slate-500">{t("dashboard.weeklyEvolution")}</span>
                      <div className="flex items-center gap-1.5">
                        <TrendingUp size={13} style={{ color }} />
                        <span className="text-sm font-mono font-medium" style={{ color }}>+{DIM_KEYS.reduce((s, k) => s + Math.round(dim6D[k] * 100), 0)}</span>
                      </div>
                    </div>
                    <div className="space-y-1.5">
                      {ALL_PSYCHOLOGY.map((dim, i) => {
                        const key = dim.key as DimensionKey6D;
                        const value = dim6D[key];
                        const pts = Math.round(value * 100);
                        const dimColor = PSYCHOLOGY_COLORS[key];
                        const pointLabel = POINT_LABELS[key];
                        return (
                          <div key={key} className="flex items-center gap-2.5">
                            <div className="flex items-center gap-1.5 w-[72px]">
                              <div className="w-1.5 h-1.5 rounded-full" style={{ background: dimColor }} />
                              <span className="text-[10px] font-display text-slate-400">{isTr ? dim.nameTr : dim.name}</span>
                            </div>
                            <div className="flex-1 h-[3px] rounded-full bg-white/5 overflow-hidden">
                              <motion.div className="h-full rounded-full" style={{ background: dimColor, opacity: 0.7 }}
                                initial={{ width: 0 }} animate={{ width: `${pts}%` }}
                                transition={{ duration: 1.2, delay: 0.5 + i * 0.08 }}
                              />
                            </div>
                            <div className="flex items-center gap-1 w-[72px] justify-end">
                              <span className="text-[11px] font-mono font-medium" style={{ color: dimColor }}>+{pts}</span>
                              <span className="text-[9px] font-display text-slate-600">{isTr ? pointLabel.tr : pointLabel.en}</span>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                    <div className="flex items-center flex-wrap gap-1.5 mt-2 pt-2 border-t border-white/[0.04]">
                      {weeklyStats.topGenres.slice(0, 4).map((g) => (
                        <div key={g.name} className="flex items-center gap-1 px-2 py-0.5 rounded-full" style={{ background: `${color}08`, border: `1px solid ${color}12` }}>
                          <span className="text-[10px] font-display text-slate-400">{g.name}</span>
                          <span className="text-[9px] font-mono" style={{ color }}>{g.pct}%</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </motion.div>
              </motion.div>
            )}
          </AnimatePresence>

        </div>
      </div>

    </motion.div>
  );
}

/* ── Helper Components ────────────────────────────────────────── */

function LabDimLabels({ values, dims, animated }: {
  values: number[];
  dims: { key: string; name: string; color: string }[];
  animated: boolean;
}) {
  const fontSize = dims.length <= 6 ? 11 : dims.length <= 12 ? 9 : 7;
  const dotSize = dims.length <= 6 ? 7 : dims.length <= 12 ? 5 : 4;

  const sorted = useMemo(() => {
    const items = dims.map((dim, i) => ({ dim, value: values[i] ?? 0 }));
    items.sort((a, b) => b.value - a.value);
    return items;
  }, [dims, values]);

  return (
    <div
      className="flex flex-col justify-around py-2 flex-shrink-0 border-r border-white/[0.04]"
      style={{ width: dims.length <= 6 ? 90 : dims.length <= 12 ? 76 : 62 }}
    >
      {sorted.map(({ dim }) => (
        <div key={dim.key} className="flex items-center gap-1.5 px-2">
          <div
            className="flex-shrink-0 rounded-full"
            style={{
              width: dotSize, height: dotSize,
              background: dim.color,
              boxShadow: animated ? `0 0 5px ${dim.color}60` : "none",
            }}
          />
          <span
            className="font-display truncate leading-none font-medium"
            style={{ fontSize, color: dim.color, opacity: animated ? 0.9 : 0.7 }}
          >
            {dim.name}
          </span>
        </div>
      ))}
    </div>
  );
}

function HUDStat({ label, value, icon, accent }: { label: string; value: string; icon?: React.ReactNode; accent?: string }) {
  return (
    <div>
      <div className="text-[10px] font-display font-light tracking-[0.15em] uppercase text-slate-600 mb-0.5">{label}</div>
      <div className="flex items-center gap-1.5">
        {icon && <span style={{ color: accent ?? "#94A3B8" }}>{icon}</span>}
        <span className="text-base font-mono text-slate-300">{value}</span>
      </div>
    </div>
  );
}
