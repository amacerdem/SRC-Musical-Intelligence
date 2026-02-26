/* -- GeneStrands -- 5 horizontal animated gene bars -------------------------
 *  Displays entropy, resolution, tension, resonance, plasticity as colored
 *  bars with labels and percentage values. Animated fill via Reanimated.
 *  ----------------------------------------------------------------------- */

import React from "react";
import { View, Text, StyleSheet } from "react-native";
import Animated, {
  useAnimatedStyle,
  withTiming,
  Easing,
} from "react-native-reanimated";
import type { MindGenes } from "../../types/m3";
import { colors, fonts, spacing } from "../../design/tokens";

const GENE_CONFIG = [
  { key: "entropy" as const, label: "Entropy", color: colors.tempo },
  { key: "resolution" as const, label: "Resolution", color: colors.familiarity },
  { key: "tension" as const, label: "Tension", color: colors.danger },
  { key: "resonance" as const, label: "Resonance", color: colors.success },
  { key: "plasticity" as const, label: "Plasticity", color: colors.reward },
];

interface GeneStrandsProps {
  genes: MindGenes;
}

function GeneBar({ label, value, color }: { label: string; value: number; color: string }) {
  const pct = Math.round(value * 100);

  const fillStyle = useAnimatedStyle(() => ({
    width: withTiming(`${Math.min(100, Math.max(0, value * 100))}%`, {
      duration: 800,
      easing: Easing.out(Easing.cubic),
    }),
  }));

  return (
    <View style={styles.row}>
      <Text style={styles.label}>{label}</Text>
      <View style={styles.trackContainer}>
        <View style={styles.track}>
          <Animated.View
            style={[
              styles.fill,
              { backgroundColor: color },
              fillStyle,
            ]}
          />
        </View>
      </View>
      <Text style={[styles.value, { color }]}>{pct}%</Text>
    </View>
  );
}

export function GeneStrands({ genes }: GeneStrandsProps) {
  return (
    <View style={styles.container}>
      {GENE_CONFIG.map((g) => (
        <GeneBar
          key={g.key}
          label={g.label}
          value={genes[g.key]}
          color={g.color}
        />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    gap: spacing.md,
  },
  row: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
  },
  label: {
    width: 80,
    fontSize: 12,
    fontFamily: fonts.bodySemiBold,
    color: colors.textSecondary,
    letterSpacing: 0.3,
  },
  trackContainer: {
    flex: 1,
  },
  track: {
    height: 6,
    borderRadius: 3,
    backgroundColor: colors.surfaceHigh,
    overflow: "hidden",
  },
  fill: {
    height: "100%",
    borderRadius: 3,
  },
  value: {
    width: 38,
    textAlign: "right",
    fontSize: 12,
    fontFamily: fonts.monoSemiBold,
    letterSpacing: -0.3,
  },
});
