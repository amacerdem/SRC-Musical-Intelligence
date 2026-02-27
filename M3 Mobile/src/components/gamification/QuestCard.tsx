/* -- QuestCard -- Active quest display with progress bar -------------------
 *  Shows quest title, description, type icon, status badge, progress,
 *  and time remaining. Left accent border colored by quest type.
 *  ----------------------------------------------------------------------- */

import React from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { ProgressBar } from "../ui/ProgressBar";
import { Badge } from "../ui/Badge";
import { colors, fonts, spacing } from "../../design/tokens";

/* -- Types ---------------------------------------------------------------- */

interface Quest {
  id: string;
  title: string;
  description: string;
  type: "ritual" | "anomaly" | "scavenger_hunt";
  status: "active" | "completed" | "failed";
  progress: number; // 0-100
  targetFamily?: string;
  expiresAt: number;
}

interface QuestCardProps {
  quest: Quest;
  onComplete?: () => void;
}

/* -- Constants ------------------------------------------------------------ */

const TYPE_COLORS: Record<Quest["type"], string> = {
  ritual: "#8B5CF6",
  anomaly: "#22D3EE",
  scavenger_hunt: "#F97316",
};

const TYPE_ICONS: Record<Quest["type"], keyof typeof Ionicons.glyphMap> = {
  ritual: "flame",
  anomaly: "git-branch",
  scavenger_hunt: "search",
};

const STATUS_COLORS: Record<Quest["status"], string> = {
  active: colors.violet,
  completed: colors.success,
  failed: colors.danger,
};

/* -- Helpers -------------------------------------------------------------- */

function formatTimeRemaining(expiresAt: number): string {
  const diff = expiresAt - Date.now();
  if (diff <= 0) return "Expired";

  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

  if (hours > 24) {
    const days = Math.floor(hours / 24);
    return `${days}d ${hours % 24}h left`;
  }
  if (hours > 0) {
    return `${hours}h ${minutes}m left`;
  }
  return `${minutes}m left`;
}

/* -- Component ------------------------------------------------------------ */

export function QuestCard({ quest, onComplete }: QuestCardProps) {
  const accentColor = TYPE_COLORS[quest.type];
  const iconName = TYPE_ICONS[quest.type];
  const statusColor = STATUS_COLORS[quest.status];
  const isCompleted = quest.status === "completed";

  return (
    <TouchableOpacity
      activeOpacity={isCompleted ? 1 : 0.7}
      onPress={isCompleted ? undefined : onComplete}
      disabled={quest.status !== "active"}
    >
      <View
        style={[
          styles.card,
          { borderLeftColor: accentColor },
        ]}
      >
        {/* Completed overlay */}
        {isCompleted && (
          <View style={styles.completedOverlay}>
            <Ionicons name="checkmark-circle" size={40} color={colors.success} />
          </View>
        )}

        {/* Header row: icon + title + status badge */}
        <View style={styles.header}>
          <View style={[styles.iconContainer, { backgroundColor: `${accentColor}20` }]}>
            <Ionicons name={iconName} size={18} color={accentColor} />
          </View>

          <View style={styles.titleBlock}>
            <Text style={styles.title} numberOfLines={1}>
              {quest.title}
            </Text>
            <Text style={styles.description} numberOfLines={2}>
              {quest.description}
            </Text>
          </View>

          <Badge label={quest.status} color={statusColor} />
        </View>

        {/* Progress section */}
        <View style={styles.progressSection}>
          <ProgressBar
            progress={quest.progress / 100}
            color={accentColor}
            height={5}
          />
          <View style={styles.progressMeta}>
            <Text style={styles.progressText}>{Math.round(quest.progress)}%</Text>
            <Text style={styles.timeText}>{formatTimeRemaining(quest.expiresAt)}</Text>
          </View>
        </View>
      </View>
    </TouchableOpacity>
  );
}

/* -- Styles --------------------------------------------------------------- */

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.surfaceMedium,
    borderRadius: 14,
    borderWidth: StyleSheet.hairlineWidth,
    borderColor: colors.border,
    borderLeftWidth: 4,
    padding: spacing.lg,
    gap: spacing.md,
    overflow: "hidden",
  },
  completedOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: "rgba(0,0,0,0.5)",
    zIndex: 10,
    alignItems: "center",
    justifyContent: "center",
    borderRadius: 14,
  },
  header: {
    flexDirection: "row",
    alignItems: "flex-start",
    gap: spacing.md,
  },
  iconContainer: {
    width: 36,
    height: 36,
    borderRadius: 10,
    alignItems: "center",
    justifyContent: "center",
  },
  titleBlock: {
    flex: 1,
    gap: 2,
  },
  title: {
    fontSize: 15,
    fontFamily: fonts.heading,
    color: colors.textPrimary,
    letterSpacing: 0.2,
  },
  description: {
    fontSize: 12,
    fontFamily: fonts.body,
    color: colors.textTertiary,
    lineHeight: 16,
  },
  progressSection: {
    gap: spacing.xs,
  },
  progressMeta: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  progressText: {
    fontSize: 11,
    fontFamily: fonts.monoSemiBold,
    color: colors.textSecondary,
    letterSpacing: -0.3,
  },
  timeText: {
    fontSize: 11,
    fontFamily: fonts.body,
    color: colors.textTertiary,
  },
});
