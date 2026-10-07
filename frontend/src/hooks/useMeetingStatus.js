import { useEffect, useState } from 'react';
import { createMeetingWebSocket, getMeetingStatus } from '../api/meetings';

export function useMeetingStatus(meetingId) {
  const [meeting, setMeeting] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!meetingId) {
      setMeeting(null);
      setLoading(false);
      return;
    }

    let isMounted = true;

    // Fetch initial state via REST
    getMeetingStatus(meetingId)
      .then((data) => {
        if (isMounted) {
          setMeeting(data);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (isMounted) {
          setError(err.message);
          setLoading(false);
        }
      });

    // Connect WebSocket for live dynamic events
    const socket = createMeetingWebSocket(
      meetingId,
      (updatedState) => {
        if (isMounted) {
          setMeeting((prev) => ({ ...prev, ...updatedState }));
        }
      },
      (err) => {
        console.warn('WebSocket connection error, fallback to REST polling', err);
      }
    );

    return () => {
      isMounted = false;
      if (socket && socket.readyState === WebSocket.OPEN) {
        socket.close();
      }
    };
  }, [meetingId]);

  return { meeting, setMeeting, loading, error };
}
