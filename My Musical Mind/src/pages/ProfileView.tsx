import { useState, useMemo, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { useTranslation } from "react-i18next";
import {
  ArrowLeft, Headphones, Flame, TrendingUp, Trophy, Clock, Music,
  Brain, MessageCircle, X, Sparkles,
} from "lucide-react";
import { mockUsers } from "@/data/mock-users";
import { getPersona } from "@/data/personas";
import { achievements as allAchievements } from "@/data/levels";
import { useUserStore } from "@/stores/useUserStore";
import { getCompatibilityLabel, beliefColors } from "@/design/tokens";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { MindRadar } from "@/components/mind/MindRadar";
import { MiniOrganism } from "@/components/mind/MiniOrganism";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Avatar } from "@/components/ui/Avatar";
import { LevelBadge } from "@/components/mind/LevelBadge";
import { pageTransition, staggerChildren, slideUp, cinematicReveal, fadeIn } from "@/design/animations";
import { STAGE_NAMES } from "@/types/mind";
import { useScrollBatch } from "@/hooks/useScrollTrigger";
import type { MindAxes } from "@/types/mind";

const AXIS_LABELS: { key: keyof MindAxes; label: string; short: string; belief: keyof typeof beliefColors }[] = [
  { key: "entropyTolerance", label: "Chaos", short: "CHS", belief: "consonance" },
  { key: "resolutionCraving", label: "Closure", short: "CLO", belief: "tempo" },
  { key: "monotonyTolerance", label: "Repetition", short: "RPT", belief: "familiarity" },
  { key: "salienceSensitivity", label: "Surprise", short: "SRP", belief: "salience" },
  { key: "tensionAppetite", label: "Tension", short: "TNS", belief: "reward" },
];

const BELIEF_NAMES = ["consonance", "tempo", "salience", "familiarity", "reward"] as const;
const BELIEF_LABELS: Record<string, string> = {
  consonance: "Harm", tempo: "Rhtm", salience: "Attn", familiarity: "Mem", reward: "Plsr",
};

function computeCompatibility(a: MindAxes, b: MindAxes): number {
  const keys: (keyof MindAxes)[] = [
    "entropyTolerance", "resolutionCraving", "monotonyTolerance",
    "salienceSensitivity", "tensionAppetite",
  ];
  const totalDist = keys.reduce((sum, k) => sum + Math.abs(a[k] - b[k]), 0);
  return Math.round(Math.max(0, 100 - (totalDist / keys.length) * 100));
}

/** Generate a neural compatibility narrative between two minds */
function generateCompatNarrative(userAxes: MindAxes, myAxes: MindAxes, userPersona: string, compat: number, t: (key: string, opts?: Record<string, string>) => string): string {
  type AxisWithDiff = { key: keyof MindAxes; label: string; short: string; belief: string; diff: number };
  const closestAxis = AXIS_LABELS.reduce<AxisWithDiff>((best, ax) => {
    const diff = Math.abs(userAxes[ax.key] - myAxes[ax.key]);
    return diff < best.diff ? { ...ax, diff } : best;
  }, { ...AXIS_LABELS[0], diff: 1 });

  const furthestAxis = AXIS_LABELS.reduce<AxisWithDiff>((best, ax) => {
    const diff = Math.abs(userAxes[ax.key] - myAxes[ax.key]);
    return diff > best.diff ? { ...ax, diff } : best;
  }, { ...AXIS_LABELS[0], diff: 0 });

  const closestLabel = t(`axes.profileShort.${closestAxis.key}`).toLowerCase();
  const furthestLabel = t(`axes.profileShort.${furthestAxis.key}`).toLowerCase();

  if (compat >= 90) {
    return t("insights.compatNarrative.high", { persona: userPersona, axis: closestLabel });
  } else if (compat >= 70) {
    return t("insights.compatNarrative.good", { closestAxis: closestLabel, furthestAxis: furthestLabel });
  } else if (compat >= 50) {
    return t("insights.compatNarrative.mid", { closestAxis: closestLabel, furthestAxis: furthestLabel });
  }
  return t("insights.compatNarrative.low");
}

