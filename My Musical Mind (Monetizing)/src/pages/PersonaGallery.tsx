import { useRef } from "react";
import { motion } from "framer-motion";
import { personas } from "@/data/personas";
import { PersonaCard } from "@/components/mind/PersonaCard";
import { pageTransition, fadeIn } from "@/design/animations";
import { useScrollBatch } from "@/hooks/useScrollTrigger";

export function PersonaGallery() {
  const gridRef = useRef<HTMLDivElement>(null);
  useScrollBatch(".scroll-item", gridRef, { stagger: 0.06 });

  return (
    <motion.div {...pageTransition} className="min-h-screen bg-black pb-16 relative overflow-hidden">
      {/* Cinematic vignette */}
      <div className="cinematic-vignette" />

      {/* Header */}
      <motion.div variants={fadeIn} initial="initial" animate="animate" className="relative z-10 text-center mb-16 pt-8">
        <span className="hud-label mb-3 block">Persona Atlas</span>
        <h1 className="text-4xl md:text-5xl font-display font-bold text-slate-100 tracking-tight mb-4">
          24 Musical Minds
        </h1>
        <p className="hud-label max-w-lg mx-auto leading-relaxed text-xs">
          Each persona represents a unique region in the cognitive parameter space.
          No mind is better or worse — only different.
        </p>
      </motion.div>

      {/* Atmospheric masonry-style layout */}
      <div
        ref={gridRef}
        className="relative z-10 columns-1 sm:columns-2 lg:columns-3 xl:columns-4 gap-5 space-y-5 px-2"
      >
        {personas.map((persona, index) => (
          <div
            key={persona.id}
            className="scroll-item break-inside-avoid group"
            style={{
              paddingTop: index % 3 === 1 ? "8px" : "0px",
            }}
          >
            <div
              className="spatial-card p-0 overflow-hidden transition-all duration-500 group-hover:shadow-lg"
              style={{
                "--glow-color": persona.color,
                boxShadow: "0 0 0 rgba(0,0,0,0)",
              } as React.CSSProperties}
              onMouseEnter={(e) => {
                (e.currentTarget as HTMLElement).style.boxShadow =
                  `0 0 30px ${persona.color}20, 0 0 60px ${persona.color}15, 0 0 100px ${persona.color}08`;
              }}
              onMouseLeave={(e) => {
                (e.currentTarget as HTMLElement).style.boxShadow = "0 0 0 rgba(0,0,0,0)";
              }}
            >
              <PersonaCard persona={persona} />
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
