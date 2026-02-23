import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { motion } from "framer-motion";
import { ArrowLeft, Flame, Headphones, TrendingUp, Crown, Sparkles } from "lucide-react";
import { aeMind, aeProfile } from "@/data/ae-mind";
import { getPersona } from "@/data/personas";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { MindRadar } from "@/components/mind/MindRadar";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { pageTransition, staggerChildren, slideUp, cinematicReveal, kineticContainer, kineticChar } from "@/design/animations";
import { beliefColors } from "@/design/tokens";
import { STAGE_NAMES } from "@/types/mind";

const AE_COLOR = "#6C5CE7";

export function ExploreAE() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const persona = getPersona(aeMind.personaId);

  const quoteText = t("exploreAE.quote");

  return (
    <motion.div {...pageTransition} className="min-h-screen bg-black relative overflow-hidden">
      {/* Full-screen organism background — FULL BACKGROUND, not in card */}
      <div className="absolute inset-0 pointer-events-none">
        <MindOrganismCanvas
          color={AE_COLOR}
          stage={3}
          intensity={0.6}
          breathRate={4}
          className="w-full h-full"
        />
      </div>

      {/* Cinematic vignette */}
      <div className="cinematic-vignette" />

      {/* Ambient glow */}
      <div
        className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full blur-[200px] opacity-10 pointer-events-none"
        style={{ backgroundColor: AE_COLOR }}
      />

      {/* Back button */}
      <div className="absolute top-8 left-8 z-20">
        <Button variant="ghost" size="sm" onClick={() => navigate("/")}>
          <ArrowLeft size={18} className="mr-2" />
          {t("common.back")}
        </Button>
      </div>

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center justify-start min-h-screen px-8 pt-28 pb-20">
        <motion.div
          variants={staggerChildren}
          initial="initial"
          animate="animate"
          className="w-full max-w-5xl"
        >
          {/* Hero section */}
          <motion.div variants={cinematicReveal} className="text-center mb-6">
            <span className="hud-label mb-4 block">{t("exploreAE.stageLabel")}</span>
            <h1 className="text-5xl md:text-7xl font-display font-bold mt-2 mb-4 text-gradient tracking-tight"
              style={{ "--tw-gradient-from": AE_COLOR, "--tw-gradient-to": `${AE_COLOR}80` } as React.CSSProperties}
            >
              Amac Erdem
            </h1>
            <p className="hud-label tracking-wide text-base">{t("exploreAE.mindBehindEngine")}</p>
          </motion.div>

          {/* Quote — hero text with kinetic character-by-character reveal */}
          <motion.div
            variants={kineticContainer}
            initial="initial"
            animate="animate"
            className="text-center mb-20 mt-12"
          >
            <blockquote className="relative inline-block max-w-2xl">
              <div className="absolute -left-8 -top-6 text-5xl font-display opacity-20" style={{ color: AE_COLOR }}>"</div>
              <p className="text-3xl md:text-4xl font-display font-light text-slate-300 italic leading-relaxed px-10">
                {quoteText.split("").map((char, i) => (
                  <motion.span key={i} variants={kineticChar} className="inline-block" style={{ whiteSpace: char === " " ? "pre" : undefined }}>
                    {char}
                  </motion.span>
                ))}
              </p>
              <div className="absolute -right-8 -bottom-6 text-5xl font-display opacity-20" style={{ color: AE_COLOR }}>"</div>
            </blockquote>
          </motion.div>

          {/* Spatial layout — radar + floating info panels */}
          <div className="relative">
            {/* Radar — large and centered */}
            <motion.div variants={slideUp} className="flex justify-center mb-16">
              <div className="rounded-3xl p-10 flex flex-col items-center"
                style={{ background: "rgba(0,0,0,0.5)", backdropFilter: "blur(12px)", border: "1px solid rgba(255,255,255,0.06)" }}
              >
                <span className="hud-label mb-6">{t("exploreAE.mindProfile")}</span>
                <MindRadar axes={aeProfile.mind.axes} color={AE_COLOR} size={500} />
              </div>
            </motion.div>

            {/* Floating glass panels */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
              {/* Persona */}
              <motion.div variants={slideUp} className="spatial-card p-8">
                <div className="flex items-center gap-4 mb-5">
                  <div
                    className="w-14 h-14 rounded-2xl flex items-center justify-center"
                    style={{
                      background: `linear-gradient(135deg, ${AE_COLOR}20, ${AE_COLOR}08)`,
                      border: `1px solid ${AE_COLOR}25`,
                    }}
                  >
                    <Crown size={24} style={{ color: AE_COLOR }} />
                  </div>
                  <div>
                    <h3 className="text-xl font-display font-bold text-slate-200">{t(`personas.${persona.id}.name`)}</h3>
                    <p className="text-sm text-slate-600 italic font-body font-light">"{t(`personas.${persona.id}.tagline`)}"</p>
                  </div>
                </div>
                <p className="text-sm text-slate-500 leading-relaxed font-body font-light">{t(`personas.${persona.id}.description`)}</p>
              </motion.div>

              {/* Stats — HUD style */}
              <motion.div variants={slideUp} className="spatial-card p-8">
                <span className="hud-label mb-6 block">{t("exploreAE.stats")}</span>
                <div className="grid grid-cols-2 gap-5">
                  <StatBlock icon={<TrendingUp size={14} />} label={t("exploreAE.level")} value="50" color={AE_COLOR} />
                  <StatBlock icon={<Headphones size={14} />} label={t("exploreAE.tracks")} value="12,847" color={AE_COLOR} />
                  <StatBlock icon={<Flame size={14} />} label={t("exploreAE.streak")} value="365 days" color={AE_COLOR} />
                  <StatBlock icon={<Sparkles size={14} />} label={t("exploreAE.stage")} value={t(`stages.${aeMind.stage}`)} color={AE_COLOR} />
                </div>
              </motion.div>

              {/* Belief Traces — glass panels with belief colors */}
              <motion.div variants={slideUp} className="spatial-card p-8">
                <span className="hud-label mb-5 block">{t("exploreAE.beliefSignature")}</span>
                <div className="space-y-4">
                  {(Object.keys(beliefColors) as (keyof typeof beliefColors)[]).map((belief) => {
                    const color = beliefColors[belief].primary;
                    const mockVal = belief === "consonance" ? 0.82 : belief === "tempo" ? 0.65 : belief === "salience" ? 0.91 : belief === "familiarity" ? 0.78 : 0.88;
                    const pct = Math.round(mockVal * 100);
                    return (
                      <div key={belief}>
                        <div className="flex items-center justify-between mb-1.5">
                          <div className="flex items-center gap-2">
                            <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: color }} />
                            <span className="text-xs font-body font-medium text-slate-400">{t(`beliefs.${belief}`)}</span>
                          </div>
                          <span className="hud-value text-xs" style={{ color }}>{pct}</span>
                        </div>
                        <div className="w-full h-[3px] rounded-full bg-white/5 overflow-hidden">
                          <motion.div
                            className="h-full rounded-full"
                            style={{ backgroundColor: color }}
                            initial={{ width: 0 }}
                            animate={{ width: `${pct}%` }}
                            transition={{ duration: 1, ease: [0.22, 1, 0.36, 1] }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </motion.div>

              {/* Famous Minds */}
              <motion.div variants={slideUp} className="spatial-card p-8">
                <span className="hud-label mb-5 block">{t("exploreAE.famousMinds")}</span>
                <div className="flex flex-wrap gap-2">
                  {persona.famousMinds.map((name) => (
                    <span
                      key={name}
                      className="px-3 py-1.5 rounded-lg text-xs font-body font-medium text-slate-400"
                      style={{
                        background: `${AE_COLOR}08`,
                        border: `1px solid ${AE_COLOR}15`,
                      }}
                    >
                      {name}
                    </span>
                  ))}
                </div>
              </motion.div>
            </div>
          </div>

          {/* CTA */}
          <motion.div variants={slideUp} className="text-center mt-20">
            <Button variant="primary" size="lg" onClick={() => navigate("/onboarding")}>
              {t("exploreAE.createYourMind")}
            </Button>
          </motion.div>
        </motion.div>
      </div>
    </motion.div>
  );
}

function StatBlock({ icon, label, value, color }: { icon: React.ReactNode; label: string; value: string; color: string }) {
  return (
    <div className="flex flex-col gap-1">
      <div className="flex items-center gap-1.5">
        <span style={{ color }} className="opacity-60">{icon}</span>
        <span className="hud-label">{label}</span>
      </div>
      <span className="hud-value text-lg text-slate-200">{value}</span>
    </div>
  );
}
