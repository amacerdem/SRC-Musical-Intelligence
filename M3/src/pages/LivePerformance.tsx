import { useState, useRef, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Zap, Clock, Users, Play, Square, Radio } from "lucide-react";
import { challenges } from "@/data/challenges";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { MindOrganismCanvas, type OrganismHandle } from "@/components/mind/MindOrganismCanvas";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { MiniOrganism } from "@/components/mind/MiniOrganism";
import { useUserStore } from "@/stores/useUserStore";
import { getPersona } from "@/data/personas";
import { pageTransition, staggerChildren, slideUp, fadeIn, glowPulse } from "@/design/animations";
import { beliefColors } from "@/design/tokens";
import { useScrollBatch } from "@/hooks/useScrollTrigger";

type Mode = "solo" | "duo";
type SessionState = "idle" | "performing" | "finished";

const MIND_CONTROLS = [
  { label: "Harmony", belief: "consonance" as const, description: "How pure vs rough the chords sound" },
  { label: "Rhythm", belief: "tempo" as const, description: "Tempo patterns & groove" },
  { label: "Dynamics", belief: "salience" as const, description: "Volume & textural changes" },
  { label: "Memory", belief: "familiarity" as const, description: "Repetition & variation" },
];

function getCountdown(endsAt: string): string {
  const diff = new Date(endsAt).getTime() - Date.now();
  if (diff <= 0) return "Ended";
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const days = Math.floor(hours / 24);
  const remainingHours = hours % 24;
  if (days > 0) return `${days}d ${remainingHours}h left`;
  return `${hours}h left`;
}

function formatSessionTime(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
}

