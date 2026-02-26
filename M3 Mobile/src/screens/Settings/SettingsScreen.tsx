/* -- Settings Screen -- Profile, Subscription, Language, Reset ----------------- */

import React, { useState } from "react";
import {
  View,
  Text,
  ScrollView,
  TextInput,
  TouchableOpacity,
  Alert,
  StyleSheet,
  Platform,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Animated, { FadeIn, FadeInDown } from "react-native-reanimated";
import { useTranslation } from "react-i18next";
import { useM3Store } from "../../stores/useM3Store";
import { useUserStore } from "../../stores/useUserStore";
import { personas } from "../../data/personas";
import { M3_TIERS, type TierDefinition } from "../../data/m3-stages";
import { GlassCard } from "../../components/ui/GlassCard";
import { Button } from "../../components/ui/Button";
import { Badge } from "../../components/ui/Badge";
import { colors, familyColors, fonts, spacing, radii } from "../../design/tokens";
import type { M3Tier } from "../../types/m3";

/* -- Tier ordering ---------------------------------------------------------- */

const TIER_ORDER: M3Tier[] = ["free", "basic", "premium", "ultimate"];

const TIER_LABELS: Record<M3Tier, string> = {
  free: "Free",
  basic: "Basic",
  premium: "Premium",
  ultimate: "Ultimate",
};

const TIER_PRICES: Record<M3Tier, string> = {
  free: "Free",
  basic: "$5/mo",
  premium: "$10/mo",
  ultimate: "$20/mo",
};

const TIER_FEATURES: Record<M3Tier, string[]> = {
  free: [
    "Birth your M3 persona",
    "View gene snapshot (frozen)",
    "Basic mind profile",
  ],
  basic: [
    "Weekly M3 updates",
    "Gene evolution tracking",
    "Mind observations",
  ],
  premium: [
    "Daily M3 updates",
    "Full C3 function access",
    "Predictive insights",
  ],
  ultimate: [
    "Real-time M3 evolution",
    "Cross-mind resonance",
    "Meta-awareness layer",
  ],
};

/* ========================================================================== */

export function SettingsScreen() {
  const { t, i18n } = useTranslation();

  /* -- Store state ---------------------------------------------------------- */

  const mind = useM3Store((s) => s.mind);
  const setTier = useM3Store((s) => s.setTier);
  const resetM3 = useM3Store((s) => s.resetM3);

  const displayName = useUserStore((s) => s.displayName);
  const setDisplayName = useUserStore((s) => s.setDisplayName);
  const level = useUserStore((s) => s.level);
  const joinedAt = useUserStore((s) => s.joinedAt);
  const resetStore = useUserStore((s) => s.resetStore);

  /* -- Local state for name editing ----------------------------------------- */

  const [editingName, setEditingName] = useState(false);
  const [nameValue, setNameValue] = useState(displayName || "You");

  /* -- Active persona ------------------------------------------------------- */

  const activePersona = mind
    ? personas.find((p) => p.id === mind.activePersonaId) ?? personas[0]
    : null;
  const fColor = activePersona
    ? familyColors[activePersona.family] ?? colors.violet
    : colors.violet;

  /* -- Current language ----------------------------------------------------- */

  const currentLang = i18n.language ?? "en";

  /* -- Format joined date --------------------------------------------------- */

  const memberSince = joinedAt
    ? new Date(joinedAt).toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      })
    : "---";

  /* -- Tier selection ------------------------------------------------------- */

  function onSelectTier(tier: M3Tier) {
    if (!mind) return;
    if (tier === mind.tier) return;
    setTier(tier);
  }

  /* -- Language switch ------------------------------------------------------- */

  function onChangeLang(lang: string) {
    i18n.changeLanguage(lang);
  }

  /* -- Name save ------------------------------------------------------------- */

  function onSaveName() {
    const trimmed = nameValue.trim();
    if (trimmed.length > 0) {
      setDisplayName(trimmed);
    }
    setEditingName(false);
  }

  /* -- Reset ---------------------------------------------------------------- */

  function onReset() {
    Alert.alert(
      "Reset Mind",
      "This will permanently erase your M3 mind and all progress. This cannot be undone.",
      [
        { text: "Cancel", style: "cancel" },
        {
          text: "Reset",
          style: "destructive",
          onPress: () => {
            resetM3();
            resetStore();
          },
        },
      ],
    );
  }

  /* -- Render --------------------------------------------------------------- */

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {/* Header */}
        <Animated.View entering={FadeIn.duration(600)} style={styles.header}>
          <Text style={styles.title}>Settings</Text>
        </Animated.View>

        {/* Profile Section */}
        <Animated.View
          entering={FadeInDown.duration(500).delay(100)}
          style={styles.section}
        >
          <Text style={styles.sectionTitle}>Profile</Text>
          <GlassCard>
            {/* Display Name */}
            <View style={styles.profileRow}>
              <Text style={styles.profileLabel}>Display Name</Text>
              {editingName ? (
                <View style={styles.nameEditRow}>
                  <TextInput
                    style={styles.nameInput}
                    value={nameValue}
                    onChangeText={setNameValue}
                    autoFocus
                    maxLength={24}
                    onSubmitEditing={onSaveName}
                    returnKeyType="done"
                    placeholderTextColor={colors.textTertiary}
                    selectionColor={colors.violet}
                  />
                  <TouchableOpacity onPress={onSaveName} activeOpacity={0.7}>
                    <Text style={styles.saveText}>Save</Text>
                  </TouchableOpacity>
                </View>
              ) : (
                <TouchableOpacity
                  onPress={() => {
                    setNameValue(displayName || "You");
                    setEditingName(true);
                  }}
                  activeOpacity={0.7}
                >
                  <Text style={styles.profileValue}>
                    {displayName || "You"}{" "}
                    <Text style={styles.editHint}>edit</Text>
                  </Text>
                </TouchableOpacity>
              )}
            </View>

            {/* Persona */}
            {activePersona && (
              <View style={styles.profileRow}>
                <Text style={styles.profileLabel}>Persona</Text>
                <View style={styles.personaRow}>
                  <Badge label={activePersona.name} color={fColor} />
                  <Text style={[styles.familyText, { color: fColor }]}>
                    {activePersona.family}
                  </Text>
                </View>
              </View>
            )}

            {/* Level & Stage */}
            {mind && (
              <View style={styles.profileRow}>
                <Text style={styles.profileLabel}>Mind</Text>
                <Text style={styles.profileValue}>
                  Level {mind.level} | {mind.stage}
                </Text>
              </View>
            )}

            {/* Member since */}
            <View style={[styles.profileRow, { borderBottomWidth: 0 }]}>
              <Text style={styles.profileLabel}>Member Since</Text>
              <Text style={styles.profileValue}>{memberSince}</Text>
            </View>
          </GlassCard>
        </Animated.View>

        {/* Subscription Section */}
        <Animated.View
          entering={FadeInDown.duration(500).delay(200)}
          style={styles.section}
        >
          <Text style={styles.sectionTitle}>Subscription</Text>

          {/* Current tier */}
          {mind && (
            <View style={styles.currentTierRow}>
              <Text style={styles.currentTierLabel}>Current:</Text>
              <Badge
                label={TIER_LABELS[mind.tier]}
                color={M3_TIERS[mind.tier].color}
              />
            </View>
          )}

          {/* Tier cards */}
          <View style={styles.tierGrid}>
            {TIER_ORDER.map((tierKey) => {
              const tier = M3_TIERS[tierKey];
              const isActive = mind?.tier === tierKey;
              const features = TIER_FEATURES[tierKey];

              return (
                <GlassCard
                  key={tierKey}
                  style={[
                    styles.tierCard,
                    isActive && {
                      borderWidth: 1.5,
                      borderColor: tier.color,
                    },
                  ]}
                >
                  {/* Tier header */}
                  <View style={styles.tierHeader}>
                    <Text style={[styles.tierName, { color: tier.color }]}>
                      {TIER_LABELS[tierKey]}
                    </Text>
                    <Text style={styles.tierPrice}>
                      {TIER_PRICES[tierKey]}
                    </Text>
                  </View>

                  {/* Features */}
                  {features.map((feat, i) => (
                    <View key={i} style={styles.featureRow}>
                      <View
                        style={[
                          styles.featureDot,
                          { backgroundColor: tier.color },
                        ]}
                      />
                      <Text style={styles.featureText}>{feat}</Text>
                    </View>
                  ))}

                  {/* Select button */}
                  <TouchableOpacity
                    style={[
                      styles.tierBtn,
                      isActive
                        ? { backgroundColor: `${tier.color}20` }
                        : { backgroundColor: "rgba(255,255,255,0.05)" },
                    ]}
                    onPress={() => onSelectTier(tierKey)}
                    disabled={isActive}
                    activeOpacity={0.7}
                  >
                    <Text
                      style={[
                        styles.tierBtnText,
                        { color: isActive ? tier.color : colors.textSecondary },
                      ]}
                    >
                      {isActive ? "Current" : "Select"}
                    </Text>
                  </TouchableOpacity>
                </GlassCard>
              );
            })}
          </View>
        </Animated.View>

        {/* Language Section */}
        <Animated.View
          entering={FadeInDown.duration(500).delay(300)}
          style={styles.section}
        >
          <Text style={styles.sectionTitle}>Language</Text>
          <GlassCard>
            <View style={styles.langRow}>
              <TouchableOpacity
                style={[
                  styles.langBtn,
                  currentLang === "en" && styles.langBtnActive,
                ]}
                onPress={() => onChangeLang("en")}
                activeOpacity={0.7}
              >
                <Text
                  style={[
                    styles.langBtnText,
                    currentLang === "en" && styles.langBtnTextActive,
                  ]}
                >
                  English
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[
                  styles.langBtn,
                  currentLang === "tr" && styles.langBtnActive,
                ]}
                onPress={() => onChangeLang("tr")}
                activeOpacity={0.7}
              >
                <Text
                  style={[
                    styles.langBtnText,
                    currentLang === "tr" && styles.langBtnTextActive,
                  ]}
                >
                  Turkce
                </Text>
              </TouchableOpacity>
            </View>
          </GlassCard>
        </Animated.View>

        {/* Danger Zone */}
        <Animated.View
          entering={FadeInDown.duration(500).delay(400)}
          style={styles.section}
        >
          <Text style={styles.sectionTitle}>Danger Zone</Text>
          <GlassCard
            style={{
              borderWidth: 1,
              borderColor: "rgba(239,68,68,0.3)",
            }}
          >
            <Text style={styles.dangerDescription}>
              Permanently erase your Musical Mind and all progress. This action
              cannot be undone.
            </Text>
            <TouchableOpacity
              style={styles.resetBtn}
              onPress={onReset}
              activeOpacity={0.7}
            >
              <Text style={styles.resetBtnText}>Reset Mind</Text>
            </TouchableOpacity>
          </GlassCard>
        </Animated.View>

        {/* App Info */}
        <Animated.View
          entering={FadeInDown.duration(500).delay(500)}
          style={styles.appInfo}
        >
          <Text style={styles.appVersion}>M3 Mobile v1.0.0</Text>
          <Text style={styles.appCredit}>SRC9 Musical Intelligence</Text>
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

  /* Sections */
  section: {
    paddingHorizontal: spacing.lg,
    marginTop: spacing.xl,
  },
  sectionTitle: {
    fontFamily: fonts.heading,
    fontSize: 17,
    color: colors.textPrimary,
    marginBottom: spacing.md,
  },

  /* Profile */
  profileRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: spacing.md,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: colors.border,
  },
  profileLabel: {
    fontFamily: fonts.body,
    fontSize: 14,
    color: colors.textSecondary,
  },
  profileValue: {
    fontFamily: fonts.bodySemiBold,
    fontSize: 14,
    color: colors.textPrimary,
  },
  editHint: {
    fontFamily: fonts.body,
    fontSize: 12,
    color: colors.violet,
  },
  personaRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
  },
  familyText: {
    fontFamily: fonts.body,
    fontSize: 12,
  },
  nameEditRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
  },
  nameInput: {
    fontFamily: fonts.bodySemiBold,
    fontSize: 14,
    color: colors.textPrimary,
    borderBottomWidth: 1,
    borderBottomColor: colors.violet,
    paddingVertical: 4,
    minWidth: 100,
  },
  saveText: {
    fontFamily: fonts.bodySemiBold,
    fontSize: 13,
    color: colors.violet,
  },

  /* Subscription */
  currentTierRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
    marginBottom: spacing.md,
  },
  currentTierLabel: {
    fontFamily: fonts.body,
    fontSize: 13,
    color: colors.textSecondary,
  },
  tierGrid: {
    gap: spacing.md,
  },
  tierCard: {
    paddingVertical: spacing.lg,
    paddingHorizontal: spacing.lg,
  },
  tierHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: spacing.md,
  },
  tierName: {
    fontFamily: fonts.heading,
    fontSize: 18,
  },
  tierPrice: {
    fontFamily: fonts.monoSemiBold,
    fontSize: 16,
    color: colors.textPrimary,
  },
  featureRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
    marginBottom: spacing.sm,
  },
  featureDot: {
    width: 5,
    height: 5,
    borderRadius: 2.5,
  },
  featureText: {
    fontFamily: fonts.body,
    fontSize: 13,
    color: colors.textSecondary,
  },
  tierBtn: {
    marginTop: spacing.md,
    paddingVertical: 10,
    borderRadius: radii.sm,
    alignItems: "center",
  },
  tierBtnText: {
    fontFamily: fonts.heading,
    fontSize: 14,
  },

  /* Language */
  langRow: {
    flexDirection: "row",
    gap: spacing.md,
  },
  langBtn: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: radii.sm,
    backgroundColor: "rgba(255,255,255,0.03)",
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.08)",
    alignItems: "center",
  },
  langBtnActive: {
    backgroundColor: "rgba(139,92,246,0.15)",
    borderColor: colors.violet,
  },
  langBtnText: {
    fontFamily: fonts.bodySemiBold,
    fontSize: 14,
    color: colors.textSecondary,
  },
  langBtnTextActive: {
    color: colors.violet,
  },

  /* Danger zone */
  dangerDescription: {
    fontFamily: fonts.body,
    fontSize: 13,
    color: colors.textSecondary,
    marginBottom: spacing.lg,
    lineHeight: 20,
  },
  resetBtn: {
    backgroundColor: "rgba(239,68,68,0.15)",
    paddingVertical: 12,
    borderRadius: radii.sm,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "rgba(239,68,68,0.3)",
  },
  resetBtnText: {
    fontFamily: fonts.heading,
    fontSize: 14,
    color: colors.danger,
  },

  /* App info */
  appInfo: {
    alignItems: "center",
    paddingVertical: spacing.xxxl,
  },
  appVersion: {
    fontFamily: fonts.mono,
    fontSize: 12,
    color: colors.textTertiary,
  },
  appCredit: {
    fontFamily: fonts.body,
    fontSize: 11,
    color: colors.textMuted,
    marginTop: 4,
  },
});
