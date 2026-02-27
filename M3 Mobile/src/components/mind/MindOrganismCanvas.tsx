/* -- MindOrganismCanvas -- Animated SVG organism background --------------------
 *  A living, breathing organism visualization for the Dashboard.
 *  Mobile-optimized SVG version of the web Canvas 2D renderer.
 *  Nucleus glow + 6 gene tendrils + 8 orbital particles + breathing pulse.
 *  Uses react-native-svg for static shapes, react-native-reanimated for motion.
 *  -------------------------------------------------------------------------- */

import React, { useMemo } from "react";
import { View, StyleSheet } from "react-native";
import Svg, { Circle, Path, G } from "react-native-svg";
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withRepeat,
  withTiming,
  Easing,
} from "react-native-reanimated";

/* ── Types ------------------------------------------------------------------ */

interface MindOrganismCanvasProps {
  genes: {
    entropy: number;
    resolution: number;
    tension: number;
    resonance: number;
    plasticity: number;
  };
  color: string; // persona primary color
  size?: number; // default 280
  opacity?: number; // default 0.6
}

/* ── Gene Colors ------------------------------------------------------------- */

const GENE_COLORS = {
  entropy: "#06B6D4",
  resolution: "#10B981",
  tension: "#EF4444",
  resonance: "#8B5CF6",
  plasticity: "#EC4899",
  harmony: "#F59E0B", // 6th tendril = average of all genes
};

/* ── Particle Palette -------------------------------------------------------- */

const PARTICLE_COLORS = [
  "#06B6D4",
  "#10B981",
  "#EF4444",
  "#8B5CF6",
  "#EC4899",
  "#F59E0B",
  "#38BDF8",
  "#A78BFA",
];

/* ── Tendril Config ---------------------------------------------------------- */

type GeneKey = "entropy" | "resolution" | "tension" | "resonance" | "plasticity";

interface TendrilDef {
  geneKey: GeneKey | "harmony";
  color: string;
  angleOffset: number; // degrees from 12 o'clock
}

const TENDRIL_DEFS: TendrilDef[] = [
  { geneKey: "entropy", color: GENE_COLORS.entropy, angleOffset: 0 },
  { geneKey: "resolution", color: GENE_COLORS.resolution, angleOffset: 60 },
  { geneKey: "tension", color: GENE_COLORS.tension, angleOffset: 120 },
  { geneKey: "resonance", color: GENE_COLORS.resonance, angleOffset: 180 },
  { geneKey: "plasticity", color: GENE_COLORS.plasticity, angleOffset: 240 },
  { geneKey: "harmony", color: GENE_COLORS.harmony, angleOffset: 300 },
];

/* ── Particle Config --------------------------------------------------------- */

interface ParticleDef {
  orbitRadius: number;
  period: number; // seconds per revolution
  color: string;
  radius: number; // dot size
  startAngle: number; // degrees
}

const PARTICLE_DEFS: ParticleDef[] = [
  { orbitRadius: 45, period: 12, color: PARTICLE_COLORS[0], radius: 2.5, startAngle: 0 },
  { orbitRadius: 60, period: 16, color: PARTICLE_COLORS[1], radius: 2, startAngle: 45 },
  { orbitRadius: 75, period: 10, color: PARTICLE_COLORS[2], radius: 3, startAngle: 90 },
  { orbitRadius: 55, period: 18, color: PARTICLE_COLORS[3], radius: 2, startAngle: 135 },
  { orbitRadius: 90, period: 14, color: PARTICLE_COLORS[4], radius: 2.5, startAngle: 180 },
  { orbitRadius: 40, period: 8, color: PARTICLE_COLORS[5], radius: 3, startAngle: 225 },
  { orbitRadius: 100, period: 20, color: PARTICLE_COLORS[6], radius: 2, startAngle: 270 },
  { orbitRadius: 70, period: 11, color: PARTICLE_COLORS[7], radius: 2.5, startAngle: 315 },
];

/* ── Helpers ----------------------------------------------------------------- */

/** Degrees to radians */
function deg2rad(deg: number): number {
  return (deg * Math.PI) / 180;
}

/**
 * Build a quadratic Bezier path from nucleus center outward.
 * The control point is offset perpendicular to the main direction
 * for a natural curve.
 */
function buildTendrilPath(
  cx: number,
  cy: number,
  angleDeg: number,
  length: number,
): string {
  const rad = deg2rad(angleDeg - 90); // -90 so 0° = 12 o'clock
  const endX = cx + length * Math.cos(rad);
  const endY = cy + length * Math.sin(rad);

  // Control point: offset perpendicular to the direction for curvature
  const perpRad = rad + Math.PI / 2;
  const midDist = length * 0.5;
  const perpOffset = length * 0.18; // curvature amount
  const cpX = cx + midDist * Math.cos(rad) + perpOffset * Math.cos(perpRad);
  const cpY = cy + midDist * Math.sin(rad) + perpOffset * Math.sin(perpRad);

  return `M ${cx} ${cy} Q ${cpX} ${cpY} ${endX} ${endY}`;
}

/** Get the endpoint of a tendril for tip dot placement */
function getTendrilEnd(
  cx: number,
  cy: number,
  angleDeg: number,
  length: number,
): { x: number; y: number } {
  const rad = deg2rad(angleDeg - 90);
  return {
    x: cx + length * Math.cos(rad),
    y: cy + length * Math.sin(rad),
  };
}

