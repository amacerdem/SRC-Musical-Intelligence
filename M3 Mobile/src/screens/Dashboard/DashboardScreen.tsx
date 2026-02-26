/* -- DashboardScreen -- Scrollable Stats & Insights Page --------------------
 *  Layout (ScrollView):
 *    1. HUD Stats Bar — streak, tracks, level, XP
 *    2. Persona Identity Card — avatar, name, family, evolution %
 *    3. Mind Radar — 5-axis SVG pentagon
 *    4. Gene Distribution — MindTypeRing donut chart
 *    5. Weekly Listening — 7-bar chart (Mon-Sun)
 *    6. Belief Traces — 5 mini sparklines
 *    7. Active Functions — 3x3 grid F1-F9
 *    8. Brain Monologue — typewriter text
 *  -------------------------------------------------------------------------- */

import React, { useMemo, useEffect, useState } from "react";
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  Dimensions,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Animated, {
  FadeInDown,
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withDelay,
  Easing,
} from "react-native-reanimated";
import Svg, { Polyline } from "react-native-svg";
import { Ionicons } from "@expo/vector-icons";
import { useM3Store } from "../../stores/useM3Store";
import { useUserStore } from "../../stores/useUserStore";
import { getPersona } from "../../data/personas";
import { getLevelName } from "../../data/persona-levels";
import { generateTrace } from "../../data/mock-traces";
import { weeklyStats } from "../../data/mock-listening";
import { GlassCard } from "../../components/ui/GlassCard";
import { Badge } from "../../components/ui/Badge";
import { ProgressBar } from "../../components/ui/ProgressBar";
import { MindRadar } from "../../components/mind/MindRadar";
import { MindTypeRing } from "../../components/mind/MindTypeRing";
import { WeeklyChart } from "../../components/dashboard/WeeklyChart";
import { FunctionsGrid } from "../../components/dashboard/FunctionsGrid";
import { colors, fonts, spacing, familyColors } from "../../design/tokens";
import { getDominantType } from "../../types/m3";
import type { BeliefTrace } from "../../types/mind";

const { width: SCREEN_WIDTH } = Dimensions.get("window");
const SPARKLINE_WIDTH = (SCREEN_WIDTH - 80) / 2.5;
const SPARKLINE_HEIGHT = 36;

/* -- HUD Stats Bar --------------------------------------------------------- */

function HUDStatsBar({
  streak,
  tracks,
  level,
  xpProgress,
}: {
  streak: number;
  tracks: number;
  level: number;
  xpProgress: number;
}) {
  return (
    <View style={styles.hudBar}>
      {/* Streak */}
      <View style={styles.hudItem}>
        <Ionicons name="flame" size={16} color={colors.tempo} />
        <Text style={styles.hudValue}>{streak}</Text>
        <Text style={styles.hudLabel}>days</Text>
      </View>

      {/* Tracks */}
      <View style={styles.hudItem}>
        <Ionicons name="musical-notes" size={16} color={colors.consonance} />
        <Text style={styles.hudValue}>{tracks}</Text>
        <Text style={styles.hudLabel}>tracks</Text>
      </View>

      {/* Level */}
      <View style={styles.hudItem}>
        <Ionicons name="star" size={16} color={colors.reward} />
        <Text style={styles.hudValue}>L{level}</Text>
      </View>

      {/* XP Bar */}
      <View style={styles.hudXpContainer}>
        <ProgressBar progress={xpProgress} color={colors.violet} height={3} />
      </View>
    </View>
  );
}

/* -- Sparkline (mini belief trace chart) ----------------------------------- */

const SPARKLINE_COLORS: Record<string, string> = {
  consonance: colors.consonance,
  tempo: colors.tempo,
  salience: colors.salience,
  familiarity: colors.familiarity,
  reward: colors.reward,
};

