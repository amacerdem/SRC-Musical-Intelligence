/* -- M3HubScreen -- The Core Growth Interface ---------------------------------
 *  Two modes: "idle" (vertical scroll — persona, genes, learn button,
 *  milestones) and "playing" (now playing, visualizer, playlist).
 *
 *  IDLE mode:
 *    - Persona name + family badge + level indicator
 *    - 5 GeneStrands bars
 *    - Pulsating "Learn" button (or upgrade overlay if frozen)
 *    - Recent milestones (last 3)
 *
 *  PLAYING mode:
 *    - Now playing track info
 *    - MindVisualizer
 *    - Playlist with playback controls
 *    - Sticky NowPlayingBar
 *  -------------------------------------------------------------------------- */

import React, { useCallback, useState, useEffect } from "react";
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
  ActivityIndicator,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Animated, {
  FadeIn,
  FadeInDown,
  useAnimatedStyle,
  useSharedValue,
  withRepeat,
  withTiming,
  withSequence,
  Easing,
} from "react-native-reanimated";
import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import { useM3Store } from "../../stores/useM3Store";
import { useM3AudioStore } from "../../stores/useM3AudioStore";
import { useUserStore } from "../../stores/useUserStore";
import { useOnboardingStore } from "../../stores/useOnboardingStore";
import { useM3Gate } from "../../hooks/useM3Gate";
import { usePlaylistGenerator, generateWeeklyPlaylist } from "../../hooks/usePlaylistGenerator";
import { SpotifySimulator, trackToM3Signal } from "../../services/SpotifySimulator";
import { LIBRARY_TRACKS } from "../../data/track-library";
import { getPersona } from "../../data/personas";
import { getLevelName } from "../../data/persona-levels";
import { GlassCard } from "../../components/ui/GlassCard";
import { Badge } from "../../components/ui/Badge";
import { ProgressBar } from "../../components/ui/ProgressBar";
import { GeneStrands } from "../../components/m3/GeneStrands";
import { MindVisualizer } from "../../components/m3/MindVisualizer";
import { PlaylistView } from "../../components/m3/PlaylistView";
import { NowPlayingBar } from "../../components/m3/NowPlayingBar";
import { colors, fonts, spacing, familyColors } from "../../design/tokens";
import type { M3Milestone } from "../../types/m3";

const { width: SCREEN_WIDTH } = Dimensions.get("window");

/* -- LearnButton -- Pulsating circular button -------------------------------- */

function LearnButton({ onPress, isLoading }: { onPress: () => void; isLoading: boolean }) {
  const scale = useSharedValue(1);

  useEffect(() => {
    scale.value = withRepeat(
      withSequence(
        withTiming(1.06, { duration: 1200, easing: Easing.inOut(Easing.sin) }),
        withTiming(1.0, { duration: 1200, easing: Easing.inOut(Easing.sin) }),
      ),
      -1,
      true,
    );
  }, []);

  const pulseStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  return (
    <Animated.View style={[styles.learnButtonOuter, pulseStyle]}>
      <TouchableOpacity
        onPress={onPress}
        disabled={isLoading}
        activeOpacity={0.8}
      >
        <LinearGradient
          colors={[colors.violet, "#A78BFA", "#F472B6"]}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
          style={styles.learnButton}
        >
          {isLoading ? (
            <ActivityIndicator color={colors.textPrimary} size="small" />
          ) : (
            <>
              <Ionicons name="flash" size={28} color={colors.textPrimary} />
              <Text style={styles.learnButtonText}>Learn</Text>
            </>
          )}
        </LinearGradient>
      </TouchableOpacity>
    </Animated.View>
  );
}

/* -- FrozenOverlay -- Shown for free tier ------------------------------------ */

function FrozenOverlay() {
  return (
    <View style={styles.frozenContainer}>
      <Ionicons name="lock-closed" size={32} color={colors.textTertiary} />
      <Text style={styles.frozenTitle}>Mind Frozen</Text>
      <Text style={styles.frozenSubtitle}>
        Upgrade your plan to unlock learning and grow your Musical Mind.
      </Text>
    </View>
  );
}

/* -- MilestoneRow ------------------------------------------------------------ */

