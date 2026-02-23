import { motion } from "framer-motion";
import { beliefColors } from "@/design/tokens";

const stages = [
  { label: "Audio", sub: "Raw Signal", color: "#64748B" },
  { label: "R\u00B3", sub: "97 Dimensions", color: beliefColors.consonance.primary },
  { label: "H\u00B3", sub: "32 Horizons", color: beliefColors.tempo.primary },
  { label: "C\u00B3", sub: "5 Beliefs", color: beliefColors.salience.primary },
  { label: "\u03A8\u00B3", sub: "Experience", color: beliefColors.reward.primary },
];

interface Props {
  visible: boolean;
}

export function PipelineViz({ visible }: Props) {
  return (
    <div className="flex items-center justify-center gap-3 md:gap-6">
      {stages.map((stage, i) => (
        <motion.div
          key={stage.label}
          initial={{ opacity: 0, y: 30, scale: 0.8 }}
          animate={visible ? { opacity: 1, y: 0, scale: 1 } : {}}
          transition={{
            duration: 0.8,
            delay: i * 0.15,
            ease: [0.22, 1, 0.36, 1],
          }}
          className="flex items-center gap-3 md:gap-6"
        >
          <div className="flex flex-col items-center gap-2">
            <div
              className="w-12 h-12 md:w-16 md:h-16 rounded-2xl flex items-center justify-center font-display font-bold text-sm md:text-lg"
              style={{
                background: `${stage.color}10`,
                border: `1px solid ${stage.color}25`,
                color: stage.color,
                boxShadow: `0 0 30px ${stage.color}10`,
              }}
            >
              {stage.label}
            </div>
            <span className="text-[10px] text-slate-600 font-mono whitespace-nowrap">
              {stage.sub}
            </span>
          </div>

          {/* Arrow connector */}
          {i < stages.length - 1 && (
            <motion.div
              initial={{ opacity: 0, scaleX: 0 }}
              animate={visible ? { opacity: 0.3, scaleX: 1 } : {}}
              transition={{ duration: 0.5, delay: i * 0.15 + 0.3 }}
              className="w-6 md:w-10 h-px origin-left"
              style={{
                background: `linear-gradient(90deg, ${stage.color}40, ${stages[i + 1].color}40)`,
              }}
            />
          )}
        </motion.div>
      ))}
    </div>
  );
}
