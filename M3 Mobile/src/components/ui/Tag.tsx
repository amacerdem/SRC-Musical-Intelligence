import React from "react";
import { View, Text, StyleSheet } from "react-native";

interface TagProps {
  label: string;
  color?: string;
  size?: "sm" | "md";
}

export function Tag({ label, color = "rgba(255,255,255,0.6)", size = "md" }: TagProps) {
  return (
    <View style={[styles.tag, size === "sm" && styles.tagSm]}>
      <Text style={[styles.label, { color }, size === "sm" && styles.labelSm]}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  tag: {
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 6,
    backgroundColor: "rgba(255,255,255,0.05)",
    borderWidth: StyleSheet.hairlineWidth,
    borderColor: "rgba(255,255,255,0.1)",
    alignSelf: "flex-start",
  },
  tagSm: {
    paddingHorizontal: 8,
    paddingVertical: 3,
  },
  label: {
    fontSize: 12,
    fontFamily: "Inter_500Medium",
  },
  labelSm: {
    fontSize: 10,
  },
});
