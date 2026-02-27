import React, { useCallback } from "react";
import { View, StyleSheet } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { StatusBar } from "expo-status-bar";
import * as SplashScreen from "expo-splash-screen";
import {
  useFonts,
  Saira_400Regular,
  Saira_500Medium,
  Saira_600SemiBold,
  Saira_700Bold,
} from "@expo-google-fonts/saira";
import {
  Inter_400Regular,
  Inter_500Medium,
  Inter_600SemiBold,
  Inter_700Bold,
} from "@expo-google-fonts/inter";
import {
  JetBrainsMono_400Regular,
  JetBrainsMono_500Medium,
} from "@expo-google-fonts/jetbrains-mono";

import { RootNavigator } from "./src/navigation/RootNavigator";
import { M3DarkTheme } from "./src/design/theme";
import { RevenueCatService } from "./src/services/RevenueCatService";
import "./src/i18n";

// Initialize RevenueCat on app startup
RevenueCatService.configure();

SplashScreen.preventAutoHideAsync();

export default function App() {
  const [fontsLoaded] = useFonts({
    Saira_400Regular,
    Saira_500Medium,
    Saira_600SemiBold,
    Saira_700Bold,
    Inter_400Regular,
    Inter_500Medium,
    Inter_600SemiBold,
    Inter_700Bold,
    JetBrainsMono_400Regular,
    JetBrainsMono_500Medium,
  });

  const onLayoutRootView = useCallback(async () => {
    if (fontsLoaded) {
      await SplashScreen.hideAsync();
    }
  }, [fontsLoaded]);

  if (!fontsLoaded) return null;

  return (
    <GestureHandlerRootView style={styles.root}>
      <View style={styles.root} onLayout={onLayoutRootView}>
        <NavigationContainer theme={M3DarkTheme}>
          <RootNavigator />
        </NavigationContainer>
        <StatusBar style="light" />
      </View>
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: "#000000" },
});
