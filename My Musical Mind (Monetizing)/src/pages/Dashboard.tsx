import { useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { motion } from "framer-motion";
import {
  Flame, ChevronRight, Sparkles, Brain,
  TrendingUp,
} from "lucide-react";
import { useUserStore } from "@/stores/useUserStore";
import { getPersona } from "@/data/personas";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { NeuronBrainCanvas } from "@/components/mind/NeuronBrainCanvas";
import { DimensionSunburst } from "@/components/mind/DimensionSunburst";
import {
  generateWeeklyMonologue,
  generateBrainQuote,
} from "@/data/mind-insights";
import { beliefColors } from "@/design/tokens";
import { pageTransition, fadeIn, cinematicReveal } from "@/design/animations";
import { weeklyStats } from "@/data/mock-listening";
import { useM3Store } from "@/stores/useM3Store";
import { levelToOrganismStage } from "@/types/m3";
import { useActiveIdentity } from "@/hooks/useActiveIdentity";
import { useDimensions } from "@/hooks/useDimensions";
import { ALL_PSYCHOLOGY, PSYCHOLOGY_COLORS } from "@/data/dimensions";
import type { DimensionKey6D } from "@/types/dimensions";

/* ── 6D Dimension weekly deltas (mock — matches sunburst order) ── */
const DIM_DELTAS_6D: Record<string, number> = {
  discovery: +0.08,
  intensity: +0.14,
  flow:      -0.03,
  depth:     +0.22,
  trace:     +0.11,
  sharing:   +0.05,
};

/* ── Evolution % from 6D deltas ─────────────────────────────────── */
function computeEvolution6D(): { pct: string; direction: "up" | "down" } {
  const vals = Object.values(DIM_DELTAS_6D);
  const avg = vals.reduce((a, b) => a + Math.abs(b), 0) / vals.length;
  const net = vals.reduce((a, b) => a + b, 0);
  return { pct: (avg * 100).toFixed(1), direction: net >= 0 ? "up" : "down" };
}

export function Dashboard() {
  const navigate = useNavigate();
  const { t, i18n } = useTranslation();
  const isTr = i18n.language === "tr";
  const { mind, level, xp, streak, displayName } = useUserStore();
  const m3Mind = useM3Store((s) => s.mind);
  const identity = useActiveIdentity();
  const { state: dimState } = useDimensions(isTr ? "tr" : "en");
  const activePersonaId = m3Mind?.activePersonaId ?? mind?.personaId;
  const persona = activePersonaId ? getPersona(activePersonaId) : null;

  if (!mind || !persona) return null;

  const color = identity.color;
  const xpForNext = level * 200;
  const xpProgress = Math.min(100, (xp % xpForNext) / xpForNext * 100);
  const evolution = useMemo(() => computeEvolution6D(), []);

  const monologue = useMemo(() => generateWeeklyMonologue(persona, mind.axes, t), [persona, mind.axes, t]);
  const brainQuote = useMemo(() => generateBrainQuote(identity.family, persona.id, t), [identity.family, persona.id, t]);

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
                <DimensionSunburst color={color} size={260} />
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
                  const delta = DIM_DELTAS_6D[key] ?? 0;
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

          {/* ═ CENTER COLUMN (5 cols): Persona + Neuron Brain ═══ */}
          <div className="col-span-5 flex flex-col items-center justify-center gap-3 min-h-0">

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
              <p className="text-xs font-mono text-slate-600 mt-1">— {t("dashboard.yourMind", { family: identity.family.slice(0, -1) })}</p>
            </motion.div>

            {/* Neuron Brain Visualization */}
            <motion.div
              initial={{ opacity: 0, scale: 0.85 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.5, duration: 1.2, ease: [0.22, 1, 0.36, 1] }}
              className="w-full flex-1 min-h-0 max-h-[340px] spatial-card overflow-hidden relative"
              style={{ border: `1px solid ${color}10` }}
            >
              <NeuronBrainCanvas color={color} />
            </motion.div>
          </div>

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

            {/* Your Brain This Week — Narrative */}
            <div className="spatial-card p-4 flex-shrink-0">
              <div className="flex items-center gap-2 mb-2.5">
                <Brain size={14} style={{ color: beliefColors.reward.primary }} />
                <span className="text-xs font-display font-light tracking-[0.15em] uppercase text-slate-500">{t("dashboard.yourBrainThisWeek")}</span>
              </div>
              <p className="text-[12px] text-slate-300 leading-relaxed font-body font-light">
                Your sense of musical pleasure shifted <span className="font-mono font-medium" style={{ color: PSYCHOLOGY_COLORS.depth }}>+22%</span> this week.
                That's significant — your mind is recalibrating what "good music" means to you.
                The songs that moved you last month might not hit the same way next month.
              </p>
              <p className="text-[12px] text-slate-400 leading-relaxed font-body font-light mt-2">
                Your need for closure (<span className="font-mono" style={{ color: PSYCHOLOGY_COLORS.discovery }}>75%</span>) shaped your week.
                Every resolved chord, every satisfying ending — your mind marked each one as a small victory.
                You hear music as a series of promises kept.
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
