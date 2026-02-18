import { motion } from "framer-motion";

interface Props {
  color: string;
  size?: number;
  active?: boolean;
  pulsing?: boolean;
  glow?: boolean;
  className?: string;
}

/**
 * CSS-only nucleus dot — the organism's pulsing neural node, miniaturized.
 * 3-layer radial: outer halo, core, specular highlight.
 * Zero canvas overhead.
 */
export function NucleusDot({
  color,
  size = 6,
  active = false,
  pulsing = false,
  glow = false,
  className = "",
}: Props) {
  return (
    <motion.div
      className={`relative flex items-center justify-center ${className}`}
      style={{ width: size * 3, height: size * 3 }}
      animate={
        pulsing
          ? { scale: [1, 1.3, 1], opacity: [0.7, 1, 0.7] }
          : undefined
      }
      transition={
        pulsing
          ? { duration: 3, repeat: Infinity, ease: "easeInOut" }
          : undefined
      }
    >
      {/* Outer halo */}
      {(active || glow) && (
        <div
          className="absolute inset-0 rounded-full"
          style={{
            background: `radial-gradient(circle, ${color}40 0%, ${color}10 50%, transparent 70%)`,
            filter: `blur(${size * 0.5}px)`,
          }}
        />
      )}

      {/* Core */}
      <div
        className="rounded-full relative z-10"
        style={{
          width: size,
          height: size,
          background: active
            ? `radial-gradient(circle at 35% 35%, ${color}, ${color}CC)`
            : `${color}99`,
          boxShadow: active ? `0 0 ${size * 2}px ${color}60` : undefined,
        }}
      >
        {/* Specular highlight */}
        <div
          className="absolute rounded-full"
          style={{
            width: size * 0.4,
            height: size * 0.4,
            top: size * 0.15,
            left: size * 0.2,
            background: "rgba(255,255,255,0.4)",
          }}
        />
      </div>
    </motion.div>
  );
}