export function LivePerformance() {
  const [mode, setMode] = useState<Mode>("solo");
  const [intensity, setIntensity] = useState(50);
  const [energy, setEnergy] = useState(60);
  const [mood, setMood] = useState(40);
  const [sessionState, setSessionState] = useState<SessionState>("idle");
  const [sessionTime, setSessionTime] = useState(0);
  const [beliefStates, setBeliefStates] = useState([0.5, 0.5, 0.5, 0.5, 0.5]);
  const [peakReward, setPeakReward] = useState(0);
  const [sessionCount] = useState(17);

  const { mind } = useUserStore();
  const persona = mind ? getPersona(mind.personaId) : null;
  const color = persona?.color ?? beliefColors.tempo.primary;
  const organismRef = useRef<OrganismHandle>(null);
  const challengeGridRef = useRef<HTMLDivElement>(null);
  const timerRef = useRef<number>(0);
  useScrollBatch(".scroll-challenge", challengeGridRef, { stagger: 0.06 });

  // Session timer + belief state simulation
  useEffect(() => {
    if (sessionState !== "performing") return;

    const interval = setInterval(() => {
      setSessionTime((t) => t + 1);

      // Simulate belief state evolution based on slider values
      setBeliefStates((prev) => {
        const intFactor = intensity / 100;
        const engFactor = energy / 100;
        const moodFactor = mood / 100;
        const t = Date.now() / 1000;

        const newStates = [
          // consonance — influenced by mood
          Math.max(0, Math.min(1, prev[0] + (moodFactor - 0.5) * 0.02 + Math.sin(t * 0.3) * 0.01)),
          // tempo — influenced by energy
          Math.max(0, Math.min(1, prev[1] + (engFactor - 0.5) * 0.02 + Math.sin(t * 0.5) * 0.015)),
          // salience — influenced by intensity
          Math.max(0, Math.min(1, prev[2] + (intFactor - 0.5) * 0.025 + Math.sin(t * 0.7) * 0.012)),
          // familiarity — gradually builds
          Math.max(0, Math.min(1, prev[3] + 0.003 + Math.sin(t * 0.2) * 0.008)),
          // reward — combination of all, with PE dynamics
          Math.max(0, Math.min(1, prev[4] + (intFactor * 0.01 + engFactor * 0.005 - 0.005) + Math.sin(t * 0.4) * 0.02)),
        ];

        // Track peak reward
        if (newStates[4] > peakReward) {
          setPeakReward(newStates[4]);
        }

        return newStates;
      });

      // Pulse organism on high reward moments
      if (Math.random() > 0.92) {
        organismRef.current?.pulse(0.5);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [sessionState, intensity, energy, mood, peakReward]);

  const handleStart = useCallback(() => {
    setSessionState("performing");
    setSessionTime(0);
    setBeliefStates([0.5, 0.5, 0.5, 0.5, 0.3]);
    setPeakReward(0.3);
    organismRef.current?.pulse(0.8);
  }, []);

  const handleStop = useCallback(() => {
    setSessionState("finished");
    organismRef.current?.pulse(0.3);
  }, []);

  const BELIEF_NAMES = ["consonance", "tempo", "salience", "familiarity", "reward"] as const;

  return (
    <motion.div {...pageTransition} className="min-h-screen bg-black pb-16 relative overflow-hidden">
      <div className="cinematic-vignette" />

      {/* Organism — responsive to session state */}
      <div className="absolute inset-0 z-0 opacity-[0.12] pointer-events-none">
        <MindOrganismCanvas
          ref={organismRef}
          color={sessionState === "performing" ? beliefColors.reward.primary : beliefColors.tempo.primary}
          secondaryColor={beliefColors.reward.primary}
          stage={sessionState === "performing" ? 2 : 1}
          intensity={sessionState === "performing" ? 0.5 + (intensity / 100) * 0.4 : 0.3}
          breathRate={sessionState === "performing" ? 2 + (energy / 100) * 3 : 5}
          variant="hero"
          constellations
          className="w-full h-full"
          interactive={false}
        />
      </div>

      {/* Header */}
      <motion.div variants={fadeIn} initial="initial" animate="animate" className="relative z-10 text-center mb-10 pt-8">
        <span className="hud-label mb-3 block">Performance</span>
        <h1 className="text-4xl md:text-5xl font-display font-bold text-slate-100 tracking-tight mb-3">
          Live Performance
        </h1>
        <p className="hud-label text-xs">Create music with your mind in real-time</p>

        {/* Session timer overlay when performing */}
        <AnimatePresence>
          {sessionState === "performing" && (
            <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
              className="mt-4 flex items-center justify-center gap-3"
            >
              <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
              <span className="text-red-400 font-mono text-lg">{formatSessionTime(sessionTime)}</span>
              <span className="hud-label text-red-400/60">LIVE</span>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* Mode toggle */}
      <motion.div variants={fadeIn} initial="initial" animate="animate" className="relative z-10 flex justify-center mb-12">
        <div className="flex rounded-full p-1" style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.06)" }}>
          {(["solo", "duo"] as const).map((m) => (
            <button key={m} onClick={() => setMode(m)} disabled={sessionState === "performing"}
              className="px-6 py-2 rounded-full text-sm font-display font-medium transition-all duration-300 capitalize disabled:opacity-50"
              style={{
                background: mode === m ? `${color}15` : "transparent",
                color: mode === m ? "#E2E8F0" : "#475569",
                border: mode === m ? `1px solid ${color}25` : "1px solid transparent",
              }}
            >
              {m === "solo" ? "Solo Performance" : "Duo Session"}
            </button>
          ))}
        </div>
      </motion.div>

      <motion.div variants={staggerChildren} initial="initial" animate="animate" className="relative z-10 max-w-5xl xl:max-w-6xl 2xl:max-w-7xl mx-auto px-4">
        {/* Control panels */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* You Control */}
          <motion.div variants={slideUp} className="spatial-card p-7">
            <div className="flex items-center gap-2 mb-6">
              <NucleusDot color={color} size={5} active pulsing={sessionState === "performing"} />
              <span className="hud-label">You Control</span>
              {sessionState === "performing" && (
                <span className="text-[9px] font-mono text-slate-700 ml-auto">Adjustments affect output in real-time</span>
              )}
            </div>
            <div className="space-y-6">
              <SliderControl label="Intensity" value={intensity} onChange={setIntensity} color={color}
                description="How dramatic the music feels — subtle whispers to overwhelming waves" />
              <SliderControl label="Energy" value={energy} onChange={setEnergy} color={beliefColors.tempo.primary}
                description="Rhythmic density and drive — from floating to pounding" />
              <SliderControl label="Mood" value={mood} onChange={setMood} color={beliefColors.consonance.primary}
                description="Dark and tense vs bright and resolved" />
            </div>
          </motion.div>

          {/* Your Mind Controls */}
          <motion.div variants={slideUp} className="spatial-card p-7">
            <div className="flex items-center gap-2 mb-6">
              <NucleusDot color={beliefColors.reward.primary} size={5} active />
              <span className="hud-label">Your Mind Controls</span>
            </div>
            <div className="space-y-3">
              {MIND_CONTROLS.map((ctrl, i) => {
                const bColor = beliefColors[ctrl.belief].primary;
                const stateValue = beliefStates[i];
                const isPerforming = sessionState === "performing";
                return (
                  <div key={ctrl.belief} className="flex items-center gap-3 py-2.5 px-3 rounded-xl transition-all"
                    style={{ background: `${bColor}${isPerforming ? "0a" : "06"}`, border: `1px solid ${bColor}${isPerforming ? "15" : "08"}` }}
                  >
                    <div className="w-8 h-8 rounded-lg flex items-center justify-center">
                      <MiniOrganism color={bColor} stage={1} size={32} />
                    </div>
                    <div className="flex-1">
                      <div className="text-sm font-body font-medium text-slate-300">{ctrl.label}</div>
                      <div className="text-[10px] text-slate-600 font-body font-light">{ctrl.description}</div>
                    </div>
                    {/* Live belief state indicator */}
                    <div className="flex items-center gap-2">
                      {isPerforming && (
                        <span className="text-[10px] font-mono" style={{ color: bColor }}>
                          {(stateValue * 100).toFixed(0)}
                        </span>
                      )}
                      <div className={`w-2 h-2 rounded-full ${isPerforming ? "animate-pulse" : ""}`}
                        style={{
                          background: bColor,
                          boxShadow: isPerforming ? `0 0 ${8 + stateValue * 12}px ${bColor}${Math.round(stateValue * 99).toString(16).padStart(2, "0")}` : `0 0 8px ${bColor}60`,
                        }}
                      />
                    </div>
                  </div>
                );
              })}

              {/* Reward — special treatment */}
              {sessionState === "performing" && (
                <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                  className="flex items-center gap-3 py-2.5 px-3 rounded-xl mt-2"
                  style={{ background: `${beliefColors.reward.primary}0a`, border: `1px solid ${beliefColors.reward.primary}20` }}
                >
                  <div className="w-8 h-8 rounded-lg flex items-center justify-center">
                    <MiniOrganism color={beliefColors.reward.primary} stage={2} size={32} />
                  </div>
                  <div className="flex-1">
                    <div className="text-sm font-body font-medium text-slate-300">Reward</div>
                    <div className="text-[10px] text-slate-600 font-body font-light">Emergent from all belief interactions</div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-mono" style={{ color: beliefColors.reward.primary }}>
                      {(beliefStates[4] * 100).toFixed(0)}
                    </span>
                    <div className="w-2 h-2 rounded-full animate-pulse"
                      style={{ background: beliefColors.reward.primary, boxShadow: `0 0 ${8 + beliefStates[4] * 16}px ${beliefColors.reward.primary}80` }}
                    />
                  </div>
                </motion.div>
              )}
            </div>
          </motion.div>
        </div>

        {/* Real-time belief trace (during session) */}
        <AnimatePresence>
          {sessionState === "performing" && (
            <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} exit={{ opacity: 0, height: 0 }}
              className="mb-8"
            >
              <div className="spatial-card p-6 glow-border" style={{ "--glow-color": beliefColors.reward.primary } as React.CSSProperties}>
                <div className="flex items-center justify-between mb-4">
                  <span className="hud-label">Live Belief States</span>
                  <span className="text-[10px] font-mono text-slate-700">
                    Peak reward: <span style={{ color: beliefColors.reward.primary }}>{(peakReward * 100).toFixed(0)}</span>
                  </span>
                </div>
                <div className="flex items-end gap-3 h-20">
                  {BELIEF_NAMES.map((b, i) => {
                    const val = beliefStates[i];
                    const bColor = beliefColors[b].primary;
                    return (
                      <div key={b} className="flex-1 flex flex-col items-center gap-1">
                        <motion.div className="w-full rounded-t-sm" style={{ backgroundColor: bColor, opacity: 0.3 + val * 0.5 }}
                          animate={{ height: `${val * 80}px` }} transition={{ duration: 0.5 }}
                        />
                        <span className="text-[8px] font-mono" style={{ color: `${bColor}80` }}>{b.slice(0, 4)}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Session finished summary */}
        <AnimatePresence>
          {sessionState === "finished" && (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
              className="mb-8"
            >
              <div className="spatial-card p-8 glow-border text-center" style={{ "--glow-color": beliefColors.reward.primary } as React.CSSProperties}>
                <h3 className="text-lg font-display font-medium text-slate-300 mb-2">Session Complete</h3>
                <div className="flex justify-center gap-8 mb-4">
                  <div>
                    <span className="hud-value text-2xl" style={{ color: beliefColors.tempo.primary }}>{formatSessionTime(sessionTime)}</span>
                    <p className="text-[9px] font-mono text-slate-700">Duration</p>
                  </div>
                  <div>
                    <span className="hud-value text-2xl" style={{ color: beliefColors.reward.primary }}>{(peakReward * 100).toFixed(0)}</span>
                    <p className="text-[9px] font-mono text-slate-700">Peak Pleasure</p>
                  </div>
                  <div>
                    <span className="hud-value text-2xl" style={{ color: beliefColors.salience.primary }}>{(beliefStates[2] * 100).toFixed(0)}</span>
                    <p className="text-[9px] font-mono text-slate-700">Attention</p>
                  </div>
                </div>
                <p className="text-xs text-slate-600 font-body font-light">
                  Your {persona?.name ?? "mind"} generated {sessionTime} seconds of live music.
                  The most surprising moment was around {formatSessionTime(Math.round(sessionTime * 0.65))}.
                </p>
                <Button variant="glass" size="sm" className="mt-4" onClick={() => setSessionState("idle")}>New Session</Button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Start/Stop session */}
        <motion.div variants={slideUp} className="flex justify-center mb-12">
          {sessionState === "idle" || sessionState === "finished" ? (
            <Button variant="primary" size="lg" onClick={handleStart}>
              <Play size={18} className="mr-2" />
              Start {mode === "solo" ? "Solo" : "Duo"} Session
            </Button>
          ) : (
            <Button variant="glass" size="lg" onClick={handleStop}>
              <Square size={18} className="mr-2" />
              End Session
            </Button>
          )}
        </motion.div>

        {/* Stats */}
        <motion.div variants={slideUp} className="flex justify-center gap-12 mb-12">
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-2">
              <NucleusDot color={beliefColors.salience.primary} size={5} active pulsing />
              <span className="hud-label">Sessions</span>
            </div>
            <span className="hud-value text-3xl" style={{ color: beliefColors.salience.primary }}>{sessionCount}</span>
          </div>
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-2">
              <NucleusDot color={beliefColors.tempo.primary} size={5} active />
              <span className="hud-label">Total Time</span>
            </div>
            <span className="hud-value text-3xl" style={{ color: beliefColors.tempo.primary }}>4h</span>
          </div>
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-2">
              <NucleusDot color={beliefColors.reward.primary} size={5} active pulsing />
              <span className="hud-label">Best Streak</span>
            </div>
            <span className="hud-value text-3xl" style={{ color: beliefColors.reward.primary }}>5</span>
          </div>
        </motion.div>

        {/* Challenges */}
        <span className="hud-label mb-6 block">Active Sessions</span>
        <div ref={challengeGridRef} className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {challenges.map((ch) => {
            const chColor = beliefColors[ch.type === "entropy" ? "tempo" : ch.type === "resolution" ? "salience" : ch.type === "fusion" ? "consonance" : "familiarity"].primary;
            const countdown = getCountdown(ch.endsAt);
            return (
              <motion.div key={ch.id} className="scroll-challenge" animate={glowPulse.animate}>
                <div className="spatial-card p-6 relative overflow-hidden group cursor-pointer transition-all duration-500"
                  onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.boxShadow = `0 4px 40px ${chColor}15`; }}
                  onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.boxShadow = "none"; }}
                >
                  <div className="absolute top-0 left-0 right-0 h-[1px]" style={{ background: `linear-gradient(90deg, ${chColor}40, transparent)` }} />
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <div className="relative w-10 h-10 rounded-xl flex items-center justify-center overflow-hidden">
                        <MiniOrganism color={chColor} stage={1} size={40} />
                        <div className="absolute inset-0 flex items-center justify-center z-10" style={{ color: chColor }}><Zap size={16} /></div>
                      </div>
                      <div>
                        <h3 className="text-sm font-body font-semibold text-slate-200">{ch.title}</h3>
                        <Badge label={ch.type} color={chColor} />
                      </div>
                    </div>
                    <span className="hud-value text-xs" style={{ color: beliefColors.reward.primary }}>+{ch.xpReward} XP</span>
                  </div>
                  <p className="text-xs text-slate-600 mb-4 leading-relaxed font-body font-light">{ch.description}</p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4 text-xs text-slate-700">
                      <span className="flex items-center gap-1 font-mono"><Users size={11} /> {ch.participants.toLocaleString()}</span>
                      <span className="flex items-center gap-1 font-mono"><Clock size={11} /> {countdown}</span>
                    </div>
                    <Button variant="primary" size="sm">Join</Button>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </motion.div>
    </motion.div>
  );
}

function SliderControl({ label, value, onChange, color, description }: {
  label: string; value: number; onChange: (v: number) => void; color: string; description?: string;
}) {
  return (
    <div>
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-body font-medium text-slate-400">{label}</span>
        <span className="hud-value text-xs" style={{ color }}>{value}%</span>
      </div>
      <input type="range" min={0} max={100} value={value} onChange={(e) => onChange(Number(e.target.value))}
        className="w-full h-[3px] rounded-full appearance-none cursor-pointer"
        style={{ background: `linear-gradient(90deg, ${color} ${value}%, rgba(255,255,255,0.05) ${value}%)`, accentColor: color }}
      />
      {description && <p className="text-[9px] text-slate-700 font-mono mt-1">{description}</p>}
    </div>
  );
}
