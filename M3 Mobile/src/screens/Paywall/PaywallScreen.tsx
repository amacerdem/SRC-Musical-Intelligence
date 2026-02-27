/* -- PaywallScreen -- Full-page subscription plan selector -------------------
 *  3 tiers: Pulse ($9.99), Resonance ($19.99, recommended), Transcendence ($49.99)
 *  RevenueCat integration for purchases & restore.
 *  -------------------------------------------------------------------------- */

import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  Alert,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Animated, { FadeInDown } from "react-native-reanimated";
import { Ionicons } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";
import type { PurchasesPackage } from "react-native-purchases";
import { RevenueCatService } from "../../services/RevenueCatService";
import { useM3Store } from "../../stores/useM3Store";
import { colors, fonts, spacing } from "../../design/tokens";

/* -- Plan Definitions ------------------------------------------------------- */

interface PlanFeature {
  label: string;
}

interface Plan {
  id: string;
  name: string;
  tier: "basic" | "premium" | "ultimate";
  price: string;
  color: string;
  recommended: boolean;
  features: PlanFeature[];
}

const PLANS: Plan[] = [
  {
    id: "pulse",
    name: "Pulse",
    tier: "basic",
    price: "$9.99/mo",
    color: "#818CF8",
    recommended: false,
    features: [
      { label: "Mind Growth" },
      { label: "Weekly Playlist" },
      { label: "Basic Visualizer" },
    ],
  },
  {
    id: "resonance",
    name: "Resonance",
    tier: "premium",
    price: "$19.99/mo",
    color: "#8B5CF6",
    recommended: true,
    features: [
      { label: "All Pulse features" },
      { label: "Live Resonance" },
      { label: "Mind Garden" },
      { label: "Social" },
    ],
  },
  {
    id: "transcendence",
    name: "Transcendence",
    tier: "ultimate",
    price: "$49.99/mo",
    color: "#FBBF24",
    recommended: false,
    features: [
      { label: "All Resonance features" },
      { label: "Echo Layer" },
      { label: "Advanced Analytics" },
      { label: "Priority" },
    ],
  },
];

/* ========================================================================== */

