import React, { useState } from 'react';
import { 
  Video, 
  ArrowRight, 
  AlertCircle, 
  ShieldCheck, 
  Sparkles, 
  Radio, 
  FileText,
  Clock
} from 'lucide-react';

export function StartMeeting({ onStart, isConnecting }) {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    const cleanUrl = url.trim();
    if (!cleanUrl) {
      setError('Please provide a Google Meet URL');
      return;
    }

    if (!cleanUrl.includes('meet.google.com')) {
      setError('URL should be a valid Google Meet link (https://meet.google.com/xxx-xxxx-xxx)');
      return;
    }

    onStart(cleanUrl);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      {/* Welcome banner */}
      <div className="text-center space-y-3 pt-4">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-xs font-semibold text-blue-400 mb-2">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Local Autonomous Meeting Agent</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">
          Record, Transcribe & Analyze <br />
          <span className="bg-gradient-to-r from-blue-400 via-indigo-300 to-sky-400 bg-clip-text text-transparent">
            Your Google Meet Calls
          </span>
        </h2>
        <p className="text-sm sm:text-base text-slate-400 max-w-xl mx-auto">
          Connect your bot in one click. Meet-AI will join via Chrome CDP, track participants, capture audio, and deliver structured minutes with action items.
        </p>
      </div>

      {/* Input Card */}
      <div className="p-6 sm:p-8 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl shadow-black/40 backdrop-blur-md">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">
              Google Meet URL
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                <Video className="w-5 h-5" />
              </div>
              <input
                type="text"
                placeholder="https://meet.google.com/xxx-xxxx-xxx"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                disabled={isConnecting}
                className="w-full pl-11 pr-4 py-3.5 bg-slate-950/80 border border-slate-700/80 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all font-mono text-sm"
              />
            </div>
            {error && (
              <p className="mt-2 text-xs text-rose-400 flex items-center gap-1.5">
                <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                {error}
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={isConnecting}
            className="w-full flex items-center justify-center gap-2 py-3.5 px-6 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold text-sm shadow-lg shadow-blue-600/25 transition-all transform active:scale-[0.99] disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            {isConnecting ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Connecting to Google Meet...</span>
              </>
            ) : (
              <>
                <span>🚀 Connect to Meeting</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        <div className="mt-6 pt-5 border-t border-slate-800/80 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-400 gap-3">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>Authenticated via Remote Chrome (port 9222)</span>
          </div>
          <span className="text-slate-500 text-[11px]">No credentials required in browser</span>
        </div>
      </div>

      {/* Feature pillars */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-800/60 space-y-2">
          <div className="w-8 h-8 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center">
            <Radio className="w-4 h-4" />
          </div>
          <h4 className="text-xs font-semibold text-slate-200">Continuous WAV Capture</h4>
          <p className="text-[12px] text-slate-400 leading-relaxed">
            Records local loopback audio seamlessly in chunks with zero dropped packets.
          </p>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-800/60 space-y-2">
          <div className="w-8 h-8 rounded-lg bg-purple-500/10 text-purple-400 flex items-center justify-center">
            <Sparkles className="w-4 h-4" />
          </div>
          <h4 className="text-xs font-semibold text-slate-200">Speaker Diarization</h4>
          <p className="text-[12px] text-slate-400 leading-relaxed">
            Distinguishes attendees using pyannote voice embeddings and maps to participant names.
          </p>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-800/60 space-y-2">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
            <FileText className="w-4 h-4" />
          </div>
          <h4 className="text-xs font-semibold text-slate-200">Executive PDF Synthesis</h4>
          <p className="text-[12px] text-slate-400 leading-relaxed">
            Generates downloadable executive reports with decisions, summaries, and action items.
          </p>
        </div>
      </div>
    </div>
  );
}
