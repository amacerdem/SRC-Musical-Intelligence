import React, { useState, useRef, useCallback, useEffect } from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Alert,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Animated, {
  FadeInDown,
  FadeInUp,
  FadeIn,
  useSharedValue,
  useAnimatedStyle,
  withTiming,
} from "react-native-reanimated";
import { useNavigation } from "@react-navigation/native";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";
import type { OnboardingStackParamList } from "../../navigation/types";
import { useOnboardingStore } from "../../stores/useOnboardingStore";
import { useUserStore } from "../../stores/useUserStore";
import { SpotifyService } from "../../services/spotify";
import { SpotifySimulator } from "../../services/SpotifySimulator";
import { Button } from "../../components/ui/Button";
import { GlassCard } from "../../components/ui/GlassCard";
import { ProgressBar } from "../../components/ui/ProgressBar";
import { colors } from "../../design/tokens";

/* ---------------------------------------------------------------------------
 *  Constants
 * ------------------------------------------------------------------------- */

const PHASES = [
  "Scanning your listening history...",
  "2,847 tracks found across 156 playlists...",
  "Analyzing harmonic patterns...",
  "Mapping spectral preferences...",
  "Detecting rhythmic signatures...",
  "Building your perceptual profile...",
  "Calibrating 97 R\u00B3 dimensions...",
  "Training belief networks...",
  "Forming neural connections...",
  "Your musical mind is ready.",
];

const PLATFORMS = [
  {
    id: "spotify",
    name: "Spotify",
    icon: "S",
    color: "#1DB954",
    subtitle: "Your playlists & history",
  },
  {
    id: "apple",
    name: "Apple Music",
    icon: "\u266B",
    color: "#FC3C44",
    subtitle: "Your library & favorites",
  },
  {
    id: "soundcloud",
    name: "SoundCloud",
    icon: "\u2601",
    color: "#FF5500",
    subtitle: "Your likes & reposts",
  },
] as const;

/** Belief indicators that light up during analysis. */
const BELIEFS = [
  { label: "Consonance", color: "#8B5CF6", threshold: 10 },
  { label: "Tempo", color: "#06B6D4", threshold: 25 },
  { label: "Salience", color: "#F59E0B", threshold: 45 },
  { label: "Familiarity", color: "#10B981", threshold: 65 },
  { label: "Reward", color: "#EC4899", threshold: 85 },
] as const;

/** Genre chips that appear one by one starting at 50%. */
const GENRES = ["Electronic", "Jazz", "Ambient", "World", "Classical"];

const TYPEWRITER_SPEED = 30; // ms per character
const PROGRESS_INTERVAL = 80; // ms per 1% increment

/* ---------------------------------------------------------------------------
 *  Helpers
 * ------------------------------------------------------------------------- */

/** Interpolate from violet to cyan based on progress (0-1). */
function progressColor(t: number): string {
  // violet #8B5CF6 -> cyan #06B6D4
  const r = Math.round(0x8b + (0x06 - 0x8b) * t);
  const g = Math.round(0x5c + (0xb6 - 0x5c) * t);
  const b = Math.round(0xf6 + (0xd4 - 0xf6) * t);
  return `rgb(${r},${g},${b})`;
}

/* ---------------------------------------------------------------------------
 *  Belief Dot (animated glow)
 * ------------------------------------------------------------------------- */

function BeliefDot({
  label,
  color,
  active,
  delay,
}: {
  label: string;
  color: string;
  active: boolean;
  delay: number;
}) {
  const opacity = useSharedValue(0.15);
  const scale = useSharedValue(1);

  useEffect(() => {
    if (active) {
      opacity.value = withTiming(1, { duration: 600 });
      scale.value = withTiming(1.25, { duration: 300 });
      const timer = setTimeout(() => {
        scale.value = withTiming(1, { duration: 300 });
      }, 300);
      return () => clearTimeout(timer);
    }
  }, [active]);

  const dotStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
    transform: [{ scale: scale.value }],
  }));

  const glowStyle = useAnimatedStyle(() => ({
    opacity: withTiming(active ? 0.4 : 0, { duration: 600 }),
  }));

  return (
    <View style={styles.beliefItem}>
      <View style={styles.beliefDotContainer}>
        {/* Glow layer */}
        <Animated.View
          style={[
            styles.beliefGlow,
            { backgroundColor: color },
            glowStyle,
          ]}
        />
        {/* Dot */}
        <Animated.View
          style={[
            styles.beliefDot,
            { backgroundColor: color },
            dotStyle,
          ]}
        />
      </View>
      <Text
        style={[
          styles.beliefLabel,
          active && { color: "rgba(255,255,255,0.8)" },
        ]}
      >
        {label}
      </Text>
    </View>
  );
}

