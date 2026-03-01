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

  const hasContent = body !== bodyKey;

  return (
    <motion.section
      id={`section-${section.key}`}
      variants={slideUp}
      className="scroll-mt-24"
    >
      <div className="flex items-start gap-2">
        <span
          className="text-xs mt-0.5 opacity-60"
          style={{ color }}
        >
          {section.iconEmoji}
        </span>
        <div className="flex-1 min-w-0">
          <h2
            className="text-xs font-display font-semibold uppercase tracking-wider mb-1"
            style={{ color }}
          >
            {t(section.labelKey)}
          </h2>
          {hasContent ? (
            <p className="text-[13px] text-slate-400/90 leading-[1.55] font-body font-light">
              {body}
            </p>
          ) : (
            <p className="text-[13px] text-slate-700 italic font-body font-light">
              {t("persona.sections.comingSoon")}
            </p>
          )}
        </div>
      </div>
    </motion.section>
  );
}
