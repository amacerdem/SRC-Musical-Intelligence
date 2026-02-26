/* -- MindVisualizer -- Simulated audio visualization bars -------------------
 *  12 vertical bars that respond to vizParams from the M3 audio store.
 *  Uses sine-wave simulation when no real audio analysis is available.
 *  Colors follow the consonance gradient palette.
 *  Reanimated for smooth bar height changes.
 *  ----------------------------------------------------------------------- */

import React, { useEffect } from "react";
import { View, StyleSheet, Dimensions } from "react-native";
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withRepeat,
  withSequence,
  withDelay,
  Easing,
} from "react-native-reanimated";
import { useM3AudioStore, type VizParams } from "../../stores/useM3AudioStore";
import { colors } from "../../design/tokens";

const BAR_COUNT = 12;
const { width: SCREEN_WIDTH } = Dimensions.get("window");
const VIZ_WIDTH = SCREEN_WIDTH - 64;
const BAR_GAP = 6;
const BAR_WIDTH = (VIZ_WIDTH - BAR_GAP * (BAR_COUNT - 1)) / BAR_COUNT;
const MAX_BAR_HEIGHT = 160;

/* -- Bar colors: gradient from consonance purple through reward gold -- */
const BAR_COLORS = [
  "#C084FC", "#B47AFA", "#A872F8", "#9C6AF6",
  "#9065F4", "#8B5CF6", "#A06AE0", "#B878CA",
  "#D08AB4", "#E89C9E", "#F0AE88", "#FBBF24",
];

interface BarProps {
  index: number;
  vizParams: VizParams;
  isPlaying: boolean;
}

function VizBar({ index, vizParams, isPlaying }: BarProps) {
  const height = useSharedValue(10);

  useEffect(() => {
    if (!isPlaying) {
      // Idle: gentle breathing animation
      const baseHeight = 10 + Math.sin(index * 0.7) * 8;
      height.value = withRepeat(
        withSequence(
          withTiming(baseHeight + 15, { duration: 1200 + index * 100, easing: Easing.inOut(Easing.sin) }),
          withTiming(baseHeight, { duration: 1200 + index * 100, easing: Easing.inOut(Easing.sin) }),
        ),
        -1,
        true,
      );
      return;
    }

    // Playing: derive height from vizParams
    const { energy, bass, mid, treble, brightness, loudness } = vizParams;

    // Each bar responds to different frequency ranges
    let barValue: number;
    if (index < 3) {
      // Low bars: bass-heavy
      barValue = bass * 0.7 + energy * 0.3;
    } else if (index < 6) {
      // Low-mid bars
      barValue = bass * 0.3 + mid * 0.5 + energy * 0.2;
    } else if (index < 9) {
      // Mid-high bars
      barValue = mid * 0.4 + treble * 0.4 + brightness * 0.2;
    } else {
      // High bars: treble + brightness
      barValue = treble * 0.5 + brightness * 0.3 + loudness * 0.2;
    }

    // Add per-bar variation with sine offset
    const variation = Math.sin(Date.now() * 0.003 + index * 0.8) * 0.15;
    const targetHeight = Math.max(8, (barValue + variation) * MAX_BAR_HEIGHT);

    height.value = withTiming(targetHeight, {
      duration: 150,
      easing: Easing.out(Easing.quad),
    });
  }, [vizParams, isPlaying]);

  const animatedStyle = useAnimatedStyle(() => ({
    height: height.value,
  }));

  return (
    <Animated.View
      style={[
        styles.bar,
        {
          width: BAR_WIDTH,
          backgroundColor: BAR_COLORS[index],
          opacity: isPlaying ? 0.9 : 0.4,
        },
        animatedStyle,
      ]}
    />
  );
}

export function MindVisualizer() {
  const vizParams = useM3AudioStore((s) => s.vizParams);
  const isPlaying = useM3AudioStore((s) => s.isPlaying);

  return (
    <View style={styles.container}>
      <View style={styles.barsRow}>
        {Array.from({ length: BAR_COUNT }, (_, i) => (
          <VizBar
            key={i}
            index={i}
            vizParams={vizParams}
            isPlaying={isPlaying}
          />
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 24,
  },
  barsRow: {
    flexDirection: "row",
    alignItems: "flex-end",
    justifyContent: "center",
    height: MAX_BAR_HEIGHT + 20,
    gap: BAR_GAP,
  },
  bar: {
    borderRadius: 3,
    minHeight: 6,
  },
});
