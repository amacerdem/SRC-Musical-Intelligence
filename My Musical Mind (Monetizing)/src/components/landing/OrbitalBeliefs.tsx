import { motion } from "framer-motion";
import { ALL_PSYCHOLOGY } from "@/data/dimensions";

const dimensions = [
  { key: "energy",     orbit: 90,  speed: 24, startAngle: 330 },
  { key: "valence",    orbit: 110, speed: 28, startAngle: 55 },
  { key: "tempo",      orbit: 130, speed: 32, startAngle: 120 },
  { key: "tension",    orbit: 150, speed: 26, startAngle: 185 },
  { key: "groove",     orbit: 170, speed: 30, startAngle: 250 },
  { key: "complexity", orbit: 190, speed: 34, startAngle: 315 },
];

const dimColors: Record<string, string> = {};
for (const d of ALL_PSYCHOLOGY) dimColors[d.key] = d.color;

interface Props {
  visible: boolean;
  size?: number;
}

export function OrbitalBeliefs({ visible, size = 500 }: Props) {
  const center = size / 2;

  return (
    <div className="relative" style={{ width: size, height: size }}>
      {dimensions.map((b, i) => {
        const color = dimColors[b.key] ?? "#A855F7";
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
                background: `conic-gradient(from ${b.startAngle}deg, ${color}50, ${color}44 5%, ${color}38 10%, ${color}2C 16%, ${color}1E 22%, ${color}12 30%, ${color}08 38%, ${color}03 46%, transparent 55%, transparent 100%)`,
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
                border: `1px solid ${color}06`,
              }}
            />

            {/* Dimension dot */}
            <motion.div
              className="absolute"
              style={{
                width: 8,
                height: 8,
                left: center + b.orbit - 4,
                top: center - 4,
                borderRadius: "50%",
                background: color,
                boxShadow: `0 0 14px ${color}80, 0 0 35px ${color}40`,
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
