/* -- MindVisualizer -- Circular radial audio visualization --------------------
 *  16 bars arranged radially around a central glowing nucleus.
 *  Each bar extends outward from the center like a starburst.
 *  Bars respond to vizParams from the M3 audio store.
 *  Color gradient cycles: violet -> cyan -> amber -> pink -> violet.
 *  Reanimated for smooth bar height changes and nucleus breathing.
 *  ----------------------------------------------------------------------- */

import React, { useEffect } from "react";
import { View, StyleSheet } from "react-native";
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

const BAR_COUNT = 16;
const DEFAULT_SIZE = 200;
const NUCLEUS_RADIUS = 12;
const BAR_WIDTH = 3.5;
const MAX_BAR_HEIGHT = 60;
const INNER_OFFSET = NUCLEUS_RADIUS + 4; // gap between nucleus edge and bar start

/* -- 16-color gradient: violet -> cyan -> amber -> pink -> violet ---------- */
const BAR_COLORS = [
  "#8B5CF6", // 0   violet
  "#7C6AEE", // 1
  "#5E8DE6", // 2
  "#3AA5DE", // 3
  "#06B6D4", // 4   cyan
  "#2EBE9E", // 5
  "#6CC468", // 6
  "#B0CA3C", // 7
  "#FBBF24", // 8   amber
  "#F5A235", // 9
  "#EF8546", // 10
  "#EA6857", // 11
  "#EC4899", // 12  pink
  "#C84EAA", // 13
  "#A453BB", // 14
  "#8B58D0", // 15  back toward violet
];

/* -- Nucleus (center glow) ------------------------------------------------ */

function Nucleus() {
  const opacity = useSharedValue(0.4);

  useEffect(() => {
    opacity.value = withRepeat(
      withSequence(
        withTiming(0.8, { duration: 2000, easing: Easing.inOut(Easing.sin) }),
        withTiming(0.4, { duration: 2000, easing: Easing.inOut(Easing.sin) }),
      ),
      -1,
      true,
    );
  }, []);

  const animatedStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
  }));

  return (
    <Animated.View style={[styles.nucleus, animatedStyle]} />
  );
}

/* -- Radial Bar ----------------------------------------------------------- */

interface RadialBarProps {
  index: number;
  vizParams: VizParams;
  isPlaying: boolean;
  size: number;
}

function RadialBar({ index, vizParams, isPlaying, size }: RadialBarProps) {
  const barHeight = useSharedValue(20);
  const angleDeg = (index / BAR_COUNT) * 360;
  const center = size / 2;

  useEffect(() => {
    if (!isPlaying) {
      // Idle: gentle breathing animation (20-40px range)
      const base = 20 + Math.sin(index * 0.9) * 6;
      const peak = base + 14 + Math.sin(index * 1.3) * 6;
      barHeight.value = withRepeat(
        withSequence(
          withDelay(
            index * 80,
            withTiming(peak, {
              duration: 1400 + index * 60,
              easing: Easing.inOut(Easing.sin),
            }),
          ),
          withTiming(base, {
            duration: 1400 + index * 60,
            easing: Easing.inOut(Easing.sin),
          }),
        ),
        -1,
        true,
      );
      return;
    }

    // Playing: derive height from vizParams by frequency band
    const { energy, bass, mid, treble, brightness, loudness } = vizParams;

    let barValue: number;
    if (index < 4) {
      // Bars 0-3: bass-heavy
      barValue = bass * 0.7 + energy * 0.3;
    } else if (index < 8) {
      // Bars 4-7: low-mid
      barValue = bass * 0.3 + mid * 0.5 + energy * 0.2;
    } else if (index < 12) {
      // Bars 8-11: mid-high
      barValue = mid * 0.4 + treble * 0.4 + brightness * 0.2;
    } else {
      // Bars 12-15: treble + brightness
      barValue = treble * 0.5 + brightness * 0.3 + loudness * 0.2;
    }

    const targetHeight = Math.max(6, Math.min(barValue * MAX_BAR_HEIGHT, MAX_BAR_HEIGHT));

    barHeight.value = withTiming(targetHeight, {
      duration: 120,
    });
  }, [vizParams, isPlaying]);

  const animatedStyle = useAnimatedStyle(() => ({
    height: barHeight.value,
  }));

  return (
    <View
      style={[
        styles.barAnchor,
        {
          left: center - BAR_WIDTH / 2,
          top: center,
          transform: [{ rotate: `${angleDeg}deg` }],
        },
      ]}
    >
      <Animated.View
        style={[
          styles.bar,
          {
            width: BAR_WIDTH,
            backgroundColor: BAR_COLORS[index],
            opacity: isPlaying ? 0.9 : 0.5,
            // translateY moves bar outward from center (negative = upward in pre-rotated space)
            transform: [{ translateY: -(INNER_OFFSET) }],
          },
          animatedStyle,
        ]}
      />
    </View>
  );
}

/* -- Main Component ------------------------------------------------------- */

interface MindVisualizerProps {
  size?: number;
}

export function MindVisualizer({ size = DEFAULT_SIZE }: MindVisualizerProps) {
  const vizParams = useM3AudioStore((s) => s.vizParams);
  const isPlaying = useM3AudioStore((s) => s.isPlaying);

  return (
    <View style={[styles.container, { width: size, height: size }]}>
      {/* Radial bars */}
      {Array.from({ length: BAR_COUNT }, (_, i) => (
        <RadialBar
          key={i}
          index={i}
          vizParams={vizParams}
          isPlaying={isPlaying}
          size={size}
        />
      ))}

      {/* Center nucleus */}
      <View
        style={[
          styles.nucleusContainer,
          {
            left: size / 2 - NUCLEUS_RADIUS,
            top: size / 2 - NUCLEUS_RADIUS,
          },
        ]}
      >
        <Nucleus />
      </View>
    </View>
  );
}

/* -- Styles --------------------------------------------------------------- */

const styles = StyleSheet.create({
  container: {
    alignSelf: "center",
    position: "relative",
  },
  barAnchor: {
    position: "absolute",
    alignItems: "center",
    // The anchor sits at center; rotation fans bars out.
    // transformOrigin defaults to center of the element.
    // The bar inside uses translateY to push outward from this anchor.
  },
  bar: {
    borderRadius: BAR_WIDTH / 2,
    // Bar grows upward (in its local rotated coordinate space) = outward from center
    // The anchor origin is at center, translateY on bar pushes it out
  },
  nucleusContainer: {
    position: "absolute",
    width: NUCLEUS_RADIUS * 2,
    height: NUCLEUS_RADIUS * 2,
  },
  nucleus: {
    width: NUCLEUS_RADIUS * 2,
    height: NUCLEUS_RADIUS * 2,
    borderRadius: NUCLEUS_RADIUS,
    backgroundColor: colors.violet,
    shadowColor: colors.violet,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.8,
    shadowRadius: 10,
    elevation: 8,
  },
});
