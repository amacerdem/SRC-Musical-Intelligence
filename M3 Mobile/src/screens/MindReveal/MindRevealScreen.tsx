import React, { useEffect, useState, useCallback } from "react";
import { View, Text, StyleSheet, Dimensions } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Animated, {
  FadeIn,
  FadeInDown,
  FadeInUp,
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withRepeat,
  withSequence,
  withDelay,
  Easing,
} from "react-native-reanimated";
import { useNavigation, CommonActions } from "@react-navigation/native";
import { useM3Store } from "../../stores/useM3Store";
import { personas } from "../../data/personas";
import { GENE_NAMES } from "../../types/m3";
import { Button } from "../../components/ui/Button";
import { Badge } from "../../components/ui/Badge";
import { GlassCard } from "../../components/ui/GlassCard";
import { colors, familyColors } from "../../design/tokens";

/* ── Gene Colors ─────────────────────────────────────────────────────── */

const GENE_COLORS: Record<string, string> = {
  entropy: "#06B6D4",
  resolution: "#10B981",
  tension: "#EF4444",
  resonance: "#8B5CF6",
  plasticity: "#EC4899",
};

/* ── Layout ──────────────────────────────────────────────────────────── */

const { width: SCREEN_WIDTH } = Dimensions.get("window");
const BAR_TRACK_WIDTH = SCREEN_WIDTH - 48 - 32 - 70 - 8 - 36 - 8;
// 48=horizontal padding, 32=GlassCard padding, 70=geneName width, 36=value width, gaps

/* ── Animated Gene Bar ───────────────────────────────────────────────── */

