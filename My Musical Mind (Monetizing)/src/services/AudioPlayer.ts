/* ── AudioPlayer — HTMLAudioElement → Web Audio API graph ────────────
 *  Plays MP3 files from public/music/ while routing through AnalyserNode
 *  for real-time FFT visualization.
 *
 *  Graph:  HTMLAudioElement → MediaElementSource → GainNode → AnalyserNode → Destination
 *
 *  Usage:
 *    const player = new AudioPlayer();
 *    await player.play("/music/lib-01.mp3");
 *    player.getAnalyser();  // → AnalyserNode for AudioAnalyzer
 *    player.dispose();
 *  ──────────────────────────────────────────────────────────────── */

export class AudioPlayer {
  private ctx: AudioContext | null = null;
  private audio: HTMLAudioElement | null = null;
  private source: MediaElementAudioSourceNode | null = null;
  private gain: GainNode | null = null;
  private analyser: AnalyserNode | null = null;
  private _volume = 0.75;
  private _currentSrc = "";

  /* ── Initialization ────────────────────────── */

  private ensureContext() {
    if (!this.ctx) {
      this.ctx = new AudioContext();
      this.gain = this.ctx.createGain();
      this.gain.gain.value = this._volume;

      this.analyser = this.ctx.createAnalyser();
      this.analyser.fftSize = 2048;
      this.analyser.smoothingTimeConstant = 0.8;

      this.gain.connect(this.analyser);
      this.analyser.connect(this.ctx.destination);
    }
  }

  private ensureAudio() {
    if (!this.audio) {
      this.audio = new Audio();
      this.audio.crossOrigin = "anonymous";
      this.audio.preload = "auto";
    }
  }

  /* ── Playback ──────────────────────────────── */

  async play(src: string): Promise<void> {
    this.ensureContext();
    this.ensureAudio();

    // Resume AudioContext if suspended (browser autoplay policy)
    if (this.ctx!.state === "suspended") {
      await this.ctx!.resume();
    }

    // If same source, just resume
    if (this._currentSrc === src && this.audio!.paused) {
      await this.audio!.play();
      return;
    }

    // Disconnect previous source if any
    if (this.source) {
      try { this.source.disconnect(); } catch { /* already disconnected */ }
      this.source = null;
    }

    this._currentSrc = src;
    this.audio!.src = src;

    // Create new MediaElementSource (only once per audio element)
    if (!this.source) {
      this.source = this.ctx!.createMediaElementSource(this.audio!);
      this.source.connect(this.gain!);
    }

    await this.audio!.play();
  }

  pause() {
    this.audio?.pause();
  }

  resume() {
    if (this.ctx?.state === "suspended") {
      this.ctx.resume();
    }
    this.audio?.play();
  }

  stop() {
    if (this.audio) {
      this.audio.pause();
      this.audio.currentTime = 0;
    }
  }

  seek(time: number) {
    if (this.audio) {
      this.audio.currentTime = Math.max(0, Math.min(time, this.audio.duration || 0));
    }
  }

  /* ── Volume ────────────────────────────────── */

  setVolume(vol: number) {
    this._volume = Math.max(0, Math.min(1, vol));
    if (this.gain) {
      this.gain.gain.value = this._volume;
    }
  }

  getVolume(): number {
    return this._volume;
  }

  /* ── Getters ───────────────────────────────── */

  getAnalyser(): AnalyserNode | null {
    return this.analyser;
  }

  getCurrentTime(): number {
    return this.audio?.currentTime ?? 0;
  }

  getDuration(): number {
    return this.audio?.duration ?? 0;
  }

  isPaused(): boolean {
    return this.audio?.paused ?? true;
  }

  isEnded(): boolean {
    return this.audio?.ended ?? false;
  }

  getAudioElement(): HTMLAudioElement | null {
    return this.audio;
  }

  /* ── Event Binding ─────────────────────────── */

  onEnded(callback: () => void) {
    this.audio?.addEventListener("ended", callback);
    return () => this.audio?.removeEventListener("ended", callback);
  }

  onTimeUpdate(callback: (time: number) => void) {
    const handler = () => callback(this.audio?.currentTime ?? 0);
    this.audio?.addEventListener("timeupdate", handler);
    return () => this.audio?.removeEventListener("timeupdate", handler);
  }

  onLoadedMetadata(callback: (duration: number) => void) {
    const handler = () => callback(this.audio?.duration ?? 0);
    this.audio?.addEventListener("loadedmetadata", handler);
    return () => this.audio?.removeEventListener("loadedmetadata", handler);
  }

  /* ── Cleanup ───────────────────────────────── */

  dispose() {
    if (this.audio) {
      this.audio.pause();
      this.audio.src = "";
    }
    if (this.source) {
      try { this.source.disconnect(); } catch { /* ok */ }
    }
    if (this.gain) {
      try { this.gain.disconnect(); } catch { /* ok */ }
    }
    if (this.analyser) {
      try { this.analyser.disconnect(); } catch { /* ok */ }
    }
    if (this.ctx && this.ctx.state !== "closed") {
      this.ctx.close();
    }
    this.ctx = null;
    this.audio = null;
    this.source = null;
    this.gain = null;
    this.analyser = null;
    this._currentSrc = "";
  }
}
