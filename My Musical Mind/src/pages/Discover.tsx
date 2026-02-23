import { useState, useCallback, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { motion, AnimatePresence } from "framer-motion";
import {
  Upload, Search, Sparkles, ChevronDown, ChevronUp, Radio,
  Brain, Clock, Music, Headphones, TrendingUp, Zap,
} from "lucide-react";
import { useUserStore } from "@/stores/useUserStore";
import { getPersona } from "@/data/personas";
import { generateTrace } from "@/data/mock-traces";
import { recommendedTracks, topPerformances, friendActivity } from "@/data/mock-tracks";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Avatar } from "@/components/ui/Avatar";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { OrganismLoader } from "@/components/mind/OrganismLoader";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { MiniOrganism } from "@/components/mind/MiniOrganism";
import { mockUsers } from "@/data/mock-users";
import { pageTransition, staggerChildren, slideUp, scaleIn, fadeIn } from "@/design/animations";
import { beliefColors } from "@/design/tokens";
import type { BeliefTrace } from "@/types/mind";

type LabState = "idle" | "analyzing" | "done";

const BELIEF_KEYS = ["consonance", "tempo", "salience", "familiarity", "reward"] as const;
const BELIEF_LABELS: Record<string, string> = {
  consonance: "Harmony", tempo: "Rhythm", salience: "Attention", familiarity: "Memory", reward: "Pleasure",
};
const BELIEF_I18N_KEY: Record<string, string> = {
  consonance: "dashboard.beliefs.harmony",
  tempo: "dashboard.beliefs.rhythm",
  salience: "dashboard.beliefs.attention",
  familiarity: "dashboard.beliefs.memory",
  reward: "dashboard.beliefs.pleasure",
};

/* ── Analysis pipeline phases — what's happening under the hood ── */
const ANALYSIS_PHASES = [
  { threshold: 5,  key: "discover.phases.p1", icon: "ear" },
  { threshold: 15, key: "discover.phases.p2", icon: "eye" },
  { threshold: 25, key: "discover.phases.p3", icon: "wave" },
  { threshold: 35, key: "discover.phases.p4", icon: "clock" },
  { threshold: 50, key: "discover.phases.p5", icon: "chart" },
  { threshold: 60, key: "discover.phases.p6", icon: "brain" },
  { threshold: 70, key: "discover.phases.p7", icon: "zap" },
  { threshold: 80, key: "discover.phases.p8", icon: "target" },
  { threshold: 90, key: "discover.phases.p9", icon: "star" },
  { threshold: 97, key: "discover.phases.p10", icon: "layers" },
];

