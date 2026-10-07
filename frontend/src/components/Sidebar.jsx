import React from 'react';
import { 
  PlusCircle, 
  History, 
  Settings, 
  HelpCircle, 
  Activity,
  Layers
} from 'lucide-react';

export function Sidebar({ currentView, onViewChange, hasActiveMeeting }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: PlusCircle },
    { id: 'active', label: 'Live Session', icon: Activity, badge: hasActiveMeeting },
    { id: 'history', label: 'Meeting History', icon: History },
  ];

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-900/40 p-4 flex flex-col justify-between hidden md:flex shrink-0">
      <div className="space-y-6">
        <div>
          <p className="px-3 text-[11px] font-semibold uppercase tracking-wider text-slate-500 mb-2">
            Navigation
          </p>
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentView === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => onViewChange(item.id)}
                  className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-blue-600 text-white shadow-md shadow-blue-600/20'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <Icon className="w-4 h-4" />
                    <span>{item.label}</span>
                  </div>
                  {item.badge && (
                    <span className="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        <div className="p-3.5 rounded-xl bg-slate-800/40 border border-slate-700/50">
          <div className="flex items-center gap-2 mb-2">
            <Layers className="w-4 h-4 text-blue-400" />
            <h4 className="text-xs font-semibold text-slate-200">Pipeline Engine</h4>
          </div>
          <div className="space-y-1.5 text-[11px] text-slate-400">
            <div className="flex justify-between">
              <span>Whisper STT:</span>
              <span className="text-slate-200 font-mono">base (CUDA/CPU)</span>
            </div>
            <div className="flex justify-between">
              <span>Diarization:</span>
              <span className="text-slate-200 font-mono">pyannote 1.0</span>
            </div>
            <div className="flex justify-between">
              <span>AI Model:</span>
              <span className="text-slate-200 font-mono">OpenRouter AI</span>
            </div>
          </div>
        </div>
      </div>

      <div className="p-3 rounded-lg bg-slate-800/20 border border-slate-800 text-xs text-slate-400 flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
        <span>Local Backend Ready</span>
      </div>
    </aside>
  );
}
