from datetime import datetime

class RBEvent:
    def __init__(self,
                 id: int | None = None,
                 subject: str | None = None,
                 major_id: int | None = None,
                 start_time: datetime | None = None,
                 end_time: datetime | None = None):
        self.id = id
        self.subject = subject
        self.major_id = major_id
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self) -> dict:
        data = {
            'id': self.id,
            'subject': self.subject,
            'major_id': self.major_id,
            'start_time': self.start_time,
            'end_time': self.end_time
        }

        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data