/* -- LeaderboardScreen -- Full-page ranked user leaderboard ------------------
 *  Layout (ScrollView):
 *    1. Header — "Leaderboard" title
 *    2. Filter bar — All Time / Weekly / By Level sort modes
 *    3. Ranked user rows — avatar, name, persona, level, XP, country, streak
 *    4. Top 3 get podium-style colored borders (gold / silver / bronze)
 *  -------------------------------------------------------------------------- */

import React, { useState, useMemo } from "react";
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Animated, { FadeInDown } from "react-native-reanimated";
import { Ionicons } from "@expo/vector-icons";
import { mockUsers } from "../../data/mock-users";
import { getPersona } from "../../data/personas";
import { GlassCard } from "../../components/ui/GlassCard";
import { Badge } from "../../components/ui/Badge";
import { colors, fonts, spacing, familyColors } from "../../design/tokens";

const { width: SCREEN_WIDTH } = Dimensions.get("window");

/* -- Types ----------------------------------------------------------------- */

type SortMode = "xp" | "level" | "streak";

/* -- Helpers --------------------------------------------------------------- */

/** Convert ISO 3166-1 alpha-2 country code to flag emoji. */
function countryFlag(code: string): string {
  const base = 0x1f1e6 - 65; // 'A' char code offset for regional indicators
  return String.fromCodePoint(
    ...code
      .toUpperCase()
      .split("")
      .map((c) => base + c.charCodeAt(0)),
  );
}

/** Podium colors for ranks 1-3. */
const PODIUM_COLORS: Record<number, string> = {
  1: "#FBBF24", // gold
  2: "#94A3B8", // silver
  3: "#CD7F32", // bronze
};

/* -- Filter Button --------------------------------------------------------- */

function FilterButton({
  label,
  active,
  onPress,
}: {
  label: string;
  active: boolean;
  onPress: () => void;
}) {
  return (
    <TouchableOpacity
      activeOpacity={0.7}
      onPress={onPress}
      style={[styles.filterButton, active && styles.filterButtonActive]}
    >
      <Text
        style={[styles.filterLabel, active && styles.filterLabelActive]}
      >
        {label}
      </Text>
    </TouchableOpacity>
  );
}

/* -- Leaderboard Row ------------------------------------------------------- */

function LeaderboardRow({
  rank,
  user,
  index,
}: {
  rank: number;
  user: (typeof mockUsers)[number];
  index: number;
}) {
  const persona = getPersona(user.mind.personaId);
  const familyColor = familyColors[persona.family] ?? colors.violet;
  const podiumColor = PODIUM_COLORS[rank];
  const isTopThree = rank <= 3;

  return (
    <Animated.View entering={FadeInDown.delay(80 * index).duration(400)}>
      <GlassCard
        intensity={isTopThree ? "high" : "medium"}
        style={[
          styles.rowCard,
          isTopThree && {
            borderColor: podiumColor,
            borderWidth: 1.5,
          },
        ]}
      >
        <View style={styles.rowInner}>
          {/* Rank */}
          <View style={styles.rankContainer}>
            {isTopThree ? (
              <Ionicons
                name="trophy"
                size={18}
                color={podiumColor}
              />
            ) : (
              <Text style={styles.rankNumber}>{rank}</Text>
            )}
          </View>

          {/* Avatar initial circle */}
          <View style={[styles.avatarCircle, { borderColor: familyColor }]}>
            <Text style={[styles.avatarInitial, { color: familyColor }]}>
              {user.displayName.charAt(0)}
            </Text>
          </View>

          {/* Name + persona */}
          <View style={styles.userInfo}>
            <View style={styles.nameRow}>
              <Text style={styles.displayName} numberOfLines={1}>
                {user.displayName}
              </Text>
              <Text style={styles.countryFlag}>{countryFlag(user.country)}</Text>
            </View>
            <Text style={[styles.personaLabel, { color: familyColor }]} numberOfLines={1}>
              {persona.name}
            </Text>
          </View>

          {/* Stats column */}
          <View style={styles.statsColumn}>
            {/* Level badge */}
            <Badge label={`L${user.level}`} color={familyColor} />

            {/* XP */}
            <Text style={styles.xpText}>
              {user.xp >= 1000
                ? `${(user.xp / 1000).toFixed(user.xp >= 10000 ? 0 : 1)}k`
                : user.xp}{" "}
              XP
            </Text>
          </View>

          {/* Streak */}
          <View style={styles.streakContainer}>
            <Ionicons name="flame" size={14} color={colors.tempo} />
            <Text style={styles.streakText}>{user.streak}</Text>
          </View>
        </View>
      </GlassCard>
    </Animated.View>
  );
}

