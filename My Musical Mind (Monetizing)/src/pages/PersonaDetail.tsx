/* ── PersonaDetail — 16personalities-Style Persona Page ──────────
 *  Layout: Sidebar (sticky nav) + Hero (organism + identity) + Sections
 *  Each persona gets 8 narrative prose sections, evolution track,
 *  and family-morphology organism visualization.
 *  ──────────────────────────────────────────────────────────────── */

import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { motion } from "framer-motion";
import { useMemo } from "react";
import { Users, Sparkles } from "lucide-react";
import { getPersona, personas } from "@/data/personas";
import { FAMILY_COLORS } from "@/data/persona-levels";
import { NARRATIVE_SECTIONS } from "@/data/persona-narratives";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { PersonaCard } from "@/components/mind/PersonaCard";
import { PersonaSidebar } from "@/components/persona/PersonaSidebar";
import { PersonaSection } from "@/components/persona/PersonaSection";
import { PersonaLevelTrack } from "@/components/persona/PersonaLevelTrack";

import { Badge } from "@/components/ui/Badge";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { pageTransition, staggerChildren, slideUp, cinematicReveal } from "@/design/animations";
import { useM3Store } from "@/stores/useM3Store";
import { FAMILY_MORPHOLOGY, levelToOrganismStage } from "@/types/m3";
import type { FamilyMorphology } from "@/canvas/mind-organism";
import { DashboardRadar } from "@/components/mind/DashboardRadar";
import { PersonaAvatar } from "@/components/mind/PersonaAvatar";
import { getPersonaDimensions } from "@/data/persona-dimensions";
import { profileToArray } from "@/data/dimensions";
import type { NeuralFamily } from "@/types/mind";

const FAMILY_ORDER: NeuralFamily[] = [
  "Alchemists", "Architects", "Explorers", "Anchors", "Kineticists",
];

const FAMILY_DESC: Record<NeuralFamily, string> = {
  Alchemists:  "Transformation & tension — intensity and dramatic resolution",
  Architects:  "Structure & order — patterns, intervals, and form",
  Explorers:   "Novelty & chaos — the unexpected and uncharted",
  Anchors:     "Emotion & memory — deep feeling and human connection",
  Kineticists: "Drive & energy — rhythm-first, pulse-seeking",
};

