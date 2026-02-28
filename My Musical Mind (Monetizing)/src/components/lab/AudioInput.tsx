/* ── AudioInput — Browse dataset / Upload file / Record mic ─────────── */

import { useState, useRef, useCallback, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Upload, Mic, MicOff, Music, X, Loader2 } from "lucide-react";
import { miDataService } from "@/services/MIDataService";
import type { MICatalogTrack } from "@/types/mi-dataset";
import type { AudioSource } from "@/stores/useLabStore";
import { useLabStore } from "@/stores/useLabStore";

const API_BASE = "http://localhost:8000/api/pipeline";

interface Props {
  accentColor: string;
}

export function AudioInput({ accentColor }: Props) {
  const { activeTab, setActiveTab, selectTrack, setPhase, setExperimentId, setProgress } = useLabStore();

  return (
    <div className="flex flex-col gap-2 h-full">
      {/* Tab selector */}
      <div className="flex items-center gap-1">
        {([
          { key: "dataset" as AudioSource, icon: Search, label: "Browse" },
          { key: "upload"  as AudioSource, icon: Upload, label: "Upload" },
          { key: "mic"     as AudioSource, icon: Mic,    label: "Record" },
        ]).map(({ key, icon: Icon, label }) => {
          const active = activeTab === key;
          return (
            <button
              key={key}
              onClick={() => setActiveTab(key)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-display transition-all duration-300"
              style={{
                background: active ? `${accentColor}12` : "transparent",
                color: active ? accentColor : "#64748B",
                border: active ? `1px solid ${accentColor}20` : "1px solid transparent",
              }}
            >
              <Icon size={13} />
              {label}
            </button>
          );
        })}
      </div>

      {/* Tab content */}
      <AnimatePresence mode="wait">
        {activeTab === "dataset" && (
          <motion.div key="dataset" initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -4 }} transition={{ duration: 0.2 }}>
            <DatasetSearch accentColor={accentColor} onSelect={selectTrack} />
          </motion.div>
        )}
        {activeTab === "upload" && (
          <motion.div key="upload" initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -4 }} transition={{ duration: 0.2 }}>
            <FileUpload accentColor={accentColor} />
          </motion.div>
        )}
        {activeTab === "mic" && (
          <motion.div key="mic" initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -4 }} transition={{ duration: 0.2 }}>
            <MicRecorder accentColor={accentColor} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

/* ── Dataset Search ──────────────────────────────────────────────────── */

/** Map catalog IDs → v4.0 pipeline IDs (when a newer analysis exists) */
const V4_TRACK_IDS: Record<string, string> = {
  "pyotr_ilyich_tchaikovsky_berliner_philharmoniker_mstislav_rostropovich__swan_lake_suite_op_20a_i_scene_swan_theme_modera":
    "tchaikovsky__swan_lake_suite_op20a_scene",
};

function DatasetSearch({ accentColor, onSelect }: { accentColor: string; onSelect: (detail: any) => void }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<MICatalogTrack[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const labTracks = miDataService.getAllTracks().filter(
      (t) => t.id.includes("swan_lake") && t.duration_s > 60
    );
    if (!query.trim()) {
      setResults(labTracks);
      return;
    }
    const q = query.toLowerCase();
    const filtered = labTracks.filter(
      (t) => t.artist.toLowerCase().includes(q) || t.title.toLowerCase().includes(q)
    );
    setResults(filtered);
  }, [query]);

  const handleSelect = async (track: MICatalogTrack) => {
    setLoading(true);
    try {
      // Use v4.0 pipeline data when available
      const resolvedId = V4_TRACK_IDS[track.id] ?? track.id;
      const detail = await miDataService.getTrackDetail(resolvedId);
      onSelect(detail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-1.5">
      <div className="relative">
        <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-600" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search analyzed tracks..."
          className="w-full pl-9 pr-3 py-2 bg-white/[0.03] border border-white/[0.06] rounded-lg text-sm text-slate-300 placeholder:text-slate-700 outline-none focus:border-white/[0.12] transition-colors font-body"
        />
        {query && (
          <button onClick={() => setQuery("")} className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-600 hover:text-slate-400">
            <X size={12} />
          </button>
        )}
      </div>

      <div className="flex-1 min-h-0 overflow-y-auto space-y-0.5" style={{ scrollbarWidth: "thin", scrollbarColor: `${accentColor}30 transparent` }}>
        {results.map((track) => (
          <button
            key={track.id}
            onClick={() => handleSelect(track)}
            disabled={loading}
            className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-left transition-all duration-200 hover:bg-white/[0.04] group"
          >
            <Music size={12} className="text-slate-700 group-hover:text-slate-400 flex-shrink-0" />
            <div className="flex-1 min-w-0">
              <div className="text-xs font-display text-slate-400 truncate group-hover:text-slate-200">
                {track.title}
              </div>
              <div className="text-[10px] font-body text-slate-600 truncate">
                {track.artist} — {Math.round(track.duration_s)}s
              </div>
            </div>
            <span
              className="text-[8px] font-mono px-1.5 py-0.5 rounded-full flex-shrink-0"
              style={{ background: `${accentColor}08`, color: `${accentColor}70` }}
            >
              {track.dominant_family}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}

/* ── File Upload ─────────────────────────────────────────────────────── */

function FileUpload({ accentColor }: { accentColor: string }) {
  const [dragOver, setDragOver] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const { setPhase, setExperimentId, setProgress } = useLabStore();

  const handleFile = useCallback(async (file: File) => {
    const ext = file.name.split(".").pop()?.toLowerCase();
    if (!["wav", "mp3", "ogg", "flac"].includes(ext || "")) {
      alert("Supported: WAV, MP3, OGG, FLAC");
      return;
    }
    setFileName(file.name);
    setUploading(true);
    setPhase("analyzing");

    try {
      const form = new FormData();
      form.append("file", file);
      const res = await fetch(`${API_BASE}/upload`, { method: "POST", body: form });
      if (!res.ok) throw new Error(await res.text());
      const { experiment_id } = await res.json();
      setExperimentId(experiment_id);

      // Poll status
      const poll = setInterval(async () => {
        try {
          const st = await fetch(`${API_BASE}/status/${experiment_id}`).then((r) => r.json());
          setProgress(st.progress ?? 0);
          if (st.status === "done") {
            clearInterval(poll);
            setPhase("done");
            setUploading(false);
          } else if (st.status === "error") {
            clearInterval(poll);
            setPhase("error");
            setUploading(false);
          }
        } catch {
          // keep polling
        }
      }, 1000);
    } catch {
      setPhase("error");
      setUploading(false);
    }
  }, [setPhase, setExperimentId, setProgress]);

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  }, [handleFile]);

  const onChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  }, [handleFile]);

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
      onDragLeave={() => setDragOver(false)}
      onDrop={onDrop}
      onClick={() => !uploading && inputRef.current?.click()}
      className="flex flex-col items-center justify-center gap-2 py-6 rounded-lg cursor-pointer transition-all duration-300"
      style={{
        background: dragOver ? `${accentColor}08` : "rgba(255,255,255,0.02)",
        border: `1px dashed ${dragOver ? accentColor : "rgba(255,255,255,0.08)"}`,
      }}
    >
      <input ref={inputRef} type="file" accept=".wav,.mp3,.ogg,.flac" onChange={onChange} className="hidden" />
      {uploading ? (
        <Loader2 size={20} className="animate-spin text-slate-500" />
      ) : (
        <Upload size={20} className="text-slate-600" />
      )}
      <span className="text-xs font-body text-slate-500">
        {uploading ? `Analyzing ${fileName}...` : fileName ? fileName : "Drop audio or click to upload"}
      </span>
      <span className="text-[10px] font-mono text-slate-700">WAV, MP3, OGG, FLAC</span>
    </div>
  );
}

