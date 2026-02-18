import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowRight } from "lucide-react";
import { useUserStore } from "@/stores/useUserStore";
import { getPersona } from "@/data/personas";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { MindRadar } from "@/components/mind/MindRadar";
import { beliefColors } from "@/design/tokens";

type RevealPhase = "void" | "birth" | "name" | "radar" | "ready";

export function MindReveal() {
  const navigate = useNavigate();
  const { mind, displayName } = useUserStore();
  const [phase, setPhase] = useState<RevealPhase>("void");

  const persona = mind ? getPersona(mind.personaId) : null;

  useEffect(() => {
    if (!mind) { navigate("/"); return; }
    const timers = [
      setTimeout(() => setPhase("birth"), 1200),
      setTimeout(() => setPhase("name"), 3500),
      setTimeout(() => setPhase("radar"), 6500),
      setTimeout(() => setPhase("ready"), 8500),
    ];
    return () => timers.forEach(clearTimeout);
  }, [mind, navigate]);

  if (!persona || !mind) return null;

  const color = persona.color;

  return (
    <div className="fixed inset-0 bg-black overflow-hidden">
      <div className="cinematic-vignette" />

      {/* Conic gradient trails per belief */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        {phase !== "void" && (["consonance", "tempo", "salience", "familiarity", "reward"] as const).map((b, i) => {
          const bColor = beliefColors[b].primary;
          const radius = 150 + i * 40;
          return (
            <motion.div
              key={b}
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 0.15, scale: 1 }}
              transition={{ duration: 2, delay: i * 0.2, ease: [0.22, 1, 0.36, 1] }}
              className="absolute rounded-full"
              style={{
                width: radius * 2, height: radius * 2,
                background: `conic-gradient(from ${i * 72}deg, ${bColor}20, transparent 20%, transparent 100%)`,
                maskImage: `radial-gradient(transparent ${radius - 2}px, black ${radius - 1}px, black ${radius + 1}px, transparent ${radius + 2}px)`,
                WebkitMaskImage: `radial-gradient(transparent ${radius - 2}px, black ${radius - 1}px, black ${radius + 1}px, transparent ${radius + 2}px)`,
                animation: `orbit ${28 + i * 4}s linear infinite`,
              }}
            />
          );
        })}
      </div>

      {/* Organism explodes from center */}
      <AnimatePresence>
        {phase !== "void" && (
          <motion.div
            initial={{ opacity: 0, scale: 0.05 }}
            animate={{ opacity: phase === "ready" ? 0.5 : 0.3, scale: 1 }}
            transition={{ duration: 3, ease: [0.22, 1, 0.36, 1] }}
            className="absolute inset-0"
          >
            <MindOrganismCanvas
              color={color}
              stage={phase === "ready" || phase === "radar" ? 2 : 1}
              intensity={phase === "ready" ? 0.8 : 0.5}
              breathRate={3}
              className="w-full h-full"
              interactive={false}
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Color wash */}
      <motion.div
        className="absolute inset-0 pointer-events-none"
        initial={{ opacity: 0 }}
        animate={{ opacity: phase !== "void" ? 1 : 0 }}
        transition={{ duration: 2 }}
        style={{ background: `radial-gradient(ellipse 60% 50% at 50% 45%, ${color}08, transparent 70%)` }}
      />

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center justify-center h-full px-6">
        <AnimatePresence>
          {phase === "void" && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 0.3 }} exit={{ opacity: 0 }} transition={{ duration: 0.8 }}>
              <motion.span animate={{ opacity: [0.2, 0.5, 0.2] }} transition={{ duration: 2, repeat: Infinity }} className="text-sm text-slate-700 font-display font-light">
                Preparing your mind...
              </motion.span>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Name — character-by-character */}
        <AnimatePresence>
          {(phase === "name" || phase === "radar" || phase === "ready") && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }} className="text-center">
              <motion.p initial={{ opacity: 0, y: 10 }} animate={{ opacity: 0.3, y: 0 }} transition={{ duration: 1 }} className="hud-label mb-5">
                {displayName && displayName !== "You" ? `${displayName}, you are a` : "You are a"}
              </motion.p>

              <h1 className="text-5xl md:text-7xl lg:text-8xl font-display font-bold mb-4 leading-none flex justify-center flex-wrap">
                {persona.name.split("").map((char, i) => (
                  <motion.span
                    key={i}
                    initial={{ opacity: 0, y: 50, scale: 0.3, filter: "blur(15px)" }}
                    animate={{ opacity: 1, y: 0, scale: 1, filter: "blur(0px)" }}
                    transition={{ duration: 0.7, delay: i * 0.06, ease: [0.22, 1, 0.36, 1] }}
                    style={{ color, display: "inline-block" }}
                  >
                    {char === " " ? "\u00A0" : char}
                  </motion.span>
                ))}
              </h1>

              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 0.4 }}
                transition={{ delay: persona.name.length * 0.06 + 0.5, duration: 1 }}
                className="text-lg text-slate-500 font-display font-light italic"
              >
                {persona.tagline}
              </motion.p>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Radar */}
        <AnimatePresence>
          {(phase === "radar" || phase === "ready") && (
            <motion.div
              initial={{ opacity: 0, scale: 0.6, filter: "blur(15px)" }}
              animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
              transition={{ duration: 1.2, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
              className="mt-10"
            >
              <MindRadar axes={mind.axes} color={color} size={240} />
            </motion.div>
          )}
        </AnimatePresence>

        {/* CTA */}
        <AnimatePresence>
          {phase === "ready" && (
            <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 1, delay: 0.5 }} className="mt-10 text-center">
              <p className="text-sm text-slate-500 mb-2 max-w-sm mx-auto leading-relaxed font-light">{persona.description}</p>
              <motion.p initial={{ opacity: 0 }} animate={{ opacity: 0.3 }} transition={{ delay: 1, duration: 1.5 }} className="hud-label mb-8">
                This is your Musical Mind
              </motion.p>
              <button
                onClick={() => navigate("/dashboard")}
                className="group relative px-8 py-3.5 rounded-full transition-all duration-500 hover:scale-[1.03]"
                style={{ background: `${color}08`, border: `1px solid ${color}20` }}
                onMouseEnter={(e) => { e.currentTarget.style.background = `${color}18`; e.currentTarget.style.boxShadow = `0 0 40px ${color}15`; }}
                onMouseLeave={(e) => { e.currentTarget.style.background = `${color}08`; e.currentTarget.style.boxShadow = "none"; }}
              >
                <span className="text-sm font-display font-medium text-slate-200">Enter Your Mind</span>
                <ArrowRight size={16} className="inline ml-2 text-slate-400 group-hover:translate-x-1 transition-transform" />
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
