import { motion } from "framer-motion";
import { beliefColors } from "@/design/tokens";

const beliefs = [
  { name: "Consonance", key: "consonance" as const, orbit: 90, speed: 24, startAngle: 330 },
  { name: "Prediction", key: "prediction" as const, orbit: 105, speed: 27, startAngle: 21 },
  { name: "Tempo", key: "tempo" as const, orbit: 120, speed: 30, startAngle: 73 },
  { name: "Salience", key: "salience" as const, orbit: 135, speed: 36, startAngle: 124 },
  { name: "Emotion", key: "emotion" as const, orbit: 150, speed: 22, startAngle: 176 },
  { name: "Familiarity", key: "familiarity" as const, orbit: 165, speed: 28, startAngle: 227 },
  { name: "Reward", key: "reward" as const, orbit: 180, speed: 32, startAngle: 279 },
];

interface Props {
  visible: boolean;
  size?: number;
}

export function OrbitalBeliefs({ visible, size = 500 }: Props) {
  const center = size / 2;

  return (
    <div className="relative" style={{ width: size, height: size }}>
      {/* Orbital rings */}
      {beliefs.map((b, i) => {
        const colors = beliefColors[b.key];
        return (
          <motion.div
            key={b.key}
            initial={{ opacity: 0, scale: 0.5 }}
            animate={visible ? { opacity: 1, scale: 1 } : {}}
            transition={{ duration: 1, delay: i * 0.12, ease: [0.22, 1, 0.36, 1] }}
            className="absolute inset-0"
          >
            {/* Conic gradient trail */}
            <div
              className="absolute rounded-full"
              style={{
                width: b.orbit * 2,
                height: b.orbit * 2,
                left: center - b.orbit,
                top: center - b.orbit,
                background: `conic-gradient(from ${b.startAngle}deg, ${colors.primary}50, ${colors.primary}44 5%, ${colors.primary}38 10%, ${colors.primary}2C 16%, ${colors.primary}1E 22%, ${colors.primary}12 30%, ${colors.primary}08 38%, ${colors.primary}03 46%, transparent 55%, transparent 100%)`,
                maskImage: `radial-gradient(transparent ${b.orbit - 2}px, black ${b.orbit - 1}px, black ${b.orbit + 1}px, transparent ${b.orbit + 2}px)`,
                WebkitMaskImage: `radial-gradient(transparent ${b.orbit - 2}px, black ${b.orbit - 1}px, black ${b.orbit + 1}px, transparent ${b.orbit + 2}px)`,
                animation: `orbit ${b.speed}s linear infinite`,
              }}
            />

            {/* Orbit ring */}
            <div
              className="absolute rounded-full"
              style={{
                width: b.orbit * 2,
                height: b.orbit * 2,
                left: center - b.orbit,
                top: center - b.orbit,
                border: `1px solid ${colors.primary}06`,
              }}
            />

            {/* Belief dot */}
            <motion.div
              className="absolute"
              style={{
                width: 8,
                height: 8,
                left: center + b.orbit - 4,
                top: center - 4,
                borderRadius: "50%",
                background: colors.primary,
                boxShadow: `0 0 14px ${colors.primary}80, 0 0 35px ${colors.primary}40`,
                animation: `orbit ${b.speed}s linear infinite`,
                transformOrigin: `${-b.orbit + 4}px 4px`,
              }}
            />
          </motion.div>
        );
      })}
    </div>
  );
}
