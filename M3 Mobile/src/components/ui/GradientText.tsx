import React from "react";
import { Text, type TextStyle } from "react-native";

// Simplified version: just uses the middle gradient color since MaskedView may not be installed
interface GradientTextProps {
  text: string;
  colors?: string[];
  style?: TextStyle;
}

export function GradientText({ text, colors = ["#818CF8", "#A78BFA", "#F472B6"], style }: GradientTextProps) {
  // Use the middle gradient color as a solid fallback
  return <Text style={[{ color: colors[1] || colors[0] }, style]}>{text}</Text>;
}
