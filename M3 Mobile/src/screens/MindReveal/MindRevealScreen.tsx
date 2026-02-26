import React from "react";
import { View, Text, StyleSheet, Dimensions } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Animated, { FadeIn, FadeInDown, FadeInUp } from "react-native-reanimated";
import { useNavigation, CommonActions } from "@react-navigation/native";
import { useM3Store } from "../../stores/useM3Store";
import { personas } from "../../data/personas";
import { GENE_NAMES } from "../../types/m3";
import { Button } from "../../components/ui/Button";
import { Badge } from "../../components/ui/Badge";
import { GlassCard } from "../../components/ui/GlassCard";
import { colors, familyColors } from "../../design/tokens";

const GENE_COLORS: Record<string, string> = {
  entropy: colors.tempo,
  resolution: colors.familiarity,
  tension: colors.danger,
  resonance: colors.success,
  plasticity: colors.reward,
};

const { width } = Dimensions.get("window");

export function MindRevealScreen() {
  const navigation = useNavigation();
  const mind = useM3Store((s) => s.mind);

  const persona = mind
    ? personas.find((p) => p.id === mind.activePersonaId) ?? personas[0]
    : personas[0];
  const fColor = familyColors[persona.family] ?? colors.violet;
  const genes = mind?.genes ?? { entropy: 0.2, resolution: 0.2, tension: 0.2, resonance: 0.2, plasticity: 0.2 };

  const onEnter = () => {
    navigation.dispatch(
      CommonActions.reset({ index: 0, routes: [{ name: "MainTabs" as never }] })
    );
  };

  return (
    <View style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        {/* Persona name reveal */}
        <View style={styles.center}>
          <Animated.View entering={FadeIn.delay(500).duration(1200)} style={styles.avatarCircle}>
            <Text style={[styles.avatarLetter, { color: fColor }]}>
              {persona.name.charAt(0)}
            </Text>
          </Animated.View>

          <Animated.Text
            entering={FadeInUp.delay(1000).duration(800)}
            style={[styles.personaName, { color: fColor }]}
          >
            {persona.name}
          </Animated.Text>

          <Animated.View entering={FadeIn.delay(1400).duration(600)}>
            <Badge label={persona.family} color={fColor} />
          </Animated.View>

          <Animated.Text
            entering={FadeInDown.delay(1800).duration(600)}
            style={styles.bornText}
          >
            Your mind has been born.
          </Animated.Text>

          <Animated.Text
            entering={FadeInDown.delay(2200).duration(600)}
            style={styles.tagline}
          >
            "{persona.tagline}"
          </Animated.Text>

          {/* Gene bars */}
          <Animated.View entering={FadeInDown.delay(2600).duration(600)} style={styles.geneSection}>
            <GlassCard>
              <Text style={styles.geneTitle}>Gene Signature</Text>
              {GENE_NAMES.map((g) => (
                <View key={g} style={styles.geneRow}>
                  <Text style={styles.geneName}>{g}</Text>
                  <View style={styles.geneBarTrack}>
                    <View
                      style={[
                        styles.geneBarFill,
                        {
                          width: `${Math.round(genes[g] * 100)}%`,
                          backgroundColor: GENE_COLORS[g] ?? colors.violet,
                        },
                      ]}
                    />
                  </View>
                  <Text style={styles.geneValue}>
                    {Math.round(genes[g] * 100)}
                  </Text>
                </View>
              ))}
            </GlassCard>
          </Animated.View>
        </View>

        {/* Enter button */}
        <Animated.View entering={FadeInDown.delay(3000).duration(600)} style={styles.footer}>
          <Button title="Enter Your Mind" onPress={onEnter} size="lg" />
        </Animated.View>
      </SafeAreaView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#000000" },
  safeArea: { flex: 1, justifyContent: "space-between", paddingHorizontal: 24 },
  center: { flex: 1, justifyContent: "center", alignItems: "center" },
  avatarCircle: {
    width: 80, height: 80, borderRadius: 40,
    backgroundColor: "rgba(255,255,255,0.05)",
    borderWidth: 2, borderColor: "rgba(255,255,255,0.1)",
    alignItems: "center", justifyContent: "center",
    marginBottom: 16,
  },
  avatarLetter: { fontSize: 36, fontFamily: "Saira_700Bold" },
  personaName: { fontSize: 32, fontFamily: "Saira_700Bold", marginBottom: 12, textAlign: "center" },
  bornText: { fontSize: 16, fontFamily: "Inter_500Medium", color: "rgba(255,255,255,0.7)", marginTop: 24 },
  tagline: { fontSize: 14, fontFamily: "Inter_400Regular", color: "rgba(255,255,255,0.4)", marginTop: 8, fontStyle: "italic", textAlign: "center", paddingHorizontal: 32 },
  geneSection: { width: width - 48, marginTop: 32 },
  geneTitle: { fontSize: 13, fontFamily: "Saira_600SemiBold", color: "rgba(255,255,255,0.6)", marginBottom: 12, textTransform: "uppercase", letterSpacing: 1 },
  geneRow: { flexDirection: "row", alignItems: "center", marginBottom: 8, gap: 8 },
  geneName: { fontSize: 11, fontFamily: "Inter_500Medium", color: "rgba(255,255,255,0.5)", width: 70, textTransform: "capitalize" },
  geneBarTrack: { flex: 1, height: 6, borderRadius: 3, backgroundColor: "rgba(255,255,255,0.06)" },
  geneBarFill: { height: 6, borderRadius: 3 },
  geneValue: { fontSize: 11, fontFamily: "JetBrainsMono_400Regular", color: "rgba(255,255,255,0.4)", width: 28, textAlign: "right" },
  footer: { paddingVertical: 16 },
});
