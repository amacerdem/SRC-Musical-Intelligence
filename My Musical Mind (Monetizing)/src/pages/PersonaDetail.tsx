import { useParams, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { motion } from "framer-motion";
import { ArrowLeft, Users, Sparkles } from "lucide-react";
import { getPersona, personas } from "@/data/personas";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { MindRadar } from "@/components/mind/MindRadar";
import { PersonaCard } from "@/components/mind/PersonaCard";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { pageTransition, staggerChildren, slideUp, cinematicReveal } from "@/design/animations";
import { beliefColors } from "@/design/tokens";
import type { MindAxes, EvolutionStage } from "@/types/mind";
import { STAGE_NAMES } from "@/types/mind";

const AXIS_LABELS: { key: keyof MindAxes; label: string; short: string; belief: keyof typeof beliefColors }[] = [
  { key: "entropyTolerance", label: "Entropy Tolerance", short: "ENT", belief: "consonance" },
  { key: "resolutionCraving", label: "Resolution Craving", short: "RES", belief: "tempo" },
  { key: "monotonyTolerance", label: "Monotony Tolerance", short: "MON", belief: "familiarity" },
  { key: "salienceSensitivity", label: "Salience Sensitivity", short: "SAL", belief: "salience" },
  { key: "tensionAppetite", label: "Tension Appetite", short: "TEN", belief: "reward" },
];

const STAGES: { stage: EvolutionStage; name: string }[] = [
  { stage: 1, name: STAGE_NAMES[1] },
  { stage: 2, name: STAGE_NAMES[2] },
  { stage: 3, name: STAGE_NAMES[3] },
];

export function PersonaDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { t } = useTranslation();
  const persona = getPersona(Number(id));

  if (!persona) {
    return (
      <motion.div {...pageTransition} className="flex items-center justify-center h-96 bg-black">
        <p className="text-slate-500 text-lg font-body font-light">{t("personaDetail.notFound")}</p>
      </motion.div>
    );
  }

  const compatiblePersonas = persona.compatibleWith
    .map((cid) => personas.find((p) => p.id === cid))
    .filter(Boolean) as typeof personas;

  return (
    <motion.div {...pageTransition} className="min-h-screen bg-black relative pb-16">
      {/* Full-screen organism background */}
      <div className="absolute inset-0 opacity-15 pointer-events-none">
        <MindOrganismCanvas
          color={persona.color}
          stage={2}
          intensity={0.4}
          breathRate={5}
          className="w-full h-full"
        />
      </div>

      {/* Cinematic vignette */}
      <div className="cinematic-vignette" />

      {/* Ambient glow */}
      <div
        className="absolute top-32 left-1/2 -translate-x-1/2 w-[500px] h-[500px] rounded-full blur-[180px] opacity-10 pointer-events-none"
        style={{ backgroundColor: persona.color }}
      />

      {/* Back button */}
      <div className="relative z-20 mb-8 pt-4">
        <Button variant="ghost" size="sm" onClick={() => navigate("/info")}>
          <ArrowLeft size={16} className="mr-2" />
          {t("personaDetail.allPersonas")}
        </Button>
      </div>

      <motion.div variants={staggerChildren} initial="initial" animate="animate" className="relative z-10">
        {/* Hero — persona identity floating over organism */}
        <motion.div variants={cinematicReveal} className="text-center mb-16">
          <div
            className="inline-flex items-center justify-center w-20 h-20 rounded-2xl font-display font-bold text-3xl mb-6"
            style={{
              background: `linear-gradient(135deg, ${persona.color}20, ${persona.color}08)`,
              color: persona.color,
              border: `1px solid ${persona.color}20`,
            }}
          >
            {persona.id}
          </div>
          <h1 className="text-4xl md:text-5xl font-display font-bold text-slate-100 tracking-tight mb-3">
            {t(`personas.${persona.id}.name`)}
          </h1>
          <p className="text-lg text-slate-500 italic font-body font-light mb-4">"{t(`personas.${persona.id}.tagline`)}"</p>
          <Badge label={t("common.ofListeners", { pct: persona.populationPct })} color={persona.color} size="md" />
          <p className="text-slate-500 leading-relaxed mt-6 max-w-2xl mx-auto font-body font-light">
            {t(`personas.${persona.id}.description`)}
          </p>
        </motion.div>

        {/* Main content — spatial layout */}
        <div className="grid grid-cols-12 gap-8 max-w-6xl 2xl:max-w-7xl mx-auto px-4">
          {/* Left: Radar + Axes */}
          <motion.div variants={slideUp} className="col-span-12 lg:col-span-5 space-y-8">
            {/* Radar — glass panel */}
            <div className="rounded-2xl p-8 flex flex-col items-center"
              style={{ background: "rgba(0,0,0,0.5)", backdropFilter: "blur(12px)", border: "1px solid rgba(255,255,255,0.06)" }}
            >
              <span className="hud-label mb-6">{t("personaDetail.mindProfile")}</span>
              <MindRadar axes={persona.axes} color={persona.color} size={420} />
            </div>

            {/* Axes — HUD style bars with belief colors */}
            <div className="spatial-card p-8">
              <span className="hud-label mb-6 block">{t("personaDetail.axesBreakdown")}</span>
              <div className="space-y-5">
                {AXIS_LABELS.map(({ key, label, short, belief }) => {
                  const pct = Math.round(persona.axes[key] * 100);
                  const barColor = beliefColors[belief].primary;
                  return (
                    <div key={key}>
                      <div className="flex items-center justify-between mb-1.5">
                        <div className="flex items-center gap-2">
                          <span className="hud-label w-8">{short}</span>
                          <span className="text-xs text-slate-500 font-body">{t(`axes.${key}`)}</span>
                        </div>
                        <span className="hud-value text-xs" style={{ color: barColor }}>{pct}</span>
                      </div>
                      <div className="w-full h-[3px] rounded-full bg-white/5 overflow-hidden">
                        <motion.div
                          className="h-full rounded-full"
                          style={{ backgroundColor: barColor }}
                          initial={{ width: 0 }}
                          animate={{ width: `${pct}%` }}
                          transition={{ duration: 1, ease: [0.22, 1, 0.36, 1] }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </motion.div>

          {/* Right: Details */}
          <motion.div variants={slideUp} className="col-span-12 lg:col-span-7 space-y-8">
            {/* Strengths */}
            <div className="spatial-card p-8">
              <div className="flex items-center gap-2 mb-5">
                <Sparkles size={14} className="text-slate-600" />
                <span className="hud-label">{t("personaDetail.strengths")}</span>
              </div>
              <div className="flex flex-wrap gap-2">
                {persona.strengths.map((s, i) => (
                  <Badge key={s} label={t(`personas.${persona.id}.strengths.${i}`)} color={persona.color} size="md" />
                ))}
              </div>
            </div>

            {/* Famous Minds */}
            <div className="spatial-card p-8">
              <span className="hud-label mb-5 block">{t("personaDetail.famousMinds")}</span>
              <div className="flex flex-wrap gap-3">
                {persona.famousMinds.map((name) => (
                  <div
                    key={name}
                    className="px-4 py-2 rounded-xl text-sm font-body font-light text-slate-400"
                    style={{
                      background: `${persona.color}08`,
                      border: `1px solid ${persona.color}15`,
                    }}
                  >
                    {name}
                  </div>
                ))}
              </div>
            </div>

            {/* Compatible Personas */}
            <div className="spatial-card p-8">
              <div className="flex items-center gap-2 mb-5">
                <Users size={14} className="text-slate-600" />
                <span className="hud-label">{t("personaDetail.compatiblePersonas")}</span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {compatiblePersonas.map((cp) => (
                  <PersonaCard key={cp.id} persona={cp} compact />
                ))}
              </div>
            </div>

            {/* Evolution Path */}
            <div className="spatial-card p-8">
              <span className="hud-label mb-8 block">{t("personaDetail.evolutionPath")}</span>
              <div className="flex items-center gap-0">
                {STAGES.map((s, i) => (
                  <div key={s.stage} className="flex items-center flex-1">
                    <div className="flex flex-col items-center flex-1">
                      <div
                        className="w-12 h-12 rounded-full flex items-center justify-center font-display font-bold text-sm mb-3"
                        style={{
                          background: `linear-gradient(135deg, ${persona.color}${s.stage === 3 ? "30" : s.stage === 2 ? "18" : "08"}, transparent)`,
                          border: `1.5px solid ${persona.color}${s.stage === 3 ? "40" : s.stage === 2 ? "25" : "15"}`,
                          color: persona.color,
                          opacity: s.stage === 3 ? 1 : s.stage === 2 ? 0.7 : 0.4,
                        }}
                      >
                        {s.stage}
                      </div>
                      <span className="text-sm font-body font-medium text-slate-300">{t(`stages.${s.stage}`)}</span>
                      <span className="hud-label mt-1">{t("common.stage", { n: s.stage })}</span>
                    </div>
                    {i < STAGES.length - 1 && (
                      <div
                        className="h-[1px] flex-1 -mx-2"
                        style={{
                          background: `linear-gradient(90deg, ${persona.color}20, ${persona.color}08)`,
                        }}
                      />
                    )}
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>
      </motion.div>
    </motion.div>
  );
}
