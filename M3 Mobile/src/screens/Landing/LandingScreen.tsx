import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, Dimensions, TouchableOpacity } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Animated, {
  FadeInDown,
  FadeInUp,
  useSharedValue,
  useAnimatedStyle,
  withRepeat,
  withTiming,
  withDelay,
  Easing,
  FadeIn,
} from "react-native-reanimated";
import { LinearGradient } from "expo-linear-gradient";
import { useTranslation } from "react-i18next";
import { useNavigation } from "@react-navigation/native";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";
import type { RootStackParamList } from "../../navigation/types";
import { Button } from "../../components/ui/Button";
import { colors } from "../../design/tokens";

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get("window");
const CENTER_X = SCREEN_WIDTH / 2;
const CENTER_Y = SCREEN_HEIGHT / 2;

/* -------------------------------------------------------------------------- */
/*  Orbital Dot Configuration                                                  */
/* -------------------------------------------------------------------------- */

interface OrbitalDotConfig {
  color: string;
  size: number;
  radius: number;
  duration: number; // ms for one full revolution
  startAngle: number; // radians
  glowOpacity: number;
}

const ORBITAL_DOTS: OrbitalDotConfig[] = [
  { color: "#8B5CF6", size: 10, radius: 120, duration: 12000, startAngle: 0, glowOpacity: 0.5 },
  { color: "#06B6D4", size: 8, radius: 90, duration: 9000, startAngle: Math.PI * 0.4, glowOpacity: 0.45 },
  { color: "#F59E0B", size: 12, radius: 155, duration: 18000, startAngle: Math.PI * 0.9, glowOpacity: 0.5 },
  { color: "#10B981", size: 7, radius: 70, duration: 14000, startAngle: Math.PI * 1.3, glowOpacity: 0.4 },
  { color: "#EF4444", size: 9, radius: 140, duration: 10000, startAngle: Math.PI * 1.7, glowOpacity: 0.45 },
  { color: "#EC4899", size: 6, radius: 105, duration: 16000, startAngle: Math.PI * 0.6, glowOpacity: 0.4 },
  { color: "#3B82F6", size: 11, radius: 180, duration: 20000, startAngle: Math.PI * 1.1, glowOpacity: 0.5 },
];

/* -------------------------------------------------------------------------- */
/*  OrbitalDot Component                                                       */
/* -------------------------------------------------------------------------- */

function OrbitalDot({ config, delay: enterDelay }: { config: OrbitalDotConfig; delay: number }) {
  const progress = useSharedValue(config.startAngle);

  useEffect(() => {
    // Animate from startAngle to startAngle + 2*PI, repeating forever
    progress.value = config.startAngle;
    progress.value = withDelay(
      enterDelay,
      withRepeat(
        withTiming(config.startAngle + Math.PI * 2, {
          duration: config.duration,
          easing: Easing.linear,
        }),
        -1, // infinite
        false // don't reverse
      )
    );
  }, []);

  // Fade in the dot
  const opacity = useSharedValue(0);
  useEffect(() => {
    opacity.value = withDelay(
      enterDelay,
      withTiming(1, { duration: 1500, easing: Easing.out(Easing.cubic) })
    );
  }, []);

  const dotStyle = useAnimatedStyle(() => {
    const x = Math.cos(progress.value) * config.radius;
    const y = Math.sin(progress.value) * config.radius;
    return {
      transform: [
        { translateX: x - config.size / 2 },
        { translateY: y - config.size / 2 },
      ],
      opacity: opacity.value,
    };
  });

  // Outer glow layers
  const glowSize = config.size * 3;
  const glowSize2 = config.size * 5;

  return (
    <Animated.View
      style={[
        {
          position: "absolute",
          left: CENTER_X,
          top: CENTER_Y - 40, // offset slightly above true center for visual balance
          width: config.size,
          height: config.size,
        },
        dotStyle,
      ]}
    >
      {/* Outer glow */}
      <View
        style={{
          position: "absolute",
          width: glowSize2,
          height: glowSize2,
          borderRadius: glowSize2 / 2,
          backgroundColor: config.color,
          opacity: config.glowOpacity * 0.1,
          left: -(glowSize2 - config.size) / 2,
          top: -(glowSize2 - config.size) / 2,
        }}
      />
      {/* Mid glow */}
      <View
        style={{
          position: "absolute",
          width: glowSize,
          height: glowSize,
          borderRadius: glowSize / 2,
          backgroundColor: config.color,
          opacity: config.glowOpacity * 0.25,
          left: -(glowSize - config.size) / 2,
          top: -(glowSize - config.size) / 2,
        }}
      />
      {/* Core */}
      <View
        style={{
          width: config.size,
          height: config.size,
          borderRadius: config.size / 2,
          backgroundColor: config.color,
          opacity: 0.9,
        }}
      />
    </Animated.View>
  );
}