/* ---------------------------------------------------------------------------
 *  Animated Counter (ticks from 0 to target)
 * ------------------------------------------------------------------------- */

function AnimatedCounter({
  target,
  suffix,
  duration = 2000,
}: {
  target: number;
  suffix: string;
  duration?: number;
}) {
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    let start = 0;
    const step = Math.max(1, Math.floor(target / (duration / 16)));
    const timer = setInterval(() => {
      start += step;
      if (start >= target) {
        start = target;
        clearInterval(timer);
      }
      setDisplay(start);
    }, 16);
    return () => clearInterval(timer);
  }, [target, duration]);

  return (
    <Text style={styles.statValue}>
      {display.toLocaleString()}
      <Text style={styles.statSuffix}> {suffix}</Text>
    </Text>
  );
}

/* ---------------------------------------------------------------------------
 *  Main Component
 * ------------------------------------------------------------------------- */

export function ListeningImportScreen() {
  const nav =
    useNavigation<NativeStackNavigationProp<OnboardingStackParamList>>();
  const setProgress = useOnboardingStore((s) => s.setProgress);

  /* -- State ---------------------------------------------------------------- */
  const [selectedPlatform, setSelectedPlatform] = useState<string | null>(null);
  const [progress, setLocalProgress] = useState(0); // 0-100 integer
  const [analyzing, setAnalyzing] = useState(false);
  const [done, setDone] = useState(false);
  const [showContinue, setShowContinue] = useState(false);

  // Typewriter
  const [displayText, setDisplayText] = useState("");
  const [currentPhaseIdx, setCurrentPhaseIdx] = useState(0);

  // Stats reveal
  const [showTracks, setShowTracks] = useState(false);
  const [showHours, setShowHours] = useState(false);
  const [visibleGenres, setVisibleGenres] = useState<string[]>([]);

  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const typewriterRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const phaseQueueRef = useRef<number>(0);

  /* -- Typewriter Effect ---------------------------------------------------- */
  const typewriterText = useRef("");
  const typewriterTarget = useRef("");

  const startTypewriter = useCallback((text: string) => {
    // Clear any existing typewriter
    if (typewriterRef.current) clearInterval(typewriterRef.current);
    typewriterTarget.current = text;
    typewriterText.current = "";
    setDisplayText("");

    let charIdx = 0;
    typewriterRef.current = setInterval(() => {
      charIdx++;
      const partial = text.slice(0, charIdx);
      typewriterText.current = partial;
      setDisplayText(partial);
      if (charIdx >= text.length) {
        if (typewriterRef.current) clearInterval(typewriterRef.current);
      }
    }, TYPEWRITER_SPEED);
  }, []);

  /* -- Progress Animation --------------------------------------------------- */
  const runProgressAnimation = useCallback(
    (realTrackCount?: number, realGenres?: string[]) => {
      setAnalyzing(true);
      setLocalProgress(0);
      phaseQueueRef.current = 0;

      // Start first phase typewriter
      startTypewriter(PHASES[0]);

      let p = 0;
      timerRef.current = setInterval(() => {
        p += 1;

        /* -- Phase transitions -------------------------------------------- */
        const phaseIdx = Math.min(
          PHASES.length - 1,
          Math.floor((p / 100) * PHASES.length)
        );
        if (phaseIdx !== phaseQueueRef.current) {
          phaseQueueRef.current = phaseIdx;
          setCurrentPhaseIdx(phaseIdx);
          startTypewriter(PHASES[phaseIdx]);
        }

        /* -- Stats panel reveals ------------------------------------------ */
        if (p === 15) setShowTracks(true);
        if (p === 30) setShowHours(true);
        if (p >= 50 && p <= 70) {
          const genreChips = realGenres?.length ? realGenres.slice(0, 5) : GENRES;
          const genreIdx = Math.floor(((p - 50) / 20) * genreChips.length);
          setVisibleGenres(genreChips.slice(0, Math.min(genreIdx + 1, genreChips.length)));
        }
        if (p >= 70) {
          const genreChips = realGenres?.length ? realGenres.slice(0, 5) : GENRES;
          setVisibleGenres([...genreChips]);
        }

        /* -- Completion --------------------------------------------------- */
        if (p >= 100) {
          p = 100;
          if (timerRef.current) clearInterval(timerRef.current);
          setDone(true);
          setLocalProgress(100);
          setProgress(100, PHASES[PHASES.length - 1]);

          startTypewriter(PHASES[PHASES.length - 1]);

          setTimeout(() => setShowContinue(true), 500);
        } else {
          setLocalProgress(p);
          setProgress(p, PHASES[phaseQueueRef.current]);
        }
      }, PROGRESS_INTERVAL);
    },
    [setProgress, startTypewriter]
  );

  /* -- Spotify OAuth Flow -------------------------------------------------- */
  const startSpotifyAuth = useCallback(async () => {
    try {
      const request = SpotifyService.getAuthRequest();
      await request.makeAuthUrlAsync(SpotifyService.discovery);

      const result = await request.promptAsync(SpotifyService.discovery);

      if (result.type === "success" && result.params.code) {
        await SpotifyService.exchangeCode(result.params.code, request);
        useUserStore.getState().setSpotifyConnected(true);

        setSelectedPlatform("spotify");

        // Fetch real data in the background while the animation runs
        const tracksPromise = SpotifyService.getInitialBatch();
        runProgressAnimation();

        const tracks = await tracksPromise;
        // Extract unique genres from real tracks
        const uniqueGenres = [...new Set(tracks.map((t) => t.genre).filter((g) => g !== "Unknown"))];
        if (uniqueGenres.length > 0) {
          setVisibleGenres(uniqueGenres.slice(0, 5));
        }
      } else if (result.type === "error") {
        Alert.alert("Spotify Error", result.error?.message ?? "Authentication failed");
      }
      // result.type === "dismiss" → user closed the browser, do nothing
    } catch (err: any) {
      Alert.alert("Connection Error", err.message ?? "Could not connect to Spotify");
    }
  }, [runProgressAnimation]);

  /* -- Start Analysis (entry point) ---------------------------------------- */
  const startAnalysis = useCallback(
    (platformId: string) => {
      if (platformId === "spotify") {
        startSpotifyAuth();
        return;
      }
      // Other platforms: use mock analysis
      setSelectedPlatform(platformId);
      runProgressAnimation();
    },
    [startSpotifyAuth, runProgressAnimation]
  );

  /* -- Cleanup -------------------------------------------------------------- */
  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      if (typewriterRef.current) clearInterval(typewriterRef.current);
    };
  }, []);

  /* -- Computed ------------------------------------------------------------- */
  const progressFraction = progress / 100;
  const barColor = progressColor(progressFraction);

  /* -- Phase 1: Platform Selection ----------------------------------------- */
  if (!analyzing) {
    return (
      <SafeAreaView style={styles.container}>
        <Animated.View entering={FadeInDown.duration(600).delay(100)}>
          <Text style={styles.title}>Connect Your Music</Text>
          <Text style={styles.subtitle}>
            Choose a platform to begin forming your musical mind.
          </Text>
        </Animated.View>

        <View style={styles.platformSection}>
          <View style={styles.platformRow}>
            {PLATFORMS.map((platform, idx) => (
              <Animated.View
                key={platform.id}
                entering={FadeInUp.duration(500).delay(300 + idx * 120)}
                style={styles.platformCardWrapper}
              >
                <TouchableOpacity
                  activeOpacity={0.7}
                  onPress={() => startAnalysis(platform.id)}
                >
                  <GlassCard style={styles.platformCard}>
                    <View
                      style={[
                        styles.platformIcon,
                        { backgroundColor: platform.color },
                      ]}
                    >
                      <Text style={styles.platformIconText}>
                        {platform.icon}
                      </Text>
                    </View>
                    <Text style={styles.platformName}>{platform.name}</Text>
                    <Text style={styles.platformSubtitle}>
                      {platform.subtitle}
                    </Text>
                  </GlassCard>
                </TouchableOpacity>
              </Animated.View>
            ))}
          </View>
        </View>

        <View style={styles.platformFooterSpacer} />
      </SafeAreaView>
    );
  }

  /* -- Phase 2: Analysis / Evolution --------------------------------------- */
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.analysisScroll}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <Animated.View entering={FadeIn.duration(400)}>
          <Text style={styles.analysisTitle}>Evolving</Text>
          <Text style={styles.analysisSubtitle}>
            Forming your musical mind...
          </Text>
        </Animated.View>

        {/* Percentage display */}
        <Animated.View
          entering={FadeIn.duration(500).delay(200)}
          style={styles.percentBlock}
        >
          <Text style={[styles.percentText, { color: barColor }]}>
            {progress}%
          </Text>
        </Animated.View>

        {/* Progress bar */}
        <Animated.View
          entering={FadeIn.duration(500).delay(300)}
          style={styles.progressBarWrap}
        >
          <ProgressBar
            progress={progressFraction}
            color={barColor}
            height={6}
          />
        </Animated.View>

        {/* Typewriter phase text */}
        <Animated.View
          entering={FadeIn.duration(400).delay(400)}
          style={styles.typewriterWrap}
        >
          <Text style={styles.typewriterText}>
            {displayText}
            <Text style={styles.cursor}>|</Text>
          </Text>
        </Animated.View>

        {/* Belief indicators */}
        <Animated.View
          entering={FadeInUp.duration(500).delay(600)}
          style={styles.beliefsRow}
        >
          {BELIEFS.map((b, i) => (
            <BeliefDot
              key={b.label}
              label={b.label}
              color={b.color}
              active={progress >= b.threshold}
              delay={i * 150}
            />
          ))}
        </Animated.View>

        {/* Stats panel */}
        <View style={styles.statsPanel}>
          {showTracks && (
            <Animated.View
              entering={FadeInUp.duration(400)}
              style={styles.statRow}
            >
              <AnimatedCounter
                target={2847}
                suffix="tracks analyzed"
                duration={2500}
              />
            </Animated.View>
          )}

          {showHours && (
            <Animated.View
              entering={FadeInUp.duration(400)}
              style={styles.statRow}
            >
              <AnimatedCounter
                target={3107}
                suffix="hours mapped"
                duration={2500}
              />
            </Animated.View>
          )}

          {visibleGenres.length > 0 && (
            <Animated.View
              entering={FadeIn.duration(300)}
              style={styles.genreRow}
            >
              {visibleGenres.map((genre, idx) => (
                <Animated.View
                  key={genre}
                  entering={FadeIn.duration(300).delay(idx * 80)}
                >
                  <View style={styles.genreChip}>
                    <Text style={styles.genreChipText}>{genre}</Text>
                  </View>
                </Animated.View>
              ))}
            </Animated.View>
          )}
        </View>

        {/* Spacer for scroll */}
        <View style={{ height: 32 }} />
      </ScrollView>

      {/* Continue button */}
      {showContinue && (
        <Animated.View
          entering={FadeInUp.duration(500)}
          style={styles.footer}
        >
          <Button
            title="Continue"
            onPress={() => nav.navigate("NameEntry")}
            size="lg"
          />
        </Animated.View>
      )}
    </SafeAreaView>
  );
}

