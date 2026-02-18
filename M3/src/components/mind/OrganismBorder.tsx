import { type ReactNode } from "react";
import { beliefColors } from "@/design/tokens";

type BeliefDomain = "consonance" | "tempo" | "salience" | "familiarity" | "reward";

interface Props {
  children: ReactNode;
  beliefDomain?: BeliefDomain;
  color?: string;
  pulsing?: boolean;
  className?: string;
}

/**
 * Organism membrane-inspired animated border.
 * Conic gradient rotation with belief-colored glow.
 * Pure CSS — no canvas overhead.
 */
export function OrganismBorder({
  children,
  beliefDomain,
  color,
  pulsing = false,
  className = "",
}: Props) {
  const resolvedColor = color
    ?? (beliefDomain ? beliefColors[beliefDomain].primary : "#A855F7");

  return (
    <div className={`relative group ${className}`}>
      {/* Animated gradient border */}
      <div
        className="absolute -inset-[1px] rounded-2xl opacity-40 group-hover:opacity-70 transition-opacity duration-500"
        style={{
          background: `conic-gradient(from var(--organism-border-angle, 0deg), transparent 0%, ${resolvedColor}30 15%, transparent 30%, ${resolvedColor}20 50%, transparent 65%, ${resolvedColor}40 80%, transparent 100%)`,
          animation: pulsing
            ? "organismBorderSpin 8s linear infinite, organismBorderPulse 4s ease-in-out infinite"
            : "organismBorderSpin 8s linear infinite",
          filter: `blur(0.5px)`,
        }}
      />

      {/* Inner glow */}
      <div
        className="absolute -inset-[1px] rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"
        style={{
          boxShadow: `inset 0 0 20px ${resolvedColor}10, 0 0 30px ${resolvedColor}08`,
        }}
      />

      {/* Content */}
      <div className="relative z-10 bg-black/60 backdrop-blur-xl rounded-2xl border border-white/[0.04]">
        {children}
      </div>
    </div>
  );
}
