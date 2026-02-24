/* ── PersonaEvolutionVisual — 12 mini-organisms at each level ──── */

import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";
import { MiniOrganism } from "@/components/mind/MiniOrganism";
import type { PersonaLevel } from "@/types/m3";
import { levelToOrganismStage } from "@/types/m3";
import { getLevelName } from "@/data/persona-levels";
import type { NeuralFamily } from "@/types/mind";

interface Props {
  color: string;
  family: NeuralFamily;
  currentLevel: PersonaLevel;
}

export function PersonaEvolutionVisual({ color, family, currentLevel }: Props) {
  const { t, i18n } = useTranslation();
  const lang = i18n.language === "tr" ? "tr" : "en";
  const levels = Array.from({ length: 12 }, (_, i) => (i + 1) as PersonaLevel);

  return (
    <div className="grid grid-cols-4 md:grid-cols-6 gap-4">
      {levels.map((level) => {
        const stage = levelToOrganismStage(level);
        const isCurrent = level === currentLevel;
        const isCompleted = level < currentLevel;
        const isFuture = level > currentLevel;
        const levelInfo = getLevelName(family, level);
        const name = lang === "tr" ? levelInfo.nameTr : levelInfo.name;

        return (
          <motion.div
            key={level}
            className="flex flex-col items-center gap-1.5"
            animate={isCurrent ? { scale: [1, 1.05, 1] } : {}}
            transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
          >
            <div
              className="relative w-12 h-12 flex items-center justify-center rounded-xl transition-all duration-500"
              style={{
                background: isCurrent
                  ? `linear-gradient(135deg, ${color}25, ${color}10)`
                  : isCompleted
                  ? `${color}08`
                  : "rgba(255,255,255,0.02)",
                border: isCurrent
                  ? `1.5px solid ${color}40`
                  : isCompleted
                  ? `1px solid ${color}15`
                  : "1px solid rgba(255,255,255,0.04)",
                opacity: isFuture ? 0.3 : 1,
                boxShadow: isCurrent ? `0 0 20px ${color}20` : "none",
              }}
            >
              <MiniOrganism color={color} stage={stage} size={28} />
            </div>
            <span
              className="text-[8px] font-mono text-center leading-tight max-w-[56px]"
              style={{ color: isCurrent ? color : isCompleted ? `${color}80` : `${color}30` }}
            >
              L{level}
            </span>
            <span
              className="text-[7px] font-display text-center leading-tight max-w-[56px] truncate"
              style={{ color: isCurrent ? `${color}CC` : "rgb(100,116,139)" }}
            >
              {name}
            </span>
          </motion.div>
        );
      })}
    </div>
  );
}
