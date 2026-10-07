from datetime import datetime


class MeetingState:

    def __init__(self, participants):

        self.participants = set(participants)

        self.join_times = {
            participant: datetime.now()
            for participant in participants
        }

    def participant_joined(self, participant):

        self.participants.add(participant)

        self.join_times[participant] = datetime.now()

    def participant_left(self, participant):

        self.participants.discard(participant)

        self.join_times.pop(
            participant,
            None
        )

    def is_present(self, participant):

        return participant in self.participants

    def get_current_participants(self):

        return set(self.participants)

    def get_participant_count(self):

        return len(self.participants)

    def get_duration(self, participant):

        if participant not in self.join_times:

            return None

        duration = (
            datetime.now()
            - self.join_times[participant]
        )

        return duration.total_seconds()