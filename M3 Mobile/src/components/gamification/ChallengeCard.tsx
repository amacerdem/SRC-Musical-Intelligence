import React, { useMemo } from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { colors, fonts, spacing } from "../../design/tokens";
import type { Challenge } from "../../types/game";

/* ── Type-to-visual mappings ──────────────────────────────────────── */

const TYPE_COLORS: Record<Challenge["type"], string> = {
  prediction: "#818CF8",
  entropy: "#22D3EE",
  resolution: "#FBBF24",
  fusion: "#F472B6",
};

const TYPE_ICONS: Record<Challenge["type"], keyof typeof Ionicons.glyphMap> = {
  prediction: "eye",
  entropy: "pulse",
  resolution: "key",
  fusion: "git-merge",
};

/* ── Time-remaining helper ────────────────────────────────────────── */

function formatTimeRemaining(endsAt: string): string {
  const diff = new Date(endsAt).getTime() - Date.now();
  if (diff <= 0) return "Ended";

  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
  const minutes = Math.floor((diff / (1000 * 60)) % 60);

  if (days > 0) return `${days}d ${hours}h left`;
  if (hours > 0) return `${hours}h ${minutes}m left`;
  return `${minutes}m left`;
}

/* ── Participant formatter ────────────────────────────────────────── */

function formatParticipants(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M joined`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(n >= 10_000 ? 0 : 1).replace(/\.0$/, "")}K joined`;
  return `${n.toLocaleString()} joined`;
}

/* ── Component ────────────────────────────────────────────────────── */

interface ChallengeCardProps {
  challenge: Challenge;
  onJoin?: () => void;
}

export function ChallengeCard({ challenge, onJoin }: ChallengeCardProps) {
  const accent = TYPE_COLORS[challenge.type];
  const icon = TYPE_ICONS[challenge.type];
  const timeLeft = useMemo(() => formatTimeRemaining(challenge.endsAt), [challenge.endsAt]);
  const ended = timeLeft === "Ended";

  return (
    <View style={styles.card}>
      {/* Gradient left accent */}
      <View style={[styles.accent, { backgroundColor: accent }]} />

      <View style={styles.content}>
        {/* Header row: icon + time */}
        <View style={styles.headerRow}>
          <View style={[styles.iconCircle, { backgroundColor: `${accent}20` }]}>
            <Ionicons name={icon} size={16} color={accent} />
          </View>
          <Text style={[styles.timeText, ended && styles.timeEnded]}>{timeLeft}</Text>
        </View>

        {/* Title */}
        <Text style={styles.title} numberOfLines={1}>
          {challenge.title}
        </Text>

        {/* Description */}
        <Text style={styles.description} numberOfLines={2}>
          {challenge.description}
        </Text>

        {/* Bottom row: XP badge, participants, Join button */}
        <View style={styles.bottomRow}>
          <View style={[styles.xpBadge, { backgroundColor: `${accent}18` }]}>
            <Text style={[styles.xpText, { color: accent }]}>+{challenge.xpReward} XP</Text>
          </View>

          <Text style={styles.participants}>
            {formatParticipants(challenge.participants)}
          </Text>

          <TouchableOpacity
            style={[styles.joinButton, { backgroundColor: accent }, ended && styles.joinDisabled]}
            onPress={onJoin}
            activeOpacity={0.7}
            disabled={ended}
          >
            <Text style={styles.joinText}>{ended ? "Ended" : "Join"}</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}

/* ── Styles ───────────────────────────────────────────────────────── */

const styles = StyleSheet.create({
  card: {
    flexDirection: "row",
    backgroundColor: colors.surfaceMedium,
    borderRadius: 16,
    borderWidth: StyleSheet.hairlineWidth,
    borderColor: colors.border,
    overflow: "hidden",
  },
  accent: {
    width: 4,
  },
  content: {
    flex: 1,
    padding: spacing.lg,
  },
  headerRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: spacing.sm,
  },
  iconCircle: {
    width: 32,
    height: 32,
    borderRadius: 16,
    alignItems: "center",
    justifyContent: "center",
  },
  timeText: {
    fontFamily: fonts.mono,
    fontSize: 11,
    color: colors.textSecondary,
  },
  timeEnded: {
    color: colors.danger,
  },
  title: {
    fontFamily: fonts.heading,
    fontSize: 16,
    color: colors.textPrimary,
    marginBottom: spacing.xs,
  },
  description: {
    fontFamily: fonts.body,
    fontSize: 13,
    color: colors.textSecondary,
    lineHeight: 18,
    marginBottom: spacing.md,
  },
  bottomRow: {
    flexDirection: "row",
    alignItems: "center",
  },
  xpBadge: {
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
  },
  xpText: {
    fontFamily: fonts.monoSemiBold,
    fontSize: 11,
  },
  participants: {
    flex: 1,
    fontFamily: fonts.body,
    fontSize: 12,
    color: colors.textTertiary,
    marginLeft: spacing.sm,
  },
  joinButton: {
    paddingHorizontal: 16,
    paddingVertical: 6,
    borderRadius: 8,
  },
  joinDisabled: {
    opacity: 0.4,
  },
  joinText: {
    fontFamily: fonts.heading,
    fontSize: 13,
    color: "#FFFFFF",
  },
});
