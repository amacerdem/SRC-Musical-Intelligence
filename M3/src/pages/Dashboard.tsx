import { useState, useMemo, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  PenTool, Compass, Radio, Flame, ChevronRight, Sparkles,
  Clock, Music, BarChart3, Brain, MessageCircle, X,
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
import { Badge } from "@/components/ui/Badge";
import { mockUsers } from "@/data/mock-users";
import { lastWeekDays, weeklyStats, monthlyEvolution, recentTracks } from "@/data/mock-listening";
import {
  generateWeeklyMonologue,
  generateEvolutionNarrative,
  generatePEInsight,
  generateRecommendations,
  findSimilarMind,
  generateBrainQuote,
  getRecentTracksWithContext,
  NEUROCHEMICALS,
} from "@/data/mind-insights";
import { beliefColors, getCompatibilityLabel } from "@/design/tokens";
import { STAGE_NAMES } from "@/types/mind";
import { pageTransition, staggerChildren, slideUp, fadeIn, cinematicReveal } from "@/design/animations";
import { useScrollBatch } from "@/hooks/useScrollTrigger";
import type { MindAxes } from "@/types/mind";

/* ── Axis metadata ──────────────────────────────────────────── */
const AXIS_META: { key: keyof MindAxes; label: string; shortLabel: string; belief: keyof typeof beliefColors }[] = [
  { key: "entropyTolerance", label: "Chaos Appetite", shortLabel: "CHS", belief: "consonance" },
  { key: "resolutionCraving", label: "Need for Closure", shortLabel: "CLO", belief: "tempo" },
  { key: "monotonyTolerance", label: "Repetition Comfort", shortLabel: "RPT", belief: "familiarity" },
  { key: "salienceSensitivity", label: "Surprise Sensitivity", shortLabel: "SRP", belief: "salience" },
  { key: "tensionAppetite", label: "Tension Love", shortLabel: "TNS", belief: "reward" },
];

const BELIEF_NAMES = ["consonance", "tempo", "salience", "familiarity", "reward"] as const;
const BELIEF_LABELS: Record<string, string> = {
  consonance: "Harmony", tempo: "Rhythm", salience: "Attention", familiarity: "Memory", reward: "Pleasure",
};
const DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

export function Dashboard() {
  const navigate = useNavigate();
  const { mind, level, xp, streak, tracksAnalyzed, displayName } = useUserStore();
  const persona = mind ? getPersona(mind.personaId) : null;
  const scrollRef = useRef<HTMLDivElement>(null);
  const [chatOpen, setChatOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState<{ from: "you" | "them"; text: string }[]>([]);
  const [chatInput, setChatInput] = useState("");

  useScrollBatch(".scroll-section", scrollRef, { stagger: 0.08 });

  if (!mind || !persona) return null;

  const color = persona.color;
  const xpForNext = level * 200;
  const xpProgress = Math.min(100, (xp % xpForNext) / xpForNext * 100);

  // Generate insights
  const monologue = useMemo(() => generateWeeklyMonologue(persona, mind.axes), [persona, mind.axes]);
  const evolution = useMemo(() => generateEvolutionNarrative(mind.axes), [mind.axes]);
  const peInsight = useMemo(() => generatePEInsight(), []);
  const recommendations = useMemo(() => generateRecommendations(persona, mind.axes), [persona, mind.axes]);
  const similarMind = useMemo(() => findSimilarMind(mind.axes, persona, mockUsers), [mind.axes, persona]);
  const brainQuote = useMemo(() => generateBrainQuote(persona, mind.axes), [persona, mind.axes]);
  const recentWithContext = useMemo(() => getRecentTracksWithContext(), []);

  const handleSendChat = () => {
    const text = chatInput.trim();
    if (!text) return;
    setChatMessages((prev) => [...prev, { from: "you", text }]);
    setChatInput("");
    // Context-aware auto-reply
    setTimeout(() => {
      const otherPersona = similarMind ? getPersona(similarMind.user.mind.personaId) : null;
      const replies = [
        `That resonates with how my ${otherPersona?.name || "mind"} processes harmony. My consonance system would fire differently at that moment though — I hear the tension before the resolution.`,
        `I've been thinking about that too. My H³ temporal morphology has been shifting lately — I'm hearing longer arcs in music, not just beat-level patterns.`,
        `Your mind is ${similarMind ? similarMind.similarity : 80}% aligned with mine, but it's that ${100 - (similarMind?.similarity ?? 80)}% divergence that makes this interesting. You hear structures I literally can't predict.`,
        `My reward signal peaks in different places than yours — where you get the DA spike, I get the slow serotonin build. That's what makes shared listening between our minds transformative.`,
        `Have you tried listening at your peak hour? My salience sensitivity changes dramatically between morning and ${weeklyStats.peakListeningHour > 18 ? "late night" : "evening"} sessions.`,
      ];
      setChatMessages((prev) => [...prev, { from: "them", text: replies[prev.length % replies.length] }]);
    }, 1200);
  };

  return (
    <motion.div {...pageTransition} className="relative min-h-screen overflow-hidden pb-16">
      {/* ═══════════════════════════════════════════════════════════════
       *  HERO: Centered Organism — THE focal point
       *  Everything orbits this. Full viewport height.
       * ═══════════════════════════════════════════════════════════ */}
      <div className="relative h-[85vh] min-h-[600px] flex flex-col items-center justify-center">
        {/* Organism — dead center, full bleed */}
        <div className="absolute inset-0 z-0">
          <MindOrganismCanvas
            color={color}
            secondaryColor={beliefColors.reward.primary}
            stage={mind.stage}
            intensity={0.7}
            breathRate={4}
            className="w-full h-full"
            interactive
          />
        </div>

        {/* Radial gradient overlay for depth */}
        <div className="absolute inset-0 z-[1] pointer-events-none"
          style={{ background: `radial-gradient(ellipse 50% 50% at 50% 50%, transparent 30%, rgba(0,0,0,0.7) 70%, rgba(0,0,0,0.95) 100%)` }}
        />

        {/* Cinematic vignette */}
        <div className="cinematic-vignette z-[2]" />

        {/* Identity overlay — top */}
        <motion.div {...cinematicReveal} className="relative z-10 text-center mb-auto pt-10">
          <span className="hud-label" style={{ color: `${color}80` }}>{STAGE_NAMES[mind.stage]}</span>
          {displayName && displayName !== "You" && (
            <p className="text-sm text-slate-500 mt-1 font-display font-light">
              Welcome back, <span className="text-slate-300 font-medium">{displayName}</span>
            </p>
          )}
        </motion.div>

        {/* Persona name — center below organism */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1.5, ease: [0.22, 1, 0.36, 1], delay: 0.3 }}
          className="relative z-10 text-center"
        >
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-display font-bold tracking-tight leading-none" style={{ color }}>
            {persona.name}
          </h1>
          <p className="text-sm md:text-base text-slate-600 mt-3 font-display font-light italic max-w-md mx-auto">
            {persona.tagline}
          </p>
        </motion.div>

        {/* HUD stats — bottom */}
        <motion.div
          variants={fadeIn}
          initial="initial"
          animate="animate"
          className="relative z-10 mt-auto pb-8 flex items-end justify-between w-full max-w-2xl px-6"
        >
          <div className="flex gap-6">
            <HUDStat label="Streak" value={`${streak}d`} icon={<Flame size={12} />} accent={color} />
            <HUDStat label="Tracks" value={String(tracksAnalyzed)} />
            <HUDStat label="Level" value={String(level)} />
          </div>
          <div className="flex items-center gap-3">
            <div className="w-32 h-1 rounded-full overflow-hidden" style={{ background: `${color}10` }}>
              <motion.div className="h-full rounded-full" style={{ background: color, opacity: 0.6 }}
                initial={{ width: 0 }} animate={{ width: `${xpProgress}%` }}
                transition={{ duration: 1.2, ease: [0.22, 1, 0.36, 1] }}
              />
            </div>
            <span className="text-[10px] font-mono text-slate-600">{xp.toLocaleString()} XP</span>
          </div>
        </motion.div>

        {/* Action pills — floating bottom-center */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="absolute bottom-4 z-10 flex gap-3"
        >
          <ActionPill icon={<PenTool size={16} />} label="Compose" color="#A855F7" onClick={() => navigate("/compose")} />
          <ActionPill icon={<Compass size={16} />} label="Discover" color="#6366F1" onClick={() => navigate("/discover")} />
          <ActionPill icon={<Radio size={16} />} label="Live" color="#EC4899" onClick={() => navigate("/live")} />
        </motion.div>
      </div>

      {/* ═══════════════════════════════════════════════════════════════
       *  CONTENT: Scrollable sections below the organism
       * ═══════════════════════════════════════════════════════════ */}
      <div ref={scrollRef} className="relative z-10 max-w-5xl xl:max-w-6xl 2xl:max-w-7xl mx-auto px-4 sm:px-6 md:px-8">

        {/* ── YOUR BRAIN THIS WEEK ──────────────────────────────── */}
        <div className="scroll-section mt-12 mb-16">
          <div className="flex items-center gap-2 mb-6">
            <Brain size={14} style={{ color: beliefColors.reward.primary }} />
            <span className="hud-label">Your Week in Music</span>
          </div>
          <div className="spatial-card p-8 glow-border" style={{ "--glow-color": color } as React.CSSProperties}>
            <p className="text-sm md:text-base text-slate-400 leading-relaxed font-body font-light">
              {monologue}
            </p>
            <div className="mt-6 flex items-center gap-4">
              {Object.entries(NEUROCHEMICALS).map(([key, nc]) => (
                <div key={key} className="flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 rounded-full" style={{ background: nc.color }} />
                  <span className="text-[9px] font-mono" style={{ color: `${nc.color}80` }}>{nc.emoji}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* ── WEEKLY LISTENING PATTERN ──────────────────────────── */}
        <div className="scroll-section mb-16">
          <div className="flex items-center gap-2 mb-6">
            <Clock size={14} className="text-slate-600" />
            <span className="hud-label">This Week</span>
            <span className="text-[10px] font-mono text-slate-700 ml-auto">
              {weeklyStats.totalMinutes} min · {weeklyStats.totalTracks} tracks
            </span>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Daily listening bars */}
            <div className="spatial-card p-6">
              <span className="hud-label mb-4 block">Daily Listening</span>
              <div className="flex items-end gap-2 h-32">
                {lastWeekDays.map((day, i) => {
                  const maxMin = Math.max(...lastWeekDays.map(d => d.minutesListened));
                  const height = (day.minutesListened / maxMin) * 100;
                  const bColor = beliefColors[day.dominantBelief].primary;
                  return (
                    <div key={day.date} className="flex-1 flex flex-col items-center gap-1">
                      <span className="text-[9px] font-mono text-slate-700">{day.minutesListened}m</span>
                      <motion.div
                        className="w-full rounded-t-sm"
                        style={{ backgroundColor: bColor, opacity: 0.6 }}
                        initial={{ height: 0 }}
                        animate={{ height: `${height}%` }}
                        transition={{ duration: 0.8, delay: i * 0.08, ease: [0.22, 1, 0.36, 1] }}
                      />
                      <span className="text-[9px] font-mono text-slate-700">{DAY_NAMES[i]}</span>
                    </div>
                  );
                })}
              </div>
              <div className="flex items-center gap-2 mt-4">
                <span className="text-[10px] text-slate-700 font-mono">Peak hour:</span>
                <span className="hud-value text-xs">{weeklyStats.peakListeningHour}:00</span>
              </div>
            </div>

            {/* Genre breakdown + Belief deltas */}
            <div className="spatial-card p-6">
              <span className="hud-label mb-4 block">Genre Spectrum</span>
              <div className="space-y-2.5 mb-6">
                {weeklyStats.topGenres.map((g) => (
                  <div key={g.name} className="flex items-center gap-3">
                    <span className="text-[11px] text-slate-500 font-body font-light w-24 truncate">{g.name}</span>
                    <div className="flex-1 h-[3px] rounded-full bg-white/5 overflow-hidden">
                      <motion.div
                        className="h-full rounded-full"
                        style={{ backgroundColor: color, opacity: 0.3 + (g.pct / 100) * 0.5 }}
                        initial={{ width: 0 }}
                        animate={{ width: `${g.pct}%` }}
                        transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
                      />
                    </div>
                    <span className="text-[10px] font-mono text-slate-600 w-8 text-right">{g.pct}%</span>
                  </div>
                ))}
              </div>

              <span className="hud-label mb-3 block">How You're Shifting</span>
              <div className="flex gap-3">
                {BELIEF_NAMES.map((b, i) => {
                  const delta = weeklyStats.beliefDeltas[i];
                  const bColor = beliefColors[b].primary;
                  return (
                    <div key={b} className="flex-1 text-center">
                      <NucleusDot color={bColor} size={3} active />
                      <div className="text-[10px] font-mono mt-1" style={{ color: delta >= 0 ? bColor : "#EF4444" }}>
                        {delta >= 0 ? "+" : ""}{(delta * 100).toFixed(0)}%
                      </div>
                      <div className="text-[8px] font-mono text-slate-700 mt-0.5">{b.slice(0, 4)}</div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>

        {/* ── PEAK PREDICTION ERROR EVENT ────────────────────────── */}
        <div className="scroll-section mb-16">
          <div className="spatial-card p-6 glow-border" style={{ "--glow-color": beliefColors.reward.primary } as React.CSSProperties}>
            <div className="flex items-start gap-4">
              <div className="mt-1">
                <Sparkles size={16} style={{ color: beliefColors.reward.primary }} />
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <span className="hud-label" style={{ color: `${beliefColors.reward.primary}80` }}>Your Biggest Surprise</span>
                  <span className="hud-value text-sm">{peInsight.title}</span>
                </div>
                <p className="text-xs text-slate-500 leading-relaxed font-body font-light">{peInsight.body}</p>
              </div>
            </div>
          </div>
        </div>

        {/* ── BELIEF TRACES ─────────────────────────────────────── */}
        <div className="scroll-section mb-16">
          <div className="flex items-center gap-2 mb-6">
            <BarChart3 size={14} className="text-slate-600" />
            <span className="hud-label">Your Mind in Motion</span>
          </div>
          <div className="spatial-card p-6">
            <BeliefMiniTrace height={120} />
            <div className="flex gap-4 mt-3">
              {BELIEF_NAMES.map((b) => (
                <div key={b} className="flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 rounded-full" style={{ background: beliefColors[b].primary }} />
                  <span className="text-[9px] font-mono capitalize" style={{ color: `${beliefColors[b].primary}80` }}>
                    {BELIEF_LABELS[b]}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* ── MONTHLY EVOLUTION ─────────────────────────────────── */}
        <div className="scroll-section mb-16">
          <div className="flex items-center gap-2 mb-6">
            <span className="hud-label">How You've Grown — 4 Weeks</span>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-[2fr_3fr] gap-6">
            {/* Monthly belief trajectory chart */}
            <div className="spatial-card p-6">
              <span className="hud-label mb-4 block">Your Journey</span>
              <div className="space-y-4">
                {BELIEF_NAMES.map((b, bIdx) => {
                  const values = monthlyEvolution.weeklySnapshots.map(s => s[bIdx]);
                  const bColor = beliefColors[b].primary;
                  return (
                    <div key={b}>
                      <div className="flex items-center justify-between mb-1">
                        <div className="flex items-center gap-1.5">
                          <NucleusDot color={bColor} size={3} active />
                          <span className="text-[10px] font-body font-medium text-slate-500">{BELIEF_LABELS[b]}</span>
                        </div>
                        <span className="text-[10px] font-mono" style={{ color: bColor }}>
                          {values[0].toFixed(2)} → {values[3].toFixed(2)}
                        </span>
                      </div>
                      <div className="flex items-center gap-1">
                        {values.map((v, wi) => (
                          <div key={wi} className="flex-1 h-[4px] rounded-full overflow-hidden bg-white/5">
                            <motion.div
                              className="h-full rounded-full"
                              style={{ backgroundColor: bColor, opacity: 0.3 + v * 0.6 }}
                              initial={{ width: 0 }}
                              animate={{ width: `${v * 100}%` }}
                              transition={{ duration: 0.8, delay: wi * 0.1 }}
                            />
                          </div>
                        ))}
                      </div>
                    </div>
                  );
                })}
              </div>
              <div className="flex justify-between mt-3 text-[8px] font-mono text-slate-700">
                <span>Week 1</span><span>Week 2</span><span>Week 3</span><span>Now</span>
              </div>
            </div>

            {/* Evolution narrative */}
            <div className="spatial-card p-6">
              <span className="hud-label mb-4 block">What's Changing</span>
              <div className="space-y-4">
                {evolution.map((line, i) => (
                  <motion.p
                    key={i}
                    initial={{ opacity: 0, x: 10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.6, delay: i * 0.15 }}
                    className="text-xs text-slate-500 leading-relaxed font-body font-light pl-3"
                    style={{ borderLeft: `2px solid ${beliefColors[BELIEF_NAMES[i % 5]].primary}20` }}
                  >
                    {line}
                  </motion.p>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* ── RECENT TRACKS WITH NEURAL CONTEXT ─────────────────── */}
        <div className="scroll-section mb-16">
          <div className="flex items-center gap-2 mb-6">
            <Music size={14} className="text-slate-600" />
            <span className="hud-label">Recent Listening</span>
          </div>
          <div className="spatial-card p-6 space-y-4">
            {recentWithContext.map((track, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: i * 0.08 }}
                className="flex items-start gap-4 py-3 border-b border-white/[0.03] last:border-0"
              >
                <div className="relative w-10 h-10 rounded-lg flex items-center justify-center overflow-hidden shrink-0">
                  <MiniOrganism
                    color={track.rewardIntensity > 0.85 ? beliefColors.reward.primary : color}
                    stage={1}
                    size={40}
                  />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <h4 className="text-sm font-body font-medium text-slate-300 truncate">{track.title}</h4>
                    <span className="text-[10px] font-mono text-slate-700">{track.listenedAt}</span>
                  </div>
                  <p className="text-[11px] text-slate-600 font-body font-light">{track.artist} · {track.genre}</p>
                  <p className="text-[10px] text-slate-700 font-mono mt-1">
                    Peak: {track.peakRewardMoment}
                  </p>
                  <p className="text-[10px] text-slate-600 font-body font-light mt-1 leading-relaxed">
                    {track.neuralContext}
                  </p>
                </div>
                <div className="shrink-0">
                  <div className="w-8 h-8 rounded-full flex items-center justify-center"
                    style={{ background: `${beliefColors.reward.primary}${Math.round(track.rewardIntensity * 30).toString(16).padStart(2, '0')}` }}
                  >
                    <span className="text-[9px] font-mono" style={{ color: beliefColors.reward.primary }}>
                      {(track.rewardIntensity * 100).toFixed(0)}
                    </span>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* ── MIND AXES (compact) ───────────────────────────────── */}
        <div className="scroll-section mb-16">
          <span className="hud-label mb-5 block">Your Musical DNA</span>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
            {AXIS_META.map((axis, i) => {
              const value = mind.axes[axis.key];
              const pct = Math.round(value * 100);
              const axisColor = beliefColors[axis.belief].primary;
              return (
                <div key={axis.key} className="spatial-card p-4">
                  <div className="flex items-center gap-1.5 mb-2">
                    <NucleusDot color={axisColor} size={3} active />
                    <span className="hud-label">{axis.shortLabel}</span>
                    <span className="hud-value text-xs ml-auto" style={{ color: axisColor }}>{pct}</span>
                  </div>
                  <div className="w-full h-[3px] rounded-full bg-white/5 overflow-hidden">
                    <motion.div
                      className="h-full rounded-full"
                      style={{ backgroundColor: axisColor }}
                      initial={{ width: 0 }}
                      animate={{ width: `${pct}%` }}
                      transition={{ duration: 1, ease: [0.22, 1, 0.36, 1], delay: i * 0.08 }}
                    />
                  </div>
                  <p className="text-[9px] text-slate-600 mt-1.5 font-body font-light">{axis.label}</p>
                </div>
              );
            })}
          </div>
        </div>

        {/* ── NEUROSCIENCE-BACKED RECOMMENDATIONS ───────────────── */}
        <div className="scroll-section mb-16">
          <div className="flex items-center gap-2 mb-6">
            <Sparkles size={14} style={{ color: beliefColors.consonance.primary }} />
            <span className="hud-label">Your Mind Would Love</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {recommendations.map((rec, i) => {
              const bColor = beliefColors[rec.belief].primary;
              return (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: i * 0.1 }}
                  className="spatial-card p-5 cursor-pointer group hover:bg-white/[0.02] transition-colors"
                  onClick={() => navigate("/discover")}
                >
                  <div className="flex items-start gap-3">
                    <div className="relative w-10 h-10 rounded-lg flex items-center justify-center overflow-hidden shrink-0">
                      <MiniOrganism color={bColor} stage={1} size={40} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h4 className="text-sm font-body font-medium text-slate-300 group-hover:text-slate-100 transition-colors">
                        {rec.title}
                      </h4>
                      <p className="text-[11px] text-slate-600 font-body font-light">{rec.artist}</p>
                    </div>
                    <Badge label={BELIEF_LABELS[rec.belief]} color={bColor} />
                  </div>
                  <p className="text-[10px] text-slate-500 leading-relaxed font-body font-light mt-3">{rec.reason}</p>
                  <p className="text-[9px] font-mono mt-2" style={{ color: `${bColor}60` }}>{rec.peOptimization}</p>
                </motion.div>
              );
            })}
          </div>
        </div>

        {/* ── SIMILAR MIND MATCH ────────────────────────────────── */}
        {similarMind && (
          <div className="scroll-section mb-16">
            <div className="flex items-center gap-2 mb-6">
              <NucleusDot color={beliefColors.familiarity.primary} size={5} active pulsing />
              <span className="hud-label">Similar Mind Detected</span>
            </div>

            <div className="spatial-card p-8 glow-border" style={{ "--glow-color": beliefColors.familiarity.primary } as React.CSSProperties}>
              <div className="grid grid-cols-1 lg:grid-cols-[1fr_auto_1fr] gap-8 items-center">
                {/* Your profile */}
                <div className="text-center">
                  <div className="relative w-16 h-16 mx-auto mb-3">
                    <div className="absolute -inset-2 opacity-30 pointer-events-none">
                      <MiniOrganism color={color} stage={mind.stage} size={80} />
                    </div>
                    <div className="relative z-10 w-16 h-16 rounded-full flex items-center justify-center"
                      style={{ background: `${color}15`, border: `1px solid ${color}30` }}
                    >
                      <span className="text-sm font-display font-bold" style={{ color }}>You</span>
                    </div>
                  </div>
                  <p className="text-xs font-body font-medium text-slate-400">{persona.name}</p>
                  <p className="text-[10px] font-body font-light text-slate-600">{persona.family}</p>
                </div>

                {/* Radar comparison + similarity */}
                <div className="flex flex-col items-center gap-4">
                  <MindRadar
                    axes={mind.axes}
                    color={color}
                    compareAxes={similarMind.user.mind.axes}
                    compareColor={getPersona(similarMind.user.mind.personaId).color}
                    size={180}
                  />
                  <div className="text-center">
                    <span className="hud-value text-2xl" style={{ color: beliefColors.familiarity.primary }}>
                      {similarMind.similarity}%
                    </span>
                    <p className="text-[10px] font-mono text-slate-600 mt-1">Mind Similarity</p>
                  </div>
                </div>

                {/* Their profile */}
                <div className="text-center">
                  <div className="relative w-16 h-16 mx-auto mb-3">
                    <div className="absolute -inset-2 opacity-30 pointer-events-none">
                      <MiniOrganism color={getPersona(similarMind.user.mind.personaId).color} stage={1} size={80} />
                    </div>
                    <div className="relative z-10">
                      <Avatar
                        src={similarMind.user.avatarUrl || undefined}
                        name={similarMind.user.displayName}
                        size={64}
                        borderColor={getPersona(similarMind.user.mind.personaId).color}
                      />
                    </div>
                  </div>
                  <p className="text-xs font-body font-medium text-slate-400">{similarMind.user.displayName}</p>
                  <p className="text-[10px] font-body font-light text-slate-600">
                    {getPersona(similarMind.user.mind.personaId).name}
                  </p>
                </div>
              </div>

              {/* Shared traits */}
              <div className="mt-6 pt-6 border-t border-white/[0.04]">
                <div className="flex flex-wrap gap-2 mb-3">
                  {similarMind.sharedTraits.map((trait) => (
                    <span key={trait} className="text-[10px] font-mono px-2.5 py-1 rounded-full"
                      style={{ background: `${beliefColors.familiarity.primary}10`, color: `${beliefColors.familiarity.primary}80`, border: `1px solid ${beliefColors.familiarity.primary}20` }}
                    >
                      {trait}
                    </span>
                  ))}
                </div>
                <p className="text-[11px] text-slate-500 font-body font-light leading-relaxed mb-2">
                  {similarMind.connectionInsight}
                </p>
                <p className="text-[10px] text-slate-600 font-body font-light italic">{similarMind.divergence}</p>
              </div>

              {/* Connect Minds CTA */}
              <div className="mt-6 flex justify-center">
                <Button
                  variant="primary"
                  size="lg"
                  onClick={() => setChatOpen(true)}
                >
                  <MessageCircle size={16} className="mr-2" />
                  Connect Minds?
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* ── BRAIN QUOTE ───────────────────────────────────────── */}
        <div className="scroll-section mb-16">
          <div className="spatial-card p-8 text-center">
            <Brain size={20} className="mx-auto mb-4" style={{ color: `${color}40` }} />
            <p className="text-sm md:text-base text-slate-400 font-display font-light italic max-w-2xl mx-auto leading-relaxed">
              "{brainQuote}"
            </p>
            <p className="text-[10px] font-mono text-slate-700 mt-4">— Your {persona.family.slice(0, -1)} Mind</p>
          </div>
        </div>

        {/* ── FRIEND'S MINDS ────────────────────────────────────── */}
        <div className="scroll-section mb-8">
          <div className="flex items-center justify-between mb-5">
            <span className="hud-label">Friend's Minds</span>
            <button onClick={() => navigate("/friends")} className="flex items-center gap-1 text-[10px] uppercase tracking-widest text-slate-600 hover:text-slate-400 transition-colors">
              See All <ChevronRight size={12} />
            </button>
          </div>
          <div className="flex gap-4 overflow-x-auto pb-2 scrollbar-hide">
            {mockUsers.slice(0, 8).map((user) => {
              const userPersona = getPersona(user.mind.personaId);
              const compat = seededCompat(user.id);
              const compatLabel = getCompatibilityLabel(compat);
              return (
                <button
                  key={user.id}
                  onClick={() => navigate(`/friends/${user.id}`)}
                  className="flex-shrink-0 w-36 spatial-card p-4 text-center group"
                >
                  <div className="relative w-12 h-12 mx-auto mb-2">
                    <div className="absolute -inset-1 opacity-40 pointer-events-none">
                      <MiniOrganism color={userPersona.color} stage={1} size={56} />
                    </div>
                    <div className="relative z-10">
                      <Avatar src={user.avatarUrl || undefined} name={user.displayName} size={48} borderColor={userPersona.color} />
                    </div>
                  </div>
                  <div className="text-xs font-body font-medium text-slate-400 truncate group-hover:text-slate-200 transition-colors">{user.displayName}</div>
                  <div className="text-[10px] font-mono mt-0.5" style={{ color: compatLabel.color }}>{compat}%</div>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* ═══════════════════════════════════════════════════════════════
       *  CHAT MODAL — "Connect Minds" conversation
       * ═══════════════════════════════════════════════════════════ */}
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
              {/* Chat header */}
              <div className="flex items-center justify-between p-5 border-b border-white/[0.04]">
                <div className="flex items-center gap-3">
                  <div className="relative">
                    <NucleusDot color={beliefColors.familiarity.primary} size={5} active pulsing />
                  </div>
                  <div>
                    <h3 className="text-sm font-display font-medium text-slate-300">
                      Mind Link: {similarMind.user.displayName}
                    </h3>
                    <p className="text-[10px] font-mono text-slate-600">
                      {similarMind.similarity}% neural similarity · {getPersona(similarMind.user.mind.personaId).name}
                    </p>
                  </div>
                </div>
                <button onClick={() => setChatOpen(false)} className="text-slate-600 hover:text-slate-400 transition-colors">
                  <X size={18} />
                </button>
              </div>

              {/* Chat body */}
              <div className="p-5 h-80 overflow-y-auto space-y-4">
                {/* System message */}
                <div className="text-center">
                  <p className="text-[10px] font-mono text-slate-700 mb-2">Minds connected</p>
                  <p className="text-[11px] text-slate-600 font-body font-light max-w-sm mx-auto">
                    Your auditory cortices share {similarMind.sharedTraits.length} processing traits.
                    Start by sharing what you're listening to.
                  </p>
                </div>

                {/* Auto-generated opening from "them" */}
                <div className="flex gap-3">
                  <Avatar src={similarMind.user.avatarUrl || undefined} name={similarMind.user.displayName} size={28} borderColor={getPersona(similarMind.user.mind.personaId).color} />
                  <div className="flex-1">
                    <div className="rounded-xl p-3 max-w-[80%]"
                      style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.04)" }}
                    >
                      <p className="text-xs text-slate-400 font-body font-light">
                        Hey! I saw we matched at {similarMind.similarity}%. I've been deep into {weeklyStats.topGenres[0].name} this week too — what's your peak track been?
                      </p>
                    </div>
                    <span className="text-[9px] font-mono text-slate-700 mt-1 block">just now</span>
                  </div>
                </div>

                {/* User messages */}
                {chatMessages.map((msg, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`flex gap-3 ${msg.from === "you" ? "flex-row-reverse" : ""}`}
                  >
                    {msg.from === "them" && (
                      <Avatar src={similarMind.user.avatarUrl || undefined} name={similarMind.user.displayName} size={28} borderColor={getPersona(similarMind.user.mind.personaId).color} />
                    )}
                    <div className={`rounded-xl p-3 max-w-[80%] ${msg.from === "you" ? "ml-auto" : ""}`}
                      style={{
                        background: msg.from === "you" ? `${color}15` : "rgba(255,255,255,0.03)",
                        border: `1px solid ${msg.from === "you" ? `${color}30` : "rgba(255,255,255,0.04)"}`,
                      }}
                    >
                      <p className="text-xs text-slate-400 font-body font-light">{msg.text}</p>
                    </div>
                  </motion.div>
                ))}
              </div>

              {/* Chat input */}
              <form
                className="p-4 border-t border-white/[0.04]"
                onSubmit={(e) => { e.preventDefault(); handleSendChat(); }}
              >
                <div className="flex gap-3">
                  <input
                    type="text"
                    placeholder="Share your mind..."
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    className="flex-1 px-4 py-2.5 rounded-xl text-sm text-slate-300 placeholder-slate-700 font-body font-light focus:outline-none"
                    style={{ background: "rgba(0,0,0,0.5)", border: "1px solid rgba(255,255,255,0.06)" }}
                  />
                  <Button variant="primary" size="sm" type="submit">Send</Button>
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
      <div className="hud-label mb-0.5">{label}</div>
      <div className="flex items-center gap-1.5">
        {icon && <span style={{ color: accent ?? "#94A3B8" }}>{icon}</span>}
        <span className="hud-value">{value}</span>
      </div>
    </div>
  );
}

function ActionPill({ icon, label, color, onClick }: { icon: React.ReactNode; label: string; color: string; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="group flex items-center gap-2 px-5 py-2.5 rounded-full transition-all duration-500 hover:scale-[1.03]"
      style={{ background: `${color}08`, border: `1px solid ${color}12`, backdropFilter: "blur(12px)" }}
      onMouseEnter={(e) => { e.currentTarget.style.background = `${color}15`; e.currentTarget.style.borderColor = `${color}30`; e.currentTarget.style.boxShadow = `0 0 30px ${color}10`; }}
      onMouseLeave={(e) => { e.currentTarget.style.background = `${color}08`; e.currentTarget.style.borderColor = `${color}12`; e.currentTarget.style.boxShadow = "none"; }}
    >
      <span style={{ color }} className="opacity-50 group-hover:opacity-100 transition-opacity">{icon}</span>
      <span className="text-xs font-display font-medium text-slate-500 group-hover:text-slate-200 transition-colors">{label}</span>
    </button>
  );
}
