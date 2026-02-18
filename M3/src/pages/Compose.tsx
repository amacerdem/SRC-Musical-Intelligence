import { useState, useCallback, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Wand2, Share2, Play, Loader2, Check, Brain } from "lucide-react";
import { useUserStore } from "@/stores/useUserStore";
import { getPersona } from "@/data/personas";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { pageTransition, staggerChildren, slideUp, scaleIn, fadeIn } from "@/design/animations";
import { beliefColors } from "@/design/tokens";

type GenerationState = "idle" | "generating" | "done";

const DURATION_OPTIONS = [
  { label: "30s", value: 30 },
  { label: "1 min", value: 60 },
  { label: "3 min", value: 180 },
];

const BELIEF_NAMES = ["consonance", "tempo", "salience", "familiarity", "reward"] as const;
const BELIEF_LABELS: Record<string, string> = {
  consonance: "Harmony", tempo: "Rhythm", salience: "Attention", familiarity: "Memory", reward: "Pleasure",
};

/** Generation phases — what your mind is doing */
const GEN_PHASES = [
  { at: 5, text: "Reading your musical DNA...", belief: null },
  { at: 15, text: "Chaos appetite → choosing harmonic vocabulary", belief: "consonance" as const },
  { at: 25, text: "Need for closure → how often the music resolves", belief: "consonance" as const },
  { at: 35, text: "Tension love → designing the build-ups", belief: "reward" as const },
  { at: 45, text: "Surprise sensitivity → shaping dynamic range", belief: "salience" as const },
  { at: 55, text: "Repetition comfort → how deep the patterns go", belief: "familiarity" as const },
  { at: 65, text: "Building 97 perceptual targets...", belief: null },
  { at: 75, text: "Shaping the time feel across scales...", belief: "tempo" as const },
  { at: 85, text: "Optimizing for maximum pleasure...", belief: "reward" as const },
  { at: 92, text: "Rendering waveform...", belief: null },
];

/** Generate mock belief influence values based on user params */
function generateBeliefInfluence(style: number, complexity: number) {
  return {
    consonance: 0.3 + (complexity / 100) * 0.5 + Math.random() * 0.1,
    tempo: 0.2 + (style / 100) * 0.4 + Math.random() * 0.1,
    salience: 0.1 + (style / 100) * 0.6 + Math.random() * 0.1,
    familiarity: 0.8 - (complexity / 100) * 0.4 + Math.random() * 0.1,
    reward: 0.3 + (style / 100) * 0.2 + (complexity / 100) * 0.2 + Math.random() * 0.1,
  };
}

/** Generate a mock waveform that's deterministic per-generation */
function generateWaveform(style: number, complexity: number, duration: number): number[] {
  const count = 120;
  const bars: number[] = [];
  const seed = style * 1000 + complexity * 10 + duration;
  for (let i = 0; i < count; i++) {
    const center = count / 2;
    const dist = Math.abs(i - center) / center;
    // Use seeded pseudo-random instead of Math.random for stable output
    const pseudo = Math.sin(seed + i * 13.37) * 0.5 + 0.5;
    const envelope = 1 - dist * 0.6;
    const noise = 0.3 + pseudo * 0.7;
    const complexityFactor = 0.5 + (complexity / 100) * 0.5;
    bars.push(Math.max(6, envelope * noise * complexityFactor * 180));
  }
  return bars;
}

