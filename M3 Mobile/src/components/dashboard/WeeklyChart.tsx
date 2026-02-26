/* -- WeeklyChart -- 7 vertical bars (Mon-Sun) for weekly listening ----------
 *  Mock data from mock-listening. Each bar height proportional to minutes.
 *  Colors blended from belief domain colors.
 *  Day labels below each bar.
 *  ----------------------------------------------------------------------- */

import React from "react";
import { View, Text, StyleSheet } from "react-native";
import Animated, {
  useAnimatedStyle,
  withTiming,
  withDelay,
  Easing,
} from "react-native-reanimated";
import { lastWeekDays } from "../../data/mock-listening";
import { colors, fonts, spacing } from "../../design/tokens";

const DAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
const MAX_HEIGHT = 100;

/* Belief-to-color mapping for bar tinting */
const BELIEF_COLORS: Record<string, string> = {
  consonance: colors.consonance,
  tempo: colors.tempo,
  salience: colors.salience,
  familiarity: colors.familiarity,
  reward: colors.reward,
};

interface DayBarProps {
  minutes: number;
  maxMinutes: number;
  dayLabel: string;
  color: string;
  index: number;
}

function DayBar({ minutes, maxMinutes, dayLabel, color, index }: DayBarProps) {
  const heightPct = maxMinutes > 0 ? minutes / maxMinutes : 0;
  const barHeight = Math.max(4, heightPct * MAX_HEIGHT);

  const animatedStyle = useAnimatedStyle(() => ({
    height: withDelay(
      index * 60,
      withTiming(barHeight, { duration: 600, easing: Easing.out(Easing.cubic) }),
    ),
  }));

  return (
    <View style={styles.barColumn}>
      <Text style={styles.minutesLabel}>{minutes}</Text>
      <Animated.View style={[styles.bar, { backgroundColor: color }, animatedStyle]} />
      <Text style={styles.dayLabel}>{dayLabel}</Text>
    </View>
  );
}

export function WeeklyChart() {
  const maxMinutes = Math.max(...lastWeekDays.map((d) => d.minutesListened));

  return (
    <View style={styles.container}>
      <View style={styles.barsRow}>
        {lastWeekDays.map((day, i) => (
          <DayBar
            key={day.date}
            minutes={day.minutesListened}
            maxMinutes={maxMinutes}
            dayLabel={DAY_LABELS[i] ?? "?"}
            color={BELIEF_COLORS[day.dominantBelief] ?? colors.violet}
            index={i}
          />
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingTop: spacing.sm,
  },
  barsRow: {
    flexDirection: "row",
    alignItems: "flex-end",
    justifyContent: "space-between",
    height: MAX_HEIGHT + 40,
    paddingHorizontal: spacing.xs,
  },
  barColumn: {
    alignItems: "center",
    flex: 1,
    gap: spacing.xs,
  },
  bar: {
    width: 20,
    borderRadius: 4,
    minHeight: 4,
  },
  minutesLabel: {
    fontSize: 9,
    fontFamily: fonts.mono,
    color: colors.textTertiary,
  },
  dayLabel: {
    fontSize: 10,
    fontFamily: fonts.bodySemiBold,
    color: colors.textTertiary,
    letterSpacing: 0.3,
  },
});
