import { Bell, Search } from "lucide-react";
import { Avatar } from "@/components/ui/Avatar";
import { useUserStore } from "@/stores/useUserStore";
import { personas } from "@/data/personas";

export function Header() {
  const { displayName, mind } = useUserStore();
  const persona = mind ? personas.find((p) => p.id === mind.personaId) : null;

  return (
    <header className="h-16 border-b border-m3-border flex items-center justify-between px-6 bg-m3-surface/30 backdrop-blur-sm">
      {/* Search */}
      <div className="flex items-center gap-2 bg-m3-surface border border-m3-border rounded-xl px-4 py-2 w-80">
        <Search size={16} className="text-slate-500" />
        <input
          type="text"
          placeholder="Search minds, tracks, personas..."
          className="bg-transparent text-sm text-slate-300 placeholder:text-slate-600 outline-none flex-1"
        />
      </div>

      {/* Right side */}
      <div className="flex items-center gap-4">
        {/* Notifications */}
        <button className="relative p-2 rounded-lg hover:bg-white/5 transition-colors">
          <Bell size={18} className="text-slate-400" />
          <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-m3-accent-pink" />
        </button>

        {/* User */}
        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-sm font-medium text-slate-200">{displayName || "Guest"}</div>
            {persona && (
              <div className="text-xs" style={{ color: persona.color }}>
                {persona.name}
              </div>
            )}
          </div>
          <Avatar name={displayName || "G"} size={36} borderColor={persona?.color} />
        </div>
      </div>
    </header>
  );
}
