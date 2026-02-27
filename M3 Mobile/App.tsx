import React, { useCallback, useEffect } from "react";
import { View, Text, StyleSheet, Platform } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { StatusBar } from "expo-status-bar";
import * as SplashScreen from "expo-splash-screen";
import { registerRootComponent } from "expo";
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

// Initialize RevenueCat on app startup (skip on web if API key is mobile-only)
if (Platform.OS !== "web") {
  RevenueCatService.configure();
}

if (Platform.OS !== "web") {
  SplashScreen.preventAutoHideAsync();
}

/* ── Error Boundary (catches render crashes and shows the error on screen) ── */
class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { error: Error | null }
> {
  state = { error: null as Error | null };
  static getDerivedStateFromError(error: Error) {
    return { error };
  }
  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error("[M3] Render crash:", error, info.componentStack);
  }
  render() {
    if (this.state.error) {
      return (
        <View style={{ flex: 1, backgroundColor: "#000", justifyContent: "center", padding: 24 }}>
          <Text style={{ color: "#EF4444", fontSize: 18, fontWeight: "bold", marginBottom: 12 }}>
            M3 Render Error
          </Text>
          <Text style={{ color: "#FFF", fontSize: 13, fontFamily: "monospace" }}>
            {this.state.error.message}
          </Text>
          <Text style={{ color: "rgba(255,255,255,0.5)", fontSize: 11, fontFamily: "monospace", marginTop: 8 }}>
            {this.state.error.stack?.slice(0, 600)}
          </Text>
        </View>
      );
    }
    return this.props.children;
  }
}

function App() {
  const [fontsLoaded, fontError] = useFonts({
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
    if (fontsLoaded && Platform.OS !== "web") {
      await SplashScreen.hideAsync();
    }
  }, [fontsLoaded]);

  useEffect(() => {
    if (fontError) {
      console.warn("[M3] Font loading error:", fontError);
    }
  }, [fontError]);

  if (!fontsLoaded && !fontError && Platform.OS !== "web") return null;

  return (
    <ErrorBoundary>
      <GestureHandlerRootView style={styles.root}>
        <View style={styles.root} onLayout={onLayoutRootView}>
          <NavigationContainer theme={M3DarkTheme}>
            <RootNavigator />
          </NavigationContainer>
          <StatusBar style="light" />
        </View>
      </GestureHandlerRootView>
    </ErrorBoundary>
  );
}

export default App;
registerRootComponent(App);

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: "#000000" },
});
