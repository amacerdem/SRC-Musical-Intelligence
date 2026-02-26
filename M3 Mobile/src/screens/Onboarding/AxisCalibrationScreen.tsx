import React, { useState } from "react";
import { View, Text, StyleSheet, Platform } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Animated, { FadeInDown } from "react-native-reanimated";
import Slider from "@react-native-community/slider";
import { useNavigation } from "@react-navigation/native";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";
import type { OnboardingStackParamList } from "../../navigation/types";
import { Button } from "../../components/ui/Button";
import { GlassCard } from "../../components/ui/GlassCard";
import { colors } from "../../design/tokens";

const AXES = [
  { key: "entropy", label: "Entropy Tolerance", low: "Order", high: "Chaos", color: colors.tempo },
  { key: "resolution", label: "Resolution Craving", low: "Open", high: "Closed", color: colors.familiarity },
  { key: "monotony", label: "Monotony Tolerance", low: "Variety", high: "Repetition", color: colors.salience },
  { key: "salience", label: "Salience Sensitivity", low: "Relaxed", high: "Alert", color: colors.consonance },
  { key: "tension", label: "Tension Appetite", low: "Gentle", high: "Intense", color: colors.danger },
];

export function AxisCalibrationScreen() {
  const nav = useNavigation<NativeStackNavigationProp<OnboardingStackParamList>>();
  const [values, setValues] = useState<Record<string, number>>({
    entropy: 0.5, resolution: 0.5, monotony: 0.5, salience: 0.5, tension: 0.5,
  });

  return (
    <SafeAreaView style={styles.container}>
      <Animated.View entering={FadeInDown.duration(500)}>
        <Text style={styles.title}>Calibrate Your Mind</Text>
        <Text style={styles.subtitle}>
          Adjust each axis to reflect your musical personality.
        </Text>
      </Animated.View>

      <View style={styles.sliderContainer}>
        {AXES.map((axis, i) => (
          <Animated.View key={axis.key} entering={FadeInDown.delay(100 * i).duration(500)}>
            <GlassCard style={styles.sliderCard}>
              <View style={styles.labelRow}>
                <Text style={styles.axisLabel}>{axis.label}</Text>
                <Text style={[styles.valueText, { color: axis.color }]}>
                  {Math.round(values[axis.key] * 100)}
                </Text>
              </View>
              <View style={styles.sliderRow}>
                <Text style={styles.extremeLabel}>{axis.low}</Text>
                <View style={styles.sliderWrap}>
                  <Slider
                    style={styles.slider}
                    value={values[axis.key]}
                    onValueChange={(v) => setValues((prev) => ({ ...prev, [axis.key]: v }))}
                    minimumValue={0}
                    maximumValue={1}
                    step={0.01}
                    minimumTrackTintColor={axis.color}
                    maximumTrackTintColor="rgba(255,255,255,0.08)"
                    thumbTintColor={axis.color}
                  />
                </View>
                <Text style={styles.extremeLabel}>{axis.high}</Text>
              </View>
            </GlassCard>
          </Animated.View>
        ))}
      </View>

      <View style={styles.footer}>
        <Button title="Continue" onPress={() => nav.navigate("ListeningImport")} size="lg" />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#000000", paddingHorizontal: 16 },
  title: { fontSize: 28, fontFamily: "Saira_700Bold", color: "#fff", marginTop: 16 },
  subtitle: { fontSize: 14, fontFamily: "Inter_400Regular", color: "rgba(255,255,255,0.5)", marginTop: 8, marginBottom: 24 },
  sliderContainer: { flex: 1, gap: 12 },
  sliderCard: { paddingVertical: 12, paddingHorizontal: 14 },
  labelRow: { flexDirection: "row", justifyContent: "space-between", marginBottom: 4 },
  axisLabel: { fontSize: 13, fontFamily: "Saira_600SemiBold", color: "#fff" },
  valueText: { fontSize: 13, fontFamily: "JetBrainsMono_500Medium" },
  sliderRow: { flexDirection: "row", alignItems: "center", gap: 8 },
  extremeLabel: { fontSize: 10, fontFamily: "Inter_400Regular", color: "rgba(255,255,255,0.3)", width: 48 },
  sliderWrap: { flex: 1 },
  slider: { width: "100%", height: 32 },
  footer: { paddingVertical: 16 },
});
