import React, { useState, useRef, useCallback } from "react";
import { View, Text, StyleSheet } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Animated, { FadeInDown, FadeIn } from "react-native-reanimated";
import { useNavigation } from "@react-navigation/native";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";
import type { OnboardingStackParamList } from "../../navigation/types";
import { useOnboardingStore } from "../../stores/useOnboardingStore";
import { Button } from "../../components/ui/Button";
import { GlassCard } from "../../components/ui/GlassCard";
import { ProgressBar } from "../../components/ui/ProgressBar";
import { colors } from "../../design/tokens";

const PHASES = [
  "Scanning library...",
  "Analyzing patterns...",
  "Extracting features...",
  "Building neural profile...",
  "Calibrating beliefs...",
  "Complete!",
];

export function ListeningImportScreen() {
  const nav = useNavigation<NativeStackNavigationProp<OnboardingStackParamList>>();
  const setProgress = useOnboardingStore((s) => s.setProgress);
  const [progress, setLocalProgress] = useState(0);
  const [phase, setPhase] = useState("");
  const [analyzing, setAnalyzing] = useState(false);
  const [done, setDone] = useState(false);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const startAnalysis = useCallback(() => {
    setAnalyzing(true);
    let p = 0;
    timerRef.current = setInterval(() => {
      p += 2;
      if (p >= 100) {
        p = 100;
        if (timerRef.current) clearInterval(timerRef.current);
        setDone(true);
        setPhase(PHASES[5]);
        setLocalProgress(1);
        setProgress(100, PHASES[5]);
      } else {
        const phaseIdx = Math.min(4, Math.floor(p / 20));
        const phaseText = PHASES[phaseIdx];
        setPhase(phaseText);
        setLocalProgress(p / 100);
        setProgress(p, phaseText);
      }
    }, 60);
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      <Animated.View entering={FadeInDown.duration(500)}>
        <Text style={styles.title}>Connect Your Music</Text>
        <Text style={styles.subtitle}>
          Import your listening history to personalize your M³ experience.
        </Text>
      </Animated.View>

      <View style={styles.center}>
        {/* Spotify placeholder */}
        <GlassCard style={styles.spotifyCard}>
          <View style={styles.spotifyIcon}>
            <Text style={styles.spotifyEmoji}>S</Text>
          </View>
          <Text style={styles.spotifyTitle}>Spotify</Text>
          <Text style={styles.spotifyDesc}>
            We'll scan your listening history to understand your musical mind.
          </Text>

          {!analyzing && !done && (
            <Button
              title="Connect & Analyze"
              onPress={startAnalysis}
              variant="primary"
              size="md"
              style={{ marginTop: 20 }}
            />
          )}

          {analyzing && (
            <Animated.View entering={FadeIn.duration(300)} style={styles.progressSection}>
              <ProgressBar progress={progress} color="#1DB954" height={6} />
              <Text style={styles.phaseText}>{phase}</Text>
              <Text style={styles.percentText}>{Math.round(progress * 100)}%</Text>
            </Animated.View>
          )}
        </GlassCard>
      </View>

      {done && (
        <Animated.View entering={FadeInDown.duration(500)} style={styles.footer}>
          <Button title="Continue" onPress={() => nav.navigate("NameEntry")} size="lg" />
        </Animated.View>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#000000", paddingHorizontal: 16 },
  title: { fontSize: 28, fontFamily: "Saira_700Bold", color: "#fff", marginTop: 16 },
  subtitle: { fontSize: 14, fontFamily: "Inter_400Regular", color: "rgba(255,255,255,0.5)", marginTop: 8 },
  center: { flex: 1, justifyContent: "center" },
  spotifyCard: { alignItems: "center", paddingVertical: 32 },
  spotifyIcon: {
    width: 64, height: 64, borderRadius: 32,
    backgroundColor: "#1DB954", alignItems: "center", justifyContent: "center",
    marginBottom: 16,
  },
  spotifyEmoji: { fontSize: 28, fontFamily: "Saira_700Bold", color: "#fff" },
  spotifyTitle: { fontSize: 20, fontFamily: "Saira_600SemiBold", color: "#fff" },
  spotifyDesc: { fontSize: 13, fontFamily: "Inter_400Regular", color: "rgba(255,255,255,0.5)", textAlign: "center", marginTop: 8, paddingHorizontal: 24 },
  progressSection: { width: "100%", marginTop: 24, gap: 8, paddingHorizontal: 16 },
  phaseText: { fontSize: 12, fontFamily: "Inter_500Medium", color: "rgba(255,255,255,0.6)", textAlign: "center" },
  percentText: { fontSize: 24, fontFamily: "JetBrainsMono_500Medium", color: "#1DB954", textAlign: "center" },
  footer: { paddingVertical: 16 },
});
