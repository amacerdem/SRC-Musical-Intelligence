/* -- FunctionsGrid -- 3x3 grid of C3 Functions F1-F9 -----------------------
 *  Each cell shows function number and short name.
 *  Active functions (from mind.activeFunctions) have colored border/glow.
 *  Inactive ones are dimmed.
 *  ----------------------------------------------------------------------- */

import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { C3_FUNCTIONS } from "../../data/m3-stages";
import { colors, fonts, spacing } from "../../design/tokens";

interface FunctionsGridProps {
  activeFunctions: number[];
}

function FunctionCell({
  id,
  abbr,
  name,
  color,
  isActive,
}: {
  id: number;
  abbr: string;
  name: string;
  color: string;
  isActive: boolean;
}) {
  return (
    <View
      style={[
        styles.cell,
        isActive
          ? {
              borderColor: color,
              backgroundColor: `${color}10`,
            }
          : {
              borderColor: "rgba(255,255,255,0.04)",
              backgroundColor: "rgba(255,255,255,0.02)",
            },
      ]}
    >
      <Text
        style={[
          styles.abbr,
          { color: isActive ? color : colors.textTertiary },
        ]}
      >
        {abbr}
      </Text>
      <Text
        style={[
          styles.name,
          { color: isActive ? colors.textSecondary : colors.textMuted },
        ]}
      >
        {name}
      </Text>
    </View>
  );
}

export function FunctionsGrid({ activeFunctions }: FunctionsGridProps) {
  return (
    <View style={styles.grid}>
      {C3_FUNCTIONS.map((fn) => (
        <FunctionCell
          key={fn.id}
          id={fn.id}
          abbr={fn.abbr}
          name={fn.name}
          color={fn.color}
          isActive={activeFunctions.includes(fn.id)}
        />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  grid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: spacing.sm,
  },
  cell: {
    width: "30.5%",
    aspectRatio: 1.2,
    borderRadius: 10,
    borderWidth: 1,
    alignItems: "center",
    justifyContent: "center",
    gap: 2,
  },
  abbr: {
    fontSize: 15,
    fontFamily: fonts.monoSemiBold,
    letterSpacing: 0.5,
  },
  name: {
    fontSize: 9,
    fontFamily: fonts.body,
    textTransform: "uppercase",
    letterSpacing: 0.6,
  },
});
