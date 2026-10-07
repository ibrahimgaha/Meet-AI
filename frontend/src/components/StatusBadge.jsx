import React from 'react';
import { 
  Radio, 
  CheckCircle2, 
  Clock, 
  AlertCircle, 
  Loader2, 
  Sparkles,
  WifiOff
} from 'lucide-react';

export function StatusBadge({ status, className = '' }) {
  switch (status) {
    case 'recording':
      return (
        <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20 animate-pulse ${className}`}>
          <span className="w-2 h-2 rounded-full bg-rose-500"></span>
          Recording Live
        </span>
      );
    case 'connecting':
    case 'opening_meet':
    case 'joining':
      return (
        <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-amber-500/10 text-amber-400 border border-amber-500/20 ${className}`}>
          <Loader2 className="w-3.5 h-3.5 animate-spin" />
          Connecting...
        </span>
      );
    case 'merging_audio':
    case 'transcribing':
    case 'diarizing':
    case 'mapping_speakers':
    case 'analyzing':
    case 'generating_report':
    case 'processing_audio':
      return (
        <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-blue-500/10 text-blue-400 border border-blue-500/20 ${className}`}>
          <Sparkles className="w-3.5 h-3.5 animate-pulse text-blue-400" />
          Processing AI
        </span>
      );
    case 'completed':
      return (
        <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 ${className}`}>
          <CheckCircle2 className="w-3.5 h-3.5" />
          Completed
        </span>
      );
    case 'error':
      return (
        <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-red-500/10 text-red-400 border border-red-500/20 ${className}`}>
          <AlertCircle className="w-3.5 h-3.5" />
          Failed
        </span>
      );
    case 'idle':
    default:
      return (
        <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-400 border border-slate-700 ${className}`}>
          <span className="w-2 h-2 rounded-full bg-slate-500"></span>
          Bot Ready
        </span>
      );
  }
}
