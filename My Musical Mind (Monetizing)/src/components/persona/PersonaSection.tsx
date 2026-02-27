/* ── PersonaSection — A single narrative block ────────────────── */

import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";
import { slideUp } from "@/design/animations";
import type { NarrativeSection } from "@/data/persona-narratives";
import { sectionI18nKey } from "@/data/persona-narratives";

interface Props {
  section: NarrativeSection;
  personaId: number;
  color: string;
}

export function PersonaSection({ section, personaId, color }: Props) {
  const { t } = useTranslation();
  const bodyKey = sectionI18nKey(personaId, section.key);
  const body = t(bodyKey);

  // If the i18n key returns itself (no translation), show a placeholder
  const hasContent = body !== bodyKey;

  return (
    <motion.section
      id={`section-${section.key}`}
      variants={slideUp}
      className="scroll-mt-24"
    >
      <div className="mb-3 flex items-center gap-2">
        <span
          className="text-sm font-display"
          style={{ color }}
        >
          {section.iconEmoji}
        </span>
        <h2
          className="text-lg font-display font-semibold"
          style={{ color }}
        >
          {t(section.labelKey)}
        </h2>
      </div>
      <div
        className="h-[1px] mb-5"
        style={{ background: `linear-gradient(90deg, ${color}30, transparent)` }}
      />
      {hasContent ? (
        <p className="text-sm text-slate-400 leading-relaxed font-body font-light whitespace-pre-line">
          {body}
        </p>
      ) : (
        <p className="text-sm text-slate-700 italic font-body font-light">
          {t("persona.sections.comingSoon")}
        </p>
      )}
    </motion.section>
  );
}
