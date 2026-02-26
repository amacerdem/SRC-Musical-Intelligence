import React from "react";
import { View, Text, StyleSheet, Dimensions, TouchableOpacity } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Animated, { FadeInDown, FadeInUp } from "react-native-reanimated";
import { LinearGradient } from "expo-linear-gradient";
import { useTranslation } from "react-i18next";
import { useNavigation } from "@react-navigation/native";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";
import type { RootStackParamList } from "../../navigation/types";
import { Button } from "../../components/ui/Button";
import { colors } from "../../design/tokens";

const { height: SCREEN_HEIGHT } = Dimensions.get("window");

export function LandingScreen() {
  const { t, i18n } = useTranslation();
  const navigation = useNavigation<NativeStackNavigationProp<RootStackParamList>>();
  const currentLang = i18n.language ?? "en";

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={["#000000", "#0a0015", "#120025"]}
        style={StyleSheet.absoluteFill}
      />
      <SafeAreaView style={styles.safeArea}>
        {/* Language Toggle */}
        <Animated.View entering={FadeInDown.delay(200).duration(600)} style={styles.langRow}>
          <TouchableOpacity
            onPress={() => i18n.changeLanguage(currentLang === "en" ? "tr" : "en")}
            style={styles.langBtn}
          >
            <Text style={styles.langText}>{currentLang === "en" ? "TR" : "EN"}</Text>
          </TouchableOpacity>
        </Animated.View>

        {/* Center Content */}
        <View style={styles.centerContent}>
          <Animated.Text
            entering={FadeInUp.delay(400).duration(800)}
            style={styles.title}
          >
            M³
          </Animated.Text>
          <Animated.Text
            entering={FadeInUp.delay(600).duration(800)}
            style={styles.subtitle}
          >
            My Musical Mind
          </Animated.Text>
          <Animated.Text
            entering={FadeInUp.delay(800).duration(800)}
            style={styles.tagline}
          >
            Your mind has a sound. Discover it.
          </Animated.Text>
        </View>

        {/* Bottom Buttons */}
        <Animated.View entering={FadeInDown.delay(1000).duration(600)} style={styles.buttonContainer}>
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
        <Animated.Text
          entering={FadeInDown.delay(1200).duration(600)}
          style={styles.copyright}
        >
          SRC⁹ Musical Intelligence
        </Animated.Text>
      </SafeAreaView>
    </View>
  );
}

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
    borderColor: "rgba(255,255,255,0.1)",
  },
  langText: {
    fontSize: 13,
    fontFamily: "Inter_600SemiBold",
    color: "rgba(255,255,255,0.6)",
  },
  centerContent: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  title: {
    fontSize: 72,
    fontFamily: "Saira_700Bold",
    color: "#8B5CF6",
    letterSpacing: 4,
    textShadowColor: "rgba(139,92,246,0.5)",
    textShadowOffset: { width: 0, height: 0 },
    textShadowRadius: 30,
  },
  subtitle: {
    fontSize: 20,
    fontFamily: "Saira_500Medium",
    color: "rgba(255,255,255,0.8)",
    marginTop: 8,
    letterSpacing: 2,
  },
  tagline: {
    fontSize: 14,
    fontFamily: "Inter_400Regular",
    color: "rgba(255,255,255,0.4)",
    marginTop: 16,
    fontStyle: "italic",
  },
  buttonContainer: {
    paddingBottom: 16,
  },
  copyright: {
    textAlign: "center",
    fontSize: 11,
    fontFamily: "Inter_400Regular",
    color: "rgba(255,255,255,0.2)",
    paddingBottom: 12,
  },
});