export function Compose() {
  const { mind } = useUserStore();
  const persona = mind ? getPersona(mind.personaId) : null;

  const [style, setStyle] = useState(50);
  const [duration, setDuration] = useState(60);
  const [complexity, setComplexity] = useState(50);
  const [genState, setGenState] = useState<GenerationState>("idle");
  const [progress, setProgress] = useState(0);
  const [shared, setShared] = useState(false);
  const [generationCount, setGenerationCount] = useState(0);

  const accentColor = persona?.color ?? beliefColors.consonance.primary;

  const beliefInfluence = useMemo(
    () => genState === "done" ? generateBeliefInfluence(style, complexity) : null,
    [genState, style, complexity],
  );

  const waveform = useMemo(
    () => genState === "done" ? generateWaveform(style, complexity, duration) : [],
    [genState, style, complexity, duration],
  );

  const handleGenerate = useCallback(() => {
    setGenState("generating");
    setProgress(0);
    setShared(false);
    setGenerationCount((c) => c + 1);

    const interval = setInterval(() => {
      setProgress((prev) => {
        const next = prev + Math.random() * 8 + 2;
        if (next >= 100) {
          clearInterval(interval);
          setTimeout(() => setGenState("done"), 300);
          return 100;
        }
        return next;
      });
    }, 180);
  }, []);

  const handleShare = () => {
    setShared(true);
    setTimeout(() => setShared(false), 3000);
  };

  const activePhases = GEN_PHASES.filter((p) => progress > p.at);

  return (
    <motion.div {...pageTransition} className="min-h-screen bg-black relative overflow-hidden pb-16">
      {persona && mind && (
        <div className="absolute inset-0 opacity-10 pointer-events-none">
          <MindOrganismCanvas color={accentColor} stage={mind.stage} intensity={0.3} breathRate={6} className="w-full h-full" />
        </div>
      )}
      <div className="cinematic-vignette" />
      <div className="absolute top-0 right-1/4 w-[500px] h-[500px] rounded-full blur-[200px] opacity-[0.06] pointer-events-none"
        style={{ backgroundColor: accentColor }}
      />

      {/* Header */}
      <motion.div variants={fadeIn} initial="initial" animate="animate" className="relative z-10 text-center mb-12 pt-8">
        <span className="hud-label mb-3 block">Composition</span>
        <h1 className="text-4xl md:text-5xl font-display font-bold text-slate-100 tracking-tight mb-3">Compose</h1>
        <p className="hud-label text-xs">Compose music shaped by your mind</p>
        {persona && (
          <div className="flex items-center justify-center gap-3 mt-4">
            <Badge label={persona.name} color={accentColor} size="md" />
            <span className="text-xs text-slate-700 font-body font-light">shapes every note</span>
          </div>
        )}
      </motion.div>

      <motion.div variants={staggerChildren} initial="initial" animate="animate" className="relative z-10">
        <div className="grid grid-cols-12 gap-8 max-w-5xl xl:max-w-6xl 2xl:max-w-7xl mx-auto px-4">
          {/* Controls */}
          <motion.div variants={slideUp} className="col-span-12 lg:col-span-5 space-y-6">
            {/* Style */}
            <div className="spatial-card p-7">
              <div className="flex items-center justify-between mb-5">
                <div className="flex items-center gap-2">
                  <NucleusDot color={beliefColors.salience.primary} size={3} active />
                  <span className="hud-label">Style</span>
                </div>
                <span className="hud-value text-sm" style={{ color: beliefColors.salience.primary }}>{style}%</span>
              </div>
              <div className="flex items-center justify-between text-[10px] text-slate-700 mb-2 font-mono">
                <span>Calm</span><span>Intense</span>
              </div>
              <input type="range" min={0} max={100} value={style} onChange={(e) => setStyle(Number(e.target.value))}
                className="w-full h-[3px] rounded-full bg-white/5 appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:cursor-pointer"
                style={{ accentColor: beliefColors.salience.primary, background: `linear-gradient(90deg, ${beliefColors.salience.primary}40 ${style}%, rgba(255,255,255,0.05) ${style}%)` }}
              />
              <p className="text-[9px] text-slate-700 font-mono mt-2">
                Controls how dramatic the dynamics are — quiet vs loud, subtle vs bold
              </p>
            </div>

            {/* Duration */}
            <div className="spatial-card p-7">
              <span className="hud-label mb-5 block">Duration</span>
              <div className="flex gap-3">
                {DURATION_OPTIONS.map((opt) => (
                  <button key={opt.value} onClick={() => setDuration(opt.value)}
                    className={`flex-1 py-3 rounded-xl text-sm font-body font-medium transition-all duration-300 ${duration === opt.value ? "text-white" : "text-slate-500 hover:text-slate-300"}`}
                    style={duration === opt.value
                      ? { background: `linear-gradient(135deg, ${beliefColors.tempo.primary}40, ${beliefColors.tempo.primary}20)`, border: `1px solid ${beliefColors.tempo.primary}30` }
                      : { background: "rgba(0,0,0,0.5)", backdropFilter: "blur(12px)", border: "1px solid rgba(255,255,255,0.06)" }
                    }
                  >
                    {opt.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Complexity */}
            <div className="spatial-card p-7">
              <div className="flex items-center justify-between mb-5">
                <div className="flex items-center gap-2">
                  <NucleusDot color={beliefColors.consonance.primary} size={3} active />
                  <span className="hud-label">Complexity</span>
                </div>
                <span className="hud-value text-sm" style={{ color: beliefColors.consonance.primary }}>{complexity}%</span>
              </div>
              <div className="flex items-center justify-between text-[10px] text-slate-700 mb-2 font-mono">
                <span>Simple</span><span>Complex</span>
              </div>
              <input type="range" min={0} max={100} value={complexity} onChange={(e) => setComplexity(Number(e.target.value))}
                className="w-full h-[3px] rounded-full bg-white/5 appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:cursor-pointer"
                style={{ accentColor: beliefColors.consonance.primary, background: `linear-gradient(90deg, ${beliefColors.consonance.primary}40 ${complexity}%, rgba(255,255,255,0.05) ${complexity}%)` }}
              />
              <p className="text-[9px] text-slate-700 font-mono mt-2">
                Maps to: harmonic vocabulary size, entropy tolerance, consonance target range
              </p>
            </div>

            {/* How your mind shapes this */}
            {persona && (
              <div className="spatial-card p-5">
                <div className="flex items-center gap-2 mb-3">
                  <Brain size={12} style={{ color: `${accentColor}60` }} />
                  <span className="hud-label">Mind Influence</span>
                </div>
                <p className="text-[10px] text-slate-600 font-body font-light leading-relaxed">
                  As a <span style={{ color: accentColor }}>{persona.name}</span>, your{" "}
                  {persona.axes.tensionAppetite > 0.7 ? "high tension appetite shapes the build-up architecture" :
                   persona.axes.monotonyTolerance > 0.6 ? "deep monotony tolerance allows for rich repetition structures" :
                   persona.axes.entropyTolerance > 0.7 ? "entropy tolerance unlocks chaotic harmonic vocabularies" :
                   "resolution craving drives strong cadential patterns"}.{" "}
                  Your {persona.family} neural family biases the generation toward{" "}
                  {persona.family === "Alchemists" ? "tension-release cycles" :
                   persona.family === "Architects" ? "structural precision" :
                   persona.family === "Explorers" ? "novel sonic territories" :
                   persona.family === "Anchors" ? "emotionally resonant textures" :
                   "rhythmic drive"}.
                </p>
              </div>
            )}

            {/* Generate button */}
            <Button variant="primary" size="lg" className="w-full" onClick={handleGenerate} disabled={genState === "generating"}>
              {genState === "generating" ? (
                <><Loader2 size={20} className="mr-2 animate-spin" />Generating...</>
              ) : genState === "done" ? (
                <><Wand2 size={20} className="mr-2" />Compose Again</>
              ) : (
                <><Wand2 size={20} className="mr-2" />Compose</>
              )}
            </Button>
          </motion.div>

          {/* Output */}
          <motion.div variants={slideUp} className="col-span-12 lg:col-span-7">
            <div className="spatial-card p-8 min-h-[600px] flex flex-col glow-border">
              <span className="hud-label mb-6">Output</span>

              <AnimatePresence mode="wait">
                {genState === "idle" && (
                  <motion.div key="idle" {...scaleIn} exit={{ opacity: 0, scale: 0.95 }}
                    className="flex-1 flex flex-col items-center justify-center text-center"
                  >
                    <div className="w-20 h-20 rounded-full flex items-center justify-center mb-6"
                      style={{ background: "rgba(0,0,0,0.5)", backdropFilter: "blur(12px)", border: "1px solid rgba(255,255,255,0.06)" }}
                    >
                      <Play size={28} className="text-slate-600 ml-1" />
                    </div>
                    <p className="text-slate-600 text-sm font-body font-light">Configure your parameters and hit Compose</p>
                    <p className="text-slate-700 text-xs mt-2 font-body font-light">
                      Your {persona?.name ?? "mind"} profile will influence every harmonic decision
                    </p>
                  </motion.div>
                )}

                {genState === "generating" && (
                  <motion.div key="generating" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                    className="flex-1 flex flex-col items-center justify-center"
                  >
                    <div className="w-full max-w-sm">
                      <div className="flex items-center justify-between text-sm mb-3">
                        <span className="text-slate-500 font-body font-light">Processing through your mind...</span>
                        <span className="hud-value text-sm" style={{ color: beliefColors.familiarity.primary }}>{Math.round(progress)}%</span>
                      </div>
                      <div className="w-full h-[2px] rounded-full bg-white/5 overflow-hidden">
                        <motion.div className="h-full rounded-full"
                          style={{ width: `${progress}%`, background: `linear-gradient(90deg, ${beliefColors.consonance.primary}, ${beliefColors.tempo.primary})` }}
                        />
                      </div>

                      {/* Pipeline phases — neuroscience-grounded */}
                      <div className="mt-6 space-y-2">
                        {activePhases.slice(-4).map((phase, i) => (
                          <motion.div key={phase.at} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }}
                            className="flex items-center gap-2"
                          >
                            {phase.belief && <NucleusDot color={beliefColors[phase.belief].primary} size={3} active />}
                            {!phase.belief && <div className="w-1.5 h-1.5 rounded-full bg-slate-700" />}
                            <span className="text-[10px] font-mono" style={{ color: phase.belief ? `${beliefColors[phase.belief].primary}80` : "#475569" }}>
                              {phase.text}
                            </span>
                          </motion.div>
                        ))}
                      </div>

                      {/* Active belief indicators */}
                      <div className="mt-6 flex justify-center gap-4">
                        {BELIEF_NAMES.map((b) => {
                          const isActive = activePhases.some((p) => p.belief === b);
                          const bColor = beliefColors[b].primary;
                          return (
                            <div key={b} className="flex flex-col items-center gap-1">
                              <NucleusDot color={bColor} size={4} active={isActive} pulsing={isActive} />
                              <span className="text-[8px] font-mono" style={{ color: isActive ? bColor : "#334155" }}>
                                {b.slice(0, 4)}
                              </span>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  </motion.div>
                )}

                {genState === "done" && beliefInfluence && (
                  <motion.div key="done" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                    className="flex-1 flex flex-col"
                  >
                    {/* Waveform */}
                    <div className="flex-1 flex items-end justify-center gap-[1px] px-2 pb-4">
                      {waveform.map((h, i) => {
                        // Color each bar based on which belief "dominates" at that position
                        const pos = i / waveform.length;
                        const beliefIdx = Math.floor(pos * 5) % 5;
                        const bColor = beliefColors[BELIEF_NAMES[beliefIdx]].primary;
                        return (
                          <motion.div key={i} initial={{ height: 0 }} animate={{ height: h }}
                            transition={{ duration: 0.4, delay: i * 0.005 }}
                            className="flex-1 rounded-sm min-w-[1px]"
                            style={{ backgroundColor: bColor, opacity: 0.15 + (h / 200) * 0.5 }}
                          />
                        );
                      })}
                    </div>

                    {/* Belief contribution bars */}
                    <div className="border-t border-white/5 pt-5 mb-4">
                      <span className="hud-label mb-3 block">Belief Influence on Generation</span>
                      <div className="grid grid-cols-5 gap-2">
                        {BELIEF_NAMES.map((b) => {
                          const val = beliefInfluence[b];
                          const bColor = beliefColors[b].primary;
                          return (
                            <div key={b} className="text-center">
                              <div className="h-16 flex items-end justify-center mb-1">
                                <motion.div className="w-4 rounded-t-sm"
                                  style={{ backgroundColor: bColor, opacity: 0.4 + val * 0.4 }}
                                  initial={{ height: 0 }} animate={{ height: `${val * 64}px` }}
                                  transition={{ duration: 0.6, delay: BELIEF_NAMES.indexOf(b) * 0.08 }}
                                />
                              </div>
                              <div className="text-[9px] font-mono" style={{ color: bColor }}>{(val * 100).toFixed(0)}%</div>
                              <div className="text-[8px] font-mono text-slate-700">{BELIEF_LABELS[b]}</div>
                            </div>
                          );
                        })}
                      </div>
                    </div>

                    {/* Metadata */}
                    <div className="border-t border-white/5 pt-5">
                      <div className="flex items-center justify-between">
                        <div>
                          <h4 className="text-sm font-body font-medium text-slate-300 mb-2">
                            {persona?.name ?? "Mind"} Generation #{generationCount}
                          </h4>
                          <div className="flex items-center gap-2">
                            <span className="hud-label">{duration}s</span>
                            <span className="text-slate-700">·</span>
                            <span className="hud-label" style={{ color: `${beliefColors.salience.primary}80` }}>
                              {style > 60 ? "Intense" : style > 30 ? "Balanced" : "Calm"}
                            </span>
                            <span className="text-slate-700">·</span>
                            <span className="hud-label" style={{ color: `${beliefColors.consonance.primary}80` }}>
                              {complexity > 60 ? "Complex" : complexity > 30 ? "Moderate" : "Simple"}
                            </span>
                          </div>
                          <p className="text-[9px] font-mono text-slate-700 mt-1">
                            Peak reward predicted at ~{Math.round(duration * 0.65)}s · Estimated PE: {(0.3 + style * 0.004 + complexity * 0.002).toFixed(2)}σ
                          </p>
                        </div>
                        <Button variant="glass" size="sm" onClick={handleShare}>
                          {shared ? <><Check size={14} className="mr-2 text-green-400" />Shared</> : <><Share2 size={14} className="mr-2" />Share</>}
                        </Button>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </motion.div>
        </div>
      </motion.div>
    </motion.div>
  );
}