function MilestoneRow({ milestone }: { milestone: M3Milestone }) {
  const iconMap: Record<string, string> = {
    birth: "sparkles",
    level_up: "arrow-up-circle",
    stage_up: "rocket",
    persona_shift: "shuffle",
    function_unlock: "flash",
    type_change: "git-compare",
    insight: "bulb",
  };

  return (
    <View style={styles.milestoneRow}>
      <Ionicons
        name={(iconMap[milestone.type] ?? "ellipse") as any}
        size={16}
        color={colors.violet}
      />
      <View style={styles.milestoneInfo}>
        <Text style={styles.milestoneText}>{milestone.detail}</Text>
        <Text style={styles.milestoneTime}>
          {new Date(milestone.timestamp).toLocaleDateString()}
        </Text>
      </View>
    </View>
  );
}

/* -- M3HubScreen ------------------------------------------------------------- */

export function M3HubScreen() {
  const mind = useM3Store((s) => s.mind);
  const milestones = useM3Store((s) => s.milestones);
  const learnFromListening = useM3Store((s) => s.learnFromListening);
  const { isFrozen, canGrow, isAlive } = useM3Gate();

  const mode = useM3AudioStore((s) => s.mode);
  const setPlaylist = useM3AudioStore((s) => s.setPlaylist);
  const setMode = useM3AudioStore((s) => s.setMode);
  const setIsPlaying = useM3AudioStore((s) => s.setIsPlaying);
  const setDuration = useM3AudioStore((s) => s.setDuration);
  const stopPlayback = useM3AudioStore((s) => s.stopPlayback);

  const [isLearning, setIsLearning] = useState(false);

  // Current persona info
  const persona = mind ? getPersona(mind.activePersonaId) : null;
  const familyColor = persona ? familyColors[persona.family] ?? colors.violet : colors.violet;
  const levelName = persona && mind
    ? getLevelName(persona.family, mind.level)
    : null;

  // Recent milestones (last 3)
  const recentMilestones = milestones.slice(-3).reverse();

  /* -- Learn Flow ---------------------------------------------------------- */

  const handleLearn = useCallback(async () => {
    if (!mind || isFrozen) return;
    setIsLearning(true);

    try {
      // 1. Simulate getting a listening session
      const session = SpotifySimulator.getListeningSession();

      // 2. Feed each track to M3 for learning
      for (const entry of session) {
        const signal = trackToM3Signal(entry.track, {
          wasSkipped: entry.wasSkipped,
        });
        learnFromListening(signal);
      }

      // 3. Generate personalized playlist based on updated genes
      const updatedMind = useM3Store.getState().mind;
      if (updatedMind) {
        const playlist = generateWeeklyPlaylist(
          LIBRARY_TRACKS,
          updatedMind.genes,
          12,
        );
        setPlaylist(playlist);

        if (playlist.length > 0) {
          setDuration(playlist[0].durationSec);
        }
      }

      // 4. Switch to playing mode
      setMode("playing");
      setIsPlaying(true);
    } catch (err) {
      console.warn("[M3Hub] Learn error:", err);
    } finally {
      setIsLearning(false);
    }
  }, [mind, isFrozen, learnFromListening, setPlaylist, setMode, setIsPlaying, setDuration]);

  /* -- Stop Playing -------------------------------------------------------- */

  const handleStopPlaying = useCallback(() => {
    stopPlayback();
  }, [stopPlayback]);

  /* -- Render Guard -------------------------------------------------------- */

  if (!mind || !persona) {
    return (
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.emptyState}>
          <Ionicons name="planet" size={48} color={colors.textTertiary} />
          <Text style={styles.emptyTitle}>No Mind Yet</Text>
          <Text style={styles.emptySubtitle}>
            Complete onboarding to birth your Musical Mind.
          </Text>
        </View>
      </SafeAreaView>
    );
  }

  /* -- PLAYING MODE -------------------------------------------------------- */

  if (mode === "playing") {
    const currentTrack = useM3AudioStore.getState().playlist[
      useM3AudioStore.getState().currentTrackIdx
    ];

    return (
      <SafeAreaView style={styles.safeArea} edges={["top"]}>
        <View style={styles.playingContainer}>
          {/* Header with back button */}
          <Animated.View
            entering={FadeIn.duration(300)}
            style={styles.playingHeader}
          >
            <TouchableOpacity
              onPress={handleStopPlaying}
              style={styles.backButton}
              activeOpacity={0.7}
            >
              <Ionicons name="chevron-down" size={24} color={colors.textPrimary} />
            </TouchableOpacity>

            <View style={styles.playingHeaderInfo}>
              <Text style={styles.playingHeaderTitle}>Now Playing</Text>
              <Text style={styles.playingHeaderSubtitle}>
                {persona.name} -- L{mind.level}
              </Text>
            </View>

            <View style={{ width: 40 }} />
          </Animated.View>

          {/* Now playing track info */}
          {currentTrack && (
            <Animated.View
              entering={FadeInDown.delay(100).duration(400)}
              style={styles.nowPlayingInfo}
            >
              <Text style={styles.nowPlayingTitle} numberOfLines={1}>
                {currentTrack.name}
              </Text>
              <Text style={styles.nowPlayingArtist} numberOfLines={1}>
                {currentTrack.artist}
              </Text>
            </Animated.View>
          )}

          {/* Visualizer */}
          <Animated.View entering={FadeInDown.delay(200).duration(500)}>
            <MindVisualizer />
          </Animated.View>

          {/* Playlist */}
          <Animated.View
            entering={FadeInDown.delay(300).duration(500)}
            style={styles.playlistSection}
          >
            <PlaylistView />
          </Animated.View>

          {/* Bottom bar */}
          <NowPlayingBar />
        </View>
      </SafeAreaView>
    );
  }

  /* -- IDLE MODE ----------------------------------------------------------- */

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* ── Top Section: Persona Identity ── */}
        <Animated.View
          entering={FadeInDown.delay(100).duration(500)}
          style={styles.identitySection}
        >
          <View style={styles.identityRow}>
            {/* Persona avatar circle */}
            <View style={[styles.avatarCircle, { borderColor: familyColor }]}>
              <Text style={[styles.avatarInitial, { color: familyColor }]}>
                {persona.name.charAt(0)}
              </Text>
            </View>

            <View style={styles.identityInfo}>
              <Text style={styles.personaName}>{persona.name}</Text>
              <View style={styles.badgeRow}>
                <Badge label={persona.family} color={familyColor} />
                <View style={[styles.levelBadge, { backgroundColor: `${familyColor}20` }]}>
                  <Text style={[styles.levelText, { color: familyColor }]}>
                    L{mind.level}
                  </Text>
                </View>
              </View>
            </View>
          </View>

          {/* Stage name + progress */}
          {levelName && (
            <View style={styles.stageRow}>
              <Text style={styles.stageName}>{levelName.name}</Text>
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
        </Animated.View>

        {/* ── Gene Strands ── */}
        <Animated.View entering={FadeInDown.delay(200).duration(500)}>
          <GlassCard style={styles.genesCard}>
            <Text style={styles.sectionTitle}>Mind Genes</Text>
            <GeneStrands genes={mind.genes} />
          </GlassCard>
        </Animated.View>

        {/* ── Learn Button or Frozen Overlay ── */}
        <Animated.View
          entering={FadeInDown.delay(300).duration(500)}
          style={styles.learnSection}
        >
          {isFrozen ? (
            <FrozenOverlay />
          ) : (
            <LearnButton onPress={handleLearn} isLoading={isLearning} />
          )}
        </Animated.View>

        {/* ── Stats Row ── */}
        <Animated.View entering={FadeInDown.delay(350).duration(500)}>
          <View style={styles.statsRow}>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{mind.totalListens}</Text>
              <Text style={styles.statLabel}>Listens</Text>
            </View>
            <View style={styles.statDivider} />
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{mind.totalMinutes}</Text>
              <Text style={styles.statLabel}>Minutes</Text>
            </View>
            <View style={styles.statDivider} />
            <View style={styles.statItem}>
              <Text style={styles.statValue}>
                {mind.activeFunctions.length}/9
              </Text>
              <Text style={styles.statLabel}>Functions</Text>
            </View>
          </View>
        </Animated.View>

        {/* ── Recent Milestones ── */}
        {recentMilestones.length > 0 && (
          <Animated.View entering={FadeInDown.delay(400).duration(500)}>
            <GlassCard style={styles.milestonesCard}>
              <Text style={styles.sectionTitle}>Recent Observations</Text>
              {recentMilestones.map((ms, i) => (
                <MilestoneRow key={`${ms.timestamp}-${i}`} milestone={ms} />
              ))}
            </GlassCard>
          </Animated.View>
        )}

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
    paddingTop: spacing.lg,
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

  /* Identity section */
  identitySection: {
    marginBottom: spacing.xl,
  },
  identityRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.lg,
    marginBottom: spacing.md,
  },
  avatarCircle: {
    width: 56,
    height: 56,
    borderRadius: 28,
    borderWidth: 2,
    backgroundColor: colors.surface,
    alignItems: "center",
    justifyContent: "center",
  },
  avatarInitial: {
    fontSize: 24,
    fontFamily: fonts.display,
  },
  identityInfo: {
    flex: 1,
    gap: spacing.xs,
  },
  personaName: {
    fontSize: 22,
    fontFamily: fonts.display,
    color: colors.textPrimary,
    letterSpacing: 0.5,
  },
  badgeRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
  },
  levelBadge: {
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
  },
  levelText: {
    fontSize: 11,
    fontFamily: fonts.monoSemiBold,
    letterSpacing: 0.5,
  },
  stageRow: {
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

  /* Genes */
  genesCard: {
    marginBottom: spacing.xl,
  },
  sectionTitle: {
    fontSize: 13,
    fontFamily: fonts.heading,
    color: colors.textSecondary,
    textTransform: "uppercase",
    letterSpacing: 1.2,
    marginBottom: spacing.md,
  },

  /* Learn button */
  learnSection: {
    alignItems: "center",
    marginBottom: spacing.xl,
  },
  learnButtonOuter: {
    // Animated wrapper for pulse
  },
  learnButton: {
    width: 120,
    height: 120,
    borderRadius: 60,
    alignItems: "center",
    justifyContent: "center",
    gap: spacing.xs,
  },
  learnButtonText: {
    fontSize: 15,
    fontFamily: fonts.heading,
    color: colors.textPrimary,
    letterSpacing: 1,
  },

  /* Frozen overlay */
  frozenContainer: {
    alignItems: "center",
    gap: spacing.sm,
    paddingVertical: spacing.xl,
  },
  frozenTitle: {
    fontSize: 18,
    fontFamily: fonts.heading,
    color: colors.textTertiary,
  },
  frozenSubtitle: {
    fontSize: 13,
    fontFamily: fonts.body,
    color: colors.textTertiary,
    textAlign: "center",
    paddingHorizontal: spacing.xxl,
    lineHeight: 20,
  },

  /* Stats row */
  statsRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-around",
    backgroundColor: colors.surface,
    borderRadius: 12,
    paddingVertical: spacing.lg,
    marginBottom: spacing.xl,
  },
  statItem: {
    alignItems: "center",
    gap: 2,
  },
  statValue: {
    fontSize: 18,
    fontFamily: fonts.monoSemiBold,
    color: colors.textPrimary,
  },
  statLabel: {
    fontSize: 11,
    fontFamily: fonts.body,
    color: colors.textTertiary,
    textTransform: "uppercase",
    letterSpacing: 0.5,
  },
  statDivider: {
    width: StyleSheet.hairlineWidth,
    height: 28,
    backgroundColor: colors.border,
  },

  /* Milestones */
  milestonesCard: {
    marginBottom: spacing.lg,
  },
  milestoneRow: {
    flexDirection: "row",
    alignItems: "flex-start",
    gap: spacing.md,
    paddingVertical: spacing.sm,
  },
  milestoneInfo: {
    flex: 1,
  },
  milestoneText: {
    fontSize: 13,
    fontFamily: fonts.body,
    color: colors.textPrimary,
    lineHeight: 18,
  },
  milestoneTime: {
    fontSize: 11,
    fontFamily: fonts.mono,
    color: colors.textTertiary,
    marginTop: 2,
  },

  /* Playing mode */
  playingContainer: {
    flex: 1,
    backgroundColor: colors.background,
  },
  playingHeader: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
  },
  backButton: {
    width: 40,
    height: 40,
    alignItems: "center",
    justifyContent: "center",
  },
  playingHeaderInfo: {
    flex: 1,
    alignItems: "center",
  },
  playingHeaderTitle: {
    fontSize: 13,
    fontFamily: fonts.heading,
    color: colors.textSecondary,
    textTransform: "uppercase",
    letterSpacing: 1,
  },
  playingHeaderSubtitle: {
    fontSize: 11,
    fontFamily: fonts.mono,
    color: colors.textTertiary,
    marginTop: 2,
  },
  nowPlayingInfo: {
    alignItems: "center",
    paddingHorizontal: spacing.xl,
    paddingVertical: spacing.md,
  },
  nowPlayingTitle: {
    fontSize: 20,
    fontFamily: fonts.display,
    color: colors.textPrimary,
    letterSpacing: 0.3,
  },
  nowPlayingArtist: {
    fontSize: 14,
    fontFamily: fonts.body,
    color: colors.textSecondary,
    marginTop: 4,
  },
  playlistSection: {
    flex: 1,
  },
});
