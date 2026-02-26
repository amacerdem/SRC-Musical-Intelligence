/* -- NowPlayingBar -- Sticky bottom playback bar ----------------------------
 *  Shows current track info, play/pause, skip forward, thin progress bar.
 *  Uses useM3AudioStore for all playback state.
 *  ----------------------------------------------------------------------- */

import React from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import Animated, { useAnimatedStyle, withTiming } from "react-native-reanimated";
import { Ionicons } from "@expo/vector-icons";
import { useM3AudioStore } from "../../stores/useM3AudioStore";
import { colors, fonts, spacing } from "../../design/tokens";

export function NowPlayingBar() {
  const playlist = useM3AudioStore((s) => s.playlist);
  const currentTrackIdx = useM3AudioStore((s) => s.currentTrackIdx);
  const isPlaying = useM3AudioStore((s) => s.isPlaying);
  const currentTime = useM3AudioStore((s) => s.currentTime);
  const duration = useM3AudioStore((s) => s.duration);
  const togglePlay = useM3AudioStore((s) => s.togglePlay);
  const skipTrack = useM3AudioStore((s) => s.skipTrack);

  const track = playlist[currentTrackIdx];
  if (!track) return null;

  const progress = duration > 0 ? currentTime / duration : 0;

  const progressStyle = useAnimatedStyle(() => ({
    width: withTiming(`${Math.min(100, progress * 100)}%`, { duration: 300 }),
  }));

  return (
    <View style={styles.container}>
      {/* Progress bar (top edge) */}
      <View style={styles.progressTrack}>
        <Animated.View
          style={[styles.progressFill, progressStyle]}
        />
      </View>

      <View style={styles.content}>
        {/* Track info */}
        <View style={styles.trackInfo}>
          <Text style={styles.trackName} numberOfLines={1}>
            {track.name}
          </Text>
          <Text style={styles.artistName} numberOfLines={1}>
            {track.artist}
          </Text>
        </View>

        {/* Controls */}
        <View style={styles.controls}>
          <TouchableOpacity
            onPress={togglePlay}
            style={styles.playButton}
            activeOpacity={0.7}
          >
            <Ionicons
              name={isPlaying ? "pause" : "play"}
              size={22}
              color={colors.textPrimary}
            />
          </TouchableOpacity>

          <TouchableOpacity
            onPress={skipTrack}
            style={styles.skipButton}
            activeOpacity={0.7}
          >
            <Ionicons
              name="play-forward"
              size={20}
              color={colors.textSecondary}
            />
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: "rgba(10,10,10,0.95)",
    borderTopWidth: StyleSheet.hairlineWidth,
    borderTopColor: colors.border,
  },
  progressTrack: {
    height: 2,
    backgroundColor: colors.surfaceHigh,
  },
  progressFill: {
    height: "100%",
    backgroundColor: colors.violet,
  },
  content: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
  },
  trackInfo: {
    flex: 1,
    marginRight: spacing.md,
  },
  trackName: {
    fontSize: 14,
    fontFamily: fonts.bodySemiBold,
    color: colors.textPrimary,
    letterSpacing: 0.2,
  },
  artistName: {
    fontSize: 12,
    fontFamily: fonts.body,
    color: colors.textSecondary,
    marginTop: 2,
  },
  controls: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.md,
  },
  playButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: colors.surfaceHigh,
    alignItems: "center",
    justifyContent: "center",
  },
  skipButton: {
    width: 36,
    height: 36,
    alignItems: "center",
    justifyContent: "center",
  },
});
