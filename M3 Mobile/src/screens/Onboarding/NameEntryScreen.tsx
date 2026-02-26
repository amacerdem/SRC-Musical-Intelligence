import React, { useState } from "react";
import { View, Text, TextInput, ScrollView, TouchableOpacity, StyleSheet } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Animated, { FadeInDown } from "react-native-reanimated";
import { useNavigation, CommonActions } from "@react-navigation/native";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";
import type { RootStackParamList } from "../../navigation/types";
import { useOnboardingStore } from "../../stores/useOnboardingStore";
import { useM3Store } from "../../stores/useM3Store";
import { useUserStore } from "../../stores/useUserStore";
import { personas } from "../../data/personas";
import { GlassCard } from "../../components/ui/GlassCard";
import { Button } from "../../components/ui/Button";
import { Badge } from "../../components/ui/Badge";
import { colors, familyColors } from "../../design/tokens";
import type { M3Tier } from "../../types/m3";

const PLANS = [
  { id: "pulse", tier: "basic" as M3Tier, name: "Pulse", price: "$5/mo", features: ["Weekly M³ updates", "Gene tracking", "Observations"] },
  { id: "resonance", tier: "premium" as M3Tier, name: "Resonance", price: "$10/mo", features: ["Daily updates", "Full C³ functions", "Predictions"] },
  { id: "transcendence", tier: "ultimate" as M3Tier, name: "Transcendence", price: "$20/mo", features: ["Real-time evolution", "Cross-mind", "Meta-layer"] },
];

export function NameEntryScreen() {
  const navigation = useNavigation<NativeStackNavigationProp<RootStackParamList>>();
  const selectedPersonaId = useOnboardingStore((s) => s.selectedPersonaId);
  const setSelectedPlan = useOnboardingStore((s) => s.setSelectedPlan);
  const selectedPlan = useOnboardingStore((s) => s.selectedPlan);
  const selectedTier = useOnboardingStore((s) => s.selectedTier);
  const birthM3 = useM3Store((s) => s.birthM3);
  const completeOnboarding = useUserStore((s) => s.completeOnboarding);

  const [name, setName] = useState("");

  const persona = personas.find((p) => p.id === selectedPersonaId) ?? personas[0];
  const fColor = familyColors[persona.family] ?? colors.violet;

  const onBirth = () => {
    birthM3(persona, selectedTier);
    completeOnboarding(
      {
        personaId: persona.id,
        stage: 1 as const,
        subTrait: null,
        axes: {
          entropyTolerance: persona.axes.entropyTolerance,
          resolutionCraving: persona.axes.resolutionCraving,
          monotonyTolerance: persona.axes.monotonyTolerance,
          salienceSensitivity: persona.axes.salienceSensitivity,
          tensionAppetite: persona.axes.tensionAppetite,
        },
      },
      name.trim() || "You"
    );
    navigation.dispatch(
      CommonActions.reset({ index: 0, routes: [{ name: "MindReveal" }] })
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.scroll}>
        <Animated.View entering={FadeInDown.duration(500)}>
          <Text style={styles.title}>Name Your Mind</Text>
        </Animated.View>

        {/* Name input */}
        <Animated.View entering={FadeInDown.delay(100).duration(500)}>
          <GlassCard>
            <Text style={styles.label}>Display Name</Text>
            <TextInput
              style={styles.input}
              value={name}
              onChangeText={setName}
              placeholder="Enter your name"
              placeholderTextColor="rgba(255,255,255,0.2)"
              maxLength={24}
              selectionColor={colors.violet}
            />
          </GlassCard>
        </Animated.View>

        {/* Persona preview */}
        <Animated.View entering={FadeInDown.delay(200).duration(500)} style={styles.section}>
          <GlassCard style={{ borderLeftWidth: 3, borderLeftColor: fColor }}>
            <Text style={[styles.personaName, { color: fColor }]}>{persona.name}</Text>
            <Badge label={persona.family} color={fColor} />
            <Text style={styles.personaTagline}>{persona.tagline}</Text>
          </GlassCard>
        </Animated.View>

        {/* Plan selection */}
        <Text style={styles.sectionTitle}>Choose Your Plan</Text>
        {PLANS.map((plan, i) => {
          const isSelected = selectedPlan === plan.id;
          return (
            <Animated.View key={plan.id} entering={FadeInDown.delay(300 + i * 100).duration(500)}>
              <TouchableOpacity activeOpacity={0.8} onPress={() => setSelectedPlan(plan.id)}>
                <GlassCard
                  style={[styles.planCard, isSelected && { borderColor: colors.violet, borderWidth: 1.5 }]}
                >
                  <View style={styles.planHeader}>
                    <Text style={styles.planName}>{plan.name}</Text>
                    <Text style={styles.planPrice}>{plan.price}</Text>
                  </View>
                  {plan.features.map((f) => (
                    <Text key={f} style={styles.planFeature}>• {f}</Text>
                  ))}
                </GlassCard>
              </TouchableOpacity>
            </Animated.View>
          );
        })}

        {/* Free option */}
        <TouchableOpacity
          onPress={() => setSelectedPlan("")}
          style={[styles.freeOption, !selectedPlan && styles.freeOptionActive]}
        >
          <Text style={[styles.freeText, !selectedPlan && { color: colors.violet }]}>
            Start Free (frozen mind)
          </Text>
        </TouchableOpacity>
      </ScrollView>

      <View style={styles.footer}>
        <Button title="Birth Your M³" onPress={onBirth} size="lg" />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#000000" },
  scroll: { paddingHorizontal: 16, paddingBottom: 100 },
  title: { fontSize: 28, fontFamily: "Saira_700Bold", color: "#fff", marginTop: 16, marginBottom: 20 },
  label: { fontSize: 12, fontFamily: "Inter_500Medium", color: "rgba(255,255,255,0.5)", marginBottom: 8 },
  input: {
    fontSize: 18, fontFamily: "Saira_500Medium", color: "#fff",
    borderBottomWidth: 1, borderBottomColor: "rgba(255,255,255,0.1)",
    paddingVertical: 8,
  },
  section: { marginTop: 16 },
  personaName: { fontSize: 18, fontFamily: "Saira_700Bold", marginBottom: 8 },
  personaTagline: { fontSize: 12, fontFamily: "Inter_400Regular", color: "rgba(255,255,255,0.5)", marginTop: 8 },
  sectionTitle: { fontSize: 17, fontFamily: "Saira_600SemiBold", color: "#fff", marginTop: 24, marginBottom: 12 },
  planCard: { marginBottom: 12, paddingVertical: 16 },
  planHeader: { flexDirection: "row", justifyContent: "space-between", marginBottom: 8 },
  planName: { fontSize: 16, fontFamily: "Saira_600SemiBold", color: "#fff" },
  planPrice: { fontSize: 16, fontFamily: "JetBrainsMono_500Medium", color: colors.violet },
  planFeature: { fontSize: 12, fontFamily: "Inter_400Regular", color: "rgba(255,255,255,0.5)", marginTop: 4 },
  freeOption: {
    paddingVertical: 14, alignItems: "center", marginTop: 8,
    borderRadius: 12, borderWidth: 1, borderColor: "rgba(255,255,255,0.08)",
  },
  freeOptionActive: { borderColor: colors.violet, backgroundColor: "rgba(139,92,246,0.1)" },
  freeText: { fontSize: 14, fontFamily: "Inter_500Medium", color: "rgba(255,255,255,0.4)" },
  footer: { paddingHorizontal: 16, paddingVertical: 16 },
});