export function PaywallScreen() {
  const navigation = useNavigation();

  const [loading, setLoading] = useState(true);
  const [purchasing, setPurchasing] = useState<string | null>(null);
  const [restoring, setRestoring] = useState(false);
  const [packages, setPackages] = useState<PurchasesPackage[] | null>(null);

  /* -- Fetch offerings on mount --------------------------------------------- */

  useEffect(() => {
    async function fetchOfferings() {
      try {
        const offering = await RevenueCatService.getOfferings();
        setPackages(offering?.availablePackages ?? null);
      } catch (err) {
        console.warn("[Paywall] Failed to fetch offerings:", err);
        Alert.alert(
          "Connection Error",
          "Unable to load subscription plans. Please check your connection and try again.",
          [{ text: "OK", onPress: () => navigation.goBack() }],
        );
      } finally {
        setLoading(false);
      }
    }

    fetchOfferings();
  }, [navigation]);

  /* -- Purchase handler ----------------------------------------------------- */

  async function handlePurchase(plan: Plan) {
    if (purchasing) return;

    // Find the matching package from RevenueCat offerings
    const pkg = packages?.find(
      (p) =>
        p.identifier?.toLowerCase().includes(plan.id) ||
        p.product?.identifier?.toLowerCase().includes(plan.id),
    );

    if (!pkg) {
      Alert.alert(
        "Plan Unavailable",
        "This subscription plan is not available right now. Please try again later.",
      );
      return;
    }

    setPurchasing(plan.id);

    try {
      await RevenueCatService.purchasePackage(pkg);

      // Fetch the current tier after successful purchase
      const tier = await RevenueCatService.getCurrentTier();

      // Update M3 store if setTier is available
      const store = useM3Store.getState();
      if (typeof store.setTier === "function") {
        store.setTier(plan.tier);
      } else {
        console.log("[Paywall] setTier not available on store, tier:", tier);
      }

      Alert.alert(
        "Welcome to " + plan.name,
        "Your subscription is now active. Enjoy your evolution.",
        [{ text: "Let's Go", onPress: () => navigation.goBack() }],
      );
    } catch (err: any) {
      // User cancelled -- not an error
      if (err?.userCancelled) return;

      console.error("[Paywall] Purchase failed:", err);
      Alert.alert(
        "Purchase Failed",
        "Something went wrong with your purchase. You have not been charged. Please try again.",
      );
    } finally {
      setPurchasing(null);
    }
  }

  /* -- Restore handler ------------------------------------------------------ */

  async function handleRestore() {
    if (restoring) return;
    setRestoring(true);

    try {
      await RevenueCatService.restorePurchases();

      const tier = await RevenueCatService.getCurrentTier();

      const store = useM3Store.getState();
      if (typeof store.setTier === "function" && tier) {
        store.setTier(tier);
      }

      Alert.alert(
        "Purchases Restored",
        "Your previous purchases have been restored successfully.",
        [{ text: "OK", onPress: () => navigation.goBack() }],
      );
    } catch (err) {
      console.error("[Paywall] Restore failed:", err);
      Alert.alert(
        "Restore Failed",
        "Unable to restore purchases. Please make sure you are signed in with the correct Apple ID.",
      );
    } finally {
      setRestoring(false);
    }
  }

  /* -- Loading state -------------------------------------------------------- */

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={colors.violet} />
          <Text style={styles.loadingText}>Loading plans...</Text>
        </View>
      </SafeAreaView>
    );
  }

  /* -- Main Render ---------------------------------------------------------- */

  return (
    <SafeAreaView style={styles.container}>
      {/* Close Button */}
      <TouchableOpacity
        style={styles.closeButton}
        onPress={() => navigation.goBack()}
        activeOpacity={0.7}
      >
        <Ionicons name="close" size={28} color={colors.textSecondary} />
      </TouchableOpacity>

      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {/* Header */}
        <Animated.View
          entering={FadeInDown.duration(500).delay(0)}
          style={styles.header}
        >
          <Text style={styles.title}>Unlock Your Mind</Text>
          <Text style={styles.subtitle}>Choose your evolution path</Text>
        </Animated.View>

        {/* Plan Cards */}
        {PLANS.map((plan, index) => {
          const isActive = purchasing === plan.id;
          const isDisabled = purchasing !== null && !isActive;

          return (
            <Animated.View
              key={plan.id}
              entering={FadeInDown.duration(500).delay(100 + index * 120)}
            >
              <View
                style={[
                  styles.planCard,
                  {
                    borderColor: plan.recommended
                      ? plan.color
                      : colors.border,
                    borderWidth: plan.recommended ? 1.5 : 1,
                  },
                ]}
              >
                {/* Recommended Badge */}
                {plan.recommended && (
                  <View
                    style={[
                      styles.recommendedBadge,
                      { backgroundColor: plan.color },
                    ]}
                  >
                    <Ionicons
                      name="star"
                      size={10}
                      color="#000000"
                      style={styles.recommendedIcon}
                    />
                    <Text style={styles.recommendedText}>RECOMMENDED</Text>
                  </View>
                )}

                {/* Plan Header */}
                <View style={styles.planHeader}>
                  <View>
                    <Text style={[styles.planName, { color: plan.color }]}>
                      {plan.name}
                    </Text>
                    <Text style={styles.planPrice}>{plan.price}</Text>
                  </View>
                </View>

                {/* Features */}
                <View style={styles.featureList}>
                  {plan.features.map((feature, i) => (
                    <View key={i} style={styles.featureRow}>
                      <Ionicons
                        name="checkmark-circle"
                        size={18}
                        color={plan.color}
                      />
                      <Text style={styles.featureText}>{feature.label}</Text>
                    </View>
                  ))}
                </View>

                {/* Subscribe Button */}
                <TouchableOpacity
                  style={[
                    styles.subscribeButton,
                    plan.recommended
                      ? { backgroundColor: plan.color }
                      : {
                          backgroundColor: "transparent",
                          borderWidth: 1,
                          borderColor: plan.color,
                        },
                    isDisabled && styles.subscribeButtonDisabled,
                  ]}
                  onPress={() => handlePurchase(plan)}
                  disabled={isDisabled}
                  activeOpacity={0.7}
                >
                  {isActive ? (
                    <ActivityIndicator
                      size="small"
                      color={plan.recommended ? "#000000" : plan.color}
                    />
                  ) : (
                    <Text
                      style={[
                        styles.subscribeButtonText,
                        {
                          color: plan.recommended ? "#000000" : plan.color,
                        },
                      ]}
                    >
                      Subscribe
                    </Text>
                  )}
                </TouchableOpacity>
              </View>
            </Animated.View>
          );
        })}

        {/* Restore Purchases */}
        <Animated.View
          entering={FadeInDown.duration(500).delay(500)}
          style={styles.restoreContainer}
        >
          <TouchableOpacity
            onPress={handleRestore}
            disabled={restoring}
            activeOpacity={0.7}
          >
            {restoring ? (
              <ActivityIndicator size="small" color={colors.textTertiary} />
            ) : (
              <Text style={styles.restoreText}>Restore Purchases</Text>
            )}
          </TouchableOpacity>
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
    paddingHorizontal: spacing.lg,
    paddingBottom: 120,
  },

  /* Loading */
  loadingContainer: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    gap: spacing.lg,
  },
  loadingText: {
    fontFamily: fonts.body,
    fontSize: 14,
    color: colors.textSecondary,
  },

  /* Close Button */
  closeButton: {
    position: "absolute",
    top: 60,
    right: spacing.lg,
    zIndex: 10,
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: colors.surfaceMedium,
    alignItems: "center",
    justifyContent: "center",
  },

  /* Header */
  header: {
    alignItems: "center",
    paddingTop: spacing.xxxl,
    paddingBottom: spacing.xxl,
  },
  title: {
    fontFamily: fonts.display,
    fontSize: 32,
    color: colors.textPrimary,
    letterSpacing: 0.5,
    textAlign: "center",
  },
  subtitle: {
    fontFamily: fonts.body,
    fontSize: 16,
    color: colors.textSecondary,
    marginTop: spacing.sm,
    textAlign: "center",
  },

  /* Plan Card */
  planCard: {
    backgroundColor: colors.surface,
    borderRadius: 16,
    padding: spacing.xl,
    marginBottom: spacing.lg,
    overflow: "hidden",
  },

  /* Recommended Badge */
  recommendedBadge: {
    position: "absolute",
    top: 0,
    right: 0,
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: spacing.xs,
    paddingHorizontal: spacing.md,
    borderBottomLeftRadius: 12,
  },
  recommendedIcon: {
    marginRight: 4,
  },
  recommendedText: {
    fontFamily: fonts.bodySemiBold,
    fontSize: 10,
    color: "#000000",
    letterSpacing: 1,
  },

  /* Plan Header */
  planHeader: {
    marginBottom: spacing.lg,
  },
  planName: {
    fontFamily: fonts.display,
    fontSize: 24,
    letterSpacing: 0.3,
  },
  planPrice: {
    fontFamily: fonts.monoSemiBold,
    fontSize: 18,
    color: colors.textPrimary,
    marginTop: spacing.xs,
  },

  /* Features */
  featureList: {
    gap: spacing.md,
    marginBottom: spacing.xl,
  },
  featureRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
  },
  featureText: {
    fontFamily: fonts.body,
    fontSize: 14,
    color: colors.textSecondary,
  },

  /* Subscribe Button */
  subscribeButton: {
    height: 48,
    borderRadius: 12,
    alignItems: "center",
    justifyContent: "center",
  },
  subscribeButtonDisabled: {
    opacity: 0.4,
  },
  subscribeButtonText: {
    fontFamily: fonts.heading,
    fontSize: 16,
    letterSpacing: 0.3,
  },

  /* Restore */
  restoreContainer: {
    alignItems: "center",
    paddingVertical: spacing.xl,
  },
  restoreText: {
    fontFamily: fonts.body,
    fontSize: 14,
    color: colors.textTertiary,
    textDecorationLine: "underline",
  },
});
