import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { OrbitalBeliefs } from "@/components/landing/OrbitalBeliefs";

const INSTITUTIONS = [
  { name: "MIT", dept: "Media Lab" },
  { name: "Stanford", dept: "CCRMA" },
  { name: "CMU", dept: "School of Music" },
];

export function Landing() {
  const navigate = useNavigate();

  return (
    <div className="fixed inset-0 bg-black overflow-hidden">
      {/* Living organism background */}
      <div className="absolute inset-0 z-0">
        <MindOrganismCanvas
          color="#7C3AED"
          secondaryColor="#6366F1"
          stage={2}
          intensity={0.6}
          breathRate={5}
          className="w-full h-full"
          interactive
        />
      </div>

      {/* Orbital beliefs — ambient decoration */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none z-[1]">
        <OrbitalBeliefs visible size={Math.min(600, typeof window !== "undefined" ? window.innerWidth * 0.85 : 600)} />
      </div>

      {/* Cinematic vignette */}
      <div className="cinematic-vignette" />

      {/* Content */}
      <div className="relative z-10 h-full flex flex-col items-center justify-center px-6">
        {/* M³ Title */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8, filter: "blur(20px)" }}
          animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
          transition={{ duration: 2, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
        >
          <h1 className="relative text-center">
            <span className="inline-block">
              <span
                className="text-[clamp(5rem,14vw,16rem)] font-display font-bold leading-none tracking-tighter"
                style={{
                  background: "linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(139,92,246,0.6) 50%, rgba(99,102,241,0.15) 100%)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                }}
              >
                M
              </span>
              <span
                className="text-[clamp(3rem,9vw,10rem)] font-display font-bold leading-none align-super"
                style={{
                  background: "linear-gradient(180deg, rgba(255,255,255,0.9) 0%, rgba(139,92,246,0.5) 100%)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                }}
              >
                3
              </span>
            </span>
            <div
              className="absolute inset-0 pointer-events-none"
              style={{
                background: "radial-gradient(ellipse at 50% 60%, rgba(139,92,246,0.15) 0%, transparent 60%)",
                filter: "blur(60px)",
              }}
            />
          </h1>
        </motion.div>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 0.6, y: 0 }}
          transition={{ duration: 1.5, delay: 1, ease: [0.22, 1, 0.36, 1] }}
          className="text-lg md:text-xl text-slate-400 font-display font-light tracking-[0.2em] mt-4 mb-14"
        >
          MY MUSICAL MIND
        </motion.p>

        {/* CTA Button */}
        <motion.button
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 1.8, ease: [0.22, 1, 0.36, 1] }}
          onClick={() => navigate("/onboarding")}
          className="group relative px-12 py-4 rounded-full overflow-hidden transition-all duration-500 hover:scale-[1.04]"
        >
          <div
            className="absolute inset-0 rounded-full opacity-60 group-hover:opacity-100 transition-opacity duration-500"
            style={{
              background: "linear-gradient(135deg, #6366F1, #A855F7, #EC4899)",
              padding: "1px",
            }}
          >
            <div className="w-full h-full rounded-full bg-black/90 backdrop-blur-xl" />
          </div>
          <div
            className="absolute inset-0 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-700"
            style={{
              boxShadow: "0 0 60px rgba(139,92,246,0.3), 0 0 120px rgba(99,102,241,0.1)",
            }}
          />
          <span className="relative z-10 text-sm font-display font-medium text-slate-200 group-hover:text-white transition-colors tracking-wide">
            Discover Your Mind
          </span>
        </motion.button>

        {/* Secondary link */}
        <motion.button
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 2.5 }}
          onClick={() => navigate("/explore-ae")}
          className="group mt-5 px-8 py-3 text-sm text-slate-700 hover:text-slate-400 transition-all duration-500"
        >
          <span className="border-b border-slate-800 group-hover:border-slate-600 pb-0.5 transition-colors font-display tracking-wide">
            Explore the mind behind the engine
          </span>
        </motion.button>
      </div>

      {/* ── Bottom bar: Science + Institutions + Footer ─────────── */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 2.5, duration: 2 }}
        className="absolute bottom-0 left-0 right-0 z-10 px-6 pb-5 flex items-end justify-between"
      >
        {/* Left: SRC⁹ footer */}
        <div className="flex flex-col gap-1.5">
          <span className="text-[11px] font-display font-semibold text-slate-600 tracking-wide">
            SRC<sup className="text-[8px]">9</sup>
          </span>
          <span className="text-[9px] text-slate-800 font-mono">
            &copy; 2025 Amac Erdem. All rights reserved.
          </span>
        </div>

        {/* Center: Scientific foundation */}
        <div className="hidden md:flex flex-col items-center gap-2">
          <div className="flex items-center gap-6">
            {INSTITUTIONS.map((inst) => (
              <div key={inst.name} className="flex flex-col items-center">
                <span className="text-[10px] font-display font-semibold text-slate-600 tracking-wider">
                  {inst.name}
                </span>
                <span className="text-[8px] text-slate-800 font-mono">{inst.dept}</span>
              </div>
            ))}
          </div>
          <span className="text-[9px] text-slate-800 font-mono tracking-wide">
            Built on 251 neuroscience &amp; music cognition papers
          </span>
        </div>

        {/* Right: Stats */}
        <div className="flex flex-col items-end gap-1.5">
          <span className="text-[9px] text-slate-800 font-mono tracking-wide">
            97 perceptual dimensions
          </span>
          <span className="text-[9px] text-slate-800 font-mono tracking-wide">
            5 cognitive beliefs
          </span>
          <span className="text-[9px] text-slate-800 font-mono tracking-wide">
            32 temporal horizons
          </span>
        </div>
      </motion.div>
    </div>
  );
}
