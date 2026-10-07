import React from 'react';
import { 
  CheckCircle2, 
  Loader2, 
  Circle, 
  Sparkles,
  FileAudio,
  Radio,
  Users,
  FileText
} from 'lucide-react';

const STEPS = [
  { id: 'merging_audio', label: 'Audio Merging', desc: 'Merging 60-second WAV chunks into full master recording', icon: FileAudio },
  { id: 'transcribing', label: 'Whisper Transcription', desc: 'Local AI speech-to-text inference with timestamp alignment', icon: Radio },
  { id: 'diarizing', label: 'Speaker Diarization', desc: 'Extracting voice embeddings and segmenting multiple speakers (pyannote)', icon: Users },
  { id: 'mapping_speakers', label: 'Speaker Mapping', desc: 'Correlating identified speaker clusters with participant roster', icon: Users },
  { id: 'analyzing', label: 'AI Meeting Analysis', desc: 'Extracting key takeaways, decisions, and action items via OpenRouter', icon: Sparkles },
  { id: 'generating_report', label: 'PDF Report Generation', desc: 'Compiling formatted ReportLab PDF executive documentation', icon: FileText },
];

export function ProcessingTimeline({ meeting }) {
  const currentStep = meeting.progress_step || meeting.status;
  const isFinished = meeting.status === 'completed';

  const getStepStatus = (stepId, index) => {
    if (isFinished) return 'completed';

    const currentStepIndex = STEPS.findIndex((s) => s.id === currentStep);
    if (currentStepIndex === -1) {
      return index === 0 ? 'in_progress' : 'pending';
    }

    if (index < currentStepIndex) return 'completed';
    if (index === currentStepIndex) return 'in_progress';
    return 'pending';
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl backdrop-blur-md">
        <div className="flex items-center justify-between pb-6 border-b border-slate-800">
          <div>
            <span className="text-xs font-semibold text-blue-400 uppercase tracking-wider">
              Post-Meeting Synthesis
            </span>
            <h2 className="text-xl font-bold text-white mt-1">Processing Meeting Intelligence</h2>
            <p className="text-xs text-slate-400 mt-0.5">
              The AI pipeline is autonomously processing audio, extracting dialogue, and generating reports.
            </p>
          </div>
          <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-blue-400 animate-pulse" />
          </div>
        </div>

        {/* Timeline steps */}
        <div className="mt-8 relative space-y-6">
          {STEPS.map((step, index) => {
            const status = getStepStatus(step.id, index);
            const StepIcon = step.icon;

            return (
              <div key={step.id} className="flex items-start gap-4 relative">
                {/* Connector line */}
                {index < STEPS.length - 1 && (
                  <div 
                    className={`absolute left-5 top-10 bottom-[-16px] w-[2px] transition-colors ${
                      status === 'completed' ? 'bg-emerald-500/50' : 'bg-slate-800'
                    }`} 
                  />
                )}

                {/* Status icon bullet */}
                <div className="shrink-0 z-10">
                  {status === 'completed' && (
                    <div className="w-10 h-10 rounded-full bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                      <CheckCircle2 className="w-5 h-5" />
                    </div>
                  )}
                  {status === 'in_progress' && (
                    <div className="w-10 h-10 rounded-full bg-blue-500/20 border border-blue-500 flex items-center justify-center text-blue-400 shadow-lg shadow-blue-500/20">
                      <Loader2 className="w-5 h-5 animate-spin" />
                    </div>
                  )}
                  {status === 'pending' && (
                    <div className="w-10 h-10 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-600">
                      <Circle className="w-4 h-4" />
                    </div>
                  )}
                </div>

                {/* Content */}
                <div className="pt-1.5 flex-1">
                  <div className="flex items-center justify-between">
                    <h4 className={`text-sm font-semibold ${
                      status === 'in_progress' ? 'text-blue-300' : status === 'completed' ? 'text-slate-200' : 'text-slate-500'
                    }`}>
                      {step.label}
                    </h4>
                    <span className="text-[11px] font-mono">
                      {status === 'completed' && <span className="text-emerald-400">Done</span>}
                      {status === 'in_progress' && <span className="text-blue-400 animate-pulse">Running...</span>}
                      {status === 'pending' && <span className="text-slate-600">Queued</span>}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mt-1">{step.desc}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
