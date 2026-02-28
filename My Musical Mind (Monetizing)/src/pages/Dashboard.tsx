import { useMemo, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { motion } from "framer-motion";
import {
  Flame, ChevronRight, Sparkles, Brain,
  TrendingUp, Send,
} from "lucide-react";
import { useUserStore } from "@/stores/useUserStore";
import { getPersona } from "@/data/personas";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import {
  generateWeeklyMonologue,
  generateBrainQuote,
} from "@/data/mind-insights";
import { beliefColors } from "@/design/tokens";
import { pageTransition, fadeIn, cinematicReveal } from "@/design/animations";
import { weeklyStats } from "@/data/mock-listening";
import { useM3Store } from "@/stores/useM3Store";
import { levelToOrganismStage, GENE_NAMES, GENE_COLORS, getDominantGene } from "@/types/m3";
import { useActiveIdentity } from "@/hooks/useActiveIdentity";
import { useChatStore } from "@/stores/useChatStore";
import { MiniOrganism } from "@/components/mind/MiniOrganism";
import { ChatMessage, TypingIndicator } from "@/components/chat/ChatMessage";

export function Dashboard() {
  const navigate = useNavigate();
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
  const error = useChatStore((s) => s.error);
  const sendMessage = useChatStore((s) => s.sendMessage);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages.length, isLoading]);

  if (!mind || !persona) return null;

  const color = identity.color;
  const xpForNext = level * 200;
  const xpProgress = Math.min(100, (xp % xpForNext) / xpForNext * 100);
  const genes = m3Mind?.genes ?? { entropy: 0.5, resolution: 0.5, tension: 0.5, resonance: 0.5, plasticity: 0.5 };
  const dominantGene = getDominantGene(genes);
  const avgGeneStrength = useMemo(() => GENE_NAMES.reduce((s, g) => s + genes[g], 0) / 5, [genes]);

  const monologue = useMemo(() => generateWeeklyMonologue(persona, mind.axes, t), [persona, mind.axes, t]);
  const brainQuote = useMemo(() => generateBrainQuote(identity.family, persona.id, t), [identity.family, persona.id, t]);

  const morphology = identity.morphology;
  const organismStage = m3Mind ? levelToOrganismStage(m3Mind.level) : mind.stage;
  const personaLevel = m3Mind?.level ?? 1;

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
            background: `radial-gradient(ellipse 40% 35% at 80% 70%, ${beliefColors.reward.primary}04 0%, transparent 50%)`,
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

      {/* ═══ MAIN LAYOUT ══════════════════════════════════════════ */}
      <div className="relative z-10 h-full flex flex-col px-5 sm:px-8 md:px-10 pt-10 pb-24">

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
        <div className="flex-1 grid grid-cols-12 gap-4 min-h-0 overflow-hidden mt-1">

          {/* ═ LEFT COLUMN (3 cols): Sunburst + Weekly Evolution (6D) ═ */}
          <div className="col-span-3 flex flex-col gap-3 min-h-0">

            {/* Dimension Sunburst */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 1, delay: 0.2 }}
              className="spatial-card p-3 flex flex-col items-center flex-shrink-0"
            >
              <div className="w-full flex items-center justify-center">
                <DimensionSunburst color={color} size={340} />
              </div>
            </motion.div>

            {/* Weekly Evolution — 6D Psychological Dimensions */}
            <div className="spatial-card p-3 flex-1 min-h-0 overflow-hidden">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-display font-light tracking-[0.15em] uppercase text-slate-500">{t("dashboard.weeklyEvolution")}</span>
                <div className="flex items-center gap-1.5">
                  <TrendingUp size={13} style={{ color }} />
                  <span className="text-sm font-mono font-medium" style={{ color }}>+{evolution.pct}%</span>
                </div>
              </div>
              <div className="space-y-2">
                {ALL_PSYCHOLOGY.map((dim, i) => {
                  const key = dim.key as DimensionKey6D;
                  const delta = dimDeltas[key] ?? 0;
                  const isPositive = delta >= 0;
                  const dimColor = PSYCHOLOGY_COLORS[key];
                  const absDelta = Math.abs(delta);
                  return (
                    <div key={key} className="flex items-center gap-3">
                      <div className="flex items-center gap-1.5 w-20">
                        <div className="w-2 h-2 rounded-full" style={{ background: dimColor }} />
                        <span className="text-[11px] font-display text-slate-400">
                          {isTr ? dim.nameTr : dim.name}
                        </span>
                      </div>
                      <div className="flex-1 h-[4px] rounded-full bg-white/5 overflow-hidden">
                        <motion.div
                          className="h-full rounded-full"
                          style={{ backgroundColor: dimColor, opacity: 0.8 }}
                          initial={{ width: 0 }}
                          animate={{ width: `${Math.min(absDelta * 400, 100)}%` }}
                          transition={{ duration: 1, delay: 0.5 + i * 0.1 }}
                        />
                      </div>
                      <span className="text-[12px] font-mono w-12 text-right" style={{ color: isPositive ? dimColor : "#EF4444" }}>
                        {isPositive ? "+" : ""}{(delta * 100).toFixed(0)}%
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* ═ CENTER COLUMN (5 cols): Embedded Chat with Organism ═ */}
          <motion.div
            initial={{ opacity: 0, y: 20, filter: "blur(12px)" }}
            animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
            transition={{ duration: 0.8, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
            className="col-span-5 flex flex-col min-h-0 rounded-2xl overflow-hidden relative"
          >
            {/* Living organism background — persona-specific */}
            <div
              className="absolute inset-0 z-0"
              style={{ transform: "scale(1.3)", transformOrigin: "center 40%" }}
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
              className="absolute inset-0 z-[1] rounded-2xl"
              style={{
                background: "rgba(0, 0, 0, 0.55)",
                backdropFilter: "blur(20px)",
                WebkitBackdropFilter: "blur(20px)",
                border: `1px solid ${color}12`,
                boxShadow: `0 0 60px ${color}06, 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.04)`,
              }}
            />

            {/* Content layer above glass */}
            <div className="relative z-[2] flex flex-col min-h-0 h-full">
            {/* Chat Header — persona identity */}
            <div
              className="flex items-center gap-3 px-4 py-3 border-b border-white/[0.06]"
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
              className="flex-1 overflow-y-auto px-4 py-4 space-y-3 scroll-smooth"
              style={{ scrollbarWidth: "none" }}
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
                    className="text-center max-w-[280px]"
                  >
                    <p className="text-sm text-slate-400 font-body leading-relaxed">
                      I am your musical mind. Talk to me about your music experiences, emotions, and discoveries.
                    </p>
                  </motion.div>

                  {/* Brain quote as conversation starter */}
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.6, duration: 1 }}
                    className="max-w-[300px] mt-2"
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

              {messages.map((msg) => (
                <ChatMessage
                  key={msg.id}
                  role={msg.role}
                  content={msg.content}
                  accentColor={color}
                />
              ))}

              {isLoading && <TypingIndicator accentColor={color} />}

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

          {/* ═ RIGHT COLUMN (4 cols): Peak Moment + Brain Narrative + Genres ═ */}
          <div className="col-span-4 flex flex-col gap-2 min-h-0">

            {/* Peak Moment This Week — TOP */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.8 }}
              className="flex-shrink-0"
            >
              <div className="spatial-card p-4 glow-border" style={{ "--glow-color": beliefColors.reward.primary } as React.CSSProperties}>
                <div className="flex items-start gap-3">
                  <Sparkles size={16} className="mt-0.5 shrink-0" style={{ color: beliefColors.reward.primary }} />
                  <div className="flex-1 min-w-0">
                    <span className="text-[11px] font-display font-light tracking-[0.1em] uppercase" style={{ color: `${beliefColors.reward.primary}90` }}>
                      {t("dashboard.peakMomentThisWeek")}
                    </span>
                    <p className="text-[12px] text-slate-400 font-body font-light mt-1 leading-relaxed">
                      {weeklyStats.peakPE.description.slice(0, 140)}
                    </p>
                    <div className="flex items-center gap-2 mt-2">
                      <div className="h-1 flex-1 rounded-full bg-white/5 overflow-hidden">
                        <motion.div className="h-full rounded-full" style={{ background: beliefColors.reward.primary }}
                          initial={{ width: 0 }} animate={{ width: `${weeklyStats.peakPE.magnitude * 100}%` }}
                          transition={{ duration: 1.2, delay: 1 }}
                        />
                      </div>
                      <span className="text-[11px] font-mono" style={{ color: beliefColors.reward.primary }}>
                        {(weeklyStats.peakPE.magnitude * 100).toFixed(0)}% {t("dashboard.intensity")}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Your Brain This Week — Narrative (data-driven) */}
            <div className="spatial-card p-4 flex-shrink-0">
              <div className="flex items-center gap-2 mb-2.5">
                <Brain size={14} style={{ color: beliefColors.reward.primary }} />
                <span className="text-xs font-display font-light tracking-[0.15em] uppercase text-slate-500">{t("dashboard.yourBrainThisWeek")}</span>
              </div>
              {(() => {
                const genes = aggregateProfile?.genes;
                const depthDelta = dimDeltas.depth ?? 0;
                // Find strongest dimension shift
                const dimEntries = Object.entries(dimDeltas).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]));
                const strongestDim = dimEntries[0];
                const strongestPct = strongestDim ? (Math.abs(strongestDim[1]) * 100).toFixed(0) : "0";
                const strongestName = strongestDim?.[0] ?? "depth";
                const strongestColor = PSYCHOLOGY_COLORS[strongestName as DimensionKey6D] ?? color;
                return (
                  <>
                    <p className="text-[12px] text-slate-300 leading-relaxed font-body font-light">
                      {isTr ? "En güçlü boyut kaymanız" : "Your strongest dimension shift"}: <span className="font-mono font-medium" style={{ color: strongestColor }}>{strongestDim?.[1] && strongestDim[1] >= 0 ? "+" : ""}{strongestPct}% {strongestName}</span>.
                      {" "}{depthDelta > 0.1
                        ? (isTr ? "Müzikal hazzınız güçleniyor — zihniniz 'iyi müzik'in ne olduğunu yeniden kalibre ediyor." : "Your sense of musical pleasure is strengthening — your mind is recalibrating what 'good music' means.")
                        : depthDelta < -0.05
                          ? (isTr ? "Duygusal derinliğiniz sakinleşiyor — dinleme tercihleriniz rafine ediliyor." : "Your emotional depth is settling — your listening preferences are becoming more refined.")
                          : (isTr ? "Müzikal kimliğiniz dengeli bir evrimde." : "Your musical identity is in a balanced evolution.")}
                    </p>
                    <p className="text-[12px] text-slate-400 leading-relaxed font-body font-light mt-2">
                      {genes ? (
                        genes.resolution > 0.55
                          ? (isTr
                            ? <>Çözünürlük ihtiyacınız (<span className="font-mono" style={{ color: PSYCHOLOGY_COLORS.discovery }}>{(genes.resolution * 100).toFixed(0)}%</span>) haftanıza damgasını vurdu. Her çözülen akor, her tatmin edici son — zihniniz her birini küçük bir zafer olarak kaydetti.</>
                            : <>Your resolution drive (<span className="font-mono" style={{ color: PSYCHOLOGY_COLORS.discovery }}>{(genes.resolution * 100).toFixed(0)}%</span>) shaped your week. Every resolved chord, every satisfying ending — your mind marked each one as a small victory.</>)
                          : genes.entropy > 0.45
                            ? (isTr
                              ? <>Entropi toleransınız (<span className="font-mono" style={{ color: PSYCHOLOGY_COLORS.discovery }}>{(genes.entropy * 100).toFixed(0)}%</span>) sizi yeniliğe yöneltiyor. Keşfetme dürtünüz güçlü.</>
                              : <>Your entropy tolerance (<span className="font-mono" style={{ color: PSYCHOLOGY_COLORS.discovery }}>{(genes.entropy * 100).toFixed(0)}%</span>) drives you toward novelty. Your exploration instinct is strong.</>)
                            : (isTr
                              ? <>Rezonans derinliğiniz (<span className="font-mono" style={{ color: PSYCHOLOGY_COLORS.depth }}>{(genes.resonance * 100).toFixed(0)}%</span>) müzikal hafızanızı şekillendiriyor.</>
                              : <>Your resonance depth (<span className="font-mono" style={{ color: PSYCHOLOGY_COLORS.depth }}>{(genes.resonance * 100).toFixed(0)}%</span>) shapes your musical memory.</>)
                      ) : null}
                    </p>
                  </>
                );
              })()}
            </div>

            {/* Top Genres */}
            <div className="spatial-card p-3 flex-shrink-0">
              <div className="flex items-center flex-wrap gap-2">
                {weeklyStats.topGenres.slice(0, 4).map((g) => (
                  <div key={g.name} className="flex items-center gap-1.5 px-2.5 py-1 rounded-full" style={{ background: `${color}08`, border: `1px solid ${color}12` }}>
                    <span className="text-[11px] font-display text-slate-400">{g.name}</span>
                    <span className="text-[10px] font-mono" style={{ color }}>{g.pct}%</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Brain Monologue */}
            <div className="spatial-card p-3 flex-1 min-h-0 overflow-hidden">
              <p className="text-[11px] text-slate-500 font-display font-light leading-relaxed line-clamp-4">
                {monologue}
              </p>
            </div>
          </div>

        </div>
      </div>

    </motion.div>
  );
}

/* ── Helper Components ────────────────────────────────────────── */

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
