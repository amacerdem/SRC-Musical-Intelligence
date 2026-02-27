import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { fonts } from "../../design/tokens";

/* ── Tier thresholds ──────────────────────────────────────────────── */

interface Tier {
  max: number;
  color: string;
}

const TIERS: Tier[] = [
  { max: 5, color: "#818CF8" },   // Seed        (indigo)
  { max: 15, color: "#22D3EE" },  // Sprout      (cyan)
  { max: 25, color: "#10B981" },  // Growth      (emerald)
  { max: 35, color: "#FBBF24" },  // Bloom       (gold)
  { max: 45, color: "#F472B6" },  // Harvest     (pink)
  { max: Infinity, color: "#EF4444" }, // Transcendent (red)
];

function getTierColor(level: number): string {
  for (const tier of TIERS) {
    if (level <= tier.max) return tier.color;
  }
  return TIERS[TIERS.length - 1].color;
}

/* ── Component ────────────────────────────────────────────────────── */

interface LevelBadgeProps {
  level: number;
  size?: number;
}

export function LevelBadge({ level, size = 40 }: LevelBadgeProps) {
  const color = getTierColor(level);
  const fontSize = size * 0.38;

  return (
    <View
      style={[
        styles.circle,
        {
          width: size,
          height: size,
          borderRadius: size / 2,
          backgroundColor: `${color}20`,
        },
      ]}
    >
      <Text
        style={[
          styles.label,
          {
            fontSize,
            color,
          },
        ]}
      >
        L{level}
      </Text>
    </View>
  );
}

/* ── Styles ───────────────────────────────────────────────────────── */

const styles = StyleSheet.create({
  circle: {
    alignItems: "center",
    justifyContent: "center",
  },
  label: {
    fontFamily: fonts.monoSemiBold,
  },
});