/* -------------------------------------------------------------------------- */
/*  Pulsing Title Component                                                    */
/* -------------------------------------------------------------------------- */

function PulsingTitle() {
  const glowRadius = useSharedValue(20);

  useEffect(() => {
    glowRadius.value = withRepeat(
      withTiming(50, { duration: 2500, easing: Easing.inOut(Easing.sin) }),
      -1,
      true // reverse (breathe in and out)
    );
  }, []);

  const titleStyle = useAnimatedStyle(() => ({
    textShadowRadius: glowRadius.value,
  }));

  return (
    <Animated.Text
      entering={FadeInUp.delay(400).duration(1000).easing(Easing.out(Easing.cubic))}
      style={[styles.title, titleStyle]}
    >
      M{"\u00B3"}
    </Animated.Text>
  );
}

/* -------------------------------------------------------------------------- */
/*  Typewriter Subtitle Component                                              */
/* -------------------------------------------------------------------------- */

function TypewriterText({
  text,
  delayMs,
  durationMs,
  style,
}: {
  text: string;
  delayMs: number;
  durationMs: number;
  style: any;
}) {
  const [displayed, setDisplayed] = useState("");
  const [started, setStarted] = useState(false);

  useEffect(() => {
    const startTimeout = setTimeout(() => setStarted(true), delayMs);
    return () => clearTimeout(startTimeout);
  }, [delayMs]);

  useEffect(() => {
    if (!started) return;
    const charDelay = durationMs / text.length;
    let idx = 0;
    const interval = setInterval(() => {
      idx++;
      setDisplayed(text.slice(0, idx));
      if (idx >= text.length) clearInterval(interval);
    }, charDelay);
    return () => clearInterval(interval);
  }, [started, text, durationMs]);

  if (!started) return null;

  return (
    <Animated.Text entering={FadeIn.duration(300)} style={style}>
      {displayed}
      <Text style={{ opacity: displayed.length < text.length ? 1 : 0 }}>|</Text>
    </Animated.Text>
  );
}

/* -------------------------------------------------------------------------- */
/*  Main Landing Screen                                                        */
/* -------------------------------------------------------------------------- */

