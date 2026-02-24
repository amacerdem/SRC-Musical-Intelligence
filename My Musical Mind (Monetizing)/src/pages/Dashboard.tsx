import { useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { motion, AnimatePresence } from "framer-motion";
import {
  Flame, ChevronRight, Sparkles, Brain, MessageCircle, X,
  TrendingUp, Activity, Clock, Music,
} from "lucide-react";
import { useUserStore } from "@/stores/useUserStore";
import { getPersona } from "@/data/personas";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { MindRadar } from "@/components/mind/MindRadar";
import { MiniOrganism } from "@/components/mind/MiniOrganism";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { Avatar } from "@/components/ui/Avatar";
import { BeliefMiniTrace } from "@/components/dashboard/BeliefMiniTrace";
import { Button } from "@/components/ui/Button";
import { mockUsers } from "@/data/mock-users";
import {
  generateWeeklyMonologue,
  generatePEInsight,
  findSimilarMind,
  generateBrainQuote,
} from "@/data/mind-insights";
import { beliefColors, getCompatibilityLabel } from "@/design/tokens";
import { pageTransition, fadeIn, cinematicReveal } from "@/design/animations";
import type { MindAxes } from "@/types/mind";
import { weeklyStats, lastWeekDays, monthlyEvolution } from "@/data/mock-listening";

/* ── Axis metadata ──────────────────────────────────────────── */
const AXIS_META: { key: keyof MindAxes; shortLabel: string; belief: keyof typeof beliefColors }[] = [
  { key: "entropyTolerance", shortLabel: "Entropy", belief: "consonance" },
  { key: "resolutionCraving", shortLabel: "Resolution", belief: "tempo" },
  { key: "monotonyTolerance", shortLabel: "Monotony", belief: "familiarity" },
  { key: "salienceSensitivity", shortLabel: "Salience", belief: "salience" },
  { key: "tensionAppetite", shortLabel: "Tension", belief: "reward" },
];

const BELIEF_NAMES = ["consonance", "tempo", "salience", "familiarity", "reward"] as const;
const BELIEF_LABELS: Record<string, string> = {
  consonance: "Harmony", tempo: "Rhythm", salience: "Attention", familiarity: "Memory", reward: "Pleasure",
};
const DAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

const BELIEF_I18N_KEY: Record<string, string> = {
  consonance: "dashboard.beliefs.harmony",
  tempo: "dashboard.beliefs.rhythm",
  salience: "dashboard.beliefs.attention",
  familiarity: "dashboard.beliefs.memory",
  reward: "dashboard.beliefs.pleasure",
};

const DAY_I18N_KEYS = [
  "dashboard.days.mon", "dashboard.days.tue", "dashboard.days.wed", "dashboard.days.thu",
  "dashboard.days.fri", "dashboard.days.sat", "dashboard.days.sun",
];

const AXIS_I18N_KEY: Record<string, string> = {
  entropyTolerance: "dashboard.axes.entropy",
  resolutionCraving: "dashboard.axes.resolution",
  monotonyTolerance: "dashboard.axes.monotony",
  salienceSensitivity: "dashboard.axes.salience",
  tensionAppetite: "dashboard.axes.tension",
};

/* ── Evolution % calculation ─────────────────────────────────── */
function computeEvolution(): { pct: string; direction: "up" | "down" } {
  const snaps = monthlyEvolution.weeklySnapshots;
  const prev = snaps[snaps.length - 2];
  const curr = snaps[snaps.length - 1];
  const totalDelta = curr.reduce((sum, v, i) => sum + Math.abs(v - prev[i]), 0);
  const avgPrev = prev.reduce((a, b) => a + b, 0) / prev.length;
  const pct = ((totalDelta / prev.length) / avgPrev) * 100;
  const net = curr.reduce((a, b) => a + b, 0) - prev.reduce((a, b) => a + b, 0);
  return { pct: pct.toFixed(1), direction: net >= 0 ? "up" : "down" };
}

export function Dashboard() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const { mind, level, xp, streak, tracksAnalyzed, displayName, totalListeningHours } = useUserStore();
  const persona = mind ? getPersona(mind.personaId) : null;
  const [chatOpen, setChatOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState<{ from: "you" | "them"; text: string }[]>([]);
  const [chatInput, setChatInput] = useState("");

  if (!mind || !persona) return null;

  const color = persona.color;
  const xpForNext = level * 200;
  const xpProgress = Math.min(100, (xp % xpForNext) / xpForNext * 100);
  const evolution = useMemo(() => computeEvolution(), []);

  const monologue = useMemo(() => generateWeeklyMonologue(persona, mind.axes, t), [persona, mind.axes, t]);
  const peInsight = useMemo(() => generatePEInsight(t), [t]);
  const similarMind = useMemo(() => findSimilarMind(mind.axes, persona, mockUsers, t), [mind.axes, persona, t]);
  const brainQuote = useMemo(() => generateBrainQuote(persona, mind.axes, t), [persona, mind.axes, t]);

  const handleSendChat = () => {
    const text = chatInput.trim();
    if (!text) return;
    setChatMessages((prev) => [...prev, { from: "you", text }]);
    setChatInput("");
    setTimeout(() => {
      const otherPersona = similarMind ? getPersona(similarMind.user.mind.personaId) : null;
      const replies = [
        `That resonates with how my ${otherPersona?.name || "mind"} processes harmony.`,
        `My H³ temporal morphology has been shifting lately — I'm hearing longer arcs.`,
        `Your mind is ${similarMind ? similarMind.similarity : 80}% aligned with mine, but that divergence makes it interesting.`,
      ];
      setChatMessages((prev) => [...prev, { from: "them", text: replies[prev.length % replies.length] }]);
    }, 1200);
  };

  return (
    <motion.div {...pageTransition} className="relative h-screen overflow-hidden">
      {/* Organism background — enlarged */}
      <div className="absolute inset-0 z-0" style={{ transform: "scale(1.4)", transformOrigin: "center center" }}>
        <MindOrganismCanvas
          color={color}
          secondaryColor={beliefColors.reward.primary}
          stage={mind.stage}
          intensity={0.7}
          breathRate={4}
          className="w-full h-full"
          variant="hero"
          interactive
        />
      </div>
      <div className="absolute inset-0 z-[1] pointer-events-none"
        style={{ background: `radial-gradient(ellipse 60% 60% at 50% 45%, transparent 15%, rgba(0,0,0,0.7) 55%, rgba(0,0,0,0.92) 100%)` }}
      />
      <div className="cinematic-vignette z-[2]" />

      {/* ── TOP-LEFT: HUD Stats ──────────────────────────────────── */}
      <motion.div
        variants={fadeIn}
        initial="initial"
        animate="animate"
        className="fixed top-10 left-6 z-30 flex items-center gap-5"
      >
        <HUDStat label={t("dashboard.streak")} value={`${streak}d`} icon={<Flame size={14} />} accent={color} />
        <HUDStat label={t("dashboard.tracks")} value={String(tracksAnalyzed)} icon={<Music size={13} />} />
        <HUDStat label={t("dashboard.level")} value={String(level)} icon={<TrendingUp size={13} />} />
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

        {/* ── TOP: Identity ───────────────────────────────────── */}
        <motion.div {...cinematicReveal} className="text-center py-0.5">
          <span className="text-xs font-display font-light tracking-[0.25em] uppercase" style={{ color: `${color}90` }}>
            {t(`stages.${mind.stage}`)}
          </span>
          {displayName && displayName !== "You" && (
            <span className="text-sm text-slate-500 font-display font-light ml-4">
              {t("dashboard.welcomeBack")} <span className="text-slate-300 font-medium">{displayName}</span>
            </span>
          )}
        </motion.div>

        {/* ── MAIN GRID ───────────────────────────────────────── */}
        <div className="flex-1 grid grid-cols-12 gap-4 min-h-0 overflow-hidden mt-1">

          {/* ═ LEFT COLUMN (3 cols): Radar + DNA + Signals ═════ */}
          <div className="col-span-3 flex flex-col gap-3 min-h-0">

            {/* Mind Radar */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 1, delay: 0.2 }}
              className="spatial-card p-3 flex flex-col items-center flex-1 min-h-0"
            >
              <div className="w-full h-full flex items-center justify-center">
                <MindRadar axes={mind.axes} color={color} size={280} />
              </div>
            </motion.div>

            {/* Radar legend — integrated with radar above */}
            <div className="px-3 py-2 flex-shrink-0 -mt-1">
              <div className="space-y-1.5">
                {AXIS_META.map((axis, i) => {
                  const value = mind.axes[axis.key];
                  const pct = Math.round(value * 100);
                  return (
                    <div key={axis.key} className="flex items-center gap-2">
                      <span className="text-[10px] font-display text-slate-500 w-20 truncate">{t(AXIS_I18N_KEY[axis.key])}</span>
                      <div className="flex-1 h-[2px] rounded-full bg-white/5 overflow-hidden">
                        <motion.div
                          className="h-full rounded-full"
                          style={{ backgroundColor: color, opacity: 0.5 }}
                          initial={{ width: 0 }}
                          animate={{ width: `${pct}%` }}
                          transition={{ duration: 1, ease: [0.22, 1, 0.36, 1], delay: 0.3 + i * 0.08 }}
                        />
                      </div>
                      <span className="text-[10px] font-mono w-7 text-right" style={{ color: `${color}90` }}>{pct}</span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Belief Signals */}
            <motion.div variants={fadeIn} initial="initial" animate="animate" className="spatial-card p-3 flex-shrink-0">
              <span className="text-xs font-display font-light tracking-[0.15em] uppercase text-slate-500 block mb-2">{t("dashboard.liveSignals")}</span>
              <BeliefMiniTrace height={55} />
              <div className="flex justify-center gap-3 mt-2">
                {BELIEF_NAMES.map((b) => (
                  <div key={b} className="flex items-center gap-1">
                    <div className="w-2 h-2 rounded-full" style={{ background: beliefColors[b].primary }} />
                    <span className="text-[10px] font-mono capitalize" style={{ color: `${beliefColors[b].primary}90` }}>
                      {t(BELIEF_I18N_KEY[b])}
                    </span>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>

          {/* ═ CENTER COLUMN (5 cols): Persona + Quote + PE ═══ */}
          <div className="col-span-5 flex flex-col items-center justify-center gap-4 min-h-0">

            {/* Persona identity */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 1.5, ease: [0.22, 1, 0.36, 1], delay: 0.3 }}
              className="text-center"
            >
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-display font-bold tracking-tight leading-none" style={{ color }}>
                {t(`personas.${persona.id}.name`)}
              </h1>
              <p className="text-sm text-slate-500 mt-2 font-display font-light italic">
                {t(`personas.${persona.id}.tagline`)}
              </p>
            </motion.div>

            {/* Brain evolution stat */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5, duration: 0.8 }}
              className="flex items-center gap-3 px-5 py-2.5 rounded-full"
              style={{ background: `${color}08`, border: `1px solid ${color}15` }}
            >
              <Activity size={16} style={{ color }} />
              <span className="text-sm font-display font-medium" style={{ color }}>
                {t("dashboard.evolution", { pct: evolution.pct })}
              </span>
              <span className="text-xs text-slate-500 font-display font-light">{t("dashboard.evolutionThisWeek")}</span>
            </motion.div>

            {/* Brain quote */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8, duration: 1 }}
              className="text-center max-w-lg px-4"
            >
              <p className="text-sm text-slate-400 font-display font-light italic leading-relaxed">
                "{brainQuote}"
              </p>
              <p className="text-xs font-mono text-slate-600 mt-2">— {t("dashboard.yourMind", { family: persona.family.slice(0, -1) })}</p>
            </motion.div>

            {/* PE Insight */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6, duration: 0.8 }}
              className="w-full max-w-lg"
            >
              <div className="spatial-card p-4 glow-border" style={{ "--glow-color": beliefColors.reward.primary } as React.CSSProperties}>
                <div className="flex items-start gap-3">
                  <Sparkles size={16} className="mt-0.5 shrink-0" style={{ color: beliefColors.reward.primary }} />
                  <div className="flex-1 min-w-0">
                    <span className="text-[11px] font-display font-light tracking-[0.1em] uppercase" style={{ color: `${beliefColors.reward.primary}90` }}>
                      {t("dashboard.peakMomentThisWeek")}
                    </span>
                    <p className="text-[13px] text-slate-400 font-body font-light mt-1 leading-relaxed">
                      {t("insights.mockPE").slice(0, 120)}...
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

            {/* Friends strip — bottom of center */}
            <motion.div variants={fadeIn} initial="initial" animate="animate" className="flex items-center gap-4">
              <div className="flex -space-x-2">
                {mockUsers.slice(0, 5).map((user) => {
                  const userPersona = getPersona(user.mind.personaId);
                  return (
                    <button
                      key={user.id}
                      onClick={() => navigate(`/friends/${user.id}`)}
                      className="relative group"
                    >
                      <Avatar src={user.avatarUrl || undefined} name={user.displayName} size={32} borderColor={userPersona.color} />
                    </button>
                  );
                })}
              </div>
              <button onClick={() => navigate("/friends")} className="flex items-center gap-1 text-xs text-slate-500 hover:text-slate-300 transition-colors font-display">
                {t("nav.friends")} <ChevronRight size={14} />
              </button>
              {similarMind && (
                <button
                  onClick={() => setChatOpen(true)}
                  className="flex items-center gap-2 px-3 py-1.5 rounded-full transition-colors"
                  style={{ background: `${beliefColors.familiarity.primary}10`, border: `1px solid ${beliefColors.familiarity.primary}20` }}
                >
                  <MessageCircle size={13} style={{ color: beliefColors.familiarity.primary }} />
                  <span className="text-[11px] font-display" style={{ color: beliefColors.familiarity.primary }}>
                    {t("dashboard.match", { pct: similarMind.similarity })}
                  </span>
                </button>
              )}
            </motion.div>
          </div>

          {/* ═ RIGHT COLUMN (4 cols): Weekly + Deltas + Brain ═ */}
          <div className="col-span-4 flex flex-col gap-2 min-h-0">

            {/* Weekly Listening Chart */}
            <div className="spatial-card p-3 flex-shrink-0">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-display font-light tracking-[0.15em] uppercase text-slate-500">{t("dashboard.thisWeek")}</span>
                <div className="flex items-center gap-2">
                  <Clock size={12} className="text-slate-600" />
                  <span className="text-xs font-mono text-slate-400">{Math.floor(weeklyStats.totalMinutes / 60)}h {weeklyStats.totalMinutes % 60}m</span>
                </div>
              </div>
              <div className="flex items-end gap-1.5 h-20">
                {lastWeekDays.map((day, i) => {
                  const maxMin = Math.max(...lastWeekDays.map(d => d.minutesListened));
                  const height = (day.minutesListened / maxMin) * 100;
                  const bColor = beliefColors[day.dominantBelief].primary;
                  return (
                    <div key={day.date} className="flex-1 flex flex-col items-center gap-1">
                      <span className="text-[10px] font-mono text-slate-500">{day.minutesListened}m</span>
                      <motion.div
                        className="w-full rounded-sm"
                        style={{ backgroundColor: bColor, opacity: 0.7 }}
                        initial={{ height: 0 }}
                        animate={{ height: `${height}%` }}
                        transition={{ duration: 0.8, delay: i * 0.06 }}
                      />
                      <span className="text-[10px] font-mono text-slate-500">{t(DAY_I18N_KEYS[i])}</span>
                    </div>
                  );
                })}
              </div>
              <div className="flex justify-between mt-2 text-[11px] font-mono text-slate-500">
                <span>{t("dashboard.tracksCount", { count: weeklyStats.totalTracks })}</span>
                <span>{t("dashboard.peak", { hour: weeklyStats.peakListeningHour })}</span>
              </div>
            </div>

            {/* Belief Evolution Deltas */}
            <div className="spatial-card p-3 flex-shrink-0">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-display font-light tracking-[0.15em] uppercase text-slate-500">{t("dashboard.weeklyEvolution")}</span>
                <div className="flex items-center gap-1.5">
                  <TrendingUp size={13} style={{ color }} />
                  <span className="text-sm font-mono font-medium" style={{ color }}>+{evolution.pct}%</span>
                </div>
              </div>
              <div className="space-y-2">
                {BELIEF_NAMES.map((b, i) => {
                  const delta = weeklyStats.beliefDeltas[i];
                  const isPositive = delta >= 0;
                  const bColor = beliefColors[b].primary;
                  const absDelta = Math.abs(delta);
                  return (
                    <div key={b} className="flex items-center gap-3">
                      <div className="flex items-center gap-1.5 w-20">
                        <div className="w-2 h-2 rounded-full" style={{ background: bColor }} />
                        <span className="text-[11px] font-display text-slate-400">{t(BELIEF_I18N_KEY[b])}</span>
                      </div>
                      <div className="flex-1 h-[4px] rounded-full bg-white/5 overflow-hidden">
                        <motion.div
                          className="h-full rounded-full"
                          style={{ backgroundColor: bColor, opacity: 0.8 }}
                          initial={{ width: 0 }}
                          animate={{ width: `${Math.min(absDelta * 500, 100)}%` }}
                          transition={{ duration: 1, delay: 0.5 + i * 0.1 }}
                        />
                      </div>
                      <span className="text-[12px] font-mono w-12 text-right" style={{ color: isPositive ? bColor : "#EF4444" }}>
                        {isPositive ? "+" : ""}{(delta * 100).toFixed(0)}%
                      </span>
                    </div>
                  );
                })}
              </div>
              <p className="text-[11px] text-slate-500 font-display font-light mt-3 leading-relaxed">
                {t("insights.mockDrift").slice(0, 100)}...
              </p>
            </div>

            {/* Brain Monologue */}
            <div className="spatial-card p-3 flex-shrink-0 overflow-hidden">
              <div className="flex items-center gap-2 mb-1.5">
                <Brain size={14} style={{ color: beliefColors.reward.primary }} />
                <span className="text-xs font-display font-light tracking-[0.15em] uppercase text-slate-500">{t("dashboard.yourBrainThisWeek")}</span>
              </div>
              <p className="text-[12px] text-slate-400 leading-relaxed font-body font-light line-clamp-3">
                {monologue}
              </p>
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
          </div>

        </div>
      </div>

      {/* ═══ CHAT MODAL ═════════════════════════════════════════════ */}
      <AnimatePresence>
        {chatOpen && similarMind && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/70 backdrop-blur-sm p-4"
            onClick={() => setChatOpen(false)}
          >
            <motion.div
              initial={{ y: 100, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: 100, opacity: 0 }}
              transition={{ type: "spring", damping: 25 }}
              className="w-full max-w-lg rounded-2xl overflow-hidden"
              style={{ background: "rgba(10,10,15,0.95)", border: "1px solid rgba(255,255,255,0.06)", backdropFilter: "blur(24px)" }}
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between p-5 border-b border-white/[0.04]">
                <div className="flex items-center gap-3">
                  <NucleusDot color={beliefColors.familiarity.primary} size={5} active pulsing />
                  <div>
                    <h3 className="text-sm font-display font-medium text-slate-300">
                      {t("dashboard.mindLink", { name: similarMind.user.displayName })}
                    </h3>
                    <p className="text-xs font-mono text-slate-600">
                      {t("dashboard.neuralSimilarity", { pct: similarMind.similarity })}
                    </p>
                  </div>
                </div>
                <button onClick={() => setChatOpen(false)} className="text-slate-600 hover:text-slate-400 transition-colors">
                  <X size={18} />
                </button>
              </div>
              <div className="p-5 h-80 overflow-y-auto space-y-4">
                <div className="text-center">
                  <p className="text-xs font-mono text-slate-700 mb-2">{t("dashboard.mindsConnected")}</p>
                  <p className="text-sm text-slate-500 font-body font-light max-w-sm mx-auto">
                    {t("dashboard.sharedTraits", { count: similarMind.sharedTraits.length })}
                  </p>
                </div>
                <div className="flex gap-3">
                  <Avatar src={similarMind.user.avatarUrl || undefined} name={similarMind.user.displayName} size={32} borderColor={getPersona(similarMind.user.mind.personaId).color} />
                  <div className="flex-1">
                    <div className="rounded-xl p-3 max-w-[80%]" style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.04)" }}>
                      <p className="text-sm text-slate-400 font-body font-light">
                        {t("dashboard.chatInitial", { pct: similarMind.similarity })}
                      </p>
                    </div>
                  </div>
                </div>
                {chatMessages.map((msg, i) => (
                  <motion.div key={i} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
                    className={`flex gap-3 ${msg.from === "you" ? "flex-row-reverse" : ""}`}>
                    {msg.from === "them" && (
                      <Avatar src={similarMind.user.avatarUrl || undefined} name={similarMind.user.displayName} size={32} borderColor={getPersona(similarMind.user.mind.personaId).color} />
                    )}
                    <div className={`rounded-xl p-3 max-w-[80%] ${msg.from === "you" ? "ml-auto" : ""}`}
                      style={{ background: msg.from === "you" ? `${color}15` : "rgba(255,255,255,0.03)", border: `1px solid ${msg.from === "you" ? `${color}30` : "rgba(255,255,255,0.04)"}` }}>
                      <p className="text-sm text-slate-400 font-body font-light">{msg.text}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
              <form className="p-4 border-t border-white/[0.04]" onSubmit={(e) => { e.preventDefault(); handleSendChat(); }}>
                <div className="flex gap-3">
                  <input type="text" placeholder={t("dashboard.shareMind")} value={chatInput} onChange={(e) => setChatInput(e.target.value)}
                    className="flex-1 px-4 py-2.5 rounded-xl text-sm text-slate-300 placeholder-slate-700 font-body font-light focus:outline-none"
                    style={{ background: "rgba(0,0,0,0.5)", border: "1px solid rgba(255,255,255,0.06)" }} />
                  <Button variant="primary" size="sm" type="submit">{t("dashboard.send")}</Button>
                </div>
              </form>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

/* ── Helper Components ────────────────────────────────────────── */

function seededCompat(userId: string): number {
  let hash = 0;
  for (let i = 0; i < userId.length; i++) hash = (hash * 31 + userId.charCodeAt(i)) | 0;
  return 40 + Math.abs(hash % 59);
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
