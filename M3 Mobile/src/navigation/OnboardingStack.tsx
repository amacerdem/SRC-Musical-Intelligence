import React from "react";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import type { OnboardingStackParamList } from "./types";
import { PersonaSelectScreen } from "../screens/Onboarding/PersonaSelectScreen";
import { AxisCalibrationScreen } from "../screens/Onboarding/AxisCalibrationScreen";
import { ListeningImportScreen } from "../screens/Onboarding/ListeningImportScreen";
import { NameEntryScreen } from "../screens/Onboarding/NameEntryScreen";

const Stack = createNativeStackNavigator<OnboardingStackParamList>();

export function OnboardingStack() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false, animation: "slide_from_right" }}>
      <Stack.Screen name="PersonaSelect" component={PersonaSelectScreen} />
      <Stack.Screen name="AxisCalibration" component={AxisCalibrationScreen} />
      <Stack.Screen name="ListeningImport" component={ListeningImportScreen} />
      <Stack.Screen name="NameEntry" component={NameEntryScreen} />
    </Stack.Navigator>
  );
}
