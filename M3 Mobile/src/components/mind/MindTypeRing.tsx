/* -- MindTypeRing -- Circular donut chart for gene proportions ---------------
 *  5 segments colored by gene. Dominant gene name shown in center.
 *  Uses SVG circles with strokeDasharray for donut segments.
 *  ----------------------------------------------------------------------- */

import React, { useMemo } from "react";
import { View, Text, StyleSheet } from "react-native";
import Svg, { Circle } from "react-native-svg";
import type { MindGenes, GeneName } from "../../types/m3";
import { GENE_NAMES, getDominantGene, GENE_TO_TYPE } from "../../types/m3";
import { colors, fonts } from "../../design/tokens";

interface MindTypeRingProps {
  genes: MindGenes;
  size?: number;
  strokeWidth?: number;
}

const GENE_RING_COLORS: Record<GeneName, string> = {
  entropy: colors.tempo,       // orange
  resolution: colors.familiarity, // blue
  tension: "#EF4444",           // red
  resonance: colors.success,   // green
  plasticity: colors.reward,   // amber
};

const GENE_SHORT_LABELS: Record<GeneName, string> = {
  entropy: "Entropy",
  resolution: "Resolution",
  tension: "Tension",
  resonance: "Resonance",
  plasticity: "Plasticity",
};

export function MindTypeRing({ genes, size = 160, strokeWidth = 12 }: MindTypeRingProps) {
  const cx = size / 2;
  const cy = size / 2;
  const radius = (size - strokeWidth) / 2 - 2;
  const circumference = 2 * Math.PI * radius;

  const dominantGene = getDominantGene(genes);
  const dominantFamily = GENE_TO_TYPE[dominantGene];
  const dominantColor = GENE_RING_COLORS[dominantGene];

  // Compute proportional arcs
  const segments = useMemo(() => {
    const total = GENE_NAMES.reduce((sum, g) => sum + Math.max(0.01, genes[g]), 0);
    let offset = 0;

    return GENE_NAMES.map((g) => {
      const proportion = Math.max(0.01, genes[g]) / total;
      const dashLength = proportion * circumference;
      const gapLength = circumference - dashLength;
      const currentOffset = offset;
      offset += proportion * circumference;

      return {
        key: g,
        color: GENE_RING_COLORS[g],
        dashArray: `${dashLength} ${gapLength}`,
        dashOffset: -currentOffset,
        proportion,
      };
    });
  }, [genes, circumference]);

  return (
    <View style={[styles.container, { width: size, height: size }]}>
      <Svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        {/* Background ring */}
        <Circle
          cx={cx}
          cy={cy}
          r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.04)"
          strokeWidth={strokeWidth}
        />

        {/* Gene segments */}
        {segments.map((seg) => (
          <Circle
            key={seg.key}
            cx={cx}
            cy={cy}
            r={radius}
            fill="none"
            stroke={seg.color}
            strokeWidth={strokeWidth}
            strokeDasharray={seg.dashArray}
            strokeDashoffset={seg.dashOffset}
            strokeLinecap="round"
            transform={`rotate(-90 ${cx} ${cy})`}
            opacity={seg.key === dominantGene ? 1 : 0.6}
          />
        ))}
      </Svg>

      {/* Center label */}
      <View style={styles.centerLabel}>
        <Text style={[styles.dominantName, { color: dominantColor }]}>
          {GENE_SHORT_LABELS[dominantGene]}
        </Text>
        <Text style={styles.familyLabel}>{dominantFamily}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: "center",
    justifyContent: "center",
  },
  centerLabel: {
    position: "absolute",
    alignItems: "center",
    gap: 2,
  },
  dominantName: {
    fontSize: 14,
    fontFamily: fonts.heading,
    letterSpacing: 0.5,
  },
  familyLabel: {
    fontSize: 10,
    fontFamily: fonts.body,
    color: colors.textTertiary,
    textTransform: "uppercase",
    letterSpacing: 0.8,
  },
});