/* ── Neuroscience context for analysis results ─────────────────── */
function generateAnalysisNarrative(
  traces: BeliefTrace[],
  personaName: string,
  style: string,
  t: (key: string, opts?: Record<string, unknown>) => string,
): { summary: string; beliefs: { key: string; narrative: string; avgValue: number }[]; peakMoment: string; brainRegions: string[] } {
  const avg = (key: keyof BeliefTrace) => traces.reduce((s, t) => s + (t[key] as number), 0) / traces.length;
  const avgC = avg("consonance");
  const avgT = avg("tempo");
  const avgS = avg("salience");
  const avgF = avg("familiarity");
  const avgR = avg("reward");

  // Find peak reward moment
  let peakIdx = 0;
  for (let i = 1; i < traces.length; i++) {
    if (traces[i].reward > traces[peakIdx].reward) peakIdx = i;
  }
  const peakTime = traces[peakIdx].time;
  const peakR = traces[peakIdx].reward;

  const beliefs = [
    {
      key: "consonance",
      avgValue: avgC,
      narrative: avgC > 0.65
        ? t("discover.narratives.consonanceHigh")
        : avgC > 0.45
        ? t("discover.narratives.consonanceMid")
        : t("discover.narratives.consonanceLow"),
    },
    {
      key: "tempo",
      avgValue: avgT,
      narrative: avgT > 0.6
        ? t("discover.narratives.tempoHigh")
        : avgT > 0.4
        ? t("discover.narratives.tempoMid")
        : t("discover.narratives.tempoLow"),
    },
    {
      key: "salience",
      avgValue: avgS,
      narrative: avgS > 0.55
        ? t("discover.narratives.salienceHigh")
        : avgS > 0.35
        ? t("discover.narratives.salienceMid")
        : t("discover.narratives.salienceLow"),
    },
    {
      key: "familiarity",
      avgValue: avgF,
      narrative: avgF > 0.6
        ? t("discover.narratives.familiarityHigh")
        : avgF > 0.35
        ? t("discover.narratives.familiarityMid")
        : t("discover.narratives.familiarityLow"),
    },
    {
      key: "reward",
      avgValue: avgR,
      narrative: avgR > 0.06
        ? t("discover.narratives.rewardHigh", { value: (avgR * 100).toFixed(1) })
        : avgR > 0.02
        ? t("discover.narratives.rewardMid", { value: (avgR * 100).toFixed(1) })
        : t("discover.narratives.rewardLow", { value: (avgR * 100).toFixed(1) }),
    },
  ];

  const brainRegions = [
    t("discover.brainRegions.hearing"),
    t("discover.brainRegions.harmony"),
    t("discover.brainRegions.rhythm"),
    t("discover.brainRegions.pleasure"),
    t("discover.brainRegions.memory"),
    t("discover.brainRegions.attention"),
  ];

  const summary = `Your ${personaName} mind processed this ${style} track across 97 perceptual dimensions and ${traces.length} moments in time. `
    + `Peak pleasure occurred at ${formatTime(peakTime)} (${(peakR * 100).toFixed(1)}% intensity) — `
    + `that's the moment where what you expected was most beautifully violated and then resolved.`;

  return {
    summary,
    beliefs,
    peakMoment: `${formatTime(peakTime)} — reward intensity ${(peakR * 100).toFixed(1)}%`,
    brainRegions,
  };
}

function findPeakReward(traces: BeliefTrace[]): { time: number; value: number } {
  let best = traces[0];
  for (const t of traces) { if (t.reward > best.reward) best = t; }
  return { time: best.time, value: best.reward };
}

