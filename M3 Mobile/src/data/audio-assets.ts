/* ── Audio Asset Map — Static require() for bundled MP3s ────────────────
 *  React Native requires static require() calls, so we map track
 *  audioFile paths to their bundled asset modules.
 *  ──────────────────────────────────────────────────────────────── */

const AUDIO_ASSETS: Record<string, number> = {
  "/music/lib-01.mp3": require("../../assets/music/lib-01.mp3"),
  "/music/lib-02.mp3": require("../../assets/music/lib-02.mp3"),
  "/music/lib-03.mp3": require("../../assets/music/lib-03.mp3"),
  "/music/lib-04.mp3": require("../../assets/music/lib-04.mp3"),
  "/music/lib-05.mp3": require("../../assets/music/lib-05.mp3"),
  "/music/lib-06.mp3": require("../../assets/music/lib-06.mp3"),
  "/music/lib-07.mp3": require("../../assets/music/lib-07.mp3"),
  "/music/lib-08.mp3": require("../../assets/music/lib-08.mp3"),
  "/music/lib-09.mp3": require("../../assets/music/lib-09.mp3"),
  "/music/lib-10.mp3": require("../../assets/music/lib-10.mp3"),
  "/music/lib-11.mp3": require("../../assets/music/lib-11.mp3"),
  "/music/lib-12.mp3": require("../../assets/music/lib-12.mp3"),
  "/music/lib-13.mp3": require("../../assets/music/lib-13.mp3"),
  "/music/lib-14.mp3": require("../../assets/music/lib-14.mp3"),
  "/music/lib-15.mp3": require("../../assets/music/lib-15.mp3"),
  "/music/lib-16.mp3": require("../../assets/music/lib-16.mp3"),
  "/music/lib-17.mp3": require("../../assets/music/lib-17.mp3"),
  "/music/lib-18.mp3": require("../../assets/music/lib-18.mp3"),
  "/music/lib-19.mp3": require("../../assets/music/lib-19.mp3"),
  "/music/lib-20.mp3": require("../../assets/music/lib-20.mp3"),
  "/music/lib-21.mp3": require("../../assets/music/lib-21.mp3"),
  "/music/lib-22.mp3": require("../../assets/music/lib-22.mp3"),
  "/music/lib-23.mp3": require("../../assets/music/lib-23.mp3"),
  "/music/lib-24.mp3": require("../../assets/music/lib-24.mp3"),
  "/music/lib-25.mp3": require("../../assets/music/lib-25.mp3"),
  "/music/lib-26.mp3": require("../../assets/music/lib-26.mp3"),
  "/music/lib-27.mp3": require("../../assets/music/lib-27.mp3"),
  "/music/lib-28.mp3": require("../../assets/music/lib-28.mp3"),
  "/music/lib-29.mp3": require("../../assets/music/lib-29.mp3"),
  "/music/lib-30.mp3": require("../../assets/music/lib-30.mp3"),
  "/music/lib-31.mp3": require("../../assets/music/lib-31.mp3"),
  "/music/lib-32.mp3": require("../../assets/music/lib-32.mp3"),
  "/music/lib-33.mp3": require("../../assets/music/lib-33.mp3"),
  "/music/lib-34.mp3": require("../../assets/music/lib-34.mp3"),
  "/music/lib-35.mp3": require("../../assets/music/lib-35.mp3"),
  "/music/lib-36.mp3": require("../../assets/music/lib-36.mp3"),
  "/music/lib-37.mp3": require("../../assets/music/lib-37.mp3"),
  "/music/lib-38.mp3": require("../../assets/music/lib-38.mp3"),
  "/music/lib-39.mp3": require("../../assets/music/lib-39.mp3"),
  "/music/lib-40.mp3": require("../../assets/music/lib-40.mp3"),
  "/music/lib-41.mp3": require("../../assets/music/lib-41.mp3"),
  "/music/lib-42.mp3": require("../../assets/music/lib-42.mp3"),
  "/music/lib-43.mp3": require("../../assets/music/lib-43.mp3"),
  "/music/lib-44.mp3": require("../../assets/music/lib-44.mp3"),
  "/music/lib-45.mp3": require("../../assets/music/lib-45.mp3"),
  "/music/lib-46.mp3": require("../../assets/music/lib-46.mp3"),
  "/music/lib-47.mp3": require("../../assets/music/lib-47.mp3"),
  "/music/lib-48.mp3": require("../../assets/music/lib-48.mp3"),
};

/** Resolve a track's audioFile path to a bundled asset module ID */
export function resolveAudioAsset(audioFile: string): number | undefined {
  return AUDIO_ASSETS[audioFile];
}
