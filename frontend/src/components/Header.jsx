import React from 'react';
import { Bot, Radio, Wifi, Sparkles } from 'lucide-react';
import { StatusBadge } from './StatusBadge';

export function Header({ activeMeeting }) {
  const currentStatus = activeMeeting?.status || 'idle';

  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/60 backdrop-blur-md sticky top-0 z-40 px-6 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-lg font-bold tracking-tight text-white">Meet-AI</h1>
            <span className="text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30">
              Local Assistant
            </span>
          </div>
          <p className="text-xs text-slate-400">Intelligent Meeting Recorder & Analyzer</p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/60 text-xs text-slate-300">
          <span className="text-slate-400">Chrome CDP:</span>
          <span className="font-mono text-emerald-400">localhost:9222</span>
        </div>

        <StatusBadge status={currentStatus} />
      </div>
    </header>
  );
}
