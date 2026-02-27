import React, { useState } from "react";
import {
  View, Text, TextInput, ScrollView, TouchableOpacity, StyleSheet, Dimensions,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Animated, { FadeInDown } from "react-native-reanimated";
import { Ionicons } from "@expo/vector-icons";
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

const { width } = Dimensions.get("window");

export function NameEntryScreen() {
  const navigation = useNavigation<NativeStackNavigationProp<RootStackParamList>>();
  const selectedPersonaId = useOnboardingStore((s) => s.selectedPersonaId);
  const selectedTier = useOnboardingStore((s) => s.selectedTier);
  const birthM3 = useM3Store((s) => s.birthM3);
  const completeOnboarding = useUserStore((s) => s.completeOnboarding);

  const [name, setName] = useState("");

  const persona = personas.find((p) => p.id === selectedPersonaId) ?? personas[0];
  const fColor = familyColors[persona.family] ?? colors.violet;

  const hasPlan = selectedTier !== "free";

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
      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scroll}
        keyboardShouldPersistTaps="handled"
      >
        <Animated.View entering={FadeInDown.duration(500)}>
          <Text style={styles.title}>Name Your Mind</Text>
          <Text style={styles.subtitle}>
            Give your musical mind an identity
          </Text>
        </Animated.View>

        {/* Name input */}
        <Animated.View entering={FadeInDown.delay(100).duration(500)}>
          <GlassCard>
            <Text style={styles.label}>Display Name</Text>
            <TextInput
              style={styles.input}
              value={name}
              onChangeText={setName}
              placeholder="What shall we call you?"
              placeholderTextColor="rgba(255,255,255,0.2)"
              maxLength={24}
              selectionColor={colors.violet}
              autoCapitalize="words"
              returnKeyType="done"
            />
          </GlassCard>
        </Animated.View>

        {/* Persona preview */}
        <Animated.View entering={FadeInDown.delay(200).duration(500)} style={styles.section}>
          <GlassCard style={{ borderLeftWidth: 3, borderLeftColor: fColor }}>
            <View style={styles.personaRow}>
              <View style={[styles.personaAvatar, { backgroundColor: `${fColor}20`, borderColor: fColor }]}>
                <Text style={[styles.personaLetter, { color: fColor }]}>
                  {persona.name.charAt(0)}
                </Text>
              </View>
              <View style={styles.personaInfo}>
                <Text style={[styles.personaName, { color: fColor }]}>{persona.name}</Text>
                <Badge label={persona.family} color={fColor} />
              </View>
            </View>
            <Text style={styles.personaTagline}>"{persona.tagline}"</Text>
          </GlassCard>
        </Animated.View>

        {/* Subscription Section */}
        <Animated.View entering={FadeInDown.delay(300).duration(500)}>
          <Text style={styles.sectionTitle}>Subscription</Text>

          {/* Choose Plan Button */}
          <TouchableOpacity
            activeOpacity={0.8}
            onPress={() => navigation.navigate("Paywall")}
          >
            <GlassCard style={styles.planBtn}>
              <View style={styles.planBtnRow}>
                <View style={styles.planBtnLeft}>
                  <Ionicons name="diamond-outline" size={24} color={colors.violet} />
                  <View style={styles.planBtnText}>
                    <Text style={styles.planBtnTitle}>
                      {hasPlan ? `${selectedTier.charAt(0).toUpperCase() + selectedTier.slice(1)} Plan` : "Choose a Plan"}
                    </Text>
                    <Text style={styles.planBtnDesc}>
                      {hasPlan
                        ? "Tap to change your subscription"
                        : "Unlock your mind's full potential"}
                    </Text>
                  </View>
                </View>
                <Ionicons name="chevron-forward" size={20} color="rgba(255,255,255,0.3)" />
              </View>
            </GlassCard>
          </TouchableOpacity>

          {/* Free option */}
          {!hasPlan && (
            <Text style={styles.freeHint}>
              Or continue free with limited features
            </Text>
          )}
        </Animated.View>
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
  title: {
    fontSize: 28, fontFamily: "Saira_700Bold", color: "#fff", marginTop: 16,
  },
  subtitle: {
    fontSize: 14, fontFamily: "Inter_400Regular",
    color: "rgba(255,255,255,0.5)", marginTop: 6, marginBottom: 20,
  },
  label: {
    fontSize: 12, fontFamily: "Inter_500Medium",
    color: "rgba(255,255,255,0.5)", marginBottom: 8,
  },
  input: {
    fontSize: 18, fontFamily: "Saira_500Medium", color: "#fff",
    borderBottomWidth: 1, borderBottomColor: "rgba(255,255,255,0.1)",
    paddingVertical: 8,
  },
  section: { marginTop: 16 },
  personaRow: { flexDirection: "row", alignItems: "center", gap: 12 },
  personaAvatar: {
    width: 48, height: 48, borderRadius: 24,
    borderWidth: 1.5, alignItems: "center", justifyContent: "center",
  },
  personaLetter: { fontSize: 22, fontFamily: "Saira_700Bold" },
  personaInfo: { gap: 6 },
  personaName: { fontSize: 18, fontFamily: "Saira_700Bold" },
  personaTagline: {
    fontSize: 12, fontFamily: "Inter_400Regular",
    color: "rgba(255,255,255,0.4)", marginTop: 12, fontStyle: "italic",
  },
  sectionTitle: {
    fontSize: 17, fontFamily: "Saira_600SemiBold", color: "#fff",
    marginTop: 24, marginBottom: 12,
  },
  planBtn: { paddingVertical: 16 },
  planBtnRow: {
    flexDirection: "row", alignItems: "center", justifyContent: "space-between",
  },
  planBtnLeft: { flexDirection: "row", alignItems: "center", gap: 14, flex: 1 },
  planBtnText: { gap: 4, flex: 1 },
  planBtnTitle: { fontSize: 16, fontFamily: "Saira_600SemiBold", color: "#fff" },
  planBtnDesc: {
    fontSize: 12, fontFamily: "Inter_400Regular", color: "rgba(255,255,255,0.4)",
  },
  freeHint: {
    fontSize: 13, fontFamily: "Inter_400Regular",
    color: "rgba(255,255,255,0.3)", textAlign: "center", marginTop: 12,
  },
  footer: { paddingHorizontal: 16, paddingVertical: 16 },
});
