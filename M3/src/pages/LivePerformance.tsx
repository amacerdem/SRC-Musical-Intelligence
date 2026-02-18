import { useState, useRef } from "react";
import { motion } from "framer-motion";
import { Zap, Clock, Users, Flame, Play, Radio } from "lucide-react";
import { challenges } from "@/data/challenges";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { MiniOrganism } from "@/components/mind/MiniOrganism";
import { useUserStore } from "@/stores/useUserStore";
import { getPersona } from "@/data/personas";
import { pageTransition, staggerChildren, slideUp, fadeIn, glowPulse } from "@/design/animations";
import { beliefColors } from "@/design/tokens";
import { useScrollBatch } from "@/hooks/useScrollTrigger";

type Mode = "solo" | "duo";

const MIND_CONTROLS = [
  { label: "Harmony", belief: "consonance" as const, description: "Consonance & dissonance balance" },
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

export function LivePerformance() {
  const [mode, setMode] = useState<Mode>("solo");
  const [intensity, setIntensity] = useState(50);
  const [energy, setEnergy] = useState(60);
  const [mood, setMood] = useState(40);
  const { mind } = useUserStore();
  const persona = mind ? getPersona(mind.personaId) : null;
  const color = persona?.color ?? beliefColors.tempo.primary;
  const challengeGridRef = useRef<HTMLDivElement>(null);
  useScrollBatch(".scroll-challenge", challengeGridRef, { stagger: 0.06 });

  return (
    <motion.div {...pageTransition} className="min-h-screen bg-black pb-16 relative overflow-hidden">
      <div className="cinematic-vignette" />

      {/* Hero organism — high-energy */}
      <div className="absolute inset-0 z-0 opacity-[0.12] pointer-events-none">
        <MindOrganismCanvas
          color={beliefColors.tempo.primary}
          secondaryColor={beliefColors.reward.primary}
          stage={2}
          intensity={0.7}
          breathRate={3}
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
      </motion.div>

      {/* Mode toggle */}
      <motion.div variants={fadeIn} initial="initial" animate="animate" className="relative z-10 flex justify-center mb-12">
        <div className="flex rounded-full p-1" style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.06)" }}>
          {(["solo", "duo"] as const).map((m) => (
            <button
              key={m}
              onClick={() => setMode(m)}
              className="px-6 py-2 rounded-full text-sm font-display font-medium transition-all duration-300 capitalize"
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
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-12">
          {/* You Control */}
          <motion.div variants={slideUp} className="spatial-card p-7">
            <div className="flex items-center gap-2 mb-6">
              <NucleusDot color={color} size={5} active pulsing />
              <span className="hud-label">You Control</span>
            </div>
            <div className="space-y-6">
              <SliderControl label="Intensity" value={intensity} onChange={setIntensity} color={color} />
              <SliderControl label="Energy" value={energy} onChange={setEnergy} color={beliefColors.tempo.primary} />
              <SliderControl label="Mood" value={mood} onChange={setMood} color={beliefColors.consonance.primary} />
            </div>
          </motion.div>

          {/* Your Mind Controls */}
          <motion.div variants={slideUp} className="spatial-card p-7">
            <div className="flex items-center gap-2 mb-6">
              <NucleusDot color={beliefColors.reward.primary} size={5} active />
              <span className="hud-label">Your Mind Controls</span>
            </div>
            <div className="space-y-4">
              {MIND_CONTROLS.map((ctrl) => {
                const bColor = beliefColors[ctrl.belief].primary;
                return (
                  <div key={ctrl.belief} className="flex items-center gap-3 py-2 px-3 rounded-xl" style={{ background: `${bColor}06`, border: `1px solid ${bColor}08` }}>
                    <div className="w-8 h-8 rounded-lg flex items-center justify-center">
                      <MiniOrganism color={bColor} stage={1} size={32} />
                    </div>
                    <div className="flex-1">
                      <div className="text-sm font-body font-medium text-slate-300">{ctrl.label}</div>
                      <div className="text-[10px] text-slate-600">{ctrl.description}</div>
                    </div>
                    <div className="w-2 h-2 rounded-full animate-pulse" style={{ background: bColor, boxShadow: `0 0 8px ${bColor}60` }} />
                  </div>
                );
              })}
            </div>
          </motion.div>
        </div>

        {/* Start session */}
        <motion.div variants={slideUp} className="flex justify-center mb-16">
          <Button variant="primary" size="lg">
            <Play size={18} className="mr-2" />
            Start {mode === "solo" ? "Solo" : "Duo"} Session
          </Button>
        </motion.div>

        {/* Stats */}
        <motion.div variants={slideUp} className="flex justify-center gap-12 mb-12">
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-2">
              <NucleusDot color={beliefColors.salience.primary} size={5} active pulsing />
              <span className="hud-label">Sessions</span>
            </div>
            <span className="hud-value text-3xl" style={{ color: beliefColors.salience.primary }}>17</span>
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

        {/* Active sessions (challenges) */}
        <span className="hud-label mb-6 block">Active Sessions</span>
        <div ref={challengeGridRef} className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {challenges.map((ch) => {
            const chColor = beliefColors[ch.type === "entropy" ? "tempo" : ch.type === "resolution" ? "salience" : ch.type === "fusion" ? "consonance" : "familiarity"].primary;
            const countdown = getCountdown(ch.endsAt);
            return (
              <motion.div key={ch.id} className="scroll-challenge" animate={glowPulse.animate}>
                <div
                  className="spatial-card p-6 relative overflow-hidden group cursor-pointer transition-all duration-500"
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

function SliderControl({ label, value, onChange, color }: { label: string; value: number; onChange: (v: number) => void; color: string }) {
  return (
    <div>
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-body font-medium text-slate-400">{label}</span>
        <span className="hud-value text-xs" style={{ color }}>{value}%</span>
      </div>
      <div className="relative">
        <input
          type="range"
          min={0}
          max={100}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="w-full h-[3px] rounded-full appearance-none cursor-pointer"
          style={{
            background: `linear-gradient(90deg, ${color} ${value}%, rgba(255,255,255,0.05) ${value}%)`,
            accentColor: color,
          }}
        />
      </div>
    </div>
  );
}
