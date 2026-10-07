from datetime import datetime


class MeetingSession:

    def __init__(self, participants):

        self.start_time = datetime.now()
        self.end_time = None

        self.initial_participants = set(participants)

        self.current_participants = set(participants)

        self.events = []

        self.join_times = {
            participant: self.start_time
            for participant in participants
        }

        self.participant_durations = {}

    def add_event(self, participant, event):

        timestamp = datetime.now()

        self.events.append({
            "time": timestamp,
            "participant": participant,
            "event": event
        })

        if event == "ENTERED":

            self.current_participants.add(
                participant
            )

            self.join_times[participant] = timestamp

        elif event == "LEFT":

            self.current_participants.discard(
                participant
            )

            if participant in self.join_times:

                duration = (
                    timestamp
                    - self.join_times[participant]
                )

                self.participant_durations[
                    participant
                ] = (
                    self.participant_durations.get(
                        participant,
                        0
                    )
                    + duration.total_seconds()
                )

                del self.join_times[participant]

    def end(self):

        self.end_time = datetime.now()

        # Calculate duration for people
        # who are still inside the meeting.

        for participant in list(
            self.current_participants
        ):

            if participant in self.join_times:

                duration = (
                    self.end_time
                    - self.join_times[participant]
                )

                self.participant_durations[
                    participant
                ] = (
                    self.participant_durations.get(
                        participant,
                        0
                    )
                    + duration.total_seconds()
                )

                del self.join_times[participant]

    def get_duration(self):

        if self.end_time is None:

            return None

        return self.end_time - self.start_time

    def get_participant_duration(
        self,
        participant
    ):

        return self.participant_durations.get(
            participant,
            0
        )

    def get_summary(self):

        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.get_duration(),
            "initial_participants": self.initial_participants,
            "current_participants": self.current_participants,
            "events": self.events,
            "participant_durations":
                self.participant_durations
        }