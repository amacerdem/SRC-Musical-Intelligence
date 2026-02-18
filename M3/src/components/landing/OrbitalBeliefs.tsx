import { motion } from "framer-motion";
import { beliefColors } from "@/design/tokens";

const beliefs = [
  { name: "Consonance", key: "consonance" as const, orbit: 120, speed: 24, startAngle: 0 },
  { name: "Tempo", key: "tempo" as const, orbit: 150, speed: 30, startAngle: 72 },
  { name: "Salience", key: "salience" as const, orbit: 180, speed: 36, startAngle: 144 },
  { name: "Familiarity", key: "familiarity" as const, orbit: 210, speed: 28, startAngle: 216 },
  { name: "Reward", key: "reward" as const, orbit: 240, speed: 32, startAngle: 288 },
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
                background: `conic-gradient(from ${b.startAngle}deg, ${colors.primary}30, transparent 25%, transparent 100%)`,
                maskImage: `radial-gradient(transparent ${b.orbit - 3}px, black ${b.orbit - 2}px, black ${b.orbit + 2}px, transparent ${b.orbit + 3}px)`,
                WebkitMaskImage: `radial-gradient(transparent ${b.orbit - 3}px, black ${b.orbit - 2}px, black ${b.orbit + 2}px, transparent ${b.orbit + 3}px)`,
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
                border: `1px solid ${colors.primary}08`,
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
                boxShadow: `0 0 12px ${colors.primary}60, 0 0 30px ${colors.primary}20`,
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