function formatTime(sec: number): string {
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

export function Discover() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const { mind } = useUserStore();
  const persona = mind ? getPersona(mind.personaId) : null;
  const accentColor = persona?.color ?? beliefColors.consonance.primary;

  const [analyzeOpen, setAnalyzeOpen] = useState(false);
  const [trackUrl, setTrackUrl] = useState("");
  const [labState, setLabState] = useState<LabState>("idle");
  const [progress, setProgress] = useState(0);
  const [traces, setTraces] = useState<BeliefTrace[]>([]);
  const [analysisStyle, setAnalysisStyle] = useState<string>("balanced");
  const [selectedTrack, setSelectedTrack] = useState<string | null>(null);

  const handleAnalyze = useCallback((trackTitle?: string) => {
    setLabState("analyzing");
    setProgress(0);
    if (trackTitle) setSelectedTrack(trackTitle);

    const style = persona
      ? persona.axes.entropyTolerance > 0.7 ? "chaotic"
      : persona.axes.tensionAppetite > 0.7 ? "dramatic"
      : persona.axes.monotonyTolerance > 0.6 ? "calm" : "balanced"
      : "balanced";
    setAnalysisStyle(style);

    const interval = setInterval(() => {
      setProgress((prev) => {
        const next = prev + Math.random() * 6 + 1.5;
        if (next >= 100) {
          clearInterval(interval);
          setTraces(generateTrace(182, style as "calm" | "dramatic" | "chaotic" | "balanced"));
          setTimeout(() => setLabState("done"), 300);
          return 100;
        }
        return next;
      });
    }, 200);
  }, [persona]);

  const peakReward = useMemo(() => traces.length > 0 ? findPeakReward(traces) : null, [traces]);

  const analysisNarrative = useMemo(
    () => traces.length > 0 ? generateAnalysisNarrative(traces, persona?.name ?? "Unknown", analysisStyle, t) : null,
    [traces, persona, analysisStyle, t],
  );

  // Current analysis phase text
  const currentPhase = useMemo(
    () => ANALYSIS_PHASES.filter(p => progress >= p.threshold).pop(),
    [progress],
  );

  return (
    <motion.div {...pageTransition} className="min-h-screen bg-black relative overflow-hidden pb-16">
      <div className="cinematic-vignette" />

      <div className="absolute inset-0 z-0 opacity-[0.08] pointer-events-none">
        <MindOrganismCanvas color={accentColor} secondaryColor={beliefColors.familiarity.primary} stage={1} intensity={0.2} breathRate={6} variant="ambient" className="w-full h-full" interactive={false} />
      </div>

      {/* Header */}
      <motion.div variants={fadeIn} initial="initial" animate="animate" className="relative z-10 text-center mb-12 pt-8">
        <span className="hud-label mb-3 block">{t("discover.hudLabel")}</span>
        <h1 className="text-4xl md:text-5xl font-display font-bold text-slate-100 tracking-tight mb-3">{t("discover.title")}</h1>
        <p className="hud-label text-xs">{t("discover.subtitle")}</p>
      </motion.div>

      <motion.div variants={staggerChildren} initial="initial" animate="animate" className="relative z-10 max-w-5xl xl:max-w-6xl 2xl:max-w-7xl mx-auto px-4">

        {/* ── Your Mind Would Love — enriched cards ─────────────── */}
        <motion.div variants={slideUp} className="mb-12">
          <div className="flex items-center gap-2 mb-5">
            <Brain size={14} style={{ color: accentColor }} />
            <span className="hud-label">{t("discover.yourMindWouldLove")}</span>
            {persona && (
              <span className="text-[9px] font-mono text-slate-700 ml-auto">
                {t("discover.curatedFor", { name: persona.name })}
              </span>
            )}
          </div>
          <div className="flex gap-4 overflow-x-auto pb-2 scrollbar-hide">
            {recommendedTracks.map((track) => {
              const trackBeliefColor = track.peakBelief ? beliefColors[track.peakBelief].primary : accentColor;
              return (
                <div
                  key={track.id}
                  className="flex-shrink-0 w-60 spatial-card p-5 group cursor-pointer hover:bg-white/[0.02] transition-colors"
                  onClick={() => { setAnalyzeOpen(true); handleAnalyze(track.title); }}
                >
                  <div className="w-full aspect-square rounded-xl mb-3 overflow-hidden relative flex items-center justify-center"
                    style={{ background: `${trackBeliefColor}08`, border: `1px solid ${trackBeliefColor}10` }}
                  >
                    <MiniOrganism color={trackBeliefColor} stage={1} size={80} />
                    {track.peakBelief && (
                      <div className="absolute bottom-2 right-2">
                        <NucleusDot color={trackBeliefColor} size={4} active pulsing />
                      </div>
                    )}
                  </div>
                  <h4 className="text-sm font-body font-medium text-slate-300 truncate group-hover:text-slate-100 transition-colors">
                    {track.title}
                  </h4>
                  <p className="text-[11px] text-slate-600 font-body font-light truncate">{track.artist}</p>
                  <div className="flex items-center justify-between mt-2">
                    <span className="text-[9px] text-slate-700 font-mono">
                      {track.bpm && `${track.bpm}bpm`}{track.key && ` · ${track.key}`}
                    </span>
                    <Badge label={`${track.match}%`} color={accentColor} />
                  </div>
                  {/* PE reason */}
                  {track.peReason && (
                    <p className="text-[9px] text-slate-700 font-mono mt-2 leading-relaxed line-clamp-2">
                      {track.peReason}
                    </p>
                  )}
                  {/* Peak moment */}
                  {track.peakMoment && (
                    <div className="flex items-center gap-1 mt-1.5">
                      <Zap size={8} style={{ color: trackBeliefColor }} />
                      <span className="text-[8px] font-mono" style={{ color: `${trackBeliefColor}80` }}>
                        {track.peakMoment}
                      </span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </motion.div>

        {/* ── Top Performances — enriched ────────────────────────── */}
        <motion.div variants={slideUp} className="mb-12">
          <div className="flex items-center gap-2 mb-5">
            <Headphones size={14} className="text-slate-600" />
            <span className="hud-label">{t("discover.topPerformances")}</span>
            <span className="text-[9px] font-mono text-slate-700 ml-auto">{t("discover.community")}</span>
          </div>
          <div className="spatial-card p-6 space-y-1">
            {topPerformances.map((track, i) => {
              const bColor = track.peakBelief ? beliefColors[track.peakBelief].primary : beliefColors.consonance.primary;
              return (
                <div
                  key={track.id}
                  className="flex items-center gap-4 py-3 px-3 rounded-xl hover:bg-white/[0.02] transition-colors cursor-pointer group"
                  onClick={() => { setAnalyzeOpen(true); handleAnalyze(track.title); }}
                >
                  {/* Rank */}
                  <span className="text-[10px] font-mono text-slate-700 w-5 text-center">
                    {i + 1}
                  </span>

                  <div className="relative w-10 h-10 rounded-lg flex items-center justify-center overflow-hidden">
                    <MiniOrganism color={track.isLive ? "#EF4444" : bColor} stage={1} size={40} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      {track.isLive && (
                        <span className="flex items-center gap-1 text-[9px] font-mono text-red-400">
                          <Radio size={10} className="animate-pulse" /> {t("discover.live")}
                        </span>
                      )}
                      <h4 className="text-sm font-body font-medium text-slate-300 truncate group-hover:text-slate-100 transition-colors">{track.title}</h4>
                    </div>
                    <div className="flex items-center gap-2">
                      <p className="text-[11px] text-slate-600 font-body font-light">{track.artist}</p>
                      {track.bpm && <span className="text-[9px] font-mono text-slate-700">{track.bpm}bpm</span>}
                      {track.key && <span className="text-[9px] font-mono text-slate-700">{track.key}</span>}
                    </div>
                    {/* Peak moment */}
                    {track.peakMoment && (
                      <p className="text-[9px] font-mono mt-0.5" style={{ color: `${bColor}60` }}>
                        {t("discover.peakLabel")} {track.peakMoment}
                      </p>
                    )}
                  </div>
                  <div className="flex items-center gap-3 shrink-0">
                    {track.peakBelief && <NucleusDot color={bColor} size={3} active />}
                    <span className="text-[10px] font-mono text-slate-700">{t("discover.plays", { num: track.plays?.toLocaleString() ?? "0" })}</span>
                    <span className="text-[9px] font-mono text-slate-700">{track.duration}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </motion.div>

        {/* ── Friends Are Listening — enriched with avatars ──────── */}
        <motion.div variants={slideUp} className="mb-12">
          <div className="flex items-center gap-2 mb-5">
            <Music size={14} className="text-slate-600" />
            <span className="hud-label">{t("discover.friendsListening")}</span>
          </div>
          <div className="spatial-card p-6 space-y-2">
            {friendActivity.map((fa) => {
              const user = mockUsers.find(u => u.id === fa.userId);
              const userPersona = user ? getPersona(user.mind.personaId) : null;
              const dotColor = fa.action === "performing" ? "#EF4444"
                : fa.action === "composed" ? beliefColors.consonance.primary
                : beliefColors.familiarity.primary;
              return (
                <div
                  key={fa.id}
                  className="flex items-center gap-3 py-2.5 cursor-pointer hover:bg-white/[0.02] transition-colors rounded-xl px-3"
                  onClick={() => navigate(`/friends/${fa.userId}`)}
                >
                  {/* Avatar instead of just a dot */}
                  <div className="relative shrink-0">
                    <Avatar
                      src={user?.avatarUrl || undefined}
                      name={fa.userName}
                      size={32}
                      borderColor={userPersona?.color}
                    />
                    {fa.action === "performing" && (
                      <div className="absolute -top-0.5 -right-0.5 w-3 h-3 rounded-full bg-red-500 border border-black animate-pulse" />
                    )}
                  </div>
                  <div className="flex-1 text-sm">
                    <span className="text-slate-300 font-body font-medium">{fa.userName}</span>
                    <span className="text-slate-600 font-body font-light ml-1">
                      {fa.action === "performing" ? t("discover.friendActions.performing") : fa.action === "composed" ? t("discover.friendActions.composed") : t("discover.friendActions.listening")}
                    </span>
                    <span className="text-slate-400 font-body font-medium ml-1">"{fa.trackTitle}"</span>
                  </div>
                  <NucleusDot color={dotColor} size={4} active pulsing={fa.action === "performing"} />
                  <span className="text-[10px] font-mono text-slate-700">{fa.timeAgo}</span>
                </div>
              );
            })}
          </div>
        </motion.div>

        {/* ── Analyze a Track (collapsible) — deep pipeline ──────── */}
        <motion.div variants={slideUp}>
          <button onClick={() => setAnalyzeOpen(!analyzeOpen)} className="w-full flex items-center justify-between py-3 mb-4">
            <div className="flex items-center gap-2">
              <TrendingUp size={14} className="text-slate-600" />
              <span className="hud-label">{t("discover.analyzeTrack")}</span>
            </div>
            {analyzeOpen ? <ChevronUp size={14} className="text-slate-600" /> : <ChevronDown size={14} className="text-slate-600" />}
          </button>

          <AnimatePresence>
            {analyzeOpen && (
              <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.3 }}>
                <div className="spatial-card p-6 mb-6">
                  <div className="flex flex-col sm:flex-row gap-4">
                    <div className="flex-1 relative">
                      <Search size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-700" />
                      <input type="text" placeholder={t("discover.searchPlaceholder")} value={trackUrl} onChange={(e) => setTrackUrl(e.target.value)} className="w-full pl-11 pr-4 py-3 rounded-xl text-slate-300 placeholder-slate-700 focus:outline-none transition-colors text-sm font-body font-light" style={{ background: "rgba(0,0,0,0.5)", border: "1px solid rgba(255,255,255,0.06)" }} />
                    </div>
                    <div className="flex gap-3">
                      <Button variant="glass" size="md"><Upload size={14} className="mr-2" />{t("discover.upload")}</Button>
                      <Button variant="primary" size="md" onClick={() => handleAnalyze()} disabled={labState === "analyzing"}>
                        <Sparkles size={14} className="mr-2" />{t("discover.analyze")}
                      </Button>
                    </div>
                  </div>
                  {selectedTrack && labState !== "idle" && (
                    <p className="text-[10px] font-mono text-slate-600 mt-3">
                      {t("discover.analyzing")} <span className="text-slate-400">{selectedTrack}</span>
                    </p>
                  )}
                </div>

                <AnimatePresence mode="wait">
                  {labState === "idle" && (
                    <motion.div key="idle" {...scaleIn} exit={{ opacity: 0 }}>
                      <div className="spatial-card min-h-[250px] flex flex-col items-center justify-center text-center p-10">
                        <MiniOrganism color={accentColor} stage={1} size={60} />
                        <h3 className="text-base font-display font-medium text-slate-400 mt-6 mb-2">{t("discover.dropTrack")}</h3>
                        <p className="text-xs text-slate-600 max-w-md font-body font-light">
                          {t("discover.dropTrackDesc")}
                        </p>
                      </div>
                    </motion.div>
                  )}

                  {labState === "analyzing" && (
                    <motion.div key="analyzing" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                      <div className="spatial-card min-h-[300px] flex flex-col items-center justify-center p-10">
                        <OrganismLoader progress={progress} color={accentColor} size={60} className="mb-6" />

                        {/* Real pipeline phase indicator */}
                        <div className="w-full max-w-md space-y-2 mb-4">
                          {ANALYSIS_PHASES.map((phase) => {
                            const active = progress >= phase.threshold;
                            const current = currentPhase === phase;
                            return (
                              <motion.div
                                key={phase.threshold}
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: active ? 1 : 0.2, x: 0 }}
                                transition={{ duration: 0.3 }}
                                className="flex items-center gap-2"
                              >
                                <div className={`w-1.5 h-1.5 rounded-full shrink-0 ${current ? "animate-pulse" : ""}`}
                                  style={{ backgroundColor: active ? accentColor : "#334155" }}
                                />
                                <span className={`text-[10px] font-mono ${active ? "text-slate-500" : "text-slate-800"} ${current ? "text-slate-300" : ""}`}>
                                  {t(phase.key)}
                                </span>
                                {active && !current && (
                                  <span className="text-[8px] font-mono text-green-800 ml-auto">{t("discover.done")}</span>
                                )}
                              </motion.div>
                            );
                          })}
                        </div>

                        {/* Active belief dots */}
                        <div className="flex items-center gap-3 mt-2">
                          {BELIEF_KEYS.map((b) => (
                            <motion.div
                              key={b}
                              animate={{ opacity: progress > 60 ? 0.8 : 0.2, scale: progress > 60 ? 1 : 0.8 }}
                              className="flex items-center gap-1"
                            >
                              <NucleusDot color={beliefColors[b].primary} size={3} active={progress > 60} pulsing={progress > 70 && progress < 95} />
                              <span className="text-[8px] font-mono" style={{ color: `${beliefColors[b].primary}60` }}>
                                {b.slice(0, 4)}
                              </span>
                            </motion.div>
                          ))}
                        </div>
                      </div>
                    </motion.div>
                  )}

                  {labState === "done" && traces.length > 0 && (
                    <motion.div key="done" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="space-y-6">

                      {/* Neural Summary */}
                      {analysisNarrative && (
                        <div className="spatial-card p-6 glow-border" style={{ "--glow-color": accentColor } as React.CSSProperties}>
                          <div className="flex items-center gap-2 mb-4">
                            <Brain size={14} style={{ color: accentColor }} />
                            <span className="hud-label">{t("discover.whatYourMindHeard")}</span>
                            {selectedTrack && (
                              <span className="text-[10px] font-mono text-slate-600 ml-auto">{selectedTrack}</span>
                            )}
                          </div>
                          <p className="text-xs text-slate-400 leading-relaxed font-body font-light mb-4">
                            {analysisNarrative.summary}
                          </p>
                          <div className="flex flex-wrap gap-2">
                            {analysisNarrative.brainRegions.map((region) => (
                              <span key={region} className="text-[9px] font-mono px-2 py-1 rounded-full"
                                style={{ background: `${accentColor}08`, color: `${accentColor}60`, border: `1px solid ${accentColor}15` }}
                              >
                                {region}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Belief Traces */}
                      <div className="spatial-card p-8">
                        <span className="hud-label mb-6 block">{t("discover.howYourMindResponded", { count: traces.length })}</span>
                        <div className="space-y-6">
                          {BELIEF_KEYS.map((belief) => {
                            const bColor = beliefColors[belief].primary;
                            const values = traces.map((t) => t[belief]);
                            const narrative = analysisNarrative?.beliefs.find(b => b.key === belief);
                            return (
                              <div key={belief}>
                                <div className="flex items-center justify-between mb-2">
                                  <div className="flex items-center gap-2">
                                    <NucleusDot color={bColor} size={4} active pulsing />
                                    <span className="text-xs font-body font-medium text-slate-400">{t(BELIEF_I18N_KEY[belief])}</span>
                                  </div>
                                  <div className="flex items-center gap-4 text-[10px]">
                                    <span className="text-slate-700 font-mono">
                                      min: <span className="hud-value">{Math.min(...values).toFixed(2)}</span>
                                    </span>
                                    <span className="text-slate-700 font-mono">
                                      avg: <span className="hud-value">{(values.reduce((a, b) => a + b, 0) / values.length).toFixed(2)}</span>
                                    </span>
                                    <span className="text-slate-700 font-mono">
                                      max: <span className="hud-value">{Math.max(...values).toFixed(2)}</span>
                                    </span>
                                  </div>
                                </div>

                                {/* Trace bars */}
                                <div className="flex items-end gap-[1px] h-14 px-1 mb-2">
                                  {traces.filter((_, i) => i % 2 === 0).map((t, i) => {
                                    const nv = belief === "reward" ? (t[belief] + 0.5) / 1.0 : t[belief];
                                    return (
                                      <motion.div key={i} initial={{ height: 0 }} animate={{ height: Math.max(2, nv * 56) }} transition={{ duration: 0.3, delay: i * 0.003 }} className="flex-1 rounded-sm" style={{ backgroundColor: bColor, opacity: 0.2 + nv * 0.5, minWidth: 1 }} />
                                    );
                                  })}
                                </div>

                                {/* Per-belief narrative */}
                                {narrative && (
                                  <p className="text-[10px] text-slate-600 font-body font-light leading-relaxed pl-3"
                                    style={{ borderLeft: `2px solid ${bColor}20` }}
                                  >
                                    {narrative.narrative}
                                  </p>
                                )}
                              </div>
                            );
                          })}
                        </div>

                        {/* Timeline axis */}
                        <div className="flex justify-between mt-4 text-[8px] font-mono text-slate-700 px-1">
                          <span>0:00</span>
                          <span>{formatTime(traces[Math.floor(traces.length / 4)]?.time ?? 0)}</span>
                          <span>{formatTime(traces[Math.floor(traces.length / 2)]?.time ?? 0)}</span>
                          <span>{formatTime(traces[Math.floor(traces.length * 3 / 4)]?.time ?? 0)}</span>
                          <span>{formatTime(traces[traces.length - 1]?.time ?? 0)}</span>
                        </div>
                      </div>

                      {/* Peak Reward Moment */}
                      {peakReward && (
                        <div className="spatial-card p-6 glow-border" style={{ "--glow-color": beliefColors.reward.primary } as React.CSSProperties}>
                          <div className="flex items-center gap-3">
                            <Sparkles size={16} style={{ color: beliefColors.reward.primary }} />
                            <div className="flex-1">
                              <h3 className="text-sm font-body font-medium text-slate-300">
                                {t("discover.peakPleasure", { time: formatTime(peakReward.time) })}
                              </h3>
                              <p className="text-[10px] text-slate-600 font-mono">
                                {t("discover.peakIntensityDesc", { value: (peakReward.value * 100).toFixed(1) })}
                              </p>
                            </div>
                            <div className="shrink-0 w-12 h-12 rounded-full flex items-center justify-center"
                              style={{ background: `${beliefColors.reward.primary}15`, border: `1px solid ${beliefColors.reward.primary}30` }}
                            >
                              <span className="text-sm font-mono font-bold" style={{ color: beliefColors.reward.primary }}>
                                {(peakReward.value * 100).toFixed(0)}
                              </span>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* Analyze another */}
                      <div className="text-center pt-2">
                        <Button variant="glass" size="sm" onClick={() => { setLabState("idle"); setTraces([]); setSelectedTrack(null); }}>
                          {t("discover.analyzeAnother")}
                        </Button>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </motion.div>
    </motion.div>
  );
}
