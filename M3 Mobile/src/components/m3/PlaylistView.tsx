/* -- PlaylistView -- Track list with now-playing highlight -------------------
 *  FlatList of LibraryTrack items from useM3AudioStore.playlist.
 *  Currently playing track highlighted with accent color.
 *  Tapping a row switches to that track.
 *  ----------------------------------------------------------------------- */

import React, { useCallback } from "react";
import { View, Text, FlatList, TouchableOpacity, StyleSheet } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useM3AudioStore } from "../../stores/useM3AudioStore";
import type { LibraryTrack } from "../../data/track-library";
import { colors, fonts, spacing } from "../../design/tokens";

function formatDuration(sec: number): string {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m}:${s.toString().padStart(2, "0")}`;
}

interface TrackRowProps {
  track: LibraryTrack;
  index: number;
  isCurrent: boolean;
  onPress: () => void;
}

function TrackRow({ track, index, isCurrent, onPress }: TrackRowProps) {
  return (
    <TouchableOpacity
      style={[styles.row, isCurrent && styles.rowActive]}
      onPress={onPress}
      activeOpacity={0.7}
    >
      {/* Track number or playing indicator */}
      <View style={styles.indexCol}>
        {isCurrent ? (
          <Ionicons name="musical-note" size={14} color={colors.violet} />
        ) : (
          <Text style={styles.indexText}>{index + 1}</Text>
        )}
      </View>

      {/* Title + Artist */}
      <View style={styles.infoCol}>
        <Text
          style={[styles.trackTitle, isCurrent && styles.trackTitleActive]}
          numberOfLines={1}
        >
          {track.name}
        </Text>
        <Text style={styles.trackArtist} numberOfLines={1}>
          {track.artist}
        </Text>
      </View>

      {/* Duration */}
      <Text style={styles.duration}>
        {formatDuration(track.durationSec)}
      </Text>
    </TouchableOpacity>
  );
}

export function PlaylistView() {
  const playlist = useM3AudioStore((s) => s.playlist);
  const currentTrackIdx = useM3AudioStore((s) => s.currentTrackIdx);
  const setCurrentTrack = useM3AudioStore((s) => s.setCurrentTrack);
  const setIsPlaying = useM3AudioStore((s) => s.setIsPlaying);

  const handleTrackPress = useCallback(
    (idx: number) => {
      setCurrentTrack(idx);
      setIsPlaying(true);
    },
    [setCurrentTrack, setIsPlaying],
  );

  const renderItem = useCallback(
    ({ item, index }: { item: LibraryTrack; index: number }) => (
      <TrackRow
        track={item}
        index={index}
        isCurrent={index === currentTrackIdx}
        onPress={() => handleTrackPress(index)}
      />
    ),
    [currentTrackIdx, handleTrackPress],
  );

  const keyExtractor = useCallback((item: LibraryTrack) => item.id, []);

  if (playlist.length === 0) {
    return (
      <View style={styles.emptyContainer}>
        <Text style={styles.emptyText}>No tracks in playlist</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.header}>
        Playlist ({playlist.length} tracks)
      </Text>
      <FlatList
        data={playlist}
        renderItem={renderItem}
        keyExtractor={keyExtractor}
        showsVerticalScrollIndicator={false}
        style={styles.list}
        contentContainerStyle={styles.listContent}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    fontSize: 13,
    fontFamily: fonts.heading,
    color: colors.textSecondary,
    textTransform: "uppercase",
    letterSpacing: 1,
    paddingHorizontal: spacing.lg,
    marginBottom: spacing.sm,
  },
  list: {
    flex: 1,
  },
  listContent: {
    paddingBottom: 100, // room for NowPlayingBar
  },
  row: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.lg,
    gap: spacing.md,
  },
  rowActive: {
    backgroundColor: "rgba(139,92,246,0.08)",
  },
  indexCol: {
    width: 24,
    alignItems: "center",
  },
  indexText: {
    fontSize: 13,
    fontFamily: fonts.mono,
    color: colors.textTertiary,
  },
  infoCol: {
    flex: 1,
  },
  trackTitle: {
    fontSize: 14,
    fontFamily: fonts.bodySemiBold,
    color: colors.textPrimary,
    letterSpacing: 0.1,
  },
  trackTitleActive: {
    color: colors.violet,
  },
  trackArtist: {
    fontSize: 12,
    fontFamily: fonts.body,
    color: colors.textSecondary,
    marginTop: 2,
  },
  duration: {
    fontSize: 12,
    fontFamily: fonts.mono,
    color: colors.textTertiary,
    minWidth: 36,
    textAlign: "right",
  },
  emptyContainer: {
    padding: spacing.xxl,
    alignItems: "center",
  },
  emptyText: {
    fontSize: 14,
    fontFamily: fonts.body,
    color: colors.textTertiary,
  },
});
