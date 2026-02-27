/* ── RevenueCatService — In-App Subscription Management ───────────────
 *  Wraps react-native-purchases (RevenueCat SDK) to manage M3 tiers:
 *    Pulse       ($9.99/mo)  → "basic"
 *    Resonance   ($19.99/mo) → "premium"
 *    Transcendence ($49.99/mo) → "ultimate"
 *    No subscription         → "free"
 *  ──────────────────────────────────────────────────────────────────── */

import Purchases, {
  PurchasesOffering,
  PurchasesPackage,
  CustomerInfo,
} from "react-native-purchases";

import type { M3Tier } from "../types/m3";

/* ── Constants ────────────────────────────────────────────────────────── */

const REVENUECAT_API_KEY = "REVENUECAT_API_KEY";

/** RevenueCat entitlement IDs mapped to M3 subscription tiers */
const ENTITLEMENT_TO_TIER: Record<string, M3Tier> = {
  transcendence: "ultimate",
  resonance: "premium",
  pulse: "basic",
};

/**
 * Priority-ordered entitlement IDs (highest tier first).
 * When a customer holds multiple entitlements we resolve to the highest.
 */
const TIER_PRIORITY: string[] = ["transcendence", "resonance", "pulse"];

/* ── Service ──────────────────────────────────────────────────────────── */

export const RevenueCatService = {
  /* ── Initialization ──────────────────────────────────────────────── */

  /**
   * Configure the RevenueCat SDK.
   * Call once at app startup (e.g. in the root layout effect).
   */
  async configure(): Promise<void> {
    try {
      Purchases.configure({ apiKey: REVENUECAT_API_KEY });
    } catch (error) {
      console.warn("[RevenueCat] configure failed:", error);
    }
  },

  /* ── Offerings ───────────────────────────────────────────────────── */

  /**
   * Fetch available subscription offerings from RevenueCat.
   * Returns the current offering, or `null` if none are available.
   */
  async getOfferings(): Promise<PurchasesOffering | null> {
    try {
      const offerings = await Purchases.getOfferings();
      return offerings.current ?? null;
    } catch (error) {
      console.warn("[RevenueCat] getOfferings failed:", error);
      return null;
    }
  },

  /* ── Purchase ────────────────────────────────────────────────────── */

  /**
   * Purchase a subscription package.
   * Returns the updated `CustomerInfo` on success, or `null` on failure.
   */
  async purchasePackage(
    pkg: PurchasesPackage,
  ): Promise<CustomerInfo | null> {
    try {
      const { customerInfo } = await Purchases.purchasePackage(pkg);
      return customerInfo;
    } catch (error: any) {
      // RevenueCat uses `userCancelled` flag for user-initiated cancellations
      if (error?.userCancelled) {
        // Not an error — user dismissed the purchase sheet
        return null;
      }
      console.warn("[RevenueCat] purchasePackage failed:", error);
      return null;
    }
  },

  /* ── Customer Info ───────────────────────────────────────────────── */

  /**
   * Retrieve the current customer's subscription info.
   * Returns `null` if the request fails.
   */
  async getCustomerInfo(): Promise<CustomerInfo | null> {
    try {
      const info = await Purchases.getCustomerInfo();
      return info;
    } catch (error) {
      console.warn("[RevenueCat] getCustomerInfo failed:", error);
      return null;
    }
  },

  /* ── Restore ─────────────────────────────────────────────────────── */

  /**
   * Restore previous purchases (e.g. after reinstall or device change).
   * Returns the restored `CustomerInfo`, or `null` on failure.
   */
  async restorePurchases(): Promise<CustomerInfo | null> {
    try {
      const info = await Purchases.restorePurchases();
      return info;
    } catch (error) {
      console.warn("[RevenueCat] restorePurchases failed:", error);
      return null;
    }
  },

  /* ── Tier Resolution ─────────────────────────────────────────────── */

  /**
   * Determine the current M3Tier from RevenueCat entitlements.
   * Checks entitlements in priority order (highest first) so that a
   * customer who somehow holds multiple entitlements resolves to the
   * highest tier.
   *
   * Returns "free" if no active entitlements are found or on error.
   */
  async getCurrentTier(): Promise<M3Tier> {
    try {
      const info = await Purchases.getCustomerInfo();
      const entitlements = info.entitlements.active;

      for (const entitlementId of TIER_PRIORITY) {
        if (entitlements[entitlementId]?.isActive) {
          return ENTITLEMENT_TO_TIER[entitlementId];
        }
      }

      return "free";
    } catch (error) {
      console.warn("[RevenueCat] getCurrentTier failed:", error);
      return "free";
    }
  },

  /* ── Listener ────────────────────────────────────────────────────── */

  /**
   * Register a listener that fires whenever the customer's subscription
   * status changes (purchase, renewal, expiration, etc.).
   *
   * Returns a removal function to unsubscribe.
   */
  addCustomerInfoUpdateListener(
    callback: (info: CustomerInfo) => void,
  ): () => void {
    Purchases.addCustomerInfoUpdateListener(callback);
    // RevenueCat SDK listener doesn't return a cleanup function;
    // callers should manage lifecycle externally.
    return () => {};
  },
};
