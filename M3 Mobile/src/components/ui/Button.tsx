import React from "react";
import { TouchableOpacity, Text, StyleSheet, type ViewStyle } from "react-native";
import { LinearGradient } from "expo-linear-gradient";

interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md" | "lg";
  disabled?: boolean;
  style?: ViewStyle;
}

export function Button({ title, onPress, variant = "primary", size = "md", disabled, style }: ButtonProps) {
  const height = size === "sm" ? 36 : size === "lg" ? 56 : 44;
  const fontSize = size === "sm" ? 13 : size === "lg" ? 17 : 15;
  const paddingHorizontal = size === "sm" ? 16 : size === "lg" ? 32 : 24;

  if (variant === "primary") {
    return (
      <TouchableOpacity onPress={onPress} disabled={disabled} activeOpacity={0.8} style={style}>
        <LinearGradient
          colors={["#818CF8", "#A78BFA", "#F472B6"]}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 0 }}
          style={[styles.base, { height, paddingHorizontal, opacity: disabled ? 0.5 : 1 }]}
        >
          <Text style={[styles.text, { fontSize }]}>{title}</Text>
        </LinearGradient>
      </TouchableOpacity>
    );
  }

  return (
    <TouchableOpacity
      onPress={onPress}
      disabled={disabled}
      activeOpacity={0.7}
      style={[
        styles.base,
        variant === "secondary" ? styles.secondary : styles.ghost,
        { height, paddingHorizontal, opacity: disabled ? 0.5 : 1 },
        style,
      ]}
    >
      <Text style={[styles.text, { fontSize }, variant === "ghost" && styles.ghostText]}>
        {title}
      </Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  base: {
    borderRadius: 12,
    alignItems: "center",
    justifyContent: "center",
  },
  secondary: {
    backgroundColor: "rgba(255,255,255,0.05)",
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.1)",
  },
  ghost: {
    backgroundColor: "transparent",
  },
  text: {
    color: "#FFFFFF",
    fontFamily: "Saira_600SemiBold",
    letterSpacing: 0.5,
  },
  ghostText: {
    color: "rgba(255,255,255,0.6)",
  },
});
