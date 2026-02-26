/* -- Live Screen -- Resonance Field (2D mobile) ------------------------------- */

import React, { useEffect, useRef, useMemo } from "react";
import {
  View,
  Text,
  StyleSheet,
  Dimensions,
  TouchableOpacity,
  Platform,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Svg, {
  Circle,
  Line,
  Text as SvgText,
  Defs,
  RadialGradient,
  Stop,
} from "react-native-svg";
import Animated, {
  FadeIn,
  FadeInUp,
  useAnimatedStyle,
  useSharedValue,
  withRepeat,
  withTiming,
  Easing,
} from "react-native-reanimated";
import { useTranslation } from "react-i18next";
import {
  useResonanceStore,
  SELF_TRACKS,
} from "../../stores/useResonanceStore";
import { resonance as computeResonance } from "../../data/resonance-simulation";
import type { Psi5, ResonanceUser } from "../../data/resonance-simulation";
import { personas } from "../../data/personas";
import { GlassCard } from "../../components/ui/GlassCard";
import { colors, familyColors, fonts, spacing } from "../../design/tokens";

const { width: SCREEN_WIDTH } = Dimensions.get("window");
const FIELD_SIZE = SCREEN_WIDTH - 32;
const FIELD_CENTER = FIELD_SIZE / 2;
const FIELD_RADIUS = FIELD_SIZE / 2 - 24;

/* -- Signal toast labels ---------------------------------------------------- */

const SIGNAL_EMOJI: Record<string, string> = {
  wave: "~",
  chills: "*",
  vibe: "+",
  fire: "!",
  mind: "o",
  feel: "<3",
  sync: "=",
  peak: "^",
};

/* -- Map 3D position to 2D field coordinates -------------------------------- */

function projectTo2D(
  pos: [number, number, number],
  center: number,
  radius: number,
): { x: number; y: number } {
  // Use XZ plane, ignore Y. Normalize [-25, 25] -> [0, fieldSize].
  const maxDist = 25;
  const x = center + (pos[0] / maxDist) * radius;
  const y = center + (pos[2] / maxDist) * radius;
  return { x, y };
}

/* -- User dot size from resonance ------------------------------------------- */

function dotRadius(res: number): number {
  return 6 + res * 12; // 6px to 18px
}

/* -- Format time mm:ss ------------------------------------------------------ */

function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

/* ========================================================================== */

export function LiveScreen() {
  const { t } = useTranslation();

  const users = useResonanceStore((s) => s.users);
  const connections = useResonanceStore((s) => s.connections);
  const signals = useResonanceStore((s) => s.signals);
  const selfPsi = useResonanceStore((s) => s.selfPsi);
  const isPlaying = useResonanceStore((s) => s.isPlaying);
  const selfTrackIdx = useResonanceStore((s) => s.selfTrackIdx);
  const selfPlaybackTime = useResonanceStore((s) => s.selfPlaybackTime);
  const selectedUserId = useResonanceStore((s) => s.selectedUserId);
  const initialize = useResonanceStore((s) => s.initialize);
  const cleanup = useResonanceStore((s) => s.cleanup);
  const togglePlay = useResonanceStore((s) => s.togglePlay);
  const skipTrack = useResonanceStore((s) => s.skipTrack);
  const selectUser = useResonanceStore((s) => s.selectUser);

  const tickRef = useRef<ReturnType<typeof setInterval> | null>(null);

  /* -- Self pulse animation ------------------------------------------------- */
  const pulseScale = useSharedValue(1);
  useEffect(() => {
    pulseScale.value = withRepeat(
      withTiming(1.25, { duration: 1200, easing: Easing.inOut(Easing.ease) }),
      -1,
      true,
    );
  }, []);

  const pulseStyle = useAnimatedStyle(() => ({
    transform: [{ scale: pulseScale.value }],
  }));

  /* -- Initialize / Tick / Cleanup ------------------------------------------ */

  useEffect(() => {
    initialize();
    tickRef.current = setInterval(() => {
      useResonanceStore.getState().tick(0.016);
    }, 16);
    return () => {
      if (tickRef.current) clearInterval(tickRef.current);
      cleanup();
    };
  }, []);

  /* -- Current track -------------------------------------------------------- */

  const currentTrack = SELF_TRACKS[selfTrackIdx];
  const trackProgress = currentTrack
    ? selfPlaybackTime / currentTrack.duration
    : 0;

  /* -- Self-connection count ------------------------------------------------ */

  const selfConnections = useMemo(
    () => connections.filter((c) => c.userA === "self" || c.userB === "self"),
    [connections],
  );

  /* -- Incoming signals to self --------------------------------------------- */

  const incomingSignals = useMemo(
    () => signals.filter((s) => s.to === "self"),
    [signals],
  );

  /* -- Compute resonance values per user for sizing/opacity ----------------- */

  const userResonances = useMemo(() => {
    const map: Record<string, number> = {};
    for (const u of users) {
      map[u.id] = computeResonance(selfPsi, u.psi);
    }
    return map;
  }, [users, selfPsi]);

  /* -- Get user family color ------------------------------------------------ */

  function getUserColor(u: ResonanceUser): string {
    const p = personas.find((p) => p.id === u.personaId);
    return p ? (familyColors[p.family] ?? colors.violet) : colors.violet;
  }

  /* -- Build connection lines between users & self in 2D -------------------- */

  function getConnectionEndpoints(conn: {
    userA: string;
    userB: string;
  }): { x1: number; y1: number; x2: number; y2: number } | null {
    const getPos = (id: string): { x: number; y: number } | null => {
      if (id === "self") return { x: FIELD_CENTER, y: FIELD_CENTER };
      const u = users.find((u) => u.id === id);
      if (!u) return null;
      return projectTo2D(u.position, FIELD_CENTER, FIELD_RADIUS);
    };
    const a = getPos(conn.userA);
    const b = getPos(conn.userB);
    if (!a || !b) return null;
    return { x1: a.x, y1: a.y, x2: b.x, y2: b.y };
  }

  /* -- Render --------------------------------------------------------------- */

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <Animated.View entering={FadeIn.duration(600)} style={styles.header}>
        <Text style={styles.title}>Resonance Field</Text>
        <Text style={styles.subtitle}>
          {users.length} minds nearby
        </Text>
      </Animated.View>

      {/* SVG Resonance Field */}
      <Animated.View
        entering={FadeInUp.duration(800).delay(200)}
        style={styles.fieldContainer}
      >
        <Svg
          width={FIELD_SIZE}
          height={FIELD_SIZE}
          viewBox={`0 0 ${FIELD_SIZE} ${FIELD_SIZE}`}
        >
          <Defs>
            <RadialGradient id="selfGlow" cx="50%" cy="50%" r="50%">
              <Stop offset="0%" stopColor={colors.violet} stopOpacity={0.4} />
              <Stop offset="100%" stopColor={colors.violet} stopOpacity={0} />
            </RadialGradient>
            <RadialGradient id="fieldBg" cx="50%" cy="50%" r="50%">
              <Stop
                offset="0%"
                stopColor="rgba(139,92,246,0.06)"
                stopOpacity={1}
              />
              <Stop
                offset="70%"
                stopColor="rgba(139,92,246,0.02)"
                stopOpacity={1}
              />
              <Stop
                offset="100%"
                stopColor="rgba(0,0,0,0)"
                stopOpacity={1}
              />
            </RadialGradient>
          </Defs>

          {/* Background glow */}
          <Circle
            cx={FIELD_CENTER}
            cy={FIELD_CENTER}
            r={FIELD_RADIUS}
            fill="url(#fieldBg)"
          />

          {/* Range rings */}
          {[0.33, 0.66, 1].map((r, i) => (
            <Circle
              key={i}
              cx={FIELD_CENTER}
              cy={FIELD_CENTER}
              r={FIELD_RADIUS * r}
              fill="none"
              stroke="rgba(255,255,255,0.04)"
              strokeWidth={0.5}
            />
          ))}

          {/* Connection lines */}
          {selfConnections.map((conn) => {
            const pts = getConnectionEndpoints(conn);
            if (!pts) return null;
            return (
              <Line
                key={conn.id}
                x1={pts.x1}
                y1={pts.y1}
                x2={pts.x2}
                y2={pts.y2}
                stroke={colors.violet}
                strokeWidth={1 + conn.strength * 2}
                strokeOpacity={0.15 + conn.strength * 0.4}
                strokeDasharray={conn.strength > 0.6 ? undefined : "4,4"}
              />
            );
          })}

          {/* User-to-user connections (non-self, fainter) */}
          {connections
            .filter((c) => c.userA !== "self" && c.userB !== "self")
            .slice(0, 10)
            .map((conn) => {
              const pts = getConnectionEndpoints(conn);
              if (!pts) return null;
              return (
                <Line
                  key={conn.id}
                  x1={pts.x1}
                  y1={pts.y1}
                  x2={pts.x2}
                  y2={pts.y2}
                  stroke="rgba(255,255,255,0.1)"
                  strokeWidth={0.5 + conn.strength}
                  strokeDasharray="3,5"
                />
              );
            })}

          {/* User dots */}
          {users.map((u) => {
            const pos = projectTo2D(u.position, FIELD_CENTER, FIELD_RADIUS);
            const res = userResonances[u.id] ?? 0;
            const r = dotRadius(res);
            const col = getUserColor(u);
            const isSelected = selectedUserId === u.id;

            return (
              <React.Fragment key={u.id}>
                {/* Glow for high resonance */}
                {res > 0.6 && (
                  <Circle
                    cx={pos.x}
                    cy={pos.y}
                    r={r + 8}
                    fill={col}
                    fillOpacity={0.08}
                  />
                )}
                {/* Main dot */}
                <Circle
                  cx={pos.x}
                  cy={pos.y}
                  r={r}
                  fill={col}
                  fillOpacity={0.25 + res * 0.6}
                  stroke={isSelected ? "#FFFFFF" : col}
                  strokeWidth={isSelected ? 2 : 0.5}
                  strokeOpacity={isSelected ? 1 : 0.5}
                  onPress={() => selectUser(isSelected ? null : u.id)}
                />
                {/* Name label */}
                <SvgText
                  x={pos.x}
                  y={pos.y + r + 12}
                  fill="rgba(255,255,255,0.5)"
                  fontSize={9}
                  fontFamily={fonts.body}
                  textAnchor="middle"
                >
                  {u.displayName.split(" ")[0]}
                </SvgText>
              </React.Fragment>
            );
          })}

          {/* Self glow ring */}
          <Circle
            cx={FIELD_CENTER}
            cy={FIELD_CENTER}
            r={28}
            fill="url(#selfGlow)"
          />

          {/* Self dot */}
          <Circle
            cx={FIELD_CENTER}
            cy={FIELD_CENTER}
            r={18}
            fill={colors.violet}
            fillOpacity={0.8}
            stroke={colors.violetLight}
            strokeWidth={2}
          />
          <SvgText
            x={FIELD_CENTER}
            y={FIELD_CENTER + 5}
            fill="#FFFFFF"
            fontSize={12}
            fontWeight="bold"
            fontFamily={fonts.heading}
            textAnchor="middle"
          >
            You
          </SvgText>
        </Svg>

        {/* Pulse overlay on self (Reanimated) */}
        <Animated.View
          style={[
            styles.selfPulse,
            {
              left: FIELD_CENTER + 16 - 20,
              top: FIELD_CENTER - 20,
            },
            pulseStyle,
          ]}
        />
      </Animated.View>

      {/* Selected user info */}
      {selectedUserId && (() => {
        const u = users.find((u) => u.id === selectedUserId);
        if (!u) return null;
        const p = personas.find((p) => p.id === u.personaId);
        const res = userResonances[u.id] ?? 0;
        return (
          <Animated.View entering={FadeIn.duration(300)} style={styles.selectedCard}>
            <GlassCard intensity="high" style={styles.selectedInner}>
              <View style={styles.selectedRow}>
                <View style={{ flex: 1 }}>
                  <Text style={styles.selectedName}>{u.displayName}</Text>
                  <Text style={styles.selectedMeta}>
                    {p?.name ?? "Unknown"} | {u.country}
                  </Text>
                  {u.trackTitle && (
                    <Text style={styles.selectedTrack} numberOfLines={1}>
                      {u.trackArtist} -- {u.trackTitle}
                    </Text>
                  )}
                </View>
                <View style={styles.resonanceBadge}>
                  <Text style={styles.resonanceValue}>
                    {Math.round(res * 100)}%
                  </Text>
                  <Text style={styles.resonanceLabel}>resonance</Text>
                </View>
              </View>
            </GlassCard>
          </Animated.View>
        );
      })()}

      {/* Signal toasts */}
      {incomingSignals.length > 0 && (
        <View style={styles.signalContainer}>
          {incomingSignals.slice(-3).map((sig) => {
            const fromUser = users.find((u) => u.id === sig.from);
            return (
              <Animated.View
                key={sig.id}
                entering={FadeIn.duration(400)}
                style={styles.signalToast}
              >
                <Text style={styles.signalText}>
                  {SIGNAL_EMOJI[sig.type] ?? "~"}{" "}
                  {fromUser?.displayName ?? "Someone"} sent{" "}
                  {sig.type}
                </Text>
              </Animated.View>
            );
          })}
        </View>
      )}

      {/* Bottom panel — Now playing */}
      <Animated.View
        entering={FadeInUp.duration(600).delay(400)}
        style={styles.bottomPanel}
      >
        <GlassCard intensity="high" style={styles.nowPlaying}>
          {/* Track info */}
          <View style={styles.trackRow}>
            <View style={styles.trackInfo}>
              <Text style={styles.trackTitle} numberOfLines={1}>
                {currentTrack?.title ?? "---"}
              </Text>
              <Text style={styles.trackArtist} numberOfLines={1}>
                {currentTrack?.artist ?? "---"}
              </Text>
            </View>

            {/* Controls */}
            <View style={styles.controls}>
              <TouchableOpacity
                onPress={togglePlay}
                style={styles.controlBtn}
                activeOpacity={0.7}
              >
                <Text style={styles.controlIcon}>
                  {isPlaying ? "||" : ">"}
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                onPress={skipTrack}
                style={styles.controlBtn}
                activeOpacity={0.7}
              >
                <Text style={styles.controlIcon}>{">>"}</Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* Progress bar */}
          <View style={styles.progressTrack}>
            <View
              style={[
                styles.progressFill,
                { width: `${Math.min(100, trackProgress * 100)}%` },
              ]}
            />
          </View>

          {/* Time + connection count */}
          <View style={styles.bottomRow}>
            <Text style={styles.timeText}>
              {formatTime(selfPlaybackTime)} /{" "}
              {formatTime(currentTrack?.duration ?? 0)}
            </Text>
            <Text style={styles.connectionText}>
              {selfConnections.length} connection
              {selfConnections.length !== 1 ? "s" : ""}
            </Text>
          </View>
        </GlassCard>
      </Animated.View>
    </SafeAreaView>
  );
}

