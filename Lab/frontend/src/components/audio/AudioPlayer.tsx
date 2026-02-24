import { useState, useRef, useCallback, useEffect } from 'react'
import { Play, Pause, SkipBack } from 'lucide-react'
import { AudioTimeline } from './AudioTimeline'

interface AudioPlayerProps {
  /** URL to audio file or null */
  src: string | null
  /** Accent color */
  color?: string
  className?: string
}

export function AudioPlayer({ src, color = '#3b82f6', className = '' }: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement>(null)
  const [playing, setPlaying] = useState(false)
  const [cursor, setCursor] = useState(0)
  const [duration, setDuration] = useState(0)
  const [samples, setSamples] = useState<Float32Array | null>(null)
  const rafRef = useRef<number>(0)

  // Decode audio for waveform display
  useEffect(() => {
    if (!src) { setSamples(null); return }
    const ctrl = new AbortController()

    fetch(src, { signal: ctrl.signal })
      .then((r) => r.arrayBuffer())
      .then((buf) => {
        const actx = new AudioContext()
        return actx.decodeAudioData(buf).then((decoded) => {
          setSamples(decoded.getChannelData(0))
          actx.close()
        })
      })
      .catch(() => {})

    return () => ctrl.abort()
  }, [src])

  // Animation loop for cursor
  const tick = useCallback(() => {
    const audio = audioRef.current
    if (audio && !audio.paused && audio.duration) {
      setCursor(audio.currentTime / audio.duration)
    }
    rafRef.current = requestAnimationFrame(tick)
  }, [])

  useEffect(() => {
    rafRef.current = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(rafRef.current)
  }, [tick])

  const togglePlay = () => {
    const audio = audioRef.current
    if (!audio || !src) return
    if (audio.paused) {
      audio.play()
      setPlaying(true)
    } else {
      audio.pause()
      setPlaying(false)
    }
  }

  const restart = () => {
    const audio = audioRef.current
    if (!audio) return
    audio.currentTime = 0
    setCursor(0)
  }

  const handleSeek = (pos: number) => {
    const audio = audioRef.current
    if (!audio || !audio.duration) return
    audio.currentTime = pos * audio.duration
    setCursor(pos)
  }

  return (
    <div className={`glass-card p-3 space-y-2 ${className}`}>
      {src && (
        <audio
          ref={audioRef}
          src={src}
          onLoadedMetadata={() => setDuration(audioRef.current?.duration ?? 0)}
          onEnded={() => setPlaying(false)}
        />
      )}

      {/* Timeline */}
      <AudioTimeline
        samples={samples}
        cursor={cursor}
        duration={duration}
        onSeek={handleSeek}
        color={color}
      />

      {/* Controls */}
      <div className="flex items-center gap-2">
        <button
          onClick={restart}
          className="p-1.5 rounded hover:bg-white/5 text-text-tertiary hover:text-text-secondary transition-colors"
          title="Restart"
        >
          <SkipBack size={14} />
        </button>
        <button
          onClick={togglePlay}
          className="p-1.5 rounded hover:bg-white/5 text-text-primary transition-colors"
          title={playing ? 'Pause' : 'Play'}
          disabled={!src}
        >
          {playing ? <Pause size={16} /> : <Play size={16} />}
        </button>
        <span className="mono text-[10px] text-text-tertiary ml-2">
          {formatTime(cursor * duration)} / {formatTime(duration)}
        </span>
        {!src && (
          <span className="text-[10px] text-text-tertiary italic ml-auto">no audio loaded</span>
        )}
      </div>
    </div>
  )
}

function formatTime(s: number): string {
  if (!s || !isFinite(s)) return '0:00.0'
  const m = Math.floor(s / 60)
  const sec = (s % 60).toFixed(1)
  return `${m}:${sec.padStart(4, '0')}`
}
