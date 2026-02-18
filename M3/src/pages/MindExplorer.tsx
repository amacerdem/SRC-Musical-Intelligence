import { useState, useRef } from "react";
import { motion } from "framer-motion";
import { Eye, EyeOff } from "lucide-react";
import { useUserStore } from "@/stores/useUserStore";
import { getPersona } from "@/data/personas";
import { aeProfile } from "@/data/ae-mind";
import { MindRadar } from "@/components/mind/MindRadar";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { MindOrganismCanvas, type OrganismHandle } from "@/components/mind/MindOrganismCanvas";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { pageTransition, staggerChildren, slideUp, fadeIn } from "@/design/animations";
import { beliefColors } from "@/design/tokens";
import { useScrollBatch } from "@/hooks/useScrollTrigger";
import type { MindAxes } from "@/types/mind";

const AXIS_META: { key: keyof MindAxes; label: string; shortLabel: string; description: string; belief: keyof typeof beliefColors; beliefIndex: number }[] = [
  {
    key: "entropyTolerance",
    label: "Entropy Tolerance",
    shortLabel: "ENT",
    description: "Your capacity to enjoy unpredictable, chaotic musical structures. High values mean dissonance and randomness feel stimulating rather than uncomfortable.",
    belief: "consonance",
    beliefIndex: 0,
  },
  {
    key: "resolutionCraving",
    label: "Resolution Craving",
    shortLabel: "RES",
    description: "How strongly you need musical tension to resolve. High values mean unresolved chords and deceptive cadences create genuine frustration.",
    belief: "tempo",
    beliefIndex: 1,
  },
  {
    key: "monotonyTolerance",
    label: "Monotony Tolerance",
    shortLabel: "MON",
    description: "Your ability to find depth in repetition. High values mean looping patterns feel meditative rather than boring.",
    belief: "familiarity",
    beliefIndex: 3,
  },
  {
    key: "salienceSensitivity",
    label: "Salience Sensitivity",
    shortLabel: "SAL",
    description: "How strongly dramatic musical moments capture your attention. High values mean you notice every dynamic shift and textural change.",
    belief: "salience",
    beliefIndex: 2,
  },
  {
    key: "tensionAppetite",
    label: "Tension Appetite",
    shortLabel: "TEN",
    description: "Your desire for musical build-up and suspense. High values mean you crave the architecture of tension — the climb before the peak.",
    belief: "reward",
    beliefIndex: 4,
  },
];