function Sparkline({
  data,
  belief,
  label,
}: {
  data: number[];
  belief: string;
  label: string;
}) {
  const color = SPARKLINE_COLORS[belief] ?? colors.violet;

  // Normalize data to sparkline height
  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;

  const points = data
    .map((v, i) => {
      const x = (i / (data.length - 1)) * SPARKLINE_WIDTH;
      const y = SPARKLINE_HEIGHT - ((v - min) / range) * (SPARKLINE_HEIGHT - 4) - 2;
      return `${x},${y}`;
    })
    .join(" ");

  return (
    <View style={styles.sparklineContainer}>
      <Text style={[styles.sparklineLabel, { color }]}>{label}</Text>
      <Svg width={SPARKLINE_WIDTH} height={SPARKLINE_HEIGHT}>
        <Polyline
          points={points}
          fill="none"
          stroke={color}
          strokeWidth={1.5}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </Svg>
    </View>
  );
}

/* -- Brain Monologue (typewriter effect) ----------------------------------- */

function BrainMonologue({ text }: { text: string }) {
  const [displayedText, setDisplayedText] = useState("");

  useEffect(() => {
    setDisplayedText("");
    let idx = 0;
    const timer = setInterval(() => {
      idx++;
      if (idx <= text.length) {
        setDisplayedText(text.slice(0, idx));
      } else {
        clearInterval(timer);
      }
    }, 25);
    return () => clearInterval(timer);
  }, [text]);

  return (
    <View style={styles.monologueContainer}>
      <Ionicons
        name="chatbubble-ellipses"
        size={14}
        color={colors.violet}
        style={styles.monologueIcon}
      />
      <Text style={styles.monologueText}>{displayedText}</Text>
    </View>
  );
}

/* -- DashboardScreen -------------------------------------------------------- */

