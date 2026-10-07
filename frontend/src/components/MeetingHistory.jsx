import React, { useEffect, useState } from 'react';
import { 
  History, 
  Calendar, 
  Users, 
  ArrowRight, 
  CheckCircle2, 
  FileText, 
  Sparkles,
  ExternalLink,
  Download,
  Trash2,
  Loader2
} from 'lucide-react';
import { listMeetings, getReportDownloadUrl, deleteMeeting } from '../api/meetings';
import { StatusBadge } from './StatusBadge';

export function MeetingHistory({ onSelectMeeting }) {
  const [meetings, setMeetings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState(null);

  const fetchMeetings = () => {
    listMeetings()
      .then((data) => {
        setMeetings(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchMeetings();
  }, []);

  const handleDelete = async (e, meetingId) => {
    e.stopPropagation();
    if (!window.confirm(`Are you sure you want to permanently delete meeting "${meetingId}" and all its audio, transcripts, and reports from disk?`)) {
      return;
    }

    setDeletingId(meetingId);
    try {
      await deleteMeeting(meetingId);
      setMeetings((prev) => prev.filter((m) => m.meeting_id !== meetingId));
    } catch (err) {
      alert(`Failed to delete meeting: ${err.message}`);
    } finally {
      setDeletingId(null);
    }
  };

  const formatDate = (folderName) => {
    // Expected format: YYYY-MM-DD_HH-MM-SS
    try {
      const [datePart, timePart] = folderName.split('_');
      const [year, month, day] = datePart.split('-');
      const [hour, min] = timePart.split('-');
      const date = new Date(year, month - 1, day, hour, min);
      return date.toLocaleDateString(undefined, {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return folderName;
    }
  };

  if (loading) {
    return (
      <div className="py-20 text-center space-y-2">
        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="text-xs text-slate-400">Loading archived sessions...</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between pb-4 border-b border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white">Meeting Archive</h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Access past recordings, speaker-mapped transcripts, and synthesized reports.
          </p>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
          {meetings.length} Total Meetings
        </span>
      </div>

      {meetings.length === 0 ? (
        <div className="py-20 text-center space-y-3 border border-dashed border-slate-800 rounded-2xl bg-slate-900/40">
          <History className="w-10 h-10 text-slate-600 mx-auto" />
          <h3 className="text-sm font-semibold text-slate-300">No meeting history found</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            Completed meetings will automatically persist in the meetings directory with full transcripts and PDF reports.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-3">
          {meetings.map((m) => {
            const participantsCount = m.participants?.length || 0;
            const pdfUrl = getReportDownloadUrl(m.meeting_id);

            return (
              <div
                key={m.meeting_id}
                className="p-5 rounded-xl bg-slate-900/60 border border-slate-800/80 hover:border-slate-700 hover:bg-slate-900/90 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4 group"
              >
                <div className="space-y-1.5">
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-bold text-white group-hover:text-blue-400 transition-colors">
                      {formatDate(m.meeting_id)}
                    </span>
                    <StatusBadge status={m.status} />
                  </div>

                  <div className="flex flex-wrap items-center gap-4 text-xs text-slate-400">
                    <span className="flex items-center gap-1.5">
                      <Users className="w-3.5 h-3.5 text-slate-500" />
                      {participantsCount} participants
                    </span>
                    <span>•</span>
                    <span className="font-mono text-[11px] text-slate-500">{m.meeting_id}</span>
                  </div>

                  {m.participants && m.participants.length > 0 && (
                    <div className="flex flex-wrap gap-1.5 pt-1">
                      {m.participants.slice(0, 4).map((p, i) => (
                        <span
                          key={i}
                          className="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-800 text-slate-300"
                        >
                          {p}
                        </span>
                      ))}
                      {m.participants.length > 4 && (
                        <span className="px-1.5 py-0.5 rounded text-[10px] text-slate-500">
                          +{m.participants.length - 4} more
                        </span>
                      )}
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  {m.has_report && (
                    <a
                      href={pdfUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="p-2.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors"
                      title="Download PDF"
                      onClick={(e) => e.stopPropagation()}
                    >
                      <Download className="w-4 h-4" />
                    </a>
                  )}

                  <button
                    onClick={(e) => handleDelete(e, m.meeting_id)}
                    disabled={deletingId === m.meeting_id}
                    className="p-2.5 rounded-lg bg-slate-800/80 hover:bg-rose-500/20 text-slate-400 hover:text-rose-400 border border-transparent hover:border-rose-500/30 transition-all cursor-pointer disabled:opacity-50"
                    title="Delete meeting from history and disk"
                  >
                    {deletingId === m.meeting_id ? (
                      <Loader2 className="w-4 h-4 animate-spin text-rose-400" />
                    ) : (
                      <Trash2 className="w-4 h-4" />
                    )}
                  </button>

                  <button
                    onClick={() => onSelectMeeting(m.meeting_id)}
                    className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-blue-600/10 hover:bg-blue-600 border border-blue-500/20 hover:border-transparent text-blue-400 hover:text-white text-xs font-semibold transition-all cursor-pointer"
                  >
                    <span>View Intel</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
