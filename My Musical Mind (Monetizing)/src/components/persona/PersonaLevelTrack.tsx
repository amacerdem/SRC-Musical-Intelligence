/* ── PersonaLevelTrack — 12-node horizontal progression ────────── */

import { motion } from "framer-motion";
import { NucleusDot } from "@/components/mind/NucleusDot";
import type { PersonaLevel } from "@/types/m3";

interface Props {
  currentLevel: PersonaLevel;
  color: string;
}

export function PersonaLevelTrack({ currentLevel, color }: Props) {
  const levels = Array.from({ length: 12 }, (_, i) => i + 1) as PersonaLevel[];

  return (
    <div className="flex items-center gap-0 w-full">
      {levels.map((level) => {
        const completed = level < currentLevel;
        const current = level === currentLevel;
        const future = level > currentLevel;

        return (
          <div key={level} className="flex items-center flex-1">
            <div className="flex flex-col items-center relative">
              {/* Node */}
              {current ? (
                <motion.div
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                >
                  <NucleusDot color={color} size={10} active pulsing />
                </motion.div>
              ) : (
                <div
                  className="rounded-full transition-all duration-300"
                  style={{
                    width: completed ? 8 : 6,
                    height: completed ? 8 : 6,
                    backgroundColor: completed ? color : "transparent",
                    border: `1.5px solid ${completed ? color : future ? `${color}30` : color}`,
                    opacity: future ? 0.3 : 1,
                  }}
                />
              )}

              {/* Level number (show for milestones) */}
              {(level === 1 || level === 4 || level === 7 || level === 10 || level === 12 || current) && (
                <span
                  className="absolute -bottom-5 text-[8px] font-mono"
                  style={{ color: current ? color : future ? `${color}40` : `${color}80` }}
                >
                  {level}
                </span>
              )}
            </div>

            {/* Connector line */}
            {level < 12 && (
              <div
                className="h-[1px] flex-1 mx-0.5"
                style={{
                  background: completed
                    ? `${color}60`
                    : `${color}15`,
                }}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}
