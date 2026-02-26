import { Audio } from "expo-av";

export class AudioPlayer {
  private sound: Audio.Sound | null = null;
  private onEndedCallback: (() => void) | null = null;
  private onTimeUpdateCallback: ((time: number) => void) | null = null;
  private updateInterval: ReturnType<typeof setInterval> | null = null;

  async initialize() {
    await Audio.setAudioModeAsync({
      playsInSilentModeIOS: true,
      staysActiveInBackground: true,
      shouldDuckAndroid: true,
    });
  }

  async play(src: string): Promise<void> {
    await this.stop();

    const { sound } = await Audio.Sound.createAsync(
      // For bundled assets, use require; for URIs, use { uri: src }
      { uri: src },
      { shouldPlay: true, volume: 1.0 },
      this.onPlaybackStatusUpdate.bind(this)
    );
    this.sound = sound;

    // Start time update polling
    this.startTimeUpdates();
  }

  async playAsset(asset: number): Promise<void> {
    await this.stop();

    const { sound } = await Audio.Sound.createAsync(
      asset,
      { shouldPlay: true, volume: 1.0 },
      this.onPlaybackStatusUpdate.bind(this)
    );
    this.sound = sound;
    this.startTimeUpdates();
  }

  private onPlaybackStatusUpdate(status: any) {
    if (status.isLoaded && status.didJustFinish) {
      this.onEndedCallback?.();
    }
  }

  private startTimeUpdates() {
    this.stopTimeUpdates();
    this.updateInterval = setInterval(async () => {
      if (!this.sound) return;
      const status = await this.sound.getStatusAsync();
      if (status.isLoaded) {
        this.onTimeUpdateCallback?.(status.positionMillis / 1000);
      }
    }, 250);
  }

  private stopTimeUpdates() {
    if (this.updateInterval) {
      clearInterval(this.updateInterval);
      this.updateInterval = null;
    }
  }

  async pause(): Promise<void> {
    await this.sound?.pauseAsync();
  }

  async resume(): Promise<void> {
    await this.sound?.playAsync();
  }

  async stop(): Promise<void> {
    this.stopTimeUpdates();
    if (this.sound) {
      await this.sound.stopAsync();
      await this.sound.unloadAsync();
      this.sound = null;
    }
  }

  async seek(seconds: number): Promise<void> {
    await this.sound?.setPositionAsync(seconds * 1000);
  }

  async setVolume(vol: number): Promise<void> {
    await this.sound?.setVolumeAsync(Math.max(0, Math.min(1, vol)));
  }

  async getDuration(): Promise<number> {
    if (!this.sound) return 0;
    const status = await this.sound.getStatusAsync();
    if (status.isLoaded) return (status.durationMillis ?? 0) / 1000;
    return 0;
  }

  async getCurrentTime(): Promise<number> {
    if (!this.sound) return 0;
    const status = await this.sound.getStatusAsync();
    if (status.isLoaded) return status.positionMillis / 1000;
    return 0;
  }

  onEnded(callback: () => void): () => void {
    this.onEndedCallback = callback;
    return () => { this.onEndedCallback = null; };
  }

  onTimeUpdate(callback: (time: number) => void): () => void {
    this.onTimeUpdateCallback = callback;
    return () => { this.onTimeUpdateCallback = null; };
  }

  async dispose(): Promise<void> {
    await this.stop();
    this.onEndedCallback = null;
    this.onTimeUpdateCallback = null;
  }
}

// Singleton
export const audioPlayer = new AudioPlayer();