/* -- Styles ---------------------------------------------------------------- */

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.md,
    paddingBottom: spacing.sm,
  },
  title: {
    fontFamily: fonts.display,
    fontSize: 28,
    color: colors.textPrimary,
  },
  subtitle: {
    fontFamily: fonts.body,
    fontSize: 13,
    color: colors.textSecondary,
    marginTop: 2,
  },

  /* Field */
  fieldContainer: {
    alignSelf: "center",
    width: FIELD_SIZE,
    height: FIELD_SIZE,
    borderRadius: 16,
    overflow: "hidden",
    backgroundColor: "rgba(255,255,255,0.01)",
    borderWidth: StyleSheet.hairlineWidth,
    borderColor: colors.border,
  },
  selfPulse: {
    position: "absolute",
    width: 40,
    height: 40,
    borderRadius: 20,
    borderWidth: 1.5,
    borderColor: colors.violet,
    opacity: 0.3,
  },

  /* Selected user */
  selectedCard: {
    paddingHorizontal: spacing.lg,
    marginTop: spacing.sm,
  },
  selectedInner: {
    paddingVertical: spacing.md,
  },
  selectedRow: {
    flexDirection: "row",
    alignItems: "center",
  },
  selectedName: {
    fontFamily: fonts.heading,
    fontSize: 16,
    color: colors.textPrimary,
  },
  selectedMeta: {
    fontFamily: fonts.body,
    fontSize: 12,
    color: colors.textSecondary,
    marginTop: 2,
  },
  selectedTrack: {
    fontFamily: fonts.mono,
    fontSize: 11,
    color: colors.textTertiary,
    marginTop: 4,
  },
  resonanceBadge: {
    alignItems: "center",
    marginLeft: spacing.lg,
  },
  resonanceValue: {
    fontFamily: fonts.monoSemiBold,
    fontSize: 22,
    color: colors.violet,
  },
  resonanceLabel: {
    fontFamily: fonts.body,
    fontSize: 10,
    color: colors.textTertiary,
  },

  /* Signal toasts */
  signalContainer: {
    position: "absolute",
    top: 120,
    right: spacing.lg,
    gap: 6,
  },
  signalToast: {
    backgroundColor: "rgba(139,92,246,0.2)",
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
    borderWidth: StyleSheet.hairlineWidth,
    borderColor: "rgba(139,92,246,0.3)",
  },
  signalText: {
    fontFamily: fonts.body,
    fontSize: 11,
    color: colors.violetLight,
  },

  /* Bottom panel */
  bottomPanel: {
    position: "absolute",
    bottom: Platform.OS === "ios" ? 100 : 80,
    left: spacing.lg,
    right: spacing.lg,
  },
  nowPlaying: {
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.lg,
  },
  trackRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  trackInfo: {
    flex: 1,
    marginRight: spacing.md,
  },
  trackTitle: {
    fontFamily: fonts.heading,
    fontSize: 15,
    color: colors.textPrimary,
  },
  trackArtist: {
    fontFamily: fonts.body,
    fontSize: 12,
    color: colors.textSecondary,
    marginTop: 2,
  },
  controls: {
    flexDirection: "row",
    gap: spacing.sm,
  },
  controlBtn: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: "rgba(139,92,246,0.2)",
    alignItems: "center",
    justifyContent: "center",
  },
  controlIcon: {
    fontFamily: fonts.monoSemiBold,
    fontSize: 14,
    color: colors.textPrimary,
  },
  progressTrack: {
    height: 3,
    backgroundColor: "rgba(255,255,255,0.06)",
    borderRadius: 1.5,
    marginTop: spacing.md,
    overflow: "hidden",
  },
  progressFill: {
    height: "100%",
    backgroundColor: colors.violet,
    borderRadius: 1.5,
  },
  bottomRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: spacing.sm,
  },
  timeText: {
    fontFamily: fonts.mono,
    fontSize: 11,
    color: colors.textTertiary,
  },
  connectionText: {
    fontFamily: fonts.body,
    fontSize: 11,
    color: colors.textSecondary,
  },
});
