import React from "react";
import { View, StyleSheet, type ViewProps } from "react-native";

interface GlassCardProps extends ViewProps {
  children: React.ReactNode;
  intensity?: "low" | "medium" | "high";
}

export function GlassCard({ children, intensity = "medium", style, ...props }: GlassCardProps) {
  const bgOpacity = intensity === "low" ? 0.03 : intensity === "high" ? 0.08 : 0.05;
  return (
    <View
      style={[
        styles.card,
        { backgroundColor: `rgba(255,255,255,${bgOpacity})` },
        style,
      ]}
      {...props}
    >
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    borderRadius: 16,
    borderWidth: StyleSheet.hairlineWidth,
    borderColor: "rgba(255,255,255,0.06)",
    padding: 16,
    overflow: "hidden",
  },
});
