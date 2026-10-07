import React, { useEffect, useState } from 'react';
import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';
import { StartMeeting } from './components/StartMeeting';
import { LiveMeeting } from './components/LiveMeeting';
import { ProcessingTimeline } from './components/ProcessingTimeline';
import { MeetingResults } from './components/MeetingResults';
import { MeetingHistory } from './components/MeetingHistory';
import { useMeetingStatus } from './hooks/useMeetingStatus';
import { startMeeting, stopMeeting, getActiveMeeting } from './api/meetings';
import { AlertCircle } from 'lucide-react';

export default function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [activeMeetingId, setActiveMeetingId] = useState(null);
  const [selectedHistoryId, setSelectedHistoryId] = useState(null);
  const [isStarting, setIsStarting] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // Hook tracking real-time status of active or viewed meeting
  const targetMeetingId = currentView === 'history_view' ? selectedHistoryId : activeMeetingId;
  const { meeting, loading } = useMeetingStatus(targetMeetingId);

  // Check for any currently active meeting on first load
  useEffect(() => {
    getActiveMeeting()
      .then((res) => {
        if (res.active && res.meeting) {
          setActiveMeetingId(res.meeting.meeting_id);
          setCurrentView('active');
        }
      })
      .catch((err) => console.log('No active meeting session'));
  }, []);

  const handleStartMeeting = async (meetUrl) => {
    setIsStarting(true);
    setErrorMessage('');
    try {
      const res = await startMeeting(meetUrl);
      setActiveMeetingId(res.meeting_id);
      setCurrentView('active');
    } catch (err) {
      setErrorMessage(err.message || 'Failed to start meeting');
    } finally {
      setIsStarting(false);
    }
  };

  const handleStopMeeting = async (id) => {
    try {
      await stopMeeting(id);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSelectHistoryMeeting = (id) => {
    setSelectedHistoryId(id);
    setCurrentView('history_view');
  };

  const isMeetingProcessing = meeting && [
    'ending',
    'processing_audio',
    'merging_audio',
    'transcribing',
    'diarizing',
    'mapping_speakers',
    'analyzing',
    'generating_report',
  ].includes(meeting.status);

  const isMeetingCompleted = meeting && meeting.status === 'completed';

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Header activeMeeting={meeting} />

      <div className="flex-1 flex overflow-hidden">
        <Sidebar
          currentView={currentView}
          onViewChange={(view) => {
            setCurrentView(view);
            setErrorMessage('');
          }}
          hasActiveMeeting={Boolean(activeMeetingId && meeting?.status === 'recording')}
        />

        <main className="flex-1 overflow-y-auto p-4 sm:p-8">
          {errorMessage && (
            <div className="max-w-3xl mx-auto mb-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{errorMessage}</span>
            </div>
          )}

          {currentView === 'dashboard' && (
            <StartMeeting onStart={handleStartMeeting} isConnecting={isStarting} />
          )}

          {currentView === 'active' && meeting && (
            <>
              {isMeetingCompleted ? (
                <MeetingResults meeting={meeting} />
              ) : isMeetingProcessing ? (
                <ProcessingTimeline meeting={meeting} />
              ) : (
                <LiveMeeting meeting={meeting} onStop={handleStopMeeting} />
              )}
            </>
          )}

          {currentView === 'active' && !meeting && (
            <div className="py-20 text-center space-y-3">
              <p className="text-xs text-slate-400">No active meeting in session.</p>
              <button
                onClick={() => setCurrentView('dashboard')}
                className="px-4 py-2 rounded-xl bg-blue-600 text-xs font-semibold text-white cursor-pointer"
              >
                Go to Dashboard
              </button>
            </div>
          )}

          {currentView === 'history' && (
            <MeetingHistory onSelectMeeting={handleSelectHistoryMeeting} />
          )}

          {currentView === 'history_view' && meeting && (
            <div className="space-y-4">
              <button
                onClick={() => setCurrentView('history')}
                className="text-xs text-blue-400 hover:text-blue-300 font-semibold cursor-pointer mb-2"
              >
                ← Back to History List
              </button>
              <MeetingResults meeting={meeting} />
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
