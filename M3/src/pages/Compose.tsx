import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Wand2, Share2, Play, Loader2 } from "lucide-react";
import { useUserStore } from "@/stores/useUserStore";
import { getPersona } from "@/data/personas";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
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

export function Compose() {
  const { mind } = useUserStore();
  const persona = mind ? getPersona(mind.personaId) : null;

  const [style, setStyle] = useState(50);
  const [duration, setDuration] = useState(60);
  const [complexity, setComplexity] = useState(50);
  const [genState, setGenState] = useState<GenerationState>("idle");
  const [progress, setProgress] = useState(0);

  const handleGenerate = useCallback(() => {
    setGenState("generating");
    setProgress(0);

    const interval = setInterval(() => {
      setProgress((prev) => {
        const next = prev + Math.random() * 12 + 3;
        if (next >= 100) {
          clearInterval(interval);
          setTimeout(() => setGenState("done"), 300);
          return 100;
        }
        return next;
      });
    }, 200);
  }, []);

  const accentColor = persona?.color ?? beliefColors.consonance.primary;

  return (
    <motion.div {...pageTransition} className="min-h-screen bg-black relative overflow-hidden pb-16">
      {/* Organism background — subtle, atmospheric */}
      {persona && mind && (
        <div className="absolute inset-0 opacity-10 pointer-events-none">
          <MindOrganismCanvas
            color={accentColor}
            stage={mind.stage}
            intensity={0.3}
            breathRate={6}
            className="w-full h-full"
          />
        </div>
      )}

      {/* Cinematic vignette */}
      <div className="cinematic-vignette" />

      {/* Ambient glow */}
      <div
        className="absolute top-0 right-1/4 w-[500px] h-[500px] rounded-full blur-[200px] opacity-[0.06] pointer-events-none"
        style={{ backgroundColor: accentColor }}
      />

      {/* Header */}
      <motion.div variants={fadeIn} initial="initial" animate="animate" className="relative z-10 text-center mb-12 pt-8">
        <span className="hud-label mb-3 block">Composition</span>
        <h1 className="text-4xl md:text-5xl font-display font-bold text-slate-100 tracking-tight mb-3">
          Compose
        </h1>
        <p className="hud-label text-xs">Compose music shaped by your mind</p>
        {persona && (
          <div className="flex items-center justify-center gap-3 mt-4">
            <Badge label={persona.name} color={accentColor} size="md" />
            <span className="text-xs text-slate-700 font-body font-light">will shape the generation</span>
          </div>
        )}
      </motion.div>

      <motion.div variants={staggerChildren} initial="initial" animate="animate" className="relative z-10">
        <div className="grid grid-cols-12 gap-8 max-w-5xl xl:max-w-6xl 2xl:max-w-7xl mx-auto px-4">
          {/* Controls — glass panels with belief-colored tools */}
          <motion.div variants={slideUp} className="col-span-12 lg:col-span-5 space-y-6">
            {/* Style slider */}
            <div className="spatial-card p-7">
              <div className="flex items-center justify-between mb-5">
                <span className="hud-label">Style</span>
                <span className="hud-value text-sm" style={{ color: beliefColors.salience.primary }}>{style}%</span>
              </div>
              <div className="flex items-center justify-between text-[10px] text-slate-700 mb-2 font-mono">
                <span>Calm</span>
                <span>Intense</span>
              </div>
              <input
                type="range"
                min={0}
                max={100}
                value={style}
                onChange={(e) => setStyle(Number(e.target.value))}
                className="w-full h-[3px] rounded-full bg-white/5 appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:cursor-pointer"
                style={{
                  accentColor: beliefColors.salience.primary,
                  background: `linear-gradient(90deg, ${beliefColors.salience.primary}40 ${style}%, rgba(255,255,255,0.05) ${style}%)`,
                }}
              />
            </div>

            {/* Duration */}
            <div className="spatial-card p-7">
              <span className="hud-label mb-5 block">Duration</span>
              <div className="flex gap-3">
                {DURATION_OPTIONS.map((opt) => (
                  <button
                    key={opt.value}
                    onClick={() => setDuration(opt.value)}
                    className={`flex-1 py-3 rounded-xl text-sm font-body font-medium transition-all duration-300 ${
                      duration === opt.value
                        ? "text-white"
                        : "text-slate-500 hover:text-slate-300"
                    }`}
                    style={
                      duration === opt.value
                        ? {
                            background: `linear-gradient(135deg, ${beliefColors.tempo.primary}40, ${beliefColors.tempo.primary}20)`,
                            border: `1px solid ${beliefColors.tempo.primary}30`,
                          }
                        : {
                            background: "rgba(0,0,0,0.5)",
                            backdropFilter: "blur(12px)",
                            border: "1px solid rgba(255,255,255,0.06)",
                          }
                    }
                  >
                    {opt.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Complexity slider */}
            <div className="spatial-card p-7">
              <div className="flex items-center justify-between mb-5">
                <span className="hud-label">Complexity</span>
                <span className="hud-value text-sm" style={{ color: beliefColors.consonance.primary }}>{complexity}%</span>
              </div>
              <div className="flex items-center justify-between text-[10px] text-slate-700 mb-2 font-mono">
                <span>Simple</span>
                <span>Complex</span>
              </div>
              <input
                type="range"
                min={0}
                max={100}
                value={complexity}
                onChange={(e) => setComplexity(Number(e.target.value))}
                className="w-full h-[3px] rounded-full bg-white/5 appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:cursor-pointer"
                style={{
                  accentColor: beliefColors.consonance.primary,
                  background: `linear-gradient(90deg, ${beliefColors.consonance.primary}40 ${complexity}%, rgba(255,255,255,0.05) ${complexity}%)`,
                }}
              />
            </div>

            {/* Generate button */}
            <Button
              variant="primary"
              size="lg"
              className="w-full"
              onClick={handleGenerate}
              disabled={genState === "generating"}
            >
              {genState === "generating" ? (
                <>
                  <Loader2 size={20} className="mr-2 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <Wand2 size={20} className="mr-2" />
                  Compose
                </>
              )}
            </Button>
          </motion.div>

          {/* Output area — glass panel */}
          <motion.div variants={slideUp} className="col-span-12 lg:col-span-7">
            <div className="spatial-card p-8 min-h-[520px] flex flex-col glow-border">
              <span className="hud-label mb-6">Output</span>

              <AnimatePresence mode="wait">
                {genState === "idle" && (
                  <motion.div
                    key="idle"
                    {...scaleIn}
                    exit={{ opacity: 0, scale: 0.95 }}
                    className="flex-1 flex flex-col items-center justify-center text-center"
                  >
                    <div className="w-20 h-20 rounded-full flex items-center justify-center mb-6"
                      style={{ background: "rgba(0,0,0,0.5)", backdropFilter: "blur(12px)", border: "1px solid rgba(255,255,255,0.06)" }}
                    >
                      <Play size={28} className="text-slate-600 ml-1" />
                    </div>
                    <p className="text-slate-600 text-sm font-body font-light">Configure your parameters and hit Generate</p>
                    <p className="text-slate-700 text-xs mt-2 font-body font-light">Your mind profile will influence the output</p>
                  </motion.div>
                )}

                {genState === "generating" && (
                  <motion.div
                    key="generating"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="flex-1 flex flex-col items-center justify-center"
                  >
                    <div className="w-full max-w-sm">
                      <div className="flex items-center justify-between text-sm mb-3">
                        <span className="text-slate-500 font-body font-light">Processing through your mind...</span>
                        <span className="hud-value text-sm" style={{ color: beliefColors.familiarity.primary }}>{Math.round(progress)}%</span>
                      </div>
                      <div className="w-full h-[2px] rounded-full bg-white/5 overflow-hidden">
                        <motion.div
                          className="h-full rounded-full"
                          style={{
                            width: `${progress}%`,
                            background: `linear-gradient(90deg, ${beliefColors.consonance.primary}, ${beliefColors.tempo.primary})`,
                          }}
                        />
                      </div>
                      <div className="mt-6 text-[10px] text-slate-700 text-center space-y-1.5 font-mono">
                        {progress > 20 && <p>Analyzing mind axes...</p>}
                        {progress > 45 && <p>Mapping persona to tonal space...</p>}
                        {progress > 70 && <p>Rendering waveform...</p>}
                        {progress > 90 && <p>Finalizing...</p>}
                      </div>
                    </div>
                  </motion.div>
                )}

                {genState === "done" && (
                  <motion.div
                    key="done"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    className="flex-1 flex flex-col"
                  >
                    {/* Mock waveform with belief colors */}
                    <div className="flex-1 flex items-end justify-center gap-[2px] px-4 pb-8">
                      {Array.from({ length: 80 }, (_, i) => {
                        const center = 40;
                        const dist = Math.abs(i - center) / center;
                        const base = (1 - dist * 0.6) * (0.4 + Math.random() * 0.6);
                        const height = Math.max(8, base * 200);
                        return (
                          <motion.div
                            key={i}
                            initial={{ height: 0 }}
                            animate={{ height }}
                            transition={{ duration: 0.5, delay: i * 0.01 }}
                            className="w-1 rounded-full"
                            style={{
                              backgroundColor: accentColor,
                              opacity: 0.15 + base * 0.5,
                            }}
                          />
                        );
                      })}
                    </div>

                    {/* Metadata */}
                    <div className="border-t border-white/5 pt-5">
                      <div className="flex items-center justify-between">
                        <div>
                          <h4 className="text-sm font-body font-medium text-slate-300 mb-2">Mind Generation #1</h4>
                          <div className="flex items-center gap-2">
                            <span className="hud-label">{duration}s</span>
                            <span className="text-slate-700">|</span>
                            <span className="hud-label" style={{ color: `${beliefColors.salience.primary}80` }}>
                              {style > 60 ? "Intense" : style > 30 ? "Balanced" : "Calm"}
                            </span>
                            <span className="text-slate-700">|</span>
                            <span className="hud-label" style={{ color: `${beliefColors.consonance.primary}80` }}>
                              {complexity > 60 ? "Complex" : complexity > 30 ? "Moderate" : "Simple"}
                            </span>
                          </div>
                        </div>
                        <Button variant="glass" size="sm">
                          <Share2 size={14} className="mr-2" />
                          Share
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
