import React, { useState, useCallback } from "react";
import {
  View, Text, FlatList, ScrollView, TouchableOpacity, StyleSheet, Dimensions,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Animated, { FadeInDown } from "react-native-reanimated";
import { useNavigation } from "@react-navigation/native";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";
import type { OnboardingStackParamList } from "../../navigation/types";
import { useOnboardingStore } from "../../stores/useOnboardingStore";
import { personas } from "../../data/personas";
import type { Persona, NeuralFamily } from "../../types/mind";
import { GlassCard } from "../../components/ui/GlassCard";
import { Button } from "../../components/ui/Button";
import { Badge } from "../../components/ui/Badge";
import { colors, familyColors } from "../../design/tokens";

const { width } = Dimensions.get("window");
const CARD_WIDTH = (width - 56) / 2;

const FAMILIES: (NeuralFamily | "All")[] = [
  "All", "Alchemists", "Architects", "Explorers", "Anchors", "Kineticists",
];

export function PersonaSelectScreen() {
  const nav = useNavigation<NativeStackNavigationProp<OnboardingStackParamList>>();
  const selectedId = useOnboardingStore((s) => s.selectedPersonaId);
  const setPersona = useOnboardingStore((s) => s.setPersona);
  const [filter, setFilter] = useState<NeuralFamily | "All">("All");

  const filtered = filter === "All"
    ? personas
    : personas.filter((p) => p.family === filter);

  const renderCard = useCallback(({ item }: { item: Persona }) => {
    const isSelected = item.id === selectedId;
    const fColor = familyColors[item.family] ?? colors.violet;
    return (
      <TouchableOpacity
        activeOpacity={0.8}
        onPress={() => setPersona(item.id)}
        style={[styles.cardWrap, { width: CARD_WIDTH }]}
      >
        <GlassCard
          style={[
            styles.card,
            { borderLeftColor: fColor, borderLeftWidth: 3 },
            isSelected && { borderColor: fColor, borderWidth: 1.5 },
          ]}
        >
          <Text style={[styles.personaName, isSelected && { color: fColor }]}>
            {item.name}
          </Text>
          <Text style={styles.tagline} numberOfLines={2}>{item.tagline}</Text>
          <Badge label={item.family} color={fColor} />
        </GlassCard>
      </TouchableOpacity>
    );
  }, [selectedId]);

  return (
    <SafeAreaView style={styles.container}>
      <Animated.View entering={FadeInDown.duration(500)}>
        <Text style={styles.title}>Choose Your Persona</Text>
        <Text style={styles.subtitle}>
          24 personas across 5 neural families. Which resonates with you?
        </Text>
      </Animated.View>

      {/* Family filter chips */}
      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.chipRow}>
        {FAMILIES.map((f) => {
          const isActive = f === filter;
          const chipColor = f === "All" ? colors.violet : (familyColors[f] ?? colors.violet);
          return (
            <TouchableOpacity
              key={f}
              style={[
                styles.chip,
                isActive && { backgroundColor: `${chipColor}20`, borderColor: chipColor },
              ]}
              onPress={() => setFilter(f)}
            >
              <Text style={[styles.chipText, isActive && { color: chipColor }]}>{f}</Text>
            </TouchableOpacity>
          );
        })}
      </ScrollView>

      {/* Persona grid */}
      <FlatList
        data={filtered}
        renderItem={renderCard}
        keyExtractor={(p) => String(p.id)}
        numColumns={2}
        columnWrapperStyle={styles.gridRow}
        contentContainerStyle={styles.gridContent}
        showsVerticalScrollIndicator={false}
      />

      {/* Continue button */}
      <View style={styles.footer}>
        <Button
          title="Continue"
          onPress={() => nav.navigate("AxisCalibration")}
          disabled={selectedId === null}
          size="lg"
        />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#000000", paddingHorizontal: 16 },
  title: { fontSize: 28, fontFamily: "Saira_700Bold", color: "#fff", marginTop: 16 },
  subtitle: { fontSize: 14, fontFamily: "Inter_400Regular", color: "rgba(255,255,255,0.5)", marginTop: 8, marginBottom: 16 },
  chipRow: { flexGrow: 0, marginBottom: 16 },
  chip: {
    paddingHorizontal: 14, paddingVertical: 7, borderRadius: 20,
    backgroundColor: "rgba(255,255,255,0.04)", borderWidth: 1,
    borderColor: "rgba(255,255,255,0.08)", marginRight: 8,
  },
  chipText: { fontSize: 12, fontFamily: "Inter_500Medium", color: "rgba(255,255,255,0.5)" },
  gridRow: { justifyContent: "space-between", marginBottom: 12 },
  gridContent: { paddingBottom: 100 },
  cardWrap: {},
  card: { paddingVertical: 14, paddingHorizontal: 12, gap: 8 },
  personaName: { fontSize: 14, fontFamily: "Saira_600SemiBold", color: "#fff" },
  tagline: { fontSize: 11, fontFamily: "Inter_400Regular", color: "rgba(255,255,255,0.4)", lineHeight: 16 },
  footer: { paddingVertical: 16 },
});