/* -- LeaderboardScreen ----------------------------------------------------- */

export function LeaderboardScreen() {
  const [sortMode, setSortMode] = useState<SortMode>("xp");

  const sortedUsers = useMemo(() => {
    const users = [...mockUsers];
    switch (sortMode) {
      case "xp":
        return users.sort((a, b) => b.xp - a.xp);
      case "level":
        return users.sort((a, b) => b.level - a.level || b.xp - a.xp);
      case "streak":
        return users.sort((a, b) => b.streak - a.streak || b.xp - a.xp);
    }
  }, [sortMode]);

  return (
    <SafeAreaView style={styles.safeArea}>
      {/* Header */}
      <Animated.View
        entering={FadeInDown.delay(0).duration(400)}
        style={styles.header}
      >
        <Ionicons name="podium" size={24} color={colors.violet} />
        <Text style={styles.headerTitle}>Leaderboard</Text>
      </Animated.View>

      {/* Filter bar */}
      <Animated.View
        entering={FadeInDown.delay(40).duration(400)}
        style={styles.filterBar}
      >
        <FilterButton
          label="All Time"
          active={sortMode === "xp"}
          onPress={() => setSortMode("xp")}
        />
        <FilterButton
          label="By Level"
          active={sortMode === "level"}
          onPress={() => setSortMode("level")}
        />
        <FilterButton
          label="By Streak"
          active={sortMode === "streak"}
          onPress={() => setSortMode("streak")}
        />
      </Animated.View>

      {/* User list */}
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {sortedUsers.map((user, index) => (
          <LeaderboardRow
            key={user.id}
            rank={index + 1}
            user={user}
            index={index}
          />
        ))}

        {/* Bottom spacer for tab bar */}
        <View style={{ height: 100 }} />
      </ScrollView>
    </SafeAreaView>
  );
}

/* -- Styles ----------------------------------------------------------------- */

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: colors.background,
  },

  /* Header */
  header: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.md,
    paddingBottom: spacing.sm,
  },
  headerTitle: {
    fontSize: 28,
    fontFamily: fonts.display,
    color: colors.textPrimary,
    letterSpacing: 0.3,
  },

  /* Filter bar */
  filterBar: {
    flexDirection: "row",
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.md,
    gap: spacing.sm,
  },
  filterButton: {
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.sm,
    borderRadius: 20,
    backgroundColor: colors.surface,
    borderWidth: StyleSheet.hairlineWidth,
    borderColor: colors.border,
  },
  filterButtonActive: {
    backgroundColor: `${colors.violet}20`,
    borderColor: colors.violet,
  },
  filterLabel: {
    fontSize: 13,
    fontFamily: fonts.bodySemiBold,
    color: colors.textTertiary,
  },
  filterLabelActive: {
    color: colors.violet,
  },

  /* Scroll */
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.xs,
  },

  /* Row card */
  rowCard: {
    marginBottom: spacing.sm,
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.md,
  },
  rowInner: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.md,
  },

  /* Rank */
  rankContainer: {
    width: 28,
    alignItems: "center",
    justifyContent: "center",
  },
  rankNumber: {
    fontSize: 16,
    fontFamily: fonts.monoSemiBold,
    color: colors.textTertiary,
  },

  /* Avatar */
  avatarCircle: {
    width: 42,
    height: 42,
    borderRadius: 21,
    borderWidth: 2,
    backgroundColor: colors.surface,
    alignItems: "center",
    justifyContent: "center",
  },
  avatarInitial: {
    fontSize: 18,
    fontFamily: fonts.display,
  },

  /* User info */
  userInfo: {
    flex: 1,
    gap: 2,
  },
  nameRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.xs,
  },
  displayName: {
    fontSize: 15,
    fontFamily: fonts.heading,
    color: colors.textPrimary,
    flexShrink: 1,
  },
  countryFlag: {
    fontSize: 14,
  },
  personaLabel: {
    fontSize: 11,
    fontFamily: fonts.bodySemiBold,
    letterSpacing: 0.3,
  },

  /* Stats */
  statsColumn: {
    alignItems: "flex-end",
    gap: 4,
  },
  xpText: {
    fontSize: 11,
    fontFamily: fonts.mono,
    color: colors.textSecondary,
  },

  /* Streak */
  streakContainer: {
    flexDirection: "row",
    alignItems: "center",
    gap: 2,
    minWidth: 36,
    justifyContent: "flex-end",
  },
  streakText: {
    fontSize: 13,
    fontFamily: fonts.monoSemiBold,
    color: colors.tempo,
  },
});
