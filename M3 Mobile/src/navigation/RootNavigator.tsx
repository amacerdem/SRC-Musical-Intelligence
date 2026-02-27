import React from "react";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import type { RootStackParamList } from "./types";
import { useUserStore } from "../stores/useUserStore";
import { LandingScreen } from "../screens/Landing/LandingScreen";
import { OnboardingStack } from "./OnboardingStack";
import { MindRevealScreen } from "../screens/MindReveal/MindRevealScreen";
import { MainTabs } from "./MainTabs";
import { PaywallScreen } from "../screens/Paywall/PaywallScreen";

const Stack = createNativeStackNavigator<RootStackParamList>();

export function RootNavigator() {
  const hasCompleted = useUserStore((s) => s.hasCompletedOnboarding);

  return (
    <Stack.Navigator screenOptions={{ headerShown: false, animation: "fade" }}>
      {hasCompleted ? (
        <>
          <Stack.Screen name="MainTabs" component={MainTabs} />
          <Stack.Screen name="Paywall" component={PaywallScreen} options={{ presentation: "modal", animation: "slide_from_bottom" }} />
        </>
      ) : (
        <>
          <Stack.Screen name="Landing" component={LandingScreen} />
          <Stack.Screen name="Onboarding" component={OnboardingStack} />
          <Stack.Screen name="MindReveal" component={MindRevealScreen} />
        </>
      )}
    </Stack.Navigator>
  );
}
