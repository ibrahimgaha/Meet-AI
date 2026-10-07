import React, { useEffect, useState } from 'react';
import { 
  Sparkles, 
  CheckCircle2, 
  ListChecks, 
  AlertCircle, 
  Copy, 
  Check, 
  FileText 
} from 'lucide-react';
import { getAnalysis } from '../api/meetings';

export function AnalysisViewer({ meetingId }) {
  const [rawText, setRawText] = useState('');
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    getAnalysis(meetingId)
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

  // Parse 5 sections from the analysis text
  const parseSections = () => {
    if (!rawText) return [];

    const sectionRegex = /\*\*(\d+\.\s+[^*]+)\*\*/g;
    const parts = [];
    let match;
    const indices = [];

    while ((match = sectionRegex.exec(rawText)) !== null) {
      indices.push({ title: match[1], start: match.index, end: match.index + match[0].length });
    }

    if (indices.length === 0) {
      return [{ title: 'Meeting Summary', content: rawText }];
    }

    for (let i = 0; i < indices.length; i++) {
      const current = indices[i];
      const next = indices[i + 1];
      const content = rawText
        .substring(current.end, next ? next.start : rawText.length)
        .trim();
      parts.push({ title: current.title, content });
    }

    return parts;
  };

  const sections = parseSections();

  if (loading) {
    return (
      <div className="py-20 text-center space-y-2">
        <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="text-xs text-slate-400">Loading AI meeting intelligence...</p>
      </div>
    );
  }

  if (!rawText) {
    return (
      <div className="py-16 text-center space-y-2 border border-dashed border-slate-800 rounded-xl">
        <Sparkles className="w-8 h-8 text-slate-600 mx-auto" />
        <p className="text-xs text-slate-400">AI analysis is not available for this session.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center">
            <Sparkles className="w-4 h-4" />
          </div>
          <span className="text-xs font-semibold text-slate-300">OpenRouter AI Analysis</span>
        </div>

        <button
          onClick={handleCopy}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-200 transition-all cursor-pointer"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
          <span>{copied ? 'Copied' : 'Copy Recap'}</span>
        </button>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {sections.map((sec, idx) => (
          <div
            key={idx}
            className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800/80 space-y-3"
          >
            <div className="flex items-center gap-2 pb-2 border-b border-slate-800/60">
              <span className="text-xs font-bold uppercase tracking-wider text-blue-400">
                {sec.title}
              </span>
            </div>

            <div className="text-xs text-slate-300 leading-relaxed whitespace-pre-line space-y-2">
              {sec.content}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
