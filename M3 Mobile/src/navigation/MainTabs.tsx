import React from "react";
import { View, Text, StyleSheet, Platform } from "react-native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { BlurView } from "expo-blur";
import type { MainTabParamList } from "./types";
import { M3HubScreen } from "../screens/M3Hub/M3HubScreen";
import { DashboardScreen } from "../screens/Dashboard/DashboardScreen";
import { LiveScreen } from "../screens/Live/LiveScreen";
import { InfoStack } from "./InfoStack";
import { SettingsScreen } from "../screens/Settings/SettingsScreen";
import { colors } from "../design/tokens";

const Tab = createBottomTabNavigator<MainTabParamList>();

// Simple icon components (circles with letters as placeholders)
function TabIcon({ label, focused }: { label: string; focused: boolean }) {
  return (
    <View style={[styles.iconContainer, focused && styles.iconFocused]}>
      <Text style={[styles.iconText, focused && styles.iconTextFocused]}>
        {label[0]}
      </Text>
    </View>
  );
}

export function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarStyle: {
          position: "absolute",
          backgroundColor: "rgba(0,0,0,0.85)",
          borderTopColor: colors.border,
          borderTopWidth: StyleSheet.hairlineWidth,
          height: Platform.OS === "ios" ? 88 : 68,
          paddingBottom: Platform.OS === "ios" ? 28 : 8,
          paddingTop: 8,
        },
        tabBarActiveTintColor: colors.violet,
        tabBarInactiveTintColor: colors.textMuted,
        tabBarLabelStyle: {
          fontFamily: "Inter_500Medium",
          fontSize: 10,
        },
      }}
    >
      <Tab.Screen
        name="Mind"
        component={M3HubScreen}
        options={{
          tabBarIcon: ({ focused }) => <TabIcon label="Mind" focused={focused} />,
        }}
      />
      <Tab.Screen
        name="Discover"
        component={DashboardScreen}
        options={{
          tabBarIcon: ({ focused }) => <TabIcon label="Discover" focused={focused} />,
        }}
      />
      <Tab.Screen
        name="Live"
        component={LiveScreen}
        options={{
          tabBarIcon: ({ focused }) => <TabIcon label="Live" focused={focused} />,
        }}
      />
      <Tab.Screen
        name="Library"
        component={InfoStack}
        options={{
          tabBarIcon: ({ focused }) => <TabIcon label="Library" focused={focused} />,
        }}
      />
      <Tab.Screen
        name="Settings"
        component={SettingsScreen}
        options={{
          tabBarIcon: ({ focused }) => <TabIcon label="Settings" focused={focused} />,
        }}
      />
    </Tab.Navigator>
  );
}

const styles = StyleSheet.create({
  iconContainer: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: "rgba(255,255,255,0.05)",
    alignItems: "center",
    justifyContent: "center",
  },
  iconFocused: {
    backgroundColor: "rgba(139,92,246,0.2)",
  },
  iconText: {
    fontSize: 14,
    fontFamily: "Saira_600SemiBold",
    color: "rgba(255,255,255,0.35)",
  },
  iconTextFocused: {
    color: "#8B5CF6",
  },
});
