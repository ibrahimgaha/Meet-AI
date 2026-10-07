import React, { useEffect, useState } from 'react';
import { 
  Users, 
  Radio, 
  Clock, 
  Square, 
  CheckCircle2, 
  AlertTriangle,
  UserCheck,
  Volume2
} from 'lucide-react';
import { StatusBadge } from './StatusBadge';

export function LiveMeeting({ meeting, onStop }) {
  const [elapsed, setElapsed] = useState(0);
  const [stopping, setStopping] = useState(false);

  useEffect(() => {
    if (!meeting?.joined_at) return;

    const startTime = new Date(meeting.joined_at).getTime();

    const interval = setInterval(() => {
      // Freeze timer once call ends
      if (meeting.ended_at) {
        const endTime = new Date(meeting.ended_at).getTime();
        setElapsed(Math.max(0, Math.floor((endTime - startTime) / 1000)));
        clearInterval(interval);
      } else {
        const now = Date.now();
        setElapsed(Math.max(0, Math.floor((now - startTime) / 1000)));
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [meeting?.joined_at, meeting?.ended_at]);

  const formatTimer = (seconds) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hrs.toString().padStart(2, '0')}:${mins
      .toString()
      .padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleStopClick = async () => {
    setStopping(true);
    try {
      await onStop(meeting.meeting_id);
    } catch (e) {
      console.error(e);
      setStopping(false);
    }
  };

  const participants = meeting.participants || [];

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Live Status Header Card */}
      <div className="p-6 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl backdrop-blur-md flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <StatusBadge status={meeting.status} />
            <span className="text-xs text-slate-400 font-mono">
              ID: {meeting.meeting_id}
            </span>
          </div>

          <h2 className="text-2xl font-bold text-white tracking-tight">
            {meeting.status === 'recording' ? 'Meeting in Progress' : 'Meeting Active'}
          </h2>

          <p className="text-xs text-slate-400 max-w-lg leading-relaxed">
            {meeting.message || 'Managing active Google Meet session...'}
          </p>
        </div>

        {/* Live Timer and Controls */}
        <div className="flex flex-wrap items-center gap-4 bg-slate-950/60 p-4 rounded-xl border border-slate-800/80">
          <div className="space-y-1">
            <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Clock className="w-3 h-3 text-blue-400" />
              Duration
            </span>
            <div className="font-mono text-3xl font-extrabold text-white tracking-tight">
              {formatTimer(elapsed)}
            </div>
          </div>

          {meeting.status === 'recording' && (
            <button
              onClick={handleStopClick}
              disabled={stopping}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-rose-600/90 hover:bg-rose-600 text-white font-medium text-xs shadow-lg shadow-rose-600/20 transition-all cursor-pointer active:scale-95 disabled:opacity-50"
            >
              <Square className="w-3.5 h-3.5 fill-current" />
              <span>{stopping ? 'Stopping...' : 'Stop Meeting'}</span>
            </button>
          )}
        </div>
      </div>

      {/* Grid: Audio Stream & Participants */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Stream health & details */}
        <div className="md:col-span-1 p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
            <Volume2 className="w-4 h-4 text-blue-400" />
            Audio Engine Status
          </h3>

          <div className="space-y-3 text-xs">
            <div className="flex justify-between items-center py-2 border-b border-slate-800/60">
              <span className="text-slate-400">Capture Device</span>
              <span className="font-semibold text-slate-200">WASAPI Loopback</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-slate-800/60">
              <span className="text-slate-400">Sample Rate</span>
              <span className="font-mono text-slate-200">48,000 Hz Stereo</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-slate-800/60">
              <span className="text-slate-400">Chunk Size</span>
              <span className="font-mono text-slate-200">60 seconds</span>
            </div>
            <div className="flex justify-between items-center py-2">
              <span className="text-slate-400">Audio Level</span>
              <span className="flex items-center gap-1.5 text-emerald-400 font-semibold">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                Active
              </span>
            </div>
          </div>
        </div>

        {/* Real-time participant tracker */}
        <div className="md:col-span-2 p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
              <Users className="w-4 h-4 text-indigo-400" />
              Detected Participants ({participants.length})
            </h3>
            <span className="text-[11px] text-slate-500">Auto-detected via DOM</span>
          </div>

          {participants.length === 0 ? (
            <div className="py-10 text-center space-y-2 border border-dashed border-slate-800 rounded-xl">
              <Users className="w-8 h-8 text-slate-600 mx-auto" />
              <p className="text-xs text-slate-400">Awaiting participants in Google Meet call...</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 max-h-64 overflow-y-auto pr-1">
              {participants.map((person, index) => (
                <div
                  key={index}
                  className="flex items-center gap-3 p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 hover:border-slate-700/80 transition-all"
                >
                  <div className="w-8 h-8 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold text-xs">
                    {person.charAt(0).toUpperCase()}
                  </div>
                  <div className="truncate">
                    <p className="text-xs font-semibold text-slate-200 truncate">{person}</p>
                    <span className="inline-flex items-center gap-1 text-[10px] text-emerald-400 font-medium">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                      Present in call
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
