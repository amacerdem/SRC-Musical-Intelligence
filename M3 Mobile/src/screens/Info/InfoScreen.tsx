/* -- Info Screen -- Persona Gallery / Mind Library ----------------------------- */

import React, { useState, useCallback, useMemo } from "react";
import {
  View,
  Text,
  FlatList,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useNavigation } from "@react-navigation/native";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";
import Animated, { FadeIn, FadeInDown } from "react-native-reanimated";
import type { InfoStackParamList } from "../../navigation/types";
import { personas } from "../../data/personas";
import type { Persona } from "../../types/mind";
import type { NeuralFamily } from "../../types/mind";
import { getDominantGene, GENE_NAMES, GENE_TO_TYPE } from "../../types/m3";
import { GlassCard } from "../../components/ui/GlassCard";
import { Badge } from "../../components/ui/Badge";
import { colors, familyColors, fonts, spacing, radii } from "../../design/tokens";

const { width: SCREEN_WIDTH } = Dimensions.get("window");
const CARD_GAP = 12;
const CARD_WIDTH = (SCREEN_WIDTH - spacing.lg * 2 - CARD_GAP) / 2;

type NavProp = NativeStackNavigationProp<InfoStackParamList, "InfoList">;

const FAMILIES: Array<"All" | NeuralFamily> = [
  "All",
  "Alchemists",
  "Architects",
  "Explorers",
  "Anchors",
  "Kineticists",
];

/* ========================================================================== */

export function InfoScreen() {
  const navigation = useNavigation<NavProp>();
  const [selectedFamily, setSelectedFamily] = useState<"All" | NeuralFamily>("All");

  /* -- Filtered personas ---------------------------------------------------- */

  const filtered = useMemo(() => {
    if (selectedFamily === "All") return personas;
    return personas.filter((p) => p.family === selectedFamily);
  }, [selectedFamily]);

  /* -- Chip color helper ---------------------------------------------------- */

  function chipColor(family: "All" | NeuralFamily): string {
    if (family === "All") return colors.violet;
    return familyColors[family] ?? colors.violet;
  }

  /* -- Navigate to persona detail ------------------------------------------- */

  const onCardPress = useCallback(
    (personaId: number) => {
      navigation.navigate("PersonaDetail", { personaId });
    },
    [navigation],
  );

  /* -- Render persona card -------------------------------------------------- */

  const renderCard = useCallback(
    ({ item, index }: { item: Persona; index: number }) => {
      const fColor = familyColors[item.family] ?? colors.violet;
      const dominantGene = getDominantGene(item.genes);

      return (
        <Animated.View
          entering={FadeInDown.duration(400).delay(index * 50)}
          style={styles.cardWrapper}
        >
          <TouchableOpacity
            activeOpacity={0.7}
            onPress={() => onCardPress(item.id)}
          >
            <GlassCard
              style={[
                styles.card,
                { borderLeftWidth: 3, borderLeftColor: fColor },
              ]}
            >
              {/* Name */}
              <Text style={styles.cardName} numberOfLines={1}>
                {item.name}
              </Text>

              {/* Family */}
              <Text style={[styles.cardFamily, { color: fColor }]}>
                {item.family}
              </Text>

              {/* Dominant gene */}
              <View style={styles.geneRow}>
                <View
                  style={[styles.geneDot, { backgroundColor: fColor }]}
                />
                <Text style={styles.geneText}>
                  {dominantGene.charAt(0).toUpperCase() + dominantGene.slice(1)}
                </Text>
              </View>

              {/* Population */}
              <Text style={styles.cardPopulation}>
                {item.populationPct}% of minds
              </Text>
            </GlassCard>
          </TouchableOpacity>
        </Animated.View>
      );
    },
    [onCardPress],
  );

  /* -- Key extractor -------------------------------------------------------- */

  const keyExtractor = useCallback((item: Persona) => String(item.id), []);

  /* -- Render --------------------------------------------------------------- */

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <Animated.View entering={FadeIn.duration(600)} style={styles.header}>
        <Text style={styles.title}>Mind Library</Text>
        <Text style={styles.subtitle}>
          {personas.length} neural personas
        </Text>
      </Animated.View>

      {/* Family filter chips */}
      <Animated.View entering={FadeIn.duration(600).delay(200)}>
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={styles.chipRow}
        >
          {FAMILIES.map((family) => {
            const isActive = selectedFamily === family;
            const color = chipColor(family);

            return (
              <TouchableOpacity
                key={family}
                activeOpacity={0.7}
                onPress={() => setSelectedFamily(family)}
                style={[
                  styles.chip,
                  isActive
                    ? { backgroundColor: `${color}25`, borderColor: color }
                    : { borderColor: "rgba(255,255,255,0.1)" },
                ]}
              >
                <Text
                  style={[
                    styles.chipText,
                    { color: isActive ? color : colors.textSecondary },
                  ]}
                >
                  {family}
                </Text>
              </TouchableOpacity>
            );
          })}
        </ScrollView>
      </Animated.View>

      {/* Persona grid */}
      <FlatList
        data={filtered}
        renderItem={renderCard}
        keyExtractor={keyExtractor}
        numColumns={2}
        columnWrapperStyle={styles.row}
        contentContainerStyle={styles.listContent}
        showsVerticalScrollIndicator={false}
      />
    </SafeAreaView>
  );
}

/* -- Styles ---------------------------------------------------------------- */

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.md,
    paddingBottom: spacing.sm,
  },
  title: {
    fontFamily: fonts.display,
    fontSize: 28,
    color: colors.textPrimary,
  },
  subtitle: {
    fontFamily: fonts.body,
    fontSize: 13,
    color: colors.textSecondary,
    marginTop: 2,
  },

  /* Chips */
  chipRow: {
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
    gap: spacing.sm,
  },
  chip: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: radii.full,
    borderWidth: 1,
  },
  chipText: {
    fontFamily: fonts.bodySemiBold,
    fontSize: 13,
  },

  /* Grid */
  listContent: {
    paddingHorizontal: spacing.lg,
    paddingBottom: 120,
  },
  row: {
    gap: CARD_GAP,
    marginBottom: CARD_GAP,
  },
  cardWrapper: {
    width: CARD_WIDTH,
  },
  card: {
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.md,
    minHeight: 120,
  },
  cardName: {
    fontFamily: fonts.heading,
    fontSize: 15,
    color: colors.textPrimary,
    marginBottom: 4,
  },
  cardFamily: {
    fontFamily: fonts.body,
    fontSize: 11,
    marginBottom: 8,
  },
  geneRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    marginBottom: 6,
  },
  geneDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
  },
  geneText: {
    fontFamily: fonts.mono,
    fontSize: 11,
    color: colors.textSecondary,
  },
  cardPopulation: {
    fontFamily: fonts.body,
    fontSize: 10,
    color: colors.textTertiary,
  },
});
