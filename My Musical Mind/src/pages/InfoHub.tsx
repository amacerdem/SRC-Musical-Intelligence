import { useRef } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";
import { useTranslation } from "react-i18next";
import { personas } from "@/data/personas";
import { PersonaCard } from "@/components/mind/PersonaCard";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { pageTransition, fadeIn, staggerChildren, slideUp } from "@/design/animations";
import { beliefColors } from "@/design/tokens";
import { useScrollBatch } from "@/hooks/useScrollTrigger";

const ENGINE_COLOR = "#6C5CE7";

const ENGINE_STATS = [
  { value: "97", labelKey: "infoHub.stats.perceptualDimensions", color: beliefColors.consonance.primary },
  { value: "5", labelKey: "infoHub.stats.cognitiveBeliefs", color: beliefColors.reward.primary },
  { value: "32", labelKey: "infoHub.stats.temporalHorizons", color: beliefColors.tempo.primary },
  { value: "24", labelKey: "infoHub.stats.morphologies", color: beliefColors.salience.primary },
];

export function InfoHub() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const gridRef = useRef<HTMLDivElement>(null);
  useScrollBatch(".scroll-item", gridRef, { stagger: 0.06 });

  return (
    <motion.div {...pageTransition} className="min-h-screen bg-black pb-16 relative overflow-hidden">
      {/* Organism background */}
      <div className="absolute inset-0 z-0 opacity-[0.06] pointer-events-none">
        <MindOrganismCanvas
          color={ENGINE_COLOR}
          secondaryColor={beliefColors.consonance.primary}
          stage={3}
          intensity={0.15}
          breathRate={8}
          variant="ambient"
          className="w-full h-full"
          interactive={false}
        />
      </div>

      {/* Cinematic vignette */}
      <div className="cinematic-vignette" />

      {/* Header */}
      <motion.div variants={fadeIn} initial="initial" animate="animate" className="relative z-10 text-center mb-14 pt-8">
        <span className="hud-label mb-3 block">{t("infoHub.hudLabel")}</span>
        <h1 className="text-4xl md:text-5xl font-display font-bold text-slate-100 tracking-tight mb-3">
          {t("infoHub.title")}
        </h1>
        <p className="hud-label max-w-lg mx-auto leading-relaxed text-xs">
          {t("infoHub.subtitle")}
        </p>
      </motion.div>

      <motion.div variants={staggerChildren} initial="initial" animate="animate" className="relative z-10">
        {/* Engine Section */}
        <motion.div variants={slideUp} className="max-w-4xl xl:max-w-5xl 2xl:max-w-6xl mx-auto mb-16 px-4">
          <div
            className="spatial-card p-8 relative overflow-hidden"
            style={{ "--glow-color": ENGINE_COLOR } as React.CSSProperties}
          >
            {/* Ambient glow */}
            <div
              className="absolute -top-20 -right-20 w-60 h-60 rounded-full blur-[100px] opacity-10 pointer-events-none"
              style={{ backgroundColor: ENGINE_COLOR }}
            />

            <div className="relative z-10">
              <div className="flex items-center gap-2 mb-5">
                <NucleusDot color={ENGINE_COLOR} size={5} active pulsing />
                <span className="hud-label">{t("infoHub.engineLabel")}</span>
              </div>

              <p className="text-sm text-slate-400 leading-relaxed font-body font-light mb-6 max-w-2xl">
                {t("infoHub.engineDescription")}
              </p>

              {/* Stats row */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                {ENGINE_STATS.map((stat) => (
                  <div key={stat.labelKey} className="text-center">
                    <div className="hud-value text-2xl mb-1" style={{ color: stat.color }}>
                      {stat.value}
                    </div>
                    <div className="hud-label text-[9px]">{t(stat.labelKey)}</div>
                  </div>
                ))}
              </div>

              {/* AE link */}
              <button
                onClick={() => navigate("/explore-ae")}
                className="group flex items-center gap-2 px-5 py-2.5 rounded-full transition-all duration-500 hover:scale-[1.03]"
                style={{
                  background: `${ENGINE_COLOR}08`,
                  border: `1px solid ${ENGINE_COLOR}15`,
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = `${ENGINE_COLOR}18`;
                  e.currentTarget.style.borderColor = `${ENGINE_COLOR}30`;
                  e.currentTarget.style.boxShadow = `0 0 30px ${ENGINE_COLOR}10`;
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = `${ENGINE_COLOR}08`;
                  e.currentTarget.style.borderColor = `${ENGINE_COLOR}15`;
                  e.currentTarget.style.boxShadow = "none";
                }}
              >
                <span className="text-xs font-display font-medium text-slate-500 group-hover:text-slate-200 transition-colors">
                  {t("infoHub.exploreAE")}
                </span>
                <ArrowRight
                  size={14}
                  className="text-slate-700 group-hover:text-slate-400 group-hover:translate-x-1 transition-all"
                />
              </button>
            </div>
          </div>
        </motion.div>

        {/* Persona Atlas */}
        <motion.div variants={slideUp} className="px-4">
          <div className="text-center mb-10">
            <span className="hud-label mb-2 block">{t("infoHub.personaAtlas")}</span>
            <h2 className="text-2xl font-display font-bold text-slate-200 mb-2">
              {t("infoHub.personaAtlasTitle")}
            </h2>
            <p className="hud-label max-w-md mx-auto leading-relaxed text-xs">
              {t("infoHub.personaAtlasSubtitle")}
            </p>
          </div>

          <div
            ref={gridRef}
            className="columns-1 sm:columns-2 lg:columns-3 xl:columns-4 gap-5 space-y-5"
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
      </motion.div>
    </motion.div>
  );
}
