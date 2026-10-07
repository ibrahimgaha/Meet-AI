import React, { useState } from 'react';
import { 
  FileText, 
  Sparkles, 
  Download, 
  CheckCircle2, 
  Clock, 
  Users, 
  ExternalLink 
} from 'lucide-react';
import { TranscriptViewer } from './TranscriptViewer';
import { AnalysisViewer } from './AnalysisViewer';
import { getReportDownloadUrl } from '../api/meetings';

export function MeetingResults({ meeting }) {
  const [activeTab, setActiveTab] = useState('analysis');

  const reportUrl = getReportDownloadUrl(meeting.meeting_id);
  const participantsCount = meeting.participants?.length || 0;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Success banner */}
      <div className="p-6 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <CheckCircle2 className="w-3.5 h-3.5" />
            Meeting Successfully Processed
          </div>

          <h2 className="text-2xl font-bold text-white tracking-tight">
            Synthesis & Documentation Ready
          </h2>

          <div className="flex flex-wrap items-center gap-4 text-xs text-slate-400 pt-1">
            <span className="flex items-center gap-1.5">
              <Users className="w-4 h-4 text-blue-400" />
              {participantsCount} Participants
            </span>
            <span>•</span>
            <span className="font-mono text-slate-400">ID: {meeting.meeting_id}</span>
          </div>
        </div>

        {/* Action download button */}
        <a
          href={reportUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs shadow-lg shadow-blue-600/20 transition-all transform active:scale-95"
        >
          <Download className="w-4 h-4" />
          <span>Download PDF Report</span>
        </a>
      </div>

      {/* Tabs navigation */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab('analysis')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
            activeTab === 'analysis'
              ? 'bg-blue-600 text-white shadow-md shadow-blue-600/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>AI Executive Analysis</span>
        </button>

        <button
          onClick={() => setActiveTab('transcript')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
            activeTab === 'transcript'
              ? 'bg-blue-600 text-white shadow-md shadow-blue-600/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
        >
          <FileText className="w-3.5 h-3.5" />
          <span>Speaker-Aligned Transcript</span>
        </button>

        <a
          href={reportUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-semibold text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 transition-all ml-auto"
        >
          <span>Open PDF</span>
          <ExternalLink className="w-3 h-3" />
        </a>
      </div>

      {/* Tab Panels */}
      <div>
        {activeTab === 'analysis' && <AnalysisViewer meetingId={meeting.meeting_id} />}
        {activeTab === 'transcript' && <TranscriptViewer meetingId={meeting.meeting_id} />}
      </div>
    </div>
  );
}
