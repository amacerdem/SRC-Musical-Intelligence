import React from "react";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import type { InfoStackParamList } from "./types";
import { InfoScreen } from "../screens/Info/InfoScreen";
import { PersonaDetailScreen } from "../screens/Info/PersonaDetailScreen";

const Stack = createNativeStackNavigator<InfoStackParamList>();

export function InfoStack() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="InfoList" component={InfoScreen} />
      <Stack.Screen name="PersonaDetail" component={PersonaDetailScreen} options={{ animation: "slide_from_right" }} />
    </Stack.Navigator>
  );
}