export function DashboardScreen() {
  const mind = useM3Store((s) => s.mind);
  const milestones = useM3Store((s) => s.milestones);
  const streak = useUserStore((s) => s.streak);
  const tracksAnalyzed = useUserStore((s) => s.tracksAnalyzed);
  const xp = useUserStore((s) => s.xp);
  const level = useUserStore((s) => s.level);

  /* Persona + level name */
  const persona = mind ? getPersona(mind.activePersonaId) : null;
  const familyColor = persona ? familyColors[persona.family] ?? colors.violet : colors.violet;
  const levelName = persona && mind ? getLevelName(persona.family, mind.level) : null;

  /* XP progress for the current level */
  const xpForCurrentLevel = level * 200;
  const xpProgress = xpForCurrentLevel > 0 ? Math.min(1, (xp % xpForCurrentLevel) / xpForCurrentLevel) : 0;

  /* Generate mock traces for belief sparklines */
  const traces: BeliefTrace[] = useMemo(() => {
    const style = persona
      ? persona.family === "Alchemists"
        ? "dramatic"
        : persona.family === "Explorers"
        ? "chaotic"
        : persona.family === "Anchors"
        ? "calm"
        : "balanced"
      : "balanced";
    return generateTrace(300, style as any, 50);
  }, [persona]);

  // Extract belief streams from traces
  const beliefStreams = useMemo(() => {
    if (traces.length === 0) return {};
    return {
      consonance: traces.map((t) => t.consonance),
      tempo: traces.map((t) => t.tempo),
      salience: traces.map((t) => t.salience),
      familiarity: traces.map((t) => t.familiarity),
      reward: traces.map((t) => t.reward),
    };
  }, [traces]);

  /* Brain monologue text */
  const monologueText = useMemo(() => {
    if (!mind || !persona) return "";
    const dominant = getDominantType(mind.genes);
    const listens = mind.totalListens;

    if (listens < 10) {
      return `The first neural pathways are forming. Your ${dominant} tendencies are becoming visible, but there is much to learn. Keep listening.`;
    }
    if (listens < 50) {
      return `Patterns are emerging. Your ${persona.name} mind is developing preferences in the ${dominant} direction. The belief network is beginning to stabilize.`;
    }
    if (listens < 200) {
      return `After ${listens} listening sessions, your mind has developed distinct preferences. The ${dominant} pathways are well-established. Prediction accuracy is improving.`;
    }
    return `A mature ${persona.name} mind. ${listens} sessions have refined your neural parameters across all 5 genes. Your mind now predicts musical events with notable accuracy.`;
  }, [mind, persona]);

  /* -- Render Guard -------------------------------------------------------- */

  if (!mind || !persona) {
    return (
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.emptyState}>
          <Ionicons name="analytics" size={48} color={colors.textTertiary} />
          <Text style={styles.emptyTitle}>No Data Yet</Text>
          <Text style={styles.emptySubtitle}>
            Birth your Musical Mind to see your dashboard.
          </Text>
        </View>
      </SafeAreaView>
    );
  }

  /* -- Main Render --------------------------------------------------------- */

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* ── 1. HUD Stats Bar ── */}
        <Animated.View entering={FadeInDown.delay(50).duration(400)}>
          <HUDStatsBar
            streak={streak}
            tracks={mind.totalListens || tracksAnalyzed}
            level={mind.level}
            xpProgress={xpProgress}
          />
        </Animated.View>

        {/* ── 2. Persona Identity Card ── */}
        <Animated.View entering={FadeInDown.delay(100).duration(500)}>
          <GlassCard style={styles.identityCard}>
            <View style={styles.identityRow}>
              {/* Avatar circle */}
              <View style={[styles.avatarCircle, { borderColor: familyColor }]}>
                <Text style={[styles.avatarInitial, { color: familyColor }]}>
                  {persona.name.charAt(0)}
                </Text>
              </View>

              <View style={styles.identityInfo}>
                <Text style={styles.personaName}>{persona.name}</Text>
                <Badge label={persona.family} color={familyColor} />
              </View>
            </View>

            {/* Evolution progress */}
            {levelName && (
              <View style={styles.evolutionRow}>
                <Text style={styles.stageName}>
                  {levelName.name}
                </Text>
                <Text style={styles.stageProgress}>
                  {Math.round(mind.stageProgress * 100)}%
                </Text>
              </View>
            )}
            <ProgressBar
              progress={mind.stageProgress}
              color={familyColor}
              height={3}
            />

            {/* Stage label */}
            <Text style={styles.stageLabel}>
              Stage: {mind.stage} -- Level {mind.level}/12
            </Text>
          </GlassCard>
        </Animated.View>

        {/* ── 3. Mind Radar ── */}
        <Animated.View entering={FadeInDown.delay(200).duration(500)}>
          <GlassCard style={styles.radarCard}>
            <Text style={styles.sectionTitle}>Mind Radar</Text>
            <View style={styles.radarCenter}>
              <MindRadar genes={mind.genes} size={200} />
            </View>
          </GlassCard>
        </Animated.View>

        {/* ── 4. Gene Distribution (MindTypeRing) ── */}
        <Animated.View entering={FadeInDown.delay(300).duration(500)}>
          <GlassCard style={styles.ringCard}>
            <Text style={styles.sectionTitle}>Gene Distribution</Text>
            <View style={styles.ringCenter}>
              <MindTypeRing genes={mind.genes} size={160} />
            </View>
          </GlassCard>
        </Animated.View>

        {/* ── 5. Weekly Listening ── */}
        <Animated.View entering={FadeInDown.delay(400).duration(500)}>
          <GlassCard style={styles.weeklyCard}>
            <Text style={styles.sectionTitle}>Weekly Listening</Text>
            <WeeklyChart />
            <View style={styles.weeklyFooter}>
              <Text style={styles.weeklyFooterText}>
                {weeklyStats.totalMinutes} min -- {weeklyStats.totalTracks} tracks
              </Text>
            </View>
          </GlassCard>
        </Animated.View>

        {/* ── 6. Belief Traces ── */}
        <Animated.View entering={FadeInDown.delay(500).duration(500)}>
          <GlassCard style={styles.tracesCard}>
            <Text style={styles.sectionTitle}>Belief Traces</Text>
            <View style={styles.sparklineGrid}>
              {Object.entries(beliefStreams).map(([key, data]) => (
                <Sparkline
                  key={key}
                  data={data as number[]}
                  belief={key}
                  label={key.charAt(0).toUpperCase() + key.slice(1)}
                />
              ))}
            </View>
          </GlassCard>
        </Animated.View>

        {/* ── 7. Active Functions ── */}
        <Animated.View entering={FadeInDown.delay(600).duration(500)}>
          <GlassCard style={styles.functionsCard}>
            <Text style={styles.sectionTitle}>
              Active Functions ({mind.activeFunctions.length}/9)
            </Text>
            <FunctionsGrid activeFunctions={mind.activeFunctions} />
          </GlassCard>
        </Animated.View>

        {/* ── 8. Brain Monologue ── */}
        <Animated.View entering={FadeInDown.delay(700).duration(500)}>
          <GlassCard style={styles.monologueCard}>
            <Text style={styles.sectionTitle}>Mind Speaks</Text>
            <BrainMonologue text={monologueText} />
          </GlassCard>
        </Animated.View>

        {/* Bottom spacer */}
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
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.md,
  },

  /* Empty state */
  emptyState: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
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

  /* HUD Stats Bar */
  hudBar: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: colors.surface,
    borderRadius: 12,
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.lg,
    marginBottom: spacing.lg,
    gap: spacing.lg,
  },
  hudItem: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
  },
  hudValue: {
    fontSize: 14,
    fontFamily: fonts.monoSemiBold,
    color: colors.textPrimary,
  },
  hudLabel: {
    fontSize: 10,
    fontFamily: fonts.body,
    color: colors.textTertiary,
  },
  hudXpContainer: {
    flex: 1,
  },

  /* Identity Card */
  identityCard: {
    marginBottom: spacing.lg,
  },
  identityRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.lg,
    marginBottom: spacing.md,
  },
  avatarCircle: {
    width: 52,
    height: 52,
    borderRadius: 26,
    borderWidth: 2,
    backgroundColor: colors.surface,
    alignItems: "center",
    justifyContent: "center",
  },
  avatarInitial: {
    fontSize: 22,
    fontFamily: fonts.display,
  },
  identityInfo: {
    flex: 1,
    gap: spacing.xs,
  },
  personaName: {
    fontSize: 20,
    fontFamily: fonts.display,
    color: colors.textPrimary,
    letterSpacing: 0.3,
  },
  evolutionRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: spacing.xs,
  },
  stageName: {
    fontSize: 13,
    fontFamily: fonts.bodySemiBold,
    color: colors.textSecondary,
  },
  stageProgress: {
    fontSize: 12,
    fontFamily: fonts.mono,
    color: colors.textTertiary,
  },
  stageLabel: {
    fontSize: 11,
    fontFamily: fonts.mono,
    color: colors.textTertiary,
    marginTop: spacing.sm,
    textTransform: "capitalize",
  },

  /* Section title */
  sectionTitle: {
    fontSize: 13,
    fontFamily: fonts.heading,
    color: colors.textSecondary,
    textTransform: "uppercase",
    letterSpacing: 1.2,
    marginBottom: spacing.md,
  },

  /* Radar */
  radarCard: {
    marginBottom: spacing.lg,
  },
  radarCenter: {
    alignItems: "center",
  },

  /* Ring */
  ringCard: {
    marginBottom: spacing.lg,
  },
  ringCenter: {
    alignItems: "center",
  },

  /* Weekly */
  weeklyCard: {
    marginBottom: spacing.lg,
  },
  weeklyFooter: {
    marginTop: spacing.sm,
    alignItems: "center",
  },
  weeklyFooterText: {
    fontSize: 11,
    fontFamily: fonts.mono,
    color: colors.textTertiary,
  },

  /* Traces */
  tracesCard: {
    marginBottom: spacing.lg,
  },
  sparklineGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: spacing.lg,
  },
  sparklineContainer: {
    gap: 4,
  },
  sparklineLabel: {
    fontSize: 10,
    fontFamily: fonts.bodySemiBold,
    textTransform: "uppercase",
    letterSpacing: 0.5,
  },

  /* Functions */
  functionsCard: {
    marginBottom: spacing.lg,
  },

  /* Monologue */
  monologueCard: {
    marginBottom: spacing.lg,
  },
  monologueContainer: {
    flexDirection: "row",
    alignItems: "flex-start",
    gap: spacing.sm,
  },
  monologueIcon: {
    marginTop: 2,
  },
  monologueText: {
    flex: 1,
    fontSize: 13,
    fontFamily: fonts.body,
    color: colors.textSecondary,
    lineHeight: 20,
    letterSpacing: 0.1,
  },
});