export function PersonaDetail() {
  const { id } = useParams<{ id: string }>();
  const { t } = useTranslation();
  const m3Mind = useM3Store((s) => s.mind);
  const persona = getPersona(id ? Number(id) : (m3Mind?.activePersonaId ?? 24))!;

  const isMyPersona = m3Mind?.activePersonaId === persona.id;
  const personaLevel = isMyPersona ? (m3Mind?.level ?? 1) : 1;
  const organismStage = levelToOrganismStage(personaLevel);
  const morphology = FAMILY_MORPHOLOGY[persona.family] as FamilyMorphology;

  const compatiblePersonas = persona.compatibleWith
    .map((cid) => personas.find((p) => p.id === cid))
    .filter(Boolean) as typeof personas;

  const familyPersonas = personas.filter(p => p.family === persona.family && p.id !== persona.id);

  const personaDim6D = useMemo(() => profileToArray(getPersonaDimensions(persona.id)), [persona.id]);

  const familyGroups = useMemo(() =>
    FAMILY_ORDER.map((family) => ({
      family,
      color: FAMILY_COLORS[family],
      desc: FAMILY_DESC[family],
      members: personas.filter((p) => p.family === family),
    })),
  []);

  return (
    <motion.div {...pageTransition} className="min-h-screen bg-black relative pb-24 -mt-36">
      {/* Full-screen organism background */}
      <div className="absolute inset-0 opacity-10 pointer-events-none">
        <MindOrganismCanvas
          color={persona.color}
          stage={organismStage}
          intensity={0.3}
          breathRate={6}
          familyMorphology={morphology}
          className="w-full h-full"
          interactive={false}
        />
      </div>

      {/* Cinematic vignette */}
      <div className="cinematic-vignette" />

      {/* Ambient glow */}
      <div
        className="absolute top-64 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full blur-[200px] opacity-8 pointer-events-none"
        style={{ backgroundColor: persona.color }}
      />

      {/* Hero — Persona Identity */}
      <motion.div variants={staggerChildren} initial="initial" animate="animate" className="relative z-10">
        <motion.div variants={cinematicReveal} className="mb-4 -mt-10">
          {/* Hero layout: Identity left, Avatar center, Strengths right */}
          <div className="relative max-w-7xl mx-auto px-4">
            <div className="flex items-end justify-center gap-0">
              {/* Left: Identity */}
              <motion.div
                initial={{ opacity: 0, x: -30 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8, delay: 0.1, ease: [0.22, 1, 0.36, 1] }}
                className="hidden lg:flex flex-col items-end text-right flex-shrink-0 w-[260px] pb-8"
              >
                <div className="flex items-center gap-2 mb-2">
                  <NucleusDot color={persona.color} size={4} active />
                  <span className="hud-label text-[10px]">{persona.family}</span>
                </div>

                <h1 className="text-4xl font-display font-bold text-slate-100 tracking-tight mb-1 leading-tight">
                  {t(`personas.${persona.id}.name`)}
                </h1>
                <p className="text-sm text-slate-500 italic font-body font-light mb-3">
                  "{t(`personas.${persona.id}.tagline`)}"
                </p>

                <Badge label={t("common.ofListeners", { pct: persona.populationPct })} color={persona.color} size="md" />

                <div className="mt-5 w-full max-w-[220px]">
                  <PersonaLevelTrack currentLevel={personaLevel} color={persona.color} />
                </div>

              </motion.div>

              {/* Center: Avatar + Organism */}
              <div className="flex items-end gap-4 flex-shrink-0">
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
                >
                  <PersonaAvatar
                    personaId={persona.id}
                    color={persona.color}
                    family={persona.family}
                    size={480}
                    level={personaLevel}
                    showAura
                  />
                </motion.div>

                <motion.div
                  className="relative w-20 h-20 mb-8"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.8, delay: 0.1, ease: [0.22, 1, 0.36, 1] }}
                >
                  <MindOrganismCanvas
                    color={persona.color}
                    stage={organismStage}
                    intensity={0.8}
                    breathRate={4}
                    familyMorphology={morphology}
                    variant="micro"
                    className="w-full h-full"
                    interactive={false}
                  />
                </motion.div>
              </div>

              {/* Right: Strengths + Famous Minds */}
              <motion.div
                initial={{ opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
                className="hidden lg:flex flex-col items-start flex-shrink-0 w-[260px] pb-8 space-y-5"
              >
                <div>
                  <div className="flex items-center gap-2 mb-3">
                    <Sparkles size={14} style={{ color: persona.color }} />
                    <span className="hud-label">{t("personaDetail.strengths")}</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {persona.strengths.map((_, i) => (
                      <Badge key={i} label={t(`personas.${persona.id}.strengths.${i}`)} color={persona.color} size="md" />
                    ))}
                  </div>
                </div>

                <div>
                  <span className="hud-label mb-3 block">{t("personaDetail.famousMinds")}</span>
                  <div className="flex flex-wrap gap-2">
                    {persona.famousMinds.map((name) => (
                      <div
                        key={name}
                        className="px-3 py-1.5 rounded-lg text-sm font-body font-light text-slate-400"
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

              </motion.div>
            </div>

            {/* Mobile identity — shown only on small screens */}
            <div className="lg:hidden text-center mt-2">
              <div className="flex items-center justify-center gap-2 mb-1">
                <NucleusDot color={persona.color} size={4} active />
                <span className="hud-label text-[10px]">{persona.family}</span>
              </div>
              <h1 className="text-3xl font-display font-bold text-slate-100 tracking-tight mb-1">
                {t(`personas.${persona.id}.name`)}
              </h1>
              <p className="text-sm text-slate-500 italic font-body font-light mb-2">
                "{t(`personas.${persona.id}.tagline`)}"
              </p>
              <Badge label={t("common.ofListeners", { pct: persona.populationPct })} color={persona.color} size="md" />
              <div className="max-w-xs mx-auto px-4 mt-4">
                <PersonaLevelTrack currentLevel={personaLevel} color={persona.color} />
              </div>
            </div>
          </div>
        </motion.div>

        {/* Main content — Sidebar + Content */}
        <div className="max-w-6xl 2xl:max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-12 gap-8">
            {/* Sidebar — sticky nav (desktop only) */}
            <motion.div variants={slideUp} className="hidden lg:block col-span-3">
              <div className="sticky top-24">
                <PersonaSidebar color={persona.color} />

                {/* Mind Profile — 6D Radar */}
                <div className="mt-6 flex justify-center">
                  <DashboardRadar total={personaDim6D} color={persona.color} size={240} />
                </div>
              </div>
            </motion.div>

            {/* Content — narrative sections */}
            <motion.div variants={staggerChildren} initial="initial" animate="animate" className="col-span-12 lg:col-span-9 space-y-12">
              {/* Narrative sections */}
              {NARRATIVE_SECTIONS.map((section) => (
                <PersonaSection
                  key={section.key}
                  section={section}
                  personaId={persona.id}
                  color={persona.color}
                />
              ))}

              {/* Compatible personas */}
              <div className="spatial-card p-8">
                <div className="flex items-center gap-2 mb-5">
                  <Users size={14} style={{ color: persona.color }} />
                  <span className="hud-label">{t("personaDetail.compatiblePersonas")}</span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {compatiblePersonas.map((cp) => (
                    <PersonaCard key={cp.id} persona={cp} compact />
                  ))}
                </div>
              </div>

              {/* Same family */}
              {familyPersonas.length > 0 && (
                <div className="spatial-card p-8">
                  <span className="hud-label mb-5 block">
                    {t("personaDetail.sameFamily", { family: persona.family })}
                  </span>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                    {familyPersonas.map((fp) => (
                      <PersonaCard key={fp.id} persona={fp} compact />
                    ))}
                  </div>
                </div>
              )}

              {/* Mobile radar (hidden on desktop) */}
              <div className="lg:hidden flex justify-center">
                <DashboardRadar total={personaDim6D} color={persona.color} size={280} />
              </div>
            </motion.div>
          </div>
        </div>

        {/* ── All Personas Atlas ─────────────────────────────────── */}
        <motion.div
          variants={slideUp}
          initial="initial"
          animate="animate"
          className="max-w-7xl mx-auto mt-20 px-4"
        >
          <div className="text-center mb-10">
            <span className="hud-label mb-2 block">{t("infoHub.personaAtlas")}</span>
            <h2 className="text-2xl font-display font-bold text-slate-200 mb-2">
              {t("infoHub.personaAtlasTitle")}
            </h2>
            <p className="hud-label max-w-md mx-auto leading-relaxed text-xs">
              {t("infoHub.personaAtlasSubtitle")}
            </p>
          </div>

          <div className="space-y-12">
            {familyGroups.map(({ family, color: fColor, desc, members }) => (
              <div key={family}>
                <div className="flex items-center gap-3 mb-5">
                  <div className="w-2.5 h-2.5 rounded-full" style={{ background: fColor, boxShadow: `0 0 12px ${fColor}60` }} />
                  <h3 className="text-lg font-display font-bold" style={{ color: fColor }}>
                    {family}
                  </h3>
                  <div className="flex-1 h-px" style={{ background: `${fColor}15` }} />
                  <span className="text-[10px] font-body text-slate-600 font-light max-w-xs text-right">
                    {desc}
                  </span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4">
                  {members.map((p) => (
                    <div key={p.id} className="spatial-card p-0 overflow-hidden">
                      <PersonaCard persona={p} />
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </motion.div>
    </motion.div>
  );
}