export function LandingScreen() {
  const { t, i18n } = useTranslation();
  const navigation = useNavigation<NativeStackNavigationProp<RootStackParamList>>();
  const currentLang = i18n.language ?? "en";

  // Ambient background pulse
  const ambientOpacity = useSharedValue(0.03);
  useEffect(() => {
    ambientOpacity.value = withRepeat(
      withTiming(0.08, { duration: 4000, easing: Easing.inOut(Easing.sin) }),
      -1,
      true
    );
  }, []);

  const ambientStyle = useAnimatedStyle(() => ({
    opacity: ambientOpacity.value,
  }));

  return (
    <View style={styles.container}>
      {/* Multi-stop gradient background */}
      <LinearGradient
        colors={["#000000", "#05000d", "#0a0015", "#0d001f", "#120025"]}
        locations={[0, 0.25, 0.5, 0.75, 1]}
        style={StyleSheet.absoluteFill}
      />

      {/* Radial ambient glow in center (faux radial gradient) */}
      <Animated.View style={[styles.ambientGlow, ambientStyle]} />

      {/* Orbital Dots */}
      {ORBITAL_DOTS.map((dot, i) => (
        <OrbitalDot key={i} config={dot} delay={800 + i * 200} />
      ))}

      <SafeAreaView style={styles.safeArea}>
        {/* Language Toggle */}
        <Animated.View entering={FadeInDown.delay(200).duration(600)} style={styles.langRow}>
          <TouchableOpacity
            onPress={() => i18n.changeLanguage(currentLang === "en" ? "tr" : "en")}
            style={styles.langBtn}
            activeOpacity={0.7}
          >
            <Text style={styles.langText}>{currentLang === "en" ? "TR" : "EN"}</Text>
          </TouchableOpacity>
        </Animated.View>

        {/* Center Content */}
        <View style={styles.centerContent}>
          {/* Pulsing M3 Title */}
          <PulsingTitle />

          {/* Subtitle */}
          <Animated.Text
            entering={FadeInUp.delay(700).duration(800).easing(Easing.out(Easing.cubic))}
            style={styles.subtitle}
          >
            My Musical Mind
          </Animated.Text>

          {/* Typewriter Tagline */}
          <TypewriterText
            text="Your mind has a sound. Discover it."
            delayMs={1400}
            durationMs={2000}
            style={styles.tagline}
          />
        </View>

        {/* Bottom Buttons */}
        <Animated.View
          entering={FadeInDown.delay(1200).duration(700).easing(Easing.out(Easing.cubic))}
          style={styles.buttonContainer}
        >
          <Button
            title="Begin Your Journey"
            onPress={() => navigation.navigate("Onboarding")}
            variant="primary"
            size="lg"
          />
          <View style={{ height: 12 }} />
          <Button
            title="Explore"
            onPress={() => navigation.navigate("Onboarding")}
            variant="secondary"
            size="md"
          />
        </Animated.View>

        {/* Footer */}
        <Animated.View
          entering={FadeInDown.delay(1500).duration(600)}
          style={styles.footerContainer}
        >
          <Text style={styles.footerPrimary}>
            SRC{"\u2079"} Musical Intelligence
          </Text>
          <Text style={styles.footerSecondary}>
            MIT Media Lab {"\u00B7"} Stanford CCRMA {"\u00B7"} CMU School of Music
          </Text>
        </Animated.View>
      </SafeAreaView>
    </View>
  );
}

/* -------------------------------------------------------------------------- */
/*  Styles                                                                     */
/* -------------------------------------------------------------------------- */

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#000000",
  },
  ambientGlow: {
    position: "absolute",
    width: SCREEN_WIDTH * 1.2,
    height: SCREEN_WIDTH * 1.2,
    borderRadius: SCREEN_WIDTH * 0.6,
    backgroundColor: "#8B5CF6",
    left: CENTER_X - SCREEN_WIDTH * 0.6,
    top: CENTER_Y - SCREEN_WIDTH * 0.6 - 40,
  },
  safeArea: {
    flex: 1,
    justifyContent: "space-between",
    paddingHorizontal: 24,
  },
  langRow: {
    alignItems: "flex-end",
    paddingTop: 8,
  },
  langBtn: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
    backgroundColor: "rgba(255,255,255,0.05)",
    borderWidth: StyleSheet.hairlineWidth,
    borderColor: "rgba(255,255,255,0.12)",
  },
  langText: {
    fontSize: 13,
    fontFamily: "Inter_600SemiBold",
    color: "rgba(255,255,255,0.6)",
    letterSpacing: 1,
  },
  centerContent: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  title: {
    fontSize: 80,
    fontFamily: "Saira_700Bold",
    color: "#8B5CF6",
    letterSpacing: 6,
    textShadowColor: "rgba(139,92,246,0.6)",
    textShadowOffset: { width: 0, height: 0 },
    textShadowRadius: 30,
  },
  subtitle: {
    fontSize: 22,
    fontFamily: "Saira_500Medium",
    color: "rgba(255,255,255,0.85)",
    marginTop: 10,
    letterSpacing: 3,
  },
  tagline: {
    fontSize: 14,
    fontFamily: "Inter_400Regular",
    color: "rgba(255,255,255,0.4)",
    marginTop: 20,
    fontStyle: "italic",
    letterSpacing: 0.5,
    textAlign: "center",
  },
  buttonContainer: {
    paddingBottom: 16,
  },
  footerContainer: {
    alignItems: "center",
    paddingBottom: 14,
  },
  footerPrimary: {
    textAlign: "center",
    fontSize: 11,
    fontFamily: "Inter_500Medium",
    color: "rgba(255,255,255,0.2)",
    letterSpacing: 1,
  },
  footerSecondary: {
    textAlign: "center",
    fontSize: 9,
    fontFamily: "Inter_400Regular",
    color: "rgba(255,255,255,0.12)",
    marginTop: 4,
    letterSpacing: 0.5,
  },
});
