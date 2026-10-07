import React, { useEffect, useState } from 'react';
import { FileText, Copy, Check, Search, User } from 'lucide-react';
import { getTranscript } from '../api/meetings';

export function TranscriptViewer({ meetingId }) {
  const [rawText, setRawText] = useState('');
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    getTranscript(meetingId)
      .then((data) => {
        setRawText(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [meetingId]);

  const handleCopy = () => {
    navigator.clipboard.writeText(rawText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Parse transcript lines: [start -> end] Speaker: Message
  const parseLines = () => {
    if (!rawText) return [];
    return rawText
      .split('\n')
      .map((line) => line.trim())
      .filter(Boolean)
      .map((line) => {
        const match = line.match(/^\[(.*?)\]\s*(.*?):\s*(.*)$/);
        if (match) {
          return {
            timestamp: match[1],
            speaker: match[2],
            text: match[3],
          };
        }
        return {
          timestamp: '',
          speaker: 'Speaker',
          text: line,
        };
      });
  };

  const lines = parseLines().filter((item) => {
    if (!filter) return true;
    const q = filter.toLowerCase();
    return (
      item.speaker.toLowerCase().includes(q) ||
      item.text.toLowerCase().includes(q)
    );
  });

  if (loading) {
    return (
      <div className="py-20 text-center space-y-2">
        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="text-xs text-slate-400">Loading transcript data...</p>
      </div>
    );
  }

  if (!rawText) {
    return (
      <div className="py-16 text-center space-y-2 border border-dashed border-slate-800 rounded-xl">
        <FileText className="w-8 h-8 text-slate-600 mx-auto" />
        <p className="text-xs text-slate-400">No transcript available for this meeting session.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Controls */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            placeholder="Search transcript or speaker..."
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 bg-slate-900 border border-slate-800 rounded-lg text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
        </div>

        <button
          onClick={handleCopy}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-200 transition-all cursor-pointer"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
          <span>{copied ? 'Copied' : 'Copy All'}</span>
        </button>
      </div>

      {/* Transcript bubbles */}
      <div className="space-y-3 max-h-[600px] overflow-y-auto pr-1">
        {lines.length === 0 ? (
          <p className="text-center text-xs text-slate-500 py-8">No matching dialogue found.</p>
        ) : (
          lines.map((item, index) => (
            <div
              key={index}
              className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800/80 hover:border-slate-700 transition-all space-y-1.5"
            >
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <span className="w-6 h-6 rounded-md bg-blue-500/10 text-blue-400 flex items-center justify-center font-bold text-[10px]">
                    {item.speaker.charAt(0).toUpperCase()}
                  </span>
                  <span className="font-semibold text-slate-200">{item.speaker}</span>
                </div>
                {item.timestamp && (
                  <span className="text-[11px] font-mono text-slate-500 bg-slate-950 px-2 py-0.5 rounded border border-slate-800/60">
                    {item.timestamp}
                  </span>
                )}
              </div>
              <p className="text-xs text-slate-300 leading-relaxed pl-8">
                {item.text}
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