/* ── Orbital Particle (Animated) --------------------------------------------- */

function OrbitalParticle({
  cx,
  cy,
  orbitRadius,
  period,
  color,
  radius,
  startAngle,
}: ParticleDef & { cx: number; cy: number }) {
  const progress = useSharedValue(0);

  React.useEffect(() => {
    progress.value = withRepeat(
      withTiming(1, {
        duration: period * 1000,
        easing: Easing.linear,
      }),
      -1, // infinite
      false,
    );
  }, [period, progress]);

  const animatedStyle = useAnimatedStyle(() => {
    const angle = deg2rad(startAngle + progress.value * 360);
    const tx = cx + orbitRadius * Math.cos(angle) - radius;
    const ty = cy + orbitRadius * Math.sin(angle) - radius;
    return {
      transform: [{ translateX: tx }, { translateY: ty }],
    };
  });

  return (
    <Animated.View
      style={[
        {
          position: "absolute",
          width: radius * 2,
          height: radius * 2,
          borderRadius: radius,
          backgroundColor: color,
          opacity: 0.7,
        },
        animatedStyle,
      ]}
    />
  );
}

/* ── Breathing Wrapper ------------------------------------------------------- */

function BreathingWrapper({
  children,
  size,
}: {
  children: React.ReactNode;
  size: number;
}) {
  const scale = useSharedValue(0.95);

  React.useEffect(() => {
    scale.value = withRepeat(
      withTiming(1.05, {
        duration: 3000,
        easing: Easing.inOut(Easing.sin),
      }),
      -1, // infinite
      true, // reverse
    );
  }, [scale]);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  return (
    <Animated.View
      style={[
        {
          width: size,
          height: size,
          alignItems: "center",
          justifyContent: "center",
        },
        animatedStyle,
      ]}
    >
      {children}
    </Animated.View>
  );
}

/* ── Main Component ---------------------------------------------------------- */

export function MindOrganismCanvas({
  genes,
  color,
  size = 280,
  opacity = 0.6,
}: MindOrganismCanvasProps) {
  const cx = size / 2;
  const cy = size / 2;
  const nucleusRadius = 20;

  // Compute tendril lengths from gene values.
  // Min length = 30, max length = size/2 - 20 (leave room for tip dots).
  const maxTendrilLength = size / 2 - 20;
  const minTendrilLength = 30;

  const harmonyValue = useMemo(
    () =>
      (genes.entropy +
        genes.resolution +
        genes.tension +
        genes.resonance +
        genes.plasticity) /
      5,
    [genes],
  );

  const geneValues: Record<GeneKey | "harmony", number> = useMemo(
    () => ({ ...genes, harmony: harmonyValue }),
    [genes, harmonyValue],
  );

  // Build tendril data
  const tendrils = useMemo(
    () =>
      TENDRIL_DEFS.map((def) => {
        const value = Math.max(0, Math.min(1, geneValues[def.geneKey]));
        const length =
          minTendrilLength + value * (maxTendrilLength - minTendrilLength);
        const path = buildTendrilPath(cx, cy, def.angleOffset, length);
        const tip = getTendrilEnd(cx, cy, def.angleOffset, length);
        return { ...def, length, path, tip, value };
      }),
    [geneValues, cx, cy, maxTendrilLength],
  );

  return (
    <View style={[styles.container, { width: size, height: size, opacity }]}>
      <BreathingWrapper size={size}>
        {/* Static SVG layer: nucleus + tendrils + tips */}
        <Svg
          width={size}
          height={size}
          viewBox={`0 0 ${size} ${size}`}
          style={StyleSheet.absoluteFill}
        >
          <G>
            {/* ── Nucleus Glow ── */}
            {/* Outermost glow ring */}
            <Circle
              cx={cx}
              cy={cy}
              r={nucleusRadius * 3}
              fill={color}
              opacity={0.08}
            />
            {/* Middle glow ring */}
            <Circle
              cx={cx}
              cy={cy}
              r={nucleusRadius * 2}
              fill={color}
              opacity={0.15}
            />
            {/* Nucleus core */}
            <Circle
              cx={cx}
              cy={cy}
              r={nucleusRadius}
              fill={color}
              opacity={0.6}
            />

            {/* ── Tendrils ── */}
            {tendrils.map((t) => (
              <Path
                key={`tendril-${t.geneKey}`}
                d={t.path}
                stroke={t.color}
                strokeWidth={2}
                strokeLinecap="round"
                fill="none"
                opacity={0.7}
              />
            ))}

            {/* ── Tendril Tips ── */}
            {tendrils.map((t) => (
              <Circle
                key={`tip-${t.geneKey}`}
                cx={t.tip.x}
                cy={t.tip.y}
                r={4}
                fill={t.color}
                opacity={0.8}
              />
            ))}
          </G>
        </Svg>

        {/* Animated particle layer: absolutely positioned over SVG */}
        {PARTICLE_DEFS.map((p, i) => (
          <OrbitalParticle
            key={`particle-${i}`}
            cx={cx}
            cy={cy}
            orbitRadius={p.orbitRadius}
            period={p.period}
            color={p.color}
            radius={p.radius}
            startAngle={p.startAngle}
          />
        ))}
      </BreathingWrapper>
    </View>
  );
}

/* ── Styles ------------------------------------------------------------------ */

const styles = StyleSheet.create({
  container: {
    alignItems: "center",
    justifyContent: "center",
  },
});