export function ProfileView() {
  const { t } = useTranslation();
  const { userId } = useParams<{ userId: string }>();
  const navigate = useNavigate();
  const { mind: myMind } = useUserStore();
  const scrollRef = useRef<HTMLDivElement>(null);
  const [chatOpen, setChatOpen] = useState(false);
  const [messages, setMessages] = useState<{ from: "them" | "you"; text: string }[]>([]);

  useScrollBatch(".scroll-section", scrollRef, { stagger: 0.08 });

  const user = mockUsers.find((u) => u.id === userId);

  if (!user) {
    return (
      <motion.div {...pageTransition} className="flex flex-col items-center justify-center h-96 gap-4 bg-black">
        <p className="text-2xl font-display font-bold text-slate-500">{t("profile.mindNotFound")}</p>
        <p className="text-slate-600 font-body font-light">{t("profile.mindNotFoundDesc")}</p>
        <Button variant="glass" size="sm" onClick={() => navigate("/friends")}>
          <ArrowLeft size={16} className="mr-2" />{t("profile.backToFriends")}
        </Button>
      </motion.div>
    );
  }

  const persona = getPersona(user.mind.personaId);
  const myPersona = myMind ? getPersona(myMind.personaId) : null;
  const userAchievements = user.achievements.map((aid) => allAchievements.find((a) => a.id === aid)).filter(Boolean);

  const compatibility = myMind ? computeCompatibility(myMind.axes, user.mind.axes) : null;
  const compatLabel = compatibility !== null ? getCompatibilityLabel(compatibility) : null;
  const compatNarrative = useMemo(
    () => myMind && compatibility !== null
      ? generateCompatNarrative(user.mind.axes, myMind.axes, t(`personas.${persona.id}.name`), compatibility, t)
      : null,
    [user.mind.axes, myMind, persona.id, compatibility, t],
  );

  const listening = user.listening;
  const recentTracks = user.recentTracks;

  const handleSendMessage = (text: string) => {
    if (!text.trim()) return;
    setMessages((prev) => [...prev, { from: "you", text }]);
    // Auto-reply after a short delay
    setTimeout(() => {
      const replies = [
        `That's interesting — my ${persona.name} mind hears that differently. I'd probably catch the harmonic shift before the melody change.`,
        `I've been deep into ${listening?.topGenres[0]?.name || "new genres"} lately. It's changing how I hear everything else too.`,
        `We both score high on ${AXIS_LABELS[Math.floor(Math.random() * 5)].label.toLowerCase()} — I can feel it in how we describe music.`,
        `Have you noticed how different genres hit you differently? My pleasure response shifts completely between ${listening?.topGenres[0]?.name || "Electronic"} and ${listening?.topGenres[1]?.name || "Jazz"}.`,
      ];
      setMessages((prev) => [...prev, { from: "them", text: replies[prev.length % replies.length] }]);
    }, 1200);
  };

  return (
    <motion.div {...pageTransition} className="min-h-screen bg-black relative overflow-hidden pb-16">
      {/* Organism background */}
      <div className="absolute inset-0 opacity-[0.12] pointer-events-none">
        <MindOrganismCanvas color={persona.color} stage={user.mind.stage} intensity={0.5} breathRate={5} className="w-full h-full" />
      </div>
      <div className="cinematic-vignette" />
      <div className="absolute top-20 left-1/2 -translate-x-1/2 w-[500px] h-[400px] rounded-full blur-[180px] opacity-10 pointer-events-none"
        style={{ backgroundColor: persona.color }}
      />

      {/* Back */}
      <div className="relative z-20 mb-6 pt-4 px-4">
        <Button variant="ghost" size="sm" onClick={() => navigate("/friends")}>
          <ArrowLeft size={16} className="mr-2" />Back
        </Button>
      </div>

      <div ref={scrollRef} className="relative z-10 max-w-5xl xl:max-w-6xl 2xl:max-w-7xl mx-auto px-4 sm:px-6">
        <motion.div variants={staggerChildren} initial="initial" animate="animate">

          {/* ── HERO ──────────────────────────────────────────── */}
          <motion.div variants={cinematicReveal} className="scroll-section mb-12">
            <div className="flex items-start gap-5 mb-5">
              <div className="relative">
                <div className="absolute -inset-2 opacity-40 pointer-events-none">
                  <MiniOrganism color={persona.color} stage={user.mind.stage} size={88} />
                </div>
                <div className="relative z-10">
                  <Avatar src={user.avatarUrl || undefined} name={user.displayName} size={80} borderColor={persona.color} />
                </div>
              </div>
              <div className="flex-1">
                <h1 className="text-3xl md:text-4xl font-display font-bold text-slate-100 tracking-tight">
                  {user.displayName}
                </h1>
                <div className="flex items-center gap-3 mt-2 flex-wrap">
                  <Badge label={t(`personas.${persona.id}.name`)} color={persona.color} size="md" />
                  <Badge label={t(`stages.${user.mind.stage}`)} color={persona.color} />
                  <Badge label={t(`families.${persona.family}`)} color={`${persona.color}80`} />
                </div>
                {user.bio && (
                  <p className="text-xs text-slate-500 mt-3 leading-relaxed font-body font-light max-w-xl">{user.bio}</p>
                )}
              </div>
            </div>

            {/* Stats row */}
            <div className="flex flex-wrap gap-6 text-sm">
              <StatChip icon={<TrendingUp size={13} />} label={t("profile.level")} value={`${user.level}`} color={beliefColors.reward.primary} />
              <StatChip icon={<Headphones size={13} />} label={t("profile.tracks")} value={user.tracksAnalyzed.toLocaleString()} color={beliefColors.consonance.primary} />
              <StatChip icon={<Flame size={13} />} label={t("profile.streak")} value={`${user.streak}d`} color={beliefColors.tempo.primary} />
              <StatChip icon={<Trophy size={13} />} label={t("profile.region")} value={user.country} color={beliefColors.salience.primary} />
              {listening && (
                <>
                  <StatChip icon={<Clock size={13} />} label={t("profile.totalHours")} value={listening.totalHours.toLocaleString()} color={beliefColors.familiarity.primary} />
                  <StatChip icon={<Music size={13} />} label={t("profile.compositions")} value={String(user.compositionsCreated || 0)} color={beliefColors.consonance.primary} />
                </>
              )}
            </div>
          </motion.div>

          {/* ── MAIN GRID ─────────────────────────────────────── */}
          <div className="grid grid-cols-12 gap-6 mb-12">
            {/* Left: Radar + Axes */}
            <motion.div variants={slideUp} className="col-span-12 lg:col-span-5 space-y-6">
              <div className="spatial-card p-8 flex flex-col items-center">
                <span className="hud-label mb-5">{t("profile.mindProfile")}</span>
                <MindRadar
                  axes={user.mind.axes}
                  color={persona.color}
                  compareAxes={myMind?.axes}
                  compareColor={myMind ? (myPersona?.color ?? beliefColors.consonance.primary) : undefined}
                  size={400}
                />
                {myMind && (
                  <div className="flex items-center gap-8 mt-5 text-xs">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full" style={{ backgroundColor: persona.color }} />
                      <span className="text-slate-600 font-body font-light">{user.displayName}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full" style={{ backgroundColor: myPersona?.color ?? beliefColors.consonance.primary }} />
                      <span className="text-slate-600 font-body font-light">{t("common.you")}</span>
                    </div>
                  </div>
                )}
              </div>

              {/* Axes bars */}
              <div className="spatial-card p-6">
                <span className="hud-label mb-4 block">{t("profile.axes")}</span>
                <div className="space-y-3">
                  {AXIS_LABELS.map(({ key, label, short, belief }) => {
                    const pct = Math.round(user.mind.axes[key] * 100);
                    const barColor = beliefColors[belief].primary;
                    return (
                      <div key={key}>
                        <div className="flex items-center justify-between mb-1">
                          <div className="flex items-center gap-2">
                            <NucleusDot color={barColor} size={3} active />
                            <span className="text-[10px] text-slate-600 font-body">{t(`axes.profileShort.${key}`)}</span>
                          </div>
                          <span className="hud-value text-[11px]" style={{ color: barColor }}>{pct}</span>
                        </div>
                        <div className="w-full h-[3px] rounded-full bg-white/5 overflow-hidden">
                          <motion.div className="h-full rounded-full" style={{ backgroundColor: barColor }}
                            initial={{ width: 0 }} animate={{ width: `${pct}%` }}
                            transition={{ duration: 1, ease: [0.22, 1, 0.36, 1] }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </motion.div>

            {/* Right: Compatibility + Listening + Tracks */}
            <motion.div variants={slideUp} className="col-span-12 lg:col-span-7 space-y-6">
              {/* Compatibility panel */}
              {compatibility !== null && compatLabel && (
                <div className="spatial-card p-6 glow-border" style={{ "--glow-color": compatLabel.color } as React.CSSProperties}>
                  <span className="hud-label mb-5 block">{t("profile.mindCompatibility")}</span>
                  <div className="flex items-start gap-6 mb-5">
                    <div className="text-center shrink-0">
                      <span className="text-4xl font-display font-bold" style={{ color: compatLabel.color }}>
                        {compatibility}%
                      </span>
                      <p className="text-[11px] mt-1 font-body font-light" style={{ color: compatLabel.color }}>
                        {t(`compatibility.${compatLabel.label.toLowerCase()}`)}
                      </p>
                    </div>
                    <div className="flex-1 space-y-2">
                      {AXIS_LABELS.map(({ key, label, belief }) => {
                        const diff = Math.abs(user.mind.axes[key] - (myMind?.axes[key] ?? 0));
                        const similarity = Math.round((1 - diff) * 100);
                        const barColor = beliefColors[belief].primary;
                        return (
                          <div key={key} className="flex items-center gap-2 text-xs">
                            <span className="w-14 text-slate-600 font-body font-light truncate">{t(`axes.profileShort.${key}`)}</span>
                            <div className="flex-1 h-[2px] rounded-full bg-white/5 overflow-hidden">
                              <motion.div className="h-full rounded-full" style={{ backgroundColor: barColor }}
                                initial={{ width: 0 }} animate={{ width: `${similarity}%` }}
                                transition={{ duration: 0.8 }}
                              />
                            </div>
                            <span className="hud-value text-[9px] w-6 text-right">{similarity}</span>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                  {/* Neural narrative */}
                  {compatNarrative && (
                    <div className="pt-4 border-t border-white/[0.04]">
                      <div className="flex items-start gap-2">
                        <Brain size={12} className="mt-0.5 shrink-0" style={{ color: `${compatLabel.color}60` }} />
                        <p className="text-[11px] text-slate-500 leading-relaxed font-body font-light">{compatNarrative}</p>
                      </div>
                    </div>
                  )}
                  {/* Connect button */}
                  <div className="mt-5 flex justify-end">
                    <Button variant="primary" size="sm" onClick={() => {
                      setChatOpen(true);
                      if (messages.length === 0) {
                        setMessages([{
                          from: "them",
                          text: `Hey! I noticed we have ${compatibility}% neural similarity. ${listening?.topGenres[0]?.name ? `I've been deep into ${listening.topGenres[0].name} this week` : "What are you listening to"} — what's been hitting your reward system lately?`,
                        }]);
                      }
                    }}>
                      <MessageCircle size={14} className="mr-2" />{t("profile.connectMinds")}
                    </Button>
                  </div>
                </div>
              )}

              {/* Listening Stats */}
              {listening && (
                <div className="spatial-card p-6">
                  <div className="flex items-center justify-between mb-5">
                    <span className="hud-label">{t("profile.thisWeekListening")}</span>
                    <span className="text-[10px] font-mono text-slate-700">
                      {listening.minutesThisWeek} min · {listening.tracksThisWeek} tracks
                    </span>
                  </div>

                  {/* Genre breakdown */}
                  <div className="space-y-2 mb-5">
                    {listening.topGenres.slice(0, 5).map((g) => (
                      <div key={g.name} className="flex items-center gap-3">
                        <span className="text-[10px] text-slate-500 font-body font-light w-24 truncate">{g.name}</span>
                        <div className="flex-1 h-[3px] rounded-full bg-white/5 overflow-hidden">
                          <motion.div className="h-full rounded-full"
                            style={{ backgroundColor: persona.color, opacity: 0.3 + (g.pct / 100) * 0.5 }}
                            initial={{ width: 0 }} animate={{ width: `${g.pct}%` }}
                            transition={{ duration: 0.8 }}
                          />
                        </div>
                        <span className="text-[9px] font-mono text-slate-600 w-8 text-right">{g.pct}%</span>
                      </div>
                    ))}
                  </div>

                  {/* Top artists */}
                  <div className="flex flex-wrap gap-2 mb-5">
                    {listening.topArtists.map((artist) => (
                      <span key={artist} className="text-[10px] font-mono px-2 py-0.5 rounded-full"
                        style={{ background: `${persona.color}08`, color: `${persona.color}80`, border: `1px solid ${persona.color}15` }}
                      >
                        {artist}
                      </span>
                    ))}
                  </div>

                  {/* Belief snapshot */}
                  <div className="pt-4 border-t border-white/[0.04]">
                    <span className="hud-label mb-3 block">{t("profile.currentMindState")}</span>
                    <div className="flex gap-3">
                      {BELIEF_NAMES.map((b, i) => {
                        const val = listening.beliefSnapshot[i];
                        const delta = listening.beliefDeltas[i];
                        const bColor = beliefColors[b].primary;
                        return (
                          <div key={b} className="flex-1 text-center">
                            <div className="h-12 flex items-end justify-center mb-1">
                              <motion.div
                                className="w-3 rounded-t-sm"
                                style={{ backgroundColor: bColor, opacity: 0.5 + val * 0.4 }}
                                initial={{ height: 0 }}
                                animate={{ height: `${val * 48}px` }}
                                transition={{ duration: 0.8, delay: i * 0.08 }}
                              />
                            </div>
                            <div className="text-[9px] font-mono" style={{ color: bColor }}>{val.toFixed(2)}</div>
                            <div className="text-[8px] font-mono" style={{ color: delta >= 0 ? "#84CC16" : "#EF4444" }}>
                              {delta >= 0 ? "+" : ""}{(delta * 100).toFixed(0)}%
                            </div>
                            <div className="text-[8px] font-mono text-slate-700">{t(`beliefs.short.${b}`)}</div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>
              )}

              {/* Recent Tracks */}
              {recentTracks && recentTracks.length > 0 && (
                <div className="spatial-card p-6">
                  <span className="hud-label mb-4 block">{t("profile.recentListening")}</span>
                  <div className="space-y-3">
                    {recentTracks.map((track, i) => (
                      <div key={i} className="flex items-start gap-3 py-2 border-b border-white/[0.03] last:border-0">
                        <div className="relative w-8 h-8 rounded-lg flex items-center justify-center overflow-hidden shrink-0 mt-0.5">
                          <MiniOrganism
                            color={track.rewardIntensity > 0.85 ? beliefColors.reward.primary : persona.color}
                            stage={1} size={32}
                          />
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2">
                            <h4 className="text-xs font-body font-medium text-slate-300 truncate">{track.title}</h4>
                            <span className="text-[9px] font-mono text-slate-700">{track.listenedAt}</span>
                          </div>
                          <p className="text-[10px] text-slate-600 font-body font-light">{track.artist} · {track.genre}</p>
                          {track.peakMoment && (
                            <p className="text-[9px] font-mono text-slate-700 mt-0.5">{t("profile.peak")}: {track.peakMoment}</p>
                          )}
                        </div>
                        <div className="shrink-0 w-7 h-7 rounded-full flex items-center justify-center"
                          style={{ background: `${beliefColors.reward.primary}${Math.round(track.rewardIntensity * 25).toString(16).padStart(2, '0')}` }}
                        >
                          <span className="text-[8px] font-mono" style={{ color: beliefColors.reward.primary }}>
                            {(track.rewardIntensity * 100).toFixed(0)}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </motion.div>
          </div>

          {/* ── PROGRESSION + ACHIEVEMENTS ─────────────────────── */}
          <div className="scroll-section grid grid-cols-1 lg:grid-cols-2 gap-6 mb-12">
            <div className="spatial-card p-6">
              <span className="hud-label mb-4 block">{t("profile.progression")}</span>
              <div className="flex items-center gap-5">
                <LevelBadge level={user.level} size="lg" />
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs text-slate-600 font-body font-light">{t("profile.experience")}</span>
                    <span className="hud-value text-xs text-slate-500">{user.xp.toLocaleString()} XP</span>
                  </div>
                  <div className="w-full h-[3px] rounded-full bg-white/5 overflow-hidden">
                    <motion.div className="h-full rounded-full" style={{ backgroundColor: beliefColors.reward.primary }}
                      initial={{ width: 0 }} animate={{ width: `${Math.min(100, (user.xp / 240000) * 100)}%` }}
                      transition={{ duration: 1.2, ease: [0.22, 1, 0.36, 1] }}
                    />
                  </div>
                </div>
              </div>
              {/* Extra stats */}
              <div className="grid grid-cols-3 gap-3 mt-5 pt-4 border-t border-white/[0.04]">
                <div className="text-center">
                  <span className="hud-value text-lg">{user.compositionsCreated || 0}</span>
                  <p className="text-[9px] font-mono text-slate-700">{t("profile.compositions")}</p>
                </div>
                <div className="text-center">
                  <span className="hud-value text-lg">{user.liveSessionsPlayed || 0}</span>
                  <p className="text-[9px] font-mono text-slate-700">{t("profile.liveSessions")}</p>
                </div>
                <div className="text-center">
                  <span className="hud-value text-lg">{listening?.totalHours.toLocaleString() ?? "—"}</span>
                  <p className="text-[9px] font-mono text-slate-700">{t("profile.hoursListened")}</p>
                </div>
              </div>
            </div>

            <div className="spatial-card p-6">
              <span className="hud-label mb-4 block">{t("profile.achievements")}</span>
              <div className="grid grid-cols-2 gap-2">
                {userAchievements.map((ach) => {
                  if (!ach) return null;
                  const rarityColor =
                    ach.rarity === "legendary" ? beliefColors.reward.primary :
                    ach.rarity === "epic" ? beliefColors.consonance.primary :
                    ach.rarity === "rare" ? beliefColors.familiarity.primary : "#94A3B8";
                  return (
                    <div key={ach.id} className="p-2.5 rounded-xl flex items-center gap-2.5"
                      style={{ background: "rgba(0,0,0,0.5)", border: "1px solid rgba(255,255,255,0.06)" }}
                    >
                      <div className="w-7 h-7 rounded-lg flex items-center justify-center text-[10px] font-bold shrink-0"
                        style={{ background: `${rarityColor}12`, color: rarityColor, border: `1px solid ${rarityColor}20` }}
                      >
                        {ach.name.charAt(0)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="text-[11px] font-body font-medium text-slate-300 truncate">{ach.name}</div>
                        <div className="text-[9px] text-slate-600 truncate font-body font-light">{ach.description}</div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* ── PERSONA DESCRIPTION ────────────────────────────── */}
          <div className="scroll-section mb-12">
            <div className="spatial-card p-8 text-center">
              <Brain size={18} className="mx-auto mb-4" style={{ color: `${persona.color}40` }} />
              <p className="text-sm text-slate-400 font-display font-light italic max-w-2xl mx-auto leading-relaxed">
                "{t(`personas.${persona.id}.description`)}"
              </p>
              <div className="flex items-center justify-center gap-3 mt-5">
                {persona.strengths.map((s, i) => (
                  <span key={s} className="text-[9px] font-mono px-2 py-0.5 rounded-full"
                    style={{ background: `${persona.color}08`, color: `${persona.color}60`, border: `1px solid ${persona.color}15` }}
                  >
                    {t(`personas.${persona.id}.strengths.${i}`)}
                  </span>
                ))}
              </div>
              <div className="flex items-center justify-center gap-2 mt-4 text-[10px] text-slate-700 font-mono">
                <span>{persona.populationPct}% {t("common.ofAllMinds")}</span>
                <span>·</span>
                <span>{t("common.famous")}: {persona.famousMinds.join(", ")}</span>
              </div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* ── CHAT MODAL ──────────────────────────────────────── */}
      <AnimatePresence>
        {chatOpen && (
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/70 backdrop-blur-sm p-4"
            onClick={() => setChatOpen(false)}
          >
            <motion.div
              initial={{ y: 100, opacity: 0 }} animate={{ y: 0, opacity: 1 }} exit={{ y: 100, opacity: 0 }}
              transition={{ type: "spring", damping: 25 }}
              className="w-full max-w-lg rounded-2xl overflow-hidden"
              style={{ background: "rgba(10,10,15,0.95)", border: "1px solid rgba(255,255,255,0.06)", backdropFilter: "blur(24px)" }}
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between p-5 border-b border-white/[0.04]">
                <div className="flex items-center gap-3">
                  <NucleusDot color={persona.color} size={5} active pulsing />
                  <div>
                    <h3 className="text-sm font-display font-medium text-slate-300">
                      {t("profile.mindLink", { name: user.displayName })}
                    </h3>
                    <p className="text-[10px] font-mono text-slate-600">
                      {t("profile.neuralSimilarity", { pct: compatibility })} · {t(`personas.${persona.id}.name`)}
                    </p>
                  </div>
                </div>
                <button onClick={() => setChatOpen(false)} className="text-slate-600 hover:text-slate-400 transition-colors">
                  <X size={18} />
                </button>
              </div>

              <div className="p-5 h-80 overflow-y-auto space-y-4">
                <div className="text-center mb-4">
                  <p className="text-[10px] font-mono text-slate-700">{t("profile.mindsConnected")}</p>
                </div>
                {messages.map((msg, i) => (
                  <div key={i} className={`flex gap-3 ${msg.from === "you" ? "flex-row-reverse" : ""}`}>
                    {msg.from === "them" ? (
                      <Avatar src={user.avatarUrl || undefined} name={user.displayName} size={28} borderColor={persona.color} />
                    ) : (
                      <div className="w-7 h-7 rounded-full flex items-center justify-center shrink-0"
                        style={{ background: `${myPersona?.color ?? "#6366F1"}20`, border: `1px solid ${myPersona?.color ?? "#6366F1"}30` }}
                      >
                        <span className="text-[9px] font-bold" style={{ color: myPersona?.color ?? "#6366F1" }}>Y</span>
                      </div>
                    )}
                    <div className={`flex-1 ${msg.from === "you" ? "flex justify-end" : ""}`}>
                      <div className="rounded-xl p-3 max-w-[80%] inline-block"
                        style={msg.from === "them"
                          ? { background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.04)" }
                          : { background: `${myPersona?.color ?? "#6366F1"}12`, border: `1px solid ${myPersona?.color ?? "#6366F1"}20` }
                        }
                      >
                        <p className="text-xs text-slate-400 font-body font-light">{msg.text}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="p-4 border-t border-white/[0.04]">
                <form onSubmit={(e) => {
                  e.preventDefault();
                  const input = e.currentTarget.querySelector("input");
                  if (input) { handleSendMessage(input.value); input.value = ""; }
                }} className="flex gap-3">
                  <input type="text" placeholder={t("profile.shareMind")}
                    className="flex-1 px-4 py-2.5 rounded-xl text-sm text-slate-300 placeholder-slate-700 font-body font-light focus:outline-none"
                    style={{ background: "rgba(0,0,0,0.5)", border: "1px solid rgba(255,255,255,0.06)" }}
                  />
                  <Button variant="primary" size="sm">{t("common.send")}</Button>
                </form>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

function StatChip({ icon, label, value, color }: { icon: React.ReactNode; label: string; value: string; color: string }) {
  return (
    <div className="flex flex-col gap-0.5">
      <div className="flex items-center gap-1.5">
        <span style={{ color }} className="opacity-60">{icon}</span>
        <span className="hud-label">{label}</span>
      </div>
      <span className="hud-value text-sm text-slate-300">{value}</span>
    </div>
  );
}
