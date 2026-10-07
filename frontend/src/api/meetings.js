const API_BASE = '/api';

export async function startMeeting(meetUrl) {
  const response = await fetch(`${API_BASE}/meetings/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ meet_url: meetUrl }),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to start meeting session');
  }
  return response.json();
}

export async function stopMeeting(meetingId) {
  const response = await fetch(`${API_BASE}/meetings/${meetingId}/stop`, {
    method: 'POST',
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to stop meeting');
  }
  return response.json();
}

export async function getActiveMeeting() {
  const response = await fetch(`${API_BASE}/meetings/active`);
  if (!response.ok) throw new Error('Failed to check active meeting');
  return response.json();
}

export async function getMeetingStatus(meetingId) {
  const response = await fetch(`${API_BASE}/meetings/${meetingId}/status`);
  if (!response.ok) throw new Error('Failed to load meeting status');
  return response.json();
}

export async function listMeetings() {
  const response = await fetch(`${API_BASE}/meetings`);
  if (!response.ok) throw new Error('Failed to fetch meeting history');
  return response.json();
}

export async function getTranscript(meetingId) {
  const response = await fetch(`${API_BASE}/meetings/${meetingId}/transcript`);
  if (!response.ok) throw new Error('Transcript not available');
  return response.text();
}

export async function getAnalysis(meetingId) {
  const response = await fetch(`${API_BASE}/meetings/${meetingId}/analysis`);
  if (!response.ok) throw new Error('Analysis not available');
  return response.text();
}

export function getReportDownloadUrl(meetingId) {
  return `${API_BASE}/meetings/${meetingId}/report`;
}

export async function deleteMeeting(meetingId) {
  const response = await fetch(`${API_BASE}/meetings/${meetingId}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to delete meeting');
  }
  return response.json();
}

export function createMeetingWebSocket(meetingId, onMessage, onError) {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}/ws/meetings/${meetingId}`;
  const socket = new WebSocket(wsUrl);

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onMessage(data);
    } catch (err) {
      console.error('Error parsing WebSocket message:', err);
    }
  };

  if (onError) {
    socket.onerror = onError;
  }

  return socket;
}
