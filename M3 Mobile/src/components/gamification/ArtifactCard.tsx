/* -- ArtifactCard -- Collectible artifact display with glow effects --------
 *  Renders a focus artifact with family-colored border, rarity-based glow,
 *  lock overlay for unearned artifacts, and pulsating animation for Anomalous.
 *  ----------------------------------------------------------------------- */

import React from "react";
import { View, Text, StyleSheet } from "react-native";
import Animated, {
  useAnimatedStyle,
  useSharedValue,
  withRepeat,
  withTiming,
  Easing,
} from "react-native-reanimated";
import { Ionicons } from "@expo/vector-icons";
import type { FocusArtifact, Rarity, NeuralFamily } from "../../types/mind";
import { colors, fonts, spacing, familyColors } from "../../design/tokens";

/* -- Types ---------------------------------------------------------------- */

interface ArtifactCardProps {
  artifact: FocusArtifact;
  isLocked?: boolean;
  size?: "sm" | "md";
}

/* -- Constants ------------------------------------------------------------ */

const SIZE_MAP = {
  sm: 80,
  md: 120,
} as const;

const FAMILY_ICONS: Record<NeuralFamily, keyof typeof Ionicons.glyphMap> = {
  Architects: "construct",
  Alchemists: "flask",
  Explorers: "compass",
  Anchors: "heart",
  Kineticists: "flash",
};

const RARITY_BORDER_WIDTH: Record<Rarity, number> = {
  Common: 1,
  Rare: 2,
  Legendary: 3,
  Anomalous: 3,
};

const RARITY_LABEL_COLORS: Record<Rarity, string> = {
  Common: colors.textTertiary,
  Rare: colors.info,
  Legendary: colors.reward,
  Anomalous: "#EF4444",
};

/* -- Rarity shadow styles ------------------------------------------------- */

function rarityShadow(rarity: Rarity, familyColor: string) {
  switch (rarity) {
    case "Common":
      return {};
    case "Rare":
      return {
        shadowColor: familyColor,
        shadowOffset: { width: 0, height: 0 },
        shadowOpacity: 0.25,
        shadowRadius: 6,
        elevation: 4,
      };
    case "Legendary":
    case "Anomalous":
      return {
        shadowColor: familyColor,
        shadowOffset: { width: 0, height: 0 },
        shadowOpacity: 0.5,
        shadowRadius: 14,
        elevation: 8,
      };
  }
}

/* -- Component ------------------------------------------------------------ */

export function ArtifactCard({
  artifact,
  isLocked = false,
  size = "md",
}: ArtifactCardProps) {
  const dimension = SIZE_MAP[size];
  const familyColor = familyColors[artifact.family] ?? colors.violet;
  const borderWidth = RARITY_BORDER_WIDTH[artifact.rarity];
  const shadow = rarityShadow(artifact.rarity, familyColor);
  const isAnomalous = artifact.rarity === "Anomalous";
  const iconSize = size === "sm" ? 24 : 36;

  /* Pulse animation for Anomalous rarity */
  const pulse = useSharedValue(1);

  React.useEffect(() => {
    if (isAnomalous && !isLocked) {
      pulse.value = withRepeat(
        withTiming(0.5, { duration: 1200, easing: Easing.inOut(Easing.ease) }),
        -1,
        true,
      );
    }
  }, [isAnomalous, isLocked, pulse]);

  const pulseStyle = useAnimatedStyle(() => {
    if (!isAnomalous || isLocked) return {};
    return {
      shadowOpacity: pulse.value,
      borderColor: familyColor,
    };
  });

  return (
    <View style={styles.wrapper}>
      {/* Card body */}
      <Animated.View
        style={[
          styles.card,
          {
            width: dimension,
            height: dimension,
            borderWidth,
            borderColor: isLocked ? colors.border : familyColor,
            backgroundColor: isLocked
              ? "rgba(255,255,255,0.02)"
              : `${familyColor}10`,
          },
          !isLocked && shadow,
          isAnomalous && !isLocked && pulseStyle,
        ]}
      >
        {/* Family icon */}
        <Ionicons
          name={FAMILY_ICONS[artifact.family]}
          size={iconSize}
          color={isLocked ? colors.textMuted : familyColor}
          style={isLocked ? styles.grayscaleIcon : undefined}
        />

        {/* Lock overlay */}
        {isLocked && (
          <View style={styles.lockOverlay}>
            <Ionicons name="lock-closed" size={size === "sm" ? 20 : 28} color={colors.textTertiary} />
          </View>
        )}

        {/* Rarity label inside card bottom */}
        <Text
          style={[
            styles.rarityLabel,
            {
              fontSize: size === "sm" ? 8 : 10,
              color: isLocked ? colors.textMuted : RARITY_LABEL_COLORS[artifact.rarity],
            },
          ]}
          numberOfLines={1}
        >
          {artifact.rarity}
        </Text>
      </Animated.View>

      {/* Artifact name below card */}
      <Text
        style={[
          styles.name,
          {
            maxWidth: dimension,
            color: isLocked ? colors.textMuted : colors.textSecondary,
          },
        ]}
        numberOfLines={1}
      >
        {artifact.name}
      </Text>
    </View>
  );
}

/* -- Styles --------------------------------------------------------------- */

const styles = StyleSheet.create({
  wrapper: {
    alignItems: "center",
    gap: spacing.xs,
  },
  card: {
    borderRadius: 14,
    alignItems: "center",
    justifyContent: "center",
    overflow: "hidden",
  },
  lockOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: "rgba(0,0,0,0.55)",
    alignItems: "center",
    justifyContent: "center",
    borderRadius: 14,
  },
  grayscaleIcon: {
    opacity: 0.3,
  },
  rarityLabel: {
    position: "absolute",
    bottom: 6,
    fontFamily: fonts.mono,
    textTransform: "uppercase",
    letterSpacing: 0.8,
  },
  name: {
    fontSize: 11,
    fontFamily: fonts.bodySemiBold,
    textAlign: "center",
    letterSpacing: 0.2,
  },
});
