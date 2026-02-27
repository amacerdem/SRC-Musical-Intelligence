/* -- MindGardenView -- 5x5 animated seed grid ----------------------------------
 *  Visualizes the user's Mind Garden: a living grid of listened tracks.
 *  Each active seed glows with its NeuralFamily color; empty slots are dim.
 *  Seasonal indicator, biodiversity score, and XP stats at the bottom.
 *  -------------------------------------------------------------------------- */

import React, { useMemo } from "react";
import { View, Text, StyleSheet, Dimensions } from "react-native";
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withRepeat,
  withTiming,
  withSequence,
  Easing,
} from "react-native-reanimated";
import { Ionicons } from "@expo/vector-icons";
import { useGamificationStore } from "../../stores/useGamificationStore";
import { colors, fonts, spacing, familyColors } from "../../design/tokens";
import { GlassCard } from "../ui/GlassCard";

/* -- Constants -------------------------------------------------------------- */

const GRID_SIZE = 5;
const TOTAL_CELLS = GRID_SIZE * GRID_SIZE;
const SCREEN_WIDTH = Dimensions.get("window").width;
const GRID_PADDING = spacing.lg;
const CELL_GAP = spacing.sm;
// Available width inside the GlassCard (padding: 16 from GlassCard + our own GRID_PADDING)
const GRID_INNER_WIDTH = SCREEN_WIDTH - spacing.xl * 2 - GRID_PADDING * 2;
const NODE_SIZE = (GRID_INNER_WIDTH - CELL_GAP * (GRID_SIZE - 1)) / GRID_SIZE;

const SEASON_CONFIG: Record<
  string,
  { icon: keyof typeof Ionicons.glyphMap; label: string; color: string }
> = {
  spring: { icon: "leaf", label: "Spring", color: "#10B981" },
  summer: { icon: "sunny", label: "Summer", color: "#FBBF24" },
  autumn: { icon: "cloudy", label: "Autumn", color: "#F97316" },
  winter: { icon: "snow", label: "Winter", color: "#38BDF8" },
};

/* -- Pulsing Seed Node ------------------------------------------------------ */

interface SeedNodeProps {
  familyColor: string | null;
  index: number;
}

function SeedNode({ familyColor, index }: SeedNodeProps) {
  const isActive = familyColor !== null;

  // Stagger the animation start per node so they don't all pulse in unison
  const pulseProgress = useSharedValue(0);

  React.useEffect(() => {
    if (!isActive) return;

    // Small stagger based on grid position
    const delay = (index % 7) * 120;

    const timeout = setTimeout(() => {
      pulseProgress.value = withRepeat(
        withSequence(
          withTiming(1, { duration: 1800, easing: Easing.inOut(Easing.ease) }),
          withTiming(0, { duration: 1800, easing: Easing.inOut(Easing.ease) }),
        ),
        -1, // infinite
        false,
      );
    }, delay);

    return () => clearTimeout(timeout);
  }, [isActive, index, pulseProgress]);

  const animatedStyle = useAnimatedStyle(() => {
    if (!isActive) return {};

    const scale = 1 + pulseProgress.value * 0.08;
    const glowOpacity = 0.25 + pulseProgress.value * 0.35;

    return {
      transform: [{ scale }],
      shadowOpacity: glowOpacity,
    };
  });

  if (!isActive) {
    return <View style={[styles.node, styles.emptyNode]} />;
  }

  return (
    <Animated.View
      style={[
        styles.node,
        {
          backgroundColor: `${familyColor}20`,
          borderColor: `${familyColor}60`,
          shadowColor: familyColor,
          shadowRadius: 10,
          shadowOffset: { width: 0, height: 0 },
        },
        animatedStyle,
      ]}
    >
      <View
        style={[styles.nodeCore, { backgroundColor: familyColor }]}
      />
    </Animated.View>
  );
}

/* -- Main Component --------------------------------------------------------- */