/* ── Microphone Recorder ─────────────────────────────────────────────── */

function MicRecorder({ accentColor }: { accentColor: string }) {
  const [recording, setRecording] = useState(false);
  const [duration, setDuration] = useState(0);
  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const chunks = useRef<Blob[]>([]);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const { setPhase, setExperimentId, setProgress } = useLabStore();

  const startRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream, { mimeType: "audio/webm" });
      chunks.current = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunks.current.push(e.data);
      };

      recorder.onstop = async () => {
        stream.getTracks().forEach((t) => t.stop());
        const blob = new Blob(chunks.current, { type: "audio/webm" });
        const file = new File([blob], "recording.webm", { type: "audio/webm" });

        setPhase("analyzing");
        try {
          const form = new FormData();
          form.append("file", file);
          const res = await fetch(`${API_BASE}/upload`, { method: "POST", body: form });
          if (!res.ok) throw new Error(await res.text());
          const { experiment_id } = await res.json();
          setExperimentId(experiment_id);

          const poll = setInterval(async () => {
            try {
              const st = await fetch(`${API_BASE}/status/${experiment_id}`).then((r) => r.json());
              setProgress(st.progress ?? 0);
              if (st.status === "done") {
                clearInterval(poll);
                setPhase("done");
              } else if (st.status === "error") {
                clearInterval(poll);
                setPhase("error");
              }
            } catch {
              // keep polling
            }
          }, 1000);
        } catch {
          setPhase("error");
        }
      };

      mediaRecorder.current = recorder;
      recorder.start();
      setRecording(true);
      setDuration(0);
      timerRef.current = setInterval(() => setDuration((d) => d + 1), 1000);
    } catch {
      alert("Microphone access denied");
    }
  }, [setPhase, setExperimentId, setProgress]);

  const stopRecording = useCallback(() => {
    mediaRecorder.current?.stop();
    setRecording(false);
    if (timerRef.current) clearInterval(timerRef.current);
  }, []);

  const formatTime = (s: number) => `${Math.floor(s / 60)}:${(s % 60).toString().padStart(2, "0")}`;

  return (
    <div className="flex flex-col items-center gap-3 py-4">
      <button
        onClick={recording ? stopRecording : startRecording}
        className="w-14 h-14 rounded-full flex items-center justify-center transition-all duration-300"
        style={{
          background: recording ? "rgba(239,68,68,0.15)" : `${accentColor}10`,
          border: `2px solid ${recording ? "#EF4444" : accentColor}`,
          boxShadow: recording ? "0 0 24px rgba(239,68,68,0.3)" : "none",
        }}
      >
        {recording ? (
          <motion.div animate={{ scale: [1, 1.2, 1] }} transition={{ repeat: Infinity, duration: 1 }}>
            <MicOff size={22} className="text-red-400" />
          </motion.div>
        ) : (
          <Mic size={22} style={{ color: accentColor }} />
        )}
      </button>
      <span className="text-xs font-mono text-slate-500">
        {recording ? formatTime(duration) : "Tap to record"}
      </span>
      {recording && (
        <motion.div
          animate={{ opacity: [0.3, 1, 0.3] }}
          transition={{ repeat: Infinity, duration: 1.5 }}
          className="flex items-center gap-1.5"
        >
          <div className="w-2 h-2 rounded-full bg-red-500" />
          <span className="text-[10px] font-display text-red-400 uppercase tracking-wider">Recording</span>
        </motion.div>
      )}
    </div>
  );
}
