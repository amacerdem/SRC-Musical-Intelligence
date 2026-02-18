import { useState, useCallback, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, Search, Sparkles, ChevronDown, ChevronUp, Radio } from "lucide-react";
import { useUserStore } from "@/stores/useUserStore";
import { getPersona } from "@/data/personas";
import { generateTrace } from "@/data/mock-traces";
import { recommendedTracks, topPerformances, friendActivity } from "@/data/mock-tracks";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { OrganismLoader } from "@/components/mind/OrganismLoader";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { MiniOrganism } from "@/components/mind/MiniOrganism";
import { pageTransition, staggerChildren, slideUp, scaleIn, fadeIn } from "@/design/animations";
import { beliefColors } from "@/design/tokens";
import type { BeliefTrace } from "@/types/mind";

type LabState = "idle" | "analyzing" | "done";

const BELIEF_KEYS = ["consonance", "tempo", "salience", "familiarity", "reward"] as const;
const BELIEF_LABELS: Record<string, string> = {
  consonance: "Consonance", tempo: "Tempo State", salience: "Salience", familiarity: "Familiarity", reward: "Reward",
};

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
  const { mind } = useUserStore();
  const persona = mind ? getPersona(mind.personaId) : null;
  const accentColor = persona?.color ?? beliefColors.consonance.primary;

  const [analyzeOpen, setAnalyzeOpen] = useState(false);
  const [trackUrl, setTrackUrl] = useState("");
  const [labState, setLabState] = useState<LabState>("idle");
  const [progress, setProgress] = useState(0);
  const [traces, setTraces] = useState<BeliefTrace[]>([]);

  const handleAnalyze = useCallback(() => {
    setLabState("analyzing");
    setProgress(0);
    const interval = setInterval(() => {
      setProgress((prev) => {
        const next = prev + Math.random() * 8 + 2;
        if (next >= 100) {
          clearInterval(interval);
          const style = persona
            ? persona.axes.entropyTolerance > 0.7 ? "chaotic"
            : persona.axes.tensionAppetite > 0.7 ? "dramatic"
            : persona.axes.monotonyTolerance > 0.6 ? "calm" : "balanced"
            : "balanced";
          setTraces(generateTrace(182, style as "calm" | "dramatic" | "chaotic" | "balanced"));
          setTimeout(() => setLabState("done"), 300);
          return 100;
        }
        return next;
      });
    }, 150);
  }, [persona]);

  const peakReward = useMemo(() => traces.length > 0 ? findPeakReward(traces) : null, [traces]);

  return (
    <motion.div {...pageTransition} className="min-h-screen bg-black relative overflow-hidden pb-16">
      <div className="cinematic-vignette" />

      <div className="absolute inset-0 z-0 opacity-[0.08] pointer-events-none">
        <MindOrganismCanvas color={accentColor} secondaryColor={beliefColors.familiarity.primary} stage={1} intensity={0.2} breathRate={6} variant="ambient" className="w-full h-full" interactive={false} />
      </div>

      {/* Header */}
      <motion.div variants={fadeIn} initial="initial" animate="animate" className="relative z-10 text-center mb-12 pt-8">
        <span className="hud-label mb-3 block">Discovery</span>
        <h1 className="text-4xl md:text-5xl font-display font-bold text-slate-100 tracking-tight mb-3">Discover</h1>
        <p className="hud-label text-xs">Music your mind would love</p>
      </motion.div>

      <motion.div variants={staggerChildren} initial="initial" animate="animate" className="relative z-10 max-w-5xl xl:max-w-6xl 2xl:max-w-7xl mx-auto px-4">

        {/* ── Your Mind Would Love ─────────────────────────── */}
        <motion.div variants={slideUp} className="mb-12">
          <span className="hud-label mb-5 block">Your Mind Would Love</span>
          <div className="flex gap-4 overflow-x-auto pb-2 scrollbar-hide">
            {recommendedTracks.map((track) => (
              <div key={track.id} className="flex-shrink-0 w-52 spatial-card p-5 group cursor-pointer">
                <div className="w-full aspect-square rounded-xl mb-3 overflow-hidden relative flex items-center justify-center" style={{ background: `${accentColor}08`, border: `1px solid ${accentColor}10` }}>
                  <MiniOrganism color={accentColor} stage={1} size={80} />
                </div>
                <h4 className="text-sm font-body font-medium text-slate-300 truncate group-hover:text-slate-100 transition-colors">{track.title}</h4>
                <p className="text-[11px] text-slate-600 font-body font-light truncate">{track.artist}</p>
                <div className="flex items-center justify-between mt-2">
                  <span className="text-[9px] text-slate-700 font-mono">{track.genre}</span>
                  <Badge label={`${track.match}%`} color={accentColor} />
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* ── Top Performances ─────────────────────────────── */}
        <motion.div variants={slideUp} className="mb-12">
          <span className="hud-label mb-5 block">Top Performances</span>
          <div className="spatial-card p-6 space-y-3">
            {topPerformances.map((track) => (
              <div key={track.id} className="flex items-center gap-4 py-2.5 px-3 rounded-xl hover:bg-white/[0.02] transition-colors cursor-pointer group">
                <div className="relative w-10 h-10 rounded-lg flex items-center justify-center overflow-hidden">
                  <MiniOrganism color={track.isLive ? "#EF4444" : beliefColors.consonance.primary} stage={1} size={40} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    {track.isLive && (
                      <span className="flex items-center gap-1 text-[9px] font-mono text-red-400">
                        <Radio size={10} className="animate-pulse" /> LIVE
                      </span>
                    )}
                    <h4 className="text-sm font-body font-medium text-slate-300 truncate group-hover:text-slate-100 transition-colors">{track.title}</h4>
                  </div>
                  <p className="text-[11px] text-slate-600 font-body font-light">{track.artist} &middot; {track.duration}</p>
                </div>
                <span className="text-[10px] font-mono text-slate-700">{track.plays?.toLocaleString()} plays</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* ── Friends Are Listening ────────────────────────── */}
        <motion.div variants={slideUp} className="mb-12">
          <span className="hud-label mb-5 block">Friends Are Listening</span>
          <div className="spatial-card p-6 space-y-3">
            {friendActivity.map((fa) => (
              <div key={fa.id} className="flex items-center gap-3 py-2 cursor-pointer hover:bg-white/[0.02] transition-colors rounded-lg px-2" onClick={() => navigate(`/friends/${fa.userId}`)}>
                <NucleusDot
                  color={fa.action === "performing" ? "#EF4444" : fa.action === "composed" ? beliefColors.consonance.primary : beliefColors.familiarity.primary}
                  size={5}
                  active
                  pulsing={fa.action === "performing"}
                />
                <div className="flex-1 text-sm">
                  <span className="text-slate-300 font-body font-medium">{fa.userName}</span>
                  <span className="text-slate-600 font-body font-light ml-1">
                    {fa.action === "performing" ? "is live performing" : fa.action === "composed" ? "composed" : "is listening to"}
                  </span>
                  <span className="text-slate-400 font-body font-medium ml-1">"{fa.trackTitle}"</span>
                </div>
                <span className="text-[10px] font-mono text-slate-700">{fa.timeAgo}</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* ── Analyze a Track (collapsible) ────────────────── */}
        <motion.div variants={slideUp}>
          <button onClick={() => setAnalyzeOpen(!analyzeOpen)} className="w-full flex items-center justify-between py-3 mb-4">
            <span className="hud-label">Analyze a Track</span>
            {analyzeOpen ? <ChevronUp size={14} className="text-slate-600" /> : <ChevronDown size={14} className="text-slate-600" />}
          </button>

          <AnimatePresence>
            {analyzeOpen && (
              <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.3 }}>
                <div className="spatial-card p-6 mb-6">
                  <div className="flex flex-col sm:flex-row gap-4">
                    <div className="flex-1 relative">
                      <Search size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-700" />
                      <input type="text" placeholder="Paste a track URL or search..." value={trackUrl} onChange={(e) => setTrackUrl(e.target.value)} className="w-full pl-11 pr-4 py-3 rounded-xl text-slate-300 placeholder-slate-700 focus:outline-none transition-colors text-sm font-body font-light" style={{ background: "rgba(0,0,0,0.5)", border: "1px solid rgba(255,255,255,0.06)" }} />
                    </div>
                    <div className="flex gap-3">
                      <Button variant="glass" size="md"><Upload size={14} className="mr-2" />Upload</Button>
                      <Button variant="primary" size="md" onClick={handleAnalyze} disabled={labState === "analyzing"}><Sparkles size={14} className="mr-2" />Analyze</Button>
                    </div>
                  </div>
                </div>

                <AnimatePresence mode="wait">
                  {labState === "idle" && (
                    <motion.div key="idle" {...scaleIn} exit={{ opacity: 0 }}>
                      <div className="spatial-card min-h-[250px] flex flex-col items-center justify-center text-center p-10">
                        <MiniOrganism color={accentColor} stage={1} size={60} />
                        <h3 className="text-base font-display font-medium text-slate-400 mt-6 mb-2">Drop a track into your mind</h3>
                        <p className="text-xs text-slate-600 max-w-md font-body font-light">Your mind will process it through the C3 cognitive engine.</p>
                      </div>
                    </motion.div>
                  )}

                  {labState === "analyzing" && (
                    <motion.div key="analyzing" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                      <div className="spatial-card min-h-[250px] flex flex-col items-center justify-center p-10">
                        <OrganismLoader progress={progress} color={accentColor} size={60} className="mb-6" />
                        <div className="space-y-1.5 text-[10px] text-slate-700 text-center font-mono">
                          {progress > 10 && <p>Extracting R3 features...</p>}
                          {progress > 30 && <p>Computing H3 temporal morphology...</p>}
                          {progress > 55 && <p>Running C3 belief updates...</p>}
                          {progress > 75 && <p>Computing reward signal...</p>}
                        </div>
                      </div>
                    </motion.div>
                  )}

                  {labState === "done" && traces.length > 0 && (
                    <motion.div key="done" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="space-y-6">
                      <div className="spatial-card p-8">
                        <span className="hud-label mb-6 block">Belief Traces</span>
                        <div className="space-y-6">
                          {BELIEF_KEYS.map((belief) => {
                            const bColor = beliefColors[belief].primary;
                            const values = traces.map((t) => t[belief]);
                            return (
                              <div key={belief}>
                                <div className="flex items-center justify-between mb-3">
                                  <div className="flex items-center gap-2">
                                    <NucleusDot color={bColor} size={4} active pulsing />
                                    <span className="text-xs font-body font-medium text-slate-400">{BELIEF_LABELS[belief]}</span>
                                  </div>
                                  <div className="flex items-center gap-4 text-[10px]">
                                    <span className="text-slate-700 font-mono">min: <span className="hud-value">{Math.min(...values).toFixed(2)}</span></span>
                                    <span className="text-slate-700 font-mono">max: <span className="hud-value">{Math.max(...values).toFixed(2)}</span></span>
                                  </div>
                                </div>
                                <div className="flex items-end gap-[1px] h-14 px-1">
                                  {traces.filter((_, i) => i % 2 === 0).map((t, i) => {
                                    const nv = belief === "reward" ? (t[belief] + 0.5) / 1.0 : t[belief];
                                    return (
                                      <motion.div key={i} initial={{ height: 0 }} animate={{ height: Math.max(2, nv * 56) }} transition={{ duration: 0.3, delay: i * 0.003 }} className="flex-1 rounded-sm" style={{ backgroundColor: bColor, opacity: 0.2 + nv * 0.5, minWidth: 1 }} />
                                    );
                                  })}
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      </div>
                      {peakReward && (
                        <div className="spatial-card p-6 glow-border">
                          <div className="flex items-center gap-3">
                            <Sparkles size={16} style={{ color: beliefColors.reward.primary }} />
                            <div>
                              <h3 className="text-sm font-body font-medium text-slate-300">Peak Reward at {formatTime(peakReward.time)}</h3>
                              <p className="text-[10px] text-slate-600 font-mono">Value: {peakReward.value.toFixed(3)}</p>
                            </div>
                          </div>
                        </div>
                      )}
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
