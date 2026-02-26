/* -- Persona Detail Screen -- Full persona profile ----------------------------- */

import React, { useMemo } from "react";
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import {
  useRoute,
  useNavigation,
  type RouteProp,
} from "@react-navigation/native";
import Animated, {
  FadeIn,
  FadeInDown,
  FadeInUp,
} from "react-native-reanimated";
import type { InfoStackParamList } from "../../navigation/types";
import { personas } from "../../data/personas";
import type { Persona } from "../../types/mind";
import { GENE_NAMES, GENE_COLORS, type GeneName } from "../../types/m3";
import { GlassCard } from "../../components/ui/GlassCard";
import { Badge } from "../../components/ui/Badge";
import { Tag } from "../../components/ui/Tag";
import { ProgressBar } from "../../components/ui/ProgressBar";
import { colors, familyColors, fonts, spacing, radii } from "../../design/tokens";

const { width: SCREEN_WIDTH } = Dimensions.get("window");
const GENE_BAR_WIDTH = SCREEN_WIDTH - spacing.lg * 2 - 32 - 80;

/* -- Gene label formatting -------------------------------------------------- */

const GENE_LABELS: Record<GeneName, string> = {
  entropy: "Entropy",
  resolution: "Resolution",
  tension: "Tension",
  resonance: "Resonance",
  plasticity: "Plasticity",
};

/* ========================================================================== */

export function PersonaDetailScreen() {
  const route = useRoute<RouteProp<InfoStackParamList, "PersonaDetail">>();
  const navigation = useNavigation();
  const { personaId } = route.params;

  /* -- Find persona --------------------------------------------------------- */

  const persona = useMemo(
    () => personas.find((p) => p.id === personaId) ?? personas[0],
    [personaId],
  );

  const fColor = familyColors[persona.family] ?? colors.violet;

  /* -- Compatible personas -------------------------------------------------- */

  const compatibles = useMemo(
    () =>
      persona.compatibleWith
        .map((id) => personas.find((p) => p.id === id))
        .filter(Boolean) as Persona[],
    [persona],
  );

  /* -- Navigate to another persona ------------------------------------------ */

  function navigateToPersona(id: number) {
    (navigation as any).navigate("PersonaDetail", { personaId: id });
  }

  /* -- Render --------------------------------------------------------------- */

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {/* Back button */}
        <TouchableOpacity
          style={styles.backBtn}
          onPress={() => navigation.goBack()}
          activeOpacity={0.7}
        >
          <Text style={styles.backText}>{"<- Back"}</Text>
        </TouchableOpacity>

        {/* Header */}
        <Animated.View
          entering={FadeIn.duration(500)}
          style={styles.headerSection}
        >
          {/* Color accent strip */}
          <View style={[styles.accentStrip, { backgroundColor: fColor }]} />

          <Text style={styles.name}>{persona.name}</Text>

          <View style={styles.badgeRow}>
            <Badge label={persona.family} color={fColor} />
            <View style={styles.populationBadge}>
              <Text style={styles.populationText}>
                {persona.populationPct}%
              </Text>
            </View>
          </View>

          {/* Tagline */}
          <Text style={styles.tagline}>"{persona.tagline}"</Text>
        </Animated.View>

        {/* Gene Bars */}
        <Animated.View
          entering={FadeInDown.duration(500).delay(100)}
          style={styles.section}
        >
          <Text style={styles.sectionTitle}>Mind Genes</Text>
          <GlassCard>
            {GENE_NAMES.map((gene) => {
              const value = persona.genes[gene];
              const gColor = GENE_COLORS[gene];
              return (
                <View key={gene} style={styles.geneRow}>
                  <View style={styles.geneLabelCol}>
                    <View
                      style={[styles.geneDot, { backgroundColor: gColor }]}
                    />
                    <Text style={styles.geneLabel}>
                      {GENE_LABELS[gene]}
                    </Text>
                  </View>
                  <View style={styles.geneBarCol}>
                    <ProgressBar
                      progress={value}
                      color={gColor}
                      height={6}
                    />
                  </View>
                  <Text style={[styles.geneValue, { color: gColor }]}>
                    {(value * 100).toFixed(0)}
                  </Text>
                </View>
              );
            })}
          </GlassCard>
        </Animated.View>

        {/* Description */}
        <Animated.View
          entering={FadeInDown.duration(500).delay(200)}
          style={styles.section}
        >
          <Text style={styles.sectionTitle}>About</Text>
          <Text style={styles.description}>{persona.description}</Text>
        </Animated.View>

        {/* Strengths */}
        <Animated.View
          entering={FadeInDown.duration(500).delay(300)}
          style={styles.section}
        >
          <Text style={styles.sectionTitle}>Strengths</Text>
          <GlassCard>
            {persona.strengths.map((strength, i) => (
              <View key={i} style={styles.strengthRow}>
                <View
                  style={[styles.strengthDot, { backgroundColor: fColor }]}
                />
                <Text style={styles.strengthText}>{strength}</Text>
              </View>
            ))}
          </GlassCard>
        </Animated.View>

        {/* Compatible Personas */}
        {compatibles.length > 0 && (
          <Animated.View
            entering={FadeInDown.duration(500).delay(400)}
            style={styles.section}
          >
            <Text style={styles.sectionTitle}>Compatible Minds</Text>
            <ScrollView
              horizontal
              showsHorizontalScrollIndicator={false}
              contentContainerStyle={styles.compatRow}
            >
              {compatibles.map((cp) => {
                const cpColor = familyColors[cp.family] ?? colors.violet;
                return (
                  <TouchableOpacity
                    key={cp.id}
                    activeOpacity={0.7}
                    onPress={() => navigateToPersona(cp.id)}
                  >
                    <GlassCard
                      style={[
                        styles.compatCard,
                        {
                          borderLeftWidth: 2,
                          borderLeftColor: cpColor,
                        },
                      ]}
                    >
                      <Text
                        style={styles.compatName}
                        numberOfLines={1}
                      >
                        {cp.name}
                      </Text>
                      <Text
                        style={[styles.compatFamily, { color: cpColor }]}
                      >
                        {cp.family}
                      </Text>
                    </GlassCard>
                  </TouchableOpacity>
                );
              })}
            </ScrollView>
          </Animated.View>
        )}

        {/* Famous Minds */}
        <Animated.View
          entering={FadeInDown.duration(500).delay(500)}
          style={styles.section}
        >
          <Text style={styles.sectionTitle}>Famous Minds</Text>
          <View style={styles.tagRow}>
            {persona.famousMinds.map((name) => (
              <Tag key={name} label={name} color={fColor} />
            ))}
          </View>
        </Animated.View>

        {/* Persona color swatch */}
        <Animated.View
          entering={FadeInUp.duration(500).delay(600)}
          style={styles.section}
        >
          <GlassCard intensity="low" style={styles.colorSection}>
            <View style={styles.colorRow}>
              <View
                style={[
                  styles.colorSwatch,
                  { backgroundColor: persona.color },
                ]}
              />
              <View>
                <Text style={styles.colorLabel}>Persona Color</Text>
                <Text style={styles.colorHex}>{persona.color}</Text>
              </View>
            </View>
          </GlassCard>
        </Animated.View>
      </ScrollView>
    </SafeAreaView>
  );
}

