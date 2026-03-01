/* ── PersonaDetail — 16personalities-Style Persona Page ──────────
 *  Layout: Sidebar (sticky nav) + Hero (organism + identity) + Sections
 *  Each persona gets 8 narrative prose sections, evolution track,
 *  and family-morphology organism visualization.
 *  ──────────────────────────────────────────────────────────────── */

import { useParams, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { motion } from "framer-motion";
import { useMemo } from "react";
import { ArrowLeft, Users, Sparkles } from "lucide-react";
import { getPersona, personas } from "@/data/personas";
import { FAMILY_COLORS } from "@/data/persona-levels";
import { NARRATIVE_SECTIONS } from "@/data/persona-narratives";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { PersonaCard } from "@/components/mind/PersonaCard";
import { PersonaSidebar } from "@/components/persona/PersonaSidebar";
import { PersonaSection } from "@/components/persona/PersonaSection";
import { PersonaLevelTrack } from "@/components/persona/PersonaLevelTrack";
import { PersonaEvolutionVisual } from "@/components/persona/PersonaEvolutionVisual";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { NucleusDot } from "@/components/mind/NucleusDot";
import { MindTypeRing } from "@/components/mind/MindTypeRing";
import { pageTransition, staggerChildren, slideUp, cinematicReveal } from "@/design/animations";
import { useM3Store } from "@/stores/useM3Store";
import { FAMILY_MORPHOLOGY, levelToOrganismStage, GENE_NAMES, GENE_COLORS } from "@/types/m3";
import type { FamilyMorphology } from "@/canvas/mind-organism";
import { DimensionSunburst } from "@/components/mind/DimensionSunburst";
import { PersonaAvatar } from "@/components/mind/PersonaAvatar";
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
  const navigate = useNavigate();
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

  const familyGroups = useMemo(() =>
    FAMILY_ORDER.map((family) => ({
      family,
      color: FAMILY_COLORS[family],
      desc: FAMILY_DESC[family],
      members: personas.filter((p) => p.family === family),
    })),
  []);

  return (
    <motion.div {...pageTransition} className="min-h-screen bg-black relative pb-24 -mt-14">
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
        className="absolute top-32 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full blur-[200px] opacity-8 pointer-events-none"
        style={{ backgroundColor: persona.color }}
      />

      {/* Hero — Persona Identity */}
      <motion.div variants={staggerChildren} initial="initial" animate="animate" className="relative z-10">
        <motion.div variants={cinematicReveal} className="text-center mb-6 -mt-4">
          {/* Character Avatar + Organism side by side */}
          <div className="flex items-center justify-center gap-6 mb-1">
            {/* 2D Character */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
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

            {/* Organism avatar */}
            <motion.div
              className="relative w-24 h-24"
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

          {/* Family badge */}
          <div className="flex items-center justify-center gap-2 mb-1">
            <NucleusDot color={persona.color} size={4} active />
            <span className="hud-label text-[10px]">{persona.family}</span>
          </div>

          {/* Persona name */}
          <h1 className="text-4xl md:text-5xl font-display font-bold text-slate-100 tracking-tight mb-1">
            {t(`personas.${persona.id}.name`)}
          </h1>
          <p className="text-base text-slate-500 italic font-body font-light mb-2">
            "{t(`personas.${persona.id}.tagline`)}"
          </p>

          {/* Badges row */}
          <div className="flex items-center justify-center gap-3 mb-6">
            <Badge label={t("common.ofListeners", { pct: persona.populationPct })} color={persona.color} size="md" />
            {isMyPersona && (
              <Badge label={`L${personaLevel}/12`} color={persona.color} size="md" />
            )}
          </div>

          {/* Level track */}
          <div className="max-w-md mx-auto px-8 mb-8">
            <PersonaLevelTrack currentLevel={personaLevel} color={persona.color} />
          </div>
        </motion.div>

        {/* Main content — Sidebar + Content */}
        <div className="max-w-6xl 2xl:max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-12 gap-8">
            {/* Sidebar — sticky nav (desktop only) */}
            <motion.div variants={slideUp} className="hidden lg:block col-span-3">
              <div className="sticky top-24">
                <PersonaSidebar color={persona.color} />

                {/* Dimension Sunburst — 6D / 12D / 24D concentric rings */}
                <div className="mt-6">
                  <DimensionSunburst color={persona.color} size={240} />
                </div>

                {/* Gene DNA — 5 genes */}
                <div className="mt-6 p-4 rounded-xl" style={{ background: "rgba(0,0,0,0.4)", border: "1px solid rgba(255,255,255,0.04)" }}>
                  <span className="hud-label mb-3 block">{t("personaDetail.geneDna")}</span>
                  <div className="flex justify-center mb-4">
                    <MindTypeRing genes={persona.genes} size={140} showLabels={false} />
                  </div>
                  <div className="space-y-2">
                    {GENE_NAMES.map((gene, i) => {
                      const pct = Math.round(persona.genes[gene] * 100);
                      const color = GENE_COLORS[gene];
                      const isDominant = pct === Math.max(...GENE_NAMES.map(g => Math.round(persona.genes[g] * 100)));
                      return (
                        <div key={gene}>
                          <div className="flex items-center justify-between mb-0.5">
                            <div className="flex items-center gap-1.5">
                              <div
                                className="w-1.5 h-1.5 rounded-full"
                                style={{
                                  background: color,
                                  boxShadow: isDominant ? `0 0 6px ${color}80` : "none",
                                }}
                              />
                              <span
                                className="hud-label text-[8px]"
                                style={{ color: isDominant ? color : undefined }}
                              >
                                {t(`m3.gene.${gene}`)}
                              </span>
                            </div>
                            <span className="text-[9px] font-mono" style={{ color }}>
                              {pct}
                            </span>
                          </div>
                          <div className="w-full h-[3px] rounded-full bg-white/5 overflow-hidden">
                            <motion.div
                              className="h-full rounded-full"
                              style={{
                                backgroundColor: color,
                                boxShadow: isDominant ? `0 0 10px ${color}40` : "none",
                              }}
                              initial={{ width: 0 }}
                              animate={{ width: `${pct}%` }}
                              transition={{ duration: 1, delay: 0.2 + i * 0.06, ease: [0.22, 1, 0.36, 1] }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
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

              {/* Strengths */}
              <div className="spatial-card p-8">
                <div className="flex items-center gap-2 mb-5">
                  <Sparkles size={14} style={{ color: persona.color }} />
                  <span className="hud-label">{t("personaDetail.strengths")}</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {persona.strengths.map((_, i) => (
                    <Badge key={i} label={t(`personas.${persona.id}.strengths.${i}`)} color={persona.color} size="md" />
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

              {/* Evolution visual — 12 levels */}
              <div className="spatial-card p-8">
                <span className="hud-label mb-6 block">{t("personaDetail.evolutionPath")}</span>
                <PersonaEvolutionVisual
                  color={persona.color}
                  family={persona.family}
                  currentLevel={personaLevel}
                />
              </div>

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

              {/* Mobile genes (hidden on desktop) */}
              <div className="lg:hidden spatial-card p-8">
                <span className="hud-label mb-4 block">{t("personaDetail.geneDna")}</span>
                <div className="flex justify-center mb-5">
                  <MindTypeRing genes={persona.genes} size={160} />
                </div>
                <div className="space-y-2.5">
                  {GENE_NAMES.map((gene, i) => {
                    const pct = Math.round(persona.genes[gene] * 100);
                    const color = GENE_COLORS[gene];
                    const isDominant = pct === Math.max(...GENE_NAMES.map(g => Math.round(persona.genes[g] * 100)));
                    return (
                      <div key={gene}>
                        <div className="flex items-center justify-between mb-0.5">
                          <div className="flex items-center gap-1.5">
                            <div
                              className="w-1.5 h-1.5 rounded-full"
                              style={{
                                background: color,
                                boxShadow: isDominant ? `0 0 6px ${color}80` : "none",
                              }}
                            />
                            <span
                              className="hud-label text-[9px]"
                              style={{ color: isDominant ? color : undefined }}
                            >
                              {t(`m3.gene.${gene}`)}
                            </span>
                          </div>
                          <span className="text-[10px] font-mono" style={{ color }}>
                            {pct}
                          </span>
                        </div>
                        <div className="w-full h-[3px] rounded-full bg-white/5 overflow-hidden">
                          <motion.div
                            className="h-full rounded-full"
                            style={{
                              backgroundColor: color,
                              boxShadow: isDominant ? `0 0 10px ${color}40` : "none",
                            }}
                            initial={{ width: 0 }}
                            animate={{ width: `${pct}%` }}
                            transition={{ duration: 1, delay: i * 0.06, ease: [0.22, 1, 0.36, 1] }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
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