export function MindExplorer() {
  const { mind } = useUserStore();
  const persona = mind ? getPersona(mind.personaId) : null;
  const [compareMode, setCompareMode] = useState(false);
  const axisGridRef = useRef<HTMLDivElement>(null);
  const organismRef = useRef<OrganismHandle>(null);
  useScrollBatch(".scroll-item", axisGridRef, { stagger: 0.06 });

  if (!mind || !persona) {
    return (
      <motion.div {...pageTransition} className="flex items-center justify-center h-96 bg-black">
        <p className="text-slate-500 text-lg font-body font-light">Complete onboarding to explore your mind.</p>
      </motion.div>
    );
  }

  const aePersona = getPersona(aeProfile.mind.personaId);

  return (
    <motion.div {...pageTransition} className="min-h-screen bg-black pb-16 relative overflow-hidden">
      {/* Cinematic vignette */}
      <div className="cinematic-vignette" />

      {/* Organism background with constellations — neural network feel */}
      <div className="absolute inset-0 z-0 opacity-[0.10] pointer-events-none">
        <MindOrganismCanvas
          ref={organismRef}
          color={persona.color}
          secondaryColor={beliefColors.consonance.primary}
          stage={2}
          intensity={0.3}
          breathRate={6}
          variant="ambient"
          constellations
          className="w-full h-full"
          interactive={false}
        />
      </div>

      {/* Header */}
      <motion.div variants={fadeIn} initial="initial" animate="animate" className="relative z-10 flex items-center justify-between mb-12 pt-4">
        <div>
          <span className="hud-label mb-2 block">Cognitive Profile</span>
          <h1 className="text-4xl font-display font-bold text-slate-100 tracking-tight">Mind Explorer</h1>
          <p className="hud-label mt-2">Deep dive into your cognitive musical profile</p>
        </div>
        <Button
          variant={compareMode ? "primary" : "glass"}
          size="sm"
          onClick={() => setCompareMode(!compareMode)}
        >
          {compareMode ? <EyeOff size={16} className="mr-2" /> : <Eye size={16} className="mr-2" />}
          {compareMode ? "Hide Compare" : "Compare with AE"}
        </Button>
      </motion.div>

      <motion.div variants={staggerChildren} initial="initial" animate="animate" className="relative z-10">
        {/* Central Radar — dominant element */}
        <motion.div variants={slideUp} className="flex flex-col items-center mb-16">
          <div className="relative">
            {/* Organism glow behind radar */}
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
              <div className="w-[460px] h-[460px] opacity-15">
                <MindOrganismCanvas
                  color={persona.color}
                  stage={1}
                  intensity={0.4}
                  breathRate={4}
                  variant="glow"
                  frozen
                  className="w-full h-full"
                  interactive={false}
                />
              </div>
            </div>

            <div className="relative rounded-3xl p-10 flex flex-col items-center"
              style={{ background: "rgba(0,0,0,0.5)", backdropFilter: "blur(12px)", border: "1px solid rgba(255,255,255,0.06)" }}
            >
              <div className="flex items-center gap-4 mb-8">
                <Badge label={persona.name} color={persona.color} size="md" />
                {compareMode && (
                  <Badge label={aePersona.name} color={aePersona.color} size="md" />
                )}
              </div>

              <MindRadar
                axes={mind.axes}
                color={persona.color}
                compareAxes={compareMode ? aeProfile.mind.axes : undefined}
                compareColor={compareMode ? aePersona.color : undefined}
                size={460}
              />

              {compareMode && (
                <div className="flex items-center gap-8 mt-8 text-sm">
                  <div className="flex items-center gap-2">
                    <NucleusDot color={persona.color} size={5} active pulsing />
                    <span className="text-slate-500 font-body font-light">You</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <NucleusDot color={aePersona.color} size={5} active />
                    <span className="text-slate-500 font-body font-light">Amac Erdem</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </motion.div>

        {/* Floating axis detail panels */}
        <div ref={axisGridRef} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6 px-2">
          {AXIS_META.map((axis, index) => {
            const value = mind.axes[axis.key];
            const pct = Math.round(value * 100);
            const aeValue = aeProfile.mind.axes[axis.key];
            const aePct = Math.round(aeValue * 100);
            const beliefColor = beliefColors[axis.belief].primary;

            return (
              <div
                key={axis.key}
                className="scroll-item spatial-card group relative p-6"
                style={{ "--glow-color": beliefColor } as React.CSSProperties}
                onMouseEnter={() => {
                  organismRef.current?.highlightBelief(axis.beliefIndex, 0.8);
                }}
                onMouseLeave={() => {
                  organismRef.current?.highlightBelief(axis.beliefIndex, 0);
                }}
              >
                {/* HUD label with NucleusDot */}
                <div className="flex items-center gap-2 mb-3">
                  <NucleusDot color={beliefColor} size={4} active />
                  <span className="hud-label">{axis.shortLabel}</span>
                </div>

                {/* Value display */}
                <div className="flex items-baseline justify-between mb-2">
                  <h4 className="text-sm font-body font-semibold text-slate-300 group-hover:text-slate-200 transition-colors">
                    {axis.label}
                  </h4>
                  <span className="hud-value text-lg font-bold" style={{ color: beliefColor }}>
                    {pct}
                  </span>
                </div>

                {/* Thin atmospheric bar */}
                <div className="w-full h-[3px] rounded-full bg-white/5 mb-4 overflow-hidden">
                  <motion.div
                    className="h-full rounded-full"
                    style={{ backgroundColor: beliefColor }}
                    initial={{ width: 0 }}
                    animate={{ width: `${pct}%` }}
                    transition={{ duration: 1, ease: [0.22, 1, 0.36, 1], delay: index * 0.1 }}
                  />
                </div>

                {/* Description */}
                <p className="text-[11px] text-slate-600 leading-relaxed font-body font-light">{axis.description}</p>

                {/* Compare overlay */}
                {compareMode && (
                  <div className="mt-4 pt-3 border-t border-white/5">
                    <div className="flex items-center justify-between text-xs mb-1.5">
                      <span className="text-slate-600 font-body">AE</span>
                      <span className="hud-value text-xs" style={{ color: aePersona.color }}>{aePct}</span>
                    </div>
                    <div className="w-full h-[2px] rounded-full bg-white/5 overflow-hidden">
                      <motion.div
                        className="h-full rounded-full"
                        style={{ backgroundColor: aePersona.color }}
                        initial={{ width: 0 }}
                        animate={{ width: `${aePct}%` }}
                        transition={{ duration: 0.8, ease: "easeOut", delay: 0.3 }}
                      />
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </motion.div>
    </motion.div>
  );
}