/* ---------------------------------------------------------------------------
 *  Styles
 * ------------------------------------------------------------------------- */

const styles = StyleSheet.create({
  /* Layout */
  container: {
    flex: 1,
    backgroundColor: colors.background,
    paddingHorizontal: 16,
  },
  analysisScroll: {
    paddingBottom: 16,
  },

  /* Phase 1: Platform Selection */
  title: {
    fontSize: 28,
    fontFamily: "Saira_700Bold",
    color: colors.textPrimary,
    marginTop: 24,
  },
  subtitle: {
    fontSize: 14,
    fontFamily: "Inter_400Regular",
    color: colors.textSecondary,
    marginTop: 8,
    lineHeight: 20,
  },
  platformSection: {
    flex: 1,
    justifyContent: "center",
  },
  platformRow: {
    flexDirection: "row",
    gap: 10,
  },
  platformCardWrapper: {
    flex: 1,
  },
  platformCard: {
    alignItems: "center",
    paddingVertical: 16,
    paddingHorizontal: 6,
    minHeight: 80,
  },
  platformIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 8,
  },
  platformIconText: {
    fontSize: 18,
    fontFamily: "Saira_700Bold",
    color: "#FFFFFF",
  },
  platformName: {
    fontSize: 13,
    fontFamily: "Saira_600SemiBold",
    color: colors.textPrimary,
    textAlign: "center",
  },
  platformSubtitle: {
    fontSize: 10,
    fontFamily: "Inter_400Regular",
    color: colors.textTertiary,
    textAlign: "center",
    marginTop: 4,
  },
  platformFooterSpacer: {
    height: 32,
  },

  /* Phase 2: Analysis */
  analysisTitle: {
    fontSize: 32,
    fontFamily: "Saira_700Bold",
    color: colors.textPrimary,
    marginTop: 24,
    textAlign: "center",
    letterSpacing: 1,
  },
  analysisSubtitle: {
    fontSize: 14,
    fontFamily: "Inter_400Regular",
    color: colors.textSecondary,
    marginTop: 4,
    textAlign: "center",
  },
  percentBlock: {
    marginTop: 32,
    alignItems: "center",
  },
  percentText: {
    fontSize: 48,
    fontFamily: "JetBrainsMono_500Medium",
    textAlign: "center",
    letterSpacing: -2,
  },
  progressBarWrap: {
    marginTop: 16,
    paddingHorizontal: 8,
  },
  typewriterWrap: {
    marginTop: 20,
    minHeight: 24,
    alignItems: "center",
    paddingHorizontal: 16,
  },
  typewriterText: {
    fontSize: 13,
    fontFamily: "JetBrainsMono_400Regular",
    color: "rgba(255,255,255,0.6)",
    textAlign: "center",
    lineHeight: 20,
  },
  cursor: {
    color: "rgba(255,255,255,0.3)",
    fontFamily: "JetBrainsMono_400Regular",
  },

  /* Belief dots */
  beliefsRow: {
    flexDirection: "row",
    justifyContent: "center",
    gap: 20,
    marginTop: 32,
    paddingHorizontal: 8,
  },
  beliefItem: {
    alignItems: "center",
    gap: 6,
  },
  beliefDotContainer: {
    width: 24,
    height: 24,
    alignItems: "center",
    justifyContent: "center",
  },
  beliefDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    position: "absolute",
  },
  beliefGlow: {
    width: 24,
    height: 24,
    borderRadius: 12,
    position: "absolute",
  },
  beliefLabel: {
    fontSize: 9,
    fontFamily: "Inter_500Medium",
    color: "rgba(255,255,255,0.3)",
    textTransform: "uppercase",
    letterSpacing: 0.5,
  },

  /* Stats panel */
  statsPanel: {
    marginTop: 28,
    gap: 12,
    paddingHorizontal: 8,
  },
  statRow: {
    alignItems: "center",
  },
  statValue: {
    fontSize: 18,
    fontFamily: "JetBrainsMono_500Medium",
    color: colors.textPrimary,
  },
  statSuffix: {
    fontSize: 13,
    fontFamily: "Inter_500Medium",
    color: colors.textSecondary,
  },
  genreRow: {
    flexDirection: "row",
    justifyContent: "center",
    flexWrap: "wrap",
    gap: 8,
    marginTop: 4,
  },
  genreChip: {
    paddingHorizontal: 12,
    paddingVertical: 5,
    borderRadius: 20,
    backgroundColor: "rgba(255,255,255,0.06)",
    borderWidth: StyleSheet.hairlineWidth,
    borderColor: "rgba(255,255,255,0.12)",
  },
  genreChipText: {
    fontSize: 11,
    fontFamily: "Inter_600SemiBold",
    color: "rgba(255,255,255,0.7)",
    letterSpacing: 0.3,
  },

  /* Footer */
  footer: {
    paddingVertical: 16,
    paddingHorizontal: 8,
  },
});