/* -- Styles ---------------------------------------------------------------- */

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  scrollContent: {
    paddingBottom: 120,
  },

  /* Back button */
  backBtn: {
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
  },
  backText: {
    fontFamily: fonts.body,
    fontSize: 15,
    color: colors.violet,
  },

  /* Header */
  headerSection: {
    paddingHorizontal: spacing.lg,
    marginBottom: spacing.xl,
  },
  accentStrip: {
    width: 40,
    height: 4,
    borderRadius: 2,
    marginBottom: spacing.md,
  },
  name: {
    fontFamily: fonts.display,
    fontSize: 32,
    color: colors.textPrimary,
    marginBottom: spacing.sm,
  },
  badgeRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
    marginBottom: spacing.md,
  },
  populationBadge: {
    backgroundColor: "rgba(255,255,255,0.05)",
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  populationText: {
    fontFamily: fonts.mono,
    fontSize: 12,
    color: colors.textSecondary,
  },
  tagline: {
    fontFamily: fonts.body,
    fontSize: 16,
    color: colors.textSecondary,
    fontStyle: "italic",
  },

  /* Sections */
  section: {
    paddingHorizontal: spacing.lg,
    marginBottom: spacing.xl,
  },
  sectionTitle: {
    fontFamily: fonts.heading,
    fontSize: 17,
    color: colors.textPrimary,
    marginBottom: spacing.md,
  },

  /* Gene bars */
  geneRow: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: spacing.md,
  },
  geneLabelCol: {
    flexDirection: "row",
    alignItems: "center",
    width: 100,
    gap: 6,
  },
  geneDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  geneLabel: {
    fontFamily: fonts.body,
    fontSize: 12,
    color: colors.textSecondary,
  },
  geneBarCol: {
    flex: 1,
    marginHorizontal: spacing.sm,
  },
  geneValue: {
    fontFamily: fonts.monoSemiBold,
    fontSize: 13,
    width: 30,
    textAlign: "right",
  },

  /* Description */
  description: {
    fontFamily: fonts.body,
    fontSize: 15,
    color: "rgba(255,255,255,0.8)",
    lineHeight: 24,
  },

  /* Strengths */
  strengthRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
    marginBottom: spacing.md,
  },
  strengthDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
  },
  strengthText: {
    fontFamily: fonts.body,
    fontSize: 14,
    color: colors.textPrimary,
  },

  /* Compatible personas */
  compatRow: {
    gap: spacing.md,
    paddingRight: spacing.lg,
  },
  compatCard: {
    width: 140,
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.md,
  },
  compatName: {
    fontFamily: fonts.heading,
    fontSize: 13,
    color: colors.textPrimary,
    marginBottom: 4,
  },
  compatFamily: {
    fontFamily: fonts.body,
    fontSize: 11,
  },

  /* Tags */
  tagRow: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: spacing.sm,
  },

  /* Color section */
  colorSection: {
    paddingVertical: spacing.md,
  },
  colorRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.md,
  },
  colorSwatch: {
    width: 40,
    height: 40,
    borderRadius: radii.md,
  },
  colorLabel: {
    fontFamily: fonts.body,
    fontSize: 12,
    color: colors.textSecondary,
  },
  colorHex: {
    fontFamily: fonts.mono,
    fontSize: 13,
    color: colors.textPrimary,
    marginTop: 2,
  },
});