export function MindGardenView() {
  const { mindGarden, neuralPlasticity } = useGamificationStore();
  const {
    seedsPlanted,
    biodiversityScore,
    season,
    recentTracks,
  } = mindGarden;

  const seasonInfo = SEASON_CONFIG[season] ?? SEASON_CONFIG.spring;

  // Build the 25-cell grid: first N cells are filled from recentTracks, rest empty.
  // We cycle recentTracks if we have fewer than 25 but more than 0.
  const gridCells = useMemo(() => {
    const cells: (string | null)[] = [];
    for (let i = 0; i < TOTAL_CELLS; i++) {
      if (recentTracks.length === 0 || i >= seedsPlanted) {
        cells.push(null);
      } else {
        const track = recentTracks[i % recentTracks.length];
        const family = track.dominantFamily;
        cells.push(familyColors[family] ?? colors.violet);
      }
    }
    return cells;
  }, [recentTracks, seedsPlanted]);

  const biodiversityPercent = Math.round(biodiversityScore * 100);

  return (
    <GlassCard style={styles.container}>
      {/* -- Season Header --------------------------------------------------- */}
      <View style={styles.seasonRow}>
        <View style={styles.seasonBadge}>
          <Ionicons
            name={seasonInfo.icon}
            size={16}
            color={seasonInfo.color}
          />
          <Text style={[styles.seasonLabel, { color: seasonInfo.color }]}>
            {seasonInfo.label}
          </Text>
        </View>
        <Text style={styles.title}>Mind Garden</Text>
      </View>

      {/* -- 5x5 Seed Grid --------------------------------------------------- */}
      <View style={styles.gridContainer}>
        {Array.from({ length: GRID_SIZE }).map((_, row) => (
          <View key={`row-${row}`} style={styles.gridRow}>
            {Array.from({ length: GRID_SIZE }).map((_, col) => {
              const idx = row * GRID_SIZE + col;
              return (
                <SeedNode
                  key={`seed-${idx}`}
                  familyColor={gridCells[idx]}
                  index={idx}
                />
              );
            })}
          </View>
        ))}
      </View>

      {/* -- Stats Row ------------------------------------------------------- */}
      <View style={styles.statsRow}>
        <View style={styles.statItem}>
          <Ionicons name="sparkles" size={14} color={colors.violet} />
          <Text style={styles.statValue}>{seedsPlanted}</Text>
          <Text style={styles.statLabel}>Seeds</Text>
        </View>

        <View style={styles.statDivider} />

        <View style={styles.statItem}>
          <Ionicons name="color-palette-outline" size={14} color={colors.success} />
          <Text style={styles.statValue}>{biodiversityPercent}%</Text>
          <Text style={styles.statLabel}>Biodiversity</Text>
        </View>

        <View style={styles.statDivider} />

        <View style={styles.statItem}>
          <Ionicons name="flash" size={14} color={colors.reward} />
          <Text style={styles.statValue}>{neuralPlasticity}</Text>
          <Text style={styles.statLabel}>XP</Text>
        </View>
      </View>
    </GlassCard>
  );
}

/* -- Styles ----------------------------------------------------------------- */

const styles = StyleSheet.create({
  container: {
    paddingVertical: spacing.lg,
    paddingHorizontal: GRID_PADDING,
    gap: spacing.lg,
  },

  /* Season header */
  seasonRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  seasonBadge: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.xs,
    backgroundColor: "rgba(255,255,255,0.04)",
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
    borderRadius: 999,
  },
  seasonLabel: {
    fontSize: 12,
    fontFamily: fonts.bodySemiBold,
    letterSpacing: 0.4,
  },
  title: {
    fontSize: 14,
    fontFamily: fonts.heading,
    color: colors.textSecondary,
    letterSpacing: 0.5,
  },

  /* Grid */
  gridContainer: {
    alignItems: "center",
    gap: CELL_GAP,
  },
  gridRow: {
    flexDirection: "row",
    gap: CELL_GAP,
  },

  /* Seed nodes */
  node: {
    width: NODE_SIZE,
    height: NODE_SIZE,
    borderRadius: NODE_SIZE / 2,
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 1,
  },
  emptyNode: {
    backgroundColor: "rgba(255,255,255,0.02)",
    borderColor: "rgba(255,255,255,0.05)",
  },
  nodeCore: {
    width: NODE_SIZE * 0.4,
    height: NODE_SIZE * 0.4,
    borderRadius: (NODE_SIZE * 0.4) / 2,
    opacity: 0.9,
  },

  /* Stats */
  statsRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-around",
    paddingTop: spacing.sm,
    borderTopWidth: StyleSheet.hairlineWidth,
    borderTopColor: "rgba(255,255,255,0.06)",
  },
  statItem: {
    alignItems: "center",
    gap: 2,
  },
  statValue: {
    fontSize: 16,
    fontFamily: fonts.heading,
    color: colors.textPrimary,
    letterSpacing: 0.3,
  },
  statLabel: {
    fontSize: 10,
    fontFamily: fonts.body,
    color: colors.textTertiary,
    textTransform: "uppercase",
    letterSpacing: 0.6,
  },
  statDivider: {
    width: 1,
    height: 28,
    backgroundColor: "rgba(255,255,255,0.06)",
  },
});
