/* -- SocialFeedScreen -- Community Activity Feed ------------------------------
 *  Displays recent activity from the M3 community:
 *    evolution, creation, compatibility, achievement,
 *    challenge, performance, composition, listening
 *  -------------------------------------------------------------------------- */

import React from "react";
import { View, Text, FlatList, StyleSheet } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Animated, { FadeInDown } from "react-native-reanimated";
import { Ionicons } from "@expo/vector-icons";
import { mockActivity } from "../../data/mock-users";
import { GlassCard } from "../../components/ui/GlassCard";
import { colors, fonts, spacing } from "../../design/tokens";
import type { ActivityItem } from "../../types/social";

/* -- Type configuration ---------------------------------------------------- */

type ActivityType = ActivityItem["type"];

const TYPE_ICONS: Record<ActivityType, keyof typeof Ionicons.glyphMap> = {
  evolution: "rocket",
  creation: "brush",
  compatibility: "heart",
  achievement: "trophy",
  challenge: "flag",
  performance: "radio",
  composition: "musical-notes",
  listening: "headset",
};

const TYPE_COLORS: Record<ActivityType, string> = {
  evolution: "#8B5CF6",
  creation: "#22D3EE",
  compatibility: "#F472B6",
  achievement: "#FBBF24",
  challenge: "#F97316",
  performance: "#10B981",
  composition: "#818CF8",
  listening: "#94A3B8",
};

/* -- Relative time helper -------------------------------------------------- */

function formatRelativeTime(timestamp: string): string {
  const now = Date.now();
  const then = new Date(timestamp).getTime();
  const diffMs = now - then;

  const minutes = Math.floor(diffMs / 60_000);
  const hours = Math.floor(diffMs / 3_600_000);
  const days = Math.floor(diffMs / 86_400_000);

  if (minutes < 1) return "Just now";
  if (minutes < 60) return `${minutes}m ago`;
  if (hours < 24) return `${hours}h ago`;
  if (days === 1) return "Yesterday";
  if (days < 7) return `${days}d ago`;
  if (days < 30) return `${Math.floor(days / 7)}w ago`;
  return `${Math.floor(days / 30)}mo ago`;
}

/* -- Activity Row ---------------------------------------------------------- */

function ActivityRow({
  item,
  index,
}: {
  item: ActivityItem;
  index: number;
}) {
  const iconName = TYPE_ICONS[item.type];
  const accentColor = TYPE_COLORS[item.type];

  return (
    <Animated.View entering={FadeInDown.delay(index * 60).duration(400)}>
      <GlassCard style={styles.card}>
        <View style={[styles.accentBorder, { backgroundColor: accentColor }]} />

        <View style={styles.cardContent}>
          {/* Icon */}
          <View style={[styles.iconCircle, { backgroundColor: `${accentColor}18` }]}>
            <Ionicons name={iconName} size={18} color={accentColor} />
          </View>

          {/* Text */}
          <View style={styles.textContainer}>
            <Text style={styles.messageText} numberOfLines={3}>
              <Text style={styles.userName}>{item.userName}</Text>
              {"  "}
              {item.message}
            </Text>
            <Text style={[styles.timestamp, { color: accentColor }]}>
              {formatRelativeTime(item.timestamp)}
            </Text>
          </View>
        </View>
      </GlassCard>
    </Animated.View>
  );
}

/* -- SocialFeedScreen ------------------------------------------------------ */

export function SocialFeedScreen() {
  const renderItem = ({ item, index }: { item: ActivityItem; index: number }) => (
    <ActivityRow item={item} index={index} />
  );

  return (
    <SafeAreaView style={styles.safeArea}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Activity</Text>
      </View>

      {/* Feed */}
      <FlatList
        data={mockActivity}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        contentContainerStyle={styles.listContent}
        showsVerticalScrollIndicator={false}
        ListEmptyComponent={
          <View style={styles.emptyState}>
            <Ionicons name="people" size={48} color={colors.textTertiary} />
            <Text style={styles.emptyTitle}>No Activity Yet</Text>
            <Text style={styles.emptySubtitle}>
              Community activity will appear here as minds evolve, create, and connect.
            </Text>
          </View>
        }
      />
    </SafeAreaView>
  );
}

/* -- Styles ---------------------------------------------------------------- */

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: colors.background,
  },

  /* Header */
  header: {
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.md,
    paddingBottom: spacing.lg,
  },
  headerTitle: {
    fontSize: 28,
    fontFamily: fonts.display,
    color: colors.textPrimary,
    letterSpacing: 0.3,
  },

  /* List */
  listContent: {
    paddingHorizontal: spacing.lg,
    paddingBottom: 100,
    gap: spacing.md,
  },

  /* Card */
  card: {
    flexDirection: "row",
    overflow: "hidden",
    padding: 0,
  },
  accentBorder: {
    width: 3,
    borderTopLeftRadius: 16,
    borderBottomLeftRadius: 16,
  },
  cardContent: {
    flex: 1,
    flexDirection: "row",
    alignItems: "flex-start",
    padding: spacing.lg,
    gap: spacing.md,
  },

  /* Icon */
  iconCircle: {
    width: 36,
    height: 36,
    borderRadius: 18,
    alignItems: "center",
    justifyContent: "center",
  },

  /* Text */
  textContainer: {
    flex: 1,
    gap: spacing.xs,
  },
  userName: {
    fontFamily: fonts.bodySemiBold,
    color: colors.textPrimary,
    fontSize: 14,
  },
  messageText: {
    fontFamily: fonts.body,
    color: colors.textSecondary,
    fontSize: 14,
    lineHeight: 20,
  },
  timestamp: {
    fontSize: 11,
    fontFamily: fonts.mono,
    marginTop: 2,
  },

  /* Empty state */
  emptyState: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    paddingTop: 120,
    gap: spacing.md,
  },
  emptyTitle: {
    fontSize: 20,
    fontFamily: fonts.heading,
    color: colors.textPrimary,
  },
  emptySubtitle: {
    fontSize: 14,
    fontFamily: fonts.body,
    color: colors.textSecondary,
    textAlign: "center",
    paddingHorizontal: spacing.xxl,
  },
});