function AnimatedGeneBar({
  gene,
  value,
  index,
  visible,
}: {
  gene: string;
  value: number;
  index: number;
  visible: boolean;
}) {
  const barWidth = useSharedValue(0);
  const displayValue = useSharedValue(0);
  const [renderedValue, setRenderedValue] = useState(0);
  const targetPct = Math.round(value * 100);
  const color = GENE_COLORS[gene] ?? colors.violet;

  useEffect(() => {
    if (!visible) return;

    const staggerDelay = index * 200;

    barWidth.value = withDelay(
      staggerDelay,
      withTiming(targetPct, { duration: 800, easing: Easing.out(Easing.cubic) })
    );

    // Count-up effect for the numeric value
    const stepDuration = 800;
    const steps = 20;
    const stepTime = stepDuration / steps;
    let currentStep = 0;

    const timeout = setTimeout(() => {
      const interval = setInterval(() => {
        currentStep++;
        const progress = Math.min(currentStep / steps, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // cubic ease-out
        setRenderedValue(Math.round(targetPct * eased));
        if (currentStep >= steps) clearInterval(interval);
      }, stepTime);
    }, staggerDelay);

    return () => clearTimeout(timeout);
  }, [visible, targetPct, index]);

  const barStyle = useAnimatedStyle(() => ({
    width: `${barWidth.value}%`,
    backgroundColor: color,
    opacity: 0.6 + (barWidth.value / targetPct || 0) * 0.4,
  }));

  return (
    <View style={styles.geneRow}>
      <Text style={styles.geneName}>{gene}</Text>
      <View style={styles.geneBarTrack}>
        <Animated.View style={[styles.geneBarFill, barStyle]} />
      </View>
      <Text style={[styles.geneValue, { color }]}>{renderedValue}</Text>
    </View>
  );
}

/* ── Staggered Name Characters ───────────────────────────────────────── */

function StaggeredName({ name, color }: { name: string; color: string }) {
  return (
    <View style={styles.nameRow}>
      {name.split("").map((char, i) => (
        <Animated.Text
          key={`${char}-${i}`}
          entering={FadeIn.delay(3500 + i * 80).duration(300)}
          style={[styles.personaName, { color }]}
        >
          {char}
        </Animated.Text>
      ))}
    </View>
  );
}

/* ── Main Screen ─────────────────────────────────────────────────────── */

export function MindRevealScreen() {
  const navigation = useNavigation();
  const mind = useM3Store((s) => s.mind);

  const persona = mind
    ? personas.find((p) => p.id === mind.activePersonaId) ?? personas[0]
    : personas[0];
  const pColor = persona.color;
  const fColor = familyColors[persona.family] ?? colors.violet;
  const genes = mind?.genes ?? {
    entropy: 0.2,
    resolution: 0.2,
    tension: 0.2,
    resonance: 0.2,
    plasticity: 0.2,
  };

  /* ── Phase state ──────────────────────────────────────────────────── */

  const [phase, setPhase] = useState<1 | 2 | 3>(1);

  useEffect(() => {
    const t2 = setTimeout(() => setPhase(2), 2000);
    const t3 = setTimeout(() => setPhase(3), 5000);
    return () => {
      clearTimeout(t2);
      clearTimeout(t3);
    };
  }, []);

  /* ── Phase 1: pulsing dot ─────────────────────────────────────────── */

  const dotScale = useSharedValue(1);

  useEffect(() => {
    dotScale.value = withRepeat(
      withSequence(
        withTiming(2, { duration: 900, easing: Easing.inOut(Easing.ease) }),
        withTiming(1, { duration: 900, easing: Easing.inOut(Easing.ease) })
      ),
      -1,
      true
    );
  }, []);

  const dotAnimStyle = useAnimatedStyle(() => ({
    width: 8 * dotScale.value,
    height: 8 * dotScale.value,
    borderRadius: 4 * dotScale.value,
    backgroundColor: pColor,
    shadowColor: pColor,
    shadowOpacity: 0.8,
    shadowRadius: 12,
    shadowOffset: { width: 0, height: 0 },
  }));

  /* ── Phase 2: expanding circle ────────────────────────────────────── */

  const circleSize = useSharedValue(8);
  const circleOpacity = useSharedValue(0);

  useEffect(() => {
    if (phase >= 2) {
      circleSize.value = withTiming(80, {
        duration: 800,
        easing: Easing.out(Easing.cubic),
      });
      circleOpacity.value = withTiming(1, { duration: 600 });
    }
  }, [phase]);

  const circleAnimStyle = useAnimatedStyle(() => ({
    width: circleSize.value,
    height: circleSize.value,
    borderRadius: circleSize.value / 2,
    opacity: circleOpacity.value,
  }));

  /* ── Navigation ───────────────────────────────────────────────────── */

  const onEnter = useCallback(() => {
    navigation.dispatch(
      CommonActions.reset({
        index: 0,
        routes: [{ name: "MainTabs" as never }],
      })
    );
  }, [navigation]);

  /* ── Render ───────────────────────────────────────────────────────── */

  return (
    <View style={styles.container}>
      {/* Radial glow background */}
      <View style={styles.glowContainer} pointerEvents="none">
        <View
          style={[
            styles.glowOrb,
            {
              backgroundColor: pColor,
              shadowColor: pColor,
            },
          ]}
        />
      </View>

      <SafeAreaView style={styles.safeArea}>
        <View style={styles.center}>
          {/* ─── PHASE 1: Void ───────────────────────────────────────── */}
          {phase === 1 && (
            <>
              <Animated.View style={dotAnimStyle} />
              <Animated.Text
                entering={FadeIn.duration(800)}
                style={styles.preparingText}
              >
                Preparing...
              </Animated.Text>
            </>
          )}

          {/* ─── PHASE 2: Birth ──────────────────────────────────────── */}
          {phase >= 2 && (
            <>
              {/* Expanding circle with persona initial */}
              <Animated.View
                style={[
                  styles.avatarCircle,
                  { borderColor: `${pColor}40` },
                  circleAnimStyle,
                ]}
              >
                <Animated.Text
                  entering={FadeIn.delay(400).duration(500)}
                  style={[styles.avatarLetter, { color: pColor }]}
                >
                  {persona.name.charAt(0)}
                </Animated.Text>
              </Animated.View>

              {/* "You are..." */}
              <Animated.Text
                entering={FadeIn.delay(500).duration(600)}
                style={styles.youAreText}
              >
                You are...
              </Animated.Text>

              {/* Persona name: staggered character reveal */}
              <StaggeredName name={persona.name} color={pColor} />

              {/* Family badge */}
              <Animated.View
                entering={FadeIn.delay(4000).duration(500)}
                style={styles.badgeWrap}
              >
                <Badge label={persona.family} color={fColor} />
              </Animated.View>

              {/* Tagline */}
              <Animated.Text
                entering={FadeInDown.delay(4500).duration(500)}
                style={styles.tagline}
              >
                "{persona.tagline}"
              </Animated.Text>
            </>
          )}

          {/* ─── PHASE 3: Stats ──────────────────────────────────────── */}
          {phase >= 3 && (
            <Animated.View
              entering={FadeInUp.delay(0).duration(700)}
              style={styles.geneSection}
            >
              <GlassCard>
                <Text style={styles.geneTitle}>Gene Signature</Text>
                {GENE_NAMES.map((g, i) => (
                  <AnimatedGeneBar
                    key={g}
                    gene={g}
                    value={genes[g]}
                    index={i}
                    visible={phase >= 3}
                  />
                ))}

                {/* Level badge */}
                <Animated.View
                  entering={FadeIn.delay(1200).duration(500)}
                  style={styles.levelBadgeWrap}
                >
                  <View style={styles.levelBadge}>
                    <Text style={styles.levelBadgeText}>
                      Level 1  ·  Stage I
                    </Text>
                  </View>
                </Animated.View>
              </GlassCard>
            </Animated.View>
          )}
        </View>

        {/* Enter button — fades in at ~7s (phase 3 + 2s delay) */}
        {phase >= 3 && (
          <Animated.View
            entering={FadeInDown.delay(2000).duration(600)}
            style={styles.footer}
          >
            <Button title="Enter Your Mind" onPress={onEnter} size="lg" />
          </Animated.View>
        )}
      </SafeAreaView>
    </View>
  );
}

/* ── Styles ──────────────────────────────────────────────────────────── */

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#000000",
  },
  safeArea: {
    flex: 1,
    justifyContent: "space-between",
    paddingHorizontal: 24,
  },
  center: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },

  /* Background glow */
  glowContainer: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: "center",
    alignItems: "center",
  },
  glowOrb: {
    width: 300,
    height: 300,
    borderRadius: 150,
    opacity: 0.08,
    shadowOpacity: 1,
    shadowRadius: 120,
    shadowOffset: { width: 0, height: 0 },
  },

  /* Phase 1 */
  preparingText: {
    fontSize: 14,
    fontFamily: "Inter_400Regular",
    color: "rgba(255,255,255,0.25)",
    marginTop: 24,
    letterSpacing: 2,
  },

  /* Phase 2 */
  avatarCircle: {
    backgroundColor: "rgba(255,255,255,0.04)",
    borderWidth: 2,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 20,
    overflow: "hidden",
  },
  avatarLetter: {
    fontSize: 36,
    fontFamily: "Saira_700Bold",
  },
  youAreText: {
    fontSize: 15,
    fontFamily: "Inter_500Medium",
    color: "rgba(255,255,255,0.4)",
    marginBottom: 8,
    letterSpacing: 1.5,
  },
  nameRow: {
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "center",
    marginBottom: 12,
  },
  personaName: {
    fontSize: 32,
    fontFamily: "Saira_700Bold",
    textAlign: "center",
  },
  badgeWrap: {
    marginBottom: 8,
    alignSelf: "center",
  },
  tagline: {
    fontSize: 14,
    fontFamily: "Inter_400Regular",
    color: "rgba(255,255,255,0.4)",
    fontStyle: "italic",
    textAlign: "center",
    paddingHorizontal: 32,
    marginBottom: 4,
  },

  /* Phase 3 */
  geneSection: {
    width: SCREEN_WIDTH - 48,
    marginTop: 28,
  },
  geneTitle: {
    fontSize: 13,
    fontFamily: "Saira_600SemiBold",
    color: "rgba(255,255,255,0.6)",
    marginBottom: 14,
    textTransform: "uppercase",
    letterSpacing: 1.5,
  },
  geneRow: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 10,
    gap: 8,
  },
  geneName: {
    fontSize: 11,
    fontFamily: "Inter_500Medium",
    color: "rgba(255,255,255,0.5)",
    width: 70,
    textTransform: "capitalize",
  },
  geneBarTrack: {
    flex: 1,
    height: 6,
    borderRadius: 3,
    backgroundColor: "rgba(255,255,255,0.06)",
    overflow: "hidden",
  },
  geneBarFill: {
    height: 6,
    borderRadius: 3,
  },
  geneValue: {
    fontSize: 12,
    fontFamily: "JetBrainsMono_500Medium",
    width: 36,
    textAlign: "right",
  },
  levelBadgeWrap: {
    marginTop: 14,
    alignItems: "center",
  },
  levelBadge: {
    backgroundColor: "rgba(255,255,255,0.05)",
    borderRadius: 8,
    paddingHorizontal: 14,
    paddingVertical: 6,
    borderWidth: StyleSheet.hairlineWidth,
    borderColor: "rgba(255,255,255,0.1)",
  },
  levelBadgeText: {
    fontSize: 12,
    fontFamily: "JetBrainsMono_400Regular",
    color: "rgba(255,255,255,0.5)",
    letterSpacing: 1,
  },

  /* Footer */
  footer: {
    paddingVertical: 16,
  },
});
