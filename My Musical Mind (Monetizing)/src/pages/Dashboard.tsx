import { useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { motion } from "framer-motion";
import {
  Flame, ChevronRight, Sparkles, Brain,
  TrendingUp, Activity, Clock, Music,
} from "lucide-react";
import { useUserStore } from "@/stores/useUserStore";
import { getPersona } from "@/data/personas";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { BeliefMiniTrace } from "@/components/dashboard/BeliefMiniTrace";
import { MindTypeRing } from "@/components/mind/MindTypeRing";
import {
  generateWeeklyMonologue,
  generatePEInsight,
  generateBrainQuote,
} from "@/data/mind-insights";
import { beliefColors } from "@/design/tokens";
import { pageTransition, fadeIn, cinematicReveal } from "@/design/animations";
import { weeklyStats, lastWeekDays, monthlyEvolution } from "@/data/mock-listening";
import { useM3Store } from "@/stores/useM3Store";
import { M3_STAGES } from "@/data/m3-stages";
import { getPrimaryObservation } from "@/data/m3-observations";
import { getNextStage } from "@/data/m3-stages";
import { levelToOrganismStage } from "@/types/m3";
import { useActiveIdentity } from "@/hooks/useActiveIdentity";
import { DimensionRadar } from "@/components/mind/DimensionRadar";
import { DimensionPanel } from "@/components/mind/DimensionPanel";
import { useDimensions } from "@/hooks/useDimensions";
import { getPersonaDimensions } from "@/data/persona-dimensions";

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
  const { mind, level, xp, streak, tracksAnalyzed, displayName } = useUserStore();
  const m3Mind = useM3Store((s) => s.mind);
  const identity = useActiveIdentity();
  // Use M3's active persona (evolved through training), fall back to onboarding persona
  const activePersonaId = m3Mind?.activePersonaId ?? mind?.personaId;
  const persona = activePersonaId ? getPersona(activePersonaId) : null;

  if (!mind || !persona) return null;

  const color = identity.color;
  const xpForNext = level * 200;
  const xpProgress = Math.min(100, (xp % xpForNext) / xpForNext * 100);
  const evolution = useMemo(() => computeEvolution(), []);

  const monologue = useMemo(() => generateWeeklyMonologue(persona, mind.axes, t), [persona, mind.axes, t]);
  const brainQuote = useMemo(() => generateBrainQuote(identity.family, persona.id, t), [identity.family, persona.id, t]);

  // Family morphology from active identity (gene-derived)
  const family = identity.family;
  const morphology = identity.morphology;
  const organismStage = m3Mind ? levelToOrganismStage(m3Mind.level) : mind.stage;
  const personaLevel = m3Mind?.level ?? 1;

  return (
    <motion.div {...pageTransition} className="relative h-screen overflow-hidden">
      {/* Organism background — enlarged */}
      <div className="absolute inset-0 z-0" style={{ transform: "scale(1.4)", transformOrigin: "center center" }}>
        <MindOrganismCanvas
          color={color}
          secondaryColor={beliefColors.reward.primary}
          stage={organismStage}
          intensity={0.7}
          breathRate={4}
          familyMorphology={morphology}
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

            {/* 6D Dimension Radar (primary) */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 1, delay: 0.2 }}
              className="spatial-card p-3 flex flex-col items-center flex-1 min-h-0"
            >
              <div className="w-full h-full flex items-center justify-center">
                <DimensionRadar
                  profile={getPersonaDimensions(m3Mind?.activePersonaId ?? mind?.personaId ?? 1)}
                  color={color}
                  coloredAxes
                  size={280}
                />
              </div>
            </motion.div>

            {/* Dimension legend */}
            <div className="px-3 py-2 flex-shrink-0 -mt-1">
              <DimensionPanel accentColor={color} compact />
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

            {/* Mind Type (compact) */}
            {m3Mind && (
              <motion.div variants={fadeIn} initial="initial" animate="animate" className="spatial-card p-3 flex-shrink-0 flex flex-col items-center">
                <span className="text-xs font-display font-light tracking-[0.15em] uppercase text-slate-500 block mb-2 w-full">{t("m3.hub.mindType")}</span>
                <MindTypeRing genes={m3Mind.genes} size={80} showLabels={false} />
              </motion.div>
            )}
          </div>

          {/* ═ CENTER COLUMN (5 cols): Persona + Quote + PE ═══ */}
          <div className="col-span-5 flex flex-col items-center justify-center gap-4 min-h-0">

            {/* View Persona button */}
            <motion.button
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
              onClick={() => navigate(`/info/${persona.id}`)}
              className="group relative px-6 py-2 rounded-full overflow-hidden transition-all duration-500 hover:scale-[1.05]"
              style={{ background: `${color}08`, border: `1px solid ${color}20` }}
              onMouseEnter={(e) => { e.currentTarget.style.background = `${color}15`; e.currentTarget.style.boxShadow = `0 0 30px ${color}15`; }}
              onMouseLeave={(e) => { e.currentTarget.style.background = `${color}08`; e.currentTarget.style.boxShadow = "none"; }}
            >
              <motion.div
                className="absolute inset-0 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-700"
                style={{ background: `radial-gradient(ellipse at 50% 50%, ${color}12, transparent 70%)` }}
              />
              <span className="relative z-10 flex items-center gap-2 text-sm font-display font-medium tracking-wide" style={{ color }}>
                <Sparkles size={14} className="group-hover:animate-pulse" />
                {t("dashboard.viewPersona")}
                <ChevronRight size={14} className="group-hover:translate-x-0.5 transition-transform duration-300" />
              </span>
            </motion.button>

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
              <p className="text-xs font-mono text-slate-600 mt-2">— {t("dashboard.yourMind", { family: identity.family.slice(0, -1) })}</p>
            </motion.div>

            {/* M³ Widget */}
            <M3Widget color={color} />

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

            {/* Persona link */}
            <motion.div variants={fadeIn} initial="initial" animate="animate">
              <button
                onClick={() => navigate(`/info/${persona.id}`)}
                className="flex items-center gap-2 px-4 py-2 rounded-full transition-colors text-xs font-display text-slate-500 hover:text-slate-300"
                style={{ background: `${color}08`, border: `1px solid ${color}15` }}
              >
                {t("dashboard.viewPersona")} <ChevronRight size={14} />
              </button>
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

function M3Widget({ color }: { color: string }) {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const m3Mind = useM3Store((s) => s.mind);

  if (!m3Mind) return null;

  const stageDef = M3_STAGES[m3Mind.stage];
  const stageColor = stageDef.color;
  const nextStage = getNextStage(m3Mind.stage);
  const obs = getPrimaryObservation(m3Mind, t);
  const activePersona = getPersona(m3Mind.activePersonaId);

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4, duration: 0.8 }}
      className="w-full max-w-lg"
    >
      <button
        onClick={() => navigate("/m3")}
        className="w-full spatial-card p-4 text-left transition-all duration-500 hover:scale-[1.01] group"
        style={{ border: `1px solid ${stageColor}15` }}
      >
        <div className="flex items-center gap-3">
          <div
            className="w-10 h-10 rounded-xl flex items-center justify-center text-sm"
            style={{ background: `${stageColor}12`, border: `1px solid ${stageColor}20` }}
          >
            <span style={{ color: stageColor }}>{stageDef.icon}</span>
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-display font-light tracking-[0.1em] uppercase" style={{ color: `${stageColor}90` }}>
                {t("m3.dashboard.widget.title")}
              </span>
              <span className="text-[9px] font-mono px-1.5 py-0.5 rounded-full" style={{ background: `${stageColor}10`, color: stageColor }}>
                L{m3Mind.level}/12
              </span>
              {m3Mind.frozen && (
                <span className="text-[9px] font-mono px-1.5 py-0.5 rounded-full bg-white/[0.04] text-slate-600">
                  {t("m3.dashboard.widget.sleeping")}
                </span>
              )}
            </div>
            <p className="text-[12px] text-slate-400 font-body font-light mt-0.5 truncate">
              {obs.text}
            </p>
          </div>
          <ChevronRight size={14} className="text-slate-700 group-hover:text-slate-400 transition-colors" />
        </div>
        {/* Progress bar */}
        <div className="mt-2.5 flex items-center gap-2">
          <span className="text-[10px] font-display" style={{ color: stageColor }}>{t(`m3.stage.${m3Mind.stage}`)}</span>
          <div className="flex-1 h-[2px] rounded-full bg-white/[0.04] overflow-hidden">
            <motion.div
              className="h-full rounded-full"
              style={{ background: stageColor, opacity: 0.7 }}
              initial={{ width: 0 }}
              animate={{ width: `${m3Mind.stageProgress * 100}%` }}
              transition={{ duration: 1, ease: [0.22, 1, 0.36, 1] }}
            />
          </div>
          {nextStage && (
            <span className="text-[10px] font-mono text-slate-600">
              {t("m3.dashboard.widget.progress", { progress: Math.round(m3Mind.stageProgress * 100), nextStage: t(`m3.stage.${nextStage}`) })}
            </span>
          )}
        </div>
      </button>
    </motion.div>
  );
}
