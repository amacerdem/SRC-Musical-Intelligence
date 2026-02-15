/**
 * Web Audio API playback engine with rAF-driven frame synchronization.
 */
import { audioUrl } from "../api/client";

export class PlaybackEngine {
  private ctx: AudioContext | null = null;
  private buffer: AudioBuffer | null = null;
  private source: AudioBufferSourceNode | null = null;
  private gainNode: GainNode | null = null;
  private startTime = 0; // audioContext.currentTime when play() started
  private startOffset = 0; // offset in the audio buffer
  private rafId = 0;
  private _isPlaying = false;
  private onTimeUpdate: (time: number) => void;

  constructor(onTimeUpdate: (time: number) => void) {
    this.onTimeUpdate = onTimeUpdate;
  }

  get isPlaying(): boolean {
    return this._isPlaying;
  }

  get duration(): number {
    return this.buffer?.duration ?? 0;
  }

  async load(slug: string): Promise<void> {
    if (!this.ctx) {
      this.ctx = new AudioContext();
      this.gainNode = this.ctx.createGain();
      this.gainNode.connect(this.ctx.destination);
    }
    const url = audioUrl(slug);
    const res = await fetch(url);
    const arrayBuf = await res.arrayBuffer();
    this.buffer = await this.ctx.decodeAudioData(arrayBuf);
    this.startOffset = 0;
    this._isPlaying = false;
  }

  play(): void {
    if (!this.ctx || !this.buffer || !this.gainNode || this._isPlaying) return;
    this.source = this.ctx.createBufferSource();
    this.source.buffer = this.buffer;
    this.source.connect(this.gainNode);
    this.source.onended = () => {
      if (this._isPlaying) this.stop();
    };
    this.startTime = this.ctx.currentTime;
    this.source.start(0, this.startOffset);
    this._isPlaying = true;
    this._tick();
  }

  pause(): void {
    if (!this.ctx || !this._isPlaying) return;
    this.startOffset += this.ctx.currentTime - this.startTime;
    this.source?.stop();
    this.source = null;
    this._isPlaying = false;
    cancelAnimationFrame(this.rafId);
  }

  stop(): void {
    this.pause();
    this.startOffset = 0;
    this.onTimeUpdate(0);
  }

  seek(time: number): void {
    const wasPlaying = this._isPlaying;
    if (wasPlaying) {
      this.source?.stop();
      this.source = null;
      this._isPlaying = false;
      cancelAnimationFrame(this.rafId);
    }
    this.startOffset = Math.max(0, Math.min(time, this.duration));
    this.onTimeUpdate(this.startOffset);
    if (wasPlaying) this.play();
  }

  setVolume(v: number): void {
    if (this.gainNode) this.gainNode.gain.value = Math.max(0, Math.min(1, v));
  }

  /** Compute RMS waveform envelope for display (downsampled to N points). */
  getWaveformEnvelope(numPoints: number): Float32Array {
    if (!this.buffer) return new Float32Array(numPoints);
    const raw = this.buffer.getChannelData(0);
    const env = new Float32Array(numPoints);
    const chunkSize = Math.floor(raw.length / numPoints);
    for (let i = 0; i < numPoints; i++) {
      let sum = 0;
      const start = i * chunkSize;
      const end = Math.min(start + chunkSize, raw.length);
      for (let j = start; j < end; j++) {
        sum += raw[j]! * raw[j]!;
      }
      env[i] = Math.sqrt(sum / (end - start));
    }
    return env;
  }

  currentTime(): number {
    if (!this.ctx || !this._isPlaying) return this.startOffset;
    return this.startOffset + (this.ctx.currentTime - this.startTime);
  }

  dispose(): void {
    cancelAnimationFrame(this.rafId);
    this.source?.stop();
    void this.ctx?.close();
    this.ctx = null;
  }

  private _tick = (): void => {
    if (!this._isPlaying || !this.ctx) return;
    const t = this.startOffset + (this.ctx.currentTime - this.startTime);
    this.onTimeUpdate(Math.min(t, this.duration));
    this.rafId = requestAnimationFrame(this._tick);
  };
}
